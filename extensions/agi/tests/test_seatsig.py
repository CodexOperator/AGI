"""Tests for the seatsig swappable-signature-scheme package.

Covers: RFC 8032 section 7.1 Ed25519 test vectors 1-3 (bytes-exact for
secret key, public key, message, signature); tamper/wrong-key rejection;
keygen/sign/verify round trips; fingerprint; unknown-name KeyError; a
``dummy`` scheme registered inside a test proving the table is the only
coupling; and ``sig_scheme``-style indirection via a string variable.
"""

from __future__ import annotations

import hashlib

import pytest

from src.seatsig import SCHEMES, Scheme, register, get, fingerprint

# ---------------------------------------------------------------------------
# RFC 8032 section 7.1, test vectors 1-3, transcribed verbatim (the octets
# are hex encoded in the RFC, whitespace inserted for readability only).
# These are FIXED against the RFC text on purpose: the point of the vector
# check is that OUR ed25519 reproduces the published bytes exactly, so a
# vector must never be "adjusted" to make the code pass.
# ---------------------------------------------------------------------------
RFC_VECTORS = [
    # TEST 1: empty message
    {
        "secret": ("9d61b19deffd5a60ba844af492ec2cc4"
                   "4449c5697b326919703bac031cae7f60"),
        "public": ("d75a980182b10ab7d54bfed3c964073a"
                   "0ee172f3daa62325af021a68f707511a"),
        "message": "",
        "signature": ("e5564300c360ac729086e2cc806e828a"
                      "84877f1eb8e5d974d873e06522490155"
                      "5fb8821590a33bacc61e39701cf9b46b"
                      "d25bf5f0595bbe24655141438e7a100b"),
    },
    # TEST 2: 1-byte message 0x72
    {
        "secret": ("4ccd089b28ff96da9db6c346ec114e0f"
                   "5b8a319f35aba624da8cf6ed4fb8a6fb"),
        "public": ("3d4017c3e843895a92b70aa74d1b7ebc"
                   "9c982ccf2ec4968cc0cd55f12af4660c"),
        "message": "72",
        "signature": ("92a009a9f0d4cab8720e820b5f642540"
                      "a2b27b5416503f8fb3762223ebdb69da"
                      "085ac1e43e15996e458f3613d0f11d8c"
                      "387b2eaeb4302aeeb00d291612bb0c00"),
    },
    # TEST 3: 2-byte message 0xaf82
    {
        "secret": ("c5aa8df43f9f837bedb7442f31dcb7b1"
                   "66d38535076f094b85ce3a2e0b4458f7"),
        "public": ("fc51cd8e6218a1a38da47ed00230f058"
                   "0816ed13ba3303ac5deb911548908025"),
        "message": "af82",
        "signature": ("6291d657deec24024827e69c3abe01a3"
                      "0ce548a284743a445e3680d7db5ac3ac"
                      "18ff9b538d16f290ae67f760984dc659"
                      "4a7c15e9716ed28dc027beceea1ec40a"),
    },
]


@pytest.mark.parametrize("vector", RFC_VECTORS, ids=["rfc8032-7.1-test1",
                                                     "rfc8032-7.1-test2",
                                                     "rfc8032-7.1-test3"])
def test_rfc8032_vector(vector):
    """Bytes-exact reproduction of RFC 8032 section 7.1 test vectors 1-3."""
    scheme = get("ed25519")
    secret = bytes.fromhex(vector["secret"])
    public = bytes.fromhex(vector["public"])
    message = bytes.fromhex(vector["message"])
    signature = bytes.fromhex(vector["signature"])

    # Public key: recompute from the secret seed. Ed25519 is deterministic,
    # so this must reproduce the RFC's public key byte-for-byte.
    pub = scheme.public_from_secret(secret)
    assert pub == public, "RFC 8032 public key mismatch -- ed25519 is wrong"

    # Signature: deterministic, must be byte-for-byte the RFC's.
    sig = scheme.sign(secret, message)
    assert sig == signature, "RFC 8032 signature mismatch -- ed25519 is wrong"


def test_signature_derived_not_fixed_string():
    """The vector check proves real recomputation is exercised, not a stub.

    We assert the produced signature actually wraps the message by verifying
    a *different* message under the same key must NOT produce the vector
    signature (which would be the case if sign() ignored its message).
    """
    scheme = get("ed25519")
    vector = RFC_VECTORS[0]
    secret = bytes.fromhex(vector["secret"])
    sig = scheme.sign(secret, b"")
    assert sig == bytes.fromhex(vector["signature"])
    # Changing the message must change the signature.
    assert scheme.sign(secret, b"x") != sig


def test_tampered_message_fails_verify():
    scheme = get("ed25519")
    priv, pub = scheme.keygen()
    sig = scheme.sign(priv, b"genuine payload")
    assert scheme.verify(pub, b"genuine payload", sig) is True
    assert scheme.verify(pub, b"tampered payload", sig) is False


def test_wrong_key_fails_verify():
    scheme = get("ed25519")
    priv, pub = scheme.keygen()
    other_priv, other_pub = scheme.keygen()
    sig = scheme.sign(priv, b"payload")
    # Right message, wrong key -> must fail.
    assert scheme.verify(other_pub, b"payload", sig) is False


def test_roundtrip_true():
    scheme = get("ed25519")
    for _ in range(5):
        priv, pub = scheme.keygen()
        for msg in (b"", b"a", b"a" * 1024):
            sig = scheme.sign(priv, msg)
            assert scheme.verify(pub, msg, sig) is True


def test_fingerprint():
    scheme = get("ed25519")
    _, pub_a = scheme.keygen()
    _, pub_b = scheme.keygen()
    fa, fa2 = fingerprint(pub_a), fingerprint(pub_a)
    fb = fingerprint(pub_b)
    assert len(fa) == 16
    assert fa == fa2, "fingerprint must be deterministic"
    assert fa != fb, "distinct keys need distinct fingerprints"
    assert set(fa).issubset(set("0123456789abcdef")), "must be hex"


def test_unknown_scheme_keyerror_names_it():
    with pytest.raises(KeyError) as exc:
        get("nope")
    assert "nope" in str(exc.value)


class _DummyScheme(Scheme):
    """Registered INSIDE the test so the table-only coupling is proven.

    sign = sha256(msg + priv), verify recomputes. Not a real signature
    scheme -- it exists to prove code that goes through get()/Scheme works
    for any registered scheme, ed25519 ordinary.
    """

    name = "dummy"

    def keygen(self):
        import os
        # For a dummy, "pub" mirrors the secret so verify() can recompute
        # what sign() produced from the interface's (priv, pub) split.
        priv = os.urandom(8)
        return priv, priv

    def sign(self, priv, msg):
        return hashlib.sha256(msg + priv).digest()

    def verify(self, pub, msg, sig):
        return sig == hashlib.sha256(msg + pub).digest()


def test_dummy_scheme_registered_in_test_and_used_through_table():
    """The table is the only coupling: we never touch ed25519 directly."""
    register(_DummyScheme())
    scheme = get("dummy")
    assert scheme.name == "dummy"
    priv, pub = scheme.keygen()
    sig = scheme.sign(priv, b"hi")
    assert scheme.verify(pub, b"hi", sig) is True
    assert scheme.verify(pub, b"bye", sig) is False


def test_sig_scheme_string_indirection():
    """Selecting a scheme from a small string mapping (send.py-style)."""
    # Map a config string to a scheme object exactly as send.py would.
    # Register the dummy HERE: a test must pass alone, never lean on a
    # sibling's side effect (L4.275 parent review: alone -> KeyError).
    register(_DummyScheme())
    sig_scheme = {
        "ed25519": get("ed25519"),
        "dummy": get("dummy"),
    }
    for name, scheme in sig_scheme.items():
        priv, pub = scheme.keygen()
        msg = ("route:%s" % name).encode()
        sig = scheme.sign(priv, msg)
        assert scheme.verify(pub, msg, sig) is True, name


def test_default_ed25519_registered():
    """ed25519 is the default scheme and present in the live table."""
    assert "ed25519" in SCHEMES
    assert get("ed25519").name == "ed25519"