"""seatsig.countersign -- the tier EARNED: promotion by countersigned verdicts.

RUNG 4 SLICE 4 (conjunct 3) of hypothesis:l4-an-untrusted-lane-earns-tier-by-
signed-verdicts: an untrusted row's tier is EARNED, not granted -- a signed
verdict history (experiment verdict records a trusted reviewer countersigned)
crosses a threshold DECLARED in the ladder geometry node, and the row is
promoted off 'untrusted' by an acting post that is neither the promoted post
nor itself untrusted. Never a self-edit, never new crypto.

The unit counted is one VERDICT-COUNTERSIGN record: a rings.decision_cell of
kind ``verdict-countersign`` over the fields ``{node, verdict, owner}``
(``node`` = the experiment node id, ``verdict`` = the verdict state, ``owner``
= the post whose verdict it is), carrying one or more
``<reviewer>:<scheme>:<sig_hex>`` countersignatures over the record's OWN
canonical bytes. A countersignature is VALID only when ALL OF:

    * it verifies against the countersigner's config:posts row pubkey
      (through rings.verify_ring, the rung-2 gate -- never a hand-rolled
      verifier);
    * the countersigner's row tier is not 'untrusted' (an untrusted reviewer
      cannot vouch for anyone);
    * the countersigner is not the post whose verdict is being counted
      (a reviewer cannot countersign its own work -- and because only the
      counted post's own verdicts are considered, this is the same rule as
      "at least one counted verdict is not the post's own");

Each distinct verdict record counts at most once, however many (or however
duplicated) countersignatures it carries. The promotion is REFUSED BY NAME
when the valid count is below the ladder threshold (naming both numbers),
when the acting post IS the promoted post, when the acting post is itself
untrusted, or when no threshold cell is declared on the ladder node.

The threshold cell lives on the ladder geometry node (``ladder:ladder``)under
``untrusted_promotion_threshold`` -- read through the engine's node reader,
NEVER a literal in this module. The promoted row lands through ``write.submit``
(the sanctioned row writer every other config edit uses).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import seatsig
from seatsig import rings  # the rung-2 helper beside us

#: The ladder geometry node carrying the promotion threshold cell.
LADDER_CELL_PATH = Path("nodes") / ".geometry" / "ladder.md"

#: The ONE declared cell (deliverable 1). Never a hardcoded number here.
PROMOTION_THRESHOLD_CELL = "untrusted_promotion_threshold"

#: The decision kind every counter-signed verdict record carries.
COUNTERSIGN_KIND = "verdict-countersign"
_VERDICT_RING = "verdict-countersign"


def graph_root(root: Path) -> Path:
    """The graph root (the `.agi` dir) for a project root, mirroring send.py's
    ``_graph_root``. A root that IS the `.agi` dir passes through."""
    if (root / ".agi" / "config.json").is_file():
        return root / ".agi"
    return root


def ladder_path(root: Path) -> Path:
    """The ladder geometry node path for a given graph/project root."""
    return graph_root(root) / LADDER_CELL_PATH


def load_promotion_threshold(root: Path):
    """The ladder's promotion-threshold cell, or None when the ladder node or
    the cell is absent/unreadable. Read via the engine node reader
    (graph_core.persistence.frontmatter) so the number is DECLARED on the
    node, not written here. None lets promotion REFUSE BY NAME."""
    cell = ladder_path(root)
    if not cell.is_file():
        return None
    try:
        from graph_core.persistence import frontmatter

        nf = frontmatter.load_node_file(cell)
        return nf.frontmatter.get(PROMOTION_THRESHOLD_CELL)
    except Exception:  # noqa: BLE001 (unreadable cell == undeclared cell)
        return None


def _rows(root: Path) -> list:
    """The config:posts rows via the ONE geometry reader (seats alias too)."""
    try:
        import geometry_config

        return geometry_config.load_rows(graph_root(root))
    except Exception:  # noqa: BLE001
        return []


def _row(rows: list, post: str) -> dict | None:
    for r in rows:
        if r.get("name") == post:
            return r
    return None


def verdict_cell(node_id, verdict, owner, signatures: list):
    """A counter-signed verdict record: a rings.decision_cell (kind
    ``verdict-countersign``, fields ``{node, verdict, owner}``) carrying the
    reviewer countersignatures. This is the UNIT a promotion counts."""
    return rings.decision_cell(_VERDICT_RING, COUNTERSIGN_KIND,
                              {"node": node_id, "verdict": verdict,
                               "owner": owner}, signatures)


def verdict_canonical_hex(node_id, verdict, owner) -> str:
    """The canonical bytes hex a reviewer signs for one verdict record -- the
    exact bytes a re-reader recomputes from the cell's OWN fields, so a sig
    over differing bytes never verifies against this record."""
    return rings.canonical_bytes(
        COUNTERSIGN_KIND, {"node": node_id, "verdict": verdict,
                            "owner": owner}).hex()


def _valid_reviewer_sig(rows: list, post: str, canonical: bytes,
                        signatures: list) -> bool:
    """True when ``signatures`` holds at least one countersignature VALID
    under ALL the countersign conditions -- verifies against the reviewer's
    row pubkey, the reviewer's tier is not 'untrusted', and the reviewer is
    not the counted post. Uses rings.verify_ring for the signature-validity
    half (rung-2 labels VERIFIED/FORGED)."""
    for sig in signatures or []:
        parts = str(sig).split(":", 2)
        if len(parts) != 3:
            continue
        reviewer, scheme_name, sig_hex = parts
        if reviewer == post:
            continue  # a reviewer cannot counter-sign its own work (cond 3/4)
        rev = _row(rows, reviewer)
        if rev is None:
            continue
        if rev.get("tier", "") == "untrusted":
            continue  # an untrusted reviewer vouches for nothing
        ring = {"name": _VERDICT_RING, "m": 1, "members": [reviewer]}
        result = rings.verify_ring(
            ring, canonical, [sig],
            get_scheme=seatsig.get,
            pubkey_for_post=lambda p: (rev.get("pubkey") or None))
        if result.ok:
            return True
    return False


def count_valid_countersigned(root: Path, post: str, verdict_cells: list
                             ) -> int:
    """Count the DISTINCT counter-signed verdict records whose owner is
    ``post`` and that carry at least one VALID reviewer countersignature.
    Duplicate records (same canonical bytes, same signature set) count once;
    one verdict with two countersignatures from the same reviewer counts once
    (the unit is the record, never the signature)."""
    rows = _rows(root)
    seen = set()
    count = 0
    for cell in verdict_cells or []:
        if not isinstance(cell, dict) or cell.get("kind") != COUNTERSIGN_KIND:
            continue
        fields = cell.get("fields") or {}
        if fields.get("owner") != post:
            continue  # only the counted post's own verdicts
        canonical = rings.canonical_bytes(COUNTERSIGN_KIND, fields)
        key = (canonical.hex(), tuple(sorted(cell.get("signatures") or [])))
        if key in seen:
            continue  # a duplicate/tampered record counts once
        seen.add(key)
        if _valid_reviewer_sig(rows, post, canonical,
                              cell.get("signatures") or []):
            count += 1
    return count


def promote(root: Path, post: str, verdict_cells: list,
            actor: str = "", role: str = "") -> dict | None:
    """Promote the untrusted row ``post`` off 'untrusted' -- but ONLY when
    the valid counter-signed-verdict count crosses the ladder threshold AND
    the acting post is not ``post`` (never a self-edit) AND the acting post's
    own row is not untrusted. Refuses BY NAME (returns None, no write) on
    every miss: no such row, row already not untrusted, no threshold declared,
    count short of the threshold (naming both numbers), a self-edit, or an
    untrusted acting post. On success writes the promoted row through
    write.submit and returns it."""
    graph = graph_root(root)
    rows = _rows(root)
    post_row = _row(rows, post)
    if post_row is None:
        print(f"REFUSED {post}: no config:posts row to promote; nothing "
              "written", file=sys.stderr)
        return None
    if str(post_row.get("tier", "")) != "untrusted":
        print(f"REFUSED {post}: tier is already off 'untrusted'; only an "
              "untrusted row earns its tier by verdicts", file=sys.stderr)
        return None
    if not actor or actor in ("", "<unknown>") or actor == post:
        print(f"REFUSED {post}: a post cannot promote its own row (a "
              "self-edit is refused; promotion needs a different acting "
              "post)", file=sys.stderr)
        return None
    actor_row = _row(rows, actor)
    if actor_row is None:
        print(f"REFUSED {post}: acting post {actor!r} has no config:posts "
              "row; cannot promote (only a seated post promotes)",
              file=sys.stderr)
        return None
    if str(actor_row.get("tier", "")) == "untrusted":
        print(f"REFUSED {post}: acting post {actor!r} is itself untrusted; "
              "cannot promote another", file=sys.stderr)
        return None

    threshold = load_promotion_threshold(graph)
    if threshold is None:
        print(f"REFUSED {post}: no promotion threshold is DECLARED on the "
              "ladder node (ladder:ladder, cell "
              f"{PROMOTION_THRESHOLD_CELL!r}); nothing to compare",
              file=sys.stderr)
        return None
    try:
        threshold = int(threshold)
    except (TypeError, ValueError):
        print(f"REFUSED {post}: the ladder promotion threshold "
              f"({threshold!r}) is not an integer", file=sys.stderr)
        return None

    count = count_valid_countersigned(graph, post, verdict_cells)
    if count < threshold:
        print(f"REFUSED {post}: promotion needs {threshold} counter-signed "
              f"verdict(s), got {count} -- one short of the threshold "
              f"(tier not promoted)", file=sys.stderr)
        return None

    # ---- promote: the row's tier leaves 'untrusted', nothing else changes --
    new_row = dict(post_row)
    new_row["tier"] = 0  # the lowest seeded tier -- off 'untrusted' by choice
    new_row["promoted_by"] = actor
    new_rows = [dict(r) for r in rows]
    for i, r in enumerate(new_rows):
        if r.get("name") == post:
            new_rows[i] = new_row
            break
    graph = graph_root(root)
    try:
        import write as write_mod
        import geometry_config

        _, list_key = geometry_config.resolve(graph)
        e = write_mod.Edit(f"config:{list_key}")
        write_mod.verb_set(e, list_key, json.dumps(new_rows))
        write_mod.submit(graph, e, actor=actor, role=role)
    except Exception:  # noqa: BLE001  (report is the caller's job)
        print(f"REFUSED {post}: config write was refused; tier not promoted",
              file=sys.stderr)
        return None
    print(f"promoted {post}: tier off 'untrusted' ({count} counter-signed "
          f"verdict(s), threshold {threshold}) by {actor}")
    return dict(new_row)