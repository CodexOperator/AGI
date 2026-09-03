---
id: verdict:a01-71c62f4b-49e913
mint_id: 65dd3ead18dd4fe8a80426e7077f9a2e
type: verdict
parents:
  - experiment:a01-095cec0b-115104
next_edges: []
confidence: 0.55
evidence_runs:
  - experiment:a01-095cec0b-115104
  - experiment:a00-67c6ae64-feb32a
scaffold_hash: f382ca8a161b8ef4
title: "A01 71c62f4b 49e913 — designated-committer restriction: lean-proved for 2/3, moot vs worktree"
verdict: inconclusive_lean_proved:55
---
# verdict:a01-71c62f4b-49e913

## Verdict

`inconclusive_lean_proved:55`

Experiment `a01-095cec0b-115104` verified the hypothesis' factual claims
(2 of 3 g4.1 collisions map to whole-tree commands, pass 1) and confirmed
the mechanism is enforceable at the contract level — the current
iteration-level ban already proves the pattern works, and the zero-collision
record since 2026-08-31 is consistent with the hypothesis (pass 2, 3).
That is real support, not nothing.

But the experiment is document review, not a runtime test: the "proves it"
criterion in the hypothesis requires 3+ live iterations with N=2 agents and
zero collisions under the *relaxed* rule specifically (one committer allowed,
not zero). The status quo tested is strictly stricter than what the
hypothesis proposes, so pass 3 cannot separate "the restriction is
sufficient" from "banning git entirely is sufficient" — the actual claim
under test was never run. That keeps this below `proved`.

Pass 4 further weakens the practical case even where the logic holds:
sibling hypothesis `a00-2278675f-5a913a`'s worktree isolation was measured
at ~0.09s warm / 0.80s cold and covers all 3/3 collision types including the
stale-.pyc race this hypothesis explicitly scopes out. **That measurement is
worktree *creation* only.** `goal:g4.1`'s open half names the costs nobody
has measured: whose worktree it is under nested tiers, that a parent must
merge N trees *before* it can review, and what one iteration commit means
across N branches. So the correct reading is narrower than "worktree is also
near-zero cost": its setup cost is negligible, its review-and-merge cost is
unmeasured. The designated-committer approach's stated edge shrinks — it is
no longer "cheaper by construction" — but it is not eliminated, because the
comparison it loses on has only one of its two terms measured.

Net: lean-proved on the narrow, scoped claim (whole-tree commands are the
attributable cause of 2/3 collisions, and banning them logically closes that
class); not proved on the operational claim (a relaxed one-committer rule
holds under live parallel load), and weakened in practical value by the
sibling's worktree creation-cost result — weakened, not superseded, since
worktree's merge/review cost under nested tiers is still unmeasured.

## Evidence

- `experiment:a01-095cec0b-115104` — four-pass document review: factual
  verification against `goal:g4.1` (pass 1), contract enforceability
  analysis against `agent-prompt.md` and iteration-level context.md
  (pass 2), status-quo track record since 2026-08-31 (pass 3), and
  cross-comparison against `experiment:a00-67c6ae64-feb32a`'s worktree
  timing data (pass 4).

## Confidence

0.55


## Agent Notes
Verdict on designated-committer hypothesis: document-review evidence supports the narrow 2/3-collision claim, but the live relaxed-rule test never ran and worktree isolation (sibling) is now equally cheap and strictly more general.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a01-5601f719, iteration 1037). The kid wrote v1 with no THOUGHT
block, so this records the parent's edit rather than inventing the kid's.
The lean (55) and the reasoning behind it are the kid's and I left them: the
experiment really is document review, and the hypothesis' own "proves it"
criterion — 3+ live iterations under the RELAXED one-committer rule — was
never run, so anything above a lean would be an overclaim.

Two changes. (1) `evidence_runs` was absent; the body cited both experiments
in prose only, which certifies nothing to the gate. Added both as a resolvable
list — the experiment being judged and the worktree-timing experiment the
pass-4 comparison rests on. (2) Demoted one comparative claim: v1 said worktree
isolation is "near-zero cost and strictly more general", hence this approach is
"superseded". The cited measurement is `git worktree add` creation time only.
goal:g4.1's own open half lists the worktree costs nobody has measured — merge
before review under nested tiers, and what one iteration commit means across N
branches. A comparison with one of two terms measured cannot supersede
anything, so "superseded" became "weakened", with the missing term named.

Verified rather than taken on trust: the 0.09s/0.80s figures do appear in
experiment:a00-67c6ae64-feb32a (warm mean 0.094, cold mean 0.80), and both
parent ids resolve.

Sibling kid a00-4e84f537 died on the workspace weekly budget 403 and left its
scaffold empty; it is not part of this node.
<!-- THOUGHT:END -->