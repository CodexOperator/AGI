"""An UNREADABLE tmux server is never reported as a gone window.

hypothesis:g1-send-says-cannot-list-windows-never-window-gone. On the live
box the tmux socket dir is mode 0700 owned by another uid, so EVERY
`list-windows` returns non-zero. Before the fix send.py collapsed that into
`[]` -- indistinguishable from "the session really has no such window" -- and
printed a confident "row window @5 is gone and no window named X is listed"
about a LIVE master. The file sweep carried the message; the line lied.

Two fixtures, both fake subprocess: an UNREADABLE listing (rc != 0) must say
"cannot list windows" and never "gone"; a READABLE listing that lacks the
target must still say "gone" (falsifier 2 -- the true case survives).

The red-on-trunk witness is the FOURTH test: it monkeypatches the two lookup
helpers (`_window_listed`, `_window_id_listed`) back to today's collapsing
`False`-for-everything semantics and asserts THAT build prints "gone". If the
patch stops changing the behaviour, the witness is measuring nothing.
"""
from __future__ import annotations

import subprocess
import sys

from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
_TS = str(Path(__file__).resolve().parent)
if _TS not in sys.path:
    sys.path.insert(0, _TS)

import send as send_mod  # noqa: E402


def _unreadable_tmux(monkeypatch):
    """Every `tmux list-windows` fails with rc=1 -- what a 0700 socket dir
    owned by another uid returns. Records calls; never a real tmux."""
    calls = []

    def fake_run(cmd, capture_output, text, timeout):
        calls.append(cmd)
        if cmd[:2] == ["tmux", "list-windows"]:
            return subprocess.CompletedProcess(
                cmd, 1, stdout="", stderr="no server running")
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(send_mod.subprocess, "run", fake_run)
    monkeypatch.setattr(send_mod.time, "sleep", lambda s: None)
    return calls


def _readable_tmux(monkeypatch, window_names):
    calls = []

    def fake_run(cmd, capture_output, text, timeout):
        calls.append(cmd)
        if cmd[:2] == ["tmux", "list-windows"]:
            return subprocess.CompletedProcess(
                cmd, 0, stdout="\n".join(window_names), stderr="")
        return subprocess.CompletedProcess(cmd, 0, stdout="", stderr="")

    monkeypatch.setattr(send_mod.subprocess, "run", fake_run)
    monkeypatch.setattr(send_mod.time, "sleep", lambda s: None)
    return calls


# ── (1) unreadable server: "cannot list", never "gone" ────────────────────

def test_unreadable_lookups_answer_none_not_false(monkeypatch):
    """The TRI-STATE contract on its own: an unreadable server answers None
    from BOTH lookups -- never False, which the send arm would read as a gone
    window. (These pure helpers print nothing, so the "no gone wording" half
    lives in the seat-row tests below.)"""
    _unreadable_tmux(monkeypatch)
    assert send_mod._window_listed("agi", "sanctuary-master") is None
    assert send_mod._window_id_listed("agi", "@5") is None


def test_windowless_recipient_stays_a_silent_no_op(tmp_path, monkeypatch,
                                                   capsys):
    """A row that CLAIMED no window keeps the silent no-op it always had --
    on an unreadable box that silence is the same as before the fix, so the
    fix adds no per-tick stderr flood to the sweep (test_send's one-line
    refusal conjunct depends on it)."""
    _unreadable_tmux(monkeypatch)
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    assert send_mod._nudge_target(tmp_path, "sanctuary-master", None) is None
    assert capsys.readouterr().err == ""


# ── (2) the @id repair branch: unreadable is not a STALE @id ──────────────

def _write_seats(project: Path, rows) -> None:
    from test_send import _seats_md
    (project / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    (project / "nodes" / ".geometry" / "seats.md").write_text(_seats_md(rows))


def test_unreadable_never_calls_a_live_at_id_stale(tmp_path, monkeypatch,
                                                   capsys):
    _unreadable_tmux(monkeypatch)
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    _write_seats(tmp_path, [{"name": "sanctuary-master", "role": "director",
                             "window": "@5", "pid": 424242}])
    assert send_mod._nudge_target(tmp_path, "sanctuary-master", None) is None
    err = capsys.readouterr().err
    assert "cannot list windows" in err, err
    assert "is gone" not in err, f"an unreadable server proves no staleness: {err}"


# ── (3) a READABLE listing without the target still says "gone" ───────────

def test_absent_window_in_a_readable_listing_still_says_gone(
        tmp_path, monkeypatch, capsys):
    """Falsifier 2, NON-vacuously: a seats row CLAIMS "@5" and the READABLE
    listing holds neither "@5" nor the name -- so the target really is absent
    and the line must be the positive "is gone" one."""
    _readable_tmux(monkeypatch, ["@246", "somebody-else"])
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    _write_seats(tmp_path, [{"name": "sanctuary-master", "role": "director",
                             "window": "@5", "pid": 424242}])
    assert send_mod._nudge_target(tmp_path, "sanctuary-master", None) is None
    err = capsys.readouterr().err
    assert "is gone" in err, err
    assert "no window named sanctuary-master is listed" in err, err
    assert "cannot list windows" not in err, err


def test_name_window_row_on_an_unreadable_server_says_cannot_list(
        tmp_path, monkeypatch, capsys):
    """The carve-out is as wide as the claim: a row that CLAIMED a window --
    here a NAME, which the refusal arm clears -- still hears the ONE
    cannot-list line, never "gone". A rowless recipient stays silent (above)."""
    _unreadable_tmux(monkeypatch)
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    _write_seats(tmp_path, [{"name": "sanctuary-master", "role": "director",
                             "window": "sanctuary-master", "pid": 424242}])
    assert send_mod._nudge_target(tmp_path, "sanctuary-master", None) is None
    err = capsys.readouterr().err
    assert "cannot list windows" in err, err
    assert "gone" not in err, err


def test_repair_stale_id_false_builds_the_at_id_target_in_silence(
        tmp_path, monkeypatch, capsys):
    """The DOCUMENTED opt-out: repair_stale_id=False never lists, so it must
    build the target straight from the @id -- and say nothing, not even
    cannot-list. The TARGET is the assertion; stderr alone would be vacuous.
    """
    _unreadable_tmux(monkeypatch)
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    _write_seats(tmp_path, [{"name": "sanctuary-master", "role": "director",
                             "window": "@5", "pid": 424242}])
    got = send_mod._nudge_target(tmp_path, "sanctuary-master", "agi",
                                 repair_stale_id=False)
    assert got == ("agi:@5", 424242, "agi"), got
    assert capsys.readouterr().err == ""


# ── (4) red-on-trunk witness ─────────────────────────────────────────────

def test_trunk_lookups_would_have_said_gone(tmp_path, monkeypatch, capsys):
    """Today's pre-fix lookups answered False for BOTH cases -- unreadable
    and absent alike. Drive the SAME code with that pair of lookups restored
    and the honest wording is gone: this is the line the hypothesis measured
    on the live box, reproduced on fixtures."""
    _unreadable_tmux(monkeypatch)
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    monkeypatch.setattr(send_mod, "_window_listed", lambda *a, **k: False)
    monkeypatch.setattr(send_mod, "_window_id_listed", lambda *a, **k: False)
    _write_seats(tmp_path, [{"name": "sanctuary-master", "role": "director",
                             "window": "@5", "pid": 424242}])
    assert send_mod._nudge_target(tmp_path, "sanctuary-master", None) is None
    err = capsys.readouterr().err
    assert "is gone" in err, f"trunk wording not reproduced: {err}"
    assert "cannot list windows" not in err, err
