# Business Rules

**Project:** RevView-OMNI
**Team:** Team 8
**Client:** Sumalee Rodolph, Applied Avionics
**Version:** 0.1

---

_**How to use this template.** Instructions appear in italic square brackets. Fill in underneath them and leave them in place until the document is stable._

_**What a business rule is.** A corporate policy, a government regulation, a law, an industry standard, or a computational formula. Business rules are a rich source of requirements, because they dictate properties your system must have in order to conform to them._

_**What a business rule is not: a software requirement.** This is the distinction students get wrong, so read it twice. A rule is a property of the **business**. It exists whether or not your software does, it was true before you arrived, and it will still be true if the project is cancelled. "A student may only submit a peer evaluation during an active week" is a rule the course had before anyone wrote code._

_What belongs to your software is the **enforcement** of that rule, and that is a functional requirement, written in the specification and cited back here. Keeping the two apart is what lets you answer the question that comes up every semester: "who decided this, and can we change it?" If it is a rule, the client's organization decides and you comply. If it is a requirement, your team decides and you can negotiate._

## How to hear one in a meeting

_[Rules almost never arrive announced. They surface in the middle of a story about something else, usually in one of these shapes:]_

- _"Must comply with..."_
- _"Only `<someone>` may `<do something>`"_
- _"If `<condition>`, then `<something happens>`"_
- _"Must be calculated according to..."_
- _"...unless it has been more than a year."_

_Examples of a client stating a rule without knowing it: "A new client must pay 30 percent of the estimated consulting fee and travel expenses in advance." "Time-off approvals must comply with the company's vacation policy."_

_When you hear one, write it down in the meeting. You will not reconstruct it afterward, and the exact wording matters because the rule is someone else's sentence, not yours._

## The five shapes a rule takes

_[Useful for recognizing rules, not for organizing this document. Sections below are grouped by topic, not by these categories.]_

| Shape | What it does | Example |
|---|---|---|
| **Fact** | States something always true about the business | Every senior design team belongs to exactly one course section. |
| **Constraint** | Restricts what may be done, or by whom | Only a course admin may create a course section. |
| **Action enabler** | Triggers an action when a condition holds | If a student has not completed safety training in 12 months, the request is refused. |
| **Inference** | Derives a new fact from known facts | A team with no submissions for two consecutive weeks is at risk. |
| **Computation** | Defines how a value is calculated | The peer evaluation score is the mean of all scores received that week. |

_Computations are the ones teams forget are rules. A formula the client uses today is a rule you must reproduce exactly, not a design decision you get to make. Ask for the spreadsheet._

## What a rule turns into

_[One rule usually propagates into several requirements of different kinds. This is why the document exists as its own artifact rather than being scattered through the specification.]_

| Requirement type | How the rule shows up | Example |
|---|---|---|
| Business requirement | A regulation drives a business objective | The system must enable compliance with all federal and state chemical reporting regulations within five months. |
| User requirement | A privacy policy dictates who may do what | Only laboratory managers may generate chemical exposure reports for anyone other than themselves. |
| Functional requirement | A company policy becomes system behavior | If an invoice is received from an unregistered vendor, the system shall email the vendor the supplier intake form and the W-9. |
| Quality attribute | A safety regulation becomes a checked property | The system must maintain safety training records and check them before a user can request a hazardous chemical. |

## Identifiers and traceability

_Each rule carries a stable `BR-<slug>` identifier, a name-based slug coined from the rule's gist: `BR-active-weeks`, `BR-section-admin-only`, `BR-artifact-key-unique`. Never renumber, rename, or repoint one. The thematic grouping into sections below is organizational only and does not affect a rule's identity, so moving a rule between sections is free and renaming it is not._

_**Cite rules, do not copy them.** When a use case is governed by a rule, its Business Rules field carries the identifier only, never the rule's text. One rule, one home. A rule copied into three use cases will be updated in one of them._

_A rule may cite another rule by identifier where one depends on another._

## Every rule needs a source

_[The column teams leave blank, and the one that matters most. For each rule, record where it comes from: a named policy document, a regulation, a page of the client's handbook, or the person who told you and the date.]_

_A rule you cannot attribute is usually not a rule. It is your team's design decision wearing a rule's clothes, and it belongs in the specification where it can be argued with. The test: if you asked your client to change it tomorrow, who would have to approve? If the answer is "you", it was never a rule._

_Where a rule is expected to change, say so and say when. Rules change on the business's schedule, not on yours._

## Where your AI teammate helps, and where it is dangerous

_[Delegate: turning your meeting notes into candidate rules, spotting sentences in a transcript that have the shape of a rule, and finding use cases in your specification that a given rule ought to govern but does not cite.]_

_**Do not let it invent rules.** This section is the single most dangerous place in your requirements for fabricated content, because an invented rule reads exactly like a real one. "Passwords must be at least 8 characters." "Records must be retained for 7 years." Both are plausible, both are common, and neither is your client's policy unless your client said so. A fabricated rule then propagates into functional requirements, tests that pass, and code that enforces something nobody asked for._

_The Source column is the defense. Every rule traces to a document or a person, or it does not go in the file. When your agent proposes a rule, the only question is: who told us this?_

## Revision History

| Date | Version | Description | Author |
|---|---|---|---|
| 2026-09-09 | 0.1 | Initial rules from the client brief and first client meeting | Valerie Valles |
| 2026-09-18 | 0.2 | Reviewed rules and clarified questions on project with the client | Valerie Valles |
| 2026-09-25 | 0.3 | Drafted rules from the RevView/OMNI concept document; pending client confirmation | Valerie Valles |

---

## 1. Introduction

### 1.1 Purpose

This document collects the business rules — policies, regulations, standards, and
formulas — that govern Applied Avionics' business as it relates to RevView-OMNI.
The [software requirements specification / SRS] cites these rules by identifier
rather than restating them, so each rule has a single source of truth.

### 1.2 Scope

This document covers business rules related to:

- The required review artifacts (diff files, review records, checklists) and their audit/compliance properties.
- The role of AI assistance relative to reviewer and author judgment.
- Constraints on student access to Applied Avionics' internal systems during development.
- The process governing how the student team hands off work to the software team for production verification.

The following are out of scope for this document because they are not yet confirmed as governing rules rather than open questions or software design choices:

- Any formal industry standard (e.g., DO-178C) that may govern the review process itself — the concept document references it only as educational context, not as a stated compliance requirement. See `OI-1` in [OPEN-ISSUES.md](OPEN-ISSUES.md).
- Reviewer assignment, escalation, and platform-specific checklist criteria — not described in enough detail yet to state as rules.
- Internal HR or vendor-account policy (e.g., Atlassian's free-tier user limit) that does not govern the review process itself.


---

## 2. Rules

### 2.1 Review Artifacts and Audit Compliance

- **`BR-svn-diff-required`:** A formal code review's diff file must be generated from SVN, since an SVN-generated diff is a required review artifact.
  **Source:** RevView/OMNI Review Helper Application Concept document, Section 8.
- **`BR-review-package-exportable`:** Review records and checklists must remain producible and exportable in their original file format (Excel/CSV) so the existing review package can still be generated for audits.
  **Source:** same document, Sections 7–8.
- **`BR-diff-checklist-match`:** Every file included in a review's diff must match the files listed in that review's checklist.
  **Source:** same document, Section 7.3.
- **`BR-review-nine-parts`:** A single code review may consist of up to nine parts, spanning code/tools/test categories across up to three platforms.
  **Source:** same document, Section 2.3.
- **`BR-review-record-fields`:** A review record must capture, at minimum, the type of review, method, date, return date, and reviewers.
  **Source:** same document, Section 7.1. **Flagged:Needs_Review** the source document marks this information as possibly automatable, so which fields stay human-entered vs. system-derived may change — confirm with the client before treating the field list as fixed.

### 2.2 AI and Human Judgment

- **`BR-ai-human-override`:** Any AI-generated compliance suggestion or flagged issue must be approved or overridden by a human reviewer; AI must not replace reviewer judgment.
  **Source:** same document, Sections 5, 5.3.
- **`BR-author-owns-change-rationale`:** The engineering reason for a file change belongs to the author. AI may summarize objective diff content but must not invent or assert the reason for the change.
  **Source:** same document, Section 5.

### 2.3 IT and Access Constraints

- **`BR-no-student-prod-access`:** Students may not be added as users on Applied Avionics' internal network and may not be given direct access to the production Jira, SVN, or Jenkins instances for development or testing.
  **Source:** same document, Section 12. **Flagged:Needs_Review** confirm this is still current IT policy directly with the client/IT, since it drives the sandbox architecture for the whole project.

### 2.4 Student–Software Team Engagement

- **`BR-sprint-handoff-cadence`:** The student team must hand off each completed component to the software team for verification against production systems by the earlier of (a) the last day of the sprint, or (b) whenever the student team marks the feature complete.
  **Source:** same document, Section 13.
- **`BR-build-tagging`:** Every build handed to the software team for verification must be tagged with a demonstration and/or a README.
  **Source:** same document, Section 13.1.
- **`BR-discrepancy-next-sprint`:** Any discrepancy the software team finds during verification must be logged and addressed by the student team in the following sprint.
  **Source:** same document, Section 13.1.

_**Checklist:** Does every rule have a source? Could your client change it without asking you? Is it stated as one sentence about the business, rather than as a sentence about your software? Does any use case cite it, and if none does, is that correct?_
