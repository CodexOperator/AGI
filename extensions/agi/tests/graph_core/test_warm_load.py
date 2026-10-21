"""T-013 tests: warm-load cache (graph-core/R7)."""

from pathlib import Path

import pytest

from graph_core.cache import WarmLoadCache, directory_digest
from graph_core.loader import load_directory


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


class _Spy:
    """A loader that counts its calls and loads for real (goal:g7.16.1.11.31.1)."""

    def __init__(self) -> None:
        self.calls = 0

    def __call__(self, base: Path):
        self.calls += 1
        return load_directory(base)


class _AlwaysLoads(WarmLoadCache):
    """The mutant: a get() that never trusts its cache and calls the loader every time."""

    def get(self, directory, loader=load_directory):
        self._stats["misses"] += 1
        return loader(Path(directory).resolve())


def _one_cold_five_warm(cache: WarmLoadCache, base: Path) -> None:
    """Fw1, the invariant's carrier: a warm get never calls the loader. Counted, not timed, so the
    box's load cannot move it (the digest walk every get() runs scales with load; a stopwatch on
    a hit measured the box, not the cache)."""
    spy = _Spy()
    for _ in range(6):   # 1 cold + 5 warm
        cache.get(base, loader=spy)
    assert spy.calls == 1, f"loader called {spy.calls}x over 1 cold + 5 warm gets"
    assert cache.hits == 5, f"hits {cache.hits}, wanted 5"


def test_warm_load_second_call_fast(tmp_path: Path) -> None:
    """R7.1: 1 cold get + 5 warm gets -> the loader ran once and the cache hit five times (no timing)."""
    _seed(tmp_path, {f"n{i}.md": f"---\nid: n{i}\n---\n" for i in range(20)})
    _one_cold_five_warm(WarmLoadCache(), tmp_path)


def test_warm_load_fw1_mutant_that_always_calls_the_loader_is_red(tmp_path: Path) -> None:
    """The same check on a get() that always calls the loader: 6 calls, 0 hits -> RED, every run."""
    _seed(tmp_path, {f"n{i}.md": f"---\nid: n{i}\n---\n" for i in range(20)})
    with pytest.raises(AssertionError, match="loader called 6x"):
        _one_cold_five_warm(_AlwaysLoads(), tmp_path)


def test_warm_load_has_no_wall_clock_claim() -> None:
    """Fw3: this file asserts no millisecond bound and claims no noise floor (they timed the box).
    The needles are built from pieces so this check does not contain what it forbids."""
    text = Path(__file__).read_text()
    for needle in ("< " + "5.0", "<= " + "1ms", "perf_" + "counter", "import " + "time"):
        assert needle not in text, needle


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
