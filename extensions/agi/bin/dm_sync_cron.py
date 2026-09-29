#!/usr/bin/env python3
"""dm_sync_cron.py — ONE per-box DM sync cron; interval config cell (g7.32.6.3).

Owner design (goal:g7.32.6 design line 3): ONE cron per box; a config cell
at 1-3 min (start at 3). The cron finds posts local to this box and syncs
only their dms from each post's remote head.

Public API
----------
CONFIG_PATH cells (first hit wins):
  values.dm.sync_interval_min
  comms.dm_sync_interval_min

DEFAULT_INTERVAL_MIN = 3
MIN_INTERVAL_MIN = 1
MAX_INTERVAL_MIN = 3

interval_minutes(config) -> int
interval_seconds(config) -> int
ensure_config_cell(config) -> dict
    Return a COPY of config with the cell present (default 3) when absent.
"""
from __future__ import annotations

import copy
from typing import Any

DEFAULT_INTERVAL_MIN = 3
MIN_INTERVAL_MIN = 1
MAX_INTERVAL_MIN = 3


def _read_raw(config: dict | None) -> Any:
    if not isinstance(config, dict):
        return None
    values = config.get("values")
    if isinstance(values, dict):
        dm = values.get("dm")
        if isinstance(dm, dict) and "sync_interval_min" in dm:
            return dm.get("sync_interval_min")
    comms = config.get("comms")
    if isinstance(comms, dict) and "dm_sync_interval_min" in comms:
        return comms.get("dm_sync_interval_min")
    return None


def interval_minutes(config: dict | None = None) -> int:
    """Return the sync interval in minutes; default 3; refuse out of [1,3]."""
    raw = _read_raw(config)
    if raw is None or raw == "":
        return DEFAULT_INTERVAL_MIN
    try:
        n = int(raw)
    except (TypeError, ValueError) as exc:
        raise ValueError(
            f"dm_sync_cron: sync_interval_min must be int in "
            f"[{MIN_INTERVAL_MIN},{MAX_INTERVAL_MIN}], got {raw!r}"
        ) from exc
    if n < MIN_INTERVAL_MIN or n > MAX_INTERVAL_MIN:
        raise ValueError(
            f"dm_sync_cron: sync_interval_min={n} out of "
            f"[{MIN_INTERVAL_MIN},{MAX_INTERVAL_MIN}] — refuse by name"
        )
    return n


def interval_seconds(config: dict | None = None) -> int:
    return interval_minutes(config) * 60


def ensure_config_cell(config: dict | None) -> dict:
    """COPY of config with values.dm.sync_interval_min set (default 3)."""
    out = copy.deepcopy(config) if isinstance(config, dict) else {}
    values = out.setdefault("values", {})
    if not isinstance(values, dict):
        values = {}
        out["values"] = values
    dm = values.setdefault("dm", {})
    if not isinstance(dm, dict):
        dm = {}
        values["dm"] = dm
    if "sync_interval_min" not in dm or dm.get("sync_interval_min") in (None, ""):
        dm["sync_interval_min"] = DEFAULT_INTERVAL_MIN
    # validate
    interval_minutes(out)
    return out


if __name__ == "__main__":
    import argparse

    argparse.ArgumentParser(description=__doc__.splitlines()[0]).parse_args()
