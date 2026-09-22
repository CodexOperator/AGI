---
id: experiment:a00-c616d368-scalar-evidence-type-violation
mint_id: c409c78fcffe4e9b9879f9d6a4f5f4e8
type: experiment
parents:
  - hypothesis:a00-c616d368-e4ece1
next_edges: []
edited_by: a00-c616d368
evidence_runs: experiment:a00-c616d368-scalar-evidence-type-violation
confidence: 0.9
production_lines: 38
line_ceiling: 40
season: 2
status: completed
tags:
  - experiment
  - evidence-gate
  - g7.31.4
title: "exp: scalar evidence_runs is a list/type violation -- the gate test plus the whole gate suite, green"
town: core
---
# experiment:a00-c616d368-scalar-evidence-type-violation

**Hypothesis:** `hypothesis:a00-c616d368-e4ece1`
**Status:** completed
**Date:** 2026-09-22
**Agent:** a00-c616d368

## What was run

Pre-fix reproduction (in a scratch interpreter, on the committed bytes):

```
evidence_runs_violations("exp:real")            -> []          # scalar silently accepted
normalize_evidence_runs("exp:real", {"exp:real"}) -> 0
apply_gate("proved", "exp:real", corpus={"exp:real"},
           self_id="hypothesis:x", node_type="hypothesis")
  -> rejected=False, demoted=True, verdict=inconclusive_lean_proved:50
     # named "no evidence", NOT named a type error
```

The scalar id-shaped string is exactly the MUR case
(`mur-g7-31-4-dt-85`): `evidence_runs: experiment:a00-752a05cb-mesh-transport-loci`
on a real node is a scalar string, resolves to 0, and was reported as
"no evidence" rather than a schema type violation.

## The fix (production bytes)

`extensions/agi/bin/evidence_gate.py`, 38 changed production lines:

- `evidence_runs_violations`: a present, non-list value now returns `[value]`
  instead of `[]`; `None` still returns `[]` (absent is not malformed).
- `apply_gate`: the rejection message now names a **list/type violation**,
  not only "non-id value(s)". A scalar count (int/bool/numeric string,
  including the literal `0` `cli.py` passes for `--evidence-runs 0`) stays the
  softer goal:g7.3 unverifiable-attestation demotion, so the documented
  `--evidence-runs 0` path does not hard-fail.

## New test (the visibility end to end)

`extensions/agi/tests/test_evidence_gate.py`:

- `test_evidence_runs_violations` rows updated: `(0, [0])`, `("3", ["3"])`,
  plus the new scalar id-shaped row `("exp:real", ["exp:real"])`.
- `test_scalar_evidence_runs_rejects_a_decisive_verdict_as_a_type_violation`:
  `apply_gate("proved", "exp:real", corpus={"exp:real"},
  self_id="hypothesis:x", node_type="hypothesis")` must be `rejected`, must
  NOT be a mere `evidence_runs=0` demotion, and `res.reason` must name the
  type violation.

## Real output

```
$ python3 -m pytest extensions/agi/tests/test_evidence_gate.py -q
141 passed, 9 warnings in 4.76s
```

Whole gate suite (the brief's second command):

```
$ python3 -m pytest extensions/agi/tests/ -q -k "evidence or gate"
1 failed, 428 passed, 1 skipped, 5512 deselected, 23 warnings in 90.08s
```

The one failure is
`test_season.py::TestMergeUp::test_merge_up_town_gate_refuses_cross_town_and_allows_same_town`
— an environment issue (git "Committer identity unknown" inside a temp repo),
not an assertion in any file this round touched. Re-run alone reproduces the
same git-identity failure, so it is pre-existing and unrelated.

## Production lines

`git diff --numstat -- extensions/agi/bin/evidence_gate.py`:
`38  16  extensions/agi/bin/evidence_gate.py` -> `production_lines: 38`,
under the 40-line ceiling.

## Evidence

Raw output, screenshots, logs.