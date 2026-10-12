---
name: ifc-analysis
description: Read an IFC model without BIM software - element counts by type and by storey, quantities from IfcQto and property sets (areas, volumes, lengths, counts), property set values, model units and schema, missing or empty parameters, IFC type objects, a schedule exported from the model, comparison of two IFC issues by GUID, and IDS validation. Use when the user asks to analyse an IFC file, count elements, take quantities from a model, check property sets or parameters, validate a model against an IDS or a client requirement, export a schedule from IFC, or compare two IFC issues.
---

# IFC analysis

Goal: model data taken from the file itself - counts, quantities, properties - with the schema, the units, the storey and the element type stated for every number. The output is a schedule or a report another engineer can check.

Python with `ifcopenshell` is required for everything here. There is no way to read IFC without a library, so without it the skill asks for the install instead of working around it.

## 1. Load context

- Read `PROJECT.md`: jurisdiction, disciplines, deliverable language, section "Project standards" (the IFC requirements: schema version, IDS or client requirements, naming and property requirements).
- No `PROJECT.md`: offer `project-brief`. If declined, ask for the deliverable language and the IFC requirement document in use.
- Load `references/shared/disciplines/<discipline>.md` for what the elements and properties mean in that discipline.
- Load `references/ifc-reading.md` (this skill) for the schema differences, where quantities live, property sets, units, GUIDs and the model quality checks.
- Model and property requirements come from the BEP or the client's information requirements. This skill reports what is in the model against them; it does not decide the requirement.

## 2. Collect inputs

1. **The file.** Path, file date and issue, schema version, and whether it is the coordination model or a discipline export.
2. **What is wanted**: counts, quantities, one property set, a schedule, missing parameter checks, a comparison of two issues, or IDS validation. Ask - a full dump of a large model is unreadable and hides the answer.
3. **The requirement** for any check: the IDS file, the client's property list, or the element table from the BEP. Without it, the check becomes a report of what exists, and that must be said.
4. **Scope filters**: disciplines, storeys, element types, and whether type objects or occurrences are wanted.
5. **Cross-check**: the schedule or the drawing the values will be compared with.

## 3. Work

1. **Start with the summary.** Schema, units, project structure, storeys, element counts by type. Everything else is read in the context of these.
   ```
   python scripts/ifc_report.py summary --file model.ifc
   python scripts/ifc_report.py quantities --file model.ifc --type IfcFlowTerminal [--storey "Level 1"]
   python scripts/ifc_report.py psets --file model.ifc --type IfcPump --pset Pset_FlowMoverCommon
   python scripts/ifc_report.py missing --file model.ifc --require requirements.json --csv missing.csv
   python scripts/ifc_report.py schedule --file model.ifc --type IfcAirTerminal --props Name,Tag,FireRating --csv terminals.csv
   python scripts/ifc_report.py compare --old revB.ifc --new revC.ifc
   python scripts/ifc_report.py ids --file model.ifc --spec spec.ids     # needs ifctester
   ```
2. **Counts.** By element type and by storey, with the schema stated. State whether IfcTypeObject (types) and occurrences are counted separately, and do not add them together.
3. **Quantities.** Take them from IfcElementQuantity (Qto sets) where present, and say which quantity set and which quantity name was used. Where a quantity is missing, take it from the property set only if the user accepts that fallback, and say so. Never compute a quantity from geometry silently; if geometry is the only source, say that a geometry-based calculation is an approximation and needs the modelling assumptions.
4. **Properties.** Report values per element or as a table for a type. Empty strings, missing properties and duplicated properties are findings, not noise: they break schedules, IDS checks and quantity takeoff.
5. **Missing parameters.** Check against the supplied requirement list and report per element: element, type, storey, the missing property, and the rule it comes from. Group the result by rule as well as by element, because that is what the modeller has to fix.
6. **Schedules.** Export the table the user needs, with the property names as columns and one row per element: element GUID, type, storey, name, tag, and the requested properties. State the source: model file, date, schema.
7. **Comparison of two issues.** Compare by GUID: added, removed, changed properties. Report what the GUID comparison shows and state that a renamed or re-created element appears as a removal plus an addition even when the design did not change.
8. **IDS validation.** Run the IDS file if `ifctester` is available and report the result per specification: passed, failed, with the failing elements. Without it, say the check could not run, and offer the manual check against the requirement list instead.

## 4. Verify

- Units: read the IfcUnitAssignment and state the length, area and volume units. A model in millimetres gives quantities 1000 or 10^6 times off, and this is the most common silent error.
- Schema: state IFC2X3, IFC4 or IFC4X3. Property and quantity set names and availability differ between them.
- Counts: state the filter (type, storey, including or excluding types and spaces) and whether the count comes from occurrences or types.
- Quantities: state the quantity set and name for each column. A quantity without its set name cannot be checked.
- Missing values: report them; never fill, interpolate or copy a value from another element.
- GUID comparison: state that GUIDs are stable only when the authoring tool preserves them; a re-export can change many GUIDs without any design change.
- Model quality findings trimmed to what matters: missing or empty properties, missing quantities, duplicate elements, elements outside any storey, unknown or proxy types.
- Any number used for money or for a selection goes to `cost-estimate` or `equipment-selection` with its source, and is not used directly here.

## 5. Output

Write in `deliverable_language` from `PROJECT.md`. Default Markdown; on request `.csv` or `.xlsx`.

1. **Summary**: file, date, schema, units, storeys, element counts by type, the three findings that matter.
2. **Counts**: table by element type and by storey.
3. **Quantities**: table with element type, storey, quantity set, quantity name, value, unit, source.
4. **Properties / schedule**: table with one row per element and the requested properties as columns.
5. **Requirement check**: per rule, passed, failed, not checked, with the failing elements and the reason.
6. **Comparison**: added, removed, changed, and the GUID caveat.
7. **Findings**: unit, schema, empty property, duplicate, unassigned storey.
8. **To verify**: values to confirm with the modeller, requirements that could not be checked, and the tool versions used.

## Rules

- Read only. Never edit, re-export or repair the user's IFC. Write output to new files only.
- Do not invent element counts, quantities or property values. Absent means absent, and it is reported.
- A model is not the design: state that the report describes the model as received, at the date and version given.
- Do not silently convert units. Report the model units and, when a value is converted for readability, show both.
- IDS results are evidence about the model, not a statement that the design is compliant.
- State the ifcopenshell (and ifctester) version in every report.
