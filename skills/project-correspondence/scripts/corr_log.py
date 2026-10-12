#!/usr/bin/env python3
"""Correspondence register helper. Standard library only.

Holds numbers, dates and deadlines for letters, RFIs, transmittals, notices, change requests,
non-conformance reports and coordination issue reports. It does NOT write the documents.

Commands:
  init     create an empty register
           --file register.json --project "Biurowiec B2" --prefix B2
  next     next number for a type, without adding it
           --file register.json --type RFI
  add      add an entry and print its number
           --file register.json --type RFI --to "Zamawiający" --subject "Brak rzutu"
           [--days 7] [--ref "B2-LET-012"] [--note "..."] [--date 2026-10-02]
  list     show the register
           --file register.json [--overdue] [--status open] [--json]
  close    change the status of an entry
           --file register.json --id B2-RFI-005 --status answered [--note "..."]

Types: LET letter, RFI technical query, TRA transmittal, NOT notice, CHG change request,
NCR non-conformance, COORD coordination issue, MIN minutes.

Dates are ISO (YYYY-MM-DD). Use --date to reproduce an example; without it the script uses
today. The type codes map to the register on purpose: the number is what makes a document
traceable, so the script never renumbers and never reuses a number.
"""

import argparse
import json
import sys
from datetime import date, timedelta

TYPES = ["LET", "RFI", "TRA", "NOT", "CHG", "NCR", "COORD", "MIN"]
STATUSES = ["open", "answered", "closed", "cancelled"]


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save(path, data):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def today(args):
    return date.fromisoformat(args.date) if getattr(args, "date", None) else date.today()


def next_number(data, doc_type):
    prefix = data.get("prefix", "DOC")
    used = 0
    for entry in data.get("entries", []):
        if entry.get("type") != doc_type:
            continue
        tail = entry.get("id", "").rsplit("-", 1)[-1]
        if tail.isdigit():
            used = max(used, int(tail))
    return f"{prefix}-{doc_type}-{used + 1:03d}"


def cmd_init(args):
    if args.file:
        data = {"project": args.project, "currency": "", "prefix": args.prefix, "entries": []}
        save(args.file, data)
        print(f"created {args.file}: project {args.project}, prefix {args.prefix}")


def cmd_next(args):
    data = load(args.file)
    print(next_number(data, args.type))


def cmd_add(args):
    data = load(args.file)
    day = today(args)
    due = day + timedelta(days=args.days) if args.days else None
    entry = {"id": next_number(data, args.type), "type": args.type, "date": day.isoformat(),
             "to": args.to, "subject": args.subject,
             "due": due.isoformat() if due else "", "ref": args.ref or "",
             "status": "open", "note": args.note or ""}
    data.setdefault("entries", []).append(entry)
    save(args.file, data)
    print(f"added {entry['id']}  to {entry['to']}  due {entry['due'] or 'not set'}")


def cmd_list(args):
    data = load(args.file)
    day = today(args)
    rows = []
    for entry in data.get("entries", []):
        due = entry.get("due") or ""
        days_left = None
        if due:
            days_left = (date.fromisoformat(due) - day).days
        overdue = bool(due) and days_left < 0 and entry.get("status") == "open"
        row = dict(entry)
        row["days_left"] = days_left
        row["overdue"] = overdue
        rows.append(row)
    if args.status:
        rows = [r for r in rows if r["status"] == args.status]
    if args.overdue:
        rows = [r for r in rows if r["overdue"]]
    if args.json:
        print(json.dumps({"project": data.get("project", ""), "as_of": day.isoformat(),
                          "entries": rows}, ensure_ascii=False, indent=2))
        return
    print(f"{data.get('project','')}  register  as of {day.isoformat()}  "
          f"({len(rows)} entr{'y' if len(rows)==1 else 'ies'})")
    print(f"{'ID':<16} {'Date':<11} {'To':<18} {'Due':<11} {'Days':>5}  {'Status':<10} Subject")
    for row in rows:
        days = "" if row["days_left"] is None else str(row["days_left"])
        flag = "!" if row["overdue"] else " "
        print(f"{row['id']:<16} {row['date']:<11} {row['to'][:17]:<18} {row.get('due',''):<11} "
              f"{days:>5}{flag} {row['status']:<10} {row['subject'][:40]}")
    overdue = [r for r in rows if r["overdue"]]
    if overdue:
        print(f"\nOVERDUE: {len(overdue)} item(s). Send a reminder quoting the number and date, "
              "and state the consequence of further delay.")


def cmd_close(args):
    data = load(args.file)
    for entry in data.get("entries", []):
        if entry.get("id") == args.id:
            entry["status"] = args.status
            if args.note:
                entry["note"] = args.note
            save(args.file, data)
            print(f"{args.id} -> {args.status}")
            return
    print(f"ERROR: no entry with id {args.id}", file=sys.stderr)
    raise SystemExit(2)


def build_parser():
    p = argparse.ArgumentParser(description="Correspondence register helper.")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add(name, func):
        s = sub.add_parser(name)
        s.set_defaults(func=func, date=None)
        s.add_argument("--file", required=True)
        s.add_argument("--date", help="override today, ISO format, for examples and tests")
        return s

    s = add("init", cmd_init)
    s.add_argument("--project", required=True)
    s.add_argument("--prefix", required=True)

    s = add("next", cmd_next)
    s.add_argument("--type", choices=TYPES, required=True)

    s = add("add", cmd_add)
    s.add_argument("--type", choices=TYPES, required=True)
    s.add_argument("--to", required=True)
    s.add_argument("--subject", required=True)
    s.add_argument("--days", type=int, default=0)
    s.add_argument("--ref", default="")
    s.add_argument("--note", default="")

    s = add("list", cmd_list)
    s.add_argument("--overdue", action="store_true")
    s.add_argument("--status", choices=STATUSES)
    s.add_argument("--json", action="store_true")

    s = add("close", cmd_close)
    s.add_argument("--id", required=True)
    s.add_argument("--status", choices=STATUSES, required=True)
    s.add_argument("--note", default="")
    return p


def main():
    args = build_parser().parse_args()
    try:
        args.func(args)
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
