---
id: hypothesis:a00-7fcf6562-82d4b3
mint_id: 7f12b0add53f4380b205f8bbc0a41fdd
type: hypothesis
parents:
  - goal:g7.8
next_edges: []
confidence: 0.0
edited_by: season.py
scaffold_hash: 23ae4fe4112e53c9
season: 1
testable_claim: "Adding a corpus-resolution check before `snapshot-build-site.py` writes a parent-hyp ID (constructed at line 358 as `f\"hyp:{domain}-{rnum.lower()}\"`) will catch every unresolved reference that the current code silently accepts — emitting `WARN: task <id> cavekit_req <req> -> unresolvable <parent_hyp>` and setting `parents: []` — without ever producing a false-positive (flagging a reference that actually resolves) or a false-negative (missing a reference that does not resolve)."
thought_session: season
title: A00 7fcf6562 82d4b3
verdict: pending
---
# hypothesis:a00-7fcf6562-82d4b3

<!-- THOUGHT:BEGIN -->
Parent a01-d34158ae review (iter 1014): accepted as written, no demotion — verdict
`pending` on an untested hypothesis is the correct state. Both load-bearing factual
claims were checked against the artifact, not the report: (1) `bin/snapshot-build-site.py`
line 358 does construct `parent_hyp = f"hyp:{domain}-{rnum.lower()}"`, and a second
occurrence exists at line 252 for the hyp nodes themselves, so a fix must cover both
write sites, not just the task site the claim names; (2) line 371 writes
`"parents": [parent_hyp] if parent_hyp else []` with no membership check against the
loaded corpus, so the "defect" premise stands. The zero-FP/zero-FN bound is strong
for a hypothesis to test, which is why it stays pending until an exp measures it.
<!-- THOUGHT:END -->

## Hypothesis

### Testable claim

Adding a corpus-resolution check before `snapshot-build-site.py` writes a parent-hyp ID (constructed at line 358 as `f"hyp:{domain}-{rnum.lower()}"`) will catch every unresolved reference that the current code silently accepts — emitting `WARN: task <id> cavekit_req <req> -> unresolvable <parent_hyp>` and setting `parents: []` — without ever producing a false-positive (flagging a reference that actually resolves) or a false-negative (missing a reference that does not resolve).

### Formal statement

Let:
- C = set of hypothesis node IDs in the loaded corpus at write time
- H(t) = constructed parent ID `f"hyp:{domain}-{rnum.lower()}"` for task t
- P(t) = the `parents` entry written for task t

**Current behavior (defect):** ∀ t where `cavekit_req` contains "/": P(t) = [H(t)]. No check that H(t) ∈ C.

**Proposed behavior:** If H(t) ∈ C then P(t) = [H(t)]; else P(t) = [] and emit `WARN: task {t[id]} cavekit_req {t[cavekit_req]} -> unresolvable {H(t)}`.

**Claim:** On the current corpus, the proposed behavior produces zero changes to P(t) for every task where H(t) is already resolvable, and emits WARN only for the known dangling cases (T-090, T-092 referencing `hyp:graph-core-r11` before the kit fix; T-020's unresolvable blocker refs). The set of tasks with changed P(t) equals the set of tasks with unresolvable H(t).

### What would prove it

1. Run `driver.sh --smoke` on the current corpus to snapshot all task nodes.
2. Implement the resolution check in `snapshot-build-site.py`.
3. Re-run `driver.sh --smoke` and compare — every task that previously had `parents: [hyp:...]` still has that same parent; no task loses a valid parent.
4. Confirm WARN lines are emitted only for known unresolvable references (the T-020 blocker edge).
5. The total set of changes is exactly the set of unresolvable references, with no false positives.

### What would disprove it

- Any task with a valid, resolvable parent-hyp ID receives `parents: []` instead (false positive — the resolution check is over-matching).
- A known dangling reference is missed (false negative — the check is under-matching).
- The change breaks the generator's ability to produce task nodes at all (crash on load, malformed corpus state).


## Agent Notes
Hypothesis: snapshot-build-site.py's parent-hyp ID construction (line 358) should resolve against the loaded corpus before writing, emitting WARN + parents:[] on miss. Formal claim with zero-false-positive/zero-false-negative bounds.