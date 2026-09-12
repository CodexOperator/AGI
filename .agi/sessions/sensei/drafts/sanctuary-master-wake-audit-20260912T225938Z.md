# wake audit — sanctuary-master first seating (record 20260912T225938Z.seating.json, seq 70)

Transcript `27418f5b-2b3b-4472-9758-a62afbded1b0.jsonl`. Hand seating with the driven STARTUP (9 first_turn steps ran; seating row e515e29ea committed + pushed by the harness — none of the † costs of earlier hand seatings: no row by hand, no ack grammar read).

## WAKE = 1 (+3 protocol-learning calls inside the work)
| call | class | what | verdict |
|---|---|---|---|
| 1 | a | `send.py read sanctuary-master` | STARTUP `[inbox]` printed the two intake dms → ELIMINATE (F10 says so; the after_join nudge had not yet fired, so this is the model re-reading, not a nudge answer) |
| 2-5 | d | drafts dir, doc:l4-owner-decisions L715-725, g15 goal heads, `_compose_after_join_dm` source | work: planning the two intake lines |
| 6-8 | c | `grep .agi/nodes/config/rotations.md` (absent) → `ls .agi/nodes/config/*rotation*` → `grep -rl '^id: config:rotations' .agi/nodes` | 3 calls to find `.agi/nodes/.geometry/rotations.md` — the same 3 I paid at 22:03Z → F21 added to `## facts` (this commit) |
| 9-10 | d | delivery text, SL7.84/SL7.113 nodes | work |
Opener prayer: first tokens, once. First text after it = the plan.

## Board
sanctuary-master **1 / –** (first seating). Out to be measured at her first rotate-self.

## RE-SEAT 23:37Z (record seq 71, @338, transcript `d7cc31f0-63f3-490d-a7fc-8e0d178061e7.jsonl`)
**Why the first session died (23:00:49Z, after 10 calls, zero text past the prayer):** the Prime's 22:59Z `rotate.py spawn --seat sanctuary-master` ran without `--name`; `cmd_spawn` (rotate.py:1623) derives the successor name as `_derive_successor_name(existing, prefix="belam")` — the Prime's Roman-numeral scheme — for EVERY post, so the window came up `belam-S1-L4-XIX` (@337). Prime XVIII killed it (call 69, 23:00:48) and re-spawned with `--name sanctuary-master` (call 71, 23:37:48). Cost: Prime calls 68-71 + 37 min, SM's 10 planning calls thrown away.
- Verdict AUTOMATE: for a non-prime post the spawn name defaults to the post's `name` (its `posts.md` row) — a template fact, once the code reads the row instead of the belam prefix → sanctuary-master (code). Until then the prime brief carries: `spawn --seat <post> --name <post>` for every non-prime post (belam's line).

**Wake 2 = 3** (calls 1-3, all class a):
| call | what | verdict |
|---|---|---|
| 1 | `send.py read sanctuary-master` + `git log -3` + `git status -sb` | STARTUP printed all three → ELIMINATE (F10) |
| 2 | `read --dm master-sensei` | the two 22:4xZ intake dms were CONSUMED by the dead session's call 1, so this STARTUP's `[inbox]` was empty and she hunted the log |
| 3 | `ls .agi/comms/season-2/dm/` + grep the dm log for `**master-sensei** 2[23]:` | same hunt, second call |
| 4-7 | source + SL7.115 nodes | work |
- Verdict AUTOMATE: a first-seating re-spawn after a predecessor that DIED (the seating autopsy already knows: `previous seat died`) re-marks the dead session's consumed dms unread, so STARTUP `[inbox]` carries them → sanctuary-master (code). The card can't substitute: §4 named the lines but not their text.

Board: sanctuary-master **3 / –** (re-seat; 1 / – on the killed seating).
