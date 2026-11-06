# Traceability Matrix

**Project:** RevView/OMNI
**Team:** Team 8
**Version:** 0.2
**Last checked:** 2026-11-06, Ethan Nguyen (teammate review pending)

---

_**How to use this file.** Maintain links from business objectives and features to requirements, design, code, and tests. Cite identifiers instead of copying requirement text. An empty cell is an unresolved link, not evidence of completion._

## 1. Feature to use case area

Features and MVP inclusion come from [vision and scope section 4.3](requirements/vision-and-scope.md#43-mvp-scope); descriptions are in section 4.2 and business objectives in section 2.2. Areas are defined in [the use-case list](requirements/use-cases.md#3-use-case-list).

The objective and area mappings below are proposed trace links based on those descriptions and the existing use cases. `REV` prepares the materials that `ASS` consumes; `NOT` coordinates notification; `CLS` retains evidence at closure. Team review must confirm these mappings.

| Feature | Business objectives | Use case areas |
|---|---|---|
| `FEAT-review-initiation` | `BO-review-setup-time`, `BO-review-completion-rate` | `REV` |
| `FEAT-context-assembly` | `BO-review-setup-time`, `BO-review-consistency` | `REV`, `ASS` |
| `FEAT-diff-and-source-prep` | `BO-review-setup-time`, `BO-review-consistency`, `BO-audit-readiness` | `REV`, `ASS` |
| `FEAT-checklist-mapping` | `BO-review-completion-rate`, `BO-review-consistency` | `REV`, `ASS` |
| `FEAT-integrity-validation` | `BO-review-completion-rate`, `BO-review-consistency` | `REV` |
| `FEAT-review-notification` | `BO-review-awareness` | `NOT` |
| `FEAT-evidence-retention` | `BO-audit-readiness` | `CLS` |
| `FEAT-admin-and-configuration` |  |  |

`FEAT-admin-and-configuration` is explicitly outside the MVP. Its empty cells record that no business-objective or use-case-area assignment is currently specified; no administration use case is invented here. This is a known coverage gap for team disposition, rather than a completed feature mapping.

**Checks (2026-11-05):**

1. All eight named features in section 4.3 are present. All seven MVP features have an area; the deferred administration feature has none, as noted above.
2. All four defined areas (`REV`, `NOT`, `ASS`, `CLS`) are reached by an MVP feature. Every objective identifier used above is defined in vision and scope section 2.2.

---

## 2. Business rule to what enforces it

This table includes every rule defined in [business-rules.md section 2](requirements/business-rules.md#2-rules). Sources are copied from that document, expanding “same document” to its title. “Enforced by” lists only use cases whose **Business Rules** field explicitly cites the rule; a citation is a specification link, not proof that enforcement is implemented.

| Business rule | Source | Enforced by |
|---|---|---|
| `BR-svn-diff-required` | RevView/OMNI Review Helper Application Concept document, Section 8. | [`UC-REV-assemble-materials`](requirements/use-cases.md#uc-rev-assemble-materials-assemble-review-materials) |
| `BR-review-package-exportable` | RevView/OMNI Review Helper Application Concept document, Sections 7–8. | [`UC-CLS-close-review`](requirements/use-cases.md#uc-cls-close-review-close-a-review-and-retain-evidence) |
| `BR-diff-checklist-match` | RevView/OMNI Review Helper Application Concept document, Section 7.3. | [`UC-REV-assemble-materials`](requirements/use-cases.md#uc-rev-assemble-materials-assemble-review-materials), [`UC-REV-validate-package`](requirements/use-cases.md#uc-rev-validate-package-validate-review-package-completeness) |
| `BR-review-nine-parts` | RevView/OMNI Review Helper Application Concept document, Section 2.3. | [`UC-REV-create-review`](requirements/use-cases.md#uc-rev-create-review-create-a-review-package), [`UC-REV-validate-package`](requirements/use-cases.md#uc-rev-validate-package-validate-review-package-completeness) |
| `BR-review-package-required` | RevView/OMNI Review Helper Application Concept document, Section 7. | [`UC-REV-create-review`](requirements/use-cases.md#uc-rev-create-review-create-a-review-package), [`UC-REV-assemble-materials`](requirements/use-cases.md#uc-rev-assemble-materials-assemble-review-materials), [`UC-REV-validate-package`](requirements/use-cases.md#uc-rev-validate-package-validate-review-package-completeness), [`UC-NOT-notify-reviewers`](requirements/use-cases.md#uc-not-notify-reviewers-notify-reviewers), [`UC-CLS-close-review`](requirements/use-cases.md#uc-cls-close-review-close-a-review-and-retain-evidence) |
| `BR-reviewer-assessment-based-on-checklist` | RevView/OMNI Review Helper Application Concept document, Sections 2.1 and 2.3. | [`UC-ASS-assess-review-section`](requirements/use-cases.md#uc-ass-assess-review-section-assess-a-review-section), [`UC-ASS-record-findings`](requirements/use-cases.md#uc-ass-record-findings-record-review-findings) |
| `BR-review-record-fields` | RevView/OMNI Review Helper Application Concept document, Section 7.1. **Flagged:Needs_Review** the source document marks this information as possibly automatable, so which fields stay human-entered vs. system-derived may change — confirm with the client before treating the field list as fixed. |  |
| `BR-ai-human-override` | RevView/OMNI Review Helper Application Concept document, Sections 5, 5.3. | [`UC-ASS-assess-review-section`](requirements/use-cases.md#uc-ass-assess-review-section-assess-a-review-section), [`UC-ASS-record-findings`](requirements/use-cases.md#uc-ass-record-findings-record-review-findings) |
| `BR-author-owns-change-rationale` | RevView/OMNI Review Helper Application Concept document, Section 5. |  |
| `BR-no-student-prod-access` | RevView/OMNI Review Helper Application Concept document, Section 12. **Flagged:Needs_Review** confirm this is still current IT policy directly with the client/IT, since it drives the sandbox architecture for the whole project. |  |
| `BR-sprint-handoff-cadence` | RevView/OMNI Review Helper Application Concept document, Section 13. |  |
| `BR-build-tagging` | RevView/OMNI Review Helper Application Concept document, Section 13.1. |  |
| `BR-discrepancy-next-sprint` | RevView/OMNI Review Helper Application Concept document, Section 13.1. |  |

The following six rules have no citation in any use case's Business Rules field, so their enforcement cells are intentionally empty:

- `BR-review-record-fields`.
- `BR-author-owns-change-rationale`.
- `BR-no-student-prod-access`.
- `BR-sprint-handoff-cadence`.
- `BR-build-tagging`.
- `BR-discrepancy-next-sprint`.

An empty cell does not mean the team has decided to ignore a rule. In particular, `FR-EXPORT-legacy-format` also cites `BR-review-package-exportable`, and the SRS cites `BR-no-student-prod-access` through the sandbox-development constraint and `BR-review-nine-parts` in its domain model. These are additional specification links, not use-case Business Rules citations. Delivery-process rules may need process evidence rather than application use cases; the team must decide ownership and record any policy decision in [OPEN-ISSUES.md](requirements/OPEN-ISSUES.md).

**Checks (2026-11-05):**

1. All 13 defined rules appear exactly once; seven have explicit use-case citations and six have empty enforcement cells.
2. Every rule identifier cited in the seven use cases' Business Rules fields exists in business-rules.md. All concrete `BR-*` citations in the SRS also resolve. Template examples and identifier-pattern instructions are excluded from this check.
3. `BR-review-record-fields` and `BR-no-student-prod-access` retain their source document's **Flagged:Needs_Review** qualifications; this matrix does not resolve them.

---

## 3. Release plan and implementation traceability

One row tracks each of the seven use cases and each of the three functional requirements defined in [SRS section 5.2](requirements/software-requirements-specification.md#52-non-use-case-functional-requirements). Template examples such as `FR-SAVE-autosave-active` are not project requirements.

**Release:** the allowed assignments are `v0.1.0`, `v0.2.0`, `v1.0.0`, `Spring`, or `Out`. Assembly is assigned `v0.1.0` as the proving slice ([architecture section 6](design/architectural-design.md#6-runtime-view) and the Block 7 instruction). “Pending team (Block 8)” is an unresolved decision, not a release assignment. The remaining nine rows need team agreement; no release commitment is inferred from MVP scope alone.

**Build / Verify:** use the status words expected by `/design` and `/implement`. Build starts at `❌ Not started`; `/design` sets it to `📐 Designed`, and `/implement` advances it to `🟡 In progress` or `✅ Built`. Verify starts at `🔎 None`; use `🟡 Partial` for incomplete coverage and `✅ Verified` only when tests cover the main flow and every extension and pass. A release assignment or documentation PR does not establish implementation or verification.

**Design / Code / Tests:** leave Design empty until `/design` fills it with `design/<area>.md`. `/implement` fills Code and Tests with the implementation and test links. Local, uncommitted proposals and paths suggested in build-context issues are not evidence of merged work.

| Use case / functional requirement | Release | Build | Design | Code | Tests | Verify |
|---|---|---|---|---|---|---|
| [`UC-REV-create-review`](requirements/use-cases.md#uc-rev-create-review-create-a-review-package) | Pending team (Block 8) | ❌ Not started | | | | 🔎 None |
| [`UC-REV-assemble-materials`](requirements/use-cases.md#uc-rev-assemble-materials-assemble-review-materials) | `v0.1.0` | ❌ Not started | | | | 🔎 None |
| [`UC-REV-validate-package`](requirements/use-cases.md#uc-rev-validate-package-validate-review-package-completeness) | Pending team (Block 8) | ❌ Not started | | | | 🔎 None |
| [`UC-NOT-notify-reviewers`](requirements/use-cases.md#uc-not-notify-reviewers-notify-reviewers) | Pending team (Block 8) | ❌ Not started | | | | 🔎 None |
| [`UC-ASS-assess-review-section`](requirements/use-cases.md#uc-ass-assess-review-section-assess-a-review-section) | Pending team (Block 8) | ❌ Not started | | | | 🔎 None |
| [`UC-ASS-record-findings`](requirements/use-cases.md#uc-ass-record-findings-record-review-findings) | Pending team (Block 8) | ❌ Not started | | | | 🔎 None |
| [`UC-CLS-close-review`](requirements/use-cases.md#uc-cls-close-review-close-a-review-and-retain-evidence) | Pending team (Block 8) | ❌ Not started | | | | 🔎 None |
| [`FR-EXPORT-legacy-format`](requirements/software-requirements-specification.md#52-non-use-case-functional-requirements) | Pending team (Block 8) | ❌ Not started | | | | 🔎 None |
| [`FR-AUDIT-action-log`](requirements/software-requirements-specification.md#52-non-use-case-functional-requirements) | Pending team (Block 8) | ❌ Not started | | | | 🔎 None |
| [`FR-SYNC-reviewer-bidirectional`](requirements/software-requirements-specification.md#52-non-use-case-functional-requirements) | Pending team (Block 8) | ❌ Not started | | | | 🔎 None |

**Block 8 decision checklist:**

- Assign the remaining nine releases from the allowed values above and record the meeting/date supporting the decisions.
- Confirm feature/objective/area mappings and disposition of the deferred administration feature.
- Assign owners for the six rule-citation gaps; record agreed requirement or process links without inventing new policy.
- Confirm the proving slice can demonstrate assembly with an existing package fixture before other workflow use cases are built.

**Checks (2026-11-06):** exactly ten distinct rows cover all seven use cases and all three defined `FR-*` requirements; assembly is `v0.1.0`. All rows start at Build `❌ Not started` and Verify `🔎 None`, with Design empty. Remaining release decisions and teammate approval are pending.

---

## Maintaining the matrix

When a requirement is implemented, update its Design, Code, and Tests links in the same pull request. Record verification evidence separately from build completion and keep failed or unexecuted checks visible. When source requirements change, rerun the feature coverage, rule citation, and requirement-row checks before updating the last-checked date.
