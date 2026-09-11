#!/usr/bin/env python3
"""reaper_log.py — the ONE resolver for the per-event reaper log line.

heal.py's `_watch_log` and send.py's `wake` outcome line share this single
resolver so a second log path never appears (clause (3) of
hypothesis:l4-a-strand-is-only-a-line-inside-a-rendered-input-box-and-wake-
names-its-path: through the SAME resolver, never a second path).

Resolver: `AGI_REAPER_LOG` env when set, else stderr. Tests point
AGI_REAPER_LOG at a tmp path so they never touch a real log; the unit (the
systemd service) sets it in Environment= or lets it default.

This is a MOVE of heal.py's `_watch_log` body to a shared module, not a
behaviour change. heal.py's `_watch_log` now delegates here so that every
per-event line — the watcher's own `watch:` lines and the one `wake:` outcome
line — lands in the same file, in the same dir+hash style.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path


def log(line: str) -> None:
    """Write ONE line to the reaper log, or to stderr when the log is not
    overridable / unwritable (best-effort, never raises)."""
    log = os.environ.get("AGI_REAPER_LOG")
    if log:
        try:
            p = Path(log)
            p.parent.mkdir(parents=True, exist_ok=True)
            with open(p, "a", encoding="utf-8") as fh:
                fh.write(line.rstrip("\n") + "\n")
            return
        except Exception as exc:                          # noqa: BLE001
            print(f"reaper: log write failed ({exc}); "
                  f"falling back to stderr", file=sys.stderr)
    print(line, file=sys.stderr)