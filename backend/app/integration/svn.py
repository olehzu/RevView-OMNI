"""SVN adapter interface, its Synthetic Data fake, and the error every adapter raises.

The real sandbox adapter replaces ``FakeSvnAdapter`` behind ``SvnAdapter`` (design/rev.md).
"""

import re
from collections.abc import Collection, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Protocol


class IntegrationUnavailable(Exception):
    """An external system did not answer. ``source`` names it, for example "SVN".

    Every adapter raises this, and only this, when its system fails, so the failure
    is reported as unavailable and never as empty or passing (section 8.2.1).
    """

    def __init__(self, source: str) -> None:
        super().__init__(f"{source} is unavailable")
        self.source = source


def contains_ticket_key(text: str, ticket_key: str) -> bool:
    """True when ``text`` contains the Jira Ticket key, case-sensitive, not followed by a digit.

    "SYN-1-timer-fix" contains "SYN-1"; "SYN-10-cleanup" does not (design/rev.md).
    """
    return re.search(re.escape(ticket_key) + r"(?!\d)", text) is not None


@dataclass(frozen=True)
class SvnChangedFile:
    """One Changed File on an SVN Branch, as SVN reports it."""

    path: str
    """Full repository path, ``<category>/<platform>/branches/<branch>/…``."""
    revision: str | None
    """The Revision, or ``None`` when SVN has none for the file (extension 2a)."""
    repository_link: str
    diff: str
    """The SVN-generated diff output for this file (``BR-svn-diff-required``)."""


class SvnAdapter(Protocol):
    def find_branches(self, ticket_key: str) -> list[str]:
        """Names of the SVN Branches whose name contains the Jira Ticket key."""
        ...

    def changed_files(self, branch: str) -> list[SvnChangedFile]:
        """Changed Files on the branch, across every ``<category>/<platform>/branches/<branch>`` root."""
        ...


@dataclass
class FakeSvnAdapter:
    """Answers from Synthetic Data (``CO-sandbox-development``, section 8.2.10).

    ``branches`` maps each SVN Branch name to its Changed Files. Every method named in
    ``fail_on`` raises ``IntegrationUnavailable("SVN")``, as an outage would. ``calls``
    records each method called, so a test can see what was asked.
    """

    branches: Mapping[str, Sequence[SvnChangedFile]]
    fail_on: Collection[str] = ()
    calls: list[str] = field(default_factory=list)

    def _answer(self, method: str) -> None:
        self.calls.append(method)
        if method in self.fail_on:
            raise IntegrationUnavailable("SVN")

    def find_branches(self, ticket_key: str) -> list[str]:
        self._answer("find_branches")
        return [name for name in self.branches if contains_ticket_key(name, ticket_key)]

    def changed_files(self, branch: str) -> list[SvnChangedFile]:
        self._answer("changed_files")
        return list(self.branches.get(branch, ()))
