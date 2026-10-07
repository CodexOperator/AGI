#!/usr/bin/env python3
"""metrics_cell.py — the hourly metrics job's guarded write of ONE node cell.

goal:g3.8 R2. The job writes one line into a cell of the town node. A write that
cannot commit (write.py exit 3: MAIN's verify-suite.lock is held) leaves the node
dirty, and a dirty node refuses EVERY later write to it, thought-master's too,
until a human commits. So this wrapper never leaves the node dirty:

  * the node is ALREADY dirty (a hand edit), or the graph's suite lock is held by a
    live pid  -> ONE `skip:` line, exit 0, the node's bytes and HEAD untouched;
  * otherwise it runs <command> (it prints the ONE line), writes
    `write.py <node> "set <cell> <line>"`, and if the write still left the node dirty
    (the race after the checks above) it commits that node BY EXACT PATH
    (git add/commit -- <node>), never checkout or reset.

Usage:
    metrics_cell.py <graph-root> <node-id> <cell> [--actor A] -- <command ...>
"""
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

BIN = Path(__file__).resolve().parent


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
    repo = Path(top.stdout.strip())

    why = None
    if _dirty(repo, path) is not False:
        why = f"{args.node} is already dirty (or git cannot say); {args.cell} not written"
    else:
        try:
            import verification  # noqa: PLC0415 -- the ONE live-holder read write.py uses
            holder = verification.suite_lock_holder(root)
        except Exception:  # noqa: BLE001 -- no lock reading: write.py's own policy decides
            holder = None
        if holder:
            why = f"the suite lock is held by live pid {holder}; {args.cell} not written"
    if why:
        print(f"skip: {why}")
        return 0

    got = subprocess.run(cmd, capture_output=True, text=True)
    line = got.stdout.strip()
    if got.returncode or not line:
        print(f"ERR: metrics_cell.py: {cmd[-3:]} rc={got.returncode}, "
              f"{'no line' if not line else 'a line'}; {args.cell} not written", file=sys.stderr)
        return got.returncode or 1

    wrote = subprocess.run([sys.executable, str(BIN / "write.py"), args.node,
                            f"set {args.cell} {line}", "--actor", args.actor,
                            "--root", str(root)], capture_output=True, text=True)
    sys.stdout.write(wrote.stdout)
    sys.stderr.write(wrote.stderr)
    if _dirty(repo, path):   # landed uncommitted (exit 3) or died half-way: ours alone, the check above was clean
        _git(repo, "add", "--", str(path))
        done = _git(repo, "commit", "-q", "-m", f"write.py: {args.node} ({args.actor})",
                    "--", str(path))
        if done.returncode or _dirty(repo, path):
            print(f"ERR: metrics_cell.py: could not commit {args.node} by path: "
                  f"{(done.stderr or done.stdout).strip()[:200]}", file=sys.stderr)
            return wrote.returncode or 1
        return 0   # recovered: the cell is committed, the node is clean
    return wrote.returncode


if __name__ == "__main__":
    sys.exit(main())
