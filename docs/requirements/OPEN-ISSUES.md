# Open Issues

**Project:** RevView/OMNI
**Team:** Team 8

---

_**What this file is.** Every question about the project that you cannot answer yet, in one place, with the name of the person who can answer it. It is the shortest document in `docs/requirements/` and the one your client meetings run on._

_**Why it exists.** A draft specification with confident guesses in the gaps is more dangerous than one with holes in it, because nobody can tell the guesses from the facts. Writing "we do not know" is not an admission of failure in week 3, it is the correct state. What fails is knowing and not writing it down._

_**Where entries come from.** Three places, and all three are routine:_

- _Drafting a section of [vision-and-scope.md](vision-and-scope.md) and hitting something the client brief does not say._
- _Your agent's list. When you ask it to draft a section, ask it to list every question it could not answer from the material you gave it. Its list is longer than yours and it is not embarrassed to ask obvious things._
- _The meeting itself. Your client says something that contradicts your notes, or answers a question with "I would have to check"._

_**How they leave.** Answered in a client meeting, in Slack, or by reading a document. Record the answer and the date, mark it resolved, and put the substance where it belongs (an objective, a term in the [glossary](project-glossary.md), a business rule). This file is a queue, not a home: an answer that stays here has not been filed._

_**Identifiers here are numbers**, `OI-1` upward, and that is deliberate. Numbers are fine for a list that only ever grows at the bottom and gets cited lightly. The slug convention in [vision-and-scope.md](vision-and-scope.md) exists for identifiers that get **reordered** or **cited often**, which is not this list._

## Before a client meeting

_[Sort the open list by what it costs you to stay wrong, not by what is easy to ask. You will get through fewer questions than you plan to. Take the ones where a wrong guess sends the whole team down the wrong path for a month, and leave the ones you can settle by reading a document or trying the client's current tool yourself.]_

_[Send the shortlist to your client the day before. A client who has seen the questions arrives with answers instead of promises.]_

## Open

| ID | Question | Why it matters | Who can answer | Raised |
|---|---|---|---|---|
| OI-3 | Can Sumalee walk the team through one complete, recent review end to end, including a case where it went wrong or got stuck? | She began a live walkthrough in meeting 1 (Excel spreadsheet, SVN links) but stopped after about 10 minutes without finishing. A full pass, and a "went wrong" story, are where the real requirements and business rules hide. | Sumalee Rodolph | 2026-09-09 |
| OI-5 | How many reviews happen per week or month, and how big is the largest change ever reviewed? | We know 5 to 6 developers use the process daily and there are 6 reviews in progress right now (as of 2026-09-18), but not the ongoing rate or the size of the largest diff, both of which drive the SVN diff and build design. | Sumalee Rodolph | 2026-09-09 |
| OI-7 | Who owns AppliedAvionics' production Jira, SVN, and Jenkins, and is there documentation for how the sandbox should mirror them? | The client's project concept document lays out the sandbox shape (Atlassian free-tier Jira, self-hosted SVN and Jenkins, isolated from AppliedAvionics' network), and a sample Jira was promised for about 2026-09-25, but no named system owner or formal documentation has been provided yet. | Sumalee Rodolph | 2026-09-09 |
| OI-9 | Are there other AppliedAvionics stakeholders (for example engineering management, IT/security) the team should meet or get sign-off from? | Not raised in either meeting so far. A stakeholder with a veto discovered late is expensive to accommodate. | Sumalee Rodolph | 2026-09-09 |
| OI-10 | What is the agreed meeting cadence, and when and where is meeting 3? | Contact channel is confirmed (Microsoft Teams direct messages, fast turnaround), but no explicit cadence has been agreed and meeting 3's date, time, and place are not yet on the calendar. | Sumalee Rodolph | 2026-09-09 |
| OI-11 | Is there anything about the process or project we have not asked about that worries Sumalee? | The guide's catch-all question has not been asked in either meeting yet, and it is called out as the highest-yield question in the guide. | Sumalee Rodolph | 2026-09-09 |
| OI-12 | When exactly will the example/sample Jira setup be ready, and does it cover what the sandbox needs? | Promised during meeting 2 for "next week" (around 2026-09-25); needed to validate the sandbox Jira structure against something concrete before integration work starts on it. | Sumalee Rodolph | 2026-09-18 |

## Resolved

| ID | Question | Answer | Answered by | Date | Filed in |
|---|---|---|---|---|---|
| OI-2 | What does the current review process cost in time today, so we have a baseline for `BO-review-centralization`? | About 20 minutes per review to gather forms and fill in fields, not counting Jenkins build time. | Sumalee Rodolph | 2026-09-09 | `BO-review-centralization`, vision-and-scope.md section 2.3 (not yet drafted) |
| OI-4 | What about the current process works well and should not change? | Do not change the underlying review process or the existing tools (SVN, Jira, Jenkins, the review record); the app should only make the existing process faster to run. Review records and checklists must still export in the same Excel/CSV format used today. | Sumalee Rodolph | 2026-09-09 | vision-and-scope.md sections 2.7 and 4 (not yet drafted) |
| OI-6 | Can the team talk to or observe an actual review author or reviewer, not only Sumalee? | No, not at this time. Sumalee is the team's only point of contact at AppliedAvionics for now. | Sumalee Rodolph | 2026-09-09 | `RI-proxy-only-contact`, vision-and-scope.md section 2.6 (not yet drafted) |
| OI-8 | Who maintains this system after the team graduates, and what do they already run? | Sumalee will maintain it herself. Expect to need about one person available for roughly a year after handoff for any issues; after that, support needs should drop off. | Sumalee Rodolph | 2026-09-18 | vision-and-scope.md section 4.4 (not yet drafted) |
