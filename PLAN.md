# construction-eng-skills: implementation plan

Public, open-source set of Agent Skills for construction engineers (design and contracting).
Skills are written in English. Deliverables are produced in the language set in `PROJECT.md`.

Status: phases 0-4 done, phase 5 in progress. Last update: 2026-10-12.

Progress notes:
- Phase 0, 1 done.
- Phase 2 done: `equipment-selection` covers HVAC, plumbing, electrical and fire, each with a script, an example and evals; `code-compliance` has 5 evals and 4 examples (HVAC, plumbing, electrical, fire). Discipline files `hvac.md`, `plumbing.md`, `electrical.md`, `fire.md` are at v0.1 (structure full, values to review).
- Phase 3 done, except the real-project check of its done criterion: `cost-estimate`, `bid-review` and `project-correspondence` each have references, a script, examples and 4 evals.
- Phase 4 done: `drawing-review`, `dxf-dwg-analysis` and `ifc-analysis` each have references, a script, an example and 4 evals. Legal clause numbers and the real-project checks of the phase done criteria remain open.
- Phase 5 in progress: `meeting-minutes` and `site-visit` done. `punch-list` next; the mobile test needs claude.ai (phase 5 done criterion).
- Optional Python dependencies are declared in `tools/requirements-optional.txt` (pypdf, ezdxf, ifcopenshell, ODA File Converter); missing dependencies degrade to a clear message, and the drawing skill works without Python at all.
- `architecture.md` and `structural.md` remain skeletons; `uk.md` and `us.md` remain skeletons (phase 6).
- Still open for a v1.0 pass: verified legal clause numbers (all jurisdiction references marked "to verify"), and real-project checks of the done criteria.

---

## 1. Principles

1. **One method, many disciplines.** `SKILL.md` holds a discipline-neutral procedure. Discipline knowledge lives in `references/disciplines/*.md`.
2. **One method, many countries.** Country-specific law, standards and price sources live in `references/jurisdictions/*.md`.
3. **Project context first.** Every skill reads `PROJECT.md` before working: jurisdiction, disciplines, role, units, document locations, project standards.
4. **No copyrighted standard text.** Skills reference standards and laws by number and clause and say where to get them. The user supplies the text when needed.
5. **Law from government sources only.** Each jurisdiction file lists the official government domains for law and regulations. News, blogs and vendor pages are never a legal source.
6. **Never invent.** No invented clause numbers, prices or product data. Unknown means "to verify", with a stated assumption.
7. **Deterministic math in scripts.** Calculations run in `scripts/*.py`, not in the model's head. Exception: skills that must work on mobile (no Python).
8. **No duplication of built-in tools.** Generic PDF/DOCX/XLSX handling is left to Claude's built-in skills. Our skills add construction-specific workflows on top.
9. **Agent-agnostic.** Follow the open Agent Skills format (`SKILL.md` + frontmatter), so skills work in Claude Code, claude.ai (web, desktop, mobile), Codex and Hermes.

---

## 2. Dimensions

### Disciplines (`shared/references/disciplines/`)

| File | Scope at v1.0 |
|---|---|
| `architecture.md` | general only |
| `structural.md` | general only |
| `hvac.md` | full |
| `plumbing.md` | full (water supply, drainage, sewage) |
| `electrical.md` | full |
| `fire.md` | full (sprinklers, detection, smoke control, passive) |

### Jurisdictions (`shared/references/jurisdictions/`)

| File | Content |
|---|---|
| `eu.md` | CPR 305/2011, Ecodesign/ErP, EN and Eurocodes map, EUR-Lex |
| `pl.md` | Prawo budowlane, WT 2021, fire regulations, PN-EN via PKN, ISAP; price sources KNR/KNNR, Sekocenbud, Intercenbud |
| `us.md` | IBC, IMC, IPC, NFPA 70/13/72, ASHRAE 90.1/62.1, state adoption note; price source RSMeans |
| `uk.md` | Building Regulations and Approved Documents, BS EN, CIBSE guides; price sources SPON's, BCIS |

Each jurisdiction file has the same sections: legal hierarchy, official legal sources (government domains only), standards and product data, standards map by topic, approvals/permits, price sources, units and conventions.

---

## 3. Skills (13)

### Context layer
| Skill | Purpose | Output |
|---|---|---|
| `project-brief` | Interview the engineer at project start or during the project; build and update `PROJECT.md` | `PROJECT.md` |
| `project-standards` | Check and enforce project standards: file naming, layers, families, BEP rules, workflow | compliance report, corrected names |

### Engineering
| Skill | Purpose | Output |
|---|---|---|
| `equipment-selection` | Size and select equipment with inputs, calculation, margins, product check, alternatives | selection sheet |
| `code-compliance` | Check a design or solution against applicable law and standards, with clause references and sources | compliance checklist |
| `cost-estimate` | Quantity takeoff, unit rates from jurisdiction price sources, overheads | estimate (xlsx) |
| `bid-review` | Analyse tender and client documents: scope, risks, assumptions, exclusions, clarification questions, then the offer | bid review report, RFI list, offer |
| `project-correspondence` | Letters, RFIs, transmittals, notices (incl. FIDIC), change requests, coordination issue reports | letter / issue (docx, md) |

### Files
| Skill | Purpose | Output |
|---|---|---|
| `drawing-review` | PDF drawing sets: sheet register from title blocks, revision comparison, data extraction | register, diff report |
| `dxf-dwg-analysis` | DXF via `ezdxf`; DWG via ODA File Converter. Layers, blocks, attributes, counts, revision diff | takeoff, layer report |
| `ifc-analysis` | IFC via `ifcopenshell`: element counts, quantities, Psets, missing parameters, IDS validation | schedules, validation report |

### Site
| Skill | Purpose | Output |
|---|---|---|
| `meeting-minutes` | Minutes with decisions and actions (owner, deadline), decision log | minutes |
| `site-visit` | Site visit or inspection from photos and dictation; mobile-friendly (no scripts) | site visit report |
| `punch-list` | Defect register: location, photo, trade, status, deadline | defect log (xlsx/md) |

Out of scope: Revit (separate MCP project), agent-workflow skills (model routing, delegation, git, email).

---

## 4. Repository structure

```
construction-eng-skills/
  README.md                     # what it is, install, quick start
  LICENSE
  CONTRIBUTING.md               # how to add a discipline, jurisdiction or skill
  PLAN.md
  .claude-plugin/
    plugin.json                 # Claude Code plugin manifest
    marketplace.json            # install via /plugin marketplace add
  templates/
    SKILL.template.md           # standard skill layout
  shared/
    references/
      disciplines/*.md          # single source of truth
      jurisdictions/*.md
      PROJECT.template.md       # project context template, shipped with every skill
  skills/
    <skill-name>/
      SKILL.md
      references/               # skill-specific refs
        shared/                 # generated copy of shared/references (do not edit)
      scripts/                  # Python helpers
      evals/evals.json          # test prompts and expectations
      examples/                 # sample inputs and outputs
  tools/
    build.py                    # copy shared refs into skills, validate, zip for claude.ai
  dist/                         # zips for claude.ai upload (gitignored, built in CI)
```

Why copy shared refs into each skill: a skill uploaded to claude.ai must be self-contained and cannot read other skills' files. `shared/` stays the single source of truth. `tools/build.py` syncs the copies and CI fails if they drift.

---

## 5. Standard skill layout

Every `SKILL.md` follows the same sections:

1. **Load context**: read `PROJECT.md`. If missing, offer `project-brief` or ask for the minimum (jurisdiction, discipline, role).
2. **Collect inputs**: checklist from the discipline file. Ask for missing data. List every assumption.
3. **Work**: the procedure. Use scripts for calculations.
4. **Verify**: check against sources. Mark unknowns as "to verify".
5. **Output**: fixed format, in the deliverable language from `PROJECT.md`.

Rules: `SKILL.md` under 500 lines; details go to `references/`. Frontmatter `description` states clearly when the skill triggers.

---

## 6. Phases

### Phase 0: foundation
- `git init`, README, LICENSE, CONTRIBUTING, `.gitignore`
- `shared/references/PROJECT.template.md`, `templates/SKILL.template.md`
- `shared/references/` skeleton: all 6 discipline files and 4 jurisdiction files with section headings
- `.claude-plugin/plugin.json` and `marketplace.json`
- `tools/build.py` (sync refs, validate frontmatter, build zips)

Done when: the plugin installs in Claude Code from a local path, with no skills yet.

### Phase 1: context layer
- `project-brief`, `project-standards`
- `pl.md` and `eu.md` filled

Done when: interviewing for a real project produces a usable `PROJECT.md`, and `project-standards` catches naming errors in a sample file list.

### Phase 2: engineering core
- `equipment-selection` (HVAC first, then plumbing, electrical, fire)
- `code-compliance`
- `hvac.md`, `plumbing.md`, `electrical.md`, `fire.md` filled

Done when: selecting a real pump and a real AHU gives a correct sheet with sources and a verification list.

### Phase 3: commercial and correspondence
- `cost-estimate`, `bid-review`, `project-correspondence`

Done when: a real tender package gives a risk list, clarification questions and an offer draft.

### Phase 4: files
- `drawing-review`, `dxf-dwg-analysis` (with ODA conversion), `ifc-analysis`

Done when: a real drawing set gets a register and a revision diff; a real DWG and a real IFC give correct counts.

### Phase 5: site
- `meeting-minutes`, `site-visit`, `punch-list`
- Mobile test: upload to claude.ai, run a site visit on the phone

Done when: a real site visit gives a report on the phone, and the docx is generated afterwards.

### Phase 6: release v1.0
- `us.md`, `uk.md` filled; `architecture.md`, `structural.md` general content
- Evals pass for all skills; examples for all skills
- Public GitHub repo, release with zips, announcement (blog)

---

## 7. Definition of done (per skill)

- `SKILL.md` follows the standard layout and is under 500 lines
- Reads `PROJECT.md`; works with PL and EU at minimum
- No invented clauses, prices or product data in eval runs
- `evals/evals.json` with at least 3 realistic prompts; all pass
- One example in `examples/`
- Tested in Claude Code and on claude.ai

---

## 8. Open decisions

- **License:** proposal Apache-2.0 for code and MIT-like freedom for skills, or CC BY 4.0 for reference content. Decide in Phase 0.
- **Repo name and owner:** decided: `PawelKinczyk/construction-eng-skills`, private during development, public at v1.0.
- **Relation to `hermes-aec-template`:** separate repo; template links to this one.
- **Borrowed upstream skills:** none copied; link only, unless the license allows reuse with attribution.
