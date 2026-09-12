"""Tests for seatsig.veto -- the rung-3 HUMAN GATE (hypothesis:l4-a-veto-
freezes-never-frees).

Proves on FIXTURE keys, on a fake geometry dict / a tmp geometry node (the
real posts/seats tree is read, never written): a MAJORITY (council+Keep
quorum) veto GATES; a MINORITY does not; an EXPIRED veto is INERT; the rate
limit REFUSES the N+1th; and an UNANSWERED gate stays FROZEN across a
simulated rotation. The veto quorum routes through rings.verify_decision --
the SAME seatsig interface -- never the veto module's own crypto.
"""

from __future__ import annotations

import os
import tempfile
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

import seatsig  # noqa: F401  (guarantees the engine spelling, mur-39 (e))
from seatsig import register, Scheme, get  # noqa: F401
from seatsig import rings
from seatsig import veto


class _DummyScheme(Scheme):
    """Fixture scheme (same shape as test_rings'): cheap sign/verify so the
    quorum check is exercised through the registry without the real crypto.
    The veto still verifies through seatsig.get() exactly like ed25519."""

    name = "fixture"

    def keygen(self):
        priv = os.urandom(8)
        return priv, priv

    def sign(self, priv, msg):
        import hashlib

        return hashlib.sha256(msg + priv).digest()[:16]

    def verify(self, pub, msg, sig):
        import hashlib

        return sig == hashlib.sha256(msg + pub).digest()[:16]


register(_DummyScheme())


@pytest.fixture(scope="module")
def council_and_keep():
    """A council+Keep ring: two council posts + a Keep seat, threshold 2
    (a majority). Keys resolve through a fixture mapping."""
    scheme = get("fixture")
    members = ("council-core", "council-streaming-suite", "keep-prime")
    keys = {m: scheme.keygen() for m in members}
    ring = {"name": "council-and-keep", "m": 2, "members": list(members)}
    pubkeys = {m: priv.hex() for m, (priv, _pub) in keys.items()}
    signers = {m: priv for m, (priv, _pub) in keys.items()}

    def resolve(post):
        return pubkeys.get(post)

    return locals()


def _veto_cell(ck, scope, reason="council majority deep-freeze",
               expires_at=None, signers=("council-core", "keep-prime")):
    """A signed veto DECISION CELL (rings shape, kind 'veto') over the FULL
    veto fields, signed by the given members (a majority by default)."""
    fields = veto.veto_fields(scope, reason, expires_at)
    canonical = rings.canonical_bytes("veto", fields)
    sigs = []
    for post in signers:
        if post not in ck["signers"]:
            continue
        scheme = get("fixture")
        sigs.append(
            f"{post}:fixture:{scheme.sign(ck['signers'][post], canonical).hex()}")
    return rings.decision_cell(
        "council-and-keep", "veto", fields, sigs)


@pytest.fixture
def geom():
    """A fresh fake VETOES geometry dict: limit 2/window, expiry 86400s,
    no gates yet, empty log."""
    return {
        "veto_room": "veto",
        "rate_limit_per_window": 2,
        "window_seconds": 3600,
        "expiry_seconds": 86400,
        "active_gates": [],
        "vetoes": [],
    }


# ---- claim (4) case 1: a MAJORITY veto GATES --------------------------
def test_majority_veto_gates(council_and_keep, geom):
    """2-of-3 council+Keep majority -> the veto is ACCEPTED and the scope
    becomes FROZEN (a human gate is set, unanswered)."""
    cell = _veto_cell(council_and_keep, "prime",
                      reason="merge-up push over the prime's own scope")
    refusal, new = veto.evaluate_veto(
        geom, "prime", cell, ring=council_and_keep["ring"],
        pubkey_for_post=council_and_keep["resolve"])
    assert refusal is None
    frozen, why = veto.is_frozen(None, "prime", geom=new)
    assert frozen is True
    assert "FROZEN" in why
    assert len(new["vetoes"]) == 1
    active = new["active_gates"][0]
    assert active["scope"] == "prime"
    assert active["answered"] == ""  # unanswered -> still frozen


# ---- claim (4) case 2: a MINORITY does NOT gate -----------------------
def test_minority_does_not_gate(council_and_keep, geom):
    """1-of-3 -> short of quorum -> refused by name, nothing frozen."""
    cell = _veto_cell(council_and_keep, "prime",
                      signers=("council-core",))  # ONE member = minority
    refusal, new = veto.evaluate_veto(
        geom, "prime", cell, ring=council_and_keep["ring"],
        pubkey_for_post=council_and_keep["resolve"])
    assert refusal is not None
    assert "minority" in refusal
    frozen, _why = veto.is_frozen(None, "prime", geom=new)
    assert frozen is False
    assert new["active_gates"] == []


# ---- claim (4) case 3: an EXPIRED veto is INERT -----------------------
def test_expired_veto_inert(council_and_keep, geom):
    """A veto whose authority window (expires_at) has passed cannot set a
    gate -- even with a full majority behind it."""
    past = "2000-01-01T00:00:00Z"
    cell = _veto_cell(council_and_keep, "prime", expires_at=past)
    refusal, new = veto.evaluate_veto(
        geom, "prime", cell, ring=council_and_keep["ring"],
        pubkey_for_post=council_and_keep["resolve"], now=None)
    assert refusal is not None
    assert "expired" in refusal and "inert" in refusal
    frozen, _why = veto.is_frozen(None, "prime", geom=new)
    assert frozen is False


# ---- claim (4) case 4: the rate limit refuses the (N+1)th ------------
def test_rate_limit_refuses_n_plus_1(council_and_keep, geom):
    """Two vetoes per window are allowed; the THIRD is refused by name."""
    # first veto accepted
    c1 = _veto_cell(council_and_keep, "prime", reason="first")
    refusal, new1 = veto.evaluate_veto(
        geom, "prime", c1, ring=council_and_keep["ring"],
        pubkey_for_post=council_and_keep["resolve"])
    assert refusal is None
    # second accepted
    c2 = _veto_cell(council_and_keep, "prime", reason="second")
    refusal, new2 = veto.evaluate_veto(
        new1, "prime", c2, ring=council_and_keep["ring"],
        pubkey_for_post=council_and_keep["resolve"])
    assert refusal is None
    # third refused
    c3 = _veto_cell(council_and_keep, "prime", reason="third")
    refusal, new3 = veto.evaluate_veto(
        new2, "prime", c3, ring=council_and_keep["ring"],
        pubkey_for_post=council_and_keep["resolve"])
    assert refusal is not None
    assert "rate-limited" in refusal and "3" in refusal
    frozen, _why = veto.is_frozen(None, "prime", geom=new3)
    assert frozen is True  # the freeze from veto 1/2 holds


# ---- claim (4) case 5: an unanswered gate stays FROZEN across a
#      simulated rotation ---------------------------------------------
def test_unanswered_gate_stays_frozen_across_rotation(council_and_keep, geom):
    """The freeze lives in the shared VETOES node, not in an actor/pid, so
    simulating a rotation (a NEW actor re-reading the SAME node) must still
    see the scope frozen. Nothing but an owner answer clears it. Also:
    writing the accepted geometry to a tmp VETOES node and re-reading it
    through veto.read() round-trips the freeze."""
    cell = _veto_cell(council_and_keep, "prime", reason="freeze through rotation")
    refusal, accepted = veto.evaluate_veto(
        geom, "prime", cell, ring=council_and_keep["ring"],
        pubkey_for_post=council_and_keep["resolve"])
    assert refusal is None

    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        path = Path("nodes") / ".geometry" / "vetoes.md"
        veto.save(root, accepted, path)
        # ... and a RESTART (fresh VETOES module state) re-reads the node.
        reloaded = veto.read(root, path)
    # a rotation is a NEW actor with the same shared state:
    frozen, why = veto.is_frozen(None, "prime", geom=reloaded)
    assert frozen is True
    assert "rotation" not in why  # the freeze is not actor-lifetime scoped

    # the ONLY release is an owner answer:
    freed = veto.record_answer(reloaded, "prime", "owner: understood, cleared")
    frozen, _why = veto.is_frozen(None, "prime", geom=freed)
    assert frozen is False
    # and the log carries the whole lifecycle (filed -> answered):
    assert any(v.get("answer") for v in freed["vetoes"])


# ---- the freeze is scope-scoped: another scope is not caught ----------
def test_freeze_is_scope_scoped(council_and_keep, geom):
    """A gate on one scope does not freeze a different scope."""
    cell = _veto_cell(council_and_keep, "prime")
    refusal, new = veto.evaluate_veto(
        geom, "prime", cell, ring=council_and_keep["ring"],
        pubkey_for_post=council_and_keep["resolve"])
    assert refusal is None
    frozen_other, _why = veto.is_frozen(None, "sanctuary-director", geom=new)
    assert frozen_other is False


# ---- a VETOES cell that declares nothing gates nothing (opt-in) -------
def test_no_ring_no_veto_gates_nothing(council_and_keep, geom):
    """A veto with NO ring (opt-in) cannot set a gate -- refused by name."""
    cell = rings.decision_cell("nope", "veto", {"scope": "prime"}, [])
    refusal, new = veto.evaluate_veto(
        geom, "prime", cell, ring=None,
        pubkey_for_post=council_and_keep["resolve"])
    assert refusal is not None
    assert "no council+Keep ring" in refusal
    frozen, _why = veto.is_frozen(None, "prime", geom=new)
    assert frozen is False

# ---- the NAMED-ROOM wire (send.py `veto` verb, claim (1)&(2)) --------
# The owner-answer path is the wire surface an owner RELEASES a frozen scope
# through: `send.py veto --scope X --answer "..."`. It posts the owner line to
# the named veto_room AND writes the answered record back into the ONE
# geometry log (veto.record_answer -> veto.save). Proved on a tmp graph root
# and tmp comms root; the real tree is read, never written.
_BIN = Path(__file__).resolve().parents[1] / "bin"


def _load_send():
    import importlib.util
    import sys as _sys

    if str(_BIN) not in _sys.path:
        _sys.path.insert(0, str(_BIN))
    import locations  # noqa: F401  (resolves through BIN)
    spec = importlib.util.spec_from_file_location("send", _BIN / "send.py")
    send_m = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(send_m)
    return send_m


def _frozen_geom():
    """A VETOES geometry dict with an ACTIVE (unanswered) `prime` gate."""
    return {
        "veto_room": "veto",
        "rate_limit_per_window": 2,
        "window_seconds": 3600,
        "expiry_seconds": 86400,
        "active_gates": [{"scope": "prime", "since": "2026-09-12T00:00:00Z",
                          "reason": "council veto", "veto_ref": "veto:001",
                          "answered": ""}],
        "vetoes": [{"veto_ref": "veto:001", "scope": "prime",
                    "filed_at": "2026-09-12T00:00:00Z",
                    "expires_at": "2026-09-12T00:00:00Z", "answer": ""}],
    }


def test_send_veto_helpers_status_and_answer(tmp_path, monkeypatch):
    """The `veto` verb's two helpers: status reports the freeze by name, and
    an OWNER ANSWER is the ONLY release -- it clears the gate and logs the
    whole filed->frozen->answered lifecycle into the ONE geometry file."""
    send = _load_send()
    root = tmp_path / "graph"
    root.mkdir(parents=True, exist_ok=True)
    # pin the verb's graph-root resolution to the tmp graph (main identity)
    monkeypatch.setattr(send, "_main_graph_root", lambda r: r)

    from seatsig import veto as _veto
    cell = Path("nodes") / ".geometry" / "vetoes.md"
    _veto.save(root, _frozen_geom(), cell)

    status = send.veto_gate_status(root, "prime")
    assert "GATE-FROZEN" in status and "prime" in status

    out = send.veto_answer(root, "prime", "owner: understood, cleared")
    assert "ANSWERED" in out
    reloaded = _veto.read(root, cell)
    frozen, _why = _veto.is_frozen(None, "prime", geom=reloaded)
    assert frozen is False
    assert any(v.get("answer") for v in reloaded["vetoes"])  # logged
    assert all(g.get("answered") for g in reloaded["active_gates"])

    # answering a scope with no gate is a named no-op, never a crash
    out2 = send.veto_answer(root, "sanctuary-director", "owner: n/a")
    assert "not under an active gate" in out2


def test_send_veto_verb_cli_posts_room_and_releases(tmp_path, monkeypatch):
    """`send.py veto --scope prime --answer ...` (the real CLI dispatch): the
    gate is released in the geometry log AND the owner line lands in the
    named veto_room comms file."""
    send = _load_send()
    root = tmp_path / "graph"
    root.mkdir(parents=True, exist_ok=True)
    croot = tmp_path / "comms"
    monkeypatch.setattr(send, "_main_graph_root", lambda r: r)
    monkeypatch.setattr(send, "_project_root", lambda: root)

    from seatsig import veto as _veto
    cell = Path("nodes") / ".geometry" / "vetoes.md"
    _veto.save(root, _frozen_geom(), cell)

    rc = send.main(["veto", "--scope", "prime", "--answer", "owner: ok",
                    "--comms-root", str(croot), "--from", "owner"])
    assert rc == 0

    reloaded = _veto.read(root, cell)
    frozen, _why = _veto.is_frozen(None, "prime", geom=reloaded)
    assert frozen is False

    room = croot / "room" / "veto.md"
    assert room.is_file()
    assert "owner: ok" in room.read_text()


# ---- RUNG 3 claim (1)+(3): a rotation of ANOTHER post is GATED ---------
# A rotation whose target seat is not the caller's OWN post (self_row) is a
# GATED Prime-scope act: while the prime scope is FROZEN it is refused BY
# NAME and never auto-released. The freeze is carried IN THE ROTATION RECORD
# (claim (3)) so a reader sees scope+why without asking `viewport --live`.
# Both conjuncts are exercised on tmp roots (the real tree is read, never
# written), through the helper seam AND the real `cmd_rotate_self` dispatch.
_BIN_ROT = Path(__file__).resolve().parents[1] / "bin"


def _load_rotate():
    import importlib.util
    import sys as _sys

    if str(_BIN_ROT) not in _sys.path:
        _sys.path.insert(0, str(_BIN_ROT))
    import locations  # noqa: F401
    spec = importlib.util.spec_from_file_location("rotate", _BIN_ROT / "rotate.py")
    rot = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(rot)
    return rot


def _write_rot_vetoes(root, geom):
    """Put a frozen-gate VETOES geometry node at `<root>/nodes/.geometry/`,
    the path `_shared_graph_root` resolves on a bare fixture root."""
    from seatsig import veto as _veto
    cell = Path("nodes") / ".geometry" / "vetoes.md"
    _veto.save(root, geom, cell)
    return cell


def test_rotate_helper_gates_another_post_not_self(council_and_keep, geom,
                                                   tmp_path, monkeypatch):
    """The `_rotate_human_gate` seam: with the prime scope FROZEN, rotating
    ANOTHER post is refused by name, but rotating the caller's OWN post
    (self_row) is NEVER gated; with the scope FREE no rotation is gated."""
    rot = _load_rotate()
    root = tmp_path / "graph"
    root.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("AGI_SEAT", "adv-alive")  # the caller's own post

    # frozen prime scope
    cell = _write_rot_vetoes(root, _frozen_geom())
    _ = cell
    # another post -> gated
    held, freeze = rot._rotate_human_gate(root, "other-post")
    assert held is not None and "HELD" in held
    assert "another post" in held
    assert freeze["scope"] == "prime"
    assert "FROZEN" in freeze["hold_reason"]
    assert freeze["auto_released"] is False
    # the caller's OWN post -> never gated (self_row carve-out)
    held2, freeze2 = rot._rotate_human_gate(root, "adv-alive")
    assert held2 is None and freeze2 is None

    # a FREE scope gates nothing -- another post rotates freely
    free = dict(geom)
    free["active_gates"] = []
    free["vetoes"] = []
    cell3 = _write_rot_vetoes(root, free)
    _ = cell3
    held3, freeze3 = rot._rotate_human_gate(root, "other-post")
    assert held3 is None and freeze3 is None


def test_rotate_holds_another_post_record_carries_freeze(tmp_path, monkeypatch,
                                                        capsys):
    """The wired `cmd_rotate_self` path: with the prime scope FROZEN, a
    rotation of ANOTHER post exits 3 (HELD-by-name, stderr) and writes a
    durable ROTATION RECORD whose `human_gate` block carries the freeze
    (scope + why) -- so the record alone tells a reader the rotation was
    held, never auto-released."""
    rot = _load_rotate()
    root = tmp_path / "graph"
    root.mkdir(parents=True, exist_ok=True)
    monkeypatch.setenv("AGI_SEAT", "belam")  # caller is the prime; target is not
    _write_rot_vetoes(root, _frozen_geom())

    args = SimpleNamespace(name="other-post", prepare=False)
    rc = rot.cmd_rotate_self(args, root)
    assert rc == 3
    err = capsys.readouterr().err
    assert "HELD" in err and "another post" in err

    recs = list((root / "sessions" / "rotations").glob("other-post.*.json"))
    assert recs, "a HELD rotation writes a durable rotation record"
    rec = json.loads(recs[0].read_text())
    assert rec["result"] == "held"
    hg = rec["human_gate"]
    assert hg["scope"] == "prime"
    assert "FROZEN" in hg["hold_reason"]
    assert hg["auto_released"] is False
    assert rec["refusal_reason"].startswith("rotation: HELD")

