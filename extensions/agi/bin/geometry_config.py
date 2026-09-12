"""geometry_config.py — ONE resolver for the seats/posts geometry config.

`config:seats` is being renamed `config:posts` (hypothesis:l4-a-seat-is-a-post-
everywhere). For one season BOTH spellings resolve: `posts.md`/`posts:` is the
primary, `seats.md`/`seats:` is a deprecated alias. Every reader that opens the
geometry config, and every sink that spells the identity as `--seat`/`AGI_SEAT`,
routes through here so the post-first / seat-fallback behaviour and the
exactly-once-per-process deprecation notice live in ONE place instead of a
hand-rolled copy per reader.

Public API
----------
resolve(root) -> (Path | None, str)
    The geometry config file to read plus the frontmatter LIST KEY to read from
    it. Prefers ``<root>/nodes/.geometry/posts.md`` + ``posts:``; else falls
    back to ``<root>/nodes/.geometry/seats.md`` + ``seats:`` (emitting a
    deprecated-alias notice at most once per process); else
    ``(posts_path, "posts")`` so a caller with no file resolves to ``[]``.
    ``root`` None -> ``(None, "posts")``. Never raises.

geometry_config_path(root) -> Path | None
    Just the file path half of :func:`resolve` — for callers that need the
    exact file (e.g. the ack's single staged/committed path).

load_rows(root) -> list[dict]
    The config's list rows, post-first with the seats fallback, or ``[]`` when
    absent/unparseable. Never raises.

resolved_seat_env() -> str | None
    The seat identity from the environment: ``AGI_POST`` WINS over ``AGI_SEAT``
    when both are set (the deprecated ``AGI_SEAT`` spelling prints a notice at
    most once per process when it is the only spellingsource). None when
    neither is set — never a placeholder.

SeatAction(argparse.Action)
    argparse action for ``--seat``/``--post`` on the same parser (dest stays
    ``seat``, so no call site breaks). A literal ``--seat`` prints the
    deprecated-alias notice at most once per process.
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

_FILE_DEP_MSG = (
    "note: config:seats is deprecated; use config:posts "
    "(nodes/.geometry/posts.md with a `posts:` list). "
    "Falling back to the old seats.md layout this season."
)
_FLAG_DEP_MSG = (
    "note: --seat is deprecated; use --post this season."
)
_ENV_DEP_MSG = (
    "note: AGI_SEAT is deprecated; use AGI_POST this season."
)

# Module-level flags: the deprecated-alias notices fire AT MOST ONCE PER
# PROCESS, however many readers/consumers hit the fallback.
_seen_file = False
_seen_flag = False
_seen_env = False


def _print_once(msg: str, flag_holder: str) -> None:
    """Print a deprecation notice once per process (best effort, never raises)."""
    global _seen_file, _seen_flag, _seen_env
    if flag_holder == "file" and _seen_file:
        return
    if flag_holder == "flag" and _seen_flag:
        return
    if flag_holder == "env" and _seen_env:
        return
    if flag_holder == "file":
        _seen_file = True
    elif flag_holder == "flag":
        _seen_flag = True
    else:
        _seen_env = True
    try:
        print(msg, file=sys.stderr)
    except Exception:  # noqa: BLE001  (a notice must never break a reader)
        pass


def resolve(root: Path | None):
    """Return (geometry_config_path, list_key), post-first with a one-season
    seats fallback. See module docstring. Never raises."""
    if root is None:
        return None, "posts"
    posts = Path(root) / "nodes" / ".geometry" / "posts.md"
    if posts.exists():
        return posts, "posts"
    seats = Path(root) / "nodes" / ".geometry" / "seats.md"
    if seats.exists():
        _print_once(_FILE_DEP_MSG, "file")
        return seats, "seats"
    return posts, "posts"


def geometry_config_path(root: Path | None) -> Path | None:
    """Just the file path half of :func:`resolve`."""
    path, _ = resolve(root)
    return path


def load_rows(root: Path | None) -> list:
    """The config's `posts:`/`seats:` rows, post-first with the seats fallback,
    or [] when absent/unparseable. Never raises."""
    path, key = resolve(root)
    if path is None or not Path(path).exists():
        return []
    try:
        # Same engine node-loader every reader already uses, never a hand-rolled
        # copy of the frontmatter read.
        from graph_core.persistence import frontmatter

        nf = frontmatter.load_node_file(path)
        rows = nf.frontmatter.get(key) or []
        if isinstance(rows, list):
            return [r for r in rows if isinstance(r, dict)]
    except Exception:  # noqa: BLE001
        pass
    return []


def resolved_seat_env() -> str | None:
    """AGI_POST wins over AGI_SEAT when both are set (deprecated spelling
    notices at most once per process). None when neither — never a
    placeholder."""
    post = os.environ.get("AGI_POST")
    if post:
        return post
    seat = os.environ.get("AGI_SEAT")
    if seat:
        _print_once(_ENV_DEP_MSG, "env")
        return seat
    return None


class SeatAction(argparse.Action):
    """argparse action for `--seat`/`--post` on the same parser. dest stays
    `seat` (unlike `store`, a literal `--seat` emits the deprecated-alias
    notice at most once per process; `--post` is silent)."""

    def __call__(self, parser, namespace, values, option_string=None):
        if option_string == "--seat":
            _print_once(_FLAG_DEP_MSG, "flag")
        setattr(namespace, self.dest, values)


def _main(argv=None) -> int:
    """CLI front door: --help, and --root PATH prints the resolved post config
    and its rows so the module is genuinely runnable. Matches the OTHER bin/
    modules' convention so test_bin_help_smoke (which runs every bin/ script
    with --help expecting non-empty stdout and exit 0) passes."""
    ap = argparse.ArgumentParser(
        prog="geometry_config.py",
        description=(
            "Resolve the posts geometry config (nodes/.geometry/posts.md with a "
            "`posts:` list); the deprecated seats.md/`seats:` layout still "
            "resolves this season as an alias."
        ),
    )
    ap.add_argument(
        "--root",
        default=None,
        help="Project root to resolve the post config from (default: current "
             "working directory's nearest .agi project).",
    )
    args = ap.parse_args(argv)

    root = args.root
    if root is None:
        from graph_core.locations import find_root  # noqa: PLC0415

        try:
            root = find_root()
        except Exception:  # noqa: BLE001  (best effort for a print helper)
            root = None

    path, key = resolve(root)
    if path is not None:
        print(f"config: {path} (frontmatter key: {key})")
        rows = load_rows(root)
        for row in rows:
            print(f"  - {row.get('name', '?')}")
    else:
        print("config: <none>")
    return 0


if __name__ == "__main__":
    sys.exit(_main())
