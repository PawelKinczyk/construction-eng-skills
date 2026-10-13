# Discipline: Architecture

Status: v0.1, reviewed 2026-10. Target at v1.0: general only.

Scope: space planning, building envelope, doors and windows, finishes, accessibility, egress.

This file is discipline-neutral. It does not contain standard text and it gives no numeric limits. A value that would come from memory is named here as a quantity and marked "from the project design, to verify". Country rules are in the jurisdiction files. The architect's design, the approved permit design and the fire safety concept win over anything here. Always state which source you used.

## Systems and equipment

| System | Main elements |
|---|---|
| Space planning | functional layout, room schedule, circulation, core (stairs, lifts, shafts), plant rooms, risers, ceiling zones and floor build-ups |
| Building envelope | external walls, roof, ground floor slab, thermal insulation, air and vapour layers, thermal bridges, parapets, roof terraces, balconies |
| Facade and glazing | curtain walling, windows, glazed doors, rooflights, shading (fixed, movable), safety glazing, fixings and brackets |
| Doors and openings | internal and external doors, fire-rated doors, smoke control doors, automatic doors, access control hardware, hatches, louvres and wall openings for services |
| Vertical circulation | stairs, ramps, passenger lifts, evacuation or fire lifts, escalators, handrails and guards |
| Finishes | floor, wall and ceiling finishes, suspended ceilings, raised floors, partitions (dry-lining, masonry), acoustic linings |
| Accessibility | step-free routes, accessible toilets, accessible parking, tactile and visual wayfinding, lift and door dimensions |
| Egress | escape routes, exit doors, exit widths, protected stairs and lobbies, refuge areas (with `fire.md`) |
| Fire interface | compartment walls and floors, fire-rated doors, penetration seals, shaft enclosures, facade and cavity barriers (with `fire.md`) |

## Input checklists

Ask for all of these before checking or coordinating. Missing items become stated assumptions.

### Building definition
- Building use and occupancy per room or zone, and the expected number of people.
- Number of storeys above and below ground, building height and floor-to-floor heights (from the project design, to verify).
- Gross, net and usable areas and the measurement rule used for each (see "Areas, heights and measurement" under Compliance topics).
- Permit design (projekt budowlany or national equivalent), its revision, and any conditions attached to it.
- Fire safety concept and the fire compartment plan.

### Layout and room schedule
- Room data sheets: use, finish, ceiling height, services expected, acoustic and thermal class.
- Plans, sections and elevations at a stated scale and revision; coordinated reflected ceiling plans.
- Core, shaft and riser locations with their internal dimensions.
- Plant rooms, roof plant and external plant areas with access routes and equipment lifting paths.

### Envelope
- Wall, roof and floor build-ups with layer thicknesses and materials.
- Required thermal transmittance (U-value) per element, from the project design, to verify.
- Window and door schedule: size, type, glazing, frame, safety class, fire class, acoustic class.
- Airtightness target and the shading strategy.
- Openings in the envelope needed by services (louvres, intakes, exhausts, penetrations) and their positions.

### Accessibility and egress
- Accessibility requirements that apply to the use and the jurisdiction.
- Escape route plan: travel distances, exit widths, number of exits, stair widths (all from the fire concept, to verify).
- Door swing, direction of escape, locking and access control on escape routes.

### Acoustics and daylight
- Acoustic requirements per room pair and per facade (airborne, impact, facade insulation, service equipment noise).
- Daylight and view-out requirements and the room orientation.
- Site noise survey if the project is near road, rail or air traffic.

### Finishes and fire reaction
- Reaction-to-fire class required per surface and per location (route, room, facade).
- Floor loadings and floor finish limits (with `structural.md`).

## Design margins

Architecture has no safety factors in the engineering sense. The entries below are coordination allowances. Never stack them: apply each at one level and state the reason.

| Item | Typical margin | Reason / note |
|---|---|---|
| Ceiling void for services | none stated here | the void is a result of the coordinated services section, not a percentage; take it from the project design |
| Shaft and riser size | none stated here | take it from the services designers' sizes plus insulation, supports, access and fire stopping; state the allowance used |
| Plant room size | none stated here | take it from the equipment dimensions, service clearance from manufacturer data, and routes for replacement |
| Opening in the envelope | none stated here | size to the free area and the louvre or duct sizes in the services design; confirm with the architect before issue |
| Dimensional tolerance | none stated here | state the construction tolerance used for clearances; take it from the specification or the execution standard |

## Typical calculations

The repo has no architecture calculation script. Architecture is mainly checked against given values. Calculations done by the architect or a specialist, and the inputs needed to review them:

| Calculation | Inputs |
|---|---|
| Thermal transmittance of an element | layer thicknesses, thermal conductivity of each material, surface resistances, bridging effects (EN ISO 6946; thermal bridges EN ISO 10211) |
| Energy performance of the building | envelope data, systems data, use profile (EN ISO 52000 series; national method in the jurisdiction file) |
| Sound insulation between rooms and of the facade | element data, flanking paths, room volumes (EN ISO 12354 series) |
| Daylight provision | room geometry, window size and transmittance, obstructions, orientation (EN 17037, to verify) |
| Egress width and travel distance | occupant number, exit and stair widths, route lengths (from the fire concept) |
| Areas and volumes | measured from the drawings by the stated rule |

For services-related checks (condensation, overheating, ventilation openings), the numbers come from the services designer's calculation. Do not replace them with an estimate.

## Common errors

- Ceiling, floor and shaft build-ups drawn without the services: duct, pipe, tray and sprinkler zones do not fit.
- Riser or shaft too small once insulation, supports, access and fire stopping are included.
- Plant room without a route for installation and replacement of the largest item, or without ventilation and drainage provision.
- Openings in fire walls, floors and shafts not shown on the architectural drawings, or shown without the fire class of the seal.
- Fire-rated door or wall drawn but a duct, cable tray or pipe passes through with no damper or seal.
- Facade louvre free area smaller than the services design needs, or intake and exhaust placed close together.
- Door schedule mismatch: fire class, swing direction or hardware differs from the fire concept or the access control design.
- Accessibility route interrupted by a step, a heavy door, a narrow lift or a service obstruction.
- Wall and floor build-up without the acoustic layers that the room pair requires; noisy plant next to quiet rooms.
- Thermal bridge or air barrier broken by a service penetration or a bracket.
- Glazing that needs safety glass (low sill, door, balustrade, overhead) not marked as such.
- Plans, sections and schedules at different revisions; room names or numbers differ between disciplines.
- Roof layout without access, fall arrest and loading allowances for roof plant.
- Finish reaction-to-fire class not checked against the route or room it is used in.
- Floor finish or raised floor height not coordinated with the structure and the services below.

## Compliance topics

Checklist seed for `code-compliance`. Each topic needs the jurisdiction's legal source and the project value.

| Topic | What to check |
|---|---|
| Accessibility | step-free routes, door and corridor clear widths, lift size, accessible toilets, parking, signage (EN 17210 as a reference; national rules in the jurisdiction file) |
| Fire compartmentation interface | compartment boundaries on the plans, fire class of walls, floors, doors and shafts, seals at penetrations (with `fire.md`) |
| Egress | number and width of exits, travel distances, stair and corridor widths, door swing, locks on escape routes, refuge areas (with `fire.md`) |
| Daylight and sunlight | daylight in rooms for long occupancy, distance to neighbouring buildings, overshadowing rules |
| Acoustics | airborne and impact insulation between rooms, facade insulation, noise from services, limits per use |
| Thermal envelope | U-values, thermal bridges, airtightness, condensation and mould risk, overheating, energy performance requirement |
| Areas, heights and measurement | building height, number of storeys, floor and use area, plot coverage, set-backs, and the measurement rule used |
| Facade and glazing safety | safety glazing locations, falling glass, guards and balustrades, cleaning and maintenance access, wind load resistance, facade fire spread |
| Doors and ironmongery | fire and smoke doors, exit devices, automatic doors, access control on escape routes |
| Stairs, ramps, guards | going, rise, handrail, guard height and loading (loading with `structural.md`) |
| Ventilation and openings | openings for natural ventilation, intake and exhaust distances, ventilation of habitable rooms (with `hvac.md`) |
| Finishes and fire reaction | reaction-to-fire class by location, floor slip resistance, emissions where required |
| Environment and sustainability | energy certificate, material declarations, certification scheme if the client requires one |
| Information management | model and document exchange rules if required (ISO 19650 series, to verify scope) |

## Standards by topic

Standard numbers below are references only. Never quote clause text. Give number, edition and clause and say the user must check the licensed copy. Entries marked "listed in `eu.md`" are in the EU standards map; the rest are "to verify" against a CEN, ISO or national standards body catalogue before citing.

| Topic | Standards | Status |
|---|---|---|
| Accessibility of the built environment | EN 17210 | listed in `eu.md` |
| Thermal transmittance, thermal bridges | EN ISO 6946; EN ISO 10211 | listed in `eu.md` |
| Energy performance of buildings | EN ISO 52000 series | listed in `eu.md` |
| Acoustics in buildings | EN ISO 12354 series | listed in `eu.md` |
| Sound insulation rating of results | ISO 717 series | to verify |
| Fire classification | EN 13501-1; EN 13501-2 | listed in `eu.md` |
| Fire door test | EN 1634-1 | to verify |
| Daylight in buildings | EN 17037 | to verify |
| Windows, external doors | EN 14351-1; air, water and wind classes EN 12207, EN 12208, EN 12210 | to verify |
| Curtain walling | EN 13830 | to verify |
| Glass impact behaviour | EN 12600 | to verify |
| Laminated and insulating glass | EN 14449; EN 1279 series | to verify |
| Exit devices on escape routes | EN 179; EN 1125 | to verify |
| Power operated pedestrian doors | EN 16005 | to verify |
| Area and space indicators | ISO 9836 | to verify |
| Information management with BIM | ISO 19650 series | to verify |

Country rules for accessibility, daylight, heights, areas and egress are in the jurisdiction files. In Poland the technical conditions for buildings (WT) are the base; verify the paragraph numbers against the ISAP text before citing.

## Coordination interfaces

What architecture gives to, and takes from, each discipline. Each row is a question to close in coordination.

| With | Architecture provides | Architecture needs | Typical conflict |
|---|---|---|---|
| `hvac.md` | plant rooms, shafts, ceiling voids, facade openings, roof layout, acoustic requirements | duct and pipe sizes, free areas of louvres, plant weights and noise, service clearances | duct does not fit the void; louvre too small; plant noise near quiet rooms |
| `plumbing.md` | wet room layout, shafts, floor falls, floor build-up | pipe routes, stack positions, drain falls, plant and tank sizes | stack passes through a room it should not; floor build-up too thin for falls |
| `electrical.md` | electrical rooms, risers, ceiling layout, luminaire positions, door and access control schedule | cable route widths, board sizes, ventilation and heat from rooms, luminaire and device positions | riser too small; board room without clearance and access |
| `fire.md` | compartment boundaries, door and wall fire classes, stairs, escape routes, facade design | fire concept, damper and seal positions, smoke vents, hydrant and sprinkler plant space | seal missing at a penetration; smoke vent area not on the facade |
| `structural.md` | layouts, openings, floor-to-floor heights, finishes loads, facade loads | slab and beam depth, column and wall positions, opening limits, deflection limits | beam in the ceiling void; opening cut in a structural wall |

## Drawing and document deliverables

- General arrangement plans, sections and elevations with a revision and a date.
- Reflected ceiling plans, coordinated with the services.
- Room data sheets and a room schedule.
- Door, window and ironmongery schedules with fire, acoustic and safety classes.
- Wall, floor, roof and facade build-up details, with penetration details for services.
- Fire compartment plan and escape route plan (coordinated with the fire designer).
- Shaft, riser and plant room drawings with the dimensions the services designers need.
- Accessibility statement or compliance notes, and area schedule with the measurement rule stated.
- Facade and glazing specifications, and safety glazing locations.
- Model or drawing register and the issue status (ISO 19650 series, to verify if the project uses it).

## Common review comments

- State the revision of the architectural drawing the services design is based on.
- Show all fire-rated walls, floors and doors on the services drawings, and the seal at each penetration.
- Dimension the shaft or riser, including insulation, supports and access.
- Show the ceiling build-up and the services zone on the coordinated section.
- Confirm the facade opening free area against the services design.
- Show the route for plant installation and replacement.
- Mark the acoustic requirement for rooms next to plant.
- Mark the safety glazing locations.
- State the accessibility route and the clear widths of doors and lifts.
- Reconcile room numbers, names and use between architecture and services drawings.

## What to verify

- The fire safety concept and the compartment plan are the current revision.
- Escape widths, travel distances and exit counts match the fire concept (not a remembered value).
- Every penetration of a fire-rated element has a stated seal, damper or sleeve.
- Shaft, riser and plant room sizes equal the services designers' dimensions plus the stated allowances.
- U-values, airtightness and acoustic ratings are given from the project design, with the source.
- Safety glazing locations are marked and the class is stated.
- The measurement rule for each area or height is stated.
- Standard numbers marked "to verify" are checked against a CEN, ISO or national standards body catalogue before citing.
- Country values come from the jurisdiction file, with the legal source.
