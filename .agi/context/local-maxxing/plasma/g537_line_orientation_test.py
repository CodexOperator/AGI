"""goal:g5.37 pre-run tests: the data, the bank, the votes, and the falsifier on fake results.
No arm accuracy on the real task is computed here (pre-registration)."""
import numpy as np

import g537_falsifier as F
import g537_line_orientation as E


def test_lines_shape_and_classes():
    x, y = E.make_lines(np.random.default_rng(0), 200, 8, 1.0, 0.0, 10.0, 2.0)
    assert x.shape == (200, 64) and set(y.tolist()) <= {0, 1, 2, 3}
    assert (x.sum(1) > 0).all()  # every image carries a line


def test_bank_reads_clean_centred_lines():
    x, y = E.make_lines(np.random.default_rng(1), 400, 8, 1.0, 0.0, 0.0, 0.0)
    assert (E.bank_answer(x, 8, E.bar_bank(), 0) == y).mean() > 0.95
    assert (E.bank_answer(x, 8, E.bar_bank(), 1) == y).mean() < 0.05  # the mutant on clean data


def test_vote_ties_and_confidence():
    ans, conf = E.vote(np.array([[0, 1], [1, 1], [0, 2], [1, 3]]))
    assert ans.tolist() == [0, 1] and conf.tolist() == [0.5, 0.5]


def test_replay_is_byte_identical():
    p = {"sizes": [64, 16, 4], "sigmas": [0.0, 0.3], "taus": [1.0], "k_votes": 3, "ece_bins": 10,
         "seeds": [7], "train": {"steps": 20, "batch": 16, "lr": 0.01},
         "data": {"side": 8, "n_train": 64, "n_test": 32, "width": 1.0, "px_noise": 0.5,
                  "jitter_deg": 10.0, "max_offset": 2.0},
         "shift": {"width": 2.0, "px_noise": 1.0}}
    assert E.run_seed(7, p) == E.run_seed(7, p)
    assert E.run_seed(7, p)["n_params"] == 64 * 16 + 16 + 16 * 4 + 4


def fake(p_acc, p0_acc, t_acc, brot=0.1, spread=0.01):
    seeds = []
    for i in range(5):
        e = spread * (i - 2) / 2
        seeds.append({"P": {"0.0": {"acc": 0.7 + e}, "0.3": {"acc": p_acc + e}},
                      "P0": {"0.3": {"acc": p0_acc + e}}, "T": {"1.0": {"acc": t_acc + e}},
                      "B": {"acc": 0.8}, "B_rot": {"acc": brot}})
    return {"params": {"sigmas": [0.0, 0.3], "taus": [1.0]}, "seeds": seeds}


def test_falsifier_confirms_only_a_core_gain():
    assert F.judge(fake(0.9, 0.7, 0.7))["verdict"] == "CONFIRMED"


def test_falsifier_red1_no_gain():
    j = F.judge(fake(0.705, 0.6, 0.7))
    assert j["red1"] and j["verdict"] == "DISPROVED"


def test_falsifier_red2_regularizer():
    j = F.judge(fake(0.9, 0.895, 0.7))
    assert j["red2"] and not j["red1"] and j["verdict"] == "DISPROVED"


def test_mutant_not_red_is_void():
    assert F.judge(fake(0.9, 0.7, 0.7, brot=0.5))["verdict"] == "VOID"


def test_falsifier_red_at_mint(tmp_path):
    assert F.main(["x", str(tmp_path / "absent.json")]) == 2
