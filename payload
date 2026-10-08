"""Node primitive — implements graph-core/R1.

Six-field, no-frills record. Type semantics deferred to schema-registry.
ID minting deferred to T-005 (mint_id / IdRegistry).

Acceptance criteria covered (T-001 / R1):
- R1.1: id, type, payload_ref, parents, children, tags exposed; nothing else mandatory
- R1.2: no-parent root and no-child leaf accepted
- R1.4: tags is a set of strings independent of typed links
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Node:
    """Generic graph node.

    Exactly seven fields. No timestamps. No auto-derived fields.
    """

    id: str
    type: str
    payload_ref: Optional[str] = None
    parents: set[str] = field(default_factory=set)
    children: set[str] = field(default_factory=set)
    tags: set[str] = field(default_factory=set)
    origin: Optional[str] = None  # "build-site" if from snapshot, None = agent-generated

    @property
    def is_root(self) -> bool:
        """A node with no parents is a root (R1.2)."""
        return not self.parents

    @property
    def is_leaf(self) -> bool:
        """A node with no children is a leaf (R1.2)."""
        return not self.children

    def add_parent(self, parent_id: str) -> None:
        """Add a parent id with self-loop guard (T-002 / R1.3).

        Set semantics absorb duplicates silently.
        Self-loop raises :class:`SelfLoopError`.
        """
        from .errors import SelfLoopError

        if parent_id == self.id:
            raise SelfLoopError(self.id, "parents")
        self.parents.add(parent_id)

    def add_child(self, child_id: str) -> None:
        """Add a child id with self-loop guard (T-002 / R1.3).

        Set semantics absorb duplicates silently.
        Self-loop raises :class:`SelfLoopError`.
        """
        from .errors import SelfLoopError

        if child_id == self.id:
            raise SelfLoopError(self.id, "children")
        self.children.add(child_id)

    def add_tag(self, tag: str) -> None:
        """Add a tag (independent of typed links — R1.4)."""
        self.tags.add(tag)
