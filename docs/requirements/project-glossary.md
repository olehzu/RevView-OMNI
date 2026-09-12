# Project Glossary

**Project:** _RevReview OMNI_  
**Team:** _Team 8_  
**Client:** _[Sumalee Rodolph](https://www.linkedin.com/in/sumalee-rodolph/)_ - Applied Avionics  
**Version:** 0.1

---

_**How to use this template.** Instructions appear in italic square brackets. Fill in underneath them and leave them in the file until the document is stable._

_**What this document is for.** Every project has words that mean something specific inside the client's organization and something else outside it, or nothing at all. This file fixes one word to one concept, and commits the team, the client, and the AI teammate to using it. That shared vocabulary is called a **ubiquitous language**: the same term in the client conversation, in the vision and scope, in the use cases, in the class names, and in the database columns._

_**Why the glossary is the first artifact you write and the last one you finish.** It is the cheapest document to start, because your client hands you the terms in the first meeting whether you ask or not, and it is the one that keeps paying: every later document cites it instead of redefining things._

## Why this matters when an agent writes your code

_[Read this once, then delete this section when the document goes stable.]_

_If two words in your project mean the same thing and nothing says so, your team will use both. So will your agent. You will end up with inconsistent names in the source code, database, API, and documentation._

_The glossary gives the team, client, and AI-assisted development process one shared vocabulary._

## The entries that earn their place

_[The glossary should focus on project-specific terms, ambiguous words, client acronyms, and concepts that may otherwise be named inconsistently.]_

## Conventions

_[The **term itself is the identifier**. There is no separate numbering scheme, because a glossary entry already has a unique, meaningful name._

_Rules:_

- _One entry per concept._
- _Alphabetical order._
- _Define the concept, not the implementation._
- _Use the client's terminology whenever possible._
- _If two terms mean the same thing, select one preferred term and list the other as a synonym._
- _If a term still needs clarification from the client, do not invent a definition; mark it for confirmation instead._

## Revision History

| Date | Version | Description | Author |
|---|---|---|---|
| 2026-09-12 | 0.1 | Initial glossary based on the first client meeting and project concept document | Team 8 |

---

## Definitions

### AI Assistance

The optional use of artificial intelligence to reduce repetitive review work, such as summarizing changes, drafting file-change descriptions, or identifying simple compliance concerns. AI Assistance supports the review process but does not replace human engineering judgment.

**Not to be confused with:** automated rules, which may perform deterministic checks without generative AI.

---

### Author

The person responsible for preparing and starting a code review. The Author provides or verifies review information, ensures the required review materials are available, selects Reviewers, and starts the Review.

---

### Build

An execution of the project's build and test process used to verify software changes before or during a Review.

**Preferred term when referring specifically to Jenkins:** Jenkins Build.

---

### Changed File

A source code, tool, test, or related file whose contents have changed and are included in a Review. Changed Files are identified through the version-control information associated with the Review.

---

### Checklist

A structured set of review criteria that must be evaluated as part of the formal review process. Some Checklist information may be populated automatically, while judgment-based items remain the responsibility of a human Reviewer.

**Synonyms:** Review Checklist, Code Review Checklist.

**Preferred term:** Review Checklist when referring specifically to the checklist used during a Review.

---

### Compliance Check

An evaluation of a file or change against a review requirement or Checklist criterion. The system may provide preliminary results, but judgment-based decisions remain subject to human review.

Possible preliminary results discussed with the client include:

- Compliant
- Not compliant
- Not applicable
- Needs reviewer judgment

---

### Diff

A representation of the changes between software revisions used during a Review. The system should generate required Diffs from SVN and associate them with the corresponding Changed Files.

**Not to be confused with:** the source file itself.

---

### Human Review

The evaluation of software changes by an engineer or other authorized Reviewer. Automation and AI Assistance may support Human Review, but final engineering judgment remains with people.

---

### In Close Out

A Jira workflow status used when the formal Review has been completed and the Review is moving through its closing activities.

The application is expected to move the associated Jira Ticket to **In Close Out** when the Review is closed.

---

### Jenkins

The build automation system used as part of the existing review workflow. The new application is expected to integrate with Jenkins to start or obtain Builds and associate their results with Reviews.

---

### Jenkins Build

A Build executed through Jenkins for the software associated with a Review. Where applicable, the application should make the result of the Jenkins Build available from the Review workspace.

---

### Jira

The issue-tracking system used to manage the work associated with software changes. The application will use Jira information as one of the starting points for creating a Review.

---

### Jira Ticket

The Jira work item associated with the software changes being reviewed. A Review may be started by selecting a Jira Ticket and retrieving information such as its identifier, title, description, status, requirements, and related metadata.

---

### Moderator

A participant responsible for coordinating or closing parts of the formal Review process. Based on the current project concept, the Moderator receives Review status information and can initiate Review Closure.

**Needs client confirmation:** the complete responsibilities and permissions of the Moderator have not yet been defined.

---

### Production Environment

The client's actual internal Jira, SVN, Jenkins, and related systems used for real avionics development work.

Students will not have direct access to the Production Environment during development.

**Not to be confused with:** Sandbox Environment.

---

### Review

The formal process in which software changes and their supporting information are evaluated by one or more Reviewers. A Review includes software changes, review criteria, supporting artifacts, comments, and results while preserving the human judgment and traceability required by the client's process.

---

### Review Artifact

A file, record, or result that forms part of the formal Review and may need to be preserved for traceability or audit purposes.

Examples include:

- Review Record
- Review Checklist
- Diff
- Build and test results
- Additional files supplied by the Author

---

### Review Checklist

A Checklist used by Reviewers to evaluate the files and changes included in a Review. The application may automatically populate information that can be obtained from connected systems, while judgment-based fields remain for humans to complete.

**Synonyms:** Checklist, Code Review Checklist.

---

### Review Closure

The process of completing a Review after the required review work has been performed. Review Closure includes consolidating results, updating the Review Record, gathering required Review Artifacts, generating the Review Package, notifying relevant users, and updating the Jira Ticket as required.

---

### Review Package

The complete collection of Review Artifacts produced and preserved for a completed Review. It supports traceability and the client's existing audit process.

The package may include the Review Record, Review Checklists, Diff files, Build results, and supporting files.

---

### Review Record

The formal record containing information about a Review. The system should automatically populate fields where possible while preserving fields that require human input.

**Not to be confused with:** Review Package, which contains the Review Record along with other Review Artifacts.

---

### Reviewer

A person assigned to evaluate the changes included in a Review. Reviewers inspect relevant code, Diffs, Jira information, Review Checklists, and supporting material and provide comments or judgments as required.

---

### Sandbox Environment

An isolated development and testing environment containing representative Jira, SVN, and Jenkins systems and synthetic project data. It allows the student team to develop and test integrations without connecting to the client's Production Environment.

**Synonyms:** Sandbox, Mock Environment.

**Preferred term:** Sandbox Environment.

---

### SVN

**Subversion (SVN)** is the version-control system used by the client's current review process. The application will integrate with SVN to locate relevant branches, determine changed files and revisions, obtain repository information, and generate Diffs.

---

### SVN Branch

A branch within SVN containing software changes associated with a Jira Ticket or Review. The application should attempt to locate the appropriate SVN Branch when a Review is created.

---

### Traceability

The ability to preserve and follow the relationship between a software change and its associated Jira Ticket, revisions, Review Artifacts, comments, Build results, Reviewers, and Review history.

Maintaining Traceability is a key requirement because the system supports a formal avionics software review process.

---

### Unified Review Workspace

The application's central interface for performing a Review without requiring users to work across several disconnected tools and documents.

The workspace is expected to bring together information such as source code, Jira details, Changed Files, Diffs, Review Checklists, comments, and Build status.

---

## Terms Requiring Client Confirmation

The following terms or distinctions were identified during the initial project discussion but require additional clarification before they should become stable glossary definitions:

- **RevReview OMNI vs. RevView/OMNI** — confirm the official project/product name and spelling.
- **Moderator** — confirm all responsibilities and permissions.
- **Review type** — determine the different types of Reviews supported by the client's process.
- **Review method** — clarify what values or methods are currently used.
- **Review round** — confirm when a new round begins and how rounds are identified.
- **Reviewer assignment** — determine whether Reviewers have different roles or approval authority.
- **Review completion** — establish the exact business rule that determines when a Review is considered complete.
- **Review closure** — confirm whether "complete," "closed," and "In Close Out" represent separate states.
