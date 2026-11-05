#!/usr/bin/env python3
"""metrics_cell.py — the hourly metrics job's guarded write of ONE node cell.

goal:g3.8 R2, re-based on node_commit by goal:g7.16.1.11.46.23 V8a 3a (the old writer is retired; council decision
alive 23:28:02Z 10-25). The job writes one line into a cell of the town node, as ONE commit of that node by exact
path, subject `board: <node> (<actor>)`. Every refusal is LOUD (rc 3, ONE `ERR:` line naming it and the recover
command): an hour is never skipped silently.

  * the node is ALREADY dirty (a hand edit), or a live pid holds the suite lock PAST hold_wait_s (it is waited for first): refused BEFORE the command
    runs, nothing written, HEAD untouched, nothing left dirty (a dirty node would publish the hand edit under the
    job's subject, and would refuse every later hour);
  * otherwise it runs <command> (it prints the ONE line, about a minute) and node_commit.land checks AGAIN right
    before writing (a human may have edited the node meanwhile), writes the cell + `edited_by` through
    node_writer.update_node, waits out a held suite lock up to hold_wait_s, and commits the node BY EXACT PATH;
  * a lock held past the bound, an exhausted index.lock retry, an unreadable lock state, or a hand edit that lands
    during the wait leaves the written bytes uncommitted, names the cause and the recover command, rc 3, never
    laundered.

Usage:
    metrics_cell.py <graph-root> <node-id> <cell> [--actor A] -- <command ...>
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


def _git(repo: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(repo), *args], capture_output=True, text=True)


def _node_path(root: Path, node_id: str) -> Path:
    kind, _, slug = node_id.partition(":")
    return root / "nodes" / kind / f"{slug}.md"


def _dirty(repo: Path, path: Path) -> bool | None:
    """True/False for the node's status against HEAD; None when git cannot say."""
    out = _git(repo, "status", "--porcelain", "--", str(path))
    return bool(out.stdout.strip()) if out.returncode == 0 else None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("root", help="the graph root (<repo>/.agi)")
    ap.add_argument("node", help="node id, e.g. town:local-maxxing")
    ap.add_argument("cell", help="the frontmatter cell to set")
    ap.add_argument("--actor", default="belam")
    raw = list(sys.argv[1:] if argv is None else argv)
    head, cmd = (raw[:raw.index("--")], raw[raw.index("--") + 1:]) if "--" in raw else (raw, [])
    args = ap.parse_args(head)   # everything after the first `--` is the command, verbatim
    if not cmd:
        print("ERR: metrics_cell.py: no command after --", file=sys.stderr)
        return 2
    root = Path(args.root).resolve()
    path = _node_path(root, args.node)
    top = _git(root, "rev-parse", "--show-toplevel")
    if top.returncode or not path.is_file():
        print(f"ERR: metrics_cell.py: {args.node} is not a node of a git repo under {root}",
              file=sys.stderr)
        return 2
    repo = Path(top.stdout.strip()).resolve()

    if _dirty(repo, path) is not False:   # git cannot say = refused too: a state we cannot read is not clean
        print(f"ERR: metrics_cell.py: {path} already dirty (or git cannot say): refused, nothing written; "
              f"{args.cell} not written (a hand edit would ride under the board subject)", file=sys.stderr)
        return 3

    import node_commit  # noqa: PLC0415
    import node_writer  # noqa: PLC0415
    try:   # a lock held at the START waits the SAME bounded hold_wait_s node_commit uses (one loop, not two); only a lock
        holder, waited = node_commit.wait_lock(root)   # STILL held past it is refused, BEFORE the command runs (nothing written)
    except (Exception, SystemExit) as exc:  # noqa: BLE001 -- an unreadable lock state is a hold we cannot rule out
        print(f"ERR: metrics_cell.py: the suite-lock state is unreadable ({type(exc).__name__}: {str(exc)[:100]}): "
              f"refused, nothing written; {args.cell} not written", file=sys.stderr)
        return 3
    if holder:
        print(f"ERR: metrics_cell.py: suite lock held past {waited:g}s (live pid {holder}): refused, "
              f"nothing written; {args.cell} not written", file=sys.stderr)
        return 3

    got = subprocess.run(cmd, capture_output=True, text=True)
    line = got.stdout.strip()
    if got.returncode or not line:
        print(f"ERR: metrics_cell.py: {cmd[-3:]} rc={got.returncode}, "
              f"{'no line' if not line else 'a line'}; {args.cell} not written", file=sys.stderr)
        return got.returncode or 1

    set_fm = {args.cell: line, **node_commit.provenance(root, args.actor)}
    try:   # an unreadable lock policy or holder FAILS CLOSED inside node_commit (a hold we cannot rule out is a hold)
        node_commit.land(root, args.node, f"board: {args.node} ({args.actor})",
                         lambda: node_writer.update_node(root, args.node, set_fm=set_fm))
    except (node_commit.CommitRefused, Exception, SystemExit) as exc:  # noqa: BLE001
        line_ = getattr(exc, "line", None) or f"{type(exc).__name__}: {str(exc)[:200]}"
        print(f"ERR: metrics_cell.py: {args.node}: {line_}", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    sys.exit(main())
