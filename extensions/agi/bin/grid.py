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

CONFIG_MARKER = "agi-tree.config.json"
# Compatibility window: legacy-named projects still resolve. Canonical name first.
CONFIG_MARKERS = (CONFIG_MARKER, "autoresearch-tree.config.json")
ID_RE = re.compile(r'^id:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
GIT_IDENT = ["-c", "user.name=grid", "-c", "user.email=grid@agi"]
REF_NS = "refs/grid"
FETCH_SPEC = f"+{REF_NS}/*:{REF_NS}/*"
PUSH_SPEC = f"{REF_NS}/*:{REF_NS}/*"


def find_project_root(start: Path | None = None) -> Path:
    cur = (start or Path.cwd()).resolve()
    for p in [cur, *cur.parents]:
        if any((p / name).exists() for name in CONFIG_MARKERS):
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


def _encode_component(s: str) -> str:
    """Percent-encode `s` into a single git-ref-safe, injective path component.

    `%` is escaped first (`%25`) so the escape alphabet cannot be forged by
    the input, then every character outside `[A-Za-z0-9_-]` is percent-encoded
    from its UTF-8 bytes (uppercase hex, e.g. `:` -> `%3A`, ` ` -> `%20`).
    Unlike collapsing to `-`, percent-encoding never maps two different
    characters to the same output byte, so the whole function stays
    injective: `@` and `-` can no longer collide, because `@` always becomes
    `%40` and a literal `-` is left alone.

    `.` is the one character kept literal outside the safe alphabet, for
    readability (`autoresearch.config.json` should not become an opaque
    string of `%2E`s) — but only where git allows it structurally. `.` is
    escaped instead of kept literal when it would otherwise violate a
    git-ref-format rule that has nothing to do with collisions: leading or
    trailing position in the component, a run of two or more (git forbids
    `..` in a refname), or a trailing `.lock` (git reserves that suffix for
    lock files). Each of those is a fixed function of `.`'s position in the
    input, so the same input always encodes the same way — encoding, not
    stripping, is what keeps it injective (the old `.strip(".")` made `"a"`
    and `"a."` collide; a component can never be produced two different ways
    here because `%` is escaped before anything else, so a literal `%2E`
    typed by a user is unreachable — it would first become `%252E`).
    """
    out = []
    dot_run = 0
    n = len(s)
    for i, ch in enumerate(s):
        if ch == "%":
            out.append("%25")
            dot_run = 0
        elif ch == ".":
            dot_run += 1
            if i == 0 or i == n - 1 or dot_run > 1:
                out.append("%2E")
            else:
                out.append(".")
        elif ("A" <= ch <= "Z") or ("a" <= ch <= "z") or ("0" <= ch <= "9") or ch in "_-":
            out.append(ch)
            dot_run = 0
        else:
            out.append("".join(f"%{b:02X}" for b in ch.encode("utf-8")))
            dot_run = 0
    component = "".join(out)
    if component.endswith(".lock"):
        # Every char above is 1:1 on the input, and escape sequences are
        # always uppercase-hex after `%`, so a literal trailing ".lock" here
        # can only come from a literal trailing ".lock" in `s` -- never from
        # an escape that happens to spell those letters. Safe to rewrite.
        component = component[:-5] + "%2Elock"
    return component


def sanitize(node_id: str) -> str:
    """Map a node id to `<type>/<rest>` — exactly two ref path segments.

    "hyp:zoom-x-r1" -> "hyp/zoom-x-r1": the type prefix becomes a ref namespace
    so refs group naturally by node type.

    Only the **first** colon separates. Every later one is escaped rather than
    turned into another path separator, because git cannot hold both a ref
    `a/b` and a ref `a/b/c` — the first is a file where the second needs a
    directory. Splitting on all colons made `exp:x-r1:extend8` collide with
    `exp:x-r1` and abort the whole `commit --all` run, losing versioning for
    every node after it (found live, 3 such ids in the agi-tree corpus).

    Every character outside the safe alphabet is percent-encoded (see
    `_encode_component`), so the map is injective by construction: no two
    distinct ids can ever produce the same ref path. This replaces an earlier
    version that collapsed everything outside `[A-Za-z0-9._%-]` to `-`, which
    let `level3:bin-stitch@v2` and a hypothetical `level3:bin-stitch-v2`
    collide on `level3/bin-stitch-v2` — confirmed live on 2026-08-24 by three
    `@v2` nodes minted that day (see `_sanitize_legacy` / `migrate-refs`,
    which move their refs onto the fixed scheme).
    """
    head, sep, tail = node_id.partition(":")
    parts = [_encode_component(head)] + (
        [_encode_component(tail)] if sep and tail else []
    )
    return "/".join(p for p in parts if p)


def _sanitize_legacy(node_id: str) -> str:
    """Frozen, byte-for-byte copy of the pre-fix `sanitize()`.

    Kept ONLY so `migrate-refs` can compute what a node's ref path used to be,
    to find and move it. Never "fix" this function: fixing it would make the
    migration blind to the very collisions it exists to repair, since the
    whole point is to compute the OLD (buggy) ref path, not a corrected one.
    """
    head, sep, tail = node_id.partition(":")

    def clean(s: str) -> str:
        s = s.replace("%", "%25").replace(":", "%3A")
        return re.sub(r"[^A-Za-z0-9._%-]", "-", s).strip(".")

    parts = [clean(head)] + ([clean(tail)] if sep and tail else [])
    return "/".join(p for p in parts if p)


def node_ref(node_id: str) -> str:
    return f"{REF_NS}/node/{sanitize(node_id)}"


def _node_ref_legacy(node_id: str) -> str:
    return f"{REF_NS}/node/{_sanitize_legacy(node_id)}"


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


def cmd_migrate_refs(root: Path, write: bool) -> None:
    """Move `refs/grid/node/*` from the pre-fix sanitize() scheme to the
    injective one, driven entirely by node ids found on disk today.

    Dry-run by default (`write=False`): prints what would happen, touches
    nothing. Idempotent: a ref only moves if its OLD-scheme ref still exists,
    so a second run (write or dry) sees nothing left to move and reports
    those ids as unchanged. Refuses to overwrite: if the destination already
    holds different history, that node is reported and skipped, never
    clobbered. Ids whose OLD ref is shared by more than one distinct id
    (a real pre-existing collision, not a rename) are reported separately
    and never touched -- there is no way to know which id's history the
    shared ref actually holds.
    """
    ensure_repo(root)
    ids = sorted({nid for p in iter_node_files(root)
                  if (nid := parse_node_id(p)) is not None})

    old_ref_to_ids: dict[str, list[str]] = {}
    for nid in ids:
        old_ref_to_ids.setdefault(_node_ref_legacy(nid), []).append(nid)
    collided = {r: v for r, v in old_ref_to_ids.items() if len(v) > 1}

    renamed = unchanged = conflicts = in_collision = 0
    for nid in ids:
        old_ref = _node_ref_legacy(nid)
        if old_ref in collided:
            in_collision += 1
            continue

        new_ref = node_ref(nid)
        if old_ref == new_ref:
            unchanged += 1
            continue

        old_tip = ref_tip(root, old_ref)
        if old_tip is None:
            unchanged += 1  # no history under the old scheme -- nothing to move
            continue

        new_tip = ref_tip(root, new_ref)
        if new_tip is not None:
            if new_tip == old_tip:
                unchanged += 1  # already migrated -- idempotent no-op
            else:
                conflicts += 1
                print(f"CONFLICT  {nid}: {new_ref} already exists with "
                      f"different history than {old_ref} -- not touched",
                      file=sys.stderr)
            continue

        action = "RENAME" if write else "WOULD-RENAME"
        print(f"{action}  {old_ref} -> {new_ref}  ({nid})")
        if write:
            git(root, "update-ref", new_ref, old_tip)
            git(root, "update-ref", "-d", old_ref, old_tip)
        renamed += 1

    for r, v in sorted(collided.items()):
        print(f"COLLISION  {r} shared by {len(v)} ids (pre-existing under "
              f"the old scheme, needs human triage -- cannot tell whose "
              f"history it holds): {', '.join(v)}", file=sys.stderr)

    mode = "write" if write else "dry-run"
    print(f"grid migrate-refs ({mode}): {renamed} renamed, {unchanged} "
          f"unchanged, {conflicts} conflict(s), {len(collided)} collided "
          f"old ref(s) covering {in_collision} id(s)")


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
    m = sub.add_parser("migrate-refs",
                       help="move refs/grid/node/* onto the injective "
                            "sanitize() scheme; dry-run unless --write")
    m.add_argument("--write", action="store_true")
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
    elif args.cmd == "migrate-refs":
        cmd_migrate_refs(root, args.write)
    elif args.cmd == "sync":
        cmd_sync(root, args.remote)
    elif args.cmd == "cron":
        cmd_cron(root, args.action, args.snapshot_mins)


if __name__ == "__main__":
    main()
