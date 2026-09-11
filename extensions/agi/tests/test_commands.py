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

import os
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
#
# `find_project_root` returns `Optional[Path]`, and the None is handled HERE
# rather than inside a test. The marker's whole promise is a SKIP when this
# project's node is absent; a bare `REAL_ROOT / ...` would raise TypeError
# while the module was still being imported, turning that promised skip into
# a collection error — a louder failure than the literal it replaced, in the
# one case the marker exists for. An assertion inside a test body cannot
# cover this: import happens first.
REAL_ROOT = locations.find_project_root(Path(__file__).resolve())
SOURCE_ROOT = locations.source_root(REAL_ROOT) if REAL_ROOT else None
real_only = pytest.mark.skipif(
    REAL_ROOT is None
    or not (REAL_ROOT / commands.COMMANDS_NODE_REL).is_file(),
    reason="this project's own commands node is not present")

# The stream group's argv resolves `<stub>` through `locations.streamer_stub`
# (default `~/work/streamer-stub`), and the real-fragment tests below assert
# `os.path.isfile` / `os.access(X_OK)` / `.is_dir()` against that directory ON
# DISK. On a box where the stub is not installed -- a fresh engine clone, CI,
# an unrelated project -- those assertions FAIL, not skip (the argument is
# `<stub>/bin/hold.sh`; the file is missing). `@real_only` does not cover this:
# it skips only when `REAL_ROOT` is None or this project's own commands node is
# missing, both true on any machine including ones with no stub. This is the
# same external-artifact convention as test_reconciler.py's
# `pytest.skip("... not present; evidence is elsewhere")` -- a machine without
# the stub skips the STUB-DEPENDENT assertions, never runs-and-fails them.
STREAM_STUB_PRESENT = (
    REAL_ROOT is not None
    and locations.streamer_stub(REAL_ROOT).is_dir()
)
stub_only = pytest.mark.skipif(
    not STREAM_STUB_PRESENT,
    reason=(
        "streamer stub not installed under locations.streamer_stub "
        "(default ~/work/streamer-stub); the executable-FILE evidence these "
        "assertions check lives on the operator's box, not in a fresh clone "
        "(cf. test_reconciler.py `not present; evidence is elsewhere`)"))


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


# --------------------------------------------------------------------------
# l4-the-command-runner-eats-its-passengers-flag — the wrapper must not
# answer for a flag the caller typed for someone else
# --------------------------------------------------------------------------

@real_only
def test_a_leading_flag_reaches_the_target_without_a_separator(monkeypatch):
    """🔴 `commands.py run links --dry-run` used to print the WRAPPER's usage.

    Measured before the fix (experiment:a00-914a9ae6-ee1f1e): argparse
    claimed the `-`-prefixed token for `commands.py` itself, so the error
    read `commands.py: error: unrecognized arguments: --dry-run` and printed
    `commands.py`'s usage block — handing a reader debugging a flag they
    typed for `links.py` the wrong program's manual. The error lied about
    whose problem it was. Any leading dash did it, not only `--long`.
    """
    seen = {}

    def fake_run(root, name, extra):
        seen["name"] = name
        seen["extra"] = list(extra)
        return 0

    monkeypatch.setattr(commands, "run", fake_run)
    assert commands.main(["run", "links", "--dry-run"]) == 0
    assert seen["name"] == "links"
    assert seen["extra"] == ["--dry-run"], (
        "the flag must reach the target, not be eaten by the wrapper")

    seen.clear()
    assert commands.main(["run", "links", "-x"]) == 0
    assert seen["extra"] == ["-x"], "a single dash is claimed the same way"


@real_only
def test_the_separator_form_still_works_unchanged(monkeypatch):
    """`--` is documented in `main`'s own docstring and callers may rely on
    it. Whatever the wrapper does with a bare leading flag, the explicit form
    must keep forwarding exactly what it forwarded before."""
    seen = {}

    def fake_run(root, name, extra):
        seen["extra"] = list(extra)
        return 0

    monkeypatch.setattr(commands, "run", fake_run)
    assert commands.main(["run", "links", "--", "--dry-run"]) == 0
    assert seen["extra"] == ["--dry-run"]


@real_only
def test_a_wrapper_flag_after_the_name_still_binds_to_the_wrapper():
    """The trade-off, pinned to what was DECIDED rather than what falls out.

    `--root` after the name already bound to the wrapper before this fix —
    `commands.py run links --root /tmp` printed `ERR: not an agi project:
    /tmp`, never running the command. That was accidental status quo, and
    the round measured it rather than guessing. `parse_known_args` preserves
    it; `argparse.REMAINDER` would have forwarded `--root /x` to the target
    and changed behaviour nobody asked to change. This test is why that
    choice cannot be quietly reversed later.
    """
    assert commands.main(["run", "links", "--root", "/tmp"]) == 1


# --- `<stub>` substitution and the owner-only gate (residue 6) ------------
#
# The stream command group (`command:commands`) declares its argv as
# `<stub>/<subcommand>`; `<stub>` must resolve from `locations.streamer_stub`
# at run time exactly the way `<root>`/`<engine>` do, and `panic` must be
# refused for every actor but the owner BEFORE any subprocess call. The stream
# is LIVE — these tests never execute the stub; the owner-path test
# monkeypatches `subprocess.call` and would fail if the real one were reached.

# The landed argv spelling for the stream group (see the real fragment,
# briefs/commands.stream.fragment.md): each argv[0] is `<stub>/bin/<script>` —
# an executable FILE, never `<stub>` alone (a directory) — carrying the
# explicit flag that reaches its mode. hold.sh dispatches on argv[0]'s
# basename (case "${0##*/}"), so a bare `hold.sh brb` spelling falls through
# to usage/exit 2; only the explicit --status/--pause/--off reach a mode.
STREAM_NODE = """---
commands:
  sb-status:
    argv: ["<stub>/bin/hold.sh", "--status"]
    about: "read-only stream status"
    workflow: read
    owner_only: false
  brb:
    argv: ["<stub>/bin/hold.sh", "--pause"]
    about: "pause the streamer — operator sets the stub to be-right-back"
    workflow: see
    owner_only: false
  back:
    argv: ["<stub>/bin/hold.sh", "--off"]
    about: "resume the streamer after brb — operator brings the stub back to live"
    workflow: see
    owner_only: false
  panic:
    argv: ["<stub>/bin/panic.sh"]
    about: "OWNER-ONLY emergency stop"
    workflow: see
    owner_only: true
id: "command:commands"
mint_id: aaacccc11112222
type: command
title: "stream command group"
---

body
"""


@pytest.fixture()
def stream_project(tmp_path: Path) -> Path:
    graph = tmp_path / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / ".geometry" / "commands.md").write_text(STREAM_NODE)
    return graph


def test_stub_is_substituted_at_resolve_time_not_left_literal(stream_project):
    """`<stub>` must resolve to the streamer stub's real directory the way
    `<root>`/`<engine>` do, so a declared command actually runs. The rendered
    docs keep the placeholder (goal:g8.2)."""
    cmd = commands.get(stream_project, "sb-status")
    assert cmd.argv[0] != "<stub>"
    assert cmd.argv[0] == str(
        locations.streamer_stub(stream_project) / "bin" / "hold.sh")
    assert cmd.argv[0].endswith("streamer-stub/bin/hold.sh")
    # The landed argv carries an explicit flag, not a bare subcommand word —
    # hold.sh dispatches on argv[0] basename, so a bare `hold.sh sb-status`
    # spelling would fall through to usage/exit 2 (measured).
    assert cmd.argv == [
        str(locations.streamer_stub(stream_project) / "bin" / "hold.sh"),
        "--status",
    ]
    assert "<stub>" not in " ".join(cmd.argv), "resolve-time, not literal"
    # The rendered form keeps the raw token so docs stay machine-agnostic
    # (the resolved path must never leak into docs, goal:g8.2).
    assert "<stub>" in cmd.shell(placeholders=True)
    assert cmd.shell() != cmd.shell(placeholders=True)


def test_stub_is_configurable_from_locations_streamer_stub(stream_project, monkeypatch):
    """`locations.streamer_stub` in the config overrides the default."""
    custom = stream_project.parent / "my-stub"
    custom.mkdir()
    cfg = locations.load_config(stream_project)
    cfg.setdefault("locations", {})["streamer_stub"] = str(custom)
    monkeypatch.setattr(
        locations, "load_config",
        lambda root: cfg if str(Path(root).resolve()) == str(
            stream_project.resolve()) else {},
    )
    stub = locations.streamer_stub(stream_project)
    assert str(stub) == str(custom.resolve())
    # argv[0] resolves under the configured stub — `<stub>/bin/hold.sh`
    assert commands.get(stream_project, "sb-status").argv[0] == str(
        custom.resolve() / "bin" / "hold.sh")
    assert commands.get(stream_project, "sb-status").argv[0].startswith(
        str(custom.resolve()))


def test_panic_is_refused_for_a_non_owner_without_any_subprocess(
        stream_project, monkeypatch, capsys):
    """A non-owner asking for `panic` is refused loudly with a non-zero exit
    and NOTHING is executed — the stream stays live. subprocess.call is
    monkeypatched to fail the test if it is ever reached."""

    def _never(*_a, **_k):
        raise AssertionError(
            "panic must be refused before any subprocess call") 

    monkeypatch.setenv("AGI_ACTOR", "some-agent")
    monkeypatch.delenv("USER", raising=False)
    monkeypatch.setattr(commands.subprocess, "call", _never)

    code = commands.run(stream_project, "panic")
    assert code == 3
    err = capsys.readouterr().err
    assert "REFUSED" in err
    assert "owner_only" in err
    assert "some-agent" in err


def test_panic_passes_for_the_owner_without_spawning_the_stub(
        stream_project, monkeypatch, capsys):
    """Actor `owner` clears the gate — but the test still must not spawn the
    stub (the stream is LIVE), so subprocess.call is monkeypatched and the
    received argv inspected instead of executed."""
    seen = {}

    def _fake_call(argv, cwd=None):
        seen["argv"] = list(argv)
        seen["cwd"] = cwd
        return 0

    monkeypatch.setenv("AGI_ACTOR", "owner")
    monkeypatch.delenv("USER", raising=False)
    monkeypatch.setattr(commands.subprocess, "call", _fake_call)

    assert commands.run(stream_project, "panic") == 0
    # The landed argv is `<stub>/bin/panic.sh` with NO flag — a bare panic.sh
    # with no argument is the full hard cut.
    assert seen["argv"] == [
        str(locations.streamer_stub(stream_project) / "bin" / "panic.sh")]
    assert len(seen["argv"]) == 1


def test_owner_only_defaults_to_false(stream_project):
    """A command with no `owner_only` cell runs for anyone — the field must
    default to False, not reject everything."""
    assert commands.get(stream_project, "sb-status").owner_only is False
    assert commands.get(stream_project, "panic").owner_only is True


# --------------------------------------------------------------------------
# L4.143 — hypothesis:l4-the-stream-fragment-argv-resolves-to-executables.
# The stream group's argv must resolve to EXECUTABLE FILES, each reaching its
# intended mode — READ FROM THE REAL FRAGMENT, not a synthetic fixture.
#
# 🔴 First version of these four entries declared argv as `<stub>` plus a bare
# subcommand word (`["<stub>", "sb-status"]`, `["<stub>", "brb"]`, ...) and a
# rewrite proposal said `hold.sh brb`. Both spellings are false, measured
# against the real stub:
#   * `<stub>` alone resolves to the stub DIRECTORY — executing it runs a
#     directory, not a script.
#   * `hold.sh brb` (argv[0]=hold.sh, argv[1]=brb) hits the usage error:
#     hold.sh dispatches on argv[0]'s BASENAME via `case "${0##*/}"`
#     (bin/hold.sh:21-25). A `hold.sh` basename falls to `*)`, setting
#     MODE="$1"="brb"; "brb" is not a known MODE, so `case "$MODE"` falls to
#     `*)` → usage/exit 2. Measured in a SANDBOXED SB_HOME: `hold.sh brb`
#     → "usage: brb | retract | back | brb --status", exit 2 (does NOT pause);
#     `hold.sh --pause` → "PAUSED.", exit 0.
# So each argv is now `<stub>/bin/<script> <explicit-flag>`, keeping
# `locations.streamer_stub` as the ONE configurable root. These tests assert
# the real argv resolves to an executable FILE that carries an explicit flag
# reaching its mode. They must NOT execute hold.sh / panic.sh / live.sh — the
# stream is LIVE; this is a static + filesystem assertion only.
# --------------------------------------------------------------------------

FRAGMENT = BIN.parent / "briefs" / "commands.stream.fragment.md"

# Which argv[1] reaches each intended mode of the executable, as measured.
# hold.sh dispatches on basename, so with argv[0] always `hold.sh` a bare
# word can never reach a mode — only these explicit flags can. `sb-status` is
# NOT here: it is the one two-half command (L4.165,
# hypothesis:l4-sb-status-is-both-halves) whose argv[0] is the `~/bin/sb-status`
# wrapper (hold.sh --status + panic.sh --status), not a hold.sh flag.
_HOLD_FLAG_MODES = {
    "brb":        "--pause",   # pause / BRB card
    "back":       "--off",     # release the hold
}
_PANIC_SCRIPT = "panic.sh"     # no flag = the full hard cut


def _check_sb_status_wrapper(exe: str, stub: Path, problems: list[str]) -> None:
    """`sb-status` is TWO halves reached through one wrapper executable
    (~/bin/sb-status, generated by <stub>/bin/install-cli.sh): the wrapper's
    body must invoke BOTH <stub>/bin/hold.sh --status AND
    <stub>/bin/panic.sh --status, and each stub half must itself exist and be
    executable. If the fragment ever names only one half (e.g. reverts to
    `<stub>/bin/hold.sh --status`), the argv[0] basename stops being
    `sb-status` and this whole branch — and thus the test — goes RED."""
    script = Path(exe)
    if script.name != "sb-status":
        problems.append(
            f"sb-status: argv[0] must be the two-half wrapper ~/bin/sb-status "
            f"(reaches both hold.sh --status and panic.sh --status), got "
            f"{script.name}")
        return
    if not script.is_file():
        problems.append(f"sb-status: wrapper not a file: {exe}")
        return
    try:
        text = script.read_text()
    except OSError as exc:
        problems.append(f"sb-status: cannot read wrapper {exe}: {exc}")
        return
    lines = text.splitlines()
    hold_line = next((ln for ln in lines if "hold.sh" in ln), None)
    panic_line = next((ln for ln in lines if "panic.sh" in ln), None)
    # hold half
    if hold_line is None:
        problems.append("sb-status wrapper: no hold.sh half found")
    elif "--status" not in hold_line:
        problems.append(f"sb-status wrapper: hold half missing --status: {hold_line}")
    elif str(stub) not in hold_line:
        problems.append(f"sb-status wrapper: hold half not on the stub: {hold_line}")
    # panic half
    if panic_line is None:
        problems.append("sb-status wrapper: no panic.sh half found")
    elif "--status" not in panic_line:
        problems.append(f"sb-status wrapper: panic half missing --status: {panic_line}")
    elif str(stub) not in panic_line:
        problems.append(f"sb-status wrapper: panic half not on the stub: {panic_line}")
    # each stub half exists and is executable
    for label, rela in (("hold", "hold.sh"), ("panic", "panic.sh")):
        half = stub / "bin" / rela
        if not os.path.isfile(half):
            problems.append(f"sb-status: stub {label} half not a file: {half}")
        elif not os.access(half, os.X_OK):
            problems.append(f"sb-status: stub {label} half not executable: {half}")



def _stream_fragment_commands():
    """The yaml `commands:` block from the REAL stream fragment."""
    import yaml
    text = FRAGMENT.read_text()
    block = text.split("```yaml", 1)[1].split("```", 1)[0]
    decl = yaml.safe_load(block)
    assert isinstance(decl, dict) and decl, "fragment must declare commands"
    return decl


@real_only
@stub_only
def test_stream_fragment_argv_resolves_to_executable_files():
    """Every declared stream argv, after `<stub>` substitution, must start with
    an existing executable FILE carrying an explicit flag reaching the command's
    intended mode — a directory (`<stub> <word>`) or a bare-word `hold.sh brb`
    spelling is a command that fails the first time a cold operator trusts it
    (or executes a directory). The ONE exception is `sb-status`
    (L4.165, hypothesis:l4-sb-status-is-both-halves): it is a TWO-HALF command
    whose argv[0] is the `~/bin/sb-status` wrapper (off the stub root) that runs
    BOTH `hold.sh --status` and `panic.sh --status`; this test reads the wrapper
    and fails if EITHER half is missing, so a fragment naming only the hold
    half goes red. `brb`/`back` keep the hold.sh+flag spelling."""
    commands_decl = _stream_fragment_commands()
    stub = locations.streamer_stub(REAL_ROOT)
    assert stub.name == "streamer-stub" and stub.is_dir(), stub

    problems = []
    for name, spec in commands_decl.items():
        exe = str(spec["argv"][0]).replace("<stub>", str(stub)).replace(
            "<home>", str(Path.home()))
        tail = [
            str(a).replace("<stub>", str(stub)).replace("<home>",
                                                          str(Path.home()))
            for a in spec["argv"][1:]
        ]
        if not os.path.isfile(exe):
            problems.append(f"{name}: argv[0] is not a file: {exe}")
            continue
        if not os.access(exe, os.X_OK):
            problems.append(f"{name}: argv[0] not executable: {exe}")
        if name == "panic":
            if Path(exe).name != _PANIC_SCRIPT:
                problems.append(
                    f"panic: argv[0] must be {_PANIC_SCRIPT}, got {Path(exe).name}")
            if tail:
                problems.append(f"panic: no flag expected (full hard cut), got {tail}")
            continue
        if name == "sb-status":
            # the two-half wrapper — the ONE argv[0] allowed off the stub root
            if tail:
                problems.append(f"sb-status: wrapper takes no flag; got {tail}")
            _check_sb_status_wrapper(exe, stub, problems)
            continue
        want = _HOLD_FLAG_MODES.get(name)
        if want is None:
            problems.append(f"{name}: no expected mode registered for it")
            continue
        if Path(exe).name != "hold.sh":
            problems.append(f"{name}: argv[0] must be hold.sh, got {Path(exe).name}")
        if tail != [want]:
            problems.append(
                f"{name}: argv[1]={tail} does not reach its mode; want ['{want}'] "
                f"(hold.sh dispatches on basename — a bare word like 'brb' would "
                f"fall through to usage/exit 2)")
    assert problems == [], "\n".join(problems)


@stub_only
def test_real_fragment_resolves_through_commands_py_and_owner_gate(
        tmp_path, monkeypatch, capsys):
    """The REAL fragment's commands yaml, materialised into a temp project's
    commands node, must resolve through commands.py ITSELF — not a synthetic
    fixture (hypothesis:l4-the-stream-fragment-argv-resolves-to-executables).

    Every old resolve+gate test exercised a synthetic STREAM_NODE whose argv
    carried the BROKEN `<stub> <word>` / `<stub> panic` shape, so the code
    path was only tested against the spelling that was disproved. This test
    runs the real fragment's argv through commands.get / commands.run, so a
    future reader cannot re-derive the bug from a canonised fixture. The
    stream is LIVE — panic is REFUSED and nothing is executed; subprocess.call
    is monkeypatched to fail the test if it is ever reached.
    """
    import yaml
    decl = _stream_fragment_commands()
    node = ("---\n" + yaml.safe_dump({"commands": decl}, sort_keys=False)
            + "---\nbody\n")
    graph = tmp_path / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / ".geometry" / "commands.md").write_text(node)

    # 1) every resolved argv: no `<stub>` left literal, argv[0] an existing
    #    executable FILE reaching its loaded mode (via commands.py itself).
    stub = locations.streamer_stub(graph)
    for name in ("sb-status", "brb", "back", "panic"):
        cmd = commands.get(graph, name)
        assert "<stub>" not in cmd.shell(), f"{name}: <stub> left literal"
        argv0 = cmd.argv[0]
        assert os.path.isfile(argv0), f"{name}: argv[0] not a file: {argv0}"
        assert os.access(argv0, os.X_OK), (
            f"{name}: argv[0] not executable: {argv0}")
        if name == "sb-status":
            # the two-half wrapper lives at ~/bin/sb-status, off the stub root
            assert Path(argv0).name == "sb-status", (
                f"sb-status: argv[0] must be the ~/bin/sb-status wrapper, "
                f"got {Path(argv0).name}")
        else:
            assert str(stub) in argv0, f"{name}: {argv0} off the stub root"

    # 2) panic is REFUSED for a non-owner with a non-zero exit and NOTHING
    #    executed under any circumstance.
    def _never(*_a, **_k):
        raise AssertionError(
            "panic must be refused before any subprocess call")

    monkeypatch.setenv("AGI_ACTOR", "some-agent")
    monkeypatch.delenv("USER", raising=False)
    monkeypatch.setattr(commands.subprocess, "call", _never)

    assert commands.run(graph, "panic") == 3
    err = capsys.readouterr().err
    assert "REFUSED" in err and "owner_only" in err
    assert "some-agent" in err


@stub_only
def test_real_fragment_sb_status_resolves_from_home_not_stub_depth(
        tmp_path):
    """DEPTH-INDEPENDENCE (hypothesis:l4-sb-status-resolves-from-home-not-
    from-stub-depth). The real fragment's `sb-status` argv[0] is now spelled
    `<home>/bin/sb-status`, expanded by `_substitute` to `~/bin/sb-status`
    REGARDLESS of how deep `locations.streamer_stub` sits under home. The
    old `<stub>/../../bin/sb-status` spelling only resolved to the wrapper
    while the stub sat exactly two levels under home (the code default
    `~/work/streamer-stub`); a project configuring the stub at any OTHER
    depth resolved to a MISSING path — a command that fails the first time
    an operator trusts it. This test pins the stub THREE levels deep and
    asserts the resolved argv[0] is still the real `~/bin/sb-status`
    executable; under the old spelling it resolves to a missing path and this
    assertion goes RED (kept that behaviour on purpose).
    """
    import yaml
    decl = _stream_fragment_commands()
    node = ("---\n" + yaml.safe_dump({"commands": decl}, sort_keys=False)
            + "---\nbody\n")
    graph = tmp_path / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    # a stub THREE levels deep, i.e. NOT two levels under home — exactly where
    # the old `<stub>/../../bin/sb-status` spelling broke.
    deep_stub = tmp_path / "a" / "b" / "stub"
    deep_stub.mkdir(parents=True)
    (graph / "config.json").write_text(
        "{\"locations\": {\"streamer_stub\": \"%s\"}}" % deep_stub)
    (graph / "nodes" / ".geometry" / "commands.md").write_text(node)

    assert locations.streamer_stub(graph) == deep_stub.resolve()
    cmd = commands.get(graph, "sb-status")
    want = os.path.join(str(Path.home()), "bin", "sb-status")
    # the crux: argv[0] must resolve from HOME, not from the stub's depth.
    assert cmd.argv[0] == want, (
        f"sb-status: argv[0] should resolve from home to {want} "
        f"(stub is {deep_stub}, THREE levels deep), got {cmd.argv[0]}")
    assert os.path.isfile(cmd.argv[0]), (
        f"sb-status: resolved wrapper is not a file: {cmd.argv[0]}")
    assert os.access(cmd.argv[0], os.X_OK), (
        f"sb-status: resolved wrapper not executable: {cmd.argv[0]}")
    # the two-half wrapper still holds: its body invokes BOTH the real stub's
    # hold.sh --status AND panic.sh --status, each executable.
    problems = []
    _check_sb_status_wrapper(cmd.argv[0], locations.streamer_stub(REAL_ROOT),
                             problems)
    assert problems == [], "\n".join(problems)
    # the other three commands must be unchanged: `<stub>` off the declared
    # (depth-3) stub root, resolving to `<stub-relative>` paths (not asserted
    # as files here — the depth-3 stub is deliberately empty).
    for name in ("brb", "back", "panic"):
        cmd2 = commands.get(graph, name)
        assert "<home>" not in cmd2.shell()
        assert str(deep_stub.resolve()) in cmd2.argv[0], (
            f"{name}: argv[0] off the configured stub root")



@real_only
@stub_only
def test_stream_panic_is_declared_owner_only_and_never_executed():
    """`panic` must still be a DECLARATION, not a run green-light: owner_only
    stays true and the group is never executed by these fragments (the stream
    is LIVE). Asserted on the fragment's own yaml."""
    decl = _stream_fragment_commands()
    panic = decl["panic"]
    assert panic.get("owner_only") is True, "panic must stay owner_only: true"
    # Every entry is a template declaration for the operator table — none of
    # them may carry an eager/workflow that would execute the live stream.
    for name, spec in decl.items():
        assert "workflow" in spec, f"{name} missing workflow cell"
