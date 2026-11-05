"""goal:g5.39 -- where several answers are valid, core noise vs output temperature on coherent joint samples.

A cue c in {0, 1} admits two orientations (c=0: {0, 90}, c=1: {45, 135}); a net 2-32-64 maps the
one-hot cue to 64 pixel logits. Arms (same data, init and batch streams per seed):
  P   Gaussian sigma on the 32 hidden pre-activations at training AND inference, pixel on iff
      logit > 0; trained best-of-K (loss = min over K noise draws of the per-pixel BCE).
  T   sigma 0, per-pixel BCE; a sample = independent Bernoulli(sigmoid(logit / tau)) per pixel.
  MF  P's weights, the hidden layer at its Gaussian expectation, one image per cue (REPORTED ONLY).
Mutants: M1 = P with ONE noise draw frozen per seed and cue; M2 = the scorer on true lines and on
Bernoulli(0.5) images. Generator and geometry: g537_line_orientation (goal:g5.37).
Every eval draw comes from default_rng([seed, stream, arm, setting, cue]): replayable byte for byte.

  python g539_joint_samples.py PARAMS_JSON OUT_JSON
"""
import json
import math
import sys

import numpy as np

import g537_line_orientation as G

PAIRS = {0: (0, 2), 1: (1, 3)}
VAL, TEST, M1_STREAM, M2_STREAM = 1, 2, 3, 4
ARM_P, ARM_T, ARM_MF, ARM_TRUE, ARM_COIN = 0, 1, 2, 3, 4


# ---------------------------------------------------------------- scorer
def templates(p):
    s = p["score"]
    js = np.arange(-s["jitter_deg"], s["jitter_deg"] + 1e-9, s["jitter_step"])
    offs = np.arange(-s["max_offset"], s["max_offset"] + 1e-9, s["offset_step"])
    ang, off, cls = [], [], []
    for k in range(G.CLASSES):
        for j in js:
            for o in offs:
                ang.append(np.deg2rad(45.0 * k + j))
                off.append(o)
                cls.append(k)
    side = p["data"]["side"]
    t = G.render(np.array(ang), np.array(off), side, p["data"]["width"]).reshape(-1, side * side)
    return t, np.array(cls)


def score(samples, cue, tmpl, tcls, iou_min):
    """samples (n, 64) in {0,1}: VALID iff best IoU >= 3/5 (iou_min = [5, 3]) AND its class is in the
    cue's pair; coverage = entropy of the valid samples' class histogram / log 2."""
    inter = samples @ tmpl.T
    union = samples.sum(1, keepdims=True) + tmpl.sum(1)[None] - inter
    best = (inter / union).argmax(1)
    cls = tcls[best]
    r = np.arange(len(samples))
    num, den = iou_min  # VALID in integers (plasma pre-run pin, 11:14Z): num x |inter| >= den x |union|
    hit = num * np.rint(inter[r, best]).astype(np.int64) >= den * np.rint(union[r, best]).astype(np.int64)
    valid = hit & np.isin(cls, PAIRS[cue])
    vf = float(valid.mean())
    cov = 0.0
    if valid.any():
        h = np.bincount(cls[valid], minlength=G.CLASSES) / valid.sum()
        h = h[h > 0]
        cov = float(-(h * np.log(h)).sum() / math.log(2))
    return {"valid": vf, "coverage": cov, "score": vf * cov}


def score_cues(per_cue):
    out = {k: float(np.mean([c[k] for c in per_cue])) for k in ("valid", "coverage", "score")}
    out["cues"] = per_cue
    return out


# ---------------------------------------------------------------- net
def init_net(rng, sizes):
    return G.init_net(rng, sizes)


def hidden_pre(net, cue_onehot):
    (w1, b1), _ = net
    return cue_onehot @ w1 + b1


def train(net, x, t, sigma, k, p, rng_batch, rng_noise):
    """Adam; loss = min over k noise draws of the mean per-pixel BCE (k = 1, sigma = 0 for T)."""
    m = [[np.zeros_like(w), np.zeros_like(b)] for w, b in net]
    v = [[np.zeros_like(w), np.zeros_like(b)] for w, b in net]
    b1, b2, eps, lr = 0.9, 0.999, 1e-8, p["lr"]
    for step in range(1, p["steps"] + 1):
        idx = rng_batch.integers(0, len(x), size=p["batch"])
        xb, tb = x[idx], t[idx]
        (w1, _), (w2, bb2) = net
        h = xb @ w1 + net[0][1]
        noise = rng_noise.normal(0.0, sigma, size=(k,) + h.shape) if sigma > 0 else np.zeros((k,) + h.shape)
        hk = h[None] + noise
        ak = np.maximum(hk, 0.0)
        lk = ak @ w2 + bb2
        bce = (np.logaddexp(0.0, lk) - tb[None] * lk).mean(2)  # (k, B)
        pick = bce.argmin(0)
        r = np.arange(len(xb))
        a, hh, logit = ak[pick, r], hk[pick, r], lk[pick, r]
        g = (1.0 / (1.0 + np.exp(-logit)) - tb) / (tb.shape[1] * len(xb))
        gw2, gb2 = a.T @ g, g.sum(0)
        gh = (g @ w2.T) * (hh > 0)
        gw1, gb1 = xb.T @ gh, gh.sum(0)
        grads = [[gw1, gb1], [gw2, gb2]]
        for li in range(2):
            for j in range(2):
                m[li][j] = b1 * m[li][j] + (1 - b1) * grads[li][j]
                v[li][j] = b2 * v[li][j] + (1 - b2) * grads[li][j] ** 2
                mh = m[li][j] / (1 - b1 ** step)
                vh = v[li][j] / (1 - b2 ** step)
                net[li][j] = net[li][j] - lr * mh / (np.sqrt(vh) + eps)
    return net


def onehot(cue, n):
    x = np.zeros((n, 2))
    x[:, cue] = 1.0
    return x


def sample_p(net, cue, sigma, n, rng, frozen=False):
    h = hidden_pre(net, onehot(cue, n))
    noise = rng.normal(0.0, sigma, size=(1 if frozen else n, h.shape[1]))
    a = np.maximum(h + noise, 0.0)
    (_, _), (w2, b2) = net
    return ((a @ w2 + b2) > 0).astype(np.float64)


def sample_t(net, cue, tau, n, rng):
    h = hidden_pre(net, onehot(cue, n))
    (_, _), (w2, b2) = net
    logit = np.maximum(h, 0.0) @ w2 + b2
    pr = 1.0 / (1.0 + np.exp(-logit / tau))
    return (rng.random(size=pr.shape) < pr).astype(np.float64)


def sample_mf(net, cue, sigma):
    """E[relu(h + N(0, sigma^2))] = h Phi(h / sigma) + sigma phi(h / sigma); one image."""
    h = hidden_pre(net, onehot(cue, 1))[0]
    z = h / sigma
    phi = np.exp(-0.5 * z ** 2) / math.sqrt(2 * math.pi)
    big_phi = 0.5 * (1.0 + np.array([math.erf(v / math.sqrt(2)) for v in z]))
    a = h * big_phi + sigma * phi
    (_, _), (w2, b2) = net
    return ((a @ w2 + b2) > 0).astype(np.float64)[None]


def rng_for(seed, stream, arm, setting, cue):
    return np.random.default_rng([seed, stream, arm, setting, cue])


# ---------------------------------------------------------------- one seed
def run_seed(seed, p, tmpl, tcls):
    ss = np.random.SeedSequence(seed)
    r_data, r_init, r_batch, r_tnoise = [np.random.default_rng(s) for s in ss.spawn(4)]
    d, n_s, iou_min = p["data"], p["n_samples"], p["score"]["iou_min"]
    n = d["n_train"]
    cue = r_data.integers(0, 2, size=n)
    pick = r_data.integers(0, 2, size=n)
    y = np.array([PAIRS[c][q] for c, q in zip(cue, pick)])
    t, _ = G.make_lines(r_data, n, d["side"], d["width"], 0.0, d["jitter_deg"], d["max_offset"], y=y)
    x = np.eye(2)[cue]
    init_state = r_init.bit_generator.state
    batch_seed, tnoise_seed = int(r_batch.integers(2 ** 63)), int(r_tnoise.integers(2 ** 63))

    def fresh_net():
        r_init.bit_generator.state = init_state  # the SAME init for every arm (matched)
        return init_net(r_init, p["sizes"])

    def trained(sigma, k):
        return train(fresh_net(), x, t, sigma, k, p["train"], np.random.default_rng(batch_seed),
                     np.random.default_rng(tnoise_seed))

    out = {"seed": seed, "P": {}, "T": {}, "MF": {}, "M1": {}}
    nets_p = {}
    for si, sg in enumerate(p["sigmas"]):
        nets_p[sg] = trained(sg, p["k_best_of"])
        out["P"][str(sg)] = {st: score_cues([score(sample_p(nets_p[sg], c, sg, n_s, rng_for(seed, sid, ARM_P, si, c)),
                                                   c, tmpl, tcls, iou_min) for c in (0, 1)])
                             for st, sid in (("val", VAL), ("test", TEST))}
        out["MF"][str(sg)] = score_cues([score(sample_mf(nets_p[sg], c, sg), c, tmpl, tcls, iou_min)
                                         for c in (0, 1)])
        out["M1"][str(sg)] = score_cues([score(sample_p(nets_p[sg], c, sg, n_s, rng_for(seed, M1_STREAM, ARM_P, si, c),
                                                        frozen=True), c, tmpl, tcls, iou_min) for c in (0, 1)])
    net_t = trained(0.0, 1)
    for ti, tau in enumerate(p["taus"]):
        out["T"][str(tau)] = {st: score_cues([score(sample_t(net_t, c, tau, n_s, rng_for(seed, sid, ARM_T, ti, c)),
                                                    c, tmpl, tcls, iou_min) for c in (0, 1)])
                              for st, sid in (("val", VAL), ("test", TEST))}
    # M2: the scorer on 64 true target lines per cue (32 per class) and on 64 Bernoulli(0.5) images
    true_c, coin_c = [], []
    for c in (0, 1):
        r = rng_for(seed, M2_STREAM, ARM_TRUE, 0, c)
        yy = np.repeat(np.array(PAIRS[c]), n_s // 2)
        lines, _ = G.make_lines(r, n_s, d["side"], d["width"], 0.0, d["jitter_deg"], d["max_offset"], y=yy)
        true_c.append(score(lines, c, tmpl, tcls, iou_min))
        coin = (rng_for(seed, M2_STREAM, ARM_COIN, 0, c).random(size=(n_s, d["side"] ** 2)) < 0.5).astype(np.float64)
        coin_c.append(score(coin, c, tmpl, tcls, iou_min))
    out["M2_true"], out["M2_coin"] = score_cues(true_c), score_cues(coin_c)
    out["n_params"] = G.n_params(net_t)
    return out


def main(argv):
    p = json.load(open(argv[1]))
    tmpl, tcls = templates(p)
    res = {"leaf": "goal:g5.39", "numpy": np.__version__, "params": p, "n_templates": int(len(tmpl)),
           "seeds": [run_seed(s, p, tmpl, tcls) for s in p["seeds"]]}
    with open(argv[2], "w") as f:
        json.dump(res, f, indent=1, sort_keys=True)
        f.write("\n")


if __name__ == "__main__":
    main(sys.argv)
