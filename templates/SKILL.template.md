---
name: skill-name
description: One or two sentences. What the skill does and when to use it. Name the trigger phrases and the tasks it covers, because the agent picks the skill from this text alone.
---

# Skill title

One paragraph: the goal of this skill and its output.

## 1. Load context

- Read `PROJECT.md` in the working directory or project root.
- If it is missing, offer to run `project-brief`. If the user declines, ask only for: jurisdiction, discipline, role, deliverable language.
- Load `references/shared/jurisdictions/<jurisdiction>.md` and `references/shared/disciplines/<discipline>.md` for every discipline in scope.

## 2. Collect inputs

- Use the input checklist for this task from the discipline file.
- Ask for missing data in one message, not one question at a time.
- Never assume silently. Every assumption goes to the "Assumptions" list in the output.

## 3. Work

The procedure, as numbered steps. Use `scripts/` for every calculation and show formula, inputs, result and units.

## 4. Verify

- Check results against sources (standards, law, product data, project documents).
- Cite every source: document, clause or page, edition or date.
- Never invent clause numbers, prices or product data. Unknown means "to verify".

## 5. Output

Fixed format, written in `deliverable_language` from `PROJECT.md`:

1. Summary
2. Result
3. Assumptions
4. Sources
5. To verify

## Rules

- Keep this file under 500 lines. Move detail to `references/`.
- Do not copy text of paid standards. Reference number, clause and where to get it.
