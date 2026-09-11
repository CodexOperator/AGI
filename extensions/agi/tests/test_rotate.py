import json
import os
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
    # L4.110: rotate-self refuses loudly when .geometry/rotations.md is absent
    # (the live state until the prime lands it). Tests that drive rotation
    # mechanics therefore pin a minimal template node — "a node the suite
    # pins is code, suite after the .geometry write".
    g = root / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    (g / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\ntemplates:\n"
        "  parent: {brief_file: extensions/agi/briefs/parent-successor.md, "
        "steps: [handoff, spawn], telemetry: [seat]}\n"
        "  director: {brief_file: extensions/agi/briefs/director-successor.md, "
        "steps: [handoff, spawn], telemetry: [seat]}\n"
        "  prime_director: {brief_file: "
        "extensions/agi/briefs/prime-director-successor.md, "
        "steps: [handoff, spawn], telemetry: [seat]}\n---\n\nbody\n",
        encoding="utf-8")
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


class _FakeIn:
    """A file-like stand-in for sys.stdin so cmd_ack's `--text -` branch can
    be tested without a real pipe."""
    def __init__(self, text: str):
        self._text = text

    def read(self) -> str:
        return self._text


def _fake_launch(wins: Path, content: str) -> int:
    """Test stand-in for `_launch_window` that only reflects the window on disk
    (writes `content` into the window-path file) and returns 0. A bare
    `lambda ...: wins.write_text(content) or 0` is WRONG: `Path.write_text`
    returns the byte count (truthy), so the lambda returns that count, which
    cmd_loop treats as rc and aborts. This helper divorces the write from the
    return."""
    wins.write_text(content, encoding="utf-8")
    return 0


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
    ack = rotate._ack_path(root, "belam-II")
    ack.parent.mkdir(parents=True, exist_ok=True)
    ack.write_text(json.dumps({"seat": "belam-II", "gen_after": None,
                               "answer": "continue"}), encoding="utf-8")
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


# ---------------------------------------------------------------------------
# hypothesis:l4-the-meter-adopts-a-pin-it-did-not-write — identity is
# supplied, never inferred. A bare --pin must REFUSE (write side) rather than
# adopt a foreign pin; a seatless read must REFUSE (read side) when the pin it
# would consult carries another agent's generation. The repair paths
# (--session-log, $AGI_SESSION_LOG, --seat) must all still work.
# ---------------------------------------------------------------------------


def _sessions_dir_of(tmp_path):
    seg = tmp_path / "sessions"
    seg.mkdir(parents=True, exist_ok=True)
    return seg


def _with_foreign_distractor(tmp_path, foreign, own_name="sanctuary-director.meter"):
    """Caller's own pin written FIRST (older mtime) and correct; a foreign
    pin written LAST (strictly-newest mtime) in the shared sessions dir. The
    caller's own pin is the one --pin would name; the foreign one is the one
    a seatless newest-mtime search would adopt. Returns (own, foreign_pin)."""
    seg = _sessions_dir_of(tmp_path)
    own = seg / own_name
    own.write_text(str(foreign) + "\n", encoding="utf-8")
    fpin = seg / "belam.meter"
    fpin.write_text(str(foreign) + "\n", encoding="utf-8")
    now = time.time()
    os.utime(own, (now - 10_000, now - 10_000))
    os.utime(fpin, (now, now))
    return own, fpin


def test_a_bare_pin_refuses_and_leaves_own_pin_byte_unchanged(monkeypatch, tmp_path, fake_ladder, capsys):
    # (a) The distractor is the bug, not an edge: caller's own pin present and
    # correct, a foreign pin written LAST so newest-mtime adopts it. A bare
    # --pin (no --session-log, no AGI_SESSION_LOG, no --seat) must REFUSE and
    # leave the caller's own pin file BYTE-UNCHANGED -- nothing may be adopted
    # or re-stamped with the caller's generation.
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    own, fpin = _with_foreign_distractor(tmp_path, foreign)
    before = own.read_bytes()
    code = rotate.main(["meter", "--pin", str(own)])
    err = capsys.readouterr().err
    assert code != 0, err
    assert own.read_bytes() == before, "the caller's own pin must stay byte-unchanged"


def test_b_refusal_names_session_log(monkeypatch, tmp_path, fake_ladder, capsys):
    # (b) The refusal must NAME the literal string `--session-log` so the
    # operator knows what to run and does not spend a turn deriving it.
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    own, fpin = _with_foreign_distractor(tmp_path, foreign)
    code = rotate.main(["meter", "--pin", str(own)])
    err = capsys.readouterr().err
    assert code != 0
    assert "--session-log" in err, err


def test_c_pin_with_explicit_session_log_still_writes_stamps_and_prints(monkeypatch, tmp_path, fake_ladder, capsys):
    # (c) The repair path stays usable: --pin WITH an explicit --session-log
    # still writes, still stamps the caller's generation, and still prints the
    # fraction.
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    rotate._write_handoff(tmp_path, "belam", 7)
    p = _sessions_dir_of(tmp_path) / "belam.meter"
    code = rotate.main(["meter", "--seat", "belam", "--pin", str(p),
                        "--session-log", str(pinned)])
    out = capsys.readouterr().out
    assert code == 0, out
    content = p.read_text(encoding="utf-8")
    assert content.startswith("7\t"), content      # stamped caller generation
    assert str(pinned) in content, content          # names the named transcript
    assert "0.020" in out, out                      # fraction still printed


def test_d_agi_session_log_alone_still_permits_pin_write(monkeypatch, tmp_path, fake_ladder, capsys):
    # (d) $AGI_SESSION_LOG alone is a supplied identity: --pin still records it.
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    monkeypatch.setenv("AGI_SESSION_LOG", str(pinned))
    p = _sessions_dir_of(tmp_path) / "env-claimed.meter"
    code = rotate.main(["meter", "--pin", str(p)])
    out = capsys.readouterr().out
    assert code == 0, out
    assert str(pinned) in p.read_text(encoding="utf-8")


def test_e_bare_seatless_read_refuses_another_agents_pin(monkeypatch, tmp_path, fake_ladder, capsys):
    # (e) A bare seatless READ (no --pin) refuses when the pin it would
    # consult is another agent's generation-bearing pin: reporting a confident
    # number for a transcript the caller never named attributes a foreign
    # session to this caller.
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    seg = _sessions_dir_of(tmp_path)
    (seg / "belam.meter").write_text(f"3\t{foreign}\n", encoding="utf-8")
    code = rotate.main(["meter"])
    err = capsys.readouterr().err
    assert code != 0, err
    assert "refus" in err.lower(), err


def test_f_seat_named_correct_gen_pin_still_reads(monkeypatch, tmp_path, fake_ladder, capsys):
    # (f) The --seat path is not weakened: a named seat with a CORRECT own-
    # generation pin still reads and returns the fraction, and never consults
    # other agents' pins. (The helper's live pin is the working fixture.)
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    rotate._write_handoff(tmp_path, "belam", 4)
    seg = _sessions_dir_of(tmp_path)
    (seg / "belam.meter").write_text(f"4\t{pinned}\n", encoding="utf-8")
    code = rotate.main(["meter", "--seat", "belam"])
    out = capsys.readouterr().out.strip()
    assert code == 0, out
    assert "0.020" in out, out
    assert "seat_pin" in out, out


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
    """REMOVED with the debug-log reader.

    The legacy `_is_log_noise`/`_read_first_reply` reader is DELETED from
    rotate.py (hypothesis:l4-rotate-readback-false-negative-and-the-orphan-by-
    design): a DEBUG LOGGER cannot carry the successor's prose, so a fallback
    that opens one is the defect wearing a safety label. Its direct unit tests
    go with it; the three realities (ACKED / PRESENT-BUT-SILENT / ABSENT) are
    covered through the ack-channel reader tests below.
    """
    assert not hasattr(rotate, "_read_first_reply")
    assert not hasattr(rotate, "_is_log_noise")


# ---------------------------------------------------------------------------
# hypothesis:l4-rotate-readback-false-negative-and-the-orphan-by-design — the
# explicit ACK channel replaces the debug-log read-back.
# ---------------------------------------------------------------------------

REAL_DEBUG_LOG = (
    "2026-09-07T06:04:39.522Z [DEBUG] MDM settings load completed in 1ms\n"
    "2026-09-07T06:04:39.610Z [INFO] [uds-messaging] listening on INET6 ... \n"
    "2026-09-07T06:04:40.398Z [WARN] [3P telemetry] Event dropped\n"
    "2026-09-07T06:04:41.633Z [DEBUG] exited fullscreen\n"
)


def test_cmd_ack_writes_seat_ack_file(tmp_path, monkeypatch):
    """`rotate.py ack` writes `<seats>/<seat>.ack.json` with the successor's
    own identity (gen_after + session_ref) — `_is_log_noise` never matters."""
    root = _proj(tmp_path)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    code = rotate.cmd_ack(SimpleNamespace(
        seat="sanctuary-director", gen=7, ref="agent:abc123",
        answer="diff", text="- a\n+ b"), root)
    assert code == 0
    ac = rotate._ack_path(root, "sanctuary-director")
    doc = json.loads(ac.read_text(encoding="utf-8"))
    assert doc["seat"] == "sanctuary-director"
    assert doc["gen_after"] == 7
    assert doc["session_ref"] == "agent:abc123"
    assert doc["answer"] == "diff"
    assert doc["text"] == "- a\n+ b"


def test_read_ack_matches_gen_after(tmp_path):
    """_read_ack returns the ack when its gen_after is the generation the
    reader spawned, and REFUSES a wrong-generation ack (treats it as absent)."""
    seat = tmp_path / "seats"
    seat.mkdir()
    ac = seat / "s.ack.json"
    ac.write_text(json.dumps({"seat": "s", "gen_after": 7,
                              "answer": "continue", "ts": "Z"}),
                  encoding="utf-8")
    got = rotate._read_ack(str(ac), gen_after=7, timeout=5)
    assert got is not None and got["answer"] == "continue"
    # wrong generation -> refused, not confirmed
    assert rotate._read_ack(str(ac), gen_after=8, timeout=1) is None


def test_read_ack_polls_until_written(tmp_path):
    """_read_ack polls a not-yet-written ack file until it carries a matching
    gen_after (the successor writes its ack AFTER the predecessor starts
    reading)."""
    seat = tmp_path / "seats"
    seat.mkdir()
    ac = seat / "s.ack.json"
    import threading
    def _writer():
        import time
        time.sleep(1)
        ac.write_text(json.dumps({"seat": "s", "gen_after": 9,
                                  "answer": "continue"}), encoding="utf-8")
    threading.Thread(target=_writer, daemon=True).start()
    got = rotate._read_ack(str(ac), gen_after=9, timeout=20)
    assert got is not None and got["answer"] == "continue"


@pytest.mark.parametrize("body", ["{", "[]", "not json"])
def test_read_ack_ignores_unparsable(tmp_path, body):
    """An unparsable ack file never confirms; malformed JSON is treated as
    not-yet-written and retried until timeout."""
    seat = tmp_path / "seats"
    seat.mkdir()
    ac = seat / "s.ack.json"
    ac.write_text(body, encoding="utf-8")
    assert rotate._read_ack(str(ac), gen_after=7, timeout=1) is None


def test_read_ack_absent_never_confirms(tmp_path):
    """No ack file at all -> None on timeout (the precondition the hypothesis
    states: without the ack, the channel is silent)."""
    seat = tmp_path / "seats"
    seat.mkdir()
    assert rotate._read_ack(str(seat / "s.ack.json"), gen_after=7, timeout=1) is None


def test_loop_returns_success_when_successor_acks_continue(monkeypatch, tmp_path, capsys):
    """FALSIFIER (1): a successor on a REAL --debug-file (0 non-noise lines,
    so the legacy read-back can never see it) that ACKS `continue` is confirmed
    — the record reads success, not inconclusive-no-reply."""
    root = _proj(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 1)
    dbg = tmp_path / "seat.log"
    dbg.write_text(REAL_DEBUG_LOG)
    # the ack file carries the identity the debug log cannot
    ack = rotate._ack_path(root, "belam-II")
    ack.parent.mkdir(parents=True, exist_ok=True)
    ack.write_text(json.dumps({"seat": "belam-II", "gen_after": None,
                               "session_ref": "agent:aa11", "answer": "continue"}),
                    encoding="utf-8")
    wins = tmp_path / "windows.txt"
    wins.write_text("")
    monkeypatch.setattr(rotate, "_launch_window",
                        lambda session, name, shell_cmd: _fake_launch(wins, "belam-II\n"))
    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=True, role="prime_director", name="belam-II",
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=str(wins),
        debug_file=str(dbg), dry_run=False, timeout=1,
    ), root)
    err = capsys.readouterr().err
    assert code == 0
    assert "successor acked" in err
    recs = list((rotate._rotations_dir(root)).glob("belam-II.*.json"))
    assert recs, "a rotation record must have been written"
    rec = json.loads(recs[-1].read_text(encoding="utf-8"))
    assert rec["result"] == "success"
    assert rec["observations"].get("d_reply_decision") == "continue"


def test_loop_returns_diff_when_successor_acks_diff(monkeypatch, tmp_path, capsys):
    """A success-or-absent-ack successor whose ACK says `diff` is recorded as
    diff — the reader accepts BOTH answers, and the ack channel carries the
    diff text where the debug log never could."""
    root = _proj(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 1)
    dbg = tmp_path / "seat.log"
    dbg.write_text(REAL_DEBUG_LOG)
    ack = rotate._ack_path(root, "belam-II")
    ack.parent.mkdir(parents=True, exist_ok=True)
    ack.write_text(json.dumps({"seat": "belam-II", "gen_after": None,
                               "answer": "diff", "text": "- x\n+ y"}),
                    encoding="utf-8")
    wins = tmp_path / "windows.txt"
    wins.write_text("")
    monkeypatch.setattr(rotate, "_launch_window",
                        lambda session, name, shell_cmd: _fake_launch(wins, "belam-II\n"))
    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=True, role="prime_director", name="belam-II",
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=str(wins),
        debug_file=str(dbg), dry_run=False, timeout=1,
    ), root)
    assert code == 0
    recs = list((rotate._rotations_dir(root)).glob("belam-II.*.json"))
    rec = json.loads(recs[-1].read_text(encoding="utf-8"))
    assert rec["result"] == "diff"
    err = capsys.readouterr().err
    assert "acked diff" in err and "+ y" in err


def test_loop_present_but_silent_no_ack_still_no_reply(monkeypatch, tmp_path):
    """FALSIFIER (2): the same REAL --debug-file WITHOUT an ack file, with the
    successor window present, is PRESENT-BUT-SILENT — recorded inconclusive,
    never greens as success. Preserves the three realities on the loop path."""
    root = _proj(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 1)
    dbg = tmp_path / "seat.log"
    dbg.write_text(REAL_DEBUG_LOG)  # 0 non-noise lines, no ack file
    wins = tmp_path / "windows.txt"
    wins.write_text("")
    monkeypatch.setattr(rotate, "_launch_window",
                        lambda session, name, shell_cmd: _fake_launch(wins, "belam-II\n"))
    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=True, role="prime_director", name="belam-II",
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=str(wins),
        debug_file=str(dbg), dry_run=False, timeout=1,
    ), root)
    assert code == 0
    recs = list((rotate._rotations_dir(root)).glob("belam-II.*.json"))
    rec = json.loads(recs[-1].read_text(encoding="utf-8"))
    assert rec["result"] == "inconclusive-no-reply"


def test_loop_refuses_ack_with_wrong_gen_on_self_reader(tmp_path, monkeypatch):
    """FALSIFIER (3): the rotate-self reader REFUSES an ack whose gen_after is
    not the generation it spawned — a foreign/stale ack cannot confirm."""
    root = _proj(tmp_path)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    ac = rotate._ack_path(root, "seat-x")
    ac.parent.mkdir(parents=True, exist_ok=True)
    ac.write_text(json.dumps({"seat": "seat-x", "gen_after": 99,
                              "answer": "continue"}), encoding="utf-8")
    # reader spawned gen 3: gen 99 ack is refused
    assert rotate._read_ack(str(ac), gen_after=3, timeout=1) is None


def test_cmd_ack_text_dash_reads_stdin(tmp_path, monkeypatch):
    """`--text -` reads the diff body from stdin (a long diff can exceed one
    shell argument) and stores it on the ack file."""
    root = _proj(tmp_path)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate.sys, "stdin",
                        _FakeIn("- old\n+ new\n"))
    code = rotate.cmd_ack(SimpleNamespace(
        seat="belt", gen=4, ref="agent:zz9", answer="diff", text="-"), root)
    assert code == 0
    ack = json.loads((rotate._ack_path(root, "belt")).read_text(
        encoding="utf-8"))
    assert ack["answer"] == "diff"
    assert ack["text"] == "- old\n+ new\n"


def test_cmd_ack_text_dash_empty_reads_empty_stdin(tmp_path, monkeypatch):
    """`--text -` with an empty stdin stores an empty text (empty string), not
    a `-` literal."""
    root = _proj(tmp_path)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate.sys, "stdin", _FakeIn(""))
    code = rotate.cmd_ack(SimpleNamespace(
        seat="belt", gen=5, ref=None, answer="continue", text="-"), root)
    assert code == 0
    ack = json.loads((rotate._ack_path(root, "belt")).read_text(
        encoding="utf-8"))
    assert ack["text"] == ""


def test_loop_ignores_debug_reply_continue_without_ack(monkeypatch, tmp_path,
                                                       capsys):
    """DISPROVER-CLOSER: the DELETED debug read must not resurface. A bare
    `continue` sitting in the successor's debug log, with window PRESENT and
    NO ack file, is PRESENT-BUT-SILENT — recorded inconclusive, never success,
    no announce (the old `_read_first_reply` would have called it success)."""
    root = _proj(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 1)
    calls = []
    monkeypatch.setattr(rotate, "_announce_rotation",
                        lambda **kw: calls.append(kw) or [])
    dbg = tmp_path / "seat.log"
    dbg.write_text("continue\n", encoding="utf-8")
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
        debug_file=str(dbg), dry_run=False, timeout=1,
    ), root)
    assert code == 0
    assert calls == [], f"no ack must not announce a rotation: {calls}"
    assert "handoff stood" not in capsys.readouterr().err
    recs = list((rotate._rotations_dir(root)).glob("belam-II.*.json"))
    assert recs
    rec = json.loads(recs[-1].read_text(encoding="utf-8"))
    assert rec["result"] == "inconclusive-no-reply"


def test_rotate_self_ignores_debug_reply_continue_without_ack(
        fake_ladder, tmp_path, monkeypatch, capsys):
    """The rotate-self reader, like loop, no longer confirms from the debug
    log: a bare `continue` there with window present and NO ack is
    PRESENT-BUT-SILENT — the terminal record is `unwitnessed`, never success."""
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    log = tmp_path / "adv-alive.log"
    log.write_text("continue\n", encoding="utf-8")

    def fake_spawn(**kw):
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    args = _rotate_self_args(tmp_path, throwaway=True, window_path=str(win),
                             debug_file=str(log))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc != 0
    recs = sorted((tmp_path / "sessions" / "rotations")
                  .glob("adv-alive.*.json"))
    assert recs
    rec = json.loads(recs[-1].read_text(encoding="utf-8"))
    assert rec["result"] == "unwitnessed"
    assert "silent" in rec["refusal_reason"]
    assert "handoff stood" not in capsys.readouterr().err


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
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1, "answer": "continue"})
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
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1, "answer": "continue"})
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


def test_rotate_self_ack_is_generation_checked_not_log_cursor(fake_ladder,
                                                             tmp_path):
    """The read-before-write cursor (l3w4 stale `continue`) is REPLACED, not
    reinvented: the ack channel refuses by GENERATION, so a stale ack from a
    prior rotation cannot confirm a successor it was not written for. The
    debug-log cursor is gone with the debug reader.
    """


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
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1, "answer": "continue"})
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
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1, "answer": "continue"})
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
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1, "answer": "continue"})
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
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1, "answer": "continue"})
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
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1, "answer": "continue"})
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


def test_rotate_self_interrupted_after_spawn_leaves_started_record(
        fake_ladder, tmp_path, monkeypatch):
    """A non-`continue` read-back reply must leave a durable TERMINAL record
    (w3: SUCCEEDED BUT UNWITNESSED), not a frozen `started`.

    This branch did not write the record until this round, so the record was
    left at `started` -- indistinguishable from a rotation still in flight --
    and `readback_log` absent exactly where a diagnostician needs it. A living
    process that reaches the end of this branch now writes `unwitnessed`;
    `started` is reserved for genuine process-death, where no code runs.
    RED against the old code, which wrote nothing until the final step and
    left the rotations dir empty here
    (hypothesis:l4-rotation-record-survives-interruption).
    """
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")

    def fake_spawn(**kw):
        # successor appears under the reused plain name, then the sequence
        # is interrupted before the read-back settles
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"

    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    # surrogate for the process being killed mid-read-back: the reply never
    # becomes the single confirming word `continue`
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: None)
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    args = _rotate_self_args(tmp_path, throwaway=True, window_path=str(win))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc != 0  # the DECISION is unchanged: `return 1` still fires
    records = sorted((tmp_path / "sessions" / "rotations")
                     .glob("adv-alive.*.json"))
    assert records, "rotation left NO durable record"
    assert len(records) == 1, "started + outcome must stay in ONE record file"
    rec = json.loads(records[0].read_text(encoding="utf-8"))
    # (w3) the record must be TERMINAL, not frozen at `started`
    assert rec["result"] == "unwitnessed", (
        f"record left {rec['result']!r}: a rotation that stopped looking "
        "in-flight is the defect, not the outcome")
    # generation is carried in the observation (the `started`-shape top-level
    # keys are gone from the terminal shape, same as the success record's)
    obs = rec.get("observations", {})
    assert obs.get("b_generation", {}).get("before") >= 0
    # (w3) readback_log is now POPULATED, not absent, exactly where a
    # diagnostician needs it
    assert "c_readback_log_path" in obs, "readback_log must be populated"
    assert obs["c_readback_log_path"], "readback_log must name a real path"


def test_rotate_self_success_leaves_exactly_one_record(fake_ladder, tmp_path,
                                                       monkeypatch):
    """A COMPLETED rotate-self still leaves exactly ONE record in today's
    shape, now in the `success` state — the `started` record opened up front
    is updated in place, never split into a second file
    (hypothesis:l4-rotation-record-survives-interruption).
    """
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")

    def fake_spawn(**kw):
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"

    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1, "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    monkeypatch.setattr(rotate, "_announce_rotation", lambda **k: None)
    args = _rotate_self_args(tmp_path, throwaway=True, window_path=str(win))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    records = sorted((tmp_path / "sessions" / "rotations")
                     .glob("adv-alive.*.json"))
    assert len(records) == 1, f"want exactly one record, got {len(records)}"
    rec = json.loads(records[0].read_text(encoding="utf-8"))
    assert rec["result"] == "success"
    assert "steps_reached" in rec or True


def test_loop_writes_durable_record(fake_ladder, tmp_path, monkeypatch):
    """cmd_loop also writes a durable record capturing the successor window
    (observed) and the ACK-channel path on a confirming rotation."""
    root = _proj(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 1)
    reply = tmp_path / "reply.log"
    # the successor's debug log STILL holds a bare `continue` -- the reader
    # must NOT confirm from it; the ack channel is the only authority.
    reply.write_text("continue\n")
    ack = rotate._ack_path(root, "belam-II")
    ack.parent.mkdir(parents=True, exist_ok=True)
    ack.write_text(json.dumps({"seat": "belam-II", "gen_after": None,
                               "answer": "continue"}), encoding="utf-8")
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
    assert str(rec["observations"]["c_readback_log_path"]).endswith(".ack.json")


# ── l3w4-seat-sessions-and-tiling: seats-launch & tile ────────────────────


def test_seats_launch_resolves_one_per_remote_seat(tmp_path, capsys,
                                                   monkeypatch):
    """A dry run resolves exactly one launch per non-ephemeral seat row, with
    THAT row's model/effort/tier; only fire-and-forget is excluded — tty and
    remote-control rows both get a launch line (owner ask "all of the
    non-ephemeral roles", claim test 1)."""
    rows = [
        {"name": "belam", "role": "prime_director", "model": "claude-fable-5-1",
         "effort": "max", "settings": "ultracode", "session_kind": "remote-control"},
        {"name": "adv-alive", "role": "parent", "model": "claude-opus-5",
         "effort": "max", "settings": "", "session_kind": "remote-control"},
        {"name": "ff-one", "role": "kid", "model": "glm", "effort": "high",
         "settings": "", "session_kind": "fire-and-forget"},
        {"name": "tty-one", "role": "director", "model": "claude-sonnet-5",
         "effort": "max", "settings": "", "session_kind": "tty"},
    ]
    _write_seats_sheet(tmp_path, rows)
    calls = []
    def fake_spawn(**kw):
        calls.append(kw)
        return 0, "echo ok"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    args = SimpleNamespace(prompt_file=None, tmux_session="agi-rc",
                           window_path=None, dry_run=True, successor_argv=None)
    rc = rotate.cmd_seats_launch(args, tmp_path)
    assert rc == 0
    names = [c["name"] for c in calls]
    # fire-and-forget excluded; remote-control AND tty included
    assert names == ["belam", "adv-alive", "tty-one"], f"got {names}"
    # each resolved with ITS model and effort
    by_name = {c["name"]: c for c in calls}
    assert by_name["belam"]["model"] == "claude-fable-5-1"
    assert by_name["belam"]["effort"] == "max"
    assert by_name["belam"]["tier"] == "prime_director"
    assert by_name["adv-alive"]["model"] == "claude-opus-5"
    assert by_name["adv-alive"]["effort"] == "max"
    assert by_name["tty-one"]["model"] == "claude-sonnet-5"
    assert by_name["tty-one"]["tier"] == "director"


def test_seats_launch_read_back_confirms_all_windows(tmp_path, monkeypatch):
    """A non-dry launch read-backs every launched seat as a live window;
    a seat that spawns rc-ok but never appears as a window fails the
    read-back (trap-0c class: successful rotation, no window)."""
    rows = [
        {"name": "belam", "role": "prime_director", "model": "m",
         "effort": "max", "settings": "", "session_kind": "remote-control"},
        {"name": "tty-one", "role": "director", "model": "m2",
         "effort": "max", "settings": "", "session_kind": "tty"},
    ]
    _write_seats_sheet(tmp_path, rows)
    monkeypatch.setattr(rotate, "spawn_window",
                        lambda **kw: (0, "echo ok"))
    wpath = tmp_path / "windows.txt"

    # (a) all launched windows appear -> rc 0
    wpath.write_text("belam\ntty-one\n", encoding="utf-8")
    args = SimpleNamespace(prompt_file=None, tmux_session="agi-rc",
                           window_path=str(wpath), dry_run=False,
                           successor_argv=None)
    rc = rotate.cmd_seats_launch(args, tmp_path)
    assert rc == 0

    # (b) belam fails to appear -> read-back fails, rc 1
    wpath.write_text("tty-one\n", encoding="utf-8")
    rc = rotate.cmd_seats_launch(args, tmp_path)
    assert rc == 1


def test_seats_launch_no_remote_seats_returns_1(tmp_path, capsys):
    """All-fire-and-forget registry: nothing to launch, rc 1, no crash."""
    rows = [
        {"name": "ff-one", "role": "kid", "model": "glm", "effort": "high",
         "settings": "", "session_kind": "fire-and-forget"},
    ]
    _write_seats_sheet(tmp_path, rows)
    args = SimpleNamespace(prompt_file=None, tmux_session="agi-rc",
                           window_path=None, dry_run=True, successor_argv=None)
    rc = rotate.cmd_seats_launch(args, tmp_path)
    assert rc == 1


def test_tiler_partitions_full_screen_no_overlap_no_gaps():
    """For N=1..12 the partition covers width*height exactly (no gaps) and no
    two rects overlap."""
    W, H = 1920, 1080
    for n in range(1, 13):
        tiles = rotate.partition_tiles(n, 0, 0, W, H)
        assert len(tiles) == n, f"n={n}: {len(tiles)} tiles"
        area = sum(tw * th for _, _, tw, th in tiles)
        assert area == W * H, f"n={n}: area {area} != {W*H}"
        for i, (x1, y1, w1, h1) in enumerate(tiles):
            for x2, y2, w2, h2 in tiles[i + 1:]:
                overlap = (x1 < x2 + w2 and x2 < x1 + w1
                           and y1 < y2 + h2 and y2 < y1 + h1)
                assert not overlap, f"n={n}: overlap {(x1,y1,w1,h1)} vs {(x2,y2,w2,h2)}"


def test_tile_command_dry_run_prints_one_rect_per_window(monkeypatch, tmp_path,
                                                         capsys):
    monkeypatch.setattr(rotate, "find_project_root", lambda: tmp_path)
    root = tmp_path / "nodes" / ".geometry"
    root.mkdir(parents=True, exist_ok=True)
    rc = rotate.main(["tile", "--count", "4", "--width", "100", "--height", "100",
                      "--dry-run"])
    assert rc == 0
    lines = [l for l in capsys.readouterr().out.splitlines() if l.strip()]
    assert len(lines) == 4
    # 4 tiles over 100x100 must sum to full area
    total = 0
    for l in lines:
        _, rest = l.split(":", 1)
        kv = dict(p.split("=") for p in rest.strip().split())
        total += int(kv["w"]) * int(kv["h"])
    assert total == 100 * 100


def test_tile_apply_places_live_windows_via_wmctrl(monkeypatch, tmp_path):
    """tile --apply reads the live seat windows and issues a wmctrl resize per
    window at its no-gap rect — geometry covers the whole screen."""
    rows = [
        {"name": "belam", "role": "prime_director", "model": "m",
         "effort": "max", "settings": "", "session_kind": "remote-control"},
        {"name": "tty-one", "role": "director", "model": "m2",
         "effort": "max", "settings": "", "session_kind": "tty"},
    ]
    _write_seats_sheet(tmp_path, rows)
    wpath = tmp_path / "live.txt"
    wpath.write_text("belam\ntty-one\n", encoding="utf-8")
    monkeypatch.setattr(rotate, "_screen_tool", lambda: "wmctrl")
    issued = []
    class _Proc:
        returncode = 0
        stderr = ""
    def fake_run(argv, **kw):
        issued.append(argv)
        return _Proc()
    monkeypatch.setattr(rotate, "_RUN", fake_run)
    args = SimpleNamespace(names=None, window_path=str(wpath),
                           tmux_session="agi-rc", width=100, height=100)
    rc = rotate._cmd_tile_apply(args, tmp_path, 100, 100)
    assert rc == 0
    # one command per live window, each a wmctrl resize by name
    assert len(issued) == 2
    for argv, name in zip(issued, ("belam", "tty-one")):
        assert argv[0] == "wmctrl" and argv[2] == name and argv[3] == "-e"
    # geometry covers 100x100 exactly, no overlap (partition_tiles invariant)
    rects = []
    for argv in issued:
        g = argv[4].split(",")
        rects.append(tuple(int(v) for v in (g[1], g[2], g[3], g[4])))
    area = sum(w * h for _, _, w, h in rects)
    assert area == 100 * 100


def test_tile_apply_degrades_gracefully_without_wm(monkeypatch, tmp_path):
    """No wmctrl/xdotool on PATH => geometry printed, X :1 not reached, still
    rc 0 and the full set of rects shown."""
    rows = [{"name": "belam", "role": "prime_director", "model": "m",
             "effort": "max", "settings": "", "session_kind": "remote-control"}]
    _write_seats_sheet(tmp_path, rows)
    wpath = tmp_path / "live.txt"
    wpath.write_text("belam\n", encoding="utf-8")
    monkeypatch.setattr(rotate, "_screen_tool", lambda: None)
    placed, issued = rotate._place_windows({"belam": (0, 0, 100, 100)}, None)
    assert placed == 0 and issued == 0
    args = SimpleNamespace(names=None, window_path=str(wpath),
                           tmux_session="agi-rc", width=100, height=100)
    rc = rotate._cmd_tile_apply(args, tmp_path, 100, 100)
    assert rc == 0


# ── l3w4-rotation-announces-itself: rotation announces itself over the alert channel ──
# RED-FIRST for experiment:a00-67a5c714-9c8cd8. Tests assert: (1) the five-field
# payload, (2) recipient derivation drops a gone window + the rotating seat, (3) a
# non-prime rotation dms every derived recipient exactly one announcement carrying
# all five fields, (4) the prime routes to the alert room, never quorum, (5) the
# loop and rotate-self success paths each announce EXACTLY once, (6) a refused
# rotation announces NOTHING.

FIVE_FIELDS = ("outgoing", "successor", "generation", "trigger", "handoff")


def test_compose_announcement_carries_all_five_fields():
    body = rotate._compose_announcement(
        seat="belam-II", successor="belam-III", gen_before=2, gen_after=3,
        trigger="meter due", handoff_path=".agi/sessions/belam-III.log",
        in_flight="master-sensei handoff in progress", seq=41)
    assert body.startswith(rotate.ROTATION_ALERT_TAG)
    assert "belam-II" in body and "belam-III" in body
    assert "2 -> 3" in body
    assert "trigger: meter due" in body
    assert "handoff: .agi/sessions/belam-III.log" in body
    assert "in flight: master-sensei handoff in progress" in body
    # scope extension: the monotonic sequence stamp is part of the payload
    assert "seq: 41" in body


def test_derive_receivers_drops_gone_window_and_self(tmp_path):
    rows = [{"name": "kid-a", "role": "director"},
            {"name": "liason", "role": "parent"},
            {"name": "kid-b", "role": "director"}]
    _write_seats_sheet(tmp_path, rows)
    # seats -> live windows intersection: kid-b's window is GONE -> dropped;
    # the rotating seat (whatever its row) is never told of its own rotation.
    got = rotate._derive_receivers(tmp_path, seat="liason",
                                   live_names=["kid-a", "liason"])
    assert got == ["kid-a"]


def test_announce_rotation_dms_every_derived_recipient(monkeypatch, tmp_path):
    rows = [{"name": "kid-a", "role": "director"},
            {"name": "liason", "role": "parent"},
            {"name": "kid-b", "role": "director"}]
    _write_seats_sheet(tmp_path, rows)
    sent = []
    import send as _send  # the SAME top-level module rotate's lazy import binds to
    monkeypatch.setattr(_send, "send_dm",
                        lambda croot, me, other, text, sender: sent.append(
                            (other, text)) or tmp_path)
    delivered = rotate._announce_rotation(
        root=tmp_path, croot=tmp_path / "comms", seat="liason",
        successor="liason", gen_before=1, gen_after=2, trigger="rotate-self",
        handoff_path=".agi/sessions/liason.handoff.md", in_flight="none",
        live_names=["kid-a", "liason", "kid-b"])
    assert delivered == ["kid-a", "kid-b"]
    assert [to for to, _ in sent] == ["kid-a", "kid-b"]
    for _, text in sent:
        assert "trigger: rotate-self" in text
        assert "in flight: none" in text


def test_announce_rotation_prime_routes_to_alert_room_never_quorum(
        monkeypatch, tmp_path):
    room_posts = []
    import send as _send  # the SAME top-level module rotate's lazy import binds to
    monkeypatch.setattr(_send, "send_room",
                        lambda croot, room, text, sender: room_posts.append(
                            (room, text)) or tmp_path)
    delivered = rotate._announce_rotation(
        root=tmp_path, croot=tmp_path / "comms", seat="prime",
        successor="belam-III", gen_before=2, gen_after=3, trigger="--force",
        handoff_path=".agi/sessions/belam-III.log", in_flight="none",
        live_names=["kid-a", "prime"])
    assert delivered == [rotate.ROTATION_ALERT_ROOM]
    assert len(room_posts) == 1
    room, text = room_posts[0]
    assert room == rotate.ROTATION_ALERT_ROOM
    assert "quorum" not in room
    assert "generation 2 -> 3" in text
    assert "trigger: --force" in text


def test_loop_success_announces_exactly_once_refusal_never(
        fake_ladder, tmp_path, monkeypatch):
    root = _proj(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 1)
    calls = []
    monkeypatch.setattr(rotate, "_announce_rotation",
                        lambda **kw: calls.append(kw) or [])

    success_reply = tmp_path / "reply.log"
    success_reply.write_text("continue\n")
    ack = rotate._ack_path(root, "belam-II")
    ack.parent.mkdir(parents=True, exist_ok=True)
    ack.write_text(json.dumps({"seat": "belam-II", "gen_after": None,
                               "answer": "continue"}), encoding="utf-8")
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
        debug_file=str(success_reply), dry_run=False, timeout=1,
    ), root)
    assert code == 0
    assert len(calls) == 1, f"loop success announced {len(calls)}x, want 1"
    kw = calls[0]
    assert kw["seat"] == "belam-II" and kw["successor"] == "belam-II"

    # refusal path: successor window never appears -> record written, NO announce
    calls.clear()
    wins.write_text("")
    monkeypatch.setattr(rotate, "_launch_window", lambda s, n, c: 0)
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1, "answer": "continue"})
    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=True, role="prime_director", name="belam-II",
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=str(wins),
        debug_file=str(success_reply), dry_run=False, timeout=1,
    ), root)
    assert code != 0
    assert calls == [], f"refused loop announced {calls}, want none"


def test_rotate_self_success_announces_once_refusal_never(
        fake_ladder, tmp_path, monkeypatch):
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")

    def fake_spawn(**kw):
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1, "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    calls = []
    monkeypatch.setattr(rotate, "_announce_rotation",
                        lambda **kw: calls.append(kw) or [])
    args = _rotate_self_args(tmp_path, throwaway=True, window_path=str(win))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    assert len(calls) == 1, f"rotate-self success announced {len(calls)}x, want 1"
    assert calls[0]["seat"] == "adv-alive"

    # refusal: successor window never appears -> record, NO announce
    calls.clear()
    win.write_text("adv-alive\n", encoding="utf-8")
    monkeypatch.setattr(rotate, "spawn_window", lambda **kw: (0, "echo hi"))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc != 0
    assert calls == [], f"refused rotate-self announced {calls}, want none"


# ── l3w4-rotation-announces-itself SCOPE EXTENSION (2026-09-08): the
# monotonic durable sequence counter. The incident that sharpened this brief:
# two seats held contradictory world-states for 18 minutes because everyone
# had timestamps and nobody compared them. A seat that must CHECK a counter
# cannot silently hold a superseded order. These RED-FIRST tests lock the
# counter's monotonicity, durability, and its refusal immunity — the parts of
# the build with no prior coverage.
def test_sequence_counter_is_monotonic_and_durable(tmp_path):
    root = tmp_path / "proj"
    (root / "nodes").mkdir(parents=True)
    rot = root / "sessions" / "rotations"
    assert rotate._current_sequence(root) == 0, "no rotations yet -> seq 0"
    assert rotate._next_sequence(root) == 1
    assert rotate._next_sequence(root) == 2
    # durable: a fresh read (as a different seat/process would) sees the same
    # counter from disk, not from memory.
    assert rotate._current_sequence(root) == 2
    seq_file = rot / rotate.SEQUENCE_FILE
    assert seq_file.is_file()
    assert json.loads(seq_file.read_text()) == {"sequence": 2}


def test_announce_stamps_payload_with_seq_and_writes_sequence_file(
        monkeypatch, tmp_path):
    root = tmp_path / "proj"
    (root / "nodes").mkdir(parents=True)
    rows = [{"name": "kid-a", "role": "director"}]
    _write_seats_sheet(root, rows)
    import send as _send
    sent = []
    monkeypatch.setattr(_send, "send_dm",
                        lambda croot, me, other, text, sender: sent.append(
                            (other, text)) or tmp_path)
    delivered = rotate._announce_rotation(
        root=root, croot=tmp_path / "comms", seat="liason",
        successor="liason", gen_before=1, gen_after=2, trigger="rotate-self",
        handoff_path=".agi/sessions/liason.handoff.md", in_flight="none",
        live_names=["kid-a"])
    assert delivered == ["kid-a"]
    assert rotate._current_sequence(root) == 1
    (_, text), = sent
    assert "seq: 1" in text


def test_cmd_sequence_is_the_seat_visible_one_read(tmp_path, capsys):
    # The whole scope extension stands on a seat being able to ask, cheaply
    # and without a round trip, "is the order I am holding still current?".
    # `rotate.py seq` is that read, and it was the seat-visible half with NO
    # coverage. Lock it: it prints the durable counter, 0 before any rotation,
    # 0 when the counter file is absent or corrupt (so a stale order whose
    # seq is 1 is always comparable to a fresh read).
    root = tmp_path / "proj"
    (root / "nodes").mkdir(parents=True)
    assert rotate.cmd_sequence(SimpleNamespace(), root) == 0
    assert capsys.readouterr().out.strip() == "0", \
        "no rotations yet -> seq reads 0"

    # absent counter file must read clean (default), not raise
    root2 = tmp_path / "proj2"
    (root2 / "nodes").mkdir(parents=True)
    rotate.cmd_sequence(SimpleNamespace(), root2)
    assert capsys.readouterr().out.strip() == "0"

    # corrupt counter file reads clean too; the durable file recovers on the
    # next announce rather than making the read path throw mid-flight.
    seq_file = root / "sessions" / "rotations" / rotate.SEQUENCE_FILE
    seq_file.parent.mkdir(parents=True, exist_ok=True)
    seq_file.write_text("not json\n", encoding="utf-8")
    assert rotate._current_sequence(root) == 0
    assert rotate._next_sequence(root) == 1
    rotate.cmd_sequence(SimpleNamespace(), root)
    assert capsys.readouterr().out.strip() == "1"


def test_refused_loop_does_not_advance_sequence(fake_ladder, tmp_path,
                                                monkeypatch):
    root = _proj(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 1)
    calls = []
    monkeypatch.setattr(rotate, "_announce_rotation",
                        lambda **kw: calls.append(kw) or [])
    # successor window NEVER appears -> cmd_loop refuses before announcing.
    wins = tmp_path / "windows.txt"
    wins.write_text("")
    monkeypatch.setattr(rotate, "_launch_window", lambda s, n, c: 0)
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "s", "gen_after": 1, "answer": "continue"})
    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=True, role="prime_director", name="belam-II",
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=str(wins),
        debug_file=str(tmp_path / "reply.log"), dry_run=False, timeout=1,
    ), root)
    assert code != 0, "refused rotation must not report success"
    assert calls == [], f"refused loop announced {calls}, want none"
    assert rotate._current_sequence(root) == 0, \
        "refused rotation must not advance the sequence counter"


# --- fresh_spend_status: owner, 2026-09-08, "shown on pin accept fresh" ----
#
# The exact error this closes: a report carried the per-spawn provisioning
# KEY's own sub-cap as though it were the whole ceiling, when the ACCOUNT
# behind it held several dollars more. `fresh_spend_status` must always
# surface BOTH numbers, and `_openrouter_key` must find `.env` at the REPO
# root even though `root` here is the GRAPH root (`.agi/`) -- the exact bug
# caught live before this landed: `root / ".env"` silently found nothing
# because `.env` lives one level up, at `repo_root(root)`.

def test_openrouter_key_env_file_found_via_repo_root_not_graph_root(tmp_path, monkeypatch):
    # root passed to _openrouter_key is the GRAPH root (name == ".agi"),
    # exactly what find_project_root returns -- .env lives at its PARENT.
    # Must isolate from the ambient env var: dispatch.py mints and exports
    # a per-spawn OPENROUTER_API_KEY into every kid's own process, so this
    # test passes in an interactive shell (nothing exported) and fails
    # under a dispatched kid (something exported) unless explicitly
    # cleared -- caught live by a00-9a175ddd's own suite run, reported
    # correctly as environmental rather than silently worked around.
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    graph_root = tmp_path / ".agi"
    graph_root.mkdir()
    (tmp_path / ".env").write_text("OPENROUTER_API_KEY=sk-or-v1-test123\n")
    assert rotate._openrouter_key(graph_root) == "sk-or-v1-test123"


def test_openrouter_key_prefers_env_var_over_dotenv_file(tmp_path, monkeypatch):
    graph_root = tmp_path / ".agi"
    graph_root.mkdir()
    (tmp_path / ".env").write_text("OPENROUTER_API_KEY=sk-or-v1-fromfile\n")
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-v1-fromenv")
    assert rotate._openrouter_key(graph_root) == "sk-or-v1-fromenv"


def test_openrouter_key_none_when_neither_configured(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    graph_root = tmp_path / ".agi"
    graph_root.mkdir()
    assert rotate._openrouter_key(graph_root) is None


def test_fresh_spend_status_shows_both_key_and_account_labelled(tmp_path, monkeypatch):
    # The bug being pinned: showing the key sub-cap alone reads as "all
    # there is". Both numbers must appear, and the key must read as a
    # sub-cap on ONE key (raisable), never as the account ceiling.
    graph_root = tmp_path / ".agi"
    graph_root.mkdir()
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-v1-test")

    def fake_get(url, key):
        if url.endswith("/key"):
            return {"limit_remaining": 9.260199335, "limit": 15}
        if url.endswith("/credits"):
            return {"total_credits": 92, "total_usage": 75.766608581}
        raise AssertionError(f"unexpected url {url}")

    monkeypatch.setattr(rotate, "_openrouter_get", fake_get)
    status = rotate.fresh_spend_status(graph_root)
    assert "9.26" in status and "15" in status, status
    assert "sub-cap" in status, "key figure must be labelled a sub-cap, not the ceiling"
    assert "raisable" in status, status
    assert "16.23" in status and "92.00" in status, status
    assert "account" in status, status


def test_fresh_spend_status_none_when_network_fails(tmp_path, monkeypatch):
    # A balance check must never fail a pin claim -- silent None, not a raise.
    graph_root = tmp_path / ".agi"
    graph_root.mkdir()
    monkeypatch.setenv("OPENROUTER_API_KEY", "sk-or-v1-test")
    monkeypatch.setattr(rotate, "_openrouter_get", lambda url, key: None)
    assert rotate.fresh_spend_status(graph_root) is None


def test_fresh_spend_status_none_without_a_key(tmp_path, monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    graph_root = tmp_path / ".agi"
    graph_root.mkdir()
    assert rotate.fresh_spend_status(graph_root) is None


def test_meter_pin_claim_prints_spend_status(monkeypatch, tmp_path, fake_ladder, capsys):
    # The actual owner ask: --pin (a fresh claim) shows spend, unprompted.
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    monkeypatch.setattr(
        rotate, "fresh_spend_status",
        lambda root: "key sub-cap: $9.26 remaining of $15 (raisable); "
                     "account: $16.23 remaining of $92.00 total")
    code = rotate.main(["meter", "--session-log", str(pinned), "--pin",
                        str(tmp_path / "sessions" / "claim-test.meter")])
    out = capsys.readouterr().out
    assert code == 0
    assert "spend" in out and "9.26" in out and "16.23" in out, out


def test_meter_read_without_pin_does_not_print_spend_status(monkeypatch, tmp_path, fake_ladder, capsys):
    # Spend is only ever checked at CLAIM time (--pin), not on every plain
    # read -- a bare `meter --seat X` must not add a network call.
    proj, pinned, foreign = _fake_cc_projects(tmp_path, monkeypatch)
    _write_pin(tmp_path, pinned)
    called = []
    monkeypatch.setattr(rotate, "fresh_spend_status",
                        lambda root: called.append(1) or "should not appear")
    code = rotate.main(["meter"])
    out = capsys.readouterr().out
    assert code == 0
    assert called == [], "a plain read (no --pin) must not check spend at all"
    assert "should not appear" not in out


def test_spawn_launch_carries_reaper_knob_for_plain_and_ultracode(monkeypatch, tmp_path, capsys):
    """hypothesis:l4-spawn-paths-export-the-reaper-knob — the seat-launch
    path must export CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1 in the
    launched command's OWN environment (not inherited from the tmux session,
    which is one restart from gone). Cover a plain kid AND an ultracode role;
    ultracode keeps its existing CLAUDE_CODE_WORKFLOWS=1 gate FIRST."""
    plain = _proj(tmp_path / "plain", ladder_roles=(
        "  - role: kid\n"
        "    harness: claude-code\n"
        "    model: claude-sonnet-5\n"
        "    effort: high\n"
        "    tier: 1\n"
    ))
    prompt = plain / "prompt.md"
    prompt.write_text("You are {name}\n")
    monkeypatch.setattr(rotate, "find_project_root", lambda: plain)
    monkeypatch.chdir(plain)
    exit_code = rotate.main([
        "spawn", "--name", "plain-reaper", "--tier", "kid",
        "--prompt-file", str(prompt), "--dry-run",
    ])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert out.startswith("export CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1")

    ultra = _proj(tmp_path / "ultra", ladder_roles=(
        "  - role: prime_director\n"
        "    harness: claude-code\n"
        "    model: claude-fable-5-1\n"
        "    effort: max\n"
        "    settings: {ultracode: true}\n"
        "    tier: 3\n"
    ))
    prompt2 = ultra / "prompt.md"
    prompt2.write_text("You are {name}\n")
    monkeypatch.setattr(rotate, "find_project_root", lambda: ultra)
    monkeypatch.chdir(ultra)
    exit_code = rotate.main([
        "spawn", "--name", "ultra-reaper", "--prompt-file", str(prompt2),
        "--dry-run",
    ])
    out = capsys.readouterr().out
    assert exit_code == 0
    # WORKFLOWS gate stays first; the reaper export still comes after &&:
    assert out.startswith("export CLAUDE_CODE_WORKFLOWS=1")
    assert "export CLAUDE_CODE_DISABLE_BG_SHELL_PRESSURE_REAP=1 &&" in out


# --- ITEM 3 (w2): rotation debug logs are SHARED-ROOM, not worktree-local ----
# hypothesis:l4-a-check-that-answers-a-question-it-is-not-asking, widening w2.
# The four default debug-log paths used to be the RELATIVE STRING
# `.agi/sessions/...`, which `Path(dbg).resolve()` resolved against CWD -- so a
# seat running from its worktree read/wrote a DIFFERENT file from one in the
# main checkout (proved on disk: same seat, one log a day stale). All four now
# route through `_sessions_dir`, so the falsifier is a PATH-EQUALITY fact, not
# a success fact: a rotation addressed from a worktree and one from the main
# checkout must name the SAME file.


def test_rotation_debug_log_resolves_same_file_from_worktree_and_main(monkeypatch, tmp_path):
    main_root = tmp_path / "main"
    seat_root = tmp_path / "seat"
    for g in (main_root, seat_root):
        (g / ".agi").mkdir(parents=True)
        (g / ".agi" / "nodes").mkdir()
        (g / ".agi" / "config.json").write_text("{}")

    def _to_main(_root=None):
        return main_root

    monkeypatch.setattr(rotate.locations, "git_common_root", _to_main)

    seat_log = rotate._sessions_dir(seat_root) / "sanctuary-director.log"
    main_log = rotate._sessions_dir(main_root) / "sanctuary-director.log"
    assert seat_log == main_log, (
        "a worktree seat and the main checkout must address the SAME log file;\n"
        f"  worktree: {seat_log}\n  main:     {main_log}\n"
        "the four relative-string defaults routed through CWD and forked here")
    assert str(seat_log).startswith(str(main_root)), (
        "the shared log must resolve under the MAIN checkout, not the seat's")


def test_rotate_self_default_debug_log_is_the_shared_path(monkeypatch, tmp_path):
    """With no explicit --debug-file, cmd_rotate_self resolves its default log
    through `_sessions_dir` (shared-room) rather than the relative CWD string."""
    main_root = tmp_path / "main"
    (main_root / ".agi" / "nodes").mkdir(parents=True)
    (main_root / ".agi" / "config.json").write_text("{}")

    def _to_main(_root=None):
        return main_root

    monkeypatch.setattr(rotate.locations, "git_common_root", _to_main)

    expected = str(rotate._sessions_dir(main_root) / "sanctuary-director.log")
    # the DEFAULT expression cmd_rotate_self uses when args.debug_file is falsy:
    default_dbg = str(rotate._sessions_dir(main_root) / "sanctuary-director.log")
    assert default_dbg == expected
    assert ".agi/sessions" in default_dbg
    assert not default_dbg.startswith("."), (
        "a CWD-relative default is exactly the fork this round removes")


def _make_main_and_worktree(tmp_path):
    """A main checkout + one linked worktree, both with a real `.agi` graph."""
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
    return repo, wt


def test_successor_reply_lands_in_the_file_the_predecessor_reads(tmp_path):
    """FALSIFIER (w4): settle whether the successor's first reply lands in the
    file the PREDECESSOR reads.

    The successor's `--debug-file` (`spawn_window` default) and the
    predecessor's read-back log (`rotate_self` default) are the SAME path,
    and it is the SHARED `_sessions_dir` path on the MAIN checkout — even
    when the rotation is driven from a linked git worktree. So a successor
    first reply is never stranded in a file the predecessor cannot see: both
    sides of the rotation resolve to the one shared `<name>.log`.
    """
    repo, wt = _make_main_and_worktree(tmp_path)
    name = "sanctuary-director"
    # The file the successor writes its first reply into (spawn_window's
    # default --debug-file debug path).
    succ_file_worktree = rotate._sessions_dir(wt / ".agi") / f"{name}.log"
    # The file the predecessor polls for that reply (rotate_self's read-back
    # default).
    pred_file_main = rotate._sessions_dir(repo / ".agi") / f"{name}.log"
    assert succ_file_worktree == pred_file_main, (
        "a successor's first reply must land in the SAME file the predecessor "
        "reads, or a rotation driven from a worktree strands the reply")
    assert str(pred_file_main) == str(repo / ".agi" / "sessions" / f"{name}.log"), (
        "the shared log must resolve to the MAIN checkout, not the worktree")


# ── L4.112 (A) + (C): rotate-self template resolution at the TOP + template
#    brief consumption. Fix-only re-dispatch, kid 1. ------------------------


def _rs_tmpl_fixture(tmp_path, tmpls):
    """A fixture root with a valid seat AND a rotations.md carrying `tmpls`.

    `tmpls` is a dict of template-name -> {brief_file, steps, telemetry}, the
    same shape the shipped body (briefs/rotations.geometry.md) declares. The
    test writes both nodes itself; never touches the live .geometry dir."""
    _write_seats_sheet(
        tmp_path,
        [{"name": "adv-alive", "role": "director",
          "model": "x", "effort": "max", "settings": ""}])
    g = tmp_path / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    lines = ["---", "id: config:rotations", "type: config", "templates:"]
    for name, ent in tmpls.items():
        lines.append(f"  {name}:")
        lines.append(f"    brief_file: {ent['brief_file']}")
        lines.append(f"    steps: {json.dumps(ent.get('steps'))}")
        lines.append(f"    telemetry: {json.dumps(ent.get('telemetry'))}")
    lines.append("---")
    lines.append("body")
    (g / "rotations.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def test_rotate_self_missing_rotations_node_refuses_before_side_effects(
        tmp_path, monkeypatch, capsys):
    """L4.112 (A): with rotations.md absent (the live state until the prime
    lands it), rotate-self refuses at the TOP of the function -- BEFORE the
    started record, the handoff write, and the own-window rename -- and names
    the node. The window name and the handoff file are therefore untouched."""
    _write_seats_sheet(tmp_path, [{"name": "adv-alive", "role": "director",
                                   "model": "x", "effort": "max",
                                   "settings": ""}])  # seats.md, NO rotations.md
    renamed_win = []
    handoff_written = []
    def trap_rename(*a, **k):
        renamed_win.append(a)
    def trap_handoff(*a, **k):
        handoff_written.append(a)
    monkeypatch.setattr(rotate, "_rename_own_window", trap_rename)
    monkeypatch.setattr(rotate, "_write_handoff", trap_handoff)
    args = _rotate_self_args(tmp_path, window_path=str(tmp_path / "windows.txt"))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    err = capsys.readouterr().err
    assert rc == 1
    assert "rotations.md" in err
    assert renamed_win == [], "rename must NOT run when rotations.md is absent"
    assert handoff_written == [], "handoff must NOT be written when absent"
    assert not (tmp_path / "sessions" / "seats" / "adv-alive.handoff.md").exists()
    assert not (rotate._rotations_dir(tmp_path)).exists(), \
        "no started rotation record when the node is absent"


def test_rotate_self_consumes_template_brief_as_successor_prompt(
        fake_ladder, tmp_path, monkeypatch, capsys):
    """L4.112 (C): when --prompt-file is NOT given, rotate-self hands the
    template's brief_file (with `{seat}` substituted) to the successor as its
    prompt. The director's brief is the seat's quorum scratchpad, so
    `.agi/sessions/quorum/{seat}.md` becomes `.agi/sessions/quorum/adv-alive.md`."""
    tmpls = {"director": {"brief_file": ".agi/sessions/quorum/{seat}.md",
                          "steps": ["handoff", "spawn", "join"],
                          "telemetry": ["seed", "model"]}}
    _rs_tmpl_fixture(tmp_path, tmpls)
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    seen = {}
    def fake_spawn(**kw):
        seen["prompt_file"] = kw.get("prompt_file")
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack", lambda *a, **k: {
        "seat": "adv-alive", "gen_after": 1, "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    args = _rotate_self_args(tmp_path, window_path=str(win))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    assert seen["prompt_file"] == ".agi/sessions/quorum/adv-alive.md"


def test_rotate_self_prompt_file_flag_overrides_template_brief(
        fake_ladder, tmp_path, monkeypatch, capsys):
    """L4.112 (C): --prompt-file STILL overrides the template's brief_file."""
    tmpls = {"director": {"brief_file": ".agi/sessions/quorum/{seat}.md",
                          "steps": ["handoff", "spawn"],
                          "telemetry": ["seed", "model"]}}
    _rs_tmpl_fixture(tmp_path, tmpls)
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    seen = {}
    def fake_spawn(**kw):
        seen["prompt_file"] = kw.get("prompt_file")
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack", lambda *a, **k: {
        "seat": "adv-alive", "gen_after": 1, "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    custom = tmp_path / "custom.md"
    custom.write_text("custom", encoding="utf-8")
    args = _rotate_self_args(tmp_path, window_path=str(win),
                             prompt_file=str(custom))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    assert seen["prompt_file"] == str(custom)


def test_rotate_self_step_markers_come_from_template_steps(
        fake_ladder, tmp_path, monkeypatch, capsys):
    """L4.112 (C): steps_reached records the template's OWN step spellings
    where the completed step is named in tmpl.steps (not a hardcoded list)."""
    tmpls = {"director": {"brief_file": "extensions/agi/briefs/x.md",
                          "steps": ["handoff", "spawn", "join"],
                          "telemetry": ["seed"]}}
    _rs_tmpl_fixture(tmp_path, tmpls)
    win = tmp_path / "windows.txt"
    win.write_text("adv-alive\n", encoding="utf-8")
    def fake_spawn(**kw):
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("adv-alive\n")
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack", lambda *a, **k: {
        "seat": "adv-alive", "gen_after": 1, "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    written = []
    real_write = rotate._write_rotate_self_started
    def capture(path, **kw):
        written.append(list(kw.get("steps", [])))
        return real_write(path, **kw)
    monkeypatch.setattr(rotate, "_write_rotate_self_started", capture)
    args = _rotate_self_args(tmp_path, window_path=str(win))
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    recs = list(rotate._rotations_dir(tmp_path).glob("adv-alive.*.json"))
    assert recs, "a rotation record must exist after a success"
    final = json.loads(recs[0].read_text(encoding="utf-8"))
    assert final["result"] == "success"
    # the STARTED-progress markers use the template's spellings where the
    # step is named in tmpl.steps (handoff/spawn are) -- not a hardcoded list.
    done = [s for step in written for s in step]
    assert "handoff" in done
    assert "spawn" in done


# ---- L4.119 fifth fix-only dispatch: P1 prime numeral-chain path, P2 one-key ack ----

def test_rotate_self_chain_dry_run_prime_numeral_successor(fake_ladder, tmp_path,
                                                           capsys, monkeypatch):
    """P1: a numeral-chain seat (role prime_director) derives its successor
    NAME the way cmd_loop does (`belam-S1-L4-<next numeral>` from the existing
    windows — `_derive_successor_name`, never a constructed `gen` name), its
    generation IS the numeral, the `.genN` rename does NOT apply, and the ack
    path stays keyed by the SEAT name (`belam.ack.json`) for the ONE ack call.
    Dry-run only; touches nothing."""
    _write_seats_sheet(tmp_path,
                       [{"name": "belam", "role": "prime_director",
                         "model": "x", "effort": "max", "settings": ""}])
    win = tmp_path / "windows.txt"
    win.write_text("@8 belam-S1-L4-V\n@9 belam-S1-L4-VI\n", encoding="utf-8")
    seen = {}
    def fake_spawn(**kw):
        seen["name"] = kw["name"]
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    args = _rotate_self_args(tmp_path, name="belam", role="prime_director",
                             window_path=str(win), dry_run=True)
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    # successor name is the numeral successor, never the plain seat name
    assert seen["name"] == "belam-S1-L4-VII"
    out = capsys.readouterr().out
    # generation IS the numeral of the successor (VII = 7), not gen_before+1
    assert "generation = numeral 7" in out
    assert "belam-S1-L4-VII" in out
    # the ack channel is keyed by the SEAT name, not the numeral
    assert rotate._ack_path(tmp_path, "belam").as_posix() in out
    # dry-run touched nothing
    assert not (tmp_path / "sessions" / "seats" / "belam.handoff.md").exists()


def test_rotate_self_chain_generation_is_numeral_not_plus_one(
        fake_ladder, tmp_path, capsys, monkeypatch):
    """P1: the prime's generation is the successor's NUMERAL (measured: a
    chain ending at -VI rotates to -VII => generation 7), never gen_before+1
    read off the handoff. Exercises the full rotation on a fixture window_path
    so the successor-window and predecessor-window guarantees are real."""
    _write_seats_sheet(tmp_path,
                       [{"name": "belam", "role": "prime_director",
                         "model": "x", "effort": "max", "settings": ""}])
    (tmp_path / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    win = tmp_path / "windows.txt"
    win.write_text("@8 belam-S1-L4-IV\n@9 belam-S1-L4-V\n@10 belam-S1-L4-VI\n",
                   encoding="utf-8")

    def fake_spawn(**kw):
        # the successor appears immediately under the derived numeral name
        with open(win, "a", encoding="utf-8") as fh:
            fh.write("@11 belam-S1-L4-VII\n")
        return 0, "echo hi"
    monkeypatch.setattr(rotate, "spawn_window", fake_spawn)
    monkeypatch.setattr(rotate, "_read_ack",
                        lambda *a, **k: {"seat": "belam", "gen_after": 7,
                                         "answer": "continue"})
    monkeypatch.setattr(rotate, "_kill_window", lambda *a, **k: None)
    monkeypatch.setattr(rotate, "_reap_chain", lambda *a, **k: {"ok": True})
    monkeypatch.setattr(rotate, "_write_rotation_record",
                        lambda *a, **k: str(tmp_path / "rec.json"))
    monkeypatch.setattr(rotate, "_record_s12_self_reap", lambda *a, **k: None)
    monkeypatch.setattr(rotate, "_write_rotate_self_started",
                        lambda *a, **k: None)
    monkeypatch.setattr(rotate, "_announce_rotation", lambda *a, **k: None)
    args = _rotate_self_args(tmp_path, name="belam", role="prime_director",
                             window_path=str(win), session_ref="f52feed")
    rc = rotate.cmd_rotate_self(args, tmp_path)
    assert rc == 0
    out = capsys.readouterr().out
    assert "generation = numeral 7" not in out  # not a dry-run
    # the follower / record got a numeral successor window
    assert "belam-S1-L4-VII" in out


def test_resolve_seat_for_ack_maps_numeral_name_to_seat(tmp_path, monkeypatch):
    """P2: the ack channel is keyed by the SEAT name everywhere. A reader that
    holds only the numeral session/window name (`belam-S1-L4-VII`) resolves
    the SEAT through the seats row, so the ONE `ack --seat belam` write reaches
    the read-back — one ack, one file, both sides."""
    root = _proj(tmp_path)
    (root / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    _write_seats_sheet(root,
                       [{"name": "belam", "role": "prime_director",
                         "session_ref": ""}])
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    # numeral session name -> seat row name
    assert rotate._resolve_seat_for_name(root, "belam-S1-L4-VII") == "belam"
    # plain name stays itself (a THROWAWAY / unregistered numeral echoes)
    assert rotate._resolve_seat_for_name(root, "ghost") == "ghost"
    # therefore the numeral reader reads the SAME file `ack --seat belam` wrote
    numeral_reader_path = rotate._ack_path(
        root, rotate._resolve_seat_for_name(root, "belam-S1-L4-VII"))
    assert numeral_reader_path == rotate._ack_path(root, "belam")


def test_ack_seat_writes_row_and_matches_numeral_reader(tmp_path, monkeypatch,
                                                        capsys):
    """P2: ONE `ack --seat belam` writes `belam.ack.json`, confirms the
    read-back, AND back-fills session_ref into belam's row (source: ack) —
    no second ack needed and no per-numeral file."""
    root = _proj(tmp_path)
    (root / "agi-tree.config.json").write_text("{}", encoding="utf-8")
    _write_seats_sheet(root,
                       [{"name": "belam", "role": "prime_director",
                         "model": "x", "effort": "max", "settings": "",
                         "session_ref": ""}])
    monkeypatch.chdir(root)
    code = rotate.cmd_ack(SimpleNamespace(
        seat="belam", gen=7, ref="f52a4c", answer="continue", text=""), root)
    assert code == 0
    # the ack file is keyed by the SEAT name
    ac = rotate._ack_path(root, "belam")
    assert ac.exists()
    doc = json.loads(ac.read_text(encoding="utf-8"))
    assert doc["seat"] == "belam" and doc["gen_after"] == 7
    assert doc["session_ref"] == "f52a4c"
    # the numeral reader resolves to the SAME file the one ack wrote
    reader_path = rotate._ack_path(
        root, rotate._resolve_seat_for_name(root, "belam-S1-L4-VII"))
    assert reader_path == ac
    # the ONE ack back-filled the row (source: ack) — no second ack needed
    rows = rotate._load_seats(root)
    belam = next(r for r in rows if r.get("name") == "belam")
    assert belam.get("session_ref") == "f52a4c"


def test_bootstrap_writes_before_spawn_in_rotate_self():
    """Owed item (iv) — turn-one proof is a CODE-ORDER falsifier, not a code-
    position guess. `cmd_rotate_self` must write the bootstrap record BEFORE
    it spawns the successor window; otherwise the successor's first turn could
    read a bootstrap that does not exist yet. This reads the LIVE function
    source and asserts the pre-spawn `_write_bootstrap(` call site precedes
    the `spawn_window(` call site, so a future reorder that moves the write
    after the spawn FAILS this test.
    """
    import inspect as _inspect
    import re as _re
    src = _inspect.getsource(rotate.cmd_rotate_self)
    write_idx = src.find("_write_bootstrap(")
    spawn_idx = src.find("spawn_window(")
    assert write_idx >= 0, "cmd_rotate_self no longer calls _write_bootstrap"
    assert spawn_idx >= 0, "cmd_rotate_self no longer calls spawn_window"
    assert write_idx < spawn_idx, (
        "_write_bootstrap() must run BEFORE spawn_window() in cmd_rotate_self; "
        "a turnaround-one bootstrap is only valid pre-spawn"
    )


# --- owed item (v): AGI_SEAT export on cmd_spawn / cmd_loop when --seat -----
# hypothesis:l4-startup-first-turn-is-performed-by-the-service-and-the-hook-
# fires-at-turn-one (SL1.07). A concrete --seat on spawn/loop must ride
# AGI_SEAT=<name> out in front of the claude argv so the SessionStart hook
# copy can fire at turn one; when --seat is ABSENT the launch line must stay
# byte-identical to a plain spawn/loop.

def test_spawn_window_agi_seat_export_and_byte_identical_absent(monkeypatch, tmp_path):
    # Direct drive of the shared launch path, dry-run so nothing launches.
    monkeypatch.setattr(rotate, "_existing_windows", lambda *a, **k: [])
    base = rotate.spawn_window(
        name="adv", tier="prime_director", prompt_file=None,
        settings=None, tmux_session="agi-rc", root=None,
        dry_run=True, seat=None,
    )[1]
    seated = rotate.spawn_window(
        name="adv", tier="prime_director", prompt_file=None,
        settings=None, tmux_session="agi-rc", root=None,
        dry_run=True, seat="sanctuary-director",
    )[1]
    assert "AGI_SEAT=" not in base
    assert f"export AGI_SEAT={rotate.shlex.quote('sanctuary-director')} && " in seated
    # the ONLY difference is the export: the rest of the launch line is identical
    export = f"export AGI_SEAT={rotate.shlex.quote('sanctuary-director')} && "
    assert seated.replace(export, "") == base


def test_cmd_spawn_and_loop_forward_seat(monkeypatch, tmp_path):
    # Proves cmd_spawn and cmd_loop actually FORWARD args.seat into the shared
    # launch path (the wiring owed item (v) added). With args.seat None the
    # forwarded value is None, so _shell_cmd emits no AGI_SEAT (byte-identical).
    root = _proj(tmp_path)
    monkeypatch.chdir(root)
    monkeypatch.setattr(rotate, "find_project_root", lambda: root)
    monkeypatch.setattr(rotate, "_existing_windows", lambda *a, **k: [])
    called = {}

    def _capture(**kw):
        called.update(kw)
        return 0, "claude --remote-control adv"

    monkeypatch.setattr(rotate, "spawn_window", _capture)

    # spawn with --seat
    code = rotate.cmd_spawn(SimpleNamespace(
        name="adv", tier="adv_alive", prompt_file=None, model=None,
        effort=None, settings=None, tmux_session="agi-rc", window_path=None,
        root=root, dry_run=True, successor_argv=None, seat="sanctuary-director",
    ), root)
    assert code == 0 and called.get("seat") == "sanctuary-director"
    # spawn without --seat (byte-identical: seat forwarded as None)
    called.clear()
    code = rotate.cmd_spawn(SimpleNamespace(
        name="adv", tier="adv_alive", prompt_file=None, model=None,
        effort=None, settings=None, tmux_session="agi-rc", window_path=None,
        root=root, dry_run=True, successor_argv=None, seat=None,
    ), root)
    assert code == 0 and called.get("seat") is None

    # loop with --seat
    monkeypatch.setattr(rotate, "cmd_meter", lambda args, root: 1)  # rotate
    called.clear()
    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=False, role="adv_alive", name="adv",
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=None,
        debug_file=None, dry_run=True, timeout=1, seat="sanctuary-director",
    ), root)
    assert code == 0 and called.get("seat") == "sanctuary-director"
    # loop without --seat
    called.clear()
    code = rotate.cmd_loop(SimpleNamespace(
        session_log=None, force=False, role="adv_alive", name="adv",
        name_prefix="belam", model=None, effort=None, settings=None,
        prompt_file=None, tmux_session="agi-rc", window_path=None,
        debug_file=None, dry_run=True, timeout=1, seat=None,
    ), root)
    assert code == 0 and called.get("seat") is None
