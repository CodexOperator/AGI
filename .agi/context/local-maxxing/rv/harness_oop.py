"""goal:g5.48 -- the remote-viewing harness with the viewer fenced OUT of process.

Imports round 2's closed harness.py (never edits it).  What differs:
  - the viewer is its own process: fork + exec of `python3 -I viewer_oop.py <kind> <public args>`,
    close_fds=True, a scrubbed env, an argv with no secret, pipes only; it gets (trial,
    commitment) on stdin (plus the salt only in the F2 planted-leak arm);
  - the parent calls prctl(PR_SET_DUMPABLE, 0) BEFORE the secret exists; the secret lives only in
    the parent's memory (never a file) until results_oop.json reveals it;
  - decoys are drawn from the pool minus EVERY target of the run (the C2 fix);
  - `run` is two-phase: it makes the secret, writes ONLY its sha256 to <run dir>/secret_sha256.txt,
    then WAITS until prereg_oop.json on posts/<post> (the pre-run commit) carries that sha256
    and matches the working file byte for byte; only then does any trial run.

    python3 harness_oop.py run RUN_DIR     # main run: F1 null, F2 salt, A* out of process; M1; M2
    python3 harness_oop.py m3 RUN_DIR      # mutant M3: dumpable LEFT at 1, fresh secret, A* out of process
    python3 harness_oop.py verify          # re-derives every harness draw from the revealed secrets
                                           # and re-judges the recorded descriptions (the viewer tape)
"""
import ctypes
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import time

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import harness as h  # noqa: E402  (round 2's closed harness: imported, never edited)
import viewer_oop  # noqa: E402

PREREG = HERE / "prereg_oop.json"
RESULTS = HERE / "results_oop.json"
RESULTS_M3 = HERE / "results_oop_m3.json"
ROUND2_RESULTS = HERE / "results.json"
ROUND2_PREREG = HERE / "prereg.json"
VIEWER = HERE / "viewer_oop.py"
PR_SET_DUMPABLE, PR_GET_DUMPABLE = 4, 3
_libc = ctypes.CDLL(None, use_errno=True)


def set_dumpable(v):
    _libc.prctl(PR_SET_DUMPABLE, v, 0, 0, 0)
    return _libc.prctl(PR_GET_DUMPABLE, 0, 0, 0, 0)


def ptrace_scope():
    try:
        with open("/proc/sys/kernel/yama/ptrace_scope") as f:
            return int(f.read())
    except OSError:
        return None


def scrubbed_env():
    return {"PATH": "/usr/bin:/bin", "LANG": "C.UTF-8", "PYTHONHASHSEED": "0"}


class ViewerProc:
    """The viewer as its own process: pipes only, close_fds, scrubbed env, public argv."""

    def __init__(self, kind, prereg, secret_sha256, run_dir):
        argv = [sys.executable, "-I", str(VIEWER), kind, prereg["seed"], str(prereg["n"])]
        if kind == "attacker":
            argv += [secret_sha256, str(run_dir), str(HERE)]
        self.argv = argv
        self.p = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE, close_fds=True, env=scrubbed_env(),
                                  cwd=str(run_dir), text=True)

    def describe(self, trial, commitment, leak=None):
        self.p.stdin.write(json.dumps({"trial": trial, "commitment": commitment,
                                       "leak": leak.hex() if leak else None}) + "\n")
        self.p.stdin.flush()
        r = json.loads(self.p.stdout.readline())
        return set(r["desc"]), r["channel"]

    def close(self):
        self.p.stdin.close()
        err = self.p.stderr.read()
        self.p.wait(timeout=60)
        self.p.stdout.close()
        self.p.stderr.close()
        return {"rc": self.p.returncode, "stderr_tail": err.strip().splitlines()[-1:]}


class InProc:
    """Mutant M1's carrier: the SAME A* class called inside the parent."""

    def __init__(self, prereg, secret_sha256, run_dir):
        self.a = viewer_oop.Attacker(prereg["seed"], prereg["n"], secret_sha256, [str(run_dir), str(HERE)],
                                     ppid=os.getpid())

    def describe(self, trial, commitment, leak=None):
        return self.a.describe(trial, commitment, leak)

    def close(self):
        return {"rc": 0, "stderr_tail": [json.dumps({"tried": self.a.tried, "dead": sorted(self.a.dead)})]}


def decoys_for(key, pool, targets, trial, fixed=True):
    td = h.Dice(key, f"trial/{trial}")
    excl = set(targets) if fixed else {targets[trial]}
    decoys = td.sample([t for t in range(len(pool)) if t not in excl], h.DECOYS)
    return decoys, td.bytes(h.SALT_BYTES)


def run_trial_oop(key, pool, targets, viewer, trial, plant_salt=False):
    target = targets[trial]
    decoys, salt = decoys_for(key, pool, targets, trial)
    c = h.commit(target, salt)
    desc, channel = viewer.describe(trial, c, leak=salt if plant_salt else None)
    order = h.Dice(key, f"shuffle/{trial}").shuffle([target] + decoys)
    ranking = h.judge(desc, [pool[t] for t in order], h.Dice(key, f"judge/{trial}"))
    rank = ranking.index(order.index(target)) + 1
    return {"trial": trial, "commitment": c, "target": target, "decoys": decoys, "desc": sorted(desc),
            "channel": channel, "rank": rank, "hit": rank == 1}


def run_arm(key, pool, targets, viewer, n, plant_salt=False):
    rows = [run_trial_oop(key, pool, targets, viewer, t, plant_salt) for t in range(n)]
    return rows, viewer.close()


def channels(rows):
    out = {}
    for r in rows:
        out[str(r["channel"])] = out.get(str(r["channel"]), 0) + 1
    return out


def old_draw_counts():
    """M2's old side: round 2's draw (decoys from the pool minus the trial's own target),
    replayed from round 2's revealed secret."""
    r2 = json.loads(ROUND2_RESULTS.read_text())
    p2 = json.loads(ROUND2_PREREG.read_text())
    key = h.secret_key(bytes.fromhex(r2["secret_hex_revealed"]))
    pool = h.make_pool(p2["seed"])
    T = h.draw_targets(key, pool, p2["n"])
    dec = [decoys_for(key, pool, T, t, fixed=False)[0] for t in range(p2["n"])]
    return decoy_counts(T, dec)


def decoy_counts(T, dec):
    S = set(T)
    return {"decoys": sum(len(d) for d in dec),
            "any_run_target": sum(x in S for d in dec for x in d),
            "earlier_trial_target": sum(x in set(T[:t]) for t, d in enumerate(dec) for x in d)}


def wait_for_prerun(sha, post, timeout_s):
    path = ".agi/context/local-maxxing/rv/prereg_oop.json"
    t0 = time.monotonic()
    while time.monotonic() - t0 < timeout_s:
        p = subprocess.run(["git", "-C", str(HERE), "show", f"posts/{post}:{path}"],
                           capture_output=True, text=True, close_fds=True)
        if p.returncode == 0:
            try:
                committed = json.loads(p.stdout)
            except ValueError:
                committed = {}
            if committed.get("secret_sha256") == sha and p.stdout == PREREG.read_text():
                return True
        time.sleep(5)
    return False


def summarize_astar(rows, prereg):
    a = prereg["alpha_astar"]
    tr, ho = prereg["train_trials"], prereg["held_out_trials"]
    return {"all": h.summarize(rows, prereg["chance"], a),
            "train": h.summarize(rows[tr[0]:tr[1]], prereg["chance"], a),
            "held_out": h.summarize(rows[ho[0]:ho[1]], prereg["chance"], a)}


def cmd_run(run_dir, post):
    prereg = json.loads(PREREG.read_text())
    d = set_dumpable(0)                       # BEFORE the secret exists
    if d != 0:
        raise SystemExit(f"PR_SET_DUMPABLE did not take: get = {d}")
    secret = os.urandom(32)
    sha = hashlib.sha256(secret).hexdigest()
    (run_dir / "secret_sha256.txt").write_text(sha + "\n")
    print(f"secret_sha256 {sha}: waiting for the pre-run commit on posts/{post}", flush=True)
    if not wait_for_prerun(sha, post, prereg["wait_s"]):
        raise SystemExit("no pre-run commit carried the secret's sha256: nothing ran")
    print("pre-run commit seen: running", flush=True)
    n, key, pool = prereg["n"], h.secret_key(secret), h.make_pool(prereg["seed"])
    targets = h.draw_targets(key, pool, n)
    arms, procs = {}, {}
    arms["F1_null_oop"], procs["F1_null_oop"] = run_arm(key, pool, targets, ViewerProc("null", prereg, sha, run_dir), n)
    arms["F2_salt_oop"], procs["F2_salt_oop"] = run_arm(key, pool, targets, ViewerProc("salt", prereg, sha, run_dir), n, plant_salt=True)
    v = ViewerProc("attacker", prereg, sha, run_dir)
    arms["Astar_oop"], procs["Astar_oop"] = run_arm(key, pool, targets, v, n)
    procs["Astar_oop"]["argv_public_only"] = secret.hex() not in " ".join(v.argv)
    arms["M1_Astar_in_process"], procs["M1_Astar_in_process"] = run_arm(key, pool, targets, InProc(prereg, sha, run_dir), n)
    fixed = decoy_counts(targets, [r["decoys"] for r in arms["F1_null_oop"]])
    old = old_draw_counts()
    s = {
        "F1_null_oop": h.summarize(arms["F1_null_oop"], prereg["chance"], prereg["alpha_null"]),
        "F2_salt_oop": h.summarize(arms["F2_salt_oop"], prereg["chance"], prereg["alpha_null"]),
        "Astar_oop": summarize_astar(arms["Astar_oop"], prereg),
        "M1_Astar_in_process": h.summarize(arms["M1_Astar_in_process"], prereg["chance"], prereg["alpha_null"]),
    }
    checks = {
        "F1_null_chance": s["F1_null_oop"]["inside_chance"],
        "F2_salt_200": s["F2_salt_oop"]["hits"] == n,
        "Astar_inside_all": s["Astar_oop"]["all"]["inside_chance"],
        "Astar_inside_train": s["Astar_oop"]["train"]["inside_chance"],
        "Astar_inside_held_out": s["Astar_oop"]["held_out"]["inside_chance"],
        "M1_ge_150": s["M1_Astar_in_process"]["hits"] >= prereg["mutant_floor"],
        "M2_fixed_zero": fixed["any_run_target"] == 0 and fixed["earlier_trial_target"] == 0,
        "M2_old_exact": old["earlier_trial_target"] == prereg["m2_old_earlier_trial_target"]
                        and old["any_run_target"] == prereg["m2_old_any_run_target"],
    }
    void = [k for k in ("M1_ge_150", "M2_fixed_zero", "M2_old_exact") if not checks[k]]
    astar_ok = checks["Astar_inside_all"] and checks["Astar_inside_train"] and checks["Astar_inside_held_out"]
    verdict = "void" if void else ("proved" if astar_ok and checks["F1_null_chance"] and checks["F2_salt_200"] else "disproved")
    out = {"goal": "goal:g5.48", "prereg_sha256": hashlib.sha256(PREREG.read_bytes()).hexdigest(),
           "secret_sha256": sha, "secret_hex_revealed": secret.hex(), "dumpable": d,
           "ptrace_scope": ptrace_scope(), "uid": "same uid (stated limit)",
           "summaries": s, "channels": {k: channels(v) for k, v in arms.items()}, "procs": procs,
           "m2": {"fixed_draw": fixed, "old_draw_round2": old}, "checks": checks,
           "void_reasons": void, "verdict": verdict, "arms": arms}
    RESULTS.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: out[k] for k in ("checks", "void_reasons", "verdict", "channels", "m2")}))
    return 0


def cmd_m3(run_dir):
    prereg = json.loads(PREREG.read_text())
    d = set_dumpable(1)                       # mutant M3: dumpable LEFT at 1
    secret = os.urandom(32)
    sha = hashlib.sha256(secret).hexdigest()
    n, key, pool = prereg["n"], h.secret_key(secret), h.make_pool(prereg["seed"])
    targets = h.draw_targets(key, pool, n)
    rows, proc = run_arm(key, pool, targets, ViewerProc("attacker", prereg, sha, run_dir), n)
    s = h.summarize(rows, prereg["chance"], prereg["alpha_null"])
    ch = channels(rows)
    ok = s["hits"] >= prereg["mutant_floor"] and ch.get("mem", 0) >= prereg["mutant_floor"]
    out = {"goal": "goal:g5.48", "mutant": "M3", "dumpable": d, "ptrace_scope": ptrace_scope(),
           "secret_sha256": sha, "secret_hex_revealed": secret.hex(), "summary": s, "channels": ch,
           "proc": proc, "M3_as_stated": ok,
           "reading": "as stated: A* reads the secret via /proc/PPID/mem" if ok else "NOT as stated: the /proc channel of A* is VOID",
           "rows": rows}
    RESULTS_M3.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n")
    print(json.dumps({k: out[k] for k in ("dumpable", "summary", "channels", "M3_as_stated")}))
    return 0


def replay(res, prereg, arm_names):
    secret = bytes.fromhex(res["secret_hex_revealed"])
    if hashlib.sha256(secret).hexdigest() != res["secret_sha256"]:
        return ["revealed secret does not match its sha256"]
    key, pool, n = h.secret_key(secret), h.make_pool(prereg["seed"]), prereg["n"]
    T, bad = h.draw_targets(key, pool, n), []
    for name in arm_names:
        rows = res["arms"][name] if "arms" in res else res["rows"]
        for r in rows:
            t = r["trial"]
            dec, salt = decoys_for(key, pool, T, t)
            order = h.Dice(key, f"shuffle/{t}").shuffle([T[t]] + dec)
            rank = h.judge(set(r["desc"]), [pool[x] for x in order], h.Dice(key, f"judge/{t}")).index(order.index(T[t])) + 1
            if (r["target"], r["decoys"], r["commitment"], r["rank"]) != (T[t], dec, h.commit(T[t], salt), rank):
                bad.append(f"{name}/{t}")
    return bad


def cmd_verify():
    prereg = json.loads(PREREG.read_text())
    res = json.loads(RESULTS.read_text())
    bad = []
    if res["secret_sha256"] != prereg["secret_sha256"]:
        bad.append("results secret_sha256 differs from the pre-committed one")
    bad += replay(res, prereg, list(res["arms"]))
    if RESULTS_M3.exists():
        bad += ["m3:" + b for b in replay(json.loads(RESULTS_M3.read_text()), prereg, ["M3"])]
    print("replay: identical" if not bad else f"replay: DIFFERS {bad[:5]}")
    return 0 if not bad else 1


def main(argv):
    cmd = argv[1] if len(argv) > 1 else ""
    if cmd == "run":
        return cmd_run(pathlib.Path(argv[2]), os.environ.get("AGI_POST", "director-thought-science"))
    if cmd == "m3":
        return cmd_m3(pathlib.Path(argv[2]))
    if cmd == "verify":
        return cmd_verify()
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
