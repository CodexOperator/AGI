---
id: doc:card-director-general-5
mint_id: 2ba5a1adbdcb4ea2aa3aa6d92d309253
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: belam
scaffold_hash: e13627c192e516b7
season: 2
tags:
  - card
  - director
  - director-general-5
thought_session: director-general-5
title: Card director general 5
town: core
---
# doc:card-director-general-5

Role = the director template + the HEAD (`doc:unified-head`) + the council protocol (`doc:council-loop`). This card is the ONE scratch: replaced whole, ≤ 100 lines; rules live in skills, progress on the town board.

## §0 State (09-30, gen 2, meter 0.28 of 0.47)
| | |
|---|---|
| post | director-general-5 · MAIN /data/work/agi on local-maxxing/season2/main · CC Opus 5.5 high |
| goal | goal:g7.16.1.7, PLACED by the council (alive 23:4xZ): 7a NOW = goal:g7.16.1.7.1 · 7b AFTER goal:g7.16.1.6 + goal:g4.18.6 = goal:g7.16.1.7.2 |
| split of record | room `directors`, DG4 23:40:55 amend: rotate.py WHOLLY DG5 (launch + W1c goal:g4.18.5.3 + its commit sites; W1c after DG3 posts the commit_node signature) · dispatch.py launch resolvers · heal.py key path. DG3 = write.py/node_writer · DG4 = every non-rotate writer |
| claims | none held; `[claim] <file>` before any edit, `[release] <file> <sha>` after (room directors) |
| skills | agi-goal · agi-node-write · agi-verify · agi-send · agi-rotate · agi-post · agi-workflow |
| peers | DG3 · DG4 · alive (convener) · belam (session names change at rotation: ListAgents) |
| route up | to belam: merge-up · decision · rotation · red · rule only. Council: ONE council-loop room line per landing |

## §1 Plan
```
7a  .1.1.1 COMPLETE · .1.1.3 COMPLETE (P2 56c9e02ee + P3 d91710b4f) · .1.1.2.1 COMPLETE (9ccb00ccc)
    .1.1 COMPLETE: .1.1.2 closed + .1.1.4 ONE stand-up verb rotate.stand_up (905108691, 70d451b4d)
    .1.2 first turn = render of the live card + row F: non-prime LANDED d52d4bfbb (stays active until .1.2.1)
    .1.2.1 the Prime's numeral-name launch renders its row  <- IN FLIGHT (code + tests green, suite run nbhd7)
    .1.3 ONE pi template: JSON model rows + default marker; pi / pi-free / pi-local retired by name (g4.20.1)
    .1.4 heal assigns keys from a forgiving key template; key row lands on the post's own trunk too
7b  .2.1 walk · .2.2 atomic swap · .2.3 one role resolver · .2.4 post row = links · .2.5 formation
    BLOCKED on goal:g7.16.1.6 (DG3 commit_node) + goal:g4.18.6 -- never built on unlanded machinery (council)
W1c (goal:g4.18.5.3) after DG3 posts commit_node's signature in room directors
```

## §2 Landed (gen 1 + gen 2)
- gen 1: 032ee4fc0 leaves · 803309d2c one tmux launcher · bd950a3df scope argv · 80e94c3d0 R2 · 813900da7 · 05da5eb49 lock · 56c9e02ee P2 resume
- d91710b4f P3: started + dead row pid + no successor window -> aborted-by-crash in place, predecessor resumed, in-flight skips logged
- 9ccb00ccc heal session table every pass; own session_id live -> stale-row skip, pin or no pin; conftest _registry_default_to_tmp
- 905108691 + 70d451b4d rotate.stand_up: spawn / seats-launch / rotate-self / loop / heal recover / `rotate.py stand-up --post` (hand restart); skill agi-post §4
- d52d4bfbb brief.card_text: card NODE wins over a copy; [card] id·mint·grid v·git + [formation] line; heal director recovery renders; refused render keeps the card
- 0be603067 minted goal:g7.16.1.7.1.2.1
- build:bin-heal THOUGHT per round (faa9ea0cf and after) · goals .1.1.3 · .1.1.2.1 · .1.1.4 · .1.1.2 · .1.1 set complete · links 5237/0

## 🔴 Where it stops
```
.1.2.1 uncommitted in MAIN: rotate.py (_assembled_successor_command post=, spawn_window post=seat or name), heal.py (prime drops
DEFAULT_PROMPT_FILE, prompt_file=None), tests/test_brief_card_live.py (+2 tests). Suite unit agi-director-general-5-nbhd7 -> /tmp/dg5-nbhd.out.
Green -> commit those 3 by exact path, THOUGHT build:bin-rotate + bin-heal, set .1.2.1 then .1.2 complete, [release] + council line.
Open reds, not mine (red at HEAD): test_brief g15 fallback · test_rotate_closeout_steps rc2 (write.py, DG3 told).
Next command: `grep -c '^==' /tmp/dg5-nbhd.out; grep '^== .*failed' /tmp/dg5-nbhd.out`
```
## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared with 9 posts | commit by exact path; never commit, reset or stash another post's file |
| verify-suite.lock held in bursts (PASS B3) | a run inside it = every test ERRORs at setup: wait for the lock, rerun that file (loop: wait lock -> run -> retry on " errors in") |
| a --body-file with its own H1 | create adds one -> two; strip it before create |
| write.py sub is literal; replace body guards splits | card: `replace body 3:<Paid-for line - 1> <file>` (the file ends before the Paid-for line) (H1 line 1 and THOUGHT stay) |
| rotate.py / heal.py run every live post | launch-path edits tested on dummies only (conftest no-real-tmux fixture) |
| tests load rotate via spec_from_file_location | heal's own `import rotate` is sys.modules: patch THAT alias (conftest does, for REGISTRY_DEFAULT_DIR) |
| council invariant | no parent/kid dispatch; nodes via write.py; nothing deleted |

## §5 Verification
`python3 extensions/agi/bin/links.py links` 0 broken · heal/rotate files one per run: test_heal_seats test_heal_watch test_heal_pin_reap test_heal_resume test_heal_ack_rotation test_rotate_recover test_rotate_identity_main test_heal_worktree_refusal test_box_guard test_bin_help_smoke + test_stand_up + test_rotate*.py (58 files: /tmp/dg5-nbhd.sh via systemd-run, mkdir its basetemp parent)

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Stood up by belam-S2-L5-XVIII on the owner 23:3xZ order, verbatim: "Restart council including DG5 stand up. Then let them tackle the bundle and see how best to streamline it further." Lane per the owner 23:1xZ: "If needed, spawn director-general-5 as well and have them tackle the rotate/spawn unification/template+config gutting and streamlining."
<!-- THOUGHT:END -->
