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
**What it is (owner 01:3xZ 09-21, verbatim on goal:g14):** "a super node that exists to the side and links into all relevant nodes that relate to it. It's bigger than a single sub goal and maybe sometimes bigger than a perpetual goal but smaller than a vision. An individual set of metrics we are trying to chase for this track. In our case we are hoping that layering all these techniques lets us run bigger and bigger existing models on smaller and smaller footprints with longer and longer [context] windows." **How it changes (owner 01:4xZ-01:5xZ):** metrics may be adjusted mid-research to test things or when adjustments are needed; each change is NOT a note — it is a new node version: overwrite this body in place (the grid records the version; the reason goes in the THOUGHT block); an A/B of a metric change = a branch worktree, overwrite vs control, both measured. The board below is updated the same way (replace the section, never append). A proper `trajectory` node type is queued (G14.14.5); until it lands this doc IS the node.

## The metrics chased (one row per measured point; newest first; every number on its node)
| date | model (params) | footprint | ctx line | tok/s | quality (battery) | how | node |
|---|---|---|---|---|---|---|---|
| target | bigger | smaller | longer | usable | within 10 pct of deepseek-v4.1-flash on HumanEval + IFEval | layered: dead-head prune → context/throughput → fine-tune → QAT → telepathy | goal:g14.11 (the switch) |
| 09-20 | Bonsai 2 27B PTQ1_0 (27.36B, 1.75 bpw) | 7,268 MiB VRAM (8 GB rig) | 64K, 1 stream | 23.0 empty / 18.9 at 16.8K | HumanEval 86.6 pct (142/164); IFEval — ; reference — | ternary PTQ (shipped) | experiment:a00-bb10233d-5a7f1f |
| 09-20 | Qwen3.5-9B Q4_K_M (9B) | 6,010 MiB | 64K | 62.68 (2.87 J/tok) | HumanEval 78.0 / 79.3 pct (A / A2) | Q4 (shipped) | experiment:a00-c4441397-c8a8c6 |

## Links (every node that moves these numbers; the future `links:` field)
goal:g14 · goal:g14.6 · goal:g14.7 · goal:g14.8 · goal:g14.9 · goal:g14.10 · goal:g14.11 · goal:g14.12 · goal:g14.13 · goal:g14.14 · goal:g14.15 · doc:lm-round0-table · doc:lm-local-town-box-facts · doc:lm-research-corpus-registry · doc:recurrent-looped-transformer · idea:lm-nodes-as-kv-caches · hypothesis:lm-kv-slot-save-beats-reprefill · hypothesis:lm-bonsai2-27b-abc-coding-test-on-the-8gb-box · hypothesis:lm-own-refusal-direction-on-qwen35-9b-cuts-refusals-at-no-coding-cost · hypothesis:lm-hidden-state-mean-direction-cuts-refusals-on-qwen35-9b · hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery · hypothesis:lm-magic-pane-detector-predicts-the-form-from-the-first-prose-tokens · hypothesis:lm-dead-head-kc-threshold-is-not-a-critical-point · hypothesis:lm-morals-and-sanctuary-corpus-assembles-to-a-clean-sft-set

## Board (formation · live · queue — replaced in place, never appended)
- **Formation (01:5xZ 09-21):** thought-master (Opus max, MAIN = trunk; IDLE between merge-ups, owner order) · director-thought (Sonnet max, research rounds) · director-engine (Sonnet max, engine rounds under goal:g14.14, seated 01:33Z window @7) · pi parents + kids on OpenRouter carry the graph. One [merge-up] per batch; the master merges and gates.
- **Memory (01:20Z):** 15 GB total, 12 GB available with the 9B resident; memory_max 6G per kid (ceiling); ONE model-loading kid on the host at a time; engine kids 2-3 in parallel; GPU = one research round at a time. **06:39Z-~07:40Z 09-21: the Prime's large mur claims 3 GB + 2 cores** (every 6 h with 5 h notice).
- **Grid:** seeded 01:5xZ (3,773 versions); the cron refuses on this branch until G14.14.6 lands (first engine item) — until then versions land only when the seed command is run by hand (the master's, on order).
- **Live:** SWR.01 chunk 1 (a00-9db255d9, API-only) · MP.01 (a00-af8cefa3) · engine batch (director-engine: G14.14.6 first item → 14.14.3(c) → 14.14.1-2 → 14.14.4 workflows → 14.14.5 trajectory type → the maxxing pass).
- **Research queue (one GPU round at a time):** TEL.01 span fidelity (G14.15.1, resident 9B) → SWR.02 IFEval local arms → OSC.01 → FT.00 → DS.01 → H1'.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
thought-master 01:5xZ 09-21 — v2 of this node, and the first change made under the owner's versioning rule: the body is overwritten in place (this IS the record), the two 'mutability' notes of 01:4xZ are folded into the 'How it changes' paragraph and dropped as notes, the board says how it is updated (replace, never append) and carries the grid state. No metric row changed in this version.
<!-- THOUGHT:END -->
