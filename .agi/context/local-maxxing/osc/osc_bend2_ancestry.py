#!/usr/bin/env python3
"""BEND2 OVER THE GRAPH'S OWN STRUCTURE (goal:g5.47 v2, hypothesis:lm-bend2-kernel-certifies-ancestry-and-its-disproof):
STEP A the (results -> pre-run) and (pre-run -> pin) pairs of the closed rounds g5.35-g5.45, each with git's answer
(git merge-base --is-ancestor); STEP B the answer as a bend2 LAW over commit records (sha, parents, generation level =
1 + max over parents): a PROOF of "Y is an ancestor of X" is a parent path X -> ... -> Y whose every step is a listed
edge; a DISPROOF is R, X's record first, then the ancestors of X at level >= level(Y), every parent of every record
listed with its level, the kernel checking each parent is in R or below level(Y). The kernel certifies the reachability
LOGIC over the records, not their provenance: extract re-derives every record from git, and a reviewer re-runs it.
Stages (CLI): extract (git) | gen | check (bend only, no git) | score. g5.42's module (osc_bend2_law) is IMPORTED, never
edited: run_bend (the RSS watchdog), write_dir, sha."""
import collections, hashlib, json, os, statistics, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_bend2_law as L  # noqa: E402
import paths  # noqa: E402

# STEP A, fixed before any law: (key, round, kind, X, Y). A pin is the leaf commit the round's own pre-run bytes name
# (or the leaf's frozen residues name); a round whose pre-run names none contributes its (results -> pre-run) pair only.
PAIRS = [
    ("g535r1_res", "g5.35 r1", "results->pre-run", "c07ed3c864", "7e781e240b"),
    ("g535r1_pin", "g5.35 r1", "pre-run->pin", "7e781e240b", "33b3e4f121"),
    ("g535r2_res", "g5.35 r2", "results->pre-run", "124fd6c51b", "09f2e322f0"),
    ("g536_res", "g5.36", "results->pre-run", "f157dedb99", "f533da2a1a"),
    ("g537_res", "g5.37", "results->pre-run", "330d9986c3", "20bbea41bb"),
    ("g538_res", "g5.38", "results->pre-run", "29798337de", "3b499a36bc"),
    ("g538_pin", "g5.38", "pre-run->pin", "3b499a36bc", "e952001d88"),
    ("g539_res", "g5.39", "results->pre-run", "0cf9035b09", "7b75964aea"),
    ("g539_pin", "g5.39", "pre-run->pin", "7b75964aea", "e952001d88"),
    ("g540r1_res", "g5.40 r1", "results->pre-run", "fd73e53e3a", "5d09e9bf0a"),
    ("g540r1_pin", "g5.40 r1", "pre-run->pin", "5d09e9bf0a", "7387e6afd3"),
    ("g540r2_res", "g5.40 r2", "results->pre-run", "df6ddf4d06", "14ebc9ffe5"),
    ("g541_res", "g5.41", "results->pre-run", "d48b32691e", "cee90e7bff"),
    ("g541_pin", "g5.41", "pre-run->pin", "cee90e7bff", "86567311db"),
    ("g542_res", "g5.42", "results->pre-run", "a87b8558c0", "3721c042a5"),
    ("g542_pin", "g5.42", "pre-run->pin", "3721c042a5", "86567311db"),
    ("g543_res", "g5.43", "results->pre-run", "d04861ed6f", "f93be0f7b3"),
    ("g543_pin", "g5.43", "pre-run->pin", "f93be0f7b3", "1dc81b4f4b"),
    ("g544_res", "g5.44", "results->pre-run", "e4ac31e618", "f19f305fba"),
    ("g544_pin", "g5.44", "pre-run->pin", "f19f305fba", "1dc81b4f4b"),
    ("g545_res", "g5.45", "results->pre-run", "5f583c27be", "8bb44eae2f"),
    ("g545_pin", "g5.45", "pre-run->pin", "8bb44eae2f", "9f5a760cfe"),
]
RESIDUES = {("e952001d88", "3b499a36bc"), ("e952001d88", "7b75964aea"), ("86567311db", "cee90e7bff")}   # (pin, pre-run), frozen by the leaf


def git(*a):
    return subprocess.run(["git", "-C", HERE] + list(a), capture_output=True, text=True, check=True).stdout


def is_ancestor(y, x):
    return subprocess.run(["git", "-C", HERE, "merge-base", "--is-ancestor", y, x]).returncode == 0


# ---------- the prover side (Python): levels, closures, paths ----------
def levels(par):
    """par: {sha: [parent shas]} closed under parents. -> {sha: 1 + max over parents (0 for none)}, iteratively."""
    lev = {}
    for c0 in par:
        st = [c0]
        while st:
            c = st[-1]
            if c in lev:
                st.pop()
                continue
            todo = [p for p in par[c] if p not in lev]
            if todo:
                st += todo
            else:
                lev[c] = 1 + max((lev[p] for p in par[c]), default=0)
                st.pop()
    return lev


def closure(par, lev, x, y):
    """R: X first, then every ancestor of X at level >= level(Y), in BFS order over git's parent order."""
    R, seen, q = [x], {x}, collections.deque([x])
    while q:
        for p in par[q.popleft()]:
            if p not in seen and lev[p] >= lev[y]:
                seen.add(p), R.append(p), q.append(p)
    return R


def shortest_path(par, lev, x, y):
    """A shortest parent path X -> ... -> Y (BFS, git's parent order breaks ties), or None."""
    prev, q = {x: None}, collections.deque([x])
    while q:
        c = q.popleft()
        if c == y:
            out = [c]
            while prev[out[-1]] is not None:
                out.append(prev[out[-1]])
            return out[::-1]
        for p in par[c]:
            if p not in prev and lev[p] >= lev[y]:
                prev[p] = c
                q.append(p)
    return None


def offered_path(par, lev, x, y):
    """The OPPOSITE proof of a non-ancestor pair: the first-parent chain from X while its level exceeds level(Y),
    then Y appended (the last step is the claim the kernel must refuse)."""
    out = [x]
    while lev[out[-1]] > lev[y] and par[out[-1]]:
        out.append(par[out[-1]][0])
    return out + [y]


# ---------- the literal (Bend) ----------
def words(s):   # a sha1 as 5 big-endian U32 words
    assert len(s) == 40
    return "[" + ", ".join(str(int(s[i:i + 8], 16)) for i in range(0, 40, 8)) + "]"


def lit_proof(x, y, path, edges):
    return "\n".join(["import Base", "import ./A.bend as A", "", f"def x() -> +List<U32>:\n  {words(x)}\n", f"def y() -> +List<U32>:\n  {words(y)}\n",
                      "def path() -> +List<+List<U32>>:\n  [" + ", ".join(words(c) for c in path) + "]\n",
                      "def edges() -> +List<A.Edge>:\n  [" + ", ".join(f"A.Edge{{{words(c)}, {words(p)}}}" for c, p in edges) + "]\n"])


def lit_disproof(x, y, ylev, recs):
    """recs: [(sha, level, [(parent sha, parent level), ...])] -- ALL parents of each record, each with its level."""
    rs = ", ".join(f"A.Rec{{{words(c)}, {lv}, [" + ", ".join(f"A.Par{{{words(p)}, {pl}}}" for p, pl in ps) + "]}" for c, lv, ps in recs)
    return "\n".join(["import Base", "import ./A.bend as A", "", f"def x() -> +List<U32>:\n  {words(x)}\n", f"def y() -> +List<U32>:\n  {words(y)}\n",
                      f"def ylev() -> U32:\n  {ylev}\n", f"def recs() -> +List<A.Rec>:\n  [{rs}]\n"])


LAW = {"proof": "law ancestor:\n  {A.b2u(A.proof_ok(D.x(), D.y(), D.path(), D.edges())) == 1 : U32}\n",
       "disproof": "law not_ancestor:\n  {A.b2u(A.disproof_ok(D.x(), D.y(), D.ylev(), D.recs())) == 1 : U32}\n"}


def law_files(kind, lit):
    name = "ancestor" if kind == "proof" else "not_ancestor"
    return {"A.bend": open(os.path.join(HERE, "bend2_ancestry.bend")).read(), "LIT.bend": lit,
            "LAWS.bend": "import Base\nimport ./A.bend as A\nimport ./LIT.bend as D\n\n" + LAW[kind],
            "PROOF.bend": f"import Base\nimport ./LAWS.bend as Laws\n\ndef Laws.{name}():\n  {{==}}\n"}


# ---------- stages ----------
def out_dir():
    return paths.get_local("bend2_ancestry_dir")


def load_P():
    pp = os.path.join(out_dir(), "params.json")
    return json.load(open(pp)), L.sha(pp)


def stage_extract():
    """records.json: STEP A (git's answer per pair), every record a certificate reads (sha, level, ALL parents with
    levels), and the prover's certificates (path, R, offered path); python reachability cross-checked against git."""
    full = {s: git("rev-parse", s).strip() for p in PAIRS for s in p[3:]}
    par = {}
    for ln in git("rev-list", "--parents", *sorted(set(full.values()))).splitlines():
        c, *ps = ln.split()
        par[c] = ps
    lev = levels(par)
    pairs, need = [], set()
    for key, rnd, kind, x, y in PAIRS:
        X, Y = full[x], full[y]
        anc = is_ancestor(Y, X)
        R, path = closure(par, lev, X, Y), shortest_path(par, lev, X, Y)
        assert (path is not None) == anc == (Y in R), (key, anc)   # VOID otherwise: the extraction disagrees with git
        assert ((y, x) in RESIDUES) == (not anc), key              # the leaf's frozen residues, and only those
        off = None if anc else offered_path(par, lev, X, Y)
        need |= set(R) | set(path or []) | set(off or []) | {X, Y}
        pairs.append({"key": key, "round": rnd, "kind": kind, "x": X, "y": Y, "git_ancestor": anc, "level_x": lev[X], "level_y": lev[Y],
                      "R": R, "path": path, "offered_path": off})
    recs = {c: {"level": lev[c], "parents": [[p, lev[p]] for p in par[c]]} for c in sorted(need)}
    R = {"n_pairs": len(pairs), "n_ancestor": sum(p["git_ancestor"] for p in pairs), "n_commits_walked": len(par), "pairs": pairs, "records": recs}
    fp = os.path.join(out_dir(), "records.json")
    json.dump(R, open(fp, "w"), indent=1, sort_keys=True)
    print(json.dumps({"records_sha256": L.sha(fp), "n_pairs": R["n_pairs"], "n_ancestor": R["n_ancestor"], "n_commits_walked": len(par)}))


def rec(R, c):
    r = R["records"][c]
    return (c, r["level"], [tuple(p) for p in r["parents"]])


def law_sets(R):
    """-> {name: (kind, literal, want, role, pair key)}; role in honest | opposite | Me1a | Me1b | Me2 | Me3 | Me4 |
    reported (P_omit: a record with a parent DROPPED is provenance, which the kernel does not certify)."""
    S, ps = {}, R["pairs"]
    for i, p in enumerate(ps):
        k, x, y, ylev = p["key"], p["x"], p["y"], p["level_y"]
        recs = [rec(R, c) for c in p["R"]]
        if p["git_ancestor"]:
            path = p["path"]
            es = list(zip(path, path[1:]))
            u = next(c for q in ps[i + 1:] + ps[:i] for c in (q["x"], q["y"]) if c not in path)   # the swap: the next pair's X (else Y) off this path
            S[f"{k}_proof"] = ("proof", lit_proof(x, y, path, es), "check", "honest", k)
            S[f"{k}_disproof_opp"] = ("disproof", lit_disproof(x, y, ylev, recs), "fail", "opposite", k)
            S[f"{k}_Me1a"] = ("proof", lit_proof(x, y, path, es[1:]), "fail", "Me1a", k)
            S[f"{k}_Me1b"] = ("proof", lit_proof(x, y, path, [(es[0][0], u)] + es[1:]), "fail", "Me1b", k)
            S[f"{k}_Me4"] = ("disproof", lit_disproof(x, y, ylev, [r for r in recs if r[0] != y]), "fail", "Me4", k)
            om = [(c, lv, [q for q in pp if q[0] != y]) for c, lv, pp in recs if c != y]
            S[f"{k}_P_omit"] = ("disproof", lit_disproof(x, y, ylev, om), "reported", "reported", k)
        else:
            off = p["offered_path"]
            S[f"{k}_disproof"] = ("disproof", lit_disproof(x, y, ylev, recs), "check", "honest", k)
            S[f"{k}_proof_opp"] = ("proof", lit_proof(x, y, off, list(zip(off, off[1:]))[:-1]), "fail", "opposite", k)
            last = recs[-1]
            S[f"{k}_Me2"] = ("disproof", lit_disproof(x, y, ylev, recs[:-1] + [(last[0], last[1], last[2] + [(y, ylev)])]), "fail", "Me2", k)
            S[f"{k}_Me3"] = ("disproof", lit_disproof(x, y, ylev, recs + [rec(R, y)]), "fail", "Me3", k)
            S[f"{k}_Me4"] = ("disproof", lit_disproof(x, y, ylev, recs[1:]), "fail", "Me4", k)
    return S


def stage_gen():
    o = out_dir()
    R = json.load(open(os.path.join(o, "records.json")))
    files, sets = {}, {}
    for name, (kind, lit, want, role, key) in sorted(law_sets(R).items()):
        files[name] = L.write_dir(os.path.join(o, "laws", name), law_files(kind, lit))
        sets[name] = {"kind": kind, "want": want, "role": role, "pair": key, "literal_bytes": len(lit.encode())}
    json.dump({"records_sha256": L.sha(os.path.join(o, "records.json")), "files": files, "sets": sets}, open(os.path.join(o, "laws_files.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps({"n_sets": len(sets), "by_role": dict(collections.Counter(s["role"] for s in sets.values()))}))


def stage_check():
    """bend --check-only on every set (no git, no network: each dir is self-contained); --verdict on the honest sets."""
    P, psha = load_P()
    o = out_dir()
    F = json.load(open(os.path.join(o, "laws_files.json")))
    res = {}
    for k in sorted(F["sets"]):
        s, d = F["sets"][k], os.path.join(o, "laws", k)
        assert all(L.sha(os.path.join(d, f)) == h for f, h in F["files"][k].items()), k   # the committed bytes, unchanged
        r = L.run_bend(P, d, False)
        res[k] = {**{x: r[x] for x in ("status", "wall_s", "peak_rss_mib")}, "want": s["want"], "tail": r["tail"][-4:]}
        if s["role"] == "honest":
            v = L.run_bend(P, d, True)
            res[k]["verdict"] = {x: v[x] for x in ("status", "wall_s", "peak_rss_mib")}
        print(k, r["status"], s["want"], r["wall_s"], res[k].get("verdict", {}).get("status", ""), flush=True)
    json.dump({"params_sha256": psha, "sets": res}, open(os.path.join(o, "check.json"), "w"), indent=1, sort_keys=True)


def score(F, C, R, cap_s):
    """The falsifier, read mechanically (committed before the run). -> verdict dict."""
    sets, res = F["sets"], C["sets"]
    over = sorted(k for k, r in res.items() if r["status"] in ("rss_cap", "wall_cap") or r["wall_s"] > cap_s
                  or r.get("verdict", {}).get("status") in ("rss_cap", "wall_cap") or r.get("verdict", {}).get("wall_s", 0) > cap_s)
    errs = sorted(k for k, r in res.items() if r["status"] not in ("check", "fail", "rss_cap", "wall_cap"))
    by = lambda role: {k: s for k, s in sets.items() if s["role"] == role}
    kernel = {}
    for p in R["pairs"]:
        pr = next(k for k, s in sets.items() if s["pair"] == p["key"] and s["kind"] == "proof" and s["role"] in ("honest", "opposite"))
        dp = next(k for k, s in sets.items() if s["pair"] == p["key"] and s["kind"] == "disproof" and s["role"] in ("honest", "opposite"))
        a, n = res[pr]["status"] == "check", res[dp]["status"] == "check"
        kernel[p["key"]] = {"git_ancestor": p["git_ancestor"], "kernel": "ancestor" if a and not n else "not_ancestor" if n and not a else "none",
                            "agrees": (a and not n) if p["git_ancestor"] else (n and not a)}
    honest_ok = all(res[k]["status"] == "check" and res[k].get("verdict", {}).get("status") == "check" for k in by("honest"))
    opp_refused = all(res[k]["status"] == "fail" for k in by("opposite"))
    muts = {k: res[k]["status"] for role in ("Me1a", "Me1b", "Me2", "Me3", "Me4") for k in by(role)}
    hp = [s["literal_bytes"] for s in by("honest").values() if s["kind"] == "proof"]
    hd = [s["literal_bytes"] for s in by("honest").values() if s["kind"] == "disproof"]
    mp, md = statistics.median(hp), statistics.median(hd)
    void = []
    if over:
        void.append(f"over the cap: {over}")
    if errs:
        void.append(f"bend errors: {errs}")
    if any(v != "fail" for v in muts.values()):
        void.append(f"a mutant did not FAIL: {sorted(k for k, v in muts.items() if v != 'fail')}")
    l1 = "proved" if honest_ok and opp_refused and all(v["agrees"] for v in kernel.values()) else "disproved"
    return {"void": void, "line1": "void" if void else l1, "line2_L_ASYM": "void" if void else ("proved" if md >= 10 * mp else "disproved"),
            "honest_all_check_and_verdict": honest_ok, "opposites_all_refused": opp_refused, "kernel_vs_git": kernel,
            "mutants": muts, "median_proof_literal_bytes": mp, "median_disproof_literal_bytes": md, "ratio": round(md / mp, 3),
            "proof_literal_bytes": sorted(hp), "disproof_literal_bytes": sorted(hd),
            "reported_P_omit": {k: res[k]["status"] for k in by("reported")},
            "time_reported": {"honest_proof_wall_s": sorted(res[k]["wall_s"] for k, s in by("honest").items() if s["kind"] == "proof"),
                              "honest_disproof_wall_s": sorted(res[k]["wall_s"] for k, s in by("honest").items() if s["kind"] == "disproof")},
            "max_wall_s": max(r["wall_s"] for r in res.values()), "max_peak_rss_mib": max(r["peak_rss_mib"] for r in res.values())}


def stage_score():
    P, psha = load_P()
    o = out_dir()
    F, C, R = (json.load(open(os.path.join(o, f))) for f in ("laws_files.json", "check.json", "records.json"))
    V = {"params_sha256": psha, "check_sha256": L.sha(os.path.join(o, "check.json")), **score(F, C, R, P["wall_cap_s"])}
    json.dump(V, open(os.path.join(o, "verdict.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps({k: V[k] for k in ("void", "line1", "line2_L_ASYM", "ratio", "max_wall_s", "max_peak_rss_mib")}))


if __name__ == "__main__":
    {"extract": stage_extract, "gen": stage_gen, "check": stage_check, "score": stage_score}[sys.argv[1]]()
