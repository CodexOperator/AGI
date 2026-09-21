"""TM.73 -- is the verdict q1 residual SHAPE not scale? Per-group isotonic regression on the
committed scrub rows, pure NumPy, CPU, 0 API calls. Mirrors experiment:a00-bdec620b-6c4cf7
(50/50 by act id within subgroup, seeds 20260918/1/7/42/1234). Kept under typesafe/ not
sessions/ (.gitignore:100) so it stays reproducible. Run: python3 jev_isotonic_residual.py
"""
import json, sys, numpy as np
D = __file__.rsplit('/', 1)[0]; SEEDS = [20260918, 1, 7, 42, 1234]


def ece(s, y, b=10):  # 10 equal-width bins, as class_ranking_review_call.py:18
    e = 0.0
    for i in range(b):
        lo, hi = i / b, (i + 1) / b
        m = (s >= lo) & ((s < hi) if i < b - 1 else (s <= hi))
        if m.sum(): e += m.mean() * abs(s[m].mean() - y[m].mean())
    return float(e)
def isotonic(x, y):  # PAVA -> (sorted_x, fitted step values)
    o = np.argsort(x, kind='stable'); xs, ys = x[o], y[o]; vals, wts = [], []
    for yi in ys:
        v, w = float(yi), 1
        while vals and vals[-1] >= v:
            pv, pw = vals.pop(), wts.pop(); v, w = (pv * pw + v * w) / (pw + w), pw + w
        vals.append(v); wts.append(w)
    return xs, np.repeat(vals, [int(w) for w in wts]).astype(float)
def apply_map(xs, fit, x):  # monotone step lookup, clipped to [0,1]
    i = np.clip(np.searchsorted(xs, x, side='right') - 1, 0, len(fit) - 1)
    return np.clip(fit[i], 0.0, 1.0)
def load():
    rows = [json.loads(l) for l in open(D + '/acts_replay_scrub.jsonl')]; G = {}
    for g in ('experiment', 'verdict'):
        rs = [r for r in rows if r['kind'] == g]
        u = [r for r in rs if r['answers'].get('q1', {}).get('probabilities') and r['labels'].get('q1')]
        G[g] = {'acts': sorted({r['act'] for r in rs}), 'rows': u, 'prob': [r['answers']['q1']['probabilities'] for r in u],
                'confB': np.array([max(r['answers']['q1']['probabilities'].values()) for r in u]),
                'confA': np.array([r['answers']['q1']['confidence'] for r in u]),
                'correct': np.array([int(r['answers']['q1']['choice'] == r['labels']['q1']) for r in u])}
    return G
def main():
    G = load(); out = []
    for g in ('experiment', 'verdict'):
        d = G[g]
        out.append({'probe': 'full_corpus_before', 'group': g, 'n_rows': len(d['rows']),
                    'ece_A': round(ece(d['confA'], d['correct']), 4), 'ece_B': round(ece(d['confB'], d['correct']), 4)})
    for seed in SEEDS:
        acc = {}
        for g in ('experiment', 'verdict'):
            d = G[g]; n = len(d['acts']); perm = np.random.default_rng(seed).permutation(n)
            tr = np.array([r['act'] in set(d['acts'][i] for i in perm[:n // 2]) for r in d['rows']]); te = ~tr
            ytr, yte = d['correct'][tr].astype(float), d['correct'][te]
            xs, fit = isotonic(d['confB'][tr], ytr); xa, fa = isotonic(d['confA'][tr], ytr)
            aB, aA = apply_map(xs, fit, d['confB'][te]), apply_map(xa, fa, d['confA'][te])
            moved = sum(max({k: float(apply_map(xs, fit, np.array([v]))[0]) for k, v in d['prob'][i].items()},
                            key=lambda k, p=d['prob'][i]: float(apply_map(xs, fit, np.array([p[k]]))[0]))
                        != max(d['prob'][i], key=d['prob'][i].get) for i in np.where(te)[0])
            out.append({'probe': 'seed', 'seed': seed, 'group': g, 'n_rows_held': int(te.sum()),
                        'ece_A_before': round(ece(d['confA'][te], yte), 4), 'ece_B_before': round(ece(d['confB'][te], yte), 4),
                        'ece_B_after': round(ece(aB, yte), 4), 'ece_A_after_scalar_input': round(ece(aA, yte), 4),
                        'argmax_delta_maxonly': 0.0, 'argmax_moved_elementwise': int(moved),
                        'argmax_delta_elementwise': round(moved / int(te.sum()), 4)})
            acc[g] = (int(te.sum()), ece(d['confB'][te], yte), ece(aB, yte), ece(d['confA'][te], yte), ece(aA, yte))
        nt = sum(v[0] for v in acc.values())
        out.append({'probe': 'pooled_heldout', 'seed': seed, 'n_rows_held': nt,
                    'ece_B_before': round(sum(v[1] * v[0] for v in acc.values()) / nt, 4),
                    'ece_B_after': round(sum(v[2] * v[0] for v in acc.values()) / nt, 4),
                    'ece_A_before': round(sum(v[3] * v[0] for v in acc.values()) / nt, 4),
                    'ece_A_after_scalar_input': round(sum(v[4] * v[0] for v in acc.values()) / nt, 4)})
    [print(json.dumps(r)) for r in out]
    if len(sys.argv) > 1:
        open(sys.argv[1], 'w').write(''.join(json.dumps(r) + '\n' for r in out))
    return out
if __name__ == '__main__':
    main()
