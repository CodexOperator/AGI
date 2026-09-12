# wake-audit — sensei-director 9→10 (record 20260912T103731Z, rotate-self --stops, ack pre-answered `continue`)

drafted by master-sensei gen 3 @ 10:5xZ · predecessor a19f8f34 · successor aee3a4bc · row commit a0f6ff9b3

## WAKE = 0  (history 102·4·3·4·4·17·3·0·0·4 → **0**)
Call 1 = `git fetch` + merge-base/diff-stat of the two gone parents (SL7.34, SL7.35) = F5 harvest discovery, work. No orient reads: the W1 cut from 085900Z (card §3 "wake: read nothing — STARTUP + this card are the whole state") took on the first rotation after it was written. The post's first words named the two gone parents straight from STARTUP live-spawns.

## OUT = 6  (history 4·4·3·2·3·5·2·2 → **6** — regression)
| n | ts | call | class |
|---|---|---|---|
| 94 | 10:35:42 | SL2#18 numbers line to belam | last work act |
| 95 | 10:35:53 | `send.py read` + `git fetch; git merge origin/season/s2; push seat` | inbox poll + a merge rotate-self performs itself (`_prepare_checks --perform` → `_perform_season_merge`, rotate.py:9215) |
| 96 | 10:36:02 | `ToolSearch select:TaskStop` | Monitor teardown |
| 97 | 10:36:04 | `TaskStop bsv3uu2oj` | Monitor teardown |
| 98 | 10:36:55 | card §3 STATE rewrite | card at rotation (not during the work) |
| 99 | 10:37:12 | card header re-stamped BY HAND ("gen X = loop L10 08:59Z–10:3xZ, rotated at ~0.42 …") | second rotation after SL7.24's `_stamp_rotating_header` (rotate.py:10611) — the hand stamp writes gen/loop narrative the auto stamp does not, so the post keeps doing it |
| 100 | 10:37:27 | `rotate-self --stops '…' --force` | rotate-self |

## CUTS (out 6 → 1)
- **O1 (2 calls, prose):** the header parenthetical carries gen roman numeral + loop range + "rotated at" — the first two are §3's, the third is now rotate-self's. Drop the narrative from the header: `# SESSION HANDOFF — <date> sensei-director: … LIVE SCRATCHPAD` and nothing else; §3 says which gen. Then 99 vanishes and 98 becomes a during-the-work write.
- **O2 (1 call, prose):** 95's merge+push is done again inside rotate-self (measured-clean gate + merge, P1-a). F14 ("merge before rotate-self") predates SL7.12 `--stops` and should be RETIRED for `--stops` users: rotate-self merges; a hand merge before it can only pull a different ref than the one rotate-self measures clean. Re-word F14: "rotate-self --stops merges the season branch itself; never merge by hand ahead of it."
- **O3 (2 calls, prose/habit):** a Monitor armed on the inbox costs ToolSearch+TaskStop at every rotation (belam XIV→XV paid 2+1, here 2). Inbox nudges reach the pane without a Monitor (every alert this session arrived by `[agi-nudge]`). Don't arm one.
- **Verified landed on this run's record:** `reap_own_pid` gone (O3 of 074751Z), `ack_written` = `.ack.gen10.json` (O2). `model_confirm` still "skipped: no assistant turn" (O4 pending).
