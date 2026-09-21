---
id: goal:g7.3
mint_id: aa7f005bc80244729b3cdc87218dd8d1
type: goal
parents:
  - goal:g7
confidence: 1.0
edited_by: season.py
goal_id: G7.3
goal_kind: subgoal
heading_level: 3
origin: goals-doc
season: 1
seeds: []
status: complete
tags:
  - goal
  - subgoal
thought_session: season
title: "G7.3: `evidence_runs` as a bare integer is still unverifiable"
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

## Closed 2026-08-27 — a bare integer no longer counts

`normalize_evidence_runs` returns 0 for every scalar: `int`, `bool`, and
numeric string alike. Only a reference resolving to a real node in the corpus
counts. H4c removed `"synthetic"` for being uncheckable and left `3` accepted
as "direct attestation"; it was the same hole with a different literal.

**The honest-count path this goal worried about breaking was preserved rather
than sacrificed.** `is_unverifiable_attestation()` keeps the count *visible* so
it does not read as plain absence, and `cli.py done --evidence-runs` now takes
node ids while still accepting a bare count — as a **soft demotion, never a
rejection**. That distinction was found by breaking it: collapsing the flag to
a list made `--evidence-runs 0` arrive as `["0"]`, which the taxonomy check
treated like the `synthetic` sentinel and rejected with exit 2, discarding the
agent's work over an argument style that was the documented one that morning.
Rejection is for claims that are actively false; an unverifiable count is not
that.

`cli.py` also now writes the *references* back to the node rather than the
resolved count. Writing the count would have been self-defeating: the node
would come back off disk as a bare int and a correctly evidenced verdict would
fail its own gate on the next read.

**The 12 live instances, resolved without inventing a single citation:**

- `verdict:zoom-encoded-node-ids` — the severe one, `proved` and decisive only
  because of the unchecked `1`. **Not demoted.** Its evidence was never
  missing, only unnamed: its own `parents:` lists exactly one node,
  `exp:id-fanout-budget`, which exists, and a verdict's parent experiment is
  its backing run. Naming it is reading the node's own frontmatter.
- The other 11 are all `exp:` nodes carrying **no verdict**, whose parents are
  goals and hypotheses rather than experiments. For those, choosing a reference
  genuinely would be invention — which is exactly what this goal refused to do
  in the 2026-08-27 survey — so they were left as they are. Carrying no
  verdict, they cannot be decisive and cost nothing.

Measured across the change: `unevidenced_decisive_verdicts` 0 -> 1 (the alarm
firing on the one false `proved`) -> 0 (after naming the reference).
`decisive_evidence_fraction` 1.0 -> 0.941 -> 1.0. `evidence_fraction` returns
to 0.206 — the same number as before, now backed by a reference that resolves
instead of by an assertion nobody could check.

Side effect worth recording: `metrics.py` and `dashboard.py` now agree.
`test_bare_integer_evidence_runs_fails_closed` used to assert they disagreed
and called that gap "the contamination the dashboard exists to name". Closing
the hole in the shared `normalize_evidence_runs` closed it in both.