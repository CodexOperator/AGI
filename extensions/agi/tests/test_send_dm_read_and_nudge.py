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


# ── (b) the read marker never passes an unread VALID block read did not print

def _three_blocks(project: Path, bodies=("a1", "a2", "a3")) -> Path:
    """An inbox file holding `len(bodies)` unsigned blocks, in order."""
    inbox = _inbox(project)
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text("".join(
        send_mod._block("2020-01-01T00:00:00Z", PEER, ME, b) for b in bodies))
    return inbox


def _read_twice(project, croot, monkeypatch, capsys):
    """Two `read <me>` calls, returning (first stdout, second stdout)."""
    assert _read_cli(project, croot, monkeypatch=monkeypatch) == 0
    first = capsys.readouterr().out
    assert _read_cli(project, croot, monkeypatch=monkeypatch) == 0
    return first, capsys.readouterr().out


def test_every_block_prints_exactly_once_across_two_reads(project, croot,
                                                          monkeypatch, capsys):
    """D1: a multi-block inbox prints each block ONCE, in order, across two
    reads. The marker's cut offset used to be computed from the WHOLE
    marker-stripped file while the printer indexed the UNREAD SLICE, so with
    a marker present `starts[last + 1]` landed one block EARLY and the block
    just printed re-printed on the next read."""
    _three_blocks(project)
    first, second = _read_twice(project, croot, monkeypatch, capsys)
    order = [b for b in ("a1", "a2", "a3") if b in first]
    assert order == ["a1", "a2", "a3"], "blocks must print in order: " + first
    for b in ("a1", "a2", "a3"):
        assert first.count(b) == 1, f"{b} printed {first.count(b)}x: " + first
        assert b not in second, f"{b} re-printed on the second read: " + second


def test_each_block_prints_once_with_no_marker_present(project, croot,
                                                       monkeypatch, capsys):
    """D1, the no-marker case: with NO marker in the file the unread region is
    the whole file, and the same once-each property must hold."""
    inbox = _three_blocks(project)
    assert send_mod.READ_MARKER not in inbox.read_text(), "fixture precondition"
    first, second = _read_twice(project, croot, monkeypatch, capsys)
    for b in ("a1", "a2", "a3"):
        assert first.count(b) == 1, f"{b} printed {first.count(b)}x: " + first
        assert b not in second, f"{b} re-printed on the second read: " + second
    assert send_mod.READ_MARKER in inbox.read_text(), (
        "the read wrote no marker at all: " + repr(inbox.read_text()))


def test_marker_stays_put_when_no_printer_ran(project, croot, monkeypatch,
                                              capsys):
    """D2: when nothing printed (the printer is stubbed to print nothing),
    the marker must stay WHERE IT WAS -- the old `last < 0 -> cut = 0` branch
    rewrote it at the top of the file, destroying its position and un-reading
    the mail behind it."""
    inbox = _three_blocks(project)
    _read_cli(project, croot, monkeypatch=monkeypatch)
    capsys.readouterr()
    with open(inbox, "a") as f:      # a new arrival BEHIND the marker
        f.write(send_mod._block("2020-01-01T00:00:00Z", PEER, ME, "a4"))
    before = inbox.read_text()
    at = before.index(send_mod.READ_MARKER)
    monkeypatch.setattr(send_mod, "_print_blocks_with_labels",
                        lambda *a, **k: None)   # prints nothing at all
    assert _read_cli(project, croot, monkeypatch=monkeypatch) == 0
    after = inbox.read_text()
    assert after.index(send_mod.READ_MARKER) == at, (
        "the marker moved although nothing printed:\n%r\n---\n%r"
        % (before, after))
    assert after.index("a4") > after.index(send_mod.READ_MARKER), (
        "the marker passed a VALID block nothing printed: " + repr(after))
    assert after.index("a1") < after.index(send_mod.READ_MARKER), (
        "the marker jumped to the top of the file: " + repr(after))


def test_withheld_forged_block_between_two_printed_blocks(project, croot,
                                                         monkeypatch, capsys):
    """D3 + D4: a FORGED block withheld BETWEEN two VALID blocks must not
    retire unread VALID mail, and it IS consumed (the committed rule at
    test_send.py:5757/5775 -- the inbox drains so the same bytes are never
    re-refused; the quarantine keeps the one copy). The narrowed conjunct 2 is
    `the marker never passes an unread VALID block that was not printed`."""
    (project / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "outcome_coverage",
         "comms": {"verify": "enforcing"}}))
    _signing_seat(project, PEER)
    monkeypatch.setattr(send_mod, "_project_root", lambda: project)
    monkeypatch.setattr(send_mod, "_nudge_window", lambda *a, **k: True)
    _three_blocks(project, ("a1",))
    inbox = _inbox(project)
    send_mod.send(project, ME, "forged-block", PEER)   # the signed middle one
    with open(inbox, "a") as f:
        f.write(send_mod._block("2020-01-01T00:00:00Z", PEER, ME, "a3"))
    text = inbox.read_text()
    assert text.count("sig:") == 1, "exactly one block must be signed"
    # Tamper the MIDDLE body only: its canonical message no longer matches.
    inbox.write_text(text.replace("forged-block", "forged-tampered"))
    assert send_mod.main(["--from", ME, "read", ME]) == 0
    out = capsys.readouterr().out
    assert "REFUSED FORGED" in out, "the fixture missed the refusing path: " + out
    for b in ("a1", "a3"):
        # the BODY LINE, not the bare string: a random pubkey hex in the
        # keygen output can contain "a1" and flake this assertion
        assert out.count("\n%s\n" % b) == 1, (
            "the VALID block %s did not print: " % b) + out
    after = inbox.read_text()
    marker = after.index(send_mod.READ_MARKER)
    for b in ("a1", "a3"):
        assert marker > after.index(b), (
            "the marker retired the VALID block %s that read printed" % b)
    # the withheld block is consumed (committed rule), not re-refused forever
    assert send_mod.main(["--from", ME, "read", ME]) == 0
    out2 = capsys.readouterr().out
    assert "REFUSED FORGED" not in out2, (
        "the withheld block was never consumed: " + out2)
    q = _inbox(project).parent / "quarantine" / f"{ME}.md"
    assert q.read_text().count("forged-tampered") == 1, (
        "the quarantine must keep exactly one durable copy: " + q.read_text())


def test_marker_never_advances_past_a_block_read_did_not_print(project,
                                                              monkeypatch,
                                                              capsys):
    """NARROWED CONJUNCT 2: the marker never passes an unread VALID block the
    read did not print. The withheld-FORGED case is NOT this conjunct -- it is
    the committed rule at test_send.py:5757/5775 (`read` advances past a
    withheld block, the quarantine keeps the copy), now pinned by
    `test_withheld_forged_block_between_two_printed_blocks` above. The probe
    that decides this conjunct is a printer that walks NOTHING."""
    inbox = _inbox(project)
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text(send_mod._block("2020-01-01T00:00:00Z", PEER, ME,
                                     "unprinted-block-xyz"))
    monkeypatch.setattr(send_mod, "_project_root", lambda: project)
    monkeypatch.setattr(send_mod, "_nudge_window", lambda *a, **k: True)
    monkeypatch.setattr(send_mod, "_print_blocks_with_labels",
                        lambda *a, **k: None)   # walks nothing, prints nothing
    assert send_mod.main(["--from", ME, "read", ME]) == 0
    assert capsys.readouterr().out == ""
    after = inbox.read_text()
    assert after.find(send_mod.READ_MARKER) < after.find("unprinted-block-xyz"), (
        "the marker passed a VALID block nothing printed: " + repr(after))


def _partial_printer(monkeypatch, n: int):
    """A printer that walks only the FIRST `n` blocks of the region and
    answers the index of the last one it printed -- the P3 shape: a printer
    that DID run (its answer is an int) but did not walk the whole region."""
    real = send_mod._print_blocks_with_labels

    def partial(root, me, blocks, **kw):
        return real(root, me, list(blocks)[:n], **kw)

    monkeypatch.setattr(send_mod, "_print_blocks_with_labels", partial)
    return partial


def test_partial_printer_does_not_retire_the_blocks_it_never_walked(project,
                                                                   monkeypatch,
                                                                   capsys):
    """P3: a printer that printed only the FIRST of three VALID blocks still
    answers an int, so `read` knows a printer ran -- but the two blocks it
    never walked were never SEEN, and the marker must not pass them."""
    inbox = _three_blocks(project)
    monkeypatch.setattr(send_mod, "_project_root", lambda: project)
    monkeypatch.setattr(send_mod, "_nudge_window", lambda *a, **k: True)
    _partial_printer(monkeypatch, 1)
    assert send_mod.main(["--from", ME, "read", ME]) == 0
    first = capsys.readouterr().out
    assert "a1" in first, first
    assert "a2" not in first and "a3" not in first, first
    after = inbox.read_text()
    at = after.index(send_mod.READ_MARKER)
    assert at > after.index("a1"), ("the marker ate the one printed block: "
                                   + repr(after))
    for b in ("a2", "a3"):
        assert at < after.index(b), (
            "the marker retired the VALID block %s the printer never "
            "walked: %r" % (b, after))
    # and the blocks the printer never walked are still unread: the second
    # read (same partial printer) reaches a2, and never repeats a1
    assert send_mod.main(["--from", ME, "read", ME]) == 0
    second = capsys.readouterr().out
    assert second.count("a2") == 1, second
    assert "a1" not in second, "a1 re-printed: " + second
    assert "a3" not in second, ("a3 printed although the partial printer "
                                "never walked it: " + second)


def test_partial_printer_with_a_marker_already_in_the_file(project,
                                                           monkeypatch, capsys):
    """P3, with the marker PRESENT: the unread region is the slice behind the
    marker, so a partial printer must cut inside that slice, not at its end."""
    inbox = _inbox(project)
    inbox.parent.mkdir(parents=True, exist_ok=True)
    inbox.write_text(
        send_mod._block("2020-01-01T00:00:00Z", PEER, ME, "a1")
        + send_mod.READ_MARKER                       # a1 already read
        + send_mod._block("2020-01-01T00:00:00Z", PEER, ME, "a2")
        + send_mod._block("2020-01-01T00:00:00Z", PEER, ME, "a3"))
    monkeypatch.setattr(send_mod, "_project_root", lambda: project)
    monkeypatch.setattr(send_mod, "_nudge_window", lambda *a, **k: True)
    _partial_printer(monkeypatch, 1)
    assert send_mod.main(["--from", ME, "read", ME]) == 0
    first = capsys.readouterr().out
    assert "a1" not in first, "a1 was already read: " + first
    assert "a2" in first and "a3" not in first, first
    after = inbox.read_text()
    at = after.index(send_mod.READ_MARKER)
    for b in ("a1", "a2"):
        assert at > after.index(b), (
            "the marker un-read the printed block %s: %r" % (b, after))
    assert at < after.index("a3"), (
        "the marker retired a3, which the partial printer never walked: %r"
        % after)

def _signing_seat(project: Path, seat: str) -> None:
    """One seat row + a real key, so a block it signs can be FORGED."""
    send_mod.keygen(project, seat)
    text = _seats_md(
        [{"name": seat, "role": "director", "window": "@9", "pid": 424242,
          "sig_scheme": "ed25519", "pubkey": _seat_pubkey_hex(project, seat)}])
    for base in (project, project / ".agi"):
        (base / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
        (base / "nodes" / ".geometry" / "seats.md").write_text(text)


def test_marker_write_is_independent_of_what_the_reader_printed(project,
                                                               monkeypatch,
                                                               capsys):
    """CONJUNCT 2, structural probe: `read` reaches the marker write with no
    dependence on the printing step's RETURN VALUE beyond "did a printer
    run". A stub printing nothing leaves the marker before the block; the
    read is still fully consumed (sidecars, counts) either way."""
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


def test_box_local_row_does_not_print_empty_before_the_dm_sweep(project, croot,
                                                               monkeypatch,
                                                               capsys):
    """D5: the `--box-local` mail_poll branch read each local row WITHOUT
    `quiet_empty=True`, so `inbox for <nm>: empty` printed BEFORE the row's dm
    channels were swept -- a false `empty` line per row. The row's own verdict
    is decided after `read_dms`, exactly as the positional path does."""
    _write_dm_block(croot, PEER, ME, ME, "dm-only-body-xyz")
    rows = [{"name": ME, "role": "director", "window": "@9", "pid": 424242,
             "box": "local"}]
    monkeypatch.setattr(send_mod, "_locally_loaded_rows", lambda r: rows)
    monkeypatch.setattr(send_mod, "_project_root", lambda: project)
    monkeypatch.setattr(send_mod, "_nudge_window", lambda *a, **k: True)
    rc = send_mod.main(["--from", ME, "--comms-root", str(croot),
                        "read", "--box-local"])
    out = capsys.readouterr().out
    assert rc == 0, out
    assert "dm-only-body-xyz" in out, "the row's dm block never printed: " + out
    assert "inbox for" not in out, (
        "the box-local branch declared the row EMPTY before the sweep: " + out)
    # a row with nothing at all still gets its (post-sweep) empty verdict
    monkeypatch.setattr(send_mod, "_locally_loaded_rows",
                        lambda r: [{"name": "seat-c", "box": "local"}])
    assert send_mod.main(["--from", ME, "--comms-root", str(croot),
                          "read", "--box-local"]) == 0
    assert "inbox for seat-c: empty" in capsys.readouterr().out


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
