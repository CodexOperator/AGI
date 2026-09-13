"""Tests for the `alerts:` routing matrix of config:rotations.

hypothesis:l4-rotation-alerts-follow-a-routing-matrix-in-config-rotations-
audit-plus-edges-intersect-live-minus-self-minus-silent

A rotation-alert receiver set = (audit ∪ edges[seat]) ∩ live − {seat} − silent.
`alerts:` absent -> today's BROADCAST, byte-identical. `silent` applies to
EVERY machine sender (the after_join dm included). The Sensei (audit) is in
the set once; stream-master (silent) never.

The fixtures carry the owner's matrix as test data on a rotation config node:
    alerts:
      audit:   [master-sensei]
      edges:
        belam:               [sanctuary-director, sanctuary-helper]
        sanctuary-director:  [belam]
        sanctuary-helper:    [belam]
        sanctuary-master:    [sensei-director]
        sensei-director:     [sanctuary-master]
      silent: [stream-master]
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate  # noqa: E402

AUDIT = ["master-sensei"]
EDGES = {
    "belam": ["sanctuary-director", "sanctuary-helper"],
    "sanctuary-director": ["belam"],
    "sanctuary-helper": ["belam"],
    "sanctuary-master": ["sensei-director"],
    "sensei-director": ["sanctuary-master"],
}
SILENT = ["stream-master"]
ALL = (set(EDGES) | set(AUDIT) | set(SILENT)) | {"belam"}


def _rotations_md(alerts: bool) -> str:
    if not alerts:
        return "---\nid: config:rotations\ntype: config\n---\n"
    # the exact ONE write.py `set alerts {…}` line the Prime writes at
    # merge-up: a single bare-flow mapping (write.py nests nothing). yaml
    # loads `alerts: {...}` as a native dict; `_load_alerts` also accepts a
    # quoted-JSON str cell defensively (like `rotate_defaults`).
    matrix = json.dumps({
        "audit": AUDIT,
        "edges": EDGES,
        "silent": SILENT,
    }, separators=(",", ":"))
    return ("---\nid: config:rotations\ntype: config\n"
            f"alerts: {matrix}\n---\n")


def _mk(root: Path, alerts: bool = True,
        seats=("belam", "sanctuary-director", "sanctuary-helper",
               "sanctuary-master", "sensei-director",
               "master-sensei", "stream-master")) -> Path:
    geom = root / "nodes" / ".geometry"
    geom.mkdir(parents=True, exist_ok=True)
    (geom / "rotations.md").write_text(_rotations_md(alerts), encoding="utf-8")
    body = "---\nid: config:seats\ntype: config\nseats:\n"
    for s in seats:
        body += "  - " + json.dumps({"name": s, "role": "director"}) + "\n"
    body += "---\n"
    (geom / "seats.md").write_text(body, encoding="utf-8")
    (root / "sessions").mkdir(exist_ok=True)
    return root


def _rx(root: Path, seat: str, live=None) -> list:
    return rotate._derive_receivers(
        root, seat=seat, live_names=list(live if live is not None else
                                          (ALL | {seat})))


def test_belam_both_edges_live_routes_matrix(tmp_path):
    """belam with both edges live -> {sanctuary-director, sanctuary-helper,
    master-sensei} -- the audit plus belam's edge set, live only."""
    got = _rx(_mk(tmp_path), "belam")
    assert got == ["master-sensei", "sanctuary-director", "sanctuary-helper"]


def test_sensei_director_edges(tmp_path):
    got = _rx(_mk(tmp_path), "sensei-director")
    assert got == ["master-sensei", "sanctuary-master"]


def test_stream_master_rotating_alerts_audit_only(tmp_path):
    """A silent post that ROTATES still alerts the audit -- silent silences its
    INBOX, not its own outgoing alerts."""
    got = _rx(_mk(tmp_path), "stream-master")
    assert got == ["master-sensei"]


def test_post_absent_from_edges_alerts_audit_only(tmp_path):
    got = _rx(_mk(tmp_path), "nobody")
    assert got == ["master-sensei"]


def test_dead_edge_dropped(tmp_path):
    """A receiver outside (audit ∪ edges) ∩ live — a dead edge (no live tmux
    window) is NOT announced."""
    live = (ALL | {"belam"}) - {"sanctuary-helper"}
    got = _rx(_mk(tmp_path), "belam", live)
    assert got == ["master-sensei", "sanctuary-director"]


def test_stream_master_never_a_receiver_for_any_seat(tmp_path):
    """silent beats audit AND edges: stream-master never appears in any
    receiver set, for every seat in the matrix."""
    root = _mk(tmp_path)
    for seat in EDGES:
        assert "stream-master" not in _rx(root, seat)


def test_alerts_absent_is_today_broadcast(tmp_path):
    """`alerts:` ABSENT -> byte-identical broadcast: config:seats rows
    intersected with live, minus self (the pre-matrix behaviour)."""
    root = _mk(tmp_path, alerts=False, seats=["a", "b", "c"])
    assert _rx(root, "a", ["a", "b", "c"]) == ["b", "c"]


def test_after_join_dm_to_silent_post_refused(tmp_path):
    """silent applies to the after_join machine sender too: run_after_join
    refuses the dm to a silent successor — the seam is never fired."""
    root = _mk(tmp_path)
    sent = []
    rotate.run_after_join(
        root, seat="stream-master",
        startup={}, values={"succ_ref": "x"},
        send_dm=lambda to, text: sent.append((to, text)) or ("heal", False),
        dry_run=False)
    assert sent == [], f"silent successor must receive no after_join dm: {sent}"


def test_rotation_record_carries_announced_to(monkeypatch, tmp_path):
    """Conjunct 4 — a completed ROTATION record carries `announced_to` = the
    recipients the announce actually reached, stamped in place onto the same
    record a reader follows (the way the seating record already did). Before
    this fix only the seating record got announced_to; a rotation record told
    nobody who it alerted."""
    root = _mk(tmp_path)
    import send as _send
    monkeypatch.setattr(
        _send, "send_dm",
        lambda croot, me, other, text, sender: tmp_path)
    monkeypatch.setattr(
        _send, "send",
        lambda root, recv, text, sender=None, nudge=None: tmp_path)
    monkeypatch.setattr(_send, "wake", lambda root, recv: None)
    rec_path = tmp_path / "sessions" / "rotations" / "belam.t.json"
    rec_path.parent.mkdir(parents=True, exist_ok=True)
    rec_path.write_text(json.dumps({"seat": "belam", "result": "success"}),
                        encoding="utf-8")
    delivered = rotate._announce_rotation(
        root=root, croot=tmp_path / "comms", seat="belam",
        successor="belam-III", gen_before=2, gen_after=3, trigger="--force",
        handoff_path=".agi/sessions/belam-III.log", in_flight="none",
        live_names=list(ALL | {"belam"}), record_path=str(rec_path))
    assert delivered == ["master-sensei", "sanctuary-director",
                         "sanctuary-helper"]
    rec = json.loads(rec_path.read_text(encoding="utf-8"))
    assert rec.get("announced_to") == delivered, (
        f"rotation record must name who it told: {rec.get('announced_to')}"
        f" != {delivered}")


def test_after_join_type_seam_to_silent_never_fires(tmp_path):
    """Conjunct 5 — silent stops the TYPING path too. In production the
    after_join's SECOND input is TYPED into the successor pane (send_dm is
    never reached), so gating send_dm alone leaked a machine line to a silent
    post's pane. A type_input seam to a SILENT successor must fire NO seam at
    all — the pane gets zero machine lines."""
    root = _mk(tmp_path)
    typed = []
    sent = []
    rotate.run_after_join(
        root, seat="stream-master",
        startup={}, values={"succ_ref": "x"},
        type_input=lambda s, t: typed.append((s, t)) or True,
        send_dm=lambda to, text: sent.append((to, text)) or ("heal", False),
        dry_run=False)
    assert typed == [], (
        f"silent successor pane must receive no typed input: {typed}")
    assert sent == [], f"silent successor must receive no dm: {sent}"

def test_real_write_py_emitted_str_shape_still_routes(tmp_path):
    """P4 regression - the matrix must survive the SHAPE write.py ACTUALLY
    writes. The Prime runs `write.py config:rotations 'set alerts
    {audit:[...],edges:{...},silent:[...]}'`; _coerce keeps that unquoted-key
    flow map as a STR (only pure JSON parses), node_writer._render_value then
    QUOTES it, and yaml reads the cell back as a string with unquoted keys.
    json.loads rejects that exact string and the matrix used to be read as
    absent -> broadcast. _load_alerts must fall back to yaml.safe_load, which
    parses this spelling. Routes through the REAL _coerce->_render_value->
    yaml.safe_load round-trip, never a hand-written YAML map."""
    import yaml as _yaml
    from agi.bin import write as _write, node_writer as _nw
    from agi.bin import rotate as _rot
    shipped = ("{audit:[master-sensei],"
               "edges:{belam:[sanctuary-director,sanctuary-helper]},"
               "silent:[stream-master]}")
    coerced = _write._coerce(shipped)
    assert isinstance(coerced, str), (
        "write.py must keep the flow map a STR (P4): got "
        + type(coerced).__name__)
    rendered = "\n".join(_nw._render_value("alerts", coerced))
    cell = _yaml.safe_load(rendered)["alerts"]
    assert isinstance(cell, str) and cell.startswith("{"), repr(cell)
    # put that exact write.py-emitted string cell on a scratch rotations node,
    # then parse the matrix through _load_alerts -> _derive_receivers.
    geom = tmp_path / "nodes" / ".geometry"
    geom.mkdir(parents=True, exist_ok=True)
    (geom / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\n"
        f"alerts: \"{cell}\"\n---\n", encoding="utf-8")
    (geom / "seats.md").write_text(
        "---\nid: config:seats\ntype: config\nseats:\n"
        '  - name: belam\n  - name: sanctuary-director\n'
        '  - name: sanctuary-helper\n  - name: stream-master\n'
        '  - name: master-sensei\n---\n', encoding="utf-8")
    live = ["belam", "sanctuary-director", "sanctuary-helper",
            "stream-master", "master-sensei"]
    got = _rot._derive_receivers(tmp_path, seat="belam", live_names=live)
    assert got == ["master-sensei", "sanctuary-director",
                   "sanctuary-helper"], got
