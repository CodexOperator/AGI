"""goal:g5.35 -- the harness's own test.  Runs on a DEV seed + DEV key only: the measured secret
is first used by `harness.py run`, after the pre-run commit.

    python3 .agi/context/local-maxxing/rv/test_harness.py
"""
import inspect
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import harness as h  # noqa: E402

DEV = "dev-not-the-measured-seed"
KEY = "dev-key-not-the-measured-secret"
N = 200


class Spy:
    def __init__(self):
        self.calls = []

    def describe(self, trial, commitment, leak=None):
        self.calls.append((trial, commitment, leak))
        return set(h.VOCAB[:h.TAGS_PER_TARGET])


def rate(rows):
    return h.summarize(rows, 0.2, 0.05)


class TestHarness(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pool = h.make_pool(DEV)
        cls.targets = h.draw_targets(KEY, cls.pool, N)

    def block(self, viewer, key=KEY, targets=None, **kw):
        return h.run_block(key, self.pool, self.targets if targets is None else targets, viewer, range(N), **kw)

    def test_dice_replay_and_separation(self):
        self.assertEqual(h.Dice(DEV, "a").bytes(64), h.Dice(DEV, "a").bytes(64))
        self.assertNotEqual(h.Dice(DEV, "a").bytes(64), h.Dice(DEV, "b").bytes(64))
        d = h.Dice(DEV, "c")
        self.assertTrue(all(0 <= d.below(5) < 5 for _ in range(500)))

    def test_pool_distinct_and_targets_never_repeat(self):
        self.assertEqual(len(set(self.pool)), h.POOL_SIZE)
        self.assertEqual(len(set(self.targets)), N)

    def test_commitment_binds(self):
        salt = h.Dice(DEV, "s").bytes(h.SALT_BYTES)
        c = h.commit(7, salt)
        self.assertEqual(c, h.commit(7, salt))
        self.assertNotEqual(c, h.commit(8, salt))
        self.assertNotEqual(c, h.commit(7, bytes(h.SALT_BYTES)))

    def test_viewer_sees_only_trial_and_commitment(self):
        spy, ledger = Spy(), []
        row = h.run_trial(KEY, self.pool, self.targets, spy, 3, ledger=ledger)
        (trial, commitment, leak), = spy.calls
        self.assertEqual((trial, leak), (3, None))
        self.assertEqual(commitment, row["commitment"])
        self.assertEqual([e[0] for e in ledger], ["commit", "describe", "reveal"])

    def test_judge_is_blind_by_signature(self):
        self.assertEqual(list(inspect.signature(h.judge).parameters), ["desc", "candidates", "dice"])

    def test_band(self):
        c = h.upper_band(200, 0.2, 0.05)
        self.assertLessEqual(h.binom_sf(c, 200, 0.2), 0.05)
        self.assertGreater(h.binom_sf(c - 1, 200, 0.2), 0.05)

    def test_F1_null_reads_chance(self):
        self.assertTrue(rate(self.block(h.NullViewer(DEV)))["inside_chance"])

    def test_F2_salt_mutant_reads_red(self):
        m = h.SaltMutantViewer(self.pool)
        self.assertEqual(rate(self.block(m, plant_salt=True))["hits"], N)
        self.assertTrue(rate(self.block(m))["inside_chance"])

    def test_F4_seed_reader_red_on_public_keyed_chance_on_secret_keyed(self):
        r = h.SeedReaderViewer(DEV, self.pool, N)
        pub = h.draw_targets(DEV, self.pool, N)
        self.assertEqual(rate(self.block(r, key=DEV, targets=pub))["hits"], N)
        self.assertTrue(rate(self.block(r))["inside_chance"])

    def test_F5_position0_judge_red_without_shuffle_chance_with_it(self):
        v = h.NullViewer(DEV)
        self.assertEqual(rate(self.block(v, judge_fn=h.position0_judge, shuffle=False))["hits"], N)
        self.assertTrue(rate(self.block(v, judge_fn=h.position0_judge))["inside_chance"])

    def test_run_refuses_a_wrong_secret(self):
        with self.assertRaises(ValueError):
            h.run({"secret_sha256": "0" * 64}, b"x" * 32)

    def test_replay_byte_for_byte(self):
        a = h.run_block(KEY, self.pool, self.targets, h.NullViewer(DEV, 2), range(20))
        b = h.run_block(KEY, h.make_pool(DEV), h.draw_targets(KEY, self.pool, N), h.NullViewer(DEV, 2), range(20))
        self.assertEqual(h.dump(a), h.dump(b))


if __name__ == "__main__":
    unittest.main()
