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


def _fixture(root, box_root):
    os.makedirs(os.path.join(root, ".agi"), exist_ok=True)
    with open(os.path.join(root, ".agi", "config.json"), "w", encoding="utf-8") as fh:
        json.dump({"box": {"root": box_root},
                   "paths": {"local_maxxing": {"k": "datasets/x",
                                               "abs": box_root}}}, fh)


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


if __name__ == "__main__":
    unittest.main()
