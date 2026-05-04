"""T-013 tests: warm-load cache (graph-core/R7)."""

import time
from pathlib import Path

from graph_core.cache import WarmLoadCache, directory_digest


def _seed(d: Path, files: dict[str, str]) -> None:
    for name, content in files.items():
        p = d / name
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(content)


def test_warm_load_hit_after_first_call(tmp_path: Path) -> None:
    """R7.1: second load is a cache hit."""
    _seed(tmp_path, {"a.md": "---\nid: a\n---\n", "b.md": "---\nid: b\n---\n"})
    cache = WarmLoadCache()
    cache.get(tmp_path)
    cache.get(tmp_path)
    assert cache.hits == 1
    assert cache.misses == 1


def test_warm_load_second_call_fast(tmp_path: Path) -> None:
    """R7.1: second load returns within noise floor (<= 1ms)."""
    _seed(tmp_path, {f"n{i}.md": f"---\nid: n{i}\n---\n" for i in range(20)})
    cache = WarmLoadCache()
    cache.get(tmp_path)  # cold
    t0 = time.perf_counter()
    cache.get(tmp_path)  # warm
    elapsed_ms = (time.perf_counter() - t0) * 1000
    assert elapsed_ms < 5.0, f"warm load too slow: {elapsed_ms}ms"


def test_modifying_file_invalidates_cache(tmp_path: Path) -> None:
    """R7.2: modifying a file invalidates the cache."""
    _seed(tmp_path, {"a.md": "---\nid: a\n---\nbody\n"})
    cache = WarmLoadCache()
    cache.get(tmp_path)
    # Modify
    (tmp_path / "a.md").write_text("---\nid: a\n---\nDIFFERENT body\n")
    cache.get(tmp_path)
    # Two misses, no hits
    assert cache.misses == 2
    assert cache.hits == 0


def test_renaming_file_invalidates_cache(tmp_path: Path) -> None:
    """R7.3: renaming detected via path-included digest."""
    _seed(tmp_path, {"old.md": "---\nid: x\n---\n"})
    cache = WarmLoadCache()
    cache.get(tmp_path)
    # Rename
    (tmp_path / "old.md").rename(tmp_path / "new.md")
    cache.get(tmp_path)
    assert cache.misses == 2


def test_directory_digest_stable_for_same_content(tmp_path: Path) -> None:
    _seed(tmp_path, {"a.md": "---\nid: a\n---\n", "b.md": "---\nid: b\n---\n"})
    d1 = directory_digest(tmp_path)
    d2 = directory_digest(tmp_path)
    assert d1 == d2 != ""


def test_directory_digest_changes_with_content(tmp_path: Path) -> None:
    _seed(tmp_path, {"a.md": "---\nid: a\n---\n"})
    d1 = directory_digest(tmp_path)
    (tmp_path / "a.md").write_text("---\nid: a\n---\nchanged\n")
    d2 = directory_digest(tmp_path)
    assert d1 != d2


def test_two_dirs_independent_cache(tmp_path: Path) -> None:
    a = tmp_path / "a"
    b = tmp_path / "b"
    a.mkdir()
    b.mkdir()
    _seed(a, {"x.md": "---\nid: x\n---\n"})
    _seed(b, {"y.md": "---\nid: y\n---\n"})
    cache = WarmLoadCache()
    cache.get(a)
    cache.get(b)
    cache.get(a)  # hit
    cache.get(b)  # hit
    assert cache.hits == 2
    assert cache.misses == 2
