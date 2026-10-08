"""Persistence layer (T-006 / R4)."""

from .frontmatter import load_node_file, save_node_file, FrontmatterError
from .frontmatter import load_node_dir, DirLoadResult, LoadError
from .backend import PersistenceBackend
from .filesystem import FilesystemBackend
from .in_memory import InMemoryBackend
from .sqlite_backend import SQLiteBackend

__all__ = [
    "load_node_file",
    "save_node_file",
    "load_node_dir",
    "FrontmatterError",
    "DirLoadResult",
    "LoadError",
    "PersistenceBackend",
    "FilesystemBackend",
    "InMemoryBackend",
    "SQLiteBackend",
]
