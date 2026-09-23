#!/usr/bin/env python3
"""T1-T4: is chi_c=0.96025 a knee on dead-precision/safe-recall, or a label on a smooth ranking? Stdlib only."""
import csv, hashlib, json, math, os, random, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import paths
CHI_C, D, SEED = 0.96025, 896, 20260923
BREAKS = [round(0.4 + 0.1 * i, 2) for i in range(33)]
def lstsq(A, y):
    n = len(A[0]); M = [[sum(A[r][i] * A[r][j] for r in range(len(A))) for j in range(n)] + [sum(A[r][i] * y[r] for r in range(len(A)))] for i in range(n)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(M[r][c])); M[c], M[p] = M[p], M[c]
        for r in range(n):
            if r != c and M[r][c]:
                f = M[r][c] / M[c][c]; M[r] = [M[r][k] - f * M[c][k] if k >= c else M[r][k] for k in range(n + 1)]
    return [M[i][n] / M[i][i] for i in range(n)]
def bic(xs, ys, brk=None):
    A = [[1., x, x * x, x ** 3] + ([1., x - brk] if brk is not None and x > brk else ([0., 0.] if brk is not None else [])) for x in xs]
    b = lstsq(A, ys); rss = sum((sum(a * c for a, c in zip(rw, b)) - y) ** 2 for rw, y in zip(A, ys))
    return len(xs) * math.log(rss / len(xs)) + len(b) * math.log(len(xs))
def curv(xs, ys):
    sm = [sum(ys[i:i + 5]) / 5 for i in range(len(ys) - 4)]; d2 = [abs(sm[i + 2] - 2 * sm[i + 1] + sm[i]) for i in range(len(sm) - 2)]
    m = max(d2); return xs[d2.index(m) + 2], m
def sp(a, b):
    def rk(v):
        o = sorted(range(len(v)), key=v.__getitem__); r = [0.] * len(v); i = 0
        while i < len(o):
            j = i
            while j + 1 < len(o) and v[o[j + 1]] == v[o[i]]: j += 1
            for k in range(i, j + 1): r[o[k]] = (i + j) / 2 + 1
            i = j + 1
        return r
    ra, rb, n = rk(a), rk(b), len(a); ma, mb = sum(ra) / n, sum(rb) / n
    return sum((x - ma) * (y - mb) for x, y in zip(ra, rb)) / math.sqrt(sum((x - ma) ** 2 for x in ra) * sum((y - mb) ** 2 for y in rb))
def main(out):
    art = os.path.basename(paths.get_local("dead_head_artifact"))
    raw = open(os.path.join(paths.get_local("dead_head_run_dir"), art), "rb").read().decode()
    doc = json.loads(raw); ct = doc["clr_theory"]; dec = ct["decisions"]; hr = doc["head_results"]
    tol = ct["ground_truth_loss_threshold"]; z = [math.sqrt(D) * d["mean_cosine"] for d in dec]; dl = [r["delta_loss"] for r in hr]
    pool = [i for i, d in enumerate(dec) if not d["protected"]]; dead = [i for i, d in enumerate(dec) if d["dead"]]; safe = [i for i in pool if dl[i] <= tol]
    prec = sum(1 for i in dead if dl[i] <= tol) / len(dead)
    t1 = {"dead": len(dead), "protected": len(dec) - len(pool), "alive": ct["alive_count"], "dead_safe": sum(1 for i in dead if dl[i] <= tol), "dead_unsafe": sum(1 for i in dead if dl[i] > tol), "pool": len(pool), "pool_safe": len(safe), "precision": prec, "z_field": "clr_theory.decisions[].mean_cosine * sqrt(896)", "delta_loss_field": "head_results[].delta_loss", "tolerance_field": "clr_theory.ground_truth_loss_threshold"}
    t1["matches_summary_block"] = (t1["dead"] == ct["dead_count"] and t1["protected"] == ct["protected_count"] and t1["alive"] == ct["alive_count"] and t1["dead_safe"] == ct["true_positive_dead_safe"] and t1["dead_unsafe"] == ct["false_positive_dead_unsafe"] and abs(prec - ct["dead_precision"]) < 1e-12)
    sweep = []
    for k in range(191):
        chi = round(0.2 + 0.02 * k, 2); dd = [i for i in pool if z[i] < chi]; g = sum(1 for i in dd if dl[i] <= tol)
        sweep.append([chi, len(dd), g / len(dd), g / len(safe), sum(dl[i] for i in dd)])
    xs = [s[0] for s in sweep]; ys = {"precision": [s[2] for s in sweep], "safe_recall": [s[3] for s in sweep]}; fits = {}
    for n, v in ys.items():
        s0 = bic(xs, v); s1 = bic(xs, v, CHI_C); c, m = curv(xs, v); db = {b: s0 - bic(xs, v, b) for b in BREAKS + [CHI_C]}
        fits[n] = {"bic_smooth": s0, "bic_break": s1, "delta_bic": s0 - s1, "curvature_chi": c, "curvature_mag": m, "knee": s0 - s1 >= 10 and abs(c - CHI_C) <= 0.10, "placebo_delta_bic": db, "placebo_rank_of_0.96025_among_33": sorted(db, key=db.get, reverse=True).index(CHI_C) + 1, "placebo_breaks": BREAKS}
    win = [s for s in sweep if 0.9 <= s[0] <= 1.02]
    window = {"precision_change": win[-1][2] - win[0][2], "safe_recall_change": win[-1][3] - win[0][3], "max_step_precision": max(abs(win[i + 1][2] - win[i][2]) for i in range(len(win) - 1)), "max_step_safe_recall": max(abs(win[i + 1][3] - win[i][3]) for i in range(len(win) - 1))}
    sd = [i for i in pool if z[i] < CHI_C]
    rng = random.Random(SEED); nd = len(dead); draws = [rng.sample(pool, nd) for _ in range(10000)]
    mp = sum(sum(1 for i in d if dl[i] <= tol) / nd for d in draws) / 10000; md = sum(sum(dl[i] for i in d) for d in draws) / 10000
    t4 = {"spearman_pool_291": sp([z[i] for i in pool], [dl[i] for i in pool]), "spearman_all336": sp(z, dl), "artifact_precision": prec, "random_mean_precision": mp, "lift": prec / mp, "damage_lift": md / sum(dl[i] for i in dead), "seed": SEED, "draws": 10000}
    knee = any(f["knee"] for f in fits.values())
    if knee: verdict, nxt = "disproved", "K_c breakpoint stands; oscillator threshold and chain 2 retain standing"
    elif t4["lift"] <= 1.05 and abs(t4["spearman_pool_291"]) < 0.3: verdict, nxt = "proved", "coherence falsified as a pruning criterion; prune by measured delta-loss per GQA group"
    else: verdict, nxt = "proved", "chunk 2: z_h in one CPU pass on the served 9B + its GQA-group yield"
    prov = {"repo": "github.com/project-89/coherence-guided-dead-head-identification", "commit_short": "583962f", "commit_full_sha": "583962f87209bb92468c822575a62911aabada00", "url": "https://raw.githubusercontent.com/project-89/coherence-guided-dead-head-identification/583962f87209bb92468c822575a62911aabada00/data/" + art, "bytes": len(raw), "sha256": hashlib.sha256(raw.encode()).hexdigest(), "license": "PolyForm-NC 1.0.0", "fetched_via": "curl -sL -A Mozilla/5.0", "note": "third-party noncommercial bytes, kept uncommitted via .gitignore"}
    os.makedirs(out, exist_ok=True)
    open(out + "/sweep.csv", "w").write("chi,n_dead,precision,safe_recall,sum_delta_loss\n" + "\n".join(",".join(map(str, r)) for r in sweep) + "\n")
    json.dump({"chi_c": CHI_C, "curves": fits, "window_0.90_1.02": window, "at_chi_0.96": sweep[38], "at_chi_0.96025_simple_rule": [len(sd), sum(1 for i in sd if dl[i] <= tol) / len(sd)], "artifact_bridge_timer_rule": [ct["dead_count"], ct["dead_precision"]]}, open(out + "/fits.json", "w"), indent=1)
    json.dump({"T1_recount": t1, "T4_ranking": t4, "verdict": verdict, "next_step": nxt}, open(out + "/stats.json", "w"), indent=1)
    json.dump(prov, open(out + "/provenance.json", "w"), indent=1)
    print(json.dumps({"T1_matches": t1["matches_summary_block"], "at_0.96": sweep[38], "delta_bic": {n: fits[n]["delta_bic"] for n in fits}, "knee": {n: fits[n]["knee"] for n in fits}, "curvature_chi": {n: fits[n]["curvature_chi"] for n in fits}, "placebo_rank": {n: fits[n]["placebo_rank_of_0.96025_among_33"] for n in fits}, "window": window, "T4": t4, "verdict": verdict, "next_step": nxt}, indent=1))
if __name__ == "__main__": main(sys.argv[1] if len(sys.argv) > 1 else paths.get_local("dead_head_run_dir"))
