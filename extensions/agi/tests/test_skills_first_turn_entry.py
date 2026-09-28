"""goal:g1.27 / hypothesis:free-lane-mint-and-skills-startup-have-end-to-end-
tests (b) -- the `skills` first_turn entry ran with zero coverage: nothing ever
RAN one. This runs the LIVE entry, from the live node. FALSIFIERS: the cmd
exits non-zero; its output exceeds its byte_cap; it omits or names a
`skills/agi-*` dir wrongly. Reads only.
"""
from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
ROTATIONS = REPO / ".agi" / "nodes" / ".geometry" / "rotations.md"
sys.path.insert(0, str(REPO / "extensions" / "agi" / "src"))
sys.path.insert(0, str(REPO / "extensions" / "agi" / "bin"))

# NO OMITTED_DEFECT EXEMPTION. The `agi-corrective` clause was once carried
# "until its build node reaches the trunk" (config:rotations why text, 09-27
# NEAR MISS); `build:skills-agi-corrective-SKILL.md` HAS been on the trunk
# since, so the exemption expired. The fix site (`id: config:rotations`, both
# `skills` first_turn entries) now names agi-corrective, and this suite goes
# RED if that clause is ever removed again. A human TODO cannot be
# re-deleted silently; this can.

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


def test_the_skills_entry_names_every_skill_dir_on_the_trunk():
    """BOTH directions, or a `;`-chained clause is unchecked: a dir the entry
    omits is red, and so is a clause naming a REMOVED dir -- the last
    clause's rc never proved that."""
    for role, entry in _skills_entries():
        named = set(re.findall(r"build:skills-(\S+?)-SKILL\.md", entry["cmd"]))
        present = {d.name for d in (REPO / "skills").iterdir()
                   if d.is_dir() and d.name.startswith("agi")}
        assert not (present - named), (
            f"{role}: the skills entry omits {sorted(present - named)}; every "
            "agi-* skill dir on the trunk must be named. Fix site: "
            f"{ROTATIONS.relative_to(REPO)}:83,123 (config:rotations)")
        assert not named - present, (
            f"{role}: the skills entry names {sorted(named - present)}, absent "
            "from the trunk -- a dead clause in the `;`-chained cmd")


def test_every_build_node_the_cmd_names_resolves_in_the_graph():
    """/bin/sh -c returns the LAST clause's rc, so a clause naming a RENAMED
    or REMOVED build node fails while the suite stays green -- a dead clause
    is invisible. Ask the one resolver write.py itself uses
    (node_writer.find_node_file, extensions/agi/bin/node_writer.py:185)."""
    import node_writer
    for role, entry in _skills_entries():
        named = re.findall(r"(build:\S+?\.md)", entry["cmd"])
        assert named, f"{role}: the skills entry names no build node at all"
        dead = [n for n in sorted(set(named))
                if node_writer.find_node_file(REPO / ".agi", n) is None]
        assert not dead, (
            f"{role}: the skills cmd names build nodes {dead} which do not "
            "RESOLVE in the graph -- a dead mid-chain clause: /bin/sh -c "
            "returns only the last clause's rc, so this clause fails SILENTLY")
