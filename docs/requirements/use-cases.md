# Use Cases

**Project:** RevView/OMNI
**Team:** Team 8
**Client:** Sumalee Rodolph - Applied Avionics
**Version:** 0.1

---

_**How to use this template.** Instructions appear in italic square brackets. Fill in underneath them and leave them in place until the document is stable._

_**What a use case is.** One goal a user can accomplish with your system, written as the dialogue between the actor and the system, including what happens when it goes wrong. It is the unit of work in this course: one use case becomes one issue, one branch, one pull request, and one set of tests._

_**Why the use case and not the user story.** You will meet user stories in industry, and they are a good planning tool: "As a student, I want to submit my report so that I get credit." A story is deliberately under-specified, because it is a **placeholder for a conversation** that happens later, between people. That is exactly the wrong property when the thing building your code is an agent that will implement precisely what the specification says and never ask what you meant. Use stories to plan and prioritize. Build against use cases._

_The difference that matters is the parts a story does not have: preconditions, the step-by-step flow, and above all the **extensions**, which is where the failure paths live. Most defects your team ships this semester will be in a path nobody wrote down._

## Identifiers

Use cases are identified as `UC-<AREA>-<slug>`, where the area code groups related functionality and the slug is coined from the goal. The RevView/OMNI use cases below map to the product features documented in [vision-and-scope.md](vision-and-scope.md).

## Revision History

| Date | Version | Description | Author |
|---|---|---|---|
| 2026-09-25 | 0.1 | Initial use cases for RevView/OMNI review-preparation, review, and closure workflow | Cong Le |

---

## 1. Introduction

### 1.1 Purpose

This document defines the primary goals users can accomplish with RevView/OMNI in enough detail for implementation and testing. It translates the vision and scope into operational use cases that describe how an author prepares a review, how a reviewer receives and evaluates it, and how the system retains evidence for later audit review.

### 1.2 Scope

This document covers the feature areas identified in [vision-and-scope.md](vision-and-scope.md): review initiation, context assembly, diff and source preparation, checklist mapping, integrity validation, review notification, and evidence retention. It does not cover production deployment beyond the internal system boundary or details of a final production network configuration.

---

## 2. Use Case Template

**UC ID and Name.** The identifier plus a concise name stating the value this use case provides to a user.

**Created By** and **Date Created.** Who wrote it and when.

**Primary and Secondary Actors.** The initiator and supporting participants in the interaction.

**Trigger.** The event that begins the use case.

**Description.** The reason for and outcome of the use case.

**Preconditions.** Facts that must already be true before the use case starts.

**Postconditions.** The state of the system at successful completion.

**Main Success Scenario.** The actor and system steps under expected conditions.

**Extensions.** Alternative acceptable paths and expected error handling.

**Priority.** Implementation priority.

**Frequency of Use.** Estimated usage rate.

**Business Rules.** The `BR-*` identifiers that govern the behavior.

**Associated Information.** Data fields, validations, and operational constraints relevant to the use case.

**Related Use Cases.** Other use cases this one depends on or is invoked by.

**Assumptions.** Conditions assumed to be true during execution.

**Open Issues.** Missing details that should be confirmed with the client.

---

## 3. Use Case List

| Area code | Feature area | Use cases |
|---|---|---|
| `REV` | Review package creation and validation | `UC-REV-create-review`, `UC-REV-assemble-materials`, `UC-REV-validate-package` |
| `NOT` | Review notification and coordination | `UC-NOT-notify-reviewers` |
| `ASS` | Reviewer assessment and findings | `UC-ASS-assess-review-section`, `UC-ASS-record-findings` |
| `CLS` | Review closure and evidence retention | `UC-CLS-close-review` |

---

## 4. Use Cases

### `UC-REV-create-review`: Create a review package

**UC ID and Name:** `UC-REV-create-review`: Create a review package
**Created By:** Cong Le
**Date Created:** 2026-09-25
**Primary Actor:** author
**Secondary Actors:** reviewer, moderator
**Trigger:** The author chooses to start a formal review for a software change.
**Description:** The author creates a review package for a specific change, selects the affected platform and review sections, and begins the review-preparation workflow.

**Preconditions:**

- PRE-1. The author is authenticated and authorized to create review packages for the selected project or platform.
- PRE-2. A Jira ticket or equivalent change record exists for the software change under review.
- PRE-3. The selected platform and review sections have been defined in the system configuration or review template.

**Postconditions:**

- POST-1. A review package record exists with a unique identifier, author, change context, platform, and selected sections.
- POST-2. The review package is ready for material assembly and validation.

**Main Success Scenario:**

1. The author selects the software change to review and chooses the project or work item from Jira.
2. The system displays candidate review sections and required checklist templates based on the selected platform and review scope.
3. The author selects the applicable sections and confirms the review metadata.
4. The system creates the review record and assigns a unique review identifier.
5. The system begins collection of ticket data, affected files, repository references, and relevant diff information.
6. The system stores the review state as “In preparation” and displays the package to the author.
7. Use case ends.

**Extensions:**

- **4a. The change record is missing or incomplete:**
    - 4a1. The system prompts the author to add or correct the Jira ticket or description.
    - 4a2. The author updates the required metadata and returns to step 4.
- **3a. The author chooses a platform or section not supported by the configuration:**
    - 3a1. The system rejects the invalid selection and lists valid options.
    - 3a2. The author chooses a valid combination and resumes at step 4.

**Priority:** High
**Frequency of Use:** Frequent; each review begins with this flow.
**Business Rules:** `BR-review-package-required`, `BR-platform-section-required`

**Associated Information:**

| Property name | Data type | Validation rule | Security or access concerns | Glossary reference |
|---|---|---|---|---|
| review_id | String | Required; unique within project | Author and reviewer access only | Review record |
| platform | String | Required; must match configured platforms | Restricted to approved engineering groups | Platform |
| project_ticket | String | Required; link to the work item | Access limited to project participants | Jira ticket |
| selected_sections | Array[String] | Required; at least one section | Section visibility follows role-based access | Review section |

**Related Use Cases:** `UC-REV-assemble-materials`: Assemble review materials.
**Assumptions:** The underlying Jira data source is available for the selected work item.
**Open Issues:** Which platforms and sections are mandatory for each review type still need sponsor confirmation.

---

### `UC-REV-assemble-materials`: Assemble review materials

**UC ID and Name:** `UC-REV-assemble-materials`: Assemble review materials
**Created By:** Cong Le
**Date Created:** 2026-09-25
**Primary Actor:** author
**Secondary Actors:** Jira, SVN, Jenkins
**Trigger:** A review package is created and the system begins package assembly.
**Description:** The system gathers the change context, file list, SVN revisions, repository links, diff information, and build/test data needed for review.

**Preconditions:**

- PRE-1. A review package exists in the “In preparation” state.
- PRE-2. The author has permission to retrieve change details from Jira, SVN, and build outputs.
- PRE-3. The review package includes at least one section requiring supporting evidence.

**Postconditions:**

- POST-1. The review package contains a complete set of supporting evidence for the selected sections.
- POST-2. Missing or inconsistent material is flagged for correction before publication.

**Main Success Scenario:**

1. The system retrieves the associated Jira ticket and change context for the review.
2. The system queries SVN for the changed files, revision numbers, repository links, and diff output.
3. The system includes relevant source files or code excerpts tied to the selected review sections.
4. The system checks whether the selected sections require Jenkins build or test information.
5. The system attaches the required checklist templates and review-record documents for each section.
6. The system stores the assembled materials in the review package and marks it as “Materials assembled.”
7. Use case ends.

**Extensions:**

- **2a. SVN information is incomplete or missing:**
    - 2a1. The system records the missing file or revision and alerts the author.
    - 2a2. The author corrects the source information or selects a valid alternate change set.
- **4a. The selected section requires build output but no Jenkins result is available:**
    - 4a1. The system marks the item as “Pending build validation.”
    - 4a2. The author requests or triggers the build and resumes the assembly process once the result is available.
- **5a. A checklist template is not available for a selected section:**
    - 5a1. The system shows a warning and keeps the package in an incomplete state.
    - 5a2. The author confirms the template or requests a missing form before continuing.

**Priority:** High
**Frequency of Use:** Frequent; executed for every review package.
**Business Rules:** `BR-review-evidence-retained`, `BR-review-package-required`

**Associated Information:**

| Property name | Data type | Validation rule | Security or access concerns | Glossary reference |
|---|---|---|---|---|
| file_list | Array[FileRef] | At least one file required for a code review | Project-scoped access only | Repository |
| revision_number | String | Required for each changed file when available | Restricted to project participants | Revision number |
| diff_output | Text/Attachment | Required when a code change is under review | Sensitive source information | Diff |
| build_status | Enum | Optional unless the review section requires build evidence | Restricted to authorized engineering users | Build |
| checklist_template | String | Required for each selected section | Role-based access to review records | Review checklist |

**Related Use Cases:** `UC-REV-create-review`, `UC-REV-validate-package`
**Assumptions:** SVN and Jenkins remain the authoritative data sources for the review package.
**Open Issues:** The exact review sections and required evidence for each platform still need formal confirmation.

---

### `UC-REV-validate-package`: Validate review package completeness

**UC ID and Name:** `UC-REV-validate-package`: Validate review package completeness
**Created By:** Cong Le
**Date Created:** 2026-09-25
**Primary Actor:** author
**Secondary Actors:** system, reviewer
**Trigger:** The assembled review package is ready for review publication.
**Description:** The system checks that all required sections, file descriptions, revision references, and checklist items are present before the review is sent to reviewers.

**Preconditions:**

- PRE-1. A review package exists with assembled materials and selected sections.
- PRE-2. The author has completed all required package entry fields, or the system has identified the specific missing items.

**Postconditions:**

- POST-1. The review package is either marked as ready for review or returned to the author for correction.
- POST-2. All validation warnings are recorded in the review log for traceability.

**Main Success Scenario:**

1. The author requests validation of the assembled review package.
2. The system compares the selected review sections to the required sections for the selected platform.
3. The system checks for missing file descriptions, missing revision numbers, incomplete diff coverage, or missing build/test evidence.
4. The system checks that every required checklist form has an associated template or record.
5. The system either marks the package as valid and ready for reviewer notification or lists the issues that must be corrected.
6. Use case ends.

**Extensions:**

- **2a. A required review section is missing:**
    - 2a1. The system highlights the absent section and blocks publication.
    - 2a2. The author adds the missing section or confirms an intentional exception.
- **3a. Diff coverage is incomplete:**
    - 3a1. The system lists the files excluded from the diff and warns the author.
    - 3a2. The author updates the review package or documents the reason for exclusion.
- **5a. Validation fails because of unresolved issues:**
    - 5a1. The system keeps the package in a draft or corrective state.
    - 5a2. The author fixes the issues and re-runs validation.

**Priority:** High
**Frequency of Use:** Frequent; each review is validated before publication.
**Business Rules:** `BR-review-package-required`, `BR-review-evidence-retained`

**Associated Information:**

| Property name | Data type | Validation rule | Security or access concerns | Glossary reference |
|---|---|---|---|---|
| validation_status | Enum | Required; values: valid, incomplete, blocked | Author and moderator access only | Review record |
| missing_items | Array[String] | Optional but shown for incomplete reviews | Restricted to authorized reviewers and authors | Review section |
| validation_log | Text | Required for issues and remediation steps | Audit access only | Audit |

**Related Use Cases:** `UC-REV-assemble-materials`, `UC-NOT-notify-reviewers`
**Assumptions:** Review section requirements are defined by the internal review configuration.
**Open Issues:** The exact validation rules for platform-specific completeness are still being confirmed with the project sponsor.

---

### `UC-NOT-notify-reviewers`: Notify reviewers

**UC ID and Name:** `UC-NOT-notify-reviewers`: Notify reviewers
**Created By:** Cong Le
**Date Created:** 2026-09-25
**Primary Actor:** author
**Secondary Actors:** reviewer, system
**Trigger:** The review package is validated and ready for assessment.
**Description:** The system notifies the assigned reviewers that the review package is ready and provides access to the same evidence package used for assessment.

**Preconditions:**

- PRE-1. The review package has passed validation.
- PRE-2. At least one reviewer has been assigned to the review or the assignment list is available in the system.

**Postconditions:**

- POST-1. Each assigned reviewer receives a notification that a review is ready.
- POST-2. The review package remains accessible for assessment until closure or reassignment.

**Main Success Scenario:**

1. The author submits the review package for reviewer access.
2. The system verifies the package status is ready for review.
3. The system identifies the assigned reviewers and notification method.
4. The system sends the review invitation or notification with a link to the package and summary of required sections.
5. The system records the time and outcome of the notification as part of the review history.
6. Use case ends.

**Extensions:**

- **3a. No reviewer is assigned:**
    - 3a1. The system requests the author to choose or assign at least one reviewer.
    - 3a2. The author assigns a reviewer and resumes at step 4.
- **4a. Notification delivery fails:**
    - 4a1. The system logs the failure and flags the review as not yet notified.
    - 4a2. The author retries delivery or uses an alternate notification channel.

**Priority:** High
**Frequency of Use:** Frequent; occurs for each review once ready for assessment.
**Business Rules:** `BR-notification-timeliness`, `BR-review-package-required`

**Associated Information:**

| Property name | Data type | Validation rule | Security or access concerns | Glossary reference |
|---|---|---|---|---|
| reviewer_list | Array[String] | At least one reviewer required for a live review | Restricted to review participants | Reviewer |
| notification_time | DateTime | Required when sent | Audit and internal operational visibility | Review artifact |
| review_status | Enum | Required; transitions to “Notified” | Access restricted to participants | Review record |

**Related Use Cases:** `UC-REV-validate-package`, `UC-ASS-assess-review-section`
**Assumptions:** Email or another internal notification channel is available for the review participants.
**Open Issues:** The exact assignment model and coordinator role still need definition with the sponsor.

---

### `UC-ASS-assess-review-section`: Assess a review section

**UC ID and Name:** `UC-ASS-assess-review-section`: Assess a review section
**Created By:** Cong Le
**Date Created:** 2026-09-25
**Primary Actor:** reviewer
**Secondary Actors:** author, system
**Trigger:** A reviewer opens a review package and starts evaluating one section.
**Description:** The reviewer examines the application’s assembled review materials for a specific platform section and records whether the section passes, fails, or needs follow-up based on checklist criteria and source evidence.

**Preconditions:**

- PRE-1. The reviewer is authenticated and authorized to access the review package.
- PRE-2. The review has been notified and is currently open for assessment.
- PRE-3. The review section has applicable evidence and an associated checklist template.

**Postconditions:**

- POST-1. The reviewer has recorded a result for the assessed section.
- POST-2. The package reflects the current reviewer assessment outcome and any required findings.

**Main Success Scenario:**

1. The reviewer opens the review package and selects a section to assess.
2. The system displays the checklist criteria, changed-file context, source references, and any build/test data that apply to that section.
3. The reviewer reviews the evidence and evaluates the section against the checklist criteria.
4. The reviewer records the result and adds comments or references to the relevant file, line, or checklist item when needed.
5. The system saves the assessment result and updates the review progress status.
6. The reviewer repeats the process for other applicable sections until complete or defers remaining sections.
7. Use case ends.

**Extensions:**

- **3a. The evidence is incomplete or stale:**
    - 3a1. The system alerts the reviewer that the package is missing supporting material or may be out of date.
    - 3a2. The reviewer informs the author or requests a correction before continuing.
- **4a. The review reveals a defect or issue:**
    - 4a1. The reviewer creates a finding tied to the relevant checklist item, file, and line reference.
    - 4a2. The system records the finding and updates the review as needing follow-up.
- **5a. The reviewer submits an incomplete assessment:**
    - 5a1. The system prevents closure while required sections remain unresolved.
    - 5a2. The reviewer completes the missing entries or marks the section as deferred.

**Priority:** High
**Frequency of Use:** Frequent; each review section is assessed by one or more reviewers.
**Business Rules:** `BR-reviewer-assessment-based-on-checklist`, `BR-review-evidence-retained`

**Associated Information:**

| Property name | Data type | Validation rule | Security or access concerns | Glossary reference |
|---|---|---|---|---|
| section_result | Enum | Required; values: pass, fail, needs follow-up | Reviewer-only edit; author may view | Review section |
| checklist_reference | String | Required when the result is based on a checklist item | Access limited to project participants | Review checklist |
| file_reference | String | Optional but required when recorded against a file | Scope limited by project permissions | Repository |
| line_reference | String | Optional; valid when file reference exists | Restricted to the review package participants | Review artifact |

**Related Use Cases:** `UC-NOT-notify-reviewers`, `UC-ASS-record-findings`, `UC-CLS-close-review`
**Assumptions:** Reviewers use the checklist and supporting evidence as the ground truth for evaluation.
**Open Issues:** The exact reviewer workflow for multiple-reviewer signoff and re-opened reviews still needs client confirmation.

---

### `UC-ASS-record-findings`: Record review findings

**UC ID and Name:** `UC-ASS-record-findings`: Record review findings
**Created By:** Cong Le
**Date Created:** 2026-09-25
**Primary Actor:** reviewer
**Secondary Actors:** author, system
**Trigger:** The reviewer identifies a defect, issue, or required change during section assessment.
**Description:** The reviewer records the finding with context, references, and required follow-up so the author can address it and the review record reflects the issue accurately.

**Preconditions:**

- PRE-1. The review section is open for assessment and the reviewer has the necessary evidence.
- PRE-2. The finding is connected to a specific checklist item, file, or code location when applicable.

**Postconditions:**

- POST-1. The review package contains a logged finding with supporting reference information.
- POST-2. The author receives visibility into the finding and the review remains open until resolution or disposition.

**Main Success Scenario:**

1. The reviewer identifies a problem or required follow-up during assessment.
2. The system asks for the checklist item, file reference, and description of the finding.
3. The reviewer enters the issue description and any supporting evidence or line references.
4. The system records the finding and associates it with the review package and selected section.
5. The system marks the review as requiring author follow-up.
6. Use case ends.

**Extensions:**

- **2a. The reviewer does not know the exact file or line:**
    - 2a1. The system allows a general finding description but prompts for as much traceable evidence as possible.
    - 2a2. The reviewer supplies what is available and continues.
- **3a. The issue is duplicate of an existing finding:**
    - 3a1. The system suggests a matching finding and allows merger with the existing record.
    - 3a2. The reviewer confirms or edits the merged entry.
- **5a. The author disputes the finding:**
    - 5a1. The system keeps the finding and its disposition visible in the review record.
    - 5a2. The review remains open until the issue is resolved or formally closed.

**Priority:** High
**Frequency of Use:** Moderate; each review may generate multiple findings.
**Business Rules:** `BR-review-evidence-retained`, `BR-reviewer-assessment-based-on-checklist`

**Associated Information:**

| Property name | Data type | Validation rule | Security or access concerns | Glossary reference |
|---|---|---|---|---|
| finding_id | String | Required; unique within review | Restricted to review participants | Review artifact |
| finding_description | Text | Required | Access limited to review participants | Review finding |
| severity | Enum | Optional; if used, must be defined by policy | Restricted to internal reviewer roles | Review record |
| resolution_status | Enum | Required after author response | Audit visibility | Review artifact |

**Related Use Cases:** `UC-ASS-assess-review-section`, `UC-CLS-close-review`
**Assumptions:** Findings are recorded as part of the review process and may remain open until resolved.
**Open Issues:** The exact disposition workflow for disputed findings is not yet defined.

---

### `UC-CLS-close-review`: Close a review and retain evidence

**UC ID and Name:** `UC-CLS-close-review`: Close a review and retain evidence
**Created By:** Cong Le
**Date Created:** 2026-09-25
**Primary Actor:** moderator or author
**Secondary Actors:** reviewer, system
**Trigger:** The review package has been assessed, follow-up is complete, and closure is authorized.
**Description:** The system records the final review outcome, archives the assembled evidence for audit or later inspection, and marks the review as closed.

**Preconditions:**

- PRE-1. The review package has been assessed and all mandatory sections have a disposition.
- PRE-2. Any required findings have been addressed or formally accepted as unresolved under the review policy.
- PRE-3. The closure action is performed by an authorized user.

**Postconditions:**

- POST-1. The review is marked closed in the system.
- POST-2. A retained evidence package and final record are available for audit or review follow-up.

**Main Success Scenario:**

1. The moderator or author initiates closure for the review package.
2. The system checks whether all required sections have a complete disposition and whether all major findings are addressed or accepted.
3. The system captures the final review outcome and summary of findings.
4. The system archives the review package, checklist records, supporting evidence, and metadata for retention.
5. The system marks the review as closed and records the timestamp and user who closed it.
6. Use case ends.

**Extensions:**

- **2a. A required section remains incomplete:**
    - 2a1. The system prevents closure and identifies the incomplete section.
    - 2a2. The moderator or author resolves the issue or documents the reason for deferred closure.
- **3a. Review findings remain unresolved:**
    - 3a1. The system records the unresolved findings with their status.
    - 3a2. The review may remain open or be closed with formal disposition, depending on policy.
- **4a. Evidence retention is unavailable:**
    - 4a1. The system logs the storage failure and keeps the review in a closure-pending state.
    - 4a2. The authorized user resolves the retention issue before the final close.

**Priority:** Medium
**Frequency of Use:** Moderate; occurs when a review is complete.
**Business Rules:** `BR-review-evidence-retained`, `BR-review-package-required`

**Associated Information:**

| Property name | Data type | Validation rule | Security or access concerns | Glossary reference |
|---|---|---|---|---|
| final_status | Enum | Required; values: pass, fail, closed-with-findings | Restricted to authorized roles | Review record |
| closure_timestamp | DateTime | Required | Internal audit access | Audit |
| evidence_package | Attachment | Required for retained review evidence | Sensitive operational data | Review artifact |
| closure_user | String | Required | Access limited to authorized internal roles | Moderator |

**Related Use Cases:** `UC-ASS-record-findings`, `UC-ASS-assess-review-section`
**Assumptions:** The organization maintains a formal policy for recording review outcomes and retained evidence.
**Open Issues:** The exact closure criteria and required retention period still need sponsor confirmation.

---

## Working these with your agent

This use-case set is intentionally grounded in the project brief and the review workflow documented in the concept note. The next useful step is to test these against the client’s actual process by verifying the review sections, role names, and notification model. Any mismatches should be captured as issues and moved into [OPEN-ISSUES.md](OPEN-ISSUES.md).

The key verification question is straightforward: if a stakeholder reads each main success scenario aloud, do they recognize the same review flow they perform today, but with the repetitive manual work removed? If the answer is “yes,” the use cases reflect real behavior. If the answer is “not quite,” the missing details belong in the open issues list before implementation begins.

