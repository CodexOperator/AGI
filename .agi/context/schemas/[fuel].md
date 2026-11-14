---
name: fuel
derived_from: owner-approved 2026-11-09 (belam's [note] 19:5xZ 11-09, relaying the owner's chat to belam); placement option B smallest (self-perpetuating 19:55:55Z, all-is-one 19:56:47Z, alive); 2 prior fuel nodes, both typed idea
fields:
  title: {type: str}       # starts "FUEL"
  status: {type: str}      # open | extended | abandoned | deprecated
  parents: {type: list}    # goal or vision ids: what the musing would feed
  next_edges: {type: list}
  tags: {type: list}       # e.g. season-4: the season it is kept for
  season: {type: int}
validation:
  required: [id, type, mint_id, title, status, parents, tags]
  types:
    title: str
    status: str
    parents: list
    tags: list
  regex:
    title: '^FUEL.*$'
    status: '^(open|extended|abandoned|deprecated)$'
---

# fuel

Owner-sparked musing kept for a later season: raw material for brainstorming, **never a plan or an order**. A goal,
idea or hypothesis may later take one up; until then it waits.

ID prefix: `fuel:<short-slug>` (e.g. `fuel:s4-retire-the-python-engine`).

## Spawn rule — what it would feed
`allowed_parents: [goal, vision]`, `min_parents: 1`, `max_parents: 2`. The parent names what the musing would feed:
a goal (a season's bundle, an area) or a vision (a value it serves). The two fuel nodes before this type were
ideas under `vision:the-living-being` and `goal:g5.4`; no other parent type has been used.

## Status — three live states
- `open`: waiting.
- `extended`: a goal, idea or hypothesis took it up; that node names this one in its parents or body.
- `abandoned`: the owner dropped it. (`deprecated` only with the move to `deprecated/fuel/`: retire, never delete.)

## Body — the owner's spark, then the counted, then the musing
1. At least one `## OWNER <time> (c:<12 hex>)` block: the owner's words that sparked it, verbatim. Under the interim
   rule (self-perpetuating 19:55:55Z 11-09) the chunk must be in belam's store, until the cite leaf under
   goal:g7.16.1.11.46 lands; words given elsewhere go under a plain heading, their chunk id named in the text.
2. What was measured, with its source command or node, in a section of its own.
3. The musing, in a separate section: a reader must tell what was counted from what is a direction.

TYPE CLOSED 2026-11-14 (fuel fold, owner 16:2xZ 11-14 via belam, council 3/3 16:20Z; L569 + L570): fuel lives in the town board node, one '## Fuel' section per board, one block per post; no fuel node can be minted (growth.tsv has no fuel row, and this schema's spawn: block is removed, so grow-project projects none back and spawn_gate reports no spawn block; the 'Spawn rule' section below is history) and both fuel nodes are retired under deprecated/. This schema stays only as the retired nodes' reader; it is retired itself once a fixture shows verify, links.py and the schema readers green with deprecated/fuel/ present and no schema.
