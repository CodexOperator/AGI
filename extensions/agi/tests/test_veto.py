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


def _owner_row(owner="owner", role="owner"):
    """A keyed config:posts row whose signature the answer must verify over.
    Uses the registered fixture scheme (no real crypto) -- same shape
    send.py's ``_verify_block``/``_row_for_label`` read."""
    scheme = get("fixture")
    priv, _pub = scheme.keygen()
    return {**{"name": owner, "role": role, "pubkey": priv.hex(),
               "sig_scheme": "fixture"}, "_priv": priv}


def _signed_answer(priv, text="owner: understood, cleared",
                   from_id="owner", to="veto", ts="2026-09-12T00:00:00Z"):
    """A dm-style signed answer block (ts/from/to/sig + body) over the SAME
    canonical bytes send.py's ``_canonical_msg`` covers."""
    msg = f"{ts}\n{from_id}\n{to}\n\n{text}".encode()
    sig = get("fixture").sign(priv, msg).hex()
    return (f"ts: {ts}\nfrom: {from_id}\nto: {to}\n"
            f"sig: fixture:owner:{sig}\n\n{text}")


def test_send_veto_helpers_status_and_answer(tmp_path, monkeypatch):
    """The `veto` verb's two helpers: status reports the freeze by name; an
    UNSIGNED or NON-OWNER answer is REFUSED BY NAME (frees nothing); and an
    OWNER-role SIGNED answer is the ONLY release -- it clears the gate and
    logs the whole filed->frozen->answered lifecycle into the ONE geometry
    file (defect 1e, hypothesis:l4-...gate-sits-on-the-merge-up-push)."""
    send = _load_send()
    root = tmp_path / "graph"
    root.mkdir(parents=True, exist_ok=True)
    # pin the verb's graph-root resolution to the tmp graph (main identity)
    monkeypatch.setattr(send, "_main_graph_root", lambda r: r)
    owner = _owner_row()
    nonowner = _owner_row("other", "director")
    monkeypatch.setattr(send, "_load_rows", lambda r: [owner, nonowner])

    from seatsig import veto as _veto
    cell = Path("nodes") / ".geometry" / "vetoes.md"
    _veto.save(root, _frozen_geom(), cell)

    status = send.veto_gate_status(root, "prime")
    assert "GATE-FROZEN" in status and "prime" in status

    # (a) an UNSIGNED answer is refused by name and frees nothing
    unsigned = send.veto_answer(root, "prime", "owner: understood, cleared")
    assert "REFUSED" in unsigned and "UNSIGNED" in unsigned
    assert _veto.is_frozen(None, "prime", geom=_veto.read(root, cell))[0] is True

    # (b) a signed NON-OWNER answer is refused by name and frees nothing
    non_owner_block = _signed_answer(
        nonowner["_priv"], text="other: understood", from_id="other")
    refused = send.veto_answer(root, "prime", non_owner_block)
    assert "REFUSED" in refused and "OWNER-role" in refused
    assert _veto.is_frozen(None, "prime", geom=_veto.read(root, cell))[0] is True

    # (c) an OWNER signed answer is the ONE release
    block = _signed_answer(owner["_priv"])
    out = send.veto_answer(root, "prime", block)
    assert "ANSWERED" in out
    reloaded = _veto.read(root, cell)
    frozen, _why = _veto.is_frozen(None, "prime", geom=reloaded)
    assert frozen is False
    assert any(v.get("answer") for v in reloaded["vetoes"])  # logged
    assert all(g.get("answered") for g in reloaded["active_gates"])

    # answering a scope with no gate is a named no-op, never a crash
    out2 = send.veto_answer(root, "sanctuary-director", block)
    assert "not under an active gate" in out2


def test_send_veto_verb_cli_posts_room_and_releases(tmp_path, monkeypatch):
    """`send.py veto --scope prime --answer <signed-block>` (the real CLI
    dispatch): the OWNER-signed answer releases the gate in the geometry log
    AND the owner line lands in the named veto_room comms file; an UNSIGNED
    answer exits 3 and leaves the gate frozen."""
    send = _load_send()
    root = tmp_path / "graph"
    root.mkdir(parents=True, exist_ok=True)
    croot = tmp_path / "comms"
    monkeypatch.setattr(send, "_main_graph_root", lambda r: r)
    monkeypatch.setattr(send, "_project_root", lambda: root)
    owner = _owner_row()
    monkeypatch.setattr(send, "_load_rows", lambda r: [owner])

    from seatsig import veto as _veto
    cell = Path("nodes") / ".geometry" / "vetoes.md"
    _veto.save(root, _frozen_geom(), cell)

    block = _signed_answer(owner["_priv"], text="owner: ok")
    rc = send.main(["veto", "--scope", "prime", "--answer", block,
                    "--comms-root", str(croot), "--from", "owner"])
    assert rc == 0

    reloaded = _veto.read(root, cell)
    frozen, _why = _veto.is_frozen(None, "prime", geom=reloaded)
    assert frozen is False

    room = croot / "room" / "veto.md"
    assert room.is_file()
    assert "owner: ok" in room.read_text()

    # an UNSIGNED answer exits non-zero and leaves the gate frozen
    _veto.save(root, _frozen_geom(), cell)
    rc_bad = send.main(["veto", "--scope", "prime",
                        "--answer", "owner: nope",
                        "--comms-root", str(croot), "--from", "owner"])
    assert rc_bad != 0
    assert _veto.is_frozen(None, "prime", geom=_veto.read(root, cell))[0] is True


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



# ---- kid B: FRESHNESS on a ring-authorized veto (opt-in) ----------------
def _veto_cell_fresh(ck, scope, reason, ts, nonce):
    """A signed veto DECISION CELL whose fields carry the reserved `_fresh`
    (ts|nonce) -- a producer opting into a finite signature-replay life."""
    import time as _time
    from seatsig import rings
    base = veto.veto_fields(scope, reason)
    fields = rings.fresh_fields(base, ts=ts, nonce=nonce)
    canonical = rings.canonical_bytes("veto", fields)
    sigs = []
    for post in ("council-core", "keep-prime"):
        scheme = get("fixture")
        sigs.append(
            f"{post}:fixture:{scheme.sign(ck['signers'][post], canonical).hex()}")
    return rings.decision_cell("council-and-keep", "veto", fields, sigs)


def test_veto_fresh_fields_opt_in_admits(council_and_keep, geom):
    """A veto decision carrying a FRESH `_fresh` is accepted (the opt-in
    read-side guard is a no-op on a within-window fresh veto)."""
    import time as _time
    from seatsig import rings
    cell = _veto_cell_fresh(
        council_and_keep, "prime", "opt-in fully scripted",
        ts=rings._now_iso(), nonce="vnow1")
    refusal, new = veto.evaluate_veto(
        geom, "prime", cell, ring=council_and_keep["ring"],
        pubkey_for_post=council_and_keep["resolve"])
    assert refusal is None
    assert len(new["active_gates"]) == 1


def test_veto_fresh_stale_refused_by_name(council_and_keep, geom):
    """A veto decision carrying a STALE `_fresh` (past its replay window) is
    refused BY NAME on freshness -- it can neither set a gate nor log."""
    import time as _time
    from seatsig import rings
    stale_ts = rings._now_iso()  # would be a real old ts below; use far past:
    from datetime import datetime, timedelta, timezone
    stale_ts = (datetime.now(timezone.utc) - timedelta(seconds=5000)
                ).strftime("%Y-%m-%dT%H:%M:%SZ")
    cell = _veto_cell_fresh(
        council_and_keep, "prime", "stale fresh", ts=stale_ts, nonce="vold1")
    refusal, new = veto.evaluate_veto(
        geom, "prime", cell, ring=council_and_keep["ring"],
        pubkey_for_post=council_and_keep["resolve"])
    assert refusal is not None
    assert "freshness" in refusal
    assert "stale" in refusal
      # nothing froze, nothing logged
    assert new["active_gates"] == []
    assert new["vetoes"] == []


# ---- DEFECT 5 (hypothesis:l4-...gate-sits-on-the-merge-up-push) --------
# save() round-trips the node BODY and writes EMPTY lists as `[]` (never YAML
# null), and the FILED veto's logged expires_at is the EFFECTIVE expiry
# (the once-dead `_effective_expiry` is actually called on the filing path) --
# never the bare filing instant.
def test_save_round_trips_empty_lists_and_body(tmp_path):
    """save() writes `active_gates`/`vetoes` empty lists as `[]` (never YAML
    null, which re-read as None and silently erased the opt-in state) and
    preserves an authored node BODY byte-for-byte across a save."""
    root = tmp_path
    p = Path("nodes") / ".geometry" / "vetoes.md"
    (root / p).parent.mkdir(parents=True, exist_ok=True)
    cell = root / p
    cell.write_text(
        "---\nid: config:vetoes\ntype: config\nactive_gates:\n---\n\n"
        "# config:vetoes\n\nfixture body line one\nbody line two\n")
    geom = {"veto_room": "veto", "rate_limit_per_window": 2,
            "window_seconds": 3600, "expiry_seconds": 86400,
            "active_gates": [], "vetoes": []}
    veto.save(root, geom, p)
    text = cell.read_text()
    assert "active_gates: []" in text and "vetoes: []" in text
    assert "fixture body line one\nbody line two" in text  # body preserved
    reloaded = veto.read(root, p)
    assert reloaded["active_gates"] == []
    assert reloaded["vetoes"] == []


def test_filed_veto_logs_effective_expiry(council_and_keep):
    """The LOGGED expires_at on the filing path is the EFFECTIVE expiry (now +
    expiry_seconds for a veto with no explicit window) -- so `_effective_expiry`
    is actually called -- never the bare filing instant."""
    import datetime as _dt

    geom = {"veto_room": "veto", "rate_limit_per_window": 2,
            "window_seconds": 3600, "expiry_seconds": 86400,
            "active_gates": [], "vetoes": []}
    now = _dt.datetime(2026, 9, 12, 0, 0, 0, tzinfo=_dt.timezone.utc)
    cell = _veto_cell(council_and_keep, "prime", reason="expiry window")
    refusal, new = veto.evaluate_veto(geom, "prime", cell,
                                      ring=council_and_keep["ring"],
                                      pubkey_for_post=council_and_keep["resolve"],
                                      now=now)
    assert refusal is None
    logged = new["vetoes"][0]
    assert logged["expires_at"] != logged["filed_at"]  # NOT the filing time
    exp = veto._parse_iso(logged["expires_at"])
    expect = now + _dt.timedelta(seconds=86400)
    assert abs((exp - expect).total_seconds()) < 2


# ---- DEFECT 1a: `evaluate_veto` has a real (non-test) caller -- the
# `veto ==file` wire in send.py files a council+Keep decision cell through it.
def test_veto_file_is_non_test_evaluate_caller(tmp_path, monkeypatch,
                                               council_and_keep):
    """send.veto_file is the one NON-TEST caller of evaluate_veto: filing a
    council+Keep majority decision cell through the `veto --file` wire sets
    the human gate; a NO-RING decision gates nothing."""
    send = _load_send()
    root = tmp_path / "graph"
    root.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(send, "_main_graph_root", lambda r: r)

    posts = root / "nodes" / ".geometry"
    posts.mkdir(parents=True, exist_ok=True)
    rows = [{"name": m, "role": "member",
             "pubkey": council_and_keep["pubkeys"][m]}
            for m in council_and_keep["members"]]
    (posts / "posts.md").write_text(
        "---\nid: config:posts\ntype: config\nposts:\n" +
        "\n".join(f"  - {r!r}" for r in rows) + "\n---\n")
    ring = council_and_keep["ring"]
    (posts / "rings.md").write_text(
        "---\nid: config:rings\ntype: config\nrings:\n"
        f"  - {ring!r}\n---\n")

    cell = _veto_cell(council_and_keep, "prime", reason="majority freeze")
    out = send.veto_file(root, "prime", cell)
    assert "FILED" in out
    cell_path = Path("nodes") / ".geometry" / "vetoes.md"
    _frozen, _why = veto.is_frozen(None, "prime", geom=veto.read(root, cell_path))
    assert _frozen is True

    # a NO-RING decision (opt-in) gates nothing -- refused by name
    free = {"veto_room": "veto", "rate_limit_per_window": 2,
            "window_seconds": 3600, "expiry_seconds": 86400,
            "active_gates": [], "vetoes": []}
    veto.save(root, free, cell_path)
    poison = rings.decision_cell("nope", "veto", {"scope": "prime"}, [])
    out2 = send.veto_file(root, "prime", poison)
    assert "REFUSED" in out2
    _frozen2, _why2 = veto.is_frozen(None, "prime", geom=veto.read(root, cell_path))
    assert _frozen2 is False


# ---- DEFECT 1b: the MERGE-UP push is a GATED Prime-scope act. A FROZEN
# prime scope refuses `_stops_push(root, label="merge")` by name
# (`push: HELD -- ...`); an UNFROZEN merge-up push passes (reaches the real
# push layer and returns None, never a HELD line).
def test_rotate_merge_up_push_gated_when_frozen(tmp_path, monkeypatch, capsys):
    rot = _load_rotate()
    root = tmp_path / "graph"
    root.mkdir(parents=True, exist_ok=True)

    # frozen prime scope -> refused by name exactly like the spawn own-row leg
    _write_rot_vetoes(root, _frozen_geom())
    held = rot._stops_push(root, label="merge")
    assert held is not None and held.startswith("push: HELD")
    assert "merge-up push is a gated act" in held
    capsys.readouterr()  # flush the HELD line so the frozen leg does not leak

    # unfrozen -> the merge-up push proceeds (git layer faked to a success)
    # and returns None; NEVER a HELD line.
    (root / "nodes" / ".geometry" / "vetoes.md").unlink()

    def fake_run(cmd, **kw):
        class _R:
            def __init__(s, rc, out=""):
                s.returncode, s.stdout, s.stderr = rc, out, ""
        if "--show-toplevel" in cmd:
            return _R(0, str(root) + "\n")
        if "--abbrev-ref" in cmd:
            return _R(0, "main\n")
        return _R(0)

    monkeypatch.setattr(rot.subprocess, "run", fake_run)
    res = rot._stops_push(root, label="merge")
    assert res is None
    err = capsys.readouterr().err
    assert "merge push: OK" in err
    assert "HELD" not in err


def test_veto_answer_accepts_ring_decision(tmp_path, monkeypatch,
                                           council_and_keep):
    """defect 1e: an answer may also be a valid ring DECISION (rung 2b) -- a
    scope-matching council+Keep decision cell verified through the declared
    ring clears the gate; a minority / wrong-scope decision refuses by name."""
    send = _load_send()
    root = tmp_path / "graph"
    root.mkdir(parents=True, exist_ok=True)
    monkeypatch.setattr(send, "_main_graph_root", lambda r: r)
    posts = root / "nodes" / ".geometry"
    posts.mkdir(parents=True, exist_ok=True)
    rows = [{"name": m, "role": "member",
             "pubkey": council_and_keep["pubkeys"][m]}
            for m in council_and_keep["members"]]
    (posts / "posts.md").write_text(
        "---\nid: config:posts\ntype: config\nposts:\n" +
        "\n".join(f"  - {r!r}" for r in rows) + "\n---\n")
    ring = council_and_keep["ring"]
    (posts / "rings.md").write_text(
        "---\nid: config:rings\ntype: config\nrings:\n"
        f"  - {ring!r}\n---\n")
    cell_path = Path("nodes") / ".geometry" / "vetoes.md"
    veto.save(root, _frozen_geom(), cell_path)

    # a valid majority ring decision over the gated scope clears
    decision = _veto_cell(council_and_keep, "prime", reason="clear via ring")
    out = send.veto_answer(root, "prime", json.dumps(decision))
    assert "ANSWERED" in out
    frozen, _why = veto.is_frozen(None, "prime", geom=veto.read(root, cell_path))
    assert frozen is False

    # a NON-majority (minority) decision refuses by name and clears nothing
    veto.save(root, _frozen_geom(), cell_path)
    minority = _veto_cell(council_and_keep, "prime", reason="minority",
                          signers=("council-core",))
    out2 = send.veto_answer(root, "prime", json.dumps(minority))
    assert "REFUSED" in out2
    frozen2, _why2 = veto.is_frozen(None, "prime",
                                    geom=veto.read(root, cell_path))
    assert frozen2 is True
