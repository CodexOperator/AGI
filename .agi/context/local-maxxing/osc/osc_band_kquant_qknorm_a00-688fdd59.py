#!/usr/bin/env python3
"""OSC.15 TMM.122 mechanical pre-step: QK-norm (Qwen3) adapter for OSC.10's
post-RoPE key quantizer. MECHANISM ONLY -- tiny random Qwen3, no checkpoint,
no network, no GPU. Imports quant_bw from osc_band_kquant, never copies it.

Run: V="$(python3 .agi/context/local-maxxing/paths.py osc03_pylib_dir)" PYTHONPATH="$V" \
  nice -n 19 "$(python3 .agi/context/local-maxxing/paths.py ml_python)" \
  .agi/context/local-maxxing/osc/osc_band_kquant_qknorm_a00-688fdd59.py
"""
import json, os, sys, time
os.environ["HF_HUB_OFFLINE"] = "1"        # hard backstop: fail fast, never reach the net
os.environ["TRANSFORMERS_OFFLINE"] = "1"
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import paths
import osc_band_prune as obp        # reuse the OSC.04 layer tracker (CUR["l"])
import osc_band_kquant as kq        # quant_bw (imported, not copied)
import transformers.models.qwen3.modeling_qwen3 as M3
torch.set_num_threads(4)

AGENT = "a00-688fdd59"
STATE, CAP = {"bw": False, "inner": None}, {}


def install_qwen3(model):
    """Post-RoPE key quantizer for Qwen3 + layer-0 q/k capture at the attn
    interface. head_dim=64 (2*32) keeps kq.quant_bw's 32-block reshape valid."""
    obp.install(model)
    STATE["inner"] = M3.apply_rotary_pos_emb
    inner, eaf = STATE["inner"], M3.eager_attention_forward

    def rope(q, k, cos, sin, unsqueeze_dim=1):
        qq, kk = inner(q, k, cos, sin, unsqueeze_dim)
        if obp.CUR["l"] == 0:
            CAP["q_pre"], CAP["k_pre"] = q.detach().clone(), k.detach().clone()
            CAP["cos"], CAP["sin"] = cos.detach().clone(), sin.detach().clone()
        if STATE["bw"]:
            kk = kq.quant_bw(kk)             # post-RoPE key, exactly OSC.10's hook point
        return qq, kk

    def attn(module, query, key, value, *a, **kw):
        if getattr(module, "layer_idx", None) == 0:
            CAP["q_attn"], CAP["k_attn"] = query.detach().clone(), key.detach().clone()
        return eaf(module, query, key, value, *a, **kw)

    M3.apply_rotary_pos_emb = rope
    M3.ALL_ATTENTION_FUNCTIONS["eager"] = attn   # _local_mapping override, read by get_interface


def build_tiny(seed=0):
    from transformers import Qwen3Config, Qwen3ForCausalLM
    torch.manual_seed(seed)
    cfg = Qwen3Config(hidden_size=64, num_hidden_layers=2, num_attention_heads=4,
                      num_key_value_heads=2, head_dim=64, intermediate_size=128,
                      vocab_size=256, max_position_embeddings=64, rms_norm_eps=1e-6)
    cfg._attn_implementation = "eager"
    return Qwen3ForCausalLM(cfg).eval()


def run(model, ids, quant_on):
    STATE["bw"] = quant_on
    with torch.no_grad():
        return model(ids).logits[0]


def qknorm_struct(model):
    a = model.model.layers[0].self_attn
    ok = (isinstance(a.q_norm, torch.nn.Module) and isinstance(a.k_norm, torch.nn.Module)
          and not isinstance(a.q_norm, torch.nn.Identity)
          and not isinstance(a.k_norm, torch.nn.Identity))
    return bool(ok), type(a.q_norm).__name__, type(a.k_norm).__name__


def qwen2_has_norm():
    import inspect
    from transformers.models.qwen2 import modeling_qwen2 as M2
    src = inspect.getsource(M2.Qwen2Attention.__init__)
    return ("q_norm" in src) or ("k_norm" in src)


def main():
    t0 = time.time()
    print("offline HF_HUB_OFFLINE=%s TRANSFORMERS_OFFLINE=%s"
          % (os.environ["HF_HUB_OFFLINE"], os.environ["TRANSFORMERS_OFFLINE"]), flush=True)
    model = build_tiny()
    print("config._attn_implementation =", model.config._attn_implementation, flush=True)
    install_qwen3(model)
    ids = torch.randint(0, 256, (1, 12), generator=torch.Generator().manual_seed(7))
    l_off, l_on = run(model, ids, False), run(model, ids, True)
    qref, kref = STATE["inner"](CAP["q_pre"], CAP["k_pre"], CAP["cos"], CAP["sin"])
    hook = {"q_untouched": bool(torch.equal(CAP["q_attn"], qref)),
            "attn_k_is_quant_postrope": bool(torch.equal(CAP["k_attn"], kq.quant_bw(kref))),
            "quant_changes_output": bool(not torch.equal(l_off, l_on))}
    print("hook:", json.dumps(hook), flush=True)
    assert all(hook.values()), ("hook failed; NOT forcing True", hook)
    smod, qn, kn = qknorm_struct(model)
    q2 = qwen2_has_norm()
    print("q_norm=%s k_norm=%s structural=%s | qwen2_has_qk_norm=%s" % (qn, kn, smod, q2), flush=True)
    assert smod and (not q2) and model.config._attn_implementation == "eager", (smod, q2)

    od = os.path.join(paths.get_local("osc_band_qknorm_dir"), AGENT)
    os.makedirs(od, exist_ok=True)
    res = {"meta": {"transformers": __import__("transformers").__version__,
                    "torch": torch.__version__, "model": "Qwen3ForCausalLM random weights",
                    "attn_implementation": model.config._attn_implementation,
                    "head_dim": model.config.head_dim, "seq_len": 12,
                    "offline": [os.environ["HF_HUB_OFFLINE"], os.environ["TRANSFORMERS_OFFLINE"]],
                    "no_checkpoint": True, "t_s": round(time.time() - t0, 3)},
           "hook": hook, "q_norm_type": qn, "k_norm_type": kn,
           "qwen2_has_qk_norm": q2, "structural_ok": smod}
    json.dump(res, open(os.path.join(od, "raw.json"), "w"), indent=1)
    lines = [
        "# OSC.15 TMM.122 mechanical pre-step: Qwen3 QK-norm adapter", "",
        "MECHANISM ONLY (no checkpoint/network/GPU; HF_HUB_OFFLINE=1, TRANSFORMERS_OFFLINE=1).", "",
        "Verified: attn_implementation=%s | hook=%s" % (model.config._attn_implementation, json.dumps(hook)),
        "q_norm=%s k_norm=%s structural=%s qwen2_has_qk_norm=%s" % (qn, kn, smod, q2), "",
        "q_norm/k_norm are real Qwen3RMSNorm, applied BEFORE RoPE (absent on Qwen2); the patched",
        "post-RoPE key at the attention interface equals an independent quant_bw(rope(q,k)) reference,",
        "and ALL_ATTENTION_FUNCTIONS[\"eager\"] item-assignment is honored live (output differs on/off).", "",
        "Remains gated: a scored agreement/KL result needs a PRETRAINED QK-norm checkpoint -- none",
        "obtained (no download/network in scope, none cached on this box); no bit budget was tested.",
    ]
    open(os.path.join(od, "summary.md"), "w").write("\n".join(lines) + "\n")
    print(json.dumps(res, indent=1), flush=True)
    print("wrote", od, flush=True)


if __name__ == "__main__":
    main()
