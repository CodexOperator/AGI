"""T-007 tests: lazy body loading (graph-core/R4.1)."""

from pathlib import Path

from graph_core.persistence.lazy_body import LazyBody


FIXTURE = Path(__file__).parent.parent / "fixtures" / "nodes" / "sample.md"


def test_construct_does_not_read() -> None:
    LazyBody.reset_counter()
    lb = LazyBody(FIXTURE)
    assert LazyBody.read_count() == 0
    assert lb.loaded is False


def test_first_access_reads_once() -> None:
    LazyBody.reset_counter()
    lb = LazyBody(FIXTURE)
    _ = lb.value
    assert LazyBody.read_count() == 1
    assert lb.loaded is True


def test_repeated_access_does_not_reread() -> None:
    LazyBody.reset_counter()
    lb = LazyBody(FIXTURE)
    _ = lb.value
    _ = lb.value
    _ = str(lb)
    assert LazyBody.read_count() == 1


def test_body_content_strips_frontmatter() -> None:
    LazyBody.reset_counter()
    lb = LazyBody(FIXTURE)
    body = lb.value
    assert "---" not in body or not body.lstrip().startswith("---")
    assert "hypothesis" in body.lower() or "lru_cache" in body.lower()
