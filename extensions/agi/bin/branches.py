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
one line per process, never raises. `post/<name>@s<N>` is the INTERMEDIATE
alias of a post (the seat->post rename's mid-point) and resolves the same way
to `season<N>/posts/<name>`.


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
    "is_legal_branch",
    "RESERVED",
]

RESERVED = ("main", "posts", "loops")

# One-time-per-process alias warning.
_warned = False

_MAIN_RE = re.compile(r"^season/s(\d+)$")
_SEAT_RE = re.compile(r"^seat/(.+?)@s(\d+)$")
_POST_AT_RE = re.compile(r"^post/(.+?)@s(\d+)$")
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


def is_legal_branch(name: str) -> bool:
    """True ONLY for `master` or the season MAIN — canonical `season<N>/main`
    or its one-season alias `season/s<N>`; False for everything else.

    The grid's `commit --all` runs unattended under a 5-min cron and writes the
    same ref namespace from any worktree, so it may only run on a branch every
    node's refs resolve identically on — the season main (or master, inherited
    from the l2w15 guard). A post, loop or town-main branch in EITHER spelling
    (season2/posts/x | season2/loops/x | season2/<t>/season<k>/main, and their
    legacy seat/…@s<N>, loop/…@s<N>, town/… forms), a feature branch, a
    malformed season name, and empty/detached-HEAD names are all refused. The
    refusal is a real decision, not the old `startswith("season/")` rule
    (which both admitted every live branch AND broke on the canonical
    `"season2/main".startswith("season/")`).
    """
    if name == "master":
        return True
    try:
        p = parse(name)
    except ValueError:
        return False
    if p.get("kind") == "alias":
        # One-season alias: legal only for the core season main (season/s<N>).
        # A town alias (town/<t>/season/s<k>, town/<t>@s<N>) canonicalises to
        # a town_main, a post/loop alias (seat/x@s<N>, loop/x-a@s<N>) to a
        # post/loop — all of those stay refused.
        try:
            return parse(p["canonical"]).get("kind") == "main"
        except ValueError:
            return False
    return p.get("kind") == "main"


def ref_candidates(branch: str) -> list[str]:
    """The ref names a reader should try, CANONICAL FIRST then the legacy
    one-season spellings, for a `branch` that may be new, intermediate, or
    old. Old names are accepted, never refused: a live tree that has NOT been
    renamed yet must remain reachable under its legacy spelling. For a POST
    the candidates are, in order and deduped: the canonical
    ``season<n>/posts/<n>``, the INTERMEDIATE as-written ``post/<n>@s<n>``,
    and the legacy deprecated ``seat/<n>@s<n>``. The as-written input always
    appears in the result (it is one of the three spellings for every input
    kind). For main/loop/town the intermediate and legacy spellings are the
    same single old name, deduped to one. Returns ``[canonical]`` alone when
    no legacy spelling exists."""
    canonical = branch
    try:
        p = parse(branch)
    except ValueError:
        return [branch]
    if p.get("kind") == "alias":
        canonical = p["canonical"]
    # intermediate is the as-written post/<n>@s<n> for a post (g17.1 ruling);
    # legacy is the even-older seat/<n>@s<n> deprecated spelling. Both dedupe
    # to one for main/loop/town, where they are the same old name.
    inter = _canonical_to_old(canonical)
    legacy = _canonical_to_old(canonical, legacy_seat=True)
    out = []
    for cand in (canonical, inter, legacy):
        if cand is None or cand in out:
            continue
        out.append(cand)
    return out or [canonical]


def _canonical_to_old(name: str, *, legacy_seat: bool = False) -> str | None:
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
    # season<n>/posts/<name> -> post/<name>@s<n>
    # The INTERMEDIATE spelling the seat->post rename moves through (cli.py
    # branch --apply renames `seat/<n>@s2` to `post/<n>@s2`, then re-points
    # onto the canonical `season<n>/posts/<n>`). It is the reverse of the
    # `_POST_AT_RE` intermediate rule added in L4.319. The even-older
    # `seat/<name>@s<N>` DEPRECATED spelling is kept reachable via
    # `legacy_seat=True` (ref_candidates passes it, so a reader handed a
    # canonical POST name on a PRE-migration tree still finds the live seat
    # branch; `_SEAT_RE` also still parses it as an input). Default returns
    # the intermediate, per the g17.1 ruling that `post/<n>@sN` is the
    # intermediate alias to season<n>/posts/<n>.
    m = re.fullmatch(r"season(\d+)/posts/(.+)", name)
    if m:
        spell = f"seat/{m.group(2)}@s{m.group(1)}" if legacy_seat \
            else f"post/{m.group(2)}@s{m.group(1)}"
        return spell
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

    m = _POST_AT_RE.fullmatch(name)
    if m:
        # A `post/<name>@s<N>` is a POST branch under that season's main —
        # the intermediate spelling the seat->post rename moves through.
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
    import argparse as _argparse
    import json as _json

    _p = _argparse.ArgumentParser(
        prog="branches.py",
        description="Parse branch names into the season grammar (node JSON per arg).")
    _p.add_argument("names", nargs="*", help="branch names to parse")
    _a = _p.parse_args()
    for arg in _a.names:
        try:
            print(_json.dumps(parse(arg)))
        except ValueError as exc:
            print(f"error: {exc}", file=sys.stderr)
