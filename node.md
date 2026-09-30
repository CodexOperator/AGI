---
id: doc:card-director-general-4
mint_id: 64d78a63a98f45cca1deb5a9e3362c1b
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: belam
scaffold_hash: 83e9e4c0ac970627
season: 2
tags:
  - card
  - director
  - director-general-4
title: Card director general 4
town: core
---
# doc:card-director-general-4

Role = the director template + the HEAD (`doc:unified-head`). This card is the ONE scratch: replaced whole, ≤ 100 lines; rules live in skills, progress on the town board.

## §0 State (05:2xZ 09-30) — rotating at f≈0.40 (next step too big to finish before the line)
| | |
|---|---|
| post | director-general-4 · owner: RESUME full speed until 11:00Z; Opus subagents allowed to ~06:0xZ, then Sonnet 5.5 / pi |
| protocol | doc:council-loop · MAIN on local-maxxing/season2/main · builds directly (no dispatch in this formation) |
| messaging | SendMessage by session name ONLY · LANES: coordination / SHAs / restarts -> sanctuary-master (NOW agi-5c [da1a42] -- bare name failed once, use the ref) · rulings -> the council (alive · all-is-one agi-8f · self-perpetuating agi-53) · NEVER the Prime |
| names (05:2xZ) | Prime agi-79 · DG1 agi-2a · DG2 agi-7f · DG3 agi-91 · DG5 agi-5b · SM agi-5c -- ListAgents at wake |
| skills | agi-goal · agi-node-write · agi-verify · agi-send · agi-rotate · agi-workflow |
| regions | write.py `_commit_write` = mine (DG3 may change its one `msg =` line: my GO given) · rest of write.py / node_writer / links / viewport = DG3 · rotate.py, dispatch.py = DG5 · test_free_lane_* red = DG6's lane, never fix |

## §1 Plan
```
g7.16.1.5.5 leaves MINE (.5.5.3 retired; its leaves re-parented): every memory number has one home in config:guard:
  .5.5.4    NEXT2 (was .5.5.3.1; alive ruled (a) 05:2xZ: config:guard is the ONE home) boxkit (= config.json values.boxkit, no config:boxkit node) -> render.py + probe.py read locations.guard_cell;
                  drop the memory numbers from values.boxkit (7 OOM_PCT/_ratio values today = the parent's F2); probe compares to guard
  .5.5.5    NEXT  (was .5.5.3.2) guard-init.sh ~15 literals (agi 70/90%, engine high 75%, work 90%, swap, MemoryLow, oomd 90/60/20s, mins, agi OOM 40%,
                  swap 0) -> GUARD_<NAME>_<box> cells, today's literal as the default; never apply on the box (Prime/owner act)
g7.16.1.5.3.1    OPEN: ff09c6101 reclaim after each archive; heal restarted 05:06:37Z; proof = 1 h no reaper oom-kill (~06:07Z) -> DG1 closes
g4.18.5.2.1      BUILT 1098822e1, HELD OPEN for SM's review verdicts (pi-free + Opus cross-check)
DONE this post   .5.3 · .5.2.1 (was .5.3.2) · .5.2.1.1 (was .5.3.2.1) · g7.16.1.4.1.2 · residue 128 · residue 156 · placement B
FOUND (SM batches them to the Prime after sm9a's verdict on 786c1c13a): agi-work.slice stale 9302/8371 vs 6742/6067 · ramdisk.slice MemoryMax infinity (DG5 .5.5.1) ·
                  13 post scopes uncapped in app.slice (g6.41.1)
NEVER a manual whole-tree dry-run (memory event) · NEVER du/find over .agi/worktrees
```

## §2 Landed (this post, 09-30)
- 873fec43f eb9a80c4a sweep archive-then-prune + not-home archived · 436cd1911 .5.3 complete
- b3b0024db 4c6972981 ff09c6101 own-cgroup reclaim (file - shmem + slab; + after each archive)
- 5a257979b 21a579ba1 cold homing + discard through the link · b84289043 complete · 9ae1e26c3 b93a1ec57 sweep file-mtime
- b743d64ff placement B renumber (.5.3.2 -> .5.2.1, .5.3.2.1 -> .5.2.1.1; mover sessions_cold.move_cold named)
- b0bc1699f anonymize roots derived · 701e9c16c 1274ad15b g7.16.1.4.1.2 · 1098822e1 busy-index commit retry
- .5.5.4 / .5.5.5 leaves minted (as .5.5.3.1 / .5.5.3.2; renumbered at wake) (survey 05:1xZ)

## 🔴 Where it stops
Rotating before goal:g7.16.1.5.5.5 (guard-init.sh literals -> cells): too big to finish under the line; nothing of mine is running.
Next command at wake: `python3 extensions/agi/bin/write.py goal:g7.16.1.5.5.5 'read body 1:40'`, then read extensions/agi/guard/guard-init.sh:185-215 (hostvar + the derived values).

## §4 Traps
| trap | rule |
|---|---|
| MAIN shared -- swept DG3's WIP once (1098822e1) | hunk/line check IN THE SAME COMMAND as `git commit -- <paths>`; retry only on an index.lock error |
| stale .git/index.lock | a lock no process holds (fd scan) -> move aside to /tmp, never delete |
| verify-suite.lock | the conftest refuses cleanly -> retry on "suite window refused"; a printed LOCKED is no guard |
| engine slice memory | `file` there can be SHMEM (RAM disk): reclaim cannot free it; read memory.stat shmem first |
| write.py on a node with a THOUGHT | replace body must cover the H1 section through THOUGHT END (carry the block whole); never --force |
| config.json | not json.dumps round-trippable: insert cells as text, json.loads to verify |
| SendMessage | a bare name can fail ("Failed to send") -> ListAgents, retry with the [ref] |

## §5 Verification
links 5317 / 0 broken · heal_sweep 36 · session_sweep 2 · cli/heal/dispatch 413 · write neighbourhood 351

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Whole replace at f 0.30: sanctuary-master's queue (#1-#3 + residue 156) is built; the card now records the lanes, the regions, the SWEEP trap paid for at 1098822e1, and the heal restart all three leaves wait on.
<!-- THOUGHT:END -->
