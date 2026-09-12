"""One line-anchored frontmatter reader (hypothesis:l4-one-line-anchored-
frontmatter-reader-and-the-suite-runner-refuses-a-held-lock-before-spawning).

Residue (4): a node whose frontmatter VALUE carries a literal `---` run must
read identically through every migrated reader. These tests exercise the
shared `frontmatter` module and the live reproduction it fixes, plus the
falsifier that no split-on-dashes reader remains in the migrated files.
"""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

import frontmatter  # noqa: E402


def _live_nodes_dir() -> Path:
    import locations
    root = locations.find_project_root()
    assert root is not None, "no .agi project root resolvable from pytest cwd"
    nodes = Path(root) / "nodes"
    assert nodes.is_dir(), f"live nodes dir missing: {nodes}"
    return nodes


#: The target node whose `testable_claim` carries a `---` run inside a quoted
#: value — the live reproducer. Its OWN double-quoted testable_claim holds a
#: literal `---`, which the old substring split cut short (measured 25a580079).
TARGET_ID = "hypothesis:l4-one-line-anchored-frontmatter-reader-and-the-suite-runner-refuses-a-held-lock-before-spawning"


@pytest.fixture(scope="module")
def dash_fixture() -> str:
    """A well-formed node whose title and testable_claim carry literal `---`."""
    return (
        "---\n"
        "id: hypothesis:dash-fixture\n"
        "title: 'a --- run inside the title'\n"
        "testable_claim: 'the --- and --- again'\n"
        "---\n"
        "body below\n"
    )


def test_split_frontmatter_survives_dashes_in_values(dash_fixture):
    """(a) A `---` inside a quoted value never splits; body round-trips."""
    res = frontmatter.split_frontmatter(dash_fixture)
    assert res is not None
    fm_text, body = res
    assert body == "body below\n"
    assert "'a --- run inside the title'" in fm_text
    assert "the --- and --- again" in fm_text


def test_read_frontmatter_matches_pyyaml_on_raw_bytes(dash_fixture):
    """(a) read_frontmatter == PyYAML on exactly the frontmatter, -- runs intact."""
    res = frontmatter.split_frontmatter(dash_fixture)
    assert res is not None
    fm_text, _body = res
    raw = yaml.safe_load(fm_text) or {}
    assert frontmatter.read_frontmatter(dash_fixture) == raw
    # the dashes survived as one value, not a split boundary
    assert raw["title"] == "a --- run inside the title"
    assert raw["testable_claim"] == "the --- and --- again"


def test_split_returns_none_without_line1_marker():
    """Absent shape -> None: empty text, marker not on line 1, unterminated."""
    assert frontmatter.split_frontmatter("") is None
    assert frontmatter.split_frontmatter("no marker here\n") is None
    assert frontmatter.split_frontmatter("---\nid: x\n") is None  # no close
    assert frontmatter.split_frontmatter("---foo\n---\nbody\n") is None  # not line-exact


def test_split_never_splits_on_body_dashes():
    """A `---` in the BODY (past the frontier) is body, not a split."""
    text = "---\nid: x\n---\ncode with --- inside\nand --- again\n"
    res = frontmatter.split_frontmatter(text)
    assert res is not None
    _fm, body = res
    assert body == "code with --- inside\nand --- again\n"


def _legacy_read(text: str) -> dict | None:
    """The OLD substring reader, exactly as the seventeen sites did it."""
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except Exception:
        return None
    return fm if isinstance(fm, dict) else None


def _well_formed_nodes(limit: int = 20) -> list[Path]:
    """First `limit` well-formed live node files (frontmatter parses both ways)."""
    nodes = _live_nodes_dir()
    out: list[Path] = []
    for p in sorted(nodes.rglob("*.md")):
        try:
            text = p.read_text(encoding="utf-8")
        except Exception:
            continue
        if _legacy_read(text) is not None and frontmatter.read_frontmatter(text) is not None:
            out.append(p)
        if len(out) >= limit:
            break
    assert out, "no well-formed live node files found"
    return out


def test_byte_identical_reads_on_twenty_real_nodes():
    """(b) migrated reader == old split reader on 20 REAL well-formed nodes."""
    for p in _well_formed_nodes(20):
        text = p.read_text(encoding="utf-8")
        assert frontmatter.read_frontmatter(text) == _legacy_read(text), p


def test_spawn_gate_reads_the_dash_carrying_target():
    """(c) live reproduction fixed: spawn_gate resolves the target node's id."""
    from spawn_gate import _read_frontmatter  # noqa: E402
    path = _live_nodes_dir() / "hypothesis" / "l4-one-line-anchored-frontmatter-reader-and-the-suite-runner-refuses-a-held-lock-before-spawning.md"
    assert path.exists(), f"target node missing: {path}"
    fm = _read_frontmatter(path)
    assert fm is not None, "spawn_gate._read_frontmatter still reads None — split still cuts the dashes"
    assert fm.get("id") == TARGET_ID, fm


def test_migrated_evidence_gate_reader_matches_legacy_on_real_nodes():
    """(b) evidence_gate.read_frontmatter_text agrees with legacy on 20 nodes."""
    from evidence_gate import read_frontmatter_text  # noqa: E402
    for p in _well_formed_nodes(20):
        text = p.read_text(encoding="utf-8")
        assert read_frontmatter_text(text) == _legacy_read(text), p


def test_falsifier_no_substring_split_left_in_migrated_files():
    """(d) No `split(\"---\"` remains in the shared reader or the 8 migrated files.

    The reader is the ONE place the boundary lives; any substring split that
    survives is a regression. (Other engine files — snapshot-goals, crons,
    sensei, brief, envfile, write_guard, season, post_wire, workflow,
    backfill, verify_unified — still split on `---` but are OUTSIDE the
    seventeen-site scope of this hypothesis; a different node owns them.)
    """
    files = ["frontmatter.py", "metrics.py", "evidence_gate.py", "spawn_gate.py",
             "completion.py", "cli.py", "node_writer.py", "stitch.py"]
    bin_dir = Path(__file__).resolve().parent.parent / "bin"
    offenders = []
    for name in files:
        src = (bin_dir / name).read_text(encoding="utf-8")
        # allow only the shared reader's own (never uses split(-)
        if 'split("---"' in src:
            offenders.append(name)
    assert not offenders, f"substring split-on-dashes still present: {offenders}"
