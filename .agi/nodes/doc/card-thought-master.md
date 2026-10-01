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

## §0 State (10:1xZ 10-01, read from date -u)
| | |
|---|---|
| lane | research: its board rows (town:local-maxxing), its goals g5.22-g5.31, placing its rounds -- MINE, no SM word (owner 22:1xZ 09-30) · subagents: Opus 5.5, <= 3 at a time |
| run | FREE LANE (0 USD); council mode = dispatch.py unused -> each round: mint the hypothesis (pre-registered rule) -> an Opus BUILDER subagent (detached unit, MemoryMax, evidence_runs set) -> an Opus adversarial REVIEWER -> THOUGHT + board row |
| formation | council loop building config:engine (goal:g7.16.1.11) · board bundles = goal:g7.16.1.11.1-.10 (re-swept c9880a5e1, owner 07:2xZ) · SM only for a gate or a slot collision · belam reachable by SendMessage (its inbox row is quiet) |
| HELD | key / identity / signing / rotate / spawn-row / write-gate work waits on goal:g7.16.1.11 -- not yours |

## §1 Plan
```
LIVE   (10:1xZ) REVIEWER of L4 run 4 (read-only, experiment:tm-l4-direct-1001)
       BUILDER of the periodicity POSITIVE CONTROL (hypothesis:lm-neuron-periodicity-pipeline-finds-the-known-mod-p-circuit; unit tm-neuron-pc -> experiment tm-neuron-period-pc-1001)
       SURVEY (read-only, no repo writes): llama.cpp per-layer / per-KV-head windows + the served 9B's attention shape -> sizes the next L4 round
NEXT   L4 r4 review -> THOUGHT + board row · survey -> mint L4 run 5 (the 9B: quality-only path first, or the memory-saving llama.cpp path)
       positive control -> proved: stage 2 SELF-POKE can start on THIS toy model as a sandbox (opt-in, sham + blind, debrief) · disproved: the pipeline is blind, fix it before any LLM claim
HELD   SELF-POKE on an LLM until a period family moves behaviour there · an LLM with multi-digit number tokens = a download (BANKED)
```
| round | verdict | review | one line |
|---|---|---|---|
| L4 r1 tm-l4-window-0930 | disproved | ACCEPT_WITH_RESIDUE | band = a weak locality proxy (1/3 budgets) |
| L4 r2 tm-l4-distance-1001 | PROVED 3/3 | ACCEPT_WITH_RESIDUE | measured distance beats random; sink-heavy far readers leak in at k 26 |
| L4 r3 tm-l4-mass-1001 | disproved | ACCEPT_WITH_RESIDUE | mass ~ distance; the per-head DIRECT cost is best everywhere |
| L4 r4 tm-l4-direct-1001 | PROVED 3/3 | pending | frozen DIRECT on 8 fresh docs: KL 0.0085 / 0.0255 / 0.0545 vs random min 0.076 / 0.114 / 0.197 at kept 0.75 / 0.60 / 0.50; wins on every doc; joint cost 1.06-1.17x solo |
| MAP r1 tm-neuron-period-1001 | disproved | ACCEPT_WITH_RESIDUE | C1 passed on ramps only; the per-turn overlap = a layer confound |
| MAP r2 tm-neuron-period2-1001 | disproved | ACCEPT_WITH_RESIDUE | oscillators 0.27-0.47 pct; the periods = the single-digit tokenizer |
| jev | retired | -- | absorbed by config:engine (brief.py walk); local TF-IDF beat it 0.648 vs 0.588 |

## §2 Landed
- 09-30 22:2xZ town:local-maxxing a59698750e -- the trajectory's PERMANENT home (owner 21:5xZ verbatim)
- 10-01: idea:lm-neuron-periodicity-map-and-self-poke (owner 22:0xZ + debrief 22:1xZ verbatim) · 8 hypotheses · 6 experiments · 6 reviews · board re-swept c9880a5e1 · jev reading 5907250622

## 🔴 Where it stops
```
three subagents live (a dead session loses them): positive control = `systemctl --user status tm-neuron-pc` + datasets/osc-band/2026-10-01-neuron-period-pc/ ; no experiment node -> re-brief a builder from the hypothesis body · L4 r4 review = re-run read-only from experiment:tm-l4-direct-1001 · the llama.cpp survey = re-run from L4 r4's LARGEST SAFE STEP
```

## §4 Traps
- an experiment node needs evidence_runs (self id) or the grid commit auto-demotes a decisive verdict -- every builder brief says so
- builders bent box rules once (run 3: unit MemoryMin + a shared-slice cache reclaim) -- briefs now forbid slice-wide / box-wide / cache-drop actions
- town:local-maxxing: `--actor thought-master` with NO --role ([town] admits director TEMPORARILY until goal:g7.16.1.11)
- write.py `sub` refuses an empty replacement and can merge lines when a replacement drops a newline -- rewrite the card whole (`replace body 3:<line before THOUGHT>`)
- box: ONE model load at a time; start at MemAvailable >= 6 GB + PSI avg10 < 5; stop at >= 20; containers with --memory
- my posts row is right on the town trunk (@34); season2/main's stale @1 is belam's to carry
- never pipe `send.py read` through tail

## §5 Verification
- every round: the verdict recomputed from results.json by an independent Opus reviewer; links 0 broken (07:4xZ); pushed after every write

## §6 BANKED
- an LLM re-test of the periodicity idea needs a model whose tokenizer holds multi-digit numbers as one token: none resident (all Qwen-family) -> one free download (/data ~89 GB free) -- options: (a) ask the owner after the positive control passes (RECOMMENDED) · (b) stay on Qwen with ones-digit-matched controls

## Skills
agi-send · agi-node-write · agi-goal · agi-workflow · agi-verify · agi-rotate · agi-dispatch · agi-memory-guard · agi-master-gate

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
OWNER 22:1xZ 09-30, direct in thought-master's pane, verbatim: "Also, you have a GM from SM, but it not, might not arrive yet because you have all these tasks going on. But I basically let Sanctuary Master know that you're in charge of like the research portion fully on the board and everything, like the board and the goals. If it's like the research lane, that's kind of your territory, not Sanctuary Master's." -- this version: the formation row names the research lane (board rows, goals, round placement) as thought-master's; SM confirmed in a [rule] dm 22:11Z. BANKED option (b) becomes the recommendation: the ring gate (goal:g12) still refuses a master on town:local-maxxing.
<!-- THOUGHT:END -->
