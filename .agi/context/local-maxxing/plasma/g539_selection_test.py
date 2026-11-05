"""SM's gate via thought-master [fix] 12:41Z 11-05: the closed falsifier tests used one sigma and one tau with
val == test, so select-on-validation could never go red. These cases make val and test disagree.
g537 / g539 falsifiers are imported, never edited."""
import g537_falsifier as F37
import g539_falsifier as F39


def cell(val, test, valid=0.8):
    return {"val": {"score": val, "valid": valid, "coverage": 1.0},
            "test": {"score": test, "valid": valid, "coverage": 1.0}}


def fake39(p_cells, t_cells):
    seeds = []
    for _ in range(5):
        seeds.append({"P": p_cells, "T": t_cells, "M1": {s: {"score": 0.0} for s in p_cells},
                      "MF": {s: {"score": 0.0, "valid": 0.0, "coverage": 0.0} for s in p_cells},
                      "M2_true": {"score": 1.0}, "M2_coin": {"valid": 0.0}})
    return {"params": {"sigmas": [float(s) for s in p_cells], "taus": [float(t) for t in t_cells]}, "seeds": seeds}


def test_g539_picks_sigma_and_tau_on_val_not_test():
    # sigma 0.3 is best on val but worst on test; tau 1.0 is best on val, tau 2.0 best on test
    j = F39.judge(fake39({"0.3": cell(0.9, 0.1), "1.0": cell(0.5, 0.8)},
                         {"1.0": cell(0.4, 0.0), "2.0": cell(0.1, 0.7)}))
    assert (j["sigma_star"], j["tau_star"]) == ("0.3", "1.0")
    assert j["P_test"] == [0.1] * 5 and j["T_test"] == [0.0] * 5  # the TEST scores of the VAL picks


def test_g539_selection_on_test_would_have_flipped_the_verdict():
    # val-best sigma has a test score below T's; a test-picked sigma would have PROVED
    j = F39.judge(fake39({"0.3": cell(0.9, 0.1), "1.0": cell(0.5, 0.8)},
                         {"1.0": cell(0.4, 0.3), "2.0": cell(0.1, 0.2)}))
    assert j["sigma_star"] == "0.3" and j["verdict"] == "DISPROVED"
    j_test = F39.judge(fake39({"0.3": cell(0.1, 0.1), "1.0": cell(0.8, 0.8)},
                              {"1.0": cell(0.3, 0.3), "2.0": cell(0.2, 0.2)}))
    assert j_test["sigma_star"] == "1.0" and j_test["verdict"] == "PROVED"


def fake37(p, p0, t, b_rot=0.1):
    seeds = []
    for i in range(5):
        e = 0.002 * (i - 2)
        seeds.append({"P": {k: {"acc": v + e} for k, v in p.items()}, "P0": {k: {"acc": v + e} for k, v in p0.items()},
                      "T": {k: {"acc": v + e} for k, v in t.items()}, "B": {"acc": 0.8}, "B_rot": {"acc": b_rot}})
    return {"params": {"sigmas": [float(k) for k in p], "taus": [float(k) for k in t]}, "seeds": seeds}


def test_g537_selects_on_the_shifted_test_by_registration():
    # g5.37 has NO validation stream: sigma* and tau* are picked on the shifted test, as registered in
    # 20bbea41bb and disclosed in its [complete]. This pins that behaviour with several sigmas and taus.
    j = F37.judge(fake37({"0.0": 0.70, "0.1": 0.72, "0.3": 0.90, "1.0": 0.80},
                         {"0.1": 0.71, "0.3": 0.70, "1.0": 0.80}, {"0.5": 0.70, "1.0": 0.75, "2.0": 0.72}))
    assert (j["sigma_star"], j["tau_star"]) == ("0.3", "1.0")
    assert not j["red1"] and not j["red2"] and j["verdict"] == "CONFIRMED"
