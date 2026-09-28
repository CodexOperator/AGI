#!/usr/bin/env python3
"""A node that VANISHES after the snapshot is named, not raised on.

Parent probe (DH.393, a00-2c72092b), measured on a fake root:
    old re-glob discipline  -> verify returns 1, prints a clean `1 EXTRA id` DRIFT
    frozen snapshot seam    -> verify RAISES FileNotFoundError: .../n7.md
`read_node` had no vanished-path arm, and `build`/`file_sets` each iterated the
frozen list themselves, so the two stages could not agree on the vanish.

This pins the fixed discipline: ONE read point (`read_all`), the vanish skipped,
counted and NAMED once; verify still returns an int and still goes red with a reason;
and the drift check is NOT blinded -- a content change to a path that is still there
is still caught with the frozen seam.
"""
from __future__ import annotations

import io
import contextlib
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import graph2sql as g  # noqa: E402


class VanishedNode(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="g2sql-vanish-"))
        self.nodes = self.root / ".agi" / "nodes"
        self.nodes.mkdir(parents=True)
        (self.root / ".agi" / "config.json").write_text("{}", encoding="utf-8")
        for i in range(8):
            (self.nodes / f"n{i}.md").write_text(
                f"---\nid: hypothesis:van-{i}\ntype: hypothesis\n---\nbody {i}\n",
                encoding="utf-8")
        self.db = self.root / "nodes.sqlite"
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)

    def _build(self, files=None):
        return g.build(self.root, self.nodes, self.db, quiet=True, files=files)

    def _verify(self, files=None):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            rc = g.verify(self.root, self.nodes, self.db, files=files)
        return rc, out.getvalue()

    # falsifier 1 -- frozen seam, node deleted between build and verify
    def test_frozen_seam_names_the_vanished_path_instead_of_raising(self):
        files = g.iter_files(self.nodes)             # frozen ONCE
        self._build(files)
        (self.nodes / "n7.md").unlink()               # ... and then it is gone
        rc, out = self._verify(files=files)          # MUST NOT raise
        self.assertIsInstance(rc, int)
        self.assertIn("n7.md", out, "the vanished path must be named")
        self.assertIn("VANISHED", out)
        self.assertEqual(rc, 1, "a vanished node is real drift, not a pass")

    # falsifier 2 -- the default (files=None) discipline keeps its clean DRIFT
    def test_default_discipline_still_reports_a_clean_named_drift(self):
        self._build()                                # re-globs
        (self.nodes / "n7.md").unlink()
        rc, out = self._verify()
        self.assertEqual(rc, 1)
        self.assertIn("EXTRA id: hypothesis:van-7", out)
        self.assertNotIn("Traceback", out)

    # falsifier 3 -- the fix must NOT blind the drift check under the frozen seam
    def test_content_drift_is_still_detected_with_the_frozen_seam(self):
        files = g.iter_files(self.nodes)
        self._build(files)
        (self.nodes / "n3.md").write_text(
            "---\nid: hypothesis:van-3-edited\ntype: hypothesis\n---\nbody 3\n",
            encoding="utf-8")                        # path still present, content not
        rc, out = self._verify(files=files)
        self.assertEqual(rc, 1, "a frozen list must still see a content change")
        self.assertIn("EXTRA id: hypothesis:van-3", out)
        self.assertIn("MISSING id: hypothesis:van-3-edited", out)

    # the near miss: the vanish is skipped AND the counts still agree with the db
    def test_counts_agree_after_a_vanish_and_the_build_says_so(self):
        files = g.iter_files(self.nodes)
        n_nodes, _n_edges, n_files = self._build(files)
        (self.nodes / "n7.md").unlink()
        live, vanished = g.read_all(self.root, self.nodes, files=files)
        self.assertEqual([p.name for p in vanished], ["n7.md"])
        n_live = sum(1 for _p, parsed in live if parsed is not None)
        self.assertEqual(n_live, n_files - 1, "one vanish, counted once")
        self.assertEqual(n_nodes, n_files)


if __name__ == "__main__":
    unittest.main(verbosity=2)
