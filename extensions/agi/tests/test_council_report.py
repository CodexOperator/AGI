"""hypothesis:g716105-council-report-py-writes-one-row-per-round-and-routes-
residues — one report row per round, every residue on its OWNER's leaf.

One falsifier per test, every value synthetic, a tmp project and tmp run dir;
the LIVE graph is never written (the node writer is a recording seam, and the
one test that calls the real writer runs it against a tmp node file).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

_REPO = Path(__file__).resolve().parents[3]
_BIN = _REPO / "extensions" / "agi" / "bin"
sys.path.insert(0, str(_BIN))
sys.path.insert(0, str(_REPO / "extensions"))

from agi.bin import council_report as cr  # noqa: E402

LEAVES = {"director-engine": "goal:g9.2", "post-a": "goal:g7.9",
          "default": "goal:g7.33.19"}


def _project(tmp_path: Path, *, cell=True, title="round brief (assigned: post-a)"):
    root = tmp_path / "proj"
    (root / ".agi" / "nodes" / "goal").mkdir(parents=True)
    cfg = {"council": {"residue_leaves": dict(LEAVES)}} if cell else {}
    (root / ".agi" / "config.json").write_text(json.dumps(cfg))
    for nid, slug in (("doc:council-report", "council-report"),
                      ("goal:g7.9", "g7.9"), ("goal:g9.2", "g9.2"),
                      ("goal:g7.33.19", "g7.33.19")):
        f = root / ".agi" / "nodes" / nid.split(":")[0] / f"{slug}.md"
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(
            "---\nid: " + nid + "\ntitle: " + json.dumps(title)
            + "\n---\n# " + nid + "\n")
    return root


def _run(root: Path, key="k1", label="a1", review=None, verify=None):
    d = root / ".agi" / "sessions" / "workflows" / "runs" / key
    d.mkdir(parents=True, exist_ok=True)
    if review is not None:
        (d / f"review_{label}.json").write_text(json.dumps(review))
    if verify is not None:
        (d / f"verify_{label}.json").write_text(json.dumps(verify))
    return d


def _writer(store=None):
    store = store if store is not None else {}
    return lambda root, node_id, body: store.__setitem__(node_id, body)


def test_f1_one_row_per_round_and_a_re_add_never_duplicates(tmp_path):
    root = _project(tmp_path)
    _run(root, label="a1", verify={"final_recommendation": "pass", "verdicts": []})
    _run(root, label="a2", verify={"final_recommendation": "pass", "verdicts": []})
    store = {}
    args = {"parent": "goal:g7.9", "old": "aaa", "new": "bbb"}
    cr.add(root / ".agi", "k1", args, writer=_writer(store))
    assert len([ln for ln in store["doc:council-report"].splitlines()
                if ln.startswith("|")]) == 4          # header + sep + 2 rows
    store2 = {}
    cr.add(root / ".agi", "k1", args, writer=_writer(store2))
    assert store2["doc:council-report"].count("| k1/a1 |") == 1
    assert len([ln for ln in store2["doc:council-report"].splitlines()
                if ln.startswith("|")]) == 4


def test_f2_a_residue_only_in_verify_missed_lands_on_the_owner_leaf(tmp_path):
    root = _project(tmp_path)
    _run(root, review={"verdict_recommendation": "pass", "defects": []},
         verify={"final_recommendation": "accept", "verdicts": [],
                 "missed": ["the blind spot"]})
    store = {}
    cr.add(root / ".agi", "k1", {"parent": "goal:g7.9"}, writer=_writer(store))
    assert "the blind spot" in store["goal:g7.9"]


def test_f3_a_refuted_verdict_lands_nowhere(tmp_path):
    root = _project(tmp_path)
    _run(root, verify={"final_recommendation": "accept",
                       "verdicts": [{"defect": {"title": "no"}, "refuted": True}]})
    store = {}
    cr.add(root / ".agi", "k1", {"parent": "goal:g7.9"}, writer=_writer(store))
    assert "goal:g7.9" not in store and store["doc:council-report"].count("| 0 |") == 1


def test_f4_the_prime_resolves_to_director_engine_never_its_own_leaf(tmp_path):
    root = _project(tmp_path, title="round (assigned: belam)")
    _run(root, verify={"final_recommendation": "accept",
                       "missed": ["owned by the Prime"]})
    store = {}
    cr.add(root / ".agi", "k1", {"parent": "goal:g7.9"}, writer=_writer(store))
    assert "owned by the Prime" in store["goal:g9.2"]
    assert "belam" not in cr.owner_post("round (assigned: belam)", "")


def test_f5_no_verify_is_review_only_and_a_note_is_not_a_residue(tmp_path):
    root = _project(tmp_path)
    _run(root, review={"verdict_recommendation": "accept", "defects": [
        {"title": "a residue", "severity": "residue"},
        {"title": "a note", "severity": "note"}]})
    store = {}
    cr.add(root / ".agi", "k1", {"parent": "goal:g7.9"}, writer=_writer(store))
    assert "REVIEWED:review-only" in store["doc:council-report"]
    assert "a residue" in store["goal:g7.9"] and "a note" not in store["goal:g7.9"]


def test_f6_an_absent_cell_refuses_rc2_naming_the_cell(tmp_path, capsys):
    root = _project(tmp_path, cell=False)
    _run(root, verify={"final_recommendation": "accept", "missed": ["x"]})
    args_file = tmp_path / "args.json"
    args_file.write_text(json.dumps({"parent": "goal:g7.9"}))
    rc = cr.main(["add", "--run", "k1", "--args", str(args_file),
                  "--root", str(root)])
    assert (rc, cr.LEAF_CELL in capsys.readouterr().out) == (2, True)


def test_owner_falls_back_to_the_commit_subject_then_director_engine():
    assert cr.owner_post("", "a commit subject (post-b)") == "post-b"
    assert cr.owner_post("", "no post here") == "director-engine"
    assert cr.owner_post("round (assigned: post-c)", "(post-b)") == "post-c"


def test_a_post_absent_from_the_cell_routes_to_default():
    assert cr.leaf_for("post-zzz", LEAVES) == "goal:g7.33.19"
    assert cr.leaf_for("post-a", LEAVES) == "goal:g7.9"


def test_write_body_is_a_no_op_when_the_body_is_unchanged(tmp_path, monkeypatch):
    root = _project(tmp_path)
    called = []
    monkeypatch.setattr(cr.subprocess, "run",
                        lambda *a, **k: called.append(a))
    cr.write_body(root / ".agi", "doc:council-report",
                  cr.node_body(root / ".agi", "doc:council-report"))
    assert called == []


@pytest.mark.parametrize("script", ["--help"])
def test_help(script):
    import subprocess
    assert subprocess.run([sys.executable, str(_BIN / "council_report.py"), script],
                          capture_output=True).returncode == 0