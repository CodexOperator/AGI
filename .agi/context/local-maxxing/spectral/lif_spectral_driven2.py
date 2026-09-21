#!/usr/bin/env python3
"""CORRECTED driven spectral-snapshot LIF vs the C-driven reference (TM.58 re-run).

Builds on lif_spectral_driven.py read-only (PRNG/drive/init/ref-trains/stats).
Two fixes over the previous kid:
  FIX 1  at each snapshot boundary, after threshold+reset, re-project the
         post-reset membrane into the kept modes: vh = fft(v)[modes]. Without
         this the next window advances the PRE-reset state; the reset is lost.
  FIX 2  the coupling carries the C ring-gain: c_lag = raw per-lag mean of
         wgt(i,lag-1,seed); gsc = 0.9/(100*mean(c_lag)); lambda = gsc*DFT(c).
Validation at M=N,S=1: the FFT path must equal a direct neuron-space sim of the
same gsc-scaled circulant model (round-off); that sim must be within ~1 pct of
the C per-net reference (79675/4). Then the (M,S) sweep with acceptance:
within 5 pct on rate AND ISI KS(20-step bins) <= 0.05 AND within 5 pct on R.
Work bound reported two ways: product M*S <= 1000*4, and M<=1000 with S<=4.
"""
import importlib.util, json, os, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("lsd", os.path.join(HERE, "lif_spectral_driven.py"))
L = importlib.util.module_from_spec(spec); spec.loader.exec_module(L)
N, SYN, T, A, B, SEEDS, DT = L.N, L.SYN, L.T, L.A, L.B, L.SEEDS, L.DT
OUT = os.path.join(HERE, "rows_driven2.jsonl")
MS, SS = [8, 32, 128, 512, 1024, 2000, 4000, 8000, 10000], [1, 2, 4, 8, 16]
WORK_PRODUCT, WORK_M, WORK_S = 1000 * 4, 1000, 4
ENV = L.ENV


def lag_means(seed):
    i = np.arange(N, dtype=np.uint32); c = np.empty(SYN)
    for lag in range(1, SYN + 1):
        with np.errstate(over="ignore"):
            idx = i * np.uint32(97) + np.uint32(lag - 1) * np.uint32(3266489917) + np.uint32(seed)
        c[lag - 1] = float((L.prng(idx) & np.uint32(127)).mean()) / 1024.0
    return c


def modes_of(M):
    return np.concatenate([np.arange(M // 2), np.arange(-(M // 2), 0)])


def scaled_lambda(seed, modes):
    c = lag_means(seed); lag = np.arange(1, SYN + 1)
    gsc = 0.9 / (100.0 * c.mean())
    lam = (c[None, :] * np.exp(-2j * np.pi * modes[:, None] * lag[None, :] / N)).sum(1) * gsc
    return lam, gsc, c


def direct_net(seed, c, gsc):
    drive, v, spk, tr = L.drive_vec(seed), L.init_v(seed), np.zeros(N), []
    for t in range(T):
        I = np.zeros(N)
        for lag in range(1, SYN + 1):
            I += gsc * c[lag - 1] * np.roll(spk, lag)
        v1 = A * v + B * (I + drive[t]); f = v1 >= 1.0
        v = np.where(f, v1 - 1.0, v1); spk = f.astype(float)
        tr += [(t, int(i)) for i in np.nonzero(f)[0]]
    return tr


def spectral_net(seed, M, S, Xh, lam):
    modes = modes_of(M); aS, wts = A ** S, A ** np.arange(S - 1, -1, -1)
    Xm = Xh[:, modes]
    v = L.init_v(seed); vh = np.fft.fft(v)[modes]; spk = np.zeros(N); tr = []
    for w in range(T // S):
        sh = np.fft.fft(spk)[modes]
        xs = (Xm[w * S:w * S + S] * wts[:, None]).sum(0)
        vh = aS * vh + B * (lam * sh + xs)
        full = np.zeros(N, dtype=complex); full[modes] = vh
        v = np.fft.ifft(full).real
        f = v >= 1.0; v[f] -= 1.0
        vh = np.fft.fft(v)[modes]                      # FIX 1: carry post-reset state
        spk = f.astype(float)
        tr += [(w * S, int(i)) for i in np.nonzero(f)[0]]
    return tr


def rate_of(trains):
    return sum(len(x) for x in trains) / (len(trains) * N * T * DT / 1000.0)


def ref_acceptance(trains):
    counts = np.zeros((len(trains), T // 100), np.int64); active = np.zeros(len(trains), np.int64)
    for q, tr in enumerate(trains):
        byn = {}
        for t, i in tr:
            counts[q, t // 100] += 1; byn[i] = byn.get(i, 0) + 1
        active[q] = sum(1 for c in byn.values() if c >= 2)
    wrate = counts / (N * 100 * DT / 1000.0)
    return float(wrate.min()), float(active.mean() / N)


def main():
    trains, total, ref_wall = L.ref_trains()
    rate_ref = rate_of(trains)
    wmin, apct = ref_acceptance(trains)
    cdf20, isi_n = L.isi_cdf(trains, np.arange(0, T + 21, 20))
    cdf200, _ = L.isi_cdf(trains, np.arange(0, T + 201, 200))
    R_ref = L.pop_R(trains)
    print("REF", json.dumps({"spikes": total, "wall_s": round(ref_wall, 3), "rate": rate_ref,
                             "win_min": wmin, "active_pct": apct, "isi_n": isi_n, "R": R_ref}))
    print("REF_ACCEPT", json.dumps({"rate_in_5_20": 5.0 <= rate_ref <= 20.0,
                                    "win_min_ge_2": wmin >= 2.0, "active_ge_50pct": apct >= 0.5}))
    base = {"ts_utc": time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()), "env": ENV, "seeds": SEEDS,
            "workload": "lif N=10000 syn=100 dt=0.1 steps=1000 nets=4", "spikes": total,
            "wall_s": round(ref_wall, 3), "rate": rate_ref, "isi_n": isi_n, "R": R_ref}
    with open(OUT, "w") as f:
        f.write(json.dumps(dict(base, tool="cc-f64", isi_ks=None, within_5pct=None)) + "\n")

    # --- VALIDATION at M=N, S=1: FFT path vs direct sim of the same model ---
    for s in SEEDS:
        lam, gsc, c = scaled_lambda(s, modes_of(N))
        assert abs(gsc * 100.0 * c.mean() - 0.9) < 1e-12, "gsc*100*mean(c) != 0.9"
        Xh = np.fft.fft(L.drive_vec(s), axis=1)
        kf, kd = len(spectral_net(s, N, 1, Xh, lam)), len(direct_net(s, c, gsc))
        v = dict(base, tool="validation", seed=int(s), M=N, S=1, fft_spikes=kf,
                 direct_spikes=kd, diff=kf - kd, c_net_ref=total / 4.0,
                 direct_vs_c_pct=round(100.0 * abs(kd - total / 4.0) / (total / 4.0), 3),
                 gsc=round(gsc, 6), gsc_mean_check=round(gsc * 100.0 * c.mean(), 12))
        with open(OUT, "a") as f:
            f.write(json.dumps(v) + "\n")
        print("VALID", json.dumps({k: v[k] for k in ("seed", "fft_spikes", "direct_spikes",
              "diff", "c_net_ref", "direct_vs_c_pct", "gsc")}))

    # --- SWEEP ---
    passed, budget_passed = [], []
    for M in MS:
        for S in SS:
            t0 = time.perf_counter(); msp = []
            for s in SEEDS:
                lam, gsc, c = scaled_lambda(s, modes_of(M))
                msp.append(spectral_net(s, M, S, np.fft.fft(L.drive_vec(s), axis=1), lam))
            wall = time.perf_counter() - t0
            rate = rate_of(msp); R = L.pop_R(msp)
            mcdf20, _ = L.isi_cdf(msp, np.arange(0, T + 21, 20))
            mcdf200, _ = L.isi_cdf(msp, np.arange(0, T + 201, 200))
            ks20 = float(np.max(np.abs(mcdf20 - cdf20))) if sum(len(x) for x in msp) else None
            ks200 = float(np.max(np.abs(mcdf200 - cdf200))) if sum(len(x) for x in msp) else None
            ok = (abs(rate - rate_ref) <= 0.05 * rate_ref and ks20 is not None and ks20 <= 0.05
                  and abs(R - R_ref) <= 0.05 * R_ref)
            wp, wms = M * S <= WORK_PRODUCT, (M <= WORK_M and S <= WORK_S)
            row = dict(base, tool="numpy-spectral-driven2",
                       ts_utc=time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()), M=M, S=S,
                       wall_s=round(wall, 4), spikes=sum(len(x) for x in msp), rate=rate,
                       R=R, isi_ks=ks20, isi_ks_200step=ks200, within_5pct=ok,
                       within_work_product=wp, within_work_grid=wms)
            with open(OUT, "a") as f:
                f.write(json.dumps(row) + "\n")
            print("ROW", json.dumps({k: row[k] for k in ("M", "S", "wall_s", "spikes", "rate", "R",
                  "isi_ks", "isi_ks_200step", "within_5pct", "within_work_product", "within_work_grid")}))
            if ok:
                passed.append((M, S))
                if wp:
                    budget_passed.append((M, S))
    print("PASSED", json.dumps(passed))
    print("PASSED_WITHIN_PRODUCT_BOUND", json.dumps(budget_passed))
    print("rows:", OUT)


if __name__ == "__main__":
    main()
