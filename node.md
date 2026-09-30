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

## §0 State (01:0xZ 09-30, meter 0.33 of 0.47) — gen 1, stood up by belam-S2-L5-XVIII on the owner's word
| | |
|---|---|
| post | director-general-5 · session agi-c8 · tmux window @14 · MAIN /data/work/agi on local-maxxing/season2/main · CC Opus 5.5 high |
| goal | goal:g7.16.1.7, PLACED by the council (alive 23:4xZ): 7a NOW = goal:g7.16.1.7.1 · 7b AFTER goal:g7.16.1.6 + goal:g4.18.6 = goal:g7.16.1.7.2 |
| split of record | room `directors`, DG4 23:40:55 amend: rotate.py WHOLLY DG5 (launch + W1c goal:g4.18.5.3 + its commit sites, W1c after DG3 posts the commit_node signature) · dispatch.py launch resolvers · heal.py key path. DG3 = write.py/node_writer · DG4 = every non-rotate writer |
| skills | agi-goal · agi-node-write · agi-verify · agi-send · agi-rotate · agi-post · agi-workflow |
| peers | DG3 agi-6b · DG4 agi-47 · alive agi-13 (convener) · belam agi-9c · DG1 agi-77 · DG2 agi-40 |
| route up | to belam: merge-up · decision · rotation · red · rule only. Council: ONE council-loop room line per landing |

## §1 Plan
```
done  measure · split agreed (room directors) · 11 leaves + .1.1 split into 4 · .1.1.1 COMPLETE · .1.1.2 lock LANDED (05da5eb49)
7a  .1.1.2.1 skip a post whose session is open in a live pid (registry read every pass; conftest isolation first)
    .1.1.3 resume   <- NEXT: heal relaunches a dead post with claude --resume on its transcript; aborted rotation -> predecessor resumed (g6.41.1 P2 P3)
    .1.1.4 ONE stand-up verb: rotate.py stand-up --post <p>; spawn / rotate / heal recover / hand restart = thin callers
    .1.2 first turn = render of the live card + row F formation line (g1.9, g1.9.2)
    .1.3 ONE pi template: JSON model rows + default marker; pi / pi-free / pi-local retired by name (g4.20.1)
    .1.4 heal assigns keys from a forgiving key template; key row lands on the post's own trunk too
7b  .2.1 walk · .2.2 atomic swap · .2.3 one role resolver, DEFAULT_CC_ROLES 9 -> 0 · .2.4 post row = links · .2.5 formation template
    BLOCKED on goal:g7.16.1.6 (DG3 commit_node) + goal:g4.18.6 -- never built on unlanded machinery (council)
W1c (goal:g4.18.5.3, rotate.py's 4 posts-row commit paths -> ONE _commit_posts_row) after DG3 posts commit_node's signature
```

## §2 Landed
- 032ee4fc0 + write.py commits: goal:g7.16.1.7.1 .1.1-.1.4 · .2 .2.1-.2.5 · .1.1.1-.1.1.4 (links 5182/0 broken)
- 803309d2c (a) ONE tmux launcher rotate.launch_in_window; heal._launch_recovered thin caller
- bd950a3df (b) ONE scope-argv builder mem_cap.scope_argv(own_scope) + mem_cap.unit_name
- 80e94c3d0 (c) R2: N consecutive pressure deferrals -> ONE [red] to the prime_director row; cell reaper.recovery_defer_alert_after
- 813900da7 (d) announced handoff path tree-relative (rotate._tree_rel)
- 05da5eb49 (e) ONE launch lock per post rotate.post_launch_lock: heal recover + seated cmd_spawn
- build:bin-rotate / bin-heal / bin-mem-cap THOUGHT per round (latest 8071b0955 16b8d548e) · leaf .1.1.2.1 minted

## 🔴 Where it stops
Next: .1.1.3 resume (g6.41.1 P2): add a `--resume` slot to templates/harness/claude-code.toml (template first), then heal._recover_seat: row session_id + transcript (rotate.transcript_from_registry_dict {cwd: seat tree, session_id}) exists -> same name + generation, prompt = a short RESUMED line, row keeps session_id; else today's fresh spawn. `[claim] rotate.py + heal.py` first.
Next command: `grep -n "slot\b\|def render\|def emit" extensions/agi/bin/harness_template.py | head`

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared with 9 posts | commit by exact path; never commit, reset or stash another post's file (goal:g7.16.1.7.md carries someone else's pending key-row edit: not mine) |
| verify-suite.lock is held in short bursts (PASS B3) | write.py writes land uncommitted; commit by exact path in a gap |
| a --body-file with its own H1 | create adds one -> two; strip it before create |
| write.py sub is literal | no \n; multi-line = replace body N:M <file>, the range a whole paragraph |
| a test file run long (workflow 146 s) can hit a suite-lock refusal mid-file = a setup ERROR; rerun that test alone before calling it red |
| suite lock races | a file can be refused between the lock check and pytest start: /tmp/dg5-retry.sh retries on 'suite window refused'; long runs detached via systemd-run --user |
| rotate.py / heal.py run every live post | launch-path edits tested on dummy scopes only (goal:g6.41.1) |
| council invariant | no parent/kid dispatch; nodes via write.py; nothing deleted |

## §5 Verification
`python3 extensions/agi/bin/links.py links` 0 broken · the engine test file touched, ONE file at a time while PASS B3 runs

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Stood up by belam-S2-L5-XVIII on the owner 23:3xZ order, verbatim: "Restart council including DG5 stand up. Then let them tackle the bundle and see how best to streamline it further." Lane per the owner 23:1xZ: "If needed, spawn director-general-5 as well and have them tackle the rotate/spawn unification/template+config gutting and streamlining."
<!-- THOUGHT:END -->
