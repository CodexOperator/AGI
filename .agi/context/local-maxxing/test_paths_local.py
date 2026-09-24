"""get_local() anchors repo-relative paths at the checkout that owns the config.

Temp-dir fixtures ONLY: get()'s box.root is deliberately pointed at a DIFFERENT
directory than the one holding .agi/config.json, which is the stale-box-root
trap get_local() exists to close.
"""
import json
import os
import shutil
import tempfile
import unittest

import paths


def _fixture(root, box_root, table=None, extra_box=None):
    os.makedirs(os.path.join(root, ".agi"), exist_ok=True)
    box = {"root": box_root}
    box.update(extra_box or {})
    table = table or {"k": "datasets/x", "abs": box_root}
    with open(os.path.join(root, ".agi", "config.json"), "w", encoding="utf-8") as fh:
        json.dump({"box": box, "paths": {"local_maxxing": table}}, fh)


class TestProposedRoots(unittest.TestCase):
    def test_value_table(self):
        expected = {
            "served_models_dir": "/data/ml/models",
            "served_9b_gguf": "/data/ml/models/Qwen3.5-9B-Q4_K_M.gguf",
            "osc02_scratch_dir": "/data/ml/scratch/osc02",
            "osc02_9b_gguf": "/data/ml/scratch/osc02/Qwen3.5-9B-Q4_K_M.gguf",
            "wikitext2_test_raw": "/data/ml/scratch/osc02/wikitext-2-raw/wiki.test.raw",
            "wikitext2_zip": "/data/ml/scratch/osc02/wikitext-2-raw-v1.zip",
            "osc03_hf_dir": "/data/ml/scratch/osc03/hf",
            "osc03_pylib_dir": "/data/ml/scratch/osc03/pylib",
            "cuda_jit_cache_dir": "/data/ml/scratch/cuda-jit-cache",
            "ml_python": "/data/ml/.venv/bin/python",
            "nsys_dir": "/data/ml/tools/nsight-systems-2026.3.2/opt/nvidia/nsight-systems/2026.3.2",
        }
        self.assertEqual({key: paths.get(key) for key in expected}, expected)


class TestGetLocal(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.checkout = os.path.join(self.tmp, "worktree")
        self.other = os.path.join(self.tmp, "main")
        os.makedirs(self.checkout)
        os.makedirs(self.other)
        _fixture(self.checkout, self.other)
        self._saved_here = paths._HERE
        paths._HERE = os.path.join(self.checkout, ".agi", "context", "local-maxxing")
        os.makedirs(paths._HERE)
        paths._CACHE.clear()

    def tearDown(self):
        paths._HERE = self._saved_here
        shutil.rmtree(self.tmp)
        paths._CACHE.clear()

    def test_local_anchors_at_checkout_not_box_root(self):
        self.assertEqual(paths.get_local("k"), os.path.join(self.checkout, "datasets", "x"))
        self.assertEqual(paths.get("k"), os.path.join(self.other, "datasets", "x"))

    def test_get_is_unchanged_for_absolute_values(self):
        self.assertEqual(paths.get("abs"), self.other)
        self.assertEqual(paths.get_local("abs"), self.other)

    def test_unknown_key_raises(self):
        with self.assertRaises(KeyError):
            paths.get_local("nope")
        with self.assertRaises(KeyError):
            paths.get("nope")

    def test_box_cell_beats_proposed_table(self):
        _fixture(self.checkout, self.other, {"model": "{models_dir}/x"},
                 {"models_dir": "/override"})
        paths._CACHE.clear()
        self.assertEqual(paths.get("model"), "/override/x")

    def test_unresolved_placeholder_raises_named_key_error(self):
        _fixture(self.checkout, self.other, {"bad": "{no_such_root}/x"})
        paths._CACHE.clear()
        for resolve in (paths.get, paths.get_local):
            with self.assertRaisesRegex(KeyError, "no_such_root"):
                resolve("bad")


if __name__ == "__main__":
    unittest.main()
