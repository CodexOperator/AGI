#!/usr/bin/env python3
"""unify.py — merge the two-repo layout into one, for **goal:g11**.

Today `agi-tree` holds the thoughts and `agi` holds the code, and everything
between them (`payloads/`, `grid.py checkout`, `stitch.py --publish`,
`publish-engine.sh`) exists only to carry bytes across that boundary
(**goal:g6.3**). G11 removes the boundary: the graph moves under `.agi/`
*inside* the engine repo it describes, so a `payload_ref` becomes a path to a
tracked file in the same worktree and one `git commit` carries a thought and
the code it produced together.

This script performs that merge, once, on two already-cloned repos:

    0. pre-state            snapshot HEAD + every ref, for --rollback
    1. preflight            both source repos clean; target is a fresh clone;
                             every payload_ref the graph knows about resolves
                             under the engine (the publish-lag gate)
    2. graft                subtree-merge the tree's history under `.agi/`
    3. relocate             `.agi/GOALS.md` -> `GOALS.md`, likewise CLAUDE.md
                             and AGENTS.md; config -> `.agi/config.json`
    4. gitignore            one merged `.gitignore` at the repo root
    5. grid refs            fetch `refs/grid/*` across, verify the count
    6. report               a dict describing exactly what happened

Every payload byte lives in exactly one place: a grid ref (**goal:g7** —
nothing the loop produces is ever silently lost). Step 5's count assertion is
the load-bearing check in this whole script for that reason; every other
mismatch is recoverable from a re-clone, a lost grid ref is not.

**Zero `payload_ref` values need rewriting.** A `payload_ref` is stored
relative to the engine root; under the `.agi` layout `locations.source_root`
resolves to the enclosing repo, which *is* the engine root, so every value
resolves unchanged across the move. This script does not touch node content
at all — if a caller finds that assumption wrong, that is a bug in the
assumption, not something to "fix" by adding node-rewriting code here.

## Never run this against the real repos

`--engine` and `--tree` must point at throwaway clones — `git clone` the real
`agi` and `agi-tree` to `/tmp/...` and pass those paths. `preflight()` refuses
outright, unconditionally, before any other check and regardless of
`--force`, if either path resolves to the two real checkouts this machine
happens to keep at `/home/ubuntu/work/agi` and `/home/ubuntu/work/agi-tree`.
That is a literal path comparison, not a remote-URL check, because a
legitimate throwaway clone's own `origin` can point at the very same GitHub
repos — the thing that must never be `/home/ubuntu/work/agi` is the
*directory this script writes into*, and a clone under `/tmp` is a different
directory regardless of what it was cloned from.

## Dry-run by default, `--yes` to mutate

Every entry point below either only reads (`preflight`, the two pure
gitignore helpers) or is a single, explicit mutating stage (`graft_graph`,
`relocate_files`, `write_merged_gitignore`, `fetch_grid_refs`). `run_unify`
calls `preflight` unconditionally and returns its report as-is on failure;
without `--yes` it stops there and returns a plan built entirely from
`preflight`'s read-only data — no remote is ever added, no ref is ever
fetched, nothing under `--engine` changes. `main()`'s `--dry-run` flag is an
explicit override that forces the plan path even if `--yes` is also given,
for a caller that wants to pass both defensively.

## Idempotency: a clean refusal, not a re-apply

This script does not support re-running against a target it already
migrated. `preflight` requires the target to have no `.agi/` yet, which the
first successful run creates — so a second run against the same `--engine`
checkout refuses with `reason: engine_has_agi_already` rather than silently
doing nothing or (worse) partially re-applying. Recovering from a partial
failure means a fresh clone, or `--force` (which bypasses the fresh-clone
checks for deliberate recovery and does not undo any partial state itself).

## `--rollback`: four operations, not one

Rehearsal run 4 found that reversing a migration is not `git reset --hard`
alone: `reset` does nothing to `refs/grid/*` — those arrive by fetch and
survive a branch reset — so a rollback that skipped the explicit ref deletion
would leave the repo holding every grid ref from a migration that supposedly
did not happen. `write_prestate` records HEAD and every ref to
`<engine>/.git/agi-unify-prestate.json` (inside `.git/`, so `reset --hard`
and `clean -fd` cannot touch it) before the first mutating stage runs;
`--rollback` reads it back and performs `reset --hard` + delete every
`refs/grid/*` + `clean -fd` + drop the temporary remote if still present.

It refuses if the pre-state file is missing, if HEAD is not a descendant of
the recorded pre-migration HEAD (this is not the migrated repo, or someone
already rolled back), or if the migrated HEAD is reachable from any
`refs/remotes/*` (the pushed case — reversing published history needs a
force-push, a materially worse operation that must not happen by accident).
`--force` overrides only the last of these.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import locations  # noqa: E402

# The ENGINE's graph_core, never a project's vendored src/ — same precedent as
# node_writer.py's `mint_permanent_id` import (goal:s14): unify.py always runs
# from `<engine clone>/extensions/agi/bin/`, so its own sibling `src/` is the
# one frontmatter parser the publish-lag gate below must agree with.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from graph_core.persistence.frontmatter import load_node_file, FrontmatterError  # noqa: E402

# Every git invocation below carries its own identity rather than relying on
# the ambient `user.name`/`user.email` — a throwaway clone made purely for a
# rehearsal has no reason to have either configured, and `grid.py` sets the
# same precedent (`GIT_IDENT`) for exactly that reason.
GIT_IDENT = ["-c", "user.name=agi-unify", "-c", "user.email=agi-unify@agi"]

#: Git's index mode for a symlink. `AGENTS.md` must keep this mode through the
#: relocate step (goal:s9 — `grid.py`'s `commit_file()` once mis-hashed a
#: symlink as a regular file in this exact area), so it is checked explicitly
#: rather than trusted to `git mv`.
SYMLINK_MODE = "120000"

#: Name for the temporary remote added in the target during the graft. Cheap
#: enough to hardcode: exactly one graft ever runs against a given target
#: (see "Idempotency" above), and `graft_graph` removes any stale remote of
#: this name before adding it, so a retry after a partial failure still works.
REMOTE_NAME = "agi-unify-source"

GRID_REF_NAMESPACE = "refs/grid"
GRID_FETCH_REFSPEC = "refs/grid/*:refs/grid/*"

GRAFT_COMMIT_MESSAGE = (
    "goal:g11 — graft the graph's history under .agi/\n\n"
    "Subtree merge (merge -s ours + read-tree --prefix=.agi/): both histories "
    "are parents of this commit, preserved rather than squashed."
)
RELOCATE_COMMIT_MESSAGE = (
    "goal:g11 — relocate GOALS.md, CLAUDE.md and AGENTS.md to the repo root, "
    "config into .agi/\n\n"
    "git mv, so history follows all four files. AGENTS.md is a symlink to "
    "CLAUDE.md (goal:s9) and its 120000 mode is verified, not assumed."
)
GITIGNORE_COMMIT_MESSAGE = (
    "goal:g11 — merge the two .gitignore files into one at the repo root"
)

#: Name of the pre-migration snapshot `write_prestate` writes under `<engine
#: clone>/.git/` — deliberately inside `.git/`, not the working tree: a
#: rollback's own first two operations (`reset --hard`, `clean -fd`) touch
#: everything the working tree holds, and the one thing recovery cannot
#: survive losing is the file that describes how to recover.
PRESTATE_FILENAME = "agi-unify-prestate.json"

#: Where `--rollback` looks for the pushed case: a remote-tracking ref that
#: already has the migrated HEAD as an ancestor means the migration has left
#: this clone, and reversing it now needs a force-push against shared
#: history rather than a private `git reset`.
REMOTE_REF_NAMESPACE = "refs/remotes"


class UnifyError(Exception):
    """A git operation failed, or a post-condition this script exists to
    guarantee did not hold. Every raise site names the path and command at
    fault. Never caught and patched over inside this module — `main()` is the
    one place that turns this into a process exit code."""


# --- git plumbing -----------------------------------------------------------


def _git(repo: Path, *args: str, check: bool = True) -> str:
    res = subprocess.run(
        ["git", *GIT_IDENT, "-C", str(repo), *args],
        capture_output=True, text=True,
    )
    if check and res.returncode != 0:
        raise UnifyError(
            f"git -C {repo} {' '.join(args)} failed (exit {res.returncode}): "
            f"{res.stderr.strip()}"
        )
    return res.stdout


def _git_stdin(repo: Path, args: list[str], stdin_text: str) -> str:
    """Like `_git`, but feeds `stdin_text` to the command — the one shape
    `git update-ref --stdin` needs and plain `_git` cannot express."""
    res = subprocess.run(
        ["git", *GIT_IDENT, "-C", str(repo), *args],
        input=stdin_text, capture_output=True, text=True,
    )
    if res.returncode != 0:
        raise UnifyError(
            f"git -C {repo} {' '.join(args)} (stdin) failed (exit "
            f"{res.returncode}): {res.stderr.strip()}"
        )
    return res.stdout


def _is_ancestor(repo: Path, ancestor: str, descendant: str) -> bool:
    """`ancestor` is `descendant` itself or reachable from it. Shared by the
    graft's own history-preserved check and the rollback safety checks below
    — one definition of "is this sha still in the line of descent" rather
    than two copies that could drift on the reflexive case (a commit is its
    own ancestor)."""
    return subprocess.run(
        ["git", "-C", str(repo), "merge-base", "--is-ancestor", ancestor, descendant],
    ).returncode == 0


def _all_refs(repo: Path) -> dict[str, str]:
    """Every ref in `repo` (branches, tags, `refs/grid/*`, anything else) as
    `{refname: sha}` — the pre-migration snapshot's other half beyond HEAD,
    and the read `--rollback` uses to know exactly which `refs/grid/*` names
    to delete."""
    out = _git(repo, "for-each-ref", "--format=%(refname) %(objectname)")
    refs: dict[str, str] = {}
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        name, _, sha = line.partition(" ")
        refs[name] = sha
    return refs


def _resolve_branch(repo: Path) -> str:
    """The checked-out branch of `repo`. Re-derived rather than hardcoded to
    `master` — both real repos happen to use `master` today (verified), but a
    resolver that hardcodes it is exactly the S2 defect (agi-tree's own
    `crons.py` module docstring) repeated in a new file."""
    res = subprocess.run(
        ["git", "-C", str(repo), "symbolic-ref", "--short", "-q", "HEAD"],
        capture_output=True, text=True,
    )
    branch = res.stdout.strip()
    if res.returncode != 0 or not branch:
        raise UnifyError(
            f"{repo}: HEAD is not on a branch (detached?) — refusing to guess "
            f"a branch name for the graft"
        )
    return branch


def count_grid_refs(repo: Path) -> int:
    """Number of refs under `refs/grid/` in `repo`. A ref is the only home of
    every payload byte (goal:g7) — this is the number step 5 asserts across
    unchanged, and the number `preflight` records before anything happens."""
    out = _git(repo, "for-each-ref", GRID_REF_NAMESPACE)
    return len([line for line in out.splitlines() if line.strip()])


def _node_count(nodes_dir: Path) -> int:
    return len(list(nodes_dir.rglob("*.md"))) if nodes_dir.is_dir() else 0


# --- publish-lag gate (rehearsal run 2) --------------------------------------


def iter_payload_refs(tree: Path) -> list[tuple[Path, str]]:
    """`(node_path, payload_ref)` for every `.md` node under `<tree>/nodes`
    that declares one. Walks the retired sibling too (`nodes/deprecated/...`
    is nested under `nodes/`, so `rglob` finds it for free) — a deprecated
    node's grid ref outlives its file (CLAUDE.md's deprecation convention),
    and its `payload_ref` is exactly as real as a live node's.

    A file whose frontmatter fails to parse is skipped, not raised on: this
    gate exists to catch the engine being behind the graph's last publish, not
    to become a second frontmatter linter.
    """
    nodes_dir = Path(tree) / "nodes"
    out: list[tuple[Path, str]] = []
    if not nodes_dir.is_dir():
        return out
    for p in sorted(nodes_dir.rglob("*.md")):
        try:
            nf = load_node_file(p, body=False)
        except FrontmatterError:
            continue
        ref = nf.frontmatter.get("payload_ref")
        if isinstance(ref, str) and ref.strip():
            out.append((p, ref.strip()))
    return out


def find_missing_payloads(tree: Path, engine: Path) -> list[str]:
    """`payload_ref` values from `tree`'s nodes that do not exist under
    `engine` — the check rehearsal run 2 found missing. A `payload_ref` is
    stored relative to the engine root (`locations.source_root`'s contract),
    so this is that same resolution rule, checked *before* the graft that
    would otherwise carry the graph's description of a file the engine does
    not have onto disk.

    Sorted and de-duplicated: two nodes can (in principle) name the same
    path, and the caller reports a count of distinct missing files, not a
    count of nodes.
    """
    engine = Path(engine).resolve()
    missing = {ref for _node_path, ref in iter_payload_refs(tree) if not (engine / ref).exists()}
    return sorted(missing)


def find_stale_payloads(tree: Path, engine: Path) -> list[str]:
    """`payload_ref` paths that EXIST under `engine` but whose bytes disagree
    with the grid.

    **Existence is not the invariant, and testing the gate on live data is what
    showed it.** `find_missing_payloads` catches a file the graph knows about
    that the engine has never seen — rehearsal run 2's case, four brand-new
    files. It does not catch the far more ordinary case: a file that was
    published once and then *edited*, so the engine still has a copy and that
    copy is stale. Measured on the real repos before the migration: 0 missing,
    **2 stale**. The gate passed, and a migration at that moment would have
    produced a repo whose working tree silently disagreed with its own grid
    refs — the same failure run 2 found, arriving through a door the run-2 fix
    left open.

    The grid is the authority (**goal:g6.3** — the graph holds the bytes and
    the engine tree is what falls out), so the comparison is against
    `refs/grid/node/<mint-id>:payload` read straight out of the tree clone with
    plumbing. No import of `grid.py`: this check must keep working even if that
    module is mid-edit, which during an engine migration it plausibly is.

    A node with no grid ref yet is skipped rather than reported — it has no
    recorded bytes to disagree with, and `find_missing_payloads` already covers
    the case where its file is absent entirely.
    """
    engine = Path(engine).resolve()
    stale: set[str] = set()

    for node_path, ref in iter_payload_refs(tree):
        target = engine / ref
        if not target.is_file():
            continue  # find_missing_payloads owns this case
        mint_id = _read_mint_id(node_path)
        if not mint_id:
            continue
        res = subprocess.run(
            ["git", "-C", str(tree), "cat-file", "blob",
             f"refs/grid/node/{mint_id}:payload"],
            capture_output=True,
        )
        if res.returncode != 0:
            continue  # no grid ref yet — nothing recorded to disagree with
        if hashlib.sha256(res.stdout).hexdigest() != _sha256_file(target):
            stale.add(ref)

    return sorted(stale)


def _read_mint_id(node_path: Path) -> str | None:
    """`mint_id` from a node's frontmatter, or None. Grid refs key on the mint
    id rather than the address precisely so that a retag never renames a ref
    (**goal:g2.5**), so this is the only correct key to look a payload up by."""
    try:
        text = node_path.read_text(encoding="utf-8")
    except OSError:
        return None
    for line in text.split("\n", 200)[:200]:
        if line.startswith("mint_id:"):
            return line.split(":", 1)[1].strip() or None
        if line.strip() == "---" and not line.startswith("mint_id"):
            continue
    return None


def _sha256_file(path: Path) -> str:
    """sha256 of a file's bytes. Reads bytes, never text: a payload may be a
    binary or a symlink target and must not go through decoding."""
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


# --- safety: never the real repos -------------------------------------------

#: Defense in depth beyond operator discipline (see module docstring): these
#: two paths are never a legitimate `--engine`/`--tree`, regardless of
#: `--force`. Deliberately a literal path comparison, not a remote-URL check
#: — a throwaway clone's own `origin` can legitimately point at the same
#: GitHub repos these paths hold locally; what must never happen is *this
#: script writing into these two directories*.
_FORBIDDEN_REAL_PATHS = (
    Path("/home/ubuntu/work/agi"),
    Path("/home/ubuntu/work/agi-tree"),
)


def _touches_a_real_repo(path: Path) -> bool:
    resolved = Path(path).resolve()
    return any(resolved == forbidden.resolve() for forbidden in _FORBIDDEN_REAL_PATHS)


# --- 1. preflight ------------------------------------------------------------


def _refuse(reason: str, detail: str) -> dict:
    return {"ok": False, "reason": reason, "detail": detail}


def preflight(engine: Path, tree: Path, *, force: bool = False) -> dict:
    """Both source repos exist and are clean; the target is a fresh clone;
    record tip shas and grid-ref counts. Returns `{"ok": False, "reason":
    ..., "detail": ...}` on the first failing check — never a list, because
    the caller (`main`) reports exactly one thing to fix at a time, same as
    `CronsError` in `crons.py`.

    `force` bypasses three checks on the target (`engine`): an existing
    `.agi/`, a dirty working tree, and the publish-lag gate below. It never
    bypasses the real-repo guard, and never relaxes the requirement that the
    *source* (`tree`) be clean — there is no recovery scenario where reading
    from a dirty source is the right call.
    """
    engine = Path(engine).resolve()
    tree = Path(tree).resolve()

    if _touches_a_real_repo(engine) or _touches_a_real_repo(tree):
        return _refuse(
            "refuses_real_repo",
            f"{engine} or {tree} resolves to one of the real repos this "
            f"script must never write into — clone to /tmp and point there",
        )

    if not (engine / ".git").exists():
        return _refuse("engine_not_git_repo", f"{engine}: no .git — not a git repository")
    if not (tree / ".git").exists():
        return _refuse("tree_not_git_repo", f"{tree}: no .git — not a git repository")

    tree_status = _git(tree, "status", "--porcelain")
    if tree_status.strip():
        return _refuse("tree_dirty", f"{tree}: working tree is not clean")

    engine_status = _git(engine, "status", "--porcelain")
    if engine_status.strip() and not force:
        return _refuse(
            "engine_dirty",
            f"{engine}: working tree is not clean — pass --force only for recovery",
        )

    if (engine / locations.GRAPH_DIR_NAME).exists() and not force:
        return _refuse(
            "engine_has_agi_already",
            f"{engine}/{locations.GRAPH_DIR_NAME} already exists — target is "
            f"not a fresh clone; pass --force only for recovery",
        )

    # goal:g11, rehearsal run 2: unify.py builds the unified repo from the
    # ENGINE, and the engine is only as current as its last publish. Four
    # payload_refs did not resolve there because the graph was three commits
    # ahead of the last publish — nothing was lost (the bytes were in the
    # grid), but the migrated *working tree* was missing files the graph
    # correctly described, which is the worst state to debug later. Refuse
    # by default; --force is for deliberate recovery only.
    missing_payloads = find_missing_payloads(tree, engine)
    if missing_payloads and not force:
        sample = missing_payloads[:10]
        return {
            "ok": False,
            "reason": "engine_missing_payloads",
            "detail": (
                f"{len(missing_payloads)} payload_ref path(s) under "
                f"{tree}/nodes do not exist under {engine} — the engine is "
                f"behind the graph's last publish. Run publish-engine.sh "
                f"against the real engine checkout, then re-clone --engine "
                f"and retry. First {len(sample)}: {sample}"
            ),
            "missing_payload_count": len(missing_payloads),
            "missing_payload_sample": sample,
        }

    # The other half of the same gate, and the half a synthetic fixture will
    # not produce: a payload the engine HAS but at stale bytes. Same remedy,
    # same refusal, different question — "is it there" vs "is it current".
    stale_payloads = find_stale_payloads(tree, engine)
    if stale_payloads and not force:
        sample = stale_payloads[:10]
        return {
            "ok": False,
            "reason": "engine_stale_payloads",
            "detail": (
                f"{len(stale_payloads)} payload_ref path(s) exist under "
                f"{engine} but disagree with the grid — the engine holds an "
                f"older copy than the graph recorded. Migrating now would "
                f"carry those stale bytes onto disk while the grid refs "
                f"carry the current ones. Run publish-engine.sh against the "
                f"real engine checkout, then re-clone --engine and retry. "
                f"First {len(sample)}: {sample}"
            ),
            "stale_payload_count": len(stale_payloads),
            "stale_payload_sample": sample,
        }

    engine_tip = _git(engine, "rev-parse", "HEAD").strip()
    tree_tip = _git(tree, "rev-parse", "HEAD").strip()

    return {
        "ok": True,
        "reason": None,
        "engine": str(engine),
        "tree": str(tree),
        "engine_tip": engine_tip,
        "tree_tip": tree_tip,
        "engine_commit_count": int(_git(engine, "rev-list", "--count", "HEAD").strip()),
        "tree_commit_count": int(_git(tree, "rev-list", "--count", "HEAD").strip()),
        "engine_grid_ref_count": count_grid_refs(engine),
        "tree_grid_ref_count": count_grid_refs(tree),
        "tree_node_count": _node_count(tree / "nodes"),
        "force": force,
    }


# --- 2. graft ----------------------------------------------------------------


def graft_graph(engine: Path, tree: Path, *, remote_name: str = REMOTE_NAME) -> dict:
    """The standard subtree-merge recipe (goal:g11): `remote add`, `fetch`,
    `merge -s ours --no-commit --allow-unrelated-histories`, `read-tree
    --prefix=.agi/ -u`, `commit`. Asserts the tree's tip is an ancestor of the
    result afterward — "both histories preserved" is the whole point of doing
    it this way instead of a plain copy, so it is checked, not assumed.
    """
    engine = Path(engine).resolve()
    tree = Path(tree).resolve()

    tree_tip = _git(tree, "rev-parse", "HEAD").strip()
    engine_tip_before = _git(engine, "rev-parse", "HEAD").strip()
    branch = _resolve_branch(tree)

    existing_remotes = _git(engine, "remote").split()
    if remote_name in existing_remotes:
        # A retry after a partial failure left this remote behind; drop it
        # rather than fail on "remote already exists".
        _git(engine, "remote", "remove", remote_name)
    _git(engine, "remote", "add", remote_name, str(tree))
    _git(engine, "fetch", "-q", remote_name)

    _git(engine, "merge", "-s", "ours", "--no-commit", "--allow-unrelated-histories",
         f"{remote_name}/{branch}")
    _git(engine, "read-tree", f"--prefix={locations.GRAPH_DIR_NAME}/", "-u",
         f"{remote_name}/{branch}")
    _git(engine, "commit", "-m", GRAFT_COMMIT_MESSAGE)

    engine_tip_after = _git(engine, "rev-parse", "HEAD").strip()

    is_ancestor = _is_ancestor(engine, tree_tip, "HEAD")
    if not is_ancestor:
        raise UnifyError(
            f"graft_graph: {tree_tip} (tree's tip) is not an ancestor of HEAD "
            f"after the graft — the subtree merge did not preserve the tree's "
            f"history"
        )

    return {
        "engine_tip_before": engine_tip_before,
        "engine_tip_after": engine_tip_after,
        "tree_tip": tree_tip,
        "tree_branch": branch,
        "tree_history_preserved": is_ancestor,
        "remote_name": remote_name,
    }


# --- 3. relocate --------------------------------------------------------------


def _git_file_mode(repo: Path, relpath: str) -> str:
    """The git index mode of a tracked path, e.g. `120000` for a symlink,
    `100644` for a regular file. `git ls-files -s` is the source of truth
    for what git actually recorded — reading it back, rather than trusting
    `Path.is_symlink()` on disk, is the point: `commit_file()` in `grid.py`
    once mis-hashed a symlink as a regular file in this exact area (goal:s9),
    so this asks git directly instead of assuming a `git mv` preserved it.
    """
    out = _git(repo, "ls-files", "-s", relpath).strip()
    if not out:
        raise UnifyError(f"_git_file_mode: {relpath!r} is not a tracked file in {repo}")
    return out.split()[0]


def relocate_files(engine: Path) -> dict:
    """`.agi/GOALS.md` -> `GOALS.md`, `.agi/CLAUDE.md` -> `CLAUDE.md`,
    `.agi/AGENTS.md` -> `AGENTS.md` (`goals_path()` under this layout is a
    bare `goals_file` name at the repo root, never inside the dot directory,
    and CLAUDE.md/AGENTS.md belong beside it for the same reason: the
    documents a human or an agent opens first must not be hidden in a dot
    directory), `.agi/<config name>` -> `.agi/config.json`. All via `git mv`,
    one commit, so history follows every file. Accepts either config
    filename `locations.py` still reads (`CONFIG_NAMES`) rather than
    hardcoding the canonical one, since a project mid-rename-window could
    carry the legacy name.

    CLAUDE.md and AGENTS.md are required, not optional: this is the fix for
    a regression the migration used to introduce silently (the unified repo
    root ending up with no CLAUDE.md at all), so a tree missing either one
    fails loudly here rather than producing that same regression again.
    AGENTS.md is a symlink to CLAUDE.md (goal:s9) — its mode is checked
    before and after the move so the migration is never the thing that turns
    it into a plain-file copy.
    """
    engine = Path(engine).resolve()
    graph_dir = engine / locations.GRAPH_DIR_NAME

    goals_src = graph_dir / "GOALS.md"
    if not goals_src.exists():
        raise UnifyError(f"relocate_files: expected {goals_src} after the graft, not found")

    claude_src = graph_dir / "CLAUDE.md"
    if not claude_src.exists():
        raise UnifyError(f"relocate_files: expected {claude_src} after the graft, not found")

    agents_src = graph_dir / "AGENTS.md"
    if not (agents_src.exists() or agents_src.is_symlink()):
        raise UnifyError(f"relocate_files: expected {agents_src} after the graft, not found")
    agents_src_rel = str(agents_src.relative_to(engine))
    agents_src_mode = _git_file_mode(engine, agents_src_rel)
    if agents_src_mode != SYMLINK_MODE:
        raise UnifyError(
            f"relocate_files: {agents_src_rel} is tracked with mode "
            f"{agents_src_mode}, not a symlink ({SYMLINK_MODE}) — refusing "
            f"to relocate it as one"
        )

    config_src = None
    for name in locations.CONFIG_NAMES:
        cand = graph_dir / name
        if cand.exists():
            config_src = cand
            break
    if config_src is None:
        raise UnifyError(
            f"relocate_files: no config file found under {graph_dir} "
            f"(looked for {list(locations.CONFIG_NAMES)})"
        )

    goals_dst = engine / "GOALS.md"
    claude_dst = engine / "CLAUDE.md"
    agents_dst = engine / "AGENTS.md"
    config_dst = graph_dir / "config.json"

    _git(engine, "mv", str(goals_src.relative_to(engine)), str(goals_dst.relative_to(engine)))
    _git(engine, "mv", str(claude_src.relative_to(engine)), str(claude_dst.relative_to(engine)))
    _git(engine, "mv", agents_src_rel, str(agents_dst.relative_to(engine)))
    _git(engine, "mv", str(config_src.relative_to(engine)), str(config_dst.relative_to(engine)))

    agents_dst_mode = _git_file_mode(engine, str(agents_dst.relative_to(engine)))
    if agents_dst_mode != SYMLINK_MODE:
        raise UnifyError(
            f"relocate_files: AGENTS.md lost its symlink mode during the "
            f"move ({agents_src_mode} -> {agents_dst_mode})"
        )

    _git(engine, "commit", "-m", RELOCATE_COMMIT_MESSAGE)

    return {
        "moved": [
            {"from": str(goals_src.relative_to(engine)), "to": str(goals_dst.relative_to(engine))},
            {"from": str(claude_src.relative_to(engine)), "to": str(claude_dst.relative_to(engine))},
            {"from": agents_src_rel, "to": str(agents_dst.relative_to(engine))},
            {"from": str(config_src.relative_to(engine)), "to": str(config_dst.relative_to(engine))},
        ],
        "agents_md_mode": agents_dst_mode,
    }


# --- 4. gitignore merge (pure) -----------------------------------------------

#: Any block whose only pattern is one of these is dropped in its entirety —
#: comment included — because the block's sole reason to exist was that
#: symlink, and goal:g11 removes both (`agi-tree/agi` and `agi/agi-tree`).
_DROP_WHOLE_BLOCK = {"agi", "agi-tree"}

#: The graph's own generated-file paths. Checked (and rewritten) *before* the
#: duplicate check below, deliberately: some of these names are also bare
#: entries in the engine's own `.gitignore` today (`sessions/`, `loop.log`)
#: with a different, unrelated meaning — the engine's own generated files at
#: the engine's own root. Re-rooting must win over dedup, or the graph's
#: entry would be silently dropped as a "duplicate" of something that, after
#: the move, no longer names the same file at all.
_REROOT = {
    "sessions/": ".agi/sessions/",
    "context/INJECTION.md": ".agi/context/INJECTION.md",
    "context/publish-state.json": ".agi/context/publish-state.json",
    "nodes.db": ".agi/nodes.db",
    ".chain_cache.pkl": ".agi/.chain_cache.pkl",
    "loop.log": ".agi/loop.log",
    "payloads/": ".agi/payloads/",
}


def _gitignore_blocks(text: str) -> list[list[str]]:
    """Blank-line-separated blocks, source order preserved. Both files use one
    blank line between an explanation and the pattern(s) it explains, so a
    block is the unit "comment(s) + what they justify" — the unit this merge
    needs to keep or drop as one, to honor "preserve the explanatory
    comments" without orphaning one from a pattern it no longer sits next to.
    """
    blocks: list[list[str]] = []
    current: list[str] = []
    for line in text.splitlines():
        if line.strip() == "":
            if current:
                blocks.append(current)
                current = []
            continue
        current.append(line)
    if current:
        blocks.append(current)
    return blocks


def _block_patterns(block: list[str]) -> list[str]:
    return [l.strip() for l in block if l.strip() and not l.strip().startswith("#")]


def _filter_graph_block(block: list[str], *, dedupe_against: set[str]) -> list[str] | None:
    """One block from the GRAPH's `.gitignore`, filtered for the merge.
    `None` means the block disappears: either it is the `agi` block, or every
    pattern in it turned out to duplicate something the engine's own
    `.gitignore` already ignores repo-wide — keeping a comment with nothing
    left to explain would be worse than dropping both.
    """
    if any(p in _DROP_WHOLE_BLOCK for p in _block_patterns(block)):
        return None

    kept: list[str] = []
    survivors = 0
    for line in block:
        s = line.strip()
        if not s or s.startswith("#"):
            kept.append(line)
            continue
        if s in _REROOT:
            kept.append(_REROOT[s])
            survivors += 1
            continue
        if s in dedupe_against:
            continue  # already ignored repo-wide by the engine's own entry
        kept.append(line)
        survivors += 1

    return kept if survivors else None


def merge_gitignore(tree_text: str, engine_text: str) -> str:
    """One `.gitignore` for the unified repo root (goal:g11 step 4). Pure —
    no filesystem, no git — so it is tested directly on strings as well as
    through the end-to-end migration.

    The engine's blocks pass through unchanged except for dropping the
    `agi-tree` block (the symlink this merge deletes). The graph's blocks are
    then appended, each filtered by `_filter_graph_block`: the `agi` block
    dropped for the same reason, generated-file paths re-rooted under
    `.agi/` (`_REROOT`), and any pattern the engine already covers repo-wide
    dropped as a duplicate (`__pycache__/`, `.claude/worktrees/`, ...).
    Everything else survives byte-for-byte, comments included.
    """
    engine_blocks = [
        b for b in _gitignore_blocks(engine_text)
        if not any(p in _DROP_WHOLE_BLOCK for p in _block_patterns(b))
    ]
    engine_patterns = {p for b in engine_blocks for p in _block_patterns(b)}

    tree_blocks = []
    for block in _gitignore_blocks(tree_text):
        filtered = _filter_graph_block(block, dedupe_against=engine_patterns)
        if filtered is not None:
            tree_blocks.append(filtered)

    merged_blocks = engine_blocks + tree_blocks
    return "\n\n".join("\n".join(b) for b in merged_blocks) + "\n"


def write_merged_gitignore(engine: Path) -> dict:
    """Read `<engine>/.gitignore` and the grafted `<engine>/.agi/.gitignore`,
    merge them with `merge_gitignore`, write the result at the repo root, and
    remove the now-redundant nested copy. One commit."""
    engine = Path(engine).resolve()
    tree_gitignore = engine / locations.GRAPH_DIR_NAME / ".gitignore"
    engine_gitignore = engine / ".gitignore"

    tree_text = tree_gitignore.read_text(encoding="utf-8") if tree_gitignore.exists() else ""
    engine_text = engine_gitignore.read_text(encoding="utf-8") if engine_gitignore.exists() else ""

    merged = merge_gitignore(tree_text, engine_text)
    engine_gitignore.write_text(merged, encoding="utf-8")
    _git(engine, "add", ".gitignore")

    removed_nested = False
    if tree_gitignore.exists():
        _git(engine, "rm", "-q", str(tree_gitignore.relative_to(engine)))
        removed_nested = True

    _git(engine, "commit", "-m", GITIGNORE_COMMIT_MESSAGE)
    return {
        "merged_gitignore": str(engine_gitignore.relative_to(engine)),
        "removed_nested_gitignore": removed_nested,
    }


# --- 5. grid refs -------------------------------------------------------------


def fetch_grid_refs(engine: Path, tree: Path, *, remote_name: str = REMOTE_NAME) -> dict:
    """`git fetch <remote> 'refs/grid/*:refs/grid/*'`, then assert the
    target's count now equals the source's. A grid ref is the only home of
    every payload byte (goal:g7) — losing one here is unrecoverable, so this
    is the one stage that raises on a mismatch instead of just reporting it.
    """
    engine = Path(engine).resolve()
    tree = Path(tree).resolve()

    before = count_grid_refs(engine)
    source_count = count_grid_refs(tree)
    _git(engine, "fetch", "-q", remote_name, GRID_FETCH_REFSPEC)
    after = count_grid_refs(engine)

    if after != source_count:
        raise UnifyError(
            f"fetch_grid_refs: expected {source_count} grid refs after fetch "
            f"(the source's count), target now has {after}"
        )

    return {"grid_refs_before": before, "grid_refs_after": after, "source_count": source_count}


def remove_temp_remote(engine: Path, remote_name: str = REMOTE_NAME) -> dict:
    """Drop the remote `graft_graph` added. Nothing in the unified repo
    should point at wherever the tree happened to be cloned for this run."""
    _git(engine, "remote", "remove", remote_name)
    return {"remote_removed": remote_name}


# --- 0. pre-state, for --rollback (rehearsal run 4) --------------------------


def prestate_path(engine: Path) -> Path:
    """Where the pre-migration snapshot lives — inside `.git/`, never the
    working tree. A rollback's own first two operations (`reset --hard`,
    `clean -fd`) rewrite everything the working tree holds; the one thing
    recovery cannot survive losing is the file that describes how to
    recover, so it goes where neither operation reaches."""
    return Path(engine).resolve() / ".git" / PRESTATE_FILENAME


def write_prestate(engine: Path) -> dict:
    """Snapshot `engine`'s state before any mutating stage runs: HEAD, every
    ref with its sha, and a timestamp. **This is the load-bearing step for
    `--rollback`** — the pre-migration HEAD stops being reachable from any
    branch the instant the migration commits, so it must be written down
    here, not re-derived later from a memory nothing will have.
    """
    engine = Path(engine).resolve()
    data = {
        "head": _git(engine, "rev-parse", "HEAD").strip(),
        "refs": _all_refs(engine),
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    prestate_path(engine).write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return data


def read_prestate(engine: Path) -> dict:
    """The snapshot `write_prestate` recorded, or `UnifyError` if it is
    missing or unreadable — `--rollback`'s first refusal: no snapshot means
    this repo was never migrated by this script, or the snapshot has already
    been consumed by a previous rollback and the caller is retrying."""
    path = prestate_path(engine)
    if not path.exists():
        raise UnifyError(
            f"read_prestate: no {path} — this repo was not migrated by "
            f"unify.py, or its pre-state snapshot is gone"
        )
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        raise UnifyError(f"read_prestate: {path} is not valid JSON: {exc}") from exc
    if not isinstance(data, dict) or "head" not in data or "refs" not in data:
        raise UnifyError(f"read_prestate: {path} is missing required keys (head, refs)")
    return data


def _head_reachable_from_any_remote(engine: Path, head: str) -> list[str]:
    """Remote-tracking refs (`refs/remotes/*`) that already have `head` as an
    ancestor — the pushed case. Non-empty means the migration has left this
    clone for a shared remote, so reversing it now needs a force-push against
    published history rather than a private `git reset` (goal:g11's stated
    condition: do not push until verified)."""
    engine = Path(engine).resolve()
    out = _git(engine, "for-each-ref", "--format=%(refname)", REMOTE_REF_NAMESPACE)
    return [
        ref for ref in (line.strip() for line in out.splitlines())
        if ref and _is_ancestor(engine, head, ref)
    ]


def preflight_rollback(engine: Path, *, force: bool = False) -> dict:
    """Read-only checks before `perform_rollback` touches anything. Returns
    the same `{"ok": False, "reason": ..., "detail": ...}` shape as
    `preflight` on the first failing check, or `{"ok": True, ...}` with the
    prestate and what would be undone.

    `force` overrides exactly one of these: the pushed-history check. It
    never overrides "no pre-state file" or "HEAD is not a descendant of the
    recorded pre-migration HEAD" — there is no recovery gesture for either;
    the first means this was never migrated (or already rolled back) and the
    second means this is not the repo unify.py touched.
    """
    engine = Path(engine).resolve()

    if _touches_a_real_repo(engine):
        return _refuse(
            "refuses_real_repo",
            f"{engine} resolves to one of the real repos this script must "
            f"never mutate",
        )

    if not (engine / ".git").exists():
        return _refuse("engine_not_git_repo", f"{engine}: no .git — not a git repository")

    try:
        prestate = read_prestate(engine)
    except UnifyError as exc:
        return _refuse("rollback_no_prestate", str(exc))

    pre_head = prestate["head"]
    current_head = _git(engine, "rev-parse", "HEAD").strip()

    if current_head == pre_head:
        return _refuse(
            "rollback_nothing_to_undo",
            f"{engine}: HEAD already equals the recorded pre-migration HEAD "
            f"{pre_head[:12]} — already rolled back, or never migrated",
        )

    if not _is_ancestor(engine, pre_head, current_head):
        return _refuse(
            "rollback_not_descendant",
            f"{engine}: HEAD ({current_head[:12]}) is not a descendant of "
            f"the recorded pre-migration HEAD ({pre_head[:12]}) — this is "
            f"not the repo unify.py migrated, or its history has since been "
            f"rewritten",
        )

    pushed_to = _head_reachable_from_any_remote(engine, current_head)
    if pushed_to and not force:
        return _refuse(
            "rollback_pushed",
            f"{engine}: the migrated HEAD {current_head[:12]} is already "
            f"reachable from {len(pushed_to)} remote-tracking ref(s) "
            f"({pushed_to[:5]}) — rolling back now needs a force-push "
            f"against published history, a materially worse operation; "
            f"pass --force only if that is exactly what is intended",
        )

    return {
        "ok": True,
        "reason": None,
        "engine": str(engine),
        "prestate": prestate,
        "current_head": current_head,
        "grid_refs_to_delete": sorted(
            r for r in _all_refs(engine) if r.startswith(GRID_REF_NAMESPACE + "/")
        ),
        "pushed_to": pushed_to,
        "force": force,
    }


def perform_rollback(engine: Path, pre: dict) -> dict:
    """The four operations rehearsal run 4 found necessary, given an already
    -validated `preflight_rollback` report:

        git reset --hard <pre-migration HEAD>
        git for-each-ref --format='delete %(refname)' refs/grid/ |
            git update-ref --stdin
        git clean -fd
        <remove the temporary remote, if the migrator did not>

    The second line is the one reasoning about `git reset` missed: it does
    nothing to `refs/grid/*`. Those arrive by fetch and survive a branch
    reset, so a rollback that omitted this line would leave the repo holding
    every grid ref from a migration that supposedly did not happen — neither
    the old state nor the new one.
    """
    engine = Path(engine).resolve()
    pre_head = pre["prestate"]["head"]

    _git(engine, "reset", "--hard", pre_head)

    delete_cmds = _git(engine, "for-each-ref", "--format=delete %(refname)", GRID_REF_NAMESPACE)
    if delete_cmds.strip():
        _git_stdin(engine, ["update-ref", "--stdin"], delete_cmds)

    _git(engine, "clean", "-fd")

    remote_removed = False
    if REMOTE_NAME in _git(engine, "remote").split():
        _git(engine, "remote", "remove", REMOTE_NAME)
        remote_removed = True

    return {
        "ok": True,
        "dry_run": False,
        "mutated": True,
        "engine": str(engine),
        "reset_to": pre_head,
        "grid_refs_deleted": len([ln for ln in delete_cmds.splitlines() if ln.strip()]),
        "remote_removed": remote_removed,
        "pushed_to": pre["pushed_to"],
        "forced_past_push": bool(pre["pushed_to"]),
    }


def run_rollback(engine: Path, *, yes: bool = False, force: bool = False) -> dict:
    """`--rollback`'s entry point, mirroring `run_unify`'s dry-run-by-default
    shape: `preflight_rollback` runs unconditionally; `yes=False` returns a
    plan built from its read-only data, `yes=True` performs the four
    operations and returns their result.
    """
    engine = Path(engine).resolve()

    pre = preflight_rollback(engine, force=force)
    if not pre["ok"]:
        return {"ok": False, "stage": "preflight_rollback", "reason": pre["reason"],
                "detail": pre["detail"], "preflight": pre}

    if not yes:
        return {
            "ok": True,
            "dry_run": True,
            "mutated": False,
            "preflight": pre,
            "would_reset_to": pre["prestate"]["head"],
            "would_delete_grid_refs": len(pre["grid_refs_to_delete"]),
            "pushed_to": pre["pushed_to"],
        }

    try:
        return perform_rollback(engine, pre)
    except UnifyError as exc:
        return {"ok": False, "stage": "rollback", "reason": str(exc), "preflight": pre}


# --- orchestration ------------------------------------------------------------


def _would_relocate(tree: Path) -> list[dict]:
    """Preview of `relocate_files`'s moves, read straight off the tree's own
    root before the graft (where these files sit pre-migration). CLAUDE.md
    and AGENTS.md are previewed conditionally — `relocate_files` itself
    requires them, but a dry-run report should describe what a given tree
    actually has rather than assert on it, so a plan never raises."""
    tree = Path(tree)
    moves = [
        {"from": f"{locations.GRAPH_DIR_NAME}/GOALS.md", "to": "GOALS.md"},
    ]
    if (tree / "CLAUDE.md").exists():
        moves.append({"from": f"{locations.GRAPH_DIR_NAME}/CLAUDE.md", "to": "CLAUDE.md"})
    agents = tree / "AGENTS.md"
    if agents.exists() or agents.is_symlink():
        moves.append({"from": f"{locations.GRAPH_DIR_NAME}/AGENTS.md", "to": "AGENTS.md"})
    moves.append({"from": f"{locations.GRAPH_DIR_NAME}/agi-tree.config.json",
                  "to": f"{locations.GRAPH_DIR_NAME}/config.json"})
    return moves


def _plan(engine: Path, tree: Path, pre: dict) -> dict:
    """The dry-run report: everything computable read-only from `pre` plus a
    real preview of the merged `.gitignore` (pure function, needs no git
    state beyond the two files as they already sit on disk). No mutation of
    `engine` happens to produce this — not even a `git remote add`.
    """
    tree_gitignore = Path(tree) / ".gitignore"
    engine_gitignore = Path(engine) / ".gitignore"
    tree_text = tree_gitignore.read_text(encoding="utf-8") if tree_gitignore.exists() else ""
    engine_text = engine_gitignore.read_text(encoding="utf-8") if engine_gitignore.exists() else ""

    return {
        "ok": True,
        "dry_run": True,
        "mutated": False,
        "preflight": pre,
        "would_graft": {"tree_tip": pre["tree_tip"], "onto_engine_tip": pre["engine_tip"]},
        "would_relocate": _would_relocate(tree),
        "would_fetch_grid_refs": pre["tree_grid_ref_count"],
        "gitignore_preview": merge_gitignore(tree_text, engine_text),
        "node_count": pre["tree_node_count"],
    }


def _summarize(engine: Path, pre: dict, stages: dict) -> dict:
    engine = Path(engine).resolve()
    root = locations.find_project_root(engine)
    return {
        "ok": True,
        "dry_run": False,
        "mutated": True,
        "commits_before": pre["engine_commit_count"],
        "commits_after": int(_git(engine, "rev-list", "--count", "HEAD").strip()),
        "tree_commit_count": pre["tree_commit_count"],
        "grid_refs_before": pre["engine_grid_ref_count"],
        "grid_refs_after": count_grid_refs(engine),
        "node_count": _node_count(engine / locations.GRAPH_DIR_NAME / "nodes"),
        "files_moved": stages["relocate"]["moved"],
        "project_root_resolved": str(root) if root else None,
        "project_root_correct": root == (engine / locations.GRAPH_DIR_NAME),
        "graft": stages["graft"],
        "gitignore": stages["gitignore"],
        "prestate_file": str(prestate_path(engine)),
        "prestate_head": stages["prestate"]["head"],
    }


def run_unify(engine: Path, tree: Path, *, yes: bool = False, force: bool = False) -> dict:
    """The whole pipeline. `yes=False` (the default) never mutates `engine`
    or `tree` — it runs `preflight` and, if that passes, returns a plan built
    from `preflight`'s own read-only data. `yes=True` runs every mutating
    stage against `engine` in order and returns a summary; a failure partway
    stops immediately and reports which stage and why, with whatever stages
    already succeeded included under `"stages"`.
    """
    engine = Path(engine).resolve()
    tree = Path(tree).resolve()

    pre = preflight(engine, tree, force=force)
    if not pre["ok"]:
        return {"ok": False, "stage": "preflight", "reason": pre["reason"],
                "detail": pre["detail"], "preflight": pre}

    if not yes:
        return _plan(engine, tree, pre)

    stages: dict = {}
    try:
        # Written first, and outside any stage that could partially fail: the
        # whole point is a snapshot of `engine` before anything below touches
        # it, so --rollback has ground truth even if a later stage errors.
        stages["prestate"] = write_prestate(engine)
        stages["graft"] = graft_graph(engine, tree)
        stages["relocate"] = relocate_files(engine)
        stages["gitignore"] = write_merged_gitignore(engine)
        stages["grid_refs"] = fetch_grid_refs(engine, tree)
        stages["remote_cleanup"] = remove_temp_remote(engine)
    except UnifyError as exc:
        return {"ok": False, "stage": "mutate", "reason": str(exc),
                "preflight": pre, "stages": stages}

    return _summarize(engine, pre, stages)


# --- cli ----------------------------------------------------------------------


def _print_human(report: dict) -> None:
    if not report.get("ok"):
        print(f"unify: REFUSED at stage {report.get('stage')}: {report.get('reason')}")
        if report.get("detail"):
            print(f"  {report['detail']}")
        return
    if report.get("dry_run"):
        pre = report["preflight"]
        print("unify: DRY RUN (pass --yes to mutate)")
        print(f"  would graft tree tip {pre['tree_tip'][:12]} under "
              f"{locations.GRAPH_DIR_NAME}/ onto engine tip {pre['engine_tip'][:12]}")
        for m in report["would_relocate"]:
            print(f"  would move {m['from']} -> {m['to']}")
        print(f"  would fetch {report['would_fetch_grid_refs']} grid ref(s)")
        print(f"  node count: {report['node_count']}")
        return
    print("unify: DONE")
    print(f"  commits: {report['commits_before']} -> {report['commits_after']} "
          f"(+{report['tree_commit_count']} from the tree)")
    print(f"  grid refs: {report['grid_refs_before']} -> {report['grid_refs_after']}")
    print(f"  node count under {locations.GRAPH_DIR_NAME}/nodes: {report['node_count']}")
    for m in report["files_moved"]:
        print(f"  moved {m['from']} -> {m['to']}")
    print(f"  project root resolves to: {report['project_root_resolved']} "
          f"({'correct' if report['project_root_correct'] else 'WRONG'})")
    print(f"  pre-migration state recorded at {report['prestate_file']} "
          f"(HEAD {report['prestate_head'][:12]}) — needed by --rollback")


def _print_human_rollback(report: dict) -> None:
    if not report.get("ok"):
        print(f"unify --rollback: REFUSED at stage {report.get('stage')}: {report.get('reason')}")
        if report.get("detail"):
            print(f"  {report['detail']}")
        return
    if report.get("dry_run"):
        print("unify --rollback: DRY RUN (pass --yes to mutate)")
        print(f"  would reset HEAD to {report['would_reset_to'][:12]}")
        print(f"  would delete {report['would_delete_grid_refs']} refs/grid/* ref(s)")
        if report["pushed_to"]:
            print(f"  WARNING: migrated HEAD is reachable from {report['pushed_to']} "
                  f"— rollback needs --force and a force-push afterward")
        return
    print("unify --rollback: DONE")
    print(f"  reset to {report['reset_to'][:12]}")
    print(f"  deleted {report['grid_refs_deleted']} refs/grid/* ref(s)")
    print(f"  temporary remote removed: {report['remote_removed']}")
    if report["forced_past_push"]:
        print(f"  WARNING: this rollback overrode the pushed-history check "
              f"for {report['pushed_to']} — a force-push is now needed to "
              f"make the remote agree with local history")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Merge the two-repo layout into one (goal:g11). Dry-run "
                     "by default; pass --yes to mutate --engine.")
    ap.add_argument("--engine", required=True,
                    help="path to a throwaway clone of the engine repo — the "
                         "migration target, or the repo to reverse under --rollback")
    ap.add_argument("--tree",
                    help="path to a throwaway clone of the graph repo — source "
                         "only, never mutated. Required unless --rollback")
    ap.add_argument("--rollback", action="store_true",
                    help="reverse a previous migration on --engine instead of "
                         "performing one; reads the pre-state file unify.py wrote")
    ap.add_argument("--yes", action="store_true",
                    help="perform the migration or rollback; omit for a dry-run report only")
    ap.add_argument("--dry-run", action="store_true",
                    help="force a dry run even if --yes is also given")
    ap.add_argument("--force", action="store_true",
                    help="proceed against a target that already has .agi/, is "
                         "not clean, or has payload_refs missing from the engine "
                         "(migration mode); or override the pushed-history check "
                         "(--rollback mode). Recovery only, never bypasses the "
                         "real-repo guard")
    ap.add_argument("--report-json", action="store_true",
                    help="print the result as JSON instead of a human-readable summary")
    args = ap.parse_args(argv)

    if not args.rollback and not args.tree:
        ap.error("--tree is required unless --rollback is given")

    mutate = args.yes and not args.dry_run

    try:
        if args.rollback:
            report = run_rollback(Path(args.engine), yes=mutate, force=args.force)
        else:
            report = run_unify(Path(args.engine), Path(args.tree), yes=mutate, force=args.force)
    except UnifyError as exc:
        print(f"ERR: unify.py: {exc}", file=sys.stderr)
        return 1

    if args.report_json:
        print(json.dumps(report, indent=2, default=str))
    elif args.rollback:
        _print_human_rollback(report)
    else:
        _print_human(report)

    return 0 if report.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
