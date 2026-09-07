import subprocess
import sys
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
    rc_log = rc_base / ".agi" / "sessions"
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


def test_derive_successor_name():
    assert rotate._derive_successor_name([], "belam") == "belam-1"
    # live prime window `belam-S1-L3` has no trailing integer => N=1
    assert rotate._derive_successor_name(["belam-S1-L3"], "belam") == "belam-2"
    assert rotate._derive_successor_name(["belam"], "belam") == "belam-2"
    assert (
        rotate._derive_successor_name(["belam-2", "belam-4", "belam"], "belam")
        == "belam-5"
    )
    assert rotate._derive_successor_name(["agi-master-7"], "belam") == "belam-1"
    assert rotate._derive_successor_name(["belam-3"], "belam") == "belam-4"


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
    assert "--remote-control belam-2" in out
    assert "hi belam-2" in out


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
    monkeypatch.setattr(
        rotate, "_launch_window",
        lambda session, name, shell_cmd: launched.update(name=name) or 0,
    )

    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=False, role="prime_director", name=None,
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=str(wins),
        debug_file=str(reply), dry_run=False, timeout=1,
    ), root)
    assert code == 0
    assert launched.get("name") == "belam-1"
    assert "handoff stood" in capsys.readouterr().err

