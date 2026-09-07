---
id: hypothesis:l3w4-masters-rollover
mint_id: 275b9de2e0a64367971f2523dacf22d8
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: belam-S1-L3-V
scaffold_hash: 3eceaf3a538134c7
season: 2
testable_claim: season.py judge and rollover gain --actor SEAT --session S (mirroring retag's existing flags) so each write's edited_by/thought_session equals the passed seat instead of the hardcoded season.py/season; rollover --name's season_names[1] = name (L880) is fixed to season_names[season] = name, the closing season's own key; and a rollover rehearsal that runs judge --actor glitch-master on the season's outcomes, judge --actor training-master on its bigger_outcomes and overviews (clearing _unjudged_overviews), and rollover --visions-from <dir> --name <summary> --branch --actor sanctuary-master to open season/s<N+1>, followed only by the prime's existing merge-up season/s<N> --target master, leaves grid.py diff ladder:ladder showing edited_by change seat by seat with no new frontmatter field added.
thought_session: L3.26
title: Hand season rollover to the Masters
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-masters-rollover

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## CLAIM

Rollover becomes a three-Master handoff: Glitch Master judges tier-0
outcomes as they land, Training Master judges tier-1 bigger_outcomes
mid-season and tier-2 overviews at close, naming the season, Sanctuary
Master runs `season.py rollover` to write that name and open
`season/s<N+1>`, and the prime only runs `merge-up
season/s<N> --target master`. `judge`/`rollover` gain `--actor SEAT
--session S` (mirroring `retag`), attributing writes to the seat, not the
hardcoded `season.py`/`season`; `rollover --name`'s
`season_names[1] = name` (L880) is fixed to `season_names[season] = name`.

## WHY

Owner (9): "the Bug Master could run the strict graph submission review
loops, and the Quality Master would do bigger-picture audits... work with
the Sanctuary Master to do season rollovers." Owner (10) renames Bug→Glitch
Master (Training Master per HANDOFF §6 item 24). Item 11: a season name is
"a one-line summary written at rollover." `[ladder].md` says `season_names`
is "written at rollover looking back" — never done; season 1 is the only
rollover so far.

## FILES

- extensions/agi/bin/season.py :: cmd_judge, cmd_rollover, _shell_out_write,
  season_names[1] (bug at L880), p_judge/p_rollover add_argument — EDIT
- extensions/agi/tests/test_season.py :: season-1 name/branch tests
  (unaffected) — NEW test added
- .agi/context/schemas/[ladder].md :: season_names comment — cited, unedited
- .agi/nodes/.geometry/ladder.md :: season_names, current_season — written
  only through the fixed command

## DESIGN

`judge`/`rollover` add `--actor SEAT --session S`, falling back to the
current literals when omitted. `cmd_judge` threads them into its one write;
`cmd_rollover` only into the ladder-bump write — `_mint_vision`'s
`edited_by: "owner"` is untouched.

Order (director proposal, owner names no tiers): (1) Glitch Master runs `judge
<outcome-id> --actor glitch-master` per tier-0 landing; (2) mid-season,
Training Master judges `bigger_outcome`s; at close she judges `overview`s
(`--actor training-master`), clearing `_unjudged_overviews`, and drafts the
name; (3) Sanctuary Master runs `rollover --visions-from <dir> --name "<name>"
--branch --actor sanctuary-master` — its checkout already moves
every seat sharing that tree (loop branches alone get a worktree); (4) the
prime runs the existing `merge-up season/s<N> --target master` once green.
No new field: `grid.py diff ladder:ladder` shows `edited_by` change seat by
seat.

## TESTS

Red-first: `test_second_rollover_names_its_own_season_and_attributes_each_write`
— rehearse 1→2 (`--name genesis --actor sanctuary-master`) then 2→3
(`--name wave-4-masters --actor sanctuary-master`); assert `season_names ==
{1: "genesis", 2: "wave-4-masters"}` (today: genesis clobbered) and the
season-2 version's `edited_by == "sanctuary-master"` (today: `season.py`).

## GATE

The named test fails on current `season.py`, passes once fixed. Season-1
tests stay green unmodified; suite green, 0 broken links.

## NOT IN SCOPE

Sanctuary Master's seat row / `rotate.py master` entrypoint
(`l3w4-sanctuary-master`); Glitch Master's seat row and review internals
(`l3w4-bug-master-seat`); Training Master's seat (`l3w4-training-master`); `judge
--quorum` tallying (`l3w4-quorum-reviews`); rotation alarms
(`l3w4-seat-rotation-loops`); merge-up internals (`l3w4-parent-branch-merge-up`, generic already).

## SOURCE

`.agi/context/l3-command-ladder-brief.md`, "Owner text 2026-09-07... to
Belam II after rotation", owner verbatim (9) and (10); `HANDOFF.md` §6 items
11 and 24.

OWNER QUOTE (12), 2026-09-07 ~17:55 UTC (verbatim in doc:l3-command-ladder-brief): the Training Master of quote (9) is renamed MASTER SENSEI — the one seat looking over the Masters themselves (the Sanctuary Master included); the Sanctuary Master owns seat assignments, model selection and seat-structure changes. Read "Training Master" in this body as Master Sensei; his brief is hypothesis:l3w4-master-sensei.
