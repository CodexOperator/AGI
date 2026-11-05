"""goal:g5.37 -- intrinsic state noise at the core vs output temperature vs a hand-set filter bank.

One process, numpy only, CPU. Every random draw comes from a numpy SeedSequence spawned from the
seed recorded in params.json (remix veto: keep the chaos, log the dice): data, init, the training
noise, the inference noise and the temperature samples each get their own child stream, so a
reviewer replays a cell byte for byte with the same numpy version (recorded in the results).

  python g537_line_orientation.py PARAMS_JSON OUT_JSON
"""
import json
import sys

import numpy as np

CLASSES = 4  # 0, 45, 90, 135 degrees


# ---------------------------------------------------------------- data
def make_lines(rng, n, side, width, px_noise, jitter_deg, max_offset, y=None):
    """n images side x side: one line of class k at angle 45k +- jitter, offset from centre.
    y given (goal:g5.39 reuses this): the classes are taken, not drawn; px_noise 0 draws nothing."""
    if y is None:
        y = rng.integers(0, CLASSES, size=n)
    ang = np.deg2rad(45.0 * y + rng.uniform(-jitter_deg, jitter_deg, size=n))
    off = rng.uniform(-max_offset, max_offset, size=n)
    img = render(ang, off, side, width)
    if px_noise > 0:
        img += rng.normal(0.0, px_noise, size=img.shape)
    return img.reshape(n, side * side), y


def render(ang, off, side, width):
    """clean binary lines: angle ang (radians, y up), offset off along the normal; (n, side, side)."""
    c = (side - 1) / 2.0
    yy, xx = np.mgrid[0:side, 0:side]
    px, py = xx - c, c - yy  # pixel centres, y up
    # distance of each pixel centre to the line through (off * normal) with direction ang
    nx, ny = -np.sin(ang), np.cos(ang)
    d = np.abs(px[None] * nx[:, None, None] + py[None] * ny[:, None, None] - off[:, None, None])
    return (d <= width / 2.0).astype(np.float64)


# ---------------------------------------------------------------- net
def init_net(rng, sizes):
    ws = []
    for a, b in zip(sizes[:-1], sizes[1:]):
        ws.append([rng.normal(0.0, np.sqrt(2.0 / a), size=(a, b)), np.zeros(b)])
    return ws


def n_params(net):
    return int(sum(w.size + b.size for w, b in net))


def forward(net, x, sigma, rng):
    """64-16-4: noise N(0, sigma^2) on the hidden PRE-activations (the core state), then relu."""
    (w1, b1), (w2, b2) = net
    h = x @ w1 + b1
    if sigma > 0:
        h = h + rng.normal(0.0, sigma, size=h.shape)
    a = np.maximum(h, 0.0)
    return a @ w2 + b2, (x, h, a)


def train(net, x, y, sigma, p, rng_batch, rng_noise):
    """Adam on softmax cross-entropy; the same steps, batch and lr for every arm."""
    m = [[np.zeros_like(w), np.zeros_like(b)] for w, b in net]
    v = [[np.zeros_like(w), np.zeros_like(b)] for w, b in net]
    b1, b2, eps, lr = 0.9, 0.999, 1e-8, p["lr"]
    for t in range(1, p["steps"] + 1):
        idx = rng_batch.integers(0, len(x), size=p["batch"])
        xb, yb = x[idx], y[idx]
        logits, (xi, h, a) = forward(net, xb, sigma, rng_noise)
        z = logits - logits.max(1, keepdims=True)
        pr = np.exp(z)
        pr /= pr.sum(1, keepdims=True)
        g = pr
        g[np.arange(len(yb)), yb] -= 1.0
        g /= len(yb)
        (w1, _), (w2, _) = net
        gw2, gb2 = a.T @ g, g.sum(0)
        gh = (g @ w2.T) * (h > 0)
        gw1, gb1 = xi.T @ gh, gh.sum(0)
        grads = [[gw1, gb1], [gw2, gb2]]
        for li in range(2):
            for j in range(2):
                m[li][j] = b1 * m[li][j] + (1 - b1) * grads[li][j]
                v[li][j] = b2 * v[li][j] + (1 - b2) * grads[li][j] ** 2
                mh = m[li][j] / (1 - b1 ** t)
                vh = v[li][j] / (1 - b2 ** t)
                net[li][j] = net[li][j] - lr * mh / (np.sqrt(vh) + eps)
    return net


# ---------------------------------------------------------------- votes and scores
def vote(labels_k):
    """labels_k: (K, n) int votes -> (answer, confidence = winning vote fraction).
    Ties go to the lowest class index (argmax rule, deterministic)."""
    k = labels_k.shape[0]
    counts = np.stack([(labels_k == c).sum(0) for c in range(CLASSES)], 1)
    ans = counts.argmax(1)
    return ans, counts.max(1) / float(k)


def ece(conf, correct, bins):
    edges = np.linspace(0.0, 1.0, bins + 1)
    e, n = 0.0, len(conf)
    for i in range(bins):
        lo, hi = edges[i], edges[i + 1]
        sel = (conf > lo) & (conf <= hi) if i else (conf >= lo) & (conf <= hi)
        if sel.any():
            e += sel.sum() / n * abs(correct[sel].mean() - conf[sel].mean())
    return float(e)


def score(ans, conf, y, bins):
    correct = (ans == y).astype(np.float64)
    return {"acc": float(correct.mean()), "ece": ece(conf, correct, bins)}


def votes_noise(net, x, sigma, k, rng):
    return np.stack([forward(net, x, sigma, rng)[0].argmax(1) for _ in range(k)])


def votes_temperature(net, x, tau, k, rng):
    logits = forward(net, x, 0.0, None)[0] / tau
    z = logits - logits.max(1, keepdims=True)
    pr = np.exp(z)
    pr /= pr.sum(1, keepdims=True)
    cdf = pr.cumsum(1)
    u = rng.random(size=(k, len(x), 1))
    return np.minimum((u > cdf[None]).sum(2), CLASSES - 1)


# ---------------------------------------------------------------- arm B: hand-set filter bank
def bar_bank():
    """4 hand-set 3x3 oriented-bar kernels (0, 45, 90, 135 deg), zero mean, 0 training."""
    h = np.array([[-1, -1, -1], [2, 2, 2], [-1, -1, -1]], dtype=np.float64)
    d = np.array([[-1, -1, 2], [-1, 2, -1], [2, -1, -1]], dtype=np.float64)  # 45 deg, y up
    return [h, d, h.T.copy(), d[:, ::-1].copy()]


def bank_answer(x, side, bank, rotate):
    """class = argmax over kernels of the summed rectified response; `rotate` relabels kernel k
    as class (k + rotate) mod 4 -- rotate=1 is the MUTANT that must read RED."""
    imgs = x.reshape(-1, side, side)
    resp = []
    for kern in bank:
        r = np.zeros(len(imgs))
        for i in range(side - 2):
            for j in range(side - 2):
                r += np.maximum((imgs[:, i:i + 3, j:j + 3] * kern).sum((1, 2)), 0.0)
        resp.append(r)
    resp = np.stack(resp, 1)
    return (resp.argmax(1) + rotate) % CLASSES


# ---------------------------------------------------------------- one seed
def run_seed(seed, p):
    ss = np.random.SeedSequence(seed)
    r_data, r_test, r_init, r_batch, r_tnoise, r_inoise, r_temp = [
        np.random.default_rng(s) for s in ss.spawn(7)]
    d, sh = p["data"], p["shift"]
    xtr, ytr = make_lines(r_data, d["n_train"], d["side"], d["width"], d["px_noise"],
                          d["jitter_deg"], d["max_offset"])
    xte, yte = make_lines(r_test, d["n_test"], d["side"], sh["width"], sh["px_noise"],
                          d["jitter_deg"], d["max_offset"])
    init_state = r_init.bit_generator.state
    k, bins = p["k_votes"], p["ece_bins"]
    out = {"seed": seed, "P": {}, "P0": {}, "T": {}}
    nets = {}
    batch_seed, tnoise_seed = int(r_batch.integers(2 ** 63)), int(r_tnoise.integers(2 ** 63))
    for s in p["sigmas"]:
        r_init.bit_generator.state = init_state  # the SAME init for every sigma (matched)
        net = init_net(r_init, p["sizes"])
        nets[s] = train(net, xtr, ytr, s, p["train"],
                        np.random.default_rng(batch_seed),  # the SAME batches for every sigma
                        np.random.default_rng(tnoise_seed))
        out["P"][str(s)] = score(*vote(votes_noise(nets[s], xte, s, k, r_inoise)), yte, bins)
        if s > 0:
            out["P0"][str(s)] = score(*vote(votes_noise(nets[s], xte, 0.0, k, None)), yte, bins)
    for tau in p["taus"]:
        out["T"][str(tau)] = score(*vote(votes_temperature(nets[0.0], xte, tau, k, r_temp)),
                                   yte, bins)
    bank = bar_bank()
    ones = np.ones(len(yte))
    out["B"] = score(bank_answer(xte, d["side"], bank, 0), ones, yte, bins)
    out["B_rot"] = score(bank_answer(xte, d["side"], bank, 1), ones, yte, bins)
    out["n_params"] = n_params(nets[0.0])
    return out


def main(argv):
    p = json.load(open(argv[1]))
    if float(p["sigmas"][0]) != 0.0:
        raise SystemExit("sigmas[0] must be 0 (the deterministic net arm T samples from)")
    res = {"leaf": "goal:g5.37", "numpy": np.__version__, "params": p,
           "seeds": [run_seed(s, p) for s in p["seeds"]]}
    with open(argv[2], "w") as f:
        json.dump(res, f, indent=1, sort_keys=True)
        f.write("\n")


if __name__ == "__main__":
    main(sys.argv)
