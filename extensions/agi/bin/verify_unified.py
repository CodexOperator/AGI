#!/usr/bin/env python3
"""verify_unified.py — did the goal:g11 migration lose anything?

**goal:g11, goal:g7** — nothing the loop produces is ever silently lost.
`unify.py` moves a graph repo (`nodes/`, `GOALS.md`, `refs/grid/*`) inside the
source tree it describes, collapsing `<project>/<project>-tree/agi` into one
repo with `.agi/` holding the graph. That is exactly the kind of rewrite that
has cost this project a 29,264-node corpus before (H0/H0b) — twice, from a
project-local script that shadowed the engine's safe one and a snapshot that
silently pruned what it did not re-derive.

This module is deliberately **not** part of `unify.py` and imports nothing
from it. If the same bug shaped the migration and the check, the check would
pass while the migration was wrong — the two are written by different people,
in different files, against the CONTRACT the migration is supposed to meet,
not against each other's code. `main()` never touches disk except to read: no
`open(..., "w")`, no `git commit`/`update-ref`/`checkout`, nothing. It answers
one question — before vs. after, pass or fail per invariant — and exits
nonzero the moment any invariant does not hold.

## The eight invariants

1. `no_node_lost`            — `*.md` count under `nodes/` == under `.agi/nodes/`.
2. `no_node_bytes_changed`   — sha256 of every node file, unchanged path for path.
3. `no_grid_ref_lost`        — `refs/grid/*` unchanged: same names, same target
                                shas. Missing / extra / diverged are reported
                                separately because they are different failures:
                                missing is data loss, extra is unexplained
                                growth, diverged is the same name now pointing
                                somewhere else — silently rewritten history.
4. `both_histories_present`  — `<before>`'s tip is an ancestor of `<after>`'s
                                HEAD, so the migration commit sits ON TOP of
                                the graph's own history rather than replacing
                                it.
5. `resolver_agrees`         — `locations.py` (the sibling module this file
                                imports the same way `crons.py` does) resolves
                                `<after>` the way the `.agi` layout promises:
                                project root is `<after>/.agi`, and both
                                `repo_root` and `source_root` come back to
                                `<after>` itself.
6. `goals_at_repo_root`      — `GOALS.md` lives at `<after>/GOALS.md`, not
                                inside `.agi/` where it would be invisible to
                                a human opening the repo.
7. `payload_refs_resolve`    — every build node's `payload_ref` still resolves
                                under `<after>`. This is the check that would
                                catch the module docstring's central claim —
                                "the migration rewrites zero node files because
                                `payload_ref` is relative to the engine root
                                and `source_root` still resolves there" — being
                                wrong for even one node.
8. `config_at_expected_path` — `<after>/.agi/config.json` exists and parses.

Every check function takes plain `Path`s and returns a `CheckResult`; `main()`
wraps each in `_safe()` so a check that hits a genuinely broken repo (no
`.git`, no `nodes/`, unreadable YAML) reports FAIL with a reason instead of
taking the whole run down with a traceback — "fails loudly, named" beats
"doesn't run at all" for a tool whose entire job is to be trusted after
something destructive already happened.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

sys.path.insert(0, str(Path(__file__).resolve().parent))
import locations  # noqa: E402
from frontmatter import split_frontmatter  # noqa: E402

import yaml

#: Same constant `locations.py` uses for the graph directory G11 moves the
#: tree into. Imported, not restated, so a rename of the directory only ever
#: has to happen in one file.
GRAPH_DIR_NAME = locations.GRAPH_DIR_NAME


class CheckResult:
    """One named invariant's verdict. `detail` is always JSON-serializable —
    plain strs, ints, bools, lists — so `--json` never needs a custom encoder."""

    def __init__(self, name: str, passed: bool, message: str,
                 detail: dict[str, Any] | None = None):
        self.name = name
        self.passed = passed
        self.message = message
        self.detail = detail or {}

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "passed": self.passed,
                "message": self.message, "detail": self.detail}


# --- git plumbing: read-only, every call --------------------------------


def _git(repo: Path, *args: str) -> str:
    """Run a git subcommand and return stdout, raising on failure. Every
    argument list here is a read command (`rev-parse`, `for-each-ref`,
    `merge-base --is-ancestor`) — nothing in this module ever calls `commit`,
    `checkout`, `update-ref`, or `reset`. That is the whole safety story for
    a tool whose job is to run against a repo something else just wrote to."""
    res = subprocess.run(["git", "-C", str(repo), *args],
                          capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(
            f"git -C {repo} {' '.join(args)} failed: {res.stderr.strip()}")
    return res.stdout


def _rev_parse(repo: Path, rev: str = "HEAD") -> str | None:
    """`None` rather than raising: a repo with no commits yet, or that is not
    a git repo at all, is a normal input to describe as a failure, not a
    reason for this process to crash."""
    res = subprocess.run(["git", "-C", str(repo), "rev-parse", rev],
                          capture_output=True, text=True)
    return res.stdout.strip() if res.returncode == 0 else None


def _grid_refs(repo: Path) -> dict[str, str]:
    """`{refname: target sha}` for every ref under `refs/grid/`."""
    out = _git(repo, "for-each-ref", "refs/grid/", "--format=%(refname) %(objectname)")
    refs: dict[str, str] = {}
    for line in out.splitlines():
        line = line.strip()
        if not line:
            continue
        name, sha = line.rsplit(" ", 1)
        refs[name] = sha
    return refs


# --- node frontmatter -----------------------------------------------------


def _read_frontmatter(path: Path) -> dict | None:
    """Same shape as `crons.py::_parse_frontmatter` and
    `backfill-mint-ids.py::read_node` — the line-anchored splitter, then
    `yaml.safe_load` on the frontmatter. `None` on anything unparseable: a bad
    node here is a node this checker cannot read `payload_ref` from, reported
    by the caller, never guessed at."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    if not text.strip().startswith("---"):
        return None
    parted = split_frontmatter(text)
    if parted is None:
        return None
    try:
        fm = yaml.safe_load(parted[0])
    except yaml.YAMLError:
        return None
    return fm if isinstance(fm, dict) else None


def _sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _node_files(nodes_dir: Path) -> list[Path]:
    """Every node under `nodes_dir`, retired siblings included.

    `rglob`, never a fixed-depth `glob("*/*.md")` — `nodes/.geometry/` is a
    real, reachable node directory (confirmed against `level3.py`), and a
    two-level glob pattern would silently stop matching the day a node moves
    one directory deeper, which is exactly how this project has lost node
    corpora before.
    """
    return sorted(nodes_dir.rglob("*.md")) if nodes_dir.is_dir() else []


def _node_hash_map(nodes_dir: Path) -> dict[str, str]:
    return {
        str(p.relative_to(nodes_dir)): _sha256_file(p)
        for p in _node_files(nodes_dir) if p.is_file()
    }


# --- the eight checks -------------------------------------------------


def check_node_count(before: Path, after: Path) -> CheckResult:
    """1. No node lost — raw counts, before `nodes/` vs. after `.agi/nodes/`."""
    before_nodes = _node_files(before / "nodes")
    after_nodes = _node_files(after / GRAPH_DIR_NAME / "nodes")
    passed = len(before_nodes) == len(after_nodes)
    return CheckResult(
        "no_node_lost", passed,
        f"{len(before_nodes)} node(s) before, {len(after_nodes)} after",
        {"before_count": len(before_nodes), "after_count": len(after_nodes)},
    )


def check_node_bytes(before: Path, after: Path) -> CheckResult:
    """2. No node's bytes changed — the migration is expected to rewrite ZERO
    node files, so any hash difference at the same relative path is reported,
    and so is a path present on only one side."""
    before_map = _node_hash_map(before / "nodes")
    after_map = _node_hash_map(after / GRAPH_DIR_NAME / "nodes")

    missing = sorted(set(before_map) - set(after_map))
    extra = sorted(set(after_map) - set(before_map))
    diverged = sorted(
        k for k in (set(before_map) & set(after_map)) if before_map[k] != after_map[k]
    )

    passed = not (missing or extra or diverged)
    offending = (diverged + missing + extra)[:10]
    return CheckResult(
        "no_node_bytes_changed", passed,
        f"{len(before_map)} node(s) hashed: {len(missing)} missing, "
        f"{len(extra)} extra, {len(diverged)} with changed bytes",
        {
            "missing_count": len(missing), "extra_count": len(extra),
            "diverged_count": len(diverged),
            "offending_paths": offending,
        },
    )


def check_grid_refs(before: Path, after: Path) -> CheckResult:
    """3. No grid ref lost — same names, same target sha, in the SAME
    namespace (goal:g6.3's per-node history is the only durable home of every
    payload byte). Missing / extra / diverged are kept as three separate
    lists because they are three separate failures with three separate
    remedies."""
    before_refs = _grid_refs(before)
    after_refs = _grid_refs(after)

    missing = sorted(set(before_refs) - set(after_refs))
    extra = sorted(set(after_refs) - set(before_refs))
    diverged = sorted(
        name for name in (set(before_refs) & set(after_refs))
        if before_refs[name] != after_refs[name]
    )

    passed = not (missing or extra or diverged)
    return CheckResult(
        "no_grid_ref_lost", passed,
        f"{len(before_refs)} ref(s) before, {len(after_refs)} after: "
        f"{len(missing)} missing, {len(extra)} extra, {len(diverged)} diverged",
        {
            "before_count": len(before_refs), "after_count": len(after_refs),
            "missing": missing[:10], "extra": extra[:10], "diverged": diverged[:10],
        },
    )


def check_histories(before: Path, after: Path) -> CheckResult:
    """4. Both histories present — `<before>`'s tip must be an ancestor of
    `<after>`'s HEAD, so the unification commit sits on top of the graph's own
    history instead of starting a new one that merely resembles it.

    The engine-side tip is reported too when `locations.source_root(before)`
    names a distinct git checkout (today's `<before>/agi` clone or symlink) —
    informational, not gating, since a checker for a specific migration
    contract should not invent a second hard requirement the contract itself
    does not state.
    """
    before_tip = _rev_parse(before)
    after_head = _rev_parse(after)
    detail: dict[str, Any] = {"before_tip": before_tip, "after_head": after_head}

    if before_tip is None or after_head is None:
        return CheckResult(
            "both_histories_present", False,
            "could not resolve HEAD on --before and/or --after "
            "(not a git repo, or no commits yet)",
            detail,
        )

    res = subprocess.run(
        ["git", "-C", str(after), "merge-base", "--is-ancestor", before_tip, after_head],
        capture_output=True, text=True,
    )
    graph_is_ancestor = res.returncode == 0
    detail["graph_tip_is_ancestor_of_after_head"] = graph_is_ancestor

    engine_root = locations.source_root(before)
    detail["engine_root_considered"] = str(engine_root)
    engine_ancestry: bool | None = None
    if engine_root != Path(before).resolve() and (engine_root / ".git").exists():
        engine_tip = _rev_parse(engine_root)
        detail["engine_tip"] = engine_tip
        if engine_tip is not None:
            eres = subprocess.run(
                ["git", "-C", str(after), "merge-base", "--is-ancestor",
                 engine_tip, after_head],
                capture_output=True, text=True,
            )
            engine_ancestry = eres.returncode == 0
    detail["engine_tip_is_ancestor_of_after_head"] = engine_ancestry

    passed = graph_is_ancestor
    return CheckResult(
        "both_histories_present", passed,
        f"before tip {before_tip[:12]} is "
        f"{'an ancestor' if graph_is_ancestor else 'NOT an ancestor'} "
        f"of after HEAD {after_head[:12]}",
        detail,
    )


def check_resolver(after: Path) -> CheckResult:
    """5. The resolver agrees — `locations.py` must see `<after>` exactly the
    way the `.agi` layout promises: graph root, repo root and source root all
    land where G11 says they do."""
    after = Path(after).resolve()
    expected_root = after / GRAPH_DIR_NAME
    root = locations.find_project_root(after)

    if root is None:
        return CheckResult(
            "resolver_agrees", False,
            f"locations.find_project_root({after}) returned None, "
            f"expected {expected_root}",
            {"find_project_root": None, "expected_root": str(expected_root)},
        )

    repo_root = locations.repo_root(root)
    source_root = locations.source_root(root)
    goals_path = locations.goals_path(root)
    expected_goals = after / "GOALS.md"

    detail = {
        "find_project_root": str(root), "expected_root": str(expected_root),
        "repo_root": str(repo_root), "expected_repo_root": str(after),
        "source_root": str(source_root), "expected_source_root": str(after),
        "goals_path": str(goals_path), "expected_goals_path": str(expected_goals),
    }
    passed = (
        root == expected_root
        and repo_root == after
        and source_root == after
        and goals_path == expected_goals
    )
    return CheckResult(
        "resolver_agrees", passed,
        "resolver agrees with the .agi layout" if passed else
        "resolver disagrees with the .agi layout — see detail",
        detail,
    )


def check_goals_location(after: Path) -> CheckResult:
    """6. GOALS.md is at the repo root, and specifically NOT inside `.agi/` —
    both halves checked, since a copy left behind in `.agi/` after the render
    moved on is its own kind of drift."""
    at_root = (after / "GOALS.md").is_file()
    inside_graph_dir = (after / GRAPH_DIR_NAME / "GOALS.md").exists()
    passed = at_root and not inside_graph_dir
    return CheckResult(
        "goals_at_repo_root", passed,
        f"present at {after / 'GOALS.md'}: {at_root}; "
        f"present inside {GRAPH_DIR_NAME}/: {inside_graph_dir}",
        {"at_root": at_root, "inside_graph_dir": inside_graph_dir},
    )


def _count_payload_refs(nodes_dir: Path) -> int:
    """How many nodes under `nodes_dir` carry a non-empty `payload_ref`."""
    n = 0
    for p in _node_files(nodes_dir):
        fm = _read_frontmatter(p)
        if fm and isinstance(fm.get("payload_ref"), str) and fm["payload_ref"].strip():
            n += 1
    return n


def check_payload_refs(before: Path, after: Path) -> CheckResult:
    """7. Every payload_ref resolves, AND none went missing.

    Catches the zero-rewrite assumption (module docstring, point 2) being
    wrong. Walks every node under `.agi/nodes/`, reads `payload_ref` where
    present, and resolves it against `<after>` itself — under the `.agi`
    layout `source_root` is always the repo root (see `check_resolver`), so
    this check does not need `check_resolver` to have passed first.

    **The count is half the invariant, and it is the half that was missing.**
    Resolving-every-ref alone passes vacuously when there are no refs to
    resolve: a migration that dropped every build node would satisfy it
    perfectly, reporting "0 checked, 0 unresolved" in the same green as a
    correct run. That is precisely the shape of failure this tool exists to
    catch, so the number of payload_refs before and after must also match.
    Parent review, iteration 3 — the vacuous pass was observed live in the
    sanity run against a never-migrated clone, where this was the one check
    that did not fail.
    """
    nodes_dir = after / GRAPH_DIR_NAME / "nodes"
    source_root = Path(after).resolve()
    before_count = _count_payload_refs(Path(before).resolve() / "nodes")

    checked = 0
    unresolved: list[dict[str, str]] = []
    for p in _node_files(nodes_dir):
        fm = _read_frontmatter(p)
        if not fm:
            continue
        ref = fm.get("payload_ref")
        if not isinstance(ref, str) or not ref.strip():
            continue
        checked += 1
        target = source_root / ref
        if not target.is_file():
            unresolved.append({
                "node": str(p.relative_to(nodes_dir)),
                "payload_ref": ref,
            })

    passed = not unresolved and checked == before_count
    msg = (f"{checked} payload_ref(s) checked, {len(unresolved)} unresolved; "
           f"{before_count} before")
    if checked != before_count:
        msg += f" -- COUNT MISMATCH, {before_count - checked} lost"
    return CheckResult(
        "payload_refs_resolve", passed, msg,
        {"checked": checked, "before_count": before_count,
         "unresolved": unresolved[:10]},
    )


def check_config(after: Path) -> CheckResult:
    """8. Config is where the resolver expects it — `<after>/.agi/config.json`
    exists and parses as JSON."""
    config_path = after / GRAPH_DIR_NAME / "config.json"
    exists = config_path.is_file()
    parses = False
    error = None
    if exists:
        try:
            json.loads(config_path.read_text(encoding="utf-8"))
            parses = True
        except (OSError, ValueError) as exc:
            error = str(exc)

    passed = exists and parses
    detail = {"path": str(config_path), "exists": exists, "parses": parses}
    if error:
        detail["error"] = error
    return CheckResult(
        "config_at_expected_path", passed,
        f"{config_path}: exists={exists} parses={parses}",
        detail,
    )


# --- orchestration -----------------------------------------------------

#: `(name, fn)` pairs in report order. `name` here is only used for the
#: `_safe` wrapper's failure message when `fn` itself raises before it can
#: build its own `CheckResult` — the real check name is set within each `fn`.
_TWO_ARG_CHECKS: list[Callable[[Path, Path], CheckResult]] = [
    check_node_count, check_node_bytes, check_grid_refs, check_histories,
    check_payload_refs,
]
_ONE_ARG_CHECKS: list[Callable[[Path], CheckResult]] = [
    check_resolver, check_goals_location, check_config,
]


def _safe(name: str, fn: Callable[..., CheckResult], *args: Path) -> CheckResult:
    """Run one check; turn a raised exception into a FAIL rather than letting
    it take the whole run down. A verifier's entire value is being trustable
    against a repo that something else may have just broken — it must never
    itself be the thing that crashes with a traceback and no verdict."""
    try:
        return fn(*args)
    except Exception as exc:  # noqa: BLE001 — deliberately broad, see docstring
        return CheckResult(name, False,
                            f"check raised {exc.__class__.__name__}: {exc}",
                            {"exception": str(exc)})


def run_all(before: Path, after: Path) -> list[CheckResult]:
    before = Path(before).resolve()
    after = Path(after).resolve()
    results = [_safe(fn.__name__, fn, before, after) for fn in _TWO_ARG_CHECKS]
    results += [_safe(fn.__name__, fn, after) for fn in _ONE_ARG_CHECKS]
    return results


# --- cli -----------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Independent post-migration checker for goal:g11 — did "
                     "the unify.py migration lose a node, a grid ref, a "
                     "history, or a payload_ref? Read-only; never writes."
    )
    ap.add_argument("--before", required=True,
                     help="pre-migration graph repo (nodes/, GOALS.md, refs/grid/*)")
    ap.add_argument("--after", required=True,
                     help="post-migration unified repo (.agi/, GOALS.md at root)")
    ap.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = ap.parse_args(argv)

    before = Path(args.before)
    after = Path(args.after)

    if not before.is_dir():
        print(f"ERR: verify_unified.py: --before {before} is not a directory",
              file=sys.stderr)
        return 2
    if not after.is_dir():
        print(f"ERR: verify_unified.py: --after {after} is not a directory",
              file=sys.stderr)
        return 2

    results = run_all(before, after)
    ok = all(r.passed for r in results)

    if args.json:
        print(json.dumps({
            "ok": ok,
            "before": str(before.resolve()),
            "after": str(after.resolve()),
            "checks": [r.to_dict() for r in results],
        }, indent=2))
    else:
        for r in results:
            status = "PASS" if r.passed else "FAIL"
            print(f"[{status}] {r.name}: {r.message}")
            if not r.passed:
                for k, v in r.detail.items():
                    print(f"    {k}: {v}")
        print()
        print("OK — nothing lost" if ok else "FAILED — see checks above")

    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
