#!/usr/bin/env python3
"""Complete the one missing Qwen2.5 key-only energy cell; one model/process."""
import json, os, sys
import numpy as np, torch
HERE=os.path.dirname(__file__); sys.path[:0]=[HERE,os.path.dirname(HERE)]
import paths, osc_band_prune as obp
import importlib.util
_spec=importlib.util.spec_from_file_location("sweep",os.path.join(HERE,"osc_band_sweep_a00-31ae16be.py"))
_sweep=importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_sweep)
run=_sweep.run
KID="a00-c564b605-de0ef2"
def q2_array(kind):
    root=os.path.join(paths.get_local("osc_band_qknorm_dir"),"a00-31ae16be-c0ddf6","profile-qwen2")
    d=json.load(open(os.path.join(root,"profiles.json")))
    return np.array([[d["cells"][f"L{L}H{h*7}"][kind] for h in range(2)] for L in range(24)])
def main():
    from transformers import AutoTokenizer, AutoModelForCausalLM
    hf=paths.get("osc03_hf_dir")
    tok=AutoTokenizer.from_pretrained(hf)
    model=AutoModelForCausalLM.from_pretrained(hf,dtype=torch.float32,attn_implementation="eager").eval()
    prompts,_=obp.build_eval(tok)
    outroot=os.path.join(paths.get_local("osc_band_qknorm_dir"),KID)
    out=os.path.join(outroot,"qwen2-key_only"); os.makedirs(out,exist_ok=True)
    result=run(model,prompts,q2_array("key_only_energy"),out)
    json.dump({"method":"key_only_energy","model":"Qwen2.5","rows":result},open(os.path.join(out,"result.json"),"w"),indent=1)
    print(json.dumps(result,indent=1))
if __name__=="__main__": main()
