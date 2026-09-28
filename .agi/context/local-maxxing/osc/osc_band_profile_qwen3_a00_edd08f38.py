#!/usr/bin/env python3
"""Qwen3 OSC.03 profile_pooled cell and key-only statistic comparison."""
import datetime as dt, hashlib, json, os, sys
os.environ["HF_HUB_OFFLINE"] = os.environ["TRANSFORMERS_OFFLINE"] = "1"
import numpy as np, torch
HERE = os.path.dirname(__file__); sys.path[:0] = [HERE, os.path.dirname(HERE)]
import paths, osc_band_prune as obp, osc_band_measure as obm

def sha(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1<<20),b""): h.update(b)
    return h.hexdigest()

def install(model):
    c=model.config
    spec={"layers":len(model.model.layers),"heads":c.num_attention_heads,
          "kv_heads":c.num_key_value_heads,"head_dim":getattr(c,"head_dim",None) or c.hidden_size//c.num_attention_heads}
    spec["pairs"]=spec["head_dim"]//2; spec["group"]=spec["heads"]//spec["kv_heads"]
    key="qwen3" if c.model_type=="qwen3" else "qwen2"
    M=__import__("transformers.models."+key+".modeling_"+key,fromlist=["x"])
    inner=M.apply_rotary_pos_emb; cap={}; cur={"l":0}
    def rope(q,k,cos,sin,unsqueeze_dim=1):
        qq,kk=inner(q,k,cos,sin,unsqueeze_dim); cap[cur["l"]]=(qq.detach(),kk.detach()); return qq,kk
    M.apply_rotary_pos_emb=rope
    for i,layer in enumerate(model.model.layers):
        old=layer.self_attn.forward
        def wrap(f,i=i):
            def fwd(*a,**kw): cur["l"]=i; return f(*a,**kw)
            return fwd
        layer.self_attn.forward=wrap(old)
    return spec,cap,key

def profiles(model,prompts,spec,cap):
    E=np.zeros((spec["layers"],spec["kv_heads"],spec["pairs"]))
    K=np.zeros_like(E)
    for pi,ids in enumerate(prompts):
        cap.clear()
        with torch.no_grad(): model(torch.tensor([ids]))
        assert set(cap)==set(range(spec["layers"])), (pi,set(cap))
        for L in range(spec["layers"]):
            q,k=cap[L]
            e=obm.head_var(q,k,spec["group"],spec["pairs"])
            E[L]+=e.reshape(spec["kv_heads"],spec["group"],spec["pairs"]).sum(1)/len(prompts)
            # Literal key-only energy: RMS over tokens, per RoPE pair and KV head.
            z=k[0].float().reshape(spec["kv_heads"],-1,spec["pairs"],2).square().sum(-1).mean(1).cpu().numpy()
            K[L]+=z/len(prompts)
    return E,K

def spearman(a,b):
    ra=np.argsort(np.argsort(a)).astype(float); rb=np.argsort(np.argsort(b)).astype(float)
    return float(np.corrcoef(ra,rb)[0,1])

def main():
    out=os.path.join(paths.get_local("osc_band_qknorm_dir"),"a00-edd08f38-profile-qwen3")
    bench_dir=os.path.join(out,"bench"); os.makedirs(bench_dir,exist_ok=True)
    bench=os.path.join(bench_dir,dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")+".jsonl")
    hf=paths.get("osc15_hf_dir")
    from transformers import AutoModelForCausalLM,AutoTokenizer
    tok=AutoTokenizer.from_pretrained(hf); model=AutoModelForCausalLM.from_pretrained(hf,dtype=torch.float32,attn_implementation="eager").eval()
    spec,cap,key=install(model); prompts,emeta=obp.build_eval(tok)
    assert key=="qwen3" and spec["head_dim"]==128 and spec["pairs"]==64 and spec["group"]==2
    E,K=profiles(model,prompts,spec,cap)
    cells={}
    for L in range(spec["layers"]):
      for h in range(spec["kv_heads"]):
        e=E[L,h]; k=K[L,h]; cells[f"L{L}H{h*spec['group']}"]={
          "profile_pooled":(e/e.sum()).round(8).tolist(),
          "key_only_energy":(k/k.sum()).round(8).tolist(),
          "rank_correlation":spearman(e,k)}
    meta={"event":"meta","model":"Qwen/Qwen3-0.6B","hf":hf,"offline":True,
          "eval":emeta,"architecture":spec,"capture":"post_rope_per_layer",
          "input_sha256":{n:sha(os.path.join(hf,n)) for n in ("config.json","model.safetensors")}}
    with open(bench,"w") as f: f.write(json.dumps(meta)+"\n")
    vals=[v["rank_correlation"] for v in cells.values()]
    result={"event":"profile_result","model":"Qwen/Qwen3-0.6B","cells":cells,
            "rank_correlation":{"n":len(vals),"min":min(vals),"mean":float(np.mean(vals)),
                                "median":float(np.median(vals)),"max":max(vals)},
            "threshold":{"rank_spearman":0.9,"crosses":bool(min(vals)>=0.9)},
            "literal_key_only_energy_is_distinct":bool(min(vals)<0.9),
            "provenance":meta["input_sha256"],"bench":os.path.relpath(bench,os.path.dirname(out))}
    json.dump(result,open(os.path.join(out,"profiles.json"),"w"),indent=1)
    with open(bench,"a") as f: f.write(json.dumps(result)+"\n")
    open(os.path.join(out,"summary.md"),"w").write("# Qwen3 profile_pooled cell\n\n"+json.dumps(result["rank_correlation"],indent=1)+"\n")
    print(json.dumps(result,indent=1))
if __name__=="__main__": main()
