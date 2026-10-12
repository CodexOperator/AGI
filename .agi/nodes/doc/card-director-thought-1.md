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

director-thought-1 · v5 post · Sonnet 5.5 high · director under thought-master (TM) · town local-maxxing · goal:g7.16.1 council loop · tree <home>/t · branch posts/director-thought-1 (LOCAL-ONLY, never push) · box encryption-town (E) · idle order 04:2xZ 10-12 LIFTED 05:0xZ (box rebooted 05:00:51Z, owner 'go'); nothing queued, periodicity side track PAUSED (goal:g5.28 horizon)

## §0 State
```
skills  agi-send (mail is BOX ONLY) · agi-memory-guard (box gate before a heavy lane) · agi-node-write (old setup: plain Write/Edit) · agi-verify
order   NONE held. Last: g5.28 PAIR-LOSS (thought-master 10-10, belam GO 08:3xZ) DONE and returned by box [complete]. Standing: the 04:2xZ idle order is lifted (TM relay 05:0xZ 10-12); the reboot wiped /tmp scratch and /run/agi-<post> (~/scratch/torch-cpu survived, checked)
comms   BOX ONLY: read `AGI_POST=director-thought-1 box read`; send `printf '%s\n' '[tag] ...' | AGI_POST=director-thought-1 box send <post>` (prints nothing, no receipt). NEVER box belam (owner 10-11 20:2xZ): anything for belam goes to thought-master, who folds it into the one ~4 h digest; only a [red] or a blocking owner ask goes at once. No [ack]/[thanks]/[landed] upward. A keepalive prompt: reply `ok`, nothing else
```

## §1 Plan
```
DONE   experiment:dt1-neuron-period-pairloss-1010 DISPROVED: T={seed0 k=34, seed1 k=3}; k=34 has 3/3 partners beating the null (best g=45 1.133 vs 0.069); seed 1 k=3 has 0/3 (inert, dCE 1.8e-8); seed 2 k=17 (unscored) 3/3. Pre-run 7f82854951, results e670e9c8b6, node ec913021fe
NEXT   nothing assigned: on resume `box read`, do nothing without an order
BLOCK  none
```

## 🔴 Where it stops
```
Tree clean, on posts/director-thought-1 (HEAD came up detached at the branch tip again after the 10-12 reboot (switched back); check `git status -sb` before any commit). No process of mine is running.
Cold resume: 1) git status -sb  2) AGI_POST=director-thought-1 box read  3) on an order, `git merge <sha the order names>` (posts/thought-master) BEFORE any edit.
Torch on E (none in the system python): cd <tree>; (ulimit -v 4000000; OMP_NUM_THREADS=1 PYTHONPATH=$HOME/scratch/torch-cpu/pylib python3 -m pytest <file> -q -p no:cacheprovider --basetemp <scratchpad>/bt)
  torch 2.14.0+cpu in ~/scratch/torch-cpu/pylib (belam GO 09:2xZ 10-10; wheel sha256 a09987c9...0bc260 is in the node); system numpy 1.26.4 + pytest 7.4.4 stay the system's. ~/scratch is in my home, not /tmp
```

## §4 Traps (this generation)
```
box E     no /data/ml, so no torch, no osc_test_pythonpath: any osc run needs the private pylib above; pip into a shared env is forbidden, a download needs a GO
detached  a checkout by the engine can leave HEAD detached at the branch tip: `git switch posts/director-thought-1` before committing, or the commit misses the branch
links.py  `links.py links` runs past the tool's 120 s foreground limit; start it in the background and read the output file
```

## §6 BANKED
```
none
```
