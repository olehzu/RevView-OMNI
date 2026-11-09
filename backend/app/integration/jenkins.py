"""Jenkins adapter interface and its Synthetic Data fake.

Read only: there is no method that starts a build. When no build matches, the author
is prompted to run one (``OI-35``, design/rev.md).
"""

from collections.abc import Collection, Sequence
from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol

from app.integration.common import IntegrationUnavailable, contains_ticket_key


@dataclass(frozen=True)
class JenkinsBuild:
    """One Jenkins Build, as Jenkins reports it."""

    build_number: int
    name: str
    description: str
    branch_parameter: str
    """The build's branch-name parameter, compared with the SVN Branch."""
    result: str
    built_at: datetime
    """When Jenkins built it, timezone-aware UTC."""


class JenkinsAdapter(Protocol):
    def find_builds(self, ticket_key: str, branch: str) -> list[JenkinsBuild]:
        """Builds whose name or description contains the Jira Ticket key and whose
        branch-name parameter equals the SVN Branch, in any order."""
        ...


@dataclass
class FakeJenkinsAdapter:
    """Answers from Synthetic Data (``CO-sandbox-development``, section 8.2.10).

    Every method named in ``fail_on`` raises ``IntegrationUnavailable("Jenkins")``.
    ``calls`` records each method called.
    """

    builds: Sequence[JenkinsBuild]
    fail_on: Collection[str] = ()
    calls: list[str] = field(default_factory=list)

    def find_builds(self, ticket_key: str, branch: str) -> list[JenkinsBuild]:
        self.calls.append("find_builds")
        if "find_builds" in self.fail_on:
            raise IntegrationUnavailable("Jenkins")
        return [
            build
            for build in self.builds
            if build.branch_parameter == branch
            and (
                contains_ticket_key(build.name, ticket_key)
                or contains_ticket_key(build.description, ticket_key)
            )
        ]
