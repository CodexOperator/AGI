#!/usr/bin/env python3
"""dm_send_version.py — send = ONE dm-file node version, read=false (g7.32.6.2).

Owner design (goal:g7.32.6 design line 1): send calls write.py — ONE commit
+ push per dm as a new version of the pairwise dm file node, its read row
= false. No inbox write.

Public API
----------
pairwise_slug(a, b) -> str
    Sorted pair name `<lo>--<hi>`.

dm_relpath(a, b) -> str
    Graph-relative path under comms dm/ — never sessions/inbox/.

build_send_version(sender, addressee, body, address) -> dict
    Payload for the write.py dm version: read=False, destination=address.
"""
from __future__ import annotations

from typing import Any


def pairwise_slug(a: str, b: str) -> str:
    """Canonical pairwise dm file stem; names sorted."""
    lo, hi = sorted([str(a).strip(), str(b).strip()])
    if not lo or not hi:
        raise ValueError("dm_send_version.pairwise_slug: both names required")
    if lo == hi:
        raise ValueError(
            f"dm_send_version.pairwise_slug: refuse self-pair {lo!r}"
        )
    return f"{lo}--{hi}"


def dm_relpath(a: str, b: str) -> str:
    """Relative dm node path (post-branch route). Never an inbox path."""
    return f"comms/dm/{pairwise_slug(a, b)}.md"


def build_send_version(
    *,
    sender: str,
    addressee: str,
    body: str,
    address: str,
) -> dict[str, Any]:
    """ONE send version: read=false, destination=address, path=dm_relpath.

    Raises ValueError when address/body/names missing — never invents hub.
    """
    if not str(sender).strip() or not str(addressee).strip():
        raise ValueError("dm_send_version: sender and addressee required")
    if not str(body).strip():
        raise ValueError("dm_send_version: body required")
    if not str(address).strip():
        raise ValueError(
            "dm_send_version: address (addressee remote head) required — "
            "refuse hub fallback"
        )
    path = dm_relpath(sender, addressee)
    if "inbox" in path.split("/"):
        raise ValueError("dm_send_version: inbox path refused by name")
    return {
        "kind": "dm_send",
        "path": path,
        "slug": pairwise_slug(sender, addressee),
        "from": str(sender).strip(),
        "to": str(addressee).strip(),
        "body": body,
        "read": False,
        "destination": str(address).strip(),
        "route": "post-branch",
    }


if __name__ == "__main__":
    import argparse

    argparse.ArgumentParser(description=__doc__.splitlines()[0]).parse_args()
