"""Startup first_turn (hypothesis:l4-startup-is-one-script-or-a-driven-prompt,
0b round) — the pure runner in rotate.py: allowlist refusal, placeholder
resolution, per-command timeout, byte-cap truncation, `## STARTUP OUTPUT`
composition, and dry-run-runs-nothing. Hermetic — no graph, no real spawn, no
tmux; subprocess.run is monkeypatched where a command must "hang" or "overflow"
deterministically."""
import json
import os
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from agi.bin import rotate

# A fully-filled values map matching the 13 canonical placeholders.
VALUES = {
    "seat": "sanctuary-director",
    "succ_ref": "abc123",
    "succ_name": "sd-next",
    "succ_transcript": "/tmp/sd-next.jsonl",
    "pin_ref": "/tmp/sanctuary-director.meter",
    "gen": "11",
    "prime_ref": "7cff1a",
    "prime_key": "aabbccdd1122334455667788",
    "prime_seat": "belam",
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


def test_tmux_hash_brace_format_is_literal_but_bare_brace_is_not():
    # hypothesis:l4-startup-first-turn-is-performed-by-the-service-and-the-
    # hook-fires-at-turn-one (SL1.07). tmux's OWN format syntax `#{window_id}`
    # / `#{window_name}` is LITERAL tmux output the join step must pass
    # through; the resolver must NOT treat the `{window_id}` inside it as a
    # startup placeholder and refuse. A BARE `{window_id}` NOT preceded by `#`
    # must still refuse, so a genuinely missing placeholder cannot slip
    # through hidden inside tmux syntax.
    cmd = (
        "tmux list-windows -t {tmux_session} "
        "-F '#{window_id} #{window_name}' | grep {succ_name}"
    )
    resolved = rotate._resolve_startup_placeholders(cmd, VALUES)
    assert "#{window_id} #{window_name}" in resolved  # literal, byte-for-byte
    assert "agi-rc" in resolved
    assert "{tmux_session}" not in resolved
    assert "{succ_name}" not in resolved
    # A bare `{window_id}` (no `#`) is NOT tmux syntax and must refuse.
    with pytest.raises(ValueError) as ei:
        rotate._resolve_startup_placeholders("echo {window_id}", VALUES)
    assert "window_id" in str(ei.value)


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
    # and never echoed past the filter. Tested against the executor directly
    # (_run_units_no_shell): a pipe-fed PRODUCER (`python3 | python3`) is
    # deliberately REFUSED by the allowlist judge now (a first_turn pipeline
    # has no reason to pipe into a producer), so the stderr-merge property is
    # pinned at the executor layer, not through the full allowlist gate.
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    (bin_dir / "boom.py").write_text(
        "import sys\nprint('boom-err', file=sys.stderr)\nsys.exit(3)\n",
        encoding="utf-8")
    (bin_dir / "ident.py").write_text(
        "import sys\nprint('IDENT')\n", encoding="utf-8")
    boom = str(bin_dir / "boom.py")
    ident = str(bin_dir / "ident.py")

    units = [[(["python3", boom], {}), (["python3", ident], {})]]
    rc, out = rotate._run_units_no_shell(units, 30)
    # last stage exit code (ident normally 0) — but boom's stderr must be present
    assert rc == 0, (rc, out)
    assert "boom-err" in out, out
    assert "IDENT" in out, out
    assert out.index("boom-err") < out.index("IDENT"), out


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
    assert "env prefix PATH refused unconditionally" in res[0]["refused"], res
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
    assert "env prefix PATH refused unconditionally" in res[0]["refused"], res
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
    assert "env prefix LD_PRELOAD refused unconditionally" in res[0]["refused"], res


def test_env_prefix_not_allowed_fires_before_allowlist(tmp_path):
    # an env prefix on a DISALLOWED var is the named reason even when the argv
    # would already be off-allowlist (python -c) — the env judge runs first.
    cmd = "PATH=/tmp/x python3 -c 'print(1)'"
    res = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "xp", "cmd": cmd}]}, VALUES)
    assert "env prefix PATH refused unconditionally" in res[0]["refused"], res


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


def test_s_env_value_stays_one_argv_token_no_stage(monkeypatch, tmp_path):
    # hypothesis:l4-an-env-value-cannot-break-a-quoted-argument: an env value
    # carrying `| touch <marker>` is NO LONGER re-parsed as a stage. Env
    # expansion now happens PER argv TOKEN, after shlex tokenization, so the
    # value stays INSIDE the single `$SEAT` argument — the executor receives
    # argv[3] == exactly the value, nothing else executes, and the record keeps
    # `$SEAT` LITERAL (fix b). The security invariant is unchanged (no marker),
    # achieved now by the value being inert DATA rather than by refusing the
    # command.
    marker = tmp_path / "pwned2-MARKER"
    monkeypatch.setenv("SEAT", f"seatA | touch {marker}")
    captured = {}
    def _run(cmd, **kwargs):
        captured["argv"] = list(cmd)
        return _Proc(rc=0)
    monkeypatch.setattr(rotate.subprocess, "run", _run)
    cmd = "python3 {worktree}/extensions/list.py $SEAT"
    res = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "env", "cmd": cmd}]}, VALUES)
    assert "refused" not in res[0], res
    assert res[0]["rc"] == 0, res
    # ONE argv element holds the whole value — pipe and all, no extra stage
    assert captured["argv"] == [
        "python3", "/wt/extensions/list.py", f"seatA | touch {marker}"], \
        captured
    assert str(captured["argv"]) == ("['python3', '/wt/extensions/list.py', "
                                     "'seatA | touch %s']" % marker), captured
    assert not marker.exists(), res          # nothing actually executed
    assert res[0]["cmd"] == "python3 /wt/extensions/list.py $SEAT", res


def test_s2_env_value_semicolon_stays_one_token(monkeypatch, tmp_path):
    # the `;`-arm of the same claim: a value carrying `; cat ...` is a single
    # argv element, not a sequential-unit boundary — `cat` never runs, the
    # record keeps the literal `$SEAT`, and no secret-shaped fragment surfaces.
    secret = "tkn-yz-9f00ba"
    monkeypatch.setenv("SEAT", f"x; cat {secret}")
    captured = {}
    def _run(cmd, **kwargs):
        captured["argv"] = list(cmd)
        return _Proc(rc=0)
    monkeypatch.setattr(rotate.subprocess, "run", _run)
    cmd = "python3 {worktree}/extensions/list.py $SEAT"
    res = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "env", "cmd": cmd}]}, VALUES)
    assert "refused" not in res[0], res
    assert captured["argv"][-1] == f"x; cat {secret}", captured
    assert res[0]["cmd"] == "python3 /wt/extensions/list.py $SEAT", res
    assert secret not in res[0]["cmd"], res


def test_s3_env_value_never_in_record_or_output(monkeypatch, tmp_path):
    # the VALUE (the secret-shaped payload) stays out of the record and the
    # rendered STARTUP OUTPUT block — it only ever lived in the exec argv, which
    # the record/report never echoes (fix b: record keeps `$VAR` literal).
    secret = "tkn-yz-9f00ba"
    monkeypatch.setenv("SEAT", f"x; cat {secret}")
    def _run(cmd, **kwargs):
        return _Proc(rc=0)
    monkeypatch.setattr(rotate.subprocess, "run", _run)
    cmd = "python3 {worktree}/extensions/list.py $SEAT"
    res = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "env", "cmd": cmd}]}, VALUES)
    assert secret not in str(res), res
    block = rotate._compose_startup_output(res)
    assert secret not in block, block
    assert res[0]["cmd"] == "python3 /wt/extensions/list.py $SEAT", res


def test_s4_placeholder_injection_still_refuses(tmp_path):
    # hypothesis:l4-the-refusal-names-the-record-stage-not-the-expanded-tokens:
    # the PLACEHOLDER injection path is untouched by the env-value scrub — a
    # `{seat}` value that injects an off-allowlist `cat` stage is still refused
    # by name, the marker never runs, and the record keeps the placeholder's
    # (already-substituted) value, exactly as test_r pins. Only ENV vars stay
    # literal; placeholder VALUES are record content by design (fix b).
    vals = dict(VALUES, seat="a | cat /etc/hostname")
    cmd = "python3 {worktree}/extensions/list.py {seat}"
    res = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "ph", "cmd": cmd}]}, vals)
    assert "refused" in res[0], res
    assert "cat" in res[0]["refused"], res
    assert "not on startup.allow" in res[0]["refused"], res


def test_env_value_cannot_add_argv_element(monkeypatch):
    # hypothesis:l4-an-env-value-cannot-break-a-quoted-argument, claim (a), on
    # an actually-allowable producer: `python3 <ok.py> $SEAT` (the engine-ya
    # producer whose allowlist does not reject `$`) with SEAT carrying a double
    # quote + space must stay inside the ONE `$SEAT` element — no extra
    # `--no-such-flag` argv token is split out by a re-parse. (git's own
    # `-C "$WT"` form is separately refused at TEMPLATE time by the git
    # `$`-in-`-C`-path guard — pinned by test_git_dollar_c_path_is_blocked
    # _at_template_time below."""
    monkeypatch.setenv("SEAT", 'x" --no-such-flag "y')
    captured = {}
    def _run(cmd, **kwargs):
        captured["argv"] = list(cmd)
        return _Proc(rc=0)
    monkeypatch.setattr(rotate.subprocess, "run", _run)
    cmd = "python3 {worktree}/extensions/list.py $SEAT"
    res = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "p", "cmd": cmd}]}, VALUES)
    assert "refused" not in res[0], res
    assert captured["argv"] == ["python3", "/wt/extensions/list.py",
                                'x" --no-such-flag "y'], captured
    assert "--no-such-flag" not in captured["argv"][2:], captured


def test_env_value_pipe_stays_in_one_arg_no_operator_refusal(monkeypatch):
    # hypothesis:l4-an-env-value-cannot-break-a-quoted-argument, claim (b): a
    # value carrying `| sh` is ONE argv token — no second stage, and the
    # operator/allowlist refusal does NOT fire on it (it is data now). The
    # single producer runs; a mocked rc proves nothing extra executed.
    monkeypatch.setenv("SEAT", "x | sh")
    captured = {}
    def _run(cmd, **kwargs):
        captured["argv"] = list(cmd)
        return _Proc(rc=2)
    monkeypatch.setattr(rotate.subprocess, "run", _run)
    cmd = "python3 {worktree}/extensions/list.py $SEAT"
    res = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "p", "cmd": cmd}]}, VALUES)
    assert "refused" not in res[0], res
    assert captured["argv"] == ["python3", "/wt/extensions/list.py",
                                "x | sh"], captured
    assert res[0]["rc"] == 2, res


def test_git_dollar_c_path_is_blocked_at_template_time(monkeypatch):
    # the claim's OWN example template `git -C "$WT" status -sb` cannot even
    # reach the re-judge: the git `-C` ARG allowlist (hypothesis:l4-a-
    # producing-git-stage-is-argument-restricted) refuses a `$` (backtick, `~`)
    # in the `-C` path value AT TEMPLATE TIME, so a literal `$WT` as the path
    # is refused before env expansion. That is the tightest git defence-in-
    # depth; the per-token fix keeps every other producer (python3/ps/...) from
    # re-parsing an env value, and this test pins that git stays closed even if
    # the `-C` guard were ever loosened.
    monkeypatch.setenv("WT", 'x" --no-such-flag "y')
    cmd = 'git -C "$WT" status -sb'
    res = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "git", "cmd": cmd}]}, VALUES)
    assert "refused" in res[0], res
    ref = res[0]["refused"]
    assert "producer git" in ref, ref
    assert "status" in ref or "allowlist" in ref, ref
    assert res[0]["cmd"] == cmd, res  # record keeps the literal template


def test_scrub_keeps_short_innocent_words_byte_identical(monkeypatch):
    # claim (c): the scrub drops a message word only when it is >= 4 chars, so
    # short innocent words that are substrings of some env VALUE (`on`,`the`,
    # `me`,`in`) survive — the message does not collapse to the bare trailer.
    monkeypatch.setenv("WT", "me on the in producer")
    msg = "not on the allowlist: producer git me on the in"
    out = rotate._scrub_injected_refusal(msg, "echo $WT")
    assert out == msg, out  # no word (<4 or template) was dropped


def test_scrub_redacts_long_env_fragment_still(monkeypatch):
    # claim (d): a 12-char fragment of $HOME (>= 4 chars, a substring of the
    # VALUE, not record text) is STILL dropped and redacted to the trailer —
    # the longer-fragment redaction is unchanged.
    monkeypatch.setenv("HOME", "/home/ubuntu-probe")
    msg = "producer /home/ubuntu-probe not on the allowlist"
    out = rotate._scrub_injected_refusal(msg, "echo $HOME")
    assert "/home/ubuntu-probe" not in out, out
    assert "<expanded value redacted>" in out, out
    assert "$HOME" in out, out


def test_scrub_keeps_template_word_that_coincides_with_env_fragment(monkeypatch):
    # the "not a word of the message template" gate: a template prose word
    # (`producer`) that happens to be a substring of an env VALUE is NOT
    # treated as an injection — it survives, even when >= 4 chars.
    monkeypatch.setenv("WT", "cheeseproducer")
    msg = "producer git x not on the allowlist"
    out = rotate._scrub_injected_refusal(msg, "echo $WT")
    assert "producer" in out, out
    assert "not on the allowlist" in out, out


def test_placeholder_injection_still_refuses_with_per_token_env(monkeypatch,
                                                                tmp_path):
    # hypothesis:l4-the-judge-runs-on-the-substituted-command — the PLACEHOLDER
    # injection path is UNCHANGED by per-token env expansion: `{seat}` inserts
    # a real `|` INTO the string BEFORE tokenization, so the injected `touch`
    # stage is still a genuine stage and still REFUSED, even while an env var
    # carrying similar text is data. The marker never runs.
    marker = tmp_path / "pwned3-MARKER"
    monkeypatch.setenv("SEAT", "a | touch placeholder")
    vals = dict(VALUES, seat=f"a | touch {marker}")
    cmd = "python3 {worktree}/extensions/list.py {seat}"
    res = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "ph", "cmd": cmd}]}, vals)
    assert "refused" in res[0], res
    assert "not on startup.allow" in res[0]["refused"], res
    assert not marker.exists(), res



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


def test_u_empty_placeholder_with_declared_fallback_substitutes_by_key():
    # hypothesis:l4-prime-authority-resolves-by-key-when-the-prime-rows-
    # session-ref-is-empty... — a used placeholder whose value is EMPTY is
    # substituted by a WHOLE resolvable FRAGMENT (flags included), so a prime
    # row whose session_ref is empty under SL7.06's default still resolves
    # authority by the row's pubkey. The per-placeholder code map
    # `_STARTUP_FALLBACKS["prime_ref"]` is the by-key whois form: substituting
    # only the pubkey VALUE would land it in the POSITIONAL session_ref slot,
    # where whois answers NO-MATCH, never IS-AUTHORIZED.
    vals = dict(VALUES, prime_ref="", prime_key="a1b2c3d4e5f6")
    resolved = rotate._resolve_startup_placeholders(
        "python3 extensions/agi/bin/send.py whois {prime_ref} --claim belam",
        vals, refuse_empty=True)
    assert "--key a1b2c3d4e5f6" in resolved      # the FRAGMENT, flags included
    assert "{prime_ref}" not in resolved
    assert "{prime_key}" not in resolved
    # the resolved whole command still passes the producing allowlist
    assert rotate._producing_refusal(resolved) is None, resolved


def test_u2_entry_level_fallback_overrides_the_code_map():
    # a per-entry `fallback:` fragment wins over the code map; here the entry
    # wants the by-name form for the same empty placeholder.
    vals = dict(VALUES, prime_ref="", prime_key="a1b2c3d4e5f6",
                prime_seat="belam")
    resolved = rotate._resolve_startup_placeholders(
        "python3 extensions/agi/bin/send.py whois {prime_ref}",
        vals, refuse_empty=True, fallback="--seat {prime_seat}")
    assert "--seat belam" in resolved
    assert "{prime_ref}" not in resolved


def test_u3_fallback_fragment_references_empty_placeholder_refuses():
    # a fragment must not substitute itself; that is a broken fallback, not a
    # silent self-reference.
    vals = dict(VALUES, prime_ref="")
    with pytest.raises(ValueError) as ei:
        rotate._resolve_startup_placeholders(
            "python3 extensions/agi/bin/send.py whois {prime_ref}",
            vals, refuse_empty=True, fallback="--seat {prime_ref}")
    assert "prime_ref" in str(ei.value)


def test_v_fallback_value_also_empty_still_refuses():
    # a fallback whose value is also empty fails CLOSED: the refusal names the
    # placeholder AND the exhausted fallback — a placeholder never runs empty
    # and never silently self-declares a fallback.
    vals = dict(VALUES, prime_ref="", prime_key="")
    with pytest.raises(ValueError) as ei:
        rotate._resolve_startup_placeholders(
            "python3 extensions/agi/bin/send.py whois {prime_ref}",
            vals, refuse_empty=True)
    assert "prime_ref" in str(ei.value)
    assert "prime_key" in str(ei.value)


def test_w_first_turn_entry_without_any_fallback_still_refuses():
    # the FALSIFIER guard: the fallback substitutes ONLY when a fallback
    # EXISTS (a per-entry `fallback:`, or the per-placeholder code map). An
    # entry whose emptied placeholder has NEITHER refuses exactly as before —
    # a placeholder never stops meaning empty just because a fallback
    # mechanism exists. `{succ_ref}` has no code-map entry, so it is the
    # honest probe.
    vals = dict(VALUES, succ_ref="")
    with pytest.raises(ValueError) as ei:
        rotate._resolve_startup_placeholders(
            "python3 extensions/agi/bin/send.py whois {succ_ref}",
            vals, refuse_empty=True)
    assert "succ_ref" in str(ei.value)
    assert "empty at spawn" in str(ei.value)


def test_e_prime_authority_startup_block_shows_authorized_by_key(monkeypatch):
    # (e): the CURRENT director-template shape (no per-entry fallback) with an
    # EMPTY prime session_ref must resolve by key, pass the producing judge
    # (None), run, and the composed ## STARTUP OUTPUT must show IS-AUTHORIZED
    # by key — proving the transition mechanism, not the direct re-cut.
    captured = {}
    def _run(argv, **kwargs):
        captured["argv"] = list(argv)
        return _Proc(0, "IS-AUTHORIZED by key: "
                     "abcdef1234567890 (belam) window @123")
    monkeypatch.setattr(rotate.subprocess, "run", _run)
    vals = dict(VALUES, prime_ref="", prime_key="abcdef1234567890",
                prime_seat="belam")
    startup = {"first_turn": [{
        "label": "prime-authority",
        "cmd": "python3 extensions/agi/bin/send.py whois {prime_ref} "
               "--claim belam",
    }]}
    res = rotate._run_first_turn_commands(startup, vals)
    assert not res[0].get("refused"), res[0]
    assert "rc" in res[0] and res[0]["rc"] == 0
    assert "--key" in res[0]["cmd"] and "abcdef1234567890" in res[0]["cmd"]
    assert captured["argv"][:3] == ["python3",
                                     "extensions/agi/bin/send.py", "whois"]
    assert "--key" in captured["argv"] and "abcdef1234567890" \
        in captured["argv"]
    assert captured["argv"].index("--key") < \
        captured["argv"].index("abcdef1234567890")
    block = rotate._compose_startup_output(res)
    assert "[prime-authority] exit 0" in block
    assert "$ python3 extensions/agi/bin/send.py whois --key " \
        "abcdef1234567890 --claim belam" in block
    assert "IS-AUTHORIZED by key" in block


def _graph_root() -> Path:
    # The graph root the LIVE config test reads from: the real `.agi/` of the
    # checkout under test (parents[3] = worktree root; the same resolution
    # `locations.find_project_root` would produce walking up from the test).
    return Path(__file__).resolve().parents[3] / ".agi"


def test_e_live_prime_authority_entry_resolves_by_key_from_the_live_node(
        monkeypatch):
    # LIVE-CONFIG (the standing kid rule: a test of live config reads the
    # live node, never a copied list). Load `config:rotations` through the
    # SAME loader rotate.py uses (`_load_templates`), take the REAL
    # `prime-authority` first_turn entry from the director template and its
    # prime_director mirror, set the values map from `_first_turn_values`
    # with the prime row's session_ref EMPTY (the SL7.06 default), and assert
    # the entry resolves WITHOUT a refusal to the by-key form (`--key
    # <pubkey>`) and that the resolved whole command still passes the
    # producing allowlist. Asserts the RESOLVED SHAPE, not which path
    # produced it: if the live template has been re-cut to `--key
    # {prime_key}` the test still passes.
    #
    # SEAM-INJECTED: `_first_turn_values` routes the pushed-prime read
    # through `_prime_pushed_seats`, which is monkeypatched here with a
    # canned PUSHED row so this LIVE-CONFIG test performs NO real
    # `git fetch origin <name>` inside the offline suite
    # (hypothesis:l4-rotate-self-fetches-the-pushed-season-ref-once-per-run-
    # through-a-seam-and-no-suite-test-reaches-origin). The row's pubkey is
    # a stand-in; the claim under test is the LIVE TEMPLATE's by-key
    # resolution, not the live seats value.
    rotate._prime_rows_fetch_clear()
    fake_key = "c0ffee" + "0" * 34
    monkeypatch.setattr(rotate, "_prime_pushed_seats", lambda root, ref: (
        [{"role": "prime_director", "name": "sanctuary-director",
          "session_ref": "", "pubkey": fake_key}], "SHA", ref))
    # Skips (not fails) only when the
    # graph/rotations node is genuinely absent so the hermetic suite stays
    # runnable off-repo; a PRESENT node that fails to resolve is a live drift
    # finding, not a skip.
    #
    # hypothesis:l4-prime-authority-resolves-by-key-when-the-prime-rows-
    # session-ref-is-empty-and-a-placeholder-with-a-fallback-never-refuses
    graph = _graph_root()
    node = rotate._rotations_node_path(graph)
    if not node.exists():
        pytest.skip(f"live rotations node absent: {node}")
    templates = rotate._load_templates(graph)
    if not templates:
        pytest.skip(f"live rotations node declares no templates: {node}")
    tested = []
    for tmpl_name in ("director", "prime_director"):
        tmpl = templates.get(tmpl_name)
        if not tmpl or not isinstance(tmpl, dict):
            pytest.fail(
                f"live rotations node has no '{tmpl_name}' template: {node}")
        entries = (tmpl.get("startup") or {}).get("first_turn") or []
        ent = next((e for e in entries
                    if isinstance(e, dict)
                    and e.get("label") == "prime-authority"), None)
        if ent is None:
            pytest.fail(
                f"{tmpl_name} template has no 'prime-authority' first_turn "
                f"entry in live {node}")
        live_cmd = ent.get("cmd", "")
        live_fallback = ent.get("fallback") or ""
        # FULLY-FILLED canonical map from the live seats registry, then the
        # one SL7.06 default: the prime row's session_ref is EMPTY.
        vals = rotate._first_turn_values(
            graph, seat="sanctuary-director", gen="1",
            succ_name="sd-next")
        vals = dict(vals, prime_ref="")
        if not vals.get("prime_key"):
            pytest.fail(
                f"prime row in live seats has no pubkey; cannot assert the "
                f"by-key form ({tmpl_name} prime-authority)")
        try:
            resolved = rotate._resolve_startup_placeholders(
                live_cmd, vals, refuse_empty=True, fallback=live_fallback)
        except ValueError as exc:
            pytest.fail(
                f"live {tmpl_name} prime-authority cmd REFUSES with prime "
                f"session_ref empty: {exc}\n  cmd: {live_cmd}")
        assert "--key" in resolved, (
            f"live {tmpl_name} prime-authority did not resolve to the "
            f"by-key form; got: {resolved}")
        assert vals["prime_key"] in resolved
        assert "{prime_ref}" not in resolved
        assert "{prime_key}" not in resolved
        refusal = rotate._producing_refusal(resolved)
        assert refusal is None, (
            f"live {tmpl_name} prime-authority resolved form refused: "
            f"{refusal}: {resolved}")
        tested.append((tmpl_name, live_cmd, resolved))
    # Report the EXACT live line read, so the round's acceptance (e) is tied
    # to the node bytes, not a re-derived shape.
    assert tested, "no live prime-authority entry resolved"
    for tmpl_name, live_cmd, resolved in tested:
        print(f"  [{tmpl_name}] live cmd : {live_cmd}")
        print(f"  [{tmpl_name}] resolved: {resolved}")


def test_filter_allowlist_refuses_escape_list(tmp_path):
    # hypothesis:l4-a-filter-stage-is-argument-restricted / goal:g17.1 ruling
    # (merge-up 33): the post-`|` filter judge is an ALLOWLIST parser, not a
    # denylist. Every escape of the known list is refused by NAME — a free
    # operand where none is allowed, an off-allowlist option or `--long`, a
    # `$`/`~`/backtick echo leak, awk's program — all as `filter <exe> <tok>
    # not on the allowlist`.
    P = "python3 extensions/agi/bin/foo.py"
    refused = [
        (f"{P} | head -1 /etc/hostname", "filter head /etc/hostname not on the allowlist"),
        (f"{P} | cat /etc/hostname", "filter cat /etc/hostname not on the allowlist"),
        (f"{P} | tail -n 5 /var/log/syslog", "filter tail /var/log/syslog not on the allowlist"),
        (f"{P} | grep -f /tmp/pat.txt", "filter grep -f not on the allowlist"),
        (f"{P} | head -1 .env", "filter head .env not on the allowlist"),
        (f"{P} | sort .env", "filter sort .env not on the allowlist"),
        (f"{P} | wc -l .env", "filter wc .env not on the allowlist"),
        (f"{P} | uniq x", "filter uniq x not on the allowlist"),
        (f"{P} | cut x", "filter cut x not on the allowlist"),
        (f"{P} | tail .env", "filter tail .env not on the allowlist"),
        (f"{P} | grep foo x y", "filter grep x not on the allowlist"),
        (f"{P} | sed s/a/b/g .env", "filter sed .env not on the allowlist"),
        (f"{P} | tr a b c", "filter tr c not on the allowlist"),
        (f"{P} | sort -o M", "filter sort -o not on the allowlist"),
        (f"{P} | sort --output=M", "filter sort --output=M not on the allowlist"),
        (f"{P} | grep -f3", "filter grep -f not on the allowlist"),
        (f"{P} | sed -i s/a/b/", "filter sed -i not on the allowlist"),
        (f"{P} | echo $SMOKE_SECRET", "filter echo $SMOKE_SECRET not on the allowlist"),
        (f"{P} | echo ~", "filter echo ~ not on the allowlist"),
        # sed `$`-address is now refused as a forbidden char too: `$` on any
        # filter token (the `$d` would fail at exec anyway — env var never set).
        (f"{P} | sed '$d'", "filter sed $d not on the allowlist"),
    ]
    for cmd, name in refused:
        ref = rotate._producing_refusal(cmd)
        assert ref == name, (cmd, ref)


def test_filter_awk_refused_outright(tmp_path):
    # `| awk BEGIN{system(...)}` executes a command through awk's program body;
    # awk is refused outright (its program can reach system/getline/`>`/`|`).
    cmd = "python3 extensions/agi/bin/foo.py | awk 'BEGIN{system(\"touch /tmp/x\")}'"
    assert rotate._producing_refusal(cmd) == "filter awk"


def test_filter_short_cluster_expansion_pinned(tmp_path):
    # Short-option CLUSTERS are expanded character by character: `-ni` is
    # `-n -i`, `-if` is `-i -f`. An unlisted letter INSIDE a cluster is
    # refused (`-f` is off grep's allowlist), so the escape `grep -if pats`
    # and `sed -ni p` both fall; the same letters that are ON a list pass.
    P = "python3 extensions/agi/bin/foo.py"
    assert (rotate._producing_refusal(f"{P} | grep -if pats")
            == "filter grep -f not on the allowlist")
    assert (rotate._producing_refusal(f"{P} | sed -ni p")
            == "filter sed -i not on the allowlist")
    assert rotate._producing_refusal(f"{P} | grep -in x") is None
    assert rotate._producing_refusal(f"{P} | sort -rn") is None
    assert rotate._producing_refusal(f"{P} | sort -k2 -nr") is None


def test_producing_refusal_path_form_exe_and_sed_grammar(tmp_path):
    # hypothesis:l4-a-filter-exe-is-judged-by-path-and-a-sed-grammar-
    # anchors-its-fields. TWO escapes must be REFUSED by name.
    P = "python3 extensions/agi/bin/foo.py"
    name = "producer %s is a path, not an allowlisted name"
    # (1) EXE TOKEN BY PATH: a path-form exe (any `/`) is refused BY NAME
    # for unit-leading producers AND pipe-fed filter stages; basename would
    # silently allow an off-allowlist binary behind a path.
    assert rotate._producing_refusal(f"{P} | /tmp/x/head -5") == \
        name % "/tmp/x/head"
    assert rotate._producing_refusal(f"{P} | ./head -5") == name % "./head"
    assert rotate._producing_refusal("/tmp/x/git status -sb") == name % "/tmp/x/git"
    assert rotate._producing_refusal("git status -sb | /tmp/x/head -5") == \
        name % "/tmp/x/head"
    # (2) SED GRAMMAR BACKTRACKING: the delimiter may NOT be a flag char or
    # alphanumeric, and each field is anchored to never contain it — so a
    # delimiter-absorbed `e` flag can no longer pass. Benign forms still run.
    for cmd, allowed in [("s/x/y/", True), ("s/x/y/g", True),
                         ("s/x/y/e", False), ("s|x|y|e", False),
                         ("sgxgygeg", False), ("s0x0y0e0", False)]:
        ref = rotate._producing_refusal(f"{P} | sed {cmd}")
        if allowed:
            assert ref is None, (cmd, ref)
        else:
            assert ref == "filter sed program", (cmd, ref)


def test_filter_sed_program_grammar_allowlist(tmp_path):
    # sed programs are allowlisted by GRAMMAR, not by token. A `;`-split
    # command must be `s<d>...<d>...<d>[gIp0-9]*` or an address command
    # (`A`,`A,B`,`/re/`,`$` + one of p/d/q/!d) — sed `e` executes a shell
    # command (`1e id` runs `id`) and `r`/`w` read/write files. sed's FLAGS
    # are themselves allowlisted (`-n -E -r` only), so `-i`/`-e`/`-f` are
    # refused as off-allowlist before the program is even read.
    P = "python3 extensions/agi/bin/foo.py"
    for cmd in [f"{P} | sed e id", f"{P} | sed '1e id'",
                f"{P} | sed 'w /tmp/f'", f"{P} | sed 'r /tmp/f'",
                f"{P} | sed '/foo/{{;s/a/b/;}}'"]:
        assert rotate._producing_refusal(cmd) == "filter sed program", cmd
    # a single path-looking positional fails the grammar, not the path rule
    assert rotate._producing_refusal(f"{P} | sed /etc/passwd") == "filter sed program"
    # benign grammar-form programs still run. `sed '$d'` (a `$` address) is
    # NOT here: `$` is _FILTER_FORBIDDEN across every filter token, and `$d`
    # ends up refused by our new token-sweep (it would also fail at exec time
    # — env var $d is never set).
    for cmd in ["sed -n 1,40p", "sed s/x/y/g", "sed 's/a b/c/'", "sed 2d",
                "sed 5q", "sed /foo/d", "sed 1,5p",
                "sed s/x//I", "sed 's/a\\/b/c/g'", "sed -E s/x/y/g",
                "sed -r s/x/y/"]:
        assert rotate._producing_refusal(f"{P} | {cmd}") is None, cmd


def test_filter_grep_pattern_option_kills_the_free_positional(tmp_path):
    # grep/egrep `-e PAT` SUPPLIES the pattern, so the one free positional
    # the single-pattern budget allowed was actually a FILE: `| grep -e x
    # .env` read the key file into the rotation record AND the successor's
    # STARTUP OUTPUT. Once `-e` has supplied the pattern, the free-positional
    # budget is ZERO — a further non-option token is refused.
    for cmd in ["python3 extensions/agi/bin/foo.py | grep -e x .env",
                "python3 extensions/agi/bin/foo.py | egrep -e x .env"]:
        ref = rotate._producing_refusal(cmd)
        assert ref == "filter grep .env not on the allowlist" \
            or ref == "filter egrep .env not on the allowlist", (cmd, ref)
    # pattern supplied by -e / free positional, no file: runs
    for cmd in ["python3 extensions/agi/bin/foo.py | grep -e x",
                "python3 extensions/agi/bin/foo.py | egrep -e x",
                "python3 extensions/agi/bin/foo.py | grep -c x",
                "python3 extensions/agi/bin/foo.py | grep -i x",
                "python3 extensions/agi/bin/foo.py | grep foo"]:
        assert rotate._producing_refusal(cmd) is None, cmd


def test_git_unit_leading_refused_by_argument(tmp_path):
    # hypothesis:l4-a-producing-git-stage-is-argument-restricted: a unit-
    # LEADING git stage must be refused by NAMED TOKEN, not accepted on its
    # read-only subcommand alone. These used to return None (accepted) and
    # leak file contents / write a file / run a program: `git log -p -- .env`
    # prints a tracked file into the rotation record, `git diff HEAD -- .env`
    # same, `git --all -p` same, `git -c core.pager=less log` runs a pager
    # program, `git log --output=FILE` writes a file.
    bad = [
        "git log -p -- .env",
        "git diff HEAD -- .env",
        "git log --all -p -- .env",
        "git -c core.pager=less log",
        "git log --output=/tmp/x",
    ]
    for cmd in bad:
        ref = rotate._producing_refusal(cmd)
        assert ref is not None, cmd
        assert ref.startswith("producer git "), cmd


def test_git_off_allowlist_token_names_itself():
    # the refusal must NAME the offending token, not just refuse the stage
    assert rotate._producing_refusal("git log -p -- .env") \
        == "producer git -p not on the allowlist"
    assert rotate._producing_refusal("git log --output=/tmp/x") \
        == "producer git --output not on the allowlist"
    assert "-c" in rotate._producing_refusal("git -c core.pager=less log")


def _shared_live_first_turn_cmds(path=None) -> list:
    """Every startup.first_turn cmd from BOTH templates, flattening the SHARED
    reader (`test_rotate_templates._live_first_turn`, which has the `path=`
    seam). There is exactly ONE copy of the rotations.md loader — the shared
    `_live_first_turn` in test_rotate_templates.py — and this module consumes
    it, never re-reads the node (hypothesis:l4-the-drifted-node-test-is-in-
    the-suite: the two near-identical live readers are consolidated).
    It never writes the node."""
    from tests.test_rotate_templates import _live_first_turn  # shared loader
    cmds = []
    for entries in _live_first_turn(path).values():
        for e in entries:
            if isinstance(e, dict) and e.get("cmd"):
                cmds.append(e["cmd"])
    return cmds


def test_git_live_template_commands_still_pass():
    # every git command in the LIVE rotations template
    # (.agi/nodes/.geometry/rotations.md) keeps passing the allowlist -- read
    # from the node, never a hand-copied list (hypothesis:l4-a-test-of-live-
    # config-reads-the-live-node). A NEW off-allowlist git line added to the
    # live node must turn this test red. The DRIFTED-COPY falsifier below is
    # the /tmp half of this pair; this is the LIVE half and stays.
    import tempfile
    git_cmds = [c for c in _shared_live_first_turn_cmds() if "git" in c]
    assert git_cmds, "no git commands in the live rotations.md first_turn lists"
    with tempfile.TemporaryDirectory() as d:
        wt, ro = d + "/worktree", d + "/repo"
        for cmd in git_cmds:
            rendered = (cmd.replace("{worktree}", wt)
                        .replace("{repo}", ro))
            assert rotate._producing_refusal(rendered) is None, rendered


def test_git_drifted_copy_goes_red_through_the_shared_reader(tmp_path):
    # hypothesis:l4-the-drifted-node-test-is-in-the-suite: the LIVE half above
    # reads the live node and CANNOT be pointed at a copy, so a DRIFTED
    # rotations.md that appends an off-allowlist first_turn line ships without
    # a red test. This falsifier copies the LIVE node to tmp, appends a
    # `git log -p -- .env` first_turn entry to the COPY, points the SHARED
    # reader (`_live_first_turn`, via `path=`) at the copy, and asserts the
    # SAME live-config judgement (rotate._producing_refusal on the rendered
    # cmd) that the LIVE half uses REFUSES it. If this test ever pointed the
    # reader at a different code path than the live test, the drift would be a
    # near miss — that is what this asserts against.
    from graph_core.persistence import frontmatter as _fm  # noqa: E402
    from tests.test_rotate_templates import _live_first_turn  # shared loader
    live = (Path(__file__).resolve().parents[3]
            / ".agi" / "nodes" / ".geometry" / "rotations.md")
    assert live.exists(), f"live rotations.md missing: {live}"
    nf = _fm.load_node_file(live)
    # append a DRIFTED entry to the director template's first_turn, in memory
    drifted = {"label": "drift", "cmd": "git log -p -- .env",
               "why": "deliberate drift inserted by the falsifier"}
    templates = nf.frontmatter.get("templates") or {}
    dir_ft = ((templates.get("director") or {}).get("startup") or {})
    dir_ft.setdefault("first_turn", []).append(drifted)
    copy = tmp_path / "rotations.md"
    _fm.save_node_file(copy, nf)  # writes the COPY, never the live node
    # the shared reader parses the copy and yields the drifted cmd
    cmds = [e.get("cmd") for e in _live_first_turn(copy)["director"]]
    assert "git log -p -- .env" in cmds, "drift did not reach the copy"
    # the drift stays in the COPY, never the live node
    live_after = _fm.load_node_file(live).frontmatter.get("templates")
    live_cmds = [e.get("cmd")
                 for e in (live_after.get("director") or {}).get(
                     "startup").get("first_turn")]
    assert "git log -p -- .env" not in live_cmds, "drift leaked into live node"
    # the SAME judgement as the live half: _producing_refusal on the rendered
    # cmd must REFUSE the drifted copy (go red), meaning a drifted live node
    # would now ship with a red suite test instead of a silent green.
    refusal = rotate._producing_refusal("git log -p -- .env")
    assert refusal is not None, "drifted copy passed the allowlist (near miss)"
    assert refusal.startswith("producer git "), refusal
    # and the copy genuinely exercises the shared loader, not a shadow: the
    # live half and this drift read through the SAME `_live_first_turn`
    assert callable(_live_first_turn) and callable(rotate._producing_refusal)


def test_git_benign_set_still_passes():
    for cmd in [
        "git status -sb",
        "git log --oneline -5",
        "git rev-parse --abbrev-ref HEAD",
        "git branch --show-current",
        "git diff --stat",
    ]:
        assert rotate._producing_refusal(cmd) is None, cmd


def test_git_benign_prefix_unit_cannot_bypass_later_unit():
    # hypothesis:l4-a-producing-git-stage-is-argument-restricted FIX: a one-
    # token BENIGN prefix unit used to `return` out of the WHOLE judge on the
    # first `;`-unit, so every LATER unit was never judged by the git branch:
    # `git status -sb; git log -p -- .env` -> None (WRONG). A benign git unit
    # must `continue` to the next unit/stage like every other producer branch.
    bad = [
        "git status -sb; git log -p -- .env",
        "git status -sb; git log --all -p -- .env",
        "git status -sb; git diff HEAD -- .env",
        "git status; git -c core.pager=less log",
    ]
    for cmd in bad:
        ref = rotate._producing_refusal(cmd)
        assert ref is not None, cmd
        assert ref.startswith("producer git "), cmd
    assert rotate._producing_refusal("git status -sb; git log -p -- .env") \
        == "producer git -p not on the allowlist"


def test_git_benign_prefix_unit_then_all_benign_passes():
    # same mechanics in the positive direction: every `;`-unit is judged, and
    # when ALL are benign the whole line still passes.
    assert rotate._producing_refusal("git status -sb; git log --oneline -5") is None
    assert rotate._producing_refusal("git status -sb; git branch --show-current") is None


def test_git_negC_value_subject_to_bad_token_scan():
    # hypothesis:l4-a-producing-git-stage-is-argument-restricted FIX: the
    # `-C <path>` VALUE was consumed by the skip loop with NO `$`/backtick/`~`
    # check, so `git -C $HOME status -sb` leaked the shell-expanded value into
    # the record while returning None. The value is now scanned like every
    # other token.
    assert rotate._producing_refusal("git -C $HOME status -sb") \
        == "producer git $HOME not on the allowlist"
    # backtick inside the -C value is REFUSED too, but one stage earlier by
    # _operator_refusal (unmodeled shell operator) — a refusal either way
    assert rotate._producing_refusal("git -C `pwd` status -sb") is not None
    assert rotate._producing_refusal("git -C ~ status -sb") \
        == "producer git ~ not on the allowlist"
    # a literal (non-shell) path stays benign
    assert rotate._producing_refusal("git -C /a/b status -sb") is None


def test_filter_pipe_fed_nonfilter_refused(tmp_path):
    # A `;`-unit's FIRST stage is judged as a PRODUCER; a PIPE-FED stage that
    # is NOT a modeled filter is refused by name — a first_turn pipeline has
    # no reason to pipe into a producer, which closes `| git log -p -- .env`
    # and `| git diff HEAD -- .env` WITHOUT touching the git allowlist.
    P = "python3 extensions/agi/bin/foo.py"
    assert rotate._producing_refusal(f"{P} | git log -p -- .env") == "filter git"
    assert rotate._producing_refusal(f"{P} | git diff HEAD -- .env") == "filter git"
    assert rotate._producing_refusal(f"{P} | python3 extensions/agi/bin/bar.py") == "filter python3"
    assert rotate._producing_refusal(f"{P} | ps aux") == "filter ps"


def test_filter_env_value_never_leaks_into_output(tmp_path, monkeypatch):
    # goal:g17.1 / hypothesis:l4-a-filter-stage-is-argument-restricted: an env
    # value set for the run must never appear in the rendered output or the
    # record. `| echo $ANY_SECRET` is REFUSED (echo positionals may not
    # contain `$`), so the value is never printed and never recorded.
    monkeypatch.setenv("SMOKE_SECRET_VAL", "plaintext-leak-xyz")
    P = "python3 extensions/agi/bin/foo.py"
    startup = {"first_turn": [
        {"label": "leak", "cmd": f"{P} | echo $SMOKE_SECRET_VAL"}]}
    res = rotate._run_first_turn_commands(startup, VALUES)
    assert res[0]["refused"], res
    assert "not on the allowlist" in res[0]["refused"], res
    block = rotate._compose_startup_output(res)
    assert "plaintext-leak-xyz" not in block
    assert "plaintext-leak-xyz" not in str(res)


def test_filter_benign_stdio_filters_still_run(tmp_path):
    # The allowed stdio-filter invocations all pass the allowlist parser:
    # the positive-control set from the build order plus the benign cluster /
    # value forms that used to pass and must STILL pass.
    P = "python3 extensions/agi/bin/foo.py"
    benign = [
        f"{P} | head -5",
        f"{P} | head -n 5",
        f"{P} | tail -3",
        f"{P} | grep -c x",
        f"{P} | grep -i x",
        f"{P} | grep -o abc",
        f"{P} | grep -w x",
        f"{P} | grep -v x",
        f"{P} | sed -n 1,40p",
        f"{P} | sed 's/x/y/g'",
        f"{P} | sed /foo/d",
        f"{P} | cut -c1-80",
        f"{P} | cut -f1",
        f"{P} | cut -d: -f1",
        f"{P} | sort",
        f"{P} | sort -f",
        f"{P} | sort -rn",
        f"{P} | sort -k2 -n",
        f"{P} | uniq",
        f"{P} | uniq -w 3",
        f"{P} | uniq -c",
        f"{P} | wc -l",
        f"{P} | tr a-z A-Z",
        f"{P} | tr -d ' '",
        f"{P} | cat -n",
        f"{P} | echo -n hi",
    ]
    for cmd in benign:
        assert rotate._producing_refusal(cmd) is None, cmd

def test_filter_forbidden_scans_every_token_env_never_leaks(
        monkeypatch, tmp_path):
    # hypothesis:l4-a-filter-stage-is-argument-restricted, FIX-ONLY #3
    # (L4.184): `_FILTER_FORBIDDEN` (`$` backtick `~`) is checked on EVERY
    # token of every filter stage — options, option values and positionals
    # alike — not just echo positionals. Without this, `_resolve_shell_vars`
    # expands `$VAR` from the whole environment at exec time even inside
    # single quotes, so these all passed the judge and leaked/mapped an env
    # value into the committed rotation record and the successor's STARTUP
    # OUTPUT. Hermetic: SECRET_PROBE is set, and assert the value appears in
    # NO result — each cmd is refused by name.
    secret = "sk-probe-value"
    monkeypatch.setenv("SECRET_PROBE", secret)
    P = "python3 extensions/agi/bin/foo.py"
    lethal = [
        f"{P} | sed 's/x/$SECRET_PROBE/'",
        f"{P} | grep '$SECRET_PROBE'",
        f"{P} | tr abcdef \"$SECRET_PROBE\"",
        f"{P} | echo $SECRET_PROBE",
    ]
    startup = {"first_turn": [{"label": f"leak{i}", "cmd": c}
                              for i, c in enumerate(lethal)]}
    res = rotate._run_first_turn_commands(startup, VALUES)
    for r, cmd in zip(res, lethal):
        assert r["refused"], (r)
        assert "not on startup.allow" in r["refused"], r
        assert "filter" in r["refused"], r
        assert secret not in r["cmd"], r        # record keeps the literal $VAR
        assert secret not in str(r), r          # nothing leaks anywhere in result
    # the same stages WITHOUT `$` still run (existing positive controls).
    for cmd in [f"{P} | echo -n hi", f"{P} | tr a-z A-Z"]:
        assert rotate._producing_refusal(cmd) is None, cmd


def test_filter_forbidden_sweeps_consumed_option_values(monkeypatch, tmp_path):
    # hypothesis:l4-a-filter-stage-is-argument-restricted, FIX-ONLY #4
    # (L4.184): `_FILTER_FORBIDDEN` must also run on the SEPARATE token a
    # value-taking option CONSUMES (the `skip = 2` branch). The top-of-loop
    # sweep never re-visits that token — `-e $SECRET_PROBE` advances past the
    # value and would otherwise let `_resolve_shell_vars` expand the env value
    # into the record. Hermetic: SECRET_PROBE set, every cmd refused by name,
    # the value absent from every result.
    secret = "sk-probe-value"
    monkeypatch.setenv("SECRET_PROBE", secret)
    P = "python3 extensions/agi/bin/foo.py"
    lethal = [
        f"{P} | grep -e $SECRET_PROBE",
        f"{P} | head -n $SECRET_PROBE",
        f"{P} | cut -d $SECRET_PROBE",
        f"{P} | sort -k $SECRET_PROBE",
        f"{P} | uniq -w $SECRET_PROBE",
        f"{P} | grep -ne $SECRET_PROBE",   # cluster `-ne`, value in next token
    ]
    startup = {"first_turn": [{"label": f"leak{i}", "cmd": c}
                              for i, c in enumerate(lethal)]}
    res = rotate._run_first_turn_commands(startup, VALUES)
    for r, cmd in zip(res, lethal):
        assert r["refused"], r
        assert "filter" in r["refused"], r
        assert "not on the allowlist" in r["refused"], r
        assert secret not in r["cmd"], r        # literal $VAR kept in record
        assert secret not in str(r), r          # nothing leaks in any result
    # positive controls with non-`$` values still run.
    benign = [
        f"{P} | grep -e x",
        f"{P} | head -n 5",
        f"{P} | cut -d: -f1",
        f"{P} | sort -k2 -n",
        f"{P} | uniq -w 3",
        f"{P} | sort -t: -k2",
    ]
    for cmd in benign:
        assert rotate._producing_refusal(cmd) is None, cmd


def test_filter_refusal_named_before_run(tmp_path):
    # the NAMED refusal surfaces on the actual run path too — the startup
    # output names the filter, nothing runs, no marker.
    marker = tmp_path / "pwned-MARKER"
    cmd = f"python3 extensions/agi/bin/foo.py | awk 'BEGIN{{system(\"touch {marker}\")}}'"
    res = rotate._run_first_turn_commands(
        {"first_turn": [{"label": "badfilt", "cmd": cmd}]}, VALUES)
    assert res[0]["refused"], res
    assert "filter awk" in res[0]["refused"], res
    assert "not on startup.allow" in res[0]["refused"], res
    assert not marker.exists(), res
    block = rotate._compose_startup_output(res)
    assert "[badfilt] REFUSED" in block


def test_fold_env_path_refused_even_when_allowlisted(tmp_path):
    # hypothesis FOLD: PATH/PYTHONPATH/LD_* are refused UNCONDITIONALLY, even
    # when a template puts them on startup.env_allow — a template author cannot
    # redirect binary lookup out of convenience.
    for cmd, name in [("PATH=/x python3 /wt/a.py", "PATH"),
                      ("PYTHONPATH=/x python3 /wt/a.py", "PYTHONPATH"),
                      ("LD_PRELOAD=/x.so python3 /wt/a.py", "LD_PRELOAD")]:
        startup = {"env_allow": ["PATH", "PYTHONPATH", "LD_PRELOAD"],
                   "first_turn": [{"label": "fold", "cmd": cmd}]}
        res = rotate._run_first_turn_commands(startup, VALUES)
        assert res[0]["refused"], res
        assert f"env prefix {name} refused unconditionally" in res[0]["refused"], \
            (cmd, res)


def test_git_fetch_off_the_allowlist():
    # hypothesis:l4-the-git-allowlist-has-no-network-write: `fetch` was on
    # _GIT_ALLOW and a bare `git fetch` returned None (accepted) — a NETWORK
    # WRITE (it advances remote-tracking refs) that no rotation template uses.
    # fetch is now NOT on the allowlist, so a git first stage naming it falls
    # through to a named refusal. The FALSIFIER is acceptance: any `git fetch`
    # accepted by the judge fails the claim.
    for cmd in ["git fetch", "git fetch origin", "git fetch upstream"]:
        ref = rotate._producing_refusal(cmd)
        assert ref is not None, cmd
        assert ref.startswith("producer git "), cmd
        assert "fetch" in ref, (cmd, ref)


def test_git_diff_requires_stat():
    # hypothesis:l4-the-git-allowlist-has-no-network-write: `diff` REQUIRES
    # `--stat`. A bare `git diff` would print the working-tree PATCH (file
    # contents) into the rotation record and the successor's STARTUP OUTPUT;
    # it is refused by name. `git diff HEAD` is refused (HEAD is not a diff
    # operand on the allowlist). `git diff --stat` still passes.
    for cmd in ["git diff", "git diff HEAD"]:
        ref = rotate._producing_refusal(cmd)
        assert ref is not None, cmd
        assert ref.startswith("producer git "), cmd
    assert "stat" in rotate._producing_refusal("git diff")
    # --stat present -> passes; the flag also STAYS allowed on log
    assert rotate._producing_refusal("git diff --stat") is None
    assert rotate._producing_refusal("git log --stat -5") is None


def test_git_readonly_subcmds_deleted():
    # hypothesis:l4-the-git-allowlist-has-no-network-write: _GIT_READONLY_SUBCMDS
    # had ONE remaining reference, its own definition — dead code whose
    # `fetch`-inclusion kept implying a bare fetch was a safe read. It is
    # deleted with no remaining reference (its name no longer binds).
    assert not hasattr(rotate, "_GIT_READONLY_SUBCMDS")


def test_probe_bare_separator_value_stays_one_stage(monkeypatch, tmp_path):
    # hypothesis:l4-a-bare-separator-env-value-cannot-inject-a-stage: an env
    # VALUE that is EXACTLY a shlex punctuation char (`|` / `;`) must ride as
    # ONE argv element through the stage split — it is DATA, not a separator.
    # The OLD resolver round-tripped the resolved command through shlex.join
    # then re-tokenized, which turned the value `'|'` back into a bare `|` and
    # SPLIT one stage into two (`echo x` | `cat ...`). The structural resolver
    # never re-parses: the boundary is fixed at tokenize time, so the value
    # cannot inject a stage. Judge and executor must agree on ONE unit / ONE
    # stage, and the executed argv must carry the char whole.
    monkeypatch.setenv("PROBE", "|")
    toks = rotate._resolve_shell_vars_per_token(
        "echo x $PROBE cat /etc/hostname")
    assert toks == [("arg", "echo"), ("arg", "x"), ("arg", "|"),
                    ("arg", "cat"), ("arg", "/etc/hostname")], toks
    # ONE unit, ONE stage; the `|` sits INSIDE the argv, not between stages
    assert rotate._startup_units(toks) == \
        [[["echo", "x", "|", "cat", "/etc/hostname"]]], \
        rotate._startup_units(toks)
    assert rotate._command_units(toks) == \
        [[(["echo", "x", "|", "cat", "/etc/hostname"], {})]], \
        rotate._command_units(toks)

    monkeypatch.setenv("PROBE", ";")
    toks = rotate._resolve_shell_vars_per_token(
        "echo x $PROBE touch /tmp/pwn")
    assert rotate._startup_units(toks) == \
        [[["echo", "x", ";", "touch", "/tmp/pwn"]]], \
        rotate._startup_units(toks)
    assert rotate._command_units(toks) == \
        [[(["echo", "x", ";", "touch", "/tmp/pwn"], {})]], \
        rotate._command_units(toks)


def test_probe_bare_separator_full_runner_one_argv(monkeypatch, tmp_path):
    # End-to-end, through _run_first_turn_commands with a real allowlisted
    # producer: the value exactly `|` (then `;`) is the WHOLE argv element. No
    # second stage is split out, the judge sees ONE allowed stage (no refusal),
    # and the mocked subprocess receives the char whole — nothing else runs.
    marker = tmp_path / "probe-MARKER"
    for val in ("|", ";"):
        monkeypatch.setenv("PROBE", val)
        captured = {}
        def _run(cmd, **kwargs):
            captured["argv"] = list(cmd)
            return _Proc(rc=0)
        monkeypatch.setattr(rotate.subprocess, "run", _run)
        cmd = "python3 {worktree}/extensions/list.py $PROBE"
        res = rotate._run_first_turn_commands(
            {"first_turn": [{"label": "probe", "cmd": cmd}]}, VALUES)
        assert "refused" not in res[0], (val, res)
        assert res[0]["rc"] == 0, (val, res)
        # ONE argv element holds the bare char; nothing injected
        assert captured["argv"] == ["python3", "/wt/extensions/list.py",
                                    val], (val, captured)
        assert not marker.exists(), (val, res)


def test_probe_judge_sees_one_stage_on_allowlisted_producer(monkeypatch):
    # the JUDGE on the resolved structure must see ONE stage — the whole point:
    # `_producing_refusal` consumed a two-stage split before, so `cat` was
    # judged as a pipe-fed stage; now the `|` is one element of one allowed
    # producer stage and the judge refuses nothing.
    monkeypatch.setenv("PROBE", "|")
    toks = rotate._resolve_shell_vars_per_token(
        "python3 {worktree}/extensions/list.py x $PROBE y")
    assert rotate._producing_refusal(toks) is None, \
        rotate._producing_refusal(toks)
    monkeypatch.setenv("PROBE", ";")
    toks = rotate._resolve_shell_vars_per_token(
        "python3 {worktree}/extensions/list.py x $PROBE y")
    assert rotate._producing_refusal(toks) is None, \
        rotate._producing_refusal(toks)


def test_resolve_shell_vars_whole_string_gone():
    # hypothesis:l4-a-bare-separator-env-value-cannot-inject-a-stage,
    # requirement 2: the whole-string `_resolve_shell_vars` had ZERO callers
    # and was DELETE-d; its name no longer binds in the module, so a future
    # reader cannot reintroduce a whole-string env round-trip.
    assert not hasattr(rotate, "_resolve_shell_vars")


# ---- _first_turn_values reads the PRIME row from the PUSHED season ref,
# ---- the way whois reads it, falling back to the working-tree row only
# ---- when the ref is unreachable and SAYING SO (hypothesis:l4-prime-key-is-
# ---- read-from-the-pushed-ref-and-whois-key-with-sig-resolves-the-sig-row-
# ---- by-pubkey). A deferred-key window (a pending key persisted when the
# ---- push FAILED) leaves the ROTATING worktree's prime row carrying a key
# ---- the pushed authority does not; a startup {prime_key} read from the
# ---- worktree then names a key the pushed row never carries and reads
# ---- NO-MATCH/RETIRED for a live Prime.
# ---------------------------------------------------------------------------

_WORKTREE_PRIME_ROW = {
    "name": "belam", "role": "prime_director", "tier": 3,
    "session_ref": "7902ac", "pubkey": "11112222deadbeef",
}
_PUSHED_PRIME_ROW = {
    "name": "belam", "role": "prime_director", "tier": 3,
    "session_ref": "", "pubkey": "aabbccdddeadbeef",  # deferred-key window: pushed row is the CURRENT one
}


def _prime_dual_source_rows(monkeypatch, tmp_path, work_row, push_row):
    """Write a worktree seats row + stub the PUSHED reader, so the
    pushed row and the worktree row carry DIFFERENT pubkeys (the falsifier
    fixture)."""
    import send as _send  # the SAME top-level module rotate's lazy import binds to
    rotate._prime_rows_fetch_clear()  # memo cleared, so it can never shadow this stub
    nodes = tmp_path / "nodes" / ".geometry"
    nodes.mkdir(parents=True, exist_ok=True)
    body = ("---\nid: config:seats\ntype: config\nseats:\n  - "
            + json.dumps(work_row) + "\n---\n")
    (nodes / "seats.md").write_text(body, encoding="utf-8")
    monkeypatch.setattr(_send, "_pushed_seats",
                        lambda root, ref, do_fetch: ([push_row], "abc123",
                                                     "origin/season/s2"))
    return _send


def test_first_turn_prime_key_reads_pushed_row_never_worktree(monkeypatch,
                                                              tmp_path):
    # FALSIFIER: worktree row and pushed row carry DIFFERENT pubkeys — the
    # resolved {prime_key} must be the PUSHED row's.
    _prime_dual_source_rows(monkeypatch, tmp_path, _WORKTREE_PRIME_ROW,
                             _PUSHED_PRIME_ROW)
    vals = rotate._first_turn_values(tmp_path, seat="sanctuary-director",
                                     gen=7, succ_name="sd-next")
    assert vals["prime_key"] == "aabbccdddeadbeef"   # pushed, never the worktree key
    assert vals["prime_key"] != "11112222deadbeef"
    assert vals["prime_seat"] == "belam"
    assert vals["prime_ref"] == ""                    # pushed prime's session_ref is empty here


def test_first_turn_prime_key_falls_back_to_worktree_with_note(monkeypatch,
                                                               tmp_path):
    # Pushed authority unreachable: fall back to the working-tree row
    # (never a silent worktree read, never an empty key).
    import send as _send
    rotate._prime_rows_fetch_clear()   # memo cleared, so the None stub is not shadowed
    nodes = tmp_path / "nodes" / ".geometry"
    nodes.mkdir(parents=True, exist_ok=True)
    body = ("---\nid: config:seats\ntype: config\nseats:\n  - "
            + json.dumps(_WORKTREE_PRIME_ROW) + "\n---\n")
    (nodes / "seats.md").write_text(body, encoding="utf-8")
    monkeypatch.setattr(_send, "_pushed_seats", lambda root, ref, do_fetch: None)
    vals = rotate._first_turn_values(tmp_path, seat="sanctuary-director",
                                     gen=7, succ_name="sd-next")
    assert vals["prime_key"] == "11112222deadbeef"


# ---- g15.25 (SL7.49): first seating gen follows the seat's ROW, not a      #
# ---- hard-coded gen 1 (hypothesis:l4-a-first-seating-on-an-existing-seat-  #
# ---- reports-the-rows-generation-not-a-hard-coded-gen-1)                  #


def _fs_seats_sheet(root, rows):
    """A config:seats node carrying the given rows (same shape the snapshot
    and test_rotate_g1517 build)."""
    nodes = root / "nodes" / ".geometry"
    nodes.mkdir(parents=True, exist_ok=True)
    (root / "sessions").mkdir(parents=True, exist_ok=True)
    body = "---\nid: config:seats\ntype: config\nseats:\n"
    for r in rows:
        body += "  - " + json.dumps(r) + "\n"
    body += "---\n"
    (nodes / "seats.md").write_text(body, encoding="utf-8")


def _fs_prime_pushed_patch(monkeypatch):
    """Stub the pushed-seats SEAM (`rotate._prime_pushed_seats`) so a
    first-seating build never performs a REAL `git fetch origin <name>`
    inside the suite (pre-fix: the four test_first_seating_* tests
    reached `_prime_pushed_seats` UNSTUBBED = 8 real fetch attempts per
    file run — the Prime's measured falsifier for hypothesis:l4-the-
    first-seating-tests-stub-the-pushed-seats-seam-and-a-none-miss-is-not-
    pinned-for-the-process). Clears the per-process memo first so an earlier
    test's memoized value can never shadow this stub. The canned row is
    irrelevant to the gen assertions; it only keeps `_prime_row_authority`
    from the worktree fallback."""
    rotate._prime_rows_fetch_clear()
    monkeypatch.setattr(rotate, "_prime_pushed_seats", lambda root, ref: (
        [{"role": "prime_director", "name": "sanctuary-director",
          "session_ref": "", "pubkey": "K" * 40}], "SHA", ref))


def _fs_director_first_turn(root, monkeypatch):
    """A config:rotations node whose director template declares a
    `startup.first_turn` probe that echoes `seat` and `gen` — the block a
    first seating composes, so `{gen}` substitution is observable. Also
    stubs the pushed-seats seam so no real git fetch is attempted."""
    _fs_prime_pushed_patch(monkeypatch)
    g = root / "nodes" / ".geometry"
    g.mkdir(parents=True, exist_ok=True)
    (root / "bin").mkdir(parents=True, exist_ok=True)
    (root / "bin" / "probe_fs.py").write_text(
        "import sys\nprint(','.join(sys.argv[1:]))\n", encoding="utf-8")
    (g / "rotations.md").write_text(
        "---\nid: config:rotations\ntype: config\ntemplates:\n"
        "  director: {brief_file: x.md, steps: [spawn], telemetry: [seat, ack],\n"
        "    startup: {first_turn: [{label: probe, "
        "cmd: \"python3 {repo}/bin/probe_fs.py {seat} gen={gen}\"}]}}\n"
        "---\n\nbody\n", encoding="utf-8")


def _fs_bootstrap(root, seat):
    p = rotate._sessions_dir(root) / "seats" / f"{seat}.bootstrap.json"
    return json.loads(p.read_text(encoding="utf-8"))


def test_first_seating_on_existing_seat_reports_row_gen_not_1(
        monkeypatch, tmp_path):
    """A RE-spawn onto a config:seats row that already carries
    `generation: 4` records generation 4 in the bootstrap record, substitutes
    `{gen}` = 4 into the composed STARTUP OUTPUT, and names `gen 4` in the
    turn-one ack override — never a hard-coded `gen 1` (the pre-fix defect:
    `_first_seating_run` built every gen-carrying value with `gen=1`)."""
    _fs_seats_sheet(tmp_path, [
        {"name": "re-seated", "role": "director", "model": "m",
         "effort": "max", "settings": "", "generation": 4},
    ])
    _fs_director_first_turn(tmp_path, monkeypatch)
    block, results = rotate._first_seating_run(
        tmp_path, seat="re-seated", role="director", succ_name="re-seated",
        dry_run=False)

    bs = _fs_bootstrap(tmp_path, "re-seated")
    # the bootstrap record generation agrees with the row, never a hard-coded 1.
    assert bs["generation"] == 4, \
        f"bootstrap generation must follow the row, got {bs['generation']}"
    # the turn-one ack override inside the record names gen 4, never gen 1.
    ack_fact = bs["telemetry"]["ack"]
    assert "gen 4" in ack_fact and "first-seating" in ack_fact, \
        f"ack fact must name the row gen and source first-seating: {ack_fact}"
    assert "gen 1" not in ack_fact, \
        f"no stale hard-coded gen 1 anywhere in the ack fact: {ack_fact}"
    # the {gen} placeholder inside the composed STARTUP OUTPUT is 4.
    assert "gen=4" in block and "gen=1" not in block, \
        f"composed block must substitute the row gen 4:\n{block}"
    assert results, "first seating should compose a non-empty first_turn"


def test_first_seating_ask_diff_ack_override_carries_row_gen(
        monkeypatch, tmp_path):
    """The ask-diff mode's ack override (answer `diff-requested`, source
    `first-seating`) also names the row generation, byte-identical source
    handling with the corrected gen."""
    _fs_seats_sheet(tmp_path, [
        {"name": "diff-seat", "role": "director", "generation": 7},
    ])
    _fs_director_first_turn(tmp_path, monkeypatch)
    _block, _results = rotate._first_seating_run(
        tmp_path, seat="diff-seat", role="director", succ_name="diff-seat",
        dry_run=False, ask_diff=True)
    bs = _fs_bootstrap(tmp_path, "diff-seat")
    assert bs["generation"] == 7
    ack_fact = bs["telemetry"]["ack"]
    assert "diff-requested" in ack_fact and "gen 7" in ack_fact, \
        f"ask-diff ack fact must name diff-requested and gen 7: {ack_fact}"
    assert "first-seating" in ack_fact, \
        "ask-diff source stays first-seating, never predecessor"
    assert "gen 1" not in ack_fact


def test_first_seating_new_seat_still_records_gen_1(monkeypatch,
                                                 tmp_path):
    """A BRAND-NEW seat (no row, or a gen-less row) is byte-identical to
    today: generation 1, source first-seating, `{gen}` = 1. Guards the
    regression that a gen-less first seating must not accidentally resolve to
    a row generation of 0 or refuse."""
    _fs_seats_sheet(tmp_path, [
        {"name": "fresh-seat", "role": "director", "model": "m"},  # no gen
    ])
    _fs_director_first_turn(tmp_path, monkeypatch)
    block, _results = rotate._first_seating_run(
        tmp_path, seat="fresh-seat", role="director", succ_name="fresh-seat",
        dry_run=False)
    bs = _fs_bootstrap(tmp_path, "fresh-seat")
    assert bs["generation"] == 1, \
        f"a brand-new seat stays at FIRST_SEATING_GEN=1, got {bs['generation']}"
    assert "gen 1" in bs["telemetry"]["ack"]
    assert "first-seating" in bs["telemetry"]["ack"]
    assert "gen=1" in block, f"fresh-seat block must substitute gen 1:\n{block}"


def test_first_seating_no_row_still_records_gen_1(monkeypatch,
                                               tmp_path):
    """A first seating with NO config:seats row at all (a throwaway seat)
    also stays at gen 1 — the `_seat_row_generation` reader returns None and
    the resolution falls back to FIRST_SEATING_GEN."""
    (tmp_path / "sessions").mkdir(parents=True, exist_ok=True)
    _fs_director_first_turn(tmp_path, monkeypatch)
    block, _results = rotate._first_seating_run(
        tmp_path, seat="throwaway", role="director", succ_name="throwaway",
        dry_run=False)
    bs = _fs_bootstrap(tmp_path, "throwaway")
    assert bs["generation"] == 1
    assert "gen 1" in bs["telemetry"]["ack"]
    assert "gen=1" in block


def test_first_seating_respawn_record_and_alert_carry_row_gen(
        monkeypatch, tmp_path):
    """A RE-spawn onto an EXISTING seat whose config:seats row carries
    `generation: 4` threads that ONE resolved generation to the seating
    RECORD (gen_after) AND the rotation-alert dm (which names `generation
    0 -> 4`), byte-for-byte with the bootstrap `_first_seating_run` already
    wrote — never a hard-coded gen-1 (hypothesis:l4-one-resolved-generation-
    for-the-seating-record-the-alert-and-the-bootstrap-on-a-re-spawn)."""
    _fs_seats_sheet(tmp_path, [
        {"name": "re-seated", "role": "director", "generation": 4},
    ])
    _fs_director_first_turn(tmp_path, monkeypatch)
    # the bootstrap writer resolves the row gen to 4.
    _block, _results = rotate._first_seating_run(
        tmp_path, seat="re-seated", role="director", succ_name="re-seated",
        dry_run=False)
    assert _fs_bootstrap(tmp_path, "re-seated")["generation"] == 4
    captured = {}
    monkeypatch.setattr(
        rotate, "_announce_rotation",
        lambda *a, **kw: captured.update(kw) or [])
    rotate._first_seating_announce(
        tmp_path, None, seat="re-seated", role="director", source="test",
        tmux_session="t", live_names=[])
    seating = captured["seating"]
    # the ONE record the alert shares reports gen_after 4, never a hard-coded 1.
    assert seating["gen_after"] == 4, \
        f"seating record gen_after must follow the row (4), got {seating['gen_after']}"
    assert seating["gen_before"] == 0
    # the same gen_after was threaded to the announce rotation call.
    assert captured["gen_after"] == 4, \
        f"_announce_rotation gen_after must be 4, got {captured['gen_after']}"
    # the ALERT dm names the same generation — `generation 0 -> 4`, never 1.
    text = rotate._compose_seating_announcement(
        seat="re-seated", ref=seating.get("ref") or "",
        pid=seating.get("pid"), in_flight="",
        generation=seating.get("gen_after") or 1, ask_diff=True)
    assert "generation 0 -> 4" in text, \
        f"alert dm must name generation 0 -> 4:\n{text}"
    assert "generation 0 -> 1" not in text
    assert "--gen 4" in text, f"alert ack line must name gen 4:\n{text}"


def test_first_seating_row_generation_zero_is_kept_as_zero(
        monkeypatch, tmp_path):
    """A row generation of 0 must be KEPT as 0 across the bootstrap, the
    seating record and the alert dm — never coerced to 1 by an `or
    FIRST_SEATING_GEN` (the pre-fix defect at `_first_seating_run`'s gen
    resolution). Only an absent / gen-less row falls back to gen 1."""
    _fs_seats_sheet(tmp_path, [
        {"name": "zero-seat", "role": "director", "generation": 0},
    ])
    _fs_director_first_turn(tmp_path, monkeypatch)
    block, _results = rotate._first_seating_run(
        tmp_path, seat="zero-seat", role="director", succ_name="zero-seat",
        dry_run=False)
    bs = _fs_bootstrap(tmp_path, "zero-seat")
    assert bs["generation"] == 0, \
        f"a row generation of 0 must stay 0, got {bs['generation']}"
    assert "gen 0" in bs["telemetry"]["ack"] and "gen 1" not in bs["telemetry"]["ack"]
    assert "gen=0" in block and "gen=1" not in block, \
        f"block must substitute a kept 0:\n{block}"
    captured = {}
    monkeypatch.setattr(
        rotate, "_announce_rotation",
        lambda *a, **kw: captured.update(kw) or [])
    rotate._first_seating_announce(
        tmp_path, None, seat="zero-seat", role="director", source="test",
        tmux_session="t", live_names=[])
    assert captured["seating"]["gen_after"] == 0, \
        f"seating record must keep a row gen 0, got {captured['seating']['gen_after']}"
    assert captured["gen_after"] == 0
    text = rotate._compose_seating_announcement(
        seat="zero-seat", in_flight="",
        generation=captured["gen_after"])
    assert "generation 0 -> 0" in text, \
        f"alert dm must name generation 0 -> 0:\n{text}"
    assert "generation 0 -> 1" not in text


def _run_real_announce(monkeypatch, tmp_path, seat, gen_after):
    """Drive the REAL `_announce_rotation` first-seating branch with a
    seating record carrying `gen_after`, capturing the alert dm text it
    ACTUALLY emits. Only the delivery/transport calls (`send.send`,
    `send.send_dm`, `send.wake`) are stubbed -- `_announce_rotation` and its
    composer run for real, so rotate.py:3676 (the `or FIRST_SEATING_GEN`
    coercion) is exercised. Returns the captured dm texts."""
    import send as _send  # the SAME top-level module rotate's lazy import binds to
    # a second live seat so _derive_receivers yields a (non-prime) recipient.
    _fs_seats_sheet(tmp_path, [
        {"name": seat, "role": "director", "generation": gen_after},
        {"name": "other-seat", "role": "director"},
    ])
    (tmp_path / "sessions").mkdir(parents=True, exist_ok=True)
    seating = {"seat": seat, "gen_before": 0, "gen_after": gen_after,
               "window_id": "w", "ref": "abc", "pid": 123,
               "session_id": "s1", "transcript_path": "t.json",
               "in_flight": ""}
    sent = []
    monkeypatch.setattr(_send, "send",
                        lambda root, recv, text, sender=None: sent.append(text))
    monkeypatch.setattr(_send, "send_dm",
                        lambda croot, s, recv, text, sender=None: sent.append(text))
    monkeypatch.setattr(_send, "wake", lambda root, recv: None)
    deliv = rotate._announce_rotation(
        root=tmp_path, croot=tmp_path, seat=seat, successor="x",
        gen_before=0, gen_after=gen_after, trigger="first-seating",
        handoff_path="", in_flight="", live_names=[seat, "other-seat"],
        seating=seating, ask_diff=True)
    assert deliv == ["other-seat"], \
        f"should deliver to other-seat, got {deliv}"
    assert sent, "the real alert composer must have produced dm text"
    return sent


def test_first_seating_alert_real_announce_keeps_gen0(monkeypatch, tmp_path):
    """The REAL `_announce_rotation` first-seating branch names a KEPT 0 in
    the alert dm -- `generation 0 -> 0`, never `or`-coerced to 1 (the exact
    falsifier at rotate.py:3676 `seating.get('gen_after') or
    FIRST_SEATING_GEN`). Delivery is stubbed; the composer is NOT."""
    sent = _run_real_announce(monkeypatch, tmp_path, "zero-seat", 0)
    for text in sent:
        assert "generation 0 -> 0" in text, \
            f"alert dm must keep gen 0 (was or-coerced to 1):\n{text}"
        assert "generation 0 -> 1" not in text, \
            f"no or-coercion to 1 in the alert dm:\n{text}"
        assert "--gen 0" in text, f"alert ack line must name gen 0:\n{text}"


def test_first_seating_alert_real_announce_keeps_gen4(monkeypatch, tmp_path):
    """Same real-path check for a gen-4 row: the alert dm names 0 -> 4."""
    sent = _run_real_announce(monkeypatch, tmp_path, "re-seated", 4)
    for text in sent:
        assert "generation 0 -> 4" in text, \
            f"alert dm must name gen 4:\n{text}"
        assert "--gen 4" in text, f"alert ack line must name gen 4:\n{text}"


def test_prime_pushed_seats_fetches_once_per_process_across_values_builds(
        monkeypatch, tmp_path):
    # FALSIFIER for hypothesis:l4-rotate-self-fetches-the-pushed-season-ref-
    # once-per-run-through-a-seam-and-no-suite-test-reaches-origin: a rotate-
    # self builds first_turn values at FIVE sites (first seating, a second
    # compose, driven startup, startup, after-join), each routing through
    # `_prime_pushed_seats`, which memoizes on (str(root), ref). Build the
    # values map repeatedly — the multi-site shape — and assert the
    # underlying `send._pushed_seats` (the REAL fetch) ran exactly ONCE.
    import send as _send  # the SAME top-level module rotate's lazy import binds to
    fetch_calls = {"n": 0}

    def fake_pushed(root, ref, do_fetch):
        fetch_calls["n"] += 1
        assert do_fetch is True
        return ([{"role": "prime_director", "name": "sanctuary-director",
                  "session_ref": "", "pubkey": "K" * 40}], "SHA", ref)

    monkeypatch.setattr(_send, "_pushed_seats", fake_pushed)
    rotate._prime_rows_fetch_clear()
    try:
        for gen in range(1, 6):
            vals = rotate._first_turn_values(
                tmp_path, seat="sanctuary-director", gen=gen,
                succ_name="sd-next")
            assert vals["prime_key"] == "K" * 40
        assert fetch_calls["n"] == 1, (
            f"pushed-seats fetch ran {fetch_calls['n']} times across a "
            f"five-site values build; expected exactly once")
    finally:
        rotate._prime_rows_fetch_clear()

def test_prime_pushed_seats_none_miss_retries_once_then_pins(monkeypatch,
                                                             tmp_path):
    # hypothesis:l4-the-first-seating-tests-stub-the-pushed-seats-seam-and-
    # a-none-miss-is-not-pinned-for-the-process: a None result (pushed ref
    # unreachable) is NOT memoized on its first miss — the next build RETRIES
    # the real fetch once — so one transient fetch failure on the FIRST build
    # never pins the worktree fallback for every later build in the process.
    # A SECOND consecutive miss for the same (root, ref) pins None (a
    # genuinely-dead pushed ref is fetched at most twice per process, not on
    # every one of the five values-build sites).
    import send as _send  # the SAME top-level module rotate's lazy import binds to
    fetch_calls = {"n": 0}
    # a pushed ref that always yields None (unreachable)
    def missing(root, ref, do_fetch):
        fetch_calls["n"] += 1
        return None
    monkeypatch.setattr(_send, "_pushed_seats", missing)
    rotate._prime_rows_fetch_clear()
    try:
        # first miss: not memoized.
        assert rotate._prime_pushed_seats(tmp_path, "refX") is None
        assert fetch_calls["n"] == 1
        # second build RETRIES (the first miss was not pinned).
        assert rotate._prime_pushed_seats(tmp_path, "refX") is None
        assert fetch_calls["n"] == 2
        # third build: the second consecutive miss IS pinned.
        assert rotate._prime_pushed_seats(tmp_path, "refX") is None
        assert fetch_calls["n"] == 2, (
            f"a pinned None miss must not re-fetch, got {fetch_calls['n']} "
            f"calls after the second miss; expected 2")
    finally:
        rotate._prime_rows_fetch_clear()


def test_first_seating_family_reaches_no_origin_fetch(monkeypatch, tmp_path):
    # FALSIFIER for the same hypothesis, backstopped on the PRIME-seam side:
    # with the `_fs_*` fixture stubbing `rotate._prime_pushed_seats`, a real
    # `send._pushed_seats` (the origin fetch) must be reached ZERO times by
    # the four seat shapes. The Prime measured 8 real `git fetch origin`
    # attempts across this family pre-fix; this test pins the count at 0.
    import send as _send  # the SAME top-level module rotate's lazy import binds to
    seen = {"n": 0}
    def counting(root, ref, do_fetch):
        seen["n"] += 1
        raise AssertionError(
            f"first seating reached the real origin fetch ({ref}); the "
            f"_fs_* fixture must stub rotate._prime_pushed_seats")
    monkeypatch.setattr(_send, "_pushed_seats", counting)
    rotate._prime_rows_fetch_clear()
    try:
        for seat, gen in (("re-seated", 4), ("fresh-seat", 1),
                          ("throwaway", 1)):
            _fs_seats_sheet(tmp_path, [
                {"name": seat, "role": "director", "generation": gen},
            ])
            (tmp_path / "sessions").mkdir(parents=True, exist_ok=True)
            _fs_director_first_turn(tmp_path, monkeypatch)
            block, results = rotate._first_seating_run(
                tmp_path, seat=seat, role="director", succ_name=seat,
                dry_run=False)
            assert block and results
    finally:
        rotate._prime_rows_fetch_clear()
    assert seen["n"] == 0, (
        f"first-seating family reached the origin fetch {seen['n']} times; "
        f"expected 0 with the seam stubbed")


# ── g15.25 SL7.71 — the 'meter' telemetry key resolves in the bootstrap ────


def _cc_transcript(path, input_tokens=1000, cache_read=0, cache_creation=0):
    """A one-assistant-turn Claude Code transcript JSONL with a usage block."""
    path.write_text(json.dumps({
        "message": {
            "role": "assistant",
            "usage": {
                "input_tokens": input_tokens,
                "cache_read_input_tokens": cache_read,
                "cache_creation_input_tokens": cache_creation,
                "output_tokens": 50,
            },
        },
    }) + "\n", encoding="utf-8")
    return path


def _meter_pin(root, seat, transcript, gen=1):
    sess = root / "sessions"
    sess.mkdir(parents=True, exist_ok=True)
    p = sess / f"{seat}{rotate.METER_PIN_EXT}"
    p.write_text(f"{gen}\t{transcript}\n", encoding="utf-8")
    return p


def test_meter_fact_measured_fraction_exactly_as_meter_prints(tmp_path):
    """(a) the pinned successor transcript that carries assistant usage ->
    the measured fraction EXACTLY as rotate.py meter prints it — `0.NNNN
    (used/tokens window) source=... threshold=...` — never an estimate, never
    a bare number (goal:g15.25 SL7.71 falsifier: 'a transcript with usage
    prints an estimate')."""
    tr = tmp_path / "sessions"
    tr.mkdir(parents=True, exist_ok=True)
    tx = _cc_transcript(tr / "succ.jsonl", input_tokens=1000)
    _meter_pin(tmp_path, "mseat", str(tx))
    val, reason = rotate._derive_bootstrap_fact(
        "meter", root=tmp_path, seat="mseat", seat_row={}, commit="abc1234")
    assert reason is None
    assert val.startswith("0.0010 (1000/1000000 tokens) ")
    assert "source=claude-code transcript (pinned)" in val
    assert "threshold=0.47" in val
    assert "est." not in val


def test_meter_fact_estimate_from_composed_first_input_bytes(tmp_path):
    """(b) a pinned transcript with NO assistant usage yet, but the caller
    supplied the successor's composed first-input byte count -> `est. N
    tokens = first input <bytes>/4 (head + brief + STARTUP)` — LABELLED, never
    a bare number (P6), never a confident wrong number."""
    # transcript exists but carries only a user line: no assistant usage.
    tr = tmp_path / "sessions"
    tr.mkdir(parents=True, exist_ok=True)
    (tr / "succ.jsonl").write_text(
        json.dumps({"message": {"role": "user", "content": "hello"}}) + "\n",
        encoding="utf-8")
    _meter_pin(tmp_path, "mseat", str(tr / "succ.jsonl"))
    val, reason = rotate._derive_bootstrap_fact(
        "meter", root=tmp_path, seat="mseat", seat_row={}, commit="abc1234",
        meter_first_input_bytes=4000)
    assert reason is None
    assert val == ("est. 1000 tokens = first input 4000 bytes/4 "
                   "(head + brief + STARTUP)")
    assert val.startswith("est.")


def test_meter_fact_join_only_pending_then_filled(tmp_path):
    """(c) pre-spawn neither a measure nor the composed bytes -> the key is
    join-only: the pre-spawn record writes `pending: resolved after join`
    (never blank, never SKIPPED), and _fill_bootstrap_join_facts fills the
    measured fraction once the successor's transcript carries its first
    assistant turn — the pending marker is never left behind after the join."""
    # pre-spawn write: meter is in BOOTSTRAP_JOIN_ONLY_FACTS, so it lands
    # `pending: resolved after join`, never `SKIPPED: no handover derivation`.
    _write = rotate._write_bootstrap(
        tmp_path, seat="mseat", generation=1,
        telemetry=["ack", "meter"], verification=None,
        join_pending=set(rotate.BOOTSTRAP_JOIN_ONLY_FACTS))
    doc = json.loads(Path(_write).read_text(encoding="utf-8"))
    assert doc["telemetry"]["meter"] == "pending: resolved after join"
    # after the join the successor has answered: a seat pin names a transcript
    # that now carries assistant usage; the fill must resolve meter in place.
    tr = tmp_path / "sessions"
    tx = _cc_transcript(tr / "succ.jsonl", input_tokens=2000)
    _meter_pin(tmp_path, "mseat", str(tx))
    ok = rotate._fill_bootstrap_join_facts(
        tmp_path, seat="mseat", live_model="claude-opus-5",
        refusal_fallback="fallback", join_poll_secs=10)
    assert ok
    doc2 = json.loads(Path(_write).read_text(encoding="utf-8"))
    assert doc2["telemetry"]["meter"].startswith("0.0020 (2000/1000000 tokens)")
    assert not doc2["telemetry"]["meter"].startswith("pending:")
    assert doc2["telemetry"]["meter"] != "SKIPPED: no handover derivation for meter"
