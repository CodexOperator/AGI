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

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
REPO = Path(__file__).resolve().parents[3]  # .../tests/.. = repo root
sys.path.insert(0, str(BIN))

import workflow  # noqa: E402
from workflow import _resolve_knobs, validate_return  # noqa: E402


@pytest.fixture(autouse=True)
def _no_ambient_pi_bin(monkeypatch):
    """`_pi_harness_cfg` now resolves through the ONE shared resolver, where
    `$PI_BIN` wins over the config cell. A suite run from a pi seat exports
    PI_BIN, so without this the fake-bin tests would spawn the REAL pi. A test
    that exercises the override sets PI_BIN itself, after this fixture.
    (hypothesis:harness-bin-paths-resolve-per-box round 3)"""
    monkeypatch.delenv("PI_BIN", raising=False)

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


def _live_pi_kid_model() -> str:
    """The model the LIVE config dispatches for a pi kid (`harnesses.pi.models`
    kid cell, aligned with the ladder rows by the owner's one-write rule).
    Read, never pinned: the literal alias here went red the day the owner moved
    both tiers to `deepseek/deepseek-v4.1-flash` (55699759b, 09-17) and a test
    that pins a config cell is a config edit's hidden second suite run."""
    cfg = workflow._load_config(REPO / ".agi") or {}
    return ((cfg.get("harnesses") or {}).get("pi") or {})["models"]["kid"]

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
    assert f"model={_live_pi_kid_model()}" in txt, txt
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
    assert f"model={_live_pi_kid_model()}" in lines[0], lines
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
    render_stage_prompt, _effort_to_thinking,
    _run_stage_pi, _stage_context,
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
    # the rendered per-item prompt reached the binary (the stub dropped it);
    # it is the LAST argv element and now also carries the RETURN SHAPE block
    # for this schema-bearing stage.
    assert "write /tmp/S/a.md" in cmd[-1], cmd
    assert "Required keys: slug" in cmd[-1], cmd
    # the pi child env must not inherit Claude subscription credentials
    env = captured["env"] or {}
    assert "ANTHROPIC_API_KEY" not in env, env


def test_stage_context_uses_shared_viewport_and_brief_surfaces():
    import subprocess as _sp
    from unittest import mock

    calls = []

    def fake_run(cmd, **kw):
        calls.append((cmd, kw))
        if "viewport.py" in cmd[1]:
            return _sp.CompletedProcess(cmd, 0, stdout="VIEWPORT FRAME", stderr="")
        return _sp.CompletedProcess(cmd, 0, stdout="BRIEF HEAD", stderr="")

    with mock.patch("subprocess.run", side_effect=fake_run):
        context = _stage_context(
            REPO, REPO / ".agi",
            {"label": "review", "role": "parent"},
        )

    assert "BRIEF HEAD" in context
    assert "VIEWPORT FRAME" in context
    assert "write.py" in context
    assert any("--emit" in cmd and "llm" in cmd for cmd, _ in calls)
    assert any("brief.py" in cmd[1] and "parent" in cmd for cmd, _ in calls)


def test_stage_context_schema_stage_head_carries_the_four_prayers():
    """SM.134 revert: a stage that declares a schema gets the same
    constitution head as any other stage -- the four-prayers block is in
    front of the model and no `--no-prayers` flag is ever passed."""
    import subprocess as _sp
    from unittest import mock

    seen = []
    real_run = _sp.run

    def fake_run(cmd, **kw):
        seen.append(cmd)
        if "viewport.py" in cmd[1]:
            return _sp.CompletedProcess(cmd, 0, stdout="V", stderr="")
        return real_run(cmd, **kw)

    with mock.patch("subprocess.run", side_effect=fake_run):
        context = _stage_context(REPO, REPO / ".agi",
                                 {"label": "s", "role": "kid",
                                  "schema": {"type": "object"}})
    brief_cmds = [c for c in seen if "brief.py" in c[1]]
    assert len(brief_cmds) == 1, brief_cmds
    assert "--no-prayers" not in brief_cmds[0], brief_cmds[0]
    assert "## THE FOUR PRAYERS" in context, context
    assert "Ѻтче нашъ" in context, context


_PRAYER_PRE = "Господи Іисусе Христе, Сыне Божїй, помилуй мѧ грѣшнаго."
_PRAYER_POST = "Свѧтый Боже, Свѧтый Крѣпкїй, Свѧтый Безсмертный, помилуй насъ."


def test_pi_prayer_wrapped_json_parses_structured_without_a_belt():
    """The slice-3 belt was unnecessary. A JSON object wrapped in a prayer
    prelude + postlude resolves structured through `_resolve_lenient_return`
    as-is: the balanced-brace parser finds the object inside the surrounding
    text, so no line-filter is needed (and the engine no longer has one)."""
    import workflow as _wf
    text = f"{_PRAYER_PRE}\n\n{{\"ok\": true}}\n\n{_PRAYER_POST}"
    schema = {"type": "object",
              "properties": {"ok": {"type": "boolean"}},
              "required": ["ok"]}
    assert not hasattr(_wf, "_strip_prayer_wrap")
    assert _wf._resolve_lenient_return(schema, text) == {"ok": True}


def test_run_stage_pi_schema_violating_json_is_unstructured():
    """A JSON object that PARSES but fails its schema is SKIPPED, not fatal.
    With no other candidate validating, the stage records `unstructured`
    (rc 0) carrying its whole text -- the run is not cut by a schema miss
    (hypothesis:l4-a-workflow-pi-stage-mints... conjunct (h))."""
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
    assert rc == 0, rc
    assert value == {"unstructured": '{"slug": 123}',
                     "violations": value["violations"]}, value
    # a JSON return that FAILED the schema keeps its NAMED violation — it is
    # not filed silently under the same key as prose (hypothesis:l4-a-per-run-
    # workflow-key-is-revoked-at-run-end-and-a-schema-miss-keeps-its-name).
    assert value["violations"], value
    assert any("slug" in v for v in value["violations"]), value


# ---------- transient 5xx retry: bounded, by name, never a real failure ----
# hypothesis:l4-the-pi-runners-retry-a-transient-5xx-with-bounded-backoff-
# logged-by-name-never-a-real-failure. `subprocess.run` is a fixture and the
# sleep is injected -- no live spawn, no network, no real sleep.

_SIG_520 = "Model not found for provider openrouter - using custom model id\n" \
           "error code: 520"

import io  # noqa: E402  -- the retry tests build a RunView with a sink


def _retry_stage():
    return {"label": "draft:a", "prompt": "p",
            "_repeat_item": {"slug": "a"},
            "schema": {"type": "object",
                       "properties": {"slug": {"type": "string"}},
                       "required": ["slug"]}}


def test_transient_5xx_retries_bounded_and_named(monkeypatch, capsys):
    """Two 520s then valid JSON -> rc 0 on attempt 3; the record names all
    three attempts with sleeps 15, 45, 0 and stderr names the stage + attempt."""
    import subprocess as _sp
    from unittest import mock
    import workflow as _wf

    replies = ["rc1", "rc1", "ok"]

    def fake_run(cmd, **kw):
        r = replies.pop(0)
        if r == "rc1":
            return _sp.CompletedProcess(cmd, 1, stdout=_SIG_520, stderr="")
        return _sp.CompletedProcess(cmd, 0, stdout='{"slug": "a"}', stderr="")

    sleeps: list[float] = []
    monkeypatch.setattr(_wf, "_RETRY_SLEEP", sleeps.append)
    cfg = {"harnesses": {"pi": {"bin": "/bin/fakepi", "provider": "openrouter"}}}
    view = _wf.RunView("k", [_retry_stage()], "pi", out=io.StringIO())
    with mock.patch("subprocess.run", side_effect=fake_run):
        rc, value = _run_stage_pi(
            cfg, _retry_stage(), {"draft:a": {"model": "m", "effort": "x"}},
            {}, view=view)
    assert rc == 0 and value == {"slug": "a"}, (rc, value)
    assert sleeps == [15, 45], sleeps          # bounded, injected, never real
    att = view.state["draft:a"]["attempts"]
    assert [a["attempt"] for a in att] == [1, 2, 3], att
    assert [a["sleep_s"] for a in att] == [15, 45, 0], att
    assert all(a["signature"] == "error code: 520" for a in att[:2]), att
    assert view.state["draft:a"]["status"] == "ok"   # retried run ends ok
    err = capsys.readouterr().err
    assert "draft:a" in err and "attempt 1/3" in err and "15s" in err, err
    assert "error code: 520" in err, err


def test_non_transient_rc_is_never_retried(monkeypatch):
    """rc != 0 with NO 5xx signature -> rc 3 on the FIRST attempt, no sleep."""
    import subprocess as _sp
    from unittest import mock
    import workflow as _wf

    calls = []

    def fake_run(cmd, **kw):
        calls.append(cmd)
        return _sp.CompletedProcess(cmd, 1, stdout="boom: bad prompt", stderr="")

    sleeps: list[float] = []
    monkeypatch.setattr(_wf, "_RETRY_SLEEP", sleeps.append)
    cfg = {"harnesses": {"pi": {}}}
    with mock.patch("subprocess.run", side_effect=fake_run):
        rc, value = _run_stage_pi(
            cfg, _retry_stage(), {"draft:a": {"model": "m", "effort": "x"}}, {})
    assert rc == 3 and value is None, (rc, value)
    assert len(calls) == 1, calls
    assert sleeps == [], sleeps


def test_timeout_is_one_attempt_no_retry(monkeypatch):
    """A timeout is NOT transient: rc 2, exactly one attempt, no sleep."""
    import subprocess as _sp
    from unittest import mock
    import workflow as _wf

    calls = []

    def fake_run(cmd, **kw):
        calls.append(cmd)
        raise _sp.TimeoutExpired(cmd, 600)

    sleeps: list[float] = []
    monkeypatch.setattr(_wf, "_RETRY_SLEEP", sleeps.append)
    cfg = {"harnesses": {"pi": {}}}
    with mock.patch("subprocess.run", side_effect=fake_run):
        rc, value = _run_stage_pi(
            cfg, _retry_stage(), {"draft:a": {"model": "m", "effort": "x"}}, {})
    assert rc == 2 and value is None, (rc, value)
    assert len(calls) == 1, calls
    assert sleeps == [], sleeps


def test_a_timeout_says_timed_out_and_never_could_not_start(monkeypatch):
    """hypothesis:l4-the-harvest-reads-the-diff-per-deliverable-a-timeout-
    says-timed-out-and-the-done-tests-stay-hermetic item (3), from mur-sm-60,
    AND SM.70 item 3 here (landed independently, reconciled at a
    season2/main merge conflict): 30 min of pi spend, the refuter never ran,
    and the record said "could not start pi" because `TimeoutExpired` IS a
    `SubprocessError` and the string it carries buries the whole argv --
    prompt and all.

    A timeout is its OWN outcome: the budget the CALLER resolved, named
    first, and never the could-not-start wording. rc stays 2, one attempt,
    no retry/sleep -- a timeout is not treated as the transient 5xx case.
    """
    import subprocess as _sp
    from unittest import mock
    import workflow as _wf

    calls = []

    def fake_run(cmd, **kw):
        calls.append(cmd)
        raise _sp.TimeoutExpired(cmd, 42)

    sleeps: list[float] = []
    monkeypatch.setattr(_wf, "_RETRY_SLEEP", sleeps.append)
    cfg = {"harnesses": {"pi": {}}}
    st = _retry_stage()
    view = _wf.RunView("k", [st], "pi", out=io.StringIO())
    err = io.StringIO()
    with mock.patch("subprocess.run", side_effect=fake_run), \
         mock.patch.object(sys, "stderr", err):
        rc, value = _run_stage_pi(
            cfg, st, {"draft:a": {"model": "m", "effort": "x"}}, {},
            view=view, timeout_s=42)
    assert rc == 2 and value is None, (rc, value)
    assert len(calls) == 1 and sleeps == [], (calls, sleeps)
    msg = err.getvalue()
    assert "stage draft:a timed out after 42 s" in msg, msg
    assert "could not start pi" not in msg, msg
    detail = view.state["draft:a"].get("detail", "")
    assert detail.startswith("timed out after 42 s"), detail
    assert "could not start pi" not in detail, detail


def test_transient_5xx_exhausts_at_three_attempts(monkeypatch):
    """520 on every attempt -> rc 3 after exactly 3 calls, all named."""
    import subprocess as _sp
    from unittest import mock
    import workflow as _wf

    calls = []

    def fake_run(cmd, **kw):
        calls.append(cmd)
        return _sp.CompletedProcess(cmd, 1, stdout=_SIG_520, stderr="")

    sleeps: list[float] = []
    monkeypatch.setattr(_wf, "_RETRY_SLEEP", sleeps.append)
    cfg = {"harnesses": {"pi": {}}}
    view = _wf.RunView("k", [_retry_stage()], "pi", out=io.StringIO())
    with mock.patch("subprocess.run", side_effect=fake_run):
        rc, value = _run_stage_pi(
            cfg, _retry_stage(), {"draft:a": {"model": "m", "effort": "x"}},
            {}, view=view)
    assert rc == 3 and value is None, (rc, value)
    assert len(calls) == 3, calls
    assert sleeps == [15, 45], sleeps
    att = view.state["draft:a"]["attempts"]
    assert [a["attempt"] for a in att] == [1, 2, 3], att
    assert all(a["signature"] == "error code: 520" for a in att), att
    assert view.state["draft:a"]["status"] == "failed"


# ---------- lenient pi stage return: bare / fenced / prose ----------------
# hypothesis:l4-a-workflow-pi-stage-mints-its-own-capped-key-like-a-dispatched-
# spawn conjunct (h). The strict `find('{') : rfind('}')` parse lost a valid
# seven-finding review to one stray brace in prose (rc 4, refuter skipped). A
# pi stage now takes the FIRST balanced candidate that json.loads parses AND
# its schema validates; prose-only is `unstructured` (rc 0, whole text kept)
# and the run continues.

# JSON valid under BOTH review stages' schemas (extra keys allowed).
_REVIEW_BOTH_JSON = (
    '{"git_status": [], "links_broken": 0, "goals_check_ok": true, '
    '"summary": "s", "hypothesis": "h", "parent_agent": "p", '
    '"verdict": "v", "overclaims": [], "open_gaps": []}')

# Seven markdown findings with a stray `{` and no schema-valid JSON. The long
# distinctive tail substring is what a 120/200-char stub would have cut.
_PROSE_TAIL = "finding seven: the strict parse swallowed this whole review"
_REVIEW_PROSE = (
    "## Review findings\n"
    "1. the guard is { inert under g11\n"
    "2. links.py reports zero broken links\n"
    "3. GOALS.md round-trips byte-identically\n"
    "4. suite counts look sane\n"
    "5. no overclaims in the parent verdict\n"
    "6. one open gap remains: the refuter never ran\n"
    "7. " + _PROSE_TAIL + "\n")


def _fake_pi_bin(tmp_path: Path) -> Path:
    """A real fake pi executable: echoes a fixed stdout chosen by the prompt
    it is handed, and appends every prompt it receives to $FAKE_PI_CAPTURE so a
    test can assert what a LATER stage was actually given."""
    p = tmp_path / "fakepi"
    p.write_text(
        "#!/usr/bin/env python3\n"
        "import os, sys\n"
        "prompt = sys.argv[-1]\n"
        "cap = os.environ.get('FAKE_PI_CAPTURE')\n"
        "if cap:\n"
        "    with open(cap, 'a', encoding='utf-8') as fh:\n"
        "        fh.write('===PROMPT===\\n' + prompt + '\\n')\n"
        "mode = os.environ.get('FAKE_PI_MODE', 'bare')\n"
        "if 'You review one agi round target window' in prompt:\n"
        "    mode = 'bare'\n"
        "if 'prior text follows' in prompt:\n"
        "    sys.stdout.write('{\"ok\": true}')\n"
        "    sys.exit(0)\n"
        "if mode == 'prose':\n"
        "    sys.stdout.write(" + repr(_REVIEW_PROSE) + ")\n"
        "elif mode == 'fenced':\n"
        "    sys.stdout.write('Here is the review:\\n```json\\n'"
        "                     + " + repr(_REVIEW_BOTH_JSON) + " + '\\n```\\nthanks')\n"
        "elif mode == 'yaml-fenced':\n"
        "    sys.stdout.write('Review:\\n```yaml\\n'"
        "                     + " + repr(_REVIEW_BOTH_JSON) + " + '\\n```\\nbyebye')\n"
        "else:\n"
        "    sys.stdout.write(" + repr(_REVIEW_BOTH_JSON) + ")\n",
        encoding="utf-8")
    p.chmod(0o755)
    return p


def _run_review_pi(tmp_path_factory, fake_bin: Path, mode: str,
                   monkeypatch, args: dict | None = None):
    """Drive a real pi run on the `review` manifest against `fake_bin`, with
    the sessions root redirected under tmp. Returns (rc, stdout_text, rows)."""
    import workflow as _wf
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    saved_cfg = _wf._load_config

    def cfg(root):
        c = json.loads(json.dumps(saved_cfg(root)))
        c.setdefault("harnesses", {}).setdefault("pi", {})["bin"] = str(fake_bin)
        return c

    monkeypatch.setenv("FAKE_PI_MODE", mode)
    monkeypatch.setenv("FAKE_PI_CAPTURE", str(tmp / "prompts.txt"))
    _wf._load_config = cfg
    try:
        buf = io.StringIO()
        rc = run_workflow(REPO / ".agi", "review", "pi",
                          args or {"targets": [{"window": "t1"}]}, False, out=buf)
        rows = []
        path = tmp / "sessions" / "workflows" / "review.jsonl"
        if path.exists():
            rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines()]
        return rc, buf.getvalue(), rows, tmp
    finally:
        _wf._load_config = saved_cfg
        restore()


def test_pi_bare_json_stage_is_ok(tmp_path_factory, tmp_path, monkeypatch):
    fake = _fake_pi_bin(tmp_path)
    rc, text, rows, _tmp = _run_review_pi(tmp_path_factory, fake, "bare",
                                          monkeypatch)
    assert rc == 0, text
    assert "└─ [✓] review:t1" in text
    assert "[summary] workflow=review stages=2 ok=2 unstructured=0 failed=0" in text
    assert rows and rows[0]["ok"] == 2 and rows[0]["unstructured"] == 0


def test_pi_fenced_json_stage_is_ok_with_prose_around_it(tmp_path_factory,
                                                          tmp_path, monkeypatch):
    fake = _fake_pi_bin(tmp_path)
    rc, text, rows, _tmp = _run_review_pi(tmp_path_factory, fake, "fenced",
                                          monkeypatch)
    assert rc == 0, text
    assert "[summary] workflow=review stages=2 ok=2 unstructured=0 failed=0" in text
    # fenced parse resolves EXACTLY the same object the bare case did
    assert rows[0]["stages"] == {"global-checks": "ok", "review:t1": "ok"}, rows


def test_pi_yaml_fenced_json_stage_is_ok(tmp_path_factory, tmp_path, monkeypatch):
    """hypothesis:l4-pi-review-stages-return-structured-reports item (2): a
    ```yaml fence whose payload is JSON bytes is lifted like a ```json fence.
    The model tagged the block `yaml` but the block holds JSON, which is the
    residue that used to read `unstructured`."""
    fake = _fake_pi_bin(tmp_path)
    rc, text, rows, _tmp = _run_review_pi(tmp_path_factory, fake, "yaml-fenced",
                                          monkeypatch)
    assert rc == 0, text
    assert "[summary] workflow=review stages=2 ok=2 unstructured=0 failed=0" in text
    assert rows[0]["stages"] == {"global-checks": "ok", "review:t1": "ok"}, rows


def test_pi_prose_stage_is_unstructured_not_failed(tmp_path_factory, tmp_path,
                                                    monkeypatch):
    """The defect, end to end: seven findings with a stray `{` -> the stage is
    `unstructured` (rc 0), the NEXT stage still runs, the whole text is carried
    in the tracking row, and the next stage's prompt received it."""
    fake = _fake_pi_bin(tmp_path)
    # A run where the prose stage is CHAINED INTO by a second stage whose
    # prompt names the whole text, so prior-threading is directly asserted.
    import workflow as _wf
    manifest = {
        "name": "review", "type": "review", "script": "agi-round-review.js",
        "stages": [
            {"label": "find", "role": "kid", "model_hint": "sonnet",
             "effort_hint": "low",
             "repeat": {"of": "targets", "label_template": "find:{window}"},
             "prompt": "find things",
             "schema": {"type": "object", "properties": {"a": {"type": "string"}},
                        "required": ["a"]}},
            {"label": "refute", "role": "reviewer", "model_hint": "sonnet",
             "effort_hint": "medium", "chained_from": "find",
             "repeat": {"of": "targets", "label_template": "refute:{window}"},
             "prompt": "prior text follows:\n{unstructured}\nend prior",
             "schema": {"type": "object", "properties": {"ok": {"type": "boolean"}},
                        "required": ["ok"]}},
        ],
    }
    saved_manifest = _wf._load_manifest

    def load(repo, key):
        return manifest

    import workflow as _wf2
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf2)
    saved_cfg = _wf2._load_config

    def cfg(root):
        c = json.loads(json.dumps(saved_cfg(root)))
        c.setdefault("harnesses", {}).setdefault("pi", {})["bin"] = str(fake)
        return c

    monkeypatch.setenv("FAKE_PI_MODE", "prose")
    cap = tmp / "prompts.txt"
    monkeypatch.setenv("FAKE_PI_CAPTURE", str(cap))
    _wf2._load_manifest = load
    _wf2._load_config = cfg
    try:
        buf = io.StringIO()
        rc = run_workflow(REPO / ".agi", "review", "pi",
                          {"targets": [{"window": "t1"}]}, False, out=buf)
        text = buf.getvalue()
        assert rc == 0, text  # prose is NOT a failure; the chain is not cut
        assert "[summary] workflow=review stages=2 ok=1 unstructured=1 failed=0" in text
        assert "[?] find:t1" in text
        assert "[✓] refute:t1" in text, "the next stage must still run"
        rows = [json.loads(l) for l in
                (tmp / "sessions" / "workflows" / "review.jsonl")
                .read_text(encoding="utf-8").splitlines()]
        assert rows[0]["unstructured"] == 1 and rows[0]["failed"] == 0
        assert rows[0]["stages"] == {"find:t1": "unstructured", "refute:t1": "ok"}
        # the WHOLE text, not a 120/200-char stub
        assert rows[0]["returns"]["find:t1"] == _REVIEW_PROSE
        assert _PROSE_TAIL in rows[0]["returns"]["find:t1"]
        # the next stage's rendered prompt actually carried it
        prompts = cap.read_text(encoding="utf-8")
        assert ("prior text follows:\n" + _REVIEW_PROSE) in prompts, prompts
        # `workflow.py status` surfaces the new column
        sbuf = io.StringIO()
        from workflow import status_workflow
        assert status_workflow(tmp, "review", out=sbuf) == 0
        assert "unstructured=1" in sbuf.getvalue(), sbuf.getvalue()
    finally:
        _wf2._load_manifest = saved_manifest
        _wf2._load_config = saved_cfg
        restore()


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
        if "--provider" in cmd:
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
        assert "[summary] workflow=prime-open-questions stages=2 ok=2 unstructured=0 failed=0" \
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
        assert tail[-1] == "[summary] workflow=review stages=2 ok=1 unstructured=0 failed=1", tail
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


def test_pi_live_run_renders_tree_through_view(tmp_path_factory):
    """The pi path redraws the stage tree live per event and ends with the
    same summary shape — no more flat log lines. Tracking is redirected to a
    tmp root: this NON-dry pi run (stages mocked) tracked one real row per
    suite run from MAIN (review-16/17, merge-up 40) — the same leak L4.286
    closed for the claude-code sibling below."""
    import subprocess as _sp
    from unittest import mock
    import workflow as _wf
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    try:
        _pi_live_run_body(_sp, mock, run_workflow)
    finally:
        restore()


def _pi_live_run_body(_sp, mock, run_workflow):
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
    assert "[summary] workflow=review stages=2 ok=2 unstructured=0 failed=0" in text
    assert "[claude-code]" not in text and "[ok]" not in text


def _clear_cc_seam(monkeypatch):
    """Clear the three live Claude Code seam vars for the duration of a test.

    The Bash tool that runs pytest inherits `CLAUDECODE=1`,
    `CLAUDE_CODE_SESSION_ID` and `CLAUDE_CODE_MESSAGING_SOCKET`, so a test that
    calls `run_workflow(..., "claude-code", ...)` directly and means to test the
    seam-ABSENT path must clear them explicitly — otherwise detection silently
    reroutes it onto the native-handback branch.
    """
    for var in workflow.CLAUDE_CODE_SEAM_VARS:
        monkeypatch.delenv(var, raising=False)


def test_claude_code_path_feeds_the_same_view(tmp_path_factory, monkeypatch):
    # Seam-ABSENT path: clear the ambient Claude Code markers the pytest Bash
    # tool exports, or this test hits the native-handback branch instead.
    _clear_cc_seam(monkeypatch)
    # This test predated the tmp-path tracking seam its neighbours use and
    # ran a NON-dry claude-code workflow against the REAL project root, so
    # `_track_run` appended one phantom row to the production
    # `.agi/sessions/workflows/review.jsonl` on EVERY suite run
    # (hypothesis:l4-a-workflow-test-tracks-no-row-outside-tmp). Redirect
    # the SESSIONS resolver through the same `_tmp_session_root` seam the
    # tracking tests below use -- never the real path.
    import workflow as _wf
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    try:
        buf = io.StringIO()
        rc = run_workflow(REPO / ".agi", "review", "claude-code",
                          {"targets": [{"window": "t1"}]}, False, out=buf)
        assert rc == 0
        text = buf.getvalue()
        assert "workflow review (harness=claude-code)" in text
        assert "[·] global-checks" in text      # resolved, not executed here
        tail = [l for l in text.splitlines()
                if l.startswith(("[stage]", "[summary]"))]
        assert tail[-1] == "[summary] workflow=review stages=2 ok=0 unstructured=0 failed=0", tail
        assert all("claude-code" not in l for l in tail), tail
        # Tracking still happens, but ONLY into the throwaway seam -- one
        # row under tmp, never the real `.agi/sessions/workflows/`.
        lines = (tmp / "sessions" / "workflows" / "review.jsonl")\
            .read_text(encoding="utf-8").splitlines()
        assert len(lines) == 1, lines
    finally:
        restore()


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


def test_real_cc_run_appends_exactly_one_row(tmp_path_factory, monkeypatch):
    _clear_cc_seam(monkeypatch)
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


# ---------- suite-wide leak guard: no row may reach the REAL sessions dir  --
# The class of defect :630 used to be: a workflow test that runs a NON-dry
# workflow against the real project root appends a phantom row to the
# production `.agi/sessions/workflows/<key>.jsonl` on every suite run. The
# per-test tmp seam fixes the known instance; this session fixture pins the
# OUTCOME so any FUTURE test that leaks a row -- by using the wrong root, by
# forgetting the seam, or by a new non-dry path -- is red at session end
# (hypothesis:l4-a-workflow-test-tracks-no-row-outside-tmp).


@pytest.fixture(scope="session", autouse=True)
def _no_workflow_row_leaks_to_real_sessions():
    """Assert NO workflow row tracked by THIS pytest process reached a real
    sessions dir.

    The previous body compared `.agi/sessions/workflows/*.jsonl` LINE COUNTS
    at session start and session end and called any change a leak
    (hypothesis:l4-a-workflow-test-tracks-no-row-outside-tmp). That is
    unsound under concurrency: the shared `<main>/.agi/sessions/workflows/` is
    LIVE production state, written by every seat on the box through
    `workflow.py run` -> `_track_run` -> `shared_project_root`. Measured
    2026-09-16: `{"run_key": "mur-sm-36", "workflow": "merge-up-review",
    "harness": "pi", "timestamp": "2026-09-16T11:57:04.916706+00:00"}` -- a
    live season merge-up review, not a test artefact -- landed in
    merge-up-review.jsonl during a suite run, and the resulting session
    teardown ERROR was reported against whichever test pytest collected LAST
    (`test_zoom.py::test_no_source_comment_cites_an_unresolvable_tier_node_id`
    in one run, `schema_registry/test_validation.py::test_errors_do_not_abort`
    in another) -- the "only inside the full suite" signature. The count
    helper could not tell a concurrent seat's row from the suite's own.

    Attribution is now per-PROCESS, not per-file: wrapping `_track_run`
    records only writes made by this pytest process, and a concurrent seat
    running in its own process can never enter the wrapper. A real leak to a
    real root is still caught, and only a real leak.
    """
    import tempfile

    import workflow as _wf

    real_track = _wf._track_run
    leaked: list[str] = []

    def _watched(root, key, harness, view, run_key=None):
        try:
            sess = _wf._loc.shared_project_root(root) or root
        except Exception:  # a test may stub the resolver to blow up
            sess = None
        if sess is not None:
            wf_dir = Path(sess) / "sessions" / "workflows"
            if not str(wf_dir).startswith(tempfile.gettempdir()):
                leaked.append(str(wf_dir))
        return real_track(root, key, harness, view, run_key)

    _wf._track_run = _watched
    try:
        yield
    finally:
        _wf._track_run = real_track
    assert not leaked, (
        "workflow tests leaked rows into the real sessions dir "
        f"(changed/added: {sorted(leaked)}); a non-dry workflow run test "
        "must redirect tracking to a tmp root via _tmp_session_root, never "
        "run against the real project root."
    )


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
    rows (nine since merge-up-review, desktop-check, and trove-survey),
    `workflow.py list` on the REAL registry shows every registered
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
            # trove-survey: registered by the Prime (owner 2026-09-14 01:38Z,
            # commit 2c78f3edf, config:workflows row) alongside the
            # thought-master/local-maxxing town bootstrap.
            {"name": "trove-survey", "harness": "claude-code"},
            # recovery-survey: registered by the Prime belam gen 21
            # (2026-09-16, commit 5180aa1a6): a re-seated Prime learns a
            # bounded window by NAME (survey:{key} -> refute:{key}).
            {"name": "recovery-survey", "harness": "claude-code"},
            # g15-close-triage: registered by the Prime belam gen 24
            # (2026-09-16, commit 23d3b8c2b): the L4 CLOSE retire-or-keep over
            # the experiment-less g15 hypotheses (triage:{key} -> refute:{key}).
            {"name": "g15-close-triage", "harness": "claude-code"},
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
            {"name": "trove-survey", "type": "trove-survey"},
            {"name": "recovery-survey", "type": "recovery-survey"},
            {"name": "g15-close-triage", "type": "g15-close-triage"},
        ],
    ), encoding="utf-8")
    monkeypatch.setattr(workflow, "_geometry_node_path", lambda root: node)
    buf = io.StringIO()
    rc = list_workflows(REPO / ".agi", out=buf)
    assert rc == 0, buf.getvalue()
    txt = buf.getvalue()
    for k in ("deep-search", "drafting", "l3w-route-probe",
              "l4-plan-research", "prime-open-questions", "review",
              "merge-up-review", "desktop-check", "trove-survey"):
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
    # merge-up review of merge-up 40 (REAL arg shape: list of dicts, two
    # rounds both carrying merge_up 40 -> DEDUPED to one token, never 40-40)
    assert _mint_run_key(tmp_path, "merge-up-review", {"rounds": [
        {"merge_up": 40, "key": "L4.288"},
        {"merge_up": 40, "key": "L4.289"}]}) == "mur-40"
    # SL1#2 merge_up cell -> slugified to sl1-2
    assert _mint_run_key(tmp_path, "merge-up-review",
                         {"rounds": [{"merge_up": "SL2#2"}]}) == "mur-sl2-2"
    # a DESCRIPTOR cell: `42 (point, mur-42 window)` slugs its LEADING token
    # `42`, exactly like the bare integer 42, and the two dedupe to ONE token
    assert _mint_run_key(tmp_path, "merge-up-review", {"rounds": [
        {"merge_up": "42 (point, mur-42 window)", "key": "L4.301"},
        {"merge_up": 42, "key": "L4.302"}]}) == "mur-42"
    assert _mint_run_key(tmp_path, "merge-up-review", {"rounds": [
        {"merge_up": "42 (point)"},
        {"merge_up": 40}]}) == "mur-42-40"
    # a round with no merge_up cell names itself by its key cell
    assert _mint_run_key(tmp_path, "merge-up-review",
                         {"rounds": [{"key": "L4.288"}]}) == "mur-l4-288"
    # author/validate keep their whole name with no run args
    assert _mint_run_key(tmp_path, "author", {}) == "author"
    assert _mint_run_key(tmp_path, "validate", {}) == "validate"
    # a single-word key keeps its name and joins the slugged scalar arg
    assert _mint_run_key(tmp_path, "review",
                         {"window": "SL1#2"}) == "review-sl1-2"
    # bare scalar arg cell (legacy `n` shape) stays a scalar
    assert _mint_run_key(tmp_path, "merge-up-review",
                         {"n": 39}) == "mur-39"


def test_mint_run_key_collision_appends_suffix(tmp_path_factory):
    import workflow as _wf
    from workflow import _mint_run_key
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    try:
        assert _mint_run_key(tmp, "merge-up-review",
                             {"rounds": [{"merge_up": 40, "key": "L4.288"}]
                              }) == "mur-40"
        # a tracked row already claimed mur-40 -> deterministic -2, -3
        wf_dir = tmp / "sessions" / "workflows"
        wf_dir.mkdir(parents=True, exist_ok=True)
        path = wf_dir / "merge-up-review.jsonl"
        for rk in ("mur-40", "mur-40-2"):
            with open(path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps({"run_key": rk,
                                     "workflow": "merge-up-review"}) + "\n")
        assert _mint_run_key(tmp, "merge-up-review",
                             {"rounds": [{"merge_up": 40, "key": "L4.288"}]
                              }) == "mur-40-3"
    finally:
        restore()


# A run_key minted from a long `why`/args blob (brainstorm's shape: idea id +
# whole why sentence + max_hypotheses, all slugged and joined) can run well
# past the ~255-byte filesystem limit on a single path component. Measured:
# `_persist_stage_value` used the raw run_key as a directory name, mkdir threw
# `File name too long`, the broad except swallowed it, and the stage's
# structured return was never written to disk -- the chained stage then read
# back only the 200-char in-process preview and failed schema validation
# (director gen 6, commit 453445d60: both brainstorm stages "recorded
# unstructured"). hypothesis: the fix bounds the PATH COMPONENT only, and
# leaves the descriptive run_key (used for reporting/citing) untouched.

def test_run_key_path_component_bounds_long_keys():
    from workflow import _run_key_path_component
    short = "mur-40"
    assert _run_key_path_component(short) == short
    long_key = "brainstorm-idea-lm-why-jev-echoes-leaked-verdicts-" + "x" * 300
    out = _run_key_path_component(long_key)
    assert len(out.encode("utf-8")) <= 200
    # deterministic and distinguishable: two long keys sharing a prefix must
    # not collide on the same truncated directory
    other_long_key = "brainstorm-idea-lm-why-jev-echoes-leaked-verdicts-" + "y" * 300
    assert out != _run_key_path_component(other_long_key)
    assert out == _run_key_path_component(long_key)  # deterministic


def test_persist_stage_value_survives_a_long_run_key(tmp_path_factory):
    import json as _json
    import workflow as _wf
    from workflow import _persist_stage_value
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    long_key = "brainstorm-idea-lm-why-jev-echoes-leaked-verdicts-" + "z" * 300
    try:
        _persist_stage_value(tmp, long_key, "brainstorm", {"a": "structured"})
        runs_dir = tmp / "sessions" / "workflows" / "runs"
        written = list(runs_dir.glob("*/brainstorm.json"))
        assert len(written) == 1, list(runs_dir.iterdir())
        assert _json.loads(written[0].read_text()) == {"a": "structured"}
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


# ---------- per-run minted credential for pi stages -------------------------
# hypothesis:l4-a-workflow-pi-stage-mints-its-own-capped-key-like-a-dispatched
# -spawn conjuncts (a)-(f): a pi workflow stage used to inherit whatever
# OPENROUTER_API_KEY the caller shell carried; now ONE capped key is minted
# per RUN through the same provisioning seam dispatch.py uses.

_GOOD_REVIEW_JSON = (
    '{"git_status": [], "links_broken": 0, "goals_check_ok": true, '
    '"summary": "s", "hypothesis": "h", "parent_agent": "p", '
    '"verdict": "v", "overclaims": [], "open_gaps": []}')


def _fake_minted(secret="sk-minted-run"):
    import workflow as _wf
    return _wf.provisioning.MintedKey(
        secret=secret, key_hash="hash-" + secret, name="agi-test-key",
        limit_usd=5.0, expires_at="2030-01-01T00:00:00Z")


def test_pi_run_mints_one_credential_for_all_stages(tmp_path_factory,
                                                    monkeypatch):
    """(a)+(c): every pi stage's env carries the MINTED secret, and a
    two-stage run mints exactly ONCE — one key per run, not per stage. Two
    keys for one run is an explicit falsifier on the target node."""
    import subprocess as _sp
    from unittest import mock
    import workflow as _wf
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    seen = []

    def fake_run(cmd, **kw):
        if "--provider" in cmd:
            seen.append(kw.get("env") or {})
        return _sp.CompletedProcess(cmd, 0, stdout=_GOOD_REVIEW_JSON,
                                    stderr="")

    calls = []

    def fake_mint(**kw):
        calls.append(kw)
        return _fake_minted()

    monkeypatch.setattr(_wf.provisioning, "available", lambda root=None: True)
    monkeypatch.setattr(_wf.provisioning, "mint", fake_mint)
    try:
        buf = io.StringIO()
        with mock.patch("subprocess.run", side_effect=fake_run):
            rc = run_workflow(REPO / ".agi", "review", "pi",
                              {"targets": [{"window": "t1"}]}, False, out=buf)
        assert rc == 0, buf.getvalue()
        assert len(seen) == 2, seen            # global-checks + review:t1
        for env in seen:
            assert env.get("OPENROUTER_API_KEY") == "sk-minted-run", env
        assert len(calls) == 1, calls          # ONE mint for TWO stages
        # (b) the key NAME carries the run key: `workflow:<run_key>`
        kw = calls[0]
        assert kw["agent_id"].startswith("workflow:"), kw
        assert str(kw["iter_n"]) in kw["agent_id"], kw
        assert kw["agent_id"] == f"workflow:{kw['iter_n']}", kw
        # limit/ttl/workspace come from provisioning.settings/workspace(cfg):
        # compare against the LIVE cells, never a literal -- the cap is a
        # Prime config edit and a pinned 5.0 turned the suite red at 5de4ef940
        _cred = json.loads((REPO / ".agi" / "config.json").read_text())["spawn"]["credential"]
        assert kw["limit_usd"] == float(_cred["per_spawn_limit_usd"]), kw
        assert kw["ttl_minutes"] == int(_cred["ttl_minutes"]), kw
        assert kw["workspace_id"] == _cred["workspace_id"], kw
    finally:
        restore()


def test_pi_dry_run_prints_credential_line_before_dispatch(monkeypatch):
    """(d): `--dry-run` names the credential decision BEFORE the per-stage
    dispatch lines, from the SAME decision helper the live path uses — and
    never mints (available/needs_credential are reads)."""
    import workflow as _wf
    from workflow import run_workflow
    called = []
    monkeypatch.setattr(_wf.provisioning, "available", lambda root=None: True)
    monkeypatch.setattr(_wf.provisioning, "mint",
                        lambda **kw: called.append(kw))
    buf = io.StringIO()
    rc = run_workflow(REPO / ".agi", "review", "pi",
                      {"targets": [{"window": "t1"}]}, True, out=buf)
    assert rc == 0, buf.getvalue()
    lines = buf.getvalue().splitlines()
    cred = [i for i, l in enumerate(lines) if l.startswith("[credential]")]
    disp = [i for i, l in enumerate(lines) if l.startswith("[dispatch]")]
    assert len(cred) == 1 and disp and cred[0] < disp[0], lines
    assert lines[cred[0]] == "[credential] mint per-run", lines
    assert called == [], called


def test_dry_run_credential_line_matches_live_decision():
    """(d) the printed line and the live choice come from one helper — a
    claude-code harness needs no credential, and its dry-run line says so."""
    import workflow as _wf
    from workflow import run_workflow
    would, reason = _wf._credential_decision(REPO / ".agi",
                                             _wf._load_config(REPO / ".agi"),
                                             "claude-code")
    assert would is False and "needs no credential" in reason, (would, reason)
    buf = io.StringIO()
    run_workflow(REPO / ".agi", "review", "claude-code",
                 {"targets": [{"window": "t1"}]}, True, out=buf)
    cred = [l for l in buf.getvalue().splitlines()
            if l.startswith("[credential]")]
    assert cred == [f"[credential] inherited env ({reason})"], cred


def test_pi_fallback_prints_one_named_line_when_provisioning_absent(
        tmp_path_factory, monkeypatch, capsys):
    """(a)/(f): provisioning unavailable -> inherited env, EXACTLY ONE stderr
    line naming the reason, and no mint attempted."""
    import subprocess as _sp
    from unittest import mock
    import workflow as _wf
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    called = []
    monkeypatch.setattr(_wf.provisioning, "available", lambda root=None: False)
    monkeypatch.setattr(_wf.provisioning, "mint",
                        lambda **kw: called.append(kw))
    try:
        buf = io.StringIO()
        with mock.patch("subprocess.run",
                        side_effect=lambda cmd, **kw: _sp.CompletedProcess(
                            cmd, 0, stdout=_GOOD_REVIEW_JSON, stderr="")):
            rc = run_workflow(REPO / ".agi", "review", "pi",
                              {"targets": [{"window": "t1"}]}, False, out=buf)
        assert rc == 0, buf.getvalue()
        assert called == []
        err = [l for l in capsys.readouterr().err.splitlines() if l.strip()]
        assert err == ["workflow.py: [credential] inherited env "
                       "(provisioning unavailable)"], err
    finally:
        restore()


def test_prose_stage_persists_whole_return(tmp_path_factory, monkeypatch):
    """(item 1) a pi stage that returns prose persists its WHOLE return to
    `runs/<run_key>/<label>.json` (rc 0), and the jsonl row records the run_key
    plus the unstructured full return — never the 200-char tree view."""
    import workflow as _wf
    fake = _fake_pi_bin(tmp_path_factory.mktemp("pi"))
    rc, buf, rows, tmp = _run_review_pi(
        tmp_path_factory, fake, "prose", monkeypatch)
    assert rc == 0, rc
    assert rows, "no jsonl row tracked"
    run_key = rows[0].get("run_key")
    assert run_key, rows[0]
    assert rows[0].get("unstructured", 0) >= 1, rows[0]
    runs = tmp / "sessions" / "workflows" / "runs" / run_key
    persisted = sorted(p for p in runs.iterdir() if p.suffix == ".json")
    assert persisted, f"no persisted stage files under {runs}"
    text = persisted[0].read_text(encoding="utf-8")
    assert _PROSE_TAIL in text, "prose tail missing (persist truncated)"
    assert len(text) > 200, f"persisted return is flat ({len(text)} chars)"
    # the reading side records the unstructured full prose too, not a stub
    rets = {lb: d for lb, d in rows[0].get("returns", {}).items()}
    assert rets, rows[0]
    assert any(_PROSE_TAIL in (d or "") for d in rets.values()), rets


def test_pi_mint_error_refuses_when_inherited_key_unusable(tmp_path_factory,
                                                              monkeypatch,
                                                              capsys):
    """(item 5a) a failed mint REFUSES rc 3 naming the mint error verbatim
    when the inherited key is NOT usable — no stage runs, no silent fallback
    onto a credential nothing verified."""
    import subprocess as _sp
    from unittest import mock
    import workflow as _wf
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    monkeypatch.setattr(_wf.provisioning, "available", lambda root=None: True)

    def boom(**kw):
        raise _wf.provisioning.ProvisioningError("HTTP 401 nope")

    monkeypatch.setattr(_wf.provisioning, "mint", boom)
    monkeypatch.setattr(_wf.provisioning, "check_runtime_key_usable",
                        lambda cfg, root=None: (False, "dead key"))
    try:
        buf = io.StringIO()
        with mock.patch("subprocess.run") as run:
            rc = run_workflow(REPO / ".agi", "review", "pi",
                              {"targets": [{"window": "t1"}]}, False, out=buf)
        assert rc == 3, rc
        assert not run.called, run.call_args_list
        err = capsys.readouterr().err
        assert "ERR: could not mint a workflow credential: HTTP 401 nope" in err
        assert "refusing stage" in err
    finally:
        restore()


def test_pi_mint_error_runs_inherited_env_when_verified(tmp_path_factory,
                                                        monkeypatch,
                                                        capsys):
    """(item 5b) a failed mint RUNS the stage on the inherited env when it is
    proven usable, with the named `[credential] inherited env, verified` line."""
    import subprocess as _sp
    from unittest import mock
    import workflow as _wf
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    monkeypatch.setattr(_wf.provisioning, "available", lambda root=None: True)

    def boom(**kw):
        raise _wf.provisioning.ProvisioningError("HTTP 401 nope")

    monkeypatch.setattr(_wf.provisioning, "mint", boom)
    monkeypatch.setattr(_wf.provisioning, "check_runtime_key_usable",
                        lambda cfg, root=None: (True, None))
    try:
        buf = io.StringIO()
        with mock.patch("subprocess.run",
                        side_effect=lambda cmd, **kw: _sp.CompletedProcess(
                            cmd, 0, stdout=_GOOD_REVIEW_JSON, stderr="")):
            rc = run_workflow(REPO / ".agi", "review", "pi",
                              {"targets": [{"window": "t1"}]}, False, out=buf)
        assert rc == 0, buf.getvalue()
        err = capsys.readouterr().err
        assert "[credential] inherited env, verified" in err, err
    finally:
        restore()


def test_claude_code_path_mints_nothing(tmp_path_factory, monkeypatch):
    """(e): the claude-code branch never touches the credential seam and its
    emitted lines are unchanged."""
    _clear_cc_seam(monkeypatch)
    import workflow as _wf
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    called = []
    monkeypatch.setattr(_wf.provisioning, "available", lambda root=None: True)
    monkeypatch.setattr(_wf.provisioning, "mint",
                        lambda **kw: called.append(kw))
    try:
        buf = io.StringIO()
        rc = run_workflow(REPO / ".agi", "review", "claude-code",
                          {"targets": [{"window": "t1"}]}, False, out=buf)
        assert rc == 0
        assert called == []
        text = buf.getvalue()
        assert "workflow review (harness=claude-code)" in text
        assert "[credential]" not in text
        tail = [l for l in text.splitlines()
                if l.startswith(("[stage]", "[summary]"))]
        assert tail[-1] == "[summary] workflow=review stages=2 ok=0 unstructured=0 failed=0", tail
    finally:
        restore()


def test_pi_stage_receives_minted_key_across_the_process(tmp_path,
                                                         tmp_path_factory,
                                                         monkeypatch):
    """The fake-pi-bin proof: a REAL subprocess crosses the seam and writes
    its os.environ out, so the assertion is on the child's actual env, not on
    a mocked kwarg."""
    import workflow as _wf
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    env_out = tmp_path / "pi-env.json"
    fake = tmp_path / "fakepi"
    fake.write_text(
        "#!/usr/bin/env python3\n"
        "import json, os\n"
        f"open({str(env_out)!r}, 'w').write(json.dumps(dict(os.environ)))\n"
        f"print({_GOOD_REVIEW_JSON!r})\n",
        encoding="utf-8")
    fake.chmod(0o755)
    monkeypatch.setattr(
        _wf, "_pi_harness_cfg",
        lambda cfg: {"bin": str(fake), "provider": "openrouter",
                     "thinking": "medium"})
    monkeypatch.setattr(_wf.provisioning, "available", lambda root=None: True)
    monkeypatch.setattr(_wf.provisioning, "mint",
                        lambda **kw: _fake_minted(secret="sk-real-seam"))
    try:
        buf = io.StringIO()
        rc = run_workflow(REPO / ".agi", "review", "pi",
                          {"targets": [{"window": "t1"}]}, False, out=buf)
        assert rc == 0, buf.getvalue()
        child_env = json.loads(env_out.read_text(encoding="utf-8"))
        assert child_env.get("OPENROUTER_API_KEY") == "sk-real-seam", \
            child_env.get("OPENROUTER_API_KEY")
        assert "ANTHROPIC_API_KEY" not in child_env
    finally:
        restore()


# ---------- conjunct 2: the per-run minted key is REVOKED at run end --------
# hypothesis:l4-a-per-run-workflow-key-is-revoked-at-run-end-and-a-schema-miss-
# keeps-its-name. `_resolve_workflow_spawn_env` minted and dropped the hash, so
# nothing could revoke it and the key outlived the run on success, on stage
# failure and on a raise/timeout path.

def _revoke_spy(monkeypatch, _wf, result=True):
    calls = []

    def fake_revoke(key_hash, root=None):
        calls.append(key_hash)
        return result

    monkeypatch.setattr(_wf.provisioning, "revoke", fake_revoke)
    return calls


def _fake_pi_completed(_sp, rc=0, stdout=None):
    def fake_run(cmd, **kw):
        if "--provider" in cmd:
            return _sp.CompletedProcess(
                cmd, rc, stdout=stdout if stdout is not None
                else _GOOD_REVIEW_JSON, stderr="")
        return _sp.CompletedProcess(cmd, 0, stdout="CTX", stderr="")
    return fake_run


def test_pi_run_revokes_the_minted_key_once_on_success(tmp_path_factory,
                                                       monkeypatch):
    import subprocess as _sp
    from unittest import mock
    import workflow as _wf
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    monkeypatch.setattr(_wf.provisioning, "available", lambda root=None: True)
    monkeypatch.setattr(_wf.provisioning, "mint", lambda **kw: _fake_minted())
    revoked = _revoke_spy(monkeypatch, _wf)
    try:
        buf = io.StringIO()
        with mock.patch("subprocess.run",
                        side_effect=_fake_pi_completed(_sp)):
            rc = run_workflow(REPO / ".agi", "review", "pi",
                              {"targets": [{"window": "t1"}]}, False, out=buf)
        assert rc == 0, buf.getvalue()
        assert revoked == ["hash-sk-minted-run"], revoked
    finally:
        restore()


def test_pi_run_revokes_the_minted_key_once_when_a_stage_fails(
        tmp_path_factory, monkeypatch):
    import subprocess as _sp
    from unittest import mock
    import workflow as _wf
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    monkeypatch.setattr(_wf.provisioning, "available", lambda root=None: True)
    monkeypatch.setattr(_wf.provisioning, "mint", lambda **kw: _fake_minted())
    revoked = _revoke_spy(monkeypatch, _wf)
    try:
        buf = io.StringIO()
        with mock.patch("subprocess.run",
                        side_effect=_fake_pi_completed(_sp, rc=1)):
            rc = run_workflow(REPO / ".agi", "review", "pi",
                              {"targets": [{"window": "t1"}]}, False, out=buf)
        assert rc != 0, buf.getvalue()
        assert revoked == ["hash-sk-minted-run"], revoked
    finally:
        restore()


def test_pi_run_with_no_mint_revokes_nothing(tmp_path_factory, monkeypatch):
    import subprocess as _sp
    from unittest import mock
    import workflow as _wf
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    monkeypatch.setattr(_wf.provisioning, "available", lambda root=None: False)
    revoked = _revoke_spy(monkeypatch, _wf)
    try:
        buf = io.StringIO()
        with mock.patch("subprocess.run",
                        side_effect=_fake_pi_completed(_sp)):
            rc = run_workflow(REPO / ".agi", "review", "pi",
                              {"targets": [{"window": "t1"}]}, False, out=buf)
        assert rc == 0, buf.getvalue()
        assert revoked == [], revoked
    finally:
        restore()


def test_revoke_failure_does_not_fail_the_run_but_is_named(
        tmp_path_factory, monkeypatch, capsys):
    import subprocess as _sp
    from unittest import mock
    import workflow as _wf
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    monkeypatch.setattr(_wf.provisioning, "available", lambda root=None: True)
    monkeypatch.setattr(_wf.provisioning, "mint", lambda **kw: _fake_minted())
    revoked = _revoke_spy(monkeypatch, _wf, result=False)
    try:
        buf = io.StringIO()
        with mock.patch("subprocess.run",
                        side_effect=_fake_pi_completed(_sp)):
            rc = run_workflow(REPO / ".agi", "review", "pi",
                              {"targets": [{"window": "t1"}]}, False, out=buf)
        assert rc == 0, buf.getvalue()
        assert revoked == ["hash-sk-minted-run"], revoked
        err = capsys.readouterr().err
        assert "revoke" in err and "hash-sk-minted-run" in err, err
    finally:
        restore()


# ---------- conjunct 5: the stage timeout comes from the manifest ----------

def _manifest_with_timeout(timeout_s=None, stage_timeout=None):
    st = {"label": "only", "role": "kid", "model_hint": "sonnet",
          "prompt": "do the thing",
          "schema": {"type": "object", "properties": {"ok": {"type": "boolean"}},
                     "required": ["ok"]}}
    if stage_timeout is not None:
        st["timeout_s"] = stage_timeout
    m = {"name": "review", "type": "review", "script": "agi-round-review.js",
         "stages": [st]}
    if timeout_s is not None:
        m["timeout_s"] = timeout_s
    return m


def _capture_timeouts(tmp_path_factory, monkeypatch, manifest):
    import subprocess as _sp
    from unittest import mock
    import workflow as _wf
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    saved_manifest = _wf._load_manifest
    _wf._load_manifest = lambda repo, key: manifest
    monkeypatch.setattr(_wf.provisioning, "available", lambda root=None: False)
    seen = []

    def fake_run(cmd, **kw):
        if "--provider" in cmd:
            seen.append(kw.get("timeout"))
            return _sp.CompletedProcess(cmd, 0, stdout='{"ok": true}',
                                        stderr="")
        return _sp.CompletedProcess(cmd, 0, stdout="CTX", stderr="")

    try:
        buf = io.StringIO()
        with mock.patch("subprocess.run", side_effect=fake_run):
            rc = run_workflow(REPO / ".agi", "review", "pi", {}, False, out=buf)
        assert rc == 0, buf.getvalue()
        return seen
    finally:
        _wf._load_manifest = saved_manifest
        restore()


def test_manifest_timeout_s_reaches_the_stage_subprocess(
        tmp_path_factory, monkeypatch):
    seen = _capture_timeouts(tmp_path_factory, monkeypatch,
                             _manifest_with_timeout(timeout_s=7))
    assert seen == [7], seen


def test_no_manifest_timeout_keeps_the_3600_default(tmp_path_factory,
                                                    monkeypatch):
    """SM.105: the undeclared default wall is 3600 s (was 600), so a stage
    that declares no timeout_s anywhere gets 60 minutes."""
    seen = _capture_timeouts(tmp_path_factory, monkeypatch,
                             _manifest_with_timeout())
    assert seen == [3600], seen


def test_per_stage_timeout_overrides_the_manifest(tmp_path_factory,
                                                  monkeypatch):
    seen = _capture_timeouts(
        tmp_path_factory, monkeypatch,
        _manifest_with_timeout(timeout_s=7, stage_timeout=3))
    assert seen == [3], seen


def _capture_timeouts_rc(tmp_path_factory, monkeypatch, manifest):
    """Like `_capture_timeouts`, but returns (rc, seen) so a REFUSED run can
    be asserted: `seen == []` is the observable that no stage was dispatched."""
    import subprocess as _sp
    from unittest import mock
    import workflow as _wf
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    saved_manifest = _wf._load_manifest
    _wf._load_manifest = lambda repo, key: manifest
    monkeypatch.setattr(_wf.provisioning, "available", lambda root=None: False)
    seen = []

    def fake_run(cmd, **kw):
        if "--provider" in cmd:
            seen.append(kw.get("timeout"))
            return _sp.CompletedProcess(cmd, 0, stdout='{"ok": true}',
                                        stderr="")
        return _sp.CompletedProcess(cmd, 0, stdout="CTX", stderr="")

    try:
        buf = io.StringIO()
        with mock.patch("subprocess.run", side_effect=fake_run):
            rc = run_workflow(REPO / ".agi", "review", "pi", {}, False, out=buf)
        return rc, seen
    finally:
        _wf._load_manifest = saved_manifest
        restore()


def test_manifest_timeout_zero_is_refused_by_name_before_any_stage(
        tmp_path_factory, monkeypatch, capsys):
    """A manifest timeout_s=0 must NOT reach subprocess.run(timeout=0) and
    silently kill every stage. Definition (a): refused by name, non-zero exit,
    ZERO stages dispatched (conjunct (5))."""
    rc, seen = _capture_timeouts_rc(
        tmp_path_factory, monkeypatch, _manifest_with_timeout(timeout_s=0))
    assert rc != 0, "a zero-second budget must refuse the run"
    assert seen == [], f"no stage may be dispatched under a 0 budget: {seen}"
    err = capsys.readouterr().err
    assert "timeout_s" in err and "0" in err, err


def test_stage_timeout_zero_overrides_manifest_600_and_is_refused(
        tmp_path_factory, monkeypatch, capsys):
    """A stage-level timeout_s=0 with a manifest timeout_s=600 proves the
    STAGE value is the one resolved (0 -> refused by name, no stage
    dispatched) rather than the manifest's 600 (which would have run)."""
    rc, seen = _capture_timeouts_rc(
        tmp_path_factory, monkeypatch,
        _manifest_with_timeout(timeout_s=600, stage_timeout=0))
    assert rc != 0
    assert seen == [], f"the manifest's 600 must not be used: {seen}"
    err = capsys.readouterr().err
    assert "only" in err and "0" in err, err
    assert "600" not in err, err


def test_negative_stage_timeout_is_refused_not_passed_through(
        tmp_path_factory, monkeypatch, capsys):
    rc, seen = _capture_timeouts_rc(
        tmp_path_factory, monkeypatch,
        _manifest_with_timeout(stage_timeout=-1))
    assert rc != 0
    assert seen == []
    assert "timeout_s" in capsys.readouterr().err


# ---------- conjunct 3 (SD.06 residue): --dry-run agrees with the live run
# on timeout_s, and conjunct 4: the refusal has its own return code ----------

def _dry_run_with_manifest(tmp_path_factory, monkeypatch, manifest):
    """Drive `--dry-run` with an injected manifest; returns (rc, stdout).

    Same shape as `_capture_timeouts_rc` but `dry_run=True`, so the credential
    and dispatch lines are captured instead of subprocess.run."""
    import workflow as _wf
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    saved_manifest = _wf._load_manifest
    _wf._load_manifest = lambda repo, key: manifest
    monkeypatch.setattr(_wf.provisioning, "available", lambda root=None: False)
    try:
        buf = io.StringIO()
        rc = run_workflow(REPO / ".agi", "review", "pi", {}, True, out=buf)
        assert not (tmp / "sessions").exists(), (
            "a dry run must not create a sessions dir")
        return rc, buf.getvalue()
    finally:
        _wf._load_manifest = saved_manifest
        restore()


def test_dry_run_refuses_an_invalid_timeout_exactly_as_the_live_run(
        tmp_path_factory, monkeypatch, capsys):
    """hypothesis:l4-sd06-residue-renumber-notice-fixture-dry-run-parity-
    refused-run-key conjunct (3). Pre-fix the `if dry_run:` return sat ABOVE
    the budget-resolution loop, so `--dry-run` printed the credential line,
    every dispatch line and `[summary]` and exited 0 for a manifest whose
    `timeout_s` the live run refuses — the dry run APPROVED a run that could
    not start. Each invalid shape must now refuse under `--dry-run` too, with
    the same rc 5 the live run gives and no dispatch/summary lines."""
    for manifest in (_manifest_with_timeout(timeout_s=0),
                     _manifest_with_timeout(stage_timeout=-1),
                     _manifest_with_timeout(stage_timeout="600")):
        rc, text = _dry_run_with_manifest(tmp_path_factory, monkeypatch,
                                          manifest)
        assert rc == 5, (rc, text)
        assert "[dispatch]" not in text, text
        assert "[summary]" not in text, text
        err = capsys.readouterr().err
        assert "timeout_s" in err, err


def test_dry_run_still_green_for_a_valid_timeout(tmp_path_factory,
                                                 monkeypatch):
    """Control for the parity fix: a valid budget still dry-runs to rc 0 with
    its dispatch and summary lines, so the refusal did not become a blanket
    refusal."""
    rc, text = _dry_run_with_manifest(
        tmp_path_factory, monkeypatch, _manifest_with_timeout(timeout_s=7))
    assert rc == 0, text
    assert "[dispatch]" in text and "[summary]" in text, text


def test_timeout_refusal_rc_is_distinct_from_the_stage_parse_error_rc(
        tmp_path_factory, monkeypatch):
    """conjunct (4). Pre-fix the timeout refusal returned 4 — the same value
    `_run_stage_pi` returns when a stage's output cannot be parsed — so a
    caller could not tell "refused before any stage ran" from "a stage ran and
    returned unparseable output". Both arms are DRIVEN here, not asserted from
    a comment: the parse-error arm by making `_resolve_lenient_return` raise
    (the only path that reaches its handler), the refusal arm by an invalid
    `timeout_s`. The two must differ."""
    import subprocess as _sp
    from unittest import mock
    import workflow as _wf
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    saved_manifest = _wf._load_manifest
    _wf._load_manifest = lambda repo, key: _manifest_with_timeout(timeout_s=7)
    monkeypatch.setattr(_wf.provisioning, "available", lambda root=None: False)

    def _boom(*a, **k):
        raise ValueError("forced schema failure")

    monkeypatch.setattr(_wf, "_resolve_lenient_return", _boom)

    def fake_run(cmd, **kw):
        if "--provider" in cmd:
            return _sp.CompletedProcess(cmd, 0, stdout='{"ok": true}',
                                        stderr="")
        return _sp.CompletedProcess(cmd, 0, stdout="CTX", stderr="")

    try:
        buf = io.StringIO()
        with mock.patch("subprocess.run", side_effect=fake_run):
            parse_rc = run_workflow(REPO / ".agi", "review", "pi", {},
                                    False, out=buf)
    finally:
        _wf._load_manifest = saved_manifest
        restore()
    assert parse_rc == 4, (
        f"the stage return-parse-error arm is rc 4, got {parse_rc}")

    refused_rc, seen = _capture_timeouts_rc(
        tmp_path_factory, monkeypatch, _manifest_with_timeout(timeout_s=0))
    assert refused_rc == 5, refused_rc
    assert seen == [], seen
    assert refused_rc != parse_rc, (
        "a refused-before-any-stage run must not share the stage parse-error "
        "return code")


def test_no_per_run_key_is_minted_for_a_timeout_refused_run(
        tmp_path_factory, monkeypatch):
    """conjunct (4), the mint half. The budget is resolved BEFORE
    `_resolve_workflow_spawn_env`, so a manifest that will be refused spends
    NO key: with provisioning 'available' and `mint` patched, a refused run
    must call it ZERO times."""
    import subprocess as _sp
    from unittest import mock
    import workflow as _wf
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    saved_manifest = _wf._load_manifest
    _wf._load_manifest = lambda repo, key: _manifest_with_timeout(timeout_s=0)
    monkeypatch.setattr(_wf.provisioning, "available", lambda root=None: True)
    minted = []
    monkeypatch.setattr(_wf.provisioning, "mint",
                        lambda **kw: minted.append(kw))
    try:
        buf = io.StringIO()
        with mock.patch("subprocess.run",
                        side_effect=lambda *a, **k: _sp.CompletedProcess(
                            [], 0, stdout="", stderr="")):
            rc = run_workflow(REPO / ".agi", "review", "pi", {}, False,
                              out=buf)
        assert rc == 5, (rc, buf.getvalue())
        assert minted == [], (
            f"a refused run must spend no key, minted {len(minted)}")
    finally:
        _wf._load_manifest = saved_manifest
        restore()


# ---------- conjunct 3: a schema miss keeps its violation -------------------

def _run_one_stage_with_output(tmp_path_factory, monkeypatch, output,
                               schema=None):
    import subprocess as _sp
    from unittest import mock
    import workflow as _wf
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    saved_manifest = _wf._load_manifest
    manifest = {"name": "review", "type": "review",
                "script": "agi-round-review.js",
                "stages": [{"label": "only", "role": "kid",
                            "model_hint": "sonnet", "prompt": "p",
                            "schema": schema if schema is not None else
                            {"type": "object",
                             "properties": {"answer": {"type": "integer"}},
                             "required": ["answer"]}}]}
    _wf._load_manifest = lambda repo, key: manifest
    monkeypatch.setattr(_wf.provisioning, "available", lambda root=None: False)

    def fake_run(cmd, **kw):
        if "--provider" in cmd:
            return _sp.CompletedProcess(cmd, 0, stdout=output, stderr="")
        return _sp.CompletedProcess(cmd, 0, stdout="CTX", stderr="")

    try:
        buf = io.StringIO()
        with mock.patch("subprocess.run", side_effect=fake_run):
            rc = run_workflow(REPO / ".agi", "review", "pi", {}, False, out=buf)
        rows = []
        path = tmp / "sessions" / "workflows" / "review.jsonl"
        if path.exists():
            rows = [json.loads(l) for l in
                    path.read_text(encoding="utf-8").splitlines()]
        return rc, buf.getvalue(), rows
    finally:
        _wf._load_manifest = saved_manifest
        restore()


def test_schema_violation_is_recorded_on_the_unstructured_return(
        tmp_path_factory, monkeypatch):
    rc, text, rows = _run_one_stage_with_output(
        tmp_path_factory, monkeypatch, '{"answer": "x"}')
    assert rc == 0, text
    assert "[summary] workflow=review stages=1 ok=0 unstructured=1 failed=0" in text
    assert rows, "the run must be tracked"
    ret = rows[0]["returns"]["only"]
    assert ret == '{"answer": "x"}', ret
    viol = rows[0]["violations"]["only"]
    assert viol, rows[0]
    assert any("answer" in v for v in viol), viol


def test_later_valid_candidate_still_wins_after_a_schema_miss(
        tmp_path_factory, monkeypatch):
    rc, text, rows = _run_one_stage_with_output(
        tmp_path_factory, monkeypatch, '{"answer": "x"}\n{"answer": 4}')
    assert rc == 0, text
    assert "[summary] workflow=review stages=1 ok=1 unstructured=0 failed=0" in text
    assert rows[0]["returns"] == {}, rows[0]


# ---------- conjunct 3: the tree PREVIEWS, never inlines, a blob --------

def test_tree_previews_a_multi_kb_detail_while_tracking_keeps_it_whole(
        tmp_path_factory, monkeypatch):
    """A >= 4000-char unstructured return renders ONE tree line that is
    SHORTER than the input and names the exact omitted size, while the
    tracking row still holds the whole text character-for-character
    (hypothesis:l4-workflow-residue-sub-floor-marker-dead-code-and-truncation
    conjunct (3)). Numeric on both sides."""
    from workflow import _TREE_DETAIL_PREVIEW_CHARS
    output = "".join(f"prose line {i} of the model's stdout\n"
                     for i in range(300))
    assert len(output) >= 4000, len(output)
    rc, text, rows = _run_one_stage_with_output(
        tmp_path_factory, monkeypatch, output)
    assert rc == 0, text
    stage_lines = [l for l in text.splitlines() if l.startswith("└─ [?] only")]
    assert len(stage_lines) == 1, text
    tree_line = stage_lines[0]
    assert "\n" not in tree_line
    # The tree is the preview: strictly shorter than the blob it describes.
    assert len(tree_line) < len(output), (len(tree_line), len(output))
    flat_len = len(output.replace("\n", " "))
    omitted = flat_len - _TREE_DETAIL_PREVIEW_CHARS
    assert f"… (+{omitted} chars)" in tree_line, tree_line
    assert len(tree_line) == len("└─ [?] only — ") + _TREE_DETAIL_PREVIEW_CHARS + \
        len(f"… (+{omitted} chars)"), len(tree_line)
    # The tracking row still carries the whole text, unchanged.
    assert rows, "the run must be tracked"
    assert rows[0]["returns"]["only"] == output
    assert len(rows[0]["returns"]["only"]) == len(output)


# ---------- native handback: the seam, the one call, the link, the hook ------
# hypothesis:l4-same-harness-handback-a-claude-code-caller-gets-one-exact-native-
# workflow-call-every-engine-js-is-registered-and-a-hook-closes-the-record

def _set_cc_seam(monkeypatch):
    """Export the three live Claude Code seam markers so run_workflow takes the
    native-handback branch."""
    for var in workflow.CLAUDE_CODE_SEAM_VARS:
        monkeypatch.setenv(var, "test-value")


def test_cc_seam_helper_reads_an_explicit_env():
    assert workflow._claude_code_seam_present({}) is False
    full = {v: "x" for v in workflow.CLAUDE_CODE_SEAM_VARS}
    assert workflow._claude_code_seam_present(full) is True
    for var in workflow.CLAUDE_CODE_SEAM_VARS:
        partial = dict(full)
        partial.pop(var)
        assert workflow._claude_code_seam_present(partial) is False, var


def test_native_seam_prints_one_call_with_the_script_stem(tmp_path_factory,
                                                          monkeypatch, capsys):
    """A native session gets ONE exact Workflow call whose `name` is the
    REGISTERED script stem, never the config key. review -> agi-round-review,
    drafting -> agi-brief-drafting: a key-formatted name would not resolve as a
    `.claude/workflows/` link and the caller's copy-paste would fail."""
    import workflow as _wf
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    _set_cc_seam(monkeypatch)
    try:
        buf = io.StringIO()
        rc = run_workflow(REPO / ".agi", "review", "claude-code",
                          {"targets": [{"window": "t1"}]}, False, out=buf)
        err = capsys.readouterr().err
        assert rc == 0
        calls = [l for l in buf.getvalue().splitlines()
                 if l.startswith("Workflow(")]
        assert len(calls) == 1, calls
        parsed = json.loads(calls[0][len("Workflow("):-1])
        assert parsed["name"] == "agi-round-review", parsed
        # The caller's targets survive; the runner ALSO resolves the project
        # root into args so the native Workflow call carries it (the stages
        # `cd {project_root}`, never a hardcoded checkout).
        assert parsed["args"]["targets"] == [{"window": "t1"}], parsed
        assert parsed["args"]["project_root"] == str(REPO), parsed
        # the SM.120 stderr notice belongs to the headless path only
        assert "no stage executed by workflow.py" not in err, err
        # and the row is still tracked, still unnoted
        lines = (tmp / "sessions" / "workflows" / "review.jsonl")\
            .read_text(encoding="utf-8").splitlines()
        assert json.loads(lines[0])["harness_id"] == []
    finally:
        restore()


def test_native_seam_key_and_stem_diverge_for_drafting(tmp_path_factory,
                                                       monkeypatch):
    import workflow as _wf
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    _set_cc_seam(monkeypatch)
    try:
        buf = io.StringIO()
        rc = run_workflow(REPO / ".agi", "drafting", "claude-code",
                          {"briefs": [{"slug": "x"}]}, False, out=buf)
        assert rc == 0
        calls = [l for l in buf.getvalue().splitlines()
                 if l.startswith("Workflow(")]
        assert len(calls) == 1, calls
        assert json.loads(calls[0][len("Workflow("):-1])["name"] == \
            "agi-brief-drafting", calls
    finally:
        restore()


def test_no_seam_still_prints_the_stderr_notice(tmp_path_factory, monkeypatch,
                                                capsys):
    import workflow as _wf
    from workflow import run_workflow
    tmp, restore = _tmp_session_root(tmp_path_factory, _wf)
    _clear_cc_seam(monkeypatch)
    try:
        buf = io.StringIO()
        rc = run_workflow(REPO / ".agi", "review", "claude-code",
                          {"targets": [{"window": "t1"}]}, False, out=buf)
        assert rc == 0
        assert "no stage executed by workflow.py" in capsys.readouterr().err
        assert "Workflow(" not in buf.getvalue()
    finally:
        restore()


def test_link_creates_every_registered_script_and_is_idempotent(tmp_path,
                                                               monkeypatch):
    """After `link`, every real manifest's `script` resolves to a live symlink
    in the fixture's `.claude/workflows/`, and a second run creates 0."""
    from workflow import link_workflows
    scripts = set()
    for mf in sorted(WF_DIR.glob("*.json")):
        m = json.loads(mf.read_text(encoding="utf-8"))
        scripts.add(m["script"])
        (tmp_path / "extensions" / "agi" / "workflows" / mf.name).parent\
            .mkdir(parents=True, exist_ok=True)
        (tmp_path / "extensions" / "agi" / "workflows" / mf.name)\
            .write_text(json.dumps(m), encoding="utf-8")
        src = tmp_path / "extensions" / "agi" / "workflows" / m["script"]
        if not src.exists():
            src.write_text("// fixture\n", encoding="utf-8")
    graph = tmp_path / ".agi"
    graph.mkdir()
    (graph / "config.json").write_text("{}", encoding="utf-8")
    monkeypatch.setattr(workflow, "_repo_root", lambda root: tmp_path)
    buf = io.StringIO()
    assert link_workflows(graph, out=buf) == 0
    # Derived from the live manifests above, never a pinned literal: the
    # literal "12" drifted the moment a new workflow pair landed (TM.60,
    # research-review), which is the copied-list defect this assertion is
    # supposed to catch, not commit.
    assert f"[linked] {len(scripts)} workflow link(s) created" in buf.getvalue(), \
        buf.getvalue()
    for script in scripts:
        link = tmp_path / ".claude" / "workflows" / script
        assert link.is_symlink(), f"{link} not a symlink"
        assert link.resolve().is_file(), f"{link} does not resolve"
    buf2 = io.StringIO()
    assert link_workflows(graph, out=buf2) == 0
    assert "[linked] 0 workflow link(s) created" in buf2.getvalue()


def test_link_refuses_a_non_symlink_by_name(tmp_path, monkeypatch, capsys):
    from workflow import link_workflows
    wf = tmp_path / "extensions" / "agi" / "workflows"
    wf.mkdir(parents=True)
    (wf / "review.json").write_text(json.dumps(
        {"name": "review", "script": "agi-round-review.js"}))
    graph = tmp_path / ".agi"
    graph.mkdir()
    (graph / "config.json").write_text("{}", encoding="utf-8")
    links = tmp_path / ".claude" / "workflows"
    links.mkdir(parents=True)
    blocker = links / "agi-round-review.js"
    blocker.write_text("not a link\n", encoding="utf-8")
    monkeypatch.setattr(workflow, "_repo_root", lambda root: tmp_path)
    assert link_workflows(graph, out=io.StringIO()) == 2
    assert "link refused" in capsys.readouterr().err
    assert not blocker.is_symlink()
    assert blocker.read_text() == "not a link\n"


# ---------- the hook: reverse-map, last open row, note seam ------------------

def _load_hook():
    import importlib.util
    p = Path(__file__).resolve().parents[1] / "hooks" / "workflow_note.py"
    spec = importlib.util.spec_from_file_location("workflow_note", p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _hook_fixture(tmp_path):
    graph = tmp_path / ".agi"
    (graph / "sessions" / "workflows").mkdir(parents=True)
    (graph / "config.json").write_text("{}", encoding="utf-8")
    wf = tmp_path / "extensions" / "agi" / "workflows"
    wf.mkdir(parents=True)
    (wf / "review.json").write_text(json.dumps(
        {"name": "review", "script": "agi-round-review.js"}))
    return graph


def test_hook_plans_the_run_key_from_the_registered_name(tmp_path):
    """The reverse map is a manifest `script` read: a name formatted from the
    config key would not match `agi-round-review.js`."""
    hook = _load_hook()
    graph = _hook_fixture(tmp_path)
    (graph / "sessions" / "workflows" / "review.jsonl").write_text(
        json.dumps({"workflow": "review", "run_key": "mur-1",
                    "harness_id": ["wf_old"]}) + "\n" +
        json.dumps({"workflow": "review", "run_key": "mur-2",
                    "harness_id": []}) + "\n")
    payload = {"tool_name": "Workflow",
               "tool_input": {"name": "agi-round-review", "args": {}},
               "tool_response": {"runId": "wf_new"}}
    assert hook.plan_note(payload, graph) == ("mur-2", "wf_new")


def test_hook_accepts_the_ordered_id_keys(tmp_path):
    hook = _load_hook()
    graph = _hook_fixture(tmp_path)
    (graph / "sessions" / "workflows" / "review.jsonl").write_text(
        json.dumps({"workflow": "review", "run_key": "mur-1",
                    "harness_id": []}) + "\n")
    for key in ("runId", "run_id", "id"):
        payload = {"tool_name": "Workflow",
                   "tool_input": {"name": "agi-round-review"},
                   "tool_response": {key: "wf_x"}}
        assert hook.plan_note(payload, graph) == ("mur-1", "wf_x"), key


def test_hook_skips_named_on_everything_it_does_not_understand():
    hook = _load_hook()
    for payload in (
        {"tool_name": "Bash", "tool_input": {"name": "agi-round-review"}},
        {"tool_name": "Workflow", "tool_input": {"args": {}}},
        {"tool_name": "Workflow", "tool_input": {"name": "not-a-wf"}},
        {"tool_name": "Workflow", "tool_input": {"name": "agi-round-review"},
         "tool_response": {"nope": 1}},
    ):
        try:
            hook.plan_note(payload, Path("/nonexistent"))
            raise AssertionError(f"expected HookSkip for {payload}")
        except hook.HookSkip as exc:
            assert str(exc)


def test_hook_main_notes_once_and_never_raises(tmp_path, monkeypatch, capsys):
    hook = _load_hook()
    graph = _hook_fixture(tmp_path)
    (graph / "sessions" / "workflows" / "review.jsonl").write_text(
        json.dumps({"workflow": "review", "run_key": "mur-9",
                    "harness_id": []}) + "\n")
    calls = []
    monkeypatch.setattr(hook, "_note", lambda rk, hid: calls.append((rk, hid)))
    payload = {"cwd": str(tmp_path), "hook_event_name": "PostToolUse",
               "tool_name": "Workflow",
               "tool_input": {"name": "agi-round-review", "args": {}},
               "tool_response": {"runId": "wf_zzz"}}
    assert hook.main(json.dumps(payload)) == 0
    assert calls == [("mur-9", "wf_zzz")]
    # malformed stdin: named, exit 0, no note
    assert hook.main("{not json") == 0
    assert calls == [("mur-9", "wf_zzz")]
    # unrelated project (no .agi from cwd): refused by name, exit 0
    other = tmp_path / "elsewhere"
    other.mkdir()
    payload["cwd"] = str(other)
    assert hook.main(json.dumps(payload)) == 0
    err = capsys.readouterr().err
    assert "workflow_note:" in err


# ---------- --root: a detached run never depends on cwd ---------------------
# hypothesis:l5-workflow-py-takes-an-explicit-root-so-a-detached-run-never-
# depends-on-cwd. `systemd-run --user ... -- python3 workflow.py run ...`
# does not inherit the caller's cwd, so the launcher sees systemd-run's 0
# while workflow.py exits 2 with "no .agi project root found from cwd". The
# fix is one --root option that works AFTER the subcommand, the position a
# director naturally appends to a brief's `run <name> --dry-run` line.

def _wfl(argv, cwd):
    import subprocess as _sp
    return _sp.run([sys.executable, str(BIN / "workflow.py"), *argv],
                   cwd=str(cwd), capture_output=True, text=True, timeout=60)


def test_root_after_subcommand_resolves_from_a_non_project_cwd(tmp_path):
    """The exact literal the brief uses: `run <name> --dry-run --root <p>`,
    --root AFTER the verb, run from a cwd with no .agi above it."""
    r = _wfl(["run", "review", "--dry-run", "--root", str(REPO)], tmp_path)
    assert r.returncode == 0, (r.stdout, r.stderr)
    assert "[dispatch] global-checks" in r.stdout, r.stdout
    assert "[summary] workflow=review" in r.stdout, r.stdout


def test_root_before_subcommand_also_resolves(tmp_path):
    """The parent-parser position keeps working; one option, two positions."""
    r = _wfl(["--root", str(REPO), "run", "review", "--dry-run"], tmp_path)
    assert r.returncode == 0, (r.stdout, r.stderr)
    assert "[dispatch] global-checks" in r.stdout, r.stdout


def test_no_root_from_non_project_cwd_exits_2_byte_identical(tmp_path):
    """Without --root the old behaviour is untouched, message included."""
    r = _wfl(["run", "review", "--dry-run"], tmp_path)
    assert r.returncode == 2
    assert r.stderr == "workflow.py: no .agi project root found from cwd\n"


def test_root_to_a_non_project_path_exits_2_naming_it(tmp_path):
    missing = tmp_path / "nope"
    r = _wfl(["run", "review", "--dry-run", "--root", str(missing)], tmp_path)
    assert r.returncode == 2
    assert str(missing) in r.stderr, r.stderr
    assert "--root" in r.stderr, r.stderr


def test_help_names_root_and_still_exits_0():
    r = _wfl(["--help"], REPO)
    assert r.returncode == 0
    assert r.stdout.strip()
    assert "--root" in r.stdout, r.stdout


# ---------- R1: the runner resolves {project_root}, never a literal --------
# hypothesis:lm-chained-research-review-cuts-director-glue-calls, residues
# from outcome:a00-cc347774-096d54. The why/brainstorm/refute/review prompts
# used to `cd /home/ubuntu/work/agi`, so a run started in a git worktree
# minted into the MAIN checkout's graph. The runner now injects the resolved
# project root as a run arg and each prompt carries `{project_root}`.

def test_research_review_prompts_name_the_runner_project_root():
    from workflow import render_stage_prompt
    manifest = workflow._load_manifest(REPO, "research-review")
    worktree = "/tmp/fake-worktree"
    args = {"project_root": worktree}
    seen = 0
    for st in manifest["stages"]:
        out = render_stage_prompt(st, args, prior={
            "verdicts": "[]", "missed": "none", "summary": "s",
            "final_recommendation": "accept", "why_node": "idea:x",
            "why_question": "q", "why_summary": "s", "evidence": "e",
            "branch": "why", "push_further": "none", "hypotheses": "[]",
            "idea": "idea:x", "refined_question": "q"})
        assert "/home/ubuntu/work/agi" not in out, (st["label"], out)
        if "{project_root}" not in st["prompt"]:
            continue
        seen += 1
        assert f"cd {worktree} &&" in out, (st["label"], out[:200])
    assert seen == 4, seen  # review, why, brainstorm, refute


def test_render_stage_prompt_project_root_falls_back_to_cwd_root(tmp_path,
                                                                 monkeypatch):
    """A direct caller that passes no project_root still gets a REAL path,
    never an empty `cd  &&` — resolved from the cwd's project root."""
    from workflow import render_stage_prompt
    monkeypatch.setattr(workflow._loc, "find_project_root",
                        lambda *a, **k: tmp_path / ".agi")
    st = {"label": "refute:x", "prompt": "cd {project_root} && true"}
    out = render_stage_prompt(st, {})
    assert out == f"cd {tmp_path} && true", out


def test_pi_run_renders_project_root_not_main_checkout(tmp_path_factory):
    """The live pi path: with a REAL run_workflow call, the rendered refute
    prompt carries the run's resolved repo root (REPO, in this suite), never
    the hardcoded main checkout."""
    import subprocess as _sp
    from unittest import mock
    from workflow import run_workflow

    calls = []
    good = json.dumps({"target": "k", "decisions": [], "ready_batch": [],
                       "kept": "none", "dropped": "none", "notes": "n"})

    def fake_run(cmd, **kw):
        if "--provider" in cmd:
            calls.append(" ".join(cmd))
        return _sp.CompletedProcess(cmd, 0, stdout=good, stderr="")

    saved = workflow._loc.shared_project_root
    workflow._loc.shared_project_root = lambda root: tmp_path_factory.mktemp("s")
    try:
        buf = io.StringIO()
        with mock.patch("subprocess.run", side_effect=fake_run):
            rc = run_workflow(REPO / ".agi", "research-review", "pi",
                              {"targets": [{"key": "k", "hypothesis": "h",
                                            "experiments": "e", "files": "f",
                                            "focus": "x", "verdict": "proved"}]},
                              False, out=buf)
        assert rc == 0, buf.getvalue()
        assert calls, "no stage rendered"
        assert any(f"cd {REPO} &&" in c for c in calls), calls[0][:400]
        assert all("/home/ubuntu/work/agi &&" not in c or f"cd {REPO} &&" in c
                   for c in calls), "main checkout literal survived"
    finally:
        workflow._loc.shared_project_root = saved


# ---------- R2: an empty handoff list is visible, not a silent ok ----------
# The acceptance clause "ready_batch of 1 to 5" is prompt-only: the schema has
# no minItems, so a refuter that drops everything leaves downstream blank
# while the summary reads ok. The runner now names it.

def test_empty_handoff_renders_a_warn_and_sets_batch_empty():
    from workflow import RunView
    buf = io.StringIO()
    v = RunView("research-review", [{"label": "refute:k"}], "pi", out=buf)
    v.stage_finished("refute:k", {"ready_batch": []})
    v.stage_empty_handoff("refute:k", "ready_batch")
    v.summary()
    text = buf.getvalue()
    assert "[warn] refute:k: handoff ready_batch is empty" in text, text
    assert "batch_empty=true" in text, text
    # the summary line is still last among summary-render lines
    tail = [l for l in text.splitlines() if l.startswith(("[stage]", "[summary]"))]
    assert tail[-1] == ("[summary] workflow=research-review stages=1 ok=1 "
                        "unstructured=0 failed=0"), tail
    assert v.empty_handoffs == [{"stage": "refute:k", "field": "ready_batch"}]


def test_nonempty_handoff_never_warns():
    from workflow import RunView
    buf = io.StringIO()
    v = RunView("research-review", [{"label": "refute:k"}], "pi", out=buf)
    v.stage_finished("refute:k", {"ready_batch": [{"id": "hypothesis:x"}]})
    v.summary()
    assert "[warn]" not in buf.getvalue()
    assert v.empty_handoffs == []


def test_pi_empty_handoff_lands_in_the_tracked_row(tmp_path_factory):
    """The mechanical detection: a stage declaring `handoff_list` and
    returning it empty makes the run level say so, through the summary AND
    the tracking row's `batch_empty` — without failing the run (rc 0)."""
    import subprocess as _sp
    from unittest import mock
    from workflow import run_workflow

    good = json.dumps({"target": "k", "decisions": [], "ready_batch": [],
                       "kept": "none", "dropped": "none", "notes": "n"})

    def fake_run(cmd, **kw):
        return _sp.CompletedProcess(cmd, 0, stdout=good, stderr="")

    tmp = tmp_path_factory.mktemp("handoff-sess")
    saved = workflow._loc.shared_project_root
    workflow._loc.shared_project_root = lambda root: tmp
    try:
        buf = io.StringIO()
        with mock.patch("subprocess.run", side_effect=fake_run):
            rc = run_workflow(REPO / ".agi", "research-review", "pi",
                              {"targets": [{"key": "k", "hypothesis": "h",
                                            "experiments": "e", "files": "f",
                                            "focus": "x", "verdict": "proved"}]},
                              False, out=buf)
        assert rc == 0, buf.getvalue()
        assert "[warn] refute:k: handoff ready_batch is empty" in buf.getvalue()
        row = json.loads((tmp / "sessions" / "workflows" /
                          "research-review.jsonl").read_text().splitlines()[-1])
        assert row["batch_empty"] is True, row
        assert row["failed"] == 0
    finally:
        workflow._loc.shared_project_root = saved
# ---------- RETURN SHAPE block: pi stage sees its schema ------------------

def _capture_pi_prompt(stage, run_args):
    import subprocess as _sp
    from unittest import mock
    captured = {}

    def fake_run(cmd, **kw):
        captured["cmd"] = cmd
        return _sp.CompletedProcess(cmd, 0,
                                    stdout='{"a": "x"}', stderr="")

    cfg = {"harnesses": {"pi": {"bin": "/bin/fakepi",
                                "provider": "openrouter"}}}
    st = dict(stage)
    label = st["label"]
    with mock.patch("subprocess.run", side_effect=fake_run):
        _run_stage_pi(cfg, st, {label: {"model": "m", "effort": "low"}},
                      run_args)
    return captured["cmd"][-1]


def test_pi_prompt_carries_every_required_key_and_result_file():
    """hypothesis:lm-pi-stage-never-sees-its-schema...: a schema-bearing pi
    stage must be handed its own schema, its required keys named, the
    last-thing-in-stdout instruction, and the rendered result_file path."""
    schema = {"type": "object",
              "properties": {"angle": {"type": "string"},
                             "chains": {"type": "array"}},
              "required": ["angle", "chains"]}
    stage = {"label": "panel:a", "role": "kid", "prompt": "do the work",
             "schema": schema, "result_file": "{scratch}/panel-{key}.json",
             "_repeat_item": {"key": "a"}}
    prompt = _capture_pi_prompt(stage, {"scratch": "/tmp/S"})
    assert "do the work" in prompt
    assert '"angle"' in prompt and '"chains"' in prompt, prompt
    assert "Required keys" in prompt and "angle" in prompt, prompt
    assert "LAST thing in your stdout" in prompt, prompt
    assert "/tmp/S/panel-a.json" in prompt, prompt


def test_pi_prompt_without_schema_is_byte_identical():
    """A stage with NO schema renders byte-identical to before: the block is
    appended only when a schema is declared."""
    stage = {"label": "plain:a", "role": "kid", "prompt": "just prose {key}",
             "_repeat_item": {"key": "a"}}
    args = {"scratch": "/tmp/S"}
    prompt = _capture_pi_prompt(stage, args)
    assert prompt == render_stage_prompt(stage, args), repr(prompt)


# ---------- round 3: _pi_harness_cfg reads the ONE shared resolver ----------
# hypothesis:harness-bin-paths-resolve-per-box. The reader used to be
# config-BEFORE-env and fell back to a /home/ubuntu literal, so a per-box
# `~/.npm-global/bin/pi` cell never expanded and every merge-up-review stage
# died at once with `pi exited rc=1`.

def test_pi_harness_cfg_env_override_wins_over_the_config_cell(monkeypatch):
    """The claim's precedence: $PI_BIN FIRST, config cell second."""
    monkeypatch.setenv("PI_BIN", "/from/PI_BIN")
    cfg = {"harnesses": {"pi": {"bin": "/from/config",
                                "provider": "openrouter"}}}
    assert workflow._pi_harness_cfg(cfg)["bin"] == "/from/PI_BIN"


def test_pi_harness_cfg_expands_a_home_token_against_the_box_home(
        tmp_path, monkeypatch):
    """No /home/<user> literal and no hand-made symlink: a `~/...` cell is the
    EXPANDED path under the CURRENT HOME when the file exists."""
    monkeypatch.delenv("PI_BIN", raising=False)
    bindir = tmp_path / ".npm-global" / "bin"
    bindir.mkdir(parents=True)
    fake = bindir / "pi"
    fake.write_text("#!/bin/sh\n", encoding="utf-8")
    fake.chmod(0o755)
    monkeypatch.setenv("HOME", str(tmp_path))
    cfg = {"harnesses": {"pi": {"bin": "~/.npm-global/bin/pi",
                                "provider": "openrouter"}}}
    assert workflow._pi_harness_cfg(cfg)["bin"] == str(fake)


def test_pi_harness_cfg_default_is_a_bare_path_name_not_a_home_literal():
    """A project with no `harnesses.pi` row gets `pi`, not a /home/<user>
    literal that only exists on core-town's box."""
    cfg = {"harnesses": {}}
    assert workflow._pi_harness_cfg(cfg)["bin"] == "pi"
