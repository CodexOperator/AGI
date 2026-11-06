#!/usr/bin/env python3
"""REACHED WITNESSES (goal:g5.51 v3, hypothesis:lm-a-superset-witness-over-states-what-a-gate-ever-emitted): g5.50
called a mutant gate NON-vacuous on a witness in a SUPERSET of its outputs (all class histograms). Here each such gate's
OWN construction runs at its round's PRE-RUN code on N fresh, pre-declared seeds (a draw = one seed of all its streams,
training included), and the gate reads WITNESSED iff some draw's output reads not-RED under it AND the kernel checks
that output from its committed counts; else UNKNOWN (reach probability < 3/N at 95%). VACUOUS calls are re-checked.

Drivers: each gate's draw repeats, line for line, the part of its round's run_seed that builds that gate's outputs,
importing the round's own modules from `git archive <pre-run>` (never edited); FIDELITY: the driver run on the round's
OWN first seed must reproduce the round's committed numbers exactly (draw 0), else that gate is VOID.
Stages (CLI): fidelity | draws | gen | check | score; `worker` is internal (one subprocess per gate and round tree).
g5.50's module and checker are IMPORTED (osc_bend2_vacuity, bend2_vacuity.bend); g5.42's run_bend is the watchdog."""
import io, json, os, shutil, subprocess, sys, tarfile, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]

N_S, N_R = 64, 512
PLASMA = ".agi/context/local-maxxing/plasma"
ROUNDS = {   # round: (pre-run commit, results commit, the committed params + results dir)
    "g5.39": ("7b75964aea", "0cf9035b09", "datasets/plasma/2026-11-05-g5.39-joint-samples"),
    "g5.41": ("cee90e7bff", "d48b32691e", "datasets/plasma/2026-11-05-g5.41-blend-race"),
    "g5.43": ("f93be0f7b3", "d04861ed6f", "datasets/plasma/2026-11-05-g5.43-code-inputs"),
    "g5.46": ("29b9084b23", "c6a3e3de09", "datasets/plasma/2026-11-05-g5.46-cvae"),
}
# gate: (round, driver, g5.50 call, conjuncts as g5.50 reads them: (reading, arm, p, q) or (dist reading, arm, k))
GATES = {
    "g539_M2": ("g5.39", "m2", "non_vacuous", [("score_ge", "true", 9, 10), ("valid_le", "coin", 1, 20)]),
    "g541_M2": ("g5.41", "m2", "non_vacuous", [("score_ge", "true", 9, 10), ("valid_le", "coin", 1, 20)]),
    "g543_M2": ("g5.43", "m2", "non_vacuous", [("score_ge", "true", 9, 10), ("valid_le", "coin", 1, 20)]),
    "g546_M2": ("g5.46", "m2", "non_vacuous", [("score_ge", "true", 9, 10), ("valid_le", "coin", 1, 20)]),
    "g546_MC": ("g5.46", "mc", "non_vacuous", [("dist_ge", "mc", 150)]),
    "g543_Mz2": ("g5.43", "mz2", "non_vacuous", [("valid_le", "test", 1, 10)]),
    "g546_MK": ("g5.46", "mk", "non_vacuous", [("score_le", "test", 1, 20), ("dist_le", "rich", 16)]),
    # controls (falsifier 3)
    "U_synth": (None, "synth", "control_witnessed", [("score_le", "test", 1, 20)]),
    "U_z3enum": ("g5.43", "z3enum", "control_witnessed", [("score_le", "test", 1, 20)]),
    "O_one_image": ("g5.39", "one_image", "control_not_witnessed", [("score_le", "test", 1, 20)]),
}
VACUOUS = ["g539_M1", "g541_M1S", "g541_M1C", "g543_Mz1", "g543_Mz6"]   # g5.50's vacuous calls, re-checked
SEED0 = 55100001   # fresh draws: SEED0 .. SEED0 + N - 1, disjoint from every round's seeds (53901 .. 54605)


TOP = subprocess.run(["git", "-C", HERE, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()


def git(*a, text=True):
    """git at the repo's TOP level, so a pathspec is repo-rooted (never relative to this file's dir)."""
    return subprocess.run(["git", "-C", TOP, *a], capture_output=True, check=True, text=text).stdout


def round_tree(rnd, work):
    """the round's plasma dir at its pre-run, extracted once (git archive; never edited)."""
    c = ROUNDS[rnd][0]
    d = os.path.join(work, "round-" + rnd)
    if not os.path.isdir(d):   # extract to a temp dir, then rename: a failed extract never leaves a half tree
        tmp = d + ".tmp"
        shutil.rmtree(tmp, ignore_errors=True)
        os.makedirs(tmp)
        tarfile.open(fileobj=io.BytesIO(git("archive", c, PLASMA, text=False))).extractall(tmp, filter="data")
        os.rename(tmp, d)
    return os.path.join(d, PLASMA)


def committed(rnd):
    """the round's params.json and results.json, read by git show at its RESULTS commit."""
    _, rc, ds = ROUNDS[rnd]
    return json.loads(git("show", f"{rc}:{ds}/params.json")), json.loads(git("show", f"{rc}:{ds}/results.json"))


# ---------- the worker: runs INSIDE one round's tree (sys.path = that tree only) ----------
def counts(samples, cue, tmpl, tcls, iou_min, E):
    """per-cue valid class counts (a, b) over the cue's pair, by g539's score rule (valid: integer IoU + class in pair)."""
    import numpy as np
    inter = samples @ tmpl.T
    union = samples.sum(1, keepdims=True) + tmpl.sum(1)[None] - inter
    best = (inter / union).argmax(1)
    r = np.arange(len(samples))
    num, den = iou_min
    hit = num * np.rint(inter[r, best]).astype(np.int64) >= den * np.rint(union[r, best]).astype(np.int64)
    cls = tcls[best]
    valid = hit & np.isin(cls, E.PAIRS[cue])
    pa, pb = E.PAIRS[cue]
    return [int((valid & (cls == pa)).sum()), int((valid & (cls == pb)).sum())]


def worker(driver, rnd, seeds, out_path):
    import numpy as np
    import g537_line_orientation as G37
    import g539_joint_samples as E
    p, _ = committed(rnd) if rnd else (None, None)
    tmpl, tcls = E.templates(p if p else committed("g5.39")[0])
    d = (p or committed("g5.39")[0])
    dd, iou_min = d["data"], d["score"]["iou_min"]
    done = set()
    if os.path.exists(out_path):
        done = {json.loads(l)["seed"] for l in open(out_path)}
    for seed in seeds:
        if seed in done:
            continue
        if os.path.exists("/fast/.game-on"):
            print(json.dumps({"paused": "game-on"}), flush=True)
            return 9
        t0 = time.time()
        row = {"seed": seed}
        if driver == "m2":
            mod = {"g5.39": None, "g5.41": "g541_blend_race", "g5.43": "g543_code_inputs", "g5.46": "g546_cvae"}[rnd]
            M = __import__(mod) if mod else E
            ids = getattr(M, "ARM_IDS", None) or getattr(M, "ARM", None)
            t_id, c_id = (E.ARM_TRUE, E.ARM_COIN) if mod is None else (ids["TRUE"], ids["COIN"])
            for arm in ("true", "coin"):
                row[arm] = []
            for c in (0, 1):   # the round's M2 block, line for line
                r = E.rng_for(seed, E.M2_STREAM, t_id, 0, c)
                yy = np.repeat(np.array(E.PAIRS[c]), N_S // 2)
                lines, _ = G37.make_lines(r, N_S, dd["side"], dd["width"], 0.0, dd["jitter_deg"], dd["max_offset"], y=yy)
                coin = (E.rng_for(seed, E.M2_STREAM, c_id, 0, c).random(size=(N_S, dd["side"] ** 2)) < 0.5).astype(np.float64)
                row["true"].append({**E.score(lines, c, tmpl, tcls, iou_min), "ab": counts(lines, c, tmpl, tcls, iou_min, E)})
                row["coin"].append({**E.score(coin, c, tmpl, tcls, iou_min), "ab": counts(coin, c, tmpl, tcls, iou_min, E)})
        elif driver == "mc":
            import g546_cvae as K
            row["mc"] = []
            for c in (0, 1):
                r = E.rng_for(seed, E.M2_STREAM, K.ARM_IDS["MC"], 0, c)
                yy = np.repeat(np.array(E.PAIRS[c]), N_R // 2)
                lines, _ = G37.make_lines(r, N_R, dd["side"], dd["width"], 0.0, dd["jitter_deg"], dd["max_offset"], y=yy)
                row["mc"].append(K.distinct_valid(lines, c, tmpl, tcls, iou_min))
        elif driver in ("mz2", "z3enum", "mk"):
            ss = np.random.SeedSequence(seed)   # run_seed's setup, line for line (g543 / g546 run_seed)
            r_data, r_init, r_batch, r_tnoise = [np.random.default_rng(s) for s in ss.spawn(4)]
            n = dd["n_train"]
            cue = r_data.integers(0, 2, size=n)
            pick = r_data.integers(0, 2, size=n)
            y = np.array([E.PAIRS[cc][q] for cc, q in zip(cue, pick)])
            t, _ = G37.make_lines(r_data, n, dd["side"], dd["width"], 0.0, dd["jitter_deg"], dd["max_offset"], y=y)
            x = np.eye(2)[cue]
            batch_seed, tnoise_seed = int(r_batch.integers(2 ** 63)), int(r_tnoise.integers(2 ** 63))
            row["test"] = []
            if driver == "mk":
                import g546_cvae as K
                net = K.train_cv(K.init_cv(r_init, 2), x, t, p, np.random.default_rng(batch_seed), np.random.default_rng(tnoise_seed), zero_z=True)
                samp = lambda c, k, rr: K.sample_cv(net, c, k, rr)
                aid = K.ARM_IDS["MK"]
                row["rich"] = [K.distinct_valid(samp(c, N_R, E.rng_for(seed, K.RICH, aid, 0, c)), c, tmpl, tcls, iou_min) for c in (0, 1)]
            else:
                import g543_code_inputs as C
                name = "MZ2" if driver == "mz2" else "Z3-ENUM"
                arm = p["code_arms"][name]
                net, _ = C.train_code(E.init_net(r_init, [2 + arm["dim"], 32, 64]), x, t, arm, p,
                                      np.random.default_rng(batch_seed), np.random.default_rng(tnoise_seed))
                samp = lambda c, k, rr: C.sample_code(net, c, k, arm, rr)
                aid = C.ARM_IDS[name]
            for c in (0, 1):
                s = samp(c, N_S, E.rng_for(seed, E.TEST, aid, 0, c))
                row["test"].append({**E.score(s, c, tmpl, tcls, iou_min), "ab": counts(s, c, tmpl, tcls, iou_min, E)})
        elif driver == "synth":   # M-UNDER (a): each of 64 samples is class A or B with p 1/2 (a recorded stream)
            r = np.random.default_rng(seed)
            row["test"] = []
            for c in (0, 1):
                a = int(r.binomial(N_S, 0.5))
                ab = [a, N_S - a]
                v = sum(ab)
                cov = -sum(k / v * np.log2(k / v) for k in ab if k)
                row["test"].append({"valid": 1.0, "coverage": float(cov), "score": float(cov), "ab": ab})
        elif driver == "one_image":   # M-OVER: one image repeated (the cue pair's first-class template), any seed
            row["test"] = []
            for c in (0, 1):
                img = tmpl[list(tcls).index(E.PAIRS[c][0])]
                s = np.repeat(img[None], N_S, 0)
                row["test"].append({**E.score(s, c, tmpl, tcls, iou_min), "ab": counts(s, c, tmpl, tcls, iou_min, E)})
        row["wall_s"] = round(time.time() - t0, 3)
        for arm in ("true", "coin", "test"):
            for x_ in row.get(arm, []):
                assert abs(sum(x_["ab"]) / N_S - x_["valid"]) < 1e-12, "counts disagree with the round's own valid"
        with open(out_path, "a") as f:
            f.write(json.dumps(row, sort_keys=True) + "\n")
    return 0


# ---------- the gate's reading over one draw (the round's own floats) ----------
def mean(xs):
    return sum(xs) / len(xs)


def reading(gid, row):
    """-> list of (conjunct index, holds): the gate reads 'as required' iff every conjunct holds."""
    out = []
    for i, (r, arm, *th) in enumerate(GATES[gid][3]):
        if r == "score_ge":
            out.append((i, mean([x["score"] for x in row[arm]]) >= th[0] / th[1]))
        elif r == "score_le":
            out.append((i, mean([x["score"] for x in row[arm]]) <= th[0] / th[1]))
        elif r == "valid_le":
            out.append((i, mean([x["valid"] for x in row[arm]]) <= th[0] / th[1]))
        elif r == "dist_ge":
            out.append((i, min(row[arm]) >= th[0]))
        elif r == "dist_le":
            out.append((i, max(row[arm]) <= th[0]))
    return out


def reached(gid, row):
    """-> the first conjunct the draw breaks (a not-RED output), or None."""
    return next((i for i, ok in reading(gid, row) if not ok), None)


# ---------- orchestration (the main process: git, the workers, bend) ----------
import paths  # noqa: E402
import osc_bend2_law as L  # noqa: E402


def out_dir():
    return paths.get_local("bend2_reach_dir")


def work_dir():
    return os.path.join(os.environ.get("FALSIFY_SCRATCH", "/data/scratch/director-thought-1"), "reach-work")


def run_worker(gid, seeds, out_path):
    rnd, driver = GATES[gid][0], GATES[gid][1]
    tree = round_tree(rnd or "g5.39", work_dir())
    env = {**os.environ, "PYTHONPATH": tree, "PYTHONDONTWRITEBYTECODE": "1",   # ONE thread: a person's PC, CPU only
           "OMP_NUM_THREADS": "1", "OPENBLAS_NUM_THREADS": "1", "MKL_NUM_THREADS": "1"}
    code = ("import sys, json; sys.path[:0] = [%r, %r, %r]; import osc_bend2_reach as W; "
            "sys.exit(W.worker(%r, %r, json.loads(sys.argv[1]), sys.argv[2]))") % (tree, HERE, os.path.dirname(HERE), driver, rnd)
    py = os.environ.get("REACH_PYTHON", sys.executable)
    p = subprocess.run(["nice", "-n", "10", py, "-c", code, json.dumps(seeds), out_path], env=env, capture_output=True, text=True)
    if p.returncode not in (0, 9):
        raise RuntimeError(f"worker {gid} rc {p.returncode}: {p.stderr[-2000:]}")
    return p.returncode


def draw0_expect(gid):
    """the round's own committed numbers for its FIRST seed, in the driver's row shape (fidelity)."""
    rnd, driver = GATES[gid][0], GATES[gid][1]
    _, R = committed(rnd)
    s = R["seeds"][0]
    if driver == "m2":
        return s["seed"], {"true": [c["score"] for c in s["M2_true"]["cues"]], "coin": [c["valid"] for c in s["M2_coin"]["cues"]]}
    if driver == "mc":
        return s["seed"], {"mc": s["MC_distinct"]}
    if driver == "mk":
        return s["seed"], {"test": [c["score"] for c in s["MK"]["test"]["cues"]], "rich": s["MK"]["rich_distinct"]}
    name = {"mz2": "MZ2", "z3enum": "Z3-ENUM"}[driver]
    return s["seed"], {"test": [c["valid"] if driver == "mz2" else c["score"] for c in s[name]["test"]["cues"]]}


def stage_fidelity():
    """draw 0: each driver on its round's OWN first seed must reproduce the committed numbers EXACTLY; the wall of that
    run is the per-draw estimate for N. Writes fidelity.json (before any fresh draw)."""
    o = out_dir()
    os.makedirs(os.path.join(o, "draws"), exist_ok=True)
    res = {}
    for gid, (rnd, driver, call, _) in GATES.items():
        if rnd is None or driver == "one_image":
            res[gid] = {"applies": False, "why": "no committed round output (a planted control)"}
            continue
        seed, want = draw0_expect(gid)
        path = os.path.join(o, "draws", f"{gid}.draw0.jsonl")
        if os.path.exists(path):
            os.remove(path)
        run_worker(gid, [seed], path)
        row = json.loads(open(path).read().splitlines()[0])
        got = {k: ([x["score"] if (driver != "mz2" and (k != "coin")) else x["valid"] for x in row[k]]
                   if isinstance(row[k][0], dict) else row[k]) for k in want}
        res[gid] = {"seed": seed, "want": want, "got": got, "exact": got == want, "wall_s": row["wall_s"]}
        print(gid, "exact" if got == want else "DIFFERS", row["wall_s"], flush=True)
    json.dump(res, open(os.path.join(o, "fidelity.json"), "w"), indent=1, sort_keys=True)


def load_P():
    pp = os.path.join(out_dir(), "params.json")
    return json.load(open(pp)), L.sha(pp)


def seeds_for(P, gid):
    return [SEED0 + i for i in range(P["N"][gid])]


def stage_draws():
    """the fresh draws, resumable (a draw already in the file is never re-run); pauses on /fast/.game-on."""
    P, _ = load_P()
    for gid in GATES:
        path = os.path.join(out_dir(), "draws", f"{gid}.jsonl")
        t0 = time.time()
        rc = run_worker(gid, seeds_for(P, gid), path)
        print(gid, "paused (game-on)" if rc == 9 else "done", round(time.time() - t0, 1), flush=True)
        if rc == 9:
            return 9


def rows(gid, P):
    want = seeds_for(P, gid)
    got = {r["seed"]: r for r in map(json.loads, open(os.path.join(out_dir(), "draws", f"{gid}.jsonl")))}
    assert sorted(got) == want, f"{gid}: the draws on disk are not exactly the pre-declared seeds"
    return [got[s] for s in want]


def first_witness(gid, rs):
    """-> (draw index, row, conjunct) of the FIRST reached not-RED draw, in seed order, or None."""
    for i, r in enumerate(rs):
        k = reached(gid, r)
        if k is not None:
            return i, r, k
    return None


# ---------- laws (g5.50's checker, imported) ----------
def wit_law(gid, row, k):
    """the reached output as a LITERAL of its committed counts; WIT checks it breaks conjunct k; VAC (the gate read
    'as required' over exactly these outputs) is its opposite and must FAIL."""
    r, arm, *th = GATES[gid][3][k]
    if r.startswith("dist"):
        ds = row[arm]
        x = max(ds) if r == "dist_le" else min(ds)
        lit = f"def s() -> +List<U32>:\n  [{', '.join(str(d) for d in ds)}]\n\ndef w() -> U32:\n  {x}\n"
        wit = f"A.wit_{r}(D.s(), D.w(), {th[0]})"
        vac = f"A.vac_{r}(D.s(), {th[0]})"
    else:
        o0, o1 = (x["ab"] for x in row[arm])
        lit = (f"def s() -> +List<A.O>:\n  [A.O{{{o0[0]}, {o0[1]}}}, A.O{{{o1[0]}, {o1[1]}}}]\n\n"
               f"def w0() -> A.O:\n  A.O{{{o0[0]}, {o0[1]}}}\n\ndef w1() -> A.O:\n  A.O{{{o1[0]}, {o1[1]}}}\n")
        wit = f"A.wit_{r}(D.s(), D.w0(), D.w1(), {N_S}, {th[0]}, {th[1]})"
        vac = f"A.vac_{r}(D.s(), {N_S}, {th[0]}, {th[1]})"
    return lit, wit, vac


def law_dir_files(lit, expr, name):
    return {"A.bend": open(os.path.join(HERE, "bend2_vacuity.bend")).read(),
            "LIT.bend": "import Base\nimport ./A.bend as A\n\n" + lit,
            "LAWS.bend": f"import Base\nimport ./A.bend as A\nimport ./LIT.bend as D\n\nlaw {name}:\n  {{A.b2u({expr}) == 1 : U32}}\n",
            "PROOF.bend": f"import Base\nimport ./LAWS.bend as Laws\n\ndef Laws.{name}():\n  {{==}}\n"}


def inserted_vacuity_law(vgid, witness):
    """a g5.50 VACUOUS gate's for-all with a REACHED witness inserted into its O_g literal: must FAIL."""
    import osc_bend2_vacuity as V
    g = next(x for x in V.resolved() if x["id"] == vgid)
    r, kind, *th = g["conj"][0]
    if r.startswith("dist"):
        lit = "def s0() -> +List<U32>:\n  " + V.dl(V.space(kind) + [witness]) + "\n"
    else:
        lit = "def s0() -> +List<A.O>:\n  " + V.ol(V.space(kind) + [tuple(witness)]) + "\n"
    return lit, V.call("vac", 0, g["conj"][0])


def stage_gen():
    P, _ = load_P()
    o = out_dir()
    sets, files, wit = {}, {}, {}
    for gid in GATES:
        w = first_witness(gid, rows(gid, P))
        wit[gid] = None if w is None else {"draw": w[0], "seed": w[1]["seed"], "conjunct": w[2]}
        if w is None:
            continue
        lit, wexpr, vexpr = wit_law(gid, w[1], w[2])
        for name, expr, want, role in (("wit", wexpr, "check", "witness"), ("vac_opp", vexpr, "fail", "opposite")):
            k = f"{gid}_{name}"
            files[k] = L.write_dir(os.path.join(o, "laws", k), law_dir_files(lit, expr, name))
            sets[k] = {"gate": gid, "want": want, "role": role}
    # the reached witnesses inserted into the VACUOUS gates (falsifier 2): a score one and a distinct-count one
    z = rows("U_z3enum", P)[wit["U_z3enum"]["draw"]] if wit["U_z3enum"] else None
    mc = rows("g546_MC", P)[0]
    import osc_bend2_vacuity as V
    for vg in VACUOUS:
        r = next(x for x in V.resolved() if x["id"] == vg)["conj"][0][0]
        if r.startswith("dist"):
            ins = max(mc["mc"])   # a reached distinct count (g5.46 MC's first fresh draw)
        elif z is None:
            continue
        else:
            ins = max((x["ab"] for x in z["test"]), key=lambda ab: (2 * ab[0] * ab[1]) / max(sum(ab), 1))
        lit, expr = inserted_vacuity_law(vg, ins)
        k = f"{vg}_vac_inserted"
        files[k] = L.write_dir(os.path.join(o, "laws", k), law_dir_files(lit, expr, "vac"))
        sets[k] = {"gate": vg, "want": "fail", "role": "vacuous_opposite", "inserted": ins}
        # g5.50's own vacuity law, re-checked from its committed dir
        src = os.path.join(V.out_dir(), "laws", f"{vg}_vac")
        k = f"{vg}_vac_recheck"
        files[k] = L.write_dir(os.path.join(o, "laws", k), {f: open(os.path.join(src, f)).read() for f in sorted(os.listdir(src))})
        sets[k] = {"gate": vg, "want": "check", "role": "vacuous_recheck"}
    json.dump({"files": files, "sets": sets, "witness": wit}, open(os.path.join(o, "laws_files.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps({"n_sets": len(sets), "witnessed": sorted(g for g, w in wit.items() if w)}))


def stage_check():
    P, psha = load_P()
    o = out_dir()
    F = json.load(open(os.path.join(o, "laws_files.json")))
    res = {}
    for k in sorted(F["sets"]):
        d = os.path.join(o, "laws", k)
        assert all(L.sha(os.path.join(d, f)) == h for f, h in F["files"][k].items()), k
        r = L.run_bend(P, d, False)
        res[k] = {**{x: r[x] for x in ("status", "wall_s", "peak_rss_mib")}, "want": F["sets"][k]["want"], "tail": r["tail"][-4:]}
        if F["sets"][k]["want"] == "check":
            v = L.run_bend(P, d, True)
            res[k]["verdict"] = {x: v[x] for x in ("status", "wall_s", "peak_rss_mib")}
        print(k, r["status"], F["sets"][k]["want"], r["wall_s"], flush=True)
    json.dump({"params_sha256": psha, "sets": res}, open(os.path.join(o, "check.json"), "w"), indent=1, sort_keys=True)


def score(P, fid, F, C, cap_s):
    """the falsifier, read mechanically (committed before any draw)."""
    res, sets = C["sets"], F["sets"]
    st = lambda k: res[k]["status"] if k in res else None
    over = sorted(k for k, r in res.items() if r["status"] in ("rss_cap", "wall_cap") or r["wall_s"] > cap_s
                  or r.get("verdict", {}).get("status") in ("rss_cap", "wall_cap") or r.get("verdict", {}).get("wall_s", 0) > cap_s)
    errs = sorted(k for k, r in res.items() if r["status"] not in ("check", "fail", "rss_cap", "wall_cap"))
    unfaithful = sorted(g for g, f in fid.items() if f.get("applies", True) and not f.get("exact"))
    calls = {}
    for gid in GATES:
        w = F["witness"][gid]
        if w is None:
            calls[gid] = {"call": "UNKNOWN", "reach_bound_95": f"< {3 / P['N'][gid]:.4g} (rule of three, N = {P['N'][gid]})"}
        else:
            ok = st(f"{gid}_wit") == "check" and res[f"{gid}_wit"].get("verdict", {}).get("status") == "check" and st(f"{gid}_vac_opp") == "fail"
            calls[gid] = {"call": "WITNESSED" if ok else "WITNESS_UNCHECKED", **w}
        calls[gid]["predicted"] = P["predicted"][gid]
        calls[gid]["as_predicted"] = calls[gid]["call"] == P["predicted"][gid]
        d0 = fid.get(gid, {})
        calls[gid]["draw0_exact"] = d0.get("exact")
    for vg in VACUOUS:
        ok = st(f"{vg}_vac_recheck") == "check" and st(f"{vg}_vac_inserted") == "fail"
        calls[vg] = {"call": "VACUOUS" if ok else "NOT_VACUOUS", "predicted": P["predicted"][vg]}
        calls[vg]["as_predicted"] = calls[vg]["call"] == P["predicted"][vg]
    nonvac = [g for g, v in GATES.items() if v[2] == "non_vacuous"]
    void = ([f"over the cap: {over}"] if over else []) + ([f"bend errors: {errs}"] if errs else []) + (
        [f"a driver does not replay its round's own draw 0: {unfaithful}"] if unfaithful else [])
    if calls["O_one_image"]["call"] != "UNKNOWN":
        void.append("M-OVER came out WITNESSED: the search reads the superset")
    unknown_void = [g for g in ("U_synth", "U_z3enum") if calls[g]["call"] != "WITNESSED"]
    if unknown_void and any(calls[g]["call"] == "UNKNOWN" for g in nonvac):
        void.append(f"M-UNDER control(s) not WITNESSED {unknown_void}: every UNKNOWN is VOID")
    opp_ok = all(st(k) == "fail" for k, s in sets.items() if s["want"] == "fail")
    if void:
        h = "void"
    elif all(calls[g]["call"] == "WITNESSED" for g in nonvac):
        h = "disproved"
    elif (any(calls[g]["call"] == "UNKNOWN" for g in nonvac) and all(calls[v]["call"] == "VACUOUS" for v in VACUOUS)
          and not any(calls[g]["call"] == "WITNESS_UNCHECKED" for g in GATES)):
        h = "proved"
    else:
        h = "disproved"
    return {"void": void, "H_REACH": h, "counterproofs_all_fail": opp_ok, "calls": calls,
            "predicted_right": sum(v["as_predicted"] for v in calls.values()), "n_calls": len(calls),
            "max_wall_s": max((r["wall_s"] for r in res.values()), default=0),
            "max_peak_rss_mib": max((r["peak_rss_mib"] for r in res.values()), default=0)}


def stage_score():
    P, psha = load_P()
    o = out_dir()
    fid, F, C = (json.load(open(os.path.join(o, f))) for f in ("fidelity.json", "laws_files.json", "check.json"))
    V = {"params_sha256": psha, "check_sha256": L.sha(os.path.join(o, "check.json")), **score(P, fid, F, C, P["wall_cap_s"])}
    json.dump(V, open(os.path.join(o, "verdict.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps({k: V[k] for k in ("void", "H_REACH", "counterproofs_all_fail", "predicted_right", "n_calls")}))
    print(json.dumps({g: v["call"] for g, v in V["calls"].items()}))


if __name__ == "__main__":
    sys.exit({"fidelity": stage_fidelity, "draws": stage_draws, "gen": stage_gen, "check": stage_check, "score": stage_score}[sys.argv[1]]())
