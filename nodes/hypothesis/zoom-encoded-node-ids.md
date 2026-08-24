---
confidence: 0.6
id: "hyp:zoom-encoded-node-ids"
parents:
  - goal:g2.5
type: hypothesis
title: "Hierarchical zoom-encoded node ids make collisions structurally impossible"
tags: [g2.5]
---

**Claim.** If every node id is its parent's id plus exactly one additional
alphanumeric character identifying it among its siblings (coarsest level 5
characters, +1 per level, level 3 = 7 characters), then sibling-local
uniqueness is sufficient for global uniqueness, and truncating an id to N
characters always yields the id of its correct ancestor at that zoom level.
No separate collision resolver (`:2` suffixes, "kept X, hidden Y" warnings)
is ever needed.

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
