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

import importlib.machinery
import importlib.util

import commands  # noqa: E402
import locations  # noqa: E402

_loader = importlib.machinery.SourceFileLoader(
    "derive_commands", str(BIN / "derive-commands.py"))
_spec = importlib.util.spec_from_loader(_loader.name, _loader)
derive_commands = importlib.util.module_from_spec(_spec)
_loader.exec_module(derive_commands)
render_commands_table = derive_commands._render_table

NODE = """---
commands:
  smoke:
    argv: ["bash", "<engine>/driver.sh", "--smoke"]
    about: "no dispatch"
  tests:
    argv: ["python3", "-m", "pytest", "<root>/tests"]
    about: "the suite"
  raw-root:
    argv: ["python3", "-m", "cli", "<root>"]
    about: "ensure <root> survives in rendered docs"
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
    assert set(table) == {"smoke", "tests", "raw-root"}
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
        assert isinstance(cmd.raw_argv, list)
        assert cmd.raw_argv != cmd.argv, (
            "raw argv must preserve placeholders so derive-commands can render"
        )


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


def test_engine_for_resolves_the_engine_enclosing_the_graph(tmp_path):
    """`<engine>` must come from the engine that OWNS the graph, not from
    wherever the running script lives. In the unified single-repo layout the
    repo holding `.agi` also carries `extensions/agi/bin/commands.py`, so
    engine_for walks up from the graph root to find it — a worktree running
    with `--root` at the main checkout must substitute the MAIN engine, not
    the worktree's (hypothesis:l4-verification-counts-and-engine-root)."""
    main = tmp_path / "main-checkout"
    eng = main / "extensions" / "agi" / "bin"
    eng.mkdir(parents=True)
    (eng / "commands.py").write_text("# engine")
    graph = main / ".agi"
    graph.mkdir(parents=True)
    # a graph at main/.agi is owned by the engine at main/
    assert commands.engine_for(graph).resolve() == main.resolve()

    # a DIFFERENT project with no engine of its own falls back to this
    # script's engine rather than guess — and the caller names both roots.
    foreign = tmp_path / "foreign" / ".agi"
    foreign.mkdir(parents=True)
    assert commands.engine_for(foreign) == commands.ENGINE_ROOT


def test_load_substitutes_engine_from_the_root(tmp_path):
    """The <engine> a declared argv fills in is the engine OWNING the --root
    graph, so run_check against a foreign root never mixes engines. This is
    the resolution half of PROVED-BY (d)."""
    main = tmp_path / "main"
    eng = main / "extensions" / "agi" / "bin"
    eng.mkdir(parents=True)
    (eng / "commands.py").write_text("# engine")
    (main / ".agi" / "nodes" / ".geometry").mkdir(parents=True)
    (main / ".agi" / "config.json").write_text("{}")
    (main / ".agi" / "nodes" / ".geometry" / "commands.md").write_text(NODE)
    table = commands.load(main / ".agi")
    assert str(main.resolve()) in " ".join(table["smoke"].argv)
    assert str(commands.ENGINE_ROOT) not in " ".join(table["smoke"].argv)


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


def test_render_table_preserves_placeholders(project):
    table = render_commands_table(project)
    assert "<engine>" in table
    assert "<root>" in table
    assert "/home/" not in table, (
        "rendered docs must stay clone-agnostic — literal paths violate goal:g8.2"
    )


# --------------------------------------------------------------------------
# This project's own declaration — the table has to actually work
# --------------------------------------------------------------------------

# The graph this suite describes is the one it RUNS in, not the main checkout.
# goal:g11's resolver answers "where is the graph?" from where we stand; a test
# pinned to a literal path could only testify about one checkout. question 1 is
# find_project_root (the graph), question 2 is source_root (what it describes).
REAL_ROOT = locations.find_project_root(Path(__file__).resolve())
SOURCE_ROOT = locations.source_root(REAL_ROOT)
real_only = pytest.mark.skipif(
    not (REAL_ROOT / commands.COMMANDS_NODE_REL).is_file(),
    reason="this project's own commands node is not present")


def test_resolved_root_follows_the_tree_under_test():
    """The fixed REAL_ROOT must point into the SAME repo this test file lives
    in — a test that resolved to the main checkout while running in a seat
    worktree could not testify about the tree it ran in. Descendant check is
    the property that encodes "follows the tree under test" and is checkable
    without a second checkout."""
    own_repo = Path(__file__).resolve()
    assert REAL_ROOT is not None
    assert own_repo.is_relative_to(SOURCE_ROOT)
    assert REAL_ROOT.is_relative_to(SOURCE_ROOT)
    assert REAL_ROOT.name == ".agi"


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


def _declared_subcommands(script: Path) -> set[str] | None:
    """Every subcommand `script` accepts, or None if it declares none statically.

    THREE styles are in use in `bin/` and all have to be read:
    `sub.add_parser("commit")` (grid.py, crons.py),
    `add_argument("action", choices=[...])` (provisioning.py, links.py), and a
    module-level `SUBCOMMANDS = (...)` for a script that dispatches by hand
    rather than through argparse (write_guard.py).

    The third style was added at merge-up 3. It is a widening, NOT a
    loosening: `None` -- the script declares nothing at all -- is still a
    FAILURE, which is the property that makes this test a guard. What it fixes
    is a script that DOES accept its subcommand and had no argparse-shaped
    place to say so, which would otherwise have forced either a false failure
    or an argparse rewrite of a working CLI to satisfy a reader.
    """
    import ast

    try:
        tree = ast.parse(script.read_text())
    except (OSError, SyntaxError):
        return None

    found: set[str] = set()
    for node in ast.walk(tree):
        # style 3: a module-level `SUBCOMMANDS = ("check", "hook")`. Only a
        # literal sequence of string constants counts -- a name or a call
        # would be a promise this reader cannot check.
        if isinstance(node, ast.Assign):
            for tgt in node.targets:
                if isinstance(tgt, ast.Name) and tgt.id == "SUBCOMMANDS" \
                        and isinstance(node.value, (ast.Tuple, ast.List, ast.Set)):
                    found.update(e.value for e in node.value.elts
                                 if isinstance(e, ast.Constant)
                                 and isinstance(e.value, str))
        if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
            continue
        if node.func.attr == "add_parser":
            if node.args and isinstance(node.args[0], ast.Constant) \
                    and isinstance(node.args[0].value, str):
                found.add(node.args[0].value)
        elif node.func.attr == "add_argument":
            for kw in node.keywords:
                if kw.arg == "choices" and isinstance(kw.value, (ast.List, ast.Tuple)):
                    found.update(e.value for e in kw.value.elts
                                 if isinstance(e, ast.Constant)
                                 and isinstance(e.value, str))
    return found or None


@real_only
def test_every_declared_command_accepts_its_own_subcommand():
    """The file existing is not the command working, and the gap is real.

    On 2026-09-03 `write.py` was renamed to `links.py` and a new `write.py`
    took its place. `links` and `schema` were declared as `write.py links` /
    `write.py schema`, and both broke instantly — but the existence test above
    stayed green the whole time, because it only asks whether *a file by that
    name* exists, and one did. It was the wrong file.

    **The obvious probe does not work, and the reason is worth recording.**
    Shelling out to `script.py <sub> --help` and checking the exit code passes
    even when `<sub>` is nonsense: argparse handles `--help` first and exits
    0, so the new `write.py` cheerfully absorbed `links` as its `node_id`
    positional and printed its own help. That version of this test was written,
    run against the reintroduced bug, and **passed** — which is the only reason
    it is not still here. A guard is not a guard until it has failed once on
    purpose.

    So this reads the script instead of running it: every subcommand argparse
    declares, by either style, must contain the one the node declares.
    """
    broken = []
    for name, cmd in commands.load(REAL_ROOT).items():
        target = next((a for a in cmd.argv if a.endswith(".py")), None)
        if target is None:
            continue
        i = cmd.argv.index(target)
        sub = cmd.argv[i + 1:i + 2]
        # Only meaningful for a command declared WITH a subcommand; a bare
        # `script.py` is already covered by the existence test above.
        if not sub or sub[0].startswith("-"):
            continue
        accepted = _declared_subcommands(Path(target))
        # `None` — the script declares NO subcommand vocabulary — is a
        # failure, not a skip, and that distinction is the whole test. The
        # second version of this guard skipped it and stayed green on the real
        # bug for the second time: the new `write.py` takes two bare
        # positionals and declares no choices at all, so "nothing to check
        # against" was indistinguishable from "accepts anything". Every one of
        # the six commands in this table that carries a subcommand points at a
        # script that declares its vocabulary, so requiring one costs nothing
        # and is exactly the property that broke.
        if accepted is None:
            broken.append((name, f"{Path(target).name} {sub[0]}",
                           ["<script declares no subcommands>"]))
        elif sub[0] not in accepted:
            broken.append((name, f"{Path(target).name} {sub[0]}",
                           sorted(accepted)))
    assert broken == [], (
        "declared commands whose script does not accept their subcommand:\n"
        + "\n".join(f"  {n}: `{c}` — accepts {a}" for n, c, a in broken))


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


# --------------------------------------------------------------------------
# L1.06 — the `agi <verb>` router in driver.sh
# --------------------------------------------------------------------------

DRIVER = Path(__file__).resolve().parent.parent / "driver.sh"


def _agi(*args, cwd=None):
    import subprocess
    # cwd defaults to the SOURCE root of the tree under test, not the main
    # checkout — driver.sh must route against the graph this worktree carries.
    return subprocess.run(["bash", str(DRIVER), *args], capture_output=True,
                          text=True, timeout=180,
                          cwd=str(cwd or SOURCE_ROOT))


@real_only
def test_a_bare_first_word_runs_a_declared_command():
    """`agi links` must run the command the GRAPH declares.

    The verb list is deliberately NOT a `case` arm per verb in the shell —
    that would be a fifth prose copy of the command table, which is the exact
    drift `goal:g1.10` measured and ended. Adding `agi view` is a node edit.
    """
    proc = _agi("links")
    assert proc.returncode == 0, proc.stderr
    assert "resolved" in proc.stdout


@real_only
def test_flags_still_reach_the_driver_untouched():
    """The router must not capture the interface it was added beside."""
    proc = _agi("--help")
    assert proc.returncode == 0
    assert "OPTIONS:" in proc.stdout
    assert "--max-iters" in proc.stdout


@real_only
def test_an_unknown_verb_names_what_is_declared_and_points_at_the_node():
    proc = _agi("nosuchverb")
    assert proc.returncode != 0
    blob = proc.stdout + proc.stderr
    assert "nosuchverb" in blob
    assert "links" in blob, "the error must list what IS available"
    assert "commands.md" in blob, "and say where to add one"


@real_only
def test_pass_through_flags_reach_the_command_not_the_router():
    """🔴 `agi write <id> <script> --dry-run` died on
    `unrecognized arguments: --dry-run` — the router eating its passenger's
    mail. Fixed with `--` before the extras and `--root` before the verb.
    """
    proc = _agi("write", "goal:g9.7", "set status active", "--dry-run")
    assert proc.returncode == 0, proc.stderr
    assert "goal:g9.7" in proc.stdout
    assert "unrecognized" not in (proc.stdout + proc.stderr)


@real_only
def test_the_view_commands_are_declared_in_the_graph():
    """The owner asked for two views: the human one with spiders, and the one
    an LLM actually receives. Both are commands, so both are discoverable."""
    table = commands.load(REAL_ROOT)
    for name in ("view", "view-llm", "write"):
        assert name in table, f"`agi {name}` is not declared"
    assert "--live" in table["view"].argv, "the human view is the live one"
    assert "llm" in table["view-llm"].argv


def test_subcommand_reader_still_fails_a_script_that_declares_nothing(tmp_path):
    """The widening at merge-up 3 must not have turned the guard toothless.

    `_declared_subcommands` gained a third style (a module-level SUBCOMMANDS
    literal). The property that makes the guard work is unchanged: a script
    that declares NO vocabulary returns None, and the caller treats None as a
    failure rather than a skip. Twice before, "nothing to check against" was
    indistinguishable from "accepts anything" and a real bug stayed green — so
    this asserts the negative case directly rather than trusting the widening.
    """
    silent = tmp_path / "silent.py"
    silent.write_text("import sys\n\n\ndef main():\n    return 0\n")
    assert _declared_subcommands(silent) is None

    declared = tmp_path / "declared.py"
    declared.write_text('SUBCOMMANDS = ("check", "hook")\n')
    assert _declared_subcommands(declared) == {"check", "hook"}

    # A name or a call is a promise the reader cannot check, so it counts for
    # nothing — otherwise `SUBCOMMANDS = _discover()` would pass while saying
    # nothing a reader can verify.
    indirect = tmp_path / "indirect.py"
    indirect.write_text("SUBCOMMANDS = _discover()\n")
    assert _declared_subcommands(indirect) is None
