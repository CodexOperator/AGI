"""goal:g7.31.3.1 -- the cold-seat brief lists the five pane-facing routes.

The falsifier: a cold-seat brief / custom-instruction surface lists the five
routes by the names in `goal:g7.31.3`'s table (or records a deliberate rename
old->new). The canonical names are DERIVED from that goal node's table, so a
rename in the table moves this test in the same edit -- the table is the
contract, the artifacts are the copies.

Identified cold-seat surfaces (injection cited in the experiment node):
  * .agi/nodes/doc/director-grok-internals.md    -- grok director PROFILE
    (injected via doc:grok-harness-internals-sync L74 SECTION:PROFILE ->
    profile description, */30 `grok-internals-sync`).
  * .agi/nodes/doc/unified-director-brief.md     -- the director ROLE brief.
  * extensions/agi/briefs/director-belam-duties.md -- standing role file,
    pointer on every card.

KNOWN GAP (residue, NOT asserted here): .agi/nodes/doc/belam-grok-internals.md
(the Prime PROFILE) carries no route enumeration. It is intentionally left out
of ENFORCED and recorded as a residue on the experiment node; those docs are
Belam-edited via write.py only.

Deliberate rename mapping (artifact spelling -> contract name) is asserted
below: write.py -> write, dispatch/workflow -> (dispatch|workflow), etc.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
CONTRACT = REPO / ".agi" / "nodes" / "goal" / "g7.31.3.md"
ENFORCED = (
    REPO / ".agi" / "nodes" / "doc" / "director-grok-internals.md",
    REPO / ".agi" / "nodes" / "doc" / "unified-director-brief.md",
    REPO / "extensions" / "agi" / "briefs" / "director-belam-duties.md",
)
GAP = REPO / ".agi" / "nodes" / "doc" / "belam-grok-internals.md"

# artifact spelling -> canonical contract group (alternatives OR-ed).
RENAMES = {
    "write.py": {"write"},
    "read": {"read"},
    "send": {"send"},
    "dispatch/workflow": {"dispatch", "workflow"},
    "rotate/spawn": {"rotate", "spawn"},
}


def canonical_groups(table_text: str) -> list[set[str]]:
    """Parse `goal:g7.31.3`'s route table into one OR-set per row.

    Row cell shape: `| 1 | **write** | ... |`; alternatives split on `|`
    (escaped as `\\|` in the table). A rename in the goal table changes the
    groups and therefore this assertion, in the same edit.
    """
    groups = []
    for m in re.finditer(r"^\|\s*\d+\s*\|\s*\*\*(.+?)\*\*\s*\|",
                         table_text, re.M):
        alts = [a.replace("\\", "").strip()
                for a in m.group(1).split("|")]
        groups.append({a for a in alts if a})
    return groups


def routes_line(text: str) -> str:
    """The enumeration line: `routes` FIRST, not a prose mention of routes."""
    hits = [ln for ln in text.splitlines() if re.match(r"\s*routes\b", ln)]
    assert len(hits) == 1, hits
    return hits[0]


def normalize(line: str) -> list[str]:
    """Tokens of a routes line: strip a `.py` suffix, split on `·`/`|`/`/`."""
    tail = line.split("routes", 1)[1].replace("`", " ")
    tail = re.sub(r"[·|/,+]+", " ", tail)
    return [t[:-3] if t.endswith(".py") else t for t in tail.split()]


def missing(groups: list[set[str]], line: str) -> list[set[str]]:
    toks = set(normalize(line))
    return [g for g in groups if not (g & toks)]


def test_table_yields_exactly_five_route_groups():
    groups = canonical_groups(CONTRACT.read_text())
    assert len(groups) == 5, groups
    assert [g for g in groups] == [
        {"write"}, {"read"}, {"send"},
        {"dispatch", "workflow"}, {"rotate", "spawn"}], groups


def test_every_enforced_cold_seat_brief_lists_all_five():
    groups = canonical_groups(CONTRACT.read_text())
    for artifact in ENFORCED:
        line = routes_line(artifact.read_text())
        assert not missing(groups, line), (artifact.name, line)


def test_rename_mapping_artifact_spelling_to_contract_name():
    for spelling, group in RENAMES.items():
        assert set(normalize(f"routes: {spelling} x")) & group, spelling


def test_prime_profile_is_the_recorded_gap_not_silently_green():
    assert GAP not in ENFORCED
    assert "routes" not in GAP.read_text()


def test_negative_a_brief_missing_one_route_must_fail():
    groups = canonical_groups(CONTRACT.read_text())
    good = "routes: write.py · read · send · dispatch/workflow · rotate/spawn"
    assert missing(groups, good) == []
    no_send = "routes: write.py · read · dispatch/workflow · rotate/spawn"
    assert missing(groups, no_send) == [{"send"}]
    no_rotate = "routes: write.py · read · send · dispatch/workflow"
    assert missing(groups, no_rotate) == [{"rotate", "spawn"}]
