#!/usr/bin/env python3
"""C2 Kid A (decisive curve) — digital Kuramoto in flip mode, all-flip coupling.

Implements the byte-neuron INDEPENDENTLY from the spec in
hypothesis:c2-digital-kuramoto-flip-mode (CLAIM section):

  m_i uint8; per tick  m <- ((m*205)>>8) + I_i + kick_i + n_i
  205/256 = 0.8008 = E3 beta 0.8; n_i uniform in {-1,0,+1}
  spike s_i = carry-out (acc >= 256); reset = wrap (acc & 0xFF)
  flip f_i = s_i XOR s_i[t-1]
  DC drive I_i = round(N(80, sigma_I)) clipped [56,120]
  all-flip mean field kick_i = floor(K_int * F[t-1] / N), F = popcount(f)
  synchronous ticks; every neuron reads flips of t-1.

Order parameter: theta_i = 2*pi*(t - t_last_i)/(t_last_i - t_prev_i)
from the last two carry times; a neuron with t - t_last > 3 periods is
excluded; R undefined if < N/2 remain; a window with mean spike rate
>= 0.98 is the degenerate all-fire fixed point.

Grid K_int = 0..256 step 8 (33 points), 4096 ticks, R averaged over the
last 2048; seeds {0..4}.

Run:  ~/.venv-lm/bin/python c2_kidA_sweep.py --out c2_kidA_results.json
"""
import argparse
import json
import os
import time

import numpy as np

N = 256
T = 4096
WINDOW = 2048
KS = list(range(0, 257, 8))  # 33 points
LEAK = 205  # >>8  == E3 beta 0.8
CLIP_LO, CLIP_HI = 56, 120
DEGENERATE_RATE = 0.98
N_THREADS = 4


def box_row():
    """loadavg (1/5/15) + MemAvailable kB — D1 tenancy protocol, one row per number."""
    la = [float(x) for x in open("/proc/loadavg").read().split()[:3]]
    mem = None
    with open("/proc/meminfo") as fh:
        for line in fh:
            if line.startswith("MemAvailable:"):
                mem = int(line.split()[1])
                break
    return la, mem


def make_inputs(N, T, sigma_I, seed):
    """Per (seed, sigma): drives, initial membranes, jitter matrix.

    The jitter matrix is drawn once per (seed, sigma) and reused across K so
    that the K sweep at fixed seed is a paired comparison (the same noise
    realisation drives K=0 and K=256).  Deterministic: same seed -> same bytes.
    """
    ss = np.random.SeedSequence([int(seed), int(sigma_I)])
    rng = np.random.default_rng(ss)
    drive = np.clip(np.round(rng.normal(80.0, float(sigma_I), size=N)), CLIP_LO, CLIP_HI)
    drive = drive.astype(np.int32)
    m0 = rng.integers(0, 256, size=N).astype(np.int32)
    jit = rng.integers(-1, 2, size=(T, N)).astype(np.int32)
    return drive, m0, jit


def simulate(K_int, drive, m0, jit, N, T, window):
    """One run.  Returns R (window mean), R_final, spike rate, flip rate,
    population period, R_m, degenerate flag."""
    m = m0.copy()
    last = np.zeros(N, dtype=np.int64)
    prev = np.zeros(N, dtype=np.int64)
    nfire = np.zeros(N, dtype=np.int64)
    s_prev = np.zeros(N, dtype=bool)
    F = 0
    Rsum = 0.0
    Rn = 0
    R_final = float("nan")
    spikes_win = 0
    flips_win = 0
    start = T - window
    for t in range(1, T + 1):
        kick = (K_int * F) // N
        acc = ((m * LEAK) >> 8) + drive + kick + jit[t - 1]
        s = acc >= 256
        m = acc & 0xFF
        f = s ^ s_prev
        F = int(f.sum())
        idx = np.flatnonzero(s)
        if idx.size:
            prev[idx] = last[idx]
            last[idx] = t
            nfire[idx] += 1
        if t > start:
            spikes_win += int(idx.size)
            flips_win += F
            # phase estimate from the last two carry times
            per = last - prev
            valid = (nfire >= 2) & (per > 0) & ((t - last) <= 3 * per)
            nv = int(valid.sum())
            if nv >= N // 2:
                th = 2.0 * np.pi * (t - last[valid]) / per[valid]
                Rt = abs(np.exp(1j * th).mean())
                Rsum += Rt
                Rn += 1
                R_final = Rt
        s_prev = s

    R = Rsum / Rn if Rn > 0 else float("nan")
    spike_rate = spikes_win / float(N * window)
    flip_rate = flips_win / float(N * window)
    # population period at the final tick (median ISI of included neurons)
    per = last - prev
    valid = (nfire >= 2) & (per > 0) & ((T - last) <= 3 * per)
    pop_period = float(np.median(per[valid])) if int(valid.sum()) else float("nan")
    R_m = float(abs(np.exp(2j * np.pi * m / 256.0).mean()))
    return {
        "R": float(R),
        "R_final": float(R_final),
        "spike_rate": float(spike_rate),
        "flip_rate": float(flip_rate),
        "pop_period": pop_period,
        "R_m": R_m,
        "degenerate": bool(spike_rate >= DEGENERATE_RATE),
        "n_valid_phase": int(valid.sum()),
    }


def interp_K(Ks, Rs, level):
    """First upward crossing of `level` on the (Ks, Rs) curve, linear in K."""
    for i in range(1, len(Ks)):
        y0, y1 = Rs[i - 1], Rs[i]
        if not (np.isfinite(y0) and np.isfinite(y1)):
            continue
        if y0 < level <= y1:
            if y1 == y0:
                return float(Ks[i])
            return float(Ks[i - 1] + (level - y0) * (Ks[i] - Ks[i - 1]) / (y1 - y0))
    return None


def sweep(sigma_I, seeds, N, T, window, rows):
    """Full 33-point K sweep for each seed at one sigma_I.  Returns per-seed curves."""
    curves = {}
    for seed in seeds:
        drive, m0, jit = make_inputs(N, T, sigma_I, seed)
        Rs = []
        for K_int in KS:
            t0 = time.time()
            r = simulate(K_int, drive, m0, jit, N, T, window)
            la, mem = box_row()
            rows.append({
                "sigma_I": sigma_I,
                "seed": seed,
                "K_int": int(K_int),
                "R": r["R"],
                "R_final": r["R_final"],
                "spike_rate": r["spike_rate"],
                "flip_rate": r["flip_rate"],
                "pop_period": r["pop_period"],
                "R_m": r["R_m"],
                "degenerate": r["degenerate"],
                "n_valid_phase": r["n_valid_phase"],
                "loadavg_1_5_15": la,
                "MemAvailable_kB": mem,
                "wall_s": time.time() - t0,
            })
            Rs.append(r["R"])
        curves[seed] = Rs
    return curves


def curve_stats(curves, seeds, label):
    """K_c per seed, 5-seed CV, pooled curve, sharpness, R(0), R(192)."""
    Kc = [interp_K(KS, curves[s], 0.5) for s in seeds]
    Kc_ok = [k for k in Kc if k is not None]
    mean = float(np.mean(Kc_ok)) if Kc_ok else None
    std = float(np.std(Kc_ok, ddof=1)) if len(Kc_ok) > 1 else 0.0
    cv = (std / mean) if (mean and mean > 0) else None

    pooled = list(np.nanmean(np.array([curves[s] for s in seeds], dtype=float), axis=0))
    Kc_pooled = interp_K(KS, pooled, 0.5)
    K025 = interp_K(KS, pooled, 0.25)
    K075 = interp_K(KS, pooled, 0.75)
    sharp = None
    if Kc_pooled is not None and K025 is not None and K075 is not None and K075 > K025:
        sharp = Kc_pooled / (K075 - K025)
    per_seed_sharp = []
    for s in seeds:
        a = interp_K(KS, curves[s], 0.25)
        b = interp_K(KS, curves[s], 0.75)
        c = interp_K(KS, curves[s], 0.5)
        if a is not None and b is not None and c is not None and b > a:
            per_seed_sharp.append(c / (b - a))
    R0 = [curves[s][KS.index(0)] for s in seeds]
    R192 = [curves[s][KS.index(192)] for s in seeds]
    return {
        "label": label,
        "sigma_I": None,
        "Kc_per_seed": Kc,
        "Kc_mean": mean,
        "Kc_std": std,
        "Kc_cv": cv,
        "Kc_pooled_curve": Kc_pooled,
        "K_025_pooled": K025,
        "K_075_pooled": K075,
        "sharpness_pooled": sharp,
        "sharpness_per_seed_mean": float(np.mean(per_seed_sharp)) if per_seed_sharp else None,
        "sharpness_per_seed": per_seed_sharp,
        "R_at_0_per_seed": R0,
        "R_at_0_mean": float(np.mean(R0)),
        "R_at_192_per_seed": R192,
        "R_at_192_mean": float(np.mean(R192)),
        "pooled_curve": pooled,
    }


def stats_at(curves, seeds, K_int):
    i = KS.index(K_int)
    R = [curves[s][i] for s in seeds]
    return {"K_int": K_int, "R_mean": float(np.mean(R)), "R_per_seed": R}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="c2_kidA_results.json")
    ap.add_argument("--sigmas", default="10,5,20")
    ap.add_argument("--seeds", default="0,1,2,3,4")
    ap.add_argument("--N", type=int, default=N)
    ap.add_argument("--T", type=int, default=T)
    ap.add_argument("--window", type=int, default=WINDOW)
    args = ap.parse_args()

    try:
        import os as _os
        for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
            _os.environ.setdefault(v, str(N_THREADS))
    except Exception:
        pass

    sigmas = [int(x) for x in args.sigmas.split(",")]
    seeds = [int(x) for x in args.seeds.split(",")]
    n_osc, t_ticks, window = args.N, args.T, args.window
    t_start = time.time()
    la0, mem0 = box_row()

    rows = []
    per_sigma = {}
    for si in sigmas:
        curves = sweep(si, seeds, n_osc, t_ticks, window, rows)
        st = curve_stats(curves, seeds, "sigma_I=%d" % si)
        st["sigma_I"] = si
        st["R_at_192"] = stats_at(curves, seeds, 192)
        per_sigma[si] = (curves, st)

    # mean spike rate at K_int=192 from the raw rows (independent of curve arrays)
    for si in sigmas:
        rs = [r["spike_rate"] for r in rows if r["sigma_I"] == si and r["K_int"] == 192]
        per_sigma[si][1]["spike_rate_at_192_mean"] = float(np.mean(rs))
        rr = [r["pop_period"] for r in rows if r["sigma_I"] == si and r["K_int"] == 192]
        per_sigma[si][1]["pop_period_at_192_median"] = float(np.nanmedian(rr))
        r0 = [r["spike_rate"] for r in rows if r["sigma_I"] == si and r["K_int"] == 0]
        per_sigma[si][1]["spike_rate_at_0_mean"] = float(np.mean(r0))

    main_si = 10 if 10 in sigmas else sigmas[0]
    st = per_sigma[main_si][1]

    wall = time.time() - t_start
    la1, mem1 = box_row()

    claim = {
        "R_0_le_0.125": bool(st["R_at_0_mean"] <= 0.125),
        "R_0_mean": st["R_at_0_mean"],
        "Kc_cv_le_0.05": bool(st["Kc_cv"] is not None and st["Kc_cv"] <= 0.05),
        "Kc_cv": st["Kc_cv"],
        "sharpness_ge_2": bool(st["sharpness_pooled"] is not None and st["sharpness_pooled"] >= 2.0),
        "sharpness_pooled": st["sharpness_pooled"],
        "R_192_ge_0.9": bool(st["R_at_192_mean"] >= 0.9),
        "R_192_ge_0.9_per_seed": [bool(x >= 0.9) for x in st["R_at_192_per_seed"]],
        "rate_192_le_0.9": bool(st["spike_rate_at_192_mean"] <= 0.9),
        "spike_rate_at_192_mean": st["spike_rate_at_192_mean"],
    }
    claim["all_conjuncts_hold"] = bool(
        claim["R_0_le_0.125"] and claim["Kc_cv_le_0.05"] and claim["sharpness_ge_2"]
        and claim["R_192_ge_0.9"] and claim["rate_192_le_0.9"])

    out = {
        "spec": {
            "N": n_osc, "T": t_ticks, "window": window, "KS": KS,
            "leak": "205/256=0.8008", "drive": "round(N(80,sigma)) clip [56,120]",
            "kick": "floor(K_int*F/N), F=popcount(flip vector)",
            "spike": "carry-out acc>=256, wrap", "flip": "s XOR s_prev",
            "order_parameter": ("theta_i=2pi(t-t_last)/(t_last-t_prev); excluded if "
                                "t-t_last>3*period or <2 fires; R undef if <N/2 remain"),
            "degenerate_rate": DEGENERATE_RATE,
            "threads": N_THREADS, "numpy": np.__version__,
        },
        "box": {
            "loadavg_1_5_15_at_start": la0,
            "MemAvailable_kB_at_start": mem0,
            "loadavg_1_5_15_at_end": la1,
            "MemAvailable_kB_at_end": mem1,
            "nproc": os.cpu_count(),
            "wall_s_total": wall,
        },
        "claim_sigma_I_%d" % main_si: claim,
        "per_sigma": {str(si): {
            k: v for k, v in per_sigma[si][1].items() if k != "pooled_curve"
        } for si in sigmas},
        "pooled_curve_sigma_I_%d" % main_si: per_sigma[main_si][1]["pooled_curve"],
        "rows": rows,
    }
    with open(args.out, "w") as fh:
        json.dump(out, fh, indent=1)

    print("wall_s_total=%.1f rows=%d" % (wall, len(rows)))
    print("sigma_I=%d:" % main_si)
    print("  R(0)=%.4f  Kc=%.2f CV=%.4f  sharp=%.3f  R(192)=%.4f  rate(192)=%.4f"
          % (st["R_at_0_mean"], st["Kc_mean"], st["Kc_cv"], st["sharpness_pooled"],
             st["R_at_192_mean"], st["spike_rate_at_192_mean"]))
    print("  Kc_per_seed=%s" % ["%.2f" % k for k in st["Kc_per_seed"]])
    print("  claim_all_conjuncts_hold=%s" % claim["all_conjuncts_hold"])
    for si in sigmas:
        s2 = per_sigma[si][1]
        print("  sigma=%d Kc=%.2f CV=%.4f R(0)=%.4f R(192)=%.4f"
              % (si, s2["Kc_mean"], s2["Kc_cv"], s2["R_at_0_mean"], s2["R_at_192_mean"]))
    print("  wrote %s" % args.out)


if __name__ == "__main__":
    main()
