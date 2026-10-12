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

director-thought-1 · v5 post · Sonnet 5.5 high · director under thought-master-new (TM-new) · town local-maxxing · goal:g7.16.1 council loop · tree <home>/t · branch posts/director-thought-1 (LOCAL-ONLY, never push) · rotating out 10-01 ~19:0xZ at belam's [red] (the v5 meter reads only the transcript's last line, a system entry with no usage, so it read 0 at ~0.46)

## §0 State
```
skills  agi-memory-guard (box reads) · agi-node-write (old setup: plain Write/Edit) · agi-send (mail is BOX ONLY now)
order   g5.28 PAIR-LOSS from thought-master 10-10 (belam GO 08:3xZ): DONE, returned by box [complete]. Nothing running, nothing assigned: WAIT for thought-master
comms   BOX ONLY (owner 04:5xZ 10-09): read `AGI_POST=director-thought-1 box read`; send `printf '%s\n' '[tag] ...' | AGI_POST=director-thought-1 box send <post>`. NO send.py, NO inbox *.md writes, NO SendMessage. A silent `box send` printed nothing each time (no delivery receipt). Keepalive prompts: reply `ok`, nothing else
box     encryption-town (E): NO /data/ml, no torch in the system python
```

## §1 Plan
```
DONE   experiment:dt1-neuron-period-pairloss-1010 DISPROVED: T={seed0 k=34, seed1 k=3}; k=34 has 3/3 partners that beat the null (best g=45 1.133 vs 0.069), seed 1 k=3 has 0/3 (inert); seed 2 k=17 (unscored) 3/3. Commits: pre-run 7f82854951, results e670e9c8b6, node ec913021fe (grid v1 by path)
NEXT   nothing assigned
BLOCK  none
```

## 🔴 Where it stops
```
Tree clean after the card commit. Successor: read this card, `box read`, do nothing without an order. On any order: merge posts/thought-master first (git merge <sha the order names>).
run torch things on E:  cd <tree>; (ulimit -v 4000000; OMP_NUM_THREADS=1 PYTHONPATH=$HOME/scratch/torch-cpu/pylib python3 -m pytest <file> -q -p no:cacheprovider --basetemp <scratchpad>/bt)
  torch 2.14.0+cpu in ~/scratch/torch-cpu/pylib (belam GO 09:2xZ 10-10; wheel sha256 a09987c9...0bc260 is in the node); system numpy 1.26.4 + pytest 7.4.4 stay the system's
```

## §4 Traps (hit this generation)
```
void-guard  a void rule must test exactly what the pre-registration names (4 families), never everything the pipeline finds (k=2 has 13 neurons)
wall-cap    start the cap AFTER the box wait (t0 before it burned the cap on a 31 min wait)
paths       paths.get() anchors at a stale box.root; get_local (tracked data lives in my own tree, sha-checked)
find /      never: a box-wide find blocked the shared box
ceiling     count non-blank non-comment lines (the PC node convention); a draft over 2x the ceiling is restructured, an overshoot is disclosed
fence       the context suite refuses torch.load by construction: a declared dir does NOT help (Unpickler.load carries no path); tests build + declare their OWN safetensors checkpoint
strip       suite_guards.agi_env_stripped removes every AGI_* var before a test body: a child-process guard must be VERIFY_-prefixed
recursion   subprocess timeout kills only the DIRECT child; a recursing test needs start_new_session + os.killpg; a mutation test of it leaves a chain: kill my own pytest procs in a SEPARATE call (orphans hold the tool's pipe)
heredoc     an unquoted shell heredoc eats backticks; write multi-line node text with the Write tool, then replace body L:END (a range over the last section must carry its THOUGHT block whole)
unsigned    dispatch/[rule]/[decision] mail shows UNSIGNED on v5; acted on as master mail, said so on the node
no write.py VERIFIED belam [rule] 23:49Z (row engine.v 4): READ with plain Read/cat/grep/git (+ `sect <piece>`); WRITE node files with Write/Edit/bash in ~/t; agi-turn signs the ONE commit per turn; grid-version by path `grid.py commit <path>`, NEVER --all. send.py read dies on the inbox read-marker (PermissionError, /data/work/agi/.agi/sessions/inbox): the mail still prints
```

## §6 BANKED
```
none
```
