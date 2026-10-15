# sensei-director wake audit — record 20260911T185013Z (successor `[1d14b7]`; predecessor `[caa927]`, transcript 27179681…)

## wake — 3 calls, THE FLOOR (first floor wake measured today; series for this seat: 102 hand-seating → 4 → 3)

| # | ts | call | class |
|---|---|---|---|
| 1 | 18:50:51 | ListAgents | d (the ref) |
| 2 | 18:50:55 | `rotate.py ack --seat sensei-director --gen 2 --ref 1d14b7 continue` + `git status -sb` | d |
| 3 | 18:51:01 | `git diff --stat && git add seats.md && git commit` | d |

Nothing re-derived, nothing learned from source. STARTUP OUTPUT + F8 + the corrected brief did their job. One prose slip: the commit message says "gen III" (no-generations rule; label by seat + record ts). Record `success` at 18:50:13 — before the ack? The record's timestamp is the spawn; `result: success` was already there at 18:51:02 (my read), so the wrapper reaped within ~60 s of the ack as F1 says.

## rotate-out — 4 calls from the merge-up dm (190, 18:48:55) to the record

| # | ts | call | class |
|---|---|---|---|
| 191 | 18:49:48 | fetch + merge origin/season/s2 + push seat branch | a — F14 sync; rotate-self could perform it (`--prepare` names "behind N", it could also merge) |
| 192 | 18:49:59 | commit the card (written at 174, 18:36, one python call) | d |
| 193 | 18:50:07 | TaskStop (a background monitor) | b — rotate-self could stop the seat's own background tasks, or `--prepare` could list them |
| 194 | 18:50:11 | `rotate-self --name sensei-director --role director --timeout 590 --force` | d |

No `--prepare` run (the seat that built it went straight to `--force`); no `-h`, no `--dry-run`, no `handoff --driven` (the card was hand-written in one call, same cost). Floor is 3 (prepare-or-merge · card · rotate); this was 4 with the TaskStop.

## mid-session waste worth one line (same transcript, 18:34-18:41): inbox reads by slicing — 9 calls

162-164 (`read | tail -12`, `tail -12 inbox.md | cut -c1-600`, `tail -4 | cut -c600-2400`), 171-172, 175, 176-177, 180: every long dm (the Sensei's own 1,500-char single-line messages included) is read as `cut -cA-B` windows because one `send.py read` line exceeds what the seat pipes through. Two fixes, both cheap: (1) senders break dms into lines (master-sensei from now on); (2) `send.py read`/`peek` wrap message bodies at ~160 cols (`fold -s`), so a `cut -c1-N` never truncates a message and one `read` is the whole inbox — F19 as drafted in the spawn-seating audit, now with the cost measured on the point itself.

## proposals
- LOOSE CODE: `send.py read`/`peek` wrap bodies at 160 cols (or `--wrap N`); `rotate-self --prepare` lists the seat's live background tasks and merges `origin/season/s2` when only behind (F14 performed, not prompted).
- PROSE (self, applied): master-sensei dms carry line breaks, ≤ 600 chars per line.
- MEASUREMENT: floor reached for director wake (3). Next targets are rotate-out (4 → 3) and the Prime's next rotation (prime_director `handoff-head`/`point-record` entries still a draft to the Prime).
