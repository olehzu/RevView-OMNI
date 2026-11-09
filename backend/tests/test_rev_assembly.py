"""Unit tests for UC-REV-assemble-materials: step 3 (classify) and the gaps that leave
nothing to assemble (design/rev.md, Tests)."""

from collections.abc import Sequence

import pytest

from app.integration.jenkins import FakeJenkinsAdapter
from app.integration.svn import FakeSvnAdapter, SvnChangedFile
from app.rev import fixtures
from app.rev.assembly import (
    AssemblyIncomplete,
    AssemblyService,
    UnclassifiablePath,
    classify,
)
from app.rev.models import Category, Platform, ReviewPackageStatus
from app.rev.repository import ReviewPackageRepository


@pytest.mark.parametrize("platform", list(Platform))
@pytest.mark.parametrize("category", list(Category))
def test_classify_maps_every_platform_and_category_from_the_path(
    platform: Platform, category: Category
):
    path = f"{category}/{platform}/branches/SYN-1-timer-fix/src/file.c"

    assert classify(path) == (platform, category)


def test_classify_tools_common_example_from_the_design():
    path = "tools/common/branches/SYN-1-timer-fix/src/timer.py"

    assert classify(path) == (Platform.COMMON, Category.TOOLS)


@pytest.mark.parametrize(
    "path",
    [
        "docs/common/branches/SYN-1-timer-fix/readme.txt",  # unknown category
        "code/apollo/branches/SYN-1-timer-fix/main.c",  # unknown platform
        "code/falcon/trunk/SYN-1-timer-fix/main.c",  # not a branch
        "Code/falcon/branches/SYN-1-timer-fix/main.c",  # case differs from the segment
        "code/falcon/branches/SYN-1-timer-fix",  # no file under the branch
        "code/falcon/branches//main.c",  # no branch name
        "main.c",
    ],
)
def test_classify_refuses_a_path_outside_the_pattern(path: str):
    with pytest.raises(UnclassifiablePath):
        classify(path)


def _service(
    branches: dict[str, Sequence[SvnChangedFile]],
) -> tuple[AssemblyService, ReviewPackageRepository, FakeJenkinsAdapter]:
    repository = ReviewPackageRepository()
    repository.save(fixtures.review_package())
    jenkins = FakeJenkinsAdapter(builds=fixtures.jenkins_builds())
    service = AssemblyService(repository, FakeSvnAdapter(branches=branches), jenkins)
    return service, repository, jenkins


def _assert_refused_with_nothing_stored(
    service: AssemblyService, repository: ReviewPackageRepository, gap: str
) -> None:
    with pytest.raises(AssemblyIncomplete) as raised:
        service.assemble(fixtures.REVIEW_ID)

    assert raised.value.status_code == 409
    assert raised.value.code == "ASSEMBLY_INCOMPLETE"
    assert gap in raised.value.message
    assert repository.get(fixtures.REVIEW_ID) == fixtures.review_package()


def test_no_matching_svn_branch_is_assembly_incomplete():
    service, repository, jenkins = _service({"OTHER-2-docs": [], "SYN-10-x": []})

    _assert_refused_with_nothing_stored(service, repository, "No SVN Branch")
    assert jenkins.calls == []


def test_several_matching_svn_branches_is_assembly_incomplete_naming_them():
    service, repository, _ = _service({"SYN-1-a": [], "SYN-1-b": []})

    _assert_refused_with_nothing_stored(service, repository, "SYN-1-a, SYN-1-b")


def test_a_branch_with_no_changed_files_is_assembly_incomplete():
    service, repository, _ = _service({"SYN-1-timer-fix": []})

    _assert_refused_with_nothing_stored(service, repository, "no Changed Files")


def test_an_unclassifiable_path_is_assembly_incomplete_naming_the_path():
    path = "docs/common/branches/SYN-1-timer-fix/readme.txt"
    service, repository, _ = _service(
        {
            "SYN-1-timer-fix": [
                fixtures.changed_file(
                    "code/falcon/branches/SYN-1-timer-fix/src/scheduler.c"
                ),
                fixtures.changed_file(path),
            ]
        }
    )

    _assert_refused_with_nothing_stored(service, repository, path)


def test_the_fixture_assembles_one_diff_per_platform_and_category_touched():
    service, _, _ = _service(fixtures.svn_branches())

    package = service.assemble(fixtures.REVIEW_ID)

    assert package.status == ReviewPackageStatus.MATERIALS_ASSEMBLED
    assert [(d.platform, d.category) for d in package.diffs] == [
        (Platform.COMMON, Category.TOOLS),
        (Platform.FALCON, Category.CODE),
        (Platform.FALCON, Category.TESTS),
    ]
