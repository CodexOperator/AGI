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
import re
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
    # hypothesis:l3-write-partial-diffs-as-writes -- `patch` lands a unified
    # diff (the grid's own delta vocabulary) as the new payload bytes,
    # instead of re-emitting the whole file. `patch_from` names the source
    # (`-` for stdin, or a path); `patch_diff` holds the bytes once read.
    # This module still performs no file write: the diff is applied in memory
    # by `apply_unified_diff` and the resulting bytes flow through the same
    # `replace_payload` the whole-file verbs use, so edited_by,
    # thought_session, the write guard and the grid version all still happen.
    patch_from: str = ""
    patch_diff: str = ""
    # hypothesis:l3w4-hierarchy-one-source, body leg -- `body_patch` is
    # `patch` for a graph node's BODY. `patch` targets a build node's payload
    # file and REFUSES a graph node (no payload_ref), so a stale pipe table
    # in a node body could not be removed as a sanctioned write -- the
    # standing unsanctioned-write failure class that deferred the one-source
    # deletion for three rounds. `body_patch` reuses the same fail-closed
    # unified diff against the body text and lands through `update_node`, so
    # the THOUGHT region is carried, provenance is stamped, and write_guard
    # sees a sanctioned write. `body_patch_from` names the source (`-` for
    # stdin, or a path); `body_patch_diff` holds the bytes once read.
    body_patch_from: str = ""
    body_patch_diff: str = ""
    # hypothesis:l3-write-partial-diffs-as-writes, build item 1 — `read` is
    # the read half of the line-addressing: fetch a line RANGE of the node
    # body or of the payload, cheaply, instead of loading the whole file.
    # Read-only — this verb never writes and is handled as a terminal verb in
    # main (it short-circuits before submit), so it carries no provenance
    # stamp of its own. `read_target` is `payload` or `body`; `read_range` is
    # the 1-based inclusive `START:END` with either side optional.
    read_target: str = ""
    read_range: str = ""
    # L4, owner 2026-09-09 — `replace` is the OFFSET-FREE partial write, and
    # the reason it exists: `read <t> N:M` then `<t>_patch` forced the caller
    # to hand-build a `@@` hunk in the applier's coordinates, and getting that
    # arithmetic wrong is a silent corruption (trap 0ah). `replace` takes the
    # SAME `N:M` the read just used, so the round trip needs no arithmetic at
    # all. `replace_target` is `payload` or `body` and both go through ONE
    # reader (`_target_text`) and ONE transform (`_splice_range`), so a
    # payload file is editable by exactly the routine a node body is.
    replace_target: str = ""
    replace_range: str = ""
    replace_from: str = ""
    replace_text: str = ""
    # hypothesis:l3-node-without-mint-id -- `adopt` mints a first mint_id on
    # a node written outside node_writer. Deliberately NOT a `set_fm` entry:
    # `mint_id` is PROTECTED (goal:g2.5), and adopting is not setting it, it
    # is Minting it through node_writer.repair_mint, which refuses an already-
    # minted id. This flag is what lets main route it there rather than into
    # the ordinary submit -> update_node path (which would refuse it).
    adopt: bool = False

    @property
    def empty(self) -> bool:
        return not (self.set_fm or self.unset_fm or self.body_append
                    or self.thought or self.payload_from
                    or self.payload_bytes or self.adopt
                    or self.patch_from or self.patch_diff
                    or self.body_patch_from or self.body_patch_diff
                    or self.read_target or self.read_range
                    or self.replace_target)


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


def verb_body_patch(edit: Edit, source: str) -> Edit:
    """`body_patch <path|->` — apply a unified diff to the node's BODY, in place.

    The missing half of the delete-duplicates leg of
    hypothesis:l3w4-hierarchy-one-source: `patch` covers the payload file
    behind a build node and REFUSES a graph node (no payload_ref), so a stale
    pipe table in a node body could not be removed as a sanctioned write — the
    standing unsanctioned-write failure class that deferred the one-source
    deletion for three rounds. `body_patch` reuses the same fail-closed
    unified-diff vocabulary (`apply_unified_diff`) against the BODY text and
    lands through `update_node`, so the THOUGHT region is carried across,
    provenance is stamped, and write_guard sees a sanctioned write. Diff bytes
    arrive by file path or `-` for stdin, never inline in the `&&` script — a
    diff contains almost any character, including the doubled ampersand that
    splits the script form.
    """
    edit.body_patch_from = source
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


def verb_adopt(edit: Edit, *extra: str) -> Edit:
    """`adopt` — mint a first `mint_id` for a node written outside
    node_writer (a kid's own file tool), so grid.py can version it.

    hypothesis:l3-node-without-mint-id. Refuses when a `mint_id` already
    exists. The one sanctioned exception to the `mint_id` PROTECTION: this
    does not SET the id, it routes through `node_writer.repair_mint`, which
    mints and refuses an already-minted node. Standalone -- it cannot
    meaningfully share a line with other verbs.
    """
    if extra:
        raise EditError(f"adopt takes no arguments, got: {' '.join(extra)}")
    edit.adopt = True
    return edit


def verb_patch(edit: Edit, source: str) -> Edit:
    """`patch <path|->` — apply a unified diff to the payload, in place.

    hypothesis:l3-write-partial-diffs-as-writes. The grid already stores and
    renders exactly this delta (`grid.py diff`), so the diff vocabulary is
    reused rather than inventing a second patch format: a one-line change to
    a large module now costs a one-line diff instead of a whole-file
    re-emission, which is what makes `write.py` affordable for the agents the
    rules require it of.

    The diff bytes arrive by file path or `-` for stdin (copying `payload -`),
    never inline in the `&&` script — a diff contains almost any character,
    including the doubled ampersand that splits the script form. It is
    applied with `apply_unified_diff`, which fails CLOSED: a hunk that does
    not apply to the payload's current bytes refuses the whole write and
    changes nothing on disk, because a half-applied payload patch is this
    loop's single most expensive failure shape. Provenance is unchanged: the
    result lands through the same `replace_payload` the whole-file verbs
    reach, so `edited_by`, `thought_session`, the schema warning and the
    grid version all happen exactly as they do today.
    """
    edit.patch_from = source
    return edit


def verb_read(edit: Edit, target: str, rng: str) -> Edit:
    """`read <payload|body> <START:END>` — fetch a line range, cheaply.

    hypothesis:l3-write-partial-diffs-as-writes, build item 1. The read half
    of line-addressing: a node becomes something you read in pieces, not just
    whole. For a payload the range is streamed so only the requested lines are
    ever materialised — a ranged read of a big module costs a few lines, not
    a whole-file reload. For a body the node's own canonical reader yields it
    and the range is sliced from that.

    The range is 1-based and inclusive, with either side optional: `10:20`
    lines 10..20, `10:` line 10 to the end, `:20` the start to line 20.

    Read-only: this verb never writes and is handled as a terminal verb in
    `main` before `submit` is reached, so no `edited_by` / `thought_session`
    stamp is implied — reading a node must not look like editing it.
    """
    if target not in ("payload", "body"):
        raise EditError(
            f"read target must be 'payload' or 'body', got {target!r}")
    _parse_range(rng)   # validates and raises early, so a typo refuses here
    edit.read_target = target
    edit.read_range = rng
    return edit


def verb_replace(edit: Edit, target: str, rng: str, source: str) -> Edit:
    """`replace <payload|body> <START:END> <path|->` — overwrite a line range.

    The write half of line addressing, and the verb that removes the manual
    offset step. `read <target> N:M` then `replace <target> N:M` is the whole
    round trip: the range vocabulary is identical and `_splice_range` is the
    exact inverse of the `_slice_range` the read used, so nothing has to be
    counted, converted, or expressed as a `@@` hunk.

    `body` and `payload` are the same operation here, not two — one reader
    (`_target_text`), one transform (`_splice_range`) — and they differ only
    in where the result lands, which is forced: a body lands through
    `update_node` (carrying the THOUGHT region and provenance), a payload
    through `replace_payload`. Both are sanctioned writes the guard sees.

    The replacement text rides a file or stdin (`-`) rather than the argv
    chunk, for the reason `payload`/`patch` already do: arbitrary content can
    contain the doubled ampersand the script parser splits on.
    """
    if target not in ("payload", "body"):
        raise EditError(
            f"replace target must be 'payload' or 'body', got {target!r}")
    _parse_range(rng)   # validates and raises early, so a typo refuses here
    edit.replace_target = target
    edit.replace_range = rng
    edit.replace_from = source
    return edit


def _parse_range(rng: str) -> tuple[int | None, int | None]:
    """`10:20` -> (10, 20); `10:` -> (10, None); `:20` -> (None, 20).

    1-based inclusive. At least one bound must be present and the range must
    be non-empty (start <= end when both are given); anything else refuses
    loudly rather than guessing at a slice.
    """
    text = str(rng).strip()
    if ":" not in text:
        raise EditError(f"bad read range {rng!r}: expected START:END "
                        f"(1-based inclusive, either side optional)")
    lo_s, hi_s = text.split(":", 1)

    def _side(s: str) -> int | None:
        s = s.strip()
        if not s:
            return None
        if not s.isdigit():
            raise EditError(f"bad read range {rng!r}")
        return int(s)

    lo, hi = _side(lo_s), _side(hi_s)
    if lo is None and hi is None:
        raise EditError(f"bad read range {rng!r}: need at least one bound")
    if lo is not None and hi is not None and lo > hi:
        raise EditError(f"bad read range {rng!r}: {lo} > {hi}")
    return lo, hi


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
    "patch": verb_patch,
    "body_patch": verb_body_patch,
    "read": verb_read,
    "replace": verb_replace,
    "adopt": verb_adopt,
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
         "payload": 1, "payload_text": 1, "patch": 1, "body_patch": 1,
         "read": 2, "replace": 3, "adopt": 0}


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
        import json
        # hypothesis:l3-write-set-nested-json — a JSON array (e.g. the ladder
        # roles rows, a list of objects) must parse as one nested value. The
        # old comma-split turned `[{"tier": 3, ...}, {...}]` into broken string
        # rows whose inner objects never landed (L3.01). Try the real parse
        # first; the `[a, b]` comma-split is a fallback for the non-JSON
        # spelling and round-trips through the existing renderer unchanged.
        try:
            return json.loads(text)
        except (json.JSONDecodeError, ValueError):
            pass
        inner = text[1:-1].strip()
        return [_coerce(p.strip()) for p in inner.split(",")] if inner else []
    if text.startswith("{") and text.endswith("}"):
        import json
        try:
            return json.loads(text)
        except (json.JSONDecodeError, ValueError):
            pass
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


def _enforce_written_by(root, node_type, actor, where):
    """Refuse a write when the node type's OWN schema declares a restricted
    writer (hypothesis:l4-moral-written-by-carrier).

    The owner-only rule lives as DATA — `written_by:` in the frontmatter of
    `context/schemas/[<type>].md` — read through `schema_registry`, not as a
    hardcoded type literal here. So the rule is carried by the type that owns
    it, and a schema that declares no `written_by` (or whose schema is
    absent) gates nothing: the moral schema's `written_by: owner` is the one
    and only thing that makes moral nodes hand-edit-by-owner-only.

    The compare is EXACTLY `actor not in admitted` — the actor name is what
    is compared, never a role (that is L4.41), and `admitted` is one parse
    shared with `links.py` (`parse_written_by`), so a list-valued or
    comma-separated `written_by` refuses nothing it admits.
    """
    try:
        from schema_registry import load_schemas_from_dir
    except Exception:  # noqa: BLE001
        return
    schemas_dir = Path(root) / "context" / "schemas"
    if not schemas_dir.is_dir():
        return
    try:
        schema = load_schemas_from_dir(schemas_dir).get(node_type)
    except Exception:  # noqa: BLE001
        return
    if schema is None:
        return
    written_by = schema.frontmatter.get("written_by")
    admitted = links.parse_written_by(written_by) if written_by is not None else None
    if admitted and actor not in admitted:
        raise EditError(
            f"{node_type} nodes ({where}) may be hand-edited only by "
            f"{', '.join(sorted(admitted))}. Pass --actor "
            f"{sorted(admitted)[0]} (goal:g12).")


def _resolve_replace_text(edit: Edit) -> None:
    """The ONE resolver that turns `replace_from` into `replace_text`.

    Used by BOTH the CLI (`main`) and the library (`submit`), so an API
    caller and a script form cannot disagree about what a `replace` means —
    the divergence this module shipped
    (hypothesis:l4-replace-api-drops-source). `main` calls it early for its
    `--dry-run` preview; `submit` calls it too, idempotently, so a direct API
    caller gets the same resolution and the same refusals without the read
    being copied into a second place.

    Fail-closed: an absent, unreadable or EMPTY source raises an EditError
    naming the source, and nothing is written anywhere. `replace <t> N:M -`
    keeps its stdin contract: arbitrary content cannot ride an `&&` chunk,
    so it comes off stdin verbatim — exactly as it does today.
    """
    if not edit.replace_from:
        return
    if edit.replace_text:
        # Already resolved — by main() for its --dry-run preview, or by an
        # API caller that set the text directly. Never re-read: a second
        # stdin read for `-` would consume nothing and hang the caller.
        return
    if edit.replace_from == "-":
        # Same stdin contract as `payload -` / `patch -`: replacement text is
        # arbitrary content and cannot ride an `&&` script chunk.
        edit.replace_text = sys.stdin.read()
        return
    try:
        text = Path(edit.replace_from).read_text(encoding="utf-8")
    except OSError as exc:
        raise EditError(
            f"replace source {edit.replace_from!r} unreadable: {exc} — "
            f"nothing written")
    if text == "":
        raise EditError(
            f"replace source {edit.replace_from!r} is empty — refusing to "
            f"replace a range with an empty source (it would delete the "
            f"range). Nothing written. A deliberate deletion needs an "
            f"explicit signal, not an empty file.")
    edit.replace_text = text


def submit(root, edit: Edit, actor: str = "", session: str = "") -> object:
    """Write the accumulated edit. **The only thing in this module that writes.**

    Returns `node_writer`'s own result object, so a caller sees `UPDATED`,
    `UNCHANGED` or `REJECTED` and the reason — the same statuses every other
    writer path reports.
    """
    if edit.empty:
        raise EditError(f"nothing to submit for {edit.node_id}")

    # hypothesis:l4-replace-api-drops-source — the ONE shared resolution of
    # the replacement source. Without this, an API caller's `replace_from`
    # never became `replace_text` and submit spliced `""`, silently deleting
    # the range while reporting success. Idempotent: main has already resolved
    # it for its --dry-run preview, and this must not read stdin a second time.
    _resolve_replace_text(edit)

    _enforce_written_by(root, edit.node_id.split(":", 1)[0], actor, edit.node_id)

    set_fm = dict(edit.set_fm)
    set_fm[PROVENANCE_ACTOR] = actor or _default_actor()
    if session:
        set_fm[PROVENANCE_SESSION] = session

    body = None
    if edit.body_append or edit.thought:
        body = _compose_body(root, edit)
    # hypothesis:l3-partial-write-adoption — the PATH form must read its diff
    # BEFORE the apply-check below, or body_patch_diff is still empty at apply
    # time and the diff is silently discarded (measured 2026-09-09: `body_patch
    # <path>` printed updated: and landed nothing). `patch` does it this way
    # (525-528); body_patch must not differ. The stdin form clears body_patch_from
    # in main() and sets body_patch_diff directly, so this is a no-op there.
    if edit.body_patch_from and not edit.body_patch_diff and edit.body_patch_from != "-":
        from pathlib import Path as _P
        edit.body_patch_diff = _P(edit.body_patch_from).read_text(encoding="utf-8")
    if edit.body_patch_diff:
        # hypothesis:l3w4-hierarchy-one-source — `body_patch` resolves against
        # the node's CURRENT body (not a build-node payload) and lands it
        # through `update_node` below, so the THOUGHT region is carried across
        # and write_guard sees a sanctioned write. Exclusive with note/thought:
        # one body writer per submit keeps a single writer author of the body.
        if edit.body_append or edit.thought:
            raise EditError(
                "body_patch is standalone; it cannot share a line with note "
                "or thought (one body writer per submit)")
        body = apply_unified_diff(_read_body_text(root, edit.node_id),
                                  edit.body_patch_diff)

    # Everything that can refuse, refuses BEFORE anything is written: a
    # payload swap that lands next to a rejected node edit is a file whose
    # reason never made it into the graph, which is the exact split this verb
    # exists to close.
    touches_payload = bool(edit.payload_from or edit.payload_bytes
                           or edit.patch_from or edit.patch_diff
                           or edit.replace_target == "payload")
    payload_ref, location = _payload_ref(root, edit) if touches_payload else ("", None)

    # hypothesis:l3-write-partial-diffs-as-writes -- a `patch` computes the
    # new payload bytes by applying its diff to the payload's CURRENT bytes,
    # fail-closed, in memory. The result is handed to `replace_payload` as
    # `data=` below, so write.py still does not touch the file system. If
    # `apply_unified_diff` refuses, nothing has been written anywhere -- the
    # node update below has not run yet either.
    if edit.patch_diff:
        edit.payload_bytes = apply_unified_diff(
            _read_payload_bytes(root, payload_ref, location),
            edit.patch_diff)
    if edit.patch_from and not edit.patch_diff and edit.patch_from != "-":
        from pathlib import Path as _P
        edit.patch_diff = _P(edit.patch_from).read_text(encoding="utf-8")
        edit.payload_bytes = apply_unified_diff(
            _read_payload_bytes(root, payload_ref, location),
            edit.patch_diff)
    # L4, owner 2026-09-09 — the offset-free partial write, for BOTH targets
    # through one reader and one transform. Everything that can refuse has
    # refused above; `_splice_range` refuses a range past EOF before anything
    # is written, so a bad range leaves the node and the payload untouched.
    if edit.replace_target:
        if edit.replace_target == "body" and (edit.body_append or edit.thought
                                              or edit.body_patch_diff):
            raise EditError(
                "replace body is standalone; it cannot share a line with "
                "note, thought or body_patch (one body writer per submit)")
        _spliced = _splice_range(
            _target_text(root, edit, edit.replace_target,
                         payload_ref, location),
            edit.replace_range, edit.replace_text)
        if edit.replace_target == "body":
            body = _spliced
        else:
            edit.payload_bytes = _spliced

    # A `location` set in this same edit wins over the one on disk: naming the
    # new base and moving the bytes is one intention, not two.
    if "location" in set_fm:
        location = set_fm["location"]

    res = node_writer.update_node(root, edit.node_id, set_fm=set_fm,
                                  unset_fm=edit.unset_fm, body=body,
                                  log_extra=_log_provenance(actor))
    if payload_ref and res.status != node_writer.REJECTED:
        # hypothesis:l3-write-payload-unchanged-unlogged — a same-bytes re-log
        # is still a sanction. Hand the owning node's mint_id to
        # replace_payload so the payload-write log entry carries it, matching
        # write_guard's (mint_id, sha256) key even when the bytes did not
        # change.
        mint = _node_mint_id(root, edit.node_id)
        dest, changed = node_writer.replace_payload(
            root, payload_ref, edit.payload_from or None,
            location=location,
            data=edit.payload_bytes.encode() if edit.payload_bytes else None,
            mint_id=mint,
            log_extra=_log_provenance(actor))
        res.payload_changed = changed
        res.payload_path = str(dest)
    return res


def _node_mint_id(root, node_id: str) -> str:
    """The mint_id of the node an edit targets, for the payload sanction log.

    hypothesis:l3-write-payload-unchanged-unlogged — a payload re-log must
    carry the owning node's mint_id so write_guard's (mint_id, sha256) lookup
    matches the node's frontmatter. Read-only; this module performs no file
    write (test_edit_py_contains_no_file_write).
    """
    from graph_core.persistence import frontmatter as fm_reader
    try:
        path = node_writer.find_node_file(root, node_id)
        if path is None:
            return ""
        return str(fm_reader.load_node_file(path, body=False).frontmatter
                   .get("mint_id", "") or "")
    except BaseException:
        return ""


def _read_payload_bytes(root, ref: str, location: str | None) -> str:
    """The payload's current bytes, as text, resolved the same way the
    whole-file verbs resolve them. Read-only; this module performs no write.
    """
    import locations as _loc
    dest = _loc.resolve_payload_path(Path(root), ref, location)
    if not dest.is_file():
        raise EditError(f"payload {dest} does not exist — nothing to patch.")
    return dest.read_text(encoding="utf-8")


def _slice_range(text: str, rng: str) -> str:
    """The 1-based inclusive line range of a text, ready to print.

    hypothesis:l3-write-partial-diffs-as-writes, build item 1. `10:20` ->
    lines 10..20, `10:` -> 10..end, `:20` -> start..20. `_parse_range` has
    already validated `rng`, so a slice here can only produce the lines the
    shape names. Returns an empty string for a range past EOF.
    """
    lo, hi = _parse_range(rng)
    lines = text.split("\n")
    start = 0 if lo is None else lo - 1
    end = len(lines) if hi is None else hi
    return "\n".join(lines[start:end])


def _splice_range(text: str, rng: str, new: str) -> str:
    """Overwrite the 1-based inclusive line range of `text` with `new`.

    **The exact inverse of `_slice_range`, in the same coordinates.** That is
    the whole point: `read <target> N:M` shows you bytes, and
    `replace <target> N:M` overwrites *those* bytes. No offset is computed by
    the caller, so the class of error trap 0ah names — a hunk built from a
    naive line count that does not match the applier's view — cannot occur.

    `10:20` replaces lines 10..20, `10:` from 10 to the end, `:20` the start
    to line 20. A single trailing newline on `new` is absorbed rather than
    inserting a blank line, so replacing with the text a file/stdin naturally
    carries does not grow the file by one line each time.
    """
    lo, hi = _parse_range(rng)
    lines = text.split("\n")
    start = 0 if lo is None else lo - 1
    end = len(lines) if hi is None else hi
    if start > len(lines):
        raise EditError(
            f"replace range {rng} starts past the end of the target "
            f"({len(lines)} lines) — nothing written.")
    new_lines = new.split("\n")
    if new_lines and new_lines[-1] == "":
        new_lines.pop()
    return "\n".join(lines[:start] + new_lines + lines[end:])


def _read_payload_text(root, ref: str, location: str | None, rng: str) -> str:
    """The requested line range of a build node's payload file, as text.

    Read-only; this module performs no file write and no node write. Only the
    requested lines are ever materialised: the walk starts at the first
    wanted line and stops at the last, so a ranged read of a large module
    costs a few lines, not a whole-file reload.
    """
    import locations as _loc
    dest = _loc.resolve_payload_path(Path(root), ref, location)
    if not dest.is_file():
        raise EditError(f"payload {dest} does not exist — nothing to read.")
    lo, hi = _parse_range(rng)
    start = 1 if lo is None else lo
    wanted: list[str] = []
    with open(dest, "r", encoding="utf-8") as fh:
        for idx, line in enumerate(fh, 1):
            if idx < start:
                continue
            if hi is not None and idx > hi:
                break
            wanted.append(line.rstrip("\n"))
    return "\n".join(wanted)



def _read_body_text(root, node_id: str) -> str:
    """The node body's current text, via the canonical reader. Read-only;
    this module performs no write. `body_patch` resolves its diff against
    this so line numbers are relative to the body, not the whole file.
    """
    from graph_core.persistence import frontmatter as fm_reader
    path = node_writer.find_node_file(root, node_id)
    if path is None:
        raise EditError(f"no node file for {node_id}")
    return fm_reader.load_node_file(path).body


def _target_text(root, edit: "Edit", target: str,
                 payload_ref: str = "", location: str | None = None) -> str:
    """The CURRENT full text of one edit target.

    **The single reader `body` and `payload` both go through**, which is what
    makes a payload file editable by the same routine as a node body rather
    than by a parallel one. Read-only; this module performs no file write.
    """
    if target == "body":
        return _read_body_text(root, edit.node_id)
    return _read_payload_bytes(root, payload_ref, location)


_HUNK_RE = re.compile(
    r"@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@.*")


def apply_unified_diff(original: str, diff: str) -> str:
    """Apply a unified diff to `original`, fail-closed, in memory.

    hypothesis:l3-write-partial-diffs-as-writes. Reads the grid's own diff
    vocabulary (what `git diff` / `difflib.unified_diff` emit): `---`/`+++`
    headers are optional, `@@` hunks carry body lines prefixed with space
    (context), `-` (removed) or `+` (added).

    **No partial application, ever.** Every context line and every removal is
    checked against the payload's current bytes; the first mismatch raises
    `EditError` and nothing is returned, so nothing is written. A hunk whose
    header is malformed, or body bytes that arrive outside any hunk, also
    refuse. The result is a single new string built entirely in memory.
    """
    orig = original.split("\n")
    diff_lines = diff.split("\n")
    if diff_lines and diff_lines[-1] == "":
        diff_lines = diff_lines[:-1]

    # --- Collect the hunks first, so a malformed diff refuses before any
    # state has been touched. ---
    hunks = []
    i, n = 0, len(diff_lines)
    while i < n:
        line = diff_lines[i]
        if line.startswith("@@"):
            m = _HUNK_RE.match(line)
            if not m:
                raise EditError(f"malformed hunk header: {line!r}")
            old_start = int(m.group(1))
            new_start = int(m.group(3))
            i += 1
            body = []
            while i < n and not diff_lines[i].startswith("@@"):
                b = diff_lines[i]
                i += 1
                if not b:
                    body.append((" ", ""))   # a context blank line
                    continue
                if b[0] not in "+- ":
                    raise EditError(f"bytes outside any hunk: {b!r}")
                body.append((b[0], b[1:]))
            hunks.append((old_start, new_start, body))
        else:
            # `---`/`+++` path headers and stray blank separators are
            # tolerated; anything else is malformed.
            if line and not (line.startswith("---") or
                             line.startswith("+++")):
                raise EditError(f"unexpected diff line outside a hunk: {line!r}")
            i += 1

    # --- Apply, fail-closed: every context/removal must match. ---
    out = []
    oi = 0
    for old_start, new_start, body in hunks:
        target = old_start - 1        # 1-based in the diff -> 0-based index
        while oi < target:
            out.append(orig[oi])
            oi += 1
        for action, content in body:
            if action == " ":
                if oi >= len(orig) or orig[oi] != content:
                    got = (repr(orig[oi]) if oi < len(orig) else "<EOF>")
                    raise EditError(
                        f"context mismatch at original line {oi + 1}: "
                        f"diff expects {content!r}, file has {got}")
                out.append(orig[oi])
                oi += 1
            elif action == "-":
                if oi >= len(orig) or orig[oi] != content:
                    got = (repr(orig[oi]) if oi < len(orig) else "<EOF>")
                    raise EditError(
                        f"removal mismatch at original line {oi + 1}: "
                        f"diff expects {content!r}, file has {got}")
                oi += 1
            else:                       # action == "+"
                out.append(content)
    while oi < len(orig):
        out.append(orig[oi])
        oi += 1
    return "\n".join(out)


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


def _log_provenance(actor: str = "") -> dict:
    """The actor/role/seat for a write-log entry, via the `extra` hook.

    hypothesis:l4-write-log-role-capture — every write-log entry should record
    WHO wrote it. `actor` is the resolved caller identity (`actor` param or
    `_default_actor`). `role` and `seat` are READ from what the environment
    already sets (AGI_ROLE / AGI_SEAT, exported by dispatch); when a source is
    absent the key is ABSENT, never a placeholder. Only present keys land in
    the entry — so a hand `write.py submit` with no AGI_ROLE/AGI_SEAT still
    records `actor`, and a non-write.py writer records none of these at all.
    """
    prov: dict = {"actor": actor or _default_actor()}
    role = os.environ.get("AGI_ROLE")
    if role:
        prov["role"] = role.strip()
    seat = os.environ.get("AGI_SEAT")
    if seat:
        prov["seat"] = seat.strip()
    return prov


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
    _enforce_written_by(root, node_type, actor, f"{node_type}:{slug}")

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
                                 extra_fm=extra or None, bypass=bypass,
                                 log_extra=_log_provenance(actor))
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
        node_writer.update_node(root, res.node_id, set_fm=stamp.set_fm,
                                log_extra=_log_provenance(actor))
    return res, created_file


def main(argv: list[str] | None = None) -> int:
    """`write.py <node-id> "set k v && link self && thought why"`
    or `write.py build:bin-x "read payload 10:20"` / `"patch -"` (diff on
    stdin, fail-closed; `body_patch -` for a node body).

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

    # hypothesis:l3-write-partial-diffs-as-writes, build item 1 — `read` is a
    # TERMINAL, read-only verb: render the requested range to stdout and
    # return BEFORE `submit` is reached. This is the branch whose absence let
    # a read fall through the write path and restamp edited_by while printing
    # nothing (measured 2026-09-09). A read that looks like an edit is worse
    # than no read at all, so it cannot share a line with write verbs either.
    if edit.read_target:
        if (edit.set_fm or edit.unset_fm or edit.body_append or edit.thought
                or edit.payload_from or edit.payload_bytes
                or edit.patch_from or edit.patch_diff
                or edit.body_patch_from or edit.body_patch_diff):
            print("ERR: read is a terminal verb; it cannot share a line with "
                  "write verbs", file=sys.stderr)
            return 2
        try:
            if edit.read_target == "payload":
                payload_ref, location = _payload_ref(root, edit)
                text = _read_payload_text(root, payload_ref, location,
                                          edit.read_range)
            else:
                text = _slice_range(_read_body_text(root, edit.node_id),
                                    edit.read_range)
        except (EditError, FileNotFoundError) as exc:
            print(f"ERR: {exc}", file=sys.stderr)
            return 2
        if args.dry_run:
            print(f"read {edit.read_target} {edit.read_range} "
                  f"({len(text)} chars) of {edit.node_id}")
            return 0
        sys.stdout.write(text)
        if text:
            sys.stdout.write("\n")
        return 0

    # hypothesis:l3-node-without-mint-id -- `adopt` is the one verb that does
    # NOT accumulate into an Edit and submit through `update_node` (which
    # would refuse `mint_id` as PROTECTED). It routes through
    # `node_writer.repair_mint`: mint a first mint_id, refuse an existing one.
    if edit.adopt:
        if (edit.set_fm or edit.unset_fm or edit.thought or edit.body_append
                or edit.payload_from or edit.payload_bytes):
            print("ERR: adopt is standalone; it cannot share a line with "
                  "other verbs", file=sys.stderr)
            return 2
        if args.dry_run:
            print(f"adopt {edit.node_id}: would mint a first mint_id "
                  "(refuses if one exists)")
            return 0
        try:
            res = node_writer.repair_mint(root, edit.node_id, announce=True)
        except Exception as exc:
            print(f"ERR: adopt failed: {exc}", file=sys.stderr)
            return 2
        if res.status == node_writer.REJECTED:
            print(f"ERR: {res.reason}", file=sys.stderr)
            return 2
        if res.status == node_writer.SKIPPED:
            print(f"SKIP: {edit.node_id} -- {res.reason}", file=sys.stderr)
            return 1
        mint = ""
        try:
            import re as _re
            _mt = _re.search(r"^mint_id:\s*([^\n\s]+)",
                             res.path.read_text(encoding="utf-8"), _re.M)
            mint = _mt.group(1) if _mt else ""
        except Exception:
            pass
        print(f"adopted: {edit.node_id} mint_id={mint or '(written)'}")
        return 0

    if edit.patch_from == "-":
        # `patch -` reads the diff from stdin, the way `payload -` already
        # does: a diff is bytes that can contain almost any character, so it
        # cannot ride an `&&` script chunk (the doubled ampersand splits it).
        edit.patch_diff = sys.stdin.read()

    # hypothesis:l4-replace-api-drops-source — ONE resolver, not a second
    # read. Delegate to the same function `submit` uses, so dry-run shows the
    # bytes and a missing/empty source refuses here exactly as it refuses in
    # the library. Refusals print ERR and write nothing.
    try:
        _resolve_replace_text(edit)
    except EditError as exc:
        print(f"ERR: {exc}", file=sys.stderr)
        return 2

    # `patch <path>` reading happens in `submit` (fail-closed, after the
    # payload ref is resolved) rather than here, so a refused diff is still
    # refused before consuming it.

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
        if edit.patch_diff:
            _src = "stdin" if edit.patch_from == "-" else edit.patch_from
            print(f"  patch   ({len(edit.patch_diff)} bytes of diff, {_src})")
        if edit.patch_from and not edit.patch_diff:
            print(f"  patch   from {edit.patch_from}")
        if edit.body_patch_diff:
            _src2 = "stdin" if edit.body_patch_from == "-" else edit.body_patch_from
            print(f"  body_patch ({len(edit.body_patch_diff)} bytes of diff, {_src2})")
        if edit.body_patch_from and not edit.body_patch_diff:
            print(f"  body_patch from {edit.body_patch_from}")
        if edit.replace_target:
            _src3 = "stdin" if edit.replace_from == "-" else edit.replace_from
            print(f"  replace {edit.replace_target} {edit.replace_range} "
                  f"({len(edit.replace_text)} chars, {_src3})")
        return 0

    if edit.payload_from == "-":
        # The CLI layer reads stdin; the library never does. `payload -` is
        # for content that cannot ride in an argv chunk -- anything with `&&`
        # in it, or a whole file being piped in.
        edit.payload_from = ""
        edit.payload_bytes = sys.stdin.read()

    if edit.body_patch_from == "-":
        # Same stdin contract as `payload -` / `patch -`: the diff bytes ride
        # stdin because a diff can contain the doubled ampersand that would
        # split the `&&` script form. Read once, here, never in the library.
        edit.body_patch_from = ""
        edit.body_patch_diff = sys.stdin.read()

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
