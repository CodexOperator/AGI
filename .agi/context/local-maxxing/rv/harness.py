"""goal:g5.35 -- a remote-viewing harness that is proved not to leak, and its null viewer.

Stdlib only, ONE process, no model.  Every random draw is a sha256 counter stream keyed by
(key, label) -- `Dice` -- so a run replays byte for byte ("keep the chaos, log the dice", remix 11-05).

TWO keys (round 2, CORRECTIVE DH.1 leak A):
  - the PUBLIC seed (prereg.json): the target pool and the viewers' own streams;
  - the run-time SECRET (32 bytes of os.urandom, `harness.py secret-new`): EVERY harness-side draw --
    which targets, decoys, salt, candidate shuffle, judge ties.  No viewer is ever handed it; only
    sha256(secret) is in the pre-run commit, the secret itself is revealed in results.json.

One trial (`run_trial`), in this order:
  1. the trial's target is the run's secret-keyed draw WITHOUT replacement from POOL; decoys + a
     16-byte salt from the secret-keyed trial stream;
  2. COMMIT: sha256(target_id || salt) goes to the ledger BEFORE the viewer runs;
  3. the viewer sees (trial, commitment) only -- plus the salt ONLY in the planted-leak mutant arm;
  4. its description's sha256 goes to the ledger BEFORE the reveal;
  5. REVEAL: the salt is checked against the commitment (a mismatch raises);
  6. the blind JUDGE gets the description and the 5 candidates' tag sets, shuffled by the secret
     stream, never the commitment, the salt or the target id, and ranks them; rank 1 = a hit.

Arms (all in results.json; the verdict needs every one the right way round):
  F1  null viewer on the real harness                              -> inside chance
  F2  salt planted (SaltMutantViewer)                              -> RED
  F4  seed-reader viewer: real harness -> chance; public-keyed (round-1) harness -> RED
  F5  position-0 judge (a judge-side channel): real harness -> chance; shuffle removed -> RED

Hill-climb (`climb`): a policy change is KEPT only on train-block gain and GRADED only on the
held-out block, both blocks declared in prereg.json before any policy is frozen.

    python3 harness.py secret-new FILE    # 32 random bytes -> FILE (0600); prints sha256 for prereg.json
    python3 harness.py run FILE           # writes results.json (the secret revealed in it)
    python3 harness.py verify             # re-runs from results.json's revealed secret, byte for byte
"""
import hashlib
import json
import math
import os
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
POOL_SIZE = 1000
DECOYS = 4
SALT_BYTES = 16


class Dice:
    """A recorded random stream: sha256(key | label | counter), rejection-sampled, so it is
    identical on every Python build and two labels never share a draw."""

    def __init__(self, key, label):
        self._key = f"{key}|{label}|".encode()
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
    """POOL_SIZE distinct targets, each a sorted tuple of TAGS_PER_TARGET tags (public)."""
    dice, pool, seen = Dice(seed, "pool"), [], set()
    while len(pool) < POOL_SIZE:
        t = tuple(sorted(dice.sample(VOCAB, TAGS_PER_TARGET)))
        if t not in seen:
            seen.add(t)
            pool.append(t)
    return pool


def draw_targets(key, pool, n):
    """n DISTINCT target ids for the whole run (no repeats within or across blocks)."""
    return Dice(key, "targets").sample(range(len(pool)), n)


def commit(target_id, salt):
    return hashlib.sha256(f"{target_id}|".encode() + salt).hexdigest()


def desc_hash(desc):
    return hashlib.sha256(json.dumps(sorted(desc)).encode()).hexdigest()


# ---- viewers: describe(trial, commitment, leak) -> a set of tags --------------------------------

class NullViewer:
    """A seeded RNG with no channel to the target: its stream is keyed on the public seed and
    names only the policy and the trial."""

    def __init__(self, seed, policy=0):
        self.seed, self.policy = seed, policy

    def describe(self, trial, commitment, leak=None):
        return set(Dice(self.seed, f"viewer/null/{self.policy}/{trial}").sample(VOCAB, TAGS_PER_TARGET))


class SaltMutantViewer:
    """MUTANT F2 (must read RED): given the revealed salt early (a planted leak), it opens the
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


class SeedReaderViewer:
    """MUTANT F4: reads the PUBLIC seed (prereg.json) and re-derives the targets as if the harness
    keyed its draws on it.  RED on the public-keyed harness; chance on the secret-keyed one."""

    def __init__(self, seed, pool, n):
        self.pool, self.targets = pool, draw_targets(seed, pool, n)

    def describe(self, trial, commitment, leak=None):
        return set(self.pool[self.targets[trial]])


# ---- judges: (desc, candidates, dice) -> positions, best first ---------------------------------

def judge(desc, candidates, dice):
    """The blind judge: Jaccard overlap with the description; ties by the judge's own stream.
    Takes NOTHING but the description and the candidates."""
    d = set(desc)
    keys = [(-(len(d & set(c)) / len(d | set(c)) if d | set(c) else 0.0), dice.below(1 << 30), i)
            for i, c in enumerate(candidates)]
    return [i for _, _, i in sorted(keys)]


def position0_judge(desc, candidates, dice):
    """MUTANT F5's judge: ignores the description and answers slot 0.  Scores above chance only
    if the harness puts the target in a predictable slot (a judge-side channel)."""
    return list(range(len(candidates)))


# ---- the trial --------------------------------------------------------------------------------

def run_trial(key, pool, targets, viewer, trial, plant_salt=False, ledger=None,
              judge_fn=judge, shuffle=True):
    ledger = [] if ledger is None else ledger
    target = targets[trial]
    td = Dice(key, f"trial/{trial}")
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
    order = [target] + decoys
    if shuffle:
        order = Dice(key, f"shuffle/{trial}").shuffle(order)
    ranking = judge_fn(desc, [pool[t] for t in order], Dice(key, f"judge/{trial}"))
    rank = ranking.index(order.index(target)) + 1
    return {"trial": trial, "commitment": c, "salt": salt.hex(), "target": target,
            "desc_sha256": h, "rank": rank, "hit": rank == 1}


def run_block(key, pool, targets, viewer, trials, **kw):
    return [run_trial(key, pool, targets, viewer, t, **kw) for t in trials]


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


def climb(seed, key, pool, targets, policies, train, held_out):
    """Keep a policy only on train-block gain; grade it only on the held-out block."""
    rates = {p: sum(r["hit"] for r in run_block(key, pool, targets, NullViewer(seed, p), train)) / len(train)
             for p in policies}
    best = max(policies, key=lambda p: (rates[p], -p))
    held = run_block(key, pool, targets, NullViewer(seed, best), held_out)
    return {"policies": len(policies), "baseline_policy": policies[0], "kept_policy": best,
            "baseline_train_rate": rates[policies[0]], "kept_train_rate": rates[best],
            "train_gain": rates[best] - rates[policies[0]], "held_out": held}


def secret_key(secret):
    return "secret/" + secret.hex()


def run(prereg, secret):
    if hashlib.sha256(secret).hexdigest() != prereg["secret_sha256"]:
        raise ValueError("the secret does not match prereg.json's secret_sha256")
    seed, p, a = prereg["seed"], prereg["chance"], prereg["alpha_harness"]
    key, n = secret_key(secret), prereg["n"]
    pool = make_pool(seed)
    targets = draw_targets(key, pool, n)
    pub_targets = draw_targets(seed, pool, n)          # the round-1 (public-keyed) harness, MUTANT F4
    T = list(range(n))
    reader = SeedReaderViewer(seed, pool, n)
    null = run_block(key, pool, targets, NullViewer(seed, 0), T)
    arms = {
        "F1_null": null,
        "F2_salt_planted": run_block(key, pool, targets, SaltMutantViewer(pool), T, plant_salt=True),
        "F4_seed_reader_real": run_block(key, pool, targets, reader, T),
        "F4_seed_reader_public_keyed_harness": run_block(seed, pool, pub_targets, reader, T),
        "F5_position0_judge_real": run_block(key, pool, targets, NullViewer(seed, 0), T,
                                             judge_fn=position0_judge),
        "F5_position0_judge_shuffle_removed": run_block(key, pool, targets, NullViewer(seed, 0), T,
                                                        judge_fn=position0_judge, shuffle=False),
    }
    s = {k: summarize(v, p, a) for k, v in arms.items()}
    must = {"F1_null": True, "F2_salt_planted": False, "F4_seed_reader_real": True,
            "F4_seed_reader_public_keyed_harness": False, "F5_position0_judge_real": True,
            "F5_position0_judge_shuffle_removed": False}
    for k in s:
        s[k]["must_be_inside_chance"] = must[k]
        s[k]["as_required"] = s[k]["inside_chance"] == must[k]
    train, held_out = prereg["train_trials"], prereg["held_out_trials"]
    cl = climb(seed, key, pool, targets, list(range(prereg["climb_policies"])),
               list(range(*train)), list(range(*held_out)))
    cl["held_out"] = summarize(cl["held_out"], p, prereg["alpha_held_out"])
    return {
        "goal": "goal:g5.35", "round": 2,
        "prereg_sha256": hashlib.sha256(PREREG.read_bytes()).hexdigest() if PREREG.exists() else None,
        "seed": seed, "secret_hex_revealed": secret.hex(),
        "pool_sha256": hashlib.sha256(json.dumps(pool).encode()).hexdigest(),
        "distinct_targets": len(set(targets)), "n": n,
        "arms": s, "climb": cl,
        "verdict": "proved" if all(v["as_required"] for v in s.values()) else "disproved",
        "trials": {k: v for k, v in arms.items() if k in ("F1_null", "F2_salt_planted")},
    }


def dump(obj):
    return json.dumps(obj, indent=1, sort_keys=True) + "\n"


def main(argv):
    cmd = argv[1] if len(argv) > 1 else ""
    if cmd == "secret-new":
        path = pathlib.Path(argv[2])
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        secret = os.urandom(32)
        os.write(fd, secret)
        os.close(fd)
        print(hashlib.sha256(secret).hexdigest())
        return 0
    prereg = json.loads(PREREG.read_text())
    if cmd == "run":
        RESULTS.write_text(dump(run(prereg, pathlib.Path(argv[2]).read_bytes())))
    elif cmd == "verify":
        old = RESULTS.read_text()
        same = old == dump(run(prereg, bytes.fromhex(json.loads(old)["secret_hex_revealed"])))
        print("replay: identical" if same else "replay: DIFFERS")
        return 0 if same else 1
    else:
        print(__doc__)
        return 2
    r = json.loads(RESULTS.read_text())
    for k, v in r["arms"].items():
        print(k, {x: v[x] for x in ("hits", "n", "band_hits_lt", "p_one_sided", "inside_chance", "as_required")})
    c = r["climb"]
    print("climb", c["baseline_train_rate"], c["kept_train_rate"], c["train_gain"],
          c["held_out"]["hits"], c["held_out"]["p_one_sided"])
    print("distinct_targets", r["distinct_targets"], "verdict", r["verdict"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
