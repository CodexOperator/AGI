"""Regression tests for the corrected actual Qwen3 RoPE call site."""
import importlib.util, os
import numpy as np
import torch

P=os.path.dirname(__file__)
S=importlib.util.spec_from_file_location("corrected",os.path.join(P,"osc_band_kquant_qknorm_a00-bcb6c85e.py"))
m=importlib.util.module_from_spec(S); S.loader.exec_module(m)

def tiny():
    from transformers import Qwen3Config,Qwen3ForCausalLM
    c=Qwen3Config(hidden_size=64,num_hidden_layers=2,num_attention_heads=4,
                  num_key_value_heads=2,head_dim=64,intermediate_size=128,
                  vocab_size=256,max_position_embeddings=64,rms_norm_eps=1e-6)
    c._attn_implementation="eager"
    return Qwen3ForCausalLM(c).eval()

def test_actual_hook_captures_distinguishable_post_rope_tensors():
    model=tiny(); m.install(model); ids=torch.randint(0,256,(1,16))
    original=m.STATE["inner"]
    try:
        m.STATE["inner"]=lambda q,k,cos,sin,unsqueeze_dim=1:(q+1,k+2)
        m.forward(model,ids.tolist()[0],capture=True)
        assert {x for x in m.CAP if isinstance(x,int)}=={0,1}
        for L in (0,1):
            pre_q,pre_k=m.CAP[("pre",L)]; post_q,post_k=m.CAP[L]
            assert torch.equal(post_q,pre_q+1) and torch.equal(post_k,pre_k+2)
            assert not torch.equal(post_k,pre_k)
    finally:
        m.STATE["inner"]=original
        m.STATE["wrapped"].apply_rotary_pos_emb=original

def test_allocation_is_computed_per_layer_not_one_broadcast_prior():
    model=tiny(); m.install(model); ids=torch.randint(0,256,(1,16))
    E=m.profile(model,[ids.tolist()[0]],n=1)
    assert E.shape==(2,2,32) and np.any(E) and not np.array_equal(E[0],E[1])
    low=m.arm(E,[4,4,2,3])
    assert not torch.equal(low[0],low[1])
