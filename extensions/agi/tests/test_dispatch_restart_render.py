"""hypothesis:a-restarted-agent-gets-the-same-render-as-its-first-spawn.

A restart is the SAME round's first turn, so it must carry the SAME bytes the
first spawn carried -- read back from that spawn's own `spawn.json`, never
re-derived from inputs that may have moved since. Dispatch threads
`rendered_brief` into every adapter `restart()`; each adapter hands it to the
`build_command` it already accepts.

RED on pre-fix bytes: `_reap_one_impl` passed NO `rendered_brief`, so the
adapter assembled a second, possibly different, brief -- and a direct
`restart(rendered_brief=...)` raised `TypeError: restart() got an unexpected
keyword argument 'rendered_brief'`.

Conjunct 2 (`FaithRefError` -> loud `brief.assemble` fallback) and conjunct 3
(a fixture `config:brief` node renders real bytes, not the fallback) are
REGRESSION LOCKS: the director verified both on f36cc2420 before minting, so
those tests are GREEN pre-fix -- the round's new code is the restart carry.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(BIN / "adapters"))

import adapters  # noqa: E402
import brief  # noqa: E402
import dispatch  # noqa: E402
import mem_cap  # noqa: E402
import spawn_budget  # noqa: E402

RENDERED = "DISPATCH-RENDER-SENTINEL-9c31\n\nhead + card + extras, one render\n"
MARKER = "RENDER-HEAD-MARKER-777"


# ---- conjunct 1: the carry -------------------------------------------------


def _carry_rig(tmp_path: Path):
    graph = tmp_path / ".agi"
    iter_dir = graph / "sessions" / "iter-001"
    agent_id = "a00-x"
    sess = iter_dir / agent_id
    sess.mkdir(parents=True)
    (sess / "context.md").write_text("ctx", encoding="utf-8")
    return graph, iter_dir, agent_id, sess


def test_carried_restart_brief_reads_the_spawn_artifact(tmp_path):
    """The SAME bytes, read back from the ONE place the spawn wrote them."""
    _graph, iter_dir, agent_id, sess = _carry_rig(tmp_path)
    (sess / "spawn.json").write_text(json.dumps({"brief": RENDERED}),
                                     encoding="utf-8")
    assert dispatch._carried_restart_brief(iter_dir, agent_id) == RENDERED


def test_carried_restart_brief_is_none_without_render_or_artifact(tmp_path):
    """Absent artifact, absent key, and the failed-render sentinel all fall
    back to the pre-fix assemble path -- back-compat, never a garbage brief."""
    _graph, iter_dir, agent_id, sess = _carry_rig(tmp_path)
    assert dispatch._carried_restart_brief(iter_dir, agent_id) is None
    (sess / "spawn.json").write_text(json.dumps(
        {"brief": "<brief render failed>"}), encoding="utf-8")
    assert dispatch._carried_restart_brief(iter_dir, agent_id) is None


class _CapturingAdapter:
    def restart(self, **kw):
        self.kw = kw
        return 4242


def _stub_reaper(monkeypatch):
    monkeypatch.setattr(spawn_budget, "is_paused", lambda root: None)
    monkeypatch.setattr(spawn_budget, "acquire", lambda *a, **k: {"name": "lease"})
    monkeypatch.setattr(spawn_budget, "commit", lambda *a, **k: None)
    monkeypatch.setattr(spawn_budget, "release", lambda *a, **k: None)
    monkeypatch.setattr(mem_cap, "reaped_cap_death", lambda *a, **k: False)


def test_reap_restart_threads_the_spawned_render_to_the_adapter(tmp_path, monkeypatch):
    """The dispatch restart path (`_reap_one_impl`) hands the adapter the
    bytes the first spawn recorded in `spawn.json` -- RED pre-fix: no
    `rendered_brief` kwarg was ever passed."""
    graph, iter_dir, agent_id, sess = _carry_rig(tmp_path)
    (sess / "spawn.json").write_text(json.dumps({"brief": RENDERED}),
                                     encoding="utf-8")
    _stub_reaper(monkeypatch)
    fake = _CapturingAdapter()
    rec = {"tier": "kid", "context_file": str(sess / "context.md"),
           "target": "hypothesis:x"}
    out = dispatch._reap_one_impl(graph, iter_dir, fake, rec, agent_id, 999,
                                  cfg={"reaper": {"max_restarts": 1}})
    assert fake.kw.get("rendered_brief") == RENDERED
    assert out["record"]["status"] == "running"


def test_reap_restart_without_a_render_assembles_as_before(tmp_path, monkeypatch):
    """Back-compat control: an old record with no spawn render passes None, so
    the adapter's own `brief.assemble` path is byte-identical to pre-fix."""
    graph, iter_dir, agent_id, sess = _carry_rig(tmp_path)
    _stub_reaper(monkeypatch)
    fake = _CapturingAdapter()
    rec = {"tier": "kid", "context_file": str(sess / "context.md"),
           "target": "hypothesis:x"}
    dispatch._reap_one_impl(graph, iter_dir, fake, rec, agent_id, 999,
                            cfg={"reaper": {"max_restarts": 1}})
    assert fake.kw.get("rendered_brief") is None


# ---- conjunct 1 (adapter half) + conjunct 3: the bytes reach argv ----------


@pytest.fixture
def adapter_rig(tmp_path):
    sess = tmp_path / "sess"
    sess.mkdir()
    (sess / "context.md").write_text("ctx", encoding="utf-8")
    return {"sess": sess}


class _StubProc:
    pid = 7007


def _capture_popen(monkeypatch):
    captured: dict = {}

    def _fake(argv, **kw):
        captured["argv"] = argv
        return _StubProc()

    monkeypatch.setattr(subprocess, "Popen", _fake)
    return captured


@pytest.mark.parametrize("name", ["pi", "claude_code", "copilot_cli"])
def test_adapter_restart_carries_the_render_into_its_argv(
        name, adapter_rig, monkeypatch):
    """The restart argv IS the render -- `brief.assemble` inside the adapter is
    made to fail loudly, so only the threaded render can satisfy this.
    RED pre-fix: `restart()` had no `rendered_brief` parameter, TypeError."""
    mod = adapters.load(name)
    mod.child_env = lambda **kw: {}
    monkeypatch.setattr(mod.brief, "assemble", lambda **kw: (
        (_ for _ in ()).throw(AssertionError(f"{name} assembled a second brief"))))
    captured = _capture_popen(monkeypatch)
    pid = mod.restart(
        harness={"adapter": name, "models": {"kid": "k"}}, tier="kid",
        context_file=str(adapter_rig["sess"] / "context.md"), agent_id="a00-x",
        iter_n=1, sess_dir=adapter_rig["sess"], rendered_brief=RENDERED)
    argv = captured["argv"]
    if name == "claude_code":
        i = argv.index("--append-system-prompt-file")
        assert RENDERED in Path(argv[i + 1]).read_text(encoding="utf-8")
    else:
        assert RENDERED in "\n".join(argv)
    assert pid == 7007


def test_grok_restart_accepts_the_render_without_dying(adapter_rig, monkeypatch):
    """grok's stub accepts-and-ignores; the signature must still carry it, and
    the accept-and-ignore must not TypeError (the pre-fix failure)."""
    mod = adapters.load("grok_bot")
    mod.child_env = lambda **kw: {}
    captured = _capture_popen(monkeypatch)
    pid = mod.restart(
        harness={"adapter": "grok_bot", "models": {"kid": "g"}}, tier="kid",
        context_file=str(adapter_rig["sess"] / "context.md"), agent_id="a00-x",
        iter_n=1, sess_dir=adapter_rig["sess"], rendered_brief=RENDERED)
    assert captured["argv"] and pid == 7007


# ---- conjunct 2: the FaithRefError fallback (gate) -------------------------


def test_render_dispatch_brief_falls_back_loudly_on_faith_ref_error(
        monkeypatch, capsys):
    monkeypatch.setattr(brief, "assemble", lambda **kw: ["FALLBACK-BODY"])
    monkeypatch.setattr(brief, "render", lambda **kw: (
        (_ for _ in ()).throw(brief.FaithRefError("no reference region"))))
    out = dispatch._render_dispatch_brief(root=None, tier="kid", role="kid",
                                          harness="pi")
    assert out == "FALLBACK-BODY"
    err = capsys.readouterr().err
    assert "brief.render refused" in err and "falling back" in err


@pytest.mark.parametrize("exc", [brief.RenderError("nope"), KeyError("boom")])
def test_render_dispatch_brief_only_catches_the_brief_errors(exc, monkeypatch):
    """The catch stays NARROW: a RenderError falls back, a KeyError (or any
    non-brief exception) still propagates -- a swallowed KeyError is a bug
    hidden behind a silent fallback."""
    monkeypatch.setattr(brief, "assemble", lambda **kw: ["BODY"])
    monkeypatch.setattr(brief, "render", lambda **kw: (
        (_ for _ in ()).throw(exc)))
    if isinstance(exc, KeyError):
        with pytest.raises(KeyError):
            dispatch._render_dispatch_brief(root=None, tier="kid", role="kid",
                                            harness="pi")
    else:
        assert dispatch._render_dispatch_brief(
            root=None, tier="kid", role="kid", harness="pi") == "BODY"


# ---- conjunct 3: the config:brief node's REAL render, not the fallback -----


def _write_config_brief_fixture(graph: Path) -> None:
    """The fixture the old test lacked: a committable `config:brief` node
    whose `kid` parts are head+extras, a unified head carrying a MARKER the
    legacy `brief.assemble` path never emits, and the faith reference the head
    part demands -- so a real `brief.render` is distinguishable from the
    fallback."""
    for sub in ("config", "doc", "moral"):
        (graph / "nodes" / sub).mkdir(parents=True, exist_ok=True)
    (graph / "config.json").write_text(json.dumps({"harnesses": {}}),
                                       encoding="utf-8")
    (graph / "nodes" / "config" / "brief.md").write_text(
        "---\nid: config:brief\ntype: config\nbrief:\n  parts:\n    kid:\n"
        "      - head\n      - extras\n---\n", encoding="utf-8")
    (graph / "nodes" / "doc" / "unified-head.md").write_text(
        "---\nid: doc:unified-head\ntype: doc\n---\n"
        f"<!-- HEAD:BEGIN -->\n{MARKER}\n<!-- HEAD:END -->\n",
        encoding="utf-8")
    (graph / "nodes" / "moral" / "faith.md").write_text(
        "---\nid: moral:faith\ntype: moral\n---\n## REFERENCE\n\n"
        "### 4.1 prayers\n\nPRAYER-TEXT-ZZZ\n", encoding="utf-8")


def _render_kw(tmp_path: Path) -> dict:
    return dict(tier="kid", role="kid", harness="pi", agent_id="a00-x",
                iter_n=1, cli_py="/x/cli.py", dispatch_py="/x/dispatch.py",
                scaffold=None, source_root="/x", target="hypothesis:x",
                parallel=1, max_live=1, kid_ceiling=3, addendum=None,
                session_dir=tmp_path)


def test_config_brief_render_is_what_build_command_receives(tmp_path):
    """The bytes a build_command gets ARE a real `brief.render` (head+extras
    from the fixture node), never the `brief.assemble` fallback the old
    fixture silently fell to (its tmp `.agi` had no `config:brief` node)."""
    graph = tmp_path / ".agi"
    _write_config_brief_fixture(graph)
    rendered = dispatch._render_dispatch_brief(root=graph, **_render_kw(tmp_path))
    assert MARKER in rendered, "the fixture config:brief render must carry the head"

    bare = tmp_path / "bare" / ".agi"
    (bare / "nodes" / ".geometry").mkdir(parents=True)
    (bare / "config.json").write_text(json.dumps({"harnesses": {}}),
                                      encoding="utf-8")
    fallback = dispatch._render_dispatch_brief(root=bare, **_render_kw(tmp_path))
    assert MARKER not in fallback and rendered != fallback

    mod = adapters.load("pi")
    argv = mod.build_command(
        harness={"adapter": "pi", "models": {"kid": "k"}}, tier="kid",
        context_file="/tmp/ctx.md", agent_id="a00-x", iter_n=1,
        sess_dir=tmp_path, cli_py="/x/cli.py", dispatch_py="/x/dispatch.py",
        target="hypothesis:x", max_live=1, rendered_brief=rendered)
    segs = [argv[i + 1] for i, a in enumerate(argv)
            if a == "--append-system-prompt"]
    assert rendered in segs and any(MARKER in s for s in segs)