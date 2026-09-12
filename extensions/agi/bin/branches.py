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
    "derive_names",
    "is_remote_visible",
    "assert_remote_visible",
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

# v3 TOWN-FIRST trunk leaves (derive_names). These three regexes ARE the
# grammar's own remote-visible trunk shapes: the season main (`season<n>/main`,
# the same spell parse() and _canonical_to_old() recognise) plus the two
# town-first leaves (`<town>/main`, `<town>/season<m>/main`). No second
# hand-spelled list of branch shapes exists to drift from them — the predicate
# and the builder share one set.
_SEASON_MAIN_RE   = re.compile(r"^season(\d+)/main$")
_V3_TOWN_MAIN_RE  = re.compile(r"^([^/]+)/main$")
_V3_TOWN_SEASON_RE = re.compile(r"^([^/]+)/season(\d+)/main$")

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


def _v3_season_first(p: dict) -> list[str]:
    """The SEASON-FIRST spelling(s) a LIVE tree may still carry for a v3
    TOWN-FIRST record, derived from the same ONE tuple (town, town_season,
    post, round, agent). A v3 input resolved by ref_candidates must ALSO try
    the season-first form -- the live tree is held by the owner mid-rename,
    so a reader that only resolves v3 names breaks the live tree.

    A bare town main (`<town>/main`) is omitted: it carries NO season number,
    so no season-first town spelling is derivable, and inventing a parent or
    town season would be a guess. Everything else maps `<town>/season<m>/...`
    onto the season-first `season<m>/...` form the `derive_names` tuple's one
    season implies, and a v3 POST/LOOP falls back to the season-level
    `season<m>/posts/<p>` / `season<m>/loops/<round>-<agent>` (the v3 town
    qualifier is dropped -- the old world's live branch for a town's post is
    a post under that season's main). One spelling per shape, deduped at the
    caller; the one-season aliases of each are derived by _canonical_to_old.
    """
    kind = p.get("kind")
    town = p.get("town")
    n = p.get("town_season")
    if kind == "v3_town_main" or n is None:
        return []
    if kind == "v3_town_season_main":
        # season<m>: the tuple's ONE season fills both the parent and town
        # season of the season-first town main.
        return [f"season{n}/{town}/season{n}/main"]
    if kind == "v3_post":
        return [f"season{n}/posts/{p['name']}"]
    if kind == "v3_loop":
        return [f"season{n}/loops/{p['name']}"]
    return []


def ref_candidates(branch: str) -> list[str]:
    """The ref names a reader should try, CANONICAL FIRST then the legacy
    one-season spellings, for a `branch` that may be new, intermediate, or
    old. Old names are accepted, never refused: a live tree that has NOT been
    renamed yet must remain reachable under its legacy spelling. For a POST
    the candidates are, in order and deduped: the canonical
    ``season<n>/posts/<n>``, the INTERMEDIATE as-written ``post/<n>@s<n>``,
    and the legacy deprecated ``seat/<n>@s<n>``. The as-written input always
    appears in the result (it is one of the spellings for every input kind).
    For main/loop/town the intermediate and legacy spellings are the same
    old name deduped to one, except where a canonical carries TWO legacy
    spellings — ``season1/main`` also bears the pre-rename ``master``, and a
    town ``season<n>/<t>/season1/main`` also bears its one-season alias
    ``town/<t>@s<n>`` — in which case both are listed, canonical first.
    Returns ``[canonical]`` alone when no legacy spelling exists."""
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
    out = [canonical]
    for cand in (*inter, *legacy):
        if cand in out:
            continue
        out.append(cand)
    # v3 TOWN-FIRST input: as-written already first (canonical == branch for a
    # v3 kind). Append the season-first spelling(s) a live tree may still
    # carry, then each of THOSE one-season aliases -- a reader handed a v3
    # name must still reach the season-first live branch until the rename
    # lands (hypothesis l4-every-branch-name-derives-from-one-tuple-...).
    if p.get("kind", "").startswith("v3"):
        for sf in _v3_season_first(p):
            if sf not in out:
                out.append(sf)
            for cand in (*_canonical_to_old(sf),
                         *_canonical_to_old(sf, legacy_seat=True)):
                if cand not in out:
                    out.append(cand)
    return out


def _canonical_to_old(name: str, *, legacy_seat: bool = False) -> list[str]:
    """The one-season DEPRECATED spellings of a canonical branch, deduped.
    Empty when the canonical has no legacy spelling. Each reverse row yields
    EVERY pre-rename alias a live tree may still carry, so the as-written
    input is always reachable until the tree is renamed (hypothesis
    l4-an-empty-or-blank-explicit-kinds-is-refused-and-every-branch-spelling-
    is-in-its-own-ref-candidates — the docstring must be true). Inverts the
    alias table so readers can fall back to the old name."""
    # season<n>/main -> [season/s<n>]; season1/main also bears the pre-rename
    # spelling `master` (is_legal_branch accepts it; _ALIASES maps it here).
    m = re.fullmatch(r"season(\d+)/main", name)
    if m:
        out = [f"season/s{m.group(1)}"]
        if m.group(1) == "1":
            out.append("master")
        return out
    # season<n>/<town>/season<k>/main -> [town/<town>/season/s<k>]; and, when
    # k==1, the one-season town alias town/<town>@s<n> (which canonicalises
    # back to town_main(n, town, 1)) is also a reachable old spelling.
    m = re.fullmatch(r"season(\d+)/(.+?)/season(\d+)/main", name)
    if m:
        _check_town(m.group(2))
        out = [f"town/{m.group(2)}/season/s{m.group(3)}"]
        if m.group(3) == "1":
            out.append(f"town/{m.group(2)}@s{m.group(1)}")
        return out
    # season<n>/loops/<slug>-<agent> -> loop/<slug>-<agent>@s<n>
    m = re.fullmatch(r"season(\d+)/loops/(.+)", name)
    if m:
        return [f"loop/{m.group(2)}@s{m.group(1)}"]
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
        return [spell]
    return []


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


def derive_names(town: str, town_season: int,
                 post: str | None = None,
                 round: str | None = None,
                 agent: str | None = None) -> dict:
    """v3 TOWN-FIRST branch names, all derived from the ONE tuple
    (town, town_season, post, round, agent).

    Keys and values:
      town_main        -> "<town>/main"
      town_season_main -> "<town>/season<m>/main"
      post_main        -> "<town>/season<m>/posts/<post>/main"  (post given)
      loop             -> "<town>/season<m>/posts/<post>/loops/<round>/<agent>"
                          (post AND round AND agent given)

    `town` is validated by the module's own `_check_town` (RESERVED =
    main/posts/loops refused). `town_season` is an int >= 1. A key is PRESENT
    only when its inputs are present; town_main and town_season_main are
    always present. Every level is a DIR with a `main` leaf because git
    forbids a ref that is both leaf and dir — hence `<town>/main`, never a
    bare `<town>`. This is the grammar-only half of the round; the live
    SEASON-FIRST spellings (parse/_canonical_to_old) are unchanged and added
    alongside, never replaced.
    """
    _check_town(town)
    if not isinstance(town_season, int) or isinstance(town_season, bool) \
            or town_season < 1:
        raise ValueError(
            f"town_season must be an int >= 1, got {town_season!r}")
    out = {
        "town_main": f"{town}/main",
        "town_season_main": f"{town}/season{town_season}/main",
    }
    if post is not None:
        out["post_main"] = \
            f"{town}/season{town_season}/posts/{post}/main"
        if round is not None and agent is not None:
            out["loop"] = \
                f"{town}/season{town_season}/posts/{post}/loops/{round}/{agent}"
    return out


def is_remote_visible(name: str) -> bool:
    """True for EXACTLY `master`, `season<n>/main`, `<town>/main`,
    `<town>/season<m>/main` — the trunk pair per level that reaches origin.
    Everything else (a post, loop, feature branch, a reserved or malformed
    town, a bare town with no leaf) is False. NEVER raises: a name that does
    not parse is simply not remote-visible, and returning False for it is
    correct. `season<n>/main` stays visible (it is the Prime's leaf), which is
    why `is_remote_visible("season2/main") is True` while
    `is_remote_visible("season2/posts/x") is False`.
    """
    if not isinstance(name, str) or not name:
        return False
    if name == "master":
        return True
    if _SEASON_MAIN_RE.fullmatch(name):
        return True
    m = _V3_TOWN_MAIN_RE.fullmatch(name)
    if m and m.group(1) not in RESERVED:
        return True
    m = _V3_TOWN_SEASON_RE.fullmatch(name)
    if m and m.group(1) not in RESERVED:
        return True
    return False


def assert_remote_visible(name: str) -> None:
    """Raise ValueError naming the branch AND the rule when `name` is not
    remote-visible — the 'push of any sub-top-level name to refs/heads is
    refused by name' falsifier. Returns None when the branch is remote-visible.
    """
    if not is_remote_visible(name):
        raise ValueError(
            f"branch {name!r} refused by name: only the trunk pair per level "
            f"(master, season<n>/main, <town>/main, <town>/season<m>/main) "
            f"reaches origin, so {name!r} is not remote-visible")
    return None


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
    if len(parts) == 2 and re.fullmatch(r"season\d+", parts[0]) \
            and parts[1] == "main":
        n = _season_num(parts[0])
        return {"kind": "main", "season": n, "name": parts[0]}

    # season<n>/posts/<name>  |  season<n>/loops/<slug>-<agent>
    if len(parts) == 3 and re.fullmatch(r"season\d+", parts[0]):
        n = _season_num(parts[0])
        if parts[1] == "posts":
            return {"kind": "post", "season": n, "name": parts[2]}
        if parts[1] == "loops":
            return {"kind": "loop", "season": n, "name": parts[2]}

    # season<n>/<town>/season<k>/main
    if len(parts) == 4 and re.fullmatch(r"season\d+", parts[0]) \
            and parts[3] == "main" and re.fullmatch(r"season\d+", parts[2]):
        n = _season_num(parts[0])
        k = _season_num(parts[2])
        _check_town(parts[1])
        return {"kind": "town_main", "season": n, "town": parts[1],
                "town_season": k, "name": parts[1]}

    # season<n>/<town>/season<k>/posts/<name>
    # season<n>/<town>/season<k>/loops/<slug>-<agent>
    if len(parts) == 5 and re.fullmatch(r"season\d+", parts[0]) \
            and re.fullmatch(r"season\d+", parts[2]):
        n = _season_num(parts[0])
        k = _season_num(parts[2])
        _check_town(parts[1])
        if parts[3] == "posts":
            return {"kind": "post", "season": n, "town": parts[1],
                    "town_season": k, "name": parts[4]}
        if parts[3] == "loops":
            return {"kind": "loop", "season": n, "town": parts[1],
                    "town_season": k, "name": parts[4]}

    # --- v3 TOWN-FIRST shapes (derive_names: the ONE tuple) ---
    # Reached only when parts[0] is NOT a season prefix, so these cannot
    # shadow the season-first rules above. New kinds so the existing
    # `kind == "main"` contract (is_legal_branch, verification's
    # _integration_branch_candidates) is untouched.
    if len(parts) == 2 and parts[1] == "main" \
            and not re.fullmatch(r"season\d+", parts[0]):
        _check_town(parts[0])
        return {"kind": "v3_town_main", "town": parts[0], "name": parts[0]}
    if len(parts) == 3 and parts[2] == "main" \
            and re.fullmatch(r"season\d+", parts[1]) \
            and not re.fullmatch(r"season\d+", parts[0]):
        m = re.fullmatch(r"season(\d+)", parts[1])
        if m:
            _check_town(parts[0])
            return {"kind": "v3_town_season_main", "town": parts[0],
                    "town_season": int(m.group(1)), "name": parts[0]}
    if len(parts) == 5 and parts[4] == "main" and parts[2] == "posts" \
            and re.fullmatch(r"season\d+", parts[1]) \
            and not re.fullmatch(r"season\d+", parts[0]):
        m = re.fullmatch(r"season(\d+)", parts[1])
        if m:
            _check_town(parts[0])
            return {"kind": "v3_post", "town": parts[0], "name": parts[3],
                    "town_season": int(m.group(1))}
    if len(parts) == 7 and parts[2] == "posts" and parts[4] == "loops" \
            and re.fullmatch(r"season\d+", parts[1]) \
            and not re.fullmatch(r"season\d+", parts[0]):
        m = re.fullmatch(r"season(\d+)", parts[1])
        if m:
            _check_town(parts[0])
            # the tuple's round and agent are separate segments; the
            # season-first loop spelling joins them with a dash.
            return {"kind": "v3_loop", "town": parts[0], "name":
                    f"{parts[5]}-{parts[6]}",
                    "town_season": int(m.group(1))}

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
