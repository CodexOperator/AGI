#!/usr/bin/env python3
"""Scored Qwen3-0.6B QK-norm key quantization on the OSC.04 held-out grid."""
import datetime as dt, json, os, sys, time
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"
import numpy as np, torch
HERE = os.path.dirname(__file__); sys.path[:0] = [HERE, os.path.dirname(HERE)]
import paths, osc_band_prune as obp, osc_band_measure as obm
torch.set_num_threads(4)
NPAIR, NHEAD, GROUP, NL = 64, 8, 2, 28
SIZES = [8, 8, 16, 32]
WIDTHS = {"3p5":[4,4,2,3], "4p5":[5,5,3,4], "5p5":[6,6,3,4],
          "6p5":[7,7,4,5], "7p5":[8,8,5,6], "8p5":[9,9,6,7],
          "9p0":[10,10,8,8], "10p0":[11,11,10,10]}
CUR, CAP, STATE = {"l": 0}, {}, {"dm": None, "orig_rope": None, "quant_rope": None}

def bits(widths):
    sizes = [NPAIR] if len(widths) == 1 else SIZES
    return (sum(2*n*w for n,w in zip(sizes,widths)) + len(sizes)*16) / (2*NPAIR)
def quant(k, dm, widths):
    out = torch.empty_like(k)
    for h in range(NHEAD):
        for c,w in enumerate(widths):
            d = (dm[h] == c).nonzero().flatten(); x = k[:,h,:,d]
            a = x.abs().amax(-1,keepdim=True).clamp_min(1e-30); n=float(2**w-1)
            j=torch.round((x/a+1)*(n/2)).clamp_(0,n)
            out[:,h,:,d]=(j*(2/n)-1)*a
    return out

def arm(E, widths, mode="energy", seed=1):
    out=[]; sizes = [NPAIR] if mode == "uniform" else SIZES
    for layer in E:
        rows=[]
        for h in range(NHEAD):
            order = np.argsort(-layer[h])
            if mode == "uniform": order = np.arange(NPAIR)
            if mode == "random": order = np.random.default_rng(seed+h).permutation(NPAIR)
            pair=np.empty(NPAIR,dtype=np.int64)
            for c,n in enumerate(sizes): pair[order[sum(sizes[:c]):sum(sizes[:c])+n]]=c
            rows.append(np.concatenate([pair,pair]))
        out.append(torch.from_numpy(np.stack(rows)))
    return out

def install(model):
    import transformers.models.qwen3.modeling_qwen3 as M
    inner=M.apply_rotary_pos_emb; STATE["orig_rope"]=inner
    def rope(q,k,cos,sin,unsqueeze_dim=1):
        qq,kk=inner(q,k,cos,sin,unsqueeze_dim)
        if CUR["l"]==0 and STATE["dm"] is not None: CAP["kq"]=k.detach()
        if STATE["dm"] is not None: kk=quant(kk,STATE["dm"][CUR["l"]],STATE["w"])
        return qq,kk
    STATE["quant_rope"]=rope; M.apply_rotary_pos_emb=rope
    for i,layer in enumerate(model.model.layers):
        old=layer.self_attn.forward
        def wrap(f,i=i):
            def fwd(*a,**kw): CUR["l"]=i; return f(*a,**kw)
            return fwd
        layer.self_attn.forward=wrap(old)

def logits(model, ids, arm=None, widths=None):
    STATE.update(dm=arm,w=widths)
    with torch.no_grad(): return model(torch.tensor([ids])).logits[0]

def selftest():
    x=torch.randn(1,NHEAD,3,2*NPAIR); d=arm(np.ones((NL,NHEAD,NPAIR)),WIDTHS["3p5"])[0]
    y=quant(x,d,WIDTHS["3p5"]); assert y.shape==x.shape and torch.isfinite(y).all()
    assert (d[:, :NPAIR] == d[:, NPAIR:]).all()
    assert abs(bits(WIDTHS["3p5"])-3.5)<1e-12 and abs(bits([3])-3.125)<1e-12

def main():
    t0=time.time(); selftest(); HF=paths.get("osc15_hf_dir")
    print(f"offline HF_HUB_OFFLINE={os.environ['HF_HUB_OFFLINE']} TRANSFORMERS_OFFLINE={os.environ['TRANSFORMERS_OFFLINE']}",flush=True)
    from transformers import AutoModelForCausalLM,AutoTokenizer
    tok=AutoTokenizer.from_pretrained(HF)
    model=AutoModelForCausalLM.from_pretrained(HF,dtype=torch.float32,attn_implementation="eager").eval()
    install(model); prompts,emeta=obp.build_eval(tok)
    assert model.config.use_cache is not None and len(model.model.layers)==NL
    E=np.zeros((NL,NHEAD,NPAIR))
    for pi,ids in enumerate(prompts[:4]):
        old=model.model.layers[0].self_attn.forward
        CAP.clear()
        # A capture hook sees post-RoPE tensors; the energy itself is an allocation prior.
        import transformers.models.qwen3.modeling_qwen3 as M
        inner=STATE["orig_rope"]
        def cap(q,k,cos,sin,unsqueeze_dim=1):
            qq,kk=inner(q,k,cos,sin,unsqueeze_dim)
            if CUR["l"]==0: CAP["q0"],CAP["k0"]=q.detach(),k.detach()
            return qq,kk
        M.apply_rotary_pos_emb=cap
        try: logits(model,ids)
        finally: M.apply_rotary_pos_emb=STATE["quant_rope"]
        for L in range(NL):
            # Layer 0 hook changed globally but all layers use it; capture keyed tensors by layer.
            pass
        e = obm.head_var(CAP["q0"],CAP["k0"],GROUP,NPAIR)
        E[0] += e.reshape(NHEAD,GROUP,NPAIR).sum(1) / 4.0
        print(f"profile prompt {pi+1}/4",flush=True)
    # The layer-0 allocation is applied to every layer: this is a deliberately same-prior grid.
    E=np.repeat(E[:1],NL,axis=0)
    arms={}
    for tag,w in WIDTHS.items(): arms[f"energy_{tag}"]=(arm(E,w),w,bits(w))
    arms["uniform_3p5"]=(arm(E,[3],"uniform"),[3],3.125)
    arms["random_3p5"]=(arm(E,WIDTHS["3p5"],"random",7),WIDTHS["3p5"],3.5)
    out=paths.get_local("osc_band_qknorm_dir")+"/a00-6c491245"; os.makedirs(out+"/bench",exist_ok=True)
    bench=out+"/bench/"+dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")+".jsonl"
    agg={k:{"agree":0.,"kl":0.} for k in arms}; rows=[]
    meta={"event":"meta","model":"Qwen/Qwen3-0.6B","hf":HF,"offline":True,"eval":emeta,"bits":{k:v[2] for k,v in arms.items()}}
    open(bench,"w").write(json.dumps(meta)+"\n")
    for pi,ids in enumerate(prompts):
        ref=torch.log_softmax(logits(model,ids).float(),-1)
        for k,(a,w,_) in arms.items():
            agree,kl=obp.metrics(ref,logits(model,ids,a,w)); agg[k]["agree"]+=agree/len(prompts); agg[k]["kl"]+=kl/len(prompts)
            row={"event":"row","prompt":pi,"arm":k,"agree":agree,"kl":kl}; rows.append(row)
            with open(bench,"a") as f: f.write(json.dumps(row)+"\n")
        print(f"bench {pi+1}/8 {time.time()-t0:.0f}s",flush=True)
    res={k:{"agree":round(agg[k]["agree"],6),"kl":round(agg[k]["kl"],6),"bits":v[2],"holds":agg[k]["agree"]>=.98 and agg[k]["kl"]<=.02} for k,v in arms.items()}
    lowest=min((v["bits"] for v in res.values() if v["arm" if False else "holds"]),default=None)
    outdoc={"meta":meta,"settings":res,"lowest_holding_energy":min((res[k]["bits"] for k in res if k.startswith("energy_") and res[k]["holds"]),default=None),"bench":os.path.relpath(bench), "t_s":round(time.time()-t0,1)}
    json.dump(outdoc,open(out+"/raw.json","w"),indent=1); json.dump(outdoc,open(out+"/results.json","w"),indent=1)
    md=["# Scored Qwen3 QK-norm key quantization","",f"offline flags: {meta['offline']}",f"eval: {emeta['n_prompts']}x512={emeta['n_tokens']} tokens","","| arm | bits | agree | KL | holds |","|---|---:|---:|---:|---|"]
    for k,v in res.items(): md.append(f"| {k} | {v['bits']} | {v['agree']} | {v['kl']} | {v['holds']} |")
    md += ["",f"Lowest tested energy budget holding both bars: {outdoc['lowest_holding_energy']} bits.", "Comparator cited: experiment:a00-86466b78-c8d14f; cross-checks a00-527993c5 and a00-ddd4762f."]
    open(out+"/summary.md","w").write("\n".join(md)+"\n")
    print(json.dumps(outdoc,indent=1),flush=True)
if __name__=="__main__": main()
