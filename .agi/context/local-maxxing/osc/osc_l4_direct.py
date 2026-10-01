#!/usr/bin/env python3
# L4 run 4 (hypothesis:lm-l4-direct-head-cost-ranking-holds-on-fresh-docs): run 3's per-head DIRECT windowing-cost
# ranking and run 1's sink-counting ranking, both FROZEN from run 3's results.json (no re-ranking), windowed (sinks +
# last W) on 8 FRESH wiki.valid docs vs run 1's random arms (same heads); band (run 1) and distance (run 2) reported;
# ADDITIVITY = joint KL of the k DIRECT heads / sum of their solo KLs. Loader / mask / kept_fraction / scoring / hidden
# / load_params IMPORTED from osc_l4_window.py, osc_l4_mass.py (and through it osc_l4_distance.py), all unchanged.
# Grid: <cell osc_band_l4_direct_dir>/params.json; outputs beside it. Fresh ids (tokenizer only): this.py --pick.
# Run detached: PYTHONPATH=<osc_test_pythonpath> <ml_python> this.
import hashlib, json, os, re, subprocess, sys, time
import torch

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import osc_l4_window as W  # noqa: E402  (puts the local-maxxing dir on sys.path)
import osc_l4_mass as X  # noqa: E402
import paths  # noqa: E402

FROZEN = ("direct", "sinkcount")


def pick(lens, excl, n, L):
    # deterministic: the first n article indices, in file order, with >= L tokens and not excluded
    return [i for i, m in enumerate(lens) if m >= L and i not in excl][:n]


def exclusions(P):   # run 1's eval docs, run 2's calibration docs, run 2's exclude list (doc 13)
    return {d for d, _ in P["eval_docs"] + P["calib_docs"]} | set(P["exclude_docs"])


def fresh(tok, P):
    text = open(os.path.join(os.path.dirname(paths.get(P["text_cell"])), P["text_file"]), encoding="utf-8").read()
    parts = re.split(r"(?m)^ = ([^=].*?) = \n", text)   # run 1's article split (W.load_docs re-asserts every title)
    arts = list(zip(parts[1::2], parts[2::2]))
    lens = [len(tok(body, add_special_tokens=False)["input_ids"]) for _, body in arts]
    return [[i, arts[i][0]] for i in pick(lens, exclusions(P), P["n_fresh"], P["L"])]


def additivity(joint, solo):   # joint KL of the k windowed heads / sum of their solo KLs; one head -> 1
    return joint / sum(solo)


def frozen_ok(P, R3):   # byte-equality of the frozen lists with run 3's results.json
    return all(json.dumps(P[f"frozen_{a}_ranking"]) == json.dumps(R3[f"{a}_ranking"]) for a in FROZEN)


key = lambda heads: ",".join(map(str, heads))  # noqa: E731


def main():
    P, t0 = X.load_params(out := paths.get_local("osc_band_l4_direct_dir")), time.time()
    from transformers import AutoModelForCausalLM, AutoTokenizer
    tok = AutoTokenizer.from_pretrained(paths.get(P["model_cell"]))
    if "--pick" in sys.argv:
        return print(json.dumps(fresh(tok, P)))
    psha = hashlib.sha256(open(os.path.join(out, "params.json"), "rb").read()).hexdigest()
    R1, R2, R3 = (json.load(open(os.path.join(paths.get_local(P[c]), "results.json"))) for c in (
        "run1_cell", "run2_cell", "run3_cell"))
    git = lambda *a: subprocess.run(["git", "-C", HERE, *a, "--", __file__], capture_output=True, text=True)  # noqa
    commit, dirty = git("log", "-1", "--format=%H").stdout.strip(), git("diff", "--quiet", "HEAD").returncode != 0
    torch.set_num_threads(P["threads"])
    import transformers.models.qwen2.modeling_qwen2 as M
    model = AutoModelForCausalLM.from_pretrained(paths.get(P["model_cell"]), dtype=torch.float32,
                                                 attn_implementation="eager").eval()
    W.install(M)
    c = model.config
    nkv, n = c.num_key_value_heads, c.num_hidden_layers * c.num_key_value_heads
    L, lo, hi, ch, N = P["L"], P["score_lo"], P["score_hi"], P["lm_head_chunk"], P["score_hi"] - P["score_lo"]
    W.S.update(bad=W.disallow(L, P["W"], P["sinks"]), win={}, dist=None, lo=lo, hi=hi)
    ev = [d for d, _ in P["fresh_docs"]]
    overlap = bool(set(ev) & exclusions(P)) or len(set(ev)) != len(ev) or len(ev) != P["n_fresh"]
    froz = frozen_ok(P, R3)
    docs = W.load_docs(tok, dict(P, eval_docs=P["fresh_docs"][1:], calib_doc=P["fresh_docs"][0]))
    ks = dict(zip(map(str, P["budgets"]), P["k"]))
    kept = {b: W.kept_fraction(k, P["W"], P["sinks"], L, n) for b, k in ks.items()}
    arms = {b: {"direct": P["frozen_direct_ranking"][:k], "sinkcount": P["frozen_sinkcount_ranking"][:k],
                "distance": R2["arms"][b]["distance"], **{a: h for a, h in R1["arms"][b].items() if a != "ref"}}
            for b, k in ks.items()}
    same_k = all(len(h) == ks[b] for b in arms for h in arms[b].values())   # one W, one mask for every arm
    kept_ok = all(kept[b] == R1["table"][b]["kept"] == R3["table"][b]["kept"] for b in arms)
    solo = [[h] for h in P["frozen_direct_ranking"][:max(P["k"])]]   # for additivity
    sets = list(dict.fromkeys(key(h) for h in [h for A in arms.values() for h in A.values()] + solo))
    part = os.path.join(out, "partial.json")   # checkpoint per pass; a resumed doc must reproduce its reference sha
    st = json.load(open(part)) if os.path.exists(part) else {"P": P, "passes": {}, "done": [], "repro": True,
                                                             "h_sha256": {}, "resumed": []}
    assert st["P"] == P, "partial.json belongs to another grid"
    for d in [d for d in ev if d not in st["done"]]:
        h1, h2 = X.hidden(model, docs[d], lo, hi), X.hidden(model, docs[d], lo, hi)
        sha = hashlib.sha256(h1.numpy().tobytes()).hexdigest()
        if str(d) in st["h_sha256"]:
            st["repro"] &= sha == st["h_sha256"][str(d)]
            st["resumed"].append(d)
        st["repro"] &= bool(torch.equal(h1, h2))
        st["h_sha256"][str(d)], pd = sha, st["passes"].setdefault(str(d), {})
        for s in [s for s in sets if s not in pd]:
            pd[s] = X.scored(model, h1, docs[d], [int(x) for x in s.split(",")], nkv, lo, hi, ch)
            print(f"{time.time() - t0:7.0f}s doc {d} heads {s} agree, kl {pd[s]}", flush=True)
            json.dump(st, open(part, "w"))
        st["done"].append(d)
        json.dump(st, open(part, "w"))
    pool = lambda s, i: sum(st["passes"][str(d)][s][i] * N for d in ev) / (N * len(ev))  # noqa: E731  (as runs 1-3)
    table = {}
    for b, A in arms.items():
        row = {a: {m: pool(key(h), i) for i, m in enumerate(("agree", "kl"))} for a, h in A.items()}
        rmin, rmax = ({m: f(v[m] for a, v in row.items() if a.startswith("random")) for m in ("agree", "kl")}
                      for f in (min, max))
        dk, sol, sol3 = row["direct"]["kl"], [pool(str(h), 1) for h in A["direct"]], [
            R3["mean_direct_kl"][h] for h in A["direct"]]
        table[b] = {"arms": row, "random_min": rmin, "random_max": rmax, "kept": kept[b],
                    "beats_random": row["direct"]["agree"] > rmax["agree"] and dk < rmin["kl"],
                    "kl_below_sinkcount": dk < row["sinkcount"]["kl"],
                    "additivity": {"joint_kl": dk, "solo_sum": sum(sol), "ratio": additivity(dk, sol),
                                   "solo_sum_run3": sum(sol3), "ratio_run3": additivity(dk, sol3)}}
    rw, sw = (sum(t[x] for t in table.values()) for x in ("beats_random", "kl_below_sinkcount"))
    void = overlap or not (froz and st["repro"] and same_k and kept_ok)
    res = {"P": P, "params_sha256": psha, "script_commit": commit, "script_dirty": dirty, "torch": torch.__version__,
           "verdict": "void" if void else ["disproved", "proved"][rw >= P["need_random_wins"] and sw >= P[
               "need_sinkcount_kl_wins"]], "random_wins": rw, "sinkcount_kl_wins": sw, "fresh_overlap": overlap,
           "frozen_equals_run3": froz, "full_repro_bitexact": st["repro"], "same_k": same_k,
           "kept_equals_run1_run3": kept_ok, "docs_resumed_mid_doc": st["resumed"], "full_h_sha256": st["h_sha256"],
           "table": table, "arms": arms, "passes": st["passes"], "n_scored_per_doc": N,
           "per_doc": [{"doc": d, "budget": b, "arm": a, "agree": st["passes"][str(d)][key(h)][0],
                        "kl": st["passes"][str(d)][key(h)][1]} for d in ev for b, A in arms.items() for a, h in
                       A.items()], "wall_s": round(time.time() - t0, 1)}
    lines = [f"# L4 direct round: {res['verdict']} (DIRECT beats random {rw}/3, needs {P['need_random_wins']}; DIRECT "
             f"KL < sinkcount KL {sw}/3, needs {P['need_sinkcount_kl_wins']})", "", f"fresh docs {ev}; script {commit} "
             f"dirty {dirty}; params sha256 {psha}", "", f"void checks: fresh overlap {overlap}; frozen == run 3 {froz}; "
             f"full-KV bit-exact x2 {st['repro']}; same k {same_k}; kept == runs 1/3 {kept_ok}", "",
             "| budget | k | kept | metric | DIRECT | random min-max | sinkcount | distance | band | DIRECT beats random "
             "| DIRECT KL < sinkcount |", "|---" * 11 + "|"]
    for b, r in table.items():
        for m, f in (("agree", ".4f"), ("kl", ".5f")):
            v = [f"{(r if x[:3] == 'ran' else r['arms'])[x][m]:{f}}" for x in (
                "direct", "random_min", "random_max", "sinkcount", "distance", "band")]
            lines.append(f"| {b} | {ks[b]} | {r['kept']:.4f} | {m} | {v[0]} | {v[1]}-{v[2]} | {' | '.join(v[3:])} | "
                         f"{r['beats_random']} | {r['kl_below_sinkcount']} |")
    lines += ["", "| budget | k | joint KL | solo sum (fresh) | ratio | solo sum (run 3 calib) | ratio_run3 |",
              "|---" * 7 + "|"] + [f"| {b} | {ks[b]} | " + " | ".join(f"{r['additivity'][x]:.5f}" for x in (
                  "joint_kl", "solo_sum", "ratio", "solo_sum_run3", "ratio_run3")) + " |" for b, r in table.items()]
    X.dump(out, res, lines)
    os.remove(part)


if __name__ == "__main__":
    main()
