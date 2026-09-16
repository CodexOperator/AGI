#!/usr/bin/env python3
"""C2 Kid C (gate as a device: latency, memory, ledger) — digital Kuramoto in
flip mode, all-flip coupling.

Implements the byte-neuron INDEPENDENTLY from the spec in
hypothesis:c2-digital-kuramoto-flip-mode (CLAIM section):

  m_i uint8; per tick  m <- ((m*205)>>8) + I_i + kick_i + n_i
  205/256 = 0.8008 = E3 beta 0.8; n_i uniform in {-1,0,+1}
  spike s_i = carry-out (acc >= 256); reset = wrap (acc & 0xFF)
  flip f_i = s_i XOR s_i[t-1]
  DC drive I_i = round(N(80, sigma_I)) clipped [56,120]
  all-flip mean field kick_i = floor(K_int * F[t-1] / N), F = popcount(f)
  synchronous ticks; every neuron reads flips of t-1.

Order parameter (single-tick R, NOT the 2048-window mean): at every tick
  theta_i = 2*pi*(t - t_last_i)/(t_last_i - t_prev_i)
from the last two carry times; a neuron with t - t_last > 3 periods or < 2
carries is excluded; R_t is NaN if < N/2 remain (quiescent).  A tick with
mean spike rate >= 0.98 is the degenerate all-fire fixed point (R=1
trivially) and is flagged, never counted as 'synchronized'.

DEVICE: three phases per seed, N=256, sigma_I=10, seeds {0..4}:
  phase 1: K=0    for 1024 ticks  (fresh floor)
  phase 2: K_on   for 1024 ticks  (switch on)
  phase 3: K=0    for 1024 ticks  (post-sync floor)
K_on in {128,160,192,256}; the K_on=192 run is the primary device run.

CLAIM: R_off (mean single-tick R over the LAST 256 ticks of phase 3) is
>= 2 x the fresh R(0) of the SAME seed (Kid A's reference floor) in >= 4
of 5 seeds (the gate has memory).

Columns (information, not claim): T_sync (first tick of phase 2 with
R_t >= 0.5 held 32 ticks) for each K_on; T_desync (first tick of phase 3
with R_t <= 0.25 held 32 ticks, or None); us/tick at N in {256,1024,4096};
bytes/decision = N * T_sync * 4 + gate_state (N membranes 256 B + carry/flip
bit-vectors 64 B + 4N B spike timestamps).

Run:  ~/.venv-lm/bin/python c2_kidC_switch.py --out c2_kidC_results.json
"""
import argparse
import json
import os
import sys
import time

import numpy as np

N_DEFAULT = 256
PHASE_T = 1024
LAST_WINDOW = 256
HOLD = 32
LEAK = 205  # >>8 == E3 beta 0.8
CLIP_LO, CLIP_HI = 56, 120
DEGENERATE_RATE = 0.98
SIGMA_I = 10
KS_ON = [128, 160, 192, 256]
K_PRIMARY = 192
SEEDS = [0, 1, 2, 3, 4]
N_THREADS = 4

# Kid A's reference fresh floor R(0) at sigma_I=10, seeds {0..4}
# (experiment:a00-28814c2f-20cef8, c2_kidA_results.json
#  per_sigma.10.R_at_0_per_seed).  Used as the per-seed reference floor the
# claim compares R_off against; recomputed in-script too (see fresh_R0_script).
KID_A_R0 = [0.07312339946229363, 0.068815423849029, 0.08416663588633554,
            0.07191958826508849, 0.0637070484348929]

# gate state bytes: N membranes 256 B + carry/flip bit-vectors 64 B
# + 4N B spike timestamps
def gate_state_bytes(N):
    return N * 1 + 64 + 4 * N


def box_row():
    """loadavg (1/5/15) + MemAvailable kB — D1 tenancy protocol."""
    la = [float(x) for x in open("/proc/loadavg").read().split()[:3]]
    mem = None
    with open("/proc/meminfo") as fh:
        for line in fh:
            if line.startswith("MemAvailable:"):
                mem = int(line.split()[1])
                break
    return la, mem


def make_inputs(N, T, sigma_I, seed):
    """Same construction as Kid A so the K=0 floor is the same realisation."""
    ss = np.random.SeedSequence([int(seed), int(sigma_I)])
    rng = np.random.default_rng(ss)
    drive = np.clip(np.round(rng.normal(80.0, float(sigma_I), size=N)), CLIP_LO, CLIP_HI)
    drive = drive.astype(np.int32)
    m0 = rng.integers(0, 256, size=N).astype(np.int32)
    jit = rng.integers(-1, 2, size=(T, N)).astype(np.int32)
    return drive, m0, jit


def simulate_device(K_on, drive, m0, jit, N, phase_t, last_window):
    """Three phases (K=0, K_on, K=0).  Returns per-phase single-tick R arrays,
    per-phase spike-rate means, and the sorted carry times needed for
    T_sync / T_desync.  phase_t ticks per phase."""
    m = m0.copy()
    last = np.zeros(N, dtype=np.int64)
    prev = np.zeros(N, dtype=np.int64)
    nfire = np.zeros(N, dtype=np.int64)
    s_prev = np.zeros(N, dtype=bool)
    F = 0
    T = 3 * phase_t

    R_t = np.full(T + 1, np.nan)
    fire_t = np.zeros(T + 1, dtype=np.int64)  # spikes this tick (all neurons)
    tick_phase = np.zeros(T + 1, dtype=np.int64)
    K_tick = np.zeros(T + 1, dtype=np.int64)
    for t in range(1, T + 1):
        if t <= phase_t:
            K = 0
            ph = 1
        elif t <= 2 * phase_t:
            K = K_on
            ph = 2
        else:
            K = 0
            ph = 3
        tick_phase[t] = ph
        K_tick[t] = K

        kick = (K * F) // N
        acc = ((m * LEAK) >> 8) + drive + kick + jit[t - 1]
        s = acc >= 256
        m = acc & 0xFF
        f = s ^ s_prev
        F = int(f.sum())

        idx = np.flatnonzero(s)
        fire_t[t] = int(idx.size)
        if idx.size:
            prev[idx] = last[idx]
            last[idx] = t
            nfire[idx] += 1

        per = last - prev
        valid = (nfire >= 2) & (per > 0) & ((t - last) <= 3 * per)
        if int(valid.sum()) >= N // 2:
            th = 2.0 * np.pi * (t - last[valid]) / per[valid]
            R_t[t] = abs(np.exp(1j * th).mean())
        s_prev = s

    return R_t, fire_t, tick_phase, K_tick


def held(mask, hold):
    """First index i such that mask[i:i+hold] all True; None if never."""
    if hold <= 0:
        return None
    run = 0
    for i, v in enumerate(mask):
        if v:
            run += 1
            if run >= hold:
                return i - hold + 1
        else:
            run = 0
    return None


def phase_slice(R_t, phase, t0, t1):
    return R_t[t0:t1 + 1][phase[t0:t1 + 1] == 1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="c2_kidC_results.json")
    ap.add_argument("--seeds", default=",".join(str(s) for s in SEEDS))
    ap.add_argument("--ks", default=",".join(str(k) for k in KS_ON))
    ap.add_argument("--N", type=int, default=N_DEFAULT)
    ap.add_argument("--T", type=int, default=PHASE_T)
    ap.add_argument("--window", type=int, default=LAST_WINDOW)
    args = ap.parse_args()

    for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ.setdefault(v, str(N_THREADS))

    seeds = [int(x) for x in args.seeds.split(",")]
    ks = [int(x) for x in args.ks.split(",")]
    N, PT, W = args.N, args.T, args.window

    t_start = time.time()
    la0, mem0 = box_row()

    device_rows = []
    per_seed = {}

    for seed in seeds:
        T = 3 * PT
        drive, m0, jit = make_inputs(N, T, SIGMA_I, seed)
        seed_rec = {"seed": seed, "runs": {}}
        for K_on in ks:
            t0 = time.time()
            R_t, fire_t, phase, Kt = simulate_device(
                K_on, drive, m0, jit, N, PT, W)
            wall = time.time() - t0

            # --- single-tick R per phase ---
            R1 = R_t[1:PT + 1]
            R2 = R_t[PT + 1:2 * PT + 1]
            R3 = R_t[2 * PT + 1:3 * PT + 1]

            r0_fresh = float(np.nanmean(R1[-W:])) if np.isfinite(R1[-W:]).any() else float("nan")
            r_off = float(np.nanmean(R3[-W:])) if np.isfinite(R3[-W:]).any() else float("nan")

            # --- T_sync: first tick of phase 2 with R >= 0.5 held HOLD ---
            mask_on = np.zeros(PT, dtype=bool)
            for i in range(PT):
                v = R2[i]
                if np.isfinite(v) and v >= 0.5:
                    mask_on[i] = True
            i_sync = held(mask_on, HOLD)
            T_sync = int(i_sync) + 1 if i_sync is not None else None  # ticks after K_on

            # --- T_desync: first tick of phase 3 with R <= 0.25 held HOLD ---
            mask_off = np.zeros(PT, dtype=bool)
            for i in range(PT):
                v = R3[i]
                if np.isfinite(v) and v <= 0.25:
                    mask_off[i] = True
            i_des = held(mask_off, HOLD)
            T_desync = int(i_des) + 1 if i_des is not None else None  # ticks after K_off

            r2_tail = float(np.nanmean(R2[-W:]))
            F1 = fire_t[1:PT + 1]
            F2 = fire_t[PT + 1:2 * PT + 1]
            F3 = fire_t[2 * PT + 1:3 * PT + 1]
            rate1 = float(np.mean(F1[-W:])) / N
            rate2 = float(np.mean(F2[-W:])) / N
            rate3 = float(np.mean(F3[-W:])) / N
            deg = bool(rate2 >= DEGENERATE_RATE)

            la, mem = box_row()
            row = {
                "phase_ticks": PT, "N": N, "sigma_I": SIGMA_I, "seed": seed,
                "K_on": int(K_on),
                "R0_fresh_script": r0_fresh,
                "R_lock_phase2_last256": r2_tail,
                "R_off_phase3_last256": r_off,
                "R0_fresh_kidA_reference": float(KID_A_R0[seeds.index(seed)]),
                "ratio_Roff_over_R0_kidA": (r_off / KID_A_R0[seeds.index(seed)])
                if KID_A_R0[seeds.index(seed)] > 0 else None,
                "ratio_Roff_over_R0_script": (r_off / r0_fresh) if r0_fresh > 0 else None,
                "T_sync_ticks": T_sync,
                "T_desync_ticks": T_desync,
                "phase2_degenerate": deg,
                "spike_rate_phase1_last256": rate1,
                "spike_rate_phase2_last256": rate2,
                "spike_rate_phase3_last256": rate3,
                "wall_s": wall,
                "loadavg_1_5_15": la, "MemAvailable_kB": mem,
            }
            device_rows.append(row)
            seed_rec["runs"][str(K_on)] = row
            if K_on == K_PRIMARY:
                seed_rec["primary"] = row
                seed_rec["R_t_phase3_last256"] = [
                    float(x) if np.isfinite(x) else None for x in R3[-W:]]
        per_seed[seed] = seed_rec

    # ---------- claim: primary K_on=192 ----------
    prim = [per_seed[s]["primary"] for s in seeds]
    clears_kidA = [bool(r["R_off_phase3_last256"] >= 2.0 * r["R0_fresh_kidA_reference"])
                   for r in prim]
    clears_script = [bool(r["R_off_phase3_last256"] >= 2.0 * r["R0_fresh_script"])
                     for r in prim]
    n_clear_kidA = int(sum(clears_kidA))
    n_clear_script = int(sum(clears_script))
    claim = {
        "K_primary": K_PRIMARY,
        "R_off_per_seed": [r["R_off_phase3_last256"] for r in prim],
        "R0_kidA_reference_per_seed": [r["R0_fresh_kidA_reference"] for r in prim],
        "R0_fresh_script_per_seed": [r["R0_fresh_script"] for r in prim],
        "ratio_Roff_over_R0_kidA_per_seed": [r["ratio_Roff_over_R0_kidA"] for r in prim],
        "ratio_Roff_over_R0_script_per_seed": [r["ratio_Roff_over_R0_script"] for r in prim],
        "clears_2x_kidA_per_seed": clears_kidA,
        "clears_2x_script_per_seed": clears_script,
        "n_seeds_clearing_2x_kidA": n_clear_kidA,
        "n_seeds_clearing_2x_script": n_clear_script,
        "claim_holds_kidA_ge4of5": bool(n_clear_kidA >= 4),
        "claim_holds_script_ge4of5": bool(n_clear_script >= 4),
    }

    # ---------- columns ----------
    tsync = {str(k): [per_seed[s]["runs"][str(k)]["T_sync_ticks"] for s in seeds]
             for k in ks}
    tdesync = {str(k): [per_seed[s]["runs"][str(k)]["T_desync_ticks"] for s in seeds]
               for k in ks}

    # ---------- us/tick at N in {256, 1024, 4096} (K=192 device loop) ----------
    bench = {}
    for Nb in (256, 1024, 4096):
        drive, m0, jit = make_inputs(Nb, 3 * PT, SIGMA_I, 0)
        t0 = time.time()
        simulate_device(K_PRIMARY, drive, m0, jit, Nb, PT, W)
        w = time.time() - t0
        la, mem = box_row()
        bench[str(Nb)] = {"ticks": 3 * PT, "wall_s": w,
                          "us_per_tick": 1e6 * w / (3 * PT),
                          "loadavg_1_5_15": la, "MemAvailable_kB": mem}

    # ---------- bytes/decision ----------
    gsb = gate_state_bytes(N)
    bytes_decision = {}
    for k in ks:
        ts = [t for t in tsync[str(k)] if t]
        med = float(np.median(ts)) if ts else None
        bytes_decision[str(k)] = {
            "T_sync_median": med,
            "gate_state_bytes": gsb,
            "bytes_per_decision_formula": "N * T_sync * 4 + gate_state",
            "bytes_per_decision_at_Tsync_median": (N * med * 4 + gsb) if med else None,
            "bytes_per_decision_at_Tsync_1": N * 1 * 4 + gsb,
            "bytes_per_decision_at_Tsync_64": N * 64 * 4 + gsb,
        }

    wall_total = time.time() - t_start
    la1, mem1 = box_row()

    out = {
        "spec": {
            "N": N, "phase_ticks": PT, "phases": [0, K_PRIMARY, 0],
            "last_window": W, "hold": HOLD, "seeds": seeds, "Ks_on": ks,
            "sigma_I": SIGMA_I, "leak": "205/256=0.8008",
            "drive": "round(N(80,sigma)) clip [56,120]",
            "kick": "floor(K_int*F/N), F=popcount(flip vector)",
            "spike": "carry-out acc>=256, wrap", "flip": "s XOR s_prev",
            "R_estimator": ("SINGLE-TICK R: theta_i=2pi(t-t_last)/(t_last-t_prev); "
                            "excluded if t-t_last>3*period or <2 fires; R NaN if "
                            "<N/2 remain; tick degenerate if mean rate>=0.98"),
            "T_sync": "first tick of phase 2 with R>=0.5 held 32",
            "T_desync": "first tick of phase 3 with R<=0.25 held 32, or None",
            "degenerate_rate": DEGENERATE_RATE,
            "threads": N_THREADS, "numpy": np.__version__,
            "python": sys.version.split()[0],
            "n_device_runs": len(device_rows),
            "n_seeds": len(seeds),
        },
        "box": {
            "loadavg_1_5_15_at_start": la0, "MemAvailable_kB_at_start": mem0,
            "loadavg_1_5_15_at_end": la1, "MemAvailable_kB_at_end": mem1,
            "nproc": os.cpu_count(), "wall_s_total": wall_total,
        },
        "claim": claim,
        "columns": {
            "T_sync_per_Kon_ticks": tsync,
            "T_desync_per_Kon_ticks": tdesync,
            "us_per_tick": bench,
            "bytes_per_decision": bytes_decision,
        },
        "device_rows": device_rows,
    }
    with open(args.out, "w") as fh:
        json.dump(out, fh, indent=1)

    print("wall_s_total=%.1f device_runs=%d" % (wall_total, len(device_rows)))
    print("CLAIM K_on=%d: R_off/R0(kidA) per seed = %s"
          % (K_PRIMARY, ["%.2f" % x for x in claim["ratio_Roff_over_R0_kidA_per_seed"]]))
    print("  clears 2x kidA: %s  (%d/5) holds=%s"
          % (claim["clears_2x_kidA_per_seed"], n_clear_kidA,
             claim["claim_holds_kidA_ge4of5"]))
    print("  clears 2x script: %d/5 holds=%s"
          % (n_clear_script, claim["claim_holds_script_ge4of5"]))
    print("  R_off=%s" % ["%.4f" % x for x in claim["R_off_per_seed"]])
    print("  R0(kidA)=%s" % ["%.4f" % x for x in claim["R0_kidA_reference_per_seed"]])
    print("T_sync per K_on: %s" % {k: tsync[k] for k in tsync})
    print("T_desync per K_on: %s" % {k: tdesync[k] for k in tdesync})
    print("us/tick: %s" % {k: round(v["us_per_tick"], 2) for k, v in bench.items()})
    print("bytes/decision: %s"
          % {k: bytes_decision[str(k)]["bytes_per_decision_at_Tsync_median"] for k in ks})
    print("wrote %s" % args.out)


if __name__ == "__main__":
    main()
