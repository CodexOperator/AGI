import importlib.util, os, sys, json
import numpy as np, torch
torch.set_num_threads(4)
here='.agi/context/local-maxxing/osc'
sys.path.insert(0,os.path.dirname(here)); sys.path.insert(0,here)
import osc_band_prune as obp
spec=importlib.util.spec_from_file_location('kq',os.path.join(here,'osc_band_kquant_a00-527993c5.py'))
kq=importlib.util.module_from_spec(spec); spec.loader.exec_module(kq)
kq.CANDS=kq.candidates()
CAP={}
orig_rope=kq.make_rope
def cap_rope(orig):
    def f(q,k,cos,sin,unsqueeze_dim=1):
        qq,kk=orig(q,k,cos,sin,unsqueeze_dim)
        CAP.setdefault(kq.CUR["l"],[]).append((float(kk.abs().max()), float(kk.abs().mean())))
        return qq,kk
    return f
from transformers import AutoTokenizer, AutoModelForCausalLM
tok=AutoTokenizer.from_pretrained(kq.HF)
model=AutoModelForCausalLM.from_pretrained(kq.HF,dtype=torch.float32,attn_implementation="eager").eval()
kq.install(model)
prompts,meta=obp.build_eval(tok)
ids=torch.tensor([prompts[0][:128]])
def run(alloc):
    kq.ALLOC["a"]=alloc
    with torch.no_grad():
        return model(ids).logits[0].float()
ref=run(None)
def uni(w): return [[("pair",np.zeros(32,dtype=np.int64),[w]) for _ in range(kq.KVD)] for _ in range(24)]
for w in (16,8,5,4):
    lg=run(uni(w))
    a,kl=obp.metrics(torch.log_softmax(ref,-1),lg)
    d=(lg.log_softmax(-1)-torch.log_softmax(ref,-1))
    print('w',w,'agree',round(a,5),'kl',round(kl,5),'maxabs_logit_diff',round(float((lg-ref).abs().max()),4))
# raw k quant error at w=8, layer 0
kq.ALLOC["a"]=uni(8)
CAP.clear()
run(uni(8))
