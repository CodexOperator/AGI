# test_rotate_pane_contract.py -- G7.31.2.2 / falsifier 1 (goal:g7.31.2.2):
# rotate / auto-rotation REUSES the same pane contract. The successor is
# spawned under the SAME plain seat name the predecessor held, through the ONE
# `spawn_window` + template seam; the predecessor window is renamed aside to
# the documented `<seat>.prev`; and no second per-harness argv builder for
# grok (or anyone) reappears in `rotate.py`.
#
# Fixtures are modelled on test_rotate_boundary_rename.py (faked `spawn_window`
# capturing `name=`, throwaway tmp_path, no live tmux).
import argparse
import contextlib as _c
import io
import json
import sys
from pathlib import Path
from types import SimpleNamespace

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


def _sessions(root, seat):
    for parent, name in [
        (root / "sessions" / "seats", f"{seat}.key"),
        (root / "sessions" / "seats", f"{seat}.handoff.md"),
        (root / "sessions" / "quorum", f"{seat}.md"),
        (root / "sessions" / "inbox", f"{seat}.md"),
    ]:
        parent.mkdir(parents=True, exist_ok=True)
        (parent / name).write_text(f"content {name}\n", encoding="utf-8")


def _graph_ready(root):
    """The marker + `self_row` schema carve-out the successor row write needs
    (same shape test_rotate_boundary_rename.py uses)."""
    (root / "agi-tree.config.json").write_text(
        '{"metric_primary": "x"}', encoding="utf-8")
    schemas = root / "context" / "schemas"
    schemas.mkdir(parents=True, exist_ok=True)
    (schemas / "[config].md").write_text(
        "---\nname: config\nwritten_by: [owner, prime_director]\n"
        "self_row: {list_key: seats, match_key: name, fields: [session_ref, "
        "session_name, session_id, generation, window, pid, pubkey, "
        "sig_scheme, enc_scheme, key_history, session_label]}\n---\nbody\n",
        encoding="utf-8")


def _ladder(root, monkeypatch):
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate, "load_ladder_field",
                        lambda r, f, d: {"director_context_tokens": 100_000,
                                         "director_rotate_at": 0.25}.get(f, d))
    g = root / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    (g / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\ntemplates:\n"
        "  parent: {brief_file: extensions/agi/briefs/parent-successor.md, "
        "steps: [handoff, spawn], telemetry: [seat]}\n---\n\nbody\n",
        encoding="utf-8")


def _rotate_self_args(**over):
    base = dict(name="adv-alive", force=False, timeout=5, debug_file=None,
                model=None, effort=None, settings=None, prompt_file=None,
                tmux_session="t", window_path=None, dry_run=False,
                throwaway=False, successor_argv=None, role="parent")
    base.update(over)
    return SimpleNamespace(**base)


def _err(fn):
    buf = io.StringIO()
    with _c.redirect_stderr(buf):
        rc = fn()
    return rc, buf.getvalue()


# ---- conjunct 1: the successor holds the SAME pane contract (WIRE) --------
def test_pane_name_reused_across_rotate_self(tmp_path, monkeypatch):
    """FALSIFIER CLASS: wire. Drive `cmd_rotate_self` with a faked
    `spawn_window` that captures `name=`. The successor must be spawned under
    the SAME plain seat name `S` (never a Roman numeral, never a bespoke argv
    path), and the predecessor window is renamed aside to the documented
    `<seat>.prev` successor rename."""
    import send as _send
    _graph_ready(tmp_path)
    _seats(tmp_path, [{"name": "adv-alive", "role": "parent", "model": "x",
                       "effort": "max", "settings": ""}])
    _sessions(tmp_path, "adv-alive")
    (tmp_path / "sessions" / "seats").mkdir(parents=True, exist_ok=True)
    _send._seat_key_path(tmp_path, "adv-alive").write_text(
        json.dumps({"scheme": "ed25519", "priv_hex": "00", "pub_hex": "00"}),
        encoding="utf-8")
    _ladder(tmp_path, monkeypatch)
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    seen = {}

    def _lines():
        return [ln.strip() for ln in win.read_text().splitlines() if ln.strip()]

    def fake_spawn(**kw):
        seen["name"] = kw["name"]
        # snapshot the window list the spawn ACTUALLY sees: step (2) renamed
        # the pre-seeded fixture line aside before step (3) spawns, so a
        # plain `adv-alive` here would mean the fixture, not the spawn.
        seen["pre_spawn"] = _lines()
        with open(win, "a", encoding="utf-8") as fh:
            fh.write(kw["name"] + "\n")
        seen["appended"] = [kw["name"]]
        return 0, "echo hi"

    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1,
                                         "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    rc, err = _err(lambda: rotate.cmd_rotate_self(
        _rotate_self_args(window_path=str(win), session_ref="adv-alive-9"),
        tmp_path))
    assert rc == 0, err
    # the successor arrives through spawn_window under the SAME plain name
    assert seen.get("name") == "adv-alive", seen
    # NOT VACUOUS (was: `"adv-alive" in names`, already true of the fixture
    # line before the spawn ran). The spawn APPENDED the plain name -- its
    # capture proves it -- and at spawn time step (2) had already renamed the
    # fixture line to `.prev`, so the plain name here cannot be the fixture's.
    assert seen.get("appended") == ["adv-alive"], seen
    assert "adv-alive" not in seen.get("pre_spawn", []), seen
    names = [ln.strip() for ln in win.read_text().splitlines() if ln.strip()]
    assert names.count("adv-alive") == 1, names
    # the predecessor is renamed aside (documented successor rename on this tip)
    assert "adv-alive.prev" in names, names


# ---- conjunct 4: the STAGED-RENAME branch of rotate-self (WIRE) -----------
def _stage_rename(root, old, new):
    """Stage `.agi/sessions/seats/<old>.rename.json` through the committed
    `rotate.cmd_rename_post` (never a hand-built plan), so the boundary's
    re-derived table and the staged table agree by construction."""
    ns = argparse.Namespace(old_name=old, new_name=new, dry_run=False,
                            now=False, apply=False, root=None)
    assert rotate.cmd_rename_post(ns, root) == 0
    return root / "sessions" / "seats" / f"{old}.rename.json"


def test_staged_rename_spawns_successor_under_new_name_and_prev(
        tmp_path, monkeypatch):
    """FALSIFIER CLASS: wire. With a `<seat>.rename.json` stage present, the
    (0.9) boundary branch of `cmd_rotate_self` applies it BEFORE the handoff
    and spawn: the successor arrives through the ONE `spawn_window` seam
    under the documented POST-rename name (`adv-renamed`, the stage's `new`),
    never the old name; the predecessor window is renamed aside to
    `<old>.prev` (the documented successor rename on this tip); and the stage
    is consumed. This covers the branch the node previously cited untested."""
    import send as _send
    _graph_ready(tmp_path)
    _seats(tmp_path, [{"name": "adv-alive", "role": "parent", "model": "x",
                       "effort": "max", "settings": ""}])
    _sessions(tmp_path, "adv-alive")
    (tmp_path / "sessions" / "seats").mkdir(parents=True, exist_ok=True)
    _send._seat_key_path(tmp_path, "adv-alive").write_text(
        json.dumps({"scheme": "ed25519", "priv_hex": "00", "pub_hex": "00"}),
        encoding="utf-8")
    _ladder(tmp_path, monkeypatch)
    (tmp_path / "sessions" / "quorum").mkdir(parents=True, exist_ok=True)
    (tmp_path / "sessions" / "quorum" / "adv-alive.md").write_text(
        "# card\n", encoding="utf-8")
    stage = _stage_rename(tmp_path, "adv-alive", "adv-renamed")
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    seen = {}

    def fake_spawn(**kw):
        seen["name"] = kw["name"]
        with open(win, "a", encoding="utf-8") as fh:
            fh.write(kw["name"] + "\n")
        return 0, "echo hi"

    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1,
                                         "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    rc, err = _err(lambda: rotate.cmd_rotate_self(
        _rotate_self_args(window_path=str(win), session_ref="adv-alive-9"),
        tmp_path))
    assert rc == 0, err
    # the successor holds the documented POST-rename name, through the ONE seam
    assert seen.get("name") == "adv-renamed", seen
    assert not stage.exists(), "boundary must consume the stage"
    names = [ln.strip() for ln in win.read_text().splitlines() if ln.strip()]
    assert "adv-renamed" in names, names
    # non-live seams rename the name the window ACTUALLY carries (`old`) aside
    assert "adv-alive.prev" in names, names
    assert "adv-alive" not in names, names


# ---- conjunct 2: no per-harness argv builder / zero grok (GATE-NEGATIVE) --
def test_rotate_has_no_per_harness_argv_builder():
    """FALSIFIER CLASS: gate / negative. There is ONE argv seam and it
    RENDERS a template (asserted by calling it, not by grepping prose)."""
    src = Path(rotate.__file__).read_text(encoding="utf-8")
    for forbidden in ("_build_claude_command", "_build_copilot_command",
                      "_build_pi_command", "_build_grok_command",
                      "_build_grokbot_command"):
        assert forbidden not in src, forbidden
    assert "grok" not in src.lower(), "a grok-specific path reappeared"
    # the ONE seam reaches `harness_template.render`: it RETURNS argv.
    argv = rotate._build_harness_command(
        "claude-code", name="S", prompt_text="hello", debug_file="d.log")
    assert argv[0] == "claude"
    assert argv[1:3] == ["--remote-control", "S"]
    assert argv[-1] == "hello"


# ---- conjunct 3: the honest edge -- grok has no rotate seat (AUTH-GATE) ---
def test_grok_seat_is_refused_by_name_no_template():
    """FALSIFIER CLASS: auth / gate. `grok-bot` is NOT a known harness and has
    NO template, so `_validate_harness` refuses it BY NAME. This is the
    goal:g7.31.1 prerequisite, NOT a second argv builder; no guessed
    `grok-bot.toml` is added here."""
    templates = (Path(rotate.__file__).resolve().parents[1] /
                 "templates" / "harness")
    assert "grok-bot" not in rotate._known_harnesses()
    assert not (templates / "grok-bot.toml").exists()
    rc, ret = rotate._validate_harness(None, "grok-bot")
    assert rc == 1 and ret == ""
    rc, err = _err(lambda: rotate._validate_harness(None, "grok-bot")[0])
    assert rc == 1, err
    assert "grok-bot" in err, err
    assert ("no harness" in err
            or "declared but rotate.py cannot build it" in err), err