#!/usr/bin/env python3
"""kid_write_gate.py — parents own kid* rows only; kids write none (g7.31.3.3.5).

Owner design (goal:g7.31.3.3.5): gate who may write which rows — parents write
only their own kid rows; kids write none.

Public API
----------
is_kid_row_key(key) -> bool
    True when the target key is a kid* row id.

may_write(writer, target_key, *, parent_post=None) -> tuple[bool, str]
    (allowed, reason). reason is empty on allow; a named refusal otherwise.

assert_may_write(...) -> None
    Raise PermissionError with the named refusal when not allowed.

check_write(...) -> str | None
    None when allowed; refusal string when refused (for callers that prefer
    soft refusal over raise).
"""
from __future__ import annotations

import re
from typing import Any

_KID_KEY = re.compile(r"^kid([0-9]+|[-_][A-Za-z0-9_-]*|[A-Za-z][A-Za-z0-9_-]*)?$")


def is_kid_row_key(key: str | None) -> bool:
    """True for kid / kid0 / kid-a / kid_1 style row keys under a parent slot."""
    if not key or not isinstance(key, str):
        return False
    return bool(_KID_KEY.match(key.strip()))


def _writer_role(writer: dict | None) -> str:
    if not isinstance(writer, dict):
        return ""
    role = str(writer.get("role") or "").strip().lower()
    if role:
        return role
    # tier-0 convention: explicit kid/parent markers
    if writer.get("kid") or str(writer.get("kind") or "").lower() == "kid":
        return "kid"
    if str(writer.get("kind") or "").lower() == "parent":
        return "parent"
    return ""


def _writer_post(writer: dict | None) -> str:
    if not isinstance(writer, dict):
        return ""
    return str(
        writer.get("post")
        or writer.get("parent_post")
        or writer.get("name")
        or writer.get("slot_owner")
        or ""
    ).strip()


def may_write(
    writer: dict | None,
    target_key: str,
    *,
    parent_post: str | None = None,
) -> tuple[bool, str]:
    """Return (allowed, refusal_reason).

    Rules
    -----
    - Kids write none (any target).
    - Parents may write only their own kid* rows under their slot.
    - Parent → foreign kid* refused by name.
    - Parent → non-kid target refused (unscoped write path).
    - Non-parent / non-kid writers (director/loop) are out of this leaf's
      gate — return allow so sibling loops are not blocked; this leaf owns
      the parent/kid write surface only.
    """
    role = _writer_role(writer)
    key = (target_key or "").strip()
    if not key:
        return False, "kid_write_gate: empty target refused"

    if role == "kid":
        return False, f"kid_write_gate: kids write none (target={key})"

    if role == "parent":
        if not is_kid_row_key(key):
            return (
                False,
                f"kid_write_gate: parent may write only own kid* rows "
                f"(target={key} is not kid*)",
            )
        owner = (parent_post or "").strip() or _writer_post(writer)
        writer_post = _writer_post(writer)
        if owner and writer_post and owner != writer_post:
            return (
                False,
                f"kid_write_gate: foreign-kid write refused "
                f"(writer={writer_post} target_owner={owner} target={key})",
            )
        # Own kid* under this parent's slot.
        if writer_post and owner and writer_post == owner:
            return True, ""
        if writer_post and not owner:
            # No foreign owner declared — treat as own-slot write.
            return True, ""
        if not writer_post:
            return False, "kid_write_gate: parent writer missing post name"
        return True, ""

    # Directors / reaper loop / unset role: this leaf does not gate them.
    return True, ""


def check_write(
    writer: dict | None,
    target_key: str,
    *,
    parent_post: str | None = None,
) -> str | None:
    """None when allowed; named refusal string when refused."""
    ok, reason = may_write(writer, target_key, parent_post=parent_post)
    return None if ok else reason


def assert_may_write(
    writer: dict | None,
    target_key: str,
    *,
    parent_post: str | None = None,
) -> None:
    reason = check_write(writer, target_key, parent_post=parent_post)
    if reason:
        raise PermissionError(reason)


def apply_write(
    store: dict[str, Any],
    writer: dict | None,
    target_key: str,
    value: Any,
    *,
    parent_post: str | None = None,
) -> dict[str, Any]:
    """Mutate store[target_key]=value only when may_write allows; else raise."""
    assert_may_write(writer, target_key, parent_post=parent_post)
    store[target_key] = value
    return store


if __name__ == "__main__":
    import argparse
    argparse.ArgumentParser(description=__doc__.splitlines()[0]).parse_args()
