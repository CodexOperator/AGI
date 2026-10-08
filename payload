#!/usr/bin/env python3
"""inject.py — write the injected map, from the viewport's own frame stream.

`goal:g9.4` / `goal:g9.7`, and the owner's instruction that **all work starts
and ends on the graph**. This replaces `render-context.py`, which composed
`INJECTION.md` from a *fourth* tree renderer (`renderers/ascii`) that no human
ever looked at, beside a viewport nobody's context came from.

## What actually changed, and what deliberately did not

The briefing — the nine sections of rules, metrics and commands an agent is
judged against — moved to `briefing.py` in L1.04 and is **unchanged here**.
This file only swaps which renderer draws the tree underneath it:

    render-context.py:  briefing + renderers/ascii  -> INJECTION.md
    inject.py:          briefing + viewport frames  -> INJECTION.md

So the thing a session is handed is now, by construction, the thing
`viewport.py --emit llm` shows — and `--emit human` is the same stream. Before
this there was no instrument pointing at what an agent actually receives,
which is `goal:g9`'s founding complaint.

## Why this file exists rather than a flag on the viewport

**`viewport.py` opens nothing for writing, and that invariant is worth more
than the file this would have saved.** It is safe to run at any moment,
including mid-iteration of the loop it is watching, and a `--write` flag would
end that. So the viewport renders to stdout and *this* composes and writes.
The seam is the same one `goal:g13` draws everywhere else: readers read,
writers write, and the writer is the small thing.

## Honest scope

`renderers/ascii` is now unused by the injection path but is **not deleted** —
it has its own tests and is still importable. `zoom.py`'s internal renderers
are untouched: they build *kid* context, and moving those onto the frame
stream changes what every spawned agent receives, which is its own change with
its own falsifier. The "five render paths" count goes to four, not one.
"""
from __future__ import annotations

import sys
from pathlib import Path

BIN = Path(__file__).resolve().parent
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(BIN.parent / "src"))

import briefing  # noqa: E402
import locations  # noqa: E402
import viewport  # noqa: E402
import zoom  # noqa: E402

#: How many frames the written map carries. `render-context.py` capped its
#: ASCII block at 200 lines for the same reason: both injectors truncate, and
#: a map longer than the truncation is a map whose tail nobody reads.
#:
#: 200 -> 90 (SD.08, hypothesis:l3w4-context-load-minimal): the graph frame
#: stream is 85% of the injected file (7187 of 8407 tok, measured o200k on
#: 2026-09-08) and is paid by EVERY role EVERY turn. Deep navigation does not
#: need to be always-on: this is the map's TOP view, and a role that needs a
#: deeper or anchored slice reads it on demand (`viewport.py --anchor`, zoom),
#: which is cheaper than carrying 8.4k tokens of static tree per turn. 90
#: frames keeps the tree under the parent-targeted ~3k-token stream while
#: preserving the node-catalog top view; `--frames` still overrides for a full
#: dump.
DEFAULT_FRAMES = 90


def build_text(root: Path, max_frames: int = DEFAULT_FRAMES) -> str:
    """The full injected map. Pure — computes a string, writes nothing."""
    g, _loaded = zoom._load_wired_graph(root)

    fm_by_id: dict = {}
    for d in sorted((root / "nodes").glob("*")):
        if d.is_dir():
            fm_by_id.update(zoom._frontmatter_for(root, d.name))

    # Chain diagnostics are descriptive, never a target -- but "unavailable"
    # is not the same claim as "0 chains", and shipping the first while the
    # engine imports fine would quietly downgrade the map. Computed here
    # because it is the caller's job to supply what it can, and absence stays
    # honest when it cannot.
    chain_stats = None
    try:
        from chain_engine.chains import find_chains
        chains = find_chains(g, graph_dir=str(root / "nodes"))
        chain_stats = (len(chains),
                       max((len(c) for c in chains), default=0))
    except Exception as exc:                                     # noqa: BLE001
        print(f"inject: chain diagnostics unavailable "
              f"({type(exc).__name__}: {exc})", file=sys.stderr)

    brief = briefing.build(root, g, _loaded, chain_stats=chain_stats)
    # goal:s23 — the injected map loses retired nodes. `render-context.py` did
    # this with a `_LiveOnly` graph view; the equivalent here is a flag on the
    # walk. An agent handed a retired node as a live chain head will extend
    # it, which is the whole reason retirement exists.
    frames = viewport.frame_stream(g, fm_by_id, None, 3, hide_deprecated=True)

    body = viewport.render_llm(frames, 0, 0, max_frames, 10_000,
                               status="", brief=brief)
    return (
        "# agi-tree INJECTION CONTEXT\n"
        f"_generated {brief.generated_at}_\n"
        "\n"
        + body
    )


def project_root(start=None, nodes_dir=None):
    """This entry point's root resolution, as a function rather than inline.

    Split out of `main` so `test_locations.py` can probe it the way it probes
    every other entry point — the invariant there is *one question, one
    answer, wherever you are standing* (`goal:g8.2`), and the failure it
    guards against is a generator silently answering `os.getcwd()` and aiming
    at `<repo>/nodes` instead of `<repo>/.agi/nodes`. Resolution that only
    exists inside `main` is resolution no test can reach.
    """
    root = locations.find_project_root(Path(start) if start else Path.cwd())
    if root is None and nodes_dir:
        # `render-context.py` was invoked as `render-context.py <project>/nodes`
        # and driver.sh still passes that argument. Accept it rather than
        # making the caller change shape at the same moment the renderer does.
        root = locations.find_project_root(Path(nodes_dir))
    return Path(root) if root is not None else None


def main(argv: list[str] | None = None) -> int:
    import argparse

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("nodes_dir", nargs="?", default=None,
                    help="ignored; accepted for render-context.py compatibility")
    ap.add_argument("--root", default=None, help="any path inside the project")
    ap.add_argument("--frames", type=int, default=DEFAULT_FRAMES)
    ap.add_argument("--stdout", action="store_true",
                    help="print instead of writing, for inspection")
    args = ap.parse_args(argv)

    root = project_root(args.root, args.nodes_dir)
    if root is None:
        print("inject: no project found (no enclosing .agi/ with a config)",
              file=sys.stderr)
        return 2

    text = build_text(root, args.frames)
    if args.stdout:
        print(text, end="")
        return 0

    out = root / "context" / "INJECTION.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")
    print(f"wrote: {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
