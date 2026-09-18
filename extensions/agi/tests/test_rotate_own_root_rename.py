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
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate  # noqa: E402

# `rotate` imports `locations` from the `extensions/agi/bin` sys.path entry,
# so the module the test must monkeypatch is `rotate.locations`, NOT
# `agi.bin.locations` -- the two are distinct objects in `sys.modules` and a
# patch on the latter is invisible to `_own_sessions_dir`.
locations = rotate.locations


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


# --- L5.14: the relative worktree CELL -------------------------------------
# Every test above spells the seat row's `worktree` cell ABSOLUTELY
# (`str(wt)`). Live seat rows carry it RELATIVE -- `config:seats` row
# `director-sanctuary` holds `".agi/worktrees/post-sensei-director"` -- and
# `_own_sessions_dir` runs a DIFFERENT branch for it:
#     if not p.is_absolute():
#         p = Path(locations.git_common_root(root) or root) / wt
# With `root` = the rotating post's own graph dir, `git_common_root` returns
# the MAIN checkout, so the cell is relative to THAT. A tmp_path-only test
# with no git exercises only the `or root` fallback, which is NOT the live
# branch -- hence a real linked `git worktree` fixture. Pinned to the shape
# `rotate.py:3554` actually takes; see
# hypothesis:l5-relative-worktree-cell-resolution-has-no-committed-test-
# coverage.


def _git(path, *args):
    res = subprocess.run(["git", *args], cwd=path, capture_output=True,
                         text=True)
    if res.returncode != 0:
        raise RuntimeError(f"git {args}: {res.stderr}")
    return res.stdout.strip()


def _main_repo_with_worktree(tmp_path, cell):
    """A REAL main repo whose graph is `main/.agi/`, with a linked git
    worktree at `main/.agi/worktrees/post-old` -- the live geometry (the
    worktree lives UNDER the main checkout's `.agi`, so the relative cell
    `.agi/worktrees/post-old` is relative to the MAIN root, not the graph
    root). `cell` is the spelling the seat row carries. Returns
    `(main, graph_root, worktree_path)`."""
    main = tmp_path / "main"
    (main / ".agi" / "nodes").mkdir(parents=True)
    _git(main, "init", "-q", "-b", "master")
    _git(main, "config", "user.email", "t@t")
    _git(main, "config", "user.name", "t")
    (main / ".gitignore").write_text(".agi/worktrees/\n")
    (main / "README").write_text("x")
    (main / ".agi" / "nodes" / ".keep").write_text("x")
    _git(main, "add", "-A")
    _git(main, "commit", "-q", "-m", "init")
    wt_rel = ".agi/worktrees/post-old"
    wt = main / wt_rel
    _git(main, "worktree", "add", "-q", str(wt), "-b", "old", "master")
    graph_root = main / ".agi"
    spelling = wt_rel if cell == "relative" else str(wt)
    _seats(graph_root, [{"name": "old", "role": "director",
                         "worktree": spelling}])
    return main, graph_root, wt


def _quorum_in_wt(wt, name="old.md"):
    q = wt / ".agi" / "sessions" / "quorum"
    q.mkdir(parents=True, exist_ok=True)
    p = q / name
    p.write_text("card\n", encoding="utf-8")
    return p


def test_own_sessions_dir_relative_cell_runs_git_common_root(tmp_path,
                                                            monkeypatch):
    """RELATIVE cell, REAL git: `_own_sessions_dir(graph_root, seat)` must
    resolve through `git_common_root(graph_root)` (the MAIN checkout) and
    find the worktree's own sessions dir. `graph_root` is the main graph dir,
    the root a director on MAIN holds for a worktree post. WITHOUT git the
    `or root` fallback would join the cell onto `graph_root/.agi`, a path
    that does not exist, and fall back to MAIN's shared dir -- so this test
    is the branch, not the fallback."""
    main, graph_root, wt = _main_repo_with_worktree(tmp_path, "relative")
    _quorum_in_wt(wt)
    monkeypatch.chdir(tmp_path)  # never the worktree, never the graph root
    assert locations.git_common_root(graph_root) == main.resolve()
    expected = wt / ".agi" / "sessions"
    assert rotate._own_sessions_dir(graph_root, "old") == expected
    assert expected.is_dir()


def test_own_sessions_dir_relative_and_absolute_cells_agree(tmp_path,
                                                           monkeypatch):
    """The two spellings of the SAME worktree cell resolve to the identical
    Path -- the relative case cannot drift from the absolute one already
    pinned above."""
    monkeypatch.chdir(tmp_path)
    rel_main, rel_graph, rel_wt = _main_repo_with_worktree(
        tmp_path / "rel", "relative")
    abs_main, abs_graph, abs_wt = _main_repo_with_worktree(
        tmp_path / "abs", "absolute")
    assert rotate._own_sessions_dir(rel_graph, "old") == rel_wt / ".agi" / "sessions"
    assert rotate._own_sessions_dir(abs_graph, "old") == abs_wt / ".agi" / "sessions"
    assert (rotate._own_sessions_dir(rel_graph, "old")
            == Path(str(rel_wt)) / ".agi" / "sessions")


def test_resolve_brief_file_reroots_on_the_relative_cell(tmp_path,
                                                         monkeypatch):
    """`_resolve_brief_file` re-roots the `.agi/sessions`-prefixed relative
    template on the SAME dir `_own_sessions_dir` returns for a RELATIVE cell
    -- the successor reads the card the boundary renames."""
    main, graph_root, wt = _main_repo_with_worktree(tmp_path, "relative")
    _quorum_in_wt(wt)
    monkeypatch.chdir(tmp_path)
    got = rotate._resolve_brief_file(
        graph_root, "old", ".agi/sessions/quorum/{seat}.md".replace(
            "{seat}", "old"))
    assert got == str(wt / ".agi" / "sessions" / "quorum" / "old.md")
    # ... exactly the file the rename boundary renames.
    surf = _quorum_surfaces(rotate._rename_surfaces(graph_root, "old", "new"))
    assert [s["src"] for s in surf] == [got]


def test_rename_surfaces_relative_cell_names_the_worktree_card(tmp_path,
                                                              monkeypatch):
    """`_rename_surfaces` names the worktree quorum card as a
    `session-file` surface for a RELATIVE cell -- the shape the live
    `sensei-director.20260917T222602Z.json` `applied_rename.surfaces`
    recorded."""
    main, graph_root, wt = _main_repo_with_worktree(tmp_path, "relative")
    wt_card = _quorum_in_wt(wt, "old.md")
    _quorum(graph_root, "old.md", "stale main copy\n")
    monkeypatch.chdir(tmp_path)
    surf = _quorum_surfaces(rotate._rename_surfaces(graph_root, "old", "new"))
    assert len(surf) == 1, surf
    assert surf[0]["src"] == str(wt_card)
    assert surf[0]["dst"] == str(wt / ".agi" / "sessions" / "quorum" / "new.md")


def test_own_card_path_ignores_the_cell_and_keys_on_root(tmp_path,
                                                        monkeypatch):
    """HONEST RESIDUE, not a vacuous pass: `_own_card_path` (rotate.py:7586)
    reads NO seat row at all -- it tries `root/sessions/quorum/<seat>.md`
    then `root/.agi/sessions/quorum/<seat>.md` and falls back to MAIN's
    shared dir. So it can only find a worktree post's card when `root` is
    ALREADY the worktree's own graph dir (the rotating post's cwd, the live
    case). Against that worktree graph root BOTH cell spellings give the
    identical path -- which is exactly what the code guarantees (the cell is
    inert) and NOT evidence that the cell is honoured. A caller holding the
    MAIN graph root for a worktree post would get MAIN's stale copy; that is
    the residue this test records rather than hides."""
    main, graph_root, wt = _main_repo_with_worktree(tmp_path, "relative")
    wt_card = _quorum_in_wt(wt, "old.md")
    monkeypatch.chdir(tmp_path)
    root_wt = wt / ".agi"
    from_rel = rotate._own_card_path(root_wt, "old")
    # re-spell the SAME row absolutely: the resolver never reads it, so the
    # answer cannot move -- pinned, not asserted to be correct.
    _seats(graph_root, [{"name": "old", "role": "director",
                         "worktree": str(wt)}])
    from_abs = rotate._own_card_path(root_wt, "old")
    assert from_rel == from_abs == wt_card
    # residue: from the MAIN graph root it resolves MAIN's shared copy, not
    # the worktree card -- the cell is inert.
    main_shared = rotate._own_card_path(graph_root, "old")
    assert main_shared == rotate._sessions_dir(graph_root) / "quorum" / "old.md"
    assert main_shared != wt_card


def test_relative_cell_without_git_falls_back_not_into_the_worktree(
        tmp_path, monkeypatch):
    """FALSIFIER for the fixture itself: disable `git_common_root` (return
    None = no enclosing repo) and the relative cell resolves onto
    `graph_root/.agi/...`, which does not exist, so the resolver falls back
    to MAIN's shared dir and MISSES the worktree card. This is why the
    committed test needs a real `git worktree` and cannot be replaced by a
    tmp_path-only probe."""
    main, graph_root, wt = _main_repo_with_worktree(tmp_path, "relative")
    _quorum_in_wt(wt)
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(locations, "git_common_root", lambda root: None)
    assert rotate._own_sessions_dir(graph_root, "old") == (
        rotate._sessions_dir(graph_root))
    assert rotate._own_sessions_dir(graph_root, "old") != wt / ".agi" / "sessions"


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
