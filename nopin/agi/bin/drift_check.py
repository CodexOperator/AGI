#!/usr/bin/env python3
"""Drift check: compare pinned engine_commit against actual HEAD.

Part of the L9 pinning gap fix (goal:g8.1). Reads engine_commit (or engine_ref)
from the project config, resolves the engine checkout directory, and compares
the declared commit to `git rev-parse HEAD`.

Returns exit code only under --strict (for CI). Under normal loop use, always
exits 0 and emits warnings to stderr — never blocking, never failing.

Integration point: driver.sh calls this before every iteration (after env-file
sourcing, before dispatch), matching the hypothesis:a00-4d063889-c4e95d proof
criterion ("some entry point reads it, compares to cloned engine's actual HEAD,
and emits a non-fatal warning on mismatch").
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE))
import locations  # noqa: E402


def resolve_engine_dir(root: Path) -> Path:
    """Where the engine checkout lives for this project.

    Same logic as `locations.source_root()` — the engine IS the source in the
    G11 layout and IS the `agi/` clone in the classic layout:
      1. G11 (.agi/ graph dir): engine is the repo root (parent of .agi/)
      2. Classic clone: <project_root>/agi/
      3. Fallback: the graph root itself
    """
    if locations.is_graph_dir(root):
        return root.parent  # repo root
    beside = root / "agi"
    if beside.exists():
        return beside.resolve()
    return root


def git_head(engine_dir: Path) -> str | None:
    """Return the full SHA of HEAD, or None if not a git repo."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=engine_dir,
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def check_drift(root: Path) -> tuple[bool, str | None, str | None]:
    """Check for engine drift.

    Returns (drifted, pinned_commit, actual_head).

    - pinned_commit is None if no engine_commit/engine_ref field exists.
    - drifted is True only when pinned_commit is set and HEAD differs.
    """
    cfg = locations.load_config(root)
    pinned = cfg.get("engine_commit") or cfg.get("engine_ref")
    if not pinned:
        return False, None, None  # not pinned -> no drift possible

    engine_dir = resolve_engine_dir(root)
    head = git_head(engine_dir)
    if head is None:
        return False, pinned, None  # not a git repo -> can't check

    return head != pinned, pinned, head


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="Check engine drift against pinned commit.")
    ap.add_argument("start", nargs="?", default=None,
                    help="directory to resolve from (default: cwd)")
    ap.add_argument("--engine-dir", default=None,
                    help="override engine checkout dir (for testing)")
    ap.add_argument("--strict", action="store_true",
                    help="exit non-zero if drift detected (default: always 0)")
    args = ap.parse_args(argv)

    root = locations.find_project_root(args.start)
    if root is None:
        print("[drift] no agi project found — nothing to check", flush=True)
        return 0

    cfg = locations.load_config(root)
    pinned = cfg.get("engine_commit") or cfg.get("engine_ref")
    if not pinned:
        print("[drift] NOT PINNED: no engine_commit or engine_ref in config — "
              "nothing to check", flush=True)
        return 0

    engine_dir = Path(args.engine_dir).resolve() if args.engine_dir else resolve_engine_dir(root)
    head = git_head(engine_dir)

    if head is None:
        print(f"[drift] WARNING: {engine_dir} is not a git repo — "
              f"cannot check engine_commit={pinned}", flush=True)
        return 0 if not args.strict else 2

    if head == pinned:
        print(f"[drift] OK: engine at {engine_dir} HEAD {head[:12]} matches "
              f"pinned {pinned[:12]}", flush=True)
        return 0

    print(f"[drift] WARNING: engine at {engine_dir} HEAD is {head[:12]} "
          f"but config pins {pinned[:12]}",
          file=sys.stderr, flush=True)
    print(f"[drift]   To update: git -C {engine_dir} pull  (or update "
          f"config's engine_commit to {head})",
          file=sys.stderr, flush=True)
    return 1 if args.strict else 0


if __name__ == "__main__":
    raise SystemExit(main())