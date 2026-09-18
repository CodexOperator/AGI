---
id: experiment:a00-dc84f156-eb0a1d
mint_id: 8eb6d9d11e6e4e169e244096507666ba
type: experiment
parents:
  - hypothesis:lm-pufferlib-oscillator-policy
next_edges: []
confidence: 0.9
edited_by: a00-129d9872
evidence_runs:
  - experiment:a00-dc84f156-eb0a1d
line_ceiling: 150
loop: hypothesis:lm-pufferlib-oscillator-policy@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 92
profile: balanced
role: kid
scaffold_hash: 82a14fbb47a34940
season: 2
title: PufferLib 5.0 does not build CPU-only on ARM4C aarch64 - raylib pinned amd64 and native trainer needs CUDA
town: local-maxxing
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-dc84f156-eb0a1d

## Experiment

ARM4C half of hypothesis:lm-pufferlib-oscillator-policy: can PufferLib 5.0-experiments install and build CPU-only on aarch64 with no CUDA, and does breakout train run?

Tag check: `git ls-remote --tags` gave `5.0-experiments -> 89414204ce8509c3fecede41f5dc432e33e35908`. Shallow `git clone --depth 1 --branch 5.0-experiments` = 222 MB (full repo ~926 MB avoided). venv created under `.agi/context/local-maxxing/puffer/`.

Size gate: release asset `puffer5_models.zip` = 213593501 B (213.6 MB) <= 500 MB, so it was fetched.

Install shape: the tag has NO `pyproject.toml` and NO `setup.py`; there is no `pufferlib` Python package (the `tests/test_api.py` imports are stale 4.x leftovers). Install is `build.sh`. The trainer is `src/pufferl.cu`, compiled by `$CUDA_HOME/bin/nvcc` and linked against cudart/cublas/cusolver/nccl. No CPU fallback trainer source exists.

Attempt 1 (native trainer): `CUDA_HOME=/nonexistent ./build.sh breakout` -> `ccache: command not found` (EXIT 127); `nvcc` MISSING on this box. A CUDA toolkit is required, so the trainer cannot build CPU-only.

Attempt 2 (the only CPU target): `./build.sh breakout --cpu`. With `CC=gcc` it dies on clang-only flag `-ferror-limit=3` (EXIT 1). After installing clang 18 + ccache + libgl-dev and running as shipped:

```
/usr/bin/ld: raylib-5.5_linux_amd64/lib/libraylib.a(rcore.o): Relocations in generic ELF (EM: 62)
/usr/bin/ld: raylib-5.5_linux_amd64/lib/libraylib.a: error adding symbols: file in wrong format
clang: error: linker command failed with exit code 1
```

`build.sh` pins `RAYLIB_NAME=raylib-5.5_linux_amd64` on every Linux host; EM:62 is x86-64, so it cannot link on aarch64. Even if it linked, `--cpu` builds `src/puffercpu.c`, a forward-pass-only play/eval binary (no backprop, no optimizer), not a trainer.

## Evidence

First falsifier condition trips: PufferLib 5.0 does NOT build CPU-only on aarch64. No timing rows exist because no binary was produced. Full commands and raw output: `.agi/context/local-maxxing/puffer/cmds.md`; machine-readable rows: `.agi/context/local-maxxing/puffer/bench/20260918T174200Z.jsonl`.

Rollback scope untouched: `rm -rf venv pufferlib puffer5_models.zip`. No remote or off-box machine touched; no RL run attempted; rhythm_bank env not built.

## Agent Notes
PufferLib 5.0-experiments has no CPU-only path on ARM4C. Native trainer src/pufferl.cu requires nvcc/CUDA and nvcc is absent. The only CPU target builds src/puffercpu.c (forward-pass play/eval, no backprop) and fails to link because build.sh pins raylib-5.5_linux_amd64 (EM:62 x86-64) on aarch64. First falsifier condition trips. puffer5_models.zip 213.6MB <= 500MB was fetched. No timing rows since no binary was produced.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-129d9872), ARM4C half. Read the bytes, not the result file: the diff carries cmds.md, bench/20260918T174200Z.jsonl (3 rows), and this node; it does NOT carry rhythm_bank_env.py, and the kid says so explicitly ("rhythm_bank env not built this half"), which matches the director scoping. Verified every named deliverable exists on disk. Ran three independent negative probes: (gate) `env CC=clang bash ./build.sh breakout --cpu` on aarch64 -> ld raylib EM:62 file in wrong format, exit 1 -- the shipped CPU target cannot link here; (wire) build.sh:444 sets NVCC="ccache $CUDA_HOME/bin/nvcc" and the trainer source is src/pufferl.cu (CUDA), while `command -v nvcc` is empty -- the trainer compile path reaches nvcc and no CPU trainer source exists; (gate) no pyproject.toml, setup.py or root .py -- no pip install path in the tag. Kid caveat stands: it did not prove that a from-source aarch64 raylib cannot link, so the precise true statement is "no CPU-only trainer and the shipped CPU build fails", not "no aarch64 binary is theoretically buildable". That caveat does not rescue conjunct 1, because the only CPU target (src/puffercpu.c) is forward-pass play/eval, not a trainer. Verdict disproved (ARM4C arm of conjunct 1) accepted; evidence_runs cites this node.
<!-- THOUGHT:END -->
