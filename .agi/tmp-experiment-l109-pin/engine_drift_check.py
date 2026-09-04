#!/usr/bin/env python3
"""Experiment: prototype engine_commit pinning + drift check for L9 gap.

Simulates what driver.sh / locations.py would do to detect engine drift.
A project config declares the expected engine commit; this script reads it,
compares to the cloned engine's actual HEAD, and warns on mismatch.

Usage:
  python3 engine_drift_check.py <project-config.json>
  python3 engine_drift_check.py <project-config.json> --engine-dir <path>
"""

import json
import subprocess
import sys
from pathlib import Path


def git_head(engine_dir: Path) -> str | None:
    """Return the SHA of HEAD in engine_dir, or None on error."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=str(engine_dir),
            capture_output=True,
            text=True,
            timeout=10,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass
    return None


def check_drift(config_path: Path, engine_dir: Path | None = None) -> dict:
    """Check if the engine is pinned and whether it has drifted."""
    result = {
        "config_path": str(config_path),
        "engine_dir": str(engine_dir or Path.cwd()),
        "engine_commit_in_config": None,
        "actual_head": None,
        "match": None,
        "pinned": False,
        "drifted": None,
        "message": "",
    }

    # 1. Read config
    try:
        with open(config_path) as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        result["message"] = f"ERR: cannot read config — {e}"
        return result

    engine_commit = config.get("engine_commit") or config.get("engine_ref")
    result["engine_commit_in_config"] = engine_commit

    if engine_commit is None:
        result["pinned"] = False
        result["message"] = "NOT PINNED: config has no engine_commit or engine_ref field. No drift check possible."
        result["match"] = None
        return result

    result["pinned"] = True

    # 2. Resolve engine_dir (the engine lives as a checkout somewhere)
    ed = engine_dir or _default_engine_dir(config_path)

    # 3. Get actual HEAD
    actual = git_head(ed)
    result["actual_head"] = actual

    if actual is None:
        result["message"] = f"WARN: engine dir {ed} is not a git repo or cannot be read"
        result["drifted"] = None
        return result

    # 4. Compare
    if actual == engine_commit:
        result["match"] = True
        result["drifted"] = False
        result["message"] = f"OK: engine at {actual[:12]} matches pinned commit {engine_commit[:12]}"
    else:
        result["match"] = False
        result["drifted"] = True
        result["message"] = (
            f"DRIFT WARNING: engine HEAD is {actual[:12]} but config pins {engine_commit[:12]}\n"
            f"  Run: git -C {ed} pull  (or update config's engine_commit)"
        )

    return result


def _default_engine_dir(config_path: Path) -> Path:
    """Guess engine dir relative to config. For a project at <proj>/config.json
    with engine cloned as <proj>/agi/, this returns <config_dir>/agi/."""
    cand = config_path.parent / "agi"
    if cand.is_dir() and (cand / ".git").is_dir():
        return cand.resolve()
    return config_path.parent.resolve()


def main():
    if len(sys.argv) < 2:
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(1)

    config_path = Path(sys.argv[1]).resolve()
    engine_dir = None
    if "--engine-dir" in sys.argv:
        idx = sys.argv.index("--engine-dir")
        engine_dir = Path(sys.argv[idx + 1]).resolve()

    result = check_drift(config_path, engine_dir)

    print("=" * 60)
    print("ENGINE DRIFT CHECK — L9 Pinning Gap Prototype")
    print("=" * 60)
    print(f"  Config:            {result['config_path']}")
    print(f"  Engine dir:        {result['engine_dir']}")
    print(f"  Pinned:            {result['pinned']}")
    if result["engine_commit_in_config"]:
        print(f"  Pinned commit:     {result['engine_commit_in_config'][:12]}")
    print(f"  Actual HEAD:       {result['actual_head'][:12] if result['actual_head'] else 'N/A'}")
    print(f"  Match:             {result['match']}")
    print(f"  Drifted:           {result['drifted']}")
    print("-" * 60)
    print(result["message"])
    print("=" * 60)

    if result["pinned"] and result["drifted"]:
        ret = 2
    elif result["pinned"] and not result["drifted"]:
        ret = 0
    else:
        ret = 1
    return ret


if __name__ == "__main__":
    sys.exit(main())