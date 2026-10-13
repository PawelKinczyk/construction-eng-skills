---
name: code-compliance
description: Check a building design, system, room, product or solution against applicable building law, regulations and standards for the project's country, and produce a compliance checklist with exact legal references and sources. Covers HVAC, plumbing, electrical, fire protection, architecture and structural topics. Use when the user asks "is this compliant", "which regulations apply", "check against WT / Building Regulations / IBC", "what does the law require for...", prepares a design for permit or review, or answers a reviewer's or authority's comments.
---

# Code compliance

Goal: a compliance checklist where every requirement has an exact, checkable source and every result is clear: OK, FAIL, TO VERIFY or NOT APPLICABLE. The engineer can hand it to a reviewer.

## 1. Load context

- Read `PROJECT.md`: jurisdiction, location, phase, building type, disciplines, role, watch-outs.
- No `PROJECT.md`: offer `project-brief`. If declined, ask for country, building type, discipline and the permit application date.
- Load `references/shared/jurisdictions/<jurisdiction>.md` (and `eu.md` for EU member states). Use only its "Official legal sources" for law.
- If the jurisdiction file says `Status: skeleton`, tell the user in the answer, build the list from the official sources only, and mark every item taken from that file TO VERIFY.
- Load `references/shared/disciplines/<discipline>.md`, section "Compliance topics".

## 2. Collect inputs

1. **Which rules apply in time.** Find the regulation version that applies to this project. It usually depends on the permit application date and transition rules. Example for Poland: which WT version. If unclear, stop and ask. Do not check against the wrong edition.
2. **Building classification.** Building type, height group, use and occupancy, fire category or risk class, number of storeys. Classification drives most requirements. Confirm it before checking details.
3. **Scope of the check.** The whole discipline, one system, one room type, or one question. Agree the scope before writing the checklist.
4. **Design data.** Drawings, schedules, calculations, technical description, product data. Ask for the specific values the requirements need.

## 3. Work

1. **Build the checklist.**
   - Start from "Compliance topics" in the discipline file.
   - Map each topic to its legal source in the jurisdiction file: "Legal hierarchy" and "Standards map by topic".
   - Drop topics that do not apply. Keep them in the list with result NOT APPLICABLE and the reason.
   - A topic that cannot be assessed (no data, no readable source) is still a row with result TO VERIFY. A short line per topic is enough. Do not invent a fifth result value.
   - A question of the type "which regulations apply" with no design data: give an applicability list (topic, source, why it applies, what data is needed) instead of the 8-column checklist. Offer the checklist once the data exists.
   - A conclusion that rests on an unresolved row (for example "is this wall a fire separation") is conditional on that row. Say so in its result and in the summary.
2. **Get each requirement from the source.**
   - Law and regulations: read the current text on an official government source from the jurisdiction file. Cite act, date, article or paragraph, and the consolidated text or journal reference you read.
   - Standards: cite number, edition and clause. Do not quote paid standard text. Use the value only when the user provides the standard or the law itself states the value.
   - If you cannot read the source, the requirement is TO VERIFY. Do not fill it from memory.
   - If an official legal site blocks automated fetching (for example the ISAP human-verification page), try the official journal PDF on an official domain from the jurisdiction file. If that fails, ask the user to paste the clause or the consolidated text. The requirement stays TO VERIFY meanwhile.
   - A journal PDF holds only the original text of an act. When the act is often amended, a result from it alone is TO VERIFY, or carries the note "original text only, amendments not checked". Never give a hard OK or FAIL from it. Report the blocked site to the user as a finding.
3. **Compare.** For each requirement: the required value, the design value with its source (drawing, page, calculation), and the result.
4. **Explain failures.** For each FAIL: what is wrong, by how much, and one or two ways to fix it. Do not redesign; propose.
5. **Conflicts.** When two sources conflict, apply the hierarchy from the jurisdiction file and say which one wins and why.

## 4. Verify

- Every requirement has a source that another engineer can open: official URL or standard reference with edition and clause.
- No legal source outside the official government domains in the jurisdiction file.
- No invented paragraph numbers. If you are not sure of the exact paragraph, cite the chapter and mark TO VERIFY.
- The regulation edition matches the project date.
- Results use only the four values: OK, FAIL, TO VERIFY, NOT APPLICABLE. In the deliverable they are shown with a label in `deliverable_language` (see section 5).

## 5. Output

Write in `deliverable_language` from `PROJECT.md`. Section headings in that language.

1. **Summary**: scope, regulation editions used, counts per result, the most serious FAIL items.
2. **Basis**: building classification, project date used for edition choice, documents checked (with revisions).
3. **Checklist**: table. The four result values stay as codes, shown with a label in `deliverable_language`, e.g. pl: OK, NIEZGODNE (FAIL), DO WERYFIKACJI (TO VERIFY), NIE DOTYCZY (NOT APPLICABLE). Keep all 8 columns.

   | # | Topic | Requirement | Source | Design value | Design source | Result | Note / fix |
   |---|---|---|---|---|---|---|---|

4. **Failures and fixes**: one short paragraph per FAIL.
5. **To verify**: requirements without a readable source, missing design data, questions to the user or authority.
6. **Sources**: list of laws (with URLs on official domains), standards (number, edition), project documents.

Default format: Markdown. On request: `.xlsx` (one row per checklist line) or `.docx`.

## Rules

- This is a support check, not a legal opinion or an approval. Say so in the summary.
- The project-specific fire safety expert, authority or reviewer decides in disputed cases. Flag those cases; do not decide them.
- Never lower a legal requirement because of a contract, client wish or cost.
- Keep the checklist focused. A long list of NOT APPLICABLE lines hides real problems; group them in one line per topic.
