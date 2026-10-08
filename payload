"""Tests for bin/backfill-mint-ids.py — the one-time additive mint_id
backfill (goal:g2.5 "Tension resolved 2026-08-25: two identifiers, two
jobs").
"""

import importlib.util
import re
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

BIN = Path(__file__).resolve().parents[1] / "bin" / "backfill-mint-ids.py"
spec = importlib.util.spec_from_file_location("backfill_mint_ids", BIN)
bmi = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bmi)

MINT_ID_RE = re.compile(r"^[0-9a-f]{32}$")


def run(project: Path, *args):
    return subprocess.run(
        [sys.executable, str(BIN), "--project", str(project), *args],
        capture_output=True, text=True,
    )


def fm_of(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    return yaml.safe_load(text.split("---", 2)[1])


@pytest.fixture()
def project(tmp_path):
    nodes = tmp_path / "nodes" / "idea"
    nodes.mkdir(parents=True)
    (nodes / "a.md").write_text(
        '---\nconfidence: 1.0\nid: "idea:a"\norigin: level3-scan\n'
        'parents:\n  - goal:g2.5\ntags:\n  - t1\n  - t2\ntitle: "A"\ntype: idea\n'
        '---\n\nBody text for A, unchanged by backfill.\n'
    )
    (nodes / "b.md").write_text(
        '---\nid: "idea:b"\nmint_id: deadbeefdeadbeefdeadbeefdeadbeef\ntype: idea\n---\n\nAlready minted.\n'
    )
    return tmp_path


def test_dry_run_mints_nothing_on_disk(project):
    node_a = project / "nodes" / "idea" / "a.md"
    before = node_a.read_bytes()

    res = run(project)

    assert res.returncode == 0
    assert node_a.read_bytes() == before  # dry-run touches no file
    assert "WOULD-MINT" in res.stdout
    assert "backfill-mint-ids (dry-run): 2 node file(s), 1 already had mint_id, " \
           "1 would mint, 0 unparseable/skipped" in res.stdout


def test_write_adds_mint_id_and_preserves_every_other_field(project):
    node_a = project / "nodes" / "idea" / "a.md"

    res = run(project, "--write")
    assert res.returncode == 0

    fm = fm_of(node_a)
    assert MINT_ID_RE.match(fm["mint_id"])
    # Nothing this script does not own moved or vanished:
    assert fm["id"] == "idea:a"
    assert fm["origin"] == "level3-scan"
    assert fm["parents"] == ["goal:g2.5"]
    assert fm["tags"] == ["t1", "t2"]
    assert fm["title"] == "A"
    assert fm["confidence"] == 1.0
    assert "Body text for A, unchanged by backfill." in node_a.read_text()


def test_node_with_existing_mint_id_is_never_touched(project):
    node_b = project / "nodes" / "idea" / "b.md"
    before = node_b.read_bytes()

    run(project, "--write")

    assert node_b.read_bytes() == before  # byte-identical: not even reformatted
    assert fm_of(node_b)["mint_id"] == "deadbeefdeadbeefdeadbeefdeadbeef"


def test_idempotent_second_write_run_changes_nothing(project):
    run(project, "--write")
    node_a = project / "nodes" / "idea" / "a.md"
    after_first = node_a.read_bytes()
    minted_id = fm_of(node_a)["mint_id"]

    res2 = run(project, "--write")

    assert res2.returncode == 0
    assert node_a.read_bytes() == after_first  # not re-minted, not rewritten
    assert fm_of(node_a)["mint_id"] == minted_id
    assert "2 already had mint_id, 0 minted" in res2.stdout


def test_unparseable_frontmatter_is_reported_and_skipped(project):
    junk = project / "nodes" / "idea" / "junk.md"
    junk.write_text("no frontmatter delimiter at all\n")

    res = run(project, "--write")

    assert res.returncode == 0
    assert "SKIP (unparseable frontmatter)" in res.stderr
    assert "1 unparseable/skipped" in res.stdout
    assert junk.read_text() == "no frontmatter delimiter at all\n"  # untouched


def test_missing_nodes_dir_errors(tmp_path):
    res = run(tmp_path)
    assert res.returncode != 0
    assert "no nodes/" in res.stderr


def test_backfill_function_returns_counts_matching_report(project):
    counts = bmi.backfill(project, write=True)
    assert counts == {"total": 2, "already": 1, "minted": 1, "unparseable": 0}
