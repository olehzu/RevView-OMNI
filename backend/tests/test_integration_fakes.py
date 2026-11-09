"""The Integration Gateway's adapter interfaces and their Synthetic Data fakes."""

from datetime import UTC, datetime

import pytest

from app.integration.common import IntegrationUnavailable, contains_ticket_key
from app.integration.jenkins import FakeJenkinsAdapter, JenkinsAdapter, JenkinsBuild
from app.integration.svn import FakeSvnAdapter, SvnChangedFile


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        ("SYN-1-timer-fix", True),
        ("SYN-1", True),
        ("fix-SYN-1", True),
        ("SYN-10-cleanup", False),
        ("syn-1-timer-fix", False),
        ("ASYN-1-refactor", False),
        ("7SYN-1-refactor", False),
        ("fix_SYN-1", True),
        ("SYN-2-other", False),
    ],
)
def test_ticket_key_match_is_case_sensitive_and_not_followed_by_a_digit(
    text: str, expected: bool
):
    assert contains_ticket_key(text, "SYN-1") is expected


def _file(path: str) -> SvnChangedFile:
    return SvnChangedFile(path=path, revision="1", repository_link="link", diff="d")


def test_svn_fake_finds_only_branches_matching_the_ticket_key():
    svn = FakeSvnAdapter(
        branches={
            "SYN-1-timer-fix": [],
            "SYN-10-cleanup": [],
            "ASYN-1-refactor": [],
            "OTHER-2": [],
        }
    )

    assert svn.find_branches("SYN-1") == ["SYN-1-timer-fix"]


def test_svn_fake_returns_the_branch_files():
    files = [_file("tools/common/branches/SYN-1-timer-fix/src/timer.py")]
    svn = FakeSvnAdapter(branches={"SYN-1-timer-fix": files})

    assert svn.changed_files("SYN-1-timer-fix") == files
    assert svn.calls == ["changed_files"]


@pytest.mark.parametrize("method", ["find_branches", "changed_files"])
def test_svn_fake_outage_raises_unavailable_naming_svn(method: str):
    call = getattr(FakeSvnAdapter(branches={}, fail_on={method}), method)

    with pytest.raises(IntegrationUnavailable) as raised:
        call("SYN-1")

    assert raised.value.source == "SVN"


def _build(number: int, name: str, branch: str, description: str = "") -> JenkinsBuild:
    return JenkinsBuild(
        build_number=number,
        name=name,
        description=description,
        branch_parameter=branch,
        result="SUCCESS",
        built_at=datetime(2026, 11, 5, tzinfo=UTC),
    )


def test_jenkins_fake_matches_key_in_name_or_description_and_the_branch_parameter():
    jenkins = FakeJenkinsAdapter(
        builds=[
            _build(1, "SYN-1 timer fix", "SYN-1-timer-fix"),
            _build(2, "nightly", "SYN-1-timer-fix", description="for SYN-1"),
            _build(3, "SYN-1 timer fix", "trunk"),
            _build(4, "SYN-10 cleanup", "SYN-1-timer-fix"),
            _build(5, "ASYN-1 refactor", "SYN-1-timer-fix"),
            _build(6, "nightly", "SYN-1-timer-fix", description="for ASYN-1"),
        ]
    )

    found = jenkins.find_builds("SYN-1", "SYN-1-timer-fix")

    assert [build.build_number for build in found] == [1, 2]


def test_jenkins_fake_outage_raises_unavailable_naming_jenkins():
    jenkins = FakeJenkinsAdapter(builds=[], fail_on={"find_builds"})

    with pytest.raises(IntegrationUnavailable) as raised:
        jenkins.find_builds("SYN-1", "SYN-1-timer-fix")

    assert raised.value.source == "Jenkins"


def test_jenkins_adapter_is_read_only():
    """OI-35: the adapter can only find builds, never start one."""
    public = {name for name in vars(JenkinsAdapter) if not name.startswith("_")}

    assert public == {"find_builds"}
