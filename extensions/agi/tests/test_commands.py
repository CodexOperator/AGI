"""goal:g1.10 — the engine's standard commands, declared in a node.

The node is only allowed to exist because code resolves against it
(`goal:g10.2`): a command table nothing reads is a fifth copy of `CLAUDE.md`'s
prose rather than the deletion of the other four. So these tests are mostly
about the two readers — the resolver, and the `INJECTION.md` renderer that
hands the set to every agent.

The sharpest test here is
`test_a_node_that_exists_but_cannot_be_read_says_so`. The first version of
`_load_node` returned `{}` for both "no node" and "node present but
unreadable", so a missing `src/` on `sys.path` reported *"no commands
declared"* about a fully parseable node sitting right there.
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import commands  # noqa: E402

NODE = """---
commands:
  smoke:
    argv: ["bash", "<engine>/driver.sh", "--smoke"]
    about: "no dispatch"
  tests:
    argv: ["python3", "-m", "pytest", "<root>/tests"]
    about: "the suite"
  broken:
    argv: "not a list"
    about: "a note, not a command"
id: "command:commands"
mint_id: aaaabbbbccccdddd
type: command
title: "Standard command declaration"
ordered:
  - verify
workflows:
  verify: [smoke, tests]
  loose: [smoke]
---

body
"""


@pytest.fixture()
def project(tmp_path: Path) -> Path:
    graph = tmp_path / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / ".geometry" / "commands.md").write_text(NODE)
    return graph


def test_commands_resolve_from_the_node(project):
    table = commands.load(project)
    assert set(table) == {"smoke", "tests"}
    assert table["tests"].about == "the suite"


def test_a_command_with_no_argv_list_is_skipped_not_half_resolved(project):
    """A Command that cannot run is worse than an absent one — it looks
    available."""
    assert "broken" not in commands.load(project)


def test_placeholders_are_substituted_so_the_node_holds_no_absolute_paths(project):
    table = commands.load(project)
    assert "<root>" not in " ".join(table["tests"].argv)
    assert "<engine>" not in " ".join(table["smoke"].argv)
    assert str(project.resolve()) in " ".join(table["tests"].argv)
    raw = (project / "nodes" / ".geometry" / "commands.md").read_text()
    assert "/home/" not in raw, (
        "an absolute path in the node is machine state the graph must not "
        "carry (goal:g8.2)")


def test_argv_is_a_list_so_nothing_is_reparsed_by_a_shell(project):
    """A shell string invites `&&`, pipes and quoting, and then the node stops
    being data and becomes a program the resolver interprets."""
    for cmd in commands.load(project).values():
        assert isinstance(cmd.argv, list)
        assert all(isinstance(a, str) for a in cmd.argv)


def test_an_unknown_command_names_what_is_available(project):
    with pytest.raises(commands.CommandError) as exc:
        commands.get(project, "nope")
    assert "smoke" in str(exc.value) and "tests" in str(exc.value)
    assert "editing the node IS the change" in str(exc.value)


def test_absent_node_is_a_supported_state(tmp_path):
    graph = tmp_path / ".agi"
    (graph / "nodes").mkdir(parents=True)
    assert commands.load(graph) == {}
    assert commands.render_for_injection(graph) == []


def test_a_node_that_exists_but_cannot_be_read_says_so(project, capsys):
    """Absence is silent because it is normal; failing to read something
    present never is. The first version returned `{}` for both."""
    (project / "nodes" / ".geometry" / "commands.md").write_text(
        "---\nnot: [valid\n---\nbody\n")
    assert commands.load(project) == {}
    assert "could not be read" in capsys.readouterr().err


# --------------------------------------------------------------------------
# The INJECTION.md renderer — the reader that justifies the node
# --------------------------------------------------------------------------

def test_only_a_declared_ordered_workflow_is_rendered_as_a_sequence(project):
    """Telling every agent that an unordered set must be run in order is a
    false instruction delivered at scale — the class of mistake `goal:s8`
    records, where every kid was handed a contradictory contract."""
    text = "\n".join(commands.render_for_injection(project))
    assert "- **verify** — in this order:" in text
    assert "- **loose**:" in text
    assert "loose** — in this order" not in text


def test_the_injected_lines_carry_the_runnable_command(project):
    text = "\n".join(commands.render_for_injection(project))
    assert "pytest" in text
    assert "the suite" in text, "the `about` is what makes the list usable"


# --------------------------------------------------------------------------
# This project's own declaration — the table has to actually work
# --------------------------------------------------------------------------

REAL_ROOT = Path("/home/ubuntu/work/agi/.agi")
real_only = pytest.mark.skipif(
    not (REAL_ROOT / commands.COMMANDS_NODE_REL).is_file(),
    reason="this project's own commands node is not present")


@real_only
def test_every_declared_command_points_at_something_that_exists():
    """A declared command whose script is gone is a command that will fail the
    first time a cold session trusts it. Caught here rather than there."""
    missing = []
    for name, cmd in commands.load(REAL_ROOT).items():
        target = next((a for a in cmd.argv if a.endswith((".py", ".sh"))), None)
        if target and not Path(target).exists():
            missing.append((name, target))
    assert missing == [], f"declared commands point at missing files: {missing}"


@real_only
def test_the_declaration_stays_small():
    """The owner's scope, enforced: *not a command for every custom test call,
    just the commands used during standard workflows*. The failure mode for
    this node is not being wrong, it is growing."""
    table = commands.load(REAL_ROOT)
    assert len(table) <= 20, (
        f"{len(table)} commands declared. This is not a shell-alias dumping "
        f"ground — a command that saves one keystroke does not belong; one a "
        f"cold session must be TOLD does (goal:g1.10).")
