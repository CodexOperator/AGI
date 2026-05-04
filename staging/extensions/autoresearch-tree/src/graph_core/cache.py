"""Warm-load cache for the directory loader (T-013 / R7).

Content-addressed: cache key = (resolved directory path, sha256 of sorted
(relative path, file digest) tuples). Renaming a file changes the relative
path → digest changes → cache miss. Editing any file changes its sha256 →
cache miss.

R7.1 second load returns within noise floor.
R7.2 modifying any node file invalidates cache.
R7.3 cache key includes content-addressed digest so renaming is detected.
"""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Callable, Optional

from .graph import Graph
from .loader import LoadedNode, load_directory


def directory_digest(directory: str | Path) -> str:
    """SHA-256 over sorted ``(rel_path, sha256(file_bytes))`` tuples."""
    base = Path(directory).resolve()
    if not base.is_dir():
        return ""
    parts: list[bytes] = []
    for root, dirs, files in os.walk(base):
        dirs.sort()
        for fname in sorted(files):
            p = Path(root) / fname
            try:
                rel = p.relative_to(base).as_posix()
            except ValueError:
                continue
            try:
                content = p.read_bytes()
            except OSError:
                continue
            file_digest = hashlib.sha256(content).hexdigest()
            parts.append(f"{rel}\t{file_digest}".encode("utf-8"))
    h = hashlib.sha256()
    for p in parts:
        h.update(p)
        h.update(b"\n")
    return h.hexdigest()


class WarmLoadCache:
    """Memoize `load_directory(dir)` keyed on `(resolved_path, digest)`."""

    def __init__(self) -> None:
        self._cache: dict[tuple[str, str], tuple[Graph, list[LoadedNode]]] = {}
        self._stats: dict[str, int] = {"hits": 0, "misses": 0}

    def get(
        self,
        directory: str | Path,
        loader: Callable[[Path], tuple[Graph, list[LoadedNode]]] = load_directory,
    ) -> tuple[Graph, list[LoadedNode]]:
        base = Path(directory).resolve()
        digest = directory_digest(base)
        key = (str(base), digest)
        if key in self._cache:
            self._stats["hits"] += 1
            return self._cache[key]
        self._stats["misses"] += 1
        result = loader(base)
        self._cache[key] = result
        return result

    @property
    def hits(self) -> int:
        return self._stats["hits"]

    @property
    def misses(self) -> int:
        return self._stats["misses"]

    def clear(self) -> None:
        self._cache.clear()
        self._stats = {"hits": 0, "misses": 0}
