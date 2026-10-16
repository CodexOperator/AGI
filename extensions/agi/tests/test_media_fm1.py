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


def _run(path, capsys, chapters=18):
    rc = media_fm1.check(str(path), REPO, chapters)
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


def _write(tmp_path, text):
    p = tmp_path / "m.md"
    p.write_text(text)
    return p


def test_mutant_every_sha_header_dropped_is_not_a_green(tmp_path, capsys):
    """The vacuous pass: with no `sha:` line above them the fn:/live:/uncalled: lines used to be SKIPPED, so the outline printed
    fn=0 live=0 unresolved=0 and exited 0. Now each such line counts as unresolved."""
    text = re.sub(r"(?m)^sha: .*\n", "", OUTLINE.read_text())
    rc, mism, unres = _run(_write(tmp_path, text), capsys)
    assert rc != 0 and unres >= 1


def test_mutant_one_chapters_fn_removed_is_one(tmp_path, capsys):
    text = OUTLINE.read_text()
    a = text.index("## C3 ")
    b = text.index("## C4 ")
    chap = re.sub(r"(?m)^fn: .*\n", "", text[a:b])
    rc, mism, unres = _run(_write(tmp_path, text[:a] + chap + text[b:]), capsys)
    assert (mism, unres) == (0, 1) and rc == 1


def test_a_file_with_nothing_to_check_is_not_green(tmp_path, capsys):
    rc, mism, unres = _run(_write(tmp_path, "# nothing\n\njust prose\n"), capsys)
    assert rc != 0 and unres >= 1


def test_the_m2_script_is_green_for_fm1(capsys):
    """The script payload obeys the same excerpt / function / caller rules as the outline (stage M2)."""
    script = Path(REPO) / ".agi/context/media/season3-explainer-script.md"
    rc, mism, unres = _run(script, capsys)
    assert (rc, mism, unres) == (0, 0, 0)


def test_mutant_chapter_headings_renamed_is_not_green(tmp_path, capsys):
    """The chapters must equal the outline's 18: with the `## C<n>` headings renamed the file used to count 0 chapters and exit 0."""
    text = re.sub(r"(?m)^## C(\d+)", r"## Chapter \1", OUTLINE.read_text())
    rc, mism, unres = _run(_write(tmp_path, text), capsys)
    assert rc != 0 and unres >= 1


def test_mutant_an_excerpt_range_past_eof_is_a_mismatch(tmp_path, capsys):
    """sed -n a,bp stops at EOF, so a range that runs past the end is cut short by the slice: b > len counts as a mismatch."""
    sha = "6432bf88d5"
    path = ".agi/nodes/goal/g7.16.1.1.6.2.md"
    body = subprocess.check_output(["git", "-C", REPO, "show", f"{sha}:{path}"], text=True).split("\n")
    if body[-1] == "":
        body.pop()
    n = len(body)
    tail = "\n".join(body[n - 2:n])
    good = f"## C0 · t\n\nsha: {sha}\n\nfn: piece:sect\n\n@@excerpt {sha}:{path}:L{n - 1}-L{n}\n~~~~\n{tail}\n~~~~\n"
    rc, mism, unres = _run(_write(tmp_path, good), capsys, 1)
    assert (rc, mism, unres) == (0, 0, 0)    # the in-range excerpt is green
    bad = good.replace(f"L{n - 1}-L{n}", f"L{n - 1}-L{n + 50}")
    rc, mism, unres = _run(_write(tmp_path, bad), capsys, 1)
    assert mism == 1 and rc != 0
