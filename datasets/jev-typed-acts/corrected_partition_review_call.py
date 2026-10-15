"""TM.51 -- does the CORRECTED partition derive the human review call? Offline; no network, no jev calls.
Pre-registered: hypothesis:lm-jev-corrected-partition-derives-the-review-call (5-fold held-out, threshold fitted on train)."""
import json, numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, confusion_matrix
D = __file__.rsplit('/', 1)[0]
CL = ['proved', 'disproved', 'inconclusive_lean_proved', 'inconclusive_lean_disproved', 'pending']
PARTS = {'A_prereg': ['proved', 'inconclusive_lean_proved'],
         'B_corrected': ['proved', 'disproved', 'inconclusive_lean_proved'],
         'TM50_control': ['proved', 'disproved']}
def emit(r):
    with open(D + '/corrected_partition_rows.jsonl', 'a') as f: f.write(json.dumps(r) + '\n'); f.flush()
def load():
    by, lab = {}, {}
    for r in (json.loads(l) for l in open(D + '/single_axis_rows.jsonl')):
        if r['arm'] != 'arm2_verdict': continue
        p = r['answers']['q1'].get('probabilities')
        if not p or not set(CL) <= set(p): continue
        by.setdefault(r['act'], []).append(p)
        lab[r['act']] = (1 if r['labels']['q2'] == 'accept' else 0, r['kind'])
    acts = sorted(by)
    return acts, by, np.array([lab[a][0] for a in acts]), np.array([lab[a][1] == 'verdict' for a in acts])
def ece(s, y, b=10):
    e = 0.0
    for i in range(b):
        lo, hi = i / b, (i + 1) / b; m = (s >= lo) & ((s < hi) if i < b - 1 else (s <= hi))
        if m.sum(): e += m.mean() * abs(s[m].mean() - y[m].mean())
    return float(e)
def fit_t(s, y, f):
    c = np.unique(s[f]); return float(max(c, key=lambda t: ((s[f] >= t).astype(int) == y[f]).mean()))
def cv(s, y, feat=None, seed=20260918, fitthr=False):
    pred = np.zeros(len(y), int); p = np.zeros(len(y)); folds = []; ts = []
    for tr, te in StratifiedKFold(5, shuffle=True, random_state=seed).split(s[:, None] if feat is None else feat, y):
        p[te] = s[te] if feat is None else LogisticRegression(max_iter=1000).fit(feat[tr], y[tr]).predict_proba(feat[te])[:, 1]
        t = fit_t(p, y, tr) if (feat is None or fitthr) else 0.5
        ts.append(t); pred[te] = (p[te] >= t).astype(int); folds.append(roc_auc_score(y[te], p[te]))
    return dict(n=int(len(y)), n_pos=int(y.sum()), n_neg=int((1 - y).sum()), auc=round(float(roc_auc_score(y, p)), 4),
                agree=round(float((pred == y).mean()), 4), auc_folds=[round(x, 4) for x in folds],
                auc_std=round(float(np.std(folds)), 4), thr_std=round(float(np.std(ts)), 3), ece=round(ece(p, y), 4),
                conf=confusion_matrix(y, pred, labels=[1, 0]).tolist())
def pops(tag, s, y, kv, feat=None, **kw):
    for pop, m in [('all', np.ones(len(y), bool)), ('verdict', kv), ('experiment', ~kv)]:
        emit(dict(tag=tag, pop=pop, **cv(s[m], y[m], None if feat is None else feat[m], **kw)))
if __name__ == '__main__':
    open(D + '/corrected_partition_rows.jsonl', 'w').close()
    acts, by, y, kv = load()
    Z = np.zeros(len(y)); X = np.array([np.mean([[p[k] for k in CL] for p in by[a]], axis=0) for a in acts])
    for name, keys in PARTS.items():
        s = np.array([np.mean([sum(p[k] for k in keys) for p in by[a]]) for a in acts])
        pops(name + '_mapping', s, y, kv)
    pops('LR_0.5', Z, y, kv, X); pops('LR_fit', Z, y, kv, X, fitthr=True)
    for name in ('A_prereg', 'B_corrected'):
        s = np.array([np.mean([sum(p[k] for k in PARTS[name]) for p in by[a]]) for a in acts])
        for seed in range(20):
            emit(dict(tag=name + '_shuffled', seed=seed, auc=round(float(roc_auc_score(y[np.random.default_rng(4000 + seed).permutation(len(y))], s)), 4)))
    for seed in range(20):
        emit(dict(tag='LR_shuffled', seed=seed, auc=cv(Z, y[np.random.default_rng(9000 + seed).permutation(len(y))], X, seed=7)['auc']))
    print(json.dumps({'acts': len(acts), 'rows': sum(1 for _ in open(D + '/corrected_partition_rows.jsonl'))}))
