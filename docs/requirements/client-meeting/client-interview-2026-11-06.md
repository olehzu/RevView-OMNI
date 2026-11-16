# Client Interview Guide

**Project:** RevView/OMNI
**Team:** Team 8
**Client:** Sumalee Rodolph, AppliedAvionics
**Meeting:** 4 of several

---

_**What this file is.** Your script going in, your meeting record coming out. Copy it once per meeting into `docs/requirements/` as `client-interview-YYYY-MM-DD.md` and commit it the same day._

_**How to use it.** Each section says what it is for, what it is worth in minutes, and whether it must happen in this meeting. Write the answers underneath in **their** words rather than yours._

## Before you go

- [x] **Three roles assigned.** Lead asks and moves the agenda, one person not four. Scribe writes and does not ask, capturing exact words, especially nouns. Observer watches what is not said. _[Lead Oleh Zubariev, scribe Ralph Castilleja; no observer recorded.]_
- [x] **Everyone has read the client's pitch slides** and written questions individually before you merged them.
- [ ] **Shortlist sent to the client the day before.** _[The agenda was the slice blockers `OI-29`, `OI-33`, and `OI-36`, then `OI-30` to `OI-32`, `OI-34`, `OI-35`, `OI-37`, `OI-38`, the quality-goal ranking, and the reminder about the checklist structure and Moderator page. Whether it was sent ahead is not recorded.]_
- [x] **This file open on the scribe's laptop.**
- [ ] **Someone owns the clock.**

## Meeting record

| | |
|---|---|
| **Date** | 2026-11-06 |
| **Time and location** | 12:00 PM, Tucker 137 |
| **Client participants** | Sumalee Rodolph (AppliedAvionics) |
| **Team participants** | Oleh Zubariev (lead), Ralph Castilleja (scribe), Francisco Lugo Gonzales, Valerie Valles, Cong Quoc Le, Ethan Nguyen |
| **Recording** | None recorded. Answers below come from the scribe's notes, plus Sumalee's written follow-up sent after the meeting (date not recorded), quoted where it is used. |
| **Photos of screens or forms** | One screenshot from Sumalee's follow-up: a VisualSVN Server listing of `dcu/tools/common/branches/ISP-BBBB/vectorcast`, file names blacked out by Sumalee. It shows each file's size, last revision, last author, and age; one file was changed by a different author "an hour ago" (revision withheld) while the rest date from four months to a year earlier. Ticket numbers in this record are placeholders (`ISP-AAAA`, `ISP-BBBB`), and author user names and revision numbers are left out, because the repository may be public. |

_This meeting worked through the open list in [OPEN-ISSUES.md](../OPEN-ISSUES.md) by number. Each answer is filed under the section it belongs to and cites its `OI-*`. The scribe's notes are partly fragmentary; fragments are quoted as written and marked for confirmation._

---

# Opening

## 1. Get to know your client

_**Must ask. 5 min.**_

**What they said:** Not covered this meeting.

---

# The business

## 2. Context and domain

_**Must ask. 5 min.** Every term you do not recognize goes in the glossary before you leave._

**What they said:** Platform names confirmed (`OI-36`): "common (everything common between falcon and phoenix)", "falcon (one project)", "phoenix (another project)".

**Terms for the glossary, in their words:**

- **Platform:** common, falcon, phoenix, as above.
- **SKU:** "we should focus on the SKU rather than the directory path. The SKU should match the branch number." Not defined in the meeting; the team reads it as the ticket number (for example `ISP-AAAA`). To confirm.
- **Tools branch** and **Jenkinsfile path:** Jenkins build parameters, alongside the branch name (`OI-34`).
- **Review package:** after the change in section 5, one checklist spreadsheet, one review record, and up to nine diff files.
- **Stretch goal:** used for `OI-37`, meaning not developed this semester.

## 3. Business drivers and objectives

_**Must ask. 5 min.**_

**What they said:** Not covered this meeting.

---

# The process

## 4. How it works today

_**Must ask. 10 min.** Ask them to show you rather than tell you._

**What they said:**

- **Branches in SVN (`OI-29`):** "On the Jira board, we can use a ticket such as ISP-AAAA to find the corresponding SVN branch. In Subversion, we can look under `dcu/applications/common`, where the branch names are listed. However, the exact path may vary depending on the code, so we should focus on the SKU rather than the directory path. The SKU should match the branch number, and we can also use the search feature to find possible matches."
- **Where changes live (`OI-36`, scribe's notes as written):** "code will be in the application folder then …. src, test in one of the ISP branches and test,". Incomplete; to confirm.
- **Jenkins builds (`OI-34`):** "All builds are labeled, and the ticket name is always included in the description. In the Jenkins parameters, we can find the branch name, tools branch, and Jenkinsfile path." And: "if someone is working on App Phoenix and commits changes to a branch, they can run a Jenkins build to test those changes. The ISP ticket number is added to the end of the build name to help identify it and see what changed in that branch. The platform, branch name, and tools branch are all important when finding the correct build, although which ones matter most depends on what is being worked on."
- **From the follow-up screenshot (`OI-32`):** "we can see that 41kb file was recently changed as part of ISP-BBBB. the system should know that since a file in tools/common/branches/ISP-BBBB was changed, that file would need to be included as part of the ISP-BBBB review under the" (the sentence ends there). _Team reading, to confirm: the path places the file in the common Platform and the tools category, so it belongs in the common-tools diff of the `ISP-BBBB` review._

**Artifacts they showed us:** The VisualSVN screenshot described in the meeting record above.

## 5. What is hard about it

_**Must ask. 5 min.** Listen for "must", "unless", "only", and "except"._

**What they said:**

- **The review package changes shape (`OI-36`, `OI-31`):** "For the checklist template, everything will remain the same as the previous version, but if a new revision is introduced, we will need to adjust how it is connected. The main change is how the review gets exported into the final review package. Instead of having three separate reviews for code, tests, and tools in the checklist, everything will now be combined into one code review. This doesn't change any of the information we already have in the project, only how it is organized and formatted in the final review package." Her written follow-up spells it out: "i dont think we're bothering to use code/tools/test anymore for the checklist spreadsheet, but there will still be that distinction for the diff files. there will also be one review record now, not one for each platform like how it was earlier. so in short, a complete review package could look like this:
  - 1 checklist spreadsheet with 3 tabs for common, falcon and phoenix. no distinction between files that are code/test/tool changes.
  - 1 review record, no distinction between common, falcon and phoenix platforms.
  - up to 9 diff files. this is because you may have worked on common, falcon, and/or phoenix, and within those platforms you may have worked on their respective code, tests and/or tools. for example in ISP-AAAA i made changes to tests in common, phoenix and falcon. then i also made changes to a tool in common. so there would be 4 diff files: common-test, phoenix-test, falcon-test, common-tool"
- **Diffs (`OI-31`):** "you have 3 platforms, and you also have test tools and code for each platform. so 9 in total."
- **Merged-in work (`OI-30`):** no answer; Sumalee does not know, and it is something the team can research.

**Rules heard (candidate `BR-*`):**

- A review package has one checklist spreadsheet with one tab per Platform (common, falcon, phoenix), one review record, and one diff file per Platform and category that the change touches, up to nine (`OI-36`, `OI-31`). _This changes `BR-review-nine-parts` and `BR-review-package-required`; see Open questions._
- Every review section needs Jenkins build or test evidence (`OI-33`): "all of them."
- Everything the author changes needs a diff and is listed in the code review (`OI-37`).
- If no matching branch is found, the branch field is left blank for now (`OI-29`).

## 6. What already works

_**Must ask. 3 min.**_

**What they said:** The checklist template stays "the same as the previous version"; only the organization of the exported package changes (`OI-36`).

## 7. Volumes and scale

_**Must ask. 3 min.**_

**What they said:** Not covered this meeting. Up to nine diff files per review (`OI-31`).

## 8. Who the users are

_**Must ask. 4 min.**_

**What they said:** Not covered this meeting.

---

# The boundaries

## 9. Constraints and rules

_**Must ask. 4 min.**_

**What they said:**

- Review types besides code review (`OI-37`): "Test and tools, and then everything u change needs a diff and listed in the code review." In the written follow-up: "OI-37 yes but we dont need to develop that or worry about it this semester - it'll be a stretch goal." _Which part is the stretch goal (separate test and tools reviews, presumably) is to confirm._
- The proposed tech stack and the quality-goal ranking were on the agenda; no answers are recorded.

## 10. External dependencies

_**Must ask. 3 min.**_

**What they said:**

- **Jenkins evidence (`OI-34`):** "we should use the most recent build." Matching uses the ticket name in the build description and name, and the branch name, tools branch, and Jenkinsfile path parameters.
- **Starting a build (`OI-35`):** "it should prompt the author."
- **Linking builds (`OI-33`, written follow-up):** "if there are existing Jenkins builds with parameters for the ticket youre starting a review for, the system should be able to recognize that. i think it would be best for it to pull up a list of builds that are associated with the branch and let the author choose which one(s) to link for their review."
- **Incomplete SVN information (`OI-38`, scribe's notes as written):** "l it will,". _Team reading, to confirm: SVN will have the information, so no alternate change set is needed._

## 11. Lifetime and who maintains it

_**Must ask. 2 min.**_

**What they said:** Not covered this meeting.

## 12. Other stakeholders

_**If there is time. 1 min.**_

**What they said:** Not covered this meeting.

---

# The close

## 13. Anything else

_**Must ask. 1 min.**_

**What they said:** Not recorded.

## 14. The read-back

_**Never skip. 5 min.**_

**What we read back, and what they corrected:** Not recorded in the scribe's notes.

## 15. Before you leave the room

_**Never skip. 4 min.**_

- [ ] **Next meeting on the calendar.** _[Not recorded.]_
- [ ] **Cadence agreed.** _[Not recorded.]_
- [x] **Contact channel and how fast they reply.** _[Microsoft Teams group chat; Sumalee answered follow-up questions in writing after the meeting.]_
- [ ] **Who to contact between meetings.** _[Sumalee Rodolph; no alternate recorded.]_
- [ ] **Copies requested** of every artifact you were shown. _[The checklist structure and the Moderator page promised on 2026-10-09 were on the agenda; whether they were sent is not recorded.]_
- [ ] **Introductions requested.** _[None.]_
- [ ] **Say what happens next.** _[Not recorded.]_

---

# After the meeting

_File everything within 24 hours, while you still remember why each answer mattered. This file is a record, not a home._

## Initial ideas

_[Solutions anyone floated, yours or theirs. Record them here and nowhere else yet.]_

- **Branch matching, the team's proposal:** look for the Jira ticket key in the branch name; if there is no single clear match, ask the author to choose or correct the branch. Sumalee added that the search feature can find possible matches and that the field can be left blank when none is found.
- **Build linking, Sumalee's suggestion:** list the Jenkins builds associated with the branch and let the author choose which to link.
- **Jenkins evidence, the team's placeholder:** mark the package as pending when it is unclear whether a section needs Jenkins evidence. Superseded by "all of them" (`OI-33`).

## Disagreements and hesitations

No observer was recorded.

- **Most recent build, or the author's choice?** In the meeting, "we should use the most recent build" (`OI-34`); in the follow-up, "let the author choose which one(s) to link" (`OI-33`). One reading reconciles them (offer the matching builds with the most recent first), but she has not said so.
- **"SKU"** was used without a definition (`OI-29`).
- **`OI-32` was answered with "the diff is just based on what you edit"**, which does not say how a file is assigned to a Platform and category. The follow-up screenshot suggests the repository path decides it.
- **Fragmentary notes:** the `OI-36` folder sentence and the `OI-38` answer ("l it will,") need confirming.

## Open questions

_[Copy each into [OPEN-ISSUES.md](../OPEN-ISSUES.md) as an `OI-*` with the person who can answer it.]_

- `OI-29` (answered, to confirm "SKU"): match the ticket number to the branch name, using search; leave the branch blank if nothing matches. Several matches not answered directly.
- `OI-30` (still open): Sumalee has no answer; the team researches it.
- `OI-31` (answered): one diff per Platform and category touched, up to nine.
- `OI-32` (partially answered): "based on what you edit"; the path rule (for example `tools/common/branches/<ticket>` means common tools) to confirm.
- `OI-33` (answered): all sections need Jenkins evidence; list the branch's builds and let the author choose which to link.
- `OI-34` (answered, to reconcile with `OI-33`): the most recent build, matched by ticket name, branch name, tools branch, and Jenkinsfile path.
- `OI-35` (answered): prompt the author.
- `OI-36` (answered): Platforms common, falcon, phoenix; one checklist spreadsheet with three Platform tabs, one review record, up to nine diffs. Templates unchanged.
- `OI-37` (answered): test and tools reviews exist; developing them is a stretch goal, not this semester.
- `OI-38` (answered, to confirm): SVN will have the information.
- Not answered or not recorded: the quality-goal ranking, the tech stack proposal, and the checklist structure and Moderator page.

**Requirements this changes (impact list needed):** the new review package shape affects `BR-review-nine-parts` (nine parts become up to nine diff files within one review), `BR-review-package-required` (one checklist with Platform tabs, one review record), the one-diff-per-package domain model in software-requirements-specification.md section 7.1, `UC-REV-assemble-materials` steps 2 to 5, `UC-REV-validate-package`, and `FR-EXPORT-legacy-format`.

---

_**Within 24 hours**, send the client your notes and the open questions. Then commit this file._
