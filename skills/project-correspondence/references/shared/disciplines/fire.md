# Discipline: Fire protection

Status: v0.1, reviewed 2026-10. Target at v1.0: full.

Scope: sprinklers and water extinguishing, hydrants and fire water supply, detection and alarm, smoke and heat control, passive fire protection, extinguishers, gas suppression, fire service access.

Values in this file marked "rule of thumb" or "typical" are design practice, not law and not standard text. Fire safety requirements are set by national fire law and by the fire safety concept (scenariusz pożarowy) for the building. For fire, the national law and the fire safety expert's concept win over every typical value here. Always state which source you used.

## Systems and equipment

| System | Main equipment |
|---|---|
| Water extinguishing | sprinkler system (wet, dry, pre-action, deluge), water mist, foam, hydrant system, fire pumps (main, jockey, diesel or electric), water storage (tank, reservoir), pipes and valves |
| Fire water supply | fire hydrants (external, internal), hose reel systems, wet riser and dry riser, fire mains, connection from the network or a dedicated tank |
| Detection and alarm | fire detection and alarm system (SAP/DSO), automatic detectors (optical, heat, aspiration), manual call points, alarm devices (sounders, beacons), control and indicating equipment, monitoring link |
| Smoke and heat control (SHD) | smoke exhaust fans, natural smoke vents, smoke shafts and ducts, smoke dampers, make-up air inlets, pressure differential systems (pressurisation of staircases and lobbies), smoke curtains |
| Passive protection | fire compartments and elements with a fire resistance class, fire doors and shutters, penetrations seals, fire dampers and smoke dampers, reaction-to-fire materials, fire stopping of joints |
| Evacuation | escape route layout, exit and evacuation lighting (with `electrical.md`), exit signs, evacuation plans, lifts for evacuation or for the fire service |
| Extinguishers and manual | portable extinguishers, extinguishing blankets, hydrant cabinets, signage |
| Gas suppression | inert and chemical agents, room tightness, hold time, pressure relief, warning and release controls |
| Fire service access | access roads, hardstanding, fire lift, firefighting lobby, smoke control for the fire service, hydrant connection points |
| Fire structure and facades | facade fire spread, roof structures, external fire spread, curtain walling and cavity barriers |

## Input checklists

Ask for all of these before sizing. Missing items become stated assumptions.

### Fire safety concept
- The fire safety concept (scenariusz pożarowy) and the fire safety expert's opinion, if required.
- Building use and category per the national fire classification (in Poland: ZL, PM, IN, and their sub-categories).
- Fire zones: area and height limits per zone, compartmentation plan.
- Number of floors, height above and below ground, and the fire zones by height.
- Evacuation strategy: simultaneous or phased, protected staircases, evacuation lifts, refuge spaces.
- Fire load and occupancy density per zone, and any special hazard (storage, high-rack, vehicles, server rooms, kitchens).
- Whether automatic extinguishing and automatic detection are required, and by which rule.

### Sprinkler system
- Occupancy or hazard class per the standard (EN 12845 or the national rule), and the design density.
- Design area (operating area) and the assumed number of operating heads.
- Sprinkler head type, temperature rating and response class (К-factor, K-factor), spacing per the standard.
- Water supply: reliability source, tank volume, pump set, connection to the network.
- Hose allowance (added flow for hydrants or hose reels) and the water supply duration from the standard.
- Maximum and minimum operating pressure, and the pipe material and joint type.
- Approval requirement on the products and on the installer (for example CNBOP-PIB in Poland).
- Areas not sprinklered, and their justification.

### Fire water supply and hydrants
- Required flow and pressure from the national rule and the water supply regulation.
- Source: network, tank, reservoir, or a combination, and its reliability.
- Pump arrangement, redundancy, and the time to start.
- Hydrant locations, spacing, and the fire service connection points.
- Water reserve for fighting the design fire, and the refill time.

### Detection and alarm
- Areas to be monitored, and the detection principle for each (smoke, heat, flame, aspiration, linear heat).
- Coverage and spacing for the chosen detector, per the standard, and the room height limit.
- Environment: dust, steam, cooking vapour, vehicles, cold, moisture; areas where optical detectors will false alarm.
- Cause and effect matrix: what each signal triggers (alarm, shutdown, door release, smoke control, evacuation).
- Alarm devices, alarm zones, and the link to the fire service or to a monitoring station.
- Interface with smoke control, lifts, doors, dampers, gas suppression and BMS.

### Smoke and heat control
- Method: natural smoke exhaust, mechanical exhaust, pressure differential (pressurisation), or a combination, and the rule or concept that requires it.
- Smoke zones and smoke reservoirs, area and height, balcony or channelling depth.
- Design fire size (kW), location and the smoke production rate.
- Make-up air: path, velocity, and temperature.
- Temperature class of the exhaust fans and ducts (F class), and the duration required.
- Areas that must stay clear of smoke: escape routes, firefighting routes, protected lobbies.
- Control layers (activate by zone), and the interface with the detection system and the doors.

### Passive protection
- Required fire resistance (R, E, I or REI class) for each element, from the national rule.
- Compartment boundaries, shaft walls, and the floor and wall construction type.
- Openings: doors, shutters, glazing, dampers, conveyors, ducts, cable penetrations.
- Fire doors with their class, self-closing or hold-open, and their release on alarm.
- Fire dampers and smoke dampers in ducts at compartment and shaft boundaries (with `hvac.md`).
- Sealing systems for pipes, cables and joints, with the test standard and the approval.
- Facade and roof provisions: cavity barriers, fire stops, and the reaction-to-fire class of materials.

### Gas suppression and extinguishers
- The hazard, the room volume and the room tightness (door and duct leakage).
- Extinguishing agent, design concentration, hold time and discharge time.
- Occupancy during discharge and the warning and delay time needed for evacuation.
- Pressure relief and room ventilation after discharge.
- Portable extinguisher types, sizes, travel distance and location.

## Design margins

Rules of thumb. Always state the margin and the reason. Never stack margins: apply each margin once, at one level.

| Item | Typical margin | Reason / note |
|---|---|---|
| Sprinkler design density | none | the density and the design area come from the standard or the concept. Do not add a percentage |
| Sprinkler design area | per the standard, for the hazard and the ceiling type | state the area and the assumed number of heads |
| Hose allowance | added flow per the standard | it is part of the formula, not a margin |
| Fire pump flow | none above the calculated demand | the pump duty already includes the hose allowance |
| Fire pump head | small margin only if the hydraulic calculation is uncertain, stated | a large margin oversizes the pump and can change the actual flow |
| Water reserve | from the standard duration times the demand | do not add a percentage; check the refill time instead |
| Smoke exhaust flow | none; the design fire and the concept set it | a margin changes the smoke layer control, not only the cost |
| Pressurisation air | the standard's method sets it | check the door opening force, do not "add air" |
| Detection coverage | per the standard spacing | a margin means more detectors than needed and more false alarms |
| Fire resistance of elements | the required class exactly, per the rule | going up a class is a cost decision for the client, not a default |
| Compartmentation | exactly as the concept and the rule require | do not extend compartments casually; each change affects the whole concept |

Fire designs are checked against the law and the standard, not against a margin. State every assumption and keep the calculation reproducible.

## Typical calculations

Script: `scripts/fire_calc.py` (in `equipment-selection`). Fire pump power and pipe pressure drop use `scripts/hvac_calc.py` (`pump-power`, `pipe-dp`).

| Calculation | Command |
|---|---|
| Sprinkler design flow | `sprinkler-flow --density 5 --area-m2 216 [--hose-allowance-l-min 900]` |
| Fire water reserve | `water-reserve --flow-l-min 1800 --duration-min 60` |
| Smoke exhaust flow from an air change rate | `smoke-exhaust --volume-m3 12000 --ach 10` |
| Smoke exhaust flow from a design fire | `smoke-exhaust --fire-kw 3000 --height-m 4 --method plume` |
| Detector count from spacing | `detector-count --area-m2 1200 --spacing-m 10 [--factor 1.0]` |
| Fire pump head and power | `pump-power --flow-m3h (--head-m | --dp-kpa) [--eff]` |
| Pipe pressure drop of the sprinkler network | `pipe-dp --flow-m3h --id-mm --length-m [--zeta]` |

The design density, the design area, the water supply duration and the detector spacing are NOT in the script. Take each from the standard or the fire safety concept, state the source, and give the clause.

Rules of thumb (check against the standard and the concept):

| Item | Typical value |
|---|---|
| Sprinkler flow from density and area | Q [l/min] = density [mm/min] * area [m2] |
| Water supply duration, ordinary hazard sprinklers | often 60 min; check the standard and the concept |
| Hose allowance | per the standard, added to the sprinkler flow |
| Fire pump pressure measurement point | at the sprinkler valve or the hydrant, per the standard |
| Smoke exhaust, natural vents | per the concept and the standard; no universal value |
| Smoke exhaust, mechanical | from the design fire, the smoke layer height and the temperature class |
| Pressurisation of staircases | pressure differential and door force limits per the standard |
| Fire damper testing | integrity and leakage per the test standard, with the classification report |
| Portable extinguisher travel distance | per the national rule, per extinguisher class |
| Fire service access road width and bearing | per the national rule |

National requirements for the density, the duration, the categories and the smoke control methods are in the jurisdiction files. Use them, not the values above, when they differ.

## Common errors

- Sprinkler design density, design area or hazard class taken from memory instead of the standard or the concept.
- Sprinkler flow without the hose allowance, or the hose allowance counted twice.
- Water supply not reliable: a single connection to the network with no tank, and no check of the network pressure at the design flow.
- Pump curve checked only at the nominal point, not at the design flow and pressure at the sprinkler valve.
- Pump starting and changeover not checked against the standard (jockey pump, diesel start, pressure switch settings).
- Water reserve volume taken as a round number instead of the demand times the duration.
- Detection type wrong for the environment, so false alarms disable the system.
- Detector spacing and the ceiling height limit not checked, so coverage has holes or the detector is outside its rating.
- Cause and effect matrix incomplete: doors, dampers, smoke control, lifts and shutdowns not all covered.
- Smoke control and the detection zones not coordinated, so the wrong zone activates.
- Make-up air missing or too small, so the smoke exhaust does not perform; door opening force too high in a pressurised staircase.
- Smoke damper or fire damper missing at a compartment boundary, or the duct fire resistance class lower than the element it crosses.
- Fire stopping of a penetration with an unapproved system, or a class lower than the element.
- Fire doors held open with no release, or with the wrong release mechanism.
- Compartment boundaries broken by later service routes (ducts, cables, conveyors, laundry chutes).
- Facade cavity barriers and fire stops missing, so fire spreads in the cavity.
- Reaction-to-fire class of materials not checked in escape routes and on facades.
- Evacuation lighting and exit signs not coordinated with the escape strategy.
- Product approvals (CE marking, national approval such as CNBOP-PIB) not checked for fire products.
- The concept and the design documents not consistent, so the fire safety expert cannot assess the design.

## Compliance topics

Checklist seed for `code-compliance`. Each topic needs the jurisdiction's legal source and the project value.

| Topic | What to check |
|---|---|
| Fire safety of the building | national fire regulations and the technical building rules for the building use and category |
| Fire safety concept and expert opinion | when an opinion of a fire safety expert (rzeczoznawca) is required, and its scope |
| Fire compartments | area, height and separation limits, and the resistance class of elements |
| Escape routes and evacuation | number, width, length and protection of routes, and the evacuation strategy |
| Smoke and heat control | when required, the method, and the standard or concept used |
| Sprinklers and water extinguishing | when required, the standard applied, the water supply duration |
| Fire water supply and hydrants | required flow and pressure, the source, the reserve |
| Detection and alarm | when required, the categories and the interface with other systems |
| Gas suppression | when permitted for occupied rooms, concentration and warning time |
| Fire dampers and ducts | location, class, approval, and the alarm interface (with `hvac.md`) |
| Electrical installations for fire | fire-rated circuits, the supply to fire pumps, smoke control and alarms (with `electrical.md`) |
| Fire-rated cable circuits | required circuit endurance time for each safety system, cable reaction-to-fire class (EN 50575, number only), fire-resistant supports and fixings, penetration seals, and whether the cable type is approved for the use |
| Fire service access | access roads, hardstanding, fire lifts, firefighting lobbies, connection points |
| Product approvals | CE marking and national approvals for fire products, and the installer competence |
| Maintenance and testing | inspection and test regime required by law, and the records |
| Handover documents | the fire safety instruction (instrukcja bezpieczeństwa pożarowego) and the as-built fire documents |

## Standards by topic

See `eu.md` "Standards map by topic" for EN numbers (EN 12845 sprinklers, EN 671 hose systems, EN 54 series and CEN/TS 54-14 detection, EN 12101 series smoke and heat control, EN 13501-1/-2 fire classification, EN 15650 fire dampers, EN 1366-2 damper testing).
Country rules for categories, compartments, sprinkler and detection duties, hydrants and smoke control are in the jurisdiction files. In Poland: WT Dział VI (fire safety), Rozporządzenie MSWiA z 7 czerwca 2010 r. and Rozporządzenie MSWiA z 24 lipca 2009 r. (fire water supply and access roads), with product approvals from CNBOP-PIB. Verify the paragraph numbers against the ISAP text before citing.
