#!/usr/bin/env python3
"""BEND2 VACUITY LAWS (goal:g5.50, hypothesis:lm-bend2-kernel-calls-a-mutant-gate-vacuous-or-shows-a-witness): per closed
round's mutant gate g of the joint-samples family (g5.39, g5.41, g5.43, g5.46: every gate read through g5.39's scorer),
its construction-implied OUTPUT SPACE O_g stated from the round's code with a file:line citation at the round's pre-run
(a trusted premise: the scope), and the gate's reading over O_g as a bend2 LAW: VACUOUS = for EVERY o in O_g the gate
reads "as required" (it could not have failed); NON-VACUOUS = a WITNESS o* in O_g where it definitely does not.
O_g: a frozen draw on a deterministic decoder = ONE-CLASS per-cue histograms; every other gate = ALL histograms of its n
(distinct-image counters: 0..n, or the construction's own cap). The checker bend2_vacuity.bend bounds score exactly in
integers (coverage 0 on one class, <= 1, >= 2ab / v^2). Stages (CLI): cites (git) | gen | check (bend only) | score.
g5.42's module (osc_bend2_law) is IMPORTED, never edited: run_bend (the RSS watchdog), write_dir, sha."""
import collections, json, math, os, re, subprocess, sys
from fractions import Fraction as Fr

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_bend2_law as L  # noqa: E402
import paths  # noqa: E402

N, N_RICH = 64, 512   # samples per cue (every round's params n_samples); g5.46's n_rich
PL = ".agi/context/local-maxxing/plasma/"
F39, F41, F43, F46 = (("7b75964aea", PL + "g539_joint_samples.py"), ("cee90e7bff", PL + "g541_blend_race.py"),
                      ("f93be0f7b3", PL + "g543_code_inputs.py"), ("29b9084b23", PL + "g546_cvae.py"))
E41 = ("cee90e7bff", PL + "g539_joint_samples.py")   # g5.41 imports g5.39's sampler (E): read at g5.41's pre-run
at = lambda f, l: (f[0], f[1], l)
site = lambda draw, call, dec=None: {"draw": draw, "call": call, "dec": dec}
VALID = at(F39, 55)   # a valid sample's class lies in the cue's pair: a per-cue valid histogram has two classes
S39_M1 = site(at(F39, 122), at(F39, 183), at(F39, 125))
M2 = lambda f, lt, lc: [("score_ge", site(at(f, lt), at(f, lt)), N, 9, 10), ("valid_le", site(at(f, lc), at(f, lc)), N, 1, 20)]

# conjunct: (reading, site, n of its instrument, threshold p, q) or (dist reading, site, n, k). The site's three lines
# decide O_g's class by the committed rule o_class (falsifier 5): nothing below names a class by hand.
GATES = [
    {"id": "g539_M1", "round": "g5.39", "review": "vacuous", "review_src": "goal:g5.43 Falsifier 5 note + g539_m1_residue.py docstring (SM gate 12:41Z): one noise row broadcast, coverage 0 for ANY net",
     "text": "M1 P with ONE noise draw frozen per seed and cue scores <= 0.05 on every seed", "conj": [("score_le", S39_M1, N, 1, 20)]},
    {"id": "g539_M2", "round": "g5.39", "review": None, "text": "M2 the scorer: 64 true target lines per cue (32 per class) score >= 0.9, and 64 Bernoulli(0.5) images have valid fraction <= 0.05",
     "conj": M2(F39, 194, 196)},
    {"id": "g541_M1S", "round": "g5.41", "review": None, "text": "M1-S = S with every unit frozen at its likelier state scores <= 0.05 on every seed",
     "conj": [("score_le", site(at(F41, 206), at(F41, 266), at(F41, 210)), N, 1, 20)]},
    {"id": "g541_M1C", "round": "g5.41", "review": None, "text": "M1-C = G-chamfer with ONE draw frozen per seed and cue scores <= 0.05 on every seed",
     "conj": [("score_le", site(at(E41, 122), at(F41, 260), at(E41, 125)), N, 1, 20)]},
    {"id": "g541_M2", "round": "g5.41", "review": None, "text": "M2 = the scorer arm as in g5.39", "conj": M2(F41, 276, 278)},
    {"id": "g543_Mz1", "round": "g5.43", "review": "vacuous", "review_src": "goal:g5.43 close (v3): Mz1 is VACUOUS BY CONSTRUCTION on all five latent arms",
     "text": "Mz1 EVERY latent arm with its latent FIXED at sampling scores <= 0.05 on every seed",
     "conj": [("score_le", site(at(F43, 85), at(F43, 155), at(F43, 94)), N, 1, 20)]},
    {"id": "g543_Mz2", "round": "g5.43", "review": "non_vacuous", "review_src": "goal:g5.43 close (v3): Mz2 a real kill (valid 0.0 on all seeds; review's own variant agrees)",
     "text": "Mz2 Z3 trained with ONE uniform code PER TARGET per step ... falls to valid <= 0.1 on every seed",
     "conj": [("valid_le", site(at(F43, 85), at(F43, 153), at(F43, 94)), N, 1, 10)]},
    {"id": "g543_Mz6", "round": "g5.43", "review": None, "text": "Mz6 Z6-ENUM sampled through (code mod 8) ... must read distinct valid images < 16 per cue on EVERY seed",
     "conj": [("dist_le", site(at(F43, 90), at(F43, 157), at(F43, 94)), N, 15)]},
    {"id": "g543_M2", "round": "g5.43", "review": "non_vacuous", "review_src": "goal:g5.43 close (v3): M2 RED",
     "text": "M2 the scorer arm as in g5.39", "conj": M2(F43, 166, 168)},
    {"id": "g546_MK", "round": "g5.46", "review": "non_vacuous", "review_src": "goal:g5.46 close (v3): MK RED (review's kill); the call is BY CONSTRUCTION only (v2 falsifier 1): not that MK's RED depends on W_z (R2: RED at every W_z scale incl. 0)",
     "text": "MK CV with z ZEROED in TRAINING ..., z ~ N(0, I) at sampling, scores <= 0.05 AND has <= 16 distinct valid per cue of 512 on every seed",
     "conj": [("score_le", site(at(F46, 108), at(F46, 159), at(F46, 109)), N, 1, 20), ("dist_le", site(at(F46, 108), at(F46, 159), at(F46, 109)), N_RICH, 16)]},
    {"id": "g546_MC", "round": "g5.46", "review": None, "text": "MC (plasma) the distinct counter on 512 true target lines per cue reads >= 150 on every seed, MIN over cues",
     "conj": [("dist_ge", site(at(F46, 179), at(F46, 179)), N_RICH, 150)]},
    {"id": "g546_M2", "round": "g5.46", "review": None, "text": "M2 the scorer arm as in g5.39", "conj": M2(F46, 173, 175)},
]
PLANTED = [   # Falsifier 3: each must read as stated, else VOID; planted, so no site: O_g = all histograms, stated
    {"id": "P_taut", "want": "vacuous", "text": "planted tautology: valid count >= 0", "conj": [("valid_ge", None, N, 0, 1)]},
    {"id": "P_strong", "want": "non_vacuous", "text": "planted strong gate: score <= 0.05 over ALL histograms", "conj": [("score_le", None, N, 1, 20)]},
]


# ---------- falsifier 5: O_g's class from the cited code, by rule ----------
RAND = re.compile(r"\brng\b|random|normal\(|integers\(")


def m_draws(draw, call):
    """m = distinct latent draws per cue on the cited path, read from the draw line and its call site:
    R1 `1 if <flag> else n`: 1 iff the call passes <flag>=True, else n;  R2 `% mod`: the call's mod=k, else n;
    R4 (read before R3) `size=(n..` or `make_lines(r, n..`: n;  R3 no random token on the draw line: 1, and only under
    a frozen=True / fixed=True call. No rule matches -> VOID (raised)."""
    f = re.search(r"\b1 if (\w+) else n\b", draw)
    if f:
        return 1 if f"{f[1]}=True" in call else "n"
    if "% mod" in draw:
        k = re.search(r"\bmod=(\d+)", call)
        return int(k[1]) if k else "n"
    if re.search(r"size=\(n\w*\b|make_lines\(r, n\w*\b", draw):
        return "n"
    if not RAND.search(draw):
        assert re.search(r"\b(frozen|fixed)=True", call), ("R3 needs a frozen / fixed call", draw, call)
        return 1
    raise AssertionError(("no rule matches: VOID", draw))


def deterministic(dec):
    """the decoder line thresholds at 0 and draws nothing; None = the instrument's samples ARE its draws."""
    return dec is None or ("> 0)" in dec and not RAND.search(dec))


def o_class(lines):
    """-> one_class | cap<k> | all: m = 1 on a deterministic path -> one image per cue -> ONE-CLASS histograms; m = k
    -> at most k distinct images; m = n or a random decoder -> all histograms of n."""
    m = m_draws(lines["draw"], lines["call"])
    if m == "n" or not deterministic(lines.get("dec")):
        return "all", m
    return ("one_class" if m == 1 else f"cap{m}"), m


def kind_of(reading, cls, n):
    if reading.startswith("dist"):
        return f"dist{min(int(cls[3:]) if cls.startswith('cap') else n, n)}" if cls != "one_class" else "dist1"
    return "one_class" if cls == "one_class" else "all"


def resolve(g, table):
    """the gate with each conjunct's O kind filled from the committed table (planted gates: all)."""
    out = []
    for i, (r, s, n, *th) in enumerate(g["conj"]):
        out.append((r, "all" if s is None and r[0] != "d" else kind_of(r, table[g["id"]][i]["class"], n), *th))
    return {**g, "conj": out}


# ---------- O_g ----------
def space(kind):
    if kind == "one_class":
        return sorted({(v, 0) for v in range(N + 1)} | {(0, v) for v in range(N + 1)}, reverse=True)
    if kind == "all":
        return [(a, v - a) for v in range(N, -1, -1) for a in range(v, -1, -1)]
    if kind.startswith("dist"):
        return list(range(int(kind[4:]) + 1))
    raise ValueError(kind)


# ---------- the Python reference (exact rationals; the same bounds the checker uses) ----------
hi = lambda o: Fr(0) if 0 in o else Fr(sum(o), N)
lo = lambda o: Fr(0) if sum(o) == 0 else Fr(2 * o[0] * o[1], N * sum(o))
vf = lambda o: Fr(sum(o), N)


def true_score(o):
    v = sum(o)
    return 0.0 if v == 0 else v / N * -sum(c / v * math.log2(c / v) for c in o if c)


def conj_ref(c):
    """-> (vacuous, a witness or None): vacuous iff the reading holds for EVERY per-seed outcome (pairs reduce to extremes)."""
    r, kind, *th = c
    O = space(kind)
    if r in ("score_le", "score_ge", "valid_le", "valid_ge"):
        t = Fr(th[0], th[1])
        holds = {"score_le": lambda o: hi(o) <= t, "score_ge": lambda o: lo(o) >= t, "valid_le": lambda o: vf(o) <= t, "valid_ge": lambda o: vf(o) >= t}[r]
        breaks = {"score_le": lambda o: lo(o) > t, "score_ge": lambda o: hi(o) < t, "valid_le": lambda o: vf(o) > t, "valid_ge": lambda o: vf(o) < t}[r]
        w = next((o for o in O if breaks(o)), None)   # the pair (o*, o*): its mean equals o*'s reading
        return all(holds(o) for o in O), (None if w is None else [w, w])
    k = th[0]
    holds, breaks = (lambda d: d <= k, lambda d: d > k) if r == "dist_le" else (lambda d: d >= k, lambda d: d < k)
    return all(holds(d) for d in O), next((d for d in O if breaks(d)), None)


def gate_ref(g):
    rs = [conj_ref(c) for c in g["conj"]]
    vac = all(v for v, _ in rs)
    wit = next(((i, w) for i, (_, w) in enumerate(rs) if w is not None), None)
    assert vac == (wit is None), g["id"]   # the bounds decide every gate here: no undecided reading
    return {"call": "vacuous" if vac else "non_vacuous", "witness": wit}


def candidate(g):
    """A vacuous gate's OPPOSITE: the claimed witness = O_g's outcome with the MOST valid samples (or the largest count)."""
    c = g["conj"][0]
    O = space(c[1])
    return [0, [max(O, key=sum)] * 2 if c[0].startswith(("score", "valid")) else max(O)]


# ---------- the literal + laws (Bend) ----------
ol = lambda O: "[" + ", ".join(f"A.O{{{a}, {b}}}" for a, b in O) + "]"
dl = lambda O: "[" + ", ".join(str(d) for d in O) + "]"


def lit(g, wit):
    out = ["import Base", "import ./A.bend as A", ""]
    for i, c in enumerate(g["conj"]):
        O = space(c[1])
        out += [f"def s{i}() -> +List<{'A.O' if c[0][0] != 'd' else 'U32'}>:", f"  {ol(O) if c[0][0] != 'd' else dl(O)}", ""]
    if wit is not None:
        i, w = wit
        if g["conj"][i][0][0] == "d":
            out += ["def w() -> U32:", f"  {w}", ""]
        else:
            out += ["def w0() -> A.O:", f"  A.O{{{w[0][0]}, {w[0][1]}}}", "", "def w1() -> A.O:", f"  A.O{{{w[1][0]}, {w[1][1]}}}", ""]
    return "\n".join(out)


def call(fn, i, c, wit=False):
    r, _, *th = c
    if r[0] == "d":
        return f"A.{fn}_{r}(D.s{i}(), {'D.w(), ' if wit else ''}{th[0]})"
    return f"A.{fn}_{r}(D.s{i}(), {'D.w0(), D.w1(), ' if wit else ''}{N}, {th[0]}, {th[1]})"


def law_text(g, form, wit):
    if form == "vac":
        e = " && ".join(call("vac", i, c) for i, c in enumerate(g["conj"]))
    elif form == "ex":
        e = " || ".join(call("ex", i, c) for i, c in enumerate(g["conj"]))
    else:
        e = call("wit", wit[0], g["conj"][wit[0]], True)
    return f"law {form}:\n  {{A.b2u({e}) == 1 : U32}}\n"


def law_files(g, form, wit=None):
    return {"A.bend": open(os.path.join(HERE, "bend2_vacuity.bend")).read(), "LIT.bend": lit(g, wit),
            "LAWS.bend": f"import Base\nimport ./A.bend as A\nimport ./LIT.bend as D\n\n# {g['id']}: {g.get('text', '')[:200]}\n" + law_text(g, form, wit),
            "PROOF.bend": f"import Base\nimport ./LAWS.bend as Laws\n\ndef Laws.{form}():\n  {{==}}\n"}


def law_sets(gs):
    """-> {name: (gate, form, witness, want, role)}: a vacuous call = vac CHECK + ex FAIL + the claimed witness FAIL;
    a non-vacuous call = the witness CHECK + ex CHECK + vac (the for-all) FAIL."""
    S = {}
    for g in gs:
        ref = gate_ref(g)
        role = "planted" if g["id"].startswith("P_") else "gate"
        if ref["call"] == "vacuous":
            cw = candidate(g)
            S[f"{g['id']}_vac"] = (g, "vac", None, "check", role)
            S[f"{g['id']}_ex_opp"] = (g, "ex", None, "fail", role)
            S[f"{g['id']}_wit_opp"] = (g, "wit", cw, "fail", role)
        else:
            S[f"{g['id']}_wit"] = (g, "wit", ref["witness"], "check", role)
            S[f"{g['id']}_ex"] = (g, "ex", None, "check", role)
            S[f"{g['id']}_vac_opp"] = (g, "vac", None, "fail", role)
    return S


# ---------- stages ----------
def out_dir():
    return paths.get_local("bend2_vacuity_dir")


def load_P():
    pp = os.path.join(out_dir(), "params.json")
    return json.load(open(pp)), L.sha(pp)


def line_at(c):
    s, f, l = c
    t = subprocess.run(["git", "-C", HERE, "show", f"{s}:{f}"], capture_output=True, text=True, check=True).stdout.splitlines()
    assert 1 <= l <= len(t) and t[l - 1].strip(), c
    return t[l - 1].strip()


def stage_rule():
    """o_table.json (falsifier 5), BEFORE any law: per gate and conjunct, the cited lines read at the round's pre-run
    (git show), m and O_g's class computed by o_class; plus the valid-pair line every histogram rests on."""
    out = {"valid_pair": {"cite": list(VALID), "text": line_at(VALID)}, "rule": m_draws.__doc__.strip() + " " + o_class.__doc__.strip()}
    for g in GATES:
        rows = []
        for r, s, n, *th in g["conj"]:
            lines = {k: (None if c is None else line_at(c)) for k, c in s.items()}
            cls, m = o_class(lines)
            rows.append({"reading": r, "n": n, "cites": {k: (None if c is None else list(c)) for k, c in s.items()}, "lines": lines,
                         "m": m, "class": cls, "kind": kind_of(r, cls, n)})
        out[g["id"]] = rows
    json.dump(out, open(os.path.join(out_dir(), "o_table.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps({g["id"]: [x["kind"] for x in out[g["id"]]] for g in GATES}))


def resolved():
    table = json.load(open(os.path.join(out_dir(), "o_table.json")))
    return [resolve(g, table) for g in GATES + PLANTED]


def stage_gen():
    o = out_dir()
    gs = resolved()
    files, sets = {}, {}
    for name, (g, form, wit, want, role) in sorted(law_sets(gs).items()):
        fs = law_files(g, form, wit)
        files[name] = L.write_dir(os.path.join(o, "laws", name), fs)
        sets[name] = {"gate": g["id"], "form": form, "want": want, "role": role, "witness": wit, "literal_bytes": len(fs["LIT.bend"].encode())}
    ref = {g["id"]: {**gate_ref(g), "review": g.get("review"), "conj": g["conj"]} for g in gs}
    json.dump({"o_table_sha256": L.sha(os.path.join(o, "o_table.json")), "files": files, "sets": sets, "python_ref": ref},
              open(os.path.join(o, "laws_files.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps({"n_sets": len(sets), "calls": {k: v["call"] for k, v in ref.items()}}))


def stage_check():
    P, psha = load_P()
    o = out_dir()
    F = json.load(open(os.path.join(o, "laws_files.json")))
    res = {}
    for k in sorted(F["sets"]):
        d = os.path.join(o, "laws", k)
        assert all(L.sha(os.path.join(d, f)) == h for f, h in F["files"][k].items()), k   # the committed bytes, unchanged
        r = L.run_bend(P, d, False)
        res[k] = {**{x: r[x] for x in ("status", "wall_s", "peak_rss_mib")}, "want": F["sets"][k]["want"], "tail": r["tail"][-4:]}
        if F["sets"][k]["want"] == "check":
            v = L.run_bend(P, d, True)
            res[k]["verdict"] = {x: v[x] for x in ("status", "wall_s", "peak_rss_mib")}
        print(k, r["status"], F["sets"][k]["want"], r["wall_s"], res[k].get("verdict", {}).get("status", ""), flush=True)
    json.dump({"params_sha256": psha, "sets": res}, open(os.path.join(o, "check.json"), "w"), indent=1, sort_keys=True)


def score(F, C, cap_s):
    """The falsifier, read mechanically (committed before the run)."""
    sets, res = F["sets"], C["sets"]
    st = lambda k: res[k]["status"]
    over = sorted(k for k, r in res.items() if r["status"] in ("rss_cap", "wall_cap") or r["wall_s"] > cap_s
                  or r.get("verdict", {}).get("status") in ("rss_cap", "wall_cap") or r.get("verdict", {}).get("wall_s", 0) > cap_s)
    errs = sorted(k for k, r in res.items() if r["status"] not in ("check", "fail", "rss_cap", "wall_cap"))
    kernel = {}
    for gid in sorted({s["gate"] for s in sets.values()}):
        mine = sorted(k for k, s in sets.items() if s["gate"] == gid)
        forms = {s["form"]: st(k) for k, s in sets.items() if s["gate"] == gid}
        call = ("vacuous" if forms.get("vac") == "check" and forms.get("ex") == "fail" and forms.get("wit") == "fail" else
                "non_vacuous" if forms.get("wit") == "check" and forms.get("ex") == "check" and forms.get("vac") == "fail" else "none")
        kernel[gid] = {"kernel": call, "python": F["python_ref"][gid]["call"], "review": F["python_ref"][gid]["review"], "sets": mine}
    honest_ok = all(st(k) == "check" and res[k].get("verdict", {}).get("status") == "check" for k, s in sets.items() if s["want"] == "check")
    opp_refused = all(st(k) == "fail" for k, s in sets.items() if s["want"] == "fail")
    reviewed = {g: v for g, v in kernel.items() if v["review"]}
    void = ([f"over the cap: {over}"] if over else []) + ([f"bend errors: {errs}"] if errs else [])
    planted = {"P_taut": kernel["P_taut"]["kernel"] == "vacuous", "P_strong": kernel["P_strong"]["kernel"] == "non_vacuous"}
    if not all(planted.values()):
        void.append(f"a planted mutant did not read as stated: {planted}")
    l1 = "proved" if all(v["kernel"] == v["review"] for v in reviewed.values()) and honest_ok else "disproved"
    return {"void": void, "line1": "void" if void else l1, "line2_counterproofs": "void" if void else ("proved" if opp_refused else "disproved"),
            "honest_all_check_and_verdict": honest_ok, "opposites_all_refused": opp_refused, "planted": planted,
            "kernel": kernel, "reviewed_agree": {g: v["kernel"] == v["review"] for g, v in reviewed.items()},
            "reported": {g: v["kernel"] for g, v in kernel.items() if not v["review"] and not g.startswith("P_")},
            "max_wall_s": max(r["wall_s"] for r in res.values()), "max_peak_rss_mib": max(r["peak_rss_mib"] for r in res.values())}


def stage_score():
    P, psha = load_P()
    o = out_dir()
    F, C = (json.load(open(os.path.join(o, f))) for f in ("laws_files.json", "check.json"))
    V = {"params_sha256": psha, "check_sha256": L.sha(os.path.join(o, "check.json")), **score(F, C, P["wall_cap_s"])}
    json.dump(V, open(os.path.join(o, "verdict.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps({k: V[k] for k in ("void", "line1", "line2_counterproofs", "reviewed_agree", "reported", "max_wall_s")}))


if __name__ == "__main__":
    {"rule": stage_rule, "gen": stage_gen, "check": stage_check, "score": stage_score}[sys.argv[1]]()
