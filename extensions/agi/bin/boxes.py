#!/usr/bin/env python3
"""boxes.py — which BOX a checkout is, and whether a posts row belongs to it.

A "box" is a machine (or clone) that runs its own crontab and its own seats.
A `config:posts` row may carry a `box` cell naming whose box its `pid`/`window`
cells are true of; a row without the cell belongs to the graph's default box.
`AGI_BOX` in the resolved env names THIS box (box-local by construction); unset
falls back to the `default_box` cell on the posts node.

This is a DIFFERENT `box` from `rotate.py`'s `_box_fact()` (a machine load
snapshot `{loadavg, cores}` stored under `rec["box"]` in rotation records).
Same word, unrelated meanings, different places — do not merge them.
"""
from __future__ import annotations

import os
from pathlib import Path


def default_box(root: Path) -> str:
    """The `default_box` cell on the config:posts node; '' when undeclared."""
    import frontmatter
    import yaml
    path = Path(root) / "nodes" / ".geometry" / "posts.md"
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    parted = frontmatter.split_frontmatter(text)
    if not parted:
        return ""
    fm = yaml.safe_load(parted[0]) or {}
    return str(fm.get("default_box") or "").strip()


def this_box(root: Path) -> str:
    """AGI_BOX from the resolved env, else the posts node's default box."""
    import envfile
    val = os.environ.get("AGI_BOX", "").strip()
    if not val:
        val = envfile.read_env(envfile.resolve(root).env_file).get("AGI_BOX", "").strip()
    val = val or default_box(root)
    if not val:
        raise RuntimeError(
            f"no AGI_BOX in the env and no `default_box` cell on the posts "
            f"node under {root} — this graph cannot say which box it is"
        )
    return val


def row_is_local(root: Path, row: dict) -> bool:
    """True when `row`'s box (its own cell, else the default) is THIS box.

    A graph with NO box declaration at all (no AGI_BOX and no `default_box`)
    is a single-box graph: every row is local, which is exactly today's
    behaviour. The guard is FAIL-OPEN there rather than crashing a watcher.
    """
    own = str((row or {}).get("box") or "").strip()
    try:
        here = this_box(root)
    except Exception:  # noqa: BLE001 -- undeclared box: single-box graph
        return True
    if not own:
        own = default_box(root)
    return own == here

if __name__ == "__main__":
    import argparse
    argparse.ArgumentParser(description=__doc__.splitlines()[0]).parse_args()
