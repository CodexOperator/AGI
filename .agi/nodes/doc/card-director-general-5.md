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
| **goal:g1.31.4.6.2** | **RESIDUES ALL CLOSED; re-mur 2 RUNNING, tip `5075d6dae`.** (a) the name refusal moved OUT of the strict-xfail into two non-xfail tests — it was invisible in a normal run · (b) C1's five dead asserts now execute against a faithful seam · (c) suite account corrected · (d) `testable_claim` + "What landed" corrected · (e) `## Dispatch line` added | SM: re-mur `old_tip baf2cc2d7dadcb2da55ef87edbbe25462f3edf4c` → `new_tip 9d8f354df`. I cannot dispatch — `.env` |
| **mur-2 (review_c2b.json): 3 NOT_MET, all closed at `2a0152805`** | (a) the a00-273b2e39 conjunct was read against the SUPERSEDED `9d8f354df` — fixed already at `5075d6dae`; but it found REAL damage I had missed: that node's BODY still said "THE SEAM IS A LIST" and told the next agent to name the seam from `_ROW_WRITE_SEAMS` — a landed record re-instructing the mechanism this round deletes. Section, probe rows and "Left to" item corrected; both surviving mentions sit inside the correction that says it is deleted · (b) suite account is now ONE, falsifier-table row 3, checkout named: `9d8f354df` → 354 passed / 0 failed, base `baf2cc2d7` → 350 / 0, delta +4/+3/0 — I adopt the reviewer's numbers, mine are the same 354 with 5 flipped by this seat's missing `origin` · (c) the Dispatch line WAS truncated mid-sentence, my own damage; now complete in the schema's `config-max / template-max / code` shape |
| **mur-2 LANDMINE — CONFIRMED and defused, `4081f2432`** | SM found that `test_a_correctly_repointed_write_under_another_name_is_refused_by_name` was green ONLY while `write.ONE_ROW_WRITE` was absent: the day the re-point lands it goes RED, because the refusal then arrives via the COUNT, not the contract. I reproduced it BEFORE touching anything (a `-p` plugin defines the seam; no tree bytes touched) — it is worse than brittle, it PUNISHES the fix. Both tests are now hermetic: one deletes the seam to test the wrong-name world, a NEW one installs it to test the bypassing path on the count. 5 passed in world A (not landed) AND world B (landed). `evidence_runs`: a00-35ca5dd6 self-citation -> `[]`; a00-273b2e39 scalar -> JSON list. `links.py links` 0 broken, `links.py schema` clean |
| **my own near miss** | the fix for (a) was **decorative at first**: it asserted the bare name, which the count assert's message also prints, so it PASSED with the `hasattr` deleted. Only mutation caught it. Now asserts the contract's distinctive phrase and goes RED under that mutant | none — fixed and committed |
| **residue (d) — MISSED, now fixed** | SM's (d) named TWO nodes; I answered for `a00-35ca5dd6` only and did not say I had skipped `a00-273b2e39-f74351`, so SM had to catch it. Now set there: `verdict: inconclusive_lean_disproved`, `evidence_runs: hypothesis:a00-35ca5dd6-f4f87a`, corrected `testable_claim` — plus its `probes:` P1/P2/P3 corrected off the deleted `_write_row` name | none — fixed, `5075d6dae` |
| goal:g4.18.5.3 | **DG1's node — I did not write it.** Falsifier 1 must name `write.ONE_ROW_WRITE`; the guard is inert until it does. C3 must declare `post-rename` an exception with a test | DG1 (asked twice) |
| goal:g1.31.4.2.1 (#40 #42 #31) | DG4's worktrees | SM owns |
| goal:g1.31.4.1 (#8 #9) | CLOSED 10-01 | — |
| goal:g7.16.1.5.4 | closes when the RAM worktree count is 0; `/mnt/agi-ram` denies me | SM/box |
| goal:g1.31.5.3, g4.18.5.6, g7.16.1.5.5.x | not dispatched — need a dispatch path I do not have | with the `.env` decision |
| **`send.py read` reports empty on unread mail** | RESOLVED as a symptom, SM 17:2xZ diagnosed it precisely: my cursor sat at inbox line 120, PAST their `[decision]` at 119 — the cursor advances past unread mail. Not mine to fix; I stopped re-reporting it as open. |
## 🔴 Where it stops
```
Round committed on the loop branch, residues closed, merge-up re-sent to SM.
I cannot run the mur: .env is 0640 and every director seat is outside it.
Next command (pickup post):
  git -C /var/lib/agi/director-general-5/wt-462 log --oneline -3
```

## §4 Traps
| trap | rule |
|---|---|
| **no director seat can dispatch** | `workflow.py run` dies in `provisioning.available()` on `/data/work/agi/.env` (0640). Not even `--dry-run`. Every "cut a round, re-mur" row of mine is unexecutable |
| **write.py body offsets SHIFT after every write** | I re-used one stale offset across three writes and duplicated a section, then had to restore from a known-good commit — 11 noisy commits on the node. Re-derive the offset with `read body N:N` IMMEDIATELY before every `replace body` |
| the ACL is fixed | `season2/*`, `.agi/worktrees`, `.agi/sessions/.spawn-budget` writable since 15:0xZ 10-01 |
| **a RAM worktree symlink breaks the suite for EVERY seat** | `/mnt/agi-ram` denies me; `conftest.py:192` `if not wt.is_dir(): continue` does NOT skip it, because `Path.is_dir()` swallows ENOENT/ENOTDIR/EBADF/ELOOP but NOT EACCES — PermissionError kills the whole file. SM's `a00-d311e8c8` (17:06Z) armed it. Patched LOCALLY to measure, reverted, deliberately NOT in my commit (outside my file scope, not my tree). One-line fix is SM's |
| **assert the distinctive phrase, not the name** | asserting `_ONE_ROW_WRITE in str(exc)` was satisfied by an unrelated message → a decorative test. Mutate the code and confirm RED, every time |
| **pytest runs, in a private venv** | `~/director-general-5/.venv`; `--basetemp` under my own path |
| **two module objects for one file** | tests `from agi.bin import rotate`, rotate imports bare `write`. Patch `item.module` / `sys.modules["write"]`, never the plugin's copy |
| **the 5 reds are my SEAT's env** | no usable `origin` here; the reviewer measures 0. Never phrase it as "pre-existing" — that reads as a property of the tree |
| the ACL is fixed | `season2/*`, `.agi/worktrees`, `.agi/sessions/.spawn-budget` writable since 15:0xZ 10-01 |
| MAIN is shared with 9 posts | commit by exact path; never touch another post's file |
| verify-suite.lock | every runner holds it per file; pytest inside it ERRORs at setup |
| systemd user manager sets TMPDIR=/data/tmp | pin `env -u TMUX -u TMUX_PANE TMPDIR=/tmp` |
| replace body on this card | §0 slice is 1..75; re-derive before every write |

## §5 Verification
`links.py links` 5367 resolved, 0 broken · guard `1 passed, 4 xfailed` (still strict-xfail RED — correct, the re-point has not landed) · full `test_rotate.py` in this seat `5 failed, 349 passed, 1 skipped, 5 xfailed` (the 5 = no `origin` here; reviewer measures 0) · both mutants re-run: seam-writes-nothing → RED, hasattr-deleted → RED

## §6 BANKED
**`.env` blocks every director dispatch (owner decision, banked not taken).** `workflow.py run` cannot even dry-run from any `agi-*` seat. Recommendation: leave it shut — it is the owner's money — and let SM/belam run every mur, which is how the council already works. The alternative, if directors are meant to review their own rounds, is a `group:agi` READ entry on `.env` alone, 0640 unchanged. I touched nothing under `.env`.

**PARITY, unresolved and cheap to close:** `config:engine`'s projector selects `.engine.v==4`, so DG5's seat is pi-free/medium while its board rows come from a claude-code opus-5-5 high lane. Both in the graph, they disagree. No red: the run works, it is just not the run the config describes.

**The node's body ORDER is still not normalized** to `[hypothesis]` (Measured · CLAIM · Dispatch line · FALSIFIERS · TESTS · FILE SCOPE · CEILING). It predates the rule and carries a landed round's shape; renaming its sections would rewrite a record SM has already read. Master's call, not mine.

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Stood up by belam-S2-L5-XVIII on the owner 23:3xZ order, verbatim: "Restart council including DG5 stand up. Then let them tackle the bundle and see how best to streamline it further." Lane per the owner 23:1xZ: "If needed, spawn director-general-5 as well and have them tackle the rotate/spawn unification/template+config gutting and streamlining."
<!-- THOUGHT:END -->
