"""hypothesis:l5-a-parent-waits-for-its-kid-in-the-foreground-and-a-turn-end-
with-a-live-kid-is-named-not-a-death, conjunct 1: `cli.py wait`.

A parent must block IN-PROCESS on its kid's terminal status instead of ending
its harness turn (in headless `-p` a turn-end IS process exit). Red-first:
before the fix there was no `wait` verb at all, so every assertion below
failed with an argparse exit 2.

The poll interval is injected on the module (`_WAIT_POLL_SECONDS = 0`) and
`time.sleep` is faked, so these tests spawn nothing and never wall-clock.
"""

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

#: The round's base ref tip, resolved at authoring time with
#: `git merge-base HEAD season2/loops/hypothesis-wait-returns-on-an-em-a00-72e9d440`.
#: Hardcoded so the red-on-pre-fix proof is reproducible forever.
_BASE_SHA = "76a6be473cfe5f0ec09268635c9159868ef7eb8a"

#: The PRE-ROUND tip (`git rev-parse HEAD` at authoring time, `6e6ef7fe5`),
#: which returned 0 on an empty kid set; hardcoded so round 2's red is forever.
_PRE_ROUND_SHA = "6e6ef7fe5ba06fae83918b430cb646e9e52df4ca"


def _load_cli():
    bin_dir = Path(__file__).resolve().parents[1] / "bin"
    spec = importlib.util.spec_from_file_location("agi_cli_wait", bin_dir / "cli.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_base_cli(tmp_path):
    """Load `cmd_wait`'s PRE-FIX bytes from the base ref as a tmp module.

    The module's sibling imports (`locations`, `spawn_budget`, ...) resolve only
    if `extensions/agi/bin` is at the FRONT of sys.path first.
    """
    repo = Path(__file__).resolve().parents[3]
    bin_dir = Path(__file__).resolve().parents[1] / "bin"
    src = subprocess.run(
        ["git", "show", f"{_BASE_SHA}:extensions/agi/bin/cli.py"],
        cwd=repo, capture_output=True, text=True, check=True).stdout
    tmp_mod = tmp_path / "base_cli.py"
    tmp_mod.write_text(src)
    if str(bin_dir) not in sys.path:
        sys.path.insert(0, str(bin_dir))
    spec = importlib.util.spec_from_file_location("agi_cli_wait_base", tmp_mod)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_pre_round_cli(tmp_path):
    """Load cli.py's bytes as of the PRE-ROUND tip (before this round's edit)."""
    repo = Path(__file__).resolve().parents[3]
    bin_dir = Path(__file__).resolve().parents[1] / "bin"
    src = subprocess.run(
        ["git", "show", f"{_PRE_ROUND_SHA}:extensions/agi/bin/cli.py"],
        cwd=repo, capture_output=True, text=True, check=True).stdout
    tmp_mod = tmp_path / "pre_round_cli.py"
    tmp_mod.write_text(src)
    if str(bin_dir) not in sys.path:
        sys.path.insert(0, str(bin_dir))
    spec = importlib.util.spec_from_file_location("agi_cli_wait_pre", tmp_mod)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _fixture(tmp_path, monkeypatch, agents):
    cli = _load_cli()
    man = tmp_path / "sessions" / "iter-007" / "manifest.json"
    man.parent.mkdir(parents=True)
    man.write_text(json.dumps({"agents": agents}))
    monkeypatch.setattr(cli, "_session_root", lambda: tmp_path)
    monkeypatch.setattr(cli, "_legacy_fallback", lambda root, p: p)
    monkeypatch.setattr(cli, "_WAIT_POLL_SECONDS", 0.0)
    return cli, man


def _args(**kw):
    base = dict(iter_n=7, agent=[], max_seconds=10.0)
    base.update(kw)
    return argparse.Namespace(**base)


def test_wait_returns_zero_after_the_manifest_flips(tmp_path, monkeypatch, capsys):
    """A fake manifest flipping to done on the 3rd poll returns 0 after 3
    heartbeat lines -- the kid is named with its status each poll."""
    cli, man = _fixture(tmp_path, monkeypatch,
                        [{"id": "k1", "tier": "kid", "status": "running"}])
    sleeps = []

    def fake_sleep(_s):
        sleeps.append(_s)
        if len(sleeps) == 2:
            man.write_text(json.dumps(
                {"agents": [{"id": "k1", "tier": "kid", "status": "done"}]}))

    monkeypatch.setattr(cli.time, "sleep", fake_sleep)
    assert cli.cmd_wait(_args()) == 0
    out = capsys.readouterr().out
    assert out.count("wait 7:") == 3
    assert "k1=running" in out and "k1=done" in out


def test_wait_timeout_returns_two_and_names_the_agent(tmp_path, monkeypatch, capsys):
    """When max-seconds elapses with the kid still running, wait returns 2 and
    stderr names the still-running agent -- never a silent success."""
    cli, _man = _fixture(tmp_path, monkeypatch,
                         [{"id": "k1", "tier": "kid", "status": "running"}])
    # deadline already passed: one poll, then the timeout path
    assert cli.cmd_wait(_args(max_seconds=-1.0)) == cli._WAIT_TIMEOUT
    assert "still running: k1" in capsys.readouterr().err


def test_wait_defaults_to_kids_and_ignores_the_parent_row(tmp_path, monkeypatch):
    """The default set is every `tier: kid` row; the round's own parent row
    (tier parent, status running) must never hold the wait open."""
    cli, _man = _fixture(tmp_path, monkeypatch, [
        {"id": "p1", "tier": "parent", "status": "running"},
        {"id": "k1", "tier": "kid", "status": "failed"},
    ])
    assert cli.cmd_wait(_args()) == 0


def test_wait_missing_manifest_is_an_error_not_a_hang(tmp_path, monkeypatch):
    cli = _load_cli()
    monkeypatch.setattr(cli, "_session_root", lambda: tmp_path)
    monkeypatch.setattr(cli, "_legacy_fallback", lambda root, p: p)
    assert cli.cmd_wait(_args()) == 1


def test_wait_empty_kid_set_returns_a_named_code_at_once(
        tmp_path, monkeypatch, capsys):
    """DEF5 case 1: an iter with NO `tier: kid` row returns the named
    `_WAIT_NO_KID_ROWS` at once -- it never sleeps to the deadline and never
    returns 2 with an empty `still running:` line. Zero kid rows after
    `dispatch --detach` returned means no kid was ever spawned
    (dispatch.py:2933 writes the manifest BEFORE dispatch returns), so a
    silent 0 would let the parent end its turn with nothing running."""
    cli, _man = _fixture(tmp_path, monkeypatch,
                         [{"id": "p1", "tier": "parent", "status": "running"}])
    monkeypatch.setattr(cli, "_WAIT_POLL_SECONDS", 300.0)
    sleeps = []
    monkeypatch.setattr(cli.time, "sleep", lambda s: sleeps.append(s))
    monkeypatch.setattr(cli.time, "monotonic", lambda: 100.0)
    rc = cli.cmd_wait(_args(max_seconds=999.0))
    assert rc == cli._WAIT_NO_KID_ROWS
    assert rc not in (0, 1, 2, cli._WAIT_NO_AGENT)
    assert sleeps == []  # a poll to the deadline would have slept
    err = capsys.readouterr().err
    assert "no tier:kid row" in err and "iter 7" in err


def test_wait_agent_absent_from_manifest_is_named_at_once(
        tmp_path, monkeypatch, capsys):
    """DEF5 case 2: `--agent X` where X matches no manifest row returns the
    named `_WAIT_NO_AGENT` code at once, and stderr names X."""
    cli, _man = _fixture(tmp_path, monkeypatch,
                         [{"id": "k1", "tier": "kid", "status": "running"}])
    monkeypatch.setattr(cli, "_WAIT_POLL_SECONDS", 300.0)
    sleeps = []
    monkeypatch.setattr(cli.time, "sleep", lambda s: sleeps.append(s))
    monkeypatch.setattr(cli.time, "monotonic", lambda: 100.0)
    rc = cli.cmd_wait(_args(agent=["ghost"], max_seconds=999.0))
    assert rc == cli._WAIT_NO_AGENT
    assert rc not in (1, 2)
    assert sleeps == []
    assert "ghost" in capsys.readouterr().err


def test_wait_every_heartbeat_line_carries_elapsed(
        tmp_path, monkeypatch, capsys):
    """DEF1: every heartbeat line carries each agent's elapsed whole seconds,
    keeping the `id=status` shape; a row with no `started_at` reads elapsed=0s."""
    cli, man = _fixture(tmp_path, monkeypatch, [
        {"id": "k1", "tier": "kid", "status": "running", "started_at": 1000},
        {"id": "k2", "tier": "kid", "status": "running"},
    ])
    monkeypatch.setattr(cli.time, "time", lambda: 1012.0)
    monkeypatch.setattr(cli.time, "monotonic", lambda: 0.0)
    monkeypatch.setattr(cli, "_WAIT_POLL_SECONDS", 0.0)
    assert cli.cmd_wait(_args(max_seconds=-1.0)) == cli._WAIT_TIMEOUT
    out = capsys.readouterr().out
    assert "k1=running elapsed=12s" in out
    assert "k2=running elapsed=0s" in out  # absent started_at never raises


def test_pre_fix_base_sha_polls_empty_kid_set_to_timeout(
        tmp_path, monkeypatch, capsys):
    """RED-ON-PRE-FIX: the base-ref `cmd_wait` on an empty-kid manifest sleeps
    to the deadline and returns 2 (with an empty `still running:` line), while
    the same fixture on the built bytes returns 0 at once."""
    base = _load_base_cli(tmp_path)
    man = tmp_path / "base" / "sessions" / "iter-007" / "manifest.json"
    man.parent.mkdir(parents=True)
    man.write_text(json.dumps(
        {"agents": [{"id": "p1", "tier": "parent", "status": "running"}]}))
    monkeypatch.setattr(base, "_session_root", lambda: tmp_path / "base")
    monkeypatch.setattr(base, "_legacy_fallback", lambda root, p: p)
    monkeypatch.setattr(base, "_WAIT_POLL_SECONDS", 0.0)
    sleeps = []
    monkeypatch.setattr(base.time, "sleep", lambda s: sleeps.append(s))
    # a clock that advances one second per check: the deadline is reached
    clock = iter([0.0, 1.0, 2.0, 3.0, 4.0, 5.0])
    monkeypatch.setattr(base.time, "monotonic", lambda: next(clock))
    assert base.cmd_wait(_args(max_seconds=2.0)) == 2
    assert sleeps  # it polled/slept to the deadline instead of returning
    assert "still running: " in capsys.readouterr().err

    # the built bytes on the SAME fixture name the condition at once (green)
    cli, _man = _fixture(tmp_path, monkeypatch,
                         [{"id": "p1", "tier": "parent", "status": "running"}])
    monkeypatch.setattr(cli.time, "monotonic", lambda: 0.0)
    assert cli.cmd_wait(_args(max_seconds=999.0)) == cli._WAIT_NO_KID_ROWS


def test_pre_round_base_sha_returns_zero_on_an_empty_kid_set(
        tmp_path, monkeypatch, capsys):
    """RED-ON-PRE-FIX (round 2): the pre-round tip returns 0 on an empty kid
    set -- the silent success the named `_WAIT_NO_KID_ROWS` replaces."""
    base = _load_pre_round_cli(tmp_path)
    man = tmp_path / "pre" / "sessions" / "iter-007" / "manifest.json"
    man.parent.mkdir(parents=True)
    man.write_text(json.dumps(
        {"agents": [{"id": "p1", "tier": "parent", "status": "running"}]}))
    monkeypatch.setattr(base, "_session_root", lambda: tmp_path / "pre")
    monkeypatch.setattr(base, "_legacy_fallback", lambda root, p: p)
    monkeypatch.setattr(base, "_WAIT_POLL_SECONDS", 0.0)
    monkeypatch.setattr(base.time, "monotonic", lambda: 0.0)
    sleeps = []
    monkeypatch.setattr(base.time, "sleep", lambda s: sleeps.append(s))
    assert base.cmd_wait(_args(max_seconds=999.0)) == 0
    assert sleeps == []
