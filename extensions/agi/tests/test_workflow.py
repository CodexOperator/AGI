"""Tests for bin/workflow.py — the harness-agnostic workflow runner
(hypothesis:l3w4-workflows-config-maxxed).

Locks the PROPERTY the hypothesis asserts: every knob reads from the
`.agi/config.json workflows.<name>` row with per-run args overriding and never
a hard-coded literal, the `.claude/workflows` symlinks resolve into the repo
tree, the pi-harness dry-run prints one dispatch per stage, a returned stage
value is validated against its JSON schema, and the stage manifests match the
stages the .js Claude Code scripts declare. Any of these breaking is the
config-maxxed contract breaking.
"""
from __future__ import annotations

import io
import os
import re
import sys
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"
REPO = Path(__file__).resolve().parents[3]  # .../tests/.. = repo root
sys.path.insert(0, str(BIN))

import workflow  # noqa: E402
from workflow import _resolve_knobs, validate_return  # noqa: E402

WF_DIR = REPO / "extensions" / "agi" / "workflows"
CLAUDE_WF = REPO / ".claude" / "workflows"


# ---------- config row overrides script defaults; args override config ------

def test_config_row_overrides_script_defaults():
    "# builtin stage hint < config row < per-run args"
    stage = {"model_hint": "sonnet", "effort_hint": "low"}
    cfg = {"model": "opus", "effort": "high"}
    k = _resolve_knobs(stage, cfg, {})
    assert k == {"model": "opus", "effort": "high"}, k  # config row wins


def test_args_override_config_row_and_hint():
    stage = {"model_hint": "sonnet", "effort_hint": "low"}
    cfg = {"model": "opus", "effort": "high"}
    k = _resolve_knobs(stage, cfg, {"model": "glm", "effort": "max"})
    assert k == {"model": "glm", "effort": "max"}, k  # args top


def test_missing_row_falls_back_to_hint_then_builtin_default():
    assert _resolve_knobs({"effort_hint": "low"}, {}, {})["effort"] == "low"
    assert _resolve_knobs({}, {}, {}) == {
        "model": workflow._DEFAULT_MODEL,
        "effort": workflow._DEFAULT_EFFORT,
    }


# ---------- config maxxed end-to-end: row flips the model, no script edit ---

def test_config_flip_changes_dispatched_model():
    import json
    from workflow import run_workflow
    buf = io.StringIO()
    # run_workflow reads the REAL config row (review.model = sonnet)
    rc = run_workflow(REPO / ".agi", "review", "pi", {}, True, out=buf)
    assert rc == 0
    txt = buf.getvalue()
    assert "model=sonnet" in txt, txt
    # a flipped config row must change the resolved model WITHOUT touching the
    # stage manifest — monkeypatch the config loader to prove the knob path.
    saved = workflow._load_config
    try:
        workflow._load_config = lambda root: {
            "workflows": {"review": {"model": "glm-flash", "effort": "low"}}
        }
        buf2 = io.StringIO()
        rc2 = run_workflow(REPO / ".agi", "review", "pi", {}, True, out=buf2)
        assert rc2 == 0
        assert "model=glm-flash" in buf2.getvalue(), buf2.getvalue()
        assert "model=sonnet" not in buf2.getvalue(), buf2.getvalue()
    finally:
        workflow._load_config = saved


# ---------- symlinks resolve to repo workflow files -------------------------

def test_named_workflow_symlinks_resolve_to_repo_files():
    for script in ("agi-round-review.js", "agi-brief-drafting.js"):
        link = CLAUDE_WF / script
        assert link.is_symlink(), f"{link} is not a symlink"
        target = link.resolve()
        assert target.is_file(), f"{target} missing"
        assert str(target).startswith(str(WF_DIR)), target


# ---------- pi-harness dry-run prints one dispatch per stage ---------------

def test_runner_pi_harness_dry_run_prints_one_dispatch_per_stage():
    from workflow import run_workflow
    buf = io.StringIO()
    rc = run_workflow(REPO / ".agi", "review", "pi", {"targets": [
        {"window": "t1", "hyp": "h1"}, {"window": "t2", "hyp": "h2"}]}, True, out=buf)
    assert rc == 0
    lines = [l for l in buf.getvalue().splitlines() if l.startswith("[dispatch]")]
    assert len(lines) == 3, lines  # global-checks + review:t1 + review:t2
    assert "model=sonnet" in lines[0], lines
    assert any("global-checks" in l for l in lines), lines
    assert any("review:t1" in l for l in lines), lines
    assert any("review:t2" in l for l in lines), lines


# ---------- stage return is schema-validated -------------------------------

def test_stage_return_is_schema_validated():
    schema = {"type": "object", "properties": {
        "slug": {"type": "string"},
        "verdict": {"type": "string"},
    }, "required": ["slug", "verdict"]}
    assert validate_return(schema, {"slug": "x", "verdict": "proved"}) == []
    errs = validate_return(schema, {"slug": "x"})          # missing required
    assert errs, "missing required field must be reported"
    assert any("verdict" in e for e in errs), errs
    errs2 = validate_return(schema, {"slug": 3, "verdict": "x"})  # wrong type
    assert errs2
    assert validate_return(None, {"anything": 1}) == []    # no schema -> valid




# ---------- pi harness LIVE path: prompt render + JSON parse + validate -----

from workflow import (  # noqa: E402
    render_stage_prompt, _parse_last_json, _effort_to_thinking,
    _run_stage_pi,
)


def test_render_stage_prompt_uses_repeat_item_fields_over_args():
    from workflow import _expand_stages
    manifest = {"stages": [{
        "label": "draft", "repeat": {"of": "briefs",
        "label_template": "draft:{slug}"},
        "prompt": "write {scratch}/{slug}.md parent={parent} scope={scope}",
    }]}
    stages = _expand_stages(manifest, {"scratch": "/tmp/S", "briefs": [
        {"slug": "a", "parent": "goal:x", "scope": "s1"},
        {"slug": "b", "parent": "goal:y", "scope": "s2"},
    ]})
    assert len(stages) == 2, stages
    st = stages[0]
    assert st["label"] == "draft:a"
    assert st["_repeat_key"] == "a"
    out = render_stage_prompt(st, {"scratch": "/tmp/S"})
    assert out == "write /tmp/S/a.md parent=goal:x scope=s1", out
    assert render_stage_prompt(stages[1], {"scratch": "/tmp/S"}) \
        == "write /tmp/S/b.md parent=goal:y scope=s2"


def test_render_stage_prompt_missing_field_and_json_braces_pass_through():
    # JSON schema braces in a prompt must survive rendering untouched; a
    # missing `{word}` placeholder stays literal (str.format_map would blow up
    # on the schema braces, which is the original bug).
    st = {"label": "critic",
          "prompt": 'under {scratch}/ and {optional} schema {"a":1}'}
    assert render_stage_prompt(st, {"scratch": "/tmp"}) == \
        'under /tmp/ and  schema {"a":1}'  # {optional} absent -> ""; JSON braces intact


def test_render_stage_prompt_requires_prompt_text():
    # The stub ran stages with no prompt at all; a pi run must refuse loudly.
    st = {"label": "x", "schema": {}}
    try:
        render_stage_prompt(st, {})
        raise AssertionError("expected ValueError for a prompt-less stage")
    except ValueError as exc:
        assert "no 'prompt'" in str(exc)


def test_parse_last_json_tolerates_preamble_and_trailing_glue():
    assert _parse_last_json("ok here\n{\"slug\": \"x\", \"v\": 1}\n thanks") == \
        {"slug": "x", "v": 1}
    try:
        _parse_last_json("no braces here")
        raise AssertionError("expected ValueError")
    except ValueError:
        pass


def test_effort_to_thinking_map():
    assert _effort_to_thinking("max") == "high"
    assert _effort_to_thinking("high") == "high"
    assert _effort_to_thinking("low") == "low"
    assert _effort_to_thinking("medium") == "medium"
    assert _effort_to_thinking(None) == "medium"


def test_run_stage_pi_passes_resolved_model_and_rendered_prompt():
    """The live pi path must hand the stage's RESOLVED knob and its rendered
    prompt to the pi binary — the two things the stub swallowed."""
    import subprocess as _sp
    from unittest import mock
    captured = {}

    def fake_run(cmd, **kw):
        captured["cmd"] = cmd
        captured["env"] = kw.get("env")
        return _sp.CompletedProcess(
            cmd, 0,
            stdout='{"slug": "a", "v": 1}', stderr="")

    st = {"label": "draft:a", "role": "drafter",
          "prompt": "write {scratch}/{slug}.md",
          "_repeat_item": {"slug": "a"},
          "schema": {"type": "object", "properties": {"slug": {"type": "string"}},
                      "required": ["slug"]}}
    cfg = {"harnesses": {"pi": {"bin": "/bin/fakepi", "provider": "openrouter",
                                "thinking": "medium"}}}
    with mock.patch("subprocess.run", side_effect=fake_run):
        rc = _run_stage_pi(cfg, st, {"draft:a": {"model": "glm",
                                                   "effort": "max"}},
                           {"scratch": "/tmp/S"})
    assert rc == 0
    cmd = captured["cmd"]
    assert "/bin/fakepi" in cmd, cmd
    assert "--provider" in cmd and "openrouter" in cmd, cmd
    assert "--model" in cmd and "glm" in cmd, cmd
    assert "--thinking" in cmd and "high" in cmd, cmd  # effort max -> high
    # the rendered per-item prompt reached the binary (the stub dropped it)
    assert "write /tmp/S/a.md" in cmd, cmd
    # the pi child env must not inherit Claude subscription credentials
    env = captured["env"] or {}
    assert "ANTHROPIC_API_KEY" not in env, env


def test_run_stage_pi_rejects_schema_violating_return():
    import subprocess as _sp
    from unittest import mock

    def fake_run(cmd, **kw):
        return _sp.CompletedProcess(cmd, 0, stdout="{\"slug\": 123}", stderr="")

    st = {"label": "draft:a", "prompt": "p", "_repeat_item": {"slug": "a"},
          "schema": {"type": "object", "properties": {"slug": {"type": "string"}},
                      "required": ["slug"]}}
    cfg = {"harnesses": {"pi": {}}}
    with mock.patch("subprocess.run", side_effect=fake_run):
        rc = _run_stage_pi(cfg, st, {"draft:a": {"model": "m", "effort": "x"}}, {})
    assert rc == 5, rc  # schema-violating JSON -> non-zero, stage fails

# ---------- stage manifests match the .js Claude Code scripts ---------------

def test_review_and_drafting_stage_json_matches_js_prompts():
    js = (WF_DIR / "agi-round-review.js").read_text(encoding="utf-8")
    manifest = workflow._load_manifest(REPO, "review")
    js_labels = re.findall(r"label:\s*['`]([^'`$]+)", js)
    for stage in manifest["stages"]:
        base = stage["label"]
        assert any(base in jl for jl in js_labels), (base, js_labels)

    jsd = (WF_DIR / "agi-brief-drafting.js").read_text(encoding="utf-8")
    m2 = workflow._load_manifest(REPO, "drafting")
    for stage in m2["stages"]:
        base = stage["label"]
        assert base in jsd or base + ":" in jsd, (base,)
    assert m2["script"] == "agi-brief-drafting.js"