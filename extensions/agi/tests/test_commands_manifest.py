"""hypothesis:commands-manifest-is-jevs-one-choice-surface — the manifest reader.

`commands.py manifest` prints ONE deterministic JSON choice set from
`command:commands` alone. The node is only allowed to exist because code
resolves against it (`goal:g10.2`), so the interesting test is not "does it
print JSON" but:

1. **drift** — every verb of `write.py`'s `VERBS` table (plus `create`) is
   either a declared `manifest:` entry or an `excluded:` entry declared BY
   NAME with a reason. The test INTROSPECTS the module, never a copied list,
   so a new verb fails here instead of shipping undeclared.
2. **determinism** — two renders are byte-identical.
3. **no machine state** — no absolute path, no resolved home/root/engine.
4. **read-only** — the manifest writes no file and spawns no process.

The live test reads the real `command:commands` node; only the read-only and
shape tests use a synthetic node, because they are about the resolver rather
than about the declaration.
"""
from __future__ import annotations

import importlib.machinery
import importlib.util
import json
import sys
from pathlib import Path

import pytest

BIN = Path(__file__).resolve().parent.parent / "bin"
SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(BIN))
sys.path.insert(0, str(SRC))

import commands  # noqa: E402
import locations  # noqa: E402

#: `write.py` is a script, not a package module: load it by path. It must be
#: registered in `sys.modules` BEFORE `exec_module` or the `@dataclass`
#: decorator fails resolving `cls.__module__` (hit on the first attempt).
_loader = importlib.machinery.SourceFileLoader("write_module_manifest_test",
                                               str(BIN / "write.py"))
_spec = importlib.util.spec_from_loader(_loader.name, _loader)
write_module = importlib.util.module_from_spec(_spec)
sys.modules[_loader.name] = write_module
_loader.exec_module(write_module)

NODE = """---
commands:
  smoke:
    argv: ["bash", "<engine>/driver.sh", "--smoke"]
    about: "no dispatch"
manifest:
  write.py:set:
    cli: write.py
    verb: set
    argv: ["python3", "<engine>/write.py", "<node-id>", "set <key> <value>"]
    args:
      - {name: key, type: str, required: true, choices: []}
      - {name: value, type: str, required: true, choices: []}
    purpose: "set a key"
    side_effects: graph-write
    proposable: true
  write.py:read:
    cli: write.py
    verb: read
    argv: ["python3", "<engine>/write.py", "<node-id>", "read body 1:2"]
    purpose: "read a slice"
    side_effects: read
    proposable: true
excluded:
  write.py:patch:
    cli: write.py
    verb: patch
    argv: ["python3", "<engine>/write.py", "<node-id>", "patch -"]
    reason: "reads a unified diff on stdin"
    side_effects: graph-write
    proposable: false
id: "command:commands"
mint_id: aaaabbbbccccdddd
type: command
title: "Standard command declaration"
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


# --------------------------------------------------------------------------
# The live declaration: drift against the real verb table
# --------------------------------------------------------------------------

def _live_manifest() -> tuple[Path, dict]:
    root = locations.find_project_root(Path(__file__).resolve())
    assert root is not None, "test must run inside the project"
    return root, commands.manifest(root)


def test_every_write_verb_is_declared_or_excluded_by_name():
    """Falsifier: a write.py verb neither declared nor excluded."""
    _, man = _live_manifest()
    write_names = {k.split(":", 1)[1] for k in man if k.startswith("write.py:")}
    assert write_names == set(write_module.VERBS) | {"create"}, (
        "write.py's verb table and the node's write.py entries have drifted; "
        "add the verb to `manifest:` or `excluded:` in commands.md"
    )


def test_an_excluded_verb_is_not_proposable_and_carries_its_reason():
    _, man = _live_manifest()
    for key, entry in man.items():
        if key.startswith("write.py:") and entry.get("proposable") is False:
            assert entry.get("reason"), f"{key} excluded without a reason"
    for name in ("write.py:patch", "write.py:body_patch"):
        assert man[name]["proposable"] is False
        assert man[name]["reason"]


def test_every_entry_carries_the_typed_fields_a_proposer_reads():
    _, man = _live_manifest()
    assert man, "the live node must declare at least the write.py surface"
    for key, entry in man.items():
        assert entry["name"] == key
        assert entry["side_effects"] in commands.SIDE_EFFECTS, key
        assert isinstance(entry["argv"], list) and entry["argv"]
        assert isinstance(entry["args"], list)
        assert isinstance(entry["proposable"], bool)
        for arg in entry["args"]:
            assert set(arg) >= {"name", "type", "required", "choices"}, key


# --------------------------------------------------------------------------
# Determinism and machine-state hygiene
# --------------------------------------------------------------------------

def test_two_renders_are_byte_identical(project):
    first = commands.render_manifest(project)
    second = commands.render_manifest(project)
    assert first == second
    json.loads(first)  # and it is JSON, not a repr


def test_no_absolute_path_or_resolved_box_value_appears(project):
    text = commands.render_manifest(project)
    for entry in json.loads(text).values():
        for token in entry["argv"]:
            assert not str(token).startswith("/"), (
                "an absolute path in the manifest would not survive a clone")
    for box_value in (str(Path.home()), str(project.resolve())):
        assert box_value not in text


def test_the_write_surface_carries_no_home_placeholder():
    """The mesh commands keep `<home>` (clone-agnostic, resolved at run time)
    and the brief forbids editing them; every entry THIS round authored must
    carry only `<engine>`/`<node-id>`."""
    _, man = _live_manifest()
    for key, entry in man.items():
        if key.startswith("write.py:"):
            joined = " ".join(entry["argv"])
            assert "<home>" not in joined, key


# --------------------------------------------------------------------------
# Read-only: no write, no spawn
# --------------------------------------------------------------------------

def test_manifest_writes_no_file_and_spawns_no_process(project, monkeypatch):
    def boom(*a, **k):
        raise AssertionError("manifest must not spawn or write")

    for name in ("call", "Popen", "run", "check_call", "check_output"):
        monkeypatch.setattr(commands.subprocess, name, boom)
    monkeypatch.setattr(Path, "write_text", boom)
    monkeypatch.setattr(Path, "write_bytes", boom)

    # both readers, so the CLI branch is covered too
    assert isinstance(commands.manifest(project), dict)
    assert commands.render_manifest(project)


def test_the_manifest_action_prints_the_rendered_bytes(project, capsys):
    rc = commands.main(["manifest", "--root", str(project.parent)])
    assert rc == 0
    assert capsys.readouterr().out == commands.render_manifest(project) + "\n"


# --------------------------------------------------------------------------
# Every listed engine CLI: its verbs are declared or excluded BY NAME
# --------------------------------------------------------------------------
# The declaration is only complete if it covers the CLIs the brief names, and
# it is only honest if the verb list is READ OFF each CLI's own argparse at
# test time -- never a copied list. `_introspect_cli` captures the top parser
# by replacing `parse_args`/`parse_known_args` with a spy that raises the
# moment the parser is built, so no verb list is ever written down here.

_LISTED_CLIS = [
    "send.py", "dispatch.py", "workflow.py", "cli.py", "grid.py", "links.py",
    "rotate.py", "spawn_budget.py", "provisioning.py", "snapshot-goals.py",
    "viewport.py", "crons.py", "envfile.py",
]


class _ParserCaptured(Exception):
    """Raised by the spy once the top-level parser exists, before it parses."""


def _arg_dests(parser) -> set[str]:
    return {a.dest for a in parser._actions if a.dest != "help"}


def _subparsers(parser) -> dict:
    import argparse
    for act in parser._actions:
        if isinstance(act, argparse._SubParsersAction):
            return dict(act.choices)
    return {}


def _introspect_cli(cli: str, monkeypatch) -> dict[str, set[str]]:
    """`{verb: {arg dests}}` read from the CLI's OWN argparse, never a list.

    A CLI with subparsers keys on each verb; one with a positional `action`
    choices list keys on those choices; one with neither is the single verb
    `""`. The spy raises before parse, so `main` never does its work.
    """
    import argparse
    import contextlib
    import inspect
    import io

    captured: dict = {}

    def spy(self, *a, **k):
        captured.setdefault("top", self)
        raise _ParserCaptured()

    monkeypatch.setattr(argparse.ArgumentParser, "parse_args", spy)
    monkeypatch.setattr(argparse.ArgumentParser, "parse_known_args", spy)

    modname = "manifest_probe_" + cli.replace(".", "_").replace("-", "_")
    loader = importlib.machinery.SourceFileLoader(modname, str(BIN / cli))
    spec = importlib.util.spec_from_loader(modname, loader)
    module = importlib.util.module_from_spec(spec)
    sys.modules[modname] = module
    with contextlib.redirect_stdout(io.StringIO()), \
            contextlib.redirect_stderr(io.StringIO()):
        loader.exec_module(module)
        try:
            params = list(inspect.signature(module.main).parameters)
            try:
                module.main([]) if params else module.main()
            except TypeError:
                module.main()
        except (_ParserCaptured, SystemExit):
            pass

    top = captured.get("top")
    assert top is not None, f"{cli}: could not capture its ArgumentParser"

    subs = _subparsers(top)
    if subs:
        return {verb: _arg_dests(sp) for verb, sp in subs.items()}
    positionals = [a for a in top._actions
                   if not a.option_strings and a.dest != "help"]
    choices = next((list(a.choices) for a in positionals if a.choices), None)
    if choices is None:
        return {"": _arg_dests(top)}
    return {verb: _arg_dests(top) for verb in choices}


@pytest.mark.parametrize("cli", _LISTED_CLIS)
def test_every_listed_cli_verb_is_declared_or_excluded(cli, monkeypatch):
    """Falsifier: a verb of a listed CLI neither declared nor excluded."""
    _, man = _live_manifest()
    declared = {k.split(":", 1)[1] for k in man if k.startswith(cli + ":")}
    introspected = set(_introspect_cli(cli, monkeypatch))
    missing = sorted(introspected - declared)
    extra = sorted(declared - introspected)
    assert introspected == declared, (
        f"{cli} verbs and its manifest/excluded keys have drifted: "
        f"missing={missing} extra={extra}"
    )


@pytest.mark.parametrize("cli", _LISTED_CLIS)
def test_declared_args_are_still_accepted_by_the_cli(cli, monkeypatch):
    """Falsifier: a declared arg the CLI no longer accepts."""
    _, man = _live_manifest()
    dests = _introspect_cli(cli, monkeypatch)
    for key, entry in man.items():
        if not key.startswith(cli + ":") or not entry.get("proposable"):
            continue
        verb = key.split(":", 1)[1]
        allowed = dests.get(verb, set())
        for arg in entry["args"]:
            assert arg["name"] in allowed, (
                f"{key}: declares arg {arg['name']!r} the CLI no longer "
                f"accepts (has {sorted(allowed)})"
            )


def test_live_manifest_carries_no_absolute_path_or_box_value():
    root, man = _live_manifest()
    text = commands.render_manifest(root)
    for key, entry in man.items():
        for token in entry["argv"]:
            assert not str(token).startswith("/"), (key, token)
    for box_value in (str(Path.home()), str(root.resolve())):
        assert box_value not in text, box_value


# --------------------------------------------------------------------------
# propose: validate against the entry and RETURN the argv, never run it
# --------------------------------------------------------------------------

def test_propose_substitutes_values_into_a_compound_token():
    """The compound token `"set <key> <value>"` takes both values in place."""
    root, _ = _live_manifest()
    argv = commands.propose(root, "write.py:set",
                            {"key": "title", "value": "hello world"})
    assert argv[0] == "python3"
    assert argv[-1] == "set title hello world"


def test_propose_refuses_an_unknown_name_by_name():
    root, _ = _live_manifest()
    with pytest.raises(commands.CommandError) as exc:
        commands.propose(root, "write.py:nope", {})
    assert "write.py:nope" in str(exc.value)


def test_propose_refuses_a_non_proposable_entry_with_its_reason():
    root, _ = _live_manifest()
    with pytest.raises(commands.CommandError) as exc:
        commands.propose(root, "write.py:patch", {})
    assert "not proposable" in str(exc.value)
    assert "stdin" in str(exc.value)


def test_propose_refuses_missing_required():
    root, _ = _live_manifest()
    with pytest.raises(commands.CommandError) as exc:
        commands.propose(root, "write.py:set", {"key": "title"})
    assert "missing required" in str(exc.value)


def test_propose_refuses_a_value_outside_choices():
    root, _ = _live_manifest()
    with pytest.raises(commands.CommandError) as exc:
        commands.propose(root, "write.py:read",
                         {"target": "header", "range": "1:2"})
    assert "not in" in str(exc.value)


def test_propose_completes_a_required_arg_that_used_to_be_dropped():
    """The old `write.py:read` validated `range` then left `<N:M>` in the
    argv -- the silent drop. It must land, and no placeholder may survive."""
    root, _ = _live_manifest()
    argv = commands.propose(root, "write.py:read",
                            {"target": "body", "range": "1:2"})
    assert argv[-1] == "read body 1:2"


def test_every_proposable_entry_places_every_required_arg():
    """Falsifier: a required arg a proposer supplies that never lands.

    Feeds a distinct synthetic value for every required arg of every
    proposable entry and asserts each appears in the returned argv, so an
    entry that validates then silently drops an arg fails here rather than in
    a proposer's hands. Entries with no required arg have nothing to place."""
    root, man = _live_manifest()
    for key, entry in man.items():
        if not entry.get("proposable"):
            continue
        required = [a for a in entry.get("args") or [] if a.get("required")]
        if not required:
            continue
        args = {}
        for arg in required:
            choices = arg.get("choices") or []
            args[arg["name"]] = (choices[0] if choices
                                 else f"SYNTH{len(args)}x{arg['name']}")
        try:
            argv = commands.propose(root, key, args)
        except commands.CommandError as exc:
            pytest.fail(f"{key}: refused a fully-supplied proposal: {exc}")
        joined = " ".join(argv)
        for name, value in args.items():
            assert value in joined, (
                f"{key}: required arg {name!r}={value!r} never landed in "
                f"{argv!r}")


def test_no_spend_spawn_or_destructive_entry_is_proposable():
    _, man = _live_manifest()
    bad = [k for k, e in man.items()
           if e["side_effects"] in ("spend", "spawn", "destructive")
           and e["proposable"]]
    assert bad == [], bad


def test_propose_substitutes_once_and_ignores_undeclared_keys():
    """One pass only: a value containing `<x>` is never re-scanned, and a key
    that is not a declared arg substitutes nothing."""
    root, _ = _live_manifest()
    argv = commands.propose(root, "write.py:set",
                            {"key": "title", "value": "x <engine> y",
                             "engine": "BAD"})
    joined = " ".join(argv)
    assert "BAD" not in joined, joined
    assert "x <engine> y" in joined, joined


def test_propose_refuses_a_required_arg_with_nowhere_to_land(tmp_path: Path):
    """A supplied required arg whose name has no `<name>` in the template is a
    drop -- it must refuse by name, not return the argv."""
    graph = tmp_path / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / ".geometry" / "commands.md").write_text(
        "---\n"
        "manifest:\n"
        "  x.py:go:\n"
        "    cli: x.py\n"
        "    verb: go\n"
        "    argv: [python3, x.py, go]\n"
        "    args:\n"
        "      - {name: 'wanted', type: str, required: true, choices: []}\n"
        "    side_effects: read\n"
        "    proposable: true\n"
        "id: 'command:commands'\n"
        "mint_id: aaaabbbbccccdddd\n"
        "type: command\n"
        "title: probe\n"
        "---\n")
    with pytest.raises(commands.CommandError) as exc:
        commands.propose(graph, "x.py:go", {"wanted": "v"})
    assert "cannot place arg" in str(exc.value)
    assert "wanted" in str(exc.value)


def test_propose_refuses_an_unmapped_placeholder():
    """A template still holding a placeholder no declared arg maps must
    refuse by name rather than hand back an argv a proposer cannot run."""
    root, _ = _live_manifest()
    with pytest.raises(commands.CommandError) as exc:
        commands.propose(root, "session-complete", {})
    assert "unmapped placeholder" in str(exc.value)
    assert "<iter>" in str(exc.value)


def test_command_schema_declares_manifest_and_excluded():
    """The `[command]` schema names both maps its resolver reads."""
    root, _ = _live_manifest()
    text = (root / "context" / "schemas" / "[command].md").read_text()
    assert "manifest:" in text
    assert "excluded:" in text


def test_propose_writes_no_file_and_spawns_no_process(project, monkeypatch):
    def boom(*a, **k):
        raise AssertionError("propose must not spawn or write")

    for name in ("call", "Popen", "run", "check_call", "check_output"):
        monkeypatch.setattr(commands.subprocess, name, boom)
    monkeypatch.setattr(Path, "write_text", boom)
    monkeypatch.setattr(Path, "write_bytes", boom)
    assert commands.propose(project, "write.py:set",
                            {"key": "k", "value": "v"})


def test_propose_action_prints_argv_and_exits_zero(project, capsys):
    rc = commands.main(["propose", "write.py:set", "--args",
                        '{"key": "k", "value": "v"}',
                        "--root", str(project.parent)])
    assert rc == 0
    assert json.loads(capsys.readouterr().out) == [
        "python3", "<engine>/write.py", "<node-id>", "set k v"]


def test_propose_action_refuses_non_zero_on_stderr(project, capsys):
    rc = commands.main(["propose", "write.py:patch",
                        "--root", str(project.parent)])
    assert rc != 0
    assert "not proposable" in capsys.readouterr().err
