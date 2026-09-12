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
import geometry_config  # noqa: E402
import frontmatter  # noqa: E402  # the ONE line-anchored boundary rule

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
    # hypothesis:l4-a-ring-decision-carries-m-of-n-signatures -- the ring
    # signatures backing a non-self-row config write that a `ring:`-declaring
    # schema demands (rung 2). Each is `<post>:<scheme>:<sig_hex>` over the
    # record's canonical bytes, verified through the seatsig Scheme
    # interface (`seatsig/rings.py`). Absent list -> no quorum demanded.
    signatures: list = field(default_factory=list)
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

def _marker_bad_line(line: str) -> bool:
    """True when `line` is one the shared line-anchored reader would split
    on: a line exactly `---` (frontmatter.py's `_FM_LINE` — the ONE boundary
    rule, IMPORTED here, never re-spelled) or an open `<!-- THOUGHT:` marker
    (the authored-region begin)."""
    return (frontmatter._FM_LINE.match(line) is not None
            or "<!-- THOUGHT:" in line)


def _refuse_marker_value(key: str, value) -> str | None:
    """Return a ONE-LINE refusal (naming `key`) when `value` would write a
    frontmatter region the shared line-anchored reader (`frontmatter.py`) or
    the thought extraction would mis-read — a line exactly `---` (the ONE
    boundary rule, imported not re-spelled) or an open `<!-- THOUGHT:` marker.
    None when the value is safe.

    Used by BOTH `set` and `create --set` (claim 6b, hypothesis:
    l4-prepare-check-2-reads-the-index-blob-...): a value the reader would
    split on is refused by the writer identically through either verb, so
    create never lands a bare-marker value the reader then mis-splits.
    Scalars collapse their newlines (`_scalar`) and are quoted when they carry
    a `---` run, so the shapes whose marker content survives rendering are
    list-string items (emitted raw as `- <item>`) and the THOUGHT marker
    substring in any string form."""
    if isinstance(value, list):
        for item in value:
            if isinstance(item, str):
                # a list item renders RAW as `- <item>`; lines after the
                # first survive at column 0 (the danger lines).
                if any(_marker_bad_line(ln)
                       for ln in item.split("\n")[1:]):
                    return (f"cannot set {key!r}: the value would render a "
                            "bare `---` line or an open THOUGHT marker, "
                            "which the shared line-anchored reader would "
                            "mistake for the closing frontmatter marker")
            else:
                nested = _refuse_marker_value(key, item)
                if nested:
                    return nested
    elif isinstance(value, dict):
        return _refuse_marker_value(key, list(value.values()))
    elif isinstance(value, str) and "<!-- THOUGHT:" in value:
        return (f"cannot set {key!r}: the value carries an open "
                "THOUGHT marker")
    return None


def verb_set(edit: Edit, key: str, value: str) -> Edit:
    """`set <key> <value>` — one frontmatter field."""
    if key in PROTECTED:
        raise EditError(
            f"{key!r} is identity or completion state and no verb may set it. "
            f"A mint id is assigned once (goal:g2.5); scaffold_hash is how "
            f"completion is detected, and edit mode is not a loophole in the "
            f"rule the kid brief already follows.")
    coerced = _coerce(value)
    refusal = _refuse_marker_value(key, coerced)
    if refusal:
        raise EditError(refusal)
    edit.set_fm[key] = coerced
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

#: One-line example per verb, for the help epilog. Module-level (not local to
#: main) so a test can assert each example PARSES as its verb's arity via the
#: shared `parse_script` -- the drift guard that completes the epilog check
#: (hypothesis:l4-the-carve-out-refuses-a-non-dict-template-and-keys-on-the-
#: resolved-seat). The `set` example is `set key value` (TWO arguments), never
#: `set k=v`; the parser splits `k=v` as one token and the grammar the epilog
#: teaches would be refused.
VERB_EXAMPLES = {
    "set": "set key value",
    "unset": "unset frontmatter_key",
    "link": "link self",
    "thought": "thought why this version differs",
    "note": "note a whole sentence, spaces absorbed",
    "payload": "payload path/to/source.py",
    "payload_text": "payload_text literal text body",
    "patch": "patch -",
    "body_patch": "body_patch -",
    "read": "read body 4:9",
    "replace": "replace body 4:9 path/to/file",
    "adopt": "adopt",
}


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


def _load_seats(root) -> list[dict]:
    """The geometry config `posts:`/`seats:` rows (config:posts, post-first
    with a one-season config:seats fallback), or [] when absent/unparseable.
    Shared resolver: geometry_config.load_rows. Each row carries `name` and
    `role`, which is what role resolution keys on.
    """
    return geometry_config.load_rows(root)


def _pick_longest_role(candidates: list[tuple[int, str, str]]):
    """From `(name_len, name, role)` candidates pick the longest match's role,
    fail-closed. A tie at the same longest length REFUSES — it never picks one
    arbitrarily (hypothesis:l4-role-resolution-longest-prefix). Under the
    strict `==`/`startswith(name+'-')` boundary rule a real-input tie is
    structurally impossible, so this guard is defensive by design: if the
    seat table ever grows a case that produces one, we refuse rather than
    silently grant a role.
    """
    if not candidates:
        return None
    longest = max(c[0] for c in candidates)
    at_longest = [c for c in candidates if c[0] == longest]
    if len(at_longest) > 1:
        names = ", ".join(sorted(c[1] for c in at_longest))
        raise EditError(
            f"ambiguous seat prefix: seats {names} tie at the longest match; "
            f"refusing to pick one (fail-closed, "
            f"hypothesis:l4-role-resolution-longest-prefix)")
    return at_longest[0][2]


def _resolve_seats_role(root, actor: str):
    """Resolve the actor's role from the config:seats rows, longest-prefix-wins.

    A row matches only when the actor EQUALS the row name or begins with the
    row name FOLLOWED BY `-` — a bare `startswith` would let the row `alive`
    claim `aliveness-bot`, and matching the other way round would let the
    actor `sanctuary` claim several rows at once. Returns the role string, or
    None when no row matches (caller falls through to the `owner` literal), or
    raises EditError when two distinct rows tie at the longest length.
    """
    if not actor:
        return None
    candidates: list[tuple[int, str, str]] = []
    for row in _load_seats(root):
        name = row.get("name")
        role = row.get("role")
        if not name or not role:
            continue
        if actor == name or actor.startswith(name + "-"):
            candidates.append((len(name), str(name), str(role)))
    return _pick_longest_role(candidates)


# The role ladder, highest power first (hypothesis:l4-a-role-is-resolved-
# never-typed): a caller may name, explicitly or via AGI_ROLE, ONLY the role
# its resolved seat holds or a LOWER one — never a higher one. Lower number =_
# higher power, so a requested role is an elevation (refused) exactly when its
# rank is strictly less than the seat role's rank.
_LADDER = {"owner": 0, "prime_director": 1, "director": 2,
           "parent": 3, "kid": 4}


def _ceiling_refusal(requested: str, seat_role: str | None, actor: str,
                     source: str) -> str | None:
    """The refusal text when `requested` names a role HIGHER on the ladder
    than the actor's resolved seat role; None when it is not an elevation.
    `source` is `--role` or `AGI_ROLE`, used verbatim in the message
    (hypothesis:l4-a-role-is-resolved-never-typed). An actor with no seat row
    or a seat role outside the ladder refuses nothing (fallbacks unchanged);
    a requested role not on the ladder is likewise not ours to refuse."""
    if seat_role not in _LADDER or requested not in _LADDER:
        return None
    if _LADDER[requested] < _LADDER[seat_role]:
        return (f"{source} {requested} refused: actor {actor} resolves to "
                f"{seat_role} (a role may name only the one the actor's seat "
                f"holds or a lower one; "
                f"hypothesis:l4-a-role-is-resolved-never-typed)")
    return None


def _resolve_role(root, actor: str, role_param: str = "") -> str:
    """The effective role for a write, resolved fail-closed in order.

    (1) an explicit `--role` if passed; (2) else the `AGI_ROLE` env var;
    (3) else the config:seats row whose name is a prefix of the actor (longest
    wins, boundary required, tie refuses); (4) else the literal actor `owner`
    -> role `owner`; (5) else UNRESOLVED (`""`), which the caller refuses
    ONLY when the type declares `written_by`.

    A role named by `--role` or `AGI_ROLE` may name only the role the actor's
    seat resolves to or a LOWER one on the ladder (owner > prime_director >
    director > parent > kid); a higher one is refused by name and nothing is
    written (hypothesis:l4-a-role-is-resolved-never-typed). An actor that
    resolves to no seat keeps the fallbacks unchanged.
    """
    seat_role = _resolve_seats_role(root, actor)
    if role_param:
        refusal = _ceiling_refusal(role_param, seat_role, actor, "--role")
        if refusal:
            raise EditError(refusal)
        return role_param
    env = (os.environ.get("AGI_ROLE") or "").strip()
    if env:
        refusal = _ceiling_refusal(env, seat_role, actor, "AGI_ROLE")
        if refusal:
            raise EditError(refusal)
        return env
    if seat_role is not None:
        return seat_role
    if actor == "owner":
        return "owner"
    return ""


SELF_ROW_PROTECTED = frozenset({
    # Prime/owner-only on a config node's seat rows; a seated self-row writer
    # may never touch these, and the presence of ANY of them in a self-row
    # write refuses the whole thing (L4.110 prime ruling B). The list is data
    # here because the directive named it verbatim; enforcement stays generic.
    "role", "model", "tier", "harness", "effort",
    "owning_goal", "worktree", "rotated_by",
})


def _resolve_seat(root, actor: str):
    """The NAME of the config:seats row the actor resolved from, or None.

    The mirror of `_resolve_seats_role`, kept as the one place BOTH callers
    key on, so the self-row rule matches the SAME identity `_resolve_role`
    used to admit the writer — never the free-text `--actor` string (L4.110
    prime ruling B). Longest-prefix-with-boundary wins; a tie at the longest
    length refuses (fail-closed, same rule as `_pick_longest_role`).
    """
    if not actor:
        return None
    candidates: list[tuple[int, str]] = []
    for row in _load_seats(root):
        name = row.get("name")
        role = row.get("role")
        if not name or not role:
            continue
        if actor == name or actor.startswith(name + "-"):
            candidates.append((len(name), str(name)))
    if not candidates:
        return None
    longest = max(c[0] for c in candidates)
    at_longest = [c for c in candidates if c[0] == longest]
    if len(at_longest) > 1:
        names = ", ".join(sorted(c[1] for c in at_longest))
        raise EditError(
            f"ambiguous seat prefix: seats {names} tie at the longest match; "
            f"refusing to pick one (fail-closed, L4.110 self-row rule)")
    return at_longest[0][1]


def _self_row_refusal(root, schema, actor, set_fm, unset_fm, where: str):
    """Evaluate a config node's `self_row` declaration for a seated writer.

    The directive (L4.110 prime ruling B): a writer whose RESOLVED role is a
    seated role may update only the row whose `match_key` equals the seat it
    resolved from, and only the declared `fields`; every prime-only field and
    every other row is refused WHOLE. Returns None when the write is a valid
    own-row, declared-fields-only write, else a human refusal message.
    GENERIC by construction: everything here is read from the schema's
    `self_row` mapping — there is no `seats` literal in this function.
    """
    sr = schema.frontmatter.get("self_row")
    if not isinstance(sr, dict):
        return None
    seat = _resolve_seat(root, actor)
    if seat is None:
        return None  # not a seated writer; the caller's written_by gate decides
    # The list key is resolved POST-FIRST from the live geometry config
    # (hypothesis:l4-a-seat-is-a-post-everywhere): `posts` when posts.md
    # exists, else `seats` when only seats.md exists. The schema's declared
    # `list_key` is used ONLY as the fallback when the resolver finds neither
    # file, so a migrated tree (posts.md) admits ack-shaped `set_fm["posts"]`
    # writes instead of refusing them as a foreign top-level field. The
    # schema's `list_key: seats` spelling stays as the one-season deprecated
    # alias.
    lst_path, resolved_key = geometry_config.resolve(root)
    if lst_path is not None and Path(lst_path).exists() and resolved_key in (
            "posts", "seats"):
        list_key = resolved_key
    else:
        list_key = sr.get("list_key")
    match_key = sr.get("match_key")
    fields = [str(f) for f in (sr.get("fields") or [])]
    if not list_key or not match_key:
        return "self_row declaration is missing list_key/match_key"

    # 1) No top-level field other than the list_key may be written by a
    #    seated role — those are prime/owner-only declarations.
    touched_top = set(set_fm or {}) | set(unset_fm or {})
    bad_top = touched_top - {list_key}
    if bad_top:
        return ("a seated role may write ONLY the "
                f"`{list_key}` row list (touched top-level field(s) "
                f"{', '.join(sorted(bad_top))}); those declarations are "
                "prime/owner-only")

    # 2) The row list itself must be present and shaped.
    if list_key not in set_fm:
        return (f"a self-row write must supply the `{list_key}` list "
                "(nothing set)")
    new_rows = set_fm[list_key]
    if not isinstance(new_rows, list):
        return f"`{list_key}` must be a list of rows, got {type(new_rows).__name__}"
    # The current rows, read from the pre-write node file in the same root — a
    # seated writer's whole-list set must reproduce them with its own row's
    # declared fields changed and NOTHING else.
    old_rows = _load_seats(root)

    old_own = next((r for r in old_rows if r.get(match_key) == seat), None)
    new_own = next((r for r in new_rows if r.get(match_key) == seat), None)
    if new_own is None:
        return f"the row whose `{match_key}` is {seat!r} must survive the write"
    if old_own is None:
        return (f"no current row whose `{match_key}` is {seat!r}; a seated "
                "writer may only update its OWN existing row")

    # Every other row must be byte-identical (same rows, same order, same k/v).
    old_others = [r for r in old_rows if r.get(match_key) != seat]
    new_others = [r for r in new_rows if r.get(match_key) != seat]
    if old_others != new_others:
        return ("a seated role may update ONLY its own row; another row's "
                "bytes changed or an unrelated row was added/removed")

    # The own row may differ only in declared fields.
    old_own = old_own or {}
    keys = set(old_own.keys()) | set(new_own.keys())
    for k in keys:
        if k == match_key:
            continue
        if old_own.get(k) != new_own.get(k):
            if k not in fields:
                if k in SELF_ROW_PROTECTED:
                    return (f"field {k!r} is prime/owner-only on a seat row; "
                            "a seated role may never write it")
                return (f"field {k!r} is not in the self-row fields "
                        f"{fields} declared by the node's schema")
    return None


def _read_node_fm(root, node_id):
    """Read a node's CURRENT frontmatter as a dict, or None if unreadable.

    Needed by the master-sensei templates carve-out to compare the bytes the
    write would replace against the bytes on disk (the self_row pattern).
    Read-only; this module performs no file write.
    """
    try:
        from graph_core.persistence import frontmatter as fm_reader
    except Exception:  # noqa: BLE001
        return None
    try:
        path = node_writer.find_node_file(root, node_id)
    except Exception:  # noqa: BLE001
        return None
    if path is None:
        return None
    try:
        return dict(fm_reader.load_node_file(path).frontmatter)
    except Exception:  # noqa: BLE001
        return None


def _master_sensei_templates_refusal(root, schema, actor, set_fm, unset_fm,
                                     where: str):
    """The master-sensei templates carve-out (PRIME RULING 2026-09-11,
    hypothesis:write-guard-carve-out-for-master-sensei-templates).

    The Sensei keeps improving the roles' rotation config directly instead of
    dm-and-wait. It may write ONLY certain regions of config:rotations
    `templates`: each role entry's `startup` and `telemetry`, and the `## facts`
    body section, for EVERY role EXCEPT the declared deny-roles (prime_director
    -- Prime/owner-only). `brief_file` and `steps` of any template stay
    prime/owner-only. The rule is DATA - the allowed regions, the deny roles
    and the writable fields all live in the schema's `master_sensei_row`
    declaration, with no role literal in this function (the self_row pattern).

    A second, load-bearing half is the PRODUCING JUDGE: every resolved
    first_turn/after_join cmd in the written value must pass
    `rotate._producing_refusal` - the guard runs the same judge the executor
    would, so a Sensei cannot land an entry the executor would refuse, and the
    refusal NAMES the entry. Returns None when the write is a valid
    master-sensei template write, else a human refusal message.
    """
    ms = schema.frontmatter.get("master_sensei_row")
    if not isinstance(ms, dict):
        return None  # no declaration -> the written_by gate decides
    actor_row = ms.get("actor")
    if not actor_row:
        return None
    # The master-sensei identity is the RESOLVED SEAT NAME only -- the same
    # identity the self_row rule keys on (L4.110 prime ruling B). A free-text
    # `--actor` whose string merely starts with the declared name is NOT the
    # master-sensei: the caller-supplied string is never the identity, the
    # seats registry is (hypothesis:l4-the-carve-out-refuses-a-non-dict-
    # template-and-keys-on-the-resolved-seat).
    is_ms = _resolve_seat(root, actor) == str(actor_row)
    if not is_ms:
        return None  # not the master-sensei seat; not this carve-out
    list_key = ms.get("list_key")
    fields = [str(f) for f in (ms.get("fields") or [])]
    role_field = ms.get("role_field") or "id"
    deny = [str(r) for r in (ms.get("deny_roles") or [])]
    if not list_key:
        return "master_sensei_row declaration is missing list_key"

    # The whole-list replacement is the write shape (set_fm[list_key] == the
    # full `templates` mapping), exactly as self_row replaces the full list.
    if list_key not in set_fm:
        return None  # not touching templates; body gate / written_by decide
    new_val = set_fm[list_key]
    if not isinstance(new_val, dict):
        return f"`{list_key}` must be a dict of role templates, got " \
               f"{type(new_val).__name__}"
    old_fm = _read_node_fm(root, where)
    old_val = (old_fm or {}).get(list_key)
    if old_val is None:
        old_val = {}
    if not isinstance(old_val, dict):
        return f"current `{list_key}` is not a dict; refusing to judge the delta"

    roles = set(old_val.keys()) | set(new_val.keys())
    for role in roles:
        if role in deny:
            if old_val.get(role) != new_val.get(role):
                return (f"the {role!r} template is prime/owner-only; a "
                        "master-sensei write may NOT touch it (owner: "
                        "'modifications to Belam or his advisors require "
                        "owner approval')")
            continue
        old_r = old_val.get(role) or {}
        new_r = new_val.get(role) or {}
        # A non-dict template value is NEVER a valid master-sensei write: it
        # would silently drop brief_file/steps (whose field check below is
        # gated on BOTH being dicts) and can't be judged by the producing
        # judge. Refuse by name, so `templates.director = 'garbage'` is not
        # admitted and the director's brief_file + steps survive
        # (hypothesis:l4-the-carve-out-refuses-a-non-dict-template-and-keys-
        # on-the-resolved-seat).
        if role in new_val and not isinstance(new_val[role], dict):
            return (f"template {role!r} must be a dict of fields, got "
                    f"{type(new_val[role]).__name__}")
        if isinstance(old_r, dict) and isinstance(new_r, dict):
            keys = set(old_r.keys()) | set(new_r.keys())
            for k in keys:
                if old_r.get(k) != new_r.get(k):
                    if k not in fields:
                        return (f"template field {k!r} is prime/owner-only; a "
                                f"master-sensei write may change only "
                                f"{', '.join(sorted(fields))} (the regions "
                                f"declared writable)")

    # PRODUCING JUDGE gate: every resolved first_turn/after_join cmd in the
    # written templates (deny-role entries excluded) must pass
    # rotate._producing_refusal; a refused entry refuses the whole write,
    # naming the entry (test c).
    try:
        import rotate
    except Exception:  # noqa: BLE001
        return None
    for role in roles:
        if role in deny:
            continue
        new_r = new_val.get(role)
        if not isinstance(new_r, dict):
            continue
        startup = new_r.get("startup")
        if isinstance(startup, dict):
            for sec in ("first_turn", "after_join"):
                for entry in startup.get(sec) or []:
                    if not isinstance(entry, dict):
                        continue
                    label = entry.get("label") or "(unlabeled)"
                    cmd = entry.get("cmd") or ""
                    refusal = rotate._producing_refusal(str(cmd))
                    if refusal is not None:
                        return (f"master-sensei write refused: startup entry "
                                f"{label!r} would be refused by the startup "
                                f"producing judge: {refusal}")
    return None


def _sectionize(body: str):
    """Split a node body into {header: text} + a preamble, keyed on `## `.

    A `## ` header starts a section; the preamble is everything before the
    first one. Same-splitting both the old and new body lets the facts gate
    require byte-identity OUTSIDE the `## facts` section without diffing.
    """
    if body is None:
        return None, {}
    lines = body.splitlines(keepends=True)
    preamble: list[str] = []
    sections: dict[str, list[str]] = {}
    cur = None
    for ln in lines:
        if ln.startswith("## "):
            cur = ln[3:].strip()
            sections.setdefault(cur, [])
        elif cur is None:
            preamble.append(ln)
        else:
            sections[cur].append(ln)
    # Normalise a single trailing newline so a serializer-perceived difference
    # (the frontmatter reader strips it, the splice can keep it) does not look
    # like a section delta.
    return "".join(preamble).rstrip("\n"), {
        k: "".join(v).rstrip("\n") for k, v in sections.items()}


def _enforce_master_sensei_facts_body(root, node_id, actor, new_body):
    """Refuse a master-sensei body edit whose delta leaves `## facts`.

    The third writable region of the carve-out: the `## facts` body section
    of the governed node. The rest of the body (templates/steps/preamble and
    every other section) stays prime/owner-only, so the delta must be
    byte-identical outside the `## facts` section. A no-op for any non
    master-sensei writer (their admission is the written_by gate's business).
    """
    try:
        from schema_registry import load_schemas_from_dir
    except Exception:  # noqa: BLE001
        return
    if new_body is None:
        return
    node_type = str(node_id).split(":", 1)[0]
    schemas_dir = Path(root) / "context" / "schemas"
    if not schemas_dir.is_dir():
        return
    try:
        schema = load_schemas_from_dir(schemas_dir).get(node_type)
    except Exception:  # noqa: BLE001
        return
    ms = schema.frontmatter.get("master_sensei_row") if schema else None
    if not isinstance(ms, dict) or not ms.get("actor"):
        return
    list_key = ms.get("list_key")
    if not list_key:
        return
    # The master-sensei identity is the RESOLVED SEAT NAME only (L4.110 self_row
    # rule); a free-text `--actor` is never the identity (hypothesis:l4-the-
    # carve-out-refuses-a-non-dict-template-and-keys-on-the-resolved-seat).
    is_ms = _resolve_seat(root, actor) == str(ms.get("actor"))
    if not is_ms:
        return  # a non-master-sensei writer's body edit is not this gate
    # The facts-body carve-out applies ONLY to the node whose FRONTMATTER
    # carries the declaration's list_key (the `templates` node). A body-only
    # master-sensei edit on ANY OTHER config node (a config:seats body probe,
    # say) is not granted here -- it falls through to the written_by gate and
    # is refused.
    try:
        old_body = _read_body_text(root, node_id)
    except EditError:
        return
    node_fm = _read_node_fm(root, node_id) or {}
    if not node_fm.get(list_key):
        raise EditError(
            f"{node_id}: a master-sensei body edit is limited to the `## facts` "
            f"section of the node that carries the declaration's list_key "
            f"`{list_key}`; this node does not (PRIME RULING 2026-09-11, "
            f"hypothesis:l4-the-carve-out-refuses-a-non-dict-template-and-"
            f"keys-on-the-resolved-seat)")
    old_preamble, old_secs = _sectionize(old_body)
    new_preamble, new_secs = _sectionize(new_body)
    if old_secs is None or new_secs is None:
        return
    if old_preamble != new_preamble:
        raise EditError(
            f"{node_id}: a master-sensei body edit may change ONLY the "
            f"`## facts` section; the preamble changed (PRIME RULING "
            f"2026-09-11, hypothesis:write-guard-carve-out-for-master-"
            f"sensei-templates)")
    for sec in set(old_secs) | set(new_secs):
        if sec == "facts":
            continue
        if old_secs.get(sec) != new_secs.get(sec):
            raise EditError(
                f"{node_id}: a master-sensei body edit may change ONLY the "
                f"`## facts` section; section {sec!r} changed "
                f"(PRIME RULING 2026-09-11, hypothesis:write-guard-carve-"
                f"out-for-master-sensei-templates)")


def _ring_pubkey_for_post(root):
    """Resolve a ring member's CURRENT pubkey for the write gate: the posts/
    seats geometry rows' `pubkey` cell under the graph root, or None when the
    post has no resolvable key (a ring then reads UNKEYED for it and it does
    not count toward m).
    """
    try:
        rows = geometry_config.load_rows(root)
    except Exception:  # noqa: BLE001
        rows = []

    cache = {r.get("name"): (r.get("pubkey") or None) for r in rows}

    def resolver(post):
        return cache.get(post)

    return resolver


def _config_write_fields(where, set_fm):
    """The FULL config-write decision fields a ring's signatures cover: the
    node id AND every row field being written, its value string-serialized by
    rings.json_field -- NO truncation (hypothesis:l4-a-ring-decision-carries-
    m-of-n-signatures claim (2), HOLE 2: the signed bytes must cover the
    decision they authorise, so a signature for one row cannot authorise a
    different one). The sign side, the gate, and the persisted record all use
    these same bytes."""
    from seatsig import rings as _rings  # noqa: PLC0415
    fields = {"node": where}
    for k, v in (set_fm or {}).items():
        fields[k] = _rings.json_field(v)
    return fields


def _enforce_written_by(root, node_type, actor, where, role: str = "",
                        set_fm: dict | None = None,
                        unset_fm: list | None = None,
                        allow_self_row: bool = False,
                        has_body: bool = False,
                        signatures: list | None = None,
                        out_decision: dict | None = None):
    """Refuse a write when the node type's OWN schema declares a restricted
    writer (hypothesis:l4-moral-written-by-carrier).

    The owner-only rule lives as DATA — `written_by:` in the frontmatter of
    `context/schemas/[<type>].md` — read through `schema_registry`, not as a
    hardcoded type literal here. So the rule is carried by the type that owns
    it, and a schema that declares no `written_by` (or whose schema is
    absent) gates nothing: the moral schema's `written_by: owner` is the one
    and only thing that makes moral nodes hand-edit-by-owner-only.

    L4.41: the compare is a RESOLVED ROLE, never the actor string. The Prime
    writes as `belam-S1-L4-<N>`, a generation name that changes every
    rotation, so keying on the actor would break on a schedule nobody
    controls; `written_by` admits ROLES. `admitted` is one parse shared with
    `links.py` (`parse_written_by`), so a list-valued or comma-separated
    `written_by` refuses nothing it admits. An UNRESOLVED identity refuses
    only because the type declares `written_by`; a schema declaring nothing
    still gates nothing. The refusal names the node TYPE and its admitted
    roles — never a hardcoded type literal (L4.40).
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
    if not admitted:
        return
    resolved = _resolve_role(root, actor, role)
    if resolved in admitted:
        return

    # PRIME RULING 2026-09-11 carve-out: the master-sensei seat may write
    # config:rotations `templates` (startup/telemetry, facts body) directly
    # instead of dm-and-wait. Authorized by the schema's `master_sensei_row`
    # declaration, gated by the startup producing judge -- one generic rule,
    # no role literal in the enforcement path (the self_row pattern). Must be
    # tried only when the writer is NOT admitted. Two entry shapes: a
    # templates frontmatter set (checked here against old bytes + the
    # judge), and a body-only edit (set_fm/unset_fm empty -- checked by
    # submit's facts-region gate, since the body bytes only exist after
    # composition). This block comes BEFORE the self_row gate so a
    # master-sensei templates write is adjudicated by this carve-out, not
    # refused by an unrelated seats declaration.
    ms = schema.frontmatter.get("master_sensei_row")
    if isinstance(ms, dict) and ms.get("actor") and has_body is not None:
        # The master-sensei identity is the RESOLVED SEAT NAME only (L4.110
        # self_row rule); a free-text `--actor` string is never the identity
        # (hypothesis:l4-the-carve-out-refuses-a-non-dict-template-and-keys-
        # on-the-resolved-seat).
        is_ms = _resolve_seat(root, actor) == str(ms.get("actor"))
        if is_ms:
            touches_templates = (set_fm is not None
                                 and ms.get("list_key") in set_fm)
            if touches_templates:
                mrefusal = _master_sensei_templates_refusal(
                    root, schema, actor, set_fm, unset_fm, where)
                if mrefusal is None:
                    return
                raise EditError(
                    f"{node_type} nodes ({where}): a master-sensei write is "
                    f"limited to the declared template regions and must pass "
                    f"the startup producing judge; {mrefusal} "
                    f"(PRIME RULING 2026-09-11)")
            if has_body and not (set_fm or unset_fm):
                # Body-only master-sensei edit: the facts-body carve-out
                # applies ONLY to the node whose frontmatter carries the
                # declaration's list_key (the `templates` node). A config:seats
                # body probe, or any other config node, is NOT granted here and
                # falls through to the written_by refusal below
                # (hypothesis:l4-the-carve-out-refuses-a-non-dict-template-
                # and-keys-on-the-resolved-seat).
                if ms.get("list_key") and (_read_node_fm(root, where) or {}).get(
                        ms.get("list_key")):
                    # admission here is refined by submit's facts-region gate,
                    # which refuses any delta outside the `## facts` section.
                    return

    # L4.110 prime ruling B carve-out: a SEATED role (a director on a seat,
    # say) is not in `written_by` and yet may update ONE thing — its own seat
    # row, restricted to the fields the type's `self_row` declaration names.
    # This is the only unadmitted-writer path; without the schema declaring
    # `self_row`, or for a `create`, the refusal below holds exactly as
    # before. `allow_self_row` is True only for `submit` (an edit); `create`
    # never admits a seated writer to mint a config node.
    if allow_self_row and (set_fm is not None or unset_fm is not None):
        sr = schema.frontmatter.get("self_row")
        if isinstance(sr, dict) and _resolve_seat(root, actor) is not None:
            refusal = _self_row_refusal(root, schema, actor, set_fm,
                                        unset_fm, where)
            if refusal is None:
                return
            raise EditError(
                f"{node_type} nodes ({where}): a seated role may update only "
                f"its OWN row and only the declared fields; {refusal}. "
                f"(L4.110 prime ruling B)")

    # RUNG 2 ring gate (hypothesis:l4-a-ring-decision-carries-m-of-n-
    # signatures). OPT-IN: only a schema that declares `ring: <name>` — the
    # ring whose quorum governs NON-SELF-ROW config writes to this node type
    # — demands a quorum, and only for a config-row edit (set_fm/unset_fm),
    # never a body-only or self-row write (those returned above). The quorum
    # is verified through the SAME seatsig Scheme interface send.py uses
    # (seatsig/rings.py), never the gate's own crypto; a record short of m is
    # REFUSED BY NAME with the m-of-n count.
    ring_name = schema.frontmatter.get("ring")
    if ring_name and (set_fm or unset_fm):
        try:
            from seatsig import rings as _rings

            rings_rows = _rings.load_rings(root)
            ring = _rings.ring_by_name(rings_rows, ring_name)
        except Exception:  # noqa: BLE001
            ring = None
        if ring is not None:
            fields = _config_write_fields(where, set_fm)
            canonical = _rings.canonical_bytes("config-write", fields)
            res = _rings.verify_ring(
                ring, canonical, signatures or [],
                pubkey_for_post=_ring_pubkey_for_post(root))
            if not res.ok:
                raise EditError(
                    f"{node_type} nodes ({where}): {res.refused}. "
                    f"(rung 2 multisig ring)")
            # RUNG 2 claim (2): hand the admitted config-write decision
            # (kind + signed fields + signatures) back to the caller so it
            # can be persisted onto the node the write sanctions -- a reader
            # then re-verifies m-of-n from disk, never argv.
            if out_decision is not None:
                out_decision["cell"] = _rings.decision_cell(
                    ring_name, "config-write", fields, signatures or [])
            return  # ring quorum satisfied -> admit

    raise EditError(        
        f"{node_type} nodes ({where}) may be hand-edited only by "
        f"admitted roles {', '.join(sorted(admitted))}; resolution for actor "
        f"{actor!r} gave {resolved or 'UNRESOLVED'}, which is not admitted. "
        f"(goal:g12)")


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


def _resolve_api_root(root) -> Path:
    """Resolve the graph root a caller handed the Python API — DESCEND-ONLY.

    The CLI resolves `--root` through `locations.find_project_root` BEFORE
    touching `create`/`submit` (write.py:1208, :1253), so CLI callers are
    safe. The API takes `root` raw (hypothesis:l4-write-api-root-resolution),
    and a raw `.` from the repo root used to mint into `<repo>/nodes/...`
    instead of `<repo>/.agi/nodes/...`, silently. Worse, a caller inside a
    bare dir with no project of its own would have had `find_project_root`
    walk UP into a real ancestor graph and write a node into it — a
    data-loss-shaped hazard for any test that passed a no-`.agi/` tmp dir.

    Resolution here looks at ONLY `root` and the `.agi/` directly beneath it,
    and NEVER walks up the filesystem: a project path resolves to its graph
    root, and a bare dir REFUSES (raises) rather than resolving into a real
    graph above it. The never-ascend property is asserted directly by
    test_write.py, not inferred from the passing tests around it. Refusing
    before any write is what closes the "wrong root looks like success"
    symptom — the node is not minted and nothing is written anywhere.
    """
    d = Path(root).resolve()
    # The root itself is a graph root (a `.agi/` dir, or a legacy config dir).
    if locations.config_path(d) is not None:
        return d
    # `root/.agi` directly beneath it holds a config (the G11 layout).
    child = d / locations.GRAPH_DIR_NAME
    if locations.config_path(child) is not None:
        return child
    raise EditError(
        f"not an agi project graph root: {root!r} — the Python API resolves "
        f"root descend-only and refuses to walk UP the filesystem into a "
        f"different project (hypothesis:l4-write-api-root-resolution). "
        f"Nothing was written.")


def submit(root, edit: Edit, actor: str = "", session: str = "", role: str = "") -> object:
    """Write the accumulated edit. **The only thing in this module that writes.**

    Returns `node_writer`'s own result object, so a caller sees `UPDATED`,
    `UNCHANGED` or `REJECTED` and the reason — the same statuses every other
    writer path reports.
    """
    if edit.empty:
        raise EditError(f"nothing to submit for {edit.node_id}")

    # hypothesis:l4-write-api-root-resolution — an API caller's `root` is
    # resolved descend-only here, so a wrong root refuses before any write.
    root = _resolve_api_root(root)

    # hypothesis:l4-replace-api-drops-source — the ONE shared resolution of
    # the replacement source. Without this, an API caller's `replace_from`
    # never became `replace_text` and submit spliced `""`, silently deleting
    # the range while reporting success. Idempotent: main has already resolved
    # it for its --dry-run preview, and this must not read stdin a second time.
    _resolve_replace_text(edit)

    _ring_out: dict = {}
    _enforce_written_by(root, edit.node_id.split(":", 1)[0], actor,
                        edit.node_id, role,
                        set_fm=edit.set_fm, unset_fm=edit.unset_fm,
                        allow_self_row=True,
                        has_body=bool(edit.body_append or edit.thought
                                      or edit.body_patch_diff
                                      or edit.replace_target == "body"),
                        signatures=getattr(edit, "signatures", []),
                        out_decision=_ring_out)

    set_fm = dict(edit.set_fm)
    # RUNG 2 claim (2): when a `ring:`-declaring schema admitted this
    # config-row write by a quorum, the verified decision (kind + signed
    # fields + signatures) is persisted onto the node's own frontmatter so the
    # node on disk carries them and a reader re-verifies m-of-n without argv.
    if _ring_out.get("cell"):
        set_fm["ring_decision"] = _ring_out["cell"]
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

    # PRIME RULING 2026-09-11 facts-region gate: a master-sensei BODY edit on
    # a `master_sensei_row`-governed node may change ONLY the `## facts`
    # section. Written here (post-composition) because the body bytes only
    # exist after the splice; `_enforce_written_by` admitted the writer on
    # the body-only path and this gate is the load-bearing confinement.
    _enforce_master_sensei_facts_body(root, edit.node_id, actor, body)

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
    seat = geometry_config.resolved_seat_env()
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
           actor: str = "", session: str = "", role: str = "",
           bypass: bool = False):
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
    # hypothesis:l4-write-api-root-resolution — same descend-only resolution
    # as submit; a wrong root refuses before the node or its payload file is
    # created, instead of minting into `<root>/nodes/...` with the spawn gate
    # silently unverified.
    root = _resolve_api_root(root)

    _enforce_written_by(root, node_type, actor, f"{node_type}:{slug}", role)

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

    #: One-line example per verb, for the help epilog. Chosen hand-in-sync by
    #: intent but CHECKED against VERBS/ARITY below so a divergence fails at
    #: help-build time instead of silently reaching a seat whose first_turn
    #: `write-verbs` fact reads this epilog for the grammar (config:rotations
    #: F4, hypothesis:write-py-help-epilog-lists-verb-grammar). The module-level
    #: `VERB_EXAMPLES` each ALSO parse as their verb's arity (asserted in
    #: test_write_master_sensei.py), so the grammar the epilog teaches is real.
    missing_v = sorted(set(VERBS) - set(VERB_EXAMPLES))
    missing_a = sorted(set(VERB_EXAMPLES) - set(ARITY))
    if missing_v or missing_a:
        raise SystemExit(
            f"write.py help epilog drift: verbs without examples "
            f"{missing_v}, examples without arity {missing_a} -- "
            "add the example (and ARITY entry) or remove stale help "
            "(hypothesis:write-py-help-epilog-lists-verb-grammar)")
    epilog_lines = [
        "verbs (each accepts a node_id first; join several with &&):",
    ]
    for name in VERBS:
        epilog_lines.append(
            f"  {name}\t{ARITY[name]} arg(s)\t{VERB_EXAMPLES[name]}")
    epilog = "\n".join(epilog_lines)

    ap = argparse.ArgumentParser(
        description=__doc__.splitlines()[0], epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)
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
    ap.add_argument("--role", default="",
                    help="explicit role, resolved ahead of AGI_ROLE and the "
                         "seat prefix (hypothesis:l4-role-resolution-longest-prefix)")
    ap.add_argument("--session", default="",
                    help="the session that produced it (thought_session)")
    ap.add_argument("--dry-run", action="store_true",
                    help="print the accumulated edit and write nothing")
    ap.add_argument("--ring-sig", dest="ring_sigs", action="append",
                    default=[],
                    help="repeatable; a `<post>:<scheme>:<sig_hex>` signature "
                         "backing a config write that a `ring:`-declaring "
                         "schema demands (rung 2, seatsig/rings.py)")
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
            k, v = k.strip(), _coerce(v.strip())
            # claim 6b: `create --set` runs the SAME marker guard as `set` —
            # a value the shared reader would split on is refused here too
            # (exit 2, one line naming the key), never landed into the
            # frontmatter for the reader to mis-split.
            refusal = _refuse_marker_value(k, v)
            if refusal:
                print(f"ERR: {refusal}", file=sys.stderr)
                return 2
            set_fm[k] = v
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
                           actor=args.actor, session=args.session, role=args.role,
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
        edit.signatures = args.ring_sigs
        res = submit(root, edit, actor=args.actor, session=args.session,
                     role=args.role)
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
