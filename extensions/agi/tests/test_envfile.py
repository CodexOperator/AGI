"""Tests for bin/envfile.py — the credential geometry reader (goal:g1.8).

The interesting assertions are the ones about what this module *refuses* to do:
it never lowers the forbidden-key floor a project's own node might try to drop,
and it never prints a value. Those two are the whole safety story; the path
resolution is ordinary and is tested mostly to pin the `<source_root>` shape,
which is what stops a declared path from encoding one machine's layout.
"""
from __future__ import annotations

import json
import os
import sys
import textwrap
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parents[1] / "bin"
sys.path.insert(0, str(BIN))

import envfile as agi_secrets  # noqa: E402


# --- fixtures --------------------------------------------------------------


def make_project(repo: Path) -> Path:
    """A goal:g11 project: `<repo>/.agi/` beside the source it describes."""
    graph = repo / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    (graph / "config.json").write_text(json.dumps({"metric_primary": "outcome_coverage"}))
    return graph


def write_node(graph: Path, body: str) -> Path:
    path = graph / "nodes" / ".geometry" / "secrets.md"
    path.write_text(textwrap.dedent(body).lstrip())
    return path


DEFAULT_NODE = """
    ---
    id: "config:secrets"
    type: config
    status: active
    mint_id: 0123456789abcdef0123456789abcdef
    title: "test secrets node"
    locations:
      env_file:
        path: "<source_root>/.env"
      env_template:
        path: "<source_root>/.env.example"
    required_keys:
      - OPENROUTER_API_KEY
    optional_keys:
      - OPENAI_API_KEY
    forbidden_keys:
      - SOMETHING_LOCAL
    ---

    body
    """


def write_env(repo: Path, text: str, mode: int = 0o600) -> Path:
    path = repo / ".env"
    path.write_text(textwrap.dedent(text).lstrip())
    path.chmod(mode)
    return path


# --- resolution ------------------------------------------------------------


def test_resolves_paths_from_the_node(tmp_path):
    graph = make_project(tmp_path)
    write_node(graph, DEFAULT_NODE)
    res = agi_secrets.resolve(tmp_path)
    assert res.from_node is True
    assert res.env_file == tmp_path / ".env"
    assert res.template == tmp_path / ".env.example"


def test_source_root_placeholder_is_the_repo_not_the_graph_dir(tmp_path):
    """`<source_root>` under the g11 layout is the repo enclosing `.agi/`.

    Pinned because getting this wrong puts the secret INSIDE the graph
    directory, one `.gitignore` slip away from being committed.
    """
    graph = make_project(tmp_path)
    write_node(graph, DEFAULT_NODE)
    res = agi_secrets.resolve(tmp_path)
    assert res.env_file.parent == tmp_path
    assert res.env_file.parent != graph


def test_falls_back_when_no_node_and_says_so(tmp_path):
    """A project with no secrets node still resolves — but reports which it got."""
    make_project(tmp_path)
    res = agi_secrets.resolve(tmp_path)
    assert res.from_node is False
    assert res.env_file == tmp_path / ".env"
    _problems, notes = agi_secrets.check(res)
    assert any("no secrets node" in n for n in notes)


def test_unresolvable_placeholder_raises(tmp_path):
    graph = make_project(tmp_path)
    write_node(graph, DEFAULT_NODE.replace("<source_root>/.env\"", "<nowhere>/.env\""))
    with pytest.raises(agi_secrets.SecretsError, match="unresolved placeholder"):
        agi_secrets.resolve(tmp_path)


def test_no_project_raises(tmp_path):
    with pytest.raises(agi_secrets.SecretsError, match="no agi project"):
        agi_secrets.resolve(tmp_path / "nowhere")


# --- the forbidden-key floor -----------------------------------------------


def test_node_can_extend_the_forbidden_floor(tmp_path):
    graph = make_project(tmp_path)
    write_node(graph, DEFAULT_NODE)
    res = agi_secrets.resolve(tmp_path)
    assert "SOMETHING_LOCAL" in res.forbidden_keys


def test_node_cannot_lower_the_forbidden_floor(tmp_path):
    """A project that declares an empty list still gets the ANTHROPIC_* floor.

    This is the assertion that matters: `dispatch.py` scrubs those names so pi
    subagents cannot bill the Claude Code subscription, and an env file is read
    below that scrub. A project must not be able to opt out by editing its own
    node.
    """
    graph = make_project(tmp_path)
    write_node(graph, DEFAULT_NODE.replace("forbidden_keys:\n  - SOMETHING_LOCAL",
                                           "forbidden_keys: []"))
    res = agi_secrets.resolve(tmp_path)
    for key in agi_secrets.ALWAYS_FORBIDDEN:
        assert key in res.forbidden_keys


def test_forbidden_key_present_is_a_problem(tmp_path):
    graph = make_project(tmp_path)
    write_node(graph, DEFAULT_NODE)
    write_env(tmp_path, """
        OPENROUTER_API_KEY=sk-or-v1-test
        ANTHROPIC_API_KEY=sk-ant-test
        """)
    res = agi_secrets.resolve(tmp_path)
    problems, _notes = agi_secrets.check(res)
    assert any("ANTHROPIC_API_KEY" in p for p in problems)


# --- checking --------------------------------------------------------------


def test_missing_env_file_names_the_required_keys(tmp_path):
    graph = make_project(tmp_path)
    write_node(graph, DEFAULT_NODE)
    res = agi_secrets.resolve(tmp_path)
    problems, _notes = agi_secrets.check(res)
    assert len(problems) == 1
    assert "OPENROUTER_API_KEY" in problems[0]


def test_empty_required_key_is_a_problem(tmp_path):
    graph = make_project(tmp_path)
    write_node(graph, DEFAULT_NODE)
    write_env(tmp_path, "OPENROUTER_API_KEY=\n")
    res = agi_secrets.resolve(tmp_path)
    problems, _notes = agi_secrets.check(res)
    assert any("missing or empty" in p for p in problems)


def test_satisfied_env_file_has_no_problems(tmp_path):
    graph = make_project(tmp_path)
    write_node(graph, DEFAULT_NODE)
    write_env(tmp_path, "OPENROUTER_API_KEY=sk-or-v1-test\n")
    res = agi_secrets.resolve(tmp_path)
    problems, notes = agi_secrets.check(res)
    assert problems == []
    assert not any("mode" in n for n in notes)


def test_loose_mode_is_a_note_not_a_problem(tmp_path):
    """A wrong mode is a hazard the operator can see; refusing to run is not
    this tool's call, so it warns and continues."""
    graph = make_project(tmp_path)
    write_node(graph, DEFAULT_NODE)
    write_env(tmp_path, "OPENROUTER_API_KEY=sk-or-v1-test\n", mode=0o644)
    res = agi_secrets.resolve(tmp_path)
    problems, notes = agi_secrets.check(res)
    assert problems == []
    assert any("mode 644" in n for n in notes)


# --- parsing ---------------------------------------------------------------


@pytest.mark.parametrize("line,key,value", [
    ("FOO=bar", "FOO", "bar"),
    ("export FOO=bar", "FOO", "bar"),
    ('FOO="bar"', "FOO", "bar"),
    ("FOO='bar'", "FOO", "bar"),
    ("FOO=sk-or-v1-a=b=c", "FOO", "sk-or-v1-a=b=c"),
    ("  FOO = bar  ", "FOO", "bar"),
])
def test_read_env_line_shapes(tmp_path, line, key, value):
    path = write_env(tmp_path, line + "\n")
    assert agi_secrets.read_env(path)[key] == value


def test_read_env_skips_comments_and_blanks(tmp_path):
    path = write_env(tmp_path, """
        # a comment

        FOO=bar
        not-an-assignment
        """)
    assert agi_secrets.read_env(path) == {"FOO": "bar"}


def test_read_env_missing_file_is_empty_not_an_error(tmp_path):
    assert agi_secrets.read_env(tmp_path / "nope") == {}


# --- cli -------------------------------------------------------------------


def test_cli_what_env_file(tmp_path, capsys):
    graph = make_project(tmp_path)
    write_node(graph, DEFAULT_NODE)
    rc = agi_secrets.main([str(tmp_path), "--what", "env-file"])
    assert rc == 0
    assert capsys.readouterr().out.strip() == str(tmp_path / ".env")


def test_cli_check_exits_nonzero_on_a_problem(tmp_path):
    graph = make_project(tmp_path)
    write_node(graph, DEFAULT_NODE)
    assert agi_secrets.main([str(tmp_path), "--check"]) == 1


def test_cli_without_check_reports_but_exits_zero(tmp_path):
    """`driver.sh` calls the plain form every pass: it must report a missing
    key without failing the run, or a first `--smoke` on a fresh clone dies
    before it can tell you what is wrong."""
    graph = make_project(tmp_path)
    write_node(graph, DEFAULT_NODE)
    assert agi_secrets.main([str(tmp_path)]) == 0


def test_cli_never_prints_a_value(tmp_path, capsys):
    graph = make_project(tmp_path)
    write_node(graph, DEFAULT_NODE)
    write_env(tmp_path, """
        OPENROUTER_API_KEY=sk-or-v1-SUPERSECRET
        ANTHROPIC_API_KEY=sk-ant-ALSOSECRET
        """)
    agi_secrets.main([str(tmp_path), "--check"])
    agi_secrets.main([str(tmp_path), "--json"])
    captured = capsys.readouterr()
    assert "SUPERSECRET" not in captured.out + captured.err
    assert "ALSOSECRET" not in captured.out + captured.err


# ---------------------------------------------------------------------------
# goal:g1.11 -- an optional key must be verifiable without being printed.
#
# `OPENROUTER_PROVISIONING_KEY` is optional by design, so `--check` said
# nothing about it and there was no way to confirm a write short of reading
# the file -- which puts a secret on a terminal to answer "did it land?".
# ---------------------------------------------------------------------------


def test_an_optional_key_that_is_set_is_reported_present_but_never_by_value(tmp_path):
    graph = make_project(tmp_path)
    write_node(graph, DEFAULT_NODE)
    write_env(tmp_path, """
        OPENROUTER_API_KEY=sk-or-v1-test
        OPENAI_API_KEY=sk-a-very-secret-value
        """)
    res = agi_secrets.resolve(tmp_path)
    problems, notes = agi_secrets.check(res)
    blob = "\n".join(problems + notes)

    assert not problems, "an optional key can never be a problem either way"
    assert "OPENAI_API_KEY is set" in blob
    assert str(len("sk-a-very-secret-value")) in blob, "the length is the proof"
    assert "sk-a-very-secret-value" not in blob, "the VALUE must never be printed"


# --- credential validity (hypothesis:l4-a-check-that-answers-a-
# question-it-is-not-asking, ITEM 1) --------------------------------------
#
# `--check` used to assert presence and print "ok" for a revoked key. These
# tests assert the NEW half: a 401 makes the check FAIL and say the key is
# present but NOT USABLE (both halves); a network error stays fail-open and is
# reported as UNKNOWN, never dead; a live key still passes. The verifier is
# stubbed at module level so no test touches the network; a real-tree probe is
# run manually against the live box and recorded on the experiment node.


def _stub_verify(status, detail):
    import envfile as _e

    def _fake(key):
        return (status, detail)

    return _fake


def test_verify_401_makes_check_fail_and_names_present_but_not_usable(tmp_path, monkeypatch):
    """Falsifier (a): a dead key must FAIL the validating check and say BOTH
    that it is present AND that it is not usable — a message that only says
    'failed' loses the distinction the round exists to create."""
    import envfile as _e
    graph = make_project(tmp_path)
    write_node(graph, DEFAULT_NODE)
    write_env(tmp_path, "OPENROUTER_API_KEY=sk-or-v1-revoked\n")
    monkeypatch.setattr(_e, "_verify_provider_key", _stub_verify("dead", "provider rejected it (HTTP 401)"))
    res = _e.resolve(tmp_path)
    problems, notes = _e.check(res, verify=True)
    assert any("present" in p and "NOT USABLE" in p for p in problems), problems
    assert any("401" in p for p in problems), problems
    assert not problems or "sk-or-v1-revoked" not in "\n".join(problems), "never a value"


def test_verify_network_error_is_unknown_and_fail_open(tmp_path, monkeypatch):
    """Falsifier (b)+(c) of ITEM 1: an unreachable API is evidence of nothing.
    It must pass fail-open and be reported as UNKNOWN, never as dead — two
    different facts, two different behaviours."""
    import envfile as _e
    graph = make_project(tmp_path)
    write_node(graph, DEFAULT_NODE)
    write_env(tmp_path, "OPENROUTER_API_KEY=sk-or-v1-liveish\n")
    monkeypatch.setattr(_e, "_verify_provider_key", _stub_verify("unknown", "could not reach the provider (URLError)"))
    res = _e.resolve(tmp_path)
    problems, notes = _e.check(res, verify=True)
    assert problems == [], "a network error must never be a dead-key problem"
    assert any("OPENROUTER_API_KEY" in n and "unknown" in n.lower() or "not confirmed usable" in n for n in notes), notes
    assert not any("dead" in n or "NOT USABLE" in n for n in notes), notes


def test_verify_live_key_still_passes(tmp_path, monkeypatch):
    """Falsifier (c): a healthy key must still pass exactly as today — no new
    problem, only a confirming note."""
    import envfile as _e
    graph = make_project(tmp_path)
    write_node(graph, DEFAULT_NODE)
    write_env(tmp_path, "OPENROUTER_API_KEY=sk-or-v1-good\n")
    monkeypatch.setattr(_e, "_verify_provider_key", _stub_verify("valid", "provider accepted it (HTTP 200)"))
    res = _e.resolve(tmp_path)
    problems, notes = _e.check(res, verify=True)
    assert problems == []
    assert any("OPENROUTER_API_KEY" in n and "validated" in n for n in notes), notes


def test_verify_off_by_default_so_plain_check_stays_offline(tmp_path, monkeypatch):
    """The plain `check(res)` / driver path must NOT fire the authenticated
    call — `driver.sh` runs it every pass and stays offline."""
    import envfile as _e
    graph = make_project(tmp_path)
    write_node(graph, DEFAULT_NODE)
    write_env(tmp_path, "OPENROUTER_API_KEY=sk-or-v1-whatever\n")
    called = {"n": 0}
    def _boom(*a, **k):
        called["n"] += 1
        raise AssertionError("verify must not run with verify=False")
    monkeypatch.setattr(_e, "_verify_provider_key", _boom)
    res = _e.resolve(tmp_path)
    problems, notes = _e.check(res, verify=False)
    assert called["n"] == 0
    assert problems == []


def test_provider_for_unknown_prefix_is_unknown_not_valid(tmp_path, monkeypatch):
    """A key whose shape we cannot recognize must be reported UNKNOWN, never
    accepted as valid and never condemned as dead — we have no verdict for it."""
    import envfile as _e
    # No network: _provider_for is pure prefix logic; stub _verify_openrouter
    # to fail loudly so this proves the prefix path short-circuits.
    def _boom(key):
        raise AssertionError("must not call a provider verifier for an unknown prefix")
    original = _e._VERIFIERS["openrouter"]
    _e._VERIFIERS["openrouter"] = _boom
    try:
        status, detail = _e._verify_provider_key("ghp_something")
        assert status == "unknown", status
        assert "no verifier" in detail
    finally:
        _e._VERIFIERS["openrouter"] = original


def test_cli_check_with_a_dead_key_fails_and_never_prints_a_value(tmp_path, monkeypatch, capsys):
    """The CLI `--check` path routes verify=True: a dead key fails the audit
    AND the value never reaches the terminal."""
    import envfile as _e
    graph = make_project(tmp_path)
    write_node(graph, DEFAULT_NODE)
    write_env(tmp_path, "OPENROUTER_API_KEY=sk-or-v1-REVOKEDSECRET\n")
    monkeypatch.setattr(_e, "_verify_provider_key", _stub_verify("dead", "provider rejected it (HTTP 401)"))
    rc = _e.main([str(tmp_path), "--check"])
    out, err = capsys.readouterr()
    assert rc == 1, "a dead key must fail --check"
    assert "REVOKEDSECRET" not in out + err, "never a value on the terminal"


def test_an_optional_key_that_is_absent_says_so_and_is_not_a_failure(tmp_path):
    graph = make_project(tmp_path)
    write_node(graph, DEFAULT_NODE)
    write_env(tmp_path, """
        OPENROUTER_API_KEY=sk-or-v1-test
        """)
    res = agi_secrets.resolve(tmp_path)
    problems, notes = agi_secrets.check(res)
    assert not problems
    assert any("OPENAI_API_KEY is not set" in n for n in notes)


# --------------------------------------------------------------------------
# env-get.sh — pi's auth.json indirection (goal:g1.8, goal:g1.11)
#
# This script had NO tests, which is why the defect below shipped and survived
# an entire session of work built on top of it.
# --------------------------------------------------------------------------

ENV_GET = (Path(__file__).resolve().parent.parent / "bin" / "env-get.sh")


def _run_env_get(var, env_file, extra_env=None):
    import os
    import subprocess
    env = dict(os.environ)
    # Start from a clean slate for the variable under test, so a value leaking
    # in from the developer's own shell cannot make this pass.
    env.pop(var, None)
    env.update(extra_env or {})
    return subprocess.run([str(ENV_GET), var, str(env_file)],
                          capture_output=True, text=True, env=env, timeout=60)


def test_env_get_falls_back_to_the_file_when_nothing_is_injected(tmp_path):
    envf = tmp_path / ".env"
    envf.write_text("OPENROUTER_API_KEY=sk-from-the-file\n")
    proc = _run_env_get("OPENROUTER_API_KEY", envf)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout == "sk-from-the-file", "no trailing newline, ever"


def test_env_get_prefers_an_injected_value_over_the_file(tmp_path):
    """🔴 goal:g1.11's whole mechanism, and it was broken end to end.

    `dispatch.py` mints a capped, expiring key per spawn and injects it into
    the child's environment. pi does not read that variable — its auth.json
    shells out to `env-get.sh`, which read `.env` unconditionally. So every
    kid authenticated with the shared long-lived key while its own minted key
    sat unused: measured in the first live run as two minted keys at
    `usage=0` with all spend on the shared key.

    Proved against a stub, the mechanism looked fine — a stub that dumps its
    environment shows the injection happened. It cannot show that the harness
    *reads* what was injected.
    """
    envf = tmp_path / ".env"
    envf.write_text("OPENROUTER_API_KEY=sk-shared-long-lived\n")
    proc = _run_env_get("OPENROUTER_API_KEY", envf,
                        {"OPENROUTER_API_KEY": "sk-minted-for-this-spawn"})
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout == "sk-minted-for-this-spawn", (
        "the injected per-spawn key must win over the shared file value, or "
        "per-spawn credentials are decorative")


def test_env_get_ignores_an_empty_injected_value_and_uses_the_file(tmp_path):
    """Empty is not a credential. An exported-but-blank var must not shadow."""
    envf = tmp_path / ".env"
    envf.write_text("OPENROUTER_API_KEY=sk-from-the-file\n")
    proc = _run_env_get("OPENROUTER_API_KEY", envf, {"OPENROUTER_API_KEY": ""})
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout == "sk-from-the-file"


def test_env_get_still_fails_loudly_when_the_value_is_nowhere(tmp_path):
    envf = tmp_path / ".env"
    envf.write_text("SOMETHING_ELSE=1\n")
    proc = _run_env_get("OPENROUTER_API_KEY", envf)
    assert proc.returncode != 0
    assert "OPENROUTER_API_KEY" in proc.stderr


# --- linked worktrees share the main checkout's .env (l3w4) ----------------
# `hypothesis:l3w4-branch-shared-state`: `.env` is gitignored, so a `--branch`
# worktree has none of its own; a kid whose cwd is `.agi/worktrees/<agent>`
# must read the MAIN checkout's `.env`, resolved through `git_common_root`,
# or every key lookup is silently unrunnable under `--branch`.


def _worktree_repo(tmp_path: Path) -> tuple[Path, Path, Path]:
    """(repo, worktree, main_env): a repo, its linked worktree, and the main
    checkout's `.env` (gitignored, so the worktree cannot have one)."""
    import subprocess
    repo = tmp_path / "main"
    repo.mkdir(parents=True)
    subprocess.run(["git", "-C", str(repo), "init", "-b", "master"],
                   check=True, capture_output=True, text=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "t@t"],
                   check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "t"],
                   check=True, capture_output=True)
    (repo / "README").write_text("x")
    make_project(repo)  # `<repo>/.agi/` + config.json
    write_node(repo / ".agi", DEFAULT_NODE)
    subprocess.run(["git", "-C", str(repo), "add", "-A"], check=True,
                   capture_output=True, text=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "init"],
                   check=True, capture_output=True, text=True)
    wt = tmp_path / "wt"
    subprocess.run(["git", "-C", str(repo), "worktree", "add",
                    "-b", "loop/x@s2", str(wt), "master"],
                   check=True, capture_output=True, text=True)
    main_env = write_env(repo, "OPENROUTER_API_KEY=sk-main-only\n")
    return repo, wt, main_env


def test_resolve_from_worktree_reads_the_main_checkout_env(tmp_path):
    """cwd `.agi/worktrees/<agent>` must resolve to the MAIN checkout's
    gitignored `.env`, never to a nonexistent per-worktree fork."""
    import os as _os
    _, wt, main_env = _worktree_repo(tmp_path)
    old = _os.getcwd()
    try:
        _os.chdir(wt)  # a dispatched kid's cwd: the worktree root
        res = agi_secrets.resolve(None)
    finally:
        _os.chdir(old)
    assert res.from_node
    assert res.env_file == main_env, (
        "a worktree kid must read the main checkout's .env, not a "
        f"per-worktree fork at {wt / '.env'}"
    )


def test_env_get_from_worktree_resolves_shared_env_file(tmp_path):
    """The value a worktree kid authenticates with comes out of the MAIN
    checkout's .env through git_common_root — not the worktree's own dir."""
    import os as _os
    repo, wt, main_env = _worktree_repo(tmp_path)
    # envfile's path from the worktree must point at the main checkout.
    old = _os.getcwd()
    try:
        _os.chdir(wt)
        res = agi_secrets.resolve(None)
    finally:
        _os.chdir(old)
    assert res.env_file.is_file()
    assert res.env_file == repo / ".env"
    env = agi_secrets.read_env(main_env)
    assert env["OPENROUTER_API_KEY"] == "sk-main-only"
