#!/usr/bin/env python3
"""POSITIVE CONTROL (hypothesis:lm-neuron-periodicity-pipeline-finds-the-known-mod-p-circuit): grok (a+b) mod 113 in
a 1-layer transformer; read its MLP neurons with MAP run 2's IMPORTED dpeak / detrended_null (unchanged) -> P1, P2, P3.
Grid = <cell osc_neuron_period_pc_dir>/params.json. Run detached; resumable from <out>/partial."""
import csv, hashlib, json, os, shutil, subprocess, sys, time
import numpy as np, torch
import torch.nn.functional as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_neuron_period2 as R2  # noqa: E402  run 2: dpeak + detrended_null (unchanged); R2.S = run 1 (wait_box)
import paths  # noqa: E402


class OneLayer(torch.nn.Module):
    """(a, b, '='): embed + pos -> causal attention -> ReLU MLP -> unembed, no LayerNorm; MLP runs at '=' only (the
    only read-out, position-wise: same logits). abl = (mask, values) overwrites post-ReLU; seen = last post-ReLU."""

    def __init__(self, m):
        super().__init__()
        d, self.h, L = m["d_model"], m["n_heads"], torch.nn.Linear
        self.E = torch.nn.Parameter(torch.randn(m["vocab_in"], d) / d ** 0.5)
        self.pos = torch.nn.Parameter(torch.randn(m["n_ctx"], d) / d ** 0.5)
        self.qkv, self.o, self.w_in = L(d, 3 * d, bias=False), L(d, d, bias=False), L(d, m["d_mlp"])
        self.w_out, self.U, self.abl, self.seen = L(m["d_mlp"], d), L(d, m["vocab_out"], bias=False), None, None

    def forward(self, x):
        r = F.one_hot(x, len(self.E)).to(self.E.dtype) @ self.E + self.pos   # one-hot: deterministic backward
        B, T, d = r.shape
        q, k, v = self.qkv(r).view(B, T, 3, self.h, d // self.h).permute(2, 0, 3, 1, 4)
        r = r + self.o(F.scaled_dot_product_attention(q, k, v, is_causal=True).transpose(1, 2).reshape(B, T, d))
        h = F.relu(self.w_in(r[:, -1]))
        self.seen = (h := h if self.abl is None else torch.where(self.abl[0], self.abl[1], h)).detach()
        return self.U(r[:, -1] + self.w_out(h))


make = lambda P, seed: (torch.manual_seed(seed), OneLayer(P["model"]))[1]


def data(P):
    """All p*p rows (a, b, '=') at index a*p+b, labels (a+b) mod p, the seeded disjoint train / test index split."""
    a, b = np.divmod(np.arange((p := P["p"]) ** 2), p)
    perm, n = np.random.default_rng(P["split_seed"]).permutation(p * p), int(P["train_fraction"] * p * p)
    return (torch.from_numpy(np.stack([a, b, np.full_like(a, p)], 1)), torch.from_numpy((a + b) % p),
            torch.from_numpy(np.sort(perm[:n])), torch.from_numpy(np.sort(perm[n:])))


def evaluate(model, X, y, abl=None):   # -> (loss, acc)
    model.abl = abl
    with torch.no_grad():
        lg, model.abl = model(X).double(), None
    return F.cross_entropy(lg, y).item(), (lg.argmax(1) == y).double().mean().item()


psi = lambda: float(open("/proc/pressure/memory").read().split()[1].split("=")[1])


def train(P, part, seed, X, y, tr, te, log):
    """Full-batch AdamW to the grok rule, step cap or wall cap; checkpoints make a relaunch resume exactly."""
    ck, model, o = os.path.join(part, f"ckpt_s{seed}.pt"), make(P, seed), P["optimizer"]
    opt = torch.optim.AdamW(model.parameters(), lr=o["lr"], weight_decay=o["weight_decay"], betas=tuple(o["betas"]))
    if os.path.exists(ck):
        model.load_state_dict((z := torch.load(ck))["model"]), opt.load_state_dict(z["opt"])
    st = z["st"] if os.path.exists(ck) else {"step": 0, "curve": [], "wall": 0.0}
    t0, c, ev = time.time() - st["wall"], st["curve"], P["eval_every"]
    n_hold = P["grok_hold_steps"] // ev + 1   # evals in the hold window
    save = lambda: torch.save({"model": model.state_dict(), "opt": opt.state_dict(),
                               "st": {**st, "wall": time.time() - t0}}, ck)
    while True:
        if (s := st["step"]) % ev == 0:
            if not c or c[-1][0] != s:
                c.append([s, *evaluate(model, X[tr], y[tr]), *evaluate(model, X[te], y[te])])
                if s % 1000 == 0:
                    log(f"seed {seed} step {s}: train loss/acc {c[-1][1]:.4g}/{c[-1][2]:.4f} test loss/acc "
                        f"{c[-1][3]:.4g}/{c[-1][4]:.4f} psi {psi()} ({time.time() - t0:.0f}s)")
            held = len(c) >= n_hold and all(r[4] >= P["grok_threshold"] for r in c[-n_hold:])
            if held or s >= P["step_cap"] or time.time() - t0 > P["wall_cap_s"]:
                save()
                break
            if psi() >= P["box_stop_psi_some_avg10"]:
                save(), log(f"memory psi >= {P['box_stop_psi_some_avg10']} at step {s}: checkpointed, exit 3")
                sys.exit(3)
            if s and s % P["checkpoint_every"] == 0:
                save()
        loss = F.cross_entropy(model(X[tr]).double(), y[tr])
        opt.zero_grad(), loss.backward(), opt.step()
        st["step"] += 1
    return model, {"seed": seed, "grokked": held, "grok_step": c[-n_hold][0] if held else None, "steps": s,
                   "wall_s": round(time.time() - t0, 1), "curve": c,
                   **dict(zip(("final_train_loss", "final_train_acc", "final_test_loss", "final_test_acc"), c[-1][1:]))}


def sweep(model, P):
    """(a, b, '=') for a = 0..p-1 per b in b_set -> post-ReLU activations at '=' -> (len(b_set), p, d_mlp)."""
    p, a = P["p"], torch.arange(P["p"])
    with torch.no_grad():
        model(torch.cat([torch.stack([a, torch.full_like(a, b), torch.full_like(a, p)], 1) for b in P["b_set"]]))
    return model.seen.view(len(P["b_set"]), p, -1).numpy().astype(np.float64)


def stat(acts, tol):
    """Imported detrended peakiness per b, averaged over b; dominant bin = most common per-b bin (ties smallest)."""
    pk, kb = zip(*(R2.dpeak(x, tol) for x in acts))
    return np.mean(pk, 0), np.array([int(np.bincount(col).argmax()) for col in np.array(kb).T])


def null(acts, P):   # imported permute-then-detrend null per b (same 20 perms per b), averaged over b -> (20, d_mlp)
    return np.mean([R2.detrended_null(x, P["null_permutations"], P["null_seed"], P["detrend_tol"]) for x in acts], 0)


def main():
    out = paths.get_local("osc_neuron_period_pc_dir")
    pp, part = os.path.join(out, "params.json"), os.path.join(out, "partial")
    P, sha = json.load(open(pp)), hashlib.sha256(open(pp, "rb").read()).hexdigest()
    log = lambda m, f=open(os.path.join(out, "run.log"), "a"): (print(m, flush=True), f.write(m + "\n"), f.flush())
    os.makedirs(part, exist_ok=True)
    if not os.path.exists(fs := os.path.join(part, "start.json")):
        json.dump({"params_sha256": sha}, open(fs, "w"))
    torch.set_num_threads(P["threads"]), R2.S.wait_box(P)
    log(f"launch: params sha256 {sha}, torch {torch.__version__}")
    (X, y, tr, te), runs = data(P), []
    for seed in (P["train_seed"], P["fallback_seed"]):   # the fallback seed is the ONE pre-declared fallback
        model, r = train(P, part, seed, X, y, tr, te, log)
        runs.append(r), log(f"seed {seed}: " + json.dumps({k: v for k, v in r.items() if k != "curve"}))
        if r["grokked"]:
            break
    torch.save(model.state_dict(), fm := os.path.join(out, "model.pt"))
    with open(os.path.join(out, "curve.csv"), "w", newline="") as f:
        csv.writer(f).writerows([["seed", "step", "train_loss", "train_acc", "test_loss", "test_acc"]] +
                                [[r["seed"], *row] for r in runs for row in r["curve"]])
    tol, acts, twin = P["detrend_tol"], sweep(model.eval(), P), sweep(make(P, P["twin_seed"]).eval(), P)
    (pk, kb), tpk, nl = stat(acts, tol), stat(twin, tol)[0], null(acts, P)
    q, tmax, n = float(np.quantile(nl, P["null_quantile"])), float(tpk.max()), acts.shape[2]
    p1 = np.flatnonzero((pk > q) & (pk > tmax))
    ks, cnt = np.unique(kb[p1], return_counts=True)
    ks, cnt = ks[o := np.lexsort((ks, -cnt))], cnt[o]   # count desc, ties smallest k
    n_cover = int(np.searchsorted(np.cumsum(cnt), P["p2_cover"] * len(p1)) + 1) if len(p1) else 0
    fam = [int(i) for i in p1 if kb[i] == ks[0]] if len(p1) else []
    evaluate(model, X, y)
    means, rs = model.seen.mean(0), {s: sorted(int(i) for i in np.random.default_rng(s).choice(
        np.setdiff1d(np.arange(n), fam), len(fam), replace=False)) for s in P["random_seeds"]}   # mean over p*p at '='
    arm = lambda ids: evaluate(model, X[te], y[te], (torch.isin(torch.arange(n), torch.tensor(ids, dtype=int)), means))
    (bl, ba), (fl, fa), ra = arm([]), arm(fam), [arm(rs[s]) for s in P["random_seeds"]]
    rdrop = [ba - a for _, a in ra]
    np.savez_compressed(os.path.join(out, "acts.npz"), acts=acts.astype(np.float32), twin=twin.astype(np.float32),
                        peak=pk, k=kb, twin_peak=tpk, null=nl, means=means.numpy())
    g, match_ok = runs[-1], all(len(v) == len(fam) and not set(v) & set(fam) for v in rs.values())
    void = not (g["grokked"] and g["final_test_acc"] >= P["grok_threshold"] and match_ok and os.path.exists(fm)
                and acts.shape == twin.shape == (len(P["b_set"]), P["p"], P["model"]["d_mlp"])
                and nl.shape == (P["null_permutations"], n) and json.load(open(fs))["params_sha256"] == sha)
    v1, v2 = len(p1) / n >= P["p1_min_fraction"], bool(len(p1)) and n_cover <= P["p2_max_freqs"]
    v3 = bool(fam) and (ba - fa) > max(rdrop)
    git = lambda *a: subprocess.run(["git", "-C", HERE, *a, "--", __file__], capture_output=True, text=True)
    R = {"verdict": "void" if void else "proved" if v1 and v2 and v3 else "disproved", "void": void,
         "match_ok": match_ok, "params_sha256": sha, "script_commit": git("log", "-1", "--format=%H").stdout.strip(),
         "script_dirty": git("diff", "--quiet", "HEAD").returncode != 0,
         "train": [{k: v for k, v in r.items() if k != "curve"} for r in runs],
         "p1": {"pass": bool(v1), "count": len(p1), "fraction": len(p1) / n, "n_neurons": n, "null_q999": q,
                "null_n": int(nl.size), "twin_seed": P["twin_seed"], "twin_max": tmax,
                "count_beat_null": int((pk > q).sum()), "count_beat_twin": int((pk > tmax).sum()),
                "flat_or_dead": int((pk == 0).sum()), "pk_median": float(np.median(pk)), "members": p1.tolist()},
         "p2": {"pass": bool(v2), "n_cover": n_cover, "freq_counts": {int(k): int(c) for k, c in zip(ks, cnt)},
                "cover_fraction": float(cnt[:n_cover].sum() / len(p1)) if len(p1) else 0.0},
         "p3": {"pass": bool(v3), "freq": int(ks[0]) if len(p1) else None, "size": len(fam), "baseline_test_acc": ba,
                "baseline_test_loss": bl, "ablated_test_acc": fa, "ablated_test_loss": fl, "drop": ba - fa,
                "rand_drop": rdrop, "rand_test_acc": [a for _, a in ra], "rand_test_loss": [l for l, _ in ra],
                "members": fam, "rand_sets": {str(s): v for s, v in rs.items()}}, "torch": torch.__version__}
    json.dump(R, open(os.path.join(out, "results.json"), "w"), indent=1)
    shutil.rmtree(part)
    sh = lambda d: {k: sh(v) if type(v) is dict else v for k, v in d.items() if k not in ("members", "rand_sets")}
    lines = [f"# POSITIVE CONTROL: {R['verdict']}", ""] + [f"- {k}: {json.dumps(v)}" for k, v in sh(R).items()]
    log(t := "\n".join(lines)), open(os.path.join(out, "summary.md"), "w").write(t + "\n")


if __name__ == "__main__":
    main()
