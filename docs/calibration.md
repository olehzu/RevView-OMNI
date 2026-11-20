# Calibration

**Project:** RevView/OMNI
**Team:** Team 8

One row per estimate. **Actual** is the hours logged on weekly activity report lines tagged with the use case's ID since the estimate was made. **Ratio** is actual divided by midpoint: multiply both ends of the next estimate by it. The **biggest miss** is the owner's one-sentence answer from the retrospective held when the use case closes.

| Use case | Estimate | Made | Range (h) | Midpoint (h) | Actual (h) | Ratio | Biggest miss |
|---|---|---|---|---|---|---|---|
| `UC-REV-assemble-materials` | Coarse | 2026-10-19 ([#28](https://github.com/olehzu/RevView-OMNI/issues/28): clarify and design 2–3, build and review 2–6, verify 2–3) | 6–12 | 9 | 6 | 0.67 | Preparation missed most: we did not have the client's answers to the slice blockers (`OI-29`, `OI-33`, `OI-36`) until 2026-11-06, so next time we ask Sumalee as soon as a blocker is found. |
| `UC-REV-assemble-materials` | Refined | Not made | — | — | — | — | No refined estimate was written on the issue before building; write one before the next use case's build starts. |

**Forecast:** Applying the exact team ratio (6 ÷ 9 = 2/3) to the 6–12 h range gives a 4–8 h forecast for a comparable estimate.

**Individual actuals and ratios**

| Team member | Actual (h) | Ratio (actual ÷ 9 h) |
|---|---:|---:|
| Oleh Zubariev | 1 | 1/9 ≈ 0.11 |
| Ralph Castilleja | 1 | 1/9 ≈ 0.11 |
| Francisco Lugo Gonzales | 1 | 1/9 ≈ 0.11 |
| Valerie Valles | 1 | 1/9 ≈ 0.11 |
| Cong Quoc Le | 1 | 1/9 ≈ 0.11 |
| Ethan Nguyen | 1 | 1/9 ≈ 0.11 |
| **Team total** | **6** | **6/9 ≈ 0.67** |

**Notes on the first row**

- Each of the six team members reported 1 hour on weekly activity report lines tagged `UC-REV-assemble-materials`.
- The use case was closed by [#43](https://github.com/olehzu/RevView-OMNI/pull/43) and released as [v0.1.0](https://github.com/olehzu/RevView-OMNI/releases/tag/v0.1.0) on 2026-11-09.
