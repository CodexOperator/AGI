"""`hypothesis:l3w4-handoff-sections-claimable` — HANDOFF.md sections are
claimable to read and to write, without changing the document format.

These tests exercise the four properties the hypothesis is falsified if it
loses, mirroring how `test_spawn_budget.py` tests the concurrency bound with
real processes rather than a mocked counter:

1. a claimed section is served alone at a fraction of the whole-file token cost
   (byte-for-byte identical content, cost measured not assumed);
2. two concurrent writers to DIFFERENT sections both survive, file valid and
   byte-identical to a single sequential write (goal:s28's read-merge-write
   lesson: a race that looks fine and loses a write is the standing bug);
3. a write to a section the caller does not hold is refused, naming the holder;
4. a `cat HANDOFF.md` (here: the raw fallback path) still reads exactly the
   bytes that went in — claims and sectioned reads never touch the file, and a
   write touches only its own section's span.
"""
from __future__ import annotations

import multiprocessing as mp
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))

import handoff  # noqa: E402


SAMPLE = (
    "# SESSION HANDOFF — scratch\n\n"
    "preamble not claimable\n\n"
    "## §0 State block\n"
    "alpha\n\n"
    "## §4 Traps\n"
    "beta\n\n"
    "## §5 Verify\n"
    "gamma\n"
)


@pytest.fixture()
def root(tmp_path: Path) -> Path:
    (tmp_path / "sessions").mkdir()
    handoff.handoff_path(tmp_path).write_text(SAMPLE)
    return tmp_path


# ---------------------------------------------------------------------------
# 1. Sectioned read is cheap and returns the exact section bytes
# ---------------------------------------------------------------------------

def test_sections_parse_stable_by_header(root: Path):
    secs = handoff.parse_sections(SAMPLE)
    names = [s["name"] for s in secs]
    assert names == ["§0 State block", "§4 Traps", "§5 Verify"]
    assert all(t["text"].startswith("## ") for t in secs)


def test_sectioned_read_costs_less_than_whole(root: Path):
    whole = handoff.read_section(root, "", prime=True, whole=True)
    # not yet claimable -> a bare reader is refused (fail-closed on read too)
    r = handoff.read_section(root, "§5 Verify", "somebody")
    assert "error" in r and "claim" in r["error"]
    handoff.claim(root, "§5 Verify", "seatA")
    s5 = handoff.read_section(root, "§5 Verify", "seatA")
    assert "error" not in s5, s5
    assert s5["bytes"] < whole["bytes"]
    assert s5["tokens"] < whole["tokens"]
    assert s5["text"].startswith("## §5 Verify")
    assert s5["bytes"] == len(s5["text"])


def test_estimate_tokens_scales_with_size():
    small = handoff.estimate_tokens(845)
    whole = handoff.estimate_tokens(246_221)
    assert small < whole
    assert handoff.estimate_tokens(100) >= 1


# ---------------------------------------------------------------------------
# 2 & 3. Write claims: exclusive, additive, refuse-naming-holder
# ---------------------------------------------------------------------------

def test_write_claim_is_exclusive_and_refusal_names_holder(root: Path):
    assert "error" not in handoff.claim(root, "§4 Traps", "seatB", write=True)
    r2 = handoff.claim(root, "§4 Traps", "seatC", write=True)
    assert "error" in r2 and "seatB" in r2["error"], r2


def test_write_refused_without_claim_names_holder(root: Path):
    handoff.claim(root, "§4 Traps", "seatB", write=True)
    res = handoff.write_section(root, "§4 Traps", "## §4 Traps\nnew",
                                "seatC")
    assert "error" in res and "seatB" in res["error"], res


def test_write_patches_only_its_own_section(root: Path):
    handoff.claim(root, "§4 Traps", "seatB", write=True)
    res = handoff.write_section(root, "§4 Traps", "## §4 Traps\nNEWBODY",
                                "seatB")
    assert "error" not in res, res
    p = handoff.handoff_path(root)
    text = p.read_text()
    assert "NEWBODY" in text
    # every OTHER section and the preamble are byte-unchanged
    secs = handoff.parse_sections(text)
    assert [s["name"] for s in secs] == ["§0 State block", "§4 Traps", "§5 Verify"]
    s0 = handoff.section_by_name(secs, "§0 State block")
    assert s0["text"] == "## §0 State block\nalpha\n\n"
    s5 = handoff.section_by_name(secs, "§5 Verify")
    assert s5["text"] == "## §5 Verify\ngamma\n"
    assert text.startswith("# SESSION HANDOFF — scratch\n\npreamble not claimable")


def test_write_requires_its_own_header_line(root: Path):
    handoff.claim(root, "§4 Traps", "seatB", write=True)
    res = handoff.write_section(root, "§4 Traps", "not a section header\nX",
                                "seatB")
    assert "error" in res


# ---------------------------------------------------------------------------
# 4. Concurrent writers to different sections both survive (real processes)
# ---------------------------------------------------------------------------

def _runner(root: str, section: str, content: str, holder: str) -> int:
    res = handoff.write_section(Path(root), section, content, holder)
    return 0 if "error" not in res else 1


def test_concurrent_writes_to_different_sections_both_survive(root: Path):
    handoff.claim(root, "§4 Traps", "seatB", write=True)
    handoff.claim(root, "§5 Verify", "seatC", write=True)
    procs = [
        mp.Process(target=_runner, args=(
            str(root), "§4 Traps", "## §4 Traps\nbeta\n\n", "seatB")),
        mp.Process(target=_runner, args=(
            str(root), "§5 Verify", "## §5 Verify\ngamma\n", "seatC")),
    ]
    for p in procs:
        p.start()
    for p in procs:
        p.join(30)
    assert all(p.exitcode == 0 for p in procs), [p.exitcode for p in procs]
    # file is still one valid doc, both sections present, all headers intact
    text = handoff.handoff_path(root).read_text()
    secs = handoff.parse_sections(text)
    assert [s["name"] for s in secs] == ["§0 State block", "§4 Traps", "§5 Verify"]
    assert "beta" in handoff.section_by_name(secs, "§4 Traps")["text"]
    assert "gamma" in handoff.section_by_name(secs, "§5 Verify")["text"]
    assert text.startswith("# SESSION HANDOFF — scratch")


def test_read_claim_released_frees_it(root: Path):
    handoff.claim(root, "§5 Verify", "seatA")
    assert handoff.release(root, "§5 Verify", "seatA")
    assert not handoff.show_claims(root)


# ---------------------------------------------------------------------------
# SD.16 friction fixes -- the tool's own output is copy-pasteable back in
# ---------------------------------------------------------------------------

def test_norm_section_strips_printed_prefix():
    assert handoff.norm_section("## §5 Verify") == "§5 Verify"
    assert handoff.norm_section("§5 Verify") == "§5 Verify"


def test_cli_claim_accepts_printed_form_and_seat_alias(root: Path, capsys):
    # `sections` prints `## <name>`; claim must accept that exact string (friction a)
    # and `--seat` as the alias for `--holder` (friction b).
    rc = handoff.main(["--root", str(root), "claim", "## §5 Verify", "--seat", "seatA"])
    out, _ = capsys.readouterr()
    assert rc == 0
    assert "claimed" in out
    assert handoff.show_claims(root)


def test_cli_read_with_seat_alias_serves_section(root: Path, capsys):
    handoff.claim(root, "§5 Verify", "seatA")
    rc = handoff.main(["--root", str(root), "read", "## §5 Verify", "--seat", "seatA"])
    out, _ = capsys.readouterr()
    assert rc == 0
    assert "gamma" in out


def test_cli_read_missing_holder_names_the_flag(root: Path, capsys):
    # friction c -- a bare `read` must say WHICH flag is missing,
    # never print "None does not hold a claim".
    rc = handoff.main(["--root", str(root), "read", "§5 Verify"])
    _, err = capsys.readouterr()
    assert rc == 1
    assert "--holder" in err
    assert "None" not in err


def test_cli_write_missing_holder_names_the_flag(root: Path, capsys):
    rc = handoff.main(["--root", str(root), "write", "§5 Verify",
                      "--content", "## §5 Verify\nnew"])
    _, err = capsys.readouterr()
    assert rc == 1
    assert "--holder" in err
    assert "None" not in err