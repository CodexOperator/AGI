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
