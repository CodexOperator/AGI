"""agi-ring-merge: each box writes only its own posts' signer lines, and never deletes one (the local-town carrier)."""
import subprocess
import sys
from pathlib import Path

TOOL = Path(__file__).resolve().parents[1] / "guard" / "agi-ring-merge"
KEY = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5" + "A" * 48
KEY2 = "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5" + "B" * 48
TM = 'tm@agi namespaces="git",valid-after="20260101000000Z" ' + KEY
TM_STAMPED = 'tm@agi namespaces="git",valid-after="20260101000000Z",valid-before="20260201000000Z" ' + KEY
TM_NEW = 'tm@agi namespaces="git",valid-after="20260201000000Z" ' + KEY2
SM = 'sm@agi namespaces="git",valid-after="20260101000000Z" ' + KEY


def merge(ring, home, text, *flags):
    return subprocess.run([sys.executable, str(TOOL), str(ring), home, *flags], input=text, capture_output=True, text=True, check=True)


def lines(ring):
    return ring.read_text().splitlines()


def test_home_takes_a_new_key_and_the_stamp(tmp_path):
    ring = tmp_path / "r"
    ring.write_text(TM + "\n" + SM + "\n")
    merge(ring, "tm", TM_STAMPED + "\n" + TM_NEW + "\n")
    assert lines(ring) == [TM_STAMPED, SM, TM_NEW]


def test_a_line_for_a_post_the_other_box_is_not_home_to_is_dropped(tmp_path):
    ring = tmp_path / "r"
    ring.write_text(SM + "\n")
    forged = 'sm@agi namespaces="git",valid-after="20260301000000Z" ' + KEY2
    merge(ring, "tm", forged + "\n")
    assert lines(ring) == [SM]


def test_not_inverts_home(tmp_path):
    ring = tmp_path / "r"
    merge(ring, "tm", TM + "\n" + SM + "\n", "--not")
    assert lines(ring) == [SM]


def test_never_deletes_and_keeps_unparsed_own_lines(tmp_path):
    ring = tmp_path / "r"
    ring.write_text("# a comment\n" + TM + "\n")
    merge(ring, "tm", "")
    assert lines(ring) == ["# a comment", TM]


def test_unparsed_input_is_refused_and_a_second_run_changes_nothing(tmp_path):
    ring = tmp_path / "r"
    out = merge(ring, "tm", "tm@agi junk\n" + TM + "\n")
    assert "refused" in out.stderr and lines(ring) == [TM]
    before = ring.stat().st_mtime_ns
    assert "0 line(s) changed" in merge(ring, "tm", TM + "\n").stdout
    assert ring.stat().st_mtime_ns == before
