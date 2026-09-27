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
import re
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


def _synthetic(tmp_path: Path, extra_marker: str) -> Path:
    """A minimal graph whose `x.py:go` entry has NO `<wanted>` metavar (a
    value with nowhere to land) and whose `x.py:slice` entry carries
    `extra_marker` verbatim after its declared `<target>`."""
    graph = tmp_path / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
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
        "  x.py:slice:\n"
        "    cli: x.py\n"
        "    verb: slice\n"
        f"    argv: [python3, x.py, slice, '<target>', '{extra_marker}']\n"
        "    args:\n"
        "      - {name: 'target', type: str, required: true, choices: []}\n"
        "    side_effects: read\n"
        "    proposable: true\n"
        "id: 'command:commands'\n"
        "mint_id: aaaabbbbccccdddd\n"
        "type: command\n"
        "title: probe\n"
        "---\n")
    return graph


def _synthetic_multi(tmp_path: Path, rules_yaml: str = "") -> Path:
    """A minimal graph whose `x.py:go` takes an optional `owns` with no
    `<owns>` in the template, plus `rules_yaml` under `placement:`."""
    graph = tmp_path / ".agi"
    (graph / "nodes" / ".geometry").mkdir(parents=True, exist_ok=True)
    (graph / "config.json").write_text("{}")
    (graph / "nodes" / ".geometry" / "commands.md").write_text(
        "---\n"
        "manifest:\n"
        "  x.py:go:\n"
        "    cli: x.py\n"
        "    verb: go\n"
        "    argv: [python3, x.py, go]\n"
        "    args:\n"
        "      - {name: 'owns', type: str, required: false, choices: []}\n"
        "    side_effects: read\n"
        "    proposable: true\n"
        "placement:\n"
        "  defaults: true\n"
        f"{rules_yaml}"
        "id: 'command:commands'\n"
        "mint_id: aaaabbbbccccdddd\n"
        "type: command\n"
        "title: probe\n"
        "---\n")
    return graph


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

# EF.48 CLI GROUP A. Appended rather than folded into the literal above so the
# sibling round's GROUP B edit cannot collide with this one.
_LISTED_CLIS += [
    "brief.py", "level3.py", "season.py", "heal.py", "zoom.py",
    "locations.py", "commands.py", "stitch.py", "paths.py",
    "evidence_gate.py",
]

# EF.48 CLI GROUP B. Appended, like GROUP A, so sibling edits cannot collide.
_LISTED_CLIS += [
    "sensei.py", "post_wire.py", "node_writer.py", "metrics.py", "unify.py",
    "hierarchy.py", "handoff.py", "benchmark.py", "anonymize.py",
]

# EF.54 CLI GROUP C. Appended, like GROUP A/B, so sibling edits cannot collide.
# These 11 build their parser outside a plain module-level `main()`: under
# `if __name__ == "__main__"`, in `_cli`/`_main`, or not at all (manual argv,
# listed parserless below).
_LISTED_CLIS += [
    "boxes.py", "branches.py", "completion.py", "mem_cap.py",
    "migrate_channel.py", "geometry_config.py", "spawn_gate.py", "towns.py",
    "ws_raw.py", "pi_edit_forgiveness.py", "pi_trajectory.py",
]

# EF.54 CLI GROUP D. Appended, like GROUP C, so sibling edits cannot collide.
# The 12 remaining engine CLIs whose parser is a plain module-level `main`:
# every one is captured by the harness already, so this round is DATA -- each
# verb declared or excluded by name in `command:commands`, read off its own
# argparse.
_LISTED_CLIS += [
    "backfill-mint-ids.py", "briefing.py", "dashboard.py",
    "decompose-engine.py", "derive-commands.py", "drift_check.py",
    "failures.py", "frontier.py", "glitch_master.py", "graphweb.py",
    "grid_coverage_check.py", "inject.py",
]

# EF.54 CLI GROUP E. Appended, like GROUP C/D, so sibling edits cannot collide.
# The 12 last engine CLIs whose parser is a plain module-level `main`; every
# verb is declared or excluded BY NAME in `command:commands`.
_LISTED_CLIS += [
    "lm_bench.py", "mail_alert.py", "payload_boundary.py", "plan_master.py",
    "reconciler.py", "rolslice.py", "seat_status.py", "stall_detect.py",
    "success_metrics.py", "telemetry_rollup.py", "verify_unified.py",
    "ws_raw_client.py",
]

# EF.69 CLI GROUP F. Appended, like GROUP A-E, so sibling edits cannot collide.
# `verification.py` has one optional positional (`window`) beside its bare
# rotation check; `write_guard.py` is a hand-rolled dispatcher that declares
# its vocabulary in a module-level `SUBCOMMANDS` tuple (it has no argparse at
# all) -- so `_introspect_cli` learns both shapes below. Every verb of each is
# declared or excluded BY NAME in `command:commands`.
_LISTED_CLIS += ["verification.py", "write_guard.py"]

#: `memory_alarm.py` is the box's memory-pressure reader: a plain module-level
#: `main` with a bare parser, whose EVERY threshold is a `config:crons` cell,
#: so a bare invocation has nothing to read. Declared by name in
#: `command:commands` with that reason, never proposable.
_LISTED_CLIS += ["memory_alarm.py"]

#: CLIs with NO argparse parser at all: `node_writer.py` is a library module
#: with no `main`, `metrics.py` reads a manual argv, `pi_edit_forgiveness.py`
#: and `pi_trajectory.py` parse argv by hand, and `ws_raw.py`'s `_parse_args`
#: is a hand-rolled scanner too (the parent brief called it "async", but the
#: async is only its `main`). They are still IN the coverage test --
#: `require_parser=False` returns the single-verb `{"": set()}` vocabulary,
#: EXCEPT when the module declares a module-level `SUBCOMMANDS` tuple (see
#: `_declared_subcommands`): `write_guard.py` dispatches by hand and its
#: `SUBCOMMANDS` is the vocabulary the coverage test reads. `main` is never
#: imported or run for these.
_PARSERLESS_CLIS = {"node_writer.py", "metrics.py", "pi_edit_forgiveness.py",
                    "pi_trajectory.py", "ws_raw.py", "write_guard.py"}


def _declared_subcommands(cli: str) -> set[str] | None:
    """A hand-rolled dispatcher's module-level `SUBCOMMANDS` tuple, or None.

    `write_guard.py` has no argparse for the spy to capture, so the vocabulary
    is read, never guessed: the tuple is a literal, and a computed value (an
    indirect `SUBCOMMANDS = _discover()`) returns None and the coverage test
    then treats the CLI as the single `""` verb, exactly as before.
    """
    import ast
    tree = ast.parse((BIN / cli).read_text(encoding="utf-8"))
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        if not any(isinstance(t, ast.Name) and t.id == "SUBCOMMANDS"
                   for t in node.targets):
            continue
        try:
            value = ast.literal_eval(node.value)
        except ValueError:
            return None
        return {str(v) for v in value} if isinstance(value, (list, tuple)) else None
    return None


class _ParserCaptured(Exception):
    """Raised by the spy once the top-level parser exists, before it parses."""


def _drive_module(path, modname: str, as_main: bool):
    """Exec `path` under the active argparse spy and drive its entry point.

    A CLI may build its parser in a module-level `main`, in `_cli`/`_main`, or
    only under `if __name__ == "__main__"`; this covers all three. `as_main`
    execs with `__name__ = "__main__"` so the guarded block fires. Every
    exception -- the spy, a SystemExit, or the CLI's own -- is swallowed: a
    probe must never let a verb run.
    """
    import contextlib
    import inspect
    import io
    import types

    # A plain `exec` rather than `SourceFileLoader.exec_module`: the loader
    # refuses a module whose `__name__` differs from the loader's (it cannot
    # "handle __main__"), and the whole point of the `as_main` pass is to give
    # the module `__name__ == "__main__"` so its guarded block fires.
    module = types.ModuleType(modname)
    module.__file__ = str(path)
    if as_main:
        module.__name__ = "__main__"
    sys.modules[modname] = module
    code = compile(Path(path).read_text(encoding="utf-8"), str(path), "exec")
    with contextlib.redirect_stdout(io.StringIO()), \
            contextlib.redirect_stderr(io.StringIO()):
        try:
            exec(code, module.__dict__)
            if as_main:
                return module
            for fname in ("main", "_cli", "_main", "_parse_args"):
                fn = getattr(module, fname, None)
                if not callable(fn):
                    continue
                try:
                    params = list(inspect.signature(fn).parameters)
                except (TypeError, ValueError):
                    continue
                try:
                    fn([]) if params else fn()
                except TypeError:
                    try:
                        fn()
                    except BaseException:  # noqa: BLE001 -- probe
                        pass
                break
        except BaseException:  # noqa: BLE001 -- probe: never run a verb
            pass
    return module


def _arg_dests(parser) -> set[str]:
    return {a.dest for a in parser._actions if a.dest != "help"}


def _subparsers(parser) -> dict:
    import argparse
    for act in parser._actions:
        if isinstance(act, argparse._SubParsersAction):
            return dict(act.choices)
    return {}


def _introspect_cli(cli: str, monkeypatch,
                    require_parser: bool = True) -> dict[str, set[str]]:
    """`{verb: {arg dests}}` read from the CLI's OWN argparse, never a list.

    A CLI with subparsers keys on each verb; one with a positional `action`
    choices list keys on those choices; one with neither is the single verb
    `""`. The spy raises before parse, so `main` never does its work.

    `require_parser=False` returns the single-verb `{"": set()}` WITHOUT
    importing or running the module -- the declared path for a parserless
    library/manual-argv CLI -- UNLESS the module declares a module-level
    `SUBCOMMANDS` tuple, which is then returned as its vocabulary. The
    parser-required assertion below stays on for every CLI whose caller leaves
    the knob True.
    """
    if not require_parser:
        subs = _declared_subcommands(cli)
        return {v: set() for v in subs} if subs else {"": set()}
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

    stem = "manifest_probe_" + cli.replace(".", "_").replace("-", "_")
    _drive_module(BIN / cli, stem, False)
    if "top" not in captured:
        # The parser was built ONLY under `if __name__ == "__main__"`.
        _drive_module(BIN / cli, stem + "_main", True)

    top = captured.get("top")
    assert top is not None, f"{cli}: could not capture its ArgumentParser"

    subs = _subparsers(top)
    if subs:
        return {verb: _arg_dests(sp) for verb, sp in subs.items()}
    positionals = [a for a in top._actions
                   if not a.option_strings and a.dest != "help"]
    optional = next((a for a in positionals if a.choices), None)
    if optional is None:
        return {"": _arg_dests(top)}
    out = {verb: _arg_dests(top) for verb in optional.choices}
    # An OPTIONAL positional that IS the CLI's subcommand slot (`dest ==
    # "subcommand"`, `nargs="?"`) leaves the BARE invocation valid too --
    # verification.py's rotation check beside its `window` subcommand. A
    # positional named `action`/`mode`/`cmd` carries a non-None default whose
    # bare form is that default, not a new verb, and is not a subcommand slot.
    if optional.nargs == "?" and optional.dest == "subcommand":
        out[""] = _arg_dests(top)
    return out


@pytest.mark.parametrize("cli", _LISTED_CLIS)
def test_every_listed_cli_verb_is_declared_or_excluded(cli, monkeypatch):
    """Falsifier: a verb of a listed CLI neither declared nor excluded."""
    _, man = _live_manifest()
    declared = {k.split(":", 1)[1] for k in man if k.startswith(cli + ":")}
    introspected = set(_introspect_cli(cli, monkeypatch,
                                       require_parser=cli not in _PARSERLESS_CLIS))
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
    dests = _introspect_cli(cli, monkeypatch,
                            require_parser=cli not in _PARSERLESS_CLIS)
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
    """One pass only: a value containing a NON-kept placeholder is never
    re-scanned and lands verbatim, and a key that is not a declared arg
    substitutes nothing.

    `<foo>`/`<div>` are deliberately absent from `KEPT_METAVARS`: an earlier
    resolver scanned the SUBSTITUTED OUTPUT, so it could not tell a template
    placeholder from caller data and refused this."""
    root, _ = _live_manifest()
    argv = commands.propose(root, "write.py:set",
                            {"key": "title",
                             "value": "<foo> and <div>x</div>",
                             "engine": "BAD"})
    joined = " ".join(argv)
    assert "BAD" not in joined, joined
    assert "<foo> and <div>x</div>" in joined, joined


def test_propose_refuses_an_unmapped_placeholder(tmp_path: Path):
    """A template still holding a placeholder no declared arg maps must
    refuse by name rather than hand back an argv a proposer cannot run.

    Red-on-prefix: the refusal is read off the TEMPLATE, so a caller value
    shaped like `<N:M>` does not."""
    graph = _synthetic(tmp_path, "<N:M>")
    with pytest.raises(commands.CommandError) as exc:
        commands.propose(graph, "x.py:slice", {"target": "body"})
    assert "unmapped placeholder" in str(exc.value)
    assert "<N:M>" in str(exc.value)


def test_propose_refuses_a_required_arg_with_nowhere_to_land(tmp_path: Path):
    """A declared arg with no `<name>` in the template and NO `placement`
    declared is a drop -- it must refuse by name, not return the argv.

    A graph that has not opted into `placement: {defaults: true}` gets no
    guessed flag, so the refusal still fires."""
    graph = _synthetic(tmp_path, "")
    with pytest.raises(commands.CommandError) as exc:
        commands.propose(graph, "x.py:go", {"wanted": "v"})
    assert "cannot place arg" in str(exc.value)
    assert "wanted" in str(exc.value)


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

# --------------------------------------------------------------------------
# Optional args: `propose` places them from the node's `placement` data, and
# a drift test introspects each CLI's OWN argparse at test time.
# --------------------------------------------------------------------------

def test_propose_places_an_optional_flag_from_the_node():
    """`back` has no `<back>` in `grid.py:diff`'s argv; the node's `placement`
    default places it as grid.py's own `--back <value>`."""
    root, _ = _live_manifest()
    argv = commands.propose(root, "grid.py:diff",
                            {"node_id": "x", "back": "2"})
    assert argv[-2:] == ["--back", "2"], argv


def test_propose_places_an_optional_bool_switch_only_when_true():
    """A bool becomes its CLI switch when true, and is omitted when false or
    absent -- never `--box-local False`."""
    root, _ = _live_manifest()
    on = commands.propose(root, "send.py:read",
                          {"target": "local-town", "box_local": True})
    off = commands.propose(root, "send.py:read",
                           {"target": "local-town", "box_local": False})
    assert "--box-local" in on, on
    assert "--box-local" not in off, off


def test_propose_places_a_declared_const_pair():
    """A `store_const` pair places the flag its value selects: `record: fail`
    becomes `--record-fail`, never `--record-record fail`."""
    root, _ = _live_manifest()
    argv = commands.propose(root, "rotate.py:next",
                            {"seat": "s", "record": "fail"})
    assert "--record-fail" in argv, argv
    ok = commands.propose(root, "rotate.py:next",
                          {"seat": "s", "record": "ok"})
    assert "--record-ok" in ok, ok


def test_propose_places_every_value_of_a_multi_value_option(tmp_path):
    """Falsifier: a `nargs='+'` option supplied N values. Pre-fix `propose`
    emitted ONE token (`str(['a','b','c'])`); every value must appear as its
    own argv token after the flag."""
    graph = _synthetic_multi(
        tmp_path, "  owns: {kind: option, flag: \"--owns\", arity: many}\n")
    argv = commands.propose(graph, "x.py:go", {"owns": ["a", "b", "c"]})
    assert argv[-4:] == ["--owns", "a", "b", "c"], argv


def test_propose_repeats_the_flag_for_an_append_option(tmp_path):
    """`action='append'` needs the flag per value: `--owns a --owns b`."""
    graph = _synthetic_multi(
        tmp_path, "  owns: {kind: option, flag: \"--owns\", arity: append}\n")
    argv = commands.propose(graph, "x.py:go", {"owns": ["a", "b"]})
    assert argv[-4:] == ["--owns", "a", "--owns", "b"], argv


def test_propose_places_exactly_n_values_or_refuses(tmp_path):
    """A fixed `nargs=2` places two values and REFUSES a wrong count."""
    graph = _synthetic_multi(
        tmp_path, "  owns: {kind: option, flag: \"--owns\", arity: \"2\"}\n")
    assert commands.propose(
        graph, "x.py:go", {"owns": ["a", "b"]})[-3:] == ["--owns", "a", "b"]
    with pytest.raises(commands.CommandError) as exc:
        commands.propose(graph, "x.py:go", {"owns": ["a", "b", "c"]})
    assert "needs 2 values" in str(exc.value)


def test_propose_refuses_multiple_values_with_no_declared_arity(tmp_path):
    """The pre-fix silent drop: a list for an arg whose placement declares no
    arity was stringified into ONE token. It must refuse by name instead."""
    graph = _synthetic_multi(tmp_path)
    with pytest.raises(commands.CommandError) as exc:
        commands.propose(graph, "x.py:go", {"owns": ["a", "b"]})
    assert "owns" in str(exc.value) and "arity" in str(exc.value)


def _full_supply(key, entry, rules):
    """One value for every declared arg, EXACTLY as many as the node's own
    placement arity demands (`nargs=2` needs two, `append:2` needs two) -- so
    the full-supply falsifiers stay valid once arity data lands."""
    args = {}
    for arg in entry.get("args") or []:
        choices = arg.get("choices") or []
        base = (True if arg.get("type") == "bool"
                else (choices[0] if choices
                      else f"SYNTH{len(args)}x{arg['name']}"))
        placed = commands._resolve_placement(arg["name"], arg, key, rules)
        mode, size = commands._split_arity(placed[4] if placed else None)
        args[arg["name"]] = ([f"{base}{i}" for i in range(size)]
                              if mode == "nargs"
                              or (mode == "append" and size > 1) else base)
    return args


def test_every_proposable_entry_accepts_a_full_supply_of_its_args():
    """Falsifier: a declared arg, required or optional, that `propose` cannot
    place. Supplies every declared arg of every proposable entry and asserts
    the result is a complete argv -- no refusal, no surviving placeholder."""
    root, man = _live_manifest()
    rules = commands._load_node(root).get("placement") or {}
    for key, entry in man.items():
        if not entry.get("proposable"):
            continue
        args = _full_supply(key, entry, rules)
        try:
            argv = commands.propose(root, key, args)
        except commands.CommandError as exc:
            pytest.fail(f"{key}: refused a fully-supplied proposal: {exc}")
        assert not [t for t in argv
                    if any(p not in commands.KEPT_METAVARS
                           for p in commands._PLACEHOLDER_RE.findall(t))], \
            (key, argv)


def test_every_proposable_entry_lands_every_supplied_value_or_refuses_by_name():
    """Falsifier: a supplied declared arg that is SILENTLY DROPPED. Supplies a
    distinct value for every declared arg of every proposable entry and asserts
    each value either lands in the returned argv or the call refused by NAMING
    it."""
    root, man = _live_manifest()
    rules = commands._load_node(root).get("placement") or {}
    drops = []
    for key, entry in man.items():
        if not entry.get("proposable"):
            continue
        args = _full_supply(key, entry, rules)
        try:
            argv = commands.propose(root, key, args)
        except commands.CommandError as exc:
            if not any(n in str(exc) for n in args):
                drops.append((key, "refusal names no arg", str(exc)))
            continue
        joined = " ".join(argv)
        for name, value in args.items():
            for v in (value if isinstance(value, list) else [value]):
                if isinstance(v, bool):
                    continue
                if str(v) not in joined:
                    drops.append((key, name, v, argv))
    assert drops == [], drops


def test_operator_verbs_are_declared_not_proposable_with_a_reason():
    """A proposer must never be handed the verbs that write the real crontab /
    systemd units, nor owner-ops `mesh-gw`. Each is declared by name with a
    non-empty reason, so the choice surface says WHY it is off the table."""
    _, man = _live_manifest()
    for key in ("crons.py:apply", "crons.py:remove", "mesh-gw"):
        assert man[key]["proposable"] is False, key
        assert man[key].get("reason"), key


_BOX_LABELS = ("GPU2070S", "ARM4C", "CPU8G", "EDGE")


def test_rendered_manifest_names_no_box_detail():
    """The anonymize guard goes over the WHOLE rendered manifest, purposes
    included: no box label, no dotted-quad address. The mesh purposes used to
    name the physical rig they run on."""
    root, _ = _live_manifest()
    text = commands.render_manifest(root)
    hits = [tok for tok in _BOX_LABELS if tok in text]
    hits += ["ip:" + m
             for m in re.findall(r"\b\d{1,3}(?:\.\d{1,3}){3}\b", text)]
    assert hits == [], hits


def test_propose_never_imports_a_cli_or_touches_argparse(monkeypatch):
    """`propose` places from DATA: it must not import/exec a CLI or call
    argparse. A parse_args monkeypatched to raise is never reached, and no CLI
    script enters `sys.modules`."""
    import argparse
    root, _ = _live_manifest()

    def boom(*a, **k):
        raise AssertionError("propose must never parse args")

    monkeypatch.setattr(argparse.ArgumentParser, "parse_args", boom)
    before = set(sys.modules)
    argv = commands.propose(root, "grid.py:diff",
                            {"node_id": "x", "back": "2"})
    assert argv[-2:] == ["--back", "2"], argv
    new = [m for m in set(sys.modules) - before
           if m.rsplit(".", 1)[-1] in
           ("grid", "send", "cli", "rotate", "crons", "workflow")]
    assert new == [], new


# --------------------------------------------------------------------------
# Drift: introspect each CLI's own argparse AT TEST TIME, and fail when the
# node's declared/default placement disagrees. Import/exec is fine HERE; it is
# forbidden in `propose`.
# --------------------------------------------------------------------------

class _ArgsCaptured(BaseException):
    pass


_SPEC_CACHE: dict[str, dict] = {}


def _cli_arg_specs(entry: dict) -> dict:
    """`{dest: [(kind, token, const)]}` from the CLI's own argparse, cached by
    script path. The parser is captured by replacing `parse_args` with a spy
    that raises before any subcommand runs."""
    import argparse
    import contextlib
    import importlib.util
    import inspect
    import io
    argv = [str(a) for a in entry["argv"]]
    script = next((a for a in argv if a.endswith((".py", ".sh"))), "")
    if not script:
        return {}
    path = Path(script.replace("<engine>/", ""))
    if not path.is_absolute():
        path = BIN / path.name
    key = str(path)
    verb = next((a for a in argv[argv.index(script) + 1:]
                 if not a.startswith("-")), "")
    key = f"{path}|{verb}"
    if key in _SPEC_CACHE:
        return _SPEC_CACHE[key]
    seen: dict = {}

    def spy(self, *a, **k):
        seen.setdefault("top", self)
        raise _ArgsCaptured()

    old = (argparse.ArgumentParser.parse_args,
           argparse.ArgumentParser.parse_known_args)
    argparse.ArgumentParser.parse_args = spy
    argparse.ArgumentParser.parse_known_args = spy
    try:
        _drive_module(path, "_drift_probe", False)
        if "top" not in seen:
            # The parser was built ONLY under `if __name__ == "__main__"`.
            _drive_module(path, "_drift_probe_main", True)
    finally:
        argparse.ArgumentParser.parse_args, \
            argparse.ArgumentParser.parse_known_args = old
        sys.modules.pop("_drift_probe", None)
        sys.modules.pop("_drift_probe_main", None)
    top = seen.get("top")
    assert top is not None, f"{path.name}: main() never built a parser"
    for act in getattr(top, "_actions", []):
        if isinstance(act, argparse._SubParsersAction) and verb in act.choices:
            top = act.choices[verb]
            break
    out: dict = {}
    for act in getattr(top, "_actions", []):
        if act.dest == "help":
            continue
        ar = _cli_arity(act)
        if act.option_strings:
            long = [o for o in act.option_strings if o.startswith("--")]
            token = (long or act.option_strings)[0]
            if type(act).__name__ == "_StoreConstAction":
                item = ("const", token, act.const, ar)
            elif act.nargs == 0:
                item = ("switch", token, None, ar)
            else:
                item = ("option", token, None, ar)
        else:
            item = ("positional", "", None, ar)
        out.setdefault(act.dest, []).append(item)
    _SPEC_CACHE[key] = out
    return out


def _cli_arity(act) -> str | None:
    """Canonical arity of one argparse action: `many` for `nargs='+'/'*'`,
    `append:1`/`append:N` for `action='append'`, `"N"` for a fixed `nargs=N`,
    None for a single value."""
    import argparse
    if isinstance(act, argparse._AppendAction):
        return f"append:{act.nargs}" if isinstance(act.nargs, int) else "append:1"
    if act.nargs in ("+", "*"):
        return "many"
    if isinstance(act.nargs, int) and act.nargs > 1:
        return str(act.nargs)
    return None


def _arity_key(arity) -> str | None:
    """The SAME canonical vocabulary as `_cli_arity`, from a placement's own
    `arity` spelling -- `many`, `append`/`append:N`, `"N"`, or None."""
    mode, size = commands._split_arity(arity)
    return {"many": "many", "append": f"append:{size}",
            "nargs": str(size)}.get(mode)


def _norm_token(value) -> str:
    return re.sub(r"[-_]", "", str(value).lstrip("-")).lower()


def _match_spec(specs: dict, name: str):
    """The CLI items for a declared arg, by dest or by any option spelling --
    `parent` finds `--parent`, whose dest is `parents`."""
    if name in specs:
        return specs[name]
    want = _norm_token(name)
    for dest, items in specs.items():
        if _norm_token(dest) == want:
            return items
        for _kind, token, _const, _ar in items:
            if token and _norm_token(token) == want:
                return items
    return None


def _drift_problems(man: dict, rules: dict) -> list:
    """Every proposable entry whose declared placement disagrees with the
    CLI's own argparse -- flag, kind, consts, and (only where the node
    DECLARES one) arity. `propose` never runs this; the test does."""
    bad = []
    for key, entry in man.items():
        if not entry.get("proposable"):
            continue
        template = " ".join(str(t) for t in entry["argv"])
        need = [a for a in entry.get("args") or []
                if f"<{a['name']}>" not in template]
        if not need:
            continue
        specs = _cli_arg_specs(entry)
        for arg in need:
            items = _match_spec(specs, arg["name"])
            placed = commands._resolve_placement(arg["name"], arg, key, rules)
            if items is None or placed is None:
                bad.append((key, arg["name"], "no CLI spec" if items is None
                            else "no placement", items, placed))
                continue
            kind, flag, const, consts, arity = placed
            live = ([ar for k, _t, _c, ar in items if k == kind]
                    if kind in ("positional", "const")
                    else [ar for k, t, _c, ar in items
                          if k == kind and t == flag])
            if not live:
                bad.append((key, arg["name"], f"expected {kind} {flag}", items))
            elif kind == "const":
                got = {str(c): t for k, t, c, _ar in items if k == "const"}
                if got != {str(v): t for v, t in consts.items()}:
                    bad.append((key, arg["name"], "const mismatch", items,
                                consts))
            elif arity is not None and live[0] != _arity_key(arity):
                bad.append((key, arg["name"],
                            f"arity {_arity_key(arity)} != {live[0]}", items))
    return bad


def test_declared_placement_matches_each_cli_introspected_at_test_time():
    """For every proposable entry and every declared arg that lacks a `<name>`,
    introspect the CLI's argparse and assert the node's placement (default or
    declared) matches it. A renamed flag, or a declared arity the CLI does not
    have, fails HERE, not silently at propose time. Arity is pinned only where
    the node declares one -- an entry with no arity data is not yet migrated."""
    root, man = _live_manifest()
    rules = commands._load_node(root).get("placement") or {}
    bad = _drift_problems(man, rules)
    assert bad == [], bad


def test_drift_catches_a_declared_arity_the_cli_does_not_have(tmp_path):
    """The arity pin is real, not decorative: introspect a CLI whose `--owns`
    is `nargs='+'`, and report a node that declares `arity: \"2\"`. A declared
    arity no CLI has is caught HERE, at test time."""
    cli = tmp_path / "probe_cli.py"
    cli.write_text(
        "import argparse\n"
        "def main():\n"
        "    ap = argparse.ArgumentParser()\n"
        "    ap.add_argument('--owns', nargs='+', default=None)\n"
        "    ap.parse_args()\n")
    entry = {"cli": "probe_cli.py", "verb": "go",
             "argv": ["python3", str(cli), "go"],
             "args": [{"name": "owns", "type": "str", "required": False,
                       "choices": []}],
             "proposable": True}
    assert _match_spec(_cli_arg_specs(entry), "owns") == \
        [("option", "--owns", None, "many")]
    good = {"owns": {"kind": "option", "flag": "--owns", "arity": "many"}}
    assert _drift_problems({"x.py:go": entry}, good) == []
    wrong = {"owns": {"kind": "option", "flag": "--owns", "arity": "2"}}
    got = _drift_problems({"x.py:go": entry}, wrong)
    assert got and "arity" in got[0][2], got


# --------------------------------------------------------------------------
# Coverage of the survey itself: no engine CLI may slip in unlisted
# --------------------------------------------------------------------------

#: Engine CLIs deliberately OUTSIDE the choice-surface survey, each with the
#: reason it is not a choice. A bin/*.py with a `__main__` block that is in
#: neither this map, `_LISTED_CLIS`, nor write.py fails
#: `test_every_engine_cli_is_listed_write_py_or_named_outside` below.
_OUTSIDE_CLIS = {
    "analyze-chat-structure.py": "one-off transcript analysis, not an engine verb",
    "snapshot-build-site.py": "retired build-site generator; its inputs are gone and must not return",
}


def test_every_engine_cli_is_listed_write_py_or_named_outside():
    """Falsifier: a `bin/*.py` with a `__main__` block the survey never
    reached. Every engine CLI is either listed in `_LISTED_CLIS` (and so has
    its verbs read off its own argparse by the coverage test), is `write.py`
    (covered by its own `VERBS` drift test), or is named in `_OUTSIDE_CLIS`
    with a reason. Red on the pre-fix bytes: `verification.py` and
    `write_guard.py` had a `__main__` block and no entry at all."""
    covered = set(_LISTED_CLIS) | {"write.py"} | set(_OUTSIDE_CLIS)
    missed = sorted(
        p.name for p in BIN.glob("*.py")
        if "__main__" in p.read_text(encoding="utf-8") and p.name not in covered
    )
    assert missed == [], (
        "engine CLIs with a `__main__` block and no entry in the choice "
        f"surface survey: {missed}; add each to _LISTED_CLIS or "
        f"_OUTSIDE_CLIS with a reason")


# --------------------------------------------------------------------------
# The operator verbs off the choice surface: suite, stamp, ring, hook
# --------------------------------------------------------------------------

_OPERATOR_FLAG_TOKENS = ("--suite", "--stamp")


def test_no_suite_stamp_ring_or_hook_verb_is_proposable():
    """Falsifier: a proposable entry whose stored argv demands the engine
    suite, stamps the never-lower baseline, signs a ring, or installs the
    write-guard hook. The choice surface must not offer any of them.

    Red on the pre-fix bytes: the legacy `verify-suite` entry was proposable
    with `--suite` in its argv."""
    _, man = _live_manifest()
    bad = []
    for key, entry in man.items():
        if not entry.get("proposable"):
            continue
        argv = [str(t) for t in entry["argv"]]
        if any(t in _OPERATOR_FLAG_TOKENS for t in argv):
            bad.append(key)
        elif any(t.startswith("--ring-") for t in argv):
            bad.append(key)
        elif (any(t.endswith("write_guard.py") for t in argv)
              and "hook" in argv):
            bad.append(key)
    assert bad == [], bad


def test_legacy_verification_names_resolve_and_the_suite_is_refused():
    """The legacy `verify` / `verify-suite` / `write-guard` names keep
    resolving -- the commands they name still exist -- while the suite variant
    is refused by `propose` with its reason and `propose` imports nothing."""
    root, man = _live_manifest()
    for legacy in ("verify", "verify-suite", "write-guard"):
        assert legacy in commands.load(root), legacy
    for key in ("verification.py:", "verification.py:window", "verify-suite"):
        assert man[key]["proposable"] is False, key
        assert man[key].get("reason"), key
    with pytest.raises(commands.CommandError) as exc:
        commands.propose(root, "verify-suite", {})
    assert "not proposable" in str(exc.value)
    # The read-only check still resolves to a complete argv.
    assert commands.propose(root, "write-guard", {})[-1] == "check"
