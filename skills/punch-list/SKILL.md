---
name: punch-list
description: Build and run a defect or punch list (snag list, lista usterek) - raise items from a walkthrough, photos or dictation, with location, trade, description, severity, photo reference, responsible party and deadline; allocate items to trades, track them to completion, verify fixes and close them, and produce the handover view grouped by room, level or trade. Use when the user asks to prepare or update a punch list, add defects, check what is still open before handover, list overdue items by trade, or export the defect register as a table.
---

# Punch list

Goal: every defect has a place, an owner, a deadline, a photo and a status, and nothing is closed without someone having checked the fix. The list is the record that decides whether a room, a floor or the building is ready.

Two views come out of one register: the working view (by trade, for chasing) and the handover view (by room or level, for the client and for acceptance).

## 1. Load context

- Read `PROJECT.md`: jurisdiction, project stage, role, deliverable language, and the acceptance and handover procedure if the project has one (who accepts, what evidence, what deadlines).
- No `PROJECT.md`: offer `project-brief`. If declined, ask for the project name, the deliverable language and who signs off the fixes.
- Load `references/shared/disciplines/<discipline>.md` for the tolerances and the defects that matter in each discipline (a leak is not a scratch).
- Load `references/punch-list-format.md` (this skill) for the fields, the severity classes, the workflow and the handover rules.
- Defects recorded in a site report (`site-visit`) come here as items. Decisions about design questions go to the designer, not into this list.

## 2. Collect inputs

1. **The walkthrough material**: photos, dictation, notes, or the user's list. Ask for the areas covered and the date of the walkthrough.
2. **The reference document** for what "correct" means: the specification, the drawings, the manufacturer's instructions, the standard. Where a tolerance is claimed, the clause must be named. Without it, the defect is described by what was seen, not by a tolerance.
3. **Responsibility**: which party finishes each item. The contract decides, not the person who finds the defect. Where it is not obvious, ask.
4. **Severity convention**: the project's own (for example A/B/C or critical/major/minor) plus the deadlines attached to each class. Without one, use the default in `references/punch-list-format.md` and say it is a default.
5. **The existing register**, so items are added rather than duplicated.

## 3. Work

1. **Raise items** one per row: location, element and trade, description of the fact seen, severity, photo reference, party responsible and deadline.
   ```
   python scripts/punch_list.py init --file punch.json --project "Biurowiec Zabłocie B2"
   python scripts/punch_list.py add --file punch.json --location "skrz. A, poz. 0, pom. 1.04" \
       --trade sanitarne --element "izolacja przewodu c.w.u." \
       --description "Izolacja zakończona 300 mm przed zaworem odcinającym" --severity B \
       --photo "SV-007/4" --owner "Wykonawca / M. Lis" --due 2026-10-15
   python scripts/punch_list.py list --file punch.json --open --trade sanitarne
   python scripts/punch_list.py list --file punch.json --overdue
   python scripts/punch_list.py status --file punch.json --id U-001 --status fixed --note "poprawiono 14.10.2026, zdjęcie 22"
   python scripts/punch_list.py verify --file punch.json --id U-001 --by "Inspektor / T. Wrona" --note "sprawdzone 16.10.2026"
   python scripts/punch_list.py summary --file punch.json
   python scripts/punch_list.py export --file punch.json --csv punch.csv --view room
   ```
2. **Describe the fact, not the opinion**: "insulation ends 300 mm before the valve", not "sloppy work". Where a requirement is known, quote it with its document and clause; the requirement is what makes the item contractual rather than a preference.
3. **One item per defect per location.** A defect in three rooms is three items (or one item with the room list, when the fix is a single action — say which convention the list uses).
4. **Severity** according to the effect: safety or structural, functional, cosmetic, observation. Severity drives the deadline; say how.
5. **Photos**: reference the photo for each item, and say if the item has none. An item without a photo is weaker at handover; note what is missing (wide view, close-up, scale).
6. **Allocate** to the party responsible under the contract, and record the deadline from the severity class or the handover date.
7. **Track**: open, in progress, fixed, verified, closed, rejected (with reason). Only the party that did not do the work verifies the fix. Verification is a separate status from "fixed" and gets its own line.
8. **Handover view**: per room or per level, with the status of each item, ready for the walkthrough with the client. Items still open on the handover date are listed explicitly, with the plan for them.
9. **Never close silently**: closing requires a verifier, a date, and a note naming the evidence (photo, test, measurement).

## 4. Verify

- Every item has: location, trade, description of a fact, severity, owner, deadline, status. Photo references where they exist, and a flag where they do not.
- Every item traces to a source: the site report, the inspection, the photo, the test result, or a person who reported it (attributed).
- Descriptions use tolerances only with the source document and clause named.
- Owners are parties under the contract, and the allocation matches the contract, not the finding.
- No item is closed without a verifier different from the party who fixed it.
- Rejected items carry the reason and who rejected them.
- Design questions are not in the list; they are routed to the designer with a written record.
- Duplicates: check by location and element before adding, and merge with a note where the same defect was raised twice.
- The list states the walkthrough date and the areas covered, and which areas were not inspected.

## 5. Output

Write in `deliverable_language` from `PROJECT.md`. Markdown or `.xlsx` (default: `.xlsx` for a list that people work in, Markdown for a quick report).

1. **Summary**: items by status and severity, per trade, the count overdue, and what blocks handover.
2. **Working list**: grouped by trade, or one table with filters, with the columns from `references/punch-list-format.md`.
3. **Handover view**: per room or level, with open items marked.
4. **Overdue**: items past their deadline, with the owner and days late.
5. **Photos**: index of photo references used.
6. **To verify**: items without photos, without a source requirement, or with an owner the contract does not clearly assign.

## Rules

- A punch list is a record of facts and of responsibility agreed under the contract. It is not a claim, not a notice, not a valuation, and not a statement that the works are accepted.
- Never invent a defect, a location, a photo reference or a deadline.
- Never close an item to make a handover look cleaner. Open items at handover are normal; hidden ones are not.
- Do not edit or delete photos. Keep the originals.
- Do not name individuals in a way that personalises the defect; the responsible party is a company, with the person named only where the project's process needs a contact.
- Keep the register in a file, not only in a report: the list is a living document until the defects liability period ends.
