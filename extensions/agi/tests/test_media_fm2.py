"""goal:g5.4.2 Fm2 + the claim/cite pairs: the explainer script's narration carries no bare number (digits or number words) outside a
slot, every pair's cite contains its needle, every slot resolves at the chapter's sha. Mutants: a typed count -> 1; "five thousand nodes"
-> 1 (one finding per line); a pair whose needle is not in the cited range -> 1; a slot that does not resolve -> 1."""
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import media_fm1  # noqa: E402
import media_fm2  # noqa: E402

REPO = subprocess.check_output(["git", "-C", str(HERE), "rev-parse", "--show-toplevel"], text=True).strip()
SCRIPT = Path(REPO) / ".agi/context/media/season3-explainer-script.md"


def _run(path, capsys):
    rc = media_fm2.check(str(path), REPO)
    out = capsys.readouterr().out
    g = lambda k: int(re.search(k + r"=(\d+)", out).group(1))  # noqa: E731
    return rc, g("pairs_bad"), g("bare_numbers"), g("bad_slots")


def _mut(tmp_path, old, new):
    text = SCRIPT.read_text()
    assert old in text, old
    p = tmp_path / "m.md"
    p.write_text(text.replace(old, new, 1))
    return p


def test_script_is_green(capsys):
    assert _run(SCRIPT, capsys) == (0, 0, 0, 0)


def test_script_is_an_hour_or_less_and_the_html_is_not_smaller_than_nothing(capsys):
    media_fm2.check(str(SCRIPT), REPO)
    out = capsys.readouterr().out
    words = int(re.search(r"words_narration=(\d+)", out).group(1))
    assert 6500 <= words <= 9000    # about 45 to 60 minutes at the measured sample pace


def test_mutant_a_typed_count_is_one(tmp_path, capsys):
    p = _mut(tmp_path, "It is only {{bytes:sect}} bytes long.", "It is only 214 bytes long.")
    assert _run(p, capsys)[2] == 1


def test_mutant_five_thousand_nodes_is_one(tmp_path, capsys):
    p = _mut(tmp_path, "Well now, good evening, friends,", "Well now, five thousand nodes, friends,")
    assert _run(p, capsys)[2] == 1


def test_mutant_a_needle_not_in_the_cite_is_one(tmp_path, capsys):
    p = _mut(tmp_path, "~ .agi/nodes\n", "~ a-string-that-the-cite-does-not-hold\n")
    assert _run(p, capsys)[1] == 1


def test_mutant_a_slot_that_does_not_resolve_is_one(tmp_path, capsys):
    p = _mut(tmp_path, "{{bytes:sect}}", "{{bytes:no-such-piece}}")
    assert _run(p, capsys)[3] == 1


def test_render_speaks_every_slot():
    text = SCRIPT.read_text()
    sha = re.search(r"(?m)^sha: *([0-9a-f]+)", text).group(1)
    spoken = media_fm2.render("It is only {{bytes:sect}} bytes long.", REPO, sha)
    assert re.search(r"[a-z]", spoken) and not re.search(r"\d", spoken)
