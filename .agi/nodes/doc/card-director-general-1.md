---
id: doc:card-director-general-1
mint_id: 241494f333d2430abc688586909a2c99
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: belam
scaffold_hash: ce9da8b3b952451b
season: 2
title: Card director general 1
town: core
---
# doc:card-director-general-1

# doc:card-director-general-1 — director-general-1's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (02:12Z 09-30 — RESUMED after the planned reboot (belam = agi-c2, 02:1xZ); this session = agi-2a; f≈0.23)
| | |
|---|---|
| post | director-general-1 |
| stage | NEW LOOP (owner 23:5xZ, doc:council-loop "The loop"): DG2 hands rows after its MVP-vs-hypotheses pass -> DG1 checks BUILD nodes vs GOALS -> correctives as NESTED subgoals -> no residue -> OUTCOME per goal (parent = the goal) -> SM |
| protocol | doc:council-loop · goal:g7.16.1 · NOT in room directors (DG3/4/5 only, belam 23:5xZ) |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 high |
| skills | agi-goal · agi-node-write · agi-send · agi-rotate · agi-post |

## §1 Plan
```
done   outcomes FINALIZED bundles 1-3; SM bigger_outcome 4ae3324b2 reviewed by council -> goal:g7.16.1.1.6 (DG2 part 1: 4 new verdicts A,B disproved+forks · C,D proved)
done   W0 g7.16.1.4.2 · W1b + W2a correctives (2c94133cc) · W1a correctives goal:g4.18.5.1.1 + .1.2 (77234eb7a 0ded56936; DG2 kept ONE fork spanning both)
done   census split: goal:g7.16.1.1.6.1 (config:census + check_census) + .6.2 (home-path row), both DG3 (9757e298e 2d5e7b03e)
done   SM residue 101: goal:g4.19 horizon + F3 -> goal:g4.18.7.3 F1; seed hypothesis:l4b15-intercept-layer claim realigned (11342dd8e 76597d04c 61bc32084)
done   SM residue 113 (falsifier half): goal:g7.16.1.2.7 F2 -> THOUGHT:\(?(BEGIN|END) (68611cef9 1a99824a6); finding write.py:217 prefix recognizer -> DG2 B fork, told DG3
done   W1a build-vs-goal: goal:g4.18.5.1.1 + .1.2 COMPLETE (688c00d08 95c64b6fd) on verdict:dg2mvp-w1afix2 PROVED 0.9; parent g4.18.5.1 waits for the bundle-4 outcome
done   W2b.1 build-vs-goal: goal:g4.18.6.2.1 COMPLETE (a81bd0f68) on verdict:dg2mvp-w2b1 0.8; per-id rebuild fork -> rides goal:g4.18.6.2.2
hold   W2a build-vs-goal: goal:g4.18.6.1.1 unmet on 3 bullets (title raw x74 · N resolves = N builds · links.py -h still '32-hex'); DG2 fork hypothesis:mint-index-decodes-titles-and-resolves-over-one-index + asked to add the -h line; close .1.1 when it passes
hold   W-G goal:g7.16.1.4.1: SM re-review CLEAN (00:5xZ) · DG1 smoke rc 0 node_count 5283 (5045+238), broken 0 · .4.1.1 COMPLETE (d5cfcf7d7), F2 exclusion dropped (3c5abfdc0) · closes when goal:g7.16.1.4.1.2 (DG4, config prose, 4a7109f3d) closes, citing one clean rotation closeout (Prime 00:56Z rotation, in flight at 00:5xZ)
done   SM residue 128 outcome half: bundle-1 F-row + bundle-2 R3 restated to the /home class (4fcdfac2c b58791552); SM CLOSED 128-outcome + 101
next   goal:g6.41.1 (assigned DG1): belam hands a leaf -- the reboot path gives a --resume'd post NO first turn (Prime sat idle 02:02:47Z until the owner typed); rotation's after_join wakes, the reboot path does not
next   bundle-4 OUTCOME when SM hands it (residues open) · g7.16.1.6/.7 leaves when alive places them
```

## 🔴 Where it stops
Waiting for handoffs: belam's g6.41.1 leaf · DG2's mint-index fork pass · DG4's goal:g7.16.1.4.1.2 · SM's bundle-4 outcome. MESSAGING (owner verbatim, until the bundles land): "use internal messaging only for everything and full guarantee until bundles land. Use the town bundles and goal nodes to coordinate context among the council and directors." = SendMessage by session name (ListAgents) ONLY -- NO send.py, NO rooms. Session names change at every relaunch: re-run ListAgents before each send. /tmp is wiped by a reboot. Check git status after each write.
```
python3 extensions/agi/bin/write.py goal:g6.41.1 'read body 1:60'
for g in g4.18.6.1.1 g7.16.1.4.1.2 g7.16.1.4.1; do grep -h '^status' .agi/nodes/goal/$g.md; done
```

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

## §5 Verification: `links.py links` 0 broken · anonymize ok on each diff

## §6 BANKED
(none)

Paid-for path guard: never create `.agi/bin/snapshot-build-site.py` or `.agi/bin/render-context.py`; never recreate `.agi/context/kits/` or `.agi/context/plans/build-site.md`.
