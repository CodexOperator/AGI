#!/usr/bin/env python3
"""dm_read_version.py — read pushes read=true to SENDER remote (g7.32.6.5).

Owner design (goal:g7.32.6 design line 5): read = a new dm node version
with the read flag true, pushed to the SENDER's remote head (not the
addressee). Other posts learn read status on their next sync.

Public API
----------
build_read_version(*, sender_row, addressee, body="", season=2) -> dict
    Payload with read=True and destination=resolve_address(sender_row).
"""
from __future__ import annotations

from typing import Any

import dm_address
import dm_send_version


def build_read_version(
    *,
    sender_row: dict,
    addressee: str,
    body: str = "",
    season: int = 2,
    existing: dict | None = None,
) -> dict[str, Any]:
    """ONE read version aimed at the sender's remote head."""
    if not isinstance(sender_row, dict):
        raise ValueError("dm_read_version: sender_row required")
    sender = str(sender_row.get("name") or "").strip()
    if not sender:
        raise ValueError("dm_read_version: sender_row.name required")
    if not str(addressee).strip():
        raise ValueError("dm_read_version: addressee required")
    destination = dm_address.resolve_address(sender_row, season=season)
    path = dm_send_version.dm_relpath(sender, addressee)
    base = dict(existing) if isinstance(existing, dict) else {}
    base.update(
        {
            "kind": "dm_read",
            "path": path,
            "slug": dm_send_version.pairwise_slug(sender, addressee),
            "from": str(addressee).strip(),  # reader acknowledging
            "to": sender,  # back to sender
            "body": body if body != "" else base.get("body", ""),
            "read": True,
            "destination": destination,
            "route": "post-branch",
            "read_target": "sender",
        }
    )
    if base["destination"] != destination:
        raise ValueError("dm_read_version: destination must be sender remote")
    if base.get("read") is not True:
        raise ValueError("dm_read_version: read flag must be True")
    return base


if __name__ == "__main__":
    import argparse

    argparse.ArgumentParser(description=__doc__.splitlines()[0]).parse_args()
