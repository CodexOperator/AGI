#!/usr/bin/env python3
"""Low-peak fp32 model load for the osc band rounds (TMM.226/230).

Weights stay RESIDENT in bf16 (the checkpoint's own dtype) and every Linear sees its
weight upcast to fp32 at access -- bf16 -> fp32 is exact, so the fp32 kernels get the
same values an fp32 load holds. The tied embedding is kept fp32 (the lm_head is the
largest matmul). The lm_head is lifted OUT of the model: forward() returns hidden
states [T, H], and metrics() applies the head in row chunks (values.local_maxxing.
lowpeak_head_rows), recomputing the reference log_softmax per chunk, then takes the
same final mean obp.metrics() takes over the concatenated per-row values.
Predicted peak 2249 MiB vs 3615/4207 for the fp32 load (bba276955)."""
import json
import torch
import torch.nn.functional as F
from torch.nn.utils import parametrize
import paths


class Upcast(torch.nn.Module):
    def forward(self, w):
        return w.float()


def rows():
    return int(json.load(open(paths.config_path()))["values"]["local_maxxing"]["lowpeak_head_rows"])


def load(hf):
    """bf16-resident, fp32-computing model; returns (model, head_w). model(...).logits = hidden."""
    from transformers import AutoModelForCausalLM
    model = AutoModelForCausalLM.from_pretrained(hf, dtype=torch.bfloat16, attn_implementation="eager").eval()
    head_w = model.get_input_embeddings().weight
    assert model.lm_head.weight is head_w, "lowpeak assumes tied embeddings"
    lin = [m for n, m in model.named_modules() if isinstance(m, torch.nn.Linear) and m is not model.lm_head]
    for m in lin:
        parametrize.register_parametrization(m, "weight", Upcast(), unsafe=True)
    for n, p in model.named_parameters():   # embedding, norms, biases -> fp32 (exact)
        if not n.endswith(".original"):
            p.data = p.data.float()
    bad = [n for n, b in model.named_buffers() if b.is_floating_point() and b.dtype != torch.float32]
    assert not bad, ("non-fp32 buffers would not match an fp32 load", bad)
    model.lm_head = torch.nn.Identity()
    return model, head_w


@torch.no_grad()   # head_w is a Parameter: without this, autograd would hold every chunk
def metrics(head_w, ref_h, arm_h, n=None):
    """obp.metrics(log_softmax(ref logits), arm logits), with the head applied n rows at a time."""
    n = n or rows(); ag, kl = [], []
    for s in range(0, ref_h.shape[0], n):
        ref = torch.log_softmax(F.linear(ref_h[s:s + n], head_w).float(), -1)
        lp = torch.log_softmax(F.linear(arm_h[s:s + n], head_w).float(), -1)
        ag.append(ref.argmax(-1) == lp.argmax(-1))
        d = ref - lp; d.mul_(ref.exp()); kl.append(d.sum(-1))
    return float(torch.cat(ag).float().mean()), float(torch.cat(kl).mean())
