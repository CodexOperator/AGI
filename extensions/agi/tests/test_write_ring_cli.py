"""write.py ring-gate AND semantics + full-decision bytes (kid C).

Covers hypothesis:l4-canonical-bytes-are-injective-and-fresh-and-the-ring-
gates-the-write-itself defects 1-3 and the acceptance tests A-G:

- A  an admitted writer, `ring:` schema, NO --ring-sig -> REFUSED naming the
     ring and the m-of-n count.
- B  same + m valid sigs -> admitted AND the persisted record carries the
     ring decision cell.
- C  a NOT-written_by writer + m valid sigs -> REFUSED by the written_by line
     (names admitted roles), never the ring line (today the ring admits it).
- D  a seated self-row write on a ring-declaring type, no sigs -> still
     admitted by the self_row path (ruling: the ring gates NON-self-row
     config writes; a seat may always update its own declared row).
- E  an unset_fm-ONLY non-self-row edit, no sigs -> REFUSED (the ring covers
     unset keys -- defect 1).
- F  a signature WITHOUT the unset key fails against a record that unsets it;
     one WITH it verifies (defect 1's falsifier).
- G  a set_fm `node` key cannot rename the signed record (id is under the
     reserved `_node` key, the caller's `node` lands elsewhere, both in the
     bytes); writing the reserved `_node` key is refused by name (defect 2).

Signing is the SAME seatsig fixture scheme test_rings.py registers, and the
members' pubkeys resolve from a fixture posts.md through write._ring_pubkey_
for_post -- never a real key, never live geometry. For the submit()-driven
end-to-end there is NO CLI seam to pin the gate's freshness nonce (kid D owns
that), so the test pins the nonce by monkeypatching seatsig.rings.secrets
and _now_iso to the SAME values it signed with -- the gate then builds
byte-identical fields in-process (see the KNOWN AND NOT YOURS section).
"""
from __future__ import annotations

import datetime
import hashlib
import sys
import time
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import write  # noqa: E402
import seatsig  # noqa: E402
from seatsig import get, register, Scheme  # noqa: E402
from seatsig import rings  # noqa: E402
import seatsig.rings as _rings  # noqa: E402


class _DummyScheme(Scheme):
    """Same fixture scheme test_rings.py registers (name `fixture`, hash-16)."""
    name = "fixture"

    def keygen(self, **kw):
        sk = b"k" * 32
        return sk, b"pub" + sk

    def sign(self, priv, msg):
        return hashlib.sha256(msg + priv).digest()[:16]

    def verify(self, pub, msg, sig):
        return sig == hashlib.sha256(msg + pub).digest()[:16]


register(_DummyScheme())


def _iso(t):
    return (datetime.datetime.fromtimestamp(t, datetime.timezone.utc)
            .strftime("%Y-%m-%dT%H:%M:%SZ"))


def _now() -> str:
    return _iso(time.time())


def _sigs(signers, canonical, posts):
    scheme = get("fixture")
    out = []
    for m in posts:
        out.append(f"{m}:fixture:{scheme.sign(signers[m], canonical).hex()}")
    return out


def _ring_root(tmp_path, written_by="prime", ring="approval",
               self_row=None, m=2):
    """A fixture graph root: a `config` schema declaring written_by / ring /
    self_row, a rings geometry cell, and posts.md carrying the members'
    pubkeys (what `_ring_pubkey_for_post` and `_load_seats` read)."""
    agi = tmp_path / ".agi"
    agi.mkdir(parents=True)
    (agi / "config.json").write_text("{}", encoding="utf-8")
    sd = agi / "context" / "schemas"
    sd.mkdir(parents=True)
    extra = ""
    if self_row:
        sr = ", ".join(f"{k}: {v}" for k, v in self_row.items())
        extra = f"self_row: {{{sr}}}"
    (sd / "[config].md").write_text(
        "---\ntype: config\n"
        f"written_by: {written_by or ''}\n"
        f"ring: {ring or ''}\n"
        f"{extra}\n---\n", encoding="utf-8")
    scheme = get("fixture")
    keys = {nm: scheme.keygen() for nm in ("alice", "bob", "carol")}
    pubkeys = {nm: priv.hex() for nm, (priv, _pub) in keys.items()}
    (agi / "nodes" / ".geometry").mkdir(parents=True)
    (agi / "nodes" / ".geometry" / "rings.md").write_text(
        "---\ntype: cell\nrings:\n"
        f"  - name: approval\n    m: {m}\n"
        "    members: [alice, bob, carol]\n---\n", encoding="utf-8")
    rows = "\n".join(
        f"  - name: {nm}\n    pubkey: {pubkeys[nm]}"
        for nm in ("alice", "bob", "carol"))
    (agi / "nodes" / ".geometry" / "posts.md").write_text(
        f"---\ntype: config\nposts:\n{rows}\n---\n", encoding="utf-8")
    signers = {nm: priv for nm, (priv, _pub) in keys.items()}
    return agi, signers


def _cell_fields(root, where, set_fm=None, unset_fm=None, ts=None, nonce=None):
    """The exact fresh fields a ring gate builds for this decision (sign side)."""
    return write._config_write_fields(where, set_fm, unset_fm,
                                      ts=ts, nonce=nonce)


def _pin_gate_freshness(monkeypatch, ts, nonce):
    """Make the in-process gate mint the SAME `_fresh` the signer covered, so
    a valid signature matches the gate's bytes (no CLI seam -- kid D)."""
    monkeypatch.setattr(_rings, "_now_iso", lambda: ts)
    monkeypatch.setattr(_rings.secrets, "token_hex", lambda n=16: nonce)


# ---------------------------------------------------------------------------
# A / B / C / E / F: gate-level, writing nothing, on the exact signed fields.
# ---------------------------------------------------------------------------

def test_A_admitted_writer_no_sigs_refused_naming_ring_and_count(tmp_path):
    """A (defect 3): an admitted writer on a `ring:` schema with NO signature
    is refused, and the refusal names the ring and the m-of-n count."""
    root, _s = _ring_root(tmp_path)
    with pytest.raises(write.EditError) as ei:
        write._enforce_written_by(
            root, "config", "director1", "config:seats", role="prime",
            set_fm={"seats": [{"name": "x"}]})
    msg = str(ei.value)
    assert "approval" in msg          # names the ring
    assert "rung 2 multisig ring" in msg
    assert "2" in msg                 # m-of-n count


def test_B_admitted_writer_with_quorum_admitted(tmp_path):
    """B: an admitted writer with m valid signatures over the exact fields is
    admitted (no refusal)."""
    root, signers = _ring_root(tmp_path)
    ts, nonce = _now(), "write-b"
    fields = _cell_fields(root, "config:seats",
                          {"seats": [{"name": "x"}]}, ts=ts, nonce=nonce)
    canonical = rings.canonical_bytes("config-write", fields)
    sigs = _sigs(signers, canonical, ["alice", "bob"])
    write._enforce_written_by(
        root, "config", "director1", "config:seats", role="prime",
        set_fm={"seats": [{"name": "x"}]}, signatures=sigs,
        ring_fresh=(ts, nonce))


def test_C_unadmitted_writer_with_quorum_refused_by_written_by(tmp_path):
    """C (defect 3): an UNADMITTED writer with m valid signatures is refused
    by the written_by line (names admitted roles), NEVER the ring line. Today
    the ring admits it -- this is the failing direction."""
    root, signers = _ring_root(tmp_path, written_by="prime")
    ts, nonce = _now(), "write-c"
    fields = _cell_fields(root, "config:seats",
                          {"seats": [{"name": "x"}]}, ts=ts, nonce=nonce)
    canonical = rings.canonical_bytes("config-write", fields)
    sigs = _sigs(signers, canonical, ["alice", "bob"])
    with pytest.raises(write.EditError) as ei:
        write._enforce_written_by(
            root, "config", "intruder", "config:seats",
            set_fm={"seats": [{"name": "x"}]}, signatures=sigs,
            ring_fresh=(ts, nonce))
    msg = str(ei.value)
    assert "hand-edited only by" in msg   # the written_by line
    assert "prime" in msg                 # names the admitted roles
    assert "rung 2" not in msg            # NOT the ring line


def test_E_unset_only_non_self_row_refused(tmp_path):
    """E (defect 1): an unset_fm-ONLY non-self-row edit is refused -- the ring
    gate covers unset keys, and with no signatures it names the quorum."""
    root, _s = _ring_root(tmp_path)
    with pytest.raises(write.EditError) as ei:
        write._enforce_written_by(
            root, "config", "director1", "config:seats", role="prime",
            unset_fm=["seats"])
    msg = str(ei.value)
    assert "approval" in msg
    assert "rung 2 multisig ring" in msg


def test_F_signature_without_unset_key_does_not_verify_against_unset(tmp_path):
    """F (defect 1 falsifier): the signed bytes must include an unset key, or
    a signature for a record WITHOUT it must not open a record that unsets it.
    A signature computed WITH the unset key must."""
    root, signers = _ring_root(tmp_path)
    ts, nonce = _now(), "write-f"
    # Sign the decision WITHOUT the unset key...
    fields_no_unset = _cell_fields(root, "config:seats",
                                   {"a": "1"}, ts=ts, nonce=nonce)
    canonical_no = rings.canonical_bytes("config-write", fields_no_unset)
    sigs_no = _sigs(signers, canonical_no, ["alice", "bob"])
    # ...and refuse it against a record that ALSO unsets `seats`: the quorum
    # over fields WITHOUT the key must NOT admit the unset edit.
    with pytest.raises(write.EditError) as ei:
        write._enforce_written_by(
            root, "config", "director1", "config:seats", role="prime",
            set_fm={"a": "1"}, unset_fm=["seats"],
            signatures=sigs_no, ring_fresh=(ts, nonce))
    assert "rung 2 multisig ring" in str(ei.value)
    # Sign WITH the unset key -> the same edit admits.
    fields_with_unset = _cell_fields(root, "config:seats",
                                     {"a": "1"}, ["seats"], ts=ts, nonce=nonce)
    canonical_with = rings.canonical_bytes("config-write", fields_with_unset)
    sigs_with = _sigs(signers, canonical_with, ["alice", "bob"])
    write._enforce_written_by(
        root, "config", "director1", "config:seats", role="prime",
        set_fm={"a": "1"}, unset_fm=["seats"],
        signatures=sigs_with, ring_fresh=(ts, nonce))


def test_G_node_key_cannot_rename_the_signed_record(tmp_path):
    """G (defect 2): a set_fm key literally named `node` cannot make the
    signed record name a different node. The id lives under the reserved
    `_node` key; the caller's `node` key lands SEPARATELY in the bytes -- both
    are covered -- and writing the reserved `_node` is refused by name."""
    root, _s = _ring_root(tmp_path)
    fields = write._config_write_fields(
        "config:seats", {"node": "config:OTHER"})
    assert fields[write.NODE_KEY] == "config:seats"   # the REAL node id
    assert fields["node"] == "config:OTHER"            # caller's key, separately
    # A signature over these bytes admits a decision naming config:seats.
    ts, nonce = _now(), "write-g"
    fields2 = _cell_fields(root, "config:seats", {"node": "config:OTHER"},
                           ts=ts, nonce=nonce)
    assert write.NODE_KEY in fields2 and "node" in fields2
    # Writing the reserved key is refused by name (fail-closed).
    with pytest.raises(write.EditError) as ei:
        write._config_write_fields("config:seats", {write.NODE_KEY: "evil"})
    assert "REFUSED" in str(ei.value)


# ---------------------------------------------------------------------------
# D: the seated self-row path admits WITHOUT the ring quorum.
# ---------------------------------------------------------------------------

def _seated_row_root(tmp_path):
    """written_by: prime, ring: approval, self_row on the (posts) row list;
    the actor `director1` is a seated post resolving to role `director`."""
    agi, signers = _ring_root(
        tmp_path, written_by="prime", ring="approval",
        self_row={"list_key": "seats", "match_key": "name",
                  "fields": "[]"})
    # director1 is a seated POST: give it a role (not prime -> not admitted by
    # written_by, so the self_row carve-out decides).
    rows = ("  - name: director1\n    role: director\n"
            "  - name: alice\n    role: prime\n"
            "  - name: bob\n    role: prime\n"
            "  - name: carol\n    role: prime\n")
    (agi / "nodes" / ".geometry" / "posts.md").write_text(
        f"---\ntype: config\nposts:\n{rows}\n---\n", encoding="utf-8")
    return agi


def test_D_seated_self_row_admitted_without_sigs(tmp_path):
    """D (ruling): a seated role updating its OWN declared row on a
    `ring:`-declaring type is admitted by the self_row path WITHOUT the ring
    quorum -- the ring gates NON-self-row config writes. (A self-row edit
    needs no quorum because the seat IS the identity already.)"""
    root = _seated_row_root(tmp_path)
    new_rows = ("  - name: director1\n    role: director\n"
                "  - name: alice\n    role: prime\n"
                "  - name: bob\n    role: prime\n"
                "  - name: carol\n    role: prime\n").strip()
    # byte-identical own-row reproduction, no declared-field delta ->
    # _self_row_refusal returns None -> admitted, never reaching the ring.
    set_fm = {"posts": [
        {"name": "director1", "role": "director"},
        {"name": "alice", "role": "prime"},
        {"name": "bob", "role": "prime"},
        {"name": "carol", "role": "prime"},
    ]}
    write._enforce_written_by(root, "config", "director1", "config:posts",
                              role="", set_fm=set_fm, allow_self_row=True)


# ---------------------------------------------------------------------------
# submit()-driven end-to-end on a REAL tmp-root node: one admitted (valid
# quorum, byte-identical fields via pinned freshness) and one short-of-m
# refused. No CLI seam (kid D), so the test drives write.submit in-process.
# ---------------------------------------------------------------------------

def _real_node(tmp_path):
    """A real config node at nodes/posts.md with a mint_id, targeting `where`."""
    (tmp_path / "nodes").mkdir(parents=True, exist_ok=True)
    (tmp_path / "nodes" / "posts.md").write_text(
        "---\nid: config:posts\ntype: config\nmint_id: cfgtst001\n"
        "title: posts\n---\n\nbody\n", encoding="utf-8")


def test_submit_end_to_end_admitted_with_cell(tmp_path, monkeypatch):
    """An admitted writer with a valid quorum mutates a REAL node and the
    persisted frontmatter carries the ring decision cell (re-verified from
    disk, no argv)."""
    root, signers = _ring_root(tmp_path, written_by="prime", ring="approval")
    _real_node(root)
    ts, nonce = _now(), "e2e-admit"
    fields = _cell_fields(root, "config:posts",
                          {"posts": [{"name": "x"}]}, ts=ts, nonce=nonce)
    canonical = rings.canonical_bytes("config-write", fields)
    sigs = _sigs(signers, canonical, ["alice", "bob"])
    # Make the gate mint the SAME fresh fields the signer covered.
    _pin_gate_freshness(monkeypatch, ts, nonce)
    edit = write.Edit("config:posts")
    edit.set_fm["posts"] = [{"name": "x"}]
    edit.signatures = sigs
    res = write.submit(root, edit, actor="director1", role="prime")
    assert "updated" in str(res.status)
    (root / "nodes" / "posts.md").read_text()
    # Re-verify the persisted cell m-of-n from DISK, no argv.
    from graph_core.persistence import frontmatter as _fm  # noqa: PLC0415
    nf = _fm.load_node_file(root / "nodes" / "posts.md")
    ring = rings.ring_by_name(rings.load_rings(root), "approval")
    assert rings.verify_decision(
        nf.frontmatter["ring_decision"], ring,
        pubkey_for_post=write._ring_pubkey_for_post(root)).ok is True


def test_submit_end_to_end_short_of_m_refused(tmp_path, monkeypatch):
    """Write.py ring path end-to-end: one valid signature of m=2 is refused
    short-of-m by name through write.submit (nothing persists)."""
    root, signers = _ring_root(tmp_path, written_by="prime", ring="approval")
    _real_node(root)
    ts, nonce = _now(), "e2e-short"
    fields = _cell_fields(root, "config:posts",
                          {"posts": [{"name": "x"}]}, ts=ts, nonce=nonce)
    canonical = rings.canonical_bytes("config-write", fields)
    sigs = _sigs(signers, canonical, ["alice"])          # one of m=2
    _pin_gate_freshness(monkeypatch, ts, nonce)
    edit = write.Edit("config:posts")
    edit.set_fm["posts"] = [{"name": "x"}]
    edit.signatures = sigs
    with pytest.raises(write.EditError) as ei:
        write.submit(root, edit, actor="director1", role="prime")
    assert "approval" in str(ei.value)
    assert "got 1" in str(ei.value)
    assert "ring_decision" not in (root / "nodes" / "posts.md").read_text()