"""hypothesis:g133 — resolve_old_sha: the ONE pre-rewrite commit-id resolver.

Every value here is SYNTHETIC (fake 40-hex old ids, a tmp git repo, a tmp
config naming a tmp map). The real map and every real pre-rewrite id are never
read by this file, and no real box path is printed.

Falsifiers, one per test: F1 mapped, F2 x4 silent-None, F3 the `sha`
subcommand's output shape, F4 no map path literal in the code, F5 write.py
WARNs and does not refuse.
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import links  # noqa: E402

OLD_A = "a" * 40          # synthetic pre-rewrite id
OLD_B = "b" * 40
OLD_C = "c" * 40
SHARED = "deadbeef"       # two rows share this prefix -> ambiguous


def _git_repo(tmp_path: Path) -> "tuple[Path, str]":
    repo = tmp_path / "repo"
    repo.mkdir()
    env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
           "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t",
           "PATH": "/usr/bin:/bin", "HOME": str(tmp_path)}
    subprocess.run(["git", "init", "-q", str(repo)], check=True, env=env)
    (repo / "f").write_text("x\n")
    subprocess.run(["git", "-C", str(repo), "add", "f"], check=True, env=env)
    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "c"], check=True, env=env)
    head = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                          check=True, capture_output=True, text=True,
                          env=env).stdout.strip()
    return repo, head


def _project(tmp_path: Path, map_rows: list[str] | None, *, cell: bool = True) -> Path:
    """A tmp `.agi/` project whose config names a tmp map (or does not)."""
    agi = tmp_path / "proj" / ".agi"
    agi.mkdir(parents=True)
    cfg = {"paths": {"local_maxxing": {}}}
    if cell:
        cfg["paths"]["local_maxxing"]["scrub_commit_map"] = ".agi/scrub/m.tsv"
        (agi / "scrub").mkdir()
        (agi / "scrub" / "m.tsv").write_text(
            "".join(r + "\n" for r in (map_rows or [])))
    (agi / "config.json").write_text(__import__("json").dumps(cfg))
    (agi / "nodes").mkdir()
    return agi.parent


def test_f1_known_commit_answers_full_id(tmp_path):
    repo, head = _git_repo(tmp_path)
    root = repo
    full = links.resolve_old_sha(root, head[:12])
    assert full and len(full) == 40 and full == links.resolve_old_sha(root, full)


def test_f1_mapped_prefix_answers_the_rewritten_id(tmp_path):
    _repo, head = _git_repo(tmp_path)
    proj = _project(tmp_path, [f"{OLD_A}\t{head}"])
    assert links.resolve_old_sha(proj, OLD_A[:9]) == head
    assert links.resolve_old_sha(proj, OLD_A) == head


@pytest.mark.parametrize("rows,cell", [
    ([], True),                      # cell present, map empty -> unknown
    ([f"{OLD_B}\t{OLD_C}"], True),   # id nobody knows -> unknown
    ([f"{SHARED}01\t{OLD_A}", f"{SHARED}02\t{OLD_B}"], True),   # ambiguous
    ([f"{OLD_A}\t{OLD_C}"], False),  # cell absent
])
def test_f2_falls_through_silently(tmp_path, rows, cell):
    proj = _project(tmp_path, rows, cell=cell)
    assert links.resolve_old_sha(proj, OLD_A) is None


def test_f2_absent_map_file_is_silent(tmp_path):
    proj = _project(tmp_path, None)
    (proj / ".agi" / "scrub" / "m.tsv").unlink()
    assert links.resolve_old_sha(proj, OLD_A) is None


def test_f3_sha_subcommand_prints_only_the_new_id(tmp_path, capsys):
    _repo, head = _git_repo(tmp_path)
    proj = _project(tmp_path, [f"{OLD_A}\t{head}"])
    rc = links.main(["sha", OLD_A[:8], "--root", str(proj)])
    out = capsys.readouterr()
    assert rc == 0 and out.out.strip() == head
    assert OLD_A not in (out.out + out.err) and "map" not in out.out.lower()
    rc = links.main(["sha", OLD_B, "--root", str(proj)])
    out = capsys.readouterr()
    assert rc == 1 and "unknown" in out.err


def test_f4_no_map_path_literal_in_code():
    src = (BIN / "links.py").read_text(encoding="utf-8")
    assert "commit-map" not in src and "commit_map/" not in src
    assert "scrub_commit_map" in src      # the CELL name, not a path


def test_f5_write_warns_and_does_not_refuse(tmp_path, capsys):
    import json as _json
    import write as w
    proj = _project(tmp_path, [])
    agi = proj / ".agi"
    (agi / "config.json").write_text(_json.dumps({"id": "n"}))
    edit = w.Edit(node_id="n",
                  replace_text="see /home/someone/x.log\n")
    w._warn_home_path(edit)
    err = capsys.readouterr().err
    assert err.startswith("WARN:") and "refused" in err.lower()
