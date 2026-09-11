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
        rc, value = _run_stage_pi(cfg, st, {"draft:a": {"model": "glm",
                                                          "effort": "max"}},
                                  {"scratch": "/tmp/S"})
    assert rc == 0 and value == {"slug": "a", "v": 1}
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
        rc, value = _run_stage_pi(cfg, st, {"draft:a": {"model": "m", "effort": "x"}}, {})
    assert rc == 5 and value is None, rc  # schema-violating JSON -> non-zero, no prior value

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


def test_registry_flag_manifest_naming_unimplemented_stage(tmp_path, monkeypatch):
    """RED direction 2: a manifest naming a stage the script does not
    implement is an error — the script is the source of truth.

    Since hypothesis:l4-workflow-types-and-default-harness-are-a-geometry-node
    validate also requires every manifest to name a type the geometry node
    declares, so this test pins its OWN temp node (one type, `t`) and gives
    the sound pair that type -- the live config:workflows must not decide
    whether a registry-shape test is green (merge-up 20 went red on it)."""
    import workflow
    from workflow import validate_registry
    wf = tmp_path
    node = tmp_path / "workflows.md"
    node.write_text(_geometry_node_text("pi", [{"name": "t"}], []),
                    encoding="utf-8")
    monkeypatch.setattr(workflow, "_geometry_node_path", lambda root: node)
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
    _pair(wf2, "sound", "t", [{"label": "a"}])
    buf2 = io.StringIO()
    rc2 = validate_registry(REPO / ".agi", wf=wf2, out=buf2)
    assert rc2 == 0, buf2.getvalue()
    assert "sound" in buf2.getvalue()


def test_register_refuses_naming_author_verb(tmp_path, monkeypatch, capsys):
    """hypothesis:l4-workflow-authoring-is-a-harness-tool — register can only
    derive `<TODO>` prompt skeletons from an inline script's labels, which
    validate now rejects as non-runnable. So register refuses, naming the
    replacement verb (`workflow.py author`), and lands NOTHING."""
    from workflow import register_workflow
    script = tmp_path / "inline-script.js"
    script.write_text(
        "phase('Draft')\n"
        "const drafts = await parallel(briefs.map(b => agent(`write {b.slug}`, "
        "{label: `draft:${b.slug}`, schema: DRAFT_SCHEMA})))\n"
        "const critic = await agent(prompt, {label: 'critic', schema: "
        "CRITIC_SCHEMA})\n", encoding="utf-8")
    reg_dir = tmp_path / "wf"
    reg_dir.mkdir()
    monkeypatch.setattr(workflow, "_repo_root", lambda root: tmp_path)
    monkeypatch.setattr(workflow, "WORKFLOWS_DIR_REL", ("wf",))
    rc = register_workflow(tmp_path, "draft-briefs", script,
                           from_dir=tmp_path / "some-run", out=io.StringIO())
    err = capsys.readouterr().err
    assert rc == 2, err
    assert "workflow.py author" in err
    # it must NOT leave a half-written, non-runnable pair behind
    assert not (reg_dir / "agi-draft-briefs.js").exists()
    assert not (reg_dir / "draft-briefs.json").exists()


def _AUTHOR_STAGES():
    return [
        {"label": "investigate", "role": "kid",
         "prompt": "Investigate {question} under {scratch}. "
                   'Return {"answer":"..."} key={key}',
         "schema": {"type": "object", "properties": {"answer": {"type": "string"},
                      "evidence": {"type": "array"}, "still_live": {"type": "boolean"}},
                      "required": ["answer", "evidence", "still_live"]},
         "repeat": {"of": "questions", "label_template": "investigate:{key}"}},
        {"label": "refute", "chained_from": "investigate",
         "prompt": "Refute answer={answer} live={still_live} for {key}.",
         "schema": {"type": "object", "properties": {"refuted": {"type": "boolean"},
                      "why": {"type": "string"}},
                      "required": ["refuted", "why"]},
         "repeat": {"of": "questions", "label_template": "refute:{key}"}},
    ]


def test_author_lands_runnable_pair_dictated_by_manifest(tmp_path, monkeypatch):
    """author writes BOTH halves in one action — <name>.json with real prompts
    AND agi-<name>.js GENERATED FROM the manifest. The derived script must be a
    genuine Workflow script (meta/phases/pipeline/labels) whose stage base
    labels match the manifest, so validate_registry is sound on it, and it must
    refuse to land a <TODO> prompt."""
    from workflow import author_workflow, validate_registry
    wf = tmp_path / "wf"
    wf.mkdir()
    monkeypatch.setattr(workflow, "_repo_root", lambda root: tmp_path)
    monkeypatch.setattr(workflow, "WORKFLOWS_DIR_REL", ("wf",))
    buf = io.StringIO()
    rc = author_workflow(tmp_path, "prime-open-questions",
                         json.dumps(_AUTHOR_STAGES()), out=buf, source_note="t")
    assert rc == 0, buf.getvalue()
    assert "[authored]" in buf.getvalue()
    mf = wf / "prime-open-questions.json"
    js = wf / "agi-prime-open-questions.js"
    assert mf.is_file() and js.is_file()
    manifest = json.loads(mf.read_text(encoding="utf-8"))
    assert manifest["script"] == "agi-prime-open-questions.js"
    assert {s["label"] for s in manifest["stages"]} == {"investigate", "refute"}
    js_text = js.read_text(encoding="utf-8")
    # the script is DERIVED from the manifest: meta block, pipeline form,
    # agent() labels whose bases match the manifest stages (the invariant).
    assert "export const meta" in js_text and "await pipeline(" in js_text
    labels = workflow._script_stage_labels(js_text)
    for st in manifest["stages"]:
        assert st["label"] in labels, (st["label"], labels)
    # sound, and authoring writes on top of an existing pair (explicit tool)
    bufv = io.StringIO()
    assert validate_registry(tmp_path, wf=wf, out=bufv) == 0, bufv.getvalue()
    rc2 = author_workflow(tmp_path, "prime-open-questions",
                          json.dumps(_AUTHOR_STAGES()), out=io.StringIO())
    assert rc2 == 0  # author overwrites by design


def test_author_refuses_todo_prompt(tmp_path, monkeypatch, capsys):
    from workflow import author_workflow
    wf = tmp_path / "wf"
    wf.mkdir()
    monkeypatch.setattr(workflow, "_repo_root", lambda root: tmp_path)
    monkeypatch.setattr(workflow, "WORKFLOWS_DIR_REL", ("wf",))
    stages = [{"label": "x",
               "prompt": "<TODO: author the stage prompt for stage 'x'>"}]
    rc = author_workflow(tmp_path, "bad", json.dumps(stages), out=io.StringIO())
    err = capsys.readouterr().err
    assert rc == 2, err
    assert "<TODO>" in err
    assert not (wf / "bad.json").exists()


def test_validate_flags_todo_skeleton(tmp_path):
    """Strictly stronger than the base invariant: a manifest carrying a <TODO>
    prompt is a non-runnable skeleton and validate must flag it (this is what
    makes disproved-by checkable by the registry itself)."""
    from workflow import validate_registry
    wf = tmp_path
    (wf / "agi-skel.js").write_text(
        "phase('A')\nawait agent('x', {label: 'a'})\n", encoding="utf-8")
    (wf / "skel.json").write_text(json.dumps({
        "name": "skel", "script": "agi-skel.js",
        "stages": [{"label": "a",
                     "prompt": "<TODO: author the stage prompt for stage 'a'>"}]}),
        encoding="utf-8")
    buf = io.StringIO()
    rc = validate_registry(__import__("pathlib").Path("."), wf=wf, out=buf)
    assert rc == 1, buf.getvalue()
    assert "<TODO>" in buf.getvalue()


def test_render_stage_prompt_chains_prior_finding(tmp_path):
    """The pi chain mechanism: a repeated stage whose manifest carries
    `chained_from` renders with the prior stage's return for the same repeat
    key merged into its context, so it can name the finding's schema fields."""
    from workflow import render_stage_prompt
    st = {"label": "refute:c", "chained_from": "investigate",
          "prompt": "answer={answer} still_live={still_live} for {key}",
          "_repeat_item": {"key": "c"}}
    prior = {"answer": "it is inert", "still_live": True,
             "evidence": ["dispatch.py:755"]}
    out = render_stage_prompt(st, {"scratch": "/tmp"}, prior=prior)
    assert out == "answer=it is inert still_live=True for c", out


def test_pi_run_chains_investigate_to_refute(tmp_path_factory):
    """The whole point of the rewrite: an investigate->refute pair actually
    CHAINS on pi — the refute stage prompt is rendered with the investigate
    stage's validated return for the same repeat key (mock subprocess)."""
    import subprocess as _sp
    from unittest import mock
    import workflow as _wf
    from workflow import run_workflow
    finding = {"answer": "the guard is inert", "evidence": ["dispatch.py:755"],
               "still_live": True, "recommendation": "none", "ungrounded": "none"}
    verdict = {"refuted": False, "why": "holds", "corrected": "n/a"}
    calls = []

    def fake_run(cmd, **kw):
        calls.append(" ".join(cmd))
        prompt = " ".join(cmd[6:])  # prompt text follows provider/model/thinking
        body = verdict if "ANSWER:" in prompt else finding
        return _sp.CompletedProcess(cmd, 0, stdout=json.dumps(body), stderr="")

    tmp = tmp_path_factory.mktemp("chain-wf")
    saved = _wf._loc.shared_project_root
    _wf._loc.shared_project_root = lambda root: tmp
    try:
        buf = io.StringIO()
        with mock.patch("subprocess.run", side_effect=fake_run):
            rc = run_workflow(REPO / ".agi", "prime-open-questions", "pi",
                              {"questions": [{"key": "c", "question": "Q?"}]},
                              False, out=buf)
        assert rc == 0, buf.getvalue()
        assert len(calls) == 2, calls
        # the investigate finding reached the refute stage's rendered prompt
        assert any("the guard is inert" in c for c in calls), \
            "refute prompt never carried the investigate finding"
        assert "[summary] workflow=prime-open-questions stages=2 ok=2 failed=0" \
            in buf.getvalue()
    finally:
        _wf._loc.shared_project_root = saved


def test_list_workflows_enumerates_registry(tmp_path, monkeypatch):
    from workflow import list_workflows
    wf = tmp_path / "wf"
    wf.mkdir()
    _write_registry_pair(wf, "alpha",
                         "phase('A')\nawait agent('x', {label: 'a'})\n",
                         [{"label": "a"}])
    monkeypatch.setattr(workflow, "_repo_root", lambda root: tmp_path)
    monkeypatch.setattr(workflow, "WORKFLOWS_DIR_REL", ("wf",))
    # the new contract (hypothesis:l4-workflow-types-and-default-harness-are-
    # a-geometry-node): list resolves the harness through the geometry node,
    # never a literal — so the fixture needs a workflows.md.
    node = tmp_path / "nodes" / ".geometry" / "workflows.md"
    node.parent.mkdir(parents=True)
    node.write_text(_geometry_node_text("pi", [], []), encoding="utf-8")
    buf = io.StringIO()
    rc = list_workflows(tmp_path, out=buf)
    assert rc == 0, buf.getvalue()
    assert "alpha" in buf.getvalue()
    assert "agi-alpha.js" in buf.getvalue()
    assert "1" in buf.getvalue()  # one stage
    # resolved harness AND the level it came from (alpha: nothing declares it,
    # so it is the prime default)
    assert "pi" in buf.getvalue()
    assert "prime default" in buf.getvalue()

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


# ---------- run tracking: one row/real run, none on dry-run, never fatal ----
# Extends hypothesis:l4b13-workflow-router — a workflow run started either
# harness writes ONE jsonl row to `.agi/sessions/workflows/<key>.jsonl`,
# reusing the `<project>/sessions/` pattern dispatch.py already writes.


def _tmp_session_root(tmp_path_factory, wf_mod):
    """Redirect workflow's `<project>/sessions/` resolution into a temp dir so
    a test asserts exactly what tracking wrote, never the real `.agi/sessions/`.
    Returns (tmp_root, restore)."""
    tmp = tmp_path_factory.mktemp("wf-sessions")
    saved = wf_mod._loc.shared_project_root
    wf_mod._loc.shared_project_root = lambda root: tmp
    return tmp, lambda: setattr(wf_mod._loc, "shared_project_root", saved)


def test_real_cc_run_appends_exactly_one_row(tmp_path_factory):
    import workflow as _wf
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    try:
        buf = io.StringIO()
        rc = run_workflow(REPO / ".agi", "review", "claude-code",
                          {"targets": [{"window": "t1"}]}, False, out=buf)
        assert rc == 0
        path = tmp / "sessions" / "workflows" / "review.jsonl"
        lines = path.read_text(encoding="utf-8").splitlines()
        assert len(lines) == 1, lines
        row = json.loads(lines[0])
        assert row["workflow"] == "review"
        assert row["harness"] == "claude-code"
        assert row["timestamp"]
        review_lb = [k for k in row["stages"] if k.startswith("review")]
        assert "global-checks" in row["stages"] and len(review_lb) == 1, row
        assert row["stages"]["global-checks"] == "resolved"
        assert row["ok"] == 0 and row["failed"] == 0
    finally:
        restore()


def test_real_pi_run_appends_one_row_with_ok_counts(tmp_path_factory):
    import subprocess as _sp
    from unittest import mock
    import workflow as _wf
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    # a JSON valid under BOTH review stages' schemas (extra keys allowed)
    good = ('{"git_status": [], "links_broken": 0, "goals_check_ok": true, '
            '"summary": "s", "hypothesis": "h", "parent_agent": "p", '
            '"verdict": "v", "overclaims": [], "open_gaps": []}')

    def fake_run(cmd, **kw):
        return _sp.CompletedProcess(cmd, 0, stdout=good, stderr="")
    try:
        buf = io.StringIO()
        with mock.patch("subprocess.run", side_effect=fake_run):
            rc = run_workflow(REPO / ".agi", "review", "pi",
                              {"targets": [{"window": "t1"}]}, False, out=buf)
        assert rc == 0
        lines = (tmp / "sessions" / "workflows" / "review.jsonl")\
            .read_text(encoding="utf-8").splitlines()
        assert len(lines) == 1, lines
        row = json.loads(lines[0])
        assert row["harness"] == "pi"
        review_lb = [k for k in row["stages"] if k.startswith("review")]
        assert row["stages"]["global-checks"] == "ok"
        assert len(review_lb) == 1 and row["stages"][review_lb[0]] == "ok"
        assert row["ok"] == 2 and row["failed"] == 0
    finally:
        restore()


def test_dry_run_writes_no_row(tmp_path_factory):
    import workflow as _wf
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    try:
        buf = io.StringIO()
        rc = run_workflow(REPO / ".agi", "review", "claude-code",
                          {"targets": [{"window": "t1"}]}, True, out=buf)
        assert rc == 0
        assert not (tmp / "sessions").exists(), \
            "dry-run must not create a sessions dir"
    finally:
        restore()


def test_tracking_failure_does_not_fail_workflow(tmp_path_factory, capsys):
    import workflow as _wf
    from workflow import run_workflow
    saved = _wf._loc.shared_project_root

    def boom(root):
        raise OSError("disk full (simulated)")
    _wf._loc.shared_project_root = boom
    try:
        buf = io.StringIO()
        rc = run_workflow(REPO / ".agi", "review", "claude-code",
                          {"targets": [{"window": "t1"}]}, False, out=buf)
        assert rc == 0, "tracking failure must NOT fail the workflow run"
        assert "warn: run tracking failed" in capsys.readouterr().err
    finally:
        _wf._loc.shared_project_root = saved


# ============================================================================
# geometry-node harness resolution — hypothesis:l4-workflow-types-and-default-
# harness-are-a-geometry-node. workflow.py run/list resolve the default harness
# through .geometry/workflows.md (per-workflow > per-type > prime default),
# with NO hardcoded 'pi' fallback: absent or exhausted, they refuse loudly
# naming the node. An explicit --harness still wins (the CLI per-run override).
# A kid cannot write a live `config` node, so these prove on fixture roots and
# on a temp node redirected through `_geometry_node_path`.
# ============================================================================


def _geometry_node_text(default_harness, types, workflows):
    """Render a `.geometry/workflows.md` frontmatter (the shape workflow.py
    reads via yaml.safe_load, built from dicts so the reader and the writer
    agree on structure). A `types` row is {name, harness?}; a `workflows`
    row is {name, type?, harness?}."""
    import yaml as _y
    fm = {"id": "config:workflows", "type": "config",
          "parents": ["goal:g1.14"],
          "default_harness": default_harness,
          "types": types, "workflows": workflows}
    return ("---\n" + _y.safe_dump(fm, sort_keys=False)
            + "---\n# config:workflows\n")


def _pair(wf: Path, name: str, typ: "str | None", stages: list,
          provider: "str | None" = None):
    """Write a SOUND manifest+script pair (script implements its stages) with
    an optional `type` and optional `provider`, so validate's base invariant
    stays green and only the type under test moves."""
    (wf / f"agi-{name}.js").write_text(
        "phase('X')\n"
        + "\n".join(f"await agent('proc', {{label: '{s['label']}'}})"
                    for s in stages) + "\n", encoding="utf-8")
    mf = {"name": name, "script": f"agi-{name}.js", "stages": stages}
    if typ:
        mf["type"] = typ
    if provider:
        mf["provider"] = provider
    (wf / f"{name}.json").write_text(
        json.dumps(mf, indent=2) + "\n", encoding="utf-8")


def test_geometry_node_resolves_all_live_workflows(tmp_path, monkeypatch):
    """PROVED-BY: with a workflows.md declaring every live type + per-workflow
    rows (eight since merge-up-review and desktop-check), `workflow.py list` on the REAL registry shows every registered
    workflows resolving through the node, each with the LEVEL it came from
    (config row / per-workflow override / per-type override) — no literal.
    The node is a TEMP file the test writes; `_geometry_node_path` is
    redirected to it (a kid cannot write the live config node)."""
    from workflow import list_workflows
    node = tmp_path / "workflows.md"
    node.write_text(_geometry_node_text(
        default_harness="pi",
        types=[
            {"name": "review", "harness": "pi"},
            {"name": "drafting", "harness": "claude-code"},
            {"name": "research", "harness": "pi"},
            {"name": "route-probe", "harness": "pi"},
            {"name": "plan-research", "harness": "pi"},
            {"name": "investigate-refute", "harness": "pi"},
            # merge-up-review: registered by the Prime L4-VII (owner 2026-09-11,
            # the merge-up review runs through the unified router).
            {"name": "merge-up-review", "harness": "claude-code"},
            {"name": "desktop-check", "harness": "claude-code"},
        ],
        workflows=[
            {"name": "review", "type": "review"},
            {"name": "drafting", "type": "drafting"},
            {"name": "deep-search", "type": "research"},
            {"name": "l3w-route-probe", "type": "route-probe",
             "harness": "claude-code"},
            {"name": "l4-plan-research", "type": "plan-research"},
            {"name": "prime-open-questions", "type": "investigate-refute"},
            {"name": "merge-up-review", "type": "merge-up-review"},
            {"name": "desktop-check", "type": "desktop-check"},
        ],
    ), encoding="utf-8")
    monkeypatch.setattr(workflow, "_geometry_node_path", lambda root: node)
    buf = io.StringIO()
    rc = list_workflows(REPO / ".agi", out=buf)
    assert rc == 0, buf.getvalue()
    txt = buf.getvalue()
    for k in ("deep-search", "drafting", "l3w-route-probe",
              "l4-plan-research", "prime-open-questions", "review",
              "merge-up-review", "desktop-check"):
        assert k in txt, (k, txt)
    assert "config row" in txt, txt          # review/drafting/deep-search rows
    assert "claude-code" in txt, txt         # drafting config row
    assert "per-workflow" in txt, txt        # l3w-route-probe node override
    assert "type:investigate-refute" in txt, txt
    assert "type:plan-research" in txt, txt


def test_fixture_root_resolution_levels_and_default_flip(tmp_path):
    """PROVED-BY (fixture root): a temp `.agi` with its own config.json + a
    workflows.md the test writes resolves four workflows through all four
    sources — config row, per-type, per-workflow override, prime default —
    and flipping default_harness in the node (no manifest or code edit) moves
    what the override-less workflow resolves to."""
    from workflow import list_workflows
    agi = tmp_path / "_agi"
    (agi / "nodes" / ".geometry").mkdir(parents=True)
    (agi / "config.json").write_text(json.dumps(
        {"workflows": {"A": {"provider": "claude-code"}}}), encoding="utf-8")
    node = agi / "nodes" / ".geometry" / "workflows.md"
    node.write_text(_geometry_node_text(
        "pi",
        [{"name": "tB", "harness": "claude-code"},
         {"name": "tC", "harness": "pi"}],
        [{"name": "B", "type": "tB"},
         {"name": "C", "type": "tC", "harness": "claude-code"},
         {"name": "D"}],
    ), encoding="utf-8")
    wf = tmp_path / "extensions" / "agi" / "workflows"
    wf.mkdir(parents=True)
    _pair(wf, "A", None, [{"label": "a"}])
    _pair(wf, "B", "tB", [{"label": "b"}])
    _pair(wf, "C", "tC", [{"label": "c"}])
    _pair(wf, "D", None, [{"label": "d"}])

    buf = io.StringIO()
    assert list_workflows(agi, out=buf) == 0, buf.getvalue()
    txt = buf.getvalue()
    assert "A" in txt and "config row" in txt, txt
    assert "B" in txt and "type:tB" in txt, txt
    assert "C" in txt and "per-workflow" in txt, txt
    assert "D" in txt and "pi" in txt and "prime default" in txt, txt
    c_line = next(l for l in txt.splitlines()
                  if l.startswith("C") and "agi-C" in l)
    # C's per-workflow override (claude-code) beats its type's harness (pi)
    assert "claude-code" in c_line and "per-workflow" in c_line, c_line
    b_line = next(l for l in txt.splitlines()
                  if l.startswith("B") and "agi-B" in l)
    assert "claude-code" in b_line and "type:tB" in b_line, b_line

    # FLIP the prime default (a node edit COMMIT): the override-less D moves.
    node.write_text(_geometry_node_text(
        "deep-seek",
        [{"name": "tB", "harness": "claude-code"},
         {"name": "tC", "harness": "pi"}],
        [{"name": "B", "type": "tB"},
         {"name": "C", "type": "tC", "harness": "claude-code"},
         {"name": "D"}],
    ), encoding="utf-8")
    buf2 = io.StringIO()
    assert list_workflows(agi, out=buf2) == 0, buf2.getvalue()
    d_line2 = next(l for l in buf2.getvalue().splitlines()
                   if l.startswith("D") and "agi-D" in l)
    assert "deep-seek" in d_line2 and "prime default" in d_line2, d_line2
    b_line2 = next(l for l in buf2.getvalue().splitlines()
                   if l.startswith("B") and "agi-B" in l)
    assert "claude-code" in b_line2, b_line2  # override untouched by the flip


def test_missing_node_refuses_loudly_naming_it(tmp_path):
    """DISPROVED-BY guard: with NO workflows.md (the live state until the
    prime lands it), `list` and `run` must REFUSE loudly naming the node —
    never fall back to a literal 'pi'."""
    from workflow import list_workflows, run_workflow, WorkflowsNodeError
    agi = tmp_path / "_agi"
    (agi / "nodes" / ".geometry").mkdir(parents=True)
    (agi / "config.json").write_text("{}", encoding="utf-8")
    wf = tmp_path / "extensions" / "agi" / "workflows"
    wf.mkdir(parents=True)
    _pair(wf, "A", None, [{"label": "a"}])
    try:
        list_workflows(agi, out=io.StringIO())
        raise AssertionError("expected WorkflowsNodeError on an absent node")
    except WorkflowsNodeError as exc:
        assert "workflows.md" in str(exc), exc
    try:
        run_workflow(agi, "A", None, {}, True, out=io.StringIO())
        raise AssertionError("expected WorkflowsNodeError on an absent node")
    except WorkflowsNodeError as exc:
        assert "workflows.md" in str(exc), exc


def test_validate_refuses_undeclared_and_missing_type(tmp_path):
    """PROVED-BY: with the node present, validate refuses a manifest whose
    `type` is undeclared, and one with no `type` at all — and accepts a sound
    pair whose type is declared."""
    from workflow import validate_registry
    agi = tmp_path / "_agi"
    (agi / "nodes" / ".geometry").mkdir(parents=True)
    (agi / "config.json").write_text("{}", encoding="utf-8")
    node = agi / "nodes" / ".geometry" / "workflows.md"
    node.write_text(_geometry_node_text(
        "pi", [{"name": "good", "harness": "pi"}],
        [{"name": "ok", "type": "good"}]), encoding="utf-8")
    wf = tmp_path / "extensions" / "agi" / "workflows"
    wf.mkdir(parents=True)
    _pair(wf, "ok", "good", [{"label": "ok"}])          # declared -> green
    buf = io.StringIO()
    assert validate_registry(agi, wf=wf, out=buf) == 0, buf.getvalue()
    _pair(wf, "bogus", "ghost-type", [{"label": "bogus"}])  # undeclared
    buf2 = io.StringIO()
    assert validate_registry(agi, wf=wf, out=buf2) == 1, buf2.getvalue()
    assert "not a declared type" in buf2.getvalue(), buf2.getvalue()
    assert "ghost-type" in buf2.getvalue(), buf2.getvalue()
    _pair(wf, "bare", None, [{"label": "bare"}])          # missing type
    buf3 = io.StringIO()
    assert validate_registry(agi, wf=wf, out=buf3) == 1, buf3.getvalue()
    assert "declares no `type`" in buf3.getvalue(), buf3.getvalue()


def test_config_row_shadows_node_perworkflow_and_type(tmp_path):
    """THE SHADOWING GAP (experiment:a00-74831cf6-8c9c96). When a workflow
    carries a config.json `workflows.<name>.provider` row, that row resolves
    FIRST in _resolve_default_harness (level "config row") and the node's OWN
    per-workflow `workflows.<name>.harness` AND its per-type `types[type]
    .harness` are both UNREACHABLE. The node's two committed override levels
    are dead weight for any workflow with a provider row — 3 of the 6 live
    workflows (review, drafting, deep-search) have one, so for them the node
    per-workflow and per-type overrides silently do nothing.

    This uses a DELIBERATELY DISTINCTIVE node per-workflow harness
    ('deep-seek') and type harness ('type-seek') that never appear in the
    config row, so the assertion can only pass because the row shadows them —
    not because the values happen to agree."""
    from workflow import list_workflows
    agi = tmp_path / "_agi"
    (agi / "nodes" / ".geometry").mkdir(parents=True)
    # X: config row provider = claude-code (level "config row", shadows all below)
    (agi / "config.json").write_text(json.dumps(
        {"workflows": {"X": {"provider": "claude-code"}}}), encoding="utf-8")
    node = agi / "nodes" / ".geometry" / "workflows.md"
    node.write_text(_geometry_node_text(
        "pi",
        [{"name": "tX", "harness": "type-seek"}],
        [{"name": "X", "type": "tX", "harness": "deep-seek"}],
    ), encoding="utf-8")
    wf = tmp_path / "extensions" / "agi" / "workflows"
    wf.mkdir(parents=True)
    _pair(wf, "X", "tX", [{"label": "x"}])     # manifest also carries type tX

    buf = io.StringIO()
    assert list_workflows(agi, out=buf) == 0, buf.getvalue()
    txt = buf.getvalue()
    x_line = next(l for l in txt.splitlines() if "agi-X" in l)
    assert "claude-code" in x_line, x_line            # the config row wins
    assert "config row" in x_line, x_line
    assert "deep-seek" not in txt, txt   # node per-workflow shadowed -> dead
    assert "per-workflow" not in txt, txt
    assert "type-seek" not in txt, txt    # node per-type shadowed -> dead
    assert "type:tX" not in txt, txt

    # Same workflow WITHOUT a config row but WITH a manifest provider: the
    # manifest provider (level "manifest") shadows the node's two levels too.
    (agi / "config.json").write_text("{}", encoding="utf-8")
    _pair(wf, "Y", "tY", [{"label": "y"}], provider="claude-code-py")
    buf2 = io.StringIO()
    assert list_workflows(agi, out=buf2) == 0, buf2.getvalue()
    txt2 = buf2.getvalue()
    y_line = next(l for l in txt2.splitlines() if "agi-Y" in l)
    assert "claude-code-py" in y_line, y_line
    assert "manifest" in y_line, y_line


def _workflow_body_parses(script_text: str) -> str | None:
    """Wrap a generated Workflow script the way the Workflow tool does (an
    async body with top-level `return` and `await`) and parse it with node
    when node is on PATH. Returns the SyntaxError line, or None when it
    parses (or when node is absent — then the caller falls back to the
    textual assertions)."""
    import shutil
    import subprocess
    import tempfile
    node = shutil.which("node")
    if not node:
        return None
    body = "\n".join(ln for ln in script_text.splitlines()
                     if not ln.startswith("export const meta"))
    # drop the meta literal's remaining lines up to its closing brace
    lines = body.splitlines()
    for i, ln in enumerate(lines):
        if ln.strip() == "}":
            lines = lines[i + 1:]
            break
    wrapped = ("async function __w(args, agent, parallel, pipeline, phase, "
               "log) {\n" + "\n".join(lines) + "\n}\n")
    with tempfile.NamedTemporaryFile("w", suffix=".mjs", delete=False) as fh:
        fh.write(wrapped)
        path = fh.name
    proc = subprocess.run([node, "--check", path], capture_output=True,
                          text=True, timeout=30)
    for ln in (proc.stderr or "").splitlines():
        if "SyntaxError" in ln:
            return ln
    return None


def test_generated_script_parses_as_a_workflow_body():
    """PROVED-BY (Prime L4-VII, 2026-09-11): the first two pairs authored
    through `workflow.py author` failed at the Workflow tool with
    `Unterminated regular expression` — the generated `fill` line escaped its
    closing slash (`\\}\\/g`) — and a single-stage pair with a hyphenated
    label returned `{ capture-and-read: r0 }`, not an identifier. Both are
    generator defects the existing tests could not see, because they check
    the manifest round-trip and never parse the script. This test parses the
    generated body with node (when present) and asserts the two lines
    textually regardless."""
    from workflow import _gen_script
    single = {"name": "parse-probe", "description": "d", "stages": [
        {"label": "capture-and-read", "prompt": "look at {focus}",
         "schema": {"type": "object", "properties": {"x": {"type": "string"}},
                    "required": ["x"]}}]}
    text = _gen_script(single)
    fill = [ln for ln in text.splitlines() if ln.startswith("const fill")][0]
    assert "\\}/g," in fill and "\\}\\/g" not in fill, fill
    assert 'return { "capture-and-read": r0 }' in text, text.splitlines()[-1]
    err = _workflow_body_parses(text)
    assert err is None, err
    chained = {"name": "parse-probe-2", "description": "d", "stages": [
        {"label": "review", "prompt": "review {key}",
         "repeat": {"of": "rounds", "label_template": "review:{key}"}},
        {"label": "verify", "prompt": "verify {key} {summary}",
         "chained_from": "review",
         "repeat": {"of": "rounds", "label_template": "verify:{key}"}}]}
    err = _workflow_body_parses(_gen_script(chained))
    assert err is None, err


# ---------- descriptive per-run keys (hypothesis:l4-a-workflow-run-is- ---
# named-not-numbered) -----------------------------------------------------
# A workflow run is cited by a KEY derived from its type + run args, printed
# first, recorded beside the workflow in the tracked row, and resolved by
# `workflow.py status` — never by the opaque harness-minted id.


def test_mint_run_key_three_shapes(tmp_path):
    from workflow import _mint_run_key
    # merge-up review of merge-up 39
    assert _mint_run_key(tmp_path, "merge-up-review",
                         {"rounds": [39]}) == "mur-39"
    # SL1#2 -> slugified to sl1-2
    assert _mint_run_key(tmp_path, "merge-up-review",
                         {"rounds": ["SL1#2"]}) == "mur-sl1-2"
    # author/validate keep their whole name with no run args
    assert _mint_run_key(tmp_path, "author", {}) == "author"
    assert _mint_run_key(tmp_path, "validate", {}) == "validate"
    # a single-word key keeps its name and joins the slugged scalar arg
    assert _mint_run_key(tmp_path, "review",
                         {"window": "SL1#2"}) == "review-sl1-2"


def test_mint_run_key_collision_appends_suffix(tmp_path_factory):
    import workflow as _wf
    from workflow import _mint_run_key
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    try:
        assert _mint_run_key(tmp, "merge-up-review",
                             {"rounds": [39]}) == "mur-39"
        # a tracked row already claimed mur-39 -> deterministic -2, -3
        wf_dir = tmp / "sessions" / "workflows"
        wf_dir.mkdir(parents=True, exist_ok=True)
        path = wf_dir / "merge-up-review.jsonl"
        for rk in ("mur-39", "mur-39-2"):
            with open(path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps({"run_key": rk,
                                     "workflow": "merge-up-review"}) + "\n")
        assert _mint_run_key(tmp, "merge-up-review",
                             {"rounds": [39]}) == "mur-39-3"
    finally:
        restore()


def test_run_prints_run_key_first_and_tracks_it(tmp_path_factory):
    import subprocess as _sp
    from unittest import mock
    import workflow as _wf
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    good = ('{"git_status": [], "links_broken": 0, "goals_check_ok": true, '
            '"summary": "s", "hypothesis": "h", "parent_agent": "p", '
            '"verdict": "v", "overclaims": [], "open_gaps": []}')

    def fake_run(cmd, **kw):
        return _sp.CompletedProcess(cmd, 0, stdout=good, stderr="")
    try:
        buf = io.StringIO()
        with mock.patch("subprocess.run", side_effect=fake_run):
            rc = run_workflow(REPO / ".agi", "review", "pi",
                              {"window": "SL1#2"}, False, out=buf)
        assert rc == 0, buf.getvalue()
        text = buf.getvalue()
        # the run key is printed FIRST, before any stage tree line
        assert text.splitlines()[0] == "[run-key] review-sl1-2", text
        # and recorded BESIDE the workflow in the tracked row
        rows = [json.loads(l) for l in (tmp / "sessions" / "workflows"
                / "review.jsonl").read_text(encoding="utf-8")
                .splitlines()]
        assert rows[0]["run_key"] == "review-sl1-2"
        assert rows[0]["workflow"] == "review"
    finally:
        restore()


def test_status_resolves_by_run_key(tmp_path_factory):
    import workflow as _wf
    from workflow import RunView, _track_run, status_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    try:
        v = RunView("merge-up-review", [{"label": "a"}], "pi",
                    out=io.StringIO())
        _track_run(tmp, "merge-up-review", "pi", v, "mur-39")
        buf = io.StringIO()
        rc = status_workflow(tmp, "mur-39", out=buf)
        assert rc == 0, buf.getvalue()
        assert "mur-39" in buf.getvalue()
        assert "merge-up-review" in buf.getvalue()
        # a key naming no run resolves to a miss (exit 1)
        miss = io.StringIO()
        assert status_workflow(tmp, "nope", out=miss) == 1
    finally:
        restore()


def test_note_records_harness_id_and_status_shows_it(tmp_path_factory):
    """`workflow.py note <run_key> --harness-id wf_<id>` records the claude-
    code harness's minted id beside the tracked row, and `status <run_key>`
    prints it (hypothesis:l4-a-workflow-run-is-named-not-numbered)."""
    import workflow as _wf
    from workflow import RunView, _track_run, note_workflow, status_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    try:
        v = RunView("merge-up-review", [{"label": "a"}], "claude-code",
                    out=io.StringIO())
        _track_run(tmp, "merge-up-review", "claude-code", v, "mur-39")
        note = io.StringIO()
        rc = note_workflow(tmp, "mur-39", "wf_ba530baa-dab", out=note)
        assert rc == 0, note.getvalue()
        buf = io.StringIO()
        assert status_workflow(tmp, "mur-39", out=buf) == 0
        assert "harness_id=wf_ba530baa-dab" in buf.getvalue(), buf.getvalue()
        # before any note, status shows a dash
        v2 = RunView("review", [{"label": "a"}], "claude-code",
                     out=io.StringIO())
        _track_run(tmp, "review", "claude-code", v2, "review")
        pre = io.StringIO()
        status_workflow(tmp, "review", out=pre)
        assert "harness_id=-" in pre.getvalue(), pre.getvalue()
    finally:
        restore()


def test_note_unknown_run_key_refused(tmp_path_factory):
    import workflow as _wf
    from workflow import note_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    try:
        note = io.StringIO()
        rc = note_workflow(tmp, "never-minted", "wf_x", out=note)
        assert rc == 2, note.getvalue()
        assert "never-minted" in note.getvalue()
    finally:
        restore()


def test_note_second_different_id_appends_not_overwrites(tmp_path_factory):
    import workflow as _wf
    from workflow import RunView, _track_run, note_workflow, status_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    try:
        v = RunView("merge-up-review", [{"label": "a"}], "claude-code",
                    out=io.StringIO())
        _track_run(tmp, "merge-up-review", "claude-code", v, "mur-39")
        for hid in ("wf_ba530baa-dab", "wf_c7475c13-812"):
            assert note_workflow(tmp, "mur-39", hid) == 0
        # re-noting the SAME id is a no-op; the two distinct ids both survive
        assert note_workflow(tmp, "mur-39", "wf_ba530baa-dab") == 0
        buf = io.StringIO()
        assert status_workflow(tmp, "mur-39", out=buf) == 0
        assert "harness_id=wf_ba530baa-dab,wf_c7475c13-812" in buf.getvalue(), \
            buf.getvalue()
    finally:
        restore()


def test_status_resolves_by_harness_id(tmp_path_factory):
    import workflow as _wf
    from workflow import RunView, _track_run, status_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    try:
        v = RunView("merge-up-review", [{"label": "a"}], "claude-code",
                    out=io.StringIO())
        _track_run(tmp, "merge-up-review", "claude-code", v, "mur-39")
        buf = io.StringIO()
        assert status_workflow(tmp, "wf_ba530baa-dab", out=buf) == 1
        from workflow import note_workflow
        note_workflow(tmp, "mur-39", "wf_ba530baa-dab")
        hit = io.StringIO()
        assert status_workflow(tmp, "wf_ba530baa-dab", out=hit) == 0
        assert "mur-39" in hit.getvalue(), hit.getvalue()
    finally:
        restore()


def test_author_round_trip_keeps_type_and_appends_note(tmp_path, monkeypatch):
    """Re-authoring an EXISTING manifest must carry `type` through (a dropped
    type is one more validate violation) and APPEND the --note to the existing
    description instead of replacing it (measured: author dropped type and
    replaced description; restored by hand at 07bae9ea8)."""
    from workflow import author_workflow
    wf = tmp_path / "wf"
    wf.mkdir()
    monkeypatch.setattr(workflow, "_repo_root", lambda root: tmp_path)
    monkeypatch.setattr(workflow, "WORKFLOWS_DIR_REL", ("wf",))
    orig = {
        "name": "merge-up-review",
        "script": "agi-merge-up-review.js",
        "type": "merge-up-review",
        "description": "base description of the workflow",
        "stages": _AUTHOR_STAGES(),
    }
    (wf / "merge-up-review.json").write_text(
        json.dumps(orig, indent=2) + "\n", encoding="utf-8")
    rc = author_workflow(tmp_path, "merge-up-review",
                         json.dumps(_AUTHOR_STAGES()),
                         out=io.StringIO(), source_note="X")
    assert rc == 0
    carried = json.loads((wf / "merge-up-review.json")
                         .read_text(encoding="utf-8"))
    assert carried["type"] == "merge-up-review", \
        "the type cell must survive re-authoring"
    assert carried["description"].startswith("base description"), carried
    assert "(X)" in carried["description"], \
        "the --note must be APPENDED to the existing description"
