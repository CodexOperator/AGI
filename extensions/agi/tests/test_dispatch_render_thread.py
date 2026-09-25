"""hypothesis:the-spawned-agents-first-turn-is-the-render.

The spawned prompt IS the dispatch render, not a second `brief.assemble`
inside the adapter. dispatch.py computes `_render_dispatch_brief` ONCE and
threads it into every adapter as `rendered_brief`; each adapter then carries
those bytes instead of assembling its own.

RED on pre-fix bytes: no adapter's `build_command` accepted `rendered_brief`,
so every call below raised `TypeError: build_command() got an unexpected
keyword argument 'rendered_brief'` (and the spawned argv carried pi's own
`brief.assemble` spelling, not the render). `_refuse_assemble` makes a second
assemble in the adapter fail loudly rather than silently differ.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(BIN / "adapters"))

import adapters  # noqa: E402
import brief  # noqa: E402

RENDERED = "DISPATCH-RENDER-SENTINEL-9c31\n\nhead + card + extras, one render\n"


def _refuse_assemble(monkeypatch, mod):
    """A second `brief.assemble` inside an adapter is the defect, made loud."""
    def _boom(**kw):
        raise AssertionError(
            f"{mod.NAME}.build_command called brief.assemble despite being "
            f"handed rendered_brief")
    monkeypatch.setattr(mod.brief, "assemble", _boom)


@pytest.fixture
def rig(tmp_path):
    """`<repo>/.agi/sessions/iter-001/a00-test` + a context and skill file."""
    root = tmp_path / "repo" / ".agi"
    sess = root / "sessions" / "iter-001" / "a00-test"
    sess.mkdir(parents=True)
    ctx = sess / "context.md"
    ctx.write_text("# ZOOM CONTEXT MARKER\nsome map\n", encoding="utf-8")
    skill = tmp_path / "agent-prompt.md"
    skill.write_text("SKILL PROMPT MARKER\n", encoding="utf-8")
    return {"root": root, "sess": sess, "ctx": ctx, "skill": skill}


def _base(rig, **kw):
    kw.setdefault("agent_id", "a00-test")
    kw.setdefault("iter_n", 1)
    kw.setdefault("sess_dir", rig["sess"])
    kw.setdefault("cli_py", "/x/cli.py")
    kw.setdefault("dispatch_py", "/x/dispatch.py")
    kw.setdefault("skill_prompt", rig["skill"])
    return kw


def test_pi_build_command_carries_the_rendered_brief_verbatim(rig, monkeypatch):
    mod = adapters.load("pi")
    _refuse_assemble(monkeypatch, mod)
    argv = mod.build_command(
        harness={"adapter": "pi", "models": {"kid": "k"}}, tier="kid",
        context_file=str(rig["ctx"]), rendered_brief=RENDERED, **_base(rig))
    segs = [argv[i + 1] for i, a in enumerate(argv)
            if a == "--append-system-prompt"]
    assert RENDERED in segs, "pi's argv must carry the render as ONE segment"


def test_claude_code_build_command_writes_the_rendered_brief_verbatim(
        rig, monkeypatch):
    mod = adapters.load("claude_code")
    _refuse_assemble(monkeypatch, mod)
    argv = mod.build_command(
        harness={"adapter": "claude_code", "models": {"kid": "c"}}, tier="kid",
        context_file=str(rig["ctx"]), rendered_brief=RENDERED, **_base(rig))
    i = argv.index("--append-system-prompt-file")
    body = Path(argv[i + 1]).read_text(encoding="utf-8")
    assert RENDERED in body, "the written system prompt must BE the render"


def test_copilot_cli_build_command_carries_the_rendered_brief_verbatim(
        rig, monkeypatch):
    mod = adapters.load("copilot_cli")
    _refuse_assemble(monkeypatch, mod)
    argv = mod.build_command(
        harness={"adapter": "copilot_cli", "models": {"kid": "auto"}},
        tier="kid", context_file=str(rig["ctx"]), rendered_brief=RENDERED,
        **_base(rig))
    assert RENDERED in "\n".join(argv), "the -p turn must carry the render"


def test_pi_argv_carries_the_real_dispatch_render_byte_for_byte(tmp_path):
    """The load-bearing one: `_render_dispatch_brief`'s actual output (the
    same string spawn.json records) must be the argv's brief segment verbatim."""
    import dispatch

    root = tmp_path / ".agi"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    (root / "config.json").write_text(json.dumps({"harnesses": {}}),
                                      encoding="utf-8")
    rendered = dispatch._render_dispatch_brief(
        root=root, tier="kid", role="kid", harness="pi", agent_id="a00-x",
        iter_n=1, cli_py="/x/cli.py", dispatch_py="/x/dispatch.py",
        scaffold=None, source_root="/x", target="hypothesis:x",
        parallel=1, max_live=1, kid_ceiling=3, addendum=None,
        session_dir=tmp_path)
    mod = adapters.load("pi")
    argv = mod.build_command(
        harness={"adapter": "pi", "models": {"kid": "k"}}, tier="kid",
        context_file="/tmp/ctx.md", agent_id="a00-x", iter_n=1,
        sess_dir=tmp_path, cli_py="/x/cli.py", dispatch_py="/x/dispatch.py",
        target="hypothesis:x", max_live=1, rendered_brief=rendered)
    segs = [argv[i + 1] for i, a in enumerate(argv)
            if a == "--append-system-prompt"]
    assert rendered in segs and len(rendered) > 200


def test_grok_stub_accepts_rendered_brief_without_dying(rig):
    mod = adapters.load("grok_bot")
    argv = mod.build_command(
        harness={"adapter": "grok_bot", "models": {"kid": "g"}}, tier="kid",
        context_file=str(rig["ctx"]), rendered_brief=RENDERED)
    assert argv, "an accepted-and-ignored kwarg must not TypeError"


def test_render_refuses_extras_for_a_role_whose_parts_lack_it(tmp_path):
    """Conjunct 3: an extras body handed to a role with no `extras` part is
    REFUSED by name, never silently dropped. RED pre-fix: `render` returned
    the head-only bytes and discarded the dispatch body without a word."""
    (tmp_path / "config.json").write_text(
        json.dumps({"brief": {"parts": {"director": ["head"]}}}),
        encoding="utf-8")
    with pytest.raises(brief.RenderError, match="extras"):
        brief.render(role="director", extras_text="BODY", project_root=tmp_path)


def test_render_still_accepts_extras_for_a_role_that_carries_it(tmp_path):
    """The refusal is narrow: a role whose parts DO carry `extras` is
    unchanged and lands the body (the existing kid contract)."""
    (tmp_path / "config.json").write_text(
        json.dumps({"brief": {"parts": {"kid": ["extras"]}}}),
        encoding="utf-8")
    out = brief.render(role="kid", extras_text="EXTRAS-BODY",
                       project_root=tmp_path)
    assert out.startswith("EXTRAS-BODY")
    assert brief.PAID_FOR_PATH_GUARD in out
