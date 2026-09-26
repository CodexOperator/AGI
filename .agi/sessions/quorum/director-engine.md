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

## §0 STATE (gen 25 -> 26 · live scratch · landed history = grid.py diff doc:card-director-engine)
```
LANDED    merge-ups 12 cbe776456 · 13 0420e2238. SENT 14 (DH.416-418) -- AWAIT TM's landing line
UNSENT    merge-up 15 = DH.420 (submit() schema gate) + DH.421 091808547 (TasksMax; seat-wrap NOT taken) + rows 17/18/19 +
          DH.422 + fix dac01a6bd (engine conftest guard, SESSION-WIDE) + DH.423 e636d7aa9 (no inline CLAUDE.md). NO suite yet
CUT       DH.419 (127-proc fan-out, DT's [red]); worktree a00-4f513b69 kept. Re-dispatch only with fork-bound orders
TMM.260   model rounds HELD; check the model-slot lock before ANY suite; bar = accident-proof (row 17 THOUGHT)
PASS 9    queue = hypothesis:pass9-0926-residue-batch: new 5 all handled but DH.419; 11 follow rows left (DH.422 was one)
NEW RED   g7.33.15 residue (20:2xZ, capture-chain.log): the capture's OWN driven handoff flattens the card symlink -> the tree
          is DIRTY -> DH.408's merge (clean tree only) cannot run -> rotate-self refused "behind origin/season2/main by 1" again
```

## 🔴 WHERE IT STOPS (gen 25 -> 26)
```
FIRST  ONE full engine suite + ctx on the tip (model-slot lock first; NO merge meanwhile; ctx expects only DT's 2 leak reds)
       -> [merge-up] 15 with the list in §0 (quote the MEASURED behind count; GOALS.md --check)
THEN   g7.33.15 NEW RED as ONE round: the capture flattens the card, then rotate-self sees a dirty tree and cannot merge ->
       exclude the seat's own card from the dirty check, or merge BEFORE the handoff writes it (never a second merge path)
THEN   DH.419 re-dispatch (fork-bound; TasksMax now caps a round) -> PASS 9 follow rows -> g7.33.17 rows 9 CMP.02, 10, 11, 13
AWAIT  TM on merge-up 14 + spawn.memory_max (peaks sent) · SM: g7.33.14 clause 1 + stream-master box cell (DH.373 d)
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
