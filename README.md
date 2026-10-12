# construction-eng-skills

Agent Skills for construction engineers, for design and contracting.
The skills work with Claude Code, claude.ai (web, desktop, mobile) and other agents that read the open Agent Skills format (`SKILL.md`).

> Status: early development (v0.1). Skills in beta: `project-brief`, `project-standards`, `equipment-selection` (HVAC, plumbing, electrical, fire), `code-compliance`. See [PLAN.md](PLAN.md).

## Skills

| Group | Skill | What it does | Status |
|---|---|---|---|
| Context | `project-brief` | Interviews the engineer and builds `PROJECT.md` | beta |
| Context | `project-standards` | Checks naming, layers, BEP and project rules | beta |
| Engineering | `equipment-selection` | Sizes and selects equipment, with sources and alternatives | beta (HVAC, plumbing, electrical, fire) |
| Engineering | `code-compliance` | Checks a design against law and standards, with clause references | beta |
| Engineering | `cost-estimate` | Quantity takeoff, unit rates and cost structure from local price sources | beta |
| Engineering | `bid-review` | Analyses tender documents: scope, risks, questions, offer | beta |
| Engineering | `project-correspondence` | Letters, RFIs, notices, coordination issues, register | beta |
| Files | `drawing-review` | PDF drawing register, revision comparison, data extraction | beta |
| Files | `dxf-dwg-analysis` | DXF/DWG layers, blocks, counts, revision comparison | beta (DXF) |
| Files | `ifc-analysis` | IFC quantities, property sets, IDS validation | beta |
| Site | `meeting-minutes` | Minutes with decisions and actions, plus the registers | beta |
| Site | `site-visit` | Site visit report from photos and dictation, works on mobile | beta |
| Site | `punch-list` | Defect register | planned |

Disciplines: architecture and structural (general), HVAC, plumbing, electrical, fire protection.
Jurisdictions: EU, Poland, United Kingdom, United States.

## Install

### Claude Code

```
/plugin marketplace add PawelKinczyk/construction-eng-skills
/plugin install construction-eng-skills@construction-eng-skills
```

### claude.ai (web, desktop, mobile)

1. Download a skill zip from the Releases page.
2. Go to Settings → Capabilities → Skills and upload the zip.

### Other agents (Codex, Hermes, others)

Copy the folder `skills/<skill-name>/` into the agent's skills directory.

## Quick start

1. Copy [shared/references/PROJECT.template.md](shared/references/PROJECT.template.md) into your project folder, or ask the agent: "set up a project brief".
2. Fill in jurisdiction, disciplines, role and deliverable language.
3. Work as usual. Every skill reads `PROJECT.md` first.

## Optional Python dependencies

Most skills work with no Python at all. The file-reading skills use scripts for bulk work, with
dependencies they declare and check themselves:

```
pip install -r tools/requirements-optional.txt
```

| Package | Used by | Without it |
|---|---|---|
| `pypdf` (or Poppler `pdftotext`) | `drawing-review` | the agent reads the PDFs directly; folder scans stop with an install hint |
| `ezdxf` | `dxf-dwg-analysis` | DXF analysis is unavailable |
| `ifcopenshell` | `ifc-analysis` | IFC analysis is unavailable |
| ODA File Converter (external, not pip) | `dxf-dwg-analysis` | DWG files can only be analysed after conversion to DXF |

## Principles

- Skills are discipline- and country-neutral. Knowledge lives in `references/disciplines/` and `references/jurisdictions/`.
- No text of paid standards. Skills give the standard number, clause and where to get it.
- No invented clauses, prices or product data. Unknown values are marked "to verify".
- Calculations run in scripts, not in the model's head.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
