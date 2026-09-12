"""SL7.14 / SL7.19 — the MANDATORY two-tree rotate-self alert fixture.

Closes the two measured gaps of
hypothesis:l4-a-two-tree-rotate-self-alert-fixture-reads-verified-under-
enforcing-and-keeps-the-old-key-on-a-failed-push, on a REAL bare origin +
MAIN clone + a LINKED worktree (`git worktree add`) for the rotating seat,
every path under tmp_path:

  GAP 1 (rotate.py `_announce_rotation` `[rotation-alert]` envelope was
         NEVER sent through the resolver): a REAL rotation-alert block
         produced by `_announce_rotation` with REAL `send.send` +
         `send.send_dm` under `comms.verify = enforcing`, read back through
         REAL `send._verify_block`, carries a label that startswith
         `VERIFIED seat-a` — never FORGED / UNVERIFIABLE / REFUSED / withheld.
         `_verify_block`'s resolver fetches the PUSHED set from the bare
         origin and falls back to MAIN's committed row — the two-tree
         authority `test_absent_pushed_row_two_tree*` proves on a hand-built
         envelope but never through the alert path.

  GAP 2 (rotate.py `_commit_spawn_row` push leg + `_apply_successor_key_gated`):
         a REAL failed own-row push — the origin remote is REMOVED so
         `git push origin season/s2` FAILS — keeps `seats/seat-a.key`
         BYTE-IDENTICAL, the `push:` stderr line NAMES the failure, and the
         deferred swap return reads `key_replace: NOT applied -- push did not
         succeed`. SL7.09's contract, first time through a real failed push.
         The success complement (origin present) proves the swap DOES complete
         the flip, so the byte-identity on failure is a real detection, not a
         fixture that can never tell.

The linked worktree is the two-tree shape the claim demands:
`send._shared_graph_root`/`_shared_seats_path` rebase a worktree call to MAIN
through `locations.git_common_root`; `_verify_block` `git show HEAD:`'s
MAIN's committed row from that top-level. All git is REAL (the conftest
tmux guard passes non-tmux subprocess through); tmux is refused by the guard.
The geometry lives in BOTH spellings a real tree carries: `.agi/nodes/...`
(send's pushed/committed reader) and `nodes/...` (rotate's
geometry_resolver for `_derive_receivers`).

TESTS ONLY — nothing under extensions/agi/bin is edited. Reused, never
copied: `send_mod._seat_key_path` and rotate's `_announce_rotation` /
`_compose_announcement` / `_commit_spawn_row` / `_rotate_successor_key` /
`_apply_successor_key_gated`.
"""
from __future__ import annotations

import importlib.util
import json
import os
import subprocess
import sys
import types
from pathlib import Path

import pytest

EXT = Path(__file__).resolve().parents[2]      # extensions/ (namespace pkg)
BIN = Path(__file__).resolve().parents[1] / "bin"
TST = Path(__file__).resolve().parents[0]     # tests/ (namespace pkg)
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(EXT))
sys.path.insert(0, str(TST))

from test_rotate_handover import _FakeTmux  # noqa: E402  (reused, never copied)

import send as _send  # noqa: E402  (the top-level module rotate lazily binds)
from agi.bin import rotate  # noqa: E402

spec = importlib.util.spec_from_file_location("send_mod", BIN / "send.py")
send_mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(send_mod)

SEASON = "season/s2"


def _sh(cmd, cwd=None, check=True):
    r = subprocess.run(cmd, cwd=str(cwd) if cwd else None,
                       capture_output=True, text=True, timeout=60)
    if check and r.returncode != 0:
        raise AssertionError(
            f"{' '.join(cmd)} in {cwd} rc={r.returncode}: "
            f"{r.stderr.strip() or r.stdout.strip()}")
    return r.stdout.strip(), r.stderr.strip()


def _seats_md(rows):
    body = "---\nid: config:seats\ntype: config\nseats:\n"
    for r in rows:
        body += "  - " + json.dumps(r) + "\n"
    body += "---\n"
    return body


def _init_main(tmp_path, rows, comms):
    root = tmp_path / "main"
    (root / ".agi" / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    (root / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    (root / ".agi" / "config.json").write_text(json.dumps(
        {"metric_primary": "x", "comms": comms}))
    _geo = _seats_md(rows)
    (root / ".agi" / "nodes" / ".geometry" / "seats.md").write_text(
        _geo, encoding="utf-8")
    (root / "nodes" / ".geometry" / "seats.md").write_text(
        _geo, encoding="utf-8")
    (root / ".agi" / "sessions").mkdir(parents=True, exist_ok=True)
    (root / ".gitignore").write_text("sessions/\n", encoding="utf-8")
    # the rotation TEMPLATE for role `parent` — `cmd_rotate_self` refuses
    # loudly (`_resolve_template`) when the config:rotations node is absent,
    # so the fixture seed carries it (committed + pushed, so the linked
    # worktree inherits it). Shape mirrors test_rotate_handover._fix.
    _rot = (
        "---\nid: config:rotations\ntype: config\ntemplates:\n"
        "  parent:\n    brief_file: .agi/sessions/quorum/{seat}.md\n"
        "    steps: [handoff, rename, spawn, handover, readback, record, kill]\n"
        "    telemetry: []\n---\n")
    (root / "nodes" / ".geometry" / "rotations.md").write_text(_rot)
    (root / ".agi" / "nodes" / ".geometry" / "rotations.md").write_text(_rot)
    _sh(["git", "init", "-q", "-b", SEASON, str(root)])
    _sh(["git", "-C", str(root), "config", "user.email", "t@t"])
    _sh(["git", "-C", str(root), "config", "user.name", "t"])
    _sh(["git", "-C", str(root), "add", "-A"])
    _sh(["git", "-C", str(root), "commit", "-q", "-m", "seed seats"])
    return root


def _mk_worktree(tmp_path, main):
    origin = tmp_path / "remote.git"
    _sh(["git", "init", "--bare", "-q", str(origin)])
    _sh(["git", "-C", str(main), "remote", "add", "origin", str(origin)])
    _sh(["git", "-C", str(main), "push", "-q", "-u", "origin", SEASON])
    wt = tmp_path / "wt-seat-a"
    _sh(["git", "-C", str(main), "worktree", "add", "-q", "-b",
         "wt-seat-a-branch", str(wt), SEASON])
    return origin, wt


def _write_key(root, seat, priv_hex):
    kp = send_mod._seat_key_path(root, seat)
    kp.parent.mkdir(parents=True, exist_ok=True)
    kp.write_text(json.dumps({"scheme": "ed25519", "priv_hex": priv_hex}))
    os.chmod(kp, 0o600)
    return kp


def _two_tree(tmp_path):
    """ONE fixture: bare origin + MAIN (keyed seat-a row, recipient row,
    `comms.verify = enforcing`) pushed to origin, a LINKED worktree for
    seat-a, and `seats/seat-a.key` (ed25519). Returns a namespace."""
    seat, recv = "seat-a", "recv"
    scheme = send_mod.seatsig.get("ed25519")
    priv, pub = scheme.keygen()
    rows = [
        {"name": seat, "sig_scheme": "ed25519", "pubkey": pub.hex(),
         "generation": 2, "role": "parent", "model": "x", "effort": "max",
         "settings": "", "harness": "claude-code"},
        {"name": recv, "role": "director", "model": "x", "effort": "max",
         "settings": ""},
    ]
    main = _init_main(tmp_path, rows, comms={"verify": "enforcing"})
    origin, wt = _mk_worktree(tmp_path, main)
    _write_key(wt, seat, priv.hex())
    row = {"name": seat, "pubkey": pub.hex(), "sig_scheme": "ed25519",
           "generation": 2, "role": "parent"}
    return types.SimpleNamespace(origin=origin, main=main, wt=wt,
                                 seat=seat, recv=recv, row=row)


def _bump_own_row(root, seat, gen):
    """Advance the seat's own row in MAIN's WORKING-TREE geometry (both
    spellings) — the stand-in for the s6.1 spawn-row write the rotation's
    session key rides onto."""
    for rel in (root / ".agi" / "nodes" / ".geometry" / "seats.md",
                root / "nodes" / ".geometry" / "seats.md"):
        rows = send_mod._load_seats_rows(rel.read_text(encoding="utf-8"))
        own = next((r for r in rows if r.get("name") == seat), None)
        assert own is not None, f"no own row for {seat} in {rel}"
        own["generation"] = gen
        rel.write_text(_seats_md(rows), encoding="utf-8")


def test_gap1_alert_reads_verified_under_enforcing_two_tree(
        tmp_path, capsys, monkeypatch):
    """GAP 1: a REAL `_announce_rotation` `[rotation-alert]` block, written by
    REAL `send.send` + REAL `send.send_dm` under `comms.verify = enforcing`
    into the fixture, is read back through REAL `send._verify_block` and
    labels `VERIFIED seat-a` — never FORGED / UNVERIFIABLE / REFUSED. The
    rotation-alert path finally crosses the resolver."""
    fx = _two_tree(tmp_path)
    delivered = rotate._announce_rotation(
        root=fx.wt, croot=fx.wt, seat=fx.seat, successor=fx.seat,
        gen_before=2, gen_after=3, trigger="meter due",
        handoff_path=f"{fx.seat}.handoff.md", in_flight="",
        live_names=[fx.seat, fx.recv])
    assert fx.recv in delivered, f"alert must reach {fx.recv}: {delivered}"
    # The dm is observed ON DISK, never through a monkeypatched `send_dm`:
    # rotate binds `send` lazily at call time, and in the full suite that
    # binding is not always the `send` object this module imported (an
    # earlier test may have re-imported it), so a wrapper installed on
    # `_send` can be invisible to rotate while the real dm still lands
    # (SL2#17 first cut, 08:36Z: passed alone, failed only in the full run).
    dm_log = send_mod._dm_path(fx.wt, fx.seat, fx.recv)
    assert dm_log.is_file(), f"the alert must land as a real dm: {dm_log}"
    assert "[rotation-alert]" in dm_log.read_text(encoding="utf-8")

    # read the recipient's inbox (written by real send.send on the worktree)
    # back through the real read -> _verify_block -> resolver path.
    send_mod.read(fx.wt, fx.recv, None)
    out = capsys.readouterr().out
    assert "VERIFIED seat-a" in out, out
    assert "FORGED" not in out and "UNVERIFIABLE" not in out \
        and "REFUSED" not in out and "withheld" not in out


def test_gap2_failed_push_keeps_old_key_byte_identical(tmp_path, capsys):
    """GAP 2 (b): origin REMOVED so the own-row push FAILS. Direct driver of
    the real rotate legs: `_rotate_successor_key` mints the pending successor
    key (deferred), `_commit_spawn_row` commits the own-row and its push
    FAILS for real, and REAL `_apply_successor_key_gated` refuses the swap —
    `seats/seat-a.key` BYTE-IDENTICAL and the `push:` line names the
    failure."""
    fx = _two_tree(tmp_path)
    key_path = send_mod._seat_key_path(fx.wt, fx.seat)
    before = key_path.read_bytes()

    key_rotation = rotate._rotate_successor_key(
        fx.wt, fx.seat, fx.row, gen_before=2, gen_after=3)
    assert key_rotation and key_rotation.get("pending_key"), \
        "a keyed seat must mint a pending successor key"

    _bump_own_row(fx.main, fx.seat, 3)
    _sh(["git", "-C", str(fx.main), "remote", "remove", "origin"])
    commit_outcome = rotate._commit_spawn_row(
        fx.wt, seat=fx.seat, generation=3, session_id="u1",
        window="@1", pid=99)
    _push_line = commit_outcome.rpartition("\npush: ")[2]
    assert "push:" in commit_outcome, commit_outcome
    assert "FAILED" in _push_line, \
        f"push line must NAME the refusal: {_push_line!r}"
    err = capsys.readouterr().err
    assert "push: FAILED" in err, f"stderr must name the push failure: {err}"

    outcome = rotate._apply_successor_key_gated(
        key_rotation, "config:seats row gen 3", commit_outcome)
    assert outcome.startswith("key_replace: NOT applied"), outcome
    assert "push did not succeed" in outcome, outcome
    assert key_path.read_bytes() == before, \
        "the key file must be BYTE-IDENTICAL after a failed push"


def test_gap2_success_push_completes_the_swap(tmp_path, capsys):
    """GAP 2 (a) complement: origin PRESENT, the own-row push SUCCEEDS, and
    REAL `_apply_successor_key_gated` COMPLETES the swap — the key flips from
    the snapshot and the `push:` line names success. Proves the byte-identity
    on failure is a detection, not a fixture that never flips."""
    fx = _two_tree(tmp_path)
    key_path = send_mod._seat_key_path(fx.wt, fx.seat)
    before = key_path.read_bytes()

    key_rotation = rotate._rotate_successor_key(
        fx.wt, fx.seat, fx.row, gen_before=2, gen_after=3)
    assert key_rotation and key_rotation.get("pending_key")

    _bump_own_row(fx.main, fx.seat, 3)
    commit_outcome = rotate._commit_spawn_row(
        fx.wt, seat=fx.seat, generation=3, session_id="u1",
        window="@1", pid=99)
    _push_line = commit_outcome.rpartition("\npush: ")[2]
    assert "OK" in _push_line, \
        f"push line must name success: {_push_line!r}"

    outcome = rotate._apply_successor_key_gated(
        key_rotation, "config:seats row gen 3", commit_outcome)
    assert outcome.startswith(
        "key_replace: wrote successor key"), outcome
    assert key_path.read_bytes() != before, \
        "a successful push must flip the key to the successor"


# ---------------------------------------------------------------------------
# GAP 3 (THIS iteration, experiment:a00-79126269-184ecb) — drive the REAL
# `cmd_rotate_self` handover machine itself, from the LINKED worktree, with
# the fake tmux (`_FakeTmux` from test_rotate_handover, subclassed to name
# the successor window) monkeypatched over the spawn path and `_read_ack`
# answered `continue`. The parent's demotion reason: the three GAP-1/2 tests
# drive the rotate legs (`_announce_rotation` / `_commit_spawn_row` /
# `_apply_successor_key_gated`) DIRECTLY — none enters cmd_rotate_self,
# which is where spawn / broker / readback / kill and the worktree rebase
# actually live. The three tests below close that: the FULL rotate-self span
# runs on REAL git bytes (real bare origin + MAIN on season/s2 + linked
# worktree), the checklist `_prepare_checks` is REAL (the worktree branch is
# pushed -u so check 1's `@{u}` resolves), and the only seams are the two
# the hypothesis names: the fake tmux over `rotate.spawn_window` and
# `_read_ack` answered `continue`.
#
#   test_self_cmd_success_reaches_verified_alert       — (a) rc==0, the
#     rotation-alert dm reads back `VERIFIED seat-a` under enforcing, the
#     push: line names OK, the successor key swap COMPLETES (the full
#     handover flips seats/seat-a.key), the rotation record says `success`.
#   test_self_cmd_origin_removed_blocks_the_checklist — (b) the hypothesis's
#     exact mechanism (`git remote remove origin`). MEASURED DEFECT: this
#     BLOCKS the captive rotate-out checklist (`no upstream for
#     wt-seat-a-branch`, rotate.py:9143-ish) BEFORE the rotation can reach
#     the push — so cmd_rotate_self returns 3, never 0, and the key stays
#     byte-identical for the WRONG reason (rotation refused, not
#     push-failure-deferred). xfail(strict=True); never patches rotate.py.
#   test_self_cmd_pre_receive_refuses_push_keeps_key  — (b') the push-failure
#     deferral reached through the FULL machine by a mechanism that keeps
#     the checklist GREEN (a bare-origin pre-receive hook refuses the own-
#     row push): rc==0, `push: FAILED` names it, seats/seat-a.key stays
#     BYTE-IDENTICAL, and the alert still reads `VERIFIED seat-a` under the
#     OLD key. This is the honest way the (b) contract actually fires.
#
# `_rot_self_args` mirrors test_rotate_handover._rotate_self_args but keeps
# every field cmd_rotate_self getattrs (its `adv-alive` default is not
# portable), and the window-file fixture is a subclass of `_FakeTmux` so the
# successor spawn writes the SEAT's plain name (not the reuse's hardcoded
# `adv-alive`).
#


class _TwoTreeTmux(_FakeTmux):
    """`_FakeTmux` with the successor spawn naming THIS seat's plain window
    (`_FakeTmux.fake_spawn` hardcodes `adv-alive`; a seat-a rotation needs
    the reused window to be `seat-a` for the successor-window guarantee).
    The live set includes `recv` so `_announce_rotation`'s `_derive_receivers`
    intersects a live recipient window (a rotate-self drives live_names from
    the observed tmux windows; GAP 1 passed live_names in by hand, GAP 3 must
    not)."""

    def __init__(self, tmpfs, seat="seat-a", recv="recv"):
        super().__init__(tmpfs, initial=[seat, recv])
        self.seat = seat
        self.recv = recv

    def fake_spawn(self, **kw):
        self.spawned.append(kw["name"])
        with open(self.win, "a", encoding="utf-8") as fh:
            fh.write(self.seat + "\n")
        return 0, "echo hi"


def _rot_self_args(tmpfs, **over):
    base = dict(name="seat-a", force=False, timeout=60, debug_file=None,
                model=None, effort=None, settings=None, prompt_file=None,
                tmux_session="t", window_path=None, dry_run=False,
                throwaway=False, successor_argv=None, role="parent",
                session_ref="00000000-0000-4000-8000-000000000000", successor_transcript=None, own_pid=None,
                belam_prefix=None, ask_diff=False, stops=None, stops_file=None,
                template=None, comms_root=None, in_flight=None, trigger=None,
                grid_commit_legal=False, grid_commit_branch=None,
                verification_argv=None, registry_dir=None, registry_poll=None,
                after_join=False, own_chain=None, view_path=None, prepare=False)
    base.update(over)
    return types.SimpleNamespace(**base)


def _push_wt_upstream(fx):
    """Push the linked worktree's branch -u so `_prepare_checks` check 1's
    `@{u}` resolves (the rotate-out checklist refuses an un-upstreamed
    branch by name; the real guard is inert under pytest, AGI_TIER unset)."""
    _sh(["git", "-C", str(fx.wt), "push", "-q", "-u", "origin",
         "wt-seat-a-branch"])


def _drive_self(fx, monkeypatch, capsys, tmp_path, seat="seat-a"):
    """Drive the REAL cmd_rotate_self from the linked worktree with the two
    named seams (fake tmux over spawn_window, `_read_ack` -> continue) and
    return (rc, args, ft)."""
    ft = _TwoTreeTmux(tmp_path, seat)
    monkeypatch.setattr(rotate, "spawn_window", ft.fake_spawn)
    # SL7.40's turn-driven model confirm (run_after_join, rotate-self fallback
    # included) polls the successor transcript with REAL sleeps for up to
    # DEFAULT_AFTER_JOIN_TIMEOUT_S when no assistant turn appears; the fake
    # successor here never produces one, so zero the budget (the confirm
    # records `skipped: no assistant turn within 0s`, nothing waits).
    monkeypatch.setattr(rotate, "DEFAULT_AFTER_JOIN_TIMEOUT_S", 0)
    monkeypatch.setattr(
        rotate, "_read_ack",
        lambda *a, **k: {"seat": seat, "gen_after": 3, "answer": "continue",
                         "session_ref": ""})
    args = _rot_self_args(tmp_path, window_path=str(ft.win))
    rc = rotate.cmd_rotate_self(args, fx.wt)
    return rc, args, ft


def _alert_read(fx, capsys):
    """Read the recipient's inbox through the real read -> _verify_block
    resolver, as GAP 1 does, and return the collected stdout."""
    send_mod.read(fx.wt, fx.recv, None)
    return capsys.readouterr().out


def test_self_cmd_success_reaches_verified_alert(tmp_path, capsys, monkeypatch):
    """(a) the REAL cmd_rotate_self, driven from the LINKED worktree with the
    fake tmux + `_read_ack`->continue seams, returns 0; the [rotation-alert]
    dm it announces reads back `VERIFIED seat-a` under enforcing, the `push:`
    line names OK, the successor-key swap COMPLETES through the full handover
    (seats/seat-a.key flips), and the rotation record says `success`."""
    fx = _two_tree(tmp_path)
    _push_wt_upstream(fx)
    key_path = send_mod._seat_key_path(fx.wt, fx.seat)
    before = key_path.read_bytes()

    rc, _, _ = _drive_self(fx, monkeypatch, capsys, tmp_path)
    assert rc == 0, f"cmd_rotate_self must succeed from the linked worktree: {rc}"
    err = capsys.readouterr().err
    assert "push: OK" in err, f"push line must name success: {err}"

    out = _alert_read(fx, capsys)
    assert "VERIFIED seat-a" in out, out
    assert "FORGED" not in out and "UNVERIFIABLE" not in out \
        and "REFUSED" not in out and "withheld" not in out

    # the success handover flips the key to the successor (full machine swap,
    # not just the direct `_apply_successor_key_gated` GAP-2 leg).
    assert key_path.read_bytes() != before, \
        "a successful full rotate-self must flip seats/seat-a.key"

    # the durable record says success, and the successor row advanced to gen 3.
    rot = fx.main / ".agi" / "sessions" / "rotations"
    recs = sorted(rot.glob(f"{fx.seat}.*.json"))
    assert recs, f"no rotation record under {rot}"
    rec = json.loads(recs[-1].read_text(encoding="utf-8"))
    assert rec["result"] == "success", rec.get("result")


@pytest.mark.xfail(strict=True,
                   reason="hypothesis (b) mechanism defect: removing origin "
                            "blocks the rotate-out checklist on 'no upstream "
                            "for wt-seat-a-branch' BEFORE any push; see node")
def test_self_cmd_origin_removed_is_measured_xfail(tmp_path, capsys,
                                                   monkeypatch):
    """The same origin-removed drives as a strict marker of the measured
    defect, so the failing assertion above is not the suite's last word.
    This is the honest recording of the (b) mechanism gap."""
    fx = _two_tree(tmp_path)
    _push_wt_upstream(fx)
    key_path = send_mod._seat_key_path(fx.wt, fx.seat)
    before = key_path.read_bytes()
    _sh(["git", "-C", str(fx.main), "remote", "remove", "origin"])

    rc, _, _ = _drive_self(fx, monkeypatch, capsys, tmp_path)
    err = capsys.readouterr().err
    assert rc == 0, f"expected rc==0; got {rc}; {err[:600]}"
    assert key_path.read_bytes() == before


def test_self_cmd_pre_receive_refuses_push_keeps_key(tmp_path, capsys,
                                                     monkeypatch):
    """(b') the push-failure deferral reached through the FULL cmd_rotate_self
    by a mechanism that keeps the checklist GREEN: a bare-origin pre-receive
    hook REFUSES the own-row push (fetch still works, so the checklist's
    `@{u}`/behind reads and the alert's origin fetch all keep working).
    cmd_rotate_self returns 0, the `push:` line NAMES the failure, seats/
    seat-a.key stays BYTE-IDENTICAL (the swap deferred), and the alert still
    reads `VERIFIED seat-a` under the OLD key."""
    fx = _two_tree(tmp_path)
    _push_wt_upstream(fx)
    key_path = send_mod._seat_key_path(fx.wt, fx.seat)
    before = key_path.read_bytes()

    hd = fx.origin / "hooks"
    hd.mkdir(parents=True, exist_ok=True)
    (hd / "pre-receive").write_text(
        "#!/bin/sh\necho 'refusing for the test' >&2\nexit 1\n")
    (hd / "pre-receive").chmod(0o755)

    rc, _, _ = _drive_self(fx, monkeypatch, capsys, tmp_path)
    assert rc == 0, f"a refused own-row push must still be a graceful rotate-self: {rc}"
    err = capsys.readouterr().err
    assert "push: FAILED" in err, f"push line must NAME the refusal: {err}"

    out = _alert_read(fx, capsys)
    assert "VERIFIED seat-a" in out, out
    assert "FORGED" not in out and "UNVERIFIABLE" not in out \
        and "REFUSED" not in out

    assert key_path.read_bytes() == before, \
        "the key file must be BYTE-IDENTICAL after a refused own-row push"
    # the durable record is a SUCCESS even though the swap was deferred — the
    # push refusal is recorded, not fatal.
    rot = fx.main / ".agi" / "sessions" / "rotations"
    recs = sorted(rot.glob(f"{fx.seat}.*.json"))
    assert recs
    rec = json.loads(recs[-1].read_text(encoding="utf-8"))
    assert rec["result"] == "success", rec.get("result")

