#!/usr/bin/env python3
"""Fresh, single-round post-RoPE key-only grid with true-uniform controls."""
import argparse, datetime as dt, hashlib, importlib.util, json, os, subprocess, sys
os.environ["HF_HUB_OFFLINE"] = os.environ["TRANSFORMERS_OFFLINE"] = "1"
import numpy as np, torch
HERE = os.path.dirname(__file__); sys.path[:0] = [HERE, os.path.dirname(HERE)]
import paths, osc_band_prune as obp
_spec=importlib.util.spec_from_file_location("fresh_fixed",os.path.join(HERE,"osc_band_kquant_qknorm_a00-bcb6c85e.py"))
fixed=importlib.util.module_from_spec(_spec); _spec.loader.exec_module(fixed)
torch.set_num_threads(4)
TARGETS = [float(x) for x in paths.get_data("osc_fresh_grid_targets").split(",")]
print("resolved TARGETS", TARGETS, flush=True)
MODELS = dict(x.split("=", 1) for x in paths.get_data("osc_fresh_grid_models").split(","))
RUN_ID = paths.get_data("osc_fresh_grid_id")

def key_energy(k, spec):
    """Key-only per-layer energy; deliberately never reads queries."""
    n = spec["np"]
    return k.float().reshape(spec["kv"], -1, n, 2).square().sum(-1).mean(1).cpu().numpy()

def keyprofile(model, prompts, spec=fixed.SPEC):
    E = np.zeros((spec["nl"], spec["kv"], spec["np"]))
    for ids in prompts[:4]:
        fixed.CAP.clear(); fixed.forward(model, ids, capture=True)
        assert {x for x in fixed.CAP if isinstance(x, int)} == set(range(spec["nl"]))
        for layer in range(spec["nl"]):
            E[layer] += key_energy(fixed.CAP[layer][1][0], spec) / 4
    assert E.shape == (spec["nl"], spec["kv"], spec["np"])
    assert not np.allclose(E, E[0]), "capture collapsed to layer 0"
    return E

def key_widths(target):
    """Find the closest exact four-bucket integer budget; no target-label shortcut."""
    best = min(((a,b,c,d) for a in range(1,17) for b in range(1,17)
                for c in range(1,17) for d in range(1,17)),
               key=lambda w:(abs(fixed.bits(list(w))-target), np.var(w), w))
    assert abs(fixed.bits(list(best))-target) < 1e-9
    return list(best)

def uniform_width(target):
    npairs = fixed.SPEC["np"]; nearest = int(np.floor(target-8/npairs+0.5))
    assert abs(fixed.bits([nearest])-target) <= 0.5
    return [nearest]

def free_mib():
    return os.sysconf("SC_AVPHYS_PAGES") * os.sysconf("SC_PAGE_SIZE") // 2**20

def run_model(which, root):
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    hf = paths.get(MODELS[which]); out = os.path.join(root, which); os.makedirs(out, exist_ok=True)
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(hf)
    model = AutoModelForCausalLM.from_pretrained(hf, dtype=torch.float32,
                                                 attn_implementation="eager").eval()
    fixed.install(model); prompts, emeta = obp.build_eval(tok)
    E = keyprofile(model, prompts, fixed.SPEC)
    assert E.shape == (fixed.SPEC["nl"], fixed.SPEC["kv"], fixed.SPEC["np"])
    bench = os.path.join(out, "bench.jsonl"); cells = {}; stream = open(bench, "w")
    digest = hashlib.sha256(json.dumps(prompts, sort_keys=True).encode()).hexdigest()
    stream.write(json.dumps({"event":"meta","model":which,"pid":os.getpid(),"started":started,
                             "capture":"post_rope_per_layer","fresh":True,"input_sha256":digest,
                             "eval":emeta})+"\n")
    for pi, ids in enumerate(prompts):
        ref = torch.log_softmax(fixed.forward(model, ids).float(), -1)
        for target in TARGETS:
            kw = key_widths(target); uw = uniform_width(target)
            for mode, widths in (("key_only",kw),("uniform",uw),("random",kw)):
                allocation = fixed.arm(E, widths, "uniform" if mode=="uniform" else
                                       "energy" if mode=="key_only" else "random", 7)
                actual = fixed.bits(widths)
                label = "nearest uniform" if mode == "uniform" else "energy allocation"
                agree, kl = obp.metrics(ref, fixed.forward(model, ids, allocation, widths))
                cell = {"target_bits":target,"actual_bits":actual,"widths":widths,
                        "control":label,"agree":agree,"kl":kl,"holds":agree>=.98 and kl<=.02}
                cells[f"{target:g}:{mode}"] = cell
                stream.write(json.dumps({"prompt":pi,"target_bits":target,"arm":mode,
                                         "widths":widths,"actual_bits":actual,
                                         "agree":agree,"kl":kl})+"\n")
    stream.close(); settings = {}
    # Recompute aggregates from the just-written rows, never from inherited summaries.
    rows = [json.loads(x) for x in open(bench)][1:]
    for target in TARGETS:
        for mode in ("key_only","uniform","random"):
            rs = [r for r in rows if r["target_bits"]==target and r["arm"]==mode]
            assert len(rs)==len(prompts) and all(r["actual_bits"]==fixed.bits(r["widths"]) for r in rs)
            widths = rs[0]["widths"]; agree=sum(r["agree"] for r in rs)/len(rs); kl=sum(r["kl"] for r in rs)/len(rs)
            settings[f"{target:g}:{mode}"] = {"target_bits":target,"actual_bits":fixed.bits(widths),
                "widths":widths,"control":"nearest uniform" if mode=="uniform" else "energy allocation",
                "agree":round(agree,6),"kl":round(kl,6),"holds":agree>=.98 and kl<=.02}
    doc={"model":which,"pid":os.getpid(),"started":started,"finished":dt.datetime.now(dt.timezone.utc).isoformat(),
         "capture":"post_rope_per_layer","fresh_provenance":{"source":"this_process","reused_cells":0,
         "input_sha256":digest,"bench":"bench.jsonl"},"np":fixed.SPEC["np"],"settings":settings}
    with open(os.path.join(out,"results.json"),"w") as f: json.dump(doc,f,indent=1)
    return doc

def main():
    p=argparse.ArgumentParser(); p.add_argument("--child",choices=list(MODELS)); p.add_argument("--root"); a=p.parse_args()
    if a.child: print(json.dumps(run_model(a.child,a.root))); return
    stamp=dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    root=os.path.join(paths.get_local("osc_band_qknorm_dir"),RUN_ID,stamp); os.makedirs(root)
    for which in MODELS:
        available=free_mib(); assert available>=4000, (which,available)
        subprocess.run([sys.executable,__file__,"--child",which,"--root",root],check=True)
    docs={x:json.load(open(os.path.join(root,x,"results.json"))) for x in MODELS}
    summary={"experiment":RUN_ID,"run_dir":stamp,"models":docs,"cells":24,
             "provenance":"all 24 cells produced by this dated run; no prior results read"}
    with open(os.path.join(root,"summary.json"),"w") as f: json.dump(summary,f,indent=1)
    print(json.dumps(summary,indent=1))
if __name__=="__main__": main()
