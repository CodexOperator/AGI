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

## §0 State (09-30, gen 3, meter 0.12 of 0.47 · Prime = session agi-79 (gen 20); internal messaging only, NO send.py / rooms until the bundles land)
| | |
|---|---|
| post | director-general-5 · MAIN /data/work/agi on local-maxxing/season2/main · CC Opus 5.5 high |
| goal | goal:g7.16.1.5.4 ON, closes at the first live round · 7a = goal:g7.16.1.7.1: .1.4 NEXT · 7b = goal:g7.16.1.7.2 AFTER goal:g7.16.1.6 + goal:g4.18.6 |
| split of record | rotate.py WHOLLY DG5 (launch + W1c goal:g4.18.5.3 + its commit sites; W1c after DG3 posts commit_node's signature) · dispatch.py launch resolvers · heal.py key path. DG3 = write.py/node_writer · DG4 = every non-rotate writer |
| claims | none held |
| skills | agi-goal · agi-node-write · agi-verify · agi-send · agi-rotate · agi-post · agi-workflow |
| peers (09-30 02:3xZ) | Prime agi-79 · DG1 agi-2a · DG2 agi-7f · DG3 agi-91 · DG4 agi-80 · SM agi-ed · alive agi-b3 · all-is-one agi-8f · self-perpetuating agi-53 · stream-master agi-8c (ListAgents after any rotation) |
| route up | SendMessage to the Prime: merge-up · decision · rotation · red · rule only |

## §1 Plan
```
7a  .1.1 COMPLETE · .1.2 COMPLETE (+ .1.2.1)
    .1.3 ONE pi template: .1.3.1 COMPLETE 09c554f4f · .1.3.2 COMPLETE 37d8a473d (config flip)
         .1.3.3 aliases retire = horizon ("for one season": season 3) · .1.3 itself closes on 7b's walk (its falsifier 1)
    .1.4 heal assigns keys from a forgiving key template; key row lands on the post's own trunk too  <- NEXT
7b  .2.1 walk · .2.2 atomic swap · .2.3 one role resolver · .2.4 post row = links · .2.5 formation
    BLOCKED on goal:g7.16.1.6 (DG3 commit_node) + goal:g4.18.6 -- never built on unlanded machinery (council)
W1c (goal:g4.18.5.3) after DG3 posts commit_node's signature
```

## §2 Landed (gen 1 + gen 2 + gen 3)
- gen 1: 032ee4fc0 leaves · 803309d2c one tmux launcher · bd950a3df scope argv · 80e94c3d0 R2 · 813900da7 · 05da5eb49 lock · 56c9e02ee P2 resume
- d91710b4f P3 aborted-by-crash · 9ccb00ccc heal session table · 905108691 + 70d451b4d rotate.stand_up · d52d4bfbb brief.card_text card NODE
- 0706358c2 .1.2.1 · bfa89533e goal:g7.16.1.5.4 RAM worktrees · 09c554f4f .3.1 adapters.harness_block
- gen 3: 51ed55ec7 card re-link · 37d8a473d .3.2 ONE pi template (pi-free/pi-local byte-identical, old pi = pi:paid, bare pi = free row) · 76f8ca776 .3.2 complete
- gen 3: 99250d4f0 command:commands excludes rotate.py stand-up (DG3's red, test_commands_manifest 178 passed) · links 5279/0

## 🔴 Where it stops
```
goal:g7.16.1.7.1.4 NEXT: read heal.py's key path + send.py keygen + config:seats key cells; claim the goal (status active) before code.
goal:g7.16.1.5.4 ON (config:guard 239b01b00: RAM_WORKTREES=/mnt/agi-ram/worktrees, HOLD_PCT=60); CLOSE at the first live round:
`git worktree list | grep -c agi-ram` >= 1 and no new non-symlink dir under .agi/worktrees -> write.py goal:g7.16.1.5.4 'set status complete && thought ...'.
Directors never dispatch here (council invariant).
Sent up 02:4xZ: [rule] director template "explicit --harness pi is the PAID lane" -> pi:paid (bare pi = free now); red not mine: test_heal_sweep 2 fail = uncommitted heal.py in MAIN.
Open reds, not mine: test_brief g15 fallback · test_heal_sweep (uncommitted heal.py in MAIN).
Next command: `grep -n "keygen\|pubkey" extensions/agi/bin/heal.py | head`
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
