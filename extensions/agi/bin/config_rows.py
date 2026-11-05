"""config_rows -- the narrow writer of config:posts / config:seats rows (goal:g7.16.1.11.46.23, V8a tip 2b).

Replaces the six call shapes that went through `write.submit` (see
doc:v8a-submit-guard-census section 1): a keygen's own row, `--all-live` keygen,
a spawn-mint's new row, a countersign promotion, a seat's session cells, and the
migrate tick's seating cells.

THE SITE DECLARES, THE HELPER CHECKS. A caller names what it means to write:
``declare = {row_name: (op, keys)}`` with op in {"set", "create"} and ``keys`` the
only cells it may change (None = any, for a create). The old-to-new row diff must
equal the declaration EXACTLY: a keygen that also touches another row, or a
countersign that also changes `model`, is refused before anything is written.

THEN THE ACTOR IS ADMITTED BY SCHEMA DATA (``.agi/context/schemas/[config].md``),
never by a literal name or role here:
  (W) the role the actor's OWN posts row holds is in the schema's `written_by`
      (the literal actor `owner` is role owner);
  (S) a `set` of the actor's own row whose changed keys are all in `self_row.fields`
      and none in SELF_ROW_PROTECTED;
  (A) an `actor_rows` entry whose `actor` is the actor's seat, for this list, with the
      op in `ops`, the row not in `deny_roles`, and every changed key in `fields`.
A caller-passed role is never read, so it cannot be forged up. An unresolved actor
is refused. A graph with NO config schema declares no writers and gates nothing (as the old
gate read it); the declared diff still binds. Nothing but the row list is written.

What this module deliberately does NOT carry (doc:v8a-submit-guard-census, rows C8
and C9, dropped here and replaced by R-land at every trunk move): the rung-3 veto
freeze and the town vocabulary. The write goes through `node_writer.update_node`.
"""
from __future__ import annotations

import os
from pathlib import Path

import geometry_config
import links
import locations
import node_writer

#: cells a seat's own-row write may never carry, whatever `self_row.fields` says
#: (the L4.110 ruling B list, as the old gate held it).
SELF_ROW_PROTECTED = frozenset({
    "role", "model", "tier", "harness", "effort", "owning_goal", "worktree", "rotated_by",
})

#: the cells a keygen writes into a row (send.py's own-row and --all-live shapes)
KEYGEN_KEYS = frozenset({"pubkey", "sig_scheme", "enc_scheme", "key_history"})

PROVENANCE_ACTOR = "edited_by"
PROVENANCE_SESSION = "thought_session"


class RowWriteRefused(ValueError):
    """The write was refused by name; nothing was written."""


def _config_schema(root: Path):
    """The config schema's frontmatter, or None when this graph carries NO config schema
    (no schemas dir, or no `config` entry): a type with no schema declares no writers, so it
    gates nothing, exactly as the old gate read it; the site's declared diff still binds. A
    schema that EXISTS but cannot be read refuses (never a pass on unreadable bytes)."""
    sdir = Path(root) / "context" / "schemas"
    if not sdir.is_dir():
        return None
    try:
        from schema_registry import load_schemas_from_dir
        schema = load_schemas_from_dir(sdir).get("config")
    except Exception as exc:  # noqa: BLE001
        raise RowWriteRefused(f"cannot read the config schema ({exc})") from exc
    return None if schema is None else (schema.frontmatter or {})


def _resolve_seat(rows: list, actor: str):
    """The NAME of the posts row the actor resolves to: the exact name, or the longest
    `<name>-...` prefix (a generation-suffixed actor); a tie at the longest refuses."""
    if not actor:
        return None
    hits = [(len(str(r["name"])), str(r["name"])) for r in rows
            if r.get("name") and r.get("role")
            and (actor == r["name"] or actor.startswith(str(r["name"]) + "-"))]
    if not hits:
        return None
    longest = max(h[0] for h in hits)
    top = sorted({h[1] for h in hits if h[0] == longest})
    if len(top) > 1:
        raise RowWriteRefused(
            f"ambiguous seat prefix: {', '.join(top)} tie at the longest match for actor {actor!r}")
    return top[0]


def _diff(old: list, new: list) -> dict:
    """{name: (op, changed_keys)} for every row that differs; op in create/set/retire."""
    o = {r.get("name"): r for r in old if isinstance(r, dict)}
    n = {r.get("name"): r for r in new if isinstance(r, dict)}
    out = {}
    for name in list(o) + [x for x in n if x not in o]:
        a, b = o.get(name), n.get(name)
        if a == b:
            continue
        if a is None:
            out[name] = ("create", set(b) - {"name"})
        elif b is None:
            out[name] = ("retire", set(a) - {"name"})
        else:
            out[name] = ("set", {k for k in set(a) | set(b) if a.get(k) != b.get(k)})
    return out


def _check_shape(old: list, new: list) -> None:
    if not isinstance(new, list) or not all(isinstance(r, dict) for r in new):
        raise RowWriteRefused("the row list must be a list of rows (dicts)")
    names = [r.get("name") for r in new]
    if any(not isinstance(x, str) or not x for x in names):
        raise RowWriteRefused("every row needs a non-empty string `name`")
    if len(set(names)) != len(names):
        raise RowWriteRefused("row names must be unique")


def _check_declared(changes: dict, declare: dict) -> None:
    """The diff must equal what the site declared, exactly."""
    extra = sorted(set(changes) - set(declare))
    if extra:
        raise RowWriteRefused(f"this write changes row(s) {', '.join(map(str, extra))} the caller did not declare")
    for name, (op, keys) in changes.items():
        d_op, d_keys = declare[name]
        if op != d_op:
            raise RowWriteRefused(f"row {name!r}: the caller declared op {d_op!r}, the write is {op!r}")
        if d_keys is not None:
            stray = sorted(keys - set(d_keys))
            if stray:
                raise RowWriteRefused(
                    f"row {name!r}: cell(s) {', '.join(stray)} are outside the {sorted(d_keys)} the caller declared")


def _admit(fm: dict, rows: list, list_key: str, actor: str, name: str, op: str, keys: set) -> None:
    seat = _resolve_seat(rows, actor)
    role = ""
    if seat is not None:
        role = str(next(r for r in rows if r.get("name") == seat).get("role") or "")
    elif actor == "owner":
        role = "owner"
    if not role:
        raise RowWriteRefused(f"actor {actor!r} is UNRESOLVED (no posts row, not owner): nothing admits this write")
    # (W) written_by
    admitted = links.parse_written_by(fm.get("written_by"))
    if admitted and role in admitted:
        return
    # (S) self_row
    sr = fm.get("self_row")
    if (isinstance(sr, dict) and op == "set" and seat == name):
        fields = {str(f) for f in (sr.get("fields") or [])}
        if keys <= fields and not (keys & SELF_ROW_PROTECTED):
            return
    # (A) actor_rows
    for e in (fm.get("actor_rows") or []):
        if not isinstance(e, dict) or str(e.get("actor") or "") != seat:
            continue
        if str(e.get("list_key") or "") not in (list_key, "posts", "seats") or not e.get("match_key"):
            continue
        ops = {str(o) for o in (e.get("ops") or ["set"])}
        deny = {str(d) for d in (e.get("deny_roles") or [])}
        fields = {str(f) for f in (e.get("fields") or [])}
        own_ok = set()
        if seat == name and isinstance(sr, dict):
            own_ok = {str(f) for f in (sr.get("fields") or [])}
        if name in deny or op not in ops:
            continue
        if op == "retire" or keys <= (fields | own_ok):
            return
    raise RowWriteRefused(
        f"row {name!r} ({op}, cells {sorted(keys)}): actor {actor!r} (role {role!r}) is admitted by no "
        f"written_by, self_row or actor_rows entry of the config schema")


def _graph_root(root) -> Path:
    """DESCEND-ONLY, as write._resolve_api_root was: the root itself, or the `.agi/` directly
    beneath it, must carry the project marker; a bare directory refuses rather than resolving
    into some graph above it. Nothing is written for a wrong root."""
    d = Path(root).resolve()
    if locations.config_path(d) is not None:
        return d
    child = d / locations.GRAPH_DIR_NAME
    if locations.config_path(child) is not None:
        return child
    raise RowWriteRefused(f"not an agi project graph root: {str(root)!r} (descend-only; nothing written)")


def write_rows(root, new_rows: list, *, actor: str, declare: dict, session: str = ""):
    """Write the config row list ``new_rows`` (the WHOLE list) if the diff equals
    ``declare`` and the actor is admitted. Returns node_writer's result; raises
    RowWriteRefused (nothing written) otherwise. ``root`` is the graph (.agi) dir."""
    root = _graph_root(root)
    path, list_key = geometry_config.resolve(root)
    if path is None or not Path(path).exists():
        raise RowWriteRefused("no config:posts / config:seats node: neither nodes/.geometry/posts.md "
                              "nor seats.md exists in this graph")
    # ONE resolver: the id node_writer is handed is the RESOLVED file's OWN frontmatter id, never one
    # built from the list key (a file found by NAME with rows but no `id:` is no node: the old path
    # reported success and printed 'wrote identity cells' for a row it never wrote).
    from graph_core.persistence import frontmatter as _fm
    try:
        node_id = (_fm.load_node_file(Path(path), body=False).frontmatter or {}).get("id")
    except Exception as exc:  # noqa: BLE001
        raise RowWriteRefused(f"config_rows: {path} cannot be read ({exc})") from exc
    if node_id not in ("config:posts", "config:seats"):
        raise RowWriteRefused(f"config_rows: {path} carries id {node_id or 'none'}, not config:posts|seats "
                              "(nothing written)")
    old = geometry_config.load_rows(root)
    _check_shape(old, new_rows)
    changes = _diff(old, new_rows)
    _check_declared(changes, declare)
    fm = _config_schema(root) if changes else None
    if fm is not None:
        for name, (op, keys) in changes.items():
            _admit(fm, old, list_key, actor, name, op, keys)
    set_fm = {list_key: new_rows, PROVENANCE_ACTOR: actor}
    if session:
        set_fm[PROVENANCE_SESSION] = session
    prov = {"actor": actor}
    if os.environ.get("AGI_ROLE"):
        prov["role"] = os.environ["AGI_ROLE"].strip()
    seat = geometry_config.resolved_seat_env()
    if seat:
        prov["seat"] = seat.strip()
    res = node_writer.update_node(root, node_id, set_fm=set_fm, log_extra=prov)
    if res.status == node_writer.REJECTED:
        raise RowWriteRefused(f"node_writer rejected the write: {res.reason}")
    return res


def _main(argv=None) -> int:
    """CLI front door: `--help` prints what this module is. There is nothing to run from a
    shell (a writer needs a site's declared diff); this keeps the bin/ smoke lane, which runs
    every script with --help expecting non-empty stdout and exit 0, honest."""
    import argparse

    ap = argparse.ArgumentParser(
        prog="config_rows.py",
        description=("The narrow writer of config:posts / config:seats rows "
                     "(goal:g7.16.1.11.46.23 V8a): import config_rows and call "
                     "write_rows(root, new_rows, actor=, declare={row: (op, keys)}). "
                     "The site declares what it writes; the schema's written_by / self_row / "
                     "actor_rows data admits the actor. Nothing is run from this CLI."))
    ap.parse_args(argv)
    ap.print_help()
    return 0


if __name__ == "__main__":
    import sys

    sys.exit(_main())
