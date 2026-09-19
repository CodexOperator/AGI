#!/usr/bin/env python3
"""ARM4C NumPy reference of the spectral-snapshot LIF (hypothesis steps b+c).

Fixture identical to bend/lif_baseline.py: N=10000, syn=100, dt=0.1, 1000
steps, 4 seeded nets (7, 100010, 200013, 300016). Reference spike trains come
from lif_baseline.py's own C body with a per-spike dump appended, so the total
must reproduce the stock baseline's 19983.

SCHEME (concrete reading).  Below threshold the LIF step is linear:
v_{t+1} = a v_t + b(1 + W s_t), a=1-b=0.9, b=dt=0.1, s binary spikes, W the
ring coupling (lags 1..100).  Replacing W by its circulant mean (mean weight
per lag) diagonalises it with the DFT: mode m has complex coupling gain
lambda_m = sum_lag c_lag exp(-2 pi i m lag / N).  With the spike vector FROZEN
at the snapshot, the exact sub-threshold evolution of each kept mode is
vh_m <- a^S vh_m + (1 - a^S)(onehat_m + lambda_m sh_m): gain plus a per-mode
complex (phase x gain) drive.  Threshold and reset are re-inserted ONLY at the
snapshot boundary.  M low modes kept (symmetric).
"""
import importlib.util, json, os, subprocess, time
import numpy as np

N, SYN, T, DT = 10000, 100, 1000, 0.1
A, B = 1.0 - DT, DT
SEEDS = [7, 100010, 200013, 300016]
MS, SS = [8, 32, 128], [1, 4, 16, 64]
HERE = os.path.dirname(os.path.abspath(__file__))
BEND = os.path.normpath(os.path.join(HERE, "..", "bend"))
BENCH = os.path.normpath(os.path.join(HERE, "..", "bench"))


def _load_baseline():
    spec = importlib.util.spec_from_file_location("lif_baseline", os.path.join(BEND, "lif_baseline.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _u32(x):
    return np.asarray(x, dtype=np.uint32)


def prng(x):
    with np.errstate(over="ignore"):
        x = _u32(x) ^ (_u32(x) << np.uint32(13))
        x = x ^ (x >> np.uint32(17))
        return x ^ (x << np.uint32(5))


def init_v(seed):
    return (prng(_u32(np.arange(N)) + np.uint32(seed)) & np.uint32(255)).astype(np.float64) / 195.0


def lambda_modes(seed, modes):
    i = _u32(np.arange(N))
    c = np.empty(SYN)
    for lag in range(1, SYN + 1):
        k = np.uint32(lag - 1)
        with np.errstate(over="ignore"):
            idx = i * np.uint32(97) + k * np.uint32(3266489917) + np.uint32(seed)
        c[lag - 1] = float((prng(idx) & np.uint32(127)).mean()) / 1024.0
    lag = np.arange(1, SYN + 1)
    return (c[None, :] * np.exp(-2j * np.pi * modes[:, None] * lag[None, :] / N)).sum(1)


def ref_trains():
    base = _load_baseline().C
    src_c = base.replace("total++; }", 'total++; printf("S %d %d %d\\n",q,i,t); }')
    src_c = src_c.replace('printf("%llu\\n", total);', 'fprintf(stderr,"TOTAL %llu\\n", total);')
    d = "/dev/shm/lifref"
    os.makedirs(d, exist_ok=True)
    src, exe = os.path.join(d, "r.c"), os.path.join(d, "r")
    open(src, "w").write(src_c)
    subprocess.run(["cc", "-O3", "-march=native", "-fopenmp", src, "-o", exe], check=True)
    t0 = time.perf_counter()
    out = subprocess.run([exe], capture_output=True, text=True,
                         env=dict(os.environ, OMP_NUM_THREADS="4"), check=True)
    wall = time.perf_counter() - t0
    trains = [[] for _ in SEEDS]
    for line in out.stdout.splitlines():
        if not line.strip():
            continue
        q, i, t = line.split()[1:]
        trains[int(q)].append((int(t), int(i)))
    return trains, int(out.stderr.strip().split()[-1]), wall


def spectral_net(seed, M, S):
    modes = np.concatenate([np.arange(M // 2), np.arange(-(M // 2), 0)])
    lam = lambda_modes(seed, modes)
    onehat = np.where(modes == 0, float(N), 0.0)
    v, spk, spikes = init_v(seed), np.zeros(N), []
    for w in range(T // S):
        sh = np.fft.fft(spk)[modes]
        vh = A ** S * np.fft.fft(v)[modes] + (1 - A ** S) * (onehat + lam * sh)
        full = np.zeros(N, dtype=complex)
        full[modes] = vh
        v = np.fft.ifft(full).real
        fired = v >= 1.0
        v[fired] -= 1.0
        spikes.extend((w * S, int(i)) for i in np.nonzero(fired)[0])
        spk = fired.astype(np.float64)
    return spikes


def stats(trains):
    isis, rs = [], []
    edges = np.arange(0, 1021, 20)
    for tr in trains:
        byn = {}
        for t, i in tr:
            byn.setdefault(i, []).append(t)
        for ts in byn.values():
            ts.sort()
            isis.extend(np.diff(ts).tolist())
        n, _ = np.histogram([t for t, _ in tr], bins=np.arange(T + 1))
        if n.mean() > 0:
            rs.append(n.var() / n.mean())
    hist, _ = np.histogram(isis, bins=edges)
    total = sum(len(tr) for tr in trains)
    return {"rate": total / (len(SEEDS) * N * T), "isi_cdf": np.cumsum(hist) / max(hist.sum(), 1),
            "isi_n": len(isis), "R": float(np.mean(rs)) if rs else 0.0, "spikes": total}


def main():
    trains, total, ref_wall = ref_trains()
    assert total == 19983, f"reference total {total} != stock baseline 19983"
    r = stats(trains)
    if r["isi_n"] == 0:
        print("NOTE reference has no repeated spikes (all at t=0/1): one-shot transient,"
              " ISI KS undefined on this fixture")
    load1, load15 = os.getloadavg()[:2]
    utc = time.strftime("%Y%m%dT%H%M%SZ", time.gmtime())
    wl = "lif N=10000 syn=100 dt=0.1 steps=1000 nets=4"
    rows = [{"ts_utc": utc, "label": "spectral-reference", "tool": "cc-f64", "workload": wl,
             "threads": 4, "wall_s": round(ref_wall, 3), "rate": r["rate"],
             "spikes": r["spikes"], "isi_n": r["isi_n"], "R": r["R"], "isi_ks": None,
             "one_shot_transient": r["isi_n"] == 0, "loadavg_1m": load1, "loadavg_15m": load15}]
    for M in MS:
        for S in SS:
            t0 = time.perf_counter()
            m = stats([spectral_net(s, M, S) for s in SEEDS])
            wall = time.perf_counter() - t0
            ks = None if r["isi_n"] == 0 else float(np.max(np.abs(m["isi_cdf"] - r["isi_cdf"])))
            within5 = (abs(m["rate"] - r["rate"]) <= 0.05 * r["rate"] and ks is not None
                       and ks <= 0.05 and abs(m["R"] - r["R"]) <= 0.05 * r["R"])
            load1, load15 = os.getloadavg()[:2]
            rows.append({"ts_utc": utc, "label": "spectral-snapshot", "tool": "numpy", "workload": wl,
                         "M": M, "S": S, "wall_s": round(wall, 4), "rate": m["rate"],
                         "spikes": m["spikes"], "isi_n": m["isi_n"], "R": m["R"], "isi_ks": ks,
                         "within_5pct": within5, "loadavg_1m": load1, "loadavg_15m": load15})
            print(json.dumps(rows[-1]))
    with open(os.path.join(HERE, "rows.jsonl"), "w") as f:
        f.write("".join(json.dumps(row) + "\n" for row in rows))
    os.makedirs(BENCH, exist_ok=True)
    with open(os.path.join(BENCH, utc + ".jsonl"), "a") as f:
        f.write("".join(json.dumps(row) + "\n" for row in rows))
    print("bench:", os.path.join(BENCH, utc + ".jsonl"))


if __name__ == "__main__":
    main()
