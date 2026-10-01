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
thought_session: director-general-5
title: Card director general 5
town: core
---
# doc:card-director-general-5

Role = the director template + the HEAD (`doc:unified-head`) + the council protocol (`doc:council-loop`). This card is the ONE scratch: replaced whole, ≤ 100 lines; rules live in skills, progress on the town board.

## §0 State (09-30 06:2xZ · STOOD DOWN on the owner's order 06:1xZ via belam, verbatim: "We also will need to stand down director-general 5 and 6 to help conserve tokens as well. Just let them arrive at a stopping point and have them stop and take down the posts to free up resources. 3,4 can continue as is and pick up whatever 5,6 don't finish after standing down")
| | |
|---|---|
| post | director-general-5 · MAIN /data/work/agi on local-maxxing/season2/main · DOWN: recover false + pid 0 (belam) |
| pickup | DG3 / DG4 via SM's board: the HANDOVER table below is the whole state |
| split of record | rotate.py WHOLLY DG5 (now: whoever SM names) · dispatch.py launch resolvers · heal.py key path |
| ENGINE (measured 10-01 11:0xZ, not recalled) | this post's projected cells are **AGI_V=4, AGI_HARNESS=pi-free, AGI_MODEL=stealth/space-bunny-alpha, AGI_EFFORT=medium** (`config:posts` DG5 row `engine` object; env confirms). **It does NOT run engine v5**: `config:engine` marks v5 "PROPOSED v5 (owner GO 06:1xZ; doc:radically-simple-engine §Q+§R)" and the projector at `config:engine` sect agi-project selects `.engine.v==4`. Parity break to raise: the seat is projected pi-free/medium while THIS session ran the claude-code opus-5-5 high director lane — see HANDOVER-DG5-10-01.md |
| skills | agi-dispatch · agi-corrective · agi-workflow · agi-master-gate · agi-goal · agi-node-write · agi-verify · agi-memory-guard |

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
thought_session: director-general-5
title: Card director general 5
town: core
---
# doc:card-director-general-5

Role = the director template + the HEAD (`doc:unified-head`) + the council protocol (`doc:council-loop`). This card is the ONE scratch: replaced whole, ≤ 100 lines; rules live in skills, progress on the town board.

## §0 State (09-30 06:2xZ · STOOD DOWN on the owner's order 06:1xZ via belam, verbatim: "We also will need to stand down director-general 5 and 6 to help conserve tokens as well. Just let them arrive at a stopping point and have them stop and take down the posts to free up resources. 3,4 can continue as is and pick up whatever 5,6 don't finish after standing down")
| | |
|---|---|
| post | director-general-5 · MAIN /data/work/agi on local-maxxing/season2/main · DOWN: recover false + pid 0 (belam) |
| pickup | DG3 / DG4 via SM's board: the HANDOVER table below is the whole state |
| split of record | rotate.py WHOLLY DG5 (now: whoever SM names) · dispatch.py launch resolvers · heal.py key path |
| ENGINE (measured 10-01 11:0xZ, not recalled) | this post's projected cells are **AGI_V=4, AGI_HARNESS=pi-free, AGI_MODEL=stealth/space-bunny-alpha, AGI_EFFORT=medium** (`config:posts` DG5 row `engine` object; env confirms). **It does NOT run engine v5**: `config:engine` marks v5 "PROPOSED v5 (owner GO 06:1xZ; doc:radically-simple-engine §Q+§R)" and the projector at `config:engine` sect agi-project selects `.engine.v==4`. Parity break to raise: the seat is projected pi-free/medium while THIS session ran the claude-code opus-5-5 high director lane — see HANDOVER-DG5-10-01.md |
| skills | agi-dispatch · agi-corrective · agi-workflow · agi-master-gate · agi-goal · agi-node-write · agi-verify · agi-memory-guard |

## §1 HANDOVER (every unfinished leaf / row)

| goal / row | state | next command |
|---|---|---|
| **goal:g1.31.4.6.2 (#15)** | **C2 RESOLVED BY MEASUREMENT this session.** The guard counts calls into the NAMES in `_ROW_WRITE_SEAMS`; I routed `_ack_commit_seats` through a seam and changed only the NAME: `_write_row` → count 1, guard advances; `_write_one_row` → `seams present: NONE`, count 0, blind. **The verdict is a function of the name, not the code** — a correct re-point under any other name stays permanently green-looking. DG4's proposed probe is vacuous (installs an uncalled seam → xfail in both worlds). Fix already ordered: contract the name as a goal falsifier + `hasattr` first assert | SM/belam: commit the on-disk DH.1 (recovery command below), then ONE round for C1+C3 and the name-contract edit. No round needed for C2's finding |
| goal:g1.31.4.6.2 commit | DH.1 corrective + this measurement are ON DISK in wt-462, **uncommitted** — write.py writes, the `season2/loops/*` ref lock is refused by name | `git -C /var/lib/agi/director-general-5/wt-462 commit -q -m 'write.py: hypothesis:a00-35ca5dd6-f4f87a (director-general-5)' -- .agi/nodes/hypothesis/a00-35ca5dd6-f4f87a.md` (file already staged) |
| goal:g1.31.4.2.1 (#40 #42 #31) | DG4's (`dg4-c2c`, `dg4-fdreaders` worktrees). mur `agi-director-general-5-mur4210609` was RUNNING at last check | SM owns; my read last cycle: #31 a residue (hook_lines only PRINTS, writes no copilot hooks config) |
| goal:g1.31.4.1 (#8 #9) | **CLOSED 10-01** — ancestor of origin trunk, 0 ahead. The card's "STILL LIVE" was stale | — |
| goal:g7.16.1.5.4 | falsifiers 1+2 hold on DG5.01; closes when the RAM worktree count is 0. `/mnt/agi-ram` denies me | SM/box, not me |
| goal:g1.31.5.3 (n33 129 130 139 76 107) | not dispatched — n129/n130 overlap .4.2.1, n107 overlaps .4.6.2's test_rotate.py xfail | dispatch after both land |
| goal:g4.18.5.6, g7.16.1.5.5.7, g7.16.1.5.5.6 | horizon / active; all need a loop branch + worktree, both still denied | after the ACL fix lands |
| g7.16.1.5.5.1 | the proof is DONE and recorded on the node | SM reviews 1f81dbdbd |

## 🔴 Where it stops
```
STOOD DOWN (recover false, pid 0). Nothing of mine is live or detached.
Next command (pickup post): python3 extensions/agi/bin/spawn_budget.py status
```

## §4 Traps
| trap | rule |
|---|---|
| **the ACL fix is one level deep** | `.git/refs/heads` writable, `.git/refs/heads/season2` NOT. `setfacl` without `-R` leaves every subdir belam:belam: no loop branch, no worktree, no spawn_budget lock |
| **pytest runs now** | private venv `/var/lib/agi/director-general-5/.venv` (pytest 9.1.1 + pyyaml). `--basetemp` must be under my own path — `/tmp/dg5` is root-owned and pytest ERRORs on it |
| **two module objects for one file** | a `-p` plugin's `rotate` is NOT the test module's `rotate` (`id()` differs). Patch `item.module.rotate`; patching the plugin's copy measures nothing and reports `seams present: NONE` |
| **an xfail is not a measurement** | `-k calls_the_one_row_write` prints `4 xfailed` under a correct re-point, a wrong one, and no probe at all. Use `--runxfail` and a probe that COULD have flipped the result |
| MAIN is shared with 9 posts | commit by exact path; never commit, reset or stash another post's file |
| verify-suite.lock | every runner holds it per file; pytest inside it ERRORs at setup |
| systemd user manager sets TMPDIR=/data/tmp | pin `env -u TMUX -u TMUX_PANE TMPDIR=/tmp` |
| a watch grepping "failed" | matches "xfailed": grep "[0-9]+ failed" |
| replace body on this card | start at the first `## ` heading (never the H1), end on a blank line before the paid-for line |

## §5 Verification
`python3 extensions/agi/bin/links.py links` 0 broken · this session: guard baseline `1 passed, 4 xfailed`; discriminating probe re-run per the node's reproduction block · falsifier 2 `git grep '"hash-object" in inspect.getsource'` → 0 hits

## §6 BANKED
**BOX (re-measured 10-01 11:1xZ, one level deeper than last session):** belam's `setfacl` reached `.git/refs`, `.agi/sessions`, `.agi/comms/season-2/dm` and nothing below. Denied: `.git/refs/heads/season2{,/loops}`, `.agi/worktrees`, `.agi/sessions/.spawn-budget`. Committable: my post branch only. Fix (one command, `-R`): `setfacl -R -m u:agi-director-general-5:rwx /data/work/agi/.git/refs /data/work/agi/.agi`, per post; `.env` stays 0640 and must NOT join. Sent to belam (delivered) and SM.

**PARITY, unresolved and cheap to close:** the `config:engine` projector selects `.engine.v==4`, so DG5's seat is pi-free/medium while its board rows are written from a claude-code opus-5-5 high lane. Either the projection or the board is wrong; both are in the graph and disagree. No red: the run works, it is just not the run the config describes.

**DONE this session despite the box:** built the missing pytest (private venv, shared box untouched), which is what let C2 be measured instead of argued — the first substantive engine finding this post has landed in two sessions.

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Stood up by belam-S2-L5-XVIII on the owner 23:3xZ order, verbatim: "Restart council including DG5 stand up. Then let them tackle the bundle and see how best to streamline it further." Lane per the owner 23:1xZ: "If needed, spawn director-general-5 as well and have them tackle the rotate/spawn unification/template+config gutting and streamlining."
<!-- THOUGHT:END -->
