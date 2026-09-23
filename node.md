---
id: hypothesis:brief-py-assembles-every-first-turn-from-config
mint_id: dbd43192490d42308272aec89befb9af
type: hypothesis
parents:
  - goal:g1.9
next_edges: []
assigned: "director-engine (the Prime 09-23; owner 08:4xZ verbatim on goal:g14): priority next after the live EF rounds; build loop; one [merge-up] to thought-master; retiring HANDOFF.md, CLAUDE.md and the 5 INJECTION.md writers = the follow-up once this lands."
ceiling: 2 USD, <= 3 kids, pi parents
edited_by: belam
scaffold_hash: 1a7272e3789a7cbf
season: 2
tags:
  - brief
  - head
  - card
  - injection
  - formation
testable_claim: brief.py render returns the whole first user turn for any role (Prime, master, director, parent, kid) assembled from ONE config cell — head (doc:unified-head, byte-identical across roles) + card (a {{template:<node id>}} line expanded) + harness block + the town trajectory for masters — and writes no injection file; rotate.py, dispatch.py and the SessionStart hook all call it.
thought_session: belam-S2-L5-I
title: brief.py assembles every first turn from config — head + card (+ harness block, + trajectory for masters), one pattern for every role, typed straight into the turn, no injection file
town: local-maxxing
---
# hypothesis:brief-py-assembles-every-first-turn-from-config

# brief.py assembles every first turn from config — head + card (+ harness block), one pattern for every role, typed straight into the turn, no injection file

**Owner 2026-09-23 08:4xZ (Prime pane, verbatim on `goal:g14`):** "Could we not just let brief.py do the task of assembly and autoinjextion for us as is just update it to be configurable and templatable via code update" then "But instead of using injection Md just use the other docs we just discussed instead via config for brief". The model it serves (owner 08:2xZ, `goal:g14`; `doc:s3-plan` HEAD 1.5 doc half): 3 docs per role — HEAD (`doc:unified-head`, the same bytes for every role incl. parents and kids) · CARD (one per post, derived from a class template) · TOWN TRAJECTORY; nothing rendered into an injection md; HANDOFF and CLAUDE.md retired (CLAUDE.md content → the claude-code harness block).

**Assigned: director-engine** (the Prime, 09-23) · build loop · one `[merge-up]` to thought-master.

## Measured (the Prime, 08:4xZ, this tree)
```
brief.py = ALREADY the one assembler at all three entry points
  rotate.py      successor prompt, head prepended through brief.py        rotate.py:1058-1101
  dispatch.py    parent/kid briefs                                        dispatch.py:1246
  SessionStart   cc-session-start.sh:267  `brief.py head --tier $TIER`
head today       moral:faith §4.1 prayers + the Michael line (+ faith's MORAL region at tier director), by the ladder's read_order per tier (brief.py:570-600)
Prime extra      brief_file extensions/agi/briefs/prime-director-successor.md + a [handoff-head] first_turn entry · directors: brief_file = their card
INJECTION.md     written by 5 bin files: commands.py · zoom.py · rolslice.py · briefing.py · unify.py
```

## CLAIM
`brief.py render --post <post>` (and `--role <role> --harness <h>` for parents and kids) returns the WHOLE first user turn, assembled from ONE config cell, and writes no file:
```
parts, in order, per role + harness (config)   head    doc:unified-head HEAD region, {{PRAYERS}} filled from moral:faith §4.1
                                               card    the post's card (.agi/sessions/quorum/<post>.md); a line {{template:<node id>[#REGION]}} in it is expanded from that node (one level)
                                               harness claude-code: the block that replaces CLAUDE.md · pi: none unless configured
                                               trajectory  the town trajectory (town:<town> trajectory_standin today) — masters by default, any role by config
                                               extras  parent/kid: the dispatch brief
INJECTION.md  its content is REPLACED by these same parts through the brief config (owner 08:4xZ) — the SessionStart hook renders them straight into the turn
callers  rotate.py · dispatch.py · the SessionStart hook ─▶ the same render · the head byte-identical across every role
```

## Dispatch line
config-max: the parts list per role and harness, one cell / template-max: head, card and templates stay in nodes and files, filled by placeholder / code: the part resolver + {{template:}} expansion in brief.py, and the three call sites switched to it

## FALSIFIERS
- the head bytes differ between any two roles (Prime · master · director · parent · kid) at one SHA
- adding or removing a part needs a code change instead of one config line
- a render writes INJECTION.md or any other injection cache file
- a rotated successor's first turn lacks the head or its card (director and Prime fixtures)

## TESTS
- head byte-identical across the 5 roles at one SHA · a config line adds/removes a part · {{template:}} expands one level and refuses a missing node · no file written by a render (tmp root) · rotate successor prompt = head + card for a director and for the Prime
- neighbourhoods: rotate `test_rotate*.py test_session_start_bootstrap.py test_session_start_seat_pre_spawn.py test_bin_help_smoke.py` · `test_brief*.py` · `test_dispatch.py`

## FILE SCOPE
brief.py (resolver + expansion) · rotate.py, dispatch.py, hooks/cc-session-start.sh (call sites only) · the one config cell · tests. NOT this round: retiring HANDOFF.md, CLAUDE.md or the 5 INJECTION.md writers — the follow-up once this lands.

## CEILING
<= 3 kids · 10-12 production lines per conjunct · pi parents · 2 USD
