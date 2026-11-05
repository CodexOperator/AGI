"""goal:g5.46 pre-run tests: the CV's gradients against finite differences, MK leaves W_z and the encoder at
init, replay, sizes, the distinct counter, and every falsifier route on fake results. No arm is scored on
the real params here (pre-registration)."""
import copy
import json

import numpy as np

import g539_joint_samples as E
import g546_cvae as V
import g546_falsifier as F

PARAMS = json.load(open(__file__.rsplit("/", 1)[0] + "/../../../../datasets/plasma/"
                        "2026-11-05-g5.46-cvae/params.json"))


def batch(n=6, seed=0):
    rng = np.random.default_rng(seed)
    return np.eye(2)[rng.integers(0, 2, size=n)], (rng.random((n, 64)) < 0.2).astype(np.float64), rng


def test_gradients_match_finite_differences():
    x, t, rng = batch()
    net = V.init_cv(np.random.default_rng(1), 2)
    eps = rng.normal(size=(len(x), 2))
    _, g = V.loss_and_grads(net, x, t, eps, 1.0)
    h = 1e-6
    for k in ("w1", "b1", "wz", "w2", "b2", "we1", "be1", "we2", "be2"):
        flat = net[k].reshape(-1)
        for i in np.random.default_rng(2).choice(flat.size, size=min(4, flat.size), replace=False):
            up, dn = copy.deepcopy(net), copy.deepcopy(net)
            up[k].reshape(-1)[i] += h
            dn[k].reshape(-1)[i] -= h
            num = (V.loss_and_grads(up, x, t, eps, 1.0)[0] - V.loss_and_grads(dn, x, t, eps, 1.0)[0]) / (2 * h)
            assert abs(num - g[k].reshape(-1)[i]) < 1e-5 * max(1.0, abs(num)), k


def test_mk_trains_neither_wz_nor_the_encoder():
    x, t, _ = batch(64)
    p = {"beta": 1.0, "train": {"steps": 10, "batch": 16, "lr": 0.01}}
    net0 = V.init_cv(np.random.default_rng(1), 2)
    net = V.train_cv(copy.deepcopy(net0), x, t, p, np.random.default_rng(2), np.random.default_rng(3), zero_z=True)
    for k in ("wz", "we1", "be1", "we2", "be2"):
        assert np.array_equal(net[k], net0[k]), k
    assert not np.array_equal(net["w2"], net0["w2"])


def test_distinct_counter():
    t, cls = E.templates(PARAMS)
    a, b = t[cls == 0][265], t[cls == 2][265]
    assert V.distinct_valid(np.vstack([a, a, b, np.zeros(64)]), 0, t, cls, (5, 3)) == 2


def tiny():
    p = json.loads(json.dumps(PARAMS))
    p.update({"seeds": [9], "n_samples": 8, "n_rich": 16, "win_window": 2})
    p["train"].update({"steps": 4})
    p["data"].update({"n_train": 32})
    return p


def test_replay_is_byte_identical_and_sizes():
    p = tiny()
    t, cls = E.templates(p)
    a, b = V.run_seed(9, p, t, cls), V.run_seed(9, p, t, cls)
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
    assert a["CV2"]["n_params"] == 2208 + 64 + (66 * 16 + 16 + 16 * 4 + 4)
    assert a["CV1"]["n_params"] == 2208 + 32 + (66 * 16 + 16 + 16 * 2 + 2)


def cell(valid=0.8, cov=0.95, score=0.7, d64=20, rich=(100, 100), kl=1.0, split=(10, 5, 2)):
    c = {"valid": valid, "coverage": cov, "score": score, "distinct_valid_min": d64}
    return {"val": c, "test": c, "rich_distinct": list(rich), "kl_nats": kl,
            "split": {"blend": split[0], "sparse": split[1], "other": split[2]}}


def fake(cv=None, mk=None, mc=(200, 200), m2t=1.0):
    seeds = []
    for i in range(5):
        s = {a: cell() for a in ("CV1", "CV4", "Z3-ENUM")}
        s["CV2"] = (cv or {}).get(i, cell())
        s["MK"] = mk or cell(score=0.0, rich=(3, 4))
        s["MC_distinct"] = list(mc)
        s["M2_true"], s["M2_coin"] = {"score": m2t}, {"valid": 0.0}
        seeds.append(s)
    return {"seeds": seeds}


def test_lines_prove():
    j = F.judge(fake())
    assert (j["CV-OUT"], j["L-RICH"]) == ("PROVED", "PROVED") and j["prediction_blend_largest"]["came_true"]


def test_reds():
    assert F.judge(fake(cv={2: cell(d64=13)}))["CV-OUT"] == "DISPROVED"
    assert F.judge(fake(cv={2: cell(kl=0.005)}))["CV-OUT"] == "DISPROVED"
    assert F.judge(fake(cv={2: cell(rich=(64, 90))}))["L-RICH"] == "DISPROVED"
    j = F.judge(fake(cv={1: cell(valid=0.4)}))
    assert j["L-RICH"] == "DISPROVED" and j["CV-OUT"] == "PROVED"  # CV-OUT reads the MEAN valid


def test_mutants_void_their_lines():
    j = F.judge(fake(mk=cell(score=0.0, rich=(3, 20))))
    assert (j["CV-OUT"], j["L-RICH"]) == ("VOID", "VOID")
    # leaf v2: MK guards a PROVED read only; a RED stands even if MK fails
    j = F.judge(fake(cv={2: cell(d64=13, rich=(10, 10))}, mk=cell(score=0.3, rich=(30, 30))))
    assert (j["CV-OUT"], j["L-RICH"]) == ("DISPROVED", "DISPROVED")
    j = F.judge(fake(cv={2: cell(rich=(10, 10))}, mc=(100, 200)))
    assert j["L-RICH"] == "VOID"  # MC VOIDs L-RICH either way
    j = F.judge(fake(mc=(149, 200)))
    assert (j["CV-OUT"], j["L-RICH"]) == ("PROVED", "VOID")
    j = F.judge(fake(m2t=0.5))
    assert (j["CV-OUT"], j["L-RICH"]) == ("VOID", "VOID")


def test_not_done_at_mint(tmp_path):
    assert F.main(["x", str(tmp_path / "absent.json")]) == 2
