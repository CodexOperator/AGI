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
| 10-01 row says stood down, post is LIVE | `recover: false`, `pid: 0`, yet belam restarted this seat and two sessions ran 11:1xZ and 15:0xZ. The row and the reality disagree; `spawn_budget.py status` reads 0/30. Flagged to SM — a row that says down while a seat spends is a lie the heal will act on |
| skills | agi-dispatch · agi-corrective · agi-workflow · agi-master-gate · agi-goal · agi-node-write · agi-verify · agi-memory-guard |
## §1 HANDOVER (every unfinished leaf / row)

| goal / row | state | next command |
|---|---|---|
| **goal:g1.31.4.6.2 — C2** | **CLOSED by me, committed `ac0f3a319`.** The guard's seven-name guess is gone: the seam is contracted to `write.ONE_ROW_WRITE` (goal:g4.18.5.3 Falsifier 1) and `hasattr` on it is the guard's FIRST assert, so a correct re-point under any other name now stops LOUDLY instead of xfailing green-looking forever. Both worlds measured. Suite: 5 failed / 346 passed, the 5 **pre-existing** (identical with my change stashed) → 0 regressions | SM/belam: run the mur — `workflow.py run merge-up-review --harness claude-code`, old_tip `baf2cc2d7dadcb2da55ef87edbbe25462f3edf4c`, new_tip `83f492f11`. I cannot: `.env` is 0640 |
| goal:g1.31.4.6.2 — C1 | UNCUT. The "changes ONLY through that one call" assertions still have no committed test executing them. Needs a round, which needs a dispatch path I do not have | with C3 |
| goal:g1.31.4.6.2 — C3 | measured + written up on the node; NOT applied. `cli.py` `post-rename` (:4264→:4281-4284/:4314) commits posts.md by hand, outside any seam. Belongs to goal:g4.18.5.3 (DG1's node) | DG1 + SM |
| goal:g4.18.5.3 | **DG1's node — I did not write it.** Falsifier 1 must name `write.ONE_ROW_WRITE` (the guard is inert until it does); C3 must be a declared exception with a test | DG1, asked 15:4xZ |
| goal:g1.31.4.2.1 (#40 #42 #31) | DG4's worktrees. mur `agi-director-general-5-mur4210609` was RUNNING at last check | SM owns |
| goal:g1.31.4.1 (#8 #9) | **CLOSED 10-01** — ancestor of origin trunk, 0 ahead | — |
| goal:g7.16.1.5.4 | falsifiers 1+2 hold; closes when the RAM worktree count is 0. `/mnt/agi-ram` denies me | SM/box |
| goal:g1.31.5.3 (n33 129 130 139 76 107) | not dispatched — n129/n130 overlap .4.2.1, n107 overlaps .4.6.2's test_rotate.py xfail | dispatch after both land |
| g4.18.5.6, g7.16.1.5.5.7, g7.16.1.5.5.6, g7.16.1.5.5.1 | horizon / active; all need a dispatch path | with the `.env` decision |

## 🔴 Where it stops
```
Round COMMITTED on the loop branch and handable. I cannot review or dispatch it:
.env is 0640 and every director seat is outside it. That is deliberate and I am
not proposing to change it — it is banked for the owner as a decision.

Next command (pickup post):
  git -C /var/lib/agi/director-general-5/wt-462 log --oneline -3
```

## §4 Traps
| trap | rule |
|---|---|
| **no director seat can dispatch** | `workflow.py run` dies in `provisioning.available()` on `/data/work/agi/.env` (0640). Not even `--dry-run`. Every "cut a round, re-mur" row of mine is unexecutable by me — the mur is SM's/belam's |
| **pytest runs, in a private venv** | `~/director-general-5/.venv` (9.1.1 + pyyaml), shared box untouched. `--basetemp` under my own path — `/tmp/dg5` is root-owned and ERRORs |
| **two module objects for one file** | tests do `from agi.bin import rotate`; rotate imports bare `write`. A `-p` plugin patching `rotate` ≠ the test module's `rotate`. Patch `item.module` / `sys.modules["write"]`, never the plugin's copy |
| **an xfail is not a measurement** | `4 xfailed` prints under a correct re-point, a wrong one, and no probe at all. `--runxfail` + a probe that COULD have flipped the result |
| **a vacuous probe proves nothing** | installing an UNCALLED seam leaves count 0 in both worlds — that was DG4's C2 probe. Route the path through the seam, then vary only the name |
| **5 pre-existing reds in test_rotate.py** | push/mirror-refusal tests, no usable `origin`. Attribute them with `git stash` + re-run before blaming a change |
| the ACL is fixed | `season2/*`, `.agi/worktrees`, `.agi/sessions/.spawn-budget` all writable as of 15:0xZ 10-01 |
| MAIN is shared with 9 posts | commit by exact path; never commit, reset or stash another post's file |
| verify-suite.lock | every runner holds it per file; pytest inside it ERRORs at setup |
| systemd user manager sets TMPDIR=/data/tmp | pin `env -u TMUX -u TMUX_PANE TMPDIR=/tmp` |
| a watch grepping "failed" | matches "xfailed": grep "[0-9]+ failed" |
| replace body on this card | start at the first `## ` heading (never the H1); the §0 slice must NOT be re-prepended — that duplicated it once (`82c86c277`, corrected `ccf06184d`) |

## §5 Verification
`links.py links` 5629 resolved, 0 broken · guard baseline `1 passed, 4 xfailed` (still strict-xfail RED — correct, the re-point has not landed) · full `test_rotate.py` 5 failed/346 passed/1 skipped/5 xfailed, the 5 reproduced with my change stashed · both probe worlds re-run per the node's reproduction block

## §6 BANKED
**`.env` blocks every director dispatch (owner decision, banked not taken).** `provisioning.available()` raises `PermissionError` on `/data/work/agi/.env` (0640), so `workflow.py run` cannot even dry-run from any `agi-*` seat. Recommendation: leave it shut — it is the owner's money — and let SM/belam run every mur, which is how the council already works. The alternative, if directors are meant to review their own rounds, is a `group:agi` READ entry on `.env` alone, 0640 unchanged. I touched nothing under `.env`.

**PARITY, unresolved and cheap to close:** `config:engine`'s projector selects `.engine.v==4`, so DG5's seat is pi-free/medium while its board rows are written from a claude-code opus-5-5 high lane. Both are in the graph and they disagree. No red: the run works, it is just not the run the config describes.

**Two sessions, two different blockers, and the shape is worth keeping:** the first was the box refusing to let a seat *write*; the second is the box refusing to let a seat *spend*. The write side was fixed by one `-R` and this post immediately cut the round it had been blocked on for two sessions. The spend side is a policy boundary, not a defect — and the honest reading is that directors in this formation are meant to build, not to pay for reviews.

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Stood up by belam-S2-L5-XVIII on the owner 23:3xZ order, verbatim: "Restart council including DG5 stand up. Then let them tackle the bundle and see how best to streamline it further." Lane per the owner 23:1xZ: "If needed, spawn director-general-5 as well and have them tackle the rotate/spawn unification/template+config gutting and streamlining."
<!-- THOUGHT:END -->
