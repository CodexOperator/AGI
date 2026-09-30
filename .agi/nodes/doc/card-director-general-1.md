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

## §0 State (05:21Z 09-30 — RESUMED to 11:00Z; f≈0.40 of 0.47; this session = agi-2a; SM now agi-5c, alive agi-e3 [761106])
| | |
|---|---|
| post | director-general-1 |
| stage | NEW LOOP (owner 23:5xZ, doc:council-loop "The loop"): DG2 hands rows after its MVP-vs-hypotheses pass -> DG1 checks BUILD nodes vs GOALS -> correctives as NESTED subgoals -> no residue -> OUTCOME per goal (parent = the goal) -> SM |
| protocol | doc:council-loop · goal:g7.16.1 · NOT in room directors (DG3/4/5 only, belam 23:5xZ) |
| place | local-town · MAIN /data/work/agi on local-maxxing/season2/main · claude-code Opus 5.5 high |
| skills | agi-goal · agi-node-write · agi-send · agi-rotate · agi-post |

## §1 Plan
```
done   bundles 1-3 outcomes; census split g7.16.1.1.6.1/.2 (DG3); residues 101 113 128 (goal side); W1a/W1b/W2a correctives nested
done   BUNDLE-4 OUTCOMES (on SM's ready + DG2 verdicts), each goal complete:
         g4.18.5.1 W1a rows ........ outcome:g4-18-5-1-w1a-body-rows-closed (556131169)
         g4.18.6.1 W2a resolver .... outcome:g4-18-6-1-w2a-one-mint-resolver-closed (0eef20bd9)
         g4.18.6.2 W2b ids ......... outcome:g4-18-6-2-w2b-write-checks-outbound-ids-closed (d156aeba7; council ruling (b): body refs -> g4.18.6.4)
         g4.18.6.3.2 W2c B ......... outcome:g4-18-6-3-2-w2c-b-family-b-one-resolver-closed (4965c5ff5)
         g7.16.1.4.1 W-G ........... outcome:g7-16-1-4-1-w-g-goals-md-retired-closed (523ea922b)
         g4.18.5.2 W1b ......... outcome:g4-18-5-2-w1b-a-write-is-a-commit-closed (c1e08cd3e; .2.1 efea591cc + .2.2 39f7081b1 on SM's accept)
         g4.18.6.3.3 W2c C ....... outcome:g4-18-6-3-3-w2c-c-gates-resolve-mint-ids-closed (e9b0fd51b; 690 passed on a clean HEAD export, 6 red attributed off-goal) -- DG2 verdict:dg2mvp-w2cD PROVED 0.86 cited (25df72bf9)
         g4.18.6.3 W2c roll-up . outcome:g4-18-6-3-w2c-every-link-reader-resolves-mint-ids-closed (a866d20bd) -- g4.18.5 / g4.18.6 NOT complete (.5.3 .5.4 · .6.4 .6.5 .6.6 open): no roll-up; SM writes bundle-4 bigger_outcome
hold   g7.16.1.5.3.1 (DG4): DG2 re-judge verdict:dg2mvp-g7165331b INCONCLUSIVE_LEAN_PROVED 75 (05:06:37Z-06:13Z, live bound 2304M): oom half HOLDS (0 oomd kills, NRestarts 0, reaper peak 373 MiB, 25 reclaim asks 0 refused) · count half NOT MET (max 15 a00-* trees/pass vs >= 25; F1 says partial until one occurs) -> DG1 build-vs-goal 06:1xZ: NOT closable, NO corrective (nothing to build), stays active until one >= 25-tree pass shows 0 kills · DG2's fork hypothesis:heal-sweep-stops-rearchiving-a-tree-it-cannot-remove belongs to goal:g7.16.1.5.3's tree (SM places)
done   goal:g7.16.1.10 sketched (council/alive): leaves .10.1-.10.6 (3e57d149e 473c6fa20 4a3aa81e6 940bf3a08 066c0b6cd fa3dddd95) -> DG6/DG3/DG5; build-vs-goal on each as DG2 passes them
hold   g6.41.1.1 reboot wake (mine): brief hypothesis:a-session-resumed-outside-heal-gets-one-after-join-wake (ff358c109) queued on DG3
hold   g7.16.1.7.1.4 (DG5) REOPENED 7be04f413/a5da5ccf0 on DG2 verdict:dg2mvp-g717114 LEAN_PROVED 72: Invariant 1 unmet on cmd_seats_launch (keys nothing) + cmd_loop successor (no key step); 159 (cmd_spawn) CLOSED at HEAD by 4feed71aa (DG2 read db69d66f9, before it) -> corrective leaf goal:g7.16.1.7.1.4.1 (narrowed dc9707329), seed DG2's hypothesis:stand-up-verb-keys-every-mode-through-key-template, placed DG5 by SM (lands with 158b) -> close both + OUTCOME when .4.1's verdict clears
```
## 🔴 Where it stops
STOPPED clean: no step in flight, nothing uncommitted of mine. Next session resumes on the three holds in §1 (W1b g4.18.5.2 after DG2 checks .2.1 + DG3 builds .2.2 · W2c C g4.18.6.3.3 · g6.41.1.1 build on DG3), in the loop order: DG2's verdict -> DG1 build-vs-goal -> OUTCOME (parent = the goal) -> SM. Owner orders in force (director brief): SendMessage only (no send.py, no rooms) until the bundles land; coordination -> SM, rulings -> the council; no Opus subagents (pi-free workflows, Sonnet at most). Session names change at every relaunch: map `tmux list-windows -a -F '#{window_id} #{window_name}'` against ListAgents. Check git status after each write (write.py can print success over an uncommitted node until g4.18.5.2.1 is verified).
```
for g in g4.18.5.2 g4.18.5.2.1 g4.18.5.2.2 g4.18.6.3.3 g6.41.1.1; do echo "$g $(grep -h '^status' .agi/nodes/goal/$g.md)"; done
git ls-files .agi/nodes/verdict | grep -E 'dg2mvp-(w1b|w2cC|g6)'
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
