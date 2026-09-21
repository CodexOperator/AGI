---
id: verdict:zoom-encoded-node-ids
mint_id: 57859600bb8d41c1b17f0af9f976fb0b
type: verdict
parents:
  - exp:id-fanout-budget
confidence: 0.9
contradicts: []
edited_by: season.py
evidence_runs:
  - exp:id-fanout-budget
season: 1
supports:
  - hyp:zoom-encoded-node-ids
tags:
  - g2.5
thought_session: season
title: "Verdict: fan-out budget for zoom-encoded ids"
verdict: proved
---
> ⚠️ **Superseding note added on review, 2026-08-24 — read this before citing
> this verdict.** G2.5 was rewritten after this measurement to the *address*
> model: ids are fixed-width 7-character hierarchical addresses, and a
> supernode is a renderer-side grouping named by a shared **prefix**, not a
> parent node. Under that model the binding capacity number is **members per
> shared prefix**, which is determined by the tag taxonomy (G2.6). This
> experiment measured **children per parent by the `parents:` field**, which is
> a different quantity. Everything below remains true *as a statement about
> lineage fan-out* and is kept as prior art, but it is **not** evidence for
> G2.5's capacity claim as that goal now reads. The re-registered falsifier —
> max members per tag-derived group — is unrun. Do not let the `proved` in this
> node's frontmatter carry weight it did not earn: the claim it proves is the
> one stated in the next paragraph, and that claim is now a side fact rather
> than a precondition of the live design.

**Scope of this verdict: the fan-out-budget precondition only, not G2.5 as
a whole.** `exp:id-fanout-budget` measured one falsifiable claim: does any
node in the real corpus need more than 36 (or 62) single-character sibling
slots? It did not measure, and this verdict does not claim, that the
one-char-per-level scheme works end to end.

**The precondition holds, decisively.** Corpus-wide max fan-out is **20**
children, on `idea:engine-graph-core` — 55% of the strict 36-value budget
and 32% of the lenient 62-value budget. Zero parents (of 333 with any
children at all) exceed 36; zero exceed 62. Restricted to the level-3
layer specifically — 181 nodes, 58 census parents, the layer G2.5 pins at
7 characters and calls out by name as the known-large-fan-out case — the
same node is still the worst offender at 20, and the same "zero exceed
36/62" result holds. The claimed falsifier did not fire. The fixed
one-char-per-level rule survives this corpus with more than 1.8x headroom
on the tight budget.

**What this proves:** the *necessary precondition* for the scheme as
specified — that a single alphanumeric character is enough to distinguish
every current sibling set — is true today, by a wide margin, at both the
whole-corpus level and the level-3 layer G2.5 specifically flagged as
risk.

**What this does not prove, named explicitly per the evidence-gate
instructions so no downstream reader overclaims from this node:**
- **Not proved:** that migration can preserve `refs/grid/node/*` history
  under a wholesale id rewrite (G2.5's own "sequencing note" — untested
  here).
- **Not proved:** that truncating a new-scheme id to N characters actually
  yields the correct ancestor id once nodes are renumbered — this
  experiment measured the *old* ids' parent/child relation, not a
  new-scheme id in the wild.
- **Not proved:** that sibling-local uniqueness enforcement at write time
  is itself simple/race-free — a headroom of 20-of-36 today says nothing
  about the concurrency behavior of two kids minting a child under the
  same parent simultaneously.
- **Not proved:** that 36 (or 62) will keep holding as the corpus grows.
  This is a snapshot verdict on 828 files dated 2026-08-24. `idea:
  engine-graph-core` at 20/36 has less headroom than the median parent
  (which has 1); if that specific node's growth rate continues it is the
  first place to watch, not because it is close to the budget today but
  because it is the corpus's own historical outlier by a wide margin (next
  is 19, then a drop to 16).
- **Not evaluated:** the UUID alternative on any axis other than length.
  Recorded for that future decision, not adjudicated here: current ids
  span 7-88 characters (median 27, mean 26.7); a flat 36-char UUID would
  be shorter than today's worst level3 ids but longer than every goal/idea
  id, and (unlike either current short ids or the proposed scheme) carries
  no truncate-to-ancestor property at all.

**Corpus-hygiene finding, incidental to the measurement, worth flagging
separately:** 17 node ids are each duplicated across two files on disk
(e.g. `exp:graph-core-r1`, `verdict:session-management-r1`), and 20 ids
named in some node's `parents:` field do not resolve to any file in the
corpus. Both are consistent with — and independent evidence for — the
loader-hiding-files problem G2.5 already cites (G7.2) as motivation for
this whole goal. Not fixed here; this verdict's measurement counted every
file on disk regardless, so the fan-out numbers above are an upper bound
relative to what any single live loader currently sees, which only
strengthens (never weakens) the "budget holds" conclusion.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Converted `evidence_runs: 1` to name `exp:id-fanout-budget` (goal:g7.3).

This node was the single most severe instance of G7.3's hole: `proved`, and
decisive *only* because `normalize_evidence_runs` returned an unchecked `1`.
Once bare integers stopped counting it became the corpus's one
`unevidenced_decisive_verdict`.

Demoting it would have been wrong. The evidence is real and was never missing
— it was merely unnamed. This node's own `parents:` lists exactly one node,
`exp:id-fanout-budget`, which exists, and a verdict's parent experiment is its
backing run. So naming it is reading the node's own frontmatter, not inventing
a citation.

That is why the other eleven bare-int nodes were left alone: they are all
`exp:` nodes carrying no verdict, and their parents are goals and hypotheses
rather than experiments. For those, picking a reference genuinely would be
invention, and G7.3 says so explicitly. They cost nothing, because with no
verdict they cannot be decisive.

Note the separate, older caveat above this line: the superseding note from
2026-08-24 says G2.5 was rewritten to the address model and this experiment
measured a different quantity. That remains true and untouched. This change is
about how the evidence is cited, not about whether the claim still holds.
<!-- THOUGHT:END -->