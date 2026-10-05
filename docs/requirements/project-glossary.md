# Project Glossary

**Project:** _RevView/OMNI_  
**Team:** _Team 8_  
**Client:** _Sumalee Rodolph, Applied Avionics_  
**Version:** 0.1

---

_**How to use this template.** Instructions appear in italic square brackets. Fill in underneath them and leave them in the file until the document is stable._

_**What this document is for.** Every project has words that mean something specific inside the client's organization and something else outside it, or nothing at all. This file fixes one word to one concept, and commits the team, the client, and the AI teammate to using it. That shared vocabulary is called a **ubiquitous language**: the same term in the client conversation, in the vision and scope, in the use cases, in the class names, and in the database columns._

_**Why the glossary is the first artifact you write and the last one you finish.** It is the cheapest document to start, because your client hands you the terms in the first meeting whether you ask or not, and it is the one that keeps paying: every later document cites it instead of redefining things._

## Why this matters when an agent writes your code

_[Read this once, then delete this section when the document goes stable.]_

_If two words in your project mean the same thing and nothing says so, your team will use both. So will your agent. You will end up with a `Team` class and a `Group` table, a `submitReport` endpoint and a `war_entry` record, and every one of those pairs is a bug waiting for the week you try to join them._

_An agent cannot resolve this on its own. Asked to add a feature, it reads what is in the repository and imitates it. If the repository is inconsistent it will faithfully reproduce the inconsistency, and it will invent a plausible synonym for anything the repository never names. A glossary in the repository is the only thing that stops it, because the repository is the whole of the agent's memory of your project._

_The other half is human. When your client says "cycle" in one sentence and "sprint" in the next, that is your signal to ask which one they mean, in the meeting, while they are in front of you. An agent reading the transcript later cannot ask._

## The entries that earn their place

_[The temptation is to define words your teammates already know. Skip those. The entries worth writing are:]_

- _**Terms two stakeholders use differently.** The highest-value entry in any glossary. In airline statistics, the International Civil Aviation Organization says **city-pair** and the International Air Transport Association says **O and D**, for the same thing; the two bodies also say **traffic by flight stage** and **segment traffic** for another. A team that misses this builds a report that silently mixes them._
- _**Terms that sound generic but are not.** "Active", "submitted", "complete", "week". Ask what makes a record active and you often find a business rule nobody had stated._
- _**The client's acronyms**, spelled out, including the ones they use so fluently they have forgotten they are acronyms._
- _**Terms you invented** that the client does not use. Record them, then consider dropping them in favor of the client's word._

_Ask the client directly: "Is there a word your team uses here that I would not guess the meaning of?"_

## Conventions

_[The **term itself is the identifier**. There is no separate numbering scheme, because a glossary entry already has a unique, meaningful name: the word. Cite a term by writing it, and keep the spelling identical everywhere it appears._

_Rules:_

- _One entry per concept. If two words mean the same thing, pick one, define it, and list the other as a synonym under it rather than giving it its own entry._
- _Alphabetical order, so a reader can find a term without searching._
- _Define the concept, not the implementation. "A weekly record of what a student did" is a definition; "a row in the `war` table" is not._
- _Use the client's word when the client has one. You are joining their world, not renaming it._
- _If a term has a meaning outside this project that differs from the one here, say so explicitly.]_

## Revision History

| Date | Version | Description | Author |
|---|---|---|---|
| 2026-09-12 | 0.1 | Initial terms from the client brief and first client meeting | Ethan Nguyen |

---

## Definitions

_[One `###` heading per term, alphabetical. Follow the heading with a definition of one to three sentences. Add **Synonyms**, **Not to be confused with**, or **Source** lines where they help. Where a term only makes sense with an example, give one.]_

### AI Assistance

The optional use of artificial intelligence to draft objective change summaries, describe file changes, or flag simple compliance concerns. Its output must remain reviewable and editable because AI Assistance supports, but never replaces, the judgment of the Author or Reviewer.

**Not to be confused with:** Automation, which also includes deterministic operations that do not use artificial intelligence.

**Source:** *RevView/OMNI Review Helper Application Concept*, sections 5 and 6.

### AI Involvement Level

The configured degree of AI Assistance: **Level 1: None**, **Level 2: Necessary**, or **Level 3: Helper**. Level 2 is the recommended starting point because it uses AI only where it clearly reduces manual effort.

**Source:** *RevView/OMNI Review Helper Application Concept*, section 5.4.

### Author

The person who prepares and starts a Formal Review by verifying gathered information, completing fields that require human knowledge, selecting Reviewers, and approving any generated content. The Author remains responsible for the engineering reason behind a change.

### Automation

The system-driven completion of repetitive review work, such as retrieving Jira information, locating an SVN Branch, generating a Diff, populating review fields, starting a Jenkins Build, sending Notifications, or assembling a Review Package.

**Not to be confused with:** AI Assistance, which is only one optional form of support within the broader automation strategy.

### Changed File

A source-code, tool, test, or related file whose contents changed and are included in a Formal Review. Every Changed File should be represented consistently in the Diff and applicable Review Checklist.

### Checklist Item

One review criterion within a Review Checklist. A Checklist Item may receive a Compliance Result, supporting reason, human decision, and related Review Comments.

### Checklist Submission

The event in which a Reviewer submits or updates a Review Checklist. It notifies the appropriate Author and Moderator, and the Moderator is notified when all required Review Checklists have been submitted.

### Code/Tools/Tests Category

One of the three client-used categories for organizing Changed Files and Review Checklist sections: production code, supporting tools, or tests. A Formal Review may contain several of these categories across multiple Platforms.

### Compliance Result

A preliminary or human-confirmed determination for a Checklist Item: **Compliant**, **Not compliant**, **Not applicable**, or **Needs reviewer judgment**. An automatically suggested result must include a reason when applicable and may be approved or overridden by a Reviewer.

### Diff

A representation of the changes between SVN Revisions that Reviewers use to examine a Formal Review. RevView/OMNI generates the required Diff and prompts the Author to verify that it includes the expected Changed Files.

**Synonyms:** Diff file; SVN-generated Diff.

**Not to be confused with:** a Changed File, which is one of the files compared by the Diff.

### Formal Review

The controlled process in which assigned people evaluate software changes and supporting evidence against required review criteria. It includes Changed Files, Diffs, Review Checklists, Review Comments, Build results, decisions, and retained Review Artifacts.

**Synonym:** Review, used conversationally in the client concept.

**Not to be confused with:** an informal code review that does not produce the required artifacts and traceability.

### In Close Out

The Jira workflow status to which the associated Jira Ticket is moved when the Moderator closes the Formal Review.

**Not to be confused with:** Review Closure, which is the broader process that produces the final Review Package and notifications.

### Integration Layer

The boundary through which RevView/OMNI exchanges authentication, field, branch, revision, Diff, Build, and workflow information with Jira, SVN, and Jenkins. The client Software Team verifies this boundary against the Production Environment during iterative testing.

### Jenkins Build

An execution of the software build and test process through Jenkins for the changes associated with a Formal Review. Its status and results are linked to the Review and retained as Review Artifacts when required.

**Synonym:** Test Build, when referring to the Jenkins build run for review verification.

### Jira Ticket

The Jira work item associated with the software changes under Formal Review. It provides the ticket identifier, title, description, status, linked requirements, and other metadata used to create and trace the Review.

### Minimum Viable Product

The smallest semester deliverable that provides the core RevView/OMNI workflow: Review Creation from a Jira Ticket, SVN Diff generation, a Unified Review Workspace, basic Automation and AI Assistance, Notifications, and Review Closure.

**Synonym:** MVP. Spell it out on first use in a document.

### Minor Issue

A low-value problem that Automation or AI Assistance may identify before Reviewers begin, such as inconsistent indentation, blank lines, an outdated copyright header, a formatting inconsistency, or a simple style violation.

### Moderator

The participant who coordinates the Formal Review and initiates Review Closure after the required Review Checklists are submitted.

**Needs client confirmation:** the Moderator's complete permissions and whether this role may also be filled by an Author or Reviewer.

### Notification

An alert sent to a Relevant User after a review event, such as Review Start, a new Review Comment, Checklist Submission, or Review Closure.

**Needs client confirmation:** whether Notifications are in-app, email-based, or both.

### Platform

A client-defined avionics software target or product area for which a separate Review Checklist may be required. A Formal Review may affect up to three Platforms.

**Needs client confirmation:** the official Platform names and the rule used to determine which Platforms a Jira Ticket affects.

### Production Environment

The client's internal Jira, SVN, Jenkins, repositories, and related systems used for real avionics software work. Students cannot directly access this environment.

**Not to be confused with:** Sandbox Environment.

### Relevant User

An Author, Reviewer, Moderator, or other authorized participant who must receive a Notification about a particular Formal Review event. Which users are relevant depends on the event and their assigned responsibilities.

### Review Artifact

A file, record, or result that must be captured and possibly preserved for a Formal Review. Review Artifacts include the Review Record, Review Checklists, Diff, Build and test results, and additional files supplied by the Author.

### Review Checklist

A structured set of criteria used to evaluate files or changes in a Formal Review. RevView/OMNI may prefill information that can be determined reliably, but judgment-based items remain for a person to complete or approve.

**Synonyms:** Checklist; Code Review Checklist.

### Review Closure

The process that completes a Formal Review by consolidating results, updating the Review Record, assembling the Review Package, notifying Relevant Users, and moving the Jira Ticket to **In Close Out**.

**Needs client confirmation:** whether “complete,” “closed,” and **In Close Out** represent distinct workflow states.

### Review Comment

Feedback recorded by a Reviewer about a change, Checklist Item, or other Review Artifact. It should retain enough context to identify the applicable Changed File, line or code location, checklist criterion, and Jira Ticket.

### Review Creation

The process of establishing a Formal Review from a selected Jira Ticket. RevView/OMNI gathers available Jira and SVN information, identifies Changed Files, generates Diffs, and allows the Author to verify the prepared information before Review Start.

### Review Package

The complete collection of required Review Artifacts assembled at Review Closure. It preserves the information and original file types needed by the client's existing audit process even though users perform the Review through a new interface.

**Not to be confused with:** Review Record, which is one artifact within the Review Package.

### Review Record

The formal record of the identifying, administrative, participant, and outcome information for a Formal Review. RevView/OMNI populates fields automatically where possible while retaining human input for information it cannot determine reliably.

### Review Round

A distinct cycle of review activity associated with a Formal Review, potentially created after Reviewer-requested changes produce new Revisions and Diffs. Each Review Round remains connected to the earlier review history.

**Needs client confirmation:** the exact event that begins a new round and the artifacts required for each round.

### Review Start

The event that sends a prepared Formal Review to its assigned Reviewers after the Author verifies the generated information and completes required human-input fields.

**Needs client confirmation:** the exact fields and approvals required before Review Start.

### Reviewer

A person assigned to evaluate the changes and evidence included in a Formal Review. The Reviewer examines the code, Diff, Jira Ticket, Review Checklist, Build results, and related files, then records comments and final judgments.

### Reviewer Assignment

The association of one or more Reviewers with a Formal Review. Adding a Reviewer in RevView/OMNI should also add that person to the Jira Ticket, while adding a Reviewer through Jira should notify that person in RevView/OMNI.

### Revision

A version identifier recorded by SVN for repository content. RevView/OMNI captures the current Revision and the Revision used at Review Creation so that later Diffs can be generated after requested changes.

### RevView/OMNI

The web application Team 8 is developing to centralize and automate repetitive parts of the formal review process for safety-critical avionics software while preserving human judgment, traceability, and required Review Artifacts.

**Needs client confirmation:** whether **RevView/OMNI** is the complete official name and what **OMNI** means.

### Safety-Critical Avionics Software

Software used in aircraft or spacecraft contexts where failures may have serious safety consequences and development therefore requires disciplined assurance, review, testing, and traceability. RevView/OMNI supports a review process for this software, but the student project itself is not safety-critical.

### Sandbox Environment

An isolated development and testing environment containing representative Jira, SVN, and Jenkins instances and no route to the client's internal network. It uses Synthetic Data so Team 8 can build realistic integrations without production access or proprietary information.

**Synonyms:** Sandbox; Mock Environment.

**Not to be confused with:** Production Environment.

### Software Team

The client's internal engineering team that can access the Production Environment. It reviews Team 8's Integration Layer, tests completed components against designated production test areas, and reports differences for correction.

### Subversion

The version-control system used by the client's current review process. RevView/OMNI uses it to locate branches, identify Changed Files and Revisions, capture repository locations, and generate required Diffs.

**Synonym:** SVN. Spell out Subversion on first use in a document.

### SVN Branch

A development branch in Subversion containing changes associated with a Jira Ticket or Formal Review. RevView/OMNI attempts to locate the matching branch or branches from the Jira Ticket name and available repository information.

### Synthetic Data

Non-proprietary test information that mirrors the structure and behavior of the client's workflow without copying production content. It includes representative Jira tickets, placeholder checklists, SVN history, sample Diffs, and Build results.

**Synonym:** Mock Data.

### Traceability

The ability to follow the relationships among a software change, Jira Ticket, SVN Branch, Revisions, Changed Files, Diffs, requirements, Reviewers, Review Comments, Review Checklists, Build results, Review Rounds, and Review Package.

### Unified Review Workspace

The central RevView/OMNI interface in which users access source code, Jira Ticket details, Changed Files, Diffs, Review Checklists, Review Comments, Build status, and supporting files without managing several disconnected resources.

### Version History

The preserved sequence of changes to review information, Review Artifacts, Revisions, and Review Rounds. It allows users to determine what changed, when it changed, and which version was reviewed.
