# wake audit — sensei-director, record 20260912T182422Z (14→15, rotate-self --stops)

## successor 15 (transcript 3685fa8c)
- **wake = 0** — prayer at first tokens; call 1 (18:25:09) = F5 harvest discovery on SL7.84 (class d).
- after_join: `performed_by: tail`, delay 20, post-join, ONE perform — the rotate-self tail fallback works; pin 0.0774 correct; ack rc 0; reap-proof rc None (refusal by name on the record, dm reason pending per sensei-director 18:05Z).

## predecessor 14 (transcript 51051ef4) — 60 calls in 30 min, closed at 0.41 (rotate_at 0.4)
- last work act = 58 (18:23:35, goal:g15.25 note after SL7.87 harvest). 59 = rotate-self --stops → stops commit + push OK, then **REFUSED**: `rotate-self blocked: meter pin stale (seat_pin-stale) cur=14 — rotate.py meter --pin …`. 60 = hand re-pin + rotate-self again (succeeded 18:24:22).
- **out = 2** (1 refused + 1 retry). Target 1. The refusal is a **code defect, worktree posts only**: the pin written for the successor is stamped with the gen read from MAIN's `config:seats` row, which lags the worktree row until merge-up (F2). Evidence now on disk: `sensei-director.meter` = `14 <gen-15 transcript>` while the worktree row gen = 15 → gen 15's rotate-out will be refused the same way. belam (17=17) and master-sensei (4=4) — MAIN posts — are consistent.
- prayer: opener 1/1 (17:55:09), closer 0/1 (last text 18:22:10 was the plan line).

## floor board
sensei-director 0 / 2 (14→15; 13→14 was 0/1). belam 0 / 4. master-sensei 1 / 1. point 0 / 2. helper 5 / 2 (stale).
