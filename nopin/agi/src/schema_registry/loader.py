"""Schema file loader (T-019 / schema-registry R1).

Naming convention:
- ``context/schemas/name.md``   — schema file, inactive
- ``context/schemas/[name].md`` — schema file, active for this dir tree (R2 — covered later)
- Both ``.md`` (with YAML frontmatter) and ``.json`` accepted (R1.4).
"""

from __future__ import annotations

import re
import warnings
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from graph_core.persistence import load_node_file, FrontmatterError


_BRACKET_RE = re.compile(r"^\[(.+)\]$")
GENERIC_SCHEMA_NAME = "__generic__"


def is_bracketed(stem: str) -> bool:
    """Return True if a file stem is bracketed (e.g. ``[hypothesis]``)."""
    return bool(_BRACKET_RE.match(stem))


def canonical_name(stem: str) -> str:
    """Strip brackets to get the canonical schema name."""
    m = _BRACKET_RE.match(stem)
    if m:
        return m.group(1)
    return stem


@dataclass
class Schema:
    """A single schema definition loaded from disk."""

    name: str  # canonical name (no brackets)
    active: bool  # True if file was bracketed
    fields: dict[str, Any]  # declared fields (from frontmatter `fields` block, or empty)
    source_path: Path
    frontmatter: dict[str, Any] = field(default_factory=dict)


def _generic_schema() -> Schema:
    return Schema(
        name=GENERIC_SCHEMA_NAME,
        active=True,
        fields={},
        source_path=Path("__generic__"),
        frontmatter={"name": GENERIC_SCHEMA_NAME, "generic": True},
    )


@dataclass
class SchemaRegistry:
    """Registry of loaded schemas, keyed by canonical name."""

    schemas: dict[str, Schema] = field(default_factory=dict)
    errors: list[tuple[Path, str]] = field(default_factory=list)
    # T-020: track missing schemas so warnings stay one-shot per name.
    missing_warned: set[str] = field(default_factory=set)

    def get(self, name: str) -> Schema | None:
        return self.schemas.get(name)

    def has(self, name: str) -> bool:
        return name in self.schemas

    def names(self) -> set[str]:
        return set(self.schemas.keys())

    def active(self) -> dict[str, Schema]:
        return {n: s for n, s in self.schemas.items() if s.active}

    def resolve(self, type_name: str) -> Schema:
        """Return the schema for a node type, falling back to generic on miss (T-020 / R1.3).

        Emits a single :class:`UserWarning` per missing schema name across the
        registry's lifetime.
        """
        schema = self.schemas.get(type_name)
        if schema is not None:
            return schema
        if type_name not in self.missing_warned:
            self.missing_warned.add(type_name)
            warnings.warn(
                f"schema '{type_name}' not found; falling back to generic",
                UserWarning,
                stacklevel=2,
            )
        return _generic_schema()


def reload_schemas(
    directory: str | Path,
    previous: SchemaRegistry | None = None,
) -> SchemaRegistry:
    """Reload schemas, carrying forward `missing_warned` and warning on disappearances (T-020)."""
    new_reg = load_schemas_from_dir(directory)
    if previous is not None:
        new_reg.missing_warned = set(previous.missing_warned)
        gone = previous.names() - new_reg.names()
        for name in sorted(gone):
            if name not in new_reg.missing_warned:
                new_reg.missing_warned.add(name)
                warnings.warn(
                    f"schema '{name}' removed; nodes of this type will use generic fallback",
                    UserWarning,
                    stacklevel=2,
                )
    return new_reg


def load_schemas_from_dir(directory: str | Path) -> SchemaRegistry:
    """Load all schema files from ``directory``. R1.1 + R1.4."""
    d = Path(directory)
    reg = SchemaRegistry()
    if not d.is_dir():
        return reg
    # Iterate the directory ourselves so we have file paths.
    for p in sorted(d.iterdir()):
        if not p.is_file():
            continue
        if p.suffix.lower() not in {".md", ".json"}:
            continue
        try:
            nf = load_node_file(p)
        except FrontmatterError as e:
            reg.errors.append((p, str(e)))
            continue
        except Exception as e:  # noqa: BLE001
            reg.errors.append((p, f"{type(e).__name__}: {e}"))
            continue
        stem = p.stem
        active = is_bracketed(stem)
        # Schema name: prefer explicit frontmatter `name`, else canonical (de-bracketed) stem.
        fm_name = nf.frontmatter.get("name")
        if isinstance(fm_name, str) and fm_name:
            name = fm_name
        else:
            name = canonical_name(stem)
        # Schema fields can live under `fields:` in the frontmatter.
        declared_fields = nf.frontmatter.get("fields", {}) or {}
        if not isinstance(declared_fields, dict):
            reg.errors.append((p, "schema 'fields' must be a mapping"))
            continue
        # If both `[name].md` and `name.md` exist, the bracketed (active) one wins.
        existing = reg.schemas.get(name)
        if existing is not None and existing.active and not active:
            continue
        reg.schemas[name] = Schema(
            name=name,
            active=active,
            fields=declared_fields,
            source_path=p,
            frontmatter=nf.frontmatter,
        )
    return reg
