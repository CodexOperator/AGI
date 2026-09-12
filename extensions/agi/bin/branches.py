#!/usr/bin/env python3
"""branches.py — the ONE grammar module for branch names (g15 round I).

Recursive grammar  S := season<n>/main | season<n>/<town>/S
(S is exactly the TOKEN SET A below — a post/loop branch is not token A but
branches *under* it and merges up into its main; the grammar module keys on
token sets A and B.)

Token set A (the node's trunk leaf — what a Council controls):
    season<n>/main                              core Council leaf
    season<n>/<town>/season<k>/main             that town's Council leaf

Token set B (branches under a node, merged up into its main):
    season<n>/posts/<name>
    season<n>/loops/<slug>-<agent>
    season<n>/<town>/season<k>/posts/<name>
    season<n>/<town>/season<k>/loops/<slug>-<agent>

Reserved leaves: main, posts, loops are NEVER a town name — refused.

Old names (`master`, `season/s<N>`, `seat/<name>@s<N>`, `loop/<slug>-<agent>@s<N>`,
`town/<town>/season/s<k>`, `town/<town>@s<N>`) are accepted as a DEPRECATED
alias for one season: parse() returns kind="alias" plus `canonical`, prints
one line per process, never raises.

Self-contained: stdlib only. Readers import THIS module — it never imports
them.
"""
from __future__ import annotations

import re
import sys

__all__ = [
    "season_main",
    "town_main",
    "post_branch",
    "loop_branch",
    "parse",
    "merge_target",
    "ref_candidates",
    "RESERVED",
]

RESERVED = ("main", "posts", "loops")

# One-time-per-process alias warning.
_warned = False

_MAIN_RE = re.compile(r"^season/s(\d+)$")
_SEAT_RE = re.compile(r"^seat/(.+?)@s(\d+)$")
_LOOP_AT_RE = re.compile(r"^loop/(.+?)@s(\d+)$")
_TOWN_S_RE = re.compile(r"^town/(.+?)/season/s(\d+)$")
_TOWN_AT_RE = re.compile(r"^town/(.+?)@s(\d+)$")

_ALIASES = {
    "master": ("season1/main", "master -> season1/main"),
}


def _warn(line: str) -> None:
    global _warned
    if not _warned:
        _warned = True
        print(f"branches.py: deprecated alias used: {line}", file=sys.stderr)


def _check_town(town: str) -> None:
    if town in RESERVED:
        raise ValueError(f"reserved leaf {town!r} cannot be a town name")


def ref_candidates(branch: str) -> list[str]:
    """The ref names a reader should try, CANONICAL FIRST then the old name as
    a one-season deprecated fallback, for a `branch` that may be either new or
    old. Old names are accepted, never refused: a live tree that has NOT been
    renamed yet must remain reachable under its legacy spelling. Returns
    ``[canonical]`` alone when no legacy spelling exists."""
    canonical = branch
    try:
        p = parse(branch)
    except ValueError:
        return [branch]
    if p.get("kind") == "alias":
        canonical = p["canonical"]
    old = _canonical_to_old(canonical)
    if old is None or old == canonical:
        return [canonical]
    return [canonical, old]


def _canonical_to_old(name: str) -> str | None:
    """The one-season DEPRECATED spelling of a canonical branch, or None.
    Inverts the alias table so readers can fall back to the old name while a
    live tree has not been renamed yet."""
    # season<n>/main -> season/s<n>
    m = re.fullmatch(r"season(\d+)/main", name)
    if m:
        return f"season/s{m.group(1)}"
    # season<n>/<town>/season<k>/main -> town/<town>/season/s<k>
    m = re.fullmatch(r"season(\d+)/(.+?)/season(\d+)/main", name)
    if m:
        _check_town(m.group(2))
        return f"town/{m.group(2)}/season/s{m.group(3)}"
    # season<n>/loops/<slug>-<agent> -> loop/<slug>-<agent>@s<n>
    m = re.fullmatch(r"season(\d+)/loops/(.+)", name)
    if m:
        return f"loop/{m.group(2)}@s{m.group(1)}"
    # season<n>/posts/<name> -> seat/<name>@s<n>
    # A `seat/<name>@s<N>` is the legacy spelling of a POST under that
    # season's main (branches.py parse: _SEAT_RE keys on the post branch, not
    # a town). Keep the old name so a reader handed a canonical POST name on
    # a pre-migration tree still finds the live seat branch.
    m = re.fullmatch(r"season(\d+)/posts/(.+)", name)
    if m:
        return f"seat/{m.group(2)}@s{m.group(1)}"
    return None


def season_main(n: int) -> str:
    """season<n>/main — the core Council leaf."""
    return f"season{n}/main"


def town_main(season: int, town: str, town_season: int) -> str:
    """season<n>/<town>/season<k>/main — that town's Council leaf."""
    _check_town(town)
    return f"season{season}/{town}/season{town_season}/main"


def post_branch(season: int, name: str) -> str:
    """season<n>/posts/<name> — a post branch merging up into season<n>/main."""
    return f"season{season}/posts/{name}"


def loop_branch(season: int, slug: str, agent: str) -> str:
    """season<n>/loops/<slug>-<agent> — a loop branch merging up into season<n>/main."""
    return f"season{season}/loops/{slug}-{agent}"


def merge_target(branch: str) -> str:
    """The main of the node a post/loop branch sits under.

    A post/loop under season<n>/main -> season<n>/main; under
    season<n>/<town>/season<k>/main -> that town main. Given the leaf itself
    (a token set A name), returns it unchanged.
    """
    parsed = parse(branch)
    if parsed["kind"] in ("post", "loop"):
        season = parsed["season"]
        town = parsed.get("town")
        if town is not None:
            return town_main(season, town, parsed["town_season"])
        return season_main(season)
    if parsed.get("kind") == "alias":
        try:
            return merge_target(parsed["canonical"])
        except ValueError:
            return parsed["canonical"]
    # A /main leaf is its own merge target.
    return branch


def parse(name: str) -> dict:
    """Parse a branch name into {kind, season, town, town_season, name}.

    kind is one of {main, town_main, post, loop, alias}. For kind == "alias"
    a `canonical` key holds the canonical replacement.
    """
    if not isinstance(name, str) or not name:
        raise ValueError(f"empty or non-string branch name: {name!r}")

    # --- deprecated aliases, accepted for one season ---
    canonical = _alias_canonical(name)
    if canonical is not None:
        _warn(f"{name} -> {canonical}")
        try:
            parsed = parse(canonical)
        except ValueError:
            # The alias canonical need not itself be a leaf (e.g.
            # seat/<name>@s<N> -> season<N>/<name>, a town node), so build a
            # minimal record rather than raising — aliases never refuse.
            parsed = {"kind": "town", "season": None, "name": canonical}
        parsed["kind"] = "alias"
        parsed["canonical"] = canonical
        return parsed

    parts = name.split("/")

    # season<n>/main
    if len(parts) == 2 and parts[0].startswith("season") and parts[1] == "main":
        n = _season_num(parts[0])
        return {"kind": "main", "season": n, "name": parts[0]}

    # season<n>/posts/<name>  |  season<n>/loops/<slug>-<agent>
    if len(parts) == 3 and parts[0].startswith("season"):
        n = _season_num(parts[0])
        if parts[1] == "posts":
            return {"kind": "post", "season": n, "name": parts[2]}
        if parts[1] == "loops":
            return {"kind": "loop", "season": n, "name": parts[2]}

    # season<n>/<town>/season<k>/main
    if len(parts) == 4 and parts[0].startswith("season") and parts[3] == "main" \
            and parts[2].startswith("season"):
        n = _season_num(parts[0])
        k = _season_num(parts[2])
        _check_town(parts[1])
        return {"kind": "town_main", "season": n, "town": parts[1],
                "town_season": k, "name": parts[1]}

    # season<n>/<town>/season<k>/posts/<name>
    # season<n>/<town>/season<k>/loops/<slug>-<agent>
    if len(parts) == 5 and parts[0].startswith("season") and parts[2].startswith("season"):
        n = _season_num(parts[0])
        k = _season_num(parts[2])
        _check_town(parts[1])
        if parts[3] == "posts":
            return {"kind": "post", "season": n, "town": parts[1],
                    "town_season": k, "name": parts[4]}
        if parts[3] == "loops":
            return {"kind": "loop", "season": n, "town": parts[1],
                    "town_season": k, "name": parts[4]}

    raise ValueError(f"unrecognised branch name: {name!r}")


def _season_num(seg: str) -> int:
    m = re.fullmatch(r"season(\d+)", seg)
    if not m:
        raise ValueError(f"bad season segment: {seg!r}")
    return int(m.group(1))


def _alias_canonical(name: str) -> str | None:
    """Map an OLD name to its canonical two-season form, else None.

    Never raises for a malformed alias — only the canonical comes back.
    """
    if name in _ALIASES:
        return _ALIASES[name][0]

    m = _MAIN_RE.fullmatch(name)
    if m:
        return season_main(int(m.group(1)))

    m = _SEAT_RE.fullmatch(name)
    if m:
        # A `seat/<name>@s<N>` is a POST branch under that season's main.
        return f"season{int(m.group(2))}/posts/{m.group(1)}"

    m = _LOOP_AT_RE.fullmatch(name)
    if m:
        # A `loop/<slug>-<agent>@s<N>` is a LOOP branch under that main.
        return f"season{int(m.group(2))}/loops/{m.group(1)}"

    m = _TOWN_S_RE.fullmatch(name)
    if m:
        _check_town(m.group(1))
        return town_main(2, m.group(1), int(m.group(2)))

    m = _TOWN_AT_RE.fullmatch(name)
    if m:
        _check_town(m.group(1))
        return town_main(int(m.group(2)), m.group(1), 1)

    return None


if __name__ == "__main__":
    import json as _json
    for arg in sys.argv[1:]:
        try:
            print(_json.dumps(parse(arg)))
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
