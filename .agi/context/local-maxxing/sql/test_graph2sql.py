#!/usr/bin/env python3
"""test_graph2sql.py -- real assertions for the SQL mirror.

Run:  python3 .agi/context/local-maxxing/sql/test_graph2sql.py
  or: python3 -m pytest .agi/context/local-maxxing/sql/test_graph2sql.py -q

Proves the hypothesis's five conjuncts: build <= 60 s; round-trip set equality
(exit 0 on match, non-zero on drift); five standing queries each < 50 ms; the
DDL runs unchanged on Postgres 16 in a throwaway docker container; and the
runnable query entry points.
"""
from __future__ import annotations

import os
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import graph2sql as g  # noqa: E402

ROOT = g.find_root(HERE)
NODES = ROOT / ".agi" / "nodes"
QUERY_CASES = [
    ("nodes_by_type_verdict_town", ["hypothesis"]),
    ("nodes_by_type_verdict_town", ["verdict", "proved", "core"]),
    ("children_of", ["goal:g14"]),
    ("evidence_runs_of", ["experiment:a00-217797be-f1590a"]),
    ("notes_with_dates", ["owner"]),
    ("retired_dangling_supersedes", []),
]


class MirrorTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = Path(tempfile.mkdtemp(prefix="g2sql-test-"))
        cls.db = cls.tmp / "nodes.sqlite"
        # ONE frozen file set, taken before the first read. The live node tree moves
        # under the suite (every parallel kid mints nodes while it runs), so a re-glob
        # after the build compares the db against a set that grew mid-run -- the
        # DH.387 `FAIL 127 passed, 1 failed` flake, cause measured in
        # .agi/sessions/iter-DH.393/a00-6f88eaa5/probe_toctou.py, fixed here.
        cls.files = g.iter_files(NODES)
        t0 = time.perf_counter()
        g.build(ROOT, NODES, cls.db, quiet=True, files=cls.files)
        cls.build_s = time.perf_counter() - t0
        cls.con = sqlite3.connect(cls.db)

    @classmethod
    def tearDownClass(cls):
        cls.con.close()
        shutil.rmtree(cls.tmp, ignore_errors=True)

    def test_build_under_60s_and_covers_every_node_file(self):
        self.assertLess(self.build_s, 60.0, f"build took {self.build_s:.1f}s")
        n_files = sum(1 for p in self.files if g.read_node(p, ROOT))
        n_db = self.con.execute("SELECT count(*) FROM nodes").fetchone()[0]
        self.assertEqual(n_files, n_db, "node count differs from the file set")
        self.assertGreater(n_db, 3000, "the whole ~3.5k-node graph should be here")
        retired = self.con.execute("SELECT count(*) FROM nodes WHERE retired=1").fetchone()[0]
        self.assertGreater(retired, 100, "deprecated/ sibling trees must be included")

    def test_verify_roundtrip_exits_0(self):
        self.assertEqual(g.verify(ROOT, NODES, self.db, files=self.files), 0)

    def test_verify_detects_drift(self):
        con = sqlite3.connect(self.db)
        con.execute("DELETE FROM nodes WHERE id=(SELECT id FROM nodes ORDER BY id LIMIT 1)")
        con.commit()
        con.close()
        self.assertNotEqual(g.verify(ROOT, NODES, self.db, files=self.files), 0,
                            "a missing id must fail the check")
        g.build(ROOT, NODES, self.db, quiet=True, files=self.files)  # restore the good file

    def test_five_queries_under_50ms(self):
        self.assertEqual({n for n, _ in QUERY_CASES} - set(g.QUERIES), set())
        for name, args in QUERY_CASES:
            with self.subTest(query=name):
                rows = g.run_query(self.con, name, args)  # warm
                if name == "notes_with_dates":
                    self.assertTrue(all(r[2] for r in rows), "every returned note must carry a date")
                if name != "retired_dangling_supersedes":
                    # this one is empty on today's graph (every supersedes ref resolves);
                    # it is exercised against a synthetic dangling row below.
                    self.assertGreater(len(rows), 0, f"{name} found nothing on the live graph")
                times = []
                for _ in range(10):
                    t = time.perf_counter()
                    g.run_query(self.con, name, args)
                    times.append((time.perf_counter() - t) * 1000.0)
                med = sorted(times)[len(times) // 2]
                self.assertLess(med, 50.0, f"{name} median {med:.1f}ms > 50ms")
                self.assertLess(max(times), 500.0, f"{name} max {max(times):.1f}ms > falsifier 500ms")

    def test_stale_supersedes_query_finds_a_dangling_ref(self):
        db = self.tmp / "dangling.sqlite"
        shutil.copy(self.db, db)
        con = sqlite3.connect(db)
        con.execute("INSERT INTO nodes (id,type,retired,supersedes) "
                    "VALUES ('build:dangling-probe','build',1,'build:does-not-exist')")
        con.commit()
        rows = g.run_query(con, "retired_dangling_supersedes", [])
        con.close()
        self.assertEqual(rows, [("build:dangling-probe", "build:does-not-exist")])

    def test_query_entry_point_is_runnable(self):
        r = subprocess.run([sys.executable, str(HERE / "graph2sql.py"), "query",
                            "children_of", "goal:g14", "--db", str(self.db)],
                           capture_output=True, text=True, timeout=60)
        self.assertEqual(r.returncode, 0, r.stderr[-2000:])
        self.assertGreater(len(r.stdout.strip().splitlines()), 0)

    def test_schema_runs_unchanged_on_postgres16(self):
        if shutil.which("docker") is None:
            self.skipTest("docker unavailable; pglast also absent")
        name = f"g2sql-pg16-{os.getpid()}"
        subprocess.run(["docker", "rm", "-f", name], capture_output=True)
        try:
            subprocess.run(["docker", "run", "-d", "--name", name,
                            "-e", "POSTGRES_HOST_AUTH_METHOD=trust", "postgres:16"],
                           check=True, capture_output=True, timeout=300)
            ready = False
            for _ in range(90):
                if subprocess.run(["docker", "exec", name, "pg_isready", "-U", "postgres"],
                                  capture_output=True).returncode == 0:
                    ready = True
                    break
                time.sleep(1)
            self.assertTrue(ready, "postgres:16 did not become ready")
            ddl = (HERE / "schema.sql").read_text(encoding="utf-8")
            r = subprocess.run(["docker", "exec", "-i", name, "psql", "-U", "postgres",
                                "-d", "postgres", "-v", "ON_ERROR_STOP=1", "-f", "-"],
                               input=ddl, capture_output=True, text=True, timeout=60)
            self.assertEqual(r.returncode, 0, r.stderr[-3000:])
            self.assertIn("CREATE TABLE", r.stdout)
        finally:
            subprocess.run(["docker", "rm", "-f", name], capture_output=True)


if __name__ == "__main__":
    unittest.main(verbosity=2)
