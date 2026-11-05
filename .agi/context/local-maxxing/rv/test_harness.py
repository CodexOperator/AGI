"""goal:g5.35 -- the harness's own test.  Runs on a DEV seed only: the measured seed in
prereg.json is first used by `harness.py run`, after the pre-run commit.

    python3 .agi/context/local-maxxing/rv/test_harness.py
"""
import inspect
import pathlib
import sys
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import harness as h  # noqa: E402

DEV = "dev-not-the-measured-seed"


class Spy:
    def __init__(self):
        self.calls = []

    def describe(self, trial, commitment, leak=None):
        self.calls.append((trial, commitment, leak))
        return set(h.VOCAB[:h.TAGS_PER_TARGET])


class TestHarness(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pool = h.make_pool(DEV)

    def test_dice_replay_and_separation(self):
        self.assertEqual(h.Dice(DEV, "a").bytes(64), h.Dice(DEV, "a").bytes(64))
        self.assertNotEqual(h.Dice(DEV, "a").bytes(64), h.Dice(DEV, "b").bytes(64))
        d = h.Dice(DEV, "c")
        self.assertTrue(all(0 <= d.below(5) < 5 for _ in range(500)))

    def test_pool_distinct(self):
        self.assertEqual(len(set(self.pool)), h.POOL_SIZE)

    def test_commitment_binds(self):
        salt = h.Dice(DEV, "s").bytes(h.SALT_BYTES)
        c = h.commit(7, salt)
        self.assertEqual(c, h.commit(7, salt))
        self.assertNotEqual(c, h.commit(8, salt))
        self.assertNotEqual(c, h.commit(7, bytes(h.SALT_BYTES)))

    def test_viewer_sees_only_trial_and_commitment(self):
        spy, ledger = Spy(), []
        row = h.run_trial(DEV, self.pool, spy, 3, ledger=ledger)
        (trial, commitment, leak), = spy.calls
        self.assertEqual((trial, leak), (3, None))
        self.assertEqual(commitment, row["commitment"])
        self.assertNotIn(row["salt"], commitment)
        self.assertEqual([e[0] for e in ledger], ["commit", "describe", "reveal"])

    def test_judge_is_blind_by_signature(self):
        self.assertEqual(list(inspect.signature(h.judge).parameters), ["desc", "candidates", "dice"])

    def test_band(self):
        c = h.upper_band(200, 0.2, 0.05)
        self.assertLessEqual(h.binom_sf(c, 200, 0.2), 0.05)
        self.assertGreater(h.binom_sf(c - 1, 200, 0.2), 0.05)
        self.assertAlmostEqual(h.binom_sf(0, 200, 0.2), 1.0)

    def test_null_reads_chance_on_dev_seed(self):
        rows = h.run_block(DEV, self.pool, h.NullViewer(DEV), range(200))
        self.assertTrue(h.summarize(rows, 0.2, 0.05)["inside_chance"])

    def test_mutant_reads_red(self):
        """Falsifier 2: the planted-salt viewer must score ABOVE the band; without the leak it
        has nothing (the leak, not the viewer, is what scores)."""
        m = h.SaltMutantViewer(self.pool)
        leaked = h.summarize(h.run_block(DEV, self.pool, m, range(200), plant_salt=True), 0.2, 0.05)
        self.assertFalse(leaked["inside_chance"])
        self.assertEqual(leaked["hits"], 200)
        blind = h.summarize(h.run_block(DEV, self.pool, m, range(200)), 0.2, 0.05)
        self.assertTrue(blind["inside_chance"])

    def test_replay_byte_for_byte(self):
        a = h.run_block(DEV, self.pool, h.NullViewer(DEV, 2), range(20))
        b = h.run_block(DEV, h.make_pool(DEV), h.NullViewer(DEV, 2), range(20))
        self.assertEqual(h.dump(a), h.dump(b))


if __name__ == "__main__":
    unittest.main()
