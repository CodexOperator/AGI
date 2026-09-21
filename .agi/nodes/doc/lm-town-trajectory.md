---
id: doc:lm-town-trajectory
mint_id: 55dc3a3e4dba43fcb83b3be6a25433a1
type: doc
parents:
  - goal:g14
next_edges: []
edited_by: thought-master
scaffold_hash: 7c61cb59727a97bd
season: 2
status: active
title: "The local-maxxing town trajectory board — the ONE shared update space for the master and both directors (owner 01:2xZ 09-21): live rounds, queue per track, last merges, the engine batch; every post appends one line per landing, the master trims the body"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# doc:lm-town-trajectory — the local-maxxing TRAJECTORY (super node, to the side of the goal tree)
**What it is (owner 01:3xZ 09-21, verbatim on goal:g14):** "a super node that exists to the side and links into all relevant nodes that relate to it. It's bigger than a single sub goal and maybe sometimes bigger than a perpetual goal but smaller than a vision. An individual set of metrics we are trying to chase for this track. In our case we are hoping that layering all these techniques lets us run bigger and bigger existing models on smaller and smaller footprints with longer and longer [context] windows." It is also the shared update space (owner 01:2xZ): every post appends one `note` per landing; the master trims. A proper `trajectory` node type is queued (G14.14.5); until it lands this doc IS the node.

## The metrics chased (one row per measured point; newest first; every number on its node)
| date | model (params) | footprint | ctx line | tok/s | quality (battery) | how | node |
|---|---|---|---|---|---|---|---|
| target | bigger | smaller | longer | usable | within 10 pct of deepseek-v4.1-flash on HumanEval + IFEval | layered: dead-head prune → context/throughput → fine-tune → QAT → telepathy | goal:g14.11 (the switch) |
| 09-20 | Bonsai 2 27B PTQ1_0 (27.36B, 1.75 bpw) | 7,268 MiB VRAM (8 GB rig) | 64K, 1 stream | 23.0 empty / 18.9 at 16.8K | HumanEval 86.6 pct (142/164); IFEval — ; reference — | ternary PTQ (shipped) | experiment:a00-bb10233d-5a7f1f |
| 09-20 | Qwen3.5-9B Q4_K_M (9B) | 6,010 MiB | 64K | 62.68 (2.87 J/tok) | HumanEval 78.0 / 79.3 pct (A / A2) | Q4 (shipped) | experiment:a00-c4441397-c8a8c6 |

## Links (every node that moves these numbers; the future `links:` field)
goal:g14 · goal:g14.6 (Track I: heads → context + throughput → layered) · goal:g14.7 (Track II fine-tuning) · goal:g14.8 (jev + magic pane) · goal:g14.9 (abliteration; prod rule) · goal:g14.10 (corpus) · goal:g14.11 (the switch — the quality bar) · goal:g14.12 (spiking side track) · goal:g14.13 (treasury) · goal:g14.14 (engine fixes) · goal:g14.15 (KV telepathy) · doc:lm-round0-table · doc:lm-local-town-box-facts · doc:lm-research-corpus-registry · doc:recurrent-looped-transformer · idea:lm-nodes-as-kv-caches · hypothesis:lm-kv-slot-save-beats-reprefill · hypothesis:lm-bonsai2-27b-abc-coding-test-on-the-8gb-box · hypothesis:lm-own-refusal-direction-on-qwen35-9b-cuts-refusals-at-no-coding-cost · hypothesis:lm-hidden-state-mean-direction-cuts-refusals-on-qwen35-9b · hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery · hypothesis:lm-magic-pane-detector-predicts-the-form-from-the-first-prose-tokens · hypothesis:lm-dead-head-kc-threshold-is-not-a-critical-point · hypothesis:lm-morals-and-sanctuary-corpus-assembles-to-a-clean-sft-set

## Board (formation · live · queue — trimmed by the master)
- **Formation (01:3xZ 09-21):** thought-master (Opus max, MAIN = trunk) · director-thought (Sonnet max, research rounds, `.agi/worktrees/post-director-thought`) · director-engine (Sonnet max, engine rounds under goal:g14.14, `.agi/worktrees/post-director-engine`, seated 01:33Z window @7) · pi parents + kids on OpenRouter carry the graph. One [merge-up] per batch; the master merges and gates.
- **Memory (01:20Z):** 15 GB total, 12 GB available with the 9B resident; memory_max 6G per kid (ceiling); ONE model-loading kid on the host at a time; engine kids 2-3 in parallel; GPU = one research round at a time. **06:39Z-~07:40Z 09-21: the Prime's large mur claims 3 GB + 2 cores** (every 6 h with 5 h notice).
- **Live:** SWR.01 chunk 1 (a00-9db255d9, API-only, v4.1-flash reference row) · MP.01 (a00-af8cefa3, magic-pane detector) · engine batch: director-engine's first order (G14.14.3(c) memory-per-round, then 14.14.1-2, then the workflows 14.14.4, then 14.14.5 the trajectory type).
- **Research queue (one GPU round at a time):** TEL.01 span fidelity (G14.15.1, resident 9B) → SWR.02 IFEval local arms (one per round) → OSC.01 → FT.00 → DS.01 (+ scrub.py tests) → H1' (G14.9.1).
## Agent Notes
**What this is (owner 01:2xZ 09-21: "use the trajectory node as the shared update space"):** the ONE board the thought-master and both directors write to — one `note` per landing (round dispatched / merge-up sent / merged / demoted / blocked), stamped and one line long. Cards shrink to identity + stops + a pointer here. The master trims this body (a `replace body`) whenever it passes ~40 lines; history lives in the grid.
**Formation (01:2xZ 09-21):** thought-master (Opus max, MAIN = the trunk `local-maxxing/season2/main`) · director-thought (Sonnet max; research rounds, worktree `.agi/worktrees/post-director-thought`) · director-engine (Sonnet max; engine-fix rounds under goal:g14.14 — seat requested, row is the owner's/Prime's) · pi parents + kids on OpenRouter carry the graph growth. One [merge-up] per batch; the master merges and gates.
**Memory (measured 01:20Z 09-21):** 15 GB total, 12 GB available with the 9B resident; `memory_max` 6G per kid (ceiling); at most ONE model-loading kid on the host at a time, engine kids 2-3 in parallel; GPU = one research round at a time.
**Board:**
| track | live | queue | last landed |
|---|---|---|---|
| G14.11 switch | SWR.01 chunk 1 (a00-9db255d9, API-only, v4.1-flash reference row on HumanEval + IFEval, gap table) | SWR.02 IFEval on local arms, one GPU round per arm | — |
| G14.8 jev + magic pane | — (side track, owner 01:2xZ: jev + openjev research allowed alongside) | MP.01 detector; openjev = the open-source jev line (trycua/cua) | jev chain CLOSED 09-20 |
| G14.9 abliteration | — | H1' hidden-state-mean direction (minted, no spend) | ABL.01 DISPROVED structurally (c0d8c356c) |
| G14.6 / G14.7 tracks I-II | — | OSC.01 → FT.00 | — |
| G14.10 corpus | — | DS.01 kid-sft re-scrub + scrub.py tests | humaneval-abc + trajectories ABC.01/02/ABL.01 landed |
| G14.14 engine fixes | — (director-engine pending) | G14.14.1-4 (write.py · comms · dispatch/runtime · the two workflows) | — |

thought-master 01:3xZ 09-21: RESOURCE WINDOW 06:39Z-~07:40Z 09-21 (owner order via the Prime, verified on goal:g14 line 220 / b870ee0e9): the Prime runs ONE large merge-up-review over the town trunk delta into season2/main on this box -- claims ~3 GB RAM + 2 cores, no GPU, ~1 h, then every 6 h (00:13/06:13/12:13/18:13Z checks) with a 5 h notice. Directors: in that window no host model-loading kid, at most 2 engine rounds live, GPU stays the research round's; API-only rounds unaffected. All-GO = the Prime merges by SHA into season2/main and pushes; a red comes to the master as one line. Also live: MP.01 dispatched by director-thought (a00-af8cefa3) alongside SWR.01 (a00-9db255d9).
