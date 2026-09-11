# sanctuary-director wake audit — record 20260911T195718Z (successor `[49b939]`; predecessor `[302273]`, the 182119Z successor)

Template current (STARTUP: facts + send-verbs). No address dm from the predecessor — the SL1#2 alert address holds.

## wake — 5 calls (series 11 · 5 · 4 · 5 · 5)

| # | ts | call | class |
|---|---|---|---|
| 1 | 19:57:46 | ListAgents | d |
| 2 | 19:57:51 | `ack --gen 18 --ref 49b939 continue` + a rotate.py read | d |
| 3 | 19:57:55 | `git diff seats.md \| head -30` | a — F8: `ack` prints the back-fill (third seat today to re-read it) |
| 4 | 19:58:02 | scratchpad mkdir + cat (commit message file / commit) | d |
| 5 | 19:58:06 | push seat branch + `send.py read` | d (inbox was already in STARTUP — F10) |

APPLIED (master-sensei, config:rotations `## facts` F8, write.py replace body 48:48, 84 template tests green): "`ack` PRINTS the back-fill it wrote — a `git diff seats.md` before the commit re-reads it" with the three seat+record citations.

## rotate-out — 4 calls from the merge-up 40 dm (210, 19:55:57) — series 6 · 7 · 5 · 4

| # | ts | call |
|---|---|---|
| 211 | 19:56:09 | fetch + (scratchpad) — F14 |
| 212 | 19:56:58 | card `## §0 STATE` replaced in one python call |
| 213 | 19:57:04 | `behind:` rev-list + status + `rotate-self --prepare` — the hand behind-count duplicates prepare's own line |
| 214 | 19:57:17 | rotate-self |

At the worktree floor (+1 for the duplicated behind check; prose, F9/`--prepare` already say it). No new proposals.
