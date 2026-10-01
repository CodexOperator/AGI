"""hypothesis:g716105-council-report-py-writes-one-row-per-round-and-routes-
residues — one report row per round, every residue on its OWNER's leaf. One
falsifier per test, synthetic values, a tmp project and tmp git repo; the LIVE
graph is never written.
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
    leaves = dict(LEAVES) if cell is True else (cell or {})
    cfg = {"council": {"residue_leaves": leaves}} if cell else {}
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


def _writer(store=None, mangle=False):
    """A recording writer; `mangle=True` LANDS a body short of its rows."""
    store = {} if store is None else store
    def write(root, node_id, body):
        store[node_id] = body.split("\n")[0] if mangle else body
    write.read = lambda root, nid: store[nid] if nid in store else cr.node_body(root, nid)
    return write


def _flat(root: Path):
    """Flat args with REAL tips from a tmp git repo (DG3.71b: never an aaa..bbb pin)."""
    def git(*a):
        return cr.subprocess.run(["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t",
                                  *a], text=True, capture_output=True, check=True).stdout.strip()
    if not (root / ".git").exists():
        git("init", "-q"), git("commit", "-qm", "c0", "--allow-empty"), git("commit", "-qm", "c1", "--allow-empty")
    return {"parent": "goal:g7.9", "old": git("rev-parse", "--short=10", "HEAD~1"),
            "new": git("rev-parse", "--short=10", "HEAD")}


def test_c1_an_incomplete_cell_refuses_rc2_with_nothing_written(tmp_path):
    root = _project(tmp_path, cell={**LEAVES, "post-a": ""})   # a hole
    _run(root, verify={"final_recommendation": "accept", "missed": ["x"]})
    store = {}
    with pytest.raises(SystemExit) as exc:
        cr.add(root / ".agi", "k1", _flat(root), writer=_writer(store))
    assert "post-a" in str(exc.value) and store == {}     # no partial row


def test_c2_a_post_with_no_leaf_and_no_default_is_refused_by_name():
    with pytest.raises(SystemExit) as exc:
        cr.leaf_for("post-zzz", {"post-a": "goal:g7.9"})
    assert "post-zzz" in str(exc.value) and cr.LEAF_CELL in str(exc.value)


def test_c3_counts_reconcile_or_rc2_naming_the_round(tmp_path):
    """A writer landing fewer rows than the run files name is rc 2, by round."""
    root = _project(tmp_path)
    _run(root, verify={"final_recommendation": "accept", "missed": ["miss A"]})
    with pytest.raises(SystemExit) as exc:
        cr.add(root / ".agi", "k1", _flat(root), writer=_writer({}, True))
    assert "k1/a1" in str(exc.value)


def test_c3b_a_writer_that_drops_a_row_silently_is_rc2_off_the_reread(tmp_path):
    """The count re-READS the leaf: a writer returning None and landing nothing is rc 2."""
    root = _project(tmp_path)
    _run(root, verify={"final_recommendation": "accept", "missed": ["miss A"]})
    with pytest.raises(SystemExit) as exc:
        cr.add(root / ".agi", "k1", _flat(root), writer=lambda r, n, b: None)
    assert "k1/a1" in str(exc.value) and "0 landed" in str(exc.value)


def test_c3c_a_re_add_with_a_changed_residue_set_is_no_false_rc2(tmp_path):
    """The count names THIS run's rows: an older row under the same key is not counted."""
    root, store = _project(tmp_path), {}
    _run(root, verify={"final_recommendation": "accept", "missed": ["miss A"]})
    cr.add(root / ".agi", "k1", _flat(root), writer=_writer(store))
    _run(root, verify={"final_recommendation": "accept", "missed": ["miss B"]})
    cr.add(root / ".agi", "k1", _flat(root), writer=_writer(store))
    assert "miss A" in store["goal:g7.9"] and "miss B" in store["goal:g7.9"]
    _run(root, verify={"final_recommendation": "accept", "missed": ["miss\nC"]})
    cr.add(root / ".agi", "k1", _flat(root), writer=_writer(store))
    assert "| k1/a1 | verify | miss C |" in store["goal:g7.9"]   # a line break folds


def test_c1b_a_leaf_that_resolves_to_no_node_writes_nothing(tmp_path):
    root = _project(tmp_path, cell={**LEAVES, "post-a": "goal:g404"})
    _run(root, verify={"final_recommendation": "accept", "missed": ["miss A"]})
    store = {}
    with pytest.raises(SystemExit) as exc:
        cr.add(root / ".agi", "k1", _flat(root), writer=_writer(store))
    assert "goal:g404" in str(exc.value) and store == {}


def test_c5_the_real_write_py_writer_lands_the_row_on_a_tmp_node(tmp_path):
    """Corrective 5: the REAL write.py writer, on a tmp project + tmp git repo."""
    root = _project(tmp_path)
    _run(root, verify={"final_recommendation": "accept", "missed": ["miss A"]})
    cr.add(root / ".agi", "k1", _flat(root), writer=cr.write_body)
    assert "| k1/a1 | verify | miss A |" in cr.node_body(root / ".agi", "goal:g7.9")


def test_f1_one_row_per_round_and_a_re_add_never_duplicates(tmp_path):
    root = _project(tmp_path)
    _run(root, label="a1", verify={"final_recommendation": "pass", "verdicts": []})
    _run(root, label="a2", verify={"final_recommendation": "pass", "verdicts": []})
    store = {}
    args = _flat(root)
    cr.add(root / ".agi", "k1", args, writer=_writer(store))
    assert f"| k1/a1 | {args['old']}..{args['new']} |" in store["doc:council-report"]
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
    cr.add(root / ".agi", "k1", _flat(root), writer=_writer(store))
    assert "the blind spot" in store["goal:g7.9"]


def test_f2b_every_residue_of_a_round_reaches_the_leaf(tmp_path):
    """The falsifier for the round-keyed merge: ONE round, THREE residues."""
    root = _project(tmp_path)
    _run(root, "k2", label="b1", verify={"final_recommendation": "accept", "verdicts": [
        {"defect": {"title": "the defect"}}, {"defect": {"title": "z"}, "refuted": True}],
        "missed": ["miss A", "miss B"]})
    store = {}
    cr.add(root / ".agi", "k2", _flat(root), writer=_writer(store))
    leaf = store["goal:g7.9"]
    assert leaf.count("| k2/b1 |") == 3                 # 3 residues, 3 rows
    for title in ("the defect", "miss A", "miss B"):
        assert title in leaf
    assert "z" not in leaf
    assert store["doc:council-report"].count("| k2/b1 |") == 1   # one report row


def test_f2c_a_residue_re_added_twice_is_one_row(tmp_path):
    root = _project(tmp_path)
    _run(root, "k2", label="b1", verify={"final_recommendation": "accept",
                                   "missed": ["miss A", "miss A"]})
    store = {}
    cr.add(root / ".agi", "k2", _flat(root), writer=_writer(store))
    cr.add(root / ".agi", "k2", _flat(root), writer=_writer(store))
    assert store["goal:g7.9"].count("| k2/b1 |") == 1


def test_f3_a_refuted_verdict_lands_nowhere(tmp_path):
    root = _project(tmp_path)
    _run(root, verify={"final_recommendation": "accept",
                       "verdicts": [{"defect": {"title": "no"}, "refuted": True}]})
    store = {}
    cr.add(root / ".agi", "k1", _flat(root), writer=_writer(store))
    assert "goal:g7.9" not in store and store["doc:council-report"].count("| 0 |") == 1


def test_f4_the_prime_resolves_to_director_engine_never_its_own_leaf(tmp_path):
    root = _project(tmp_path, title="round (assigned: belam)")
    _run(root, verify={"final_recommendation": "accept",
                       "missed": ["owned by the Prime"]})
    store = {}
    cr.add(root / ".agi", "k1", _flat(root), writer=_writer(store))
    assert "owned by the Prime" in store["goal:g9.2"]
    assert "belam" not in cr.owner_post("round (assigned: belam)", "")


def test_f5_no_verify_is_review_only_and_a_note_is_not_a_residue(tmp_path):
    root = _project(tmp_path)
    _run(root, review={"verdict_recommendation": "accept", "defects": [
        {"title": "a residue", "severity": "residue"},
        {"title": "a note", "severity": "note"}]})
    store = {}
    cr.add(root / ".agi", "k1", _flat(root), writer=_writer(store))
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
    assert cr.subprocess.run([sys.executable, str(_BIN / "council_report.py"), script],
                              capture_output=True).returncode == 0


def _mur(tmp_path, sp=cr.subprocess):
    """mur F1/F2: 2 rounds, own tips; h1 -> goal (assigned: post-a), h2 -> commit subject."""
    root = _project(tmp_path)
    (root / ".agi/nodes/hypothesis").mkdir()
    for slug, parents in (("h1", ["goal:g7.9"]), ("h2", ["idea:x"])):
        (root / f".agi/nodes/hypothesis/{slug}.md").write_text(
            f"---\nid: hypothesis:{slug}\nparents: {json.dumps(parents)}\n---\n")
    sp.run(["git", "init", "-q", str(root)], check=True)
    for msg in ("c0 (belam)", "c1 (post-a)", "c2 (director-engine)"):
        sp.run(["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t",
                "commit", "-q", "--allow-empty", "-m", msg], check=True)
    tip = [sp.run(["git", "-C", str(root), "rev-parse", f"HEAD~{n}"], text=True,
                  capture_output=True).stdout.strip()[:10] for n in (2, 1, 0)]
    _run(root, label="a1", verify={"final_recommendation": "accept", "missed": ["r one"]})
    _run(root, label="a2-code", verify={"final_recommendation": "accept", "missed": ["r two"]})
    return root, tip, {"rounds": [
        {"key": "a1", "hypothesis": "hypothesis:h1", "old_tip": tip[0], "new_tip": tip[1]},
        {"key": "a2", "hypothesis": "hypothesis:h2", "old_tip": tip[1], "new_tip": tip[2]}]}


def test_mur_f1_each_round_writes_its_own_tips_and_routes_to_its_own_owner(tmp_path):
    (root, tip, args), store = _mur(tmp_path), {}
    cr.add(root / ".agi", "k1", args, writer=_writer(store))
    assert f"| k1/a1 | {tip[0]}..{tip[1]} |" in store["doc:council-report"]
    assert f"| k1/a2-code | {tip[1]}..{tip[2]} |" in store["doc:council-report"]
    assert "r one" in store["goal:g7.9"] and "r two" not in store["goal:g7.9"]
    assert "r two" in store["goal:g9.2"] and "r one" not in store["goal:g9.2"]


@pytest.mark.parametrize("bad", [{"key": "zz"}, {"old_tip": "deadbeef0"}, {"new_tip": ""}])
def test_mur_f2_an_unmatched_label_or_unknown_tip_is_rc2_never_a_qq_row(tmp_path, capsys, bad):
    root, _tip, args = _mur(tmp_path)
    args["rounds"][1].update(bad)
    (tmp_path / "a.json").write_text(json.dumps(args))
    rc = cr.main(["add", "--run", "k1", "--args", str(tmp_path / "a.json"), "--root", str(root)])
    assert (rc, "a2-code" in capsys.readouterr().out) == (2, True)
    assert "?..?" not in (root / ".agi/nodes/doc/council-report.md").read_text()


@pytest.mark.parametrize("bad", [{"old": None}, {"new": ""}, {"new": "deadbeef0"}])
def test_g1_a_flat_tip_missing_or_unknown_is_rc2_with_nothing_written(tmp_path, bad):
    root, store = _project(tmp_path), {}
    _run(root, verify={"final_recommendation": "accept", "missed": ["r one"]})
    args = {k: v for k, v in {**_flat(root), **bad}.items() if v is not None}
    with pytest.raises(SystemExit) as exc:
        cr.add(root / ".agi", "k1", args, writer=_writer(store))
    assert "'a1'" in str(exc.value) and store == {}   # never a ?..? row, nothing written


def test_g2_the_owner_subject_is_new_tips_own_never_old_tips(tmp_path):
    (root, tip, args), store = _mur(tmp_path), {}
    cr.subprocess.run(["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t", "commit",
                       "-q", "--allow-empty", "--allow-empty-message", "-m", ""], check=True)
    args["rounds"][1]["new_tip"] = cr.subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],
                                                     text=True, capture_output=True).stdout.strip()
    cr.add(root / ".agi", "k1", args, writer=_writer(store))   # old_tip subject: c1 (post-a)
    assert "r two" in store["goal:g9.2"] and "r two" not in store["goal:g7.9"]
