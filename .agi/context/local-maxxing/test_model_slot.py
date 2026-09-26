"""model_slot.py: the one-model slot is exclusive box-wide and gates on MemAvailable inside the lock."""
import os, subprocess, sys, time, unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import model_slot  # noqa: E402
import paths  # noqa: E402

SLOT = os.path.join(HERE, "model_slot.py")


class ModelSlot(unittest.TestCase):
    def test_lock_resolves_to_the_main_checkout_not_this_worktree(self):
        self.assertTrue(model_slot.lock_path().startswith(paths.main_checkout_root() + os.sep))

    def test_floor_is_a_config_cell(self):
        self.assertEqual(model_slot.min_avail_gib(), 3.0)

    def test_memory_gate_waits_then_passes(self):
        reads = iter([1.0, 2.0, 3.5])
        self.assertTrue(model_slot.wait_for_memory(3.0, 100, 1, read=lambda: next(reads), sleep=lambda s: None))

    def test_memory_gate_gives_up_after_wait(self):
        t = [0.0]
        def sleep(s): t[0] += s
        self.assertFalse(model_slot.wait_for_memory(3.0, 5, 1, read=lambda: 1.0, sleep=sleep, clock=lambda: t[0]))

    def test_meminfo_parse(self):
        self.assertGreater(model_slot.mem_available_gib(), 0.0)

    def test_two_holders_never_overlap(self):
        """Two wrapped commands that each record start/end never interleave."""
        log = os.path.join(os.environ.get("TMPDIR", "/tmp"), "model-slot-test-%d.log" % os.getpid())
        body = "import time,sys; open(sys.argv[1],'a').write('S\\n'); time.sleep(0.6); open(sys.argv[1],'a').write('E\\n')"
        cmd = [sys.executable, SLOT, "--wait", "0", "--", sys.executable, "-c", body, log]
        try:
            ps = [subprocess.Popen(cmd, stderr=subprocess.DEVNULL) for _ in range(2)]
            codes = [p.wait(timeout=30) for p in ps]
            if model_slot.mem_available_gib() < model_slot.min_avail_gib():
                self.skipTest("box below the memory floor; gate refused as designed")
            self.assertEqual(codes, [0, 0])
            self.assertEqual(open(log).read().split(), ["S", "E", "S", "E"])
        finally:
            if os.path.exists(log):
                os.remove(log)


if __name__ == "__main__":
    unittest.main()
