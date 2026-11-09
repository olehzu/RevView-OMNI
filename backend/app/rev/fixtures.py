"""Synthetic Data for v0.1.0 (``CO-sandbox-development``, section 8.2.10; design/rev.md).

One review package in "In preparation", seeded at startup because
``UC-REV-create-review`` is not built, and the SVN and Jenkins history the fakes answer
from. The ticket key is a placeholder; nothing here is production content.
"""

from datetime import UTC, datetime

from app.integration.jenkins import JenkinsBuild
from app.integration.svn import SvnChangedFile
from app.rev.models import ReviewPackage, ReviewPackageStatus

REVIEW_ID = "rev-0001"
JIRA_TICKET_KEY = "SYN-1"
SVN_BRANCH = "SYN-1-timer-fix"


def review_package() -> ReviewPackage:
    return ReviewPackage(
        review_id=REVIEW_ID,
        status=ReviewPackageStatus.IN_PREPARATION,
        jira_ticket_key=JIRA_TICKET_KEY,
    )


def changed_file(path: str, revision: str | None = "1042") -> SvnChangedFile:
    """A Changed File with a synthetic repository link and diff."""
    link = f"https://svn.example.invalid/repo/{path}"
    return SvnChangedFile(
        path=path,
        revision=revision,
        repository_link=f"{link}?p={revision}" if revision else link,
        diff=(
            f"Index: {path}\n"
            "===================================================================\n"
            f"--- {path}\t(revision 1041)\n"
            f"+++ {path}\t(working copy)\n"
            "@@ -1 +1 @@\n"
            "-SYNTHETIC_TIMEOUT = 10\n"
            "+SYNTHETIC_TIMEOUT = 20\n"
        ),
    )


def svn_branches() -> dict[str, list[SvnChangedFile]]:
    """The fixture branch touches three Platform x Category pairs; the others are decoys."""
    return {
        SVN_BRANCH: [
            changed_file("tools/common/branches/SYN-1-timer-fix/src/timer.py"),
            changed_file("code/falcon/branches/SYN-1-timer-fix/src/scheduler.c"),
            changed_file("code/falcon/branches/SYN-1-timer-fix/src/scheduler.h"),
            changed_file("tests/falcon/branches/SYN-1-timer-fix/test_scheduler.c"),
        ],
        "SYN-10-cleanup": [
            changed_file("code/phoenix/branches/SYN-10-cleanup/src/unused.c"),
        ],
        "OTHER-2-docs": [],
    }


def jenkins_builds() -> list[JenkinsBuild]:
    """Two matching builds, listed oldest first, and two decoys that must not match."""

    def build(
        number: int, name: str, branch: str, result: str, built_at: datetime
    ) -> JenkinsBuild:
        return JenkinsBuild(
            build_number=number,
            name=name,
            description="Synthetic build",
            branch_parameter=branch,
            result=result,
            built_at=built_at,
        )

    return [
        build(
            55,
            "SYN-1 timer fix",
            SVN_BRANCH,
            "FAILURE",
            datetime(2026, 11, 4, 9, 40, 3, tzinfo=UTC),
        ),
        build(
            57,
            "SYN-1 timer fix",
            SVN_BRANCH,
            "SUCCESS",
            datetime(2026, 11, 5, 14, 2, 11, tzinfo=UTC),
        ),
        build(
            58,
            "SYN-1 timer fix",
            "trunk",
            "SUCCESS",
            datetime(2026, 11, 6, 8, 0, 0, tzinfo=UTC),
        ),
        build(
            59,
            "SYN-10 cleanup",
            SVN_BRANCH,
            "SUCCESS",
            datetime(2026, 11, 6, 9, 0, 0, tzinfo=UTC),
        ),
    ]
