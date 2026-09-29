#!/usr/bin/env python3
"""dm_engine.py — production façade wiring dm_* into send/cron/nudge/read.

Owner design (goal:g7.32.6): send/cron/nudge/read hold on the post-branch
route. Contracts live in dm_address / dm_send_version / dm_sync_cron /
dm_nudge_gate / dm_read_version / dm_no_inbox. This module is the ONE
production composer those engine paths import — so deleting an import here
(or in send.py/crons.py) breaks a named falsifier (g7.32.6.7–.9).

Full write.py mint cutover + inbox retirement wait on goal:g4.18.1
(director-engine). This façade plans and gates; it does not yet push a
grid version or retire sessions/inbox.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any

import dm_address
import dm_no_inbox
import dm_nudge_gate
import dm_read_version
import dm_send_version
import dm_sync_cron


def plan_send(
    *,
    sender: str,
    addressee_row: dict,
    body: str,
    season: int = 2,
) -> dict[str, Any]:
    """Compose ONE send version aimed at the addressee's post-branch address.

    Raises ValueError / PermissionError from the contracts — never invents hub,
    never accepts an inbox path.
    """
    addressee = str(addressee_row.get("name") or "").strip()
    if not addressee:
        raise ValueError("dm_engine.plan_send: addressee_row.name required")
    address = dm_address.resolve_address(addressee_row, season=season)
    payload = dm_send_version.build_send_version(
        sender=sender,
        addressee=addressee,
        body=body,
        address=address,
    )
    dm_no_inbox.assert_allowed_dm_path(payload["path"])
    return payload


def plan_read(
    *,
    sender_row: dict,
    addressee: str,
    body: str = "",
    season: int = 2,
    existing: dict | None = None,
) -> dict[str, Any]:
    """Compose ONE read=true version aimed at the sender's remote head."""
    payload = dm_read_version.build_read_version(
        sender_row=sender_row,
        addressee=addressee,
        body=body,
        season=season,
        existing=existing,
    )
    dm_no_inbox.assert_allowed_dm_path(payload["path"])
    return payload


def gate_nudge(
    root: Path | None,
    row: dict | None,
    dm: dict | None,
    *,
    from_sync: bool = False,
) -> bool:
    """Production nudge gate — sync-only + local + unread + quiet/[red]."""
    return dm_nudge_gate.may_nudge(root, row, dm, from_sync=from_sync)


def sync_interval_min(config: dict | None = None) -> int:
    """Config cell values.dm.sync_interval_min (default 3, range [1,3])."""
    return dm_sync_cron.interval_minutes(config)


def sync_schedule_expr(config: dict | None = None) -> str:
    """Cron schedule expression for the per-box dm_sync job."""
    n = sync_interval_min(config)
    return f"*/{n} * * * *"


def plan_sync_tick(
    root: Path,
    local_rows: list[dict],
    unread_dms: list[tuple[dict, dict]],
    *,
    from_sync: bool = True,
) -> list[dict[str, Any]]:
    """For each (row, dm) where gate_nudge holds, return a nudge plan dict.

    unread_dms: list of (post_row, dm_dict). Does not type panes — plans only.
    """
    out: list[dict[str, Any]] = []
    for row, dm in unread_dms:
        if not gate_nudge(root, row, dm, from_sync=from_sync):
            continue
        name = str(row.get("name") or "").strip()
        out.append(
            {
                "kind": "dm_nudge",
                "post": name,
                "body": str(dm.get("body") or ""),
                "tag": "post dm" if not dm.get("reply") else "post reply",
                "from_sync": True,
            }
        )
    # local_rows retained for callers that want a count of scanned posts
    _ = local_rows
    return out


if __name__ == "__main__":
    import argparse

    argparse.ArgumentParser(description=__doc__.splitlines()[0]).parse_args()
