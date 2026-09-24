#!/usr/bin/env python3
"""Fixture/selftest for osc_band_kquant_qknorm_a00-688fdd59.py (OSC.15). Builds
the SAME tiny random Qwen3 -- no checkpoint, no network, no GPU.

Run: python3 -m pytest <this file> -q   (or directly: python3 <this file>)
"""
import importlib.util
import os

import torch

_HERE = os.path.dirname(os.path.abspath(__file__))
_s = importlib.util.spec_from_file_location(
    "qknorm", os.path.join(_HERE, "osc_band_kquant_qknorm_a00-688fdd59.py"))
qn = importlib.util.module_from_spec(_s)
_s.loader.exec_module(qn)


def test_qwen3_has_qknorm_and_qwen2_does_not():
    model = qn.build_tiny()
    ok, qname, kname = qn.qknorm_struct(model)
    assert ok and qname == "Qwen3RMSNorm" and kname == "Qwen3RMSNorm"
    assert qn.qwen2_has_norm() is False


def test_hook_intercepts_postrope_key_and_changes_output():
    model = qn.build_tiny()
    qn.install_qwen3(model)
    ids = torch.randint(0, 256, (1, 12), generator=torch.Generator().manual_seed(7))
    l_off, l_on = qn.run(model, ids, False), qn.run(model, ids, True)
    qref, kref = qn.STATE["inner"](qn.CAP["q_pre"], qn.CAP["k_pre"], qn.CAP["cos"], qn.CAP["sin"])
    assert torch.equal(qn.CAP["q_attn"], qref)
    assert torch.equal(qn.CAP["k_attn"], qn.kq.quant_bw(kref))
    assert not torch.equal(l_off, l_on)


def test_offline_env_set_before_transformers_import():
    assert os.environ.get("HF_HUB_OFFLINE") == "1"
    assert os.environ.get("TRANSFORMERS_OFFLINE") == "1"


if __name__ == "__main__":
    test_qwen3_has_qknorm_and_qwen2_does_not()
    test_hook_intercepts_postrope_key_and_changes_output()
    test_offline_env_set_before_transformers_import()
    print("all fixture tests pass")
