"""Edge primitive — implements graph-core/R2.

Four-field record. Equality + hash on the (source, target, relation) triple
so a set of edges deduplicates same-triple inserts (R2.3).

Acceptance criteria (T-003 / R2):
- R2.2: edge exposes source_id, target_id, relation, optional tags
- R2.3: idempotent insert for the same (source, target, relation) triple
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(eq=False)
class Edge:
    """Directed edge between two nodes by id, typed by `relation`.

    Equality and hash are computed only over (source_id, target_id, relation),
    so inserting the same triple twice into a set is a no-op (R2.3).
    Tags are out-of-band metadata and do NOT affect identity.
    """

    source_id: str
    target_id: str
    relation: str
    tags: set[str] = field(default_factory=set)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Edge):
            return NotImplemented
        return (
            self.source_id == other.source_id
            and self.target_id == other.target_id
            and self.relation == other.relation
        )

    def __hash__(self) -> int:
        return hash((self.source_id, self.target_id, self.relation))

    @property
    def triple(self) -> tuple[str, str, str]:
        """The identity triple (source_id, target_id, relation)."""
        return (self.source_id, self.target_id, self.relation)
