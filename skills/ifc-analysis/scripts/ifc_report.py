#!/usr/bin/env python3
"""IFC report: counts, quantities, property sets, requirement checks, schedule, comparison, IDS.

Requires ifcopenshell (pip install ifcopenshell, or the build from IfcOpenShell). Without it the
script stops with an install message and exit code 3: there is no way to read IFC without a
library.

Reads only. It never edits, repairs or re-exports the model; output goes to stdout or to a new
file you name with --csv.

Commands:
  summary     schema, units, storeys, element counts by type and by storey
              --file model.ifc [--json]
  quantities  quantities from IfcElementQuantity, per element
              --file model.ifc --type IfcWall [--storey "Level 1"] [--csv q.csv] [--json]
  psets       property sets for one type, optional single set
              --file model.ifc --type IfcPump [--pset Pset_FlowMoverCommon] [--json]
  missing     check a requirement list: psets and properties that must exist and be non-empty
              --file model.ifc --require requirements.json [--csv missing.csv]
  schedule    one row per element with selected properties
              --file model.ifc --type IfcAirTerminal --props Name,Tag,FireRating [--csv s.csv]
  compare     two issues by GUID: added, removed, changed
              --old revB.ifc --new revC.ifc [--json]
  ids         run an IDS file (needs ifctester)
              --file model.ifc --spec spec.ids

requirements.json:
{
  "IfcPump":            {"psets": ["Pset_FlowMoverCommon"],
                         "properties": ["Pset_FlowMoverCommon.RatedPower"]},
  "IfcAirTerminal":     {"psets": ["Pset_AirTerminalCommon"],
                         "properties": ["Pset_AirTerminalCommon.NominalAirFlowRate"]}
}

Every report states the schema, the units and the tool version. Quantities always carry the
quantity set and quantity name they came from.
"""

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


class DependencyError(Exception):
    pass


def ifcopenshell_module():
    try:
        import ifcopenshell
    except ImportError:
        raise DependencyError("ifcopenshell is not installed. Install it as its own "
                              "documentation describes (pip install ifcopenshell, or the "
                              "IfcOpenShell build), then run this command again.")
    return ifcopenshell


def open_model(path):
    ifcopenshell = ifcopenshell_module()
    if not str(path).lower().endswith((".ifc", ".ifczip")):
        raise ValueError("give an .ifc file")
    return ifcopenshell, ifcopenshell.open(str(path))


def version(ifcopenshell):
    return getattr(ifcopenshell, "__version__", "unknown")


def unwrap(value):
    """Readable value from an IFC attribute wrapper or a plain value."""
    if value is None:
        return None
    inner = getattr(value, "wrappedValue", None)
    if inner is not None:
        return inner
    return value


def units_of(model):
    out = {}
    projects = model.by_type("IfcProject")
    if not projects or not projects[0].UnitsInContext:
        return out
    for unit in projects[0].UnitsInContext.Units:
        kind = getattr(unit, "UnitType", None)
        if not kind:
            continue
        name = getattr(unit, "Name", None)
        prefix = getattr(unit, "Prefix", None)
        if name:
            label = f"{prefix + ' ' if prefix else ''}{name}"
        else:
            label = getattr(unit, "Name", None) or type(unit).__name__
        out[kind] = label
    return out


def storeys_of(model):
    return [{"name": s.Name or "(no name)", "guid": s.GlobalId,
             "elevation": unwrap(getattr(s, "Elevation", None))}
            for s in model.by_type("IfcBuildingStorey")]


def element_types(model, min_count=1, limit=40):
    counts = Counter()
    for element in model.by_type("IfcProduct"):
        counts[element.is_a()] += 1
    return [(name, count) for name, count in counts.most_common(limit) if count >= min_count]


def storey_of(element):
    for rel in getattr(element, "ContainedInStructure", []) or []:
        structure = rel.RelatingStructure
        if structure and structure.is_a("IfcBuildingStorey"):
            return structure.Name or "(no name)"
    return "(not assigned)"


def element_label(element):
    return (getattr(element, "Name", None) or getattr(element, "ObjectType", None)
            or element.is_a())


def quantity_rows(element):
    rows = []
    for rel in getattr(element, "IsDefinedBy", []) or []:
        definition = getattr(rel, "RelatingPropertyDefinition", None)
        if definition is None or not definition.is_a("IfcElementQuantity"):
            continue
        for quantity in definition.Quantities:
            value = None
            for attribute in ("LengthValue", "AreaValue", "VolumeValue", "CountValue",
                              "WeightValue", "TimeValue"):
                if hasattr(quantity, attribute):
                    value = unwrap(getattr(quantity, attribute))
                    break
            rows.append({"set": definition.Name or "(no name)", "quantity": quantity.Name,
                         "value": value})
    return rows


def property_rows(element):
    rows = []
    for rel in getattr(element, "IsDefinedBy", []) or []:
        definition = getattr(rel, "RelatingPropertyDefinition", None)
        if definition is None or not definition.is_a("IfcPropertySet"):
            continue
        for prop in definition.HasProperties:
            value = None
            if hasattr(prop, "NominalValue"):
                value = unwrap(prop.NominalValue)
            elif hasattr(prop, "EnumerationValues") and prop.EnumerationValues:
                value = ",".join(str(unwrap(v)) for v in prop.EnumerationValues)
            rows.append({"set": definition.Name or "(no name)", "property": prop.Name,
                         "value": value})
    return rows


def types_of_element(element):
    names = []
    for rel in getattr(element, "IsTypedBy", []) or []:
        type_object = getattr(rel, "RelatingType", None)
        if type_object is not None:
            names.append(getattr(type_object, "Name", None) or type_object.is_a())
    return names


def select(model, type_name, storey=None):
    elements = [e for e in model.by_type(type_name) if not e.is_a().endswith("Type")]
    if storey:
        elements = [e for e in elements if storey_of(e) == storey]
    return elements


def cmd_summary(args):
    ifcopenshell, model = open_model(args.file)
    counts = element_types(model)
    by_storey = defaultdict(Counter)
    for element in model.by_type("IfcProduct"):
        by_storey[storey_of(element)][element.is_a()] += 1
    payload = {"file": Path(args.file).name, "tool": f"ifcopenshell {version(ifcopenshell)}",
               "schema": model.schema, "units": units_of(model),
               "storeys": storeys_of(model), "element_counts": counts,
               "by_storey": {k: dict(v.most_common(10)) for k, v in by_storey.items()},
               "projects": [p.Name for p in model.by_type("IfcProject")],
               "spaces": len(model.by_type("IfcSpace")),
               "products": len(model.by_type("IfcProduct"))}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    print(f"== IFC summary ==  {payload['file']}   {payload['tool']}")
    print(f"schema: {payload['schema']}   projects: {payload['projects']}")
    print("units: " + (", ".join(f"{k}={v}" for k, v in payload["units"].items())
                       or "NOT DECLARED - every quantity below is suspect"))
    print(f"products: {payload['products']}   spaces: {payload['spaces']}")
    print("\nstoreys:")
    for storey in payload["storeys"]:
        print(f"  {storey['name']:<28} elevation {storey['elevation']}")
    if not payload["storeys"]:
        print("  none: the model has no IfcBuildingStorey, counts by level are impossible")
    print("\nelement counts by type (top 20):")
    for name, count in counts[:20]:
        print(f"  {name:<40} {count:>6}")
    print("\nelements by storey (top 10 types each):")
    for storey, types in payload["by_storey"].items():
        print(f"  {storey}: " + ", ".join(f"{k} {v}" for k, v in types.items()))
    print("\nCounts are occurrences, not type objects. State the filter in the report.")


def cmd_quantities(args):
    _ifcopenshell, model = open_model(args.file)
    elements = select(model, args.type, args.storey)
    rows = []
    for element in elements:
        for row in quantity_rows(element):
            rows.append({"guid": element.GlobalId, "name": element_label(element),
                         "storey": storey_of(element), "set": row["set"],
                         "quantity": row["quantity"], "value": row["value"]})
    missing = [e for e in elements if not quantity_rows(e)]
    if args.csv:
        with open(args.csv, "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=["guid", "name", "storey", "set", "quantity",
                                                    "value"])
            writer.writeheader()
            writer.writerows(rows)
        print(f"wrote {args.csv}")
    if args.json:
        print(json.dumps({"type": args.type, "storey": args.storey, "rows": rows,
                          "elements_without_quantities": len(missing)},
                         ensure_ascii=False, indent=2))
        return
    print(f"{'guid':<24} {'storey':<16} {'set':<28} {'quantity':<20} value")
    for row in rows:
        print(f"{row['guid'][:23]:<24} {str(row['storey'])[:15]:<16} {row['set'][:27]:<28} "
              f"{row['quantity'][:19]:<20} {row['value']}")
    print(f"\n{len(elements)} element(s) of {args.type}, {len(rows)} quantity value(s)")
    if missing:
        print(f"WARNING: {len(missing)} element(s) have no IfcElementQuantity at all. Their "
              "quantities are missing from the model, not zero.")
    print("Every value carries its quantity set and quantity name on purpose: a quantity without "
          "its set cannot be checked.")


def cmd_psets(args):
    _ifcopenshell, model = open_model(args.file)
    elements = select(model, args.type)
    rows = []
    for element in elements:
        for row in property_rows(element):
            if args.pset and row["set"] != args.pset:
                continue
            rows.append({"guid": element.GlobalId, "name": element_label(element),
                         "storey": storey_of(element), **row})
    if args.json:
        print(json.dumps({"type": args.type, "pset": args.pset, "rows": rows},
                         ensure_ascii=False, indent=2))
        return
    print(f"{'guid':<24} {'set':<26} {'property':<28} value")
    for row in rows:
        value = "" if row["value"] is None else str(row["value"])
        flag = "   <-- EMPTY" if value == "" else ""
        print(f"{row['guid'][:23]:<24} {row['set'][:25]:<26} {row['property'][:27]:<28} "
              f"{value[:40]}{flag}")
    print(f"\n{len(elements)} element(s) of {args.type}, {len(rows)} property value(s)")
    print("Empty values are reported on purpose: they break schedules, IDS checks and takeoff.")


def cmd_missing(args):
    _ifcopenshell, model = open_model(args.file)
    with open(args.require, encoding="utf-8") as fh:
        requirements = json.load(fh)
    findings = []
    for type_name, rules in requirements.items():
        elements = select(model, type_name)
        if not elements:
            findings.append({"type": type_name, "guid": "", "storey": "",
                             "problem": "type not found in the model", "rule": type_name})
            continue
        for element in elements:
            psets = {row["set"]: row for row in property_rows(element)}
            all_props = {(row["set"], row["property"]): row["value"] for row in property_rows(element)}
            for pset in rules.get("psets", []):
                if pset not in psets:
                    findings.append({"type": type_name, "guid": element.GlobalId,
                                     "storey": storey_of(element),
                                     "problem": f"missing property set {pset}",
                                     "rule": f"{type_name}.{pset}"})
            for path in rules.get("properties", []):
                if "." in path:
                    pset_name, prop_name = path.split(".", 1)
                else:
                    pset_name, prop_name = None, path
                if pset_name and (pset_name, prop_name) not in all_props:
                    findings.append({"type": type_name, "guid": element.GlobalId,
                                     "storey": storey_of(element),
                                     "problem": f"missing property {path}",
                                     "rule": path})
                elif pset_name and not str(all_props[(pset_name, prop_name)] or "").strip():
                    findings.append({"type": type_name, "guid": element.GlobalId,
                                     "storey": storey_of(element),
                                     "problem": f"empty property {path}",
                                     "rule": path})
    if args.csv:
        with open(args.csv, "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=["type", "guid", "storey", "problem", "rule"])
            writer.writeheader()
            writer.writerows(findings)
        print(f"wrote {args.csv}")
    by_rule = Counter(f["rule"] for f in findings)
    print(f"{len(findings)} finding(s) against {args.require}:")
    for rule, count in by_rule.most_common():
        print(f"  {rule:<60} {count}")
    print("\nGrouped by rule as well as by element: the modeller fixes the rule, not the "
          "single element.")
    print("This is a project-specific check against the supplied list, not an IDS result.")


def cmd_schedule(args):
    _ifcopenshell, model = open_model(args.file)
    props = [p.strip() for p in args.props.split(",")] if args.props else []
    elements = select(model, args.type, args.storey)
    columns = ["guid", "type", "storey", "name", "tag"] + props
    rows = []
    for element in elements:
        row = {"guid": element.GlobalId, "type": element.is_a(), "storey": storey_of(element),
               "name": getattr(element, "Name", None) or "",
               "tag": getattr(element, "Tag", None) or ""}
        values = {(r["set"], r["property"]): r["value"] for r in property_rows(element)}
        for path in props:
            if "." in path:
                pset_name, prop_name = path.split(".", 1)
                row[path] = values.get((pset_name, prop_name), "")
            else:
                # a bare name is an IFC attribute (Name, Tag, ObjectType) or, failing that, a
                # property found in any pset of the element - the column keeps the name given
                value = getattr(element, path, "")
                if not value:
                    value = next((v for (set_name, prop), v in values.items() if prop == path), "")
                row[path] = value
        rows.append(row)
    if args.csv:
        with open(args.csv, "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)
        print(f"wrote {args.csv}: {len(rows)} row(s)")
    else:
        print(",".join(columns))
        for row in rows:
            print(",".join(str(row.get(c, "")).replace(",", " ") for c in columns))
    print(f"\n{len(rows)} element(s) of {args.type}"
          + (f" on {args.storey}" if args.storey else "")
          + ". Source: the model as received, not the current design.")


def cmd_compare(args):
    _ifcopenshell, old = open_model(args.old)
    _ifcopenshell2, new = open_model(args.new)
    def index(model):
        return {e.GlobalId: e for e in model.by_type("IfcProduct")}
    old_index, new_index = index(old), index(new)
    added = sorted(set(new_index) - set(old_index))
    removed = sorted(set(old_index) - set(new_index))
    changed = []
    for guid in set(old_index) & set(new_index):
        before, after = old_index[guid], new_index[guid]
        diffs = {}
        for attribute in ("Name", "Tag", "ObjectType", "PredefinedType"):
            b, a = getattr(before, attribute, None), getattr(after, attribute, None)
            if str(b) != str(a):
                diffs[attribute] = [str(b), str(a)]
        if before.is_a() != after.is_a():
            diffs["type"] = [before.is_a(), after.is_a()]
        if diffs:
            changed.append({"guid": guid, "name": getattr(after, "Name", None), **diffs})
    payload = {"old": Path(args.old).name, "new": Path(args.new).name,
               "added": len(added), "removed": len(removed), "changed": changed,
               "old_products": len(old_index), "new_products": len(new_index)}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    print(f"== IFC comparison ==  {payload['old']} -> {payload['new']}")
    print(f"products: {payload['old_products']} -> {payload['new_products']}")
    print(f"added: {payload['added']}   removed: {payload['removed']}   "
          f"changed properties: {len(changed)}")
    for row in changed[:20]:
        detail = "; ".join(f"{k}: {v[0]} -> {v[1]}" for k, v in row.items()
                           if k not in ("guid", "name"))
        print(f"  {row['guid'][:22]}  {str(row['name'])[:24]:<24} {detail}")
    if len(changed) > 20:
        print(f"  ... {len(changed) - 20} more")
    print("\nGUIDs are stable only when the authoring tool preserves them. A re-export can show "
          "many removals plus additions with no design change. Check the removed/added pairs "
          "before reporting design changes.")


def cmd_ids(args):
    try:
        from ifctester import ids, reporter
    except ImportError:
        raise DependencyError("ifctester is not installed. It comes with the IfcOpenShell "
                              "ecosystem (pip install ifctester). Without it, use --require "
                              "with a project property list, and say that no IDS was run.")
    _ifcopenshell, model = open_model(args.file)
    spec = ids.open(str(args.spec))
    spec.validate(model)
    payload = {"file": Path(args.file).name, "spec": Path(args.spec).name,
               "specifications": []}
    for spec_item in spec.specifications:
        results = {"name": spec_item.name, "passed": 0, "failed": 0, "elements": []}
        for result in spec_item.results:
            total = len(result.applicable_entities)
            if result.status:
                results["passed"] += 1
            else:
                results["failed"] += 1
                results["elements"].append({"requirement": str(result.requirement),
                                            "applicable": total, "reason": result.reason})
        payload["specifications"].append(results)
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    for item in payload["specifications"]:
        print(f"[{'PASS' if not item['failed'] else 'FAIL'}] {item['name']}  "
              f"passed {item['passed']}, failed {item['failed']}")
        for element in item["elements"]:
            print(f"    {element['requirement'][:70]}  ({element['applicable']} element(s))")
    print("\nAn IDS pass means the model meets the specification as written. It is not a "
          "statement that the design is compliant.")


def build_parser():
    p = argparse.ArgumentParser(description="IFC report (requires ifcopenshell).")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add(name, func):
        s = sub.add_parser(name)
        s.set_defaults(func=func)
        s.add_argument("--file")
        s.add_argument("--json", action="store_true")
        return s

    add("summary", cmd_summary)

    s = add("quantities", cmd_quantities)
    s.add_argument("--type", required=True)
    s.add_argument("--storey")
    s.add_argument("--csv")

    s = add("psets", cmd_psets)
    s.add_argument("--type", required=True)
    s.add_argument("--pset")

    s = add("missing", cmd_missing)
    s.add_argument("--require", required=True)
    s.add_argument("--csv")

    s = add("schedule", cmd_schedule)
    s.add_argument("--type", required=True)
    s.add_argument("--storey")
    s.add_argument("--props")
    s.add_argument("--csv")

    s = sub.add_parser("compare")
    s.add_argument("--old", required=True)
    s.add_argument("--new", required=True)
    s.add_argument("--json", action="store_true")
    s.set_defaults(func=cmd_compare)

    s = add("ids", cmd_ids)
    s.add_argument("--spec", required=True)
    return p


def main():
    args = build_parser().parse_args()
    try:
        args.func(args)
    except DependencyError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 3
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
