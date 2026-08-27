---
confidence: 1.0
goal_id: G7.3
goal_kind: subgoal
heading_level: 3
id: "goal:g7.3"
mint_id: aa7f005bc80244729b3cdc87218dd8d1
order: 42
origin: goals-doc
parents:
  - goal:g7
seeds: []
status: horizon
tags:
  - goal
  - subgoal
title: "G7.3: `evidence_runs` as a bare integer is still unverifiable"
type: goal
---

Residual left open by G3.1 and named here so it is not forgotten. After the
H4c fix a list entry must resolve to a real node, but an integer
(`evidence_runs: 3`) is still accepted as direct attestation and counts 3.
Writing an integer is exactly as cheap as writing the `synthetic` sentinel was.

Not closed immediately on purpose: many honest nodes legitimately record a
count rather than ids, and forcing ids everywhere would break the honest path
in order to close a hole nobody has yet exploited. Decide deliberately — the
H4c lesson is that any unverifiable field eventually gets gamed, so the
question is when, not whether.

## Live examples, measured 2026-08-27 — the hole is populated, not theoretical

`evidence_runs` is declared `{type: list}` by both `[verdict].md` and
`[experiment].md`. **77 of the 112 nodes carrying the field hold a bare
integer instead**, so two thirds of the corpus violates the declared type of
the one field the evidence metric reads.

| shape | n | disposition |
|---|---|---|
| bare int `0` | 65 | normalized to `[]` on 2026-08-27 — same meaning, no invention |
| **bare int `1`** | **12** | **left as-is: converting requires knowing *which* experiment, which is inventing it** |
| list | 35 | 32 refs, all resolving after the same pass |

The 12 that remain, and they are the whole of the open hole:

    verdict:zoom-encoded-node-ids        evidence_runs: 1   verdict: proved
    exp:integrity-detection-r1           evidence_runs: 1
    exp:zoom-numeric-axis-r1             evidence_runs: 1
    exp:graph-first-engine-publish       evidence_runs: 1
    exp:engine-census-r1                 evidence_runs: 1
    exp:level3-scan-r1                   evidence_runs: 1
    exp:stitch-roundtrip-r1              evidence_runs: 1
    exp:prose-surface-probe              evidence_runs: 1
    exp:grid-payload-roundtrip           evidence_runs: 1
    exp:dashboard-cli-r1                 evidence_runs: 1
    exp:noncode-surface-census           evidence_runs: 1
    exp:evidence-gate-resolution-r1      evidence_runs: 1

**`verdict:zoom-encoded-node-ids` is the one that matters.** It is `proved`,
and it is decisive *only* because `normalize_evidence_runs` treats a bare int
as direct attestation and returns it unchecked. It passes the gate today. It
is not an overclaim anyone made in bad faith and it is not a gate bypass —
it is this goal's hole, occupied, in the highest-severity form the taxonomy
has. Every other entry is an `exp:` node, where a run *count* is at least a
defensible reading of the field.

**Why this was not fixed in the 2026-08-27 pass.** The `0 -> []` half is a
pure node edit and was done. The `1 -> [id]` half is not a node edit at all:
it needs `normalize_evidence_runs` to stop trusting integers, which is a
payload change to `bin/evidence_gate.py`, published through the grid, plus a
decision about the honest-count path this goal already flags. Scoped out
deliberately, recorded here so the next session starts from the list rather
than from the survey.
