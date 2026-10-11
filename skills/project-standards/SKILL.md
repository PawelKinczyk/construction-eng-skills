---
name: project-standards
description: Check and enforce project information standards on construction projects - file naming (ISO 19650 or a project BEP), CAD layer names, Revit/IFC object and family naming, drawing numbers, revision and status codes, and other BEP or CAD standard rules. Use when the user asks to check names, verify files against the BEP, prepare a submission or transmittal, rename files to the standard, set up naming rules, or asks "is this compliant with the project standard".
---

# Project standards

Goal: every name and deliverable follows the project's information standard before it leaves the office. Output: a compliance report and, when asked, a rename map. The skill never renames or edits files without explicit confirmation.

## 1. Load context

- Read `PROJECT.md`, section "Project standards". It names the rules and the BEP or CAD standard document.
- If `project-standards.json` exists next to `PROJECT.md`, it holds the machine-readable naming rules. Use it.
- If it does not exist, build it in step 2.
- No `PROJECT.md`: offer `project-brief`. If the user declines, ask which standard applies (project BEP, client standard, or ISO 19650 default).

## 2. Collect inputs

**A. The rules**

1. Read the BEP or CAD standard named in `PROJECT.md`. Extract only the naming and delivery rules: fields, separators, allowed codes, case, revision and status format, file formats, layer naming.
2. Convert naming rules to `project-standards.json`. Format: see the docstring in `scripts/check_names.py` and the example `references/rules.iso19650-uk.json`.
3. Several rule sets are allowed (for example files, layers, sheets). Use one JSON per set: `project-standards.files.json`, `project-standards.layers.json`.
4. No project standard: propose ISO 19650 with UK NA codes (`references/iso19650-naming.md`) as default. Tell the user the codes are an example. Ask them to confirm the project code and originator code.
5. Show the rules as a short table and get confirmation before saving the JSON. Add the JSON path to "Project standards" in `PROJECT.md`.

Rules that are not about names (for example "PDF and DWG for every drawing", "IFC4 export every two weeks", "title block with QR code") go to a manual checklist. They do not go into the JSON.

**B. The items to check**

- Files: a folder (the script scans it), or a list pasted by the user.
- CAD layers: a layer list. Get it from `dxf-dwg-analysis` or from the user (export from AutoCAD: LAYER, then copy the names).
- Sheets and drawing numbers: from a drawing register (see `drawing-review`) or a pasted list.
- Model objects or families: a list exported from the model or from `ifc-analysis`.

## 3. Work

1. Run the check:
   ```
   python scripts/check_names.py project-standards.json --dir <folder> [--recursive] [--ext .pdf .dwg]
   python scripts/check_names.py project-standards.json --list names.txt --only-errors
   ```
   Exit code 1 means at least one name failed. That is a normal result, not a crash.
2. Check the manual rules from the checklist one by one. Mark each item `OK`, `FAIL` or `NOT CHECKED`, with the reason.
3. For each failure, give a fix:
   - Mechanical fixes (case, spaces, wrong separator): the script suggests them.
   - Wrong codes (wrong role or type code): propose the right code. Mark it "to confirm" when more than one code fits.
   - Missing fields (no level, no number): never invent a sequence number. Ask, or take it from the drawing register.
4. Look for patterns, not only single errors. Examples: "all files from originator XYZ use underscores", "all M3 models miss the level field". Report each pattern once.

**No Python available** (for example claude.ai mobile): check names manually against the rules table. Keep the same report format. Say the check was manual.

## 4. Verify

- Re-run the script on the proposed names. Every proposed name must pass.
- Names that must stay unique (drawing numbers, file names) are unique after the renames.
- Every rule in the report traces to a BEP or standard clause, or to the confirmed default.

## 5. Output

Write in `deliverable_language` from `PROJECT.md`:

1. **Summary**: items checked, failed, top 3 patterns.
2. **Naming results**: table with name, result, problem, proposed name. Long lists: failures only, plus a count of passes.
3. **Manual checklist results**: rule, result, note.
4. **Rename map** (when asked): CSV with `old_name,new_name`. Save next to the checked folder as `rename-map.csv`.
5. **To confirm**: codes or numbers that need the user's decision.

Renaming files: only after the user confirms the rename map. Then rename with a script that reads the CSV. Report every rename. Never overwrite an existing file.

## Rules

- The project BEP wins over ISO 19650 defaults and over this skill's examples.
- Never mix code sets. For example, `S` means structural in the UK NA and "sanitarne" in many Polish projects.
- Do not change file content in this skill. Only names and the report.
