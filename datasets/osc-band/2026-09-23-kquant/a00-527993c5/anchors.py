import importlib.util, os, sys, json, time
import numpy as np, torch
torch.set_num_threads(4)
here='.agi/context/local-maxxing/osc'
sys.path.insert(0,os.path.dirname(here)); sys.path.insert(0,here)
import paths, osc_band_prune as obp
spec=importlib.util.spec_from_file_location('kq',os.path.join(here,'osc_band_kquant_a00-527993c5.py'))
kq=importlib.util.module_from_spec(spec); spec.loader.exec_module(kq)
kq.CANDS=kq.candidates()
from transformers import AutoTokenizer, AutoModelForCausalLM
t0=time.time()
tok=AutoTokenizer.from_pretrained(kq.HF)
model=AutoModelForCausalLM.from_pretrained(kq.HF,dtype=torch.float32,attn_implementation="eager").eval()
kq.install(model)
prompts,meta=obp.build_eval(tok)
def uni(w): return [[("pair",np.zeros(32,dtype=np.int64),[w]) for _ in range(kq.KVD)] for _ in range(24)]
WS=[6,8,12,16]
agg={w:{"agree":0.0,"kl":0.0} for w in WS}
for pi,ids in enumerate(prompts):
    it=torch.tensor([ids])
    kq.ALLOC["a"]=None
    with torch.no_grad(): ref=torch.log_softmax(model(it).logits[0].float(),-1)
    for w in WS:
        kq.ALLOC["a"]=uni(w)
        with torch.no_grad(): lg=model(it).logits[0]
        a,kl=obp.metrics(ref,lg)
        agg[w]["agree"]+=a/len(prompts); agg[w]["kl"]+=kl/len(prompts)
    print("prompt",pi+1,round(time.time()-t0),flush=True)
out={str(w):{"agree":round(agg[w]["agree"],6),"kl":round(agg[w]["kl"],6),
             "avg_bits":round(w+0.25,4),"avg_data_bits":float(w),"C":1} for w in WS}
out["_note"]="in-eval uniform absmax key-precision anchor; w=16 is the lossless-path control"
json.dump(out,open(os.path.join(paths.get_local('osc_band_kquant_dir'),'a00-527993c5','anchors.json'),'w'),indent=1)
print(json.dumps(out,indent=1))
