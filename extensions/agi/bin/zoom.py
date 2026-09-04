#!/usr/bin/env python3
"""zoom.py — produce a context bundle scoped to one grain of the graph.

Numeric zoom axis, `--level 1..5` (see `goal:g2` / `goal:g2.1` in the graph
repo for the design):

    1  Above code    — goals and their skill-tree of general nodes
    2  Sub-systems   — engine modules/entry-points and their relationships
    3  Code nodes    — one node per source file (the level3 node type)
    4  Functions     — call-level detail                    [not built yet]
    5  Built-ins     — resolved into external libraries      [not built yet]

Levels 1-3 have a real, loadable index today (`nodes/goal/`, `nodes/idea/
engine-*.md`, `nodes/level3/`). Levels 4 and 5 do not: there is no
nodes/level4/ or nodes/level5/, no generator, no contract shape for either.
Asking for them refuses loudly rather than fabricating an answer or quietly
serving a different grain (see `_unavailable_message`).

`--target <node-id>` bounds the rendered set to a 2-hop neighbourhood of that
node (BFS over `parents`/`children`, same traversal used at every level),
filtered down to nodes of the level's own type. Omit `--target` at levels
1-3 to see the whole census at that grain.

Legacy aliases (still used by `dispatch.py` and documented in
`skills/agi/SKILL.md`):

    --level big     whole-graph context (INJECTION.md + attractor list)
    --level small   2-hop subtree around --target, ANY node type

These keep their EXACT original content and requirements (small still
requires --target) — dispatch.py's live research pipeline calls `small`
with hypothesis/experiment/idea targets, and collapsing that through the
new level-3 (code-only) filter would silently break the running loop, which
is exactly the class of regression this file exists to prevent. They are
documented as the closest numeric equivalents (big -> 1, small -> 3) purely
for migration guidance; a deprecation note goes to stderr on every use.

Output: writes `<project>/sessions/<iter>/<agent_id>/context.md` and prints
that path on stdout for the dispatcher to pick up.

Usage:
    zoom.py <project_root> <iter> <agent_id> --level 1
    zoom.py <project_root> <iter> <agent_id> --level 2 --target <node_id>
    zoom.py <project_root> <iter> <agent_id> --level 3 --target <node_id>
    zoom.py <project_root> <iter> <agent_id> --level big            # legacy
    zoom.py <project_root> <iter> <agent_id> --level small --target <node_id>  # legacy
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

# goal:g11.1 — one resolver for every path. `bin/` is already importable when
# zoom is run as a script; the insert makes it so when it is imported as one.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import locations  # noqa: E402
import node_writer  # noqa: E402

#: Re-exported from `locations` rather than redefined. This file's own copy
#: knew only the legacy marker names, so it rejected both the repo root and
#: `.agi/` under the goal:g11 layout — `zoom.py . 5 kid --level small` printed
#: "not a project root" for every directory in this repo.
config_path = locations.config_path

PLUGIN_ROOT = Path(__file__).resolve().parent.parent


def default_runtime(root: Path) -> str:
    """`cc` when the project configures Claude-Code dispatch, else `pi`.

    goal:s8 — the completion contract is runtime-specific and was hardcoded
    to pi's. A project carrying `cc_dispatch` is dispatching through Claude
    Code, whose kids are told the opposite (`SKILL.md`: "no git, no push,
    no sync, no cli.py"). Defaulting off a key the project already sets
    means no existing pi project changes behaviour.
    """
    cfg_path = config_path(root)
    if cfg_path is None:
        return "pi"
    try:
        cfg = json.loads(cfg_path.read_text())
    except Exception:
        return "pi"
    return "cc" if isinstance(cfg.get("cc_dispatch"), dict) else "pi"


def completion_contract(runtime: str, iter_n, agent_id, target: str | None = None) -> list:
    """The lines telling a kid how to finish. One definition, three callers.

    It was copied into three renderers (big, legacy-small, numeric-level) and
    into the module docstring, all emitting pi's `cli.py done`. A CC kid then
    received, from the harness itself, an instruction its own protocol
    forbids — so every spawn prompt had to carry an out-of-band override
    telling the kid to ignore its own context file. Four copies of one
    contract is how that stayed true after SKILL.md said otherwise (goal:s8).
    """
    # The structured report is BOTH runtimes' — it was the CC contract's alone
    # until 2026-08-31, and the difference showed the moment the pi runtime
    # started getting its own contract: pi kids stopped emitting `struggles:`
    # and reported in free prose instead. Four of the five defects found in
    # that session's live runs came out of `struggles:` lines, so this block is
    # a measurement instrument, not politeness. `caveats` is what the kid knows
    # is weak about its node; `struggles` is what fought it — the second is the
    # one that finds engine bugs, because a kid describing what obstructed it is
    # describing the harness.
    # The field NAMES are literal and English, whatever language the model
    # reasons in. A `z-ai/glm-5.3-flash` kid on an all-English prompt reported
    # `已完成` / `注意事项` / `难点` for DONE / caveats / struggles on
    # 2026-09-01 — a correct translation, and unreadable to a reader keyed on
    # the words. It cost nothing that run because nothing parses these fields
    # yet; it costs something the day anything does, and it already costs a
    # human skimming for `struggles:`. Naming the language is cheaper than
    # teaching every future reader every translation of it.
    report = [
        "When done, report exactly:",
        "```",
        "DONE <node-id>",
        "caveats: <optional, one line — what is weak about the node itself>",
        "struggles: <optional, one line — what fought you: a tool, a flag, a",
        "            contradiction, anything that cost you a turn>",
        "```",
        "**Write the report in English, and keep the field names exactly as",
        "spelled above** — `DONE`, `caveats:`, `struggles:` — whatever language",
        "you reasoned in. They are read by name.",
        "**Report a struggle even when you worked around it.** A workaround you",
        "found is still a defect someone else will hit.",
    ]

    if runtime == "cc":
        return report + [
            "",
            "Do not commit. Do not push. Do not call cli.py. The parent reviews",
            "your node and owns all git.",
        ]
    node_id_line = "  --node-id <new_node_id>"
    if target:
        node_id_line += f" --parent {target}"
    return report + [
        "",
        "Then signal completion — this is the ONE command you run:",
        "```",
        f"python3 <plugin>/bin/cli.py done {iter_n} {agent_id} \\",
        "  --verdict <verdict_state> --confidence <0.0-1.0> \\",
        node_id_line + " \\",
        "  --evidence-runs <node-id> [<node-id> ...] \\",
        '  --notes "<one-line>"',
        "```",
        "",
        "**`--evidence-runs` is what makes `proved`/`disproved` stick.** It",
        "takes the NODE IDS of the runs backing your claim — usually the",
        "experiment node(s) you are judging, e.g.",
        "`--evidence-runs experiment:a00-1234-abcd`. Ids that do not resolve",
        "to a real node count for nothing, and a bare number counts for",
        "nothing either: a count no one can check certifies nothing. Omit the",
        "flag and a `proved` is auto-demoted to `inconclusive_lean_proved:50`,",
        "which is the correct outcome for an unevidenced claim but a silent",
        "loss when you did the work and simply did not link it.",
        "",
        "**Cite the run, not yourself.** An experiment may name itself, since",
        "it IS the run; a verdict must name the experiments it judges.",
        "",
        "**`--notes` is rendered into your node automatically**, under an",
        "`## Agent Notes` heading, exactly once however many times you call",
        "`done`. You do not need to write it into the body yourself.",
        "",
        "`<verdict_state>` is one of exactly these five:",
        "",
        "    proved | disproved | pending",
        "    inconclusive_lean_proved:N | inconclusive_lean_disproved:N",
        "",
        "**Two numbers, two scales.** `:N` in a lean is an INTEGER PERCENT",
        "(0-100); `--confidence` is a FRACTION (0..1). The same 65% lean,",
        "written correctly, uses both:",
        "",
        "    --verdict inconclusive_lean_proved:65 --confidence 0.65",
        "                                      ↑                ↑",
        "                                percent (65)     fraction (0.65)",
        "",
        "Passing 65 to `--confidence` is the common error and is corrected",
        "with a warning, not silently. `proved` and `disproved` require real",
        "experiment evidence and are auto-demoted without it, so write the",
        "honest lean rather than the strong claim.",
        "",
        "Do not commit. Do not push. Do not run git at all, and do not run",
        "grid.py. `cli.py done` is the ONLY command you run; the loop owns",
        "every commit.",
        "",
        "**This line is here because its absence was expensive.** The pi",
        "contract used to say only how to signal completion, so a kid on the",
        "2026-08-31 live run reasonably inferred that committing its own work",
        "was part of finishing — and `git commit -A` in a shared worktree swept",
        "up a second kid's half-written node and a human's uncommitted engine",
        "edits into one commit labelled with the first kid's node id",
        "(goal:g4.1). Nothing was lost; the history now says something untrue.",
        "Parallel kids share one tree, so the only safe git surface for a kid",
        "is none.",
    ]


class ZoomUnavailable(RuntimeError):
    """A bounded view could not be computed for the requested level/target.

    Raised instead of silently returning the whole graph, at ANY level: an
    unbounded context defeats the entire point of a zoom level, and a silent
    fallback hides the breakage from every caller. This used to happen three
    ways at once — graph_core import failure, sqlite backend failure, and an
    unknown --target — and all three fell back to the full INJECTION.md dump.
    Every one of those (plus the numeric levels added here) now raises this
    instead. Fail loudly — dispatch.py runs zoom.py with check=True, so this
    surfaces as a CalledProcessError rather than a context-bomb delivered to
    a kid.
    """


# Legacy --level value -> numeric level it is documented as closest to.
# Labeling only: big/small keep their original *content*, not level N's
# type-filtered rendering. See module docstring for why.
LEGACY_LEVEL_MAP = {"big": 1, "small": 3}

# Levels with a real, loadable index behind them today.
LEVEL_INFO = {
    1: dict(
        name="Goals",
        node_type="goal",
        dir_name="goal",
        blurb=(
            "Level 1 is the top of the zoom axis: goals and their skill-tree "
            "of general nodes (nodes/goal/*.md). Long-term goals (e.g. "
            "goal:g7) decompose into sub-goals (goal:g7.2, parents: [goal:g7]"
            "). No code lives at this level — it is what the project is "
            "trying to achieve, not how."
        ),
    ),
    2: dict(
        name="Sub-systems",
        node_type="idea",
        dir_name="idea",
        blurb=(
            "Level 2 is sub-systems and their relationships: one census node "
            "per engine module/entry-point (nodes/idea/engine-*.md), each "
            "carrying a unit_path pointing at the real file it describes and "
            "a parent goal that motivates it. This is the layer between "
            "'what we want' (level 1) and 'the file that does it' (level 3). "
            "Non-census idea nodes (research chains, domain groupings) are "
            "deliberately excluded — they are not sub-systems."
        ),
    ),
    3: dict(
        name="Code nodes",
        node_type="build",
        dir_name="build",
        blurb=(
            "Level 3 is actual code: one build node per source file "
            "(nodes/build/*.md), each with a payload_ref to the real file "
            "and a mechanically-generated IO contract (inputs/outputs — "
            "harness-owned, never authored by a summarising model). "
            "goal:g2.1 calls this the level that makes the graph an "
            "executable artifact rather than a description of one, and it "
            "is the only level with a real index behind it today."
        ),
    ),
}

# Levels with no backing data. Naming what would need to exist, per goal:g2's
# falsifier: a summarising model fabricating structured content here would
# repeat the exact failure that produced 0.000 frontmatter recall.
LEVEL_UNAVAILABLE = {
    4: dict(
        name="Functions",
        blurb=(
            "Level 4 is functions and call-level detail: one node per "
            "function/method, wired into the call graph. This does not "
            "exist yet — there is no nodes/level4/ directory, no generator "
            "that walks each level3 payload_ref with `ast` (or GitNexus's "
            "existing symbol+call-graph index, used as a *seed* per "
            "goal:g2.1, not as source of truth) to mint one node per "
            "function, and no contract shape for call edges (caller/callee, "
            "arity, side effects) at that grain."
        ),
    ),
    5: dict(
        name="Built-ins",
        blurb=(
            "Level 5 is individual built-ins, including inside external "
            "libraries where resolvable. It needs level 4 to exist first "
            "(built-ins are called FROM functions), plus resolution into "
            "third-party source (stdlib and installed packages) that "
            "nothing in this repo — including GitNexus's own index —  "
            "currently attempts across package boundaries. No "
            "nodes/level5/, no generator, no resolver."
        ),
    ),
}


def _add_graph_core_to_path(root: Path) -> None:
    """Put graph_core on sys.path, plugin src last so a project can override.

    Mirrors driver.sh's convention: the engine lives in PLUGIN_ROOT/src, and a
    project may shadow it with its own src/graph_core. Previously only the
    project's src was added, so on any project without its own graph_core
    (the normal case) the import always failed and small zoom silently
    degraded to the whole graph.
    """
    plugin_src = PLUGIN_ROOT / "src"
    if plugin_src.is_dir():
        sys.path.insert(0, str(plugin_src))
    proj_src = root / "src"
    if (proj_src / "graph_core").is_dir():
        sys.path.insert(0, str(proj_src))


def _load_wired_graph(root: Path):
    """Load the full node graph (every type) and wire children from parents.

    Shared by legacy small-zoom and every numeric level — both need the same
    graph, just render different slices of it. Every failure path raises
    :class:`ZoomUnavailable` rather than letting a caller silently degrade to
    "no bound at all".
    """
    _add_graph_core_to_path(root)
    try:
        from graph_core.edge import Edge  # noqa: F401 — import-availability canary
    except Exception as e:
        raise ZoomUnavailable(f"graph_core import failed: {e}") from e

    cfg_path = config_path(root)
    use_sqlite = False
    cfg: dict = {}
    if cfg_path is not None:
        cfg = json.loads(cfg_path.read_text())
        use_sqlite = cfg.get("persistence", {}).get("type") == "sqlite"

    if use_sqlite:
        try:
            from graph_core.persistence.sqlite_backend import SQLiteBackend
            from graph_core.db_loader import DBLoader
            db_path = root / cfg["persistence"]["path"]
            g, loaded = DBLoader(SQLiteBackend(db_path)).load_directory()
        except Exception as e:
            raise ZoomUnavailable(f"sqlite backend unavailable: {e}") from e
    else:
        try:
            from graph_core.loader import load_directory
        except Exception as e:
            raise ZoomUnavailable(f"filesystem loader unavailable: {e}") from e
        g, loaded = load_directory(root / "nodes")

    for ln in loaded:
        for parent_id in ln.node.parents:
            if g.has_node(parent_id):
                pn = g.get_node(parent_id)
                if pn is not None:
                    pn.children.add(ln.node.id)

    return g, loaded


def _bfs_neighbors(g, target: str, hops: int = 2) -> dict[str, int]:
    """BFS over parents|children from `target`, `hops` deep. id -> layer (0=target)."""
    layers = {target: 0}
    frontier = [target]
    for _ in range(hops):
        nxt = []
        for nid in frontier:
            n = g.get_node(nid)
            if n is None:
                continue
            for x in n.parents | n.children:
                if x not in layers:
                    layers[x] = layers[nid] + 1
                    nxt.append(x)
        frontier = nxt
    return layers


def _frontmatter_for(root: Path, dir_name: str) -> dict[str, dict]:
    """id -> frontmatter dict for every file directly under nodes/<dir_name>/.

    Header-only read (`body=False`) — cheap even though goal+idea+level3
    together are ~120 files. Used only for display enrichment (title,
    unit_path); graph *structure* always comes from `_load_wired_graph`, so
    identity/duplicate handling stays in one place (graph_core's loader).
    """
    from graph_core.persistence.frontmatter import load_node_file, FrontmatterError

    out: dict[str, dict] = {}
    # Live directory then its retired sibling `nodes/deprecated/<type>/`
    # (goal:g2.10). Retired nodes are enriched too: this map supplies titles for
    # display, and a node that appears in the graph with no title because it was
    # regrouped reads as corruption rather than as retirement.
    dirs = [d for d in (root / "nodes" / dir_name,
                        root / "nodes" / "deprecated" / dir_name) if d.is_dir()]
    if not dirs:
        return out
    for p in [q for d in dirs for q in sorted(d.glob("*.md"))]:
        try:
            nf = load_node_file(p, body=False)
        except FrontmatterError:
            continue
        nid = nf.frontmatter.get("id")
        if isinstance(nid, str):
            out[nid] = nf.frontmatter
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project_root")
    ap.add_argument("iter_n", type=locations.iteration_id)
    ap.add_argument("agent_id")
    ap.add_argument(
        "--level",
        choices=["1", "2", "3", "4", "5", "big", "small"],
        required=True,
    )
    ap.add_argument(
        "--target",
        default=None,
        help="node id. Bounds the subtree at levels 1-3 (optional there); "
             "required for legacy --level small; ignored by big/4/5.",
    )
    ap.add_argument(
        "--runtime",
        choices=["pi", "cc"],
        default=None,
        help="which completion contract to hand the kid. Default: 'cc' when "
             "the project config has a cc_dispatch block, else 'pi' (goal:s8).",
    )
    args = ap.parse_args()

    # goal:g11.1 — resolve the given path the same way every other entry point
    # resolves cwd, instead of demanding it already BE the graph root. Under the
    # goal:g11 layout the graph is at `<repo>/.agi`, so the natural argument —
    # the repo root, which is what `dispatch.py` and every human pass — held no
    # config and was rejected outright. `find_project_root` is the identity on a
    # legacy root (phase 1), so no existing project resolves differently.
    given = Path(args.project_root).resolve()
    root = locations.find_project_root(given)
    if root is None:
        print(f"ERR: not a project root: {given}", file=sys.stderr)
        return 1
    if args.runtime is None:
        args.runtime = default_runtime(root)

    raw_level = args.level
    if raw_level in LEGACY_LEVEL_MAP:
        mapped = LEGACY_LEVEL_MAP[raw_level]
        print(
            f"DEPRECATION: --level {raw_level} is a legacy alias. The zoom "
            f"axis is now numeric 1..5; '{raw_level}' is documented as "
            f"closest in spirit to level {mapped} ({LEVEL_INFO[mapped]['name']}), "
            f"but its rendered CONTENT is unchanged from before (whole-graph "
            f"for big, 2-hop-any-type subtree for small) so dispatch.py's "
            f"live research pipeline keeps working. Prefer --level 1..5 for "
            f"new callers.",
            file=sys.stderr,
        )

    sess_dir = locations.iteration_dir(root, args.iter_n) / args.agent_id
    sess_dir.mkdir(parents=True, exist_ok=True)
    out_path = sess_dir / "context.md"

    if raw_level in ("4", "5"):
        print(_unavailable_message(int(raw_level)), file=sys.stderr)
        return 1

    try:
        if raw_level == "big":
            inject_path = root / "context" / "INJECTION.md"
            if not inject_path.exists():
                print(f"ERR: INJECTION.md missing at {inject_path}", file=sys.stderr)
                return 1
            inject_text = inject_path.read_text(encoding="utf-8")
            content = _compose_big(inject_text, args)
        elif raw_level == "small":
            if not args.target:
                print("ERR: --target required for --level small", file=sys.stderr)
                return 1
            content = _compose_small(root, args)
        else:
            content = _render_level(root, args, int(raw_level))
    except ZoomUnavailable as e:
        print(
            f"ERR: zoom could not build a bounded context: {e}\n"
            f"     Refusing to fall back to the whole graph — an unbounded\n"
            f"     context defeats the entire point of a zoom level. Fix the\n"
            f"     graph_core import / target id, or dispatch this agent at\n"
            f"     --level big deliberately.",
            file=sys.stderr,
        )
        return 1

    out_path.write_text(content, encoding="utf-8")
    print(out_path)
    return 0


def _unavailable_message(level: int) -> str:
    info = LEVEL_UNAVAILABLE[level]
    return (
        f"ERR: zoom level {level} ({info['name']}) is not yet available.\n"
        f"{info['blurb']}\n"
        f"Refusing to serve a different grain under the level-{level} label, "
        f"and refusing to fall back to the whole graph — an honest refusal "
        f"beats a silently wrong grain."
    )


def _compose_big(inject_text: str, args: argparse.Namespace) -> str:
    contract = "\n".join(
        "   " + ln for ln in
        completion_contract(args.runtime, args.iter_n, args.agent_id)
    )
    return f"""# autoresearch-tree iteration {args.iter_n} — agent {args.agent_id}

## Zoom Level: BIG (legacy alias for numeric level {LEGACY_LEVEL_MAP['big']} — {LEVEL_INFO[LEGACY_LEVEL_MAP['big']]['name']})
You are exploring the WHOLE graph. Pick a high-level idea or new chain to extend.
Bias: introduce a fresh idea, fork an under-explored chain, or seed a new domain.

{inject_text}

## Your Task
1. Decide: extend longest chain, fork mid-chain, or start fresh idea.
2. Pick or create one node id (idea/hypothesis/experiment/mvp/outcome).
3. Run the experiment / implement the MVP / write the outcome.
4. {contract.lstrip()}

If stuck >2 attempts on same approach → write a `pending` verdict and stop.
"""


def _node_path_hint(root: Path, node_id: str) -> str | None:
    """Where a node's file actually is, relative to the graph root.

    A small-zoom context lists ids and types and no bodies, so a kid that needs
    a node's text has to open the file -- and an id is not a filename. The
    address is a slug (`goal:g4.3` lives in
    `nodes/goal/g4.3-finish-the-runtime-split-pi-and.md`), so the obvious guess
    fails. A live kid burned its first read on `g4.3.md` on 2026-09-01 and said
    so in its `struggles:` line.

    That is the id/address split (G2.5) billing a kid for a lookup the engine
    can do for free: `node_writer.find_node_file` is the one resolver and it is
    already loaded here. Emitting the answer beside the id is `goal:g1.9`'s
    principle at its smallest -- a fact the engine knows should not cost a kid
    a turn to rediscover.

    Best-effort by design: a node in the graph with no file on disk still
    renders, it just renders without the hint.
    """
    try:
        path = node_writer.find_node_file(root, node_id)
    except Exception:
        return None
    if path is None:
        return None
    try:
        return str(Path(path).relative_to(root))
    except ValueError:
        return str(path)


def _compose_small(root: Path, args: argparse.Namespace) -> str:
    """Legacy 2-hop subtree around --target, ANY node type. Unchanged content."""
    g, _loaded = _load_wired_graph(root)

    target = args.target
    if not g.has_node(target):
        raise ZoomUnavailable(
            f"--target '{target}' not found in the graph loaded from "
            f"{root / 'nodes'}."
        )

    layers = _bfs_neighbors(g, target, hops=2)
    seen = set(layers)

    lines = [
        f"# autoresearch-tree iteration {args.iter_n} — agent {args.agent_id}",
        "",
        f"## Zoom Level: SMALL (legacy alias for numeric level {LEGACY_LEVEL_MAP['small']} — {LEVEL_INFO[LEGACY_LEVEL_MAP['small']]['name']})",
        f"Target node: **{target}** (extending or branching from this point)",
        "",
        f"Subtree contains {len(seen)} nodes within 2 hops of target.",
        "",
        "### Subtree Nodes",
    ]
    for nid in sorted(seen, key=lambda x: (layers[x], x)):
        n = g.get_node(nid)
        if n is None:
            continue
        marker = "→" if nid == target else " "
        lines.append(f"- {marker} `{nid}` (type={n.type}, layer={layers[nid]})")
        path = _node_path_hint(root, nid)
        if path:
            lines.append(f"    file: {path}")
        if n.parents:
            lines.append(f"    parents: {', '.join(sorted(n.parents)[:3])}")
        if n.children:
            lines.append(f"    children: {', '.join(sorted(n.children)[:3])}")

    lines.extend([
        "",
        "## Your Task",
        f"Extend or fork from `{target}`. Stay tight — don't wander to other chains.",
        "Acceptable: spawn one child node (hyp from idea, exp from hyp, verdict from exp, mvp from verdict, outcome from mvp).",
    ])
    lines.extend(completion_contract(args.runtime, args.iter_n, args.agent_id, target))
    lines.extend([
        "",
        "If stuck >2 attempts → write `pending` verdict and stop.",
    ])
    return "\n".join(lines) + "\n"


def _render_level(root: Path, args: argparse.Namespace, level: int) -> str:
    """Numeric-axis renderer for levels 1-3: one node-type slice of the graph."""
    info = LEVEL_INFO[level]
    g, _loaded = _load_wired_graph(root)

    target = args.target
    if target and not g.has_node(target):
        raise ZoomUnavailable(
            f"--target '{target}' not found in the graph loaded from "
            f"{root / 'nodes'}."
        )

    fm_by_id = _frontmatter_for(root, info["dir_name"])

    def is_in_scope(nid: str) -> bool:
        n = g.get_node(nid)
        if n is None or n.type != info["node_type"]:
            return False
        if level == 2:
            # Census nodes only — non-census ideas (research chains, domain
            # groupings) are not sub-systems, even though they share the
            # "idea" node type and may sit in the same BFS neighbourhood.
            return "unit_path" in fm_by_id.get(nid, {})
        return True

    if target:
        layers = _bfs_neighbors(g, target, hops=2)
        pool = layers.keys()
        scope_desc = f"within 2 hops of target `{target}`"
    else:
        layers = {}
        pool = g.node_ids
        scope_desc = "across the whole corpus (no --target given)"

    shown = sorted(
        (nid for nid in pool if is_in_scope(nid)),
        key=lambda x: (layers.get(x, 0), x),
    )

    lines = [
        f"# autoresearch-tree iteration {args.iter_n} — agent {args.agent_id}",
        "",
        f"## Zoom Level: {level} — {info['name']}",
        info["blurb"],
        "",
    ]
    if target:
        lines.append(f"Target node: **{target}**")
    lines.append(
        f"{len(shown)} level-{level} ({info['node_type']}) node(s) {scope_desc}."
    )
    lines.append("")
    lines.append(f"### {info['name']} in scope")
    if not shown:
        lines.append(
            f"_(none — no `{info['node_type']}` node of this grain was found "
            f"{scope_desc})_"
        )
    for nid in shown:
        n = g.get_node(nid)
        fm = fm_by_id.get(nid, {})
        title = fm.get("title")
        marker = "→" if nid == target else " "
        head = f"- {marker} `{nid}`"
        if title:
            head += f" — {title}"
        if target:
            head += f" (layer={layers.get(nid, 0)})"
        lines.append(head)
        file_ref = fm.get("unit_path") or n.payload_ref
        if file_ref:
            lines.append(f"    file: {file_ref}")
        if n.parents:
            lines.append(f"    parents: {', '.join(sorted(n.parents)[:3])}")
        if n.children:
            lines.append(f"    children: {', '.join(sorted(n.children)[:3])}")

    lines.extend(["", "## Your Task"])
    if target:
        lines.append(
            f"Extend or fork from `{target}`. Stay tight — don't wander to other chains."
        )
    else:
        lines.append(
            f"Pick one `{info['node_type']}` node above to extend, fork, or seed a new chain from."
        )
    lines.extend([
        "Acceptable: spawn one child node (hyp from idea, exp from hyp, verdict from exp, mvp from verdict, outcome from mvp).",
    ])
    lines.extend(completion_contract(args.runtime, args.iter_n, args.agent_id, target))
    lines.extend([
        "",
        "If stuck >2 attempts → write `pending` verdict and stop.",
    ])
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.exit(main())
