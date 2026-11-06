#!/usr/bin/env python3
"""BEND2 OVER GRAPH CLAIMS (goal:g5.45 v2, hypothesis:lm-bend2-kernel-checks-round-verdicts-over-their-committed-counts):
STEP P a REPORTED profile of g5.42's per-pair cost (T_full / T_lit / T_slice on the first 3 tape pairs, max of 3 repeats, the
projected fallback wall) + how bend2 represents integers; STEP A the census of integer-exact falsifier lines; STEP B two
equal-shape clause pairs (g5.35 r2 PROVED, g5.41 DISPROVED) as LAWs over literals of only the counts each clause reads;
STEP C every integer-exact line as a verdict LAW, each counter-proof failing; mutants MB (per clause) and MC.

Integer-exact (STEP A's rule, fixed before any law): a line's committed verdict is the SAME for every truth value of its
non-integer clauses. Its integer clauses read committed JSON integers (or null with the meaning the line's own text gives
it); its non-integer clauses (a float, a mean, a band, a p-value, a string, node prose) enter as universally quantified
Bools (`for r: Bool` in the LAW), so the kernel proves the verdict holds whatever they are. A line with no integer clause
that decides it is listed, never approximated. Counts come from extract (git show at PINNED commits; every source sha256
and the counts' sha256 in the pre-run). g5.42's module (osc_bend2_law) is IMPORTED, never edited."""
import hashlib, itertools, json, os, subprocess, sys
from fractions import Fraction
from math import comb

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path[:0] = [HERE, os.path.dirname(HERE)]
import osc_bend2_law as L  # noqa: E402  g5.42: run_bend (the RSS watchdog), law_file, proof_file, write_dir, sha, hit, logits, lit
import paths  # noqa: E402

VERDICT = {"disproved": 0, "proved": 1, "void": 2}
CMP = {"le": "U32.is_le", "lt": "U32.is_lt", "ge": "U32.is_ge", "gt": "U32.is_gt", "eq": "U32.is_eq"}


# ---------- the verdict DSL: one tree, evaluated by Python and printed as Bend ----------
def ev(e, env):
    op, *a = e if isinstance(e, tuple) else ("lit", e)
    if op == "lit":
        return a[0]
    if op in ("var", "free"):
        return env[a[0]]
    x = [ev(t, env) for t in a]
    return {"le": lambda: x[0] <= x[1], "lt": lambda: x[0] < x[1], "ge": lambda: x[0] >= x[1], "gt": lambda: x[0] > x[1],
            "eq": lambda: x[0] == x[1], "and": lambda: all(x), "or": lambda: any(x), "not": lambda: not x[0],
            "mul": lambda: x[0] * x[1], "add": lambda: x[0] + x[1]}[op]()


def bend(e):
    op, *a = e if isinstance(e, tuple) else ("lit", e)
    if op == "lit":
        assert isinstance(a[0], int) and not isinstance(a[0], bool) and 0 <= a[0] < 2 ** 31, a[0]
        return str(a[0])
    if op == "var":
        return f"V.{a[0]}()"
    if op == "free":
        return a[0]
    s = [bend(t) for t in a]
    if op in CMP:
        return f"{CMP[op]}({s[0]}, {s[1]})"
    if op in ("and", "or"):
        return "(" + (" && " if op == "and" else " || ").join(s) + ")"
    if op == "not":
        return f"Bool.not({s[0]})"
    return f"({s[0]} {'*' if op == 'mul' else '+'} {s[1]} : U32)"


def walk(e, op):
    if not isinstance(e, tuple):
        return []
    return ([e[1]] if e[0] == op else []) + [x for t in e[1:] for x in walk(t, op)]


def frees(ln):
    return sorted(set(walk(ln["proved"], "free") + walk(ln.get("void"), "free")))


def n_cmp(e):
    return 0 if not isinstance(e, tuple) else int(e[0] in CMP) + sum(n_cmp(t) for t in e[1:])


def verdict_one(ln, env):   # the void gate first, then the proved predicate
    if ln.get("void") is not None and ev(ln["void"], env):
        return "void"
    return "proved" if ev(ln["proved"], env) else "disproved"


def verdicts_all(ln, env):   # the verdict over every truth value of the non-integer (free) clauses
    fs = frees(ln)
    return {verdict_one(ln, {**env, **dict(zip(fs, bits))}) for bits in itertools.product([True, False], repeat=len(fs))}


def verdict_bend(ln):
    v = bend(ln["void"]) if ln.get("void") is not None else "False{}"
    return f"G.code({v}, {bend(ln['proved'])})"


GRAPH_BEND = """import Base

# verdict codes: 0 disproved, 1 proved, 2 void (the void gate is read first)
def code(void: Bool, proved: Bool) -> U32:
  match void:
    case True{}:
      2
    case False{}:
      match proved:
        case True{}:
          1
        case False{}:
          0
"""


def files_for(lines, values, claim):
    """VALUES.bend (one def per committed count the laws read), G.bend, LAWS.bend (one law per line: kernel verdict ==
    claim, every free clause quantified), PROOF.bend (a case split over the free Bools, {==} in each case)."""
    used = sorted({v for ln in lines for v in walk(ln["proved"], "var") + walk(ln.get("void"), "var")})
    vals = "\n".join(["import Base", ""] + [f"def {k}() -> U32:\n  {int(values[k])}\n" for k in used])
    laws, proofs = ["import Base", "import ./G.bend as G", "import ./VALUES.bend as V", ""], ["import Base", "import ./LAWS.bend as Laws", ""]
    for ln in lines:
        fs = frees(ln)
        laws += [f"# {ln['goal']} line {ln['line']}: {ln['cite'][:200]}", f"law {ln['id']}:"] + [f"  for {f}: Bool" for f in fs]
        laws += [f"  {{{verdict_bend(ln)} == {VERDICT[claim[ln['id']]]} : U32}}", ""]
        if fs:
            cases = "".join(f"    case {' '.join('True{}' if b else 'False{}' for b in bits)}:\n      {{==}}\n" for bits in itertools.product([True, False], repeat=len(fs)))
            proofs.append(f"def Laws.{ln['id']}({', '.join(fs)}):\n  match {' '.join(fs)}:\n{cases}")
        else:
            proofs.append(f"def Laws.{ln['id']}():\n  {{==}}\n")
    return {"G.bend": GRAPH_BEND, "VALUES.bend": vals, "LAWS.bend": "\n".join(laws), "PROOF.bend": "\n".join(proofs)}


# ---------- STEP A: the census spec (authored; the cite is pulled verbatim from the goal node) ----------
V, FR = (lambda n: ("var", n)), (lambda n: ("free", n))
S35, P35 = ("124fd6c51bd4e3e121e90cb6c666e852f3b060bd", ".agi/context/local-maxxing/rv/results.json"), ("09f2e322f0", ".agi/context/local-maxxing/rv/prereg.json")
S36 = ("f157dedb99", "datasets/osc-band/2026-11-05-neuron-period-cut/results.json")
S38 = ("29798337de", "datasets/osc-band/2026-11-05-neuron-period-phase/results.json")
S40 = ("df6ddf4d06ddbb28448ef90314680d78aaddaf42", ".agi/context/local-maxxing/mutscore/results_r2.json")
S41_0 = ("cee90e7bff7816b994470a8f5c029455baf31747", "datasets/plasma/2026-11-05-g5.41-blend-race/step0.json")
S41 = ("d48b32691e7f6c337c3bfab673cab7e9d401baab", "datasets/plasma/2026-11-05-g5.41-blend-race/results.json")
S41V = ("d48b32691e7f6c337c3bfab673cab7e9d401baab", "datasets/plasma/2026-11-05-g5.41-blend-race/verdict.json")
S42 = ("a87b8558c0", "datasets/osc-band/2026-11-05-bend2-law/reference.json")
seeds5 = lambda k: [f"seeds.{i}.{k}" for i in range(5)]

READS = {   # name: (source, how, keys)
    "g535_null_hits": (S35, "int", ["arms.F1_null.hits"]), "g535_salt_hits": (S35, "int", ["arms.F2_salt_planted.hits"]),
    "g535_band": (S35, "int", ["arms.F2_salt_planted.band_hits_lt"]),
    "g536_nf_reached": (S36, "notnull", ["N_f"]), "g536_nf": (S36, "int_or0", ["N_f"]), "g536_nr": (S36, "int", ["N_r"]),
    "g538_nb_reached": (S38, "notnull", ["N_b"]), "g538_nb": (S38, "int_or0", ["N_b"]), "g538_nr": (S38, "int", ["N_r"]),
    "g538_nc_reached": (S38, "notnull", ["N_c"]), "g538_nc": (S38, "int_or0", ["N_c"]), "g538_nw_hits": (S38, "len", ["N_w_hits"]),
    "g540_survived": (S40, "int", ["H_F1_all.survived"]), "g540_not_runnable": (S40, "int", ["not_runnable"]), "g540_items": (S40, "int", ["H_F1_all.items"]),
    "g541_blend0": (S41_0, "sum", seeds5("blend")), "g541_invalid0": (S41_0, "int", ["invalid"]),
    "g541_s_valid": (S41, "sum_diff", seeds5("S.test.n") + seeds5("S.test.invalid")), "g541_s_total": (S41, "sum", seeds5("S.test.n")),
    "g541_gc_valid": (S41, "sum_diff", seeds5("GC.4\\.0.test.n") + seeds5("GC.4\\.0.test.invalid")), "g541_gc_total": (S41, "sum", seeds5("GC.4\\.0.test.n")),
    "g542_x_all": (S42, "int", ["X_all"]), "g542_x_test": (S42, "int", ["X_test"]), "g542_n_test": (S42, "int", ["n_test"]),
}

NOT_INT = lambda gid, ln, why: {"id": f"{gid.replace('.', '')}_l{ln}", "goal": f"goal:{gid}", "line": ln, "reason": why}
LINES = [
    {**NOT_INT("g5.35", "1", "PROVED needs the conjunct 'the harness's own test passes', recorded only in node prose: not decided by integers"),
     "committed": "proved", "committed_src": [S35, "verdict"], "proved": ("and", FR("r_harness_test_passes"), ("lt", V("g535_null_hits"), V("g535_band")))},
    {"id": "g535_l2", "goal": "goal:g5.35", "line": "2", "kind": "gate", "committed": "proved", "committed_src": [S35, "arms.F2_salt_planted.as_required"],
     "note": "a mutant gate: reads as required (above the band) -> proved; inside the band -> void",
     "proved": ("ge", V("g535_salt_hits"), V("g535_band")), "void": ("lt", V("g535_salt_hits"), V("g535_band"))},
    NOT_INT("g5.35", "3", "a rule for later rounds; no verdict is committed for this round"),
    {"id": "g536_l1", "goal": "goal:g5.36", "line": "1", "kind": "claim", "committed": "disproved", "committed_src": [S36, "verdict"],
     "note": "N_f null = its own text's 'none -> N_f > 64': nf_reached 0, so the clause N_f <= 64 is false",
     "proved": ("and", ("eq", V("g536_nf_reached"), 1), ("le", V("g536_nf"), 64), ("ge", V("g536_nr"), ("mul", 2, V("g536_nf"))))},
    NOT_INT("g5.36", "2", "reads the twin's held-out accuracy (a float, mutant_max)"),
    NOT_INT("g5.37", "1", "reads float gains and max-min bands over seeds"), NOT_INT("g5.37", "2", "reads a float gain within a float band"),
    NOT_INT("g5.37", "3", "reads float accuracies (<= 0.35)"),
    {"id": "g538_l1", "goal": "goal:g5.38", "line": "1", "kind": "claim", "committed": "disproved", "committed_src": [S38, "H1"],
     "note": "N_b null = the pin's N_b := '>32': nb_reached 0",
     "proved": ("and", ("eq", V("g538_nb_reached"), 1), ("le", V("g538_nb"), 32), ("ge", V("g538_nr"), ("mul", 2, V("g538_nb"))))},
    {"id": "g538_l2", "goal": "goal:g5.38", "line": "2", "kind": "claim", "committed": "disproved", "committed_src": [S38, "H2"],
     "note": "H2 is stated as a RED rule: RED -> disproved, not RED -> proved, 'no verdict' (neither reaches) -> void",
     "void": ("and", ("eq", V("g538_nb_reached"), 0), ("eq", V("g538_nc_reached"), 0)),
     "proved": ("not", ("and", ("eq", V("g538_nc_reached"), 1), ("or", ("eq", V("g538_nb_reached"), 0), ("lt", V("g538_nc"), V("g538_nb")))))},
    {"id": "g538_l3", "goal": "goal:g5.38", "line": "3", "kind": "claim", "committed": "disproved", "committed_src": [S38, "H3"],
     "note": "PROVED iff some N_w <= 32 qualifies: the committed N_w_hits list is non-empty",
     "proved": ("ge", V("g538_nw_hits"), 1)},
    NOT_INT("g5.38", "4", "the mutant gates M1-M4 read held-out accuracies and kept fractions (floats)"),
    NOT_INT("g5.38", "5", "reported, no claim"),
    NOT_INT("g5.39", "1", "(1) reads float deltas and their mean; (2) the valid fraction is committed only as floats (k/64 per cue), no integer key"),
    NOT_INT("g5.39", "2", "the mutants read float scores and valid fractions"), NOT_INT("g5.39", "3", "withdrawn before mint"),
    {"id": "g540_l1", "goal": "goal:g5.40", "line": "1", "kind": "claim", "committed": "proved", "committed_src": [S40, "H_F1_all.verdict"],
     "proved": ("ge", V("g540_survived"), 2)},
    NOT_INT("g5.40", "2", "round 2 commits H-F2's n only inside a text void reason, never as an integer key"),
    NOT_INT("g5.40", "2b", "a definition of n, no verdict"),
    {"id": "g540_l3", "goal": "goal:g5.40", "line": "3", "kind": "gate", "committed": "proved", "committed_src": [S40, "H_F1_all.void_reasons"],
     "note": "a VOID rule: not void -> proved (the gate holds); n = the qualifying items with a mutant that ran (line 2b) = H_F1_all.items",
     "void": ("or", ("gt", V("g540_not_runnable"), 5), ("lt", V("g540_items"), 10)),
     "proved": ("not", ("or", ("gt", V("g540_not_runnable"), 5), ("lt", V("g540_items"), 10)))},
    NOT_INT("g5.40", "4", "the instrument mutants are scored as outcome strings (survived / killed)"),
    {"id": "g541_l1", "goal": "goal:g5.41", "line": "1", "kind": "claim", "committed": "disproved", "committed_src": [S41V, "S-OUT"],
     "proved": ("and", ("ge", ("mul", 2, V("g541_s_valid")), V("g541_s_total")), FR("r_s_minus_g_5of5_mean")),
     "note": "valid fraction >= 0.5  <=>  2 x valid >= total (exact); the score-delta clause (floats) is quantified"},
    {"id": "g541_l2", "goal": "goal:g5.41", "line": "2", "kind": "claim", "committed": "disproved", "committed_src": [S41V, "S-MECH"],
     "proved": ("and", ("ge", ("mul", 2, V("g541_blend0")), V("g541_invalid0")), FR("r_step1_s_below_g_5of5")),
     "note": "step 0's BLEND share >= 50%  <=>  2 x blend >= invalid; step 1's per-seed share comparison (floats) is quantified"},
    {"id": "g541_l3", "goal": "goal:g5.41", "line": "3", "kind": "claim", "committed": "disproved", "committed_src": [S41V, "G-CHAMFER"],
     "proved": ("and", ("ge", ("mul", 2, V("g541_gc_valid")), V("g541_gc_total")), FR("r_coverage_ge_0_9"), FR("r_gc_minus_g_5of5_mean")),
     "note": "valid >= 0.5  <=>  2 x valid >= total; coverage and the score delta (floats) are quantified"},
    NOT_INT("g5.41", "4", "the mutants read float scores (<= 0.05) and float scorer fractions"),
    NOT_INT("g5.42", "1", "reads check statuses and wall seconds"),
    {"id": "g542_l2", "goal": "goal:g5.42", "line": "2", "kind": "claim", "committed": "proved", "committed_src": ["experiment:dt1-bend2-law-1105", "readout: NOT RED"],
     "note": "a RED rule: not RED -> proved; X_test / 8939 < 0.99  <=>  100 x X_test < 99 x n_test (exact)",
     "proved": ("and", ("ge", V("g542_x_all"), 12642), ("ge", ("mul", 100, V("g542_x_test")), ("mul", 99, V("g542_n_test"))))},
    NOT_INT("g5.42", "3", "the counter-proofs were not reached: no verdict"),
    NOT_INT("g5.42", "4", "reads check statuses, RSS and wall seconds"),
]
EXCLUDED = [{"goal": "goal:g5.43", "reason": "goal status active: not a closed round (its results landed 12:41Z, during this leaf)"}]

STEP_B = {   # the leaf's named clauses, ONE law each, the same shape in both pairs
    "proved_pair_g535_r2": [
        {"id": "b_g535_f1_null", "goal": "goal:g5.35", "line": "1", "committed": "proved", "proved": ("lt", V("g535_null_hits"), V("g535_band"))},
        {"id": "b_g535_f2_salt", "goal": "goal:g5.35", "line": "2", "committed": "proved", "proved": ("ge", V("g535_salt_hits"), V("g535_band"))}],
    "disproved_pair_g541": [
        {"id": "b_g541_smech", "goal": "goal:g5.41", "line": "2", "committed": "disproved", "proved": ("ge", ("mul", 2, V("g541_blend0")), V("g541_invalid0"))},
        {"id": "b_g541_sout", "goal": "goal:g5.41", "line": "1", "committed": "disproved", "proved": ("ge", ("mul", 2, V("g541_s_valid")), V("g541_s_total"))}],
}


def mb_mutants(vals):
    """MB per clause: each count moved JUST across its own threshold (the band from g5.35's prereg; g5.41's 50% as
    2 x count >= total). -> [(clause id, count name, moved value)]."""
    band = vals["g535_band"]
    return [("b_g535_f1_null", "g535_null_hits", band), ("b_g535_f2_salt", "g535_salt_hits", band - 1),
            ("b_g541_smech", "g541_blend0", -(-vals["g541_invalid0"] // 2)), ("b_g541_sout", "g541_s_valid", -(-vals["g541_s_total"] // 2))]


def mc_pick(lines):
    """MC fallback rule (committed before the run): the first integer-exact line, in census order, whose proved
    predicate has exactly ONE comparison; its threshold is moved one past the measured value."""
    return next(ln for ln in lines if ln.get("integer_exact") and n_cmp(ln["proved"]) == 1)


# ---------- extract / census ----------
def blob(ref, path):
    return subprocess.run(["git", "-C", HERE, "show", f"{ref}:{path}"], capture_output=True, check=True).stdout


def dig(d, key):   # "a.b.0.c" -> d["a"]["b"][0]["c"]; "4\\.0" keeps a dot inside one key
    for k in [p.replace("\0", ".") for p in key.replace("\\.", "\0").split(".")]:
        d = d[int(k)] if isinstance(d, list) else d[k]
    return d


def read(srcs, how, keys):
    v = [dig(srcs, k) for k in keys]
    isint = lambda x: isinstance(x, int) and not isinstance(x, bool)
    if how == "int":
        assert isint(v[0]), v
        return v[0]
    if how == "notnull":
        return int(v[0] is not None)
    if how == "int_or0":
        assert v[0] is None or isint(v[0]), v
        return v[0] or 0
    if how == "len":
        assert isinstance(v[0], list)
        return len(v[0])
    assert all(isint(x) for x in v), v
    if how == "sum":
        return sum(v)
    if how == "sum_diff":   # sum(n_i - invalid_i): the first half of keys minus the second half
        h = len(v) // 2
        return sum(a - b for a, b in zip(v[:h], v[h:]))
    raise ValueError(how)


def binom_band(n, chance, alpha):
    """g5.35's band re-derived from its prereg: the smallest k with P(X >= k) <= alpha, X ~ Bin(n, chance), exact."""
    p, a = Fraction(str(chance)), Fraction(str(alpha))
    tail = lambda k: sum(comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))
    return next(k for k in range(n + 1) if tail(k) <= a)


def falsifier_lines(goal_id):
    """The goal node's numbered Falsifier lines, verbatim at HEAD: ({'1': text, '2b': text, ...}, path, blob sha256)."""
    hit = subprocess.run(["git", "-C", HERE, "grep", "-l", f"^id: {goal_id}$", "HEAD", "--", ":/.agi/nodes"], capture_output=True, text=True).stdout.split()
    f = [h.split(":", 1)[1] for h in hit if "/deprecated/" not in h][0]
    t = blob("HEAD", f).decode()
    out = {}
    for ln in t.split("## Falsifier", 1)[1].split("\n## ", 1)[0].strip().splitlines():
        head = ln.split(".", 1)[0].strip()
        if head and (head.isdigit() or (head[:-1].isdigit() and head[-1].isalpha())):
            out[head] = ln.split(".", 1)[1].strip()
    return out, f, hashlib.sha256(blob("HEAD", f)).hexdigest()


def out_dir():
    return paths.get_local("bend2_graph_dir")


def load_P():
    pp = os.path.join(out_dir(), "params.json")
    return json.load(open(pp)), L.sha(pp)


def stage_extract():
    """counts.json: every value a law reads, from its PINNED source; g5.35's band re-derived from its prereg."""
    srcs, shas = {}, {}
    for src in sorted({s for s, _, _ in READS.values()} | {P35}):
        b = blob(*src)
        srcs[src], shas[f"{src[0]}:{src[1]}"] = json.loads(b), hashlib.sha256(b).hexdigest()
    vals = {name: read(srcs[src], how, keys) for name, (src, how, keys) in READS.items()}
    pr = srcs[P35]
    band = binom_band(pr["n"], pr["chance"], pr["alpha_harness"])
    assert band == vals["g535_band"], (band, vals["g535_band"])
    json.dump({"values": vals, "g535_band_from_prereg": band, "source_sha256": shas}, open(os.path.join(out_dir(), "counts.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps({"n_values": len(vals), "counts_sha256": L.sha(os.path.join(out_dir(), "counts.json")), "band": band}))


def stage_census():
    """census.json: every falsifier line of the closed rounds, its verbatim cite, integer-exact by the invariance rule
    (computed here on the committed counts, before any law), the committed verdict; n of N; the MC pick."""
    vals = json.load(open(os.path.join(out_dir(), "counts.json")))["values"]
    cites, rows = {}, []
    for ln in LINES:
        if ln["goal"] not in cites:
            cites[ln["goal"]] = falsifier_lines(ln["goal"])
        text, path, gsha = cites[ln["goal"]]
        row = {**ln, "cite": text[ln["line"]], "cite_src": {"path": path, "blob_sha256_at_HEAD": gsha}}
        if "proved" in ln and "committed" in ln:
            vs = verdicts_all(ln, vals)
            row["verdicts_over_free_clauses"] = sorted(vs)
            row["integer_exact"] = len(vs) == 1
            row["python_verdict"] = next(iter(vs)) if len(vs) == 1 else None
        else:
            row["integer_exact"] = False
        rows.append(row)
    n, N = sum(r["integer_exact"] for r in rows), len(rows)
    mc = mc_pick(rows)
    C = {"rule": __doc__.split("(STEP A's rule, fixed before any law): ")[1].split(" Counts come")[0], "n_integer_exact": n, "N_lines": N,
         "lines": rows, "excluded": EXCLUDED,
         "mc": {"pinned": "g5.36 line 1, the clause 'N_f <= threshold' moved 64 -> 128, the line staying DISPROVED", "pinned_feasible": False,
                "why": "g5.36 committed N_f only as null (its own text: none -> N_f > 64); the 128 is a float accuracy on the extension grid, never a committed integer, so 'N_f <= 128' is undecidable on committed integers",
                "fallback": mc["id"], "fallback_rule": mc_pick.__doc__.strip()}}
    json.dump(C, open(os.path.join(out_dir(), "census.json"), "w"), indent=1)
    print(json.dumps({"n_of_N": f"{n} of {N}", "integer_exact": [r["id"] for r in rows if r["integer_exact"]],
                      "python_vs_committed": {r["id"]: (r["python_verdict"], r["committed"]) for r in rows if r["integer_exact"]}, "mc_fallback": mc["id"]}))


def tup(e):
    return tuple(tup(x) for x in e) if isinstance(e, list) else e


def law_sets(C, vals):
    sets = {}
    for ln in (ln for ln in C["lines"] if ln["integer_exact"]):
        sets[f"C_{ln['id']}"] = ("C", [ln], vals, {ln["id"]: ln["committed"]}, "check")
        for other in sorted(set(VERDICT) - {ln["committed"]}):
            sets[f"C_{ln['id']}_not_{other}"] = ("C", [ln], vals, {ln["id"]: other}, "fail")
    cite = lambda c: next(r for r in C["lines"] if r["goal"] == c["goal"] and r["line"] == c["line"])["cite"]
    allb = {}
    for pair, lb in STEP_B.items():
        lb = [{**c, "cite": cite(c)} for c in lb]
        allb.update({c["id"]: c for c in lb})
        sets[f"B_{pair}"] = ("B", lb, vals, {c["id"]: c["committed"] for c in lb}, "check")
        for c in lb:
            sets[f"B_{pair}_{c['id']}_flipped"] = ("B", [c], vals, {c["id"]: "disproved" if c["committed"] == "proved" else "proved"}, "fail")
    for cid, var, to in mb_mutants(vals):
        sets[f"MB_{cid}"] = ("B", [allb[cid]], {**vals, var: to}, {cid: allb[cid]["committed"]}, "fail")
    m = next(ln for ln in C["lines"] if ln["id"] == C["mc"]["fallback"])
    measured, thr = walk(m["proved"], "var")
    moved = {**vals, thr: vals[measured] + 1}
    want = verdict_one(m, moved)
    assert want != m["committed"], "the moved threshold must flip the line"
    mm = {**m, "id": m["id"] + "_mc"}
    sets["MC_" + m["id"]] = ("C", [mm], moved, {mm["id"]: want}, "check")
    sets["MC_" + m["id"] + "_unflipped"] = ("C", [mm], moved, {mm["id"]: m["committed"]}, "fail")
    return sets


def stage_gen():
    o = out_dir()
    C, vals = json.load(open(os.path.join(o, "census.json"))), json.load(open(os.path.join(o, "counts.json")))["values"]
    for ln in C["lines"]:   # json turned the DSL tuples into lists
        for k in ("proved", "void"):
            if ln.get(k) is not None:
                ln[k] = tup(ln[k])
    files, sets = {}, {}
    for k, (step, lines, vs, claim, want) in law_sets(C, vals).items():
        fs = files_for(lines, vs, claim)
        files[k] = L.write_dir(os.path.join(o, "laws", k), fs)
        sets[k] = {"step": step, "want": want, "claim": claim, "python": {ln["id"]: sorted(verdicts_all(ln, vs)) for ln in lines},
                   "n_lines": fs["LAWS.bend"].count("\n") + fs["PROOF.bend"].count("\n") + fs["VALUES.bend"].count("\n")}
    json.dump({"files": files, "sets": sets}, open(os.path.join(o, "laws_files.json"), "w"), indent=1, sort_keys=True)
    print(json.dumps({"n_sets": len(files)}))


def stage_check():
    P, psha = load_P()
    o = out_dir()
    F = json.load(open(os.path.join(o, "laws_files.json")))
    res = {}
    for k in sorted(F["files"]):
        s = F["sets"][k]
        r = L.run_bend({**P, "wall_cap_s": P["wall_cap_b_s"] if s["step"] == "B" else P["wall_cap_c_s"]}, os.path.join(o, "laws", k), False)
        res[k] = {**{x: r[x] for x in ("status", "wall_s", "peak_rss_mib")}, "want": s["want"], "as_wanted": r["status"] == s["want"], "tail": r["tail"][-4:]}
        print(k, r["status"], s["want"], r["wall_s"], flush=True)
    json.dump({"params_sha256": psha, "sets": res}, open(os.path.join(o, "check.json"), "w"), indent=1, sort_keys=True)


# ---------- STEP P ----------
def slice_files(T, ks):
    """Consecutive tape pairs ks of row a = 0 (b = ks[0]..): T_slice = only those entries + the shared cols."""
    p, ro = T["p"], open(os.path.join(HERE, "bend2_readout.bend")).read()
    x = sum(L.hit(L.logits(T["h"][k], T["n"][k], T["W"], T["b"]), k % p) for k in ks)
    prs = ", ".join(f"R.Pr{{{L.lit(T['h'][k])}, {L.lit(T['n'][k])}}}" for k in ks)
    head = L.law_file(T, [], nr=1, nb=1)   # header + cols() (+ a 1-pair r0 / tape(), unused by the law)
    law = f"def one() -> List<R.Pr>:\n  [{prs}]\n\nlaw total:\n  {{R.row(one(), cols(), 0, {ks[0]}, 0) == {x} : U32}}\n"
    return {"RO.bend": ro, "LAWS.bend": head + "\n" + law, "PROOF.bend": L.proof_file(["total"])}, law, x


def stage_profile():
    P, psha = load_P()
    T = json.load(open(os.path.join(paths.get_local("bend2_law_dir"), "tape.json")))
    full, runs, files = L.law_file(T, []), {}, {}
    for k in (0, 1, 2):
        sf, law, _ = slice_files(T, [k])
        files[f"slice_k{k}"], files[f"full_k{k}"] = sf, {**sf, "LAWS.bend": full + "\n" + law}
    files["slice_3"] = slice_files(T, [0, 1, 2])[0]
    files["lit"] = {**files["slice_k0"], "LAWS.bend": full + "\nlaw total:\n  {0 == 0 : U32}\n"}
    for name, fs in files.items():
        d = os.path.join(P["work_dir"], "profile", name)
        L.write_dir(d, fs)
        reps = [L.run_bend({**P, "wall_cap_s": P["wall_cap_b_s"]}, d, False) for _ in range(P["profile_repeats"])]
        runs[name] = {"status": [r["status"] for r in reps], "wall_s": [r["wall_s"] for r in reps], "max_wall_s": max(r["wall_s"] for r in reps),
                      "peak_rss_mib": max(r["peak_rss_mib"] for r in reps)}
        print(name, runs[name], flush=True)
    ok = all(s == "check" for n in ("slice_k0", "slice_3") for s in runs[n]["status"])
    m = (runs["slice_3"]["max_wall_s"] - runs["slice_k0"]["max_wall_s"]) / 2 if ok else None
    su = runs["slice_k0"]["max_wall_s"] - m if ok else None
    proj = 113 * su + 12769 * m if ok else None
    rule = None if proj is None else "reopen (a NEW leaf, old caps)" if proj <= 1200 else "bank (a budget ask)" if proj <= 25540 else "close (an evidenced negative)"
    json.dump({"params_sha256": psha, "runs": runs, "marginal_s": m, "startup_s": su, "projected_wall_s": proj, "rule": rule, "int_repr": P["int_repr"]},
              open(os.path.join(out_dir(), "profile.json"), "w"), indent=1)
    print(json.dumps({"marginal_s": m, "startup_s": su, "projected_wall_s": proj, "rule": rule}))


if __name__ == "__main__":
    {"extract": stage_extract, "census": stage_census, "gen": stage_gen, "check": stage_check, "profile": stage_profile}[sys.argv[1]]()
