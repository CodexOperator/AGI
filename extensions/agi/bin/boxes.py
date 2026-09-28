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

import json
import os
import re
from pathlib import Path

class BoxSchemaError(ValueError):
    """A graph whose `[box].md` cannot declare what this reader needs."""


# The engine's OWN [box].md: fallback for a graph with none of its own.
_ENGINE_BOX_SCHEMA = (Path(__file__).resolve().parents[3] / ".agi" /
                      "context" / "schemas" / "[box].md")
# A bare `{token}` absent from the map is a stray; a shell `$`-reference
# (`${PATH}`, `${VAR:-x}`) is legal syntax and must never be convicted.
_STRAY_TOKEN = re.compile(r"(?<!\$)\{[A-Za-z_][A-Za-z0-9_]*\}")


def graph_root(root: Path) -> Path:
    """`root` itself when it IS a graph, else the nearest enclosing graph.

    Every other reader in the tree resolves its root with locations.py; this
    one did not, so a REPO root read an EMPTY cell set silently -- the exact
    render `resolve_placeholders` refuses to produce. `root` is returned
    unchanged when it already holds a config, and when nothing is found, so
    an existing caller sees no change.
    """
    start = Path(root).resolve()
    if (start / "config.json").is_file():
        return start
    import locations
    found = locations.find_project_root(start)
    return Path(found).resolve() if found else start


def box_schema_path(root: Path) -> Path:
    """The one declaration: context/schemas/[box].md under the graph root."""
    return graph_root(root) / "context" / "schemas" / "[box].md"


def _schema_at(p: Path) -> dict:
    """Parsed frontmatter of the `[box].md` at `p`; {} when `p` is absent."""
    import frontmatter, yaml
    parts = frontmatter.split_frontmatter(p.read_text(encoding="utf-8")) if p.is_file() else None
    return (yaml.safe_load(parts[0]) or {}) if parts else {}


def _box_schema(root: Path) -> dict:
    """Parsed frontmatter of context/schemas/[box].md -- the one declaration."""
    return _schema_at(box_schema_path(root))


def require_box_cells(root: Path) -> tuple[str, ...]:
    """The declared cell names, or refuse naming `[box].md`.

    An absent `[box].md` (or one declaring no `fields`) used to read as an
    empty cell set, hiding the audit's silence. Fail closed instead.
    """
    names = box_cell_names(root)
    if not names:
        raise BoxSchemaError(
            f"{box_schema_path(root)} declares no box cells "
            f"(absent, or no `fields:` map)")
    return names


def _box(root: Path) -> dict:
    try:
        data = json.loads((graph_root(root) / "config.json").read_text(encoding="utf-8"))
        return data.get("box") or {}
    except Exception:  # noqa: BLE001 -- absent/unreadable config: no cells
        return {}


def box_cell_names(root: Path) -> tuple[str, ...]:
    """The cell names from the `fields` mapping in [box].md -- the one declaration."""
    return tuple((_box_schema(root).get("fields") or {}).keys())


def box_cells(root: Path) -> dict:
    """The `box` cells true of this box: root, logs_dir, tmux_session, user."""
    box = _box(root)
    return {k: str(box.get(k) or "") for k in box_cell_names(root)}


def allow_paths(root: Path) -> list[str]:
    """The declaring config plus every `box.allow` entry, from the cells."""
    return ["config.json"] + [str(x) for x in (_box(root).get("allow") or [])]


def resolve_placeholders(text: str, cells: dict, root: Path) -> str:
    """Substitute `{token}` from `cells` using the mapping declared in [box].md.

    The declaration is the graph's own `[box].md`; a graph with NO schema
    falls back to the engine's own. A PRESENT schema without a `placeholders:`
    map, a missing or EMPTY cell, or an undeclared `{token}` each refuse by name.
    """
    p = box_schema_path(root)
    if not p.is_file() and _ENGINE_BOX_SCHEMA.is_file():
        p = _ENGINE_BOX_SCHEMA
    mapping = _schema_at(p).get("placeholders")
    if not mapping:
        raise BoxSchemaError(f"{p} declares no `placeholders:` map")
    for name, key in mapping.items():
        token = "{" + name + "}"
        if token not in text:
            continue
        if key not in (cells or {}):
            raise BoxSchemaError(
                f"{p}: placeholder {token} maps to cell `{key}`, which this "
                f"caller did not supply")
        value = str(cells[key])
        if not value.strip():
            raise BoxSchemaError(
                f"{p}: placeholder {token} maps to cell `{key}`, which this "
                f"caller supplied EMPTY -- an empty render is the bug this "
                f"resolver exists to prevent")
        text = text.replace(token, value)
    stray = _STRAY_TOKEN.search(text)
    if stray:
        raise BoxSchemaError(
            f"{p}: `{stray.group(0)}` is not declared in `placeholders:`")
    return text


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
    """AGI_BOX from the resolved env, else the box's own env file.

    NO `default_box` fallback: that cell is the posts node's DOCUMENTATION of
    its home box, never a locality fallback. An unset AGI_BOX REFUSES -- a
    silent default read every boxless row as `core-town` and so as foreign
    (hypothesis:every-live-row-carries-its-own-box-and-an-unset-box-is-
    refused, belam 00:35Z 09-27).
    """
    import envfile
    val = os.environ.get("AGI_BOX", "").strip()
    if not val:
        val = envfile.read_env(envfile.resolve(root).env_file).get("AGI_BOX", "").strip()
    if not val:
        raise RuntimeError(
            f"no AGI_BOX in the env and none in the box env file under "
            f"{root} — this graph cannot say which box it is (`default_box` "
            f"is documentation, never a fallback)"
        )
    return val


def row_is_local(root: Path, row: dict) -> bool:
    """True when `row` NAMES this box on its own `box` cell.

    An EMPTY or UNKNOWN row box is NOT local on any DECLARED box and
    `'(default)'` is never a match. The ONE retained fail-open: a graph that
    declares no box AT ALL stays a single-box graph (a dev graph must not go
    dark), but a row that DOES name a box there is foreign -- unprovable.
    """
    own = str((row or {}).get("box") or "").strip()
    try:
        here = this_box(root)
    except Exception:  # noqa: BLE001 -- an undeclared box proves nothing
        return not own
    return bool(own) and own == here

if __name__ == "__main__":
    import argparse
    argparse.ArgumentParser(description=__doc__.splitlines()[0]).parse_args()
