"""Tests for seatsig.rings -- multisig m-of-n ring verification (rung 2).

Covers on FIXTURE keys: m-of-n satisfied / one short / one forged (rung-1
FORGED label) / a member OUTSIDE the ring / rings opt-in (no ring named -->
nothing changes) / unknown scheme / unkeyed member. Everything verifies
through the seatsig Scheme interface (never its own crypto), and a record
short of m is REFUSED by name with the m-of-n count.
"""

from __future__ import annotations

import json
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
    """The canonical form is injective: field collision cannot fuse records,
    and order matters (kind then k:v lines)."""
    a = rings.canonical_bytes("g", {"x": "1"})
    b = rings.canonical_bytes("g", {"x": "1"})
    c = rings.canonical_bytes("g", {"x": "1\n"})
    d = rings.canonical_bytes("g", {"x": "1", "y": "2"})
    e = rings.canonical_bytes("g", {"y": "2", "x": "1"})
    assert a == b
    assert a != c  # a value cannot smuggle a line
    assert a != d
    assert d != e  # field order is part of the record
    assert a.startswith(b"g\n")


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
    """A config write outside the writer's own row on a `ring:`-declaring
    schema, short of m, is REFUSED BY NAME with the m-of-n count."""
    root, signers = _write_gate_root(tmp_path)
    canonical = rings.canonical_bytes(
        "config-write", write._config_write_fields(
            "config:seats", {"seats": [{"name": "x"}]}))
    sigs = [_sig(signers, "alice", canonical)]  # one of m=2
    with pytest.raises(write.EditError) as ei:
        write._enforce_written_by(root, "config", "intruder", "config:seats",
                                  set_fm={"seats": [{"name": "x"}]},
                                  signatures=sigs)
    msg = str(ei.value)
    assert "approval" in msg
    assert "got 1" in msg
    assert "2" in msg


def test_write_gate_ring_satisfied_admits(tmp_path):
    """m valid signatures over the record's canonical bytes -> the write is
    admitted (the gate returns, no refusal)."""
    root, signers = _write_gate_root(tmp_path)
    canonical = rings.canonical_bytes(
        "config-write", write._config_write_fields(
            "config:seats", {"seats": [{"name": "x"}]}))
    sigs = [_sig(signers, m, canonical) for m in ("alice", "bob")]
    # No exception == admitted by the ring quorum.
    write._enforce_written_by(root, "config", "intruder", "config:seats",
                              set_fm={"seats": [{"name": "x"}]},
                              signatures=sigs)
    assert True


def test_write_gate_ring_outside_still_refused(tmp_path):
    """A forged/outsider signature does not satisfy m -> still refused."""
    root, signers = _write_gate_root(tmp_path)
    canonical = rings.canonical_bytes(
        "config-write", write._config_write_fields(
            "config:seats", {"seats": [{"name": "x"}]}))
    # bob's sig is forged (flip last byte); alice valid -> only 1 of m=2
    forged = _sig(signers, "bob", canonical)[:-2] + "00"
    sigs = [_sig(signers, "alice", canonical), forged]
    with pytest.raises(write.EditError) as ei:
        write._enforce_written_by(root, "config", "intruder", "config:seats",
                                  set_fm={"seats": [{"name": "x"}]},
                                  signatures=sigs)
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
    canonical = rings.canonical_bytes(
        "suite-grant", verification._suite_grant_fields(
            root, "rotation", "approval"))
    sigs = [_sig(signers, "alice", canonical)]  # one of m=2
    refusal = verification._ring_gate_refusal(root, "approval", "rotation", sigs)
    assert refusal is not None
    assert "approval" in refusal
    assert "got 1" in refusal


def test_suite_ring_gate_satisfied_admits(tmp_path):
    """At m valid signatures the grant is admitted (returns None)."""
    root, signers = _suite_grant_root(tmp_path)
    canonical = rings.canonical_bytes(
        "suite-grant", verification._suite_grant_fields(
            root, "rotation", "approval"))
    sigs = [_sig(signers, m, canonical) for m in ("alice", "bob")]
    assert verification._ring_gate_refusal(root, "approval", "rotation", sigs) \
        is None


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
    canonical = rings.canonical_bytes(
        "round-cut", dispatch._round_cut_fields("kid", "", "", "", 0))
    sigs = [_sig(signers, "alice", canonical)]  # one of m=2
    refusal = dispatch._round_ring_refusal(str(tmp_path), "approval", "kid",
                                           "", sigs)
    assert refusal is not None
    assert "approval" in refusal
    assert "got 1" in refusal


def test_dispatch_round_gate_satisfied_admits(tmp_path):
    """At m valid signatures the round is admitted (returns None)."""
    root, signers = _suite_grant_root(tmp_path)
    canonical = rings.canonical_bytes(
        "round-cut", dispatch._round_cut_fields("kid", "", "", "", 0))
    sigs = [_sig(signers, m, canonical) for m in ("alice", "bob")]
    assert dispatch._round_ring_refusal(str(tmp_path), "approval", "kid",
                                        "", sigs) is None


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
    fields_a = write._config_write_fields(
        "config:seats", {"seats": [{"name": "x"}]})
    canonical_a = rings.canonical_bytes("config-write", fields_a)
    sigs = [_sig(signers, m, canonical_a) for m in ("alice", "bob")]
    # record A is admitted by its OWN signatures...
    write._enforce_written_by(root, "config", "intruder", "config:seats",
                              set_fm={"seats": [{"name": "x"}]},
                              signatures=sigs, out_decision={})
    # ...a record B differing only in the seats field is REFUSED.
    with pytest.raises(write.EditError) as ei:
        write._enforce_written_by(root, "config", "intruder", "config:seats",
                                  set_fm={"seats": [{"name": "y"}]},
                                  signatures=sigs, out_decision={})
    assert "rung 2 multisig ring" in str(ei.value)


def test_config_write_decision_reverified_from_disk(tmp_path):
    """Claim (2) persistence (config-write seam): after the gate admits, the
    decision cell is captured and, written onto the node on disk (frontmatter),
    round-trips and RE-VERIFIES m-of-n from DISK (never argv). A tampered cell
    (one signature removed) reads short-of-m by name."""
    root, signers = _write_gate_root(tmp_path)
    fields = write._config_write_fields(
        "config:seats", {"seats": [{"name": "x"}]})
    canonical = rings.canonical_bytes("config-write", fields)
    sigs = [_sig(signers, m, canonical) for m in ("alice", "bob")]
    out: dict = {}
    write._enforce_written_by(root, "config", "intruder", "config:seats",
                              set_fm={"seats": [{"name": "x"}]},
                              signatures=sigs, out_decision=out)
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
    assert verification._ring_gate_refusal(
        root, "approval", "rotation", sigs) is None
    # level changed -> the same signatures no longer admit.
    assert verification._ring_gate_refusal(
        root, "approval", "full", sigs) is not None


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
    # the gate acting on iter 1 admits those signatures...
    assert dispatch._round_ring_refusal(
        str(tmp_path), "approval", "kid", "kid", sigs,
        target="nodeX", level="small", iter_n=1) is None
    # ...a round differing only in iter_n is REFUSED (short-of-m by name).
    refusal = dispatch._round_ring_refusal(
        str(tmp_path), "approval", "kid", "kid", sigs,
        target="nodeX", level="small", iter_n=2)
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
