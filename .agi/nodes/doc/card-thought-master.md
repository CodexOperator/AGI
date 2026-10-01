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

## §0 State (22:2xZ 09-30, read from date -u)
| | |
|---|---|
| stood up | by belam gen 22 on the owner's order (21:3xZ 09-30); first turn 21:52Z |
| lane | research only: the town trajectory (town:local-maxxing trajectory_standin) + goal:g5.22-g5.31 · subagents per the template's `subagents` row (Opus 5.5, effort high, <= 3) |
| run | FREE LANE since 21:00Z 09-30 (0 USD); council mode = dispatch.py unused (doc:council-loop Rules) |
| box 21:53Z | GPU idle (72 MiB) · RAM available 9.4 GB · mem PSI some avg60 0.14 · no model container up |
| HELD | key / identity / signing / rotate / spawn-row / write-gate work waits on goal:g7.16.1.11 -- not yours |
| formation | council loop (doc:council-loop) · RESEARCH LANE = MINE: its board rows, its goals, placing its rounds -- no SM word (owner 22:1xZ; SM gen 11 22:11Z) · SM hears only a merge-up for the gate or a council/DG3 slot collision · Prime belam live again 22:10Z (signed [rule]) |

## §1 Plan
```
DONE   inbox · board + goal:g5 read · step named -> SM PLACED 21:57Z (gates: MemAvailable >= 6 GB, PSI avg10 < 5, detached, MemoryMax) · hypothesis:lm-l4-local-heads-keep-a-recent-window minted (801745ad98, v2 929a65952f)
LIVE   (00:2xZ 10-01) Opus REVIEWER of the L4 round (read-only, no model) + Opus BUILDER of stage 1 MAP (unit tm-neuron-period, MemoryMax 5G -> experiment tm-neuron-period-1001)
L4     experiment:tm-l4-window-0930 DISPROVED by the pre-registered rule (band beats random on agree AND KL at 1/3 budgets; KL alone at 2/3); measured-distance reference KL 3.6x lower at 0.75 -> candidate next rung, pending the review
MAP    hypothesis:lm-neuron-periodicity-map-finds-function-neurons minted 00:2xZ (idea:lm-neuron-periodicity-map-and-self-poke + goal:g5.28)
NEXT   review verdict -> L4 verdict + next rung onto the trajectory rows (town:local-maxxing, --actor thought-master, no --role) · MAP report -> its own review
DONE   owner's trajectory edit LANDED a59698750e 22:2xZ (town:local-maxxing: the trajectory's PERMANENT home)
```
STEP (ladder L4, goal:g5.22): L3 folds into L4 (idea:lm-why-l3-precision-allocation-wall-is-8-12-bits) -- band-energy key bits sit inside uniform's noise band at byte-matched budgets (OSC.35-38); L6 closed (experiment:a00-f256db1a-73ee5b disproved). L4 = Qwen2.5-0.5B, OSC.03 band fingerprints: high-band heads keep sinks + a recent window, low-band keep all KV; bar agree/KL vs full KV at a byte-matched KV budget beside a random head set of equal size, >= 3 seeds, pre-registered. CPU only, ~3.5 GB RSS, 0 USD.

## §2 Landed
- 22:2xZ town:local-maxxing a59698750e -- trajectory PERMANENT on the town node (owner 21:5xZ verbatim in THOUGHT); g7.34.1/.2 moot for this town (the Prime's to retire)
- 21:5xZ [placement] L4 step -> sanctuary-master (delivered) · 21:57Z PLACED
- 22:0xZ hypothesis:lm-l4-local-heads-keep-a-recent-window (goal:g5.22 + idea:lm-why-l3-precision-allocation-wall-is-8-12-bits); v2 fixed the budget tolerance to half a KV head (0.975 pct)

## 🔴 Where it stops
```
two subagents live (a dead session loses them): MAP = `systemctl --user status tm-neuron-period` + datasets/osc-band/2026-10-01-neuron-period/ ; no experiment node -> re-brief a builder from the hypothesis body · L4 review = re-run it from experiment:tm-l4-window-0930 (read-only)
```

## §4 Traps
- town:local-maxxing: write as `--actor thought-master` with NO --role (the row resolves to director; [town] admits director TEMPORARILY until goal:g7.16.1.11 lands, belam 22:21Z)
- box: every container runs with docker --memory; ONE model load at a time; start at MemAvailable >= 6 GB + PSI avg10 < 5 (belam 22:10Z, SM 21:57Z)
- belam's row is quiet: `send.py wake belam` = quiet-skip; ListAgents shows @30 as shell
- never pipe `send.py read` through tail (did it once at 21:52Z; the inbox file showed nothing lost)

## §5 Verification
- send.py status sanctuary-master: marker 0s after the send · belam: inbox file written, quiet row (no nudge)

## §6 BANKED
(none)

## Skills
agi-send · agi-node-write · agi-goal · agi-workflow · agi-verify · agi-rotate · agi-dispatch · agi-memory-guard · agi-master-gate

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
OWNER 22:1xZ 09-30, direct in thought-master's pane, verbatim: "Also, you have a GM from SM, but it not, might not arrive yet because you have all these tasks going on. But I basically let Sanctuary Master know that you're in charge of like the research portion fully on the board and everything, like the board and the goals. If it's like the research lane, that's kind of your territory, not Sanctuary Master's." -- this version: the formation row names the research lane (board rows, goals, round placement) as thought-master's; SM confirmed in a [rule] dm 22:11Z. BANKED option (b) becomes the recommendation: the ring gate (goal:g12) still refuses a master on town:local-maxxing.
<!-- THOUGHT:END -->
