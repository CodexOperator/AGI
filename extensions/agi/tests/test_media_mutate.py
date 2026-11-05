"""goal:g5.4.2 M4: the hand-break harness's own rules (council 10-21 09:52Z). A fixture project with a one-line module and a one-line test: nothing here touches media_video.py."""
import os
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import media_mutate as mm  # noqa: E402


@pytest.fixture
def proj(tmp_path):
    (tmp_path / "m.py").write_text("X = 1  # same size edits\nY = 0.8\n")
    (tmp_path / "test_m.py").write_text("import m\n\ndef test_x():\n    assert m.X == 1\n    assert m.Y == 0.8\n")
    return tmp_path


def test_the_harness_source_enforces_its_three_rules():
    src = (HERE / "media_mutate.py").read_text()
    assert 'PYTHONDONTWRITEBYTECODE="1"' in src and '"-B"' in src and "def clean_pyc" in src
    assert src.count("clean_pyc(") >= 4 and "read_bytes() != original" in src          # cleaned before and after each mutant, restored byte for byte, checked


def test_a_noop_survives_and_a_same_size_same_second_edit_is_killed_and_the_file_is_restored(proj):
    before = (proj / "m.py").read_bytes()
    table = [("noop", "X = 1", "X = 1"), ("same size", "X = 1", "X = 0"), ("other same size", "Y = 0.8", "Y = 0.0")]
    res = mm.sweep(proj / "m.py", [proj / "test_m.py"], table, proj, log=lambda r: None)
    assert [(n, s) for n, s, _ in res] == [("noop", "SURVIVED"), ("same size", "KILLED"), ("other same size", "KILLED")]
    assert (proj / "m.py").read_bytes() == before


def test_stale_bytecode_cannot_hide_a_kill(proj):
    """Plant the mechanism: compile the ORIGINAL, then make a same-size edit inside the same second; without the clean-up the old .pyc would be loaded and the mutant would 'survive'."""
    import py_compile
    m = proj / "m.py"
    py_compile.compile(str(m), doraise=True)                      # a .pyc of the original, mtime and size recorded
    mtime = m.stat().st_mtime
    m.write_text(m.read_text().replace("X = 1", "X = 0"))          # same size
    os.utime(m, (mtime, mtime))                                    # same mtime: the pyc looks current
    m.write_text(m.read_text().replace("X = 0", "X = 1"))          # put the original back for the sweep
    os.utime(m, (mtime, mtime))
    res = mm.sweep(m, [proj / "test_m.py"], [("same size", "X = 1", "X = 0")], proj, log=lambda r: None)
    assert res[0][1] == "KILLED"
    assert not list((proj / "__pycache__").glob("m.*.pyc")) if (proj / "__pycache__").exists() else True


def test_a_missing_pattern_is_reported_not_silently_skipped(proj):
    res = mm.sweep(proj / "m.py", [proj / "test_m.py"], [("nothing", "Z = 9", "Z = 8")], proj, log=lambda r: None)
    assert res[0][1] == "PATTERN MISSING" and mm.verdict(res) == ["nothing: PATTERN MISSING"]


def test_verdict_flags_a_killed_noop_a_surviving_same_size_edit_and_a_survivor():
    bad = mm.verdict([(mm.NOOP[0], "KILLED", ""), (mm.SAME_SIZE[0], "SURVIVED", ""), ("a real one", "SURVIVED", ""), ("another", "KILLED", "")])
    assert len(bad) == 3 and any("no-op" in b for b in bad) and any("same-size" in b for b in bad) and any("a real one" in b for b in bad)
    assert mm.verdict([(mm.NOOP[0], "SURVIVED", ""), (mm.SAME_SIZE[0], "KILLED", ""), ("x", "KILLED", "")]) == []


def test_every_pattern_of_the_real_table_is_in_the_real_target_exactly_once():
    src = (HERE / "media_video.py").read_text()
    for name, a, b in [mm.NOOP, mm.SAME_SIZE] + mm.MUTANTS:
        assert src.count(a) == 1, name
        assert a != b or name == mm.NOOP[0], name
