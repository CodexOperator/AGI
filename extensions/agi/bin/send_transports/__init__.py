"""goal:g7.32.4 falsifier 2 — transport discovery.

Dropping a module into this directory that defines
``register(register_delivery, helpers)`` registers its transport at
startup. send.py is never edited, and never imports the module, to admit a
new transport; ``discover`` scans the directory and calls each module's
``register``. Idempotent per registry (a resolved file path already seen by
*this* ``register_delivery`` is skipped -- no double registration on
re-import/reload), and ``directory`` is overridable so a test can point it at
a throwaway dir.
"""
from __future__ import annotations

import importlib.util
from pathlib import Path

_DIR = Path(__file__).resolve().parent


def _load(path: Path):
    spec = importlib.util.spec_from_file_location(
        f"send_transport_{path.stem}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def discover(register_delivery, helpers, directory=None) -> list:
    """Import every non-underscore ``*.py`` in *directory* (default: this
    one) and call its ``register(register_delivery, helpers)``. Returns the
    module stems loaded this call; a path already seen by this registry is
    skipped."""
    directory = Path(directory) if directory else _DIR
    seen = register_delivery.__dict__.setdefault("_discovered_paths", set())
    loaded = []
    for path in sorted(directory.glob("*.py")):
        if path.stem.startswith("_"):
            continue
        key = str(path.resolve())
        if key in seen:
            continue
        _load(path).register(register_delivery, helpers)
        seen.add(key)
        loaded.append(path.stem)
    return loaded