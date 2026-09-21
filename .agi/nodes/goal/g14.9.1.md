---
id: goal:g14.9.1
mint_id: c003bcd302234c13a57d3928d9791388
type: goal
parents:
  - goal:g14.9
next_edges: []
confidence: 0.8
edited_by: director-thought
goal_id: G14.9.1
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: 7f9f4157c307eb6f
season: 2
seeds:
  - hypothesis:lm-own-refusal-direction-on-qwen35-9b-cuts-refusals-at-no-coding-cost
  - hypothesis:lm-hidden-state-mean-direction-cuts-refusals-on-qwen35-9b
status: active
tags:
  - local-maxxing
  - abliteration
  - own-lever
title: "G14.9.1: OWN LEVER -- extract a refusal direction from Qwen3.5-9B ourselves, apply it at runtime, verify in-graph, price it on the HumanEval control (owner 16:2xZ 09-20)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# goal:g14.9.1

## Agent Notes
**Owner source (2026-09-20 16:2xZ, verbatim on goal:g14, relayed via goal:g14.9):** "if it's identical, my preference is always use the abliterated models over non-abliterated ones. So if any model is good enough to be used in prod at some point it would have to be abliterated. If not by anyone else then by us. We could extract the feature differences between abliterated and non-abliterated models and see if there are any generalized patterns across models."

**Commits to.** The first half of G14.9's capability commitment: derive a direction from a model the town actually serves (Qwen3.5-9B-Q4_K_M, the resident 9B) using the town's own tooling (llama-cvector-generator, mean-difference method over a paired refusal-eliciting/benign prompt set of at least 64 items), apply it at inference as a scaled control vector across s in {0.5, 1.0, 1.5, 2.0}, verify it is genuinely in the compute graph (s=0 byte-identical to the ABC.01 arm-A baseline; a random-direction control at the best s moves refusal far less than the real one), and price it on the same battery every other lever in this town is priced on (HumanEval pass@1, the ABC.01/ABC.02 harness, same 164 problems, same template). Cross-model signature comparison (G14.9.2, the unembedding-overlap question) waits until this lever is actually measured — it is the H2 the ABL.01 node names on a proved branch, not started here.

**Invariants.** Every scale tested carries both controls (random direction; s=0 byte-identity against the ABC.01 arm-A completions); the refusal classifier and its phrase list are committed as text, not ad hoc; refusal rate and coding cost are measured on the same held-out set and the same HumanEval harness every other lever in this town uses; the resident router server answers a real completion on :8080 before done (never merely /v1/models); no model download, no kernel build, no engine code; one paid parent (pi/deepseek, cap 1 USD), one paid round at a time, nothing stacked on the GPU.

**Falsifiers.** (a) Extraction fails to produce a vector at all — the WHY names the binary/path used (fork dir / full-cuda image / resident image) and the cvector route is dead on this box; next cheapest step is the rank-1 projection export (H1', OrcaBonsai's exporter on dequantised writer matrices). (b) The refusal rate moves less than 10 points at every scale tested — same fallback to H1'. (c) The first scale that moves refusal by more than 50 points also costs 2.0 or more HumanEval pass@1 points versus s=0 (McNemar on the discordant pairs) — the lever is too expensive at the strength needed to work; next cheapest step is again the rank-1 projection route, never a bigger model.

**Done when.** ABL.01 lands a verdict against its own pre-registered falsifiers — refusal delta and HumanEval cost at every scale tested, both controls (random direction, s=0 byte-identity) reported with real numbers. Proved or disproved are both a real answer here: a disproof feeds the WHY and the rank-1 projection alternative directly, it is not a dead end for this subgoal.

**First chunk (minted):** `hypothesis:lm-own-refusal-direction-on-qwen35-9b-cuts-refusals-at-no-coding-cost` (ABL.01), re-parented here from `idea:lm-abliteration-feature-differences-generalize-across-models` directly (the idea itself re-parented from goal:g14.9 to this sub-sub-goal). G14.9.2 (cross-model unembedding-signature comparison) is minted only when that chunk is actually reached, per the owner pace rule.
