"""goal:g5.40 ROUND 2 (CORRECTIVE DH.1) -- a COPY of round 1's closed mutscore.py (rule 11:34Z: a
pre-run never edits a closed round's script).  What differs from round 1:
  - MUTATION RULE v2: per item, the own named mutant is its own column, and ONE mutant PER NAMED
    CLAUSE of the claim forms the clause column; every mutant runs on a FRESH tree;
  - a mutant run that SKIPS reads SURVIVED (rc 0: an rc-only check cannot tell a skip from a pass);
    a BASELINE with any skip is still NOT RUNNABLE;
  - `tree: clone` items (i06) run in a standalone `git clone --shared` with origin removed, never a
    worktree of the live repo;
  - H-F1 scored on the clause column over ALL items AND over the items the review has not seen.

    python3 mutscore_r2.py validate   # static: every edit's `old` occurs exactly once at its commit
    python3 mutscore_r2.py run        # writes results_r2.json next to this file
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
PARAMS = HERE / "params_r2.json"
RESULTS = HERE / "results_r2.json"
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
    return out + list(it.get("clauses", []))


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
    return {"clause": m.get("clause"), "kind": m["kind"], "file": m["file"], "rc": r["rc"],
            "skipped": r["skipped"], "tail": r["tail"], "out_sha256": r["out_sha256"],
            "outcome": "survived" if r["rc"] == 0 else "killed"}


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
        row["clauses"] = [one(params, item, root, m) for m in item.get("clauses", [])]
    shutil.rmtree(root, ignore_errors=True)
    return row


def hf1(rows):
    ran = [m for r in rows if r["outcome"] == "ran" for m in r["clauses"]]
    sv = sum(m["outcome"] == "survived" for m in ran)
    return {"n_clause_mutants": len(ran), "killed": len(ran) - sv, "survived": sv,
            "items": sum(r["outcome"] == "ran" for r in rows),
            "items_with_a_survivor": sum(any(m["outcome"] == "survived" for m in r["clauses"])
                                         for r in rows if r["outcome"] == "ran")}


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
              [m["outcome"] for m in r.get("clauses", [])], flush=True)
    nr = sum(r["outcome"] == "not_runnable" for r in rows)
    own = [r["own"] for r in rows if r.get("own")]
    out = {"goal": "goal:g5.40", "round": 2,
           "params_sha256": hashlib.sha256(PARAMS.read_bytes()).hexdigest(),
           "not_runnable": nr,
           "own_column": {"n": len(own), "survived": sum(m["outcome"] == "survived" for m in own)}}
    for name, sub in (("all", rows), ("unseen", [r for r in rows if not r["seen_by_review"]])):
        h = hf1(sub)
        void = []
        if nr > 5:
            void.append(f"{nr} not runnable (> 5)")
        if h["n_clause_mutants"] < 10:
            void.append(f"n = {h['n_clause_mutants']} < 10")
        if not all(r["as_expected"] for r in inst):
            void.append("an instrument mutant did not read as stated")
        h["verdict"] = "void" if void else ("proved" if h["survived"] >= 2 else "disproved")
        h["void_reasons"] = void
        out["H_F1_" + name] = h
    out["H_F2"] = {"verdict": "void", "void_reasons": ["arm swap defined for 0 items (n 0 < 10), as in round 1"]}
    out["instrument"], out["items"] = inst, rows
    RESULTS.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: out[k] for k in ("not_runnable", "own_column", "H_F1_all", "H_F1_unseen", "H_F2")}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
