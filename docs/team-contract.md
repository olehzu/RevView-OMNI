# Team Contract: Team 8 RevView/OMNI

**Project:** 	RevView/OMNI  
**Members:** Oleh Zubariev, Ralph Castilleja, Francisco Lugo Gonzales, Valerie Valles, Cong Quoc Le, Ethan Nguyen   
**Repository:** https://github.com/olehzu/RevView-OMNI  
**Signed:** 09/04/2026  

## 1. Meeting time

We meet every Monday at 6pm at the TCU library, for one hour.
A member who cannot attend tells the team the day before and reads the minutes.

## 2. Communication

Primary channel: https://softwareengin-2fh7080.slack.com/archives/C0BUWG2324B. Client contact goes through Francisco Lugo Gonzales.
We reply within 24 hours on weekdays. Anything urgent: Contact through the professor or TAs.

## 3. How we decide

Routine calls: Student responsible for the use case decides.
Anything affecting the whole team: discussed at the weekly meeting, majority, ties go to the project lead.
A decision that survives the meeting is written down in Google Doc meeting summary.

## 4. How work is claimed

Work is divided by use case, not by layer. One member owns a use case end to
end: front end, back end, tests, and the pipeline.
Claiming: assign yourself the sub-issue and move the card.
Nobody is the "front-end person" or the "tester".

## 5. Git workflow and review

Coding conventions (naming, formatting, layout) live in `AGENTS.md`, not here.
This clause is about how work moves.

Branch per sub-issue, named **<convention, e.g. feat/42-short-slug>**.
Never push to `main`. Every change arrives as a pull request.
A pull request needs 2 approving review(s) from someone who does not own the use case.
A reviewer reads the issue before the diff. Blocking a merge: if produces bugs or unsufficient fix.

## 6. Working with AI

We use Claude and alternative agents. Our charter lives in `AGENTS.md`.
Every member can explain any line submitted under their name.
We do not merge agent output that nobody has read.
Additional limits we agree on: we don't overdo the pre-agreed change because "the agent wrote more".

## 7. When someone does not deliver

First: A team member raises it at the next meeting. We attack the problem, not the person.
If it happens again: encourage the person to have group development sessions during which other members can assist them.
Still unresolved: we escalate to our TA, then to the instructor. We escalate early.

## Signatures

Each member adds their own line, in their own commit.

- Oleh Zubariev, 09/04/2026
- Cong Le, 09/04/2026
- Francisco Lugo Gonzales, 09/04/2026
- Ralph Castilleja, 09/04/2026
- Ethan Nguyen, 09/07/2026
- Valerie Valles, 09/11/2026
