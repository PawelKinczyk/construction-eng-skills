# construction-eng-skills

Agent Skills for construction engineers, for design and contracting.
The skills work with Claude Code, claude.ai (web, desktop, mobile) and other agents that read the open Agent Skills format (`SKILL.md`).

> Status: early development (v0.1). No skills are ready yet. See [PLAN.md](PLAN.md).

## Skills

| Group | Skill | What it does | Status |
|---|---|---|---|
| Context | `project-brief` | Interviews the engineer and builds `PROJECT.md` | planned |
| Context | `project-standards` | Checks naming, layers, BEP and project rules | planned |
| Engineering | `equipment-selection` | Sizes and selects equipment, with sources and alternatives | planned |
| Engineering | `code-compliance` | Checks a design against law and standards, with clause references | planned |
| Engineering | `cost-estimate` | Quantity takeoff and unit rates from local price sources | planned |
| Engineering | `bid-review` | Analyses tender documents: scope, risks, questions, offer | planned |
| Engineering | `project-correspondence` | Letters, RFIs, notices, coordination issues | planned |
| Files | `drawing-review` | PDF drawing register, revision comparison, data extraction | planned |
| Files | `dxf-dwg-analysis` | DXF/DWG layers, blocks, counts, revision comparison | planned |
| Files | `ifc-analysis` | IFC quantities, property sets, IDS validation | planned |
| Site | `meeting-minutes` | Minutes with decisions and actions | planned |
| Site | `site-visit` | Site visit report from photos and dictation, works on mobile | planned |
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

1. Copy [templates/PROJECT.md](templates/PROJECT.md) into your project folder, or ask the agent: "set up a project brief".
2. Fill in jurisdiction, disciplines, role and deliverable language.
3. Work as usual. Every skill reads `PROJECT.md` first.

## Principles

- Skills are discipline- and country-neutral. Knowledge lives in `references/disciplines/` and `references/jurisdictions/`.
- No text of paid standards. Skills give the standard number, clause and where to get it.
- No invented clauses, prices or product data. Unknown values are marked "to verify".
- Calculations run in scripts, not in the model's head.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)
