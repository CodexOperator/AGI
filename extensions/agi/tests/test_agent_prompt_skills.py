"""hypothesis:parents-and-kids-are-told-their-skills-in-the-agent-prompt. agent-prompt.md is the
ONE skill_prompt every adapter appends; pi has no Skill tool, so the prompt names the SKILL.md."""
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
PROMPT = REPO / "extensions" / "agi" / "lib" / "agent-prompt.md"
SECTION_RE = re.compile(r"^## Your skills.*?$(.*?)(?=^## )", re.MULTILINE | re.DOTALL)
PATH_RE = re.compile(r"`(skills/[^`]+/SKILL\.md)`")

#: The sets judged in the build node's THOUGHT; seat flows are out of every tier.
EXPECTED: dict[str, set[str]] = {
    "parent": {f"skills/agi-{n}/SKILL.md" for n in ("dispatch", "node-write", "send", "verify")},
    "kid": {f"skills/agi-{n}/SKILL.md" for n in ("node-write", "verify")},
}


def _section() -> str:
    m = SECTION_RE.search(PROMPT.read_text(encoding="utf-8"))
    assert m, "agent-prompt.md has no '## Your skills' section"
    return m.group(0)


def test_both_tiers_are_named_with_the_judged_skill_sets() -> None:
    rows = _section().splitlines()
    for tier, expected in EXPECTED.items():
        row = next((r for r in rows if r.startswith(f"| **{tier}**")), None)
        assert row, f"no table row for tier {tier!r}"
        assert set(PATH_RE.findall(row)) == expected, tier

def test_every_named_skill_path_exists() -> None:
    for path in PATH_RE.findall(_section()):
        assert (REPO / path).is_file(), f"named path does not exist: {path}"

def test_section_stays_short_and_names_paths_not_rules() -> None:
    section = _section()
    lines = section.splitlines()
    assert (n := len([ln for ln in lines if ln.strip()])) <= 12, f"{n} non-blank lines, cap 12"
    assert "```" not in section, "section carries a fenced body, not a path table"
    assert not re.search(r"^#{1,6} ", "\n".join(lines[1:]), re.MULTILINE), "nested heading"
