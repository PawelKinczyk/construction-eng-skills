---
name: project-brief
description: Build or update PROJECT.md, the project context file that all construction-eng-skills read first. Interviews the engineer about a construction or building services project (scope, jurisdiction, disciplines, role, documents, standards, people, risks) and scans the project folder to pre-fill answers. Use at project start, when PROJECT.md is missing, or when the user says "set up a project brief", "update the brief", "add this to the project context", "new project", or shares new key project facts.
---

# Project brief

Goal: a short, accurate `PROJECT.md` that tells any agent what this project is, where its documents are, and what to watch out for. Every other skill in this collection reads it before working.

The skill has three modes:

| Mode | When | Result |
|---|---|---|
| Create | no `PROJECT.md` exists | new file from the template |
| Update | user gives new facts, decisions or documents | changed sections, `last_updated` set |
| Review | user asks "what is missing", or before a big task | gap list and questions |

## 1. Load context

- Look for `PROJECT.md` in the working directory, then in parent folders up to the project root.
- If it exists: read it and use Update or Review mode.
- If it does not exist: use Create mode. Template: `references/shared/PROJECT.template.md`.
- After the jurisdiction is known, load `references/shared/jurisdictions/<jurisdiction>.md`. For EU member states, also load `eu.md`.

## 2. Collect inputs

**Discover first, ask second.** Before asking anything, find what the project files already say.

1. If you have file access, list the project folder (2–3 levels deep). Ignore build output, caches and archives.
2. Identify key documents by name and type: contract, tender documents, drawings, specifications, models (IFC, RVT, DWG), correspondence, minutes.
3. Open only the first pages of key documents (title page, contract header, drawing title block) to read project name, number, client, location and phase.
4. Pre-fill every field you can. Mark each pre-filled value with its source file.

Then interview the engineer in rounds. One message per round, at most 6 questions per round. Show pre-filled values for confirmation instead of asking again.

| Round | Topic | Questions |
|---|---|---|
| 1 | Basics | name, number, client, location, phase, jurisdiction, disciplines, our role, deliverable language |
| 2 | Scope | what is in our scope, what is explicitly excluded, key deliverables and deadlines |
| 3 | Documents | confirm the document map; where the missing ones are |
| 4 | Standards | file naming, layer or family naming, BEP or CAD standard, drawing numbering, revisions |
| 5 | People | client contact, design lead, other disciplines, contractor, site manager |
| 6 | Watch-outs | risks, client preferences, known problems, lessons from similar projects, things to check every time |

Interview rules:
- Ask in the user's language. Field keys in the YAML block stay in English.
- Accept "skip" or "don't know" for any question. Put it in "Open questions".
- Stop after round 1 if the user wants a quick start. Rounds 2–6 can follow later.
- If the user pastes a long text (email, meeting notes, tender summary), extract facts from it first and ask only about gaps.

Allowed values for the YAML block are in the template comments. If the jurisdiction has no file in `references/shared/jurisdictions/`, write the country code anyway and tell the user that country-specific references are missing.

## 3. Work

**Create mode**
1. Copy the template structure exactly. Keep all headings, even empty ones.
2. Fill the YAML block and sections from the discovered facts and answers.
3. Document map: relative paths from the `PROJECT.md` location, or links. Add revision or date when known.
4. Watch-outs: short, concrete, testable lines. Good: "Client requires Daikin or equivalent for VRF". Bad: "client is demanding".
5. Set `last_updated` to today (YYYY-MM-DD).

**Update mode**
1. Change only the affected sections.
2. Decisions go to the "Decisions" table with date and source (meeting, email, drawing).
3. Answered open questions: tick them and move the answer to the right section.
4. Never delete existing content without asking. Superseded facts: strike through and add the new value.
5. Set `last_updated`.

**Review mode**
1. List empty or vague fields, ordered by impact on engineering work.
2. Flag stale facts: documents with a newer revision in the folder, `last_updated` older than 30 days during construction.
3. Ask the top questions as one round.

## 4. Verify

- Every pre-filled value has a source file, or the user confirmed it.
- Jurisdiction-specific checks from the jurisdiction file. Example for Poland: which WT version applies, based on the permit application date.
- Legal facts (which regulation applies, transition rules) come only from the official government sources in the jurisdiction file. Never from news, blogs or vendor pages.
- Paths in the document map exist (when you have file access).
- No guessed facts. Unknown goes to "Open questions".

## 5. Output

1. Save `PROJECT.md` in the project root, or in the folder the user names.
   - No file access (for example claude.ai on mobile): show the full file in one block and tell the user to save it as `PROJECT.md` in the project folder.
2. Write all section content in the user's language. YAML keys and section headings stay in English, so other skills can parse them.
3. After saving, report in at most 5 lines:
   - mode used, and sections created or changed,
   - number of open questions,
   - the 1–3 most important gaps,
   - the next suggested step (for example: run `project-standards` when naming rules are set).

## Rules

- Keep `PROJECT.md` short: target under 150 lines. Link documents, do not copy their content.
- Never store passwords, personal ID numbers or bank data. Contact data only when the user gives it.
- One project per `PROJECT.md`. For a multi-building site, use one file per building and link them under "Documents".
