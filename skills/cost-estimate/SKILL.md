---
name: cost-estimate
description: Prepare, check or compare a construction cost estimate - quantity takeoff from drawings, schedules or a model, unit rates from the project's price sources, direct costs with overheads, profit and VAT, escalation and contingency, and the estimate report. Use when the user asks to estimate or price works, prepare a kosztorys or bill of quantities (BOQ), do a quantity takeoff, check a contractor's estimate or a bid price, compare offers on price, or asks "what will this cost" or "how much for this scope".
---

# Cost estimate

Goal: an estimate where every line can be checked by another engineer - quantity, unit, unit rate, source, and the arithmetic. Currency, overheads and tax follow the project's jurisdiction and the client's price structure.

Nothing is invented. Every unit rate has a named source and a date. A missing rate becomes "to verify", never a guess from memory or from another project.

## 1. Load context

- Read `PROJECT.md`: jurisdiction, project type, role, currency, deliverable language, estimator conventions (price level, whether VAT is included, price source).
- No `PROJECT.md`: offer `project-brief`. If declined, ask for jurisdiction, project type, currency, price level date and the price source.
- Load `references/shared/jurisdictions/<jurisdiction>.md`, section "Price sources" and "Units and conventions", and `eu.md` for EU member states.
- Load `references/estimate-structure.md` (this skill) for the cost structure, markups and rounding.
- Load `references/takeoff-rules.md` (this skill) for measurement and quantity rules.

## 2. Collect inputs

1. **Price source.** Ask which source the project uses and get the edition or date:
   - Poland: KNR/KNNR catalogues, Sekocenbud or Intercenbud price levels, or the contractor's priced BOQ. Structure of the detailed estimate: see `estimate-structure.md`.
   - UK: NRM2 or CESMM4 measure with SPON's or BCIS rates.
   - US: MasterFormat with RSMeans, or the contractor's unit price book.
   - EU and international: BOQ in the client's structure, CESMM4 or a project-specific measurement rule.
   State the price level (month and year). Rates without a price level cannot be compared.
2. **Scope.** Which works are in the estimate, and which are excluded. Get the boundary from the tender documents, the technical description or the client's scope list.
3. **Quantities.** From where: drawings and schedules, a model takeoff (`ifc-analysis`, `dxf-dwg-analysis`), a measurement sheet, a contractor's BOQ, or a rate for a lump sum.
4. **Cost structure.** Which components the client wants: direct costs only, or with overheads, profit, contingency, escalation and tax. Ask for the percentages and their contractual source.
5. **Constraints.** Budget ceiling, price validity, currency and indexation clause from the contract, and payment terms that affect the price.

Ask for everything missing in one message. Every assumption goes into the output.

## 3. Work

1. **Structure the estimate** as a group and line tree: group (element or trade), then lines with quantity, unit, unit rate, source.
2. **Take off quantities.** Follow `takeoff-rules.md`. Show the measurement rule for each line type. Round the quantity to the unit's normal precision and state it.
3. **Unit rates.** In order of preference:
   - Rates given by the user or in the tender documents.
   - Rates from the jurisdiction price source, with the table and position number, and the price level date.
   - A published unit price from a named source with the date.
   - Without any source: the line stays empty, marked "to verify", with the quantity left in place so the estimate can be priced later.
   Never average unrelated projects to produce a rate. Never adjust a rate by an unknown factor.
4. **Calculate.** Use `scripts/estimate_calc.py`. Do not do the arithmetic in your head:
   ```
   python scripts/estimate_calc.py line --qty 145.5 --unit-rate 210.50 --unit m2 --name "Tynki wewnętrzne"
   python scripts/estimate_calc.py rollup --file boq.json --json
   python scripts/estimate_calc.py escalation --value 1250000 --percent 4.5 --periods 2
   python scripts/estimate_calc.py range --value 1250000 --percent 15
   ```
   Do not run `escalation` with placeholder percentages. Ask for the index and the period first. If the user wants an illustration, label it "illustration, not a forecast, rate to verify".
   The direct cost breakdown (R, M, S), overheads (Kp), profit (Z), purchase costs (Kz), contingency, escalation and VAT are described in `estimate-structure.md`. Apply each markup once, at one level.
5. **Check.** Compare with:
   - another estimate for the same scope, when one exists (per unit of area, volume or capacity, after normalising the scope);
   - the budget or the cost ceiling, when one exists;
   - the ratio of the main trades, to spot a group that is out of proportion.
6. **Present the uncertainty.** State the estimate class and range (see `estimate-structure.md`), the main cost drivers, and the three to five items that could move the total most.

## 4. Verify

- Every quantity has a source (drawing and revision, schedule, model, measurement sheet) and a measurement rule.
- Every unit rate has a source and a price level date. No rate from memory or from an unnamed project.
- Percentages (Kp, Z, Kz, contingency, escalation, VAT) each have a source: contract, client instruction or jurisdiction file.
- Arithmetic re-checked by script; totals in the script output match the report.
- Units are consistent: the same unit per line type, m3 for volumes, m2 for areas, t for steel, kpl or Nr for items.
- Currency stated once, with rounding rules per `estimate-structure.md`, and net and gross both shown.
- The scope list in the output matches the scope actually estimated. Exclusions are named.
- Unknown rate, unknown quantity or unknown scope: "to verify".
- Legal or tax points: only from the official government sources in the jurisdiction file. Tax rates change; check the current rate and its source, and mark it with the date read.

## 5. Output

Write in `deliverable_language` from `PROJECT.md`.

1. **Summary**: scope, price level, price source, total net and gross, estimate class and range, main cost drivers.
2. **Estimate table**: group, line, quantity, unit, unit rate, value, source. One row per line; group subtotals.
3. **Cost structure**: direct costs with the R, M, S split where known, overheads, profit, contingency, escalation, net total, VAT, gross total, each with its percentage and source.
4. **Assumptions**: every assumed value, quantity source and exclusion.
5. **Sources**: price source edition or date, catalogue positions, tender documents, drawings with revisions, measurement rules.
6. **To verify**: rates without a source, quantities from an early revision, scope questions, tax and indexation clauses to confirm.

Formats: Markdown by default. On request `.xlsx` (one row per line, subtotal formulas) or `.docx`.

For a large estimate, keep the chat output to the summary, the structure and the to-verify list, and write the full line list to a file next to the project documents.

## Rules

- This is a cost estimate, not a price offer, a valuation or a certified kosztorys. Say so in the summary.
- The estimator and, for a bid, the contractually responsible person decide the price. This skill prepares and checks it.
- Never invent a rate, a quantity or a normative labour input.
- Keep the estimate reproducible: every number traces to an input, a script run or a named source.
- When the user asks for a bid price rather than a cost estimate, use `bid-review` for the risk and contract side and come back here for the numbers.
