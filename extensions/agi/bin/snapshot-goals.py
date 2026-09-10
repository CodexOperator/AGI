#!/usr/bin/env python3
"""snapshot-goals.py — convert GOALS.md into first-class nodes under nodes/goal/.

Reads `<PROJECT_ROOT>/GOALS.md` (human-authored prose) and writes one frontmatter
file per goal heading of the form:

    ## G1 — Playable dungeon crawler (sandbox ladder) — status: active

Output: `nodes/goal/<gid-lower>-<slug-of-title>.md`, node id `goal:g1`.

Linkage is parent-pointing: a node joins a goal by listing the goal node id in
its own `parents:` list (e.g. `parents: [goal:g2]`). render-context.py already
turns `parents` into `spawns` edges, so goals traverse and render for free.
This script only *reads* those parent pointers to compute each goal's `seeds:`
list — it never emits `next_edges` and never touches chain shape.

Pruning is H0-safe: only files stamped `origin: goals-doc` that were not written
this run are removed. A missing GOALS.md is a no-op (prunes nothing).

Run: `python3 bin/snapshot-goals.py [--strict] [--project PATH]`
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import yaml
from pathlib import Path

ORIGIN = "goals-doc"
# `horizon` = declared and committed to, but deliberately not being worked yet.
# It is what lets L5 goal rotation distinguish queued goals from active ones.
# The `cc_dispatch.max_goals_active` cap that this used to reference was
# deleted 2026-09-06 (owner decision, re-brief of hypothesis:
# l2-goals-active-exempt) — long-term goals are `goal_kind: perpetual` and
# there is no active-goal cap to trip.
# `retired` is canonical (goal:g5, renamed 2026-09-02). `phasing-out` is the
# legacy spelling and stays accepted forever, not through one migration
# window: projects predating the rename carry it, and this set only decides
# whether to WARN. Dropping it would print a spurious warning on every goal in
# every such project — the S11 sequence's reader-accepts-both step, made
# permanent because there is no second writer to migrate them.
KNOWN_STATUSES = {"active", "horizon", "retired", "phasing-out", "complete"}
# Default only. `goal_body_cap` in the project config overrides it and `0`
# disables capping entirely — see `body_cap()` / `cap_body()` and goal:s12,
# which separates "silent truncation is always wrong" (a bug, fixed
# unconditionally) from "what the cap should be" (policy, the owner's).
BODY_CAP = 4000

PLUGIN_ROOT = Path(__file__).resolve().parent.parent

# goal:g11 — one resolver for every path. `bin/` is already on sys.path for
# every entry point here, so this is a plain sibling import.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import locations  # noqa: E402
from node_writer import log_write  # noqa: E402

#: **goal:g11.1's first casualty, found the hour the layout changed.** This was
#: `... or os.getcwd()`: an env var, else whatever directory you happened to be
#: standing in. Under the old layout that was harmless, because cwd *was* the
#: graph root. Under `.agi/` it is not — the graph root is `<repo>/.agi` and cwd
#: is `<repo>` — so `snapshot-goals.py --render` looked for `<repo>/nodes/goal`,
#: found nothing, and refused.
#:
#: **It refused rather than writing an empty `GOALS.md`, which is the only
#: reason this is a bug report and not a data-loss incident** (goal:s12 added
#: that guard). The failure was loud and safe; the resolver was simply wrong.
#:
#: `project_root_from_env` keeps the same env-var precedence and replaces the
#: cwd fallback with the real ancestor walk. Nine `bin/` entry points still
#: carry their own copy of the old rule — that is exactly `goal:g11.1`, and
#: this is the evidence that it is a live defect rather than tidiness.
PROJECT_ROOT = locations.project_root_from_env() or Path(os.getcwd()).resolve()


# graph_core.identity — the ENGINE's own copy, for the same reason
# backfill-mint-ids.py insists on it: a project's vendored src/ predates
# `mint_permanent_id` and cannot have a compatible one.
_graph_core_src = str(PLUGIN_ROOT / "src")
if _graph_core_src not in sys.path:
    sys.path.insert(0, _graph_core_src)
from graph_core.identity import mint_permanent_id, is_valid_mint_id  # noqa: E402


def ensure_mint_id(fm: dict) -> dict:
    """Give `fm` a `mint_id` if it does not already carry a valid one.

    **goal:s14.** Until this existed, `bin/backfill-mint-ids.py` was the only
    thing in the system that assigned a mint id, so every node a generator
    created arrived without one and was skipped — loudly, but skipped — by
    `grid.py commit --all` until someone remembered to run the backfill. A
    forgotten backfill silently cost a node its version history, which is the
    one thing goal:g7 exists to make impossible. "Run the backfill after any
    generator" was an unscripted manual step; this is the script.

    Minting here rather than in each caller is deliberate: this is the one
    serializer `level3.py`, `decompose-engine.py`, `backfill-mint-ids.py` and
    this file all write through, so one hook covers every generator at once.

    **Never overwrites.** A mint id is assigned once and never changes
    (goal:g2.5), so an existing valid value is left exactly as found. An
    *invalid* value is also left alone and reported — rewriting it would
    silently fork the node's grid history, and a human needs to see it.
    """
    existing = fm.get("mint_id")
    if isinstance(existing, str) and existing.strip():
        if not is_valid_mint_id(existing.strip()):
            print(f"WARN: mint_id {existing!r} is not 32 lowercase hex chars; "
                  "leaving it as found (rewriting it would fork the node's "
                  "grid history)", file=sys.stderr)
        return fm
    return {**fm, "mint_id": mint_permanent_id()}


#: **goal:g11.1.** Re-exported from `locations`, which is where it always
#: should have pointed. The local copy left behind by the half-migration knew
#: only the two prefixed marker names, so `config_path(<repo>/.agi)` returned
#: None for a graph directory whose config is `config.json` — and both callers
#: below read that None as "no config" and fell back to engine defaults. The
#: root was right and the config lookup was silently wrong, which is why this
#: file counted as half-migrated rather than done.
config_path = locations.config_path

# goal:g11 — not `PROJECT_ROOT / "GOALS.md"`. Under the `.agi/` layout the graph
# root is `<repo>/.agi`, and rendering the goal document there would hide the
# one file a human is most likely to open first. `goals_path` puts a bare
# `goals_file` name at the repo root instead, and honours an explicit override
# for a project that already ships a GOALS.md of its own.
GOALS_MD = locations.goals_path(PROJECT_ROOT)
NODES_DIR = PROJECT_ROOT / "nodes"

# `## G1 — Title — status: active`             long-term goal
# `### G1.2 — Title — status: active`          sub-goal, nested under G1
# `## S3 — Title — status: active`             standalone short-term goal
#
# Sub-goals and short-term goals exist so that work small enough to be a TODO
# item still lands in the graph instead of in a second document. A sub-goal
# parent-points at its long-term goal exactly the way a seed idea does; a
# short-term goal is its own root and needs no parent to be legitimate.
GOAL_RE = re.compile(r"^##\s*([GS]\d+)\b(.*)$")
SUBGOAL_RE = re.compile(r"^###\s*(G\d+\.\d+)\b(.*)$")
# A top-level perpetual goal renders under a `## Perpetual` section as `### <gid>`
# (no dot — a dotted `### G1.2` is a subgoal and matches SUBGOAL_RE).
PERPETUAL_RE = re.compile(r"^###\s*([GS]\d+)\b(.*)$")
HEADING_RE = re.compile(r"^##\s")
STATUS_RE = re.compile(r"[—-]?\s*status\s*:\s*(.+?)\s*$", re.IGNORECASE)
GOAL_ID_RE = re.compile(r"^goal:")

_GID_RE = re.compile(r"^([A-Za-z]+)(\d+(?:\.\d+)*)$")


def natural_sort_key(gid: str) -> tuple:
    """Numeric-aware sort key for a goal id like ``G2.10`` or ``S11``.

    Replaces the old `order:` frontmatter field (goal:s12's follow-on): a
    dense, contiguous `order: 0..90` across 91 goals meant every insertion
    renumbered every later goal — 21 nodes churned twice in one session for
    no semantic change. `goal_id` is already the permanent identity
    (goal:g2.5), so it needs no separate position to be sortable; it only
    needs a key that gets the numbers right.

    Splits the letter prefix from the dot-separated numeric suffix and
    compares the numeric parts component-wise as integers, so `G2.10` sorts
    after `G2.9` (a plain string/lexicographic sort would put it between
    `G2.1` and `G2.2`) and `S11` sorts after `S2`. `G` sorts before `S`
    because the prefix compares first and `"G" < "S"` lexically — which also
    preserves GOALS.md's existing G-goals-then-S-goals grouping.

    A `gid` that does not match the `<letters><digits[.digits...]>` shape
    (should not occur in practice; every goal id is minted by this same
    script) falls back to a plain string key rather than raising, so a
    malformed id degrades to alphabetical placement instead of aborting the
    whole render.
    """
    m = _GID_RE.match(gid)
    if not m:
        return (gid, ())
    prefix, nums = m.group(1), m.group(2)
    return (prefix, tuple(int(p) for p in nums.split(".")))


def _id_rest(node_id: str) -> str:
    """Everything after the first ``:`` in an id, or the whole id if there is none.

    Used to spot G7.1's common real cause: a typo'd type prefix (a node writes
    ``hypothesis:chain-engine-r1`` when the real id is ``hyp:chain-engine-r1``).
    Two ids with the same "rest" but different prefixes are almost certainly
    the same node referenced under the wrong prefix, not two unrelated ids.
    """
    return node_id.split(":", 1)[1] if ":" in node_id else node_id


def _set_project_root(path: Path) -> None:
    """Re-point the module-level path globals (used by --project in tests)."""
    global PROJECT_ROOT, GOALS_MD, NODES_DIR
    PROJECT_ROOT = Path(path).resolve()
    GOALS_MD = locations.goals_path(PROJECT_ROOT)
    NODES_DIR = PROJECT_ROOT / "nodes"


# --- helpers copied from snapshot-build-site.py (kept in sync deliberately;
#     snapshot-build-site.py is load-bearing and is not refactored here) ------


def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9\- ]", "", s.lower())
    s = re.sub(r"\s+", "-", s.strip())
    parts = s.split("-")[:6]
    return "-".join(p for p in parts if p) or "untitled"


def _add_graph_core_to_path() -> None:
    """Put graph_core on sys.path, plugin src last so a project can override.

    Mirrors driver.sh's convention and zoom.py's `_add_graph_core_to_path`.
    Without this the sqlite branch below raised ModuleNotFoundError *mid-run*,
    after some goal files had already been written — a project with
    `persistence.type: sqlite` could not snapshot its goals at all.
    """
    plugin_src = PLUGIN_ROOT / "src"
    if plugin_src.is_dir() and str(plugin_src) not in sys.path:
        sys.path.insert(0, str(plugin_src))
    proj_src = PROJECT_ROOT / "src"
    if (proj_src / "graph_core").is_dir() and str(proj_src) not in sys.path:
        sys.path.insert(0, str(proj_src))


def _upsert_node_to_db(node_id: str, fm: dict, body: str, origin: str) -> None:
    """Upsert a node into SQLite if persistence.type=sqlite."""
    if not hasattr(_upsert_node_to_db, "_backend"):
        cfg_path = config_path(PROJECT_ROOT)
        _upsert_node_to_db._backend = None
        if cfg_path is not None:
            cfg = json.loads(cfg_path.read_text())
            if cfg.get("persistence", {}).get("type") == "sqlite":
                db_path = PROJECT_ROOT / cfg["persistence"]["path"]
                _add_graph_core_to_path()
                # The DB is a mirror of the files just written, so an
                # unavailable backend must degrade to a warning. Raising here
                # aborts mid-corpus and leaves a partially-snapshotted graph —
                # a project shadowing graph_core with a stale copy that predates
                # sqlite_backend hit exactly that.
                try:
                    from graph_core.persistence.sqlite_backend import SQLiteBackend
                    _upsert_node_to_db._backend = SQLiteBackend(db_path)
                except Exception as exc:
                    print(f"WARN: sqlite persistence unavailable ({exc}); "
                          f"nodes written to files only", file=sys.stderr)
    if _upsert_node_to_db._backend is None:
        return
    from graph_core.persistence.frontmatter import NodeFile
    fm = dict(fm)
    fm["id"] = node_id
    fm["origin"] = origin
    nf = NodeFile(frontmatter={**fm, "body": body}, body=body, suffix=".json")
    _upsert_node_to_db._backend.save(node_id, nf)


# --- the authored region of a body (goal:g2.10, goal:g2.11) ---------------
# A generator owns the *derived* half of a node body and rewrites it on every
# run.  Everything a model authored used to be destroyed by that rewrite: 8,034
# `why`/`perf`/`security` fields across 190 build nodes, 0 ever filled, because
# filling one lasted until the next scan.  `THOUGHT` is the authored region --
# marked, so preserving it is mechanical rather than a guess about which prose
# was hand-written.
#
# Deliberately a body block and not a frontmatter field: `write_frontmatter`
# flattens newlines (`str(v).replace("\n", " ")` below), so prose in
# frontmatter is silently destroyed.  Deliberately marked rather than
# position-based, because "any prose after the contract block" is not
# something a regenerating writer can identify without guessing.
#
# Per-version storage is free and needs no new plumbing: the grid already
# snapshots `node.md` once per version, so every grid commit carries the
# thought current at that time and `grid.py diff` reads as a reasoning
# changelog.
THOUGHT_BEGIN = ("<!-- THOUGHT:BEGIN — authored, not derived; carried across "
                 "regenerating scans. The reasoning behind THIS version. -->")
THOUGHT_END = "<!-- THOUGHT:END -->"
_THOUGHT_RE = re.compile(
    r"<!--\s*THOUGHT:BEGIN.*?<!--\s*THOUGHT:END\s*-->", re.DOTALL)


def extract_thought(body: str | None) -> str | None:
    """The whole THOUGHT block including its markers, or None if absent.

    Absent is the normal state and means empty -- adding the field cost zero
    node churn across all 786 existing nodes precisely because absence is
    legal rather than an empty block being mandatory.
    """
    if not body:
        return None
    m = _THOUGHT_RE.search(body)
    return m.group(0) if m else None


def strip_thought(body: str) -> str:
    """`body` with its THOUGHT region removed, for readers (goal:g2.11).

    Thought is provenance to zoom into, not weight every reader carries. A
    thought written once would otherwise ride in every rendered document and
    every injected context for the rest of the project's life -- the "heavier
    pack" the design ethic exists to refuse.

    Renderers strip; the node keeps it. That asymmetry is the whole point, and
    it is also the one hazard: anything parsing a *rendered* document back into
    nodes would silently drop every thought. `GOALS.md` is generated and that
    direction is not run (goal:g6.9 reversed the arrow), but `parse_goals`
    still exists, so this is stated rather than assumed.
    """
    if not body:
        return body
    return re.sub(r"\n*" + _THOUGHT_RE.pattern, "", body, flags=re.DOTALL).rstrip()


def splice_thought(new_body: str, old_body: str | None) -> str:
    """Carry the previous body's THOUGHT block into a regenerated body.

    A thought authored *in this pass* wins over the stored one: a generator
    that clobbered a fresh thought with a stale one would be the same defect
    in the other direction.
    """
    if extract_thought(new_body) is not None:
        return new_body
    carried = extract_thought(old_body)
    if carried is None:
        return new_body
    return f"{new_body.rstrip()}\n\n{carried}"


def write_frontmatter(path: Path, fm: dict, body: str, origin: str = "",
                      preserve: dict | None = None,
                      preserve_body: str | None = None) -> None:
    """Write a node file.  `preserve` carries forward fields we do not own.

    Kept in sync with snapshot-build-site.py, where rebuilding frontmatter from
    scratch silently severed `next_edges` on every re-snapshot.  Snapshot-owned
    keys win; anything a later writer added survives.

    `preserve_body` is the same contract one level down, for the body: pass the
    node's previous body and its authored THOUGHT region survives the rewrite
    (goal:g2.10).  Frontmatter has had this since `next_edges` was being
    severed; the body did not, which is why no `why:` field in the corpus has
    ever been filled in.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    if preserve:
        merged = {k: v for k, v in preserve.items() if k not in fm}
        if merged:
            fm = {**merged, **fm}
    if preserve_body is not None:
        body = splice_thought(body, preserve_body)
    if origin:
        fm = dict(fm)  # copy so we don't mutate caller's dict
        fm["origin"] = origin
    fm = ensure_mint_id(fm)
    lines = ["---"]
    for k in sorted(fm.keys()):
        v = fm[k]
        if isinstance(v, list):
            if not v:
                lines.append(f"{k}: []")
            else:
                lines.append(f"{k}:")
                for item in v:
                    # None round-trips as a null list entry (`-` with nothing
                    # after it), not the literal 3-char string "None" --
                    # `str(None)` below would silently turn a null entry into
                    # a real value on the next parse (found live, 2026-08-25,
                    # backfilling mint_id across the corpus: 7 nodes carrying
                    # a malformed empty `parents:` item -- itself already a
                    # known, tolerated shape, see collect_parent_refs' empty-
                    # entry handling above -- came back as `parents: [None]`
                    # after one write_frontmatter round trip).
                    lines.append("  -" if item is None else f"  - {item}")
        elif isinstance(v, dict):
            # A nested mapping has to be serialized AS YAML. The generic
            # branch below does `str(v)`, which renders a dict as its Python
            # repr -- `{'enabled': True}`, with Python's capitalized booleans
            # and single quotes -- and stores it as a *string scalar*. That
            # is silent data loss in the one function that writes every node:
            # the value survives a round trip looking plausible and parses
            # back as text, so the field is no longer a mapping and every
            # reader that indexes into it fails somewhere else.
            #
            # Latent until 2026-09-01 only because the nodes carrying nested
            # fields are `.geometry/*` (`cadences:` in crons.md, `locations:`
            # in secrets.md) and no writer had reached them -- `crons.py`
            # reads that mapping to build the real crontab. Found by making
            # post_wire delegate here and round-tripping the corpus first.
            block = yaml.safe_dump(
                {k: v}, default_flow_style=False, sort_keys=False,
                allow_unicode=True, width=10_000,
            ).rstrip("\n")
            lines.extend(block.split("\n"))
        elif isinstance(v, bool):
            lines.append(f"{k}: {str(v).lower()}")
        elif v is None:
            # Same round-trip hazard as above, one level up: `contrasts:`
            # (a real YAML null, e.g. a verdict field nothing ever filled
            # in) must stay null, not become the 4-char string "None".
            lines.append(f"{k}:")
        else:
            sval = str(v).replace("\n", " ").strip()
            if any(c in sval for c in ":#'\""):
                # Escape into a YAML double-quoted scalar rather than
                # substituting the character. The old line did
                # `sval.replace('"', "'")`, which is silent data loss in the
                # one function that touches every node on every run -- S13's
                # exact finding, one line further down the same function.
                # Caught by goal:g6.9's round-trip check: `## S13 - ... the
                # string "None" ...` came back out of its node as `'None'`.
                esc = sval.replace("\\", "\\\\").replace('"', '\\"')
                sval = f'"{esc}"'
            lines.append(f"{k}: {sval}")
    lines.append("---")
    lines.append("")
    lines.append(body.strip())
    lines.append("")
    text = "\n".join(lines)
    path.write_text(text, encoding="utf-8")
    log_write(PROJECT_ROOT, "write_frontmatter",
              fm.get("id", "<no-id>"), path,
              text=text, extra={"origin": origin})


def load_existing_nodes() -> dict:
    """Load all existing nodes. Returns dict keyed by node id.
    Each value: {path: Path, origin: str, fm: dict, body: str}

    `body` was added for goal:g6.9 — rendering `GOALS.md` back out of the nodes
    needs the prose, not just the frontmatter. `split("---", 2)` caps at three
    parts, so a body containing its own `---` (the preamble has two) stays
    intact in the third.
    """
    nodes = {}
    if not NODES_DIR.exists():
        return nodes
    for md_path in sorted(NODES_DIR.rglob("*.md")):
        try:
            text = md_path.read_text(encoding="utf-8")
            if text.strip().startswith("---"):
                parts = text.split("---", 2)
                if len(parts) >= 3:
                    fm = yaml.safe_load(parts[1]) or {}
                    node_id = fm.get("id", "")
                    if node_id:
                        nodes[node_id] = {
                            "path": md_path,
                            "origin": fm.get("origin", ""),
                            "fm": fm,
                            "body": parts[2],
                        }
        except Exception:
            pass
    return nodes


# --- GOALS.md parsing ------------------------------------------------------


def _strip_separators(s: str) -> str:
    return s.strip().strip("—-").strip()


def body_cap() -> int:
    """The per-goal body cap in characters; `0` means no cap at all.

    **goal:s12, question 2 — "what the cap should be is a real trade-off; the
    owner picks".** So the engine stops picking. `BODY_CAP` is the default and
    `goal_body_cap` in the project's own config overrides it, which is the
    surface a project is supposed to change behaviour through (`SKILL.md`,
    "The config file is the project's whole customization surface") rather
    than by editing an engine constant nobody can see from inside the project.
    """
    cfg_path = config_path(PROJECT_ROOT)
    if cfg_path is None:
        return BODY_CAP
    try:
        value = json.loads(cfg_path.read_text()).get("goal_body_cap", BODY_CAP)
    except Exception:
        return BODY_CAP
    return value if isinstance(value, int) and value >= 0 else BODY_CAP


def cap_body(body: str, gid: str) -> str:
    """Truncate `body` to the configured cap **visibly**, or return it whole.

    **goal:s12, question 1 — "silent truncation is always wrong".** The old
    `[:BODY_CAP]` cut mid-character-stream: `goal:g2.5`'s node body ended
    `| Assigned | once, at node creation | derived,` — a markdown table severed
    mid-cell, which is not merely missing content but *syntactically malformed*
    content, so a naive reader mis-parses what remains rather than noticing it
    is short. Three things change and all three are required:

      1. **Cut at a block boundary.** Blank-line-separated blocks, so a table,
         a list or a fenced block is either wholly present or wholly absent.
         A single block larger than the cap has no boundary to cut at, so it
         is kept whole and over-cap rather than severed — an honest overrun
         beats a malformed fragment.
      2. **Say so in the body.** An explicit marker naming how much was
         dropped and where the complete text lives. A reader of the *graph*
         must be able to tell a complete goal from a clipped one; that was
         precisely what was impossible before.
      3. **Warn on stderr, naming the goal.** So the run reports it, rather
         than the loss being discoverable only by reading a node and noticing
         a sentence stops.
    """
    cap = body_cap()
    if cap <= 0 or len(body) <= cap:
        return body

    blocks = body.split("\n\n")
    kept: list[str] = []
    used = 0
    for block in blocks:
        cost = len(block) + (2 if kept else 0)
        if used + cost > cap:
            break
        kept.append(block)
        used += cost

    if not kept:
        # The first block alone exceeds the cap. Keeping it whole is
        # deliberate: there is no boundary inside it, and cutting anyway is
        # the exact defect this function exists to remove.
        print(f"WARN: goal {gid} — first block is {len(blocks[0])} chars, over "
              f"the {cap}-char cap and unsplittable; kept whole rather than "
              "severed mid-block", file=sys.stderr)
        return body

    dropped = len(body) - used
    print(f"WARN: goal {gid} — body is {len(body)} chars, over the {cap}-char "
          f"cap; {dropped} chars dropped at a block boundary. GOALS.md is the "
          "only complete copy (goal:s12).", file=sys.stderr)
    marker = (f"> **[truncated: {dropped} of {len(body)} characters dropped at "
              f"a block boundary to fit the {cap}-character cap. `GOALS.md` "
              f"section `{gid}` is the complete text; raise `goal_body_cap` in "
              "the project config to keep more.]**")
    return "\n\n".join(kept) + "\n\n" + marker


def parse_goals(text: str) -> list[dict]:
    """Parse GOALS.md text into an ordered list of goal dicts.

    Text before the first `## G` heading (the preamble) is returned separately
    by `parse_preamble`, not here.

    Each goal carries `heading_level` (2 for `## G7` / `## S4`, 3 for
    `### G7.2`), stored so the document can be rendered back from the nodes**
    (goal:g6.9) without guessing the heading depth from the id shape.

    Document position is **not** stored (the retired `order:` field —
    natural-sort-by-`goal_id` follow-on to goal:s12). `render_goals` recovers
    ordering from `goal_id` itself via `natural_sort_key`, which reshuffles
    the old, deliberately-unsorted S-block (S11..S17 used to sit before
    S1..S10 because ids are never renumbered and the file grew that way) into
    natural order exactly once — a documented, intentional correction, not a
    regression.
    """
    goals: list[dict] = []
    current: dict | None = None

    def _start(gid: str, rest: str, level: int) -> dict:
        status = "active"
        m_status = STATUS_RE.search(rest)
        if m_status:
            status = m_status.group(1).strip()
            rest = rest[: m_status.start()]
        title = _strip_separators(rest)
        return {
            "gid": gid,
            "title": title or gid,
            "status": status or "active",
            "heading_level": level,
            # `perpetual` is set below for a `### <gid>` heading only; a normal
            # G/S root and a dotted subgoal leave this empty and the writer
            # derives the kind from the id shape as before.
            "goal_kind": "",
            # A sub-goal carries its long-term goal as a parent; a top-level
            # goal (G or S) is a root and carries none.
            "parent_gid": gid.split(".")[0] if "." in gid else None,
            "body": [],
        }

    for line in text.splitlines():
        m = GOAL_RE.match(line)
        if m:
            if current is not None:
                goals.append(current)
            current = _start(m.group(1), m.group(2), 2)
            continue
        m_sub = SUBGOAL_RE.match(line)
        if m_sub:
            if current is not None:
                goals.append(current)
            current = _start(m_sub.group(1), m_sub.group(2), 3)
            continue
        m_peerp = PERPETUAL_RE.match(line)
        if m_peerp and "." not in m_peerp.group(1):
            # A non-dotted `### <gid>` lives under the `## Perpetual` section.
            # Perpetual roots are mid-document, so this is unambiguous against
            # a dotted subgoal (which SUBGOAL_RE already claimed). Forced to
            # heading_level 2 so round trips never drift the node's depth.
            if current is not None:
                goals.append(current)
            current = _start(m_peerp.group(1), m_peerp.group(2), 2)
            current["goal_kind"] = "perpetual"
            continue
        if HEADING_RE.match(line):
            # A non-goal `## ` heading terminates the current goal body.
            if current is not None:
                goals.append(current)
                current = None
            continue
        if current is not None:
            current["body"].append(line)
    if current is not None:
        goals.append(current)
    for g in goals:
        g["body"] = cap_body("\n".join(g["body"]).strip(), g["gid"])
    return goals


GENERATED_BANNER = (
    "<!-- GENERATED — do not edit this file.\n"
    "     Source of truth: nodes/goal/*.md and nodes/doc/goals-preamble.md.\n"
    "     Edit the node, then `snapshot-goals.py --render` (goal:g6.9).\n"
    "     An edit made here is overwritten on the next render, silently, the\n"
    "     same way an edit to nodes/goal/ used to be before the arrow flipped.\n"
    "     This document is a flat reading convenience; the graph is the\n"
    "     interface, and the hypergraph viewport (G9.4/G10.3) is the good one. -->"
)

#: Rendered at the head of the `## Perpetual` section (hypothesis
#: l3w1-goal-kind-perpetual, L3 wave 1). Perpetual goals are broadly worded,
#: one director each, meant to outlive seasons; they nevertheless may be
#: `retired` on the node — retire stays legal, it is just not a lifecycle
#: column in this section.
PERPETUAL_INTRO = (
    "The following goals are `goal_kind: perpetual` — the long-horizon\n"
    "commitments, broadly worded, one director each. Retire stays legal on the\n"
    "node; they simply carry no per-goal complete/retired lifecycle line here."
)


def strip_banner(text: str) -> str:
    """Remove the generated banner if present, so a rendered document can be
    re-imported by `--from-doc` without the banner accreting a second copy of
    itself on every round trip."""
    if text.startswith("<!-- GENERATED"):
        end = text.find("-->")
        if end != -1:
            return text[end + 3:].lstrip("\n")
    return text


def parse_preamble(text: str) -> str:
    """Everything above the first goal heading, verbatim.

    The parser has always discarded this, which was harmless while the document
    was the source. Once the nodes are the source (goal:g6.9) it is 160 lines of
    design contract that would be destroyed on the first render, so it gets a
    node of its own — `doc:goals-preamble`. `type: doc` and not `type: goal`
    deliberately: it is a document section, not a commitment, and typing it as a
    goal would add a 76th "goal" to every count that reads `type == goal` while
    having no status, no seeds and nothing to fulfil.
    """
    lines = strip_banner(text).splitlines()
    for i, line in enumerate(lines):
        if GOAL_RE.match(line) or SUBGOAL_RE.match(line):
            return "\n".join(lines[:i]).rstrip("\n")
    return "\n".join(lines).rstrip("\n")


def render_goals(preamble: str, goals: list[dict]) -> str:
    """Render `GOALS.md` from the nodes — goal:g6.9's whole point.

    The inverse of `parse_goals`/`parse_preamble`, and required to be exactly
    that: `render_goals(parse_preamble(t), parse_goals(t)) == t` is the
    migration's own falsifier, run by `--render --check`. A renderer that is
    merely close produces a diff on every run and nobody reads it after the
    third time.

    Heading depth comes from the node's own `heading_level`. Ordering comes
    from a natural sort over `goal_id` (`natural_sort_key`, retiring the old
    `order:` field) — G-goals before S-goals, numeric-aware within each
    (`G2.10` after `G2.9`, `S11` after `S2`).
    """
    out = [GENERATED_BANNER, "", preamble, ""]
    # Perpetual goals get their own section at the end of the document: they
    # are the long-horizon commitments (one director each, broadly worded),
    # and grouping them apart keeps the G/S lifecycle view short. They carry no
    # `— status:` line (no complete/retired lifecycle column); retire is still
    # legal on the node and is simply not rendered as a per-goal lifecycle here.
    perpetual = [g for g in goals if g.get("goal_kind") == "perpetual"]
    regular = [g for g in goals if g.get("goal_kind") != "perpetual"]
    for g in sorted(regular, key=lambda x: natural_sort_key(x["gid"])):
        hashes = "#" * int(g["heading_level"])
        out.append(f"{hashes} {g['gid']} — {g['title']} — status: {g['status']}")
        out.append("")
        # goal:g2.11 — the authored THOUGHT region stays on the node and never
        # reaches the rendered document. `--check` is unaffected: it compares
        # this output against a GOALS.md that this same function wrote, so both
        # sides are stripped and the round trip stays byte-identical.
        out.append(strip_thought(g["body"]))
        out.append("")
    if perpetual:
        out.append("## Perpetual")
        out.append("")
        out.append(PERPETUAL_INTRO)
        out.append("")
        for g in sorted(perpetual, key=lambda x: natural_sort_key(x["gid"])):
            # Lay one level deeper than the node's own heading_level so the
            # goal nests under the `## Perpetual` section heading.
            hashes = "#" * (int(g["heading_level"]) + 1)
            out.append(f"{hashes} {g['gid']} — {g['title']}")
            out.append("")
            out.append(strip_thought(g["body"]))
            out.append("")
    # One trailing newline, no trailing blank line — matches the hand-written
    # document byte for byte, which is what `--check` compares.
    return "\n".join(out).rstrip("\n") + "\n"


def collect_parent_refs(existing: dict) -> dict:
    """Map any referenced id -> sorted list of node ids whose `parents` reference it.

    G7.1: this used to filter down to `goal:`-prefixed refs only, because the
    only consumer was goal-seed population and the goal integrity check. Both
    still work off this same dict — seed lookups key on `goal:` ids, which are
    still in here — but now every prefix is collected so the integrity check
    below can validate ALL parent references, not just goals.
    """
    refs: dict[str, list[str]] = {}
    empty_parent_entries: dict[str, int] = {}
    for node_id, node in existing.items():
        parents = node["fm"].get("parents") or []
        if isinstance(parents, str):
            parents = [parents]
        for p in parents:
            # An empty YAML list item (`parents:\n  - `) parses to None. That is
            # malformed frontmatter, not a reference to a node called "None" —
            # reporting it as a dangling ref sent readers looking for a missing
            # node that never existed. Skipped here and counted separately below.
            if p is None or not str(p).strip():
                empty_parent_entries.setdefault(node_id, 0)
                empty_parent_entries[node_id] += 1
                continue
            refs.setdefault(str(p).strip(), []).append(node_id)
    for k in refs:
        refs[k] = sorted(set(refs[k]))
    for node_id, n in sorted(empty_parent_entries.items()):
        print(f"INTEGRITY: {node_id} has {n} empty entry/entries under `parents:` "
              f"(malformed frontmatter, not a missing node)", file=sys.stderr)
    return refs


def report_integrity(existing: dict, refs: dict,
                     known_ids: set[str]) -> tuple[int, int, int, int]:
    """G7.1's referential-integrity sweep: every parent reference must resolve.

    Extracted from the import path for goal:g6.9 so it runs in **both**
    directions. It has run on every iteration since G7.1 and is what keeps
    `INTEGRITY` at 0; making the render the default without carrying it across
    would have silently retired a live check as a side effect of an unrelated
    change, which is exactly the class of regression this project keeps paying
    for.

    Returns `(unresolved, unresolved_goals, prefix_mismatches,
    genuinely_missing)`. Reports; never deletes — a reference that does not
    resolve is a reporting event, never a load-time deletion (goal:g7.4).
    """
    rest_index: dict[str, list[str]] = {}
    for kid in known_ids:
        rest_index.setdefault(_id_rest(kid), []).append(kid)

    unresolved = unresolved_goals = prefix_mismatches = genuinely_missing = 0
    for ref in sorted(refs):
        if ref in known_ids:
            continue
        for node_id in refs[ref]:
            unresolved += 1
            path = existing[node_id]["path"]
            if GOAL_ID_RE.match(ref):
                # Preserve the original message verbatim for `goal:` refs.
                unresolved_goals += 1
                print(f"INTEGRITY: {path} references unknown goal '{ref}'",
                      file=sys.stderr)
                continue
            candidates = sorted(c for c in rest_index.get(_id_rest(ref), []) if c != ref)
            if candidates:
                prefix_mismatches += 1
                print(f"INTEGRITY: {path} references unknown parent '{ref}' "
                      f"(possible prefix typo — did you mean '{candidates[0]}'?)",
                      file=sys.stderr)
            else:
                genuinely_missing += 1
                print(f"INTEGRITY: {path} references unknown parent '{ref}'",
                      file=sys.stderr)
    return unresolved, unresolved_goals, prefix_mismatches, genuinely_missing


PREAMBLE_ID = "doc:goals-preamble"
PREAMBLE_PATH = ("doc", "goals-preamble.md")


def write_preamble_node(preamble: str, existing: dict) -> None:
    """Persist `GOALS.md`'s preamble as `doc:goals-preamble` (goal:g6.9).

    Not a goal node: it has no status, no seeds and nothing to fulfil, and
    typing it `goal` would add a phantom to every count that reads
    `type == goal`. It is a document section, so `type: doc`.
    """
    path = NODES_DIR.joinpath(*PREAMBLE_PATH)
    fm = {
        "id": PREAMBLE_ID,
        "type": "doc",
        "title": "GOALS.md preamble — the goal contract's own framing",
        "parents": [],
        "tags": ["goals-doc", "preamble"],
        "confidence": 1.0,
    }
    write_frontmatter(path, fm, preamble, origin=ORIGIN,
                      preserve=existing.get(PREAMBLE_ID, {}).get("fm"))


def load_goal_nodes(existing: dict) -> tuple[str, list[dict]]:
    """`(preamble, goals)` read back out of the nodes — the direction
    goal:g6.9 makes authoritative.

    Only nodes stamped `origin: goals-doc` participate, so a hand-written node
    that happens to be `type: goal` cannot inject a section into the rendered
    document without declaring itself part of it.

    A goal node missing `heading_level` is a hard error naming the file, never
    a guess: guessing the heading depth is precisely how a renderer silently
    reshuffles a document whose ids are permanent. `order` is no longer part
    of this check — retired in favour of a natural sort over `goal_id`
    (`natural_sort_key`), so a node need not carry it at all.
    """
    preamble = ""
    goals: list[dict] = []
    for node_id, node in sorted(existing.items()):
        fm = node["fm"]
        if node.get("origin") != ORIGIN:
            continue
        if node_id == PREAMBLE_ID:
            preamble = (node.get("body") or "").strip("\n")
            continue
        if fm.get("type") != "goal":
            continue
        gid = fm.get("goal_id")
        if not gid:
            sys.exit(f"ERR: {node['path']} is origin={ORIGIN} but has no goal_id")
        if fm.get("heading_level") is None:
            sys.exit(f"ERR: {node['path']} has no heading_level; run "
                     "`snapshot-goals.py --from-doc` once to backfill it "
                     "before rendering (goal:g6.9)")
        title = str(fm.get("title") or gid)
        # Node titles are stored as "G7: Title"; the document heading is
        # "G7 — Title". Strip the stored prefix rather than re-deriving it.
        if title.startswith(f"{gid}:"):
            title = title[len(gid) + 1:].strip()
        goals.append({
            "gid": gid,
            "title": title,
            "status": fm.get("status", "active"),
            "goal_kind": str(fm.get("goal_kind") or "").strip(),
            "heading_level": int(fm["heading_level"]),
            "body": (node.get("body") or "").strip(),
        })
    return preamble, goals


#: Goal statuses that mean "still being pursued". A root carrying one of these
#: below it has not finished, whatever its own text says.
LIVE_GOAL_STATUSES = ("active", "horizon")


def warn_premature_complete(existing: dict) -> list[tuple]:
    """goal:s26 — an overarching goal is not `complete` while its subgoals live.

    Returns the offending `(root_gid, child_gid, child_status)` triples and
    prints one warning per pair. **A warning, never a failure.** A hard error
    would make a legitimate intermediate state unrepresentable — retiring a
    tree bottom-up, one commit per goal — and `goal:g5`'s own invariant says a
    project must stay legitimate at every depth.

    Load-bearing rather than cosmetic since 2026-09-02: `complete` now SCORES
    (`metrics.SCORING_GOAL_STATUSES`), so a premature `complete` on a root
    moves `outcome_coverage` for a bookkeeping reason. That is the defect
    `goal:g5`'s revision removed, re-entering by another door.

    Reads `parents:` because that is where a subgoal declares its root. It
    deliberately produces **no count any metric consults** — a number derived
    from this edge is a fresh gaming surface, which `goal:g3` and `goal:g4.5`
    both name.
    """
    status_of, kind_of, gid_of = {}, {}, {}
    for nid, fm in existing.items():
        if str(fm.get("type") or "") != "goal":
            continue
        st = fm.get("status")
        status_of[nid] = st.strip() if isinstance(st, str) and st.strip() else "active"
        kind_of[nid] = str(fm.get("goal_kind") or "")
        gid_of[nid] = str(fm.get("goal_id") or nid)

    offenders = []
    for nid, fm in existing.items():
        if nid not in status_of:
            continue
        raw = fm.get("parents")
        parents = [x.strip() for x in raw if isinstance(x, str) and x.strip()] \
            if isinstance(raw, (list, tuple)) else []
        if status_of[nid] not in LIVE_GOAL_STATUSES:
            continue
        for par in parents:
            if status_of.get(par) == "complete":
                offenders.append((gid_of[par], gid_of[nid], status_of[nid]))

    for root, child, st in sorted(offenders):
        print(f"WARN: goal {root} is `complete` but subgoal {child} is "
              f"`{st}` — an overarching goal is not complete while its "
              f"subgoals are live (goal:s26)", file=sys.stderr)
    return offenders



def _source_digest(existing: dict) -> dict:
    """sha256 of every `origin=goals-doc` node file — the exact sources
    `load_goal_nodes` reads to build a render (hypothesis
    l4-a-check-that-cries-wolf-gets-waved-through).

    A content digest rather than mtime deliberately: mtime is coarse on some
    filesystems and two writes inside one block can land on the same mtime
    (especially a copy-back-and-forth). A hash of the bytes the renderer would
    actually read cannot miss a change that produces different output, and it
    costs nothing extra because these are the same small files the render
    already reads. An unreadable file digests to `""` so an IO error reads as
    a difference rather than a silent pass.

    The key is the resolved path so two loads of the same file cannot collide.
    A source *added or removed* between the two snapshots shows up as a key
    set difference, which is exactly a source moving under the check.
    """
    out: dict[str, str] = {}
    for node_id, node in existing.items():
        if node.get("origin") != ORIGIN:
            continue
        p = node["path"]
        try:
            out[str(p.resolve())] = hashlib.sha256(
                p.read_bytes()).hexdigest()
        except OSError:
            out[str(p.resolve())] = ""
    return out


def _compare_rendered(rendered: str, n_goals: int) -> int:
    """The one comparison in `--check`: rendered-from-nodes vs GOALS.md on disk.

    Extracted from `cmd_render` so the retry seam in `_check_with_race_guard`
    can re-run exactly this with fresh sources. The messages are byte-for-byte
    what `--check` printed before the race guard existed, so a genuine
    divergence reads exactly as it always has — the only observable change is
    that a benign concurrent write stops looking like a defect.
    """
    current = GOALS_MD.read_text(encoding="utf-8") if GOALS_MD.exists() else ""
    if rendered == current:
        print(f"render --check: {n_goals} goal(s) round-trip byte-identical")
        return 0
    import difflib
    diff = list(difflib.unified_diff(
        current.splitlines(), rendered.splitlines(),
        "GOALS.md (on disk)", "GOALS.md (rendered from nodes)", lineterm="", n=2))
    print(f"render --check: MISMATCH, {len(diff)} diff line(s)", file=sys.stderr)
    for line in diff[:60]:
        print(line, file=sys.stderr)
    if len(diff) > 60:
        print(f"... {len(diff) - 60} more", file=sys.stderr)
    return 1


def _check_with_race_guard(existing: dict, rendered: str) -> int:
    """The `--check` comparison, guarded against concurrent source writes.

    hypothesis l4-a-check-that-cries-wolf-gets-waved-through: the prime writes
    goal nodes and re-renders GOALS.md continuously, so a check that reads
    sources, renders, and compares to a GOALS.md the same writer is recomputing
    can report a *race* as a *defect*. The guard snapshots the sources just
    before and just after the comparison; if any changed in the window it
    RETRIES ONCE and says so. Fail-closed is preserved throughout:

      * a no-change pass costs nothing extra — the caller's one render is used,
        the after-digest is only taken when the comparison already failed, and
        a re-render happens only on the retry itself;
      * a genuine divergence with stable sources fails on the FIRST comparison
        and is never masked by this path (the retry only fires on a detected
        change);
      * a divergence that IS racing still fails — the retry re-renders fresh
        and its result is returned as-is, so a real defect cannot be laundered;
      * exactly ONE retry, never a loop, and the retry is printed to stderr so
        nobody reads a silent second attempt as a first success.
    """
    digest_before = _source_digest(existing)
    code = _compare_rendered(rendered, len(_goal_count(existing)))
    if code == 0:
        return 0
    digest_after = _source_digest(existing)
    if digest_after == digest_before:
        return code   # sources stable; a real divergence, fails as today
    changed = sorted(
        k for k in set(digest_before) | set(digest_after)
        if digest_before.get(k) != digest_after.get(k))
    print("render --check: source node(s) changed during comparison (%s) — "
          "retrying ONCE (concurrent write; hypothesis "
          "l4-a-check-that-cries-wolf-gets-waved-through)"
          % (", ".join(changed) or "new/missing"), file=sys.stderr)
    # exactly ONE retry: reload sources fresh and take whatever THIS attempt
    # says. A persistent divergence fails here; a transient race resolves.
    fresh = load_existing_nodes()
    if not _goal_count(fresh):
        return 1
    rendered = render_goals(*load_goal_nodes(fresh))
    return _compare_rendered(rendered, len(_goal_count(fresh)))


def _goal_count(existing: dict) -> list:
    """The goal nodes among `existing`, for the retry's "no goals" guard."""
    return [nid for nid, n in existing.items()
            if n.get("origin") == ORIGIN and n["fm"].get("type") == "goal"]


def cmd_render(check: bool, strict: bool = False,
               strict_goals: bool = False) -> int:
    """Write `GOALS.md` from the nodes, or (with `check`) prove they agree.

    `--check` is the migration's falsifier and stays useful afterwards: it is
    the one test that says the two directions are still inverses. It writes
    nothing and exits 1 on any difference.
    """
    existing = load_existing_nodes()
    unresolved, unresolved_goals, _, _ = report_integrity(
        existing, collect_parent_refs(existing), set(existing.keys()))
    preamble, goals = load_goal_nodes(existing)
    if not goals:
        print(f"no origin={ORIGIN} goal nodes under {NODES_DIR}/goal — "
              "refusing to write an empty GOALS.md", file=sys.stderr)
        return 1
    rendered = render_goals(preamble, goals)
    if check:
        return _check_with_race_guard(existing, rendered)
    GOALS_MD.write_text(rendered, encoding="utf-8")
    print(f"rendered: {len(goals)} goal(s) + preamble -> {GOALS_MD}")
    warn_premature_complete(existing)   # goal:s26
    if unresolved and strict:
        print(f"ERR: {unresolved} unresolved parent reference(s) (--strict)",
              file=sys.stderr)
        return 1
    if unresolved_goals and strict_goals:
        print(f"ERR: {unresolved_goals} unresolved goal reference(s) "
              "(--strict-goals)", file=sys.stderr)
        return 1
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Derive nodes/goal/ from GOALS.md")
    # The help text used to say "unknown goal id" while the check below tested
    # every unresolved parent reference — 81 of them on the live tree against 0
    # unresolved goals. A flag whose documentation is narrower than its
    # behaviour is worse than no flag: it reads as safe to enable and is not.
    ap.add_argument("--strict", action="store_true",
                    help="exit 1 if a node references ANY unknown parent id")
    ap.add_argument("--strict-goals", action="store_true",
                    help="exit 1 only if a node references an unknown goal id "
                         "(goal:g5 — the check driver.sh can actually enable)")
    ap.add_argument("--project", default=None,
                    help="override PROJECT_ROOT (default: env or cwd)")
    ap.add_argument("--render", action="store_true",
                    help="goal:g6.9 — write GOALS.md FROM the nodes. This is "
                         "the authoritative direction; the document is a "
                         "rendered convenience.")
    ap.add_argument("--check", action="store_true",
                    help="with --render, write nothing and exit 1 if the "
                         "rendered document differs from the one on disk")
    ap.add_argument("--from-doc", action="store_true",
                    help="the LEGACY direction: parse GOALS.md into nodes. "
                         "Retained for the migration and for importing a "
                         "hand-written GOALS.md into a fresh project. Prunes "
                         "goal nodes the document does not mention — which is "
                         "why it is no longer the default (goal:g6.9).")
    args = ap.parse_args(argv)
    if args.project:
        _set_project_root(Path(args.project))

    if args.render:
        return cmd_render(args.check, args.strict, args.strict_goals)
    if not args.from_doc:
        print("snapshot-goals.py: nodes are the source of truth for goals "
              "(goal:g6.9). Use --render to write GOALS.md from them, or "
              "--from-doc to run the legacy import.", file=sys.stderr)
        return 2

    if not GOALS_MD.exists():
        # Never prune on a missing/renamed GOALS.md — that would wipe goal nodes.
        print(f"no GOALS.md at {GOALS_MD} — skipping")
        return 0

    doc_text = GOALS_MD.read_text(encoding="utf-8")
    goals = parse_goals(doc_text)
    existing = load_existing_nodes()
    refs = collect_parent_refs(existing)
    # goal:g6.9 — the preamble is 160 lines of design contract that the parser
    # used to discard. Once the nodes are the source it has to live in one.
    write_preamble_node(parse_preamble(doc_text), existing)

    goal_ids = {f"goal:{g['gid'].lower()}" for g in goals}
    written: set[str] = set()
    written_paths: set[Path] = set()

    for g in goals:
        if g["status"] not in KNOWN_STATUSES:
            print(f"WARN: goal {g['gid']} has unrecognized status '{g['status']}'",
                  file=sys.stderr)
        node_id = f"goal:{g['gid'].lower()}"
        title = f"{g['gid']}: {g['title']}"
        parent_gid = g.get("parent_gid")
        kind = g.get("goal_kind")
        if not kind:
            if parent_gid:
                kind = "subgoal"
            elif g["gid"].startswith("S"):
                kind = "short-term"
            else:
                kind = "long-term"
        tags = ["goal"]
        if parent_gid:
            tags += ["subgoal"]
        elif kind == "perpetual":
            tags += ["root", "perpetual"]
        elif g["gid"].startswith("S"):
            tags += ["root", "short-term"]
        else:
            tags += ["root"]
        fm = {
            "id": node_id,
            "type": "goal",
            "goal_id": g["gid"],
            "title": title,
            "status": g["status"],
            "goal_kind": kind,
            # goal:g6.9 — the field a renderer needs to put this section back
            # at the depth it was. Not inferable: heading depth would have to
            # be guessed from the id shape. Document *position* used to be a
            # second such field (`order:`), retired in favour of a natural
            # sort over `goal_id` — see `natural_sort_key`.
            "heading_level": g["heading_level"],
            "seeds": refs.get(node_id, []),
            "tags": tags,
            "confidence": 1.0,
        }
        if parent_gid:
            # Same parent-pointing convention seed ideas use, so a sub-goal
            # renders and traverses under its long-term goal for free.
            #
            # `[goal].md` lets a goal name the build node that produced it
            # (2026-09-05) — a completion report, a survey, a design note. This
            # direction reconstructs `parents:` from the heading hierarchy, and
            # a heading can only ever yield the goal parent, so a rebuild that
            # simply assigned the list would silently drop the other half. Keep
            # whatever non-goal parents the node already carries; the goal
            # parent is still derived, never preserved, because the hierarchy
            # is the authority on THAT one.
            prior = (existing.get(node_id, {}).get("fm") or {}).get("parents")
            kept = [x.strip() for x in prior
                    if isinstance(x, str) and x.strip()
                    and not x.strip().startswith("goal:")] \
                if isinstance(prior, (list, tuple)) else []
            fm["parents"] = [f"goal:{parent_gid.lower()}"] + kept
        slug = f"{g['gid'].lower()}-{slugify(g['title'])}"
        out_path = NODES_DIR / "goal" / f"{slug}.md"
        write_frontmatter(out_path, fm, g["body"], origin=ORIGIN,
                          preserve=existing.get(node_id, {}).get("fm"))
        _upsert_node_to_db(node_id, fm, g["body"], origin=ORIGIN)
        written.add(node_id)
        written_paths.add(out_path.resolve())

    # Referential integrity (G7.1): every parent reference must resolve to a
    # known node id — not just `goal:`-prefixed ones. This used to check goal
    # refs only; the mechanism (warn by default, --strict to fail) is unchanged,
    # only its scope. `goal_ids` is the fresh set this run computed from
    # GOALS.md (a goal's file may not exist on disk yet this run); `existing`
    # is every id already on disk. Together they're the full universe a
    # `parents:` entry may legitimately point at.
    unresolved, unresolved_goals, prefix_mismatches, genuinely_missing = \
        report_integrity(existing, refs, set(existing.keys()) | goal_ids)

    # Prune only nodes stamped with our origin that we did not write this run
    # (covers both removed goals and goals whose title/slug changed).
    # Prune only nodes this script actually owns: `origin: goals-doc` AND
    # `type: goal`. Origin alone was not enough, and the gap cost a real node
    # within an hour of `doc:goals-preamble` existing — the published (older)
    # engine still had the origin-only rule, saw a `doc` node it had not
    # written, and deleted it. It was recovered from the grid, which is the
    # only reason this is a story rather than a loss.
    #
    # The rule that generalises: **a generator may delete only what it can
    # produce.** This one produces goal headings; a `doc` node is not one, so
    # it is not this function's to sweep, whatever origin it carries.
    stale = [
        node["path"]
        for node_id, node in existing.items()
        if node["origin"] == ORIGIN
        and node["fm"].get("type") == "goal"
        and node_id != PREAMBLE_ID
        and node["path"].resolve() not in written_paths
    ]
    for path in sorted(stale):
        path.unlink(missing_ok=True)
        print(f"removed stale: {path}")

    print(f"wrote: {len(goals)} goal nodes")
    print(f"target dir: {NODES_DIR / 'goal'}")
    if unresolved:
        print(f"unresolved parent references: {unresolved} "
              f"({prefix_mismatches} prefix-mismatch, {genuinely_missing} missing)")
    if unresolved and args.strict:
        print(f"ERR: {unresolved} unresolved parent reference(s) (--strict)",
              file=sys.stderr)
        return 1
    # goal:g5 — "fail loudly when a seed node points at a goal id that does not
    # exist." Narrower than --strict on purpose: the loop carries 81 unresolved
    # *parent* references (mostly `hypothesis:`/`hyp:` prefix drift), so
    # enabling --strict in driver.sh would abort every run on day one and be
    # reverted within the hour. A dangling goal reference is the different,
    # rarer failure this goal cares about, and it currently stands at 0 — which
    # is exactly when to start enforcing it, before the first one appears.
    if unresolved_goals and args.strict_goals:
        print(f"ERR: {unresolved_goals} unresolved goal reference(s) "
              "(--strict-goals)", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
