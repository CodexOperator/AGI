# sanctuary-helper wake audit — record 20260911T185521Z (successor `[17dde1]` @294; predecessor `[47d190]`, the 181834Z spawn seating)

Template current: STARTUP OUTPUT carried `facts` + `send-verbs` (the predecessor had merged season/s2 at 18:54:11, call 106 — F14 done).

## wake — 6 calls (floor 3 + 3)

| # | ts | call | class |
|---|---|---|---|
| 1 | 18:55:47 | ListAgents | d |
| 2 | 18:55:49 | fetch + merge origin/season/s2 + status + rev-list | F14-at-wake: MAIN moved during the 1-min rotation window (master-sensei's own pushes) — legitimate, batchable into 4 |
| 3 | 18:56:01 | `git diff seats.md` + tmux windows grep | a — F8/F10 (the row is written for you; the window is in the record) |
| 4 | 18:56:09 | ack --gen 6 --ref 17dde1 continue | d |
| 5 | 18:56:17 | commit seats.md | d |
| 6 | 18:56:23 | porcelain + push seat branch + … | d-ish — batchable into 5 |

Series for this seat: 9 → 15 → 32 (spawn) → 6. A worktree seat's realistic floor is 4 (merge · ListAgents · ack · commit+push) because main moves under it; 3 if the merge rides in the ack command.

## rotate-out — 2 calls (the leanest measured today)

| # | ts | call |
|---|---|---|
| 109 | 18:55:09 | card: `## State at handoff` replaced in one python call |
| 110 | 18:55:21 | `rotate-self --name sanctuary-helper --model claude-opus-5 --effort max --prompt-file …` |

No `--prepare`, no dry-run, no `-h`; the F14 merge had happened in the work flow (106). Trigger: self-decided after the L4.252/253 harvests — no reminder-hook text and no owner line in the transcript after 18:40 (the open "helper rotate-out trigger" measurement: neither hook nor owner this time; the seat rotated on its own read of the meter/state). Series: 11 → 2.

## proposals
- none new. The helper is at floor on both sides; the one (a) call (`git diff seats.md`/tmux at 3) is F8/F10 already in its facts — prose, no change.
- MEASUREMENT for the floor table: worktree seats: wake 4 (merge rides along), rotate-out 2 when the F14 merge is part of the last harvest. Main-checkout seats: wake 3 / rotate-out 3 (prepare is the dirty-tree check MAIN needs).
