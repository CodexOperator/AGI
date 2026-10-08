---
id: hypothesis:send-read-reads-dms-from-the-graph
mint_id: c6070d6e2d074cb78892e962cd3ff4e2
type: hypothesis
parents:
  - goal:g15
next_edges: []
assigned: "director-engine (the Prime 09-23; owner 14:5xZ, goal:g5): after the harness-paths round; build loop; one [merge-up] to thought-master."
ceiling: 1 USD, <= 2 kids, pi parents
edited_by: belam
scaffold_hash: 13ea89bf5d319efd
season: 2
tags:
  - send
  - quiet
  - inbox
testable_claim: send.py read <post> lists every dm addressed to the post in the graph dm logs since its last read, whatever the row quiet setting; quiet changes nudges only.
thought_session: belam-S2-L5-I
title: send.py read lists a posts dms straight from the graph dm logs — quiet governs nudges only, never what read shows
town: local-maxxing
---
# hypothesis:send-read-reads-dms-from-the-graph

# send.py read reads a post's dms straight from the graph — a quiet row never misses one

**Owner 2026-09-23 14:5xZ (Prime pane, verbatim on `goal:g5`):** "Oh inbox is empty due to quiet mode. I think we over-silenced the quiet mode. I think it needs a direct graph read via read or render might be better"

**Assigned: director-engine** (the Prime, 09-23) · build loop · after the harness-paths round · one `[merge-up]` to thought-master.

## Measured (the Prime, 14:5xZ)
```
quiet row   send.py:1577 `quiet` = "still WRITES the dm but types no nudge" — yet `send.py read belam` printed "inbox for belam: empty"
graph       .agi/comms/season-2/dm/*belam*.md held two [decision] dms from director-engine (07:58Z, 11:14Z) the Prime never saw
stopgap     the belam row now says quiet-system (post dms nudge; service-class stays silent)
```

## CLAIM
`send.py read <post>` lists every dm addressed to the post from the dm logs in the graph (unread since its last read), whatever the row's quiet setting; quiet governs nudges only, never what `read` shows.

## FALSIFIERS
- a dm in a `*--<post>.md` log addressed to the post, newer than its last read, is missing from `send.py read <post>`
- a quiet row's read differs from a non-quiet row's read for the same logs

## TESTS
- tmp graph: dms to a quiet row and a normal row → both listed by read; the read marker advances; nudges still follow quiet
- neighbourhood: `test_send.py test_seatsig.py test_bin_help_smoke.py`

## FILE SCOPE
extensions/agi/bin/send.py (read) · tests.

## CEILING
<= 2 kids · 10-12 production lines per conjunct · pi parents · 1 USD
