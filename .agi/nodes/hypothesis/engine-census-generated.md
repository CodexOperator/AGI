---
id: hyp:engine-census-generated
mint_id: c76a008cb4d7427b82df98d979ae03f2
type: hypothesis
parents:
  - idea:engine-self-decomposition
confidence: 0.5
edited_by: season.py
season: 1
subgraph: false
tags:
  - engine
  - l19
testable_claim: A script-generated, git-ls-files-seeded census of the engine's changeable surfaces (23 units - 6 src/ packages, 12 bin/*.py, 5 named entry points) stays accurate across re-runs and engine changes, where the 14 hand-written domain-* idea nodes did not.
thought_session: season
title: A generated engine census stays current where a hand-written one rotted
---
**The claim.** `decompose-engine.py` treats the idea layer's "which surfaces does
the engine have" question as a derived view of `git ls-files`, not a document a
human maintains by hand. If that is the right design, two things should hold
that did not hold for the hand-written layer:

1. **It does not rot.** The hand-written `domain-*` layer has 14 nodes; only 5
   (`graph-core`, `chain-engine`, `renderers`, `schema-registry`, `embeddings`)
   still name a surface that exists. `domain-exporters` and
   `domain-environment-indexers` name modules `git log --all --diff-filter=A`
   has no record of ever existing in this form. A generated census re-derives
   its 23 nodes from the tracked file tree every run, so it cannot silently
   drift out of sync with the code the way a document nobody re-reads can.
2. **Re-running it is safe.** The same script class (`snapshot-build-site.py`,
   pre-H0i `snapshot-goals.py`) has already destroyed chain structure once by
   rebuilding frontmatter from scratch on every pass, silently dropping
   `next_edges` on 15 nodes while reporting success. A generator built the same
   way would reproduce that defect on the idea layer instead of the goal layer.

**What would falsify it — pre-registered in `idea:engine-self-decomposition`
§5, carried forward unchanged:**

- **Hard, no waiting period.** Two consecutive runs against an unchanged engine
  producing a non-empty diff under `nodes/` disqualifies the generator
  outright — that is H0i again, not a bug to patch later.
- **Hard, no waiting period.** A module rename or removal lands and the old
  generated node is not retired in the same run (i.e. pruning does not track
  `git ls-files`, or reaches nodes it does not own).
- **Statistical, 20 iterations out.** If the fraction of generated idea nodes
  that have grown at least one child hypothesis falls below **79%** (11 of the
  14 hand-written ideas have ≥1 `next_edges` child today — that is the bar to
  beat), the census bought coverage at the cost of thought: 23 nodes nobody
  argues with, the H3 hop-padding pattern one layer up.

**Numbers pre-registered before this run, so the experiment node can be
checked against them rather than written to match them:**

- Exactly **23** units expected (6 + 12 + 5), per `git ls-files` against
  `extensions/agi/` and `extensions/agi-bridge/index.ts`.
- **0** units expected to carry a `parents:` goal pointer on this first run —
  no unit -> goal mapping has been declared anywhere in the repo yet (checked:
  none of the 5 existing hand-written domain nodes carry `parents:` either),
  and the generator is built to never guess one.
- A second identical run must produce **byte-identical** files under
  `nodes/idea/engine-*.md` — checked directly, not just via `git diff`, since
  the first write is to untracked paths and plain `git diff` does not see
  untracked files at all.

This hypothesis is scored by what `exp:engine-census-r1` actually measured
against these numbers, not by whether the run "looked successful."