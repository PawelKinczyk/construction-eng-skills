---
name: equipment-selection
description: Size and select building services equipment - pumps, fans, air handling units (AHU), heat pumps, boilers, chillers, VRF, fan coils, heat exchangers, expansion vessels, DHW cylinders and water heaters, cold water supply, drainage stacks and rainwater systems, cables and voltage drop, switchboards, protective devices, standby batteries, sprinkler and fire water systems, smoke exhaust, and other MEP equipment. Collects design inputs, calculates duty points with scripts, applies stated margins, checks manufacturer data, gives alternatives and a verification list. Use when the user asks to select, size, dimension, compare or check equipment, asks "what pump/fan/AHU do I need", or gives a duty point and wants a product.
---

# Equipment selection

Goal: a selection sheet that another engineer can check in five minutes. It shows the duty point, how it was calculated, the selected unit, alternatives, assumptions, sources and what still needs verification.

The method is the same for every discipline. Discipline knowledge (input checklists, margins, typical errors) is in `references/shared/disciplines/<discipline>.md`.

## 1. Load context

- Read `PROJECT.md`: jurisdiction, disciplines, role, units, deliverable language, watch-outs (client brand preferences, energy targets, acoustic limits).
- No `PROJECT.md`: offer `project-brief`. If declined, ask for jurisdiction, discipline and deliverable language only.
- Load `references/shared/disciplines/<discipline>.md`. If its status is "skeleton", say so, use the general method below and mark every limit or margin "to verify".
- Load `references/shared/jurisdictions/<jurisdiction>.md` (and `eu.md` for EU member states) for product rules (ecodesign, F-gas, CE) and design limits.

## 2. Collect inputs

1. Find the input checklist for this equipment type in the discipline file.
2. Fill what the user already gave, then what project documents show (schedules, calculations, drawings).
3. Ask for the rest in one message. For each missing item, offer a default and its source. Example: "Fluid: water 70/50 °C (typical for radiators) - confirm?".
4. Record every assumed value in the "Assumptions" list. Never assume silently.

Do not start calculating when a value that drives the size is unknown (load, flow, pressure, temperatures). Ask first.

## 3. Work

1. **Duty point.** Calculate with the scripts. Show formula, inputs, result and units.
   - HVAC: `python scripts/hvac_calc.py <command> ...` (commands listed in `hvac.md`, "Typical calculations").
   - Plumbing: `python scripts/plumbing_calc.py <command> ...` (commands listed in `plumbing.md`). Pipe pressure drop, pump power and water flow from load use `hvac_calc.py`.
   - Electrical: `python scripts/electrical_calc.py <command> ...` (commands listed in `electrical.md`).
   - Fire: `python scripts/fire_calc.py <command> ...` (commands listed in `fire.md`). Fire pump head and pipe pressure drop use `hvac_calc.py`.
   - Pressure drop of the index circuit: sum the segments, components and control valve. Show a table.
2. **Margins.** Apply the margins from the discipline file once, at one level. State value and reason. Never stack margins.
3. **Requirements.** List what the unit must meet besides the duty point: efficiency class, ecodesign limits, refrigerant and F-gas rules, noise, dimensions, weight, electrical supply, controls protocol, client brand list.
4. **Selection.**
   - Product data from the user (data sheet, selection software printout) has priority.
   - Without it: search manufacturer websites for current data sheets. Cite the URL and document date.
   - Without any product data: give a generic specification (duty point plus requirements) and mark the model "to select".
   - Check the duty point on the product curve or table, not only nominal values. For pumps and fans, check the operating point is in the efficient part of the curve and within the speed-control range.
5. **Alternatives.** Give two alternatives, from different manufacturers when possible, or one smaller and one larger size with the trade-off.

## 4. Verify

- Re-check units and orders of magnitude (kW vs W, m³/h vs l/s, kPa vs m).
- Selected duty covers the design duty without an extra unstated margin.
- Product rules from the jurisdiction files: ecodesign, energy label, F-gas, CE.
- Legal requirements: only from the official government sources listed in the jurisdiction file. Standards: number, edition, clause, no copied text.
- Every product value has a source: data sheet name, revision or date, URL.
- Anything not verified goes to "To verify".

## 5. Output

Use the selection sheet format in `references/selection-sheet.md`. Write it in `deliverable_language` from `PROJECT.md`.

Default output is Markdown in the chat or a `.md` file next to the project calculations. On request: `.xlsx` or `.docx` with the same sections.

For several units of the same type (for example 12 fan coils), use one sheet with a schedule table instead of 12 sheets.

## Rules

- The engineer decides. This skill prepares and checks the selection; it does not approve it.
- Never invent product data, model numbers or prices. Unknown means "to verify".
- Prefer lower energy use when two options meet the requirements. Say so in the sheet.
- Keep calculations reproducible: every number in the sheet comes from a script run, a user input or a cited source.
