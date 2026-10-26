#!/usr/bin/env python3
"""goal:g7.16.1.11.46.20 (V2): check the `cred` and `slot` cells of config:posts.

A row names its login with `cred`: absent or "inherit" = the director's login, else the
32-hex id of a `kind secret` capsule (a different login = a different subscription).
`slot` says where the row runs: absent or "own" = its own uid and home, "inherit" = the
director's. A different login in the director's uid is a contradiction (the uid reads the
director's credential), and an owner-facing row never carries a login of its own.
Opens ONE file and reads only those cells (capsule ids or "inherit", never a secret); the id is
checked for FORMAT only, never resolved. Names a row and a cell, never a value, and the absolute path it read. An unreadable input prints `unread` and exits 1.
"""
import json
import re
import sys
from pathlib import Path

DEFAULT = ".agi/nodes/.geometry/posts.md"
_CID = re.compile(r"[0-9a-f]{32}")
_ROW = re.compile(r"^  - (\{.*\})\s*$")


def problems(text: str) -> list[str]:
    out: list[str] = []
    for n, line in enumerate(text.splitlines(), 1):
        m = _ROW.match(line)
        if not m:
            continue
        try:
            row = json.loads(m.group(1))
        except ValueError:
            out.append(f"line {n}: a row is not JSON")
            continue
        name = row.get("name", f"line {n}")
        cred, slot = row.get("cred", "inherit"), row.get("slot", "own")
        if not (cred == "inherit" or (isinstance(cred, str) and _CID.fullmatch(cred))):
            out.append(f"{name}: `cred` is not inherit or a 32-hex capsule id")
            continue
        if slot not in ("own", "inherit"):
            out.append(f"{name}: `slot` is not own or inherit")
            continue
        if cred != "inherit" and slot == "inherit":
            out.append(f"{name}: `cred` names another login but `slot` is inherit: a different login needs its own slot")
        if cred != "inherit" and row.get("faces") == "owner":
            out.append(f"{name}: an owner-facing row keeps the login it has: `cred` must be inherit")
    return out


def main(argv: list[str]) -> int:
    if len(argv) > 1 and argv[1] in ("-h", "--help"):
        print("usage: credpiece.py [posts.md]   check the cred / slot cells of config:posts; rc 1 names a row, `unread` is rc 1")
        return 0
    p = Path(argv[1] if len(argv) > 1 else DEFAULT).resolve()
    try:
        text = p.read_text(encoding="utf-8")
    except OSError:
        print(f"[cred] unread: {p}", file=sys.stderr)
        return 1
    rows = sum(1 for l in text.splitlines() if _ROW.match(l))
    if not rows:
        print(f"[cred] unread: {p} has no post row", file=sys.stderr)
        return 1
    bad = problems(text)
    for b in bad:
        print(f"[cred] PROBLEM: {b}", file=sys.stderr)
    if not bad:
        ids = sum(1 for l in text.splitlines() if _ROW.match(l) and json.loads(_ROW.match(l).group(1)).get("cred", "inherit") != "inherit")
        print(f"[cred] ok: {rows} rows in {p} (format only: {ids} capsule ids not resolved)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
