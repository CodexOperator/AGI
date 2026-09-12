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
import hashlib
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
    rec = _read_node_file(path)
    return rec["id"] if rec else None


#: Module-level per-file parse cache: {str(path): (mtime_ns, size, record)}.
#: One server process serves one graph root, so a per-file registry is exactly
#: the right size. Because `load_nodes` / `graph_version` re-parse ONLY files
#: whose (mtime, size) changed, a single body touch costs one re-parse (~ms)
#: instead of a full re-read of every node file (~2.5 s on the real tree).
#: This is defect B4 of the parent's amended build order — without it the
#: id/edge key could not be recomputed cheaply enough for the < 2 s proof.
_PARSE_CACHE: dict = {}


def _read_node_file(path: Path) -> dict | None:
    """Parse one node file with the stat cache. Returns
    {id,type,title,parents:[...],status} or None when the file has no usable
    id. Re-parses only when (mtime_ns, size) changed."""
    try:
        st = path.stat()
    except OSError:
        return None
    key = str(path)
    hit = _PARSE_CACHE.get(key)
    if hit is not None and hit[0] == st.st_mtime_ns and hit[1] == st.st_size:
        return hit[2]
    try:
        fm = parse_frontmatter(path.read_text(encoding="utf-8"))
    except Exception:                                             # noqa: BLE001
        return None
    nid = fm.get("id")
    if not isinstance(nid, str) or not nid:
        return None
    parents = fm.get("parents") or []
    if not isinstance(parents, list):
        parents = []
    rec = {
        "id": nid,
        "type": str(fm.get("type") or "node"),
        "title": str(fm.get("title") or nid),
        "parents": [str(x) for x in parents if x],
        "status": str(fm.get("status") or ""),
    }
    _PARSE_CACHE[key] = (st.st_mtime_ns, st.st_size, rec)
    return rec


def _iter_active_node_files(graph_root: Path):
    """Yield node .md files that are ACTIVE by PATH (not under
    `nodes/deprecated/` and not under `nodes/.geometry/`). Status-level
    filtering (deprecated) happens per record via the parse cache."""
    nodes_dir = Path(graph_root) / "nodes"
    if not nodes_dir.is_dir():
        return
    for p in nodes_dir.rglob("*.md"):
        if not p.is_file():
            continue
        rel = p.relative_to(nodes_dir)
        parts = rel.parts
        if parts and (parts[0] == "deprecated" or parts[0] == ".geometry"):
            continue
        yield p


def load_nodes(graph_root: Path) -> dict:
    """{id: {id,type,title,parents:[...]}} for every ACTIVE node.

    ACTIVE = not under `nodes/deprecated/` and not `.geometry/`, and
    `status` != 'deprecated'. `.geometry` carries housekeeping config (e.g.
    config:seats) that is not part of the goal tree; it is represented
    separately via the synthetic `seat:<name>` nodes.

    Reads go through the module-level per-file parse cache (`_PARSE_CACHE`),
    so a body edit that changes no id and no edge re-parses only the touched
    file (~ms) — the whole point is that a single-node edit must not cost a
    full re-read of every node file on the next /graph.json request.
    """
    out: dict = {}
    for p in _iter_active_node_files(graph_root):
        rec = _read_node_file(p)
        if rec is None or rec["status"] == "deprecated":
            continue
        out[rec["id"]] = {
            "id": rec["id"], "type": rec["type"],
            "title": rec["title"], "parents": rec["parents"],
        }
    return out


def graph_version(graph_root: Path) -> str:
    """A stable hash of the sorted ACTIVE id set (B5).

    Cheap — a stat sweep over the parse cache, ~0.03 s on the real tree — so
    kid 3 of this round can put it in `/live.json` and the page can poll it
    every 5 s without burning a core. It changes iff an id is added, removed
    or retired; it does NOT change on a body edit (so a body edit reuses the
    persisted layout byte-identically while graph_version stays put).
    """
    ids: set = set()
    for p in _iter_active_node_files(graph_root):
        rec = _read_node_file(p)
        if rec is None or rec["status"] == "deprecated":
            continue
        ids.add(rec["id"])
    digest = hashlib.sha256()
    for nid in sorted(ids):
        digest.update(nid.encode("utf-8"))
        digest.update(b"\n")
    return digest.hexdigest()[:12]


# --------------------------------------------------------------------------- #
# Seats / agents / live                                                        #
# --------------------------------------------------------------------------- #
def load_seats(graph_root: Path) -> list:
    """config:posts / config:seats rows (post-first, one-season seats
    fallback), else [].

    Falls back to config.json's (legacy) `seats` list when the geometry file
    is absent, so a project that keeps its registry in the config still
    resolves.
    """
    try:
        import geometry_config as _gc  # same bin dir (locations pattern)
    except Exception:                                             # noqa: BLE001
        _gc = None
    if _gc is not None:
        rows = _gc.load_rows(graph_root)
        if rows:
            return [dict(r) for r in rows]
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

    Reads `tmux list-windows` ONCE, scoped to the agi-rc session (rotate.py
    DEFAULT_TMUX_SESSION). Absent tmux / absent session -> empty, never a
    raise.
    """
    try:
        out = subprocess.run(
            ["tmux", "list-windows", "-t", "agi-rc"],
            capture_output=True, text=True,
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


def _resolve_worktree(worktree: str | None, graph_root: Path) -> Path | None:
    """Resolve a (possibly relative) worktree path, or None when it does not
    exist on disk.

    A RELATIVE worktree is resolved against the candidates, in order
    (hypothesis:l4-the-graph-as-a-golden-3d-web-in-two-layers):
        [git_common_root(graph_root), graph_root.parent]
    deduped. The first `<base>/<worktree>` that is a directory wins; none
    does -> None. `git_common_root` returns the MAIN CHECKOUT ROOT (the repo
    root owning `.agi/worktrees/`), so a seat row carrying the real shape
    `.agi/worktrees/seat-<name>` resolves correctly — the old resolver joined
    relative paths under `graph_root` itself (i.e. `.agi/worktrees/...` under
    `.agi/`), which silently yielded [] for every relative seat row (the
    claim's own falsifier). In a repo-less fixture `git_common_root` returns
    `graph_root` unchanged, and `graph_root.parent` is the fallback that
    catches the fixture (tmp) layout.
    """
    if not worktree:
        return None
    wt = Path(worktree).expanduser()
    if wt.is_absolute():
        return wt if wt.is_dir() else None
    try:
        import locations as _loc
        base0 = Path(_loc.git_common_root(graph_root))
    except Exception:                                             # noqa: BLE001
        base0 = Path(graph_root)
    bases: list = []
    for b in (base0, Path(graph_root).parent):
        if b not in bases:
            bases.append(b)
    for b in bases:
        cand = b / wt
        if cand.is_dir():
            return cand
    return None


def _worktree_modified_ids(worktree: str | None, graph_root: Path) -> list:
    """Node ids whose files are MODIFIED in `worktree`, or [].

    Resolves `worktree` when not absolute via `_resolve_worktree` (against
    the checkout root, not `graph_root`), runs
    `git -C <wt> status --porcelain -- .agi/nodes` once, maps each changed
    path to its node id. A dead/missing worktree or an absent git yields []
    (never a traceback).
    """
    wt = _resolve_worktree(worktree, graph_root)
    if wt is None:
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


def _worktree_for_agent(rec: dict, all_recs: list) -> str | None:
    """The worktree whose `git status` reflects a live agent's writes.

    A PARENT-tier (or director/prime) lease carries its OWN `worktree`, and
    its in-progress node files live there. A KID has NO worktree of its own
    — it writes its node INTO ITS PARENT'S worktree (`.agi/worktrees/<parent>`)
    — so for a kid this returns the parent-tier lease (SAME `iter`) worktree.
    None when no such worktree is on the lease(s).
    """
    own = rec.get("worktree")
    if own:
        return own
    if rec.get("tier") == "kid":
        for r2 in all_recs:
            if (r2.get("iter") == rec.get("iter")
                    and r2.get("tier") != "kid" and r2.get("worktree")):
                return r2["worktree"]
    return None


def _agent_parent_id(rec: dict, all_recs: list) -> str | None:
    """The parent agent id for a KID lease (the parent-tier lease with the
    same `iter`), else None for a parent/director/prime."""
    if rec.get("tier") != "kid":
        return None
    for r2 in all_recs:
        if r2.get("iter") == rec.get("iter") and r2.get("tier") != "kid":
            return r2.get("agent_id")
    return None


_MANIFEST_NAME = "manifest.json"


def _agent_target(rec: dict, all_recs: list, graph_root: Path) -> str:
    """A live agent's target node id from its iteration manifest, "" when
    the manifest or its entry is unreadable.

    The target is the node the agent is building — recorded in the dispatch
    manifest `agents[].target`. For a PARENT the manifest lives in its own
    worktree (`<worktree>/.agi/sessions/iter-<iter>/manifest.json`); for a
    KID the manifest lives in its PARENT's worktree (same `iter`). Every read
    is wrapped: an absent manifest, a corrupt file, or a missing entry all
    yield "" and never a traceback (hypothesis:l4-the-graph-as-a-golden-3d-
    web-in-two-layers, the owner's ghost-node order).
    """
    rec_iter = rec.get("iter")
    if not rec_iter:
        return ""
    wt = _worktree_for_agent(rec, all_recs)
    candidates: list = []
    if wt:
        candidates.append(Path(wt).expanduser() / ".agi" / "sessions"
                          / f"iter-{rec_iter}" / _MANIFEST_NAME)
    for mpath in candidates:
        try:
            data = json.loads(mpath.read_text(encoding="utf-8"))
        except Exception:                                             # noqa: BLE001
            continue
        if not isinstance(data, dict):
            continue
        agents = data.get("agents")
        if not isinstance(agents, list):
            continue
        aid = rec.get("agent_id")
        for entry in agents:
            if isinstance(entry, dict) and entry.get("id") == aid:
                t = entry.get("target")
                if isinstance(t, str) and t:
                    return t
        # fallback: any entry's target (all kids of one iteration usually
        # share the iteration target).
        for entry in agents:
            if isinstance(entry, dict):
                t = entry.get("target")
                if isinstance(t, str) and t:
                    return t
    return ""


def _new_node_records(worktree: str | None, graph_root: Path,
                      agent_id: str | None = None) -> list:
    """{id,type,title,parents} for every NEW (`??` untracked or `A` added)
    node file in `worktree`'s `git status --porcelain -- .agi/nodes`.

    Used for ghost nodes: an agent whose node file is not yet committed (a
    kid's file is untracked in its parent's worktree) should render as a
    semi-transparent circle that SNAPS to the real frontmatter once the file
    exists — so the page can show real details BEFORE the node reaches the
    served `/graph.json`. When `agent_id` is given (kids), only ids that
    CONTAIN it are kept (a kid's own in-progress node id embeds its agent
    id). Every read wrapped; absent worktree / git / unparseable files
    yield [] and never a traceback.
    """
    wt = _resolve_worktree(worktree, graph_root)
    if wt is None:
        return []
    try:
        out = subprocess.run(
            ["git", "-C", str(wt), "status", "--porcelain", "--", ".agi/nodes"],
            capture_output=True, text=True, timeout=20, check=False)
    except Exception:                                             # noqa: BLE001
        return []
    if out.returncode != 0:
        return []
    recs: list = []
    seen: set = set()
    for cl in out.stdout.splitlines():
        line = cl.rstrip("\n")
        if not line:
            continue
        if line[:2].strip() not in ("??", "A"):
            continue  # only NEW files carry the future node's real details
        if "->" in line:
            path = line.split("->")[-1].strip()
        else:
            path = line[3:].strip()
        if not path:
            continue
        node_path = wt / path
        rec = _read_node_file(node_path)
        if rec is None:
            continue
        nid = rec["id"]
        if agent_id and agent_id not in nid:
            continue
        if nid in seen:
            continue
        seen.add(nid)
        recs.append({"id": nid, "type": rec["type"],
                     "title": rec["title"], "parents": rec["parents"]})
    return recs


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
    all_recs = live_agents(graph_root)
    agents: list = []
    for rec in all_recs:
        agent = rec.get("agent_id")
        if not agent:
            continue
        # For a KID the worktree is its PARENT's (kids write into the parent
        # worktree), so working_on / new_nodes below read the same place.
        wt = _worktree_for_agent(rec, all_recs)
        tier = rec.get("tier")
        agents.append({
            "agent": agent,
            "iter": rec.get("iter"),
            "tier": tier,
            "dispatched_by": _dispatched_by(rec),
            "working_on": _worktree_modified_ids(wt, graph_root),
            "target": _agent_target(rec, all_recs, graph_root),
            "parent": _agent_parent_id(rec, all_recs),
            "new_nodes": _new_node_records(
                wt, graph_root, agent if tier == "kid" else None),
        })
    return {"seats": seat_rows, "agents": agents,
            "graph_version": graph_version(graph_root)}


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


#: Where the persisted layout lives, under the graph root. gitignored by the
#: repo (`extensions/agi/.gitignore`-chain: `.agi/sessions/*`).
LAYOUT_FILE_RELPATH = Path("sessions") / "graphweb-layout.json"

#: In-process memo for the identical-signature fast path, so a warm
#: /graph.json request does not even re-read the persisted file. One server
#: process serves one graph root and only a handful of id-set generations
#: accumulate over a loop, so a small bounded registry is the right size.
#: Keyed by (graph_root, signature) -> {0: pos0, 1: pos1}.
_POS_MEMO: dict = {}


def _layout_key(layer_ids0, layer_ids1, edges0, edges1) -> str:
    """Stable signature over each layer's NODE-ID SET + EDGE SET (NOT node
    file mtimes). An edit that changes no id and no edge yields the same key
    and therefore reuses every position byte-identically (B1)."""
    def sig(ids, edges):
        parts = list(ids)
        parts += sorted(f"{e.get('from')}\x00{e.get('to')}" for e in edges)
        return "|".join(sorted(parts))
    return f"{sig(layer_ids0, edges0)};;;{sig(layer_ids1, edges1)}"


def _load_persisted_layout(graph_root: Path) -> dict | None:
    """{signature, layer0:{id:[x,y]}, layer1:{...}} or None. Treats a
    missing/corrupt/wrong-shape file as absent (B1)."""
    p = Path(graph_root) / LAYOUT_FILE_RELPATH
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except Exception:                                             # noqa: BLE001
        return None
    if not isinstance(data, dict) or not isinstance(data.get("signature"), str):
        return None
    for layer in ("layer0", "layer1"):
        pos = data.get(layer)
        if not isinstance(pos, dict):
            return None
        clean = {}
        for k, v in pos.items():
            if isinstance(v, (list, tuple)) and len(v) == 2:
                try:
                    clean[str(k)] = [float(v[0]), float(v[1])]
                except (TypeError, ValueError):
                    pass
        data[layer] = clean
    return data


def _save_persisted_layout(graph_root: Path, signature: str,
                           pos0: dict, pos1: dict) -> None:
    """Atomic write (tmp file + os.replace) of the layout keyed by the
    id+edge signature. A crash mid-write leaves only a `.tmp` file, which is
    never read — os.replace swaps the whole file in one atomic step (B1)."""
    data = {
        "kind": "graphweb-layout",
        "version": 1,
        "signature": signature,
        "layer0": {str(k): v for k, v in pos0.items()},
        "layer1": {str(k): v for k, v in pos1.items()},
    }
    p = Path(graph_root) / LAYOUT_FILE_RELPATH
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + ".tmp")
    try:
        tmp.write_text(json.dumps(data), encoding="utf-8")
        os.replace(tmp, p)
    except Exception:                                             # noqa: BLE001
        # Never let a persistence failure break the serve path; the layout
        # is still fully valid in-memory for this process.
        pass


def _centroid(coord: dict) -> list:
    if not coord:
        return [0.0, 0.0]
    n = len(coord)
    return [sum(v[0] for v in coord.values()) / n,
            sum(v[1] for v in coord.values()) / n]


def resolve_positions(graph_root: Path, layer0: set, layer1: set,
                      edges0: list, edges1: list,
                      seed: int = LAYOUT_SEED):
    """Positions {0: pos0, 1: pos1} for the two layers (B1/B2/B3).

    - persisted layout with the SAME signature -> reuse every position
      byte-identically (a body edit changes no id and no edge, so it lands
      here).
    - a persisted layout with OVERLAPPING ids -> incremental: survivors keep
      their exact positions, new ids are seeded at their first parent + a
      small seeded jitter, and only the new nodes relax (short, <= 6 iters);
      removed ids are dropped.
    - no persisted layout at all -> the bounded full cold build.

    The result is persisted atomically (B1), so a server restart reuses it
    rather than re-paying the cold build.
    """
    sig = _layout_key(layer0, layer1, edges0, edges1)
    memo_key = (str(Path(graph_root).resolve()), sig)
    hit = _POS_MEMO.get(memo_key)
    if hit is not None:
        return hit
    prev = _load_persisted_layout(graph_root)
    if prev is not None and prev.get("signature") == sig:
        # byte-identical reuse — positions loaded as-is, no re-layout.
        pos0, pos1 = prev["layer0"], prev["layer1"]
    else:
        surv0 = prev["layer0"] if prev is not None else {}
        surv1 = prev["layer1"] if prev is not None else {}
        pos0 = _positions_of_layer(layer0, edges0, surv0, seed)
        pos1 = _positions_of_layer(layer1, edges1, surv1, seed)
        _save_persisted_layout(graph_root, sig, pos0, pos1)
    out = {0: pos0, 1: pos1}
    _POS_MEMO[memo_key] = out
    if len(_POS_MEMO) > 16:
        for old in list(_POS_MEMO)[:-8]:
            _POS_MEMO.pop(old, None)
    return out


def _positions_of_layer(ids: set, edges: list, surviving: dict,
                        seed: int) -> dict:
    """Positions for one layer: incremental when a previous layout left
    intact positions for still-present ids, else the bounded full cold
    layout."""
    if not ids:
        return {}
    if not surviving:
        return _force_layout(ids, edges, seed=seed)
    return _incremental_layout(surviving, ids, edges, seed=seed)


def cached_build_graph(graph_root: Path, seed: int = LAYOUT_SEED) -> dict:
    """build_graph, with the layout already persisted+memoized so a warm (or
    body-edit) request reuses every position byte-identically instead of
    re-paying the cold build. The old mtime-keyed cache is GONE: it busted on
    every node edit, which is exactly the defect B fixes.

    Keep the memo AND the persisted file in front: the memo is the fast path
    for the identical signature across requests, the file is what survives a
    server restart and what seeds the incremental path on an id change.
    """
    return build_graph(graph_root, seed=seed)


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
    pos = resolve_positions(graph_root, layer0, layer1, edges0, edges1,
                            seed=seed)
    pos0, pos1 = pos[0], pos[1]

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


def _force_layout(ids: set, edges: list, seed: int, iters: int = 30) -> dict:
    """Seeded Fruchterman-Reingold in-plane layout, BOUNDED (B3).

    The cold build must finish in well under 20 s on a ~2100-node graph. The
    old code was O(n^2) x 180 iterations in pure Python (~170 s). Two changes
    bound it:
      * repulsion is binned on a grid (cells of the layout span / 8, minimum
        one ideal-distance wide); each node repulses only within its own and
        its 8 neighbouring cells, reducinng pairs from O(n^2) to O(n * local
        density) per iteration.
      * the seed is spread across the whole plane (not the old tight
        uniform[-1,1] cluster), so the grid is sparse from iteration 1 — a
        tight seed would pile every node into one cell and reintroduce O(n^2)
        for the early iterations.
    Returns {id:(x,y)} rounded to 3 places (byte-stable).
    """
    ids = list(ids)
    n = len(ids)
    if n == 0:
        return {}
    if n == 1:
        return {ids[0]: [0.0, 0.0]}
    rng = random.Random(seed)
    W = H = 1000.0
    k = math.sqrt((W * H) / n)
    coord = {i: [rng.uniform(0.0, W), rng.uniform(0.0, H)] for i in ids}
    idx = {i: j for j, i in enumerate(ids)}
    elist = [(idx[e["from"]], idx[e["to"]]) for e in edges
             if e["from"] in idx and e["to"] in idx]
    temp = W / 10.0
    for _ in range(iters):
        disp = {i: [0.0, 0.0] for i in ids}
        xs = [coord[i][0] for i in ids]
        ys = [coord[i][1] for i in ids]
        span = max(max(xs) - min(xs), max(ys) - min(ys))
        cellsz = max(span / 8.0, k)
        minx, miny = min(xs), min(ys)
        grid: dict = {}
        for i in ids:
            cx = int((coord[i][0] - minx) / cellsz)
            cy = int((coord[i][1] - miny) / cellsz)
            grid.setdefault((cx, cy), []).append(i)

        def repulse(a, b):
            dx = coord[a][0] - coord[b][0]
            dy = coord[a][1] - coord[b][1]
            d2 = dx * dx + dy * dy
            if d2 < 0.0001:
                dx = rng.uniform(-0.01, 0.01)
                dy = rng.uniform(-0.01, 0.01)
                d2 = dx * dx + dy * dy
            d = math.sqrt(d2)
            fr = (k * k) / d
            ux, uy = dx / d, dy / d
            disp[a][0] += ux * fr
            disp[a][1] += uy * fr
            disp[b][0] -= ux * fr
            disp[b][1] -= uy * fr

        for (cx, cy), members in grid.items():
            m = members
            for ia in range(len(m)):
                za = m[ia]
                for ib in range(ia + 1, len(m)):
                    repulse(za, m[ib])
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    nkey = (cx + dx, cy + dy)
                    if nkey < (cx, cy):
                        continue  # count each cell-pair once
                    nb = grid.get(nkey)
                    if not nb:
                        continue
                    for za in m:
                        for zb in nb:
                            repulse(za, zb)
        # spring forces (cheap: O(E))
        for a, b in elist:
            dx = coord[ids[b]][0] - coord[ids[a]][0]
            dy = coord[ids[b]][1] - coord[ids[a]][1]
            d2 = dx * dx + dy * dy
            if d2 < 0.0001:
                continue
            d = math.sqrt(d2)
            fa = (d * d) / k
            ux, uy = dx / d, dy / d
            disp[ids[a]][0] += ux * fa
            disp[ids[a]][1] += uy * fa
            disp[ids[b]][0] -= ux * fa
            disp[ids[b]][1] -= uy * fa
        for i in ids:
            x, y = coord[i]
            dx, dy = disp[i]
            mv = min(math.hypot(dx, dy), temp)
            scale = mv / math.hypot(dx, dy) if (dx or dy) else 0.0
            x += dx * scale
            y += dy * scale
            x += (-x) * 0.005
            y += (-y) * 0.005
            coord[i] = [x, y]
        temp *= 0.98
    # normalize to a tidy extent
    xs = [coord[i][0] for i in ids]
    ys = [coord[i][1] for i in ids]
    cx, cy = (max(xs) + min(xs)) / 2.0, (max(ys) + min(ys)) / 2.0
    span = max(max(xs) - min(xs), max(ys) - min(ys), 1e-6)
    target = 350.0
    pos = {}
    for i in ids:
        x = (coord[i][0] - cx) / (span) * target
        y = (coord[i][1] - cy) / (span) * target
        pos[i] = [round(x, 3), round(y, 3)]
    return pos


def _incremental_layout(surviving: dict, ids: set, edges: list,
                        seed: int, iters: int = 6) -> dict:
    """Short incremental relaxation (B2): ids present in `surviving` KEEP
    their exact positions (PINNED — byte-identical), ids new to this layer
    are seeded at their first parent's position + a small seeded jitter
    (<= 1.5 units) and relax for at most `iters` iterations. Removed ids are
    dropped simply by not appearing in the result. NEVER the full cold pass.

    A strong snap-back toward the parent keeps a lone new node hugging its
    parent's position, which is what the "new node within 2 units of its
    parent" fixture assertion checks.
    """
    ids = set(ids)
    coord = {nid: [float(v[0]), float(v[1])]
             for nid, v in surviving.items() if nid in ids}
    pinned = set(coord)
    new_ids = sorted(ids - pinned)
    if not new_ids:
        return coord
    rng = random.Random(seed)
    centroid = _centroid(coord) if coord else [0.0, 0.0]
    parent_pos: dict = {}
    for e in edges:
        child = e.get("from")
        par = e.get("to")
        if child in new_ids and par in coord:
            parent_pos.setdefault(child, coord[par])
    for nid in new_ids:
        base = parent_pos.get(nid, centroid)
        coord[nid] = [base[0] + rng.uniform(-1.5, 1.5),
                      base[1] + rng.uniform(-1.5, 1.5)]
    elist = [(e["from"], e["to"]) for e in edges
             if e["from"] in ids and e["to"] in ids]
    temp = 0.6
    k = math.sqrt((1000.0 * 1000.0) / max(1, len(ids)))
    for _ in range(iters):
        disp = {nid: [0.0, 0.0] for nid in new_ids}
        # repulsion felt by movers against ALL nodes (few movers -> cheap)
        for a in new_ids:
            for b in coord:
                if a == b:
                    continue
                dx = coord[a][0] - coord[b][0]
                dy = coord[a][1] - coord[b][1]
                d2 = dx * dx + dy * dy
                if d2 < 0.0001:
                    dx = rng.uniform(-0.01, 0.01)
                    dy = rng.uniform(-0.01, 0.01)
                    d2 = dx * dx + dy * dy
                d = math.sqrt(d2)
                fr = (k * k) / d
                ux, uy = dx / d, dy / d
                disp[a][0] += ux * fr
                disp[a][1] += uy * fr
        # springs on edges touching movers
        for a, b in elist:
            in_a = a in coord
            in_b = b in coord
            if not ((a in new_ids and in_a) or (b in new_ids and in_b)):
                continue
            dx = coord[b][0] - coord[a][0]
            dy = coord[b][1] - coord[a][1]
            d2 = dx * dx + dy * dy
            if d2 < 0.0001:
                continue
            d = math.sqrt(d2)
            fa = (d * d) / k
            ux, uy = dx / d, dy / d
            if a in new_ids:
                disp[a][0] += ux * fa
                disp[a][1] += uy * fa
            if b in new_ids:
                disp[b][0] -= ux * fa
                disp[b][1] -= uy * fa
        for nid in new_ids:
            dx, dy = disp[nid]
            mv = min(math.hypot(dx, dy), temp)
            scale = mv / math.hypot(dx, dy) if (dx or dy) else 0.0
            coord[nid][0] += dx * scale
            coord[nid][1] += dy * scale
            base = parent_pos.get(nid, centroid)
            coord[nid][0] += (base[0] - coord[nid][0]) * 0.35
            coord[nid][1] += (base[1] - coord[nid][1]) * 0.35
        temp *= 0.7
    pos: dict = {}
    for nid in sorted(ids):
        x, y = coord[nid]
        pos[nid] = [round(x, 3), round(y, 3)]
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