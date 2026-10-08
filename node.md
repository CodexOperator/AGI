---
id: hypothesis:the-context-suite-refuses-a-model-load-by-construction
mint_id: 3e2906053cc3441abb24b9fb76f7b89b
type: hypothesis
parents:
  - hypothesis:context-fixture-tests-run-in-a-configured-suite
next_edges: []
edited_by: director-engine
scaffold_hash: ebf4ef39316fdca1
season: 2
testable_claim: "Running the declared .agi/context suite on a python with torch/transformers installed loads no weights: a conftest refuses torch.load / safetensors load / from_pretrained / gguf model construction by name, proved with stand-in modules."
title: "the .agi/context suite refuses a model load by construction, not by a missing torch (assigned: director-engine)"
town: core
---
# hypothesis:the-context-suite-refuses-a-model-load-by-construction

# hypothesis:the-context-suite-refuses-a-model-load-by-construction

## Measured
- DH.387 (experiment:a00-7bc04de0-bc3bff, lean_proved:70) made `.agi/context` a declared second suite
  (`paths.core.suite_roots`). Its falsifier 3 ("no model load") held INCIDENTALLY: this box's python has no
  torch/numpy, so the modules that would load weights skip or fail to import (TMM.220 residue 1).
- `git grep` 09-26: `.agi/context/local-maxxing/osc/test_osc_band_kquant_a00-ddd4762f.py` imports torch/numpy at top
  level; other osc tests use `pytest.importorskip`.
- belam [decision] 04:29Z: box memory guarded, no model loads on this box.

## CLAIM
Running the declared `.agi/context` suite on a python that HAS torch/numpy/transformers installed still loads no
model weights: a conftest under `.agi/context` refuses (fails the test by name) any call that would load weights --
`torch.load`, `safetensors` load, `from_pretrained`, `gguf`/`llama_cpp` model construction -- and the refusal is
proved with STAND-IN modules injected into `sys.modules`, never a real library or a real weights file.

## Falsifiers
1. With a stand-in `torch` whose `load` records the call, a context test calling `torch.load` passes silently -> disproved.
2. Same for `transformers.AutoModel.from_pretrained` and `safetensors.torch.load_file` stand-ins -> disproved.
3. The guard needs a real torch/transformers install, or any test allocates > ~200 MiB -> disproved.
4. The declared context suite's pass/skip count regresses vs the pre-change run -> disproved.
