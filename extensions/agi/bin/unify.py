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

    1. preflight            both source repos clean; target is a fresh clone
    2. graft                subtree-merge the tree's history under `.agi/`
    3. relocate             `.agi/GOALS.md` -> `GOALS.md`, config -> `.agi/config.json`
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
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import locations  # noqa: E402

# Every git invocation below carries its own identity rather than relying on
# the ambient `user.name`/`user.email` — a throwaway clone made purely for a
# rehearsal has no reason to have either configured, and `grid.py` sets the
# same precedent (`GIT_IDENT`) for exactly that reason.
GIT_IDENT = ["-c", "user.name=agi-unify", "-c", "user.email=agi-unify@agi"]

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
    "goal:g11 — relocate GOALS.md to the repo root, config into .agi/\n\n"
    "git mv, so history follows both files."
)
GITIGNORE_COMMIT_MESSAGE = (
    "goal:g11 — merge the two .gitignore files into one at the repo root"
)


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

    `force` only bypasses the two "is this a fresh clone" checks on the
    target (`engine`): an existing `.agi/` and a dirty working tree. It never
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

    is_ancestor = subprocess.run(
        ["git", "-C", str(engine), "merge-base", "--is-ancestor", tree_tip, "HEAD"],
    ).returncode == 0
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


def relocate_files(engine: Path) -> dict:
    """`.agi/GOALS.md` -> `GOALS.md` (`goals_path()` under this layout is a
    bare `goals_file` name at the repo root, never inside the dot directory),
    `.agi/<config name>` -> `.agi/config.json`. Both via `git mv`, one commit,
    so history follows. Accepts either config filename `locations.py` still
    reads (`CONFIG_NAMES`) rather than hardcoding the canonical one, since a
    project mid-rename-window could carry the legacy name.
    """
    engine = Path(engine).resolve()
    graph_dir = engine / locations.GRAPH_DIR_NAME

    goals_src = graph_dir / "GOALS.md"
    if not goals_src.exists():
        raise UnifyError(f"relocate_files: expected {goals_src} after the graft, not found")

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
    config_dst = graph_dir / "config.json"

    _git(engine, "mv", str(goals_src.relative_to(engine)), str(goals_dst.relative_to(engine)))
    _git(engine, "mv", str(config_src.relative_to(engine)), str(config_dst.relative_to(engine)))
    _git(engine, "commit", "-m", RELOCATE_COMMIT_MESSAGE)

    return {
        "moved": [
            {"from": str(goals_src.relative_to(engine)), "to": str(goals_dst.relative_to(engine))},
            {"from": str(config_src.relative_to(engine)), "to": str(config_dst.relative_to(engine))},
        ],
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


# --- orchestration ------------------------------------------------------------


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
        "would_relocate": [
            {"from": f"{locations.GRAPH_DIR_NAME}/GOALS.md", "to": "GOALS.md"},
            {"from": f"{locations.GRAPH_DIR_NAME}/agi-tree.config.json",
             "to": f"{locations.GRAPH_DIR_NAME}/config.json"},
        ],
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


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Merge the two-repo layout into one (goal:g11). Dry-run "
                     "by default; pass --yes to mutate --engine.")
    ap.add_argument("--engine", required=True,
                    help="path to a throwaway clone of the engine repo — the migration target")
    ap.add_argument("--tree", required=True,
                    help="path to a throwaway clone of the graph repo — source only, never mutated")
    ap.add_argument("--yes", action="store_true",
                    help="perform the migration; omit for a dry-run report only")
    ap.add_argument("--dry-run", action="store_true",
                    help="force a dry run even if --yes is also given")
    ap.add_argument("--force", action="store_true",
                    help="proceed against a target that already has .agi/ or is "
                         "not clean — recovery only, never bypasses the real-repo guard")
    ap.add_argument("--report-json", action="store_true",
                    help="print the result as JSON instead of a human-readable summary")
    args = ap.parse_args(argv)

    mutate = args.yes and not args.dry_run

    try:
        report = run_unify(Path(args.engine), Path(args.tree), yes=mutate, force=args.force)
    except UnifyError as exc:
        print(f"ERR: unify.py: {exc}", file=sys.stderr)
        return 1

    if args.report_json:
        print(json.dumps(report, indent=2, default=str))
    else:
        _print_human(report)

    return 0 if report.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
