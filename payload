"""In-memory persistence backend for tests (T-015 / R8.2)."""

from __future__ import annotations

from pathlib import Path
from typing import Iterator

from .backend import PersistenceBackend
from .frontmatter import NodeFile


class InMemoryBackend:
    """Test backend. Stores NodeFile objects in a dict keyed on resolved path string."""

    def __init__(self) -> None:
        self._store: dict[str, NodeFile] = {}

    def load(self, path: str | Path) -> NodeFile:
        key = str(Path(path).resolve())
        if key not in self._store:
            from .frontmatter import FrontmatterError

            raise FrontmatterError(f"in-memory backend: no entry for {path}")
        return self._store[key]

    def save(self, path: str | Path, nf: NodeFile) -> None:
        key = str(Path(path).resolve())
        self._store[key] = nf

    def list(self, directory: str | Path) -> Iterator[Path]:
        base = str(Path(directory).resolve())
        out = []
        for k in sorted(self._store.keys()):
            if k.startswith(base):
                out.append(Path(k))
        return iter(out)

    def watch(self, directory: str | Path) -> Iterator[Path]:
        return self.list(directory)


def _check_protocol() -> None:
    b: PersistenceBackend = InMemoryBackend()
    _ = b
