"""The file that OWNS live-config cell declarations.

`hypothesis:rotate-term-grace-tests-never-touch-a-real-process-or-the-live-
config` moved `test_live_config_declares_the_cell` out of
test_rotate_term_grace.py and into here. The rule that follows from the move
is the point of this file: exactly ONE place in the suite reads the live
`.agi/config.json`, so a test can be a fixture-only file AND still assert
that a cell is really declared — and every other file is free to claim "no
live config" honestly, which is now MECHANICALLY TRUE (conftest's
`_no_real_process_or_live_config` guard fails any opted-in module that opens
a live `.agi/config.json` outside tmp_path).

A live read is a read of the live node, never of a copied list: if a cell is
removed from the real config, this goes red and the feature's declared
default is not the live one.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

BIN = Path(__file__).resolve().parents[1] / "bin"

#: The engine checkout that OWNS the live `.agi/config.json` — resolved by
#: rotate.py's OWN resolver (rot.ENGINE_ROOT), never a literal path.
_spec = importlib.util.spec_from_file_location(
    "rotate_for_live_cells", BIN / "rotate.py")
rot = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(rot)
ENGINE_ROOT = rot.ENGINE_ROOT


def test_live_config_declares_the_term_grace_cell():
    """`reaper.term_grace_s` is in the REAL .agi/config.json, not only in a
    fixture: the absent-argument case resolves it at runtime, so the live
    value is what an operator actually gets."""
    cfg = json.loads((ENGINE_ROOT / ".agi" / "config.json").read_text(
        encoding="utf-8"))
    assert cfg["reaper"]["term_grace_s"] == 15.0
