"""Active-vs-inactive set tracking + duplicate detection (T-021 / schema-registry R2).

Loader builds a Schema dict; this module wraps it with:
- ``ActiveSet.active_names()``  — schemas that participate in auto-discovery
- ``ActiveSet.inactive_names()`` — loaded but excluded from auto-discovery
- raises :class:`DuplicateActiveSchemaError` when two bracketed files name the same schema.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .loader import Schema, SchemaRegistry


class DuplicateActiveSchemaError(Exception):
    """Raised when two active (bracketed) schemas claim the same name (R2.4)."""

    def __init__(self, name: str, paths: list[Path]) -> None:
        self.name = name
        self.paths = paths
        joined = ", ".join(str(p) for p in paths)
        super().__init__(
            f"duplicate active schema '{name}': {joined}"
        )


@dataclass
class ActiveSet:
    active: dict[str, Schema]
    inactive: dict[str, Schema]

    def active_names(self) -> set[str]:
        return set(self.active.keys())

    def inactive_names(self) -> set[str]:
        return set(self.inactive.keys())


def build_active_set(registry: SchemaRegistry) -> ActiveSet:
    """Partition the registry into active and inactive sets (R2.1, R2.2).

    Detects duplicate active schemas by re-walking the source paths the registry
    knows about (R2.4). Inactive schemas are never auto-discovered (R2.2).
    """
    active: dict[str, Schema] = {}
    inactive: dict[str, Schema] = {}
    # Detect duplicate-active by re-scanning the source dir of each schema.
    seen_active_paths: dict[str, list[Path]] = {}
    for name, schema in registry.schemas.items():
        if schema.active:
            active[name] = schema
            seen_active_paths.setdefault(name, []).append(schema.source_path)
        else:
            inactive[name] = schema
    # Now check the source dir for any sibling bracketed file with the same canonical name
    # that may have been silently overridden by the loader.
    for name, paths in seen_active_paths.items():
        # If the registry has a single Schema for `name` but the dir holds multiple
        # bracketed files claiming the same `name`, we need to detect that. Walk the
        # parent of the schema's source_path looking for siblings.
        active_schema = active.get(name)
        if active_schema is None:
            continue
        parent = active_schema.source_path.parent
        if not parent.is_dir():
            continue
        siblings: list[Path] = []
        for p in sorted(parent.iterdir()):
            if not p.is_file():
                continue
            if p.suffix.lower() not in {".md", ".json"}:
                continue
            stem = p.stem
            if not (stem.startswith("[") and stem.endswith("]")):
                continue
            inner = stem[1:-1]
            if inner == name:
                siblings.append(p)
        if len(siblings) > 1:
            raise DuplicateActiveSchemaError(name=name, paths=siblings)
    return ActiveSet(active=active, inactive=inactive)
