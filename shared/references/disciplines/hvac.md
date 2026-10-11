# Discipline: HVAC

Status: v0.1, reviewed 2026-10. Target at v1.0: full.

Scope: heating, ventilation, air conditioning, cooling, heat recovery, controls.

Values in this file marked "rule of thumb" are typical design practice, not law and not standard text. Project requirements, client standards and manufacturer data win over them. Always state which value you used and why.

## Systems and equipment

| System | Main equipment |
|---|---|
| Heat source | gas boiler, heat pump (air-water, ground-water, water-water), district heating substation, electric boiler |
| Cooling source | air-cooled or water-cooled chiller, VRF/VRV outdoor unit, split unit, dry cooler, cooling tower |
| Hydronic distribution | circulating pump, heat exchanger, buffer tank, expansion vessel, hydraulic separator, balancing and control valves |
| Air handling | air handling unit (AHU), heat recovery (plate, rotary, run-around coil), fans, filters, coils, humidifier |
| Terminals | radiator, underfloor heating, fan coil unit (FCU), VAV/CAV box, chilled beam, VRF indoor unit, diffusers and grilles |
| Smoke and fire (with `fire.md`) | smoke extract fan, pressurisation fan, fire damper, smoke damper |
| Controls | BMS, room controllers, sensors, actuators |

## Input checklists

Ask for all of these before sizing. Missing items become stated assumptions.

### Circulating pump
- Duty: heating, cooling, domestic hot water circulation, other.
- Fluid: water or glycol mixture (type and %), design temperatures.
- Flow: from load and dT, or given. Load in kW and supply/return temperatures.
- Head: index circuit pressure drop (pipes, fittings, heat source, terminal, control valve, heat meter, strainer).
- Control: constant speed, Δp-constant, Δp-variable, external signal (0-10 V, Modbus/BACnet).
- Configuration: single, twin (duty/standby), duty/standby with separate pumps.
- Electrical supply: 1~230 V or 3~400 V.
- Connection: threaded or flanged, nominal size, installation length.
- Open system (NPSH check) or closed system.

### Fan or AHU
- Airflow supply and extract (m³/h), and the source of each (ventilation rate, load, pressurisation).
- External static pressure (ESP) for supply and extract: ducts, terminals, attenuators, louvres.
- Heat recovery type and required efficiency.
- Filter classes (ISO 16890) for supply and extract.
- Coils: heating and cooling capacity, media and temperatures, design outdoor conditions.
- Humidification or dehumidification needs.
- Location: indoor, outdoor (weatherproof), roof; access and service space; transport limits.
- Acoustic limits: at room, at plant room, at site boundary.
- SFP target or limit; energy class requirement; ecodesign compliance (Regulation 1253/2014).
- Hygiene requirement (for example VDI 6022 when the client asks).
- Control: integrated controls or BMS; protocol.

### Heat source (boiler, heat pump, substation)
- Design heat load (EN 12831-1) and domestic hot water load (simultaneity basis).
- Design outdoor temperature for the location.
- Flow and return temperatures; low-temperature emitters or not.
- Fuel or energy supply available and connection capacity.
- Heat pump: source type, bivalent point, backup heater, defrost, refrigerant and GWP, noise at boundary.
- Substation: district heating supplier's technical conditions (primary temperatures, pressure, connection rules).
- Redundancy (N, N+1) and part-load operation.

### Cooling source (chiller, VRF, split)
- Design cooling load, peak and part-load profile.
- Chilled water or refrigerant temperatures; glycol for outdoor or free cooling.
- Design outdoor temperature (dry bulb, wet bulb for water-cooled).
- Refrigerant type and GWP; F-gas restrictions; leak detection need (EN 378).
- VRF: refrigerant pipe lengths and height differences, indoor unit combination ratio, refrigerant charge per room volume (EN 378).
- Noise at boundary; location and weight.
- Redundancy and seasonal efficiency (SEER, SEPR).

### Fan coil unit or terminal
- Sensible and total cooling load, heating load per room.
- Water temperatures (2-pipe or 4-pipe) or refrigerant.
- Fresh air connection or not; airflow and throw.
- Noise limit in the room (NR or dB(A)).
- Mounting: ceiling cassette, ducted, wall, floor; available void depth.

### Expansion vessel
- System water volume, max and min temperature, static height, safety valve setting, fluid.

## Design margins

Rules of thumb. Always state the margin and the reason. Never stack margins: apply each margin once, at one level.

| Item | Typical margin | Reason / note |
|---|---|---|
| Heat load | none on top of EN 12831-1 result | the standard method already includes reheat allowance if chosen |
| Pump head | 5-10 % on calculated pressure drop | fitting losses, future balancing; variable-speed pumps tolerate less margin |
| Pump flow | none | flow follows load and dT |
| Fan pressure (ESP) | 10-15 % | duct leakage, dirty filters are covered by using final filter pressure drop, not by margin |
| Fan airflow | add duct leakage per EN 16798-3 / EN 12237 airtightness class | do not add a generic percentage on top |
| Filter pressure drop | design at mean or final drop per project rule | state which one |
| Chiller capacity | none if load includes diversity correctly | oversizing hurts part-load efficiency |
| Heat pump | size to bivalent point strategy, not to 100 % + margin | |

## Typical calculations

Script: `scripts/hvac_calc.py` (in `equipment-selection`).

| Calculation | Command |
|---|---|
| Water flow from load | `water-flow --load-kw --dt [--temp]` |
| Airflow from sensible load | `air-flow --load-kw --dt` |
| Pipe pressure drop | `pipe-dp --flow-m3h --id-mm --length-m [--zeta] [--temp]` |
| Duct pressure drop | `duct-dp --flow-m3h (--d-mm | --a-mm --b-mm) --length-m [--zeta]` |
| Pump head and power | `pump-power --flow-m3h (--head-m | --dp-kpa) [--eff]` |
| Fan power and SFP | `fan-power --flow-m3h --dp-pa [--eff]` |
| Margin | `margin --value --percent` |

Glycol mixtures: pass `--rho`, `--cp`, `--mu-mpas` from the glycol manufacturer data at design temperature. Glycol lowers capacity of coils and raises pump head; ask the manufacturer for the corrected selection.

Sizing rules of thumb (check against project requirements):

| Item | Typical value |
|---|---|
| Water velocity, small pipes (≤ DN50) | 0.5-1.0 m/s |
| Water velocity, larger pipes | 1.0-2.0 m/s |
| Pipe pressure gradient | 100-250 Pa/m |
| Duct velocity, main ducts (offices) | 4-6 m/s |
| Duct velocity, branches | 2.5-4 m/s |
| Duct pressure gradient | 0.8-1.5 Pa/m |
| Supply air dT for cooling (mixing ventilation) | 6-10 K |
| Heating flow/return, heat pumps | 35/30 to 45/40 °C |
| Chilled water | 6/12, 7/12 or higher (for example 14/18 for beams) |

## Common errors

- Oversizing by stacking margins (load + safety + selection + "round up").
- Pump selected at the wrong point on the curve; no check of the variable-speed operating range.
- Glycol correction forgotten for coils and pumps.
- AHU selected with clean-filter pressure drop.
- ESP of the AHU confused with total fan pressure.
- SFP compared against the wrong definition (SFP vs SFPint vs SFPv).
- Heat pump sized without the defrost and low-temperature capacity drop.
- Refrigerant charge vs room volume (EN 378) not checked for VRF and splits.
- F-gas restrictions not checked for the refrigerant and installation date.
- Noise at site boundary not checked for outdoor units and roof fans.
- Weight and access: equipment does not pass through doors, shafts or lifts; roof load not confirmed with structural.
- Selection based on catalogue nominal values instead of actual design conditions.

## Compliance topics

Checklist seed for `code-compliance`. Each topic needs the jurisdiction's legal source and the project value.

| Topic | What to check |
|---|---|
| Ventilation rates | outdoor airflow per person, per area or per room type; kitchens, toilets, garages |
| Heat recovery | required efficiency and when it is mandatory |
| Energy performance | primary energy limits, SFP limits, seasonal efficiency of generators |
| Insulation of pipes and ducts | minimum thickness or thermal resistance by diameter and location |
| Ecodesign and energy labelling | fans, AHUs, pumps, circulators, heat generators, chillers |
| Refrigerants | F-gas restrictions, leak checks, leak detection, charge per room volume |
| Fire safety in HVAC | fire dampers at fire separations, duct fire resistance, smoke control, plant room separation |
| Combustion and flues | boiler room requirements, air supply, flue design, gas safety |
| Acoustics | noise from equipment in rooms and at site boundary |
| Hygiene | air intake and exhaust location, distance to pollution sources, cleaning access |
| Access and maintenance | service space, access to dampers and filters, safe access on roofs |
| Metering and controls | heat and cooling meters, room controls, BACS class requirements |

## Standards by topic

See `eu.md` "Standards map by topic" for EN standard numbers (EN 12831-1, EN 16798-1/-3, EN 13053, EN 1886, ISO 16890, EN 14511, EN 14825, EN 378, EN 12237, EN 1507, EN ISO 5801).
Country rules (ventilation rates, insulation of pipes and ducts, heat recovery, energy limits) are in the jurisdiction files.
