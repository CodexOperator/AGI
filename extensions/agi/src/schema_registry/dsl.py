"""Validation rule DSL (T-024 / schema-registry R4).

A schema's frontmatter MAY include a ``validation:`` block. Recognized rules:

  required: [list of field names]      # all must be present and non-None
  types:                                # field -> expected type
    field_name: int | str | bool | float | list | dict
  regex:                                # field -> regex pattern; field must match
    field_name: '^[a-z]+$'

When the schema has no ``validation`` block, no rules apply (R4.1).
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any


_TYPE_MAP: dict[str, type] = {
    "int": int,
    "str": str,
    "bool": bool,
    "float": float,
    "list": list,
    "dict": dict,
}


@dataclass(frozen=True)
class ValidationError:
    """A single validation failure (R4.2)."""

    node_id: str
    schema: str
    rule: str  # 'required' | 'types' | 'regex'
    field: str
    reason: str


def parse_rules(frontmatter: dict[str, Any]) -> dict[str, Any]:
    """Extract a normalized validation block from schema frontmatter."""
    block = frontmatter.get("validation") or {}
    if not isinstance(block, dict):
        return {}
    return {
        "required": list(block.get("required", []) or []),
        "types": dict(block.get("types", {}) or {}),
        "regex": dict(block.get("regex", {}) or {}),
    }


def validate(
    node_id: str,
    schema_name: str,
    node_frontmatter: dict[str, Any],
    rules: dict[str, Any],
) -> list[ValidationError]:
    """Apply rules to a node, returning a list of errors. R4.1: empty rules → []."""
    errors: list[ValidationError] = []
    if not rules:
        return errors
    for f in rules.get("required", []) or []:
        v = node_frontmatter.get(f)
        if v is None or (isinstance(v, str) and not v.strip()):
            errors.append(
                ValidationError(node_id, schema_name, "required", f, "missing or empty")
            )
    for f, type_name in (rules.get("types", {}) or {}).items():
        if f not in node_frontmatter:
            continue
        expected = _TYPE_MAP.get(str(type_name))
        if expected is None:
            continue
        v = node_frontmatter[f]
        if not isinstance(v, expected):
            errors.append(
                ValidationError(
                    node_id,
                    schema_name,
                    "types",
                    f,
                    f"expected {type_name}, got {type(v).__name__}",
                )
            )
    for f, pattern in (rules.get("regex", {}) or {}).items():
        if f not in node_frontmatter:
            continue
        try:
            compiled = re.compile(str(pattern))
        except re.error:
            errors.append(
                ValidationError(node_id, schema_name, "regex", f, "invalid pattern")
            )
            continue
        v = node_frontmatter[f]
        if not isinstance(v, str) or not compiled.search(v):
            errors.append(
                ValidationError(node_id, schema_name, "regex", f, f"value did not match {pattern!r}")
            )
    return errors
