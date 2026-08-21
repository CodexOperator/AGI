#!/usr/bin/env python3
"""grid.py — per-node version control: "the git grid". Harness-agnostic (TODO H10).

Three dimensions of history, all inside the PROJECT repo itself:
  D1 chain dimension   — the repo's normal history (refs/heads/*). Not managed here.
  D2 node dimension    — ref `refs/grid/node/<id>`; one commit per version of
                         that single node file.
  D3 session dimension — ref `refs/grid/session/<iter>/<agent>/<id>` for an
                         agent's in-flight drafts before the parent accepts.

Design notes (why this shape — see TODO.md H10):
  - Baked into the work repo via a dedicated ref namespace, NOT a separate
    repo and NOT submodules. Grid refs are never checked out, never appear in
    `git branch`, and share the object store — a node version whose content is
    also committed on D1 is the same blob, so D2 costs almost nothing.
  - Commits are made with plumbing (hash-object -> mktree -> commit-tree ->
    update-ref), never a checkout, so the working tree is untouchable by
    design and loaders/renderers stay oblivious.
  - `git clone` does not fetch custom refs by default. `grid.py init` adds the
    fetch refspec to origin so a fresh machine gets the grid with `git fetch`.
  - No dependencies beyond git and stdlib. Frontmatter id is parsed with a
    regex, not yaml, so this file runs anywhere.

Usage:
  grid.py init                      # idempotent; configures origin refspec
  grid.py commit --all              # snapshot every changed node -> D2
  grid.py commit FILE [FILE..]      # snapshot specific node files -> D2
  grid.py commit FILE --session ITER AGENT   # snapshot draft -> D3
  grid.py log NODE_ID [-n N]
  grid.py diff NODE_ID [--back N]   # default: latest vs previous
  grid.py status                    # per-node drift vs ref tip
  grid.py versions NODE_ID          # version count (the vN marker)
  grid.py sync [REMOTE]             # push refs/grid/* to origin (manual/one-off)
  grid.py cron install|show|remove  # manage the two-cadence sync cron entries
                                    #   */N: snapshot + push grid refs
                                    #   hourly: push the D1 branch
"""

import argparse
import re
import subprocess
import sys
from pathlib import Path

CONFIG_MARKER = "autoresearch-tree.config.json"
ID_RE = re.compile(r'^id:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
GIT_IDENT = ["-c", "user.name=grid", "-c", "user.email=grid@agi"]
REF_NS = "refs/grid"
FETCH_SPEC = f"+{REF_NS}/*:{REF_NS}/*"
PUSH_SPEC = f"{REF_NS}/*:{REF_NS}/*"


def find_project_root(start: Path | None = None) -> Path:
    cur = (start or Path.cwd()).resolve()
    for p in [cur, *cur.parents]:
        if (p / CONFIG_MARKER).exists():
            return p
    sys.exit(f"ERR: no {CONFIG_MARKER} found walking up from {cur}")


def git(root: Path, *args: str, input_text: str | None = None, check: bool = True) -> str:
    res = subprocess.run(
        ["git", *GIT_IDENT, "-C", str(root), *args],
        capture_output=True, text=True, input=input_text,
    )
    if check and res.returncode != 0:
        sys.exit(f"ERR: git {' '.join(args)}: {res.stderr.strip()}")
    return res.stdout.strip()


def sanitize(node_id: str) -> str:
    # "hyp:zoom-x-r1" -> "hyp/zoom-x-r1": the type prefix becomes a ref
    # namespace so refs group naturally by node type.
    parts = node_id.replace(":", "/").split("/")
    clean = [re.sub(r"[^A-Za-z0-9._-]", "-", p).strip(".") for p in parts if p]
    return "/".join(clean)


def node_ref(node_id: str) -> str:
    return f"{REF_NS}/node/{sanitize(node_id)}"


def session_ref(iter_n: str, agent: str, node_id: str) -> str:
    return f"{REF_NS}/session/{sanitize(iter_n)}/{sanitize(agent)}/{sanitize(node_id)}"


def parse_node_id(path: Path) -> str | None:
    m = ID_RE.search(path.read_text(encoding="utf-8"))
    return m.group(1) if m else None


def ref_tip(root: Path, ref: str) -> str | None:
    res = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "-q", "--verify", ref],
        capture_output=True, text=True,
    )
    return res.stdout.strip() or None


def ensure_repo(root: Path) -> None:
    if subprocess.run(["git", "-C", str(root), "rev-parse", "--git-dir"],
                      capture_output=True).returncode != 0:
        sys.exit(f"ERR: {root} is not a git repo — the grid bakes into the "
                 "project repo; `git init` it first")


def cmd_init(root: Path) -> None:
    ensure_repo(root)
    remotes = git(root, "remote").splitlines()
    if "origin" in remotes:
        specs = git(root, "config", "--get-all", "remote.origin.fetch",
                    check=False).splitlines()
        if FETCH_SPEC not in specs:
            git(root, "config", "--add", "remote.origin.fetch", FETCH_SPEC)
            print(f"grid: added fetch refspec {FETCH_SPEC} to origin")
        else:
            print("grid: origin refspec already configured")
    else:
        print("grid: no origin remote yet — refs work locally; run "
              "`grid.py sync <remote-url>` or `init` again after adding one")
    count = len(git(root, "for-each-ref", REF_NS,
                    "--format=%(refname)").splitlines())
    print(f"grid ready: {count} existing version ref(s) under {REF_NS}/")


def commit_file(root: Path, path: Path, ref: str, msg_prefix: str) -> str | None:
    """Snapshot one node file onto `ref`. Returns new version tag or None."""
    node_id = parse_node_id(path)
    if node_id is None:
        print(f"skip (no id frontmatter): {path}", file=sys.stderr)
        return None
    blob = git(root, "hash-object", "-w", str(path.resolve()))
    tip = ref_tip(root, ref)
    if tip:
        old_blob = git(root, "rev-parse", f"{tip}:node.md", check=False)
        if old_blob == blob:
            return None  # unchanged — versions record change, not time
    tree = git(root, "mktree", input_text=f"100644 blob {blob}\tnode.md\n")
    n = int(git(root, "rev-list", "--count", tip)) + 1 if tip else 1
    parent = ["-p", tip] if tip else []
    commit = git(root, "commit-tree", tree, *parent, "-m",
                 f"{msg_prefix}v{n} {node_id}")
    git(root, "update-ref", ref, commit)
    return f"v{n}"


def iter_node_files(root: Path):
    yield from sorted((root / "nodes").rglob("*.md"))


def cmd_commit(root: Path, files: list[str], do_all: bool,
               session: tuple[str, str] | None, prefix: str = "") -> None:
    ensure_repo(root)
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
            ref = session_ref(session[0], session[1], node_id)
            msg_prefix = prefix + f"session {session[0]}/{session[1]}: "
        else:
            ref = node_ref(node_id)
            msg_prefix = prefix
        v = commit_file(root, p, ref, msg_prefix)
        if v:
            written += 1
            print(f"{v}  {ref.removeprefix(REF_NS + '/')}")
    print(f"grid: {written} new version(s)")


def resolve_ref(root: Path, node_id: str) -> str:
    ref = node_ref(node_id)
    if ref_tip(root, ref) is None:
        sys.exit(f"ERR: no grid history for {node_id} ({ref})")
    return ref


def cmd_log(root: Path, node_id: str, n: int) -> None:
    ref = resolve_ref(root, node_id)
    print(git(root, "log", f"-{n}", "--format=%h %ad %s", "--date=short", ref))


def cmd_diff(root: Path, node_id: str, back: int) -> None:
    ref = resolve_ref(root, node_id)
    count = int(git(root, "rev-list", "--count", ref))
    if count < back + 1:
        sys.exit(f"ERR: only {count} version(s); cannot go back {back}")
    print(git(root, "diff", f"{ref}~{back}", ref, "--", "node.md"))


def cmd_versions(root: Path, node_id: str) -> None:
    tip = ref_tip(root, node_ref(node_id))
    print(int(git(root, "rev-list", "--count", tip)) if tip else 0)


def cmd_status(root: Path) -> None:
    ensure_repo(root)
    new = changed = clean = 0
    for p in iter_node_files(root):
        node_id = parse_node_id(p)
        if node_id is None:
            continue
        tip = ref_tip(root, node_ref(node_id))
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
    ensure_repo(root)
    remotes = git(root, "remote").splitlines()
    if remote and "origin" not in remotes:
        git(root, "remote", "add", "origin", remote)
    elif remote:
        git(root, "remote", "set-url", "origin", remote)
    if "origin" not in git(root, "remote").splitlines():
        sys.exit("ERR: no origin — grid.py sync <remote-url> once to set it")
    cmd_init(root)  # keep the fetch refspec aligned on every sync
    out = git(root, "push", "origin", PUSH_SPEC)
    print(out or "grid: synced")


def cron_log(root: Path) -> Path:
    return Path.home() / "logs" / f"grid-sync-{root.name}.log"


def cron_lines(root: Path, branch: str, mins: int, log: Path) -> list[str]:
    """The two-cadence entries. The `cd` is load-bearing: cron runs from $HOME
    and find_project_root walks up from cwd — a cd-less line fails silently."""
    script = Path(__file__).resolve()
    snap = (f"*/{mins} * * * * cd {root} && "
            f"python3 {script} commit --all --prefix 'cron: ' >> {log} 2>&1 && "
            f"git push -q origin '{PUSH_SPEC}' >> {log} 2>&1")
    d1 = f"7 * * * * git -C {root} push -q origin {branch} >> {log} 2>&1"
    return [snap, d1]


def read_crontab() -> list[str]:
    res = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    return res.stdout.splitlines() if res.returncode == 0 else []


def write_crontab(lines: list[str]) -> None:
    text = "\n".join(lines) + ("\n" if lines else "")
    res = subprocess.run(["crontab", "-"], input=text, capture_output=True,
                         text=True)
    if res.returncode != 0:
        sys.exit(f"ERR: crontab install failed: {res.stderr.strip()}")


def cmd_cron(root: Path, action: str, mins: int) -> None:
    ensure_repo(root)
    log = cron_log(root)
    marker = str(log)  # unique per project; filters our entries only
    current = read_crontab()
    ours = [l for l in current if marker in l]
    keep = [l for l in current if marker not in l]
    if action == "show":
        print("\n".join(ours) if ours else "grid cron: no entries installed")
        return
    if action == "remove":
        write_crontab(keep)
        print(f"grid cron: removed {len(ours)} entr(y/ies)")
        return
    # install (idempotent: replaces any prior entries for this project)
    branch = git(root, "symbolic-ref", "--short", "HEAD")
    if "origin" not in git(root, "remote").splitlines():
        sys.exit("ERR: no origin remote — `grid.py sync <remote-url>` first")
    log.parent.mkdir(parents=True, exist_ok=True)
    new = cron_lines(root, branch, mins, log)
    write_crontab(keep + new)
    print(f"grid cron: installed (snapshot every {mins}m, {branch} hourly):")
    print("\n".join(new))


def main() -> None:
    ap = argparse.ArgumentParser(description="per-node git grid (D2/D3)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    c = sub.add_parser("commit")
    c.add_argument("files", nargs="*")
    c.add_argument("--all", action="store_true")
    c.add_argument("--session", nargs=2, metavar=("ITER", "AGENT"))
    c.add_argument("--prefix", default="",
                   help='commit-message prefix, e.g. "cron: " for auto-snapshots')
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
    cr = sub.add_parser("cron")
    cr.add_argument("action", choices=["install", "show", "remove"])
    cr.add_argument("--snapshot-mins", type=int, default=5)
    args = ap.parse_args()
    root = find_project_root()
    if args.cmd == "init":
        cmd_init(root)
    elif args.cmd == "commit":
        cmd_commit(root, args.files, args.all,
                   tuple(args.session) if args.session else None,
                   prefix=args.prefix)
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
    elif args.cmd == "cron":
        cmd_cron(root, args.action, args.snapshot_mins)


if __name__ == "__main__":
    main()
