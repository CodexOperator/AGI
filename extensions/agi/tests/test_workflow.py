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
import json
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


def test_missing_row_falls_back_to_hint_then_raises_on_no_model():
    assert _resolve_knobs({"model_hint": "m", "effort_hint": "low"}, {}, {})["effort"] == "low"
    # No builtin model default (hypothesis:l3-workflow-model-crosses-harness-
    # namespace) — a stage with nothing to say about its model must refuse,
    # not silently spend on a name nobody chose.
    try:
        _resolve_knobs({}, {}, {})
        raise AssertionError("expected ValueError for a stage with no model")
    except ValueError as exc:
        assert "no model resolved" in str(exc)


# ---------- config maxxed end-to-end: row flips the model, no script edit ---

def test_config_flip_changes_dispatched_model():
    """The pi harness resolves its model from harnesses.pi.models, NOT from
    workflows.review.model — that field is claude-code's namespace
    (hypothesis:l3-workflow-model-crosses-harness-namespace). Flipping
    workflows.review.model must NOT move the dispatched pi model; flipping
    harnesses.pi.models must."""
    from workflow import run_workflow
    buf = io.StringIO()
    rc = run_workflow(REPO / ".agi", "review", "pi", {}, True, out=buf)
    assert rc == 0
    txt = buf.getvalue()
    assert "model=sonnet" not in txt, txt  # never a claude-code alias on pi
    assert "model=~deepseek/deepseek-v4-flash-latest" in txt, txt
    saved = workflow._load_config
    try:
        # flipping the harness-agnostic row does nothing on the pi path
        workflow._load_config = lambda root: {
            "workflows": {"review": {"model": "glm-flash", "effort": "low"}},
            "harnesses": {"pi": {"provider": "openrouter",
                                  "models": {"kid": "z-ai/glm-flash-latest"}}},
        }
        buf2 = io.StringIO()
        rc2 = run_workflow(REPO / ".agi", "review", "pi", {}, True, out=buf2)
        assert rc2 == 0
        assert "model=glm-flash" not in buf2.getvalue(), buf2.getvalue()
        # flipping harnesses.pi.models DOES move the dispatched model
        assert "model=z-ai/glm-flash-latest" in buf2.getvalue(), buf2.getvalue()
    finally:
        workflow._load_config = saved


def test_pi_model_refuses_claude_code_alias_before_spawn():
    """FAIL CLOSED: a model with no 'provider/name' shape handed to the
    openrouter provider must refuse before any dispatch line prints, naming
    both the model and the provider."""
    from workflow import run_workflow
    saved = workflow._load_config
    try:
        workflow._load_config = lambda root: {
            "workflows": {"review": {}},
            "harnesses": {"pi": {"provider": "openrouter",
                                  "models": {"kid": "sonnet"}}},
        }
        buf = io.StringIO()
        try:
            run_workflow(REPO / ".agi", "review", "pi", {}, True, out=buf)
            raise AssertionError("expected ValueError for a bare alias on openrouter")
        except ValueError as exc:
            assert "sonnet" in str(exc) and "openrouter" in str(exc), exc
        assert "[dispatch]" not in buf.getvalue(), buf.getvalue()
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
    # pi harness: model comes from harnesses.pi.models, never workflows.review
    assert "model=sonnet" not in lines[0], lines
    assert "model=~deepseek/deepseek-v4-flash-latest" in lines[0], lines
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


# ---------- unified route: register / list / the registry invariant ---------
# hypothesis:l3-workflows-unified-route. Every agi-*.js must have a sibling
# <name>.json and every manifest must name only stages its script implements.
# Validation is run against an explicit tmp workflows dir so the live repo
# (where deep-search is mid-build) never makes these flaky.


def _write_registry_pair(wf: Path, key: str, script_text: str, stages: list):
    (wf / f"agi-{key}.js").write_text(script_text, encoding="utf-8")
    (wf / f"{key}.json").write_text(
        json.dumps({"name": key, "script": f"agi-{key}.js", "stages": stages},
                   indent=2) + "\n", encoding="utf-8")


def test_registry_flag_script_without_sibling_manifest(tmp_path):
    """RED direction 1: an agi-*.js with no sibling <name>.json is an error."""
    from workflow import validate_registry
    wf = tmp_path
    (wf / "agi-orphan.js").write_text(
        "phase('Orphan')\n"
        "await agent('x', {label: 'orphan'})\n", encoding="utf-8")
    buf = io.StringIO()
    rc = validate_registry(REPO / ".agi", wf=wf, out=buf)
    assert rc == 1, buf.getvalue()
    assert "agi-orphan.js has no manifest naming it" in buf.getvalue()
    # direction 2 must stay quiet: a lone manifest with a missing script too
    (wf / "ghost.json").write_text(
        json.dumps({"name": "ghost", "script": "agi-ghost.js", "stages": []}),
        encoding="utf-8")
    buf2 = io.StringIO()
    rc2 = validate_registry(REPO / ".agi", wf=wf, out=buf2)
    assert rc2 == 1, buf2.getvalue()
    assert "agi-ghost.js" in buf2.getvalue()


def test_registry_flag_manifest_naming_unimplemented_stage(tmp_path):
    """RED direction 2: a manifest naming a stage the script does not
    implement is an error — the script is the source of truth."""
    from workflow import validate_registry
    wf = tmp_path
    _write_registry_pair(wf, "good",
                         "phase('A')\nawait agent('x', {label: 'a'})\n",
                         [{"label": "a"}, {"label": "b"}])  # 'b' not implemented
    buf = io.StringIO()
    rc = validate_registry(REPO / ".agi", wf=wf, out=buf)
    assert rc == 1, buf.getvalue()
    assert "stage 'b' is not implemented by agi-good.js" in buf.getvalue()
    # sound pair -> green (separate dir so the broken pair above stays isolated)
    wf2 = tmp_path / "sound"
    wf2.mkdir()
    _write_registry_pair(wf2, "sound",
                         "phase('A')\nawait agent('x', {label: 'a'})\n",
                         [{"label": "a"}])
    buf2 = io.StringIO()
    rc2 = validate_registry(REPO / ".agi", wf=wf2, out=buf2)
    assert rc2 == 0, buf2.getvalue()
    assert "sound" in buf2.getvalue()


def test_register_derives_stages_and_refuses_overwrite(tmp_path, monkeypatch):
    """A real register round trip in an isolated workflows dir: derives the
    stage manifest from the inline script, then refuses a silent overwrite."""
    from workflow import register_workflow
    script = tmp_path / "inline-script.js"
    script.write_text(
        "phase('Draft')\n"
        "const drafts = await parallel(briefs.map(b => agent(`write {b.slug}`, "
        "{label: `draft:${b.slug}`, schema: DRAFT_SCHEMA})))\n"
        "phase('Critic')\n"
        "const critic = await agent(prompt, {label: 'critic', schema: "
        "CRITIC_SCHEMA})\n"
        "return {drafts, critic}\n", encoding="utf-8")
    reg_dir = tmp_path / "wf"
    reg_dir.mkdir()
    monkeypatch.setattr(workflow, "_repo_root", lambda root: tmp_path)
    monkeypatch.setattr(workflow, "WORKFLOWS_DIR_REL", ("wf",))
    buf = io.StringIO()
    rc = register_workflow(tmp_path, "draft-briefs", script,
                           from_dir=tmp_path / "some-run", out=buf)
    assert rc == 0, buf.getvalue()
    assert "[registered] draft-briefs" in buf.getvalue()
    js = reg_dir / "agi-draft-briefs.js"
    mf = reg_dir / "draft-briefs.json"
    assert js.is_file() and mf.is_file()
    manifest = json.loads(mf.read_text(encoding="utf-8"))
    labels = {st["label"] for st in manifest["stages"]}
    assert labels == {"draft", "critic"}, labels
    assert manifest["script"] == "agi-draft-briefs.js"
    assert manifest["_from_run"] == str(tmp_path / "some-run")
    # the derived repeat stage carries an honest label_template
    repeat = [s for s in manifest["stages"] if s["label"] == "draft"][0]
    assert repeat["repeat"]["label_template"] == "draft:{slug}", repeat
    # and the derived pair is a SOUND registry (the invariant is green on it)
    from workflow import validate_registry
    buf_v = io.StringIO()
    assert validate_registry(tmp_path, wf=reg_dir, out=buf_v) == 0, buf_v.getvalue()
    # refuses to overwrite an existing registration (exit code 2, files intact)
    buf2 = io.StringIO()
    rc2 = register_workflow(tmp_path, "draft-briefs", script, out=buf2)
    assert rc2 == 2, buf2.getvalue()
    assert js.read_text(encoding="utf-8") == script.read_text(encoding="utf-8")


def test_list_workflows_enumerates_registry(tmp_path, monkeypatch):
    from workflow import list_workflows
    wf = tmp_path / "wf"
    wf.mkdir()
    _write_registry_pair(wf, "alpha",
                         "phase('A')\nawait agent('x', {label: 'a'})\n",
                         [{"label": "a"}])
    monkeypatch.setattr(workflow, "_repo_root", lambda root: tmp_path)
    monkeypatch.setattr(workflow, "WORKFLOWS_DIR_REL", ("wf",))
    buf = io.StringIO()
    rc = list_workflows(tmp_path, out=buf)
    assert rc == 0, buf.getvalue()
    assert "alpha" in buf.getvalue()
    assert "agi-alpha.js" in buf.getvalue()
    assert "1" in buf.getvalue()  # one stage

# ---------- ONE run-event stream, TWO renderers (surface parity) -----------
# hypothesis:l3-workflow-surface-identical-across-harnesses: both harness
# paths feed RunView and nothing else; the summary renders from stage order
# and statuses only, with no harness token, so the same outcomes end
# byte-identically whichever harness fed the stream.

def test_run_view_summary_has_no_harness_token():
    from workflow import RunView
    stages = [{"label": "a"}, {"label": "b"}]
    for harness in ("pi", "claude-code"):
        buf = io.StringIO()
        v = RunView("review", stages, harness, out=buf)
        v.stage_finished("a", {"x": 1})
        v.stage_failed("b", "boom")
        v.summary()
        tail = [l for l in buf.getvalue().splitlines()
                if l.startswith(("[stage]", "[summary]"))]
        assert tail[-1] == "[summary] workflow=review stages=2 ok=1 failed=1", tail
        assert all(harness not in l for l in tail), tail


def test_summary_byte_identical_across_harnesses():
    from workflow import RunView
    stages = [{"label": "a"}, {"label": "b"}]
    summaries = []
    for harness in ("pi", "claude-code"):
        buf = io.StringIO()
        v = RunView("review", stages, harness, out=buf)
        v.stage_finished("a", {"x": 1})   # same outcomes, fed from either side
        v.stage_failed("b", "boom")
        v.summary()
        text = buf.getvalue()
        summaries.append(text[text.index("[stage]"):])
    assert summaries[0] == summaries[1]


def test_pi_live_run_renders_tree_through_view():
    """The pi path redraws the stage tree live per event and ends with the
    same summary shape — no more flat log lines."""
    import subprocess as _sp
    from unittest import mock
    from workflow import run_workflow
    # one JSON valid under BOTH review stages' schemas (extra keys allowed)
    good = ('preamble glue {"git_status": [], "links_broken": 0, "goals_check_ok": true, '
            '"summary": "s", "hypothesis": "h", "parent_agent": "p", '
            '"verdict": "v", "overclaims": [], "open_gaps": []}')
    def fake_run(cmd, **kw):
        return _sp.CompletedProcess(cmd, 0, stdout=good, stderr="")
    buf = io.StringIO()
    with mock.patch("subprocess.run", side_effect=fake_run):
        rc = run_workflow(REPO / ".agi", "review", "pi",
                          {"targets": [{"window": "t1"}]}, False, out=buf)
    assert rc == 0
    text = buf.getvalue()
    assert "workflow review (harness=pi)" in text
    assert "[~] global-checks" in text and "[~] review:t1" in text
    assert "└─ [✓] review:t1" in text          # final tree: both done
    assert "[stage] global-checks ok" in text and "[stage] review:t1 ok" in text
    assert "[summary] workflow=review stages=2 ok=2 failed=0" in text
    assert "[claude-code]" not in text and "[ok]" not in text


def test_claude_code_path_feeds_the_same_view():
    from workflow import run_workflow
    buf = io.StringIO()
    rc = run_workflow(REPO / ".agi", "review", "claude-code",
                      {"targets": [{"window": "t1"}]}, False, out=buf)
    assert rc == 0
    text = buf.getvalue()
    assert "workflow review (harness=claude-code)" in text
    assert "[·] global-checks" in text          # resolved, not executed here
    tail = [l for l in text.splitlines()
            if l.startswith(("[stage]", "[summary]"))]
    assert tail[-1] == "[summary] workflow=review stages=2 ok=0 failed=0", tail
    assert all("claude-code" not in l for l in tail), tail
