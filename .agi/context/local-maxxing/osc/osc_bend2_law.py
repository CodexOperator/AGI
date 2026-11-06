#!/usr/bin/env python3
"""BEND2's FIRST LAW (goal:g5.42, hypothesis:lm-bend2-kernel-checks-the-int8-readout-of-the-mod-113-cut): STEP 0 the 8-bit
parity staircase LAW + its refused mutant; STEP 1 the int8 readout of goal:g5.38's OMP-24 cut over a committed tape,
argmax(nonmlp_q + h_q . W_q + b_q) = (a + b) mod 113 on EXACTLY X of 12769 pairs, checked by bend (the checker evaluates;
X is never imported), with X +- 1 and a one-weight flip as counter-proofs. Stages (CLI): tape (torch) | reference | gen | check.
The g5.36 / g5.38 modules are IMPORTED, never edited. Grid = <cell bend2_law_dir>/params.json."""
import hashlib, itertools, json, os, re, signal, subprocess, sys, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import paths  # noqa: E402

P2 = 2 ** 32
M31 = 2 ** 31
sha = lambda path: hashlib.sha256(open(path, "rb").read()).hexdigest()
u32 = lambda v: int(v) % P2


# ---------- STEP 1 integer semantics (the reference) ----------
def logits(h, n, W, b):   # python ints: n_j + b_j + sum_i h_i W_ij
    return [n[j] + b[j] + sum(h[i] * W[i][j] for i in range(len(h))) for j in range(len(n))]


def hit(L, label):   # argmax with a tie counted as wrong
    m = max(L)
    return int(L.count(m) == 1 and L.index(m) == label)


def hit_u32(h, n, W, b, label):
    """The LAW's own semantics, emulated: U32 wrap-around arithmetic, signed compare by the sign-bit flip, the scan from
    best = 0x80000000 (the most negative value), strict > replaces, == sets the tie flag, > clears it."""
    bi, bv, tie = 0, M31, False
    for j in range(len(n)):
        v = u32(u32(n[j]) + u32(b[j]))
        for i in range(len(h)):
            v = u32(v + u32(h[i]) * u32(W[i][j]))
        gt, eq = (v ^ M31) > (bv ^ M31), v == bv
        bi, bv, tie = (j if gt else bi), (v if gt else bv), (not gt) and (eq or tie)
    return int((not tie) and bi == label)


def count(T, W=None, rows=None):
    """X over the tape (python ints): -> (X_all, X_test, X_by_a); T = dict of int lists (h, n, W, b, test)."""
    W, p, xa, xt = W if W is not None else T["W"], T["p"], [], 0
    for a in (rows if rows is not None else range(p)):
        s = 0
        for b_ in range(p):
            k = a * p + b_
            c = hit(logits(T["h"][k], T["n"][k], W, T["b"]), (a + b_) % p)
            s, xt = s + c, xt + c * T["test"][k]
        xa.append(s)
    return sum(xa), xt, xa


def flip_choice(T, X):
    """Largest-|w| entry of W_q (ties -> smallest flat index i*113+j); negated; if the count stays X, the next-largest."""
    order = sorted(((abs(w), -(i * len(r) + j), i, j) for i, r in enumerate(T["W"]) for j, w in enumerate(r)), reverse=True)
    tried = []
    for _, _, i, j in order:
        Wf = [list(r) for r in T["W"]]
        Wf[i][j] = -Wf[i][j]
        Xf = count(T, Wf)[0]
        tried.append({"i": i, "j": j, "w": T["W"][i][j], "X_flip": Xf})
        if Xf != X:
            return {"i": i, "j": j, "w": T["W"][i][j], "X_flip": Xf, "tried": tried}
    return {"i": None, "tried": tried}


# ---------- the tape (torch; g5.36 / g5.38 imported) ----------
def build_tape(P):
    import numpy as np, torch
    import osc_neuron_period_cut as Z   # g5.36: feats / solve / install (+ S, F)
    S, F = Z.S, Z.F
    ck = P["checkpoint"]
    assert F.sha(ck["path"]) == ck["sha256"], "checkpoint sha"
    keep = json.load(open(F.rp(P["omp24_source"]["path"])))["picks"]["omp"][P["omp24_source"]["key"]]
    assert len(keep) == 24 and F.sha(P["omp24_source"]["path"]) == P["omp24_source"]["sha256"]
    model = S.make(P, ck["train_seed"])
    model.load_state_dict(torch.load(F.rp(ck["path"])))
    model.eval()
    torch.set_num_threads(P["threads"])
    X, y, tr, te = S.data(P)
    with torch.no_grad():
        target = model(X[tr]).double()
    h_tr, rest_tr = Z.feats(model, X[tr])
    Wp, uerr = Z.solve(h_tr, rest_tr, target, keep, model.U.weight.detach().double())   # the cut's readout, train rows only
    U = model.U.weight.detach().double()
    Wl, bl = (Wp[:-1] @ U.T).numpy(), (Wp[-1] @ U.T).numpy()          # (24, 113), (113,): W_out composed with U
    h_all, rest_all = Z.feats(model, X)
    h, nm = h_all[:, keep].numpy(), rest_all.numpy()                   # (12769, 24), (12769, 113)
    fl = nm + h @ Wl + bl                                              # the float cut, for the replay check
    float_test_acc = float((fl[te.numpy()].argmax(1) == y[te].numpy()).mean())
    s_h, s_W = float(np.abs(h).max()) / 127, float(np.abs(Wl).max()) / 127   # fixed BEFORE quantizing
    q8 = lambda x, s: np.clip(np.rint(x / s), -127, 127).astype(np.int64)
    hq, Wq = q8(h, s_h), q8(Wl, s_W)
    acc_s = s_h * s_W
    nq, bq = np.rint(nm / acc_s).astype(np.int64), np.rint(bl / acc_s).astype(np.int64)
    test = np.zeros(len(X), dtype=np.int64)
    test[te.numpy()] = 1
    bound = int(np.abs(nq).max() + np.abs(bq).max() + 24 * 127 * 127)
    T = {"p": P["p"], "keep": [int(k) for k in keep], "h": hq.tolist(), "n": nq.tolist(), "W": Wq.tolist(), "b": bq.tolist(),
         "test": test.tolist()}
    meta = {"s_h": s_h, "s_W": s_W, "acc_scale": acc_s, "u_err": uerr, "float_cut_test_acc": float_test_acc,
            "int32_ok": bool(np.abs(nq).max() < M31 and np.abs(bq).max() < M31), "logit_bound": bound, "logit_bound_ok": bound < M31 - 1,
            "torch": torch.__version__, "numpy": np.__version__}
    return T, meta


# ---------- Bend files ----------
lit = lambda xs: "[" + ", ".join(str(u32(x)) for x in xs) + "]"


def law_file(T, laws, W=None, nr=None, nb=None):
    """LAWS.bend: the tape as defs (one per a), the readout columns, then each law (name, X, row or None = all);
    nr x nb restricts the tape to rows 0..nr-1 and pairs b = 0..nb-1 (tests only; the run uses the full 113 x 113)."""
    W, p = W if W is not None else T["W"], T["p"]
    nr, nb = nr or p, nb or p
    cols = ",\n    ".join(f"R.Col{{{u32(T['b'][j])}, {lit([W[i][j] for i in range(len(W))])}}}" for j in range(p))
    out = ["import Base", "import ./RO.bend as R", "", "def cols() -> +List<R.Col>:", f"  [{cols}]", ""]
    for a in range(nr):
        prs = ", ".join(f"R.Pr{{{lit(T['h'][a * p + b])}, {lit(T['n'][a * p + b])}}}" for b in range(nb))
        out += [f"def r{a}() -> List<R.Pr>:", f"  [{prs}]", ""]
    out += ["def tape() -> List<List<R.Pr>>:", "  [" + ", ".join(f"r{a}()" for a in range(nr)) + "]", ""]
    for name, X, a in laws:
        body = f"R.rows(tape(), cols(), 0, 0)" if a is None else f"R.row(r{a}(), cols(), {a}, 0, 0)"
        out += [f"law {name}:", f"  {{{body} == {u32(X)} : U32}}", ""]
    return "\n".join(out)


def proof_file(names):
    return "\n".join(["import Base", "import ./LAWS.bend as Laws", ""] + [f"def Laws.{n}():\n  {{==}}\n" for n in names])


def parity_files(mutant=False):
    """STEP 0: h_k = [sum x >= k], k = 1..8, input weights 1, output sum_k (-1)^(k+1) h_k (U32 wrap); the mutant's h_8
    output weight is +1 (wrong on exactly the all-ones input). LAW: for every x in {0,1}^8, net(x) = parity(x)."""
    xs = [f"x{i}" for i in range(8)]
    s = " + ".join(f"b2u({x})" for x in xs)
    s = s.split(" + ")
    acc = s[0]
    for t in s[1:]:
        acc = f"({acc} + {t} : U32)"
    terms = [f"(({u32((-1) ** (k + 1) if not (mutant and k == 8) else 1)} * ge(s, {k}) : U32))" for k in range(1, 9)]
    out = terms[0]
    for t in terms[1:]:
        out = f"({out} + {t} : U32)"
    sig = ", ".join(f"{x}: Bool" for x in xs)
    net = "\n".join(["import Base", "", "def b2u(x: Bool) -> U32:", "  match x:", "    case True{}:", "      1", "    case False{}:", "      0", "",
                     "def ge(+s: U32, k: U32) -> U32:", "  b2u(U32.is_ge(s, k))", "",
                     f"def net({sig}) -> U32:", f"  +s = {acc}", f"  {out}", "",
                     f"def parity({sig}) -> U32:", f"  ({acc} % 2 : U32)", ""])
    laws = "\n".join(["import Base", "import ./NET.bend as N", "", "law net_is_parity:"] + [f"  for {x}: Bool" for x in xs] +
                     [f"  {{N.net({', '.join(xs)}) == N.parity({', '.join(xs)}) : U32}}", ""])
    cases = "".join(f"    case {' '.join('True{}' if v else 'False{}' for v in bits)}:\n      {{==}}\n" for bits in itertools.product([True, False], repeat=8))
    proof = "import Base\nimport ./LAWS.bend as Laws\n\ndef Laws.net_is_parity(" + ", ".join(xs) + "):\n  match " + " ".join(xs) + ":\n" + cases
    return {"NET.bend": net, "LAWS.bend": laws, "PROOF.bend": proof}


def write_dir(d, files):
    os.makedirs(d, exist_ok=True)
    for k, v in files.items():
        open(os.path.join(d, k), "w").write(v)
    return {k: sha(os.path.join(d, k)) for k in sorted(files)}


# ---------- running bend under the RSS watchdog ----------
def tree_rss(pid):
    kids = {}
    for d in os.listdir("/proc"):
        if d.isdigit():
            try:
                kids.setdefault(int(open(f"/proc/{d}/stat").read().rsplit(")", 1)[1].split()[1]), []).append(int(d))
            except OSError:
                pass
    seen, fr, out = {pid}, [pid], 0
    while fr:
        for c in kids.get(fr.pop(), []):
            if c not in seen:
                seen.add(c), fr.append(c)
    for q in seen:
        try:
            out += int(next(l for l in open(f"/proc/{q}/status") if l.startswith("VmRSS:")).split()[1]) * 1024
        except (OSError, StopIteration):
            pass
    return out


def run_bend(P, d, verdict):
    """bend PROOF.bend [--verdict] in d; killed at the RSS cap or the wall cap. -> {status, wall_s, peak_rss_mib, tail}."""
    env = {**os.environ, "BEND_NO_TELEMETRY": "1", "PATH": f"{P['bend_bin']}:{P['lean_bin']}:{os.environ['PATH']}"}
    args, t0, peak, why = ["bend", "PROOF.bend"] + (["--verdict"] if verdict else ["--check-only"]), time.time(), 0, None
    p = subprocess.Popen(args, cwd=d, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, start_new_session=True)
    while p.poll() is None:
        peak = max(peak, tree_rss(p.pid))
        why = "rss_cap" if peak > P["rss_cap_bytes"] else "wall_cap" if time.time() - t0 > P["wall_cap_s"] else None
        if why:
            os.killpg(p.pid, signal.SIGKILL)
            p.wait()
            break
        time.sleep(0.1)
    out = re.sub(r"\x1b\[[0-9;]*m", "", p.stdout.read().decode(errors="replace"))
    st = why or ("check" if "ALL PROOFS CHECK" in out and p.returncode == 0 else "fail" if "SOME PROOFS FAIL" in out else f"error rc {p.returncode}")
    return {"status": st, "rc": p.returncode, "wall_s": round(time.time() - t0, 2), "peak_rss_mib": round(peak / 2 ** 20), "tail": out.strip().splitlines()[-8:]}


# ---------- stages ----------
def out_dir():
    return paths.get_local("bend2_law_dir")


def load_P():
    pp = os.path.join(out_dir(), "params.json")
    return json.load(open(pp)), sha(pp)


def stage_tape():
    P, psha = load_P()
    T, meta = build_tape(P)
    fp = os.path.join(out_dir(), "tape.json")
    json.dump(T, open(fp, "w"), separators=(",", ":"))
    meta.update(tape_sha256=sha(fp), params_sha256=psha)
    json.dump(meta, open(os.path.join(out_dir(), "tape_meta.json"), "w"), indent=1)
    print(json.dumps(meta))


def stage_reference():
    P, psha = load_P()
    T = json.load(open(os.path.join(out_dir(), "tape.json")))
    t0 = time.time()
    X, Xt, xa = count(T)
    wall = time.time() - t0
    p = T["p"]
    diff = [k for k in range(p * p) if hit(logits(T["h"][k], T["n"][k], T["W"], T["b"]), (k // p + k % p) % p) != hit_u32(T["h"][k], T["n"][k], T["W"], T["b"], (k // p + k % p) % p)]
    R = {"X_all": X, "X_test": Xt, "n_test": sum(T["test"]), "X_by_a": xa, "python_loop_wall_s": round(wall, 2), "u32_semantics_differ_on": diff,
         "flip": flip_choice(T, X), "tape_sha256": sha(os.path.join(out_dir(), "tape.json")), "params_sha256": psha}
    json.dump(R, open(os.path.join(out_dir(), "reference.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in R.items() if k != "X_by_a"}))


def stage_gen0():   # STEP 0 files, written into the dataset dir and committed with the pre-run
    shas = {k: write_dir(os.path.join(out_dir(), "step0", k), parity_files(k == "mutant")) for k in ("main", "mutant")}
    json.dump(shas, open(os.path.join(out_dir(), "step0_files.json"), "w"), indent=1)
    print(json.dumps(shas))


def stage_gen():
    """STEP 1 dirs from the tape + reference: law (X_all), fallback (113 row laws), counter-proofs X+1, X-1, flip."""
    P, _ = load_P()
    o = out_dir()
    T, R = json.load(open(os.path.join(o, "tape.json"))), json.load(open(os.path.join(o, "reference.json")))
    ro = open(os.path.join(HERE, "bend2_readout.bend")).read()
    X, f = R["X_all"], R["flip"]
    Wf = [list(r) for r in T["W"]]
    Wf[f["i"]][f["j"]] = -Wf[f["i"]][f["j"]]
    sets = {"law": ([("total", X, None)], None), "fallback": ([(f"row{a}", R["X_by_a"][a], a) for a in range(T["p"])], None),
            "cp_plus1": ([("total", X + 1, None)], None), "cp_minus1": ([("total", X - 1, None)], None), "cp_flip": ([("total", X, None)], Wf)}
    shas = {}
    for k, (laws, W) in sets.items():
        shas[k] = write_dir(os.path.join(P["work_dir"], "step1", k), {"RO.bend": ro, "LAWS.bend": law_file(T, laws, W), "PROOF.bend": proof_file([n for n, _, _ in laws])})
    json.dump(shas, open(os.path.join(o, "step1_files.json"), "w"), indent=1)
    print(json.dumps({k: v["LAWS.bend"][:12] for k, v in shas.items()}))


def stage_check():
    P, psha = load_P()
    o, res = out_dir(), {"params_sha256": psha}
    s0 = {}
    for k in ("main", "mutant"):
        d = os.path.join(o, "step0", k)
        s0[k] = {"check": run_bend(P, d, False), "verdict": run_bend(P, d, True)}
    ok0 = s0["main"]["check"]["status"] == "check" and s0["main"]["verdict"]["status"] == "check" and s0["main"]["verdict"]["wall_s"] <= P["step0_wall_cap_s"]
    refused = s0["mutant"]["check"]["status"] == "fail" and s0["mutant"]["verdict"]["status"] != "check"
    res["step0"] = {**s0, "discharged": ok0, "mutant_refused": refused, "red": not (ok0 and refused)}
    if res["step0"]["red"]:
        res["verdict"] = "disproved (STEP 0 RED: the leaf stops)"
    else:
        w = os.path.join(P["work_dir"], "step1")
        law = run_bend(P, os.path.join(w, "law"), False)
        res["step1_law"] = law
        if law["status"] in ("rss_cap", "wall_cap"):
            res["step1_fallback"] = run_bend(P, os.path.join(w, "fallback"), False)
        done = law["status"] == "check" or res.get("step1_fallback", {}).get("status") == "check"
        if done:
            for k in ("cp_plus1", "cp_minus1", "cp_flip"):
                res[k] = run_bend(P, os.path.join(w, k), False)
            res["step1_law_verdict"] = run_bend(P, os.path.join(w, "law" if law["status"] == "check" else "fallback"), True)
        res["step1_discharged"] = done
    res["launch_params_sha256"] = psha
    json.dump(res, open(os.path.join(o, "check.json"), "w"), indent=1)
    print(json.dumps({k: (v if not isinstance(v, dict) else {kk: (vv if not isinstance(vv, dict) else {x: vv[x] for x in ("status", "wall_s", "peak_rss_mib")}) for kk, vv in v.items()} if "status" not in v else {x: v[x] for x in ("status", "wall_s", "peak_rss_mib")}) for k, v in res.items()}, indent=1))


if __name__ == "__main__":
    {"gen0": stage_gen0, "tape": stage_tape, "reference": stage_reference, "gen": stage_gen, "check": stage_check}[sys.argv[1]]()
