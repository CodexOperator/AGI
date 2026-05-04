#!/usr/bin/env python3
"""zoom.py — produce a context bundle scoped to one chain or subtree.

Two zoom levels:
- big: full INJECTION.md (whole graph + attractor list)
- small: subtree of one target node + its parents/children only

Output: writes `<project>/sessions/<iter>/<agent_id>/context.md` and prints
that path on stdout for the dispatcher to pick up.

Usage:
    zoom.py <project_root> <iter> <agent_id> --level big
    zoom.py <project_root> <iter> <agent_id> --level small --target <node_id>
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project_root")
    ap.add_argument("iter_n", type=int)
    ap.add_argument("agent_id")
    ap.add_argument("--level", choices=["big", "small"], required=True)
    ap.add_argument("--target", default=None, help="node id (required for --level small)")
    args = ap.parse_args()

    root = Path(args.project_root).resolve()
    if not (root / "autoresearch-tree.config.json").exists():
        print(f"ERR: not a project root: {root}", file=sys.stderr)
        return 1

    sess_dir = root / "sessions" / f"iter-{args.iter_n:03d}" / args.agent_id
    sess_dir.mkdir(parents=True, exist_ok=True)
    out_path = sess_dir / "context.md"

    inject_path = root / "context" / "INJECTION.md"
    if not inject_path.exists():
        print(f"ERR: INJECTION.md missing at {inject_path}", file=sys.stderr)
        return 1
    inject_text = inject_path.read_text(encoding="utf-8")

    if args.level == "big":
        out_path.write_text(_compose_big(inject_text, args), encoding="utf-8")
    else:
        if not args.target:
            print("ERR: --target required for --level small", file=sys.stderr)
            return 1
        out_path.write_text(_compose_small(root, inject_text, args), encoding="utf-8")

    print(out_path)
    return 0


def _compose_big(inject_text: str, args: argparse.Namespace) -> str:
    return f"""# autoresearch-tree iteration {args.iter_n} — agent {args.agent_id}

## Zoom Level: BIG
You are exploring the WHOLE graph. Pick a high-level idea or new chain to extend.
Bias: introduce a fresh idea, fork an under-explored chain, or seed a new domain.

{inject_text}

## Your Task
1. Decide: extend longest chain, fork mid-chain, or start fresh idea.
2. Pick or create one node id (idea/hypothesis/experiment/mvp/outcome).
3. Run the experiment / implement the MVP / write the outcome.
4. When done, signal completion:
   ```
   python3 <plugin>/bin/cli.py done {args.iter_n} {args.agent_id} \\
     --verdict <proved|disproved|inconclusive_lean_proved:N|inconclusive_lean_disproved:N|pending> \\
     --confidence <0.0-1.0> \\
     --node-id <new_or_extended_node_id> \\
     --notes "<one-line>"
   ```

If stuck >2 attempts on same approach → write a `pending` verdict and stop.
"""


def _compose_small(root: Path, inject_text: str, args: argparse.Namespace) -> str:
    """Extract subtree around target from nodes/."""
    sys.path.insert(0, str(root / "src"))
    try:
        from graph_core.edge import Edge
    except Exception as e:
        return f"# zoom small fallback (loader unavailable: {e})\n\n{inject_text}"

    # Detect sqlite vs filesystem
    cfg_path = root / "autoresearch-tree.config.json"
    use_sqlite = False
    if cfg_path.exists():
        import json
        cfg = json.loads(cfg_path.read_text())
        use_sqlite = cfg.get("persistence", {}).get("type") == "sqlite"

    if use_sqlite:
        try:
            from graph_core.persistence.sqlite_backend import SQLiteBackend
            from graph_core.db_loader import DBLoader
            db_path = root / cfg["persistence"]["path"]
            g, loaded = DBLoader(SQLiteBackend(db_path)).load_directory()
        except Exception as e:
            return f"# zoom small fallback (sqlite unavailable: {e})\n\n{inject_text}"
    else:
        try:
            from graph_core.loader import load_directory
        except Exception as e:
            return f"# zoom small fallback (loader unavailable: {e})\n\n{inject_text}"
        g, loaded = load_directory(root / "nodes")

    # Wire children
    for ln in loaded:
        for parent_id in ln.node.parents:
            if g.has_node(parent_id):
                pn = g.get_node(parent_id)
                if pn is not None:
                    pn.children.add(ln.node.id)

    target = args.target
    if not g.has_node(target):
        return _compose_big(inject_text, args).replace(
            "## Zoom Level: BIG",
            f"## Zoom Level: SMALL (target '{target}' not found — falling back to big)",
        )

    # BFS up to depth 2 in both directions
    seen = {target}
    layers = {target: 0}
    frontier = [target]
    for _ in range(2):
        nxt = []
        for nid in frontier:
            n = g.get_node(nid)
            if n is None:
                continue
            for x in n.parents | n.children:
                if x not in seen:
                    seen.add(x)
                    layers[x] = layers[nid] + 1
                    nxt.append(x)
        frontier = nxt

    lines = [
        f"# autoresearch-tree iteration {args.iter_n} — agent {args.agent_id}",
        "",
        "## Zoom Level: SMALL",
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
        if n.parents:
            lines.append(f"    parents: {', '.join(sorted(n.parents)[:3])}")
        if n.children:
            lines.append(f"    children: {', '.join(sorted(n.children)[:3])}")

    lines.extend([
        "",
        "## Your Task",
        f"Extend or fork from `{target}`. Stay tight — don't wander to other chains.",
        "Acceptable: spawn one child node (hyp from idea, exp from hyp, mvp from exp, outcome from mvp).",
        "When done, signal completion:",
        "```",
        f"python3 <plugin>/bin/cli.py done {args.iter_n} {args.agent_id} \\",
        "  --verdict <verdict_state> --confidence <0.0-1.0> \\",
        f"  --node-id <new_node_id> --parent {target} \\",
        '  --notes "<one-line>"',
        "```",
        "",
        "If stuck >2 attempts → write `pending` verdict and stop.",
    ])
    return "\n".join(lines) + "\n"


if __name__ == "__main__":
    sys.exit(main())
