"""rolslice.py — the per-role SKILL.md slice mechanism
(hypothesis:l3w4-context-load-minimal).

Assert the slice contract without pinning byte content (SKILL.md is director-
owned this iteration and may churn):
  * every CORE + role section is present in the slice (a heading rename that
    would silently drop content is caught);
  * an unknown role FAILS LOUDLY rather than guessing;
  * the must-not-lose markers (the ones that live IN SKILL.md) survive every
    role's slice, including the leanest (kid);
  * the hierarchy chart (the "how everyone plays their part" every role needs)
    is present in every slice.
"""
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
sys.path.insert(0, str(BIN))

import rolslice  # noqa: E402
import locations  # noqa: E402

# config:posts (.agi/nodes/.geometry/posts.md) is the instance registry
# hierarchy.py reads; resolve ROOT through the repo's own resolver so it is a
# real directory carrying the geometry, never the absent `extensions/agi/agi`.
ROOT = locations.find_project_root(Path(__file__).resolve())
if ROOT is None or not ROOT.joinpath("nodes", ".geometry", "posts.md").is_file():
    cand = Path(__file__).resolve().parents[3] / ".agi"
    if cand.joinpath("nodes", ".geometry", "posts.md").is_file():
        ROOT = cand
assert ROOT is not None and ROOT.joinpath(
    "nodes", ".geometry", "posts.md").is_file(), (
    f"rolslice test: no graph root carrying config:posts found (got {ROOT})")
SKILL = Path(__file__).resolve().parents[3] / "skills" / "agi" / "SKILL.md"


@pytest.fixture(scope="module")
def root():
    return ROOT


@pytest.fixture(scope="module")
def skill():
    assert SKILL.is_file(), f"SKILL.md not found: {SKILL}"
    return SKILL


def _slice(root, skill, role, tier=0):
    return rolslice.build_slice(root, skill, role, tier)


def test_core_sections_in_every_slice(root, skill):
    for role in ("kid", "parent", "director"):
        s = _slice(root, skill, role)
        for core in rolslice.CORE:
            assert core in s, f"{role} slice missing core section: {core}"


def test_unknown_role_fails_loud(root, skill):
    with pytest.raises(ValueError):
        _slice(root, skill, "this-role-does-not-exist")


def test_must_not_lose_markers_are_in_skill_slices(root, skill):
    """The safety content that lives IN SKILL.md survives the leanest slice."""
    s = _slice(root, skill, "kid")
    for marker in ("Never create", "grid.py checkout", "safety", "Prayer",
                   "kill", "node count"):
        assert marker.lower() in s.lower(), f"kid slice lost must-not-lose: {marker}"


def test_hierarchy_chart_in_every_slice(root, skill):
    for role in ("kid", "parent", "director"):
        s = _slice(root, skill, role)
        assert "COMMAND HIERARCHY" in s, f"{role} slice missing hierarchy chart"


def test_every_mapped_key_resolves_in_real_skill(skill):
    """The FORWARD direction the rolslice.py map comment states: every CORE and
    every ROLE_SECTIONS[bucket] key names a real `## ` heading in SKILL.md."""
    keys = set(rolslice.CORE)
    for bucket in ("kid", "parent", "director"):
        keys |= set(rolslice.ROLE_SECTIONS[bucket])
    headings = {rolslice.stable_key(h) for h in
                rolslice._split_sections(skill.read_text(encoding="utf-8"))}
    missing = sorted(keys - headings)
    assert not missing, f"mapped keys absent from real SKILL.md: {missing}"


def test_slice_is_strictly_smaller_than_full_skill(root, skill):
    full = skill.read_text(encoding="utf-8")
    for role in ("kid", "parent", "director"):
        s = _slice(root, skill, role)
        assert len(s) < len(full), \
            f"{role} slice not smaller than full SKILL.md (a non-trim is a bug)"