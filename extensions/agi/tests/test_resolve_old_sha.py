"""hypothesis:g133 — resolve_old_sha: the ONE pre-rewrite commit-id resolver.

Every value here is SYNTHETIC (fake 40-hex old ids, tmp git repos, a tmp config
naming a tmp map, a fixture user under a conventional home root joined at
runtime). The real map and every real pre-rewrite id are never read by this file,
and no real box path is printed.

Falsifiers: F1 mapped, F2 silent-None, F3 the `sha` subcommand's output shape and
its refusal by name, F4 no map path literal in the code, F5 a dropped commit is
not a commit, F6 the hex gate, F7 the write.py WARN (create path, added text only).
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[3]
BIN = REPO / "extensions/agi/bin"
SRC = REPO / "extensions/agi/src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import links  # noqa: E402
import write as w  # noqa: E402

OLD_A = "a" * 40          # synthetic pre-rewrite id
OLD_B = "b" * 40
OLD_C = "c" * 40
SHARED = "deadbeef"       # two rows share this prefix -> ambiguous
#: a home-rooted path, JOINED at runtime: no home path value is ever committed
HOME = "/" + "home/" + "someuser"


def _git_head(d: Path) -> str:
    """Make `d` a git repo with one commit; return its full id."""
    env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
           "PATH": "/usr/bin:/bin", "HOME": str(d)}
    subprocess.run(["git", "init", "-q", str(d)], check=True, env=env)
    (d / "f").write_text("x\n")
    subprocess.run(["git", "-C", str(d), "add", "f"], check=True, env=env)
    subprocess.run(["git", "-C", str(d), "commit", "-qm", "c"], check=True, env=env)
    return subprocess.run(["git", "-C", str(d), "rev-parse", "HEAD"], check=True,
                          capture_output=True, text=True, env=env).stdout.strip()


def _project(tmp_path: Path, map_rows: list[str] | None, *, cell: bool = True,
             git: bool = False) -> Path:
    """A tmp `.agi/` project whose config names a tmp map (or does not)."""
    proj = tmp_path / "proj"
    agi = proj / ".agi"
    (agi / "nodes" / "idea").mkdir(parents=True)
    (agi / "nodes" / "idea" / "i1.md").write_text(
        "---\nid: idea:i1\ntype: idea\n---\n\nbody\n")
    shutil.copytree(REPO / ".agi/context/schemas", agi / "context/schemas")
    cfg = {"paths": {"local_maxxing": {}}}
    if cell:
        cfg["paths"]["local_maxxing"]["scrub_commit_map"] = ".agi/scrub/m.tsv"
        (agi / "scrub").mkdir()
        (agi / "scrub" / "m.tsv").write_text("".join(r + "\n" for r in (map_rows or [])))
    (agi / "config.json").write_text(json.dumps(cfg))
    if git:
        _git_head(proj)
    return proj


def test_f1_known_commit_answers_full_id(tmp_path):
    proj = _project(tmp_path, None, git=True)
    head = links._git_commit(proj, "HEAD")
    assert head and links.resolve_old_sha(proj, head[:12]) == head


def test_f1_mapped_prefix_answers_the_rewritten_id(tmp_path):
    proj = _project(tmp_path, None, git=True)
    head = links._git_commit(proj, "HEAD")
    (proj / ".agi/scrub/m.tsv").write_text(f"{OLD_A}\t{head}\n")
    assert links.resolve_old_sha(proj, OLD_A[:9]) == head
    assert links.resolve_old_sha(proj, OLD_A) == head


@pytest.mark.parametrize("rows,cell", [
    ([], True),                      # cell present, map empty -> unknown
    ([f"{OLD_B}\t{OLD_C}"], True),   # a new id git does not know -> unknown
    ([f"{SHARED}01\t{OLD_A}", f"{SHARED}02\t{OLD_B}"], True),   # ambiguous
    ([f"{OLD_A}\t{OLD_C}"], False),  # cell absent
])
def test_f2_falls_through_silently(tmp_path, rows, cell, capsys):
    proj = _project(tmp_path, rows, cell=cell, git=True)
    assert links.resolve_old_sha(proj, OLD_A) is None
    assert capsys.readouterr().out == "" and capsys.readouterr().err == ""


def test_f2_absent_map_file_is_silent(tmp_path):
    proj = _project(tmp_path, None, git=True)
    (proj / ".agi" / "scrub" / "m.tsv").unlink()
    assert links.resolve_old_sha(proj, OLD_A) is None


def test_f5_a_dropped_commit_is_not_a_commit(tmp_path):
    """item 5: an all-zero new id, and a new id git does not know, both -> None."""
    proj = _project(tmp_path, [f"{OLD_A}\t{'0' * 40}", f"{OLD_B}\t{OLD_C}"], git=True)
    assert links.resolve_old_sha(proj, OLD_A) is None   # zeroed row
    assert links.resolve_old_sha(proj, OLD_B) is None   # unknown commit id


def test_f6_a_four_hex_prefix_resolves(tmp_path):
    """item 6: the gate is 4..40 hex, so a 6-hex abbreviated old id answers."""
    proj = _project(tmp_path, None, git=True)
    head = links._git_commit(proj, "HEAD")
    (proj / ".agi/scrub/m.tsv").write_text(f"{OLD_A}\t{head}\n")
    assert links.resolve_old_sha(proj, OLD_A[:6]) == head
    assert links.resolve_old_sha(proj, OLD_A[:3]) is None   # under the gate


def test_f3_sha_prints_only_the_new_id(tmp_path, capsys):
    proj = _project(tmp_path, [f"{OLD_A}\t{'c' * 40}"], git=True)
    head = links._git_commit(proj, "HEAD")
    (proj / ".agi/scrub/m.tsv").write_text(f"{OLD_A}\t{head}\n")
    assert links.main(["sha", OLD_A[:8], "--root", str(proj)]) == 0
    out = capsys.readouterr()
    assert out.out.strip() == head and "map" not in out.out.lower()
    assert OLD_A not in out.out and OLD_A not in out.err   # the input id never echoes
    assert links.main(["sha", OLD_B, "--root", str(proj)]) == 1
    out = capsys.readouterr()
    assert "unknown commit id" in out.err and OLD_B not in out.err and out.out == ""


def test_f3_sha_with_no_id_is_refused_by_name(tmp_path, capsys):
    """item 10: an absent id is refused at argv (rc 2), never resolved as ""."""
    proj = _project(tmp_path, None, git=True)
    assert links.main(["sha", "--root", str(proj)]) == 2
    assert "needs a commit id" in capsys.readouterr().err


def test_f4_no_map_path_literal_in_code():
    """item 3: the forbidden literal is BUILT here, so grep over extensions/ is 0."""
    forbidden = "commit" + "-map"
    src = (BIN / "links.py").read_text(encoding="utf-8")
    assert forbidden not in src and "scrub_commit_map" in src   # the CELL, not a path


def test_f7_create_warns_once_and_still_writes(tmp_path, capsys):
    """item 1: the WARN is reachable on the CREATE branch, through main, rc 0."""
    proj = _project(tmp_path, [])
    body = tmp_path / "b.md"
    body.write_text(f"see {HOME}/x.log\n")
    assert w.main(["create", "hypothesis", "h-create-warn", "--parent", "idea:i1",
                   "--body-file", str(body), "--root", str(proj)]) == 0
    err = capsys.readouterr().err
    assert err.count("WARN:") == 1 and "refused" in err.lower()
    assert (proj / ".agi/nodes/hypothesis/h-create-warn.md").is_file()


def test_f7_the_warn_judges_added_text_only(tmp_path, capsys):
    """item 7: a CONTEXT line carrying a home path is not this write's text."""
    proj = _project(tmp_path, [])
    body = tmp_path / "b.md"
    body.write_text(f"alpha\nbeta {HOME}/x.log\ngamma\n")
    assert w.main(["create", "hypothesis", "h-diff-warn", "--parent", "idea:i1",
                   "--body-file", str(body), "--root", str(proj)]) == 0
    capsys.readouterr()
    d = tmp_path / "d.diff"
    d.write_text("--- a\n+++ b\n@@ -3,2 +3,2 @@\n alpha\n"
                 f"-beta {HOME}/x.log\n+clean text\n")
    assert w.main(["hypothesis:h-diff-warn", f"body_patch {d}", "--root", str(proj)]) == 0
    assert capsys.readouterr().err.count("WARN:") == 0, "a context line is not added text"
    d.write_text("--- a\n+++ b\n@@ -3,2 +3,2 @@\n alpha\n"
                 "-clean text\n" + f"+see {HOME}/y.log\n")
    assert w.main(["hypothesis:h-diff-warn", f"body_patch {d}", "--root", str(proj)]) == 0
    assert capsys.readouterr().err.count("WARN:") == 1


def test_f8_an_unreadable_map_is_a_silent_none(tmp_path, capsys, monkeypatch):
    """item 1: a map file that EXISTS but cannot be read is a MISS — never a raise."""
    proj = _project(tmp_path, [f"{OLD_A}\t{'c' * 40}"], git=True)
    m, real = proj / ".agi/scrub/m.tsv", Path.read_text
    monkeypatch.setattr(Path, "read_text", lambda s, *a, **k: (
        (_ for _ in ()).throw(OSError("no read")) if s == m else real(s, *a, **k)))
    assert links.resolve_old_sha(proj, OLD_A) is None
    out = capsys.readouterr()
    assert (out.out, out.err) == ("", "")


def test_f9_map_cache_reads_once_per_mtime(tmp_path):
    """item 3: _MAP_CACHE is real — one read for many calls, a changed mtime re-reads."""
    proj = _project(tmp_path, None, git=True)
    head = links._git_commit(proj, "HEAD")
    m, real, seen = proj / ".agi/scrub/m.tsv", Path.read_text, []
    Path.read_text = lambda s, *a, **k: (seen.append(s) if s == m else None,
                                         real(s, *a, **k))[1]
    try:
        m.write_text(f"{OLD_A}\t{head}\n")
        assert links.resolve_old_sha(proj, OLD_A[:8]) == head
        assert links.resolve_old_sha(proj, OLD_A) == head and len(seen) == 1
        os.utime(m, ns=(0, 0))   # a changed mtime is a changed cache key
        assert links.resolve_old_sha(proj, OLD_A) == head and len(seen) == 2
    finally:
        Path.read_text = real


def test_f10_every_file_source_is_judged(tmp_path, capsys):
    """item 2: the sources read in SUBMIT are judged, on create and on edit."""
    proj, r, src = _project(tmp_path, []), tmp_path / "r.md", tmp_path / "p.py"
    src.write_text(f"# see {HOME}/x.log\n")
    assert w.main(["create", "build", "b-warn", "--parent", "idea:i1", "--payload",
                   str(src), "--root", str(proj)]) == 0
    assert capsys.readouterr().err.count("WARN:") == 1
    assert w.main(["create", "hypothesis", "h-rep-warn", "--parent",
                   "idea:i1", "--root", str(proj)]) == 0
    capsys.readouterr()
    r.write_text(f"added {HOME}/y.log\n")
    assert w.main(["hypothesis:h-rep-warn", f"replace body 4:6 {r}",
                   "--root", str(proj)]) == 0
    assert capsys.readouterr().err.count("WARN:") == 1
