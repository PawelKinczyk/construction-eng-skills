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
