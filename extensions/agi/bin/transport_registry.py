"""Delivery-only transport registry for send routes.

Rows map a route name to a callable.  Policy and message construction stay
with the caller; this module only performs the selected delivery.
"""
from __future__ import annotations

from pathlib import Path


def _append_inbox(inbox: Path, block: str) -> None:
    with inbox.open("a") as handle:
        handle.write(block)


TRANSPORTS = {"inbox": _append_inbox}


def deliver(name: str, **kwargs):
    return TRANSPORTS[name](**kwargs)
