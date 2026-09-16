"""hypothesis:l4-needs-credential-is-provider-gated, round 3.

The credential-none rule is ONE function (`adapters.drop_unneeded_credential`)
that every adapter's `child_env` calls, so every spawn path -- the live main
dispatch, the dry-run mirror, and adapter `restart` -- applies it and none can
forget it. Round 2 had two ad-hoc pops in `dispatch.py` and the RESTART seam
inherited `OPENROUTER_API_KEY` anyway.

What these tests guard, each with `subprocess.Popen` stubbed so no real process
spawns and no `_reap_*` is involved:

  1. the predicate (`needs_credential`) is an allowlist read from the harness
     row, default mint;
  2. each adapter's `child_env` drops the inherited runtime key for a
     `credential: "none"` row and keeps it for every unmarked row -- deleting
     the shared call from an adapter turns these red (the R2 regression guard,
     relocated from the two dispatch pops to the one mechanism);
  3. a live `dispatch.main()` spawn on a `credential: "none"` row hands no
     runtime key to the child AND records `harness_spec` on the agent record;
  4. the RESTART path reads that recorded row and hands no runtime key to the
     restarted child, while an unmarked row keeps it;
  5. the credential banner obeys the same predicate: absent for a
     `credential: "none"` row, present for the default row -- asserted against
     the REAL spaced string `minting per spawn` (round 2's probe looked for
     `minting-per-spawn`, hyphens, and could pass vacuously).
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import adapters  # noqa: E402
import provisioning  # noqa: E402


def _load_dispatch():
    spec = importlib.util.spec_from_file_location(
        "agi_dispatch_crednone", BIN / "dispatch.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


dispatch = _load_dispatch()

PI_LOCAL_ROW = {"adapter": "pi", "provider": "local-town",
                "credential": "none", "models": {"kid": "Qwen3.5-9B-Q4_K_M"}}
PI_ROW = {"adapter": "pi", "provider": "fake",
          "models": {"kid": "deepseek-v4"},
          "allowed_extra": ["deepseek-v4"]}


# ------------------------------------------------------------------ fixtures


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    """A scratch agi project with a `pi-local` row (credential: none) and a
    plain `pi` row, provisioning deliberately absent (secrets geometry pinned
    to a nonexistent file) so the live path never mints or hits the network."""
    graph = tmp_path / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "nodes" / "goal").mkdir(parents=True)
    (graph / "config.json").write_text(json.dumps({
        "harnesses": {"pi-local": dict(PI_LOCAL_ROW), "pi": dict(PI_ROW)},
        "spawn": {"harness": "pi-local", "parallel": 1, "max_live": 25},
        "agent_dispatch": {"inline_reaper": False},
    }))
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ncurrent_season: 2\nroles:\n  - {tier: 0, role: kid, "
        "harness: pi-local, model: Qwen3.5-9B-Q4_K_M}\n---\nbody")
    (graph / "nodes" / ".geometry" / "secrets.md").write_text(
        "---\nenv_file: /tmp/definitely-not-a-real-secrets-file-zzz\n---\n")
    (graph / "nodes" / "goal" / "g15.md").write_text(
        "---\nid: goal:g15\ntype: goal\n---\nbody\n")
    (graph / "nodes" / "hypothesis" / "x.md").write_text(
        "---\nid: hypothesis:x\ntype: hypothesis\nparents:\n  - goal:g15\n"
        "---\nbody\n")
    for k in ("AGI_TREE_PROJECT_ROOT", "AGI_PROJECT_ROOT", "AGI_AGENT_ID",
              "AGI_ACTOR"):
        os.environ.pop(k, None)
    return tmp_path


def _stub_popen(monkeypatch):
    """Patch `subprocess.Popen` only for the SPAWN call (the one with
    `start_new_session=True`), capturing argv and env; nothing is spawned."""
    captured = {}

    class _StubProc:
        pid = 7777
        def poll(self): return None
        def wait(self, timeout=None): return 0
        def __enter__(self): return self
        def __exit__(self, *a): return False

    real_popen = subprocess.Popen

    def _patched(argv, **kwargs):
        if kwargs.get("start_new_session"):
            captured["argv"] = argv
            captured["env"] = dict(kwargs.get("env") or {})
            return _StubProc()
        return real_popen(argv, **kwargs)

    monkeypatch.setattr(subprocess, "Popen", _patched)
    return captured


def _argv(tmp_path: Path, harness: str):
    return [str(BIN / "dispatch.py"), str(tmp_path), "1",
            "--level", "small", "--harness", harness, "--tier", "kid",
            "--target", "hypothesis:x"]


def _agent_record(project: Path) -> dict:
    for p in (project / ".agi" / "sessions").rglob("agent.json"):
        return json.loads(p.read_text())
    raise AssertionError("no agent.json written under .agi/sessions/")


# ------------------------------------------------------- 1. the predicate


def test_needs_credential_is_an_allowlist_defaulting_to_mint():
    pi = adapters.load("pi")
    assert pi.needs_credential(PI_LOCAL_ROW) is False
    for row in (PI_ROW, {"adapter": "pi", "provider": "fake"},
                {"adapter": "pi", "credential": "openrouter"},
                {"adapter": "pi"}):
        assert pi.needs_credential(row) is True, row


# ------------------------------------- 2. the shared child_env rule (R2 guard)


@pytest.mark.parametrize("module_name,harness", [
    ("pi", PI_LOCAL_ROW),
    ("claude_code", {"adapter": "claude_code"}),
    ("copilot_cli", {"adapter": "copilot_cli"}),
])
def test_child_env_drops_inherited_runtime_key_for_credential_none(
        module_name, harness):
    """Every adapter's `child_env` applies the ONE shared rule."""
    mod = adapters.load(module_name)
    base = {"OPENROUTER_API_KEY": "sk-or-v1-inherited", "KEEP": "1"}
    env = mod.child_env(harness=harness, base=base, tier="kid")
    assert provisioning.RUNTIME_KEY_VAR not in env, (
        f"{module_name}.child_env must drop the inherited runtime key for a "
        f"credential-none row; env={sorted(env)}")
    assert env.get("KEEP") == "1", "the rest of the env must be untouched"


def test_child_env_keeps_inherited_runtime_key_for_unmarked_rows():
    """The default-mint direction is unchanged: an unmarked pi row keeps the
    inherited key (the no-provisioning fallback depends on it)."""
    pi = adapters.load("pi")
    base = {"OPENROUTER_API_KEY": "sk-or-v1-inherited"}
    env = pi.child_env(harness=PI_ROW, base=base, tier="kid")
    assert env.get(provisioning.RUNTIME_KEY_VAR) == "sk-or-v1-inherited"


def test_drop_unneeded_credential_is_the_shared_mechanism():
    """The rule is one exported function, not three copies: dispatch.py no
    longer pops the key itself."""
    src = (BIN / "dispatch.py").read_text()
    assert "drop_unneeded_credential" not in src.replace(
        "adapters.drop_unneeded_credential", ""), (
        "dispatch.py must not re-implement the pop; it goes through child_env")
    assert ".pop(provisioning.RUNTIME_KEY_VAR, None)" not in src, (
        "the two round-2 ad-hoc pops must be gone")
    assert callable(adapters.drop_unneeded_credential)


# ----------------------------------------------------- 3/4. the restart seam


def _capture_restart_env(monkeypatch, harness: dict, sess_dir: Path):
    pi = adapters.load("pi")
    captured = {}

    class _StubProc:
        pid = 4242
        def poll(self): return None
        def wait(self, timeout=None): return 0

    def _patched(argv, **kwargs):
        captured["env"] = dict(kwargs.get("env") or {})
        return _StubProc()

    monkeypatch.setattr(subprocess, "Popen", _patched)
    monkeypatch.setenv(provisioning.RUNTIME_KEY_VAR, "sk-or-v1-inherited")
    rec = {"id": "a00-restart", "tier": "kid", "iter": 1, "pid": 0,
           "status": "failed"}
    new_pid = pi.restart(
        harness=harness, tier="kid", context_file="/tmp/does-not-matter.md",
        agent_id="a00-restart", iter_n=1, sess_dir=sess_dir,
        agent_record=rec)
    assert new_pid == 4242, "restart must have used the stubbed Popen"
    return captured["env"]


def test_restart_env_honours_a_credential_none_row(monkeypatch, tmp_path):
    """Round 2's central residue (R1): the RESTART path built `child_env` with
    a raw `os.environ` base and no pop, so a restarted pi-local kid inherited
    the key. With the rule inside `child_env`, the recorded row now decides."""
    sess = tmp_path / "a00-restart"
    sess.mkdir()
    env = _capture_restart_env(monkeypatch, dict(PI_LOCAL_ROW), sess)
    assert provisioning.RUNTIME_KEY_VAR not in env, (
        "a restarted credential-none kid must not inherit OPENROUTER_API_KEY")


def test_restart_env_keeps_the_key_for_an_unmarked_row(monkeypatch, tmp_path):
    sess = tmp_path / "a00-restart"
    sess.mkdir()
    env = _capture_restart_env(monkeypatch, dict(PI_ROW), sess)
    assert env.get(provisioning.RUNTIME_KEY_VAR) == "sk-or-v1-inherited", (
        "the default row must keep the inherited key on restart too")


# ------------------------------------------- 3. the live spawn + agent record


def test_live_spawn_records_harness_spec_and_drops_the_key(
        project, monkeypatch, capsys):
    """A live spawn on a credential-none row: the child env has no runtime key
    (the pop now lives in child_env) AND the agent record carries the config
    row, which is what makes the restart path above reachable at all."""
    captured = _stub_popen(monkeypatch)
    monkeypatch.setenv(provisioning.RUNTIME_KEY_VAR, "sk-or-v1-inherited")
    monkeypatch.setattr(sys, "argv", _argv(project, "pi-local"))

    code = dispatch.main()
    assert code == 0, f"live spawn must succeed, got rc {code}\n{capsys.readouterr().out}"

    env = captured.get("env") or {}
    assert provisioning.RUNTIME_KEY_VAR not in env, (
        "the live spawn env must not carry the inherited runtime key")
    assert env.get("AGI_TIER") == "kid"

    rec = _agent_record(project)
    spec = rec.get("harness_spec") or {}
    assert spec.get("credential") == "none", (
        f"the agent record must carry harness_spec so restart can decide; "
        f"got {spec!r}")


def test_live_spawn_keeps_the_key_for_an_unmarked_row(
        project, monkeypatch, capsys):
    """Guard the other direction: the default row still receives the inherited
    runtime key on the live path."""
    captured = _stub_popen(monkeypatch)
    monkeypatch.setenv(provisioning.RUNTIME_KEY_VAR, "sk-or-v1-inherited")
    monkeypatch.setattr(sys, "argv", _argv(project, "pi"))

    code = dispatch.main()
    assert code == 0, f"live spawn must succeed, got rc {code}\n{capsys.readouterr().out}"
    assert (captured.get("env") or {}).get(provisioning.RUNTIME_KEY_VAR) == (
        "sk-or-v1-inherited")


# ------------------------------------------------------------ 5. the banner


class _MintedKey:
    secret = "sk-or-v1-test-not-a-real-key"
    key_hash = "hash-test"
    name = "test"
    limit_usd = 0.5
    expires_at = "2099-01-01T00:00:00Z"


def _force_provisioning(monkeypatch):
    monkeypatch.setattr(dispatch.provisioning, "available",
                        lambda root=None: True)
    monkeypatch.setattr(dispatch.provisioning, "mint",
                        lambda **kw: _MintedKey())


def test_banner_is_absent_for_a_credential_none_row(project, monkeypatch,
                                                    capsys):
    """The REAL string is spaced: `minting per spawn`. Round 2's probe looked
    for `minting-per-spawn`, which never matches -- so this asserts the exact
    spaced form and the absence for pi-local."""
    _force_provisioning(monkeypatch)
    _stub_popen(monkeypatch)
    monkeypatch.setattr(sys, "argv", _argv(project, "pi-local"))

    code = dispatch.main()
    out = capsys.readouterr().out
    assert code == 0, out
    assert "credentials: minting per spawn" not in out, (
        "a credential-none row must not announce a mint it will not do")


def test_banner_is_present_for_the_default_row(project, monkeypatch, capsys):
    _force_provisioning(monkeypatch)
    captured = _stub_popen(monkeypatch)
    monkeypatch.setattr(sys, "argv", _argv(project, "pi"))

    code = dispatch.main()
    out = capsys.readouterr().out
    assert code == 0, out
    assert "credentials: minting per spawn" in out, (
        "the default row still mints and must announce it")
    # the minted secret is what reaches the child on the default path
    assert (captured.get("env") or {}).get(
        provisioning.RUNTIME_KEY_VAR) == _MintedKey.secret
