#!/usr/bin/env python3
"""Punch list register. Standard library only.

Holds the items with their location, trade, severity, owner, deadline and status, and the
history of every status change. It does NOT write the report: the wording is the agent's job.

Commands:
  init      create an empty register
            --file punch.json --project "Biurowiec Zabłocie B2"
  add       add an item
            --file punch.json --location "poz. 0, pom. 1.04" --trade sanitarne
            --element "izolacja" --description "..." [--severity B] [--photo "SV-007/4"]
            [--owner "Wykonawca / M. Lis"] [--due 2026-10-15] [--raised "B2-SV-007"] [--date 2026-10-12]
  status    change the status (claims of a fix, reopening)
            --file punch.json --id U-001 --status fixed --note "poprawiono 14.10.2026, zdjecie 22"
  verify    verify a fixed item (the verifier must not be the party who fixed it)
            --file punch.json --id U-001 --by "Inspektor / T. Wrona" [--note "..."] [--date 2026-10-16]
  list      show items, with filters
            --file punch.json [--open] [--overdue] [--trade sanitarne] [--severity B]
            [--room "1.04"] [--owner "Lis"] [--json]
  summary   counts by status, severity and trade, plus the overdue count
            --file punch.json [--json]
  export    write a CSV, working view or handover view
            --file punch.json --csv punch.csv [--view trade|room|flat]

Statuses: open, in progress, fixed, verified, closed, rejected.
Rules enforced here: closing requires a verified item; verifying requires a name different from
the owner; every change is written into the item history with its date and note.
"""

import argparse
import csv
import json
import sys
from datetime import date

STATUSES = ["open", "in progress", "fixed", "verified", "closed", "rejected"]
SEVERITIES = ["A", "B", "C", "D"]
COLUMNS = ["id", "location", "room", "trade", "element", "description", "severity", "photo",
           "owner", "due", "status", "raised", "verified_by", "verified_on", "note"]


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save(path, data):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def today(args):
    return date.fromisoformat(args.date) if getattr(args, "date", None) else date.today()


def next_id(items):
    used = 0
    for item in items:
        tail = str(item.get("id", "")).rsplit("-", 1)[-1]
        if tail.isdigit():
            used = max(used, int(tail))
    return f"U-{used + 1:03d}"


def find(data, item_id):
    for item in data.get("items", []):
        if item.get("id") == item_id:
            return item
    return None


def room_of(location):
    """Last 'pom. <room>' or trailing number in the location, for the handover view."""
    text = location or ""
    if "pom." in text:
        return text.split("pom.")[-1].strip().split(",")[0].strip()
    return text.split(",")[-1].strip()


def cmd_init(args):
    save(args.file, {"project": args.project, "items": []})
    print(f"created {args.file} for {args.project}")


def cmd_add(args):
    data = load(args.file)
    items = data.setdefault("items", [])
    item = {"id": next_id(items), "location": args.location, "room": room_of(args.location),
            "trade": args.trade, "element": args.element, "description": args.description,
            "severity": args.severity or "", "photo": args.photo or "",
            "owner": args.owner or "", "due": args.due or "", "status": "open",
            "raised": args.raised or "", "verified_by": "", "verified_on": "", "note": "",
            "history": [{"date": today(args).isoformat(), "status": "open",
                         "note": f"raised ({args.raised})" if args.raised else "raised"}]}
    items.append(item)
    save(args.file, data)
    print(f"added {item['id']}: {item['location']} / {item['trade']} / {args.description[:50]}")
    if not item["photo"]:
        print("Note: no photo reference. An item without a photo is the first one disputed at "
              "handover.")
    if not item["owner"]:
        print("Note: no owner. An unassigned item is a record, not an action.")
    if not item["due"]:
        print("Note: no deadline.")


def cmd_status(args):
    data = load(args.file)
    item = find(data, args.id)
    if item is None:
        print(f"ERROR: no item with id {args.id}", file=sys.stderr)
        return 2
    if args.status == "closed" and item["status"] != "verified":
        print(f"ERROR: {args.id} is '{item['status']}'. An item can only be closed after it is "
              "verified: closing on a claim is how defects reappear after handover.", file=sys.stderr)
        return 2
    if args.status == "closed" and not args.note:
        print("ERROR: closing needs a note naming the evidence (photo, test, measurement).",
              file=sys.stderr)
        return 2
    item["status"] = args.status
    if args.note:
        item["note"] = args.note
    item.setdefault("history", []).append(
        {"date": today(args).isoformat(), "status": args.status, "note": args.note or ""})
    save(args.file, data)
    print(f"{args.id} -> {args.status}")
    return 0


def cmd_verify(args):
    data = load(args.file)
    item = find(data, args.id)
    if item is None:
        print(f"ERROR: no item with id {args.id}", file=sys.stderr)
        return 2
    if item["status"] not in ("fixed",):
        print(f"ERROR: {args.id} is '{item['status']}'. Verify items that are fixed.", file=sys.stderr)
        return 2
    owner_name = (item.get("owner") or "").split("/")[-1].strip().lower()
    if owner_name and owner_name in args.by.lower():
        print(f"ERROR: the verifier is the party who fixed {args.id}. Verification must be done "
              "by someone else.", file=sys.stderr)
        return 2
    item["status"] = "verified"
    item["verified_by"] = args.by
    item["verified_on"] = today(args).isoformat()
    if args.note:
        item["note"] = args.note
    item.setdefault("history", []).append(
        {"date": today(args).isoformat(), "status": "verified", "note": f"by {args.by}"
         + (f": {args.note}" if args.note else "")})
    save(args.file, data)
    print(f"{args.id} verified by {args.by}. Close it with a note naming the evidence when the "
          "client or the inspector accepts it.")
    return 0


def cmd_list(args):
    data = load(args.file)
    day = today(args)
    rows = []
    for item in data.get("items", []):
        due = item.get("due") or ""
        days_left = (date.fromisoformat(due) - day).days if due else None
        overdue = bool(due) and days_left < 0 and item["status"] in ("open", "in progress")
        rows.append(dict(item, days_left=days_left, overdue=overdue))
    if args.open:
        rows = [r for r in rows if r["status"] in ("open", "in progress", "fixed")]
    if args.overdue:
        rows = [r for r in rows if r["overdue"]]
    if args.trade:
        rows = [r for r in rows if args.trade.lower() in r["trade"].lower()]
    if args.severity:
        rows = [r for r in rows if r["severity"] == args.severity]
    if args.room:
        rows = [r for r in rows if args.room.lower() in r["room"].lower()]
    if args.owner:
        rows = [r for r in rows if args.owner.lower() in (r.get("owner") or "").lower()]
    if args.json:
        print(json.dumps({"project": data.get("project", ""), "as_of": day.isoformat(),
                          "items": rows}, ensure_ascii=False, indent=2))
        return
    print(f"{data.get('project','')}  punch list  as of {day.isoformat()}  ({len(rows)} item(s))")
    print(f"{'ID':<7} {'Room':<9} {'Trade':<12} {'Sev':<4} {'Owner':<22} {'Due':<11} {'Days':>5}  Status")
    for row in rows:
        days = "" if row["days_left"] is None else str(row["days_left"])
        flag = "!" if row["overdue"] else " "
        print(f"{row['id']:<7} {row['room'][:8]:<9} {row['trade'][:11]:<12} "
              f"{row['severity']:<4} {(row.get('owner') or '-')[:21]:<22} {row.get('due',''):<11} "
              f"{days:>5}{flag} {row['status']}")
    overdue = [r for r in rows if r["overdue"]]
    if overdue:
        print(f"\nOVERDUE: {len(overdue)} item(s). Chase by trade and give the owner the date.")
    without_photo = [r for r in rows if not r.get("photo")]
    if without_photo:
        print(f"Without a photo: {len(without_photo)} item(s): "
              + ", ".join(r["id"] for r in without_photo[:12]))


def cmd_summary(args):
    data = load(args.file)
    day = today(args)
    by_status, by_severity, by_trade, overdue = {}, {}, {}, 0
    for item in data.get("items", []):
        by_status[item["status"]] = by_status.get(item["status"], 0) + 1
        by_severity[item["severity"] or "-"] = by_severity.get(item["severity"] or "-", 0) + 1
        by_trade[item["trade"]] = by_trade.get(item["trade"], 0) + 1
        if item.get("due") and item["status"] in ("open", "in progress"):
            if (date.fromisoformat(item["due"]) - day).days < 0:
                overdue += 1
    payload = {"project": data.get("project", ""), "as_of": day.isoformat(),
               "total": len(data.get("items", [])), "by_status": by_status,
               "by_severity": by_severity, "by_trade": by_trade, "overdue": overdue,
               "no_photo": sum(1 for i in data.get("items", []) if not i.get("photo")),
               "no_owner": sum(1 for i in data.get("items", []) if not i.get("owner"))}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    print(f"{payload['project']}  punch list summary  as of {payload['as_of']}")
    print(f"total {payload['total']}   overdue {payload['overdue']}   "
          f"without photo {payload['no_photo']}   without owner {payload['no_owner']}")
    print("\nby status:   " + ", ".join(f"{k} {v}" for k, v in sorted(by_status.items())))
    print("by severity: " + ", ".join(f"{k} {v}" for k, v in sorted(by_severity.items())))
    print("by trade:")
    for trade, count in sorted(by_trade.items(), key=lambda kv: -kv[1]):
        print(f"  {trade:<28} {count}")
    print("\nItems still open at handover are normal. Items closed on a claim are not: "
          "verify before closing.")


def cmd_export(args):
    data = load(args.file)
    rows = data.get("items", [])
    view = args.view or "flat"
    if view == "room":
        rows = sorted(rows, key=lambda r: (r.get("room", ""), r.get("trade", ""), r.get("id", "")))
    elif view == "trade":
        rows = sorted(rows, key=lambda r: (r.get("trade", ""), r.get("room", ""), r.get("id", "")))
    with open(args.csv, "w", encoding="utf-8", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    print(f"wrote {args.csv}: {len(rows)} item(s), view '{view}'")
    if view == "room":
        print("Handover view: grouped by room. State the walkthrough date, the areas covered and "
              "the areas not inspected, and mark the open items.")


def build_parser():
    p = argparse.ArgumentParser(description="Punch list register.")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add(name, func):
        s = sub.add_parser(name)
        s.set_defaults(func=func, date=None)
        s.add_argument("--file", required=True)
        s.add_argument("--date", help="override today, ISO format")
        s.add_argument("--json", action="store_true")
        return s

    s = add("init", cmd_init)
    s.add_argument("--project", required=True)

    s = add("add", cmd_add)
    s.add_argument("--location", required=True)
    s.add_argument("--trade", required=True)
    s.add_argument("--element", required=True)
    s.add_argument("--description", required=True)
    s.add_argument("--severity", choices=SEVERITIES)
    s.add_argument("--photo", default="")
    s.add_argument("--owner", default="")
    s.add_argument("--due", default="")
    s.add_argument("--raised", default="")

    s = add("status", cmd_status)
    s.add_argument("--id", required=True)
    s.add_argument("--status", choices=STATUSES, required=True)
    s.add_argument("--note", default="")

    s = add("verify", cmd_verify)
    s.add_argument("--id", required=True)
    s.add_argument("--by", required=True)
    s.add_argument("--note", default="")

    s = add("list", cmd_list)
    s.add_argument("--open", action="store_true")
    s.add_argument("--overdue", action="store_true")
    s.add_argument("--trade")
    s.add_argument("--severity", choices=SEVERITIES)
    s.add_argument("--room")
    s.add_argument("--owner")

    add("summary", cmd_summary)

    s = add("export", cmd_export)
    s.add_argument("--csv", required=True)
    s.add_argument("--view", choices=["flat", "trade", "room"], default="flat")
    return p


def main():
    args = build_parser().parse_args()
    try:
        result = args.func(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return result or 0


if __name__ == "__main__":
    sys.exit(main())
