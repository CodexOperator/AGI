---
id: idea:deprecate-the-gamed-mass
mint_id: de4f70aaff7c4b7db9b81520fddb408d
type: idea
parents:
  - goal:g6
confidence: 1.0
edited_by: season.py
scale: big
season: 1
status: open
tags:
  - engine
  - seed
  - l19
thought_session: season
title: Deprecate the gamed mass without deleting it
---
Retire the H3 padding by **stamping** it, never by editing or removing it. What
follows is measured on the corpus, not restated from `TODO.md`.

## 1. The predicate

I read all 29,138 `experiment/` + `verdict/` files. Padding is not a judgement
call — it self-identifies three ways over:

- **Dense arithmetic families.** 29,060 node ids end in `-extend<N>`. They form
  **50 families**, 48 of which have ≥20 members; 20 families have *exactly 996*
  members (`exp:graph-core-r1-extend1..996` and siblings). Real work does not
  produce 996 consecutive integers.
- **Degenerate bodies.** Median body of an `extend` node is **59 characters**
  ("`Cycle 432.`", "`Chain extension cycle 262 (hops = 2*262+8 = 532).`").
  Median for everything else is **461**. The *longest* body in the entire 29,060
  is 421 chars, and it is about hop counts. There is no overlap to arbitrate.
- **Self-declaration.** 2,843 nodes carry `synthetic: true` and 2,842 carry
  `evidence_runs: [synthetic]` — the literal string. `normalize_evidence_runs`
  in `bin/evidence_gate.py` returns `len(list)`, so `["synthetic"]` counts as
  one run. Across all 14,579 verdicts, exactly **27** cite a real experiment id.
  `evidence_fraction: 0.196` is ~99% synthetic. That is worse than H3 recorded.

**Proposed predicate (family-scoped, not per-node):** a node is padding iff
(a) `type ∈ {experiment, verdict}`, (b) its id matches `^(?P<stem>.+)-extend(?P<k>\d+)$`,
(c) ≥20 nodes share that stem with `k` dense over `1..K`, and (d) `k > 3`.

Clause (d) is the precision clause and it is the one I would defend hardest.
`exp:exporters-r1-extend` and `exp:chain-engine-r1-extend` are **real prior
art**: they are the experiments that first established the
verdict→experiment→verdict cycle is stackable, which is the mechanism H3 is
*about*. Deprecating them buries the evidence for the finding. Preserving `k≤3`
per family costs **142 nodes** out of 29,060 — cheap insurance against exactly
the failure this node is trying to avoid.

**Yield: 28,916 deprecated, 142 preserved live, 78 exp/verdict nodes untouched.**

Where it misfires: a future honest experiment named `...-extend7` inside an
existing family would be swept. Mitigation is the manifest (§4), not a cleverer
regex.

## 2. What "deprecated" means

**A stamp, never an edit.** Add frontmatter only; never touch `next_edges`,
`parents`, `type`, or the body. Node count cannot drop (G7 invariant 1), and
undo is byte-exact.

The carrier is a real problem. `graph_core/node.py` defines `Node` with exactly
seven fields, and `loader.py::_node_from_frontmatter` maps only
id/type/payload_ref/parents/children/tags/origin. **`status:` is discarded at
load** — a `status: deprecated` field is invisible to every in-memory reader.
`tags` survives. So: write `status: deprecated` (for humans and `git grep`) and
a `deprecated` **tag** as the machine carrier, and — my judgement call, stated
as a deviation — add a first-class `deprecated: bool` to `Node` and the loader,
because a tag namespace anyone can collide with is a poor place to hang a
correctness filter.

Readers that must honour it, by file:
`bin/render-context.py` (`_count_descendants`, `idea_attract`),
`src/chain_engine/chains.py` (`find_chains` — it has `graph.get_node`, so it can
skip stamped ids while still walking disk `next_edges`),
`src/chain_engine/attractiveness.py` (`ChainMetrics.from_chain`, the `length`
term), `src/chain_engine/ranking.py`, `bin/dispatch.py` (`_descendant_count`),
`bin/metrics.py` (evidence counters).

## 3. Does it actually fix attractiveness? Partly — and not where TODO.md thinks

I checked before asserting, and the H3 residual looks misdiagnosed.
**58.5% of `parents` references in this corpus are dangling** (17,377 / 29,691):
padding says `parents: hypothesis:chain-engine-r1` while the real node is
`hyp:chain-engine-r1`. So the padding is already orphaned in the *spawns* graph
— which is why the top idea shows only **209** descendants, not thousands. By
contrast `next_edges` is intact: 5 dangling out of 19,617.

Consequences: (i) the descendant-count ranking in `INJECTION.md` — which
`SKILL.md` §82 says the CC runtime actually selects targets from — is *not*
meaningfully inflated by padding; deprecation will barely move it. (ii) The
`attractiveness_weights.length: 0.3` path runs through `ranking.py`, reachable
via `benchmark.py`, which **H4b says `driver.sh` invokes with the wrong
arguments under `|| true`** — so it may never have executed. The claim "target
selection keeps landing on padding" is therefore *itself* under-evidenced and
should be measured before it is treated as the justification.

What deprecation does unambiguously fix is the **evidence accounting**, which is
G6's actual currency.

## 4. Reversibility

Emit `context/deprecation-manifest.jsonl` — one line per stamped node: id,
predicate version, matched stem, `k`, timestamp. Undo is "remove the stamp for
ids in manifest vN". Re-running the predicate must be idempotent and must
*diff* against the manifest, never re-derive silently — H0e's lesson.

## 5. Falsifiers, pre-registered

- **F1 (must move):** `evidence_fraction` 0.197 → **~0.52**;
  `unevidenced_decisive_verdicts` 11,704 → **≤25**. If either barely moves, the
  readers ignored the stamp and this was cosmetic.
- **F2 (must NOT move):** `outcome_coverage` stays **0.202** — no mvp or
  hypothesis is touched. Movement means the predicate hit the wrong types.
- **F3:** three consecutive target selections land on non-deprecated nodes. If
  they still land on padding, §3's diagnosis is wrong.
- **F4:** if anyone later needs the `hops = 2N+8` stackability result and cannot
  reach it, precision failed — and the 142 preserved heads were the wrong hedge.