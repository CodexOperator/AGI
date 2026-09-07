---
id: mvp:a01-e989877e-4030c2
mint_id: 7b7d21d7e2274a4ca14da0beee67f2c5
type: mvp
parents:
  - verdict:the-verb-layer-holds
next_edges: []
confidence: 0.8
edited_by: season.py
scaffold_hash: 3cb49a2477d9dd7a
season: 1
thought_session: season
title: A01 e989877e 4030c2
verdict: pending
---
# mvp:a01-e989877e-4030c2

## MVP

**Verb registry and meta-contract** — a discoverable, testable interface between the verb layer and the modal shell.

`verdict:the-verb-layer-holds` proved the verbs are sound and built in the right order. The sibling `mvp:the-modal-shell-over-the-verbs` says *"Every key maps to a nameable verb, and every verb is reachable by name"* — but the shell currently imports `write.VERBS` as a raw dict, with no mechanism to:
- List verbs and their metadata (arity, docstring, argument types)
- Validate a verb name at binding time (not at runtime on keypress)
- Check bijection: the keymap and the verb registry agree on what exists
- Assert every verb still satisfies the NO write invariant

This MVP defines a **`VerbRegistry`** that wraps the dict and provides reflection, validation, and a contract test that any new verb must pass.

### Implementation sketch

```python
# bin/verb_registry.py (new) — or merge into write.py as `VerbRegistry` class

from __future__ import annotations

import ast
import inspect
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable


@dataclass(frozen=True)
class VerbSpec:
    """The contract a verb must satisfy."""
    name: str
    arity: int                     # declared argument count
    doc: str                       # first line of the function's docstring
    fn: Callable                   # the implementation
    modifies_body: bool = False    # thought/note touch body_append or thought
    modifies_fm: bool = True       # set/unset/link touch frontmatter


@dataclass
class VerbRegistry:
    """Discoverable verb map with introspection."""
    verbs: dict[str, VerbSpec] = field(default_factory=dict)

    @classmethod
    def from_write_module(cls) -> "VerbRegistry":
        """Reflect over `write.VERBS` and `write.ARITY` to build the registry.

        This is the ONE place the shell imports from. Every other consumer
        goes through the registry, never the raw dict.
        """
        import write as _write
        reg = cls()
        for name, fn in _write.VERBS.items():
            arity = _write.ARITY.get(name, 1)
            doc = (fn.__doc__ or "").partition("\n")[0].strip()
            modifies_body = name in ("thought", "note")
            reg.verbs[name] = VerbSpec(
                name=name, arity=arity, doc=doc, fn=fn,
                modifies_body=modifies_body,
            )
        return reg

    def exists(self, name: str) -> bool:
        return name in self.verbs

    def spec(self, name: str) -> VerbSpec | None:
        return self.verbs.get(name)

    def all(self) -> list[VerbSpec]:
        """Sorted by name for deterministic iteration."""
        return [self.verbs[k] for k in sorted(self.verbs)]

    def names(self) -> set[str]:
        return set(self.verbs)

    def keymap_complete(self, keymap: dict[str, str]) -> bool:
        """Check every key in a keymap resolves to a real verb (bijection).

        Used by the modal shell at load time to reject a dead binding before
        any keystroke arrives.
        """
        return all(self.exists(v) for v in keymap.values())
```

### Contract tests (the falsifier)

A test that imports the registry and asserts:

```python
def test_registry_covers_every_verb():
    """VERBS dict and registry agree; no verb is undiscoverable."""
    import write
    reg = VerbRegistry.from_write_module()
    assert set(reg.names()) == set(write.VERBS)
    assert set(reg.names()) == set(write.ARITY)


def test_registry_arity_matches_write():
    reg = VerbRegistry.from_write_module()
    import write
    for name, spec in reg.verbs.items():
        assert spec.arity == write.ARITY[name], f"{name}: arity mismatch"


def test_every_verb_has_a_docstring():
    reg = VerbRegistry.from_write_module()
    for spec in reg.all():
        assert spec.doc, f"{spec.name}: no docstring"


def test_a_keymap_that_resolves_to_real_verbs_passes_validation():
    reg = VerbRegistry.from_write_module()
    keymap = {"s": "set", "u": "unset", "n": "note"}
    assert reg.keymap_complete(keymap)


def test_a_keymap_with_a_bogus_verb_is_rejected():
    reg = VerbRegistry.from_write_module()
    keymap = {"x": "nonexistent"}
    assert not reg.keymap_complete(keymap)
```

## Inputs

- `write.py`'s `VERBS` dict and `ARITY` dict — the source of truth for what verbs exist.
- A keymap from the modal shell — keys mapped to verb names, validated at bind time.

## Outputs

- `VerbRegistry` object with `exists()`, `spec()`, `all()`, `names()`, `keymap_complete()`.
- A bijection check: every key in the shell's keymap resolves to a real verb, and every verb is bound to at least one key (configurable; `keymap_complete` validates one direction, the shell asserts coverage).
- Contract tests that fail as soon as a new verb is added without registry registration or arity declaration.

## Invariants

1. **The registry is derived, never authored.** It reflects `write.VERBS` and `write.ARITY` at import time. A new verb added to `write.py` appears in the registry automatically — no separate registration step.
2. **The shell never imports `write.apply_verb` directly.** It goes through the registry, so binding validation happens before any verb runs. A dead key is a compile-time error, not a runtime `EditError`.
3. **`keymap_complete` is a soft gate** — it warns at shell startup and refuses to bind, but does not crash. A missing verb in the keymap is a configuration gap, not a corrupt state.
4. **The no-file-write invariant is enforced at the registry level too.** A verb whose implementation writes to a file is caught by the same AST parse that the sibling `test_edit_py_contains_no_file_write` already runs.
5. **The registry is pure Python — no config files, no dsl.** `from_write_module()` is the only factory.

## What proves this MVP works

1. `VerbRegistry.from_write_module()` returns a registry with exactly 5 verbs (set, unset, link, thought, note) — the same 5 the verdict proved.
2. Each verb's spec has the correct arity matching `write.ARITY`.
3. A keymap with keys bound to real verbs passes `keymap_complete`.
4. A keymap with a nonexistent verb name fails `keymap_complete`.
5. The full test suite passes with these contract tests added.
6. The modal shell (sibling MVP) loads and validates its keymap through the registry before accepting input.

## What is NOT this

- **Not a new verb.** No `create`, `delete`, `move`, or any operation the layer doesn't already have.
- **Not a runtime** or a dispatch loop. The registry is read at import time and never changes during a session.
- **Not a CLI.** The shell calls the registry; a human never does.
- **Not the keymap itself.** Which keys map to which verbs is the shell's decision. The registry only validates that every target exists.

## The falsifier


A new verb added to `write.py` without an `ARITY` entry or without the registry reflecting it fails the contract tests, and the shell silently binds a dead key. The falsifier is a verb that is callable but not discoverable through the registry — the exact split `goal:g9.7` forbids. The contract tests catch it before the shell ever loads.


## Agent Notes
Verb registry MVP: discoverable interface between verb layer and modal shell. Defines VerbSpec/VerbRegistry with introspection, keymap validation, and contract tests that catch a verb added without ARITY or registry coverage.