"""TM.SFL.01 -- is the verdict held-out ECE target (0.10, def B) UNDER the estimator's
finite-sample floor? Null: replace each held-out row's correctness label by Bernoulli(fitted-T
max-prob), 200 draws. TM.74 protocol, scrub corpus. DEV: NumPy is NOT installed on this box, so
pure Python (same math, 0 API, seconds). Run: python3 jev_ece_floor.py [out.jsonl]
"""
import json, math, random, sys
D = __file__.rsplit('/', 1)[0]; SEEDS = [20260918, 1, 7, 42, 1234]; NDRAW = 200; B = 10
TGRID = [0.05 * (2000.0 ** (i / 399)) for i in range(400)]  # geomspace(0.05, 100)

def ece(c, y, b=B):
    n = len(c); e = 0.0
    for i in range(b):
        lo, hi = i / b, (i + 1) / b
        m = [j for j in range(n) if lo <= c[j] and (c[j] < hi if i < b - 1 else c[j] <= hi)]
        if m: e += len(m) / n * abs(sum(c[j] for j in m) / len(m) - sum(y[j] for j in m) / len(m))
    return e

def scale(p, T):
    z = [math.log(max(v, 1e-12)) / T for v in p]; mx = max(z); q = [math.exp(v - mx) for v in z]; s = sum(q)
    return [v / s for v in q]

def fit_t(P, Y):
    return min(((sum(-math.log(max(scale(p, T)[y], 1e-12)) for p, y in zip(P, Y)) / len(P), T) for T in TGRID))[1]

def stats(d):
    s = sorted(d); return round(s[NDRAW // 2], 4), round(s[int(0.05 * NDRAW)], 4), round(s[int(0.95 * NDRAW) - 1], 4)

rows = [json.loads(l) for l in open(D + '/acts_replay_scrub.jsonl')]
CL = sorted({k for r in rows for k in r['answers'].get('q1', {}).get('probabilities', {})})
out = []
for g in ('experiment', 'verdict'):
    u = [r for r in rows if r['kind'] == g and r['answers'].get('q1', {}).get('probabilities') and r['labels'].get('q1')]
    by = {}
    for r in u: by.setdefault(r['act'], []).append(r)
    acts = sorted(by)
    for seed in SEEDS:
        sh = acts[:]; random.Random(seed).shuffle(sh); tr = set(sh[:len(sh) // 2])
        P = [[r['answers']['q1']['probabilities'][k] for k in CL] for r in u if r['act'] in tr]
        Y = [CL.index(r['labels']['q1']) for r in u if r['act'] in tr]
        T = fit_t(P, Y)
        held = [r for r in u if r['act'] not in tr]
        c = [max(scale([r['answers']['q1']['probabilities'][k] for k in CL], T)) for r in held]
        y = [int(r['answers']['q1']['choice'] == r['labels']['q1']) for r in held]
        rng = random.Random(str(seed) + g)
        sr = [ece(c, [int(rng.random() < v) for v in c]) for _ in range(NDRAW)]
        ac = {}
        for r, v in zip(held, c): ac.setdefault(r['act'], []).append(v)
        ca = [sum(v) / len(v) for v in ac.values()]
        sa = [ece(ca, [int(rng.random() < v) for v in ca]) for _ in range(NDRAW)]
        mr, p5r, p95r = stats(sr); ma, p5a, p95a = stats(sa)
        out.append({'probe': 'seed', 'group': g, 'seed': seed, 'T_fit': round(T, 4),
                    'n_acts_held': len(ac), 'n_rows_held': len(held), 'real_ece': round(ece(c, y), 4),
                    'row_median': mr, 'row_p5': p5r, 'row_p95': p95r, 'row_ge_010': mr >= 0.10,
                    'act_median': ma, 'act_p5': p5a, 'act_p95': p95a, 'act_ge_010': ma >= 0.10})
        print(json.dumps(out[-1]))
for g in ('experiment', 'verdict'):
    r = [o for o in out if o['group'] == g]
    out.append({'probe': 'summary', 'group': g, 'n_seeds': len(r),
                'seeds_row_ge_010': sum(o['row_ge_010'] for o in r), 'seeds_act_ge_010': sum(o['act_ge_010'] for o in r),
                'real_ece_mean': round(sum(o['real_ece'] for o in r) / len(r), 4)})
    print(json.dumps(out[-1]))
if len(sys.argv) > 1: open(sys.argv[1], 'w').write(''.join(json.dumps(o) + '\n' for o in out))