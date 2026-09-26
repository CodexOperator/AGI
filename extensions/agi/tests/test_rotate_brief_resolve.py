# test_rotate_brief_resolve.py -- L5.11
# (hypothesis:l5-rename-surfaces-and-the-successor-brief-resolve-from-the-
# rotating-worktree-root). The rename boundary already re-roots the post's
# quorum card on `_own_sessions_dir` (the post's own worktree, or MAIN for a
# MAIN-resident post). The successor brief did NOT: `cmd_rotate_self` handed
# `spawn_window` a template `brief_file` and `spawn_window` resolved it
# CWD-relative, so the two agreed only when the rotating post's cwd happened
# to be its worktree. `_resolve_brief_file` makes the ONE-root property
# structural: a `.agi/sessions`-prefixed relative brief re-roots on
# `_own_sessions_dir`, an absolute path and any other relative path pass
# through.
# UPDATE (hypothesis:non-prime-rotate-self-renders-through-brief-render): the
# resolved cell now reaches `spawn_window` as `card_file`, not `prompt_file`,
# so a non-prime's successor also gets the ONE render. The RESOLUTION these
# tests pin is unchanged -- only its seat in the argv moved.
import argparse
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate  # noqa: E402


def _seats(root, rows):
    geo = root / "nodes" / ".geometry"
    geo.mkdir(parents=True, exist_ok=True)
    lines = ["---", "id: config:seats", "type: config", "seats:"]
    for r in rows:
        lines.append("  - " + json.dumps(r, sort_keys=True))
    lines += ["---", "# body"]
    (geo / "seats.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _rotations(root, brief_file):
    geo = root / "nodes" / ".geometry"
    geo.mkdir(parents=True, exist_ok=True)
    # `brief_file` is QUOTED: an unquoted value holding `{seat}` parses as a
    # YAML flow mapping and the whole frontmatter is rejected as malformed.
    (geo / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\ntemplates:\n"
        f'  parent: {{brief_file: "{brief_file}", steps: [handoff, spawn], '
        'telemetry: [seat]}\n---\n\nbody\n', encoding="utf-8")


def _root(tmp_path):
    root = tmp_path / "graph"
    (root / "nodes").mkdir(parents=True)
    return root


def _args(**over):
    base = dict(name="old", force=True, timeout=5, debug_file="/dev/null",
                model=None, effort=None, settings=None, prompt_file=None,
                tmux_session="t", window_path=None, dry_run=False,
                throwaway=True, successor_argv=None, role="parent")
    base.update(over)
    return argparse.Namespace(**base)


def _capture(monkeypatch):
    seen = {}
    monkeypatch.setattr(rotate, "spawn_window",
                        lambda **kw: seen.update(kw) or (0, "echo hi"))
    monkeypatch.setattr(rotate, "find_project_root", lambda: seen["root"])
    return seen


def test_worktree_post_brief_reroots_on_its_own_card(tmp_path, monkeypatch):
    """WIRE: a worktree post's template brief resolves to the SAME file
    `_rename_surfaces` renames for that post -- root != cwd."""
    root = _root(tmp_path)
    wt = tmp_path / "post-old"
    (wt / ".agi" / "sessions" / "quorum").mkdir(parents=True)
    _seats(root, [{"name": "old", "role": "parent", "worktree": str(wt)}])
    _rotations(root, ".agi/sessions/quorum/{seat}.md")
    monkeypatch.chdir(tmp_path)  # graph root != cwd
    seen = _capture(monkeypatch)
    seen["root"] = root

    rotate.cmd_rotate_self(_args(), root)
    assert seen["prompt_file"] is None, (
        "a non-prime rotation renders too now; the template brief arrives as "
        "card_file, not as a prompt file")
    assert Path(seen["card_file"]) == (
        rotate._own_sessions_dir(root, "old") / "quorum" / "old.md")
    assert seen["card_file"] == str(
        wt / ".agi" / "sessions" / "quorum" / "old.md")


def test_main_post_brief_stays_main_rooted(tmp_path, monkeypatch):
    """GATE: a MAIN-resident row (empty `worktree` cell) resolves to MAIN's
    shared card, never a worktree."""
    root = _root(tmp_path)
    _seats(root, [{"name": "old", "role": "parent", "worktree": ""}])
    _rotations(root, ".agi/sessions/quorum/{seat}.md")
    monkeypatch.chdir(tmp_path)
    seen = _capture(monkeypatch)
    seen["root"] = root

    rotate.cmd_rotate_self(_args(), root)
    assert "card_file" in seen
    assert seen["card_file"] == str(
        root / "sessions" / "quorum" / "old.md")


# --- L5.14: the RELATIVE worktree cell, next to its absolute sibling ------
# Every test above spells the seat row's `worktree` cell absolutely. Live
# rows carry it RELATIVE (`"worktree": ".agi/worktrees/post-sensei-
# director"`), a different branch of `_own_sessions_dir`:
# `Path(locations.git_common_root(root) or root) / wt`. With `root` the main
# graph dir, `git_common_root` is the MAIN checkout, and the cell is relative
# to THAT -- only a real `git worktree` exercises it.


def _git(path, *args):
    res = subprocess.run(["git", *args], cwd=path, capture_output=True,
                         text=True)
    if res.returncode != 0:
        raise RuntimeError(f"git {args}: {res.stderr}")
    return res.stdout.strip()


def _main_repo_with_relative_worktree(tmp_path):
    """Main repo, graph at `main/.agi/`, linked `git worktree` at
    `main/.agi/worktrees/post-old` (the live geometry), seat row carrying
    the RELATIVE cell. Returns `(graph_root, wt)`."""
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
    wt = main / ".agi" / "worktrees" / "post-old"
    _git(main, "worktree", "add", "-q", str(wt), "-b", "old", "master")
    graph_root = main / ".agi"
    _seats(graph_root, [{"name": "old", "role": "parent",
                         "worktree": ".agi/worktrees/post-old"}])
    return graph_root, wt


def test_relative_cell_brief_reroots_on_the_worktree_card(
        tmp_path, monkeypatch):
    """RELATIVE cell, REAL git: the `.agi/sessions`-prefixed template
    re-roots on the worktree's own card through `git_common_root`, and the
    ABSOLUTE spelling of the same cell re-roots to the identical file -- the
    pairing the absolute-cell wire test above pins is preserved."""
    graph_root, wt = _main_repo_with_relative_worktree(tmp_path)
    card = wt / ".agi" / "sessions" / "quorum" / "old.md"
    card.parent.mkdir(parents=True)
    card.write_text("card\n")
    monkeypatch.chdir(tmp_path)  # never the worktree, never the graph root
    template = ".agi/sessions/quorum/old.md"
    from_rel = rotate._resolve_brief_file(graph_root, "old", template)
    assert from_rel == str(card)
    # the SAME cell spelled absolutely resolves to the SAME file.
    _seats(graph_root, [{"name": "old", "role": "parent",
                         "worktree": str(wt)}])
    assert rotate._resolve_brief_file(graph_root, "old", template) == from_rel


def _name_args(old, new):
    return argparse.Namespace(old_name=old, new_name=new, dry_run=False,
                              now=False, apply=False, root=None)


def test_absolute_and_non_session_briefs_pass_through(tmp_path, monkeypatch):
    """AUTH: an absolute path is unchanged; a non-`.agi/sessions` relative
    brief (`extensions/agi/briefs/...`) keeps its own root; an explicit
    `--prompt-file` is never re-rooted."""
    root = _root(tmp_path)
    wt = tmp_path / "post-old"
    (wt / ".agi" / "sessions" / "quorum").mkdir(parents=True)
    _seats(root, [{"name": "old", "role": "parent", "worktree": str(wt)}])

    assert rotate._resolve_brief_file(
        root, "old", "/abs/x.md") == "/abs/x.md"
    assert rotate._resolve_brief_file(
        root, "old", "extensions/agi/briefs/prime-director-successor.md"
    ) == "extensions/agi/briefs/prime-director-successor.md"

    _rotations(root, ".agi/sessions/quorum/{seat}.md")
    monkeypatch.chdir(tmp_path)
    seen = _capture(monkeypatch)
    seen["root"] = root
    rotate.cmd_rotate_self(
        _args(prompt_file=".agi/sessions/quorum/override.md"), root)
    assert "prompt_file" in seen
    assert seen["prompt_file"] == ".agi/sessions/quorum/override.md"


def _stage(root, old, new):
    assert rotate.cmd_rename_post(_name_args(old, new), root) == 0


def _quorum(base, name, text="card\n"):
    q = base / "sessions" / "quorum"
    q.mkdir(parents=True, exist_ok=True)
    p = q / name
    p.write_text(text, encoding="utf-8")
    return p


def test_rename_boundary_brief_resolves_on_the_old_rows_tree(
        tmp_path, monkeypatch):
    """RED (rename transient): at a rename boundary the card is renamed under
    the PRE-rename row's tree. With ONLY the old row present, the successor
    brief must resolve there -- under the old row -- even though the card on
    disk carries the NEW name. Pre-fix the root seat stayed `seat` (the new
    name), `_find_seat` found no new row, and the brief fell back to MAIN's
    `<root>/sessions/quorum/new.md`, which does not exist: the 19:08Z
    `prompt file not found`. cwd == the worktree, the real spawn cwd."""
    root = _root(tmp_path)
    wt = tmp_path / "post-old"
    _quorum(wt / ".agi", "old.md")
    _seats(root, [{"name": "old", "role": "parent", "worktree": str(wt)}])
    _rotations(root, ".agi/sessions/quorum/{seat}.md")
    monkeypatch.chdir(wt)
    seen = _capture(monkeypatch)
    seen["root"] = root

    _stage(root, "old", "new")
    rotate.cmd_rotate_self(_args(), root)
    assert "card_file" in seen
    boundary = rotate._own_sessions_dir(root, "old") / "quorum" / "new.md"
    assert Path(seen["card_file"]) == boundary
    assert Path(seen["card_file"]).exists(), seen["card_file"]


def test_no_rename_brief_still_resolves_the_own_card(tmp_path, monkeypatch):
    """GATE: without a rename boundary the root seat is the row name; a cwd
    that is NOT the worktree must still resolve the worktree card."""
    root = _root(tmp_path)
    wt = tmp_path / "post-old"
    (wt / ".agi" / "sessions" / "quorum").mkdir(parents=True)
    _seats(root, [{"name": "old", "role": "parent", "worktree": str(wt)}])
    _rotations(root, ".agi/sessions/quorum/{seat}.md")
    elsewhere = tmp_path / "not-the-worktree"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)
    seen = _capture(monkeypatch)
    seen["root"] = root

    rotate.cmd_rotate_self(_args(), root)
    assert "card_file" in seen
    assert seen["card_file"] == str(
        wt / ".agi" / "sessions" / "quorum" / "old.md")


def test_rename_boundary_main_resident_row_stays_main_rooted(
        tmp_path, monkeypatch):
    """GATE: a MAIN-resident row (empty `worktree` cell) has no worktree
    card; the boundary renames MAIN's card and the brief must follow it
    there, not fall into a worktree."""
    root = _root(tmp_path)
    _quorum(root, "old.md")
    _seats(root, [{"name": "old", "role": "parent", "worktree": ""}])
    _rotations(root, ".agi/sessions/quorum/{seat}.md")
    monkeypatch.chdir(tmp_path)
    seen = _capture(monkeypatch)
    seen["root"] = root

    _stage(root, "old", "new")
    rotate.cmd_rotate_self(_args(), root)
    assert "card_file" in seen
    assert seen["card_file"] == str(
        root / "sessions" / "quorum" / "new.md")
    assert Path(seen["card_file"]).exists()


def test_pre_fix_brief_stays_cwd_relative(tmp_path, monkeypatch):
    """RED evidence: with the resolver disabled the captured brief is the
    CWD-relative `.agi/sessions/quorum/<seat>.md` -- the coincidence the
    fix removes. Run from a cwd that is NOT the worktree and the successor
    would read the wrong tree."""
    root = _root(tmp_path)
    wt = tmp_path / "post-old"
    (wt / ".agi" / "sessions" / "quorum").mkdir(parents=True)
    _seats(root, [{"name": "old", "role": "parent", "worktree": str(wt)}])
    _rotations(root, ".agi/sessions/quorum/{seat}.md")
    monkeypatch.setattr(rotate, "_resolve_brief_file",
                        lambda r, s, b: b)  # pre-fix rule
    elsewhere = tmp_path / "not-the-worktree"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)
    seen = _capture(monkeypatch)
    seen["root"] = root

    rotate.cmd_rotate_self(_args(), root)
    assert "card_file" in seen
    assert seen["card_file"] == ".agi/sessions/quorum/old.md"
    assert Path(seen["card_file"]).is_absolute() is False
    assert (elsewhere / seen["card_file"]).exists() is False

# --- EF.25 items 2+3: the prime's successor body is the assembled render ----


def _rotations_prime(root, brief_file):
    geo = root / "nodes" / ".geometry"
    geo.mkdir(parents=True, exist_ok=True)
    (geo / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\ntemplates:\n"
        f'  prime_director: {{brief_file: "{brief_file}", steps: [handoff, spawn], '
        'telemetry: [seat]}\n---\n\nbody\n', encoding="utf-8")


def test_prime_rotate_self_leaves_prompt_file_to_the_render(tmp_path,
                                                            monkeypatch):
    """item 2 of hypothesis:brief-py-assembles-every-first-turn-from-config:
    a prime seat's REAL rotation does not resolve the template's static
    brief_file, so `spawn_window`'s no-prompt-file branch renders head + the
    role template + doc:card-<post> + the trajectory. Resolving it here would
    bypass the render AND, with the [handoff-head] first_turn entry gone, drop
    the card entirely."""
    root = _root(tmp_path)
    _seats(root, [{"name": "belam", "role": "prime_director", "worktree": ""}])
    _rotations_prime(root, "extensions/agi/briefs/prime-director-successor.md")
    monkeypatch.chdir(tmp_path)
    seen = _capture(monkeypatch)
    seen["root"] = root

    rotate.cmd_rotate_self(_args(name="belam", role="prime_director"), root)
    assert seen.get("prompt_file") is None, (
        "a prime rotation must let spawn_window render, not read brief_file")


def test_non_prime_rotate_self_still_resolves_its_template_brief(tmp_path,
                                                                 monkeypatch):
    """GATE: the prime exemption must not disarm the template brief for the
    other roles -- a parent still resolves its quorum card."""
    root = _root(tmp_path)
    wt = tmp_path / "post-old"
    (wt / ".agi" / "sessions" / "quorum").mkdir(parents=True)
    card = wt / ".agi" / "sessions" / "quorum" / "old.md"
    card.write_text("card\n", encoding="utf-8")
    _seats(root, [{"name": "old", "role": "parent", "worktree": str(wt)}])
    _rotations(root, ".agi/sessions/quorum/{seat}.md")
    monkeypatch.chdir(tmp_path)
    seen = _capture(monkeypatch)
    seen["root"] = root

    rotate.cmd_rotate_self(_args(), root)
    assert seen["prompt_file"] is None, (
        "the template card reaches the successor as card_file, so the "
        "successor still gets the ONE render (this test's old docstring: "
        "\"a parent still resolves its quorum card\" -- the resolution is "
        "unchanged, only its SEAT in the argv is)")
    assert seen["card_file"] == str(card)


def test_faith_ref_error_in_render_falls_back_loudly(monkeypatch, capsys):
    """hypothesis:brief-render-hygiene-after-the-batch-mur: `brief.render`
    reads moral:faith, so a broken faith ref raised FaithRefError PAST the old
    `except brief.RenderError` and killed the rotation rather than falling
    back. The fallback must catch it and print its reason."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "bin"))
    import brief  # noqa: E402

    def boom(**kw):
        raise brief.FaithRefError("faith ref region missing")
    monkeypatch.setattr(brief, "render", boom)
    monkeypatch.setattr(brief, "assemble", lambda **kw: ["FALLBACK-BODY-SENTINEL"])
    seen = {}
    monkeypatch.setattr(rotate, "_build_harness_command",
                        lambda h, **kw: seen.update(prompt=kw["prompt_text"]) or [])
    rotate._assembled_successor_command(
        name="post-x", tier="director", model=None, effort=None, settings=None,
        debug_file="/dev/null")
    err = capsys.readouterr().err
    assert "FALLBACK-BODY-SENTINEL" in seen["prompt"]
    assert "faith ref region missing" in err
    assert "falling back to brief.assemble" in err
