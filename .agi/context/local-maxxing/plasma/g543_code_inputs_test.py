"""goal:g5.43 pre-run tests: Z3-ENUM is g5.41's Z (trainer and sampler), the code table, Mz1's fixed code,
distinct valid images, replay, sizes, and every falsifier route on fake results. No arm is scored on the
real params here (pre-registration)."""
import json

import numpy as np

import g539_joint_samples as E
import g541_blend_race as R
import g543_code_inputs as C
import g543_falsifier as F

PARAMS = json.load(open(__file__.rsplit("/", 1)[0] + "/../../../../datasets/plasma/"
                        "2026-11-05-g5.43-code-inputs/params.json"))


def data(n=64, seed=0):
    rng = np.random.default_rng(seed)
    return np.eye(2)[rng.integers(0, 2, size=n)], (rng.random((n, 64)) < 0.2).astype(np.float64)


def test_code_table_is_g541s():
    assert (C.code_table(3) == R.CODES).all() and C.code_table(6).shape == (64, 6)


def test_z3_enum_is_g541s_z():
    x, t = data()
    p = {"k": 8, "win_window": 5, "train": {"steps": 20, "batch": 16, "lr": 0.01}}
    n1 = R.train_z(E.init_net(np.random.default_rng(1), [5, 32, 64]), x, t, p["train"], np.random.default_rng(2))
    n2, wins = C.train_code(E.init_net(np.random.default_rng(1), [5, 32, 64]), x, t, {"kind": "enum", "dim": 3}, p,
                            np.random.default_rng(2), np.random.default_rng(3))
    for (a, b), (c, d) in zip(n1, n2):
        assert np.array_equal(a, c) and np.array_equal(b, d)
    assert wins <= set(range(8)) and wins
    s1 = R.sample_z(n1, 0, 16, np.random.default_rng(9))
    s2 = C.sample_code(n2, 0, 16, {"kind": "enum", "dim": 3}, np.random.default_rng(9))
    assert np.array_equal(s1, s2)


def test_mz1_fixed_code_is_one_image():
    x, t = data()
    p = {"k": 8, "win_window": 5, "train": {"steps": 5, "batch": 16, "lr": 0.01}}
    for arm in ({"kind": "samp", "dim": 5}, {"kind": "cont", "dim": 3}, {"kind": "one", "dim": 3}):
        net, _ = C.train_code(E.init_net(np.random.default_rng(1), [2 + arm["dim"], 32, 64]), x, t, arm, p,
                              np.random.default_rng(2), np.random.default_rng(3))
        s = C.sample_code(net, 1, 64, arm, np.random.default_rng(4), fixed=True)
        assert (s == s[0]).all() and s.shape == (64, 64)


def test_mz6_mod8_has_at_most_8_codes():
    x, t = data()
    p = {"k": 8, "win_window": 5, "train": {"steps": 5, "batch": 16, "lr": 0.01}}
    arm = {"kind": "enum", "dim": 6}
    net, _ = C.train_code(E.init_net(np.random.default_rng(1), [8, 32, 64]), x, t, arm, p,
                          np.random.default_rng(2), np.random.default_rng(3))
    s = C.sample_code(net, 0, 64, arm, np.random.default_rng(5), mod=8)
    assert len({r.tobytes() for r in s}) <= 8


def test_distinct_valid_counts_unique_valid_images():
    t, cls = E.templates(PARAMS)
    a, b = t[cls == 0][265], t[cls == 2][265]
    s = np.vstack([a, a, b, np.zeros(64)])
    r = C.score_cue(s, 0, t, cls, (5, 3))
    assert r["distinct_valid"] == 2 and r["valid"] == 0.75


def tiny():
    p = json.loads(json.dumps(PARAMS))
    p.update({"seeds": [7], "sigmas_g": [2.0], "sigmas_g64": [4.0], "n_samples": 8, "win_window": 2})
    p["train"].update({"steps": 4})
    p["data"].update({"n_train": 32})
    return p


def test_replay_is_byte_identical_and_sizes():
    p = tiny()
    t, cls = E.templates(p)
    a, b = C.run_seed(7, p, t, cls), C.run_seed(7, p, t, cls)
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
    assert a["Z3-ENUM"]["n_params"] == 2304 and a["Z6-ENUM"]["n_params"] == 2400 and a["Z5-SAMP"]["n_params"] == 2368


def cell(score, valid=0.8, cov=0.95, dmin=20):
    c = {"score": score, "valid": valid, "coverage": cov, "distinct_valid_min": dmin, "distinct_valid_mean": dmin}
    return {"val": c, "test": c}


def fake(z3=0.8, z3s=0.6, z5=0.4, c3=0.3, z6=0.8, g=0.2, g64=0.3, z3_valid=0.8, z6_dmin=20, mz1=0.0, mz2=0.05,
         m2t=1.0, mz1_arms=F.CLAIMED, mz6=8):
    seeds = []
    for _ in range(5):
        s = {"G": {"2.0": cell(g)}, "G64": {"4.0": cell(g64)}, "Z3-ENUM": cell(z3, valid=z3_valid),
             "Z3-SAMP": cell(z3s), "Z5-SAMP": cell(z5), "C3-SAMP": cell(c3), "Z6-ENUM": cell(z6, dmin=z6_dmin),
             "MZ2": cell(0.0, valid=mz2), "M2_true": {"score": m2t}, "M2_coin": {"valid": 0.0}}
        for a in F.CLAIMED + ("MZ2",):
            s[a]["mz1_fixed"] = {"score": mz1 if a in mz1_arms else 0.0}
        s["Z6-ENUM"]["mz6_mod8"] = {"distinct_valid_min": mz6, "cues": [{"distinct_valid": mz6}, {"distinct_valid": mz6}]}
        seeds.append(s)
    return {"params": {"sigmas_g": [2.0], "sigmas_g64": [4.0]}, "seeds": seeds}


LINES = ("L-REP", "L-Z", "L-ENUM", "L-STATES", "L-DISC", "L-Z6")


def test_all_lines_prove():
    assert {F.judge(fake())[k] for k in LINES} == {"PROVED"}


def test_gate_red_leaves_line_3_unread_only():
    j = F.judge(fake(z3_valid=0.4))
    assert (j["L-REP"], j["L-Z"], j["L-Z6"]) == ("DISPROVED", "DISPROVED", "PROVED")
    assert {j[k] for k in ("L-ENUM", "L-STATES", "L-DISC")} == {"NOT_READ"}


def test_line_reds():
    assert F.judge(fake(z3s=0.78))["L-ENUM"] == "DISPROVED"
    assert F.judge(fake(z5=0.58))["L-STATES"] == "DISPROVED"
    assert F.judge(fake(c3=0.7))["L-DISC"] == "DISPROVED"
    assert F.judge(fake(z6_dmin=15))["L-Z6"] == "DISPROVED"
    assert F.judge(fake(g=0.79))["L-Z"] == "DISPROVED"


def test_mutants_void_their_lines():
    j = F.judge(fake(mz1=0.2))  # Mz1 never guards L-REP, L-Z or L-Z6; it VOIDs the pair lines
    assert (j["L-REP"], j["L-Z"], j["L-Z6"]) == ("PROVED", "PROVED", "PROVED")
    assert {j[k] for k in ("L-ENUM", "L-STATES", "L-DISC")} == {"VOID"}
    j = F.judge(fake(mz1=0.2, mz1_arms=("C3-SAMP",)))  # pair-wise: only L-DISC holds C3-SAMP
    assert (j["L-ENUM"], j["L-STATES"], j["L-DISC"]) == ("PROVED", "PROVED", "VOID")
    j = F.judge(fake(mz6=16))
    assert (j["L-Z6"], j["L-Z"]) == ("VOID", "PROVED")
    j = F.judge(fake(mz2=0.3))
    assert (j["L-ENUM"], j["L-STATES"]) == ("VOID", "PROVED")
    assert {F.judge(fake(m2t=0.5))[k] for k in LINES} == {"VOID"}


def test_not_done_at_mint(tmp_path):
    assert F.main(["x", str(tmp_path / "absent.json")]) == 2
