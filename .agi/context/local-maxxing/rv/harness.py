"""goal:g5.35 -- a remote-viewing harness that is proved not to leak, and its null viewer.

Stdlib only, ONE process, no model.  Every random draw is a sha256 counter stream keyed by
(seed, label) -- `Dice` -- so a run replays byte for byte from the seed in prereg.json
("keep the chaos, log the dice", remix 11-05).

One trial (`run_trial`), in this order:
  1. the TARGET stream draws the true target + 4 decoys from POOL and a 16-byte salt;
  2. COMMIT: sha256(target_id || salt) goes to the ledger BEFORE the viewer runs;
  3. the viewer sees (trial, commitment) only -- plus the salt ONLY in the planted-leak mutant run;
  4. its description's sha256 goes to the ledger BEFORE the reveal;
  5. REVEAL: the salt is checked against the commitment (a mismatch raises);
  6. the blind JUDGE gets the description and the 5 candidates' tag sets, shuffled by their own
     stream, never the commitment, the salt or the target id, and ranks them; rank 1 = a hit.

Hill-climb (`climb`): a policy change is KEPT only on train-block gain and GRADED only on the
held-out block, both blocks declared in prereg.json before any policy is frozen.

    python3 harness.py run            # writes results.json next to this file (needs prereg.json)
    python3 harness.py verify         # re-runs and checks results.json byte for byte
"""
import hashlib
import json
import math
import pathlib
import sys

HERE = pathlib.Path(__file__).resolve().parent
PREREG = HERE / "prereg.json"
RESULTS = HERE / "results.json"

VOCAB = (
    "water", "stone", "tower", "bridge", "tree", "fire", "road", "mountain", "boat", "bird",
    "wheel", "door", "glass", "sand", "ice", "cloud", "metal", "rope", "field", "wall",
    "light", "shadow", "red", "blue", "green", "round", "tall", "flat", "curved", "square",
    "crowd", "empty", "moving", "still", "loud", "quiet", "hot", "cold", "wet", "dry",
    "old", "new", "natural", "built", "open", "closed", "high", "low",
)
TAGS_PER_TARGET = 6
POOL_SIZE = 100
DECOYS = 4
SALT_BYTES = 16


class Dice:
    """A recorded random stream: sha256(seed | label | counter), rejection-sampled, so it is
    identical on every Python build and two labels never share a draw."""

    def __init__(self, seed, label):
        self._key = f"{seed}|{label}|".encode()
        self._n = 0
        self._buf = b""

    def bytes(self, k):
        while len(self._buf) < k:
            self._buf += hashlib.sha256(self._key + str(self._n).encode()).digest()
            self._n += 1
        out, self._buf = self._buf[:k], self._buf[k:]
        return out

    def below(self, n):
        width = (n - 1).bit_length() // 8 + 1
        limit = (256 ** width // n) * n
        while True:
            x = int.from_bytes(self.bytes(width), "big")
            if x < limit:
                return x % n

    def sample(self, seq, k):
        seq = list(seq)
        for i in range(k):                     # a partial Fisher-Yates: the first k are the draw
            j = i + self.below(len(seq) - i)
            seq[i], seq[j] = seq[j], seq[i]
        return seq[:k]

    def shuffle(self, seq):
        return self.sample(seq, len(seq))


def make_pool(seed):
    """POOL_SIZE distinct targets, each a sorted tuple of TAGS_PER_TARGET tags."""
    dice, pool, seen = Dice(seed, "pool"), [], set()
    while len(pool) < POOL_SIZE:
        t = tuple(sorted(dice.sample(VOCAB, TAGS_PER_TARGET)))
        if t not in seen:
            seen.add(t)
            pool.append(t)
    return pool


def commit(target_id, salt):
    return hashlib.sha256(f"{target_id}|".encode() + salt).hexdigest()


def desc_hash(desc):
    return hashlib.sha256(json.dumps(sorted(desc)).encode()).hexdigest()


# ---- viewers: describe(trial, commitment, leak) -> a set of tags --------------------------------

class NullViewer:
    """A seeded RNG with no channel to the target: its stream's label names only the policy and
    the trial, never anything the target stream drew."""

    def __init__(self, seed, policy=0):
        self.seed, self.policy = seed, policy

    def describe(self, trial, commitment, leak=None):
        return set(Dice(self.seed, f"viewer/null/{self.policy}/{trial}").sample(VOCAB, TAGS_PER_TARGET))


class SaltMutantViewer:
    """THE MUTANT (must read RED): given the revealed salt early (a planted leak), it opens the
    commitment by brute force over the public pool and describes the true target."""

    def __init__(self, pool):
        self.pool = pool

    def describe(self, trial, commitment, leak=None):
        if leak is None:
            return set()
        for tid, tags in enumerate(self.pool):
            if commit(tid, leak) == commitment:
                return set(tags)
        return set()


# ---- the blind judge --------------------------------------------------------------------------

def judge(desc, candidates, dice):
    """Rank candidate tag sets by Jaccard overlap with the description; ties by the judge's own
    stream.  Takes NOTHING but the description and the candidates.  Returns positions, best first."""
    d = set(desc)
    keys = [(-(len(d & set(c)) / len(d | set(c)) if d | set(c) else 0.0), dice.below(1 << 30), i)
            for i, c in enumerate(candidates)]
    return [i for _, _, i in sorted(keys)]


def run_trial(seed, pool, viewer, trial, plant_salt=False, ledger=None):
    ledger = [] if ledger is None else ledger
    td = Dice(seed, f"target/{trial}")
    target = td.below(len(pool))
    decoys = td.sample([t for t in range(len(pool)) if t != target], DECOYS)
    salt = td.bytes(SALT_BYTES)
    c = commit(target, salt)
    ledger.append(("commit", trial, c))
    desc = viewer.describe(trial, c, leak=salt if plant_salt else None)
    h = desc_hash(desc)
    ledger.append(("describe", trial, h))
    if commit(target, salt) != c:                       # the reveal
        raise ValueError(f"trial {trial}: reveal does not open the commitment")
    ledger.append(("reveal", trial, salt.hex()))
    order = Dice(seed, f"shuffle/{trial}").shuffle([target] + decoys)
    ranking = judge(desc, [pool[t] for t in order], Dice(seed, f"judge/{trial}"))
    rank = ranking.index(order.index(target)) + 1
    return {"trial": trial, "commitment": c, "salt": salt.hex(), "target": target,
            "desc_sha256": h, "rank": rank, "hit": rank == 1}


def run_block(seed, pool, viewer, trials, plant_salt=False):
    return [run_trial(seed, pool, viewer, t, plant_salt) for t in trials]


# ---- statistics ---------------------------------------------------------------------------------

def binom_sf(k, n, p):
    """P(X >= k), X ~ Bin(n, p), exact."""
    return math.fsum(math.comb(n, i) * p ** i * (1 - p) ** (n - i) for i in range(k, n + 1))


def upper_band(n, p, alpha):
    """The smallest hit count c with P(X >= c) <= alpha: hits < c is inside chance (one-sided)."""
    return next(c for c in range(n + 2) if binom_sf(c, n, p) <= alpha)


def summarize(rows, p, alpha):
    n, hits = len(rows), sum(r["hit"] for r in rows)
    c = upper_band(n, p, alpha)
    return {"n": n, "hits": hits, "rate": hits / n, "band_hits_lt": c,
            "p_one_sided": binom_sf(hits, n, p), "inside_chance": hits < c}


def climb(seed, pool, policies, train, held_out):
    """Keep a policy only on train-block gain; grade it only on the held-out block."""
    rates = {p: sum(r["hit"] for r in run_block(seed, pool, NullViewer(seed, p), train)) / len(train)
             for p in policies}
    best = max(policies, key=lambda p: (rates[p], -p))
    held = run_block(seed, pool, NullViewer(seed, best), held_out)
    return {"policies": len(policies), "baseline_policy": policies[0], "kept_policy": best,
            "baseline_train_rate": rates[policies[0]], "kept_train_rate": rates[best],
            "train_gain": rates[best] - rates[policies[0]], "held_out": held}


def run(prereg):
    seed, p = prereg["seed"], prereg["chance"]
    pool = make_pool(seed)
    trials = list(range(prereg["n"]))
    train, held_out = prereg["train_trials"], prereg["held_out_trials"]
    null = run_block(seed, pool, NullViewer(seed, 0), trials)
    mutant = run_block(seed, pool, SaltMutantViewer(pool), trials, plant_salt=True)
    cl = climb(seed, pool, list(range(prereg["climb_policies"])),
               list(range(*train)), list(range(*held_out)))
    held_rows = cl.pop("held_out")
    null_s = summarize(null, p, prereg["alpha_harness"])
    mut_s = summarize(mutant, p, prereg["alpha_harness"])
    held_s = summarize(held_rows, p, prereg["alpha_held_out"])
    verdict = ("proved" if null_s["inside_chance"] and not mut_s["inside_chance"] else "disproved")
    return {
        "goal": "goal:g5.35",
        "prereg_sha256": hashlib.sha256(PREREG.read_bytes()).hexdigest() if PREREG.exists() else None,
        "seed": seed, "pool_sha256": hashlib.sha256(json.dumps(pool).encode()).hexdigest(),
        "falsifier_1_null": null_s, "falsifier_2_mutant": mut_s,
        "climb": dict(cl, held_out=held_s), "verdict": verdict,
        "null_trials": null, "mutant_trials": mutant,
    }


def dump(obj):
    return json.dumps(obj, indent=1, sort_keys=True) + "\n"


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "run"
    prereg = json.loads(PREREG.read_text())
    out = dump(run(prereg))
    if cmd == "run":
        RESULTS.write_text(out)
    elif cmd == "verify":
        same = RESULTS.read_text() == out
        print("replay: identical" if same else "replay: DIFFERS")
        return 0 if same else 1
    r = json.loads(out)
    for k in ("falsifier_1_null", "falsifier_2_mutant"):
        print(k, {x: r[k][x] for x in ("n", "hits", "rate", "band_hits_lt", "p_one_sided", "inside_chance")})
    print("climb", r["climb"]["train_gain"], r["climb"]["held_out"]["rate"], r["climb"]["held_out"]["p_one_sided"])
    print("verdict", r["verdict"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
