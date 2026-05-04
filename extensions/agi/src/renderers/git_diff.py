"""Git-diff renderer (T-065 / renderers R5).

Compares two experiment runs (by id) on the same chain, emitting a unified-style
diff over their frontmatter fields.

Acceptance criteria (R5):
- R5.1: rejects mismatched-chain pairs with a structured error
- R5.2: added/removed/changed fields show conventional ``+``/``-``/``~`` markers
- R5.3: identical runs → single-line "no differences" note (NOT empty string)
- R5.4: only printable ASCII characters in output
"""

from __future__ import annotations

from typing import Any, Callable, Optional


class MismatchedRunsError(Exception):
    """Raised when two runs do not belong to the same chain (R5.1)."""

    def __init__(self, run_a: str, run_b: str, reason: str = "different chains") -> None:
        self.run_a = run_a
        self.run_b = run_b
        self.reason = reason
        super().__init__(f"runs '{run_a}' and '{run_b}' do not belong to the same chain: {reason}")


# Type aliases
RunData = dict[str, Any]
ChainLookup = Callable[[str], Optional[str]]  # run_id -> chain_id (None = unknown)


def render_git_diff(
    run_a_id: str,
    run_a_data: RunData,
    run_b_id: str,
    run_b_data: RunData,
    chain_lookup: Optional[ChainLookup] = None,
) -> str:
    """Render a unified-style diff between two runs.

    ``chain_lookup`` returns the chain id for a given run id. If both run ids
    map to the same (non-None) chain id, the diff proceeds. If either is None
    or they differ, raises :class:`MismatchedRunsError` (R5.1).

    When ``chain_lookup`` is None, the validator is permissive (accepts any
    pair) — useful while chain-engine is not yet wired up.
    """
    if chain_lookup is not None:
        ca = chain_lookup(run_a_id)
        cb = chain_lookup(run_b_id)
        if ca is None or cb is None:
            raise MismatchedRunsError(
                run_a_id, run_b_id, reason="one or both runs not on a known chain"
            )
        if ca != cb:
            raise MismatchedRunsError(
                run_a_id, run_b_id, reason=f"chain '{ca}' vs '{cb}'"
            )

    if run_a_data == run_b_data:
        return _ascii_only(f"# diff {run_a_id} -> {run_b_id}\nno differences\n")

    a_keys = set(run_a_data.keys())
    b_keys = set(run_b_data.keys())
    added = sorted(b_keys - a_keys)
    removed = sorted(a_keys - b_keys)
    common = sorted(a_keys & b_keys)

    lines: list[str] = [f"# diff {run_a_id} -> {run_b_id}"]
    for k in removed:
        lines.append(f"- {k}: {_fmt_val(run_a_data[k])}")
    for k in added:
        lines.append(f"+ {k}: {_fmt_val(run_b_data[k])}")
    for k in common:
        if run_a_data[k] != run_b_data[k]:
            lines.append(f"~ {k}: {_fmt_val(run_a_data[k])} -> {_fmt_val(run_b_data[k])}")

    return _ascii_only("\n".join(lines) + "\n")


def _fmt_val(v: Any) -> str:
    s = repr(v)
    if len(s) > 80:
        s = s[:77] + "..."
    return s


def _ascii_only(s: str) -> str:
    """Strip non-printable / non-ASCII chars (R5.4)."""
    out_chars = []
    for ch in s:
        if ch == "\n" or ch == "\t" or (32 <= ord(ch) < 127):
            out_chars.append(ch)
        else:
            out_chars.append("?")
    return "".join(out_chars)
