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
from pathlib import Path


def _load_cli():
    bin_dir = Path(__file__).resolve().parents[1] / "bin"
    spec = importlib.util.spec_from_file_location("agi_cli_wait", bin_dir / "cli.py")
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
    assert cli.cmd_wait(_args(max_seconds=-1.0)) == 2
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
