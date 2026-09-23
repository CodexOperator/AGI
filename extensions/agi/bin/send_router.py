"""send_router.py — transport choice as a table, never policy.

`send.py` calls `choose()`; the table decides. A new transport is a new module
plus one `register()` row, never a new `if` in `send.py`. Stdlib only: the
rotate/dispatch/send coupling is what this module exists to keep out.
"""
from __future__ import annotations

from typing import NamedTuple


class Choice(NamedTuple):
    """One matched row: the transport a (verb, args) pair selects."""
    name: str
    transport: object


class NoTransport(LookupError):
    """No row matched — a named refusal, never a fallback to policy."""


class AmbiguousTransport(LookupError):
    """More than one row matched — refuse rather than guess."""


def _room(a):
    return getattr(a, "room", None) is not None


def _dm(a):
    return getattr(a, "dm_to", None) is not None


def _inbox(a):
    return getattr(a, "room", None) is None and getattr(a, "dm_to", None) is None


#: Ordered rows, first match wins: {name: (verb, transport-descriptor, matcher)}.
#: The descriptor names the transport; send.py owns the callable behind it.
TRANSPORTS: dict[str, tuple] = {
    "room": ("send", "room", _room),
    "dm": ("send", "dm", _dm),
    "inbox": ("send", "inbox", _inbox),
}


def register(name, transport, match, *, verb="send", replace=False):
    """A new transport is a row here, not a branch in send.py."""
    if name in TRANSPORTS and not replace:
        raise ValueError(f"transport {name!r} already registered")
    TRANSPORTS[name] = (verb, transport, match)
    return Choice(name, transport)


def choose(verb, args):
    """Pick a transport by pure table lookup — no policy, no fallback."""
    hits = [Choice(n, t) for n, (v, t, m) in TRANSPORTS.items()
            if v == verb and m(args)]
    if not hits:
        raise NoTransport(f"no transport for verb {verb!r}")
    if len(hits) > 1:
        raise AmbiguousTransport(f"verb {verb!r} matches {[h.name for h in hits]}")
    return hits[0]
