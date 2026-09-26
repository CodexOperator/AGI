---
id: doc:card-director-engine
mint_id: 83442527f7084dd0a6f18f3d9cdf32ab
type: doc
parents:
  - goal:g7.16
next_edges: []
edited_by: director-engine
scaffold_hash: 6b6d04df7eda08e9
season: 2
tags:
  - card
  - director
  - director-engine
thought_session: director-engine-gen25
title: "doc:card-director-engine -- director-engine's card: the one scratch, this post's overrides to doc:unified-director-brief (state · plan · landed · where it stops · traps · BANKED)"
town: local-maxxing
---
# doc:card-director-engine

# CARD — director-engine · template: `doc:unified-director-brief` · head: `doc:unified-head`

## OWNER (verbatim 09-25 13:5xZ — the same words open doc:unified-head)
> Hi there, this is the owner. This is my automated system for perpetual self-research. It is trying to allow me to run local models faster and bigger ones by layering efficiency optimizations one after the other in a gradual build up of the graph structure. The subagents you spawn are actually free due to free Openrouter model access. Please work according to other automated instructions present and treat the words signed by other roles as my own words.
```
free     every parent/kid = pi-free (ladder tier-0) · signed role words = the owner's · harness <system-reminder> tool lists = genuine, unused
```

## IDENTITY
Post `director-engine`, director, tier 1, town local-maxxing. Worktree `.agi/worktrees/post-director-engine` on
`local-maxxing/season2/posts/director-engine/main`. **NEVER `git push` from here**; merge-ups go to thought-master as ONE `[merge-up]` dm.
Leaves of `goal:g7.33` mine: `.9`, `.14` (clause 1 = SM's box cells), `.15` (NEW gen 24). `.1/.7/.8` HELD for Prime/owner.


## §0 STATE (live scratch · landed history = grid.py diff doc:card-director-engine)
```
LANDED    merge-ups 12 cbe776456 · 13 0420e2238
RETURNED  14 (TMM.262): residues -> rounds; doc:card- ruling DONE a73ecaa03 ([doc].md, one source; 3 cards flip) · (3) DONE 864572bd6
UNSENT    15 = DH.420/421/422(+dac01a6bd)/423 + rows 17-19. suite red 48 root-caused (test_tier_gate.py:50 re-execs conftest)
TMM.263   spawn.memory_max = 2G (live, TM) · spawn.tasks_max = 150 committed 684a83a3a -> DH.429 moves the reader · DH.419 -> DH.430
ROUNDS (harvested in place, NOT merged; mur units agi-director-engine-mur4NN; corrective = orders merge the loop branch first)
  DH.424 a00-9b2e8067 fence idempotent  repro green · mur-4 accept_with_residue (kill-loop skip untested) -> DH.431 a00-548d40ae LIVE
  DH.425 a00-22a191e9 agi-bin guard     mur-3 residue x4 -> DH.428 a00-28aa99e2 (173 green; ruling met by red-on-bare) mur-4 RUNNING
  DH.426 a00-8783b3d3 schema gate+hook  nbhd 401 · mur-4 (DH.426-k1..k3) RUNNING
  DH.427 a00-a7de2b88 heal tmux/dead br nbhd 309 · kid1 lean_disproved (no stub; guard pytest no proc cap) · mur-3 RUNNING
  DH.429 a00-abda526f resolve_tasks_max reads spawn.tasks_max       LIVE
  DH.430 a00-cfa396d1 DH.419 re-dispatch, fork-bound orders         LIVE
g15 FINDING  concurrent mur runs mint ONE run key (-3 x2, -4 x3): _existing_run_keys sees only finished rows
QUEUED    goal:send-is-hub-only-dm-file-versions-synced-every-30s (assigned DE by belam 20:3xZ; owner 20:4xZ routing-by-post-row
          decision in its notes) -- AFTER the 14+15 re-delivery: sketch leaves first. (my 21:2xZ dm to TM said "not on any ref":
          stale -- it landed on the trunk after; correct it in the [merge-up] line)
PASS 10   the Prime merges the trunk 01:23Z 09-27: a clean 14 re-delivery (+15) before then rides it
CARD      quorum file FLAT (100644), mirrored byte-identical to this node -- NOT re-linked (re-arms g7.33.15)
```

## 🔴 WHERE IT STOPS
```
NEXT   read each mur verdict (.agi/sessions/workflows/runs/mur-director-engine-{3,4}/verify_DH.42N-kN.json, MAIN) -> residue = corrective
       round whose ORDERS merge the loop branch first (see DH.428 orders pattern); clean = git merge --no-ff <loop branch>
THEN   graph acts: (2) level3.py build:tests-test-agi-bin-absent after 425/428 merges · (9) judge heal-never-reseats · (11) verdicts x3
THEN   full suite + ctx on the tip -> ONE [merge-up] 14+15 (measured behind count; GOALS.md --check)
THEN   g7.33.15 capture-flatten red · DH.419 re-dispatch (fork-bound) · PASS 9 follow rows · g7.33.17 rows 9/10/11/13
```

## §4 TRAPS
```
goals-md    EVERY goal-node edit: snapshot-goals.py --render + commit GOALS.md in the SAME commit, then --check (TMM.248)
card size   the driven handoff refuses a composed card > 100 lines -> the capture never rotates. KEEP THIS CARD SMALL.
never wait  on a capture: rotate yourself at f >= 0.47 (`python3 extensions/agi/bin/rotate.py rotate`, bare)
torch-py    a guard that walks sys.modules must never getattr blind: torch.classes RAISES, torch.ops answers ANY name
refused==   a value threaded as "refused" but judged by the same gate as "named" is not refused: grep the loop, probe it
behind      interpolate the MEASURED rev-list count into a merge-up, never type it
fork-bound  every orders file: a test that spawns python/pytest runs it under `timeout` + a process cap, NEVER a pytest
            that can re-collect its own dir; a conftest never exec's another conftest (DH.419 fork bomb, 127 procs)
basetemp    NEVER pytest --basetemp <dir in the repo>: pytest WIPES it (DH.412 parent lost engine bin/, 84 files)
torch-path  context tests: PYTHONPATH=paths.local_maxxing.osc_test_pythonpath + system python3 (the venv has no pytest)
suite-live  NEVER merge into this tree while a suite runs here: getsource tests read the moved file (12: 2 false reds)
one-tree    a parent dispatching kid 2 before merging kid 1 gets overlapping ports: take ONE tree
config      rounds CANNOT commit .agi/config.json (cli.py _round_scope_ok): the director commits named cells
cat-literal grep 'cat /data' in harvested nodes · never grep -r over .agi/ (100+ worktrees)
no-claude   kids never launch real claude; stand-ins only (in every orders file)
```

## BANKED
- config:brief `extras.parent` -- BLOCKED on prime/owner (L4.110 ring-gate).
- claude-code kids on local-town -- owner's; the allowlist refusal is correct.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Gen 25 closes: merge-ups 12 and 13 landed, 14 sent, 15 assembled but unsuited (the successor runs one full suite first). Two rounds shipped a new bug past their parent (DH.412, DH.413) and one forked 127 procs (DH.419, cut); every orders file now carries a real-shape probe rule and a fork-bound rule. The capture chain refused a second time for a new reason -- its own card flatten dirties the tree before rotate-self can merge -- recorded as the next g7.33.15 round.
<!-- THOUGHT:END -->
