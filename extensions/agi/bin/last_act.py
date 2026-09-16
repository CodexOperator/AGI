#!/usr/bin/env python3
"""The seat's OWN last work act — ONE clock, imported by the hook and rotate.

hypothesis:l4-the-card-age-captive-clocks-the-rotating-seat-own-last-act-never-
a-repo-wide-commit-and-merge-up-in-flight-means-a-real-merge

The card-age captive compared a card's mtime against the newest non-merge
commit by ANY seat (`git log -1 --no-merges -- .`), so in a shared checkout
every foreign commit re-staled the seat's card and the rotation looped. This is
the ONE seat-scoped clock: the newest of the seat's own stamp
(`<sessions>/seats/<seat>.last-act`) and the seat's OWN card commit time.
P7: every reader fails open — unmeasurable reads NOT stale; `touch` never raises.
"""
from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

STAMP_DIRNAME = "seats"

#: Set in the env of an ENGINE-INTERNAL write.py invocation (the rotate
#: closeout's `_g17_1_note`) so its stamp cannot re-stale the card it just
#: wrote (conjunct 1's measured hazard).
INTERNAL_ENV = "AGI_LAST_ACT_INTERNAL"

#: The env keys an act's seat is resolved from, in order.
SEAT_ENV = ("AGI_SEAT", "AGI_ACTOR", "AGI_AGENT_ID", "USER")
_UNSET = object()


def _bin_dir() -> Path:
    return Path(__file__).resolve().parent


def sessions_dir(root) -> Path:
    """The shared sessions dir through the engine's ONE resolver (locations),
    else `<root>/sessions` when locations cannot be imported (P7)."""
    try:
        if str(_bin_dir()) not in sys.path:
            sys.path.insert(0, str(_bin_dir()))
        import locations  # noqa: PLC0415
        return Path(locations.shared_sessions_dir(Path(root)))
    except Exception:  # noqa: BLE001
        return Path(root) / "sessions"


def stamp_path(root, seat: str) -> Path:
    return sessions_dir(root) / STAMP_DIRNAME / f"{seat}.last-act"


def touch(root, seat: str) -> None:
    """Stamp NOW as the seat's last act. NEVER raises (P7)."""
    try:
        p = stamp_path(root, seat)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(f"{int(time.time())}\n", encoding="utf-8")
    except Exception:  # noqa: BLE001
        pass


def env_seat(explicit: str | None = None) -> str:
    """The seat a verb acts as: the caller's `explicit` flag first (--actor,
    --seat, --from), else AGI_SEAT, AGI_ACTOR, AGI_AGENT_ID, USER. '' when
    nothing names a seat, and then NO stamp is written."""
    for v in (explicit, *[os.environ.get(k) for k in SEAT_ENV]):
        if v and str(v).strip():
            return str(v).strip()
    return ""


def touch_env(root, explicit: str | None = None) -> str:
    """Stamp the ACTING seat from the flag/env, SKIPPED when the invocation is
    engine-internal (`INTERNAL_ENV`): the closeout's own `write.py note` runs
    AFTER the rotation wrote the card, so a stamp there would re-stale it.
    Returns the seat stamped ('' when skipped or unnamed). Never raises (P7)."""
    if os.environ.get(INTERNAL_ENV):
        return ""
    seat = env_seat(explicit)
    if seat:
        touch(root, seat)
    return seat


def own_card(root, seat: str) -> Path | None:
    """The seat's own card, own copy first, then the shared sessions quorum."""
    for p in (Path(root) / "sessions" / "quorum" / f"{seat}.md",
              Path(root) / ".agi" / "sessions" / "quorum" / f"{seat}.md"):
        if p.exists():
            return p
    try:
        return sessions_dir(root) / "quorum" / f"{seat}.md"
    except Exception:  # noqa: BLE001
        return None


def _stamp_ts(p: Path) -> int | None:
    """The stamp's epoch seconds — its CONTENT when it parses, else its mtime.
    None when absent or unreadable (P7)."""
    try:
        if not p.exists():
            return None
        txt = p.read_text(encoding="utf-8").strip()
        if txt:
            return int(txt)
    except (OSError, ValueError):
        pass
    try:
        return int(p.stat().st_mtime)
    except OSError:
        return None


def _git(cwd, *args: str) -> str | None:
    """First stdout line of git in `cwd`, or None on ANY failure (P7)."""
    try:
        out = subprocess.run(["git", "-C", str(cwd), *args],
                             capture_output=True, text=True, timeout=10)
    except Exception:  # noqa: BLE001
        return None
    if out.returncode != 0 or not out.stdout.strip():
        return None
    return out.stdout.splitlines()[0].strip()


def card_commit_ts(root, card) -> int | None:
    """The commit time of the newest commit TOUCHING `card` — the seat's OWN
    card write, never another seat's commit. None unmeasurable (P7)."""
    card = Path(card)
    try:
        top = _git(root, "rev-parse", "--show-toplevel")
        if top is None:
            return None
        card = card.resolve() if card.is_absolute() else (Path(root) / card)
        rel = str(card.resolve().relative_to(Path(top).resolve()))
    except (ValueError, OSError):
        return None
    try:
        out = _git(top, "log", "-1", "--format=%ct", "--", rel)
        return int(out) if out is not None else None
    except (TypeError, ValueError):
        return None


def last_act_ts(root, seat: str, card=None) -> int | None:
    """The NEWEST of the seat's own stamp and its OWN card commit time, or None
    when neither is measurable. NEVER another seat's commit (conjunct 1)."""
    if card is None:
        card = own_card(root, seat)
    vals = [_stamp_ts(stamp_path(root, seat))]
    if card is not None:
        vals.append(card_commit_ts(root, card))
    vals = [v for v in vals if v is not None]
    return max(vals) if vals else None


def card_stale(root, seat: str, card, last_ts=_UNSET) -> tuple[bool, int | None]:
    """`(stale, last_act_ts)`. Stale iff the seat's last act is NEWER than the
    card — the seat worked after writing it.

    The card's OWN commit is the FLOOR, never an act after the card: git's %ct
    is the commit's whole second and is >= the write's mtime, so a literal
    `mtime < max(stamp, card_commit)` reads stale the instant the card is
    committed — the very loop this node removes. Stale therefore needs a LATER
    act (a stamp) than the card's own commit.

    A missing card, or an unmeasurable act, reads NOT stale (P7). `last_ts`
    lets a caller (the hook) pass its own monkeypatchable clock reading."""
    root = Path(root)
    card = Path(card)
    act = last_act_ts(root, seat, card) if last_ts is _UNSET else last_ts
    try:
        mtime = card.stat().st_mtime
    except OSError:
        return False, act                    # missing card: NOT stale (P7)
    if act is None:
        return False, None                   # unmeasurable: NOT stale (P7)
    own = card_commit_ts(root, card)
    return (mtime < act and (own is None or act > own)), act
