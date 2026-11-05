"""goal:g5.39 pre-run tests: the templates, the scorer on hand cases, the replay, and the falsifier on
fake results. No arm score and no mutant on the real params is computed here (pre-registration)."""
import json

import numpy as np

import g539_falsifier as F
import g539_joint_samples as E

PARAMS = json.load(open(__file__.rsplit("/", 1)[0] + "/../../../../datasets/plasma/"
                        "2026-11-05-g5.39-joint-samples/params.json"))


def test_templates_are_the_pinned_2108():
    t, cls = E.templates(PARAMS)
    assert t.shape == (2108, 64) and np.bincount(cls).tolist() == [527] * 4
    assert (t.sum(1) > 0).all()


def test_scorer_hand_cases():
    t, cls = E.templates(PARAMS)
    a = t[cls == 0][:1]
    b = t[cls == 2][:1]
    both = np.vstack([a, b])
    assert E.score(both, 0, t, cls, (5, 3)) == {"valid": 1.0, "coverage": 1.0, "score": 1.0}
    assert E.score(both, 1, t, cls, (5, 3))["valid"] == 0.0          # right lines, wrong cue
    assert E.score(np.vstack([a, a]), 0, t, cls, (5, 3))["coverage"] == 0.0  # one class only
    assert E.score(np.zeros((2, 64)), 0, t, cls, (5, 3))["valid"] == 0.0     # an empty image
    # the integer line: 3 of 5 pixels shared exactly on the boundary is VALID
    one = np.zeros((1, 64)); one[0, :5] = 1
    tm = np.zeros((1, 64)); tm[0, :3] = 1
    assert E.score(np.vstack([one]), 0, tm, np.array([0]), (5, 3))["valid"] == 1.0
    tm[0, :3] = 0; tm[0, 1:3] = 1; tm[0, 5] = 1   # inter 2, union 6: below the line
    assert E.score(one, 0, tm, np.array([0]), (5, 3))["valid"] == 0.0


def tiny():
    p = json.loads(json.dumps(PARAMS))
    p.update({"seeds": [3], "sigmas": [1.0], "taus": [1.0], "n_samples": 8})
    p["train"].update({"steps": 10})
    p["data"].update({"n_train": 32})
    return p


def test_replay_is_byte_identical_and_params_match():
    p = tiny()
    t, cls = E.templates(p)
    a, b = E.run_seed(3, p, t, cls), E.run_seed(3, p, t, cls)
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
    assert a["n_params"] == 2208


def fake(p_scores, t_scores, p_valid=0.8, m1=0.0, m2_true=1.0, m2_coin=0.0):
    seeds = []
    for ps, ts in zip(p_scores, t_scores):
        cell = lambda s, v: {"score": s, "valid": v, "coverage": 1.0}
        seeds.append({"P": {"1.0": {"val": cell(ps, p_valid), "test": cell(ps, p_valid)}},
                      "T": {"1.0": {"val": cell(ts, 1.0), "test": cell(ts, 1.0)}},
                      "MF": {"1.0": cell(0.0, 1.0)}, "M1": {"1.0": cell(m1, 1.0)},
                      "M2_true": cell(m2_true, 1.0), "M2_coin": cell(0.0, m2_coin)})
    return {"params": {"sigmas": [1.0], "taus": [1.0]}, "seeds": seeds}


def test_proved_only_on_a_paired_gain_with_lines():
    assert F.judge(fake([0.6] * 5, [0.4] * 5))["verdict"] == "PROVED"


def test_red_one_seed_not_positive():
    j = F.judge(fake([0.6, 0.6, 0.6, 0.6, 0.3], [0.4] * 5))
    assert not j["c1_paired"] and j["verdict"] == "DISPROVED"


def test_red_mean_delta_too_small():
    assert F.judge(fake([0.43] * 5, [0.4] * 5))["verdict"] == "DISPROVED"


def test_red_samples_not_lines():
    j = F.judge(fake([0.6] * 5, [0.4] * 5, p_valid=0.4))
    assert not j["c2_valid"] and j["verdict"] == "DISPROVED"


def test_void_on_either_mutant():
    assert F.judge(fake([0.6] * 5, [0.4] * 5, m1=0.2))["verdict"] == "VOID"
    assert F.judge(fake([0.6] * 5, [0.4] * 5, m2_true=0.8))["verdict"] == "VOID"
    assert F.judge(fake([0.6] * 5, [0.4] * 5, m2_coin=0.1))["verdict"] == "VOID"


def test_red_at_mint(tmp_path):
    assert F.main(["x", str(tmp_path / "absent.json")]) == 2
