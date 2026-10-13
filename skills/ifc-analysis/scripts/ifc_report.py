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
              --file model.ifc --type IfcWall [--storey "Level 1"] [--csv q.csv] [--json] [--no-type]
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

Property and quantity sets are read from the occurrence and from its type object
(IsTypedBy, or IfcRelDefinesByType in IFC2X3); an occurrence value overrides the type value
and a source column says which (occurrence | type). --no-type switches the type lookup off.

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


def defining_objects(element, include_type=True):
    """Yield (source, definition) for every property/quantity definition of an element.

    Occurrence definitions come from IsDefinedBy (IfcRelDefinesByProperties). Type-level
    definitions come from the type object's HasPropertySets. IFC4 exposes the type through
    IsTypedBy; IFC2X3 has no IsTypedBy and lists IfcRelDefinesByType inside IsDefinedBy, so
    both routes are read and each type object is visited once.
    """
    seen = set()
    for rel in getattr(element, "IsDefinedBy", []) or []:
        definition = getattr(rel, "RelatingPropertyDefinition", None)
        if definition is not None:
            yield "occurrence", definition
        elif include_type and getattr(rel, "RelatingType", None) is not None:
            type_object = rel.RelatingType
            if type_object.id() not in seen:
                seen.add(type_object.id())
                for definition in getattr(type_object, "HasPropertySets", None) or []:
                    yield "type", definition
    if include_type:
        for rel in getattr(element, "IsTypedBy", []) or []:
            type_object = getattr(rel, "RelatingType", None)
            if type_object is None or type_object.id() in seen:
                continue
            seen.add(type_object.id())
            for definition in getattr(type_object, "HasPropertySets", None) or []:
                yield "type", definition


def merge_rows(rows, key):
    """Occurrence rows override type rows with the same key (set, name)."""
    merged = {}
    for row in rows:
        k = key(row)
        if k not in merged or (merged[k]["source"] == "type" and row["source"] == "occurrence"):
            merged[k] = row
    return list(merged.values())


def quantity_rows(element, include_type=True):
    rows = []
    for source, definition in defining_objects(element, include_type):
        if not definition.is_a("IfcElementQuantity"):
            continue
        for quantity in definition.Quantities:
            value = None
            for attribute in ("LengthValue", "AreaValue", "VolumeValue", "CountValue",
                              "WeightValue", "TimeValue"):
                if hasattr(quantity, attribute):
                    value = unwrap(getattr(quantity, attribute))
                    break
            rows.append({"set": definition.Name or "(no name)", "quantity": quantity.Name,
                         "value": value, "source": source})
    return merge_rows(rows, lambda r: (r["set"], r["quantity"]))


def property_rows(element, include_type=True):
    rows = []
    for source, definition in defining_objects(element, include_type):
        if not definition.is_a("IfcPropertySet"):
            continue
        for prop in definition.HasProperties:
            value = None
            if hasattr(prop, "NominalValue"):
                value = unwrap(prop.NominalValue)
            elif hasattr(prop, "EnumerationValues") and prop.EnumerationValues:
                value = ",".join(str(unwrap(v)) for v in prop.EnumerationValues)
            rows.append({"set": definition.Name or "(no name)", "property": prop.Name,
                         "value": value, "source": source})
    return merge_rows(rows, lambda r: (r["set"], r["property"]))


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
        for row in quantity_rows(element, not args.no_type):
            rows.append({"guid": element.GlobalId, "name": element_label(element),
                         "storey": storey_of(element), "set": row["set"],
                         "quantity": row["quantity"], "value": row["value"],
                         "source": row["source"]})
    missing = [e for e in elements if not quantity_rows(e, not args.no_type)]
    if args.csv:
        with open(args.csv, "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=["guid", "name", "storey", "set", "quantity",
                                                    "value", "source"])
            writer.writeheader()
            writer.writerows(rows)
        print(f"wrote {args.csv}")
    if args.json:
        print(json.dumps({"type": args.type, "storey": args.storey, "rows": rows,
                          "elements_without_quantities": len(missing)},
                         ensure_ascii=False, indent=2))
        return
    print(f"{'guid':<24} {'storey':<16} {'set':<28} {'quantity':<20} {'source':<11} value")
    for row in rows:
        print(f"{row['guid'][:23]:<24} {str(row['storey'])[:15]:<16} {row['set'][:27]:<28} "
              f"{row['quantity'][:19]:<20} {row['source']:<11} {row['value']}")
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
        for row in property_rows(element, not args.no_type):
            if args.pset and row["set"] != args.pset:
                continue
            rows.append({"guid": element.GlobalId, "name": element_label(element),
                         "storey": storey_of(element), **row})
    if args.json:
        print(json.dumps({"type": args.type, "pset": args.pset, "rows": rows},
                         ensure_ascii=False, indent=2))
        return
    print(f"{'guid':<24} {'set':<26} {'property':<28} {'source':<11} value")
    for row in rows:
        value = "" if row["value"] is None else str(row["value"])
        flag = "   <-- EMPTY" if value == "" else ""
        print(f"{row['guid'][:23]:<24} {row['set'][:25]:<26} {row['property'][:27]:<28} "
              f"{row['source']:<11} {value[:40]}{flag}")
    print(f"\n{len(elements)} element(s) of {args.type}, {len(rows)} property value(s)")
    print("source = occurrence (set on the element) or type (inherited from the type object; "
          "an occurrence value overrides it). --no-type reads occurrences only.")
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
            rows = property_rows(element, not args.no_type)
            psets = {row["set"]: row for row in rows}
            all_props = {(row["set"], row["property"]): row["value"] for row in rows}
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
    print("Property sets are read from the occurrence and, unless --no-type, from the type "
          "object (occurrence overrides type).")
    print("This is a project-specific check against the supplied list, not an IDS result.")


def cmd_schedule(args):
    ifcopenshell, model = open_model(args.file)
    print(f"Source: {Path(args.file).name}   schema {model.schema}   units "
          + (", ".join(f"{k}={v}" for k, v in units_of(model).items()) or "NOT DECLARED")
          + f"   ifcopenshell {version(ifcopenshell)}")
    props = [p.strip() for p in args.props.split(",")] if args.props else []
    elements = select(model, args.type, args.storey)
    columns = ["guid", "type", "storey", "name", "tag"] + props
    rows = []
    from_type = 0
    for element in elements:
        row = {"guid": element.GlobalId, "type": element.is_a(), "storey": storey_of(element),
               "name": getattr(element, "Name", None) or "",
               "tag": getattr(element, "Tag", None) or ""}
        prop_list = property_rows(element, not args.no_type)
        values = {(r["set"], r["property"]): r["value"] for r in prop_list}
        from_type += sum(1 for r in prop_list if r["source"] == "type"
                         and (r["set"] + "." + r["property"] in props or r["property"] in props))
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
    if from_type:
        print(f"{from_type} requested value(s) were read from the type object (not set on the "
              "occurrence). Use --no-type to read occurrences only.")


def heuristic_key(element):
    return (element.is_a(), str(getattr(element, "Name", None) or ""), storey_of(element))


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
    # heuristic fallback: pair removed and added elements with the same class + name + storey
    pool = defaultdict(list)
    for guid in added:
        pool[heuristic_key(new_index[guid])].append(guid)
    pairs = 0
    unmatched_removed = []
    for guid in removed:
        bucket = pool.get(heuristic_key(old_index[guid]))
        if bucket:
            bucket.pop()
            pairs += 1
        else:
            unmatched_removed.append(guid)
    unmatched_added = [g for bucket in pool.values() for g in bucket]
    ratio = len(removed) / len(old_index) if old_index else 0.0
    payload = {"old": Path(args.old).name, "new": Path(args.new).name,
               "added": len(added), "removed": len(removed), "changed": changed,
               "changed_label": "changed attributes (Name/Tag/ObjectType/PredefinedType); "
                                "property sets are not compared",
               "old_products": len(old_index), "new_products": len(new_index),
               "removed_ratio": round(ratio, 3), "guids_look_regenerated": ratio > 0.5,
               "heuristic_pairs_class_name_storey": pairs,
               "added_after_heuristic": len(unmatched_added),
               "removed_after_heuristic": len(unmatched_removed)}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    print(f"== IFC comparison ==  {payload['old']} -> {payload['new']}")
    print(f"products: {payload['old_products']} -> {payload['new_products']}")
    print(f"added: {payload['added']}   removed: {payload['removed']}   "
          f"changed attributes (Name/Tag/ObjectType/PredefinedType; property sets are NOT "
          f"compared): {len(changed)}")
    if ratio > 0.5:
        print(f"\nWARNING: {len(removed)} of {len(old_index)} old elements ({ratio:.0%}) have no "
              "GUID in the new file. GUIDs are not stable between independent exports, so the "
              "GUID comparison above is not usable as a list of design changes.")
    print(f"\nremoved+added by GUID: {len(removed)} removed, {len(added)} added")
    print("HEURISTIC, not proof - match by class + name + storey:")
    print(f"  {pairs} removed/added pair(s) share class, name and storey (likely the same "
          "element re-exported)")
    print(f"  {len(unmatched_removed)} removed and {len(unmatched_added)} added element(s) "
          "remain without a match")
    for row in changed[:20]:
        detail = "; ".join(f"{k}: {v[0]} -> {v[1]}" for k, v in row.items()
                           if k not in ("guid", "name"))
        print(f"  {row['guid'][:22]}  {str(row['name'])[:24]:<24} {detail}")
    if len(changed) > 20:
        print(f"  ... {len(changed) - 20} more")
    print("\nGUIDs are stable only when the authoring tool preserves them. A re-export can show "
          "many removals plus additions with no design change. Check the removed/added pairs "
          "before reporting design changes. The comparison is evidence about the model; whether "
          "a change is a design change is a project decision.")


def cmd_ids(args):
    try:
        from ifctester import ids, reporter
    except ImportError:
        raise DependencyError("ifctester is not installed. It comes with the IfcOpenShell "
                              "ecosystem (pip install ifctester). Without it, use --require "
                              "with a project property list, and say that no IDS validation "
                              "was run.")
    ifcopenshell, model = open_model(args.file)
    try:
        spec = ids.open(str(args.spec))
    except Exception as exc:  # invalid or unreadable IDS file
        raise ValueError(f"cannot read IDS file {args.spec}: {type(exc).__name__}: "
                         f"{str(exc).splitlines()[0] if str(exc) else ''}")
    spec.validate(model)
    json_report = reporter.Json(spec)
    json_report.report()
    raw = json_report.to_string()
    data = raw if isinstance(raw, dict) else json.loads(raw)
    payload = {"file": Path(args.file).name, "spec": Path(args.spec).name,
               "schema": model.schema,
               "tool": f"ifcopenshell {version(ifcopenshell)}, ifctester "
                       f"{getattr(sys.modules.get('ifctester'), '__version__', 'unknown')}",
               "specifications": []}
    for item in data.get("specifications", []):
        failures = []
        for requirement in item.get("requirements", []):
            for entity in requirement.get("failed_entities", []):
                failures.append({"requirement": requirement.get("label") or
                                 requirement.get("description"),
                                 "element": entity.get("name") or entity.get("global_id"),
                                 "class": entity.get("class"),
                                 "guid": entity.get("global_id"),
                                 "reason": entity.get("reason")})
        payload["specifications"].append({
            "name": item.get("name"), "status": bool(item.get("status")),
            "applicable": item.get("total_applicable"),
            "passed": item.get("total_applicable_pass"),
            "failed": item.get("total_applicable_fail"), "failures": failures})
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    print(f"== IDS validation ==  {payload['file']} against {payload['spec']}   "
          f"schema {payload['schema']}   {payload['tool']}")
    for item in payload["specifications"]:
        print(f"[{'PASS' if item['status'] else 'FAIL'}] {item['name']}  applicable "
              f"{item['applicable']}, passed {item['passed']}, failed {item['failed']}")
        for f in item["failures"]:
            print(f"    {str(f['element'])[:24]:<24} {f['requirement']}: {f['reason']}")
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
        if name in ("quantities", "psets", "missing", "schedule"):
            s.add_argument("--no-type", action="store_true",
                           help="read occurrence property/quantity sets only, not type-level ones")
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
