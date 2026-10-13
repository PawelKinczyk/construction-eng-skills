#!/usr/bin/env python3
"""Build the fictional PDF fixtures for the drawing-review evals (no third-party packages).

Run from this folder:  python make_fixtures.py
Writes minimal one-page vector PDFs (Helvetica text) and one "scanned" sheet (no text).
All names, numbers and dates are invented.
"""
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent


def esc(s):
    return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def write_pdf(path, lines, size=(1190, 842)):
    """lines: list of (x, y, text). Empty list gives a page with no text (scan stand-in)."""
    stream = "".join(f"BT /F1 11 Tf {x} {y} Td ({esc(t)}) Tj ET\n" for x, y, t in lines)
    if not lines:  # a filled rectangle stands in for a raster image
        stream = "0.8 g 100 100 600 400 re f\n"
    objs = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {size[0]} {size[1]}] /Contents 4 0 R "
        "/Resources << /Font << /F1 5 0 R >> >> >>",
        f"<< /Length {len(stream)} >>\nstream\n{stream}endstream",
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    out, offsets = b"%PDF-1.4\n", []
    for i, body in enumerate(objs, 1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n{body}\nendobj\n".encode("latin-1")
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(out)


def sheet(path, no, title, rev, status, date, scale, body=(), project="Biurowiec Testowa 5"):
    """Title block in the lower right corner; rev/status/date may be None (field omitted)."""
    lines = [(60, 800, f"Project: {project}")]
    y = 760
    for text in body:
        lines.append((60, y, text))
        y -= 18
    tb = [f"Sheet {no}", f"TITLE: {title}"]
    if rev is not None:
        tb.append(f"Rev: {rev}")
    if status is not None:
        tb.append(f"Status: {status}")
    if date is not None:
        tb.append(f"Date: {date}")
    if scale:
        tb.append(f"Scale {scale}")
    for k, t in enumerate(tb):
        lines.append((900, 120 - 16 * k, t))
    write_pdf(path, lines)


# --- case 1: drawings/ ---------------------------------------------------------------
d = HERE / "drawings"
sheet(d / "M-101_revC.pdf", "M-101", "Ground floor ventilation plan", "C", "S3", "09.10.2026", "1:50")
sheet(d / "M-102_revC.pdf", "M-102", "First floor ventilation plan", "C", "S3", "09.10.2026", "1:50")
sheet(d / "M-301_revB.pdf", "M-301", "Fan coil schedule", "B", "S3", "05.10.2026", None,
      ["FCU schedule"])
sheet(d / "A-101_revA.pdf", "A-101", "Ground floor plan", "A", None, "01.10.2026", "1:100")  # no status
sheet(d / "M-103_revB.pdf", "M-104", "Roof plant plan", "B", "S3", "05.10.2026", "1:50")  # file/title mismatch
write_pdf(d / "scan_E-201.pdf", [])  # scanned, no text layer

# --- case 2: revB/ and revC/ ---------------------------------------------------------
b, c = HERE / "revB", HERE / "revC"
for folder, rev, date in ((b, "B", "05.10.2026"), (c, "C", "09.10.2026")):
    sheet(folder / "S-201.pdf", "S-201", "Ground floor plan, sanitary", rev, "S3", date, "1:50",
          ["Main drain DN 110"])
    sheet(folder / "S-204.pdf", "S-204", "Hot water plant, diagram", rev, "S3", date, "NTS",
          ["Plant rating 60 kW" if rev == "B" else "Plant rating 80 kW"])
    sheet(folder / "S-205.pdf", "S-205", "Fixture schedule", "B", "S3", "05.10.2026", "NTS",
          ["Fixtures 128"])
sheet(b / "S-202.pdf", "S-202", "Basement drainage", "B", "S3", "05.10.2026", "1:50")  # removed in C
sheet(c / "S-203.pdf", "S-203", "Roof drainage", "A", "S1", "09.10.2026", "1:100")  # added in C
sheet(c / "S-206_profile.pdf", "S-206", "Sewer profile, axes A-C", "A", None, "09.10.2026", "1:50")

# --- case 3: mech/ ------------------------------------------------------------------
m = HERE / "mech"
sheet(m / "M-301.pdf", "M-301", "Fan coil unit schedule", "B", "S3", "05.10.2026", None, [
    "Tag    Type        Size  Airflow m3/h  Location",
    "FCU-01 4-pipe      400   450           Open office L1",
    "FCU-02 4-pipe      400   450           Open office L1",
    "FCU-03 4-pipe      600   800           Meeting room L1",
    "FCU-04 4-pipe      400   600           Reception L0"])
sheet(m / "M-101.pdf", "M-101", "Ground floor ventilation plan", "C", "S3", "09.10.2026", "1:50", [
    "FCU-04 reception, 600 m3/h", "Note: FCU-03 airflow 900 m3/h (see plan)"])  # conflicts with schedule
write_pdf(m / "scan_M-302.pdf", [])

# --- case 4: package/ + client list --------------------------------------------------
p = HERE / "package"
sheet(p / "M-101_C.pdf", "M-101", "Ground floor ventilation plan", "C", "S3", "09.10.2026", "1:50")
sheet(p / "M-102_B.pdf", "M-102", "First floor ventilation plan", "B", "S3", "05.10.2026", "1:50")  # list wants C
sheet(p / "M-103_C.pdf", "M-103", "Roof plant plan", "C", "S1", "09.10.2026", "1:50")  # status S1, list S3
sheet(p / "M-104_old_A.pdf", "M-104", "Riser diagram", "A", "S3", "01.10.2026", "NTS")  # list wants B
sheet(p / "M-104_B.pdf", "M-104", "Riser diagram", "B", "S3", "05.10.2026", "NTS")  # supersedes the A file
sheet(p / "M-999_C.pdf", "M-999", "Spare detail", "C", "S3", "09.10.2026", "1:5")  # not on the list
with open(HERE / "client_drawing_list.csv", "w", encoding="utf-8", newline="\n") as fh:
    w = csv.writer(fh, lineterminator="\n")
    w.writerow(["sheet_no", "title", "required_rev", "required_status"])
    for row in [("M-101", "Ground floor ventilation plan", "C", "S3"),
                ("M-102", "First floor ventilation plan", "C", "S3"),
                ("M-103", "Roof plant plan", "C", "S3"),
                ("M-104", "Riser diagram", "B", "S3"),
                ("M-105", "Plant room section", "C", "S3")]:  # missing from the package
        w.writerow(row)
print("fixtures written to", HERE)
