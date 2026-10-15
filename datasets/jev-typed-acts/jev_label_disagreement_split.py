"""TM.74 -- is the verdict held-out q1 ECE floor LABEL DISAGREEMENT? Four act-level splits
(gold 3/3 same q1 label, self 3/3 same model choice, corr 3/3 same correctness, graph
verdict-node class == linked experiment class) on the committed scrub rows, TM.57 protocol.
Pure NumPy, CPU, 0 API. Run: python3 jev_label_disagreement_split.py [out.jsonl]
"""
import json, sys, glob, numpy as np
from jev_isotonic_residual import ece, isotonic, apply_map
D = __file__.rsplit('/', 1)[0]; W = D + '/../../../..'; SEEDS = [20260918, 1, 7, 42, 1234]
def fm(p):  # minimal frontmatter reader: scalars + indented/inline list fields
    o = {}; k = None
    for l in open(p).read().split('\n')[1:]:
        if l.startswith('---'): break
        if l.startswith('  - '):
            if not isinstance(o.get(k), list): o[k] = []
            o[k].append(l[4:].strip())
        elif ':' in l and not l.startswith(' '):
            k, v = l.split(':', 1); v = v.strip(); o[k] = [] if v in ('', '[]') else v
    return o
def L(x): return x if isinstance(x, list) else [t.strip().strip('\'"') for t in str(x).strip('[]').split(',') if t.strip()]
NI = {}
for p in glob.glob(W + '/.agi/nodes/**/*.md', recursive=True):
    f = fm(p)
    if f.get('id'): NI[f['id']] = (f.get('verdict', ''), L(f.get('parents')) + L(f.get('evidence_runs')))
def gsplit(a):  # True = verdict class agrees with a resolvable linked experiment class
    v = NI.get(a)
    if not v: return None
    for e in v[1]:
        if e.startswith('experiment:') and NI.get(e, ('', ''))[0]: return v[0].split(':')[0] == NI[e][0].split(':')[0]
    return None
raw = [json.loads(l) for l in open(D + '/acts_replay_scrub.jsonl')]; raw = [r for r in raw if r['kind'] == 'verdict']
CL = sorted({k for r in raw for k in r['answers'].get('q1', {}).get('probabilities', {})})
A = {}
for r in raw: A.setdefault(r['act'], []).append(r)
n_raw = len(A); A = {k: sorted(v, key=lambda r: r['repeat']) for k, v in A.items()}
A = {k: v for k, v in A.items() if len(v) == 3 and all(r['labels'].get('q1') and r['answers'].get('q1', {}).get('probabilities') for r in v)}
def arr(v):
    return (np.array([[r['answers']['q1']['probabilities'][c] for c in CL] for r in v]), np.array([CL.index(r['labels']['q1']) for r in v]),
            np.array([int(r['answers']['q1']['choice'] == r['labels']['q1']) for r in v]))
def fit_t(P, y):  # temperature by NLL of the TRUE label on p^(1/T); T>1 flattens
    lp = np.log(np.clip(P, 1e-12, 1)); best = (1e9, 1.0)
    for T in np.geomspace(0.05, 100, 400):
        z = lp / T; z -= z.max(1, keepdims=True); q = np.exp(z); q /= q.sum(1, keepdims=True)
        n = -np.mean(np.log(np.clip(q[np.arange(len(y)), y], 1e-12, 1)))
        if n < best[0]: best = (n, T)
    return best[1]
def scale(P, T):
    z = np.log(np.clip(P, 1e-12, 1)) / T; z -= z.max(1, keepdims=True); q = np.exp(z); return q / q.sum(1, keepdims=True)
SPL = {'gold': {k: True for k in A},
       'self': {k: len({r['answers']['q1']['choice'] for r in v}) == 1 for k, v in A.items()},
       'corr': {k: len({int(r['answers']['q1']['choice'] == r['labels']['q1']) for r in v}) == 1 for k, v in A.items()},
       'graph': {k: g for k in sorted(A) if (g := gsplit(k)) is not None}}
out = [{'probe': 'corpus', 'n_rows_raw': len(raw), 'n_acts_raw': n_raw, 'n_acts_usable': len(A), 'n_rows_usable': 3 * len(A), 'resolvable_graph_acts': len(SPL['graph'])}]
for name, mem in SPL.items():
    out.append({'probe': 'split_shape', 'split': name, 'n_acts': len(mem), 'n_unanimous_acts': sum(mem.values()),
                'n_contested_acts': len(mem) - sum(mem.values()), 'contested_fraction': round(1 - sum(mem.values()) / len(mem), 4) if mem else None})
    for seed in SEEDS:
        acts = sorted(mem); perm = np.random.default_rng(seed).permutation(len(acts)); train = set(acts[i] for i in perm[:len(acts) // 2])
        for sub in (True, False):
            held = [k for k in acts if k not in train and mem[k] == sub]; trs = [k for k in train if mem[k] == sub]
            if not held: continue
            thin = len(held) < 5 or len(trs) < 5
            r = {'probe': 'seed', 'split': name, 'seed': seed, 'group': 'unanimous' if sub else 'contested',
                 'n_acts_train': len(trs), 'n_acts_held': len(held), 'n_rows_held': 3 * len(held), 'too_thin': thin}
            if not thin:  # per-group fit: temperature AND isotonic fit on that group's train rows
                P = np.vstack([arr(A[k])[0] for k in held]); y = np.concatenate([arr(A[k])[1] for k in held]); cor = np.concatenate([arr(A[k])[2] for k in held])
                Ptr = np.vstack([arr(A[k])[0] for k in trs]); ytr = np.concatenate([arr(A[k])[1] for k in trs]); ctr = np.concatenate([arr(A[k])[2] for k in trs])
                T = fit_t(Ptr, ytr); sc = scale(P, T).max(1); xa, fa = isotonic(scale(Ptr, T).max(1), ctr); ia = apply_map(xa, fa, sc)
                r.update({'T_fit': round(T, 4), 'ece_before': round(ece(P.max(1), cor), 4), 'ece_temp_after': round(ece(sc, cor), 4), 'ece_iso_after': round(ece(ia, cor), 4)})
            out.append(r)
[print(json.dumps(r)) for r in out]
if len(sys.argv) > 1: open(sys.argv[1], 'w').write(''.join(json.dumps(r) + '\n' for r in out))
