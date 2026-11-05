"""geometry_config.py — ONE resolver for the seats/posts geometry config.

`config:seats` is being renamed `config:posts` (hypothesis:l4-a-seat-is-a-post-
everywhere). For one season BOTH spellings resolve: `posts.md`/`posts:` is the
primary, `seats.md`/`seats:` is a deprecated alias. Every reader that opens the
geometry config, and every sink that spells the identity as `--seat` or an env name,
routes through here so the post-first / seat-fallback behaviour and the
exactly-once-per-process seat/environment deprecation notices live in ONE
place instead of a hand-rolled copy per reader. The seats.md fallback prints
NO deprecation notice: a notice naming a migration target only reachable on a
tree where that target does not exist would be a lie on exactly the trees
where it fired (hypothesis:l4-the-config-posts-note-is-silent-until-posts-md-
exists).

Public API
----------
resolve(root) -> (Path | None, str)
    The geometry config file to read plus the frontmatter LIST KEY to read from
    it. Prefers ``<root>/nodes/.geometry/posts.md`` + ``posts:``; else falls
    back to ``<root>/nodes/.geometry/seats.md`` + ``seats:`` (silently — no
    deprecation notice, since posts.md is absent by definition on this branch
    and the old notice's advice was untakeable); else
    ``(posts_path, "posts")`` so a caller with no file resolves to ``[]``.
    ``root`` None -> ``(None, "posts")``. Never raises.

geometry_config_path(root) -> Path | None
    Just the file path half of :func:`resolve` — for callers that need the
    exact file (e.g. the ack's single staged/committed path).

load_rows(root) -> list[dict]
    The config's list rows, post-first with the seats fallback, or ``[]`` when
    absent/unparseable. Never raises.

resolved_seat_env() -> str | None
    The seat identity from the environment: ``AGI_POST``. The ONE reader of the
    retired spelling (goal:g7.16.1.11.37): it falls back to it only for a v4 row
    and prints a notice at most once per process when it is the only source.
    This fallback is deleted in the commit that moves the last v4 row to v5.
    None when neither is set — never a placeholder.

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

_FLAG_DEP_MSG = (
    "note: --seat is deprecated; use --post this season."
)

# Module-level flag: the deprecated-alias notice (the --seat flag spelling)
# fires AT MOST ONCE PER PROCESS, however many readers/consumers hit it. There
# is deliberately NO file-level notice: the seats.md fallback is silent.
_seen_flag = False


def _print_once(msg: str, flag_holder: str) -> None:
    """Print a deprecation notice once per process (best effort, never raises).
    Only the `--seat` flag remains live; there is no file fallback notice."""
    global _seen_flag
    if flag_holder == "flag" and _seen_flag:
        return
    _seen_flag = True
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
        # Silent fallback: no deprecation notice. posts.md is absent here by
        # construction (we only reach this branch when it does not exist), so
        # the old notice's advice was untakeable on exactly the trees where it
        # fired. Keeping it would be a lie; deleted instead.
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


MEM_VALUES = ("full", "season", "goal", "none")
FACES_VALUES = ("owner", "posts", "none")


def cell_errors(root: Path | None) -> list:
    """goal:g7.16.1.11.46.13 R7: the ONE check of a row's `mem:` and `faces:`
    cells. An absent `mem:` reads `none`, an absent `faces:` reads `none`;
    `faces: owner` without `mem: full` is refused, each by one named line."""
    out = []
    for row in load_rows(root):
        who, mem, faces = row.get("name", "?"), row.get("mem") or "none", row.get("faces") or "none"
        if mem not in MEM_VALUES:
            out.append(f"[cells] {who}: mem: {mem} is not {'|'.join(MEM_VALUES)}")
        elif faces not in FACES_VALUES:
            out.append(f"[cells] {who}: faces: {faces} is not {'|'.join(FACES_VALUES)}")
        elif faces == "owner" and mem != "full":
            out.append(f"[cells] {who}: faces: owner requires mem: full (has mem: {mem})")
    return out


def resolved_seat_env() -> str | None:
    """AGI_POST, the one identity variable (goal:g7.16.1.11.46.11 V10a: the
    retired spelling's fallback is gone). None when unset — never a placeholder."""
    return os.environ.get("AGI_POST") or None


def default_actor(root=None) -> str:
    """Who a write with no `--actor` is stamped as (goal:g7.33.20.2, R1; moved
    here from write._default_actor by goal:g7.16.1.11.46.23 V8a, no change).

    AGI_ACTOR, else the RESOLVED SEAT (AGI_POST), else the unix
    user PROVABLY not a post's name (every post runs as the user named like the
    Prime's seat, `belam`, so `$USER` there names the Prime, not the writer),
    else `unknown`. Fail CLOSED: when the collision check cannot run -- no project
    root resolved, the posts list unreadable, missing or empty -- `$USER` is never
    returned. `root` reads the posts list; None resolves it from the cwd."""
    actor = os.environ.get("AGI_ACTOR") or resolved_seat_env()
    if actor:
        return actor
    user = os.environ.get("USER")
    if not user:
        return "unknown"
    try:
        if root is None:
            import locations  # noqa: PLC0415  (local: same dir, no cycle)

            root = locations.find_project_root(Path.cwd())
        rows = load_rows(root) if root is not None else []
        if not rows or any(r.get("name") == user for r in rows):
            return "unknown"
    except Exception:  # noqa: BLE001 -- the check cannot run: fail closed, never $USER
        return "unknown"
    return user


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
    ap.add_argument(
        "--cells",
        action="store_true",
        help="Check the mem:/faces: cells of every row (goal:g7.16.1.11.46.13 R7): "
             "one named line per refusal, rc 1 if any.",
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
    if args.cells:
        sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
        errs, n = cell_errors(root), len(load_rows(root))
        if not n:   # a check over no rows proves nothing: never a bare ok
            errs = [f"[cells] no rows read from {path}"]
        print("\n".join(errs) if errs else f"cells: ok ({n} rows)")
        return 1 if errs else 0

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
