# Zoom round-trip ground truth (L1 baseline)

Raw artifacts from the zoom round-trip experiment whose results are recorded in
`TODO.md` L1 — overall claim recall **0.441** against a 0.90 bar, frontmatter
0.000, prose 0.792.

These were produced in `fantasia` under its old G2 (`sessions/iter-004/a01-zoomloss/`,
gitignored there and therefore machine-local and at risk). G2 was engine work
living in a game repo; when it moved into this file's L1–L7, the artifacts moved
here so the follow-up can still run.

## What's here

| Path | What it is |
|---|---|
| `ground-truth-a-t005.md` | Atomic claim list for subject A (`task:t-005`), category-tagged, written **before** any decomposition ran |
| `ground-truth-b-g1.md` | Same for subject B (`idea:goal-playable-dungeon-crawler`) |
| `scores.md` | Per-claim scoring, the locked scoring rule, and the recall table |
| `subject-{a,b}-*/trial-{1,2,3}/children.md` | What the zoom-in (decomposer) agent wrote |
| `subject-{a,b}-*/trial-{1,2,3}/reconstruction.md` | What the zoom-out (summarizer) agent rebuilt from `children.md` alone |

Both agents were haiku, ran with no shared context, and never saw the claim lists.

## Why they are kept

The next L1 node is an A/B against exactly this baseline: *mechanically inherited
contract slices restore round-trip fidelity without a smarter model.* Ground
truth, scoring rule, and baseline numbers all already exist here, which is what
makes that experiment cheap and directly comparable rather than a fresh
measurement. Recreating it from the protocol would cost 12 agent runs and would
not be comparable — different ground truth, different rater.

**Known limits, carried from the verdict:** single rater who also authored the
ground truth; one model tier; one prompt shape; two thin subjects; **precision
was never scored**. A re-run should add a third dense subject whose dependency
list is deliberately *not* the decomposition axis, and score precision.
