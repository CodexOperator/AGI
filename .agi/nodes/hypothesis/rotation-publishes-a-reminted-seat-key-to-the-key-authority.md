---
id: hypothesis:rotation-publishes-a-reminted-seat-key-to-the-key-authority
mint_id: 4fab3abb6c674581a5d7531b035e4f90
type: hypothesis
parents:
  - goal:g15
next_edges: []
assigned: "director-engine (the Prime 09-23; owner 09:4xZ, goal:g5): priority FIRST, ahead of the brief.py round; build loop; one [merge-up] to thought-master; option B unless the owner picks A."
ceiling: 1 USD, <= 2 kids, pi parents
edited_by: belam
scaffold_hash: 528c8cc427c25e08
season: 2
tags:
  - seat-key
  - rotation
  - send
  - config-max
testable_claim: "After a rotation on a town trunk re-mints a seat key, send.py whois --key <the new pubkey> --claim <post> reads IS-AUTHORIZED at once: the authority ref is one config cell (default origin/season2/main, behaviour unchanged) and the re-key step publishes the one seat row to it."
thought_session: belam-S2-L5-I
title: A re-minted seat key reaches the key authority at rotation — the authority ref one config cell (default origin/season2/main); no post reads UNVERIFIED after it rotates
town: local-maxxing
---
# hypothesis:rotation-publishes-a-reminted-seat-key-to-the-key-authority

# A re-minted seat key reaches the key authority at rotation — no post's dms read UNVERIFIED after it rotates

**Owner 2026-09-23 09:2xZ-09:4xZ (Prime pane, verbatim on `goal:g5`):** "Your key is failing" then "Your best key only" then "Seat" then "Do the config cell".

**Assigned: director-engine** (the Prime, 09-23) · build loop · priority FIRST, ahead of the brief.py round (it breaks comms at every rotation on a town trunk) · one `[merge-up]` to thought-master.

## Measured (the Prime, 09-23, this tree)
```
authority  send.py verifies seat keys against _PUSHED_SEATS = "origin/" + branches.season_main(2) = origin/season2/main
           — a hardcoded default (send.py:4307; whois `source` default), no config cell
rotation   re-mints the seat key and commits + pushes the new pubkey row to the CHECKED-OUT branch (here: the town trunk)
gap        season2/main gets the row only at the next Prime merge pass → the post's dms read UNVERIFIED until then
hit 09-23  belam (07:54 re-key → fixed by hand 7e134ba7b) · thought-master (07:52 re-key → fixed by hand ed54be7d8)
           = every post on a town trunk, at every rotation
```

## CLAIM
(1) the authority ref is ONE config cell (config-max), default `origin/season2/main`, so today's behaviour is byte-identical; (2) a rotation that re-mints a seat key publishes the new pubkey row to that authority ref in the same step (a one-row commit + push on the authority branch), so the successor's first dm verifies.

## Options (the owner's call; the Prime recommends B)
```
A  point the cell at the town trunk on this box — no rotation change, but the trunk (where town posts commit) becomes the key authority: weaker than the Prime-reviewed root
B  keep the reviewed root as the authority; publish the one seat row there at rotation — what 7e134ba7b / ed54be7d8 did by hand
```

## Dispatch line
config-max: the authority ref as one cell / template-max: none / code: send.py reads the cell; rotate.py's re-key path publishes the one row to it

## FALSIFIERS
- after a rotation on a town trunk, `send.py whois --key <the new pubkey> --claim <post>` reads anything but IS-AUTHORIZED
- the authority ref is still a literal in send.py
- the publish step writes anything but the one seat row

## TESTS
- a tmp repo with a root branch and a town trunk: a re-key on the trunk → the root carries the new row → a signed dm verifies · the cell's default leaves today's behaviour byte-identical
- neighbourhood: `test_send.py test_seatsig.py test_rotate*.py test_bin_help_smoke.py`

## FILE SCOPE
extensions/agi/bin/send.py (the ref) · extensions/agi/bin/rotate.py (the re-key publish step) · .agi/config.json (the cell) · tests. Nothing else.

## CEILING
<= 2 kids · 10-12 production lines per conjunct · pi parents · 1 USD
