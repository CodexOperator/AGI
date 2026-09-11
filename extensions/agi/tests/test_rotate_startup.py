"""Startup first_turn (hypothesis:l4-startup-is-one-script-or-a-driven-prompt,
0b round) — the pure runner in rotate.py: allowlist refusal, placeholder
resolution, per-command timeout, byte-cap truncation, `## STARTUP OUTPUT`
composition, and dry-run-runs-nothing. Hermetic — no graph, no real spawn, no
tmux; subprocess.run is monkeypatched where a command must "hang" or "overflow"
deterministically."""
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate

# A fully-filled values map matching the 11 canonical placeholders.
VALUES = {
    "seat": "sanctuary-director",
    "succ_ref": "abc123",
    "succ_name": "sd-next",
    "succ_transcript": "/tmp/sd-next.jsonl",
    "pin_ref": "/tmp/sanctuary-director.meter",
    "gen": "11",
    "prime_ref": "7cff1a",
    "worktree": "/wt",
    "repo": "/repo",
    "tmux_session": "agi-rc",
    "pred_pids": "123 456",
}


class _Proc:
    def __init__(self, rc=0, out="", err=""):
        self.returncode = rc
        self.stdout = out
        self.stderr = err


def _fake_run(monkeypatch, proc):
    def _run(cmd, **kwargs):
        return proc
    monkeypatch.setattr(rotate.subprocess, "run", _run)


def test_resolve_every_placeholder_and_unknown_is_refused():
    resolved = rotate._resolve_startup_placeholders(
        "python3 extensions/agi/bin/x.py --seat {seat} {succ_ref} {prime_ref}",
        VALUES)
    assert "sanctuary-director" in resolved
    assert "abc123" in resolved
    assert "7cff1a" in resolved
    assert "{" not in resolved  # nothing silently left in
    with pytest.raises(ValueError) as ei:
        rotate._resolve_startup_placeholders("echo {bogus}", VALUES)
    assert "bogus" in str(ei.value)


def test_producing_refusal_allows_shipped_commands():
    # The live director template's first_turn list — every producing verb
    # must pass the allowlist (engine python + read-only git + ps + curl +
    # read-only tmux) with stdio filters allowed after `|`.
    shipped = [
        "python3 extensions/agi/bin/rotate.py whois --seat {seat} --record latest",
        "python3 extensions/agi/bin/send.py whois {succ_ref} --claim {seat}",
        "git -C {worktree} status -sb | head -5; git -C {repo} status -sb | head -3",
        "python3 extensions/agi/bin/send.py read {seat}",
        "python3 extensions/agi/bin/spawn_budget.py status; "
        "python3 extensions/agi/bin/provisioning.py status | head -4",
        "python3 extensions/agi/bin/write.py -h | sed -n 1,40p",
    ]
    for cmd in shipped:
        assert rotate._producing_refusal(cmd) is None, cmd


def test_d_allowlist_refusal_names_label():
    startup = {"first_turn": [{"label": "danger", "cmd": "rm -rf /"}]}
    res = rotate._run_first_turn_commands(startup, VALUES)
    assert res[0]["refused"], res
    assert "rm" in res[0]["refused"]
    block = rotate._compose_startup_output(res)
    assert "[danger] REFUSED" in block
    assert "not on startup.allow" in block


def test_e_unknown_placeholder_refused_by_label():
    startup = {"first_turn": [
        {"label": "bad", "cmd": "python3 extensions/agi/bin/x.py {bogus}"},
    ]}
    res = rotate._run_first_turn_commands(startup, VALUES)
    assert res[0]["refused"] and "bogus" in res[0]["refused"]
    block = rotate._compose_startup_output(res)
    assert "[bad] REFUSED" in block


def test_a_composes_startup_output_block():
    results = [
        {"label": "rotation-record", "cmd": "python3 .../rotate.py whois",
         "rc": 0, "output": "row: gen 11", "truncated": False},
        {"label": "inbox", "cmd": "python3 .../send.py read sd",
         "rc": 0, "output": "no dms", "truncated": False},
    ]
    block = rotate._compose_startup_output(results)
    assert "## STARTUP OUTPUT (rotate-self ran these for you; you ran nothing)" \
        in block
    assert "[rotation-record] exit 0" in block
    assert "[inbox] exit 0" in block
    assert "row: gen 11" in block


def test_b_timeout_is_caught_and_named(monkeypatch):
    def _hang(cmd, **kwargs):
        raise subprocess.TimeoutExpired(cmd, 1)
    monkeypatch.setattr(rotate.subprocess, "run", _hang)
    startup = {"first_turn": [{"label": "slow", "cmd": "ps -e"}],
               "first_turn_timeout_s": 1}
    res = rotate._run_first_turn_commands(startup, VALUES)
    assert res[0]["timed_out_after_s"] == 1
    block = rotate._compose_startup_output(res)
    assert "[slow] TIMEOUT (>1s)" in block


def test_c_byte_cap_truncates_and_says_so(monkeypatch):
    _fake_run(monkeypatch, _Proc(rc=0, out="x" * 500))
    startup = {"first_turn": [{"label": "noisy", "cmd": "ps -e"}],
               "byte_cap": 10}
    res = rotate._run_first_turn_commands(startup, VALUES)
    assert res[0]["truncated"] is True
    assert len(res[0]["output"]) == 10
    block = rotate._compose_startup_output(res)
    assert "(output truncated to 10 bytes)" in block


def test_f_dry_run_runs_nothing(tmp_path):
    marker_dir = tmp_path / "bin"
    marker_dir.mkdir(parents=True, exist_ok=True)
    (marker_dir / "probe.py").write_text(
        "from pathlib import Path\nPath(%r).write_text('hi')\n" % str(
            tmp_path / "marker.txt"), encoding="utf-8")
    script = str(marker_dir / "probe.py")
    startup = {"first_turn": [{"label": "probe", "cmd": f"python3 {script}"}]}

    dry = rotate._run_first_turn_commands(startup, VALUES, dry_run=True)
    assert dry[0]["dry"] is True
    assert not (tmp_path / "marker.txt").exists()

    live = rotate._run_first_turn_commands(startup, VALUES, dry_run=False)
    assert live[0]["rc"] == 0
    assert (tmp_path / "marker.txt").exists()
