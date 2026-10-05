"""Tests for osc_self_poke_toy.py (hypothesis:lm-self-poke-harness-separates-real-from-sham-on-the-grokked-toy TESTS 1-7).
CPU, seconds. Run (the torch venv has no pytest; borrow a pytest dir):
  PYTHONPATH="$(python3 .agi/context/local-maxxing/paths.py osc_test_pythonpath):<dir holding pytest>" \
  "$(python3 .agi/context/local-maxxing/paths.py ml_python)" -m pytest osc_self_poke_toy_test.py -q --basetemp /tmp/<dir>
"""
import inspect
import json
import os
import sys

import pytest
pytest.importorskip('safetensors')  # collection skip, not an error, when the ml venv is absent
pytest.importorskip('torch')
import safetensors.torch as ST

torch = pytest.importorskip("torch")
np = pytest.importorskip("numpy")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_neuron_period_pc as PC  # noqa: E402
import osc_self_poke_toy as S  # noqa: E402
import paths  # noqa: E402

P = json.load(open(os.path.join(paths.get_local("osc_self_poke_toy_dir"), "params.json")))
PCD = paths.get_local(P["pc_dir_cell"])
CK, Pc = os.path.join(PCD, "model.pt"), json.load(open(os.path.join(PCD, "params.json")))
N = P["probe_size"]


@pytest.fixture
def ckpt(tmp_path, allow_model_load):
    """The context suite's model fence refuses torch.load's unpickler (it carries no path to declare): the test builds ITS OWN
    checkpoint (a seeded random-init toy, safetensors) in tmp, declares it, and S.restore reads it back by its magic bytes."""
    ST.save_file({k: v.contiguous() for k, v in PC.make(Pc, 0).state_dict().items()}, str(tmp_path / "model.pt"))
    allow_model_load(tmp_path)
    return str(tmp_path / "model.pt")


@pytest.fixture
def world(ckpt):
    model = PC.make(Pc, 1).eval()   # a different init than the checkpoint: restore must overwrite every weight
    fams, lo = {}, 0
    for k, n in P["family_sizes"].items():   # disjoint stand-in families with the registered sizes (the real ones: test 1b)
        fams[int(k)], lo = list(range(lo, lo + n)), lo + n
    return model, S.restore(model, ckpt), PC.data(Pc)[0], fams


def test_1_edit_then_restore_returns_the_state_sha(world, ckpt):
    model, sha0, X, fams = world
    S.edit(model, fams[5], 0.0)
    assert S.state_sha(model) != sha0
    assert S.restore(model, ckpt) == sha0
    assert not torch.equal(PC.make(Pc, 1).w_out.weight, model.w_out.weight)   # restore replaced the other init


def test_1b_the_real_checkpoint_pin_and_the_committed_family_sizes_match_the_pre_registration():
    assert S.sha_file(CK) == P["pc_model_sha256"] and S.sha_file(os.path.join(PCD, "params.json")) == P["pc_params_sha256"]
    R = json.load(open(os.path.join(paths.get_local("osc_self_poke_toy_dir"), "results.json")))   # the run's own recomputation
    assert {str(k): R["family_sizes"][str(k)] for k in P["families"]} == P["family_sizes"] and R["void"] is False


def test_2_scale_one_leaves_the_logits_bit_identical(world, ckpt):
    model, sha0, X, fams = world
    xb = S.probe(X, 5, N)
    with torch.no_grad():
        before = model(xb).clone()
    S.edit(model, fams[5], 1.0)
    with torch.no_grad():
        assert torch.equal(model(xb), before)
    S.restore(model, ckpt)


def test_3_told_reaches_no_computation():
    for fn in (S.PC.OneLayer.forward, S.readout, S.probe, S.edit, S.restore, S.run_trial):
        assert "told" not in inspect.signature(fn).parameters, fn
    src = inspect.getsource(S.run_trial) + inspect.getsource(S.readout) + inspect.getsource(S.edit)
    assert 'told' not in src.replace("the told flag is bookkeeping", "")


def test_4_a_declining_consent_stub_leaves_the_trial_unedited_and_logs_it(world, ckpt):
    model, sha0, X, fams = world
    t = {"trial": "t000", "family": 5, "s": 0.0, "arm": "REAL", "told": True, "probe_seed": 7}
    r0, _ = S.run_trial(model, ckpt, X, {**t, "arm": "SHAM"}, fams, N)
    r, rec = S.run_trial(model, ckpt, X, t, fams, N, consent=lambda t: False)
    assert r == r0 and rec["declined"] is True and rec["edit_applied"] is False
    r, rec = S.run_trial(model, ckpt, X, t, fams, N)
    assert r != r0 and rec["edit_applied"] is True and rec["consent"] == "n/a (toy)" and rec["restore_sha"] == sha0


def test_5_the_scorer_refuses_a_key_column_and_the_debrief_follows_the_scores(tmp_path):
    with pytest.raises(ValueError, match="arm"):
        S.score([{"trial": "t000", "r": 0.1, "arm": "REAL"}], 0.0, 0.05)
    sc = S.score([{"trial": "t000", "r": 0.2}, {"trial": "t001", "r": 0.0}], 0.0, 0.1)
    assert sc == {"t000": {"r": 0.2, "edited": True}, "t001": {"r": 0.0, "edited": False}}
    rows, recs = [{"trial": "t000", "arm": "REAL"}], {"t000": {"restore_sha": "x"}}
    for n in ("reports.jsonl",):
        (tmp_path / n).write_text("{}\n")
    with pytest.raises(AssertionError):
        S.debrief(str(tmp_path), rows, recs)
    (tmp_path / "scores.json").write_text(json.dumps(sc))
    head = S.debrief(str(tmp_path), rows, recs)
    first = json.loads((tmp_path / "debrief.jsonl").read_text().splitlines()[0])
    assert first["scores_sha256"] == head["scores_sha256"] == S.sha_file(str(tmp_path / "scores.json"))


def test_6_the_arms_of_a_cell_share_one_probe_seed():
    rows = S.schedule(P)
    assert len(rows) == len(P["families"]) * len(P["scales"]) * P["reps"] * len(P["arms"]) == 480
    cells = {}
    for t in rows:
        cells.setdefault((t["family"], t["s"], t["rep"]), []).append(t)
    assert len(cells) == 160 and all({t["arm"] for t in c} == set(P["arms"]) for c in cells.values())
    assert all(len({t["probe_seed"] for t in c}) == 1 for c in cells.values())
    assert len({c[0]["probe_seed"] for c in cells.values()}) == 160
    assert all((t["arm"] != "BLIND") == t["told"] for t in rows)
    assert [t["trial"] for t in rows] == [f"t{i:03d}" for i in range(480)] and rows == S.schedule(P)


def test_7_the_pipeline_is_imported_not_copied():
    src = inspect.getsource(S)
    for name in ("def sweep(", "def stat(", "def null(", "def dpeak(", "def detrend(", "class OneLayer", "def data("):
        assert name not in src, name
    import osc_neuron_period_pc
    assert S.PC is osc_neuron_period_pc and S.PC.sweep.__module__ == "osc_neuron_period_pc"
