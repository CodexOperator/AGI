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


def test_spawn_gate_reads_a_dash_carrying_tmp_node(tmp_path):
    """(c) claim 6c/SL7.17 (hypothesis:l4-prepare-check-2-reads-the-index-blob...):
    the dash-carrying reproducer is a TMP node written by the test — never a
    path under the LIVE nodes dir, so renaming or retiring a live node can
    never break the suite. spawn_gate reads the tmp node's frontmatter with
    the dashes intact (the guard test keeps its repo-wide grep; only the
    fixture moves)."""
    from spawn_gate import _read_frontmatter  # noqa: E402
    node = tmp_path / "hypothesis" / "l4-dash-carrying-tmp-target.md"
    node.parent.mkdir(parents=True)
    node.write_text(
        "---\n"
        f"id: {TARGET_ID}\n"
        "title: 'a --- run inside the title'\n"
        "testable_claim: 'the --- and --- again'\n"
        "---\n"
        "body below\n",
        encoding="utf-8")
    assert node.exists(), f"tmp node missing: {node}"
    fm = _read_frontmatter(node)
    assert fm is not None, "spawn_gate._read_frontmatter read None — split still cuts the dashes"
    assert fm.get("id") == TARGET_ID, fm
    assert fm.get("title") == "a --- run inside the title", fm
    assert fm.get("testable_claim") == "the --- and --- again", fm


def test_migrated_evidence_gate_reader_matches_legacy_on_real_nodes():
    """(b) evidence_gate.read_frontmatter_text agrees with legacy on 20 nodes."""
    from evidence_gate import read_frontmatter_text  # noqa: E402
    for p in _well_formed_nodes(20):
        text = p.read_text(encoding="utf-8")
        assert read_frontmatter_text(text) == _legacy_read(text), p


def test_falsifier_no_substring_split_left_in_migrated_files():
    """(d) No `split(\"---\"` remains in the shared reader or the 8 migrated files.

    The reader is the ONE place the boundary lives; any substring split that
    survives is a regression. (The remaining naive readers — snapshot-goals,
    crons, sensei, brief, envfile, write_guard, season, post_wire, workflow,
    backfill, verify_unified, snapshot-build-site — were migrated onto
    frontmatter.py by hypothesis:l4-every-remaining-frontmatter-reader-calls-
    the-one-line-anchored-splitter; the repo-wide guard, test_repo_wide_guard_
    only_frontmatter_allowed, now owns the whole bin/ tree.)
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


# --- hypothesis:l4-every-remaining-frontmatter-reader-calls-the-one-line-anchored-splitter
#
# SL7.11 residue: all seventeen documented naive `text.split("---", 2)` readers
# in `bin/` were migrated onto `frontmatter.split_frontmatter`. These tests
# pin the two halves that have to stay true: (e) NO naive reader remains in
# ANY engine file outside frontmatter.py — the repo-wide guard — and (f) the
# guard actually FAILS when a naive site lands (so a new reader trips the
# suite instead of passing because "nothing matched today"). Plus (g) the
# round-trip over a fixture goal whose title carries a `---` run, which is the
# read-narrowing the render check depends on.


def _naive_split_offenders(bin_dir: Path) -> list[str]:
    """Every *.py under `bin_dir` whose source contains the naive split literal.

    The guard greps the live source, exactly as documented: a file carrying
    `split("---", 2)` anywhere — code OR prose — is a reader the line-anchored
    splitter has not absorbed. frontmatter.py alone may carry it, and only
    because it is the boundary owner; today it does not even do that.
    """
    offenders = []
    for p in sorted(bin_dir.glob("*.py")):
        src = p.read_text(encoding="utf-8", errors="replace")
        if 'split("---", 2)' in src:
            offenders.append(p.name)
    return offenders


def test_repo_wide_guard_only_frontmatter_allowed():
    """(e) No naive read remains in ANY engine file but frontmatter.py."""
    bin_dir = Path(__file__).resolve().parent.parent / "bin"
    offenders = [f for f in _naive_split_offenders(bin_dir) if f != "frontmatter.py"]
    assert not offenders, (
        f"naive split(\"---\", 2) still in: {offenders} — migrate to "
        f"frontmatter.split_frontmatter"
    )


def test_repo_wide_guard_flags_a_new_naive_site():
    """(f) The guard is live: it FAILS when a naive site is injected.

    Zero matches today is not the point — a future reader introduces a match.
    Probe a synthetic bin/ with one offender and assert the same checker the
    guard runs flags it, so the suite would go red rather than silently accept.
    """
    import tempfile
    with tempfile.TemporaryDirectory() as td:
        probe = Path(td) / "probe.py"
        probe.write_text('parts = text.split("---", 2)\n', encoding="utf-8")
        # a real file without the pattern must stay clean
        (Path(td) / "clean.py").write_text("x = 1\n", encoding="utf-8")
        offenders = _naive_split_offenders(Path(td))
        assert offenders == ["probe.py"], offenders


def test_fixture_goal_title_with_dash_run_round_trips():
    """(g) A goal whose title carries a `---` run reads intact, round-trip.

    This is the read-narrowing the `snapshot-goals.py --render --check`
    byte-identical round trip depends on: had the split still cut on the first
    `---` inside the YAML, the title would fragment and the render would move
    bytes. The fixture mirrors the LIVE goal corpus shape — title as a quoted
    scalar holding a literal `---`, plus a body that itself carries a `---`.
    """
    fixture = (
        "---\n"
        "id: goal:g-fixture-dash\n"
        "type: goal\n"
        "title: 'cross --- the --- seam'\n"
        "status: active\n"
        "---\n"
        "preamble\n---\nthis --- line is body\n"
    )
    parted = frontmatter.split_frontmatter(fixture)
    assert parted is not None
    fm_text, body = parted
    # fm_text is exactly the YAML, dash runs intact as one scalar
    assert "title: 'cross --- the --- seam'" in fm_text
    raw = yaml.safe_load(fm_text) or {}
    assert raw["title"] == "cross --- the --- seam", raw
    assert frontmatter.read_frontmatter(fixture) == raw
    # body carries its own `---` — past the frontier it is body, never a split
    assert body == "preamble\n---\nthis --- line is body\n"
    # and the byte-identical round trip: reader output reassembles the input
    assert "---\n" + fm_text + "\n---\n" + body == fixture
