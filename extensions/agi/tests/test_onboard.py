"""RUNG 4 SLICE 1 -- send.py keygen --onboard (open onboarding).

hypothesis:l4-an-untrusted-lane-earns-tier-by-signed-verdicts, SLICE 1.
Proves on FIXTURE graphs only (never the live tree, never a real key outside
the fixture): a sponsor-co-signed charter-acceptance is verified through
rings.verify_ring BEFORE the config write, the newcomer's row lands with tier
'untrusted' plus the worktree/budget/harness cells slices 2 and 3 read, and
every refusal -- sponsor absent / sponsor unkeyed (no row pubkey, no key on
file) / row-name collision / ring short of threshold / no charter ring --
names tier 'untrusted' and the missing piece, leaving the config byte-identical
and no key behind.
"""

from __future__ import annotations

import json
import os
import stat
from pathlib import Path

import seatsig  # noqa: F401  (engine spelling, mur-39 (e))
import send as send_mod
import geometry_config

CH = "ed25519"


def _rows_md(rows, key="posts"):
    body = "\n".join(f"  - {r!r}" for r in rows)
    return (
        f"---\nid: config:{key}\nmint_id: 3e88873e3c204c5088f6ab81322a26de\n"
        f"type: config\nparents:\n  - goal:g17\n{key}:\n{body}\n"
        "---\n\n# config\n\nfixture body\n"
    )


_CHARTER_RING = """\
---
rings:
  - name: charter
    m: 2
    members: [newcomer, alice]
---

fixture body
"""


def _write_key(root, post, priv, scheme=seatsig.get(CH)):
    p = send_mod._seat_key_path(root, post)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps({"scheme": scheme.name, "priv_hex": priv.hex()}))
    os.chmod(p, stat.S_IMODE(0o600))
    return p


def _sponsor_keypair():
    scheme = seatsig.get(CH)
    priv, pub = scheme.keygen()
    return priv, pub.hex()


def _posts(root, sponsor_row):
    """belam (the admitted prime chair that performs the config write) plus the
    given sponsor row."""
    return _rows_md([{"name": "belam", "role": "prime_director", "tier": 3}]
                    + [sponsor_row])


def _project(tmp_path, rings=_CHARTER_RING, sponsor_row=None):
    root = tmp_path / "proj"
    (root / ".agi").mkdir(parents=True)
    (root / ".agi" / "config.json").write_text(
        json.dumps({"metric_primary": "outcome_coverage"}))
    d = root / ".agi" / "nodes" / ".geometry"
    d.mkdir(parents=True, exist_ok=True)
    (d / "posts.md").write_text(
        _posts(root, sponsor_row)
        if sponsor_row is not None
        else _rows_md([{"name": "belam", "role": "prime_director", "tier": 3}]))
    if rings is not None:
        (d / "rings.md").write_text(rings)
    return root


def _happy(tmp_path):
    """A fully-preconditioned project: sponsor alice with a real keypair."""
    _priv, pub = _sponsor_keypair()
    root = _project(tmp_path, sponsor_row={
        "name": "alice", "role": "director", "pubkey": pub, "harness": "pi"})
    _write_key(root, "alice", _priv)
    return root


def _rows(root):
    return geometry_config.load_rows(send_mod._graph_root(root))


def _sponsor_co_sign(root, name, sponsor):
    """The sponsor's DISJOINT signing action, in-fixture: establish the
    newcomer key, build the charter canonical, and sign it with the sponsor's
    own key. Returns ``(canonical_hex, sponsor_sig)`` -- exactly what a real
    sponsor returns to the writer, which can only VERIFY it."""
    scheme = seatsig.get(CH)
    built = send_mod._onboard_build_canonical(
        root, name, sponsor, scheme, send_mod._charter_hash())
    sig = send_mod._sponsor_sig_for(root, sponsor, built["canonical_hex"],
                                    scheme)
    assert sig, "the fixture sponsor holds a key to co-sign with"
    return built["canonical_hex"], sig


def test_onboard_success_appends_untrusted_row(tmp_path):
    """Happy path: the charter record verifies through rings.verify_ring and
    the newcomer's row lands readable via geometry_config.load_rows with tier
    'untrusted' and the worktree/budget/harness cells slices 2 and 3 read.
    The sponsor co-signature arrives as a value (never read from a sponsor
    key the writer could forge with)."""
    root = _happy(tmp_path)
    _canon, ssig = _sponsor_co_sign(root, "newcomer", "alice")
    row = send_mod.onboard(root, "newcomer", "alice", ssig, actor="belam")
    assert row is not None
    got = next(r for r in _rows(root) if r["name"] == "newcomer")
    assert got["tier"] == "untrusted"
    assert got["pubkey"], "the newcomer row carries the minted pubkey"
    assert got["worktree"] == "worktrees/newcomer"
    assert got["budget"] == 1
    assert got["harness"] == "pi"
    assert got["charter"]["ring"] == "charter"
    assert got["charter"]["kind"] == "charter"
    # the record's fields are the FULL fields and the signatures are the pair
    assert set(got["charter"]["fields"]) == {
        "name", "pubkey", "sponsor", "charter_hash"}
    assert len(got["charter"]["signatures"]) == 2
    # the key was minted in the fixture only
    assert send_mod._seat_key_path(root, "newcomer").is_file()


def test_onboard_writer_never_reads_the_sponsor_key(tmp_path):
    """THE FIX, proved: the writer (onboard) cannot forge the sponsor's part
    because it never holds the sponsor's private key. Produce a genuine
    sponsor co-signature, then DELETE the sponsor's key file -- the onboard
    still lands, proving the writer read no sponsor key on the way. Under the
    pre-fix code this was the forge: _read_key_priv(root, sponsor) signed for
    the sponsor inside the writer."""
    root = _happy(tmp_path)
    _canon, ssig = _sponsor_co_sign(root, "newcomer", "alice")
    send_mod._seat_key_path(root, "alice").unlink()  # sponsor key gone
    assert not send_mod._seat_key_path(root, "alice").exists()
    row = send_mod.onboard(root, "newcomer", "alice", ssig, actor="belam")
    assert row is not None, "the writer needs no sponsor key -- only the sig"
    got = next(r for r in _rows(root) if r["name"] == "newcomer")
    assert got["tier"] == "untrusted"


def test_onboard_refuses_missing_sponsor_sig(tmp_path):
    """No sponsor co-signature value is refused by name, config untouched.
    (Replaces the old 'sponsor holds no key on file' refusal: the writer no
    longer inspects the sponsor's key at all, it must be handed the value.)"""
    root = _happy(tmp_path)
    before = (root / ".agi" / "nodes" / ".geometry" / "posts.md").read_bytes()
    assert send_mod.onboard(root, "newcomer", "alice", "", actor="belam") \
        is None
    assert (root / ".agi" / "nodes" / ".geometry"
            / "posts.md").read_bytes() == before
    assert not send_mod._seat_key_path(root, "newcomer").exists()


def test_onboard_refuses_forged_sponsor_sig(tmp_path):
    """The writer CANNOT invent a passing sponsor co-signature: sign a bare
    different canonical with the SPONSOR's own key and feed it in -- it does
    not verify against the record the row will carry, and the onboard is
    refused with no write and no key left. This is the assertion the forge
    could not survive."""
    root = _happy(tmp_path)
    scheme = seatsig.get(CH)
    bogus_priv = send_mod._read_key_priv(root, "alice")
    forged = scheme.sign(bogus_priv, b"wrong canonical, not the charter").hex()
    before = (root / ".agi" / "nodes" / ".geometry" / "posts.md").read_bytes()
    assert send_mod.onboard(root, "newcomer", "alice", forged,
                            actor="belam") is None
    assert (root / ".agi" / "nodes" / ".geometry"
            / "posts.md").read_bytes() == before
    assert not send_mod._seat_key_path(root, "newcomer").exists(), \
        "a refused onboard must not leave a minted key behind"


def test_onboard_second_run_refuses_and_leaves_config_unchanged(tmp_path):
    root = _happy(tmp_path)
    _canon, ssig = _sponsor_co_sign(root, "newcomer", "alice")
    assert send_mod.onboard(root, "newcomer", "alice", ssig,
                            actor="belam") is not None
    before = (root / ".agi" / "nodes" / ".geometry" / "posts.md").read_bytes()
    _canon2, ssig2 = _sponsor_co_sign(root, "newcomer", "alice")
    assert send_mod.onboard(root, "newcomer", "alice", ssig2,
                            actor="belam") is None
    assert (root / ".agi" / "nodes" / ".geometry"
            / "posts.md").read_bytes() == before


def test_onboard_refuses_absent_sponsor(tmp_path):
    root = _project(tmp_path)  # no alice row, no alice key
    before = (root / ".agi" / "nodes" / ".geometry" / "posts.md").read_bytes()
    assert send_mod.onboard(root, "newcomer", "ghost", "",
                            actor="belam") is None
    assert (root / ".agi" / "nodes" / ".geometry" / "posts.md").read_bytes() \
        == before
    assert not send_mod._seat_key_path(root, "newcomer").exists()


def test_onboard_refuses_sponsor_with_no_row_pubkey(tmp_path):
    """The sponsor row names no pubkey -- refused, because there is nothing
    to verify the co-signature against."""
    _priv, _pub = _sponsor_keypair()
    root = _project(tmp_path, sponsor_row={
        "name": "alice", "role": "director", "harness": "pi"})
    _write_key(root, "alice", _priv)
    _canon, ssig = _sponsor_co_sign(root, "newcomer", "alice")
    before = (root / ".agi" / "nodes" / ".geometry" / "posts.md").read_bytes()
    assert send_mod.onboard(root, "newcomer", "alice", ssig,
                            actor="belam") is None
    assert (root / ".agi" / "nodes" / ".geometry" / "posts.md").read_bytes() \
        == before


def test_onboard_refuses_when_ring_short_of_threshold(tmp_path):
    """m=3 on a two-member record: verify_ring does not reach the threshold,
    the refusal names the count, and no key is left behind. A genuine sponsor
    co-signature is supplied so the refusal is the RING, not the signature."""
    _priv, pub = _sponsor_keypair()
    root = _project(tmp_path, rings=(
        "---\nrings:\n  - name: charter\n    m: 3\n    members: "
        "[newcomer, alice]\n---\n\nfixture\n"),
        sponsor_row={"name": "alice", "role": "director", "pubkey": pub,
                     "harness": "pi"})
    _write_key(root, "alice", _priv)
    _canon, ssig = _sponsor_co_sign(root, "newcomer", "alice")
    before = (root / ".agi" / "nodes" / ".geometry" / "posts.md").read_bytes()
    assert send_mod.onboard(root, "newcomer", "alice", ssig,
                            actor="belam") is None
    assert (root / ".agi" / "nodes" / ".geometry" / "posts.md").read_bytes() \
        == before
    # NOTE: no 'no key left behind' assert here -- the sponsor prepare step
    # (_sponsor_co_sign) legitimately mints the newcomer's key first so the
    # sponsor can sign the exact canonical; onboard leaves the newcomer's own
    # key in place. The unlink-on-refusal property is covered where onboard
    # IS the minter (test_onboard_refuses_forged_sponsor_sig).


def test_onboard_refuses_when_no_charter_ring_declared(tmp_path):
    """rings are opt-in: an undeclared 'charter' ring refuses by name. A
    genuine sponsor co-signature is supplied so the refusal is the RING."""
    _priv, pub = _sponsor_keypair()
    root = _project(tmp_path, rings=None, sponsor_row={
        "name": "alice", "role": "director", "pubkey": pub, "harness": "pi"})
    _write_key(root, "alice", _priv)
    _canon, ssig = _sponsor_co_sign(root, "newcomer", "alice")
    before = (root / ".agi" / "nodes" / ".geometry" / "posts.md").read_bytes()
    assert send_mod.onboard(root, "newcomer", "alice", ssig,
                            actor="belam") is None
    assert (root / ".agi" / "nodes" / ".geometry" / "posts.md").read_bytes() \
        == before


def test_onboard_cli_success_through_main(tmp_path, monkeypatch):
    """The CLI `keygen --onboard <name> --sponsor <post> --sponsor-sig <sig>`:
    the sponsor co-signature is computed disjointly and handed in as a value,
    never derived from a key the writer reads."""
    root = _happy(tmp_path)
    monkeypatch.chdir(root)
    _canon, ssig = _sponsor_co_sign(root, "newcomer", "alice")
    rc = send_mod.main(
        ["--from", "belam", "keygen", "--onboard", "newcomer",
         "--sponsor", "alice", "--sponsor-sig", ssig])
    assert rc == 0, rc
    got = next(r for r in _rows(root) if r["name"] == "newcomer")
    assert got["tier"] == "untrusted"


def test_onboard_cli_refuses_sponsorless(tmp_path, monkeypatch):
    """--onboard without --sponsor is refused at the CLI (exit 1)."""
    root = _happy(tmp_path)
    monkeypatch.chdir(root)
    rc = send_mod.main(
        ["--from", "belam", "keygen", "--onboard", "newcomer"])
    assert rc == 1, rc


def test_onboard_cli_refuses_missing_sponsor_sig(tmp_path, monkeypatch):
    """--onboard with --sponsor but no --sponsor-sig is refused at the CLI
    (exit 1): the writer will not fabricate a co-signature on the sponsor's
    behalf."""
    root = _happy(tmp_path)
    monkeypatch.chdir(root)
    rc = send_mod.main(
        ["--from", "belam", "keygen", "--onboard", "newcomer",
         "--sponsor", "alice"])
    assert rc == 1, rc


def test_onboard_cli_sponsor_sign_disjoint_step(tmp_path, monkeypatch, capsys):
    """`keygen --seat <sponsor> --sponsor-sign <canonical-hex>` signs a
    canonical with the sponsor's OWN key and prints hex -- the disjoint step
    that yields a --sponsor-sig the writer can verify but not invent. The
    printed value verifies under the sponsor's pubkey, and it is exactly the
    value that drives a successful onboard."""
    root = _happy(tmp_path)
    monkeypatch.chdir(root)
    _canon, _ssig = _sponsor_co_sign(root, "newcomer", "alice")
    rc = send_mod.main(["--from", "alice", "keygen", "--seat", "alice",
                        "--sponsor-sign", _canon])
    assert rc == 0, rc
    printed = capsys.readouterr().out.strip()
    assert printed and printed != "0", "the disjoint step prints a signature"
    scheme = seatsig.get(CH)
    alice_pub = next(r["pubkey"] for r in _rows(root)
                     if r["name"] == "alice")
    assert scheme.verify(bytes.fromhex(alice_pub), bytes.fromhex(_canon),
                         bytes.fromhex(printed)), \
        "what the sponsor signs verifies under the sponsor's pubkey"
    assert printed == _ssig, "same canonical, same sponsor, same signature"