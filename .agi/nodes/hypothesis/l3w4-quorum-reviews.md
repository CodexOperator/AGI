---
id: hypothesis:l3w4-quorum-reviews
mint_id: b6447de5e18b44baa29b5ea745b0f0ed
type: hypothesis
parents:
  - goal:g12.3
next_edges: []
edited_by: belam-S1-L3-VII
scaffold_hash: 73c514f060690437
season: 2
testable_claim: season.py judge --quorum, given three send.py vote posts in room tier3-quorum for one target and round, stamps alignment only on a 2-1 or 3-0 tally and otherwise (a genuine 1-1-1 split, or any --morals vote) calls send.py audience prime instead of stamping; send.py audience close then makes send.py prime-excluded true for that round; and send_dm plus a non-quorum audience prime call both refuse to reach the prime directly.
thought_session: 7af11157
title: Move review down to the quorum
---
<!-- BODY:BEGIN -->
# hypothesis:l3w4-quorum-reviews

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
## CLAIM

Advisors post one `aligned|adjust|unknown` vote per round into `tier3-quorum`
via `send.py vote`; `season.py judge --quorum` tallies the three,
stamping `alignment`/`adjust` on 3-0/2-1 (prime only `grid.py commit --all`)
or calling `send.py audience prime` on 1-1-1 or any `--morals` vote.
`audience close` then excludes Belam from further group traffic that round;
`send_dm` and a non-quorum `audience prime` refuse him too — the gap
`send_room` already closed for rooms.

## WHY

Trigger (owner): "...so Belam doesn't have to do reviews himself only help
decide things if the advisor quorum is deadlocked." Owner (2): "once quorum
finishes speaking to Belam, he exits the room and doesn't receive any other
group chats." Owner (4): "No directors get free comms to Belam, that always
goes through the quorum first. The quorum IS Belam to anyone else."
3-0/2-1/1-1-1 mechanics: Belam II's gloss (director proposal), not owner
text.

## FILES

- extensions/agi/bin/send.py :: `STANDING_ROOMS`, `PRIME`, `send_room`
  (refuses prime), `send_dm` (doesn't — the gap), `audience_prime`
- extensions/agi/bin/season.py :: `cmd_judge`, `_shell_out_write`
- extensions/agi/bin/brief.py :: `_advisor` duty 2/3 (audience rule + judge
  line)
- extensions/agi/bin/dispatch.py :: env `AGI_ROLE`, `AGI_LADDER_TIER`,
  `AGI_LOOP`
- .agi/context/schemas/[outcome].md, [bigger_outcome].md, [overview].md ::
  `alignment` enum
- extensions/agi/tests/test_send.py, test_season.py

## DESIGN

- `send.py vote --room R --target ID --vision V --alignment A [--morals]
  [--reason T]` (V = alive/all-is-one/self-perpetuating; `--round` defaults
  to `$AGI_LOOP`) posts a `VOTE` line via `send_room`; vision self-declared,
  not `--from` — sidesteps `l3-agent-id-never-exported`.
- `send.tally_votes(croot, room, target, round_)` groups by `vision`, last
  write wins, requires all 3 else ERR "incomplete quorum".
- `season.py judge <id> --quorum --room R [--round R2]` imports it: count≥2
  stamps `alignment`+`adjust` (voter `reason`) +`note`(room, tally); else,
  or any `morals=1`, shells `send.py audience prime --reason TEXT [--morals]`;
  `alignment` unset.
- `audience_prime` refuses unless `AGI_ROLE=parent`+`AGI_LADDER_TIER=3`, or
  `--morals` — quorum-only gate to Belam.
- `send.py audience close --round R2 [--decision A]` sets state
  `{opened,closed,decision}`, `exited.json[prime][R2]=true`.
- `send.py prime-excluded --round R2` (exit code) for a future alarm.
- `send_dm` refuses `other==prime` / `me==prime`, like `send_room`.

## TESTS

Red-first: `test_vote_posts_structured_line`,
`test_tally_votes_requires_all_three_visions`,
`test_judge_quorum_stamps_alignment_on_majority` (2-1,3-0),
`test_judge_quorum_deadlock_calls_audience_not_stamp`,
`test_judge_quorum_morals_forces_audience_despite_majority`,
`test_audience_prime_refuses_non_quorum_caller`,
`test_audience_prime_morals_bypasses_quorum_gate`,
`test_audience_close_sets_prime_excluded`, `test_dm_to_or_from_prime_refused`.

## GATE

Fixture: 2 aligned+1 adjust → `judge --quorum` stamps `alignment: aligned` +
note. A literal 1-1-1 calls `audience prime` instead,
`alignment` unset; `audience close` then makes `prime-excluded --round R2`
exit 0. `send.py send --to prime` and a bare non-tier3-parent `audience
prime` both refuse. Suite green, 0 broken links.

## NOT IN SCOPE

Seat registry/model table (`l3w4-seat-registry`); tty/remote-control
transport + tmux nudge (`l3w4-seat-transport`); the liaison seat
(`l3w4-liaison-seat`); rotation-loop alarms reading `prime-excluded`
(`l3w4-seat-rotation-loops`); the `doc` schema (`l3w4-context-doc-nodes`);
tier-0 director-vertical comms — no such seat yet (§1.9).

## SOURCE

`.agi/context/l3-command-ladder-brief.md`, section "Owner text 2026-09-07 …
the owner liaison" (trigger, quotes 2 and 4) and its "Director gloss (Belam
II, proposal)" paragraph "Quorum as reviewer".

RE-DISPATCH NOTE (Belam VII, 2026-09-07, for L3.30) — READ BEFORE YOU BUILD: the implementation is ALREADY ON DISK, landed in iter-L3.29 by kid a00-8c6043c1, which was killed by an OpenRouter sub-key 401 after it finished coding but before it wrote one line of its node (experiment:a00-8c6043c1-fc868a, left pending / evidence_runs 0 / status horizon; its THOUGHT has the full account). What exists: send.py has vote, _parse_vote, tally_votes, audience_close, prime_excluded and a _quorum_caller gate; season.py has its half; 549 insertions across those two modules and test_season.py plus test_send.py. The prime ran those four test files alone at 20:30 UTC and got 208 passed 0 failed. YOUR JOB IS NOT TO REBUILD IT. Read the diff first, then adversarially VERIFY it against this brief clause by clause: does the 3-0 and 2-1 stands rule hold, does 1-1-1 or a morals flag actually trigger send.py audience prime, is the prime genuinely inbox-only and does he actually exit the room when the quorum finishes speaking, does season.py judge consume the vote record, and does the collapsed-ladder comms rule hold that no director reaches Belam except through the quorum. Build ONLY what is missing or wrong, then write the verdict this round never got. If you find the implementation sound, say proved and cite the tests you re-ran yourself - a verdict you did not personally re-run is an overclaim (trap 0g runs the other way here: the risk is rubber-stamping, not probing).
