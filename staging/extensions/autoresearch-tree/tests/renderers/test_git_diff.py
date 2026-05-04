"""T-065 tests: Git-diff renderer (renderers/R5)."""

import string

import pytest

from renderers import render_git_diff
from renderers.git_diff import MismatchedRunsError


def test_diff_added_removed_changed_markers() -> None:
    """R5.2: added/removed/changed fields use +/-/~ markers."""
    a = {"x": 1, "y": "old"}
    b = {"y": "new", "z": 3}
    out = render_git_diff("run-a", a, "run-b", b)
    assert "- x:" in out
    assert "+ z:" in out
    assert "~ y:" in out


def test_identical_runs_yield_single_note() -> None:
    """R5.3: identical runs emit a one-line note (NOT blank)."""
    a = {"x": 1, "y": 2}
    out = render_git_diff("r1", a, "r2", a)
    assert "no differences" in out
    assert out.strip() != ""
    # NOT blank string
    assert len(out.strip()) > 0


def test_chain_mismatch_raises() -> None:
    """R5.1: when chain_lookup says different chains, raise structured error."""

    def lookup(rid: str) -> str:
        return {"r1": "chain-A", "r2": "chain-B"}[rid]

    with pytest.raises(MismatchedRunsError) as exc:
        render_git_diff("r1", {"x": 1}, "r2", {"x": 2}, chain_lookup=lookup)
    assert exc.value.run_a == "r1"
    assert exc.value.run_b == "r2"
    assert "chain" in str(exc.value).lower()


def test_chain_unknown_raises() -> None:
    """R5.1: if either run is not on any known chain, raise."""

    def lookup(rid: str):
        return None

    with pytest.raises(MismatchedRunsError):
        render_git_diff("r1", {"x": 1}, "r2", {"x": 2}, chain_lookup=lookup)


def test_chain_match_proceeds() -> None:
    """R5.1: same chain → diff proceeds (no exception)."""

    def lookup(rid: str) -> str:
        return "same-chain"

    out = render_git_diff(
        "r1", {"x": 1}, "r2", {"x": 2, "y": 3}, chain_lookup=lookup
    )
    assert "+ y:" in out or "~ x:" in out


def test_output_printable_ascii_only() -> None:
    """R5.4: only printable ASCII characters."""
    a = {"emoji_field": "hello ☃ snowman", "x": 1}
    b = {"emoji_field": "hello ☃ snowman replaced", "x": 2}
    out = render_git_diff("r1", a, "r2", b)
    allowed = set(string.printable) - {"\x0b", "\x0c"}
    for ch in out:
        assert ch in allowed, f"non-printable: {ch!r}"


def test_no_validator_is_permissive() -> None:
    """Without a chain_lookup, any pair is accepted (chain-engine not wired yet)."""
    a = {"x": 1}
    b = {"x": 2}
    out = render_git_diff("r1", a, "r2", b)
    assert "~ x:" in out
