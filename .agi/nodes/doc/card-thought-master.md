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

## §0 State (22:1xZ 09-30, read from date -u)
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
LIVE   ONE Opus builder subagent (22:0xZ): script + test + detached unit tm-l4-window (systemd --user, MemoryMax 5G) + experiment tm-l4-window-0930
QUEUED idea:lm-neuron-periodicity-map-and-self-poke (owner idea 22:0xZ, debrief 22:1xZ) stage 1 MAP -> mint its hypothesis when L4 frees the model slot
NEXT   its report -> an adversarial Opus review of the bytes (claim vs results.json) -> verdict line on the trajectory rows (ring-gated: via the Prime)
BLOCK  the owner's trajectory edit on town:local-maxxing -> ring gate (§6)
```
STEP (ladder L4, goal:g5.22): L3 folds into L4 (idea:lm-why-l3-precision-allocation-wall-is-8-12-bits) -- band-energy key bits sit inside uniform's noise band at byte-matched budgets (OSC.35-38); L6 closed (experiment:a00-f256db1a-73ee5b disproved). L4 = Qwen2.5-0.5B, OSC.03 band fingerprints: high-band heads keep sinks + a recent window, low-band keep all KV; bar agree/KL vs full KV at a byte-matched KV budget beside a random head set of equal size, >= 3 seeds, pre-registered. CPU only, ~3.5 GB RSS, 0 USD.

## §2 Landed
- 21:5xZ [owner] line + a ready town-node edit -> belam's inbox (.agi/sessions/inbox/belam.md; script .agi/sessions/thought-master-owner-trajectory-edit.py, dry-run clean)
- 21:5xZ [placement] L4 step -> sanctuary-master (delivered) · 21:57Z PLACED
- 22:0xZ hypothesis:lm-l4-local-heads-keep-a-recent-window (goal:g5.22 + idea:lm-why-l3-precision-allocation-wall-is-8-12-bits); v2 fixed the budget tolerance to half a KV head (0.975 pct)

## 🔴 Where it stops
```
the builder subagent is live (a session that died loses it): check `systemctl --user status tm-l4-window` + datasets/osc-band/2026-09-30-l4/ ; no experiment node yet -> re-brief a builder from the hypothesis body
```

## §4 Traps
- town:* nodes are ring-gated (goal:g12): only owner / prime_director may edit, even the trajectory rows a master "writes whole" -- hand the edit to the Prime
- box: every container runs with docker --memory; ONE model load at a time; start at MemAvailable >= 6 GB + PSI avg10 < 5 (belam 22:10Z, SM 21:57Z)
- belam's row is quiet: `send.py wake belam` = quiet-skip; ListAgents shows @30 as shell
- never pipe `send.py read` through tail (did it once at 21:52Z; the inbox file showed nothing lost)

## §5 Verification
- send.py status sanctuary-master: marker 0s after the send · belam: inbox file written, quiet row (no nudge)

## §6 BANKED
- OWNER 21:5xZ 09-30, verbatim: "Honestly let’s just leave the trajectory as the permanent home under the town board node. This is owner speaking direct btw." -- the edit (TEMPORARY -> PERMANENT, owner line in THOUGHT) is refused for a master by the ring gate. Options: (a) belam runs the ready script (asked 21:5xZ; not landed at 22:1xZ) · (b) RECOMMENDED since 22:1xZ (owner: the research board is thought-master's): the owner admits the town master to its own town node's ring, so the board is written by its owner-named writer. goal:g7.34.1 / .2 on town:core = moot for local-maxxing (the Prime's to retire).

## Skills
agi-send · agi-node-write · agi-goal · agi-workflow · agi-verify · agi-rotate · agi-dispatch · agi-memory-guard · agi-master-gate
