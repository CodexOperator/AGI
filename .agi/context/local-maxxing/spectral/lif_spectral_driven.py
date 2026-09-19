#!/usr/bin/env python3
"""Driven spectral-snapshot LIF vs the C-driven reference (TM.58, hypothesis b).

Fixture: N=10000, syn=100 ring, dt=0.1 ms, 1000 steps, 4 seeds; env
LIF_DRIVE=poisson LIF_INIT=sub LIF_AMP=9.999 LIF_GAIN=0.9 LIF_LEAK=restore
LIF_ORDER=sync. Reference trains are lif_baseline.py's own C body with a
per-spike printf appended.

Sub-threshold recurrence (leak restore => rest=0): v_{t+1} = a v_t + b(I_t + x_t),
a=0.9, b=0.1.  Circulant-mean coupling c_lag (lags 1..100) diagonalises under the
DFT with lambda_m = gsc * sum_lag c_lag exp(-2 pi i m lag/N); the drive x_t is
state-independent and enters exactly.  With spikes frozen for S steps:
  vh_m <- a^S vh_m + b * sum_{j<S} a^{S-1-j} (lambda_m sh_m + xhat_m(t+j))
M symmetric low modes kept; threshold+reset only at snapshot boundaries.
"""
import importlib.util, json, os, subprocess, time
import numpy as np

N, SYN, T, DT = 10000, 100, 1000, 0.1
A, B = 1.0 - DT, DT
SEEDS = [7, 100010, 200013, 300016]
MS, SS = [8, 32, 128, 512, 2048, 8192, 10000], [1, 4, 16, 64]
ENV = dict(LIF_DRIVE="poisson", LIF_INIT="sub", LIF_AMP="9.999", LIF_GAIN="0.9",
           LIF_LEAK="restore", LIF_ORDER="sync")
HERE = os.path.dirname(os.path.abspath(__file__))
BEND = os.path.normpath(os.path.join(HERE, "..", "bend"))


def prng(x):
    x = np.asarray(x, dtype=np.uint32)
    with np.errstate(over="ignore"):
        x = x ^ (x << np.uint32(13)); x = x ^ (x >> np.uint32(17))
        return x ^ (x << np.uint32(5))


def init_v(seed):
    i = np.arange(N, dtype=np.uint32)
    return (prng(i + np.uint32(seed)) & np.uint32(255)).astype(float) / 256.0


def lambda_modes(seed, modes):
    i = np.arange(N, dtype=np.uint32)
    c = np.empty(SYN)
    for lag in range(1, SYN + 1):
        with np.errstate(over="ignore"):
            idx = i * np.uint32(97) + np.uint32(lag - 1) * np.uint32(3266489917) + np.uint32(seed)
        c[lag - 1] = float((prng(idx) & np.uint32(127)).mean()) / 1024.0
    lag = np.arange(1, SYN + 1)
    return (c[None, :] * np.exp(-2j * np.pi * modes[:, None] * lag[None, :] / N)).sum(1)


def drive_vec(seed):
    t = np.arange(T, dtype=np.uint32)[:, None] * np.uint32(2654435761)
    i = np.arange(N, dtype=np.uint32)[None, :] * np.uint32(97)
    with np.errstate(over="ignore"):
        u = prng(t + i + np.uint32(seed)) & np.uint32(1048575)
    return (u < 2097) * 9.999


def ref_trains():
    spec = importlib.util.spec_from_file_location("lif_baseline", os.path.join(BEND, "lif_baseline.py"))
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    src = mod.C.replace("if(fired){ v[i]=v1-ONE; total++; }",
                        'if(fired){ v[i]=v1-ONE; total++; printf("S %d %d %d\\n",q,i,t); }')
    src = src.replace('printf("%llu\\n", total);', 'fprintf(stderr,"TOTAL %llu\\n", total);')
    src_c, exe = "/tmp/tm58drv.c", "/tmp/tm58drv"
    open(src_c, "w").write(src)
    subprocess.run(["cc", "-O3", "-march=native", "-fopenmp", src_c, "-o", exe], check=True)
    t0 = time.perf_counter()
    out = subprocess.run([exe], capture_output=True, text=True, check=True,
                         env=dict(os.environ, OMP_NUM_THREADS="4", **ENV))
    wall = time.perf_counter() - t0
    trains = [[] for _ in SEEDS]
    for line in out.stdout.splitlines():
        if line.strip():
            q, i, t = line.split()[1:]
            trains[int(q)].append((int(t), int(i)))
    return trains, int(out.stderr.strip().split()[-1]), wall


def isi_cdf(trains, edges):
    isis = []
    for tr in trains:
        byn = {}
        for t, i in tr:
            byn.setdefault(i, []).append(t)
        for ts in byn.values():
            ts.sort(); isis.extend(np.diff(ts))
    h, _ = np.histogram(isis, bins=edges)
    return np.cumsum(h) / max(h.sum(), 1), len(isis)


def pop_R(trains):
    rs = []
    for tr in trains:
        n = np.bincount([t for t, _ in tr], minlength=T)
        if n.mean() > 0:
            rs.append(n.var() / n.mean())
    return float(np.mean(rs)) if rs else 0.0


def spectral_net(seed, M, S, Xh):
    modes = np.concatenate([np.arange(M // 2), np.arange(-(M // 2), 0)])
    lam, aS = lambda_modes(seed, modes), A ** S
    wts = A ** np.arange(S - 1, -1, -1)
    Xm = Xh[:, modes]
    v = init_v(seed); vh = np.fft.fft(v)[modes]; spk = np.zeros(N); spikes = []
    for w in range(T // S):
        sh = np.fft.fft(spk)[modes]
        xs = (Xm[w * S:w * S + S] * wts[:, None]).sum(0)
        vh = aS * vh + B * (lam * sh + xs)
        full = np.zeros(N, dtype=complex); full[modes] = vh
        v = np.fft.ifft(full).real
        fired = v >= 1.0; v[fired] -= 1.0
        spikes.extend(zip([w * S] * int(fired.sum()), np.nonzero(fired)[0].tolist()))
        spk = fired.astype(float)
    return spikes


def main():
    out_path = os.path.join(HERE, "rows_driven.jsonl")
    trains, total, ref_wall = ref_trains()
    rate = total / (4 * N * T * DT / 1000.0)
    counts = np.zeros((4, T // 100), np.int64); active = np.zeros(4, np.int64)
    for q, tr in enumerate(trains):
        byn = {}
        for t, i in tr:
            counts[q, t // 100] += 1; byn[i] = byn.get(i, 0) + 1
        active[q] = sum(1 for c in byn.values() if c >= 2)
    wrate = counts / (N * 100 * DT / 1000.0)
    cdf20, isi_n = isi_cdf(trains, np.arange(0, T + 21, 20))
    cdf200, _ = isi_cdf(trains, np.arange(0, T + 201, 200))
    r_ref = pop_R(trains)
    acc = {"rate": rate, "win_min": float(wrate.min()), "active_pct": float(active.mean() / N),
           "isi_n": isi_n, "R": r_ref}
    print("REF", json.dumps({"spikes": total, "ref_wall_s": round(ref_wall, 3),
                             "win_rate_min": round(acc["win_min"], 3),
                             "active_pct": round(acc["active_pct"], 3), **acc}))
    base = {"ts_utc": time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()), "tool": "cc-f64",
            "env": ENV, "seeds": SEEDS, "workload": "lif N=10000 syn=100 dt=0.1 steps=1000 nets=4",
            "spikes": total, "wall_s": round(ref_wall, 3), "rate": rate, "isi_n": isi_n,
            "R": r_ref, "isi_ks": None, "within_5pct": None}
    with open(out_path, "w") as f:
        f.write(json.dumps(base) + "\n")
    for M in MS:
        for S in SS:
            t0 = time.perf_counter(); msp = []
            for s in SEEDS:
                msp.append(spectral_net(s, M, S, np.fft.fft(drive_vec(s), axis=1)))
            wall = time.perf_counter() - t0
            m = {"spikes": sum(len(x) for x in msp)}
            m["rate"] = m["spikes"] / (4 * N * T * DT / 1000.0)
            m["R"] = pop_R(msp)
            mcdf20, m["isi_n"] = isi_cdf(msp, np.arange(0, T + 21, 20))
            mcdf200, _ = isi_cdf(msp, np.arange(0, T + 201, 200))
            ks20 = float(np.max(np.abs(mcdf20 - cdf20))) if isi_n else None
            ks200 = float(np.max(np.abs(mcdf200 - cdf200))) if isi_n else None
            ok = (abs(m["rate"] - rate) <= 0.05 * rate and ks20 is not None and ks20 <= 0.05
                  and abs(m["R"] - r_ref) <= 0.05 * abs(r_ref)) if r_ref else False
            row = dict(base, **{"ts_utc": time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()),
                                "tool": "numpy-spectral-driven", "M": M, "S": S,
                                "wall_s": round(wall, 4), "rate": m["rate"], "spikes": m["spikes"],
                                "isi_n": m["isi_n"], "R": m["R"], "isi_ks": ks20,
                                "isi_ks_200step": ks200, "within_5pct": ok})
            with open(out_path, "a") as f:
                f.write(json.dumps(row) + "\n")
            print("ROW", json.dumps({k: row[k] for k in
                                     ("M", "S", "wall_s", "rate", "spikes", "isi_n", "R", "isi_ks", "isi_ks_200step", "within_5pct")}))
    print("rows:", out_path)


if __name__ == "__main__":
    main()
