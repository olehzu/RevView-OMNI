# Software Requirements Specification

**Project:** RevView/OMNI
**Team:** Team 8
**Client:** Sumalee Rodolph, AppliedAvionics
**Version:** 0.1

---

_**How to use this template.** Instructions appear in italic square brackets. Fill in underneath them and leave them in place until the document is stable._

_**What this document is, and what it is not.** The specification describes the external behavior of your system completely enough that a developer can build it and a tester can check it. What it is **not** is a container for everything you have written. Your glossary, vision and scope, use cases, and business rules are separate documents with their own identifiers, and this one **links to them rather than repeating them**._

_That makes the specification mostly a hub. Read that as a feature. One fact, one home: a business rule copied in here is a business rule that will disagree with `business-rules.md` by October, and nobody will notice which copy is right. The sections below that say "link to" are supposed to be short._

_What this document owns outright: the requirements that have no other home. Functional requirements that are not part of any use case, quality attributes, external interfaces, data requirements, operating environment, and constraints._

## Identifiers

_Every requirement in this document carries a name-based slug. Create only the spaces your project actually needs._

| Space | For | Example |
|---|---|---|
| `FR-<AREA>-<slug>` | Functional requirements outside any use case | `FR-SAVE-autosave-active` |
| `UI-<slug>` | User interface requirements | `UI-spa-views` |
| `SI-<slug>` | Software and system interfaces | `SI-llm-proxy-only` |
| `CI-<slug>` | Communications interfaces | `CI-email-notifications` |
| `DI-<slug>` | Data requirements | `DI-persist-graph` |
| `OE-<slug>` | Operating environment | `OE-supported-browsers` |
| `CO-<slug>` | Design and implementation constraints | `CO-single-application` |
| `AS-<slug>` / `DE-<slug>` | Assumptions and dependencies | `AS-supported-browser`, `DE-llm-service` |

_Quality attributes get one space per attribute, so the identifier says which kind of quality it is at the place it is cited: `USE-` usability, `PER-` performance, `SEC-` security, `SAF-` safety, `AVL-` availability, `ROB-` robustness, `SCA-` scalability, `INT-` interoperability, `MNT-` maintainability._

_Requirements cited from elsewhere keep their own identifiers: `UC-*` from [use-cases.md](use-cases.md), `BR-*` from [business-rules.md](business-rules.md), `BO-*`, `SM-*`, `FEAT-*` from [vision-and-scope.md](vision-and-scope.md)._

## Revision History

| Date | Version | Description | Author |
|---|---|---|---|
| 2026-09-25 | 0.1 | Initial draft of section 1, from vision-and-scope.md and the client interview notes | Oleh Zubariev |
| 2026-09-25 | 0.1 | Updated section 1 to match the filled-in vision-and-scope.md sections 2 through 4 | Oleh Zubariev |
| 2026-10-03 | 0.1 | Filled in section 9, Quality Attributes | Oleh Zubariev |

---

## 1. Introduction

### 1.1 The purpose of RevView/OMNI

RevView/OMNI is proposed for an internal aerospace software engineering team, at AppliedAvionics, that conducts formal code reviews for safety-critical avionics software. Today, authors manually assemble review information across Jira, SVN, and Jenkins, and complete separate checklists and review records, before a review can begin, and reviewers then move between those same materials to assess a change. This recurring administrative work takes time away from engineering assessment and creates opportunities for incomplete reviews, outdated source code under review, and missed reviewer notifications (see [vision-and-scope.md](vision-and-scope.md) sections 1.1, 1.2, and 2.1).

RevView/OMNI consolidates the review record, source and diff context, checklists, and build information into a single review workspace, so that authors, reviewers, and the review moderator or coordinator, the primary user classes described in [vision-and-scope.md](vision-and-scope.md) section 3.1, spend their time on the review itself rather than on assembling it. The application supports the current safety-critical review process but is not itself a safety-critical system; it is a coordination and evidence-management tool for the review workflow.

The project also serves as a senior design project for TCU students, who work with AppliedAvionics engineers to build it. Because students cannot access AppliedAvionics' production network, development uses isolated instances of Jira, SVN, and Jenkins populated with synthetic data, and AppliedAvionics' own software team validates the integrations against its production systems before the application is deployed internally.

### 1.2 The purpose of this document

This document describes the functional and nonfunctional requirements for RevView/OMNI. It serves as the reference for the project's requirements, defining the scope, functionality, and constraints for AppliedAvionics, the development team, and the course instructors.

This specification supports the MVP scope defined in [vision-and-scope.md](vision-and-scope.md) section 4.3: `FEAT-review-initiation`, `FEAT-context-assembly`, `FEAT-diff-and-source-prep`, `FEAT-checklist-mapping`, `FEAT-integrity-validation`, `FEAT-review-notification`, and `FEAT-evidence-retention`. `FEAT-admin-and-configuration`, AI-generated review summarization beyond assisting with evidence assembly, and full production-grade integration across every platform variant are explicitly out of scope for this release, for the reasons given in that section.

### 1.3 Document conventions

This document uses the identifier spaces listed under Identifiers above. Functional requirements that do not belong to a use case are written using the EARS (Easy Approach to Requirements Syntax) sentence shapes described in section 5.2, so that each one can be read only one way.

### 1.4 References

- [Project glossary](project-glossary.md)
- [Vision and scope](vision-and-scope.md)
- [Use cases](use-cases.md)
- [Business rules](business-rules.md)
- [Open issues](OPEN-ISSUES.md)
- [Client interview, 2026-09-09](client-meeting/client-interview-2026-09-09.md)
- [Client interview, 2026-09-18](client-meeting/client-interview-2026-09-18.md)
- [The Easy Approach to Requirements Syntax (EARS)](https://alistairmavin.com/ears/)

---

## 2. Overall Description

### 2.1 Product perspective

_[How this system relates to other systems and to the user's environment. Self-contained, or one component of something larger? Link to the product perspective section of your vision and scope and to your architecture's context diagram rather than redrawing them.]_

### 2.2 User classes and characteristics

_[The kinds of user, and what distinguishes them: frequency of use, technical skill, privilege level, whether they are inside or outside the client's organization. Link to the stakeholder profiles in your vision and scope; what belongs here is what affects the software's behavior, especially permissions.]_

### 2.3 Operating environment

_[The environment the software runs in: hardware, operating systems and versions, browsers, where users and servers are located, and any other software it has to coexist with.]_

_Examples:_

- _`OE-supported-browsers`: The system shall operate correctly on the current and previous major versions of Chrome, Firefox, Safari, and Edge._
- _`OE-server-platform`: The system shall run on a server running the current corporate-approved version of Linux._
- _`OE-access-paths`: The system shall permit access from the corporate intranet, from a VPN connection, and from Android and iOS phones and tablets._

### 2.4 Design and implementation constraints

_[Anything that limits the developers' options: corporate or regulatory policy, hardware limits, required languages or databases, coding standards, interfaces to other applications.]_

_Examples:_

- _`CO-database-engine`: The system shall use the corporate standard database engine._
- _`CO-language-version`: The backend shall be written in Java 21._
- _`CO-coding-standard`: Design, code, and maintenance documentation shall conform to the client's development standard._

_The constraint students forget: **who maintains this after you graduate, and what do they already know how to run?** If the answer is one person who knows Python, a Spring Boot service is a constraint violation nobody wrote down._

### 2.5 Assumptions and dependencies

_[An assumption is a factor you believe true without proof, which would change these requirements if it turned out false. A dependency is something outside your control that the project relies on: an external API, a third-party library, a change someone else has to make.]_

_Examples:_

- _`AS-supported-browser`: Users access the system with a browser that supports the ECMAScript version the frontend targets._
- _`DE-payroll-integration`: Operation depends on changes being made in the Payroll System to accept payment requests for meals ordered through this system._

---

## 3. Project Glossary

_[Link only. The glossary is [project-glossary.md](project-glossary.md).]_

## 4. Vision and Scope

_[Link only. Business requirements, objectives, metrics, and scope live in [vision-and-scope.md](vision-and-scope.md).]_

---

## 5. Functional Requirements

### 5.1 Use cases

_[Link to [use-cases.md](use-cases.md). Most of your system's behavior is specified there, as use cases, and it does not get restated here.]_

### 5.2 Non-use-case functional requirements

_[Behavior that is real, testable, and belongs to no single use case: autosave, validation applied everywhere, notification, authorization, audit logging. If you find yourself writing the same step into six use cases, it belongs here instead._

_Group them under sub-headings by concern, and write each one using an [EARS](https://alistairmavin.com/ears/) shape so that it cannot be read two ways:_

- _**Ubiquitous:** The `<system>` shall `<response>`._
- _**Event driven:** When `<trigger>`, the `<system>` shall `<response>`._
- _**State driven:** While `<in a state>`, the `<system>` shall `<response>`._
- _**Optional:** Where `<feature is included>`, the `<system>` shall `<response>`._
- _**Unwanted behavior:** If `<precondition>`, then the `<system>` shall `<response>`._

_Example: `FR-SAVE-autosave-active`: While a student is editing a weekly activity report during an active week, the system shall persist the draft every 30 seconds._

_**Every requirement here needs an oracle.** If you cannot say how a tester would tell whether it holds, it is not a requirement yet.]_

---

## 6. Business Rules

_[Link only, to [business-rules.md](business-rules.md). Business rules are a rich source of requirements because they dictate properties the system must have in order to conform to them, but the rules themselves are properties of the client's business, not of your software, and they have their own document.]_

---

## 7. Data Requirements

### 7.1 Business domain model

_[The entities in the problem domain and how they relate, as a mermaid class diagram. Model the **business**, not your database schema: this is what the client would recognize, before any decision about tables or persistence.]_

    ```mermaid
    classDiagram
      class Team {
        +String name
      }
      class Student {
        +String email
      }
      Team "1" --> "*" Student : has
    ```

### 7.2 Data dictionary

_[Each entity's fields, with data type, allowed values, defaults, and validation rules. Where a use case already specifies a field's validation in its Associated Information, cite the use case instead of repeating it.]_

### 7.3 Reports

_[Any report the system generates: who reads it, what it contains, how often, and in what format. Reports are where clients discover late that a field they need was never captured, so specify them early.]_

### 7.4 Data acquisition, integrity, retention, and disposal

_[Where the data comes from, how it is kept correct, how long it is kept, and how it is destroyed. If your system holds anything about students or other identifiable people, this section is not optional, and its content is usually a business rule you should cite rather than invent.]_

---

## 8. External Interface Requirements

### 8.1 User interfaces

_[The user-facing surfaces, at requirement level: which views exist, standards they must conform to, accessibility requirements. Link to wireframes or prototypes rather than describing pixel layouts.]_

### 8.2 Hardware interfaces

_[Any hardware the system talks to, or "none".]_

### 8.3 Software interfaces

_[Other software systems yours connects to: what crosses the boundary, in which direction, in what format, and what happens when the other side is unavailable.]_

### 8.4 API document

_[Link to your API documentation. It is generated from the code, so link it rather than transcribing endpoints that will be stale within a week.]_

### 8.5 Communications interfaces

_[Email, notifications, messaging, and the protocols involved.]_

---

## 9. Quality Attributes

_[How well the system does what it does. **This is the section that decides whether your client is happy with software that meets every functional requirement**, so do not treat it as a formality.]_

_The rule for every entry: an adjective is not a requirement. "Fast", "easy", "secure", and "user-friendly" are the starting point of a conversation, not the end of one. Each entry needs a number and a way to measure it._

_Write one subsection per attribute your project actually has, and say "not applicable" with a reason for the ones it does not. An explicit "not applicable" is information; silence is not._

### 9.1 Usability

`USE-pilot-confidence`: Reviewer and author confidence in the completeness and usability of a generated review package shall show a positive trend across repeated pilot reviews, measured by the short post-review feedback described in `SM-user-satisfaction` ([vision-and-scope.md](vision-and-scope.md) section 2.3). No numeric baseline exists yet because the pilot has not run; the first pilot's result becomes the baseline for later comparison.

No accessibility standard (for example WCAG) has been requested by AppliedAvionics, and none is assumed here. This is an internal tool for a small engineering team rather than a public product, but the team does not actually know whether AppliedAvionics has an internal accessibility policy that applies. Tracked as `OI-13` in [OPEN-ISSUES.md](OPEN-ISSUES.md).

### 9.2 Performance

`PER-review-setup-time`: The median time from review creation to ready-for-review status shall fall from the current baseline of approximately 20 minutes of manual preparation (excluding Jenkins build time) to approximately 9 to 10 minutes with automation alone, and to approximately 2 to 5 minutes when AI-assisted drafting is enabled, measured as specified in `SM-review-setup-time` ([vision-and-scope.md](vision-and-scope.md) section 2.3).

Notification latency (`SM-notification-latency`) is also a performance concern, but the specification cannot yet give it a number: the success metric calls for "a measurable reduction" without a baseline or target value. Tracked as part of `OI-5` in [OPEN-ISSUES.md](OPEN-ISSUES.md), since it depends on the same review-volume data that issue is already chasing.

### 9.3 Security

`SEC-role-based-review-access`: The system shall restrict read and write access to a review package's diff, source context, checklist, findings, and review record to that review's assigned author, reviewer(s), and moderator, matching the access columns already specified in every use case's Associated Information table ([use-cases.md](use-cases.md)). Verified by: an access-control test that attempts each operation as a user who is not a participant on the review and confirms it is refused.

`SEC-no-production-credentials-in-development`: While the project is developed and tested, the system and its development environment shall hold no AppliedAvionics production Jira, SVN, or Jenkins credentials; only sandbox credentials are used, with production credentials handed over at project handoff (client interview, 2026-09-09, section 9). Verified by: a configuration and secrets review before each release to the sandbox or, later, to production.

### 9.4 Safety

`SAF-not-applicable`: RevView/OMNI supports the review of safety-critical avionics software, but the application itself is not a safety-critical system; it is a coordination and evidence-management tool, and a failure in it does not directly cause an unsafe aircraft condition ([vision-and-scope.md](vision-and-scope.md) section 2.1). The safety-critical judgment stays with the human reviewer regardless of what the tool does.

### 9.5 Availability

No uptime target or announced-maintenance-window expectation has been stated by AppliedAvionics, and none is assumed here. Tracked as `OI-14` in [OPEN-ISSUES.md](OPEN-ISSUES.md).

### 9.6 Robustness

`ROB-incomplete-package-blocked`: While a review package is being validated, if a required review section, file description, revision reference, diff coverage, or checklist item is missing, the system shall flag the specific gap and shall not mark the package ready for reviewer notification, per `UC-REV-validate-package` steps 2 through 5 and its extensions 2a and 3a ([use-cases.md](use-cases.md)). Verified by: the test cases already implied by that use case's extensions, one missing section and one incomplete diff.

### 9.7 Scalability, interoperability, maintainability

`SCA-concurrent-reviews`: The system shall support at least 6 concurrently open reviews and 5 to 6 active users without degraded response, matching the review volume AppliedAvionics reported in the 2026-09-18 client interview ([client-interview-2026-09-18.md](client-meeting/client-interview-2026-09-18.md) section 7). This is a floor taken from current observed volume, not a measured load target; raised as part of `OI-5` since the team still does not know the busiest-case volume.

`INT-sandbox-tool-integration`: The system shall exchange data with Jira, SVN, and Jenkins, first the sandbox instances and later AppliedAvionics' production instances, without requiring a configuration change to those tools themselves ([vision-and-scope.md](vision-and-scope.md) section 4.1; client interview, 2026-09-09, section 10). Verified by: the integration test suite passing against the sandbox instances without modification to their setup.

`MNT-single-maintainer`: The system shall be operable and maintainable using only Python and JavaScript knowledge, with no additional language or framework required to deploy, configure, or extend it, so that Sumalee Rodolph can run it alone after the team graduates ([vision-and-scope.md](vision-and-scope.md) section 4.4; client interview, 2026-09-18, section 11). Verified by: a deployment dry run performed from the written setup documentation alone, by someone outside the development team.

---

## 10. Internationalization and Localization

_[Languages, character sets, time zones, date and currency formats. If the answer is a single locale, say so and say why, because that is a real constraint on who can use the system.]_

---

## 11. Other Requirements

_[Anything real that fits nowhere above: legal, licensing, installation, training, documentation. Delete this section if it is empty rather than leaving it as a placeholder.]_

---

## Working this document with your agent

_[Delegate: converting prose requirements into EARS shapes; checking that every `UC-*`, `BR-*`, and `FEAT-*` cited here exists in the document that owns it; finding functional requirements that appear in several use cases and should be lifted into section 5.2; drafting an oracle for a quality attribute you have stated only as an adjective._

_Keep human: the numbers. Every threshold in section 9 is a commitment somebody has to live with, and an agent will supply a plausible one (99.9% uptime, 200ms response) that nobody asked for and no one can meet. A number in this document either came from your client, from a measurement, or from a decision your team made deliberately and can defend._

_**The specific failure to watch for: invented precision.** A generated specification reads as authoritative at exactly the points where it is guessing. Check every number, every browser version, every retention period against something real, and put the ones you cannot verify in [OPEN-ISSUES.md](OPEN-ISSUES.md) instead of leaving a confident guess in the document your team will build from.]_
