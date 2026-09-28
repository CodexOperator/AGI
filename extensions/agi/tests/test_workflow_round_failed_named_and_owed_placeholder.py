"""R1 + R2 of hypothesis:a-round-stage-fails-closed-by-name-and-every-
inherited-review-stage-is-gated, on the bytes.

R1: `_run_round_stage` returns a bare rc and never touches the RunView, so a
    failed round read `pending` in the summary and in the tracking row. The
    run's own record must name it failed.
R2: a stage DECLARING `required_placeholders` that no run arg, no repeat item
    and no field of the return it chains from can supply is a named stage
    failure, never a blank `{placeholder}`. An UNDECLARED placeholder (an
    optional run arg like `{scratch}`) still renders '' — the `_SafeDict`
    contract test_workflow.py:216 depends on.
"""
import io
import json
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]  # .../tests/.. = repo root

import workflow as _wf
from workflow import render_stage_prompt, run_workflow

SCHEMA = {"type": "object", "properties": {"ok": {"type": "boolean"}},
          "required": ["ok"]}
ANSWER_SCHEMA = {"type": "object",
                 "properties": {"answer": {"type": "string"}},
                 "required": ["answer"]}


def _run(tmp_path, manifest, args, rc_of_round=0, prompts=None):
    wf = tmp_path / "extensions" / "agi" / "workflows"
    wf.mkdir(parents=True, exist_ok=True)
    (wf / "m.json").write_text(json.dumps(manifest), encoding="utf-8")
    loaded = _wf._load_manifest(tmp_path, "m")
    out = io.StringIO()

    def fake_pi(cfg, st, knobs, a, **kw):
        if prompts is not None:
            prompts.append(render_stage_prompt(st, a, prior=kw.get("prior")))
        if st.get("kind") == "round":
            return rc_of_round, None
        return 0, {"answer": "it is inert"} if st["label"] == "investigate" \
            else {"ok": True}

    m = pytest.MonkeyPatch()
    m.setattr(_wf, "_load_manifest", lambda r, k: loaded)
    m.setattr(_wf, "_stage_context", lambda *a, **k: "CTX")
    m.setattr(_wf.provisioning, "available", lambda root=None: False)
    m.setattr(_wf._loc, "shared_project_root", lambda r: tmp_path / "sessions")
    m.setattr(_wf._loc, "iteration_dir", lambda r, i: tmp_path / ".agi")
    m.setattr(_wf.time, "sleep", lambda s: None)
    m.setattr(_wf.subprocess, "run", lambda *a, **k: subprocess.CompletedProcess(
        a[0], rc_of_round, "", ""))
    m.setattr(_wf, "_run_stage_pi", fake_pi)
    try:
        rc = run_workflow(REPO / ".agi", "m", "pi", args, False, out=out)
    finally:
        m.undo()
    return rc, out.getvalue()


def test_failed_round_is_named_failed_in_the_runs_own_record(tmp_path):
    base = {"name": "base", "type": "review", "harness": "pi-free",
            "stages": [{"label": "review-a", "role": "kid", "prompt": "w",
                        "schema": SCHEMA, "model_hint": "sonnet"}]}
    manifest = {"name": "m", "extends": "base", "type": "review",
                "harness": "pi-free",
                "prelude": [{"kind": "round", "label": "round-parent",
                             "timeout_s": 1}],
                "stages": []}
    wf = tmp_path / "extensions" / "agi" / "workflows"
    wf.mkdir(parents=True, exist_ok=True)
    (wf / "base.json").write_text(json.dumps(base), encoding="utf-8")
    rc, text = _run(tmp_path, manifest,
                    {"target": "hypothesis:x", "iteration": "L1.01"},
                    rc_of_round=1)
    assert rc == 3
    assert "[stage] round-parent failed" in text
    assert "failed=1" in text
    # the inherited stage is still gated by name, never run
    assert "review-a — dependency 'round-parent' failed" in text


def test_required_placeholder_owed_by_nothing_is_a_named_failure(tmp_path):
    prompts: list = []
    manifest = {"name": "m", "type": "review", "harness": "pi-free",
                "stages": [
                    {"label": "investigate", "role": "kid", "prompt": "find",
                     "model_hint": "sonnet", "schema": ANSWER_SCHEMA},
                    {"label": "refute", "role": "kid", "model_hint": "sonnet",
                     "chained_from": "investigate", "schema": SCHEMA,
                     "required_placeholders": ["answerr"],
                     "prompt": "refute answer={answer} scratch={scratch}"}]}
    rc, text = _run(tmp_path, manifest, {"target": "x"}, prompts=prompts)
    assert rc == 3
    assert "[stage] refute failed" in text
    assert "['answerr']" in text
    # the refused stage never rendered a prompt at all
    assert not any("refute" in p for p in prompts)


def test_a_satisfied_placeholder_runs_and_an_optional_arg_still_blanks(
        tmp_path):
    prompts: list = []
    manifest = {"name": "m", "type": "review", "harness": "pi-free",
                "stages": [
                    {"label": "investigate", "role": "kid", "prompt": "find",
                     "model_hint": "sonnet", "schema": ANSWER_SCHEMA},
                    {"label": "refute", "role": "kid", "model_hint": "sonnet",
                     "chained_from": "investigate", "schema": SCHEMA,
                     "required_placeholders": ["answer"],
                     "prompt": "refute answer={answer} scratch={scratch}"}]}
    rc, _text = _run(tmp_path, manifest, {"target": "x"}, prompts=prompts)
    assert rc == 0
    assert prompts[-1] == "refute answer=it is inert scratch="
