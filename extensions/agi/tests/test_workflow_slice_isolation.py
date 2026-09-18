"""SM.105 — stage-slice isolation and the per-stage wall (workflow.py).

hypothesis:l4-a-failed-repeated-stage-slice-never-aborts-its-siblings-and-a-
manifest-stage-carries-its-own-timeout.

Measured on the jev trove-survey pi run 2026-09-18 02:2x-02:42Z: one 600 s
wall on critique:recipes-sdks aborted critique:pricing, the three panels and
the judge although the three read stages had succeeded (and the same
no-slice-isolation shape in merge-up-review). The claim built here:

  (1) a failed slice marks THAT slice failed and the loop CONTINUES: sibling
      slices and independent stages run to completion, only stages that
      depend on the failed slice are skipped BY NAME, and the run ends
      non-zero naming every failure and skip;
  (2) a stage that declares no `timeout_s` anywhere gets the new 3600 s
      default, and a stage-level `timeout_s` overrides it for that stage only;
  (3) OPTIONAL wall extension: a stage still PRODUCING at the wall (its
      declared progress file touched within `silence_s`, default 300) gets
      one extension of `extension_s` (default = its resolved budget) up to
      `max_extensions` (default 1) and the extension is recorded in the run
      status; a SILENT stage is killed at the wall; once max_extensions is
      reached the stage is killed and named.

Every timing test uses a 1-2 s wall and a stubbed `subprocess.run` — no real
minutes, no network, no tmux/systemd/crontab, no spawned agent.
"""
from __future__ import annotations

import io
import json
import os
import subprocess as _sp
import sys
from pathlib import Path
from unittest import mock

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BIN))

import workflow as _wf  # noqa: E402
from workflow import run_workflow  # noqa: E402

WF_DIR = REPO / "extensions" / "agi" / "workflows"

_OK = '{"ok": true}'
_SCHEMA = {"type": "object", "properties": {"ok": {"type": "boolean"}},
           "required": ["ok"]}


def _tmp_session_root(tmp_path_factory, wf_mod):
    """Redirect workflow's `<project>/sessions/` resolution into a temp dir so
    no test writes the live `.agi/sessions/` (same seam test_workflow uses)."""
    tmp = tmp_path_factory.mktemp("wf-isolation")
    saved = wf_mod._loc.shared_project_root
    wf_mod._loc.shared_project_root = lambda root: tmp
    return tmp, lambda: setattr(wf_mod._loc, "shared_project_root", saved)


def _drive(monkeypatch, manifest, args, fake_run, tmp_factory):
    """Run one live pi workflow against an injected manifest, subprocess
    stubbed, sessions redirected to tmp. Returns (rc, out_text, tmp_root)."""
    from unittest import mock as _mock
    tmp, restore = _tmp_session_root(tmp_factory, _wf)
    saved = _wf._load_manifest
    _wf._load_manifest = lambda repo, key: manifest
    monkeypatch.setattr(_wf.provisioning, "available", lambda root=None: False)
    try:
        buf = io.StringIO()
        with _mock.patch("subprocess.run", side_effect=fake_run):
            rc = run_workflow(REPO / ".agi", "review", "pi", args, False,
                              out=buf)
        return rc, buf.getvalue(), tmp
    finally:
        _wf._load_manifest = saved
        restore()


def _ctx_or_stage(cmd, **kw):
    """The context helpers (`_stage_context`) are plain subprocess calls with
    no `--provider`; only the pi stage dispatch carries it."""
    if "--provider" not in cmd:
        return _sp.CompletedProcess(cmd, 0, stdout="CTX", stderr="")
    return None


def _sl(label, prompt, **kw):
    st = {"label": label, "role": "kid", "prompt": prompt, "schema": _SCHEMA,
          "model_hint": "sonnet"}
    st.update(kw)
    return st


def _fanout_manifest(dep=True, indep=True):
    stages = [_sl("work", "WORK {key}",
                  repeat={"of": "sources", "label_template": "work:{key}"})]
    if dep:
        stages.append(_sl("dep", "DEP", chained_from="work"))
    if indep:
        stages.append(_sl("indep", "INDEP"))
    return {"name": "review", "type": "review", "script": "agi-review.js",
            "stages": stages}


# ---------- (1) a failed slice never aborts its siblings or independents ----

def test_failed_slice_leaves_siblings_and_independents_running(
        tmp_path_factory, monkeypatch, capsys):
    calls = []

    def fake_run(cmd, **kw):
        base = _ctx_or_stage(cmd, **kw)
        if base is not None:
            return base
        calls.append(cmd[-1])
        if "WORK a" in cmd[-1]:
            return _sp.CompletedProcess(cmd, 1, stdout="boom", stderr="")
        return _sp.CompletedProcess(cmd, 0, stdout=_OK, stderr="")

    rc, text, _ = _drive(monkeypatch, _fanout_manifest(), {"sources":
                         [{"key": "a"}, {"key": "b"}]}, fake_run,
                         tmp_path_factory)
    assert rc != 0, text
    assert "[stage] work:a failed" in text, text
    assert "[stage] work:b ok" in text, text
    assert "[stage] dep skipped" in text, text
    assert "[stage] indep ok" in text, text
    # dep was SKIPPED, never dispatched; three stages actually ran.
    assert len(calls) == 3, calls
    assert sorted(c.rstrip().splitlines()[-1] for c in calls) == [
        "INDEP", "WORK a", "WORK b"], calls
    err = capsys.readouterr().err
    assert "skipped stage dep (dependency 'work' failed)" in err, err


def test_slice_timeout_is_isolated_the_same_way(tmp_path_factory,
                                                monkeypatch):
    calls = []

    def fake_run(cmd, **kw):
        base = _ctx_or_stage(cmd, **kw)
        if base is not None:
            return base
        calls.append(cmd[-1])
        if "WORK a" in cmd[-1]:
            raise _sp.TimeoutExpired(cmd, 3600)
        return _sp.CompletedProcess(cmd, 0, stdout=_OK, stderr="")

    rc, text, _ = _drive(monkeypatch, _fanout_manifest(), {"sources":
                         [{"key": "a"}, {"key": "b"}]}, fake_run,
                         tmp_path_factory)
    assert rc == 2, text
    assert "[stage] work:a failed" in text, text
    assert "[stage] work:b ok" in text, text
    assert "[stage] dep skipped" in text, text
    assert "[stage] indep ok" in text, text


# ---------- (3) no failure -> order and outcomes unchanged -----------------

def test_no_failure_keeps_order_and_outcomes(tmp_path_factory, monkeypatch):
    def fake_run(cmd, **kw):
        base = _ctx_or_stage(cmd, **kw)
        if base is not None:
            return base
        return _sp.CompletedProcess(cmd, 0, stdout=_OK, stderr="")

    rc, text, _ = _drive(monkeypatch, _fanout_manifest(), {"sources":
                         [{"key": "a"}, {"key": "b"}]}, fake_run,
                         tmp_path_factory)
    assert rc == 0, text
    order = [ln.split()[1] for ln in text.splitlines()
             if ln.startswith("[stage]")]
    assert order == ["work:a", "work:b", "dep", "indep"], order
    assert all(ln.endswith(" ok") for ln in text.splitlines()
               if ln.startswith("[stage]")), text


# ---------- (4)/(6) the resolved wall per stage ----------------------------

def _seen_timeouts(monkeypatch, manifest, args, tmp_factory):
    seen = []

    def fake_run(cmd, **kw):
        base = _ctx_or_stage(cmd, **kw)
        if base is not None:
            return base
        seen.append(kw.get("timeout"))
        return _sp.CompletedProcess(cmd, 0, stdout=_OK, stderr="")

    rc, text, _ = _drive(monkeypatch, manifest, args, fake_run, tmp_factory)
    assert rc == 0, text
    return seen


def test_undeclared_wall_is_the_new_3600_default(tmp_path_factory,
                                                 monkeypatch):
    m = {"name": "review", "type": "review", "script": "s.js",
         "stages": [_sl("only", "ONLY")]}
    assert _seen_timeouts(monkeypatch, m, {}, tmp_path_factory) == [3600]


def test_stage_timeout_overrides_only_that_stage(tmp_path_factory,
                                                 monkeypatch):
    m = {"name": "review", "type": "review", "script": "s.js",
         "stages": [_sl("a", "A", timeout_s=5), _sl("b", "B")]}
    assert _seen_timeouts(monkeypatch, m, {}, tmp_path_factory) == [5, 3600]


# ---------- (5) merge-up-review: a red round leaves its sibling in place ---
# REGRESSION (SM.105 key-axis falsifier): the REAL manifest args name the
# slice `key`, never `window`. With a fixed window/slug probe every slice's
# _repeat_key was None, so `review:r1` failing skipped `verify:r2` too. This
# test uses the key-only shape on purpose and FAILS on that code.
def test_merge_up_review_red_round_leaves_sibling_slices(
        tmp_path_factory, monkeypatch):
    manifest = json.loads((WF_DIR / "merge-up-review.json").read_text())
    calls = []

    def fake_run(cmd, **kw):
        base = _ctx_or_stage(cmd, **kw)
        if base is not None:
            return base
        prompt = cmd[-1]
        calls.append(prompt)
        if "ADVERSARIAL VERIFY" in prompt:
            return _sp.CompletedProcess(
                cmd, 0, stdout=json.dumps({
                    "round": "r2", "verdicts": [], "missed": [],
                    "final_recommendation": "accept", "summary": "s"}),
                stderr="")
        if "ROUND r1" in prompt:
            return _sp.CompletedProcess(cmd, 1, stdout="boom", stderr="")
        return _sp.CompletedProcess(
            cmd, 0, stdout=json.dumps({
                "round": "r2", "verdict_recommendation": "accept",
                "conjuncts": [], "defects": [], "defects_summary": "NONE",
                "tests_run": "t", "node_checks": "n", "prime_step": "p"}),
            stderr="")

    args = {"rounds": [
        {"key": "r1", "hypothesis": "h1",
         "experiments": "e1", "files": "f1", "focus": "x1",
         "merge_up": "m1", "old_tip": "o1", "new_tip": "n1"},
        {"key": "r2", "hypothesis": "h2",
         "experiments": "e2", "files": "f2", "focus": "x2",
         "merge_up": "m2", "old_tip": "o2", "new_tip": "n2"}]}
    rc, text, tmp = _drive(monkeypatch, manifest, args, fake_run,
                           tmp_path_factory)
    assert rc != 0, text
    assert "[stage] review:r1 failed" in text, text
    assert "[stage] review:r2 ok" in text, text
    assert "[stage] verify:r1 skipped" in text, text
    assert "[stage] verify:r2 ok" in text, text
    # the sibling slice's validated verdict is written, not lost to the red one
    hits = list((tmp / "sessions" / "workflows" / "runs").glob(
        "*/review_r2.json"))
    assert len(hits) == 1, hits
    assert json.loads(hits[0].read_text())["verdict_recommendation"] == "accept"


# ---------- (7)/(8)/(9) the optional wall extension ------------------------

def _row(tmp):
    path = tmp / "sessions" / "workflows" / "review.jsonl"
    lines = path.read_text(encoding="utf-8").splitlines()
    return json.loads(lines[-1])


def test_producing_stage_gets_one_extension_then_completes(
        tmp_path_factory, monkeypatch):
    prog = tmp_path_factory.mktemp("prog") / "out.txt"
    prog.write_text("bytes")
    os.utime(prog, None)
    m = {"name": "review", "type": "review", "script": "s.js",
         "stages": [_sl("only", "ONLY", timeout_s=1, extension_s=1,
                        max_extensions=1, progress_file=str(prog))]}
    calls = []

    def fake_run(cmd, **kw):
        base = _ctx_or_stage(cmd, **kw)
        if base is not None:
            return base
        calls.append(kw.get("timeout"))
        if len(calls) == 1:
            raise _sp.TimeoutExpired(cmd, kw.get("timeout"))
        return _sp.CompletedProcess(cmd, 0, stdout=_OK, stderr="")

    rc, text, tmp = _drive(monkeypatch, m, {}, fake_run, tmp_path_factory)
    assert rc == 0, text
    assert calls == [1, 1], calls
    assert "[extension] only +1s (n=1)" in text, text
    assert "[stage] only ok" in text, text
    row = _row(tmp)
    assert row["extensions"]["only"] == [{"n": 1, "extension_s": 1}], row


def test_silent_stage_is_killed_at_the_wall(tmp_path_factory, monkeypatch):
    m = {"name": "review", "type": "review", "script": "s.js",
         "stages": [_sl("only", "ONLY", timeout_s=1, extension_s=5)]}
    calls = []

    def fake_run(cmd, **kw):
        base = _ctx_or_stage(cmd, **kw)
        if base is not None:
            return base
        calls.append(kw.get("timeout"))
        raise _sp.TimeoutExpired(cmd, kw.get("timeout"))

    rc, text, tmp = _drive(monkeypatch, m, {}, fake_run, tmp_path_factory)
    assert rc == 2, text
    assert calls == [1], calls          # no extension on a silent stage
    assert "[stage] only failed" in text, text
    assert "[extension]" not in text, text
    assert _row(tmp)["failed"] == 1


def test_max_extensions_reached_still_kills_and_names(
        tmp_path_factory, monkeypatch):
    prog = tmp_path_factory.mktemp("prog2") / "out.txt"
    prog.write_text("bytes")
    os.utime(prog, None)
    m = {"name": "review", "type": "review", "script": "s.js",
         "stages": [_sl("only", "ONLY", timeout_s=1, extension_s=1,
                        max_extensions=1, progress_file=str(prog))]}
    calls = []

    def fake_run(cmd, **kw):
        base = _ctx_or_stage(cmd, **kw)
        if base is not None:
            return base
        calls.append(kw.get("timeout"))
        raise _sp.TimeoutExpired(cmd, kw.get("timeout"))

    rc, text, tmp = _drive(monkeypatch, m, {}, fake_run, tmp_path_factory)
    assert rc == 2, text
    assert calls == [1, 1], calls       # exactly one extension, then killed
    assert "[extension] only +1s (n=1)" in text, text
    assert "[stage] only failed" in text, text
    row = _row(tmp)
    assert row["failed"] == 1
    assert row["extensions"]["only"] == [{"n": 1, "extension_s": 1}], row
