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
  - No dependencies beyond git and stdlib for the grid itself. Frontmatter id
    is parsed with a regex, not yaml, so this file runs anywhere. The one
    exception is deliberate: the non-session `commit` path runs the evidence
    gate over the files it is about to version (`evidence_gate.enforce_on_disk`,
    which needs yaml and `node_writer` — imported there, not here), because a
    node's bytes are ACCEPTED at commit and that is the one place every write
    path passes (hypothesis:gate-must-sit-on-the-commit-path, goal:g7).
  - **Two roots, two jobs (goal:g11).** Callers hand this file the GRAPH root
    (`<repo>/.agi`). Node files are found under it; every git invocation runs
    against `repo_root()` of it, because that is where `refs/grid/*` and the
    object store live. See the block comment above `repo_root` for what the
    conflated version silently got wrong.

Usage:
  grid.py init                      # idempotent; configures origin refspec
  grid.py commit --all              # snapshot every changed node -> D2
  grid.py commit FILE [FILE..]      # snapshot specific node files -> D2
  grid.py commit FILE --session ITER AGENT   # snapshot draft -> D3
  grid.py log NODE_ID [-n N]
  grid.py diff NODE_ID [--back N]   # default: latest vs previous
  grid.py status                    # per-node drift vs ref tip
  grid.py versions NODE_ID          # version count (the vN marker)
  grid.py payload NODE_ID [--version N] [--out PATH]
                                    # read a build node's payload back out of
                                    # its ref (goal:g6.3); bytes to stdout, or
                                    # written to PATH with its recorded mode
  grid.py checkout --all [--dir D]  # materialize payloads into <project>/payloads/
                                    # — the staged copy an author edits (goal:g6.1)
  grid.py sync [REMOTE]             # push refs/grid/* to origin (manual/one-off)
  grid.py migrate-trunk [--from NS] [--to NS]   # move every ref onto NS (the
                                    # configured grid.storage_trunk when --to is
                                    # absent); dry-run unless --write (goal:g14.14.7)
  grid.py cron install|show|remove  # manage the two-cadence sync cron entries
                                    #   */N: snapshot + push grid refs
                                    #   hourly: push the D1 branch
"""

import argparse
import fcntl
import os
import re
import stat
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

# goal:g11 — one resolver for every path. Plain sibling import; every entry
# point under `bin/` already has this directory on sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import evidence_gate  # noqa: E402
import anonymize  # noqa: E402 -- HOME_PATH_RE: the ONE home-path spelling (covers this box's passwd homes, not just /home/)
import branches  # noqa: E402
import locations  # noqa: E402
import verification  # noqa: E402 -- acquire_suite_lock: the ONE suite-lock reader

ID_RE = re.compile(r'^id:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
# goal:g2.5 "Tension resolved 2026-08-25" — the permanent identifier grid.py
# now keys writes on. Same line shape as ID_RE, parsed the same stdlib-regex
# way (this file stays yaml-free by design — see module docstring).
MINT_ID_RE = re.compile(r'^mint_id:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
PAYLOAD_REF_RE = re.compile(r'^payload_ref:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
LOCATION_RE = re.compile(r'^location:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
PARENTS_RE = re.compile(r'^parents:[ \t]*$', re.MULTILINE)
PARENTS_INLINE_RE = re.compile(r'^parents:\s*\[([^\]]*)\]\s*$', re.MULTILINE)
PARENTS_SCALAR_RE = re.compile(r'^parents:\s*([^\n\[][^\n]*)$', re.MULTILINE)
GIT_IDENT = ["-c", "user.name=grid", "-c", "user.email=grid@agi"]
DEFAULT_REF_NS = "refs/grid"
REF_NS = DEFAULT_REF_NS
#: Read-only namespaces (config `grid.legacy_namespaces`), filled by `apply_storage_trunk`.
LEGACY_NS: list[str] = []
# Tree entry names inside a node's D2 commit. `node.md` predates payloads and
# keeps its name so every existing reader (`rev-parse <tip>:node.md`) still
# works. `payload` is goal:g6.3's addition: one node owns exactly one
# `payload_ref`, so a flat entry name is unambiguous and keeps `mktree` to the
# single tree level it already builds. The path the payload belongs at in the
# engine tree stays where it always was — the node's own `payload_ref` field —
# rather than being duplicated in the ref layout.
NODE_ENTRY = "node.md"
PAYLOAD_ENTRY = "payload"
# The graph repo's staged payload checkout (`grid.py checkout`). Gitignored:
# the committed home of these bytes is the node's grid ref, and this directory
# is a working copy of it in exactly the sense git's worktree is a working copy
# of the index. Losing it costs nothing.
PAYLOAD_DIR = "payloads"
GIT_MODE_REGULAR = "100644"
GIT_MODE_EXEC = "100755"
GIT_MODE_SYMLINK = "120000"
FETCH_SPEC = f"{REF_NS}/node/*:{REF_NS}/node/*"
FETCH_SPECS = [FETCH_SPEC, f"{REF_NS}/session/*:{REF_NS}/session/*"]
#: the two kinds of ref `push_batches` lists, and the ONLY two a push may carry (goal:g7.16.1.11.46.16, council 10:50:48Z 10-26 R2): a wide
#: `<ns>/*` refspec spans slashes and would carry `refs/grid/origin-snap/*` and every legacy namespace to origin with it.
PUSH_KINDS = ("node", "session")
PUSH_SPECS = [f"{REF_NS}/{k}/*:{REF_NS}/{k}/*" for k in PUSH_KINDS]


def ref_ns_for(root: Path) -> str:
    """The grid ref namespace for graph root `root` (goal:g14.14.7).

    This is the ONE resolver the nine derived call sites in this file already
    keyed on — it now reads `grid.storage_trunk` out of the project config
    instead of returning a literal. Absent, unreadable, malformed or empty
    config resolves to `DEFAULT_REF_NS`, so a project that never sets the key
    keeps every ref exactly where it was: no silent migration for the many
    trees already carrying `refs/grid/*` history.

    A trailing `/` is stripped on purpose: `refs/grid/t1/` and `refs/grid/t1`
    must name the same namespace, or the caller's own concatenation would mint
    `refs/grid/t1//node/...` with a doubled separator and two spellings of one
    trunk, which is the exact defect this round removes.

    The config is read from the project's ONE shared checkout
    (`locations.shared_project_root`), not from the worktree handed in
    (hypothesis:grid-old-namespace-refilled-and-forked). A linked git worktree
    carries its OWN `.agi/config.json`, which can predate the storage-trunk
    migration; reading it would resolve `DEFAULT_REF_NS` and re-mint the
    migrated-from namespace while the main checkout's config names the trunk.
    A tree that is not a linked worktree, or that has no `storage_trunk`,
    resolves `DEFAULT_REF_NS` byte-for-byte as before.
    """
    shared = locations.shared_project_root(Path(root))
    cfg = locations.load_config(shared or Path(root))
    section = cfg.get("grid")
    trunk = section.get("storage_trunk") if isinstance(section, dict) else None
    if not isinstance(trunk, str) or not trunk.strip():
        return DEFAULT_REF_NS
    return trunk.strip().rstrip("/")


def trunk_declared(root: Path) -> bool:
    """True when the shared config declares `grid.storage_trunk` at all (goal:g7.16.1.11.46.16).

    The branch-blind refusal exists for an UNDECLARED tree; a declared trunk, even the
    default spelling `refs/grid`, is a project's own statement of where its refs live,
    so the refusal is lifted for it exactly as it was for a non-default trunk."""
    shared = locations.shared_project_root(Path(root))
    section = locations.load_config(shared or Path(root)).get("grid")
    trunk = section.get("storage_trunk") if isinstance(section, dict) else None
    return isinstance(trunk, str) and bool(trunk.strip())


def legacy_namespaces_for(root: Path) -> list[str]:
    """Namespaces the shared config declares READ-ONLY (`grid.legacy_namespaces`, goal:g7.16.1.11.46.16).

    Never written, never pushed again, exempt from the post-migration refusal; `unify` merges
    them into the one namespace and `commit` holds a mint whose legacy tip is not yet in that
    mint's history. Absent, unreadable or malformed -> [] (no exemption: the refusal stands)."""
    shared = locations.shared_project_root(Path(root))
    section = locations.load_config(shared or Path(root)).get("grid")
    raw = section.get("legacy_namespaces") if isinstance(section, dict) else None
    if not isinstance(raw, list):
        return []
    return [x.strip().rstrip("/") for x in raw if isinstance(x, str) and x.strip()]


def legacy_config_problem(root: Path) -> str | None:
    """Why `grid.legacy_namespaces` is unusable, or None (goal:g7.16.1.11.46.16 R4). A cell that is
    PRESENT but not a list of namespaces under refs/grid, or that names the writer's own namespace,
    makes `commit` and `unify` refuse by name: a mis-typed cell must never read as 'no legacy
    namespace' (which would switch the hold off)."""
    shared = locations.shared_project_root(Path(root))
    section = locations.load_config(shared or Path(root)).get("grid")
    if not isinstance(section, dict) or "legacy_namespaces" not in section:
        return None
    raw = section["legacy_namespaces"]
    if not isinstance(raw, list) or not all(isinstance(x, str) and x.strip() for x in raw):
        return "grid.legacy_namespaces must be a list of namespace strings"
    names = [x.strip().rstrip("/") for x in raw]
    if any(not (n == DEFAULT_REF_NS or n.startswith(DEFAULT_REF_NS + "/")) for n in names):
        return "grid.legacy_namespaces names a namespace outside refs/grid"
    if ref_ns_for(root) in names:
        return "grid.legacy_namespaces names the writer's own namespace"
    return None


def migrated_trunk_namespaces(root: Path) -> list[str]:
    """Namespaces nested under `DEFAULT_REF_NS` that already hold refs.

    The post-migration / stale-config state the falsifier names: history lives
    at `refs/grid/<trunk>/node/<mint-id>` while the resolved namespace is the
    bare `DEFAULT_REF_NS` (the shared config lost its `storage_trunk`, or a
    linked worktree still reads its own pre-migration config). Writing there
    would re-mint the migrated-from namespace and fork a second v1 root, so
    `cmd_commit` refuses by name rather than silently forking.

    A namespace is where `node/` OR `session/` begins
    (hypothesis:grid-commit-guard-and-writer-read-one-namespace conjunct 2):
    a nested trunk holding ONLY session refs was migrated too, and skipping
    it because it carries no `/node/` let the guard pass and re-mint
    `DEFAULT_REF_NS` exactly as before.
    """
    prefix = f"{DEFAULT_REF_NS}/"
    ns: set[str] = set()
    for line in git(root, "for-each-ref", DEFAULT_REF_NS,
                    "--format=%(refname)").splitlines():
        if not line.startswith(prefix):
            continue
        found = re.sub(r"/(node|session)/.*$", "", line, count=1)
        if found != line and found != DEFAULT_REF_NS:
            ns.add(found)
    return sorted(ns - set(legacy_namespaces_for(root)) - {ORIGIN_SNAP_NS})


def push_spec_for(root: Path) -> list[str]:
    """`REF_NS` push refspecs for graph root `root` — THE one builder of them (the census C-blocks of
    goal:g7.16.1.11.13 pin it by name: any other function returning a refs/grid refspec is a NEW site).

    A LIST of two (`<ns>/node/*` and `<ns>/session/*`, `PUSH_KINDS`), not one `<ns>/*`: a `*` refspec spans
    slashes (measured, git 2.43.0: `git push <bare> 'refs/grid/*:refs/grid/*'` carried node/, origin-snap/node/
    and a legacy namespace's node/ all three), so the old one-liner pushed the private origin mirror and the
    read-only legacy namespaces too. Callers pass them as separate arguments (`git push origin *specs`).

    `crons.py` imports this rather than re-hardcoding the namespace (goal:g14.14.7
    item b): the second spelling in the cron template was the gap, and a
    function is what makes `apply` and the cron line agree by construction.
    """
    ns = ref_ns_for(root)
    return [f"{ns}/{k}/*:{ns}/{k}/*" for k in PUSH_KINDS]


# The ONE declared home of the grid push defaults: a project that has not set
# `grid.push_batch_limit` in its config.json gets the value declared here, and
# the missing cell is named once in the log instead of killing the cron path
# (hypothesis:grid-sync-survives-a-project-without-push-batch-limit).
GRID_PUSH_DEFAULTS = {"push_batch_limit": 200}


def push_batch_limit(root: Path) -> int:
    """Maximum changed grid refs in one host validation request — a config
    cell, not a literal default (PASS 5/6 residue,
    hypothesis:grid-push-batch-limit-is-a-config-cell). A project that has not
    set the cell is named once and falls back to `GRID_PUSH_DEFAULTS`, so the
    grid_sync cron keeps versioning every project on the box."""
    cfg = locations.load_config(locations.shared_project_root(Path(root)) or Path(root))
    value = (cfg.get("grid") or {}).get("push_batch_limit")
    if value is None:
        value = GRID_PUSH_DEFAULTS["push_batch_limit"]
        print(
            f"grid: config cell grid.push_batch_limit is absent -- using the "
            f"declared default {value} (set it in config.json to override)")
    return max(1, int(value))


def push_batches(root: Path) -> list[list[str]]:
    """Exact post-split refspec batches for changed local tips; never a wildcard."""
    ns = ref_ns_for(root)
    # node/ and session/ only: under the default namespace a bare `refs/grid` would also list the
    # READ-ONLY legacy namespaces nested beneath it (goal:g7.16.1.11.46.16), which are never pushed again
    kinds = [f"{ns}/node", f"{ns}/session"]
    local = [line.split() for line in git(
        root, "for-each-ref", *kinds, "--format=%(refname) %(objectname)").splitlines()]
    remote = {parts[1]: parts[0] for parts in (
        line.split() for line in git(
            root, "ls-remote", "--refs", "origin", *[f"{k}/*" for k in kinds]).splitlines())}
    cfg = locations.load_config(locations.shared_project_root(Path(root)) or Path(root))
    grid_cfg = cfg.get("grid") or {}
    split_epoch = int(grid_cfg.get("push_split_epoch", 0))
    minimum = int(grid_cfg.get("push_min_season", 0))
    changed = []
    for ref, oid in local:
        if remote.get(ref) == oid:
            continue
        is_root = False
        if split_epoch or minimum:
            meta = git(root, "show", "-s", "--format=%ct %P", oid).split()
            is_root = len(meta) < 2
            if split_epoch and is_root and int(meta[0]) < split_epoch:
                # The seed pass created unrelated v1 roots; descendants remain.
                continue
        if minimum and is_root:
            season = re.search(r"^season:\s*(\d+)\s*$", git(root, "show", f"{oid}:node.md"), re.M)
            if season and int(season.group(1)) < minimum:
                continue
        changed.append(f"{ref}:{ref}")
    size = push_batch_limit(root)
    return [changed[i:i + size] for i in range(0, len(changed), size)]


RETIRED_LINE = "grid: retired (cron:crons grid_sync.enabled false); nothing written"


def grid_retired(root: Path) -> bool:
    """True only when `crons.py` reads `cadences.grid_sync.enabled` as False.

    goal:g7.16.1.11.13 E2b0: once off, `commit` and `push-changed` write nothing
    NEW (a retired `commit` returns rc 0 printing RETIRED_LINE, so rotate reports
    'grid committed'). The node is read by `crons.load_crons_node` (a lazy
    import: crons imports grid) from the project's SHARED checkout like
    `ref_ns_for`. `crons_live: false`, a `box:` gate or an absent key also drop
    the job but leave the gate OPEN (fail-safe); a node crons.py cannot validate
    (any error, no file, no key, no yaml) is NOT retired, and a CronsError (an
    invalid node) prints ONE stderr line per call, `grid: crons node invalid
    (<text>); grid NOT retired`; `False`, `no`, `off`
    ARE retired. Retired, rotate._push's `refs/grid/*` push and `grid.py sync`
    (the operator's verb, ungated by design) can only republish tips that
    already exist locally: a non-force push, idempotent, nothing new written
    (whether root pushes refs/grid at all is E2d, belam's). The `cron_lines` snap
    line (`commit --all && git push -q origin PUSH_SPECS`, installed only by
    `grid.py cron install`) is EXEMPT with `sync`: it never calls the push verbs
    gated here, and a retired `commit --all` exits 0, so its `&&` push
    republishes pre-existing tips.
    """
    try:
        import crons
        shared = Path(locations.shared_project_root(Path(root)) or root)
        if not (shared / crons.CRONS_NODE_REL).is_file():
            return False    # no crons node at all (a project without one): SILENT; an INVALID node is still named below
        return crons.load_crons_node(shared)["jobs"]["grid_sync"]["enabled"] is False
    except Exception as exc:
        if type(exc).__name__ == "CronsError":    # an invalid node (the old mirror_towns flag, a bad cell) is NAMED, never silent
            print(f"grid: crons node invalid ({exc}); grid NOT retired", file=sys.stderr)
        return False


PUSH_NON_FF = "[rejected] (non-fast-forward)"
PUSH_GENERIC_ERROR = "error: failed to push some refs"


PUSH_STATUS_FLAGS = " *+-!="


def read_push_porcelain(res: "subprocess.CompletedProcess[str]", batch: list[str]) -> tuple[list[str], str | None]:
    """Read one batch pushed with `--porcelain`: (the dst refs NAMED as non-fast-forward rejections, unread).

    `unread` is None only when every failure is a `!<TAB><src>:<dst><TAB>[rejected] (non-fast-forward)`
    line: that ref stays where the remote has it and the rest of the batch landed (a push is per ref
    unless --atomic). Anything else is unread, with the first line that says why: a non-zero rc with no
    `!` line (transport, auth, a missing remote), a `!` line with another summary (`[remote rejected]`,
    `(fetch first)`: the remote holds a tip this repo never fetched), or an `error:`/`fatal:` on stderr
    other than git's own `error: failed to push some refs` (goal:g7.16.1.11.46.16, alive 19:09:47Z).
    A batch is landed only when EVERY `<src>:<dst>` of `batch` has its own status line: git prints one
    per ref, `=` for one already up to date (measured, git 2.43), so a missing line (a silent rc 0, a
    git on PATH that printed nothing) is unread, never counted as landed (sp, alive 20:34:49Z)."""
    named, other, seen = [], [], set()
    for line in res.stdout.splitlines():
        parts = line.split("\t")
        if len(parts) >= 3 and len(parts[0]) == 1 and parts[0] in PUSH_STATUS_FLAGS:
            seen.add(parts[1].rsplit(":", 1)[-1])
        if len(parts) >= 3 and parts[0] == "!":
            if parts[2].strip() == PUSH_NON_FF:
                named.append(parts[1].rsplit(":", 1)[-1])
            else:
                other.append(" ".join(p.strip() for p in parts))
    errors = [l.strip() for l in res.stderr.splitlines()
              if l.startswith(("error:", "fatal:")) and not l.startswith(PUSH_GENERIC_ERROR)]
    if errors:
        return named, errors[0]
    if other:
        return named, other[0]
    if res.returncode != 0 and not named:
        first = next((l.strip() for l in res.stderr.splitlines() if l.strip()), "")
        return named, first or f"the push exited {res.returncode} with no ref status line"
    missing = [dst for dst in (spec.rsplit(":", 1)[-1] for spec in batch) if dst not in seen]
    if missing:
        return named, (f"no ref status line for {len(missing)} of {len(batch)} ref(s), first {missing[0]} "
                       f"(the push exited {res.returncode})")
    return named, None


def push_ref_names(root: Path, refs: list[str]) -> str:
    """The names rejections are reported by: the mint for `<ns>/node/<mint>`, else the whole ref."""
    prefix = f"{ref_ns_for(root)}/node/"
    return " ".join(r[len(prefix):] if r.startswith(prefix) else r for r in refs)


def cmd_push_changed(root: Path) -> int:
    """Advance only changed local grid tips, batch by batch: a NAMED non-fast-forward rejection is
    counted and the next batch still runs; any other failure stops at that batch, unread. Never --force.
    rc 0 only when every changed ref reached the remote; the last line is always a `grid push:` line."""
    if grid_retired(root):
        print(RETIRED_LINE)
        return 0
    ensure_repo(root)
    batches = push_batches(root)
    rejected: list[str] = []
    for number, batch in enumerate(batches, 1):
        named, unread = read_push_porcelain(git_try(root, "push", "--porcelain", "origin", *batch), batch)
        rejected.extend(named)    # counted by name; the remote keeps its tip and the next batch still runs
        if unread is not None:
            if rejected:
                print(f"grid push: rejected {len(rejected)}: {push_ref_names(root, rejected)}")
            print(f"grid push: unread at batch {number}/{len(batches)}: {unread}")
            return 1
        note = f", {len(named)} rejected" if named else ""
        print(f"grid push batch {number}/{len(batches)}: {len(batch)} ref(s){note}")
    print(f"grid push: {sum(map(len, batches))} changed ref(s) in {len(batches)} batch(es)")
    if rejected:
        print(f"grid push: rejected {len(rejected)}: {push_ref_names(root, rejected)}")
        return 1
    return 0


def fetch_specs_for(root: Path) -> list[str]:
    """`REF_NS` fetch refspecs for graph root `root`: node/ and session/ ONLY, and NEVER forced
    (goal:g7.16.1.11.46.16 R3). The old `+<ns>/*:<ns>/*` would, after `unify`, let a plain fetch from
    a remote still at the frozen tips move a merged tip BACK, and would also reach the read-only legacy
    namespaces nested under `refs/grid`; a non-forced spec refuses a non-fast-forward instead."""
    ns = ref_ns_for(root)
    return [f"{ns}/node/*:{ns}/node/*", f"{ns}/session/*:{ns}/session/*"]


def fetch_spec_for(root: Path) -> str:
    """The node/ fetch refspec (see `fetch_specs_for`, which `cmd_init` configures in full)."""
    return fetch_specs_for(root)[0]


def apply_storage_trunk(root: Path) -> str:
    """Resolve `grid.storage_trunk` for `root` into this module's globals.

    `REF_NS`, `FETCH_SPEC` and `PUSH_SPECS` are the values every other function
    here derives from, so one call makes all of them config-aware with no
    further edits. `main()` calls it once, before dispatch; a test or a caller
    holding a configured tree calls it directly. Returns the resolved
    namespace so a caller can report it without re-reading the config.
    """
    global REF_NS, FETCH_SPEC, PUSH_SPECS
    global FETCH_SPECS, LEGACY_NS
    REF_NS = ref_ns_for(root)
    LEGACY_NS = [n for n in legacy_namespaces_for(root) if n != REF_NS]
    FETCH_SPECS = fetch_specs_for(root)
    FETCH_SPEC = FETCH_SPECS[0]
    PUSH_SPECS = push_spec_for(root)
    return REF_NS


def find_project_root(start: Path | None = None) -> Path:
    """The GRAPH root — `<repo>/.agi` under G11 — via `locations` (**goal:g11.1**).

    This was its own ancestor walk, looking only for a bare config-marker name
    in each parent. That has no phase 0, so it cannot see a `<d>/.agi/` graph
    directory, and under the goal:g11 layout it walked the whole way to `/` and
    exited. The grid is where every payload byte and every node version lives,
    so a `grid.py` that cannot find the project is the most expensive form this
    residual could take: `commit --all` stops recording history and says so only
    on stderr, which in a cron is nowhere.

    Delegates to `project_root_from_env`, not to `find_project_root`, so an
    explicit `$AGI_TREE_PROJECT_ROOT` wins here exactly as it does for every
    other entry point. `grid.py` disagreeing with its callers about which
    project it is versioning is the one disagreement the grid cannot survive.

    Kept as a wrapper rather than deleted: `grid.py` calls this in a dozen
    places and the `sys.exit`-on-failure contract is what those callers expect.
    """
    root = locations.project_root_from_env(start)
    if root is None:
        cur = (start or Path.cwd()).resolve()
        sys.exit(
            f"ERR: no agi project found from {cur} — looked for "
            f"{locations.GRAPH_DIR_NAME}/ or {locations.CONFIG_NAMES[0]} "
            f"walking up, then <dir>/*-tree/ below"
        )
    return root


# --- the two roots, and why every git call takes the second one (goal:g11) ---
#
# `grid.py` is handed ONE root by its callers — the graph root — and has two
# different jobs for it:
#
#     graph root   `<repo>/.agi`   node FILES live here     (`iter_node_files`)
#     repo root    `<repo>`        grid REFS live here      (every `git` call)
#
# Before goal:g11 those were the same directory, so handing the graph root to
# `git -C` was invisibly correct. It is not any more, and what it produces is a
# **silent wrong answer, not an error**: `git -C <repo>/.agi` sets git's
# *prefix* to `.agi/`, and every cwd-scoped subcommand then resolves paths
# under that prefix — but a grid commit's tree carries `node.md` at ITS OWN
# root, under no prefix at all. Two measured consequences, both of which
# reported success:
#
#   - `ls-tree` matched nothing, so `read_tree` returned `[]` and all 809 nodes
#     read as CHANGED while being byte-identical (`cmd_status`).
#   - `diff <ref>~1 <ref> -- node.md` printed an empty diff and exited 0 for
#     `goal:g11.1`, a node with three real versions — 3696 bytes of diff when
#     the same command runs from the repo root.
#
# `ref_tip`, `rev-list` and `commit-tree` take no pathspec and were correct
# throughout, which is exactly what made the whole thing look fine.
#
# Every git invocation in this file goes through `repo_root()` below. The
# pathspec spellings that are prefix-proof (`ls-tree --full-tree`,
# `diff -- ':(top)node.md'`) are kept as belt-and-braces — they are the right
# way to say "this is a tree-root path" no matter where git is run from — but
# they are no longer what holds this up. `test_status_agrees_from_repo_root_
# and_graph_dir` and friends pin the root split on its own.


def repo_root(root: Path) -> Path:
    """The git repo enclosing graph root `root` — where `refs/grid/*` lives.

    Straight delegation to `locations.repo_root`, which is the identity under
    the legacy layout (graph root == repo root) and `root.parent` under G11.
    That is what lets every call site ask unconditionally instead of branching
    on layout, and it is why routing `git()` through here is a no-op for every
    pre-G11 project and every test fixture built as a bare tree.
    """
    return locations.repo_root(root)


def git(root: Path, *args: str, input_text: str | None = None, check: bool = True) -> str:
    """Run git for the repo enclosing graph root `root`.

    `root` is the GRAPH root as every caller in this file holds it; the `-C`
    handed to git is the REPO root (see the block comment above). Callers pass
    the root they have and never have to remember the distinction.
    """
    res = subprocess.run(
        ["git", *GIT_IDENT, "-C", str(repo_root(root)), *args],
        capture_output=True, text=True, input=input_text,
    )
    if check and res.returncode != 0:
        sys.exit(f"ERR: git {' '.join(args)}: {res.stderr.strip()}")
    return res.stdout.strip()


def git_try(root: Path, *args: str, input_text: str | None = None) -> "subprocess.CompletedProcess[str]":
    """`git` that never exits: the caller reads returncode and stderr (goal:g4.13.1)."""
    return subprocess.run(
        ["git", *GIT_IDENT, "-C", str(repo_root(root)), *args],
        capture_output=True, text=True, input=input_text,
    )


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


def parse_mint_id(path: Path) -> str | None:
    """The node's permanent id, or None if it has not been backfilled yet
    (see `bin/backfill-mint-ids.py`). Never guessed, never derived — a
    missing mint_id here means exactly that: absent."""
    m = MINT_ID_RE.search(path.read_text(encoding="utf-8"))
    return m.group(1) if m else None


def parse_payload_ref(path: Path) -> str | None:
    """The engine-repo-relative path this node's payload belongs at, or None
    for a node that carries no payload (every non-build node). Never guessed
    from the filename — absent means absent."""
    m = PAYLOAD_REF_RE.search(path.read_text(encoding="utf-8"))
    if not m:
        return None
    ref = m.group(1).strip()
    return ref or None


def parse_location(path: Path) -> str | None:
    """The node's `location:` field — the payload base it was recorded under (
    `locations.DEFAULT_PAYLOAD_LOCATION` by default, or a key the project
    config declares under `locations:`), or None when absent.

    Absent and an explicit `source_root` are the same for resolving purposes —
    both mean the default base — so parse_location returns None for a node with
    no `location:` line, and the caller falls back to the default path.
    """
    m = LOCATION_RE.search(path.read_text(encoding="utf-8"))
    if not m:
        return None
    v = m.group(1).strip()
    return v or None


def default_engine_root() -> Path:
    """The engine tree a payload is read from when the graph repo has no
    staged copy: this script's own repo, `<engine>/extensions/agi/bin/grid.py`
    -> `<engine>`. Same derivation `level3.py` uses for `DEFAULT_ENGINE_ROOT`.
    """
    return Path(__file__).resolve().parents[3]


def resolve_payload(root: Path, payload_ref: str,
                    engine_root: Path,
                    location: str | None = None) -> tuple[Path, str] | None:
    """Where a node's payload bytes are read from, and which source won.

    Two regimes, split on the node's `location:` field:

    **Default (`location` is None or `source_root`)** — this project's own
    layout (graph root == engine tree), whichever else. Priority, and the
    order *is* goal:g6.1's arrow:

      1. `<project>/payloads/<payload_ref>` — the graph repo's own staged
         checkout (`grid.py checkout`). This is the copy an author edits, and
         its presence is what makes the graph the source: the engine tree is
         never consulted for a node that has one.
      2. `<engine>/<payload_ref>` — the live engine tree. The bootstrap path,
         and what a node still uses until it has been checked out. Committing
         from here is how a node's payload history starts without anyone
         having to stage all 180 files first.

    **Non-default (`location` names a key declared under the project config's
    `locations:` map)** — resolve through the SAME location-aware mechanism
    `node_writer.ensure_payload`/`replace_payload` use, so the grid agrees
    with the node's `link_ref` (written when it was minted) about where the payload
    lives (`locations.resolve_payload_path`). The staged/engine pair does not
    apply here: that pairing only ever described the default tree.

    Returns `(path, "staged" | "engine" | <location>)`, or None when nothing
    exists at the resolved location — the caller reports that rather than
    committing a node whose payload vanished.
    """
    loc = (location or "").strip()
    if loc and loc != "source_root":
        located = locations.resolve_payload_path(root, payload_ref, loc)
        if located.is_symlink() or located.exists():
            return located, loc
        return None
    staged = root / PAYLOAD_DIR / payload_ref
    if staged.is_symlink() or staged.exists():
        return staged, "staged"
    live = engine_root / payload_ref
    if live.is_symlink() or live.exists():
        return live, "engine"
    return None


def parse_parents(path: Path) -> list[str]:
    """Best-effort, stdlib-only parse of a node's `parents:` field, covering
    the shapes `write_frontmatter` actually produces (a multi-line `- item`
    list) plus two shapes seen on hand-written nodes (an inline `[a, b]`
    list, a bare single scalar). Anything else yields `[]` rather than a
    guess — this only feeds the commit-message trailer (goal:g2.7), which is
    additive provenance, never a value a caller should treat as load-bearing
    for correctness.
    """
    text = path.read_text(encoding="utf-8")
    fm_end = text.find("\n---", 3)
    fm_text = text[:fm_end] if fm_end != -1 else text

    m = PARENTS_RE.search(fm_text)
    if m:
        items = []
        for line in fm_text[m.end():].splitlines():
            if not line.strip():
                continue
            item_m = re.match(r'^\s*-\s*(.+?)\s*$', line)
            if item_m:
                items.append(item_m.group(1).strip("\"'"))
            else:
                break  # end of this list block
        if items:
            return items

    m = PARENTS_INLINE_RE.search(fm_text)
    if m:
        return [x.strip().strip("\"'") for x in m.group(1).split(",") if x.strip()]

    m = PARENTS_SCALAR_RE.search(fm_text)
    if m:
        val = m.group(1).strip().strip("\"'")
        if val and val not in ("[]", "null", "~"):
            return [val]

    return []


def mint_node_ref(mint_id: str) -> str:
    """The permanent ref a node's history lives under from here forward.

    Runs `mint_id` through `sanitize()` anyway even though the format
    (32 lowercase hex chars — see `graph_core.identity.mint_permanent_id`)
    already needs no escaping: defense in depth if the mint id format ever
    changes, at zero behavioural cost today (`sanitize()` is the identity
    function on this alphabet).
    """
    return f"{REF_NS}/node/{sanitize(mint_id)}"


class MissingMintIdError(RuntimeError):
    """Raised by `write_ref_for` when a node has no `mint_id`. Never used to
    select a fallback ref -- writes must not go to the id-keyed ref just
    because the permanent key is absent (goal:g2.5); see `cmd_commit`, which
    catches this per-node so one un-migrated node cannot block `--all` from
    committing and pushing every other node -- the exact failure class the
    pre-fix `sanitize()` colon bug produced (see module docstring / `commit
    --all` history)."""


def write_ref_for(path: Path, node_id: str) -> str:
    """The ref a version of `path` (known to carry `node_id`) must be
    committed to. Always the mint-id ref -- writes never fall back to the
    legacy node-id ref, because that ref is keyed on the mutable address and
    would fork history the moment the node is retagged (goal:g2.5).

    Raises `MissingMintIdError`, naming both the node id and the file, if
    `path` has no `mint_id` yet. Run `bin/backfill-mint-ids.py --write` to
    fix that once, corpus-wide.
    """
    mint_id = parse_mint_id(path)
    if not mint_id:
        raise MissingMintIdError(
            f"{node_id} ({path}) has no mint_id -- refusing to write a "
            "node-id-keyed ref for it. Run backfill-mint-ids.py --write first."
        )
    return mint_node_ref(mint_id)


def build_id_index(root: Path) -> dict[str, Path]:
    """`node_id -> path` for every node file, built once per command
    invocation so per-node lookups (parent mint-id resolution, read
    fallback) do not rescan the whole corpus per call."""
    index: dict[str, Path] = {}
    for p in iter_node_files(root):
        nid = parse_node_id(p)
        if nid is not None:
            index[nid] = p
    return index


def build_parent_mint_trailer(path: Path, id_index: dict[str, Path], resolve=None) -> str | None:
    """Commit-message body for goal:g2.7: one `Parent-Mint-Id: <mint-id> <parent-node-id>`
    line per entry in `path`'s `parents:`, so a renderer can traverse disk
    nodes and grid commits as one hypergraph without a separate edge store —
    the edge is already written into the history. Documented format:

        Parent-Mint-Id: <32-hex-char mint id, or the literal UNRESOLVED> <parent node id>

    `UNRESOLVED` (never a fabricated id) means the parent could not be found
    on disk, or was found but has no `mint_id` of its own yet.

    Returns None (no body to add) if the node has no parents at all.
    `resolve` = the caller's ONE links.address_resolver: a parent written as a
    mint id is named by its address, exactly as its address twin
    (hypothesis:grid-parent-trailer-reads-a-mint-parent-through-the-resolver).
    """
    parents = [(resolve and resolve(p)) or p for p in parse_parents(path)]
    if not parents:
        return None
    lines = []
    for parent_id in parents:
        parent_path = id_index.get(parent_id)
        parent_mint = parse_mint_id(parent_path) if parent_path is not None else None
        token = parent_mint if parent_mint else "UNRESOLVED"
        lines.append(f"Parent-Mint-Id: {token} {parent_id}")
    return "\n".join(lines)


def ref_tip(root: Path, ref: str) -> str | None:
    """Tip sha of `ref`, or None. Raw `subprocess.run` rather than `git()`
    because a missing ref must be None, not `sys.exit` — but the `-C` still
    goes through `repo_root` like every other git call in this file."""
    res = subprocess.run(
        ["git", "-C", str(repo_root(root)), "rev-parse", "-q", "--verify", ref],
        capture_output=True, text=True,
    )
    return res.stdout.strip() or None


# --- git object <-> filesystem, mode- and symlink-correct (goal:s9) ----------
#
# Every one of these is what `git add` does internally, built from the four
# plumbing primitives this file already calls. The pre-S9 code hashed
# `path.resolve()` and hardcoded `100644`, which silently substituted a
# symlink's *target bytes* for its link text and downgraded every executable
# payload — measured, both directions, by `exp:grid-payload-roundtrip`.


def git_mode(path: Path) -> str:
    """The git tree mode for `path`, read from `os.lstat()`.

    `lstat`, never `stat`: the mode of a symlink is the property being
    recorded, so dereferencing first would report the target's mode and lose
    the only bit that matters.
    """
    st = os.lstat(path)
    if stat.S_ISLNK(st.st_mode):
        return GIT_MODE_SYMLINK
    if st.st_mode & 0o111:
        return GIT_MODE_EXEC
    return GIT_MODE_REGULAR


def hash_path(root: Path, path: Path, *, write: bool = True) -> tuple[str, str]:
    """`(mode, blob_sha)` for one path, the way `git add` computes them.

    For a symlink the blob content is the **link text** (`os.readlink`), fed
    through `hash-object --stdin` — not the file it points at. `os.path.abspath`
    normalises `..` lexically without resolving symlinks, so the final component
    survives; `Path.resolve()` would not, and that is exactly the pre-S9 bug.
    """
    mode = git_mode(path)
    args = ["hash-object"] + (["-w"] if write else [])
    if mode == GIT_MODE_SYMLINK:
        return mode, git(root, *args, "--stdin", input_text=os.readlink(path))
    return mode, git(root, *args, "--", os.path.abspath(path))


def read_tree_entry(root: Path, rev: str, name: str) -> tuple[str, bytes] | None:
    """`(mode, raw bytes)` for `name` in `rev`'s tree, or None if absent.

    Bytes, not text: a payload may be any file in the engine repo, and
    decoding one to hand it back would make the round trip encoding-dependent.
    """
    # `--full-tree` is belt-and-braces since `git()` moved to `repo_root`: it
    # pins the pathspec to the tree's own root regardless of git's prefix, which
    # is the right thing to say about a grid tree either way. It is no longer
    # what makes this correct — see the two-roots block comment.
    line = git(root, "ls-tree", "--full-tree", rev, "--", name, check=False)
    if not line:
        return None
    mode = line.split(maxsplit=1)[0]
    res = subprocess.run(
        ["git", "-C", str(repo_root(root)), "cat-file", "blob", f"{rev}:{name}"],
        capture_output=True,
    )
    if res.returncode != 0:
        return None
    return mode, res.stdout


def materialize_entry(dst: Path, mode: str, data: bytes) -> None:
    """Write one grid tree entry back to disk — the exact inverse of
    `hash_path`, including the mode. A `120000` entry becomes a real symlink
    whose target is the blob's text.

    Unlinks an existing `dst` first rather than opening it for write, because
    writing *through* a symlink would clobber whatever it points at.
    """
    dst.parent.mkdir(parents=True, exist_ok=True)
    if dst.is_symlink() or dst.exists():
        dst.unlink()
    if mode == GIT_MODE_SYMLINK:
        os.symlink(data.decode("utf-8"), dst)
        return
    dst.write_bytes(data)
    os.chmod(dst, 0o755 if mode == GIT_MODE_EXEC else 0o644)


def tree_entries(root: Path, path: Path, payload: Path | None,
                 *, write: bool) -> list[tuple[str, str, str]]:
    """`(name, mode, blob)` for one node version, sorted by name.

    One entry (`node.md`) when the node has no payload, two when it does. The
    node file's own mode is read rather than asserted: node files are neither
    symlinks nor executable today, and if one ever is, recording what is
    actually there beats writing down what we assumed.

    `write=False` computes the same shas without adding objects to the store,
    which is what lets `status` compare a would-be version against the ref tip
    without the side effect of writing one.
    """
    entries = [(NODE_ENTRY, *hash_path(root, path, write=write))]
    if payload is not None:
        entries.append((PAYLOAD_ENTRY, *hash_path(root, payload, write=write)))
    return sorted(entries)


def build_tree(root: Path, path: Path, payload: Path | None) -> str:
    """Write the tree object for one node version and return its sha."""
    lines = "".join(f"{mode} blob {blob}\t{name}\n"
                    for name, mode, blob in tree_entries(root, path, payload, write=True))
    return git(root, "mktree", input_text=lines)


def read_tree(root: Path, rev: str) -> list[tuple[str, str, str]]:
    """`(name, mode, blob)` for every entry in `rev`'s tree, sorted by name —
    the read-side counterpart of `tree_entries`, so the two are directly
    comparable without materialising anything."""
    out = git(root, "ls-tree", "--full-tree", rev, check=False)  # belt-and-braces; see read_tree_entry
    rows = []
    for line in out.splitlines():
        meta, _, name = line.partition("\t")
        mode, _kind, blob = meta.split()
        rows.append((name, mode, blob))
    return sorted(rows)


def ensure_repo(root: Path) -> None:
    """Fail loudly unless graph root `root` sits inside a git repo.

    Checks — and names, in the error — the REPO root, not the graph root: under
    G11 `<repo>/.agi` is never itself a repo, and `git init`-ing it because an
    error message pointed there would create a nested repo whose object store
    is not the one holding `refs/grid/*`.
    """
    repo = repo_root(root)
    if subprocess.run(["git", "-C", str(repo), "rev-parse", "--git-dir"],
                      capture_output=True).returncode != 0:
        sys.exit(f"ERR: {repo} is not a git repo — the grid bakes into the "
                 "project repo; `git init` it first")


def cmd_init(root: Path) -> None:
    ensure_repo(root)
    remotes = git(root, "remote").splitlines()
    if "origin" in remotes:
        specs = git(root, "config", "--get-all", "remote.origin.fetch",
                    check=False).splitlines()
        added = [x for x in FETCH_SPECS if x not in specs]
        for spec in added:
            git(root, "config", "--add", "remote.origin.fetch", spec)
            print(f"grid: added fetch refspec {spec} to origin")
        if not added:
            print("grid: origin refspec already configured")
    else:
        print("grid: no origin remote yet — refs work locally; run "
              "`grid.py sync <remote-url>` or `init` again after adding one")
    count = len(git(root, "for-each-ref", REF_NS,
                    "--format=%(refname)").splitlines())
    print(f"grid ready: {count} existing version ref(s) under {REF_NS}/")


#: refs whose update-ref failed for a reason other than a CAS miss (goal:g4.13.1 N1):
#: the run goes on, then `cmd_commit` exits 1 after its summary line.
UPDATE_REF_FAILURES: list[str] = []


LEGACY_HELD: list[str] = []
#: refs whose NEW mint was refused because another mint already carries the same `id:` (the double mint).
DOUBLE_MINT_REFUSED: list[str] = []
#: mints whose ref this run created (they carry their id from then on); the per-run view cache; reset per run.
MINTED_THIS_RUN: dict[str, str] = {}
_DM_CACHE: dict | None = None
#: {legacy ref: tip}, read ONCE per run by one `for-each-ref` whose rc is checked (R4): an absent ref
#: and a failed rev-parse can no longer look alike. None = not loaded yet.
LEGACY_TIPS: dict[str, str] | None = None


def legacy_tips(root: Path) -> dict[str, str]:
    global LEGACY_TIPS
    if LEGACY_TIPS is None:
        tips: dict[str, str] = {}
        for ns in LEGACY_NS:
            res = git_try(root, "for-each-ref", f"{ns}/node", "--format=%(refname) %(objectname)")
            if res.returncode != 0:
                sys.exit(f"grid: unread (for-each-ref {ns}/node failed: {res.stderr.strip()[:120]}); nothing written")
            for line in res.stdout.splitlines():
                ref, _, oid = line.partition(" ")
                tips[ref] = oid
        LEGACY_TIPS = tips
    return LEGACY_TIPS


def legacy_unmerged(root: Path, ref: str, tip: str | None) -> str | None:
    """The read-only legacy ref of the same mint whose tip is NOT in `ref`'s history, or None.

    goal:g7.16.1.11.46.16 G1a-W: once the writer is pointed at the one namespace, a mint whose live
    history still sits in a legacy namespace must be unified FIRST (`cmd_unify`); writing before that
    would fork a second line from the frozen tip. Only `<ns>/node/<mint>` refs are held."""
    if not LEGACY_NS or not ref.startswith(f"{REF_NS}/node/"):
        return None
    rest = ref[len(REF_NS) + 1:]
    for ns in LEGACY_NS:
        lref = f"{ns}/{rest}"
        ltip = legacy_tips(root).get(lref)
        if ltip is None:
            continue
        if tip and git_try(root, "merge-base", "--is-ancestor", ltip, tip).returncode == 0:
            continue
        return lref
    return None


def _dm_view(root: Path) -> dict:
    """The per-run read the double-mint refusal needs, built ONCE and only when a new mint is about to be created:
    `files` {mint: {ids its FILE names}} over the commit's own view (every node file under nodes/, deprecated/ too),
    `refs` {mint: tip} for every mint with a ref in the one namespace, and `tip_ids` {mint: the id its ref TIP names}
    for the refs whose mint has NO file in the view (ghosts, never-landed): the only mints read from a tip."""
    global _DM_CACHE
    if _DM_CACHE is not None:
        return _DM_CACHE
    files: dict[str, set[str]] = {}
    for p in iter_node_files(root):
        try:
            text = p.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        mi, ii = MINT_ID_RE.search(text), ID_RE.search(text)
        if mi and ii:
            files.setdefault(mi.group(1), set()).add(ii.group(1))
    res = git_try(root, "for-each-ref", f"{REF_NS}/node", "--format=%(objectname) %(refname)")
    if res.returncode != 0:
        sys.exit(f"grid: unread (for-each-ref {REF_NS}/node failed: {res.stderr.strip()[:120]}); nothing written")
    refs = {x.split()[1][len(REF_NS) + 6:]: x.split()[0] for x in res.stdout.splitlines() if len(x.split()) == 2}
    loose = {m: t for m, t in refs.items() if m not in files}
    tip_ids: dict[str, str] = {}
    if loose:
        out = subprocess.run(["git", "-C", str(repo_root(root)), "cat-file", "--batch"],
                             input="".join(f"{t}:{NODE_ENTRY}\n" for t in loose.values()).encode(), capture_output=True)
        if out.returncode != 0:
            sys.exit("grid: unread (cat-file over the tips of the mints with no file); nothing written")
        pos = 0
        for m in loose:
            nl = out.stdout.find(b"\n", pos)
            head = out.stdout[pos:nl].split() if nl >= 0 else []
            if len(head) != 3 or head[1] != b"blob":
                pos = nl + 1 if nl >= 0 else len(out.stdout)
                continue
            size = int(head[2])
            body = out.stdout[nl + 1:nl + 1 + size].decode("utf-8", "replace")
            pos = nl + 1 + size + 1
            ii = ID_RE.search(body)
            if ii:
                tip_ids[m] = ii.group(1)
    _DM_CACHE = {"files": files, "refs": refs, "tip_ids": tip_ids}
    return _DM_CACHE


def double_mint_holder(root: Path, mint: str, node_id: str) -> tuple[str, str] | None:
    """goal:g7.16.1.11.46.16 (the leaf of the census-orphans decision, alive 07:42:38Z 10-26): when a NEW `<ns>/node/<mint>`
    ref is about to be created, the OTHER mint that already carries `node_id`, as `(mint, where)`, else None.
    Where another mint's id is READ: from its FILE in the commit's own view (so a renumber that lands `g7.1 (M1) -> g7.2`
    and `a NEW g7.1 (M2)` in one commit never refuses M2, whatever order the files are processed in); from its ref TIP
    only for a mint with no file in that view. A mint carries its id only once it HAS a ref (or this run created it), so of
    two new files with one id the first processed is minted and the second is refused."""
    v = _dm_view(root)
    for m in sorted(v["refs"].keys() | MINTED_THIS_RUN.keys()):
        if m == mint:
            continue
        if m in v["files"]:
            if node_id in v["files"][m]:
                return m, "its node file"
        elif v["tip_ids"].get(m, MINTED_THIS_RUN.get(m)) == node_id:
            return m, "its ref tip (no node file)"
    return None


def commit_file(root: Path, path: Path, ref: str, msg_prefix: str,
                *, trailer: str | None = None,
                payload: Path | None = None) -> str | None:
    """Snapshot one node file — and, under goal:g6.3, its payload — onto `ref`.
    Returns the new version tag or None if nothing changed.

    `trailer` (goal:g2.7, `build_parent_mint_trailer`), if given, becomes
    the commit message BODY: a blank line, then the trailer lines. The
    SUBJECT line stays exactly `f"{msg_prefix}v{n} {node_id}"`, unchanged
    from before this existed — every existing reader uses `--format=%s`,
    which only ever sees the subject, so adding a body is additive and
    `trailer=None` (the default) reproduces the old single-line message
    byte-for-byte.

    `payload`, if given, is committed alongside the node file as the
    `payload` tree entry with its real mode (goal:g6.3, `build_tree`). The
    unchanged-check compares the **whole tree**, not just `node.md`, so a
    payload-only edit is a real version — comparing `node.md` alone would
    have made every payload edit invisible to history, which is the whole
    thing this goal exists to record.
    """
    node_id = parse_node_id(path)
    if node_id is None:
        print(f"skip (no id frontmatter): {path}", file=sys.stderr)
        return None
    tree = build_tree(root, path, payload)
    tip = ref_tip(root, ref)
    held = legacy_unmerged(root, ref, tip)
    if held:    # goal:g7.16.1.11.46.16: a version written now would fork from the live history
        print(f"hold (the read-only {held} is not in this ref's history; "
              f"`grid.py unify --write` first): {ref}", file=sys.stderr)
        LEGACY_HELD.append(ref)
        return None
    mint = parse_mint_id(path)
    if tip is None and mint and ref == mint_node_ref(mint):    # a MINT ref only: the legacy node-id-keyed refs are not mints
        other = double_mint_holder(root, mint, node_id)
        if other:    # a second mint for an id that is taken: the file is left for review, nothing is written
            print(f"refuse (double mint: {node_id} is already carried by mint {other[0]} ({other[1]}); "
                  f"this file's mint is {mint}; the file is left for review): {path}", file=sys.stderr)
            DOUBLE_MINT_REFUSED.append(ref)
            return None
    if tip:
        # goal:g4.13.1: carry a collapse's nest/ forward (unedited = unchanged), but only
        # a non-empty tree of trees; anything else skips THIS node and the run goes on
        er = git_try(root, "ls-tree", tip, "--", "nest")  # a failing read is a skip, never "no nest"
        ent = er.stdout.strip()
        built = None
        if er.returncode == 0 and ent:
            head = ent.split("\t")[0].split()
            kids = git_try(root, "ls-tree", head[2]) if head[:2] == ["040000", "tree"] else None
            rows = kids.stdout.split("\n")[:-1] if kids is not None and kids.returncode == 0 else []
            if rows and all(r.split()[1] == "tree" for r in rows):
                lines = git(root, "ls-tree", tree) + "\n" + f"040000 tree {head[2]}\tnest\n"
                built = git_try(root, "mktree", input_text=lines.lstrip("\n"))
        if er.returncode != 0 or (ent and (built is None or built.returncode != 0)):
            print(f"skip (the nest entry of {node_id} is unreadable or not a non-empty tree of "
                  f"trees; the ref is untouched): {ref}", file=sys.stderr)
            return None
        if ent:
            tree = built.stdout.strip()
        old_tree = git(root, "rev-parse", f"{tip}^{{tree}}", check=False)
        if old_tree == tree:
            return None  # unchanged — versions record change, not time
    # --first-parent: a collapse's members are extra parents, not versions
    n = int(git(root, "rev-list", "--count", "--first-parent", tip)) + 1 if tip else 1
    parent = ["-p", tip] if tip else []
    subject = f"{msg_prefix}v{n} {node_id}"
    message = f"{subject}\n\n{trailer}\n" if trailer else subject
    commit = git(root, "commit-tree", tree, *parent, "-m", message)
    # CAS (goal:g4.13.1): "" = the ref must not exist; a refusal skips this node only
    res = git_try(root, "update-ref", ref, commit, tip or "")
    if res.returncode == 0 and tip is None and (parse_mint_id(path) or "") and ref == mint_node_ref(parse_mint_id(path)):
        MINTED_THIS_RUN[parse_mint_id(path)] = node_id
    if res.returncode != 0:
        # ONE line whatever git said: a held ref lock is 7 lines (the lock path, a blank,
        # a 5-line "Another git process" hint); the join keeps the hint, drops the blanks
        why = " | ".join(ln.strip() for ln in res.stderr.splitlines() if ln.strip())
        if "but expected" in why or "reference already exists" in why:
            print(f"skip (ref moved since read; the next tick re-versions it): {ref}: "
                  f"{why}", file=sys.stderr)
        else:   # not a CAS miss (a stale lock, a permission error, a full disk)
            print(f"ERROR: update-ref {ref} failed (not a CAS miss): {why}", file=sys.stderr)
            UPDATE_REF_FAILURES.append(ref)
        return None
    return f"v{n}"


def iter_node_files(root: Path):
    yield from sorted((root / "nodes").rglob("*.md"))


def payload_args_to_nodes(root: Path, paths: list[Path],
                          engine_root: Path) -> tuple[list[Path], list[str]]:
    """goal:g7.33.19.1 -- translate explicit `commit <path>` arguments: a node
    file stays; a path some LIVE node names as its `payload_ref` becomes that
    node's file (one version per node, whichever of its two paths was named);
    anything else comes back in `unowned`, by name. Nothing is written here."""
    nodes: list[Path] = []
    unowned: list[str] = []
    owners: dict[str, Path] | None = None
    for p in paths:
        try:
            is_node = p.is_file() and parse_node_id(p) is not None
        except UnicodeDecodeError:
            is_node = False
        if is_node:
            found = p
        else:
            if owners is None:
                owners = {}
                for n in iter_node_files(root):
                    if is_retired_node_file(root, n):
                        continue
                    try:
                        ref = parse_payload_ref(n)
                    except UnicodeDecodeError:
                        continue
                    if ref:
                        owners.setdefault(ref.removeprefix("./"), n)
            keys = [str(p).removeprefix("./")]
            try:
                keys.append(p.resolve().relative_to(engine_root.resolve()).as_posix())
            except ValueError:
                pass
            found = next((owners[k] for k in keys if k in owners), None)
        if found is None:
            unowned.append(str(p))
        elif found not in nodes:
            nodes.append(found)
    return nodes, unowned


def is_retired_node_file(root: Path, path: Path) -> bool:
    """True for a node under `nodes/deprecated/` — retired, moved, never
    deleted (CLAUDE.md "Retire, never delete")."""
    try:
        rel = path.resolve().relative_to((root / "nodes").resolve())
    except ValueError:
        return False
    return bool(rel.parts) and rel.parts[0] == "deprecated"


class GridLock:
    """Exclusive advisory flock held across one `commit --all`.

    hypothesis:l3w0-grid-flock — a manual director `grid.py commit --all` and
    the 5-minute grid_sync cron on the same box serialize on this lock instead
    of racing on the same node refs. Only `commit --all` (non-session) takes
    it; single-file commits and every read verb take no lock.

    The lockfile lives in `.agi/sessions/` (scratch, never versioned). The
    holder stamps its pid into the file so a waiter that times out can name
    it in the error. flock is advisory and process-scoped, so the lock is
    released automatically when the holder exits even on an exception path;
    close()/release() also free it on the clean path.

    hypothesis:l3-grid-lock-doubled-path — `root` is the GRAPH root, which is
    the `.agi/` directory itself under G11 (`locations.project_root_from_env`
    returns `<repo>/.agi`, the graph dir, never the repo root). So the lock
    dir is the graph's own `sessions/`, spelled as `root / "sessions"` — NOT
    `root / ".agi" / "sessions"`, which doubles the `.agi` into a stray
    `<repo>/.agi/.agi/sessions` (hypothesis:l3-budget-dir-dropped-agi,
    hypothesis:l3-rotate-pin-path-readback). The pre-fix doubled path was
    still /shared/ by a cron `cd .agi` run and a repo-root hand run (both
    resolve to the same graph root), so the flock did serialize them, but it
    lived in the wrong scratch dir, disagreed with `_grid_lock_path` and every
    documented path, and let a correct-location holder race it. Legacy bare
    roots keep `.agi/sessions`; only the G11 graph dir uses the direct form.
    """
    def __init__(self, root: Path, wait_seconds: int) -> None:
        # G11 graph root => the `.agi` dir itself: sessions sit directly under
        # it. Legacy bare root => `.agi/sessions`, as the contract documents.
        # G11 graph root: sessions sit directly under it. Route through
        # `shared_sessions_dir` (not the plain per-worktree join) because the
        # grid `--all` lock must be ONE flock across every git worktree -- the
        # refs it serializes are shared, so a per-worktree lock forks the guard.
        self._lock_dir = locations.shared_sessions_dir(root) \
            if locations.is_graph_dir(root) else root / ".agi" / "sessions"
        self._path = self._lock_dir / ".grid.lock"
        self._wait_seconds = wait_seconds
        self._f = None

    def acquire(self) -> None:
        self._lock_dir.mkdir(parents=True, exist_ok=True)
        # open append so we create-if-missing and never truncate a holder's pid
        f = open(self._path, "a+")
        deadline = time.time() + self._wait_seconds
        holder = None
        while True:
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except OSError:
                try:
                    f.seek(0)
                    reader = f.read().strip()
                    if reader:
                        holder = reader
                except OSError:
                    pass
                if time.time() >= deadline:
                    f.close()
                    holder_msg = f" (held by pid {holder})" if holder else ""
                    print(
                        f"grid: commit --all could not acquire the grid lock "
                        f"{self._path}{holder_msg} within {self._wait_seconds}s; "
                        f"another commit (manual or the grid_sync cron) is in "
                        f"progress — wait for it to finish and retry",
                        file=sys.stderr)
                    sys.exit(2)
                time.sleep(0.05)
        # We hold the lock: stamp our pid so a waiter can name us.
        f.seek(0)
        f.truncate()
        f.write(str(os.getpid()))
        f.flush()
        self._f = f

    def release(self) -> None:
        if self._f is not None:
            try:
                fcntl.flock(self._f, fcntl.LOCK_UN)
            except OSError:
                pass
            self._f.close()
            self._f = None

    def __enter__(self) -> "GridLock":
        self.acquire()
        return self

    def __exit__(self, *exc) -> None:
        self.release()


def cmd_commit(root: Path, files: list[str], do_all: bool,
               session: tuple[str, str] | None, prefix: str = "",
               engine_root: Path | None = None,
               allow_branch: bool = False,
               lock_wait: int = 120) -> None:
    """Snapshot node files.

    Non-session writes go to the mint-id ref (goal:g2.5) and, unless the
    node has no `mint_id`, the commit body carries a `Parent-Mint-Id:`
    trailer per parent (goal:g2.7, `build_parent_mint_trailer`). A node
    missing `mint_id` is reported loudly (`ERROR:`, naming the node and
    file — see `write_ref_for`/`MissingMintIdError`) and skipped, never
    silently written under a node-id-keyed ref.

    A node carrying `payload_ref` also commits its payload into the same
    tree (goal:g6.3, `resolve_payload` / `build_tree`), so `refs/grid/node/
    <mint-id>` accumulates v1 -> v2 -> v3 of the *file*, not just of the
    node's prose. A `payload_ref` that resolves nowhere is reported and the
    node is committed **without** a payload entry rather than skipped: the
    node is still real and its history still matters, and dropping it would
    breach G7's node-count invariant to report a payload problem.

    Session (D3) writes deliberately carry no payload. A draft is a node
    file under review; the payload dimension belongs to the accepted node.

    **This must stay a per-node try/except, never a batch-aborting one.**
    `--all` runs unattended every 5 minutes via cron; a node without a
    mint_id (e.g. created between a backfill and its next run) must not
    stop every OTHER node in the corpus from committing and being pushed —
    that is the exact failure class the pre-fix `sanitize()` colon bug
    produced (see module docstring), and this file does not get to
    reintroduce it under a different cause.
    """
    if grid_retired(root):
        print(RETIRED_LINE)
        return
    ensure_repo(root)

    # hypothesis:grid-commit-guard-and-writer-read-one-namespace conjunct 1 --
    # a DIRECT `cmd_commit` call must resolve the trunk itself, from the same
    # config the guard below reads. `main()` calling `apply_storage_trunk`
    # does not help a library or test caller, and the guard would then compare
    # the config-aware `ref_ns_for(root)` against writes still going to the
    # module-global `REF_NS` default -- guard and writer, two namespaces.
    apply_storage_trunk(root)
    global LEGACY_TIPS
    LEGACY_TIPS = None
    problem = None if session else legacy_config_problem(root)
    if problem:    # goal:g7.16.1.11.46.16 R4: fail closed, write no ref
        sys.exit(f"grid: refusing commit: {problem}; nothing written")

    # hypothesis:grid-old-namespace-refilled-and-forked conjunct 2 -- refuse by
    # name after a storage-trunk migration. `ref_ns_for` now reads the shared
    # checkout's config, so a stale linked worktree is redirected to the trunk;
    # but a config that genuinely lost `storage_trunk` while nested trunk refs
    # remain is the post-migration state, and committing there would re-mint
    # the migrated-from namespace and fork a second v1 root. Name BOTH the old
    # namespace and the trunk, exit non-zero, write no ref. Session (D3) drafts
    # are exempt: a draft is not an accepted version and takes no namespace.
    if not session and ref_ns_for(root) == DEFAULT_REF_NS:
        migrated = migrated_trunk_namespaces(root)
        if migrated:
            sys.exit(
                f"grid: refusing commit: resolved namespace {DEFAULT_REF_NS!r} "
                f"but this repo already holds refs under {', '.join(migrated)}. "
                f"The shared config does not declare grid.storage_trunk (stale "
                f"linked worktree, or the key was blanked after migration); "
                f"writing to {DEFAULT_REF_NS!r} would re-mint the migrated-from "
                f"namespace and fork history. Set grid.storage_trunk to "
                f"{migrated[0]!r} in the shared checkout."
            )

    # hypothesis:l2w15-grid-master-guard — refuse commit on a non-master
    # branch unless --allow-branch is passed. Session commits (D3 drafts)
    # are never gated. Addendum (owners, seasons-as-branches): any branch the
    # season grammar admits (canonical season<n>/… or the legacy master/
    # season/s<N> aliases) is admitted like master; anything else — feature
    # branches, malformed season names, detached HEAD — refused.
    #
    # hypothesis:lm-grid-commit-configured-trunk-lifts-branch-blind-refusal —
    # the refusal exists ONLY because node refs are branch-blind: every branch
    # writes the same `refs/grid/node/<mint-id>`, so a feature branch would
    # collide with master's history. A tree that declares a non-default
    # `grid.storage_trunk` keeps its refs in a project-specific namespace, so
    # the collision it is refused for cannot occur and the refusal is lifted.
    # `ref_ns_for(root)` is the config resolver, NOT the module global `REF_NS`
    # (correct only after `apply_storage_trunk()` has run). It returns
    # `DEFAULT_REF_NS` for absent/unreadable/empty config, so an unconfigured
    # tree refuses EXACTLY as before and `--allow-branch` stays its override.
    # goal:g7.16.1.11.46.16: the lift keys on the trunk being DECLARED (`trunk_declared`), so a
    # project that declares the default spelling `refs/grid` plus `grid.legacy_namespaces` keeps it.
    if not session and not allow_branch and not trunk_declared(root):
        # resolve the checked-out branch of the repo that owns the graph
        # Use symbolic-ref: on a branch it returns the ref name (e.g. master,
        # work); on detached HEAD it fails (exit != 0) which we treat as not
        # master.
        branch = git(root, "symbolic-ref", "--short", "HEAD", check=False)
        # git symbolic-ref returns empty string on error with check=False
        if not branches.is_legal_branch(branch):
            ref_name = branch if branch else "detached HEAD"
            print(
                f"grid: refusing commit --all on {ref_name!r}, node refs are "
                f"branch-blind; merge to master first or pass --allow-branch",
                file=sys.stderr
            )
            sys.exit(2)

    paths = list(iter_node_files(root)) if do_all else [Path(f) for f in files]
    if not paths:
        sys.exit("ERR: give node files or --all")
    if not do_all and not session:
        # goal:g7.33.19.1 -- a payload path versions the node that carries it;
        # a path no node owns is refused by name BEFORE any ref is written.
        paths, unowned = payload_args_to_nodes(root, paths,
                                               engine_root or default_engine_root())
        if unowned:
            sys.exit("ERR: no build node carries payload_ref "
                     + ", ".join(unowned))

    # hypothesis:l3w0-grid-flock — commit --all serializes with any other
    # commit --all on the same box (incl. the 5-min grid_sync cron) via an
    # exclusive advisory flock on .agi/sessions/.grid.lock. Only --all; a
    # single-file commit and the read verbs take no lock. The lock covers the
    # evidence-gate rewrites and every ref write below, then is released here.
    lock: GridLock | None = None
    if do_all and not session:
        lock = GridLock(root, lock_wait)
        lock.acquire()
    try:
        # hypothesis:gate-must-sit-on-the-commit-path (goal:g7) -- the evidence
        # gate, at the point of acceptance. A writer that records a verdict through
        # `cli.py done` or `post_wire` meets the gate there; one that writes the
        # file directly meets it HERE, before the bytes become a version. Runs over
        # every file about to be committed; rewrites only a decisive verdict nothing
        # backs (demoted in place, node kept), so a passing node is byte-identical
        # and the unchanged-check below still sees it as unchanged.
        #
        # Session (D3) drafts are not gated: a draft is a node under review, not an
        # accepted one, and the gate belongs on acceptance.
        demoted = 0
        if not session:
            # hypothesis:l4-the-grid-cron-evidence-gate-defers-... — on the
            # cron path (--all, never --session) do not rewrite node FILES in
            # MAIN by the gate while the suite holds its window. Probe the
            # suite lock with verification's OWN held/stale judgement (ONE
            # reader, never a second lock parser). A LIVE foreign pid defers
            # this tick's rewrite — the ref-write loop below proceeds unchanged;
            # a lock we took (or a stale dead pid, broken inside) unlinks back
            # to a pid-free probe state and the gate runs as today.
            holder = verification.suite_lock_holder(root)
            if holder is not None:
                print(f"evidence gate deferred: suite lock held by pid {holder}",
                      file=sys.stderr)
            else:
                demoted = sum(1 for d in evidence_gate.enforce_on_disk(root, paths)
                              if d.written)
        id_index = None if session else build_id_index(root)
        import links   # ONE resolver per command, lazy: an address-only graph builds no index
        resolve = None if session else links.address_resolver(root)
        engine_root = engine_root or default_engine_root()
        written = 0
        errors = 0
        UPDATE_REF_FAILURES.clear()
        LEGACY_HELD.clear()
        DOUBLE_MINT_REFUSED.clear()
        MINTED_THIS_RUN.clear()
        global _DM_CACHE
        _DM_CACHE = None
        payloads = 0
        payload_missing = 0
        payload_retired = 0
        for p in paths:
            if not p.exists():
                print(f"skip (missing): {p}", file=sys.stderr)
                continue
            node_id = parse_node_id(p)
            if node_id is None:
                print(f"skip (no id): {p}", file=sys.stderr)
                continue
            payload = None
            if session:
                ref = session_ref(session[0], session[1], node_id)
                msg_prefix = prefix + f"session {session[0]}/{session[1]}: "
                trailer = None
            else:
                try:
                    ref = write_ref_for(p, node_id)
                except MissingMintIdError as exc:
                    print(f"ERROR: {exc}", file=sys.stderr)
                    errors += 1
                    continue
                msg_prefix = prefix
                trailer = build_parent_mint_trailer(p, id_index, resolve)
                payload_ref = parse_payload_ref(p)
                if payload_ref:
                    found = resolve_payload(root, payload_ref, engine_root,
                                            parse_location(p))
                    if found is None and is_retired_node_file(root, p):
                        # A retired build node's file is retired with it; its
                        # bytes live in the node's earlier grid versions. Counted
                        # apart so `unresolved` means a LIVE node lost its file.
                        payload_retired += 1
                    elif found is None:
                        print(f"WARN: {node_id} payload_ref {payload_ref!r} resolves "
                              f"neither under {PAYLOAD_DIR}/ nor in {engine_root} — "
                              "committing the node without a payload entry",
                              file=sys.stderr)
                        payload_missing += 1
                    else:
                        payload = found[0]
                        payloads += 1
            v = commit_file(root, p, ref, msg_prefix, trailer=trailer, payload=payload)
            if v:
                written += 1
                print(f"{v}  {ref.removeprefix(REF_NS + '/')}")
        print(f"grid: {written} new version(s), {errors} error(s) (missing mint_id), "
              f"{payloads} with payload, {payload_missing} payload(s) unresolved, "
              f"{payload_retired} retired with their node, "
              f"{demoted} demoted by the evidence gate")
        if LEGACY_HELD:    # goal:g7.16.1.11.46.16: held, not forked; not clean
            print(f"grid: {len(LEGACY_HELD)} held (a read-only legacy tip is not yet in the ref's "
                  f"history): run `grid.py unify --write`", file=sys.stderr)
        if DOUBLE_MINT_REFUSED:    # goal:g7.16.1.11.46.16: refused by name above; the run went on, not clean
            print(f"grid: {len(DOUBLE_MINT_REFUSED)} new mint(s) refused (the id is already carried by another mint)", file=sys.stderr)
        if UPDATE_REF_FAILURES or LEGACY_HELD or DOUBLE_MINT_REFUSED:   # goal:g4.13.1 N1: the run went on; it is not clean
            sys.exit(1)
    finally:
        if lock is not None:
            lock.release()


def _resolve_read_ref(root: Path, path: Path, node_id: str) -> str | None:
    """The ref to READ `node_id`'s history from, given its current file
    `path`: the mint-id ref if it exists, else the legacy node-id-keyed ref
    if IT exists, else None. This is the read-side fallback goal:g2.5
    requires -- a previous change shipped the write-side switch without it,
    which made every pre-migration version silently unreachable; caught in
    review, not shipped again here."""
    mint_id = parse_mint_id(path)
    if mint_id:
        mint_ref = mint_node_ref(mint_id)
        if ref_tip(root, mint_ref) is not None:
            return mint_ref
    legacy_ref = node_ref(node_id)
    if ref_tip(root, legacy_ref) is not None:
        return legacy_ref
    return None


def resolve_ref(root: Path, node_id: str) -> str:
    """Resolve the grid ref to read `node_id`'s history from -- mint-id ref
    preferred, legacy node-id ref as fallback (see `_resolve_read_ref`). The
    node's *current* file on disk (if any) supplies its mint_id; a node with
    no file on disk today (deprecated, renamed) still resolves via the
    legacy ref if that ref has history, so a rename never strands old
    versions."""
    node_file = build_id_index(root).get(node_id)
    if node_file is not None:
        ref = _resolve_read_ref(root, node_file, node_id)
    else:
        legacy_ref = node_ref(node_id)
        ref = legacy_ref if ref_tip(root, legacy_ref) is not None else None
    if ref is None:
        sys.exit(f"ERR: no grid history for {node_id} "
                 f"(checked mint-id ref and {node_ref(node_id)})")
    return ref


def cmd_log(root: Path, node_id: str, n: int) -> None:
    ref = resolve_ref(root, node_id)
    print(git(root, "log", f"-{n}", "--first-parent", "--format=%h %ad %s", "--date=short", ref))


def cmd_diff(root: Path, node_id: str, back: int) -> None:
    """Diff two versions of a node's `node.md`.

    `:(top)` on the pathspec is `ls-tree --full-tree`'s counterpart — `git diff`
    has no such flag, so the magic prefix is the only way to say "this path is
    relative to the tree root, not to git's prefix". It is belt-and-braces now
    that `git()` runs from `repo_root`, but it is the second place the graph-root
    `-C` bug was live and the only one `--full-tree` never covered: a bare
    `node.md` pathspec became `.agi/node.md`, matched nothing, and this command
    printed an empty diff and exited 0 for a node with three real versions.
    """
    ref = resolve_ref(root, node_id)
    count = int(git(root, "rev-list", "--count", "--first-parent", ref))
    if count < back + 1:
        sys.exit(f"ERR: only {count} version(s); cannot go back {back}")
    print(git(root, "diff", f"{ref}~{back}", ref, "--", f":(top){NODE_ENTRY}"))


def cmd_versions(root: Path, node_id: str) -> None:
    """Version count -- reads fall back the same way `resolve_ref` does
    (goal:g2.5), so a node whose mint-id ref has no history yet still
    reports its legacy-ref count instead of a misleading 0."""
    node_file = build_id_index(root).get(node_id)
    if node_file is not None:
        ref = _resolve_read_ref(root, node_file, node_id)
    else:
        legacy_ref = node_ref(node_id)
        ref = legacy_ref if ref_tip(root, legacy_ref) is not None else None
    tip = ref_tip(root, ref) if ref else None
    print(int(git(root, "rev-list", "--count", "--first-parent", tip)) if tip else 0)


# --- payload read side (goal:g6.3 / goal:g6.1) -------------------------------


def version_rev(root: Path, ref: str, node_id: str, version: int | None) -> str:
    """The revision holding version `v<version>` of `node_id`, or the tip.

    Versions count forward from 1 (`commit_file`'s `rev-list --count --first-parent` + 1), so
    v(count) is the tip and v1 is `tip~(count-1)`. An out-of-range version is a
    hard error naming the range: silently serving the tip for a version that
    does not exist is the "partial answer served as a complete one" failure G7
    names in its invariants.
    """
    if version is None:
        return ref
    count = int(git(root, "rev-list", "--count", "--first-parent", ref))
    if not 1 <= version <= count:
        sys.exit(f"ERR: {node_id} has {count} version(s); v{version} does not exist")
    return f"{ref}~{count - version}"


def cmd_payload(root: Path, node_id: str, version: int | None,
                out: str | None) -> None:
    """Read a node's payload back out of its grid ref.

    With no `--out`, raw bytes go to stdout (so `grid.py payload X | diff - f`
    works). With `--out`, the file is written with its recorded mode, symlinks
    included — `materialize_entry` is the exact inverse of what `commit_file`
    stored.
    """
    ref = resolve_ref(root, node_id)
    rev = version_rev(root, ref, node_id, version)
    entry = read_tree_entry(root, rev, PAYLOAD_ENTRY)
    if entry is None:
        sys.exit(f"ERR: no payload recorded for {node_id} at "
                 f"{'v' + str(version) if version else 'the tip'} — the node "
                 "either carries no payload_ref or has not been committed "
                 "since payloads began being recorded (run `grid.py commit --all`)")
    mode, data = entry
    if out is None:
        sys.stdout.buffer.write(data)
        return
    materialize_entry(Path(out), mode, data)
    print(f"{mode}  {out}  ({len(data)} bytes)")


def engine_tracked_files(engine_root: Path) -> list[str]:
    """Every file git tracks in the engine repo, or [] if it is not one.

    `ls-files` is the third cwd-scoped subcommand this file calls, and it lists
    only what is under git's prefix — so it goes through `repo_root` like the
    rest. Identity in practice (a source root is never named `.agi`), routed
    anyway so no git invocation here is an exception to the rule.
    """
    res = subprocess.run(["git", "-C", str(repo_root(engine_root)), "ls-files"],
                         capture_output=True, text=True)
    return [l for l in res.stdout.splitlines() if l] if res.returncode == 0 else []


def cmd_checkout(root: Path, node_ids: list[str], do_all: bool,
                 dest: str | None, engine_root: Path | None = None,
                 unmanaged: bool = True, force: bool = False) -> None:
    """Materialise payloads out of the grid into the graph repo's own
    `payloads/` tree — the staged copy an author edits (goal:g6.1).

    This is the step that reverses the arrow in practice: after a checkout,
    `resolve_payload` prefers `payloads/<payload_ref>` over the engine tree,
    so the next `grid.py commit --all` records **your edit in the graph** as
    the node's next version, and `stitch.py --out --from-grid` writes it into
    the engine. **Graph content is never filled in from disk**: a node with no
    payload in its grid ref yet is reported, never silently backfilled from the
    engine tree, because that would let a stale engine file masquerade as
    something the graph holds.

    **Uncommitted payload edits are never overwritten without `force`.** This
    command is `git checkout .` on the payload tree, and it shipped without the
    dirty check `git checkout` itself has. That cost real work within the hour:
    two agents were editing `payloads/` in one worktree (goal:g4.1), one ran
    `checkout --all`, and the other's uncommitted edits to `grid.py` — this
    function — were silently reverted to the grid tip. A file whose bytes
    differ from what the grid holds is *unrecorded work*; reverting it is the
    one thing goal:g7 says must never happen quietly.

    `unmanaged` (default on) additionally copies engine files that are tracked
    by git but carry **no node** — under `goal:g6.8`'s boundary that is
    `tests/fixtures/**` and `.jsonl` streams. They are not graph content and
    are never read back by `commit --all` (no node names them), but without
    them `payloads/` is not a *runnable* tree: 19 tests fail on missing
    fixtures, which is a trap for the workflow CLAUDE.md tells authors to use.
    The counts are reported separately so the distinction stays visible.
    """
    ensure_repo(root)
    engine_root = engine_root or default_engine_root()
    out_root = Path(dest).resolve() if dest else root / PAYLOAD_DIR
    wanted = set(node_ids)
    written = no_payload = skipped_dirty = 0
    managed: set[str] = set()

    def would_clobber(dst: Path, mode: str, data: bytes) -> bool:
        """True if `dst` exists and holds something other than what we are
        about to write. Compares link text for symlinks, bytes otherwise."""
        if not (dst.is_symlink() or dst.exists()):
            return False
        try:
            if dst.is_symlink():
                return os.readlink(dst).encode("utf-8") != data
            return dst.read_bytes() != data or git_mode(dst) != mode
        except Exception:
            return True

    for p in iter_node_files(root):
        node_id = parse_node_id(p)
        if node_id is None or (not do_all and node_id not in wanted):
            continue
        payload_ref = parse_payload_ref(p)
        if not payload_ref:
            if not do_all:
                print(f"skip (no payload_ref): {node_id}", file=sys.stderr)
            continue
        managed.add(payload_ref)
        ref = _resolve_read_ref(root, p, node_id)
        entry = read_tree_entry(root, ref, PAYLOAD_ENTRY) if ref else None
        if entry is None:
            print(f"WARN: {node_id} has no payload in the grid yet "
                  f"(run `grid.py commit --all` first)", file=sys.stderr)
            no_payload += 1
            continue
        dst = out_root / payload_ref
        if not force and would_clobber(dst, *entry):
            print(f"SKIP (locally modified): {payload_ref} — differs from the "
                  f"grid tip. Run `grid.py commit --all` to record your edit, "
                  f"or `checkout --force` to discard it.", file=sys.stderr)
            skipped_dirty += 1
            continue
        materialize_entry(dst, *entry)
        written += 1

    copied = skipped_unmanaged = 0
    if unmanaged and do_all:
        for rel in engine_tracked_files(engine_root):
            if rel in managed:
                continue
            src = engine_root / rel
            if not (src.is_symlink() or src.exists()):
                continue
            mode = git_mode(src)
            data = (os.readlink(src).encode("utf-8") if mode == GIT_MODE_SYMLINK
                    else src.read_bytes())
            dst = out_root / rel
            if not force and would_clobber(dst, mode, data):
                skipped_unmanaged += 1
                continue
            materialize_entry(dst, mode, data)
            copied += 1

    print(f"grid checkout: {written} payload(s) from the grid -> {out_root}; "
          f"{no_payload} not yet in the grid; "
          f"{copied} unmanaged file(s) copied from {engine_root} "
          f"(no node — not graph content, never committed back)")
    if skipped_dirty or skipped_unmanaged:
        print(f"grid checkout: {skipped_dirty + skipped_unmanaged} file(s) left "
              "alone because they are locally modified (see SKIP lines above)",
              file=sys.stderr)


def cmd_status(root: Path, engine_root: Path | None = None) -> None:
    """Per-node drift vs ref tip -- one of the "Reads" goal:g2.5 requires to
    fall back to the legacy node-id ref when no mint-id ref exists yet, so a
    node mid-transition (mint_id backfilled, not yet committed under it)
    reports drift against its real last version instead of reading as NEW.

    Compares the same tree `commit_file` would build, payload included
    (goal:g6.3). Comparing `node.md` alone would report `clean` for a node
    whose payload had been edited — the status command quietly disagreeing
    with the commit command about what "changed" means.
    """
    ensure_repo(root)
    engine_root = engine_root or default_engine_root()
    new = changed = clean = 0
    for p in iter_node_files(root):
        node_id = parse_node_id(p)
        if node_id is None:
            continue
        ref = _resolve_read_ref(root, p, node_id)
        if ref is None:
            new += 1
            print(f"NEW      {node_id}")
            continue
        payload_ref = parse_payload_ref(p)
        found = resolve_payload(root, payload_ref, engine_root,
                                parse_location(p)) if payload_ref else None
        fresh = tree_entries(root, p, found[0] if found else None, write=False)
        # goal:g4.13.1: a collapse's nest/ entry is carried, not drift
        if fresh == [e for e in read_tree(root, ref) if e[0] != "nest"]:
            clean += 1
        else:
            changed += 1
            print(f"CHANGED  {node_id}")
    print(f"grid status: {new} new, {changed} changed, {clean} clean")


def _rename_ref(root: Path, old_ref: str, new_ref: str, write: bool) -> str:
    """Shared compare-and-swap ref-rename core for every grid ref migration
    this file has needed: the pre-fix-sanitize() -> injective-sanitize()
    cleanup (`cmd_migrate_refs`) and the node-id-ref -> mint-id-ref
    migration (`cmd_migrate_mint_refs`, goal:g2.5). One implementation, so
    the safety-critical part -- the actual git mutation -- is never
    duplicated, only the surrounding collision-detection and reporting
    differ per caller.

    Returns one of:
      "no-history"  -- `old_ref` has nothing to move.
      "unchanged"   -- `new_ref` already exists and matches `old_ref`'s tip
                       exactly (already migrated -- idempotent no-op).
      "conflict"    -- `new_ref` exists with DIFFERENT history. Neither side
                       is touched; the caller decides how to report it.
      "moved"       -- `old_ref` had history and `new_ref` did not. If
                       `write` is true, the move already happened by the
                       time this returns (see below); if `write` is false,
                       nothing was touched and this is what "WOULD-MOVE"
                       means.

    The mutation, when `write=True` and the result is "moved":
      1. `git update-ref <new_ref> <old_tip>` -- point the NEW ref at the
         SAME commit object `old_ref` already pointed at. This is what
         preserves the full multi-version chain: the new ref's `git log`
         traverses every commit `old_ref` ever accumulated, because it is
         literally the same commit, not a fresh one. Skipping this step and
         letting the next ordinary `commit --all` create the new ref instead
         is exactly the fork this function exists to prevent -- that path
         starts a brand-new v1 ROOT commit with no parent, stranding the
         real history on the ref about to be deleted.
      2. `git update-ref -d <old_ref> <old_tip>` -- a **compare-and-swap
         delete**: passing the observed sha as the second argument makes git
         verify `old_ref` still points at exactly that commit before
         deleting it. A concurrent writer that moved `old_ref` between step 0
         (the read) and this delete makes the delete FAIL instead of
         silently discarding whatever that writer just committed.
    """
    old_tip = ref_tip(root, old_ref)
    if old_tip is None:
        return "no-history"
    new_tip = ref_tip(root, new_ref)
    if new_tip is not None:
        return "unchanged" if new_tip == old_tip else "conflict"
    if write:
        if git_try(root, "update-ref", new_ref, old_tip, "").returncode != 0:  # CAS (goal:g4.13.1)
            return "conflict"
        git(root, "update-ref", "-d", old_ref, old_tip)
    return "moved"


def _retired_write(root: Path, write: bool) -> bool:
    """goal:g7.16.1.11.13.1 F1: a `--write` migrate verb moves refs/grid, so
    once grid_sync is retired it refuses by name (RETIRED_LINE, rc 0, no ref
    moved); a dry run is never gated."""
    if write and grid_retired(root):
        print(RETIRED_LINE)
        return True
    return False


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

        status = _rename_ref(root, old_ref, new_ref, write)
        if status == "no-history":
            unchanged += 1  # no history under the old scheme -- nothing to move
        elif status == "unchanged":
            unchanged += 1  # already migrated -- idempotent no-op
        elif status == "conflict":
            conflicts += 1
            print(f"CONFLICT  {nid}: {new_ref} already exists with "
                  f"different history than {old_ref} -- not touched",
                  file=sys.stderr)
        else:  # "moved"
            action = "RENAME" if write else "WOULD-RENAME"
            print(f"{action}  {old_ref} -> {new_ref}  ({nid})")
            renamed += 1

    for r, v in sorted(collided.items()):
        print(f"COLLISION  {r} shared by {len(v)} ids (pre-existing under "
              f"the old scheme, needs human triage -- cannot tell whose "
              f"history it holds): {', '.join(v)}", file=sys.stderr)

    mode = "write" if write else "dry-run"
    print(f"grid migrate-refs ({mode}): {renamed} renamed, {unchanged} "
          f"unchanged, {conflicts} conflict(s), {len(collided)} collided "
          f"old ref(s) covering {in_collision} id(s)")


def cmd_migrate_mint_refs(root: Path, write: bool) -> None:
    """Move `refs/grid/node/<node-id>` onto `refs/grid/node/<mint-id>`
    (goal:g2.5). Dry-run by default; `--write` applies. Reuses `_rename_ref`
    -- the identical compare-and-swap safety `cmd_migrate_refs` already has,
    not a parallel implementation.

    **This step MUST run before any `commit --all` under the new mint-id
    keying, and that ordering is the entire reason this command exists.**
    `commit_file` decides "is this node new (v1, no parent commit)" purely
    from whether its WRITE-TARGET ref already has a tip. Before this
    migration runs, none of the mint-id refs exist yet, so the very next
    `commit --all` would create a fresh v1 ROOT commit on every mint-id ref
    while the real, multi-version history stays stranded on the node-id ref
    nobody is looking at any more -- forking every migrated node at once,
    the same failure class that cost four refs and a manual reconciliation
    on 2026-08-24, at roughly 200x the scale (824 nodes here). Running this
    first makes each mint-id ref's tip BE the node-id ref's tip -- the same
    commit object, not a copy -- so the next `commit --all`, if there is any
    real drift, lands as v(n+1) with the correct parent and continues the
    history instead of forking it.

    Safety properties, all shared with `cmd_migrate_refs` via `_rename_ref`:
    dry-run by default, idempotent (a second `--write` run reports 0 moved),
    refuse-never-clobber (a destination with different history is a
    conflict, reported, untouched), compare-and-swap delete.

    Two things this migration additionally has to guard that the legacy one
    did not:
      - **A node with no `mint_id` is skipped and reported, never
        invented.** There is exactly one such node in the live corpus today
        (a pre-existing malformed frontmatter file, unrelated to this
        change -- see `level3:bin-grid`'s node body).
      - **A duplicate `mint_id` across two distinct nodes** would make two
        different node-id refs want to move to the SAME destination ref.
        `mint_permanent_id()` (122 bits of random entropy) makes this
        astronomically unlikely in practice, but it is checked anyway, the
        same way `cmd_migrate_refs` checks for a shared OLD ref: reported as
        a collision, neither side touched, since there is no way to know
        which node's history the shared destination should hold.
    """
    ensure_repo(root)
    entries: list[tuple[str, str | None, Path]] = []  # (node_id, mint_id, path)
    for p in iter_node_files(root):
        nid = parse_node_id(p)
        if nid is None:
            continue
        entries.append((nid, parse_mint_id(p), p))

    old_ref_to_ids: dict[str, list[str]] = {}
    new_ref_to_ids: dict[str, list[str]] = {}
    for nid, mint_id, _ in entries:
        old_ref_to_ids.setdefault(node_ref(nid), []).append(nid)
        if mint_id:
            new_ref_to_ids.setdefault(mint_node_ref(mint_id), []).append(nid)
    old_collided = {r: v for r, v in old_ref_to_ids.items() if len(v) > 1}
    new_collided = {r: v for r, v in new_ref_to_ids.items() if len(v) > 1}

    moved = already_correct = conflicts = skipped = in_collision = 0
    for nid, mint_id, path in entries:
        old_ref = node_ref(nid)
        if old_ref in old_collided:
            in_collision += 1
            continue
        if not mint_id:
            skipped += 1
            print(f"SKIP-NO-MINT-ID  {nid}  ({path})", file=sys.stderr)
            continue
        new_ref = mint_node_ref(mint_id)
        if new_ref in new_collided:
            in_collision += 1
            continue

        status = _rename_ref(root, old_ref, new_ref, write)
        if status in ("no-history", "unchanged"):
            already_correct += 1
        elif status == "conflict":
            conflicts += 1
            print(f"CONFLICT  {nid}: {new_ref} already has different "
                  f"history than {old_ref} -- not touched", file=sys.stderr)
        else:  # "moved"
            action = "MOVE" if write else "WOULD-MOVE"
            print(f"{action}  {old_ref} -> {new_ref}  ({nid})")
            moved += 1

    for r, v in sorted(new_collided.items()):
        print(f"COLLISION  {r} shared by {len(v)} ids (duplicate mint_id "
              f"-- needs human triage, cannot tell whose history it should "
              f"hold): {', '.join(v)}", file=sys.stderr)

    mode = "write" if write else "dry-run"
    print(f"grid migrate-mint-refs ({mode}): {moved} moved, {already_correct} "
          f"already correct, {conflicts} conflict(s), {skipped} skipped "
          f"(no mint_id), {in_collision} id(s) in a ref collision")


def _valid_ref(root: Path, ref: str) -> bool:
    """True iff git would accept `ref` as a refname. Raw subprocess rather
    than `git()` because an invalid candidate is a refusal to report, not a
    process to kill."""
    res = subprocess.run(
        ["git", "check-ref-format", ref], capture_output=True, text=True,
    )
    return res.returncode == 0


def cmd_migrate_trunk(root: Path, target: str | None, write: bool,
                      source: str | None = None) -> None:
    """Move EVERY ref under a source namespace into a different one
    (goal:g14.14.7): `refs/grid/node/<x>` -> `<trunk>/node/<x>`, the one
    ref-shape change `cmd_migrate_refs` and `cmd_migrate_mint_refs` do not
    cover -- both of those move refs WITHIN `refs/grid/node/`, neither
    changes the NAMESPACE.

    Ref-driven, not node-file-driven: the source list comes from
    `git for-each-ref <old>/node/`, so a ref whose node file was deleted or
    deprecated (or that never had one) still moves. Reuses `_rename_ref`
    UNCHANGED for the safety-critical mutation -- `update-ref <new> <old_tip>`
    (same commit object, so the full multi-version chain stays traversable),
    then a compare-and-swap `update-ref -d <old> <old_tip>` -- so it inherits
    dry-run-by-default, idempotency and refuse-never-clobber for free.

    `source` is the SOURCE namespace and defaults to `DEFAULT_REF_NS`
    (`refs/grid`), NOT to the config-resolved `REF_NS`. This is deliberate:
    `main()` resolves the config into `REF_NS` via `apply_storage_trunk`
    BEFORE dispatch, so with `grid.storage_trunk` already set the
    config-resolved value is the TARGET, and using it as the source makes
    `old_ns == new_ns` and moves nothing (the config-first order the
    hypothesis names would silently no-op). The verb's job is "move where the
    refs ARE onto a trunk"; a config-declared trunk is reached with `--to`
    absent and `--from` left at its default. The migration MUST run before any
    `commit --all` under the new config, or that commit forks fresh v1 refs
    under the new namespace while the old history sits unmoved.

    `target` is the DESTINATION namespace; absent, the configured
    `grid.storage_trunk` (`ref_ns_for`) is used, so the same command is the
    cut for both `--to` and config-declared trunks. A trailing `/` is
    stripped from both namespaces (the same one-spelling rule `ref_ns_for`
    enforces).

    Refuses cleanly (SystemExit, no ref touched) if the destination is empty
    or not a valid ref namespace. If `new_ns == old_ns` every ref reports
    unchanged and nothing is moved -- idempotent by construction.
    """
    ensure_repo(root)
    old_ns = (source or DEFAULT_REF_NS).strip().rstrip("/")
    new_ns = (target or ref_ns_for(root)).strip().rstrip("/")
    if not new_ns or not _valid_ref(root, f"{new_ns}/node/x"):
        sys.exit(f"ERR: migrate-trunk: {new_ns!r} is not a valid ref "
                 f"namespace (use e.g. refs/grid/local-maxxing)")

    prefix = f"{old_ns}/node/"
    suffixes = [line[len(prefix):] for line in
                git(root, "for-each-ref", prefix,
                    "--format=%(refname)").splitlines()
                if line.startswith(prefix) and len(line) > len(prefix)]

    moved = unchanged = conflicts = 0
    for suffix in suffixes:
        old_ref = f"{prefix}{suffix}"
        new_ref = f"{new_ns}/node/{suffix}"
        if old_ref == new_ref:
            unchanged += 1
            continue
        status = _rename_ref(root, old_ref, new_ref, write)
        if status == "moved":
            print(f"{'MOVE' if write else 'WOULD-MOVE'}  {old_ref} -> {new_ref}")
            moved += 1
        elif status == "conflict":
            conflicts += 1
            print(f"CONFLICT  {old_ref} -> {new_ref}: destination already "
                  f"has different history -- not touched", file=sys.stderr)
        else:  # "unchanged" or "no-history"
            unchanged += 1

    mode = "write" if write else "dry-run"
    print(f"grid migrate-trunk ({mode}): {old_ns} -> {new_ns}: {moved} "
          f"{'moved' if write else 'would-move'}, {unchanged} unchanged, "
          f"{conflicts} conflict(s)")


def _is_ancestor(root: Path, a: str, b: str) -> bool | None:
    """True/False for `a` an ancestor of `b`; None when git could not say (rc other than 0/1)."""
    rc = git_try(root, "merge-base", "--is-ancestor", a, b).returncode
    return True if rc == 0 else False if rc == 1 else None


#: goal:g7.16.1.11.46.16 (the third history): origin's `refs/grid/node` as ONE private, read-only-by-convention
#: mirror. `origin-snap` writes it (forced: it is a local mirror, never a shared ref), `unify --legacy` reads it,
#: nothing pushes it and the writer's nested-namespace refusal exempts it.
ORIGIN_SNAP_NS = "refs/grid/origin-snap"
#: one grid_sync lap, minutes: the least a snapshot pair may be apart for the second to call origin QUIET.
ORIGIN_LAP_MIN = 30
#: goal:g7.16.1.11.46.16 (council 14:21:47Z, condition (2) REPLACED by a BYTE TEST in alive's [correction] 14:53:03Z, council 3/3, 10-26): a diverged
#: origin pair with NO merge-base and a DIFFERENT tree is a CONFLICT unless EVERY blob of origin's tip tree was SEEN, each at its own path class (below).
#: No date compare survives: tip-vs-tip passed 10 origin-only edits and a root date is a re-mint coincidence (live roots: 1721 on 09-21, 225 on 10-08).
#: WHOLE-VERDICT CADENCE of `unify --write` (alive 16:36Z: say what the code does): `_origin_quiet` runs (1) in the pre-run gate, (2) immediately before the FIRST
#: unrelated-root write, (3) before every UNRELATED_QUIET_EVERY-th unrelated-root write after it (so at most this many writes sit between two whole reads; a
#: banked or tree-equal row does not count), and (4) once after the run. A whole-listing read is ~0.17 s; one per write would hold the grid lock ~5 min over
#: ~1900 pairs. What EVERY write does re-read, immediately before its compare-and-swap, is that pair's own two tips (a moved tip -> CONFLICT, nothing written).
UNRELATED_QUIET_EVERY = 50
UNRELATED_CLASSES = ("live-seen", "trunk-seen")
_PAYLOAD_REF_RE = re.compile(r"[A-Za-z0-9_.][A-Za-z0-9_./+-]*")    # a leading dot is legal (`.agi/config.json`); `:` (pathspec magic) and a leading `-` are not
_ZERO_SHA = "0" * 40


def _raw_blobs(text: str) -> dict[str, set[str]]:
    """{path: {blob}} from `git log --raw --no-abbrev --format=` output: the NEW side of every change that is not a delete."""
    out: dict[str, set[str]] = {}
    for line in text.splitlines():
        if not line.startswith(":") or "\t" not in line:
            continue
        meta, _, path = line.partition("\t")
        fields = meta.split()
        if len(fields) >= 5 and fields[3] != _ZERO_SHA:
            out.setdefault(path, set()).add(fields[3])
    return out


class _TrunkSeen:
    """The trunk's blob evidence for `_unrelated_class`, built ONCE per run (alive 14:53:03Z): every blob that was ever at a `.agi/nodes` path
    (live or deprecated/) on `trunk`'s history -- ONE path-limited `git log --raw --no-abbrev -m --format= <trunk> -- .agi/nodes` (`-m`: a blob that
    entered the trunk only in a MERGE's resolution is trunk history too; alive 16:50Z C2, 1441 such blobs on 10-26) -- plus, on
    demand and cached, the blobs ever at ONE `payload_ref` path (`at_path`). FAIL CLOSED: a walk that errors or yields 0 blobs sets `problem`, and
    `_unrelated_class` then answers CONFLICT for every pair; an empty set is never read as a real one. `cost` quotes the walk (wall seconds, the
    git child's peak RSS) under the memory guard."""

    def __init__(self, root: Path, trunk: str) -> None:
        import resource  # noqa: PLC0415
        self.root, self.trunk, self.problem, self.nodes, self._paths, self.cost = root, trunk, "", set(), {}, ""
        t0 = time.time()
        res = git_try(root, "log", "--raw", "--no-abbrev", "--no-renames", "-m", "--format=", trunk, "--", ".agi/nodes")
        if res.returncode != 0:
            self.problem = f"git log {trunk} -- .agi/nodes failed rc {res.returncode}: {(res.stderr.strip().splitlines() or ['no reason'])[0][:120]}"
            return
        for blobs in _raw_blobs(res.stdout).values():
            self.nodes |= blobs
        if not self.nodes:
            self.problem = f"git log {trunk} -- .agi/nodes yielded 0 blobs"
            return
        self.cost = (f"{len(self.nodes)} blobs at .agi/nodes paths of {trunk}, one walk, {time.time() - t0:.1f} s, "
                     f"git child peak RSS {resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss // 1024} MB")

    def at_path(self, path: str) -> set[str] | None:
        """Blobs ever at `path` on the trunk (cached); None when git could not say or the path is not a plain repo path."""
        if not _PAYLOAD_REF_RE.fullmatch(path) or not path.strip("./") or any(seg in ("", ".", "..") for seg in path.split("/")):
            return None
        if path not in self._paths:
            res = git_try(self.root, "log", "--raw", "--no-abbrev", "--no-renames", "-m", "--format=", self.trunk, "--", path)
            self._paths[path] = None if res.returncode != 0 else {b for bs in _raw_blobs(res.stdout).values() for b in bs}
        return self._paths[path]


def _live_seen(root: Path, tip: str) -> dict[str, set[str]] | None:
    """{path: {blob}} the live ref's WHOLE history held (merges included), or None when git could not say."""
    res = git_try(root, "log", "--raw", "--no-abbrev", "--no-renames", "-m", "--format=", tip)
    return _raw_blobs(res.stdout) if res.returncode == 0 else None


def _payload_ref(root: Path, *tips: str) -> str | None:
    """`payload_ref:` from the first tip whose node.md frontmatter has one (origin's first, then live's); None when neither is readable."""
    for tip in tips:
        res = git_try(root, "show", f"{tip}:node.md")
        if res.returncode != 0:
            continue
        seen_fence = 0
        for line in res.stdout.splitlines():
            if line.strip() == "---":
                seen_fence += 1
                if seen_fence == 2:
                    break
            elif seen_fence == 1 and line.startswith("payload_ref:"):
                ref = line.split(":", 1)[1].strip().strip("\"'")
                if ref:
                    return ref
    return None


def _unrelated_class(root: Path, otip: str, live: str, seen: "_TrunkSeen | None") -> tuple[str | None, str]:
    """(class, why) of a diverged origin pair (origin tip `otip`, live tip `live`) whose trees differ. class is `live-seen` / `trunk-seen`
    (tree = LIVE may be written), None (stays a CONFLICT; `why` says which condition), or "unread" (git could not say).
    (1) NO merge-base; (2) EVERY blob of origin's tip tree was SEEN at its own path class: `node.md` in the node's own live grid history OR at an
    `.agi/nodes` path in the trunk's history; `payload` in the node's own live grid history OR at that node's `payload_ref` path in the trunk's
    history (a `payload_ref` that cannot be read -> CONFLICT, named); any other path -> CONFLICT. `trunk-seen` = at least one blob needed the
    trunk, else `live-seen`. Judged per pair, at write time, from the bytes in front of it, never from a precomputed list and never from a date."""
    mb = git_try(root, "merge-base", otip, live)
    if mb.returncode == 0 and mb.stdout.strip():
        return None, "has a merge-base"
    if mb.returncode not in (0, 1):
        return "unread", "merge-base unread"
    if seen is None or seen.problem:
        return None, f"trunk blob set unread: {seen.problem if seen else 'no trunk'}"
    tree = git_try(root, "ls-tree", "-r", otip)
    ours = _live_seen(root, live)
    if tree.returncode != 0 or ours is None:
        return "unread", "tree / live history unread"
    absent, used_trunk, ref = [], False, None
    for line in tree.stdout.splitlines():
        meta, _, path = line.partition("\t")
        blob = meta.split()[-1]
        if blob in ours.get(path, ()):
            continue
        if path == "node.md" and blob in seen.nodes:
            used_trunk = True
        elif path == "payload":
            ref = ref or _payload_ref(root, otip, live)
            if ref is None:
                return None, "payload_ref unreadable"
            at = seen.at_path(ref)
            if at is None:
                return None, f"payload_ref {ref} unreadable (not a plain repo path, or its walk failed)"
            if blob in at:
                used_trunk = True
            else:
                absent.append(f"payload@{ref}")
        else:
            absent.append(path)
    if absent:
        return None, "bytes unseen: " + ", ".join(absent)
    return ("trunk-seen" if used_trunk else "live-seen"), ""


def _cas(root: Path, ref: str, new: str, old: str) -> bool:
    """The ONE ref write of `unify`: compare-and-swap (old "" = the ref must not exist). Never a delete."""
    return git_try(root, "update-ref", ref, new, old).returncode == 0


def _unify_dir(root: Path) -> Path:
    """Where `unify --write` keeps its own pre-write snapshots (scratch, never versioned, one dir for
    every worktree like the grid lock)."""
    base = locations.shared_sessions_dir(root) if locations.is_graph_dir(root) else root / ".agi" / "sessions"
    return base / "unify"


class _Snapshot:
    """R2: `unify --write` records `for-each-ref <ns>/node` ITSELF, under the lock, immediately before its
    FIRST compare-and-swap (so it is the state the write starts from), into a file that is created
    exclusively and never overwritten. A run that writes nothing leaves no file. `--check` trusts only the
    EARLIEST such file: a caller-supplied or late file cannot make the old-tip half of the check vacuous."""

    def __init__(self, root: Path, ns: str, write: bool) -> None:
        self.root, self.ns, self.write, self.path = root, ns, write, None

    def ensure(self) -> None:
        if not self.write or self.path is not None:
            return
        listing = git(self.root, "for-each-ref", f"{self.ns}/node", "--format=%(refname) %(objectname)")
        d = _unify_dir(self.root)
        d.mkdir(parents=True, exist_ok=True)
        stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        n = 0
        while True:
            path = d / f"{stamp}-{os.getpid()}-{n}.refs"
            try:
                with open(path, "x") as f:    # 'x': never overwrites a snapshot
                    f.write(listing + "\n")
                break
            except FileExistsError:
                n += 1
        self.path = path
        print(f"grid unify: pre-write snapshot {path.name} ({len(listing.splitlines())} refs, in {d.name}/)")


def _unify_one(root: Path, ns: str, lns: str, mint: str, write: bool, snap: _Snapshot, classes: list | None = None,
               seen: "_TrunkSeen | None" = None) -> str:
    """One mint of `cmd_unify`: merge the read-only `lns` tip into `ns`. Returns
    merged | adopted | unchanged | conflict | unread. Every ref write goes through `_cas`
    (a compare-and-swap); there is no delete anywhere in this verb.

    The merged tree is the LEGACY side's, which is right for the writer's own old namespace (the live side
    wins by construction). For `ORIGIN_SNAP_NS` (a second writer's history) it is NEVER an automatic pick: a
    diverged pair merges only when the two tips' trees are EQUAL, and is a CONFLICT otherwise (origin has
    versions after the merge-base that this namespace does not carry), listed by mint, nothing written. The ONE
    narrow exception (goal:g7.16.1.11.46.16, council 14:21:47Z, condition (2) a BYTE TEST since alive's 14:53:03Z [correction]):
    `_unrelated_class` -- a pair with NO merge-base whose origin tip's blobs were ALL seen (live's own history, or the trunk's, each at its
    own path class) gets a 2-parent commit, tree = LIVE (never origin's), first parent the live tip, origin's tip the second. A pair
    that fails the byte test is a CONFLICT and, when it failed on unseen bytes, is BANKED (a `banked` row in `classes`, the reason as its
    4th field) for the owner's one batch look. `classes`, when given, collects (class, mint, origin tip, written commit | reason)."""
    lref, nref = f"{lns}/node/{mint}", f"{ns}/node/{mint}"
    ltip, ntip = ref_tip(root, lref), ref_tip(root, nref)
    if ltip is None:
        return "unread"
    if ntip == ltip:
        return "unchanged"
    if ntip is None:
        if write:
            snap.ensure()
            if not _cas(root, nref, ltip, ""):
                return "conflict"
        return "adopted"
    live_in_new = _is_ancestor(root, ltip, ntip)
    new_in_live = _is_ancestor(root, ntip, ltip)
    if live_in_new is None or new_in_live is None:
        return "unread"
    if live_in_new:
        return "unchanged"
    if new_in_live:    # the frozen side is already inside the live history: a fast-forward
        if write:
            snap.ensure()
            if not _cas(root, nref, ltip, ntip):
                return "conflict"
        return "adopted"
    if lns == ORIGIN_SNAP_NS and git(root, "rev-parse", f"{ltip}^{{tree}}", check=False) != git(
            root, "rev-parse", f"{ntip}^{{tree}}", check=False):
        sub, why = _unrelated_class(root, ltip, ntip, seen)
        if sub == "unread":
            return "unread"
        if sub is None:
            if classes is not None and (why.startswith("bytes unseen") or why.startswith("payload_ref")):
                classes.append(("banked", mint, ltip, why))
            return "conflict"    # an origin-side edit after the base, or bytes nobody saw: never an automatic tree pick
        if write:
            # immediately before the write: this pair's own two tips are still the ones judged; the whole QUIET verdict is re-read on the cadence above
            if ref_tip(root, lref) != ltip or ref_tip(root, nref) != ntip:
                return "conflict"
            if (classes is None or sum(1 for c in classes if c[0].startswith("unrelated-root/")) % UNRELATED_QUIET_EVERY == 0) and _origin_quiet(root):
                return "unread"
            snap.ensure()
            n = int(git(root, "rev-list", "--count", "--first-parent", ntip)) + 1
            msg = (f"unify v{n} {mint}\n\nUnify-Unrelated: {ltip}\nUnify-Class: unrelated-root/{sub}\n")
            res = git_try(root, "commit-tree", f"{ntip}^{{tree}}", "-p", ntip, "-p", ltip, "-m", msg)
            if res.returncode != 0 or not _cas(root, nref, res.stdout.strip(), ntip):
                return "conflict"
            if classes is not None:
                classes.append((f"unrelated-root/{sub}", mint, ltip, res.stdout.strip()))
        elif classes is not None:
            classes.append((f"unrelated-root/{sub}", mint, ltip, ""))
        return "merged"
    if write:
        snap.ensure()
        n = int(git(root, "rev-list", "--count", "--first-parent", ltip)) + 1
        # tree = the LIVE side's tree; first parent = the live tip, so `--first-parent` versions keep counting the live chain;
        # the Unify-Frozen trailer records the new-namespace tip this merge took in (what `--check` asserts against the snapshot)
        msg = f"unify v{n} {mint}\n\nUnify-Live: {ltip}\nUnify-Frozen: {ntip}\n"
        res = git_try(root, "commit-tree", f"{ltip}^{{tree}}", "-p", ltip, "-p", ntip, "-m", msg)
        if res.returncode != 0 or not _cas(root, nref, res.stdout.strip(), ntip):
            return "conflict"
        if classes is not None:
            classes.append(("tree-equal", mint, ltip, res.stdout.strip()))
    elif classes is not None:
        classes.append(("tree-equal", mint, ltip, ""))
    return "merged"


def _unify_check(root: Path, ns: str, lns: str, mints: list[str], before: dict[str, str],
                 seen: "_TrunkSeen | None" = None, owner: "_OwnerView | None" = None) -> tuple[int, list[str]]:
    """The per-mint falsifier of G1a-T, read-only. `before` is the verb's OWN earliest pre-write snapshot.
    Per mint: the live tip and the snapshot's old tip are ancestors of the new tip, `rev-list --count` new
    >= max(old), and the merge commit that took the live tip as its first parent (a) carries the live tip's
    tree and (b) records `Unify-Frozen: T` with T != the current tip, T its second parent, and the snapshot
    tip equal to T or an ancestor of T (a later delta merge records the earlier merge, which holds it)."""
    good, bad = 0, []
    for m in mints:
        ltip, ntip = ref_tip(root, f"{lns}/node/{m}"), ref_tip(root, f"{ns}/node/{m}")
        otip = before.get(m)
        if not ltip or not ntip:
            bad.append(f"{m} (a ref is missing)")
            continue
        ancestors = [_is_ancestor(root, t, ntip) for t in (ltip, otip) if t]
        counts = [git_try(root, "rev-list", "--count", t) for t in (ltip, otip, ntip) if t]
        if any(a is not True for a in ancestors) or any(c.returncode != 0 for c in counts):
            bad.append(f"{m} (an old tip is not an ancestor of the new tip)")
            continue
        c = [int(x.stdout) for x in counts]
        if c[-1] < max(c[:-1]):
            bad.append(f"{m} (fewer commits than an old side)")
            continue
        if ntip == ltip or otip is None:    # adopted: no merge commit; an old tip, if any, is inside the live history (checked above)
            good += 1                       # (otip None: no ref before the write, so nothing to preserve beyond the live tip)
            continue
        live_tips = [x.split(":", 1)[1].strip() for x in git_try(root, "log", "--format=%B", ntip).stdout.splitlines()
                     if x.startswith("Unify-Live:")]
        if _is_ancestor(root, ltip, otip) is True and not any(
                x.startswith("Unify-Live:") for x in git_try(root, "log", "--format=%B", otip).stdout.splitlines()):
            good += 1    # the live tip was already inside the pre-write tip (nothing to merge): sound ONLY while the snapshot
            continue     # is early, so a pre-write tip that already carries a unify merge (a late snapshot) never takes this exit
        if lns == ORIGIN_SNAP_NS:
            why = _check_unrelated(root, ltip, ntip, seen, owner)
            if why is None:
                good += 1
                continue
            if why:
                bad.append(f"{m} ({why})")
                continue
        merge = None
        # first-parent first (the merge this namespace took last); then the whole history: a LATER namespace's
        # merge (the third history) sits on top and holds this one as its second parent
        for walk in (("--first-parent",), ()):
            for line in git_try(root, "rev-list", *walk, "--parents", ntip).stdout.splitlines():
                parts = line.split()
                if len(parts) > 2 and parts[1] == ltip:
                    merge, second = parts[0], parts[2]
                    break
            if merge is not None:
                break
        if merge is None:
            # another namespace's merge may already hold this tip: a unify merge of ANOTHER live tip L' in the history with
            # this tip inside L' (L' != the tip itself, so a merge that dropped its own parent never covers itself)
            if any(lt != ltip and _is_ancestor(root, ltip, lt) is True for lt in live_tips):
                good += 1
                continue
            bad.append(f"{m} (no merge commit takes the live tip as its first parent)")
            continue
        if git(root, "rev-parse", f"{merge}^{{tree}}", check=False) != git(root, "rev-parse", f"{ltip}^{{tree}}", check=False):
            bad.append(f"{m} (the merge does not carry the live tree)")
            continue
        trailer = next((x.split(":", 1)[1].strip() for x in git(root, "log", "-1", "--format=%B", merge).splitlines()
                        if x.startswith("Unify-Frozen:")), None)
        if trailer is None or trailer == ntip or trailer != second:
            bad.append(f"{m} (the Unify-Frozen trailer is missing, is the current tip, or is not the second parent)")
            continue
        if otip and otip != trailer and _is_ancestor(root, otip, trailer) is not True:
            bad.append(f"{m} (the snapshot tip is not the trailer's tip or inside it)")
            continue
        good += 1
    return good, bad


def _set_unify_namespaces(into: str | None, legacy: list[str] | None) -> bool:
    """`unify --into/--legacy`: name the namespaces on the command line, so the merge can run BEFORE the
    config that declares them lands (the writer is still on the old namespace then). Returns False when
    set; a name outside refs/grid prints `unread` and exits 1."""
    global REF_NS, LEGACY_NS
    for ns in [x for x in [into, *(legacy or [])] if x is not None]:
        if not ns.strip().rstrip("/").startswith("refs/grid"):
            print(f"grid unify: unread (namespace {ns!r} is not under refs/grid)")
            sys.exit(1)
    if into:
        REF_NS = into.strip().rstrip("/")
    if legacy:
        LEGACY_NS = [x.strip().rstrip("/") for x in legacy if x.strip().rstrip("/") != REF_NS]
    return False


def _class_line(counts: "Counter[str]") -> str:
    """`classes: tree-equal K, unrelated-root tree=live N (origin bytes in live's history X, in the trunk's Y), banked B` -- the ONE line
    `unify` and `--check` print (banked = the pairs the byte test left CONFLICT on unseen bytes, for the owner's one batch look)."""
    x, y = counts.get("unrelated-root/live-seen", 0), counts.get("unrelated-root/trunk-seen", 0)
    return (f"classes: tree-equal {counts.get('tree-equal', 0)}, unrelated-root tree=live {x + y} "
            f"(origin bytes in live's history {x}, in the trunk's {y}), banked {counts.get('banked', 0)}"
            + (f", owner-batch tree=live {counts['owner-batch/live']}" if counts.get("owner-batch/live") else ""))


def _write_class_record(root: Path, ns: str, classes: list[tuple[str, str, str, str]]) -> str:
    """The stamped record of one `unify --write`: a line per merged mint, `<class> <mint> <origin tip> <written commit>`, and a `banked` line per pair
    the byte test left CONFLICT on unseen bytes (`banked <mint> <origin tip> <reason>`), created exclusively (never overwritten), under `_unify_dir` with the
    suffix `.classes` (`--check` reads `*.refs` as snapshots and `*.classes` as records). The banked pairs also get a `.batch` file beside it: per mint the
    reason and the DIFF of origin's node.md against live's (<= 150 lines), the one batch the owner / a reader looks at."""
    d = _unify_dir(root)
    d.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    n = 0
    while True:
        path = d / f"{stamp}-{os.getpid()}-{n}.classes"
        try:
            with open(path, "x") as f:
                f.write("".join(f"{c} {m} {o} {w}\n" for c, m, o, w in sorted(classes)))
            break
        except FileExistsError:
            n += 1
    banked = sorted(c for c in classes if c[0] == "banked")
    if banked:
        with open(path.with_suffix(".batch"), "x") as f:
            for _, m, o, why in banked:
                live = ref_tip(root, f"{ns}/node/{m}") or ""
                diff = git_try(root, "diff", "--no-color", f"{live}:node.md", f"{o}:node.md").stdout.splitlines()
                f.write(f"== {m} origin {o} live {live}\n   {why}\n" + "".join(f"   {x}\n" for x in diff[:150])
                        + (f"   ... {len(diff) - 150} more diff lines\n" if len(diff) > 150 else ""))
    return path.name + (f" + {path.with_suffix('.batch').name}" if banked else "")


def _home_added(root: Path, first: str, merge: str) -> bool | None:
    """Did `merge` ADD a home-path literal (anonymize.HOME_PATH_RE) against its first parent? `git diff first merge` is empty when the trees are equal.
    None = git could not say (a failed diff is NOT an empty one: it must never read as 'no literal')."""
    res = git_try(root, "diff", "--no-color", "-U0", first, merge)
    if res.returncode != 0:
        return None
    return any(x.startswith("+") and not x.startswith("+++") and anonymize.HOME_PATH_RE.search(x) for x in res.stdout.splitlines())


def _tree_sha(root: Path, rev: str) -> str | None:
    """`<rev>^{tree}` as a 40-hex sha, or None when git could not say (`git(..., check=False)` would return "" and two unreadable trees would compare equal)."""
    res = git_try(root, "rev-parse", "--verify", "-q", f"{rev}^{{tree}}")
    sha = res.stdout.strip()
    return sha if res.returncode == 0 and re.fullmatch(r"[0-9a-f]{40}", sha) else None


def _check_unrelated(root: Path, ltip: str, ntip: str, seen: "_TrunkSeen | None",
                     owner: "_OwnerView | None" = None) -> str | None:
    """`--check` for a pair `_unify_one` merged as an UNRELATED ROOT: None = sound, "" = this pair is not one (fall through to the ordinary
    check), else why it is RED. The merge is found by its SECOND parent (origin's tip) and its `Unify-Unrelated` trailer; it must carry the tree of
    its FIRST parent (the live tip it took in), and the class is judged AGAIN on that first parent (origin's tip is inside ntip's history now, so
    the live tip itself would read `live-seen` for everything)."""
    for line in git_try(root, "rev-list", "--parents", ntip).stdout.splitlines():
        parts = line.split()
        if len(parts) != 3 or parts[2] != ltip:
            continue
        merge, first = parts[0], parts[1]
        body = git(root, "log", "-1", "--format=%B", merge, check=False)
        by_owner = f"Unify-Owner: {ltip}" in body.splitlines()
        if f"Unify-Unrelated: {ltip}" not in body.splitlines() and not by_owner:
            continue
        # the home-path count is over what the merge ADDED against its first parent (empty when the trees are equal): a live tip that already carries a
        # literal merges as tree = LIVE and must read GREEN; the count is computed even when the tree check is RED (the tree = ORIGIN mutant reads RED twice)
        added = _home_added(root, first, merge)
        mtree, ftree = _tree_sha(root, merge), _tree_sha(root, first)
        if added is None:    # FAIL CLOSED: an unreadable diff / tree is a RED of its own, never the GREEN of an empty answer
            return "home check unread (git diff failed)"
        if mtree is None or ftree is None:
            return "tree unread"
        if mtree != ftree:
            return "the unrelated-root merge does not carry the live tree" + ("; a written tip carries a home-path literal" if added else "")
        if added:
            return "a written tip carries a home-path literal"
        if by_owner:    # the owner's ruling, not the byte test: every link of the chain is its own RED (goal:g7.16.1.11.46.16.2 R2)
            rec = next((x.split(":", 1)[1].strip() for x in body.splitlines() if x.startswith("Unify-Record:")), "")
            if owner is None or (ltip, merge) not in owner.rows:
                return "an owner-batch merge no stamped owner-batch record names"
            if (rec, ltip) not in owner.banked:
                return f"an owner-batch merge for an origin tip its record {rec or '(no Unify-Record)'} did not bank"
            if owner.rulings is None:
                return f"owner rulings unread at {owner.trunk}"
            if rec not in owner.rulings:
                return f"an owner-batch merge under a record no owner ruling names ({rec})"
            if owner.rulings[rec] is None:
                return f"an owner-batch merge under a record whose rulings pin different bytes ({rec})"
            if owner.sha.get(rec) != owner.rulings[rec]:
                return f"an owner-batch merge under a record that is not the bytes the owner ruled ({rec})"
            return None
        cls, why = _unrelated_class(root, ltip, first, seen)
        if cls in (None, "unread"):
            return f"the unrelated-root merge is outside the class ({why})"
        return None
    return ""


#: the class an owner-batch write records (`_write_class_record`), and the trailer `--check` knows it by (`_check_unrelated`)
OWNER_CLASS = "owner-batch/live"


#: the ONE line an owner ruling carries (goal:g7.16.1.11.46.16.2 R1), at column 0 of a doc node under .agi/nodes/doc: `owner-batch-ruling: <record>`
RULING_KEY = "owner-batch-ruling"


#: a ruling is a doc node BY NAME: a card, a review or a THOUGHT that quotes the line is not one (self-perpetuating 21:36:33Z 10-27)
RULING_GLOB = ":(glob).agi/nodes/doc/owner-ruling-*.md"    # the GATE's own literal (land.rules_paths): `*` never crosses `/`


def _owner_rulings(root: Path, trunk: str) -> dict[str, str | None] | None:
    """{record: the sha256 its ruling PINS} of every record an owner RULED, read from a COMMIT: the anchored two-token line
    `^owner-batch-ruling: <record> sha256:<64 hex>$` in a ruling node BY NAME (`RULING_GLOB`) in the TREE of `trunk` (a signed land carries it),
    never the working tree and never the sessions dir, so a file dropped on the box rules nothing. Each ruling node names ONE record (a node with
    two such lines rules none); two ruling nodes that pin ONE record to DIFFERENT bytes map it to None (they disagree: unread by name, never "any
    one matches"). None = git could not say."""
    res = git_try(root, "grep", "-E", f"^{RULING_KEY}: [^ ]+ sha256:[0-9a-f]{{64}}$", trunk, "--", RULING_GLOB)
    if res.returncode == 1:
        return {}
    if res.returncode != 0:
        return None
    per: dict[str, list[str]] = {}
    for x in res.stdout.splitlines():    # `<trunk>:<path>:<line>`
        path, _, line = x[len(trunk) + 1:].partition(f":{RULING_KEY}: ")
        per.setdefault(path, []).append(line.strip())
    out: dict[str, str | None] = {}
    for v in per.values():
        if len(v) != 1:
            continue
        rec, sha = v[0].split(" sha256:")
        out[rec] = sha if out.get(rec, sha) == sha else None
    return out


def _read_record(path: Path) -> tuple[str, list[list[str]]] | None:
    """ONE read of a stamped record: (sha256 of its bytes, its rows) from the SAME buffer, so an append between a hash and a second open cannot
    slip past the ruling's pin. None = unreadable."""
    import hashlib
    try:
        data = path.read_bytes()
    except OSError:
        return None
    return hashlib.sha256(data).hexdigest(), [x.split() for x in data.decode("utf-8", "replace").splitlines()]


class _OwnerView:
    """What `--check` judges an `Unify-Owner` merge against: the stamped owner rows {(origin tip, merge)}, the {(record, origin tip)} each
    stamped record BANKED (keyed BY RECORD, never pooled: alive 22:47:08Z), each record's sha256 as read, and the records an owner ruled at
    `trunk` with the bytes each ruling pins (None = unread)."""

    def __init__(self, root: Path, trunk: str) -> None:
        self.banked, self.rows, self.sha = set(), set(), {}
        for rec in sorted(_unify_dir(root).glob("*.classes")):
            got = _read_record(rec)
            if got is None:
                continue
            self.sha[rec.name] = got[0]
            for r in got[1]:
                if len(r) >= 3 and r[0] == "banked":
                    self.banked.add((rec.name, r[2]))
                elif len(r) == 4 and r[0] == OWNER_CLASS:
                    self.rows.add((r[2], r[3]))
        self.trunk, self.rulings = trunk, _owner_rulings(root, trunk)


class _OwnerStamp:
    """The stamped record of ONE `--owner-batch --write`, written PER ROW: the `.classes` file (and its `.batch`) is created exclusively at the
    first write and each pair is APPENDED (flushed + fsynced) right after its compare-and-swap, so a run that dies between two pairs (a raise,
    a power loss) leaves every written merge stamped. The `.batch` entry is `git diff <live tip> <origin tip>` over EVERY path, uncapped: it is
    where origin's version is SAVED (the owner's words); a diff git cannot read is ONE named `diff unread: <reason>` line, never an empty body."""

    def __init__(self, root: Path) -> None:
        self.root, self.path = root, None

    def _open(self) -> None:
        d = _unify_dir(self.root)
        d.mkdir(parents=True, exist_ok=True)
        stamp = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
        n = 0
        while True:
            path = d / f"{stamp}-{os.getpid()}-{n}.classes"
            try:
                with open(path, "x"), open(path.with_suffix(".batch"), "x"):
                    pass
                break
            except FileExistsError:
                n += 1
        self.path = path

    def add(self, mint: str, live: str, otip: str, commit: str) -> None:
        if self.path is None:
            self._open()
        res = git_try(self.root, "diff", "--no-color", "--binary", live, otip)    # --binary: a binary path is SAVED, not 'Binary files differ'
        body = (res.stdout.splitlines() if res.returncode == 0 else
                [f"diff unread: {(res.stderr.strip().splitlines() or ['git diff rc ' + str(res.returncode)])[0]}"])
        if not body:    # read, and printed nothing: say so, never an empty body
            body = ["diff empty: trees equal"]
        for path, text in ((self.path.with_suffix(".batch"), f"== {mint} origin {otip} live {live}\n   owner rule: tree = LIVE, origin's tip kept "
                            f"as the 2nd parent of {commit}\n" + "".join(f"   {x}\n" for x in body)),
                           (self.path, f"{OWNER_CLASS} {mint} {otip} {commit}\n")):
            with open(path, "a") as f:
                f.write(text)
                f.flush()
                os.fsync(f.fileno())


def _unify_owner_batch(root: Path, ns: str, record: str, write: bool, trunk: str = "HEAD") -> int:
    """goal:g7.16.1.11.46.16, the OWNER's ruling of the banked batch (10-27, belam relaying the owner: "Sounds good" to "keep the live
    version for all 40 and save origin's differing version in a stamped record"): the SELECTOR is the `banked` rows of ONE stamped record
    `<record>` (a `.classes` file under `_unify_dir`, by name). Per selected mint: origin's tip must still be the one the record banked
    (moved = CONFLICT, named), and the pair is written as ONE two-parent commit, tree = LIVE, first parent the live tip, origin's tip the
    second (`Unify-Owner: <origin tip>`), by `_cas`: the push of it is a fast-forward of origin's ref, never a force, and origin's version
    stays in the history. A pair already holding origin's tip is unchanged; one git cannot read is UNREAD, named, never skipped. `--write`
    needs the QUIET verdict and the grid lock, like every origin write; `_OwnerStamp` stamps each written pair right after its
    compare-and-swap (`owner-batch/live` rows) with origin's full diff in the `.batch` beside it. Dry-run unless `--write`."""
    if "/" in record or not record.endswith(".classes") or not (_unify_dir(root) / record).is_file():
        print(f"grid unify: unread (--owner-batch names no stamped record: {record!r}; a `.classes` file name under {_unify_dir(root).name}/)")
        return 1
    got = _read_record(_unify_dir(root) / record)    # ONE read: the hash the ruling pins and the rows selected come from the same bytes
    if got is None:
        print(f"grid unify: unread (record {record} cannot be read)")
        return 1
    sha, rows = got
    picked = [(r[1], r[2]) for r in rows if len(r) >= 3 and r[0] == "banked"]
    if not picked:
        print(f"grid unify: unread (record {record} banks no pair)")
        return 1
    rulings = _owner_rulings(root, trunk)    # goal:g7.16.1.11.46.16.2 R1: only a record an owner RULED, read from the trunk's commit
    if rulings is None or record not in rulings:
        print(f"grid unify: unread ({'owner rulings unread' if rulings is None else 'no owner ruling names ' + record} at {trunk}; "
              f"a ruling is ONE `{RULING_KEY}: <record> sha256:<hex>` line in a {RULING_GLOB} node the trunk carries)")
        return 1
    if rulings[record] is None:
        print(f"grid unify: unread (the rulings for {record} at {trunk} pin different bytes)")
        return 1
    if rulings[record] != sha:
        print(f"grid unify: unread (record {record} is not the bytes the owner ruled at {trunk}: sha256 {sha[:16]} != {rulings[record][:16]})")
        return 1
    if write:
        why = _origin_quiet(root)
        if why:
            print(f"grid unify: unread ({ORIGIN_SNAP_NS} is not QUIET: {why})")
            return 1
    lock = None
    if write:
        lock = GridLock(root, 120)
        lock.acquire()
    tally = {"merged": 0, "unchanged": 0, "conflict": 0, "unread": 0}
    named: list[str] = []
    stamp = _OwnerStamp(root)
    try:
        snap = _Snapshot(root, ns, write)
        for mint, want in picked:
            oref, nref = f"{ORIGIN_SNAP_NS}/node/{mint}", f"{ns}/node/{mint}"
            otip, ntip = ref_tip(root, oref), ref_tip(root, nref)
            held = _is_ancestor(root, otip, ntip) if otip and ntip else None
            ltree = _tree_sha(root, ntip) if ntip else None
            if otip is None or ntip is None or held is None or ltree is None:
                tally["unread"] += 1
                named.append(f"  UNREAD {mint} (a ref, an ancestry or the live tree cannot be read: origin {otip or '-'}, live {ntip or '-'})")
                continue
            if otip != want:
                tally["conflict"] += 1
                named.append(f"  CONFLICT {mint} (origin moved since the record banked it: {want} -> {otip}; nothing written)")
                continue
            if held:
                tally["unchanged"] += 1
                continue
            if write:
                snap.ensure()
                n = int(git(root, "rev-list", "--count", "--first-parent", ntip)) + 1
                msg = f"unify v{n} {mint}\n\nUnify-Owner: {otip}\nUnify-Class: {OWNER_CLASS}\nUnify-Record: {record}\n"
                res = git_try(root, "commit-tree", ltree, "-p", ntip, "-p", otip, "-m", msg)
                if res.returncode != 0:
                    tally["unread"] += 1
                    named.append(f"  UNREAD {mint} (the merge commit could not be built: {(res.stderr.strip().splitlines() or ['rc ' + str(res.returncode)])[0]}; nothing written)")
                    continue
                if not _cas(root, nref, res.stdout.strip(), ntip):
                    tally["conflict"] += 1
                    named.append(f"  CONFLICT {mint} (a lost compare-and-swap; nothing written)")
                    continue
                stamp.add(mint, ntip, otip, res.stdout.strip())    # stamped NOW: a death before the next pair leaves this one recorded
            tally["merged"] += 1
        print(f"grid unify ({'write' if write else 'dry-run'}) --owner-batch {record}: selected {len(picked)} banked pair(s): "
              + ", ".join(f"{v} {k}" for k, v in tally.items()) + " (tree = LIVE, origin's tip the 2nd parent)")
        if stamp.path is not None:
            print(f"grid unify: record {stamp.path.name} + {stamp.path.with_suffix('.batch').name} (the owner-batch rows, each stamped after its "
                  f"compare-and-swap; origin's full diff per mint)")
        for line in named:
            print(line)
    finally:
        if lock is not None:
            lock.release()
    return 1 if tally["conflict"] or tally["unread"] else 0


def cmd_unify(root: Path, write: bool, check: bool = False, trunk: str = "HEAD", owner_batch: str | None = None) -> int:
    """goal:g7.16.1.11.46.16 G1a: ONE namespace, written ADDITIVELY. Words: LEGACY = `refs/grid/local-maxxing`,
    the namespace every writer used until this land (6025 refs, live until then); `refs/grid/node` = the 09-21
    FREEZE (3807 refs), which becomes the one namespace. For every mint in each read-only legacy namespace
    (config `grid.legacy_namespaces`), make `<REF_NS>/node/<mint>`'s history include the legacy tip: a mint
    with no ref there points at the legacy tip; a mint whose ref is inside the legacy history fast-forwards;
    a diverged pair gets ONE two-parent merge whose tree is the LEGACY (current) side's tree, first parent the
    legacy tip, with an `Unify-Frozen: <old tip>` trailer. No ref is ever deleted and the legacy refs are only
    read. Dry-run unless `--write`; idempotent; `--write` takes the commit-all flock and writes its OWN
    pre-write snapshot (path printed) before its first compare-and-swap. `--check` is the read-only falsifier:
    it reads only the EARLIEST such snapshot and prints `unified m/m` (rc 0 only when every mint passes and
    m > 0); anything unreadable prints `unread` and returns 1."""
    ensure_repo(root)
    ns = REF_NS
    problem = legacy_config_problem(root)
    if problem:
        print(f"grid unify: unread ({problem})")
        return 1
    if not LEGACY_NS:
        print("grid unify: unread (grid.legacy_namespaces names no read-only namespace)")
        return 1
    listing = {}
    for lns in LEGACY_NS:
        res = git_try(root, "for-each-ref", f"{lns}/node", "--format=%(refname)")
        names = [x[len(lns) + 6:] for x in res.stdout.splitlines() if x.startswith(f"{lns}/node/")]
        if res.returncode != 0 or not names:
            print(f"grid unify: unread ({lns} lists no node refs)")
            return 1
        listing[lns] = sorted(names)
    if owner_batch is not None:
        if check or ORIGIN_SNAP_NS not in listing:
            print(f"grid unify: unread (--owner-batch reads {ORIGIN_SNAP_NS} only, and never with --check)")
            return 1
        return _unify_owner_batch(root, ns, owner_batch, write, trunk)
    if check:
        snaps = sorted(_unify_dir(root).glob("*.refs"))
        if not snaps:
            print("grid unify: unread (no pre-write snapshot: `unify --write` has not run here)")
            return 1
        before = {}
        for line in snaps[0].read_text().splitlines():
            parts = line.split()
            if len(parts) == 2 and parts[0].startswith(f"{ns}/node/") and re.fullmatch(r"[0-9a-f]{40}", parts[1]):
                before[parts[0][len(ns) + 6:]] = parts[1]
        if not before:    # an empty snapshot would make the old-tip half of the check vacuous
            print(f"grid unify: unread (snapshot {snaps[0].name} lists no {ns}/node ref)")
            return 1
        print(f"grid unify check: snapshot {snaps[0].name} ({len(before)} refs)")
        rc = 0
        bad_mints: set[str] = set()
        seen = _TrunkSeen(root, trunk) if ORIGIN_SNAP_NS in listing else None
        owner = _OwnerView(root, trunk)
        for lns, names in listing.items():
            good, bad = _unify_check(root, ns, lns, names, before, seen, owner)
            print(f"grid unify check: unified {good}/{len(names)} ({lns} -> {ns})")
            if lns == ORIGIN_SNAP_NS:
                recs = Counter()
                for rec in sorted(_unify_dir(root).glob("*.classes")):
                    recs.update(x.split(" ", 1)[0] for x in rec.read_text().splitlines() if x.strip())
                print(f"grid unify check: {_class_line(recs)} (from the stamped record{'s' if len(list(_unify_dir(root).glob('*.classes'))) != 1 else ''})")
                print(f"grid unify check: anonymize over the written tips: {sum('home-path literal' in b for b in bad)} carry a home-path literal")
            for b in bad[:10]:
                print(f"  RED {b}")
            bad_mints.update(b.split()[0] for b in bad)
            rc = rc or (0 if good == len(names) else 1)
        if len(listing) > 1:    # the UNION of every namespace's names, never the first one alone
            union = set().union(*listing.values())
            print(f"grid unify check: unified {len(union) - len(bad_mints & union)}/{len(union)} "
                  f"(union of {len(listing)} namespaces -> {ns})")
            rc = rc or (1 if bad_mints & union else 0)
        return rc
    if write and ORIGIN_SNAP_NS in listing:
        why = _origin_quiet(root)
        if why:    # a one-shot merge cannot settle a two-writer namespace: only a QUIET lap opens the write
            print(f"grid unify: unread ({ORIGIN_SNAP_NS} is not QUIET: {why})")
            return 1
    lock = None
    if write:
        lock = GridLock(root, 120)
        lock.acquire()
    try:
        snap = _Snapshot(root, ns, write)
        total: dict[str, int] = {}
        seen = _TrunkSeen(root, trunk) if ORIGIN_SNAP_NS in listing else None
        if seen is not None:    # ONE walk per run, its cost quoted; a failed / empty walk makes every unrelated-root pair a CONFLICT
            print(f"grid unify: trunk blob set unread: {seen.problem} (every unrelated-root pair stays CONFLICT)" if seen.problem
                  else f"grid unify: trunk blob set: {seen.cost}")
        for lns, names in listing.items():
            tally = {"merged": 0, "adopted": 0, "unchanged": 0, "conflict": 0, "unread": 0}
            conflicts: list[str] = []
            classes: list[tuple[str, str, str, str]] = []
            for m in names:
                got = _unify_one(root, ns, lns, m, write, snap, classes, seen)
                tally[got] += 1
                if got == "conflict":
                    conflicts.append(m)
            for k, v in tally.items():
                total[k] = total.get(k, 0) + v
            print(f"grid unify ({'write' if write else 'dry-run'}): {lns} -> {ns}: "
                  + ", ".join(f"{v} {k}" for k, v in tally.items()) + f" of {len(names)}")
            if lns == ORIGIN_SNAP_NS:
                print(f"grid unify ({'write' if write else 'dry-run'}): {_class_line(Counter(c[0] for c in classes))}")
                if write and classes:
                    print(f"grid unify: record {_write_class_record(root, ns, classes)} (every merged mint by class, the banked pairs with their diffs)")
                if write and _origin_quiet(root):    # the mirror moved while this ran: the writes are additive, but say so
                    print(f"grid unify: unread (the mirror is no longer QUIET after the write: {_origin_quiet(root)}); the writes above stand")
                    total["unread"] = total.get("unread", 0) + 1
            banked = {c[1]: c[3] for c in classes if c[0] == "banked"}    # the byte test's own reason, listed in full: the owner's one batch
            shown = [m for m in conflicts if m in banked] + [m for m in conflicts if m not in banked][:50]
            for m in shown:    # listed by mint; never an automatic tree pick
                print(f"  CONFLICT {m} ({lns}: " + (f"banked, {banked[m]}" if m in banked else
                      "a version after the merge-base with a different tree, or a lost compare-and-swap") + ")")
            if len(shown) < len(conflicts):
                print(f"  ... {len(conflicts) - len(shown)} more CONFLICT mints")
    finally:
        if lock is not None:
            lock.release()
    return 1 if total.get("conflict") or total.get("unread") else 0


def _origin_dir(root: Path) -> Path:
    """Where `origin-snap` keeps its listings and its QUIET verdict (scratch, never versioned, one dir for
    every worktree). NOT `_unify_dir`: `unify --check` reads every `*.refs` there as a pre-write snapshot."""
    base = locations.shared_sessions_dir(root) if locations.is_graph_dir(root) else root / ".agi" / "sessions"
    return base / "origin-snap"


def _origin_listing(root: Path) -> dict[str, str] | None:
    """{mint: tip} of `ORIGIN_SNAP_NS/node`, or None when git could not list it (never 'empty')."""
    res = git_try(root, "for-each-ref", f"{ORIGIN_SNAP_NS}/node", "--format=%(refname) %(objectname)")
    if res.returncode != 0:
        return None
    out = {}
    for line in res.stdout.splitlines():
        ref, _, tip = line.partition(" ")
        out[ref[len(ORIGIN_SNAP_NS) + 6:]] = tip
    return out


def _listing_digest(listing: dict[str, str]) -> str:
    import hashlib
    return hashlib.sha256("".join(f"{m} {t}\n" for m, t in sorted(listing.items())).encode()).hexdigest()


def _origin_quiet(root: Path) -> str | None:
    """Why `unify --write` may NOT merge `ORIGIN_SNAP_NS`, or None when origin read QUIET for a lap: the
    verdict `origin-snap` wrote names the digest of the listing it judged, and the mirror still has it."""
    verdict = _origin_dir(root) / "quiet"
    try:
        want = verdict.read_text().split()[0]
    except (OSError, IndexError):
        return "no QUIET verdict: run `grid.py origin-snap` twice, one lap apart"
    have = _origin_listing(root)
    if not have:
        return f"{ORIGIN_SNAP_NS} cannot be listed"
    if _listing_digest(have) != want:
        return "the mirror changed since the QUIET verdict: run `grid.py origin-snap` again"
    return None


def cmd_origin_snap(root: Path, remote: str = "origin", lap_min: int = ORIGIN_LAP_MIN) -> int:
    """goal:g7.16.1.11.46.16 (the third history, council 07:47Z 10-26): O1 + O2 for origin's `refs/grid/node`,
    which holds tips this repo never fetched (another box's grid wrote them), so `push-changed` is rejected on
    every name whose origin tip is not in MAIN.

    O1 SNAPSHOT: `git fetch <remote> '+<ns>/node/*:refs/grid/origin-snap/node/*'`. The `+` forces a PRIVATE local
    mirror, never a shared ref; nothing pushes it and nothing else writes it. A fetch that errors or lists 0
    refs prints `unread` and returns 1 (an empty side would 'succeed' with 0 merged).
    O2 LIVENESS: print the newest mirror tip's committer date and name, record the listing, and diff it against
    the most recent listing at least `lap_min` minutes old (else the latest one). A tip that MOVED, or a name
    that appeared, to a commit that is NOT inside this repo's own `<ns>/node/<mint>` history is another writer:
    `LIVE second writer`, rc 2, STOP and bank ONE question (one writer per namespace, or per-box namespaces).
    Moves to our own history are our own `push-changed` landing and are not a second writer. No foreign move
    over a baseline >= one lap old writes the QUIET verdict `unify --write` demands for `ORIGIN_SNAP_NS`."""
    ensure_repo(root)
    ns = REF_NS
    if ns == ORIGIN_SNAP_NS or ns.startswith(ORIGIN_SNAP_NS + "/"):
        print(f"grid origin-snap: unread (the one namespace {ns} is the mirror itself)")
        return 1
    d = _origin_dir(root)
    d.mkdir(parents=True, exist_ok=True)
    (d / "quiet").unlink(missing_ok=True)    # every run re-earns the verdict
    # `--refmap=` (empty): a refspec given on the command line is ALSO mapped through the remote's configured refspecs (the ones
    # `grid.py init` wrote), so without it this "private mirror" read moves, or rejects (rc 1), the LIVE `<ns>/node/*` names (alive 12:15Z 10-26, F1).
    res = git_try(root, "fetch", "--no-tags", "--prune", "-q", "--refmap=", remote, f"+{ns}/node/*:{ORIGIN_SNAP_NS}/node/*")
    if res.returncode != 0:
        print(f"grid origin-snap: unread (fetch from {remote} failed: {(res.stderr.strip().splitlines() or ['no reason'])[0][:160]})")
        return 1
    have = _origin_listing(root)
    if not have:
        print(f"grid origin-snap: unread ({remote} lists no {ns}/node refs; nothing to merge)")
        return 1
    top = git_try(root, "for-each-ref", f"{ORIGIN_SNAP_NS}/node", "--sort=-committerdate", "--count=1",
                  "--format=%(committerdate:iso-strict) %(committername) %(refname)")
    line = top.stdout.strip()
    date, _, rest = line.partition(" ")
    who, _, ref = rest.rpartition(" ")
    print(f"grid origin-snap: fetched {len(have)} refs into {ORIGIN_SNAP_NS} (remote {remote}); "
          f"newest tip {date} by {who} ({ref[len(ORIGIN_SNAP_NS) + 6:]})")
    now = int(time.time())
    # the earlier listings, newest first: `<epoch>-<pid>-<n>.refs`, header `# fetched <epoch>`
    earlier = []
    for p in d.glob("*.refs"):
        try:
            head, *body = p.read_text().splitlines()
            earlier.append((int(head.split()[2]), p, dict(tuple(x.split(" ", 1)) for x in body if " " in x)))
        except (OSError, ValueError, IndexError):
            continue
    earlier.sort(key=lambda e: (e[0], e[1].stat().st_mtime_ns), reverse=True)    # newest first, even within one second
    n = 0
    while True:
        path = d / f"{now:011d}-{os.getpid()}-{n}.refs"
        try:
            with open(path, "x") as f:
                f.write(f"# fetched {now}\n" + "".join(f"{m} {t}\n" for m, t in sorted(have.items())))
            break
        except FileExistsError:
            n += 1
    if not earlier:
        print(f"grid origin-snap: first look ({path.name}); run it again after one lap ({lap_min} min) to read liveness")
        return 0
    base = next((e for e in earlier if now - e[0] >= lap_min * 60), earlier[0])
    age = (now - base[0]) // 60
    foreign, own = [], 0
    for m, t in sorted(have.items()):
        if base[2].get(m) == t:
            continue
        ours = ref_tip(root, f"{ns}/node/{m}")
        if ours and _is_ancestor(root, t, ours):
            own += 1
        else:
            foreign.append(m)
    gone = sorted(m for m in base[2] if m not in have)    # --prune dropped a name origin no longer lists: a delete is a write too
    print(f"grid origin-snap: against {base[1].name} ({age} min earlier): {len(foreign)} foreign move(s), "
          f"{own} landing of this repo's own push, {len(gone)} name(s) origin no longer lists")
    foreign += gone
    if foreign:
        for m in foreign[:10]:
            print(f"  MOVED {m}")
        print("grid origin-snap: LIVE second writer: origin's tips are still being written by someone else -- STOP; "
              "bank ONE question (one writer per namespace, or per-box namespaces). A one-shot unify cannot settle it.")
        return 2
    if age < lap_min:
        print(f"grid origin-snap: not yet a lap ({age} min < {lap_min}): no verdict; run it again later")
        return 0
    (d / "quiet").write_text(f"{_listing_digest(have)} {now}\n")
    print(f"grid origin-snap: QUIET for the lap ({age} min >= {lap_min}): `grid.py unify --into {ns} "
          f"--legacy {ORIGIN_SNAP_NS} --write` may run")
    return 0


def _classify_orphan(mint: str, last_id: str | None, id_mints: dict[str, set[str]]) -> str:
    """goal:g7.16.1.11.46.16 (the census-orphans decision, alive 07:40:32Z 10-26): an orphan is a mint with no node file
    in the view of `rev`. `double-mint`: ANOTHER mint carries the same `id:` on the trunk (a ghost, the trunk mint is
    the node); `never-landed`: no file under any mint carries that id; `unclassified`: its tip names no id at all.
    A third class can never hide inside the total: unclassified is its own number and makes the census rc 1."""
    if not last_id:
        return "unclassified"
    return "double-mint" if id_mints.get(last_id, set()) - {mint} else "never-landed"


def cmd_census(root: Path, rev: str = "HEAD", orphans: bool = False) -> int:
    """goal:g7.16.1.11.46.16 (doc §34.5): five numbers over the ONE namespace, mints counted by their tip.

        mints    git for-each-ref <ns>/node                       (tips, not versions)
        live     } git cat-file --batch over the tips' node.md      status != deprecated / == deprecated
        retired  }                                                 live + retired = mints
        versions git rev-list --count --stdin over the tips        distinct commits (a unify merge is one)
        orphans  git grep '^mint_id:' <rev> -- <nodes>             mints with no node file in the view of <rev>

    `orphans` = double_mints + never_landed + unclassified, each its OWN printed number (`_classify_orphan`);
    an unclassified orphan prints its mint and makes the cell rc 1. `--orphans` lists every orphan as
    `<mint> <last id> <versions> <class>` before the numbers.

    The ONE pinned command behind the 22-vs-46 gap (K3): `git grep -h '^mint_id:' <rev> -- .agi/nodes`
    against `git for-each-ref <ns>/node` is a SET difference (22 at 695c008dfd); 46 was 5991 minus 5945,
    two counts that were not the same population. A failing git command or an empty listing in the
    namespace or in a declared legacy namespace prints `unread (...)` and returns 1, never a zero."""
    ensure_repo(root)
    ns = REF_NS

    def unread(what: str) -> int:
        print(f"grid census: unread ({what})")
        return 1

    for space in [ns, *LEGACY_NS]:
        res = git_try(root, "for-each-ref", f"{space}/node", "--format=%(refname)")
        if res.returncode != 0 or not res.stdout.split():
            return unread(f"{space} lists no node refs")
    res = git_try(root, "for-each-ref", f"{ns}/node", "--format=%(objectname) %(refname)")
    rows = [x.split() for x in res.stdout.splitlines()]
    tips = [r[0] for r in rows]
    mints = {r[1][len(ns) + 6:] for r in rows}
    last_id: dict[str, str] = {}    # mint -> the `id:` its tip's node.md names
    tip_of = {r[1][len(ns) + 6:]: r[0] for r in rows}
    res = subprocess.run(["git", "-C", str(repo_root(root)), "cat-file", "--batch"],
                         input="".join(f"{t}:{NODE_ENTRY}\n" for t in tips).encode(), capture_output=True)
    if res.returncode != 0:
        return unread("cat-file over the tips")
    out, pos, live, retired = res.stdout, 0, 0, 0
    for t in tips:
        nl = out.find(b"\n", pos)
        head = out[pos:nl].split() if nl >= 0 else []
        if len(head) != 3 or head[1] != b"blob":
            return unread(f"{t[:12]} has no {NODE_ENTRY}")
        size = int(head[2])
        body = out[nl + 1:nl + 1 + size].decode("utf-8", "replace")
        pos = nl + 1 + size + 1
        lines = body.split("\n")
        if lines[0].strip() != "---" or "---" not in [x.rstrip() for x in lines[1:]]:
            return unread(f"{t[:12]} has no frontmatter")
        front = "\n".join(lines[1:[x.rstrip() for x in lines[1:]].index("---") + 1])
        mi = re.search(r"^id:\s*[\"']?(\S+?)[\"']?\s*$", front, re.M)
        if mi is not None:
            last_id[next(k for k, v in tip_of.items() if v == t)] = mi.group(1)
        m = re.search(r"^status:\s*[\"']?([A-Za-z_-]+)", front, re.M)    # no status line = live (status != deprecated)
        if m is not None and m.group(1) == "deprecated":
            retired += 1
        else:
            live += 1
    res = git_try(root, "rev-list", "--count", "--stdin", input_text="\n".join(tips) + "\n")
    if res.returncode != 0:
        return unread("rev-list over the tips")
    versions = int(res.stdout)
    nodes = (Path(root) / "nodes").resolve().relative_to(repo_root(root).resolve()).as_posix()
    res = git_try(root, "grep", "-z", "-n", "-e", "^id:", "-e", "^mint_id:", rev, "--", nodes)
    if res.returncode not in (0, 1):
        return unread(f"git grep {rev}")
    per_file: dict[str, dict[str, str]] = {}    # path -> {"id": ..., "mint_id": ...}: the FIRST of each (the frontmatter)
    for line in res.stdout.split("\n"):
        parts = line.split("\0", 2)
        if len(parts) != 3 or not parts[1].isdigit():
            continue
        key, _, val = parts[2].partition(":")
        val = re.sub(r"[\"']", "", val).strip().split()
        if val:
            per_file.setdefault(parts[0].partition(":")[2], {}).setdefault(key, val[0])
    filed = {v["mint_id"] for v in per_file.values() if "mint_id" in v}
    id_mints: dict[str, set[str]] = {}
    for v in per_file.values():
        if "id" in v and "mint_id" in v:
            id_mints.setdefault(v["id"], set()).add(v["mint_id"])
    if not filed:
        return unread(f"no node file under {nodes} at {rev}")
    classes = {m: _classify_orphan(m, last_id.get(m), id_mints) for m in sorted(mints - filed)}
    n_dm = sum(1 for c in classes.values() if c == "double-mint")
    n_nl = sum(1 for c in classes.values() if c == "never-landed")
    n_un = sum(1 for c in classes.values() if c == "unclassified")
    if orphans:
        for m in sorted(classes, key=lambda x: (classes[x], x)):
            n = git_try(root, "rev-list", "--count", tip_of[m])
            print(f"{m} {last_id.get(m, '-')} {n.stdout.strip() if n.returncode == 0 else '?'} {classes[m]}")
    for m, c in classes.items():
        if c == "unclassified":
            print(f"grid census: UNCLASSIFIED orphan {m} (its tip names no id)")
    print(f"grid census: mints={len(mints)} live={live} retired={retired} versions={versions} orphans={len(classes)} "
          f"double_mints={n_dm} never_landed={n_nl} unclassified={n_un}")
    return 1 if n_un else 0


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
    out = git(root, "push", "origin", *PUSH_SPECS)
    print(out or "grid: synced")


def cron_log(root: Path) -> Path:
    """The per-project cron log — and, because `cmd_cron` uses its path as the
    marker for "our" crontab lines, the per-project *identity* of those lines.

    Named after the REPO root, not the graph root (goal:g11). Every migrated
    project's graph root is literally named `.agi`, so deriving the name from it
    gives every project on the planet the same `grid-sync-.agi.log` marker — and
    `cron install`, which removes every line carrying the marker before writing
    its own, would then silently uninstall a *different* project's crons. The
    repo root's name is the thing that actually differs between projects.
    Identity under the legacy layout, so an already-installed line keeps
    matching (verified against the live `grid-sync-fantasia.log` entry).
    """
    return Path.home() / "logs" / f"grid-sync-{repo_root(root).name}.log"


def cron_lines(root: Path, branch: str, mins: int, log: Path) -> list[str]:
    """The cadence entries. The `cd` is load-bearing: cron runs from $HOME
    and find_project_root walks up from cwd — a cd-less line fails silently.

    Both the `cd` and the `git -C` name the REPO root, not the graph root
    (goal:g11). The `cd` because `find_project_root` walking up from `<repo>`
    finds `<repo>/.agi` in phase 0 and resolves identically, while `<repo>/.agi`
    is a directory that may not exist on a project that has not migrated; the
    `git -C` for the same reason every other git call in this file does. Under
    the legacy layout `repo_root` is the identity, so these lines are unchanged
    byte-for-byte for any project already carrying an installed crontab entry.

    Two cadences always: snapshot+grid-push every `mins`, branch push hourly.

    (A third and fourth, gated on `--publish-engine`, ran `publish-engine.sh` at
    :37 and pushed the engine repo at :47 -- retired with that script, goal:g11's
    two-repo carry, by goal:g7.16.1.4.1.1.)
    """
    script = Path(__file__).resolve()
    repo = repo_root(root)
    snap = (f"*/{mins} * * * * cd {repo} && "
            f"python3 {script} commit --all --prefix 'cron: ' >> {log} 2>&1 && "
            f"git push -q origin {' '.join(repr(x) for x in PUSH_SPECS)} >> {log} 2>&1")
    d1 = f"7 * * * * git -C {repo} push -q origin {branch} >> {log} 2>&1"
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
    c.add_argument("--allow-branch", action="store_true",
                   help="allow commit --all on a non-master branch; node refs "
                        "are branch-blind, merge to master first to share history")
    c.add_argument("--lock-wait", type=int, default=120,
                   help="seconds commit --all waits on the grid flock before "
                        "failing non-zero (default 120)")
    lg = sub.add_parser("log")
    lg.add_argument("node_id")
    lg.add_argument("-n", type=int, default=20)
    d = sub.add_parser("diff")
    d.add_argument("node_id")
    d.add_argument("--back", type=int, default=1)
    v = sub.add_parser("versions")
    v.add_argument("node_id")
    pl = sub.add_parser("payload",
                        help="goal:g6.3 -- read a build node's payload out of "
                             "its grid ref")
    pl.add_argument("node_id")
    pl.add_argument("--version", type=int, default=None,
                    help="v1..vN; default is the tip")
    pl.add_argument("--out", default=None,
                    help="write to this path with the recorded mode "
                         "(default: raw bytes to stdout)")
    co = sub.add_parser("checkout",
                        help="goal:g6.1 -- materialize payloads into "
                             "<project>/payloads/ for editing")
    co.add_argument("node_ids", nargs="*")
    co.add_argument("--all", action="store_true")
    co.add_argument("--dir", default=None,
                    help=f"destination (default: <project>/{PAYLOAD_DIR})")
    co.add_argument("--engine-root", default=None,
                    help="engine repo to copy unmanaged files from "
                         "(default: this script's own repo)")
    co.add_argument("--force", action="store_true",
                    help="overwrite payloads that differ from the grid tip, "
                         "discarding unrecorded edits")
    co.add_argument("--no-unmanaged", action="store_true",
                    help="do not copy engine files that carry no node "
                         "(tests/fixtures, .jsonl). Leaves a graph-only tree "
                         "that is NOT runnable — 19 tests need those fixtures.")
    sub.add_parser("status")
    m = sub.add_parser("migrate-refs",
                       help="move refs/grid/node/* onto the injective "
                            "sanitize() scheme; dry-run unless --write")
    m.add_argument("--write", action="store_true")
    mm = sub.add_parser("migrate-mint-refs",
                        help="goal:g2.5 -- move refs/grid/node/<node-id> onto "
                             "refs/grid/node/<mint-id>; dry-run unless --write. "
                             "MUST run before commit --all under the new keying.")
    mm.add_argument("--write", action="store_true")
    mt = sub.add_parser("migrate-trunk",
                        help="goal:g14.14.7 -- move EVERY ref from a source "
                             "namespace onto a new trunk (e.g. "
                             "refs/grid -> refs/grid/local-maxxing), reusing "
                             "_rename_ref; dry-run unless --write. Config key "
                             "grid.storage_trunk declares the destination; the "
                             "source is --from (default refs/grid), never the "
                             "config-resolved namespace.")
    mt.add_argument("--from", dest="from_ns", default=DEFAULT_REF_NS,
                    help="source namespace (default: refs/grid); deliberately "
                         "NOT the configured trunk -- run this BEFORE any "
                         "commit --all under the new config")
    mt.add_argument("--to", default=None,
                    help="destination namespace (default: the configured "
                         "grid.storage_trunk); a trailing / is stripped")
    mt.add_argument("--write", action="store_true")
    un = sub.add_parser("unify",
                        help="goal:g7.16.1.11.46.16 -- merge each tip of the LEGACY namespace (refs/grid/"
                             "local-maxxing, the namespace every writer used until this land) into the one "
                             "namespace (refs/grid/node, the 09-21 freeze), additive (no delete); dry-run unless "
                             "--write (which writes its own pre-write snapshot); --check is the read-only falsifier")
    un.add_argument("--write", action="store_true")
    un.add_argument("--check", action="store_true")
    un.add_argument("--into", default=None,
                    help="the namespace to merge INTO (refs/grid: the 09-21 freeze, the one namespace), overriding the config (run BEFORE the config lands)")
    un.add_argument("--legacy", action="append", default=None,
                    help="a LEGACY namespace to merge FROM (repeatable; refs/grid/local-maxxing, the namespace every writer used until this land), overriding grid.legacy_namespaces")
    un.add_argument("--owner-batch", default=None, metavar="RECORD",
                    help="the owner's ruling of a banked batch: write every `banked` pair of the stamped record RECORD (a .classes name) as tree = LIVE, origin's tip the 2nd parent (with --legacy refs/grid/origin-snap)")
    un.add_argument("--trunk", default="HEAD",
                    help="the ref whose history is the TRUNK's blob evidence for the origin mirror's byte test (default HEAD; pass the land branch when HEAD is not it)")
    os_ = sub.add_parser("origin-snap",
                         help="goal:g7.16.1.11.46.16 -- mirror origin's refs/grid/node into the PRIVATE refs/grid/origin-snap and "
                              "read whether origin is still being written (rc 2 = a LIVE second writer); the QUIET verdict "
                              "`unify --legacy refs/grid/origin-snap --write` demands")
    os_.add_argument("remote", nargs="?", default="origin")
    os_.add_argument("--lap", type=int, default=ORIGIN_LAP_MIN, help="minutes that make a lap (default 30, grid_sync's cadence)")
    ce = sub.add_parser("census", help="goal:g7.16.1.11.46.16 -- mints, live, retired, versions, orphans")
    ce.add_argument("--rev", default="HEAD")
    ce.add_argument("--orphans", action="store_true",
                    help="list every orphan as `<mint> <last id> <versions> <class>` (double-mint | never-landed | unclassified)")
    s = sub.add_parser("sync")
    s.add_argument("remote", nargs="?")
    sub.add_parser("push-changed", help="push only changed grid tips in bounded batches")
    cr = sub.add_parser("cron")
    cr.add_argument("action", choices=["install", "show", "remove"])
    cr.add_argument("--snapshot-mins", type=int, default=5)
    args = ap.parse_args()
    root = find_project_root()
    apply_storage_trunk(root)
    if args.cmd == "commit":
        cmd_commit(root, args.files, args.all,
                   tuple(args.session) if args.session else None,
                   prefix=args.prefix, allow_branch=args.allow_branch,
                   lock_wait=args.lock_wait)
    elif args.cmd == "init":
        cmd_init(root)

    elif args.cmd == "log":
        cmd_log(root, args.node_id, args.n)
    elif args.cmd == "diff":
        cmd_diff(root, args.node_id, args.back)
    elif args.cmd == "versions":
        cmd_versions(root, args.node_id)
    elif args.cmd == "payload":
        cmd_payload(root, args.node_id, args.version, args.out)
    elif args.cmd == "checkout":
        if not args.all and not args.node_ids:
            sys.exit("ERR: give node ids or --all")
        cmd_checkout(root, args.node_ids, args.all, args.dir,
                     engine_root=Path(args.engine_root).resolve()
                     if args.engine_root else None,
                     unmanaged=not args.no_unmanaged, force=args.force)
    elif args.cmd == "status":
        cmd_status(root)
    elif args.cmd in ("migrate-refs", "migrate-mint-refs", "migrate-trunk") and _retired_write(root, args.write):
        pass
    elif args.cmd == "migrate-refs":
        cmd_migrate_refs(root, args.write)
    elif args.cmd == "migrate-mint-refs":
        cmd_migrate_mint_refs(root, args.write)
    elif args.cmd == "migrate-trunk":
        cmd_migrate_trunk(root, args.to, args.write, args.from_ns)
    elif args.cmd == "unify" and (args.into or args.legacy) and _set_unify_namespaces(args.into, args.legacy):
        pass
    elif args.cmd == "unify" and not args.check and _retired_write(root, args.write):
        pass
    elif args.cmd == "unify":
        sys.exit(cmd_unify(root, args.write, args.check, args.trunk, args.owner_batch))
    elif args.cmd == "origin-snap":
        sys.exit(cmd_origin_snap(root, args.remote, args.lap))
    elif args.cmd == "census":
        sys.exit(cmd_census(root, args.rev, args.orphans))
    elif args.cmd == "sync":
        cmd_sync(root, args.remote)
    elif args.cmd == "push-changed":
        sys.exit(cmd_push_changed(root))
    elif args.cmd == "cron":
        cmd_cron(root, args.action, args.snapshot_mins)


if __name__ == "__main__":
    main()
