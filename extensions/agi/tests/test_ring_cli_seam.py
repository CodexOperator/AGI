"""kid D: the CLI quorum path is SIGNABLE (freshness seam) + dry-run no-burn.

Fixes the measured defect (hypothesis:l4-canonical-bytes-are-injective-and-
fresh-and-the-ring-gates-the-write-itself) that `--ring-gate` / `--suite-ring`
/write-ring runs could NEVER be admitted at m>0: every gate minted a fresh
nonce per call, so the FIXED `--ring-sig` values a caller passes never matched
the canonical bytes the gate built. Kids A/B/C proved the bytes and the ring
assemble; this kid D adds the SEAM that makes them usable out-of-process:

  1. `--ring-fresh "<ts>|<nonce>"` on dispatch.py / verification.py / write.py
     pins the EXACT `_fresh` the gate builds, so a signer computes the SAME
     canonical bytes.
  2. `--ring-fields` on each prints the exact fields + canonical bytes the
     gate will verify for that argv (+ --ring-fresh), then exits 0 -- the
     signer's view (acceptance D: parse the canonical hex, sign it, admit).
  3. `--dry-run` never burns a nonce: an admitted dry run READS the ledger (a
     replayed nonce still REFUSES) but does not write it (no ring-nonces.json).

Acceptance A-F. Signing is the SAME seatsig fixture scheme test_rings.py /
test_write_ring_cli.py register (name `fixture`, hash-16), the members'
pubkeys resolve from a fixture posts.md -- never a real key, never live
geometry, always a tmp project root (the worktree must not gain a
`nodes/.geometry/ring-nonces.json`).
"""
from __future__ import annotations

import datetime
import hashlib
import sys
import time
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import dispatch  # noqa: E402
import verification  # noqa: E402
import write  # noqa: E402
import seatsig  # noqa: E402
from seatsig import get, register, Scheme  # noqa: E402
from seatsig import rings  # noqa: E402
import seatsig.rings as _rings  # noqa: E402


class _DummyScheme(Scheme):
    """Same fixture scheme test_rings.py / test_write_ring_cli.py register
    (name `fixture`, sha256-16). The ring routes through seatsig.get() exactly
    like ed25519 would -- the coupling is the REGISTRY, not the algorithm."""

    name = "fixture"

    def keygen(self, **kw):
        sk = b"k" * 32
        return sk, b"pub" + sk

    def sign(self, priv, msg):
        return hashlib.sha256(msg + priv).digest()[:16]

    def verify(self, pub, msg, sig):
        return sig == hashlib.sha256(msg + pub).digest()[:16]


register(_DummyScheme())


def _now() -> str:
    return (datetime.datetime.fromtimestamp(time.time(), datetime.timezone.utc)
            .strftime("%Y-%m-%dT%H:%M:%SZ"))


def _sigs(canonical, posts):
    """m fixture-signatures (post:fixture:<hex>) over ``canonical`` for the
    given members. All members key to the SAME priv b'k'*32 (symmetric hash
    scheme), so the posts.md pubkeys are all the hex of that priv."""
    scheme = get("fixture")
    return [f"{m}:fixture:{scheme.sign(b'k' * 32, canonical).hex()}"
            for m in posts]


def _fresh(nonce="cli-seam"):
    """A fresh '<ts>|<nonce>' with a RECENT ts (within the 900s window)."""
    return f"{_now()}|{nonce}"


def _ring_root(tmp_path):
    """A fixture graph root usable by ALL THREE surfaces: a `config` schema
    declaring `ring: approval` (write path), a rings geometry cell naming the
    ring (dispatch + verification), and posts.md carrying the members' pubkeys
    (what every gate's pubkey resolver reads). Returns the graph root dir."""
    agi = tmp_path / ".agi"
    agi.mkdir(parents=True)
    (agi / "config.json").write_text("{}", encoding="utf-8")
    (agi / "context" / "schemas").mkdir(parents=True)
    (agi / "context" / "schemas" / "[config].md").write_text(
        "---\ntype: config\nwritten_by: prime\nring: approval\n---\n",
        encoding="utf-8")
    (agi / "nodes" / ".geometry").mkdir(parents=True)
    (agi / "nodes" / ".geometry" / "rings.md").write_text(
        "---\ntype: cell\nrings:\n"
        "  - name: approval\n    m: 2\n    members: [alice, bob, carol]\n"
        "---\n", encoding="utf-8")
    (agi / "nodes" / ".geometry" / "posts.md").write_text(
        "---\ntype: config\nposts:\n"
        "  - name: alice\n    pubkey: " + ("6b" * 32) + "\n"
        "  - name: bob\n    pubkey: " + ("6b" * 32) + "\n"
        "  - name: carol\n    pubkey: " + ("6b" * 32) + "\n"
        "---\n", encoding="utf-8")
    # A real config node the write path mutates.
    (agi / "nodes").mkdir(parents=True, exist_ok=True)
    (agi / "nodes" / "posts.md").write_text(
        "---\nid: config:posts\ntype: config\nmint_id: cfgtst001\n"
        "title: posts\n---\n\nbody\n", encoding="utf-8")
    return agi


def _ledger(root):
    return root / "nodes" / ".geometry" / "ring-nonces.json"


def _canonical_hex(out):
    """Parse the machine line of a `--ring-fields` report back to bytes."""
    for line in out.splitlines():
        if line.startswith("ring-canonical-hex:"):
            return bytes.fromhex(line.split(": ", 1)[1].strip())
    raise AssertionError(f"no ring-canonical-hex in output: {out!r}")


class _Ctx:
    def __init__(self):
        self.out = StringIO()
        self.err = StringIO()


def _run(fn, argv):
    """Run one entry main() on a patched sys.argv, capturing stdout/stderr and
    the exit code (int or the SystemExit code)."""
    sys.argv = [fn] + list(argv)
    ctx = _Ctx()
    with redirect_stdout(ctx.out), redirect_stderr(ctx.err):
        try:
            rc = {"dispatch": dispatch.main,
                  "verification": verification.main,
                  "write": write.main}[fn]()
        except SystemExit as exc:
            rc = exc.code if exc.code is not None else 0
    return rc, ctx.out.getvalue(), ctx.err.getvalue()


# ---------------------------------------------------------------------------
# DISPATCH --ring-gate / --ring-fresh / --ring-fields / --dry-run
# ---------------------------------------------------------------------------

def test_D_dispatch_ring_fields_prints_the_verified_bytes(tmp_path):
    """A/D: `--ring-fields --ring-fresh T|N` prints the exact round-cut
    canonical bytes the gate verifies; the test parses them, signs over them
    and the corresponding `--ring-gate` dry-run is ADMITTED. Also: the printed
    canonical equals canonical_bytes() over the printed fields dict (the
    printed thing IS the verified thing)."""
    root = _ring_root(tmp_path)
    fresh = _fresh()
    argv = [str(tmp_path), "1", "--ring-gate", "approval", "--ring-fresh",
            fresh, "--ring-fields", "--tier", "kid", "--target", "x"]
    rc, out, err = _run("dispatch", argv)
    assert rc == 0
    canon = _canonical_hex(out)
    # cross-check: recompute canonical from the printed fields JSON
    import json
    fj = next(l for l in out.splitlines() if l.startswith("ring-fields.json:"))
    fields = json.loads(fj.split(": ", 1)[1])
    assert rings.canonical_bytes("round-cut", fields) == canon
    # dry-run with the signature over the PRINTED bytes -> admitted, no ledger
    sigs = _sigs(canon, ["alice", "bob"])
    rc, out, err = _run("dispatch", [
        str(tmp_path), "1", "--dry-run", "--ring-gate", "approval",
        "--ring-fresh", fresh, "--ring-sig", sigs[0], "--ring-sig", sigs[1],
        "--tier", "kid", "--target", "x"])
    assert rc == 0, err
    assert not _ledger(root).exists()


def test_A_dispatch_changed_target_refused(tmp_path):
    """A (refused arm): change --target one byte and keep the same signature
    -> the round is REFUSED on the quorum (the signed bytes cover the target)."""
    root = _ring_root(tmp_path)
    fresh = _fresh()
    rc, out, _ = _run("dispatch", [
        str(tmp_path), "1", "--ring-gate", "approval", "--ring-fresh", fresh,
        "--ring-fields", "--tier", "kid", "--target", "x"])
    canon = _canonical_hex(out)
    sigs = _sigs(canon, ["alice", "bob"])
    rc, out, err = _run("dispatch", [
        str(tmp_path), "1", "--dry-run", "--ring-gate", "approval",
        "--ring-fresh", fresh, "--ring-sig", sigs[0], "--ring-sig", sigs[1],
        "--tier", "kid", "--target", "y"])  # ONE byte different
    assert rc == 3
    assert "round-ring" in err


def test_C_dispatch_dry_run_twice_no_ledger_then_real_replay_unit(tmp_path):
    """C: `--dry-run` twice with the same T|N -- BOTH admitted, no ledger file.
    The REAL (non-dry-run) recording -- which a fresh spawn would take -- is
    the gate function's remember=True path: first real run admits + records,
    a second real run with the same T|N refuses REUSED as a replayed nonce."""
    root = _ring_root(tmp_path)
    fresh = _fresh()
    rc, out, _ = _run("dispatch", [
        str(tmp_path), "1", "--ring-gate", "approval", "--ring-fresh", fresh,
        "--ring-fields", "--tier", "kid", "--target", "x"])
    canon = _canonical_hex(out)
    sigs = _sigs(canon, ["alice", "bob"])
    for _ in range(2):
        rc, _, err = _run("dispatch", [
            str(tmp_path), "1", "--dry-run", "--ring-gate", "approval",
            "--ring-fresh", fresh, "--ring-sig", sigs[0], "--ring-sig", sigs[1],
            "--tier", "kid", "--target", "x"])
        assert rc == 0, err
        assert not _ledger(root).exists(), err
    # REAL run semantics -- the gate with remember=True (spawn not taken here;
    # the CLI passes remember=not dry_run, so a real run records).
    ts, nonce = fresh.split("|", 1)
    fields = _rings.fresh_fields(
        {"tier": "kid", "role": "", "target": "x", "level": "small",
         "iter_n": "1"}, ts=ts, nonce=nonce)
    from seatsig import rings as _r2
    c = _r2.canonical_bytes("round-cut", fields)
    sigs2 = _sigs(c, ["alice", "bob"])
    r1 = _round_gate(root, "approval", sigs2, target="x", level="small",
                      iter_n=1, fields=fields)
    assert r1 is None                      # real run #1 admitted
    assert _ledger(root).exists()          # and it recorded (burned) the nonce
    r2 = _round_gate(root, "approval", sigs2, target="x", level="small",
                      iter_n=1, fields=fields)
    assert r2 is not None                  # real run #2 refused
    assert "replayed nonce" in r2


def _round_gate(root, ring_name, sigs, **kw):
    """Call _round_ring_refusal the way dispatch.main does for a REAL run
    (remember=True) -- the exact gate code, without spawning an agent."""
    return dispatch._round_ring_refusal(
        str(root), ring_name, "kid", None, sigs,
        target=kw.get("target"), level=kw.get("level"),
        iter_n=kw.get("iter_n", 1), fields=kw.get("fields"))


def test_F_dispatch_seam_vs_mint_fresh(tmp_path):
    """F: `--ring-fresh` pins the SAME _fresh across runs; absent --ring-fresh
    MINTS a fresh nonce each time (existing behaviour preserved)."""
    root = _ring_root(tmp_path)
    fresh = _fresh()
    rc1, out1, _ = _run("dispatch", [
        str(tmp_path), "1", "--ring-fields", "--ring-fresh", fresh,
        "--tier", "kid", "--target", "x"])
    rc2, out2, _ = _run("dispatch", [
        str(tmp_path), "1", "--ring-fields", "--ring-fresh", fresh,
        "--tier", "kid", "--target", "x"])
    assert out1 == out2                    # pinned -> identical bytes
    rc3, out3, _ = _run("dispatch", [
        str(tmp_path), "1", "--ring-fields", "--tier", "kid", "--target", "x"])
    rc4, out4, _ = _run("dispatch", [
        str(tmp_path), "1", "--ring-fields", "--tier", "kid", "--target", "x"])
    assert rc3 == rc4 == 0
    import json
    f3 = json.loads(next(l for l in out3.splitlines()
                         if l.startswith("ring-fields.json:")).split(": ", 1)[1])
    f4 = json.loads(next(l for l in out4.splitlines()
                         if l.startswith("ring-fields.json:")).split(": ", 1)[1])
    assert "|" in f3["_fresh"] and f3["_fresh"] != f4["_fresh"]  # minted


# ---------------------------------------------------------------------------
# VERIFICATION --suite-ring
# ---------------------------------------------------------------------------

def test_D_verification_ring_fields_print_sign_admit(tmp_path, monkeypatch):
    """D/E: verification.py `--ring-fields --ring-fresh T|N` prints the exact
    suite-grant canonical; signing over exactly it admits the `--suite-ring`
    run -- proving the printed thing is the verified thing."""
    root = _ring_root(tmp_path)
    fresh = _fresh()
    argv = ["--root", str(tmp_path), "--suite", "--suite-ring", "approval",
            "--ring-fresh", fresh, "--ring-fields"]
    rc, out, _ = _run("verification", argv)
    assert rc == 0
    canon = _canonical_hex(out)
    sigs = _sigs(canon, ["alice", "bob"])
    _stub_run_level(monkeypatch)
    rc, out, err = _run("verification", [
        "--root", str(tmp_path), "--suite", "--suite-ring", "approval",
        "--ring-fresh", fresh, "--ring-sig", sigs[0], "--ring-sig", sigs[1]])
    assert rc == 0, out + err
    assert _ledger(root).exists()


def test_B_verification_replay_refused(tmp_path, monkeypatch):
    """B/E: the same T|N a SECOND time on a real --suite-ring run is REFUSED
    as a replayed nonce, naming the nonce."""
    root = _ring_root(tmp_path)
    fresh = _fresh()
    rc, out, _ = _run("verification", [
        "--root", str(tmp_path), "--suite", "--suite-ring", "approval",
        "--ring-fresh", fresh, "--ring-fields"])
    canon = _canonical_hex(out)
    sigs = _sigs(canon, ["alice", "bob"])
    _stub_run_level(monkeypatch)
    rc, _, err = _run("verification", [
        "--root", str(tmp_path), "--suite", "--suite-ring", "approval",
        "--ring-fresh", fresh, "--ring-sig", sigs[0], "--ring-sig", sigs[1]])
    assert rc == 0
    rc2, out2, err2 = _run("verification", [
        "--root", str(tmp_path), "--suite", "--suite-ring", "approval",
        "--ring-fresh", fresh, "--ring-sig", sigs[0], "--ring-sig", sigs[1]])
    assert rc2 == 1
    assert "replayed nonce" in (out2 + err2)
    assert fresh.split("|", 1)[1] in (out2 + err2)


def test_A_verification_wrong_ring_fresh_mismatch(tmp_path):
    """A/E: a signature for one T|N does NOT admit the same --suite-ring run
    with a DIFFERENT --ring-fresh (bytes differ -> quorum fails)."""
    root = _ring_root(tmp_path)
    fresh1 = _fresh("n1")
    rc, out, _ = _run("verification", [
        "--root", str(tmp_path), "--suite", "--suite-ring", "approval",
        "--ring-fresh", fresh1, "--ring-fields"])
    canon = _canonical_hex(out)
    sigs = _sigs(canon, ["alice", "bob"])
    fresh2 = _fresh("n2")
    rc, out, err = _run("verification", [
        "--root", str(tmp_path), "--suite", "--suite-ring", "approval",
        "--ring-fresh", fresh2, "--ring-sig", sigs[0], "--ring-sig", sigs[1]])
    assert rc == 1
    assert "suite-ring" in (out + err)


def _stub_run_level(monkeypatch):
    """Only the pytest SPAWN under test is stubbed (run_level would launch a
    real pytest subprocess); the ring gate and freshness seam run for real."""
    monkeypatch.setattr(verification, "run_level", lambda *a, **k: [])


# ---------------------------------------------------------------------------
# WRITE path --ring-gate semantics / --ring-fresh / --ring-fields / --dry-run
# ---------------------------------------------------------------------------

def test_D_write_ring_fields_print_sign_admit(tmp_path):
    """D/E: write.py `--ring-fields --ring-fresh T|N` prints the exact
    config-write canonical; the test parses it, signs, and the corresponding
    `set` run is ADMITTED (written) and the nonce recorded."""
    root = _ring_root(tmp_path)
    fresh = _fresh()
    rc, out, _ = _run("write", [
        "config:posts", 'set posts [{"name": "x"}]', "--ring-fields",
        "--ring-fresh", fresh, "--root", str(tmp_path)])
    assert rc == 0, out
    canon = _canonical_hex(out)
    sigs = _sigs(canon, ["alice", "bob"])
    rc, out, err = _run("write", [
        "config:posts", 'set posts [{"name": "x"}]', "--ring-fresh", fresh,
        "--ring-sig", sigs[0], "--ring-sig", sigs[1],
        "--actor", "director1", "--role", "prime", "--root", str(tmp_path)])
    assert rc == 0, out + err
    assert "updated" in out
    assert _ledger(root).exists()


def test_B_write_replay_refused(tmp_path):
    """B/E: the same T|N a SECOND real write is REFUSED in the write gate as
    a replayed nonce, naming the nonce; nothing further persists."""
    root = _ring_root(tmp_path)
    fresh = _fresh()
    rc, out, _ = _run("write", [
        "config:posts", 'set posts [{"name": "x"}]', "--ring-fields",
        "--ring-fresh", fresh, "--root", str(tmp_path)])
    canon = _canonical_hex(out)
    sigs = _sigs(canon, ["alice", "bob"])
    args = ["config:posts", 'set posts [{"name": "x"}]', "--ring-fresh", fresh,
            "--ring-sig", sigs[0], "--ring-sig", sigs[1],
            "--actor", "director1", "--role", "prime", "--root", str(tmp_path)]
    rc, _, _ = _run("write", args)
    assert rc == 0
    rc2, out2, err2 = _run("write", args)
    assert rc2 == 2
    assert "replayed nonce" in (out2 + err2)
    assert fresh.split("|", 1)[1] in (out2 + err2)


def test_A_write_changed_field_refused(tmp_path):
    """A/E: change the set value (one byte) and keep the same signature ->
    the write is REFUSED on the quorum (the signed bytes cover the value)."""
    root = _ring_root(tmp_path)
    fresh = _fresh()
    rc, out, _ = _run("write", [
        "config:posts", 'set posts [{"name": "x"}]', "--ring-fields",
        "--ring-fresh", fresh, "--root", str(tmp_path)])
    canon = _canonical_hex(out)
    sigs = _sigs(canon, ["alice", "bob"])
    rc, out, err = _run("write", [
        "config:posts", 'set posts [{"name": "y"}]', "--ring-fresh", fresh,
        "--ring-sig", sigs[0], "--ring-sig", sigs[1],
        "--actor", "director1", "--role", "prime", "--root", str(tmp_path)])
    assert rc == 2
    assert "rung 2 multisig ring" in (out + err)


def test_C_write_dry_run_no_ledger(tmp_path):
    """C/E: write `--dry-run` with a valid quorum returns before the write
    gate -- no ledger file appears. A following real run then ADMITS (the
    nonce was never burned by the dry run)."""
    root = _ring_root(tmp_path)
    fresh = _fresh()
    rc, out, _ = _run("write", [
        "config:posts", 'set posts [{"name": "x"}]', "--ring-fields",
        "--ring-fresh", fresh, "--root", str(tmp_path)])
    canon = _canonical_hex(out)
    sigs = _sigs(canon, ["alice", "bob"])
    rc, _, err = _run("write", [
        "config:posts", 'set posts [{"name": "x"}]', "--dry-run",
        "--ring-fresh", fresh, "--ring-sig", sigs[0], "--ring-sig", sigs[1],
        "--actor", "director1", "--role", "prime", "--root", str(tmp_path)])
    assert rc == 0
    assert not _ledger(root).exists()
    # real run with the same T|N -> still fresh (dry run never burned it)
    rc, out, err = _run("write", [
        "config:posts", 'set posts [{"name": "x"}]', "--ring-fresh", fresh,
        "--ring-sig", sigs[0], "--ring-sig", sigs[1],
        "--actor", "director1", "--role", "prime", "--root", str(tmp_path)])
    assert rc == 0, (out + err)
    assert "updated" in out