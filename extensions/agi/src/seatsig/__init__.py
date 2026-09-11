"""seatsig -- swappable message-signature schemes for seat/send.py routes.

Security grade (verbatim in substance): good enough for agent
collaboration -- a spoofing guard between cooperating agents on shared
infrastructure, not adversarial-grade. It authenticates that a message
came from the seat holding a known public key; it is not a defence
against a determined adversary with model access.

The only coupling a caller needs is this module's table. ``get(name)``
returns a :class:`Scheme`; keygen/sign/verify always go through that
interface, never through the concrete ed25519 module directly, so a
different scheme slot in (e.g. ``dummy`` in tests, or a hardware-backed
scheme later) without touching callers.

Public API
----------
``SCHEMES``   dict[str, Scheme] -- the live registry (``ed25519`` present).
``get(name)`` Scheme -- the scheme, or KeyError naming the unknown name.
``register(scheme)`` -- put a Scheme into the table under ``scheme.name``.
``fingerprint(pub)`` -> str -- first 16 hex chars of sha256(pub); a short
                        stable handle for logs/seat naming.
"""

from __future__ import annotations

import hashlib

from . import ed25519 as _ed25519

__all__ = ["Scheme", "SCHEMES", "register", "get", "fingerprint"]

# The ed25519 module may not have been loadable (broken install) -- it is
# pure python with only hashlib, so any load failure is a real defect and
# should surface loudly rather than be masked here.
_ED25519 = _ed25519.Ed25519Scheme()


class Scheme:
    """A named signature scheme with a uniform interface.

    Subclasses/instances must provide::

        name: str
        keygen()                      -> (priv: bytes, pub: bytes)
        sign(priv: bytes, msg: bytes) -> bytes
        verify(pub, msg, sig)         -> bool
    """

    name = ""  # set by subclasses / registered instances


#: The live scheme registry. A scheme registers under its ``name`` key.
SCHEMES = {}


def register(scheme):
    """Add a Scheme to the table under ``scheme.name``.

    Returns the scheme so ``SCHEMES['x'] = register(x)`` mirrors the dict
    semantics the interface asks for.
    """
    if not getattr(scheme, "name", None):
        raise ValueError("a seatsig Scheme needs a non-empty .name")
    SCHEMES[scheme.name] = scheme
    return scheme


def get(name):
    """Return the named scheme, or raise KeyError naming the unknown name."""
    try:
        return SCHEMES[name]
    except KeyError:
        raise KeyError(
            "unknown seatsig scheme %r; known schemes: %s"
            % (name, ", ".join(sorted(SCHEMES)) or "<none>")
        ) from None


def fingerprint(pub):
    """Short stable identity for a public key: first 16 hex chars of sha256.

    Deterministic, 16 chars, and (practically) distinct per distinct key.
    """
    return hashlib.sha256(pub).hexdigest()[:16]


# Register the default scheme at import time so ``get("ed25519")`` just works.
register(_ED25519)