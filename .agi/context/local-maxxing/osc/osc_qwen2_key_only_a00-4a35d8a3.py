#!/usr/bin/env python3
"""Run only the missing Qwen2.5 key-only cell, reusing the closed sweep helpers."""
import datetime as dt, importlib.util, json, os, sys
import numpy as np, torch
HERE=os.path.dirname(__file__); sys.path[:0]=[HERE,os.path.dirname(HERE)]
import paths, osc_band_prune as obp
spec=importlib.util.spec_from_file_location("sweep",os.path.join(HERE,"osc_band_sweep_a00-31ae16be.py"))
sweep=importlib.util.module_from_spec(spec); spec.loader.exec_module(sweep)
KID="a00-4a35d8a3-829565"
def main():
 root=os.path.join(paths.get_local("osc_band_qknorm_dir"),KID)
 prof=os.path.join(paths.get_local("osc_band_qknorm_dir"),"a00-31ae16be-c0ddf6","profile-qwen2","profiles.json")
 d=json.load(open(prof)); a=d["architecture"]
 E=np.array([[d["cells"][f"L{L}H{h*a['group']}"]["key_only_energy"] for h in range(a["kv_heads"])] for L in range(a["layers"])])
 from transformers import AutoTokenizer,AutoModelForCausalLM
 hf=paths.get("osc03_hf_dir")
 tok=AutoTokenizer.from_pretrained(hf)
 m=AutoModelForCausalLM.from_pretrained(hf,dtype=torch.float32,attn_implementation="eager").eval()
 prompts,_=obp.build_eval(tok)
 out=os.path.join(root,"qwen2-key-key_only"); os.makedirs(out,exist_ok=True)
 res=sweep.run(m,prompts,E,out)
 json.dump({"model":"Qwen2.5","method":"key_only","rows":res},open(os.path.join(root,"summary.json"),"w"),indent=1)
 print(json.dumps({"cell":"Qwen2.5/key_only","rows":res},indent=1))
if __name__=="__main__": main()
