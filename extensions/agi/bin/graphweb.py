#!/usr/bin/env python3
"""graphweb.py — the localhost 3D golden-web dashboard, SERVER + layout layer.

This is KID 1 of 3 under hypothesis:l4-the-graph-as-a-golden-3d-web-in-two-layers
(a00-c42731c0, L4.235). It owns ONLY the server and the layout:

- `python3 extensions/agi/bin/graphweb.py serve --port 8765` serves a localhost
  dashboard from the nearest `.agi` (walked up from cwd), on stdlib
  `http.server`, with NO new Python dependencies.
- `GET /`           -> `extensions/agi/web/graph/index.html` if present (KID 2
                      writes the real page), else a plain placeholder page.
- `GET /graph.json` -> every ACTIVE node as `{id,type,title,layer,pos:[x,y,z]}`
                      plus `edges {from,to,kind}` derived from `parents`, split
                      into TWO LAYERS joined at the ROOT (see `_build_graph`).
                      Also carries `palette` (sampled from the stream card png)
                      and `root`/`layer1_z` for the page.
- `GET /live.json`  -> one record per config:seats row
                      `{seat,active,generation,window,working_on}` plus every
                      live dispatched agent from the spawn-budget dir
                      `{agent,iter,tier,dispatched_by,working_on}`. `working_on`
                      = node ids whose files are MODIFIED in that seat's or
                      agent's worktree. Every tmux/ps/git read is wrapped so an
                      absent tmux or dead worktree yields EMPTY, never a
                      traceback.

KID 2 writes extensions/agi/web/graph/{index.html,app.js}; KID 3 writes
extensions/agi/tests/test_graphweb.py. Neither is authored here.

## The two-layer model (the part a falsifier must not break)

The whole ACTIVE node set is partitioned into two layers that share ONE root:

  ROOT     = `goal:g17` (the seat system / sanctuary).
  layer 1  = ROOT + every descendant of ROOT (the sanctuary subtree) via
             `parents` edges + one synthetic node per config:seats row
             (`seat:<name>`, type `seat`) with an edge `seat:<name> -> ROOT`.
  layer 0  = every other ACTIVE node, PLUS ROOT (so ROOT is the one member of
             both layers — the picture forks at the root).

layer 1 sits ABOVE layer 0 by a fixed z offset (`layer1_z`), so a reader that
drops it back to one plane still sees the same two-layer graph. The falsifier
("a layer-1 node placed at layer 0") is exactly the case this split forbids:
anything reachable from `goal:g17` via `parents` is layer 1 and never layer 0.

## Layout

Deterministic seeded force layout computed IN PYTHON (no networkx). Each layer
is laid out independently on its own plane (layer 0 at z=0, layer 1 at
z=`layer1_z`), with ROOT participating in both so the fork is visible from
every angle.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import random
import struct
import subprocess
import sys
import zlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

try:
    import yaml  # type: ignore  # present in-repo; fallback below if not
except Exception:                                              # noqa: BLE001
    yaml = None

#: The single node both layers share. The sanctuary / seat system.
ROOT = "goal:g17"

#: z offset of layer 1 above layer 0 (arbitrary; the page scales to fit).
LAYER1_Z = 60.0

#: Fixed seed so a render is byte-stable across restarts.
LAYOUT_SEED = 20260911

#: Fallback palette — the measured ground/gold of the stream card bg
#: (hypothesis node, "measured today #a48c5a on #0f1216"). Used whenever the
#: png named by config `locations.stream_card_png` is absent or undecodable.
FALLBACK_PALETTE = {"ground": "#0f1216", "gold": "#a48c5a"}

#: Where the stream-card png lives when config says nothing.
DEFAULT_STREAM_CARD_PNG = "~/work/streamer-stub/out/card-bg.png"

PLACEHOLDER_PAGE = """<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>agi graph web</title></head>
<body style="background:#0f1216;color:#a48c5a;font:15px monospace">
<h2>agi graph — 3D golden web</h2>
<p>server up. page not written yet (<code>extensions/agi/web/graph/index.html</code>).</p>
<ul>
<li><a href="/graph.json">/graph.json</a></li>
<li><a href="/live.json">/live.json</a></li>
</ul>
</body></html>
"""


# --------------------------------------------------------------------------- #
# Path / config                                                                 #
# --------------------------------------------------------------------------- #
def find_root(start: str | os.PathLike | None = None) -> Path:
    """Nearest enclosing `.agi` holding a config, walking up from `start`/cwd.

    Mirrors locations.find_project_root's phase order without importing the
    engine (the server must stay runnable in a bare checkout that only has a
    `.agi`). Returns the `.agi` directory, or raises a clear error.
    """
    try:
        import locations as _loc
        r = _loc.find_project_root(start)
        if r is not None:
            return Path(r)
    except Exception:                                             # noqa: BLE001
        pass
    d = (Path(start) if start is not None else Path.cwd()).resolve()
    cur = d
    while True:
        if (cur / ".agi" / "config.json").is_file():
            return cur / ".agi"
        if (cur / "config.json").is_file():
            return cur
        if cur.parent == cur:
            break
        cur = cur.parent
    raise RuntimeError("graphweb: no .agi with config.json found from "
                       f"{d} (walk up); run from inside the project")


def load_config(graph_root: Path) -> dict:
    """config.json for the graph root, or {} when absent/unreadable."""
    p = Path(graph_root) / "config.json"
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:                                             # noqa: BLE001
        return {}


def source_root(graph_root: Path) -> Path:
    """The repo source root that `extensions/` lives under (parent of .agi)."""
    return Path(graph_root).parent


def _page_path(graph_root: Path) -> Path:
    return source_root(graph_root) / "extensions" / "agi" / "web" / "graph" / "index.html"


def _web_dir(graph_root: Path) -> Path:
    return source_root(graph_root) / "extensions" / "agi" / "web" / "graph"


# --------------------------------------------------------------------------- #
# Frontmatter / nodes                                                          #
# --------------------------------------------------------------------------- #
def parse_frontmatter(raw: str) -> dict:
    """Minimal YAML-lite frontmatter parse; falls back to yaml when present."""
    fm: dict = {}
    lines = raw.splitlines(keepends=False)
    if not lines or lines[0].strip() != "---":
        return fm
    end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end = i
            break
    if end is None:
        return fm
    body = "\n".join(lines[1:end])
    if yaml is not None:
        try:
            got = yaml.safe_load(body)
            return got if isinstance(got, dict) else {}
        except Exception:                                          # noqa: BLE001
            pass
    return _mini_yaml(body)


def _mini_yaml(body: str) -> dict:
    """Fallback for `key: value` + `key:`-then-`  - item` block frontmatter."""
    out: dict = {}
    key = None
    for ln in body.splitlines():
        if not ln.strip() or ln.lstrip().startswith("#"):
            continue
        if ln.startswith(("  ", "\t")):
            if key and ln.strip().startswith("- "):
                out.setdefault(key, []).append(_bare(_strip_comments(ln.strip()[2:])))
            continue
        if ":" in ln:
            k, _, v = ln.partition(":")
            key = k.strip()
            v = _strip_comments(v.strip())
            if not v:
                out[key] = []
            else:
                out[key] = _bare(v)
    return out


def _strip_comments(v: str) -> str:
    # A `#` only starts a comment when preceded by whitespace.
    for i, ch in enumerate(v):
        if ch == "#" and (i == 0 or v[i - 1] in " \t"):
            return v[:i].rstrip()
    return v


def _bare(v: str):
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    if v == "null" or v == "~" or v == "":
        return None
    if v == "true":
        return True
    if v == "false":
        return False
    return v


def _file_id(path: Path) -> str | None:
    try:
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
    except Exception:                                             # noqa: BLE001
        return None
    nid = fm.get("id")
    return nid if isinstance(nid, str) and nid else None


def load_nodes(graph_root: Path) -> dict:
    """{id: {id,type,title,parents:[...]}} for every ACTIVE node.

    ACTIVE = not under `nodes/deprecated/` and not `.geometry/`, and
    `status` != 'deprecated'. `.geometry` carries housekeeping config (e.g.
    config:seats) that is not part of the goal tree; it is represented
    separately via the synthetic `seat:<name>` nodes.
    """
    nodes_dir = Path(graph_root) / "nodes"
    out: dict = {}
    if not nodes_dir.is_dir():
        return out
    for p in sorted(nodes_dir.rglob("*")):
        if not p.is_file() or p.suffix.lower() != ".md":
            continue
        rel = p.relative_to(nodes_dir)
        parts = rel.parts
        if parts and (parts[0] == "deprecated" or parts[0] == ".geometry"):
            continue
        try:
            fm = parse_frontmatter(p.read_text(encoding="utf-8"))
        except Exception:                                         # noqa: BLE001
            continue
        if fm.get("status") == "deprecated":
            continue
        nid = fm.get("id")
        if not isinstance(nid, str) or not nid:
            continue
        parents = fm.get("parents") or []
        if not isinstance(parents, list):
            parents = []
        parents = [str(x) for x in parents if x]
        out[nid] = {
            "id": nid,
            "type": str(fm.get("type") or "node"),
            "title": str(fm.get("title") or nid),
            "parents": parents,
        }
    return out


# --------------------------------------------------------------------------- #
# Seats / agents / live                                                        #
# --------------------------------------------------------------------------- #
def load_seats(graph_root: Path) -> list:
    """config:seats rows (`.geometry/seats.md` frontmatter `seats:`), else [].

    Falls back to config.json's (legacy) `seats` list when seats.md is absent,
    so a project that keeps its registry in the config still resolves.
    """
    p = Path(graph_root) / "nodes" / ".geometry" / "seats.md"
    if p.is_file():
        try:
            fm = parse_frontmatter(p.read_text(encoding="utf-8"))
        except Exception:                                         # noqa: BLE001
            fm = {}
        rows = fm.get("seats") or []
        if isinstance(rows, list):
            return [dict(r) for r in rows if isinstance(r, dict)]
    cfg = load_config(graph_root)
    rows = cfg.get("seats") or []
    if isinstance(rows, list):
        return [dict(r) for r in rows if isinstance(r, dict)]
    return []


def _pid_alive(pid) -> bool:
    """Whether `pid` names a live process, by pid directly (never a ps grep)."""
    if not pid:
        return False
    try:
        pid = int(pid)
    except (TypeError, ValueError):
        return False
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:
        return True  # exists, owned by someone else
    except Exception:                                             # noqa: BLE001
        return False


def _tmux_windows() -> set:
    """The set of tmux window refs (``@N`` tokens and names), or empty.

    Reads `tmux list-windows` ONCE. Absent tmux -> empty, never a raise.
    """
    try:
        out = subprocess.run(
            ["tmux", "list-windows"], capture_output=True, text=True,
            timeout=10, check=False)
    except Exception:                                             # noqa: BLE001
        return set()
    if out.returncode != 0:
        return set()
    wins: set = set()
    for cl in out.stdout.splitlines():
        wins.add(cl.split()[0].split(":")[0])  # window name
        for tok in cl.split():
            if tok.startswith("@") and tok[1:].isdigit():
                wins.add(tok)
    return wins


def _worktree_modified_ids(worktree: str | None, graph_root: Path) -> list:
    """Node ids whose files are MODIFIED in `worktree`, or [].

    Resolves `worktree` relative to `graph_root` when not absolute, runs
    `git -C <wt> status --porcelain -- .agi/nodes` once, maps each changed
    path to its node id. A dead/missing worktree or an absent git yields []
    (never a traceback).
    """
    if not worktree:
        return []
    wt = Path(worktree).expanduser()
    if not wt.is_absolute():
        wt = Path(graph_root) / worktree
    if not wt.is_dir():
        return []
    try:
        out = subprocess.run(
            ["git", "-C", str(wt), "status", "--porcelain", "--", ".agi/nodes"],
            capture_output=True, text=True, timeout=20, check=False)
    except Exception:                                             # noqa: BLE001
        return []
    if out.returncode != 0:
        return []
    ids: list = []
    seen: set = set()
    for cl in out.stdout.splitlines():
        line = cl.rstrip("\n")
        if not line:
            continue
        if "->" in line:
            path = line.split("->")[-1].strip()
        else:
            path = line[3:].strip()
        if not path:
            continue
        node_path = wt / path
        nid = _file_id(node_path)
        if nid and nid not in seen:
            seen.add(nid)
            ids.append(nid)
    return ids


def _dispatched_by(rec: dict) -> str:
    """The dispatching seat, derived from a lease's `base_branch`.

    Dispatches record `base_branch` like `seat/sanctuary-director@s2`; the
    `seat/<name>` prefix names the seat that spawned this agent.
    """
    base = rec.get("base_branch") or ""
    if base.startswith("seat/"):
        return base[len("seat/"):].split("@")[0]
    return ""


def live_agents(graph_root: Path) -> list:
    """Live leases from the (main-checkout) spawn-budget dir, read-only.

    Live = the lease's own pid (agent_pid, else holder_pid) is alive — read
    by pid directly, mirroring spawn_budget's liveness without writing a lock.
    """
    try:
        import spawn_budget as _sb
        d = _sb.budget_dir(graph_root)
    except Exception:                                             # noqa: BLE001
        d = Path(graph_root) / "sessions" / ".spawn-budget"
    d = Path(d)
    out: list = []
    if not d.is_dir():
        return out
    for p in sorted(d.glob("*.lease")):
        try:
            rec = json.loads(p.read_text(encoding="utf-8"))
        except Exception:                                         # noqa: BLE001
            continue
        if not isinstance(rec, dict):
            continue
        pid = rec.get("agent_pid") or rec.get("holder_pid")
        if not _pid_alive(pid):
            continue
        out.append(rec)
    return out


def live_view(graph_root: Path) -> dict:
    """The /live.json payload: seats (with liveness) + live agents."""
    seats = load_seats(graph_root)
    windows = _tmux_windows()
    seat_rows: list = []
    for row in seats:
        name = row.get("name") or row.get("id")
        if not name:
            continue
        win = row.get("window")
        pid = row.get("pid")
        alive = _pid_alive(pid)
        has_win = bool(win and (str(win) in windows or str(win).split(":")[0] in windows))
        seat_rows.append({
            "seat": name,
            "active": bool(alive and has_win),
            "generation": row.get("generation"),
            "window": row.get("window"),
            "working_on": _worktree_modified_ids(row.get("worktree"), graph_root),
        })
    agents: list = []
    for rec in live_agents(graph_root):
        agent = rec.get("agent_id")
        if not agent:
            continue
        agents.append({
            "agent": agent,
            "iter": rec.get("iter"),
            "tier": rec.get("tier"),
            "dispatched_by": _dispatched_by(rec),
            "working_on": _worktree_modified_ids(rec.get("worktree"), graph_root),
        })
    return {"seats": seat_rows, "agents": agents}


# --------------------------------------------------------------------------- #
# Palette (sampled from the stream card png)                                   #
# --------------------------------------------------------------------------- #
def _png_decoder(path: Path):
    """Yield (w,h,colortype,row_decoder) or raise on unsupported PNG."""
    data = path.read_bytes()
    if data[:8] != b"\x89PNG\r\n\x1a\n":
        raise ValueError("not a png")
    pos = 8
    idat = b""
    w = h = bits = ct = interlac = 0
    while pos < len(data):
        if pos + 8 > len(data):
            break
        ln, typ = struct.unpack(">I4s", data[pos:pos + 8])
        chunk = data[pos + 8:pos + 8 + ln]
        if typ == b"IHDR" and len(chunk) >= 13:
            w, h, bits, ct, _comp, _flt, interlac = struct.unpack(">IIBBBBB", chunk[:13])
        elif typ == b"IDAT":
            idat += chunk
        pos += 12 + ln
    if interlac != 0:
        raise ValueError("interlaced png unsupported")
    if bits != 8:
        raise ValueError("only 8-bit png supported")
    return w, h, ct, zlib.decompress(idat)


def sample_palette(graph_root: Path) -> dict:
    """{ground, gold} sampled at serve time from the stream card png.

    ground = mean of the darkest half of sampled pixels; gold = mean of the
    brightest decile (the warm gold glow). Fails open to FALLBACK_PALETTE on
    any error: absent png, unreadable file, undecodable image.
    """
    cfg = load_config(graph_root)
    png = (cfg.get("locations") or {}).get("stream_card_png") or DEFAULT_STREAM_CARD_PNG
    expanded = os.path.expanduser(str(png))
    path = (Path(expanded) if os.path.isabs(expanded) else Path(graph_root) / expanded)
    try:
        if not path.is_file():
            return dict(FALLBACK_PALETTE)
        w, h, ct, raw = _png_decoder(path)
        if ct not in (2, 6):
            return dict(FALLBACK_PALETTE)
        channels = 3 if ct == 2 else 4
        stride = w * channels
        samples = _sample_scanlines(raw, w, h, channels, stride)
        if len(samples) < 4:
            return dict(FALLBACK_PALETTE)
        return _palette_from(samples)
    except Exception:                                             # noqa: BLE001
        return dict(FALLBACK_PALETTE)


def _sample_scanlines(raw: bytes, w: int, h: int, channels: int, stride: int) -> list:
    rows_width = stride + 1
    prev = bytearray(stride)
    step = max(1, min(w, h) // 80)  # bounded sample count
    samples: list = []
    for y in range(h):
        base = y * rows_width
        if base + rows_width > len(raw):
            break
        f = raw[base]
        row = bytearray(raw[base + 1:base + 1 + stride])
        if f == 0:
            pass
        elif f == 1:
            for i in range(channels, stride):
                row[i] = (row[i] + row[i - channels]) & 255
        elif f == 2:
            for i in range(stride):
                row[i] = (row[i] + prev[i]) & 255
        elif f == 3:
            for i in range(stride):
                a = row[i - channels] if i >= channels else 0
                row[i] = (row[i] + ((a + prev[i]) >> 1)) & 255
        elif f == 4:
            for i in range(stride):
                a = row[i - channels] if i >= channels else 0
                b = prev[i]
                c = prev[i - channels] if i >= channels else 0
                pp = a + b - c
                pa, pb, pc = abs(pp - a), abs(pp - b), abs(pp - c)
                pr = a if (pa <= pb and pa <= pc) else (b if pb <= pc else c)
                row[i] = (row[i] + pr) & 255
        if y % step == 0:
            for x in range(0, w, step):
                i = x * channels
                r, g, b = row[i], row[i + 1], row[i + 2]
                samples.append((r, g, b, 0.2126 * r + 0.7152 * g + 0.0722 * b))
        prev = row
    return samples


def _palette_from(samples: list) -> dict:
    lum = lambda s: s[3]                                                      # noqa: E731
    by_lum = sorted(samples, key=lum)
    dark = by_lum[: max(1, len(by_lum) // 2)]
    bright = by_lum[-max(1, len(by_lum) // 10):]
    if not bright:
        bright = by_lum

    def mean(seq):
        n = len(seq)
        return tuple(int(sum(s[k] for s in seq) / n) for k in range(3))

    ground = mean(dark)
    gold = mean(bright)
    return {
        "ground": "#%02x%02x%02x" % ground,
        "gold": "#%02x%02x%02x" % gold,
    }


# --------------------------------------------------------------------------- #
# Two-layer graph + seeded force layout                                        #
# --------------------------------------------------------------------------- #
def sanctuary_subtree(nodes: dict, root: str = ROOT) -> set:
    """All ACTIVE ids reachable from `root` via `parents` (the sanctuary)."""
    children: dict = {}
    for _nid, node in nodes.items():
        for par in node.get("parents", []):
            children.setdefault(par, []).append(_nid)
    seen: set = set()
    stack = [root]
    while stack:
        cur = stack.pop()
        if cur in seen:
            continue
        seen.add(cur)
        stack.extend(children.get(cur, []))
    return seen


#: Module-level layout cache. The force layout is ~O(n^2)*180 iterations
#: (measured 170 s on the real 2115-node graph) — recomputing it on EVERY
#: /graph.json request is how a page load becomes a ~3-minute wait. We cache
#: the built payload keyed by graph root + the mtimes of the node files + the
#: palette source, and invalidate only when those change. One server process
#: serves one graph root, so a single-slot registry is exactly the right size.
_LAYOUT_CACHE: dict = {}  # {signature: payload}


def _layout_cache_key(graph_root: Path) -> str:
    """A signature over everything build_graph reads: node file mtimes, the
    seats/config registries. Any change busts the cache."""
    parts = [str(Path(graph_root).resolve())]
    nodes_dir = Path(graph_root) / "nodes"
    if nodes_dir.is_dir():
        mtimes = []
        for p in nodes_dir.rglob("*.md"):
            try:
                mtimes.append((str(p), int(p.stat().st_mtime_ns)))
            except OSError:
                pass
        mtimes.sort()
        parts.append(repr(mtimes))
    for extra in (Path(graph_root) / "nodes" / ".geometry" / "seats.md",
                  Path(graph_root) / "config.json"):
        try:
            parts.append(f"{extra}@{int(extra.stat().st_mtime_ns)}")
        except OSError:
            parts.append(f"{extra}@missing")
    return str(hash(tuple(parts)))


def cached_build_graph(graph_root: Path, seed: int = LAYOUT_SEED) -> dict:
    """build_graph memoized per graph shape; the cold first build still runs
    in full (and may take minutes), every warm request hits the cache."""
    key = _layout_cache_key(graph_root)
    hit = _LAYOUT_CACHE.get(key)
    if hit is not None:
        return hit
    payload = build_graph(graph_root, seed=seed)
    _LAYOUT_CACHE[key] = payload
    return payload


def build_graph(graph_root: Path, seed: int = LAYOUT_SEED) -> dict:
    """The /graph.json payload: two-layer nodes + edges + palette + layout.

    MEMBERSHIP (see module docstring):
      layer1 = {ROOT} ∪ sanctuary subtree ∪ {seat:<name> per seat}
      layer0 = ACTIVE − (layer1 − {ROOT})      (ROOT appears in BOTH layers)

    SPLIT ORDER guarantees the falsifier: a node in ROOT's subtree is ALWAYS
    layer 1 and NEVER layer 0.
    """
    nodes = load_nodes(graph_root)
    seats = load_seats(graph_root)
    sanctuary = sanctuary_subtree(nodes, ROOT)

    seat_ids = []
    for row in seats:
        name = row.get("name") or row.get("id")
        if name:
            seat_ids.append(f"seat:{name}")

    layer1 = set(sanctuary) | set(seat_ids)
    layer0 = set(nodes) | ({ROOT} if ROOT in nodes else set())
    # layer0 = ACTIVE minus sanctuary's non-root members
    layer0 -= sanctuary - {ROOT}

    # node meta (both layers draw from the same meta map; seats are synthetic)
    meta = dict(nodes)
    for sid in seat_ids:
        meta[sid] = {"id": sid, "type": "seat", "title": sid, "parents": [ROOT]}

    # --- edges (within-layer only; ROOT bridges both) ---------------------- #
    def edges_for(members: set) -> list:
        ed = []
        for _nid in members:
            meta_node = meta.get(_nid, {})
            if meta_node.get("type") == "seat":
                # synthetic seat nodes never emit a `parents` edge; they get
                # exactly one explicit `seat` edge to ROOT below.
                continue
            for par in meta_node.get("parents", []):
                if par in members:
                    ed.append({"from": _nid, "to": par, "kind": "parent"})
        return ed

    edges0 = edges_for(layer0)
    edges1 = edges_for(layer1)
    for sid in seat_ids:
        edges1.append({"from": sid, "to": ROOT, "kind": "seat"})

    # --- force layout, one plane per layer --------------------------------- #
    pos0 = _force_layout(layer0, edges0, seed=seed)
    pos1 = _force_layout(layer1, edges1, seed=seed)

    def nodes_out(ids: set, pos: dict, layer: int) -> list:
        out = []
        for _nid in sorted(ids):
            met = meta.get(_nid, {"id": _nid, "type": "node",
                                  "title": _nid, "parents": []})
            x, y = pos.get(_nid, (0.0, 0.0))
            out.append({
                "id": _nid,
                "type": met.get("type") or "node",
                "title": met.get("title") or _nid,
                "layer": layer,
                "pos": [round(x, 3), round(y, 3),
                        round(LAYER1_Z if layer == 1 else 0.0, 3)],
            })
        return out

    out_nodes = nodes_out(layer0, pos0, 0) + nodes_out(layer1, pos1, 1)
    for e in edges0:
        e["layer"] = 0
    for e in edges1:
        e["layer"] = 1
    return {
        "root": ROOT,
        "layer1_z": LAYER1_Z,
        "nodes": out_nodes,
        "edges": edges0 + edges1,
        "palette": sample_palette(graph_root),
    }


def _force_layout(ids: set, edges: list, seed: int, iters: int = 180) -> dict:
    """Seeded Fruchterman–Reingold in-plane layout. Returns {id:(x,y)}."""
    ids = list(ids)
    n = len(ids)
    pos = {i: 0.0 for i in ids}
    rng = random.Random(seed)
    if n == 0:
        return {}
    if n == 1:
        return {ids[0]: (0.0, 0.0)}
    coord = {i: [rng.uniform(-1.0, 1.0), rng.uniform(-1.0, 1.0)] for i in ids}
    idx = {i: k for k, i in enumerate(ids)}
    W = H = 1000.0
    k = math.sqrt((W * H) / n)
    elist = [(idx[a], idx[b]) for a, b in
             ((e["from"], e["to"]) for e in edges) if a in idx and b in idx]
    temp = W / 10.0
    for _ in range(iters):
        disp = [[0.0, 0.0] for _ in range(n)]
        for i in range(n):
            for j in range(i + 1, n):
                dx = coord[ids[i]][0] - coord[ids[j]][0]
                dy = coord[ids[i]][1] - coord[ids[j]][1]
                d2 = dx * dx + dy * dy
                if d2 < 0.0001:
                    dx, dy = rng.uniform(-0.01, 0.01), rng.uniform(-0.01, 0.01)
                    d2 = dx * dx + dy * dy
                d = math.sqrt(d2)
                fr = (k * k) / d
                ux, uy = dx / d, dy / d
                disp[i][0] += ux * fr
                disp[i][1] += uy * fr
                disp[j][0] -= ux * fr
                disp[j][1] -= uy * fr
        for a, b in elist:
            dx = coord[ids[b]][0] - coord[ids[a]][0]
            dy = coord[ids[b]][1] - coord[ids[a]][1]
            d2 = dx * dx + dy * dy
            if d2 < 0.0001:
                continue
            d = math.sqrt(d2)
            fa = (d * d) / k
            ux, uy = dx / d, dy / d
            disp[a][0] += ux * fa
            disp[a][1] += uy * fa
            disp[b][0] -= ux * fa
            disp[b][1] -= uy * fa
        for i in range(n):
            x, y = coord[ids[i]]
            dx, dy = disp[i]
            mv = min(math.hypot(dx, dy), temp)
            scale = mv / math.hypot(dx, dy) if (dx or dy) else 0.0
            x += dx * scale
            y += dy * scale
            # gentle centering pull
            x += (-x) * 0.005
            y += (-y) * 0.005
            coord[ids[i]] = [x, y]
        temp *= 0.98
    # normalize to a tidy extent
    xs = [coord[i][0] for i in ids]
    ys = [coord[i][1] for i in ids]
    cx, cy = (max(xs) + min(xs)) / 2.0, (max(ys) + min(ys)) / 2.0
    span = max(max(xs) - min(xs), max(ys) - min(ys), 1e-6)
    target = 350.0
    for i in ids:
        x = (coord[i][0] - cx) / (span) * target
        y = (coord[i][1] - cy) / (span) * target
        pos[i] = (round(x, 3), round(y, 3))
    return pos


# --------------------------------------------------------------------------- #
# HTTP server                                                                  #
# --------------------------------------------------------------------------- #
def _json(handler: BaseHTTPRequestHandler, payload: dict | list) -> None:
    body = json.dumps(payload).encode("utf-8")
    handler.send_response(200)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.send_header("Cache-Control", "no-store")
    handler.end_headers()
    handler.wfile.write(body)


class GraphHandler(BaseHTTPRequestHandler):
    graph_root: Path = None  # type: ignore[assignment]

    def log_message(self, fmt, *args):                                 # noqa: A003
        sys.stderr.write("[graphweb] %s\n" % (fmt % args))

    def do_GET(self):                                                   # noqa: N802
        path = self.path.split("?")[0]
        if path in ("/graph.json", "/graph.json/"):
            _json(self, cached_build_graph(self.graph_root))
        elif path in ("/live.json", "/live.json/"):
            _json(self, live_view(self.graph_root))
        elif path in ("/", "/index.html"):
            page = _page_path(self.graph_root)
            body = page.read_bytes() if page.is_file() else PLACEHOLDER_PAGE.encode("utf-8")
            ctype = "text/html; charset=utf-8"
            if page.is_file() and page.suffix == ".html":
                ctype = "text/html; charset=utf-8"
            self.send_response(200)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(body)
        elif path == "/app.js":
            # static JS sibling of the page (kid 2 deliverable)
            js = _web_dir(self.graph_root) / "app.js"
            if js.is_file():
                body = js.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "application/javascript; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.send_header("Cache-Control", "no-store")
                self.end_headers()
                self.wfile.write(body)
            else:
                self.send_response(404)
                self.send_header("Content-Length", "0")
                self.end_headers()
        elif path in ("/favicon.ico",):
            self.send_response(204)
            self.end_headers()
        else:
            self.send_response(404)
            self.send_header("Content-Length", "0")
            self.end_headers()


def serve(graph_root: Path, host: str = "127.0.0.1", port: int = 8765) -> None:
    handler = type("BoundGraphHandler", (GraphHandler,), {"graph_root": graph_root})
    httpd = ThreadingHTTPServer((host, port), handler)
    print(f"graphweb serving {graph_root} on http://{host}:{port}", flush=True)
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        httpd.server_close()


# --------------------------------------------------------------------------- #
# CLI                                                                          #
# --------------------------------------------------------------------------- #
def main(argv=None) -> int:
    ap = argparse.ArgumentParser(
        prog="graphweb.py",
        description="agi 3D golden-web dashboard — server + layout (kid 1).")
    sub = ap.add_subparsers(dest="cmd")

    serve_p = sub.add_parser("serve", help="serve the dashboard on localhost")
    serve_p.add_argument("--host", default="127.0.0.1")
    serve_p.add_argument("--port", type=int, default=8765)
    serve_p.add_argument("--root", default=None,
                         help="explicit graph root (.agi); default: nearest from cwd")

    args = ap.parse_args(argv)
    if args.cmd == "serve":
        root = Path(args.root) if args.root else find_root()
        serve(root, args.host, args.port)
        return 0
    ap.error("a subcommand is required; see -h")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())