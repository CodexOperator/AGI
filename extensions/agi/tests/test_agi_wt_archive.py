"""G8: a moved claimed tree is archived to refs/archive/wt before agi-wt drop exits 4."""
import os, re, shutil, subprocess
from pathlib import Path

GEO = Path(__file__).resolve().parents[3] / ".agi/nodes/.geometry"
MAIL = "a" + chr(64) + "t.invalid"
NODE = "---\nid: doc:t1\nmint_id: m1\n---\nbody\n"


def piece(name):
    t = (GEO / "engine-post.md").read_text()
    m = re.search(rf"^### {name} .*?\n~~~\w*\n(.*?)^~~~", t, re.S | re.M)
    return m[1]


def setup(tmp_path):
    home, rt = tmp_path / "home", tmp_path / "rt"
    (tmp_path / "bin").mkdir(), rt.mkdir()
    (home / "t/.agi/nodes").mkdir(parents=True)
    (tmp_path / "bin/agi-wt").write_text(piece("agi-wt"))
    (tmp_path / "bin/agi-wt").chmod(0o755)
    env = dict(os.environ, HOME=str(home), RUNTIME_DIRECTORY=str(rt), AGI_SEAT="p1", AGI_WT_HOLD="101",
               PATH=f"{tmp_path/'bin'}:{os.environ['PATH']}", GIT_AUTHOR_NAME="a", GIT_AUTHOR_EMAIL=MAIL,
               GIT_COMMITTER_NAME="a", GIT_COMMITTER_EMAIL=MAIL, GIT_CONFIG_GLOBAL="/dev/null")
    t = home / "t"
    g = lambda *a, **k: subprocess.run(a, cwd=t, env=env, capture_output=True, text=True, **k)
    g("git", "init", "-q"), (t / ".agi/nodes/n.md").write_text(NODE)
    g("git", "add", "-A"), g("git", "commit", "-qm", "base")
    d = Path(g("agi-wt", "pull", "doc:t1").stdout.strip())
    return g, t, rt, d


def test_f1_moved_tree_archived_and_survives_stop(tmp_path):
    g, t, rt, d = setup(tmp_path)
    (d / ".agi/nodes/n.md").write_text(NODE + "edited\n")
    (t / ".agi/nodes/n.md").write_text(NODE + "trunk\n")
    g("git", "commit", "-qam", "move")
    r = g("agi-wt", "drop", "doc:t1")
    assert r.returncode == 4 and "moved" in r.stdout
    ref = "refs/archive/wt/p1/m1"
    assert g("git", "show", f"{ref}:.agi/nodes/n.md").stdout == NODE + "edited\n"
    assert g("git", "status", "--porcelain", "--", ".agi").stdout.strip() == ""
    shutil.rmtree(rt)
    assert g("git", "show", f"{ref}:.agi/nodes/n.md").stdout == NODE + "edited\n"


def test_f2_clean_tree_drops_as_today(tmp_path):
    g, t, rt, d = setup(tmp_path)
    (d / ".agi/nodes/n.md").write_text(NODE + "edited\n")
    assert g("agi-wt", "drop", "doc:t1").returncode == 0 and not d.exists()
    assert g("git", "show", "HEAD:.agi/nodes/n.md").stdout == NODE + "edited\n"
    assert g("git", "for-each-ref", "refs/archive").stdout == ""


def test_f3_unit_keeps_runtime_dir_across_restart():
    u = (GEO / "engine-root.md").read_text()
    assert "RuntimeDirectory=agi-%i\nRuntimeDirectoryPreserve=restart\n" in u
