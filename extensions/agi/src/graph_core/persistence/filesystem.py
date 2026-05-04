"""Filesystem persistence backend (T-015 / R8.3)."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Iterator

from .backend import PersistenceBackend
from .frontmatter import NodeFile, load_node_file, save_node_file


class FilesystemBackend:
    """Default backend. No external services (R8.3)."""

    def load(self, path: str | Path) -> NodeFile:
        return load_node_file(path)

    def save(self, path: str | Path, nf: NodeFile) -> None:
        save_node_file(path, nf)

    def list(self, directory: str | Path) -> Iterator[Path]:
        d = Path(directory)
        if not d.is_dir():
            return iter([])
        out = []
        for root, dirs, files in os.walk(d):
            dirs.sort()
            for fname in sorted(files):
                p = Path(root) / fname
                if p.suffix.lower() in {".md", ".json"}:
                    out.append(p.resolve())
        return iter(out)

    def watch(self, directory: str | Path) -> Iterator[Path]:
        # Simple polling implementation; one shot returning all files.
        return self.list(directory)


# Static check that the backend satisfies the Protocol.
def _check_protocol() -> None:
    b: PersistenceBackend = FilesystemBackend()
    _ = b
