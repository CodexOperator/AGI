#!/usr/bin/env python3
"""grid_coverage_check.py — every tracked engine code file is inside the grid.

Closes the loop on `hypothesis:l3-engine-files-outside-the-grid`: the grid
versions a file only through a build node whose `payload_ref` resolves to it.
A tracked engine file with no such node has its bytes outside the grid
entirely — `grid.py commit --all` versions nothing for it and
`grid.py payload` cannot read it back. This checker is the part that KEEPS
the count closed: mint the missing nodes once, wire this where the other
invariants run, and the day the gap silently re-grows the checker turns red
instead of a human discovering it three months later.

The arithmetic is simple set subtraction, and all three sets are *data*,
never hardcoded inside an if-statement:

    tracked_engine_files
      - every declared payload_ref (any type, live AND deprecated)
      - a DECLARED exclusion list (DATA, .agi/context/grid-coverage-exclusions.md)
    = remainder  ->  exit NONZERO if non-empty

**Never widen the exclusion list to make the count pass.** The exclusion
list exists so a reader can say *which* files legitimately have no node and
*why*, not so the checker can be tuned green. If a remainder exists, report
it.

Commands
--------
  (no args)          Check the engine repo enclosing (or given by) --engine.
  --engine DIR       Repo to enumerate (default: project root resolved by
                     locations, i.e. the repo enclosing the nearest .agi/).
  --exclusions FILE  Exclusion-list data file (default:
                     <engine>/.agi/context/grid-coverage-exclusions.md).
  --verbose          Print the full remainder list, not just the count.

Exit codes
----------
  0   every tracked engine code file is covered or declared excluded
  1   at least one tracked code file has no payload_ref and no exclusion
  2   usage / enumeration error (repo missing, not a git repo, no nodes dir)
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

#: Engine code directories the grid owns. Root-relative, compared by prefix.
ENGINE_DIRS = ("extensions/", "skills/", "src/", "bin/")

#: Code file extensions the project grid-versions (the parent measured
#: `.py/.sh/.js`; a file that is not code is data and gets no node).
CODE_EXTS = (".py", ".sh", ".js")

#: Default location of the declared exclusion list, relative to --engine.
DEFAULT_EXCLUSIONS = Path(".agi") / "context" / "grid-coverage-exclusions.md"


def find_project_root(start: Path) -> Path | None:
    """Nearest enclosing .agi/ holding a config (goal:g11), else config root."""
    d = start.resolve()
    while True:
        if (d / ".agi" / "config.json").is_file():
            return d
        if (d / "agi-tree.config.json").is_file():
            return d
        if d.parent == d:
            return None
        d = d.parent


def git_ls_files(repo: Path) -> list[str]:
    """Tracked paths in `repo`, sorted."""
    out = subprocess.run(
        ["git", "-C", str(repo), "ls-files"],
        capture_output=True, text=True, check=True,
    )
    return [ln for ln in out.stdout.splitlines() if ln]


def collect_payload_refs(nodes_dir: Path) -> set[str]:
    """Every `payload_ref:` declared anywhere under nodes/ (live + deprecated).

    Reads the raw text (frontmatter and the BUILD-CONTRACT block both carry
    the field) so a reader here never depends on which of the two regions
    a given node stores its value in.
    """
    refs: set[str] = set()
    if not nodes_dir.is_dir():
        return refs
    for path in nodes_dir.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        for line in text.splitlines():
            line = line.strip()
            if not line.startswith("payload_ref:"):
                continue
            value = line.split(":", 1)[1].strip().strip("\"'")
            if value:
                refs.add(value)
    return refs


def read_exclusions(path: Path) -> dict[str, str]:
    """Parse the declared exclusion-list data file: path -> reason.

    DATA, not code: one excluded path per line, a reason after a `|` on the
    same line. Blank lines and `#` comments are ignored. A missing file is
    an empty list (not an error) — exclusions are declarative and optional.
    """
    exclusions: dict[str, str] = {}
    if not path.is_file():
        return exclusions
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if "|" in line:
            path_part, reason = line.split("|", 1)
        else:
            path_part, reason = line, ""
        path_part = path_part.strip()
        if path_part:
            exclusions[path_part] = reason.strip()
    return exclusions


def remaining(engine: Path, exclusions_file: Path) -> tuple[list[str], list[str], dict[str, str]]:
    """`(remainder, excluded_reported, exclusions)` for an engine repo.

    `remainder` is tracked code files with no payload_ref and no exclusion.
    `excluded_reported` is files that WERE matched by an exclusion — returned
    so a caller can prove an exclusion is reported with its reason rather
    than silently skipped.
    """
    root = find_project_root(engine) or engine
    nodes_dir = root / ".agi" / "nodes"
    if not nodes_dir.is_dir():
        raise SystemExit(2)

    tracked = git_ls_files(engine)
    code_files = [
        f for f in tracked
        if f.startswith(ENGINE_DIRS) and f.endswith(CODE_EXTS)
    ]
    payload_refs = collect_payload_refs(nodes_dir)
    exclusions = read_exclusions(exclusions_file)

    remainder: list[str] = []
    excluded_reported: list[str] = []
    for f in sorted(code_files):
        if f in payload_refs:
            continue
        if f in exclusions:
            excluded_reported.append(f)
            continue
        remainder.append(f)
    return remainder, excluded_reported, exclusions


def main(argv: list[str] | None = None) -> int:
    import argparse
    if argv is None:
        argv = sys.argv[1:]
    p = argparse.ArgumentParser(
        prog="grid_coverage_check.py",
        description="Every tracked engine code file is covered by a payload_ref "
                    "or a declared exclusion; exit nonzero on any remainder.")
    p.add_argument("--engine", default=None,
                   help="repo to enumerate (default: project root from locations)")
    p.add_argument("--exclusions", default=None,
                   help="exclusion-list data file (default: "
                        "<engine>/.agi/context/grid-coverage-exclusions.md)")
    p.add_argument("--verbose", action="store_true",
                   help="print the full remainder list, not just the count")
    args = p.parse_args(argv)

    engine = Path(args.engine).resolve() if args.engine else \
        (find_project_root(Path.cwd()) or Path.cwd())
    exclusions_file = Path(args.exclusions).resolve() if args.exclusions \
        else engine / DEFAULT_EXCLUSIONS

    remainder, excluded_reported, exclusions = remaining(engine, exclusions_file)

    if args.verbose or remainder:
        print(f"engine: {engine}")
        print(f"exclusions file: {exclusions_file} ({len(exclusions)} declared)")
    if args.verbose:
        for f in excluded_reported:
            reason = exclusions.get(f, "")
            print(f"  EXCLUDED: {f}   ({reason})" if reason else f"  EXCLUDED: {f}")
    if remainder:
        if args.verbose:
            for f in remainder:
                print(f"  MISSING: {f}")
        print(f"grid coverage: {len(remainder)} tracked code file(s) OUTSIDE the grid")
        return 1
    print("grid coverage: clean — every tracked engine code file is covered "
          "or declared excluded")
    return 0


if __name__ == "__main__":
    sys.exit(main())