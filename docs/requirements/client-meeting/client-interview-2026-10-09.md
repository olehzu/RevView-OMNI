# Client Interview Guide

**Project:** RevView/OMNI
**Team:** Team 8
**Client:** Sumalee Rodolph, AppliedAvionics
**Meeting:** 3 of several

---

_**What this file is.** Your script going in, your meeting record coming out. Copy it once per meeting into `docs/requirements/` as `client-interview-YYYY-MM-DD.md` and commit it the same day._

_**How to use it.** Each section says what it is for, what it is worth in minutes, and whether it must happen in this meeting. The example questions are written for a different domain (technical recruiting) on purpose, so you cannot use them unchanged. Rewrite them in your client's words before you walk in, and write the answers underneath in **their** words rather than yours._

_**Work it with your agent.** Give it your one-page brief, this file **including these instructions**, and a role: "You are an experienced business analyst preparing for a first client interview. Using the question types in this guide, write the version of each question that fits this client's domain, and list every acronym in the brief you would want defined before the meeting." Then do the part it cannot: pick which of its questions are worth your client's limited hour. **Sort by what it costs you to stay wrong**, not by what is easy to ask. Anything you could answer by reading a document is not worth a client minute._

## Listen before you build

**An idea you propose in the first twenty minutes is not worth what it costs you.** Your strongest instinct will be to show your client you understood by describing what you would build. Early, that ends the elicitation: a client who has heard your idea reacts to it instead of describing their world.

This is about order, not silence. Some clients want to think out loud with you, and a few asked for the project because they want exactly that help. Do it **after** the read-back in section 14, when you can describe their process back to them accurately and the brainstorm is grounded in their world rather than your imagination. If they open by asking for your ideas, say you have some and would rather earn them by understanding the process first, then come back to it before you leave.

**The separate rule is absolute: commit to nothing.** Not a deadline, not a feature, not "sure, we can add that". Five teammates are not in the room. "Let me write that down and bring it back to the team" is the whole sentence, and it holds even when a client pushes.

## Before you go

- [ ] **Three roles assigned.** Lead asks and moves the agenda, one person not four. Scribe writes and does not ask, capturing exact words, especially nouns. Observer watches what is not said: hesitation, the topic they keep returning to, who they defer to. _[Lead and scribe assigned (Oleh Zubariev, Francisco Lugo Gonzales); no observer recorded.]_
- [x] **Everyone has read the client's pitch slides** (TCU Online) and written questions individually before you merged them. The ones two of you wrote independently are the ones to ask.
- [ ] **Shortlist sent to the client the day before.** They arrive with answers instead of promises. _[The agenda was the open list in [OPEN-ISSUES.md](../OPEN-ISSUES.md); whether it was sent ahead is not recorded.]_
- [x] **This file open on the scribe's laptop**, with someone on paper as backup.
- [ ] **Someone owns the clock.** You will not get through this guide, and that is expected.

## Meeting record

| | |
|---|---|
| **Date** | 2026-10-09 |
| **Time and location** | 12:00 PM. Hybrid: four team members in the room with Sumalee, the rest on Microsoft Teams ("Thanks for coming guys, all four of you", then "teams people, you're dismissed") |
| **Client participants** | Sumalee Rodolph (AppliedAvionics) |
| **Team participants** | Oleh Zubariev (lead), Francisco Lugo Gonzales (scribe), Cong Quoc Le, Valerie Valles; others not recorded |
| **Recording** | Teams transcription only, started by Cong Quoc Le at 12:24 PM and run for 12 minutes, from the Moderator question (`OI-15`) to the end. Team questions asked in the room are attributed to Sumalee's speaker label in it. Earlier answers come from the scribe's notes alone. |
| **Photos of screens or forms** | Not recorded in the scribe's notes |

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

_This meeting worked through the open list in [OPEN-ISSUES.md](../OPEN-ISSUES.md) by number rather than the shape above. The scribe's notes record answers to `OI-1`, `OI-5`, `OI-9`, `OI-11`, and `OI-13` through `OI-21`; each answer below is filed under the section it belongs to and cites its `OI-*`. `OI-3`, `OI-7`, `OI-10`, and `OI-12` were deliberately not asked: the lead judged them not worth the client's time, and they are closed in [OPEN-ISSUES.md](../OPEN-ISSUES.md). Answers from `OI-15` onward are checked against the Teams transcript and quote it where it is clearer; the transcript also captured a tech stack discussion that is not in the open list (sections 9 and 10, and Initial ideas)._

**Extra time goes into section 4 first.** It repays another ten minutes and it is the only section you cannot reconstruct from notes afterward.

"Can wait" means the next meeting, not never. When you are behind, drop from the middle. **Never drop 14 or 15:** the read-back is where you learn you misunderstood something, and the close is where you stop losing two weeks to scheduling.

---

# Opening

## 1. Get to know your client

_**Must ask. 5 min.** Not small talk. Whose problem is this, how much of the domain lives only in this person's head, and how much of their own time do they have for you? A client fitting this around a full job answers email slowly, and you want to know that in week 3 rather than week 9._

_Adapt: Tell me about being an HR manager. How did you choose that line of work? What do you most and least like about it? How does this project fit alongside the rest of your work?_

**What they said:** Not covered this meeting. See [client-interview-2026-09-09.md](client-interview-2026-09-09.md) section 1.

---

# The business

## 2. Context and domain

_**Must ask. 5 min.** You are here for vocabulary as much as facts. Every term you do not recognize goes in the glossary before you leave. When your client says "cycle" in one sentence and "sprint" in the next, ask which they mean while they are still in front of you; an agent reading the transcript afterward cannot ask._

_Adapt: Give us some background on recruiting here. Why does it matter to the company? Who else is involved? Any documents, slides, or videos that would get us up to speed on the terminology? When you say [term], what does that cover?_

**What they said:** Not covered this meeting. No new terms introduced.

**Terms for the glossary, in their words:** None new. The scribe's notes say "Leads" in `OI-5`; whether that means a review lead, a Moderator, or a team lead was not recorded.

## 3. Business drivers and objectives

_**Must ask. 5 min.** Why this, why now. These become your business objectives, so push for a number: when they name a benefit, ask the follow-up nobody asks, **what is that number today?**_

_Expect to miss it here. Baselines surface in section 4, when they are looking at the thing that takes the time. Ask the objective now, listen for the number all hour, and close the gap in the read-back._

_Adapt: Why did you propose this project? What is the main problem, or the opportunity? Who is affected, and who benefits? What happens if we do nothing? How will you know it worked, and what is that number today?_

**What they said:** Not covered this meeting. Baseline unchanged from meeting 1 (about 20 minutes per review).

**Candidate objectives (`BO-<slug>`), with baselines where you got them:** Unchanged from meeting 1.

---

# The process

## 4. How it works today

_**Must ask. 10 min, the best ten in the meeting.** Ask them to show you rather than tell you. People describe the process they believe they follow; the spreadsheet shows the one they actually follow, and the gap is where the requirements hide. **"Show me" is the two most productive words in requirements engineering, and they cost nothing.**_

_Walk one real recent case end to end. "Take me through the last one you did" beats "how does it usually work", because the general shape is a summary they have given before and the last real one has the exceptions in it._

_Adapt: What are the steps in hiring a technical candidate? Could you show me your interview guide, and the notes from the last few? Who does what at each step? Where does it get stuck? What do you do when it goes wrong?_

**What they said:** Not covered this meeting. Not covered this meeting. `OI-3` (the unfinished end-to-end walkthrough from meeting 1) was deliberately not asked and is closed.

**Artifacts they showed us:** Sumalee showed a page of her own notes on screen, covering the Moderator's role, tech stack options, and background on "the Phoenix and the Falcon platform, Subversion, ... Jenkins, stuff like that", a roadmap, and "what I have already written up for the HTML files". The team did not have access to it; she said "I'll get it to you guys" and "I'll send this all to you guys."

The transcript opens mid-sentence with "Commit it, send an e-mail to everyone listing", apparently describing a step of the current process; the context before it was not captured.

## 5. What is hard about it

_**Must ask. 5 min.** The complaint is usually the requirement. Listen for "must", "unless", "only", and "except", which arrive unannounced in the middle of a story about something else. Those sentences are business rules, and they exist whether or not your software does._

_Adapt: What is the most frustrating part? Walk me through the last time it went badly. What takes longest? What do you have to redo? What do people get wrong? What do you check by hand because you do not trust the system?_

**What they said:** On the Moderator (`OI-15`): "They just need to, like, make a decision on like the back and forth, make sure that everything is completed, which, with the application, like, we'll be able to see if we have any gaps or if someone hasn't filled out yet, so that would completely get rid of that." And: "They just wanna make sure that everything is filled out and then ... that they like close it." Sumalee will send the team the page describing the role. Whether an Author or Reviewer may also act as Moderator on the same review was not asked.

**Rules heard (candidate `BR-*` for week 4):**

- The Moderator decides any back-and-forth issue between participants in a review, makes sure everything in the review is filled out, and closes it (`OI-15`). Full detail pending Sumalee's document.
- Review content shared with AI tools must be handled with care (`OI-1`). Exactly what may or may not be sent is not yet stated.

## 6. What already works

_**Must ask. 3 min.** Ask what is good before you propose replacing it. A team that removes something the client liked has lost trust it will not get back this semester, and nobody volunteers this unasked._

_Adapt: What would you keep exactly as it is? What would you miss if it disappeared? Has anything been tried before that did not work, and why?_

**What they said:** Not covered this meeting. Already answered in meeting 1: keep the underlying process and tools, keep Excel/CSV export.

## 7. Volumes and scale

_**Must ask. 3 min.** These numbers decide most of your architecture, and they are cheap to ask for and expensive to guess. Twenty records a semester and two hundred thousand a day are different systems._

_Adapt: How many of these in a week? A year? How many at the busiest moment, and when is that? How big is the largest one? How much history has to stay available? How many people use it at once on the worst day?_

**What they said:** Leads can go through up to three code reviews a day, which could mean about 20 code reviews a week. A ticket can have 30 files that need to be changed (`OI-5`). The size of the largest diff in lines, and history retention, were not recorded.

## 8. Who the users are

_**Must ask. 4 min.** The person who commissions software is often not the person who uses it._

_**If you cannot reach the real users, that is a project risk, not a scheduling detail.** Record it as an `RI-<slug>` the same day. Building from a proxy's account is the most common way a capstone ships something nobody uses, and it is survivable only if you know you are doing it._

_Adapt: Who uses this day to day? How many? What do they use today? Can we talk to two or three, and watch one of them work? Will they test it before handover?_

**What they said:** Not covered beyond `OI-20`: the team will give a demo of the application to AppliedAvionics employees. Access to users other than Sumalee was not raised; `RI-proxy-only-contact` stands, and Sumalee reinforced it: "I'm the only client. Like my boss doesn't give me input."

**Can we reach real users? If not, why, and what is the risk:** Unchanged from meeting 1, see [client-interview-2026-09-09.md](client-interview-2026-09-09.md) section 8. The planned demo to employees (`OI-20`) is the first point of contact with real users that has been named.

---

# The boundaries

## 9. Constraints and rules

_**Must ask. 4 min.** Nobody asks these in meeting 1 and everybody regrets it in November. A constraint restricts how you may build, and it is a requirement even though it describes no behavior. Ask directly; clients do not volunteer these, they assume you know._

_Adapt: Is there anything we are required to use, or forbidden from using? Does IT have to approve the technology, and how long does that take? Does this touch personal data, student records, health information, or payments? Any regulations or policies it has to satisfy? Any hard dates we do not know about? Is there a budget for hosting, and who signs off?_

**What they said:**

- No need to comply with rules (a named standard such as DO-178C), just be careful with what we put into AI (`OI-1`). _Team reading, to confirm: no formal standard governs the review artifacts, but source and review content sent to AI tools needs care._
- The project needs a sign-off from IT, and Sumalee will get it (`OI-9`).
- There are no internal accessibility or usability standards (`OI-13`).
- No export-control, data-residency, or hosting restrictions such as ITAR apply (`OI-17`): "I'm gonna say no, I'm gonna say no, but I don't think that's, we don't sell arms, we don't do that. Push button switches, like little switches." She asked what ITAR was before answering, so this is her judgement rather than a checked answer (see Disagreements and hesitations).
- No other language or number formats need to be supported (`OI-19`): asked "do we need to support the other language, the numbers?", she answered "No."
- Hosting environment, browser support, operating system, and network-access path (`OI-18`): deferred. "Send that in the chat, and I'll answer that later ... 'cause there probably is." She expects there is a requirement but did not say what it is.
- "A lot of these are IT questions, I feel like" (after `OI-21`).
- Tech stack: "Python ... API, right? React, TypeScript, and then Postgres for the database, because we're going to need ... to store, like, our code ... code review files." Not a fixed constraint: "this isn't like set in stone either ... this was just like the AI recommendation. So like, if you have a better idea, like, please let me know." This differs from the specification's `CO-frontend-language` (JavaScript), and the database is not named there at all.

## 10. External dependencies

_**Must ask. 3 min.** What your system has to talk to. Access credentials take weeks to obtain, so the ask has to happen now._

_Adapt: What other systems does this exchange data with, in which direction, in what format? Who owns them, and who do we ask for access? How long does that usually take? Is there documentation? What does the service cost, and who pays?_

**What they said:**

- AppliedAvionics has a sign-on mechanism (`OI-21`): "I think we have one. You have one. We have one." Which one, and its protocol, were not asked; "I think" makes it worth confirming with IT.
- Notifications are both in-app and email (`OI-16`). The transcript has the question but her answer is inaudible; this comes from the scribe's notes.
- SVN from Python: Cong Quoc Le asked whether SVN's API, written in C/C++, supports Python well enough, or whether the team should consider C/C++ or Node.js. Sumalee: not C/C++, "it's a web application, so it's not really like flight code"; "I looked it up earlier and it said that Python will be able to work with SVN"; "if you find out that it doesn't, then of course, like let me know if you are like blocked by anything. And then we can always change the tech stack." She asked for the question to be sent to her on Teams.
- The team still needs the sandbox set up and a server set up; if AppliedAvionics IT does not approve, the team might need to ask Dr. Wei (`OI-11`).
- The production system owners and documentation (`OI-7`) and the sample Jira setup (`OI-12`) were deliberately not asked; both are closed.

## 11. Lifetime and who maintains it

_**Must ask. 2 min.** The question students never ask and every client can answer. **Who runs this after we graduate, and what do they already know how to run?** It constrains your entire technology choice, so ask before you pick a stack rather than after._

_Adapt: How long should this keep running? Who supports it after we graduate from TCU? What do they already maintain, in what languages? Who pays for hosting next year, and who owns the accounts?_

**What they said:** The team will not have to worry about maintenance after handing the application off to the client; they will just ask questions for a little while afterward (recorded against `OI-14`, consistent with `OI-8`). An uptime target and maintenance windows, which `OI-14` asked about, were not recorded. On training (`OI-20`): "No one ... it won't be training, but like, I'll have to do a demo, so I'll have to know everything about it, or you guys, you guys could do the demo, actually, I'll have you guys do the demo."

## 12. Other stakeholders

_**If there is time. 1 min.** Cheap, and occasionally it turns out somebody with a veto has not been consulted._

_Adapt: Who else could influence this, or be affected by it? Whose approval do we need? Anyone who would rather this project did not happen?_

**What they said:** IT has to sign off on the project, and Sumalee will handle getting that sign-off (`OI-9`). No other stakeholders were named, and Sumalee said her boss does not give her input on the project. IT is the one other party with a say: she called several of the open questions "IT questions".

---

# The close

## 13. Anything else

_**Must ask. 1 min.** Ask it, then stop talking and wait through the silence. Highest-yield question in the guide, and it only works if you do not fill the pause._

_Adapt: Is there anything I should have asked and did not? What have we not talked about that worries you?_

**What they said:** First answer recorded to the catch-all question (`OI-11`): the open concern is getting the sandbox and a server set up, with Dr. Wei as the fallback if AppliedAvionics IT does not approve.

## 14. The read-back

_**Never skip. 5 min.** The part teams cut when they run late, and the highest-value five minutes of the hour. Say what you understood in your own words and watch for the correction. A client who is nodding may be being polite; a client correcting you is engaged, and that correction is usually the single most useful sentence of the meeting._

_Read back four things: the problem in one sentence, the objectives with any numbers you got, the top three things you heard are hard, and one thing you believe is **out** of scope. The last produces more correction than the other three together._

_Fill in the [vision-and-scope.md](../vision-and-scope.md) vision statement table during the meeting, read its six rows aloud, and see what they fix. Ninety seconds._

**What we read back, and what they corrected:** Not recorded in the scribe's notes. The read-back owed since meeting 2 is still outstanding.

## 15. Before you leave the room

_**Never skip. 4 min.** Unglamorous, and where teams lose two weeks._

- [ ] **Next meeting on the calendar** before anyone stands up. Not "we will be in touch". _[Date, time, place: not set. `OI-10` was deliberately not asked and is closed; Sumalee is reachable in the Teams group chat.]_
- [ ] **Cadence agreed:** how often, roughly how long, and in person or remote. This course expects meetings **in person, on campus** where your client can travel; if they are outside DFW, agree the tool and who sends the link. _[Cadence: not agreed; see `OI-10`.]_
- [ ] **Contact channel and how fast they reply.** _[Channel, turnaround: Microsoft Teams; "you can always ask me in the group chat. Please do that."]_
- [ ] **Who to contact between meetings**, including when this person is away. _[Name, contact: Sumalee Rodolph; no alternate recorded.]_
- [ ] **Copies requested** of every artifact you were shown. _[Sumalee is sending the page she showed: the Moderator's role (`OI-15`), tech stack, platform and tool background, roadmap, and her HTML write-up. The team owes her the `OI-18` question and the SVN-from-Python question in the Teams chat.]_
- [ ] **Introductions requested** to anyone named in sections 8 and 12. _[None; no new names surfaced.]_
- [ ] **Say what happens next**, in one sentence, so they know what to expect and when. _[Not recorded.]_

---

# After the meeting

_File everything within 24 hours, while you still remember why each answer mattered. This file is a record, not a home._

| Section | Feeds |
|---|---|
| 1, 2 | [project-glossary.md](../project-glossary.md), and Background in [vision-and-scope.md](../vision-and-scope.md) |
| 3 | Business Opportunity, Objectives, and Success Metrics in [vision-and-scope.md](../vision-and-scope.md) |
| 4, 6 | Background and the process flow in [vision-and-scope.md](../vision-and-scope.md); use cases in week 4 |
| 5 | Business rules catalog, week 4 |
| 7, 9, 10 | Quality attributes, constraints, and external interfaces in the specification, week 4 |
| 8, 12 | Stakeholder Profiles in [vision-and-scope.md](../vision-and-scope.md) |
| 8, 11 | Risks (`RI-<slug>`) and assumptions (`AS-<slug>`) in [vision-and-scope.md](../vision-and-scope.md) |
| 14 | Scope and the vision statement in [vision-and-scope.md](../vision-and-scope.md) |
| Anything unanswered | [OPEN-ISSUES.md](../OPEN-ISSUES.md) |

## Initial ideas

_[Solutions anyone floated, yours or theirs. Record them here and nowhere else yet. A solution the client already picked ("then I select the state from a drop-down") is not a requirement, and writing it into the specification makes a design decision on their behalf. Ask why until you reach the need underneath, then write down the need.]_

- **Tech stack, the client's:** Python API, React with TypeScript, Postgres. Sumalee said it was an AI recommendation and open to change. The need underneath is that the backend can drive SVN and the database can store code review files; the languages themselves are not a client requirement.
- **Tech stack, the team's:** Cong Quoc Le floated C/C++ (for SVN's native API) and Node.js with TypeScript on both ends. Sumalee ruled out C/C++ and invited a better proposal if the team has one.
- The fallback of asking Dr. Wei for a server (section 10) is a contingency, not a design choice.

## Disagreements and hesitations

_[The observer's section, and the one that evaporates fastest. Two participants using the same word differently. A question answered by the wrong person. A topic they returned to three times. An answer that changed between the start and the end. A visible pause before "yes". None of it is evidence on its own; all of it tells you where to look next.]_

No observer was recorded; these come from the transcript.

- **`OI-17` (ITAR) was a hedged no.** Sumalee asked what ITAR meant, said "let's research", then "I'm gonna say no ... but I don't think that's ...". The answer rests on her product line (push-button switches), not a check with export compliance.
- **`OI-21` (sign-on) was "I think we have one."** Worth confirming with IT, since the architecture depends on it.
- **She deferred to IT repeatedly** ("A lot of these are IT questions") and said "I don't know what I'm doing 100%" about the stack. Her technical answers are suggestions, not decisions.
- **Two answers should be re-asked:** `OI-14` (asked about uptime, answered about maintenance after handoff) and `OI-18` (she asked for it in the chat).

## Open questions

_[Everything you could not answer, and everything they answered with "I would have to check". Copy each into [OPEN-ISSUES.md](../OPEN-ISSUES.md) as an `OI-*` with the person who can answer it, then sort them before the next meeting by what it costs you to stay wrong.]_

- `OI-1` (answered, to confirm): no formal standard to comply with; be careful with what goes into AI.
- `OI-3` (closed, not asked): judged not worth the client's time.
- `OI-5` (answered): up to three reviews a day per lead, about 20 a week; a ticket can touch 30 files.
- `OI-7` (closed, not asked): judged not worth the client's time.
- `OI-9` (answered): IT sign-off is needed, and Sumalee will get it.
- `OI-10` (closed, not asked): judged not worth the client's time.
- `OI-11` (answered): the concern is the sandbox and server setup, with Dr. Wei as fallback.
- `OI-12` (closed, not asked): judged not worth the client's time.
- `OI-13` (answered): no internal accessibility or usability standards.
- `OI-14` (partially answered): no maintenance burden after handoff beyond questions; uptime target and maintenance windows not answered.
- `OI-15` (partially answered): the Moderator decides back-and-forth issues, ensures everything is filled out, and closes the review; full detail in a page Sumalee will send; author-as-moderator not asked.
- `OI-16` (answered, from the scribe's notes): both in-app and email.
- `OI-17` (answered, hedged): no; "we don't sell arms".
- `OI-18` (still open): Sumalee asked for it in the Teams chat; she expects there is a requirement.
- `OI-19` (answered): English only, no other number formats.
- `OI-20` (answered): no training; the team gives the demo to employees.
- `OI-21` (answered): "I think we have one".
- `OI-23` (new, open): which sign-on mechanism, and over what protocol; a question for AppliedAvionics IT through Sumalee.
- `OI-22` (new, open): does SVN's API work from Python well enough for diff generation and revision lookup, or does the stack need to change? Sumalee believes it does; the team to verify and message her on Teams.
- New, open: tech stack. The client suggested Python, React with TypeScript, and Postgres; the specification says JavaScript and names no database. The team decides and updates `CO-frontend-language`.

See [OPEN-ISSUES.md](../OPEN-ISSUES.md) for the canonical, current list; the answers above are moved into its Resolved table.

---

_**Within 24 hours**, send the client your notes and the open questions. It creates the record and gives them a second chance to correct you while the meeting is fresh. Then commit this file._
