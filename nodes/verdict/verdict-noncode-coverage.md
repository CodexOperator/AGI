---
confidence: 0.85
evidence_runs:
  - exp:noncode-surface-census
  - exp:prose-surface-probe
id: "verdict:noncode-coverage"
parents:
  - exp:prose-surface-probe
status: open
subgraph: false
tags:
  - g6.6
  - level3
title: "Coverage diagnosis holds, prescribed remedy does not deliver what G6.6 promises"
type: verdict
verdict: disproved
---

**VERDICT: disproved.** G6.6 bundles two claims that resolve in opposite
directions: the coverage gap it diagnoses is real and severe (proved), but
the fix it prescribes — a level-3 node per non-code surface with "the same
derived contract shape as a code node" — does not deliver the thing the goal
exists to buy, so the goal cannot be certified proved as written.

**Coverage claim — held:** 74/316 raw (23.4%), 74/189 eligible (39.2%) after
excluding generated/ephemeral artifacts; 0/74 declared-scope files missed
(the generator does exactly what it says, the gap is a scope decision, not a
bug); all 9 named files (`SKILL.md`, `agent-prompt.md`, three shell entry
points, the TS bridge, `schema.sql`, `README.md`, `TODO.md`) confirmed
uncovered. The omitted surface is disproportionately the highest-leverage
part — census independently rediscovered a live, currently-uncaught
contradiction between `agent-prompt.md` and `SKILL.md` on whether a kid
commits and calls `cli.py done`, which is exactly the failure mode G6.6
predicts.

**Remedy claim — failed:** the probe ran G6.6's own falsifier for real
(one-word edit to live `SKILL.md`, `stitch --verify` before/after) and it
fired as predicted — zero drift, because `ast.parse` dies unconditionally on
line 4's em dash before reaching anything else, so stored-vs-fresh are
always identical regardless of what changed. Of the four candidate prose
contract shapes evaluated (content hash, extracted structure, extracted
claims, payload-identity-only), the best — extracted claims — would pass
that literal falsifier: the edited clause sits inside a directive claim, so
a stored-vs-fresh claim diff fires. But extracted claims, and every other
candidate, would **not** have caught the actual bug that motivates the
goal — the `agent-prompt.md`/`SKILL.md` contradiction — because that is two
self-consistent nodes disagreeing with each other, not one node going stale
against its own file. `stitch.py`'s only cross-node check today
(`duplicate_payload_ref`) is an exact-string match on `payload_ref`, never
content; `stale_contracts` (where any prose contract plugs in) is
architecturally one-node-vs-its-own-file. Detecting "commit your work"
contradicting "do not commit" needs a check class stitch.py does not have
(cross-node claim comparison) plus a semantic-negation judgment no
mechanical diff performs. So the remedy as literally stated would make
`--verify` report drift on *some* prose edits, but would leave the specific,
already-found, highest-cost bug just as invisible as it is today.

**What G6.6 is missing:**
1. A concrete contract-shape decision — G6.6 leaves this open ("deciding
   what a SKILL.md node's contract *is* is the real work here"); the probe
   did that work and the answer is extracted claims (directive clauses,
   numbered rules), not content-hash or structure-only. G6.6 should adopt
   this rather than leave it undecided.
2. An explicit fifth `stitch.py` check category — cross-node claim
   comparison — since none of the current four categories compares two
   nodes' content against each other, only a node against its own file.
   Without this, node coverage alone cannot deliver the reflexive-case
   protection G6.6 argues for.
3. An admission that catching semantic contradictions (not just detecting
   *that* something changed) needs a model-judgment step alongside the
   mechanical `how`/`why` split code contracts use — this is `TODO(model)`
   territory the goal doesn't currently reserve space for.
4. The falsifier itself needs rewriting: "edit one word of SKILL.md, does
   `--verify` report drift" is passable by extracted claims without solving
   the goal's actual motivation. A falsifier that measures what the goal is
   *for* should instead be: reintroduce the `agent-prompt.md`/`SKILL.md`
   contradiction and confirm `stitch.py --verify` flags it. Passing the
   current falsifier would produce false confidence that the reflexive case
   (G1.3/G1.4 touching `agent-prompt.md`) is protected when it is not.

**Caveat:** the extracted-claims design was evaluated on paper against one
real edit, not built or run against a corpus of historical edits — its
"reacts to directive-clause edits, blind to plain-descriptive-prose edits"
characterization is a design analysis, not a second falsifier run.
