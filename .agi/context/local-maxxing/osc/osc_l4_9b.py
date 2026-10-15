#!/usr/bin/env python3
# L4 run 5 (hypothesis:lm-l4-direct-head-windows-hold-on-the-served-9b): DIRECT per-KV-head windowing cost on the
# served Qwen3.5-9B Q4_K_M GGUF, scored by llama-perplexity --kl-divergence in upstream llama.cpp at a pinned sha with
# head-window.patch (per-KV-head 4 sinks + last 128, flash-attn off, CPU, its own memory-capped container).
# Phases: --pick (tokenizer only) | --rank (calibration bases, zero-mask check, 32 solo heads -> ranking.json) |
# --freeze (ranking + seeded random sets -> params.json; commit BEFORE scoring) | --score (fresh docs, ctx 2048).
# Grid: <cell osc_l4_9b_dir>/params.json; outputs beside it; build trees, docs, logits, logs under params scratch.
import hashlib, json, os, random, re, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import paths  # noqa: E402

DONE = re.compile(r"Final estimate: PPL|Mean +KLD:")
key = lambda heads: ",".join(map(str, heads))  # noqa: E731
sha = lambda path: hashlib.sha256(open(path, "rb").read()).hexdigest()  # noqa: E731


def allowed(t, j, W, sinks):   # mirror of head-window.patch for a windowed head: causal AND (sink OR last W)
    return j <= t and (j < sinks or t - j < W)


def spec(heads, P):   # head index i -> "layer:kv_head" with i = (rank of the full-attention layer) * n_kv + kv_head
    return ",".join(f"{P['full_layers'][i // P['n_kv_heads']]}:{i % P['n_kv_heads']}" for i in sorted(heads))


def pick(lens, excl, n, m):   # deterministic: the first n articles in file order with >= m tokens, not excluded
    return [i for i, x in enumerate(lens) if x >= m and i not in excl][:n]


def parse_kl(text):   # llama-perplexity --kl-divergence summary block
    g = lambda pat: float(re.search(pat, text).group(1))  # noqa: E731
    return {"kl": g(r"Mean +KLD: +(-?[\d.]+)"), "same_top": g(r"Same top p: +([\d.]+)") / 100}


def exclusions(P):   # every doc id runs 1-4 touched (eval, calibration, doc 13, run 4's fresh) + this run's calib
    # (run 1's single calib_doc 12 is also run 2's calibration doc and in calib_ids)
    ids = set(P["calib_ids"])
    for p in (json.load(open(os.path.join(paths.get_local(c), "params.json"))) for c in P["prior_cells"]):
        ids |= {d for k in ("eval_docs", "calib_docs", "fresh_docs") for d, *_ in p.get(k, [])} | set(
            p.get("exclude_docs", []))
    return ids


def articles(P):   # run 1's article split of the same wiki.valid file
    parts = re.split(r"(?m)^ = ([^=].*?) = \n", open(os.path.join(os.path.dirname(paths.get(
        P["text_cell"])), P["text_file"]), encoding="utf-8").read())
    return list(zip(parts[1::2], parts[2::2]))


def docker(P, argv, env=None):   # the one capped container; the GGUF mounted read-only
    return ["docker", "run", "--rm", "--name", "l4-9b-pass", *P["docker_cap"], "-u", f"{os.getuid()}:{os.getgid()}",
            "-v", f"{(S := P['scratch'])}:{S}", "-v", f"{(g := os.path.dirname(paths.get(P['gguf_cell'])))}:{g}:ro",
            *[x for k, v in (env or {}).items() for x in ("-e", f"{k}={v}")],
            P["image"], f"{S}/llama.cpp-{argv[0]}/build/bin/{argv[1]}", "-m", paths.get(P["gguf_cell"]), *argv[2:]]


mem = lambda: (int(next(x for x in open("/proc/meminfo") if x.startswith("MemAvailable")).split()[1]) // 1024,  # noqa
               float(re.search(r"some avg10=([\d.]+)", open("/proc/pressure/memory").read()).group(1)))


def run(P, tag, argv, env=None):   # ONE model process; its log is the checkpoint; killed + retried at PSI >= stop
    log = f"{P['scratch']}/logs/{tag}.log"
    while not (os.path.exists(log) and DONE.search(open(log, errors="ignore").read())):
        while (m := mem())[0] < P["min_avail_mib"] or m[1] >= P["psi_start"]:
            time.sleep(print(f"gate wait: avail {m[0]} MiB psi {m[1]}", flush=True) or P["wait_s"])
        t, stop, pr = time.time(), False, subprocess.Popen(docker(P, argv, env), stdout=open(log, "w"), stderr=-2)
        while pr.poll() is None:
            time.sleep(5)
            if not stop and mem()[1] >= P["psi_stop"]:
                stop = subprocess.run(["docker", "kill", "l4-9b-pass"], capture_output=True) is not None
        if not stop and not DONE.search(open(log, errors="replace").read()):
            raise RuntimeError(f"{tag} failed rc {pr.returncode}: see {log}")
        print(f"{time.time() - t:6.0f}s {tag} {'PSI STOP, retry' if stop else 'ok'} (gate {m})", flush=True)
    return open(log, errors="replace").read()


def ppl(P, build, d, kl, suffix=""):   # base: write doc d's reference logits; kl: score against them
    return [build, "llama-perplexity", "-c", (c := str(P["ctx"])), "-b", c, "--chunks", "1", "-t", str(P["threads"]),
            "-fa", "off", "--no-warmup", "--kl-divergence-base", f"{(S := P['scratch'])}/base/{d}.kld{suffix}",
            *(["--kl-divergence"] if kl else ["-f", f"{S}/docs/{d}.txt"])]


def prepare(P, docs):   # doc file = the article body repeated past 2*ctx tokens (llama-perplexity's floor); with
    A = articles(P)     # --chunks 1 only the first ctx tokens are evaluated, all inside the first copy (margin)
    for d, title, ntok in docs:
        assert A[d][0] == title and ntok >= P["ctx"] + P["margin"], (d, title, ntok)
        open(f"{P['scratch']}/docs/{d}.txt", "w", encoding="utf-8").write(A[d][1] * (2 * P["ctx"] // ntok + 2))
        run(P, f"base_{d}", ppl(P, "base", d, False))


def kl(P, d, heads):
    return parse_kl(run(P, f"kl_{d}_{key(heads)}", ppl(P, "patched", d, True), {
        "LLAMA_HEAD_WINDOW": spec(heads, P), "LLAMA_HEAD_WINDOW_W": P["W"], "LLAMA_HEAD_WINDOW_SINKS": P["sinks"]}))


def ranking(P):   # DIRECT: each head windowed alone, mean KL over the calibration docs, ascending, ties by index
    mean = {h: sum(kl(P, d, [h])["kl"] for d, *_ in P["calib_docs"]) / len(P["calib_docs"])
            for h in range(P["n_heads"])}
    return sorted(mean, key=lambda h: (mean[h], h)), mean


def main():
    out, t0 = paths.get_local("osc_l4_9b_dir"), time.time()
    S = (P := json.load(open(os.path.join(out, "params.json"))))["scratch"]
    [os.makedirs(f"{S}/{sub}", exist_ok=True) for sub in ("docs", "base", "logs")]
    if "--pick" in sys.argv:   # tokenizer only: llama-tokenize loads the GGUF vocab, no weights
        A = articles(P)
        lens = [int(re.search(r"Total number of tokens: (\d+)", subprocess.run(docker(P, [
            "base", "llama-tokenize", "-p", body, "--show-count", "--ids", "--log-disable"]), capture_output=True,
            text=True, check=True).stdout).group(1)) for _, body in A]
        return print(json.dumps({"calib_docs": [[d, A[d][0], lens[d]] for d in P["calib_ids"]], "fresh_docs": [[
            d, A[d][0], lens[d]] for d in pick(lens, exclusions(P), P["n_fresh"], P["ctx"] + P["margin"])],
            "excluded": sorted(exclusions(P)), "lens": lens}))
    if "--rank" in sys.argv:
        prepare(P, P["calib_docs"])
        # zero-mask check on calibration doc 0: the patched build with NO heads listed, vs the unpatched base
        z = parse_kl(run(P, f"zero_kl_{(d0 := P['calib_docs'][0][0])}", ppl(P, "patched", d0, True)))
        run(P, f"zero_base_{d0}", ppl(P, "patched", d0, False, ".zero"))
        (rk, mean), b = ranking(P), f"{S}/base/{d0}.kld"
        z.update(doc=d0, base_sha256=sha(b), zero_base_sha256=sha(b + ".zero"))
        return json.dump({"ranking": rk, "mean_direct_kl": mean, "zero_mask": z}, open(f"{out}/ranking.json", "w"))
    if "--freeze" in sys.argv:   # the frozen ranking + seeded random sets, written into params.json by program
        P["frozen_direct_ranking"], n = json.load(open(f"{out}/ranking.json"))["ranking"], P["n_heads"]
        P["random_sets"] = {str(k): [sorted(random.Random(s).sample(range(n), k)) for s in P["seeds"]] for k in P["ks"]}
        return json.dump(P, open(f"{out}/params.json", "w"), indent=1)
    F, R, psha = [d for d, *_ in P["fresh_docs"]], json.load(open(f"{out}/ranking.json")), sha(f"{out}/params.json")
    froz = P["frozen_direct_ranking"] == R["ranking"] == ranking(P)[0]   # re-read from the calibration logs only
    zero = R["zero_mask"]["base_sha256"] == R["zero_mask"]["zero_base_sha256"] and R["zero_mask"]["kl"] <= P["zero_tol"]
    overlap = bool(set(F) & exclusions(P)) or len(set(F)) != len(F) or len(F) != P["n_fresh"]
    prepare(P, P["fresh_docs"])
    arms = {str(k): {"direct": sorted(P["frozen_direct_ranking"][:k]), **{f"random_s{s}": h for s, h in zip(
        P["seeds"], P["random_sets"][str(k)])}} for k in P["ks"]}
    passes = {str(d): {key(h): kl(P, d, h) for A in arms.values() for h in A.values()} for d in F}
    table, rows, v = {}, [], lambda d, h, m="kl": passes[str(d)][key(h)][m]  # noqa: E731
    for k, A in arms.items():   # pooled = mean over docs (each doc scores the same 1023 tokens)
        r = {a: {m: sum(v(d, h, m) for d in F) / len(F) for m in ("kl", "same_top")} for a, h in A.items()}
        rk, rs = ([x[m] for a, x in r.items() if a != "direct"] for m in ("kl", "same_top"))
        docs = sum(v(d, A["direct"]) < min(v(d, h) for a, h in A.items() if a != "direct") for d in F)
        table[k] = {"arms": r, "random_kl": [min(rk), max(rk)], "random_same_top": [min(rs), max(rs)],
                    "direct_beats_all_random": r["direct"]["kl"] < min(rk), "docs_direct_beats_all": docs}
        rows.append(f"| {k} | {1 - int(k) / P['n_heads']:.2f} | {r['direct']['kl']:.6f} | {min(rk):.6f}-{max(rk):.6f}"
                    f" | {r['direct']['same_top']:.4f} | {min(rs):.4f}-{max(rs):.4f} | {docs}/{len(F)} |")
    wins = sum(t["direct_beats_all_random"] for t in table.values())
    git = lambda *a: subprocess.run(["git", "-C", HERE, *a, "--", __file__], capture_output=True, text=True)  # noqa
    res = {"P": P, "params_sha256": psha, "llama_cpp_sha": P["llama_cpp_sha"], "script_commit": git(
        "log", "-1", "--format=%H").stdout.strip(), "script_dirty": git("diff", "--quiet", "HEAD").returncode != 0,
           "verdict": "void" if overlap or not (froz and zero) else ["disproved", "proved"][wins == len(arms)],
           "k_wins": wins, "frozen_equals_calibration": froz, "zero_mask_ok": zero, "zero_mask": R["zero_mask"],
           "fresh_overlap": overlap, "table": table, "arms": arms, "passes": passes, "wall_s": round(time.time() - t0)}
    json.dump(res, open(f"{out}/results.json", "w"), indent=1)
    open(f"{out}/summary.md", "w").write("\n\n".join([
        f"# L4 run 5 (served 9B, ctx {P['ctx']}): {res['verdict']} (DIRECT KL < every random set at {wins}/2 k)",
        f"fresh docs {F}; llama.cpp {P['llama_cpp_sha']}; script {res['script_commit']} dirty {res['script_dirty']}",
        f"void checks: fresh overlap {overlap}; frozen == ranking.json == calibration logs {froz}; zero mask {zero}: "
        f"{R['zero_mask']}", "| k | kept | DIRECT KL | random KL min-max | DIRECT same-top | random same-top min-max |"
        " docs DIRECT < every random |\n" + "|---" * 7 + "|\n" + "\n".join(rows)]) + "\n")


if __name__ == "__main__":
    main()
