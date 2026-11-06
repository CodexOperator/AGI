"""goal:g5.46 -- an encoder gives a CONTINUOUS core latent the per-target assignment Z3-ENUM gets by enumeration:
can it be valid AND richer than a lookup?

Closed rounds are IMPORTED, never edited: g537_line_orientation (generator), g539_joint_samples (task, scorer,
streams), g541_blend_race (the invalid split), g543_code_inputs (Z3-ENUM, distinct valid images).

  python g546_cvae.py PARAMS OUT_JSON

CV  decoder 2-32-64, z in R^d entering the hidden PRE-activations: h = W1 x + b1 + W_z z;
    encoder q(z | target, cue) = 66-16-2d (mu, log var); loss = BCE summed over the 64 pixels
    + beta x KL(q || N(0, I)) summed over d, both averaged over the batch (the ELBO, beta = 1);
    reparameterised z = mu + exp(log var / 2) eps, eps from the logged stream; a sample = z ~ N(0, I).
MK  the kill: CV with z ZEROED in training (W_z and the encoder get no gradient, stay at init),
    z ~ N(0, I) at sampling.
Z3  g5.43's Z3-ENUM exactly (g543_code_inputs.train_code / sample_code).
Every eval draw = default_rng([seed, stream, arm, setting, cue]).
"""
import json
import sys

import numpy as np

import g537_line_orientation as G37
import g539_joint_samples as E
import g541_blend_race as R
import g543_code_inputs as C

VAL, TEST, M2_STREAM, RICH = E.VAL, E.TEST, E.M2_STREAM, 5
ARM_IDS = {"CV2": 40, "CV1": 41, "CV4": 42, "MK": 43, "Z3-ENUM": 44, "TRUE": 45, "COIN": 46, "MC": 47}


# ---------------------------------------------------------------- the CV
def init_cv(rng, d):
    """decoder [2, 32, 64], then W_z (d x 32), then the encoder [66, 16, 2d], all from ONE init stream."""
    (w1, b1), (w2, b2) = E.init_net(rng, [2, 32, 64])
    wz = rng.normal(0.0, np.sqrt(2.0 / d), size=(d, 32))
    (we1, be1), (we2, be2) = E.init_net(rng, [66, 16, 2 * d])
    return {"w1": w1, "b1": b1, "wz": wz, "w2": w2, "b2": b2, "we1": we1, "be1": be1, "we2": we2, "be2": be2}


def encode(net, t, x):
    e_in = np.concatenate([t, x], 1)
    eh = e_in @ net["we1"] + net["be1"]
    ea = np.maximum(eh, 0.0)
    eo = ea @ net["we2"] + net["be2"]
    d = net["wz"].shape[0]
    return eo[:, :d], eo[:, d:], (e_in, eh, ea)


def decode(net, x, z):
    h = x @ net["w1"] + net["b1"] + z @ net["wz"]
    a = np.maximum(h, 0.0)
    return a @ net["w2"] + net["b2"], (h, a)


def kl(mu, lv):
    return 0.5 * (mu ** 2 + np.exp(lv) - lv - 1.0).sum(1)


def loss_and_grads(net, x, t, eps, beta, zero_z=False):
    """the batch-mean ELBO loss and its exact gradients (zero_z: z = 0, W_z and the encoder get none)."""
    bsz = len(x)
    if zero_z:
        z = np.zeros((bsz, net["wz"].shape[0]))
        mu = lv = None
    else:
        mu, lv, (e_in, eh, ea) = encode(net, t, x)
        std = np.exp(0.5 * lv)
        z = mu + std * eps
    l, (h, a) = decode(net, x, z)
    loss = (np.logaddexp(0.0, l) - t * l).sum(1).mean()
    if not zero_z:
        loss += beta * kl(mu, lv).mean()
    dl = (R.sigmoid(l) - t) / bsz
    g = {"w2": a.T @ dl, "b2": dl.sum(0)}
    dh = (dl @ net["w2"].T) * (h > 0)
    g["w1"], g["b1"] = x.T @ dh, dh.sum(0)
    if not zero_z:
        g["wz"] = z.T @ dh
        dz = dh @ net["wz"].T
        dmu = dz + beta * mu / bsz
        dlv = dz * eps * 0.5 * std + beta * 0.5 * (np.exp(lv) - 1.0) / bsz
        deo = np.concatenate([dmu, dlv], 1)
        g["we2"], g["be2"] = ea.T @ deo, deo.sum(0)
        deh = (deo @ net["we2"].T) * (eh > 0)
        g["we1"], g["be1"] = e_in.T @ deh, deh.sum(0)
    return loss, g


def train_cv(net, x, t, p, rng_batch, rng_eps, zero_z=False):
    tr, beta = p["train"], p["beta"]
    m = {k: np.zeros_like(v) for k, v in net.items()}
    v = {k: np.zeros_like(w) for k, w in net.items()}
    b1, b2, epsa = 0.9, 0.999, 1e-8
    d = net["wz"].shape[0]
    for step in range(1, tr["steps"] + 1):
        idx = rng_batch.integers(0, len(x), size=tr["batch"])
        eps = rng_eps.normal(0.0, 1.0, size=(len(idx), d))
        _, g = loss_and_grads(net, x[idx], t[idx], eps, beta, zero_z)
        for k, gk in g.items():  # a key with no gradient (zero_z) is never stepped
            m[k] = b1 * m[k] + (1 - b1) * gk
            v[k] = b2 * v[k] + (1 - b2) * gk ** 2
            net[k] = net[k] - tr["lr"] * (m[k] / (1 - b1 ** step)) / (np.sqrt(v[k] / (1 - b2 ** step)) + epsa)
    return net


def sample_cv(net, cue, n, rng):
    z = rng.normal(0.0, 1.0, size=(n, net["wz"].shape[0]))
    return (decode(net, E.onehot(cue, n), z)[0] > 0).astype(np.float64)


def n_params_cv(net):
    return int(sum(v.size for v in net.values()))


# ---------------------------------------------------------------- scoring
def distinct_valid(samples, cue, tmpl, tcls, iou_min):
    vm = C.valid_mask(samples, cue, tmpl, tcls, iou_min)
    return int(len({row.tobytes() for row in samples[vm].astype(np.uint8)}))


# ---------------------------------------------------------------- one seed
def run_seed(seed, p, tmpl, tcls):
    ss = np.random.SeedSequence(seed)
    r_data, r_init, r_batch, r_tnoise = [np.random.default_rng(s) for s in ss.spawn(4)]
    d, n_s, n_r, iou_min = p["data"], p["n_samples"], p["n_rich"], p["score"]["iou_min"]
    n = d["n_train"]
    cue = r_data.integers(0, 2, size=n)
    pick = r_data.integers(0, 2, size=n)
    y = np.array([E.PAIRS[c][q] for c, q in zip(cue, pick)])
    t, _ = G37.make_lines(r_data, n, d["side"], d["width"], 0.0, d["jitter_deg"], d["max_offset"], y=y)
    x = np.eye(2)[cue]
    sparse_px = 0.5 * t.sum(1).mean()
    init_state = r_init.bit_generator.state
    batch_seed, tnoise_seed = int(r_batch.integers(2 ** 63)), int(r_tnoise.integers(2 ** 63))

    def reset():
        r_init.bit_generator.state = init_state  # the SAME init stream for every arm (matched)
        return r_init

    def evals(sampler, arm):
        out = {}
        for st, sid in (("val", VAL), ("test", TEST)):
            per = [C.score_cue(sampler(c, n_s, E.rng_for(seed, sid, ARM_IDS[arm], 0, c)), c, tmpl, tcls, iou_min)
                   for c in (0, 1)]
            out[st] = C.cues(per)
        out["rich_distinct"] = [distinct_valid(sampler(c, n_r, E.rng_for(seed, RICH, ARM_IDS[arm], 0, c)), c, tmpl,
                                               tcls, iou_min) for c in (0, 1)]
        out["split"] = R.pooled([R.split(sampler(c, n_s, E.rng_for(seed, TEST, ARM_IDS[arm], 0, c)), c, tmpl, tcls,
                                          iou_min, p["blend_min"], sparse_px) for c in (0, 1)])
        for k in ("cues",):
            out["split"].pop(k)
        return out

    out = {"seed": seed}
    for arm, dz, zero in (("CV2", 2, False), ("CV1", 1, False), ("CV4", 4, False), ("MK", 2, True)):
        net = train_cv(init_cv(reset(), dz), x, t, p, np.random.default_rng(batch_seed),
                       np.random.default_rng(tnoise_seed), zero_z=zero)
        cell = evals(lambda c, k, r: sample_cv(net, c, k, r), arm)
        mu, lv, _ = encode(net, t, x)
        cell["kl_nats"] = float(kl(mu, lv).mean())
        cell["n_params"] = n_params_cv(net)
        out[arm] = cell
    z3 = {"kind": "enum", "dim": 3}
    net_z, wins = C.train_code(E.init_net(reset(), [5, 32, 64]), x, t, z3, p, np.random.default_rng(batch_seed),
                               np.random.default_rng(tnoise_seed))
    out["Z3-ENUM"] = evals(lambda c, k, r: C.sample_code(net_z, c, k, z3, r), "Z3-ENUM")
    out["Z3-ENUM"]["win_fraction"] = len(wins) / 8
    true_c, coin_c, mc = [], [], []
    for c in (0, 1):
        r = E.rng_for(seed, M2_STREAM, ARM_IDS["TRUE"], 0, c)
        yy = np.repeat(np.array(E.PAIRS[c]), n_s // 2)
        lines, _ = G37.make_lines(r, n_s, d["side"], d["width"], 0.0, d["jitter_deg"], d["max_offset"], y=yy)
        true_c.append(E.score(lines, c, tmpl, tcls, iou_min))
        coin = (E.rng_for(seed, M2_STREAM, ARM_IDS["COIN"], 0, c).random(size=(n_s, d["side"] ** 2)) < 0.5)
        coin_c.append(E.score(coin.astype(np.float64), c, tmpl, tcls, iou_min))
        r = E.rng_for(seed, M2_STREAM, ARM_IDS["MC"], 0, c)
        yy = np.repeat(np.array(E.PAIRS[c]), n_r // 2)
        lines, _ = G37.make_lines(r, n_r, d["side"], d["width"], 0.0, d["jitter_deg"], d["max_offset"], y=yy)
        mc.append(distinct_valid(lines, c, tmpl, tcls, iou_min))
    out["M2_true"], out["M2_coin"], out["MC_distinct"] = E.score_cues(true_c), E.score_cues(coin_c), mc
    return out


def main(argv):
    p = json.load(open(argv[1]))
    tmpl, tcls = E.templates(p)
    res = {"leaf": "goal:g5.46", "numpy": np.__version__, "params": p,
           "seeds": [run_seed(s, p, tmpl, tcls) for s in p["seeds"]]}
    with open(argv[2], "w") as f:
        json.dump(res, f, indent=1, sort_keys=True)
        f.write("\n")


if __name__ == "__main__":
    main(sys.argv)
