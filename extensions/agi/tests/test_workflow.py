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