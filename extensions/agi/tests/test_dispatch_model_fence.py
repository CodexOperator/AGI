"""The dispatch half of the no-model fence
(hypothesis:a-no-model-round-refuses-a-model-load-in-every-process-it-spawns).

Deliverable under test: `--no-model` (or the config default `spawn.no_model`)
puts BOTH fence cells into the env a round is ACTUALLY spawned with -- read off
the `Popen` call itself, not off a source string -- and a process launched with
that env refuses the TMM.228 loader call. Plus the residual-C fix: a fence
that cannot resolve its one table is LOUD (stderr marker + an env var a caller
can assert on), never silently absent.

Stand-ins only: no real torch/transformers, no weights dir, no network.
"""
from __future__ import annotations

import json
import os
import pathlib
import subprocess
import sys
import textwrap

import pytest

BIN = pathlib.Path(__file__).resolve().parents[1] / "bin"
PLUGIN_ROOT = BIN.parent
REPO = PLUGIN_ROOT.parents[1]
FENCE_DIR = PLUGIN_ROOT / "fence"
TABLE = PLUGIN_ROOT / "model_fence.py"

_STANDIN = {
    "transformers/__init__.py": "",
    "transformers/models/__init__.py": "",
    "transformers/models/llama.py": textwrap.dedent(
        """
        CALLS = []


        class AutoModelForCausalLM:
            @classmethod
            def from_pretrained(cls, name, **kw):
                CALLS.append(name)
                return "RECORDED"
        """),
}

_PROBE = textwrap.dedent(
    """
    import os
    import transformers.models.llama as L
    try:
        L.AutoModelForCausalLM.from_pretrained("Qwen/Qwen3-8B")
        print("NOT-REFUSED")
    except BaseException as exc:
        print("REFUSED-%s-CALLS=%d" % (type(exc).__name__, len(L.CALLS)))
    print("STATUS=%s" % os.environ.get("AGI_MODEL_FENCE_STATUS"))
    """)


@pytest.fixture()
def standin_tree(tmp_path):
    for rel, text in _STANDIN.items():
        p = tmp_path / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)
    return tmp_path


@pytest.fixture(autouse=True)
def _restore_own_env():
    """`apply_model_fence_env` writes the cells into the DISPATCHER's own env
    (that is what makes them inheritable), so this test process must give them
    back or every later subprocess in the suite runs fenced."""
    keys = ("PYTHONPATH", "AGI_MODEL_FENCE_SRC", "AGI_MODEL_FENCE_MAX_BYTES")
    saved = {k: os.environ.get(k) for k in keys}
    yield
    for k, v in saved.items():
        if v is None:
            os.environ.pop(k, None)
        else:
            os.environ[k] = v


def _project(tmp_path, spawn_extra=None) -> pathlib.Path:
    graph = tmp_path / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "nodes" / "hypothesis").mkdir(parents=True)
    (graph / "nodes" / "goal").mkdir(parents=True)
    spawn = {"harness": "pi", "parallel": 1, "max_live": 25}
    spawn.update(spawn_extra or {})
    (graph / "config.json").write_text(json.dumps({
        "harnesses": {"pi": {"adapter": "pi", "provider": "fake",
                             "models": {"parent": "glm", "kid": "glm"}}},
        "spawn": spawn,
        "agent_dispatch": {"inline_reaper": False},
    }))
    (graph / "nodes" / ".geometry" / "ladder.md").write_text(
        "---\ncurrent_season: 2\nroles:\n  - {tier: 1, role: parent, "
        "harness: pi, model: glm}\n  - {tier: 0, role: kid, harness: pi, "
        "model: glm}\n---\nbody")
    # pin secrets to a nonexistent file -> provisioning.available is False, so
    # the live path never mints a credential or touches the network
    (graph / "nodes" / ".geometry" / "secrets.md").write_text(
        "---\nenv_file: /tmp/definitely-not-a-real-secrets-file-zzz\n---\n")
    (graph / "nodes" / "goal" / "g15.md").write_text(
        "---\nid: goal:g15\ntype: goal\n---\nbody\n")
    (graph / "nodes" / "hypothesis" / "x.md").write_text(
        "---\nid: hypothesis:x\ntype: hypothesis\nparents:\n  - goal:g15\n"
        "---\nbody\n")
    return tmp_path


def _live_spawn_env(tmp_path, monkeypatch, *extra_argv) -> dict:
    """Run the REAL dispatch live path with `Popen` captured and return the env
    the child was handed. Nothing is actually launched."""
    monkeypatch.delenv("AGI_TREE_PROJECT_ROOT", raising=False)
    monkeypatch.delenv("AGI_PROJECT_ROOT", raising=False)
    import dispatch

    captured: dict = {}
    real_popen = subprocess.Popen

    class _StubProc:
        pid = 7777
        args = []
        returncode = 0
        stdin = None
        stdout = ""
        stderr = ""
        def poll(self): return None
        def wait(self, timeout=None): return 0
        def kill(self): return None
        def terminate(self): return None
        def communicate(self, input=None, timeout=None): return ("", "")
        def __enter__(self): return self
        def __exit__(self, *a): return False

    def _patched(popenargs, **kwargs):
        env = kwargs.get("env") or {}
        if env.get("GIT_CONFIG_VALUE_0"):
            captured["env"] = env
            return _StubProc()
        return real_popen(popenargs, **kwargs)

    monkeypatch.setattr(subprocess, "Popen", _patched)
    monkeypatch.setattr(dispatch, "_GRACE_SLEEP", lambda _s: None)
    monkeypatch.setattr(sys, "argv",
                        [str(BIN / "dispatch.py"), str(tmp_path), "1",
                         "--level", "small", "--harness", "pi",
                         "--tier", "parent", "--target", "hypothesis:x",
                         *extra_argv])
    code = dispatch.main()
    assert code == 0, f"live dispatch failed before the spawn: exit {code}"
    assert "env" in captured, "the spawn env was never captured"
    # the Popen stub is global to `subprocess`; the caller runs its OWN child
    # processes with the captured env, so hand the real Popen back first.
    monkeypatch.undo()
    return captured["env"]


def test_live_spawn_env_carries_both_fence_cells(tmp_path, monkeypatch):
    """The flag REACHES the env the real spawn hands the child, and it carries
    BOTH cells -- the parent's PASS-F probe showed a one-cell round is silently
    unfenced."""
    env = _live_spawn_env(_project(tmp_path), monkeypatch, "--no-model")
    assert env["AGI_MODEL_FENCE_SRC"] == str(TABLE), env.get("AGI_MODEL_FENCE_SRC")
    assert pathlib.Path(env["AGI_MODEL_FENCE_SRC"]).is_file()
    entries = env["PYTHONPATH"].split(os.pathsep)
    assert entries[-1] == str(FENCE_DIR), entries
    assert (FENCE_DIR / "sitecustomize.py").is_file()
    # the cap is written ONLY when an override is passed
    assert "AGI_MODEL_FENCE_MAX_BYTES" not in env


def test_a_process_with_the_captured_env_refuses_the_standin_loader(
        tmp_path, monkeypatch, standin_tree):
    """Falsifier 1 end to end: the env a real dispatch BUILT refuses the
    TMM.228 call in a fresh interpreter, and the fence reports itself
    installed. No pytest, no conftest, no real transformers."""
    env = dict(_live_spawn_env(_project(tmp_path), monkeypatch, "--no-model"))
    env["PYTHONPATH"] = os.pathsep.join(
        [str(standin_tree)] + env["PYTHONPATH"].split(os.pathsep))
    r = subprocess.run([sys.executable, "-c", _PROBE], capture_output=True,
                       text=True, timeout=120, env=env)
    assert "REFUSED-ModelLoadRefused-CALLS=0" in r.stdout, (r.stdout, r.stderr)
    assert "STATUS=installed" in r.stdout, r.stdout


def test_a_cap_override_is_the_only_thing_that_writes_the_cap(
        tmp_path, monkeypatch):
    env = _live_spawn_env(_project(tmp_path), monkeypatch, "--no-model",
                          "--model-fence-max-bytes", "1234")
    assert env["AGI_MODEL_FENCE_MAX_BYTES"] == "1234"


def test_without_the_flag_the_round_is_unfenced(tmp_path, monkeypatch):
    """The control, so the fence is not vacuous: no flag, no cell."""
    env = _live_spawn_env(_project(tmp_path), monkeypatch)
    assert "AGI_MODEL_FENCE_SRC" not in env
    assert str(FENCE_DIR) not in env.get("PYTHONPATH", "")


def test_the_config_default_fences_without_the_flag(tmp_path, monkeypatch):
    """`spawn.no_model` is the second opt-in, for a post that fences every
    round it cuts."""
    env = _live_spawn_env(_project(tmp_path, {"no_model": True}), monkeypatch)
    assert env["AGI_MODEL_FENCE_SRC"] == str(TABLE)
    assert env["PYTHONPATH"].split(os.pathsep)[-1] == str(FENCE_DIR)


def test_the_fence_cells_are_inheritable_from_the_dispatcher_itself(
        tmp_path, monkeypatch):
    """Never per-child argv: the dispatcher's OWN env carries the cells, so a
    nested dispatch (which reads `scrubbed_env()`) is fenced too."""
    _live_spawn_env(_project(tmp_path), monkeypatch, "--no-model")
    assert os.environ["AGI_MODEL_FENCE_SRC"] == str(TABLE)
    assert os.environ["PYTHONPATH"].split(os.pathsep)[-1] == str(FENCE_DIR)


def test_the_dry_run_shows_both_cells(tmp_path, monkeypatch):
    """A check that costs a spawn is a check nobody runs: the dry-run mirror
    reports the fence it WOULD export."""
    graph = _project(tmp_path)
    r = subprocess.run(
        [sys.executable, str(BIN / "dispatch.py"), str(graph), "1",
         "--harness", "pi", "--tier", "parent", "--target", "hypothesis:x",
         "--no-model", "--dry-run"],
        capture_output=True, text=True, env={**os.environ}, timeout=180)
    assert r.returncode == 0, r.stderr
    assert f"dir={FENCE_DIR}" in r.stdout, r.stdout
    assert f"src={TABLE}" in r.stdout, r.stdout


def test_fail_open_is_loud_and_assertable(standin_tree):
    """Residual C, fixed: the unresolvable-table case still runs python, but it
    says so on stderr AND in AGI_MODEL_FENCE_STATUS -- a caller can assert on
    it. A silent no-fence is prose again."""
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"),
           "HOME": os.environ.get("HOME", "/tmp"),
           "PYTHONPATH": os.pathsep.join([str(FENCE_DIR), str(standin_tree)]),
           "AGI_MODEL_FENCE_SRC": "/nonexistent/model_fence.py"}
    r = subprocess.run([sys.executable, "-c", _PROBE], capture_output=True,
                       text=True, timeout=120, env=env)
    assert "NOT-REFUSED" in r.stdout                       # it does fail open
    assert "AGI-MODEL-FENCE: NOT INSTALLED" in r.stderr, r.stderr
    assert "STATUS=unresolved:" in r.stdout, r.stdout
    assert r.returncode == 0                              # and does not break python


def test_falsifier_4_the_minus_S_bypass_is_real_and_named(standin_tree):
    """Falsifier 4, measured: `python -S` skips site, so the NAME fence does
    not apply. This test exists so the residual cannot quietly become a claim
    of closure; the node body names the escaping command verbatim. The second
    layer (mem_cap's RLIMIT_AS) is process-wide, not name-based."""
    env = {"PATH": os.environ.get("PATH", "/usr/bin:/bin"),
           "PYTHONPATH": os.pathsep.join([str(FENCE_DIR), str(standin_tree)]),
           "AGI_MODEL_FENCE_SRC": str(TABLE)}
    fenced = subprocess.run([sys.executable, "-c", _PROBE], capture_output=True,
                            text=True, timeout=120, env=env)
    assert "REFUSED-ModelLoadRefused-CALLS=0" in fenced.stdout
    escaped = subprocess.run([sys.executable, "-S", "-c", _PROBE],
                             capture_output=True, text=True, timeout=120, env=env)
    assert "NOT-REFUSED" in escaped.stdout, (
        "if -S no longer escapes, falsifier 4 is CLOSED -- update the node body")
    assert "AGI-MODEL-FENCE: NOT INSTALLED" not in escaped.stderr
