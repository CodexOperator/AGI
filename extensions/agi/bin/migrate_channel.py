#!/usr/bin/env python3
"""migrate_channel.py -- the ONE cross-box `migrate` record kind (SM.123).

A quick-migrate moves a post to another box. The order crosses boxes on the
channel that already rides git (comms files on the branch), read on the target
box by the mail_poll tick. This module owns that ONE record and nothing else:
one writer, one parser, one signature. `boxes.py` still resolves boxes,
`send.py` still owns the channel and the post's signing key; neither is
duplicated here.
"""
from __future__ import annotations

import re
from pathlib import Path

import yaml

import frontmatter

MODES = ("rotate", "fork")
KIND = "migrate"
SUBDIR = "migrate"

_KEYS = ("kind", "post", "mode", "source_box", "target_box", "branch", "tip",
         "session_id", "ts")
_UNSAFE = re.compile(r"[^A-Za-z0-9._-]+")


def record(*, post, mode, source_box, target_box, branch, tip, session_id, ts):
    """The ONE record dict: one kind, two modes, no addresses, no literals."""
    if mode not in MODES:
        raise ValueError(f"unknown migrate mode {mode!r} (one of {MODES})")
    if not post or not target_box or not ts:
        raise ValueError("a migrate record needs post, target_box and ts")
    return {"kind": KIND, "post": post, "mode": mode, "source_box": source_box,
            "target_box": target_box, "branch": branch, "tip": tip or "",
            "session_id": session_id or "", "ts": ts}


def record_name(rec) -> str:
    """`<ts>-<post>--<box>.md` -- aliases only, sanitized, never a path."""
    def _safe(v):
        return _UNSAFE.sub("-", str(v or "")) or "unknown"
    return f"{_safe(rec['ts'])}-{_safe(rec['post'])}--{_safe(rec['target_box'])}.md"


def _canonical(rec) -> str:
    """The record's nine fields in a fixed key order -- the payload a
    signature covers. `send._canonical_msg(ts, post, target_box, THIS)` is
    the exact signed envelope; `sig` is absent so a reader reconstructs the
    same bytes from the parsed dict (send's one-canonical-form discipline).
    """
    return "\n".join(f"{k}: {rec.get(k, '')}" for k in _KEYS)


def format_record(rec, *, sign_root=None, signer=None) -> str:
    """The record file: frontmatter fields plus an optional `sig:` line.

    A signature is only attempted when `sign_root`/`signer` are given and the
    post holds a key; a keyless post writes an unsigned record (a detectable
    absence, never a fabricated signature).
    """
    fm = {k: rec.get(k, "") for k in _KEYS}
    if sign_root is not None and signer:
        import send
        line = send._sign_line(Path(sign_root), signer, rec["ts"],
                               rec["target_box"], _canonical(rec))
        if line:
            fm["sig"] = line.split(": ", 1)[1]
    head = yaml.safe_dump(fm, sort_keys=False, default_flow_style=False)
    body = (f"migrate record: {rec['post']} -> {rec['target_box']} "
            f"(mode {rec['mode']})\n")
    return "---\n" + head + "---\n\n" + body


def parse_record(text: str) -> dict | None:
    """Parse one record file, or None when it is not a migrate record."""
    parted = frontmatter.split_frontmatter(text)
    if not parted:
        return None
    try:
        fm = yaml.safe_load(parted[0]) or {}
    except yaml.YAMLError:
        return None
    if not isinstance(fm, dict) or fm.get("kind") != KIND:
        return None
    if fm.get("mode") not in MODES:
        return None
    return fm


def verify_record(text: str, pub_hex: str, scheme_name: str | None = None) -> bool:
    """True iff the record's `sig:` verifies against `pub_hex`.

    Unsigned, malformed, or unknown-scheme records are False -- an unverified
    record is never admitted, exactly like an unsigned dm.
    """
    rec = parse_record(text)
    if rec is None:
        return False
    parts = str(rec.get("sig") or "").split(":", 2)
    if len(parts) != 3:
        return False
    name, _fp, sig_hex = parts
    if scheme_name and name != scheme_name:
        return False
    try:
        import seatsig
        import send
        msg = send._canonical_msg(str(rec.get("ts", "")),
                                 str(rec.get("post", "")),
                                 str(rec.get("target_box", "")),
                                 _canonical(rec)).encode()
        scheme = seatsig.get(name)
        return bool(scheme.verify(bytes.fromhex(pub_hex), msg,
                                  bytes.fromhex(sig_hex)))
    except Exception:  # noqa: BLE001 -- any failure is a non-verification
        return False
