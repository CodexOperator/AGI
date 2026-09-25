#!/usr/bin/env python3
"""TMM.157 anchor: independently re-derive widths=[13,13,10,10] (qwen2, key_only)
against the CURRENT fixed module, to commit the reproduction as bytes rather than
prose. Historical reading (mislabeled '7.75' at the time): agree=0.991699,
kl=0.000489, representable_widths=[13,13,10,10] -- recorded in
datasets/osc-band/2026-09-24-qknorm/a00-6f40fad2-eca451/qwen2/results.json,
settings.key_only_7p75. fixed.bits([13,13,10,10]) is 11.75, not 7.75 (TMM.154).
Reuses the exact profile()/arm()/bits()/forward() logic from
osc_band_derived_a00-395e2a3e.py -- no re-derivation of that logic here."""
import importlib.util, json, os, sys
os.environ['HF_HUB_OFFLINE'] = os.environ['TRANSFORMERS_OFFLINE'] = '1'
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.getcwd()
sys.path[:0] = [os.path.join(ROOT, '.agi/context/local-maxxing'), HERE]
import numpy as np, torch, paths, osc_band_prune as obp
torch.set_num_threads(4)
s = importlib.util.spec_from_file_location('fixed', os.path.join(HERE, 'osc_band_kquant_qknorm_a00-bcb6c85e.py'))
fixed = importlib.util.module_from_spec(s); s.loader.exec_module(fixed)


def profile(model, prompts):
    E = np.zeros((fixed.SPEC['nl'], fixed.SPEC['kv'], fixed.SPEC['np']))
    for ids in prompts[:4]:
        fixed.CAP.clear(); fixed.forward(model, ids, capture=True)
        for L in range(fixed.SPEC['nl']):
            k = fixed.CAP[L][1][0].float().reshape(fixed.SPEC['kv'], -1, fixed.SPEC['np'], 2).square().sum(-1).mean(1).cpu().numpy()
            E[L] += k / 4
    return E


def main():
    from transformers import AutoTokenizer, AutoModelForCausalLM
    hf = paths.get('osc03_hf_dir')
    tok = AutoTokenizer.from_pretrained(hf)
    model = AutoModelForCausalLM.from_pretrained(hf, dtype=torch.float32, attn_implementation='eager').eval()
    fixed.install(model)
    prompts, emeta = obp.build_eval(tok)
    E = profile(model, prompts)
    npv = fixed.SPEC['np']
    w = (13, 13, 10, 10)
    b = fixed.bits(w)
    a = fixed.arm(E, list(w), 'energy', 1)
    vals = [0., 0.]
    for ids in prompts:
        ref = torch.log_softmax(fixed.forward(model, ids).float(), -1)
        out = fixed.forward(model, ids, a, list(w))
        agree, kl = obp.metrics(ref, out)
        vals[0] += agree / len(prompts); vals[1] += kl / len(prompts)
    rec = {
        'model': 'qwen2', 'np': npv, 'cell': 'key_only@anchor-13-13-10-10',
        'widths': list(w), 'bits': b, 'agree': vals[0], 'kl': vals[1],
        'holds': vals[0] >= .98 and vals[1] <= .02,
        'purpose': 'TMM.157 reproducibility anchor vs historical mislabeled-7.75 reading '
                   '(a00-6f40fad2-eca451/qwen2/results.json settings.key_only_7p75: '
                   'agree=0.991699, kl=0.000489, representable_widths=[13,13,10,10])',
    }
    out_dir = os.path.join(ROOT, 'datasets/osc-band/2026-09-24-qknorm/a00-395e2a3e-qwen2')
    os.makedirs(out_dir, exist_ok=True)
    with open(os.path.join(out_dir, 'anchor.jsonl'), 'a') as fh:
        fh.write(json.dumps(rec) + '\n')
    print(json.dumps(rec, indent=1), flush=True)


if __name__ == '__main__':
    main()
