"""Validation engine wrapping the DSL (T-024 / schema-registry R4)."""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from .dsl import ValidationError, parse_rules, validate
from .loader import SchemaRegistry


@dataclass
class ValidationResult:
    errors: list[ValidationError] = field(default_factory=list)

    def failures_by_schema(self) -> dict[str, int]:
        """R4.4: query failure counts per schema."""
        counts: dict[str, int] = defaultdict(int)
        for e in self.errors:
            counts[e.schema] += 1
        return dict(counts)

    def failures_for_node(self, node_id: str) -> list[ValidationError]:
        return [e for e in self.errors if e.node_id == node_id]


def validate_nodes_against_registry(
    nodes: list[tuple[str, str, dict[str, Any]]],
    registry: SchemaRegistry,
) -> ValidationResult:
    """Validate a list of (node_id, schema_name, node_frontmatter) tuples.

    R4.1: nodes whose schema has no validation block → no per-field checks.
    R4.2: violators produce a structured ValidationError.
    R4.3: errors do not abort the rest of the load.
    """
    result = ValidationResult()
    for node_id, schema_name, frontmatter in nodes:
        schema = registry.schemas.get(schema_name)
        if schema is None:
            continue
        rules = parse_rules(schema.frontmatter)
        errs = validate(node_id, schema_name, frontmatter, rules)
        result.errors.extend(errs)
    return result
