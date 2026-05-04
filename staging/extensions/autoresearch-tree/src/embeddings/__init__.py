"""embeddings: vector embeddings of the graph (R1+)."""

from .node2vec import embed_graph, EmbeddingConfig, default_config
from .projection import project, ProjectionConfig
from .similarity import similar_to, cosine

__all__ = [
    "embed_graph",
    "EmbeddingConfig",
    "default_config",
    "project",
    "ProjectionConfig",
    "similar_to",
    "cosine",
]
