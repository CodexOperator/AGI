"""Fixture-only tests for graphweb.py (hypothesis:l4-the-graph-as-a-golden-3d-web-
in-two-layers, KID 3 of 3 — the test deliverable).

Every test builds a throwaway tmp `.agi`: a handful of goal nodes, a fake
config:seats registry (`.geometry/seats.md` with two rows), a fake worktree
holding one MODIFIED node file, and tmux / pid / git all monkeypatched
in-process. NO test ever touches a live tmux pane, spawns real git against the
repo, or reads/writes the real `.agi`.

The falsifier for this round: any test that reaches a live tmux pane or the
real `.agi` is a defect, and any assertion that would pass with the feature it
names deleted is a defect (e.g. the two-layer split must actually fork the
sanctuary descendant OUT of layer 0).
"""
from __future__ import annotations

import http.server
import json
import math
import os
import struct
import subprocess
import sys
import threading
import urllib.request
import zlib
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))

import graphweb  # noqa: E402

ROOT = graphweb.ROOT  # "goal:g17"
FALLBACK = graphweb.FALLBACK_PALETTE


# --------------------------------------------------------------------------- #
# Fixture builders                                                             #
# --------------------------------------------------------------------------- #
def _write_node(project: Path, rel: str, nid: str, ntype: str,
                parents: list, title: str | None = None) -> Path:
    """Write a tiny frontmatter node under <project>/.agi/nodes/<rel>."""
    p = project / ".agi" / "nodes" / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    lines = ["---",
             f"id: {nid}",
             f"type: {ntype}",
             f"title: {title or nid}"]
    if parents:
        lines.append("parents:")
        for par in parents:
            lines.append(f"  - {par}")
    else:
        lines.append("parents: []")
    lines.append("---")
    p.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return p


def write_fixture_agi(graph_root: Path) -> None:
    """A small .agi with ROOT, a ROOT descendant (the layer-1 falsifier), one
    outside node, and a config:seats registry of two rows.

    Seats:
      * sanctuary-director: window `win_a`, pid 500111, worktree wt1 (exists,
        holds one MODIFIED node file so the git-status mapping is real).
      * sanctuary-helper:   window `win_b`, pid 500222, worktree wt2 (a dead
        worktree — git is never fired for it, working_on stays []).
    """
    project = graph_root.parent
    (graph_root / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    _write_node(project, "goal/g17.md", ROOT, "goal", [])
    _write_node(project, "goal/g17child.md", "goal:g17child", "goal",
                [ROOT], title="g17child")
    _write_node(project, "goal/other.md", "goal:other", "goal", [],
                title="other")

    # the fake config:seats registry (two rows)
    seats_md = graph_root / "nodes" / ".geometry" / "seats.md"
    seats_md.write_text(
        "---\n"
        "seats:\n"
        "  - name: sanctuary-director\n"
        "    window: win_a\n"
        "    pid: 500111\n"
        "    worktree: .agi/worktrees/wt1\n"
        "  - name: sanctuary-helper\n"
        "    window: win_b\n"
        "    pid: 500222\n"
        "    worktree: .agi/worktrees/wt2\n"
        "---\n", encoding="utf-8")

    # config.json: point stream_card_png somewhere absent so every build
    # falls back to FALLBACK_PALETTE (deterministic + fast).
    graph_root.joinpath("config.json").write_text(
        json.dumps({"locations": {"stream_card_png": "absent/stream.png"}}),
        encoding="utf-8")

    # the fake worktree: one node file that git status reports as MODIFIED.
    # seat rows carry the REAL relative shape `.agi/worktrees/wt1` (checkout-
    # root-relative), and the resolver must join it against the checkout root
    # (git_common_root / graph_root.parent), so wt1 lives at
    # <project>/.agi/worktrees/wt1 -- checkout-root-relative.
    wt1_node = (graph_root / "worktrees" / "wt1" / ".agi" / "nodes" /
                "goal" / "g17child.md")
    wt1_node.parent.mkdir(parents=True, exist_ok=True)
    _write_frontmatter_at(wt1_node, "goal:g17child")
    # a dead worktree: wt2 intentionally never created.


def _write_frontmatter_at(path: Path, nid: str) -> None:
    path.write_text(f"---\nid: {nid}\ntype: goal\ntitle: {nid}\n---\n",
                    encoding="utf-8")


@pytest.fixture
def graph(tmp_path):
    """A throwaway .agi. tmp_path is unique per test, so the module-level
    layout cache never aliases one test's graph onto another's."""
    root = tmp_path / "project" / ".agi"
    write_fixture_agi(root)
    return root


def layer_of(payload: dict, nid: str) -> list:
    """The distinct layer values (0/1) a node id appears at, or [] if absent."""
    return sorted({n["layer"] for n in payload["nodes"] if n["id"] == nid})


def _edge_by(edges: list, from_id: str, kind: str):
    return [e for e in edges if e.get("from") == from_id and e.get("kind") == kind]


# --------------------------------------------------------------------------- #
# 1. Two-layer split                                                           #
# --------------------------------------------------------------------------- #
def test_two_layer_split(graph) -> None:
    """ROOT is in BOTH layers; a ROOT descendant is layer 1 and NEVER layer 0
    (the target falsifier); an outside node is layer 0 only; each seat row
    yields one synthetic seat:<name> node in layer 1 with exactly one `seat`
    edge to ROOT."""
    payload = graphweb.build_graph(graph)

    # ROOT is the one member of both layers — the fork point.
    assert layer_of(payload, ROOT) == [0, 1]

    # A goal:g17 descendant is the falsifier: it must be layer 1 and NOT
    # layer 0. If this assertion were dropped, the two-layer split could be
    # deleted and the test would still pass — the falsifier IS the point.
    assert layer_of(payload, "goal:g17child") == [1]

    # A node outside the sanctuary is layer 0 and NOT layer 1.
    assert layer_of(payload, "goal:other") == [0]

    # One synthetic seat:<name> node per config:seats row, layer 1, each with
    # exactly one `seat` edge to ROOT.
    seat_ids = [n["id"] for n in payload["nodes"]
                if n["type"] == "seat" and n["layer"] == 1]
    assert sorted(seat_ids) == ["seat:sanctuary-director",
                                "seat:sanctuary-helper"]
    for sid in seat_ids:
        assert layer_of(payload, sid) == [1]
        seat_edges = _edge_by(payload["edges"], sid, "seat")
        assert len(seat_edges) == 1, f"{sid} must have exactly one seat edge"
        assert seat_edges[0]["to"] == ROOT

    # The seat edges all live in layer 1.
    assert {e["layer"] for e in payload["edges"]
            if e["kind"] == "seat"} == {1}


# --------------------------------------------------------------------------- #
# 2. working_on resolved from a fake worktree                                  #
# --------------------------------------------------------------------------- #
class _FakeResult:
    def __init__(self, returncode, stdout=""):
        self.returncode = returncode
        self.stdout = stdout
        self.stderr = ""


def test_working_on_from_fake_worktree(graph, monkeypatch) -> None:
    """A node file that git status --porcelain reports as MODIFIED in a seat's
    worktree maps file -> node id and shows up in that seat's working_on. Absent
    tmux, dead pids and a dead worktree yield empty, never a traceback."""
    def fake_run(cmd, *args, **kwargs):
        if cmd[0] == "git":
            wt = cmd[2]  # -C <worktree>
            if "wt1" in wt:
                return _FakeResult(0, " M .agi/nodes/goal/g17child.md\n")
            return _FakeResult(0, "")
        # tmux: absent tmux raises; graphweb must swallow it -> empty set.
        raise FileNotFoundError("tmux not installed (fixture)")

    # Patch run on the SHARED subprocess module attribute graphweb reads. The
    # monkeypatch fixture restores the real function after this test.
    monkeypatch.setattr(graphweb.subprocess, "run", fake_run)

    view = graphweb.live_view(graph)

    rows = {r["seat"]: r for r in view["seats"]}
    # The modified file maps to its node id in the seat that owns wt1.
    assert rows["sanctuary-director"]["working_on"] == ["goal:g17child"]
    # The dead worktree (wt2) never fires git: working_on stays empty.
    assert rows["sanctuary-helper"]["working_on"] == []

    # Absent tmux -> empty, not a traceback.
    assert graphweb._tmux_windows() == set()

    # A pid that names nothing is not alive, not an exception.
    assert graphweb._pid_alive(999_999_999) is False
    assert graphweb._pid_alive(None) is False
    assert graphweb._pid_alive("not-a-pid") is False


def test_tmux_list_windows_is_scoped_to_agi_rc(monkeypatch) -> None:
    """tmux list-windows runs scoped `-t agi-rc` (rotate.py
    DEFAULT_TMUX_SESSION), NEVER bare — a bare call lists whatever session the
    caller happens to share, and an absent session is where the round measured
    seats silently inactive (Prime, merge-up 38).

    The moniker `agi-rc` for rotate DEFAULT_TMUX_SESSION stays live-looking;
    the point of the test is the `-t` flag is present and names it.
    """
    captured = []
    def fake_run(cmd, *args, **kwargs):
        captured.append(list(cmd))
        raise FileNotFoundError("tmux not installed (fixture)")
    monkeypatch.setattr(graphweb.subprocess, "run", fake_run)

    assert graphweb._tmux_windows() == set()   # absent session -> empty
    assert captured, "tmux was never invoked"
    cmd = captured[0]
    assert cmd[0] == "tmux"
    assert "list-windows" in cmd
    assert "-t" in cmd
    assert cmd[cmd.index("-t") + 1] == "agi-rc", f"argv: {cmd}"


def test_worktree_modified_ids_dead_worktree_no_git(graph, monkeypatch) -> None:
    """_worktree_modified_ids on a nonexistent/dead worktree returns [] and
    never fires git (unfired read completes empty)."""
    fired = []
    def fake_run(cmd, *args, **kwargs):
        fired.append(cmd)
        raise AssertionError("git must not be fired for a dead worktree")
    monkeypatch.setattr(graphweb.subprocess, "run", fake_run)

    # Absolute dead path.
    assert graphweb._worktree_modified_ids(
        str(graph / "worktrees" / "wt2"), graph) == []
    # None -> [].
    assert graphweb._worktree_modified_ids(None, graph) == []
    assert fired == []


def test_relative_checkout_root_worktree_resolves(graph, monkeypatch) -> None:
    """A RELATIVE seat row in the real shape `.agi/worktrees/wt1` resolves
    against the CHECKOUT ROOT (not graph_root) and lists the modified node
    id. This is the claim's falsifier (hypothesis:l4-the-graph-as-a-golden-
    3d-web-in-two-layers): the old resolver joined `graph/worktrees/wt1`
    (i.e. `.agi/.agi/worktrees/wt1`), silently yielding [] for every seat row.
    """
    def fake_run(cmd, *args, **kwargs):
        if cmd[0] == "git":
            assert Path(cmd[2]).is_dir(), \
                f"git fired in a non-direct worktree: {cmd[2]}"
            if "wt1" in cmd[2]:
                return _FakeResult(0, "?? .agi/nodes/goal/g17child.md\n")
            return _FakeResult(0, "")
        raise FileNotFoundError("tmux absent (fixture)")
    monkeypatch.setattr(graphweb.subprocess, "run", fake_run)

    row = {"name": "sanctuary-director", "worktree": ".agi/worktrees/wt1"}
    # The relative row resolves against the checkout root: wt1 directory.
    wt = graphweb._resolve_worktree(row["worktree"], graph)
    assert wt is not None and wt.is_dir()
    # And the modified id shows up in working_on via the live view.
    view = graphweb.live_view(graph)
    rows = {r["seat"]: r for r in view["seats"]}
    assert rows["sanctuary-director"]["working_on"] == ["goal:g17child"]
    # The dead relative worktree (wt2) never fires git and stays empty.
    assert rows["sanctuary-helper"]["working_on"] == []


# --------------------------------------------------------------------------- #
# 3. active follows tmux-window presence AND pid liveness                      #
# --------------------------------------------------------------------------- #
def test_active_requires_window_and_live_pid(graph, monkeypatch) -> None:
    """active=false when the seat's tmux window is absent (even with a live
    pid); active=true only when the pid is alive AND the window is present."""
    alive_pid = 500111
    monkeypatch.setattr(graphweb, "_pid_alive",
                        lambda pid: pid == alive_pid)
    # One window present; win_b is absent.
    monkeypatch.setattr(graphweb, "_tmux_windows", lambda: {"win_a"})

    view = graphweb.live_view(graph)
    rows = {r["seat"]: r for r in view["seats"]}

    # window present + pid alive -> active.
    assert rows["sanctuary-director"]["active"] is True
    # window absent (pid alive but no such tmux window) -> inactive.
    assert rows["sanctuary-helper"]["active"] is False


def test_active_false_when_pid_dead(graph, monkeypatch) -> None:
    """active=false with a dead pid even when the window would be present."""
    monkeypatch.setattr(graphweb, "_pid_alive", lambda pid: False)
    monkeypatch.setattr(graphweb, "_tmux_windows", lambda: {"win_a", "win_b"})

    rows = {r["seat"]: r for r in graphweb.live_view(graph)["seats"]}
    assert rows["sanctuary-director"]["active"] is False
    assert rows["sanctuary-helper"]["active"] is False


# --------------------------------------------------------------------------- #
# 4. Palette                                                                   #
# --------------------------------------------------------------------------- #
def _png_rgb(w: int, h: int, rows: list) -> bytes:
    """Build a full 8-bit RGB (colortype 2) PNG with filter type 0."""
    def chunk(typ: bytes, data: bytes) -> bytes:
        return (struct.pack(">I", len(data)) + typ + data +
                struct.pack(">I", zlib.crc32(typ + data) & 0xFFFFFFFF))
    ihdr = struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)
    raw = b"".join(b"\x00" + bytes(rows[i]) for i in range(h))
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) +
            chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b""))


def test_palette_fallback_when_png_absent(graph) -> None:
    """Exact fallback palette when the stream-card png is absent/undecodable."""
    assert graphweb.sample_palette(graph) == dict(FALLBACK)
    assert dict(FALLBACK) == {"ground": "#0f1216", "gold": "#a48c5a"}


def test_palette_sampled_from_png(graph) -> None:
    """On a 4x4 png (dark bg + one warm pixel) the sampled palette equals the
    deterministic expected hexes."""
    dark = (15, 18, 22)          # #0f1216
    warm = (164, 140, 90)        # #a48c5a
    px = warm + dark * 3         # one warm pixel + 3 dark, flat
    rows = [px, px, px, px]      # 4 rows x 4 cols
    png_path = graph / "card.png"
    png_path.write_bytes(_png_rgb(4, 4, rows))

    # point the config at the real png and re-sample.
    graph.joinpath("config.json").write_text(
        json.dumps({"locations": {"stream_card_png": "card.png"}}),
        encoding="utf-8")

    assert graphweb.sample_palette(graph) == {
        "ground": "#0f1216", "gold": "#a48c5a"}


def test_palette_fallback_on_non_png(graph) -> None:
    """A file that is not a png fails open to the fallback."""
    graph.joinpath("config.json").write_text(
        json.dumps({"locations": {"stream_card_png": "not-img.png"}}),
        encoding="utf-8")
    (graph / "not-img.png").write_bytes(b"this is not a png at all")
    assert graphweb.sample_palette(graph) == dict(FALLBACK)


# --------------------------------------------------------------------------- #
# 5. Server content types                                                      #
# --------------------------------------------------------------------------- #
def test_server_answers_core_routes(graph, monkeypatch) -> None:
    """GET /, /graph.json and /live.json answer 200 with the right content
    types from a handler bound to the tmp .agi on an ephemeral port."""
    # Deterministic live view: no live tmux, controlled liveness + worktrees.
    monkeypatch.setattr(graphweb, "_tmux_windows", lambda: {"win_a"})
    monkeypatch.setattr(graphweb, "_pid_alive", lambda pid: pid == 500111)
    monkeypatch.setattr(graphweb, "_worktree_modified_ids",
        lambda wt, gr: ["goal:g17child"] if wt and "wt1" in str(wt) else [])

    handler = type("BoundGraphHandler", (graphweb.GraphHandler,),
                   {"graph_root": graph})
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    port = httpd.server_address[1]
    t = threading.Thread(target=httpd.serve_forever, daemon=True)
    t.start()
    try:
        base = f"http://127.0.0.1:{port}"
        with urllib.request.urlopen(base + "/") as r:
            assert r.status == 200
            assert r.headers["Content-Type"].startswith("text/html")
        with urllib.request.urlopen(base + "/graph.json") as r:
            assert r.status == 200
            assert r.headers["Content-Type"].startswith("application/json")
            data = json.loads(r.read().decode("utf-8"))
            assert data["root"] == ROOT
            # the fixture graph really is two-layered on the wire too
            assert layer_of(data, "goal:g17child") == [1]
        with urllib.request.urlopen(base + "/live.json") as r:
            assert r.status == 200
            assert r.headers["Content-Type"].startswith("application/json")
            data = json.loads(r.read().decode("utf-8"))
            assert {s["seat"] for s in data["seats"]} == {
                "sanctuary-director", "sanctuary-helper"}
    finally:
        httpd.shutdown()
        httpd.server_close()
        t.join(timeout=5)


# --------------------------------------------------------------------------- #
# 6. bin help smoke (graphweb.py -h exits 0)                                   #
# --------------------------------------------------------------------------- #
def test_graphweb_bin_help_exits_zero() -> None:
    """`python3 extensions/agi/bin/graphweb.py -h` exits 0 with non-empty
    stdout. Naming mirrors the parametrised test_bin_help_smoke.py without
    duplicating its test id."""
    result = subprocess.run(
        [sys.executable, str(BIN / "graphweb.py"), "-h"],
        capture_output=True, text=True, timeout=20)
    assert result.returncode == 0, (
        f"graphweb.py -h exited {result.returncode}.\n"
        f"stderr: {result.stderr[:500]}")
    assert len(result.stdout.strip()) > 0


# --------------------------------------------------------------------------- #
# 8. Ghost nodes: agent target / parent / new_nodes (owl-priority round,     #
#    the owner's 2026-09-11 15:5xZ order) + graph_version in /live.json      #
# --------------------------------------------------------------------------- #
def _fake_parent_worktree(base: Path) -> Path:
    """A fake PARENT lease worktree holding a dispatch manifest and one
    untracked KID node file. Returns the worktree root."""
    wt = base / "wt-p"
    kid_node = wt / ".agi" / "nodes" / "experiment" / "kid-1fbbdf68-abc.md"
    kid_node.parent.mkdir(parents=True, exist_ok=True)
    kid_node.write_text(
        "---\n"
        "id: experiment:kid-1fbbdf68-abc\n"
        "type: experiment\n"
        "title: kid-1fbbdf68 build\n"
        "parents:\n"
        "  - hypothesis:some-target\n"
        "---\n", encoding="utf-8")
    # the dispatch manifest: parent entry + the kid entry, one shared target.
    manifest = (wt / ".agi" / "sessions" / "iter-L4.999" / "manifest.json")
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(json.dumps({
        "iter": "L4.999",
        "agents": [
            {"id": "par-a", "tier": "parent",
             "target": "hypothesis:some-target"},
            {"id": "kid-1fbbdf68", "tier": "kid",
             "target": "hypothesis:some-target"},
        ],
    }), encoding="utf-8")
    return wt


def _fake_seat_run(cmd, *args, **kwargs):
    """git runner for the ghost-node tests: untracked kid node in wt-p, and
    seat/os reads just resolve to empty."""
    if cmd[0] == "git":
        wt = cmd[2]
        if "wt-p" in wt:
            return _FakeResult(
                0, "?? .agi/nodes/experiment/kid-1fbbdf68-abc.md\n")
        return _FakeResult(0, "")
    raise FileNotFoundError("tmux absent (fixture)")


def test_live_agents_carry_target_parent_and_new_nodes(graph, monkeypatch) -> None:
    """In /live.json, a live KID agent (no own worktree) carries: `target`
    from its parent's dispatch manifest, `parent` (the parent-tier lease id),
    and a `new_nodes` record parsed from its UNTRACKED node file in the
    parent's worktree — so the page can snap real details in before the node
    reaches the served graph (the owner's ghost-node order, kid C)."""
    wt_p = _fake_parent_worktree(graph.parent)
    monkeypatch.setattr(graphweb, "live_agents", lambda gr: [
        {"agent_id": "par-a", "tier": "parent", "iter": "L4.999",
         "worktree": str(wt_p)},
        {"agent_id": "kid-1fbbdf68", "tier": "kid", "iter": "L4.999",
         "worktree": None},
    ])
    monkeypatch.setattr(graphweb.subprocess, "run", _fake_seat_run)

    view = graphweb.live_view(graph)
    agents = {a["agent"]: a for a in view["agents"]}

    kid = agents["kid-1fbbdf68"]
    # manifests carry the target; the parent lease is a KID's parent with the
    # same iter.
    assert kid["target"] == "hypothesis:some-target"
    assert kid["parent"] == "par-a"
    # the untracked new node (filtered to ids containing the kid's agent id).
    assert kid["new_nodes"] == [{
        "id": "experiment:kid-1fbbdf68-abc",
        "type": "experiment",
        "title": "kid-1fbbdf68 build",
        "parents": ["hypothesis:some-target"],
    }]
    # the same untracked node is also in its working_on.
    assert "experiment:kid-1fbbdf68-abc" in kid["working_on"]

    # A parent-tier agent carries target too, but parent == None.
    par = agents["par-a"]
    assert par["target"] == "hypothesis:some-target"
    assert par["parent"] is None
    # the parent's worktree holds the kid's file, so it shows up as new for
    # the parent as well (unfiltered).
    assert any(n["id"] == "experiment:kid-1fbbdf68-abc"
               for n in par["new_nodes"])


def test_no_manifest_yields_empty_target_no_traceback(graph, monkeypatch) -> None:
    """An agent whose manifest is absent/unreadable gets target "" (and no
    new_nodes / no traceback) — the ghost just never snaps."""
    wt_p = graph.parent / "wt-none"
    wt_p.mkdir(parents=True, exist_ok=True)   # a worktree with NO manifest
    monkeypatch.setattr(graphweb, "live_agents", lambda gr: [
        {"agent_id": "par-x", "tier": "parent", "iter": "L4.777",
         "worktree": str(wt_p)},
    ])
    monkeypatch.setattr(graphweb.subprocess, "run", _fake_seat_run)

    view = graphweb.live_view(graph)
    agents = {a["agent"]: a for a in view["agents"]}
    assert agents["par-x"]["target"] == ""
    assert agents["par-x"]["parent"] is None
    assert agents["par-x"]["new_nodes"] == []

    # a corrupt manifest also fails open to "".
    bad = graph.parent / "wt-bad"
    badm = bad / ".agi" / "sessions" / "iter-L4.777" / "manifest.json"
    badm.parent.mkdir(parents=True, exist_ok=True)
    badm.write_text("{ this is not json", encoding="utf-8")
    monkeypatch.setattr(graphweb, "live_agents", lambda gr: [
        {"agent_id": "par-y", "tier": "parent", "iter": "L4.777",
         "worktree": str(bad)},
    ])
    view2 = graphweb.live_view(graph)
    agents2 = {a["agent"]: a for a in view2["agents"]}
    assert agents2["par-y"]["target"] == ""


def test_live_view_carries_graph_version(graph, monkeypatch) -> None:
    """/live.json carries `graph_version` (the stable ACTIVE id-set hash)
    for the 5 s poll / re-fetch-on-change contract (kid A). It changes when an
    id is added."""
    monkeypatch.setattr(graphweb, "live_agents", lambda gr: [])
    view = graphweb.live_view(graph)
    assert view["graph_version"] == graphweb.graph_version(graph)
    assert isinstance(view["graph_version"], str) and view["graph_version"]

    graphweb._PARSE_CACHE.clear()
    _write_node(graph.parent, "goal/added2.md", "goal:added2", "goal",
                [ROOT])
    view2 = graphweb.live_view(graph)
    assert view2["graph_version"] != view["graph_version"], \
        "adding an id must change /live.json graph_version"
    (graph / "nodes" / "goal" / "added2.md").unlink()


# --------------------------------------------------------------------------- #
# 7. Layout persistence & incremental (B1/B2/B3/B5)                           #
# --------------------------------------------------------------------------- #
def _node_positions(payload: dict) -> dict:
    """{id: (x,y,z)} for the payload's node list. ROOT appears in BOTH
    layers; the last occurrence (layer 1) wins the dict, which is fine for
    the byte-identical-position assertions below."""
    return {n["id"]: tuple(n["pos"]) for n in payload["nodes"]}


def test_layout_persists_and_reuses_across_body_edit(graph, monkeypatch) -> None:
    """An edit that changes no id and no edge must REUSE every position
    byte-identically (B1), and it must reuse from the PERSISTED file (not
    just the in-memory memo). This REWRITES the old
    test_cache_returns_same_object_until_mtime_changes, whose assertion —
    REBUILD on an mtime bump — contradicted the amended contract (an mtime
    bump from a body edit is exactly the case that must NOT rebuild)."""
    calls = []
    orig = graphweb._force_layout

    def counting(*a, **k):
        calls.append(1)
        return orig(*a, **k)

    monkeypatch.setattr(graphweb, "_force_layout", counting)
    graphweb._POS_MEMO.clear()
    graphweb._PARSE_CACHE.clear()

    first = graphweb.build_graph(graph)
    cold_calls = len(calls)
    assert cold_calls > 0, "the cold build must run the full force layout"
    pos_first = _node_positions(first)

    # Drop the in-memory memo so the second build has to come from the FILE.
    graphweb._POS_MEMO.clear()

    # Edit a node BODY: title changes, but the id set and edge set do not.
    _write_node(graph.parent, "goal/other.md", "goal:other", "goal", [],
                title="renamed-body")
    second = graphweb.build_graph(graph)

    # The body edit must NOT re-run the full layout (force-layout call count
    # stays at the cold build's), and every position is byte-identical.
    assert len(calls) == cold_calls, \
        "a body edit must reuse the persisted layout, never re-layout"
    assert _node_positions(second) == pos_first, \
        "positions must be byte-identical across a body edit"
    # The re-parse (cheap, parse-cache per file) still surfaces the new title.
    titles = {n["id"]: n["title"] for n in second["nodes"]}
    assert titles["goal:other"] == "renamed-body"
    # And the layout is on disk (persisted), keyed by the id+edge signature.
    persisted = json.loads(
        (graph / "sessions" / "graphweb-layout.json").read_text(
            encoding="utf-8"))
    assert persisted["kind"] == "graphweb-layout"
    assert isinstance(persisted["signature"], str)
    assert "goal:other" in persisted["layer0"]


def test_add_one_node_incremental(graph, monkeypatch) -> None:
    """Adding one id must NOT re-run the full cold layout: old positions stay
    byte-identical (pinned survivors), the new node lands within 2 units of
    its parent, and the INCREMENTAL path (not the full pass) is what runs
    (B2). Removed ids are dropped."""
    calls = []
    orig = graphweb._force_layout

    def counting(*a, **k):
        calls.append(1)
        return orig(*a, **k)

    monkeypatch.setattr(graphweb, "_force_layout", counting)
    graphweb._POS_MEMO.clear()
    graphweb._PARSE_CACHE.clear()

    first = graphweb.build_graph(graph)
    cold_calls = len(calls)
    pos_before = _node_positions(first)

    # Add a new node whose parent is ROOT.
    _write_node(graph.parent, "goal/brandnew.md", "goal:brandnew", "goal",
                [ROOT], title="brandnew")
    graphweb._POS_MEMO.clear()  # force the incremental path through persistence

    second = graphweb.build_graph(graph)
    # The full layout must NOT rerun for an add — incremental only.
    assert len(calls) == cold_calls, \
        "an added id must go through the INCREMENTAL path, never the full pass"

    pos_after = _node_positions(second)
    # Old positions are byte-identical (survivors pinned).
    for nid in ("goal:g17", "goal:g17child", "goal:other",
                "seat:sanctuary-director", "seat:sanctuary-helper"):
        assert pos_after[nid] == pos_before[nid], \
            f"{nid} must not move on an incremental add"

    # The new node is within 2 units of its parent (ROOT).
    pnew = pos_after["goal:brandnew"]
    proot = pos_after[ROOT]
    dist = math.hypot(pnew[0] - proot[0], pnew[1] - proot[1])
    assert dist <= 2.0, f"new node {dist:.3f} units from parent (> 2)"

    # Removed ids are dropped: delete the new node and it vanishes again.
    (graph / "nodes" / "goal" / "brandnew.md").unlink()
    graphweb._POS_MEMO.clear()
    third = graphweb.build_graph(graph)
    assert "goal:brandnew" not in _node_positions(third)
    # and the surviving positions are back to the (byte-identical) baseline.
    pos_third = _node_positions(third)
    for nid in ("goal:g17", "goal:g17child", "goal:other"):
        assert pos_third[nid] == pos_before[nid]


def test_graph_version_changes_on_add_not_on_body_edit(graph) -> None:
    """graph_version is a stable hash of the ACTIVE id set: identical across
    a body edit, and DIFFERENT when an id is added, and back to the baseline
    when the id is removed again (B5)."""
    graphweb._PARSE_CACHE.clear()

    v1 = graphweb.graph_version(graph)
    assert isinstance(v1, str) and v1
    assert graphweb.graph_version(graph) == v1, "version must be stable"

    # Body edit (title change): no id changes -> same version.
    _write_node(graph.parent, "goal/other.md", "goal:other", "goal", [],
                title="edited")
    assert graphweb.graph_version(graph) == v1, \
        "a body edit changes no id, so graph_version must NOT change"

    # Add a node -> version changes.
    _write_node(graph.parent, "goal/added.md", "goal:added", "goal", [ROOT])
    v2 = graphweb.graph_version(graph)
    assert v2 != v1, "adding an id must change graph_version"

    # Restore other.md's title and remove the added node -> back to baseline.
    _write_node(graph.parent, "goal/other.md", "goal:other", "goal", [],
                title="other")
    (graph / "nodes" / "goal" / "added.md").unlink()
    assert graphweb.graph_version(graph) == v1, \
        "an id-set round-trip must return to the original version"

def test_dispatched_by_accepts_post_and_canonical_spellings():
    """hypothesis:l4-a-seat-is-a-post-everywhere — `_dispatched_by` accepts
    the seat's post- rename beside the deprecated seat- spelling: it derives
    the seat name from `post/<name>@s2` and `season<n>/posts/<name>` just as
    it does from `seat/<name>@s2`."""
    assert graphweb._dispatched_by({"base_branch": "seat/sanctuary-director@s2"}) \
        == "sanctuary-director"
    assert graphweb._dispatched_by({"base_branch": "post/sanctuary-director@s2"}) \
        == "sanctuary-director"
    assert graphweb._dispatched_by({"base_branch": "season2/posts/sanctuary-director"}) \
        == "sanctuary-director"
    assert graphweb._dispatched_by({"base_branch": ""}) == ""
