"""G8: a moved claimed tree is archived to the flat ref refs/archive/worktrees/<post>@<mint> before agi-wt drop exits 4."""
import os, re, shutil, subprocess
from pathlib import Path

GEO = Path(__file__).resolve().parents[3] / ".agi/nodes/.geometry"
MAIL = "a" + chr(64) + "t.invalid"
NODE = "---\nid: doc:t1\nmint_id: m1\n---\nbody\n"


def piece(name):
    t = (GEO / "engine-post.md").read_text()
    m = re.search(rf"^### {name} .*?\n~~~\w*\n(.*?)^~~~", t, re.S | re.M)
    return m[1]


def setup(tmp_path, **ev):
    home, rt = tmp_path / "home", tmp_path / "rt"
    rt.mkdir(parents=True), (tmp_path / "bin").mkdir()
    (home / "t/.agi/nodes").mkdir(parents=True)
    for n in ("agi-wt", "agi-flush", "agi-turn", "agi-link"):
        (tmp_path / "bin" / n).write_text(piece(n))
        (tmp_path / "bin" / n).chmod(0o755)
    env = dict(os.environ, HOME=str(home), RUNTIME_DIRECTORY=str(rt), AGI_SEAT="p1", AGI_WT_HOLD="101", USER="u1",
               PATH=f"{tmp_path/'bin'}:{os.environ['PATH']}", GIT_AUTHOR_NAME="a", GIT_AUTHOR_EMAIL=MAIL,
               GIT_COMMITTER_NAME="a", GIT_COMMITTER_EMAIL=MAIL, GIT_CONFIG_GLOBAL="/dev/null")
    env = {k: v for k, v in {**env, **ev}.items() if v is not None}
    t = home / "t"
    g = lambda *a, **k: subprocess.run(a, cwd=t, env=env, capture_output=True, text=True, **k)
    g("git", "init", "-q"), (t / ".agi/nodes/n.md").write_text(NODE)
    g("git", "add", "-A"), g("git", "commit", "-qm", "base")
    d = Path(g("agi-wt", "pull", "doc:t1").stdout.strip())
    return g, t, rt, d


def move(g, t, d):
    (d / ".agi/nodes/n.md").write_text(NODE + "edited\n")
    (t / ".agi/nodes/n.md").write_text(NODE + "trunk\n")
    g("git", "commit", "-qam", "move")


def lock(t, ref):  # a pre-existing <ref>.lock: git cannot write the archive ref
    (t / ".git" / ref).parent.mkdir(parents=True, exist_ok=True), (t / ".git" / f"{ref}.lock").write_text("")


def test_f1_moved_tree_archived_and_survives_stop(tmp_path):
    g, t, rt, d = setup(tmp_path)
    move(g, t, d)
    r = g("agi-wt", "drop", "doc:t1")
    assert r.returncode == 4 and "moved" in r.stdout
    ref = "refs/archive/worktrees/p1@m1"
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


def test_r1_failed_archive_is_loud_and_not_4(tmp_path):
    g, t, rt, d = setup(tmp_path)
    move(g, t, d)
    lock(t, "refs/archive/worktrees/p1@m1")
    r = g("agi-wt", "drop", "doc:t1")
    assert r.returncode == 5 and "agi-wt: archive of doc:t1 failed" in r.stderr and "moved" not in r.stdout


def test_r2_one_namespace_with_heal():
    m = re.search(r'^SWEEP_ARCHIVE_NS = "([^"]+)"', (GEO.parents[2] / "extensions/agi/bin/heal.py").read_text(), re.M)
    assert m, "heal.py no longer spells SWEEP_ARCHIVE_NS = \"...\" -- re-pin the namespace"
    assert f"update-ref {m[1]}$s@" in piece("agi-wt")


def test_m1_identity_post_wins_and_none_refuses(tmp_path):
    g, t, rt, d = setup(tmp_path / "a", AGI_POST="p2")
    move(g, t, d)
    assert g("agi-wt", "drop", "doc:t1").returncode == 4
    assert g("git", "for-each-ref", "refs/archive").stdout.split()[-1] == "refs/archive/worktrees/p2@m1"  # flat: no slash after the namespace
    g, t, rt, d = setup(tmp_path / "b", AGI_SEAT=None, AGI_POST=None)
    move(g, t, d)
    r = g("agi-wt", "drop", "doc:t1")
    assert r.returncode == 5 and "no AGI_POST/AGI_SEAT" in r.stderr and g("git", "for-each-ref", "refs/archive").stdout == ""


def test_m3_agi_flush_archives_moved_tree_end_to_end(tmp_path):
    g, t, rt, d = setup(tmp_path)
    move(g, t, d)
    assert g("agi-flush").returncode == 0
    assert g("git", "show", "refs/archive/worktrees/p1@m1:.agi/nodes/n.md").stdout == NODE + "edited\n"


def test_g83_agi_flush_exits_5_when_a_drop_exits_5(tmp_path):
    g, t, rt, d = setup(tmp_path)
    move(g, t, d)
    lock(t, "refs/archive/worktrees/p1@m1")
    r = g("agi-flush")
    assert r.returncode == 5 and "agi-wt: archive of m1 failed" in r.stderr and d.exists()
