---
id: hypothesis:brief-py-assembles-every-first-turn-from-config
mint_id: dbd43192490d42308272aec89befb9af
type: hypothesis
parents:
  - goal:g1.9
next_edges: []
assigned: "director-engine (the Prime 09-23; owner 08:4xZ, goal:g5): priority next after the live EF rounds; build loop; one [merge-up] to thought-master; retiring HANDOFF.md, CLAUDE.md and the 5 INJECTION.md writers = the follow-up once this lands."
ceiling: 3.5 USD, <= 5 kids, pi parents (raised from 2 USD / <= 3 kids by the owner, director-engine pane 09:4xZ 09-23)
edited_by: director-engine
scaffold_hash: 1a7272e3789a7cbf
season: 2
tags:
  - brief
  - head
  - card
  - injection
  - formation
testable_claim: "brief.py render returns the whole first user turn for any role (Prime, master, director, parent, kid) assembled from config — head (doc:unified-head, byte-identical across roles) + the role template (chosen by config: the post row cell, else the formation default) + card + harness block + the town trajectory for masters — and writes no injection file; rotate.py, dispatch.py and the SessionStart hook all call it."
thought_session: belam-S2-L5-I
title: brief.py assembles every first turn from config — head + card (+ harness block, + trajectory for masters), one pattern for every role, typed straight into the turn, no injection file
town: local-maxxing
---
# hypothesis:brief-py-assembles-every-first-turn-from-config

# brief.py assembles every first turn from config — head + card (+ harness block), one pattern for every role, typed straight into the turn, no injection file

**Owner 2026-09-23 08:4xZ (Prime pane, filed on `goal:g5`):** "Could we not just let brief.py do the task of assembly and autoinjextion for us as is just update it to be configurable and templatable via code update" then "But instead of using injection Md just use the other docs we just discussed instead via config for brief" then (08:5xZ) "By saying cards point at templates, will template text dynamically populate into the first turn via brief.py that reads said template? I figured it doesn’t even need that just the fact that the post IS a director is enough to assign it the right template. More like the post pin or whatever config needs to have a way to set which template to run with a default available depending on post in .geometry formation." The model it serves (owner 08:2xZ, `goal:g5`; `doc:s3-plan` HEAD 1.5 doc half): 3 docs per role — HEAD (`doc:unified-head`, the same bytes for every role incl. parents and kids) · CARD (one per post, derived from a class template) · TOWN TRAJECTORY; nothing rendered into an injection md; HANDOFF and CLAUDE.md retired (CLAUDE.md content → the claude-code harness block).

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
                                               template  the ROLE's template, chosen by config: the post row's template cell, else the formation default for its role (director → doc:unified-director-brief · master → doc:unified-master-brief · prime_director → build:briefs-prime-director-successor; thought-master's row says director, so its row cell names the master template) — NOT a line in the card (owner 08:5xZ)
                                               card    the post's card = a doc node, doc:card-<post> (owner 09-23; its own loop + live scratch; .agi/sessions/quorum/<post>.md is a symlink to its file during the move — doc:card-belam first)
                                               harness claude-code: the block that replaces CLAUDE.md · pi: none unless configured
                                               trajectory  the town trajectory (town:<town> trajectory_standin today) — masters by default, any role by config
                                               extras  parent/kid: the dispatch brief
INJECTION.md  its content is REPLACED by these same parts through the brief config (owner 08:4xZ) — the SessionStart hook renders them straight into the turn
callers  rotate.py · dispatch.py · the SessionStart hook ─▶ the same render · the head byte-identical across every role
```

## Dispatch line
config-max: the parts list per role and harness, one cell / template-max: head, card and templates stay in nodes and files, filled by placeholder / code: the part resolver (post → row → role → template) in brief.py, and the three call sites switched to it

## FALSIFIERS
- the head bytes differ between any two roles (Prime · master · director · parent · kid) at one SHA
- adding or removing a part needs a code change instead of one config line
- a render writes INJECTION.md or any other injection cache file
- a rotated successor's first turn lacks the head or its card (director and Prime fixtures)

## TESTS
- head byte-identical across the 5 roles at one SHA · a config line adds/removes a part · the template resolves by role (a row cell overrides the formation default) and refuses a missing node · no file written by a render (tmp root) · rotate successor prompt = head + card for a director and for the Prime
- neighbourhoods: rotate `test_rotate*.py test_session_start_bootstrap.py test_session_start_seat_pre_spawn.py test_bin_help_smoke.py` · `test_brief*.py` · `test_dispatch.py`

## FILE SCOPE
brief.py (resolver) · rotate.py, dispatch.py, hooks/cc-session-start.sh (call sites only) · the config cells (the parts list; a template cell on config:posts rows + the per-role default in the formation) · the prime_director template: the [handoff-head] first_turn entry → the card (HANDOFF.md is a symlink to it since 09-23) · tests. NOT this round: retiring HANDOFF.md, CLAUDE.md or the 5 INJECTION.md writers — the follow-up once this lands.

## CEILING
<= 3 kids · 10-12 production lines per conjunct · pi parents · 2 USD

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
ceiling raised 2 USD / <= 3 kids -> 3.5 USD / <= 5 kids. OWNER 09:4xZ 09-23 in the director-engine pane, verbatim: 'Go for finish. Raise ceiling or lower floor to something silly like -50 just whatever needed to keep working as balance allows.' (the previous version of this cell said 10:2xZ: a wrong time label, corrected from the applying commit at 09:48Z). Three kids built the template-by-role half (EF.18 x2, EF.19); the unbuilt half (dispatch.py on render, the Prime spawn path and its handoff-head entry, the master default, doc:card-<post> cards) is phase 4 (EF.25). The account floor needed no change: provisioning.min_account_remaining_usd is already -100.
<!-- THOUGHT:END -->

## Agent Notes
director-engine 10:1xZ 09-23: 3 of the <= 3 kids used (EF.18 a00-15fc3737 + a00-3ca5e37d on the pre-amendment spec; EF.19 a00-ea8aa887 on the amended one). BUILT and merged on the director-engine post branch: brief.render from the committable config:brief node, template by role (a config:posts row cell beats templates[role]; a missing node refused by name), card = data, head one md5 across the 5 roles, no file written, rotate.py director successors + the SessionStart hook on render. NOT BUILT: dispatch.py parent/kid briefs (still brief.assemble, dispatch.py:1365) · the Prime spawn path (rotate.py ~1866) and the handoff-head first_turn entry (rotations.md:116 still reads build:HANDOFF.md) · templates.master still doc:unified-director-brief though doc:unified-master-brief now exists · cards still read .agi/sessions/quorum/<post>.md (belam's is a symlink to doc:card-belam). MEASURED: a director render is 56 KB, 26.6 KB of it the claude-code harness block = CLAUDE.md, which claude-code also loads itself (a duplicate until CLAUDE.md is retired). BANKED for the Prime (not messaged: the Prime is idling on the owner's word): a phase 4 for the unbuilt half needs 1-2 more kids / about 1 USD over this node's ceiling -- raise it here (recommended), mint phase 4 as its own node, or leave it to the retirement follow-up.
