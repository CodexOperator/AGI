"""goal:g5.44 (lap 4) -- a COPY of goal:g5.40 round 2's closed mutscore_r2.py (rule 11:34Z).  What
differs from round 2:
  - THREE mutant classes per item: OWN (round 2's own named mutants, unchanged), CLAUSE and BLATANT,
    both written by a BLIND second drafter (g544_blind_brief.md); every mutant runs on a FRESH tree;
  - SKIP RULE (review residue): a mutant run with rc 0 that SKIPPED reads SURVIVED only where its
    clause carries `claim_requires_path: true`; otherwise it reads `skip_unscored` and leaves the
    denominator.  OWN and BLATANT mutants disable the claim's whole path, so for them a skip reads
    SURVIVED; a BASELINE with any skip is still NOT RUNNABLE;
  - the lap-4 falsifier, read against round 2's committed results_r2.json.

    python3 mutscore_r3.py validate   # static: every edit's `old` occurs exactly once at its commit
    python3 mutscore_r3.py run        # writes results_r3.json next to this file
"""
import hashlib
import json
import re
import os
import pathlib
import shutil
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
PARAMS = HERE / "params_r3.json"
RESULTS = HERE / "results_r3.json"
ROUND2 = HERE / "results_r2.json"
ROUND2_FRACTION = 44 / 84
REPO = HERE.parents[3]


def git(*args, **kw):
    return subprocess.run(["git", "-C", str(REPO), *args], check=True, capture_output=True, **kw).stdout


def item_file(item, path):
    """The bytes of `path` as the item's check sees them, before any mutant."""
    if "tree" in item:
        return item["tree"][path].encode()
    return git("cat-file", "blob", f"{item['pre_run_commit']}:{path}")


def mutants_of(it):
    out = [it["mutant"]] if it.get("mutant") else []
    return out + list(it.get("clauses", [])) + ([it["blatant"]] if it.get("blatant") else [])


def validate(params):
    bad = []
    for it in params["items"] + params["instrument"]:
        for m in mutants_of(it):
            text = item_file(it, m["file"]).decode()
            for old, _ in m["edits"]:
                if text.count(old) != 1:
                    bad.append((it["key"], m["file"], old[:40], text.count(old)))
    return bad


def build_tree(item, root):
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    if "tree" in item:
        for path, text in item["tree"].items():
            p = root / path
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text)
        return
    if item.get("tree_mode") == "clone":
        root.rmdir()
        q = {"capture_output": True, "check": True}
        subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", str(REPO), str(root)], **q)
        subprocess.run(["git", "-C", str(root), "remote", "remove", "origin"], **q)
        subprocess.run(["git", "-C", str(root), "-c", "advice.detachedHead=false", "checkout", "-q",
                        item["pre_run_commit"]], **q)
        return
    arc = subprocess.run(["git", "-C", str(REPO), "archive", item["pre_run_commit"]],
                         check=True, capture_output=True).stdout
    subprocess.run(["tar", "-x", "-C", str(root)], input=arc, check=True)


def child_env(params, root):
    env = {k: v for k, v in os.environ.items()
           if not k.startswith(("AGI_", "AUTORESEARCH_", "TMUX", "VERIFY_", "GIT_"))}
    home = root / ".home"
    home.mkdir(exist_ok=True)
    env.update({"HOME": str(home), "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1",
                "GIT_AUTHOR_NAME": "mutscore", "GIT_AUTHOR_EMAIL": "mutscore@local",
                "GIT_COMMITTER_NAME": "mutscore", "GIT_COMMITTER_EMAIL": "mutscore@local",
                "PYTHONHASHSEED": str(params["pythonhashseed"]), "PYTHONDONTWRITEBYTECODE": "1",
                "PATH": params["venv_bin"] + ":" + env.get("PATH", "/usr/bin:/bin")})
    return env


def run_check(params, item, root):
    cmd = f"ulimit -v {params['ulimit_v_kb']}; exec {item['check']}"
    t = time.monotonic()
    try:
        p = subprocess.run(["sh", "-c", cmd], cwd=root, env=child_env(params, root),
                           capture_output=True, timeout=params["timeout_s"])
        rc, out = p.returncode, p.stdout + p.stderr
    except subprocess.TimeoutExpired as e:
        rc, out = "timeout", (e.stdout or b"") + (e.stderr or b"")
    tail = out.decode(errors="replace").strip().splitlines()[-3:]
    text = out.decode(errors="replace")
    return {"rc": rc, "seconds": round(time.monotonic() - t, 1),
            "skipped": bool(re.search(r"\b\d+ skipped\b", text)),
            "out_sha256": hashlib.sha256(out).hexdigest(), "tail": tail}


def apply_edits(text, edits):
    spans = []
    for old, new in edits:
        if text.count(old) != 1:
            raise ValueError(f"mutant edit does not apply once: {old[:40]!r}")
        i = text.index(old)
        spans.append((i, i + len(old), new))
    spans.sort()
    if any(a[1] > b[0] for a, b in zip(spans, spans[1:])):
        raise ValueError("mutant edits overlap")
    out, at = [], 0
    for i, j, new in spans:
        out += [text[at:i], new]
        at = j
    return "".join(out + [text[at:]])


def mutate(item, root, m):
    p = root / m["file"]
    p.write_text(apply_edits(p.read_text(), m["edits"]))


def one(params, item, root, m):
    build_tree(item, root)
    mutate(item, root, m)
    r = run_check(params, item, root)
    if r["rc"] != 0:
        outcome = "killed"
    elif r["skipped"] and not m.get("claim_requires_path", True):
        outcome = "skip_unscored"
    else:
        outcome = "survived"
    return {"clause": m.get("clause"), "kind": m["kind"], "file": m["file"], "rc": r["rc"],
            "skipped": r["skipped"], "claim_requires_path": m.get("claim_requires_path", True),
            "tail": r["tail"], "out_sha256": r["out_sha256"], "outcome": outcome}


def score(params, item):
    root = pathlib.Path(params["scratch"]) / item["key"]
    row = {"key": item["key"], "hypothesis": item.get("hypothesis"), "seen_by_review": item.get("seen_by_review", False)}
    build_tree(item, root)
    row["baseline"] = run_check(params, item, root)
    if row["baseline"]["rc"] != 0 or row["baseline"]["skipped"]:
        row["outcome"] = "not_runnable"           # a skipped named test is not a pass
    else:
        row["outcome"] = "ran"
        row["own"] = one(params, item, root, item["mutant"]) if item.get("mutant") else None
        row["clauses"] = [one(params, item, root, m) for m in item.get("clauses", []) if m.get("file")]
        row["blatant"] = one(params, item, root, item["blatant"]) if item.get("blatant", {}).get("file") else None
    shutil.rmtree(root, ignore_errors=True)
    return row


def rate(ms):
    sc = [m for m in ms if m and m["outcome"] in ("killed", "survived")]
    sv = sum(m["outcome"] == "survived" for m in sc)
    return {"scored": len(sc), "survived": sv, "killed": len(sc) - sv,
            "skip_unscored": sum(1 for m in ms if m and m["outcome"] == "skip_unscored"),
            "fraction": (sv / len(sc)) if sc else None}


def main(argv):
    params = json.loads(PARAMS.read_text())
    cmd = argv[1] if len(argv) > 1 else ""
    bad = validate(params)
    if cmd == "validate":
        print("validate:", "ok" if not bad else bad)
        return 1 if bad else 0
    if cmd != "run":
        print(__doc__)
        return 2
    if bad:
        raise SystemExit(f"refused: mutants that do not apply once: {bad}")
    rows, inst = [], []
    for it in params["instrument"]:
        root = pathlib.Path(params["scratch"]) / it["key"]
        build_tree(it, root)
        base = run_check(params, it, root)
        m = one(params, it, root, it["mutant"])
        shutil.rmtree(root, ignore_errors=True)
        r = {"key": it["key"], "baseline": base, "mutant": m, "expect": it["expect"],
             "outcome": m["outcome"] if base["rc"] == 0 else "not_runnable"}
        r["as_expected"] = r["outcome"] == it["expect"]
        inst.append(r)
        print(r["key"], r["outcome"], "as expected" if r["as_expected"] else "NOT AS EXPECTED", flush=True)
    for it in params["items"]:
        r = score(params, it)
        rows.append(r)
        print(r["key"], r["outcome"], (r.get("own") or {}).get("outcome"),
              [m["outcome"] for m in r.get("clauses", [])], (r.get("blatant") or {}).get("outcome"), flush=True)
    nr = sum(r["outcome"] == "not_runnable" for r in rows)
    ran = [r for r in rows if r["outcome"] == "ran"]
    r2 = {x["key"]: any(m["outcome"] == "survived" for m in x["clauses"])
          for x in json.loads(ROUND2.read_text())["items"] if x["outcome"] == "ran"}
    per = []
    for r in rows:
        mine = any(m["outcome"] == "survived" for m in r.get("clauses", [])) if r["outcome"] == "ran" else None
        per.append({"key": r["key"], "round2_has_survivor": r2.get(r["key"]), "blind_has_survivor": mine,
                    "agree": mine is not None and mine == r2.get(r["key"])})
    agree = sum(x["agree"] for x in per)
    clause = rate([m for r in ran for m in r["clauses"]])
    blatant = rate([r["blatant"] for r in ran])
    own = rate([r.get("own") for r in ran])
    void = []
    if nr > 5:
        void.append(f"{nr} not runnable (> 5)")
    if not all(r["as_expected"] for r in inst):
        void.append("an instrument mutant (M1-M3) did not read as stated")
    if blatant["fraction"] is None or blatant["fraction"] > 0.15:
        void.append(f"falsifier 2: blatant survival {blatant['fraction']} > 0.15 (the instrument does not track closeness)")
    f = clause["fraction"]
    robust = agree >= 13 and f is not None and abs(f - ROUND2_FRACTION) <= 0.15
    out = {"goal": "goal:g5.44", "params_sha256": hashlib.sha256(PARAMS.read_bytes()).hexdigest(),
           "round2_results_sha256": hashlib.sha256(ROUND2.read_bytes()).hexdigest(),
           "not_runnable": nr, "classes": {"own": own, "clause": clause, "blatant": blatant},
           "agreement": {"agree": agree, "of": len(per), "bar": 13, "per_item": per},
           "clause_fraction_vs_round2": {"blind": f, "round2": ROUND2_FRACTION,
                                         "delta": None if f is None else f - ROUND2_FRACTION, "bar": 0.15},
           "falsifier_1": {"rule": "ROBUST iff agree >= 13 of 16 AND |blind clause fraction - 44/84| <= 0.15; RED otherwise",
                           "verdict": "void" if void else ("proved" if robust else "disproved")},
           "void_reasons": void, "instrument": inst, "items": rows}
    RESULTS.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: out[k] for k in ("not_runnable", "classes", "clause_fraction_vs_round2", "falsifier_1", "void_reasons")}))
    print("agreement", out["agreement"]["agree"], "of", out["agreement"]["of"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
