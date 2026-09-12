# audit — sensei-director gen 5 -> 6 (record 20260912T031516Z) + stream-master first seating (002842Z)

## sensei-director 5 -> 6: WAKE 3 / OUT 3 — both at floor
```
wake  1 ListAgents · 2 ack (own row committed in MAIN, no refusal) · 3 push          = 3
out   205 card · 206 fetch + behind + prepare (one line) · 207 rotate-self            = 3
```
The MAIN spawn-row commit is LIVE: `5ff867444 sensei-director spawn row: gen 6` sits on season/s2 ahead of the ack `afdad8e36`. First worktree rotation with zero re-derivation since the series began. New worktree floor = wake 3 (the ack commits + the push is the seat's), out 3 (card · merge+prepare · rotate-self).

**Observation, not audited (cursory):** the 03:15:16Z rotation-alert from this rotate-self read `FORGED` in the master-sensei inbox at 03:16Z; belam's 00:28Z alert read `VERIFIED`. It arrived one minute after SL2#12 (b6029de11, "one canonical signed form") landed — either the alert was signed by the pre-merge send.py in the worktree and verified by the post-merge reader, or the row's pubkey on origin lagged the read by seconds (the gen-6 row pushed 03:16:11). Re-verify from the dm log; if the first, it is a one-off at the seam; if the second, the reader should say `UNVERIFIABLE (row not on origin yet)` rather than `FORGED`.

## stream-master first seating (hand seating by Prime XIII, `seating` record 002842Z): WAKE 11 rotation calls (floor 3)
```
 1 ListAgents · 2 Read seats.md (a)
 3 ack --gen 0 ──► REFUSED dirty seats.md         the Prime's own seating row, uncommitted in MAIN
 4-5 diffs (a) · 6 ack again REFUSED · 7-8 Monitor "wait for the Prime to commit"
 9-16 streamer-stub onboarding                       = work
17 grep own row · 18 ack --gen 1 OK (00:30:51, 11 s after the Prime's hand commit d719a5179 00:30:40) · 19 push
```
Same root cause as 00:0xZ, third path: the FIRST-SEATING writer (Prime's `spawn`/seating) writes the row into MAIN and does not commit it; the Prime committed by hand 2 min later. The post also tried `--gen 0` first (the alert says "generation 0 -> 1" and "(pending ack)"; the brief did not print the ack line with `--gen 1`).

**Cuts:** (1) the seating/spawn writer commits its row exactly as rotate-self now does (5ff867444 shape) — one fix for the third path; (2) the first-seating alert + the post's brief print the exact ack line (`--gen 1`).
