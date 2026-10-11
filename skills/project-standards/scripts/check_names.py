#!/usr/bin/env python3
"""Check names (files, layers, sheets, objects) against a naming rule set.

Usage:
  python check_names.py RULES.json --dir PATH [--recursive] [--ext .pdf .dwg]
  python check_names.py RULES.json --list names.txt
  python check_names.py RULES.json --list -          (names from stdin)
Options:
  --format md|json|csv   output format (default md)
  --only-errors          print failing names only

Rules file (JSON):
{
  "name": "ISO 19650 file naming",
  "separator": "-",
  "case": "upper",                      # upper | lower | any
  "strip_extension": true,
  "allowed_extensions": [".pdf", ".dwg"],   # optional
  "fields": [
    {"name": "project", "pattern": "^[A-Z0-9]{2,6}$"},
    {"name": "type", "allowed": ["DR", "M3"], "descriptions": {"DR": "drawing"}},
    {"name": "suffix", "pattern": "^[A-Z]\\d{2}$", "optional": true}
  ]
}
Optional fields may only come after all required fields.

Exit code: 0 all names pass, 1 at least one fails, 2 usage error.
Standard library only.
"""

import argparse
import csv
import json
import re
import sys
from pathlib import Path


def load_rules(path):
    rules = json.loads(Path(path).read_text(encoding="utf-8"))
    fields = rules.get("fields")
    if not fields:
        raise ValueError("rules file has no 'fields'")
    seen_optional = False
    for field in fields:
        if "pattern" not in field and "allowed" not in field:
            raise ValueError(f"field '{field.get('name')}' needs 'pattern' or 'allowed'")
        if field.get("optional"):
            seen_optional = True
        elif seen_optional:
            raise ValueError("required fields must come before optional fields")
        if "pattern" in field:
            field["_re"] = re.compile(field["pattern"])
    rules.setdefault("separator", "-")
    rules.setdefault("case", "any")
    rules.setdefault("strip_extension", True)
    return rules


def split_name(name, rules):
    ext = ""
    if rules["strip_extension"] and "." in name:
        stem, ext = name.rsplit(".", 1)
        ext = "." + ext
    else:
        stem = name
    return stem, ext


def field_ok(field, value):
    if "allowed" in field and value not in field["allowed"]:
        return False
    if "_re" in field and not field["_re"].search(value):
        return False
    return True


def check(name, rules):
    """Return list of error strings for one name."""
    errors = []
    stem, ext = split_name(name, rules)
    allowed_ext = rules.get("allowed_extensions")
    if allowed_ext and ext.lower() not in [e.lower() for e in allowed_ext]:
        errors.append(f"extension '{ext or '(none)'}' not allowed")
    # Report a case error once, then check fields on the case-corrected name,
    # so one wrong case does not show up again as an error in every field.
    if rules["case"] == "upper" and stem != stem.upper():
        errors.append("must be upper case")
        stem = stem.upper()
    elif rules["case"] == "lower" and stem != stem.lower():
        errors.append("must be lower case")
        stem = stem.lower()
    if " " in stem:
        errors.append("contains spaces")
    fields = rules["fields"]
    sep = rules["separator"]
    parts = stem.split(sep)
    required = sum(1 for f in fields if not f.get("optional"))
    if not required <= len(parts) <= len(fields):
        expected = f"{required}-{len(fields)}" if required != len(fields) else f"{required}"
        message = f"has {len(parts)} fields, expected {expected}"
        wrong_seps = [s for s in "-_. " if s != sep and s in stem]
        if wrong_seps:
            message += f"; separator must be '{sep}', found '{wrong_seps[0]}'"
        errors.append(message)
        return errors
    for field, value in zip(fields, parts):
        if not field_ok(field, value):
            hint = ""
            if "allowed" in field:
                shown = ", ".join(field["allowed"][:12])
                more = "..." if len(field["allowed"]) > 12 else ""
                hint = f" (allowed: {shown}{more})"
            elif "pattern" in field:
                hint = f" (pattern {field['pattern']})"
            errors.append(f"field '{field['name']}' = '{value}' invalid{hint}")
    return errors


def suggest(name, rules):
    """Try simple mechanical fixes. Return fixed name only if it then passes."""
    stem, ext = split_name(name, rules)
    sep = rules["separator"]
    fixed = re.sub(r"[ _\-.]+", sep, stem.strip()) if sep in "-_" else stem.strip()
    if rules["case"] == "upper":
        fixed = fixed.upper()
    elif rules["case"] == "lower":
        fixed = fixed.lower()
    candidate = fixed + ext
    if candidate != name and not check(candidate, rules):
        return candidate
    return ""


def collect_names(args):
    if args.dir:
        root = Path(args.dir)
        if not root.is_dir():
            raise ValueError(f"not a directory: {root}")
        paths = root.rglob("*") if args.recursive else root.iterdir()
        exts = [e.lower() for e in args.ext] if args.ext else None
        names = []
        for p in sorted(paths):
            if p.is_file() and (exts is None or p.suffix.lower() in exts):
                names.append(p.name)
        return names
    source = sys.stdin if args.list == "-" else open(args.list, encoding="utf-8")
    with source:
        return [line.strip() for line in source if line.strip()]


def main():
    parser = argparse.ArgumentParser(description="Check names against naming rules.")
    parser.add_argument("rules")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--dir")
    group.add_argument("--list")
    parser.add_argument("--recursive", action="store_true")
    parser.add_argument("--ext", nargs="*")
    parser.add_argument("--format", choices=["md", "json", "csv"], default="md")
    parser.add_argument("--only-errors", action="store_true")
    args = parser.parse_args()

    try:
        rules = load_rules(args.rules)
        names = collect_names(args)
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    results = []
    for name in names:
        errors = check(name, rules)
        results.append({
            "name": name,
            "ok": not errors,
            "errors": errors,
            "suggestion": suggest(name, rules) if errors else "",
        })
    shown = [r for r in results if not (args.only_errors and r["ok"])]
    failed = sum(1 for r in results if not r["ok"])

    if args.format == "json":
        print(json.dumps({"rules": rules.get("name", ""), "checked": len(results),
                          "failed": failed, "results": shown}, ensure_ascii=False, indent=2))
    elif args.format == "csv":
        writer = csv.writer(sys.stdout)
        writer.writerow(["name", "ok", "errors", "suggestion"])
        for r in shown:
            writer.writerow([r["name"], r["ok"], "; ".join(r["errors"]), r["suggestion"]])
    else:
        print(f"Rules: {rules.get('name', args.rules)}")
        print(f"Checked: {len(results)}, failed: {failed}\n")
        print("| Name | Result | Problems | Suggestion |")
        print("|---|---|---|---|")
        for r in shown:
            status = "OK" if r["ok"] else "FAIL"
            print(f"| {r['name']} | {status} | {'; '.join(r['errors'])} | {r['suggestion']} |")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
