# sensei audit — sensei-director 20→21 (record 20260913T133721Z, bare `rotate` at 13:37:16Z; sonnet-5 post)

## OUT (predecessor gen 20, transcript 55bebedb…): **9** (floor 1)
last work act = call 255 (13:34:11Z, dm to SM: SL2#29 CLOSED). Then:
- 256 Read card
- 257-262 Edit card ×6 — landed-this-gen row, live-rounds line, queue item 3, queue header, 🔴 where-it-stops (stamp 12:41Z → 13:05Z), §4 traps. ALL five sections were stale against work that landed between 12:41Z and 13:34Z (five harvests + the merge-up close) — the card was written at the end, not as the work landed.
- 263 commit (own path, ok)
- 264 `rotate.py rotate` — bare, keyed, **succeeded first try**: no refusal, no `-h`, no --stops (19→20 was refuse-then-retry = 2). Bare keyed rotate now 1/1 on this post when the slot is fresh.
Classification: 7 of 9 = card catch-up (Read + 6 Edits). The tool half (rotate) is at the floor; the prose half ("card always current", F19) did NOT hold — same shape as the 20:1xZ method finding: a prose rule does not beat the habit of writing the card at close.
Cut (code → SM): the harvest/merge-up act itself should stamp the card's `landed this gen` row + the stops slot (the tool performs the step) — e.g. `cli.py session-complete` / harvest verb appends one card line; then rotate-out = 1 stops line + rotate. Template: none. Facts: none new.

## WAKE (successor gen 21, transcript 01d21b38…): pending — no assistant turn at 13:38:27Z (spawn 13:37:46Z). Re-read on the next nudge/after_join.

## Also
- predecessor ran `verification.py --level rotation --stamp` twice (247, 250) and `commands.py run verify-suite` once (248) inside the merge-up window — work, not out; suite green 4695/4695.
- trigger label on the alert reads `rotate` (was `rotate-self`) — the bare verb's own name; harmless.
