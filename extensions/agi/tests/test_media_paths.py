"""goal:g5.4.2 (council 10-21 16:24Z): the media code runs from ANY checkout, as any uid. Nothing in it may point into a post's home (director-review cannot read agi-director-general-3's, which is renamed anyway).
The needles are built from pieces so this file does not contain what it forbids."""
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import media_base  # noqa: E402
HOME_NEEDLES = ("/var/lib/" + "agi/", "w-" + "sg", "~" + "/")      # a post's home, the worktree name, a bare home-relative path
FILES = sorted(HERE.glob("media_*.py")) + sorted(HERE.glob("test_media_*.py"))
BASE_FILE = HERE / "media_base.py"


def post_names():
    """Every post name that starts with `director-` in the real posts.md (the shuffle reuses them), plus the fixed prefixes, so a name typed into a media file turns this RED."""
    import re
    names = {"director-" + "general-", "director-" + "science-", "director-" + "goals-", "director-" + "review", "dg" + "3-media"}
    posts = HERE.parents[2] / ".agi" / "nodes" / ".geometry" / "posts.md"
    if posts.exists():
        names |= set(re.findall(r'"name": "(director-[a-z0-9-]+)"', posts.read_text()))
    return names


def test_no_media_file_points_into_a_posts_home():
    hits = [(f.name, n) for f in FILES for n in HOME_NEEDLES if n in f.read_text() and f.name != "test_media_paths.py"]
    assert hits == [], hits


def test_no_media_file_names_a_post():
    """council 18:02Z 10-21: the data dir was named for a post (the shuffle reuses post names); no media file may name one again, not even in a comment or a README line it writes."""
    hits = [(f.name, n) for f in FILES for n in sorted(post_names()) if n in f.read_text() and f.name != "test_media_paths.py"]
    assert hits == [], hits


def test_the_data_dir_is_typed_in_exactly_one_module():
    """BASE lives in media_base.py; no other media file types a data dir (a path under the data root)."""
    needle = "/data/" + "work/"
    hits = [f.name for f in FILES if needle in f.read_text() and f != BASE_FILE and f.name != "test_media_paths.py"]
    assert hits == [] and needle in BASE_FILE.read_text()


def test_base_comes_from_the_env_in_every_module_that_uses_it(tmp_path):
    code = ("sys.argv = ['walk.py', '--dry']\n"
            "import media_base, media_video, media_music, media_mutate, test_media_html\n"
            "print(media_base.BASE, media_video.BASE, media_music.BASE, media_mutate.BASE, test_media_html.BASE)")
    d = tmp_path / "extensions" / "agi" / "tests"
    d.mkdir(parents=True)
    for f in list(HERE.glob("media_*.py")) + [HERE / "test_media_html.py"]:
        shutil.copy(f, d / f.name)
    env = dict(os.environ, MEDIA_BASE="/some/data/dir")
    env.pop("MEDIA_REPO", None)
    r = subprocess.run([sys.executable, "-B", "-c", "import sys; sys.path.insert(0, %r)\n%s" % (str(d), code)], cwd="/", env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-500:]
    assert r.stdout.split() == ["/some/data/dir"] * 5
    env.pop("MEDIA_BASE")
    r = subprocess.run([sys.executable, "-B", "-c", "import sys; sys.path.insert(0, %r)\nimport media_base; print(media_base.BASE, media_base.QUEUE_DIR)" % str(d)], cwd="/", env=env, capture_output=True, text=True)
    assert r.stdout.split() == ["/data/work/media/season3", "/data/work/media"]                  # the default names the WORK, not a post


def run_in_copy(tmp_path, code, env_extra=None):
    """Copy the media files into <tmp>/extensions/agi/tests (a stand-in checkout, no git) and run `code` there from an unrelated cwd."""
    d = tmp_path / "extensions" / "agi" / "tests"
    d.mkdir(parents=True)
    for f in HERE.glob("media_*.py"):
        shutil.copy(f, d / f.name)
    env = {k: v for k, v in os.environ.items() if k != "MEDIA_REPO"}
    env["MEDIA_BASE"] = media_base.BASE
    env.update(env_extra or {})
    r = subprocess.run([sys.executable, "-B", "-c", "import sys; sys.path.insert(0, %r)\n%s" % (str(d), code)], cwd="/", env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-600:]
    return r.stdout.strip()


def test_media_video_repo_is_the_checkout_that_holds_the_file_and_env_overrides(tmp_path):
    assert run_in_copy(tmp_path, "import media_video; print(media_video.REPO)") == str(tmp_path)
    assert run_in_copy(tmp_path / "x", "import media_video; print(media_video.REPO)", {"MEDIA_REPO": "/some/other/checkout"}) == "/some/other/checkout"
    assert run_in_copy(tmp_path / "y", "import media_video; print(media_video.SCRIPT)") == str(tmp_path / "y") + "/.agi/context/media/season3-explainer-script.md"


def test_media_walk_repo_and_import_path_are_the_checkout_that_holds_the_file(tmp_path):
    media_base.need(media_base.BASE + "/r2/r3/description.txt", "the walk's voice description")
    assert run_in_copy(tmp_path, "sys.argv = ['walk.py', '--dry']\nimport media_walk; print(media_walk.REPO)") == str(tmp_path)
    assert run_in_copy(tmp_path / "z", "sys.argv = ['walk.py', '--dry']\nimport media_walk; print(media_walk.REPO)", {"MEDIA_REPO": "/elsewhere"}) == "/elsewhere"


def test_a_copy_of_the_walk_elsewhere_finds_its_helpers_through_media_repo(tmp_path):
    """season3/walk/walk.py is a COPY run from the data dir: with MEDIA_REPO set it imports the checkout's helpers; the harness's own path entry is removed first."""
    media_base.need(media_base.BASE + "/r2/r3/description.txt", "the walk's voice description")
    d = tmp_path / "extensions" / "agi" / "tests"
    d.mkdir(parents=True)
    for f in HERE.glob("media_*.py"):
        shutil.copy(f, d / f.name)
    lone = tmp_path / "walkcopy"
    lone.mkdir()
    shutil.copy(HERE / "media_walk.py", lone / "walk.py")
    env = dict(os.environ, MEDIA_REPO=str(tmp_path), MEDIA_BASE=media_base.BASE)
    r = subprocess.run([sys.executable, "-B", "-c", "import sys; sys.argv=['walk.py','--dry']; sys.path.insert(0, %r)\nimport walk; print(walk.REPO, sys.path[0])" % str(lone)], cwd="/", env=env, capture_output=True, text=True)
    assert r.returncode == 0, r.stderr[-500:]
    assert r.stdout.strip() == f"{tmp_path} {tmp_path}/extensions/agi/tests"
    env.pop("MEDIA_REPO")
    r2 = subprocess.run([sys.executable, "-B", "-c", "import sys; sys.argv=['walk.py','--dry']; sys.path.insert(0, %r)\nimport walk" % str(lone)], cwd="/", env=env, capture_output=True, text=True)
    assert r2.returncode != 0                                                                       # a copy with no MEDIA_REPO does not guess: it fails loud
