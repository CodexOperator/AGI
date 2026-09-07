---
id: hyp:zoom-encoded-node-ids
mint_id: 6817edbfb91641baa4900b41f970be74
type: hypothesis
parents:
  - goal:g2.5
confidence: 0.6
edited_by: season.py
season: 1
tags:
  - g2.5
thought_session: season
title: Hierarchical zoom-encoded node ids make collisions structurally impossible
---
> ⚠️ **This hypothesis states the superseded reading of G2.5.** It was written
> against a *lineage* model — an id built up from its parent's id as the graph
> grows. G2.5 was corrected on 2026-08-24 to an *address* model: every real
> node carries a fixed 7-character id, ids never grow, and a supernode is a
> renderer-side grouping named by a shared prefix and chosen by tag (G2.6), not
> a parent node. Kept as prior art because its falsifier was genuinely run and
> the number it produced is real; superseded as a description of the design.
> The corresponding claim under the address model — that no tag-derived group
> exceeds one character's worth of members — is unstated and unmeasured here.

**Claim (as originally stated, now superseded).** If every node id is its
parent's id plus exactly one additional alphanumeric character identifying it
among its siblings (coarsest level 5 characters, +1 per level, level 3 = 7
characters), then sibling-local uniqueness is sufficient for global uniqueness,
and truncating an id to N characters always yields the id of its correct
ancestor at that zoom level. No separate collision resolver (`:2` suffixes,
"kept X, hidden Y" warnings) is ever needed.

**What survives the correction.** The *truncation* property and the
*no-collision-resolver* property are both still targets under the address
model — they were never lineage-specific. What does not survive is the premise
that ids accumulate characters as the graph deepens, and with it the reading of
"siblings" as "children of a parent node" rather than "members of a shared
prefix".

**Named precondition — the fan-out budget.** One alphanumeric character is
36 distinct values case-insensitively (`0-9a-z`) or 62 case-sensitively
(`0-9A-Za-z`). The one-char-per-level rule is only well-formed if **no node
in the real corpus needs more siblings than that** — every parent must be
able to mint a unique single character for each of its children. This is a
necessary, not sufficient, condition: it says nothing about migration,
history preservation, or whether truncation holds once the scheme is
actually implemented.

**Falsifiable form.** The hypothesis is disproved on this precondition if
any node currently has more than 36 children (fails even the lenient
case-sensitive budget of 62 would be a harder failure). It is supported on
this precondition if the corpus-wide max fan-out is <= 36.

**What would disprove it (full hypothesis, beyond this precondition):** a
migration that cannot preserve `refs/grid/node/*` history; a truncation
that does not land on the literal ancestor id once nodes are renumbered;
sibling-local uniqueness enforcement that turns out to require the same
kind of global check it was meant to eliminate (e.g. two same-parent
inserts racing for the same character). None of those are tested here —
see `exp:id-fanout-budget` and its verdict for what this iteration actually
measured.