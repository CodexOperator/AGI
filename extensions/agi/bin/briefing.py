#!/usr/bin/env python3
"""briefing.py — the graph-level facts every agent is handed, computed once.

`goal:g9.7` says **one render, two readers**: the window a human pans across
and the context a kid is spawned with must be the same thing at two grains.
`viewport.py` already holds that for the *frames* — the node tree. It did not
hold for everything wrapped around them.

## What was actually split

`INJECTION.md` is not a node tree. It is a node tree plus **nine sections of
briefing**: the graph snapshot, the primary metric and whether it is gameable,
chain diagnostics with their warning, the attractor list, the big-vs-small
split, the verdict taxonomy, the chain rules, pending-task counts, and the
declared command table. Measured 2026-09-03: `viewport.py --emit llm` was
**45 lines** against `INJECTION.md`'s **271**, and the difference was entirely
this material.

So the viewport could not replace the renderer, and the renderer owned the
only copy of the rules an agent is judged against. **The chain rules and the
verdict taxonomy were literal text inside `render-context.py`'s `out_lines`.**
Anything else wanting to show an agent the rules would have had to restate
them, and a restated contract is a contract that drifts — the same failure
`goal:g1.10` found in four prose copies of the command table, one of which had
been wrong for months.

This module is that material, extracted **before** the deletion rather than
after. `render-context.py` and `viewport.py` now compose the same object, so
they cannot disagree; and when `render-context.py` goes, nothing here goes
with it.

## Two renderings, one set of facts

`to_markdown` is the full briefing — what `INJECTION.md` carries and what a
kid is handed. `to_compact` is the few lines that fit above a terminal
viewport. **They are projections of one `Briefing`, never two computations**,
which is the same rule the frame stream already follows one layer down.

## It computes, it never writes

Like `viewport.py` and unlike `render-context.py`, nothing here opens a file
for writing. The caller decides where the text goes.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

#: The one place the verdict taxonomy is written down for agents. Kept here
#: rather than in a formatter so a second formatter cannot restate it.
VERDICT_TAXONOMY = (
    "`proved | disproved | inconclusive_lean_proved:N | "
    "inconclusive_lean_disproved:N | pending`"
)

#: Likewise the chain rules. These are the contract a kid's work is judged
#: against; they were previously inline in one renderer's line list.
CHAIN_RULES = [
    "- **chain length is never a target.** Extend a chain only when the next",
    "  node adds evidence or moves a goal; a short chain that closes a goal",
    "  beats a long one that closes nothing.",
    "- attraction is the descendant list above (goal-attributable), not hop count",
    "- mid-chain join is always allowed; so is starting fresh (see big-vs-small)",
    "- forks welcome — same idea may spawn multiple hypotheses",
    "- new ideas spawn from any node type (idea/hypothesis/experiment/verdict)",
    "- `proved`/`disproved` require `evidence_runs >= 1`; unevidenced verdicts",
    "  are auto-demoted to `inconclusive_lean_*` by the evidence gate",
]

#: The hop-count warning. Long, and it stays long: agents once drove chain
#: length to 9 chains x 2000 hops carrying no signal, and the short version of
#: this warning is what let them.
CHAIN_DIAGNOSTIC_NOTE = [
    "Hop counts describe the graph's shape; they do not score the work. A",
    "rising longest chain against a flat `{default_metric}` means hops are",
    "being padded — agents once drove this stat to 9 chains x 2000 hops carrying",
    "no signal (TODO.md H3), and that structure is what made chain-finding",
    "non-terminating (H0c). Read these numbers, never optimise them.",
]


@dataclass
class Briefing:
    """Every graph-level fact an agent is handed, computed once per render."""

    generated_at: str = ""
    node_count: int = 0
    edge_count: int = 0
    by_type: dict = field(default_factory=dict)

    primary: str = "outcome_coverage"
    primary_is_gameable: bool = False
    default_metric: str = "outcome_coverage"
    coverage: float = 0.0

    chain_engine_available: bool = False
    chain_count: int = 0
    longest_len: int = 0

    #: `(node_id, descendant_count)`, already sorted, already truncated.
    attractors: list = field(default_factory=list)
    pending_tasks: int = 0

    #: Pre-rendered by `commands.render_for_injection` — the declared command
    #: table (`goal:g1.10`). Empty when the project declares none.
    command_lines: list = field(default_factory=list)


def successors(g, nid: str) -> list:
    """Node ids reachable in one hop, **whichever way this graph stores that.**

    🔴 This project has two live graph representations and they disagree about
    where adjacency lives. `load_directory` builds explicit `Edge` objects and
    answers `edges_from`; `zoom._load_wired_graph` builds none at all and
    hangs `children` sets on the nodes.

    Measured 2026-09-03: a descendant count written against only the first
    returned **0 for every idea** on the second — so the attractor list, which
    is what an agent reads to choose a target, came out all zeros in
    alphabetical order and looked like a plausible list. Nothing raised. A
    briefing that silently reports zeros is worse than one that fails, because
    the loop keeps running on it.
    """
    if hasattr(g, "edges_from"):
        try:
            out = [getattr(e, "target", None) for e in g.edges_from(nid)]
            out = [t for t in out if t]
            if out:
                return out
        except Exception:                                        # noqa: BLE001
            pass
    node = g.get_node(nid) if hasattr(g, "get_node") else None
    return sorted(getattr(node, "children", ()) or ()) if node else []


def count_descendants(g, root: str) -> int:
    """BFS descendant count, over whichever adjacency the graph actually has."""
    seen = {root}
    stack = [root]
    n = 0
    while stack:
        cur = stack.pop()
        for tgt in successors(g, cur):
            if tgt not in seen:
                seen.add(tgt)
                stack.append(tgt)
                n += 1
    return n


def build(root: Path, g, loaded=None, *, descendants_fn=None,
          chain_stats: tuple | None = None) -> Briefing:
    """Compute the briefing for `g`.

    `descendants_fn` and `chain_stats` are injectable because the two callers
    already compute them by different routes and neither should be forced to
    recompute — but the *presentation* must be shared, which is the point.
    """
    b = Briefing()
    b.generated_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    by_type: dict = {}
    for n in getattr(g, "nodes", []):
        by_type[n.type] = by_type.get(n.type, 0) + 1
    b.by_type = by_type
    b.node_count = len(g) if hasattr(g, "__len__") else len(by_type)

    # `edge_count` is maintained by one loader and left at 0 by another, and
    # the difference is invisible until a briefing says `edges: 0` about a
    # graph with 866 of them (measured 2026-09-03, L1.05). Counting the
    # iterator when the counter says zero costs one pass and makes the number
    # a property of the graph rather than of which loader built it.
    b.edge_count = int(getattr(g, "edge_count", 0) or 0)
    if not b.edge_count:
        try:
            b.edge_count = sum(1 for _ in getattr(g, "edges", ()))
        except Exception:                                        # noqa: BLE001
            b.edge_count = 0
    if not b.edge_count:
        # No Edge objects at all — count the adjacency the nodes carry, which
        # is the only place this representation keeps it.
        b.edge_count = sum(len(getattr(n, "children", ()) or ())
                           for n in getattr(g, "nodes", []))

    try:
        import metrics as _m
        cfg = _m.read_config(root)
        b.primary = _m.primary_metric_name(cfg)
        b.default_metric = _m.DEFAULT_METRIC_PRIMARY
        b.primary_is_gameable = b.primary in _m.GAMEABLE_METRICS
        b.coverage = _m.outcome_coverage(by_type.get("mvp", 0),
                                         by_type.get("hypothesis", 0))
    except Exception:
        # A briefing that cannot read metrics is still worth handing over --
        # it just must not claim a target it did not read.
        pass

    if chain_stats is not None:
        b.chain_engine_available = True
        b.chain_count, b.longest_len = chain_stats

    fn = descendants_fn or (lambda nid: count_descendants(g, nid))
    attract = [(n.id, fn(n.id)) for n in getattr(g, "nodes", [])
               if n.type == "idea"]
    attract.sort(key=lambda x: -x[1])
    b.attractors = attract[:10]

    if loaded is not None:
        b.pending_tasks = sum(
            1 for ln in loaded
            if ln.node.type == "task" and "tier-" in " ".join(ln.node.tags))

    try:
        import commands as _commands
        b.command_lines = list(_commands.render_for_injection(root) or [])
    except Exception as exc:                                     # noqa: BLE001
        print(f"warn: could not render declared commands: "
              f"{type(exc).__name__}: {exc}", file=sys.stderr)

    return b


def to_markdown(b: Briefing) -> list[str]:
    """The full briefing — `INJECTION.md`'s body and the kid's context header."""
    out = [
        "## graph snapshot",
        f"- nodes: {b.node_count}",
        f"- edges: {b.edge_count}",
        "- by type: " + ", ".join(f"{k}={v}" for k, v in sorted(b.by_type.items())),
    ]
    if b.primary_is_gameable:
        # Never hand agents a target the engine itself rejects.
        out += [
            f"- !! `metric_primary` is `{b.primary}`, which is **not a valid "
            f"target** — it is gameable (TODO.md H3). Migrate the config to "
            f"`{b.default_metric}`.",
            f"- **score work on `{b.default_metric}`** meanwhile: "
            f"{b.coverage:.3f} (mvps per hypothesis)",
        ]
    else:
        out += [
            f"- **scored on `{b.primary}`** (`metric_primary`) — this is the target",
            f"- outcome_coverage: {b.coverage:.3f} "
            "(mvps per hypothesis; goal-attributable)",
        ]

    out += ["", "## chain diagnostics (descriptive — not targets)"]
    if b.chain_engine_available:
        out += [f"- chain count: {b.chain_count}",
                f"- longest chain: {b.longest_len} hops (via next edges)"]
    else:
        out += ["- unavailable: chain_engine not importable"]
    out += [ln.format(default_metric=b.default_metric)
            for ln in CHAIN_DIAGNOSTIC_NOTE]

    out += ["", "## attractive ideas (descendant count, top 10)"]
    out += [f"- {nid} :: {count} descendants" for nid, count in b.attractors]

    out += [
        "",
        "## big-vs-small decision",
        "Each iteration MUST first answer: **explore a big idea or small idea?**",
        "- big = fresh chain, broad concept (default 30%)",
        "- small = extend existing chain mid-way (default 70%)",
        "",
        "## verdict taxonomy",
        VERDICT_TAXONOMY,
        "",
        "## chain rules",
        *CHAIN_RULES,
        "",
        "## next-step suggestions",
        f"- pending tasks: {b.pending_tasks} (see nodes/task/)",
    ]
    if b.command_lines:
        out += ["", *b.command_lines]
    return out


def to_compact(b: Briefing) -> list[str]:
    """The few lines that fit above a terminal viewport.

    A projection of the same object, not a second computation. It carries the
    numbers a human is watching change and drops the rules text, which a human
    reading their own graph does not need re-stated every frame.
    """
    types = ", ".join(f"{k}={v}" for k, v in sorted(b.by_type.items())
                      if k in ("goal", "hypothesis", "mvp", "verdict", "experiment"))
    metric = (f"!! {b.primary} is gameable — score {b.default_metric}"
              if b.primary_is_gameable else f"{b.primary}")
    return [
        f"nodes {b.node_count} · edges {b.edge_count} · {types}",
        f"scored on {metric} = {b.coverage:.3f}"
        + (f" · chains {b.chain_count}/{b.longest_len}h"
           if b.chain_engine_available else ""),
    ]
