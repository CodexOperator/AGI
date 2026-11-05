"""goal:g5.40 -- a falsifier mutation score over landed proved checks (DeMillo-Lipton-Sayward 1978).

Stdlib only.  For each item frozen in params.json (BEFORE any run):
  1. an ARCHIVED scratch tree: `git archive <pre_run_commit> | tar -x` under SCRATCH/<key>
     (never ~/t, never a worktree of the live repo); instrument items write their own tiny tree;
  2. BASELINE: the check as committed must read proved (rc 0), else the item is NOT RUNNABLE;
  3. MUTANT: ONE pre-written change to ONE file -- a list of exact edits [old, new], each `old`
     matching exactly once, applied simultaneously (so a swap is two edits);
  4. the check again: rc != 0 = KILLED (the check can fail), rc 0 = SURVIVED (it could not).
Runs are sequential, one child at a time, each under `ulimit -v` (<= 3 GiB) and a timeout, with
AGI_* / TMUX* stripped, HOME and git's global config pointed into the scratch tree.  No random
draw is made here; PYTHONHASHSEED is pinned and recorded.

    python3 mutscore.py validate   # static: every mutant's `old` occurs exactly once at its commit
    python3 mutscore.py run        # writes results.json next to this file
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
PARAMS = HERE / "params.json"
RESULTS = HERE / "results.json"
REPO = HERE.parents[3]


def git(*args, **kw):
    return subprocess.run(["git", "-C", str(REPO), *args], check=True, capture_output=True, **kw).stdout


def item_file(item, path):
    """The bytes of `path` as the item's check sees them, before any mutant."""
    if "tree" in item:
        return item["tree"][path].encode()
    return git("cat-file", "blob", f"{item['pre_run_commit']}:{path}")


def validate(params):
    bad = []
    for it in params["items"] + params["instrument"]:
      for m in (it.get("mutant"), it.get("arm_swap")):
        if not m:
            continue
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


def score(params, item):
    """Column 1 (H-F1): the item's PRIMARY mutant (own, else arm swap, else inversion).
    Column 2 (H-F2, pin 11:14Z): the ARM SWAP, run again on a fresh tree when the primary is the
    item's own mutant; when the primary IS the arm swap the column reuses that run."""
    root = pathlib.Path(params["scratch"]) / item["key"]
    row = {"key": item["key"], "hypothesis": item.get("hypothesis"),
           "primary_kind": item.get("mutant", {}).get("kind"), "arm_swap_defined": "arm_swap" in item
           or item.get("mutant", {}).get("kind") == "arm-swap"}
    if not item.get("mutant"):
        row["outcome"] = row["arm_swap_outcome"] = "not_killable"
        return row
    build_tree(item, root)
    row["baseline"] = run_check(params, item, root)
    if row["baseline"]["rc"] != 0 or row["baseline"]["skipped"]:
        row["outcome"] = "not_runnable"           # a skipped named test is not a pass
        row["arm_swap_outcome"] = "not_runnable" if row["arm_swap_defined"] else None
        shutil.rmtree(root)
        return row
    mutate(item, root, item["mutant"])
    row["mutant"] = run_check(params, item, root)
    row["outcome"] = "survived" if row["mutant"]["rc"] == 0 else "killed"
    if item["mutant"]["kind"] == "arm-swap":
        row["arm_swap_outcome"] = row["outcome"]
    elif "arm_swap" in item:
        build_tree(item, root)
        mutate(item, root, item["arm_swap"])
        row["arm_swap"] = run_check(params, item, root)
        row["arm_swap_outcome"] = "survived" if row["arm_swap"]["rc"] == 0 else "killed"
    else:
        row["arm_swap_outcome"] = None
    shutil.rmtree(root)
    return row


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
        r = score(params, it)
        r["expect"] = it["expect"]
        r["as_expected"] = r["outcome"] == it["expect"]
        inst.append(r)
        print(r["key"], r["outcome"], "as expected" if r["as_expected"] else "NOT AS EXPECTED", flush=True)
    for it in params["items"]:
        r = score(params, it)
        rows.append(r)
        print(r["key"], r["outcome"], r["arm_swap_outcome"], flush=True)
    c = {k: sum(r["outcome"] == k for r in rows) for k in ("killed", "survived", "not_killable", "not_runnable")}
    n1 = c["killed"] + c["survived"]                     # pin (2): has a mutant AND ran
    sw = [r for r in rows if r["arm_swap_outcome"] in ("killed", "survived")]
    c2 = {"n": len(sw), "killed": sum(r["arm_swap_outcome"] == "killed" for r in sw),
          "survived": sum(r["arm_swap_outcome"] == "survived" for r in sw)}
    void = []
    if c["not_runnable"] > 5:
        void.append(f"{c['not_runnable']} not runnable (> 5)")
    if n1 < 10:
        void.append(f"H-F1 n = {n1} < 10")
    if not all(r["as_expected"] for r in inst):
        void.append("an instrument mutant did not read as stated")
    void2 = list(void) + ([f"H-F2 n = {c2['n']} < 10"] if c2["n"] < 10 else [])
    void1 = [v for v in void]
    h2_bar = max(5, c2["n"] / 4)
    out = {
        "goal": "goal:g5.40",
        "params_sha256": hashlib.sha256(PARAMS.read_bytes()).hexdigest(),
        "n_listed": len(rows), "n_excluded_at_selection": len(params["excluded"]),
        "counts_primary": dict(c, n=n1), "counts_arm_swap": c2,
        "H_F1": {"rule": "primary column: proved iff survived >= 2", "verdict":
                 "void" if void1 else ("proved" if c["survived"] >= 2 else "disproved"), "void_reasons": void1},
        "H_F2": {"rule": f"arm-swap column: proved iff survived >= max(5, n/4) = {h2_bar}", "verdict":
                 "void" if void2 else ("proved" if c2["survived"] >= h2_bar else "disproved"), "void_reasons": void2},
        "instrument": inst, "items": rows,
    }
    RESULTS.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: out[k] for k in ("counts_primary", "counts_arm_swap", "H_F1", "H_F2")}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
