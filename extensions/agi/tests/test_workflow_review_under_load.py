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

import io
import json
import subprocess as _sp
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
TST = Path(__file__).resolve().parents[0]      # tests/ (namespace pkg)
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(TST))

from test_workflow_slice_isolation import (  # noqa: E402  (reused, never copied)
    REPO, WF_DIR, _ctx_or_stage, _drive, _fanout_manifest, _seen_timeouts, _sl,
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


# ---------- (5) the context-build budget comes from the manifest -----------
# The two `_stage_context` reads (viewport.py --emit llm, brief.py head) were
# hard `timeout=60`; at box load 40-51 they took >60 s and every verify stage
# of merge-up-review died `context-build-timeout after 60 s`. The budget is now
# `context_timeout_s`, resolved stage > manifest > the 60 s pre-fix literal.

def _context_manifest(context_timeout_s=None, stage_context_timeout=None):
    st = _sl("only", "ONLY")
    if stage_context_timeout is not None:
        st["context_timeout_s"] = stage_context_timeout
    m = {"name": "review", "type": "review", "script": "s.js",
         "stages": [st]}
    if context_timeout_s is not None:
        m["context_timeout_s"] = context_timeout_s
    return m


def _seen_context_timeouts(monkeypatch, manifest, tmp_factory):
    """Drive a live pi run with subprocess stubbed; return (rc, timeouts, out)
    where `timeouts` are the `timeout=` kwarg of each CONTEXT call in order
    (viewport, then brief). The stage dispatch is not recorded, and neither is
    any OTHER non-`--provider` subprocess (`mem_cap.systemd_run_usable()`
    probes with `systemd-run ... timeout=30` on its first call in a process)."""
    seen = []

    def _is_context(cmd):
        return any("viewport.py" in str(a) or "brief.py" in str(a)
                   for a in cmd)

    def fake_run(cmd, **kw):
        base = _ctx_or_stage(cmd, **kw)
        if base is not None and _is_context(cmd):
            seen.append(kw.get("timeout"))
        if base is not None:
            return base
        return _sp.CompletedProcess(cmd, 0, stdout='{"ok": true}', stderr="")

    rc, text, _ = _drive(monkeypatch, manifest, {}, fake_run, tmp_factory)
    return rc, seen, text


def test_manifest_context_timeout_s_reaches_the_context_build(
        tmp_path_factory, monkeypatch):
    """RED on the pre-fix bytes: both context subprocesses were hard 60, so a
    manifest `context_timeout_s: 300` was silently ignored and the stage died
    at 60 s under load."""
    rc, seen, text = _seen_context_timeouts(
        monkeypatch, _context_manifest(context_timeout_s=300),
        tmp_path_factory)
    assert rc == 0, text
    assert seen == [300, 300], seen   # viewport --emit llm, then brief.py head


def test_bad_context_timeout_s_refuses_by_name_before_any_stage(
        tmp_path_factory, monkeypatch, capsys):
    """0, negative and non-numeric are REFUSED BY NAME (rc 5) before any
    stage is dispatched — the same definition of `0` the stage wall owns."""
    for bad in (0, -1, "300"):
        rc, seen, text = _seen_context_timeouts(
            monkeypatch, _context_manifest(context_timeout_s=bad),
            tmp_path_factory)
        assert rc == 5, (bad, rc, text)
        assert seen == [], (bad, seen)
        err = capsys.readouterr().err
        assert "context_timeout_s" in err and "only" in err, (bad, err)


def test_no_context_timeout_keeps_the_60_default(tmp_path_factory,
                                                 monkeypatch):
    """A manifest declaring no `context_timeout_s` anywhere keeps the pre-fix
    60 s — the default did NOT ride the stage wall's 3600."""
    rc, seen, text = _seen_context_timeouts(
        monkeypatch, _context_manifest(), tmp_path_factory)
    assert rc == 0, text
    assert seen == [60, 60], seen


def test_stage_context_timeout_beats_manifest(tmp_path_factory, monkeypatch):
    """Presence, not truthiness: a stage-level `context_timeout_s: 300` wins
    over the manifest's 60 and reaches BOTH context reads."""
    rc, seen, text = _seen_context_timeouts(
        monkeypatch,
        _context_manifest(context_timeout_s=60, stage_context_timeout=300),
        tmp_path_factory)
    assert rc == 0, text
    assert seen == [300, 300], seen


# ---------- (6) a fractional budget never floors to zero -------------------
# A 0<v<1 declared budget is a POSITIVE number, so it clears the refusal, but
# `int(0.5)` truncates it to 0 and `subprocess.run(timeout=0)` kills the stage
# instantly on the pre-fix bytes. Every truncation site floors at ONE second.

def test_fractional_context_budget_never_floors_to_zero(tmp_path_factory,
                                                        monkeypatch):
    """RED on the pre-fix bytes: int(0.5) == 0, so the context build was
    handed timeout=0 instead of a positive budget."""
    assert _wf._resolve_context_timeout(
        {"label": "only"}, {"context_timeout_s": 0.5}) >= 1
    rc, seen, text = _seen_context_timeouts(
        monkeypatch, _context_manifest(context_timeout_s=0.5),
        tmp_path_factory)
    assert rc == 0, text
    assert seen == [1, 1], seen


def test_fractional_budget_under_load_never_floors_to_zero(monkeypatch):
    """The load-scaled truncation sites floor at 1 too: 0.5*(1+0.5*0)=0.5,
    which `int()` made 0 on the pre-fix bytes."""
    monkeypatch.setattr(_wf, "_current_load", lambda: 0.0)
    assert _wf._resolve_context_timeout(
        {"label": "only", "context_timeout_s": 0.5, "load_factor": 0.5},
        {}) == 1
    assert _wf._resolve_stage_timeout(
        {"label": "only", "timeout_s": 0.5, "load_factor": 0.5}, {}) == 1


def test_bool_context_timeout_refused_and_no_stage_dispatched(
        tmp_path_factory, monkeypatch):
    """A declared `True` is a bool, not a positive number (bool is an int
    subclass, so `True <= 0` is False): refused by name before ANY subprocess
    runs — no context build, no stage dispatch, no key spent."""
    calls = []

    def fake_run(cmd, **kw):
        calls.append(cmd)
        return _sp.CompletedProcess(cmd, 0, stdout="", stderr="")

    rc, text, _ = _drive(monkeypatch, _context_manifest(context_timeout_s=True),
                         {}, fake_run, tmp_path_factory)
    assert rc == 5, text
    assert calls == [], calls


def test_dry_run_refuses_a_bad_context_timeout_with_rc_5(monkeypatch):
    """`--dry-run` and the live run agree: the budget is resolved BEFORE the
    dry-run return, so a bad context budget is rc 5 with no `[dispatch]` line
    and no subprocess at all."""
    from unittest import mock as _mock
    saved = _wf._load_manifest
    _wf._load_manifest = lambda repo, key: _context_manifest(
        context_timeout_s=0)
    monkeypatch.setattr(_wf.provisioning, "available", lambda root=None: False)
    calls = []
    buf = io.StringIO()
    try:
        with _mock.patch("subprocess.run",
                         side_effect=lambda cmd, **kw: calls.append(cmd)):
            rc = _wf.run_workflow(REPO / ".agi", "review", "pi", {}, True,
                                  out=buf)
    finally:
        _wf._load_manifest = saved
    text = buf.getvalue()
    assert rc == 5, text
    # `_repo_root` probes git via subprocess; what must NOT happen is a stage
    # dispatch line, so assert on the output, not on all subprocess calls.
    assert "[dispatch]" not in text, text
