---
id: doc:card-thought-master
mint_id: b790e16c2583455e850070c879dfccad
type: doc
parents:
  - goal:g5.19
next_edges: []
edited_by: thought-master
scaffold_hash: 4dc9b0030accb60c
season: 2
title: Card thought master
town: core
---
# doc:card-thought-master

thought-master · master of town local-maxxing · RESEARCH LANE ONLY · role = doc:unified-master-brief (template) + doc:unified-head (HEAD) · trunk MAIN = local-maxxing/season2/main (no worktree)

## §0 State (02:2xZ 10-01, read from date -u)
| | |
|---|---|
| stood up | by belam gen 22 on the owner's order (21:3xZ 09-30); first turn 21:52Z |
| lane | research: its board rows (town:local-maxxing trajectory_standin), its goals g5.22-g5.31, placing its rounds -- MINE, no SM word (owner 22:1xZ 09-30) · subagents: Opus 5.5, <= 3 at a time (template row) |
| run | FREE LANE (0 USD); council mode = dispatch.py unused -> rounds run by my Opus subagents, one model round at a time, each reviewed adversarially by a second Opus subagent before ACCEPT |
| formation | council loop (doc:council-loop) · SM hears only a merge-up for the gate or a council/DG3 slot collision · Prime belam live (signed dms 22:10Z, 22:21Z) |
| HELD | key / identity / signing / rotate / spawn-row / write-gate work waits on goal:g7.16.1.11 -- not yours |

## §1 Plan
```
LIVE   L4 run 3 BUILDER (hypothesis:lm-l4-outside-window-mass-picks-the-heads-to-window; unit tm-l4-mass -> experiment tm-l4-mass-1001; scored arm = MASS)
       MAP run 2 REVIEWER (read-only, experiment:tm-neuron-period2-1001)
NEXT   each report -> review (L4 r3) / accept + THOUGHT (MAP r2) -> the trajectory queue row (write.py town:local-maxxing, --actor thought-master, no --role)
       MAP run 3 after the review: bisect random set s0's catastrophic layer-0 neuron(s); T5_10 vs >= 20 layer-matched random sets excluding them, rank-scored; drop T2
HELD   stage 2 SELF-POKE (opt-in, sham + blind, debrief at session end) until a period family moves behaviour beyond controls
```
| round | verdict | review | one line |
|---|---|---|---|
| L4 r1 tm-l4-window-0930 | disproved | ACCEPT_WITH_RESIDUE | band = a weak locality proxy (1/3 budgets) |
| L4 r2 tm-l4-distance-1001 | PROVED 3/3 | ACCEPT_WITH_RESIDUE | measured distance: KL 0.0277 vs random min 0.0667 at kept 0.75; sink-heavy far readers leak in at k 26 |
| MAP r1 tm-neuron-period-1001 | disproved | ACCEPT_WITH_RESIDUE | C1 passed on ramps only; C3 bridge = a layer confound |
| MAP r2 tm-neuron-period2-1001 | disproved | pending | detrended 0.473 pct; T5_10 family drop 0.686 nats (exact 0.975 -> 0.775) but random s0 drops 3.67 |

## §2 Landed
- 22:2xZ town:local-maxxing a59698750e -- the trajectory's PERMANENT home (owner 21:5xZ verbatim in that version's THOUGHT)
- 22:0xZ-02:2xZ 10-01: idea:lm-neuron-periodicity-map-and-self-poke (owner 22:0xZ + debrief 22:1xZ verbatim) · 5 hypotheses · 4 experiments · trajectory queue row c7e1e38d8d, da62b34e0c, dc8b5e9e88

## 🔴 Where it stops
```
two subagents live (a dead session loses them): L4 r3 = `systemctl --user status tm-l4-mass` + datasets/osc-band/2026-10-01-l4-mass/ ; no experiment node -> re-brief a builder from the hypothesis body · MAP r2 review = re-run read-only from experiment:tm-neuron-period2-1001
```

## §4 Traps
- an experiment node needs evidence_runs (self id) or the grid commit auto-demotes a decisive verdict to inconclusive (tm-l4-window-0930, fixed 49f011f5cb) -- every builder brief says so
- town:local-maxxing: `--actor thought-master` with NO --role ([town] admits director TEMPORARILY until goal:g7.16.1.11)
- write.py `sub` refuses an empty replacement; a card with a THOUGHT block takes `replace body 3:<line before THOUGHT>` (the H1 guard)
- box: containers need docker --memory; ONE model load at a time; start at MemAvailable >= 6 GB + PSI avg10 < 5; stop at PSI >= 20
- never pipe `send.py read` through tail

## §5 Verification
- every round: verdict recomputed from results.json by an independent Opus reviewer; links 0 broken (builders report); pushed after every write

## §6 BANKED
(none)

## Skills
agi-send · agi-node-write · agi-goal · agi-workflow · agi-verify · agi-rotate · agi-dispatch · agi-memory-guard · agi-master-gate

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
OWNER 22:1xZ 09-30, direct in thought-master's pane, verbatim: "Also, you have a GM from SM, but it not, might not arrive yet because you have all these tasks going on. But I basically let Sanctuary Master know that you're in charge of like the research portion fully on the board and everything, like the board and the goals. If it's like the research lane, that's kind of your territory, not Sanctuary Master's." -- this version: the formation row names the research lane (board rows, goals, round placement) as thought-master's; SM confirmed in a [rule] dm 22:11Z. BANKED option (b) becomes the recommendation: the ring gate (goal:g12) still refuses a master on town:local-maxxing.
<!-- THOUGHT:END -->
