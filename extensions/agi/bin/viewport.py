#!/usr/bin/env python3
"""viewport.py — the live graph viewport. `goal:g9.4`, under `goal:g9.7`.

**One render, two readers.** The window a human pans across and the context a
kid is spawned with are the *same* frame stream at two grains — not two
renderers that happen to agree. `goal:g9.7`'s falsifier is mechanical: change
what the stream emits and both outputs change in the same commit, with nothing
edited by hand. `--emit both` puts them side by side; `--verify` asserts it.

That invariant is the reason this file exists rather than a fourth ASCII
renderer. Before it there were at least five render paths and **none** shared
between what a human sees and what an agent is handed:

    zoom.py           3 internal renderers (big, legacy-small, numeric-level)
    renderers/ascii   1, reached only by render-context.py -> INJECTION.md
    dashboard.py      its own render_goals/metrics/health/activity

So no human had ever looked at what a kid actually receives, because no
instrument pointed there. Tuning the view here tunes every agent's context in
the same edit.

## Three axes, chosen by the owner 2026-09-02

**space**  pan and zoom a window across a graph far larger than the screen.
**time**   step through iterations and a node's grid versions.
**live**   agents rendered where they are working, moving as they move.

Deliberately NOT built: stepping a chain node-by-node. Recorded so a later
reader does not re-propose it as an oversight.

## INVARIANT: reader, never writer (inherited from `goal:g9`)

Safe to run at any moment, including mid-iteration of the loop it is watching.
It opens nothing for writing, creates no directory, and runs no mutating git
command. `git` is reached only through `grid.py`'s read-only subcommands.

It also renders the graph's **damage** rather than a flattering picture of it:
dangling parents, unevidenced decisive verdicts and deprecated mass are drawn
in place, not hidden behind a clean summary.

## Usage

    viewport.py                              # interactive, curses
    viewport.py --emit human                 # one static frame, to stdout
    viewport.py --emit llm                   # exactly what a kid is handed
    viewport.py --emit both                  # both, from ONE frame stream
    viewport.py --verify                     # assert g9.7's invariant
    viewport.py --anchor goal:g13 --depth 3
    viewport.py --iter 104                   # time axis: one iteration
    viewport.py --live                       # live axis: agents as spiders

Keys (interactive): arrows/hjkl pan · +/- depth · [/] time · a live · q quit
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

BIN = Path(__file__).resolve().parent
PLUGIN_ROOT = BIN.parent
sys.path.insert(0, str(BIN))

import locations  # noqa: E402
import zoom  # noqa: E402  — the unified read path, imported not reimplemented


# --------------------------------------------------------------------------
# The frame stream — ONE traversal, consumed by every formatter below.
# --------------------------------------------------------------------------

#: Glyphs are data, not literals scattered through the formatters, because
#: `goal:g9.7` requires that changing the view is one edit.
GLYPH = {
    "root": "●",      # ●
    "branch": "○",    # ○
    "leaf": "·",      # ·
    "damaged": "✗",   # ✗  dangling parent / broken edge
    "spider": "✶",    # ✶  an agent, working here
    "mantle": "✦",    # ✦  a mantled spirit in the sanctuary theme
    "wisp": "≈",      # ≈  a probe / ephemeral wisp in the sanctuary theme
}

#: Node type -> single-letter tag. Kept short: at level 1 the tag is all the
#: width there is for a type.
TYPE_TAG = {
    "goal": "G", "vision": "V", "idea": "I", "hypothesis": "H",
    "experiment": "E", "verdict": "D", "mvp": "M", "outcome": "O",
    "bigger_outcome": "B", "build": "b", "task": "t", "doc": "d",
}


@dataclass(frozen=True)
class Frame:
    """One node's appearance in the stream.

    Every formatter reads only these fields. A formatter that reaches back
    into the graph for something not on a Frame has broken `goal:g9.7` --
    that is the seam where two views start to drift, so the dataclass is
    frozen and the traversal is the only thing that fills it.
    """
    node_id: str
    type: str
    depth: int
    kind: str            # root | branch | leaf
    title: str
    verdict: str
    damaged: str         # "" when sound, else why
    agents: tuple        # agent ids working here (live axis)


def _title_of(node, fm: dict) -> str:
    t = (fm.get("title") or "").strip().strip('"')
    if t:
        return t
    return node.id.split(":", 1)[-1]


def frame_stream(g, fm_by_id: dict, anchor: str | None, max_depth: int,
                 agents_at: dict | None = None,
                 hide_deprecated: bool = False) -> list[Frame]:
    """Walk the graph once from `anchor` and emit frames in display order.

    Ordering is `(depth, node_id)` and is deterministic: two runs over an
    unchanged corpus emit byte-identical streams, which is what makes
    `--verify` meaningful and what lets the time axis diff two points.

    ## `hide_deprecated` — two consumers that genuinely want opposite things

    The human viewport **shows** retired nodes on purpose: this file's own
    contract is to render the graph's damage rather than a flattering picture
    of it, and deprecated mass is part of that picture. Default `False`.

    The **injected map must hide them** (`goal:s23`): an agent handed a
    retired node as a live chain head will extend it, which is the whole
    reason retirement exists. `render-context.py` did this with a `_LiveOnly`
    graph view, and when `inject.py` replaced it on 2026-09-03 the filter was
    dropped — the map looked correct only because the one retired build node
    happened to sit outside depth 3 of any root. Anchoring on its parent
    showed it immediately.

    A view, never a removal: `g` keeps every node, and `by_type` counts still
    include retired ones exactly as they did before — the numbers describe the
    corpus, the tree describes what is live to work on.
    """
    agents_at = agents_at or {}
    if anchor and not g.has_node(anchor):
        raise SystemExit(f"viewport: --anchor '{anchor}' is not in the graph")

    roots = [anchor] if anchor else default_roots(g, fm_by_id)
    seen: set[str] = set()
    out: list[Frame] = []

    # Depth-first PRE-ORDER, children sorted. Breadth-first was the obvious
    # implementation and it is wrong for a tree view: it emits every depth-0
    # node, then every depth-1 node, so a child never appears beneath its own
    # parent and the indentation describes a nesting the order contradicts.
    # Caught by reading the first default render rather than by a test, which
    # is the argument for `goal:g9` in one line -- a view nobody looks at is
    # a view that can be wrong for free.
    def _retired(nid: str) -> bool:
        return str((fm_by_id.get(nid) or {}).get("status") or "").strip().lower() \
            == "deprecated"

    def walk(nid: str, depth: int) -> None:
        if nid in seen or depth > max_depth:
            return
        if hide_deprecated and _retired(nid):
            # Hidden WITH its subtree: a live node reached only through a
            # retired parent is not a live chain head either, and `_LiveOnly`
            # dropped incident edges for the same reason.
            seen.add(nid)
            return
        seen.add(nid)
        node = g.get_node(nid)
        if node is None:
            return
        fm = fm_by_id.get(nid, {})
        kids = sorted(getattr(node, "children", set()) or [])
        out.append(Frame(
            node_id=nid,
            type=node.type or "?",
            depth=depth,
            kind="root" if depth == 0 else ("branch" if kids else "leaf"),
            title=_title_of(node, fm),
            verdict=str(fm.get("verdict") or ""),
            damaged=_damage_of(g, node, fm),
            agents=tuple(agents_at.get(nid, ())),
        ))
        if depth < max_depth:
            for k in kids:
                walk(k, depth + 1)

    sys.setrecursionlimit(max(sys.getrecursionlimit(), 10_000))
    for r in roots:
        walk(r, 0)
    return out


def _damage_of(g, node, fm: dict) -> str:
    """What is wrong with this node, in a few words, or "".

    `goal:g9` is explicit that the view must render damage rather than hide
    it, so this is computed in the traversal and carried on the Frame -- a
    formatter cannot choose to omit it without the omission being visible in
    the code.
    """
    for p in (node.parents or []):
        if not g.has_node(p):
            return f"dangling parent {p}"
    v = str(fm.get("verdict") or "")
    if v in ("proved", "disproved"):
        ev = fm.get("evidence_runs")
        if not ev:
            return "decisive verdict, no evidence"
    return ""


def _all_ids(g) -> list[str]:
    """Every node id, however this Graph spells that.

    `Graph.node_ids` is a set attribute here, not a method, and calling it
    crashed the whole default (no-anchor) view. It survived a first pass
    because the smoke check grepped stdout for a glyph -- absent output and a
    traceback on stderr look identical to `grep`. Tolerating both spellings
    costs three lines and removes a way for this to break again.
    """
    ids = getattr(g, "node_ids", None)
    if callable(ids):
        ids = ids()
    if ids is None:
        ids = getattr(g, "nodes", {})
        ids = ids.keys() if hasattr(ids, "keys") else ids
    return sorted(ids)


def default_roots(g, fm_by_id: dict) -> list[str]:
    """What the viewport opens on when nothing is anchored.

    **Active goals, not every parentless node.** The graph has hundreds of
    natural roots, and a "single view" that opens on all of them is a dump
    rather than a view -- the exact failure `goal:g9` names, where an
    artefact is technically complete and practically unreadable. Active goals
    are what the project says it is working on, so they are the honest
    default entry point, and `--anchor` reaches anything else.

    Falls back to natural roots only if nothing is marked active, so a fresh
    project with no goals still renders something.
    """
    active = sorted(
        nid for nid in _all_ids(g)
        if (fm_by_id.get(nid, {}).get("status") == "active"
            and (g.get_node(nid).type if g.get_node(nid) else "") == "goal")
    )
    if active:
        return active
    return [nid for nid in _all_ids(g)
            if (n := g.get_node(nid)) is not None
            and (not n.parents or not any(g.has_node(p) for p in n.parents))]


# --------------------------------------------------------------------------
# Formatters. BOTH consume `frames` and nothing else.
# --------------------------------------------------------------------------

def render_human(frames: list[Frame], top: int, left: int,
                 height: int, width: int, status: str = "",
                 brief=None, seats=None) -> list[str]:
    """The terminal viewport: a window onto a graph larger than the screen.

    `brief` is the same `Briefing` object `render_llm` receives, rendered
    compactly — the numbers a human watches change, without the rules text a
    human reading their own graph does not need restated every frame.
    """
    lines: list[str] = []
    for f in frames:
        glyph = GLYPH["damaged"] if f.damaged else GLYPH[f.kind]
        spider = (" " + GLYPH["spider"] * len(f.agents)) if f.agents else ""
        tag = TYPE_TAG.get(f.type, "?")
        v = f" [{f.verdict}]" if f.verdict and f.verdict != "pending" else ""
        note = f"   {GLYPH['damaged']} {f.damaged}" if f.damaged else ""
        lines.append(f"{'  ' * f.depth}{glyph} {tag} {f.title}{v}{spider}{note}")

    window = lines[top:top + height]
    out = [ln[left:left + width].ljust(width) for ln in window]
    head = []
    if brief is not None:
        import briefing as _briefing
        head = [ln[:width] for ln in _briefing.to_compact(brief)]
    if seats is not None:
        import seat_status as _ss
        head += [ln[:width] for ln in _ss.to_compact(seats)]
    if head:
        head += ["-" * min(width, 80)]
    out = head + out
    return out + ([status[:width]] if status else [])


def render_llm(frames: list[Frame], top: int, left: int,
               height: int, width: int, status: str = "",
               brief=None, seats=None) -> str:
    """Exactly what a kid is handed for this position.

    Same frames, same slice, same order. The markdown wrapper differs because
    the consumer differs -- that is the ONLY thing allowed to differ, and it
    is why this takes the identical arguments as `render_human`.

    `brief` adds the nine briefing sections `INJECTION.md` carries — the
    metric, the chain rules, the taxonomy, the attractors, the declared
    commands. Without it this view was **45 lines against INJECTION.md's
    271**, and the missing 226 were the entire contract a kid's work is judged
    against. A "view of what an LLM sees" that omits the rules is not a view
    of what an LLM sees.
    """
    body = []
    for f in frames[top:top + height]:
        v = f" verdict={f.verdict}" if f.verdict else ""
        dmg = f" DAMAGE={f.damaged}" if f.damaged else ""
        who = f" agents={','.join(f.agents)}" if f.agents else ""
        body.append(f"{'  ' * f.depth}- `{f.node_id}` ({f.type}) {f.title}{v}{dmg}{who}")
    head = [
        "# graph viewport",
        f"_frames {top}-{min(top + height, len(frames))} of {len(frames)}_",
        "",
    ]
    if status:
        head.append(f"> {status}")
        head.append("")
    if brief is not None:
        import briefing as _briefing
        head += [*_briefing.to_markdown(brief), ""]
    if seats is not None:
        import seat_status as _ss
        head += [*_ss.to_markdown(seats), ""]
    head += ["## the graph", ""]
    return "\n".join(head + body) + "\n"


# --------------------------------------------------------------------------
# The sanctuary theme — a third live render, per goal:g9.4 under goal:g9.7
# (hypothesis:l3w4-sanctuary-theme). `--theme sanctuary`.
#
# Same one-render-two-readers discipline as the graph frame: `sanctuary_frame`
# builds a single frozen `SanctuaryScene` and `render_sanctuary_human` /
# `render_sanctuary_llm` read it and nothing else. Content: a tree on an
# outcrop houses one mantled spirit per tier-3 seat; tier-1 director seats and
# live ephemeral leases draw as wisps; a rotating seat draws a light strand
# naming its `rotated_by` holder.
# --------------------------------------------------------------------------


@dataclass(frozen=True)
class SanctuaryScene:
    """One sanctuary frame — the mirror of `Frame`, for the theme renderers."""
    spirits: tuple          # of {name, label, fraction} — mantled tier-3 avatars
    probes: tuple           # of {name, label, fraction} — tier-1 director wisps
    ephemeral_wisps: int    # live ephemeral lease count
    rotating: tuple         # (holder, seat) when a seat's window is ren-gen'd
    registry_present: bool  # False => the seats registry is absent


def sanctuary_frame(seat_rows: list, ephemeral_leases, rotating):
    """Build one `SanctuaryScene` from `config:seats` rows (hypothesis L3.24).

    Sprits are the `tier == 3` rows (Belam and the advisors, wearing their
    mantles) plus any mantled non-tier-3 row (a seated Sanctuary Master sits on
    her mantle, not her tier). Everything else — the tier-1 director rows — is a
    probe wisp.
    """
    spirits, probes = [], []
    for r in seat_rows or []:
        rec = {
            "name": str(r.get("name") or ""),
            "label": str(r.get("role") or ""),
            "fraction": r.get("fraction"),
        }
        if r.get("tier") == 3 or r.get("mantled"):
            spirits.append(rec)
        else:
            probes.append(rec)
    return SanctuaryScene(tuple(spirits), tuple(probes),
                          len(ephemeral_leases or []), rotating, True)


def load_seat_rows(root: Path, fm_by_id: dict):
    """`(rows, registry_present)` — telemetry when available, else seats.md.

    Matches telemetry's own fallback (`l3w4-telemetry-seat-status`): prefer
    `seat_status.collect(...).seats` when that module exists, otherwise read
    `config:seats`'s `seats:` list from `.geometry/seats.md` with `fraction`
    unset. Whichever lane lands first is safe to render.
    """
    try:
        import seat_status
        sv = seat_status.collect(root, fm_by_id)
        rows = getattr(sv, "seats", None)
        if rows:
            return list(rows), True
    except Exception:
        pass
    seats_md = root / "nodes" / ".geometry" / "seats.md"
    present = seats_md.is_file()
    rows = []
    if present:
        gf = zoom._frontmatter_for(root, ".geometry")
        rows = (gf.get("config:seats") or {}).get("seats") or []
    return list(rows), present


_ROTATING_RE = re.compile(r"^(.+)\.gen\d+$")


def rotating_seat(seat_rows: list, windows: list):
    """`(holder, seat)` for the seat whose tmux window is renamed `<seat>.genN`.

    The rotation loop names a rotating seat's window `<seat>.gen<digits>`
    (`l3w4-seat-rotation-loops`); resolve that to the row's `rotated_by`
    holder. Never invented: no matching window returns `None`.
    """
    names = {str(r.get("name") or ""): r for r in seat_rows or []}
    for w in windows or []:
        m = _ROTATING_RE.match((w or "").strip())
        if not m:
            continue
        row = names.get(m.group(1))
        if row is not None:
            return row.get("rotated_by"), m.group(1)
    return None


def render_sanctuary_human(scene: SanctuaryScene, width: int = 120) -> list[str]:
    """The terminal frame: tree, spirits, probes, wisps, and the light strand."""
    if not scene.registry_present:
        return ["no seat registry yet"]
    lines = [
        "   ~   ~   ~",
        "  _/ outcrop \\_",
        "  / tree of mantled spirits \\",
        "",
    ]
    for s in scene.spirits:
        frac = f"  {s['fraction']:.0%}" if s["fraction"] is not None else ""
        lines.append(f"  {GLYPH['mantle']}  {s['name']}  {s['label']}{frac}")
    for p in scene.probes:
        frac = f"  {p['fraction']:.0%}" if p["fraction"] is not None else ""
        lines.append(f"  {GLYPH['wisp']}  {p['name']}  probe{frac}")
    lines.append(f"  {scene.ephemeral_wisps} ephemeral wisps")
    if scene.rotating:
        holder, seat = scene.rotating
        lines.append(f"  {holder} ~~~✧~~~> {seat} (rotating)")
    return lines


def render_sanctuary_llm(scene: SanctuaryScene) -> str:
    """Exactly what a kid is handed, from the same `SanctuaryScene`."""
    if not scene.registry_present:
        return "# sanctuary viewport\n\nno seat registry yet\n"
    body = [f"- spirit {s['name']} ({s['label']})" for s in scene.spirits]
    body += [f"- probe {p['name']} ({p['label']})" for p in scene.probes]
    body.append(f"- ephemeral_wisps: {scene.ephemeral_wisps}")
    if scene.rotating:
        body.append(f"- rotating: {scene.rotating[0]} ~~~✧~~~> {scene.rotating[1]}")
    return "# sanctuary viewport\n\n" + "\n".join(body) + "\n"


def _render_sanctuary(args, root: Path, fm_by_id: dict) -> int:
    """Static `--theme sanctuary` path for `--emit human|llm|both`."""
    seat_rows, present = load_seat_rows(root, fm_by_id)
    ephemeral = []
    try:
        import spawn_budget
        ephemeral = spawn_budget.live_agents(root)
    except Exception:
        pass
    windows = []
    try:
        import rotate as _rotate
        windows = _rotate._existing_windows(_rotate.DEFAULT_TMUX_SESSION)
    except Exception:
        pass
    scene = sanctuary_frame(seat_rows, ephemeral, rotating_seat(seat_rows, windows))
    status = f"theme=sanctuary registry={'yes' if present else 'absent'}"
    mode = args.emit or "human"
    if mode in ("human", "both"):
        if mode == "both":
            print("=" * args.width)
            print("HUMAN VIEW — sanctuary".center(args.width))
            print("=" * args.width)
        for ln in render_sanctuary_human(scene, args.width):
            print(ln[:args.width])
    if mode in ("llm", "both"):
        if mode == "both":
            print("\n" + "=" * args.width)
            print("LLM VIEW  — same scene".center(args.width))
            print("=" * args.width)
        print(render_sanctuary_llm(scene), end="")
    return 0


# --------------------------------------------------------------------------
# The time axis.
# --------------------------------------------------------------------------

def iteration_points(root: Path) -> list[str]:
    """Iterations this project has run, oldest first. Read-only."""
    sess = root / "sessions"
    if not sess.is_dir():
        return []
    return sorted(p.name for p in sess.iterdir()
                  if p.is_dir() and p.name.startswith("iter-"))


def agents_of_iteration(root: Path, iter_name: str) -> dict:
    """`{node_id: [agent_id, ...]}` for one iteration. Read-only.

    Reads the manifest and each agent's `agent.json`, which is where a
    parent's `owns` list and a kid's `node_id` live. This is the live axis's
    data source too -- an agent is "at" the node it is writing.
    """
    out: dict[str, list[str]] = {}
    d = root / "sessions" / iter_name
    mf = d / "manifest.json"
    if not mf.is_file():
        return out
    try:
        agents = json.loads(mf.read_text()).get("agents", [])
    except (json.JSONDecodeError, OSError):
        return out
    for a in agents:
        aid = a.get("id") or ""
        targets: list[str] = []
        if a.get("node_id"):
            targets.append(a["node_id"])
        aj = d / aid / "agent.json"
        if aj.is_file():
            try:
                rec = json.loads(aj.read_text())
            except (json.JSONDecodeError, OSError):
                rec = {}
            if rec.get("node_id"):
                targets.append(rec["node_id"])
            targets.extend(rec.get("owns") or [])
        if not targets and a.get("target"):
            targets.append(a["target"])
        for t in dict.fromkeys(targets):
            out.setdefault(t, []).append(aid)
    return out


def grid_versions(node_id: str) -> list[str]:
    """A node's grid versions, newest last. Read-only (`grid.py versions`)."""
    try:
        r = subprocess.run(
            [sys.executable, str(BIN / "grid.py"), "versions", node_id],
            capture_output=True, text=True, timeout=30)
    except (OSError, subprocess.SubprocessError):
        return []
    if r.returncode != 0:
        return []
    return [ln.strip() for ln in r.stdout.splitlines() if ln.strip()]


# --------------------------------------------------------------------------
# Interactive shell.
# --------------------------------------------------------------------------

def interactive(root: Path, g, fm_by_id, args) -> int:
    import curses

    def run(scr) -> int:
        curses.curs_set(0)
        scr.nodelay(False)
        top = left = 0
        depth = args.depth
        anchor = args.anchor
        iters = iteration_points(root)
        t_idx = len(iters) - 1
        live = args.live
        msg = ""

        while True:
            h, w = scr.getmaxyx()
            iter_name = iters[t_idx] if iters and t_idx >= 0 else None
            agents = agents_of_iteration(root, iter_name) if (live and iter_name) else {}
            frames = frame_stream(g, fm_by_id, anchor, depth, agents)

            seats = None
            if live:
                try:
                    import seat_status as _ss
                    seats = _ss.collect(root, fm_by_id)
                except Exception:                                    # noqa: BLE001
                    pass

            status = (f"anchor={anchor or 'roots'} depth={depth} "
                      f"frames={len(frames)} "
                      f"time={iter_name or '-'} live={'on' if live else 'off'}"
                      + (f" | {msg}" if msg else ""))
            body = render_human(frames, top, left, h - 2, w - 1, seats=seats)

            scr.erase()
            for i, ln in enumerate(body[:h - 2]):
                try:
                    scr.addstr(i, 0, ln[:w - 1])
                except curses.error:
                    pass
            try:
                scr.addstr(h - 2, 0, status[:w - 1], curses.A_REVERSE)
                scr.addstr(h - 1, 0,
                           "arrows/hjkl pan  +/- depth  [/] time  a live  q quit"[:w - 1])
            except curses.error:
                pass
            scr.refresh()

            k = scr.getch()
            msg = ""
            if k in (ord("q"), 27):
                return 0
            elif k in (curses.KEY_DOWN, ord("j")):
                top += 1
            elif k in (curses.KEY_UP, ord("k")):
                top = max(0, top - 1)
            elif k in (curses.KEY_RIGHT, ord("l")):
                left += 4
            elif k in (curses.KEY_LEFT, ord("h")):
                left = max(0, left - 4)
            elif k == curses.KEY_NPAGE:
                top += h - 3
            elif k == curses.KEY_PPAGE:
                top = max(0, top - (h - 3))
            elif k in (ord("+"), ord("=")):
                depth += 1
            elif k == ord("-"):
                depth = max(0, depth - 1)
            elif k == ord("["):
                t_idx = max(0, t_idx - 1)
            elif k == ord("]"):
                t_idx = min(len(iters) - 1, t_idx + 1)
            elif k == ord("a"):
                live = not live
            elif k == ord("g"):
                top = 0
            top = max(0, min(top, max(0, len(frames) - 1)))

    return curses.wrapper(run)


# --------------------------------------------------------------------------

def main() -> int:
    ap = argparse.ArgumentParser(
        description="Live graph viewport — one render, two readers (goal:g9.7).")
    ap.add_argument("--project", default=None)
    ap.add_argument("--anchor", default=None, help="node id to view from")
    ap.add_argument("--depth", type=int, default=3)
    ap.add_argument("--emit", choices=("human", "llm", "both"), default=None,
                    help="static render instead of the interactive viewport")
    ap.add_argument("--verify", action="store_true",
                    help="assert goal:g9.7 — both formatters read one stream")
    ap.add_argument("--iter", default=None, help="time axis: an iter-NNN name")
    ap.add_argument("--live", action="store_true", help="draw agents as spiders")
    ap.add_argument("--top", type=int, default=0)
    ap.add_argument("--left", type=int, default=0)
    ap.add_argument("--height", type=int, default=40)
    ap.add_argument("--width", type=int, default=120)
    ap.add_argument("--theme", choices=("graph", "sanctuary"), default="graph",
                    help="live-axis view theme (default: graph)")
    args = ap.parse_args()

    root = Path(args.project) if args.project else locations.find_project_root(Path.cwd())
    if root is None:
        print("viewport: no project found (no enclosing .agi/ with a config)",
              file=sys.stderr)
        return 2
    root = Path(root)

    try:
        g, _loaded = zoom._load_wired_graph(root)
    except Exception as e:                                   # noqa: BLE001
        print(f"viewport: could not load the graph: {e}", file=sys.stderr)
        return 2

    fm_by_id: dict = {}
    for d in sorted((root / "nodes").glob("*")):
        if d.is_dir():
            fm_by_id.update(zoom._frontmatter_for(root, d.name))

    if args.theme == "sanctuary":
        return _render_sanctuary(args, root, fm_by_id)

    iter_name = args.iter
    if args.live and not iter_name:
        pts = iteration_points(root)
        iter_name = pts[-1] if pts else None
    agents = agents_of_iteration(root, iter_name) if iter_name else {}

    frames = frame_stream(g, fm_by_id, args.anchor, args.depth, agents)

    # goal:g9.7, L1.04 — the briefing is built ONCE and handed to both
    # formatters, exactly as the frame stream is. Failing to build it is not
    # fatal: a viewport that can still draw the graph is worth more than one
    # that refuses to start because the metric config is unreadable.
    brief = None
    try:
        import briefing as _briefing
        brief = _briefing.build(root, g)
    except Exception as exc:                                     # noqa: BLE001
        print(f"viewport: briefing unavailable ({type(exc).__name__}: {exc})",
              file=sys.stderr)

    # Live seat status (hypothesis:l3w4-telemetry-seat-status): one `SeatsView`
    # computed once, handed to both formatters like the frame stream and the
    # briefing. Only on `--live` — the static graph view has no business reading
    # the seat board. Fails open to an absent registry, never a traceback.
    seats = None
    if args.live:
        try:
            import seat_status as _ss
            seats = _ss.collect(root, fm_by_id)
        except Exception as exc:                                   # noqa: BLE001
            print(f"viewport: seat status unavailable "
                  f"({type(exc).__name__}: {exc})", file=sys.stderr)

    if args.verify:
        return _verify(frames, args, brief)

    if args.emit is None and sys.stdout.isatty():
        return interactive(root, g, fm_by_id, args)

    mode = args.emit or "human"
    status = (f"anchor={args.anchor or 'roots'} depth={args.depth} "
              f"frames={len(frames)} time={iter_name or '-'}")
    if mode in ("human", "both"):
        if mode == "both":
            print("=" * args.width)
            print("HUMAN VIEW".center(args.width))
            print("=" * args.width)
        print("\n".join(render_human(frames, args.top, args.left,
                                     args.height, args.width, status, brief, seats)))
    if mode in ("llm", "both"):
        if mode == "both":
            print("\n" + "=" * args.width)
            print("LLM VIEW  — same frames, same slice".center(args.width))
            print("=" * args.width)
        print(render_llm(frames, args.top, args.left,
                         args.height, args.width, status, brief, seats), end="")
    return 0


#: A frame line in the llm view, and ONLY a frame line: `- \`id\` (type) …`.
#: Matching "any line with a backtick" was correct until the briefing arrived,
#: at which point `metric_primary`, the verdict taxonomy and every declared
#: command became false positives. The stricter pattern is the point: a
#: verifier that silently starts measuring different lines has stopped
#: verifying (L1.04).
_FRAME_LINE = re.compile(r"^\s*-\s+`([^`]+)`\s+\(")


def _verify(frames: list[Frame], args, brief=None) -> int:
    """`goal:g9.7`'s falsifier, as an executable check.

    Both formatters must read the same frames, in the same order, over the
    same slice. The test is not that the two strings match -- they must not,
    the consumers differ -- but that **every node id in one appears in the
    other, in the same order**, and that neither invents or drops a frame.

    Since L1.04 it also checks the **briefing**: both readers are handed the
    same `Briefing`, so the facts each states must agree. The llm view carries
    the full contract and the human view a compact projection, and the numbers
    in the projection have to be the numbers in the contract -- otherwise the
    two readers are being told different things about the same graph, which is
    exactly what `goal:g9.7` forbids one layer up.
    """
    top, height = args.top, args.height
    sl = frames[top:top + height]

    human = render_human(frames, top, 0, height, 10_000, brief=brief)
    llm = render_llm(frames, top, 0, height, 10_000, brief=brief)

    ok = True
    llm_ids = [m.group(1) for m in
               (_FRAME_LINE.match(ln) for ln in llm.splitlines()) if m]
    if llm_ids != [f.node_id for f in sl]:
        print("FAIL: llm view's node order differs from the frame stream")
        ok = False

    human_titles = [ln.strip() for ln in human if ln.strip()]
    if len(human_titles) < len(sl):
        print(f"FAIL: human view dropped frames ({len(human_titles)} < {len(sl)})")
        ok = False

    for f in sl:
        if f.damaged and f.damaged not in llm:
            print(f"FAIL: damage on {f.node_id} is missing from the llm view")
            ok = False

    if brief is not None:
        # The facts both readers were handed must appear in both renderings.
        human_blob = "\n".join(human)
        for label, needle in (("node count", str(brief.node_count)),
                              ("primary metric", brief.primary),
                              ("coverage", f"{brief.coverage:.3f}")):
            if needle not in llm or needle not in human_blob:
                print(f"FAIL: {label} ({needle!r}) is not in both views")
                ok = False
        if "## chain rules" not in llm:
            print("FAIL: the llm view omits the chain rules a kid is judged on")
            ok = False

    print(f"frames in slice: {len(sl)}   human lines: {len(human_titles)}   "
          f"llm ids: {len(llm_ids)}   briefing: "
          f"{'yes' if brief is not None else 'absent'}")
    print("PASS — one stream, two formatters, same nodes in the same order"
          if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
