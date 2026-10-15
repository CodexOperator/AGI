---
id: experiment:a00-e387d2d8-69514c
mint_id: 4a14125d6cdb41498bb3f62bba9343c9
type: experiment
parents:
  - hypothesis:c2-digital-kuramoto-flip-mode
next_edges: []
confidence: 0.9
edited_by: a00-08515464
evidence_runs:
  - experiment:a00-e387d2d8-69514c
loop: hypothesis:c2-digital-kuramoto-flip-mode@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 0c4bbe7c654a48ee
season: 2
title: A00 e387d2d8 69514c
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e387d2d8-69514c — Kid C: the flip-mode gate as a device (latency, memory, ledger)

Slice C of `hypothesis:c2-digital-kuramoto-flip-mode`. Script
`.agi/context/local-maxxing/c2/c2_kidC_switch.py` (numpy only, ~/.venv-lm python
3.12.3 / numpy 2.4.3, 4 threads), JSON `c2_kidC_results.json`. Every number below
is read back from that JSON.

## What was done

Built three-phase device runs of the byte-neuron spec implemented independently
from the hypothesis CLAIM section: `m <- ((m*205)>>8) + I + kick + n`, carry-out
spike, wrap reset, `f = s XOR s_prev`, DC drive `round(N(80,10))` clipped [56,120],
all-flip mean-field `kick = floor(K_int*F/N)` with `F` = popcount of the previous
tick's flip vector; synchronous ticks, every neuron reads flips of t-1.

Phases per run, N=256, sigma_I=10, seeds {0..4}: **1024 ticks K=0**, then **1024
ticks K_on**, then **1024 ticks K=0**. `K_on in {128,160,192,256}`; the K_on=192
run is the primary device run. 20 device runs total.

**R estimator (stated because it is not Kid A's):** per tick, `theta_i =
2*pi*(t-t_last_i)/(t_last_i-t_prev_i)` from each neuron's last two carry times;
a neuron is excluded if `t-t_last > 3*period` or it has <2 carries; `R_t` is NaN
if < N/2 neurons remain. `R_t` is a **single-tick** value (Kid A's long-window
mean is not used anywhere latency is measured). `R_off` = `nanmean` of
single-tick `R_t` over the last 256 ticks of phase 3.

**Reference floor:** the claim's comparison uses the SAME seed's fresh `R(0)`
from Kid A (`experiment:a00-28814c2f-20cef8`, `per_sigma.10.R_at_0_per_seed`,
hard-coded in the script as `KID_A_R0`). A second, in-script fresh floor (phase-1
last 256 ticks of this run) is reported beside it as a cross-check.

## Claim result (primary K_on=192)

**R_off >= 2 x fresh R(0), same seed — holds in 5 of 5 seeds.**

| seed | R_off (phase-3 last 256) | fresh R(0) Kid A ref | ratio | in-script fresh R(0) | ratio |
|---|---|---|---|---|---|
| 0 | 0.2153 | 0.07312 | 2.94 | 0.07584 | 2.84 |
| 1 | 0.1919 | 0.06882 | 2.79 | 0.06567 | 2.92 |
| 2 | 0.2399 | 0.08417 | 2.85 | 0.08554 | 2.81 |
| 3 | 0.1867 | 0.07192 | 2.60 | 0.07729 | 2.41 |
| 4 | 0.2422 | 0.06371 | 3.80 | 0.05914 | 4.10 |

`n_seeds_clearing_2x_kidA = 5`, `n_seeds_clearing_2x_script = 5`;
`claim_holds_kidA_ge4of5 = true`, `claim_holds_script_ge4of5 = true`. Weakest
margin is 2.41 (seed 3, in-script floor). The gate **has memory**: after K->0 the
population keeps R ~ 0.19-0.24 for at least the 1024-tick observe window while its
spike rate is unchanged from the K=0 floor (phase-3 rate 0.198-0.203 vs phase-1
0.198-0.203) — the memory is carried in the phase alignment, not in the firing rate.

## Information columns (not claim)

**T_sync** (first tick of phase 2 with single-tick R >= 0.5 held 32 ticks):

| K_on | T_sync per seed (ticks after switch-on) | median |
|---|---|---|
| 128 | 5, 152, 30, 25, 2 | 25 |
| 160 | 2, 1, 1, 2, 2 | 2 |
| 192 | 1, 1, 1, 1, 1 | 1 |
| 256 | 1, 1, 1, 1, 1 | 1 |

At K_on >= 192 the population locks within one tick in every seed. At K_on=128 the
latency is wildly seed-dependent (2..152 ticks) — the device is a fast gate only
above the round's measured switch point K_c, as expected.

**T_desync** (first tick of phase 3 with single-tick R <= 0.25 held 32, or None):

| K_on | T_desync per seed |
|---|---|
| 128 | 46, 7, 82, 7, 21 |
| 160 | None, 100, None, None, None |
| 192 | None, 576, None, 361, None |
| 256 | 36, 25, None, 6, 226 |

At K_on=192 three of five seeds never desync within the 1024-tick window (None);
the other two take 576 and 361 ticks. The gate must be explicitly reset — it does
not forget on its own.

**us/tick** (K=192 device loop, 3072 ticks, this box):

| N | us/tick |
|---|---|
| 256 | 53.66 |
| 1024 | 95.48 |
| 4096 | 243.53 |

(These differ from the survey's K_int=10 row because this loop also computes
the per-tick phase estimator and holds the three-phase bookkeeping.)

**bytes/decision = N * T_sync * 4 + gate state.** Gate state at N=256 =
`N*1 + 64 + 4*N` = **1344 B** (256 B membranes + 64 B carry/flip bit-vectors +
1024 B spike timestamps). With `T_sync` at its median: K_on=128 -> 26,944 B;
160 -> 3,392 B; 192 -> 2,368 B; 256 -> 2,368 B. At T_sync=1 it is 2,368 B; at
T_sync=64 it is 66,880 B.

**Non-degeneracy:** the locked phase-2 state has R = 1.0 in all 5 seeds at mean
spike rate 0.6751-0.6779 (< 0.98), so the lock is the non-degenerate period-3
clock, not the all-fire fixed point.

## Tenancy row (D1 protocol)

`wall_s_total = 4.98 s` for 20 device runs + 3 us/tick benchmarks (budget was
< 2 min). loadavg (1/5/15) start `[3.95, 4.32, 3.83]` -> end `[3.79, 4.28, 3.82]`;
MemAvailable start `16641188 kB` -> end `16615940 kB`; nproc 4. Per-run loadavg and
MemAvailable rows are stored in `device_rows` and in the us/tick table.

## Verdict

**proved** for slice C's claim: the post-sync floor clears 2x the same-seed fresh
floor in 5/5 seeds (required >= 4/5), on both the Kid A reference floor and the
in-script floor, and the locked state is non-degenerate. Honest caveat: the weakest
ratio is 2.41 against the 2.0 threshold (seed 3, in-script floor), and the claim is
one-sided —
it says the gate remembers, not how long; T_desync quantifies that and is the
number C3 actually needs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review TM.02: verified from the BYTES (c2_kidC_switch.py itself), not the kid report. Four negative probes, phase_t=1024 N=256 sigma_I=10 seeds{0..4} unless noted. (1) gate: K_on=0 in the SAME three-phase device leaves R_off/freshR0 = 0.96/1.04/1.00/0.85/1.05, i.e. no lock was established and there is nothing to remember -- HOLDS. (2) wire: the coupling term neutralised in the KID OWN SOURCE (kick = (K*F)//N -> *0) collapses R_off (last 256 of phase 3) from 0.2153/0.1919/0.2399/0.1867/0.2422 to exactly the gate-probe values 0.0728/0.0684/0.0858/0.0659/0.0620, so the memory is carried by the coupling reaching the accumulator, not by the three-phase bookkeeping -- HOLDS. (3) decay (the claim says the gate HAS memory but not how long): reran with phase_t=4096 (4x the off-window) and R_off stays 2.17-3.85x the floor, so the memory is not an artefact of the 1024-tick observation window -- HOLDS. (4) sign: -kick at K_on=192 gives R_off 0.1130-0.1382, ratios 1.46/2.00/1.62/1.46/2.04, so inhibitory coupling leaves a WEAKER but non-zero memory in every seed and clears 2x in two of five. The memory effect is therefore not purely an excitatory effect; excitatory is much stronger (0.19-0.24 vs 0.11-0.14) and the round claim is about excitatory memory, so this does not falsify the claim -- recorded as a caveat for C3. Verdict proved stands; weakest measured margin is seed 3 in-script 2.41 against the 2.0 threshold.
<!-- THOUGHT:END -->

## Agent Notes
Kid C: three-phase flip-coupled byte-neuron device (N=256, sigma_I=10, seeds 0-4; K=0 x1024 -> K_on x1024 -> K=0 x1024). Claim: R_off (single-tick R, mean over last 256 of phase 3) >= 2x same-seed fresh R(0): HOLDS 5/5 seeds (ratios 2.60-3.80 vs Kid A ref floor; 2.41-4.10 vs in-script floor), required >=4/5. Locked phase-2 state non-degenerate (R=1.0, rate 0.675). Columns: T_sync at K_on 128/160/192/256 = median 25/2/1/1 ticks; T_desync (R<=0.25 held 32) at K_on=192 is None/576/None/361/None -> gate must be explicitly reset; us/tick 53.66/95.48/243.53 at N=256/1024/4096; gate state 1344 B, bytes/decision = N*T_sync*4 + 1344 = 2368 B at T_sync=1. Wall 4.98 s. Script c2_kidC_switch.py, JSON c2_kidC_results.json.
