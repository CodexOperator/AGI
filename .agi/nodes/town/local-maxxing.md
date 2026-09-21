---
id: town:local-maxxing
mint_id: c1cbfc52f6924643979555fee0f0386d
type: town
parents:
  - vision:the-living-being
  - ladder:ladder
  - goal:g26.towns
next_edges: []
council: council-local-maxxing
edited_by: belam
location: local-town
master: thought-master
scaffold_hash: 3876620b4bc4f88e
season: 1
thought_session: town-location-2026-09-21
town: core
visions:
  - vision:local-maxxing
  - vision:local-maxxing-smarter
  - vision:local-maxxing-together
---
<!-- BODY:BEGIN -->
# town:local-maxxing

## GOAL BUNDLE + TRAJECTORY STAND-IN

LOCATION ──▶ local-town

```
town:local-maxxing
├─ GOAL BUNDLE (diagram-max)
│  ├─ g14* ………… research tracks (g14.6–.16 + nested)
│  ├─ g5.17–.21 … remapped from legacy g14.1–.5 / g14.3 lineage
│  └─ town:local-maxxing tagged goals (same set ∩)
└─ TRAJECTORY STAND-IN ← folded from doc:lm-town-trajectory
   (pending proper `trajectory` type — G14.14.5; doc kept, deprecated pointer)
```

### Goal ids (bundle)

| id | role |
|---|---|
| goal:g14 | umbrella (retired on core/s2; lineage) |
| goal:g14.6 | TRACK I inference |
| goal:g14.7 | TRACK II fine-tune |
| goal:g14.8 | TRACK III jev + magic pane |
| goal:g14.8.3 | MAGIC PANE detector |
| goal:g14.9 | abliteration |
| goal:g14.9.1 | own refusal lever |
| goal:g14.10 | research corpus |
| goal:g14.11 | the switch / battery |
| goal:g14.11.1 | battery + reference |
| goal:g14.12 | side track spiking |
| goal:g14.13 | research treasury |
| goal:g14.14 | engine fixes |
| goal:g14.15 | KV-cache telepathy |
| goal:g14.16 | diagram-max + batch-max |
| goal:g5.17 | Sensei assigns fine-tune / local-maxxing (remap) |
| goal:g5.18 | local-maxxing TOWN (remap) |
| goal:g5.19 | Thought Master post (remap) |
| goal:g5.20 | secrets hub banked (remap) |
| goal:g5.21 | Bend2/HVM map (remap) |

Town schema parents = ladder only → **linking is Agent Notes / this body**, not `parents:` to goals.

### Trajectory stand-in (folded from `doc:lm-town-trajectory`)

**What it is (owner 01:3xZ 09-21, verbatim on goal:g14):** a super node to the side that links into all relevant nodes — bigger than a single subgoal, sometimes bigger than a perpetual, smaller than a vision. Metrics chased for this track: layer techniques so bigger models run on smaller footprints with longer context windows. **How it changes:** metric change = new node version (overwrite body; reason in THOUGHT); A/B = branch worktree. Proper `trajectory` type queued (G14.14.5); until it lands **this town section IS the stand-in**. `doc:lm-town-trajectory` remains as pointer ("stand-in moved into town body pending trajectory type") — do not delete yet.

#### Metrics chased (newest first)

| date | model (params) | footprint | ctx line | tok/s | quality (battery) | how | node |
|---|---|---|---|---|---|---|---|
| target | bigger | smaller | longer | usable | within 10 pct of deepseek-v4.1-flash on HumanEval + IFEval — reference MEASURED 09-21: 93.9 pct HumanEval (154/164) · 0.869 IFEval strict (470/541) | layered: dead-head prune → context/throughput → fine-tune → QAT → telepathy | goal:g14.11; experiment:a00-559ee702-d3c7dd |
| 09-20/21 | Bonsai 2 27B PTQ1_0 (27.36B, 1.75 bpw) | 7,268 MiB VRAM (8 GB rig) | 64K, 1 stream | 23.0 empty / 18.9 at 16.8K | HumanEval 86.6 pct = 92.2 pct of reference (FIRES 0.9x; C2 +LoRA 92.9); IFEval — (SWR.02) | ternary PTQ (shipped) | experiment:a00-bb10233d-5a7f1f · a00-559ee702-d3c7dd |
| 09-20 | Qwen3.5-9B Q4_K_M (9B) | 6,010 MiB | 64K | 62.68 (2.87 J/tok) | HumanEval 78.0 / 79.3 pct (A / A2) | Q4 (shipped) | experiment:a00-c4441397-c8a8c6 |

#### Links

goal:g14 · goal:g14.6 · goal:g14.7 · goal:g14.8 · goal:g14.9 · goal:g14.10 · goal:g14.11 · goal:g14.12 · goal:g14.13 · goal:g14.14 · goal:g14.15 · doc:lm-round0-table · doc:lm-local-town-box-facts · doc:lm-research-corpus-registry · doc:recurrent-looped-transformer · idea:lm-nodes-as-kv-caches · hypothesis:lm-kv-slot-save-beats-reprefill · hypothesis:lm-bonsai2-27b-abc-coding-test-on-the-8gb-box · hypothesis:lm-own-refusal-direction-on-qwen35-9b-cuts-refusals-at-no-coding-cost · hypothesis:lm-hidden-state-mean-direction-cuts-refusals-on-qwen35-9b · hypothesis:lm-local-candidate-within-10pct-of-deepseek-v41-flash-on-the-battery · hypothesis:lm-magic-pane-detector-predicts-the-form-from-the-first-prose-tokens · hypothesis:lm-dead-head-kc-threshold-is-not-a-critical-point · hypothesis:lm-morals-and-sanctuary-corpus-assembles-to-a-clean-sft-set · **doc:lm-town-trajectory** (pointer; folded here)

#### Board (formation · live · queue — replace in place)

```
formation  thought-master (Opus, MAIN=trunk; IDLE between merge-ups) -> director-thought (Sonnet, research) + director-engine (Sonnet, goal:g14.14 + G14.16.1-2) -> pi parents/kids
rules      diagram-max (goal:g14.16) · batch-max · board/trajectory = VERSIONS (replace body), never notes
memory     15 GB box · memory_max 6G · ONE model-loading host kid · GPU = one research round at a time
live       see doc:lm-town-trajectory board for tip ids (folded snapshot 2026-09-21)
research   MP.01 -> TEL.01 -> SWR.02 -> FT.00 -> … (tracks on g14.6–.16)
engine     G14.14.* → G14.16.* (trajectory type at 14.14.5)
comms      magic pane (G14.8 / g7.32 messaging on core) = future unified messaging layer
```

## Agent Notes

- Owner ask 2026-09-21: fold trajectory stand-in into town body; keep `doc:lm-town-trajectory` until trajectory type ships.
- Actor Belam; master cell = thought-master.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
owner ask 2026-09-21: fold doc:lm-town-trajectory into town body as GOAL BUNDLE + TRAJECTORY STAND-IN; doc kept as deprecated pointer pending trajectory type
<!-- THOUGHT:END -->
