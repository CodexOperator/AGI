"""A `kind: round` stage fails CLOSED and BY NAME.

hypothesis:a-round-stage-fails-closed-by-name-and-every-inherited-review-
stage-is-gated — falsifiers 1, 2 and 5, built as stand-in tests: no real
dispatch, no real workflow, no real model. `subprocess.run` is the stand-in
primitive; a hanging round is a `subprocess.run` that raises
`subprocess.TimeoutExpired` (the dispatch itself never returns) or a manifest
record that never reaches a terminal status (the parent is spawned, the record
hangs). Every review stage dispatch is a `_run_stage_pi` stub that RECORDS the
label it was asked to run, so "did any review stage run" is one boolean.
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


def _review(label):
    return {"label": label, "role": "kid", "prompt": f"{label} work",
            "schema": _SCHEMA, "model_hint": "sonnet"}


def _round_manifest(repo_root, review_labels, repeat_review=False):
    """base.json (the inherited review stages) extends <- round.json (a prelude
    kind:round stage) — the real composition route, materialized by the real
    `_load_manifest`, so the depends_on/chained_from wiring under test is the
    shipped wiring and not a hand-built dict. `repeat_review` expands the one
    inherited stage into one slice per source, the shape a review template
    actually takes."""
    wf = repo_root / "extensions" / "agi" / "workflows"
    wf.mkdir(parents=True)
    base = _review(review_labels[0])
    if repeat_review:
        base["repeat"] = {"of": "sources",
                          "label_template": review_labels[0] + ":{key}"}
    (wf / "base.json").write_text(json.dumps({
        "name": "base", "type": "review", "harness": "pi-free",
        "stages": [base] + [_review(l) for l in review_labels[1:]],
    }), encoding="utf-8")
    (wf / "round.json").write_text(json.dumps({
        "name": "round", "extends": "base",
        "prelude": [{"kind": "round", "label": "round-parent",
                     "timeout_s": 1}],
        "stages": [],
    }), encoding="utf-8")


def _drive(tmp_path, monkeypatch, review_labels, run_impl, rc_in,
           repeat_review=False, sources=None):
    """Run the composed round workflow end to end. `run_impl` is the stand-in
    for `subprocess.run` (the round dispatch); review stages are a
    `_run_stage_pi` stub that records the labels it was asked to run."""
    _round_manifest(tmp_path, review_labels, repeat_review)
    ran: list[str] = []
    root = REPO / ".agi"
    args = {"target": "hypothesis:x", "iteration": "L1.01"}
    if sources:
        args["sources"] = sources
    manifest = _wf._load_manifest(tmp_path, "round")
    monkeypatch.setattr(_wf, "_load_manifest", lambda repo, key: manifest)
    monkeypatch.setattr(_wf, "_stage_context", lambda *a, **k: "CTX")
    monkeypatch.setattr(_wf.provisioning, "available", lambda root=None: False)
    tmp_sessions = tmp_path / "sessions"
    monkeypatch.setattr(_wf._loc, "shared_project_root", lambda _r: tmp_sessions)
    monkeypatch.setattr(
        _wf, "_run_stage_pi",
        lambda cfg, st, knobs, args, **kw: (
            ran.append(st["label"]) or (rc_in, {"ok": True})))
    monkeypatch.setattr(_wf.subprocess, "run", run_impl)
    monkeypatch.setattr(_wf.time, "sleep", lambda _s: None)
    monkeypatch.setattr(_wf._loc, "iteration_dir",
                        lambda _r, _i: tmp_path / ".agi")
    monkeypatch.setattr(_wf, "_round_git_harvest", lambda *a, **k: {
        "old_tip": "o", "new_tip": "n", "files": []})
    import dispatch
    monkeypatch.setattr(dispatch, "_branch_has_done_commit",
                        lambda _r, rec, _a: rec.get("branch") == "loop/hyp")
    buf = io.StringIO()
    return run_workflow(root, "round", "pi", args, False, out=buf), ran, buf


def _dispatch_exit_1(cmd, **kw):
    """The stand-in round: dispatch refuses the spawn and exits 1."""
    return subprocess.CompletedProcess(cmd, 1, "", "spawn refused")


# ---------- falsifier 1: EVERY inherited review stage is skipped -----------

@pytest.mark.parametrize("review_labels", [
    ["review-a", "review-b"],
    ["review-a", "review-b", "review-c"],
])
def test_failed_round_skips_every_inherited_review_stage(
        tmp_path, monkeypatch, capsys, review_labels):
    """FALSIFIER 1 — a stand-in round exiting 1 with 2+ inherited review
    stages. ANY review stage running is a failure of the claim: the chain must
    skip EVERY inherited stage chained to the round, not only the first."""
    rc, ran, _buf = _drive(tmp_path, monkeypatch, review_labels,
                           _dispatch_exit_1, 0)
    err = capsys.readouterr().err
    assert ran == [], f"review stage(s) ran after the round failed: {ran}"
    assert "round-parent" in err and "failed" in err, err
    for label in review_labels:
        assert f"skipped stage {label}" in err, err
    assert rc != 0


def test_failed_round_skips_every_slice_of_a_repeated_inherited_review(
        tmp_path, monkeypatch, capsys):
    """FALSIFIER 1, the shape the plain two-review case does NOT reach: the
    inherited review is a REPEATED stage, so each expanded slice carries its
    own `_repeat_key`. The round is not a repeated base, so its single failure
    must gate EVERY slice — before the fix the containment check
    (`stage['_repeat_key'] in failed_keys[round]`, which is `{None}`) let
    every slice RUN after the round had failed."""
    rc, ran, _buf = _drive(tmp_path, monkeypatch, ["review", "tail-review"],
                           _dispatch_exit_1, 0, repeat_review=True,
                           sources=[{"key": "a"}, {"key": "b"}])
    err = capsys.readouterr().err
    assert ran == [], f"review slice(s) ran after the round failed: {ran}"
    assert rc != 0
    assert "skipped stage review:a" in err and "skipped stage review:b" in err, err
    assert "tail-review" in err and "failed" in err, err


def test_failed_round_skips_review_stages_when_the_stage_gate_itself_fails(
        tmp_path, monkeypatch, capsys):
    """Falsifier 1 read through the REAL failure return, not a stub of it:
    `_run_round_stage` returning a named non-zero rc (the parent dispatched,
    its manifest record read failed/timeout) must gate the same chain."""
    rc, ran, _buf = _drive(
        tmp_path, monkeypatch, ["review-a", "review-b"],
        lambda cmd, **kw: subprocess.CompletedProcess(
            cmd, 0, "spawned a00-test\n", ""), 0)
    err = capsys.readouterr().err
    # no manifest.json -> the record never reaches a terminal status; force the
    # deadline shape by making every clock read past the budget
    assert rc != 0
    assert ran == [], ran
    assert "review-a" in err and "review-b" in err, err


# ---------- falsifier 2: a HUNG round is a named stage failure -----------

def test_hung_round_dispatch_is_a_named_stage_failure_not_a_run_abort(
        tmp_path, monkeypatch, capsys):
    """FALSIFIER 2(a) — the dispatch subprocess itself never returns
    (`subprocess.run` raises TimeoutExpired). That must mark the round stage
    failed BY NAME and let the run end non-zero, NOT raise out of
    `run_workflow` as a run-level abort."""
    def hang(cmd, **kw):
        raise subprocess.TimeoutExpired(cmd, kw.get("timeout", 1))

    rc, ran, _buf = _drive(tmp_path, monkeypatch, ["review-a", "review-b"],
                           hang, 0)
    err = capsys.readouterr().err
    assert rc != 0, rc
    assert "round-parent" in err and "failed" in err, err
    assert ran == [], f"review stage(s) ran after a hung round: {ran}"


def test_hung_round_record_never_reaches_a_terminal_status(
        tmp_path, monkeypatch, capsys):
    """FALSIFIER 2(b) — the parent IS spawned but its manifest record never
    reads done/failed/timeout/stalled before the deadline. Named stage
    failure, chain gated, run ends non-zero."""
    root = tmp_path / ".agi"
    root.mkdir(exist_ok=True)
    (root / "manifest.json").write_text(json.dumps(
        # no branch: neither the record nor a done commit can ever reach a
        # terminal status, so the wait deadline is the only outcome left
        {"agents": [{"id": "a00-test", "status": "running"}]}),
        encoding="utf-8")

    def spawned(cmd, **kw):
        return subprocess.CompletedProcess(cmd, 0, "spawned a00-test\n", "")

    rc, ran, _buf = _drive(tmp_path, monkeypatch, ["review-a", "review-b"],
                           spawned, 0)
    err = capsys.readouterr().err
    assert rc != 0, rc
    assert "round-parent" in err and "failed" in err, err
    assert ran == [], ran


# ---------- falsifier 5: the success path is not the certificate ----------

def test_round_stage_failure_returns_are_named_not_swallowed(
        tmp_path, monkeypatch):
    """The certificate test at test_workflow.py `..._gates_on_branch_commit`
    only ever asserted `rc == 0`. Every non-zero return of `_run_round_stage`
    is asserted HERE, so the never-reached branch is no longer the proof that
    a failing round is named."""
    # (a) dispatch exits non-zero
    calls = []
    monkeypatch.setattr(_wf.subprocess, "run", lambda cmd, **kw: (
        calls.append(cmd) or subprocess.CompletedProcess(cmd, 3, "", "no")))
    assert _wf._run_round_stage(
        tmp_path, {}, {"target": "hypothesis:x", "iteration": "L1.01"},
        3) == (3, None)
    assert len(calls) == 1

    # (b) dispatch exits 0 but prints no `spawned <id>` — no retry, named
    monkeypatch.setattr(_wf.subprocess, "run", lambda cmd, **kw: (
        calls.append(cmd) or subprocess.CompletedProcess(cmd, 0, "ok\n", "")))
    assert _wf._run_round_stage(
        tmp_path, {}, {"target": "hypothesis:x", "iteration": "L1.01"},
        3) == (3, None)

    # (c) the dispatch itself hangs -> a named stage failure, not a raise
    def hang(cmd, **kw):
        raise subprocess.TimeoutExpired(cmd, kw.get("timeout", 3))
    monkeypatch.setattr(_wf.subprocess, "run", hang)
    assert _wf._run_round_stage(
        tmp_path, {}, {"target": "hypothesis:x", "iteration": "L1.01"},
        3) == (3, None)

    # (d) the record reads failed/timeout/stalled -> named
    root = tmp_path / ".agi"
    root.mkdir(exist_ok=True)
    monkeypatch.setattr(_wf._loc, "iteration_dir", lambda _r, _i: root)
    for status in ("failed", "timeout", "stalled"):
        (root / "manifest.json").write_text(json.dumps(
            {"agents": [{"id": "a00-test", "status": status}]}),
            encoding="utf-8")
        monkeypatch.setattr(_wf.subprocess, "run", lambda cmd, **kw: (
            subprocess.CompletedProcess(cmd, 0, "spawned a00-test\n", "")))
        monkeypatch.setattr(_wf.time, "sleep", lambda _s: None)
        assert _wf._run_round_stage(
            root, {}, {"target": "hypothesis:x", "iteration": "L1.01"},
            3) == (3, None), status
