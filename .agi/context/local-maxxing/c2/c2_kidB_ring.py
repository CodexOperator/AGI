#!/usr/bin/env python3
"""C2 Kid B (owner's nearest-flip wiring) — digital Kuramoto in flip mode.

Independent implementation of the byte-neuron from the CLAIM section of
hypothesis:c2-digital-kuramoto-flip-mode.  Compares FIVE coupling topologies
in ONE script so they share seeds, draws and the K grid:

  all_flip  : kick_i = floor(K_int * F[t-1] / N),  F = popcount(f)   [Kid A reference]
  ring8     : kick_i = floor(K_int * popcount(byte_i[t-1]) / 8),
              byte_i = flip bits of ring neighbours i+-1..i+-4       [the claim]
  ring4     : same with i+-1..i+-2   (4 neighbours, /4)
  ring2     : same with i+-1         (2 neighbours, /2)
  spike     : all-flip mean field but using s in place of f          [control]

Byte-neuron:  m uint8; m <- ((m*205)>>8) + I_i + kick_i + n_i
  spike s = carry-out (acc >= 256); reset = wrap (acc & 0xFF)
  flip f = s XOR s[t-1];  n_i uniform {-1,0,+1}
  I_i = round(N(80, sigma_I)) clipped [56,120]
Order parameter: theta_i = 2*pi*(t-t_last)/(t_last-t_prev), exclude if
  t-t_last > 3*period or <2 fires; R undefined if <N/2 remain; window
  mean rate >= 0.98 is the degenerate all-fire state.

Claim (Kid B): K_c(ring8) reproduces K_c(all_flip) within 10% on the same
seeds/grid and R(192) >= 0.9 on the ring.

Run:  ~/.venv-lm/bin/python c2_kidB_ring.py --out c2_kidB_results.json
"""
import argparse
import json
import os
import time

import numpy as np

N = 256
T = 4096
WINDOW = 2048
KS = list(range(0, 257, 8))
LEAK = 205
CLIP_LO, CLIP_HI = 56, 120
DEGENERATE_RATE = 0.98
N_THREADS = 4
TOPO = ["all_flip", "ring8", "ring4", "ring2", "spike"]
RING_WIDTH = {"ring2": 2, "ring4": 4, "ring8": 8}


def box_row():
    la = [float(x) for x in open("/proc/loadavg").read().split()[:3]]
    mem = None
    with open("/proc/meminfo") as fh:
        for line in fh:
            if line.startswith("MemAvailable:"):
                mem = int(line.split()[1])
                break
    return la, mem


def ring_index(width, N):
    """(N, width) index matrix of the nearest neighbours on a ring."""
    half = width // 2
    offs = []
    for k in range(1, half + 1):
        offs += [k, -k]
    return (np.arange(N)[:, None] + np.array(offs)[None, :]) % N


def make_inputs(N, T, sigma_I, seed):
    """Draws once per (seed, sigma) and reused across K and topology (paired)."""
    rng = np.random.default_rng(np.random.SeedSequence([int(seed), int(sigma_I)]))
    drive = np.clip(np.round(rng.normal(80.0, float(sigma_I), size=N)), CLIP_LO, CLIP_HI).astype(np.int32)
    m0 = rng.integers(0, 256, size=N).astype(np.int32)
    jit = rng.integers(-1, 2, size=(T, N)).astype(np.int32)
    return drive, m0, jit


def simulate(topo, K_int, drive, m0, jit, N, T, window):
    """One run of one topology.  kick is computed from the PREVIOUS tick's
    source vector (flip for all_flip/ring*, spike for spike mode)."""
    m = m0.copy()
    last = np.zeros(N, dtype=np.int64)
    prev = np.zeros(N, dtype=np.int64)
    nfire = np.zeros(N, dtype=np.int64)
    s_prev = np.zeros(N, dtype=bool)
    f_prev = np.zeros(N, dtype=bool)
    ring = ring_index(RING_WIDTH[topo], N) if topo in RING_WIDTH else None

    Rsum = 0.0
    Rn = 0
    spikes_win = 0
    start = T - window
    for t in range(1, T + 1):
        if topo == "all_flip" or topo == "spike":
            src_prev = s_prev if topo == "spike" else f_prev
            kick = (K_int * int(src_prev.sum())) // N
        else:
            w = RING_WIDTH[topo]
            cnt = f_prev[ring].sum(axis=1)
            kick = (K_int * cnt) // w
        acc = ((m * LEAK) >> 8) + drive + kick + jit[t - 1]
        s = acc >= 256
        m = acc & 0xFF
        f = s ^ s_prev
        idx = np.flatnonzero(s)
        if idx.size:
            prev[idx] = last[idx]
            last[idx] = t
            nfire[idx] += 1
        if t > start:
            spikes_win += int(idx.size)
            per = last - prev
            valid = (nfire >= 2) & (per > 0) & ((t - last) <= 3 * per)
            if int(valid.sum()) >= N // 2:
                th = 2.0 * np.pi * (t - last[valid]) / per[valid]
                Rsum += abs(np.exp(1j * th).mean())
                Rn += 1
        s_prev = s
        f_prev = f

    R = Rsum / Rn if Rn > 0 else float("nan")
    rate = spikes_win / float(N * window)
    per = last - prev
    valid = (nfire >= 2) & (per > 0) & ((T - last) <= 3 * per)
    return {
        "R": float(R),
        "spike_rate": float(rate),
        "pop_period": float(np.median(per[valid])) if int(valid.sum()) else float("nan"),
        "degenerate": bool(rate >= DEGENERATE_RATE),
    }


def interp_K(Rs, level):
    for i in range(1, len(KS)):
        y0, y1 = Rs[i - 1], Rs[i]
        if not (np.isfinite(y0) and np.isfinite(y1)):
            continue
        if y0 < level <= y1:
            if y1 == y0:
                return float(KS[i])
            return float(KS[i - 1] + (level - y0) * (KS[i] - KS[i - 1]) / (y1 - y0))
    return None


def summarize(curves, seeds):
    kc = [interp_K(curves[s], 0.5) for s in seeds]
    ok = [k for k in kc if k is not None]
    mean = float(np.mean(ok)) if ok else None
    std = float(np.std(ok, ddof=1)) if len(ok) > 1 else 0.0
    pooled = list(np.nanmean(np.array([curves[s] for s in seeds], dtype=float), axis=0))
    i192 = KS.index(192)
    r192 = [float(curves[s][i192]) for s in seeds]
    i0 = KS.index(0)
    return {
        "Kc_per_seed": kc,
        "Kc_mean": mean,
        "Kc_std": std,
        "Kc_cv": (std / mean) if (mean and mean > 0) else None,
        "Kc_pooled": interp_K(pooled, 0.5),
        "R_at_0_mean": float(np.mean([curves[s][i0] for s in seeds])),
        "R_at_192_per_seed": r192,
        "R_at_192_mean": float(np.mean(r192)),
        "pooled_curve": pooled,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="c2_kidB_results.json")
    ap.add_argument("--sigma", type=int, default=10)
    ap.add_argument("--seeds", default="0,1,2,3,4")
    ap.add_argument("--N", type=int, default=N)
    ap.add_argument("--T", type=int, default=T)
    ap.add_argument("--window", type=int, default=WINDOW)
    ap.add_argument("--topos", default=",".join(TOPO))
    args = ap.parse_args()

    for v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
        os.environ.setdefault(v, str(N_THREADS))

    seeds = [int(x) for x in args.seeds.split(",")]
    topos = args.topos.split(",")
    n_osc, t_ticks, window = args.N, args.T, args.window
    la0, mem0 = box_row()
    t_start = time.time()

    rows = []
    curves = {tp: {} for tp in topos}
    for seed in seeds:
        drive, m0, jit = make_inputs(n_osc, t_ticks, args.sigma, seed)
        for tp in topos:
            Rs = []
            for K_int in KS:
                r = simulate(tp, K_int, drive, m0, jit, n_osc, t_ticks, window)
                la, mem = box_row()
                rows.append({
                    "topo": tp, "sigma_I": args.sigma, "seed": seed, "K_int": int(K_int),
                    "R": r["R"], "spike_rate": r["spike_rate"],
                    "pop_period": r["pop_period"], "degenerate": r["degenerate"],
                    "loadavg_1_5_15": la, "MemAvailable_kB": mem,
                })
                Rs.append(r["R"])
            curves[tp][seed] = Rs

    summary = {tp: summarize(curves[tp], seeds) for tp in topos}
    for tp in topos:
        i192 = KS.index(192)
        rates = [r["spike_rate"] for r in rows if r["topo"] == tp and r["K_int"] == 192]
        summary[tp]["spike_rate_at_192_mean"] = float(np.mean(rates))
        i0 = KS.index(0)
        rates0 = [r["spike_rate"] for r in rows if r["topo"] == tp and r["K_int"] == 0]
        summary[tp]["spike_rate_at_0_mean"] = float(np.mean(rates0))
        # plateau rate: mean spike rate over the last 8 K points (K 192..256)
        hiK = [r["spike_rate"] for r in rows if r["topo"] == tp and r["K_int"] >= 192]
        summary[tp]["plateau_rate_mean"] = float(np.mean(hiK))

    ref = summary.get("all_flip", {}).get("Kc_mean")
    ring8 = summary.get("ring8", {})
    ratio = (ring8.get("Kc_mean") / ref) if (ref and ring8.get("Kc_mean")) else None
    claim = {
        "K_c_all_flip": ref,
        "K_c_ring8": ring8.get("Kc_mean"),
        "Kc_ratio_ring8_over_allflip": ratio,
        "ring8_within_10pct": bool(ratio is not None and 0.9 <= ratio <= 1.1),
        "ring8_R_192_ge_0.9": bool(ring8.get("R_at_192_mean") is not None
                                    and ring8["R_at_192_mean"] >= 0.9),
        "ring8_R_192_per_seed": [bool(x >= 0.9) for x in ring8.get("R_at_192_per_seed", [])],
    }
    claim["all_conjuncts_hold"] = bool(
        claim["ring8_within_10pct"] and claim["ring8_R_192_ge_0.9"])

    wall = time.time() - t_start
    la1, mem1 = box_row()
    out = {
        "spec": {
            "N": n_osc, "T": t_ticks, "window": window, "KS": KS, "sigma_I": args.sigma,
            "seeds": seeds, "topos": topos, "leak": "205/256", "threads": N_THREADS,
            "numpy": np.__version__, "n_runs": len(rows),
            "ring_kick": "floor(K_int*popcount(byte_i)/width), byte_i = flip bits of i+-1..i+-width/2",
            "all_flip_kick": "floor(K_int*F/N), F=popcount(f)",
            "spike_control": "all-flip mean field using s in place of f",
        },
        "box": {
            "loadavg_1_5_15_at_start": la0, "MemAvailable_kB_at_start": mem0,
            "loadavg_1_5_15_at_end": la1, "MemAvailable_kB_at_end": mem1,
            "nproc": os.cpu_count(), "wall_s_total": wall,
        },
        "claim": claim,
        "summary": {tp: {k: v for k, v in summary[tp].items() if k != "pooled_curve"}
                    for tp in topos},
        "pooled_curves": {tp: summary[tp]["pooled_curve"] for tp in topos},
        "rows": rows,
    }
    with open(args.out, "w") as fh:
        json.dump(out, fh, indent=1)

    print("wall_s_total=%.1f runs=%d" % (wall, len(rows)))
    for tp in topos:
        s = summary[tp]
        print("  %-8s Kc=%.2f (pooled %.2f) CV=%.4f R(0)=%.4f R(192)=%.4f "
              "rate(192)=%.4f plateau=%.4f"
              % (tp, s["Kc_mean"] if s["Kc_mean"] is not None else float("nan"),
                 s["Kc_pooled"] if s["Kc_pooled"] is not None else float("nan"),
                 s["Kc_cv"] if s["Kc_cv"] is not None else float("nan"),
                 s["R_at_0_mean"], s["R_at_192_mean"],
                 s["spike_rate_at_192_mean"], s["plateau_rate_mean"]))
        print("           Kc_per_seed=%s" % ["%.1f" % k if k is not None else "none"
                                               for k in s["Kc_per_seed"]])
    print("  ratio ring8/all_flip=%s  within_10pct=%s  ring8 R(192)>=0.9=%s  ALL=%s"
          % (("%.4f" % ratio) if ratio is not None else "nan",
             claim["ring8_within_10pct"], claim["ring8_R_192_ge_0.9"],
             claim["all_conjuncts_hold"]))
    print("  wrote %s" % args.out)


if __name__ == "__main__":
    main()
