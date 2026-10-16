"""goal:g5.4.2 sibling-grep table (council 06:23Z 10-16). Mutants: a known sibling left in and listed `kept` with no reason -> RED; a hit with
no row -> RED; a `fixed` row whose old sentence is still in the script -> RED; a grep with no rows at all -> RED; the real table is green."""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import media_sibling  # noqa: E402

REPO = subprocess.check_output(["git", "-C", str(HERE), "rev-parse", "--show-toplevel"], text=True).strip()
SCRIPT = Path(REPO) / ".agi/context/media/season3-explainer-script.md"
DIFF = Path(REPO) / ".agi/context/media/season3-explainer-recut2-diff.md"
OLD = "81cb084d6b"


def _run(tmp_path, diff_text, capsys):
    p = tmp_path / "d.md"
    p.write_text(diff_text)
    rc = media_sibling.check(str(SCRIPT), str(p), OLD, REPO)
    out = capsys.readouterr().out
    return rc, {k: int(v) for k, v in re.findall(r"^(unlisted|stale|not_fixed|no_reason)=(\d+)", out, re.M)}


def test_the_real_table_is_green(tmp_path, capsys):
    rc, c = _run(tmp_path, DIFF.read_text(), capsys)
    assert rc == 0 and c == {"unlisted": 0, "stale": 0, "not_fixed": 0, "no_reason": 0}


def test_mutant_a_sibling_kept_with_no_reason_is_red(tmp_path, capsys):
    text = DIFF.read_text()
    old = "hit R2H1 | kept:a return value of nothing from a reader function, not a claim about the engine being idle, pair C3.6 |"
    assert old in text
    rc, c = _run(tmp_path, text.replace(old, "hit R2H1 | kept: |"), capsys)
    assert rc != 0 and c["no_reason"] == 1


def test_mutant_a_hit_with_no_row_is_red(tmp_path, capsys):
    text = DIFF.read_text()
    row = next(x for x in text.split("\n") if x.startswith("hit R1 | kept:"))
    rc, c = _run(tmp_path, text.replace(row + "\n", ""), capsys)
    assert rc != 0 and c["unlisted"] == 1


def test_mutant_a_sibling_left_in_and_marked_fixed_is_red(tmp_path, capsys):
    text = DIFF.read_text()
    s = "The post can recover and merge by hand."
    row = next(x for x in text.split("\n") if x.startswith("hit F2 | kept:") and s in x)
    rc, c = _run(tmp_path, text.replace(row, f"hit F2 | fixed | {s} => {s}"), capsys)
    assert rc != 0 and c["not_fixed"] == 1


def test_mutant_a_grep_that_hits_a_new_sibling_is_red(tmp_path, capsys):
    """Widen one grep to a phrase the script still says in another sentence: the new hit has no row."""
    text = DIFF.read_text().replace("grep F2: by hand|", "grep F2: by hand|signed commit|")
    rc, c = _run(tmp_path, text, capsys)
    assert rc != 0 and c["unlisted"] >= 1


def test_no_grep_lines_is_not_green(tmp_path, capsys):
    rc, _ = _run(tmp_path, "# empty\n", capsys)
    assert rc != 0
