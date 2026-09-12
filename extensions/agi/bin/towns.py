#!/usr/bin/env python3
"""towns.py — load town:* super nodes (g15 round I-3b).

A town is a super node (owner ruling 2026-09-12): its cells are `visions`,
`council`, `season`, `season_history` — and its BRANCH NAMES are DERIVED from
those cells, never stored. Reading `town:*` nodes is what `crons.py apply`
does for `crons.md`; the towns are the declared rows.

Readers alive + deprecated, live first (CLAUDE.md convention): every glob of
`nodes/town/` ALSO reads `nodes/deprecated/town/`, so a retired town keeps
being seen and its cells keep resolving.

Refusals are BY NAME — each message names the offending town and field:
  1. a town with no visions,
  2. a council that names no config:posts row,
  3. a vision claimed by two towns,
  4. a `branches:` cell present at all (branches is DERIVED, never a cell).

`visions: auto` resolves at READ TIME to every vision no OTHER town claims —
never hardcoded.

Self-contained: stdlib + the engine node reader only.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

# Same two inserts every bin module carries (write.py:60-61): graph_core lives
# under extensions/agi/src, so the CLI and a plain `import towns` from a
# sibling module resolve it without pytest's conftest on the path (director
# fix at the L4.333 harvest — the merged bytes raised ModuleNotFoundError from
# `python3 extensions/agi/bin/towns.py .agi --tuples`).
sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from graph_core.persistence.frontmatter import load_node_file as _load_node_file  # noqa: E402

__all__ = ["Town", "TownError", "load_towns", "town_tuples", "derive_names"]

AUTO = "auto"


class TownError(Exception):
    """A town node violates the schema — refused BY NAME (see message)."""


@dataclass
class Town:
    """One loaded town super node."""

    slug: str
    visions: list = field(default_factory=list)     # resolved vision node ids
    council: str = ""
    season: int = 0
    season_history: list = field(default_factory=list)
    mint_id: str = ""
    # True if the node spelled `visions: auto` (kept for provenance).
    visions_was_auto: bool = False

    @property
    def derives(self) -> list[str]:
        """The town's derived branch names (the ruling's table), from cells."""
        return derive_names(self.slug, self.season)


def _graph_dir(root) -> Path:
    """Accept EITHER the graph dir (`.agi/`, holding `nodes/`) or the project
    root that contains it — `find_project_root()` returns the graph dir, a
    human passes the checkout. A wrong root must not read as "no towns" and
    silently take a caller's fallback (director fix, L4.333 harvest)."""
    r = Path(root)
    if (r / "nodes").is_dir():
        return r
    if (r / ".agi" / "nodes").is_dir():
        return r / ".agi"
    return r


def _town_dirs(root: Path) -> list[Path]:
    """nodes/town/ then nodes/deprecated/town/ — live first, exist-only."""
    base = _graph_dir(root) / "nodes"
    live = base / "town"
    dep = base / "deprecated" / "town"
    out: list[Path] = []
    if live.is_dir():
        out.append(live)
    if dep.is_dir():
        out.append(dep)
    return out


def _read_council_rows(root: Path) -> dict[str, dict]:
    """The config:posts row name -> row map, post-first with the deprecated
    seats.md/`seats:` sibling — same resolver shape as geometry_config.py."""
    geom = _graph_dir(root) / "nodes" / ".geometry"
    rows: list[dict] = []
    seen = set()
    for filename in ("posts.md", "seats.md"):
        p = geom / filename
        if not p.is_file():
            continue
        nf = _load_node_file(p, body=False)
        lst = nf.frontmatter.get("posts") or nf.frontmatter.get("seats")
        if not lst:
            continue
        rows = lst
        break
    return {r.get("name"): r for r in rows if r.get("name")}


def _load_one(path: Path) -> Town:
    nf = _load_node_file(path, body=False)
    fm = nf.frontmatter
    slug = str(fm.get("id", "")).replace("town:", "")
    kind = fm.get("type")
    # Only accept files that carry a town id/type; skip unrelated files.
    if not slug or (kind is not None and kind != "town"):
        return None
    visions = fm.get("visions")
    council = fm.get("council")
    season = fm.get("season")
    season_history = fm.get("season_history") or []
    mint_id = str(fm.get("mint_id", ""))
    if season is None:
        season = 0
    return Town(
        slug=slug,
        visions=list(visions) if isinstance(visions, list) else [],
        council=str(council or ""),
        season=int(season) if isinstance(season, int) else int(season or 0),
        season_history=list(season_history),
        mint_id=mint_id,
        visions_was_auto=(visions == AUTO),
    )


def _all_vision_ids(root: Path) -> set[str]:
    """Every vision node id under nodes/vision + nodes/deprecated/vision,
    live first (CLAUDE.md retired-sibling convention).

    `visions: auto` resolves against THIS set: a vision is auto-owned only if
    it is a real vision node AND no other town claims it.
    """
    ids: set[str] = set()
    base = _graph_dir(root) / "nodes"
    for d in (base / "vision", base / "deprecated" / "vision"):
        if not d.is_dir():
            continue
        for p in d.glob("*.md"):
            try:
                nf = _load_node_file(p, body=False)
            except Exception:
                continue
            vid = nf.frontmatter.get("id")
            if vid:
                ids.add(str(vid))
    return ids


def _resolve_visions(root: Path, all_towns: list[Town]) -> None:
    """Resolve explicit + auto lists into each town's OWNED set.

    Explicit vision ids must not be claimed by two towns (refusal 3). An
    `auto` town resolves to every VISION NODE no other town claims,
    computed by the loader over nodes/vision — never hardcoded.
    """
    explicit: dict[str, str] = {}   # vision id -> town slug (for dup check)
    for t in all_towns:
        if t.visions_was_auto:
            continue
        for vid in list(t.visions):
            owner = explicit.get(vid)
            if owner is not None and owner != t.slug:
                raise TownError(
                    f"vision claimed by two towns: {vid!r} in {owner!r} and "
                    f"{t.slug!r} (town:{t.slug})"
                )
            explicit[vid] = t.slug
    all_vision_ids = _all_vision_ids(root)
    for t in all_towns:
        if t.visions_was_auto:
            claimed = set(explicit)
            t.visions = sorted(all_vision_ids - claimed)
        else:
            t.visions = list(t.visions)


def _validate(t: Town, council_names: set[str]) -> None:
    """Refusals 1, 2, 4 — each BY NAME."""
    if not t.visions:
        raise TownError(f"town with no visions: {t.slug!r} (town:{t.slug}) refuses")
    if not t.council or t.council not in council_names:
        raise TownError(
            f"council names no config:posts row: town:{t.slug} council={t.council!r}"
        )
    if t.season <= 0:
        raise TownError(f"town with non-positive season: town:{t.slug} season={t.season!r}")


def load_towns(root) -> list[Town]:
    """Load and validate every town node under ``root`` — the graph dir
    (``.agi/``) or the project root that contains it (live + deprecated, live
    first). Raises TownError on the first schema violation, BY NAME."""
    root = Path(root)
    towns: list[Town] = []
    for d in _town_dirs(root):
        for p in sorted(d.glob("*.md")):
            t = _load_one(p)
            if t is not None:
                towns.append(t)

    # Refusal 4: `branches:` is DERIVED, never a cell — checked on raw frontmatter.
    for d in _town_dirs(root):
        for p in sorted(d.glob("*.md")):
            nf = _load_node_file(p, body=False)
            if "branches" in nf.frontmatter:
                raise TownError(
                    f"`branches:` is DERIVED, never a cell: town:"
                    f"{str(nf.frontmatter.get('id','')).replace('town:','')!r}"
                )

    if not towns:
        raise TownError("no town:* nodes found under nodes/town (or nodes/deprecated/town)")

    row_map = _read_council_rows(root)
    _resolve_visions(root, towns)
    for t in towns:
        _validate(t, set(row_map))
    return towns


def _ladder_global_season(root: Path) -> int:
    """The ladder's current_season — the GLOBAL counter a town_tuples row carries."""
    p = _graph_dir(root) / "nodes" / ".geometry" / "ladder.md"
    try:
        nf = _load_node_file(p, body=False)
        return int(nf.frontmatter.get("current_season", 0) or 0)
    except Exception:
        return 0


def town_tuples(root) -> list[dict]:
    """[{town, season, global_season, council}] — season is the town's OWN
    counter; global_season is the ladder's; council is the posts row name."""
    towns = load_towns(root)
    gs = _ladder_global_season(root)
    out = []
    for t in sorted(towns, key=lambda x: x.slug):
        out.append({
            "town": t.slug,
            "season": t.season,
            "global_season": gs,
            "council": t.council,
        })
    return out


def derive_names(town: str, season: int, post: str = "", loop_round: str = "",
                 agent: str = "") -> list[str]:
    """The DERIVED branch names of a town, from its cells, as the ruling's
    ordered table (town main, town-season main, then the post main and the
    loop leaf when `post` / `loop_round` + `agent` are given).

    ONE derivation: this delegates to `branches.derive_names` (I-3a, the
    grammar module that owns every branch shape) and flattens its dict in
    table order. Director fix at the L4.332/L4.333 harvest: the round's own
    f-string table was a second hand-spelled derivation that the spelling
    grep pinned as debt; now no shape is spelled here.
    """
    from branches import derive_names as _derive  # sibling module, same dir

    d = _derive(town, season, post or None,
                loop_round or None if post else None,
                agent or None if post else None)
    out = [d["town_main"], d["town_season_main"]]
    if post:
        out.append(d["post_main"])
        if "loop" in d:
            out.append(d["loop"])
    return out


def _main(argv=None) -> int:
    import argparse

    argv = sys.argv[1:] if argv is None else argv
    ap = argparse.ArgumentParser(prog="towns.py")
    ap.add_argument("root", nargs="?", default=".",
                    help="the graph dir (.agi/) or the project root containing it")
    ap.add_argument("--tuples", action="store_true",
                    help="print town_tuples rows")
    args = ap.parse_args(argv)
    try:
        if args.tuples:
            for row in town_tuples(args.root):
                print(row)
        else:
            for t in load_towns(args.root):
                print(f"{t.slug} council={t.council} season={t.season} "
                      f"visions={t.visions} derives={t.derives}")
    except TownError as e:
        print(f"towns.py: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(_main())