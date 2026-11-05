"""goal:g5.43 -- seeded codes at the INPUT of a deterministic 2-32-64 net, claimed on fresh seeds.

Closed rounds are IMPORTED, never edited: g537_line_orientation (generator), g539_joint_samples (task,
scorer, G's training and samplers, streams), g541_blend_race (Z's trainer, the IoU helper).

  python g543_code_inputs.py PARAMS OUT_JSON

Code arms: input = cue bits + a code; sigma 0; loss = min per-pixel BCE over the code draws of the step;
a sample = one code drawn from a recorded stream.
  Z<b>-ENUM  b code bits, all 2^b codes enumerated each step (Z3-ENUM = g5.41's Z)
  Z<b>-SAMP  b code bits, K = 8 codes drawn uniformly WITH replacement per target per step
  C3-SAMP    3 continuous N(0, 1) inputs, K = 8 draws per target per step
  MZ2        3 bits, ONE random code per target per step, plain BCE (no min): the Mz2 mutant
Gaussian arms (g539_joint_samples.train itself): G best-of-8, G64 best-of-64.
Reported per discrete arm: the fraction of its codes that win >= 1 target in the last `win_window` steps.
Mutants (leaf v2, 1dc81b4f4b): Mz1 = every latent arm with its latent frozen to ONE seeded draw per seed and cue;
Mz6 = Z6-ENUM sampled through (code mod 8); Mz2 = MZ2; M2 = the scorer.
Every eval draw = default_rng([seed, stream, arm, setting, cue]).
"""
import json
import sys

import numpy as np

import g537_line_orientation as G37
import g539_joint_samples as E
import g541_blend_race as R

VAL, TEST, M1_STREAM, M2_STREAM = E.VAL, E.TEST, E.M1_STREAM, E.M2_STREAM
ARM_IDS = {"G": 20, "G64": 21, "Z3-ENUM": 22, "Z3-SAMP": 23, "Z5-SAMP": 24, "C3-SAMP": 25, "Z6-ENUM": 26,
           "Z2-ENUM": 27, "Z4-ENUM": 28, "MZ2": 29, "TRUE": 30, "COIN": 31, "Z6-MOD8": 32}


def code_table(bits):
    """index c -> its bits, most significant first (bits = 3 gives g541_blend_race.CODES exactly)."""
    return np.array([[(c >> (bits - 1 - i)) & 1 for i in range(bits)] for c in range(2 ** bits)],
                    dtype=np.float64)


# ---------------------------------------------------------------- training
def train_code(net, x, t, arm, p, rng_batch, rng_code):
    """arm = {"kind": "enum" | "samp" | "cont" | "one", "dim": code width}. Returns (net, win set)."""
    m, v = R.adam_state(net)
    npx = t.shape[1]
    kind, dim = arm["kind"], arm["dim"]
    table = code_table(dim) if kind != "cont" else None
    k = p["k"]
    tr = p["train"]
    wins = set()
    for step in range(1, tr["steps"] + 1):
        idx = rng_batch.integers(0, len(x), size=tr["batch"])
        xb, tb = x[idx], t[idx]
        bsz = len(xb)
        if kind == "enum":
            ci = np.repeat(np.arange(len(table))[:, None], bsz, 1)
        elif kind == "samp":
            ci = rng_code.integers(0, len(table), size=(k, bsz))
        elif kind == "one":
            ci = rng_code.integers(0, len(table), size=(1, bsz))
        if kind == "cont":
            code = rng_code.normal(0.0, 1.0, size=(k, bsz, dim))
        else:
            code = table[ci]
        (w1, bb1), (w2, bb2) = net
        xin = np.concatenate([np.repeat(xb[None], code.shape[0], 0), code], 2)
        hk = xin @ w1 + bb1
        ak = np.maximum(hk, 0.0)
        lk = ak @ w2 + bb2
        bce = (np.logaddexp(0.0, lk) - tb[None] * lk).mean(2)
        pick = bce.argmin(0)
        r = np.arange(bsz)
        if kind != "cont" and step > tr["steps"] - p["win_window"]:
            wins.update(ci[pick, r].tolist())
        g = (R.sigmoid(lk[pick, r]) - tb) / (npx * bsz)
        a, hh, xi = ak[pick, r], hk[pick, r], xin[pick, r]
        gh = (g @ w2.T) * (hh > 0)
        R.adam_step(net, [[xi.T @ gh, gh.sum(0)], [a.T @ g, g.sum(0)]], m, v, step, tr["lr"])
    return net, wins


def sample_code(net, cue, n, arm, rng, fixed=False, mod=None):
    """fixed (Mz1, leaf v2): the latent frozen to ONE draw from rng, repeated n times.
    mod (Mz6, leaf v2): a uniform code index taken mod `mod` (at most `mod` distinct images)."""
    kind, dim = arm["kind"], arm["dim"]
    m = 1 if fixed else n
    if kind == "cont":
        code = rng.normal(0.0, 1.0, size=(m, dim))
    else:
        ci = rng.integers(0, 2 ** dim, size=m)
        code = code_table(dim)[ci % mod if mod else ci]
    code = np.repeat(code, n // m, 0)
    xin = np.concatenate([E.onehot(cue, n), code], 1)
    (w1, b1), (w2, b2) = net
    return ((np.maximum(xin @ w1 + b1, 0.0) @ w2 + b2) > 0).astype(np.float64)


# ---------------------------------------------------------------- scoring
def valid_mask(samples, cue, tmpl, tcls, iou_min):
    inter, union = R.iou_all(samples, tmpl)
    best = (inter / union).argmax(1)
    r = np.arange(len(samples))
    num, den = iou_min
    return (num * inter[r, best] >= den * union[r, best]) & np.isin(tcls[best], E.PAIRS[cue])


def score_cue(samples, cue, tmpl, tcls, iou_min):
    s = E.score(samples, cue, tmpl, tcls, iou_min)
    vm = valid_mask(samples, cue, tmpl, tcls, iou_min)
    s["distinct_valid"] = int(len({row.tobytes() for row in samples[vm].astype(np.uint8)}))
    return s


def cues(per_cue):
    out = E.score_cues([{k: c[k] for k in ("valid", "coverage", "score")} for c in per_cue])
    out["distinct_valid_min"] = min(c["distinct_valid"] for c in per_cue)
    out["distinct_valid_mean"] = sum(c["distinct_valid"] for c in per_cue) / len(per_cue)
    out["cues"] = per_cue
    return out


# ---------------------------------------------------------------- one seed
def run_seed(seed, p, tmpl, tcls):
    ss = np.random.SeedSequence(seed)
    r_data, r_init, r_batch, r_tnoise = [np.random.default_rng(s) for s in ss.spawn(4)]
    d, n_s, iou_min = p["data"], p["n_samples"], p["score"]["iou_min"]
    n = d["n_train"]
    cue = r_data.integers(0, 2, size=n)
    pick = r_data.integers(0, 2, size=n)
    y = np.array([E.PAIRS[c][q] for c, q in zip(cue, pick)])
    t, _ = G37.make_lines(r_data, n, d["side"], d["width"], 0.0, d["jitter_deg"], d["max_offset"], y=y)
    x = np.eye(2)[cue]
    init_state = r_init.bit_generator.state
    batch_seed, tnoise_seed = int(r_batch.integers(2 ** 63)), int(r_tnoise.integers(2 ** 63))

    def fresh(sizes):
        r_init.bit_generator.state = init_state  # the SAME init stream for every arm (matched)
        return E.init_net(r_init, sizes)

    def evals(sampler, arm, si):
        return {st: cues([score_cue(sampler(c, E.rng_for(seed, sid, ARM_IDS[arm], si, c)), c, tmpl, tcls, iou_min)
                          for c in (0, 1)]) for st, sid in (("val", VAL), ("test", TEST))}

    out = {"seed": seed}
    for name, k, sigmas in (("G", p["k"], p["sigmas_g"]), ("G64", p["k64"], p["sigmas_g64"])):
        out[name] = {}
        for si, sg in enumerate(sigmas):
            net = E.train(fresh([2, 32, 64]), x, t, sg, k, p["train"], np.random.default_rng(batch_seed),
                          np.random.default_rng(tnoise_seed))
            out[name][str(sg)] = evals(lambda c, r: E.sample_p(net, c, sg, n_s, r), name, si)
    for name, arm in p["code_arms"].items():
        net, wins = train_code(fresh([2 + arm["dim"], 32, 64]), x, t, arm, p,
                               np.random.default_rng(batch_seed), np.random.default_rng(tnoise_seed))
        cell = evals(lambda c, r: sample_code(net, c, n_s, arm, r), name, 0)
        cell["mz1_fixed"] = cues([score_cue(sample_code(net, c, n_s, arm, E.rng_for(seed, M1_STREAM, ARM_IDS[name], 0, c),
                                                    fixed=True), c, tmpl, tcls, iou_min) for c in (0, 1)])
        if name == "Z6-ENUM":  # Mz6: the instrument mutant, sampled through (code mod 8)
            cell["mz6_mod8"] = evals(lambda c, r: sample_code(net, c, n_s, arm, r, mod=8), "Z6-MOD8", 0)["test"]
        if arm["kind"] != "cont":
            cell["win_fraction"] = len(wins) / 2 ** arm["dim"]
        cell["n_params"] = G37.n_params(net)
        out[name] = cell
    true_c, coin_c = [], []
    for c in (0, 1):
        r = E.rng_for(seed, M2_STREAM, ARM_IDS["TRUE"], 0, c)
        yy = np.repeat(np.array(E.PAIRS[c]), n_s // 2)
        lines, _ = G37.make_lines(r, n_s, d["side"], d["width"], 0.0, d["jitter_deg"], d["max_offset"], y=yy)
        true_c.append(E.score(lines, c, tmpl, tcls, iou_min))
        coin = (E.rng_for(seed, M2_STREAM, ARM_IDS["COIN"], 0, c).random(size=(n_s, d["side"] ** 2)) < 0.5)
        coin_c.append(E.score(coin.astype(np.float64), c, tmpl, tcls, iou_min))
    out["M2_true"], out["M2_coin"] = E.score_cues(true_c), E.score_cues(coin_c)
    return out


def main(argv):
    p = json.load(open(argv[1]))
    tmpl, tcls = E.templates(p)
    res = {"leaf": "goal:g5.43", "numpy": np.__version__, "params": p,
           "seeds": [run_seed(s, p, tmpl, tcls) for s in p["seeds"]]}
    with open(argv[2], "w") as f:
        json.dump(res, f, indent=1, sort_keys=True)
        f.write("\n")


if __name__ == "__main__":
    main(sys.argv)
