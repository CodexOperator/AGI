#!/usr/bin/env python3
"""parent_slots.py — committed parent-slot defs vs live occupancy (g7.31.3.3.1/.2).

Owner design (goal:g7.31.3.3): concurrency×parallel become pre-set parent post
slots under each post in `.geometry`; live occupancy is a LOCAL runtime file,
never the committed defs.

Public API
----------
committed_path(root) -> Path
    `.agi/nodes/.geometry/parent-slots.md` (committed SoT for slot defs).

load_committed(root) -> dict[str, list[dict]]
    post name -> list of slot def dicts. Never raises; missing -> {}.

slot_count_contract(cfg) -> int
    concurrency × parallel from spawn config (defaults 1×1).

occupancy_path(root) -> Path
    Local runtime file under `.agi/sessions/parent-occupancy.json` (gitignored).

occupy / clear / read_occupancy
    Mutate ONLY the runtime file. Refuse any write that would touch committed
    defs (negative falsifier for g7.31.3.3.1 / positive for .3.3.2).

OCCUPANCY_FORBIDDEN_KEYS
    Field names that must NEVER appear as SoT inside committed slot defs.
"""
from __future__ import annotations

import json
import os
import re
from pathlib import Path
from typing import Any

OCCUPANCY_FORBIDDEN_KEYS = frozenset({
    "occupied",
    "occupant",
    "occupied_by",
    "pid",
    "live",
    "runtime",
    "session_id",
    "window",
})


def committed_path(root: Path | None) -> Path:
    """Committed parent-slot definitions (g7.31.3.3.1)."""
    if root is None:
        raise ValueError("parent_slots.committed_path: root is required")
    return Path(root) / ".agi" / "nodes" / ".geometry" / "parent-slots.md"


def occupancy_path(root: Path | None) -> Path:
    """Local runtime occupancy file (g7.31.3.3.2) — not committed."""
    if root is None:
        raise ValueError("parent_slots.occupancy_path: root is required")
    return Path(root) / ".agi" / "sessions" / "parent-occupancy.json"


def slot_count_contract(cfg: dict | None) -> int:
    """concurrency × parallel; each absent cell reads as 1."""
    spawn = (cfg or {}).get("spawn") if isinstance((cfg or {}).get("spawn"), dict) else {}
    if not isinstance(spawn, dict):
        spawn = {}

    def _one(key: str) -> int:
        raw = spawn.get(key, 1)
        try:
            n = int(raw)
        except (TypeError, ValueError):
            return 1
        return max(1, n)

    return _one("concurrency") * _one("parallel")


def _parse_slots_block(text: str) -> dict[str, list[dict]]:
    """Minimal extract of `parent_slots:` -> post -> list of slot maps."""
    out: dict[str, list[dict]] = {}
    if "parent_slots:" not in text:
        return out
    start = text.index("parent_slots:")
    body = text[start + len("parent_slots:"):]
    post: str | None = None
    for raw in body.splitlines():
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        if raw and not raw[0].isspace() and not raw.startswith("parent_slots"):
            break
        m_post = re.match(r"^  ([A-Za-z0-9_.@-]+):\s*$", raw)
        if m_post:
            post = m_post.group(1)
            out.setdefault(post, [])
            continue
        if post is None:
            continue
        m_json = re.match(r"^    - (\{\s*.*\})\s*$", raw)
        if m_json:
            try:
                row = json.loads(m_json.group(1))
            except json.JSONDecodeError:
                continue
            if isinstance(row, dict):
                out[post].append(row)
            continue
        m_id = re.match(r'^    - \{\s*id:\s*"?([^,}"\s]+)"?.*\}\s*$', raw)
        if m_id:
            out[post].append({"id": m_id.group(1)})
            continue
        m_map = re.match(r'^    - id:\s*"?([^"\s]+)"?\s*$', raw)
        if m_map:
            out[post].append({"id": m_map.group(1)})
    return out


def load_committed(root: Path | None) -> dict[str, list[dict]]:
    """post -> slot defs. Missing/unreadable -> {}."""
    try:
        path = committed_path(root)
        if not path.is_file():
            return {}
        return _parse_slots_block(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001 — readers never raise
        return {}


def assert_defs_hold_no_occupancy(defs: dict[str, list[dict]]) -> None:
    """Negative falsifier: committed defs must not store live occupancy as SoT."""
    for post, slots in defs.items():
        for i, slot in enumerate(slots):
            bad = sorted(OCCUPANCY_FORBIDDEN_KEYS & set(slot.keys()))
            if bad:
                raise AssertionError(
                    f"parent_slots: committed defs for {post}[{i}] hold "
                    f"occupancy SoT fields {bad} — those live in the runtime file"
                )


def read_occupancy(root: Path | None) -> dict[str, Any]:
    """Runtime occupancy map. Missing -> empty structure."""
    path = occupancy_path(root)
    if not path.is_file():
        return {"posts": {}}
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:  # noqa: BLE001
        return {"posts": {}}
    if not isinstance(data, dict):
        return {"posts": {}}
    posts = data.get("posts")
    if not isinstance(posts, dict):
        data["posts"] = {}
    return data


def _write_occupancy(root: Path | None, data: dict) -> Path:
    path = occupancy_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    os.replace(tmp, path)
    return path


def occupy(root: Path | None, post: str, slot_id: str, occupant: str) -> Path:
    """Record live occupancy in the runtime file only."""
    if not post or not slot_id or not occupant:
        raise ValueError("parent_slots.occupy: post, slot_id, occupant required")
    data = read_occupancy(root)
    posts = data.setdefault("posts", {})
    row = posts.setdefault(post, {})
    row[slot_id] = {"occupant": occupant}
    return _write_occupancy(root, data)


def clear(root: Path | None, post: str, slot_id: str) -> Path:
    """Clear one slot occupancy from the runtime file only."""
    data = read_occupancy(root)
    posts = data.setdefault("posts", {})
    row = posts.get(post) or {}
    if slot_id in row:
        del row[slot_id]
    if row:
        posts[post] = row
    elif post in posts:
        del posts[post]
    return _write_occupancy(root, data)


def default_slot_ids(n: int) -> list[str]:
    """Return parent-0 .. parent-(n-1)."""
    return [f"parent-{i}" for i in range(max(0, int(n)))]
