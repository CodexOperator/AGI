#!/usr/bin/env python3
"""Shim — AA1 MOVE: real module is extensions/agi/deprecated/bin/send.py (never git rm)."""
from __future__ import annotations
import importlib.util
import sys
from pathlib import Path

_BIN = Path(__file__).resolve().parent
_SRC = _BIN.parent / "src"
_PATH = _BIN.parent / "deprecated" / "bin" / "send.py"
for _p in (str(_BIN), str(_SRC)):
    if _p not in sys.path:
        sys.path.insert(0, _p)
_spec = importlib.util.spec_from_file_location("_agi_send_deprecated", _PATH)
if _spec is None or _spec.loader is None:
    raise ImportError(f"AA1 shim: cannot load {_PATH}")
_mod = importlib.util.module_from_spec(_spec)
sys.modules["_agi_send_deprecated"] = _mod
_spec.loader.exec_module(_mod)
sys.modules["send"] = _mod
sys.modules[__name__] = _mod
globals().update({k: v for k, v in _mod.__dict__.items() if k not in ("__name__", "__file__", "__package__", "__loader__", "__spec__")})
