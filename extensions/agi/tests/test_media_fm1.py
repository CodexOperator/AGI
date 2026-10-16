"""goal:g5.4.2 Fm1 / Fm1b: the explainer outline's code excerpts are byte-equal to the engine at the cited sha, every
function it names resolves, every step it calls live has a caller, and a step it calls uncalled has none. Mutants: one edited
excerpt character -> 1 mismatch; a bogus function -> 1 unresolved; a wrong caller -> 1; an `uncalled:` on a called step -> 1."""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import media_fm1  # noqa: E402

REPO = subprocess.check_output(["git", "-C", str(HERE), "rev-parse", "--show-toplevel"], text=True).strip()
OUTLINE = Path(REPO) / ".agi/nodes/doc/season3-explainer-outline.md"


def _run(path, capsys):
    rc = media_fm1.check(str(path), REPO)
    out = capsys.readouterr().out
    return rc, int(re.search(r"mismatches=(\d+)", out).group(1)), int(re.search(r"unresolved=(\d+)", out).group(1))


def test_outline_is_green(capsys):
    rc, mism, unres = _run(OUTLINE, capsys)
    assert (rc, mism, unres) == (0, 0, 0)


def _mutant(tmp_path, old, new, count=1):
    text = OUTLINE.read_text()
    assert text.count(old) >= 1, old
    p = tmp_path / "m.md"
    p.write_text(text.replace(old, new, count))
    return p


def test_mutant_one_excerpt_character_is_one_mismatch(tmp_path, capsys):
    text = OUTLINE.read_text()
    i = text.index("@@excerpt")
    j = text.index("~~~~\n", i) + 5          # first byte of the first excerpt body
    p = tmp_path / "m.md"
    p.write_text(text[:j] + ("X" if text[j] != "X" else "Y") + text[j + 1:])
    assert _run(p, capsys)[1:] == (1, 0)


def test_mutant_a_function_that_does_not_exist_is_unresolved(tmp_path, capsys):
    p = _mutant(tmp_path, "fn: piece:agi-turn", "fn: piece:agi-turn-no-such-piece")
    assert _run(p, capsys)[1:] == (0, 1)


def test_mutant_a_wrong_caller_is_unresolved(tmp_path, capsys):
    p = _mutant(tmp_path, "live: sect <- piece:agi-brief", "live: sect <- piece:agi-meter")
    assert _run(p, capsys)[1:] == (0, 1)


def test_mutant_uncalled_on_a_called_step_is_unresolved(tmp_path, capsys):
    p = _mutant(tmp_path, "uncalled: agi-land", "uncalled: agi-turn")
    assert _run(p, capsys)[1:] == (0, 1)
