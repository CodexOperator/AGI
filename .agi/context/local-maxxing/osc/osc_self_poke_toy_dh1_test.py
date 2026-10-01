"""Tests for osc_self_poke_toy_dh1.py (CORRECTIVE DH.1 of hypothesis:lm-self-poke-harness-separates-real-from-sham-on-the-
grokked-toy): the random sets, the split read from params, the told flag kept out of the trial dict, the two-sided call,
the edit's dose, imports not copies, and a reduced end-to-end smoke into a tmp dir. CPU, seconds. Run as osc_self_poke_toy_test.py."""
import inspect
import json
import os
import sys

import pytest
import safetensors.torch as ST

torch = pytest.importorskip("torch")
np = pytest.importorskip("numpy")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_self_poke_toy as T  # noqa: E402
import osc_self_poke_toy_dh1 as D  # noqa: E402
import paths  # noqa: E402

P = json.load(open(os.path.join(paths.get_local("osc_self_poke_toy_dh1_dir"), "params.json")))
CK = os.path.join(paths.get_local(P["pc_dir_cell"]), "model.pt")
Pc = json.load(open(os.path.join(paths.get_local(P["pc_dir_cell"]), "params.json")))


def build_ckpt(path):   # a checkpoint THIS test builds (seeded random-init toy, safetensors): the context fence refuses torch.load
    ST.save_file({k: v.contiguous() for k, v in D.T.PC.make(Pc, 0).state_dict().items()}, str(path))
    return str(path)


@pytest.fixture
def ckpt(tmp_path, allow_model_load):   # declared to the model fence; S.restore reads it back by its magic bytes
    allow_model_load(tmp_path)
    return build_ckpt(tmp_path / "model.pt")


def test_1_random_sets_are_20_distinct_size_128_deterministic_draws_over_all_512():
    a, b = D.rand_sets(P, 512), D.rand_sets(P, 512)
    assert a == b and len(a) == 20 == P["n_random"]
    assert all(len(v) == 128 == len(set(v)) and v == sorted(v) and 0 <= v[0] and v[-1] < 512 for v in a.values())
    assert len({tuple(v) for v in a.values()}) == 20
    assert D.rand_sets({**P, "set_seed_base": 1}, 512) != a


def test_2_the_split_comes_from_params_and_partitions_the_families():
    assert sorted(P["bearing"] + P["passengers"]) == sorted(P["families"]) and not set(P["bearing"]) & set(P["passengers"])
    src = inspect.getsource(D)
    assert 'P["bearing"]' in src and 'P["passengers"]' in src and '["families"][:' not in src


def test_3_the_told_flag_is_stripped_before_the_trial_reaches_the_forward_pass(ckpt):
    assert 't.keys() - {"told"}' in inspect.getsource(T.main)
    seen = []
    model = D.T.PC.make(Pc, 0).eval()
    T.restore(model, ckpt)
    X = D.T.PC.data(Pc)[0]
    t = {"trial": "t0", "family": 5, "s": 0.0, "arm": "REAL", "probe_seed": 3}
    T.run_trial(model, ckpt, X, t, {5: [0, 1]}, 256, consent=lambda x: seen.append(dict(x)) or True)
    assert seen and "told" not in seen[0]


def test_4_the_call_is_two_sided_about_the_median_reference():
    sc = T.score([{"trial": "lo", "r": 0.0}, {"trial": "mid", "r": 0.005}, {"trial": "hi", "r": 0.01}], 0.005, 0.001)
    assert [sc[k]["edited"] for k in ("lo", "mid", "hi")] == [True, False, True]


def test_5_an_edit_scales_exactly_its_columns_by_the_dose_and_restores(ckpt):
    model = D.T.PC.make(Pc, 0).eval()
    sha0, w0, ids = T.restore(model, ckpt), None, [3, 7, 100]
    w0 = model.w_out.weight.detach().clone()
    for s in P["scales"]:
        T.edit(model, ids, s)
        w = model.w_out.weight.detach()
        assert torch.equal(w[:, ids], w0[:, ids] * s)
        rest = [i for i in range(w.shape[1]) if i not in ids]
        assert torch.equal(w[:, rest], w0[:, rest])
        assert T.restore(model, ckpt) == sha0


def test_6_the_corrective_script_imports_run_2s_helpers_and_does_not_copy_them():
    src = inspect.getsource(D)
    for name in ("def edit(", "def restore(", "def readout(", "def probe(", "def families(", "def score(", "class OneLayer"):
        assert name not in src, name
    assert D.T is T


def test_7_reduced_end_to_end_smoke_writes_the_results_shape(tmp_path, monkeypatch, allow_model_load):
    small = {**P, "reps": 2, "n_random": 2, "scales": [0.0, 0.5], "box_min_avail_mib": 0, "box_max_psi_some_avg10": 1e9}
    out, pc = tmp_path / "out", tmp_path / "pc"
    out.mkdir(), pc.mkdir()
    (out / "params.json").write_text(json.dumps(small))
    (pc / "params.json").write_text(json.dumps(Pc))
    build_ckpt(pc / "model.pt"), allow_model_load(tmp_path)
    ids, lo = {}, 0   # the pipeline on a random-init toy finds no families: stub the (separately tested) family finder
    for k, n in P["family_sizes"].items():
        ids[int(k)], lo = list(range(lo, lo + n)), lo + n
    monkeypatch.setattr(D.T, "families", lambda model, Pc: ids)
    real = paths.get_local
    where = {"osc_self_poke_toy_dh1_dir": str(out), P["pc_dir_cell"]: str(pc)}
    monkeypatch.setattr(paths, "get_local", lambda k: where.get(k) or real(k))
    D.main()
    R = json.load(open(out / "results.json"))
    assert R["void"] is True and R["verdict"] == "void"   # the tmp params are untracked: the committed-params guard fires
    assert {"k5", "k45", "k1", "k34", "rand0", "rand1"} == set(R["dr"])
    raw = [json.loads(l) for l in open(out / "raw.jsonl")]
    assert len(raw) == 6 * 2 * 2 and {"set", "s", "seed", "r", "dr", "call"} == set(raw[0])   # 6 sets x 2 scales x 2 seeds
    assert abs(sum(x["dr"] for x in raw if x["set"] == "k5" and x["s"] == 0.0) / 2 - R["dr"]["k5"]) < 1e-12
    assert isinstance(R["c5a"], bool) and isinstance(R["c5b"], bool)
    assert set(R["c3"]["det_rate_s0"]) == {"5", "45", "1", "34"} and 0 <= R["c3"]["sham_rate"] <= 1
    assert set(R["unscored"]["detect_by_scale"]["k5"]) == {"0.0", "0.5"} and -1 <= R["unscored"]["spearman_dr_norm"] <= 1
    with pytest.raises(SystemExit):
        D.main()   # a finished session is never overwritten
