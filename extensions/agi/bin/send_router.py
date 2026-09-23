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
    dispatch: object = None


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


#: Ordered rows, FIRST MATCH WINS: {name: (verb, transport-descriptor, matcher)}.
#: The descriptor names the transport; send.py registers the callable behind it.
#: Row order IS the priority: an appended row lands after the inbox catch-all
#: and is shadowed, so register(..., first=True) inserts ahead of every row.
TRANSPORTS: dict[str, tuple] = {
    "room": ("send", "room", _room),
    "dm": ("send", "dm", _dm),
    "inbox": ("send", "inbox", _inbox),
}

#: Dispatch callables by row name, filled by register(dispatch=...) -- the row
#: carries both the choice and the code that runs it.
_RUN: dict[str, object] = {}


def register(name, transport, match, *, verb="send", replace=False,
             dispatch=None, first=False):
    """A new transport is a row here, not a branch in send.py.

    `first=True` inserts ahead of every existing row, so a new transport can
    win over the inbox catch-all instead of being silently shadowed.
    """
    global TRANSPORTS
    if name in TRANSPORTS and not replace:
        raise ValueError(f"transport {name!r} already registered")
    TRANSPORTS.pop(name, None)
    row = (verb, transport, match)
    TRANSPORTS = {name: row, **TRANSPORTS} if first else {**TRANSPORTS, name: row}
    if dispatch is not None:
        _RUN[name] = dispatch
    return Choice(name, transport, _RUN.get(name))


def choose(verb, args):
    """Pick the FIRST matching row in table order — no policy, no fallback."""
    for n, (v, t, m) in TRANSPORTS.items():
        if v == verb and m(args):
            return Choice(n, t, _RUN.get(n))
    raise NoTransport(f"no transport for verb {verb!r}")
