# Bend 2.0.5 on the A1 (aarch64) — install, build, run

Host: ARM4C (arm-cloud aarch64), 4 cores, Ubuntu 24.04, kernel 6.17.
User prefix only — no sudo, nothing system-wide. Rollback = `rm -rf ~/.bend ~/.bun`.

## 1. Install (succeeds)

    curl -fsSL https://bend-lang.com/install.sh | sh     # script saved + run
    export PATH="$HOME/.bend/bin:$HOME/.bun/bin:$PATH"
    export BEND_NO_TELEMETRY=1
    bend --version        # -> bend 2.0.5
    # Bun installed to ~/.bun (77 MB); Bend 2.0.5 to ~/.bend (752 KB, launcher
    # self-fetches the 140 KB release tarball). PATH appended to ~/.bashrc by
    # the installer.

## 2. Native build FAILS — this box has no clang

    $ clang --version
    bash: clang: command not found
    $ bend gameoflife.bend -o gol            # CC unset
    Error: bend needs clang 14 or newer to build binaries (found no clang); on
    Debian/Ubuntu: curl -fsSL https://apt.llvm.org/llvm.sh | sudo bash -s 19;
    on macOS: xcode-select --install

`bend file.bend` (no -o) runs the JS backend sequentially — no --threads. The
official clang+llvm aarch64 tarballs are 1.0–1.1 GB (over the 500 MB cap) and
the box had 547 MB free at the time, so a real clang could not be installed.

## 3. Workaround: `zig cc` as a user-prefix clang shim (43 MB download)

    mkdir -p /dev/shm/zig && cd /dev/shm/zig
    curl -fsSL -o zig.tar.xz https://ziglang.org/download/0.13.0/zig-linux-aarch64-0.13.0.tar.xz
    tar xf zig.tar.xz
    mkdir -p /dev/shm/zig/bin
    printf '#!/bin/sh\nexec /dev/shm/zig/zig-linux-aarch64-0.13.0/zig cc "$@"\n' \
      > /dev/shm/zig/bin/clang && chmod +x /dev/shm/zig/bin/clang
    export CC=/dev/shm/zig/bin/clang
    /dev/shm/zig/bin/clang --version   # -> clang version 18.1.6 (zig-bootstrap)

`cc_find` in bend2/main.ts accepts `$CC`; zig's bundled clang 18 satisfies the
clang 14 requirement and compiles Bend's emitted C (`-std=c11 -O3 -lpthread
-lm`) cleanly. The `!`/GPU lane is not usable on this box (no CUDA/Metal), so
BendRT's CPU fork-join is what is measured.

## 4. Game of Life — shipped fixture `bench/runtime/gameoflife/main.bend`

    bend gameoflife.bend -o gol
    ./gol --threads 1     # 21.27 s wall (user 20.98), checksum 2016151040
    ./gol --threads 4     #  6.17 s wall (user 20.94), checksum 2016151040

Checksum matches the fixture header (big = 18, 32 -> 2016151040). 4-thread is
0.290x of 1-thread (3.45x speedup), inside conjunct (2)'s <= 1/3 bound.

## 5. LIF — `lif.bend`, f32, N=10000, 100 synapses/neuron, dt=0.1, 1000 steps

    bend lif.bend -o lif
    ./lif --threads 1     # 71.87 s wall (user 71.64), spikes 19983
    ./lif --threads 4     # 36.17 s wall (user 71.99), spikes 19983

## 6. f64 / f32 reference — `lif_baseline.py` (C, OpenMP over the 4 nets)

    python3 lif_baseline.py 1        # C/f64  5.997 s, 19983 spikes
    python3 lif_baseline.py 4        # C/f64  1.722 s, 19983 spikes
    python3 lif_baseline.py 1 f32    # C/f32  5.862 s, 19983 spikes
    python3 lif_baseline.py 4 f32    # C/f32  1.758 s, 19983 spikes

Bend's f32 spike count equals both C references exactly (19983) -> spike-count
drift vs the f64 baseline is 0 on this trajectory. Bend is ~12x slower than the
C/f64 baseline at 1 thread (5.56e5 vs 6.67e6 neuron-steps/s) and ~21x at 4
threads (1.11e6 vs 2.32e7), so conjunct (3)'s "within 2x" is falsified.

Load note: the box is shared (loadavg 1.9–3.3 during runs), so the LIF 4-thread
run used ~2.0 cores (user/wall) and its 1.99x speedup is contention-limited.

# Bend 2.0.5 on GPU2070S (x86-64) — CUDA lane half

Host: GPU2070S (x86-64, 16 vCPU, 15 GB RAM, 8192 MiB GPU, driver 595.84), Ubuntu 24.04.
Bend in a user prefix; sudo only for the toolchain. Rollback = `rm -rf ~/.bend ~/.bun`.

## 7. Install + toolchain (clang 19 + CUDA 12)

    curl -fsSL https://bend-lang.com/install.sh | sh   # FAILED first: "unzip is
    # required to install bun" -> sudo apt-get install -y unzip; rerun -> bend 2.0.5
    sudo apt-get install -y clang-19 nvidia-cuda-toolkit   # ~1.9 GB of .deb
    nvcc --version          # Cuda compilation tools, release 12.0, V12.0.140
    clang-19 --version      # clang version 19.1.1
    # nvrtc.h -> /usr/include/nvrtc.h, libs -> /usr/lib/x86_64-linux-gnu
    sudo mkdir -p /usr/local/cuda
    sudo ln -sfn /usr/include              /usr/local/cuda/include
    sudo ln -sfn /usr/lib/x86_64-linux-gnu /usr/local/cuda/lib64
    sudo ln -sfn /usr/bin                  /usr/local/cuda/bin
    export CC=clang-19 CUDA_HOME=/usr/local/cuda BEND_NO_TELEMETRY=1

clang 19 is REQUIRED for any `!` program (its `#embed` carries the device
program); clang 14+ is enough for a CPU-only build.

## 8. Game of Life — same fixture

    bend gameoflife.bend -o gol
    ./gol --threads 1     # 0.15 s wall, checksum 2016151040
    ./gol --threads 16    # 0.15 s wall, checksum 2016151040

Startup-dominated on this box; no scaling shape to read.

## 9. LIF — same workload, Bend CPU and Bend CUDA

    bend lif.bend -o lif
    ./lif --threads 1     # 52.94 s wall (user 52.91), spikes 19983
    ./lif --threads 16    # 26.96 s wall (user 53.71), spikes 19983   (1.96x)

`lif_gpu.bend` = `lif.bend` with the parallel call marked: the base case of
`batch` becomes `net!(s)` — the same 4 independent nets the CPU fork-join
parallelizes; only the `!` marker differs (Bend needs it for the GPU lane).

    bend lif_gpu.bend -o lifgpu      # emits lifgpu + lifgpu.gpu (76 KB) — succeeds
    ./lifgpu --threads 1   # 47.98 s wall (user 47.85), spikes 19983
    ./lifgpu --threads 16  # 48.12 s wall (user 47.94), spikes 19983   (1.00x)
    ./lifgpu --gpu 2GB     # 47.77 s wall (user 47.59), spikes 19983
    ./lifgpu --gpu 512MB   # 48.03 s wall (user 47.86), spikes 19983

CUDA lane engaged: during `--gpu 2GB` the process shows in
`nvidia-smi --query-compute-apps` at 104 MiB, and a control `pow2!(24n)` build
moves `utilization.gpu`. But for the LIF, `utilization.gpu` sampled every 2 s
for the whole 48 s run reads 0%, and wall == user: the CPU executes the loop.

## 10. Reference — lif_baseline.py (C, OpenMP) on GPU2070S

    python3 lif_baseline.py 16       # C/f64  1.264 s, 19983 spikes
    python3 lif_baseline.py 16 f32   # C/f32  1.057 s, 19983 spikes
    python3 lif_baseline.py 1        # C/f64  4.824 s, 19983 spikes

## DECIDING NUMBER

Bend-CUDA LIF 47.77 s / OpenMP-C f64 16-thread baseline 1.264 s = 37.8x slower;
vs the 1-thread baseline 9.9x slower. The ACCEPT falsifier allowed at most 5x ->
the node closes DISPROVED. Spike-count drift vs f64 = 0 (19983 everywhere).

Timing hygiene: `fetch_parallel.py pause` takes window in SECONDS and noise in
BYTES, so the working call is `pause 60 65536`; `pause 1800 2` waits 1800 s
(it was killed). Loadavg outside timed windows <= 0.5.
