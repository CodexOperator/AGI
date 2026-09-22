#!/usr/bin/env python3
"""JEV surface-lexical arm -- hypothesis:lm-jev-surface-lexical-beats-jev.
Same scrubbed bodies/labels as the ECHO arm; TF-IDF 1-2gram + logreg asked q1,
5-fold stratified CV seed 20260918, plus a node-kind-token ablation for the
falsifier's second clause. No network.
"""
import datetime, json, os, re, sys
from collections import Counter
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import StratifiedKFold
from sklearn.pipeline import Pipeline
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import acts_replay as J, acts_replay_scrub as S  # noqa: E402
SEED = 20260918
KIND = re.compile(r"\b(experiment|verdict|hypothesis|idea|goal|mvp|outcome|build|doc)\b", re.I)
PIPE = lambda: Pipeline([("tf", TfidfVectorizer(ngram_range=(1, 2), sublinear_tf=True)),
                         ("lr", LogisticRegression(max_iter=2000, class_weight="balanced"))])

def rows():
    acts, labs = S.pinned_corpus(), {}
    for line in open(os.path.join(HERE, "acts_replay_scrub.jsonl"), encoding="utf-8"):
        r = json.loads(line)
        labs.setdefault(r["act"], r["labels"])
    out = [{"id": a["id"], "kind": a["kind"], "text": S.scrub(a["state"])[0],
            "label": labs.get(a["id"], a["labels"]).get("q1")} for a in acts]
    return [r for r in out if r["label"]]

def cv(texts, y):
    pred, accs = np.array([None] * len(y), dtype=object), []
    for tr, te in StratifiedKFold(5, shuffle=True, random_state=SEED).split(texts, y):
        p = PIPE().fit([texts[i] for i in tr], [y[i] for i in tr])
        pr = p.predict([texts[i] for i in te])
        for i, q in zip(te, pr):
            pred[i] = q
        accs.append(accuracy_score([y[i] for i in te], pr))
    return accs, pred

def main():
    recs = rows()
    g = {}
    for line in open(os.path.join(HERE, "acts_replay_scrub.jsonl"), encoding="utf-8"):
        r = json.loads(line); g.setdefault(r["act"], []).append(r)
    jp = {a: S.majority(rs, "q1") for a, rs in g.items()}
    y, texts = [r["label"] for r in recs], [r["text"] for r in recs]
    accs, pred = cv(texts, y)
    mean, jev = float(np.mean(accs)), sum(jp[r["id"]] == r["label"] for r in recs) / len(recs)
    amp = float(np.mean(cv([KIND.sub(" ", t) for t in texts], y)[0]))
    hist = Counter((r["kind"], r["label"]) for r in recs)
    prior = {k: max((l for k2, l in hist if k2 == k), key=lambda l: hist[(k, l)]) for k in {r["kind"] for r in recs}}
    kp = sum(prior[r["kind"]] == r["label"] for r in recs) / len(recs)
    ok = lambda i: pred[i] == y[i]
    jok = lambda i: jp[recs[i]["id"]] == y[i]
    mol = sum(ok(i) and not jok(i) for i in range(len(recs)))
    jol = sum(jok(i) and not ok(i) for i in range(len(recs)))
    both = sum(ok(i) and jok(i) for i in range(len(recs)))
    full = PIPE().fit(texts, y)
    vocab = list(full.named_steps["tf"].get_feature_names_out())
    coef, classes = full.named_steps["lr"].coef_, list(full.named_steps["lr"].classes_)
    d = {"key": "jev_surface_tfidf", "n": len(recs), "seed": SEED,
         "tfidf_mean": round(mean, 4), "folds": [round(a, 4) for a in accs],
         "tfidf_ablate_kind_mean": round(amp, 4),
         "jev_scrubbed_q1": round(jev, 4), "delta_vs_jev": round(mean - jev, 4),
         "kind_prior_baseline": round(kp, 4), "delta_vs_kind_prior": round(mean - kp, 4),
         "majority_baseline": round(max(Counter(y).values()) / len(y), 4),
         "win_loss": {"model_only_correct": mol, "jev_only_correct": jol, "both": both, "neither": len(recs) - mol - jol - both},
         "top_ngrams": {str(c): [vocab[i] for i in np.argsort(coef[ci])[::-1][:8]] for ci, c in enumerate(classes)}}
    print(json.dumps(d, indent=1))
    if "--dry" not in sys.argv:
        d["ts_utc"] = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        p = os.path.join(os.path.dirname(HERE), "bench", d["ts_utc"] + ".jsonl")
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False) + "\n")
        sys.stderr.write("wrote %s\n" % p)
if __name__ == "__main__":
    main()
