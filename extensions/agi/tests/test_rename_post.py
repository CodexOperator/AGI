# test_rename_post.py -- SM.18 RENAME ROUND, round 1 (hypothesis:
# l4-rename-post-renames-every-surface-atomically---...). Proves on a
# throwaway fixture (never the live tree):
#   * `rename-post <old> <new> --dry-run` prints N surfaces, touches nothing
#     (files intact, no stage json).
#   * default STAGES a `<old>.rename.json` carrying {new, ordered_by,
#     staged_at, surfaces}; it touches NO session file.
#   * `--now` with a live pid on the row REFUSES by name (exit 3).
#   * apply renames the session-file surface (seats/, quorum/, inbox, meter,
#     handoff...) atomically; a second apply is an idempotent no-op.
#   * the `aliases:` frontmatter table resolves old -> new in `_find_seat`
#     with the `deprecated alias used: old -> new` stderr line.
# Round-2 surfaces (row name/cells, branch, tmux, worktree dir) are listed by
# --dry-run and staged but NOT applied -- no config write this round.
import argparse
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate  # noqa: E402


def _geo(root, aliases=None, rows=None):
    """posts.md with optional `aliases:` frontmatter and `posts:` rows."""
    geo = root / "nodes" / ".geometry"
    geo.mkdir(parents=True, exist_ok=True)
    lines = ["---", "id: config:posts"]
    if aliases:
        lines.append("aliases:")
        for k, v in aliases.items():
            lines.append(f"  {k}: {v}")
    lines.append("posts:")
    for r in rows or []:
        lines.append("  - " + json.dumps(r, sort_keys=True))
    lines.append("---")
    lines.append("# body")
    (geo / "posts.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def _session_files(root, old):
    """Every session-file surface the post name touches, as a {path: content}
    map -- seats/, quorum/, inbox/, and top-level <old>.meter + <old>.handoff."""
    mk = [
        (root / "sessions" / "seats", f"{old}.key"),
        (root / "sessions" / "seats", f"{old}.bootstrap.json"),
        (root / "sessions" / "quorum", f"{old}.md"),
        (root / "sessions" / "inbox", f"{old}.md"),
        (root / "sessions" / "inbox", f"{old}.nudge.1"),
        (root / "sessions", f"{old}.meter"),
        (root / "sessions", f"{old}.handoff.md"),
    ]
    written = {}
    for parent, name in mk:
        parent.mkdir(parents=True, exist_ok=True)
        p = parent / name
        p.write_text(f"content {name}\n", encoding="utf-8")
        written[p] = f"content {name}\n"
    return written


def _ns(old, new, **kw):
    d = {"old_name": old, "new_name": new, "dry_run": False, "now": False,
         "apply": False, "root": None}
    d.update(kw)
    return argparse.Namespace(**d)


def _load_stage(root, old):
    return json.loads(
        (root / "sessions" / "seats" / f"{old}.rename.json").read_text())


def test_dry_run_prints_surfaces_touches_nothing(tmp_path):
    _geo(tmp_path, rows=[{"name": "old", "role": "kid"}])
    before = _session_files(tmp_path, "old")

    out = _capture_stdout(lambda: rotate.cmd_rename_post(
        _ns("old", "new", dry_run=True), tmp_path))
    assert f"{len(before)}" in out or "surfaces for old -> new" in out
    assert "dry-run, nothing changed" in out
    # nothing touched, no stage written
    for p in before:
        assert p.exists()
    assert not (tmp_path / "sessions" / "renames" / "old.rename.json").exists()


def test_apply_renames_session_surface_idempotent(tmp_path):
    _geo(tmp_path, rows=[{"name": "old", "role": "kid"}])
    before = _session_files(tmp_path, "old")

    rc = rotate.cmd_rename_post(_ns("old", "new", now=True), tmp_path)
    assert rc == 0, rc
    # every old-name session file is gone; new-name file exists with same bytes
    for p, content in before.items():
        assert not p.exists(), f"old surface left behind: {p}"
        newp = _renamed(p, "old", "new")
        assert newp.exists(), f"new surface missing: {newp}"
        assert newp.read_text() == content

    # idempotent: a second apply is a no-op, still exits 0, nothing renames
    rc2 = rotate.cmd_rename_post(_ns("old", "new", now=True), tmp_path)
    assert rc2 == 0, rc2
    for p, _ in before.items():
        assert not p.exists()
        assert _renamed(p, "old", "new").exists()


def test_now_refuses_live_pid_by_name(tmp_path):
    _geo(tmp_path, rows=[{"name": "old", "role": "kid", "pid": 4242}])
    _session_files(tmp_path, "old")
    rc = rotate.cmd_rename_post(_ns("old", "new", now=True), tmp_path)
    assert rc == 3, rc
    # nothing moved
    assert (tmp_path / "sessions" / "seats" / "old.key").exists()
    assert not (tmp_path / "sessions" / "seats" / "new.key").exists()


def test_default_stages_json_touches_surfaces(tmp_path):
    _geo(tmp_path, rows=[{"name": "old", "role": "kid"}])
    before = _session_files(tmp_path, "old")
    rc = rotate.cmd_rename_post(_ns("old", "new"), tmp_path)
    assert rc == 0, rc
    staged = _load_stage(tmp_path, "old")
    assert staged["new"] == "new"
    assert staged["ordered_by"] == "sanctuary-master"
    assert "staged_at" in staged
    assert len(staged["surfaces"]) >= len(before)
    # no surface touched
    for p in before:
        assert p.exists(), f"stage must not move {p}"


def test_dry_run_writes_no_stage_and_leaves_files(tmp_path):
    _geo(tmp_path, rows=[{"name": "old", "role": "kid"}])
    before = _session_files(tmp_path, "old")
    rc = rotate.cmd_rename_post(_ns("old", "new", dry_run=True), tmp_path)
    assert rc == 0
    assert not (tmp_path / "sessions" / "renames" / "old.rename.json").exists()
    for p in before:
        assert p.exists()


def test_stale_files_that_target_exists_are_skipped(tmp_path):
    """Idempotence at the per-file level: if the NEW name already holds a
    file, apply skips (never clobbers); the old file survives untouched."""
    _geo(tmp_path, rows=[{"name": "old", "role": "kid"}])
    before = _session_files(tmp_path, "old")
    dst = tmp_path / "sessions" / "seats" / "new.key"
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text("existing\n", encoding="utf-8")
    # seeds/... -- the same file listed above exists; just assert skip behavior
    rc = rotate.cmd_rename_post(_ns("old", "new", now=True), tmp_path)
    assert rc == 0, rc
    assert dst.read_text() == "existing\n"          # never clobbered
    old_src = tmp_path / "sessions" / "seats" / "old.key"
    assert old_src.exists()                          # kept (dst was taken)


def test_alias_resolution_in_find_seat(tmp_path, capsys):
    _geo(tmp_path, aliases={"old": "new"},
         rows=[{"name": "new", "role": "kid"}])
    row = rotate._find_seat(tmp_path, "old")
    assert row is not None and row["name"] == "new"
    assert "deprecated alias used: old -> new" in capsys.readouterr().err


def test_dry_run_lists_round2_surfaces_not_applied(tmp_path):
    _geo(tmp_path, rows=[{"name": "old", "role": "kid"},
                         {"name": "new", "role": "kid",
                          "rotated_by": "old"}])
    _session_files(tmp_path, "old")
    # dry-run shows row + branch + tmux surfaces as round 2
    out = _capture_stdout(lambda: rotate.cmd_rename_post(
        _ns("old", "new", dry_run=True), tmp_path))
    assert "row old name -> row new name" in out
    assert "branch: season2/posts/old -> season2/posts/new" in out
    assert "tmux window: old -> new" in out
    # apply does NOT touch config/branch/tmux surfaces (they are seamed/shipped)
    out2 = _capture_stdout(lambda: rotate.cmd_rename_post(
        _ns("old", "new", now=True), tmp_path))
    assert "shipped" in out2 and "git-seam" in out2


def test_dry_run_lists_dm_sidecar_and_edges(tmp_path):
    """Round 2 P5: dry-run lists dm log + .state.json sidecar FILE and its
    JSON KEY + alerts.edges key/value -- surfaces round 1 never listed."""
    _geo(tmp_path, aliases={"old": "new"}, rows=[{"name": "old"}])
    cdir = tmp_path / "comms" / "season-2" / "dm"
    cdir.mkdir(parents=True, exist_ok=True)
    (cdir / "buddy--old.md").write_text("hi\n", encoding="utf-8")
    (cdir / "buddy--old.md.state.json").write_text(
        json.dumps({"old": 1, "other": 2}), encoding="utf-8")
    rpm = tmp_path / "nodes" / ".geometry" / "rotations.md"
    rpm.parent.mkdir(parents=True, exist_ok=True)
    rpm.write_text("---\nid: config:rotations\nalerts:\n  audit: [x]\n"
                   "  edges:\n    old: [x, old]\n  silent: []\n---\n",
                   encoding="utf-8")
    out = _capture_stdout(lambda: rotate.cmd_rename_post(
        _ns("old", "new", dry_run=True), tmp_path))
    assert "dm log" in out and "dm state file" in out
    assert "dm state key" in out
    assert "alerts.edges key" in out and "alerts.edges value" in out
    assert "dry-run, nothing changed" in out


def test_apply_renames_dm_and_sidecar_keys_idempotent(tmp_path):
    """Apply renames the dm log + its .state.json sidecar FILE on disk and
    rewrites the sidecar's JSON KEY old->new; a second apply is a no-op."""
    _geo(tmp_path, rows=[{"name": "old"}])
    cdir = tmp_path / "comms" / "season-2" / "dm"
    cdir.mkdir(parents=True, exist_ok=True)
    log = cdir / "buddy--old.md"
    log.write_text("hi\n", encoding="utf-8")
    side = cdir / "buddy--old.md.state.json"
    side.write_text(json.dumps({"old": 1, "other": 2}), encoding="utf-8")

    rc = rotate.cmd_rename_post(_ns("old", "new", now=True), tmp_path)
    assert rc == 0, rc
    assert not log.exists() and (cdir / "buddy--new.md").exists()
    assert not side.exists() and (cdir / "buddy--new.md.state.json").exists()
    data = json.loads((cdir / "buddy--new.md.state.json").read_text())
    assert "new" in data and "old" not in data and data["other"] == 2

    rc2 = rotate.cmd_rename_post(_ns("old", "new", now=True), tmp_path)
    assert rc2 == 0, rc2                      # idempotent
    assert not log.exists() and (cdir / "buddy--new.md").exists()


def test_boundary_stage_path_is_seats(tmp_path):
    """Default stage lands at .agi/sessions/seats/<old>.rename.json, NOT
    renames/ (round 1 deviation the claim's path fixes)."""
    _geo(tmp_path, rows=[{"name": "old"}])
    _session_files(tmp_path, "old")
    rc = rotate.cmd_rename_post(_ns("old", "new"), tmp_path)
    assert rc == 0, rc
    stage = tmp_path / "sessions" / "seats" / "old.rename.json"
    assert stage.exists()
    assert not (tmp_path / "sessions" / "renames" / "old.rename.json").exists()
    assert json.loads(stage.read_text())["new"] == "new"


def test_apply_staged_seats_successor_under_new_name(tmp_path):
    """Boundary apply: _apply_staged applies the staged surfaces in ONE pass
    so the successor seats under the NEW name (never mid-generation); a
    second call is a no-op because the stage is consumed/absent."""
    _geo(tmp_path, rows=[{"name": "old"}])
    before = _session_files(tmp_path, "old")
    rotate.cmd_rename_post(_ns("old", "new"), tmp_path)   # stage
    rc = rotate._apply_staged(tmp_path, "old")
    assert rc == 0, rc
    for p, content in before.items():
        assert not p.exists(), f"left old surface: {p}"
        newp = _renamed(p, "old", "new")
        assert newp.exists() and newp.read_text() == content
    assert not (tmp_path / "sessions" / "seats" / "old.rename.json").exists()
    assert rotate._apply_staged(tmp_path, "old") == 0   # stage gone -> no-op


def test_alias_resolves_in_send_and_prints(tmp_path, capsys):
    """Round 2 P3: send.py resolves old->new through the SAME aliases table
    and prints `deprecated alias used`; send/read/peek/whois/wake all route
    through _alias_canon."""
    from agi.bin import send
    _geo(tmp_path, aliases={"old": "new"}, rows=[{"name": "new"}])
    assert send._alias_canon(tmp_path, "old") == "new"
    assert "deprecated alias used: old -> new" in capsys.readouterr().err
    assert send._alias_canon(tmp_path, "new") is None   # canonical, no print
    assert "old -> new" not in capsys.readouterr().err


def test_branch_deleted_only_under_delete_old(tmp_path):
    """The old branch is deleted ONLY under --delete-old: without it the
    seam records branch -m + the ADDITIVE mirror of the new tip but NO
    `:old` delete; with it the `push origin :old` delete is recorded too.
    goal:g15.25 (1)+(2): the post head is never pushed as a head -- the
    rename-apply mirrors to refs/agi/posts/<new> and proves it."""
    _geo(tmp_path, rows=[{"name": "old"}])
    surfaces = rotate._rename_surfaces(tmp_path, "old", "new")
    calls = []
    rec = lambda *a: calls.append(a)          # noqa: E731
    rc, _ = rotate._apply_surfaces(tmp_path, surfaces, run_git=rec,
                                   run_tmux=lambda *a: calls.append(("T",) + a))
    git_calls = [c for c in calls if c[0] != "T"]
    assert ("branch", "-m", "season2/posts/old", "season2/posts/new") in git_calls
    assert ("push", "origin", "season2/posts/new:refs/agi/posts/new") \
        in git_calls, git_calls
    assert not any(c[0] == "push" and len(c) == 3 and c[2].startswith(":")
                   for c in git_calls), "old branch deleted without --delete-old"
    calls2 = []
    rotate._apply_surfaces(tmp_path, surfaces, delete_old=True,
                           run_git=lambda *a: calls2.append(a),
                           run_tmux=lambda *a: None)
    assert ("push", "origin", "season2/posts/new:refs/agi/posts/new") in calls2
    assert ("push", "origin", ":season2/posts/old") in calls2
    # never a bare head push of the post branch
    assert not any(c[0] == "push" and len(c) == 3
                   and c[2] == "season2/posts/new"
                   for c in calls2), calls2


def test_apply_never_writes_config(tmp_path):
    """Round NEVER writes config: posts.md (the row surface) is unchanged by
    apply; row cells are printed as write.py lines, not edited."""
    _geo(tmp_path, rows=[{"name": "old"}])
    posts = tmp_path / "nodes" / ".geometry" / "posts.md"
    before = posts.read_bytes()
    _session_files(tmp_path, "old")
    rc = rotate.cmd_rename_post(_ns("old", "new", now=True), tmp_path)
    assert rc == 0, rc
    assert posts.read_bytes() == before, "config was written by the round"


def test_load_alerts_rewrites_edges_keys_and_values(tmp_path):
    """Round 2 P4: _load_alerts rewrites alerts.edges KEY and VALUE members
    through the aliases table at READ time (no config edit at rename)."""
    _geo(tmp_path, aliases={"old": "new"}, rows=[{"name": "new"}])
    rpm = tmp_path / "nodes" / ".geometry" / "rotations.md"
    rpm.parent.mkdir(parents=True, exist_ok=True)
    rpm.write_text("---\nid: config:rotations\nalerts:\n  audit: [old]\n"
                   "  edges:\n    old: [x, old]\n  silent: [old]\n---\n",
                   encoding="utf-8")
    alerts = rotate._load_alerts(tmp_path)
    assert alerts["edges"] == {"new": ["x", "new"]}
    assert alerts["audit"] == ["new"] and alerts["silent"] == ["new"]



def _renamed(p: Path, old: str, new: str) -> Path:
    return p.parent / (p.name.replace(old, new, 1))


def _capture_stdout(fn):
    import io
    from contextlib import redirect_stdout
    buf = io.StringIO()
    with redirect_stdout(buf):
        fn()
    return buf.getvalue()


def test_apply_staged_applies_with_live_pid_on_own_row(tmp_path):
    """DEFECT-1 fix (KID 3): _apply_staged must apply even when the OLD row
    itself carries a live pid -- at the boundary the rotating predecessor IS
    that live holder. It applies unconditionally, consumes the stage, and a
    second call is a no-op. The --now/--apply operator verb (not this path)
    owns the live-pid refusal."""
    _geo(tmp_path, rows=[{"name": "old", "role": "kid", "pid": 9999}])
    before = _session_files(tmp_path, "old")
    rotate.cmd_rename_post(_ns("old", "new"), tmp_path)   # stage
    rc = rotate._apply_staged(tmp_path, "old")
    assert rc == 0, rc      # applies despite <old> holding a live pid
    for p, content in before.items():
        assert not p.exists(), f"left old surface: {p}"
        newp = _renamed(p, "old", "new")
        assert newp.exists() and newp.read_text() == content
    assert not (tmp_path / "sessions" / "seats" / "old.rename.json").exists()
    assert rotate._apply_staged(tmp_path, "old") == 0   # stage gone -> no-op


def test_apply_staged_malformed_stage_returns_1(tmp_path):
    """DEFECT-1: a malformed stage is refused with exit 1, not applied and
    not silently consumed."""
    _geo(tmp_path, rows=[{"name": "old"}])
    seats = tmp_path / "sessions" / "seats"
    seats.mkdir(parents=True, exist_ok=True)
    (seats / "old.rename.json").write_text("{not json", encoding="utf-8")
    assert rotate._apply_staged(tmp_path, "old") == 1
    assert (seats / "old.rename.json").exists()


def test_tmux_seam_renames_by_resolved_id(tmp_path):
    """DEFECT-2 fix (KID 3): the tmux seam resolves each surface's NAME to
    its numeric @id/$id from the injected listing, then renames/set-options
    by THAT id -- never by '@<name>'. window -> @N (list-windows), session ->
    $N (list-sessions), stream-follow -> its window @N."""
    _geo(tmp_path, rows=[{"name": "old"}])
    surfaces = rotate._rename_surfaces(tmp_path, "old", "new")
    tmux_calls = []

    def rec(*a):
        cmd = a[0]
        if cmd == "list-windows":
            return "@3 sensei-director\n@5 old\n@9 other\n"
        if cmd == "list-sessions":
            return "$1 agi-rc\n$4 view-old\n$6 view-other\n"
        tmux_calls.append(a)

    rotate._apply_surfaces(tmp_path, surfaces, run_git=lambda *a: None,
                           run_tmux=rec)
    assert ("rename-window", "-t", "@5", "new") in tmux_calls
    assert ("rename-session", "-t", "$4", "view-new") in tmux_calls
    assert any(a[0] == "set-option" and a[2] == "@5"
               for a in tmux_calls), "stream-follow must resolve to its @id"
    # NEVER a name-shaped target: no @<name> / $<name>
    assert not any(a[0].startswith("rename-") and
                   (a[2].startswith("@") or a[2].startswith("$")) and
                   a[2][1:].isalpha()
                   for a in tmux_calls)


def test_tmux_seam_no_match_skips_by_name(tmp_path, capsys):
    """DEFECT-2: when the injected listing holds no name match, the surface
    is skipped BY NAME (no rename emitted, no @<name> attempted)."""
    _geo(tmp_path, rows=[{"name": "old"}])
    surfaces = rotate._rename_surfaces(tmp_path, "old", "new")
    renames = []

    def rec(*a):
        if a[0] in ("list-windows", "list-sessions"):
            return "$1 agi-rc\n@7 unconnected\n"
        renames.append(a)

    applied, skipped = rotate._apply_surfaces(
        tmp_path, surfaces, run_git=lambda *a: None, run_tmux=rec)
    assert not renames, f"no rename should fire without a name match: {renames}"
    assert "not live" in capsys.readouterr().err


def test_default_apply_calls_subprocess_zero_times(tmp_path, monkeypatch):
    """KID 4 the gap: WITHOUT --live, the --now/--apply path must call
    subprocess.run ZERO times -- git/tmux ride the print-only seams, so a
    caller who does not opt into --live can never execute a real rename."""
    calls = []
    monkeypatch.setattr(rotate.subprocess, "run",
                        lambda *a, **k: calls.append(a))
    _geo(tmp_path, rows=[{"name": "old"}])
    _session_files(tmp_path, "old")
    rc = rotate.cmd_rename_post(
        argparse.Namespace(old_name="old", new_name="new", dry_run=False,
                           now=True, apply=False, root=None,
                           delete_old=False, live=False),
        tmp_path)
    assert rc == 0, rc
    assert calls == [], f"default path must not subprocess.run: {calls}"


def test_live_apply_runs_real_git_argv(tmp_path, monkeypatch, capsys):
    """KID 4 + goal:g15.25 (2): with --live, --apply injects REAL git/tmux
    executors routed through subprocess.run. The worktree move and the
    branch -m arrive; the post head is NEVER pushed -- the new tip is
    mirrored to refs/agi/posts/new and proved by ls-remote -- and only then
    the --delete-old `push origin :old`. tmux list-windows feeds the @id
    resolution so rename-window fires by id."""
    _geo(tmp_path, rows=[{"name": "old"}])
    _session_files(tmp_path, "old")
    rec = []
    sha = "a1b2c3d4e5f6a1b2c3d4e5f6a1b2c3d4e5f6a1b2"

    def fake_run(cmd, *a, **k):
        rec.append(tuple(cmd))
        # a name-bearing tmux listing lets _resolve_tmux_id find the @id
        if cmd[0] == "tmux" and cmd[1] == "list-windows":
            return type("R", (), {"stdout": "@5 old\n@7 other\n",
                                   "stderr": "", "returncode": 0})()
        if cmd[0] == "tmux" and cmd[1] == "list-sessions":
            return type("R", (), {"stdout": "$1 agi-rc\n$4 view-old\n",
                                   "stderr": "", "returncode": 0})()
        if cmd[0] == "git" and "rev-parse" in cmd:
            if "--show-toplevel" in cmd:
                return type("R", (), {"stdout": str(tmp_path) + "\n",
                                       "stderr": "", "returncode": 0})()
            return type("R", (), {"stdout": sha + "\n", "stderr": "",
                                   "returncode": 0})()
        if cmd[0] == "git" and "ls-remote" in cmd:
            return type("R", (), {
                "stdout": f"{sha}\trefs/agi/posts/new\n", "stderr": "",
                "returncode": 0})()
        return type("R", (), {"stdout": "", "stderr": "",
                               "returncode": 0})()

    monkeypatch.setattr(rotate.subprocess, "run", fake_run)
    rc = rotate.cmd_rename_post(
        argparse.Namespace(old_name="old", new_name="new", dry_run=False,
                           now=True, apply=False, root=None,
                           delete_old=True, live=True),
        tmp_path)
    assert rc == 0, rc
    # git: worktree move + branch -m + the mirror push/prove (+ origin delete)
    assert ("git", "-C", str(tmp_path), "worktree", "move",
            ".agi/worktrees/post-old", ".agi/worktrees/post-new") in rec
    assert ("git", "-C", str(tmp_path), "branch", "-m",
            "season2/posts/old", "season2/posts/new") in rec
    assert ("git", "-C", str(tmp_path), "push", "origin",
            f"{sha}:refs/agi/posts/new") in rec
    assert ("git", "-C", str(tmp_path), "ls-remote", "origin",
            "refs/agi/posts/new") in rec
    assert ("git", "-C", str(tmp_path), "push", "origin",
            ":season2/posts/old") in rec, "--delete-old must push :old"
    assert ("git", "-C", str(tmp_path), "push", "origin",
            "season2/posts/new") not in rec, "a post head was pushed"
    # tmux window resolved to @5 and renamed by that id
    tmux = [c for c in rec if c[0] == "tmux"]
    assert ("tmux", "rename-window", "-t", "@5", "new") in tmux
    assert ("tmux", "rename-session", "-t", "$4", "view-new") in tmux
    assert "[LIVE]" in capsys.readouterr().out


def test_live_git_echoes_nonzero_rc_loudly(tmp_path, monkeypatch, capsys):
    """KID 4: a failed live git command (rc != 0) prints the command + rc and
    raises, so a caller cannot mistake a failed rename for success."""
    def fake_run(cmd, *a, **k):
        if cmd[0] == "git" and cmd[3] == "branch" and cmd[4] == "-m":
            return type("R", (), {"stdout": "",
                                   "stderr": "fatal: not a git repo\n",
                                   "returncode": 128})()
        return type("R", (), {"stdout": "", "stderr": "",
                               "returncode": 0})()
    monkeypatch.setattr(rotate.subprocess, "run", fake_run)
    with pytest.raises(RuntimeError) as ei:
        rotate._live_git(tmp_path, "branch", "-m", "a", "b")
    assert "failed (rc 128)" in str(ei.value)
    assert "git branch -m a b -> rc 128" in capsys.readouterr().err


def test_live_never_runs_in_boundary_apply_default(tmp_path):
    """KID 4: _apply_staged's DEFAULT (no injected executors) keeps the
    print-only seams -- the boundary apply only renames files, never git/
    tmux, unless a privileged caller injects _live_git/_live_tmux."""
    _geo(tmp_path, rows=[{"name": "old"}])
    before = _session_files(tmp_path, "old")
    rotate.cmd_rename_post(_ns("old", "new"), tmp_path)   # stage
    rc = rotate._apply_staged(tmp_path, "old")
    assert rc == 0, rc
    for p, content in before.items():
        assert not p.exists()
        assert _renamed(p, "old", "new").exists()
    assert not (tmp_path / "sessions" / "seats" / "old.rename.json").exists()