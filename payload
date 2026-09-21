"""Pluggable persistence backend Protocol (T-015 / graph-core R8).

Defines a backend contract independent of any specific store. The default
filesystem backend ships; an in-memory backend is provided for tests.
Configuration via ``context/config/graph-core.toml`` selects the backend
(R8.4).
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterator, Protocol, runtime_checkable

from .frontmatter import NodeFile


@runtime_checkable
class PersistenceBackend(Protocol):
    """Required surface for any backend (R8.1)."""

    def load(self, path: str | Path) -> NodeFile: ...

    def save(self, path: str | Path, nf: NodeFile) -> None: ...

    def list(self, directory: str | Path) -> Iterator[Path]: ...

    def watch(self, directory: str | Path) -> Iterator[Path]:
        """Yield paths whose contents have changed since last poll.
        Polling-based default; backends MAY override with notify-based watchers.
        """
        ...
