#!/usr/bin/env python3
"""Probe: is key-only quantization really this destructive, or is the hook wrong?
Uniform per-token absmax quantizer at w in {16,8,6,5,4,3,2} on k only; also
w=4 on v only and q only, for contrast. One 512-token prompt."""
import importlib.util, os, sys
import numpy as np, torch
HERE = "/data/work/agi/.agi/worktrees/a00-30502399/.agi/context/local-maxxing/osc"
sys.path.insert(0, os.path.dirname(HERE)); sys.path.insert(0, HERE)
_p = os.path.join(HERE, "osc_band_kquant_a00-86466b78.py")
_s = importlib.util.spec_from_file_location("kqm", _p)
kq = importlib.util.module_from_spec(_s); _s.loader.exec_module(kq)
import osc_band_prune as obp
import transformers.models.qwen2.modeling_qwen2 as M
torch.set_num_threads(4)

from transformers import AutoTokenizer, AutoModelForCausalLM
tok = AutoTokenizer.from_pretrained(obp.HF)
model = AutoModelForCausalLM.from_pretrained(obp.HF, dtype=torch.float32,
                                             attn_implementation="eager").eval()
kq.install(model)

TGT = {"t": "k", "w": 16}
z64 = torch.zeros(2, 64, dtype=torch.int64)
z128 = torch.zeros(2, 128, dtype=torch.int64)


def qz(x, w):
    a = x.abs().amax(-1, keepdim=True).clamp_min(1e-30)
    n = float(2 ** w - 1)
    j = torch.round((x / a + 1.0) * (n / 2.0)).clamp_(0.0, n)
    return (j * (2.0 / n) - 1.0) * a


eaf = M.ALL_ATTENTION_FUNCTIONS["eager"]


def attn(module, query, key, value, *a, **kw):
    w, t = TGT["w"], TGT["t"]
    if w < 16:
        if t == "q":
            query = qz(query, w)
        if t == "v":
            value = qz(value, w)
    return eaf(module, query, key, value, *a, **kw)


M.ALL_ATTENTION_FUNCTIONS["eager"] = attn

prompts, meta = obp.build_eval(tok)
ids = prompts[0]
ref = kq.logits(model, ids, (None, None, False))
refp = torch.log_softmax(ref.float(), -1)
for t in ["k", "q", "v"]:
    for w in [16, 8, 6, 5, 4, 3, 2]:
        TGT.update(t=t, w=w)
        kq.STATE["dm"], kq.STATE["w"], kq.STATE["bw"] = [z64]*24, [w], False
        lg = kq.logits(model, ids, ([z64]*24, [w], False) if t == "k" else (None, None, False))
        a, kl = obp.metrics(refp, lg)
        print(f"w={w:2d} target={t} agree={a:.4f} kl={kl:.4f}", flush=True)
