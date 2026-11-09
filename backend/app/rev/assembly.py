"""UC-REV-assemble-materials: steps 1 to 6 and extensions 2a1 and 4a1 (design/rev.md)."""

import logging
from collections import defaultdict
from datetime import UTC
from threading import Lock

from app.errors import AppError
from app.integration.common import IntegrationUnavailable
from app.integration.jenkins import JenkinsAdapter
from app.integration.svn import SvnAdapter, SvnChangedFile
from app.rev.models import (
    Category,
    ChangedFile,
    Diff,
    Evidence,
    JenkinsBuild,
    MissingMaterial,
    Platform,
    ReviewChecklist,
    ReviewChecklistTab,
    ReviewPackage,
    ReviewPackageStatus,
    ReviewRecord,
)
from app.rev.repository import ReviewPackageRepository

logger = logging.getLogger(__name__)

# One assembly at a time, so two requests cannot both pass PRE-1 and overwrite each
# other's result (section 8.2.8). The in-memory store has no transactions to do it.
_assembly_lock = Lock()

_PLATFORMS = list(Platform)
_CATEGORIES = list(Category)


class ReviewPackageNotFound(AppError):
    def __init__(self) -> None:
        super().__init__(
            404, "REVIEW_PACKAGE_NOT_FOUND", "No review package has that id."
        )


class ReviewPackageNotInPreparation(AppError):
    """PRE-1: assembly runs only on a package in "In preparation"."""

    def __init__(self, status: ReviewPackageStatus) -> None:
        super().__init__(
            409,
            "REVIEW_PACKAGE_NOT_IN_PREPARATION",
            f'The review package is "{status}", not "In preparation", '
            "so its materials cannot be assembled.",
        )


class AssemblyIncomplete(AppError):
    """Nothing to assemble; ``message`` names the gap. Nothing is stored."""

    def __init__(self, gap: str) -> None:
        super().__init__(409, "ASSEMBLY_INCOMPLETE", gap)


class UnclassifiablePath(ValueError):
    pass


def classify(path: str) -> tuple[Platform, Category]:
    """Step 3: the Platform and Code/Tools/Tests Category a repository path belongs to.

    The path has the form ``<category>/<platform>/branches/<branch>/<file…>``; for
    example ``tools/common/branches/SYN-1-timer-fix/src/timer.py`` is common, tools.
    """
    segments = path.split("/")
    if (
        len(segments) < 5
        or segments[2] != "branches"
        or segments[0] not in _CATEGORIES
        or segments[1] not in _PLATFORMS
        or not all(segments[3:])
    ):
        raise UnclassifiablePath(path)
    return Platform(segments[1]), Category(segments[0])


class AssemblyService:
    def __init__(
        self,
        repository: ReviewPackageRepository,
        svn: SvnAdapter,
        jenkins: JenkinsAdapter,
    ) -> None:
        self._repository = repository
        self._svn = svn
        self._jenkins = jenkins

    def assemble(self, review_id: str) -> ReviewPackage:
        try:
            with _assembly_lock:
                package = self._assemble(review_id)
        except IntegrationUnavailable as exc:
            _log(review_id, "unavailable", f"{exc.source.upper()}_UNAVAILABLE")
            raise
        except AppError as exc:
            _log(review_id, "refused", exc.code)
            raise
        _log(review_id, package.status, None)
        return package

    def _assemble(self, review_id: str) -> ReviewPackage:
        package = self._repository.get(review_id)
        if package is None:
            raise ReviewPackageNotFound()
        if package.status != ReviewPackageStatus.IN_PREPARATION:
            raise ReviewPackageNotInPreparation(package.status)

        # Step 1: v0.1.0 reads the Jira Ticket key from the package, with no Jira call.
        ticket_key = package.jira_ticket_key

        # Steps 2 and 3. Whether SVN fails or leaves nothing to assemble, the stored
        # package keeps no materials from an earlier run, and records SVN as observed.
        try:
            branch, diffs, missing = self._svn_materials(ticket_key)
        except IntegrationUnavailable:
            self._repository.save(
                _without_materials(package, svn=Evidence.UNAVAILABLE, jenkins=None)
            )
            raise
        except AssemblyIncomplete:
            self._repository.save(
                _without_materials(package, svn=Evidence.AVAILABLE, jenkins=None)
            )
            raise

        # Step 4: Jenkins evidence for the package, newest first, newest preselected.
        try:
            found = self._jenkins.find_builds(ticket_key, branch)
        except IntegrationUnavailable:
            self._repository.save(
                _without_materials(
                    package, svn=Evidence.AVAILABLE, jenkins=Evidence.UNAVAILABLE
                )
            )
            raise
        builds = sorted(
            (
                JenkinsBuild(
                    build_number=b.build_number,
                    name=b.name,
                    result=b.result,
                    built_at=b.built_at.astimezone(UTC),
                )
                for b in found
            ),
            key=lambda b: (b.built_at, b.build_number),
            reverse=True,
        )

        # Step 5.
        checklist = ReviewChecklist(
            tabs=[
                ReviewChecklistTab(
                    platform=platform,
                    changed_files=[
                        f.path
                        for d in diffs
                        if d.platform == platform
                        for f in d.changed_files
                    ],
                )
                for platform in _PLATFORMS
                if any(d.platform == platform for d in diffs)
            ]
        )
        record = ReviewRecord(
            id="rr-" + review_id.removeprefix("rev-"),
            review_id=review_id,
            jira_ticket_key=ticket_key,
        )

        # Step 6. 2a1 wins over 4a1: without its Revisions the package is not assembled.
        if missing:
            status = ReviewPackageStatus.IN_PREPARATION
        elif not builds:
            status = ReviewPackageStatus.PENDING_BUILD_VALIDATION
        else:
            status = ReviewPackageStatus.MATERIALS_ASSEMBLED

        assembled = package.model_copy(
            update={
                "status": status,
                "svn_branch": branch,
                "svn_evidence": Evidence.AVAILABLE,
                "jenkins_evidence": Evidence.AVAILABLE,
                "diffs": diffs,
                "jenkins_builds": builds,
                "preselected_build": builds[0].build_number if builds else None,
                "review_checklist": checklist,
                "review_record": record,
                "missing": missing,
            }
        )
        self._repository.save(assembled)
        return assembled

    def _svn_materials(
        self, ticket_key: str
    ) -> tuple[str, list[Diff], list[MissingMaterial]]:
        """Step 2 (the SVN Branch and its Changed Files), 2a1, and step 3 (the Diffs)."""
        branch = self._one_branch(ticket_key)
        svn_files = self._svn.changed_files(branch)
        if not svn_files:
            raise AssemblyIncomplete(f"The SVN Branch {branch} has no Changed Files.")

        # 2a1: a Changed File without a Revision is flagged, and still goes into its
        # Diff and its Review Checklist tab.
        missing = [
            MissingMaterial(path=f.path, missing="revision")
            for f in sorted(svn_files, key=lambda f: f.path)
            if not f.revision
        ]
        return branch, _diffs(svn_files), missing

    def _one_branch(self, ticket_key: str) -> str:
        branches = self._svn.find_branches(ticket_key)
        if not branches:
            raise AssemblyIncomplete(
                f"No SVN Branch name contains the Jira Ticket key {ticket_key}."
            )
        if len(branches) > 1:
            raise AssemblyIncomplete(
                f"Several SVN Branches match the Jira Ticket key {ticket_key}: "
                f"{', '.join(sorted(branches))}."
            )
        return branches[0]


def _diffs(svn_files: list[SvnChangedFile]) -> list[Diff]:
    """One Diff per Platform x Category touched, in Platform then Category order."""
    groups: defaultdict[tuple[Platform, Category], list[SvnChangedFile]] = defaultdict(
        list
    )
    for svn_file in svn_files:
        try:
            groups[classify(svn_file.path)].append(svn_file)
        except UnclassifiablePath:
            raise AssemblyIncomplete(
                f"The Changed File {svn_file.path} is not under "
                "<category>/<platform>/branches/<branch>/, "
                "so its Platform and Category are unknown."
            ) from None

    diffs = []
    for platform, category in sorted(
        groups,
        key=lambda pair: (_PLATFORMS.index(pair[0]), _CATEGORIES.index(pair[1])),
    ):
        files = sorted(groups[(platform, category)], key=lambda f: f.path)
        diffs.append(
            Diff(
                platform=platform,
                category=category,
                diff="".join(
                    f.diff if f.diff.endswith("\n") else f.diff + "\n" for f in files
                ),
                changed_files=[
                    ChangedFile(
                        path=f.path,
                        revision=f.revision or None,
                        repository_link=f.repository_link,
                    )
                    for f in files
                ],
            )
        )
    return diffs


def _without_materials(
    package: ReviewPackage, svn: Evidence, jenkins: Evidence | None
) -> ReviewPackage:
    """The package after an outage: "In preparation", the evidence as observed, and no
    materials, so nothing half-assembled is stored (design/rev.md)."""
    return package.model_copy(
        update={
            "status": ReviewPackageStatus.IN_PREPARATION,
            "svn_branch": None,
            "svn_evidence": svn,
            "jenkins_evidence": jenkins,
            "diffs": [],
            "jenkins_builds": [],
            "preselected_build": None,
            "review_checklist": None,
            "review_record": None,
            "missing": [],
        }
    )


def _log(review_id: str, outcome: str, code: str | None) -> None:
    """One line per assembly; never diff or source content (section 8.2.7)."""
    logger.info("assembly review_id=%r outcome=%s code=%s", review_id, outcome, code)
