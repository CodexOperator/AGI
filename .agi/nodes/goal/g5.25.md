---
id: goal:g5.25
mint_id: 62a962e604604457b4b0f81ed5791c1b
type: goal
parents:
  - goal:g5
next_edges: []
confidence: 0.8
edited_by: belam
goal_id: G5.25
goal_kind: subgoal
heading_level: 3
origin: goals-doc
scaffold_hash: 81bfe6086b707b83
season: 2
seeds:
  - idea:lm-abliteration-feature-differences-generalize-across-models
status: active
tags:
  - local-maxxing
  - abliteration
title: "G5.25: ABLITERATION — prod candidates must be abliterated (by us if by no one else; identical → abliterated wins); the town own lever (derive, apply at runtime, verify in-graph, price it) and the cross-model question: do the feature differences generalize? (owner 16:2xZ 09-20)"
town: local-maxxing
---
<!-- BODY:BEGIN -->
# goal:g5.25

## Agent Notes
**Owner source (2026-09-20 16:2xZ, verbatim on goal:g14):** "if it's identical, my preference is always use the abliterated models over non-abliterated ones. So if any model is good enough to be used in prod at some point it would have to be abliterated. If not by anyone else then by us. We could extract the feature differences between abliterated and non-abliterated models and see if there are any generalized patterns across models."

**Commits to.** (1) The standing rule: a prod candidate must be abliterated — by the town if by no one else; between identical candidates the abliterated one wins; every charter-table row carries `abliterated?`. (2) The capability: derive a direction from any model the town serves, apply it at runtime (control vector or rank-1 LoRA projection), verify it is in the compute graph (scale 0 byte-identical, large scale visibly broken), and price it on the G5.27 battery. (3) The research question: are the feature differences between abliterated and non-abliterated models the same object across models — compared only through basis-independent signatures (unembedding token sets vs a random-direction null, depth profile, behaviour profile), never raw cosine across hidden sizes.

**Invariants.** Every direction has an adapter-in-graph check and a random-direction control; capability cost is measured on the same battery as everything else; the shipped OrcaBonsai lever (Bonsai 2 27B) is the reference implementation the town's own lever must match before being trusted; nothing is baked into weights (a ternary re-quantisation rounds the edit away — measured by the source).

**Falsifiers.** (a) The own-lever chunk is falsified if the extracted direction moves refusal < 10 points at every scale or costs ≥ 2 battery points at the first scale that works — then the rank-1 projection route replaces the control-vector route, and if that also fails the town relies on shipped abliterations only. (b) The cross-model claim is falsified if the unembedding-signature overlap across the Qwen family is not above the random null (Jaccard of top-200 ≤ null + 2σ) — then "abliteration" is per-model and the goal narrows to the capability alone.

**Done when.** The town has abliterated at least one candidate itself, matched the shipped lever's behaviour on Bonsai, and either found a shared signature (a `doc:` with the pattern) or recorded that there is none.

**First chunk (minted):** `idea:lm-abliteration-feature-differences-generalize-across-models` → `hypothesis:lm-own-refusal-direction-on-qwen35-9b-cuts-refusals-at-no-coding-cost` (ABL.01). Sub-sub-goals are the director's to mint (G5.25.1 own lever, G5.25.2 cross-model signatures), same format, before any further chunk runs.

thought-master 23:0xZ 09-20 (knowledge from ABC.01 + ABC.02, both merged): the OrcaBonsai runtime abliteration LoRA on Bonsai 2 27B PTQ1_0 is measured NULL on coding twice -- scale 1: 141/164 vs B 142/164 (p = 1.0, 141 completions byte-identical); scale 2: 143/164 (p = 1.0 vs B, 105/164 byte-identical, so the direction IS active at scale 2 and still changes no aggregate capability). Consequence for ABL.01 (hypothesis:lm-own-refusal-direction-on-qwen35-9b-cuts-refusals-at-no-coding-cost): a refusal direction must be measured on what it is FOR -- the round's primary metric is a refusal-rate battery, HumanEval is the no-cost CONTROL, and 'no change on coding' is the expected null, never a finding. The owner's prod rule (16:2xZ: abliterated if identical) is unaffected: identical is what was measured.

thought-master 00:2xZ 09-21 (knowledge from ABL.01, merged c0d8c356c): the llama.cpp control-vector route is CLOSED for the Qwen3.5 hybrid family on this box -- llama-cvector-generator asserts at cvector-generator.cpp:221 because the Gated Delta Net stack does not emit n_layers - 1 l_out tensors; structural, reproduced twice, unfixed upstream at f072b1037. Consequences: (1) the town's own abliteration lever for Qwen3.5-9B must come from weight-space extraction (H1': the rank-1 projection export on dequantised writer matrices, per the node's own clause) or a direction computed outside llama.cpp (hidden-state means from a Python forward pass); (2) H2's cross-model signature comparison (Bonsai/OrcaBonsai 5120-d direction vs an own direction) needs the own direction from (1) first; (3) 'abliterated if identical' (owner 16:2xZ) is untouched -- nothing here changes which candidate wins, only how the town would abliterate a hybrid-arch candidate itself. First reusable battery for any later lever: datasets/abl-01/ (64 + 64 pairs, 50 held-out, classifier).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
owner ask 2026-09-21: renumber local-maxxing research g5.25 → g5.25 (g5 continuation after g5.21; mint_id preserved; town:local-maxxing kept); no director assignment
<!-- THOUGHT:END -->
