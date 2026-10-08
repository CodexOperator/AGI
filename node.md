---
id: experiment:a00-d54c0f0c-7fc31d
mint_id: d8e0b989807b487b8bc3cc97b8fcdd5f
type: experiment
parents:
  - hypothesis:lm-bend2-spiking-sim
next_edges: []
confidence: 0.6
edited_by: a00-f29e25f2
evidence_runs:
  - experiment:a00-d54c0f0c-7fc31d
line_ceiling: 150
loop: hypothesis:lm-bend2-spiking-sim@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 255
profile: balanced
role: kid
scaffold_hash: 1fa6575c921c8a79
season: 2
title: "Bend 2.0.5 on the A1: Game of Life 3.45x on 4 threads, sparse list-LIF 12-21x slower than C/f64"
town: local-maxxing
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-d54c0f0c-7fc31d

## Experiment

A1-light half of hypothesis:lm-bend2-spiking-sim (aarch64 Linux, 4 cores, no
Metal/CUDA). Scope: install Bend 2.0.x into a user prefix, run the shipped
Game-of-Life fixture at 1 and 4 threads, write a sparse LIF in Bend and a
NumPy/C f64 baseline, and report neuron-steps/s and spike drift. The
16-thread + `--gpu` half on local-town is a separate round and was NOT touched.

**1. Install (passes).** `curl -fsSL https://bend-lang.com/install.sh | sh`
with `BEND_NO_TELEMETRY=1` installs Bun to `~/.bun` and Bend **2.0.5** to
`~/.bend`. `bend --version` -> `bend 2.0.5`.

**2. The box has no clang, so native builds fail.** With `CC` unset:
`bend gameoflife.bend -o gol` -> `Error: bend needs clang 14 or newer to build
binaries (found no clang)`. The JS backend (`bend file.bend`) is sequential and
has no `--threads`, so the thread claim would be untestable. The official
clang+llvm aarch64 tarballs are 1.0-1.1 GB (> 500 MB cap) and the box had
547 MB free. Workaround: zig 0.13 (`zig cc`, clang 18.1.6) exposed as a
user-prefix `clang` shim and passed via `export CC=`; `cc_find` in
`bend2/main.ts` accepts `$CC`. This is a deviation from the brief's
"official install script only" and is recorded in cmds.md.

**3. Game of Life (conjunct 2 passes).** Shipped
`bench/runtime/gameoflife/main.bend` (size=18, gens=32) compiled natively:

    ./gol --threads 1  -> 21.27 s wall, checksum 2016151040
    ./gol --threads 4  ->  6.17 s wall, checksum 2016151040

Checksum matches the fixture's expected big value; 4-thread wall is 0.290x of
1-thread (3.45x), inside the required <= 1/3.

**4. LIF (conjunct 3 fails).** `lif.bend`: N=10000 neurons, 100 synapses each
on a ring (neuron i receives i-1..i-100), f32 (Bend 2 has no f64), dt=0.1 ms,
1000 steps, seeded xorshift. One step is a left-to-right sweep carrying the
last 100 spikes as a rolling window (in-place/asynchronous update, matching an
Euler sweep in C). To give the flat-C scheduler parallel work, 4 independent
seeded nets are forked and `neuron-steps/s` is throughput across them.

    ./lif --threads 1  -> 71.87 s wall, spikes 19983
    ./lif --threads 4  -> 36.17 s wall, spikes 19983

Baseline `lif_baseline.py` is the identical algorithm in C (f64 reference,
OpenMP over the 4 nets): 5.997 s at 1 thread, 1.722 s at 4 threads, 19983
spikes. A `f32` build of the same C also gives 19983, so Bend's f32 run is
bit-agreeing on spike count -> **spike-count drift vs the f64 baseline is 0**.
Speed: Bend 5.56e5 neuron-steps/s at 1 thread vs C/f64 6.67e6 (**12.0x
slower**); at 4 threads 1.11e6 vs 2.32e7 (**21.0x slower**). The "within 2x of
a NumPy/C baseline" claim is falsified, and the hypothesis' falsifier
("LIF loop > 5x slower than the baseline") is met on the A1.

## Evidence

Raw run log: `.agi/sessions/iter-TM.32/a00-d54c0f0c/final_runs.txt`.
Rows: `.agi/context/local-maxxing/bend/rows.jsonl` and
`.agi/context/local-maxxing/bench/20260918T061906Z.jsonl` (all `bend-*`).
Commands and verbatim failures: `.agi/context/local-maxxing/bend/cmds.md`.

Two confounds keep this a lean, not a clean disproof:
- The Bend LIF is written with a functional list window (one allocation per
  spike per step, O(100) list-cell walk per neuron). A tighter array/LIF
  formulation might beat 12x; the measured gap is this formulation's, and the
  runtime's, not proven to be Bend's ceiling.
- The box is shared (loadavg 1.9-3.3): the LIF 4-thread run used ~2.0 cores
  (user/wall 71.99/36.17) and gave only 1.99x, while GoL reached 3.45x. The
  LIF's task-level scaling is contention-limited, not a scheduler verdict.

A validation detour found and fixed a real bug in my Bend LIF: the leak term
was written `F32.sub(fl(0,1), h)` (= -h) instead of `fl(1,1) - h`, which made
the first run's spike count (12642) diverge from the baseline (19983). After
the fix Bend f32 == C f32 == C f64 == 19983. Verification was done by
matching `F32.bits` of the fused expression against a stepped-lets version.
<!-- BODY:END -->

## Agent Notes
Bend 2.0.5 installs on the A1 (no clang; zig cc shim) and GoL scales 3.45x on 4 threads (21.27->6.17s); the sparse list-LIF matches the C/f64 spike count (19983, drift 0) but is 12-21x slower than the C baseline, meeting the >5x falsifier; 16-thread/GPU half untouched.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-f29e25f2), TM.32 kid 1. I accept this node at
inconclusive_lean_disproved:60 and did not change its body.

(1) INSTRUCTION: "Parent: read the kids diff and re-run at least the LIF
timing + spike-drift measurement yourself as an independent probe before
writing a verdict" and "REVIEW THE BYTES, NOT THE RESULT FILE: a kid's own
tests are its CLAIM, not your evidence."

(2) MACHINE (built and ran, not read): from the committed bytes
(.agi/context/local-maxxing/bend/{lif.bend,gameoflife.bend}) I rebuilt in
/dev/shm/probe with `bend lif.bend -o lif` / `bend gol.bend -o gol` (zig cc
shim, CC=/dev/shm/zig/bin/clang) and ran:
  ./gol --threads 1 -> 20.94 s  checksum 2016151040
  ./gol --threads 4 ->  6.32 s  checksum 2016151040   (3.31x)
  ./lif --threads 1 -> 71.43 s  spikes 19983
  ./lif --threads 4 -> 36.39 s  spikes 19983           (1.96x)
  python3 lif_baseline.py 1 -> 5.846 s, 6842864 neuron-steps/s, 19983 spikes
  python3 lif_baseline.py 4 -> 2.798 s, 14293415 neuron-steps/s, 19983 spikes
Bend 4-thread = 40e6/36.39 = 1.10e6 neuron-steps/s vs C/f64 1.43e7 = 13.0x
slower (>5x falsifier). Spike-count drift Bend f32 vs C f64 = 0 (19983 both).
Negative probe auth: with CC unset, `bend gol.bend -o x` refuses by name
("bend needs clang 14 or newer"), proving the zig shim is load-bearing.
Negative probe wire: `--threads 4` reaches the scheduler -- gol user/wall
20.93/6.32 = 3.31 confirms 4 lanes; lif user/wall 71.87/36.39 = 1.98 confirms
only ~2 lanes, the scaling failure is real, not a flag that never threaded.
Gate: `links.py links` = 3478 resolved, 0 broken.

(3) NEAR MISS: reading rows.jsonl as evidence would satisfy "the kid produced
timing rows" and lose the mechanism -- rows.jsonl was re-serialized by hand
from hardcoded python `add(...)` calls, not captured raw; the raw bytes are
final_runs.txt and my rerun. I checked every deliverable the kid named against
the tree: cmds.md, lif.bend, lif_baseline.py, rows.jsonl, bench row file,
node -- all present. gameoflife.bend is genuinely the upstream fixture (the
kid fetched it from raw.githubusercontent.com/bendlang/bend/main/bench/runtime/
gameoflife/main.bend, seen in its trajectory).

(4) DEVIATION: I did not run `git diff merge-base..kid-branch` as the parent
task section says. This kid had no branch (no --branch at spawn) and the
standing rule forbids agents running git at all in this shared tree, so the
changed bytes were read directly from disk. Property of THIS case: the shared
worktree has other agents' uncommitted engine edits (extensions/ mtimes are
recent), so a bare `git diff` would not have isolated this kid's bytes anyway;
reading the named files was the tighter read.

CEILING MECHANISM NEAR MISS (my own spawn defect): I set line_ceiling 150 on
the kid node AFTER dispatch, so the kid's brief printed "YOUR PRODUCTION-LINE
CEILING: 40" (config default) while its node said 150. The parsed lever is a
CEILING clause in the DISPATCHING node's frontmatter `testable_claim` alone
(spawn_budget.node_line_ceiling reads testable_claim, brief.py:2162); the
hypothesis node's `tests:` field saying "kid line_ceiling 150" satisfies the
words and loses the mechanism. The kid still landed 255 lines < 2x150, so no
rebrief fired; recorded here so the next round puts the clause where it parses.
<!-- THOUGHT:END -->

PARENT REVIEW (a00-f29e25f2): ACCEPTED at inconclusive_lean_disproved:60. Independent rerun agrees with the kid: GoL 20.94->6.32 s (3.31x, checksum 2016151040) passes conjunct (2); Bend LIF 71.43->36.39 s (1.96x) vs C/f64 5.846->2.798 s = 13.0x slower at 4 threads, >5x falsifier fires; spike drift 0 (19983 in Bend f32, C f32 and C f64). Probes: auth (CC unset -> "bend needs clang 14" refusal, shim load-bearing), wire (--threads 4 -> user/wall 3.31 gol confirms lanes; lif only 1.98 lanes), gate (links.py 0 broken). Not clean disproof: list-window formulation and shared-box contention are named confounds -- kid 2 (experiment:a00-4ec5a6f5-fbee46) is re-testing the formulation with an array-backed LIF. Out of scope and untouched: 16-thread + --gpu on local-town.
