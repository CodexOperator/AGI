#!/usr/bin/env python3
"""write.py — named node operations, drivable by a human or by an agent.

**Renamed from `edit.py` on 2026-09-03, at the owner's call**, because "edit"
named half of what this is: a verb here either revises an existing node or
mints a new one, and both are *writes*. The old name would have made `create`
read as an exception to the module it lives in. The link layer that used to
hold this filename is now `links.py`, which is what it always was — `link_ref`
resolution and the `broken_links` count, not the write path.

`goal:g13.1`. A hand edit to a node is currently an **undeclared write**: it
bypasses `node_writer`, the `scaffold_hash` stamp, the evidence gate and schema
validation, and nothing records that a human changed the node or why. The
owner's framing — *"a completely stray and untraceable commit from my end"*.

This module is the **verb layer**, and it is deliberately built before the
modal shell rather than inside it.

## Why the verbs come first

The goal's design has two callers and insists they are the same operations:

- **For a human**, a modal shell binds keys to verbs, re-renders, and submits.
- **For an LLM**, the whole session serialises into one `&&`-joined command.
  That is not a lesser path — it is *the same operations with the interaction
  removed*.

**A keystroke an agent cannot spell is a verb that exists only for humans**,
which splits the write path exactly as `goal:g9.7` forbids splitting the read
path. So the nameable set is the thing with a right and a wrong answer, and
the shell is skin over it. Building the shell first would have produced verbs
shaped by keybindings.

## It writes nothing itself

Every verb ends in `node_writer.update_node`. **There is no file write in this
module**, asserted by a test that parses it rather than greps it — the same
invariant `viewport.py` holds on the read side, and the same lesson from this
session that a `grep` for a concept cannot tell prose from code.

If a change can be made here that `write.py` cannot make, edit mode has become
a bypass rather than a front end, which is the stray untraceable write it was
built to eliminate.

## Provenance is the payoff

An edit records **who** and **why**: `edited_by` and `thought_session`, the
latter reserved in frontmatter since `goal:g2.7`/`goal:g10.1` with nothing
writing it until now. An edit mode that produces an untraceable change has
delivered the convenience and none of the reason.
"""
from __future__ import annotations

import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
import locations  # noqa: E402
import node_writer  # noqa: E402
import links  # noqa: E402

#: Frontmatter keys this module stamps on every submitted edit.
PROVENANCE_ACTOR = "edited_by"
PROVENANCE_SESSION = "thought_session"

#: Keys no verb may touch, whatever a caller asks. `id` and `mint_id` are
#: identity (`goal:g2.5`: a mint id is assigned once and never changes), and
#: `scaffold_hash` is how completion is detected — the exact field the kid
#: brief forbids touching, and edit mode is not a loophole in that rule.
PROTECTED = frozenset({"id", "mint_id", "type", "scaffold_hash"})

#: The one heading body notes live under. Shared with `post_wire` and
#: `cli.py done`, which both already write it -- a second spelling here would
#: be the duplicate-heading defect this constant exists to prevent.
NOTES_HEADING = "## Agent Notes"


class EditError(RuntimeError):
    """A verb was asked for that cannot be performed."""


@dataclass
class Edit:
    """One accumulated, unsubmitted change to a node.

    Verbs mutate this; **`submit` is the only thing that writes**. That split
    is what makes the modal shell and the `&&`-serialised form the same
    operations: both accumulate, both submit once.
    """

    node_id: str
    set_fm: dict = field(default_factory=dict)
    unset_fm: list = field(default_factory=list)
    body_append: str = ""
    thought: str = ""
    payload_from: str = ""
    payload_bytes: str = ""

    @property
    def empty(self) -> bool:
        return not (self.set_fm or self.unset_fm or self.body_append
                    or self.thought or self.payload_from
                    or self.payload_bytes)


# --------------------------------------------------------------------------
# The verbs. Each is nameable, each takes strings, each is spellable by an
# agent on a command line. That is the constraint, not a coincidence.
# --------------------------------------------------------------------------

def verb_set(edit: Edit, key: str, value: str) -> Edit:
    """`set <key> <value>` — one frontmatter field."""
    if key in PROTECTED:
        raise EditError(
            f"{key!r} is identity or completion state and no verb may set it. "
            f"A mint id is assigned once (goal:g2.5); scaffold_hash is how "
            f"completion is detected, and edit mode is not a loophole in the "
            f"rule the kid brief already follows.")
    edit.set_fm[key] = _coerce(value)
    return edit


def verb_unset(edit: Edit, key: str) -> Edit:
    """`unset <key>` — drop a frontmatter field."""
    if key in PROTECTED:
        raise EditError(f"{key!r} may not be unset — see `set`.")
    edit.unset_fm.append(key)
    return edit


def verb_link(edit: Edit, ref: str) -> Edit:
    """`link <ref|self>` — declare what this node's body points at.

    `goal:g13`'s field, reached through the same accumulate-then-submit path
    as everything else rather than through `links.set_link`, so a linked edit
    and a field edit submit as one operation instead of two.
    """
    edit.set_fm[links.LINK_FIELD] = ref
    return edit


def verb_thought(edit: Edit, text: str) -> Edit:
    """`thought <text>` — rewrite the authored region.

    Rewritten from scratch, never appended to: the thought says why THIS
    version differs from the previous one (`goal:g2.11`). **Absent means
    empty** — a caller that passes nothing leaves the existing thought alone
    rather than clearing it, because a fabricated or destroyed thought reads
    as evidence either way.
    """
    edit.thought = text
    return edit


def verb_note(edit: Edit, text: str) -> Edit:
    """`note <text>` — append to the body under `## Agent Notes`.

    The one body operation. Dropping to `$EDITOR` for prose is legitimate and
    is the shell's job; hand-editing frontmatter is the thing being replaced.
    """
    edit.body_append = text
    return edit


def verb_payload_text(edit: Edit, text: str) -> Edit:
    """`payload_text <content>` — the payload's new bytes, inline.

    The same move `note` makes for a body: say the content, do not stage it.
    `payload <path>` still exists and is the right verb when the bytes already
    exist as a file or are large; this one removes the scratch-file step for
    everything else.

    One newline is ensured at the end, because a text payload without one is a
    diff that reports a change on the last line forever.

    **Caveat, stated rather than hidden:** the script form splits on `&&`, so
    content containing `&&` must come through `payload <path>` or stdin
    (`payload -`). The Python API has no such limit.
    """
    edit.payload_bytes = text if text.endswith("\n") else text + "\n"
    return edit


def verb_payload(edit: Edit, source: str) -> Edit:
    """`payload <path>` — replace the bytes of the file this node points at.

    The last node operation that had no name. A build node's payload — a
    `.py`, a `.sh`, `SKILL.md`, `HANDOFF.md` — was edited with whatever editor
    was to hand, and the node behind it learned nothing: no `edited_by`, no
    `thought_session`, no single submit tying the bytes to the reason for
    them. Compose the new content wherever you like, then hand the file over
    here and it lands with the rest of the edit (`goal:g13.1`).

    The write itself is `node_writer.replace_payload` — this module still
    performs no file write, which is the invariant that keeps the verb layer a
    front end rather than a second way in.
    """
    edit.payload_from = source
    return edit


VERBS = {
    "set": verb_set,
    "unset": verb_unset,
    "link": verb_link,
    "thought": verb_thought,
    "note": verb_note,
    "payload": verb_payload,
    "payload_text": verb_payload_text,
}

#: How many arguments each verb takes. The LAST one always absorbs the rest of
#: the chunk, because prose verbs (`thought`, `note`) take a sentence and a
#: sentence contains spaces.
#:
#: Found by dogfooding, immediately: `parse_script` originally split every
#: chunk with `maxsplit=2`, which is right for `set k v` and wrong for
#: everything else -- `note some prose here` arrived as three arguments to a
#: two-argument verb and errored. A fixed split is a parser that assumes every
#: verb has the same shape.
ARITY = {"set": 2, "unset": 1, "link": 1, "thought": 1, "note": 1,
         "payload": 1, "payload_text": 1}


def _coerce(value: str):
    """`"3"` -> 3, `"true"` -> True, `"[a, b]"` -> list. Strings otherwise.

    A command line hands over strings; frontmatter is typed, and a schema's
    `types:` block will reject `confidence: "0.9"`. Coercion belongs here
    rather than in every caller.
    """
    if not isinstance(value, str):
        return value
    text = value.strip()
    low = text.lower()
    if low in {"true", "false"}:
        return low == "true"
    if low in {"none", "null"}:
        return None
    if text.startswith("[") and text.endswith("]"):
        inner = text[1:-1].strip()
        return [_coerce(p.strip()) for p in inner.split(",")] if inner else []
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        return text


def apply_verb(edit: Edit, name: str, args: list[str]) -> Edit:
    """Run one named verb. The single entry both callers reach."""
    fn = VERBS.get(name)
    if fn is None:
        raise EditError(f"no verb {name!r}. Known: {', '.join(sorted(VERBS))}")
    try:
        return fn(edit, *args)
    except TypeError as exc:
        raise EditError(f"{name}: wrong arguments ({exc})") from exc


def parse_script(text: str) -> list[tuple[str, list[str]]]:
    """`"set status active && link self"` -> a list of verb calls.

    The `&&`-serialised form the owner described: an agent's whole edit
    session as one command. Separated on `&&` and never handed to a shell —
    the string is data here, exactly as `commands.py` keeps argv a list.
    """
    out: list[tuple[str, list[str]]] = []
    for chunk in str(text).split("&&"):
        stripped = chunk.strip()
        if not stripped:
            continue
        name = stripped.split(None, 1)[0]
        # Split by the verb's OWN arity, so the last argument absorbs the rest
        # of the chunk. `set k v` takes two; `note <a whole sentence>` takes
        # one that happens to contain spaces.
        rest = stripped[len(name):].strip()
        arity = ARITY.get(name, 1)
        args = rest.split(None, arity - 1) if rest else []
        out.append((name, args))
    return out


def submit(root, edit: Edit, actor: str = "", session: str = "") -> object:
    """Write the accumulated edit. **The only thing in this module that writes.**

    Returns `node_writer`'s own result object, so a caller sees `UPDATED`,
    `UNCHANGED` or `REJECTED` and the reason — the same statuses every other
    writer path reports.
    """
    if edit.empty:
        raise EditError(f"nothing to submit for {edit.node_id}")

    set_fm = dict(edit.set_fm)
    set_fm[PROVENANCE_ACTOR] = actor or _default_actor()
    if session:
        set_fm[PROVENANCE_SESSION] = session

    body = None
    if edit.body_append or edit.thought:
        body = _compose_body(root, edit)

    # Everything that can refuse, refuses BEFORE anything is written: a
    # payload swap that lands next to a rejected node edit is a file whose
    # reason never made it into the graph, which is the exact split this verb
    # exists to close.
    touches_payload = bool(edit.payload_from or edit.payload_bytes)
    payload_ref, location = _payload_ref(root, edit) if touches_payload else ("", None)
    # A `location` set in this same edit wins over the one on disk: naming the
    # new base and moving the bytes is one intention, not two.
    if "location" in set_fm:
        location = set_fm["location"]

    res = node_writer.update_node(root, edit.node_id, set_fm=set_fm,
                                  unset_fm=edit.unset_fm, body=body)
    if payload_ref and res.status != node_writer.REJECTED:
        dest, changed = node_writer.replace_payload(
            root, payload_ref, edit.payload_from or None,
            location=location,
            data=edit.payload_bytes.encode() if edit.payload_bytes else None)
        res.payload_changed = changed
        res.payload_path = str(dest)
    return res


def _payload_ref(root, edit: Edit) -> tuple[str, str | None]:
    """Where this node's bytes live, or an error naming why there are none.

    Read off the node rather than passed in, because `payload_ref` is the
    node's own statement about which file it is; a caller that supplied the
    path could point the verb at a file the node has never claimed.
    """
    from graph_core.persistence import frontmatter as fm_reader

    path = node_writer.find_node_file(root, edit.node_id)
    if path is None:
        raise EditError(f"no node file for {edit.node_id}")
    fm = fm_reader.load_node_file(path, body=False).frontmatter
    ref = fm.get("payload_ref") or fm.get(links.LINK_FIELD)
    if not isinstance(ref, str) or not ref.strip():
        raise EditError(
            f"{edit.node_id} has no payload_ref, so there are no bytes to "
            f"replace. `payload` edits the file a build node points at; a "
            f"node without one is edited with `set`, `note` and `thought`.")
    loc = fm.get("location")
    return ref.strip(), loc.strip() if isinstance(loc, str) and loc.strip() else None


def _default_actor() -> str:
    return os.environ.get("AGI_ACTOR") or os.environ.get("USER") or "unknown"


def _compose_body(root, edit: Edit) -> str:
    """The node's body with the note appended and the thought replaced.

    Read through the canonical reader, not by splitting on `---`. This module
    exists because hand-rolled node surgery is the problem.
    """
    from graph_core.persistence import frontmatter as fm_reader

    path = node_writer.find_node_file(root, edit.node_id)
    if path is None:
        raise EditError(f"no node file for {edit.node_id}")
    body = fm_reader.load_node_file(path).body

    if edit.body_append and edit.body_append.strip() not in body:
        # Append UNDER an existing heading rather than adding a second one.
        # The first version checked only whether the text was already present,
        # so a node that `post_wire` had already given a `## Agent Notes`
        # section got a second heading -- found on the first real use, against
        # a live node that had one.
        note = edit.body_append.rstrip()
        if NOTES_HEADING in body:
            head, sep, tail = body.rpartition(NOTES_HEADING)
            body = head + sep + tail.rstrip() + f"\n\n{note}\n"
        else:
            body = body.rstrip() + f"\n\n{NOTES_HEADING}\n{note}\n"

    if edit.thought:
        block = (node_writer._THOUGHT_RE.pattern and
                 "<!-- THOUGHT:BEGIN — authored, not derived; carried across "
                 "regenerating scans. The reasoning behind THIS version. -->\n"
                 f"{edit.thought}\n<!-- THOUGHT:END -->")
        existing = node_writer.extract_thought(body)
        if existing:
            body = body.replace(existing, block)
        else:
            body = body.rstrip() + "\n\n" + block + "\n"
    return body


def create(root, node_type: str, slug: str, parents: list[str], *,
           set_fm: dict | None = None, payload: str | None = None,
           actor: str = "", session: str = "", bypass: bool = False):
    """Mint a node — and, for a build node, the file it points at.

    **This is `write.py`'s other half, and its absence was the hole that made
    the rename honest** (`goal:g13.1`, L1.07). The verb layer could revise any
    node and mint none, so a director needing a standalone or build node still
    hand-wrote a file: the exact undeclared write the module exists to end.
    `dispatch.py` had a creation path via `cli.py scaffold`, but that one is
    wired to an agent's `agent.json` bookkeeping and is not usable by a human.

    **It reuses `node_writer.write_node` rather than reimplementing it.** That
    routine runs the spawn gate *before* touching the filesystem, mints the
    `mint_id`, and canonicalises the type. A second creation path that skipped
    any of those would be a bypass wearing the name of a front end — the same
    thing `submit` refuses to be on the update side.

    `payload` creates the source file if it is absent and records it as
    `link_ref`, so "a new node and, if needed, the code file behind it" is one
    operation. An existing file is **never overwritten** — it is linked.
    """
    extra = dict(set_fm or {})
    created_file = None
    if payload:
        # Delegated, not done here: this module's guard is that it performs no
        # file write at all, and `node_writer` already owns writing the files
        # behind nodes. See `node_writer.ensure_payload`.
        extra.setdefault("location", locations.DEFAULT_PAYLOAD_LOCATION)
        created_file = node_writer.ensure_payload(
            root, payload, extra.get("location"))
        extra[links.LINK_FIELD] = str(payload)

    res = node_writer.write_node(root, node_type, slug, parents,
                                 extra_fm=extra or None, bypass=bypass)
    if res.rejected or not res.written:
        if created_file is not None:
            # A rejected spawn must leave nothing behind, on either side.
            # `write_node` already guarantees that for the node; the file is
            # this function's to clean up, and forgetting would leave an empty
            # source file with no node behind it — precisely the gitignored
            # staging window `goal:g11` removed.
            created_file.unlink(missing_ok=True)
        return res, None

    # Provenance goes on through the same routine every other edit uses, so a
    # created node is not a node with a weaker record than an edited one.
    if actor or session:
        stamp = Edit(node_id=res.node_id)
        if actor:
            stamp.set_fm[PROVENANCE_ACTOR] = actor
        if session:
            stamp.set_fm[PROVENANCE_SESSION] = session
        node_writer.update_node(root, res.node_id, set_fm=stamp.set_fm)
    return res, created_file


def main(argv: list[str] | None = None) -> int:
    """`write.py <node-id> "set k v && link self && thought why"`

    or `write.py create <type> <slug> --parent <id> [--payload PATH]`.
    """
    import argparse

    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("node_id",
                    help='a node id, or "create" to mint one')
    ap.add_argument("script", nargs="?", default=None,
                    help='verbs joined by "&&"; with `create`, the node type')
    ap.add_argument("slug", nargs="?", default=None,
                    help="with `create`: the new node's slug")
    ap.add_argument("--parent", dest="parents", action="append", default=[],
                    help="with `create`: repeatable; the SCHEMA decides how "
                         "many are legal, not argparse")
    ap.add_argument("--payload", default=None,
                    help="with `create`: source file to link, created if absent")
    ap.add_argument("--set", dest="sets", action="append", default=[],
                    help="with `create`: extra frontmatter, k=v, repeatable")
    ap.add_argument("--no-spawn-gate", action="store_true",
                    help="bypass the spawn gate, loudly")
    ap.add_argument("--root", default=".", help="any path inside the project")
    ap.add_argument("--actor", default="", help="who is making this edit")
    ap.add_argument("--session", default="",
                    help="the session that produced it (thought_session)")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the accumulated edit and write nothing")
    args = ap.parse_args(argv)

    if args.node_id == "create":
        root = locations.find_project_root(Path(args.root).resolve())
        if root is None:
            print(f"ERR: not an agi project: {args.root}", file=sys.stderr)
            return 1
        if not args.script or not args.slug:
            print("ERR: create needs a type and a slug: "
                  'write.py create <type> <slug> --parent <id>', file=sys.stderr)
            return 2
        set_fm = {}
        for pair in args.sets:
            if "=" not in pair:
                print(f"ERR: --set expects k=v, got {pair!r}", file=sys.stderr)
                return 2
            k, v = pair.split("=", 1)
            set_fm[k.strip()] = _coerce(v.strip())
        if args.dry_run:
            print(f"create {args.script}:{args.slug}")
            print(f"  parents  {args.parents or '(none)'}")
            if args.payload:
                print(f"  payload  {args.payload}")
            for k, v in set_fm.items():
                print(f"  set      {k} = {v!r}")
            return 0
        res, made = create(root, args.script, args.slug, args.parents,
                           set_fm=set_fm, payload=args.payload,
                           actor=args.actor, session=args.session,
                           bypass=args.no_spawn_gate)
        if res.rejected:
            print(f"ERR: spawn rejected for {res.node_id}: {res.reason}. "
                  f"Fix: {res.gate.fix} (--no-spawn-gate bypasses this, loudly.)",
                  file=sys.stderr)
            return 2
        if not res.written:
            print(f"SKIP: {res.path} already exists", file=sys.stderr)
            return 0
        print(f"created: {res.node_id} -> {res.path}")
        if made is not None:
            print(f"created: {made} (empty; the node points at it)")
        return 0

    if not args.script:
        print("ERR: a script is required: "
              'write.py <node-id> "set k v && thought why"', file=sys.stderr)
        return 2

    root = locations.find_project_root(Path(args.root).resolve())
    if root is None:
        print(f"ERR: not an agi project: {args.root}", file=sys.stderr)
        return 1

    edit = Edit(node_id=args.node_id)
    try:
        for name, verb_args in parse_script(args.script):
            apply_verb(edit, name, verb_args)
    except EditError as exc:
        print(f"ERR: {exc}", file=sys.stderr)
        return 2

    if args.dry_run:
        print(f"{edit.node_id}:")
        for k, v in edit.set_fm.items():
            print(f"  set    {k} = {v!r}")
        for k in edit.unset_fm:
            print(f"  unset  {k}")
        if edit.thought:
            print(f"  thought ({len(edit.thought)} chars)")
        if edit.body_append:
            print(f"  note    ({len(edit.body_append)} chars)")
        if edit.payload_from:
            print(f"  payload from {edit.payload_from}")
        if edit.payload_bytes:
            print(f"  payload  ({len(edit.payload_bytes)} bytes, inline)")
        return 0

    if edit.payload_from == "-":
        # The CLI layer reads stdin; the library never does. `payload -` is
        # for content that cannot ride in an argv chunk -- anything with `&&`
        # in it, or a whole file being piped in.
        edit.payload_from = ""
        edit.payload_bytes = sys.stdin.read()

    try:
        res = submit(root, edit, actor=args.actor, session=args.session)
    except (EditError, FileNotFoundError) as exc:
        print(f"ERR: {exc}", file=sys.stderr)
        return 2
    print(f"{res.status}: {edit.node_id}"
          + (f" — {res.reason}" if res.reason else ""))
    if res.payload_changed is not None:
        print(f"payload: {res.payload_path} "
              + ("replaced" if res.payload_changed else "unchanged"))
    return 1 if res.status == node_writer.REJECTED else 0


if __name__ == "__main__":
    raise SystemExit(main())
