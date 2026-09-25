#!/usr/bin/env python3
import argparse, importlib.util, json, os, sys
os.environ['HF_HUB_OFFLINE']=os.environ['TRANSFORMERS_OFFLINE']='1'
HERE=os.path.dirname(__file__); ROOT=os.getcwd(); sys.path[:0]=[os.path.join(ROOT,'.agi/context/local-maxxing'),HERE]
import numpy as np, torch, paths, osc_band_prune as obp
_s=importlib.util.spec_from_file_location('fixed',os.path.join(HERE,'osc_band_kquant_qknorm_a00-bcb6c85e.py')); fixed=importlib.util.module_from_spec(_s); _s.loader.exec_module(fixed)
TAGS=('4.0','4.5','5.0','5.5','6.0','6.5','7.0','7.5','7.75')
GRID={32:{'4.0':[3,3,3,3],'4.5':[5,5,3,3],'5.0':[4,4,4,4],'5.5':[3,3,5,5],'6.0':[5,5,5,5],'6.5':[4,4,6,6],'7.0':[6,6,6,6],'7.5':[5,5,7,7],'7.75':[6,6,7,7]},64:{'4.0':[2,2,4,4],'4.5':[1,1,5,5],'5.0':[3,3,5,5],'5.5':[2,2,6,6],'6.0':[1,1,7,7],'6.5':[3,3,7,7],'7.0':[2,2,8,8],'7.5':[1,1,9,9],'7.75':[2,2,9,9]}}
ARMS=('index_order','key_only','inverse_energy','random')
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
 prompts,emeta=obp.build_eval(tok); E=profile(model,prompts); out=paths.get_local('osc_band_qknorm_dir')+'/a00-a7060fdc-'+which; os.makedirs(out,exist_ok=True); path=out+'/cells.jsonl'; done=set()
 if os.path.exists(path):
  with open(path) as f: done={json.loads(x)['cell'] for x in f if x.strip()}
 n=fixed.SPEC['np']; grid=GRID[n]; fh=open(path,'a')
 for tag in TAGS:
  w=grid[tag]
  for arm in ARMS:
   key=f'{arm}@{tag}'
   if key in done: continue
   vals=[0.,0.]
   for ids in prompts:
    ref=torch.log_softmax(fixed.forward(model,ids).float(),-1); a=fixed.arm(np.ones_like(E) if arm=='index_order' else (-E if arm=='inverse_energy' else E),w,'energy' if arm!='random' else 'random',1 if arm!='random' else 7); ag,kl=obp.metrics(ref,fixed.forward(model,ids,a,w)); vals[0]+=ag/len(prompts); vals[1]+=kl/len(prompts)
   rec={'model':which,'np':n,'cell':key,'widths':w,'agree':round(vals[0],6),'kl':round(vals[1],6),'holds':vals[0]>=.98 and vals[1]<=.02}
   fh.write(json.dumps(rec)+'\n'); fh.flush(); print(rec,flush=True)
 fh.close(); json.dump({'model':which,'np':n,'eval':emeta,'complete':True},open(out+'/meta.json','w'),indent=1)
if __name__=='__main__':
 p=argparse.ArgumentParser(); p.add_argument('which',choices=('qwen2','qwen3')); run(p.parse_args().which)
