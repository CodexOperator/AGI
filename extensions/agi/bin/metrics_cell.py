#!/usr/bin/env python3
"""metrics_cell.py — the hourly metrics job's guarded write of ONE node cell.

goal:g3.8 R2. The job writes one line into a cell of the town node. A write that
cannot commit (write.py exit 3: MAIN's verify-suite.lock is held) leaves the node
dirty, and a dirty node refuses EVERY later write to it, thought-master's too,
until a human commits. So this wrapper never leaves the node dirty:

  * the node is ALREADY dirty (a hand edit), or the graph's suite lock is held by a
    live pid  -> ONE `skip:` line, exit 0, the node's bytes and HEAD untouched;
  * otherwise it runs <command> (it prints the ONE line, about a minute), checks AGAIN
    right before writing (a human may have edited the node meanwhile: ONE `skip:` line),
    writes `write.py <node> "set <cell> <line>"`, and if the write still left the node
    dirty (exit 3, the lock taken after the checks) it commits that node BY EXACT PATH
    (git add/commit -- <node>), never checkout or reset, but ONLY when the dirt is the
    cell write itself: the node's frontmatter and body equal HEAD's except for <cell> and
    edited_by. Anything else (a hand edit riding along) is left untouched, with an `ERR:`
    line carrying the recover command and rc != 0: a hand edit is never laundered.

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


def _only_cell_changed(repo: Path, path: Path, cell: str) -> bool:
    """True when the node's working bytes differ from HEAD's ONLY in `cell` and
    `edited_by` (the keys write.py's set verb owns): same body, same other keys."""
    import frontmatter  # noqa: PLC0415
    old = _git(repo, "show", f"HEAD:{path.relative_to(repo).as_posix()}")
    if old.returncode:
        return False
    try:
        new_text = path.read_text(encoding="utf-8")
    except OSError:
        return False
    fm_old, fm_new = frontmatter.read_frontmatter(old.stdout), frontmatter.read_frontmatter(new_text)
    parts_old, parts_new = frontmatter.split_frontmatter(old.stdout), frontmatter.split_frontmatter(new_text)
    if None in (fm_old, fm_new, parts_old, parts_new) or parts_old[1] != parts_new[1]:
        return False
    keys = (set(fm_old) | set(fm_new)) - {cell, "edited_by"}
    return cell in fm_new and all(fm_old.get(k) == fm_new.get(k) for k in keys)


def _guard(root: Path, repo: Path, path: Path, node: str, cell: str) -> str | None:
    """Why NOT to write now (the node is dirty, git cannot say, or a live pid holds the
    graph's suite lock), else None."""
    if _dirty(repo, path) is not False:
        return f"{node} is already dirty (or git cannot say); {cell} not written"
    try:
        import verification  # noqa: PLC0415 -- the ONE live-holder read write.py uses
        holder = verification.suite_lock_holder(root)
    except Exception:  # noqa: BLE001 -- no lock reading: write.py's own policy decides
        holder = None
    return f"the suite lock is held by live pid {holder}; {cell} not written" if holder else None


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

    why = _guard(root, repo, path, args.node, args.cell)
    if why:
        print(f"skip: {why}")
        return 0

    got = subprocess.run(cmd, capture_output=True, text=True)
    line = got.stdout.strip()
    if got.returncode or not line:
        print(f"ERR: metrics_cell.py: {cmd[-3:]} rc={got.returncode}, "
              f"{'no line' if not line else 'a line'}; {args.cell} not written", file=sys.stderr)
        return got.returncode or 1

    why = _guard(root, repo, path, args.node, args.cell)   # the node may have changed during the run
    if why:
        print(f"skip: {why}")
        return 0
    wrote = subprocess.run([sys.executable, str(BIN / "write.py"), args.node,
                            f"set {args.cell} {line}", "--actor", args.actor,
                            "--root", str(root)], capture_output=True, text=True)
    sys.stdout.write(wrote.stdout)
    sys.stderr.write(wrote.stderr)
    if not _dirty(repo, path):
        return wrote.returncode
    # The node was clean at the check above, so what is dirty now is this write's own landing
    # (exit 3: committed nothing) -- unless a human edited it since. Commit by exact path only
    # when nothing but the cell (and edited_by) differs from HEAD. The wording of write.py's
    # refusal is NOT a signal: exit 3 is shared with the held-lock refusal.
    rel = path.relative_to(repo).as_posix()
    msg = f"write.py: {args.node} ({args.actor})"
    recover = f"git -C {repo} add -- {rel} && git -C {repo} commit -q -m '{msg}' -- {rel}"
    try:   # g1.41 E3: no by-path commit while the suite lock is held; wait <= hold_wait_s, BEFORE the only-cell re-check below
        import time, verification  # noqa: PLC0415,E401
        end = time.monotonic() + verification.suite_lock_policy(root)["hold_wait_s"]
        while verification.suite_lock_holder(root) and time.monotonic() < end:
            time.sleep(0.25)
        held = verification.suite_lock_holder(root)
    except (Exception, SystemExit):  # noqa: BLE001 -- an unreadable policy is no hold
        held = None
    if held:
        print(f"ERR: metrics_cell.py: {args.node} left dirty: the suite lock (verify-suite) is held by live pid {held} past "
              f"values.core.suite_lock.hold_wait_s; NOT committed; recover once released: {recover}", file=sys.stderr)
        return 3
    if not _only_cell_changed(repo, path, args.cell):
        print(f"ERR: metrics_cell.py: {args.node} is dirty with more than {args.cell} (a hand "
              f"edit?); NOT committed, left as it is; recover by hand: {recover}", file=sys.stderr)
        return wrote.returncode or 1
    _git(repo, "add", "--", rel)
    done = _git(repo, "commit", "-q", "-m", msg, "--", rel)
    if done.returncode or _dirty(repo, path):
        print(f"ERR: metrics_cell.py: could not commit {args.node} by path: "
              f"{(done.stderr or done.stdout).strip()[:200]}; recover by hand: {recover}",
              file=sys.stderr)
        return wrote.returncode or 1
    return 0   # recovered: the cell is committed, the node is clean


if __name__ == "__main__":
    sys.exit(main())
