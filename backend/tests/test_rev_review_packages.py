"""Integration tests for UC-REV-assemble-materials through the API (design/rev.md, Tests).

Each test gets a fresh store holding the fixture package, and fakes it can make fail
or answer differently (section 8.2.10, Synthetic Data only).
"""

import logging
from collections.abc import Iterator, Sequence
from dataclasses import dataclass
from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.integration.jenkins import FakeJenkinsAdapter, JenkinsBuild
from app.integration.svn import FakeSvnAdapter, SvnChangedFile
from app.main import app
from app.rev import fixtures
from app.rev.repository import ReviewPackageRepository
from app.rev.router import get_jenkins_adapter, get_repository, get_svn_adapter

ASSEMBLY = f"/api/v1/review-packages/{fixtures.REVIEW_ID}/assembly"
PACKAGE = f"/api/v1/review-packages/{fixtures.REVIEW_ID}"


@dataclass
class World:
    client: TestClient
    svn: FakeSvnAdapter
    jenkins: FakeJenkinsAdapter

    def use(
        self,
        branches: dict[str, Sequence[SvnChangedFile]] | None = None,
        builds: Sequence[JenkinsBuild] | None = None,
        svn_fails_on: Sequence[str] = (),
        jenkins_fails_on: Sequence[str] = (),
    ) -> None:
        if branches is not None:
            self.svn.branches = branches
        if builds is not None:
            self.jenkins.builds = builds
        self.svn.fail_on = svn_fails_on
        self.jenkins.fail_on = jenkins_fails_on

    def assemble(self) -> Any:
        return self.client.post(ASSEMBLY)

    def package(self) -> dict[str, Any]:
        response = self.client.get(PACKAGE)
        assert response.status_code == 200
        data: dict[str, Any] = response.json()["data"]
        return data


@pytest.fixture
def world() -> Iterator[World]:
    repository = ReviewPackageRepository()
    repository.save(fixtures.review_package())
    svn = FakeSvnAdapter(branches=fixtures.svn_branches())
    jenkins = FakeJenkinsAdapter(builds=fixtures.jenkins_builds())
    app.dependency_overrides[get_repository] = lambda: repository
    app.dependency_overrides[get_svn_adapter] = lambda: svn
    app.dependency_overrides[get_jenkins_adapter] = lambda: jenkins
    try:
        yield World(TestClient(app), svn, jenkins)
    finally:
        app.dependency_overrides.clear()


def _diff_files(data: dict[str, Any], platform: str | None = None) -> list[str]:
    return [
        f["path"]
        for d in data["diffs"]
        if platform is None or d["platform"] == platform
        for f in d["changed_files"]
    ]


# --- Main success scenario -------------------------------------------------------


def test_main_flow_assembles_the_fixture_package(world: World):
    response = world.assemble()

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["status"] == "Materials assembled"
    assert data["review_id"] == fixtures.REVIEW_ID
    assert data["jira_ticket_key"] == fixtures.JIRA_TICKET_KEY
    assert data["svn_branch"] == "SYN-1-timer-fix"
    assert data["svn_evidence"] == "available"
    assert data["jenkins_evidence"] == "available"
    assert data["missing"] == []

    # One Diff per Platform x Category touched, and no other.
    assert [(d["platform"], d["category"]) for d in data["diffs"]] == [
        ("common", "tools"),
        ("falcon", "code"),
        ("falcon", "tests"),
    ]
    assert sorted(_diff_files(data)) == sorted(
        f.path for f in fixtures.svn_branches()["SYN-1-timer-fix"]
    )
    for diff in data["diffs"]:
        for changed in diff["changed_files"]:
            assert changed["revision"]
            assert changed["repository_link"]
            assert f"Index: {changed['path']}" in diff["diff"]

    # BR-diff-checklist-match: each tab lists exactly its Platform's Diff files.
    tabs = data["review_checklist"]["tabs"]
    assert [tab["platform"] for tab in tabs] == ["common", "falcon"]
    for tab in tabs:
        assert sorted(tab["changed_files"]) == sorted(
            _diff_files(data, tab["platform"])
        )

    assert data["review_record"] == {
        "id": "rr-0001",
        "review_id": fixtures.REVIEW_ID,
        "jira_ticket_key": fixtures.JIRA_TICKET_KEY,
    }

    # Matching builds only, newest first, the newest preselected; UTC with Z.
    assert data["jenkins_builds"] == [
        {
            "build_number": 57,
            "name": "SYN-1 timer fix",
            "result": "SUCCESS",
            "built_at": "2026-11-05T14:02:11Z",
        },
        {
            "build_number": 55,
            "name": "SYN-1 timer fix",
            "result": "FAILURE",
            "built_at": "2026-11-04T09:40:03Z",
        },
    ]
    assert data["preselected_build"] == 57

    # OI-35: Jenkins was only asked to find builds, never to start one.
    assert world.jenkins.calls == ["find_builds"]

    assert world.package() == data


def test_newest_build_is_preselected_whatever_its_result(world: World):
    builds = fixtures.jenkins_builds()
    newest = max(
        (b for b in builds if b.build_number in (55, 57)), key=lambda b: b.built_at
    )
    world.use(
        builds=[
            JenkinsBuild(**{**vars(b), "result": "FAILURE"}) if b is newest else b
            for b in builds
        ]
    )

    data = world.assemble().json()["data"]

    assert data["preselected_build"] == 57
    assert data["jenkins_builds"][0]["result"] == "FAILURE"


def test_package_before_assembly_has_no_evidence_fetched(world: World):
    data = world.package()

    assert data["status"] == "In preparation"
    assert data["svn_evidence"] is None
    assert data["jenkins_evidence"] is None
    assert data["diffs"] == []


# --- Extension 2a1: a Changed File has no Revision -------------------------------


def _branch_with_missing_revision() -> dict[str, Sequence[SvnChangedFile]]:
    files = list(fixtures.svn_branches()["SYN-1-timer-fix"])
    files[1] = fixtures.changed_file(files[1].path, revision=None)
    return {"SYN-1-timer-fix": files}


def test_2a1_missing_revision_is_flagged_and_package_stays_in_preparation(
    world: World,
):
    world.use(branches=_branch_with_missing_revision())
    path = "code/falcon/branches/SYN-1-timer-fix/src/scheduler.c"

    response = world.assemble()

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["status"] == "In preparation"
    assert data["missing"] == [{"path": path, "missing": "revision"}]
    # The file still goes into its Diff and its Review Checklist tab.
    assert path in _diff_files(data, "falcon")
    falcon_tab = next(
        t for t in data["review_checklist"]["tabs"] if t["platform"] == "falcon"
    )
    assert path in falcon_tab["changed_files"]
    assert world.package() == data


def test_2a1_wins_over_4a1_when_both_apply(world: World):
    world.use(branches=_branch_with_missing_revision(), builds=[])

    data = world.assemble().json()["data"]

    assert data["status"] == "In preparation"
    assert data["preselected_build"] is None


# --- Extension 4a1: no matching Jenkins Build ------------------------------------


def test_4a1_no_matching_build_is_pending_build_validation(world: World):
    world.use(
        builds=[b for b in fixtures.jenkins_builds() if b.branch_parameter == "trunk"]
    )

    response = world.assemble()

    assert response.status_code == 200
    data = response.json()["data"]
    assert data["status"] == "Pending build validation"
    assert data["jenkins_builds"] == []
    assert data["preselected_build"] is None
    assert data["jenkins_evidence"] == "available"
    assert world.jenkins.calls == ["find_builds"]


# --- SVN and Jenkins unavailable (SI-svn-read, SI-jenkins-read, 8.2.1) -----------


@pytest.mark.parametrize("method", ["find_branches", "changed_files"])
def test_svn_unavailable_is_503_and_recorded_unavailable(world: World, method: str):
    world.use(svn_fails_on=[method])

    response = world.assemble()

    assert response.status_code == 503
    assert response.json()["error"]["code"] == "SVN_UNAVAILABLE"
    assert response.json()["error"]["source"] == "SVN"
    data = world.package()
    assert data["status"] == "In preparation"
    assert data["svn_evidence"] == "unavailable"
    assert data["jenkins_evidence"] is None
    assert data["diffs"] == []
    assert world.jenkins.calls == []


def test_jenkins_unavailable_is_503_and_recorded_unavailable(world: World):
    world.use(jenkins_fails_on=["find_builds"])

    response = world.assemble()

    assert response.status_code == 503
    assert response.json()["error"]["code"] == "JENKINS_UNAVAILABLE"
    assert response.json()["error"]["source"] == "Jenkins"
    data = world.package()
    assert data["status"] == "In preparation"
    assert data["status"] != "Pending build validation"
    assert data["jenkins_evidence"] == "unavailable"
    assert data["svn_evidence"] == "available"
    assert data["diffs"] == []
    assert data["preselected_build"] is None


def test_rerun_after_an_outage_overwrites_the_unavailable_evidence(world: World):
    world.use(jenkins_fails_on=["find_builds"])
    assert world.assemble().status_code == 503

    world.use()
    response = world.assemble()

    assert response.status_code == 200
    assert response.json()["data"]["status"] == "Materials assembled"
    assert world.package()["jenkins_evidence"] == "available"


def _assert_no_materials_and_svn_available(data: dict[str, Any]) -> None:
    assert data["status"] == "In preparation"
    assert data["svn_branch"] is None
    assert data["svn_evidence"] == "available"
    assert data["jenkins_evidence"] is None
    assert data["diffs"] == []
    assert data["jenkins_builds"] == []
    assert data["preselected_build"] is None
    assert data["review_checklist"] is None
    assert data["review_record"] is None
    assert data["missing"] == []


def test_rerun_after_an_outage_that_hits_409_keeps_no_stale_evidence(world: World):
    world.use(svn_fails_on=["changed_files"])
    assert world.assemble().status_code == 503
    assert world.package()["svn_evidence"] == "unavailable"

    world.use(branches={"SYN-1-timer-fix": []})
    response = world.assemble()

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "ASSEMBLY_INCOMPLETE"
    _assert_no_materials_and_svn_available(world.package())


def test_rerun_after_2a1_that_hits_409_keeps_no_stale_materials(world: World):
    world.use(branches=_branch_with_missing_revision())
    assert world.assemble().json()["data"]["diffs"] != []

    world.use(branches={"OTHER-2-docs": []})
    response = world.assemble()

    assert response.status_code == 409
    _assert_no_materials_and_svn_available(world.package())


# --- Nothing to assemble, through the API ----------------------------------------


def test_assembly_incomplete_answers_in_the_envelope(world: World):
    world.use(branches={"OTHER-2-docs": []})

    response = world.assemble()

    assert response.status_code == 409
    error = response.json()["error"]
    assert error["code"] == "ASSEMBLY_INCOMPLETE"
    assert "No SVN Branch" in error["message"]
    assert error["source"] is None
    assert world.package()["status"] == "In preparation"


# --- PRE-1 and unknown packages --------------------------------------------------


def test_pre1_second_assembly_of_an_assembled_package_is_refused(world: World):
    assert world.assemble().status_code == 200

    response = world.assemble()

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "REVIEW_PACKAGE_NOT_IN_PREPARATION"
    assert world.package()["status"] == "Materials assembled"


def test_pre1_package_pending_build_validation_is_refused(world: World):
    world.use(builds=[])
    assert world.assemble().json()["data"]["status"] == "Pending build validation"

    response = world.assemble()

    assert response.status_code == 409
    assert response.json()["error"]["code"] == "REVIEW_PACKAGE_NOT_IN_PREPARATION"


@pytest.mark.parametrize(
    ("method", "path"),
    [
        ("post", "/api/v1/review-packages/rev-9999/assembly"),
        ("get", "/api/v1/review-packages/rev-9999"),
    ],
)
def test_unknown_package_is_not_found(world: World, method: str, path: str):
    response = world.client.request(method.upper(), path)

    assert response.status_code == 404
    assert response.json()["error"]["code"] == "REVIEW_PACKAGE_NOT_FOUND"
    assert world.svn.calls == []


# --- Logging (8.2.7) and the default wiring --------------------------------------


def test_assembly_logs_one_line_without_diff_content(
    world: World, caplog: pytest.LogCaptureFixture
):
    with caplog.at_level(logging.INFO, logger="app.rev.assembly"):
        world.assemble()

    lines = [r.getMessage() for r in caplog.records if r.name == "app.rev.assembly"]
    assert lines == [
        "assembly review_id='rev-0001' outcome=Materials assembled code=None"
    ]
    assert "SYNTHETIC_TIMEOUT" not in caplog.text


def test_the_application_serves_the_seeded_fixture_package():
    response = TestClient(app).get(PACKAGE)

    assert response.status_code == 200
    assert response.json()["data"]["jira_ticket_key"] == fixtures.JIRA_TICKET_KEY
