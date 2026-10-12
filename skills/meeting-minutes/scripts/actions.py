#!/usr/bin/env python3
"""Action register and decision log for meeting minutes. Standard library only.

Holds the actions with owner, deadline and status, and the decisions with the date and the
person who took them. It does NOT write the minutes: the wording is the agent's job.

Commands:
  init      create an empty register
            --file actions.json --project "Biurowiec B2"
  add       add an action
            --file actions.json --action "Przekazać rzut" --owner "Zamawiający / J. Kowalski"
            --due 2026-10-09 [--item 3.4] [--raised 2026-011] [--source B2-RFI-001] [--date 2026-10-12]
  decide    add a decision
            --file actions.json --decision "Zmiana trasy pionu W2" --by "Projektant / A. Nowak"
            [--affects design|scope|cost|programme|quality|contract] [--reference "rys. S-201 rew. C"]
            [--meeting 2026-011] [--date 2026-10-12]
  close     change the status of an action
            --file actions.json --id A-004 --status done [--note "rzut przekazany 09.10.2026"]
  carry     move every open action to a later meeting (the minutes follow-up)
            --file actions.json --to-minutes 2026-012
  list      show actions and decisions
            --file actions.json [--open] [--overdue] [--owner "Kowalski"] [--json]
  summary   counts per owner and per status (for the meeting itself)
            --file actions.json [--json]

Statuses: open, done, carried, cancelled. Dates are ISO (YYYY-MM-DD); --date overrides today.
An action closed without a note is reported as a warning: closure without evidence is what an
audit picks up first.
"""

import argparse
import json
import sys
from datetime import date, timedelta

STATUSES = ["open", "done", "carried", "cancelled"]
AFFECTS = ["design", "scope", "cost", "programme", "quality", "contract"]


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def save(path, data):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)
        fh.write("\n")


def today(args):
    return date.fromisoformat(args.date) if getattr(args, "date", None) else date.today()


def next_id(entries, prefix, key):
    used = 0
    for entry in entries:
        tail = str(entry.get(key, "")).rsplit("-", 1)[-1]
        if tail.isdigit():
            used = max(used, int(tail))
    return f"{prefix}-{used + 1:03d}"


def cmd_init(args):
    save(args.file, {"project": args.project, "entries": [], "decisions": []})
    print(f"created {args.file} for {args.project}")


def cmd_add(args):
    data = load(args.file)
    entries = data.setdefault("entries", [])
    entry = {"id": next_id(entries, "A", "id"), "item": args.item or "", "action": args.action,
             "owner": args.owner, "due": args.due or "", "status": "open",
             "raised": args.raised or "", "note": "", "source": args.source or "",
             "carried_to": ""}
    entries.append(entry)
    save(args.file, data)
    print(f"added {entry['id']}: {entry['action'][:60]}  owner {entry['owner']}  "
          f"due {entry['due'] or 'NOT SET'}")


def cmd_decide(args):
    data = load(args.file)
    decisions = data.setdefault("decisions", [])
    entry = {"id": next_id(decisions, "D", "id"), "date": today(args).isoformat(),
             "meeting": args.meeting or "", "decision": args.decision, "by": args.by,
             "affects": args.affects or "", "reference": args.reference or ""}
    decisions.append(entry)
    save(args.file, data)
    print(f"added {entry['id']}: {entry['decision'][:60]}  by {entry['by']}")
    if entry["affects"] in ("scope", "cost", "programme", "contract"):
        print("Note: this decision changes " + entry["affects"] + ". Minutes alone are not an "
              "instruction or a notice: raise it in project-correspondence.")


def cmd_close(args):
    data = load(args.file)
    for entry in data.get("entries", []):
        if entry.get("id") == args.id:
            entry["status"] = args.status
            if args.note:
                entry["note"] = args.note
            save(args.file, data)
            print(f"{args.id} -> {args.status}")
            if args.status == "done" and not entry.get("note"):
                print("WARNING: closed with no evidence note. An action closed without evidence "
                      "is what an audit picks up first.")
            return
    print(f"ERROR: no action with id {args.id}", file=sys.stderr)
    raise SystemExit(2)


def cmd_carry(args):
    data = load(args.file)
    moved = 0
    for entry in data.get("entries", []):
        if entry.get("status") == "open":
            entry["status"] = "carried"
            entry["carried_to"] = args.to_minutes
            moved += 1
    save(args.file, data)
    print(f"carried {moved} open action(s) to minutes {args.to_minutes}")
    print("In the minutes, list each one in 'matters arising' with its new deadline: an action "
          "that disappears silently is the most common failure in project records.")


def cmd_list(args):
    data = load(args.file)
    day = today(args)
    rows = []
    for entry in data.get("entries", []):
        due = entry.get("due") or ""
        days_left = (date.fromisoformat(due) - day).days if due else None
        overdue = bool(due) and days_left < 0 and entry["status"] == "open"
        row = dict(entry, days_left=days_left, overdue=overdue)
        rows.append(row)
    if args.open:
        rows = [r for r in rows if r["status"] == "open"]
    if args.overdue:
        rows = [r for r in rows if r["overdue"]]
    if args.owner:
        rows = [r for r in rows if args.owner.lower() in r["owner"].lower()]
    if args.json:
        print(json.dumps({"project": data.get("project", ""), "as_of": day.isoformat(),
                          "entries": rows, "decisions": data.get("decisions", [])},
                         ensure_ascii=False, indent=2))
        return
    print(f"{data.get('project','')}  actions  as of {day.isoformat()}  ({len(rows)} row(s))")
    print(f"{'ID':<7} {'Item':<6} {'Owner':<26} {'Due':<11} {'Days':>5}  {'Status':<10} Action")
    for row in rows:
        days = "" if row["days_left"] is None else str(row["days_left"])
        flag = "!" if row["overdue"] else " "
        print(f"{row['id']:<7} {str(row['item'])[:5]:<6} {row['owner'][:25]:<26} "
              f"{row['due']:<11} {days:>5}{flag} {row['status']:<10} {row['action'][:44]}")
    overdue = [r for r in rows if r["overdue"]]
    if overdue:
        print(f"\nOVERDUE: {len(overdue)} action(s). Put them in 'matters arising' with the new "
              "deadline and the reason for the slip.")
    if data.get("decisions"):
        print(f"\nDecisions recorded: {len(data['decisions'])}")


def cmd_summary(args):
    data = load(args.file)
    day = today(args)
    per_owner, per_status = {}, {}
    overdue = 0
    for entry in data.get("entries", []):
        per_owner[entry["owner"]] = per_owner.get(entry["owner"], 0) + 1
        per_status[entry["status"]] = per_status.get(entry["status"], 0) + 1
        if entry.get("due") and entry["status"] == "open":
            if (date.fromisoformat(entry["due"]) - day).days < 0:
                overdue += 1
    payload = {"project": data.get("project", ""), "as_of": day.isoformat(),
               "total": sum(per_status.values()), "per_status": per_status,
               "per_owner": per_owner, "overdue": overdue,
               "decisions": len(data.get("decisions", []))}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    print(f"{payload['project']}  as of {payload['as_of']}")
    print(f"actions: {payload['total']}   " +
          ", ".join(f"{k} {v}" for k, v in sorted(payload["per_status"].items())) +
          f"   overdue {payload['overdue']}")
    print(f"decisions recorded: {payload['decisions']}")
    print("\nby owner:")
    for owner, count in sorted(per_owner.items(), key=lambda kv: -kv[1]):
        print(f"  {owner:<34} {count}")


def build_parser():
    p = argparse.ArgumentParser(description="Action register and decision log for minutes.")
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
    s.add_argument("--action", required=True)
    s.add_argument("--owner", required=True)
    s.add_argument("--due", default="")
    s.add_argument("--item", default="")
    s.add_argument("--raised", default="")
    s.add_argument("--source", default="")

    s = add("decide", cmd_decide)
    s.add_argument("--decision", required=True)
    s.add_argument("--by", required=True)
    s.add_argument("--affects", choices=AFFECTS)
    s.add_argument("--reference", default="")
    s.add_argument("--meeting", default="")

    s = add("close", cmd_close)
    s.add_argument("--id", required=True)
    s.add_argument("--status", choices=STATUSES, required=True)
    s.add_argument("--note", default="")

    s = add("carry", cmd_carry)
    s.add_argument("--to-minutes", required=True)

    s = add("list", cmd_list)
    s.add_argument("--open", action="store_true")
    s.add_argument("--overdue", action="store_true")
    s.add_argument("--owner")

    add("summary", cmd_summary)
    return p


def main():
    args = build_parser().parse_args()
    try:
        args.func(args)
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
