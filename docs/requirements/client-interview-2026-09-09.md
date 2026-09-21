# Client Interview Guide

**Project:** RevView/OMNI
**Team:** Team 8
**Client:** Sumalee Rodolph, AppliedAvionics
**Meeting:** 1 of several

---

_**What this file is.** Your script going in, your meeting record coming out. Copy it once per meeting into `docs/requirements/` as `client-interview-YYYY-MM-DD.md` and commit it the same day._

_**How to use it.** Each section says what it is for, what it is worth in minutes, and whether it must happen in this meeting. The example questions are written for a different domain (technical recruiting) on purpose, so you cannot use them unchanged. Rewrite them in your client's words before you walk in, and write the answers underneath in **their** words rather than yours._

_**Work it with your agent.** Give it your one-page brief, this file **including these instructions**, and a role: "You are an experienced business analyst preparing for a first client interview. Using the question types in this guide, write the version of each question that fits this client's domain, and list every acronym in the brief you would want defined before the meeting." Then do the part it cannot: pick which of its questions are worth your client's limited hour. **Sort by what it costs you to stay wrong**, not by what is easy to ask. Anything you could answer by reading a document is not worth a client minute._

## Listen before you build

**An idea you propose in the first twenty minutes is not worth what it costs you.** Your strongest instinct will be to show your client you understood by describing what you would build. Early, that ends the elicitation: a client who has heard your idea reacts to it instead of describing their world.

This is about order, not silence. Some clients want to think out loud with you, and a few asked for the project because they want exactly that help. Do it **after** the read-back in section 14, when you can describe their process back to them accurately and the brainstorm is grounded in their world rather than your imagination. If they open by asking for your ideas, say you have some and would rather earn them by understanding the process first, then come back to it before you leave.

**The separate rule is absolute: commit to nothing.** Not a deadline, not a feature, not "sure, we can add that". Five teammates are not in the room. "Let me write that down and bring it back to the team" is the whole sentence, and it holds even when a client pushes.

## Before you go

- [x] **Three roles assigned.** Lead asks and moves the agenda, one person not four. Scribe writes and does not ask, capturing exact words, especially nouns. Observer watches what is not said: hesitation, the topic they keep returning to, who they defer to. _(This meeting: no dedicated observer, the whole team scribed.)_
- [x] **Everyone has read the client's pitch slides** (TCU Online) and written questions individually before you merged them. The ones two of you wrote independently are the ones to ask.
- [x] **Shortlist sent to the client the day before.** They arrive with answers instead of promises.
- [x] **This file open on the scribe's laptop**, with someone on paper as backup.
- [x] **Someone owns the clock.** You will not get through this guide, and that is expected.

## Meeting record

| | |
|---|---|
| **Date** | 2026-09-09 |
| **Time and location** | 1:00 PM, in person, Tucker Building, room 339 |
| **Client participants** | Sumalee Rodolph (AppliedAvionics) |
| **Team participants** | Oleh Zubariev (lead), Cong Quoc Le (scribe), Ethan Nguyen (scribe), Francisco Lugo Gonzaels (scribe), Ralph Castilleja (scribe), Valerie Valles (scribe) |
| **Recording** | Not asked |
| **Photos of screens or forms** | Not asked |

_Ask to record, and say why: so nobody is transcribing instead of listening. If they decline, the scribe matters more. Ask separately about photographing screens, forms, and reports. A photo of the spreadsheet they actually use beats a page of notes about it._

## The shape of the hour

Most first meetings run 60 to 90 minutes. Budget for the short one.

| Part | Sections | 60 min | 90 min |
|---|---|---|---|
| Opening | 1 | 5 | 5 |
| The business | 2, 3 | 10 | 15 |
| The process | 4, 5, 6, 7, 8 | 25 | 40 |
| The boundaries | 9, 10, 11, 12 | 10 | 15 |
| The close | 13, 14, 15 | 10 | 15 |

**Extra time goes into section 4 first.** It repays another ten minutes and it is the only section you cannot reconstruct from notes afterward.

"Can wait" means the next meeting, not never. When you are behind, drop from the middle. **Never drop 14 or 15:** the read-back is where you learn you misunderstood something, and the close is where you stop losing two weeks to scheduling.

---

# Opening

## 1. Get to know your client

_**Must ask. 5 min.** Not small talk. Whose problem is this, how much of the domain lives only in this person's head, and how much of their own time do they have for you? A client fitting this around a full job answers email slowly, and you want to know that in week 3 rather than week 9._

_Adapt: Tell me about being an HR manager. How did you choose that line of work? What do you most and least like about it? How does this project fit alongside the rest of your work?_

**What they said:** Sumalee is a recent TCU graduate, a data science major who moved into software development and joined AppliedAvionics right after finishing her own TCU senior design project not long ago. RevView/OMNI was her own proposal. She has significant time available for the project and said she is reachable through Microsoft Teams direct messages essentially any time.

---

# The business

## 2. Context and domain

_**Must ask. 5 min.** You are here for vocabulary as much as facts. Every term you do not recognize goes in the glossary before you leave. When your client says "cycle" in one sentence and "sprint" in the next, ask which they mean while they are still in front of you; an agent reading the transcript afterward cannot ask._

_Adapt: Give us some background on recruiting here. Why does it matter to the company? Who else is involved? Any documents, slides, or videos that would get us up to speed on the terminology? When you say [term], what does that cover?_

**What they said:** We signed the NDA with Sumalee and briefly discussed the project idea. The goal is to simplify and automate parts of AppliedAvionics' current avionics code review process while keeping human review and traceability in place.

**Terms for the glossary, in their words:** SVN (Subversion, their source control system), Jenkins (their build system), Jira (their issue-tracking system), all named as existing tools the new system must work alongside, not replace. No conflicting usage flagged yet. Confirmed against the client's written project concept document ("RevView/OMNI Review Helper Application Concept"), which uses the same three terms with no conflicting definitions.

## 3. Business drivers and objectives

_**Must ask. 5 min.** Why this, why now. These become your business objectives, so push for a number: when they name a benefit, ask the follow-up nobody asks, **what is that number today?**_

_Expect to miss it here. Baselines surface in section 4, when they are looking at the thing that takes the time. Ask the objective now, listen for the number all hour, and close the gap in the read-back._

_Adapt: Why did you propose this project? What is the main problem, or the opportunity? Who is affected, and who benefits? What happens if we do nothing? How will you know it worked, and what is that number today?_

**What they said:** The review process today is manual end to end, and Sumalee wants it centralized without losing the human judgment and traceability that avionics code review requires. A review currently takes about 20 minutes to gather forms and fill in fields, not counting Jenkins build time (the client's own estimate, consistent with how long her partial live walkthrough took in section 4 below).

**Candidate objectives (`BO-<slug>`), with baselines where you got them:** `BO-review-centralization`: reduce the manual, multi-tool effort of running a code review. Baseline: about 20 minutes per review today, excluding build time.

---

# The process

## 4. How it works today

_**Must ask. 10 min, the best ten in the meeting.** Ask them to show you rather than tell you. People describe the process they believe they follow; the spreadsheet shows the one they actually follow, and the gap is where the requirements hide. **"Show me" is the two most productive words in requirements engineering, and they cost nothing.**_

_Walk one real recent case end to end. "Take me through the last one you did" beats "how does it usually work", because the general shape is a summary they have given before and the last real one has the exceptions in it._

_Adapt: What are the steps in hiring a technical candidate? Could you show me your interview guide, and the notes from the last few? Who does what at each step? Where does it get stuck? What do you do when it goes wrong?_

**What they said:** Sumalee walked the team through part of a real review live rather than only describing it. She opened an Excel spreadsheet and began filling in names, descriptions, and links to the SVN revision, then paused to look for related files on her desktop. The walkthrough took about 10 minutes and she did not finish it, which on its own shows how much of the process is manual lookup and file hunting rather than judgment. A full end-to-end pass, and a story about a review that went wrong, are still needed; carried forward as `OI-3`. At a higher level, an author preparing a review must: (1) collect the applicable review checklist, (2) create a diff of the change, (3) fill out a review record by hand, (4) pull the relevant SVN information, (5) run a Jenkins build, and (6) notify the reviewer(s) directly. Jira tracks the associated work item throughout, but is not connected to the other tools.

**Artifacts they showed us:** Sumalee showed the team their SVN repository and the Jira and Jenkins environments on screen during the walkthrough. Nothing was photographed or copied (not asked). The client also provided a written project concept document ("RevView/OMNI Review Helper Application Concept") describing the same process and the intended application in detail.

## 5. What is hard about it

_**Must ask. 5 min.** The complaint is usually the requirement. Listen for "must", "unless", "only", and "except", which arrive unannounced in the middle of a story about something else. Those sentences are business rules, and they exist whether or not your software does._

_Adapt: What is the most frustrating part? Walk me through the last time it went badly. What takes longest? What do you have to redo? What do people get wrong? What do you check by hand because you do not trust the system?_

**What they said:** The process is fragmented across Jira, SVN, Jenkins, checklists, and review records kept separately, with no single place to see a review end to end. No specific worst-case story was collected this meeting; raised as `OI-3`.

**Rules heard (candidate `BR-*` for week 4):** A review is not considered complete without a filled-out review record, implying a rule that a review cannot close without documented reviewer sign-off. To be confirmed in a future meeting.

## 6. What already works

_**Must ask. 3 min.** Ask what is good before you propose replacing it. A team that removes something the client liked has lost trust it will not get back this semester, and nobody volunteers this unasked._

_Adapt: What would you keep exactly as it is? What would you miss if it disappeared? Has anything been tried before that did not work, and why?_

**What they said:** Sumalee was clear the team should not change the underlying review process or any of the existing software (SVN, Jira, Jenkins, the review record itself); the app should only make the existing process faster to run, not replace it. She also wants the review record and checklist to still be exportable in the same Excel/CSV format the company uses today, even though people will fill them out in the new app rather than in Excel directly.

## 7. Volumes and scale

_**Must ask. 3 min.** These numbers decide most of your architecture, and they are cheap to ask for and expensive to guess. Twenty records a semester and two hundred thousand a day are different systems._

_Adapt: How many of these in a week? A year? How many at the busiest moment, and when is that? How big is the largest one? How much history has to stay available? How many people use it at once on the worst day?_

**What they said:** Not covered in this meeting. Partially answered in meeting 2 (5 to 6 developers use the process daily, 6 reviews in progress as of 2026-09-18); see [client-interview-2026-09-18.md](client-interview-2026-09-18.md). Weekly or monthly review volume and the size of the largest change reviewed are still unknown, carried forward as `OI-5`.

## 8. Who the users are

_**Must ask. 4 min.** The person who commissions software is often not the person who uses it._

_**If you cannot reach the real users, that is a project risk, not a scheduling detail.** Record it as an `RI-<slug>` the same day. Building from a proxy's account is the most common way a capstone ships something nobody uses, and it is survivable only if you know you are doing it._

_Adapt: Who uses this day to day? How many? What do they use today? Can we talk to two or three, and watch one of them work? Will they test it before handover?_

**What they said:** The users are other developers at AppliedAvionics, the people familiar with the code and the review process (authors and reviewers). Sumalee confirmed the team cannot talk to anyone besides her for now. Meeting 2 added a rough count: 5 to 6 people are on the development team and would use the application daily.

**Can we reach real users? If not, why, and what is the risk:** No. Sumalee is the team's only point of contact at AppliedAvionics for the foreseeable future. Risk: requirements gathered only from Sumalee's account of the process may miss what reviewers and authors actually do day to day, tracked as `RI-proxy-only-contact`.

---

# The boundaries

## 9. Constraints and rules

_**Must ask. 4 min.** Nobody asks these in meeting 1 and everybody regrets it in November. A constraint restricts how you may build, and it is a requirement even though it describes no behavior. Ask directly; clients do not volunteer these, they assume you know._

_Adapt: Is there anything we are required to use, or forbidden from using? Does IT have to approve the technology, and how long does that take? Does this touch personal data, student records, health information, or payments? Any regulations or policies it has to satisfy? Any hard dates we do not know about? Is there a budget for hosting, and who signs off?_

**What they said:** The backend must be written in Python and the frontend in JavaScript. The team cannot access AppliedAvionics' production Jira, SVN, or Jenkins directly, since IT will not add students to the company network, so a sandbox environment running real but isolated Jira, SVN, and Jenkins instances, populated with mock data, stands in for them during development. The team's own GitHub can be used, including as a public repository. Real credentials for the production systems are handed over at project handoff. The MVP must be complete by the end of this semester.

## 10. External dependencies

_**Must ask. 3 min.** What your system has to talk to. Access credentials take weeks to obtain, so the ask has to happen now._

_Adapt: What other systems does this exchange data with, in which direction, in what format? Who owns them, and who do we ask for access? How long does that usually take? Is there documentation? What does the service cost, and who pays?_

**What they said:** The new system centralizes and integrates with Jira, SVN, and Jenkins. Because students cannot reach AppliedAvionics' real instances of these, the team will build and test against a sandbox environment: a free-tier Atlassian Jira instance and self-hosted SVN and Jenkins instances, all isolated from AppliedAvionics' network and populated with mock data that mirrors the real workflow (per the client's project concept document). A sample Jira setup was promised for the week of 2026-09-25 (meeting 2). Who owns the real production instances, and formal documentation for them, was still not discussed; carried forward as `OI-7`.

## 11. Lifetime and who maintains it

_**Must ask. 2 min.** The question students never ask and every client can answer. **Who runs this after we graduate, and what do they already know how to run?** It constrains your entire technology choice, so ask before you pick a stack rather than after._

_Adapt: How long should this keep running? Who supports it after we graduate from TCU? What do they already maintain, in what languages? Who pays for hosting next year, and who owns the accounts?_

**What they said:** Not covered in this meeting. Answered in meeting 2: Sumalee will maintain the system after the team graduates. See [client-interview-2026-09-18.md](client-interview-2026-09-18.md).

## 12. Other stakeholders

_**If there is time. 1 min.** Cheap, and occasionally it turns out somebody with a veto has not been consulted._

_Adapt: Who else could influence this, or be affected by it? Whose approval do we need? Anyone who would rather this project did not happen?_

**What they said:** Not covered this meeting. Raised as `OI-9`, still open as of meeting 2, carry to meeting 3.

---

# The close

## 13. Anything else

_**Must ask. 1 min.** Ask it, then stop talking and wait through the silence. Highest-yield question in the guide, and it only works if you do not fill the pause._

_Adapt: Is there anything I should have asked and did not? What have we not talked about that worries you?_

**What they said:** Not explicitly asked in this meeting; it ran short, largely covering the NDA and project introduction. Still not asked as of meeting 2 either; carried forward as `OI-11`, make sure to ask first in meeting 3.

## 14. The read-back

_**Never skip. 5 min.** The part teams cut when they run late, and the highest-value five minutes of the hour. Say what you understood in your own words and watch for the correction. A client who is nodding may be being polite; a client correcting you is engaged, and that correction is usually the single most useful sentence of the meeting._

_Read back four things: the problem in one sentence, the objectives with any numbers you got, the top three things you heard are hard, and one thing you believe is **out** of scope. The last produces more correction than the other three together._

_Fill in the [vision-and-scope.md](vision-and-scope.md) vision statement table during the meeting, read its six rows aloud, and see what they fix. Ninety seconds._

**What we read back, and what they corrected:** The team did read back its understanding of the project to Sumalee before ending the meeting, and she approved it. That read back covered the overall project understanding rather than the guide's full four part structure (problem statement, objectives with numbers, top three hard things, one thing out of scope), and the vision statement table was not read aloud. The team agreed internally to fully work out the scope before meeting 2. No corrections were recorded. Given how informal this read back was, a fuller structured read back, including the vision statement table, is recommended for meeting 3.

**MVP scope named this meeting (to read back and confirm next time):** Review creation, SVN diff generation, a unified review workspace, basic automation/AI (summaries and simple compliance checks, not a replacement for reviewer judgment), notifications, and review closure. The client's project concept document expands this into more detail (Jira ticket selection, SVN branch/diff automation, automated checklist population, notifications, and review closure with package generation) and should be reconciled with this list when drafting vision-and-scope.md section 4.3.

## 15. Before you leave the room

_**Never skip. 4 min.** Unglamorous, and where teams lose two weeks._

- [ ] **Next meeting on the calendar** before anyone stands up. Not "we will be in touch". _[Date, time, place: not explicitly recorded at the end of this meeting; meeting 2 subsequently took place on 2026-09-18 over Microsoft Teams. Confirm meeting 3's date, time, and place next time, tracked as part of `OI-10`.]_
- [ ] **Cadence agreed:** how often, roughly how long, and in person or remote. This course expects meetings **in person, on campus** where your client can travel; if they are outside DFW, agree the tool and who sends the link. _[Cadence: not explicitly agreed. About 9 days passed between meeting 1 and meeting 2, and meeting 2 was remote (Teams) rather than in person. Still open, `OI-10`.]_
- [ ] **Contact channel and how fast they reply.** _[Channel: Microsoft Teams direct messages. Sumalee said she has a lot of time for the project and is generally available.]_
- [ ] **Who to contact between meetings**, including when this person is away. _[Name, contact: Sumalee Rodolph. No alternate contact recorded yet.]_
- [ ] **Copies requested** of every artifact you were shown. _[Nothing was shown this meeting beyond the client's written project concept document.]_
- [ ] **Introductions requested** to anyone named in sections 8 and 12. _[Not yet, no other names surfaced this meeting.]_
- [ ] **Say what happens next**, in one sentence, so they know what to expect and when. _[Not recorded this meeting.]_

---

# After the meeting

_File everything within 24 hours, while you still remember why each answer mattered. This file is a record, not a home._

| Section | Feeds |
|---|---|
| 1, 2 | [project-glossary.md](project-glossary.md), and Background in [vision-and-scope.md](vision-and-scope.md) |
| 3 | Business Opportunity, Objectives, and Success Metrics in [vision-and-scope.md](vision-and-scope.md) |
| 4, 6 | Background and the process flow in [vision-and-scope.md](vision-and-scope.md); use cases in week 4 |
| 5 | Business rules catalog, week 4 |
| 7, 9, 10 | Quality attributes, constraints, and external interfaces in the specification, week 4 |
| 8, 12 | Stakeholder Profiles in [vision-and-scope.md](vision-and-scope.md) |
| 8, 11 | Risks (`RI-<slug>`) and assumptions (`AS-<slug>`) in [vision-and-scope.md](vision-and-scope.md) |
| 14 | Scope and the vision statement in [vision-and-scope.md](vision-and-scope.md) |
| Anything unanswered | [OPEN-ISSUES.md](OPEN-ISSUES.md) |

## Initial ideas

_[Solutions anyone floated, yours or theirs. Record them here and nowhere else yet. A solution the client already picked ("then I select the state from a drop-down") is not a requirement, and writing it into the specification makes a design decision on their behalf. Ask why until you reach the need underneath, then write down the need.]_

A single workflow tying Jira, SVN, Jenkins, diffs, checklists, and reviewer comments together, with AI used only for summaries, file-change descriptions, and simple compliance checks, explicitly not to replace reviewer judgment. This came from the client, describing the shape of solution she has in mind rather than a need stated abstractly; worth confirming the underlying need (less time spent assembling review context by hand) so we are not locked into her specific solution shape too early. The client's written project concept document elaborates this in much more detail, including a three-level model for how much AI involvement to allow (sections 4 through 6), and should be treated as the fuller reference for this idea.

## Disagreements and hesitations

_[The observer's section, and the one that evaporates fastest. Two participants using the same word differently. A question answered by the wrong person. A topic they returned to three times. An answer that changed between the start and the end. A visible pause before "yes". None of it is evidence on its own; all of it tells you where to look next.]_

None noted. No dedicated observer this meeting (whole team scribed instead), and the meeting was short.

## Open questions

_[Everything you could not answer, and everything they answered with "I would have to check". Copy each into [OPEN-ISSUES.md](OPEN-ISSUES.md) as an `OI-*` with the person who can answer it, then sort them before the next meeting by what it costs you to stay wrong.]_

- `OI-2` (resolved 2026-09-09): baseline review time, about 20 minutes per review, excluding Jenkins build time.
- `OI-3` (partially resolved 2026-09-09): Sumalee began a live walkthrough of one review but did not finish it; a complete pass and a "went wrong" story are still needed.
- `OI-4` (resolved 2026-09-09): keep the underlying process and tools unchanged, keep Excel/CSV export.
- `OI-5` (partially resolved, see meeting 2): daily user count and current review count known, weekly/monthly volume and largest change size still unknown.
- `OI-6` (resolved 2026-09-09): the team cannot reach real authors or reviewers, only Sumalee, for now.
- `OI-7` (partially resolved 2026-09-09): sandbox shape known from the client's concept document, production system owner and documentation still unknown.
- `OI-8` (resolved, see meeting 2): Sumalee will maintain the system after graduation.
- `OI-9` (open): other AppliedAvionics stakeholders not yet discussed.
- `OI-10` (partially resolved 2026-09-09): contact channel is Microsoft Teams direct messages, cadence and meeting 3 logistics still open.
- `OI-11` (open): the guide's catch-all "anything else" question has not been asked in either meeting yet.

See [OPEN-ISSUES.md](OPEN-ISSUES.md) for the canonical, current list, including anything raised in meeting 2.

---

_**Within 24 hours**, send the client your notes and the open questions. It creates the record and gives them a second chance to correct you while the meeting is fresh. Then commit this file._
