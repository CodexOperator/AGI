"""rolslice.py — a SKILL.md heading rename must not drop a role section
(hypothesis:rolslice-role-sections-survive-a-heading-rename).

The Prime's goal-id sweeps rewrite the trailing `(goal:gNN)` in a SKILL.md
heading. The role->section map must resolve through a stable key that does not
carry that id, so a rename cannot make `build_slice` raise "section(s) not
found". This test builds a SMALL fixture SKILL.md from the map itself, renames
the parenthesised id in every heading, and asserts the slice still carries the
section.

RED on the pre-fix bytes: `ROLE_SECTIONS` held the full literal
`... (`goal:g13.1`)` while SKILL.md:272 already read `(`goal:g4.19`)`, so the
fixture's renamed id could not match it and `build_slice` raised ValueError.
"""
import re
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))

import rolslice  # noqa: E402

ROOT = Path(__file__).resolve().parents[1] / "agi"  # graph root for this repo
if not ROOT.joinpath("nodes", ".geometry", "seats.md").is_file():
    cand = Path(__file__).resolve().parents[3] / ".agi"
    if cand.joinpath("nodes", ".geometry", "seats.md").is_file():
        ROOT = cand

_ID_RE = re.compile(r"\s*\(`?goal:[^)`]+`?\)\s*$")


def _fixture(bucket: str, renamed_id: str) -> str:
    """A tiny SKILL.md carrying every section the bucket needs, with a renamed id."""
    want = list(rolslice.CORE) + list(rolslice.ROLE_SECTIONS.get(bucket, set()))
    lines = ["# fixture SKILL.md", ""]
    for key in want:
        base = _ID_RE.sub("", key)
        lines.append(f"## {base} (`goal:{renamed_id}`)")
        lines.append(f"body-marker::{base}")
        lines.append("")
    return "\n".join(lines)


@pytest.mark.parametrize("bucket,marker", [
    ("kid", "Every node edit goes through `write.py`"),
    ("parent", "Every node edit goes through `write.py`"),
    ("director", "`COMPLETE.md` — every finished loop writes one"),
])
def test_goal_id_rename_keeps_section(tmp_path, bucket, marker):
    skill = tmp_path / "SKILL.md"
    skill.write_text(_fixture(bucket, "g4.19"), encoding="utf-8")
    s = rolslice.build_slice(ROOT, skill, bucket)  # must NOT raise
    assert marker in s, f"{bucket} slice lost section after id rename: {marker}"


def test_genuinely_missing_section_still_fails_loud(tmp_path):
    """The loud ValueError stays: a heading that is really gone must still fail."""
    text = _fixture("kid", "g4.19").replace(
        "## Every node edit goes through `write.py` (`goal:g4.19`)", "## Gone")
    skill = tmp_path / "SKILL.md"
    skill.write_text(text, encoding="utf-8")
    with pytest.raises(ValueError):
        rolslice.build_slice(ROOT, skill, "kid")