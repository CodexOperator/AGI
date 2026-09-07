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
from pathlib import Path

# goal:g11 — one resolver for every path. Plain sibling import; every entry
# point under `bin/` already has this directory on sys.path.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import evidence_gate  # noqa: E402
import locations  # noqa: E402

ID_RE = re.compile(r'^id:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
# goal:g2.5 "Tension resolved 2026-08-25" — the permanent identifier grid.py
# now keys writes on. Same line shape as ID_RE, parsed the same stdlib-regex
# way (this file stays yaml-free by design — see module docstring).
MINT_ID_RE = re.compile(r'^mint_id:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
PAYLOAD_REF_RE = re.compile(r'^payload_ref:\s*"?([^"\n]+?)"?\s*$', re.MULTILINE)
PARENTS_RE = re.compile(r'^parents:[ \t]*$', re.MULTILINE)
PARENTS_INLINE_RE = re.compile(r'^parents:\s*\[([^\]]*)\]\s*$', re.MULTILINE)
PARENTS_SCALAR_RE = re.compile(r'^parents:\s*([^\n\[][^\n]*)$', re.MULTILINE)
GIT_IDENT = ["-c", "user.name=grid", "-c", "user.email=grid@agi"]
REF_NS = "refs/grid"
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
FETCH_SPEC = f"+{REF_NS}/*:{REF_NS}/*"
PUSH_SPEC = f"{REF_NS}/*:{REF_NS}/*"


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


def default_engine_root() -> Path:
    """The engine tree a payload is read from when the graph repo has no
    staged copy: this script's own repo, `<engine>/extensions/agi/bin/grid.py`
    -> `<engine>`. Same derivation `level3.py` uses for `DEFAULT_ENGINE_ROOT`.
    """
    return Path(__file__).resolve().parents[3]


def resolve_payload(root: Path, payload_ref: str,
                    engine_root: Path) -> tuple[Path, str] | None:
    """Where a node's payload bytes are read from, and which source won.

    Priority, and the order *is* goal:g6.1's arrow:

      1. `<project>/payloads/<payload_ref>` — the graph repo's own staged
         checkout (`grid.py checkout`). This is the copy an author edits, and
         its presence is what makes the graph the source: the engine tree is
         never consulted for a node that has one.
      2. `<engine>/<payload_ref>` — the live engine tree. The bootstrap path,
         and what a node still uses until it has been checked out. Committing
         from here is how a node's payload history starts without anyone
         having to stage all 180 files first.

    Returns `(path, "staged" | "engine")`, or None when neither exists — the
    caller reports that rather than committing a node whose payload vanished.
    """
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


def build_parent_mint_trailer(path: Path, id_index: dict[str, Path]) -> str | None:
    """Commit-message body for goal:g2.7: one `Parent-Mint-Id: <mint-id> <parent-node-id>`
    line per entry in `path`'s `parents:`, so a renderer can traverse disk
    nodes and grid commits as one hypergraph without a separate edge store —
    the edge is already written into the history. Documented format:

        Parent-Mint-Id: <32-hex-char mint id, or the literal UNRESOLVED> <parent node id>

    `UNRESOLVED` (never a fabricated id) means the parent could not be found
    on disk, or was found but has no `mint_id` of its own yet.

    Returns None (no body to add) if the node has no parents at all.
    """
    parents = parse_parents(path)
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
    if tip:
        old_tree = git(root, "rev-parse", f"{tip}^{{tree}}", check=False)
        if old_tree == tree:
            return None  # unchanged — versions record change, not time
    n = int(git(root, "rev-list", "--count", tip)) + 1 if tip else 1
    parent = ["-p", tip] if tip else []
    subject = f"{msg_prefix}v{n} {node_id}"
    message = f"{subject}\n\n{trailer}\n" if trailer else subject
    commit = git(root, "commit-tree", tree, *parent, "-m", message)
    git(root, "update-ref", ref, commit)
    return f"v{n}"


def iter_node_files(root: Path):
    yield from sorted((root / "nodes").rglob("*.md"))


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
    """
    def __init__(self, root: Path, wait_seconds: int) -> None:
        self._lock_dir = root / ".agi" / "sessions"
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
    ensure_repo(root)

    # hypothesis:l2w15-grid-master-guard — refuse commit on a non-master
    # branch unless --allow-branch is passed. Session commits (D3 drafts)
    # are never gated. Addendum (owners, seasons-as-branches): branches named
    # season/* are admitted like master; any other non-master branch refused.
    if not session and not allow_branch:
        # resolve the checked-out branch of the repo that owns the graph
        # Use symbolic-ref: on a branch it returns the ref name (e.g. master,
        # work); on detached HEAD it fails (exit != 0) which we treat as not
        # master.
        branch = git(root, "symbolic-ref", "--short", "HEAD", check=False)
        # git symbolic-ref returns empty string on error with check=False
        if not branch or (branch != "master" and not branch.startswith("season/")):
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
            demoted = sum(1 for d in evidence_gate.enforce_on_disk(root, paths)
                          if d.written)
        id_index = None if session else build_id_index(root)
        engine_root = engine_root or default_engine_root()
        written = 0
        errors = 0
        payloads = 0
        payload_missing = 0
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
                trailer = build_parent_mint_trailer(p, id_index)
                payload_ref = parse_payload_ref(p)
                if payload_ref:
                    found = resolve_payload(root, payload_ref, engine_root)
                    if found is None:
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
              f"{demoted} demoted by the evidence gate")
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
    print(git(root, "log", f"-{n}", "--format=%h %ad %s", "--date=short", ref))


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
    count = int(git(root, "rev-list", "--count", ref))
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
    print(int(git(root, "rev-list", "--count", tip)) if tip else 0)


# --- payload read side (goal:g6.3 / goal:g6.1) -------------------------------


def version_rev(root: Path, ref: str, node_id: str, version: int | None) -> str:
    """The revision holding version `v<version>` of `node_id`, or the tip.

    Versions count forward from 1 (`commit_file`'s `rev-list --count` + 1), so
    v(count) is the tip and v1 is `tip~(count-1)`. An out-of-range version is a
    hard error naming the range: silently serving the tip for a version that
    does not exist is the "partial answer served as a complete one" failure G7
    names in its invariants.
    """
    if version is None:
        return ref
    count = int(git(root, "rev-list", "--count", ref))
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
        found = resolve_payload(root, payload_ref, engine_root) if payload_ref else None
        fresh = tree_entries(root, p, found[0] if found else None, write=False)
        if fresh == read_tree(root, ref):
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
        git(root, "update-ref", new_ref, old_tip)
        git(root, "update-ref", "-d", old_ref, old_tip)
    return "moved"


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


def cron_lines(root: Path, branch: str, mins: int, log: Path,
               publish_engine: bool = False) -> list[str]:
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

    A third, **only** with `publish_engine` (goal:g6.5 step 2): rebuild the
    engine repo from the graph and commit it. Opt-in and off by default on
    purpose — G6.5's own sequencing says a cron that writes the engine before
    the version layer is trusted is a data-loss defect waiting to happen, and
    `cron install` runs on projects where it is not yet trusted. Deciding that
    for a project is the project's call, not the installer's.

    It runs at :37, after the :07 branch push, so a publish is never racing the
    push of the graph commit it cites.

    A **fourth**, also gated on `publish_engine`: push the engine repo at :47,
    ten minutes after the publish that writes it. `publish-engine.sh` commits
    the engine and deliberately does not push — "pushing is the hourly cron's
    job" — but for the engine repo that cron did not exist, so its commits
    accumulated locally and the remote went 3 days and 25 commits stale before
    anyone noticed. A design that hands a job to a cron has to install that
    cron; the two halves shipped apart and the gap was invisible from both
    sides.

    It pushes `HEAD`, not a branch captured at install time. That is the
    lesson of the `iter24-extend-300hop` incident from the other direction:
    work accumulated on a feature branch while a cron pushed `master` and
    published nothing. Pushing whatever is checked out cannot silently push
    the wrong branch — at worst it creates a remote branch, which is visible.
    """
    script = Path(__file__).resolve()
    repo = repo_root(root)
    snap = (f"*/{mins} * * * * cd {repo} && "
            f"python3 {script} commit --all --prefix 'cron: ' >> {log} 2>&1 && "
            f"git push -q origin '{PUSH_SPEC}' >> {log} 2>&1")
    d1 = f"7 * * * * git -C {repo} push -q origin {branch} >> {log} 2>&1"
    lines = [snap, d1]
    if publish_engine:
        publisher = script.parent / "publish-engine.sh"
        engine_root = script.parents[3]
        lines.append(f"37 * * * * cd {repo} && bash {publisher} >> {log} 2>&1")
        lines.append(
            f"47 * * * * git -C {engine_root} push -q origin HEAD >> {log} 2>&1")
    return lines


def read_crontab() -> list[str]:
    res = subprocess.run(["crontab", "-l"], capture_output=True, text=True)
    return res.stdout.splitlines() if res.returncode == 0 else []


def write_crontab(lines: list[str]) -> None:
    text = "\n".join(lines) + ("\n" if lines else "")
    res = subprocess.run(["crontab", "-"], input=text, capture_output=True,
                         text=True)
    if res.returncode != 0:
        sys.exit(f"ERR: crontab install failed: {res.stderr.strip()}")


def cmd_cron(root: Path, action: str, mins: int,
             publish_engine: bool = False) -> None:
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
    new = cron_lines(root, branch, mins, log, publish_engine)
    write_crontab(keep + new)
    extra = ", engine published hourly" if publish_engine else ""
    print(f"grid cron: installed (snapshot every {mins}m, {branch} hourly{extra}):")
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
    s = sub.add_parser("sync")
    s.add_argument("remote", nargs="?")
    cr = sub.add_parser("cron")
    cr.add_argument("action", choices=["install", "show", "remove"])
    cr.add_argument("--snapshot-mins", type=int, default=5)
    cr.add_argument("--publish-engine", action="store_true",
                    help="goal:g6.5 step 2 — also install an hourly entry that "
                         "rebuilds the engine repo from the graph and commits "
                         "it. Off by default: only a project whose version "
                         "layer is trusted should enable this.")
    args = ap.parse_args()
    root = find_project_root()
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
    elif args.cmd == "migrate-refs":
        cmd_migrate_refs(root, args.write)
    elif args.cmd == "migrate-mint-refs":
        cmd_migrate_mint_refs(root, args.write)
    elif args.cmd == "sync":
        cmd_sync(root, args.remote)
    elif args.cmd == "cron":
        cmd_cron(root, args.action, args.snapshot_mins, args.publish_engine)


if __name__ == "__main__":
    main()
