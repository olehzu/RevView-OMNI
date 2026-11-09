# Review Preparation Design

**Project:** RevView/OMNI
**Team:** Team 8
**Area:** `UC-REV`

> **Realizes:** [`UC-REV-assemble-materials`](../requirements/use-cases.md#uc-rev-assemble-materials-assemble-review-materials) (main success scenario, extensions 2a1 and 4a1)
> **Depends on:** `BR-review-package-required`, `BR-svn-diff-required`, `BR-diff-checklist-match`, `BR-review-nine-parts` ([business rules](../requirements/business-rules.md), read as the [2026-11-06 client meeting](../requirements/client-meeting/client-interview-2026-11-06.md) reshaped them); `SI-svn-read`, `SI-jenkins-read`, `ROB-incomplete-package-blocked`, `SEC-authenticated-access` (deferred, see Open questions), `CO-sandbox-development` ([specification](../requirements/software-requirements-specification.md)); [architecture-of-record](architectural-design.md) sections 8.2.1, 8.2.3, 8.2.4, 8.2.10
> **See:** [use cases](../requirements/use-cases.md), [specification](../requirements/software-requirements-specification.md), [architecture-of-record](architectural-design.md), [glossary](../requirements/project-glossary.md)
> **Designed against:** `c888a31` (`main`) plus `5a32b1d` (PR #41, the 2026-11-06 client meeting record, not yet merged)

---

_**How to use this template.** Copy it to `docs/design/<area>.md`, named for the lowercase area code (`ord.md` for `UC-ORD-*`). Instructions appear in italic square brackets; leave them in place until the document is stable, because the agent reads them on every later pass. The full worked example is Project Pulse's [`not.md`](https://github.com/Washingtonwei/project-pulse/blob/main/docs/design/not.md); read it for the shape, not for the answers._

_**What this document is.** The **design-of-record** for one use case area: how the code will realize its use cases, written **before** the code and approved before anyone builds from it. It is the last document your agent reads before it writes code, so anything it leaves out, the agent invents._

_**What it is not.** A copy of your use cases. It **cites** `UC-*`, `FR-*`, and `BR-*` by identifier and never restates what the system shall do; it says only how._

_**One document per area, not per use case.** The overview, the class diagram, and the data model are **revised in place**. The sequence diagrams, the API contract rows, and the test rows are **appended**, one set per use case. Never add a `## UC-…` section that repeats the whole skeleton._

_**How much to write.** Pin down what a wrong guess would break: a requirement, a business rule, a quality attribute, or the contract between two parts of your team. Leave the rest for the agent to derive while it builds._

---

## Overview

_[One paragraph: what this area does, which components of the architecture-of-record it lives in, and what it reads from or calls in other areas.]_

Review Preparation takes a review package from "In preparation" to "Materials assembled": it finds the SVN Branch for the package's Jira Ticket, collects the Changed Files, Revisions, and Diffs, links candidate Jenkins Builds, and attaches the Review Checklist and Review Record. It is the `REV` area's Review Preparation component ([use case areas](architectural-design.md#52-use-case-areas-and-components)) and reaches SVN and Jenkins only through Integration Gateway adapters (section 8.2.4).

**v0.1.0 shortcuts, deliberate:**

- **The review package comes from a fixture.** `UC-REV-create-review` is not built, so a synthetic package in "In preparation" is seeded at startup. It already holds the Jira Ticket key, so step 1 reads the key from the package and **makes no Jira call**.
- **The SVN and Jenkins adapters are fakes** returning Synthetic Data (`CO-sandbox-development`, section 8.2.10). The real sandbox adapters replace them behind the same interfaces.
- **Storage is in memory.** Nothing survives a restart. PostgreSQL (`CO-database`) arrives with the first use case that needs persistence.

**Package shape.** The shape follows the 2026-11-06 meeting (`OI-31`, `OI-36`), not specification section 7.1. A package has one Review Checklist with one tab per Platform (common, falcon, phoenix), one Review Record, and one Diff per Platform × Code/Tools/Tests Category the change touches, up to nine. The specification and business-rule edits follow in a separate pull request.

## Components & classes

_[One class diagram for the whole area, and one line per class or file saying what it does and whether it is **new** or **reused**. If the repository has no code for this area yet, list the files you expect the agent to create and mark them all new.]_

```mermaid
classDiagram
    direction LR
    class ReviewPackageRouter {
        <<new>>
        +assemble(reviewId) Response
        +get(reviewId) Response
    }
    class AssemblyService {
        <<new>>
        +assemble(reviewId) ReviewPackage
    }
    class ReviewPackageRepository {
        <<new, in memory>>
        +get(reviewId) ReviewPackage
        +save(ReviewPackage)
    }
    class SvnAdapter {
        <<new, interface>>
        +find_branches(ticketKey) List~str~
        +changed_files(branch) List~ChangedFile~
    }
    class JenkinsAdapter {
        <<new, interface>>
        +find_builds(ticketKey, branch) List~JenkinsBuild~
    }
    class FakeSvnAdapter { <<new>> }
    class FakeJenkinsAdapter { <<new>> }
    ReviewPackageRouter --> AssemblyService
    AssemblyService --> ReviewPackageRepository
    AssemblyService --> SvnAdapter
    AssemblyService --> JenkinsAdapter
    SvnAdapter <|.. FakeSvnAdapter
    JenkinsAdapter <|.. FakeJenkinsAdapter
```

- `backend/app/rev/router.py` (new): the two endpoints. It validates the request shape and nothing else.
- `backend/app/rev/assembly.py` (new): `AssemblyService`, steps 1 to 6 with the extensions below, and `classify(path)`, which maps a repository path to a Platform and a Code/Tools/Tests Category.
- `backend/app/rev/models.py` (new): Review Package, Changed File, Diff, Jenkins Build, Review Checklist (Platform tabs), Review Record.
- `backend/app/rev/repository.py` (new): the in-memory store.
- `backend/app/rev/fixtures.py` (new): one synthetic review package in "In preparation", with a placeholder ticket key.
- `backend/app/integration/common.py` (new): `IntegrationUnavailable(source)`, which every adapter raises when its system does not answer, and `contains_ticket_key`, the key match every adapter uses.
- `backend/app/integration/svn.py` (new): `SvnAdapter` and `FakeSvnAdapter`.
- `backend/app/integration/jenkins.py` (new): `JenkinsAdapter` and `FakeJenkinsAdapter`. It is **read only and has no method that starts a build** (`OI-35`).
- `backend/app/errors.py` (new): turns `IntegrationUnavailable`, the area's errors, request validation errors, unknown routes, and unexpected exceptions into the section 8.2.3 envelope at the trust boundary (section 8.2.1). It is registered in `backend/app/main.py` (reused).
- The adapters and the repository are FastAPI dependencies, declared in `router.py`, so tests swap in fakes that fail or return other data. No new packages. `backend/pyproject.toml` now finds `app*` packages, so the new subpackages are installed.

## Sequence

_[One sequence diagram per use case for its main success scenario. **Label each interaction with the use case step it implements.** Use `alt` blocks for extensions.]_

### UC-REV-assemble-materials: assembling review materials

```mermaid
sequenceDiagram
    actor A as Author
    participant R as ReviewPackageRouter
    participant S as AssemblyService
    participant DB as ReviewPackageRepository
    participant SVN as SvnAdapter
    participant J as JenkinsAdapter
    A->>R: POST /api/v1/review-packages/{reviewId}/assembly (trigger)
    R->>S: assemble(reviewId)
    S->>DB: get(reviewId), must be "In preparation" (PRE-1)
    S->>S: Jira Ticket key from the package (step 1, fixture, no Jira call)
    S->>SVN: find_branches(ticketKey) (step 2)
    alt SVN unavailable (SI-svn-read, 8.2.1)
        SVN-->>S: IntegrationUnavailable(SVN)
        S->>DB: record SVN evidence unavailable, status stays "In preparation"
        S-->>R: SVN_UNAVAILABLE
        R-->>A: 503
    end
    alt no SVN Branch, or several, match
        S-->>R: ASSEMBLY_INCOMPLETE (branch), stored with no materials
    end
    S->>SVN: changed_files(branch): path, Revision, repository link, diff (step 2)
    alt no Changed Files
        S-->>R: ASSEMBLY_INCOMPLETE (changed files), stored with no materials
    end
    opt a Changed File has no Revision (2a1)
        S->>S: record it as missing, to alert the author
    end
    S->>S: classify each path, group into one Diff per Platform x Category (step 3)
    S->>J: find_builds(ticketKey, branch) (step 4)
    alt Jenkins unavailable (SI-jenkins-read, 8.2.1)
        J-->>S: IntegrationUnavailable(Jenkins)
        S->>DB: record Jenkins evidence unavailable, status stays "In preparation"
        S-->>R: JENKINS_UNAVAILABLE
        R-->>A: 503
    end
    alt no matching Jenkins Build (4a1)
        S->>S: status "Pending build validation"
    else
        S->>S: builds newest first, most recent preselected (step 4)
    end
    S->>S: one Review Checklist, a tab per Platform listing its Changed Files, and one Review Record (step 5)
    S->>DB: save, status "Materials assembled" unless 2a1 or 4a1 applies (step 6)
    R-->>A: 200, the package and anything missing
```

**Status after assembly.** It is "Materials assembled" only when nothing is missing. A missing Revision (2a1) leaves "In preparation" with the gap listed, because POST-2 asks for the gap to be flagged for correction. No matching build (4a1) gives "Pending build validation". When both apply, 2a1 wins, since the package cannot be assembled without its Revisions.

## API contract

_[One row per endpoint. **This section is never dropped.** Use the error shape section 8.2 fixes.]_

All responses use the section 8.2.3 envelope: `{"data": …}` or `{"error": {"code", "message", "source"}}`.

| Endpoint or job | Caller (who may) | Request | Success | Errors, by extension |
|---|---|---|---|---|
| `POST /api/v1/review-packages/{reviewId}/assembly` | The package's Author. v0.1.0 has no authentication (see Open questions) | None | `200`: the package, with its status, SVN Branch, Diffs (each with its Platform, Category, and Changed Files with Revision and repository link), candidate Jenkins Builds newest first with one preselected, the Review Checklist tabs, the Review Record, and `missing` (the Changed Files without a Revision, 2a1). 4a1: status "Pending build validation", no build preselected | SVN unavailable: `503 SVN_UNAVAILABLE`, `source: "SVN"`. Jenkins unavailable: `503 JENKINS_UNAVAILABLE`, `source: "Jenkins"`. No branch, several branches, no Changed Files, or an unclassifiable path: `409 ASSEMBLY_INCOMPLETE`, the message naming which (and the path). Package not "In preparation" (PRE-1, which also refuses a re-run once past "In preparation"): `409 REVIEW_PACKAGE_NOT_IN_PREPARATION`. Unknown id: `404 REVIEW_PACKAGE_NOT_FOUND` |
| `GET /api/v1/review-packages/{reviewId}` | Same | None | `200`: the stored package as above. After an SVN or Jenkins outage, that evidence reads `unavailable` | `404 REVIEW_PACKAGE_NOT_FOUND` |

**Example `200` body** (main success scenario, Synthetic Data):

```json
{
  "data": {
    "review_id": "rev-0001",
    "status": "Materials assembled",
    "jira_ticket_key": "SYN-1",
    "svn_branch": "SYN-1-timer-fix",
    "svn_evidence": "available",
    "jenkins_evidence": "available",
    "diffs": [
      {
        "platform": "common",
        "category": "tools",
        "diff": "Index: tools/common/branches/SYN-1-timer-fix/src/timer.py\n...",
        "changed_files": [
          {
            "path": "tools/common/branches/SYN-1-timer-fix/src/timer.py",
            "revision": "1042",
            "repository_link": "https://svn.example.invalid/repo/tools/common/branches/SYN-1-timer-fix/src/timer.py?p=1042"
          }
        ]
      }
    ],
    "jenkins_builds": [
      { "build_number": 57, "name": "SYN-1 timer fix", "result": "SUCCESS", "built_at": "2026-11-05T14:02:11Z" },
      { "build_number": 55, "name": "SYN-1 timer fix", "result": "FAILURE", "built_at": "2026-11-04T09:40:03Z" }
    ],
    "preselected_build": 57,
    "review_checklist": {
      "tabs": [
        { "platform": "common", "changed_files": ["tools/common/branches/SYN-1-timer-fix/src/timer.py"] }
      ]
    },
    "review_record": { "id": "rr-0001", "review_id": "rev-0001", "jira_ticket_key": "SYN-1" },
    "missing": []
  }
}
```

- Statuses are the use case's display strings exactly. Field names are snake_case. `platform` and `category` are lowercase, spelled exactly as the path segment. Paths are full repository paths, and the same string appears in the Diff, the checklist tab, and `missing`.
- `missing` entries read `{"path": …, "missing": "revision"}`. `preselected_build` is `null` under 4a1. `svn_evidence` and `jenkins_evidence` are `"available"`, `"unavailable"`, or `null` when that system has not been asked yet: before the first assembly, and `jenkins_evidence` after an SVN outage, since Jenkins is not queried then.
- After an SVN or Jenkins outage, or an `ASSEMBLY_INCOMPLETE`, the stored package has no materials (no branch, Diffs, builds, checklist, record, or `missing`), with each system's evidence as observed: a Jenkins outage stores `svn_evidence: "available"`, `jenkins_evidence: "unavailable"`; an `ASSEMBLY_INCOMPLETE` stores `svn_evidence: "available"`, `jenkins_evidence: null`. Nothing half-assembled or left over from an earlier run is stored.
- The Review Checklist has a tab for each Platform the change touches, in common, falcon, phoenix order; Diffs are in Platform then Category order, and files within a Diff by path. The Review Record id is the review id with `rev-` replaced by `rr-`.
- Errors: `source` is `null` when no external system is involved. `ASSEMBLY_INCOMPLETE` names the gap in `message` only. `reviewId` is an opaque string, and any unknown one gives `404`.

## Key decisions

_[Only the decisions a reader could not recover from the code. **Each one names what you chose, what you rejected, and why.**]_

**SVN unavailable is a `503` plus a stored "unavailable".** Rejected: `200` with an unavailable flag, because a 2xx is too easily read as passing evidence (section 8.2.1, `SI-svn-read`). Jenkins is not queried, since the build match needs the branch.

**No matching Jenkins Build is a `200` in "Pending build validation" (4a1).** Rejected: an error, because the use case makes it a state the author resolves by running a build when prompted (`OI-35`). Missing branch and missing files remain errors because there is nothing to assemble.

**Platform and Category come from the repository path.** A path of the form `<category>/<platform>/branches/<branch>/…` (for example `tools/common/branches/<ticket>/…` is common, tools) decides both. Rejected: the author choosing per file, and file-type rules (the team's reading of `OI-32`).

**Jenkins evidence is per package, not per section.** Matching builds (the ticket key in the build name or description, and the branch-name parameter equal to the SVN Branch) are listed newest first, with the most recent preselected. Rejected: one build per section, because a build belongs to a branch, and every section needs evidence (`OI-33`, `OI-34` reconciled).

**The Jenkins adapter cannot start a build.** Rejected: triggering a build when none matches, because the client said to prompt the author (`OI-35`).

**Assembly proceeds only on exactly one SVN Branch whose name contains the ticket key.** None, or several, gives `409 ASSEMBLY_INCOMPLETE` (branch). When several match, the author should choose (`OI-29`); that choice is not built in v0.1.0, and the fixture has exactly one match. Rejected: taking the first match, which would silently assemble evidence from the wrong branch.

**The store is in memory.** Rejected: PostgreSQL in v0.1.0, because the slice proves the assembly flow and the adapters, not persistence. The repository interface is the seam the database replaces.

**Implementation rules** (from the questions test):

- The SVN Branch is a name, and `changed_files` searches every `<category>/<platform>/branches/<name>` root.
- Key match: case-sensitive, and the key must not be preceded by a letter or digit nor followed by a digit (`SYN-10-cleanup` and `ASYN-1-refactor` do not match `SYN-1`).
- Any adapter failure on any call → `503 <SOURCE>_UNAVAILABLE`, evidence recorded as `unavailable`, status unchanged.
- An unclassifiable path → `409 ASSEMBLY_INCOMPLETE` naming the path.
- A 2a1 file still goes into its Diff and its checklist tab.
- Builds are listed with their result; the newest is preselected whatever its result.
- Timestamps are UTC ISO 8601 with `Z`.
- Envelope handlers for validation errors (`VALIDATION_FAILED`), unknown routes (`NOT_FOUND`), a method a route does not allow (`405 METHOD_NOT_ALLOWED`), any other HTTP error (`REQUEST_FAILED`), and unexpected errors (`INTERNAL_ERROR`), with safe messages.
- Log one line per assembly (review id, outcome, code), never diff or source content.
- Assemblies run one at a time (a lock), so two requests cannot both pass PRE-1 and overwrite each other (section 8.2.8); the in-memory store has no transactions.

## Data model

_[The **change** this area makes to the data. If nothing changes, say "No change" and give the reason.]_

No database change: v0.1.0 holds review packages in memory (see Overview). The package shape departs from specification section 7.1 as described in the Overview. The domain-model and business-rule edits follow in a separate pull request.

## Reuse & cross-cutting

_[Which existing services, components, and conventions this area uses rather than rebuilding.]_

- The FastAPI app in `backend/app/main.py` (reused). The new router mounts under `/api/v1` beside `GET /api/v1/health`.
- Error handling: section 8.2.1, one translation in `backend/app/errors.py`.
- API conventions: section 8.2.3, the envelope.
- Code conventions: section 8.2.4. The area lives in `app/rev/`, and the adapters in `app/integration/`.
- Testing: section 8.2.10, Synthetic Data only. The tests use FastAPI's `TestClient` as `backend/tests/test_health.py` does.
- Not used in v0.1.0: the clock (section 8.2.2), because assembly stores no timestamp of its own and build order comes from Jenkins's build times; and auditing (section 8.2.9), because assembly is not among the transitions it lists.

## Tests

_[One row per flow: the main success scenario and **every** extension this document realizes. No code.]_

| Use case, flow | Level | Asserts |
|---|---|---|
| UC-REV-assemble-materials main | integration | The fixture package's POST returns `200` with status "Materials assembled"; the SVN Branch matched; one Diff per Platform × Category touched and no other; every Changed File has a Revision and a repository link; each Review Checklist tab lists exactly the Changed Files in that Platform's Diffs (`BR-diff-checklist-match`); one Review Record; builds newest first with the most recent preselected; the Jenkins fake received no start-build call; the GET returns the same package |
| UC-REV-assemble-materials step 3 | unit | `classify` maps each Platform × Category path to the right pair, for example `tools/common/branches/<ticket>/…` to common, tools |
| UC-REV-assemble-materials 2a1 | integration | A Changed File without a Revision returns `200` with that file in `missing`, and the status stays "In preparation" |
| UC-REV-assemble-materials 4a1 | integration | No matching Jenkins Build returns `200` with status "Pending build validation" and no build preselected |
| 2a1 and 4a1 together | integration | Status stays "In preparation" (2a1 wins), no build preselected |
| SVN unavailable (`SI-svn-read`, 8.2.1) | integration | A failing SVN fake gives `503 SVN_UNAVAILABLE` with `source: "SVN"`; the GET shows "In preparation", SVN evidence `unavailable`, and no Diffs; Jenkins was not called |
| Jenkins unavailable (`SI-jenkins-read`, 8.2.1) | integration | A failing Jenkins fake gives `503 JENKINS_UNAVAILABLE` with `source: "Jenkins"`; the GET shows "In preparation" and `jenkins_evidence` `unavailable`, never "Pending build validation" |
| No branch, several branches, no Changed Files | unit | Each gives `409 ASSEMBLY_INCOMPLETE` naming the gap; the status is unchanged, no materials are stored, and `svn_evidence` reads `available` |
| Re-run that hits `409` | integration | After an outage, or after 2a1, a re-run giving `ASSEMBLY_INCOMPLETE` leaves no stale materials and `svn_evidence` `available` |
| PRE-1 | integration | A second POST on an assembled package gives `409 REVIEW_PACKAGE_NOT_IN_PREPARATION` |
| Unknown package | integration | `404 REVIEW_PACKAGE_NOT_FOUND` on the POST and the GET |

## Changes to the architecture-of-record

_[List each change to the architecture-of-record in one line, or "None".]_

- Section 8.2.3 now defines the success and error envelope it already required, with the `source` field section 8.2.1 calls for.

## Open questions & risks

_[What this design could not settle and who can, and what could go wrong that you are accepting.]_

- **The fakes do not retire `RISK-sandbox-integration-unproven` or `RISK-svn-from-python`.** Those were the reasons this use case is the proving slice. The Integration Gateway stays `provisional` until the real sandbox adapters pass the same tests.
- **The assembly log line is not emitted by the running app yet.** No logging configuration exists, so `app.*` INFO messages are dropped at the root's default level; the test reads them directly. Configuring logging for the application (section 8.2.7, with a request correlation id) is a follow-up.
- **`SEC-authenticated-access` is deferred.** There is no Identity component yet, so v0.1.0 runs on a developer's machine only and must not be exposed on a network.
- **Unclassifiable paths.** A path outside the `<category>/<platform>/…` pattern has no rule. The fixture avoids it. It goes to Sumalee with the `OI-32` confirmation.
- **Assumptions to confirm with Sumalee Rodolph** (the team's readings of the 2026-11-06 meeting, treated as decided for this slice): `OI-29` (match the ticket key in the branch name; several → the author picks; none → blank), `OI-31` and `OI-36` (the package shape above), `OI-32` (the path rule), `OI-33` and `OI-34` (every section needs build evidence; newest first, most recent preselected), `OI-35` (prompt, never start a build), `OI-38` (SVN will have the information). Also, a Review Section in this shape is a Platform tab of the one Review Checklist.
- **Re-running while "In preparation" is allowed.** A POST on a package still "In preparation" (after 2a1 or an outage) runs assembly again and overwrites the stored result, including any `unavailable` evidence. PRE-1 refuses only a package past "In preparation".
- **PRE-2 and PRE-3 are not checked in v0.1.0.** PRE-2 (the author's permission) needs the Identity component, which is deferred with `SEC-authenticated-access`. PRE-3 (a section needing evidence) cannot be checked before assembly, because a section is a Platform tab and the tabs are built by assembly; every section needs build evidence anyway (`OI-33`).
- **Out of scope for v0.1.0:** 2a2 (alternate change set, `OI-38`), 4a2 (the author running a build), 5a (missing checklist template), the author choosing among several branches or builds, merged-in work (`OI-30`), test and tools reviews (`OI-37`), real Jira, SVN, and Jenkins, re-running assembly once past "In preparation", and exporting the Review Checklist and Review Record.

---

## Working this document with your agent

_[Delegate: drafting the diagrams; listing the existing files a class should extend; filling the contract rows; proposing the test row for each extension; checking that every identifier this document cites exists._

_Keep human: which side of the "would a wrong guess break something" line each detail falls on; every key decision; and the approval, which is a teammate's review of the pull request._

_**The specific failure to watch for: scope that nobody asked for.** Read the sequence labels: every interaction should name the use case step it implements.]_

---

## The questions test (before you open the pull request)

_[Start a **fresh** agent session in plan mode. Give it only the use case, the business rules it cites, the architecture-of-record's section 8, and this document, and ask:_

> _List every point you would still have to guess to implement `UC-REV-assemble-materials`. For each, say what you would guess and whether a wrong guess could violate a requirement. Do not write code._

_For each item, either fix this document or keep the guess with one line saying why a wrong guess breaks no requirement. Paste the list into the pull request description under How it was verified, inside a collapsed `<details><summary>Questions test</summary> … </details>` block.]_
