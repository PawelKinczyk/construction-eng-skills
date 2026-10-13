#!/usr/bin/env python3
"""Build the fictional DXF fixtures for the dxf-dwg-analysis evals (requires ezdxf).

Run from any folder:  python make_fixtures.py
Writes p1_plan.dxf, A-101_revB.dxf, A-101_revC.dxf and sample_plan.dwg (a stub, not a real DWG).
All content is invented. Units are metres.
"""
from pathlib import Path

import ezdxf

HERE = Path(__file__).resolve().parent


def base(units=6):
    d = ezdxf.new("R2018")
    d.header["$INSUNITS"] = units
    for n in ["M-HVAC-FCU", "M-HVAC-DUCT", "A-WALL", "A-TEXT", "M-HVAC-FCU-OPT", "Dimensions"]:
        d.layers.add(n)
    b = d.blocks.new("FCU-4PIPE")
    b.add_circle((0, 0), 0.3)
    b.add_attdef("TAG", (0, 0))
    b.add_attdef("FLOW", (0, -.2))
    b = d.blocks.new("DIFFUSER-600")
    b.add_circle((0, 0), 0.3)
    b.add_attdef("TAG", (0, 0))
    b = d.blocks.new("VAV-BOX")
    b.add_circle((0, 0), 0.2)
    return d


def ins(m, name, x, y, layer, **att):
    i = m.add_blockref(name, (x, y), dxfattribs={"layer": layer})
    if att:
        i.add_auto_attribs(att)


def mk(path, fcus, extra_stray=False, opt=True, wall=2, diff=6):
    d = base()
    m = d.modelspace()
    for k, (t, f) in enumerate(fcus):
        ins(m, "FCU-4PIPE", 5 + 4 * k, 4, "M-HVAC-FCU", TAG=t, FLOW=f)
    for k in range(diff):  # the 4th diffuser repeats tag D-03 on purpose
        ins(m, "DIFFUSER-600", 3 + 3 * k, 10, "M-HVAC-DUCT", TAG=f"D-{k + 1:02d}" if k != 3 else "D-03")
    for k in range(2):
        ins(m, "VAV-BOX", 6 + 5 * k, 14, "M-HVAC-DUCT")
    if opt:  # optional FCU on a frozen layer, outside the walls
        ins(m, "FCU-4PIPE", 25, 15, "M-HVAC-FCU-OPT", TAG="FCU-X", FLOW="300")
    for k in range(wall):
        m.add_line((0, 10 * k), (30, 10 * k), dxfattribs={"layer": "A-WALL"})
    m.add_text("WENTYLACJA MECHANICZNA BIUR", dxfattribs={"layer": "A-TEXT", "insert": (1, 18), "height": .3})
    if extra_stray:
        m.add_line((0, 0), (900, 900), dxfattribs={"layer": "A-WALL"})
    m.add_linear_dim(base=(0, -2), p1=(0, 0), p2=(30, 0), dxfattribs={"layer": "Dimensions"}).render()
    if opt:
        d.layers.get("M-HVAC-FCU-OPT").freeze()
    d.saveas(str(path))


mk(HERE / "p1_plan.dxf", [("FCU-01", "450"), ("FCU-02", "450"), ("FCU-03", ""), ("FCU-04", "600")])
mk(HERE / "A-101_revB.dxf", [("FCU-01", "450"), ("FCU-02", "450"), ("FCU-03", "")],
   extra_stray=True, wall=3, diff=6)
mk(HERE / "A-101_revC.dxf", [("FCU-01", "450"), ("FCU-02", "450"), ("FCU-03", "500"), ("FCU-04", "600")],
   opt=False, wall=2, diff=7)
(HERE / "sample_plan.dwg").write_bytes(b"AC1032" + b"\0" * 58)  # stub: only the extension matters
print("fixtures written to", HERE)
