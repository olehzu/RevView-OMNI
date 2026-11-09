"""The Review Package and the review materials assembly attaches to it (design/rev.md).

Field names and values are the API contract: snake_case names, the use case's status
strings exactly, and lowercase Platform and Category spelled as the path segment.
"""

from datetime import datetime
from enum import StrEnum
from typing import Literal

from pydantic import BaseModel


class ReviewPackageStatus(StrEnum):
    IN_PREPARATION = "In preparation"
    MATERIALS_ASSEMBLED = "Materials assembled"
    PENDING_BUILD_VALIDATION = "Pending build validation"


class Evidence(StrEnum):
    """Whether an external system answered. ``None`` on a package means not fetched yet."""

    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"


class Platform(StrEnum):
    COMMON = "common"
    FALCON = "falcon"
    PHOENIX = "phoenix"


class Category(StrEnum):
    """The Code/Tools/Tests Category."""

    CODE = "code"
    TOOLS = "tools"
    TESTS = "tests"


class ChangedFile(BaseModel):
    path: str
    revision: str | None
    repository_link: str


class Diff(BaseModel):
    """One Diff per Platform x Category the change touches (``BR-review-nine-parts``)."""

    platform: Platform
    category: Category
    diff: str
    changed_files: list[ChangedFile]


class JenkinsBuild(BaseModel):
    build_number: int
    name: str
    result: str
    built_at: datetime
    """UTC, serialized as ISO 8601 with ``Z``."""


class ReviewChecklistTab(BaseModel):
    platform: Platform
    changed_files: list[str]


class ReviewChecklist(BaseModel):
    tabs: list[ReviewChecklistTab]


class ReviewRecord(BaseModel):
    id: str
    review_id: str
    jira_ticket_key: str


class MissingMaterial(BaseModel):
    """A gap flagged for the author (extension 2a1, POST-2)."""

    path: str
    missing: Literal["revision"]


class ReviewPackage(BaseModel):
    review_id: str
    status: ReviewPackageStatus
    jira_ticket_key: str
    svn_branch: str | None = None
    svn_evidence: Evidence | None = None
    jenkins_evidence: Evidence | None = None
    diffs: list[Diff] = []
    jenkins_builds: list[JenkinsBuild] = []
    """Newest first."""
    preselected_build: int | None = None
    review_checklist: ReviewChecklist | None = None
    review_record: ReviewRecord | None = None
    missing: list[MissingMaterial] = []
