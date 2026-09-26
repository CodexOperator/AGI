"""No-checkpoint tests for osc_lowpeak (TMM.230 condition 1). Never loads a real model:
(a) the bf16-resident upcast Linear == the fp32-resident one, bit for bit, at the real
Qwen2.5-0.5B shapes; (b) the chunked head + per-chunk log_softmax == obp.metrics over the
full 512 x 151936 logits; (c) the whole load path on a TINY random Qwen2 (config-built,
a few MB) against today's fp32 from_pretrained of the same bf16 checkpoint."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path[:0] = [os.path.dirname(HERE), HERE]
import pytest, torch
import torch.nn.functional as F
from torch.nn.utils import parametrize
import osc_lowpeak as lp

H, V, T, I, KV = 896, 151936, 512, 4864, 128   # Qwen2.5-0.5B: hidden, vocab, eval rows, mlp, 2 kv heads x 64


def _avail_gib():
    return int(next(l for l in open("/proc/meminfo") if l.startswith("MemAvailable")).split()[1]) / 2**20


@pytest.mark.parametrize("fan_in,fan_out,bias", [(H, I, False), (I, H, False), (H, KV, True), (H, H, True)])
def test_upcast_linear_is_bit_identical(fan_in, fan_out, bias):
    torch.manual_seed(1)
    ref = torch.nn.Linear(fan_in, fan_out, bias=bias)
    ref.weight.data = ref.weight.data.bfloat16().float()          # an fp32 load of a bf16 checkpoint
    low = torch.nn.Linear(fan_in, fan_out, bias=bias)
    low.weight.data = ref.weight.data.bfloat16()                   # resident bf16
    if bias:
        low.bias.data = ref.bias.data.clone()
    parametrize.register_parametrization(low, "weight", lp.Upcast(), unsafe=True)
    x = torch.randn(T, fan_in)
    assert low.parametrizations.weight.original.dtype == torch.bfloat16
    assert torch.equal(low(x), ref(x))


@pytest.mark.skipif(_avail_gib() < 4, reason="needs ~2.6 GiB for the full-vocab reference")
def test_chunked_head_matches_obp_metrics():
    import osc_band_prune as obp
    torch.manual_seed(0)
    W = torch.randn(V, H) * 0.02; rh = torch.randn(T, H); ah = rh + 0.05 * torch.randn(T, H)
    full = obp.metrics(torch.log_softmax(F.linear(rh, W).float(), -1), F.linear(ah, W))
    assert lp.metrics(W, rh, ah, lp.rows()) == full               # measured 0.0 abs on this box (TMM.230)


def test_load_path_matches_fp32_load_on_a_tiny_qwen2(tmp_path):
    from transformers import Qwen2Config, Qwen2ForCausalLM, AutoModelForCausalLM
    cfg = Qwen2Config(vocab_size=512, hidden_size=64, intermediate_size=128, num_hidden_layers=2,
                      num_attention_heads=4, num_key_value_heads=2, tie_word_embeddings=True)
    torch.manual_seed(2)
    Qwen2ForCausalLM(cfg).to(torch.bfloat16).save_pretrained(tmp_path)   # a bf16 checkpoint, like the real one
    ref = AutoModelForCausalLM.from_pretrained(tmp_path, dtype=torch.float32, attn_implementation="eager").eval()
    low, head_w = lp.load(str(tmp_path))
    ids = torch.randint(0, 512, (1, 48))
    with torch.no_grad():
        want = ref(ids).logits[0]
        h = low(ids).logits[0]
    assert h.shape == (48, 64) and head_w.dtype == torch.float32
    assert torch.equal(F.linear(h, head_w), want)
    a, kl = lp.metrics(head_w, h, h, 16)
    assert a == 1.0 and kl == 0.0
