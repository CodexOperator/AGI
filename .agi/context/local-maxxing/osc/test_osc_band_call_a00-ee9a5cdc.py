"""Acceptance tests for the per-cell band CALL rule (fixtures only, no model)."""
import importlib.util, os
P = os.path.dirname(__file__)
S = importlib.util.spec_from_file_location("call", os.path.join(P, "osc_band_call_a00-ee9a5cdc.py"))
m = importlib.util.module_from_spec(S); S.loader.exec_module(m)

# A: band_agree 0.085 (the a00-bcea484d probe width), band_kl 0.02; key_only
#    agree margin 0.05625 (inside), kl margin exactly == band (equality trap).
# B: key_only wins both metrics.  C: key_only loses both.  D: 2 draws -> gated.
FIXTURE = """\
{"model":"qwen2","np":32,"budget":"5.25","arm":"random","seed":0,"agree":0.500,"kl":0.10}
{"model":"qwen2","np":32,"budget":"5.25","arm":"random","seed":1,"agree":0.530,"kl":0.11}
{"model":"qwen2","np":32,"budget":"5.25","arm":"random","seed":2,"agree":0.560,"kl":0.12}
{"model":"qwen2","np":32,"budget":"5.25","arm":"random","seed":3,"agree":0.585,"kl":0.12}
{"model":"qwen2","np":32,"budget":"5.25","arm":"key_only","seed":0,"agree":0.600,"kl":0.0925}
{"model":"qwen2","np":32,"budget":"5.25","arm":"uniform","seed":0,"agree":0.54375,"kl":0.11}
{"model":"qwen2","np":32,"budget":"5.25","arm":"key_only","seed":1,"agree":0.600,"kl":0.0925}
{"model":"qwen2","np":32,"budget":"5.25","arm":"key_only","seed":2,"agree":0.600,"kl":0.0925}
{"model":"qwen2","np":32,"budget":"6.25","arm":"random","seed":0,"agree":0.500,"kl":0.10}
{"model":"qwen2","np":32,"budget":"6.25","arm":"random","seed":1,"agree":0.530,"kl":0.11}
{"model":"qwen2","np":32,"budget":"6.25","arm":"random","seed":2,"agree":0.560,"kl":0.12}
{"model":"qwen2","np":32,"budget":"6.25","arm":"key_only","seed":0,"agree":0.700,"kl":0.05}
{"model":"qwen2","np":32,"budget":"6.25","arm":"uniform","seed":0,"agree":0.530,"kl":0.11}
{"model":"qwen2","np":32,"budget":"7.25","arm":"random","seed":0,"agree":0.500,"kl":0.10}
{"model":"qwen2","np":32,"budget":"7.25","arm":"random","seed":1,"agree":0.530,"kl":0.11}
{"model":"qwen2","np":32,"budget":"7.25","arm":"random","seed":2,"agree":0.560,"kl":0.12}
{"model":"qwen2","np":32,"budget":"7.25","arm":"key_only","seed":0,"agree":0.440,"kl":0.20}
{"model":"qwen2","np":32,"budget":"7.25","arm":"uniform","seed":0,"agree":0.530,"kl":0.11}
{"model":"qwen2","np":32,"budget":"4.25","arm":"random","seed":0,"agree":0.500,"kl":0.10}
{"model":"qwen2","np":32,"budget":"4.25","arm":"random","seed":1,"agree":0.520,"kl":0.11}
{"model":"qwen2","np":32,"budget":"4.25","arm":"key_only","seed":0,"agree":0.600,"kl":0.05}
"""


def test_band_is_the_stochastic_min_max_not_a_deterministic_spread():
    c = m.cells(m.load(FIXTURE))[("qwen2", 32, "5.25")]
    assert round(m.band(c, "agree"), 9) == 0.085
    assert round(m.band(c, "kl"), 9) == 0.02
    assert m.arm_draws(c, "uniform", "agree") == [0.54375]   # n=1, spread 0.0


def test_calls_match_the_hand_computation():
    j = m.judge(FIXTURE)
    assert j[("qwen2", 32, "5.25", "key_only", "agree")] == "inside-noise"  # 0.05625 < 0.085
    assert j[("qwen2", 32, "5.25", "key_only", "kl")] == "inside-noise"     # margin == band, strict >
    assert j[("qwen2", 32, "6.25", "key_only", "agree")] == "win"
    assert j[("qwen2", 32, "6.25", "key_only", "kl")] == "win"
    assert j[("qwen2", 32, "7.25", "key_only", "agree")] == "loss"
    assert j[("qwen2", 32, "7.25", "key_only", "kl")] == "loss"


def test_kl_sign_is_inverted_so_a_lower_kl_is_a_win():
    j = m.judge(FIXTURE)
    assert j[("qwen2", 32, "6.25", "key_only", "kl")] == "win"     # 0.05 < random 0.11
    assert j[("qwen2", 32, "7.25", "key_only", "kl")] == "loss"     # 0.20 > random 0.11


def test_uniform_against_itself_is_inside_noise_on_both_metrics():
    j = m.judge(FIXTURE, arm="uniform")
    for met in ("agree", "kl"):
        assert j[("qwen2", 32, "5.25", "uniform", met)] == "inside-noise"


def test_fewer_than_three_stochastic_draws_never_emits_a_word():
    j = m.judge(FIXTURE)
    for met in ("agree", "kl"):
        assert j[("qwen2", 32, "4.25", "key_only", met)] == "unresolved"
    c = m.cells(m.load(FIXTURE))[("qwen2", 32, "4.25")]
    assert m.band(c, "agree") is None
    assert round(m.margin(c, "key_only", "agree"), 9) == 0.09   # computable, still not a word
