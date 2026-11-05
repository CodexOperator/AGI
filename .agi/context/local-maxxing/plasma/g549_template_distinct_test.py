"""goal:g5.49 pre-run tests: the dedup is plasma's 836, the counter on hand cases and against speckle, JV's
gradients against finite differences, replay, and every falsifier route on fake results. No CV arm is scored
on the real seeds here (pre-registration)."""
import copy
import json

import numpy as np

import g539_joint_samples as E
import g543_code_inputs as C
import g549_falsifier as F
import g549_template_distinct as T

PARAMS = json.load(open(__file__.rsplit("/", 1)[0] + "/../../../../datasets/plasma/"
                        "2026-11-05-g5.49-template-distinct/params.json"))
TM, TC = E.templates(PARAMS)
DT, DC = T.dedup(TM, TC)


def test_dedup_is_836_and_keeps_first():
    assert len(DT) == 836 and np.bincount(DC).tolist() == [139, 279, 139, 279]
    assert np.array_equal(DT[0], TM[0])
    assert len({(int(k), r.astype(np.uint8).tobytes()) for r, k in zip(DT, DC)}) == 836


def test_counter_hand_cases():
    a = DT[DC == 0][10]
    b = DT[DC == 2][10]
    s = np.vstack([a, a, b, np.zeros(64)])
    r = T.count(s, 0, TM, TC, DT, DC, (5, 3))
    assert (r["templates"], r["images"], r["valid"]) == (2, 2, 0.75)


def test_counter_is_not_fooled_by_speckle_but_images_are():
    r = T.count(T.speckle(np.random.default_rng(1), 0, 512, PARAMS["data"]), 0, TM, TC, DT, DC, (5, 3))
    assert r["templates"] <= 16 and r["images"] >= 100


def test_jv_gradients_match_finite_differences():
    rng = np.random.default_rng(0)
    x = np.eye(2)[rng.integers(0, 2, size=5)]
    t = (rng.random((5, 64)) < 0.2).astype(np.float64)
    eps = rng.normal(size=(5, 2))
    net = T.init_jv(np.random.default_rng(1))
    codes = C.code_table(3)
    _, g = T.jv_loss_and_grads(net, x, t, eps, 1.0, codes)
    h = 1e-6
    for k in net:
        flat = net[k].reshape(-1)
        for i in np.random.default_rng(2).choice(flat.size, size=min(4, flat.size), replace=False):
            up, dn = copy.deepcopy(net), copy.deepcopy(net)
            up[k].reshape(-1)[i] += h
            dn[k].reshape(-1)[i] -= h
            num = (T.jv_loss_and_grads(up, x, t, eps, 1.0, codes)[0] - T.jv_loss_and_grads(dn, x, t, eps, 1.0, codes)[0]) / (2 * h)
            assert abs(num - g[k].reshape(-1)[i]) < 1e-5 * max(1.0, abs(num)), k


def test_replay_is_byte_identical():
    p = json.loads(json.dumps(PARAMS))
    p.update({"seeds": [11], "n_samples": 8, "n_rich": 16, "win_window": 2})
    p["train"].update({"steps": 3})
    p["data"].update({"n_train": 32})
    a, b = T.run_seed(11, p, TM, TC, DT, DC), T.run_seed(11, p, TM, TC, DT, DC)
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)


def cell(valid=0.8, cov=0.95, t=100, im=150, score=0.6):
    return {"valid": valid, "coverage": cov, "templates": t, "images": im, "score": score}


def fake(cv=None, ms_t=5, mct=200, mk_t=3, mk_s=0.0, m2t=1.0, rss=500000, seeds=(54901, 54902, 54903, 54904, 54905)):
    out = []
    for i, s in enumerate(seeds):
        c = (cv or {}).get(i, cell())
        out.append({"seed": s, "CV2": {"rich": [c, cell()], "test": [c, c]},
                    "MK": {"rich": [cell(t=mk_t)] * 2, "test": [cell(score=mk_s)] * 2},
                    "Z6-ENUM": {"rich": [cell(t=50)] * 2}, "JV": {"rich": [cell(valid=0.9, t=120)] * 2},
                    "MS": [cell(t=ms_t, im=300)] * 2, "MC-T": [cell(t=mct)] * 2,
                    "M2_true": {"score": m2t}, "M2_coin": {"valid": 0.0}})
    return {"seeds": out, "peak_rss_kib": rss}


def j(r):
    return F.judge(r, prior_seeds={54301, 54601})["L-RICH-T"]


def test_routes():
    assert j(fake()) == "PROVED"
    assert j(fake(cv={3: cell(t=64)})) == "DISPROVED"
    assert j(fake(cv={0: cell(cov=0.89)})) == "DISPROVED"
    assert j(fake(ms_t=16)) == "PROVED" and j(fake(ms_t=17)) == "VOID" and j(fake(mct=119)) == "VOID" and j(fake(m2t=0.5)) == "VOID"
    assert j(fake(mk_t=17)) == "VOID"
    assert j(fake(cv={3: cell(t=60)}, mk_t=17)) == "DISPROVED"  # MK never VOIDs a RED
    assert j(fake(rss=4 * 1024 * 1024)) == "VOID"
    assert j(fake(seeds=(54601, 54902, 54903, 54904, 54905))) == "VOID"
    assert F.judge(fake(), prior_seeds=set())["jv_prediction"]["came_true"]


def test_real_seeds_are_new():
    prior = set()
    for f in F.PRIOR:
        prior |= set(json.load(open(f))["seeds"])
    assert not set(PARAMS["seeds"]) & prior


def test_not_done_at_mint(tmp_path):
    assert F.main(["x", str(tmp_path / "absent.json")]) == 2
