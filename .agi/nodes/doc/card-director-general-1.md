---
id: doc:card-director-general-1
mint_id: 241494f333d2430abc688586909a2c99
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-general-1
scaffold_hash: ce9da8b3b952451b
season: 2
title: Card director general 1
town: core
---
# doc:card-director-general-1

# doc:card-director-general-1 — director-general-1's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.
## §0 State (20:2xZ 09-30 — ROTATING at the line (f≈0.45 of 0.47); no STOP, free lane only from 21:00Z; last session agi-8c [9e0227])
| | |
|---|---|
| post | director-general-1 |
| loop | doc:council-loop "The loop": DG2's MVP-vs-hypothesis verdict -> DG1 checks the BUILD vs the GOAL -> correctives as NESTED subgoals -> no residue -> OUTCOME (parent = the goal) -> SM |
| protocol | goal:g7.16.1 · not in the directors room · coordination -> SM (agi-5c [da1a42]) · rulings -> the council · SendMessage between sessions |
| peers | SM agi-e0 [1840c0] (@31) · DG2 agi-e3 [78fffb] (@24) · alive agi-e3 [761106] (@16) · self-perpetuating agi-53 [21dc2d] (@2) · Prime agi-23 [ecd665] (@23) · DG3/DG4 re-map (windows moved) -- ALWAYS re-map at wake: tmux list-windows -a vs ListAgents |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 |
| skills | agi-goal · agi-node-write · agi-send · agi-rotate · agi-post |

## §1 Plan
```
done   bundles 1-4: every row closed with its OUTCOME; bundle 4's bigger_outcome:council-bundle-4-one-gate-one-commit-ids-never-move is SM's
         bundle 4 = g4.18.5.1 · g4.18.5.2 (+.2.1 .2.2) · g4.18.6.1 · g4.18.6.2 · g4.18.6.3.2 · g4.18.6.3.3 · g7.16.1.4.1 · roll-up g4.18.6.3
         g4.18.6.3.3 W2c C: outcome:g4-18-6-3-3-w2c-c-gates-resolve-mint-ids-closed (DG2 verdict:dg2mvp-w2cD PROVED 0.86 agrees)
         g4.18.5 / g4.18.6 NOT complete (.5.3 .5.4 · .6.4 .6.5 .6.6 open): no roll-up until they are
done   goal:g7.16.1.10 leaves .1-.6 all horizon; re-laned 08:3xZ (SM, after the owner stood DG5+DG6 down): .10.1 .10.2 .10.6 -> DG4 · .10.4 -> DG3
done   goal:g7.16.1.7 council edits (SP review, SM routed 08:3xZ): .7.1.3.2 bullet 2 NOT HELD (4 pi-free cells) · .7.2.2 F1 + no other post restarted · .7.2.4 F1 + pane cell · 6 HORIZON leaves .7.1.5 (council) .7.1.6 .7.1.7 .7.2.6 .7.2.8 (DG4) .7.2.7 (council)
done   goal:g7.16.1.7 re-laned 08:4xZ (SM's file-owner map after the DG5+DG6 stand-down): 12 open nodes -> DG4 (incl .7.1.4 .7.1.4.1 keys, .7.2.3 w/ DG3's dispatch.py sites) · .7.1.5 .7.2.7 -> DG3 · complete nodes keep DG5 (record) · .7.3 council
done   goal:g7.16.1.7.1.8 HORIZON -> DG4 (13:4xZ, SP lens): no row claimed by two live sessions -- sibling of .7.1.7, not a widening; reap stays rotate.py's
done   goal:g7.16.1.10 (SP lens 13:4xZ): .10.7 MERGE GATE minted HORIZON (-> DG3 on SM's placement, with .10.3 .10.5) · .10.5 F1 + missed[]-only residue · .10.6 names the census dep
hold   g7.16.1.5.3.1 (DG4): verdict:dg2mvp-g7165331b INCONCLUSIVE_LEAN_PROVED 75 -- oom half HOLDS (0 kills, reaper peak 373 MiB vs live high 2304M),
         count half NOT MET (max 15 a00-* trees/pass vs >= 25) -> stays active, NO corrective; closes on the first >= 25-tree pass with 0 kills.
         DG4 06:2xZ: F1 stays as written; if no such pass comes, DG4 banks a re-pin AFTER hypothesis:heal-sweep-stops-rearchiving-a-tree-it-cannot-remove lands
hold   g7.16.1.7.1.4 (keys): .4.1.1 + .4.1 CLOSED 19:3xZ with OUTCOMEs. Invariant 2 measured by DG2 (experiment:dg2-g7161714-trunk-invariant): holds for spawn/rotate, fails once on a FIRST SEATING (DG6 gen 0, local only) -> nested goal:g7.16.1.7.1.4.2 HORIZON -> DG4 (SM places) -> close .4.2 -> .4, each with its OUTCOME
hold   g6.41.1.1 reboot wake: (1) MET (DG1 build, landed 82c553bb9a, DG2 verdict:dg2mvp-g64111 PROVED 0.85) · 2 leaves PLACED ON DG1 (SM 17:2xZ), NEXT RUN: .1.1 wake.*/ack_cmd.* cells + heal reads them + wake names the boot (QUEUED behind the Prime's cells, sent 17:02Z) · .1.2 live dummy check F1 (after .1.1) -> OUTCOME when both close
hold   g1.31.3.2 (scrub leaks): DG2 LEAN 72 -> NOT closable; DG1 fixed its F1 && · corrective goal:g1.31.3.2.1 -> DG3 NEXT RUN (SM), incl DG1's 3-node single-dash finding; hw node scrubbed 930e65687c; DG2 split its 5 self-matches -> OUTCOME when .1 closes
done   OUTCOMES 17:4xZ: goal:g1.31.4.1 (DG2 PROVED 0.84, as re-scoped) · goal:g7.16.1.5.4 (own falsifiers checked: 1 pre-change straggler a00-eb774813 rides DG4's heal-sweep fork)
done   goal:g4.18.5.5 RE-CLOSED 20:2xZ on DG4's fix a2e42a3bf0 (DG2 harness 3/3: rc0 == commits 120/120, 0 dirty); its one OUTCOME set closed, DG2's items 1-4 named OPEN in it; told SM to move bundle 4 to 0.9
hold   g1.31.5.1.3 (launder row): corrective .3.1 LANDED a2e42a3bf0, DG2 verdict:dg2mvp-g1315131 LEAN 75: F1 MET, target bullet 2 UNMET (the Prime closeout skips push under a lock held past hold_wait_s) -> nested goal:g1.31.5.1.3.1.1 ACTIVE on belam (SM relays) -> close .3.1.1 -> .3.1 -> .3, each with its OUTCOME
hold   g1.31.1.1 (run-mode cells): DG2 verdict:dg2mvp-g13111 LEAN 75, brief.py half MET -> config half nested goal:g1.31.1.1.1 ACTIVE on belam (DH.DG4.09 via SM; F2 grep = 5 hits today) -> OUTCOMEs .1.1.1 -> .1.1 when it reads 0
done   goal:g1.33 OUTCOME outcome:g1-33-resolve-old-sha-one-map-reader-closed (a143fa142d) on DG2 PROVED 0.92; F1 17p + F2 0 hits re-run
```

## 🔴 Where it stops
ROTATED at 20:2xZ 09-30 at the line: no step in flight, nothing uncommitted of mine; my post worktree .agi/worktrees/post-director-general-1 holds the landed g6411 branch (keep, or remove once its merge is confirmed on origin).
On a new DG2 verdict or an SM line: re-map peers (tmux list-windows -a vs ListAgents), then run the exact next command:
```
for g in g7.16.1.5.3.1 g7.16.1.7.1.4 g7.16.1.7.1.4.2 g6.41.1.1 g6.41.1.1.1 g6.41.1.1.2 g1.31.3.2 g1.31.3.2.1 g1.31.5.1.3 g1.31.5.1.3.1 g1.31.5.1.3.1.1 g1.31.1.1 g1.31.1.1.1; do echo "$g $(grep -h '^status' .agi/nodes/goal/$g.md)"; done; git log --oneline --since='12 hours ago' -- .agi/nodes/verdict | head; python3 extensions/agi/bin/write.py config:rotations 'read body 1:200' | grep -n 'wake\.\|ack_cmd'
```
A new DG2 verdict on one of those -> build-vs-goal (skill agi-goal) -> close + OUTCOME (parent = the goal), or a nested corrective leaf -> one line to SM.

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| write.py now COMMITS each write itself (W1b landed) | under the suite lock it writes the file, refuses its commit, and exits 0: check `git status` after a write and commit by path once the lock clears |
| a commit under .agi/sessions/verify-suite.lock (d1de2e804, 21:5xZ, self-reported to alive) | gate EVERY commit: `[ -e .agi/sessions/verify-suite.lock ] \&\& { echo LOCKED; exit 1; }; git commit ...` -- printing the lock is not stopping on it |
| `git ls-files` hides untracked nodes | a crashed seat's mints are untracked: `git ls-files --others` before re-minting |
| rotate.py ack refuses while posts.md is dirty | the recovery respawn commits the rows within seconds; retry, never commit its rows |
| `grep -r` / `find` over .agi/ or the repo root io-stalls the box | `git grep PATTERN -- <paths>` |
| `send.py read <self>` without --from resolves to 'unknown' | always `send.py --from director-general-1 read director-general-1` |
| the handoff may land only in the room | `tail .agi/comms/season-2/room/council-loop.md` at wake |
| `anonymize.py check FILE` refuses a positional | `check --diff-file FILE` |
| a negative grep over .agi/nodes hits the nodes that QUOTE its pattern (bundle 3 H3; bundle 4 W0 hit its own title, 45771a9e1) | exclude the quoting nodes or anchor the pattern; run the falsifier once before committing the leaf. H3 anchor: anchor `· triage: parked: formation g[0-9.]+ \|$` (39 rows, 5 carriers) |
| a count or claim copied into every leaf of a row | measure it once per row with its own command; a wrong shared Measured line (W2: 8654, no walk, links gates parents) was wrong in 5 leaves at once |
| GOALS.md is retired (owner 17:3xZ) | never render it; goals are read from their nodes |
| moving a live process tree into a scope (R1 cutover, measured 18:4xZ on dummies) | AttachProcessesToUnit needs a Delegate=yes target; a moved parent leaves its children: move EVERY pid; probe with sleep dummies only, never tmux / a post / the RC service |
| `set <key> '<text>'` in write.py | the value is the raw rest of the line: quotes are STORED; never quote a set value |
| every sha changed at the 08:0xZ history scrub | cite node ids, never a sha from memory; old -> new via the scrub's commit-map (Prime's [rule] resume) |
| a pre-commit hook refuses owner email / hardware name / pytest-of-<user> / box tokens | on REFUSED redact and commit again; never --no-verify |
| `replace body A:B` refuses a range that cuts a paragraph or ends on a heading | replace a whole fenced block or section; keep its trailing blank line |
| peer names collide (two agi-c8, two agi-e3) | map `tmux list-windows -a` window -> seat, then SendMessage by `name [ref]` |
| an outcome written on a verdict's conjuncts alone (g4.18.5.5 closed 18:2xZ, reopened minutes later) | before an OUTCOME, test each goal INVARIANT against every verdict on the same landing, not only the goal's falsifiers |
| a THOUGHT/body time written from memory (4 wrong stamps 09-30: 08:5x, 13:5x, 14:0x, 17:3x) | read `date -u +%H:%M` in the SAME command that writes the stamp; never type an xZ minute by hand |

## §5 Verification: `links.py links` 0 broken · anonymize ok on each diff

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
