#!/usr/bin/env python3
"""grid.py — per-node version control: "the git grid". Harness-agnostic (TODO H10).

Three dimensions of history:
  D1 chain dimension   — the project repo's own git history. Not managed here.
  D2 node dimension    — branch `node/<id>` in <project>/.grid/repo; one commit
                         per version of that single node file.
  D3 session dimension — branch `session/<iter>/<agent>/<id>` for an agent's
                         in-flight drafts of a node before the overseer accepts.

Design notes (why this shape — see TODO.md H10):
  - One grid repo with a branch per node, NOT a .git dir per node folder:
    refs are cheap at 29k+ nodes, .git dirs are gigabytes.
  - Commits are made with plumbing (hash-object -> mktree -> commit-tree ->
    update-ref), never a checkout, so the grid repo is bare and node source of
    truth stays in nodes/ — loaders and renderers remain oblivious.
  - No dependencies beyond git and stdlib. Frontmatter id is parsed with a
    regex, not yaml, so this file runs anywhere.

Usage:
  grid.py init
  grid.py commit --all              # snapshot every changed node -> D2
  grid.py commit FILE [FILE..]      # snapshot specific node files -> D2
  grid.py commit FILE --session ITER AGENT   # snapshot draft -> D3
  grid.py log NODE_ID [-n N]
  grid.py diff NODE_ID [--back N]   # default: latest vs previous
  grid.py status                    # per-node drift vs branch tip
  grid.py versions NODE_ID          # version count (the vN marker)
  grid.py sync [REMOTE]             # push all branches; cron-able
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

CONFIG_MARKER = "autoresearch-tree.config.json"
ID_RE = re.compile(r'^id:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
GIT_IDENT = ["-c", "user.name=grid", "-c", "user.email=grid@agi"]


def find_project_root(start: Path | None = None) -> Path:
    cur = (start or Path.cwd()).resolve()
    for p in [cur, *cur.parents]:
        if (p / CONFIG_MARKER).exists():
            return p
    sys.exit(f"ERR: no {CONFIG_MARKER} found walking up from {cur}")


def grid_dir(root: Path) -> Path:
    return root / ".grid" / "repo"


def git(root: Path, *args: str, input_text: str | None = None, check: bool = True) -> str:
    res = subprocess.run(
        ["git", *GIT_IDENT, "-C", str(grid_dir(root)), *args],
        capture_output=True, text=True, input=input_text,
    )
    if check and res.returncode != 0:
        sys.exit(f"ERR: git {' '.join(args)}: {res.stderr.strip()}")
    return res.stdout.strip()


def sanitize(node_id: str) -> str:
    # "hyp:zoom-x-r1" -> "hyp/zoom-x-r1": the type prefix becomes a ref
    # namespace so branches group naturally by node type.
    parts = node_id.replace(":", "/").split("/")
    clean = [re.sub(r"[^A-Za-z0-9._-]", "-", p).strip(".") for p in parts if p]
    return "/".join(clean)


def node_branch(node_id: str) -> str:
    return f"node/{sanitize(node_id)}"


def session_branch(iter_n: str, agent: str, node_id: str) -> str:
    return f"session/{sanitize(iter_n)}/{sanitize(agent)}/{sanitize(node_id)}"


def parse_node_id(path: Path) -> str | None:
    m = ID_RE.search(path.read_text(encoding="utf-8"))
    return m.group(1) if m else None


def branch_tip(root: Path, branch: str) -> str | None:
    res = subprocess.run(
        ["git", "-C", str(grid_dir(root)), "rev-parse", "-q", "--verify",
         f"refs/heads/{branch}"],
        capture_output=True, text=True,
    )
    return res.stdout.strip() or None


def cmd_init(root: Path) -> None:
    gd = grid_dir(root)
    if gd.exists():
        print(f"grid already at {gd}")
        return
    gd.mkdir(parents=True)
    subprocess.run(["git", "init", "--bare", "-q", str(gd)], check=True)
    print(f"grid initialized: {gd}")
    gi = root / ".gitignore"
    if gi.exists() and ".grid/" not in gi.read_text(encoding="utf-8"):
        print("NOTE: add `.grid/` to the project .gitignore — the grid is a "
              "parallel dimension, not project content.")


def commit_file(root: Path, path: Path, branch: str, msg_prefix: str) -> str | None:
    """Snapshot one node file onto `branch`. Returns new version tag or None."""
    node_id = parse_node_id(path)
    if node_id is None:
        print(f"skip (no id frontmatter): {path}", file=sys.stderr)
        return None
    blob = git(root, "hash-object", "-w", str(path.resolve()))
    tip = branch_tip(root, branch)
    if tip:
        old_blob = git(root, "rev-parse", f"{tip}:node.md", check=False)
        if old_blob == blob:
            return None  # unchanged — versions record change, not time
    tree = git(root, "mktree", input_text=f"100644 blob {blob}\tnode.md\n")
    n = int(git(root, "rev-list", "--count", tip)) + 1 if tip else 1
    parent = ["-p", tip] if tip else []
    commit = git(root, "commit-tree", tree, *parent, "-m",
                 f"{msg_prefix}v{n} {node_id}")
    git(root, "update-ref", f"refs/heads/{branch}", commit)
    return f"v{n}"


def iter_node_files(root: Path):
    yield from sorted((root / "nodes").rglob("*.md"))


def cmd_commit(root: Path, files: list[str], do_all: bool,
               session: tuple[str, str] | None) -> None:
    if not grid_dir(root).exists():
        cmd_init(root)
    paths = list(iter_node_files(root)) if do_all else [Path(f) for f in files]
    if not paths:
        sys.exit("ERR: give node files or --all")
    written = 0
    for p in paths:
        if not p.exists():
            print(f"skip (missing): {p}", file=sys.stderr)
            continue
        node_id = parse_node_id(p)
        if node_id is None:
            print(f"skip (no id): {p}", file=sys.stderr)
            continue
        if session:
            branch = session_branch(session[0], session[1], node_id)
            prefix = f"session {session[0]}/{session[1]}: "
        else:
            branch = node_branch(node_id)
            prefix = ""
        v = commit_file(root, p, branch, prefix)
        if v:
            written += 1
            print(f"{v}  {branch}")
    print(f"grid: {written} new version(s)")


def resolve_branch(root: Path, node_id: str) -> str:
    branch = node_branch(node_id)
    if branch_tip(root, branch) is None:
        sys.exit(f"ERR: no grid history for {node_id} (branch {branch})")
    return branch


def cmd_log(root: Path, node_id: str, n: int) -> None:
    branch = resolve_branch(root, node_id)
    print(git(root, "log", f"-{n}", "--format=%h %ad %s", "--date=short", branch))


def cmd_diff(root: Path, node_id: str, back: int) -> None:
    branch = resolve_branch(root, node_id)
    count = int(git(root, "rev-list", "--count", branch))
    if count < back + 1:
        sys.exit(f"ERR: only {count} version(s); cannot go back {back}")
    print(git(root, "diff", f"{branch}~{back}", branch, "--", "node.md"))


def cmd_versions(root: Path, node_id: str) -> None:
    branch = node_branch(node_id)
    tip = branch_tip(root, branch)
    print(int(git(root, "rev-list", "--count", tip)) if tip else 0)


def cmd_status(root: Path) -> None:
    if not grid_dir(root).exists():
        sys.exit("ERR: no grid — run `grid.py init`")
    new = changed = clean = 0
    for p in iter_node_files(root):
        node_id = parse_node_id(p)
        if node_id is None:
            continue
        tip = branch_tip(root, node_branch(node_id))
        if tip is None:
            new += 1
            print(f"NEW      {node_id}")
            continue
        blob = git(root, "hash-object", str(p.resolve()))
        old = git(root, "rev-parse", f"{tip}:node.md", check=False)
        if blob == old:
            clean += 1
        else:
            changed += 1
            print(f"CHANGED  {node_id}")
    print(f"grid status: {new} new, {changed} changed, {clean} clean")


def cmd_sync(root: Path, remote: str | None) -> None:
    remotes = git(root, "remote").splitlines()
    if remote and "origin" not in remotes:
        git(root, "remote", "add", "origin", remote)
    elif remote and remote not in remotes:
        git(root, "remote", "set-url", "origin", remote)
    if "origin" not in git(root, "remote").splitlines():
        sys.exit("ERR: no remote — grid.py sync <remote-url> once to set origin")
    print(git(root, "push", "--all", "origin") or "grid: synced")


def main() -> None:
    ap = argparse.ArgumentParser(description="per-node git grid (D2/D3)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    c = sub.add_parser("commit")
    c.add_argument("files", nargs="*")
    c.add_argument("--all", action="store_true")
    c.add_argument("--session", nargs=2, metavar=("ITER", "AGENT"))
    lg = sub.add_parser("log")
    lg.add_argument("node_id")
    lg.add_argument("-n", type=int, default=20)
    d = sub.add_parser("diff")
    d.add_argument("node_id")
    d.add_argument("--back", type=int, default=1)
    v = sub.add_parser("versions")
    v.add_argument("node_id")
    sub.add_parser("status")
    s = sub.add_parser("sync")
    s.add_argument("remote", nargs="?")
    args = ap.parse_args()
    root = find_project_root()
    if args.cmd == "init":
        cmd_init(root)
    elif args.cmd == "commit":
        cmd_commit(root, args.files, args.all,
                   tuple(args.session) if args.session else None)
    elif args.cmd == "log":
        cmd_log(root, args.node_id, args.n)
    elif args.cmd == "diff":
        cmd_diff(root, args.node_id, args.back)
    elif args.cmd == "versions":
        cmd_versions(root, args.node_id)
    elif args.cmd == "status":
        cmd_status(root)
    elif args.cmd == "sync":
        cmd_sync(root, args.remote)


if __name__ == "__main__":
    main()
