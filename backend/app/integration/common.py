"""What every Integration Gateway adapter shares."""

import re


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
