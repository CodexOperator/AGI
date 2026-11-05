"""goal:g5.41 pre-run tests: the blend split on hand cases, G-chamfer's trainer reducing to g5.39's at
lam 0, replay, Z's size, and the falsifier on fake results. No step-1 arm is scored on the real params."""
import json

import numpy as np

import g539_joint_samples as E
import g541_blend_race as R
import g541_falsifier as F

PARAMS = json.load(open(__file__.rsplit("/", 1)[0] + "/../../../../datasets/plasma/"
                        "2026-11-05-g5.41-blend-race/params.json"))


def test_split_hand_cases():
    t, cls = E.templates(PARAMS)
    a = t[cls == 0][265]   # j = 0, offset 0.5: a thin (8-pixel) class-0 line; at offset 0 a line is 2 rows thick
    b = t[cls == 2][265]   # its class-2 twin; the 15-pixel cross has best IoU 8/15 < 0.6
    d = t[cls == 1][len(t[cls == 1]) // 2]   # a class-1 template (wrong pair for cue 0)
    one = np.zeros(64); one[0] = 1
    s = np.vstack([a, np.maximum(a, b), one, d])
    r = R.split(s, 0, t, cls, (5, 3), (10, 3), sparse_px=4.0)
    assert (r["valid"], r["invalid"], r["blend"], r["sparse"], r["other"]) == (0.25, 3, 1, 1, 1)


def test_chamfer_trainer_reduces_to_g539_at_lam_zero():
    rng = np.random.default_rng(0)
    x = np.eye(2)[rng.integers(0, 2, size=64)]
    t = (rng.random((64, 64)) < 0.2).astype(np.float64)
    tr = {"steps": 25, "batch": 16, "lr": 0.01}
    n1 = E.train(E.init_net(np.random.default_rng(1), [2, 32, 64]), x, t, 2.0, 8, tr,
                 np.random.default_rng(2), np.random.default_rng(3))
    n2 = R.train_core(E.init_net(np.random.default_rng(1), [2, 32, 64]), x, t, "gauss", 2.0, 8, 0.0, True, tr,
                      np.random.default_rng(2), np.random.default_rng(3))
    for (w1, b1), (w2, b2) in zip(n1, n2):
        assert np.allclose(w1, w2, atol=1e-10) and np.allclose(b1, b2, atol=1e-10)


def tiny():
    p = json.loads(json.dumps(PARAMS))
    p.update({"seeds": [5], "sigmas": [2.0], "n_samples": 8})
    p["train"].update({"steps": 6})
    p["data"].update({"n_train": 32})
    return p


def test_replay_is_byte_identical_and_sizes():
    p = tiny()
    t, cls = E.templates(p)
    a, b = R.run_seed(5, p, t, cls), R.run_seed(5, p, t, cls)
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
    assert a["n_params"] == {"G": 2208, "Z": 2304}


def cell(score, valid=0.8, cov=1.0, blend=0.5):
    return {"score": score, "valid": valid, "coverage": cov, "blend_share": blend}


def fake(g=0.2, s=0.4, c=0.4, s_valid=0.8, c_valid=0.8, c_cov=0.95, s_blend=0.1, g_blend=0.6,
         m1s=0.0, m1c=0.0, m2t=1.0):
    seeds = []
    for _ in range(5):
        vt = lambda sc, **kw: {"val": cell(sc, **kw), "test": cell(sc, **kw)}
        seeds.append({"G": {"2.0": vt(g, blend=g_blend)}, "GC": {"2.0": vt(c, valid=c_valid, cov=c_cov)},
                      "GP": {"2.0": vt(0.1)}, "S": vt(s, valid=s_valid, blend=s_blend), "SC": vt(0.1), "Z": vt(0.1),
                      "MF": {"2.0": cell(0.0)}, "M1_S": cell(m1s), "M1_C": {"2.0": cell(m1c)},
                      "M2_true": cell(m2t), "M2_coin": cell(0.0, valid=0.0)})
    return {"params": {"sigmas": [2.0]}, "seeds": seeds}


def test_lines_prove_and_fail_on_their_own_text():
    j = F.judge({"blend_share": 0.6, "shares": {}}, fake())
    assert (j["S-OUT"], j["S-MECH"], j["G-CHAMFER"]) == ("PROVED", "PROVED", "PROVED")
    j = F.judge({"blend_share": 0.4, "shares": {}}, fake())
    assert j["S-MECH"] == "DISPROVED" and j["s_mech_red_at_pre_run"] and j["S-OUT"] == "PROVED"
    assert F.judge({"blend_share": 0.6, "shares": {}}, fake(s_valid=0.4))["S-OUT"] == "DISPROVED"
    assert F.judge({"blend_share": 0.6, "shares": {}}, fake(c_cov=0.8))["G-CHAMFER"] == "DISPROVED"
    assert F.judge({"blend_share": 0.6, "shares": {}}, fake(s_blend=0.7))["S-MECH"] == "DISPROVED"


def test_mutants_void_their_own_lines():
    j = F.judge({"blend_share": 0.6, "shares": {}}, fake(m1s=0.2))
    assert (j["S-OUT"], j["S-MECH"], j["G-CHAMFER"]) == ("VOID", "VOID", "PROVED")
    j = F.judge({"blend_share": 0.6, "shares": {}}, fake(m1c=0.2))
    assert (j["S-OUT"], j["G-CHAMFER"]) == ("PROVED", "VOID")
    j = F.judge({"blend_share": 0.6, "shares": {}}, fake(m2t=0.5))
    assert {j["S-OUT"], j["S-MECH"], j["G-CHAMFER"]} == {"VOID"}


def test_prediction_is_scored():
    assert F.judge({"blend_share": 0.6, "shares": {}}, fake(s=0.5, c=0.4))["prediction"]["came_true"]
    assert not F.judge({"blend_share": 0.4, "shares": {}}, fake(s=0.5, c=0.4))["prediction"]["came_true"]


def test_not_done_at_mint(tmp_path):
    assert F.main(["x", str(tmp_path / "a.json"), str(tmp_path / "b.json")]) == 2
