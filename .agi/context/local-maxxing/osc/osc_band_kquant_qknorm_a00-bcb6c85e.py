#!/usr/bin/env python3
"""Corrected post-RoPE, per-layer key-energy allocation on the OSC.04 grid."""
import datetime as dt, json, os, sys, time
os.environ["HF_HUB_OFFLINE"] = os.environ["TRANSFORMERS_OFFLINE"] = "1"
import numpy as np, torch
HERE = os.path.dirname(__file__); sys.path[:0] = [HERE, os.path.dirname(HERE)]
import paths, osc_band_prune as obp, osc_band_measure as obm
torch.set_num_threads(4)
WIDTHS = {"3p5":[4,4,2,3], "4p5":[5,5,3,4], "5p5":[6,6,3,4], "6p5":[7,7,4,5],
          "7p5":[8,8,5,6], "8p5":[9,9,6,7], "9p0":[10,10,8,8], "10p0":[11,11,10,10]}
SPEC = {}; STATE = {"inner":None, "wrapped":None, "dm":None, "w":None, "capture":False, "pre":False}
CAP, CUR = {}, {"l":0}

def configure(model):
    c=model.config; global SPEC
    hd=getattr(c,"head_dim",None) or c.hidden_size//c.num_attention_heads
    SPEC={"nl":len(model.model.layers), "nh":c.num_attention_heads,
          "kv":c.num_key_value_heads, "np":hd//2, "group":c.num_attention_heads//c.num_key_value_heads}
    assert c.num_attention_heads % c.num_key_value_heads == 0 and hd % 2 == 0

def bits(widths):
    n=SPEC["np"]; sizes=[n] if len(widths)==1 else [n//8,n//8,n//4,n//2]
    return (sum(2*x*w for x,w in zip(sizes,widths))+(len(sizes)*16))/(2*n)

def quant(k,dm,widths):
    out=torch.empty_like(k)
    for h in range(dm.shape[0]):
        for c,w in enumerate(widths):
            d=(dm[h]==c).nonzero().flatten(); x=k[:,h,:,d]
            a=x.abs().amax(-1,keepdim=True).clamp_min(1e-30); levels=float(2**w-1)
            j=torch.round((x/a+1)*(levels/2)).clamp_(0,levels)
            out[:,h,:,d]=(j*(2/levels)-1)*a
    return out

def arm(E,widths,mode="energy",seed=1):
    n=SPEC["np"]; sizes=[n] if mode=="uniform" else [n//8,n//8,n//4,n//2]
    layers=[]
    for L in range(SPEC["nl"]):
        rows=[]
        for h in range(SPEC["kv"]):
            order=np.arange(n) if mode=="uniform" else (np.argsort(-E[L][h]) if mode=="energy" else np.random.default_rng(seed+h).permutation(n))
            pairs=np.empty(n,np.int64)
            for c,size in enumerate(sizes): pairs[order[sum(sizes[:c]):sum(sizes[:c])+size]]=c
            rows.append(np.concatenate([pairs,pairs]))
        layers.append(torch.from_numpy(np.stack(rows)))
    return layers

def install(model):
    configure(model); key="qwen3" if model.config.model_type=="qwen3" else "qwen2"
    M=__import__("transformers.models."+key+".modeling_"+key,fromlist=["x"])
    STATE.update(inner=M.apply_rotary_pos_emb,wrapped=M)
    def rope(q,k,cos,sin,unsqueeze_dim=1):
        qq,kk=STATE["inner"](q,k,cos,sin,unsqueeze_dim); L=CUR["l"]
        if STATE["capture"]:
            CAP[L]=(qq.detach().clone(),kk.detach().clone())
            if STATE["pre"]: CAP[("pre",L)]=(q.detach().clone(),k.detach().clone())
        if STATE["dm"] is not None: kk=quant(kk,STATE["dm"][L],STATE["w"])
        return qq,kk
    STATE["hook"]=rope; M.apply_rotary_pos_emb=rope
    for i,layer in enumerate(model.model.layers):
        old=layer.self_attn.forward
        def wrap(f,i=i):
            def fwd(*a,**kw): CUR["l"]=i; return f(*a,**kw)
            return fwd
        layer.self_attn.forward=wrap(old)

def forward(model,ids,a=None,w=None,capture=False):
    STATE.update(dm=a,w=w,capture=capture,pre=capture)
    with torch.no_grad(): return model(torch.tensor([ids])).logits[0]

def profile(model,prompts,n=4):
    E=np.zeros((SPEC["nl"],SPEC["kv"],SPEC["np"]))
    for pi,ids in enumerate(prompts[:n]):
        CAP.clear(); forward(model,ids,capture=True)
        layers={x for x in CAP if isinstance(x,int)}; assert layers==set(range(SPEC["nl"])), (pi,layers)
        for L,(q,k) in [(x,CAP[x]) for x in range(SPEC["nl"])]:
            e=obm.head_var(q,k,SPEC["group"],SPEC["np"])
            E[L]+=e.reshape(SPEC["kv"],SPEC["group"],SPEC["np"]).sum(1)/n
    return E

def run_model(which):
    t=time.time(); HF=paths.get("osc15_hf_dir" if which=="qwen3" else "osc03_hf_dir")
    from transformers import AutoModelForCausalLM,AutoTokenizer
    tok=AutoTokenizer.from_pretrained(HF); model=AutoModelForCausalLM.from_pretrained(HF,dtype=torch.float32,attn_implementation="eager").eval()
    install(model); prompts,emeta=obp.build_eval(tok); E=profile(model,prompts)
    grid={k:(w if SPEC["np"]==64 else w[:-1]+[w[-1]-1]) for k,w in WIDTHS.items()}
    arms={f"energy_{k}":(arm(E,w),w,bits(w)) for k,w in grid.items()}
    arms["uniform_3p5"]=(arm(E,[3],"uniform"),[3],bits([3])); arms["random_3p5"]=(arm(E,grid["3p5"],"random",7),grid["3p5"],3.5)
    out=paths.get_local("osc_band_qknorm_dir")+"/a00-bcb6c85e-"+which; os.makedirs(out+"/bench",exist_ok=True)
    bench=out+"/bench/"+dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")+".jsonl"
    meta={"event":"meta","model":which,"hf":HF,"offline":True,"eval":emeta,"bits":{k:v[2] for k,v in arms.items()},"capture":"post_rope_per_layer"}
    open(bench,"w").write(json.dumps(meta)+"\n"); agg={k:{"agree":0.,"kl":0.} for k in arms}
    for pi,ids in enumerate(prompts):
        ref=torch.log_softmax(forward(model,ids).float(),-1)
        for k,(a,w,_) in arms.items():
            agree,kl=obp.metrics(ref,forward(model,ids,a,w)); agg[k]["agree"]+=agree/len(prompts); agg[k]["kl"]+=kl/len(prompts)
            open(bench,"a").write(json.dumps({"event":"row","prompt":pi,"arm":k,"agree":agree,"kl":kl})+"\n")
        print(which,pi+1,time.time()-t,flush=True)
    settings={k:{"agree":round(v["agree"],6),"kl":round(v["kl"],6),"bits":arms[k][2],"holds":v["agree"]>=.98 and v["kl"]<=.02} for k,v in agg.items()}
    doc={"meta":meta,"settings":settings,"lowest_holding_energy":min((v["bits"] for k,v in settings.items() if k.startswith("energy_") and v["holds"]),default=None),"bench":os.path.relpath(bench,paths.get_local("osc_band_qknorm_dir")),"t_s":round(time.time()-t,1)}
    for name in ("raw.json","results.json"): json.dump(doc,open(out+"/"+name,"w"),indent=1)
    open(out+"/summary.md","w").write("# corrected "+which+"\n\n"+json.dumps(doc,indent=1)+"\n")
    return doc

def selftest():
    x=torch.randn(1,1,3,2*SPEC["np"]); a=arm(np.ones((SPEC["nl"],SPEC["kv"],SPEC["np"])),WIDTHS["3p5"])
    assert quant(x,a[0],WIDTHS["3p5"]).shape==x.shape and bits(WIDTHS["3p5"])==3.5

if __name__=="__main__":
    which=sys.argv[1] if len(sys.argv)>1 else "qwen3"; assert which in ("qwen2","qwen3")
    print(json.dumps(run_model(which),indent=1),flush=True)
