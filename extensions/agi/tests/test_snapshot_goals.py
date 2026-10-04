"""Tests for bin/snapshot-goals.py — the shared node-file helpers (serializer, THOUGHT); GOALS.md and its render/import retired (goal:g7.16.1.4.1)."""

import importlib.util
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

BIN = Path(__file__).resolve().parents[1] / "bin" / "snapshot-goals.py"
spec = importlib.util.spec_from_file_location("snapshot_goals", BIN)
sg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sg)


GOALS_DOC = """# GOALS.md — sample

Preamble prose that must be ignored, including a stray G9 mention.

---

## G1 — Playable dungeon crawler (sandbox ladder) — status: active

Upgrade the scene one node at a time.

## G2 — Persistent ideation system — status: active

Adapt the research loop.

## G3 — Marketplace with proof-of-playtime — status: horizon

Design sketch only.

## G5 — Retired experiment — status: mothballed

Status value outside the taxonomy.

## G4 — Movement system

No status clause here.
"""


@pytest.fixture()
def project(tmp_path):
    (tmp_path / "GOALS.md").write_text(GOALS_DOC, encoding="utf-8")
    (tmp_path / "nodes").mkdir()
    return tmp_path


def fm_of(path: Path) -> dict:
    parts = path.read_text(encoding="utf-8").split("---", 2)
    return yaml.safe_load(parts[1]) or {}


def goal_nodes(project: Path) -> dict:
    out = {}
    for p in sorted((project / "nodes" / "goal").glob("*.md")):
        out[fm_of(p)["id"]] = (p, fm_of(p))
    return out


def write_node(project: Path, rel: str, fm: dict, body: str = "body"):
    path = project / "nodes" / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    sg.write_frontmatter(path, fm, body)
    return path


# --- 1. parsing ------------------------------------------------------------


# --- 2. unknown status -----------------------------------------------------


# --- 3. seeds from parents -------------------------------------------------


# --- 4. referential integrity ---------------------------------------------


# --- 4b. referential integrity, extended to every parent prefix (G7.1) -----
#
# L15 (later G7.1) only ever validated `goal:`-prefixed parents. On the real
# corpus 89 non-goal parent refs dangled with nothing reporting it — a
# `hypothesis:` vs `hyp:` prefix typo silently disconnected most of the
# `spawns` graph. These tests pin the extension: same mechanism (warn by
# default, exit 0; --strict exits 1), now applied to every prefix, plus a
# distinct message when the dangling ref is a same-slug/different-prefix typo
# of a real id (actionable) versus a genuinely missing node (noise otherwise).


# --- 5. pruning ------------------------------------------------------------


# --- 6. missing GOALS.md ---------------------------------------------------


# --- 7. idempotence --------------------------------------------------------


# --- parser unit -----------------------------------------------------------


# --------------------------------------------- H0i: re-snapshot must not strip


# ------------------------------------- sub-goals and standalone short-term goals

NESTED_DOC = """# GOALS.md

## G1 — Long term thing — status: active

Long body.

### G1.2 — A short step inside G1 — status: active

Sub body.

### G1.3 — Another step — status: complete

Sub body two.

## S1 — Standalone short-term item — status: active

Short body.

## G2 — Second long term — status: horizon

Second body.
"""


@pytest.fixture()
def nested(tmp_path):
    (tmp_path / "GOALS.md").write_text(NESTED_DOC, encoding="utf-8")
    (tmp_path / "nodes").mkdir()
    return tmp_path


def _by_id(project: Path) -> dict:
    return {fm_of(p)["id"]: fm_of(p)
            for p in (project / "nodes" / "goal").glob("*.md")}


# ------------------------------------------------ --strict-goals (goal:g5)


def _sg_project(tmp_path, goals_md, seed_parent):
    (tmp_path / "agi-tree.config.json").write_text("{}")
    (tmp_path / "GOALS.md").write_text(goals_md)
    d = tmp_path / "nodes" / "idea"
    d.mkdir(parents=True)
    (d / "seed.md").write_text(
        f'---\nid: "idea:seed"\ntype: idea\nparents:\n  - {seed_parent}\n---\n\nbody\n')
    return tmp_path


GOALS = "# GOALS\n\n## G1 — Real goal — status: active\n\nbody\n"


# --- write_frontmatter: None must round-trip as null, not the string "None" -
#
# Found live 2026-08-25 backfilling `mint_id` across the agi-tree corpus
# (goal:g2.5): any node carrying a real YAML null (`contrasts:` with nothing
# after it, or a malformed empty `parents:` list entry -- already a known,
# tolerated shape; see `collect_parent_refs`'s empty-entry handling above)
# came back from ONE write_frontmatter round trip as the literal 4-character
# string "None" -- `str(None)` falling through the plain scalar branch. That
# turns a null field into a truthy value, and for `parents: [None]`
# specifically it defeats `collect_parent_refs`'s own empty-entry filter,
# which only special-cases `p is None`, not the string `"None"` -- so a
# malformed-but-recognized entry becomes a phantom dangling reference to a
# node literally named "None".


def test_write_frontmatter_preserves_none_scalar(tmp_path):
    p = write_node(tmp_path, "verdict/x.md", {"id": "verdict:x", "contrasts": None})
    assert fm_of(p)["contrasts"] is None


def test_write_frontmatter_preserves_none_list_entry(tmp_path):
    p = write_node(tmp_path, "hypothesis/x.md", {"id": "hyp:x", "parents": [None]})
    assert fm_of(p)["parents"] == [None]


# --- goal:s12 — a truncated goal body must be visibly truncated --------------


@pytest.fixture()
def capped_project(tmp_path, monkeypatch):
    """A project whose config sets a small `goal_body_cap`, so the cap path is
    exercised without needing a 4000-character fixture."""
    (tmp_path / "agi-tree.config.json").write_text('{"goal_body_cap": 120}')
    monkeypatch.setattr(sg, "PROJECT_ROOT", tmp_path)
    return tmp_path


# --- goal:g6.9 — the nodes are the source; GOALS.md is rendered from them ----


# --- natural_sort_key: order: 's replacement -----------------------------


def test_write_frontmatter_preserves_backslashes(tmp_path):
    value = 'a \\ b " c'
    p = write_node(tmp_path, "goal/y.md", {"id": "goal:y", "title": value})
    assert fm_of(p)["title"] == value


# --- THOUGHT: the authored region of a body (goal:g2.10, goal:g2.11) -------


def test_extract_thought_absent_is_none():
    """Absence is legal and means empty -- that is what made adding the field
    cost zero churn across 786 existing nodes."""
    assert sg.extract_thought("just a body") is None
    assert sg.extract_thought("") is None
    assert sg.extract_thought(None) is None


def test_extract_thought_returns_block_with_markers():
    body = f"derived prose\n\n{sg.THOUGHT_BEGIN}\nwhy I did it\n{sg.THOUGHT_END}"
    got = sg.extract_thought(body)
    assert got is not None
    assert "why I did it" in got
    assert got.startswith("<!--") and got.endswith("-->")


def test_extract_thought_is_multiline_and_non_greedy():
    body = (f"{sg.THOUGHT_BEGIN}\nline one\n\nline two\n{sg.THOUGHT_END}\n"
            f"trailing derived prose")
    got = sg.extract_thought(body)
    assert "line one" in got and "line two" in got
    assert "trailing derived prose" not in got


def test_splice_carries_thought_across_a_regenerating_write():
    """The whole point of g2.10: a scan rewrites the body, the thought lives."""
    old = f"OLD derived\n\n{sg.THOUGHT_BEGIN}\nthe reasoning\n{sg.THOUGHT_END}"
    new = "NEW derived, freshly generated"
    out = sg.splice_thought(new, old)
    assert "NEW derived" in out
    assert "the reasoning" in out
    assert "OLD derived" not in out


def test_splice_prefers_a_thought_authored_this_pass():
    """Clobbering a fresh thought with a stale one is the same defect
    reversed."""
    old = f"x\n{sg.THOUGHT_BEGIN}\nSTALE\n{sg.THOUGHT_END}"
    new = f"y\n{sg.THOUGHT_BEGIN}\nFRESH\n{sg.THOUGHT_END}"
    out = sg.splice_thought(new, old)
    assert "FRESH" in out and "STALE" not in out


def test_splice_is_a_noop_without_a_stored_thought():
    assert sg.splice_thought("body", "no thought here") == "body"
    assert sg.splice_thought("body", None) == "body"


def test_write_frontmatter_preserves_thought_block(tmp_path):
    """End-to-end: the falsifier goal:g2.10 names -- write a thought, let the
    generator rewrite the body, read it back."""
    p = tmp_path / "n.md"
    fm = {"id": "build:x", "type": "build", "title": "x"}
    sg.write_frontmatter(
        p, fm,
        f"v1 derived\n\n{sg.THOUGHT_BEGIN}\nchose X over Y\n{sg.THOUGHT_END}")
    stored = p.read_text()
    assert "chose X over Y" in stored

    old_body = stored.split("---", 2)[2]
    sg.write_frontmatter(p, fm, "v2 derived, wholly regenerated",
                         preserve_body=old_body)
    after = p.read_text()
    assert "v2 derived" in after
    assert "chose X over Y" in after, "the scan wiped the thought (g2.10)"
    assert "v1 derived" not in after


def test_write_frontmatter_without_preserve_body_still_wipes(tmp_path):
    """Opt-in, not automatic: a caller that does not pass the old body gets the
    old behaviour, so this change cannot silently resurrect prose elsewhere."""
    p = tmp_path / "n.md"
    fm = {"id": "build:x", "type": "build", "title": "x"}
    sg.write_frontmatter(
        p, fm, f"{sg.THOUGHT_BEGIN}\nSENTINEL_THOUGHT\n{sg.THOUGHT_END}")
    sg.write_frontmatter(p, fm, "regenerated")
    assert "SENTINEL_THOUGHT" not in p.read_text().split("---", 2)[2]


def test_one_serializer_not_two():
    """goal:s14's residual. The two copies had already drifted apart on both
    null round-trip fixes; a third copy must not appear.

    Identity (`is`) is the wrong assertion and was tried first: each file-path
    import builds its own module object, so two `exec_module` calls on the same
    source yield equal-but-distinct functions. The invariant that actually
    matters is where the function is *defined*.
    """
    bsb = Path(__file__).resolve().parents[1] / "bin" / "snapshot-build-site.py"
    assert "def write_frontmatter" not in bsb.read_text(), (
        "snapshot-build-site.py has re-grown its own serializer (goal:s14)")

    bspec = importlib.util.spec_from_file_location("snapshot_build_site", bsb)
    bs = importlib.util.module_from_spec(bspec)
    bspec.loader.exec_module(bs)
    defined_in = Path(bs.write_frontmatter.__code__.co_filename).name
    assert defined_in == "snapshot-goals.py", defined_in


def test_strip_thought_removes_the_block():
    body = f"real prose\n\n{sg.THOUGHT_BEGIN}\nreasoning\n{sg.THOUGHT_END}"
    out = sg.strip_thought(body)
    assert out == "real prose"
    assert "reasoning" not in out


def test_strip_thought_is_a_noop_without_one():
    assert sg.strip_thought("just prose") == "just prose"
    assert sg.strip_thought("") == ""


def test_post_wire_does_not_define_its_own_serializer():
    """goal:s14, third copy. The sweep that de-duplicated `write_frontmatter`
    missed post_wire.py, which kept a private `yaml.dump` until 2026-09-01 --
    so every node it wired was round-tripped into a different YAML style than
    the corpus (list indent lost, `id:` unquoted, `title:` re-quoted, a stray
    blank line). The grid records a version per changed node, so wiring one
    edge minted versions whose content was quote style."""
    pw = Path(__file__).resolve().parents[1] / "bin" / "post_wire.py"
    text = pw.read_text()
    assert "def write_frontmatter" not in text, (
        "post_wire.py has re-grown its own serializer (goal:s14)")
    assert "yaml.dump" not in text, (
        "post_wire.py is serializing frontmatter itself again (goal:s14)")

    spec = importlib.util.spec_from_file_location("agi_post_wire", pw)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    defined_in = Path(mod.write_frontmatter.__code__.co_filename).name
    assert defined_in == "snapshot-goals.py", defined_in


# ------------------------------------- goal_kind: perpetual (hypothesis
# l3w1-goal-kind-perpetual, L3 wave 1) ------------------------------------


def _rebase_goal(project: Path, node_id: str, old: str, new: str) -> None:
    node = goal_nodes(project)[node_id][0]
    node.write_text(node.read_text(encoding="utf-8").replace(old, new),
                    encoding="utf-8")


def test_goal_schema_accepts_perpetual_and_legacy_long_term():
    """The `[goal].md` schema's goal_kind regex accepts both `perpetual`
    (canonical) and `long-term` (legacy, accepted forever like `phasing-out`),
    and both resolve as spawn variants."""
    import re as _re
    schema = Path(__file__).resolve().parents[3] / ".agi" / "context" \
        / "schemas" / "[goal].md"
    text = schema.read_text(encoding="utf-8")
    m = _re.search(r"goal_kind:\s*'(\^[^']+)'", text)
    assert m, "[goal].md goal_kind regex not found"
    rx = _re.compile(m.group(1))
    assert rx.match("perpetual")
    assert rx.match("long-term")
    assert not rx.match("bogus")
    # spawn: block declares a perpetual variant
    assert "perpetual:" in text and "long-term:" in text


# --- hypothesis l4-a-check-that-cries-wolf-gets-waved-through -----------------
# The `--check` false alarm: GOALS.md (a derived artefact) compared against
# goal nodes (its sources) that a concurrent writer can move under the
# comparison. The guard must retry exactly ONCE, report the retry visibly,
# and preserve fail-closed. These tests are NEW — no existing test is edited.


# --- bundle 4 W-G (director-general-2)
_WG_REPO = Path(__file__).resolve().parents[3]
_WG_CALLERS = {"extensions/agi/driver.sh": r"snapshot-goals\.py", "extensions/agi/bin/verification.py": r"goals-check",
               "extensions/agi/bin/rotate.py": r'"render"|"render_check"|"--render"', ".agi/nodes/.geometry/commands.md": r"goals-check",
               "extensions/agi/workflows/agi-round-review.js": r"snapshot-goals|goals_check",
               "extensions/agi/workflows/review.json": r"GOALS\.md|goals_check"}


def _wg_text(rel):
    p = _WG_REPO / rel
    return p.read_text(encoding="utf-8") if p.exists() else ""


def test_wg_from_doc_and_goals_file_retire():  # GREEN since DG3 W-G.2
    src, loc = BIN.read_text(encoding="utf-8"), _wg_text("extensions/agi/bin/locations.py")
    assert "--from-doc" not in src and "from_doc" not in src
    assert "DEFAULT_GOALS_FILE" not in loc and "goals_file" not in loc


def test_wg_reader_lines_only_point_at_the_retirement():
    schemas = sorted(p.relative_to(_WG_REPO).as_posix() for p in (_WG_REPO / ".agi/context/schemas").glob("*.md"))
    docs = ["CLAUDE.md", "QUICKSTART.md"] + schemas + [
        f"skills/{s}/SKILL.md" for s in ("agi", "agi-goal", "agi-master-gate", "agi-node-write", "agi-verify")]
    # residue 81: anchored on the retirement POINTER, never the substring "retire"
    # (a goal-status line "active | horizon | retired" passed vacuously)
    import re
    assert all((_WG_REPO / d).is_file() for d in docs), "a reader doc went missing"   # residue 88
    ptr = re.compile(r"g7\.16\.1\.4\.1(?!\.?\d)")   # the leaf itself, never its child .4.1.1
    assert [(d, ln) for d in docs for ln in _wg_text(d).splitlines()
            if re.search(r"GOALS\.md|--render", ln) and not ptr.search(ln)] == []
    # render-context.py retired at L1.05: a schema names it only beside that pointer
    assert [(d, ln) for d in schemas for ln in _wg_text(d).splitlines()
            if "render-context.py" in ln and "L1.05" not in ln] == []
