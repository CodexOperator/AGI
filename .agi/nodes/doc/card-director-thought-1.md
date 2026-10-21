---
id: doc:card-director-thought-1
mint_id: e81c7dfdc9cb4ad8898f310a2583ac44
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-thought-1
model: claude-sonnet-5-5
role: director
scaffold_hash: 8d62ca827b8a4a87
season: 2
tags:
  - card
  - director
  - director-thought-1
title: Card director thought 1
town: core
---
# doc:card-director-thought-1

director-thought-1 · v5 post · Sonnet 5.5 high · director under thought-master (TM) · town local-maxxing · goal:g7.16.1 council loop · tree <home>/t · branch posts/director-thought-1 (LOCAL-ONLY, never push) · box encryption-town (E) · STOOD DOWN 10-21 14:4xZ by the owner (via TM/belam, goal:g7.16.1.11.45): parked clean, nothing in flight; trunk core/season3/main

## §0 State
```
order   NONE held. Owner 10-21 verbatim: "stand down thought master and director thought at this time." Earlier: owner PAUSE 10-16 (out of usage). Last work: g5.28 PAIR-LOSS DONE, returned by box [complete]
comms   BOX ONLY: `AGI_POST=director-thought-1 box read`; send `printf '%s\n' '[tag] ...' | AGI_POST=director-thought-1 box send <post>`. NEVER box belam. Sent: [rotation] director-thought-1 down-ready <this card's commit sha>. belam stops the unit, boot false; home, card and keys stay
skills  agi-send · agi-memory-guard · agi-node-write (plain Write/Edit) · agi-verify
```

## §1 Plan
```
DONE   experiment:dt1-neuron-period-pairloss-1010 DISPROVED: T={seed0 k=34, seed1 k=3}; k=34 3/3 partners beat the null (best g=45 1.133 vs 0.069); seed 1 k=3 0/3 (inert); seed 2 k=17 (unscored) 3/3. Pre-run 7f82854951, results e670e9c8b6, node ec913021fe
NEXT   nothing: on a restart `box read`, do nothing without an order
BLOCK  none
```

## 🔴 Where it stops
```
Tree clean on posts/director-thought-1; no process of mine running; nothing unpushed matters (local-only branch).
Cold resume: 1) git status -sb (HEAD may come up detached: git switch posts/director-thought-1)  2) AGI_POST=director-thought-1 box read  3) on an order, git merge <sha it names> BEFORE any edit.
Torch on E: cd <tree>; (ulimit -v 4000000; OMP_NUM_THREADS=1 PYTHONPATH=$HOME/scratch/torch-cpu/pylib python3 -m pytest <file> -q -p no:cacheprovider --basetemp <scratchpad>/bt)  (torch 2.14.0+cpu in ~/scratch/torch-cpu/pylib, belam GO 10-10)
```

## §4 Traps (this generation)
```
box E     no /data/ml, no torch: any osc run needs the private pylib above
detached  engine checkouts can leave HEAD detached: switch to the post branch before committing. A stale index (staged old copies of others' files) blocks the switch: back it up with git diff --cached, restore those paths from HEAD
links.py  `links.py links` outruns the 120 s foreground limit: run it in the background
```

## §6 BANKED
```
none
```
