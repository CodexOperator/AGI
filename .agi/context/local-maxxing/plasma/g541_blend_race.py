"""goal:g5.41 -- g5.39's 21% validity raced between a topology fix (S, stochastic binary core) and a loss
fix (G-CHAMFER, a precision term), with a measured blend split (STEP 0) first.

Closed rounds are IMPORTED, never edited: g537_line_orientation (generator, geometry) and
g539_joint_samples (task, scorer, G's training, samplers, streams).

  python g541_blend_race.py step0 G539_PARAMS PARAMS OUT_JSON   STEP 0 on g5.39's bytes (P at sigma 2.0)
  python g541_blend_race.py run   PARAMS OUT_JSON          STEP 1, every arm

Arms (shared data / init / batch streams per seed; every eval draw = default_rng([seed, stream, arm, setting, cue])):
  G        g5.39's Gaussian core, best-of-K, trained by g539_joint_samples.train itself
  S        hidden unit j = 1 with prob sigmoid(h_j) else 0; best-of-K; straight-through gradient
           dL/dh = dL/da * sigmoid'(h)
  GC       G's core; loss = best-of-K recall + lam x precision, precision = mean over draws of the
           min per-pixel BCE to the batch's SAME-CUE targets (never the scorer's templates)
  SC, GP   reported: S + the same precision term; G with the precision term only
  Z        reported: 5-32-64, inputs = cue bits + 3 code bits, sigma 0, loss = min BCE over all 8 codes,
           a sample = one code drawn uniformly
  MF       reported: G(sigma*) at the hidden layer's Gaussian expectation
Mutants: M1-S (S, every unit frozen at its likelier state), M1-C (GC, one draw frozen per cue), M2 (scorer).
"""
import json
import math
import sys

import numpy as np

import g537_line_orientation as G37
import g539_joint_samples as E

VAL, TEST, M1_STREAM, M2_STREAM = E.VAL, E.TEST, E.M1_STREAM, E.M2_STREAM
ARM = {"G": 10, "S": 11, "GC": 12, "SC": 13, "GP": 14, "Z": 15, "TRUE": 16, "COIN": 17}
CODES = np.array([[(c >> 2) & 1, (c >> 1) & 1, c & 1] for c in range(8)], dtype=np.float64)


# ---------------------------------------------------------------- the blend split
def iou_all(samples, tmpl):
    inter = np.rint(samples @ tmpl.T).astype(np.int64)
    union = np.rint(samples.sum(1, keepdims=True) + tmpl.sum(1)[None]).astype(np.int64) - inter
    return inter, union


def split(samples, cue, tmpl, tcls, iou_min, blend_min, sparse_px):
    """every INVALID sample -> BLEND (IoU >= blend_min against a template of EACH class in the cue's
    pair), else SPARSE (fewer than sparse_px pixels on), else OTHER. Precedence in that order."""
    s = E.score(samples, cue, tmpl, tcls, iou_min)
    inter, union = iou_all(samples, tmpl)
    best = (inter / union).argmax(1)
    r = np.arange(len(samples))
    num, den = iou_min
    valid = (num * inter[r, best] >= den * union[r, best]) & np.isin(tcls[best], E.PAIRS[cue])
    bn, bd = blend_min
    reach = bn * inter >= bd * union  # (n, templates)
    blend = np.ones(len(samples), bool)
    for k in E.PAIRS[cue]:
        blend &= reach[:, tcls == k].any(1)
    inv = ~valid
    b = inv & blend
    sp = inv & ~blend & (samples.sum(1) < sparse_px)
    o = inv & ~blend & ~sp
    s.update({"n": int(len(samples)), "invalid": int(inv.sum()), "blend": int(b.sum()),
              "sparse": int(sp.sum()), "other": int(o.sum())})
    return s


def pooled(per_cue):
    out = E.score_cues([{k: c[k] for k in ("valid", "coverage", "score")} for c in per_cue])
    for k in ("n", "invalid", "blend", "sparse", "other"):
        out[k] = int(sum(c[k] for c in per_cue))
    out["blend_share"] = out["blend"] / out["invalid"] if out["invalid"] else 0.0
    out["cues"] = per_cue
    return out


def targets_and_sparse(seed, p):
    """g5.39's training targets for this seed, re-derived on its stream, and the SPARSE line."""
    ss = np.random.SeedSequence(seed)
    r_data = np.random.default_rng(ss.spawn(4)[0])
    d, n = p["data"], p["data"]["n_train"]
    cue = r_data.integers(0, 2, size=n)
    pick = r_data.integers(0, 2, size=n)
    y = np.array([E.PAIRS[c][q] for c, q in zip(cue, pick)])
    t, _ = G37.make_lines(r_data, n, d["side"], d["width"], 0.0, d["jitter_deg"], d["max_offset"], y=y)
    return np.eye(2)[cue], t


# ---------------------------------------------------------------- STEP 0
def step0(p39, blend_min, sigma=2.0):
    """replay g5.39's P at sigma 2.0 on its TEST stream, byte for byte, and split its invalid samples."""
    tmpl, tcls = E.templates(p39)
    si = p39["sigmas"].index(sigma)
    rows = []
    for seed in p39["seeds"]:
        x, t = targets_and_sparse(seed, p39)
        sparse_px = 0.5 * t.sum(1).mean()
        ss = np.random.SeedSequence(seed)
        r_init, r_batch, r_tnoise = [np.random.default_rng(s) for s in ss.spawn(4)[1:]]
        net = E.init_net(r_init, p39["sizes"])
        bs, ts = int(r_batch.integers(2 ** 63)), int(r_tnoise.integers(2 ** 63))
        net = E.train(net, x, t, sigma, p39["k_best_of"], p39["train"], np.random.default_rng(bs),
                      np.random.default_rng(ts))
        per = [split(E.sample_p(net, c, sigma, p39["n_samples"], E.rng_for(seed, TEST, E.ARM_P, si, c)),
                     c, tmpl, tcls, p39["score"]["iou_min"], blend_min, sparse_px) for c in (0, 1)]
        row = pooled(per)
        row.update({"seed": seed, "sparse_px": sparse_px})
        rows.append(row)
    inv = sum(r["invalid"] for r in rows)
    tot = {k: sum(r[k] for r in rows) for k in ("blend", "sparse", "other")}
    return {"seeds": rows, "invalid": inv, "shares": {k: v / inv for k, v in tot.items()},
            "blend_share": tot["blend"] / inv}


# ---------------------------------------------------------------- general training
def adam_state(net):
    return ([[np.zeros_like(w), np.zeros_like(b)] for w, b in net],
            [[np.zeros_like(w), np.zeros_like(b)] for w, b in net])


def adam_step(net, grads, m, v, t, lr, b1=0.9, b2=0.999, eps=1e-8):
    for li in range(2):
        for j in range(2):
            m[li][j] = b1 * m[li][j] + (1 - b1) * grads[li][j]
            v[li][j] = b2 * v[li][j] + (1 - b2) * grads[li][j] ** 2
            mh = m[li][j] / (1 - b1 ** t)
            vh = v[li][j] / (1 - b2 ** t)
            net[li][j] = net[li][j] - lr * mh / (np.sqrt(vh) + eps)


def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))


def train_core(net, x, t, core, sigma, k, lam, recall, p, rng_batch, rng_noise):
    """core 'gauss' (sigma on the pre-activations, relu) or 'binary' (unit = Bernoulli(sigmoid(h)),
    straight-through dL/dh = dL/da * sigmoid'(h)); loss = recall x (min over k draws of the mean
    per-pixel BCE to the example's own target) + lam x (mean over draws and examples of the min per-pixel
    BCE to the batch's SAME-CUE targets)."""
    m, v = adam_state(net)
    npx = t.shape[1]
    for step in range(1, p["steps"] + 1):
        idx = rng_batch.integers(0, len(x), size=p["batch"])
        xb, tb = x[idx], t[idx]
        bsz = len(xb)
        (w1, bb1), (w2, bb2) = net
        h = xb @ w1 + bb1
        if core == "gauss":
            hk = h[None] + rng_noise.normal(0.0, sigma, size=(k,) + h.shape)
            ak = np.maximum(hk, 0.0)
        else:
            ph = sigmoid(h)
            ak = (rng_noise.random(size=(k,) + h.shape) < ph[None]).astype(np.float64)
        lk = ak @ w2 + bb2  # (k, B, px)
        sk = sigmoid(lk)
        gl = np.zeros_like(lk)
        if recall:
            bce = (np.logaddexp(0.0, lk) - tb[None] * lk).mean(2)
            pick = bce.argmin(0)
            r = np.arange(bsz)
            gl[pick, r] += (sk[pick, r] - tb) / (npx * bsz)
        if lam > 0:
            sp = np.logaddexp(0.0, lk).sum(2)  # (k, B)
            cross = lk @ tb.T  # (k, B, B)
            pair = (sp[..., None] - cross) / npx
            same = (xb @ xb.T) > 0.5  # same cue
            pair = np.where(same[None], pair, np.inf)
            jstar = pair.argmin(2)  # (k, B)
            gl += lam * (sk - tb[jstar]) / (npx * bsz * k)
        gw2 = np.einsum("kbh,kbp->hp", ak, gl)
        gb2 = gl.sum((0, 1))
        ga = gl @ w2.T  # (k, B, hid)
        if core == "gauss":
            gh = (ga * (hk > 0)).sum(0)
        else:
            gh = ga.sum(0) * ph * (1.0 - ph)
        adam_step(net, [[xb.T @ gh, gh.sum(0)], [gw2, gb2]], m, v, step, p["lr"])
    return net


def train_z(net, x, t, p, rng_batch):
    """Z: inputs cue bits + 3 code bits, sigma 0, loss = min per-pixel BCE over ALL 8 codes."""
    m, v = adam_state(net)
    npx = t.shape[1]
    for step in range(1, p["steps"] + 1):
        idx = rng_batch.integers(0, len(x), size=p["batch"])
        xb, tb = x[idx], t[idx]
        bsz = len(xb)
        (w1, bb1), (w2, bb2) = net
        xin = np.concatenate([np.repeat(xb[None], 8, 0), np.repeat(CODES[:, None], bsz, 1)], 2)
        hk = xin @ w1 + bb1
        ak = np.maximum(hk, 0.0)
        lk = ak @ w2 + bb2
        bce = (np.logaddexp(0.0, lk) - tb[None] * lk).mean(2)
        pick = bce.argmin(0)
        r = np.arange(bsz)
        g = (sigmoid(lk[pick, r]) - tb) / (npx * bsz)
        a, hh, xi = ak[pick, r], hk[pick, r], xin[pick, r]
        gh = (g @ w2.T) * (hh > 0)
        adam_step(net, [[xi.T @ gh, gh.sum(0)], [a.T @ g, g.sum(0)]], m, v, step, p["lr"])
    return net


# ---------------------------------------------------------------- samplers
def sample_s(net, cue, n, rng, frozen=False):
    h = E.hidden_pre(net, E.onehot(cue, n))
    if frozen:
        a = (h > 0).astype(np.float64)  # every unit at its likelier state (M1-S)
    else:
        a = (rng.random(size=h.shape) < sigmoid(h)).astype(np.float64)
    (_, _), (w2, b2) = net
    return ((a @ w2 + b2) > 0).astype(np.float64)


def sample_z(net, cue, n, rng):
    codes = CODES[rng.integers(0, 8, size=n)]
    xin = np.concatenate([E.onehot(cue, n), codes], 1)
    (w1, b1), (w2, b2) = net
    return ((np.maximum(xin @ w1 + b1, 0.0) @ w2 + b2) > 0).astype(np.float64)


# ---------------------------------------------------------------- one seed
def run_seed(seed, p, tmpl, tcls):
    ss = np.random.SeedSequence(seed)
    r_data, r_init, r_batch, r_tnoise = [np.random.default_rng(s) for s in ss.spawn(4)]
    d, n_s, iou_min, blend_min = p["data"], p["n_samples"], p["score"]["iou_min"], p["blend_min"]
    n = d["n_train"]
    cue = r_data.integers(0, 2, size=n)
    pick = r_data.integers(0, 2, size=n)
    y = np.array([E.PAIRS[c][q] for c, q in zip(cue, pick)])
    t, _ = G37.make_lines(r_data, n, d["side"], d["width"], 0.0, d["jitter_deg"], d["max_offset"], y=y)
    x = np.eye(2)[cue]
    sparse_px = 0.5 * t.sum(1).mean()
    init_state = r_init.bit_generator.state
    batch_seed, tnoise_seed = int(r_batch.integers(2 ** 63)), int(r_tnoise.integers(2 ** 63))
    k, tr, lam = p["k_best_of"], p["train"], p["lam"]

    def fresh(sizes):
        r_init.bit_generator.state = init_state  # the SAME init stream for every arm (matched)
        return E.init_net(r_init, sizes)

    def rb():
        return np.random.default_rng(batch_seed)

    def rn():
        return np.random.default_rng(tnoise_seed)

    def evals(sampler, arm, si):
        return {st: pooled([split(sampler(c, E.rng_for(seed, sid, ARM[arm], si, c)), c, tmpl, tcls,
                                  iou_min, blend_min, sparse_px) for c in (0, 1)])
                for st, sid in (("val", VAL), ("test", TEST))}

    out = {"seed": seed, "sparse_px": sparse_px, "G": {}, "GC": {}, "GP": {}, "MF": {}, "M1_C": {}}
    for si, sg in enumerate(p["sigmas"]):
        net = E.train(fresh(p["sizes"]), x, t, sg, k, tr, rb(), rn())
        out["G"][str(sg)] = evals(lambda c, r: E.sample_p(net, c, sg, n_s, r), "G", si)
        out["MF"][str(sg)] = pooled([split(E.sample_mf(net, c, sg), c, tmpl, tcls, iou_min, blend_min,
                                           sparse_px) for c in (0, 1)])
        net_c = train_core(fresh(p["sizes"]), x, t, "gauss", sg, k, lam, True, tr, rb(), rn())
        out["GC"][str(sg)] = evals(lambda c, r: E.sample_p(net_c, c, sg, n_s, r), "GC", si)
        out["M1_C"][str(sg)] = pooled([split(E.sample_p(net_c, c, sg, n_s, E.rng_for(seed, M1_STREAM, ARM["GC"], si, c),
                                                        frozen=True), c, tmpl, tcls, iou_min, blend_min, sparse_px)
                                       for c in (0, 1)])
        net_p = train_core(fresh(p["sizes"]), x, t, "gauss", sg, k, lam, False, tr, rb(), rn())
        out["GP"][str(sg)] = evals(lambda c, r: E.sample_p(net_p, c, sg, n_s, r), "GP", si)
    net_s = train_core(fresh(p["sizes"]), x, t, "binary", 0.0, k, 0.0, True, tr, rb(), rn())
    out["S"] = evals(lambda c, r: sample_s(net_s, c, n_s, r), "S", 0)
    out["M1_S"] = pooled([split(sample_s(net_s, c, n_s, None, frozen=True), c, tmpl, tcls, iou_min, blend_min,
                                sparse_px) for c in (0, 1)])
    net_sc = train_core(fresh(p["sizes"]), x, t, "binary", 0.0, k, lam, True, tr, rb(), rn())
    out["SC"] = evals(lambda c, r: sample_s(net_sc, c, n_s, r), "SC", 0)
    net_z = train_z(fresh(p["sizes_z"]), x, t, tr, rb())
    out["Z"] = evals(lambda c, r: sample_z(net_z, c, n_s, r), "Z", 0)
    true_c, coin_c = [], []
    for c in (0, 1):
        r = E.rng_for(seed, M2_STREAM, ARM["TRUE"], 0, c)
        yy = np.repeat(np.array(E.PAIRS[c]), n_s // 2)
        lines, _ = G37.make_lines(r, n_s, d["side"], d["width"], 0.0, d["jitter_deg"], d["max_offset"], y=yy)
        true_c.append(E.score(lines, c, tmpl, tcls, iou_min))
        coin = (E.rng_for(seed, M2_STREAM, ARM["COIN"], 0, c).random(size=(n_s, d["side"] ** 2)) < 0.5)
        coin_c.append(E.score(coin.astype(np.float64), c, tmpl, tcls, iou_min))
    out["M2_true"], out["M2_coin"] = E.score_cues(true_c), E.score_cues(coin_c)
    out["n_params"] = {"G": G37.n_params(net_s), "Z": G37.n_params(net_z)}
    return out


def main(argv):
    if argv[1] == "step0":  # step0 G539_PARAMS G541_PARAMS OUT_JSON
        p39, p = json.load(open(argv[2])), json.load(open(argv[3]))
        res = {"leaf": "goal:g5.41", "step": 0, "numpy": np.__version__, "g539_params": p39,
               "blend_min": p["blend_min"], "prediction": p["prediction"], **step0(p39, p["blend_min"])}
        out = argv[4]
    else:  # run PARAMS OUT_JSON
        p = json.load(open(argv[2]))
        tmpl, tcls = E.templates(p)
        res = {"leaf": "goal:g5.41", "step": 1, "numpy": np.__version__, "params": p,
               "seeds": [run_seed(s, p, tmpl, tcls) for s in p["seeds"]]}
        out = argv[3]
    with open(out, "w") as f:
        json.dump(res, f, indent=1, sort_keys=True)
        f.write("\n")


if __name__ == "__main__":
    main(sys.argv)
