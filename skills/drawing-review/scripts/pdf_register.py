#!/usr/bin/env python3
"""PDF drawing set scan: sheet register, title block text, register comparison.

Standard library only, plus one optional text extractor:
  1. pypdf (pip install pypdf)      - preferred, gives text and page size
  2. pdftotext from Poppler          - text only, page size from pdfinfo if present
Without either, the script stops and says what to install. The agent can still read the PDFs
directly; this script is for bulk work over a folder.

Commands:
  scan     walk a folder, extract title block text, write a register
           --dir drawings [--recursive] [--rules rules.json] [--csv register.csv] [--json]
           [--pages 1] [--pattern "*.pdf"]
  titles   print the extracted text of the first page(s) of one file
           --file drawings/A-101.pdf [--pages 1]
  compare  compare two registers produced by scan
           --a register-revB.csv --b register-revC.csv [--json]

Field detection is project-specific, so nothing is guessed: the rules file gives a regular
expression per field and the first capture group is the value. A field with no match stays
empty and is reported in the note column. Fields are never filled from the file name.

rules.json:
{
  "sheet_no": "\\\\b([A-Z]{1,3}-[0-9]{3,4})\\\\b",
  "title":    "\\\\bTITLE[:.]?\\\\s*([^\\\\n]{3,60})",
  "rev":      "\\\\bRev[:.]?\\\\s*([A-Z0-9]{1,3})\\\\b",
  "status":   "\\\\bStatus[:.]?\\\\s*([A-Z0-9]{2})\\\\b",
  "date":     "\\\\b([0-9]{2}[./-][0-9]{2}[./-][0-9]{4})\\\\b",
  "scale":    "\\\\b1:[0-9]{1,4}\\\\b"
}

Scan columns: file, pages, page_size, sheet_no, title, rev, status, date, scale, note.
Exit codes: 0 ok, 2 bad input, 3 missing dependency.
"""

import argparse
import csv
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ISO_SIZES = [("A0", 841, 1189), ("A1", 594, 841), ("A2", 420, 594), ("A3", 297, 420),
             ("A4", 210, 297)]
FIELDS = ["sheet_no", "title", "rev", "status", "date", "scale"]
SCANNED_TEXT_THRESHOLD = 40  # characters on the first page below which the PDF looks scanned
PT_TO_MM = 25.4 / 72.0
COLUMNS = ["file", "pages", "page_size"] + FIELDS + ["note"]


class MissingDependency(Exception):
    pass


def extractor():
    """Return (name, text_function, size_function). size_function may return None."""
    try:
        from pypdf import PdfReader  # noqa: F401  (imported for the branch below)
    except ImportError:
        pass
    else:
        def text_of(path, pages):
            from pypdf import PdfReader
            reader = PdfReader(str(path))
            texts = []
            for page in reader.pages[:pages]:
                texts.append(page.extract_text() or "")
            return "\n".join(texts), len(reader.pages), _pypdf_size(reader)

        return "pypdf", text_of

    if shutil.which("pdftotext"):
        def text_of(path, pages):
            out = subprocess.run(["pdftotext", "-f", "1", "-l", str(pages), "-layout",
                                  str(path), "-"], capture_output=True, text=True)
            if out.returncode != 0:
                raise RuntimeError(out.stderr.strip() or "pdftotext failed")
            pages_count, size = _pdfinfo(path)
            return out.stdout, pages_count, size

        return "pdftotext", text_of

    raise MissingDependency(
        "no PDF text extractor found. Install pypdf (pip install pypdf) or Poppler's "
        "pdftotext, or let the agent read the PDFs directly instead of scanning a folder.")


def _pypdf_size(reader):
    try:
        box = reader.pages[0].mediabox
        width = float(box.width) * PT_TO_MM
        height = float(box.height) * PT_TO_MM
    except Exception:
        return None
    return size_name(width, height)


def _pdfinfo(path):
    count, size = None, None
    if shutil.which("pdfinfo"):
        out = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True)
        for line in out.stdout.splitlines():
            if line.lower().startswith("pages:"):
                count = int(line.split(":", 1)[1].strip())
            if line.lower().startswith("page size:"):
                parts = line.split(":", 1)[1].split()
                if len(parts) >= 3 and parts[-1].lower() == "pts":
                    size = size_name(float(parts[0]) * PT_TO_MM, float(parts[1]) * PT_TO_MM)
    return count, size


def size_name(width_mm, height_mm):
    short, long_ = sorted((width_mm, height_mm))
    for name, w, h in ISO_SIZES:
        if abs(short - w) <= 6 and abs(long_ - h) <= 6:
            return name
    return f"{short:.0f}x{long_:.0f} mm"


def load_rules(path):
    if not path:
        return {}
    with open(path, encoding="utf-8") as fh:
        rules = json.load(fh)
    for key in rules:
        if key not in FIELDS and key != "page_text_chars":
            raise ValueError(f"unknown rule '{key}'; allowed: {', '.join(FIELDS)}")
    return rules


def apply_rules(text, rules):
    values, missing = {}, []
    for field in FIELDS:
        pattern = rules.get(field)
        if not pattern:
            values[field] = ""
            continue
        match = re.search(pattern, text)
        values[field] = match.group(1) if match and match.groups() else (match.group(0) if match else "")
        if not values[field]:
            missing.append(field)
    return values, missing


def scan_file(path, rules, pages, extract):
    name, text_of = extract
    text, page_count, page_size = text_of(path, pages)
    if page_count is None:
        page_count = pages
    values, missing = apply_rules(text, rules)
    notes = []
    if rules and missing:
        notes.append("missing: " + ", ".join(missing))
    elif not rules:
        notes.append("no rules file: title block fields not extracted")
    if len(text.strip()) < SCANNED_TEXT_THRESHOLD:
        notes.append("no text found: scanned or text as curves, read visually")
    notes.append(f"extractor: {name}")
    row = {"file": path.name, "pages": page_count, "page_size": page_size or ""}
    row.update(values)
    row["note"] = "; ".join(notes[:2])
    return row, text


def iter_files(folder, recursive, pattern):
    base = Path(folder)
    if not base.is_dir():
        raise ValueError(f"{folder} is not a directory")
    files = sorted(base.rglob(pattern) if recursive else base.glob(pattern))
    return [f for f in files if f.is_file()]


def cmd_scan(args):
    rules = load_rules(args.rules)
    extract = extractor()
    rows = []
    for path in iter_files(args.dir, args.recursive, args.pattern):
        row, _text = scan_file(path, rules, args.pages, extract)
        rows.append(row)
    if args.json:
        print(json.dumps({"extractor": extract[0], "count": len(rows), "rows": rows},
                         ensure_ascii=False, indent=2))
    else:
        width = max([len(r["file"]) for r in rows] + [4])
        print(f"{'file':<{width}} {'sheet_no':<10} {'rev':<5} {'status':<7} {'date':<11} "
              f"{'size':<9} note")
        for row in rows:
            print(f"{row['file']:<{width}} {row['sheet_no'][:10]:<10} {row['rev'][:5]:<5} "
                  f"{row['status'][:7]:<7} {row['date'][:11]:<11} {row['page_size']:<9} "
                  f"{row['note']}")
        print(f"\n{len(rows)} file(s), extractor: {extract[0]}")
    if args.csv:
        with open(args.csv, "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=COLUMNS)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        print(f"wrote {args.csv}")
    return 0


def cmd_titles(args):
    _name, text_of = extractor()
    _row, text = scan_file(Path(args.file), {}, args.pages, (_name, text_of))
    print(text)


def read_register(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return {row["sheet_no"] or row["file"]: row for row in csv.DictReader(fh)}


def cmd_compare(args):
    old, new = read_register(args.a), read_register(args.b)
    added = [k for k in new if k not in old]
    removed = [k for k in old if k not in new]
    changed = []
    for key in old:
        if key not in new:
            continue
        before, after = old[key], new[key]
        diffs = [f for f in ("rev", "status", "title", "date") if before.get(f) != after.get(f)]
        if diffs:
            changed.append({"sheet_no": key,
                            "changes": {f: [before.get(f, ""), after.get(f, "")] for f in diffs},
                            "file": after.get("file", "")})
    payload = {"from": Path(args.a).name, "to": Path(args.b).name,
               "added": sorted(added), "removed": sorted(removed), "changed": changed}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    print(f"== Register comparison ==  {payload['from']} -> {payload['to']}")
    print(f"\nAdded ({len(added)}): " + (", ".join(sorted(added)) or "-"))
    print(f"Removed ({len(removed)}): " + (", ".join(sorted(removed)) or "-"))
    print(f"\nChanged ({len(changed)}):")
    for item in changed:
        detail = "; ".join(f"{f}: {v[0]!r} -> {v[1]!r}" for f, v in item["changes"].items())
        print(f"  {item['sheet_no']:<12} {detail}")
    print("\nNote: a revision change means something changed, not what changed. Open both "
          "sheets before reporting the content change.")


def build_parser():
    p = argparse.ArgumentParser(description="PDF drawing register helper.")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("scan")
    s.add_argument("--dir", required=True)
    s.add_argument("--pattern", default="*.pdf")
    s.add_argument("--recursive", action="store_true")
    s.add_argument("--rules")
    s.add_argument("--csv")
    s.add_argument("--json", action="store_true")
    s.add_argument("--pages", type=int, default=1)
    s.set_defaults(func=cmd_scan)

    s = sub.add_parser("titles")
    s.add_argument("--file", required=True)
    s.add_argument("--pages", type=int, default=1)
    s.set_defaults(func=cmd_titles)

    s = sub.add_parser("compare")
    s.add_argument("--a", required=True)
    s.add_argument("--b", required=True)
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_compare)
    return p


def main():
    args = build_parser().parse_args()
    try:
        return args.func(args) or 0
    except MissingDependency as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 3
    except (ValueError, OSError, RuntimeError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
