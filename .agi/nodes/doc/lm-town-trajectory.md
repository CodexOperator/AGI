---
id: doc:lm-town-trajectory
mint_id: 55dc3a3e4dba43fcb83b3be6a25433a1
type: doc
parents:
  - goal:g14
next_edges: []
edited_by: director-engine
scaffold_hash: 7c61cb59727a97bd
season: 2
status: active
title: "The local-maxxing town trajectory board — the ONE shared update space for the master and both directors (owner 01:2xZ 09-21): live rounds, queue per track, last merges, the engine batch; every post appends one line per landing, the master trims the body"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# doc:lm-town-trajectory — the local-maxxing TRAJECTORY (super node, to the side of the goal tree)
**What it is (owner 01:3xZ 09-21, verbatim on goal:g14):** "a super node that exists to the side and links into all relevant nodes that relate to it. It's bigger than a single sub goal and maybe sometimes bigger than a perpetual goal but smaller than a vision. An individual set of metrics we are trying to chase for this track. In our case we are hoping that layering all these techniques lets us run bigger and bigger existing models on smaller and smaller footprints with longer and longer [context] windows." **How it changes (owner 01:4xZ-01:5xZ):** metrics may be adjusted mid-research to test things or when adjustments are needed; each change is NOT a note — it is a new node version: overwrite this body in place (the grid records the version; the reason goes in the THOUGHT block); an A/B of a metric change = a branch worktree, overwrite vs control, both measured. The board below is updated the same way (replace the section, never append). A proper `trajectory` node type is queued (G14.14.5); until it lands this doc IS the node.

## The metrics chased (one row per measured point; newest first; every number on its node)
| date | model (params) | footprint | ctx line | tok/s | quality (battery) | how | node |
|---|---|---|---|---|---|---|---|
| target | bigger | smaller | longer | usable | within 10 pct of deepseek-v4.1-flash on HumanEval + IFEval — reference MEASURED 09-21: 93.9 pct HumanEval (154/164) · 0.869 IFEval strict (470/541) | layered: dead-head prune → context/throughput → fine-tune → QAT → telepathy | goal:g14.11 (the switch); experiment:a00-559ee702-d3c7dd |
| 09-20/21 | Bonsai 2 27B PTQ1_0 (27.36B, 1.75 bpw) | 7,268 MiB VRAM (8 GB rig) | 64K, 1 stream | 23.0 empty / 18.9 at 16.8K | HumanEval 86.6 pct = 92.2 pct of reference (FIRES 0.9x; C2 +LoRA 92.9); IFEval — (SWR.02) | ternary PTQ (shipped) | experiment:a00-bb10233d-5a7f1f · a00-559ee702-d3c7dd |
| 09-20 | Qwen3.5-9B Q4_K_M (9B) | 6,010 MiB | 64K | 62.68 (2.87 J/tok) | HumanEval 78.0 / 79.3 pct (A / A2) | Q4 (shipped) | experiment:a00-c4441397-c8a8c6 |

## Links (every node that moves these numbers; the future `links:` field)
goal:g14 · goal:g14.6 · goal:g14.7 · goal:g14.8 · goal:g14.9 · goal:g14.10 · goal:g14.11 · goal:g14.12 · goal:g14.13 · goal:g14.14 · goal:g14.15 · doc:lm-round0-table · doc:lm-local-town-box-facts · doc:lm-research-corpus-registry · doc:recurrent-looped-transformer · idea:lm-nodes-as-kv-caches · hypothesis:lm-kv-slot-save-beats-reprefill · hypothesis:lm-bonsai2-27b-abc-coding-test-on-the-8gb-box · hypothesis:lm-own-refusal-direction-on-qwen35-9b-cuts-refusals-at-no-coding-cost · hypothesis:lm-hidden-state-mean-direction-cuts-refusals-on-qwen35-9b · hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery · hypothesis:lm-magic-pane-detector-predicts-the-form-from-the-first-prose-tokens · hypothesis:lm-dead-head-kc-threshold-is-not-a-critical-point · hypothesis:lm-morals-and-sanctuary-corpus-assembles-to-a-clean-sft-set · goal:g14.16 · treasury: https://github.com/yifanzhang-pro/KLPO (G14.7.2 RL arm candidate, 09-21)

## Board (formation · live · queue — replaced in place, never appended; 04:3xZ 09-21)
```
formation  thought-master (Opus, MAIN=trunk; IDLE between merge-ups) -> director-thought (Sonnet, research) + director-engine (Sonnet, goal:g14.14 + G14.16.1-2; seated 01:33Z @7) -> pi parents/kids (OpenRouter)
rules      diagram-max every emission (goal:g14.16) · batch-max: ONE order = many rounds, ONE merge-up per batch · board/trajectory changes = VERSIONS (replace body), never notes · owner verbatim on goal:g14
memory     15 GB box, 12 GB avail (9B resident) · memory_max 6G ceiling · ONE model-loading host kid · engine kids 2-3 · GPU = one research round at a time · 06:39Z-~07:40Z: the Prime's large mur = 3 GB + 2 cores
grid       seeded 01:5xZ by hand ONCE (3,773 v) · grid.storage_trunk EXISTS (EF.02) but this box NOT migrated (33 literals outside scope -> EF.02b) · cron still refuses on this branch
live       MP.01 a00-af8cefa3 (research) · pd-klpo digest (pi) · engine: none live -- G14.14.1 fully landed (a,b,c proved), EF.02b next
landed     G14.14.1 COMPLETE (EF.03 disproved honestly -> EF.04 fix-forward proved the anchor guard 2d570e2db; EF.05 create --body-file + EF.06 -h docs proved, director-engine re-ran 245 tests) · EF.01 dispatch --memory + EF.02 grid trunk (68fedbace · a657f0d59) · SWR.01 chunk 1 346c377c2 · ABL.01 c0d8c356c · ABC.02 3393a7778
research   MP.01 -> TEL.01 (g14.15.1, resident 9B) -> SWR.02 (IFEval on B then C2; slots at shorter ctx; b/c label fix) -> FT.00 -> DS.01 -> G14.10.2 session trunk + jev pass -> G14.7.2 ladder (one base per order) -> G14.7.3 diagram-maxed traces -> MP.02 wrapper -> H1' -> layer G14.7.2 + G14.15
engine     EF.02b (remaining refs/grid literals + this box's migration) -> 14.14.1(d) BODY:BEGIN marker for --body-file nodes (node_writer) -> 14.14.2 -> 14.14.4 agi-round/agi-batch (+ whole-batch MUR) -> 14.14.5 trajectory type -> 14.14.6 maxxing pass -> 14.14.8 capture hook -> 14.14.9 red suite -> 14.14.10 comms -> 14.14.11 ingest file stage -> G14.16.1-2
comms      Prime dms = REFUSED FORGED here (its local key a8e869… unregistered; fix = its keygen) -> its orders read from goal:g14 (L220 window · L236 diagram-max · L240 context docs); magic pane (G14.8) = the future unified messaging layer
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
thought-master 04:4xZ 09-21 -- v8 = MERGE RESOLUTION: director-engine versioned the board on its post branch (G14.14.1 complete) while v6/v7 were written on the trunk; kept v7 (Links incl. KLPO) and folded its live/landed/engine rows in; added 14.14.1(d) (the --body-file marker caveat) to the engine row. Lesson: one writer per board VERSION -- directors send their rows in the merge-up, the master versions the board (else every batch conflicts here).
<!-- THOUGHT:END -->
