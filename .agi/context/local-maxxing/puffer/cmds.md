# puffer — cmds run (2026-09-18, kid a00-dc84f156, TM.38) — ARM4C half

PufferLib 5.0-experiments, tag `5.0-experiments`, commit `89414204ce8509c3fecede41f5dc432e33e35908`, shallow depth 1.
Install probe only; no RL training, no rhythm_bank. Rows: `bench/20260918T174200Z.jsonl`.

## Setup (ARM4C = aarch64, 4 cores, no CUDA)
```
cd .agi/context/local-maxxing/puffer
git clone --depth 1 --branch 5.0-experiments https://github.com/PufferAI/PufferLib.git pufferlib   # 222 MB shallow
python3 -m venv venv && ./venv/bin/python -m pip install --upgrade pip
curl -sL -o puffer5_models.zip https://github.com/PufferAI/PufferLib/releases/download/5.0-experiments/puffer5_models.zip
# size gate: 213593501 B (213.6 MB) <= 500 MB -> fetched
```

## Falsifier attempt 1 — native trainer needs CUDA
```
sudo apt-get install -y clang libgl-dev ccache    # build.sh wants clang+ccache; box had gcc only
env CC=gcc CUDA_HOME=/nonexistent bash ./build.sh breakout
# ./build.sh: line 506: ccache: command not found         EXIT 127
command -v nvcc                                           # MISSING
```
Native MODE compiles `src/pufferl.cu` via `$CUDA_HOME/bin/nvcc` (cudart/cublas/cusolver/nccl). No CPU trainer source exists.

## Falsifier attempt 2 — only CPU target, as shipped
```
env CC=gcc bash ./build.sh breakout --cpu
# gcc: error: unrecognized command-line option -ferror-limit=3    EXIT 1  (clang-only flags)
bash ./build.sh breakout --cpu      # after clang 18 + ccache + libgl-dev
# ld: raylib-5.5_linux_amd64/lib/libraylib.a(rcore.o): Relocations in generic ELF (EM: 62)
# ld: ... file in wrong format ; clang: linker command failed     EXIT 1
```
`RAYLIB_NAME` is pinned to linux_amd64 on any Linux; EM:62 is x86-64, cannot link on aarch64.
`--cpu` builds `src/puffercpu.c`: forward-pass-only play/eval, no backprop or optimizer. Not a trainer.

## Result
No CPU-only build succeeds on ARM4C; first falsifier condition trips. No binary, so no timing rows.
No pip package in the tag (no pyproject.toml/setup.py). Rollback: `rm -rf venv pufferlib puffer5_models.zip`.
