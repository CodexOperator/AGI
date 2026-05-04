"""Lazy body loading (T-007 / graph-core R4.1).

Wraps a node body in a deferred reader. The graph load path constructs
``LazyBody(path)`` without touching disk; the on-disk read happens on
first ``str(...)`` or ``.value`` access.

Counter hook (``LazyBody.set_reader_counter``) is exposed for tests
to assert read counts.
"""

from __future__ import annotations

from pathlib import Path
from typing import Callable, Optional


class LazyBody:
    """Deferred body reader. Reads file on first ``.value`` access only."""

    _counter: list[int] = [0]  # module-level test counter
    _reader: Callable[[Path], str] | None = None

    def __init__(self, path: str | Path) -> None:
        self._path = Path(path)
        self._cached: Optional[str] = None
        self._read_done = False

    @property
    def path(self) -> Path:
        return self._path

    @property
    def loaded(self) -> bool:
        return self._read_done

    @property
    def value(self) -> str:
        if not self._read_done:
            reader = LazyBody._reader or _default_reader
            text = reader(self._path)
            # Reuse the .md/.json frontmatter parser to strip frontmatter,
            # returning only the body portion.
            from .frontmatter import load_node_file

            nf = load_node_file(self._path, body=True)
            self._cached = nf.body
            self._read_done = True
            LazyBody._counter[0] += 1
        return self._cached or ""

    def __str__(self) -> str:
        return self.value

    @classmethod
    def reset_counter(cls) -> None:
        cls._counter[0] = 0

    @classmethod
    def read_count(cls) -> int:
        return cls._counter[0]


def _default_reader(path: Path) -> str:
    return path.read_text(encoding="utf-8")
