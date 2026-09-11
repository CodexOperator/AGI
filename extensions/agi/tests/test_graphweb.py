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
        "    worktree: worktrees/wt1\n"
        "  - name: sanctuary-helper\n"
        "    window: win_b\n"
        "    pid: 500222\n"
        "    worktree: worktrees/wt2\n"
        "---\n", encoding="utf-8")

    # config.json: point stream_card_png somewhere absent so every build
    # falls back to FALLBACK_PALETTE (deterministic + fast).
    graph_root.joinpath("config.json").write_text(
        json.dumps({"locations": {"stream_card_png": "absent/stream.png"}}),
        encoding="utf-8")

    # the fake worktree: one node file that git status reports as MODIFIED.
    # `worktree` resolves RELATIVE TO graph_root (graphweb),
    # so wt1 lives under <project>/.agi/worktrees/wt1, not the project root.
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
# 7. Cache contract                                                           #
# --------------------------------------------------------------------------- #
def test_cache_returns_same_object_until_mtime_changes(graph) -> None:
    """cached_build_graph returns the SAME payload object when the node mtimes
    are unchanged, and REBUILDS (new object) when a node file mtime changes —
    on a tiny fixture graph so it is fast and deterministic."""
    graphweb._LAYOUT_CACHE.clear()

    first = graphweb.cached_build_graph(graph)
    second = graphweb.cached_build_graph(graph)
    assert first is second, "warm cache must return the identical object"
    assert second["root"] == ROOT

    # Bump a node mtime -> the shape changed -> a fresh build.
    target = graph / "nodes" / "goal" / "other.md"
    st = target.stat()
    os.utime(target, (st.st_atime, st.st_mtime + 2.0))

    rebuilt = graphweb.cached_build_graph(graph)
    assert rebuilt is not first, "an mtime change must rebuild the graph"

    # And a second warm read after the rebuild is stable again.
    assert graphweb.cached_build_graph(graph) is rebuilt