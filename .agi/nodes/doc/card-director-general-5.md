---
id: doc:card-director-general-5
mint_id: 2ba5a1adbdcb4ea2aa3aa6d92d309253
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-5
scaffold_hash: e13627c192e516b7
season: 2
tags:
  - card
  - director
  - director-general-5
title: Card director general 5
town: core
---
# doc:card-director-general-5

Role = the director template + the HEAD (`doc:unified-head`) + the council protocol (`doc:council-loop`). This card is the ONE scratch: replaced whole, ≤ 100 lines; rules live in skills, progress on the town board.

## §0 State (01:4xZ 09-30, rotating at ~0.42 of 0.47) — gen 1 hands over
| | |
|---|---|
| post | director-general-5 · MAIN /data/work/agi on local-maxxing/season2/main · CC Opus 5.5 high |
| goal | goal:g7.16.1.7, PLACED by the council (alive 23:4xZ): 7a NOW = goal:g7.16.1.7.1 · 7b AFTER goal:g7.16.1.6 + goal:g4.18.6 = goal:g7.16.1.7.2 |
| split of record | room `directors`, DG4 23:40:55 amend: rotate.py WHOLLY DG5 (launch + W1c goal:g4.18.5.3 + its commit sites; W1c after DG3 posts the commit_node signature) · dispatch.py launch resolvers · heal.py key path. DG3 = write.py/node_writer · DG4 = every non-rotate writer |
| claims | none held (all released with shas in room directors); `[claim] <file>` before any edit, `[release] <file> <sha>` after |
| skills | agi-goal · agi-node-write · agi-verify · agi-send · agi-rotate · agi-post · agi-workflow |
| peers | DG3 agi-6b · DG4 agi-47 · alive agi-13 (convener) · belam agi-9c (session names change at rotation: ListAgents) |
| route up | to belam: merge-up · decision · rotation · red · rule only. Council: ONE council-loop room line per landing |

## §1 Plan
```
7a  .1.1.1 COMPLETE · .1.1.2 lock LANDED (05da5eb49) · .1.1.3 P2 resume LANDED (56c9e02ee)
    .1.1.3 P3  <- NEXT: aborted rotation -> predecessor resumed (see where it stops)
    .1.1.2.1 skip a post whose session is open in a live pid (registry read every pass; conftest isolation FIRST)
    .1.1.4 ONE stand-up verb: rotate.py stand-up --post <p>; spawn / rotate / heal recover / hand restart thin callers
           (flock is per open file: the verb must never nest post_launch_lock for one post)
    .1.2 first turn = render of the live card + row F formation line (g1.9, g1.9.2)
    .1.3 ONE pi template: JSON model rows + default marker; pi / pi-free / pi-local retired by name (g4.20.1)
    .1.4 heal assigns keys from a forgiving key template; key row lands on the post's own trunk too
7b  .2.1 walk · .2.2 atomic swap · .2.3 one role resolver, DEFAULT_CC_ROLES 9 -> 0 · .2.4 post row = links · .2.5 formation
    BLOCKED on goal:g7.16.1.6 (DG3 commit_node) + goal:g4.18.6 -- never built on unlanded machinery (council)
W1c (goal:g4.18.5.3) after DG3 posts commit_node's signature in room directors
```

## §2 Landed (this generation)
- 032ee4fc0 + write.py commits: goal:g7.16.1.7.1 .1.1-.1.4 · .2 .2.1-.2.5 · .1.1.1-.1.1.4 · .1.1.2.1 (links 5217/0)
- 803309d2c ONE tmux launcher rotate.launch_in_window; heal._launch_recovered thin caller
- bd950a3df ONE scope-argv builder mem_cap.scope_argv(own_scope) + mem_cap.unit_name
- 80e94c3d0 R2: N consecutive pressure deferrals -> ONE [red] to the prime_director row; cell reaper.recovery_defer_alert_after 3
- 813900da7 announced handoff path tree-relative (rotate._tree_rel)
- 05da5eb49 ONE launch lock per post rotate.post_launch_lock: heal recover + seated cmd_spawn
- 56c9e02ee P2 resume: claude-code.toml resume slot, harness_template.has_slot, spawn_window(resume=), heal resumes on a transcript
- build:bin-rotate / bin-heal / bin-mem-cap THOUGHT per round (latest 2543fe7aa)

## 🔴 Where it stops
DG5 rotates after .1.1.3 P2; next is P3, the aborted-rotation rule in heal._rotation_in_flight.
P3 plan: heal._rotation_in_flight returns True for ANY `started` record < SEAT_DEAD_WINDOW_S old, so heal skips the seat. New rule: a `started` record whose row pid is dead AND whose successor window is absent -> rewrite that record in place `result: aborted-by-crash`, log it, return False, so recovery runs and P2 resumes the predecessor. Tests in test_heal_ack_rotation.py / test_heal_watch.py style, one file per run.
Next command: `grep -n "_rotation_in_flight\|SEAT_DEAD_WINDOW_S =" extensions/agi/bin/heal.py`

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared with 9 posts | commit by exact path; never commit, reset or stash another post's file |
| verify-suite.lock is held in short bursts (PASS B3) | write.py writes land uncommitted; commit by exact path in a gap; also wait out .git/index.lock |
| suite lock races | a file can be refused between the lock check and pytest start: /tmp/dg5-retry.sh-style retry on 'suite window refused'; long runs detached via systemd-run --user |
| a long file (workflow 146 s) can hit the lock mid-file = a setup ERROR | rerun that test alone before calling it red |
| a --body-file with its own H1 | create adds one -> two; strip it before create |
| write.py sub is literal; replace body guards splits | multi-line = replace body N:M <file>, the range a whole paragraph; card: replace 3:<line before the last paragraph> |
| rotate.py / heal.py run every live post | launch-path edits tested on dummies only (conftest no-real-tmux fixture) |
| council invariant | no parent/kid dispatch; nodes via write.py; nothing deleted |

## §5 Verification
`python3 extensions/agi/bin/links.py links` 0 broken · the touched test files + neighbourhood, ONE file per run while PASS B3 runs

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Stood up by belam-S2-L5-XVIII on the owner 23:3xZ order, verbatim: "Restart council including DG5 stand up. Then let them tackle the bundle and see how best to streamline it further." Lane per the owner 23:1xZ: "If needed, spawn director-general-5 as well and have them tackle the rotate/spawn unification/template+config gutting and streamlining."
<!-- THOUGHT:END -->
