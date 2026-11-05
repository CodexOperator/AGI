"""goal:g5.49 -- L-RICH-T: is CV richer in LINES than a 64-code lookup? Distinct valid TEMPLATES, not images.

Closed rounds are IMPORTED, never edited: g537_line_orientation (generator), g539_joint_samples (task, scorer,
streams), g543_code_inputs (Z6-ENUM, valid mask), g546_cvae (CV exactly as g5.46 defined it, MK).

  python g549_template_distinct.py PARAMS OUT_JSON

The counter (plasma, f6dd947d79): the 2108-template grid DEDUPED by rendered (class, image) -> 836 templates;
a VALID sample's template = its best IoU match over that set (np.argmax: ties to the lowest index);
template-distinct = the number of distinct templates among a cue's valid samples.
Arms: CV2 (g546 CV, z in R^2); MK (g546's kill); Z6-ENUM (g543, REPORTED); JV (Z3 code + CV latent,
JointVAE, REPORTED); MS (speckle) and MC-T (true lines), the counter's two instruments.
Every draw = default_rng([seed, stream, arm, setting, cue]).
"""
import json
import resource
import sys

import numpy as np

import g537_line_orientation as G37
import g539_joint_samples as E
import g541_blend_race as R
import g543_code_inputs as C
import g546_cvae as V

VAL, TEST, M2_STREAM, RICH = E.VAL, E.TEST, E.M2_STREAM, V.RICH
ARM_IDS = {"CV2": 60, "MK": 61, "Z6-ENUM": 62, "JV": 63, "MS": 64, "MC-T": 65, "TRUE": 66, "COIN": 67}


# ---------------------------------------------------------------- the counter
def dedup(tmpl, tcls):
    """keep the FIRST of each distinct (class, image) in grid order."""
    seen, keep = set(), []
    for i, (row, k) in enumerate(zip(tmpl.astype(np.uint8), tcls)):
        key = (int(k), row.tobytes())
        if key not in seen:
            seen.add(key)
            keep.append(i)
    keep = np.array(keep)
    return tmpl[keep], tcls[keep]


def template_ids(samples, cue, tmpl, tcls, dt, dcls, iou_min):
    """the deduped template index of each VALID sample (validity exactly as g539's scorer)."""
    vm = C.valid_mask(samples, cue, tmpl, tcls, iou_min)
    if not vm.any():
        return np.array([], dtype=np.int64)
    inter, union = R.iou_all(samples[vm], dt)
    return (inter / union).argmax(1)


def count(samples, cue, tmpl, tcls, dt, dcls, iou_min):
    s = E.score(samples, cue, tmpl, tcls, iou_min)
    s["templates"] = int(len(set(template_ids(samples, cue, tmpl, tcls, dt, dcls, iou_min).tolist())))
    s["images"] = V.distinct_valid(samples, cue, tmpl, tcls, iou_min)
    return s


# ---------------------------------------------------------------- JV: a Z3 code + the CV latent
def init_jv(rng, d=2, bits=3):
    """decoder [2 + bits, 32, 64], W_z, encoder [66, 16, 2d] on ONE init stream (g546's order)."""
    (w1, b1), (w2, b2) = E.init_net(rng, [2 + bits, 32, 64])
    wz = rng.normal(0.0, np.sqrt(2.0 / d), size=(d, 32))
    (we1, be1), (we2, be2) = E.init_net(rng, [66, 16, 2 * d])
    return {"w1": w1, "b1": b1, "wz": wz, "w2": w2, "b2": b2, "we1": we1, "be1": be1, "we2": we2, "be2": be2}


def jv_loss_and_grads(net, x, t, eps, beta, codes):
    """ELBO with the code ENUMERATED: loss = min over codes of the summed BCE + beta KL(q(z | t, cue)); the
    encoder sees the target and cue only; the gradient flows through the winning code (g543's min)."""
    bsz, ncode = len(x), len(codes)
    mu, lv, (e_in, eh, ea) = V.encode(net, t, x)
    std = np.exp(0.5 * lv)
    z = mu + std * eps
    xin = np.concatenate([np.repeat(x[None], ncode, 0), np.repeat(codes[:, None], bsz, 1)], 2)
    h = xin @ net["w1"] + net["b1"] + (z @ net["wz"])[None]
    a = np.maximum(h, 0.0)
    l = a @ net["w2"] + net["b2"]
    bce = (np.logaddexp(0.0, l) - t[None] * l).sum(2)  # (codes, B)
    pick = bce.argmin(0)
    r = np.arange(bsz)
    loss = bce[pick, r].mean() + beta * V.kl(mu, lv).mean()
    lp, hp, ap, xp = l[pick, r], h[pick, r], a[pick, r], xin[pick, r]
    dl = (R.sigmoid(lp) - t) / bsz
    g = {"w2": ap.T @ dl, "b2": dl.sum(0)}
    dh = (dl @ net["w2"].T) * (hp > 0)
    g["w1"], g["b1"], g["wz"] = xp.T @ dh, dh.sum(0), z.T @ dh
    dz = dh @ net["wz"].T
    dmu = dz + beta * mu / bsz
    dlv = dz * eps * 0.5 * std + beta * 0.5 * (np.exp(lv) - 1.0) / bsz
    deo = np.concatenate([dmu, dlv], 1)
    g["we2"], g["be2"] = ea.T @ deo, deo.sum(0)
    deh = (deo @ net["we2"].T) * (eh > 0)
    g["we1"], g["be1"] = e_in.T @ deh, deh.sum(0)
    return loss, g


def train_jv(net, x, t, p, rng_batch, rng_eps, bits=3):
    tr, beta, codes = p["train"], p["beta"], C.code_table(bits)
    m = {k: np.zeros_like(v) for k, v in net.items()}
    v = {k: np.zeros_like(w) for k, w in net.items()}
    b1, b2, epsa = 0.9, 0.999, 1e-8
    d = net["wz"].shape[0]
    for step in range(1, tr["steps"] + 1):
        idx = rng_batch.integers(0, len(x), size=tr["batch"])
        eps = rng_eps.normal(0.0, 1.0, size=(len(idx), d))
        _, g = jv_loss_and_grads(net, x[idx], t[idx], eps, beta, codes)
        for k, gk in g.items():
            m[k] = b1 * m[k] + (1 - b1) * gk
            v[k] = b2 * v[k] + (1 - b2) * gk ** 2
            net[k] = net[k] - tr["lr"] * (m[k] / (1 - b1 ** step)) / (np.sqrt(v[k] / (1 - b2 ** step)) + epsa)
    return net


def sample_jv(net, cue, n, rng, bits=3):
    code = C.code_table(bits)[rng.integers(0, 2 ** bits, size=n)]
    z = rng.normal(0.0, 1.0, size=(n, net["wz"].shape[0]))
    xin = np.concatenate([E.onehot(cue, n), code], 1)
    h = xin @ net["w1"] + net["b1"] + z @ net["wz"]
    return ((np.maximum(h, 0.0) @ net["w2"] + net["b2"]) > 0).astype(np.float64)


# ---------------------------------------------------------------- the counter's instruments
def true_lines(rng, cue, n, d):
    yy = np.repeat(np.array(E.PAIRS[cue]), n // 2)
    lines, _ = G37.make_lines(rng, n, d["side"], d["width"], 0.0, d["jitter_deg"], d["max_offset"], y=yy)
    return lines


def speckle(rng, cue, n, d):
    """MS: ONE true line per cue (class drawn from the cue's pair), each copy with 1-2 random pixels flipped."""
    k = E.PAIRS[cue][int(rng.integers(0, 2))]
    base, _ = G37.make_lines(rng, 1, d["side"], d["width"], 0.0, d["jitter_deg"], d["max_offset"], y=np.array([k]))
    out = np.repeat(base, n, 0)
    for i in range(n):
        for j in rng.choice(d["side"] ** 2, size=int(rng.integers(1, 3)), replace=False):
            out[i, j] = 1.0 - out[i, j]
    return out


# ---------------------------------------------------------------- one seed
def run_seed(seed, p, tmpl, tcls, dt, dcls):
    ss = np.random.SeedSequence(seed)
    r_data, r_init, r_batch, r_tnoise = [np.random.default_rng(s) for s in ss.spawn(4)]
    d, n_s, n_r, iou_min = p["data"], p["n_samples"], p["n_rich"], p["score"]["iou_min"]
    n = d["n_train"]
    cue = r_data.integers(0, 2, size=n)
    pick = r_data.integers(0, 2, size=n)
    y = np.array([E.PAIRS[c][q] for c, q in zip(cue, pick)])
    t, _ = G37.make_lines(r_data, n, d["side"], d["width"], 0.0, d["jitter_deg"], d["max_offset"], y=y)
    x = np.eye(2)[cue]
    init_state = r_init.bit_generator.state
    batch_seed, tnoise_seed = int(r_batch.integers(2 ** 63)), int(r_tnoise.integers(2 ** 63))

    def reset():
        r_init.bit_generator.state = init_state  # the SAME init stream for every arm (matched)
        return r_init

    def cnt(samples, c):
        return count(samples, c, tmpl, tcls, dt, dcls, iou_min)

    def evals(sampler, arm):
        rich = [cnt(sampler(c, n_r, E.rng_for(seed, RICH, ARM_IDS[arm], 0, c)), c) for c in (0, 1)]
        test = [cnt(sampler(c, n_s, E.rng_for(seed, TEST, ARM_IDS[arm], 0, c)), c) for c in (0, 1)]
        return {"rich": rich, "test": test}

    out = {"seed": seed}
    for arm, zero in (("CV2", False), ("MK", True)):
        net = V.train_cv(V.init_cv(reset(), 2), x, t, p, np.random.default_rng(batch_seed),
                         np.random.default_rng(tnoise_seed), zero_z=zero)
        out[arm] = evals(lambda c, k, r: V.sample_cv(net, c, k, r), arm)
        mu, lv, _ = V.encode(net, t, x)
        out[arm]["kl_nats"] = float(V.kl(mu, lv).mean())
    z6 = {"kind": "enum", "dim": 6}
    net_z, _ = C.train_code(E.init_net(reset(), [8, 32, 64]), x, t, z6, p, np.random.default_rng(batch_seed),
                            np.random.default_rng(tnoise_seed))
    out["Z6-ENUM"] = evals(lambda c, k, r: C.sample_code(net_z, c, k, z6, r), "Z6-ENUM")
    net_j = train_jv(init_jv(reset()), x, t, p, np.random.default_rng(batch_seed), np.random.default_rng(tnoise_seed))
    out["JV"] = evals(lambda c, k, r: sample_jv(net_j, c, k, r), "JV")
    mu, lv, _ = V.encode(net_j, t, x)
    out["JV"]["kl_nats"] = float(V.kl(mu, lv).mean())
    out["MS"] = [cnt(speckle(E.rng_for(seed, M2_STREAM, ARM_IDS["MS"], 0, c), c, n_r, d), c) for c in (0, 1)]
    out["MC-T"] = [cnt(true_lines(E.rng_for(seed, M2_STREAM, ARM_IDS["MC-T"], 0, c), c, n_r, d), c) for c in (0, 1)]
    out["M2_true"] = E.score_cues([E.score(true_lines(E.rng_for(seed, M2_STREAM, ARM_IDS["TRUE"], 0, c), c, n_s, d),
                                           c, tmpl, tcls, iou_min) for c in (0, 1)])
    out["M2_coin"] = E.score_cues([E.score((E.rng_for(seed, M2_STREAM, ARM_IDS["COIN"], 0, c).random(
        size=(n_s, d["side"] ** 2)) < 0.5).astype(np.float64), c, tmpl, tcls, iou_min) for c in (0, 1)])
    return out


def main(argv):
    p = json.load(open(argv[1]))
    tmpl, tcls = E.templates(p)
    dt, dcls = dedup(tmpl, tcls)
    res = {"leaf": "goal:g5.49", "numpy": np.__version__, "params": p, "n_templates": int(len(tmpl)),
           "n_dedup": int(len(dt)), "seeds": [run_seed(s, p, tmpl, tcls, dt, dcls) for s in p["seeds"]]}
    res["peak_rss_kib"] = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    with open(argv[2], "w") as f:
        json.dump(res, f, indent=1, sort_keys=True)
        f.write("\n")


if __name__ == "__main__":
    main(sys.argv)
