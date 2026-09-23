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
