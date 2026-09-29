#!/usr/bin/env python3
"""rotation_record.py -- the ONE shared home of what rotate, heal, sensei,
write and verification each read (goal:g7.16.1.3 row H4): the rotation-record
serializer and path reader, and the live-node grep behind the park tag.
Every name here is public, so none of THESE crosses a module as a `_private`
name (heal still reads other rotate privates, e.g. _write_rotation_record: out
of this row's scope), and write.py reads parked carriers without importing
the verifier."""
from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path


class GrepError(RuntimeError):
    """The live-node grep could not look: a git error, or a hit whose
    frontmatter does not load. A guard that cannot look fails closed."""


def home_rel(obj):
    """`obj` with every string value home-relative (goal:g7.16.1.2.1): this
    box's HOME -> `~`, any other box's home dir -> `<home>/`, through
    anonymize's ONE definition. A committed rotation record never carries a
    home path -- the path fields AND the log text (after_join cmd/output, ps
    snapshots, re-homed records from another box)."""
    if isinstance(obj, dict):
        return {k: home_rel(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [home_rel(v) for v in obj]
    if isinstance(obj, str):
        from anonymize import home_relative
        return home_relative(obj)
    return obj


def dump_record(obj) -> str:
    """The ONE serializer for rotation records: home-relative, indent 2."""
    return json.dumps(home_rel(obj), indent=2) + "\n"


def resolve_record_path(value) -> str:
    """The ONE reader for a path a record (or registry) carries: `~` expanded,
    the absolute legacy form passed through unchanged; '' when absent."""
    return os.path.expanduser(str(value)) if value else ""


def grep_live(groot: Path, needle: str) -> list[tuple[str, Path, dict]]:
    """Live nodes whose bytes carry `needle`: ONE `git grep` (no rglob),
    deprecated/ skipped -> (id, file, frontmatter), id-sorted. Raises
    GrepError when git exits >= 2, exits 1 with stderr (an unreadable file),
    or a hit has no frontmatter block, cannot be read, or its frontmatter does
    not load (goal:g7.16.1.3 row H4 f)."""
    import yaml
    import node_writer
    try:  # CM6: bounded, and a launch failure (e.g. no nodes/) is a named FAIL
        r = subprocess.run(["git", "grep", "--no-index", "-lzF", "-e", needle, "--", "."],
                           cwd=groot / "nodes", capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError) as exc:
        raise GrepError(f"git grep could not run: {exc}") from None
    if r.returncode >= 2 or (r.returncode == 1 and r.stderr.strip()):
        raise GrepError(f"git grep exit {r.returncode}: {r.stderr.strip()}")
    hits = []
    for rel in filter(None, r.stdout.split("\0")):
        if not rel.startswith("deprecated/"):
            f = groot / "nodes" / rel
            try:
                split = node_writer.split_frontmatter(f.read_text("utf-8", "replace"))
                if split is None:
                    raise GrepError(f"{rel}: no frontmatter block")
                fm = yaml.safe_load(split[0])
            except (yaml.YAMLError, OSError) as exc:
                raise GrepError(f"{rel}: frontmatter does not load: {exc}") from None
            if not (isinstance(fm, dict) and fm.get("id")):  # CM5: never silently dropped
                raise GrepError(f"{rel}: frontmatter carries no id")
            hits.append((str(fm["id"]), f, fm))
    return sorted(hits, key=lambda h: h[0])


def parked_carriers(groot: Path, goal: str) -> list[tuple[str, Path, list]]:
    """goal:g7.16.1.2.6 -- live nodes whose `tags` hold `parked:<goal>` (the
    tag form in [goal].md / [hypothesis].md) -> (id, file, tags)."""
    tag = f"parked:{goal}"
    out = []
    for i, f, fm in grep_live(groot, tag):
        tags = fm.get("tags") or []
        if not isinstance(tags, list):  # CM8: a string would explode into characters
            raise GrepError(f"{i}: `tags` is {type(tags).__name__}, not a list")
        if tag in tags:
            out.append((i, f, list(tags)))
    return out
