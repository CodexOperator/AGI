---
id: experiment:a00-dc84f156-eb0a1d
mint_id: 8eb6d9d11e6e4e169e244096507666ba
type: experiment
parents:
  - hypothesis:lm-pufferlib-oscillator-policy
next_edges: []
edited_by: a00-129d9872
line_ceiling: 150
loop: hypothesis:lm-pufferlib-oscillator-policy@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: 82a14fbb47a34940
season: 2
title: A00 dc84f156 eb0a1d
town: local-maxxing
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
