#!/usr/bin/env python3
import argparse,datetime as dt,json,os,subprocess,sys
HERE=os.path.dirname(__file__); ROOT=os.getcwd()
os.environ['HF_HUB_OFFLINE']=os.environ['TRANSFORMERS_OFFLINE']='1'
import numpy as np, torch
sys.path[:0]=[os.path.join(ROOT,'.agi/context/local-maxxing'),HERE]
import paths,osc_band_prune as obp
import importlib.util
_s=importlib.util.spec_from_file_location('fixed',os.path.join(HERE,'osc_band_kquant_qknorm_a00-bcb6c85e.py')); fixed=importlib.util.module_from_spec(_s); _s.loader.exec_module(fixed)
WIDTHS={'4.0':[5,5,3,3],'5.0':[6,6,4,4],'5.5':[7,7,4,4],'6.0':[8,8,4,4],'6.5':[9,9,5,5],'7.0':[10,10,5,5],'7.5':[11,11,6,6],'7.75':[13,13,10,10]}
ARMS=('uniform','key_only','inverse_energy','random')
def profile(model,prompts):
 E=np.zeros((fixed.SPEC['nl'],fixed.SPEC['kv'],fixed.SPEC['np']))
 for ids in prompts[:4]:
  fixed.CAP.clear(); fixed.forward(model,ids,capture=True)
  for L in range(fixed.SPEC['nl']):
   k=fixed.CAP[L][1][0].float().reshape(fixed.SPEC['kv'],-1,fixed.SPEC['np'],2).square().sum(-1).mean(1).cpu().numpy(); E[L]+=k/4
 return E
def one(which,out):
 from transformers import AutoTokenizer,AutoModelForCausalLM
 hf=paths.get('osc15_hf_dir' if which=='qwen3' else 'osc03_hf_dir'); tok=AutoTokenizer.from_pretrained(hf)
 model=AutoModelForCausalLM.from_pretrained(hf,dtype=torch.float32,attn_implementation='eager').eval(); fixed.install(model)
 prompts,emeta=obp.build_eval(tok); E=profile(model,prompts); agg={a:{} for a in ARMS}; rows=[]
 os.makedirs(out,exist_ok=True)
 for pi,ids in enumerate(prompts):
  ref=torch.log_softmax(fixed.forward(model,ids).float(),-1)
  for tag,w in WIDTHS.items():
   alloc={'uniform':fixed.arm(np.ones_like(E),w,'energy',1),'key_only':fixed.arm(E,w,'energy',1),'inverse_energy':fixed.arm(-E,w,'energy',1),'random':fixed.arm(E,w,'random',7)}
   for arm,a in alloc.items():
    ag,kl=obp.metrics(ref,fixed.forward(model,ids,a,w)); z=agg[arm].setdefault(tag,[0.,0.]); z[0]+=ag/len(prompts);z[1]+=kl/len(prompts); rows.append({'prompt':pi,'arm':arm,'tag':tag,'agree':ag,'kl':kl})
  print(which,pi+1,flush=True)
 settings={}
 for arm in ARMS:
  for tag,v in agg[arm].items(): settings[arm+'_'+tag]={'agree':round(v[0],6),'kl':round(v[1],6),'holds':v[0]>=.98 and v[1]<=.02}
 doc={'model':which,'fresh':True,'capture':'post_rope_per_layer','grid':WIDTHS,'settings':settings,'eval':emeta,'rows':rows}
 json.dump(doc,open(os.path.join(out,'results.json'),'w'),indent=1); return doc
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('which',nargs='?',choices=['qwen2','qwen3']);a=p.parse_args()
 if a.which:
  out=os.path.join(paths.get_local('osc_band_qknorm_dir'),'a00-e416bc28',a.which); print(json.dumps(one(a.which,out),indent=1)); raise SystemExit
 base=os.path.join(paths.get_local('osc_band_qknorm_dir'),'a00-e416bc28'); summary={}
 for which in ('qwen2','qwen3'):
  avail=int(subprocess.check_output(['free','-m'],text=True).splitlines()[1].split()[6]); print('available_mb',avail,flush=True); assert avail>=4000
  subprocess.run([sys.executable,__file__,which],check=True); summary[which]=json.load(open(os.path.join(base,which,'results.json')))
 json.dump(summary,open(os.path.join(base,'summary.json'),'w'),indent=1)
