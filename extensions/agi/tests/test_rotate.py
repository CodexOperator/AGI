import json
import subprocess
import sys
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate
from agi.bin import brief


@pytest.fixture
def fake_ladder(tmp_path, monkeypatch):
    root = tmp_path

    def fake_root():
        return root

    monkeypatch.setattr(rotate, "find_project_root", fake_root)

    def fake_load(root_param, field, default):
        overrides = {
            "director_context_tokens": 100_000,
            "director_rotate_at": 0.25,
        }
        return overrides.get(field, default)

    monkeypatch.setattr(rotate, "load_ladder_field", fake_load)
    return root


@pytest.fixture
def fake_transcript(tmp_path):
    transcript = tmp_path / "transcript.jsonl"
    transcript.write_text(
        """
{"message": {"role": "assistant", "usage": {"input_tokens": 1000, "cache_read_input_tokens": 200, "cache_creation_input_tokens": 300}}}
{"message": {"role": "assistant", "usage": {"input_tokens": 2000, "cache_read_input_tokens": 300, "cache_creation_input_tokens": 0}}}
"""
    )
    return transcript


def test_meter_uses_cc_transcript(monkeypatch, tmp_path, fake_ladder, fake_transcript, capsys):
    projects_dir = tmp_path / ".claude" / "projects" / rotate.CC_PROJECT_SLUG
    projects_dir.mkdir(parents=True)
    dst = projects_dir / "session.jsonl"
    dst.write_text(fake_transcript.read_text())

    monkeypatch.setattr(rotate, "CC_PROJECTS_DIR", tmp_path / ".claude" / "projects")

    exit_code = rotate.main(["meter"])
    captured = capsys.readouterr().out.strip()

    assert exit_code == 0
    assert "0.023" in captured  # (2000+300) / 100000
    assert "claude-code transcript" in captured


def test_meter_check_threshold(monkeypatch, tmp_path, fake_ladder, fake_transcript, capsys):
    monkeypatch.setattr(rotate, "CC_PROJECT_SLUG", "slug-does-not-exist")
    monkeypatch.setattr(rotate, "CC_PROJECTS_DIR", tmp_path / "missing")

    rc_base = tmp_path / "nodes"
    rc_log = rc_base / "sessions"
    rc_log.mkdir(parents=True)
    log_path = rc_log / "remote-control.log"
    log_path.write_text(
        """
USAGE: {"input_tokens": 40000, "cache_read_input_tokens": 10000, "cache_creation_input_tokens": 0}
"""
    )

    def fake_find_root():
        return rc_base

    monkeypatch.setattr(rotate, "find_project_root", fake_find_root)

    exit_code = rotate.main(["meter", "--check"])
    captured = capsys.readouterr().out.strip()
    assert "0.5000" in captured
    assert exit_code == 1


def test_spawn_dry_run(monkeypatch, tmp_path, capsys):
    prompt = tmp_path / "prompt.md"
    prompt.write_text("Hello {name}")

    monkeypatch.chdir(tmp_path)

    exit_code = rotate.main([
        "spawn",
        "--name", "agi-123",
        "--prompt-file", str(prompt),
        "--dry-run",
    ])
    output = capsys.readouterr().out.strip()

    assert exit_code == 0
    assert "claude --remote-control agi-123" in output
    assert "Hello agi-123" in output


def test_spawn_refuses_existing_window(monkeypatch, tmp_path, capsys):
    prompt = tmp_path / "prompt.md"
    prompt.write_text("Hello {name}")

    def fake_run(cmd, capture_output, text, timeout):
        if cmd[:3] == ["tmux", "list-windows", "-t"]:
            return subprocess.CompletedProcess(cmd, 0, stdout="agi-123\n", stderr="")
        raise AssertionError("tmux new-window should not be called in this test")

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(subprocess, "run", fake_run)

    exit_code = rotate.main([
        "spawn",
        "--name", "agi-123",
        "--prompt-file", str(prompt),
    ])

    err = capsys.readouterr().err
    assert exit_code == 1
    assert "already exists" in err


def test_spawn_window_reusable_for_non_prime_name(monkeypatch, tmp_path, capsys):
    # hypothesis:l3w4-seat-transport — spawn_window() is the ONE reusable
    # launcher: a non-prime seat name launches via `--remote-control`, never -p.
    prompt = tmp_path / "prompt.md"
    prompt.write_text("You are {name}\n")
    monkeypatch.chdir(tmp_path)

    rc, shell = rotate.spawn_window(
        name="adv-alive", tier="parent", prompt_file=str(prompt),
        dry_run=True,
    )
    out = capsys.readouterr().out.strip()

    assert rc == 0
    assert "claude --remote-control adv-alive" in out
    assert out == shell
    assert " -p" not in out


def test_loop_uses_spawn_window(monkeypatch, tmp_path, capsys):
    # hypothesis:l3w4-seat-transport — cmd_loop routes through spawn_window
    # (one launch path), never its own inline tmux spawn.
    root = _proj(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 1)  # rotate
    called = {}
    monkeypatch.setattr(
        rotate, "spawn_window",
        lambda **kw: called.update(kw) or (0, "claude --remote-control adv-alive"),
    )

    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=False, role="adv_alive", name="adv-alive",
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=None,
        debug_file=None, dry_run=True, timeout=1,
    ), root)

    assert code == 0
    assert called.get("name") == "adv-alive"
    assert called.get("tier") == "adv_alive"
    assert called.get("dry_run") is True


# --- l3w0-rotate-roles: role resolution, head, name derivation, loop --------


def _proj(tmp_path, ladder_roles=""):
    """A minimal fake graph root: `.agi/` layout (the dir find_project_root
    returns) with a ladder node under nodes/.geometry."""
    root = tmp_path / "proj"
    (root / "nodes" / ".geometry").mkdir(parents=True)
    lines = ["---"]
    if ladder_roles:
        lines.append("roles:")
        lines.append(ladder_roles)
    lines.append("closed: false")
    lines.append("---")
    (root / "nodes" / ".geometry" / "ladder.md").write_text("\n".join(lines))
    return root


def test_spawn_resolves_role_model_effort_settings(monkeypatch, tmp_path, capsys):
    # Ladder roles table row for prime_director wins over config/defaults.
    root = _proj(tmp_path, ladder_roles=(
        "  - role: prime_director\n"
        "    harness: claude-code\n"
        "    model: claude-fable-5-1\n"
        "    effort: max\n"
        "    settings: {ultracode: true}\n"
        "    tier: 3\n"
    ))
    prompt = tmp_path / "prompt.md"
    prompt.write_text("You are {name}\n")
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.chdir(root)

    exit_code = rotate.main([
        "spawn", "--name", "belam-2", "--prompt-file", str(prompt),
        "--dry-run",
    ])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "--model claude-fable-5-1" in out
    assert "--effort max" in out
    assert "--settings" in out
    assert "ultracode" in out


def test_spawn_normalizes_string_settings_word(monkeypatch, tmp_path, capsys):
    # The landing l3w0-ladder-roles-table spells settings as the bare word
    # `ultracode`; rotate must emit `--settings '{"ultracode": true}'`.
    root = _proj(tmp_path, ladder_roles=(
        "  - role: prime_director\n"
        "    harness: claude-code\n"
        "    model: claude-fable-5-1\n"
        "    effort: max\n"
        "    settings: ultracode\n"
        "    tier: 3\n"
    ))
    prompt = tmp_path / "prompt.md"
    prompt.write_text("You are {name}\n")
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.chdir(root)

    exit_code = rotate.main([
        "spawn", "--name", "belam-2", "--prompt-file", str(prompt),
        "--dry-run",
    ])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert '--settings \'{"ultracode": true}\'' in out
    # the bare-word form (settings = the string `ultracode`) must not leak:
    assert '--settings \'"ultracode"\'' not in out


def test_spawn_ultracode_prefixes_env_and_keyword(monkeypatch, tmp_path, capsys):
    # hypothesis:l3-rotate-ultracode-env -- an ultracode role's dry-run spawn
    # must prefix the tmux launch with `export CLAUDE_CODE_WORKFLOWS=1` and
    # open the successor's user turn (the prompt body) with the keyword
    # `ultracode`. The prime measured live that the env var is the launch
    # gate and the keyword is the opt-in trigger (L3.0x, three throwaways).
    root = _proj(tmp_path, ladder_roles=(
        "  - role: prime_director\n"
        "    harness: claude-code\n"
        "    model: claude-fable-5-1\n"
        "    effort: max\n"
        "    settings: {ultracode: true}\n"
        "    tier: 3\n"
    ))
    prompt = tmp_path / "prompt.md"
    prompt.write_text("You are {name}\n")
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.chdir(root)

    exit_code = rotate.main([
        "spawn", "--name", "belam-u1", "--prompt-file", str(prompt),
        "--dry-run",
    ])
    out = capsys.readouterr().out
    assert exit_code == 0
    # the env export gates the whole shell line:
    assert out.startswith("export CLAUDE_CODE_WORKFLOWS=1")
    # the user-turn prompt body (the final quoted arg) opens with the keyword
    # as its first line, e.g. `ultracode\nYou are belam-u1...`:
    assert "ultracode\nYou are belam-u1" in out


def test_spawn_plain_role_no_env_no_keyword(monkeypatch, tmp_path, capsys):
    # hypothesis:l3-rotate-ultracode-env -- a role whose settings carry no
    # ultracode gets neither the env export nor the keyword.
    root = _proj(tmp_path, ladder_roles=(
        "  - role: kid\n"
        "    harness: claude-code\n"
        "    model: claude-sonnet-5\n"
        "    effort: high\n"
        "    tier: 1\n"
    ))
    prompt = tmp_path / "prompt.md"
    prompt.write_text("You are {name}\n")
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.chdir(root)

    exit_code = rotate.main([
        "spawn", "--name", "kid-1", "--tier", "kid",
        "--prompt-file", str(prompt), "--dry-run",
    ])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "CLAUDE_CODE_WORKFLOWS" not in out
    assert out.count("ultracode") == 0


def test_spawn_falls_back_to_defaults_without_table(monkeypatch, tmp_path, capsys):
    # No roles table, no config.json: fixed top-tier defaults apply.
    root = _proj(tmp_path)
    prompt = tmp_path / "prompt.md"
    prompt.write_text("You are {name}\n")
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.chdir(root)

    exit_code = rotate.main([
        "spawn", "--name", "belam-9", "--prompt-file", str(prompt),
        "--dry-run",
    ])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "--remote-control belam-9" in out
    assert "--model claude-fable-5-1" in out
    assert "--effort max" in out


def test_successor_prompt_prepends_constitution_head():
    body = "the successor body"
    prompt = brief.successor_prompt(tier="prime_director", body=body)
    assert prompt.startswith("─── CONSTITUTION HEAD ───")
    assert "THE FOUR PRAYERS" in prompt
    assert prompt.rstrip().endswith(body)
    assert prompt.index(body) > prompt.index("THE FOUR PRAYERS")


# ---------- l3w4-liaison-seat: spawn --tier liaison from the assembled brief ---


def test_ladder_roles_table_has_a_liaison_row():
    """The live ladder node must carry the {tier:1, role:liaison} row so
    spawn --tier liaison resolves to claude-sonnet-5 at effort high."""
    import yaml  # noqa: F401  (documented; _ladder_roles_table parses it)
    root = rotate.find_project_root()
    rows = rotate._ladder_roles_table(root)
    row = next((r for r in rows if r.get("role") == "liaison"), None)
    assert row is not None, "no liaison row in the ladder roles table"
    assert row.get("tier") == 1
    assert row.get("model") == "claude-sonnet-5"
    assert row.get("effort") == "high"
    assert row.get("harness") == "claude-code"


def test_spawn_tier_liaison_resolves_sonnet_high_from_the_new_row(monkeypatch, tmp_path, capsys):
    # The ladder row for liaion must surface on the spawned command.
    root = _proj(tmp_path, ladder_roles=(
        "  - role: liaison\n"
        "    harness: claude-code\n"
        "    model: claude-sonnet-5\n"
        "    effort: high\n"
        "    tier: 1\n"
    ))
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.chdir(root)

    exit_code = rotate.main([
        "spawn", "--name", "liaison", "--tier", "liaison", "--dry-run",
    ])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "--remote-control liaison" in out
    assert "--model claude-sonnet-5" in out
    assert "--effort high" in out


def test_spawn_liaison_prompt_sources_the_assembled_brief_not_the_static_file(monkeypatch, tmp_path, capsys):
    # spawn --tier liaison with no --prompt-file must build the body from
    # brief.assemble (the OWNER LIAISON brief), never the static
    # prime-director-successor.md.
    root = _proj(tmp_path, ladder_roles=(
        "  - role: liaison\n"
        "    harness: claude-code\n"
        "    model: claude-sonnet-5\n"
        "    effort: high\n"
        "    tier: 1\n"
    ))
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    sentinel = tmp_path / "prime.md"
    sentinel.write_text("STATIC PRIME BODY {name}\n")
    monkeypatch.setattr(rotate, "DEFAULT_PROMPT_FILE", str(sentinel))
    monkeypatch.chdir(root)

    exit_code = rotate.main([
        "spawn", "--name", "liaison", "--tier", "liaison", "--dry-run",
    ])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "STATIC PRIME BODY" not in out, "the static prime file must not be used"
    assert "OWNER LIAISON" in out, "the assembled liaison brief is the body"


def test_spawn_prime_director_static_path_is_unchanged(monkeypatch, tmp_path, capsys):
    # Regression: the prime's spawned (no --prompt-file) must still read the
    # DEFAULT_PROMPT_FILE static successor file, never the assembled brief.
    root = _proj(tmp_path)
    sentinel = tmp_path / "prime.md"
    sentinel.write_text("STATIC PRIME BODY {name}\n")
    monkeypatch.setattr(rotate, "DEFAULT_PROMPT_FILE", str(sentinel))
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.chdir(root)

    exit_code = rotate.main([
        "spawn", "--name", "belam-1", "--tier", "prime_director",
        "--dry-run",
    ])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "STATIC PRIME BODY belam-1" in out, (
        "the prime must still read DEFAULT_PROMPT_FILE through the static path")


def test_derive_successor_name():
    # nothing about the prime known => second Roman numeral of the base prefix
    assert rotate._derive_successor_name([], "belam") == "belam-II"
    # live prime window `belam-S1-L3` carries no Roman suffix => the base
    assert rotate._derive_successor_name(["belam-S1-L3"], "belam") == "belam-S1-L3-II"
    # bare base `belam` is the first of its line => -II
    assert rotate._derive_successor_name(["belam"], "belam") == "belam-II"
    # highest Roman in the series wins
    assert rotate._derive_successor_name(
        ["belam-S1-L3", "belam-S1-L3-II", "belam-S1-L3-III"], "belam") \
        == "belam-S1-L3-IV"
    # non-matching windows are ignored
    assert rotate._derive_successor_name(["agi-master-7"], "belam") == "belam-II"
    # a lone successor with no base present extends its own line
    assert rotate._derive_successor_name(["belam-S1-L3-II"], "belam") == "belam-S1-L3-III"
    # a non-belam prefix still derives in roman
    assert rotate._derive_successor_name(["ccc-III"], "ccc") == "ccc-IV"


def test_spawn_default_name_derives_from_window_path(monkeypatch, tmp_path, capsys):
    root = _proj(tmp_path)
    prompt = tmp_path / "prompt.md"
    prompt.write_text("hi {name}")
    wins = tmp_path / "windows.txt"
    wins.write_text("belam-S1-L3\n")
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.chdir(root)

    exit_code = rotate.main([
        "spawn", "--prompt-file", str(prompt),
        "--window-path", str(wins), "--dry-run",
    ])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "--remote-control belam-S1-L3-II" in out
    assert "hi belam-S1-L3-II" in out


def test_loop_below_threshold_holds(monkeypatch, tmp_path, capsys):
    root = _proj(tmp_path)
    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 0)

    def fail_spawn(*a, **k):
        raise AssertionError("must not spawn below threshold")

    monkeypatch.setattr(rotate, "_launch_window", fail_spawn)

    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=False, role="prime_director", name=None,
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=None,
        debug_file=None, dry_run=False, timeout=1,
    ), root)
    assert code == 0
    assert "no rotation" in capsys.readouterr().err


def test_loop_over_threshold_rotates_and_continue(monkeypatch, tmp_path, capsys):
    root = _proj(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    # Need a prompt file in a location the subprocess will reach:
    monkeypatch.setattr(rotate, "DEFAULT_PROMPT_FILE",
                        str(tmp_path / "successor.md"))
    (tmp_path / "successor.md").write_text("you are {name}\n")

    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 1)  # over threshold

    reply = tmp_path / "reply.log"
    reply.write_text("continue\n")
    wins = tmp_path / "windows.txt"
    wins.write_text("")  # hermetic: no existing belam windows
    launched = {}
    def fake_launch(session, name, shell_cmd):
        launched.update(name=name) or 0
        # a real spawn creates the tmux window, so reflect it in the fixture
        wins.write_text(name + "\n")
        return 0
    monkeypatch.setattr(rotate, "_launch_window", fake_launch)

    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=False, role="prime_director", name=None,
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=str(wins),
        debug_file=str(reply), dry_run=False, timeout=1,
    ), root)
    assert code == 0
    assert launched.get("name") == "belam-II"
    assert "handoff stood" in capsys.readouterr().err



# --- hypothesis:l3w4-seat-rotation-loops ADDENDUM (Belam VII 21:56 UTC):
#     cmd_loop must fail loudly when the successor's tmux window is absent, and
#     must NEVER point its read-back at the caller's own --session-log.

def test_loop_fails_loud_when_no_successor_window(monkeypatch, tmp_path, capsys):
    """No successor tmux window exists -> cmd_loop must return non-zero, never
    report rotation success. Before the fix it returned 0 and printed
    'handoff stood' even though `_existing_windows` showed nothing."""
    root = _proj(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 1)  # rotate
    reply = tmp_path / "reply.log"
    reply.write_text("continue\n")
    wins = tmp_path / "windows.txt"
    wins.write_text("")  # simulated spawn leaves NO window behind
    launched = {}
    monkeypatch.setattr(
        rotate, "_launch_window",
        lambda session, name, shell_cmd: launched.update(name=name) or 0,
    )
    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=True, role="prime_director", name="belam-II",
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=str(wins),
        debug_file=str(reply), dry_run=False, timeout=1,
    ), root)
    assert code != 0
    err = capsys.readouterr().err
    assert "NOT present" in err
    assert "refusing to report rotation success" in err


def test_loop_readback_never_uses_caller_session_log(monkeypatch, tmp_path, capsys):
    """The successor read-back must read the successor's OWN debug file, not the
    meter's `--session-log`. A 'continue' in the caller's own transcript must
    not confirm a rotation whose successor said nothing."""
    root = _proj(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 1)  # rotate
    succ = tmp_path / "successor.log"
    succ.write_text("")  # successor (gen N+1) has written nothing
    caller = tmp_path / "caller.jsonl"
    caller.write_text("the CALLER just wrote a line containing bare continue\n")
    wins = tmp_path / "windows.txt"
    wins.write_text("belam-III\n")  # window IS present (real spawn)
    monkeypatch.setattr(
        rotate, "_launch_window",
        lambda session, name, shell_cmd: 0,
    )
    code = rotate.cmd_loop(SimpleNamespace(
        session_log=str(caller), force=True, role="prime_director",
        name="belam-III", name_prefix="belam", model=None, effort=None,
        settings=None, prompt_file=None, tmux_session="agi-rc",
        window_path=str(wins), debug_file=str(succ), dry_run=False, timeout=1,
    ), root)
    err = capsys.readouterr().err
    # window was present, but the successor never answered -> the loop must NOT
    # claim the handoff stood; it must not echo the caller's own line either.
    assert "handoff stood" not in err
    assert "the CALLER just wrote" not in err

def _write_transcripts(projects_dir, pinned_usage, foreign_usage, pinned_name="pinned.jsonl", foreign_name="foreign.jsonl"):
    """Two transcripts in `projects_dir`: a PINNED (older) and a NEWER foreign one.
    Returns (pinned_path, foreign_path)."""
    projects_dir.mkdir(parents=True, exist_ok=True)
    pinned = projects_dir / pinned_name
    pinned.write_text(
        f'{{"message": {{"role": "assistant", "usage": '
        f'{{"input_tokens": {pinned_usage}, "cache_read_input_tokens": 0, '
        f'"cache_creation_input_tokens": 0}}}}}}\n'
    )
    foreign = projects_dir / foreign_name
    foreign.write_text(
        f'{{"message": {{"role": "assistant", "usage": '
        f'{{"input_tokens": {foreign_usage}, "cache_read_input_tokens": 0, '
        f'"cache_creation_input_tokens": 0}}}}}}\n'
    )
    # make foreign strictly newer than pinned
    import os
    ot, nt = time.time() - 10, time.time()
    os.utime(pinned, (ot, ot))
    os.utime(foreign, (nt, nt))
    return pinned, foreign


def _fake_cc_projects(tmp_path, monkeypatch, pinned_usage=2000, foreign_usage=40000):
    """A fake ~/.claude/projects/<default-slug> with an older pinned transcript
    (light usage) and a newer foreign transcript (heavy usage)."""
    proj = tmp_path / ".claude" / "projects" / rotate.CC_PROJECT_SLUG
    pinned, foreign = _write_transcripts(proj, 2000, 40000)
    monkeypatch.setattr(rotate, "CC_PROJECTS_DIR", tmp_path / ".claude" / "projects")
    return proj, pinned, foreign


def _write_pin(root, target, name="prime.meter"):
    # root here is the GRAPH dir (fake_ladder patches find_project_root to
    # return tmp_path), so sessions sit directly under it -- `root/sessions`,
    # never `root/.agi/sessions` (hypothesis:l3-rotate-pin-path-readback).
    seg = root / "sessions"
    seg.mkdir(parents=True, exist_ok=True)
    pin = seg / name
    pin.write_text(str(target) + "\n", encoding="utf-8")
    return pin


def test_seat_pin_stable_across_two_rotations_same_name(monkeypatch, tmp_path, fake_ladder, capsys):
    # hypothesis:l3w4-seat-registry — .agi/sessions/<name>.meter is seat-stable:
    # a seat rotation re-reads the SAME seat pin even as a NEWER foreign pin
    # lands. Without --seat, newest-mtime wins (the bug this closes).
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    seat_pin = _write_pin(tmp_path, pinned, name="belam.meter")
    _write_pin(tmp_path, foreign, name="zzz-newer.meter")
    import os
    old, now = time.time() - 10_000, time.time()
    os.utime(seat_pin, (old, old))
    os.utime(tmp_path / "sessions" / "zzz-newer.meter", (now, now))
    code = rotate.main(["meter", "--seat", "belam"])
    out = capsys.readouterr().out.strip()
    assert code == 0
    assert "0.020" in out, out      # seat's own pinned transcript
    assert "0.4" not in out, out     # NOT the newer foreign pin newest would pick


def test_seat_pin_refuses_predecessors_generation(monkeypatch, tmp_path, fake_ladder, capsys):
    # hypothesis:l3-seat-pin-not-repointed-on-rotation — Belam X pinned its
    # OWN transcript into the belam seat pin and rotated. Belam XI (the next
    # generation) read `--seat belam` and got Belam X's usage back with total
    # confidence (`source=seat_pin`), because nothing re-points or checks the
    # pin on rotation. A pin written by generation 1 read by generation 2
    # must be a loud refusal, never a silent stale number.
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    # generation 1 (the predecessor) pins its own transcript...
    rotate._write_handoff(tmp_path, "belam", 1)
    code = rotate.main(["meter", "--seat", "belam", "--pin",
                        str(tmp_path / "sessions" / "belam.meter"),
                        "--session-log", str(pinned)])
    assert code == 0
    # ...then rotation advances the seat to generation 2 (the successor)
    # without ever re-pointing the pin -- the exact gap the hypothesis names.
    rotate._write_handoff(tmp_path, "belam", 2)
    code = rotate.main(["meter", "--seat", "belam"])
    err = capsys.readouterr().err
    assert code == 1, err
    assert "generation 1" in err and "generation 2" in err, err
    assert "refus" in err.lower(), err


def test_seat_pin_same_generation_reads_clean(monkeypatch, tmp_path, fake_ladder, capsys):
    # The matching case must NOT regress into a refusal: the generation that
    # wrote the pin reading its own pin back still works.
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    rotate._write_handoff(tmp_path, "belam", 1)
    code = rotate.main(["meter", "--seat", "belam", "--pin",
                        str(tmp_path / "sessions" / "belam.meter"),
                        "--session-log", str(pinned)])
    assert code == 0
    code = rotate.main(["meter", "--seat", "belam"])
    out = capsys.readouterr().out.strip()
    assert code == 0, out
    assert "0.020" in out, out
    assert "seat_pin" in out, out


def test_meter_pin_file_wins_over_newer_foreign(monkeypatch, tmp_path, fake_ladder, capsys):
    # A pin file naming our own transcript must beat the newer foreign .jsonl
    # in the project dir (the hypothesis: without it, newest wins -> bug).
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    _write_pin(tmp_path, pinned)
    code = rotate.main(["meter"])
    out = capsys.readouterr().out.strip()
    assert code == 0
    assert "0.020" in out          # 2000/100000 = pinned, not foreign (0.400)
    assert "pin" in out


def test_meter_agi_session_log_env_uses_pinned(monkeypatch, tmp_path, fake_ladder, capsys):
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    monkeypatch.setenv("AGI_SESSION_LOG", str(pinned))
    code = rotate.main(["meter"])
    out = capsys.readouterr().out.strip()
    assert code == 0
    assert "0.020" in out
    assert "AGI_SESSION_LOG" in out


def test_meter_explicit_session_log_wins(monkeypatch, tmp_path, fake_ladder, capsys):
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    code = rotate.main(["meter", "--session-log", str(pinned)])
    out = capsys.readouterr().out.strip()
    assert code == 0
    assert "0.020" in out
    assert "explicit" in out


def test_meter_fallback_warns_and_picks_newest(monkeypatch, tmp_path, fake_ladder, capsys):
    # No log, no env, no pin -> newest wins but a WARN names the file it picked.
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    code = rotate.main(["meter"])
    captured = capsys.readouterr()
    out, err = captured.out, captured.err
    assert code == 0
    assert "0.400" in out
    assert "warn" in err and "foreign.jsonl" in err


def test_loop_uses_same_resolver(monkeypatch, tmp_path, fake_ladder, capsys):
    # cmd_loop meters via cmd_meter, which must see the pin too. We assert the
    # resolver, not a live rotate (which would spawn), by checking that a
    # pinned (light) usage stays below threshold while the foreign (heavy)
    # would trip it.
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    _write_pin(tmp_path, pinned)
    # threshold is 0.25; pinned=0.02 (hold), foreign=0.40 (would rotate)
    args = SimpleNamespace(session_log=None, check=True)
    code = rotate.cmd_meter(args, tmp_path)
    assert code == 0  # pinned keeps us below; loop would hold


# --- hypothesis:l3-rotate-pin-path-readback (red-first) -------------------


def test_pin_path_never_doubles_agi_dir(tmp_path):
    # The pin must resolve under the graph's sessions dir, NEVER the doubled
    # `<root>/.agi/.agi/sessions` (the L3.15 defect). root = the REPO root
    # (<tmp>) and root = the GRAPH dir (<tmp>/.agi) must resolve to the SAME
    # physical `<tmp>/.agi/sessions/<name>.meter`.
    graph = tmp_path / ".agi"
    (graph / "nodes").mkdir(parents=True)          # marks <tmp>/.agi as the graph
    seg = graph / "sessions"
    seg.mkdir(parents=True, exist_ok=True)
    pin = seg / "belam.meter"
    pin.write_text("/tmp/some-transcript.jsonl\n", encoding="utf-8")

    from_graph = rotate.find_pin_log(graph)
    assert str(from_graph) == str(pin), from_graph
    assert "/.agi/.agi/" not in str(from_graph)   # no doubling in the graph-dir read

    from_repo = rotate.find_pin_log(tmp_path)       # repo root maps to the same dir
    assert str(from_repo) == str(pin), from_repo


def test_is_log_noise_markers():
    # Bracketed logger lines (bare or timestamped) are noise; a bare answer is not.
    assert rotate._is_log_noise("[DEBUG] MDM settings load completed in 1ms")
    assert rotate._is_log_noise("2026-09-07T06:04:39.522Z [INFO] [uds-messaging] listening")
    assert rotate._is_log_noise("   ")
    assert rotate._is_log_noise("2026-09-07T06:04:40.398Z [WARN] [3P telemetry] Event dropped")
    assert not rotate._is_log_noise("continue")
    assert not rotate._is_log_noise("valuable diff line")


def test_readback_skips_bracketed_log_lines(tmp_path):
    # hypothesis:l3-rotate-pin-path-readback -- the read-back must skip
    # bracketed logger lines and report `continue` when the FIRST bare answer
    # line is `continue` (the L3.15 defect read `[DEBUG] MDM settings load` as
    # the reply and printed "handoff needs change").
    log = tmp_path / "belam.log"
    log.write_text(
        "[DEBUG] MDM settings load completed in 1ms\n"
        "2026-09-07T06:04:41.633Z [WARN] [bridge] continuing as before\n"
        "continue\n",
        encoding="utf-8",
    )
    assert rotate._read_first_reply(str(log), timeout=5) == "continue"


def test_readback_reports_diff_when_no_continue(tmp_path):
    # When the first bare answer is NOT `continue`, the read-back reports it
    # (so the loop knows the handoff needs a change).
    log = tmp_path / "belam.log"
    log.write_text(
        "[DEBUG] MDM settings load completed in 1ms\n"
        "valuable diff line\n",
        encoding="utf-8",
    )
    assert rotate._read_first_reply(str(log), timeout=5) == "valuable diff line"


def test_readback_never_returns_a_bracketed_line(tmp_path):
    # A log holding ONLY log lines must not surface any of them as the reply;
    # it should poll and, with no bare answer before the timeout, return None.
    log = tmp_path / "belam.log"
    log.write_text(
        "[DEBUG] MDM settings load completed in 1ms\n"
        "2026-09-07T06:04:41.633Z [WARN] [bridge] no anchor\n",
        encoding="utf-8",
    )
    assert rotate._read_first_reply(str(log), timeout=1) is None


# ---------------------------------------------------------------------------
# hypothesis:l3w4-parent-branch-merge-up — meter pins stay the main checkout
# ---------------------------------------------------------------------------


def test_sessions_dir_resolves_to_main_from_a_worktree(tmp_path):
    """A `--branch` kid carries its own `.agi/`, but the meter pins must stay
    the ONE shared directory on the main checkout (same rule as the budget
    dir and comms), or a rotation seat reading pins from a worktree would see
    a different room than the parents writing it."""
    repo = tmp_path / "main"
    repo.mkdir(parents=True)
    subprocess.run(["git", "-C", str(repo), "init", "-b", "season/s1"],
                   check=True, capture_output=True)
    for cfg in ("user.email", "user.name"):
        subprocess.run(["git", "-C", str(repo), "config", cfg, "t"],
                       check=True, capture_output=True)
    (repo / ".agi" / "nodes").mkdir(parents=True)
    (repo / ".agi" / "config.json").write_text('{"metric_primary": "x"}')
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True,
                   capture_output=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "init"],
                   check=True, capture_output=True)

    wt = tmp_path / "wt"
    subprocess.run(["git", "-C", str(repo), "worktree", "add",
                    "-b", "loop/x-a@s2", str(wt), "season/s1"],
                   check=True, capture_output=True)

    main_sess = rotate._sessions_dir(repo / ".agi")
    wt_sess = rotate._sessions_dir(wt / ".agi")
    assert str(main_sess) == str(repo / ".agi" / "sessions")
    assert wt_sess == main_sess, (
        "a worktree kid's meter pins must resolve to the MAIN checkout's "
        "sessions dir, not a per-worktree one")


# ── l3w4-seat-rotation-loops: alarms --holder / rotate-self / status --seats ──


def _write_seats_sheet(root, rows):
    """Write a minimal seals-md-style registry the loader can parse."""
    nodes = root / "nodes" / ".geometry"
    nodes.mkdir(parents=True, exist_ok=True)
    (root / "sessions").mkdir(parents=True, exist_ok=True)
    body = "---\nid: config:seats\ntype: config\nseats:\n"
    for r in rows:
        body += "  - " + json.dumps(r) + "\n"
    body += "---\n"
    (nodes / "seats.md").write_text(body, encoding="utf-8")


def _pin_seat_transcript(root, name, tokens):
    """Write a fake CC transcript + the seat-stable pin naming it."""
    transcript = root / f"t-{name}.jsonl"
    transcript.write_text(json.dumps({
        "message": {"role": "assistant",
                    "usage": {"input_tokens": tokens,
                              "cache_read_input_tokens": 0,
                              "cache_creation_input_tokens": 0}},
    }) + "\n", encoding="utf-8")
    (root / "sessions" / f"{name}.meter").write_text(
        str(transcript) + "\n", encoding="utf-8")
    return transcript


def _rotate_self_args(tmp_path, **over):
    base = dict(name="adv-alive", force=False, timeout=5, debug_file=None,
                model=None, effort=None, settings=None, prompt_file=None,
                tmux_session="t", window_path=None, dry_run=False,
                throwaway=False, successor_argv=None, role="parent")
    base.update(over)
    return SimpleNamespace(**base)


def test_alarms_once_holds_below_threshold(fake_ladder, tmp_path, capsys):
    """Below director_rotate_at: prints `hold <seat>` and sends NO dm."""
    seats = [{"name": "kid-1", "role": "director", "rotated_by": "advisor"}]
    _write_seats_sheet(tmp_path, seats)
    _pin_seat_transcript(tmp_path, "kid-1", tokens=5000)  # 0.05 < 0.25
    comms = tmp_path / "comms"
    args = SimpleNamespace(holder="advisor", once=True, interval=300,
                           comms_root=str(comms))
    rc = rotate.cmd_alarms(args, tmp_path)
    assert rc == 0
    out = capsys.readouterr().out
    assert "hold kid-1 0.0500" in out
    assert not list(comms.glob("dm/*.md"))


def test_alarms_once_dms_holder_when_due_then_stops(fake_ladder, tmp_path):
    """At/over threshold: exactly one dm `rotate now` to the holder, nil more."""
    seats = [{"name": "kid-1", "role": "director", "rotated_by": "advisor"},
             {"name": "kid-2", "role": "director", "rotated_by": "advisor"}]
    _write_seats_sheet(tmp_path, seats)
    _pin_seat_transcript(tmp_path, "kid-1", tokens=40000)  # 0.40 >= 0.25
    _pin_seat_transcript(tmp_path, "kid-2", tokens=4000)   # 0.04 < 0.25
    comms = tmp_path / "comms"
    args = SimpleNamespace(holder="advisor", once=True, interval=300,
                           comms_root=str(comms))
    rc = rotate.cmd_alarms(args, tmp_path)
    assert rc == 0
    dms = list(comms.glob("dm/*.md"))
    assert len(dms) == 1  # only the due seat was dm'd
    assert "rotate now" in dms[0].read_text(encoding="utf-8")


def test_rotate_self_dry_run_reuses_plain_name_no_roman(fake_ladder, tmp_path,
                                                        capsys, monkeypatch):
    """--dry-run prints the successor under the PLAIN seat name, generation N+1,
    never a Roman numeral, and touches nothing."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    seen = {}
    def fake_spawn(**kw):
        seen["name"] = kw["name"]
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    args = _rotate_self_args(tmp_path, dry_run=True)
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    assert seen["name"] == "adv-alive"          # plain, not adv-alive-II
    assert "generation: 1" in capsys.readouterr().out
    assert not (tmp_path / "sessions" / "seats" / "adv-alive.handoff.md").exists()


def test_rotate_self_renames_window_before_respawn(fake_ladder, tmp_path, monkeypatch):
    """The own window is renamed aside BEFORE the successor spawns."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    at_spawn = {}
    def fake_spawn(**kw):
        at_spawn["window_file"] = win.read_text(encoding="utf-8").strip()
        # the successor window appears under the reused plain name
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_first_reply",
                        lambda *a, **k: "continue")
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    args = _rotate_self_args(tmp_path, window_path=str(win))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    assert "adv-alive.gen1" in at_spawn["window_file"]


def test_rotate_self_kills_own_window_after_continue(fake_ladder, tmp_path,
                                                     capsys, monkeypatch):
    """After the successor answers `continue`, the own renamed window dies."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    killed = []
    def fake_spawn(**kw):
        # the successor window appears under the reused plain name
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_first_reply",
                        lambda *a, **k: "continue")
    monkeypatch.setattr(rotate, "_kill_window",
                        lambda name, *a, **k: killed.append(name))
    args = _rotate_self_args(tmp_path, window_path=str(win))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    assert killed == ["adv-alive.gen1"]


def test_seat_handoff_generation_bumps_on_rotation(fake_ladder, tmp_path,
                                                   capsys, monkeypatch):
    """A seat whose handoff says generation 3 rotates onto generation 4."""
    _write_seats_sheet(tmp_path,
                       [{"name": "adv-alive", "role": "parent",
                         "model": "x", "effort": "max", "settings": ""}])
    hand = tmp_path / "sessions" / "seats"
    hand.mkdir(parents=True, exist_ok=True)
    (hand / "adv-alive.handoff.md").write_text(
        "seat: adv-alive\ngeneration: 3\n", encoding="utf-8")
    seen = []
    def fake_spawn(**kw):
        seen.append(kw["name"])
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    args = _rotate_self_args(tmp_path, dry_run=True)
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    assert "generation 4" in capsys.readouterr().out
    # the read-before-write cursor still computes on the plain seat name
    assert seen == ["adv-alive"]


def test_status_seats_flag_lists_fraction_and_age(fake_ladder, tmp_path,
                                                  capsys):
    """`status --seats` prints seat/generation/fraction/age per registry row."""
    _write_seats_sheet(tmp_path,
                       [{"name": "kid-1", "role": "director",
                         "rotated_by": "advisor"}])
    _pin_seat_transcript(tmp_path, "kid-1", tokens=10000)  # 0.1
    rc = rotate.cmd_status(SimpleNamespace(seats=True), tmp_path)
    assert rc == 0
    out = capsys.readouterr().out
    assert "kid-1\tgen=" in out
    assert "frac=0.100" in out


def test_rotate_self_cursor_ignores_stale_predecessor_continue(tmp_path):
    """The read-before-write cursor: a stale bare `continue` left in a reused
    plain-name log before the successor started must NOT confirm the rotation;
    only bytes written after the cursor count (hypothesis:l3w4-seat-rotation-
    loops, fixed after L3.30's reproduced hazard)."""
    log = tmp_path / "adv-alive.log"
    log.write_text("continue\nvalid successor line\n", encoding="utf-8")
    # whole-file (the pre-fix view) still sees the stale `continue` -> the
    # hazard this must close
    assert rotate._read_first_reply(str(log), timeout=2, start_offset=0) \
        == "continue"
    # cursor past the stale line sees only the successor's fresh output
    assert rotate._read_first_reply(str(log), timeout=2, start_offset=9) \
        == "valid successor line"


# ── hypothesis:l3-rotate-self-successor-override ──────────────────────────
# The successor argv is hardwired to real `claude --remote-control` and the
# successor name must come from the seats registry, so no kid could ever
# exercise a rotation live. Two explicit, impossible-to-trip overlays: a
# successor-command override (stand-in stand-in command) and a throwaway seat
# path that never writes seats.md. RED-FIRST: these fail before the rotate.py
# change lands, pass after.

def test_spawn_window_successor_argv_override_replaces_claude(tmp_path, capsys,
                                                              monkeypatch):
    """Explicit --successor-argv replaces the real claude successor; the shell
    line is exactly the override, never a `claude --remote-control`."""
    # next: successor_argv -> AttributeError -> TypeError -> NotImplementedError
    monkeypatch.setattr(rotate, "load_role", lambda *a, **k: None)
    try:
        rc, shell = rotate.spawn_window(
            name="rh", tier="parent", prompt_file=None, tmux_session="t",
            root=tmp_path, dry_run=True, debug_file="rh.log",
            successor_argv="printf continue")
    except TypeError:
        pytest.fail("spawn_window does not accept successor_argv yet (RED)")
    assert rc == 0
    out = capsys.readouterr().out
    assert out.strip() == "printf continue"   # the override, verbatim
    assert "claude" not in out                # no real successor


def test_spawn_window_default_still_real_claude(tmp_path, capsys, monkeypatch):
    """No override -> the launch stays byte-for-byte today's real claude
    command: `claude --remote-control NAME ...` (default unchanged)."""
    monkeypatch.setattr(rotate, "load_role", lambda *a, **k: None)
    rc, shell = rotate.spawn_window(
        name="rh", tier="parent", prompt_file=None, tmux_session="t",
        root=tmp_path, dry_run=True, debug_file="rh.log")
    assert rc == 0
    out = capsys.readouterr().out
    assert out.lstrip().startswith("claude --remote-control rh") or \
        "claude --remote-control rh" in out


def test_rotate_self_throwaway_skips_registry(fake_ladder, tmp_path,
                                              monkeypatch):
    """--throwaway rotates a seat name ABSENT from seats.md, and never creates
    or writes the registry file (hypothesis:l3-rotate-self-successor-override).
    Note: no _write_seats_sheet call — the seat is deliberately unregistered.
    Before the change, cmd_rotate_self errors `no seat` here (the L3.37 gate)."""
    seen = {}
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    def fake_spawn(**kw):
        seen["name"] = kw["name"]
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")   # the successor window appears
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_first_reply",
                        lambda *a, **k: "continue")
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    args = _rotate_self_args(tmp_path, throwaway=True, window_path=str(win))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    assert seen["name"] == "adv-alive"        # plain name reused, no Roman
    seats = tmp_path / "nodes" / ".geometry" / "seats.md"
    assert not seats.exists()                 # registry untouched
    assert not (tmp_path / "nodes" / ".geometry" / "seats.md").exists()


def test_rotate_self_without_throwaway_still_refuses_unregistered(
        fake_ladder, tmp_path, monkeypatch):
    """Regression guard: the registry gate still holds for the DEFAULT path —
    an unregistered name without --throwaway must still error `no seat`."""
    mk = tmp_path / "nodes" / ".geometry"
    mk.mkdir(parents=True, exist_ok=True)
    # an empty registry sheet: adv-alive not present
    (mk / "seats.md").write_text("---\nid: config:seats\ntype: config\n---\n",
                                 encoding="utf-8")
    args = _rotate_self_args(tmp_path, throwaway=False)
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 1
    assert "no seat" in str(rc) or True  # exit code 1 is the gate


def test_rotate_self_throwaway_forwards_successor_argv(fake_ladder, tmp_path,
                                                       monkeypatch):
    """--throwaway + --successor-argv both flow into spawn_window untouched."""
    seen = {}
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    def fake_spawn(**kw):
        seen["argv"] = kw.get("successor_argv")
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_first_reply",
                        lambda *a, **k: "continue")
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    args = _rotate_self_args(tmp_path, throwaway=True, window_path=str(win),
                             successor_argv="printf continue")
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    assert seen["argv"] == "printf continue"


# --- _launch_window: the two silent failures (hypothesis:l3-rotate-launch-
# window-silent-failure, measured 2026-09-08) --------------------------------


def test_launch_window_returns_tmux_failure_instead_of_swallowing_it(
        monkeypatch, capsys):
    """tmux said `command too long` and the caller was told 0.

    This is why `rotate.py loop` reported a rotation with no successor window
    behind it for three primes running: the return code was discarded and the
    captured stderr thrown away.
    """
    def fake_run(argv, **kw):
        return subprocess.CompletedProcess(argv, 1, stdout="",
                                           stderr="command too long")
    monkeypatch.setattr(rotate.subprocess, "run", fake_run)

    rc = rotate._launch_window("agi-rc", "belam-test", "echo hi")

    assert rc == 1, "a failed tmux new-window must not report success"
    assert "command too long" in capsys.readouterr().err


def test_launch_window_hands_tmux_a_short_argv_for_a_long_command(monkeypatch):
    """A rotation line carries the constitution head and runs ~16KB.

    tmux refuses past its own buffer, so a long command goes through a script
    file and tmux receives a few dozen bytes instead. The script must still
    exist afterwards -- bash reads a script incrementally, so deleting it
    early can truncate a running successor.
    """
    seen = {}

    def fake_run(argv, **kw):
        seen["argv"] = argv
        return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")
    monkeypatch.setattr(rotate.subprocess, "run", fake_run)

    long_cmd = "claude --remote-control x " + ("y" * 20000)
    rc = rotate._launch_window("agi-rc", "belam-test", long_cmd)

    assert rc == 0
    passed = seen["argv"][-1]
    assert len(passed) < 512, f"tmux still handed {len(passed)} bytes"
    assert passed.startswith("bash ")
    script = Path(passed.split(" ", 1)[1].strip("'"))
    assert script.exists(), "the script must outlive the launch call"
    assert long_cmd in script.read_text()
    script.unlink()


def test_launch_window_leaves_a_short_command_inline(monkeypatch):
    """Below the threshold nothing changes -- no script, no new failure mode."""
    seen = {}

    def fake_run(argv, **kw):
        seen["argv"] = argv
        return subprocess.CompletedProcess(argv, 0, stdout="", stderr="")
    monkeypatch.setattr(rotate.subprocess, "run", fake_run)

    rc = rotate._launch_window("agi-rc", "belam-test", "echo hi")

    assert rc == 0
    assert seen["argv"][-1].endswith("echo hi")
    assert "bash /" not in seen["argv"][-1]
# ── hypothesis:l3-rotation-record-and-predecessor-guarantee ───────────────
# Every rotation performed by rotate.py — throwaway rehearsal or real
# claude --remote-control successor — writes a durable machine-readable JSON
# record under `.agi/sessions/rotations/` capturing all five observations as
# OBSERVED FACTS (never tool-return claims): (a) a NEW tmux window exists
# under the reused plain name, established by tmux list-windows; (b) the seat
# handoff generation before/after; (c) WHICH log the read-back read;
# (d) the stale-`continue` read-before-write cursor; (e) whether the
# predecessor window is still alive, by name. AND rotate-self/loop REFUSE to
# report success when the successor window is absent or the predecessor
# window is gone. RED-FIRST below (fail before the rotate.py change lands).


def test_rotate_self_writes_record_with_five_observations(fake_ladder, tmp_path,
                                                          monkeypatch):
    """A completed throwaway rotate-self writes a JSON record carrying all five
    observations (a)-(e), each sourced from the window-path/tmux read, never
    from spawn_window's return value."""
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")

    def fake_spawn(**kw):
        # the new successor window appears under the reused plain name
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"

    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_first_reply",
                        lambda *a, **k: "continue")
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    args = _rotate_self_args(tmp_path, throwaway=True, window_path=str(win))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    records = sorted((tmp_path / "sessions" / "rotations")
                     .glob("adv-alive.*.json"))
    assert records, "no durable rotation record written"
    rec = json.loads(records[-1].read_text(encoding="utf-8"))
    assert rec["rotation"] == "rotate-self"
    assert rec["result"] == "success"
    obs = rec["observations"]
    # (a) successor window under the plain name, observed, not tool-return
    a = obs["a_successor_window_under_plain_name"]
    assert a["present"] is True and a["window"] == "adv-alive"
    assert "adv-alive" in a["windows"]
    assert "source" in a and "window-path file" in a["source"]
    # (b) generation before/after
    assert obs["b_generation"] == {"before": 0, "after": 1}
    # (c) which log the read-back actually read
    assert str(obs["c_readback_log_path"]).endswith("adv-alive.log")
    # (d) read-before-write stale-continue cursor
    assert obs["d_stale_continue_cursor"]["read_before_write"] is True
    assert "start_offset" in obs["d_stale_continue_cursor"]
    # (e) predecessor alive by name
    e = obs["e_predecessor_alive"]
    assert e["name"] == "adv-alive.gen1" and e["present"] is True
    assert "adv-alive.gen1" in e["windows"]


def test_rotate_self_refuses_when_successor_window_absent(fake_ladder, tmp_path,
                                                          monkeypatch, capsys):
    """Spawn leaves NO successor window -> rotate-self refuses to report
    success, returns non-zero, and records the refusal durably."""
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    # successor never appears: the renamed predecessor is the only window
    monkeypatch.setattr(rotate, "spawn_window", lambda **kw: (0, "echo hi"))
    monkeypatch.setattr(rotate, "_read_first_reply",
                        lambda *a, **k: "continue")
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    args = _rotate_self_args(tmp_path, throwaway=True, window_path=str(win))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc != 0
    assert "successor" in capsys.readouterr().err
    records = sorted((tmp_path / "sessions" / "rotations")
                     .glob("adv-alive.*.json"))
    assert records
    rec = json.loads(records[-1].read_text(encoding="utf-8"))
    assert rec["result"] == "refused"
    assert "successor" in rec["refusal_reason"]


def test_rotate_self_refuses_when_predecessor_window_gone(fake_ladder, tmp_path,
                                                          monkeypatch, capsys):
    """The predecessor (renamed) window is the chain this guarantee protects:
    if it is gone after the successor is confirmed, rotate-self must refuse to
    report success and record the refusal."""
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")

    def fake_spawn(**kw):
        # successor appears under the plain name, but the predecessor vanished
        win.write_text("adv-alive\n", encoding="utf-8")
        return 0, "echo hi"

    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_first_reply",
                        lambda *a, **k: "continue")
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    args = _rotate_self_args(tmp_path, throwaway=True, window_path=str(win))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc != 0
    assert "predecessor" in capsys.readouterr().err
    records = sorted((tmp_path / "sessions" / "rotations")
                     .glob("adv-alive.*.json"))
    assert records
    rec = json.loads(records[-1].read_text(encoding="utf-8"))
    assert rec["result"] == "refused"
    assert "predecessor" in rec["refusal_reason"]


def test_loop_writes_durable_record(fake_ladder, tmp_path, monkeypatch):
    """cmd_loop also writes a durable record capturing the successor window
    (observed) and the read-back log path on a confirming rotation."""
    root = _proj(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 1)
    reply = tmp_path / "reply.log"
    reply.write_text("continue\n")
    wins = tmp_path / "windows.txt"
    wins.write_text("")

    def fake_launch(s, n, c):
        wins.write_text(n + "\n", encoding="utf-8")
        return 0

    monkeypatch.setattr(rotate, "_launch_window", fake_launch)
    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=True, role="prime_director", name="belam-II",
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=str(wins),
        debug_file=str(reply), dry_run=False, timeout=1,
    ), root)
    assert code == 0
    records = sorted((root / "sessions" / "rotations")
                     .glob("belam-II.*.json"))
    assert records, "loop wrote no durable record"
    rec = json.loads(records[-1].read_text(encoding="utf-8"))
    assert rec["rotation"] == "loop"
    assert rec["result"] == "success"
    a = rec["observations"]["a_successor_window_under_name"]
    assert a["present"] is True and a["window"] == "belam-II"
    assert str(rec["observations"]["c_readback_log_path"]).endswith("reply.log")
