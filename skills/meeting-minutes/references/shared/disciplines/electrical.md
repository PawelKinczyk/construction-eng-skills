# Discipline: Electrical

Status: v0.1, reviewed 2026-10. Target at v1.0: full.

Scope: low-voltage power distribution, switchboards, cables, earthing and protection, lighting, emergency lighting, standby supply, photovoltaic and electric vehicle charging.

Values in this file marked "rule of thumb" or "typical" are design practice, not law and not standard text. Installation rules live in HD 60364 (national adoptions: PN-HD 60364, BS HD 60364) and in the national law. Project requirements and utility conditions win over these values. Always state which value you used and why.

## Systems and equipment

| System | Main equipment |
|---|---|
| Supply and intake | utility connection (warunki przyłączenia), main switchboard, meter panel, transformer, generator, UPS, surge protective device (SPD) |
| Distribution | main switchboard, sub-distribution boards, busbar trunking, cable ladder and tray, distribution circuits |
| Switchgear and protection | circuit breakers (MCB, MCCB, ACB), fuses, residual current devices (RCD), surge protective devices, contactors, motor protective devices, soft starters, drives |
| Cables and wiring | copper and aluminium cables, fire-rated cable, halogen-free cable, reaction-to-fire class, cable trays and conduits |
| Earthing and bonding | earth electrode, main earthing terminal, protective conductors, equipotential and supplementary bonding, lightning protection and its earthing |
| Lighting | luminaires, LED modules and drivers, lighting control (presence, daylight, DALI), exterior and road lighting, emergency lighting (self-contained or central battery), exit signs |
| Standby and renewable | generator, UPS, battery system, photovoltaic array, inverter (grid-tied or hybrid), storage |
| Electric vehicle charging | AC charge point (mode 3), DC charger, load management, protection and PEN monitoring |
| Loads | motors, pumps, fans, chillers, lifts, IT equipment, kitchen and process equipment |

## Input checklists

Ask for all of these before sizing. Missing items become stated assumptions.

### Load schedule and demand
- Connected load per board and per circuit, with the load type (lighting, socket, motor, IT, HVAC).
- Diversity (simultaneity) factor per load group, and its source (national rule, client standard, project rule). State it.
- Power factor per load group, and whether compensation is fitted.
- Design load for the intake: maximum demand after diversity, with the growth allowance stated separately.
- Utility conditions: available power, connection point, transformer or cable rating, tariff and metering rules.
- Tariff structure, peak demand charge and any demand limit that the design must respect.
- Supply and earthing system (TN-S, TN-C-S, TT, IT) at the connection point, and the earth fault loop impedance.
- Fault level at the intake (kA) from the utility, for switchgear rating.

### Cable sizing
- Design current per circuit, and the protective device rating.
- Cable type, insulation, conductor material, number of loaded conductors, installation method (HD 60364-5-52 reference method).
- Ambient temperature and grouping (number of circuits in the tray, conduit or duct), and the correction factors.
- Route length, and the voltage drop limit for the circuit (lighting or other).
- Short-circuit withstand at the point, and the disconnection time the protective device must meet.
- Fire requirement on the route: fire-rated cable or not, and reaction-to-fire class.

### Switchboard
- Rated current of the busbar and of the incoming device, and the short-circuit withstand (Icw, Ipk).
- Degree of protection (IP) and impact strength (IK) for the location.
- Form of internal separation, and whether a busbar system or a panelboard is intended.
- Metering, monitoring, power factor correction and surge protection.
- Redundancy, changeover (source transfer), and the generator or UPS interaction.
- Dimensions, weight and space, access, cable entry, and heat dissipation.

### Earthing and protection
- Earthing system type, earth electrode resistance target, and the measured soil data.
- Touch voltage limit and the disconnection time the installation must meet.
- RCD requirement: rating, type (A, F, B), and the reason (socket outlets, EV charging, PV, frequencies from drives).
- Equipotential and supplementary bonding points, and metal services entering the building.
- Lightning risk assessment: need for a lightning protection system, and its class (EN 62305 series).
- Surge protection: SPD type and location per the risk and the installation.

### Lighting
- Required illuminance (lux) and the standard or client rule for each room type.
- Uniformity, glare (UGR) limit, colour rendering (Ra) and colour temperature.
- Room dimensions, reflectance, mounting height, and the maintenance factor the client accepts.
- Luminous efficacy target and the energy limit for lighting (national or client rule).
- Control requirement: presence, daylight, dimming, scene, DALI or BMS.
- Emergency lighting: escape route illuminance and duration, and the standard applied.
- Exterior lighting: light pollution class, curfew, and the boundary light limit.

### Standby supply, PV and EV charging
- Standby load list and the accepted autonomy time (generator start time or UPS ride-through).
- Generator: location, noise limit, fuel storage, exhaust route, and the load it must take (with the fire file for the plant room).
- UPS: output power, power factor, autonomy, battery type and room ventilation.
- PV: available roof or ground area, orientation and tilt, shading, and the inverter and array limits.
- PV and storage: connection point, export limit, and metering.
- EV charging: number and power of charge points, load management scheme, protection, cable route and ventilation of parking spaces.

## Design margins

Rules of thumb. Always state the margin and the reason. Never stack margins: apply each margin once, at one level.

| Item | Typical margin | Reason / note |
|---|---|---|
| Maximum demand | diversity applied once, at the intake or board level, not at each level | stacking diversity hides the real peak |
| Growth allowance | 10-25 % stated separately | state it and its basis (future extension), do not mix it into the diversity |
| Cable current rating | none on top of the correction factors | the correction factors are the margin; adding one more percentage is double counting |
| Voltage drop | no margin | check against the limit; if it fails, go up a size |
| Protective device rating | next standard size above the design current, then check the cable | the device is discrete, so state the chosen standard rating |
| Switchboard busbar | one standard step above the calculated demand | room for one or two future ways, stated |
| Generator | reject the starting current of the largest motor, then take the load list | size on the transient, not on the sum of kW |
| UPS | output power at the load power factor, plus a stated margin for the battery ageing | do not size on the nameplate kVA alone |
| PV array | none | the inverter limit and the MPPT window set the array size |
| Lighting design | maintenance factor chosen per the client rule | the maintenance factor is the allowance; do not add a second one |
| Earth electrode | target resistance from the protection requirement, not a fixed number | the value follows the disconnection and touch voltage checks |

## Typical calculations

Script: `scripts/electrical_calc.py` (in `equipment-selection`).

| Calculation | Command |
|---|---|
| Load current, single or three phase | `load-current --power-kw 30 --voltage 400 --cos-phi 0.9 --phases 3` |
| Apparent power and current from kVA | `load-current --power-kva 50 --voltage 400 --phases 3` |
| Cable voltage drop | `cable-drop --current-a 63 --length-m 80 --section-mm2 25 --voltage 400 --phases 3 [--cos-phi 0.9] [--rho 0.0225]` |
| Cable current rating after correction | `correction --iz 63 --factor 0.82 --factor 0.90` |
| Minimum cable size for a voltage drop limit | `cable-drop --current-a 63 --length-m 80 --voltage 400 --max-drop-percent 5 --size` |
| Fault current from the loop impedance | `fault-current --voltage 230 --impedance-mohm 320` |
| Maximum earth fault loop impedance | `zs-max --u0 230 --ia-a 80 [--cmin 0.95]` |
| Diversity applied to a load list | `diversity --load-kw 120 --factor 0.7` |
| Luminaire count for an illuminance | `lighting --lux 300 --area-m2 120 --flux-lm 4000 --uf 0.75 --mf 0.80` |
| Battery capacity for an autonomy time | `battery --load-w 800 --autonomy-h 0.5 --voltage 48 --dod 0.8 [--eff 0.9]` |

The script never picks the supply system, the protection type or the standard rating. Those come from HD 60364, the national law and the project.

Rules of thumb (check against the standard and the project):

| Item | Typical value |
|---|---|
| Voltage drop limit, lighting | 3 % of the nominal voltage |
| Voltage drop limit, other circuits | 5 % of the nominal voltage |
| Conductor resistivity for the drop, copper at operating temperature | 0.0225 ohm mm2/m (0.018 at 20 C); aluminium 0.036 |
| Cable reactance for the drop on small sizes | neglect for sections up to about 25 mm2 at 50 Hz |
| Socket outlet circuits in dwellings | 2.5 mm2, 16 A, RCD 30 mA |
| Voltage at the socket outlet | within ±10 % of the nominal |
| Diversity, dwellings | from the national rule; state it, do not invent it |
| Illuminance, offices (general work) | about 300-500 lx, UGR ≤ 19, Ra ≥ 80 |
| Illuminance, circulation areas | about 100 lx |
| Emergency escape route lighting | requirement and duration from EN 1838 and the national fire rules |
| Earth fault disconnection time, final circuits up to 32 A | 0.4 s in TN systems for 230 V (check the standard table) |
| Diesel generator autonomy | from the standby load list and the client requirement, not fixed here |
| UPS ride-through | long enough to cover the generator start and transfer time |
| PV connection | not more than the utility export limit; check the inverter setting |

The national voltage drop, diversity, RCD and emergency lighting rules are in the jurisdiction files. Use them, not the values above, when they differ.

## Common errors

- Diversity applied at several levels in series, so the intake is undersized.
- Growth allowance mixed into the diversity, so nobody can verify the peak demand.
- Voltage drop checked with the resistivity at 20 C, so the real drop is underestimated.
- Reactance neglected on large sections or long runs, so the drop is underestimated.
- Correction factors for grouping and ambient temperature forgotten, so the cable is overloaded.
- Protective device chosen after the cable, instead of checking the device against the cable rating (Ib ≤ In ≤ Iz).
- Disconnection time or earth fault loop impedance not checked, so the protection does not operate in time.
- RCD type (A, F, B) not matched to the load: drives and EV chargers need the right type, and DC leakage requires type B.
- PEN or PE continuity not checked where an RCD is fitted, or where a separate earth is required (EV charging).
- Fire-rated cable not used where the standard requires it (escape routes, smoke control, fire pumps, lifts).
- Reaction-to-fire class of the cable not checked for the location (EN 50575).
- SPD missing or the wrong type and location, so equipment is damaged by surges.
- Short-circuit withstand of the busbar or the cable not checked against the utility fault level.
- Heat dissipation of the switchboard ignored, so the components run above their rating in an enclosure.
- Lighting designed on the luminaire nominal flux with no maintenance factor or with the wrong one.
- Emergency lighting designed to the normal lighting level, or with the wrong duration.
- Generator sized on the sum of running kW, so it stalls on the largest motor start.
- UPS sized on kVA with no check of the load power factor or the battery ageing.
- PV array voltage above the inverter maximum at the lowest temperature, or MPPT window not checked.
- EV charger load management not coordinated with the intake, so the main fuse trips.
- Harmonics from drives, LED drivers and IT loads not considered for the neutral or the transformer.

## Compliance topics

Checklist seed for `code-compliance`. Each topic needs the jurisdiction's legal source and the project value.

| Topic | What to check |
|---|---|
| Connection conditions | utility technical conditions, metering, tariff and demand limit |
| Installation safety | protection against shock, overcurrent, overvoltage, thermal effects (HD 60364 series) |
| Earthing and bonding | earthing system, electrode resistance, equipotential bonding, touch voltage |
| RCD protection | required circuits, rating, type, and testing |
| Cables | current-carrying capacity, voltage drop, fire rating and reaction-to-fire class |
| Switchgear | rating, short-circuit withstand, IP and IK, internal separation |
| Lightning protection | risk assessment requirement, class, and the design of the system |
| Surge protection | need, type and location |
| Lighting and workplace rules | illuminance, glare, emergency lighting, workplace minimum requirements |
| Fire safety of electrical installations | fire-rated circuits, smoke control and fire pump supply, fire stopping of penetrations (with `fire.md`) |
| Standby and emergency supply | required standby loads, autonomy, and the safety services list |
| Generator and fuel storage | plant room requirements, fuel storage rules, noise and emissions |
| Photovoltaic | connection rules, export limit, protection, and roof or structure loads |
| Electric vehicle charging | protection, ventilation, load management, accessibility, fire requirements |
| Energy efficiency of products | ecodesign for motors, light sources, power supplies and standby losses |
| Energy performance of buildings | lighting power density, controls, and the metering requirement |
| Accessibility | socket and control heights, accessible controls, tactile markings |

## Standards by topic

See `eu.md` "Standards map by topic" for EN and HD numbers (HD 60364 series and its parts, EN 61439 series, EN 62305 series, EN 12464-1, EN 1838, EN 50172, EN 50575).
Country rules for voltage drop, diversity, RCD use and emergency lighting are in the jurisdiction files. In Poland: WT § 180-187 and PN-HD 60364; verify the paragraph numbers against the ISAP text before citing.
