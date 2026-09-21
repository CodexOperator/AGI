---
id: exp:evidence-gate-resolution-r1
mint_id: 485ba78c63ed4a0fa185d77e39d86bd7
type: experiment
parents:
  - goal:g3.1
confidence: 0.8
edited_by: season.py
evidence_runs: 1
season: 1
tags:
  - integrity
  - g3.1
thought_session: season
title: "Evidence gate: resolve evidence_runs against the corpus"
---
**Defect (H4c).** `normalize_evidence_runs` returned `len(value)` for any
list, so `evidence_runs: [synthetic]` — the literal sentinel string —
satisfied `evidence_runs >= 1` and both the gate and `evidence_fraction`
agreed a `proved` verdict was evidence-backed when nothing had run.

## What changed

`extensions/agi/bin/evidence_gate.py`:

- `normalize_evidence_runs(value, corpus=None)` — new `corpus` parameter.
  For a `list`/`tuple`/`set`, an entry only counts if it is **node-id-shaped**
  (`type:slug`, checked by the new `is_node_id_shaped` / `NODE_ID_RE`) *and*
  present in `corpus`. `int` / `bool` / numeric-string forms are untouched —
  they're a direct attestation, not a reference, and were never the vector
  this defect used.
- **`corpus=None` makes every list-shaped value count 0.** Deliberate: a
  gate that cannot resolve must not silently trust a length again. All
  three call sites (`cli.py`, `post_wire.py`, `metrics.py`) now build a real
  corpus before calling this, so `corpus=None` is a defensive default, not
  a code path any shipped writer actually takes.
- `evidence_runs_violations(value)` — the *taxonomy* check, separate from
  resolution: entries that aren't even shaped like a node id (`"synthetic"`,
  a stray dict, a bare int inside the list). An id-shaped-but-nonexistent
  entry (a typo, a deleted node) is **not** a violation — it just doesn't
  count, same as having no evidence at all. This distinction is the two
  separate action items in goal:g3.1: "count only entries that resolve"
  (silent 0) vs. "a non-id string fails closed, loudly" (the new path
  below).
- `build_corpus(nodes_dir)` — scans every node's own declared `id:` field.
  Cheap (frontmatter only, no `graph_core`), and it's the **one** definition
  `evidence_gate.py`, `post_wire.py`, `cli.py`, and `metrics.py` all import
  and call — nobody reimplements it, so the gate and the metric cannot read
  `evidence_runs` and disagree again (that shared-field drift was the actual
  H4c root cause, not just the sentinel itself).
- `GateResult` gains `rejected` + `taxonomy_violations`, a **third** outcome
  next to `demoted`/`bypassed`. `apply_gate` only reaches it when
  `requires_evidence(verdict)` is true and the caller hasn't bypassed —
  `pending`/`inconclusive_lean_*` return before this check runs, same as
  before, so the honest-uncertainty path is untouched (verified directly by
  `test_sentinel_evidence_does_not_reject_uncertain_verdicts`).

**Reject vs. demote, kept deliberately separate.** Demote already existed
for "clean field, genuinely nothing in it" — downgrade to
`inconclusive_lean_*:50`, keep the node. A sentinel is a different kind of
wrong: it's an active claim that evidence exists when it doesn't, so it gets
the harder response — nothing is written. `TODO.md` H4c item 2 names the
convention to reuse: "the same class of defect as a malformed verdict."

- `cli.py done`: a taxonomy violation on a decisive verdict prints
  `ERR: ... taxonomy violation ...` and returns **exit 2** — literally the
  same branch shape as the pre-existing `VERDICT_RE` check just above it.
  Nothing is written (agent record untouched, no node file touched);
  verified by `test_cli_done_rejects_sentinel_evidence_runs`.
- `post_wire.py cmd_wire`: **deviation from a literal exit-2 read of
  TODO.md**, stated here on purpose. `post_wire` processes a whole
  iteration's worth of agents in one pass and has no existing precedent for
  aborting the entire run over one bad record — it already has a `skipped`
  list for "no node_id" and similar. I extended that shape: a rejected
  agent is appended to a new `rejected` list and its write (node file *and*
  parent `next_edges`) is skipped entirely, then the loop continues to the
  next agent. Same effective refusal as `cli.py`'s exit 2 — nothing about
  the bad node changes — just scoped per-agent instead of per-process, to
  match the convention `post_wire.py` already has rather than inventing a
  process-level one it doesn't.
- `--no-evidence-gate` bypasses rejection exactly like it already bypassed
  demotion — it's the designated escape hatch for historical data whose
  evidence lives outside the corpus.

`metrics.py`: `evidence_stats()` now calls `evidence_gate.build_corpus()`
once and passes it into the *same* `normalize_evidence_runs` (imported, not
reimplemented) for every node. `test_gate_and_metrics_agree_on_the_same_input`
and `test_metrics_shares_evidence_gates_normalize_function` assert this by
identity (`metrics.normalize_evidence_runs is evidence_gate.normalize_evidence_runs`),
not just by matching output.

## Measured on the real agi-tree corpus (this repo), before/after

Via `python3 extensions/agi/bin/metrics.py /home/ubuntu/work/agi-tree`,
same real corpus, only the code changed:

| metric | before (unfixed) | after (this fix) |
|---|---|---|
| `verdicts_asserting` | 115 | 115 |
| `verdicts_evidence_backed` | 42 | **4** |
| `evidence_fraction` | 0.365 | **0.035** |
| `decisive_verdicts` | 107 | 107 |
| `decisive_evidence_fraction` | 0.346 | 0.028 |
| `unevidenced_decisive_verdicts` | 70 | **104** |

This is worse, as expected — the old 0.365 was ~90% fiction, not ~20%
better than the pre-H4 baseline it looked like. Breakdown (ad hoc script
against the same corpus, not wired into `metrics.py`'s permanent output):

- 122 total verdict-bearing nodes survive the archive (115 asserting + 7
  `pending`) — the brief's own prior figure said 121; I did not chase the
  off-by-one, it doesn't change the shape of the result.
- Of the 122, **4** resolve their `evidence_runs` to a real node in the
  corpus, and all 4 of those happen to resolve specifically to a node of
  `type: experiment`.
- 36 asserting verdicts carry a taxonomy violation (a non-id-shaped
  `evidence_runs` entry) and every one of them resolves to 0 — i.e. every
  taxonomy violation found was sentinel-only, none had *also* cited a real
  id alongside the junk. 29 of the 36 are the literal string `"synthetic"`;
  the other 7 are different placeholders (`exp-a00-407fa689-verdict-repair`,
  `t-093`, `iter24-branching-chains-test`, `exp-render-context-fix-chain-length.py`,
  and similar) — the sentinel-string defect was never a single string, it
  was "trust anything in the list," and fixing only `"synthetic"` would
  have left this shape of gaming available.
- The brief's pre-recorded "33 of 121 surviving verdicts are still
  sentinel-backed" is close to but not identical to what I measured (29
  literal-`synthetic` / 36 total violations out of 122). I did not
  reconcile the gap — plausibly a different counting method upstream (e.g.
  the `synthetic: true` flag rather than the literal `evidence_runs`
  string) — and did not tune anything to make my number match theirs.

## What I chose for "no corpus" and why

`normalize_evidence_runs(value, corpus=None)` treats **every** list-shaped
`evidence_runs` as 0 when no corpus is supplied, rather than falling back to
the old `len()` behaviour. The alternative — "if I can't check, trust it" —
is exactly the bug this goal exists to close; a resolver that fails open
when it can't resolve is not a resolver. In practice this default is never
hit by a shipped writer: `cli.py`, `post_wire.py`, and `metrics.py` all
build a corpus via `evidence_gate.build_corpus(root / "nodes")` before
calling into resolution. `int`/`bool`/numeric-string values are exempt from
this fail-closed rule on purpose — they're a bare number the author typed,
not a claim to verify against anything, and were never how the sentinel
attack worked.

## The irony, handled

This node's own `evidence_runs: 1` is a **bare int**, not a list — under
the rule above, ints are direct attestation and are not resolved against
the corpus (there is nothing to resolve; a number is not a reference). So
this claim isn't exploiting the H4c hole — a list containing an
unresolvable placeholder would be. It also isn't ungated data: this node
is `type: experiment`, not a verdict, so `apply_gate` never touches it
(no `verdict:` field here to demote or reject). The claim is simply meant
literally: this node documents one completed, real pass — design the
resolution + taxonomy rule, implement it across both writer paths and the
metric, add the tests above, and run the before/after measurement against
the live corpus — not a placeholder for work that didn't happen. It follows
the one precedent for this exact frontmatter shape already in this corpus,
`exp:engine-census-r1` (`evidence_runs: 1`, also a bare int, also on an
`experiment` node).

## Tests

Added to `extensions/agi/tests/test_evidence_gate.py`: resolution with and
without a corpus, the sentinel-counts-0 case, mixed lists, taxonomy
violations as a concept distinct from unresolved-but-shaped ids,
`build_corpus`, reject-vs-demote-vs-bypass on `apply_gate`, the `cli.py`
exit-2 path and its `--no-evidence-gate` override, and the `post_wire.py`
reject path (including that it does not touch pending/lean verdicts).
Updated `extensions/agi/tests/test_metrics.py` similarly, plus an identity
check that `metrics.py` and `evidence_gate.py` share one function. Three
pre-existing tests (`test_cli_done_infers_evidence_from_node_frontmatter`,
`test_post_wire_falls_back_to_node_frontmatter_evidence`, and three
`evidence_fraction` tests in `test_metrics.py`) had encoded the *old*
buggy semantics — they cited bare placeholder strings (`"r1"`, `"run-a"`)
as if that were evidence. Updated them to cite real, corpus-resolvable
node ids instead, so they test the behaviour this fix actually intends.

Full suite: `cd /home/ubuntu/work/agi && python3 -m pytest extensions/agi/tests -q`
→ **384 passed, 0 failed** (330 baseline + this task's additions), stable
across three consecutive runs. One run mid-session showed a single
unrelated failure in `test_dashboard.py`; it did not reproduce in isolation
or on rerun, and traced to `extensions/agi/bin/dashboard.py` /
`extensions/agi/tests/test_dashboard.py` — untracked files a concurrent
sibling agent was actively writing to at that moment (its own docstring
independently reimplements evidence resolution specifically to avoid
depending on this in-flight change, which is worth the parent's attention:
a second engine repo now has resolution logic parallel to this one). Per
the brief's hard rule I did not touch, read further into, or fix those
files beyond confirming the failure wasn't mine.

## Deviations from the brief, summarized

1. Taxonomy-violation rejection is scoped to `requires_evidence(verdict)`
   only — a stray sentinel sitting in `evidence_runs` on a `pending` or
   `inconclusive_lean_*` node does not block that write. Not stated
   explicitly in TODO.md's H4c item 2, but required by this task's rule 3
   ("do not break the honest-uncertainty path") and directly tested.
2. `post_wire.py` rejects per-agent (skip + report) rather than hard-exiting
   the whole wire pass, unlike `cli.py`'s literal exit 2 — reasoned above.
3. Did not add a permanent `verdicts_resolved_to_experiment`-style field to
   `metrics.py`'s output; computed that count with a one-off script for
   this report instead, to avoid growing the metric surface for a number
   this task needed once.