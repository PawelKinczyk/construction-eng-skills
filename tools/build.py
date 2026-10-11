#!/usr/bin/env python3
"""Build tool for construction-eng-skills.

Commands:
  sync     Copy shared/references into every skill (skills/<name>/references/shared/).
  check    Validate skills and fail if shared copies drift from shared/references.
  package  Run check, then zip each skill into dist/<name>.zip for claude.ai upload.

Standard library only.
"""

import filecmp
import re
import shutil
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SHARED = ROOT / "shared" / "references"
SKILLS = ROOT / "skills"
DIST = ROOT / "dist"

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
MAX_NAME = 64
MAX_DESCRIPTION = 1024
MAX_LINES = 500
# Not shipped in claude.ai zips.
PACKAGE_EXCLUDE = {"evals", "__pycache__"}


def skill_dirs():
    return sorted(p for p in SKILLS.iterdir() if p.is_dir() and (p / "SKILL.md").exists())


def read_frontmatter(path):
    """Parse simple YAML frontmatter: 'key: value' plus indented continuation lines."""
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    data, key = {}, None
    for line in lines[1:]:
        if line.strip() == "---":
            return data
        if line[:1] in (" ", "\t") and key:
            data[key] = (data[key] + " " + line.strip()).strip()
            continue
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            data[key] = value.strip().strip("\"'")
    return None


def validate(skill):
    errors = []
    skill_md = skill / "SKILL.md"
    fm = read_frontmatter(skill_md)
    if fm is None:
        return [f"{skill.name}: SKILL.md has no closed frontmatter block"]
    name = fm.get("name", "")
    description = fm.get("description", "")
    if name != skill.name:
        errors.append(f"{skill.name}: name '{name}' does not match folder name")
    if not NAME_RE.match(name) or len(name) > MAX_NAME:
        errors.append(f"{skill.name}: name must be lowercase-hyphenated, max {MAX_NAME} chars")
    if not description:
        errors.append(f"{skill.name}: description is missing")
    elif len(description) > MAX_DESCRIPTION:
        errors.append(f"{skill.name}: description is {len(description)} chars, max {MAX_DESCRIPTION}")
    line_count = len(skill_md.read_text(encoding="utf-8").splitlines())
    if line_count > MAX_LINES:
        errors.append(f"{skill.name}: SKILL.md has {line_count} lines, max {MAX_LINES}")
    return errors


def drift(skill):
    """Return list of files where the skill copy differs from shared/references."""
    target = skill / "references" / "shared"
    problems = []
    for src in SHARED.rglob("*"):
        if src.is_file():
            dst = target / src.relative_to(SHARED)
            if not dst.exists() or not filecmp.cmp(src, dst, shallow=False):
                problems.append(f"{skill.name}: out of date: {dst.relative_to(ROOT)}")
    if target.exists():
        for dst in target.rglob("*"):
            if dst.is_file() and not (SHARED / dst.relative_to(target)).exists():
                problems.append(f"{skill.name}: not in shared/: {dst.relative_to(ROOT)}")
    return problems


def cmd_sync():
    for skill in skill_dirs():
        target = skill / "references" / "shared"
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(SHARED, target)
        print(f"synced {skill.name}")
    return 0


def cmd_check():
    errors = []
    skills = skill_dirs()
    for skill in skills:
        errors += validate(skill)
        errors += drift(skill)
    for error in errors:
        print(f"ERROR {error}")
    if errors:
        print("Run 'python tools/build.py sync' to fix drift.")
        return 1
    print(f"OK: {len(skills)} skill(s) checked")
    return 0


def cmd_package():
    if cmd_check():
        return 1
    DIST.mkdir(exist_ok=True)
    for skill in skill_dirs():
        out = DIST / f"{skill.name}.zip"
        with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
            for path in sorted(skill.rglob("*")):
                rel = path.relative_to(skill)
                if path.is_file() and not PACKAGE_EXCLUDE.intersection(rel.parts):
                    zf.write(path, Path(skill.name) / rel)
        print(f"packaged {out.relative_to(ROOT)}")
    return 0


COMMANDS = {"sync": cmd_sync, "check": cmd_check, "package": cmd_package}

if __name__ == "__main__":
    if len(sys.argv) != 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(2)
    sys.exit(COMMANDS[sys.argv[1]]())
