# Contributing

## Repository layout

- `shared/references/` is the single source of truth for discipline and jurisdiction knowledge.
- `skills/<name>/references/shared/` is a generated copy. Do not edit it by hand.
- `tools/build.py` syncs the copies, validates skills and builds zips.

```
python tools/build.py sync      # copy shared references into all skills
python tools/build.py check     # validate skills, detect drift
python tools/build.py package   # check, then build dist/<skill>.zip
```

Run `sync` and `check` before every commit.

## Add a jurisdiction

1. Copy an existing file in `shared/references/jurisdictions/` and keep all section headings.
   List the country's official government domains under "Official legal sources".
2. Fill in each section. Link official sources.
3. Run `python tools/build.py sync`.

## Add or extend a discipline

1. Edit or create a file in `shared/references/disciplines/` and keep the section headings.
2. Put country-specific content in the jurisdiction files, not here.
3. Run `python tools/build.py sync`.

## Add a skill

1. Copy `templates/SKILL.template.md` to `skills/<name>/SKILL.md`. The folder name must equal `name` in the frontmatter.
2. Keep the five sections: Load context, Collect inputs, Work, Verify, Output.
3. Add `evals/evals.json` with at least 3 realistic prompts and one example in `examples/`.
4. Run `python tools/build.py sync` and `python tools/build.py check`.

## Scripts and dependencies

- Scripts use the Python standard library by default. A skill that needs more declares it in
  `tools/requirements-optional.txt` and says in its `SKILL.md` what works without Python.
- A script must never crash on a missing dependency: catch the import, print which package to
  install, and exit with a clear code (see `skills/drawing-review/scripts/pdf_register.py`).
- Every script prints its inputs, the formula and the result with units, and supports `--json`.
- Never invent a value to fill a gap: an unsourced number goes out as an empty field or "to verify".

## Line endings

The repository uses LF (`* text=auto eol=lf` in `.gitattributes`). On Windows, `Path.write_text`
and similar helpers write CRLF unless told otherwise: pass `newline="\n"`, or normalize before
committing. `core.autocrlf` should be `false` in this repository.

## Content rules

- Never copy text from paid or copyrighted standards. Give the number, clause and source.
- Never invent clause numbers, prices or product data.
- Cite official sources with edition or date.
- Law and regulations: only official government sources (for example `gov.pl`, `europa.eu`, `gov.uk`, `.gov`). Each jurisdiction file lists its allowed domains under "Official legal sources". Never cite news, blogs, law firms or vendors as a legal source.
- Write skills in plain, simple English: short sentences, one instruction per sentence.
