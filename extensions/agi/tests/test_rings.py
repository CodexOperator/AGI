"""Tests for seatsig.rings -- multisig m-of-n ring verification (rung 2).

Covers on FIXTURE keys: m-of-n satisfied / one short / one forged (rung-1
FORGED label) / a member OUTSIDE the ring / rings opt-in (no ring named -->
nothing changes) / unknown scheme / unkeyed member. Everything verifies
through the seatsig Scheme interface (never its own crypto), and a record
short of m is REFUSED by name with the m-of-n count.
"""

from __future__ import annotations

import json
import time
import pytest

import seatsig  # noqa: F401  (guarantees the engine spelling, mur-39 (e))
from seatsig import register, Scheme, get
from seatsig import rings


class _DummyScheme(Scheme):
    """Fixture scheme: sign = sha256(msg + priv) truncated to 16 bytes,
    verify recomputes. Cheap fixture keys, no real crypto in a test. The
    ring still routes through seatsig.get() exactly like ed25519 would --
    the coupling is the REGISTRY, not the algorithm (the mur-39 rule)."""

    name = "fixture"

    def keygen(self):
        import os

        priv = os.urandom(8)
        return priv, priv

    def sign(self, priv, msg):
        import hashlib

        return hashlib.sha256(msg + priv).digest()[:16]

    def verify(self, pub, msg, sig):
        import hashlib

        return sig == hashlib.sha256(msg + pub).digest()[:16]


@pytest.fixture(scope="module")
def _scheme():
    register(_DummyScheme())
    return get("fixture")


# Register the fixture scheme at import time so the module-scoped
# ``fixture_ring`` (which sign/verify against it) sees it regardless of
# fixture ordering.
register(_DummyScheme())


@pytest.fixture(scope="module")
def fixture_ring():
    """A 3-member ring, threshold 2, with the members' pubkeys resolved by a
    fixture mapping (the posts-rows resolver is the real-tree default; the
    gate supplies this mapping for a fixture)."""
    scheme = get("fixture")
    keys = {m: scheme.keygen() for m in ("alice", "bob", "carol")}
    ring = {"name": "approval", "m": 2,
            "members": ["alice", "bob", "carol"]}
    pubkeys = {m: priv.hex() for m, (priv, _pub) in keys.items()}
    signers = {m: priv for m, (priv, _pub) in keys.items()}
    canonical = rings.canonical_bytes("merge-grant", {"ref": "s2/main"})
    return locals()


def _sig(signers, post, canonical):
    scheme = get("fixture")
    return f"{post}:fixture:{scheme.sign(signers[post], canonical).hex()}"


def test_ring_satisfied(fixture_ring):
    """m-of-n: 2 valid signatures from distinct members >= m=2 -> ok True."""
    s = fixture_ring["signers"]
    c = fixture_ring["canonical"]
    sigs = [_sig(s, "alice", c), _sig(s, "bob", c)]
    res = rings.verify_ring(fixture_ring["ring"], c, sigs,
                            pubkey_for_post=fixture_ring["pubkeys"].get)
    assert res.ok is True
    assert res.n_valid == 2
    assert res.labels["alice"] == "VERIFIED"
    assert res.labels["bob"] == "VERIFIED"


def test_ring_one_short(fixture_ring):
    """m-of-n: 1 valid signature when m=2 -> REFUSED by name with the count."""
    s = fixture_ring["signers"]
    c = fixture_ring["canonical"]
    sigs = [_sig(s, "alice", c)]
    res = rings.verify_ring(fixture_ring["ring"], c, sigs,
                            pubkey_for_post=fixture_ring["pubkeys"].get)
    assert res.ok is False
    assert res.n_valid == 1
    assert "got 1" in res.refused
    assert "2" in res.refused
    assert "approval" in res.refused


def test_ring_one_forged(fixture_ring):
    """m-of-n: a member's sig that does NOT verify is FORGED (rung-1 label)
    and does not count toward m."""
    s = fixture_ring["signers"]
    c = fixture_ring["canonical"]
    forged = _sig(s, "bob", c)[:-2] + "00"  # flip the last sig byte
    sigs = [_sig(s, "alice", c), forged]
    res = rings.verify_ring(fixture_ring["ring"], c, sigs,
                            pubkey_for_post=fixture_ring["pubkeys"].get)
    assert res.ok is False
    assert res.labels["alice"] == "VERIFIED"
    assert res.labels["bob"] == "FORGED"
    assert res.n_valid == 1
    assert "FORGED" in res.refused


def test_ring_outsider(fixture_ring):
    """A signature from a post that is NOT a ring member is OUTSIDE and is
    never counted toward m."""
    s = fixture_ring["signers"]
    c = fixture_ring["canonical"]
    # mallory is OUTSIDE the ring; a forged post label with ANY key is still
    # OUTSIDE -- the ring membership is judged first, before any verify.
    sigs = [_sig(s, "alice", c), _sig(s, "bob", c),
            f"mallory:fixture:{_sig(s, 'alice', c).rsplit(':', 1)[1]}"]
    res = rings.verify_ring(fixture_ring["ring"], c, sigs,
                            pubkey_for_post=fixture_ring["pubkeys"].get)
    assert res.ok is True  # alice+bob still satisfy m=2
    assert res.labels["mallory"] == "OUTSIDE"
    assert res.n_valid == 2


def test_ring_opt_in_no_ring_named():
    """Rings are opt-in: with no ring matching the record, no quorum is
    demanded -- ring_by_name returns None and the gate checks nothing."""
    rings_rows = []
    assert rings.ring_by_name(rings_rows, "approval") is None
    # Even a supplied quorum-less list is simply not examined.
    assert rings.ring_by_name([{"name": "other", "m": 1,
                                "members": ["alice"]}],
                              "approval") is None


def test_ring_wrong_scheme_labeled(fixture_ring):
    """A sig naming a scheme seatsig does not know is WRONG_SCHEME (no
    scheme -> no verify -> never counted)."""
    import hashlib

    c = fixture_ring["canonical"]
    fake = hashlib.sha256(c).hexdigest()[:16]
    sigs = ["alice:no_such_scheme:" + fake]
    res = rings.verify_ring(fixture_ring["ring"], c, sigs,
                            pubkey_for_post=fixture_ring["pubkeys"].get)
    assert res.labels["alice"] == "WRONG_SCHEME"
    assert res.ok is False


def test_ring_unkeyed_member(fixture_ring):
    """A member with no resolvable pubkey is UNKEYED (not counted)."""
    s = fixture_ring["signers"]
    c = fixture_ring["canonical"]
    sigs = [_sig(s, "alice", c), _sig(s, "bob", c)]
    # bob's pubkey unresolvable now (fixture resolver returns None):
    res = rings.verify_ring(
        fixture_ring["ring"], c, sigs,
        pubkey_for_post=lambda p: None if p == "bob"
        else fixture_ring["pubkeys"].get(p))
    assert res.ok is False
    assert res.labels["bob"] == "UNKEYED"
    assert res.n_valid == 1


def test_canonical_bytes_injective():
    """The canonical form is injective and self-delimiting canonical JSON:
    every assertion here FAILS if canonical_bytes reverts to the old
    line-fused `kind\nkey:value\n` form, which collapsed the two pairs in
    test_canonical_bytes_hostile_collisions into one byte string. Dict order
    does NOT participate (sorted-key semantics): d == e now."""
    a = rings.canonical_bytes("g", {"x": "1"})
    b = rings.canonical_bytes("g", {"x": "1"})
    c = rings.canonical_bytes("g", {"x": "1\n"})
    d = rings.canonical_bytes("g", {"x": "1", "y": "2"})
    e = rings.canonical_bytes("g", {"y": "2", "x": "1"})
    # the canonical form is a single JSON object -- it must parse, carry BOTH
    # the kind and the fields, and be deterministic (real properties now)
    assert a == b
    import json as _json
    obj = _json.loads(a.decode("utf-8"))
    assert obj["kind"] == "g"
    # every key AND value is recursively type-tagged (kid B) so the canonical
    # form is injective at every depth: the field pair is [tag(x), tag(v)].
    assert obj["fields"] == [[["str", "x"], ["str", "1"]]]
    assert a != c               # a value cannot smuggle a line-control byte
    assert a != d               # two fields != one field
    assert d == e               # sorted-key semantics: dict order is ignored
    # the OLD form began with the raw kind; the NEW form must NOT, or the
    # kind-vs-field fusion collision would reopen. So assert it does not.
    assert not a.startswith(b"g\n")


def test_load_rings_from_cell(tmp_path):
    """load_rings reads the `rings:` rows from the Prime's geometry cell, and
    degrades to [] when the cell is absent or carries no rings list."""
    cell = tmp_path / "nodes" / ".geometry" / "rings.md"
    cell.parent.mkdir(parents=True)
    cell.write_text(
        "---\ntype: cell\nrings:\n"
        "  - name: approval\n    m: 2\n    members: [a, b]\n---\n",
        encoding="utf-8")
    assert rings.load_rings(tmp_path) == [{"name": "approval", "m": 2,
                                           "members": ["a", "b"]}]
    # absent cell -> []
    assert rings.load_rings(tmp_path / "nothing") == []
    # a cell with no rings list -> [] too (opt-in): a SEPARATE graph dir
    # whose geometry holds a rules cell but no rings cell.
    other = tmp_path / "other"
    (other / "nodes" / ".geometry").mkdir(parents=True)
    (other / "nodes" / "rules.md").write_text("---\ntype: cell\n---\n",
                                              encoding="utf-8")
    assert rings.load_rings(tmp_path / "other") == []

# ---------------------------------------------------------------------------
# The write.py gate (rung 2 gate 3): a `ring:`-declaring config schema demands
# the ring quorum for a NON-SELF-ROW config write, verified through seatsig,
# and REFUSES BY NAME with the m-of-n count when short. Opt-in: no `ring:` in
# a schema -> no quorum demanded.
# ---------------------------------------------------------------------------
import write  # noqa: E402  (write.py's _enforce_written_by, the gate under test)


def _write_gate_root(tmp_path):
    """A fixture graph root: config.json, a custom config schema that declares
    `written_by: prime` and `ring: approval` (so an UNADMITTED actor reaches
    the ring gate, and a quorum is demanded for a non-self-row config-row
    write), a rings geometry cell naming the ring, and a posts.md carrying the
    members' pubkeys (`_ring_pubkey_for_post` reads those rows)."""
    agi = tmp_path / ".agi"
    agi.mkdir(parents=True)
    (agi / "config.json").write_text("{}", encoding="utf-8")
    sd = agi / "context" / "schemas"
    sd.mkdir(parents=True)
    (sd / "[config].md").write_text(
        "---\ntype: config\nwritten_by: prime\nring: approval\n---\n",
        encoding="utf-8")
    scheme = get("fixture")
    keys = {m: scheme.keygen() for m in ("alice", "bob", "carol")}
    pubkeys = {m: priv.hex() for m, (priv, _pub) in keys.items()}
    (agi / "nodes" / ".geometry").mkdir(parents=True)
    (agi / "nodes" / ".geometry" / "rings.md").write_text(
        "---\ntype: cell\nrings:\n"
        "  - name: approval\n    m: 2\n"
        "    members: [alice, bob, carol]\n---\n",
        encoding="utf-8")
    rows = "\n".join(
        f"  - name: {m}\n    pubkey: {pubkeys[m]}" for m in ("alice", "bob", "carol"))
    (agi / "nodes" / ".geometry" / "posts.md").write_text(
        f"---\ntype: config\nposts:\n{rows}\n---\n", encoding="utf-8")
    # Return the SIGNING keys too (priv == pub in the dummy scheme): the
    # test signs with the same key whose pubkey the posts row carries.
    return agi, {m: priv for m, (priv, _pub) in keys.items()}


def test_write_gate_ring_short_refused_by_name(tmp_path):
    """A config write by a WRITTEN_BY-ADMITTED writer on a `ring:`-declaring
    schema, short of m, is REFUSED BY NAME with the m-of-n count (AND: the
    ring gates even an admitted writer -- hypothesis:l4-canonical-bytes-are-
    injective-and-fresh-and-the-ring-gates-the-write-itself defect 3)."""
    root, signers = _write_gate_root(tmp_path)
    # FRESH (kid B): pin the ts|nonce the signer covers so the gate verifies
    # the SAME decision; a quorum short of m refuses on quorum (not freshness)
    ts, nonce = _iso(time.time()), "write-short"
    fields = write._config_write_fields(
        "config:seats", {"seats": [{"name": "x"}]}, ts=ts, nonce=nonce)
    canonical = rings.canonical_bytes("config-write", fields)
    sigs = [_sig(signers, "alice", canonical)]  # one of m=2
    with pytest.raises(write.EditError) as ei:
        write._enforce_written_by(root, "config", "director1", "config:seats",
                                  role="prime",
                                  set_fm={"seats": [{"name": "x"}]},
                                  signatures=sigs, ring_fresh=(ts, nonce))
    msg = str(ei.value)
    assert "approval" in msg
    assert "got 1" in msg
    assert "2" in msg


def test_write_gate_ring_satisfied_admits(tmp_path):
    """m valid signatures over the record's canonical bytes with a
    WRITTEN_BY-ADMITTED writer -> the write is admitted (both gates pass, the
    gate returns, no refusal). The ring quorum alone does NOT admit an
    unadmitted writer (see test_write_gate_ring_is_an_and_gate)."""
    root, signers = _write_gate_root(tmp_path)
    ts, nonce = _iso(time.time()), "write-admits"
    fields = write._config_write_fields(
        "config:seats", {"seats": [{"name": "x"}]}, ts=ts, nonce=nonce)
    canonical = rings.canonical_bytes("config-write", fields)
    sigs = [_sig(signers, m, canonical) for m in ("alice", "bob")]
    # No exception == admitted by BOTH written_by (role prime) AND the ring
    # quorum AND freshness (ts~now).
    write._enforce_written_by(root, "config", "director1", "config:seats",
                              role="prime",
                              set_fm={"seats": [{"name": "x"}]},
                              signatures=sigs, ring_fresh=(ts, nonce))
    assert True


def test_write_gate_ring_is_an_and_gate(tmp_path):
    """DEFECT 3 (hypothesis:l4-canonical-bytes-are-injective-and-fresh-and-
the-ring-gates-the-write-itself): the ring quorum is an ADDITIONAL gate, not
an OR alternative to written_by. An UNADMITTED writer ('intruder' is not
written_by: prime) WITH a satisfied m=2 ring quorum is still REFUSED, and the
refusal is the written_by line -- never the ring line."""
    root, signers = _write_gate_root(tmp_path)
    ts, nonce = _iso(time.time()), "write-and"
    fields = write._config_write_fields(
        "config:seats", {"seats": [{"name": "x"}]}, ts=ts, nonce=nonce)
    canonical = rings.canonical_bytes("config-write", fields)
    sigs = [_sig(signers, m, canonical) for m in ("alice", "bob")]  # valid m=2
    with pytest.raises(write.EditError) as ei:
        write._enforce_written_by(root, "config", "intruder", "config:seats",
                                  set_fm={"seats": [{"name": "x"}]},
                                  signatures=sigs, ring_fresh=(ts, nonce))
    msg = str(ei.value)
    assert "hand-edited only by" in msg     # the written_by refusal, names roles
    assert "rung 2" not in msg              # never the ring line (test C)


def test_write_gate_ring_outside_still_refused(tmp_path):
    """A forged/outsider signature does not satisfy m -> still refused (ring
    gate, against a written_by-admitted writer)."""
    root, signers = _write_gate_root(tmp_path)
    ts, nonce = _iso(time.time()), "write-outside"
    fields = write._config_write_fields(
        "config:seats", {"seats": [{"name": "x"}]}, ts=ts, nonce=nonce)
    canonical = rings.canonical_bytes("config-write", fields)
    # bob's sig is forged (flip last byte); alice valid -> only 1 of m=2
    forged = _sig(signers, "bob", canonical)[:-2] + "00"
    sigs = [_sig(signers, "alice", canonical), forged]
    with pytest.raises(write.EditError) as ei:
        write._enforce_written_by(root, "config", "director1", "config:seats",
                                  role="prime",
                                  set_fm={"seats": [{"name": "x"}]},
                                  signatures=sigs, ring_fresh=(ts, nonce))
    assert "got 1" in str(ei.value)


def test_write_gate_opt_in_no_ring_declared(tmp_path):
    """No `ring:` in the schema -> no quorum demanded: a non-self-row config
    write by an unadmitted actor is refused by the ordinary written_by rule,
    NOT by the ring gate (which never fires)."""
    agi = tmp_path / ".agi"
    agi.mkdir(parents=True)
    (agi / "config.json").write_text("{}", encoding="utf-8")
    sd = agi / "context" / "schemas"
    sd.mkdir(parents=True)
    (sd / "[config].md").write_text(
        "---\ntype: config\nwritten_by: prime\n---\n", encoding="utf-8")
    with pytest.raises(write.EditError) as ei:
        write._enforce_written_by(agi, "config", "intruder", "config:seats",
                                  set_fm={"seats": [{"name": "x"}]})
    msg = str(ei.value)
    assert "hand-edited only by" in msg
    assert "ring" not in msg  # the ring gate never fired


# ---------------------------------------------------------------------------
# The verification.py --suite gate (rung 2 gate 2): a merge grant the ring
# must approve is REFUSED BY NAME with the m-of-n count when short, admitted
# at m, and untouched when no ring is named (opt-in).
# ---------------------------------------------------------------------------
import verification  # noqa: E402


def _suite_grant_root(tmp_path):
    """A fixture graph root: rings cell naming `approval` (m=2, 3 members)
    and posts.md carrying their pubkeys (what the resolver reads)."""
    agi = tmp_path / ".agi"
    agi.mkdir(parents=True)
    (agi / "config.json").write_text("{}", encoding="utf-8")
    (agi / "nodes" / ".geometry").mkdir(parents=True)
    scheme = get("fixture")
    keys = {m: scheme.keygen() for m in ("alice", "bob", "carol")}
    pubkeys = {m: priv.hex() for m, (priv, _pub) in keys.items()}
    (agi / "nodes" / ".geometry" / "rings.md").write_text(
        "---\ntype: cell\nrings:\n"
        "  - name: approval\n    m: 2\n"
        "    members: [alice, bob, carol]\n---\n", encoding="utf-8")
    rows = "\n".join(
        f"  - name: {m}\n    pubkey: {pubkeys[m]}"
        for m in ("alice", "bob", "carol"))
    (agi / "nodes" / ".geometry" / "posts.md").write_text(
        f"---\ntype: config\nposts:\n{rows}\n---\n", encoding="utf-8")
    return agi, {m: priv for m, (priv, _pub) in keys.items()}


def test_suite_ring_gate_short_refused(tmp_path):
    """A merge grant short of the ring's m is refused by name with the
    m-of-n count."""
    root, signers = _suite_grant_root(tmp_path)
    # FRESH (kid B): the exact signed decision is handed to the gate; a quorum
    # short of m is refused on quorum, never freshness (which follows admit).
    fields = verification._suite_grant_fields(root, "rotation", "approval")
    canonical = rings.canonical_bytes("suite-grant", fields)
    sigs = [_sig(signers, "alice", canonical)]  # one of m=2
    refusal = verification._ring_gate_refusal(root, "approval", "rotation",
                                              sigs, fields=fields)
    assert refusal is not None
    assert "approval" in refusal
    assert "got 1" in refusal


def test_suite_ring_gate_satisfied_admits(tmp_path):
    """At m valid signatures the grant is admitted (returns None)."""
    root, signers = _suite_grant_root(tmp_path)
    fields = verification._suite_grant_fields(root, "rotation", "approval")
    canonical = rings.canonical_bytes("suite-grant", fields)
    sigs = [_sig(signers, m, canonical) for m in ("alice", "bob")]
    assert verification._ring_gate_refusal(root, "approval", "rotation",
                                           sigs, fields=fields) is None


def test_suite_ring_gate_opt_in_no_ring(tmp_path):
    """No ring named in the geometry -> the suite-ring gate demands nothing
    (opt-in): refusal is None even with no signatures at all."""
    root, _ = _suite_grant_root(tmp_path)
    # A ring name the cell does NOT declare.
    assert verification._ring_gate_refusal(root, "ghost-ring", "rotation", []) \
        is None


# ---------------------------------------------------------------------------
# The dispatch.py round-ring gate (rung 2 gate 1): a round --ring-gate ring
# must approve the round-cut record. REFUSED BY NAME with the m-of-n count
# when short, admitted at m, opt-in when no ring is named.
# ---------------------------------------------------------------------------
import dispatch  # noqa: E402


def test_dispatch_round_gate_short_refused(tmp_path):
    """A round cut short of the ring's m is refused by name with the count;
    nothing would spawn."""
    root, signers = _suite_grant_root(tmp_path)  # same fixture shape
    fields = dispatch._round_cut_fields("kid", "", "", "", 0)
    canonical = rings.canonical_bytes("round-cut", fields)
    sigs = [_sig(signers, "alice", canonical)]  # one of m=2
    refusal = dispatch._round_ring_refusal(str(tmp_path), "approval", "kid",
                                           "", sigs, fields=fields)
    assert refusal is not None
    assert "approval" in refusal
    assert "got 1" in refusal


def test_dispatch_round_gate_satisfied_admits(tmp_path):
    """At m valid signatures the round is admitted (returns None)."""
    root, signers = _suite_grant_root(tmp_path)
    fields = dispatch._round_cut_fields("kid", "", "", "", 0)
    canonical = rings.canonical_bytes("round-cut", fields)
    sigs = [_sig(signers, m, canonical) for m in ("alice", "bob")]
    assert dispatch._round_ring_refusal(str(tmp_path), "approval", "kid",
                                        "", sigs, fields=fields) is None


def test_dispatch_round_gate_opt_in(tmp_path):
    """A ring the geometry does not name -> nothing demanded (opt-in)."""
    root, _ = _suite_grant_root(tmp_path)
    assert dispatch._round_ring_refusal(str(tmp_path), "ghost-ring", "kid",
                                        "", []) is None

# ---------------------------------------------------------------------------
# HOLE 2 (kid 2): the signed bytes must cover the FULL decision it authorises
# (no truncation), so a quorum for record A cannot replay onto record B that
# differs in any covered field. The shared field-builders (write._config_write
# _fields / dispatch._round_cut_fields / verification._suite_grant_fields) are
# the ONE source the gate AND the sign side use, so these prove the gate acts
# on exactly the bytes it signs.
# ---------------------------------------------------------------------------

def test_write_gate_nonreplay(tmp_path):
    """A quorum that admits row A (seats=[x]) must NOT admit row B
    (seats=[y]) -- a covered value changed, the canonical changed."""
    root, signers = _write_gate_root(tmp_path)
    ts, nonce = _iso(time.time()), "write-nonreplay"
    fields_a = write._config_write_fields(
        "config:seats", {"seats": [{"name": "x"}]}, ts=ts, nonce=nonce)
    canonical_a = rings.canonical_bytes("config-write", fields_a)
    sigs = [_sig(signers, m, canonical_a) for m in ("alice", "bob")]
    # record A is admitted by its OWN signatures (written_by-admitted writer)
    write._enforce_written_by(root, "config", "director1", "config:seats",
                              role="prime",
                              set_fm={"seats": [{"name": "x"}]},
                              signatures=sigs, out_decision={},
                              ring_fresh=(ts, nonce))
    # ...a record B differing only in the seats field is REFUSED (A's nonce is
    # spent AND its bytes no longer match; B never gets past the quorum).
    ts_b, nonce_b = _iso(time.time()), "write-nonreplay-b"
    with pytest.raises(write.EditError) as ei:
        write._enforce_written_by(root, "config", "director1", "config:seats",
                                  role="prime",
                                  set_fm={"seats": [{"name": "y"}]},
                                  signatures=sigs, out_decision={},
                                  ring_fresh=(ts_b, nonce_b))
    assert "rung 2 multisig ring" in str(ei.value)


def test_config_write_decision_reverified_from_disk(tmp_path):
    """Claim (2) persistence (config-write seam): after the gate admits, the
    decision cell is captured and, written onto the node on disk (frontmatter),
    round-trips and RE-VERIFIES m-of-n from DISK (never argv). A tampered cell
    (one signature removed) reads short-of-m by name."""
    root, signers = _write_gate_root(tmp_path)
    ts, nonce = _iso(time.time()), "write-disk"
    fields = write._config_write_fields(
        "config:seats", {"seats": [{"name": "x"}]}, ts=ts, nonce=nonce)
    canonical = rings.canonical_bytes("config-write", fields)
    sigs = [_sig(signers, m, canonical) for m in ("alice", "bob")]
    out: dict = {}
    write._enforce_written_by(root, "config", "director1", "config:seats",
                              role="prime",
                              set_fm={"seats": [{"name": "x"}]},
                              signatures=sigs, out_decision=out,
                              ring_fresh=(ts, nonce))
    cell = out["cell"]
    assert cell["kind"] == "config-write"
    assert cell["ring"] == "approval"
    # The sanctioned writer lands ring_decision in the node's frontmatter;
    # write a fixture node the same way and read it back from DISK.
    node = tmp_path / "config-seats.md"
    node.write_text("---\n" + json.dumps(
        {"type": "config", "ring_decision": cell}) + "\n---\nbody\n",
        encoding="utf-8")
    from graph_core.persistence import frontmatter  # noqa: PLC0415
    nf = frontmatter.load_node_file(node)
    ring = rings.ring_by_name(rings.load_rings(root), "approval")
    res = rings.verify_decision(
        nf.frontmatter["ring_decision"], ring,
        pubkey_for_post=write._ring_pubkey_for_post(root))
    assert res.ok is True
    # tamper: drop one signature -> reads short-of-m by name.
    tampered = dict(nf.frontmatter["ring_decision"])
    tampered["signatures"] = tampered["signatures"][:1]
    res2 = rings.verify_decision(
        tampered, ring, pubkey_for_post=write._ring_pubkey_for_post(root))
    assert res2.ok is False
    assert "got 1" in res2.refused


def test_suite_grant_nonreplay(tmp_path):
    """A suite-grant quorum for level rotation must NOT admit the same root
    under a different covered field (level changes -> REFUSED)."""
    root, signers = _suite_grant_root(tmp_path)
    fields_a = verification._suite_grant_fields(root, "rotation", "approval")
    canonical = rings.canonical_bytes("suite-grant", fields_a)
    sigs = [_sig(signers, m, canonical) for m in ("alice", "bob")]
    # the EXACT signed decision is handed to the gate (never argv).
    assert verification._ring_gate_refusal(
        root, "approval", "rotation", sigs, fields=fields_a) is None
    # level changed -> the same signatures no longer admit (fresh fields for
    # the level we did NOT sign cover different bytes -> FORGED).
    fields_full = verification._suite_grant_fields(root, "full", "approval")
    assert verification._ring_gate_refusal(
        root, "approval", "full", sigs, fields=fields_full) is not None


def test_suite_decision_persisted_and_reverified_from_disk(tmp_path):
    """Claim (2) persistence (suite seam): an admitted --suite-ring run merges
    its decision onto the ONE record the suite already writes (the SUITE_TS
    FILE, not a second ledger); loaded from DISK (no argv) it re-verifies
    m-of-n; a tampered record (one signature removed) reads short-of-m by name."""
    root, signers = _suite_grant_root(tmp_path)
    fields = verification._suite_grant_fields(root, "rotation", "approval")
    canonical = rings.canonical_bytes("suite-grant", fields)
    sigs = [_sig(signers, m, canonical) for m in ("alice", "bob")]
    decision = rings.decision_cell("approval", "suite-grant", fields, sigs)
    verification._record_suite_ts(root, decision)
    # Load the RECORD from disk -- no argv anywhere in the re-verify path.
    doc = json.loads(verification._suite_ts_path(root).read_text(encoding="utf-8"))
    pub = {m: priv.hex() for m, priv in signers.items()}
    ring = rings.ring_by_name(rings.load_rings(root), "approval")
    res = rings.verify_decision(doc["ring_decision"], ring,
                                pubkey_for_post=pub.get)
    assert res.ok is True
    tampered = dict(doc["ring_decision"])
    tampered["signatures"] = tampered["signatures"][:1]
    res2 = rings.verify_decision(tampered, ring, pubkey_for_post=pub.get)
    assert res2.ok is False
    assert "got 1" in res2.refused


def test_round_cut_nonreplay(tmp_path):
    """A round-cut quorum for iter 1 must NOT admit a round differing only in
    iter_n -- the covered field changed, the canonical changed."""
    root, signers = _suite_grant_root(tmp_path)
    fields_a = dispatch._round_cut_fields("kid", "kid", "nodeX", "small", 1)
    canonical_a = rings.canonical_bytes("round-cut", fields_a)
    sigs = [_sig(signers, m, canonical_a) for m in ("alice", "bob")]
    # the gate acting on the EXACT signed decision admits those signatures...
    assert dispatch._round_ring_refusal(
        str(tmp_path), "approval", "kid", "kid", sigs,
        target="nodeX", level="small", iter_n=1, fields=fields_a) is None
    # ...a round differing only in iter_n is REFUSED (short-of-m by name).
    fields_b = dispatch._round_cut_fields("kid", "kid", "nodeX", "small", 2)
    refusal = dispatch._round_ring_refusal(
        str(tmp_path), "approval", "kid", "kid", sigs,
        target="nodeX", level="small", iter_n=2, fields=fields_b)
    assert refusal is not None
    assert "m-of-n" in refusal


def test_dispatch_decision_persisted_and_reverified_from_disk(tmp_path):
    """Claim (2) persistence (round seam): the admitted round-quorum decision
    rides on the agent record (agent.json) the round writes; loaded from DISK
    (no argv) it re-verifies m-of-n; removing one signature reads short-of-m."""
    root, signers = _suite_grant_root(tmp_path)
    fields = dispatch._round_cut_fields("kid", "kid", "nodeX", "small", 1)
    canonical = rings.canonical_bytes("round-cut", fields)
    sigs = [_sig(signers, m, canonical) for m in ("alice", "bob")]
    decision = rings.decision_cell("approval", "round-cut", fields, sigs)
    agent_json = tmp_path / "agent.json"
    agent_json.write_text(
        json.dumps({"id": "a00-fixture", "ring_decision": decision}, indent=2),
        encoding="utf-8")
    rec = json.loads(agent_json.read_text(encoding="utf-8"))
    pub = {m: priv.hex() for m, priv in signers.items()}
    ring = rings.ring_by_name(rings.load_rings(root), "approval")
    res = rings.verify_decision(rec["ring_decision"], ring,
                                pubkey_for_post=pub.get)
    assert res.ok is True
    tampered = dict(rec["ring_decision"])
    tampered["signatures"] = tampered["signatures"][:1]
    res2 = rings.verify_decision(tampered, ring, pubkey_for_post=pub.get)
    assert res2.ok is False
    assert "got 1" in res2.refused


# ---------------------------------------------------------------------------
# The INJECTIVITY claim (hypothesis:l4-canonical-bytes-are-...): the OLD
# `kind\\nkey:value\\n` form collapsed the Prime's colliding pairs into one
# byte string (measured pre-fix, see the experiment node). The canonical JSON
# form MUST make every pair differ.
# ---------------------------------------------------------------------------
def test_canonical_bytes_hostile_collisions():
    """The Prime's measured collision pairs: each distinct (kind, fields)
    input must now produce DIFFERENT bytes (the old form fused both members
    of every pair)."""
    pairs = [
        ("g", {"x": "1\nb:2"}), ("g", {"x": "1", "b": "2"}),
        ("g", {"a:b": "c"}), ("g", {"a": "b:c"}),
        ("g\nx:1", {}), ("g", {"x": "1"}),
    ]
    # every consecutive pair in this list is the two members of one
    # collision; the two BYTES emitted for each pair must now differ
    toks = [rings.canonical_bytes(*p) for p in pairs]
    assert toks[0] != toks[1]
    assert toks[2] != toks[3]
    assert toks[4] != toks[5]


def test_canonical_bytes_type_tags():
    """Type tags: str/int/list/None must not collide -- `"1"` (str) vs
    `1` (int) vs `[1]`, and `None` vs `"None"`."""
    b_str = rings.canonical_bytes("g", {"x": "1"})
    b_int = rings.canonical_bytes("g", {"x": 1})
    b_list = rings.canonical_bytes("g", {"x": [1]})
    b_none = rings.canonical_bytes("g", {"x": None})
    b_none_s = rings.canonical_bytes("g", {"x": "None"})
    assert b_str != b_int
    assert b_str != b_list
    assert b_list != b_str
    assert b_none != b_none_s
    assert b_int != b_none  # int 1 vs None too
    assert b_str != b_none


def test_canonical_bytes_round_trip_through_verify(fixture_ring):
    """A hostile decision cell (fields containing `\\n` and `:`) signs over
    the NEW canonical bytes and verifies m-of-n; the SAME cell VERIFIED
    against the OLD line-fused form's bytes must FAIL (a signature for the
    new bytes is FORGED for the old bytes -- proving the identity of the
    bytes covered, not just that m sigs appear)."""
    s = fixture_ring["signers"]
    ring = fixture_ring["ring"]
    resolve = fixture_ring["pubkeys"].get
    fields = {"ref": "s2/main", "note": "line\n then: colon"}
    # signed over the CURRENT (new) canonical bytes
    canonical = rings.canonical_bytes("merge-grant", fields)
    sigs = [_sig(s, "alice", canonical), _sig(s, "bob", canonical)]
    res = rings.verify_ring(ring, canonical, sigs, pubkey_for_post=resolve)
    assert res.ok is True
    assert res.labels["alice"] == "VERIFIED"
    assert res.labels["bob"] == "VERIFIED"
    # the same cell, re-verified against the OLD-form bytes for the same
    # fields: both signatures must now read FORGED (the sigs covered the NEW
    # bytes, so they cannot verify over the old ones)
    old = (
        "merge-grant\n"
        "ref:s2/main\n"
        "note:line\n then: colon\n"
    ).encode()
    res_old = rings.verify_ring(ring, old, sigs, pubkey_for_post=resolve)
    assert res_old.ok is False
    assert res_old.labels["alice"] == "FORGED"
    assert res_old.labels["bob"] == "FORGED"


def test_canonical_bytes_round_trip_via_decision_cell(fixture_ring):
    """decision_cell -> verify_decision round-trips over a hostile field
    (key AND value both carrying `\\n` and `:`): the signatures verify and
    m-of-n is met exactly because the reader recomputes the same bytes."""
    s = fixture_ring["signers"]
    ring = fixture_ring["ring"]
    resolve = fixture_ring["pubkeys"].get
    fields = {"scope:prime\n": "merge-over\nline:1", "ref": "s2/main"}
    canonical = rings.canonical_bytes("merge-grant", fields)
    sigs = [_sig(s, "alice", canonical), _sig(s, "bob", canonical)]
    cell = rings.decision_cell("approval", "merge-grant", fields, sigs)
    res = rings.verify_decision(cell, ring, pubkey_for_post=resolve)
    assert res.ok is True
    assert res.n_valid == 2
    assert res.ring_name == "approval"


# ---------------------------------------------------------------------------
# KID B PART 1 -- kid A's two residual injectivity holes closed. The OLD
# canonical form fused a dict keyed by the int ``1`` with its str-``"1"``
# twin, and a tuple with a list of the same elements. Both pairs MUST now
# differ -- a live DISPROOF of the hypothesis as written, fixed.
# ---------------------------------------------------------------------------
def test_canonical_bytes_non_str_dict_keys_do_not_fuse():
    """A dict whose keys are not all str must NOT serialize as the same
    bytes as its str-keyed twin: {1: 'a'} and {'1': 'a'} now differ (the
    dict key is type-tagged, not silently coerced by JSON)."""
    assert rings.canonical_bytes("g", {"x": {1: "a"}}) != \
        rings.canonical_bytes("g", {"x": {"1": "a"}})
    # nested one level deeper in a list too
    assert rings.canonical_bytes("g", {"x": [{1: "a"}]}) != \
        rings.canonical_bytes("g", {"x": [{"1": "a"}]})


def test_canonical_bytes_tuple_and_list_do_not_fuse():
    """A tuple must not share a tag with a list: (1, 2) and [1, 2] now
    differ (kid A left tuple tagged as 'list'; kid B gives it 'tuple')."""
    assert rings.canonical_bytes("g", {"x": (1, 2)}) != \
        rings.canonical_bytes("g", {"x": [1, 2]})
    assert rings.canonical_bytes("g", {"x": ()}) != \
        rings.canonical_bytes("g", {"x": []})
    # nested inside a dict value too
    assert rings.canonical_bytes("g", {"x": {"y": (1, 2)}}) != \
        rings.canonical_bytes("g", {"x": {"y": [1, 2]}})


# ---------------------------------------------------------------------------
# KID B PART 2 -- FRESHNESS. A record's signatures cover its fields; those
# fields carry no time and no nonce, so a persisted quorum replays across
# time (the same signed suite-grant is valid forever). fresh_fields adds the
# reserved _fresh (ts|nonce) as a FIELD; freshness_refusal refuses by name.
# ---------------------------------------------------------------------------
_NOW = 1_776_000_000.0  # a fixed unix epoch for the no-time-randomness checks


def _iso(t):
    import datetime as _dt
    return _dt.datetime.fromtimestamp(t, _dt.timezone.utc).strftime(
        "%Y-%m-%dT%H:%M:%SZ")


def test_fresh_fields_reserved_key_cannot_be_spoofed():
    """A caller passing '_fresh' in fields to fresh_fields is OVERWRITTEN,
    never merged -- the reserved freshness key cannot be spoofed by a
    producer stuffing their own value in."""
    f = rings.fresh_fields({"_fresh": "STALE|spoof", "a": 1},
                           ts="2026-09-12T16:45:56Z", nonce="n1")
    assert f["_fresh"] == "2026-09-12T16:45:56Z|n1"
    assert f["a"] == 1
    # input dict is not mutated
    src = {"a": 1}
    rings.fresh_fields(src, ts=_iso(_NOW), nonce="x")
    assert "_fresh" not in src


def test_freshness_refusal_missing_and_malformed():
    """No _fresh -> refused by name; a _fresh missing the '|' -> malformed."""
    r = rings.freshness_refusal({"a": 1}, now=_NOW)
    assert r is not None and "_fresh" in r
    r2 = rings.freshness_refusal({"_fresh": "not-a-pipe"},
                                 now=_NOW)
    assert r2 is not None and "malformed" in r2
    r3 = rings.freshness_refusal({"_fresh": "garbage-ts|n1"}, now=_NOW)
    assert r3 is not None and "unparseable" in r3


def test_freshness_window_and_boundary():
    """A record 901s old is refused naming age AND window; one at 899s is
    admitted; exactly at max_age_s (900s) is admitted (boundary inclusive)."""
    old = rings.fresh_fields({"a": 1}, ts=_iso(_NOW - 901), nonce="o1")
    r = rings.freshness_refusal(old, now=_NOW)
    assert r is not None
    assert "901s" in r and "900s" in r
    fresh = rings.fresh_fields({"a": 1}, ts=_iso(_NOW - 899), nonce="f1")
    assert rings.freshness_refusal(fresh, now=_NOW) is None
    boundary = rings.fresh_fields({"a": 1}, ts=_iso(_NOW - 900), nonce="b1")
    assert rings.freshness_refusal(boundary, now=_NOW) is None


def test_freshness_future_skew_refused():
    """A ts 301s in the future is refused by name (clock-skew guard);
    300s exactly (the boundary) is admitted."""
    fut = rings.fresh_fields({"a": 1}, ts=_iso(_NOW + 301), nonce="fut")
    r = rings.freshness_refusal(fut, now=_NOW)
    assert r is not None and "future" in r and "clock-skew" in r
    at = rings.fresh_fields({"a": 1}, ts=_iso(_NOW + 300), nonce="at")
    assert rings.freshness_refusal(at, now=_NOW) is None


def test_freshness_replay_nononce(monkeypatch, tmp_path):
    """The same nonce twice: first admitted (and remembered), second refused
    by name; a REFUSED record does not consume its nonce."""
    seen, remember = rings.nonce_ledger(tmp_path)
    f1 = rings.fresh_fields({"a": 1}, ts=_iso(_NOW), nonce="shared")
    assert rings.freshness_refusal(f1, now=_NOW, seen=seen,
                                   remember=remember) is None
    # second use of the same nonce -> replayed by name
    f2 = rings.fresh_fields({"a": 2}, ts=_iso(_NOW), nonce="shared")
    r = rings.freshness_refusal(f2, now=_NOW, seen=seen,
                                remember=remember)
    assert r is not None and "replayed nonce" in r and "shared" in r
    # a distinct nonce is still admitted and remembered
    f3 = rings.fresh_fields({"a": 3}, ts=_iso(_NOW), nonce="other")
    assert rings.freshness_refusal(f3, now=_NOW, seen=seen,
                                   remember=remember) is None
    assert "other" in seen


def test_freshness_refused_never_burns_nonce(tmp_path):
    """A record refused on STALENESS must not have its nonce remembered, so
    a re-fresh of the same decision later is not rejected as a replay."""
    seen, remember = rings.nonce_ledger(tmp_path)
    stale = rings.fresh_fields({"a": 1}, ts=_iso(_NOW - 5000), nonce="kept")
    assert rings.freshness_refusal(stale, now=_NOW, seen=seen,
                                   remember=remember) is not None
    assert "kept" not in seen  # never burned


def test_nonce_ledger_round_trip(tmp_path):
    """remember writes the ledger; a SECOND nonce_ledger(root) call sees it
    (fresh read each call, persists across calls)."""
    seen1, remember1 = rings.nonce_ledger(tmp_path)
    remember1("n_roundtrip")
    seen2, _ = rings.nonce_ledger(tmp_path)
    assert "n_roundtrip" in seen2
    assert (tmp_path / "nodes" / ".geometry" / "ring-nonces.json").exists()


# ---------------------------------------------------------------------------
# KID B PART 3 -- the gates sign FRESH fields and re-verify freshness on the
# persisted fields (the same bytes both sides): a fresh decision is admitted,
# a stale one refused BY NAME end-to-end through verification.py's helper.
# ---------------------------------------------------------------------------
def test_suite_grant_fresh_and_stale_end_to_end(tmp_path):
    """A FRESH suite-grant is admitted and a STALE one REFUSED by name
    through verification._ring_gate_refusal -- the same helper, fixtures
    only, no real key minted. The gate internally computes FRESH fields and
    refuses a too-old decision before admitting."""
    root, signers = _suite_grant_root(tmp_path)
    pub = {m: priv.hex() for m, priv in signers.items()}
    # -- forge a stale decision's signatures and call the gate with the EXACT
    # fields it must verify (never argv): the gate refuses by age.
    def _refuse_for(fields):
        canonical = rings.canonical_bytes("suite-grant", fields)
        sigs = [_sig(signers, m, canonical) for m in ("alice", "bob")]
        return verification._ring_gate_refusal(
            root, "approval", "rotation", sigs,
            fields=rings.fresh_fields(
                {k: v for k, v in fields.items() if k != "_fresh"},
                ts=fields["_fresh"].split("|")[0],
                nonce=fields["_fresh"].split("|", 1)[1]))

    stale_fields = rings.fresh_fields(
        {"level": "rotation", "root": str(root), "ring": "approval"},
        ts=_iso(_NOW - 5000), nonce="stale1")
    r = _refuse_for(stale_fields)
    assert r is not None and "stale" in r
    fresh_fields = rings.fresh_fields(
        {"level": "rotation", "root": str(root), "ring": "approval"},
        ts=_iso(time.time()), nonce="fresh1")
    assert _refuse_for(fresh_fields) is None


def test_json_field_nested_keys_injective():
    """json_field (the config-write/pre-round value serializer) must NOT fuse
    a dict keyed by int ``1`` with its ``"1"`` str twin, nor a tuple with a
    list -- the same injection guarantee as canonical_bytes, at the field
    string layer a gate persists."""
    assert rings.json_field({1: "a"}) != rings.json_field({"1": "a"})
    assert rings.json_field((1, 2)) != rings.json_field([1, 2])
    assert rings.json_field("plain") == "plain"
