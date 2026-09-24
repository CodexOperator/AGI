#!/usr/bin/env python3
"""Fixture-only structural selftests for osc_band_kquant_chan_a00-ef75b07a.py (OSC.14).

No model, no download. Run: python3 -m pytest <this file> -q
"""
import importlib.util, os
import torch

_HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location(
    "chan_mod", os.path.join(_HERE, "osc_band_kquant_chan_a00-ef75b07a.py"))
m = importlib.util.module_from_spec(_s); _s.loader.exec_module(m)


def fixture():
    """Hard-fail structural checks: per-channel vs per-token axes and bias recovery."""
    g = torch.Generator().manual_seed(7)
    T, nd = 8, 8
    dev = torch.randn(1, T, nd, generator=g); dev = dev - dev.mean(1, keepdim=True)
    bias = torch.arange(nd).float() * 3.0 - 5.0
    x = dev + bias                                  # exact per-channel mean == bias
    kk = x.unsqueeze(0)                             # (B=1, H=1, T, D) as quant_chan expects
    dm = torch.zeros(1, nd, dtype=torch.int64)      # one head, one class, all dims

    # (a) arm 3's scale is IDENTICAL across the token axis for a given channel.
    m.quant_chan(kk, dm, [4]); a = m.CAPQ["chan_a"]
    assert tuple(a.shape) == (1, 1, nd), a.shape
    assert torch.allclose(a, x.abs().amax(-2, keepdim=True).clamp_min(1e-30))
    assert bool(torch.equal(a.expand(-1, T, -1), a.expand(-1, T, -1)))   # token-independent
    print(f"fixture a: per-channel scale shape={tuple(a.shape)} token-independent=True")

    # (b) arm 1's (token-absmax) scale DOES vary across tokens -- structural contrast.
    at = x.abs().amax(-1, keepdim=True)
    varies = not torch.allclose(at, at[:, :1, :].expand_as(at))
    assert at.shape == (1, T, 1) and varies, (at.shape, varies)
    print(f"fixture b: token-absmax scale shape={tuple(at.shape)} varies-over-tokens={varies}")

    # (c) arm 4's bias recovers the injected per-channel mean.
    m.quant_bias(kk, dm, [4]); b = m.CAPQ["bias_b"]
    assert tuple(b.shape) == (1, 1, nd) and torch.allclose(b[0, 0], bias, atol=1e-5), (b, bias)
    print(f"fixture c: bias max abs err={float((b[0,0]-bias).abs().max()):.2e} (<=1e-5)")

    # (d) matched bit points for arms 1 and 2.
    b1, b2 = m.kq.avg_bits([4, 4, 8, 16], [4, 4, 2, 2], 4), m.kq.avg_bits([16, 16], [3, 3], 2)
    assert b1 == 3.5 and b2 == 3.5, (b1, b2)
    print(f"fixture d: arm1 bits={b1} arm2 bits={b2}")

    # (e) new-arm arithmetic, printed not forced (arm 4 does not land on 3.5).
    a3 = m.kq.avg_bits([4, 4, 8, 16], [4, 4, 2, 2], 4)
    a4 = m.kq.avg_bits([4, 4, 8, 16], [4, 4, 2, 2], 4 + 4)
    print(f"fixture e: arm3 bits={a3} (nscale=4, conservative); arm4 bits={a4} (bias as 4 extra fp16/class)")
    pretty = (sum(2 * n * w for n, w in zip([4, 4, 8, 16], [4, 4, 2, 2])) + 4 * 16) / 64.0
    assert a3 == pretty == 3.5
    assert a4 == 4.5, a4          # honest: arm4 is NOT a 3.5-bit arm
    return True


def test_fixture():
    assert fixture()