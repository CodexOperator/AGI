#!/usr/bin/env python3
"""Acceptance runner for the driven LIF fixture: bend/lif_baseline.py --drive (C)
x this NumPy twin, same recurrence v1 = v + 0.1*((1-v) + I + i_ext).
Usage: lif_drive.py --drive poisson|gol|none [--amp A] [--init orig|sub] [--gain G] [--leak restore] [--out F]
"""
import argparse, json, os, subprocess, sys, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
N, SYN, T = 10000, 100, 1000
DT_S, R10 = 1e-4, 0.1
SEEDS = [7, 100010, 200013, 300016]


def c_arm(drive, amp, init, gain=None, leak="up", order="sync"):
    env = dict(os.environ, LIF_DRIVE=drive, LIF_INIT=init, LIF_AMP=repr(amp), LIF_REPORT="1")
    if gain is not None: env["LIF_GAIN"] = repr(gain)
    if leak == "restore": env["LIF_LEAK"] = "restore"
    env["LIF_ORDER"] = order
    p = subprocess.run([sys.executable, os.path.join(HERE, "lif_baseline.py"), "4"],
                       capture_output=True, text=True, env=env, cwd=HERE, check=True)
    nets = [l.split() for l in p.stderr.splitlines() if l.startswith("NET")]
    total = json.loads(p.stdout.strip().splitlines()[-1])["spikes"]
    active = sum(int(l[1]) for l in nets)
    win = [sum(int(l[2 + w]) for l in nets) for w in range(10)]
    return total, active, np.array(win, dtype=float)


def prng(x):
    x = np.asarray(x, dtype=np.uint32)
    with np.errstate(over="ignore"):
        x = x ^ (x << np.uint32(13)); x = x ^ (x >> np.uint32(17))
        return x ^ (x << np.uint32(5))


def run_net(seed, drive, amp, init, dseed, gain=None, leak="up"):
    i = np.arange(N, dtype=np.uint32); k = np.arange(SYN, dtype=np.uint32)
    with np.errstate(over="ignore"):
        idx = i[:, None] * np.uint32(97) + k[None, :] * np.uint32(3266489917) + np.uint32(seed)
    w = (prng(idx) & np.uint32(127)).astype(float) / 1024.0
    if gain is not None:  # ring gain: 100 * mean weight == gain
        w = w * (gain / (100.0 * w.mean()))
    j = ((i[:, None] - np.uint32(1) - k[None, :]) % np.uint32(4 * N)).astype(int)
    v = (prng(i + np.uint32(seed)) & np.uint32(255)).astype(float) / (256.0 if init == "sub" else 195.0)
    b = (prng(i + np.uint32(dseed)) & np.uint32(1)).astype(np.uint8).reshape(100, 100)
    spk, tot, active, win = np.zeros(N), 0, np.zeros(N, bool), np.zeros(10, np.int64)
    thr = np.uint32(int(20.0 * DT_S * 1048576))
    for t in range(T):
        I = (w * spk[j]).sum(1)  # spk is the PREVIOUS step's array (Jacobi), same as C
        if drive == "poisson":
            u = prng(np.uint32(t) * np.uint32(2654435761) + i * np.uint32(97) + np.uint32(dseed)) & np.uint32(1048575)
            x = (u < thr).astype(float) * amp
        else:
            x = b.reshape(-1).astype(float) * amp if drive == "gol" else 0.0
        v1 = v + R10 * (((0.0 if leak == "restore" else 1.0) - v) + I + x); f = v1 >= 1.0
        v = np.where(f, v1 - 1.0, v1); spk = f.astype(float)
        tot += int(f.sum()); active |= f; win[t // 100] += int(f.sum())
        if drive == "gol" and (t + 1) % 100 == 0:
            nb = sum(np.roll(b, s) for s in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)])
            b = ((nb == 3) | ((b == 1) & (nb == 2))).astype(np.uint8)
    return tot, int(active.sum()), win


def np_arm(drive, amp, init, dseed=42, gain=None, leak="up"):
    r = [run_net(s, drive, amp, init, dseed, gain, leak) for s in SEEDS]
    return sum(x[0] for x in r), sum(x[1] for x in r), np.sum([x[2] for x in r], axis=0).astype(float)


def accept(total, active, win):
    rate = total / (4 * N * 0.1); wr = win / (4 * N * 0.01)
    return {"rate": rate, "wrate": [round(float(x), 3) for x in wr], "win_min": float(wr.min()),
            "isi_n": total - active, "R_defined": total > 0}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--drive", required=True, choices=["poisson", "gol", "none"])
    ap.add_argument("--amp", type=float, default=1.0)
    ap.add_argument("--init", default="orig")
    ap.add_argument("--gain", type=float, default=None)
    ap.add_argument("--leak", default="up", choices=["up", "restore"])
    ap.add_argument("--out", default=os.path.join(HERE, "lif_drive_rows.jsonl"))
    a = ap.parse_args()
    rows = []
    for tool, fn in (("cc-f64", c_arm), ("numpy-twin", np_arm)):
        t0 = time.perf_counter()
        total, active, win = fn(a.drive, a.amp, a.init, gain=a.gain, leak=a.leak)
        rows.append({"ts_utc": time.strftime("%Y%m%dT%H%M%SZ", time.gmtime()), "arm": a.drive,
                     "tool": tool, "amp": a.amp, "init": a.init, "gain": a.gain, "leak": a.leak,
                     "seeds": SEEDS,
                     "workload": "lif N=10000 syn=100 dt=0.1 steps=1000 nets=4",
                     "wall_s": round(time.perf_counter() - t0, 3), "spikes": total,
                     **accept(total, active, win)})
    with open(a.out, "a") as f:
        f.write("".join(json.dumps(r) + "\n" for r in rows))
    for r in rows:
        print(json.dumps(r))


if __name__ == "__main__":
    main()
