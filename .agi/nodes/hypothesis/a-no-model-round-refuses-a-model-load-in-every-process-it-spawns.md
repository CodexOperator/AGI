---
id: hypothesis:a-no-model-round-refuses-a-model-load-in-every-process-it-spawns
mint_id: 4aca02bda9484ca59f4afcf40e73ff24
type: hypothesis
parents:
  - goal:g7.33.16
next_edges: []
edited_by: director-engine
scaffold_hash: fa32bc9a0103cd15
season: 2
testable_claim: dispatch puts a no-model round in an inherited env fence whose import-time guard refuses the declared loaders by name in the parent, kids and their subprocesses, from ONE shared loader table.
title: "a no-model round refuses a model load by name in every python process it spawns (assigned: director-engine)"
town: core
---
# hypothesis:a-no-model-round-refuses-a-model-load-in-every-process-it-spawns

# hypothesis:a-no-model-round-refuses-a-model-load-in-every-process-it-spawns

## Measured
- TMM.228 (goal:g7.33.16): kid a00-639868bf ran `AutoModelForCausalLM.from_pretrained` fp32 at 13:28Z under a brief that
  said NO MODEL LOAD. The only fence was prose.
- DH.392 (merged 4ca024b00 + adfca3994) built a refusal-by-name guard for loaders, but only as an `.agi/context`
  conftest: it covers one pytest run, not a round's processes.
- `extensions/agi/bin/mem_cap.py` + `.agi/config.json` `memcap` exist (a memory ceiling seam).

## CLAIM
`dispatch.py` puts a round in a no-model fence when asked (a flag or a config default for the tier): every python process
the round starts -- parent, kids, their subprocesses -- inherits an env that installs an import-time guard (e.g. a
`sitecustomize` on a PYTHONPATH the dispatch sets) refusing the declared loaders BY NAME, reusing ONE loader table
(config, shared with the DH.392 conftest rather than a second copy). The exact TMM.228 call is refused in a fenced round.

## Falsifiers
1. In a subprocess started with the fenced env, a STAND-IN `transformers` module whose
   `AutoModelForCausalLM.from_pretrained` records its call: the call is not refused -> disproved.
2. A grandchild process (python spawned by python) of the fenced env escapes the guard -> disproved.
3. The loader list exists in two places (the conftest and the fence) -> disproved.
4. The python -I / -S bypass is neither closed (memory ceiling via mem_cap) nor named in the node as the residual -> disproved.
5. test_dispatch*.py regress -> disproved. No real transformers/torch is installed or imported; stand-ins only.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
STOPPED 13:3xZ on TMM.229 (Prime condition 4: no real model load from any process before PASS 9 closes; (d) holds all model rounds). DH.397 parent a00-aae44e7f + kid a00-1f6fc2ce TERMed (gone), worktree .agi/worktrees/a00-aae44e7f KEPT (kid experiment stub uncommitted). Re-dispatch ONLY after PASS 9 closes, with the fixture rule in the orders AND the test: red-on-old loads a tiny model GENERATED in tmp from a random-init config, never osc03/osc15/brain or any real weights dir; stand-in modules for the refusal itself.
<!-- THOUGHT:END -->
