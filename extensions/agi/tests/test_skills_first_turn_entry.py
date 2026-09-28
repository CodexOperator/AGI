"""goal:g1.27 / hypothesis:free-lane-mint-and-skills-startup-have-end-to-end-
tests (b) -- the `skills` first_turn entry landed with zero coverage: nothing in
the suite ever RAN a first_turn cmd. This one runs the LIVE entry, from the
live node, in the live tree, and measures it against its OWN `byte_cap` cell.

FALSIFIERS: the cmd exits non-zero; its output exceeds its declared byte_cap;
or it omits a `skills/agi-*` directory that exists on the trunk. Reads only:
every clause is a `write.py ... 'read payload N:M'`, so the graph is not
written. No user/home/host value appears in an assertion.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
ROTATIONS = REPO / ".agi" / "nodes" / ".geometry" / "rotations.md"
sys.path.insert(0, str(REPO / "extensions" / "agi" / "src"))

# The live entry omits exactly one agi-* skill dir, and the reason recorded on
# config:rotations (belam-S2-L5-XIII 09-27 NEAR MISS) -- "until the node reaches
# the trunk" -- is now FALSE: both skills/agi-corrective/SKILL.md and its build
# node are on the trunk, and its read clause resolves (rc 0). So this is a
# DEFECT, not a deferral, and it is named on experiment:a00-77faeb4c-e043fa
# rather than quietly absorbed here. An empty set means the clause landed and
# this guard is spent.
OMITTED_DEFECT = {"agi-corrective"}


def _skills_entries() -> list[tuple[str, dict]]:
    from graph_core.persistence import frontmatter as _fm
    templates = (_fm.load_node_file(ROTATIONS).frontmatter.get("templates") or {})
    out = []
    for role, ent in sorted(templates.items()):
        if not isinstance(ent, dict):
            continue
        for entry in (ent.get("startup") or {}).get("first_turn") or []:
            if isinstance(entry, dict) and entry.get("label") == "skills":
                out.append((str(role), entry))
    return out


def test_the_live_templates_ship_a_skills_entry():
    assert _skills_entries(), (
        f"no `skills` first_turn entry in {ROTATIONS.name}; the skill index "
        "must load at startup for every role that boots a successor")


def test_the_skills_entry_runs_under_its_own_byte_cap():
    for role, entry in _skills_entries():
        cap = entry.get("byte_cap")
        assert cap, f"{role}: the skills entry declares no byte_cap cell"
        r = subprocess.run(["/bin/sh", "-c", entry["cmd"]], cwd=REPO,
                           capture_output=True, text=True, timeout=120)
        out = (r.stdout + r.stderr).encode("utf-8", "replace")
        assert r.returncode == 0, (
            f"{role}: skills first_turn exited {r.returncode}: {out[:400]!r}")
        assert len(out) <= cap, (
            f"{role}: skills first_turn emitted {len(out)} bytes, over its "
            f"byte_cap cell {cap}")


def test_the_skills_entry_omits_only_the_named_defect():
    """A successor's skill index is exactly the set of skill dirs on the trunk.
    Every agi-* dir must be named, except the ONE omission named on
    experiment:a00-77faeb4c-e043fa; any other gap -- and the guard itself going
    stale (the omission fixed, or a second one added) -- is red here."""
    for role, entry in _skills_entries():
        named = set(re.findall(r"build:skills-(\S+?)-SKILL\.md", entry["cmd"]))
        present = {d.name for d in (REPO / "skills").iterdir()
                   if d.is_dir() and d.name.startswith("agi")}
        assert present - named == OMITTED_DEFECT, (
            f"{role}: the skills first_turn entry names {sorted(named - present)}"
            f" that are absent and omits {sorted(present - named)}; every "
            "agi-* skill dir on the trunk must be named (the one declared "
            "omission is OMITTED_DEFECT -- fix the entry, then drop it)")
