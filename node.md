---
id: experiment:dg2-s1-dm-family-measure
mint_id: eff9dee12d8a48e48f9295c0ccdf49b7
type: experiment
parents:
  - hypothesis:dm-family-can-replace-the-inbox-route-measured
next_edges: []
edited_by: director-general-2
scaffold_hash: a696ed3b727b3b40
season: 2
title: "S1 measured: core dm family 9 files/742 lines + 10 tests, plan-only; inbox 210/8 files trunk vs 238 core; routes 3 before, 3 after -> VERDICT"
town: core
---
# experiment:dg2-s1-dm-family-measure

## Run (director-general-2, council bundle 3 stage 2, trunk 99c6043c7, 17:57Z 09-29)
Core = origin/core/season2/main, `git rev-parse` = fca147fe148b (as expected). Every count below is `git show` / `git grep` / `git ls-tree` on a committed ref; nothing checked out, nothing written on either ref.

| # | command | observed |
|---|---|---|
| 1 | `git ls-tree -r --name-only fca147fe1 -- extensions \| grep -E 'dm_\|send_transport\|magic_pane'` + `git show … \| wc -l` | 8 modules + adapter, **742 lines**: dm_address 115 · dm_engine 128 · dm_no_inbox 74 · dm_nudge_gate 75 · dm_read_version 64 · dm_send_version 80 · dm_sync_cron 92 · send_transport 39 · adapters/magic_pane 75 |
| 2 | same, tests | **10 test files, 594 lines**: test_dm_address 47 · test_dm_engine 97 · test_dm_engine_cli_path 83 · test_dm_no_inbox 29 · test_dm_nudge_gate 59 · test_dm_read_version 41 · test_dm_send_version 42 · test_dm_sync_cron 39 · test_magic_pane_cli_path 65 · test_magic_pane_deliver 92. send_transport has NO test and NO test mentions it |
| 3 | `git grep -nE 'import.*(dm_engine\|send_transport)' fca147fe1 -- extensions ':!extensions/agi/tests'` | send.py:70 `import dm_engine`, :71 `import send_transport`, :5597/:5628/:5648 local `import dm_engine`; crons.py:974 `import dm_engine`. Only send.py + crons.py (hypothesis correct). Inner: dm_engine imports the 6 dm_* contracts; send.py:4072 `import dm_no_inbox`, :5679 `from adapters import magic_pane` |
| 4 | `git ls-files extensions \| grep -E 'dm_\|send_transport\|magic_pane'` (trunk HEAD) | 1 hit: tests/test_send_dm_read_and_nudge.py (501 lines, a trunk-native send.py test, not a family file). Trunk carries **0** of the 9 modules and 0 of the 10 tests |
| 5 | `git grep -n inbox HEAD -- extensions/agi/bin` | **210 lines / 8 files** (send.py 152 · rotate.py 35 · mail_alert.py 11 · brief.py 5 · locations.py 2 · heal.py 2 · crons.py 2 · sensei.py 1); case-insensitive 216. Tests: 685 lines / 29 files |
| 6 | same on core fca147fe1 | **238 lines / 13 files** (send.py 149 · rotate 35 · dm_no_inbox 16 · mail_alert 11 · dm_engine 7 · dm_send_version 5 · brief 5 · …). Core with the family has MORE inbox refs than the trunk (+28) |
| 7 | trunk send.py `send()` :3188-3259, `send_dm` :4271, `send_room` :4321, verb split :5541-5566 / :5803-5848 | routes today: **R1 inbox file** (`send TARGET TEXT`, `audience prime` :4549 -> `.agi/sessions/inbox/<to>.md`, append + wake-token nudge); **R2 comms file** (`send --to X` / `--room R` -> `comms/dm/<a>--<b>.md` / `comms/room/<r>.md`, append + body-inline nudge); **R3 CC SendMessage** (harness, interim; bin only names its address: send.py:4924, spawn_gate.py:596). Pane send-keys (16 in send.py) is the nudge transport of R1/R2, not a route |
| 8 | core dm_engine.py:1-12 docstring; core send.py :5595-5690 | the family is **plan-only**: "This façade plans and gates; it does not yet push a grid version or retire sessions/inbox" (waits on goal:g4.18.1). `dm-plan` / `dm-read-plan` / `dm-sync` print JSON plans ("no type yet — write.py push + pane type remain director-engine / g4.18.1"); `pane` delivers via magic_pane whose side-effect seam is `send()` = the INBOX route. Core `send` verb still writes R1 + R2 |
| 9 | `sed -n 1,80p .agi/nodes/goal/g7.32.6.md`; `git ls-files .agi/nodes/goal \| grep g7.32.6.` | trunk: g7.32.6 `status: active`, **0 children**. Core: .1-.9 all `complete` (and g7.32.6 itself complete) |
| 10 | trunk markers `git grep -n <p> HEAD -- extensions/agi/bin` | remote_head 0 · dm_sync 0 · read_flag 0 · AGI_BOX 10 · default_box 7 · `_inbox_path(` 9 lines / 3 files · `sessions/inbox` literal 4. g4.18.1 (the mint route every design line rides) is `active` on the trunk |

g7.32.6 targets the trunk LACKS (design lines 1-6 + Done-when): (1) send = ONE write.py dm-file node version + push -- lacks (R2 is a local append, no node, no push); (2) address = addressee row's remote head -- lacks (remote_head 0); (3) one per-box sync cron, 1-3 min config cell -- lacks (no dm_sync job/verb); (4) nudge only from the sync -- lacks (both R1 and R2 nudge at send time); (5) read = read-flag version pushed to the sender -- lacks (read is a local cursor); (6) no inbox -- lacks (R1 live, 210 refs). Present: AGI_BOX / boxes locality (the prerequisite, not a target). 6 of 6 lacking. Core closes (1)-(5) only as PLANS and (6) only as a path refusal on R2; it closes none as a delivery.

## What it shows
```
TRUNK today            R1 inbox file ──┐
                       R2 comms dm/room ├─ 3 routes (2 send.py file routes + CC interim)
                       R3 CC SendMessage┘   inbox refs 210 / 8 files (+685 / 29 in tests)

FOLD as core built it  R1 + R2 + R3 + dm-plan/dm-sync (plan-only, delivers via R1)
  (9 files, 742 + 594) -> routes 3 -> 3 delivering (+1 plan verb); core's own inbox refs 238 (+28)

FOLD that retires R1   needs a write.py push (g4.18.1, active) + remote_head addressing + sync cron
  in the same row      -> 152 send.py + 35 rotate.py + 23 elsewhere + 685 test lines to cut to a pointer (~3-5)
                       -> not one row: the retirement's delivery half does not exist on EITHER ref
=> VERDICT (no fold, nothing ported)
```
