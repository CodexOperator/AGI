"""The DISPATCH shapes of the two non-pi harnesses are template DATA.

hypothesis:harness-arg-builders-are-templates-only. `claude_code_adapter.
build_command` and `copilot_cli_adapter.build_command` used to build their
argv inline; both now render `[shapes.dispatch]` from their harness template.
The frozen literals below are the OLD inline shapes, so a regression is a
diff, not a shrug. The seat (top-level) shape is guarded separately in
`test_harness_template.py`.
"""
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

import adapters  # noqa: E402
from agi.bin import harness_template  # noqa: E402

cc = adapters.load("claude_code")
cp = adapters.load("copilot_cli")

SCAFFOLD = {"path": "/x/nodes/hypothesis/h.md", "node_type": "hypothesis",
            "node_id": "hypothesis:h", "parent": "goal:g4.6"}


@pytest.fixture
def rig(tmp_path):
    repo = tmp_path / "repo"
    root = repo / ".agi"
    sess = root / "sessions" / "iter-001" / "a00-test"
    sess.mkdir(parents=True)
    ctx = sess / "context.md"
    ctx.write_text("# ZOOM CONTEXT MARKER\nsome map\n")
    skill = tmp_path / "agent-prompt.md"
    skill.write_text("SKILL PROMPT MARKER\n")
    return {"repo": repo, "root": root, "sess": sess, "ctx": ctx, "skill": skill}


def build(mod, rig, harness, tier="kid", **kw):
    kw.setdefault("scaffold", SCAFFOLD)
    kw.setdefault("skill_prompt", rig["skill"])
    kw.setdefault("cli_py", "/x/cli.py")
    kw.setdefault("dispatch_py", "/x/dispatch.py")
    kw.setdefault("target", "goal:g4.6")
    return mod.build_command(
        harness=harness, tier=tier, context_file=str(rig["ctx"]),
        agent_id="a00-test", iter_n=1, sess_dir=rig["sess"], **kw)


# ------------------------------------------------------------- the shapes


def test_claude_dispatch_shape_is_the_old_inline_argv(rig):
    """The frozen pre-template shape, built by hand, with the prompt file and
    the `--` fence exactly where the inline builder put them."""
    harness = {"adapter": "claude_code", "models": {"kid": "claude-sonnet-5"},
               "max_budget_usd": 5, "extra_args": ["--foo", "bar"]}
    args = build(cc, rig, harness)
    sess = rig["sess"]
    assert args[:4] == ["claude", "-p", "--model", "claude-sonnet-5"]
    assert args[4:9] == ["--output-format", "stream-json", "--verbose",
                         "--strict-mcp-config", "--max-budget-usd"]
    assert args[9] == "5"
    assert args[10:12] == [
        "--append-system-prompt-file", str(sess / "system-prompt.md")]
    assert args[12:14] == ["--foo", "bar"]
    assert args[14:16] == ["--add-dir", str(rig["repo"])]
    assert "--mcp-config" not in args            # absent -> no flag at all
    t = args.index("--tools")
    assert args[t:t + 7] == ["--tools", "Bash", "Read", "Edit", "Write",
                             "Glob", "Grep"]
    assert args[-2] == "--"
    assert args[-1].startswith("Begin iteration 1 as agent a00-test")


def test_claude_dispatch_shape_omits_verbose_for_non_stream_formats(rig):
    harness = {"adapter": "claude_code", "models": {"kid": "m"},
               "output_format": "json"}
    args = build(cc, rig, harness)
    assert "--verbose" not in args
    assert args[args.index("--output-format") + 1] == "json"


def test_claude_mcp_list_is_flattened_after_its_flag(rig):
    harness = {"adapter": "claude_code", "models": {"kid": "m"},
               "mcp_config": ["a.json", "b.json"]}
    args = build(cc, rig, harness)
    i = args.index("--mcp-config")
    assert args[i + 1:i + 3] == ["a.json", "b.json"]
    assert args[i + 3].startswith("--")


def test_claude_empty_tool_lists_emit_no_flag_at_all(rig):
    """An empty variadic list must skip the flag; `--tools` with no value
    would swallow the next token (this was a live bug in the first template
    draft)."""
    harness = {"adapter": "claude_code", "models": {"kid": "m"}, "tools": []}
    args = build(cc, rig, harness)
    assert "--tools" not in args
    assert "--allowedTools" not in args


def _fake_bin(tmp_path, name):
    """A REAL `bin` cell. A path-shaped cell that does not exist refuses by
    name (`hypothesis:harness-bin-absolute-token-free-bins-refused-by-name`),
    so a literal like `/x/copilot` can no longer stand in for one."""
    p = tmp_path / name
    p.write_text("#!/bin/sh\n", encoding="utf-8")
    p.chmod(0o755)
    return str(p)


def test_copilot_dispatch_shape_is_the_old_inline_argv(rig, tmp_path):
    copilot_bin = _fake_bin(tmp_path, "copilot")
    harness = {"adapter": "copilot_cli", "bin": copilot_bin,
               "models": {"kid": "auto"}, "effort": "high",
               "extra_args": ["--foo"]}
    args = build(cp, rig, harness)
    assert args[:5] == [copilot_bin, "--model", "auto", "--effort", "high"]
    assert args[5:8] == ["--allow-all", "--remote", "--foo"]
    assert args[-2] == "-p"
    assert "ZOOM CONTEXT MARKER" in args[-1]
    assert "Begin iteration 1 as agent a00-test" in args[-1]
    # and NOT the seat's interactive spelling
    assert "-i" not in args


def test_copilot_dispatch_omits_model_and_effort_when_absent(rig, tmp_path):
    copilot_bin = _fake_bin(tmp_path, "copilot")
    args = build(cp, rig, {"adapter": "copilot_cli", "bin": copilot_bin})
    assert args[:4] == [copilot_bin, "--allow-all", "--remote", "-p"]


# --------------------------------------------------- the template is data


def test_unknown_shape_is_a_named_error():
    with pytest.raises(harness_template.HarnessTemplateError) as exc:
        harness_template.render("claude-code", shape="nope", closing="C")
    assert "nope" in str(exc.value)
    assert "dispatch" in str(exc.value)


def test_both_shapes_of_a_harness_live_in_one_template_file():
    for hid in ("claude-code", "copilot-cli"):
        data = harness_template.load(hid)
        assert data.get("argv"), hid          # the seat shape, unchanged
        assert data["shapes"]["dispatch"]["argv"]  # the dispatch shape


def test_a_shape_argv_is_still_closed_vocabulary(tmp_path, monkeypatch):
    (tmp_path / "evil2.toml").write_text(
        'id = "evil2"\nbin = "e"\n[[argv]]\nconst = "--x"\n'
        '[shapes.dispatch]\nargv = [{script = "import os"}]\n')
    monkeypatch.setattr(harness_template, "template_dir", lambda: tmp_path)
    with pytest.raises(harness_template.HarnessTemplateError) as exc:
        harness_template.load("evil2")
    assert "shapes.dispatch" in str(exc.value)


def test_variadic_flag_element_needs_values_and_flag_stays_in_data():
    """`{flag, spread}` emits both only when the list is non-empty, so a
    template never emits a value-less flag."""
    assert harness_template._emit({"flag": "--t", "spread": "l"},
                                  {"l": []}) == []
    assert harness_template._emit({"flag": "--t", "spread": "l"},
                                  {"l": ["a"]}) == ["--t", "a"]


# ------------------------------------------------- the production path


@pytest.mark.parametrize("mod,hid", [(cc, "claude-code"), (cp, "copilot-cli")])
def test_adapter_production_path_reaches_render_with_the_dispatch_shape(
        mod, hid, rig, monkeypatch):
    seen = {}

    def sentinel(harness_id, **kw):
        seen["id"] = harness_id
        seen["shape"] = kw.get("shape")
        return ["sentinel"]

    monkeypatch.setattr(mod.harness_template, "render", sentinel)
    harness = {"adapter": mod.NAME.replace("-", "_"),
               "models": {"kid": "m"}}
    got = build(mod, rig, harness)
    assert got == ["sentinel"]
    assert seen == {"id": hid, "shape": "dispatch"}


def test_no_flag_construction_remains_in_either_adapter_body():
    """The literals that were the inline argv are gone from the builders.
    Docstrings and comments may still NAME a flag (the module records the
    shape it renders); live code may not contain one."""
    import re
    for mod in (cc, cp):
        src = Path(mod.__file__).read_text(encoding="utf-8")
        body = src.split("def build_command(", 1)[1].split("\ndef ", 1)[0]
        body = re.sub(r'""".*?"""', "", body, flags=re.S)
        body = "\n".join(l for l in body.splitlines()
                         if not l.lstrip().startswith(("#", "print(")))
        for flag in ("--output-format", "--strict-mcp-config", "--add-dir",
                     "--tools", "--allowedTools", "--disallowedTools",
                     "--mcp-config", "--allow-all", "--remote", "-p"):
            assert flag not in body, f"{mod.NAME}: {flag} still built in code"