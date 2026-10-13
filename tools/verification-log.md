# Verification log

Record of smoke runs. Reviewer is the same model family that wrote the skills, so a pass here
means "passed first-stage verification", not "independently verified".

## 2026-10-13, first-stage smoke run (revision after df88c40)

Method: structural checks (`build.py check`, `verify_skills.py`), then for each skill the
procedure in `SKILL.md` and its references was walked against the "must show" column of
`smoke-prompts.md`. Scripts were run where the prompt needs one (`check_names.py`, `hvac_calc.py`).
The full eval prompts were not run as separate conversations.

| Skill | Result | Notes |
|---|---|---|
| project-brief | pass with notes | Found: "branża sanitarna" spans `plumbing` and `hvac` and the skill gave no rule. Fixed in `pl.md` and `SKILL.md`: ask which installations are in scope. |
| project-standards | pass | `check_names.py` rejects both names, proposes no sequence number. |
| equipment-selection | pass with notes | Flow and pipe pressure drop computed by script. The prompt gives no equipment pressure drop and no pipe material; the skill must ask for both. |
| code-compliance | pass with notes | Procedure fixes the WT version from the permit date and marks unread requirements TO VERIFY. The WT status paragraph in `pl.md` (announcement of 18.09.2026, act of 31 July 2026) is time-sensitive and needs a human check against gov.pl. |
| cost-estimate, bid-review, project-correspondence, drawing-review, dxf-dwg-analysis, ifc-analysis, meeting-minutes, site-visit, punch-list | pass (shallow) | Every "must show" element has matching text in `SKILL.md` or its references. Behaviour in a live conversation not yet observed. |

Open for a human: legal clause numbers marked "to verify", engineering typical values, a real-project
test, the mobile test on claude.ai.

## 2026-10-13, full evaluation of all 57 eval prompts

Method: for each skill an executor agent followed `SKILL.md` on the prompts only (it was not allowed
to read the expected outputs or the verification log) and ran the scripts; a separate judge agent
graded each answer against `expected_output` and the rubric in `tools/eval_runsheet.py`, re-ran
scripts, and classified each non-pass as a skill defect, an eval defect or an executor error.
Inputs the eval cases did not supply were created as synthetic fixtures by the executors.
Executors and judges are the same model family as the author of the skills: this is not an
independent review.

Result before fixes: 1 fail, 29 pass, 27 pass with notes.

| Skill | Cases | Skill defects found | Eval defects found |
|---|---|---|---|
| project-brief | 3 | none | case 2 contradicted the example brief (gas boilers vs district heating) |
| project-standards | 3 | none | none |
| equipment-selection | 10 | example `dhw-cylinder-P3.md` had wrong energy and power; unsourced stack capacity; ampacity taken from memory | none |
| code-compliance | 5 | no fallback when ISAP blocks fetching; skeleton status not shown; result labels not in document language | cases 3-5 lacked jurisdiction and data |
| cost-estimate | 4 | escalation run with placeholder rates | none |
| bid-review | 4 | none | no tender excerpt or risk register |
| project-correspondence | 4 | no draft when facts missing; no reminders drafted (the one fail); "for approval" line optional | case 1 role conflict |
| drawing-review | 4 | docstring rules JSON broke when copied; zero-match rule silent; status regex `{2}`; example rules.json not runnable; bad regex gave a traceback | no PDFs |
| dxf-dwg-analysis | 4 | extents included frozen layers without a note; `diff` did not compare attributes | no DXF files |
| ifc-analysis | 4 | type-level property sets not read; weak GUID-mismatch handling in `compare`; `ids` path broken against the installed ifctester | no IFC files |
| meeting-minutes | 4 | none | no notes, register or transcript |
| site-visit | 4 | no "tell the site manager now" rule; no cap on questions | no dictation or transcript |
| punch-list | 4 | example mixed two dates and counted an item twice | no notes or register |

All defects above were fixed in the same change; eval cases now name fixture files under
`skills/<name>/evals/files/` (generators included). The fixed scripts were re-run on those
fixtures. The fixed skills were NOT re-run through the full agent evaluation.

Still open for a human: legal clause numbers marked "to verify" (ISAP blocks automated fetching, so
no Polish legal text could be read), engineering typical values, a real-project test, the mobile test
on claude.ai.

## Re-evaluation of the fixed skills (2026-10-13)

Second agent run, same method (separate executors and judges, same model family, so still not an independent review) on the six skills changed by commit e126311: project-correspondence, drawing-review, dxf-dwg-analysis, ifc-analysis, site-visit, code-compliance (25 prompts, using the new fixtures).

| Skill | pass | pass with notes | fail |
|---|---|---|---|
| project-correspondence | 0 | 4 | 0 |
| drawing-review | 3 | 1 | 0 |
| dxf-dwg-analysis | 3 | 1 | 0 |
| ifc-analysis | 2 | 2 | 0 |
| site-visit | 2 | 2 | 0 |
| code-compliance | 0 | 5 | 0 |

The earlier fail (project-correspondence #3) is gone. Remaining skill defects found by the judges and fixed in the follow-up commit:

- code-compliance: results from an original-text journal PDF are TO VERIFY; topics that cannot be assessed become TO VERIFY rows; an applicability-list variant for "which regulations apply"; conclusions that depend on an unresolved row are conditional; a "Fire-rated cable circuits" topic in `fire.md`; eval #5 no longer expects a sprinkler pump for a project without sprinklers.
- project-correspondence: language rule when PROJECT.md is absent; no generic reservation of rights and no invented commitments in reminders; reminders get a number and a draft register row; written confirmation of verbal answers; "Register: none found" line; never borrow numbers from the example register.
- site-visit: "imminent danger" field in safety entries; purpose is "not recorded" when not given; no internal to-dos in client text; desktop-deferral line in the short form.
- dxf-dwg-analysis: summary states that inserts are counted and frozen-layer inserts are a separate subtotal.
- ifc-analysis: output ends with a routing line and a millimetre-unit warning.

Not done: the scripts' known minor items (duplicate Name/Tag columns in `ifc_report.py schedule`), a legible scan fixture for the drawing-review visual-read path, and a real DWG fixture. These second-pass edits were not re-run through agents.
