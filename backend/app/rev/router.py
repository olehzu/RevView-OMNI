"""Review package endpoints for UC-REV-assemble-materials (design/rev.md, API contract).

The router validates the request shape and nothing else. v0.1.0 has no authentication
(``SEC-authenticated-access`` is deferred), so it must run on a developer's machine only.
"""

from typing import Annotated, Any

from fastapi import APIRouter, Depends

from app.integration.jenkins import FakeJenkinsAdapter, JenkinsAdapter
from app.integration.svn import FakeSvnAdapter, SvnAdapter
from app.rev import fixtures
from app.rev.assembly import AssemblyService, ReviewPackageNotFound
from app.rev.models import ReviewPackage
from app.rev.repository import ReviewPackageRepository

# Seeded at startup, because UC-REV-create-review is not built yet.
_repository = ReviewPackageRepository()
_repository.save(fixtures.review_package())


def get_repository() -> ReviewPackageRepository:
    return _repository


def get_svn_adapter() -> SvnAdapter:
    return FakeSvnAdapter(branches=fixtures.svn_branches())


def get_jenkins_adapter() -> JenkinsAdapter:
    return FakeJenkinsAdapter(builds=fixtures.jenkins_builds())


Repository = Annotated[ReviewPackageRepository, Depends(get_repository)]

router = APIRouter(prefix="/api/v1/review-packages")


def _envelope(package: ReviewPackage) -> dict[str, Any]:
    return {"data": package.model_dump(mode="json")}


@router.post("/{review_id}/assembly")
def assemble_materials(
    review_id: str,
    repository: Repository,
    svn: Annotated[SvnAdapter, Depends(get_svn_adapter)],
    jenkins: Annotated[JenkinsAdapter, Depends(get_jenkins_adapter)],
) -> dict[str, Any]:
    """Assemble the review materials for a package in "In preparation"."""
    return _envelope(AssemblyService(repository, svn, jenkins).assemble(review_id))


@router.get("/{review_id}")
def get_review_package(review_id: str, repository: Repository) -> dict[str, Any]:
    """The stored review package."""
    package = repository.get(review_id)
    if package is None:
        raise ReviewPackageNotFound()
    return _envelope(package)
