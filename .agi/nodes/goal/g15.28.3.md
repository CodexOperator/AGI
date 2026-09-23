---
id: goal:g15.28.3
mint_id: 6eda88f8403f475ca2948de50eed3dfd
type: goal
parents:
  - goal:g15.28
next_edges: []
confidence: 0.7
edited_by: director-engine
goal_id: G15.28.3
goal_kind: subgoal
heading_level: 5
origin: goals-doc
scaffold_hash: 45837b7b1956de04
season: 2
seeds:
  - hypothesis:the-grok-bot-build-node-has-one-live-id-and-true-prose
status: active
tags:
  - core
  - engine
  - residue-batch
  - leaf
title: "G15.28.3: THE GROK-BOT BUILD NODE HAS ONE LIVE ID AND TRUE PROSE (EF.53 mur residue leaf; assigned director-engine)"
town: core
---
# goal:g15.28.3

# goal:g15.28.3 — THE GROK-BOT BUILD NODE HAS ONE LIVE ID AND TRUE PROSE

```
leaf      execute EF.53's proposed dedupe (the a00 duplicate takes its own id, stops claiming the payload and is retired; mint kept)
          and correct the canonical's stale prose in place
source    R-EF53 verify (accept_with_residue): D1 the R14#3 record sits on the loader-hidden file · D2 "no committed reader flags
          duplicate ids" is false · D3 a stale payload hash/line count · D4 an experiment proved over its own partial probe ·
          MISSED: "the harnesses.grok-bot row is out of scope" while .agi/config.json:107 carries it
          bytes verified by director-engine 20:5xZ 09-23 on the post tip 102658116c: the loader's duplicate_ids = exactly this ONE
          id in 4144 nodes; stitch.py --verify duplicate_payload_ref = exactly this ONE payload
rule      KEEP SPLITTING (owner 09-23 10:4xZ, goal:g5): one leaf, one small round; split again if it grows
round     hypothesis:the-grok-bot-build-node-has-one-live-id-and-true-prose
writer    director-engine
```
