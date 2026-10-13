# Reading an IFC model

## 1. Schema versions

| Schema | Where it is still used | What to watch |
|---|---|---|
| IFC2X3 | common in production, MEP exports, older tools | fewer property sets, quantities often absent; no IfcAlignment, no IfcDoorType as in IFC4 |
| IFC4 | current default for new projects | richer property sets, better MEP coverage; property names differ from IFC2X3 |
| IFC4X3 | infrastructure, alignment, rail | some tools export it by accident for buildings, which breaks downstream checks |

Always report the schema first. A property set that exists in IFC4 may be absent in an IFC2X3 export of the same model, and a check that ignores this produces false failures.

## 2. Spatial structure

```
IfcProject
  IfcSite
    IfcBuilding
      IfcBuildingStorey      (one per level; some exports have only one)
        IfcSpace             (rooms; often missing in MEP exports)
          elements
```

Rules
- Counts by storey need the storey assignment (`IfcRelContainedInSpatialStructure`). Elements not assigned to a storey exist; report them, do not drop them.
- Spaces are frequently absent, empty or unassigned. A quantity per room may not be computable from the model alone.
- Site, building and storey names are free text: "Level 1", "01", "Parter". Do not assume a naming convention; report the names as they are.
- Zones (`IfcZone`) and systems (`IfcSystem`, `IfcDistributionSystem`) group elements for fire, HVAC or electrical purposes and are separate from the storey structure.

## 3. Counts: occurrences and types

| Concept | Entity | Meaning |
|---|---|---|
| Type object | `IfcWallType`, `IfcPumpType`, `IfcAirTerminalType` | the specification of a product type, one per type |
| Occurrence | `IfcWall`, `IfcPump`, `IfcAirTerminal` | one instance placed in the model; this is what you count for a schedule |
| Type assignment | `IfcRelDefinesByType` | links occurrences to their type |

Rules
- Count occurrences for a schedule, count type objects only when the user asks for the type catalogue, and never add the two.
- `IfcBuildingElementProxy` is a catch-all: report it, because quantities and properties attached to it are usually poor.
- MEP element names vary by exporter (`IfcFlowTerminal` with a predefined type such as `AIRTERMINAL`, or `IfcAirTerminal` in IFC4). Query by both the entity and the predefined type before reporting "missing elements".

## 4. Where quantities live

| Source | What it holds | Reliability |
|---|---|---|
| `IfcElementQuantity` (Qto_ sets) | declared quantities: `Qto_WallBaseQuantities` (Length, Height, Width, GrossArea, NetVolume), `Qto_SpaceBaseQuantities`, MEP Qto sets | the reliable source when present; the exporter computes it from geometry at export time |
| Property sets (`Pset_*`) | product data: flow rates, power, material, fire rating | never a geometric quantity, even when the name looks like one |
| Geometry | computable from the representation | requires a geometry engine and modelling assumptions; report it as an approximation with the assumptions |

Rules
- State the quantity set and the quantity name for every number (`Qto_WallBaseQuantities.NetVolume`, not "volume").
- "Gross" and "Net" quantities differ by openings and by material layers. Never mix them in one column.
- Where a Qto set is missing, say which elements lack it and offer the property set or the geometry as a stated fallback, with the difference it makes.

## 5. Property sets

- Standard sets start with `Pset_` and carry common data (`Pset_FlowMoverCommon`, `Pset_DistributionFlowElementCommon`).
- Custom sets (project or vendor) carry whatever the project adds, often with no consistency between disciplines; report their names, do not assume meaning.
- PSets are attached through `IfcRelDefinesByProperties`, either to the occurrence or to the type. A value may sit on the type and be inherited by every occurrence; check both before reporting "missing".
- `scripts/ifc_report.py` reads both. Type-level sets are `HasPropertySets` of the type object (`IfcPumpType`, `IfcAirTerminalType`, ...), reached from the occurrence by `IsTypedBy` (IFC4) or by an `IfcRelDefinesByType` inside `IsDefinedBy` (IFC2X3 - in IFC4 `IsDefinedBy` holds only `IfcRelDefinesByProperties`). Type-level quantity sets (`IfcElementQuantity`) are read the same way.
- Inheritance: an occurrence value overrides the type value for the same set and property. Each row carries `source` = `occurrence` | `type`. Revit and ArchiCAD exports often put `FireRating`, `Pset_PumpTypeCommon` or `RatedPower` on the type only; a type-blind read reports them missing. `--no-type` restores the occurrence-only read, for comparison with a tool that does not follow types.
- In a report, say when a value comes from the type; the modeller fixes it in a different place.
- Multi-value properties and value types (label, length, boolean) exist: a boolean that reads "True" as a string is a reported finding, not a pass.
- `IfcPropertySet` with no properties, empty strings, and duplicated property names are common model defects. Report them; they break downstream schedules.

## 6. Units

Read the `IfcUnitAssignment` and report the length, area, volume, mass and time units, plus the angle unit and the scale prefix. A model in millimetres with a Qto in millimetres gives volumes 10^9 times the cubic metre value; a reader who assumes metres is off by a factor nobody notices until the concrete order.

Rules
- Report the unit for every quantity column, as it is in the file.
- Where you convert for readability, show both values and the factor used.
- Watch for a mixed file (SI units in some properties, imperial in others), which happens when models are merged.

## 7. Requirement checks and IDS

- An IDS file (buildingSMART Information Delivery Specification) states requirements as applicability plus requirements per entity type: properties that must exist, with value constraints and cardinality.
- `ifctester` (part of the IfcOpenShell ecosystem) runs an IDS against an IFC and returns per-specification results with the failing elements and reasons. Report them grouped by specification, and count the failing elements.
- Without an IDS, check a property list supplied as JSON: per element type, the property sets and properties that must exist and must not be empty. State that this is a project-specific check, not an IDS result.
- A passed IDS means the model meets the specification as written. It says nothing about whether the specification matches the building, and nothing about design compliance.

## 8. Comparing two IFC issues

- Compare by `GlobalId` (GUID). IfcOpenShell can read the old and new files and report added, removed and changed elements.
- GUIDs are stable only when the authoring tool preserves them through the edit. A re-export from a changed model, a rebuilt phase, or a different authoring software can change many GUIDs with no design change at all. Report the count of "removed plus added" pairs before calling them design changes.
- `scripts/ifc_report.py compare` prints a warning when more than 50 % of the old elements have no GUID in the new file (GUIDs are not stable between independent exports), prints the removed and added counts, and offers a fallback: removed and added elements matched by class + name + storey. The fallback is a heuristic: elements renamed, moved to another storey or sharing a name (`P-01` twice) are mis-paired, so present it as "likely re-export", never as proof.
- The "changed" list covers Name, Tag, ObjectType, PredefinedType and class only; property set values are not compared, so say "changed attributes", not "changed properties".
- Compare properties element by element for the ones that matter (type, name, type object, pset values), not the whole file: whole-file comparison of a large model produces noise.
- The comparison is evidence about the model. Whether a change is a design change is a project decision.

## 9. Model quality findings worth reporting

| Finding | Why it matters |
|---|---|
| Missing or empty `Name` / `Tag` | schedules cannot be built, and tags drive equipment lists |
| Missing Qto set on a type that needs quantities | takeoff falls back to geometry, with a larger error |
| Elements not assigned to a storey | counts by level are wrong, and coordination misses them |
| `IfcBuildingElementProxy` volume | unknown content and poor data |
| Duplicate elements at the same position | counts too high; check by GUID and geometry |
| Unit assignment missing or inconsistent | every quantity in the report is suspect |
| Very large file with few elements | unmanaged geometry, orphaned representations |
| Spaces missing in a building model | room-based quantities and checks are impossible |

## 10. Reporting rules

- Every number carries: file name, file date, schema, unit, element type, storey, and the quantity or property set it came from.
- The model is a snapshot. Say so, and never present it as the current design without the modeller's confirmation.
- Quantities for money or selection go to `cost-estimate` or `equipment-selection`, with their source, and are checked against a schedule before use.
- Read only: never edit, repair or re-export the model.
