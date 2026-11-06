"""goal:g5.48 -- the out-of-process harness's own test.  DEV secrets only: the measured secret is made
inside `harness_oop.py run` and never exists before it.

    python3 .agi/context/local-maxxing/rv/test_harness_oop.py
"""
import hashlib
import os
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import harness as h  # noqa: E402
import harness_oop as o  # noqa: E402

PREREG = {"seed": "dev-not-the-measured-seed", "n": 30}
N = 30


class TestOOP(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.run_dir = pathlib.Path(cls.tmp.name)
        cls.secret = hashlib.sha256(b"dev secret").digest()
        cls.sha = hashlib.sha256(cls.secret).hexdigest()
        cls.key = h.secret_key(cls.secret)
        cls.pool = h.make_pool(PREREG["seed"])
        cls.targets = h.draw_targets(cls.key, cls.pool, N)

    @classmethod
    def tearDownClass(cls):
        o.set_dumpable(1)
        cls.tmp.cleanup()

    def arm(self, viewer, **kw):
        rows, proc = o.run_arm(self.key, self.pool, self.targets, viewer, N, **kw)
        return rows, proc, sum(r["hit"] for r in rows)

    def test_fixed_decoys_exclude_every_run_target(self):
        dec = [o.decoys_for(self.key, self.pool, self.targets, t)[0] for t in range(N)]
        self.assertEqual(o.decoy_counts(self.targets, dec)["any_run_target"], 0)
        old = [o.decoys_for(self.key, self.pool, self.targets, t, fixed=False)[0] for t in range(N)]
        self.assertTrue(all(self.targets[t] not in old[t] for t in range(N)))

    def test_viewer_argv_and_env_carry_no_secret(self):
        v = o.ViewerProc("attacker", PREREG, self.sha, self.run_dir)
        self.assertNotIn(self.secret.hex(), " ".join(v.argv))
        self.assertNotIn(self.secret.hex(), " ".join(o.scrubbed_env().values()))
        v.close()

    def test_null_and_salt_out_of_process(self):
        _, p, hits = self.arm(o.ViewerProc("null", PREREG, self.sha, self.run_dir))
        self.assertEqual(p["rc"], 0)
        self.assertLess(hits, N)
        _, p, hits = self.arm(o.ViewerProc("salt", PREREG, self.sha, self.run_dir), plant_salt=True)
        self.assertEqual(hits, N)

    def test_M1_attacker_in_process_reads_the_frame(self):
        rows, _, hits = self.arm(o.InProc(PREREG, self.sha, self.run_dir))
        self.assertEqual(hits, N)
        self.assertEqual({r["channel"] for r in rows}, {"frame"})

    def test_attacker_out_of_process_with_dumpable_0_falls_to_chance(self):
        self.assertEqual(o.set_dumpable(0), 0)
        rows, p, hits = self.arm(o.ViewerProc("attacker", PREREG, self.sha, self.run_dir))
        self.assertEqual(p["rc"], 0)
        self.assertEqual({r["channel"] for r in rows}, {None})
        self.assertTrue(h.summarize(rows, 0.2, 0.01)["inside_chance"])

    def test_M3_attacker_reads_proc_mem_when_dumpable_is_left_1(self):
        if o.ptrace_scope() not in (0, None):
            self.skipTest("ptrace_scope != 0: same-uid /proc/PPID/mem is closed on this box")
        self.assertEqual(o.set_dumpable(1), 1)
        rows, _, hits = self.arm(o.ViewerProc("attacker", PREREG, self.sha, self.run_dir))
        self.assertEqual(hits, N)
        self.assertEqual({r["channel"] for r in rows}, {"mem"})


if __name__ == "__main__":
    unittest.main()
