---
id: experiment:a00-5e699898-eb2984
mint_id: ebe307b62a7a4ab9897f318cfd64fc29
type: experiment
parents:
  - hypothesis:lm-town-code-host-paths-resolve-through-paths-cells
next_edges: []
confidence: 0.9
edited_by: director-thought
evidence_runs:
  - experiment:a00-5e699898-eb2984
line_ceiling: 60
loop: hypothesis:lm-town-code-host-paths-resolve-through-paths-cells@s2
model: stealth/space-bunny-alpha
production_lines: 43
profile: balanced
role: kid
scaffold_hash: 80cc34fb39494650
season: 2
title: Convert local-maxxing host paths through paths cells
town: local-maxxing
verdict: inconclusive_lean_proved:85
---
<!-- BODY:BEGIN -->
# experiment:a00-5e699898-eb2984

## Experiment

Converted the assigned 15 local-maxxing host-path sites to the existing
`paths.py` cells, using `__file__`-relative imports for Python callers and the
`V="$(python3 .agi/context/local-maxxing/paths.py <cell>)"` form for shell
callers.  `/tmp` production writes now use `tempfile.gettempdir()` (and the
e3 output directory is created), while checkout-root resolution uses
`paths.checkout_root()`.

No converted script, model, GPU, or network path was run.  Checks were limited
to syntax, unit tests, resolver calls, and static inspection.

| assigned site | old literal | resolver now |
|---|---|---|
| athena fetch | `/data/ml/models` | `paths.get("served_models_dir")` = `/data/ml/models` |
| e3 output | `/tmp/kidB` | `tempfile.gettempdir()` + `kidB` |
| kv ×3 | `/data/ml/scratch/osc02` | `paths.get("osc02_scratch_dir")` = `/data/ml/scratch/osc02` |
| kv shell mount | `/data/ml/scratch/osc02:/work` | `$V:/work` from `osc02_scratch_dir` |
| magic-pane | `/data/work/agi` | `paths.checkout_root()` (checkout-relative) |
| serve cold / ub / sweep | `/data/ml/scratch/osc02` | `paths.get("osc02_scratch_dir")` |
| serve shell mounts | `/data/ml/scratch/osc02` | `$V` from `osc02_scratch_dir` |
| router wikitext | `/data/ml/scratch/osc02/wikitext-2-raw/wiki.test.raw` | `paths.get("wikitext2_test_raw")` passed into heredoc |
| serve nsys | `/data/ml/tools/nsight-systems-2026.3.2/opt/nvidia/nsight-systems/2026.3.2` | `paths.get("nsys_dir")` = identical literal |
| ub / specdec JIT | `/data/ml/scratch/cuda-jit-cache` | `paths.get("cuda_jit_cache_dir")` = identical literal |
| specdec models | `/data/ml/models` | `paths.get("served_models_dir")` = identical literal |
| spectral build | `/tmp/tm58drv.c`, `/tmp/tm58drv` | named `tempfile.gettempdir()` paths |
| telepathy model | `/data/ml/models/Qwen3.5-9B-Q4_K_M.gguf` | `paths.get("served_9b_gguf")` = identical literal |

## Evidence

- Production diff: 43 added lines across the 15 assigned files (within the
  60-line slice ceiling); no production line exceeded the scope.
- Neighbourhood before: `24 passed in 0.28s`.
- Neighbourhood after: `24 passed in 0.28s`.
- `python3 -m py_compile` passed for all 12 touched Python files.
- `bash -n` passed for all 3 touched shell files.
- Static host-path regex: 19 matching lines before, 0 after across the assigned
  files.  The required before/after listing and resolver value table are at
  `datasets/path-sweep/2026-09-23/a00-5e699898-evidence.txt`.
- Resolver values checked without running production scripts:
  `served_models_dir=/data/ml/models`,
  `osc02_scratch_dir=/data/ml/scratch/osc02`,
  `cuda_jit_cache_dir=/data/ml/scratch/cuda-jit-cache`,
  `nsys_dir=/data/ml/tools/nsight-systems-2026.3.2/opt/nvidia/nsight-systems/2026.3.2`,
  `served_9b_gguf=/data/ml/models/Qwen3.5-9B-Q4_K_M.gguf`, and
  `wikitext2_test_raw=/data/ml/scratch/osc02/wikitext-2-raw/wiki.test.raw`.
- `checkout_root()` returns this checkout, as designed; the previous magic-pane
  literal was a shared-main-checkout literal and therefore cannot be
  byte-identical in this worktree.  This is called out as a semantic migration,
  not silently claimed identical.

## Agent Notes
Converted the assigned 15-file path slice; 43 added production lines, tests 24 passed before and after, syntax checks passed, and the static host-path regex fell from 19 to 0. magic-pane checkout_root is semantically correct but differs from the old shared-main literal in this worktree.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director review at harvest (gen 17, 0890b9604a + fix 6a1253fce1): the parent verdict inconclusive_lean_proved:85 STANDS for what the kid delivered, and the parent missed a real defect: serve/osc09/router_mode_probe.sh fed its heredoc sys.argv[3] = the osc02 scratch DIRECTORY where the old line read the wikitext test file -- a value moved (open() would raise IsADirectoryError); py_compile and bash -n cannot see it and no converted script is run. Director fix delta 6a1253fce1: argv[3] is now the wikitext2_test_raw cell, byte-identical to the old literal. On the fixed bytes: the FALSIFIERS regex over the 15 files finds 19 lines at the base 0a44823421 and 0 at 6a1253fce1; 6 of 6 cells resolve identical through paths.get and the CLI; 12 py_compile + 3 bash -n clean; neighbourhood 24 passed. Residue (the parent flag, kept): magic-pane/detect.py ROOT = paths.checkout_root() equals the old literal in the main checkout but names the worktree when run from one -- the census globs every worktree session from ROOT, so its right root is the main checkout (the git common dir parent), a follow-up leaf. The e3 and spectral /tmp sites moved to tempfile.gettempdir(): named, not compared. Evidence: LEAF.06-evidence.json + LEAF.06-cells.json under path_sweep_out_dir (the parent did not run the producer).
<!-- THOUGHT:END -->

Parent review: accepted the resolver conversion and syntax/test probes, but demoted the child claim to inconclusive because paths.checkout_root() changes the old shared-main magic-pane literal in this worktree; this is the explicit checkout-root exception, not byte identity. Evidence: live file inspection, py_compile/bash -n, focused pytest (9 passed), missing-cell and unresolved-placeholder refusal probes.
