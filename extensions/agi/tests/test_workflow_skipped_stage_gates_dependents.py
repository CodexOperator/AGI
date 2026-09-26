"""A SKIPPED stage gates its dependents like a failed one.

hypothesis:a-skipped-stage-gates-its-dependents-like-a-failed-one — falsifiers
1-5, built as stand-in tests: no real dispatch, no real workflow, no real
model. `_run_stage_pi` is a stub that RECORDS the label it was asked to run and
returns a per-label rc, so "did C run" is one boolean.
"""
from __future__ import annotations

import io
import json
import subprocess
import sys
from pathlib import Path
from unittest import mock

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BIN))

import workflow as _wf  # noqa: E402
from workflow import run_workflow  # noqa: E402

_SCHEMA = {"type": "object", "properties": {"ok": {"type": "boolean"}},
           "required": ["ok"]}


def _stage(label, **extra):
    return {"label": label, "role": "kid", "prompt": f"{label} work",
            "schema": _SCHEMA, "model_hint": "sonnet", **extra}


def _write_manifest(repo_root, stages, round_parent=False):
    """Materialize a manifest through the REAL `_load_manifest`. A `kind: round`
    parent only reaches `stages` through the composition route (`extends`), so
    `round_parent` writes base.json + round.json exactly as a composed
    manifest is composed."""
    wf = repo_root / "extensions" / "agi" / "workflows"
    wf.mkdir(parents=True)
    if not round_parent:
        (wf / "w.json").write_text(json.dumps({
            "name": "w", "type": "review", "harness": "pi-free",
            "stages": stages}), encoding="utf-8")
        return _wf._load_manifest(repo_root, "w")
    (wf / "wbase.json").write_text(json.dumps({
        "name": "wbase", "type": "review", "harness": "pi-free",
        "stages": stages}), encoding="utf-8")
    (wf / "w.json").write_text(json.dumps({
        "name": "w", "extends": "wbase", "prelude": [
            {"kind": "round", "label": "round-parent", "timeout_s": 1}],
        "stages": []}), encoding="utf-8")
    return _wf._load_manifest(repo_root, "w")


def _drive(tmp_path, monkeypatch, manifest, rc_for):
    ran: list[str] = []
    root = REPO / ".agi"
    args = {"target": "hypothesis:x", "iteration": "L1.01",
            "sources": [{"key": "a"}, {"key": "b"}]}
    monkeypatch.setattr(_wf, "_load_manifest", lambda repo, key: manifest)
    monkeypatch.setattr(_wf, "_stage_context", lambda *a, **k: "CTX")
    monkeypatch.setattr(_wf.provisioning, "available", lambda root=None: False)
    monkeypatch.setattr(_wf._loc, "shared_project_root",
                        lambda _r: tmp_path / "sessions")
    def _pi(cfg, st, knobs, args, **kw):
        label = st["label"]
        ran.append(label)
        rc = rc_for.get(label.split(":")[0], 0)
        value = {"ok": True}
        if kw.get("view") is not None:  # what the REAL runner does
            kw["view"].stage_finished(label, value)
        return rc, value

    monkeypatch.setattr(_wf, "_run_stage_pi", _pi)
    monkeypatch.setattr(_wf._loc, "iteration_dir",
                        lambda _r, _i: tmp_path / ".agi")
    monkeypatch.setattr(_wf, "_round_git_harvest", lambda *a, **k: {
        "old_tip": "o", "new_tip": "n", "files": []})
    monkeypatch.setattr(_wf.time, "sleep", lambda _s: None)
    buf = io.StringIO()
    return run_workflow(root, "w", "pi", args, False, out=buf), ran, buf


# ---------- falsifier 1: a plain A -> B -> C chain gates transitively ----------

def test_skipped_stage_gates_its_dependent_plain_chain(tmp_path, monkeypatch,
                                                      capsys):
    """FALSIFIER 1 — A fails, B is skipped for A, and C depends ONLY on B. C
    must be skipped BY NAME: the gate has to hold through the chain, not one
    hop. Before the fix B was `skipped` and never entered `failed_keys`, so C
    found nothing to fail on and RAN."""
    manifest = _write_manifest(tmp_path, [
        _stage("A"),
        _stage("B", depends_on=["A"]),
        _stage("C", depends_on=["B"]),
    ])
    rc, ran, _buf = _drive(tmp_path, monkeypatch, manifest, {"A": 1})
    err = capsys.readouterr().err
    assert "A" in ran, ran
    assert "B" not in ran and "C" not in ran, f"C ran after B was skipped: {ran}"
    assert "skipped stage C" in err, err
    assert rc != 0


# ---------- falsifier 2: the same through a REPEATED skipped base -----------

def test_skipped_stage_gates_every_slice_of_a_repeated_dependent(
        tmp_path, monkeypatch, capsys):
    """FALSIFIER 2 — the chain link is a REPEATED stage, so each slice carries
    its own `_repeat_key`. A stage whose every slice was skipped must gate the
    whole repeated dependent, not only the slices whose key happens to be
    recorded."""
    manifest = _write_manifest(tmp_path, [
        _stage("A"),
        _stage("B", depends_on=["A"], repeat={"of": "sources",
                                              "label_template": "B:{key}"}),
        _stage("C", depends_on=["B"], repeat={"of": "sources",
                                              "label_template": "C:{key}"}),
    ])
    rc, ran, _buf = _drive(tmp_path, monkeypatch, manifest, {"A": 1})
    err = capsys.readouterr().err
    assert "A" in ran, ran
    assert not [x for x in ran if x.startswith(("B", "C"))], ran
    assert "skipped stage C:a" in err and "skipped stage C:b" in err, err
    assert rc != 0


# ---------- falsifier 3: the skip line names the ROOT failure ---------------

def test_skip_line_names_the_root_failure_not_the_intermediate(
        tmp_path, monkeypatch, capsys):
    """FALSIFIER 3 — the skip reason for C must carry A, the stage that
    actually failed, so a reader is not sent to B, which never ran."""
    manifest = _write_manifest(tmp_path, [
        _stage("A"),
        _stage("B", depends_on=["A"]),
        _stage("C", depends_on=["B"]),
    ])
    rc, ran, buf = _drive(tmp_path, monkeypatch, manifest, {"A": 1})
    err = capsys.readouterr().err
    line = next(l for l in err.splitlines() if "skipped stage C" in l)
    assert "'A'" in line, f"the C skip line does not name the root: {line}"
    assert "B" not in line.split("dependency")[0], line
    # the run view names the same root
    assert "'A'" in next(l for l in buf.getvalue().splitlines()
                         if "[»] C" in l), buf.getvalue()


# ---------- falsifier 4: a resolved round counts as ok ---------------------

def test_resolved_round_is_counted_in_the_summary_ok_line(
        tmp_path, monkeypatch, capsys):
    """FALSIFIER 4 — a successful stand-in round + 2 reviews must end
    `ok=3`. `_run_round_stage` never touches the view, so before the fix the
    round stayed `pending` and ok under-counted by one."""
    root = tmp_path / ".agi"
    root.mkdir(parents=True, exist_ok=True)
    (root / "manifest.json").write_text(json.dumps(
        {"agents": [{"id": "a00-test", "status": "done", "branch": "loop/hyp"}]}),
        encoding="utf-8")
    manifest = _write_manifest(
        tmp_path, [_stage("review-a"), _stage("review-b")],
        round_parent=True)
    monkeypatch.setattr(_wf.subprocess, "run", lambda cmd, **kw:
                        subprocess.CompletedProcess(cmd, 0, "spawned a00-test\n", ""))
    import dispatch
    monkeypatch.setattr(dispatch, "_branch_has_done_commit",
                        lambda _r, rec, _a: True)
    rc, ran, buf = _drive(tmp_path, monkeypatch, manifest, {})
    summary = next(l for l in buf.getvalue().splitlines()
                   if l.startswith("[summary]"))
    assert rc == 0, capsys.readouterr().err
    assert "ok=3" in summary, f"a resolved round is not counted ok: {summary}"
    assert "failed=0" in summary, summary
    assert "resolved" in next(l for l in buf.getvalue().splitlines()
                              if l.startswith("[stage] round-parent"))


# ---------- falsifier 5: slice isolation and the existing suite -----------

def test_failed_slice_still_lets_a_sibling_slice_run(tmp_path, monkeypatch):
    """FALSIFIER 5 (the SM.105 half that must NOT regress) — a REPEATED base
    whose ONE slice fails still runs its sibling slices, and only the slices
    that depend on the failed one are gated. Gating transitively must not turn
    a single failed slice into a failed base."""
    manifest = _write_manifest(tmp_path, [
        _stage("B", repeat={"of": "sources", "label_template": "B:{key}"}),
        _stage("C", chained_from="B", repeat={"of": "sources",
                                              "label_template": "C:{key}"}),
    ])
    ran: list[str] = []

    def _run(cfg, st, knobs, args, **kw):
        ran.append(st["label"])
        rc = 1 if st["label"] == "B:a" else 0
        if kw.get("view") is not None:
            kw["view"].stage_finished(st["label"], {"ok": True})
        return rc, {"ok": True}

    root = REPO / ".agi"
    args = {"target": "hypothesis:x", "iteration": "L1.01",
            "sources": [{"key": "a"}, {"key": "b"}]}
    monkeypatch.setattr(_wf, "_load_manifest", lambda repo, key: manifest)
    monkeypatch.setattr(_wf, "_stage_context", lambda *a, **k: "CTX")
    monkeypatch.setattr(_wf.provisioning, "available", lambda root=None: False)
    monkeypatch.setattr(_wf._loc, "shared_project_root",
                        lambda _r: tmp_path / "sessions")
    monkeypatch.setattr(_wf, "_run_stage_pi", _run)
    buf = io.StringIO()
    run_workflow(root, "w", "pi", args, False, out=buf)
    assert "B:b" in ran, f"a sibling slice stopped running: {ran}"
    assert "C:b" in ran, f"a sibling dependent stopped running: {ran}"
    assert "C:a" not in ran, ran


def test_a_skip_never_rebinds_the_project_root(tmp_path, monkeypatch, capsys):
    """DH.399 harvest: the skip branch assigned `root = root_failed.get(...)`
    inside run_workflow, whose own `root` is the PROJECT root -- after any skip,
    every later _persist_stage_value / _track_run / _revoke_run_credential got a
    stage LABEL. A later independent stage must still persist under the real root."""
    manifest = _write_manifest(tmp_path, [
        _stage("A"),
        _stage("B", depends_on=["A"]),
        _stage("D"),
    ])
    seen: list = []
    monkeypatch.setattr(_wf, "_persist_stage_value",
                        lambda r, *a, **k: seen.append(("persist", r)))
    monkeypatch.setattr(_wf, "_track_run",
                        lambda r, *a, **k: seen.append(("track", r)))
    rc, ran, _buf = _drive(tmp_path, monkeypatch, manifest, {"A": 1})
    capsys.readouterr()
    assert "D" in ran and "B" not in ran, ran
    assert seen and all(r == REPO / ".agi" for _k, r in seen), seen
