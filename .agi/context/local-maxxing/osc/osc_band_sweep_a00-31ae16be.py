#!/usr/bin/env python3
"""Measure three persisted key-energy allocators on the shared OSC.04 eval."""
import datetime as dt, json, os, sys
import numpy as np, torch
HERE=os.path.dirname(__file__); sys.path[:0]=[HERE,os.path.dirname(HERE)]
import paths, osc_band_prune as obp, osc_band_measure as obm
import importlib.util
_spec=importlib.util.spec_from_file_location("osc_band_kquant", os.path.join(HERE,"osc_band_kquant_a00-86466b78.py"))
_k=importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_k)
quant, avg_bits = _k.quant, _k.avg_bits
KID="a00-31ae16be-c0ddf6"; ROOT=os.path.dirname(HERE)
BITS={"3p5":3.5,"4p5":4.5,"4p75":4.75,"5p75":5.75,"6p75":6.75,"7p75":7.75,"9p0":9.0,"10p75":10.75}
# widths are the established 4 energy classes; each row has four class widths.
W={"3p5":[4,4,2,2],"4p5":[6,6,4,4],"4p75":[7,7,5,5],"5p75":[9,9,6,6],"6p75":[11,11,8,8],"7p75":[13,13,10,10],"9p0":[15,15,12,12],"10p75":[16,16,16,16]}
SIZES={"3p5":[4,4,8,16],"4p5":[4,4,8,16],"4p75":[4,4,8,16],"5p75":[4,4,8,16],"6p75":[4,4,8,16],"7p75":[4,4,8,16],"9p0":[4,4,8,16],"10p75":[4,4,8,16]}
def arms(E):
  out={}
  for tag in BITS:
    widths=W[tag]; sizes=SIZES[tag]
    dm=[]
    for L in range(E.shape[0]):
      rows=[]
      for h in range(E.shape[1]):
        n=E.shape[2]
        # The old 32-pair sizes left Qwen3's second 32 channels unassigned.
        ns=sizes if n==32 else [n//8,n//8,n//4,n//2]
        order=np.argsort(-E[L,h]); pc=np.empty(n,np.int64); i=0
        for c,size in enumerate(ns): pc[order[i:i+size]]=c; i+=size
        rows.append(np.r_[pc,pc])
      dm.append(torch.from_numpy(np.stack(rows)))
    out[tag]=(dm,widths)
  return out
def install(model):
  import transformers.models.qwen2.modeling_qwen2 as m2
  import transformers.models.qwen3.modeling_qwen3 as m3
  M=m3 if model.config.model_type=="qwen3" else m2
  obp.install(model); inner=M.apply_rotary_pos_emb; state={"dm":None,"w":None}
  def rope(q,k,cos,sin,unsqueeze_dim=1):
    qq,kk=inner(q,k,cos,sin,unsqueeze_dim)
    if state["dm"] is not None: kk=quant(kk,state["dm"][obp.CUR["l"]],state["w"])
    return qq,kk
  M.apply_rotary_pos_emb=rope
  return state
def run(model,prompts, E, outdir):
  state=install(model); dm=arms(np.asarray(E)); refsum={t:[0.,0.] for t in BITS}
  bench=os.path.join(outdir,"bench",dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")+".jsonl"); os.makedirs(os.path.dirname(bench),exist_ok=True)
  with open(bench,"w") as f:
   for pi,ids in enumerate(prompts):
    with torch.no_grad(): ref=model(torch.tensor([ids])).logits[0]
    rp=torch.log_softmax(ref.float(),-1)
    for tag,(classes,widths) in dm.items():
     state["dm"],state["w"]=classes,widths
     with torch.no_grad(): out=model(torch.tensor([ids])).logits[0]
     a,k=obp.metrics(rp,out); refsum[tag][0]+=a/len(prompts); refsum[tag][1]+=k/len(prompts)
     f.write(json.dumps({"prompt":pi,"bits":BITS[tag],"agree":a,"kl":k})+"\n")
  res={t:{"bits":BITS[t],"agree":round(v[0],6),"kl":round(v[1],6),"holds":v[0]>=.98 and v[1]<=.02} for t,v in refsum.items()}
  json.dump({"method":outdir.split("-")[-1],"rows":res,"bench":os.path.relpath(bench,outdir)},open(os.path.join(outdir,"results.json"),"w"),indent=1)
  return res
def profile_cells(path,kind):
 d=json.load(open(path)); return np.array([[d["cells"][f"L{L}H{h*2+g}"][kind] for g in range(2)] for L in range(28) for h in []]).reshape(0)
def q2_cells():
 from osc_band_profile_qwen3_a00_edd08f38 import install as pi, profiles
 hf=paths.get("osc03_hf_dir"); from transformers import AutoTokenizer,AutoModelForCausalLM
 tok=AutoTokenizer.from_pretrained(hf); m=AutoModelForCausalLM.from_pretrained(hf,dtype=torch.float32,attn_implementation="eager").eval()
 sp,cap,key=pi(m); ps,meta=obp.build_eval(tok); E,K=profiles(m,ps,sp,cap)
 return np.array([[E[L,h*2+g] for g in range(2)] for L in range(sp["layers"]) for h in [0]])
def main():
 outroot=os.path.join(paths.get_local("osc_band_qknorm_dir"),KID); os.makedirs(outroot,exist_ok=True)
 q2dir=os.path.join(outroot,"profile-qwen2"); os.makedirs(q2dir,exist_ok=True)
 # fresh Qwen2 capture, imported capture functions
 if not os.path.exists(os.path.join(q2dir,"profiles.json")):
  from osc_band_profile_qwen3_a00_edd08f38 import install as pi,profiles
  hf=paths.get("osc03_hf_dir"); from transformers import AutoTokenizer,AutoModelForCausalLM
  tok=AutoTokenizer.from_pretrained(hf); m=AutoModelForCausalLM.from_pretrained(hf,dtype=torch.float32,attn_implementation="eager").eval()
  sp,cap,key=pi(m); ps,meta=obp.build_eval(tok); E,K=profiles(m,ps,sp,cap)
  cells={f"L{L}H{h*sp['group']}":{"profile_pooled":E[L,h].tolist(),"key_only_energy":K[L,h].tolist()} for L in range(sp["layers"]) for h in range(sp["kv_heads"])}
  json.dump({"model":"Qwen2.5","architecture":sp,"cells":cells},open(os.path.join(q2dir,"profiles.json"),"w"),indent=1)
 # persisted Qwen3 profile is the source for both requested cells
 q3=json.load(open(os.path.join(paths.get_local("osc_band_qknorm_dir"),"a00-edd08f38-profile-qwen3","profiles.json")))
 def q3arr(kind): return np.array([[q3["cells"][f"L{L}H{h*2}"][kind] for h in range(8)] for L in range(28)])
 q2=json.load(open(os.path.join(q2dir,"profiles.json")))
 def q2arr(kind): return np.array([[q2["cells"][f"L{L}H{h*7}"][kind] for h in range(2)] for L in range(24)])
 # actual sweep models (one model per process to keep memory bounded)
 results={}
 from transformers import AutoTokenizer,AutoModelForCausalLM
 for label,hf,arrs in [("qwen3-profile",paths.get("osc15_hf_dir"),[("profile_pooled",q3arr("profile_pooled")),("key_only",q3arr("key_only_energy"))]),("qwen2-key",paths.get("osc03_hf_dir"),[("key_only",q2arr("key_only_energy"))])]:
  tok=AutoTokenizer.from_pretrained(hf); m=AutoModelForCausalLM.from_pretrained(hf,dtype=torch.float32,attn_implementation="eager").eval(); prompts,_=obp.build_eval(tok)
  for meth,E in arrs:
   d=os.path.join(outroot,label+"-"+meth); os.makedirs(d,exist_ok=True); results[label+"-"+meth]=run(m,prompts,E,d)
 json.dump(results,open(os.path.join(outroot,"summary.json"),"w"),indent=1)
if __name__=="__main__": main()
