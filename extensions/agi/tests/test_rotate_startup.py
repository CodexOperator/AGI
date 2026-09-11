"""Startup first_turn (hypothesis:l4-startup-is-one-script-or-a-driven-prompt,
0b round) — the pure runner in rotate.py: allowlist refusal, placeholder
resolution, per-command timeout, byte-cap truncation, `## STARTUP OUTPUT`
composition, and dry-run-runs-nothing. Hermetic — no graph, no real spawn, no
tmux; subprocess.run is monkeypatched where a command must "hang" or "overflow"
deterministically."""
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate

# A fully-filled values map matching the 11 canonical placeholders.
VALUES = {
    "seat": "sanctuary-director",
    "succ_ref": "abc123",
    "succ_name": "sd-next",
    "succ_transcript": "/tmp/sd-next.jsonl",
    "pin_ref": "/tmp/sanctuary-director.meter",
    "gen": "11",
    "prime_ref": "7cff1a",
    "worktree": "/wt",
    "repo": "/repo",
    "tmux_session": "agi-rc",
    "pred_pids": "123 456",
}


class _Proc:
    def __init__(self, rc=0, out="", err=""):
        self.returncode = rc
        self.stdout = out
        self.stderr = err


def _fake_run(monkeypatch, proc):
    def _run(cmd, **kwargs):
        return proc
    monkeypatch.setattr(rotate.subprocess, "run", _run)


def test_resolve_every_placeholder_and_unknown_is_refused():
    resolved = rotate._resolve_startup_placeholders(
        "python3 extensions/agi/bin/x.py --seat {seat} {succ_ref} {prime_ref}",
        VALUES)
    assert "sanctuary-director" in resolved
    assert "abc123" in resolved
    assert "7cff1a" in resolved
    assert "{" not in resolved  # nothing silently left in
    with pytest.raises(ValueError) as ei:
        rotate._resolve_startup_placeholders("echo {bogus}", VALUES)
    assert "bogus" in str(ei.value)


def test_producing_refusal_allows_shipped_commands():
    # The live director template's first_turn list — every producing verb
    # must pass the allowlist (engine python + read-only git + ps + curl +
    # read-only tmux) with stdio filters allowed after `|`.
    shipped = [
        "python3 extensions/agi/bin/rotate.py whois --seat {seat} --record latest",
        "python3 extensions/agi/bin/send.py whois {succ_ref} --claim {seat}",
        "git -C {worktree} status -sb | head -5; git -C {repo} status -sb | head -3",
        "python3 extensions/agi/bin/send.py read {seat}",
        "python3 extensions/agi/bin/spawn_budget.py status; "
        "python3 extensions/agi/bin/provisioning.py status | head -4",
        "python3 extensions/agi/bin/write.py -h | sed -n 1,40p",
    ]
    for cmd in shipped:
        assert rotate._producing_refusal(cmd) is None, cmd


def test_d_allowlist_refusal_names_label():
    startup = {"first_turn": [{"label": "danger", "cmd": "rm -rf /"}]}
    res = rotate._run_first_turn_commands(startup, VALUES)
    assert res[0]["refused"], res
    assert "rm" in res[0]["refused"]
    block = rotate._compose_startup_output(res)
    assert "[danger] REFUSED" in block
    assert "not on startup.allow" in block


def test_e_unknown_placeholder_refused_by_label():
    startup = {"first_turn": [
        {"label": "bad", "cmd": "python3 extensions/agi/bin/x.py {bogus}"},
    ]}
    res = rotate._run_first_turn_commands(startup, VALUES)
    assert res[0]["refused"] and "bogus" in res[0]["refused"]
    block = rotate._compose_startup_output(res)
    assert "[bad] REFUSED" in block


def test_a_composes_startup_output_block():
    results = [
        {"label": "rotation-record", "cmd": "python3 .../rotate.py whois",
         "rc": 0, "output": "row: gen 11", "truncated": False},
        {"label": "inbox", "cmd": "python3 .../send.py read sd",
         "rc": 0, "output": "no dms", "truncated": False},
    ]
    block = rotate._compose_startup_output(results)
    assert "## STARTUP OUTPUT (rotate-self ran these for you; you ran nothing)" \
        in block
    assert "[rotation-record] exit 0" in block
    assert "[inbox] exit 0" in block
    assert "row: gen 11" in block


def test_b_timeout_is_caught_and_named(monkeypatch):
    def _hang(cmd, **kwargs):
        raise subprocess.TimeoutExpired(cmd, 1)
    monkeypatch.setattr(rotate.subprocess, "run", _hang)
    startup = {"first_turn": [{"label": "slow", "cmd": "ps -e"}],
               "first_turn_timeout_s": 1}
    res = rotate._run_first_turn_commands(startup, VALUES)
    assert res[0]["timed_out_after_s"] == 1
    block = rotate._compose_startup_output(res)
    assert "[slow] TIMEOUT (>1s)" in block


def test_c_byte_cap_truncates_and_says_so(monkeypatch):
    _fake_run(monkeypatch, _Proc(rc=0, out="x" * 500))
    startup = {"first_turn": [{"label": "noisy", "cmd": "ps -e"}],
               "byte_cap": 10}
    res = rotate._run_first_turn_commands(startup, VALUES)
    assert res[0]["truncated"] is True
    assert len(res[0]["output"]) == 10
    block = rotate._compose_startup_output(res)
    assert "(output truncated to 10 bytes)" in block


def test_f_dry_run_runs_nothing(tmp_path):
    marker_dir = tmp_path / "bin"
    marker_dir.mkdir(parents=True, exist_ok=True)
    (marker_dir / "probe.py").write_text(
        "from pathlib import Path\nPath(%r).write_text('hi')\n" % str(
            tmp_path / "marker.txt"), encoding="utf-8")
    script = str(marker_dir / "probe.py")
    startup = {"first_turn": [{"label": "probe", "cmd": f"python3 {script}"}]}

    dry = rotate._run_first_turn_commands(startup, VALUES, dry_run=True)
    assert dry[0]["dry"] is True
    assert not (tmp_path / "marker.txt").exists()

    live = rotate._run_first_turn_commands(startup, VALUES, dry_run=False)
    assert live[0]["rc"] == 0
    assert (tmp_path / "marker.txt").exists()


def test_g_shell_bypass_operators_refused_no_marker(tmp_path):
    # hypothesis:l4-first-turn-allowlist-cannot-be-bypassed-by-the-shell —
    # an unmodeled shell operator inside an OTHERWISE-allowlisted command is
    # refused (/( name named), so `$(touch ...)` and `>> ...` leave NO marker.
    marker_dir = tmp_path / "bin"
    marker_dir.mkdir(parents=True, exist_ok=True)
    (marker_dir / "probe.py").write_text(
        "from pathlib import Path\nPath(%r).write_text('hi')\n" % str(
            tmp_path / "boom.txt"), encoding="utf-8")
    script = str(marker_dir / "probe.py")
    marker = tmp_path / "shell-MARKER"
    substr = {"cmd_sub": f"python3 {script} $(touch {marker})",
              "redirect": f"python3 {script} >> {marker}",
              "andand": f"python3 {script} && touch {marker}",
              "oror": f"python3 {script} || touch {marker}"}
    for label, cmd in substr.items():
        res = rotate._run_first_turn_commands(
            {"first_turn": [{"label": label, "cmd": cmd}]}, VALUES)
        assert res[0]["refused"], (label, res)
        assert "unmodeled shell operator" in res[0]["refused"], (label, res)
        assert not marker.exists(), label
    # the allowlist-only triplet (no shell spell) still runs: control
    ctrl = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "ctrl", "cmd": f"python3 {script}"}]},
        VALUES)
    assert ctrl[0]["rc"] == 0
    assert (tmp_path / "boom.txt").exists()


def test_h_env_var_expands_without_shell(monkeypatch, tmp_path):
    # $VAR expansion is modeled securely: substituted from os.environ as a
    # literal argv token — never handed to a shell, and never RECORDED (fix b:
    # the result/dry-run `cmd` keeps `$VAR` LITERAL, byte-identical to the
    # authored text, so a secret never lands in the record). An unset var is
    # refused (named) rather than left literal.
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    script = str(bin_dir / "arg.py")
    (bin_dir / "arg.py").write_text(
        "import sys\nprint(sys.argv[1])\n", encoding="utf-8")
    cmd = f"python3 {script} $MY_SEAT"

    monkeypatch.setenv("MY_SEAT", "sanctuary-director")
    # dry-run record is byte-identical to the pre-expansion text ($VAR literal)
    res = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "auth", "cmd": cmd}]},
        VALUES, dry_run=True)
    assert res[0]["cmd"] == cmd, res
    assert "$MY_SEAT" in res[0]["cmd"], res
    assert "sanctuary-director" not in res[0]["cmd"], res
    # live run expands env only for execution
    live = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "auth", "cmd": cmd}]},
        VALUES, dry_run=False)
    assert live[0]["rc"] == 0, live
    assert "sanctuary-director" in live[0]["output"], live

    monkeypatch.delenv("MY_SEAT", raising=False)
    res = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "auth", "cmd": cmd}]},
        VALUES, dry_run=True)
    assert res[0]["refused"] and "MY_SEAT" in res[0]["refused"], res


def test_i_legit_pipeline_and_sequential_still_run_no_shell(tmp_path):
    # `|` pipeline and `;` sequential, both modeled separators, run WITHOUT a
    # shell. Producing stages are engine `python3 ...py` (allowlisted) and the
    # post-`|` filter is an allowed stdio filter.
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    (bin_dir / "p1.py").write_text("print('abc')", encoding="utf-8")
    (bin_dir / "p2.py").write_text("print('1')", encoding="utf-8")
    (bin_dir / "p3.py").write_text("print('2')", encoding="utf-8")
    p1, p2, p3 = (str(bin_dir / n) for n in ("p1.py", "p2.py", "p3.py"))

    pipe = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "pipe",
                          "cmd": f"python3 {p1} | sed -n 1,2p"}]}, VALUES)
    assert pipe[0]["rc"] == 0, pipe
    assert "abc" in pipe[0]["output"]

    seq = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "seq",
                          "cmd": f"python3 {p2}; python3 {p3}"}]}, VALUES)
    assert seq[0]["rc"] == 0, seq
    assert "1" in seq[0]["output"] and "2" in seq[0]["output"]


def test_i2_pipeline_filter_actually_truncates_stage_stdout(tmp_path):
    # hypothesis:l4-first-turn-filters-truncate — per `|` pipeline only the
    # LAST stage's stdout is appended, so a `| head -N` stdio filter really
    # truncates. A 100-line producer piped to `head -3` must yield exactly the
    # 3 filtered lines, NOT the producer's full 100 lines concatenated ahead of
    # the filter (the old behavior appended every stage's stdout).
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    (bin_dir / "producer.py").write_text(
        "\n".join(f"print({i})" for i in range(100)), encoding="utf-8")
    p = str(bin_dir / "producer.py")

    res = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "filt",
                          "cmd": f"python3 {p} | head -3"}]}, VALUES)
    assert res[0]["rc"] == 0, res
    lines = res[0]["output"].splitlines()
    assert lines == ["0", "1", "2"], res
    assert len(lines) == 3, res  # the filter truncated; no 100 producer lines

def test_i3_pipeline_failing_middle_stage_stderr_still_present(tmp_path):
    # Every stage's stderr is still merged in order — a failing middle stage
    # must stay visible even though its stdout is consumed by the next stage
    # and never echoed past the filter.
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    (bin_dir / "boom.py").write_text(
        "import sys\nprint('boom-err', file=sys.stderr)\nsys.exit(3)\n",
        encoding="utf-8")
    (bin_dir / "ident.py").write_text(
        "import sys\nprint('IDENT')\n", encoding="utf-8")
    boom = str(bin_dir / "boom.py")
    ident = str(bin_dir / "ident.py")

    res = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "mid",
                          "cmd": f"python3 {boom} | python3 {ident}"}]}, VALUES)
    # last stage exit code (ident normally 0) — but boom's stderr must be present
    assert res[0]["rc"] == 0, res
    assert "boom-err" in res[0]["output"], res
    assert "IDENT" in res[0]["output"], res
    assert res[0]["output"].index("boom-err") < res[0]["output"].index("IDENT"), res


def test_k_env_assignment_prefix_applied_and_stage_scoped(tmp_path):
    # fix (a): a leading `VAR=value` prefix is APPLIED to its stage's env (not
    # parsed-and-dropped), and it belongs to ONE stage — a `;`-sibling stage
    # does not inherit it.
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    script = str(bin_dir / "envprobe.py")
    (bin_dir / "envprobe.py").write_text(
        "import os\nprint('V=' + os.environ.get('MYPROBE','<unset>'))\n",
        encoding="utf-8")
    cmd = f"MYPROBE=hello python3 {script}"
    startup = {"env_allow": ["MYPROBE"],
               "first_turn": [{"label": "k", "cmd": cmd}]}
    res = rotate._run_first_turn_commands(startup, VALUES)
    assert res[0]["rc"] == 0, res
    assert "V=hello" in res[0]["output"], res
    assert res[0]["cmd"] == cmd, res  # record keeps the authored text

    cmd2 = (f"MYPROBE=hello python3 {script}; "
            f"python3 {script}")
    res2 = rotate._run_first_turn_commands(
        {"env_allow": ["MYPROBE"],
         "first_turn": [{"label": "k2", "cmd": cmd2}]}, VALUES)
    assert res2[0]["rc"] == 0, res2
    assert "V=hello" in res2[0]["output"], res2
    assert "V=<unset>" in res2[0]["output"], res2  # second stage isolated


def test_l_dry_run_cmd_keeps_dollar_var_literal(tmp_path):
    # fix (b): the dry-run/report `cmd` is byte-identical to the authored text
    # for a `$VAR`-bearing command — the secret never lands in the record even
    # when the var is set for execution.
    cmd = ("curl -s -m 20 https://openrouter.ai/api/v1/credits "
           "-H 'Authorization: Bearer $OPENROUTER_PROVISIONING_KEY'")
    os.environ["OPENROUTER_PROVISIONING_KEY"] = "sk-secret-12345"
    try:
        dry = rotate._run_first_turn_commands(
            {"first_turn": [{"label": "account", "cmd": cmd}]},
            VALUES, dry_run=True)
        assert dry[0]["cmd"] == cmd, dry
        assert "$OPENROUTER_PROVISIONING_KEY" in dry[0]["cmd"], dry
        assert "sk-secret-12345" not in dry[0]["cmd"], dry
    finally:
        os.environ.pop("OPENROUTER_PROVISIONING_KEY", None)


def test_m_quoted_separators_stay_whole(tmp_path):
    # hypothesis:l4-first-turn-allowlist-cannot-be-bypassed-by-the-shell,
    # residual hole: the OLD parser raw-split the command on `|`/`;` BEFORE
    # shlex, so a QUOTED argument containing a separator (e.g. `"a|b"`) was
    # cut mid-quote and the guard CRASHED (rotate-self died of a ValueError).
    # Now the single quote-aware tokenizer keeps `"a|b"` / `"x;y"` as ONE
    # argument token in both the allowlist judge and the no-shell executor.
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    (bin_dir / "arg.py").write_text(
        "import sys\nprint(sys.argv[1])\n", encoding="utf-8")
    script = str(bin_dir / "arg.py")
    for argval in ("a|b", "x;y"):
        cmd = f'python3 {script} "{argval}"'
        res = rotate._run_first_turn_commands(
            {"first_turn": [{"label": "q", "cmd": cmd}]}, VALUES)
        assert res[0]["rc"] == 0, (argval, res)
        assert res[0]["output"].strip() == argval, (argval, res)
    # judge and executor split on the SAME grammar (the whole point): both keep
    # the quoted torch whole — they cannot diverge.
    assert rotate._segment_parts(f'python3 {script} "a|b"') == \
        [["python3", script, "a|b"]]
    assert rotate._command_units(f'python3 {script} "a|b"') == \
        [[(["python3", script, "a|b"], {})]]


def test_n_quoted_separator_does_not_break_pipeline_or_seq(tmp_path):
    # A quoted `|` inside an argument is not a pipeline stage boundary, and a
    # quoted `;` is not a sequence boundary: the real unquoted `|`/`;` that
    # surround them still group exactly as before.
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    (bin_dir / "arg.py").write_text(
        "import sys; print(sys.argv[1])", encoding="utf-8")
    script = str(bin_dir / "arg.py")
    cmd = f'python3 {script} "q|w" | sed -n 1,2p; python3 {script} "r;s"'
    res = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "n", "cmd": cmd}]}, VALUES)
    assert res[0]["rc"] == 0, res
    assert "q|w" in res[0]["output"], res
    assert "r;s" in res[0]["output"], res


def test_o_unparseable_command_refused_not_crash(tmp_path):
    # Never raise out of the guard: an unparseable command (unbalanced quote,
    # trailing backslash) is a NAMED refusal, not a crash of rotate-self. Both
    # the pure judge and the full runner surface it.
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    (bin_dir / "arg.py").write_text("print('x')", encoding="utf-8")
    script = str(bin_dir / "arg.py")
    for bad in (f'python3 {script} "a|b',   # unbalanced double-quote
                f"python3 {script} 'x;y",  # unbalanced single-quote
                f'python3 {script} a\\'):    # trailing backslash
        res = rotate._run_first_turn_commands(
            {"first_turn": [{"label": "bad", "cmd": bad}]}, VALUES)
        assert res[0]["refused"] and "unparseable" in res[0]["refused"], \
            (bad, res)
        ref = rotate._producing_refusal(bad)
        assert ref and "unparseable" in ref, (bad, ref)

    # hypothesis:l4-first-turn-allowlist-cannot-be-bypassed-by-the-shell,
    # FALSIFIER demo: the attack string `python3 <ok.py> && touch MARKER` is
    # REFUSED by the guarded path (no marker). But if a mutation were to restore
    # the OLD executor (shell=True on the whole resolved string), the very same
    # phrase WOULD execute the second half and touch the marker. This pins that
    # it is the operator gate / no-shell executor, not coincidence, that stops
    # it: the raw phrase still actualizes under a shell.
    marker = tmp_path / "bypass-MARKER"
    ok_dir = tmp_path / "bin"
    ok_dir.mkdir(parents=True, exist_ok=True)
    (ok_dir / "ok.py").write_text("print('fine')\n", encoding="utf-8")
    attack = f"python3 {ok_dir / 'ok.py'} && touch {marker}"

    guarded = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "att", "cmd": attack}]}, VALUES)
    assert guarded[0]["refused"] and "unmodeled shell operator" in guarded[0]["refused"]
    assert not marker.exists()

    # the OLD path: whole string under shell=True (what the fix replaced).
    old = subprocess.run(attack, shell=True, capture_output=True, text=True)
    assert marker.exists(), (
        "old shell executor would have run the bypass; rc=%s out=%r"
        % (old.returncode, old.stdout))


def test_env_prefix_off_allowlist_refused_and_fake_never_runs(tmp_path):
    # hypothesis:l4-first-turn-env-prefix-is-judged — a leading `VAR=value`
    # prefix whose VAR is not on `startup.env_allow` (default EMPTY) is REFUSED
    # BEFORE execution, the record keeps the literal text, and the executor
    # never receives the command (a fake `PATH=` python3 never runs).
    fake_bin = tmp_path / "fakebin"
    fake_bin.mkdir(parents=True, exist_ok=True)
    marker = tmp_path / "fake-ran-MARKER"
    (fake_bin / "python3").write_text(
        "from pathlib import Path\nPath(%r).write_text('ran')\n"
        % str(marker), encoding="utf-8")
    os.chmod(fake_bin / "python3", 0o755)
    cmd = f"PATH={fake_bin} python3 -c 'print(1)'"
    res = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "ev", "cmd": cmd}]}, VALUES)
    assert res[0]["refused"], res
    assert "env prefix PATH not on startup.env_allow" in res[0]["refused"], res
    assert res[0]["cmd"] == cmd, res  # literal text kept in the record
    assert not marker.exists(), "fake python3 under PATH must never run"


def test_env_prefix_allowlisted_argv_exploit_is_refused(tmp_path):
    # hypothesis:l4-first-turn-env-prefix-is-judged — the GENUINE exploit, not
    # the `python3 -c` case. argv0 (`python3 <...>/extensions/foo.py`) is
    # ALLOWLIST-ADMISSIBLE: a `.py` script whose path contains `extensions/`, so
    # the producing judge passes it and pre-fix the only thing steering the
    # binary lookup toward the FAKE is the env prefix. The raw no-shell executor
    # really would run the fake (proof of vulnerability); the first-turn gate
    # refuses the command on the env prefix alone before the executor sees it.
    fake_bin = tmp_path / "fakebin"
    fake_bin.mkdir(parents=True, exist_ok=True)
    marker = tmp_path / "fake-ran-MARKER"
    # a /bin/sh fake is reliably executable under an overridden PATH (a bare
    # `python3` here resolves to fakebin/python3 via PATH, not the real exe)
    (fake_bin / "python3").write_text(
        "#!/bin/sh\necho ran > '%s'\n" % marker, encoding="utf-8")
    os.chmod(fake_bin / "python3", 0o755)
    # a dir literally containing `extensions/` so the allowlist judge (which
    # only checks the string ends .py and contains `extensions/`) would pass it
    ext_dir = tmp_path / "extensions"
    ext_dir.mkdir(parents=True, exist_ok=True)
    script = ext_dir / "foo.py"
    script.write_text("print('real')\n", encoding="utf-8")
    cmd = f"PATH={fake_bin} python3 {script}"

    # counterfactual assertions: the argv alone passes the judge (the prefix is
    # what must refuse it), and the raw executor would genuinely run the fake
    assert rotate._producing_refusal(cmd) is None, \
        "this argv must be ALLOWLIST-ADMISSIBLE or the test doesn't reproduce the bypass"
    rc, _ = rotate._run_units_no_shell(rotate._command_units(cmd), 60)
    assert rc == 0, rc
    assert marker.exists(), \
        "raw no-shell executor must run the fake for this to be a real exploit"
    marker.unlink()

    # now the actual first-turn gate: refused on the env prefix, marker absent
    res = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "ev", "cmd": cmd}]}, VALUES)
    assert res[0]["refused"], res
    assert "env prefix PATH not on startup.env_allow" in res[0]["refused"], res
    assert res[0]["cmd"] == cmd, res  # literal text kept in the record
    assert not marker.exists(), "fake python3 under PATH must never run past the gate"


def test_env_prefix_off_allowlist_dry_run_names_refusal(tmp_path):
    # dry-run reports the SAME env-prefix refusal (named) and runs nothing —
    # the gate fires before run, so dry wouldn't even reach a real python3.
    cmd = "LD_PRELOAD=/tmp/x.so python3 -c 'print(1)'"
    res = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "lp", "cmd": cmd}]},
        VALUES, dry_run=True)
    assert "refused" in res[0], res
    assert "env prefix LD_PRELOAD not on startup.env_allow" in res[0]["refused"], res


def test_env_prefix_not_allowed_fires_before_allowlist(tmp_path):
    # an env prefix on a DISALLOWED var is the named reason even when the argv
    # would already be off-allowlist (python -c) — the env judge runs first.
    cmd = "PATH=/tmp/x python3 -c 'print(1)'"
    res = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "xp", "cmd": cmd}]}, VALUES)
    assert "env prefix PATH not on startup.env_allow" in res[0]["refused"], res


def test_env_prefix_allowed_still_applies(tmp_path):
    # a fixture template declaring `env_allow: [FOO]` ADMITS `FOO=1 <allowed
    # cmd>` and the prefix reaches the child env (the executor still applies an
    # allowed prefix).
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    script = str(bin_dir / "show.py")
    (bin_dir / "show.py").write_text(
        "import os\nprint('FOO=' + os.environ.get('FOO', '<unset>'))\n",
        encoding="utf-8")
    cmd = f"FOO=1 python3 {script}"
    startup = {"env_allow": ["FOO"],
               "first_turn": [{"label": "allowed", "cmd": cmd}]}
    res = rotate._run_first_turn_commands(startup, VALUES)
    assert "refused" not in res[0], res
    assert res[0]["rc"] == 0, res
    assert "FOO=1" in res[0]["output"], res


def test_r_placeholder_injection_refused_no_marker(tmp_path):
    # hypothesis:l4-the-judge-runs-on-the-substituted-command — a placeholder
    # VALUE carries `; touch <marker>`. The template judge sees the un-resolved
    # `{seat}` and passes; the injected `touch` stage is only visible AFTER
    # placeholder substitution. The re-judge of exec_cmd refuses it, the marker
    # never appears, and the record holds the literal placeholder-expanded form.
    marker = tmp_path / "pwned-MARKER"
    vals = dict(VALUES, seat=f"seatA; touch {marker}")
    template = "python3 {worktree}/extensions/list.py {seat}"
    res = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "inj", "cmd": template}]}, vals)
    assert "refused" in res[0], res
    assert "not on startup.allow" in res[0]["refused"], res
    assert "touch" in res[0]["refused"], res
    assert not marker.exists(), res
    assert res[0]["cmd"] == (
        f"python3 /wt/extensions/list.py seatA; touch {marker}"), res


def test_s_env_var_injection_refused_no_marker(monkeypatch, tmp_path):
    # an env var VALUE carries `| touch <marker>`. The record keeps `$SEAT`
    # literal (fix b), while exec_cmd expands it for execution; the re-judge of
    # the substituted command refuses the injected `touch` stage before it runs.
    marker = tmp_path / "pwned2-MARKER"
    monkeypatch.setenv("SEAT", f"seatA | touch {marker}")
    cmd = "python3 {worktree}/extensions/list.py $SEAT"
    res = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "env", "cmd": cmd}]}, VALUES)
    assert "refused" in res[0], res
    assert "touch" in res[0]["refused"], res
    assert not marker.exists(), res
    assert res[0]["cmd"] == "python3 /wt/extensions/list.py $SEAT", res


def test_q_clean_substitution_still_runs(tmp_path):
    # a benign placeholder substitution still RUNS after the exec re-judge is
    # added — the new gate must not refuse the legitimate happy path.
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    script = str(bin_dir / "ok.py")
    (bin_dir / "ok.py").write_text("print('ok')\n", encoding="utf-8")
    template = f"python3 {script} {{seat}}"
    res = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "clean", "cmd": template}]}, VALUES)
    assert "refused" not in res[0], res
    assert res[0]["rc"] == 0, res
    assert "ok" in res[0]["output"], res


def test_r_empty_first_turn_placeholder_refused_named_no_marker(tmp_path):
    # hypothesis:l4-rotations-startup-commands-must-parse (kid 2, the named-
    # refusal half): a first_turn entry using `{succ_ref}` whose value is EMPTY
    # is REFUSED (placeholder named, "empty at spawn") and the executor NEVER
    # runs it — no marker file, instead of a usage-dump command on an empty slot.
    marker_dir = tmp_path / "bin"
    marker_dir.mkdir(parents=True, exist_ok=True)
    marker = tmp_path / "ran-MARKER"
    script = str(marker_dir / "probe.py")
    (marker_dir / "probe.py").write_text(
        "from pathlib import Path\nPath(%r).write_text('hi')\n" % str(marker),
        encoding="utf-8")
    cmd = f"python3 {script} {{succ_ref}}"
    vals = dict(VALUES, succ_ref="")
    res = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "seat-row", "cmd": cmd}]}, vals)
    assert "refused" in res[0], res
    assert "succ_ref" in res[0]["refused"], res
    assert "empty at spawn" in res[0]["refused"], res[0]["refused"]
    assert not marker.exists(), "executor must never run a refused entry"


def test_s_nonempty_first_turn_placeholder_still_runs(tmp_path):
    # the happy path is untouched: with `succ_ref` filled, the same command RUNS.
    marker_dir = tmp_path / "bin"
    marker_dir.mkdir(parents=True, exist_ok=True)
    marker = tmp_path / "ran-ok-MARKER"
    script = str(marker_dir / "ok.py")
    (marker_dir / "ok.py").write_text(
        "from pathlib import Path\nPath(%r).write_text('hi')\n" % str(marker),
        encoding="utf-8")
    cmd = f"python3 {script} {{succ_ref}}"
    res = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "seat-row", "cmd": cmd}]}, VALUES)
    assert "refused" not in res[0], res
    assert res[0]["rc"] == 0, res
    assert marker.exists(), res


def test_t_other_callers_resolve_empty_happily():
    # the HAZARD: `_resolve_startup_placeholders` has OTHER callers (the driven
    # `next` walk, bootstrap) where an empty placeholder is legitimate. The
    # refusal is opt-in on the first_turn path ONLY — the shared helper still
    # substitutes an empty placeholder to "" unless refuse_empty=True.
    resolved = rotate._resolve_startup_placeholders(
        "python3 extensions/agi/bin/send.py whois {succ_ref}", {"succ_ref": ""})
    assert resolved == "python3 extensions/agi/bin/send.py whois "
    assert "{" not in resolved
