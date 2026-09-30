---
id: doc:card-all-is-one
mint_id: f3ab702d3c454a6aab2d41c2e88533d2
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: all-is-one
scaffold_hash: 15b137cded6cbf1b
season: 2
title: Card all is one
town: core
---
# doc:card-all-is-one — all-is-one's card (council loop, goal:g7.16.1): the ONE scratch

Replaced whole, never appended; ≤ 100 lines; written DURING the work so a dead session is resumable.

## §0 State (04:4xZ 09-30 — STOPPED on belam's relay of the 04:00Z council stop; IDLE; meter ~0.38)
| | |
|---|---|
| post | all-is-one |
| stage | council — embody vision:all-is-one ONLY ("everyone uses a unified set of tools ... same UI/UX by any role"); TOP-DOWN, generations, never the nitty gritty (doc:council-loop "The council's lens") |
| role (owner 02:5xZ 09-30) | "directors should reach out to council for rulings who discuss it among themselves using the lenses to keep you free. Remember the council IS prime to everyone else." alive convenes: one lens line to alive, alive sends ONE ruling; silence = agree |
| loop (doc:council-loop) | DG1 finalizes ONE outcome per goal · SM writes bigger_outcomes · council reviews -> new goals / bundles, or none -> season OVERVIEW nodes |
| place | local-town · MAIN /data/work/agi (RAM disk, same path) on local-maxxing/season2/main · claude-code Opus 5.5 high · CC session agi-8f / 242e8c |
| messaging (owner, until bundles land) | SendMessage by session name ONLY; NO send.py, NO rooms |
| usage (owner 03:2xZ 09-30) | "Directors spawning a lot of agents. Please make them use pi for agentic subtasks or sonnet 5.5. Were also out of usage" -> NO Opus subagents: workflow.py --harness pi-free, or Sonnet 5.5 at most |
| peers (04:xZ) | Prime belam = agi-79 · alive = agi-b3 · self-perpetuating = agi-53 · DG1 agi-2a · DG2 agi-7f · DG3 agi-91 · DG4 agi-80 · DG5 agi-5b — names change: ListAgents + tmux @id |
| skills | agi-node-write · agi-goal · agi-send · agi-rotate · agi-post |

## §1 Plan
```
done   bundles 1-3 reviewed; bigger_outcome 1-3 v2 accepted · placements for bundle 4, .6, .7 (7a/7b), g7.32.6 (Prime (a))
done   owner-task: goals rewritten from OWNER lines -- mine g7.32.6 586b72bdd + g4.18.5 5b40c0f49 (all 6 + .9 -> .7.3 landed)
done   owner-task: 12 S goals closed -- mine s7 (retired + leaf g4.18.6.6) · s35 -> g4.18.8 · s18 retired · s32 (retired + leaf g2.4.1); retire IN PLACE (adopted for all 12)
done   residue: s32 hyps re-homed -> g2.4.1; 5 closing verdicts by DG2 7211a6473; DG2 caught 2 errors of mine -> fixed 3067b0abc (g2.4.1 gained the apply_umap_coords bridge)
done   rulings (council as prime to directors): DG5 keys g7.16.1.7.1.4 = (C) own-box remint, box = AGI_BOX, rule = key_template row · DG3 `replace payload` NOT extended (refusal names `replace body`) · DG1 g4.18.6.2 = (b) body refs -> g4.18.6.4, one definition · DG3 residue 154 = (b) fail closed
done   05:0xZ RESUMED to 11:00Z (owner 04:5xZ; subagents + reviews on Sonnet 5.5, workflow.py pi-free) · g7.16.1.5 placement check to alive: A .5.5.3 restates .5.5 (retire -> pointer) · B two session-dir movers (.5.2 timer vs .5.3.2 heal under the worktree sweep) -> .5.3.2 under .5.2, one mover
       g1.31 (PASS B3 residues) measured: 47 upheld in 23/40 rounds + 147 missed, 0 leaves -> proposed to SM (agi-ed): DG6 first assignment, leaves by file cluster; write.py/node_writer -> DG3 lane, rotate/heal/spawn -> DG5 lane; SM AGREED 05:1xZ (SM rotating; successor holds the board)
       OWED when DG6 is seated (no posts row yet at 05:1xZ): SendMessage DG6 its g1.31 brief = goal:g1.31 FIRST assignment · 47 upheld residues (verify_*.json refuted:false, 23/40 rounds) triaged fix | answer-on-node | move, THEN the 147 missed rows · lane rule: write.py/node_writer -> DG3 lane, rotate/heal/spawn -> DG5 lane, rest -> DG6, leaves cut by file cluster · subagents Sonnet 5.5 · SECOND item: workflow.py headless claude-code stage route (SM pick)
open   horizon leaves awaiting placement: g4.18.6.6 (goal seeds derived) · g2.4.1 (embeddings cache + storage + bridge) · belam's g7.16.1.5 leaves (owner priority: worktree + RAM cleanup) not yet placement-checked
never  OVERVIEW until .6, .7 and bundle 4 close (all 3 agreed)
```
Lens questions for every ask: two paths for one act? · a role-only verb or flag? · a copy of a rule (one source)? · an overbuilt branch?

## 🔴 Where it stops
05:1xZ 09-30 resumed to 11:00Z; OWED: DG6 g1.31 brief the moment DG6 is seated (text in §1); then the next director ask
```
on wake: ListAgents (names change) · read any SendMessage · git log --since='2 hours ago' --format='%h %an %s' -- '.agi/nodes/goal/g7.16.1.5*' .agi/nodes/bigger_outcome
a director ask -> one lens line to alive (convener); a placement check -> read the leaf by id, one line to alive + belam
```

## §4 Traps
| trap | rule |
|---|---|
| MAIN is shared by every post | commit by exact path; never switch branches, stash or reset |
| write.py auto-commits, BUT refuses under verify-suite.lock / a busy index.lock | "commit refused" -> `git add -- <new file>`; `git commit -- <paths>`; a live index.lock = retry in a background loop, NEVER remove it |
| `git grep -h ... | grep -v <path>` | -h drops the paths, so the filter does nothing (my s18 error): filter WITHOUT -h, then strip |
| renumber a goal (no verb; `id` protected) | write.py edits FIRST, THEN `git mv` + the 3 identity lines (id, parents, goal_id) as ONE commit, THEN re-point refs via write.py |
| `set title` in a write.py script | value = the rest of the unit, NO quotes |
| ack after a crash | non-prime: `rotate.py ack --post all-is-one --session 5d1031fa --ref <ref> continue`; own row dirty from heal -> commit that clear by path first |
| `grep -r` / `find` over .agi/ | io-stalls the box: `git grep PATTERN <sha> -- <paths>` |
| write.py `sub` with `\n` | build the arg with python3 -c print(...) |
| .agi/sessions/quorum/all-is-one.md | a STALE tracked regular file (09-18 brief), not this card — not mine to re-point |

## §5 Verification: `python3 extensions/agi/bin/links.py links` 0 broken (03:0xZ: 5270 resolved, 0 broken)

## §6 BANKED
(none)
