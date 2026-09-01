#!/usr/bin/env python3
"""evidence_gate.py — the orphan-verdict gate (TODO.md H4, H4c).

99.7% of verdicts in the agi-tree run were orphaned: `proved`/`disproved`
written with no backing experiment evidence. The loop self-flagged it
(commit 67ead2f0) but the gate was never put in the writer path — it has
been enforced by hand by the parent at review time
(`skills/agi/SKILL.md`, "Iteration protocol" step 4).

This module is that gate, as code. Both writer paths import it:
`bin/cli.py done` and `bin/post_wire.py`. `bin/metrics.py` imports
`normalize_evidence_runs` and `build_corpus` from here too, so the gate and
the `evidence_fraction` metric can never drift apart (G3, H4c item 4).

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

H4c — evidence_runs must resolve (goal:g3.1)
---------------------------------------------
`evidence_runs` used to be trusted at face value: `len(["synthetic"])` is 1,
so the literal sentinel string satisfied `evidence_runs >= 1` and the gate
passed a `proved` verdict that ran nothing. Fixed here in two parts:

1. **Resolution.** A list entry only counts if it is shaped like a node id
   (`type:slug`) *and* names an id that actually exists in the corpus
   (`build_corpus`). An unresolvable-but-id-shaped entry (a typo, a
   deleted node) counts 0 — silently, same as having no evidence at all.
2. **Taxonomy.** An entry that is not even shaped like a node id (a bare
   word like `synthetic`, a stray dict, a non-string) is a *taxonomy
   violation* — the same class of defect as a malformed verdict
   (`VERDICT_RE`), not a quieter one. For a verdict that actually requires
   evidence, `apply_gate` reports this as `rejected`, not `demoted`:
   writing a sentinel is an active claim of evidence that doesn't exist,
   which is worse than honestly having none. The caller (`cli.py done`)
   turns `rejected` into the same hard failure (exit 2) it already uses
   for a malformed verdict — nothing is written. `pending` and
   `inconclusive_lean_*` never reach this check (see `requires_evidence`),
   so the honest-uncertainty path is untouched.

Resolution needs a corpus (the set of real node ids) to check against.
`normalize_evidence_runs(value, corpus=...)` takes it as an explicit,
optional parameter. **`corpus=None` means every list-shaped value counts
0** — a gate that cannot resolve must not silently trust a length again.
Only `int` / `bool` / numeric-string forms (a direct number, not a
reference) are unaffected by the corpus, because they were never the
vector the sentinel-string defect used.
"""
from __future__ import annotations

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

#: `100|\d{1,2}` and not `\d{1,3}`. The loose form accepted `:999` while every
#: document describing it — VERDICT_HELP below, `zoom.py`'s contract,
#: `agent-prompt.md`, and `task:t-054-verdict-taxonomy-state-validation` —
#: said 0-100. That task node's own Test Strategy reads "reject
#: `inconclusive_lean_proved:101`", so the graph had specified this and the
#: regex had never implemented it. Tightened 2026-09-01 after confirming no
#: live node carries an out-of-range lean: the only `:101` in the corpus is
#: inside that task's prose, as the example of what must be rejected.
VERDICT_RE = re.compile(
    r"^(proved|disproved|inconclusive_lean_proved:(?:100|\d{1,2})"
    r"|inconclusive_lean_disproved:(?:100|\d{1,2})|pending)$"
)

#: `N` is spelled out because it was not, and a kid paid for it. On the
#: 2026-08-31 live run one wrote `inconclusive_lean_proved:0.6` — a reasonable
#: reading of a bare `:N` next to a `--confidence 0.0-1.0` flag — was rejected,
#: and fell back to `pending`, losing the lean it had actually formed. Spelling
#: out the range in the help was half the fix; the other half was making the
#: regex agree with it.
VERDICT_HELP = (
    "proved | disproved | inconclusive_lean_proved:N | "
    "inconclusive_lean_disproved:N | pending "
    "(N = integer percent 0-100, e.g. inconclusive_lean_proved:60 — "
    "NOT a 0..1 fraction; that is what --confidence takes)"
)

#: Shape of a legitimate `evidence_runs` entry: `type:slug`, no whitespace.
#: Purely syntactic — matching this says nothing about whether the id
#: actually exists in the corpus (see `build_corpus` / `normalize_evidence_runs`
#: for that). A string that does *not* match is a taxonomy violation, the
#: same class of defect as a verdict that fails `VERDICT_RE`.
NODE_ID_RE = re.compile(r"^[A-Za-z][\w.-]*:\S+$")

#: Verdicts that assert a decided outcome and therefore require evidence.
DECISIVE_VERDICTS = ("proved", "disproved")

#: What a decisive-but-unevidenced verdict becomes. 50 = "no lean either way
#: is dishonest; the claim was made, but nothing backs it".
DEMOTION = {
    "proved": "inconclusive_lean_proved:50",
    "disproved": "inconclusive_lean_disproved:50",
}

#: Frontmatter fields that shadow `verdict:` — a second place the same claim
#: can be written, which the gate must demote in lockstep or the node keeps
#: advertising the overclaim it just lost.
#:
#: `status` is the only one. It is a **legacy shadow**, not a declared field:
#: no chain-node schema declares it (`context/schemas/[verdict].md` does not
#: exist, and t-031 — the task that would ship it — names `state`, not
#: `status`), no engine writer path produces it (`cli.py done` writes
#: `status` into the *agent record* under `sessions/`, never into node
#: frontmatter), and no engine reader interprets it as a verdict. It was
#: hand-written by kids alongside `verdict:` and then left behind when the
#: gate rewrote only `verdict:`.
#:
#: `tags` is deliberately NOT in this list. A `proved` tag on a demoted node
#: is kept as a historical record of what was originally claimed; demotion
#: already keeps such nodes out of the standard graph views.
SHADOW_VERDICT_FIELDS = ("status",)


def is_valid_verdict(verdict: str | None) -> bool:
    return bool(verdict) and bool(VERDICT_RE.match(verdict))


def requires_evidence(verdict: str | None) -> bool:
    """True iff this verdict asserts a decided outcome."""
    return verdict in DECISIVE_VERDICTS


def is_decisive_shadow(value) -> bool:
    """True iff `value` is a shadow field asserting a decided outcome.

    Deliberately narrow: **only the two decisive words**, never the
    `inconclusive_lean_*` or `pending` forms. That is what keeps this safe to
    run against a `status:` field whose meaning is per-type — `task` uses
    `pending|in_progress|done`, `idea` uses `open|extended|abandoned`, `goal`
    uses the four-state lifecycle, and *none* of those domains contains
    `proved` or `disproved`. So a shadow rewrite can only ever land on a node
    that really was making a verdict claim, and a task's lifecycle `status`
    can never be clobbered by the verdict gate.
    """
    return isinstance(value, str) and value.strip() in DECISIVE_VERDICTS


def shadow_verdict_fields(fm: dict) -> list[str]:
    """Names of shadow fields in `fm` that assert a decided outcome.

    The read-only counterpart of the rewrite in `stamp` — `metrics.py` uses
    it to count nodes whose `verdict:` is honest but whose shadow still
    advertises `proved`, so the gate and the defect metric share one
    definition of "shadow" (G3, same reason `build_corpus` is shared).
    """
    if not isinstance(fm, dict):
        return []
    return [f for f in SHADOW_VERDICT_FIELDS if is_decisive_shadow(fm.get(f))]


def is_node_id_shaped(value) -> bool:
    """Pure syntactic check: does `value` look like a `type:slug` node id?

    Says nothing about whether the id resolves to a real node — that needs
    a corpus (`build_corpus`). Mirrors `is_valid_verdict`'s role for
    `VERDICT_RE`: a taxonomy check independent of context.
    """
    return isinstance(value, str) and bool(NODE_ID_RE.match(value.strip()))


def evidence_runs_violations(value) -> list:
    """Entries in an `evidence_runs` list that are not node-id-shaped.

    This is the taxonomy check (H4c item 2): a bare word like `synthetic`,
    a stray dict, a bare int inside the list — anything that isn't even
    trying to name a node. Distinct from, and checked before, resolution:
    an id-*shaped* entry that simply doesn't exist in the corpus is not a
    violation, it just doesn't count (see `normalize_evidence_runs`).

    Non-list values (int, bool, numeric string, None) have no entries to
    check and always return `[]` — they are not the vector this defect
    used.
    """
    if isinstance(value, (list, tuple, set)):
        return [v for v in value if not is_node_id_shaped(v)]
    return []


def build_corpus(nodes_dir) -> frozenset:
    """The set of real node ids under `nodes_dir` — what `evidence_runs`
    entries are allowed to resolve against (goal:g3.1).

    A plain frontmatter scan (own `id:` field only), independent of
    `graph_core`, so both writer paths can build it cheaply without
    loading the full graph. `metrics.py` calls this exact function too —
    one definition, so the gate and the metric cannot drift apart (G3).
    """
    import yaml

    ids: set[str] = set()
    p = Path(nodes_dir)
    if not p.is_dir():
        return frozenset(ids)
    for nf in sorted(p.rglob("*.md")):
        try:
            text = nf.read_text(encoding="utf-8")
        except Exception:
            continue
        if not text.startswith("---"):
            continue
        parts = text.split("---", 2)
        if len(parts) < 3:
            continue
        try:
            fm = yaml.safe_load(parts[1]) or {}
        except Exception:
            continue
        if not isinstance(fm, dict):
            continue
        nid = fm.get("id")
        if isinstance(nid, str) and nid.strip():
            ids.add(nid.strip())
    return frozenset(ids)


def normalize_evidence_runs(value, corpus=None, self_id=None,
                            allow_self: bool = False) -> int:
    """Coerce an `evidence_runs` frontmatter value to a count of entries
    that actually resolve to a real node (goal:g3.1 / TODO.md H4c).

    - `None` -> 0
    - `bool` -> 0                          (goal:g7.3 — unverifiable)
    - `int` -> 0                           (goal:g7.3 — unverifiable)
    - numeric string -> 0                  (goal:g7.3 — unverifiable)
    - `list`/`tuple`/`set` -> count of entries that are node-id-shaped
      *and* present in `corpus`. A sentinel like `"synthetic"` counts 0
      (it isn't even id-shaped); a dangling `"exp:deleted-thing"` counts 0
      (id-shaped, but not in the corpus).
    - anything else -> 0

    `corpus` is the set of real node ids (see `build_corpus`). **If
    `corpus` is `None`, no list entry can be verified, so every
    list-shaped value counts 0** — a gate that cannot resolve must not
    silently trust a length again. This is a deliberate fail-closed
    default, not an oversight: callers that want list entries to count
    must supply a corpus.

    **goal:g7.3, closed 2026-08-27: a bare integer no longer counts.**
    H4c removed the `"synthetic"` sentinel because a value nothing could
    check was worth nothing; `evidence_runs: 3` was left accepted as
    "direct attestation" and is *exactly as cheap to write*. It is the same
    hole with a different literal, and it was populated rather than
    theoretical: 77 of 112 nodes carrying the field held a bare int against
    a schema declaring a list, and `verdict:zoom-encoded-node-ids` was
    `proved` — decisive — solely because this function returned an
    unchecked `1`.

    The honest-count path G7.3 worried about breaking is preserved, just not
    here: an unverifiable count is still *reported* (see
    `is_unverifiable_attestation`), it simply no longer buys a decisive
    verdict. "I ran it three times" stays sayable; it stops being
    self-certifying.
    """
    if value is None:
        return 0
    if isinstance(value, (bool, int)):
        return 0
    if isinstance(value, (list, tuple, set)):
        if corpus is None:
            return 0
        return sum(
            1 for v in value
            if is_node_id_shaped(v)
            and v.strip() in corpus
            and not _is_self_citation(v, self_id, allow_self)
        )
    if isinstance(value, str):
        return 0
    return 0


def _is_self_citation(value, self_id, allow_self: bool) -> bool:
    """A node naming itself as its own backing run.

    goal:g7.3 closed `evidence_runs: 3` because a count nothing could check
    certified nothing and was "exactly as cheap to write". `evidence_runs:
    [<my own id>]` is exactly as cheap, resolves against the corpus because the
    node exists, and buys a decisive verdict. Same hole, one substitution
    later. It fired unprompted on 2026-09-01, on the first kid that reached for
    `proved`.

    **An `experiment` may cite itself and a `verdict` may not**, and the
    asymmetry is not a nicety: an experiment node IS the run, so naming itself
    is the honest reference. A verdict's job is to judge experiments, so a
    verdict citing itself is a claim with nothing behind it. That is the rule
    the kid contract states in words; this is where it becomes mechanical.

    `self_id=None` disables the check, so every existing caller and every
    historical node behaves exactly as before.
    """
    if allow_self or not self_id:
        return False
    return str(value).strip() == str(self_id).strip()


def is_unverifiable_attestation(value) -> bool:
    """True when `evidence_runs` claims a count nothing can resolve.

    Split out from `normalize_evidence_runs` so the information is not simply
    destroyed by goal:g7.3's fix. The count stops *certifying* a verdict; it
    stays *visible*, which is what lets `metrics.py` report how much of the
    corpus still needs converting to real references instead of the number
    silently reading as zero evidence.
    """
    if isinstance(value, bool):
        return True
    if isinstance(value, int):
        return value > 0
    if isinstance(value, str):
        return value.strip().isdigit() and int(value.strip()) > 0
    return False


@dataclass
class GateResult:
    verdict: str                 # verdict to actually write
    original: str                # verdict as requested
    evidence_runs: int
    demoted: bool = False
    bypassed: bool = False
    rejected: bool = False       # taxonomy violation on a verdict that needs evidence
    taxonomy_violations: list = field(default_factory=list)
    reason: str = ""
    messages: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """True when the requested verdict survived the gate unchanged."""
        return not self.demoted and not self.rejected


def apply_gate(
    verdict: str, evidence_runs, *, bypass: bool = False, corpus=None,
    self_id=None, node_type=None
) -> GateResult:
    """Apply the evidence gate to a requested verdict.

    Returns a :class:`GateResult` whose ``verdict`` is what should be
    written. `corpus` is the set of real node ids (`build_corpus`) that
    `evidence_runs` entries are resolved against — pass `None` only when
    no corpus is available, which makes every list-shaped `evidence_runs`
    count 0 (fail closed, see `normalize_evidence_runs`).

    Two distinct failure modes, deliberately not merged:
    - **Demoted** (existing H4 behaviour): a syntactically clean
      `evidence_runs` that just doesn't resolve to >=1 real run. The verdict
      is downgraded to an honest `inconclusive_lean_*:50`; the node is kept.
    - **Rejected** (new, H4c): `evidence_runs` contains a taxonomy
      violation — a value that isn't even shaped like a node id (e.g. the
      `synthetic` sentinel). Writing that is an active false claim, not an
      absence of evidence, so it is treated like a malformed verdict:
      nothing is written. Callers surface this as a hard failure.
      Bypassed and non-decisive (`pending` / `inconclusive_lean_*`)
      verdicts never reach this branch.

    Never raises. The caller decides what "rejected" means for its own
    exit behaviour (`cli.py done` turns it into exit 2, matching the
    existing malformed-verdict convention).
    """
    # An `experiment` IS its own run, so it may cite itself; every other
    # type must cite something else. `self_id=None` keeps the old behaviour.
    runs = normalize_evidence_runs(
        evidence_runs, corpus=corpus, self_id=self_id,
        allow_self=(str(node_type or '').strip() == 'experiment'),
    )
    violations = evidence_runs_violations(evidence_runs)
    res = GateResult(
        verdict=verdict, original=verdict, evidence_runs=runs,
        taxonomy_violations=violations,
    )

    if not requires_evidence(verdict):
        return res

    if violations and not bypass:
        res.rejected = True
        res.reason = (
            f"evidence_runs contains non-id value(s) {violations!r} — a "
            "taxonomy violation (TODO.md H4c), not evidence"
        )
        res.messages.append(
            f"EVIDENCE-GATE REJECTED: '{verdict}' requires evidence_runs to "
            f"name real experiment ids; {violations!r} is not a node id and "
            "cannot be resolved. This is a taxonomy violation, not an "
            "absence of evidence — cite a real experiment id, drop the bad "
            "entry, or write an honest inconclusive_lean_* instead. "
            "(--no-evidence-gate bypasses this for historical backfills.)"
        )
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
    if res.rejected:
        print(f"EVIDENCE-GATE REJECTED {res.original} "
              f"taxonomy_violations={res.taxonomy_violations}")
    elif res.demoted:
        print(f"EVIDENCE-GATE DEMOTED {res.original} -> {res.verdict} "
              f"evidence_runs={res.evidence_runs}")
    elif res.bypassed:
        print(f"EVIDENCE-GATE BYPASSED {res.original} evidence_runs={res.evidence_runs}")


def stamp(fm: dict, res: GateResult) -> dict:
    """Record the gate's decision in a node's frontmatter dict.

    Never call this with a `rejected` result — rejection means nothing
    should be written at all (the caller must stop before this point,
    same as it does for a malformed verdict).

    On a demotion, every shadow field (`SHADOW_VERDICT_FIELDS`) that still
    reads `proved`/`disproved` is rewritten to the demoted verdict verbatim.
    The invariant this buys: **after a demotion no frontmatter field of the
    node reads `proved` or `disproved`.** Rewriting only the `verdict:` field
    left `status: proved` standing beside `verdict: inconclusive_lean_proved:50`
    on 42 nodes, a contradiction `benchmark.py` then fed to the LLM judge as
    two adjacent lines.
    """
    if res.demoted:
        fm["verdict"] = res.verdict
        for fld in SHADOW_VERDICT_FIELDS:
            if is_decisive_shadow(fm.get(fld)):
                fm[fld] = res.verdict
        fm["demoted_from"] = res.original
        fm["demote_reason"] = res.reason
    elif res.bypassed:
        fm["evidence_gate"] = "bypassed"
    fm["evidence_runs"] = res.evidence_runs
    return fm
