#!/usr/bin/env python3
"""dm_address.py — post-branch DM address resolution (goal:g7.32.6.1).

Owner design (goal:g7.32.6 design line 2): ADDRESS = the addressee post
row's designated remote head (its inbox destination); when absent, the
nearest, lowest-level remote-visible branch. Same route for same-box and
cross-box DMs. The hub-only reading is retired.

Public API
----------
remote_head_cell(row) -> str
    The post row's own `remote_head` cell (stripped), or "".

nearest_remote_branch(row, *, season=2) -> str
    Lowest-level remote-visible branch derivable from the row's town /
    town_season / season cells. Preference (most specific first):
      1. <town>/season<m>/main
      2. <town>/main
      3. season<n>/main
    Post/loop branches are NOT remote-visible (branches.is_remote_visible).

resolve_address(row, *, season=2) -> str
    remote_head_cell wins; else nearest_remote_branch; else raise
    ValueError naming the row — never guess, never hub.
"""
from __future__ import annotations

from typing import Any


def remote_head_cell(row: dict | None) -> str:
    """Named remote_head on the post row; empty when undeclared."""
    if not isinstance(row, dict):
        return ""
    return str(row.get("remote_head") or "").strip()


def _int_cell(row: dict, *keys: str, default: int | None = None) -> int | None:
    for k in keys:
        raw = row.get(k)
        if raw is None or raw == "":
            continue
        try:
            n = int(raw)
        except (TypeError, ValueError):
            continue
        if n >= 1:
            return n
    return default


def nearest_remote_branch(row: dict | None, *, season: int = 2) -> str:
    """Nearest lowest-level remote-visible branch for this post row.

    Raises ValueError when nothing remote-visible can be derived.
    """
    if not isinstance(row, dict):
        raise ValueError("dm_address.nearest_remote_branch: row is required")
    town = str(row.get("town") or "").strip()
    # town=='all' is a roster wildcard, not a branch town
    if town.lower() in {"", "all", "main", "posts", "loops"}:
        town = ""
    town_season = _int_cell(row, "town_season", "town_season_n")
    season_n = _int_cell(row, "season", "season_n", default=season) or season

    candidates: list[str] = []
    if town and town_season is not None:
        candidates.append(f"{town}/season{town_season}/main")
    if town:
        candidates.append(f"{town}/main")
    if season_n is not None:
        candidates.append(f"season{season_n}/main")

    # Prefer in-tree branches.is_remote_visible when importable; else the
    # same trunk-pair rule spelled here so tests stay self-contained.
    try:
        import branches  # type: ignore

        def _visible(name: str) -> bool:
            return bool(branches.is_remote_visible(name))
    except Exception:  # noqa: BLE001 — contract still holds without grammar

        def _visible(name: str) -> bool:
            if name == "master":
                return True
            parts = name.split("/")
            if len(parts) == 2 and parts[0].startswith("season") and parts[1] == "main":
                return True
            if len(parts) == 2 and parts[1] == "main":
                return parts[0] not in {"main", "posts", "loops"}
            if len(parts) == 3 and parts[1].startswith("season") and parts[2] == "main":
                return parts[0] not in {"main", "posts", "loops"}
            return False

    for name in candidates:
        if _visible(name):
            return name
    raise ValueError(
        f"dm_address: no remote-visible branch for row name="
        f"{row.get('name')!r} town={row.get('town')!r} — refuse by name"
    )


def resolve_address(row: dict | None, *, season: int = 2) -> str:
    """Addressee remote head, else nearest remote-visible; never hub guess."""
    own = remote_head_cell(row)
    if own:
        return own
    return nearest_remote_branch(row, season=season)


if __name__ == "__main__":
    import argparse

    argparse.ArgumentParser(description=__doc__.splitlines()[0]).parse_args()
