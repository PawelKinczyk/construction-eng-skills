#!/usr/bin/env python3
"""Generate the small fictional IFC fixtures used by evals.json (needs ifcopenshell, ifctester).

Run from anywhere: python make_fixtures.py  (writes next to this script).
All data is invented. GUIDs are deterministic (uuid5 of salt + name) so reruns give the same
files; a different salt gives the "independent re-export" case.
"""
import uuid
from pathlib import Path

import ifcopenshell
import ifcopenshell.api
import ifcopenshell.guid

HERE = Path(__file__).resolve().parent
FM = "Pset_FlowMoverCommon"
AT = "Pset_AirTerminalCommon"
COMMON = "Pset_Common"


def guid(salt, name):
    return ifcopenshell.guid.compress(uuid.uuid5(uuid.NAMESPACE_URL, f"{salt}/{name}").hex)


def build(path, mm=False, salt="a", walls=0, ahus=(), ducts=0, pumps=(), terminals=(),
          proxies=0, unassigned_terminals=(), storey="Level 1"):
    """pumps: (name, occurrence_psets, type_psets_or_None)
    terminals: (name, tag, occurrence_psets, type_psets_or_None)"""
    run = ifcopenshell.api.run
    m = run("project.create_file", version="IFC4")
    proj = run("root.create_entity", m, ifc_class="IfcProject", name="Fictional Clinic")
    if mm:
        run("unit.assign_unit", m, length={"is_metric": True, "raw": "MILLIMETERS"})
    else:
        run("unit.assign_unit", m)
    site = run("root.create_entity", m, ifc_class="IfcSite", name="Site")
    bld = run("root.create_entity", m, ifc_class="IfcBuilding", name="B2")
    st = run("root.create_entity", m, ifc_class="IfcBuildingStorey", name=storey)
    for e, n in ((site, "Site"), (bld, "B2"), (st, storey)):
        e.GlobalId = guid(salt, n)
    run("aggregate.assign_object", m, products=[site], relating_object=proj)
    run("aggregate.assign_object", m, products=[bld], relating_object=site)
    run("aggregate.assign_object", m, products=[st], relating_object=bld)

    def make(cls, name, put=True):
        e = run("root.create_entity", m, ifc_class=cls, name=name)
        e.GlobalId = guid(salt, name)
        if put:
            run("spatial.assign_container", m, products=[e], relating_structure=st)
        return e

    def pset(e, name, props):
        p = run("pset.add_pset", m, product=e, name=name)
        run("pset.edit_pset", m, pset=p, properties=props)

    def typed(e, cls, type_name, type_psets):
        t = run("root.create_entity", m, ifc_class=cls, name=type_name)
        t.GlobalId = guid(salt, type_name)
        run("type.assign_type", m, related_objects=[e], relating_type=t)
        for k, v in type_psets.items():
            pset(t, k, v)

    for i in range(walls):
        w = make("IfcWall", f"W{i + 1}")
        q = run("pset.add_qto", m, product=w, name="Qto_WallBaseQuantities")
        run("pset.edit_qto", m, qto=q, properties={"Length": 6000.0 if mm else 6.0,
                                                   "NetVolume": 3.2})
    for name in ahus:
        make("IfcUnitaryEquipment", name)
    for i in range(ducts):
        make("IfcDuctSegment", f"D{i + 1}")
    for i in range(proxies):
        make("IfcBuildingElementProxy", f"PROXY-{i + 1}")
    for name, occ, typ in pumps:
        p = make("IfcPump", name)
        for k, v in occ.items():
            pset(p, k, v)
        if typ:
            typed(p, "IfcPumpType", f"{name}-TYPE", typ)
    for name, tag, occ, typ in terminals:
        t = make("IfcAirTerminal", name)
        if tag:
            t.Tag = tag
        for k, v in occ.items():
            pset(t, k, v)
        if typ:
            typed(t, "IfcAirTerminalType", f"{name}-TYPE", typ)
    for name in unassigned_terminals:
        make("IfcAirTerminal", name, put=False)
    m.write(str(path))


def main():
    # case 1: millimetre model, walls with Qto, pumps and terminals with no quantities,
    # one proxy and one terminal outside any storey
    build(HERE / "hvac_mm_model.ifc", mm=True, walls=5, ahus=("AHU-01", "AHU-02"), ducts=3,
          proxies=1,
          pumps=[("P-01", {}, None), ("P-02", {}, None)],
          terminals=[("NW-01", "", {}, None), ("NW-02", "", {}, None)],
          unassigned_terminals=["NW-03"])

    # case 2: requirement check. P-01 ok, P-02 empty, P-03 no pset, P-04 value only on the type,
    # P-05 right set but a different property. Terminals: T-01 ok, T-02 empty set, T-03 on type.
    build(HERE / "pumps_requirements_model.ifc",
          pumps=[("P-01", {FM: {"RatedPower": 5.5}}, None),
                 ("P-02", {FM: {"RatedPower": ""}}, None),
                 ("P-03", {}, None),
                 ("P-04", {}, {FM: {"RatedPower": 3.0}}),
                 ("P-05", {FM: {"NominalRotationSpeed": 1450.0}}, None)],
          terminals=[("T-01", "T1", {AT: {"NominalAirFlowRate": 0.05}}, None),
                     ("T-02", "T2", {AT: {}}, None),
                     ("T-03", "T3", {}, {AT: {"NominalAirFlowRate": 0.04}})])
    (HERE / "pumps_requirements.json").write_text(
        '{\n  "IfcPump": {"psets": ["Pset_FlowMoverCommon"],\n'
        '               "properties": ["Pset_FlowMoverCommon.RatedPower"]},\n'
        '  "IfcAirTerminal": {"properties": ["Pset_AirTerminalCommon.NominalAirFlowRate"]}\n}\n',
        encoding="utf-8", newline="\n")
    (HERE / "pumps_requirements.ids").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<ids xmlns="http://standards.buildingsmart.org/IDS" '
        'xmlns:xs="http://www.w3.org/2001/XMLSchema" '
        'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
        'xsi:schemaLocation="http://standards.buildingsmart.org/IDS '
        'http://standards.buildingsmart.org/IDS/1.0/ids.xsd">\n'
        '  <info><title>Pump rated power (fictional)</title></info>\n'
        '  <specifications>\n'
        '    <specification name="Pumps carry a rated power" ifcVersion="IFC4">\n'
        '      <applicability minOccurs="1" maxOccurs="unbounded"><entity><name><simpleValue>IFCPUMP</simpleValue></name></entity>'
        '</applicability>\n'
        '      <requirements><property dataType="IFCREAL" cardinality="required">'
        '<propertySet><simpleValue>Pset_FlowMoverCommon</simpleValue></propertySet>'
        '<baseName><simpleValue>RatedPower</simpleValue></baseName></property></requirements>\n'
        '    </specification>\n'
        '  </specifications>\n'
        '</ids>\n', encoding="utf-8", newline="\n")

    # case 3: revision B and an independent re-export C (all GUIDs regenerated; one pump added)
    rev_b = dict(walls=1, terminals=[("T-01", "AT-1", {}, None)])
    build(HERE / "clinic_revB.ifc", salt="B",
          pumps=[("P-01", {FM: {"RatedPower": 5.5}}, None),
                 ("P-02", {FM: {"RatedPower": 11.0}}, None)], **rev_b)
    build(HERE / "clinic_revC.ifc", salt="C",
          pumps=[("P-01", {FM: {"RatedPower": 5.5}}, None),
                 ("P-02", {FM: {"RatedPower": 11.0}}, None),
                 ("P-03", {FM: {"RatedPower": 7.5}}, None)], **rev_b)
    # same revision C with GUIDs preserved from B (for comparison, not used by an eval)
    build(HERE / "clinic_revC_sameguids.ifc", salt="B",
          pumps=[("P-01", {FM: {"RatedPower": 5.5}}, None),
                 ("P-02", {FM: {"RatedPower": 11.0}}, None),
                 ("P-03", {FM: {"RatedPower": 7.5}}, None)], **rev_b)

    # case 4: air terminals, FireRating on the type for two of three, one blank tag
    build(HERE / "terminals_schedule_model.ifc",
          terminals=[("T-01", "AT-101", {AT: {"NominalAirFlowRate": 0.05}},
                      {COMMON: {"FireRating": "EI60"}}),
                     ("T-02", "AT-102", {AT: {"NominalAirFlowRate": 0.04}}, None),
                     ("T-03", "", {AT: {"NominalAirFlowRate": 0.06}},
                      {COMMON: {"FireRating": ""}})])


if __name__ == "__main__":
    main()
