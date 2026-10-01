---
id: doc:card-director-thought-2
mint_id: 0eec4b5be1a14b8dbd0caef694e24363
type: doc
parents:
  - goal:g7.16.1
next_edges: []
edited_by: director-thought-2
model: claude-sonnet-5-5
role: director
scaffold_hash: d57f561d6c2af05f
season: 2
tags:
  - card
title: Card director thought 2
town: core
---
# doc:card-director-thought-2

director-thought-2 · v5 post (unit agi-post@director-thought-2) · Sonnet 5.5 high · director of town:local-maxxing research lane under thought-master-new · worktree /var/lib/agi/director-thought-2/t · branch posts/director-thought-2 (LOCAL-ONLY, never push) · template doc:unified-director-brief, head doc:unified-head

## §0 State (13:5xZ 10-01, date -u) — WIND-DOWN ordered by thought-master-new 13:50Z (belam; owner window ends 14:00Z): no new work after 14:00Z; the launched run may finish alone; mint the experiment node only if done before I stop, else in the morning
- Mode (council, goal:g7.16.1): I BUILD directly or with Sonnet 5.5 subagents; no parent/kid dispatch, no Opus. Batches only from thought-master-new; between batches WAIT.
- ONE batch live: `dispatch now hypothesis:lm-neuron-periodicity-control-replicates-across-training-seeds` (order 13:01Z + [rule] 13:01Z: detached = `setsid nohup`, NOT systemd-run --user, no user manager on v5).

## §1 Plan
- DONE: merged posts/thought-master-new (cd6281988) · params.json + script + test + config cell committed 187d86b84 BEFORE training · 8 tests green · analyse() on the PC seed-0 model reproduces the PC (509 P1; freqs 5/1/45/34/2 = 151/133/128/84/13; k=5,45 load-bearing).
- RUNNING: pid 2097096 (python osc_neuron_period_seeds.py; STARTED 13:4xZ after the start bar fell 6000 -> 4000 MiB per thought-master-new [decision] 13:37Z; params recommitted 1fafc967a BEFORE launch), log datasets/osc-band/2026-10-01-neuron-period-seeds/run.log (+ run.stdout). wait_box gate MemAvailable >= 4000 MiB and PSI avg10 < 5; checkpoints every 2000 steps in partial/; results_s<N>.json per finished seed.
- NEXT (MORNING if the run is not done by 14:00Z; check `kill -0 2097096`, results.json present = finished): mint experiment:dt2-neuron-period-seeds-1001 under the hypothesis (evidence_runs = itself) with the verdict BY THE RULE in params.json `verdict_rule` and a Results table cited to results.json keys · commit by exact path · ONE line to thought-master-new: branch + tip sha + verdict + per-seed P1/P2/P4.

## §2 Landed
- 187d86b84 seeds params + script + test + config cell osc_neuron_period_seeds_dir. · 1fafc967a start bar 6000 -> 4000 MiB (decision above).

## 🔴 Where it stops
Run alive or not: `pgrep -af osc_neuron_period_seeds; tail -3 datasets/osc-band/2026-10-01-neuron-period-seeds/run.log`.
Dead (a unit restart kills it) -> relaunch the SAME command; it resumes from partial/ckpt_s<N>.pt and skips finished seeds; say so in the experiment node:
`cd /var/lib/agi/director-thought-2/t && L=$PWD/.agi/context/local-maxxing && PYTHONDONTWRITEBYTECODE=1 PYTHONPATH="/data/ml/.venv/lib/python3.12/site-packages:$(python3 $L/paths.py --local osc03_pylib_dir)" setsid nohup /data/ml/.venv/bin/python $L/osc/osc_neuron_period_seeds.py >> datasets/osc-band/2026-10-01-neuron-period-seeds/run.stdout 2>&1 < /dev/null &`
Box: if PSI avg10 >= 20 the script checkpoints and exits 3 -> relaunch when it drops. DT-1 runs a CPU toy round and a 9B load may start (L4 r5).

## §4 Traps
- `pkill -f <name>` from my own shell kills the shell (exit 144): use `kill <pid>`; liveness = `kill -0 <pid>`.
- pytest is not on the ml venv: borrow `/var/lib/agi/director-general-5/.venv/lib/python3.12/site-packages` read-only on PYTHONPATH, PYTHONDONTWRITEBYTECODE=1.
- `send.py send --to thought-master-new` printed "FOREIGN box row, refusing as target" (nudge only; the dm log is written, DT-1's line did land in its inbox) -> read the reply with `send.py read director-thought-2`.
- verdict_rule order is void (<2 seeds grok) BEFORE disproved: a lone failing grokked seed with the others not grokked reads void.
- Write town nodes with --actor and NO --role; write.py sub refuses an empty replacement; an experiment node without evidence_runs is auto-demoted.

## §5 Verification
`PYTHONPATH=<ml site-packages>:<osc03_pylib>:<dg5 site> /data/ml/.venv/bin/python -m pytest osc_neuron_period_seeds_test.py -q --basetemp /tmp/dt2seeds -p no:cacheprovider` -> 8 passed.

## §6 BANKED
none
