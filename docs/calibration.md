# Calibration

**Project:** RevView/OMNI
**Team:** Team 8

One row per estimate. **Actual** is the hours logged on weekly activity report lines tagged with the use case's ID since the estimate was made. **Ratio** is actual divided by midpoint: multiply both ends of the next estimate by it. The **biggest miss** is the owner's one-sentence answer from the retrospective held when the use case closes.

| Use case | Estimate | Made | Range (h) | Midpoint (h) | Actual (h) | Ratio | Biggest miss |
|---|---|---|---|---|---|---|---|
| `UC-REV-assemble-materials` | Coarse | 2026-10-19 ([#28](https://github.com/olehzu/RevView-OMNI/issues/28): clarify and design 2–3, build and review 2–6, verify 2–3) | 6–12 | 9 | ~10 | 1.1 | Preparation missed most: we did not have the client's answers to the slice blockers (`OI-29`, `OI-33`, `OI-36`) until 2026-11-06, so next time we ask Sumalee as soon as a blocker is found. |
| `UC-REV-assemble-materials` | Refined | Not made | — | — | — | — | No refined estimate was written on the issue before building; write one before the next use case's build starts. |

**Notes on the first row**

- **Actual is the owner's approximate total** (Oleh Zubariev, 2026-11-09): about 10 hours for preparation before building plus the design and build, not yet summed from tagged weekly activity report lines. Replace it with the summed figure when the reports are checked.
- The use case was closed by [#43](https://github.com/olehzu/RevView-OMNI/pull/43) and released as [v0.1.0](https://github.com/olehzu/RevView-OMNI/releases/tag/v0.1.0) on 2026-11-09.
