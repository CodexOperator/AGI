"""TM.50 -- does the ARM2 verdict-class ranking derive the human review call? Offline, no network.
5-fold held-out, ONE threshold fitted per train fold. Controls: majority 0.776, ARM1 direct 0.541/0.581."""
import json, numpy as np
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score, confusion_matrix
D = __file__.rsplit('/', 1)[0]; ACC = ["proved", "disproved"]; DEM = ["inconclusive_lean_proved", "inconclusive_lean_disproved", "pending"]
def load():
 rows = [json.loads(l) for l in open(D + '/single_axis_rows.jsonl')]; by = {}; lab = {}; drop = 0
 for r in rows:
  if r["arm"] != "arm2_verdict": continue
  p = r["answers"]["q1"].get("probabilities")
  if not p or not set(ACC + DEM) <= set(p): drop += 1; continue
  by.setdefault(r["act"], []).append(p); lab[r["act"]] = 1 if r["labels"]["q2"] == "accept" else 0
 acts = sorted(by); X = np.array([np.mean([sum(p[k] for k in ACC) for p in by[a]]) for a in acts]); return acts, X, np.array([lab[a] for a in acts]), drop
def fit_t(s, y, f=None):
 if f is not None: s = s[f]; y = y[f]
 c = np.unique(s); return float(max(c, key=lambda t: ((s >= t).astype(int) == y).mean()))
def ece(s, y, b=10):
 e = 0.0
 for i in range(b):
  lo, hi = i / b, (i + 1) / b; m = (s >= lo) & ((s < hi) if i < b - 1 else (s <= hi))
  if m.sum(): e += m.mean() * abs(s[m].mean() - y[m].mean())
 return e
def emit(r):
 with open(D + '/class_ranking_review_rows.jsonl', 'a') as f: f.write(json.dumps(r) + "\n"); f.flush()
def run(X, y, seed=20260918, tag="main"):
 pred = np.zeros(len(y), int); ts = [];
 for k, (tr, te) in enumerate(StratifiedKFold(5, shuffle=True, random_state=seed).split(X, y)):
  t = fit_t(X, y, tr); ts.append(t); pred[te] = (X[te] >= t).astype(int)
  emit({"tag": tag, "fold": k, "threshold": t, "agreement": float((pred[te] == y[te]).mean()), "auc": float(roc_auc_score(y[te], X[te]))})
 pool = {"tag": tag, "fold": "pooled", "n": int(len(y)), "agreement": float((pred == y).mean()), "auc": float(roc_auc_score(y, X)),
         "ece": float(ece(X, y)), "confusion": confusion_matrix(y, pred, labels=[1, 0]).tolist(),
         "threshold_mean": float(np.mean(ts)), "threshold_std": float(np.std(ts)), "thresholds": [float(t) for t in ts]}
 emit(pool); return pool
if __name__ == "__main__":
 open(D + '/class_ranking_review_rows.jsonl', 'w').close(); acts, X, y, drop = load(); main = run(X, y)
 gate = run(X, y[np.random.default_rng(20260918).permutation(len(y))], seed=7, tag="shuffled_labels")
 main["n_acts"] = len(acts); main["dropped_rows"] = drop;
 print(json.dumps({"n": len(acts), "dropped_rows": drop, "main": main, "gate": {k: gate[k] for k in ("agreement", "auc", "threshold_std")}}, indent=1))
