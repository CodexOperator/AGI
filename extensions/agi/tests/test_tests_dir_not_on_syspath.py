"""The tests/ directory must never shadow a src package (collection shadowing, found 10-12).

tests/renderers and tests/embeddings are packages with an __init__.py. About twenty test modules put extensions/agi/tests on sys.path at import time
(`sys.path.insert(0, <tests dir>)`, so a sibling test imports by its bare name); every file collected after the first one then imported the TEST
directory as `renderers` / `embeddings` instead of the src packages: `ImportError: cannot import name build_representation from renderers
(.../tests/renderers/__init__.py)`, 9 collection errors, `pytest extensions/agi/tests` rc 2. The tests conftest now demotes the entry to the END of
sys.path before each collector (pytest_collectstart) and after collection. These rows run AFTER collection, so they see what is left behind.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

TESTS = Path(__file__).resolve().parent
SRC = TESTS.parent / "src"


def _idx(path: Path) -> list[int]:
    return [i for i, p in enumerate(sys.path) if p and os.path.realpath(p) == str(path)]


def test_the_tests_dir_is_never_ahead_of_the_src_dir_on_sys_path():
    t, s = _idx(TESTS), _idx(SRC)
    assert s, f"{SRC} is not on sys.path"
    assert all(i > min(s) for i in t), f"{TESTS} (sys.path {t}) is ahead of {SRC} ({s}): tests/renderers and tests/embeddings shadow the src packages"


def test_the_src_packages_win_over_a_tests_dir_of_the_same_name():
    import embeddings
    import renderers

    for mod in (renderers, embeddings):
        f = Path(mod.__file__).resolve()
        assert SRC in f.parents, f"{mod.__name__} resolves to {f}, not under {SRC}"
