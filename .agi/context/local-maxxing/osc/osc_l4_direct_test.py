"""Tests for osc_l4_direct.py (hypothesis:lm-l4-direct-head-cost-ranking-holds-on-fresh-docs TESTS 1-4). No model
load (test 1b loads the tokenizer only).

Run (the torch venv has no pytest; borrow the user site's):
  PYTHONPATH="$(python3 .agi/context/local-maxxing/paths.py osc_test_pythonpath):$(python3 -m site --user-site)" \
  "$(python3 .agi/context/local-maxxing/paths.py ml_python)" -m pytest osc_l4_direct_test.py -q --basetemp /tmp/<dir>
"""
import inspect
import json
import os
import subprocess
import sys

import pytest

torch = pytest.importorskip("torch")
pytest.importorskip("numpy")

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import osc_l4_direct as Y  # noqa: E402
import osc_l4_mass as X  # noqa: E402
import osc_l4_window as W  # noqa: E402
import paths  # noqa: E402

M = pytest.importorskip("transformers.models.qwen2.modeling_qwen2")
W.install(M)
NQ, NKV = 14, 2
COMMITS = {"osc_l4_window.py": "378a3c3eaf", "osc_l4_distance.py": "e18b2e41dd", "osc_l4_mass.py": "be4979294d"}
EXCL = {0, 1, 3, 4, 5, 6, 7, 10, 12, 16, 18, 13}


def params():
    return X.load_params(paths.get_local("osc_band_l4_direct_dir"))


def run3():
    return json.load(open(os.path.join(paths.get_local("osc_band_l4_mass_dir"), "results.json")))


def test_1_picker_excludes_every_named_id_and_is_deterministic():
    P = params()
    assert Y.exclusions(P) == EXCL
    lens = [3000] * 30
    lens[2] = lens[9] = 100                    # too short
    got = Y.pick(lens, EXCL, 8, 2048)
    assert got == [8, 11, 14, 15, 17, 19, 20, 21] and got == Y.pick(list(lens), set(EXCL), 8, 2048)
    assert not set(got) & EXCL and all(lens[i] >= 2048 for i in got)
    assert Y.pick([3000] * 14, EXCL, 8, 2048) == [2, 8, 9, 11]   # never pads with an excluded id


def test_1b_committed_fresh_docs_equal_the_picker_on_wiki_valid():
    P = params()
    tok = pytest.importorskip("transformers").AutoTokenizer.from_pretrained(paths.get(P["model_cell"]))
    a, b = Y.fresh(tok, P), Y.fresh(tok, P)
    assert a == b == P["fresh_docs"] and len(a) == P["n_fresh"] == 8
    assert not {d for d, _ in a} & EXCL
    docs = W.load_docs(tok, dict(P, eval_docs=a[1:], calib_doc=a[0]))   # run 1's loader re-asserts titles + length
    assert sorted(docs) == sorted(d for d, _ in a)


def test_2_frozen_rankings_equal_run3_byte_for_byte():
    P, R3 = params(), run3()
    for a in Y.FROZEN:
        assert json.dumps(P[f"frozen_{a}_ranking"]).encode() == json.dumps(R3[f"{a}_ranking"]).encode()
        assert sorted(P[f"frozen_{a}_ranking"]) == list(range(48))
    assert Y.frozen_ok(P, R3)
    bad = dict(P, frozen_direct_ranking=P["frozen_direct_ranking"][::-1])
    assert not Y.frozen_ok(bad, R3)


def tiny_model():
    cfg = M.Qwen2Config(vocab_size=64, hidden_size=NQ * 8, intermediate_size=64, num_hidden_layers=2,
                        num_attention_heads=NQ, num_key_value_heads=NKV, max_position_embeddings=64)
    cfg._attn_implementation = "eager"
    torch.manual_seed(0)
    return M.Qwen2ForCausalLM(cfg).eval()


def test_3_additivity_of_a_single_head_is_one():
    model, T, lo, hi = tiny_model(), 32, 16, 32
    M.eager_attention_forward = W.attn
    ids = torch.randint(0, 64, (1, T), generator=torch.Generator().manual_seed(1))
    W.S.update(win={}, dist=None, bad=W.disallow(T, 4, 2), lo=lo, hi=hi)   # a window that bites
    h = X.hidden(model, ids, lo, hi)
    for head in range(2 * NKV):
        joint, solo = X.scored(model, h, ids, [head], NKV, lo, hi, 8)[1], X.scored(model, h, ids, [head], NKV, lo,
                                                                                   hi, 8)[1]
        assert joint > 0 and Y.additivity(joint, [solo]) == 1.0
    two = X.scored(model, h, ids, [0, 3], NKV, lo, hi, 8)[1]
    r = Y.additivity(two, [X.scored(model, h, ids, [x], NKV, lo, hi, 8)[1] for x in (0, 3)])
    assert r > 0 and r == r
    assert Y.additivity(0.3, [0.1, 0.2]) == pytest.approx(1.0)
    assert Y.key([17, 3]) == "17,3" and Y.key([5]) == str(5)


def test_3b_grid_inherited_not_retyped_and_kept_equals_runs():
    out = paths.get_local("osc_band_l4_direct_dir")
    P, raw = params(), json.load(open(os.path.join(out, "params.json")))
    B1 = json.load(open(os.path.join(paths.get_local("osc_band_l4_dir"), "params.json")))
    B2 = json.load(open(os.path.join(paths.get_local("osc_band_l4_distance_dir"), "params.json")))
    assert all(P[k] == B1[k] for k in P["inherit"]) and all(P[k] == B2[k] for k in P["inherit_run2"])
    assert not {"eval_docs", "budgets", "k", "W", "sinks", "seeds", "calib_docs", "exclude_docs"} & set(raw)
    R1 = json.load(open(os.path.join(paths.get_local("osc_band_l4_dir"), "results.json")))
    for b, k in zip(P["budgets"], P["k"]):
        assert W.kept_fraction(k, P["W"], P["sinks"], P["L"], 48) == R1["table"][str(b)]["kept"]


def test_4_runs_1_3_imported_not_copied_and_unchanged():
    src = inspect.getsource(Y)
    for name in ("disallow", "window_mask", "kept_fraction", "load_docs", "score", "as_win", "install", "spearman",
                 "ranking", "hidden", "scored", "load_params", "dump", "mass_outside", "attn"):
        assert f"def {name}(" not in src
    for name in ("disallow", "kept_fraction", "load_docs", "install"):
        assert f"W.{name}(" in src
    for name in ("hidden", "scored", "load_params", "dump"):
        assert f"X.{name}(" in src
    assert Y.W is W and Y.X is X and X.W is W
    for f, c in COMMITS.items():
        for rev in (c, "HEAD"):
            r = subprocess.run(["git", "-C", HERE, "diff", "--quiet", rev, "--", os.path.join(HERE, f)])
            assert r.returncode == 0, (f, rev)
