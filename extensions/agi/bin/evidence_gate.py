#!/usr/bin/env python3
"""evidence_gate.py — the orphan-verdict gate (TODO.md H4).

99.7% of verdicts in the agi-tree run were orphaned: `proved`/`disproved`
written with no backing experiment evidence. The loop self-flagged it
(commit 67ead2f0) but the gate was never put in the writer path — it has
been enforced by hand by the parent at review time
(`skills/agi/SKILL.md`, "Iteration protocol" step 4).

This module is that gate, as code. Both writer paths import it:
`bin/cli.py done` and `bin/post_wire.py`.

Rule
----
`proved` / `disproved` require `evidence_runs >= 1`.
`pending` and `inconclusive_lean_*` are permitted with no evidence —
those states exist precisely to record honest uncertainty.

Behaviour on violation: **demote, do not discard.** A kid that did real
research and mislabelled its verdict should keep its node; only the
overclaim is removed. The demotion is loud (stderr + stdout) and is
stamped into the node frontmatter (`demoted_from`, `demote_reason`) so a
reviewer can find and reverse it.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field

VERDICT_RE = re.compile(
    r"^(proved|disproved|inconclusive_lean_proved:\d{1,3}"
    r"|inconclusive_lean_disproved:\d{1,3}|pending)$"
)

VERDICT_HELP = (
    "proved | disproved | inconclusive_lean_proved:N | "
    "inconclusive_lean_disproved:N | pending"
)

#: Verdicts that assert a decided outcome and therefore require evidence.
DECISIVE_VERDICTS = ("proved", "disproved")

#: What a decisive-but-unevidenced verdict becomes. 50 = "no lean either way
#: is dishonest; the claim was made, but nothing backs it".
DEMOTION = {
    "proved": "inconclusive_lean_proved:50",
    "disproved": "inconclusive_lean_disproved:50",
}


def is_valid_verdict(verdict: str | None) -> bool:
    return bool(verdict) and bool(VERDICT_RE.match(verdict))


def requires_evidence(verdict: str | None) -> bool:
    """True iff this verdict asserts a decided outcome."""
    return verdict in DECISIVE_VERDICTS


def normalize_evidence_runs(value) -> int:
    """Coerce an `evidence_runs` frontmatter value to a count.

    Accepts a list (its length), an int, a numeric string, or None.
    Anything unrecognised counts as 0 — the gate fails closed.
    """
    if value is None:
        return 0
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, int):
        return max(value, 0)
    if isinstance(value, (list, tuple, set)):
        return len(value)
    if isinstance(value, str):
        s = value.strip()
        if s.isdigit():
            return int(s)
        return 0
    return 0


@dataclass
class GateResult:
    verdict: str                 # verdict to actually write
    original: str                # verdict as requested
    evidence_runs: int
    demoted: bool = False
    bypassed: bool = False
    reason: str = ""
    messages: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """True when the requested verdict survived the gate unchanged."""
        return not self.demoted


def apply_gate(verdict: str, evidence_runs, *, bypass: bool = False) -> GateResult:
    """Apply the evidence gate to a requested verdict.

    Returns a :class:`GateResult` whose ``verdict`` is what should be
    written. Never raises for a policy violation — it demotes, so the
    research work behind the node is preserved.
    """
    runs = normalize_evidence_runs(evidence_runs)
    res = GateResult(verdict=verdict, original=verdict, evidence_runs=runs)

    if not requires_evidence(verdict):
        return res

    if runs >= 1:
        return res

    if bypass:
        res.bypassed = True
        res.reason = "evidence gate bypassed via --no-evidence-gate"
        res.messages.append(
            f"EVIDENCE-GATE BYPASSED: '{verdict}' written with evidence_runs=0. "
            "This verdict is unbacked; a reviewer must supply the evidence or "
            "demote it by hand."
        )
        return res

    res.verdict = DEMOTION[verdict]
    res.demoted = True
    res.reason = f"no experiment evidence (evidence_runs={runs}) for '{verdict}'"
    res.messages.append(
        f"EVIDENCE-GATE DEMOTED: '{verdict}' -> '{res.verdict}' "
        f"(evidence_runs={runs}). Decisive verdicts require evidence_runs >= 1 "
        "(TODO.md H4). The node is kept; only the overclaim is removed. "
        "Re-run with --evidence-runs N once the experiment evidence is linked."
    )
    return res


def announce(res: GateResult, stream=None) -> None:
    """Print gate messages loudly. No-op when nothing happened.

    Full explanation to stderr, a one-line grep-able marker to stdout (the
    driver tees stdout into loop.log).
    """
    stream = stream if stream is not None else sys.stderr
    for m in res.messages:
        print(f"!! {m}", file=stream)
    if res.demoted:
        print(f"EVIDENCE-GATE DEMOTED {res.original} -> {res.verdict} "
              f"evidence_runs={res.evidence_runs}")
    elif res.bypassed:
        print(f"EVIDENCE-GATE BYPASSED {res.original} evidence_runs={res.evidence_runs}")


def stamp(fm: dict, res: GateResult) -> dict:
    """Record the gate's decision in a node's frontmatter dict."""
    if res.demoted:
        fm["verdict"] = res.verdict
        fm["demoted_from"] = res.original
        fm["demote_reason"] = res.reason
    elif res.bypassed:
        fm["evidence_gate"] = "bypassed"
    fm["evidence_runs"] = res.evidence_runs
    return fm
