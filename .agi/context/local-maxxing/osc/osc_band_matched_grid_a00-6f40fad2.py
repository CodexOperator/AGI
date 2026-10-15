#!/usr/bin/env python3
import argparse,datetime as dt,json,os,subprocess,sys,time
HERE=os.path.dirname(__file__); ROOT=os.getcwd()
os.environ["HF_HUB_OFFLINE"]=os.environ["TRANSFORMERS_OFFLINE"]="1"
import numpy as np, torch
sys.path.insert(0,os.path.join(ROOT,".agi/context/local-maxxing"));sys.path.insert(0,os.path.join(ROOT,".agi/context/local-maxxing/osc"))
import paths,osc_band_prune as obp
import importlib.util
_s=importlib.util.spec_from_file_location("fixed",os.path.join(ROOT,".agi/context/local-maxxing/osc/osc_band_kquant_qknorm_a00-bcb6c85e.py"));fixed=importlib.util.module_from_spec(_s);_s.loader.exec_module(fixed)
_s=importlib.util.spec_from_file_location("keycode",os.path.join(ROOT,".agi/context/local-maxxing/osc/osc_qwen2_key_only_a00-4a35d8a3.py"));keycode=importlib.util.module_from_spec(_s);_s.loader.exec_module(keycode)
BITS={"3p5":3.5,"7p75":7.75,"9p0":9.0,"10p75":10.75}
W=keycode.sweep.W; S=keycode.sweep.SIZES
def keyprofile(model,prompts,spec):
 E=np.zeros((spec["nl"],spec["kv"],spec["np"]))
 for ids in prompts[:4]:
  fixed.CAP.clear(); fixed.forward(model,ids,capture=True)
  assert set(x for x in fixed.CAP if isinstance(x,int))==set(range(spec["nl"]))
  for L in range(spec["nl"]):
   k=fixed.CAP[L][1][0].float().reshape(spec["kv"],-1,spec["np"],2).square().sum(-1).mean(1).cpu().numpy()
   E[L]+=k/4
 return E
def one(which,out):
 from transformers import AutoTokenizer,AutoModelForCausalLM
 hf=paths.get("osc15_hf_dir" if which=="qwen3" else "osc03_hf_dir")
 tok=AutoTokenizer.from_pretrained(hf); model=AutoModelForCausalLM.from_pretrained(hf,dtype=torch.float32,attn_implementation="eager").eval()
 fixed.install(model); spec=fixed.SPEC
 if which=="qwen3": assert not isinstance(model.model.layers[0].self_attn.k_norm,torch.nn.Identity)
 prompts,emeta=obp.build_eval(tok); E=keyprofile(model,prompts,spec)
 assert E.shape==(spec["nl"],spec["kv"],spec["np"])
 alloc=keycode.sweep.arms(E); print("SPEC",spec,"E",E.shape,flush=True); settings={}
 bench=os.path.join(out,"bench",dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")+".jsonl"); os.makedirs(os.path.dirname(bench),exist_ok=True)
 f=open(bench,"w"); f.write(json.dumps({"model":which,"capture":"post_rope_per_layer","fresh":True,"eval":emeta,"grid":BITS})+"\n")
 agg={}
 for pi,ids in enumerate(prompts):
  ref=fixed.forward(model,ids); ref=torch.log_softmax(ref.float(),-1)
  for tag,w in W.items():
   if tag not in BITS: continue
   for mode in ("key_only","uniform","random"):
    if mode=="key_only": a,wused=(alloc[tag] if spec["np"]==64 else (fixed.arm(E,w,"energy",7),w))
    else:
     a=fixed.arm(E,w,mode,7); wused=[w[0]] if mode=="uniform" else w
    if pi==0: print("DM",tag,mode,a[0].shape,[(a[0]==c).sum().item() for c in range(4)],flush=True)
    outp=fixed.forward(model,ids,a,wused); agree,kl=obp.metrics(ref,outp)
    key=mode+"_"+tag; q=agg.setdefault(key,[0.,0.]); q[0]+=agree/len(prompts);q[1]+=kl/len(prompts)
    f.write(json.dumps({"prompt":pi,"arm":key,"agree":agree,"kl":kl,"widths":wused})+"\n")
  print(which,pi+1,flush=True)
 f.close()
 for k,v in agg.items():
  tag=k.rsplit("_",1)[1]; settings[k]={"target_bits":BITS[tag],"agree":round(v[0],6),"kl":round(v[1],6),"holds":v[0]>=.98 and v[1]<=.02,"actual_bits":BITS[tag],"representable_widths":W[tag]}
 doc={"model":which,"fresh_post_rope_profile":True,"capture":"post_rope_per_layer","settings":settings,"bench":os.path.relpath(bench,out)}
 json.dump(doc,open(os.path.join(out,"results.json"),"w"),indent=1); return doc
if __name__=="__main__":
 p=argparse.ArgumentParser();p.add_argument("which",nargs="?",choices=["qwen2","qwen3"]);p.add_argument("--child",action="store_true");a=p.parse_args()
 if a.which:
  out=os.path.join(paths.get_local("osc_band_qknorm_dir"),"a00-6f40fad2-eca451",a.which);os.makedirs(out,exist_ok=True)
  print(json.dumps(one(a.which,out),indent=1)); raise SystemExit
 free=int(subprocess.check_output(["free","-m"],text=True).splitlines()[1].split()[6]) if False else None
 for which in ("qwen2","qwen3"):
  avail=int(subprocess.check_output(["free","-m"],text=True).splitlines()[1].split()[6]); print("available_mb",avail,flush=True); assert avail>=4000
  cmd=[sys.executable,__file__,which,"--child"]; r=subprocess.run(cmd); assert r.returncode==0
  print(which,"exit",r.returncode,flush=True)
 summary={}
 for which in ("qwen2","qwen3"):
  pth=os.path.join(paths.get_local("osc_band_qknorm_dir"),"a00-6f40fad2-eca451",which,"results.json")
  summary[which]=json.load(open(pth))
 json.dump(summary,open(os.path.join(paths.get_local("osc_band_qknorm_dir"),"a00-6f40fad2-eca451","summary.json"),"w"),indent=1)
