"""hypothesis:parents-and-kids-are-told-their-skills-in-the-agent-prompt.

`extensions/agi/lib/agent-prompt.md` is the ONE skill_prompt every adapter
appends, on claude-code and on pi alike. A pi parent or kid has no Skill
tool, so the prompt itself is the only place that can name the SKILL.md to
read. The test pins that the section exists, that BOTH tiers are named, that
every named path really exists under `skills/`, and that the section stays
short enough to read.
"""
from __future__ import annotations

import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
PROMPT = REPO / "extensions" / "agi" / "lib" / "agent-prompt.md"

SECTION_RE = re.compile(
    r"^## Your skills.*?$(.*?)(?=^## )", re.MULTILINE | re.DOTALL
)
PATH_RE = re.compile(r"`(skills/[^`]+/SKILL\.md)`")

#: The sets judged in the node's THOUGHT block. Seat flows (agi-corrective,
#: agi-rotate, agi-goal, agi-merge-pass, agi-workflow) are deliberately out.
EXPECTED: dict[str, set[str]] = {
    "parent": {
        "skills/agi-dispatch/SKILL.md",
        "skills/agi-node-write/SKILL.md",
        "skills/agi-send/SKILL.md",
        "skills/agi-verify/SKILL.md",
    },
    "kid": {"skills/agi-node-write/SKILL.md", "skills/agi-verify/SKILL.md"},
}


def _section() -> str:
    text = PROMPT.read_text(encoding="utf-8")
    m = SECTION_RE.search(text)
    assert m, "agent-prompt.md has no '## Your skills' section"
    return m.group(0)


def _tier_paths(section: str, tier: str) -> set[str]:
    row = next(
        (ln for ln in section.splitlines() if ln.startswith(f"| **{tier}**")),
        None,
    )
    assert row, f"no table row for tier {tier!r}"
    return set(PATH_RE.findall(row))


def test_both_tiers_are_named_with_the_judged_skill_sets() -> None:
    section = _section()
    for tier, expected in EXPECTED.items():
        assert _tier_paths(section, tier) == expected, tier


def test_every_named_skill_path_exists() -> None:
    for path in PATH_RE.findall(_section()):
        assert (REPO / path).is_file(), f"named path does not exist: {path}"


def test_section_stays_short_and_names_paths_not_rules() -> None:
    section = _section()
    lines = [ln for ln in section.splitlines() if ln.strip()]
    assert len(lines) <= 12, f"skills section is {len(lines)} lines, cap is 12"
    # A path table, not a copy of a skill: no fenced body, no heading inside.
    assert "```" not in section
    body = "\n".join(section.splitlines()[1:])
    assert not re.search(r"^#{1,6} ", body, re.MULTILINE)
