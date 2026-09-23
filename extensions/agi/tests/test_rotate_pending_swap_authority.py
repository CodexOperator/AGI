# test_rotate_pending_swap_authority.py -- EF.67, kid under
# hypothesis:the-pending-key-swap-completes-only-after-the-authority-publish.
# Closes R-EF51 M1 and R-EF20 M1/M2:
#   (a) a pending persisted by an `authority: FAILED`/HELD deferral is NOT
#       completed by a later push-OK site with no authority context (neither
#       `_finish_pending_swap_on_push` nor the DIRECT
#       `_complete_pending_key_swap`) -- the key file stays byte-identical
#       and the refusal NAMES the authority leg;
#   (b) `push: HELD` DEFERS in `_apply_successor_key_gated` exactly like
#       `push: FAILED` (R-EF20 M1) -- key byte-identical;
#   (c) back-compat: a push-only / legacy pending still completes on a later
#       push OK, and an `authority: SKIPPED` line (EF.56, no authority
#       branch) does NOT gate;
#   (d) the frozen-path test R-EF20 M2 asks for: every gated path leaves the
#       successor key file BYTE-IDENTICAL.
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate  # noqa: E402
from agi.bin import send as bin_send  # noqa: E402


def _mk_seat_key(root, seat):
    d = bin_send._seats_dir(root)
    d.mkdir(parents=True, exist_ok=True)
    sch = bin_send.seatsig.get("ed25519")
    priv, pub = sch.keygen()
    p = d / f"{seat}.key"
    p.write_text(json.dumps({"scheme": "ed25519",
                             "priv_hex": priv.hex()}), encoding="utf-8")
    os.chmod(p, 0o600)
    return p, priv.hex(), pub.hex()


def _patch_committed(monkeypatch, rows):
    """Patch `_seats_committed_rows` on BOTH module aliases: rotate's local
    `import send` is the top-level module, a different object from
    `agi.bin.send` (conftest's documented two-alias trap)."""
    monkeypatch.setattr(bin_send, "_seats_committed_rows", lambda root: rows)
    try:
        import send as _top  # noqa: PLC0415
        monkeypatch.setattr(_top, "_seats_committed_rows", lambda root: rows)
    except ImportError:
        pass


def _pending(root, seat, priv_hex, pub_hex, gen=7, reason=None):
    key = bin_send._seat_key_path(root, seat)
    pend = Path(str(key.parent / f"{key.name}.pending"))
    obj = {"scheme": "ed25519", "priv_hex": priv_hex, "pub_hex": pub_hex,
           "gen_after": gen, "minted_at": ""}
    if reason is not None:
        obj["deferred_for"] = reason
    pend.write_text(json.dumps(obj), encoding="utf-8")
    os.chmod(pend, 0o600)
    return key, pend


def _rotation(key_path, succ_priv, succ_pub):
    return {
        "scheme": "ed25519",
        "successor_pub": succ_pub,
        "retired": {"to": 9},
        "note": "",
        "pending_key": {"path": str(key_path), "scheme": "ed25519",
                        "priv_hex": succ_priv},
    }


def test_authority_deferred_pending_not_completed_by_push(tmp_path,
                                                          monkeypatch):
    """(a) R-EF51 M1: an authority-deferred pending survives a later push-OK
    site with NO authority context -- through the ONE helper AND the direct
    call. The key file stays byte-identical and the refusal names the
    authority leg."""
    from agi.bin import send as s
    key_path, _pred_priv, _pred_pub = _mk_seat_key(tmp_path, "aa")
    succ_priv, succ_pub = s.seatsig.get("ed25519").keygen()
    key, pend = _pending(tmp_path, "aa", succ_priv.hex(), succ_pub.hex(),
                         reason="authority")
    before = key_path.read_bytes()
    _patch_committed(monkeypatch, [{"name": "aa", "role": "parent",
                                    "pubkey": succ_pub.hex()}])
    # the push-OK site that passes NO authority line
    r = rotate._finish_pending_swap_on_push(tmp_path, "aa", "push: OK")
    assert r.startswith("key swap NOT completed"), r
    assert "AUTHORITY" in r, r
    assert key_path.read_bytes() == before, "authority deferral must not flip"
    assert pend.exists(), "pending must survive"
    # the DIRECT call (`cmd_rotate_self` before a mint) also refuses
    r2 = rotate._complete_pending_key_swap(tmp_path, "aa")
    assert r2.startswith("key swap NOT completed"), r2
    assert "AUTHORITY" in r2, r2
    assert key_path.read_bytes() == before
    assert pend.exists()


def test_push_held_defers_in_apply_successor_key_gated(tmp_path):
    """(b) R-EF20 M1: a `push: HELD` (gated veto push) defers exactly like
    `push: FAILED` -- the key does not flip, the deferred pending is
    persisted naming the PUSH leg."""
    key_path, _pred_priv, _pred_pub = _mk_seat_key(tmp_path, "bb")
    succ_priv, succ_pub = bin_send.seatsig.get("ed25519").keygen()
    kr = _rotation(key_path, succ_priv.hex(), succ_pub.hex())
    before = key_path.read_bytes()
    r = rotate._apply_successor_key_gated(
        kr, "config:seats row bb: ...",
        "spawn_row_commit: committed (sha abc)\n"
        "push: push: HELD -- merge-up push is a gated act")
    assert "NOT applied" in r and "push did not succeed" in r, r
    assert key_path.read_bytes() == before, "a HELD push must not flip the key"
    pend = Path(str(key_path.parent / f"{key_path.name}.pending"))
    assert pend.is_file(), "a HELD push must persist the deferred swap"
    assert json.loads(pend.read_text())["deferred_for"] == "push"


def test_push_deferral_still_completes_on_push_ok(tmp_path, monkeypatch):
    """(c) back-compat: a `deferred_for: "push"` (and a legacy reason-less)
    pending still completes on a later push OK, and an `authority: SKIPPED`
    line (EF.56: no authority branch -- a non-attempt) does NOT gate."""
    from agi.bin import send as s
    for seat, reason in (("cc", "push"), ("dd", None)):
        key_path, _p, _pub = _mk_seat_key(tmp_path, seat)
        succ_priv, succ_pub = s.seatsig.get("ed25519").keygen()
        key, pend = _pending(tmp_path, seat, succ_priv.hex(),
                             succ_pub.hex(), reason=reason)
        _patch_committed(monkeypatch,
                         [{"name": seat, "role": "helper",
                           "pubkey": succ_pub.hex()}])
        r = rotate._finish_pending_swap_on_push(tmp_path, seat, "push: OK")
        assert r.startswith("key swap completed"), (seat, reason, r)
        assert not pend.exists()
        assert json.loads(key.read_text())["priv_hex"] == succ_priv.hex()
    # EF.56: an authority-deferred pending completes when the caller
    # supplies the non-gating SKIPPED line (nothing was published).
    key_path, _p, _pub = _mk_seat_key(tmp_path, "ee")
    succ_priv, succ_pub = s.seatsig.get("ed25519").keygen()
    key, pend = _pending(tmp_path, "ee", succ_priv.hex(), succ_pub.hex(),
                         reason="authority")
    _patch_committed(monkeypatch, [{"name": "ee", "role": "kid",
                                    "pubkey": succ_pub.hex()}])
    r = rotate._finish_pending_swap_on_push(
        tmp_path, "ee", "push: OK",
        authority_line="authority: SKIPPED -- no authority branch")
    assert r.startswith("key swap completed"), r
    assert not pend.exists()


def test_gated_paths_leave_successor_key_bytes_frozen(tmp_path, monkeypatch):
    """(d) R-EF20 M2: freeze the successor key file bytes and assert EVERY
    gated path leaves them byte-identical -- push HELD, authority FAILED,
    authority HELD, push-OK with no authority context, direct completion."""
    from agi.bin import send as s
    key_path, _pred_priv, _pred_pub = _mk_seat_key(tmp_path, "ff")
    succ_priv, succ_pub = s.seatsig.get("ed25519").keygen()
    kr = _rotation(key_path, succ_priv.hex(), succ_pub.hex())
    frozen = key_path.read_bytes()
    # 1. push HELD
    r = rotate._apply_successor_key_gated(
        kr, "config:seats row ff: ...",
        "spawn_row_commit: committed (sha 1)\npush: push: HELD -- veto")
    assert "NOT applied" in r and key_path.read_bytes() == frozen
    # 2. authority FAILED (push OK)
    r2 = rotate._apply_successor_key_gated(
        kr, "config:seats row ff: ...",
        "spawn_row_commit: committed (sha 2)\npush: push: OK -- trunk\n"
        "authority: FAILED -- remote refused")
    assert "NOT applied" in r2 and key_path.read_bytes() == frozen
    # 3. authority HELD
    r3 = rotate._apply_successor_key_gated(
        kr, "config:seats row ff: ...",
        "spawn_row_commit: committed (sha 3)\npush: push: OK -- trunk\n"
        "authority: HELD -- prime FROZEN")
    assert "NOT applied" in r3 and key_path.read_bytes() == frozen
    # the persisted pending is authority-deferred (reason recorded).
    pend = Path(str(key_path.parent / f"{key_path.name}.pending"))
    assert json.loads(pend.read_text())["deferred_for"] == "authority"
    _patch_committed(monkeypatch, [{"name": "ff", "role": "helper",
                                    "pubkey": succ_pub.hex()}])
    # 4. push-OK site with NO authority context
    r4 = rotate._finish_pending_swap_on_push(tmp_path, "ff", "push: OK")
    assert "NOT completed" in r4 and key_path.read_bytes() == frozen
    # 5. direct completion, no authority context
    r5 = rotate._complete_pending_key_swap(tmp_path, "ff")
    assert "NOT completed" in r5 and key_path.read_bytes() == frozen
    assert pend.exists()


def test_authority_ok_completes_an_authority_deferred_pending(
        tmp_path, monkeypatch):
    """The gate is not a wall: an authority-deferred pending DOES complete
    when the caller supplies an `authority: OK` line -- the swap is deferred
    until the authority publish actually succeeds, then flips."""
    from agi.bin import send as s
    key_path, _p, _pub = _mk_seat_key(tmp_path, "gg")
    succ_priv, succ_pub = s.seatsig.get("ed25519").keygen()
    key, pend = _pending(tmp_path, "gg", succ_priv.hex(), succ_pub.hex(),
                         reason="authority")
    _patch_committed(monkeypatch, [{"name": "gg", "role": "parent",
                                    "pubkey": succ_pub.hex()}])
    r = rotate._finish_pending_swap_on_push(
        tmp_path, "gg", "push: OK",
        authority_line="authority: OK -- abc -> season2/main")
    assert r.startswith("key swap completed"), r
    assert not pend.exists()
    assert json.loads(key.read_text())["priv_hex"] == succ_priv.hex()