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


def _write_readable_veto_cell(g):
    from seatsig import veto
    veto.save(g, {
        "veto_room": "veto", "rate_limit_per_window": 1,
        "window_seconds": 3600, "expiry_seconds": 86400,
        "active_gates": [], "vetoes": [],
    })


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

# ---------------------------------------------------------------------------
# EF.84 (experiment:a00-6c3c02f2-8362a0) -- conjunct A: an authority-deferred
# pending COMPLETES at the next successful authority publish; conjunct B: send
# signs with the key the AUTHORITY row holds (the live predecessor), never the
# pending successor.
# ---------------------------------------------------------------------------
import subprocess  # noqa: E402


def _git(repo, *args, check=True):
    return subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True, check=check)


def _posts_text(rows):
    body = "---\nid: config:posts\ntype: config\nposts:\n"
    for r in rows:
        body += "  - " + json.dumps(r) + "\n"
    body += "---\n"
    return body


def _authority_fixture(tmp_path, old_pub, new_pub, sig_scheme=None):
    """bare origin + repo: origin/season2/main holds `old_pub` for `aa`; the
    local trunk HEAD holds `new_pub` (the committed re-key the authority never
    received). ``sig_scheme`` is added only to the trunk row when requested,
    modelling the deferred window's real authority fallback."""
    repo = tmp_path / "repo"
    g = repo / ".agi"
    (g / "nodes" / ".geometry").mkdir(parents=True)
    _write_readable_veto_cell(g)
    (g / "config.json").write_text("{}", encoding="utf-8")
    posts = g / "nodes" / ".geometry" / "posts.md"
    rows = [{"name": "aa", "role": "parent", "pubkey": old_pub}]
    posts.write_text(_posts_text(rows), encoding="utf-8")
    bare = tmp_path / "remote.git"
    subprocess.run(["git", "init", "--bare", "-q", str(bare)], check=True)
    subprocess.run(["git", "-C", str(repo), "init", "-q", "-b", "trunk"],
                   check=True)
    _git(repo, "config", "user.email", "t@t")
    _git(repo, "config", "user.name", "t")
    _git(repo, "remote", "add", "origin", str(bare))
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "authority seed")
    _git(repo, "push", "-q", "origin", "HEAD:refs/heads/season2/main")
    _git(repo, "push", "-q", "-u", "origin", "trunk")
    rows[0] = dict(rows[0], pubkey=new_pub,
                   **({"sig_scheme": sig_scheme} if sig_scheme else {}))
    posts.write_text(_posts_text(rows), encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-q", "-m", "re-key on trunk")
    _git(repo, "push", "-q", "origin", "trunk")
    return repo, g, posts, bare


def _write_keys(g, seat, pred_priv, succ_priv, succ_pub, reason):
    key = bin_send._seat_key_path(g, seat)
    key.parent.mkdir(parents=True, exist_ok=True)
    key.write_text(json.dumps({"scheme": "ed25519",
                               "priv_hex": pred_priv.hex()}))
    os.chmod(key, 0o600)
    pend = Path(str(key) + ".pending")
    pend.write_text(json.dumps({"scheme": "ed25519",
                                "priv_hex": succ_priv.hex(),
                                "pub_hex": succ_pub.hex(),
                                "deferred_for": reason,
                                "gen_after": 2, "minted_at": ""}))
    os.chmod(pend, 0o600)
    return key, pend


def test_authority_deferred_pending_completes_at_next_publish(tmp_path):
    """EF.84 conjunct A: a later push-OK site RE-PUBLISHES the committed row
    to the authority and completes the authority-deferred swap -- the
    authority ref advances, `<seat>.key` flips to the successor, the pending
    file is deleted. RED on the pre-fix bytes (the site refuses by name)."""
    sch = bin_send.seatsig.get("ed25519")
    succ_priv, succ_pub = sch.keygen()
    pred_priv, pred_pub = sch.keygen()
    repo, g, posts, _bare = _authority_fixture(
        tmp_path, pred_pub.hex(), succ_pub.hex())
    key, pend = _write_keys(g, "aa", pred_priv, succ_priv, succ_pub,
                            "authority")
    frozen = key.read_bytes()
    r = rotate._finish_pending_swap_on_push(g, "aa", "push: OK")
    assert r.startswith("key swap completed"), r
    assert not pend.exists(), "the completed swap deletes the pending file"
    assert json.loads(key.read_text())["priv_hex"] == succ_priv.hex(), \
        "the live key must now be the successor"
    assert key.read_bytes() != frozen
    # the authority now holds the successor pubkey, predecessor gone.
    _git(repo, "fetch", "-q", "origin", "season2/main")
    show = _git(repo, "show",
                "origin/season2/main:.agi/nodes/.geometry/posts.md").stdout
    assert succ_pub.hex() in show and pred_pub.hex() not in show


def test_authority_publish_failed_keeps_key_byte_identical(tmp_path):
    """EF.84 conjunct A precision: an authority-deferred pending whose
    re-publish FAILS stays deferred -- key byte-identical, pending survives,
    a named refusal prints. Never raises."""
    sch = bin_send.seatsig.get("ed25519")
    succ_priv, succ_pub = sch.keygen()
    pred_priv, pred_pub = sch.keygen()
    repo, g, posts, bare = _authority_fixture(
        tmp_path, pred_pub.hex(), succ_pub.hex())
    key, pend = _write_keys(g, "aa", pred_priv, succ_priv, succ_pub,
                            "authority")
    frozen = key.read_bytes()
    # a pre-receive hook refuses the authority push -> `authority: FAILED`.
    hook = bare / "hooks" / "pre-receive"
    hook.parent.mkdir(parents=True, exist_ok=True)
    hook.write_text("#!/bin/sh\n"
                    "while read old new ref; do\n"
                    "  case \"$ref\" in refs/heads/season2/main) "
                    "echo 'refused by test' >&2; exit 1;; esac\n"
                    "done\nexit 0\n")
    os.chmod(hook, 0o755)
    r = rotate._finish_pending_swap_on_push(g, "aa", "push: OK")
    assert "NOT completed" in r and key.read_bytes() == frozen
    assert pend.exists()


def test_push_deferred_pending_never_touches_the_authority(tmp_path):
    """EF.84 conjunct A precision: with NO authority-deferred pending (a
    push-deferred one) the later push-OK completes the swap the OLD way and
    attempts NO authority publish -- the authority ref does not move."""
    sch = bin_send.seatsig.get("ed25519")
    succ_priv, succ_pub = sch.keygen()
    pred_priv, pred_pub = sch.keygen()
    repo, g, posts, _bare = _authority_fixture(
        tmp_path, pred_pub.hex(), succ_pub.hex())
    key, pend = _write_keys(g, "aa", pred_priv, succ_priv, succ_pub, "push")
    pre = _git(repo, "rev-parse", "origin/season2/main").stdout.strip()
    r = rotate._finish_pending_swap_on_push(g, "aa", "push: OK")
    assert r.startswith("key swap completed"), r
    assert not pend.exists()
    assert json.loads(key.read_text())["priv_hex"] == succ_priv.hex()
    _git(repo, "fetch", "-q", "origin", "season2/main")
    assert _git(repo, "rev-parse",
                "origin/season2/main").stdout.strip() == pre, \
        "a push-deferred pending must attempt no authority publish"


def test_authority_deferred_signer_uses_the_verifiers_row(
        tmp_path, monkeypatch):
    """An authority-deferred signer consults the verifier's own cached row."""
    key, pred_priv, pred_pub = _mk_seat_key(tmp_path, "aa")
    succ_priv, succ_pub = bin_send.seatsig.get("ed25519").keygen()
    _pending(tmp_path, "aa", succ_priv.hex(), succ_pub.hex(),
             reason="authority")
    committed = [{"name": "aa", "role": "parent", "pubkey": succ_pub.hex(),
                  "sig_scheme": "ed25519"}]
    _patch_committed(monkeypatch, committed)
    pushed = []
    fetches = []

    def rows(root, ref, do_fetch):
        fetches.append(do_fetch)
        if do_fetch or pushed:
            return pushed, "ref", "ref"
        pushed[:] = [{"name": "aa"}]
        return pushed, "ref", "ref"

    monkeypatch.setattr(bin_send, "_pushed_seats", rows)
    ts, to, text = "2026-09-24T00:00:00+00:00", "bb", "body"
    sig_line = bin_send._sign_line(tmp_path, "aa", ts, to, text)
    meta = {"ts": ts, "from": "aa", "to": to,
            "sig": sig_line.removeprefix("sig: ")}
    assert fetches == [False], fetches
    assert bin_send._verify_block(tmp_path, bin_send._load_rows(tmp_path),
                                  meta, text) == \
        "VERIFIED aa (ed25519, main-committed)"

    pushed[:] = [{"name": "aa", "role": "parent", "pubkey": pred_pub,
                  "sig_scheme": "ed25519"}]
    sig_line = bin_send._sign_line(tmp_path, "aa", ts, to, text)
    meta["sig"] = sig_line.removeprefix("sig: ")
    assert bin_send._verify_block(tmp_path, bin_send._load_rows(tmp_path),
                                  meta, text) == "VERIFIED aa (ed25519)"


def test_deferred_window_dm_verifies_against_the_real_authority_ref(
        tmp_path, monkeypatch):
    """A deferred-window signature verifies from the real authority ref.

    The pushed row intentionally has no signing scheme; MAIN's committed
    successor row supplies it, and signing must not fetch while selecting the
    key to use.
    """
    sch = bin_send.seatsig.get("ed25519")
    pred_priv, pred_pub = sch.keygen()
    succ_priv, succ_pub = sch.keygen()
    repo, g, _posts, _bare = _authority_fixture(
        tmp_path, pred_pub.hex(), succ_pub.hex(), sig_scheme="ed25519")
    _write_keys(g, "aa", pred_priv, succ_priv, succ_pub, "authority")
    ts, to, text = "2026-09-24T00:00:00+00:00", "bb", "body"
    fetches = []
    real_run_git = bin_send._run_git

    def watched(root, args):
        if "fetch" in args:
            fetches.append(args)
        return real_run_git(root, args)

    monkeypatch.setattr(bin_send, "_run_git", watched)
    sig_line = bin_send._sign_line(repo, "aa", ts, to, text)
    assert sig_line is not None
    assert fetches == [], fetches
    meta = {"ts": ts, "from": "aa", "to": to,
            "sig": sig_line.removeprefix("sig: ")}
    rows = bin_send._load_rows(repo, do_fetch=False)
    assert bin_send._verify_block(repo, rows, meta, text) == \
        "VERIFIED aa (ed25519, main-committed)"


def test_send_signs_with_the_authority_key_when_deferred_on_authority(
        tmp_path, monkeypatch):
    """EF.84 conjunct B: an authority-deferred pending whose pub matches the
    COMMITTED LOCAL row is NOT preferred by the signer -- the authority never
    received the successor, so send signs with the live predecessor key. The
    shared auth comparison (`_caller_hold_key`) stays coherent and still
    accepts the holder."""
    sch = bin_send.seatsig.get("ed25519")
    succ_priv, succ_pub = sch.keygen()
    pred_priv, pred_pub = sch.keygen()
    key = bin_send._seat_key_path(tmp_path, "aa")
    key.parent.mkdir(parents=True, exist_ok=True)
    key.write_text(json.dumps({"scheme": "ed25519",
                               "priv_hex": pred_priv.hex()}))
    os.chmod(key, 0o600)
    pend = Path(str(key) + ".pending")
    pend.write_text(json.dumps({"scheme": "ed25519",
                                "priv_hex": succ_priv.hex(),
                                "pub_hex": succ_pub.hex(),
                                "deferred_for": "authority",
                                "gen_after": 2, "minted_at": ""}))
    os.chmod(pend, 0o600)
    row = {"name": "aa", "role": "parent", "pubkey": succ_pub.hex()}
    _patch_committed(monkeypatch, [row])
    # A pushed predecessor row, like the signed end-to-end fixture below,
    # must be selected over MAIN's unkeyed/committed successor row.
    monkeypatch.setattr(
        bin_send, "_pushed_seats",
        lambda root, ref, do_fetch: ([{"name": "aa", "role": "parent",
                                      "pubkey": pred_pub.hex(),
                                      "sig_scheme": "ed25519"}], "ref", "ref"))
    obj = bin_send._signing_key_obj(tmp_path, "aa", key)
    assert obj is not None
    assert obj["priv_hex"] == pred_priv.hex(), \
        "send must sign with the key the AUTHORITY row holds (the predecessor)"
    # the shared auth path stays coherent: the holder is accepted.
    who, _row, how = rotate._caller_hold_key(tmp_path, "aa", row, "env")
    assert who == "aa", how
