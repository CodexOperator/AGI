#!/usr/bin/env python3
"""KID C / chain 4 V2-C1: is the graph's own verdict corpus trainable?
sklearn only (1.8.0), numpy 2.4.3. No downloads, no installs, no embeddings
(sentence-transformers is NOT installed - verified by import failure).
"""
import glob, json, os, re, sys, warnings
from collections import Counter, defaultdict
warnings.filterwarnings("ignore")

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.model_selection import GroupKFold, cross_val_predict, KFold
from sklearn.metrics import accuracy_score, f1_score, mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ROOT = "/home/ubuntu/work/agi/.agi/worktrees/a00-48ed5e56/.agi/nodes"

def parse_frontmatter(path):
    """Minimal YAML-ish frontmatter parser: scalars, inline lists, block lists."""
    with open(path, encoding="utf-8", errors="replace") as f:
        txt = f.read()
    if not txt.startswith("---"):
        return {}, txt
    end = txt.find("\n---", 3)
    if end < 0:
        return {}, txt
    fm_raw = txt[3:end]
    body = txt[end+4:]
    fm = {}
    key = None
    for line in fm_raw.splitlines():
        if not line.strip():
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if m:
            key = m.group(1)
            val = m.group(2).strip()
            if val == "":
                fm[key] = []
            elif val.startswith("[") and val.endswith("]"):
                inner = val[1:-1].strip()
                fm[key] = [x.strip().strip('"\'') for x in inner.split(",")] if inner else []
            elif val.startswith('"') and val.endswith('"') and len(val) > 1:
                fm[key] = val[1:-1].replace('\\n', '\n').replace('\\"', '"')
            else:
                fm[key] = val
        elif line.startswith("  - ") or line.startswith("- "):
            item = line.split("- ", 1)[1].strip().strip('"\'')
            if isinstance(fm.get(key), list):
                fm[key].append(item)
    return fm, body

def collect(dirpath):
    out = {}
    for p in sorted(glob.glob(os.path.join(dirpath, "*.md"))):
        fm, body = parse_frontmatter(p)
        if fm.get("type") != "verdict":
            continue
        nid = fm.get("id")
        if not nid:
            continue
        fm["_file"] = os.path.relpath(p, ROOT)
        fm["_body"] = body
        out[nid] = fm
    return out

# ---- node universe (live-first, then deprecated) -------------------------
nodes = {}
for sub in ("", "deprecated/"):
    for p in sorted(glob.glob(os.path.join(ROOT, sub, "*", "*.md"))):
        fm, body = parse_frontmatter(p)
        nid = fm.get("id")
        if not nid or nid in nodes:
            continue
        fm["_body"] = body
        fm["_file"] = os.path.relpath(p, ROOT)
        fm["_type"] = fm.get("type")
        fm["_deprecated"] = bool(sub)
        nodes[nid] = fm
print(f"# node universe indexed: {len(nodes)}")

# ---- normalize legacy prefixes / short-name parents ----------------------
PREFIX_MAP = {"hyp:": "hypothesis:", "exp:": "experiment:"}
def resolve(ref):
    """Resolve a parent ref to a node id in the universe (handles legacy
    hyp:/exp: prefixes and bare short names from season-1 nodes)."""
    if not isinstance(ref, str):
        return None
    if ref in nodes:
        return ref
    for a, b in PREFIX_MAP.items():
        if ref.startswith(a):
            cand = b + ref[len(a):]
            if cand in nodes:
                return cand
    return None

for nid, v in nodes.items():
    ps = v.get("parents") or []
    if isinstance(ps, str):
        ps = [ps]
    v["_parents_resolved"] = [r for r in (resolve(p) for p in ps) if r]

verdicts = {k: v for k, v in nodes.items() if v["_type"] == "verdict"}
print(f"# verdict nodes parsed: {len(verdicts)} "
      f"(live={sum(1 for v in verdicts.values() if not v['_deprecated'])}, "
      f"deprecated={sum(1 for v in verdicts.values() if v['_deprecated'])})")

# ---- class collapse ------------------------------------------------------
def collapse(vstr):
    if not isinstance(vstr, str):
        return None, None
    v = vstr.strip()
    if v == "proved":
        return "proved", 1.0
    if v == "disproved":
        return "disproved", 0.0
    if v == "pending":
        return "pending", None
    m = re.match(r"^inconclusive_lean_(proved|disproved):(\d+)$", v)
    if m:
        direction, n = m.group(1), int(m.group(2))
        if direction == "disproved":
            return ("lean_disproved_le65" if n <= 65 else "lean_disproved_gt65"), n/100.0
        if n >= 75:
            return "lean_proved_ge75", n/100.0
        if n >= 66:
            return "lean_proved_66_74", n/100.0
        return "lean_proved_le65", n/100.0
    return None, None

records = []
skipped = []
for nid, v in verdicts.items():
    cls, conf_from_v = collapse(v.get("verdict"))
    if cls is None:
        skipped.append((nid, v.get("verdict")))
        continue
    conf = v.get("confidence")
    try:
        conf = float(conf)
    except (TypeError, ValueError):
        conf = None
    parents = v.get("_parents_resolved") or []
    # find experiments / hypothesis among parents, and transitively
    exps, hyps = [], []
    for p in parents:
        if p.startswith("experiment:") and p in nodes:
            exps.append(p)
        if p.startswith("hypothesis:") and p in nodes:
            hyps.append(p)
    # transitive: exp -> its hypothesis parent
    for e in list(exps):
        for pp in (nodes[e].get("parents") or []):
            if pp.startswith("hypothesis:") and pp in nodes and pp not in hyps:
                hyps.append(pp)
    if not hyps:
        # maybe verdict parent is directly the hypothesis via other shape
        for p in parents:
            if p in nodes and nodes[p].get("_type") == "hypothesis":
                hyps.append(p)
    hyp_body = "\n\n".join(nodes[h]["_body"] for h in hyps)
    exp_body = "\n\n".join(nodes[e]["_body"] for e in exps)
    records.append({
        "verdict_id": nid, "verdict_raw": v.get("verdict"), "cls": cls,
        "conf": conf, "conf_from_verdict": conf_from_v,
        "hyps": hyps, "exps": exps, "parents": parents,
        "text": (hyp_body + "\n\n" + exp_body).strip(),
        "has_hyp": bool(hyps), "has_exp": bool(exps),
    })

print(f"# usable records: {len(records)}  skipped(raw): {len(skipped)}")
for s in skipped:
    print(f"#   SKIP {s[0]} raw={s[1]!r}")

# ---- join coverage -------------------------------------------------------
n_hyp = sum(1 for r in records if r["has_hyp"])
n_exp = sum(1 for r in records if r["has_exp"])
n_txt = sum(1 for r in records if r["text"])
print(f"# joined to hypothesis body: {n_hyp}   joined to experiment body: {n_exp}   non-empty text: {n_txt}")
print(f"# distinct hypotheses: {len(set(h for r in records for h in r['hyps']))}")

# ---- class histogram -----------------------------------------------------
hist = Counter(r["cls"] for r in records)
print("\n## CLASS HISTOGRAM (collapsed)")
CLASS_ORDER = ["proved", "lean_proved_ge75", "lean_proved_66_74",
               "lean_proved_le65", "lean_disproved_gt65", "lean_disproved_le65",
               "disproved"]
for c in CLASS_ORDER:
    print(f"{c:24s} {hist.get(c,0):4d}")
print(f"{'TOTAL':24s} {sum(hist.values()):4d}")
print("\n## RAW VERDICT STRING HISTOGRAM")
for v, n in Counter(r["verdict_raw"] for r in records).most_common():
    print(f"{n:4d}  {v}")

# ---- goal grouping -------------------------------------------------------
def root_goal(nid, seen=None):
    seen = seen or set()
    if nid in seen:
        return None
    seen.add(nid)
    n = nodes.get(nid)
    if not n:
        return None
    if nid.startswith("goal:"):
        return nid
    ps = n.get("_parents_resolved")
    if ps is None:
        ps = [resolve(p) for p in (n.get("parents") or [])]
        ps = [p for p in ps if p]
        n["_parents_resolved"] = ps
    for p in ps:
        if p.startswith("goal:"):
            return p
    for p in ps:
        g = root_goal(p, seen)
        if g:
            return g
    return None

def goal_chain(r):
    for h in r["hyps"]:
        g = root_goal(h)
        if g:
            return g
    for e in r["exps"]:
        g = root_goal(e)
        if g:
            return g
    return "unknown"

for r in records:
    r["group"] = goal_chain(r)

gcount = Counter(r["group"] for r in records)
print(f"\n## GROUP (root goal) HISTOGRAM: {len(gcount)} distinct groups")
for g, n in gcount.most_common(12):
    print(f"{n:4d}  {g}")

# ---- modelling -----------------------------------------------------------
X_text = [r["text"] for r in records]
y = np.array([r["cls"] for r in records])
groups = np.array([r["group"] for r in records])
mask = np.array([bool(t.strip()) for t in X_text])
print(f"\n# modelling on {mask.sum()} records with non-empty text")
X_text_m = [t for t, m in zip(X_text, mask) if m]
y_m, groups_m = y[mask], groups[mask]

maj = Counter(y_m).most_common(1)[0]
maj_frac = maj[1] / len(y_m)
print(f"# majority class = {maj[0]}  baseline accuracy = {maj_frac:.4f}")

# map class -> int label
classes = sorted(set(y_m))
nc = len(classes)
print(f"# {nc} classes present: {classes}")

def run_model(name, clf, X_txt, yv, grps, grouped=True):
    pipe = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2,
                                               sublinear_tf=True, strip_accents="unicode")),
                     ("clf", clf)])
    n_splits = min(5, len(set(grps)))
    if grouped:
        cv = GroupKFold(n_splits=n_splits)
        splits = list(cv.split(X_txt, yv, groups=grps))
    else:
        from sklearn.model_selection import StratifiedKFold
        cnt = Counter(yv)
        n_splits = max(2, min(5, min(cnt.values()) if min(cnt.values()) >= 2 else 2))
        if min(cnt.values()) >= 5:
            splits = list(StratifiedKFold(n_splits=5, shuffle=True, random_state=0).split(X_txt, yv))
        else:
            splits = list(GroupKFold(n_splits=n_splits).split(X_txt, yv, groups=grps))
    yp = np.empty(len(yv), dtype=object)
    covered = np.zeros(len(yv), dtype=bool)
    for tr, te in splits:
        p = Pipeline(pipe.steps)
        p.fit([X_txt[i] for i in tr], [yv[i] for i in tr])
        preds = p.predict([X_txt[i] for i in te])
        for i, pr in zip(te, preds):
            yp[i] = pr
            covered[i] = True
    yp = yp[covered]
    yt = np.array([yv[i] for i in range(len(yv)) if covered[i]])
    acc = accuracy_score(yt, yp)
    f1m = f1_score(yt, yp, average="macro", labels=classes, zero_division=0)
    print(f"{name:38s} acc={acc:.4f}  macroF1={f1m:.4f}  (n={len(yt)}, folds={len(splits)})")
    return acc, f1m

print("\n## CLASSIFICATION: 5-fold CV grouped by root goal")
res = {}
res["tfidf+logreg grouped"] = run_model("tfidf(1-2gram)+logreg [GROUPED]", LogisticRegression(max_iter=2000, C=4.0, class_weight="balanced"), X_text_m, y_m, groups_m, True)
res["tfidf+logreg ungrouped"] = run_model("tfidf(1-2gram)+logreg [ungrouped]", LogisticRegression(max_iter=2000, C=4.0, class_weight="balanced"), X_text_m, y_m, groups_m, False)
res["tfidf+logreg C=20 grouped"] = run_model("tfidf+logreg C=20 [GROUPED]", LogisticRegression(max_iter=3000, C=20.0, class_weight="balanced"), X_text_m, y_m, groups_m, True)
res["tfidf+logreg C=0.5 grouped"] = run_model("tfidf+logreg C=0.5 [GROUPED]", LogisticRegression(max_iter=2000, C=0.5, class_weight="balanced"), X_text_m, y_m, groups_m, True)
res["tfidf+linearSVC grouped"] = run_model("tfidf+LinearSVC [GROUPED]", LinearSVC(C=1.0, class_weight="balanced"), X_text_m, y_m, groups_m, True)

print(f"\n## DELTA vs majority baseline ({maj_frac:.4f}), grouped CV")
for k, (a, f) in res.items():
    print(f"{k:38s} acc={a:.4f}  delta={100*(a-maj_frac):+.2f} pts   macroF1={f:.4f}")

# 4-class formulation as specified (exact) + binary
def recode(r):
    c = r["cls"]
    if c == "proved": return "proved"
    if c in ("lean_proved_ge75",): return "lean_proved_ge75"
    if c in ("lean_proved_66_74",): return "lean_66_74"
    return "weak_or_disproved"
y4 = np.array([recode(r) for r in records])[mask]
print(f"\n## 4-CLASS SPEC Histogram: {dict(Counter(y4))}")
maj4 = Counter(y4).most_common(1)[0]
print(f"# majority 4-class baseline = {maj4[1]/len(y4):.4f} ({maj4[0]})")
res["4class logreg grouped"] = run_model("4-class tfidf+logreg [GROUPED]", LogisticRegression(max_iter=2000, C=4.0, class_weight="balanced"), X_text_m, y4, groups_m, True)

# ---- fair per-fold majority baseline + stricter grouping ----------------
def grouped_cv_acc(clf, X_txt, yv, grps, grouped=True):
    pipe_steps = [("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True, strip_accents="unicode")),
                  ("clf", clf)]
    n_splits = min(5, len(set(grps)))
    cv = GroupKFold(n_splits=n_splits)
    splits = list(cv.split(X_txt, yv, groups=grps))
    corr_model = corr_base = tot = 0
    for tr, te in splits:
        p = Pipeline(pipe_steps)
        p.fit([X_txt[i] for i in tr], [yv[i] for i in tr])
        preds = p.predict([X_txt[i] for i in te])
        # per-fold majority baseline from TRAIN labels only
        base = Counter(yv[i] for i in tr).most_common(1)[0][0]
        for i, pr in zip(te, preds):
            tot += 1
            corr_model += (pr == yv[i])
            corr_base += (base == yv[i])
    return corr_model / tot, corr_base / tot, len(splits)

print("\n## FAIR grouped CV: per-fold (train-majority) baseline vs model")
for nm, clf in [("logreg C=4", LogisticRegression(max_iter=2000, C=4.0, class_weight="balanced")),
                ("logreg C=0.5", LogisticRegression(max_iter=2000, C=0.5, class_weight="balanced"))]:
    for gname, gv in [("goal", groups_m), ("hypothesis", np.array([r["hyps"][0] if r["hyps"] else "nohyp" for r in records])[mask])]:
        a, b, k = grouped_cv_acc(clf, X_text_m, y_m, gv, True)
        print(f"{nm:12s} group={gname:11s} n_groups={len(set(gv)):4d} folds={k} model={a:.4f} foldmaj={b:.4f} delta={100*(a-b):+.2f} pts")

print("\n## BINARY: proved vs not-proved")
yb = np.array(["proved" if r["cls"] == "proved" else "not_proved" for r in records])[mask]
majb = Counter(yb).most_common(1)[0]
print(f"# histogram {dict(Counter(yb))}  majority baseline={majb[1]/len(yb):.4f}")
for nm, clf in [("logreg C=4", LogisticRegression(max_iter=2000, C=4.0, class_weight="balanced")),
                ("logreg C=0.5", LogisticRegression(max_iter=2000, C=0.5, class_weight="balanced"))]:
    a, b, k = grouped_cv_acc(clf, X_text_m, yb, groups_m, True)
    print(f"binary {nm:12s} group=goal folds={k} model={a:.4f} foldmaj={b:.4f} delta={100*(a-b):+.2f} pts")

print("\n## BINARY: disproved/lean-disproved vs rest")
yd = np.array(["disproved-ish" if "disproved" in r["cls"] else "rest" for r in records])[mask]
print(f"# histogram {dict(Counter(yd))}  majority baseline={Counter(yd).most_common(1)[0][1]/len(yd):.4f}")
a, b, k = grouped_cv_acc(LogisticRegression(max_iter=2000, C=4.0, class_weight="balanced"), X_text_m, yd, groups_m, True)
print(f"disproved-detector grouped model={a:.4f} foldmaj={b:.4f} delta={100*(a-b):+.2f} pts")

# ---- permutation test: is any grouped signal real? ----------------------
rng = np.random.default_rng(12345)

def cv_acc_for(yv, X_txt, grps, clf, n_splits=5):
    cv = GroupKFold(n_splits=n_splits)
    corr = tot = 0
    for tr, te in cv.split(X_txt, yv, groups=grps):
        if len(set(yv[i] for i in tr)) < 2:
            base = Counter(yv[i] for i in tr).most_common(1)[0][0]
            for i in te:
                tot += 1; corr += (base == yv[i])
            continue
        p = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)),
                      ("clf", clf)])
        p.fit([X_txt[i] for i in tr], [yv[i] for i in tr])
        for i, pr in zip(te, p.predict([X_txt[i] for i in te])):
            tot += 1; corr += (pr == yv[i])
    return corr / tot

clf_factory = lambda: LogisticRegression(max_iter=2000, C=4.0, class_weight="balanced")
Y = y_m
G_goal = groups_m
G_hyp = np.array([r["hyps"][0] if r["hyps"] else "nohyp" for r in records])[mask]
n_modelled_with_hyp = int((G_hyp != "nohyp").sum())
print(f"\n## GROUP COMPOSITION of {len(Y)} modelled records")
print(f"# with hypothesis group: {n_modelled_with_hyp}   without (nohyp): {int((G_hyp=='nohyp').sum())}")
print(f"# goal groups: {len(set(G_goal))}  hypothesis groups: {len(set(G_hyp))}")
print(f"# largest goal group: {Counter(G_goal).most_common(3)}")

obs_goal = cv_acc_for(Y, X_text_m, G_goal, clf_factory())
obs_hyp = cv_acc_for(Y, X_text_m, G_hyp, clf_factory())
print(f"# observed grouped acc: goal={obs_goal:.4f}  hypothesis={obs_hyp:.4f}")

N_PERM = 100
null_goal, null_hyp = [], []
for t in range(N_PERM):
    perm = rng.permutation(len(Y))
    yp = Y[perm]
    null_goal.append(cv_acc_for(yp, X_text_m, G_goal, clf_factory()))
    null_hyp.append(cv_acc_for(yp, X_text_m, G_hyp, clf_factory()))
null_goal = np.array(null_goal); null_hyp = np.array(null_hyp)
for nm, obs, null in [("goal", obs_goal, null_goal), ("hypothesis", obs_hyp, null_hyp)]:
    p = (1 + (null >= obs).sum()) / (1 + len(null))
    print(f"# permutation[{nm}]: null mean={null.mean():.4f} std={null.std():.4f} "
          f"p(acc>=obs)={p:.3f}  (obs={obs:.4f}, delta_obs_null_mean={100*(obs-null.mean()):+.2f} pts)")

# ---- confidence regression ----------------------------------------------
conf_recs = [r for r in records if r["conf"] is not None and r["text"].strip()]
Xc = [r["text"] for r in conf_recs]
yc = np.array([r["conf"] for r in conf_recs])
gc = np.array([r["group"] for r in conf_recs])
print(f"\n## CONFIDENCE REGRESSION: n={len(yc)}  mean={yc.mean():.4f} std={yc.std():.4f}")
mean_mae = mean_absolute_error(yc, np.full_like(yc, yc.mean()))
print(f"predict-the-mean baseline MAE = {mean_mae:.4f}")

from sklearn.linear_model import Ridge
n_splits = min(5, len(set(gc)))
cv = GroupKFold(n_splits=n_splits)
yp = np.full(len(yc), np.nan)
for tr, te in cv.split(Xc, yc, groups=gc):
    p = Pipeline([("tfidf", TfidfVectorizer(ngram_range=(1, 2), min_df=2, sublinear_tf=True)),
                  ("sc", StandardScaler(with_mean=False)),
                  ("clf", Ridge(alpha=1.0))])
    p.fit([Xc[i] for i in tr], yc[tr])
    yp[te] = p.predict([Xc[i] for i in te])
mae = mean_absolute_error(yc, yp)
print(f"tfidf+Ridge [GROUPED, {n_splits}-fold] MAE = {mae:.4f}")
print(f"delta vs mean-predictor = {mean_mae-mae:+.4f} (negative = worse)")

# raw verdict-string confidence (e.g. lean:58 -> 0.58) vs frontmatter confidence
pairs = [(r["conf"], r["conf_from_verdict"]) for r in records if r["conf"] is not None and r["conf_from_verdict"] is not None]
if pairs:
    a = np.array([p[0] for p in pairs]); b = np.array([p[1] for p in pairs])
    agree = np.mean(np.abs(a-b) < 0.005)
    print(f"\n# frontmatter confidence vs verdict-string N: n={len(pairs)} "
          f"agree(<0.005)={agree:.3f} mean|diff|={np.mean(np.abs(a-b)):.4f}")

print("\n## JSON SUMMARY")
print(json.dumps({
    "verdict_nodes_parsed": len(verdicts),
    "usable_records": len(records),
    "class_hist": dict(hist),
    "majority_baseline": maj_frac,
    "majority_class": maj[0],
    "grouped_acc": {k: v[0] for k, v in res.items()},
    "grouped_macroF1": {k: v[1] for k, v in res.items()},
    "conf_reg_n": len(yc),
    "conf_mean_mae": mean_mae,
    "conf_ridge_mae": mae,
    "best_grouped_delta_pts": max(100*(v[0]-maj_frac) for v in res.values()),
}, indent=1))
