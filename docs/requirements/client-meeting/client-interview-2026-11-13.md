# Client Interview Guide

**Project:** RevView/OMNI
**Team:** Team 8
**Client:** Sumalee Rodolph, AppliedAvionics
**Meeting:** 5 of several

---

_**What this file is.** Your script going in, your meeting record coming out. Copy it once per meeting into `docs/requirements/` as `client-interview-YYYY-MM-DD.md` and commit it the same day._

_**How to use it.** Each section says what it is for, what it is worth in minutes, and whether it must happen in this meeting. Write the answers underneath in **their** words rather than yours._

## Before you go

- [x] **Three roles assigned.** Lead asks and moves the agenda, one person not four. Scribe writes and does not ask, capturing exact words, especially nouns. Observer watches what is not said. _[Oleh Zubariev was both lead and scribe; no observer recorded. Answers below are from the lead's notes, so they are closer to paraphrase than usual.]_
- [x] **Everyone has read the client's pitch slides** and written questions individually before you merged them.
- [ ] **Shortlist sent to the client the day before.** _[The agenda was a demo of `UC-REV-assemble-materials`, `OI-39` (the display time zone), and the team's plan for sandbox SVN, Jira, and Jenkins. Whether it was sent ahead is not recorded.]_
- [x] **This file open on the scribe's laptop.**
- [ ] **Someone owns the clock.**

## Meeting record

| | |
|---|---|
| **Date** | 2026-11-13 |
| **Time and location** | Microsoft Teams; time not recorded |
| **Client participants** | Sumalee Rodolph (AppliedAvionics) |
| **Team participants** | Oleh Zubariev (lead and scribe), Ralph Castilleja, Francisco Lugo Gonzales, Valerie Valles, Cong Quoc Le, Ethan Nguyen |
| **Recording** | None recorded. Answers below come from the lead's notes. |
| **Photos of screens or forms** | Three screenshots of a prototype Sumalee built herself, described in section 6. The screenshots are not committed, and this record leaves out the ticket numbers, ticket titles, people's names, and file paths they show, because the repository may be public. |

_This meeting opened with a demo, then took one open question and the team's plan for the sandbox, and ended with Sumalee showing her own prototype._

---

# Opening

## 1. Get to know your client

_**Must ask. 5 min.**_

**What they said:** Not covered this meeting.

---

# The business

## 2. Context and domain

_**Must ask. 5 min.** Every term you do not recognize goes in the glossary before you leave._

**What they said:** No new terms recorded. The prototype in section 6 uses "Task", "Owner", "Collaborators", "Class", and "Priority"; whether any of these is a RevView/OMNI term is an open question (see Open questions), so none goes in the glossary yet.

## 3. Business drivers and objectives

_**Must ask. 5 min.**_

**What they said:** Not covered this meeting.

---

# The process

## 4. How it works today

_**Must ask. 10 min.** Ask them to show you rather than tell you._

**What they said:** Not covered this meeting.

**What we showed her:** The review package page for `UC-REV-assemble-materials` (issue #51) against the v0.1.0 API, on Synthetic Data with fake SVN and Jenkins adapters: loading review package `rev-0001`, assembling it, and the result: the SVN Branch, the Diffs grouped by Platform and Category with their Changed Files, Revisions, and repository links, the Jenkins Builds with the most recent preselected, and the Review Checklist with one tab per Platform. Sumalee liked the demo and expects the team to have developed more by the next meeting.

## 5. What is hard about it

_**Must ask. 5 min.** Listen for "must", "unless", "only", and "except"._

**What they said:** Not covered this meeting.

## 6. What already works

_**Must ask. 3 min.**_

**What they said:** Sumalee showed screenshots of a prototype she built herself with AI assistance ("vibecoded") and said the team should try to emulate something like it.

**Artifacts they showed us:** three screens of the prototype, a static web page opened from her machine. Most field values are placeholders from a generic template (class names such as "Mathematics" and "Science", school-style task names).

- **Task Dashboard.** A header with "+ New Task" and "Logout". A filter bar: owner, class, date, status, and "Clear Filters". A row of cards, one per ticket, each with the ticket key (`TKT-…`), a title, Owner, Class, Status (seen: New, In Progress, Completed, Blocked), and the number of Collaborators. Selecting a card opens a detail panel with the key, title, Owner, Collaborators, Class, Status, Priority, Assigned To, Start Date, Due Date, Description, and a green "Review" button.
- **Create New Task: Select Existing Ticket.** "Select a ticket from the available list": a search box, a list of tickets with radio buttons, and the buttons "Enter Manually" and "Next".
- **Create New Task: Information Retrieved.** The fields filled in from the chosen ticket (Name, Class, Assigned To, Status, Priority, Start Date, Due Date), and the buttons "Review/Edit Information" and "Create Task".

## 7. Volumes and scale

_**Must ask. 3 min.**_

**What they said:** Not covered this meeting.

## 8. Who the users are

_**Must ask. 4 min.**_

**What they said:** Not covered this meeting.

---

# The boundaries

## 9. Constraints and rules

_**Must ask. 4 min.**_

**What they said:**

- **Time zone (`OI-39`):** only the central time zone matters. _Team reading, to confirm only if it ever matters: US Central Time, including daylight saving (`America/Chicago`), as the one organization time zone of architecture section 8.2.2._

## 10. External dependencies

_**Must ask. 3 min.**_

**What they said:** The team said it will set up sandbox SVN, Jira, and Jenkins of its own, filled with Synthetic Data, before the next meeting. Sumalee said that is OK.

## 11. Lifetime and who maintains it

_**Must ask. 2 min.**_

**What they said:** Not covered this meeting.

## 12. Other stakeholders

_**If there is time. 1 min.**_

**What they said:** Not covered this meeting.

---

# The close

## 13. Anything else

_**Must ask. 1 min.**_

**What they said:** The prototype in section 6.

## 14. The read-back

_**Never skip. 5 min.**_

**What we read back, and what they corrected:** Not recorded.

## 15. Before you leave the room

_**Never skip. 4 min.**_

- [x] **Next meeting on the calendar.** _[Friday 2026-11-20. The team committed to the sandbox and to more development before it.]_
- [ ] **Cadence agreed.** _[Not recorded.]_
- [x] **Contact channel and how fast they reply.** _[Microsoft Teams group chat, as before.]_
- [ ] **Who to contact between meetings.** _[Sumalee Rodolph; no alternate recorded.]_
- [ ] **Copies requested** of every artifact you were shown. _[The prototype screenshots were shared with the team. The checklist template files offered on 2026-10-09 (`OI-36`) are not recorded as received.]_
- [ ] **Introductions requested.** _[None.]_
- [x] **Say what happens next.** _[The sandbox SVN, Jira, and Jenkins, and more development, before the next meeting on 2026-11-20.]_

---

# After the meeting

_File everything within 24 hours, while you still remember why each answer mattered. This file is a record, not a home._

## Initial ideas

_[Solutions anyone floated, yours or theirs. Record them here and nowhere else yet.]_

- **The team's sandbox plan:** run small SVN and Jenkins instances of its own (`DE-sandbox-self-hosted-svn-jenkins`) and a Jira of its own, filled with Synthetic Data shaped like what Sumalee has shown; make the parts the team cannot know (repository layout, branch naming, Jenkins job and parameter names) settings she can change at handoff; and give her a read-only connection check to run inside her network. Only "we will set up the sandbox" was put to her; the settings and the connection check were not discussed.
- **Sumalee's prototype as a model.** Sumalee expects RevView/OMNI to follow the prototype's flow: the Author starts from a dashboard of ticket tiles, selects a tile to see its details, and starts the review from there ("Review"), creating it from an existing ticket picked from a searchable list, or entered manually, and then checking the retrieved information before creating it. _Confirmed by Oleh Zubariev (lead and scribe) on 2026-11-25 from the screenshots._ This maps onto `UC-REV-create-review`, which today starts from ticket selection and has no dashboard step, so the use case needs one.

## Disagreements and hesitations

No observer was recorded.

- **"Emulate something like what she did"** means the tile dashboard and its flow (dashboard, then select a ticket, then create and review), as above. It does not settle the fields shown on each tile or in the details (next bullet).
- **The prototype's fields and statuses** (Class, Priority, Collaborators, Start and Due Date; New, In Progress, Completed, Blocked) do not match RevView/OMNI's vocabulary or the review package statuses ("In preparation", "Materials assembled", "Pending build validation"). Many look like template placeholders.
- **A Jira of our own** is not in the specification: `DE-sandbox-self-hosted-svn-jenkins` covers SVN and Jenkins only, and Jira cannot be self-hosted for free. The team still has to agree how (for example a free Atlassian Cloud site), per the charter.

## Open questions

_[Copy each into [OPEN-ISSUES.md](../OPEN-ISSUES.md) as an `OI-*` with the person who can answer it.]_

- `OI-39` (answered): the central time zone only.
- New, to file: **Which filters does the ticket dashboard need (the prototype shows owner, class, date, and status), and which tickets does it list: every open ticket, or only the Author's?** Sumalee Rodolph. Needed before the dashboard step of `UC-REV-create-review` is designed.
- New, to file: **Which of the prototype's fields and statuses are real** (Owner, Collaborators, Class, Priority, Assigned To, Start and Due Date; New, In Progress, Completed, Blocked), and which are template placeholders? Sumalee Rodolph. Only needed when the use case that shows them is designed.
- Not asked: Jira, SVN, and Jenkins types, versions, and how each logs in; whether the shape she has shown (for example `tools/shared/branches/TKT-…`) is close enough to build the Synthetic Data against; the checklist template files (`OI-36`).

**Requirements this changes (impact list needed):**

- `OI-39`: architecture section 8.2.2 (the configured organization time zone is Central); `design/rev.md`, where the review package page shows build times in UTC until the zone is known.
- The sandbox: `DE-sandbox-self-hosted-svn-jenkins` and `CO-sandbox-development` (a Jira of the team's own); `RISK-sandbox-integration-unproven` (the plan for retiring it).
- The prototype: `UC-REV-create-review` gains a first step, the ticket tile dashboard, and an extension for entering a ticket manually; its design (`design/rev.md`, PR #62) follows. The tile and detail fields wait for the questions above.

---

_**Within 24 hours**, send the client your notes and the open questions. Then commit this file._
