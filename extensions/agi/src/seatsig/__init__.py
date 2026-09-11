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
``DEFAULT_SCHEME`` str -- the default scheme name, so a caller names the
                        REGISTRY (``seatsig.get(seatsig.DEFAULT_SCHEME)``)
                        and never the algorithm literal. SCHEMES is the ONE
                        plug point for schemes.

Encryption seam (Prime ruling B: the seam, not the cipher): every
``Scheme`` carries an OPTIONAL ``enc_scheme`` name and ``encrypt``/``decrypt``
hooks, all ``None`` today. ``SCHEMES`` is the ONE plug point where a future
scheme -- or a cipher attached to one -- registers. **No encryption is
implemented**: the hooks are dead slots that look like the feature but do
nothing, so nobody believes a message is encrypted when it is not.
"""

from __future__ import annotations

import hashlib
import sys

from . import ed25519 as _ed25519

__all__ = ["Scheme", "SCHEMES", "register", "get", "fingerprint",
           "DEFAULT_SCHEME"]

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

    OPTIONAL encryption seam (Prime ruling B): ``enc_scheme`` names the
    cipher a future scheme might carry, ``encrypt``/``decrypt`` are the
    hooks. All are ``None`` today -- **no encryption is implemented**. A
    subclass that wants to carry a cipher sets these when it registers;
    callers that care measure ``scheme.enc_scheme`` being None and act
    accordingly (today: there is no cipher, so no act). SCHEMES is the ONE
    plug point.
    """

    name = ""  # set by subclasses / registered instances
    #: Optional encryption hook slot -- None means this scheme has no cipher
    #: attached. NO encryption is implemented today (Prime ruling B).
    enc_scheme = None
    encrypt = None
    decrypt = None


#: The default scheme name. A caller names the REGISTRY via this, never the
#: algorithm literal (grep-assert: no caller outside src/seatsig names
#: "ed25519"). Must name a scheme present in SCHEMES.
DEFAULT_SCHEME = _ED25519.name


#: The live scheme registry. A scheme registers under its ``name`` key.
SCHEMES = {}


def register(scheme):
    """Add a Scheme to the table under ``scheme.name``.

    Returns the scheme so ``SCHEMES['x'] = register(x)`` mirrors the dict
    semantics the interface asks for. Every registered scheme is guaranteed
    the optional encryption seam (``enc_scheme``/``encrypt``/``decrypt``,
    None when the scheme does not declare one) -- SCHEMES is the ONE plug
    point.
    """
    if not getattr(scheme, "name", None):
        raise ValueError("a seatsig Scheme needs a non-empty .name")
    for _slot in ("enc_scheme", "encrypt", "decrypt"):
        if not hasattr(scheme, _slot):
            setattr(scheme, _slot, None)
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

# ONE registry, whichever spelling loads last adopts the first's objects
# (mur-39 order (e)). The package really is imported two ways across the
# codebase -- send.py does ``import seatsig`` (src/ on sys.path), while tests
# historically did ``from src.seatsig import`` -- and without this a ``Scheme``
# registered through one spelling is invisible to the other, because ``SCHEMES``
# is a module-global on TWO module objects. Fold late-loading spellings into
# the already-loaded twin so there is exactly one table: a scheme registered
# through either spelling is ``get()``-able through both.
_TWIN_NAME = "src.seatsig" if __name__ == "seatsig" else "seatsig"
_TWIN = sys.modules.get(_TWIN_NAME)
if _TWIN is not None and _TWIN is not sys.modules.get(__name__):
    # Adopt the twin's objects as our own; register() now writes into the
    # SHARED dict (module-global rebind is visible to the functions below).
    SCHEMES = _TWIN.SCHEMES
    _ED25519 = _TWIN._ED25519
    DEFAULT_SCHEME = _TWIN.DEFAULT_SCHEME
    register(_ED25519)  # idempotent: (re)binds ed25519 into the shared table