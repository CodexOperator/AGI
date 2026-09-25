#!/usr/bin/env python3
import argparse, importlib.util, itertools, json, os, subprocess, sys
os.environ['HF_HUB_OFFLINE']=os.environ['TRANSFORMERS_OFFLINE']='1'
HERE=os.path.dirname(__file__); ROOT=os.getcwd(); sys.path[:0]=[os.path.join(ROOT,'.agi/context/local-maxxing'),HERE]
import numpy as np, torch, paths, osc_band_prune as obp
s=importlib.util.spec_from_file_location('fixed',os.path.join(HERE,'osc_band_kquant_qknorm_a00-bcb6c85e.py')); fixed=importlib.util.module_from_spec(s); s.loader.exec_module(fixed)
TAGS=('4.0','4.5','5.0','5.5','6.0','6.5','7.0','7.5','7.75'); ARMS=('index_order','key_only','inverse_energy','random')
def search(np,target):
 old=fixed.SPEC.get('np'); fixed.SPEC={'np':np}
 sols=[]
 for w in itertools.product(range(1,17),repeat=4):
  if w[0]>=w[1]>=w[2]>=w[3] and abs(fixed.bits(w)-target)<.01: sols.append((w[0]-w[3],w))
 fixed.SPEC['np']=old
 pair=[x for x in sols if x[1][0]==x[1][1] and x[1][2]==x[1][3]]
 return min(pair or sols,key=lambda x:(x[0],x[1]))[1] if sols else None
def grid(np): return {t:search(np,float(t)) for t in TAGS}
def profile(model,prompts):
 E=np.zeros((fixed.SPEC['nl'],fixed.SPEC['kv'],fixed.SPEC['np']))
 for ids in prompts[:4]:
  fixed.CAP.clear(); fixed.forward(model,ids,capture=True)
  for L in range(fixed.SPEC['nl']):
   k=fixed.CAP[L][1][0].float().reshape(fixed.SPEC['kv'],-1,fixed.SPEC['np'],2).square().sum(-1).mean(1).cpu().numpy(); E[L]+=k/4
 return E
def run(which):
 from transformers import AutoTokenizer,AutoModelForCausalLM
 hf=paths.get('osc15_hf_dir' if which=='qwen3' else 'osc03_hf_dir'); tok=AutoTokenizer.from_pretrained(hf); model=AutoModelForCausalLM.from_pretrained(hf,dtype=torch.float32,attn_implementation='eager').eval(); fixed.install(model)
 prompts,emeta=obp.build_eval(tok); E=profile(model,prompts); npv=fixed.SPEC['np']; g=grid(npv); fixed.configure(model); out=paths.get_local('osc_band_qknorm_dir')+'/a00-395e2a3e-'+which; os.makedirs(out,exist_ok=True); path=out+'/cells.jsonl'; done=set()
 if os.path.exists(path): done={json.loads(x)['cell'] for x in open(path) if x.strip()}
 with open(path,'a') as fh:
  for tag in TAGS:
   w=g[tag]
   for arm in ARMS:
    key=f'{arm}@{tag}'
    if key in done: continue
    vals=[0.,0.]; src=np.ones_like(E) if arm=='index_order' else (-E if arm=='inverse_energy' else E)
    for ids in prompts:
     ref=torch.log_softmax(fixed.forward(model,ids).float(),-1); a=fixed.arm(src,w,'random' if arm=='random' else 'energy',7 if arm=='random' else 1); ag,kl=obp.metrics(ref,fixed.forward(model,ids,a,w)); vals[0]+=ag/len(prompts); vals[1]+=kl/len(prompts)
    rec={'model':which,'np':npv,'cell':key,'widths':w,'bits':fixed.bits(w),'agree':vals[0],'kl':vals[1],'holds':vals[0]>=.98 and vals[1]<=.02}; fh.write(json.dumps(rec)+'\n'); fh.flush(); print(rec,flush=True)
 with open(out+'/meta.json','w') as f: json.dump({'model':which,'np':npv,'grid':g,'eval':emeta},f,indent=1)
if __name__=='__main__':
 p=argparse.ArgumentParser(); p.add_argument('which',choices=('qwen2','qwen3')); p.add_argument('--check',action='store_true'); a=p.parse_args()
 if a.check: print({n:grid(n) for n in (32,64)})
 else: run(a.which)
