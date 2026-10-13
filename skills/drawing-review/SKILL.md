---
name: drawing-review
description: Work with PDF drawing sets - build a sheet register from the title blocks, extract data from drawings (schedules, notes, areas, equipment tags), compare revisions of a set (added, removed, changed sheets), check a drawing against the project naming standard, and check that a package is complete for issue or for construction. Use when the user asks to list sheets, read a drawing set, build or check a drawing register, compare drawing revisions, find what changed between issues, extract a schedule from PDF drawings, or check a submission package.
---

# Drawing review

Goal: a register and a change list another engineer can check, built from the drawings themselves and not from memory. Every sheet in the register points to a file and a revision.

What needs Python: bulk work over a folder of PDFs - scanning, text extraction, building a CSV register, comparing registers. What does not: reading one drawing, answering a question about a sheet, or checking a package list, which the agent can do directly from the PDFs it can read.

## 1. Load context

- Read `PROJECT.md`: jurisdiction, disciplines, role, deliverable language, section "Project standards" (naming and numbering rules, revision and status codes, register location).
- No `PROJECT.md`: offer `project-brief`. If declined, ask for the project standard in use and the deliverable language.
- Load `references/shared/disciplines/<discipline>.md` for the drawing content (schedules, tags, symbols) of the disciplines in scope.
- Load `references/sheet-register.md` (this skill) for the register fields and the revision comparison rules.
- Load `references/pdf-extraction.md` (this skill) for what can be extracted from a PDF and what cannot.
- Naming and numbering rules come from `project-standards`. Do not duplicate them here; if the project has no rules, use that skill's ISO 19650 default and say so.

## 2. Collect inputs

1. **The set.** The folder, the file list, or the PDFs themselves. Ask for the issue date, the purpose of issue, and whether this is the current revision or a specific one.
2. **The register format.** The project's register structure (columns and order) from `PROJECT.md` or the BEP. Without one, use the default in `references/sheet-register.md` and say it is a default.
3. **Title block field map.** Which field is the sheet number, the title, the revision and the status, and where it sits on the sheet. For a bulk scan, a rules file (`references/pdf-extraction.md`) names the patterns.
4. **Comparison basis.** Which two issues to compare, and what counts as a change: revision code only, date, or content.
5. **Purpose of the check.** Completeness for issue, completeness for construction, or a data extraction question. Each gives a different report.

## 3. Work

**A. Register**

1. Per sheet, read the title block and take: sheet number, title, discipline, revision, status, date, scale, paper size, drawn by, checked by, approved by. Read them from the drawing, not from the file name; use the file name only to spot a mismatch.
2. Build the register. For a few sheets, write it directly. For a folder, run:
   ```
   python scripts/pdf_register.py scan --dir drawings --recursive --rules rules.json --csv register.csv
   python scripts/pdf_register.py titles --file drawings/A-101.pdf
   python scripts/pdf_register.py compare --a register-revB.csv --b register-revC.csv
   ```
   A rule that matches nothing (the script prints a `WARNING` on stderr) is a rules problem, not a drawing problem: check the JSON escaping and the wording of the title block, and fix the rules before reporting missing fields.
3. Mark every sheet where a field is missing, unreadable, or contradicts the file name. Never fill a field from another sheet's pattern.

**B. Content extraction**

Extract only what the user asked for, per discipline: schedules (doors, windows, equipment, valves, dampers), areas and quantities, equipment tags, legend and symbol lists, notes that carry requirements, room names and numbers.
- State the drawing, revision and sheet you read each value from.
- Vector PDFs give text; scanned sets need the agent to read the image. Say which case it is.
- Never transcribe a number from a low-resolution scan without flagging that it was read visually and must be confirmed.

**C. Revision comparison**

1. Compare the two registers first: sheets added, removed, revision or status changed, title changed. That is the cheap and reliable comparison.
2. For sheets whose revision changed, open both and report what changed where the user needs it (a schedule, a service route, a dimension that affects work). Do not claim what changed from the register alone.
3. Report the change list with sheet number, revision from, revision to and the change, plus the sheets where a change is known to exist but not yet identified.

**D. Package check**

Check against the drawing list the client or the BEP requires: every sheet present, at the right revision and status, no superseded revision in the package, file names matching the standard, and the transmittal list matching the folder contents.

## 4. Verify

- Every register row traces to a file. Count the rows against the number of PDFs and explain any difference (multiple sheets in one file, covers, empty files).
- Revision and status codes match the project standard exactly, including case.
- A revision change or a title change is confirmed by opening the sheet, not inferred from the file name.
- Extracted values are quoted with sheet number, revision and location on the sheet.
- Scanned or low-resolution content is flagged as read visually.
- The comparison basis is stated (revision code, date, or content), and sheets that could not be read are listed, not silently dropped.
- Naming check results follow `project-standards`; this skill reports them, it does not rename files.

## 5. Output

Write in `deliverable_language` from `PROJECT.md`. Default Markdown; on request `.csv` or `.xlsx`.

1. **Summary**: set reviewed, number of sheets, issues found in the title blocks, revision comparison result in one line.
2. **Sheet register**: table.
   | Sheet no. | Title | Discipline | Rev | Status | Date | Scale | Size | File | Note |
3. **Data extracted**: table per requested subject, with the sheet, revision and location of each value.
4. **Revision comparison**: added, removed, changed, and the not-compared list.
5. **Package check**: required sheets, present, missing, wrong revision, naming failures.
6. **To verify**: unreadable sheets, fields read visually, mismatches between file name and title block.

## Rules

- Do not modify, rename, move or re-save any drawing. Read only. Renaming is `project-standards`, and only after the user confirms a rename map.
- Do not invent a sheet number, revision or title. Missing means "to verify".
- The title block on the sheet wins over the file name. A mismatch is a finding, not a correction.
- Never state that a revision is superseded, or a package complete, without the client's issue list or the BEP to check it against.
- Keep the register reproducible: one row per sheet, with the file it came from.
