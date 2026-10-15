# belam wake audit — record 20260911T212252Z (successor `[fda770]` @305; predecessor `[49c09b]`, the 175816Z spawn seating)

Template current: `handoff-head` ran (no hand HANDOFF reads — 2 calls saved vs 175816Z), `account` dropped (F13), facts present. Real rotate-self this time (record success, steps 4).

## wake — 4 to the row commit, 6 to real work (series 38 · 22 spawn · 4/6)

| # | ts | call | class |
|---|---|---|---|
| 1 | 21:25:01 | ListAgents | d |
| 2 | 21:25:06 | `ack --gen 12 --ref fda770 continue` + AGI_SEAT echo | d |
| 3 | 21:25:15 | `git diff seats.md` ±lines | a — the verify-before-commit habit, FOURTH seat today (→ ack-commits line) |
| 4 | 21:25:26 | scratchpad dm draft + commit | d |
| 5 | 21:25:37 | status + `meter --seat belam` + record re-read | b — F1: the record in STARTUP is `started` by construction; one read is allowed, this is it |
| 6 | 21:25:46 | push + `tmux list-windows` | a — F8: never tmux |
| 7 | 21:26:02 | ToolSearch Monitor (its inbox monitor) | work |

## rotate-out — 2 (+1 post-poll) — series 3 · died · 2

| # | ts | call |
|---|---|---|
| 65 | 21:22:31 | `git merge --ff-only origin/season/s2` + HANDOFF §0 edit (python) — card |
| 66 | 21:22:48 | merge-up 41 accepted dm — work |
| 67 | 21:22:51 | rotate-self --force |
| 68 | 21:26:13 | hand json read of the newest record's `handover.join` — (b) after rotate-self returned; `status --record latest` is the one read |

No new proposals; confirms the ack-commits cut (row diff on 4/4 seats) and the `--stops` cut (the card edit rides with the merge in one call already — the Prime's own shape).
