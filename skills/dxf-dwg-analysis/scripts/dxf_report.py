#!/usr/bin/env python3
"""DXF report: layers, blocks, attributes, text, units, extents, revision diff.

Requires ezdxf (pip install ezdxf). DWG is not read directly: convert a copy to DXF with the
ODA File Converter first, then run these commands on the DXF. The script says so and stops if
given a .dwg file.

Reads only. It never modifies, purges or saves the user's file; output goes to stdout or to a
new file you name with --csv.

Commands:
  summary  units, extents, entity and block totals, layouts, xrefs, proxies
           --file A-101.dxf [--json]
  layers   layer list with state and entity count
           --file A-101.dxf [--csv layers.csv]
  blocks   block insert counts, and attributes per insert
           --file A-101.dxf [--attributes] [--csv blocks.csv]
  text     TEXT and MTEXT with layer and position
           --file A-101.dxf [--pattern "SAP|DSO"] [--include-off] [--json]
  diff     compare two files: layers, entity counts, block counts (also per layer),
           attribute values by TAG, units, extents
           --old revB.dxf --new revC.dxf [--json]

Extents: the full extents include entities on off/frozen layers and attribute text; the
"visible" extents use entities on layers that are on and not frozen.
Counts are model space by default; paper space is reported separately as layout content.
Units come from $INSUNITS and are reported, never assumed.
"""

import argparse
import csv
import json
import sys
from collections import Counter
from pathlib import Path

UNITS = {0: "unitless", 1: "inches", 2: "feet", 3: "miles", 4: "millimetres", 5: "centimetres",
         6: "metres", 7: "kilometres", 8: "microinches", 9: "mils", 10: "yards",
         11: "angstroms", 12: "nanometres", 13: "microns", 14: "decimetres", 15: "decametres",
         16: "hectometres", 17: "gigametres", 18: "astronomical", 19: "light years",
         20: "parsecs", 21: "US survey feet", 22: "US survey inches"}
ANON = ("*",)


class DependencyError(Exception):
    pass


def load(path):
    if str(path).lower().endswith(".dwg"):
        raise DependencyError(
            "DWG cannot be read directly. Convert a copy to DXF first, for example:\n"
            '  "<ODA File Converter folder>\\ODAFileConverter.exe" <in_folder> <out_folder> '
            "ACAD2018 DXF 0 1\n"
            "then run this script on the DXF output. Record the converter version in the report.")
    try:
        import ezdxf
    except ImportError:
        raise DependencyError("ezdxf is not installed. Run: pip install ezdxf")
    return ezdxf, ezdxf.readfile(str(path))


def units_name(doc):
    code = doc.header.get("$INSUNITS", 0)
    return f"{UNITS.get(code, 'unknown')} (code {code})"


def _box_dict(box):
    if not box.has_data:
        return None
    lo, hi = box.extmin, box.extmax
    return {"min": [round(lo.x, 2), round(lo.y, 2)], "max": [round(hi.x, 2), round(hi.y, 2)],
            "size": [round(hi.x - lo.x, 2), round(hi.y - lo.y, 2)]}


def extents(doc):
    """Full extents of model space plus 'visible': entities on layers that are on and thawed."""
    try:
        from ezdxf import bbox
    except ImportError:
        return None
    msp = doc.modelspace()
    try:
        result = _box_dict(bbox.extents(msp))
    except Exception:
        return None
    if result is None:
        return None
    hidden = {layer.dxf.name for layer in doc.layers if layer.is_off() or layer.is_frozen()}
    try:
        visible = [e for e in msp if e.dxf.layer not in hidden]
        result["visible"] = _box_dict(bbox.extents(visible)) if visible else None
    except Exception:
        result["visible"] = None
    result["hidden_layers"] = sorted(hidden)
    return result


EXTENTS_NOTE = ("Note: full extents include entities on off/frozen layers and attribute text, "
                "so they can be larger than the plotted drawing. 'visible' uses only layers "
                "that are on and not frozen.")


def print_extents(label, ext):
    if not ext:
        print(f"{label}: not available (no readable entities, or ezdxf.bbox missing)")
        return
    size = ext["size"]
    print(f"{label}: min {ext['min']}  max {ext['max']}  size {size[0]} x {size[1]}")
    vis = ext.get("visible")
    if vis and vis["size"] != size:
        print(f"{label} (visible layers only): min {vis['min']}  max {vis['max']}  "
              f"size {vis['size'][0]} x {vis['size'][1]}")
    elif vis is None and ext.get("hidden_layers"):
        print(f"{label} (visible layers only): no entities on visible layers")
    if ext.get("hidden_layers"):
        print("  off/frozen layers: " + ", ".join(ext["hidden_layers"]))


def layer_counts(msp):
    return Counter(entity.dxf.layer for entity in msp)


def block_insert_counts(msp):
    counts = Counter()
    for insert in msp.query("INSERT"):
        counts[insert.dxf.name] += 1
    return counts


def cmd_summary(args):
    ezdxf, doc = load(args.file)
    msp = doc.modelspace()
    types = Counter(entity.dxftype() for entity in msp)
    proxies = sum(count for name, count in types.items() if "PROXY" in name.upper())
    xrefs = [block.name for block in doc.blocks if getattr(block, "is_xref", False)]
    layouts = []
    for name in doc.layouts.names():
        layout = doc.layouts.get(name)
        layouts.append({"name": name, "entities": len(layout)})
    inserts = block_insert_counts(msp)
    anonymous = sum(count for name, count in inserts.items() if name.startswith(ANON))
    payload = {"file": Path(args.file).name, "ezdxf": ezdxf.__version__,
               "units": units_name(doc), "extents": extents(doc),
               "modelspace_entities": sum(types.values()),
               "entity_types": dict(types.most_common()),
               "block_inserts": sum(inserts.values()),
               "anonymous_block_inserts": anonymous,
               "block_names": len(inserts), "layouts": layouts,
               "xrefs": xrefs, "proxy_entities": proxies}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    print(f"== DXF summary ==  {payload['file']}   ezdxf {payload['ezdxf']}")
    print(f"units: {payload['units']}")
    print_extents("extents", payload["extents"])
    if payload["extents"]:
        print("  " + EXTENTS_NOTE)
        size = payload["extents"]["size"]
        if max(size) > 10000 and "millimet" not in payload["units"]:
            print("  WARNING: extents are large for the stated units. Check $INSUNITS and look "
                  "for stray entities before using any length or area.")
    print(f"model space: {payload['modelspace_entities']} entities, "
          f"{payload['block_inserts']} block inserts "
          f"({payload['anonymous_block_inserts']} anonymous, excluded from symbol counts)")
    print("entity types: " + ", ".join(f"{k} {v}" for k, v in list(payload["entity_types"].items())[:10]))
    print("layouts: " + ", ".join(f"{l['name']} ({l['entities']})" for l in payload["layouts"]))
    if payload["xrefs"]:
        print(f"XREFS ({len(payload['xrefs'])}): " + ", ".join(payload["xrefs"]))
    if proxies:
        print(f"proxy entities: {proxies} - their content is not readable, counts may be low")
    if not payload["xrefs"] and not proxies:
        print("no xrefs, no proxy entities")


def cmd_layers(args):
    _ezdxf, doc = load(args.file)
    msp = doc.modelspace()
    counts = layer_counts(msp)
    rows = []
    for layer in doc.layers:
        rows.append({"layer": layer.dxf.name, "entities": counts.get(layer.dxf.name, 0),
                     "off": bool(layer.is_off()), "frozen": bool(layer.is_frozen()),
                     "locked": bool(layer.is_locked()), "color": layer.dxf.color,
                     "linetype": layer.dxf.linetype})
    rows.sort(key=lambda r: (-r["entities"], r["layer"]))
    if args.csv:
        with open(args.csv, "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()) if rows else
                                    ["layer", "entities", "off", "frozen", "locked", "color",
                                     "linetype"])
            writer.writeheader()
            writer.writerows(rows)
        print(f"wrote {args.csv}")
    print(f"{'layer':<40} {'entities':>8}  state")
    for row in rows:
        state = ",".join(k for k in ("off", "frozen", "locked") if row[k]) or "on"
        print(f"{row['layer'][:39]:<40} {row['entities']:>8}  {state}")
    print(f"\n{len(rows)} layer(s). Entities outside any listed layer: "
          f"{sum(v for k, v in counts.items() if k not in {r['layer'] for r in rows})}")


def cmd_blocks(args):
    _ezdxf, doc = load(args.file)
    msp = doc.modelspace()
    counts = block_insert_counts(msp)
    rows = []
    for name, count in counts.most_common():
        layers = Counter(insert.dxf.layer for insert in msp.query('INSERT') if insert.dxf.name == name)
        tags = set()
        for insert in msp.query("INSERT"):
            if insert.dxf.name == name:
                tags.update(a.dxf.tag for a in insert.attribs)
        rows.append({"block": name, "inserts": count,
                     "layers": " ".join(sorted(layers)), "tags": " ".join(sorted(tags))})
    if args.csv:
        with open(args.csv, "w", encoding="utf-8", newline="") as fh:
            writer = csv.DictWriter(fh, fieldnames=["block", "inserts", "layers", "tags"])
            writer.writeheader()
            writer.writerows(rows)
        print(f"wrote {args.csv}")
    print(f"{'block':<34} {'count':>6}  layers")
    for row in rows:
        suffix = "  <-- anonymous" if row["block"].startswith(ANON) else ""
        print(f"{row['block'][:33]:<34} {row['inserts']:>6}  {row['layers'][:40]}{suffix}")
    print(f"\n{sum(r['inserts'] for r in rows)} insert(s) of {len(rows)} block name(s)")
    if args.attributes:
        print("\nAttributes per insert:")
        for insert in msp.query("INSERT"):
            if not insert.attribs:
                continue
            values = ", ".join(f"{a.dxf.tag}={a.dxf.text!r}" for a in insert.attribs)
            x, y = insert.dxf.insert.x, insert.dxf.insert.y
            print(f"  {insert.dxf.name:<24} layer {insert.dxf.layer:<20} "
                  f"at {x:.1f},{y:.1f}  {values}")
        print("Note: empty attribute values are reported as '' - they are often unset, which "
              "matters when the tag is used for a schedule.")


def cmd_text(args):
    _ezdxf, doc = load(args.file)
    import re
    pattern = re.compile(args.pattern, re.IGNORECASE) if args.pattern else None
    rows = []
    for entity in doc.modelspace().query("TEXT MTEXT"):
        text = entity.dxf.text if entity.dxftype() == "TEXT" else entity.text
        try:
            point = entity.dxf.insert
            position = [round(point.x, 1), round(point.y, 1)]
        except Exception:
            position = None
        rows.append({"layer": entity.dxf.layer, "type": entity.dxftype(), "text": text,
                     "position": position})
    if pattern:
        rows = [r for r in rows if pattern.search(r["text"] or "")]
    if args.json:
        print(json.dumps({"file": Path(args.file).name, "count": len(rows), "items": rows},
                         ensure_ascii=False, indent=2))
        return
    for row in rows:
        pos = f"{row['position'][0]},{row['position'][1]}" if row["position"] else "-"
        print(f"{row['layer'][:24]:<24} {row['type']:<6} {pos:<18} {row['text'][:80]}")
    print(f"\n{len(rows)} text entity(ies)"
          + (f" matching '{args.pattern}'" if args.pattern else ""))
    print("Note: text on frozen or off layers is still in the file and may not be plotted.")


def file_facts(path):
    ezdxf, doc = load(path)
    msp = doc.modelspace()
    return {"file": Path(path).name, "units": units_name(doc), "extents": extents(doc),
            "layer_counts": layer_counts(msp),
            "type_counts": Counter(entity.dxftype() for entity in msp),
            "block_counts": block_insert_counts(msp),
            "block_layer_counts": Counter((i.dxf.name, i.dxf.layer) for i in msp.query("INSERT")),
            "attrs": insert_attributes(msp)}


def insert_attributes(msp):
    """One dict per INSERT that has attributes: block, layer, attrs {tag: text}."""
    rows = []
    for insert in msp.query("INSERT"):
        if insert.attribs:
            rows.append({"block": insert.dxf.name, "layer": insert.dxf.layer,
                         "attrs": {a.dxf.tag: a.dxf.text for a in insert.attribs}})
    return rows


def compare_attributes(old_rows, new_rows):
    """Compare attribute values by TAG. Inserts are matched by (block, value of the TAG
    attribute) when they carry one; the rest are compared as sets of (block, attribute values)."""
    def split(rows):
        keyed, rest = {}, []
        for row in rows:
            ident = {k.upper(): v for k, v in row["attrs"].items()}.get("TAG", "")
            if ident:
                keyed.setdefault((row["block"], ident), []).append(row)
            else:
                rest.append(row)
        return keyed, rest

    old_keyed, old_rest = split(old_rows)
    new_keyed, new_rest = split(new_rows)
    changes = []
    for key in sorted(set(old_keyed) & set(new_keyed)):
        for before, after in zip(old_keyed[key], new_keyed[key]):
            for tag in sorted(set(before["attrs"]) | set(after["attrs"])):
                v0, v1 = before["attrs"].get(tag), after["attrs"].get(tag)
                if v0 != v1:
                    changes.append({"block": key[0], "id": key[1], "attribute": tag,
                                    "old": v0, "new": v1})
            if before["layer"] != after["layer"]:
                changes.append({"block": key[0], "id": key[1], "attribute": "(layer)",
                                "old": before["layer"], "new": after["layer"]})
    added = sorted(f"{k[0]} TAG={k[1]}" + (f" x{len(v) - len(old_keyed.get(k, []))}" if k in old_keyed else "")
                   for k, v in new_keyed.items() if k not in old_keyed or len(v) > len(old_keyed[k]))
    removed = sorted(f"{k[0]} TAG={k[1]}" + (f" x{len(v) - len(new_keyed.get(k, []))}" if k in new_keyed else "")
                     for k, v in old_keyed.items() if k not in new_keyed or len(v) > len(new_keyed[k]))
    def sig(row):
        return (row["block"], tuple(sorted(row["attrs"].items())))
    c_old, c_new = Counter(sig(r) for r in old_rest), Counter(sig(r) for r in new_rest)
    untagged_added = [f"{b} {dict(a)}" for (b, a), n in sorted((c_new - c_old).items())]
    untagged_removed = [f"{b} {dict(a)}" for (b, a), n in sorted((c_old - c_new).items())]
    return {"changed": changes, "added": added, "removed": removed,
            "untagged_added": untagged_added, "untagged_removed": untagged_removed}


def cmd_diff(args):
    old, new = file_facts(args.old), file_facts(args.new)
    layers_added = sorted(set(new["layer_counts"]) - set(old["layer_counts"]))
    layers_removed = sorted(set(old["layer_counts"]) - set(new["layer_counts"]))
    layer_changes = [{"layer": name, "old": old["layer_counts"][name], "new": new["layer_counts"][name]}
                     for name in sorted(set(old["layer_counts"]) & set(new["layer_counts"]))
                     if old["layer_counts"][name] != new["layer_counts"][name]]
    blocks_added = sorted(set(new["block_counts"]) - set(old["block_counts"]))
    blocks_removed = sorted(set(old["block_counts"]) - set(new["block_counts"]))
    block_changes = [{"block": name, "old": old["block_counts"][name], "new": new["block_counts"][name]}
                     for name in sorted(set(old["block_counts"]) & set(new["block_counts"]))
                     if old["block_counts"][name] != new["block_counts"][name]]
    layer_block_changes = [
        {"block": k[0], "layer": k[1], "old": old["block_layer_counts"].get(k, 0),
         "new": new["block_layer_counts"].get(k, 0)}
        for k in sorted(set(old["block_layer_counts"]) | set(new["block_layer_counts"]))
        if old["block_layer_counts"].get(k, 0) != new["block_layer_counts"].get(k, 0)]
    attribute_changes = compare_attributes(old["attrs"], new["attrs"])
    payload = {"old": {"file": old["file"], "units": old["units"], "extents": old["extents"]},
               "new": {"file": new["file"], "units": new["units"], "extents": new["extents"]},
               "units_changed": old["units"] != new["units"],
               "layers_added": layers_added, "layers_removed": layers_removed,
               "layer_changes": layer_changes,
               "blocks_added": blocks_added, "blocks_removed": blocks_removed,
               "block_changes": block_changes,
               "block_layer_changes": layer_block_changes,
               "attribute_changes": attribute_changes,
               "entity_type_changes": [{"type": t, "old": old["type_counts"].get(t, 0),
                                        "new": new["type_counts"].get(t, 0)}
                                       for t in sorted(set(old["type_counts"]) | set(new["type_counts"]))
                                       if old["type_counts"].get(t, 0) != new["type_counts"].get(t, 0)]}
    if args.json:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return
    print(f"== DXF comparison ==  {old['file']} -> {new['file']}")
    print(f"units: {old['units']} -> {new['units']}"
          + ("   WARNING: units changed" if payload["units_changed"] else ""))
    print_extents("extents old", old["extents"])
    print_extents("extents new", new["extents"])
    print(EXTENTS_NOTE)
    print(f"\nLayers added ({len(layers_added)}): " + (", ".join(layers_added) or "-"))
    print(f"Layers removed ({len(layers_removed)}): " + (", ".join(layers_removed) or "-"))
    print(f"Layer entity count changes ({len(layer_changes)}):")
    for row in layer_changes:
        print(f"  {row['layer']:<38} {row['old']:>6} -> {row['new']:>6}")
    print(f"\nBlocks added ({len(blocks_added)}): " + (", ".join(blocks_added) or "-"))
    print(f"Blocks removed ({len(blocks_removed)}): " + (", ".join(blocks_removed) or "-"))
    print(f"Block count changes ({len(block_changes)}):")
    for row in block_changes:
        print(f"  {row['block']:<38} {row['old']:>6} -> {row['new']:>6}")
    print(f"Block count changes per layer ({len(layer_block_changes)}):")
    for row in layer_block_changes:
        print(f"  {row['block']:<24} {row['layer']:<22} {row['old']:>4} -> {row['new']:>4}")
    ac = attribute_changes
    print(f"\nAttribute value changes by TAG ({len(ac['changed'])}):")
    for row in ac["changed"]:
        print(f"  {row['block']} TAG={row['id']}: {row['attribute']} {row['old']!r} -> {row['new']!r}")
    print(f"Attributed inserts only in new ({len(ac['added'])}): " + ("; ".join(ac["added"]) or "-"))
    print(f"Attributed inserts only in old ({len(ac['removed'])}): " + ("; ".join(ac["removed"]) or "-"))
    if ac["untagged_added"] or ac["untagged_removed"]:
        print("Inserts without a TAG value, compared as sets - only in new: "
              + ("; ".join(ac["untagged_added"]) or "-"))
        print("  only in old: " + ("; ".join(ac["untagged_removed"]) or "-"))
    print("Note: attributes are matched on the TAG attribute; a block without a TAG attribute "
          "is compared as a set of values. Duplicate TAG values are paired in file order.")
    print(f"\nEntity type changes ({len(payload['entity_type_changes'])}):")
    for row in payload["entity_type_changes"][:15]:
        print(f"  {row['type']:<24} {row['old']:>6} -> {row['new']:>6}")
    print("\nNote: a file comparison shows what changed in the file, not what it means. A change "
          "to a count can be a moved line, a duplicated block or a deleted note. Read the "
          "drawing before reporting the change as design work.")
    print("Note: paper space and unresolved xrefs are not compared here.")


def build_parser():
    p = argparse.ArgumentParser(description="DXF report (requires ezdxf).")
    sub = p.add_subparsers(dest="cmd", required=True)

    def add(name, func):
        s = sub.add_parser(name)
        s.set_defaults(func=func)
        return s

    s = add("summary", cmd_summary)
    s.add_argument("--file", required=True)
    s.add_argument("--json", action="store_true")

    s = add("layers", cmd_layers)
    s.add_argument("--file", required=True)
    s.add_argument("--csv")

    s = add("blocks", cmd_blocks)
    s.add_argument("--file", required=True)
    s.add_argument("--attributes", action="store_true")
    s.add_argument("--csv")

    s = add("text", cmd_text)
    s.add_argument("--file", required=True)
    s.add_argument("--pattern")
    s.add_argument("--include-off", action="store_true")
    s.add_argument("--json", action="store_true")

    s = add("diff", cmd_diff)
    s.add_argument("--old", required=True)
    s.add_argument("--new", required=True)
    s.add_argument("--json", action="store_true")
    return p


def main():
    args = build_parser().parse_args()
    try:
        args.func(args)
    except DependencyError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 3
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
