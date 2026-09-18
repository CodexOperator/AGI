"""SM.114 — a merge-up-review stage survives load (workflow.py).

hypothesis:l4-a-review-stage-survives-load-its-wall-scales-or-its-rounds-shrink-
and-a-context-build-timeout-fails-the-stage-by-name-never-the-runner.

Branch taken: LOAD-SCALING (not round-splitting). The review/verify stages of
`merge-up-review.json` carry an opt-in `load_factor`, resolved in ONE place
(`_resolve_stage_timeout`) from an injectable load seam (`_current_load`),
capped at `_LOAD_CAP_MULT` x the declared budget and a byte-for-byte no-op when
absent. A context build that raises (`RuntimeError` / `subprocess.TimeoutExpired`)
marks THAT slice failed by name and the loop continues under SM.105 isolation.

Every test rides the EXACT seam already in `test_workflow_slice_isolation.py`
(`_drive`, `_ctx_or_stage`, a patched `subprocess.run`) — no second harness —
and no test sleeps, spawns, or reads the real box's load.
"""
from __future__ import annotations

import json
import subprocess as _sp
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
TST = Path(__file__).resolve().parents[0]      # tests/ (namespace pkg)
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(TST))

from test_workflow_slice_isolation import (  # noqa: E402  (reused, never copied)
    WF_DIR, _ctx_or_stage, _drive, _fanout_manifest, _seen_timeouts, _sl,
)

import workflow as _wf  # noqa: E402


# ---------- (1) a context-build timeout fails THAT slice by name -----------

def test_context_build_timeout_fails_the_slice_and_siblings_run(
        tmp_path_factory, monkeypatch):
    contexts = {"n": 0}

    def fake_run(cmd, **kw):
        base = _ctx_or_stage(cmd, **kw)
        if base is not None:
            contexts["n"] += 1
            if contexts["n"] == 1:          # work:a's viewport --emit llm
                raise _sp.TimeoutExpired(cmd, 60)
            return base
        return _sp.CompletedProcess(cmd, 0, stdout='{"ok": true}', stderr="")

    rc, text, _ = _drive(monkeypatch, _fanout_manifest(), {"sources":
                         [{"key": "a"}, {"key": "b"}]}, fake_run,
                         tmp_path_factory)
    # Non-zero and NO uncaught exception reached the caller.
    assert rc == 3, text
    assert "[stage] work:a failed" in text, text
    assert "context-build-timeout" in text, text
    assert "[stage] work:b ok" in text, text
    assert "[stage] dep skipped" in text, text
    assert "[stage] indep ok" in text, text


def test_context_build_runtime_error_names_the_kind(
        tmp_path_factory, monkeypatch):
    def fake_run(cmd, **kw):
        base = _ctx_or_stage(cmd, **kw)
        if base is not None:
            return _sp.CompletedProcess(cmd, 1, stdout="", stderr="viewport died")
        return base

    m = {"name": "review", "type": "review", "script": "s.js",
         "stages": [_sl("only", "ONLY")]}
    rc, text, _ = _drive(monkeypatch, m, {}, fake_run, tmp_path_factory)
    assert rc == 3, text
    assert "[stage] only failed" in text, text
    assert "context-build-failed" in text, text
    assert "viewport died" in text, text


# ---------- (2) load_factor scales from the STUBBED load source ------------

def test_load_factor_scales_and_caps_the_resolved_wall(monkeypatch):
    st = _sl("only", "ONLY", timeout_s=100, load_factor=0.5)
    monkeypatch.setattr(_wf, "_current_load", lambda: 1.0)
    assert _wf._resolve_stage_timeout(st, {}) == 150
    monkeypatch.setattr(_wf, "_current_load", lambda: 4.0)
    # 100 * (1 + 0.5*4) = 300 -> capped at 2x = 200
    assert _wf._resolve_stage_timeout(st, {}) == 200


def test_merge_up_review_stages_scale_past_1800_under_load(monkeypatch):
    manifest = json.loads((WF_DIR / "merge-up-review.json").read_text())
    for st in manifest["stages"]:
        monkeypatch.setattr(_wf, "_current_load", lambda: 0.0)
        assert _wf._resolve_stage_timeout(st, manifest) == 1800, st["label"]
        monkeypatch.setattr(_wf, "_current_load", lambda: 4.0)
        assert _wf._resolve_stage_timeout(st, manifest) == 3600, st["label"]


# ---------- (3) an anchored 3-round manifest resolves PER SLICE ------------

def test_each_anchored_round_slice_resolves_its_own_wall(
        tmp_path_factory, monkeypatch):
    loads = iter([1.0, 2.0, 4.0])
    monkeypatch.setattr(_wf, "_current_load", lambda: next(loads))
    m = {"name": "review", "type": "review", "script": "s.js",
         "stages": [_sl("review", "REVIEW {key}",
                        repeat={"of": "rounds",
                                "label_template": "review:{key}"},
                        timeout_s=100, load_factor=0.5)]}
    seen = _seen_timeouts(monkeypatch, m, {"rounds": [
        {"key": "r1"}, {"key": "r2"}, {"key": "r3"}]}, tmp_path_factory)
    # 100*(1+0.5*1)=150, 100*(1+0.5*2)=200, 100*(1+0.5*4)=300 -> cap 200
    assert seen == [150, 200, 200], seen


# ---------- (4) no load_factor -> byte-for-byte today ---------------------

def test_no_load_factor_never_reads_the_load_seam(
        tmp_path_factory, monkeypatch):
    called = []
    monkeypatch.setattr(_wf, "_current_load",
                        lambda: called.append(1) or 99.0)
    m = {"name": "review", "type": "review", "script": "s.js",
         "timeout_s": 77,
         "stages": [_sl("a", "A", timeout_s=5), _sl("b", "B"),
                    _sl("r", "R", repeat={"of": "rounds",
                         "label_template": "r:{key}"})]}
    seen = _seen_timeouts(monkeypatch, m, {"rounds": [{"key": "1"},
                                                     {"key": "2"}]},
                          tmp_path_factory)
    assert seen == [5, 77, 77, 77], seen
    assert called == [], "absent load_factor must not touch the load seam"
