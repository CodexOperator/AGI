#!/usr/bin/env python3
"""Regression for the DH.387 `.agi/context` flake, cause MEASURED not guessed.

The flake: `test_build_under_60s_and_covers_every_node_file` / `test_verify_roundtrip_exits_0`
in test_graph2sql.py re-globbed the live node tree AFTER building the mirror. On a live
graph other agents write nodes while the suite runs, so the db and the re-glob are two
different sets and the run goes red once in five, with no name and no cause.

This test pins the fixed discipline: ONE file set, frozen before the first read, used by
build, by the count assertion and by verify. A node minted mid-pass must not break it.
Runs on a throwaway fake root, so it costs milliseconds and touches no repo state.
"""
from __future__ import annotations

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import graph2sql as g  # noqa: E402


class SnapshotDiscipline(unittest.TestCase):
    def setUp(self):
        self.root = Path(tempfile.mkdtemp(prefix="g2sql-snap-"))
        self.nodes = self.root / ".agi" / "nodes"
        self.nodes.mkdir(parents=True)
        (self.root / ".agi" / "config.json").write_text("{}", encoding="utf-8")
        for i in range(20):
            (self.nodes / f"n{i}.md").write_text(
                f"---\nid: hypothesis:snap-{i}\ntype: hypothesis\n---\nbody {i}\n", encoding="utf-8")
        self.db = self.root / "nodes.sqlite"
        self.addCleanup(shutil.rmtree, self.root, ignore_errors=True)

    def _mint_mid_pass(self):
        """A parallel kid mints a node after the file set was frozen."""
        (self.nodes / "zz-concurrent.md").write_text(
            "---\nid: hypothesis:snap-concurrent\ntype: hypothesis\n---\nminted mid-pass\n",
            encoding="utf-8")

    def test_frozen_file_set_survives_a_concurrent_mint(self):
        files = g.iter_files(self.nodes)          # frozen ONCE
        g.build(self.root, self.nodes, self.db, quiet=True, files=files)
        self._mint_mid_pass()
        n_files = sum(1 for p in files if g.read_node(p, self.root))
        n_db = g.sqlite3.connect(self.db).execute("SELECT count(*) FROM nodes").fetchone()[0]
        self.assertEqual(n_files, n_db, "the db and the frozen set must be the same set")
        self.assertEqual(g.verify(self.root, self.nodes, self.db, files=files), 0)

    def test_the_old_re_glob_is_what_broke_it(self):
        """The un-fixed discipline fails on the same input: the flake's cause, pinned."""
        g.build(self.root, self.nodes, self.db, quiet=True)   # no files= : re-globs
        self._mint_mid_pass()
        n_files = sum(1 for p in g.iter_files(self.nodes) if g.read_node(p, self.root))
        n_db = g.sqlite3.connect(self.db).execute("SELECT count(*) FROM nodes").fetchone()[0]
        self.assertNotEqual(n_files, n_db, "re-globbing after the build IS the flake")


if __name__ == "__main__":
    unittest.main(verbosity=2)
