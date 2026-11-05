"""goal:g5.35 residue (SM's gate 12:41Z): harness.py's in-run reveal check (`run_trial`, the line
marked `# the reveal`) recomputes the commitment from the same locals that made it, so it cannot
fail.  harness.py is round 2's CLOSED instrument (its bytes are what `harness.py verify` replays),
so it is not edited; this reader does the check that CAN fail, from the COMMITTED bytes alone:

  1. sha256(results.json's revealed secret) == prereg.json's pre-committed secret_sha256;
  2. every committed trial row opens: commit(row.target, row.salt) == row.commitment;
  3. every row's salt and target are the ones the revealed secret's streams draw (so a salt or
     target cannot have been chosen after the viewer ran).

    python3 open_reveals.py            # rc 0 = every committed reveal opens
    python3 open_reveals.py --mutant   # one row's salt flipped in memory: must exit 1 (RED)
"""
import hashlib
import json
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import harness as h  # noqa: E402


def check(results, prereg):
    bad = []
    secret = bytes.fromhex(results["secret_hex_revealed"])
    if hashlib.sha256(secret).hexdigest() != prereg["secret_sha256"]:
        bad.append("revealed secret does not match the pre-committed secret_sha256")
    key, pool = h.secret_key(secret), h.make_pool(prereg["seed"])
    targets = h.draw_targets(key, pool, prereg["n"])
    for arm, rows in results["trials"].items():
        for r in rows:
            t, salt = r["trial"], bytes.fromhex(r["salt"])
            if h.commit(r["target"], salt) != r["commitment"]:
                bad.append(f"{arm}/{t}: the committed reveal does not open the commitment")
            td = h.Dice(key, f"trial/{t}")
            td.sample([x for x in range(len(pool)) if x != targets[t]], h.DECOYS)
            if r["target"] != targets[t] or salt != td.bytes(h.SALT_BYTES):
                bad.append(f"{arm}/{t}: target or salt is not the secret stream's draw")
    return bad


def main(argv):
    results = json.loads((HERE / "results.json").read_text())
    prereg = json.loads((HERE / "prereg.json").read_text())
    if "--mutant" in argv:
        row = results["trials"]["F1_null"][0]
        row["salt"] = ("0" if row["salt"][0] != "0" else "1") + row["salt"][1:]
    bad = check(results, prereg)
    n = sum(len(v) for v in results["trials"].values())
    print(f"rows {n}, failures {len(bad)}" + ("".join("\n  " + b for b in bad[:5])))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
