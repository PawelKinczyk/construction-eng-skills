# Discipline: Structural

Status: v0.1, reviewed 2026-10. Target at v1.0: general only.

Scope: loads, structural systems, foundations, materials, anchors and supports for services.

This file is discipline-neutral. It does not contain standard text and it gives no numeric values for loads, factors or resistances. A value that would come from memory is named here as a quantity and marked "from the project design, to verify". Country-specific choices (national annexes, load maps, partial factors) are in the jurisdiction files. The structural engineer's design and calculations win over anything here. This repo checks coordination and completeness; it does not replace structural design.

## Systems and equipment

| System | Main elements |
|---|---|
| Superstructure frame | columns, beams, slabs (cast in place, precast, composite, timber), load-bearing walls, bracing, cores and shear walls |
| Roof structure | trusses, purlins, rafters, roof slabs, roof decking, supports for roof plant |
| Foundations | pad, strip and raft foundations, piles, ground beams, retaining walls, basement walls, waterproofing interface |
| Materials | concrete, reinforcement, structural steel, composite steel-concrete, timber, masonry, aluminium |
| Connections | welded and bolted joints, anchors (cast-in, post-installed), base plates, embedded plates, expansion joints, movement joints |
| Supports for services | hangers, brackets, trapeze supports, plant bases and frames, anti-vibration mounts, crane or hoist beams, pipe anchors and guides |
| Penetrations | sleeves, cores, wall and slab openings, trimming steel, fire-stopped openings |
| Temporary works | propping, falsework, scaffolding, shoring, excavation support, crane bases |
| Special | facade and cladding support, balustrade and guard fixings, lift pit and machine room structure, tank supports |

## Input checklists

Ask for all of these before checking or coordinating. Missing items become stated assumptions.

### Design basis
- Structural design basis document: codes used with their national annexes, design working life, consequence class, reliability class.
- Material grades: concrete class, reinforcement grade, steel grade, timber class, masonry unit and mortar.
- Geotechnical report and its recommendations: ground profile, groundwater level, bearing capacity, settlements, aggressivity of ground and groundwater.
- Structural drawings and the calculation report, with revision.

### Loads and actions
- Permanent loads: self-weight, finishes, partitions, facade, fixed plant (from the project design, to verify).
- Variable loads by use of area: imposed floor loads, roof loads, plant room loads, storage (from the project design, to verify).
- Climatic actions: snow, wind, temperature, for the site and the national annex.
- Accidental actions: impact, explosion, fire, as required by the project.
- Seismic action if the site requires it.
- Construction stage loads and loads from temporary works.

### Services loads and fixings (for the MEP designers to supply)
- Weight of each plant item: operating weight and, for tanks, weight when full.
- Footprint, support points and dynamic forces (fans, pumps, chillers, generators).
- Pipe loads: weight with contents and insulation, thermal forces at anchors, pressure thrust at bends.
- Position and size of every penetration in slabs, beams, walls and foundations.
- Fixing type for hangers and anchors, with the manufacturer's approval or assessment document.
- Hung services in fire conditions: fire resistance of the support, if required.

### Serviceability and durability
- Deflection limits for floors, beams, roofs and cantilevers, from the project design, to verify.
- Vibration criteria for floors with plant or sensitive equipment.
- Exposure class for durability, cover, crack width limit.
- Movement joint positions and the services crossing them.

### Fire
- Required fire resistance class per element, from the fire safety concept (with `fire.md`).
- Method of demonstrating fire resistance: tabulated, calculated or tested.
- Fire protection of steel and timber, and its compatibility with fixings.

## Design margins

Partial factors and combination factors come from the design codes and their national annexes. They are not given here. Do not stack extra margins on top of code factors.

| Item | Typical margin | Reason / note |
|---|---|---|
| Actions and resistances | none stated here | factors come from the design basis; state the code and annex used |
| Plant weight in loading assumptions | none stated here | use the manufacturer's weight; if the model is not chosen, state the allowance and replace it when known |
| Services loads on structure | none stated here | allowances for future services, if any, are a project decision; state the value and who set it |
| Penetration size | none stated here | structure sets the maximum opening; services must fit inside it with their insulation and fire stopping |
| Anchor design | none stated here | resistance comes from the approval document of the anchor and the design method it names |

## Typical calculations

The repo has no structural calculation script. Structural calculations are done by the structural engineer. What this repo checks is the input to those calculations and the interface with the services.

| Calculation | Inputs |
|---|---|
| Actions on the structure | permanent, variable, climatic and accidental actions from the design basis (EN 1991 series) |
| Combinations of actions | action values and combination rules (EN 1990) |
| Member resistance | material properties, section data, member geometry, design code of the material |
| Serviceability | deflection, vibration and crack limits, creep and shrinkage where relevant |
| Foundation design | ground data, loads at the base, settlement limits (EN 1997 series) |
| Fire resistance | exposure, member data, protection (the fire parts of the material codes, to verify) |
| Anchors and fixings | loads, base material, edge and spacing distances, anchor approval (EN 1992-4 for concrete, to verify) |
| Support of plant and pipework | weights, forces and positions supplied by the services designer |

Step for a services designer: take the weight, support points and dynamic force from the equipment data, send them to the structural engineer, and record the reply. Do not decide the structural capacity.

## Common errors

- Plant weight, tank weight when full, or dynamic force missing from the loads given to the structural engineer.
- Penetrations through beams, columns, walls or slabs not agreed with the structural engineer, or cut on site.
- Services supports fixed to elements that are not designed for the load (thin slab, lightweight wall, roof deck, cladding rail).
- Anchors chosen without the base material, edge distance, spacing and cracked concrete condition.
- Pipe thermal expansion forces not given to the structure at anchor points.
- Plant on a roof or a floor without a stated loading allowance and without vibration isolation.
- Penetration through a fire-rated element with no seal and no check of the element's fire resistance.
- Cores or sleeves through post-tensioned slabs or through reinforcement without scanning and approval.
- Foundation penetrations (drains, ducts, cables) not sleeved, causing settlement shear or water ingress.
- Movement joints crossed by rigid pipes or ducts without flexible connections.
- Floor build-up and slab depth in the structural drawings differ from the architectural and services sections.
- Temporary works and construction loads (stacked materials, cranes, props) not considered when installing heavy plant.
- Structure and drawings at different revisions; the services design uses an old structural layout.
- Corrosion of steel supports and anchors in wet or chlorinated rooms (pools, plant rooms) with no stated protection.
- Fire protection of structural steel damaged or missed by service supports.

## Compliance topics

Checklist seed for `code-compliance`. Each topic needs the jurisdiction's legal source and the project value.

| Topic | What to check |
|---|---|
| Design basis and actions | codes and national annexes used, design working life, consequence class, action values from the design basis (EN 1990, EN 1991 series) |
| Load combinations | combination rules and partial factors per the design code and annex; ultimate and serviceability cases (EN 1990) |
| Material design codes | concrete EN 1992; steel EN 1993; composite EN 1994; timber EN 1995; masonry EN 1996; geotechnical EN 1997; seismic EN 1998; aluminium EN 1999 |
| Serviceability | deflection, vibration, crack width and durability limits from the design basis |
| Robustness | provision against disproportionate collapse, tying, accidental actions (EN 1991-1-7, to verify) |
| Foundations and geotechnical interface | geotechnical report, geotechnical category, groundwater, settlements, interaction with basement and drains (EN 1997 series) |
| Fire resistance of elements | required class per element from the fire concept, method of verification (EN 1991-1-2 and the fire parts of the material codes, to verify) |
| Execution and materials | execution class and execution standard (EN 13670 for concrete, EN 1090 series for steel and aluminium, to verify), concrete specification (EN 206, to verify) |
| Temporary works | design of falsework, scaffolds and shoring (EN 12812 and EN 12811 series, to verify), construction stage checks |
| Inspection and testing | inspection plan, concrete testing, weld and bolt inspection, load tests if required, anchor proof tests |
| Structural coordination with MEP penetrations | list of penetrations approved by the structural engineer, sleeve details, trimming, fire stopping |
| Anchors and fixings | approval document of the anchor, design method, installation and proof testing |
| Seismic and special actions | requirement per national map and annex, if applicable (EN 1998) |
| Documentation | structural design sign-off, as-built records, inspection records, maintenance notes for the structure |

## Standards by topic

Standard numbers are references only. Never quote clause text. Give number, edition and clause, and say the user must check the licensed copy. `eu.md` lists the Eurocodes EN 1990 to EN 1999 as a range; second generation editions are in publication, so state the edition. Entries marked "to verify" are checked against a CEN, ISO or national standards body catalogue before citing.

| Topic | Standards | Status |
|---|---|---|
| Basis of structural design, combinations | EN 1990 | listed in `eu.md` (range EN 1990 to EN 1999) |
| Actions on structures | EN 1991 series (self-weight and imposed loads, snow, wind, thermal, fire, accidental, execution) | listed in `eu.md` as range; part numbers to verify |
| Concrete structures | EN 1992 series | listed in `eu.md` as range |
| Steel structures | EN 1993 series | listed in `eu.md` as range |
| Composite structures | EN 1994 series | listed in `eu.md` as range |
| Timber structures | EN 1995 series | listed in `eu.md` as range |
| Masonry structures | EN 1996 series | listed in `eu.md` as range |
| Geotechnical design | EN 1997 series | listed in `eu.md` as range |
| Seismic design | EN 1998 series | listed in `eu.md` as range |
| Aluminium structures | EN 1999 series | listed in `eu.md` as range |
| Design of fastenings in concrete | EN 1992-4 | to verify |
| Execution of concrete structures | EN 13670 | to verify |
| Execution of steel and aluminium structures | EN 1090 series | to verify |
| Concrete specification | EN 206 | to verify |
| Falsework and scaffolds | EN 12812; EN 12811 series | to verify |
| Fire classification of elements | EN 13501-2 | listed in `eu.md` |
| Information management | ISO 19650 series | to verify |

Country rules (national annexes, load maps, building structural regulations) are in the jurisdiction files. In Poland the technical conditions for buildings (WT) set the base requirements and the Polish national annexes to the Eurocodes give the national parameters. Verify against the ISAP text and the PKN catalogue before citing.

## Coordination interfaces with the MEP disciplines

| With | Services give structure | Structure gives services | Typical conflict |
|---|---|---|---|
| `hvac.md` | plant weights, dynamic forces, support points, penetration list, roof plant layout, duct and pipe weights | slab and beam depths, permitted openings, support details, vibration isolation limits | AHU on a roof slab not checked; large duct through a beam |
| `plumbing.md` | tank weights when full, pipe loads, penetrations, stack positions, pump set bases | sleeve and core approval, floor depth for falls, foundation penetration details | stack core through a beam; tank load not given |
| `electrical.md` | transformer, generator, UPS, battery and switchgear weights, cable tray loads, riser openings | plant bases, openings, trench and duct details, fire stopping support | transformer room slab not designed for the load; riser openings cut after the slab is cast |
| `fire.md` | sprinkler pipe and tank weights, pump and tank bases, penetrations through fire elements | fire resistance of elements, protection of steel, supports with the required fire rating | sprinkler hangers on fire-protected steel; tank on a slab not checked |
| `architecture.md` | none | grid, columns, walls, slab edges, levels, ceiling zones, openings | beam in the ceiling void; wall type differs from the architectural drawing |

## Drawing and document deliverables

- Structural general arrangement drawings: foundation, floor, roof and section plans, with revision.
- Reinforcement or steel member drawings and connection details.
- Structural design basis and the calculation report, with the codes and annexes.
- Opening and penetration schedule: position, size, element, approval status, who approved.
- Services load schedule: weight, support points, dynamic forces, for each item of plant.
- Fixings and anchor schedule with the approval documents.
- Specification of materials, execution class and tolerances.
- Inspection and testing plan and the records (concrete, welds, bolts, anchors).
- Temporary works design and construction stage drawings where required.
- Geotechnical report and foundation recommendations.

## Common review comments

- Provide plant weights, support points and dynamic forces for the structural check.
- Provide the penetration schedule and get the structural engineer's approval before coring or cutting.
- State the base material and anchor approval for each fixing.
- Show sleeves and trimming steel at the penetrations through beams and walls.
- Check the slab depth and the beam depths against the services section.
- State the loading allowance on the plant slab and who set it.
- Show the fire rating of structural elements and the seal at each penetration.
- Show flexible connections where services cross movement joints.
- Align the structural drawing revision with the architectural and services drawings.
- State the corrosion protection for supports in wet or aggressive rooms.

## What to verify

- Design basis, codes and national annexes are stated and current.
- Loads used for plant and services come from the manufacturer's data and the project design, not from memory.
- Every penetration has an approval from the structural engineer and a seal where fire-rated.
- Anchors have an approval document and the design inputs (base material, edge distance, spacing) are known.
- Deflection, vibration and durability limits are taken from the project design, with the source.
- Fire resistance class per element is the fire concept's value.
- Structural, architectural and services drawings are at agreed revisions.
- Geotechnical report conditions (groundwater, aggressivity) are reflected in foundation and drainage details.
- Standard numbers marked "to verify" are checked against a CEN, ISO or national standards body catalogue before citing.
- Country values come from the jurisdiction file, with the legal source.
