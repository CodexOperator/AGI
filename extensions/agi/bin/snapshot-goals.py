#!/usr/bin/env python3
"""snapshot-goals.py — the shared node-file helpers the goal importer left behind.

GOALS.md is RETIRED (owner 2026-09-29 17:3xZ, goal:g7.16.1.4.1): the render
(`--render` / `--check`), the legacy document import and its prune are
gone. A goal lives only in its node, minted with `write.py create goal` and
read by id. What stays is imported by file path by level3.py,
snapshot-build-site.py, backfill-mint-ids.py, decompose-engine.py and
post_wire.py: `write_frontmatter` (THE serializer), `ensure_mint_id`,
`load_existing_nodes`, `_set_project_root`, the THOUGHT helpers, the
referential-integrity report and the goal:s26 premature-complete warning.
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
PLUGIN_ROOT = Path(__file__).resolve().parent.parent

# goal:g11 — one resolver for every path. `bin/` is already on sys.path for
# every entry point here, so this is a plain sibling import.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import locations  # noqa: E402
import node_writer  # noqa: E402 -- the ONE THOUGHT definition
from node_writer import log_write  # noqa: E402
from spawn_gate import nearest_vision_town, vision_scope  # noqa: E402

#: **goal:g11.1's first casualty, found the hour the layout changed.** This was
#: `... or os.getcwd()`: an env var, else whatever directory you happened to be
#: standing in. Under the old layout that was harmless, because cwd *was* the
#: graph root. Under `.agi/` it is not — the graph root is `<repo>/.agi` and cwd
#: is `<repo>` — so the (since retired) render looked for `<repo>/nodes/goal`,
#: found nothing, and refused.
#:
#: **It refused rather than writing an empty goal document (retired since), the only
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
from graph_core.identity import ensure_mint_id as _ensure_mint_id  # noqa: E402
from frontmatter import split_frontmatter  # noqa: E402


#: goal:s14's hook, moved to graph_core.identity (goal:g7.16.1.1.4): the one
#: serializer every generator writes through still mints here, by import.
ensure_mint_id = _ensure_mint_id


#: **goal:g11.1.** Re-exported from `locations`, which is where it always
#: should have pointed. The local copy left behind by the half-migration knew
#: only the two prefixed marker names, so `config_path(<repo>/.agi)` returned
#: None for a graph directory whose config is `config.json` — and both callers
#: below read that None as "no config" and fell back to engine defaults. The
#: root was right and the config lookup was silently wrong, which is why this
#: file counted as half-migrated rather than done.
config_path = locations.config_path

NODES_DIR = PROJECT_ROOT / "nodes"

GOAL_ID_RE = re.compile(r"^goal:")


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
    global PROJECT_ROOT, NODES_DIR
    PROJECT_ROOT = Path(path).resolve()
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
THOUGHT_BEGIN = node_writer.THOUGHT_BEGIN   # the ONE spelling lives in node_writer
THOUGHT_END = node_writer.THOUGHT_END


def extract_thought(body: str | None) -> str | None:
    """The whole THOUGHT block including its markers, or None if absent.

    Absent is the normal state and means empty -- adding the field cost zero
    node churn across all 786 existing nodes precisely because absence is
    legal rather than an empty block being mandatory.
    """
    if not body:
        return None
    return node_writer.extract_thought(body)


def strip_thought(body: str) -> str:
    """`body` with its THOUGHT region removed, for readers (goal:g2.11).

    Thought is provenance to zoom into, not weight every reader carries. A
    thought written once would otherwise ride in every rendered document and
    every injected context for the rest of the project's life -- the "heavier
    pack" the design ethic exists to refuse.

    Renderers strip; the node keeps it. That asymmetry is the whole point, and
    it is also the one hazard: anything parsing a *rendered* document back into
    nodes would silently drop every thought. The goal document (retired) was generated and that
    direction is not run (goal:g6.9 reversed the arrow), but `parse_goals`
    still exists, so this is stated rather than assumed.
    """
    if not body:
        return body
    return node_writer.strip_thought(body).rstrip()


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

    `body` was added for goal:g6.9 — rendering the goal document (retired) back out of the nodes
    needs the prose, not just the frontmatter. The line-anchored reader keeps a
    body containing its own `---` (the preamble has two) intact past the
    closing marker.
    """
    nodes = {}
    if not NODES_DIR.exists():
        return nodes
    for md_path in sorted(NODES_DIR.rglob("*.md")):
        try:
            text = md_path.read_text(encoding="utf-8")
            if text.strip().startswith("---"):
                parted = split_frontmatter(text)
                if parted is not None:
                    fm = yaml.safe_load(parted[0]) or {}
                    node_id = fm.get("id", "")
                    if node_id:
                        nodes[node_id] = {
                            "path": md_path,
                            "origin": fm.get("origin", ""),
                            "fm": fm,
                            "body": parted[1],
                        }
        except Exception:
            pass
    return nodes


# --- referential integrity ---------------------------------------------------


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


#: Goal statuses that mean "still being pursued". A root carrying one of these
#: below it has not finished, whatever its own text says.
LIVE_GOAL_STATUSES = ("active", "horizon")


def _frontmatter(node: dict) -> dict:
    """The frontmatter of one node, whichever shape the caller holds.

    `load_existing_nodes()` yields wrappers `{path, origin, fm, body}` — the
    live `--render` path — while unit tests and older callers pass a flat fm
    dict. A guard that reads only one shape is inert on the other, and
    goal:s26 was exactly that: green under flat-dict tests, dead on the real
    render. Accept both so neither caller is privileged.
    """
    fm = node.get("fm")
    return fm if isinstance(fm, dict) else node


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
    for nid, node in existing.items():
        fm = _frontmatter(node)
        if str(fm.get("type") or "") != "goal":
            continue
        st = fm.get("status")
        status_of[nid] = st.strip() if isinstance(st, str) and st.strip() else "active"
        kind_of[nid] = str(fm.get("goal_kind") or "")
        gid_of[nid] = str(fm.get("goal_id") or nid)

    offenders = []
    for nid, node in existing.items():
        if nid not in status_of:
            continue
        raw = _frontmatter(node).get("parents")
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


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=(
        "RETIRED as a command (goal:g7.16.1.4.1): GOALS.md, its render and "
        "its import are gone. This module stays as the shared node-file "
        "helpers other generators import."))
    ap.parse_args(argv)
    print("snapshot-goals.py: GOALS.md is retired (goal:g7.16.1.4.1); read a "
          "goal by id: write.py goal:<id> 'read body 1:60'", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main())
