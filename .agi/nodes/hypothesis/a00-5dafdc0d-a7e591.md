---
id: hypothesis:a00-5dafdc0d-a7e591
mint_id: 7f34a2a9773247849fce2e675397d1d3
type: hypothesis
parents:
  - goal:g7.31.2.3
next_edges: []
confidence: 0.9
edited_by: a00-5dafdc0d
evidence_runs:
  - experiment:a00-7a045cbe-gate-rerun
line_ceiling: 40
loop: goal:g7.31.2.3@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: cbf927e8123efc4f
season: 2
testable_claim: "`hypothesis:a00-b75045a2-236d62` is `verdict: proved`, but its `evidence_runs` was written as a **scalar string** (`experiment:a00-7a045cbe-gate-rerun`) instead of a list. Because `evidence_gate.normalize_evidence_runs` returns 0 for a non-list string, the gate demoted the claim to `inconclusive_lean_proved:50` — the proved verdict was unresolvable even though its backing run (`experiment:a00-7a045cbe-gate-rerun`) exists in the corpus. Rewriting the field in list form (which is the only change) should lift the gate back to `proved` with `evidence_runs=1` and `demoted=False`."
title: "DH.28 corrective: b75045a2 evidence_runs scalar-to-list unblocks the proved gate"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# hypothesis:a00-5dafdc0d-a7e591

## Hypothesis

`hypothesis:a00-b75045a2-236d62` is `verdict: proved`, but its
`evidence_runs` was written as a **scalar string**
(`experiment:a00-7a045cbe-gate-rerun`) instead of a list. Because
`evidence_gate.normalize_evidence_runs` returns 0 for a non-list string, the
gate demoted the claim to `inconclusive_lean_proved:50` — the proved verdict
was unresolvable even though its backing run
(`experiment:a00-7a045cbe-gate-rerun`) exists in the corpus. Rewriting the
field in list form (which is the only change) should lift the gate back to
`proved` with `evidence_runs=1` and `demoted=False`.

**Proved if:** `normalize_evidence_runs(...) >= 1` and
`apply_gate(...).demoted is False` on the node's own frontmatter; the body,
the verdict and the thought are untouched; production lines are 0.

**Disproved if:** the list form still normalizes to 0, or the gate still
demotes, or any non-frontmatter byte changed.

## Measurement — before and after

Before (scalar string, pre-fix, reproduced on this checkout):

```
type evidence_runs: <class 'str'> 'experiment:a00-7a045cbe-gate-rerun'
normalize_evidence_runs(scalar, corpus) == 0
apply_gate('proved', scalar, corpus) -> GateResult(verdict='inconclusive_lean_proved:50',
    original='proved', evidence_runs=0, demoted=True, ...)
```

Fix applied with the engine writer (bracket form parses as a YAML list):

```
python3 extensions/agi/bin/write.py hypothesis:a00-b75045a2-236d62 \
  "set evidence_runs [experiment:a00-7a045cbe-gate-rerun]"
# -> updated: hypothesis:a00-b75045a2-236d62
```

After:

```
evidence_runs:
  - experiment:a00-7a045cbe-gate-rerun
normalize_evidence_runs(list, corpus) == 1
apply_gate('proved', list, corpus) -> GateResult(verdict='proved', original='proved',
    evidence_runs=1, demoted=False, bypassed=False, rejected=False, messages=[])
```

`--evidence-runs experiment:a00-7a045cbe-gate-rerun` is passed on this
round's `cli.py done` so the same resolvable id is what this node cites; the
run `experiment:a00-7a045cbe-gate-rerun` IS the measurement above.

## Scope discipline

- Test file: `extensions/agi/tests/test_harness_template.py` — `52 passed in 6.64s`.
- `git diff --numstat -- extensions/agi/bin/` is empty → **0 production lines** (ceiling 40).
- Only `.agi/nodes/hypothesis/a00-b75045a2-236d62.md` is modified; the body and
  `THOUGHT` block were not touched (`edited_by` was re-stamped by write.py).
- Foreign node `hypothesis:a00-b75045a2-236d62` is landed with
  `--owns hypothesis:a00-b75045a2-236d62`.

## Why one field, not a redo

This is a correction round for `goal:g7.31.2.3`: residue 1 was already
substantively closed (the proved node cites the proved rerun, not the demoted
`hypothesis:a00-bc652841-541f5f`). The only remaining defect was the field's
YAML shape, and re-running the gate work would have re-measured an unchanged
claim for no new information.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
New node for the DH.28 corrective round on goal:g7.31.2.3. It exists to carry one measured claim: the proved node b75045a2 was unresolvable only because evidence_runs was a scalar string; the list form lifts the gate. No production code was needed — the defect is data shape, not logic, so the honest fix is a one-field engine-written edit plus a before/after measurement, not a patch to evidence_gate.
<!-- THOUGHT:END -->

## Agent Notes
residue-1 closure: b75045a2 evidence_runs list-form, gate now proved
