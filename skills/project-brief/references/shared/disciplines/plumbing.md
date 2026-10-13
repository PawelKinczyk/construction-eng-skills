# Discipline: Plumbing

Status: v0.1, reviewed 2026-10. Target at v1.0: full.

Scope: domestic cold water, domestic hot water (DHW), DHW circulation, water treatment, sanitary drainage, rainwater, sewage.

Values in this file marked "rule of thumb" or "typical" are design practice, not law and not standard text. Project requirements, client standards and manufacturer data win over them. Always state which value you used and why.

## Systems and equipment

| System | Main equipment |
|---|---|
| Cold water supply | service pipe, water meter, main shut-off, pressure reducing valve (PRV), backflow preventer, storage tank or break tank, booster set, filters, risers, manifolds, pipework (steel, copper, PEX, PP-R, multilayer) |
| Domestic hot water | water heater (gas, electric, heat pump), boiler with cylinder (vented or unvented), plate heat exchanger, solar thermal or DHW heat pump, thermostatic mixing valve (TMV), safety group (valve, expansion vessel) |
| DHW circulation | circulation pump, balancing valves, circulation pipework, temperature sensors, Legionella control (thermal disinfection, recirculation) |
| Water treatment | softener, dosing unit, filtration, disinfection (UV, chemical), Legionella risk control |
| Sanitary drainage | soil stack, waste stack, ventilated stack, air admittance valve, branch pipes, traps, floor drains, backwater valve, lifting station (pump), pipes (cast iron, PP, PE-HD, PVC-U) |
| Rainwater | roof outlets or gutters, downpipes, gravity or siphonic system, retention and attenuation, infiltration, rainwater harvesting |
| Foul and special waste | grease separator (kitchen), starch separator, condensate drains and neutralisation, industrial waste pre-treatment |

## Input checklists

Ask for all of these before sizing. Missing items become stated assumptions.

### Cold water supply and pipe sizing
- Number and type of draw-off points (fixtures), with their draw-off flows.
- Building use and simultaneity basis: the sizing method from EN 806-3, or the national practice (for example DIN 1988-300 load units), or the project rule. State which method was used.
- Supply pressure at the connection: minimum and maximum dynamic pressure, static pressure. Water meter size and its pressure loss.
- Utility connection conditions (warunki przyłączenia): available flow and pressure, meter location, pipe size.
- Pipe material and its corrosion risk against the local water quality (chlorides, hardness, pH; EN 12502 series).
- Velocity limit and pressure band per EN 806-2, and the project acoustic limit.
- Backflow protection: fluid category at each point, protection type per EN 1717.
- Drinking water quality rules for the jurisdiction, and the material approval list (for example metal in contact with drinking water).

### Domestic hot water
- Peak draw: flow and duration, or a tapping profile (usually per dwelling or per person).
- Storage temperature, distribution temperature, cold water temperature at the site.
- Heat source and its continuous DHW output (boiler module, heat pump priority, district heating capacity).
- Cylinder type and pressure class: unvented (with safety group and expansion vessel) or vented.
- Recovery time and the accepted reheat period.
- Legionella control method, disinfection temperature and the national rules.
- Space, weight and access for the cylinder and the heater.

### DHW circulation
- Loop heat loss from the pipework (insulation, length, running hours).
- Accepted temperature drop in the loop, and the temperature required at the last draw-off point.
- Pump control: time program, thermostatic, or demand-based.
- Balancing valves at each riser.

### Drainage
- Sum of discharge units (DU) per stack and branch, from the EN 12056-2 table.
- Frequency factor K for the building use, from EN 12056-2.
- Stack height, number of floors, branch lengths, branch gradients, ventilation method (primary ventilated, secondary ventilated, air admittance valve).
- Fixture trap seal depth and the maximum tolerated pressure fluctuation (usually ±400 Pa).
- Connection to the external network: invert level, gradient, backwater risk, need for a lifting station.
- Pipe material and its fire class at floor and shaft penetrations.
- Special waste: kitchen grease, condensate, laboratory or industrial effluent.

### Rainwater
- Design rainfall intensity for the location and the return period required by the jurisdiction.
- Roof plan area (projected), plus other drained surfaces.
- Runoff coefficient per surface type.
- Primary and secondary (overflow) system, and whether a siphonic system is intended.
- Roof outlet or gutter capacity, number and routing of downpipes.
- Retention, attenuation, infiltration or reuse required by local law.
- Discharge destination (network, infiltration, watercourse) and its permit conditions.

## Design margins

Rules of thumb. Always state the margin and the reason. Never stack margins: apply each margin once, at one level.

| Item | Typical margin | Reason / note |
|---|---|---|
| Cold water design flow | none on top of the sizing method | the method already contains simultaneity. State the method and the simultaneity basis |
| Pressure available at the worst point | none on top of the index circuit total | add each loss once (meter, PRV, pipes, fittings, valve, fixture); never add a generic percentage |
| Pipe velocity | no margin | check against the maximum (see below); a margin on velocity means a larger pipe, decide it deliberately |
| DHW peak power | 10 % only if the draw profile is uncertain | state it; otherwise none, the profile is the design basis |
| DHW cylinder volume | none | size to the peak draw minus the volume reheated during the draw; state the reheat period |
| DHW circulation flow | none | follows the loop heat loss and the accepted temperature drop |
| Drainage flow | none | ΣDU and K include the diversity; do not add a percentage |
| Rainwater flow | none | the safety comes from the return period of the secondary system, not from a percentage |
| Storage tank volume | see the national rule or the utility requirement | state the rule used; do not invent a number of days |

## Typical calculations

Script: `scripts/plumbing_calc.py` (in `equipment-selection`). Pipe pressure drop, pump power and water flow from load use `scripts/hvac_calc.py` (same commands).

| Calculation | Command |
|---|---|
| Cold water design flow from fixtures | `peak-flow --fixture basin:12 [--fixture wc:10] [--factor K]` |
| Wall thickness check of the sizing method | `pipe-dp --flow-m3h --id-mm --length-m [--zeta] [--roughness-mm]` |
| Mixing of hot and cold water | `dhw-mix --v-mix 200 --t-mix 45 --t-hot 60 --t-cold 10` |
| DHW peak power from a draw | `dhw-demand --volume-l 200 --t-hot 60 --t-cold 10 --draw-time-min 10` |
| DHW cylinder volume after reheat | `dhw-store --v-peak 300 --t-store 60 --t-cold 10 --t-mix 45 --continuous-kw 24 --draw-time-min 10` |
| DHW circulation flow | `dhw-circ --heat-loss-w 500 --dt 5` |
| Drainage stack design flow | `stack --du 45 --k 0.7 [--capacity 6.2]` |
| Rainwater design flow | `rainwater --area-m2 1200 --intensity 300 --runoff 0.95` |
| Circulation pump head and power | `pump-power --flow-m3h (--head-m | --dp-kpa) [--eff]` |
| Margin | `margin --value --percent` |

Pipe roughness for `pipe-dp`, in mm: steel 0.045, galvanised steel 0.15, copper 0.0015, stainless steel 0.015, PEX, PP-R and multilayer 0.007. Confirm with the pipe manufacturer.

Sizing rules of thumb (check against project requirements and the national rule):

| Item | Typical value |
|---|---|
| Cold water velocity, pipes in shafts and risers | 1.0-2.0 m/s |
| Cold water velocity, pipes in rooms and near bedrooms | 0.5-1.0 m/s |
| Cold water pressure at the draw-off point | 100-300 kPa; below 50 kPa at the top fixture means a booster set |
| Static pressure at the lowest fixture | limit per EN 806-2 and the fixture data (often 500 kPa); otherwise fit a PRV per floor or per zone |
| Drainage branch gradient | per EN 12056-2 table; common practice DN100 about 1:100 to 1:50, DN50 about 1:50 to 1:30 |
| Drainage stack filling ratio | 0.25-0.33 of the pipe area |
| DHW store temperature | at least 60 °C |
| DHW distribution temperature at the tap | 55 °C, and not above 60 °C at the fixture for safety |
| Cold water temperature (Legionella) | below 20 °C, never above 25 °C |
| DHW draw, dwellings | 40-60 l per person per day at 45 °C |
| DHW draw, offices | 5-15 l per person per day at 45 °C |
| DHW circulation temperature drop | 5 K typical, per the project rule |
| Rainwater runoff coefficient C | metal or bitumen roof 0.9-1.0, gravel roof 0.6-0.9, asphalt 0.8-0.9, paving 0.5-0.9, grass 0.1-0.3 |

The national Legionella, temperature and water quality rules are in the jurisdiction files. Use them, not the values above, when they differ.

## Common errors

- Design flow taken as the sum of all fixtures with no simultaneity basis, or a simultaneity factor applied without stating the method.
- Water meter and PRV pressure losses left out of the index circuit.
- Velocity not checked: noise in risers and bedrooms, and erosion in copper at high velocity.
- Backflow protection class not matched to the fluid category (EN 1717); no protection where a hose or a boiler is connected.
- Cylinder sized on volume alone, without the continuous output of the heat source during the draw.
- No circulation, or dead legs and long uninsulated branches: Legionella risk and long waiting time for hot water.
- DHW above 60 °C at the fixture: scalding risk, no TMV fitted.
- Storage temperature set below 60 °C without an approved alternative control scheme.
- Trap seal lost by siphonage: wrong stack ventilation, branch too long or gradient wrong, or an air admittance valve in the wrong place.
- Branch gradient too steep: water leaves the solids behind.
- Sizing method and standard for drainage not stated, so the DU sum and K cannot be checked.
- Overflow (secondary) rainwater system missing, so a blocked outlet floods the roof.
- Return period not stated for the rainwater design, or the same return period used for the primary and the secondary system.
- Pipe material wrong for the fire class at a shaft or floor penetration (with `fire.md`).
- Backwater valve missing where the network can surcharge, or fitted without a lifting station capability.
- Booster set noise and vibration not checked against the acoustic requirements.
- Condensate from boilers, chillers and AHUs discharged without neutralisation or to the wrong system.
- Rainwater harvesting connected to the drinking water system without the correct backflow protection.
- Water quality, hardness or chloride content never checked, so the pipe material and the softener are chosen blind.

## Compliance topics

Checklist seed for `code-compliance`. Each topic needs the jurisdiction's legal source and the project value.

| Topic | What to check |
|---|---|
| Water supply to the building | duty to connect, service pipe rules, utility connection conditions |
| Drinking water quality | sampling, treatment, materials in contact with drinking water |
| Legionella and temperatures | store and distribution temperatures, risk assessment, records |
| Backflow protection | fluid categories, approved protection types, testing |
| Pressure safety | safety valve settings, expansion vessel, PRV, pressure class of fittings |
| Drainage and ventilation | stack ventilation, traps, gradients, materials, testing |
| Fire in shafts and penetrations | pipe fire class, sealing of penetrations, shaft construction (with `fire.md`) |
| Firefighting water | hydrants, sprinkler supply and water reserve (with `fire.md`) |
| Rainwater and surface water discharge | permit to discharge, infiltration, retention, flood protection |
| Backwater and flood protection | backwater valves where the network can surcharge, basement drainage |
| Grease and special waste | separators, discharge limits, agreements with the utility |
| Water metering and cost allocation | main meter, sub-meters, allocation rules in multi-tenant buildings |
| Energy for DHW | ecodesign for water heaters and storage tanks, energy label, DHW share of the energy certificate |
| Water efficiency | flow limiters, dual-flush, rainwater reuse requirements |
| Accessibility and safety | sanitary room dimensions, accessible fittings (with accessibility rules) |

## Standards by topic

See `eu.md` "Standards map by topic" for EN standard numbers (EN 806 series, EN 1717, EN 12056 series, EN 752, EN 12502 series, EN 12897).
Country rules for water supply, drainage and DHW temperatures are in the jurisdiction files. In Poland: WT § 113-132 for water supply and drainage, and the water quality regulation of the Ministry of Health. Verify the paragraph numbers against the ISAP text before citing.

## Drain and stack capacity tables

Stack and drain capacity tables belong to the licensed standards (EN 12056 series or the national equivalent) and are not in this repo. The agent asks the user for the capacity value, or marks the capacity check "to verify"; it does not use a remembered or assumed value.
