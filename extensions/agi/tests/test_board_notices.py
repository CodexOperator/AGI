"""goal:g7.16.1.11.46.12 (council 05:47-05:49Z 10-24, F-a..F-f): THE ROW THAT SETTLES IT. The board cron replays
`board_job.py commit --main <MAIN> --work <fresh clone --shared> -- <writer>`; the writer's cell must carry the SAME notices
segment as `prereq_notice.py line --repo <MAIN>`: trunk, seen and the goal tree are read from MAIN, never from the clone.

Real git + the REAL board_job.py and success_metrics.make_line (only the metrics.py subprocess is stubbed: it is not under test).
A writer pointed at the CLONE's own refs (@WROOT@ instead of MAIN) must read a NAMED red, never `red=none`.
"""
from __future__ import annotations

import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from .test_board_job import SUBJECT, Box

BIN = Path(__file__).resolve().parents[1] / "bin"
CRONS = Path(__file__).resolve().parents[3] / ".agi" / "nodes" / ".geometry" / "crons.md"
REAL_ENGINE_POST = Path(__file__).resolve().parents[3] / ".agi" / "nodes" / ".geometry" / "engine-post.md"
TRUNK = "core/season3/main"

pytestmark = pytest.mark.skipif(not shutil.which("ssh-keygen"), reason="ssh-keygen is needed to sign")

STUB = """
import sys
from pathlib import Path
sys.path.insert(0, {bin!r})
import success_metrics as s
s._run_metrics_once = lambda root: ({{}}, "stub")
print(s.make_line(Path(sys.argv[1])))
"""

LEAF = ("---\nid: goal:{n}\nmint_id: {m:032x}\ntype: goal\nstatus: active\nparents:\n  - goal:g1\n---\n\n## Agent Notes\n"
        "Assigned to **director-goals-1**.\n")
POSTS = ("---\nid: config:posts\nmint_id: 00000000000000000000000000000005\ntype: config\n---\nposts:\n"
         '  - {"name": "belam", "parent": "owner", "harness": "claude-code"}\n'
         '  - {"name": "sanctuary-master", "parent": "belam", "harness": "claude-code"}\n'
         '  - {"name": "director-goals-1", "parent": "sanctuary-master", "harness": "claude-code"}\n')


def box_piece() -> str:
    txt = REAL_ENGINE_POST.read_text()
    m = re.search(r"^### box \(.*?\n~~~sh\n.*?\n~~~\n", txt, re.S | re.M)
    assert m, "the box piece of engine-post.md is missing"
    return m.group(0)


@pytest.fixture
def fx(tmp_path):
    """MAIN = a Box (HEAD on `trunk`) PLUS the notices trunk branch core/season3/main carrying goal files, the geometry, and refs/notices/prereq/seen."""
    b = Box(tmp_path)
    wt = tmp_path / "trunkwt"
    assert b.g("worktree", "add", "-q", "-b", TRUNK, str(wt), "trunk").returncode == 0
    (wt / ".agi/nodes/goal").mkdir(parents=True)
    (wt / ".agi/nodes/.geometry").mkdir(parents=True)
    for i in (1, 2, 3):
        (wt / f".agi/nodes/goal/g{i}.md").write_text(LEAF.format(n=f"g{i}", m=i))
    (wt / ".agi/nodes/.geometry/posts.md").write_text(POSTS)
    (wt / ".agi/nodes/.geometry/engine-post.md").write_text(box_piece())
    b.g("add", "-A", cwd=wt)
    tip = b.commit("trunk: three claimed leaves", cwd=wt)
    b.g("worktree", "remove", "--force", str(wt))
    assert b.g("update-ref", "refs/notices/prereq/seen", tip).returncode == 0
    b.trunk_tip = tip
    return b


def line_main(b: Box) -> str:
    r = subprocess.run([sys.executable, str(BIN / "prereq_notice.py"), "line", "--repo", str(b.main)], capture_output=True, text=True)
    assert r.returncode == 0, r.stderr
    return r.stdout.strip()


def writer(b: Box, root: str) -> list[str]:
    """the cron's writer, reduced to what is under test: print make_line(<root>) into the cell and make ONE commit with the exact subject."""
    code = STUB.format(bin=str(BIN))
    script = (f"{sys.executable} -c {shlex.quote(code)} {shlex.quote(root)} > .agi/cell.txt && git add -A && "
              f'git commit -q -m "{SUBJECT}"')
    return ["sh", "-c", script]


def cell_segment(b: Box) -> str:
    text = b.g("show", f"{b.tip()}:.agi/cell.txt").stdout
    m = re.search(r"\| (notices: .*)$", text.strip().splitlines()[-1])
    assert m, f"no notices segment in the cell: {text[:300]!r}"
    return m.group(1)


def test_the_cron_row_reads_the_segment_from_main_not_from_the_clone():
    row = [ln for ln in CRONS.read_text().splitlines() if "board_job.py commit" in ln and "metrics_cell" in ln]
    assert row, "the metrics_cell cron row is missing from crons.md"
    assert "success_metrics.py --line {root}" in row[0] and "--line @WROOT@" not in row[0], row[0][-160:]


def test_the_cells_notices_segment_equals_line_repo_main(fx):
    want = line_main(fx)
    assert re.search(r"claims=3 ", want) and "lag=0" in want, want
    got = fx.job(writer=writer(fx, str(fx.main / ".agi")))
    assert got.returncode == 0, got.stdout + got.stderr
    assert cell_segment(fx) == want
    assert fx.sig(fx.tip()) == "G"


def test_a_writer_pointed_at_the_clones_own_refs_reads_a_named_red_never_none(fx):
    got = fx.job(writer=writer(fx, "@WROOT@"))
    assert got.returncode == 0, got.stdout + got.stderr
    seg = cell_segment(fx)
    assert "red=none" not in seg, seg
    assert "trunk-unresolved" in seg and "seen-unresolved" in seg, seg      # the clone has neither the trunk branch nor refs/notices/*
    assert seg != line_main(fx)
