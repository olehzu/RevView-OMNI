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
| OI-14 | Is there a required or expected uptime target for the application once deployed, and are there announced maintenance windows to plan around? | Asked on 2026-10-09, but the recorded answer covers maintenance after handoff (the team need not maintain it; Sumalee will just ask questions for a while), not an uptime target or maintenance windows. Re-ask. | Sumalee Rodolph | 2026-10-03 |
| OI-15 | What are the Moderator's complete permissions, and may an Author or Reviewer also act as Moderator on the same review? | Partly answered on 2026-10-09: the Moderator decides back-and-forth issues, makes sure everything is filled out, and closes the review. Sumalee will send the page describing the role. Still unanswered: may an Author or Reviewer also act as Moderator on the same review? | Sumalee Rodolph | 2026-10-04 |
| OI-18 | Is there a required hosting environment, browser support matrix, operating system, or network-access path (intranet, VPN, public internet) for RevView/OMNI once deployed? | Asked on 2026-10-09; Sumalee asked for it in the Teams chat and said "there probably is" a requirement. Not yet sent. | Sumalee Rodolph | 2026-10-04 |
| OI-22 | Can the backend drive SVN from Python well enough for changed-file lists, revision lookup, and diff generation, or does the stack need to change? | `UC-REV-assemble-materials`, the proving slice, depends on it. Cong Quoc Le raised on 2026-10-09 that SVN's native API is C/C++; Sumalee believes Python works and asked to be messaged on Teams if the team is blocked. | Team (verify with a spike), then Sumalee Rodolph | 2026-10-09 |
| OI-23 | Which sign-on mechanism does AppliedAvionics use, and over what protocol can RevView/OMNI integrate with it? | `OI-21` confirmed one exists ("I think we have one"); `SI-identity-provider` and `DE-identity-interface` cannot be designed without the protocol. Sumalee called these "IT questions". | Sumalee Rodolph, via AppliedAvionics IT | 2026-10-09 |

## Resolved

| ID | Question | Answer | Answered by | Date | Filed in |
|---|---|---|---|---|---|
| OI-1 | Does the formal review process need to comply with DO-178C (or another named standard), and if so, which specific clauses govern review artifacts, checklists, and traceability? | No named standard to comply with; "just be careful with what we put into AI." Team reading, to confirm: the review rules stand on internal practice, and review content sent to AI tools needs care. | Sumalee Rodolph | 2026-10-09 | Not yet filed: Source column of the affected rules in business-rules.md; [client-interview-2026-10-09.md](client-meeting/client-interview-2026-10-09.md) section 9 |
| OI-2 | What does the current review process cost in time today, so we have a baseline for `BO-review-centralization`? | About 20 minutes per review to gather forms and fill in fields, not counting Jenkins build time. | Sumalee Rodolph | 2026-09-09 | `BO-review-centralization`, vision-and-scope.md section 2.3 (not yet drafted) |
| OI-3 | Can Sumalee walk the team through one complete, recent review end to end, including a case where it went wrong or got stuck? | Closed without asking. The meeting lead judged it not worth the client's time on 2026-10-09; reopen if it turns out to matter. | Oleh Zubariev (lead) | 2026-10-09 | Not applicable |
| OI-4 | What about the current process works well and should not change? | Do not change the underlying review process or the existing tools (SVN, Jira, Jenkins, the review record); the app should only make the existing process faster to run. Review records and checklists must still export in the same Excel/CSV format used today. | Sumalee Rodolph | 2026-09-09 | vision-and-scope.md sections 2.7 and 4 (not yet drafted) |
| OI-5 | How many reviews happen per week or month, and how big is the largest change ever reviewed? | Leads can go through up to three code reviews a day, about 20 a week; a ticket can have 30 files that need to be changed. Largest diff size in lines not asked. | Sumalee Rodolph | 2026-10-09 | Not yet filed: software-requirements-specification.md section 9.2; [client-interview-2026-10-09.md](client-meeting/client-interview-2026-10-09.md) section 7 |
| OI-6 | Can the team talk to or observe an actual review author or reviewer, not only Sumalee? | No, not at this time. Sumalee is the team's only point of contact at AppliedAvionics for now. | Sumalee Rodolph | 2026-09-09 | `RI-proxy-only-contact`, vision-and-scope.md section 2.6 (not yet drafted) |
| OI-7 | Who owns AppliedAvionics' production Jira, SVN, and Jenkins, and is there documentation for how the sandbox should mirror them? | Closed without asking. The meeting lead judged it not worth the client's time on 2026-10-09; reopen if it turns out to matter. | Oleh Zubariev (lead) | 2026-10-09 | Not applicable |
| OI-8 | Who maintains this system after the team graduates, and what do they already run? | Sumalee will maintain it herself. Expect to need about one person available for roughly a year after handoff for any issues; after that, support needs should drop off. | Sumalee Rodolph | 2026-09-18 | vision-and-scope.md section 4.4 (not yet drafted) |
| OI-9 | Are there other AppliedAvionics stakeholders (for example engineering management, IT/security) the team should meet or get sign-off from? | IT has to sign off on the project, and Sumalee will get that sign-off. Her boss does not give input; she is the only client. | Sumalee Rodolph | 2026-10-09 | Not yet filed: vision-and-scope.md stakeholder profiles; [client-interview-2026-10-09.md](client-meeting/client-interview-2026-10-09.md) section 12 |
| OI-10 | What is the agreed meeting cadence, and when and where is meeting 3? | Closed without asking. The meeting lead judged it not worth the client's time on 2026-10-09; reopen if it turns out to matter. Sumalee is reachable in the Teams group chat. | Oleh Zubariev (lead) | 2026-10-09 | Not applicable |
| OI-11 | Is there anything about the process or project we have not asked about that worries Sumalee? | The open concern is getting the sandbox and a server set up; if AppliedAvionics IT does not approve, the team may need to ask Dr. Wei. | Sumalee Rodolph | 2026-10-09 | Not yet filed: architectural-design.md section 11; [client-interview-2026-10-09.md](client-meeting/client-interview-2026-10-09.md) section 13 |
| OI-12 | When exactly will the example/sample Jira setup be ready, and does it cover what the sandbox needs? | Closed without asking. The meeting lead judged it not worth the client's time on 2026-10-09; reopen if it turns out to matter. | Oleh Zubariev (lead) | 2026-10-09 | Not applicable |
| OI-13 | Does AppliedAvionics have an internal accessibility or usability standard (for example WCAG) that an internal engineering tool must meet? | No internal accessibility or usability standards. | Sumalee Rodolph | 2026-10-09 | Not yet filed: software-requirements-specification.md section 9.1; [client-interview-2026-10-09.md](client-meeting/client-interview-2026-10-09.md) section 9 |
| OI-16 | Are RevView/OMNI's review notifications in-app, email-based, or both? | Both in-app and email (from the scribe's notes; the answer is inaudible in the transcript). | Sumalee Rodolph | 2026-10-09 | Not yet filed: software-requirements-specification.md sections 5.2 and 8.5; [client-interview-2026-10-09.md](client-meeting/client-interview-2026-10-09.md) section 10 |
| OI-17 | Do any export-control, data-residency, or hosting restrictions (for example ITAR) apply to RevView/OMNI or its data, in development or in production, given AppliedAvionics manufactures avionics hardware? | No: "we don't sell arms, we don't do that. Push button switches, like little switches." A judgement on the product line, not a check with export compliance. | Sumalee Rodolph | 2026-10-09 | Not yet filed: software-requirements-specification.md section 2.3; [client-interview-2026-10-09.md](client-meeting/client-interview-2026-10-09.md) section 9 |
| OI-19 | Does RevView/OMNI need to support any locale other than English and United States date and numeric formats, for example if an international AppliedAvionics office ever authors or reviews a change? | No; English only, no other number formats. | Sumalee Rodolph | 2026-10-09 | Not yet filed: software-requirements-specification.md section 10; [client-interview-2026-10-09.md](client-meeting/client-interview-2026-10-09.md) section 9 |
| OI-20 | Who trains AppliedAvionics' authors and reviewers to use RevView/OMNI, and when, relative to the pilot and to handoff? | No formal training. The team gives a demo of the application to the employees. | Sumalee Rodolph | 2026-10-09 | Not yet filed: software-requirements-specification.md section 11; [client-interview-2026-10-09.md](client-meeting/client-interview-2026-10-09.md) section 11 |
| OI-21 | Does AppliedAvionics actually provide an enterprise identity/sign-on mechanism that RevView/OMNI can integrate with for user authentication, or does the team need to design its own account system? | Yes: "I think we have one." Which mechanism and protocol is `OI-23`. | Sumalee Rodolph | 2026-10-09 | Not yet filed: software-requirements-specification.md sections 2.5 and 8.3; [client-interview-2026-10-09.md](client-meeting/client-interview-2026-10-09.md) section 10 |
