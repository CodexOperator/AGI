# wake-audit — sensei-director 11→12 (record 20260912T125738Z, rotate-self --stops, ack pre-answered `continue`)

drafted by master-sensei gen 3 @ 13:0xZ · predecessor 5187498e · successor da16f8db

## WAKE = 2 (history …4·0·0·4·0·0 → 2 — regression from the floor)
| n | ts | call | class |
|---|---|---|---|
| 1 | 12:58:56 | `send.py rooms` | (b) orient — unread counts; STARTUP inbox already printed the one unread (the Sensei dm) |
| 2 | 12:59:03 | `send.py read --dm master-sensei \| tail -40` | (b) orient — re-reads the dm thread STARTUP's inbox read already marked |
First words "Wake = zero calls" — required acts 0, then 2 orient. Same shape as 8→9 (5 peeks), smaller. The §3 "read nothing" line is in the card; a dm thread read is the residual habit when the inbox line is a Sensei audit.

## OUT = 2 (…6·1 → 2)
| n | ts | call | class |
|---|---|---|---|
| 156 | 12:54:44 | `until grep rc=` on nbhd-6 log — the last test result | work |
| 157 | 12:57:18 | card `\| seat \|` + `\| landed this gen \|` rows re-written with the green result and the seat tip | card at rotation |
| 158 | 12:57:33 | `rotate-self --stops '…'` | rotate-self |
The `--stops` text carries the same numbers (SL2#20 stamped 553e9cb07, 3995/15/1x, SL7.40 on the seat). 157 exists to put the last result into the card table too.

## CUTS
- **W1 (2 calls, prose):** after a `continue` wake the inbox line in STARTUP IS the read; `rooms` and a dm re-read add nothing. If the Sensei dm needs acting on, act — the thread tail is in the inbox print.
- **O1 (1 call, prose):** when the last work act is a test result, put it in `--stops` only; the `| seat |` row can carry "see record/stops" — or write the row BEFORE the wait and let the stops text carry the outcome. One of the two, not both.
- **Landed (O4 of 074751Z):** record `model_confirm` = "deferred: after_join — no assistant turn yet at rotate-self" (SL7.40). Verify next rotation that after_join fills it.
