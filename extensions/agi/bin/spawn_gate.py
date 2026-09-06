#!/usr/bin/env python3
"""spawn_gate.py — the schema spawn gate (GOALS.md S17).

Seven node types were in daily use and `context/schemas/` declared six —
with `verdict`, the type `evidence_gate.py` exists to police, absent
entirely. Nothing anywhere checked a node against a schema at write time, so
the spawn rules were a **prose control**: real, written down, and enforced by
whoever happened to remember. GOALS.md's design ethic forbids exactly that —
"no prose-only controls where a code control is possible".

This module is that control, as code. It is deliberately shaped like
`bin/evidence_gate.py`, which is the in-house precedent: self-contained, no
`schema_registry` import, importable from both writer paths
(`bin/cli.py scaffold` / `done`, `bin/post_wire.py`), and loud on every
outcome.

The rule, and where it comes from
---------------------------------
**The schema is data; this file is only the enforcement.** Every per-type
value — which parent types are legal, how many parents are allowed — lives in
a `spawn:` block in `context/schemas/[<type>].md` and nowhere else. Copying
the table into Python would recreate the defect S17 names: one fact with
three definitions (`find-root.sh`, `level3.py`, `grid.py` for the engine
root). Two cross-cutting facts live in `context/schemas/[shape].md`:

- `parentless_types` — the ONLY shapes allowed an empty `parents` list.
  Exactly three: `goal:long-term`, `goal:short-term`, `idea`.
- `max_parents_ceiling` — no type may declare more without raising this too.
  Two deliberate edits, which is the point: 2 is what the corpus uses, and
  raising it is an act rather than a default.

Both are enforced against the schemas themselves at load time. A schema that
breaks either is **not used** — it is reported and its type falls back to
unverified, because a broken rule must not silently enforce something nobody
wrote.

Feedback on BOTH outcomes
-------------------------
A validator that only speaks on failure teaches nothing: an agent cannot tell
"approved" from "not checked". So `announce()` prints on every path.

  ================================================================
  approved    every rule passed. Names the schema file and each rule
              applied, so the approval is auditable and distinguishable
              from silence.
  rejected    a decidable rule failed. Names the rule, the schema file,
              the node, and what would fix it. Nothing is written.
  unverified  the rule could not be decided — no schema for the type, no
              `spawn:` block, a broken rule, or a parent id that resolves
              to no node. Fail OPEN: warn, allow, stamp. A missing schema
              must never block the loop, and G7.1 settled that inferring a
              missing edge is inventing one.
  bypassed    `--no-spawn-gate`. Loud, and stamped `spawn_gate: bypassed`
              so any such node reads as unreviewed.
  ================================================================

Why there is no "demote"
------------------------
`evidence_gate.py` has three outcomes because an overclaimed verdict can be
*softened* — `proved` has an honest weaker form. A structural violation has
no weaker form. You cannot half-parent a node, and you cannot invent the
missing parent (G7.1). So the axis is decidable/undecidable, not
strong/weak: reject what is decidably wrong, warn on what cannot be decided.

What this does NOT do
---------------------
It does not touch history. 51 nodes in the corpus violate `min_parents`
today (24 hypothesis, 21 verdict, 4 experiment, 2 level3). That is a
**report, not a purge** — G7's first invariant is that node count never
drops. This gate runs on the writer path, so those 51 keep their place and no
new one joins them.
"""
from __future__ import annotations

import sys
from dataclasses import dataclass, field
from pathlib import Path

# goal:g11.1 — one resolver for every path.
sys.path.insert(0, str(Path(__file__).resolve().parent))
import locations  # noqa: E402

#: Where the schemas live, relative to the graph root. Mirrors
#: `schema_registry/loader.py`'s caller; also declared in
#: `context/schemas/[config].md :: locations.schemas_root`.
SCHEMAS_SUBDIR = ("context", "schemas")

#: Fallback for `locations.nodes_root` when `[config].md` is absent.
DEFAULT_NODES_SUBDIR = "nodes"

#: Fallback geometry, used only when `[shape].md` is missing. Deliberately
#: identical to what that file ships, so a project without it behaves the
#: same rather than differently-and-quietly.
FALLBACK_PARENTLESS = ("goal:long-term", "goal:short-term", "idea")
FALLBACK_CEILING = 2

APPROVED = "approved"
REJECTED = "rejected"
UNVERIFIED = "unverified"
BYPASSED = "bypassed"


def canonical_type(name) -> str:
    """`bigger-outcome` and `bigger_outcome` are one type (`[shape].md`).

    Both spellings exist in the corpus — 17/2 for `bigger_outcome`, 15/2 for
    `app_purpose` — and one `app_purpose` node names a parent typed
    `bigger-outcome`, so the split shows up in an *edge*, not just a
    filename. Canonicalising on both sides of every comparison is what lets
    that correct edge validate without renaming a single node file.
    """
    if not isinstance(name, str):
        return ""
    return name.strip().replace("-", "_")


@dataclass(frozen=True)
class Rule:
    """One resolved spawn rule: what may parent this shape, and how many."""

    allowed_parents: frozenset
    min_parents: int
    max_parents: int
    variant: str = ""  # non-empty when the schema is discriminated
    #: Per-parent-type floors, as sorted (type, count) pairs so `Rule` stays
    #: hashable. `min_parents` says "how many parents"; this says "how many
    #: of *which kind*" — the distinction `bigger_outcome` needs, where one
    #: verdict plus one outcome is a different shape from two outcomes.
    #: Empty tuple means the type declares no per-type floor.
    min_parents_by_type: tuple = ()
    #: Exact permitted parent-type multisets, as sorted tuples. Where
    #: `min_parents_by_type` is an AND across kinds, this is an **OR across
    #: whole shapes** -- `build` needs it because its rule is genuinely a
    #: disjunction: one `mvp`, OR one `build` and one `goal` together, and
    #: neither of those halves alone. Empty tuple = no shape restriction, so
    #: every type that does not declare it is unaffected.
    parent_shapes: tuple = ()
    #: Which types a node of this shape may have in `season_parents:`.
    #: Empty frozenset means the type does not support season_parents
    #: at all, and any season_parents entry is refused.
    season_parents_allowed: frozenset = frozenset()


@dataclass
class SpawnSchema:
    """The `spawn:` block of one `[<type>].md`, parsed."""

    name: str
    source: str                     # display path, e.g. context/schemas/[verdict].md
    discriminator: str = ""
    flat: Rule | None = None
    variants: dict = field(default_factory=dict)
    error: str = ""                 # non-empty => refuse to enforce this schema

    def rule_for(self, fm: dict | None) -> tuple[Rule | None, str]:
        """Resolve the effective rule for a node, returning (rule, why-not)."""
        if self.error:
            return None, self.error
        if not self.discriminator:
            if self.flat is None:
                return None, f"schema '{self.name}' declares no spawn: block"
            return self.flat, ""
        value = (fm or {}).get(self.discriminator)
        if not isinstance(value, str) or not value.strip():
            return None, (
                f"schema '{self.name}' is discriminated on "
                f"'{self.discriminator}', which this node does not set"
            )
        rule = self.variants.get(value.strip())
        if rule is None:
            return None, (
                f"schema '{self.name}' declares no variant for "
                f"{self.discriminator}='{value.strip()}' "
                f"(known: {', '.join(sorted(self.variants)) or 'none'})"
            )
        return rule, ""


@dataclass
class Geometry:
    """`[shape].md`'s two cross-cutting facts."""

    parentless_types: frozenset = frozenset(FALLBACK_PARENTLESS)
    max_parents_ceiling: int = FALLBACK_CEILING
    source: str = "<default>"
    #: `edge_fields` from `[shape].md`: field name -> {role, traversable}.
    #: Empty when the project does not declare it, which is why
    #: `is_traversable` fails OPEN — an undeclared field keeps whatever
    #: behaviour it had rather than silently dropping out of a walk.
    edge_fields: dict = field(default_factory=dict)

    def is_traversable(self, field_name) -> bool:
        """May a chain/metric walk follow this edge field?

        False only for a field explicitly declared `traversable: false`.
        `depends_on` is the case this exists for: it orders the build, it is
        not descent, and counting it would make build order inflate depth.
        """
        entry = self.edge_fields.get(str(field_name).strip())
        if isinstance(entry, dict) and "traversable" in entry:
            return bool(entry["traversable"])
        return True

    def scheduling_edges(self) -> frozenset:
        """Edge fields declared non-traversable — the walk's deny-list."""
        return frozenset(
            k for k, v in self.edge_fields.items()
            if isinstance(v, dict) and v.get("traversable") is False
        )


@dataclass
class SpawnRules:
    """Everything loaded from `context/schemas/`."""

    schemas: dict = field(default_factory=dict)   # canonical type -> SpawnSchema
    geometry: Geometry = field(default_factory=Geometry)
    schema_errors: list = field(default_factory=list)   # (source, message)
    locations: dict = field(default_factory=dict)       # [config].md locations

    def get(self, node_type) -> SpawnSchema | None:
        return self.schemas.get(canonical_type(node_type))


def _read_frontmatter(path: Path) -> dict | None:
    """Plain YAML frontmatter read. Same cheap scan `build_corpus` uses."""
    import yaml

    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        fm = yaml.safe_load(parts[1]) or {}
    except Exception:
        return None
    return fm if isinstance(fm, dict) else None


def _parse_min_by_type(raw, allowed: frozenset, max_p: int) -> tuple[tuple, str]:
    """Parse `spawn.min_parents_by_type`, refusing any rule nobody can satisfy.

    Four ways a per-type floor is unsatisfiable, and all four are schema
    errors rather than runtime rejections — a rule that no node could ever
    pass would reject the whole type forever, which is a louder failure than
    the missing rule it replaced. Same instinct as the geometry checks: a
    broken rule is not enforced, it is reported.
    """
    if raw is None:
        return (), ""
    if not isinstance(raw, dict) or not raw:
        return (), "spawn.min_parents_by_type must be a non-empty mapping of type -> count"
    out: dict[str, int] = {}
    for k, v in raw.items():
        t = canonical_type(k)
        if not t:
            return (), f"spawn.min_parents_by_type has an unusable type key {k!r}"
        try:
            n = int(v)
        except (TypeError, ValueError):
            return (), f"spawn.min_parents_by_type['{t}'] must be an integer, got {v!r}"
        if isinstance(v, bool) or n < 1:
            return (), (
                f"spawn.min_parents_by_type['{t}'] must be >= 1; drop the key "
                "instead of writing 0"
            )
        if t not in allowed:
            return (), (
                f"spawn.min_parents_by_type requires {n} parent(s) of type "
                f"'{t}', which spawn.allowed_parents does not permit "
                f"({sorted(allowed) or 'none'}). Add it there or drop the floor."
            )
        out[t] = n
    total = sum(out.values())
    if total > max_p:
        return (), (
            f"spawn.min_parents_by_type requires {total} parent(s) in total "
            f"but max_parents is {max_p}: no node could satisfy this. Raise "
            "max_parents (and the ceiling in [shape].md) or lower the floors."
        )
    return tuple(sorted(out.items())), ""


def _parse_parent_shapes(raw, allowed: frozenset, min_p: int, max_p: int) -> tuple[tuple, str]:
    """Parse `spawn.parent_shapes`, refusing any shape nobody can satisfy.

    Same discipline as `_parse_min_by_type` and for the same reason: a schema
    that declares an impossible rule rejects every node of its type forever,
    loudly but uselessly, and the failure surfaces at the first spawn rather
    than at the edit that caused it.

    Each shape is a list of parent TYPE names. A node satisfies the rule when
    its parents' types, as a sorted multiset, equal one of them exactly --
    exact rather than superset, because "one mvp" and "one mvp plus a goal"
    are different claims about where a build node came from, and permitting
    the second silently would make the first unenforceable.
    """
    if raw is None:
        return (), ""
    if not isinstance(raw, (list, tuple)) or not raw:
        return (), "spawn.parent_shapes must be a non-empty list of type lists"
    shapes = []
    for entry in raw:
        if not isinstance(entry, (list, tuple)) or not entry:
            return (), f"spawn.parent_shapes entry {entry!r} must be a non-empty list"
        types = tuple(sorted(canonical_type(x) for x in entry))
        if any(not x for x in types):
            return (), f"spawn.parent_shapes entry {entry!r} has an unusable type name"
        bad = [x for x in types if x not in allowed]
        if bad:
            return (), (
                f"spawn.parent_shapes entry {list(entry)!r} names "
                f"{sorted(set(bad))}, which spawn.allowed_parents does not "
                f"permit ({sorted(allowed)})"
            )
        if not (min_p <= len(types) <= max_p):
            return (), (
                f"spawn.parent_shapes entry {list(entry)!r} has {len(types)} "
                f"parent(s), outside spawn.min_parents={min_p}..max_parents={max_p}"
            )
        if types not in shapes:
            shapes.append(types)
    return tuple(shapes), ""



def _parse_rule(block, variant: str = "") -> tuple[Rule | None, str]:
    if not isinstance(block, dict):
        return None, "spawn block is not a mapping"
    allowed = block.get("allowed_parents", None)
    if allowed is None or not isinstance(allowed, (list, tuple)):
        return None, "spawn.allowed_parents must be a list (use [] for parentless)"
    try:
        min_p = int(block.get("min_parents", 1))
        max_p = int(block.get("max_parents", 1))
    except (TypeError, ValueError):
        return None, "spawn.min_parents/max_parents must be integers"
    if min_p < 0 or max_p < min_p:
        return None, f"spawn bounds are incoherent (min={min_p}, max={max_p})"
    allowed_set = frozenset(canonical_type(a) for a in allowed)

    by_type, err = _parse_min_by_type(block.get("min_parents_by_type"), allowed_set, max_p)
    if err:
        return None, err

    shapes, err = _parse_parent_shapes(
        block.get("parent_shapes"), allowed_set, min_p, max_p)
    if err:
        return None, err

    spa_raw = block.get("season_parents_allowed")
    if spa_raw is not None:
        if not isinstance(spa_raw, (list, tuple)) or not spa_raw:
            return None, "spawn.season_parents_allowed must be a non-empty list of types"
        spa_set = frozenset(canonical_type(x) for x in spa_raw)
        if any(not x for x in spa_set):
            return None, "spawn.season_parents_allowed has an unusable type name"
    else:
        spa_set = frozenset()

    return Rule(
        allowed_parents=allowed_set,
        min_parents=min_p,
        max_parents=max_p,
        min_parents_by_type=by_type,
        parent_shapes=shapes,
        season_parents_allowed=spa_set,
        variant=variant,
    ), ""


def _display(path: Path, root: Path | None) -> str:
    if root is not None:
        try:
            return str(path.relative_to(root))
        except ValueError:
            pass
    return str(path)


def load_spawn_rules(schemas_dir, root=None) -> SpawnRules:
    """Load every ACTIVE schema's `spawn:` block, plus `[shape].md` geometry.

    Active means bracketed: `[name].md` is active, `name.md` is inactive
    (`schema_registry/loader.py`). An inactive schema is never enforced —
    same convention, so a schema parked by un-bracketing it stops gating
    immediately, which is how you turn a rule off without deleting it.

    Two schema-level invariants are checked here, against `[shape].md`, and
    a schema that fails either is recorded in `schema_errors` and **not
    enforced** (its type becomes `unverified`):

    1. `min_parents: 0` only for a shape in `parentless_types`. Without
       this, any schema could quietly license its own type to float free,
       and "exactly three may be parentless" would be prose again.
    2. `max_parents <= max_parents_ceiling`. Raising a type's budget takes
       two edits — the type file and `[shape].md` — so it cannot happen by
       reflex while writing a schema.
    """
    d = Path(schemas_dir)
    rules = SpawnRules()
    if not d.is_dir():
        rules.schema_errors.append((str(d), "schemas directory does not exist"))
        return rules

    raw: dict[str, tuple[SpawnSchema, dict]] = {}
    for p in sorted(d.iterdir()):
        if not p.is_file() or p.suffix.lower() not in {".md", ".json"}:
            continue
        stem = p.stem
        if not (stem.startswith("[") and stem.endswith("]")):
            continue  # inactive: never enforced
        fm = _read_frontmatter(p)
        if fm is None:
            rules.schema_errors.append((_display(p, root), "unreadable frontmatter"))
            continue
        name = canonical_type(fm.get("name") or stem[1:-1])
        src = _display(p, root)
        if name == "shape":
            rules.geometry = _parse_geometry(fm, src, rules)
            continue
        if name == "config":
            loc = fm.get("locations")
            if isinstance(loc, dict):
                rules.locations = loc
            continue
        raw[name] = (SpawnSchema(name=name, source=src), fm)

    for name, (schema, fm) in raw.items():
        block = fm.get("spawn")
        if block is None:
            rules.schemas[name] = schema  # no spawn: block -> unverified, not an error
            continue
        if not isinstance(block, dict):
            schema.error = "spawn: is not a mapping"
            rules.schemas[name] = schema
            continue
        disc = block.get("discriminator")
        if disc:
            schema.discriminator = str(disc)
            variants = block.get("variants")
            if not isinstance(variants, dict) or not variants:
                schema.error = "spawn.discriminator set but spawn.variants is empty"
            else:
                for vname, vblock in variants.items():
                    rule, err = _parse_rule(vblock, variant=str(vname))
                    if rule is None:
                        schema.error = f"variant '{vname}': {err}"
                        break
                    schema.variants[str(vname)] = rule
        else:
            rule, err = _parse_rule(block)
            if rule is None:
                schema.error = err
            else:
                schema.flat = rule
        if not schema.error:
            schema.error = _check_against_geometry(schema, rules.geometry)
        if schema.error:
            rules.schema_errors.append((schema.source, schema.error))
        rules.schemas[name] = schema
    return rules


def _parse_geometry(fm: dict, src: str, rules: SpawnRules) -> Geometry:
    geo = Geometry(source=src)
    pt = fm.get("parentless_types")
    if isinstance(pt, (list, tuple)) and pt:
        geo.parentless_types = frozenset(
            canonical_shape_key(x) for x in pt if isinstance(x, str)
        )
    else:
        rules.schema_errors.append((src, "parentless_types missing or empty"))
    ef = fm.get("edge_fields")
    if isinstance(ef, dict):
        geo.edge_fields = {
            str(k): v for k, v in ef.items() if isinstance(v, dict)
        }
    ceiling = fm.get("max_parents_ceiling")
    if isinstance(ceiling, int) and not isinstance(ceiling, bool) and ceiling >= 0:
        geo.max_parents_ceiling = ceiling
    else:
        rules.schema_errors.append((src, "max_parents_ceiling missing or not an int"))
    return geo


def _shape_key(type_name: str, variant: str) -> str:
    """How `parentless_types` names a shape: `idea`, or `goal:long-term`."""
    return f"{canonical_type(type_name)}:{variant}" if variant else canonical_type(type_name)


def canonical_shape_key(value) -> str:
    """Canonicalise a `parentless_types` entry — **type half only**.

    `canonical_type` cannot be applied to the whole string: a discriminator
    *value* may legitimately contain a hyphen (`goal_kind: long-term`, and
    every one of the 10 long-term goals uses that spelling). Rewriting the
    variant half turned `goal:long-term` into `goal:long_term`, which then
    matched no shape key and made the whole `[goal].md` schema unenforceable.
    Only the type half has two spellings; the variant half has one.
    """
    if not isinstance(value, str):
        return ""
    s = value.strip()
    if ":" in s:
        t, v = s.split(":", 1)
        return f"{canonical_type(t)}:{v.strip()}"
    return canonical_type(s)


def _check_against_geometry(schema: SpawnSchema, geo: Geometry) -> str:
    candidates = list(schema.variants.items()) if schema.variants else []
    if schema.flat is not None:
        candidates.append(("", schema.flat))
    for vname, rule in candidates:
        key = _shape_key(schema.name, vname)
        if rule.min_parents == 0 and key not in geo.parentless_types:
            return (
                f"'{key}' declares min_parents: 0 but is not in "
                f"parentless_types ({geo.source}). Exactly three shapes may "
                f"be parentless: {', '.join(sorted(geo.parentless_types))}."
            )
        if rule.max_parents > geo.max_parents_ceiling:
            return (
                f"'{key}' declares max_parents: {rule.max_parents}, above the "
                f"ceiling of {geo.max_parents_ceiling} in {geo.source}. "
                "Raising a type's budget is a deliberate act: raise the "
                "ceiling there too, or lower it here."
            )
    return ""


def build_type_index(nodes_dir) -> dict:
    """Map every real node id to its canonical type.

    The counterpart of `evidence_gate.build_corpus`, which maps ids to
    existence; this needs the type as well, to check `allowed_parents`. Same
    cheap frontmatter scan, same reason: both writer paths must be able to
    build it without loading the full graph.
    """
    index: dict[str, str] = {}
    p = Path(nodes_dir)
    if not p.is_dir():
        return index
    for nf in sorted(p.rglob("*.md")):
        fm = _read_frontmatter(nf)
        if not fm:
            continue
        nid = fm.get("id")
        if isinstance(nid, str) and nid.strip():
            index[nid.strip()] = canonical_type(fm.get("type") or "")
    return index


def resolve_nodes_root(root, schemas_dir=None) -> Path:
    """Where the node corpus lives, per `[config].md :: locations.nodes_root`.

    This is the one field of `[config].md` a code path actually reads, which
    is the bar G10.2 sets for a geometry declaration ("a `.geometry/`
    directory the engine does not consult is prose with a directory name").
    Non-circular: the schemas directory is found by the existing root walk,
    and `nodes_root` is a different fact. Falls back to `<root>/nodes` when
    the schema is absent, so a project without it still works.
    """
    root = Path(root)
    sd = Path(schemas_dir) if schemas_dir else root.joinpath(*SCHEMAS_SUBDIR)
    declared = None
    cfg = sd / "[config].md"
    if cfg.is_file():
        fm = _read_frontmatter(cfg) or {}
        loc = fm.get("locations")
        if isinstance(loc, dict):
            entry = loc.get("nodes_root")
            if isinstance(entry, dict):
                declared = entry.get("path")
    if isinstance(declared, str) and declared.startswith("<graph_root>/"):
        rel = declared[len("<graph_root>/"):].strip("/")
        if rel:
            return root / rel
    return root / DEFAULT_NODES_SUBDIR


def read_ladder_season(nodes_dir: Path) -> int | None:
    """Read `current_season` from `.geometry/ladder.md`.

    Returns None if the ladder node does not exist or cannot be read,
    which fails OPEN: season_parents checking is skipped and the node
    is written. A missing ladder must never block the loop.
    """
    ladder = Path(nodes_dir) / ".geometry" / "ladder.md"
    if not ladder.is_file():
        return None
    fm = _read_frontmatter(ladder)
    if not fm:
        return None
    cs = fm.get("current_season")
    if isinstance(cs, int) and not isinstance(cs, bool):
        return cs
    return None


def read_node_season(fm: dict | None) -> int | None:
    """Read `season:` from a node's frontmatter.

    Returns None when absent (pre-season-1 node), int when present.
    """
    if not isinstance(fm, dict):
        return None
    s = fm.get("season")
    if isinstance(s, int) and not isinstance(s, bool):
        return s
    return None


@dataclass
class SpawnResult:
    """What the gate decided, and enough detail to print either outcome."""

    status: str = APPROVED
    node_type: str = ""
    node_id: str = ""
    parents: list = field(default_factory=list)
    rule: Rule | None = None
    source: str = ""                 # the schema file the rule came from
    applied: list = field(default_factory=list)   # human names of rules that passed
    reason: str = ""
    fix: str = ""
    messages: list = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """True when the write may proceed. Only `rejected` stops it."""
        return self.status != REJECTED

    @property
    def approved(self) -> bool:
        return self.status == APPROVED


def check_spawn(
    node_type,
    parents,
    *,
    rules: SpawnRules,
    type_index: dict | None = None,
    fm: dict | None = None,
    node_id: str = "",
    bypass: bool = False,
    season_parents: list | None = None,
    current_season: int | None = None,
) -> SpawnResult:
    """Check one spawn against the schema. Never raises.

    `parents` is the node's `parents` list (ids). `type_index` maps id ->
    type (`build_type_index`); pass `None` and parent-type checking is
    skipped as unverifiable rather than silently passed — same fail-closed
    instinct as `evidence_gate.normalize_evidence_runs(corpus=None)`, except
    that here failing closed means *declining to approve*, not rejecting,
    because a type we cannot resolve is not evidence of a wrong type.

    `season_parents` is the node's `season_parents:` list (ids).
    `current_season` is the ladder's current_season; pass None to skip
    season_parents checking entirely (old callers that don't need it).
    """
    ntype = canonical_type(node_type)
    plist = [p.strip() for p in (parents or []) if isinstance(p, str) and p.strip()]
    res = SpawnResult(node_type=ntype, node_id=node_id or f"{ntype}:<new>",
                      parents=list(plist))

    if bypass:
        res.status = BYPASSED
        res.reason = "spawn gate bypassed via --no-spawn-gate"
        res.messages.append(
            f"SPAWN-GATE BYPASSED: {res.node_id} written without a schema "
            "check. This node is unreviewed; a reviewer must check its "
            "parents by hand."
        )
        return res

    schema = rules.get(ntype)
    if schema is None:
        res.status = UNVERIFIED
        res.reason = f"no active schema for type '{ntype}'"
        res.messages.append(
            f"SPAWN-GATE UNVERIFIED: {res.node_id} — no active schema "
            f"[{ntype}].md in context/schemas/, so no spawn rule could be "
            "applied. The node is written. Declare the type to gate it "
            "(bracketed filename = active)."
        )
        return res
    res.source = schema.source

    rule, why_not = schema.rule_for(fm)
    if rule is None:
        res.status = UNVERIFIED
        res.reason = why_not
        res.messages.append(
            f"SPAWN-GATE UNVERIFIED: {res.node_id} — {why_not} "
            f"({schema.source}). The node is written, unchecked."
        )
        return res
    res.rule = rule

    shape = _shape_key(ntype, rule.variant)

    # 1. min_parents.
    if len(plist) < rule.min_parents:
        res.status = REJECTED
        res.reason = (
            f"rule 'min_parents' ({rule.min_parents}) from {schema.source}: "
            f"{shape} declares {len(plist)} parent(s)"
        )
        res.fix = (
            f"give {res.node_id} at least {rule.min_parents} parent of type "
            f"{{{', '.join(sorted(rule.allowed_parents)) or 'n/a'}}}. Only "
            f"{', '.join(sorted(rules.geometry.parentless_types))} may be "
            f"parentless ({rules.geometry.source}). Do not invent a parent "
            "to satisfy this — pick the node this one actually follows from."
        )
        _reject_message(res, shape, schema)
        return res
    res.applied.append(f"min_parents>={rule.min_parents}")

    # 2. max_parents.
    if len(plist) > rule.max_parents:
        res.status = REJECTED
        res.reason = (
            f"rule 'max_parents' ({rule.max_parents}) from {schema.source}: "
            f"{shape} declares {len(plist)} parents {plist}"
        )
        res.fix = (
            f"drop {len(plist) - rule.max_parents} parent(s) from "
            f"{res.node_id}, or raise max_parents in {schema.source} AND the "
            f"ceiling in {rules.geometry.source}. The budget is "
            f"{rule.max_parents} because {rule.max_parents} is what the "
            "corpus has ever used; raising it is a deliberate act, not a "
            "default."
        )
        _reject_message(res, shape, schema)
        return res
    res.applied.append(f"max_parents<={rule.max_parents}")

    # 3. allowed_parents, per parent, by resolved type.
    if plist:
        if type_index is None:
            res.status = UNVERIFIED
            res.reason = "no node index available to resolve parent types"
            res.messages.append(
                f"SPAWN-GATE UNVERIFIED: {res.node_id} — parent counts pass "
                f"({schema.source}) but parent *types* could not be resolved: "
                "no node index. The node is written."
            )
            return res
        unresolved = []
        for pid in plist:
            ptype = type_index.get(pid)
            if ptype is None:
                unresolved.append(pid)
                continue
            if ptype not in rule.allowed_parents:
                res.status = REJECTED
                res.reason = (
                    f"rule 'allowed_parents' from {schema.source}: {shape} "
                    f"may not be parented by '{ptype}' (parent {pid!r}); "
                    f"allowed: {sorted(rule.allowed_parents)}"
                )
                res.fix = (
                    f"reparent {res.node_id} onto a node of type "
                    f"{{{', '.join(sorted(rule.allowed_parents))}}}, or add "
                    f"'{ptype}' to spawn.allowed_parents in {schema.source} "
                    "if the corpus really uses that shape."
                )
                _reject_message(res, shape, schema)
                return res
        if unresolved:
            res.status = UNVERIFIED
            res.reason = f"parent id(s) resolve to no node: {unresolved}"
            res.messages.append(
                f"SPAWN-GATE UNVERIFIED: {res.node_id} — parent(s) "
                f"{unresolved} name no node in the corpus, so their type "
                f"could not be checked against {schema.source}. The node is "
                "written. Fix the reference, or drop it — never infer one "
                "(G7.1)."
            )
            return res
        res.applied.append(
            f"allowed_parents={{{', '.join(sorted(rule.allowed_parents))}}}"
        )

        # 4. min_parents_by_type — per-kind floors. Only reachable once every
        #    parent id resolved to a type above, which is what makes a
        #    shortfall decidable rather than a guess.
        if rule.min_parents_by_type:
            have: dict[str, int] = {}
            for pid in plist:
                ptype = type_index.get(pid, "")
                have[ptype] = have.get(ptype, 0) + 1
            short = [
                (t, n, have.get(t, 0))
                for t, n in rule.min_parents_by_type
                if have.get(t, 0) < n
            ]
            if short:
                res.status = REJECTED
                res.reason = (
                    f"rule 'min_parents_by_type' from {schema.source}: {shape} "
                    + "; ".join(
                        f"needs {n} parent(s) of type '{t}', has {got}"
                        for t, n, got in short
                    )
                )
                res.fix = (
                    f"give {res.node_id} "
                    + ", ".join(f"{n - got} more '{t}'" for t, n, got in short)
                    + " parent(s). This type converges several kinds of "
                    "evidence on purpose: the floor is what stops an "
                    "aggregate from resting on one kind. Do not invent a "
                    "parent to satisfy it (G7.1) — if the node is not ready "
                    "to aggregate, it is not ready to be written."
                )
                _reject_message(res, shape, schema)
                return res
            res.applied.append(
                "min_parents_by_type={"
                + ", ".join(f"{t}>={n}" for t, n in rule.min_parents_by_type)
                + "}"
            )

        # 5. parent_shapes — an OR across whole shapes, where the rule above is
        #    an AND across kinds. `build` is the type that needs it: a build
        #    node comes from ONE mvp, or from an existing build node together
        #    with the goal that motivated the new version — and neither half
        #    alone. `allowed_parents` cannot say that; it would also permit a
        #    lone goal, which must not mint a build node out of nothing.
        if rule.parent_shapes:
            got = tuple(sorted(type_index.get(pid, "") for pid in plist))
            if got not in rule.parent_shapes:
                res.status = REJECTED
                pretty = " or ".join(
                    "[" + ", ".join(s) + "]" for s in rule.parent_shapes)
                res.reason = (
                    f"rule 'parent_shapes' from {schema.source}: {shape} has "
                    f"parents [{', '.join(got)}], which is not one of {pretty}"
                )
                res.fix = (
                    f"give {res.node_id} one of: {pretty}. For a build node "
                    "that means EITHER the mvp that specifies it, OR the build "
                    "node this is a new version of together with the goal that "
                    "motivated the change. A goal alone cannot mint a build "
                    "node — it can only motivate a new version of one that has "
                    "already earned its place (goal:g6.3, goal:s29)."
                )
                _reject_message(res, shape, schema)
                return res
            res.applied.append(
                "parent_shapes=[" + ", ".join(got) + "]")

    # 6. season_parents: validate by type, with grandfathering.
    if season_parents is not None and rule.season_parents_allowed:
        splist = [p.strip() for p in season_parents
                  if isinstance(p, str) and p.strip()]
        if splist:
            # Grandfathering: nodes with season < current_season skip check.
            node_season = read_node_season(fm)
            if current_season is not None and node_season is not None \
                    and node_season < current_season:
                res.applied.append(
                    f"season_parents grandfathered (season {node_season} < "
                    f"current {current_season})")
            elif current_season is not None and node_season is None \
                    and current_season == 1:
                res.applied.append(
                    "season_parents grandfathered (no season, current=1)")
            else:
                if type_index is None:
                    res.status = UNVERIFIED
                    res.reason = "no node index to resolve season_parents"
                    res.messages.append(
                        f"SPAWN-GATE UNVERIFIED: {res.node_id} — "
                        f"season_parents could not be checked: no node index. "
                        "The node is written.")
                    return res
                unresolved = []
                for spid in splist:
                    ptype = type_index.get(spid)
                    if ptype is None:
                        unresolved.append(spid)
                        continue
                    if ptype not in rule.season_parents_allowed:
                        res.status = REJECTED
                        res.reason = (
                            f"rule 'season_parents_allowed' from "
                            f"{schema.source}: {shape} season_parent "
                            f"{spid!r} has type '{ptype}', allowed "
                            f"types: {sorted(rule.season_parents_allowed)}")
                        res.fix = (
                            f"give {res.node_id} season_parents of type "
                            f"{{{', '.join(sorted(rule.season_parents_allowed))}}}, "
                            f"or add '{ptype}' to spawn.season_parents_allowed "
                            f"in {schema.source}.")
                        _reject_message(res, shape, schema)
                        return res
                if unresolved:
                    res.status = UNVERIFIED
                    res.reason = f"season_parents id(s) resolve to no node: {unresolved}"
                    res.messages.append(
                        f"SPAWN-GATE UNVERIFIED: {res.node_id} — "
                        f"season_parents {unresolved} name no node. "
                        "The node is written.")
                    return res
                res.applied.append(
                    f"season_parents_allowed="
                    f"{{{', '.join(sorted(rule.season_parents_allowed))}}}")
    elif season_parents is not None and not rule.season_parents_allowed \
            and season_parents:
        # Type does not support season_parents at all -> refuse.
        res.status = REJECTED
        res.reason = (
            f"rule 'season_parents_allowed' from {schema.source}: {shape}"
            f" does not declare season_parents_allowed, but has "
            f"season_parents entries")
        res.fix = (
            f"remove season_parents from {res.node_id}, or add "
            f"spawn.season_parents_allowed to {schema.source}.")
        _reject_message(res, shape, schema)
        return res

    res.status = APPROVED
    res.messages.append(
        f"SPAWN-GATE APPROVED: {res.node_id} checked against "
        f"{schema.source} [{shape}] — {'; '.join(res.applied)}. "
        f"parents={plist or '[] (parentless-legal)'}"
    )
    return res


def _reject_message(res: SpawnResult, shape: str, schema: SpawnSchema) -> None:
    res.messages.append(
        f"SPAWN-GATE REJECTED: {res.node_id} — {res.reason}. "
        f"Schema: {schema.source} (shape '{shape}'). Fix: {res.fix}"
    )


def announce(res: SpawnResult, stream=None) -> None:
    """Print on EVERY outcome — that is the point of this gate.

    Full explanation to stderr, one grep-able line to stdout (the driver tees
    stdout into loop.log), matching `evidence_gate.announce`. An approval is
    printed as loudly as a rejection, because "approved" and "not checked"
    must never look the same to an agent reading its own terminal.
    """
    stream = stream if stream is not None else sys.stderr
    marker = "!!" if res.status in (REJECTED, BYPASSED) else "--"
    for m in res.messages:
        print(f"{marker} {m}", file=stream)
    if res.status == REJECTED:
        print(f"SPAWN-GATE REJECTED {res.node_id} type={res.node_type} "
              f"parents={len(res.parents)} schema={res.source}")
    elif res.status == UNVERIFIED:
        print(f"SPAWN-GATE UNVERIFIED {res.node_id} type={res.node_type} "
              f"reason={res.reason}")
    elif res.status == BYPASSED:
        print(f"SPAWN-GATE BYPASSED {res.node_id} type={res.node_type}")
    else:
        print(f"SPAWN-GATE APPROVED {res.node_id} type={res.node_type} "
              f"schema={res.source} rules={','.join(res.applied) or 'none'}")


def announce_schema_errors(rules: SpawnRules, stream=None) -> None:
    """Report schemas that were refused. Silent when there are none."""
    stream = stream if stream is not None else sys.stderr
    for src, msg in rules.schema_errors:
        print(f"!! SPAWN-GATE SCHEMA ERROR: {src}: {msg} — this schema is "
              f"NOT enforced; its type falls back to unverified.", file=stream)


def stamp(fm: dict, res: SpawnResult) -> dict:
    """Record a non-clean decision in a node's frontmatter.

    Approval is deliberately NOT stamped: it is the normal path, and a field
    on every node in the graph is noise, not signal. The approval line on the
    terminal is the feedback (see the module docstring). Only the two states
    a reviewer needs to find later leave a mark.
    """
    if res.status == BYPASSED:
        fm["spawn_gate"] = "bypassed"
    elif res.status == UNVERIFIED:
        fm["spawn_check"] = "unverified"
        fm["spawn_check_reason"] = res.reason
    return fm


def gate_for_root(root, nodes_dir=None) -> tuple[SpawnRules, dict, int | None]:
    """Convenience for the writer paths: rules + type index + current season."""
    root = Path(root)
    schemas_dir = root.joinpath(*SCHEMAS_SUBDIR)
    rules = load_spawn_rules(schemas_dir, root=root)
    nd = Path(nodes_dir) if nodes_dir else resolve_nodes_root(root, schemas_dir)
    cs = read_ladder_season(nd)
    return rules, build_type_index(nd), cs


def _cli(argv) -> int:
    """`spawn_gate.py check --type T --parent P [--parent P] [--id ID]`.

    A thin front end over the same code the writer paths call — useful for
    checking a spawn before writing it, and for the S17 falsifier. Exit 2 on
    rejection, matching `cli.py done`'s convention for a taxonomy failure.
    """
    import argparse

    ap = argparse.ArgumentParser(prog="spawn_gate.py")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check")
    c.add_argument("--type", dest="node_type", required=True)
    c.add_argument("--parent", dest="parents", action="append", default=[])
    c.add_argument("--id", dest="node_id", default="")
    c.add_argument("--root", default=None)
    c.add_argument("--set", dest="sets", action="append", default=[],
                   metavar="K=V", help="extra frontmatter, e.g. goal_kind=subgoal")
    c.add_argument("--no-spawn-gate", action="store_true")
    c.add_argument("--season-parent", dest="season_parents",
                   action="append", default=[])
    c.add_argument("--current-season", type=int, default=None,
                   help="override the ladder's current_season")
    r = sub.add_parser("rules")
    r.add_argument("--root", default=None)
    args = ap.parse_args(argv)

    root = Path(args.root).resolve() if args.root else _find_root()
    rules, index, cs = gate_for_root(root)
    announce_schema_errors(rules)

    if args.cmd == "rules":
        print(f"geometry: {rules.geometry.source}")
        print(f"  parentless_types: {sorted(rules.geometry.parentless_types)}")
        print(f"  max_parents_ceiling: {rules.geometry.max_parents_ceiling}")
        for name in sorted(rules.schemas):
            s = rules.schemas[name]
            if s.error:
                print(f"{name:16} ERROR {s.error}")
            elif s.discriminator:
                print(f"{name:16} discriminator={s.discriminator} "
                      f"({s.source})")
                for v, rl in sorted(s.variants.items()):
                    print(f"  {v:14} min={rl.min_parents} max={rl.max_parents} "
                          f"allowed={sorted(rl.allowed_parents)}")
            elif s.flat:
                print(f"{name:16} min={s.flat.min_parents} "
                      f"max={s.flat.max_parents} "
                      f"allowed={sorted(s.flat.allowed_parents)} ({s.source})")
            else:
                print(f"{name:16} (no spawn: block — unverified)")
        return 0

    fm = {}
    for kv in args.sets:
        if "=" in kv:
            k, v = kv.split("=", 1)
            fm[k.strip()] = v.strip()
    res = check_spawn(
        args.node_type, args.parents, rules=rules, type_index=index, fm=fm,
        node_id=args.node_id, bypass=args.no_spawn_gate,
        season_parents=args.season_parents,
        current_season=args.current_season if args.current_season is not None else cs,
    )
    announce(res)
    return 2 if res.status == REJECTED else 0


def _find_root() -> Path:
    """The graph root for cwd, via the one shared resolver (goal:g11.1)."""
    root = locations.find_project_root()
    if root is None:
        print("ERR: no agi project found from cwd up", file=sys.stderr)
        raise SystemExit(1)
    return root


if __name__ == "__main__":
    sys.exit(_cli(sys.argv[1:]))
