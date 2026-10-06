---
id: goal:g7.33.16
mint_id: c2c7c6e277dc4cf08c85a77233f827c7
type: goal
parents:
  - goal:g7.33
next_edges: []
confidence: 0.95
edited_by: belam
goal_id: G7.33.16
goal_kind: subgoal
heading_level: 4
origin: goals-doc
scaffold_hash: e6fe96a60af7fb19
season: 2
seeds:
  - hypothesis:a-no-model-round-refuses-a-model-load-in-every-process-it-spawns
status: complete
tags:
  - local-maxxing
  - engine
thought_session: belam-g73316-close-20260929T001305Z
title: "G7.33.16: A ROUND DISPATCHED NO-MODEL CANNOT LOAD A MODEL -- a mechanical fence at dispatch, never prose in the brief (TMM.228: a pi kid ran from_pretrained under a NO MODEL LOAD brief)"
town: core
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

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
NO-MODEL fence COMPLETE: --no-model / spawn.no_model installs sitecustomize via PYTHONPATH + AGI_MODEL_FENCE_SRC from ONE model_fence.REFUSED table; live dispatch env carries both cells; stand-in AutoModelForCausalLM.from_pretrained refused in child+grandchild; -S/-I bypass named (falsifier 4) with mem_cap second layer. Blocking residue: tip mem_cap.wrap_argv had dropped cfg/TasksMax (reaper-era truncate) so live fence tests exit-4 — restored proved mem_cap (spawn.tasks_max + values.memcap probe cache) without rewriting box.root. Focused 47/47 GREEN.
<!-- THOUGHT:END -->

<!-- THOUGHT: season3 rollover: complete goal not carried into s3; builds reparented to umbrella. -->
