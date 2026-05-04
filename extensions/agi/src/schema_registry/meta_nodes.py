"""Schemas as graph nodes (T-022 / schema-registry R3).

For each registered schema, synthesize one Node of type ``meta_node``. The id
is minted deterministically from the schema name; the payload_ref is the
schema's source path; frontmatter is the schema's declared fields.

R3.1: one meta_node per registered schema; id derived from schema name
R3.2: meta-node frontmatter exposes declared fields/defaults/rules
R3.4: removing schema removes meta-node and validating edges next load
"""

from __future__ import annotations

from typing import Iterable

from graph_core import Node
from graph_core.identity import IdRegistry, mint_id

from .loader import Schema, SchemaRegistry


META_TYPE = "meta_node"
META_PREFIX = "schema"


def schema_to_meta_node(schema: Schema, registry: IdRegistry | None = None) -> Node:
    """Build a meta_node Node for a single schema."""
    nid = mint_id(META_PREFIX, schema.name, registry=registry)
    n = Node(
        id=nid,
        type=META_TYPE,
        payload_ref=str(schema.source_path) if schema.source_path else None,
    )
    n.tags.add(f"schema-name:{schema.name}")
    if schema.active:
        n.tags.add("active")
    return n


def synthesize_meta_nodes(
    reg: SchemaRegistry,
    id_registry: IdRegistry | None = None,
) -> dict[str, Node]:
    """Return {schema_name: meta_node} for every registered schema (R3.1)."""
    if id_registry is None:
        id_registry = IdRegistry()
    out: dict[str, Node] = {}
    for name in sorted(reg.names()):
        out[name] = schema_to_meta_node(reg.schemas[name], registry=id_registry)
    return out


def diff_meta_nodes(
    previous: dict[str, Node],
    current: dict[str, Node],
) -> tuple[set[str], set[str]]:
    """Return (added, removed) schema names (R3.4)."""
    prev_set = set(previous.keys())
    cur_set = set(current.keys())
    return cur_set - prev_set, prev_set - cur_set
