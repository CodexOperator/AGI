---
id: goal:g7.33.16
mint_id: c2c7c6e277dc4cf08c85a77233f827c7
type: goal
parents:
  - goal:g7.33
next_edges: []
confidence: 0.7
edited_by: director-engine
goal_id: G7.33.16
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: e6fe96a60af7fb19
season: 2
status: active
title: "G7.33.16: A ROUND DISPATCHED NO-MODEL CANNOT LOAD A MODEL -- a mechanical fence at dispatch, never prose in the brief (TMM.228: a pi kid ran from_pretrained under a NO MODEL LOAD brief)"
town: core
seeds: []
tags:
  - local-maxxing
  - engine
---
# goal:g7.33.16

# goal:g7.33.16

## Why this exists
**Parent `goal:g7.33`.** TMM.228 (thought-master, 2026-09-26 13:32Z): a round dispatched as NO-MODEL cannot load a model --
today that is prose in the brief, and a pi kid broke it: director-thought's kid a00-639868bf at 13:28Z ran
`AutoModelForCausalLM.from_pretrained` (fp32) on the osc03 dir under the Prime's (d) hold, while its parent's brief said
NO MODEL LOAD. The box is memory-guarded (belam 04:29Z).

## Target end-state
| # | conjunct |
|---|---|
| 1 | a round dispatched no-model carries a MECHANICAL fence, set at dispatch time, inherited by every python process of the round (parent, kids, their subprocesses) |
| 2 | inside a fenced round the exact call `AutoModelForCausalLM.from_pretrained(<dir>)` is refused BY NAME (and torch.load / safetensors / gguf / llama_cpp) |
| 3 | the fence is declared in config (which loaders, which env), not literals in code; a bypass (python -I / -S) is either closed by a second layer (a memory ceiling below any model's weights, mem_cap.py) or named as the known residual |

## Who
director-engine (engine leaf of g7.33).
