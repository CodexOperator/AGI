#!/usr/bin/env python3
"""TM.61 event-driven sparse LIF vs the repaired C f64 reference (see node).
Arms: c (C + reporter), dense (correct-%N vectorised control), event-k/event-src
(lazy closed-form leak, k- vs source-ordered accumulation), event-steplk (event I,
leak on every neuron -> isolates the leak approximation). Env: poisson/sub/9.999/
gain 0.9/leak restore/order sync, N=10000 syn=100 dt=0.1 T=1000. CPU8G agi-run."""
import importlib.util as ilu, json, os, sys, time
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
def load(n, p):
    s = ilu.spec_from_file_location(n, p); m = ilu.module_from_spec(s); s.loader.exec_module(m); return m
L = load("lsd", os.path.join(HERE, "..", "spectral", "lif_spectral_driven.py"))
D = load("ld", os.path.join(HERE, "..", "bend", "lif_drive.py"))
N, K, T, DT, SEEDS = L.N, L.SYN, L.T, L.DT, L.SEEDS
R10, A, AMP, GAIN = 0.1, 0.9, 9.999, 0.9
OUT = os.path.join(HERE, "event_rows.jsonl"); KK, II = np.arange(K), np.arange(N)
def emit(r):
    j = json.dumps(r); open(OUT, "a").write(j + "\n"); print(j, flush=True)
def weights(seed):
    i = np.arange(N, dtype=np.uint32); k = np.arange(K, dtype=np.uint32)
    with np.errstate(over="ignore"):
        idx = i[:, None]*np.uint32(97) + k[None, :]*np.uint32(3266489917) + np.uint32(seed)
    return (L.prng(idx) & np.uint32(127)).astype(float)/1024.0
def gsc_of(W):  # C: gwant*N*K/(100*ws), ws = sequential row-major sum
    ws = float(np.cumsum(W.ravel())[-1]); return GAIN*N*K/(100.0*ws), ws
def stats(tr):
    na = len({i for _, i in tr})
    c = np.bincount([i for _, i in tr], minlength=N) if tr else np.zeros(N, np.int64)
    n2 = int((c >= 2).sum()); win = np.bincount([t for t, _ in tr], minlength=T)
    w = np.array([win[q*100:(q+1)*100].sum() for q in range(10)], float)/(N*0.01)
    return {"spikes": len(tr), "rate_hz": len(tr)/(N*T*DT/1000.0),
            "window_rates": [round(float(x), 4) for x in w], "R": round(float(L.pop_R([tr])), 6),
            "n_active": na, "n_active_ge2": n2, "isi_n": len(tr) - na}
def ev_net(seed, mode):
    W = weights(seed); gsc, ws = gsc_of(W); X = L.drive_vec(seed)
    v = L.init_v(seed).copy(); spk = np.zeros(N, bool); tl = np.full(N, -1, np.int64)
    tr, upd = [], 0
    for t in range(T):
        src = np.nonzero(spk)[0]; I = np.zeros(N); f = spk
        if not mode.startswith("event"):  # dense: C recurrence transcribed, sequential k
            for k2 in range(K): I += gsc*W[:, k2]*spk[(II - 1 - k2) % N]
        else:
            if len(src):
                sm = mode.endswith("src")
                tg = (src[:, None] + 1 + KK[None, :]) % N if sm else (src[None, :] + 1 + KK[:, None]) % N
                I = np.bincount(tg.ravel(), weights=(gsc*W[tg, KK[None, :] if sm else KK[:, None]]).ravel(),
                                minlength=N)
            tu = np.union1d(np.nonzero(I)[0], np.nonzero(X[t])[0]); upd += len(tu)
            if not mode.endswith("steplk"):
                gap = (t - tl[tu]).astype(float) - 1.0; vd = v[tu]*(A**gap)
                v1 = vd + R10*(((0.0 - vd) + I[tu]) + X[t][tu]); f1 = v1 >= 1.0
                v[tu] = np.where(f1, v1 - 1.0, v1); tl[tu] = t
                spk = np.zeros(N, bool); spk[tu[f1]] = True
                tr.extend(zip([t]*int(f1.sum()), tu[f1].tolist())); continue
        v1 = v + R10*(((0.0 - v) + I) + X[t]); f = v1 >= 1.0
        v = np.where(f, v1 - 1.0, v1); spk = f
        tr.extend(zip([t]*int(f.sum()), np.nonzero(f)[0].tolist()))
    return tr, upd, ws, gsc
def main():
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    ref, tot, ref_wall = L.ref_trains()
    print("C-REF", json.dumps({"spikes": tot, "wall_s": round(ref_wall, 3)}), flush=True)
    for q, s in enumerate(SEEDS):
        emit(dict(stats(ref[q]), arm="c-reference", tool="cc-f64", seed=int(s), wall_s=round(ref_wall, 3),
                  wall_4nets=round(ref_wall, 3), n_divergent_spikes=0, first_divergence=None,
                  neuron_updates=None))
    for arm in (["dense", "event-k", "event-src", "event-steplk"] if which == "all" else [which]):
        for q, s in enumerate(SEEDS):
            t0 = time.perf_counter(); tr, upd, ws, gsc = ev_net(s, arm); wall = time.perf_counter() - t0
            tset, rset = set(tr), set(ref[q]); d = sorted(tset ^ rset); st = stats(tr)
            st["rate_hz"] = round(st["rate_hz"], 4)
            emit(dict(st, arm=arm, tool="numpy-event", seed=int(s), wall_s=round(wall, 4), neuron_updates=upd,
                      updates_pct_NT=round(100.0*upd/(N*T), 4), gsc=round(gsc, 8), n_divergent_spikes=len(d),
                      first_divergence=(list(d[0]) if d else None), c_spikes=len(ref[q]),
                      n_missing=len(rset - tset), n_extra=len(tset - rset)))
    if which in ("all", "twin"):
        for s in SEEDS:
            t0 = time.perf_counter(); tot2, act, win = D.run_net(s, "poisson", AMP, "sub", 42, GAIN, "restore")
            emit(dict(arm="numpy-twin", tool="lif_drive.np_arm", seed=int(s), spikes=int(tot2),
                      wall_s=round(time.perf_counter() - t0, 4), neuron_updates=None))
if __name__ == "__main__":
    main()
