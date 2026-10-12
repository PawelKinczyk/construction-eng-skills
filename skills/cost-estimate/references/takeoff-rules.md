# Quantity takeoff rules

Quantity rules by type of work, plus the measurement systems commonly named in contracts. This file does not replace the measurement standard the contract names: read that standard and follow it. When it conflicts with this file, the contract wins.

## 1. Measurement standards by country

| Country / contract | Measurement system |
|---|---|
| Poland | KNR and KNNR catalogues: the norm itself states the measurement unit and what is included; the measurement rules are in the catalogue "założenia ogólne" |
| UK | NRM2 (building works) or CESMM4 (civil engineering) |
| US | MasterFormat with the estimator's own or the client's measurement rules |
| International | CESMM4, or a project-specific measurement rule in the tender documents |

Two rules that hold everywhere:
- Measure the finished work, net, unless the standard says otherwise. Do not measure waste, laps or overlaps unless the standard includes them.
- Deduct openings above the threshold the standard sets; state the threshold you used.

## 2. Common quantities

| Work | Unit | Rule of thumb (state the source and check it) |
|---|---|---|
| Area of a floor or ceiling | m2 | plan area, net of openings above the standard threshold |
| Internal wall | m2 | length x height to the structural soffit; deduct openings |
| Wall or floor volume | m3 | area x thickness |
| Formwork | m2 | contact area of concrete with the formwork |
| Concrete | m3 | net volume of the element |
| Reinforcement | t or kg | from the bar schedule or the model; if neither, from a steel ratio per m3 of concrete, stated as an assumption |
| Roofing, cladding | m2 | developed area on the slope, not the plan area |
| Thermal insulation | m2 | area of the insulated surface, net of openings |
| Pipework | m | centreline length by diameter and material; state if fittings are included |
| Ductwork | m2 or m | m2 is the standard for pricing: developed surface area; state the method |
| Cables and wiring | m | route length with the reserve the standard allows |
| Cable tray, conduit | m | route length |
| Equipment | pieces (Nr, szt, kpl) | per schedule; state whether installation is included |
| Excavation | m3 | in situ volume before excavation; state whether backfill and disposal are separate |
| Painting | m2 | painted surface, developed |

## 3. Takeoff from drawings, schedules or a model

1. Fix the revision of every drawing used. A takeoff without a revision is not usable.
2. Prefer schedules and the model over scaling from a drawing. Where you must scale, say so and state the scale.
3. Take the model quantities from `ifc-analysis` (IfcQto quantities, Psets) or from `dxf-dwg-analysis` (areas, block counts). State which quantity set and which parameter was used.
4. Cross-check by a second method at least once per group: for example the model volume against area times thickness, or the total pipe length against the plan layout.
5. Record the count of items per type (for example: 12 fan coil units, 3 AHU) and compare with the schedule.
6. Where a quantity is missing and cannot be measured, leave the line and mark the quantity "to verify". Never fill a quantity from another project.

## 4. Rules of thumb for early estimates

Use these only when no takeoff is possible, and say clearly that the estimate is a rate per unit of the building, not a takeoff.

| Basis | Use |
|---|---|
| Cost per m2 of gross floor area | early comparison between options |
| Cost per m3 of building volume | early comparison between options |
| Percentage split by trade | checking whether one group in an estimate is out of proportion |
| Cost per bed, per seat, per kW of installed capacity | early estimates for a building type with known benchmarks |

Benchmark values differ by country, building class and year. Take a benchmark from a named published source with its date, or from the client's own data. Never present a benchmark from memory as a fact.

## 5. Takeoff quality check

- Every line has a quantity, a unit, a source (drawing and revision, schedule, model, measurement sheet) and a measurement rule.
- Areas and volumes are internally consistent (for example the sum of wall areas against the floor area).
- Units are uniform per line type across the estimate.
- Deductions applied (openings, voids, no-work zones) match the standard's thresholds.
- Quantities for identical elements (for example three identical floors) are repeated deliberately, with the count stated, not approximated by a single figure.
- Anything measured from an early revision or scaled from a drawing is listed in "to verify".
