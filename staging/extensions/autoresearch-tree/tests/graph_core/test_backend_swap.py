"""T-015 tests: pluggable backend (graph-core/R8)."""

from pathlib import Path

from graph_core.persistence import (
    FilesystemBackend,
    InMemoryBackend,
    PersistenceBackend,
)
from graph_core.persistence.frontmatter import NodeFile


def test_filesystem_backend_satisfies_protocol() -> None:
    b = FilesystemBackend()
    assert isinstance(b, PersistenceBackend)


def test_in_memory_backend_satisfies_protocol() -> None:
    b = InMemoryBackend()
    assert isinstance(b, PersistenceBackend)


def test_filesystem_round_trip(tmp_path: Path) -> None:
    """R8.3: filesystem default with no external services."""
    b = FilesystemBackend()
    nf = NodeFile(frontmatter={"id": "x"}, body="body", suffix=".md")
    p = tmp_path / "x.md"
    b.save(p, nf)
    loaded = b.load(p)
    assert loaded.frontmatter == nf.frontmatter
    assert loaded.body == nf.body


def test_in_memory_round_trip(tmp_path: Path) -> None:
    """R8.2: in-memory backend used in tests."""
    b = InMemoryBackend()
    nf = NodeFile(frontmatter={"id": "y"}, body="y-body", suffix=".md")
    p = tmp_path / "y.md"
    b.save(p, nf)
    loaded = b.load(p)
    assert loaded.frontmatter == nf.frontmatter
    assert loaded.body == nf.body


def test_swappable_in_caller_code(tmp_path: Path) -> None:
    """R8.2: swap backends without changing caller code."""

    def caller(backend: PersistenceBackend, p: Path, nf: NodeFile) -> NodeFile:
        backend.save(p, nf)
        return backend.load(p)

    nf = NodeFile(frontmatter={"id": "z"}, body="z", suffix=".md")
    fs = caller(FilesystemBackend(), tmp_path / "z.md", nf)
    mem = caller(InMemoryBackend(), tmp_path / "zz.md", nf)
    assert fs.frontmatter == mem.frontmatter == nf.frontmatter


def test_filesystem_no_network_imports() -> None:
    """R8.3: default install requires no external service — quick check on imports."""
    import inspect

    from graph_core.persistence import filesystem as fs_mod

    src = inspect.getsource(fs_mod)
    assert "import requests" not in src
    assert "import socket" not in src
    assert "urllib" not in src.split("# ")[0]  # no top-level urllib usage
