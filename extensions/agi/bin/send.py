#!/usr/bin/env python3
"""RETIRED (gate-t / goal:g7.16.1.11.11.2.1.1) — live send.py shim MOVEd aside.

Team mail SoT is `box` only (`box send` / `box read` / stdin).
Archival bytes: extensions/agi/deprecated/bin/send.py (PRESENT; never git rm).
Aside of former live shim: extensions/agi/deprecated/bin/send-live-shim-aside-gate-t-20261006.py

This stub FAILS CLOSED and does NOT load deprecated as mail SoT.
"""
from __future__ import annotations

import sys

_MSG = (
    "send.py live path retired (gate-t / AA1). Mail SoT is `box` "
    "(box send / box read). Deprecated archival stays at "
    "extensions/agi/deprecated/bin/send.py — not mail SoT."
)

if __name__ == "__main__":
    print(_MSG, file=sys.stderr)
    raise SystemExit(2)

raise ImportError(_MSG)
