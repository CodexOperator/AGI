---
id: doc:lm-town-trajectory
mint_id: 55dc3a3e4dba43fcb83b3be6a25433a1
type: doc
parents:
  - goal:g14
next_edges: []
edited_by: belam
scaffold_hash: 7c61cb59727a97bd
season: 2
status: deprecated
thought_session: owner-ask-2026-09-21
title: "The local-maxxing town trajectory board — the ONE shared update space for the master and both directors (owner 01:2xZ 09-21): live rounds, queue per track, last merges, the engine batch; every post appends one line per landing, the master trims the body"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# doc:lm-town-trajectory — STAND-IN MOVED

> **2026-09-21 (owner ask / Belam):** Trajectory stand-in content **folded into `town:local-maxxing` body** (section GOAL BUNDLE + TRAJECTORY STAND-IN). This doc is **not deleted** — it remains as a pointer until a proper `trajectory` node type ships (G7.33.5).
>
> **Status:** deprecated pointer — "stand-in moved into town body pending trajectory type".
>
> **Canonical read path now:** `town:local-maxxing` → GOAL BUNDLE + TRAJECTORY STAND-IN.
>
> Metrics / board / links: edit the **town body** (replace in place, thought whole-replace). Do not grow this doc further.

## Pointer

| was | now |
|---|---|
| this doc body (metrics + board + links) | `town:local-maxxing` body |
| future `trajectory` type | goal lineage G7.33.5 / engine track |

## Legacy one-liner

The local-maxxing town trajectory board — ONE shared update space for the master and both directors: live rounds, queue per track, last merges, the engine batch. Every post used to append here; that practice moves to the town body.

## Town board carried by the Prime's core sync (09-23): the town kept writing this doc after the fold above; fold these rows into `town:local-maxxing` at the next board write, then write the pointer only

## The metrics chased (one row per measured point; newest first; every number on its node)
| date | model (params) | footprint | ctx line | tok/s | quality (battery) | how | node |
|---|---|---|---|---|---|---|---|
| target | bigger | smaller | longer | usable | within 10 pct of deepseek-v4.1-flash on HumanEval + IFEval — reference MEASURED 09-21: 93.9 pct HumanEval (154/164) · 0.869 IFEval strict (470/541) | layered: dead-head prune → context/throughput → fine-tune → QAT → telepathy | goal:g14.11 (the switch); experiment:a00-559ee702-d3c7dd |
| 09-20/21 | Bonsai 2 27B PTQ1_0 (27.36B, 1.75 bpw) | 7,268 MiB VRAM (8 GB rig) | 64K single; 8K at N=4 | 20.5-23.0 tok/s aggregate, COMPUTE-BOUND: flat across 1/2/4/8 slots (SWR.02-B) | HumanEval 86.6 pct = 92.2 pct of reference (FIRES 0.9x); IFEval strict 0.7782 = 89.57 pct of reference (MISSES by 0.37 pp, inside the +/-0.4 scorer floor) -> two-eval switch NOT met by B; C2 next | ternary PTQ (shipped) | experiment:a00-bb10233d-5a7f1f · a00-559ee702-d3c7dd · a00-e699a4ec-a83259 · a00-4eec4fce-e9b330 |
| 09-20 | Qwen3.5-9B Q4_K_M (9B) | 6,010 MiB | 64K | 62.68 (2.87 J/tok) | HumanEval 78.0 / 79.3 pct (A / A2) | Q4 (shipped) | experiment:a00-c4441397-c8a8c6 |

## Links (every node that moves these numbers; the future `links:` field)
goal:g14 · goal:g14.6 · goal:g14.7 · goal:g14.8 · goal:g14.9 · goal:g14.10 · goal:g14.11 · goal:g14.12 · goal:g14.13 · goal:g14.14 · goal:g14.15 · doc:lm-round0-table · doc:lm-local-town-box-facts · doc:lm-research-corpus-registry · doc:recurrent-looped-transformer · idea:lm-nodes-as-kv-caches · hypothesis:lm-kv-slot-save-beats-reprefill · hypothesis:lm-bonsai2-27b-abc-coding-test-on-the-8gb-box · hypothesis:lm-own-refusal-direction-on-qwen35-9b-cuts-refusals-at-no-coding-cost · hypothesis:lm-hidden-state-mean-direction-cuts-refusals-on-qwen35-9b · hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery · hypothesis:lm-magic-pane-detector-predicts-the-form-from-the-first-prose-tokens · hypothesis:lm-dead-head-kc-threshold-is-not-a-critical-point · hypothesis:lm-morals-and-sanctuary-corpus-assembles-to-a-clean-sft-set · goal:g14.16 · treasury: https://github.com/yifanzhang-pro/KLPO (G14.7.2 RL arm candidate, 09-21)

## Board (formation · live · queue — replaced in place, never appended; 04:5xZ 09-21)
```
formation  thought-master (Opus, MAIN=trunk; IDLE between merge-ups) -> director-thought (Sonnet, research) + director-engine (Sonnet, goal:g14.14 + G14.16.1-2; seated 01:33Z @7) -> pi parents/kids (OpenRouter)
rules      diagram-max every emission (goal:g14.16) · batch-max: ONE order = many rounds, ONE merge-up per batch · board/trajectory changes = VERSIONS (replace body), never notes · owner verbatim on goal:g14
memory     15 GB box, 12 GB avail (9B resident) · memory_max 6G ceiling · ONE model-loading host kid · engine kids 2-3 · GPU = one research round at a time · 06:39Z-~07:40Z: the Prime's large mur = 3 GB + 2 cores
grid       LIVE: cron records every 5 min into refs/grid/local-maxxing/ (first tick 71 versions; refs 3812) -- this node's overwrites are versions now
live       research: SWR-C2.02 (IFEval on C2, GPU, single-stream) · engine: 14.14.8 capture hook
landed     SWR-B.03 b1b49f927 (B misses IFEval by 0.37 pp inside noise; verdict node for lm-pi-local-9b-kid restored) · SWR.02-B partial · TEL.03 · EF.08 + EF.09 (grid LIVE) · TEL.02 · EF.07 · MP.01 + TEL.01 · G14.14.1 · EF.01/02 · SWR.01 chunk 1 · ABL.01 · ABC.02
banked     TEL.01 forward path -- owner ANSWERED (TMM.23, 05:0xZ): (a) AUTHORIZED, conditional (between rounds only, by a TEL parent, router mode kept, exact server line recorded, restore+verify before done) -- dispatching TEL.02 this pass
research   SWR.02-B -> SWR.02-C2 (one merge-up) -> G14.10.2 capture (hook first) -> MP.02 suggester -> MP.03 formatter -> FT.00 -> DS.01 -> G14.7.2 ladder -> G14.7.3 -> H1' -> telepathy: text+tail-KV for big models; k=2 shift swarm on Bonsai-1.7B; fork can_shift probe
engine     14.14.8 capture hook (the pane's corpus) -> 14.14.6 maxxing pass + cli-grammar (jev's target) -> 14.14.1(d) -> 14.14.2 -> 14.14.4 agi-round/agi-batch (+ whole-batch MUR) -> 14.14.5 trajectory type -> 14.14.9 red suite -> 14.14.10 comms -> 14.14.11 ingest file stage -> G14.16.1-2
comms      Prime dms = REFUSED FORGED here (its local key a8e869… unregistered; fix = its keygen) -> its orders read from goal:g14 (L220 window · L236 diagram-max · L240 context docs); magic pane (G14.8) = the future unified messaging layer
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
stand-in moved into town:local-maxxing body pending trajectory type; doc kept as pointer (owner ask 2026-09-21)

— merged (Prime core-sync 09-23: core's pointer thought above; the town board's own thought below) —

thought-master 14:1xZ 09-21 -- v16: METRIC CHANGE on the Bonsai row (IFEval strict 0.7782 = 89.57 pct of reference, misses by 0.37 pp inside the scorer floor; two-eval switch not met by B) from experiment:a00-4eec4fce-e9b330; live/landed rows.
<!-- THOUGHT:END -->
