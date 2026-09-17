# test_rotate_own_root_rename.py -- L5.11
# (hypothesis:l5-rename-surfaces-and-the-successor-brief-resolve-from-the-
# rotating-worktree-root). The rename boundary resolved every session-file
# surface through `_sessions_dir` (MAIN), while `spawn_window` resolved the
# successor brief CWD-relative -- so a rotation-with-rename from a post's own
# worktree renamed MAIN's stale card and the successor then could not find
# the worktree brief (exit 1, `prompt file not found`). The quorum CARD is
# the post's own file (`_own_card_path`, worktree-first); the shared room
# stays MAIN-rooted.
import argparse
import contextlib as _c
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate  # noqa: E402


def _seats(root, rows):
    geo = root / "nodes" / ".geometry"
    geo.mkdir(parents=True, exist_ok=True)
    lines = ["---", "id: config:seats", "seats:"]
    for r in rows:
        lines.append("  - " + json.dumps(r, sort_keys=True))
    lines += ["---", "# body"]
    (geo / "seats.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _quorum(base, name, text="card\n"):
    q = base / "sessions" / "quorum"
    q.mkdir(parents=True, exist_ok=True)
    p = q / name
    p.write_text(text, encoding="utf-8")
    return p


def _quorum_surfaces(surfaces):
    return [s for s in surfaces
            if s["kind"] == "session-file" and "/quorum/" in s["src"]]


def _stage(root, old, new):
    ns = argparse.Namespace(old_name=old, new_name=new, dry_run=False,
                            now=False, apply=False, root=None)
    assert rotate.cmd_rename_post(ns, root) == 0
    return root / "sessions" / "seats" / f"{old}.rename.json"


def _err(fn):
    buf = io.StringIO()
    with _c.redirect_stderr(buf):
        rc = fn()
    return rc, buf.getvalue()


def test_session_file_surfaces_use_the_posts_own_worktree(tmp_path, monkeypatch):
    """RED: a worktree post's quorum card is the one the boundary must
    rename. Pre-fix the surface named MAIN's copy."""
    root = tmp_path / "graph"
    (root / "nodes").mkdir(parents=True)
    wt = tmp_path / "post-old"
    _quorum(wt / ".agi", "old.md")
    main_card = _quorum(root, "old.md", "stale main copy\n")
    _seats(root, [{"name": "old", "role": "kid", "worktree": str(wt)}])
    monkeypatch.chdir(tmp_path)  # root != cwd (cwd is the parent)

    got = _quorum_surfaces(rotate._rename_surfaces(root, "old", "new"))
    assert len(got) == 1, got
    assert got[0]["src"] == str(wt / ".agi" / "sessions" / "quorum" / "old.md")
    assert got[0]["dst"] == str(wt / ".agi" / "sessions" / "quorum" / "new.md")
    assert got[0]["src"] != str(main_card)


def test_main_post_keeps_quorum_surfaces_main_rooted(tmp_path, monkeypatch):
    """NEGATIVE PROBE: a MAIN-resident post (row `worktree` cell empty) still
    resolves MAIN-rooted -- the shared room is untouched."""
    root = tmp_path / "graph"
    (root / "nodes").mkdir(parents=True)
    main_card = _quorum(root, "old.md")
    _seats(root, [{"name": "old", "role": "kid", "worktree": ""}])
    monkeypatch.chdir(tmp_path)

    got = _quorum_surfaces(rotate._rename_surfaces(root, "old", "new"))
    assert len(got) == 1, got
    assert got[0]["src"] == str(main_card)


def test_boundary_and_brief_agree_on_the_worktree_card(tmp_path, monkeypatch):
    """The boundary renames the SAME file the successor's brief resolves to:
    root != cwd (cwd is the post's worktree, the real spawn cwd), apply, then
    the verbatim `spawn_window` resolution (`.agi/sessions/quorum/<new>.md`
    CWD-relative) finds the renamed card."""
    root = tmp_path / "graph"
    (root / "nodes").mkdir(parents=True)
    wt = tmp_path / "post-old"
    _quorum(wt / ".agi", "old.md")
    _quorum(root, "old.md", "stale main copy\n")
    _seats(root, [{"name": "old", "role": "kid", "worktree": str(wt)}])
    monkeypatch.chdir(wt)  # the post's own worktree, != graph root

    _stage(root, "old", "new")
    rc, err = _err(lambda: rotate._apply_staged(root, "old"))
    assert rc == 0, err
    brief = Path(".agi/sessions/quorum/new.md").expanduser().resolve()
    assert brief == wt / ".agi" / "sessions" / "quorum" / "new.md"
    assert brief.exists(), brief
    assert not (wt / ".agi" / "sessions" / "quorum" / "old.md").exists()


def test_pre_fix_resolution_renamed_mains_card(tmp_path, monkeypatch):
    """Pre-fix record: with the own-tree resolver disabled the boundary
    renames MAIN's card and leaves the worktree's card under the OLD name --
    exactly the mismatch of the 19:08Z incident."""
    root = tmp_path / "graph"
    (root / "nodes").mkdir(parents=True)
    wt = tmp_path / "post-old"
    _quorum(wt / ".agi", "old.md")
    _quorum(root, "old.md", "stale main copy\n")
    _seats(root, [{"name": "old", "role": "kid", "worktree": str(wt)}])
    monkeypatch.setattr(rotate, "_own_sessions_dir",
                        lambda r, s: rotate._sessions_dir(r))  # pre-fix rule

    got = _quorum_surfaces(rotate._rename_surfaces(root, "old", "new"))
    assert len(got) == 1, got
    assert got[0]["src"] == str(root / "sessions" / "quorum" / "old.md")
    _stage(root, "old", "new")
    rc, err = _err(lambda: rotate._apply_staged(root, "old"))
    assert rc == 0, err
    assert (root / "sessions" / "quorum" / "new.md").exists()
    # the file the successor will look for is NOT there: the incident.
    assert not (wt / ".agi" / "sessions" / "quorum" / "new.md").exists()
