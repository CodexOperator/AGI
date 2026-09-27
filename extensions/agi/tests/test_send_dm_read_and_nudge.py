"""RED-FIRST probes for
hypothesis:send-read-prints-every-unread-block-and-every-dm-send-nudges.

Three conjuncts, probed independently on the CURRENT bytes:

  (a) `send.py read <me>` prints every unread block from its inbox file AND
      every dm file it is party to, and says "empty" only when BOTH are empty;
  (b) no path advances the inbox read marker past a block read did not print;
  (c) every send that lands in a dm file fires the recipient nudge, through
      the same path an inbox send uses.

SAFETY: every test drives a TMP graph root, a TMP comms root and a TMP inbox
under pytest's tmp_path. tmux is stubbed (`_fake_tmux`); no live pane, no
send-keys, no live session, no live inbox, no live dm file, no host, no user
name, no absolute path literal in this file.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
_TS = str(Path(__file__).resolve().parent)
if _TS not in sys.path:
    sys.path.insert(0, _TS)

import send as send_mod  # noqa: E402

from test_send import (  # noqa: E402
    _fake_tmux,
    _seats_md,
    _seat_pubkey_hex,
    _typed,
)

ME = "seat-a"
PEER = "seat-b"


@pytest.fixture
def project(tmp_path: Path) -> Path:
    """A throwaway G11 project root: `.agi/config.json` + empty inbox dir."""
    root = tmp_path / "proj"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage"}))
    (root / ".agi" / "sessions" / "inbox").mkdir(parents=True)
    return root


@pytest.fixture
def croot(project: Path) -> Path:
    """A throwaway comms root INSIDE the throwaway project (never the live
    `comms/season-N/`): `send_dm` resolves the graph root from the comms
    root to find the SEATS row, so a comms root outside any project would
    exercise a different code path than the real one."""
    c = project / "comms" / "season-test"
    (c / "dm").mkdir(parents=True)
    return c


def _inbox(project: Path, who: str = ME) -> Path:
    return project / ".agi" / "sessions" / "inbox" / f"{who}.md"


def _dm(croot: Path, a: str = ME, b: str = PEER) -> Path:
    return send_mod._dm_path(croot, a, b)


def _write_dm_block(croot: Path, a: str, b: str, to: str, text: str) -> Path:
    """Append one dm block to `<a>--<b>.md` with the writer's own block shape."""
    path = send_mod._dm_path(croot, a, b)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a") as f:
        f.write(send_mod._block(send_mod._now(), a, to, text))
    return path


def _read_cli(project: Path, croot: Path, who: str = ME, monkeypatch=None):
    """`send.py --from <who> read <who>`, exactly as the seat runs it."""
    monkeypatch.setattr(send_mod, "_project_root", lambda: project)
    monkeypatch.setattr(send_mod, "_nudge_window", lambda *a, **k: True)
    return send_mod.main(["--from", who, "--comms-root", str(croot),
                          "read", who])


# ── (a) an unread dm block must be printed by `read <me>` ─────────────────

def test_read_prints_unread_dm_block_while_inbox_is_empty(project, croot,
                                                          monkeypatch,
                                                          capsys):
    """CONJUNCT 1, print half: an unread dm block for ME, empty inbox file.

    GREEN if the dm body reaches stdout; RED if `read` says the seat has
    nothing. The tmp inbox file is never created, so the inbox is genuinely
    empty and only the dm can carry the message.
    """
    _write_dm_block(croot, PEER, ME, ME, "dm-only-body-xyz")
    assert _read_cli(project, croot, monkeypatch=monkeypatch) == 0
    out = capsys.readouterr().out
    assert "dm-only-body-xyz" in out, (
        "an unread dm block addressed to ME was not printed by read: " + out)


def test_read_says_empty_only_when_inbox_AND_dms_are_both_empty(project,
                                                                croot,
                                                                monkeypatch,
                                                                capsys):
    """CONJUNCT 1, `empty` half: the literal empty verdict must not print
    while ANY dm channel still has an unread block -- `inbox for <me>: empty`
    is a claim about the whole of <me>'s mail, and today it is decided from
    the inbox file alone (send.py `read`, the early return before
    `read_dms` is ever called by the CLI)."""
    _write_dm_block(croot, PEER, ME, ME, "dm-only-body-xyz")
    assert _read_cli(project, croot, monkeypatch=monkeypatch) == 0
    out = capsys.readouterr().out
    assert "inbox for" not in out, (
        "read declared the seat EMPTY while a dm block was still unread: "
        + out)
    assert "empty" not in out, (
        "read printed an `empty` verdict with an unread dm block pending: "
        + out)


def test_read_dm_block_is_printed_once_and_the_dm_cursor_advances(project,
                                                                  croot,
                                                                  monkeypatch,
                                                                  capsys):
    """FALSIFIER from the target: a dm block must not print twice across two
    reads -- the dm read cursor (`<file>.state.json`) must advance too."""
    _write_dm_block(croot, PEER, ME, ME, "dm-once-body-xyz")
    assert _read_cli(project, croot, monkeypatch=monkeypatch) == 0
    first = capsys.readouterr().out
    assert first.count("dm-once-body-xyz") == 1, first
    assert _read_cli(project, croot, monkeypatch=monkeypatch) == 0
    second = capsys.readouterr().out
    assert "dm-once-body-xyz" not in second, (
        "the dm block printed a second time -- the dm cursor did not "
        "advance: " + second)


# ── (b) the read marker must never pass an unprinted block ────────────────

def _signing_seat(project: Path, seat: str) -> None:
    """One seat row + a real key, so a block it signs can be FORGED."""
    send_mod.keygen(project, seat)
    text = _seats_md(
        [{"name": seat, "role": "director", "window": "@9", "pid": 424242,
          "sig_scheme": "ed25519", "pubkey": _seat_pubkey_hex(project, seat)}])
    for base in (project, project / ".agi"):
        (base / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
        (base / "nodes" / ".geometry" / "seats.md").write_text(text)


def test_marker_never_advances_past_a_block_read_did_not_print(project,
                                                              monkeypatch,
                                                              capsys):
    """CONJUNCT 2: with a FORGED block withheld by the enforcing verifier
    (the one path where `read` deliberately does NOT print a block's bytes),
    the `# read up to here` marker must not come to sit after it.

    `read` writes the marker at END-OF-FILE regardless of how many blocks it
    printed (send.py `read`, the `inbox.write_text(content + READ_MARKER)`
    tail), so this is the probe that decides the conjunct.
    """
    (project / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage",
         "comms": {"verify": "enforcing"}}))
    _signing_seat(project, PEER)
    monkeypatch.setattr(send_mod, "_project_root", lambda: project)
    monkeypatch.setattr(send_mod, "_nudge_window", lambda *a, **k: True)
    send_mod.send(project, ME, "forged-block-body-xyz", PEER)
    inbox = _inbox(project)
    text = inbox.read_text()
    assert "sig:" in text, "the fixture block must be signed to be forgeable"
    # Tamper the BODY: the canonical message no longer matches the sig.
    inbox.write_text(text.replace("forged-block-body-xyz",
                                  "forged-block-body-xyz-tampered"))
    assert send_mod.main(["--from", ME, "read", ME]) == 0
    out = capsys.readouterr().out
    assert "REFUSED FORGED" in out, (
        "the fixture did not reach the refusing path: " + out)
    assert "forged-block-body-xyz-tampered" not in out, out
    after = inbox.read_text()
    marker = after.find(send_mod.READ_MARKER)
    body_at = after.find("forged-block-body-xyz-tampered")
    assert marker >= 0, "no read marker was written at all: " + repr(after)
    assert marker < body_at, (
        "the read marker sits AFTER a block read refused to print "
        "(marker at %d, withheld block at %d):\n%s\n---\n%s"
        % (marker, body_at, out, after))


def test_marker_write_is_independent_of_what_the_reader_printed(project,
                                                               monkeypatch,
                                                               capsys):
    """CONJUNCT 2, structural probe: `read` reaches the marker write with no
    dependence on the printing step at all. Stub the printer to print NOTHING
    and the marker still lands at end-of-file -- the file:line that rules out
    any "the marker follows what was printed" implementation."""
    inbox = _inbox(project)
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text(send_mod._block("2020-01-01T00:00:00Z", PEER, ME,
                                     "unprinted-block-xyz"))
    monkeypatch.setattr(send_mod, "_project_root", lambda: project)
    monkeypatch.setattr(send_mod, "_nudge_window", lambda *a, **k: True)
    monkeypatch.setattr(send_mod, "_print_blocks_with_labels",
                        lambda *a, **k: None)   # prints nothing at all
    assert send_mod.main(["--from", ME, "read", ME]) == 0
    assert capsys.readouterr().out == ""
    after = inbox.read_text()
    assert after.find(send_mod.READ_MARKER) < after.find("unprinted-block-xyz"), (
        "the marker passed a block nothing printed: " + repr(after))


# ── (c) a dm-file send fires the recipient nudge, same path as inbox ──────

def _seats(project: Path) -> None:
    """The ONE SEATS row file, written at BOTH roots the nudge resolver
    accepts: `<root>/nodes/.geometry` (what an inbox `send` is handed) and
    `<root>/.agi/nodes/.geometry` (what `send_dm` gets, resolving the graph
    root from the comms root). Identical bytes in both."""
    text = _seats_md(
        [{"name": PEER, "role": "director", "window": "@9", "pid": 424242},
         {"name": "seat-c", "role": "director", "window": "@10",
          "pid": 424244}])
    for base in (project, project / ".agi"):
        (base / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
        (base / "nodes" / ".geometry" / "seats.md").write_text(text)


PANE_WINDOWS = ["@8", "@9", "@10"]


def test_send_dm_reaches_the_nudge_window(project, croot, monkeypatch):
    """CONJUNCT 3: the block lands in the dm file AND `_nudge_window` is
    called for the RECIPIENT (the observable that actually exists: the pane
    path is stubbed, so the function call is the seam)."""
    _seats(project)
    seen = []

    def rec(root, to, tmux_session=None, **kw):
        seen.append((to, kw))
        return True

    monkeypatch.setattr(send_mod, "_nudge_window", rec)
    monkeypatch.setattr(send_mod, "_project_root", lambda: project)
    path = send_mod.send_dm(croot, ME, PEER, "dm-nudge-body-xyz", ME)
    assert "dm-nudge-body-xyz" in path.read_text(), "the dm file is the record"
    assert [t for t, _k in seen] == [PEER], (
        "send_dm landed a dm block without nudging the recipient: %r" % seen)
    assert seen[0][1].get("body") == "dm-nudge-body-xyz", seen


def test_dm_send_and_inbox_send_use_the_same_nudge_path(project, croot,
                                                        monkeypatch):
    """CONJUNCT 3, same-path half: an inbox send and a dm send must both
    reach the `_nudge_window` choke point for their recipient.

    The two recipients are DISTINCT seats, so the first nudge's unsubmitted-
    token marker cannot coalesce the second away -- a coalesce is a real
    documented behaviour and would hide the seam this test probes.
    """
    _seats(project)
    calls = _fake_tmux(monkeypatch, PANE_WINDOWS)
    monkeypatch.setattr(send_mod, "_registry_status", lambda pid: None)
    monkeypatch.setattr(send_mod, "_project_root", lambda: project)
    send_mod.send(project, "seat-c", "inbox-nudge-body-xyz", ME)
    inbox_typed = _typed(calls)
    assert inbox_typed, ("baseline: an inbox send to a windowed seat types "
                         "no nudge token: %r" % (calls,))
    send_mod.send_dm(croot, ME, PEER, "dm-nudge-body-xyz", ME)
    dm_typed = _typed(calls)[len(inbox_typed):]
    assert dm_typed, ("a send that landed in a dm file typed NO nudge: %r"
                      % (calls,))
    assert any("dm-nudge-body-xyz" in " ".join(c) for c in dm_typed), (
        "the dm nudge does not carry its body inline: %r" % (dm_typed,))
