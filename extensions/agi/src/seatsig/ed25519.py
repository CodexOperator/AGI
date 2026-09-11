"""Pure-Python Ed25519 (EdDSA over edwards25519) implemented from RFC 8032.

Security grade (verbatim in substance): good enough for agent
collaboration -- a spoofing guard between cooperating agents on shared
infrastructure, not adversarial-grade. This is the RFC's own reference
implementation style: correct for every input, but slow and *not*
side-channel silent. Private keys are seeds; signatures are RFC 8032
byte-exact against the section 7.1 test vectors.

The only crypto primitive imported is ``hashlib.sha512``. There is no
dependency on pynacl, cryptography, or any external library at runtime.
"""

from __future__ import annotations

import hashlib
import os

__all__ = ["Ed25519Scheme"]

# The field prime: 2^255 - 19
_P = 2**255 - 19
# The group order (RFC 8032 section 5.1, "L")
_Q = 2**252 + 27742317777372353535851937790883648493
# Curve constant d = -121665 / 121666 (mod p)
_D = (-121665 * pow(121666, _P - 2, _P)) % _P
# Square root of -1 (mod p), needed to disambiguate square roots
_SQRT_M1 = pow(2, (_P - 1) // 4, _P)

# The base point B. Its y coordinate is 4/5 (mod p); x is the recovering
# x with sign bit 0.
_GY = (4 * pow(5, _P - 2, _P)) % _P


def _recover_x(y, sign):
    """Recover the x coordinate for a given y and sign bit (RFC 8032 5.1.3)."""
    if y >= _P:
        return None
    x2 = (y * y - 1) * pow(_D * y * y + 1, _P - 2, _P) % _P
    if x2 == 0:
        return None if sign else 0
    x = pow(x2, (_P + 3) // 8, _P)
    if (x * x - x2) % _P != 0:
        x = x * _SQRT_M1 % _P
    if (x * x - x2) % _P != 0:
        return None
    if (x & 1) != sign:
        x = _P - x
    return x


def _recover_base_x():
    """Recover the base point's x coordinate (sign bit 0)."""
    return _recover_x(_GY, 0)


_GX = _recover_base_x()
# Extended homogeneous coordinates (X, Y, Z, T): x = X/Z, y = Y/Z, x*y = T/Z
_BASE = (_GX, _GY, 1, _GX * _GY % _P)


def _point_add(P, Q):
    """Complete twisted-Edwards point addition with a=-1 (RFC 8032 5.1.4)."""
    A = (P[1] - P[0]) * (Q[1] - Q[0]) % _P
    B = (P[1] + P[0]) * (Q[1] + Q[0]) % _P
    C = 2 * P[3] * Q[3] * _D % _P
    D = 2 * P[2] * Q[2] % _P
    E, F, G, H = B - A, D - C, D + C, B + A
    return (E * F % _P, G * H % _P, F * G % _P, E * H % _P)


def _point_mul(s, P):
    """Double-and-add scalar multiplication: s * P."""
    Q = (0, 1, 1, 0)  # neutral element (0,1) in extended coordinates
    while s > 0:
        if s & 1:
            Q = _point_add(Q, P)
        P = _point_add(P, P)
        s >>= 1
    return Q


def _point_equal(P, Q):
    """x1/z1 == x2/z2 and y1/z1 == y2/z2 by cross-multiplication."""
    if (P[0] * Q[2] - Q[0] * P[2]) % _P != 0:
        return False
    if (P[1] * Q[2] - Q[1] * P[2]) % _P != 0:
        return False
    return True


def _point_compress(P):
    """Encode a point as 32 bytes: y with the x sign bit in bit 255."""
    zinv = pow(P[2], _P - 2, _P)
    x = P[0] * zinv % _P
    y = P[1] * zinv % _P
    return int.to_bytes(y | ((x & 1) << 255), 32, "little")


def _point_decompress(s):
    """Decode a 32-byte point encoding, or return None on failure."""
    if len(s) != 32:
        return None
    y = int.from_bytes(s, "little")
    sign = y >> 255
    y &= (1 << 255) - 1
    if y >= _P:
        return None
    x = _recover_x(y, sign)
    if x is None:
        return None
    return (x, y, 1, x * y % _P)


def _secret_expand(secret):
    """Expand a 32-byte seed into (secret scalar, signing prefix)."""
    if len(secret) != 32:
        raise ValueError("Ed25519 secret key must be exactly 32 bytes")
    h = hashlib.sha512(secret).digest()
    a = int.from_bytes(h[:32], "little")
    a &= (1 << 254) - 8  # clear lowest 3 bits and bit 255
    a |= 1 << 254        # set bit 254
    return a, h[32:]


class Ed25519Scheme:
    """RFC 8032 Ed25519 exposed through the seatsig Scheme interface."""

    name = "ed25519"
    # Optional encryption seam (Prime ruling B: the seam, not the cipher).
    # None today -- NO encryption is implemented; these are the slots a future
    # scheme or cipher fills. SCHEMES is the ONE plug point.
    enc_scheme = None
    encrypt = None
    decrypt = None

    def keygen(self):
        """Generate a fresh (private seed, public key) pair."""
        priv = os.urandom(32)
        a, _ = _secret_expand(priv)
        pub = _point_compress(_point_mul(a, _BASE))
        return priv, pub

    def public_from_secret(self, priv):
        """Derive the public key for a given 32-byte private seed.

        Needed to reuse a stored/key-exported seed (send.py will reconstruct
        a seat's public key from its stored private seed to verify). Ed25519
        is deterministic, so this is RFC-vector-checked in the tests.
        """
        a, _ = _secret_expand(priv)
        return _point_compress(_point_mul(a, _BASE))

    def sign(self, priv, msg):
        """Sign a message with a 32-byte private seed -> 64-byte signature."""
        if len(priv) != 32:
            raise ValueError("Ed25519 secret key must be exactly 32 bytes")
        a, prefix = _secret_expand(priv)
        A = _point_compress(_point_mul(a, _BASE))
        r = int.from_bytes(hashlib.sha512(prefix + msg).digest(), "little") % _Q
        R = _point_compress(_point_mul(r, _BASE))
        k = int.from_bytes(hashlib.sha512(R + A + msg).digest(), "little") % _Q
        s = (r + k * a) % _Q
        return R + int.to_bytes(s, 32, "little")

    def verify(self, pub, msg, sig):
        """Verify a signature against a 32-byte public key."""
        if len(pub) != 32:
            return False
        if len(sig) != 64:
            return False
        A = _point_decompress(pub)
        R = _point_decompress(sig[:32])
        if A is None or R is None:
            return False
        s = int.from_bytes(sig[32:], "little")
        if s >= _Q:
            return False
        k = int.from_bytes(hashlib.sha512(sig[:32] + pub + msg).digest(),
                           "little") % _Q
        sB = _point_mul(s, _BASE)
        hA = _point_mul(k, A)
        # RFC 8032 5.1.7 step 3: check [8][S]B == [8]R + [8][k]A. The RFC
        # states it is "sufficient, but not required, to instead check
        # [S]B = R + [k]A" -- and any signature passing the un-multiplied
        # equation passes the multiplied one, so for a spoofing guard the
        # cheaper check is valid for every legitimate signature.
        return _point_equal(sB, _point_add(R, hA))