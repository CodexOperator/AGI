#!/usr/bin/env python3
"""row_settings.py -- the ONE seat-row `settings` parser and tmux default.

Pure library (no `__main__`, no argparse). Lifted byte-for-byte out of
`rotate.py` so `send.py` can read a row's quiet / quiet-system tokens and its
nudge tmux session without importing rotate at all (goal:g7.32.4 clause (1)).
`rotate.py` imports these names back, so every
`rotate._normalize_settings` / `rotate.DEFAULT_TMUX_SESSION` /
`rotate.SETTINGS_ALIASES` reference still resolves to exactly this copy.
"""
from __future__ import annotations

import json

#: Default tmux session for remote-control.
DEFAULT_TMUX_SESSION = "agi-rc"

#: The roles table spells a settings bundle by its NAME for the CC tiers
#: (e.g. `settings: ultracode`). "Ultracode" is not an effort level -- it is a
#: settings flag -- so a bare word is resolved here to the flag object the
#: claude adapter passes as `--settings '{"ultracode":true}'`.
SETTINGS_ALIASES = {
    "ultracode": {"ultracode": True},
    "quiet": {"quiet": True},
    # a row that keeps post dm nudges but never a service-class one
    "quiet-system": {"quiet_system": True},
}


def normalize_settings(val):
    """A settings cell -> dict or None: dict as-is, or a space-separated
    token list / JSON object string resolved via SETTINGS_ALIASES (words
    MERGE, so `quiet` composes with `ultracode`)."""
    if val is None or val == "":
        return None
    if isinstance(val, dict):
        return val if val else None
    if not isinstance(val, str):
        return None
    s = val.strip()
    if not s:
        return None
    if s.startswith("{"):
        try:
            parsed = json.loads(s)
        except Exception:                                     # noqa: BLE001
            return None
        return parsed if isinstance(parsed, dict) and parsed else None
    out: dict = {}
    for tok in s.lower().split():
        alias = SETTINGS_ALIASES.get(tok)
        if alias:
            out.update(alias)
    return out or None
