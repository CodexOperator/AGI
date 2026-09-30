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

import difflib
import json
import os
import shlex
import subprocess
import time
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
import last_act  # noqa: E402 -- hyp:l4-the-card-age-captive-... (one seat clock)
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
    #: goal:g4.18.5.1 -- `row <n>[:<i>-<j>]`: resolved to replace_range at
    #: submit, on node_writer.body_rows of the body as it is then
    row_ref: str = ""
    #: BUILD1 (goal:g7.16.1.4 W1, alive 841857ddb) -- `row <top>.<key> <src|->`:
    #: a NESTED frontmatter row (command:commands `manifest.<key>`), resolved
    #: once by `_resolve_fm_row` into `set_fm[<top>]`, so every set gate runs
    #: one (ref, source) per `row <top>.<key>` verb, applied in order (DG4
    #: 00:0xZ: a single slot kept only the LAST row of a script -- silent loss)
    fm_rows: list = field(default_factory=list)
    fm_row_resolved: bool = False
    replace_from: str = ""
    replace_text: str = ""
    replace_stdin_read: bool = False   # `replace ... -` consumed stdin (possibly empty)
    # hypothesis:lm-replace-body-anchor-guards-against-mis-offset-splices --
    # the explicit consent that admits a body range the structural guard
    # would otherwise refuse (`_body_range_refusal`). Spelled as a prefix on
    # the source argument (`replace body 4:9 --force -`), so the positional
    # range/source grammar is unchanged; an API caller sets the field.
    replace_force: bool = False
    # hypothesis:write-py-inline-replace-verb -- `sub`/`sub!`: the FIRST
    # ` => ` splits `<old>` from `<new>`; plain `sub` demands exactly ONE
    # literal match, `sub!` replaces every one. `sub_target` is `payload` or
    # `""` (node frontmatter + body). `_resolve_sub` resolves it ONCE into the
    # ordinary `set_fm` / body / `payload_bytes` paths, so no gate is skipped.
    sub_old: str = ""
    sub_new: str = ""
    sub_all: bool = False
    sub_target: str = ""
    sub_body: str = ""
    sub_diff: str = ""
    sub_count: int = 0
    sub_resolved: bool = False
    # conjunct 3: one `(target, old, new, all)` op per `sub`; applied in order.
    sub_ops: list = field(default_factory=list)
    # SM 145: every payload-writing VERB as parsed -- `payload`, `payload -` and
    # `payload_text` all fill payload_bytes, so the fields cannot count them
    payload_verbs: list = field(default_factory=list)
    # council ruling on SM 154: re-render the node in the ONE canonical form
    canonicalize: bool = False
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
                    or self.replace_target or self.sub_old or self.fm_rows
                    or self.canonicalize or self.sub_body)   # a body-only node patch (SM 154 round)


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
    refusal = _row_refusal(key, _coerce(value))
    if refusal:
        raise EditError(refusal)
    edit.set_fm[key] = _coerce(value)
    return edit


def _row_refusal(key: str, coerced) -> str | None:
    """The row checks `set` runs, ONE definition (SM 150: a node patch runs them
    too): a dotted key, a PROTECTED key, a marker-shaped value."""
    if "." in key:
        # hypothesis:l4-a-message-that-did-not-land...: a dotted key used to
        # land as a FLAT frontmatter literal (`comms.foo` as one key), which
        # no nested reader could ever find. Refuse by name instead: the
        # caller sets the parent mapping (key.split(".")[0]) as one object.
        return (
            f"cannot set {key!r}: dotted keys are not written as flat "
            f"frontmatter literals — set the parent mapping "
            f"{key.split('.', 1)[0]!r} as one object")
    if key in PROTECTED:
        return (
            f"{key!r} is identity or completion state and no verb may set it. "
            f"A mint id is assigned once (goal:g2.5); scaffold_hash is how "
            f"completion is detected, and edit mode is not a loophole in the "
            f"rule the kid brief already follows.")
    return _refuse_marker_value(key, coerced)


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
    edit.payload_verbs.append("payload_text")
    return edit


def verb_canonicalize(edit: Edit, *extra: str) -> Edit:
    """`canonicalize` -- re-render the node file in the ONE canonical form
    (node_writer.render_frontmatter + _serialize_node) and change nothing
    else. The canonical form drops frontmatter comments and non-significant
    quoting. A node `patch` refuses on a non-canonical node and names this
    verb (council ruling on SM 154, goal:g4.18.1.6)."""
    if extra:
        raise EditError(f"canonicalize takes no arguments, got: {' '.join(extra)}")
    edit.canonicalize = True
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
    edit.payload_verbs.append("patch")
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
    if edit.row_ref or edit.replace_target:   # SM N2: one target per script
        raise EditError("one body row or replace per script: the body is spliced once")
    # hypothesis:lm-replace-body-anchor-guards-against-mis-offset-splices --
    # `--force` rides the source argument as a PREFIX (`... 4:9 --force -`),
    # the one free-text positional, so the range/target grammar does not
    # change and an old script parses identically. Only a prefix followed by
    # a space is consumed; a bare `--force` stays a (nonexistent) path and
    # refuses loudly rather than silently deleting the range.
    if source.startswith("--force "):
        edit.replace_force = True
        source = source[len("--force "):].strip()
    _parse_range(rng)   # validates and raises early, so a typo refuses here
    edit.replace_target = target
    edit.replace_range = rng
    edit.replace_from = source
    if target == "payload":
        edit.payload_verbs.append("replace payload")
    return edit


def verb_row(edit: Edit, ref: str, source: str) -> Edit:
    """`row <n> <path|->` -- replace body row n of node_writer.body_rows (the
    ONE row index, goal:g4.18.5.1); `row <n>:<i>-<j> <path|->` replaces lines
    i..j INSIDE row n (a block row: THOUGHT, a fence). Every other byte stays.
    It rides the replace path (one reader, one splice, the same gate); the
    index, not a counted offset, picks the range, so the offset guard skips.

    `row <top>.<key> <src|->` (BUILD1) addresses a NESTED frontmatter row
    instead: `<src>` is the row's new YAML value; resolved by `_resolve_fm_row` into `set_fm[<top>]`; `--remove` as
    the source removes the row (an empty source refuses, SM 110)."""
    if re.fullmatch(r"[A-Za-z_][\w-]*\..+", ref):
        if any(ref == seen for seen, _ in edit.fm_rows):
            raise EditError(f"row {ref} twice in one script")
        edit.fm_rows.append((ref, source.strip()))
        return edit
    if not re.fullmatch(r"\d+(:\d+-\d+)?|name:.+", ref):
        raise EditError(f"row wants <n>, <n>:<i>-<j> or name:<NAME>, got {ref!r}")
    if edit.row_ref or edit.replace_target:
        raise EditError("one body row or replace per script: the body is spliced once")
    edit.replace_target, edit.row_ref = "body", ref
    edit.replace_from, edit.replace_force = source.strip(), True
    return edit


def _row_range(body: str, row_ref: str) -> str:
    """`<n>[:<i>-<j>]` -> the read-body range `a:b` it names, or EditError when
    row n or the sub-range is out of bounds. ONE resolver for `submit` and the
    `--dry-run` preview, so a preview shows the range the write would take."""
    rows = node_writer.body_rows(body)
    if row_ref.startswith("name:"):   # goal:g4.18.5.1.2: the ONE table row whose first cell is NAME
        name, lines = row_ref[5:], body.split("\n")
        hits = [a for a, b in rows if a == b and lines[a - 1].lstrip().startswith("|")
                and lines[a - 1].strip().strip("|").split("|")[0].strip() == name
                and not set(name) <= set("-: ")]   # a separator row is never a name
        if len(hits) != 1:
            raise EditError(f"row {row_ref}: {len(hits)} table rows are named {name!r}, want 1")
        return f"{hits[0]}:{hits[0]}"
    n, _, sub = row_ref.partition(":")
    if not 1 <= int(n) <= len(rows):
        raise EditError(f"row {n}: the body has {len(rows)} row(s)")
    a, b = rows[int(n) - 1]
    if sub:
        i, j = (int(x) for x in sub.split("-"))
        if not 1 <= i <= j <= b - a + 1:
            raise EditError(f"row {row_ref}: row {n} has {b - a + 1} line(s)")
        a, b = a + i - 1, a + j - 1
    return f"{a}:{b}"


def _resolve_fm_row(root, edit: Edit) -> None:
    """BUILD1: each `row <top>.<key>` -> `set_fm[<top>]` = the node's `<top>`
    mapping with row `<key>` replaced by the source's YAML value (order kept),
    or dropped when the source is `--remove`. Rows apply IN ORDER onto one mapping,
    so several rows of one script all land. Idempotent (main resolves it for
    its preview, submit again for an API caller). Refuses by EditError: `<top>`
    absent or not a mapping, `<key>` not a row of it, the same line setting or
    unsetting `<top>` too, a source that is unreadable or not YAML."""
    if not edit.fm_rows or edit.fm_row_resolved:
        return
    import yaml  # noqa: PLC0415
    from graph_core.persistence import frontmatter as fm_reader  # noqa: PLC0415
    path = node_writer.find_node_file(Path(root), edit.node_id)
    if path is None:
        raise EditError(f"no node file for {edit.node_id}")
    current = fm_reader.load_node_file(path, body=False).frontmatter
    tables: dict = {}
    for ref, src in edit.fm_rows:
        top, key = ref.split(".", 1)
        if top not in tables and (top in edit.set_fm or top in edit.unset_fm):
            raise EditError(f"row {ref} cannot share a line with set/unset {top}")
        table = tables.get(top, current.get(top))
        if not isinstance(table, dict):
            raise EditError(f"row {ref}: {edit.node_id} has no {top} mapping")
        if key not in table:
            raise EditError(f"row {ref}: {top} has no row {key!r}")
        if src == "--remove":   # SM 110: removal is explicit, never an empty source
            tables[top] = {k: v for k, v in table.items() if k != key}
            continue
        if src == "-":
            text = sys.stdin.read()
        else:
            try:
                text = Path(src).read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                raise EditError(f"row {ref}: cannot read {src}: {exc}")
        if not text.strip():
            raise EditError(f"row {ref}: the source is empty -- to remove the row, "
                            f"pass --remove as the source")
        try:
            value = yaml.safe_load(text)
        except yaml.YAMLError as exc:
            raise EditError(f"row {ref}: source is not YAML: {exc}")
        refusal = _refuse_marker_value(ref, value)   # SM 111: the set/sub guard
        if refusal:
            raise EditError(refusal)
        tables[top] = {k: (value if k == key else v) for k, v in table.items()}
    edit.set_fm.update(tables)
    edit.fm_row_resolved = True


def _stdin_refusal(edit: Edit) -> str | None:
    """stdin feeds ONE verb per script: a second `-` source reads '' and its
    verb is silently lost (SM 110 + 117) -- judged right after parsing and in
    submit, whatever verbs carry the `-`."""
    dashes = [f for _, f in edit.fm_rows] + [edit.replace_from, edit.payload_from,
                                              edit.patch_from, edit.body_patch_from]
    if sum(x == "-" for x in dashes) > 1:
        return "stdin feeds ONE verb per script: pass the other sources as files"
    return None


def _standalone_refusal(edit: Edit) -> str | None:
    """replace body / row is the one body writer of its submit -- judged in
    submit AND before the --dry-run preview, so both refuse alike (SM N1)."""
    if edit.replace_target == "body" and (edit.body_append or edit.thought
                                          or edit.body_patch_from or edit.body_patch_diff
                                          or edit.sub_body):
        return ("replace body is standalone; it cannot share a line with "
                "note, thought or body_patch (one body writer per submit)")
    if (edit.body_patch_from or edit.body_patch_diff) and (edit.body_append or edit.thought
                                                           or edit.sub_body):
        return ("body_patch is standalone; it cannot share a line with note, "
                "thought or sub (one body writer per submit)")
    return None


def _missing_link_refusal(root, set_fm: dict) -> str | None:
    """goal:g4.18.6.2.1 -- `set parents` / `set next_edges` naming an id no node
    carries refuses by name, judged by create's ONE lookup (the type index
    spawn_gate.gate_for_root builds for create's gate), never a second walk."""
    ids = [i for k in ("parents", "next_edges") if k in set_fm
           for i in ([set_fm[k]] if isinstance(set_fm[k], str) else set_fm[k] or [])
           if isinstance(i, str) and i.strip()]
    if not ids:
        return None
    import spawn_gate  # noqa: PLC0415
    index = spawn_gate.gate_for_root(root)[1]   # SM 122: built ONCE per command, never per id
    missing = [i for i in ids if i not in index]
    return (f"cannot set: {missing} name no node -- create it first, or name an id "
            f"that exists (goal:g4.18.6.2.1)") if missing else None


def _thought_marker_refusal(body: str, rng: str, new_text: str) -> str | None:
    """goal:g4.18.5.1.1 -- a body range holding a THOUGHT marker LINE refuses:
    update_node carries the old THOUGHT back, so the block would duplicate.
    Lines strictly inside the markers stay admitted; so does a range holding
    both markers when the new text brings a block. Whatever the range, the
    SPLICED body adds no block and no stray marker line: at most one block, or
    as many as the body already held (SM 112; SM 118: a body QUOTING a column-0
    pair beside its real block keeps a write path; hypothesis:body-replace-
    lands-at-most-one-well-formed-thought-and-row-name-skips-the-separator)."""
    lo, hi = _parse_range(rng)
    mark = node_writer.THOUGHT_MARKER_LINE_RE
    marks = [ln for ln in body.split("\n")[(lo or 1) - 1:hi] if mark.match(ln)]
    try:
        out = _splice_range(body, rng, new_text or "")
    except EditError as exc:
        return str(exc)

    def _shape(text: str) -> tuple[int, int]:   # (blocks, marker lines outside a block)
        n = len(node_writer.thought_blocks(text))
        return n, sum(bool(mark.match(ln)) for ln in text.split("\n")) - 2 * n
    (was, was_stray), (now, stray) = _shape(body), _shape(out)
    if ((not marks or (len(marks) == 2 and node_writer._THOUGHT_RE.search(new_text or "")))
            and now <= max(1, was) and stray <= was_stray):
        return None
    return (f"body {rng} would leave the THOUGHT malformed (a marker line in the range, "
            f"a second block or a stray marker): rewrite it with the `thought` verb, "
            f"and replace only the lines around it")


def verb_sub(edit: Edit, spec: str) -> Edit:
    """`sub <old> => <new>` -- one literal occurrence."""
    text = spec.strip()
    target = ""
    if text.startswith("payload "):
        target, text = "payload", text[8:].strip()
    if " => " not in text:
        raise EditError(f"sub needs `sub <old> => <new>`, got {spec!r}")
    old, new = text.split(" => ", 1)
    if not old:
        raise EditError("sub `<old>` is empty -- nothing written")
    edit.sub_ops.append((target, old, new, False))
    if target == "payload":
        edit.payload_verbs.append("sub payload")
    edit.sub_target, edit.sub_old, edit.sub_new = target, old, new
    return edit


def verb_sub_bang(edit: Edit, spec: str) -> Edit:
    """`sub!` -- every occurrence, count printed."""
    verb_sub(edit, spec)
    edit.sub_all = True
    _t, _o, _n, _a = edit.sub_ops[-1]
    edit.sub_ops[-1] = (_t, _o, _n, True)
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
    edit.payload_verbs.append("payload")
    return edit


VERBS = {
    "set": verb_set,
    "sub": verb_sub,
    "sub!": verb_sub_bang,
    "unset": verb_unset,
    "link": verb_link,
    "thought": verb_thought,
    "note": verb_note,
    "payload": verb_payload,
    "canonicalize": verb_canonicalize,
    "payload_text": verb_payload_text,
    "patch": verb_patch,
    "body_patch": verb_body_patch,
    "read": verb_read,
    "replace": verb_replace,
    "row": verb_row,
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
         "sub": 1, "sub!": 1,
         "payload": 1, "payload_text": 1, "patch": 1, "body_patch": 1,
         "read": 2, "replace": 3, "row": 2, "adopt": 0, "canonicalize": 0}
#: hypothesis:l5-write-py-splits-a-script-only-at-an-ampersand-pair-that-
#: begins-a-verb -- a `&&` separates chunks ONLY when what follows, stripped,
#: is a known verb name ending at whitespace or end-of-string; any other `&&`
#: stays in the current verb's last free-text argument. The literal
#: `str.split("&&")` this replaces split inside an argument too, and leaked
#: prose in a note/ref field crashed `links.py links` (experiment:a00-794503d4).
#: Residual (test-pinned): prose cannot quote a VERB-LED command UNLESS it
#: escapes the pair: `\&&` is carried byte-for-byte (backslash consumed) while
#: an unescaped verb-led `&&` still splits.
#: A trailing `&&` (nothing but whitespace after it) is still a separator --
#: otherwise it leaks into the last argument and verb-only scripts change.
#: So is a pair that closes a verb name with no space: `-&&adopt&&`.
#: A DOUBLED pair (`&&&&`) is its own separator, so it parses exactly as the
#: pre-verb-led `str.split("&&")` did (the empty middle chunk is skipped).
_ESC_AMP = "\x00esc-amp\x00"
_VERB_SEP = re.compile(r"\s*(?:&&){2,}\s*|\s*&&\s*(?=(?:%s)(?:\s|$|&&)|$)"
                       % "|".join(sorted(VERBS, key=len, reverse=True)))

#: One-line example per verb, for the help epilog. Module-level (not local to
#: main) so a test can assert each example PARSES as its verb's arity via the
#: shared `parse_script` -- the drift guard that completes the epilog check
#: (hypothesis:l4-the-carve-out-refuses-a-non-dict-template-and-keys-on-the-
#: resolved-seat). The `set` example is `set key value` (TWO arguments), never
#: `set k=v`; the parser splits `k=v` as one token and the grammar the epilog
#: teaches would be refused.
VERB_EXAMPLES = {
    "set": "set key value",
    "sub": "sub old => new",
    "sub!": "sub! old => new",
    "unset": "unset frontmatter_key",
    "link": "link self",
    "thought": "thought why this version differs",
    "note": "note a whole sentence, spaces absorbed",
    "payload": "payload path/to/source.py",
    "payload_text": "payload_text literal text body",
    "patch": "patch -",
    "body_patch": "body_patch -",
    "read": "read body 4:9",
    #: Standalone at submit(): it cannot ride the same script line as
    #: note/thought/body_patch (one body writer per submit). The rendered
    #: NOTES block below carries that rule into `-h`.
    "replace": "replace body 4:9 path/to/file",
    "row": "row 3 f  |  row 2:1-3 f  |  row name:<NAME> f  |  row manifest.<key> value.yaml|--remove",
    "adopt": "adopt",
    "canonicalize": "canonicalize",
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
    for chunk in _VERB_SEP.split(str(text).replace(r"\&&", _ESC_AMP)):
        stripped = chunk.strip().replace(_ESC_AMP, "&&")
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


def _town_cell_refusal(root, schema, set_fm, unset_fm, where: str):
    """goal:g15.25 SM.32 claim (3): a row write that CHANGES the `town` cell
    is judged on the NEW value alone -- a value outside the accepted set is
    refused WHOLE, BY NAME, and `all` is retired from the vocabulary. A row
    still spelling `town: all` stays readable: an untouched cell is never
    judged, so an unrelated write (session_name, pid, ...) is not refused.

    The declaration is the `[config]` schema's `town_cell` block (field,
    match_key, list_keys); the accepted set and the transitional row -> town
    map live there as DATA, never as a literal town name in this module
    (test_no_literal_town.py). Returns None when the write does not touch the
    cell or the schema declares no `town_cell`.
    """
    tc = schema.frontmatter.get("town_cell")
    if not isinstance(tc, dict):
        return None
    field = str(tc.get("field") or "town")
    match_key = str(tc.get("match_key") or "name")
    rows = None
    for k in (tc.get("list_keys") or ["posts", "seats"]):
        if isinstance(set_fm, dict) and k in set_fm:
            rows = set_fm[k]
            break
    if not isinstance(rows, list):
        return None
    try:
        import towns as _towns
        accepted = _towns.accepted_towns(root)
    except Exception:  # noqa: BLE001 (an unreadable vocabulary gates nothing)
        return None
    try:
        old_by = {r.get(match_key): r for r in _load_seats(root)
                  if isinstance(r, dict)}
    except Exception:  # noqa: BLE001
        old_by = {}
    for r in rows:
        if not isinstance(r, dict):
            continue
        name = r.get(match_key)
        if (old_by.get(name) or {}).get(field) == r.get(field):
            continue  # cell untouched by this write -> never judged
        val = r.get(field)
        if val not in accepted:
            return (f"`{field}` {val!r} on row {name!r} is refused BY NAME; "
                    f"the accepted town vocabulary is "
                    f"{', '.join(sorted(accepted))} (goal:g15.25)")
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


def _actor_rows_refusal(root, schema, actor, set_fm, unset_fm, where: str):
    """Resolve EVERY `actor_rows:` entry for the actor's RESOLVED seat. A
    `list_key` entry grants its row list (fields/ops/deny_roles), a `field`
    entry one top-level cell. "" = admitted, None = no entry applies, else a
    refusal naming the reason. Old rows come from the post-first geometry
    resolver, never a hardcoded file name."""
    entries = schema.frontmatter.get("actor_rows")
    if not isinstance(entries, list):
        return None
    seat = _resolve_seat(root, actor)
    if seat is None:
        return None
    for entry in entries:
        if (not isinstance(entry, dict)
                or str(entry.get("actor") or "") != seat):
            continue
        key, mk = entry.get("list_key"), entry.get("match_key")
        if key and mk:
            # (SM.108 defect 2) A grant on a row list grants ONLY that list: a
            # chained edit that also touches any other top-level key is refused
            # whole, exactly as `self_row` refuses `touched_top - {list_key}`.
            bad_top = (set(set_fm or {}) | set(unset_fm or {})) - {key}
            if bad_top:
                return (f"the actor grant on `{key}` may write ONLY that "
                        f"list (touched top-level field(s) "
                        f"{', '.join(sorted(bad_top))}); those declarations "
                        "are outside the grant")
            if key not in (set_fm or {}):
                continue
            rows = set_fm[key]
            if not isinstance(rows, list):
                return f"`{key}` must be a list of rows, got {type(rows).__name__}"
            _, resolved = geometry_config.resolve(root)
            old = (_load_seats(root) if key in (resolved, "posts", "seats")
                   else (_read_node_fm(root, where) or {}).get(key))
            old = old if isinstance(old, list) else []
            old_by = {r.get(mk): r for r in old if isinstance(r, dict)}
            new_by = {r.get(mk): r for r in rows if isinstance(r, dict)}
            # SM.115 + SM.115b: the actor's OWN row is co-governed by
            # `self_row`. A field the type's `self_row` declares (its identity
            # cells) is not THIS grant's to refuse, so it is exempted
            # FIELD-LEVEL below; every other own-row field still goes through
            # the grant's `fields` check, and non-self_row fields (town, ...)
            # stay admitted exactly as on any other row.
            _sr = schema.frontmatter.get("self_row")
            self_row_fields = ([str(f) for f in (_sr.get("fields") or [])]
                               if isinstance(_sr, dict) else [])
            fields = [str(f) for f in (entry.get("fields") or [])]
            ops = [str(o) for o in (entry.get("ops") or ["set"])]
            deny = [str(r) for r in (entry.get("deny_roles") or [])]
            for name in list(old_by) + [n for n in new_by if n not in old_by]:
                o, n = old_by.get(name), new_by.get(name)
                if o == n:
                    continue
                if str(name) in deny:
                    return f"row {name!r} is in deny_roles {deny} on `{key}`"
                op = "set" if o is not None and n is not None else (
                    "retire" if n is None else "create")
                if op not in ops:
                    return f"op {op!r} is not granted on `{key}` (ops {ops})"
                if op in ("set", "create"):
                    # (SM.108 defect 4) a CREATE row is field-checked exactly
                    # like a SET row: every key on a brand-new row except
                    # `match_key` must be in the grant's `fields`.
                    old_r = o or {}
                    for f in set(old_r) | set(n):
                        if (f != mk and old_r.get(f) != n.get(f)
                                and f not in fields
                                and not (str(name) == seat
                                         and f in self_row_fields)):
                            return (f"field {f!r} is not granted on `{key}` "
                                    f"rows (fields {fields})")
            return ""
        if entry.get("field"):
            if not (set_fm or unset_fm):
                continue
            field = str(entry["field"])
            touched = set(set_fm or {}) | set(unset_fm or [])
            if touched - {field} or field not in set_fm:
                return (f"the actor grant sets only the `{field}` field; "
                        f"this write touches "
                        f"{', '.join(sorted(touched)) or 'nothing'}")
            return ""
        # (SM.108 defect 3) the actor MATCHED but the entry's shape is one
        # this resolver does not read (no list_key+match_key, no field) --
        # refuse BY NAME rather than silently falling through to "no entry
        # applies". A no-op write is left to the caller's written_by refusal.
        if set_fm or unset_fm:
            return (f"actor_rows entry for {seat!r} declares no shape this "
                    f"resolver reads (need list_key+match_key or field; "
                    f"entry keys {sorted(entry)})")
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


#: The RESERVED key under which a config-write decision names its node id.
#: Prefixed with `_` and REFUSED BY NAME if a caller tries to write it, so a
#: ``set_fm``/``unset_fm`` key can NEVER displace the node the quorum
#: authorises (defect 2 of hypothesis:l4-canonical-bytes-are-injective-and-
#: fresh-and-the-ring-gates-the-write-itself: the id under a caller-mutable
#: ``node`` key meant one signature authorised removing ANY key from X).
NODE_KEY = "_node"

#: The removed-marker an UNSET key carries in the signed decision, so a
#: signature authorising "unset k" is DISTINCT in the bytes from one
#: authorising "set k: <value>" (defect 1: the quorum must cover the keys
#: being REMOVED, not the set keys alone -- an unset-only edit previously
#: demanded a quorum whose bytes covered nothing).
UNSET_MARKER = "<unset>"


def _config_write_fields(where, set_fm=None, unset_fm=None, *, ts=None,
                         nonce=None):
    """The FULL config-write decision fields a ring's signatures cover: the
    node id (under the reserved NODE_KEY a caller's set_fm can never dispose)
    AND every key being set AND every key being unset, each value
    string-serialized by rings.json_field (an unset key carries UNSET_MARKER,
    so "unset k" is distinct in the bytes from "set k: <value>"). The sign
    side, the gate, and the persisted record all use these same bytes.
    FRESH (kid B): the returned dict carries the reserved ``_fresh``
    (ts|nonce) so a persisted config-write quorum does NOT replay across
    time; ts/nonce default to freshly minted, pass them to fix the bytes the
    signer covered (fixtures do)."""
    from seatsig import rings as _rings  # noqa: PLC0415
    # RUNG 2b residues: refuse a caller key that would collide with the
    # reserved FRESH field, and a key present in BOTH set_fm and unset_fm,
    # BEFORE anything is signed, so every WRITTEN value is covered by the
    # quorum's signed bytes (hypothesis:l4-a-signed-decision-covers-every-
    # written-key-and-a-nonce-is-never-spent-on-a-failed-write).
    if _rings.FRESH_KEY in (set_fm or {}):
        raise EditError(
            f"config-row write to {where}: the reserved freshness key "
            f"{_rings.FRESH_KEY!r} (which carries the ts|nonce a ring "
            f"quorum covers) is REFUSED as a set field so it cannot displace "
            f"a written value from the signed bytes (RUNG 2b residue)")
    overlap = [k for k in (unset_fm or []) if k in (set_fm or {})]
    if overlap:
        raise EditError(
            f"config-row write to {where}: the key {overlap[0]!r} appears in "
            f"BOTH set_fm and unset_fm; REFUSED by name so the quorum never "
            f"signs one value while the write applies another (RUNG 2b "
            f"residue)")
    fields = {NODE_KEY: _rings.json_field(where)}  # _node: never displaced
    for k in (set_fm or {}):
        if k == NODE_KEY:
            raise EditError(
                f"config-row write to {where}: the reserved decision key "
                f"{NODE_KEY!r} (the node id a ring quorum authorises) is "
                f"REFUSED as a set field so a caller's key cannot name a "
                f"different node (defect 2, hypothesis:l4-canonical-bytes-are-"
                f"injective-and-fresh-and-the-ring-gates-the-write-itself)")
        fields[k] = _rings.json_field(set_fm[k])
    for k in (unset_fm or []):
        if k == NODE_KEY:
            raise EditError(
                f"config-row write to {where}: the reserved decision key "
                f"{NODE_KEY!r} is REFUSED as an unset key (defect 2, "
                f"hypothesis:l4-canonical-bytes-are-injective-and-fresh-and-"
                f"the-ring-gates-the-write-itself)")
        if k == _rings.FRESH_KEY:
            raise EditError(
                f"config-row write to {where}: the reserved freshness key "
                f"{_rings.FRESH_KEY!r} is REFUSED as an unset key so it cannot "
                f"displace the ts|nonce a ring quorum covers (RUNG 2b residue)")
        fields[k] = _rings.json_field(UNSET_MARKER)
    return _rings.fresh_fields(fields, ts=ts, nonce=nonce)


def _self_row_edit(schema, root, actor, where, set_fm, unset_fm,
                   allow_self_row: bool) -> bool:
    """True when this config-row write IS the writer's own self_row edit.

    Mirrors the L4.110 prime ruling B carve-out (the SAME ``self_row``
    declaration and refusal evaluation the write path later applies): a
    SEATED writer updating its OWN declared row and only the declared fields
    -- NEVER a gated act, even while the prime scope is FROZEN (defect 4,
    hypothesis:l4-...gate-sits-on-the-merge-up-push). Duplicated as a
    predicate so the human-gate check can exclude it; the actual permission
    still lives in the self_row carve-out below. Returns False for a `create`
    (``allow_self_row`` is submit-only), for a node whose schema declares no
    ``self_row``, for an unresolved/absent actor, and for a write that touches
    a row/field outside the declaration (the refusal is then gated like any
    foreign config-row write)."""
    if not allow_self_row:
        return False
    if not (set_fm or unset_fm):
        return False
    if not isinstance(schema.frontmatter.get("self_row"), dict):
        return False
    if _resolve_seat(root, actor) is None:
        return False
    try:
        refusal = _self_row_refusal(root, schema, actor, set_fm, unset_fm,
                                    where)
    except Exception:  # noqa: BLE001 (a broken refusal never silently un-gates)
        return False
    return refusal is None


def _preview_dry_run_gate(root, edit, args):
    """The `--dry-run` RING-GATE PREVIEW (hypothesis:l4-a-signed-decision-
    covers-every-written-key-and-a-nonce-is-never-spent-on-a-failed-write,
    clause 6): after resolving the edit, run the SAME written_by / ring /
    freshness judgement the real gate runs in submit -- same
    `_config_write_fields`, same `rings.verify_ring`, same
    `rings.freshness_refusal`, honouring `--ring-sig` and `--ring-fresh` --
    and print what it WOULD do. A pure no-op on state: writes nothing, stamps
    no editor, spends no nonce (`preview` -> remember=None). Without this a
    dry run of a write the gate would refuse (short of quorum, stale, or
    replayed nonce) printed as if it would succeed."""
    from seatsig import rings as _pr  # noqa: PLC0415
    _prev: dict = {}
    try:
        _pfresh = _pr.parse_ring_fresh(args.ring_fresh)
    except ValueError as _pve:
        print(f"ERR: {_pve}", file=sys.stderr)
        return 2
    try:
        _enforce_written_by(
            root, edit.node_id.split(":", 1)[0], args.actor, edit.node_id,
            args.role,
            set_fm=edit.set_fm or None,
            unset_fm=edit.unset_fm or None,
            allow_self_row=True,
            has_body=bool(edit.body_append or edit.thought
                          or edit.body_patch_diff
                          or edit.sub_body
                          or edit.replace_target == "body"),
            signatures=args.ring_sigs,
            out_decision=_prev,
            ring_fresh=_pfresh,
            preview=True)
    except Exception as _pe:  # noqa: BLE001  (a preview never masks the summary)
        _prev["refusal"] = f"{_pe}"
    if _prev.get("refusal"):
        print(f"  RING-GATE PREVIEW: {_prev['refusal']}")
    else:
        print("  RING-GATE PREVIEW: admitted (written_by + ring quorum + "
              "freshness satisfied); dry-run writes nothing")
    return 0


def _refuse(out_decision, preview, msg):
    """Raise a gate refusal in a REAL write; in a DRY-RUN preview, record it
    on ``out_decision['refusal']`` and return True instead (the caller returns).
    ONE message string shared by both paths, so a preview prints exactly the
    text the real gate would raise -- and a dry run writes nothing, stamps no
    editor, and spends no nonce (hypothesis:l4-a-signed-decision-covers-every-
    written-key-and-a-nonce-is-never-spent-on-a-failed-write, clause 6)."""
    if preview:
        out_decision["refusal"] = msg
        return True
    raise EditError(msg)


def _enforce_written_by(root, node_type, actor, where, role: str = "",
                        set_fm: dict | None = None,
                        unset_fm: list | None = None,
                        allow_self_row: bool = False,
                        has_body: bool = False,
                        signatures: list | None = None,
                        out_decision: dict | None = None,
                        ring_fresh: tuple | None = None,
                        preview: bool = False):
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

    # goal:g15.25 SM.32 claim (3): the row `town` cell is a declared
    # vocabulary -- a write that CHANGES it to a value outside the accepted
    # set is refused WHOLE, BY NAME (the schema's `town_cell` declaration;
    # the accepted set is the ladder's towns plus `core`).
    _tcr = _town_cell_refusal(root, schema, set_fm, unset_fm, where)
    if _tcr and _refuse(out_decision, preview,
                        f"{node_type} nodes ({where}): {_tcr}"):
        return

    # RUNG 3 HUMAN GATE (hypothesis:l4-a-veto-freezes-never-frees): a
    # config-row edit OUTSIDE self_row is a GATED Prime-scope act. While a
    # council+Keep veto (or an owner-written human_gate) shows the scope
    # FROZEN in the vetoes geometry node, the edit WAITS -- refused by name.
    # Checked FIRST so a frozen scope refuses even an otherwise-admitted
    # writer, and it is never auto-released; only an owner answer clears it.
    #
    # DEFECT 4 (hypothesis:l4-...gate-sits-on-the-merge-up-push): this gate
    # previously fired on EVERY submit -- ``set_fm``/``unset_fm`` are non-None
    # dicts from ``_config_write_fields`` on every config-row submission, so
    # a writer's OWN self_row write was gated too and ``key:``-only empties
    # gated even a no-op. It now fires ONLY for a config-row write OUTSIDE
    # the writer's OWN self_row: BOTH ``set_fm`` and ``unset_fm`` empty => no
    # gate, and a self_row write (the writer updating its own declared row /
    # fields) is NEVER gated.
    if (set_fm or unset_fm) and not _self_row_edit(schema, root, actor, where,
                                                   set_fm, unset_fm,
                                                   allow_self_row):
        try:
            from seatsig import veto as _veto

            _frozen, _why = _veto.is_frozen(root, "prime")
        except Exception:  # noqa: BLE001  (a broken veto cell never frees-silent)
            _frozen, _why = False, ""
        if _frozen:
            if _refuse(out_decision, preview,
                       f"{node_type} nodes ({where}): a config-row edit "
                       f"outside self_row is a gated act and {_why} "
                       f"(human gate, rung 3)"):
                return

    admitted = links.parse_written_by(written_by) if written_by is not None else None
    resolved = _resolve_role(root, actor, role)

    # CLAUSE 4 (hypothesis:l4-a-signed-decision-covers-every-written-key-and-
    # a-nonce-is-never-spent-on-a-failed-write): a `written_by` that is
    # DECLARED but EMPTY (`written_by: []` or `written_by: ""`) gates the type
    # to a writer set with nothing in it, so NO role is ever admitted. Refuse
    # BY NAME with the empty-list reason -- without this the final written_by
    # refusal below would read "admitted roles ;" as if roles were admitted.
    # An ABSENT written_by (admitted None) still gates nothing, unchanged; and
    # this REFUSES BEFORE the self_row / master_sensei carve-outs, because an
    # empty gate admits nobody regardless of a carved-out row on the same type.
    if admitted is not None and not admitted:
        if _refuse(out_decision, preview,
                   f"{node_type} nodes ({where}): the schema declares "
                   f"`written_by:` but the declared list is EMPTY, so no role "
                   f"may hand-edit them. (goal:g12)"):
            return

    # ------------------------------------------------------ GATE 1: written_by
    # The schema's OWN restricted-writer rule. An UNRESOLVED identity refuses
    # only because the type declares `written_by`; a schema declaring nothing
    # (admitted None) gates nothing here. A writer this gate does NOT admit is
    # REFUSED BEYOND THIS POINT -- a later satisfied ring quorum is never an
    # OR substitute for written_by (hypothesis:l4-canonical-bytes-are-
    # injective-and-fresh-and-the-ring-gates-the-write-itself, defect 3: the
    # two gates are an AND, so an unadmitted writer with a valid quorum is
    # still refused by name, and an ADMITTED writer still must satisfy the
    # ring when the schema declares one -- gate 2 below).
    if admitted is not None and resolved not in admitted:
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
                    if _refuse(out_decision, preview,
                               f"{node_type} nodes ({where}): a master-sensei "
                               f"write is limited to the declared template "
                               f"regions and must pass the startup producing "
                               f"judge; {mrefusal} "
                               f"(PRIME RULING 2026-09-11)"):
                        return
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

        # GENERIC `actor_rows:` carve-out (hypothesis:l4-the-formation-owner-
        # writes-config-posts-rows-...): the schema declares as a LIST which
        # RESOLVED seats may write which row list or single field -- a future
        # grant is ONE schema line, never a new branch here.
        if schema.frontmatter.get("actor_rows"):
            _ar = _actor_rows_refusal(root, schema, actor, set_fm, unset_fm, where)
            if _ar == "":
                return
            if _ar is not None and _refuse(
                    out_decision, preview,
                    f"{node_type} nodes ({where}): the actor_rows grant does "
                    f"not cover this write; {_ar} (schema-declared actor_rows)"):
                return

        # L4.110 prime ruling B carve-out: a SEATED role (a director on a seat,
        # say) is not in `written_by` and yet may update ONE thing — its own seat
        # row, restricted to the fields the type's `self_row` declaration names.
        # This is the only unadmitted-writer path; without the schema declaring
        # `self_row`, or for a `create`, the refusal below holds exactly as
        # before. `allow_self_row` is True only for `submit` (an edit); `create`
        # never admits a seated writer to mint a config node. The self_row path
        # DOES NOT need the ring quorum (test D ruling, hypothesis:l4-canonical-
        # bytes-are-injective-and-fresh-and-the-ring-gates-the-write-itself): a
        # seat may always update its OWN declared row fields, gate 2 is for
        # non-self-row config writes.
        if allow_self_row and (set_fm is not None or unset_fm is not None):
            sr = schema.frontmatter.get("self_row")
            if isinstance(sr, dict) and _resolve_seat(root, actor) is not None:
                refusal = _self_row_refusal(root, schema, actor, set_fm,
                                            unset_fm, where)
                if refusal is None:
                    return
                if _refuse(out_decision, preview,
                           f"{node_type} nodes ({where}): a seated role may "
                           f"update only its OWN row and only the declared "
                           f"fields; {refusal}. "
                           f"(L4.110 prime ruling B)"):
                    return

        # Not admitted by written_by nor any carve-out: REFUSE BY NAME with the
        # admitted roles -- even with a satisfied ring quorum (test C: the
        # refusal here is the written_by line, never the ring line).
        if _refuse(out_decision, preview,
                   f"{node_type} nodes ({where}) may be hand-edited only by "
                   f"admitted roles {', '.join(sorted(admitted))}; resolution "
                   f"for actor {actor!r} gave {resolved or 'UNRESOLVED'}, "
                   f"which is not admitted. "
                   f"(goal:g12)"):
            return

    # ------------------------------------------------------------ GATE 2: ring
    # RUNG 2 ring gate (hypothesis:l4-a-ring-decision-carries-m-of-n-
    # signatures), now an ADDITIONAL gate on top of written_by (AND, defect 3):
    # a writer that passed gate 1 is STILL refused here when the schema
    # declares `ring: <name>` and the write is a config-row edit
    # (set_fm/unset_fm). OPT-IN: a schema declaring no `ring:` (or a ring the
    # geometry does not name) demands no quorum, and body-only / self-row
    # writes never reach here. The quorum is verified through the SAME seatsig
    # Scheme interface send.py uses (seatsig/rings.py), never the gate's own
    # crypto; a record short of m is REFUSED BY NAME with the m-of-n count.
    ring_name = schema.frontmatter.get("ring")
    if ring_name and (set_fm or unset_fm):
        try:
            from seatsig import rings as _rings

            rings_rows = _rings.load_rings(root)
            ring = _rings.ring_by_name(rings_rows, ring_name)
        except Exception:  # noqa: BLE001
            ring = None
        if ring is not None:
            # FRESH (kid B): the gate signs the SAME fresh decision a producer
            # signs (pin ts/nonce via ring_fresh, or mint fresh here once);
            # canonical + freshness + the persisted cell all share these bytes.
            # The decision covers set AND unset keys (defect 1: an unset-only
            # edit's signed bytes cover the keys being removed).
            fields = _config_write_fields(
                where, set_fm, unset_fm,
                ts=ring_fresh[0] if ring_fresh else None,
                nonce=ring_fresh[1] if ring_fresh else None)
            canonical = _rings.canonical_bytes("config-write", fields)
            res = _rings.verify_ring(
                ring, canonical, signatures or [],
                pubkey_for_post=_ring_pubkey_for_post(root))
            if not res.ok:
                if _refuse(out_decision, preview,
                           f"{node_type} nodes ({where}): {res.refused}. "
                           f"(rung 2 multisig ring)"):
                    return
            # FRESH (kid B): the quorum satisfied, so the decision must still
            # sit inside its replay window and not carry a spent nonce.
            seen, remember = _rings.nonce_ledger(root)
            if preview:
                # a dry run previews the freshness judgement but NEVER spends
                # the nonce: remember=None means freshness_refusal only reads
                # the seen set and never records the nonce it admits.
                remember = None
            try:
                fr = _rings.freshness_refusal(
                    fields,
                    max_age_s=_rings._effective_max_age_s(ring),
                    seen=seen, remember=remember)
            except (_rings.LedgerWriteError, _rings.LedgerReadError) as le:
                if _refuse(out_decision, preview,
                           f"{node_type} nodes ({where}): {le}. "
                           f"(rung 2 multisig ring)"):
                    return
                raise  # pragma: no cover -- _refuse raises in the real gate
            if fr:
                if _refuse(out_decision, preview,
                           f"{node_type} nodes ({where}): freshness {fr}. "
                           f"(rung 2 multisig ring)"):
                    return
            # RUNG 2 claim (2): hand the admitted config-write decision
            # (kind + signed fields + signatures) back to the caller so it
            # can be persisted onto the node the write sanctions -- a reader
            # then re-verifies m-of-n from disk, never argv.
            if out_decision is not None:
                out_decision["cell"] = _rings.decision_cell(
                    ring_name, "config-write", fields, signatures or [])

    # Admitted: the writer passed written_by (gate 1) and, when the schema
    # declared a ring for a config-row edit, the ring quorum (gate 2).
    return


def _matches_type(value, declared: str) -> bool:
    """`declared` is one `validation.types` spelling; `value` is already
    `_coerce`d. An unrecognised spelling gates nothing — only a caller that
    already knows `declared` is truthy calls this."""
    if declared == "int":
        return isinstance(value, int) and not isinstance(value, bool)
    if declared == "float":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if declared == "bool":
        return isinstance(value, bool)
    if declared == "list":
        return isinstance(value, list)
    if declared == "str":
        return isinstance(value, str)
    return True


def _schema_field_refusal(schema, node_type: str, key, value, *,
                          verb: str) -> str | None:
    """One row's schema check — the predicate `create --set` and `set` both
    call, so the two verbs judge a row identically instead of by two
    hand-kept copies (goal:g7.33.10 round B,
    hypothesis:write-py-set-is-schema-checked). Refuses BY NAME, never a
    traceback, on the first violation:

      1. the schema's field-level `refuse:` annotation;
      2. `validation.types[key]` (or, absent that, `fields[key].type`) is
         declared and `value`'s coerced Python type does not match it —
         int/float/list/bool/str, not just int;
      3. `validation.regex[key]` is declared and `value` does not fully
         match it.

    Required-ness is a separate concern this predicate does not own
    (create's own `required_nonempty` loop and `links.py schema` do) — a
    field the schema simply does not mention gates nothing.

    NO "undeclared field is refused" check — REMOVED (thought-master TMM.171,
    returned merge-up @0f08a9d3d8): a first version refused any `key` not in
    `fields:` or a hand-picked `_UNIVERSAL_FIELDS` allowlist, and TMM.171's
    measurement (a scratch-worktree --dry-run sweep) found 111 (type, field)
    pairs across 2,273 live node-fields sit in no schema's `fields:` at all —
    `experiment.production_lines` (461 live uses), `experiment.line_ceiling`
    (362), `goal.heading_level` (362), `hypothesis.verdict` (150),
    `hypothesis.ceiling` (98), `experiment.rebrief_answer`/`rebrief_request`
    (brief.py's own re-brief protocol, cli.py:842) among them — every one of
    which the gate refused on trunk's live graph. The schemas' `fields:`
    blocks are far less complete than the corpus's actual field usage; an
    allowlist maintained by hand cannot keep up with that gap, and refusing
    on it breaks routine protocol writes rather than catching typos. Dropped
    entirely rather than patched wider — the type/regex checks below stay,
    because those only fire on a field a schema explicitly typed or
    regex'd, a far smaller and more deliberate set.
    """
    fields = schema.fields or {}
    field = fields.get(key)
    if isinstance(field, dict) and field.get("refuse"):
        ground = str(field.get("refuse"))
        return (f"{verb} {node_type} refused by name: {key!r} is not a "
                f"settable cell — {ground} (schema field-level `refuse:`, "
                f"enforced generically)")
    validation = schema.frontmatter.get("validation") or {}
    declared = (validation.get("types") or {}).get(key)
    if declared is None and isinstance(field, dict):
        declared = field.get("type")
    if declared and not _matches_type(value, declared):
        article = "an" if declared[0] in "aeiou" else "a"
        return (f"{verb} {node_type} refused by name: {key!r} must be "
                f"{article} {declared} value, got {value!r} (schema declares "
                f"{key}: {declared})")
    pattern = (validation.get("regex") or {}).get(key)
    if pattern and (not isinstance(value, str)
                    or re.fullmatch(pattern, value) is None):
        return (f"{verb} {node_type} refused by name: {key!r} must match "
                f"{pattern!r}, got {value!r} (schema validation.regex)")
    # goal:g7.16.1.2.6 -- a list field's ITEM form (the park tag parked:<goal>)
    item = (validation.get("item_regex") or {}).get(key)
    for v in (value if item and isinstance(value, list) else []):
        if re.fullmatch(item, str(v)) is None:
            return (f"{verb} {node_type} refused by name: {key!r} item {v!r} must "
                    f"match {item!r} (schema validation.item_regex)")
    return None


#: Rows an answers FILE names for the mint itself, not as frontmatter.
_ANSWERS_RESERVED = frozenset({"type", "slug", "parents", "body", "payload"})

#: Rows the WRITER mints: `node_writer.write_node` builds id/mint_id/
#: next_edges/scaffold_hash and THEN `fm.update(extra_fm)` runs, so an answers
#: row or a `--set` naming one would overwrite the node's own identity. ONE
#: definition of that fact, in `node_writer` (the builder), imported here --
#: a second transcription is a second truth that can drift.
_ANSWERS_IDENTITY = frozenset(node_writer.MINTED_IDENTITY)

#: THE PRECEDENCE, ONCE, for the rows the environment also stamps: an explicit
#: `--set` > the answers file > the calling post's config:posts row > the
#: environment (`node_writer._stamp_env_fields`). The surviving choice is
#: re-stamped AFTER the mint, so nothing above the env rank is silently lost.
#: `edited_by` is absent: that row is create()'s own `--actor` provenance and
#: the post row has always lost to it.
_STAMP_ROWS = ("role", "town", "season", "thought_session")


def _refuse_authored_identity(key: str, source: str) -> str | None:
    """ONE check for BOTH create routes (an answers row and an argv `--set`):
    a row the writer MINTS is refused BY NAME, never overwritten."""
    if key in _ANSWERS_IDENTITY:
        return (f"create --{source} refused by name: {key!r} is MINTED by "
                f"node_writer ({', '.join(sorted(_ANSWERS_IDENTITY))}) and is "
                "never authorable")
    if key in node_writer.GATED_ROWS:
        return (f"create --{source} refused by name: {key!r} is judged by the spawn "
                "gate -- pass it as the create's type or --parent, never as a row")
    return None


def _read_answers_file(path: str):
    """ONE answers file -> (data, refusal). JSON, so an apostrophe, a backtick
    and `$(` need no shell quoting: no field value on this route passes
    through a shell-quoted argv (claim 1).

    PRECEDENCE (see `_STAMP_ROWS`): an explicit `--set` beats the file, the
    file beats the calling post's `config:posts` row, and that row beats the
    environment. A row NO caller may choose (`_ANSWERS_IDENTITY`) refuses by
    name here, not silently."""
    import json
    try:
        data = json.loads(Path(path).read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, ValueError) as exc:
        return None, f"--answers {path}: {exc}"
    if not isinstance(data, dict):
        return None, f"--answers {path}: wants ONE JSON object, got {data!r}"
    if not isinstance(data.get("body", ""), str):
        return None, f"--answers {path}: 'body' must be a string"
    # `parents` is consumed as `list(answers.get("parents"))`, so a STRING
    # (JSON "5" -> `['5']`, a real parent id CHAR-SPLIT) or a non-iterable
    # (`5`, `true`) either mints a garbage parent or raises a TypeError out of
    # the parser. Type-check it HERE, where every other row is checked, and
    # refuse BY NAME.
    parents = data.get("parents")
    if parents is not None and not (
            isinstance(parents, list)
            and all(isinstance(p, str) for p in parents)):
        return None, (f"--answers {path}: 'parents' must be a list of node-id "
                      f"strings, got {parents!r}")
    return data, None


def _post_stamp(root, actor: str) -> dict:
    """The CALLING post's `config:posts` row as frontmatter rows (claim 3).

    The row is selected by EXACT name equality with the actor that is running
    the mint (or, with no `--actor`, the post the environment names) — never
    by prefix, never "the last row", so another post's row can never stamp.
    Every value is READ from the row / the ladder cell; none is transcribed.
    An empty dict when no row matches: an unstamped node beats a wrong one.
    """
    name = (actor or "").strip() or (geometry_config.resolved_seat_env() or "")
    row = next((r for r in _load_seats(root) if r.get("name") == name), None)
    if not row:
        return {}
    import season
    try:
        current = int(season._get_current_season(root))
    except (TypeError, ValueError):
        current = None  # a corrupt ladder cell stamps nothing, never a bad row
    values = {"edited_by": str(row["name"]), "role": row.get("role"),
              "town": row.get("town"),
              "season": current,
              "thought_session": row.get("session_name")
              or row.get("session_id")}
    return {k: v for k, v in values.items() if v not in (None, "")}


def _answers_row_refusal(root, node_type: str, node_id: str, slug: str,
                         parents: list[str], set_fm: dict) -> str | None:
    """The ONE row validator the answers route runs — a thin WRAPPER, never a
    second copy: `_refuse_marker_value` + `_enforce_create_schema_gate` (which
    is `_schema_field_refusal` over every row) + the REQUIRED rows
    `node_writer.seed_required` cannot derive. Every name is read through the
    schema registry; a refusal writes NOTHING (claim 2)."""
    for key, value in set_fm.items():
        refusal = _refuse_marker_value(key, value)
        if refusal:
            return refusal
    refusal = _enforce_create_schema_gate(root, node_type, set_fm)
    if refusal:
        return refusal
    preview = dict(set_fm, id=node_id, type=node_type, mint_id="0" * 32,
                   parents=list(parents))
    missing = node_writer.seed_required(root, node_type, preview, slug)
    if missing:
        return (f"create --answers {node_id} refused by name: "
                + ", ".join(repr(k) for k in missing) + " required at mint "
                "and NOT in the answers file (schema validation.required)")
    return None


def _enforce_create_schema_gate(root, node_type: str, set_fm: dict) -> str | None:
    """The CREATE half of a schema's field-level refusal annotations.

    A node is born through `create`, and until this gate existed nothing on
    that path consulted the schema's field `refuse:` annotation — so a cell
    the loader bans at READ time (the town `branches:` cell, whose schema
    field carries `refuse: "DERIVED, never a cell …"`) could be WRITTEN by
    `create --set`, and only refused rounds later when a reader hit the node.
    This gate closes the gap: for any schema declaring a field-level
    `refuse:` OR a declared `int` type, `create --set` refuses BY NAME at
    mint — GENERICALLY, driven by the schema itself, never a town-shaped
    special case.

    Two rules, both data-driven:
      (1) a `--set <key>` where the schema's field `<key>` carries a `refuse:`
          annotation is refused by name, quoting the annotation's ground;
      (2) a `--set <key>` where the schema declares `<key>: int` but the
          value is not an integer (`season=abc`, `season=true`) is refused by
          name, never a traceback.
      (3) a field on the schema's `validation.required_nonempty` list that
          `--set` leaves EMPTY or ABSENT is refused by name. This is the
          schema-DECLARED own of goal:s31's missing-required warn-and-write:
          a scaffold is born valid and a READER refuses, so `validation.
          required` alone stays a SCHEMA-WARNING and the node is written — but
          a type that declares `required_nonempty` opts OUT of that for those
          specific fields and refuses at MINT (a town with no `visions` would
          otherwise be born only for `towns.load_towns` to refuse it at READ,
          the round's exact disproof). A schema declaring no such list keeps
          its current warn-and-write behaviour.

    Returns a ONE-LINE refusal or None when every `--set` value passes. A
    schema that does not exist, or a `set_fm` whose keys the schema does not
    declare, gates nothing (unknown keys fall through to the schema's own
    seed/validation machinery).
    """
    try:
        from schema_registry import load_schemas_from_dir
    except Exception:  # noqa: BLE001
        return None
    schemas_dir = Path(root) / "context" / "schemas"
    if not schemas_dir.is_dir():
        return None
    try:
        schema = load_schemas_from_dir(schemas_dir).get(node_type)
    except Exception:  # noqa: BLE001
        return None
    if schema is None:
        return None
    required_nonempty = ((schema.frontmatter.get("validation") or {})
                         .get("required_nonempty") or [])
    for key, value in set_fm.items():
        refusal = _schema_field_refusal(schema, node_type, key, value,
                                        verb="create")
        if refusal:
            return refusal
    for key in required_nonempty:
        if key not in set_fm:
            return (f"create {node_type} refused by name: {key!r} is required "
                    f"non-empty at mint and was NOT set — a node born without "
                    f"it would be refused at read (schema "
                    f"validation.required_nonempty)")
        v = set_fm[key]
        if v is None or (hasattr(v, "__len__") and len(v) == 0):
            return (f"create {node_type} refused by name: {key!r} is required "
                    f"non-empty at mint, got {v!r} (empty) — a node born with "
                    f"an empty {key} would be refused at read (schema "
                    f"validation.required_nonempty)")
    return None


def _enforce_set_schema_gate(root, node_type: str, set_fm: dict) -> str | None:
    """The SET half of goal:g7.33.10 round B — `create --set` has run
    `_enforce_create_schema_gate` since the town gate landed; an existing
    node's `set` consulted no schema at all until now (measured: an invented
    field, an out-of-regex `goal_id`/`status`, a non-float `confidence` and
    a raw string into a list-typed field all wrote clean, exit 0). Shares
    `_schema_field_refusal` with `create` so the two verbs judge a row
    identically. Returns a ONE-LINE refusal or None; a schema or key this
    predicate does not recognise gates nothing, exactly like the create
    gate — required-ness stays out of scope here too.
    """
    try:
        from schema_registry import load_schemas_from_dir
    except Exception:  # noqa: BLE001
        return None
    schemas_dir = Path(root) / "context" / "schemas"
    if not schemas_dir.is_dir():
        return None
    try:
        schema = load_schemas_from_dir(schemas_dir).get(node_type)
    except Exception:  # noqa: BLE001
        return None
    if schema is None:
        return None
    for key, value in set_fm.items():
        refusal = _schema_field_refusal(schema, node_type, key, value,
                                        verb="set")
        if refusal:
            return refusal
    return None


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
    if edit.replace_text or edit.replace_stdin_read:
        # Already resolved — by main() for its --dry-run preview, or by an
        # API caller that set the text directly. Never re-read: a second
        # stdin read for `-` would consume nothing and hang the caller.
        return
    if edit.replace_from == "-":
        # Same stdin contract as `payload -` / `patch -`: replacement text is
        # arbitrary content and cannot ride an `&&` script chunk.
        edit.replace_text = sys.stdin.read()
        edit.replace_stdin_read = True   # SM 132 probe: an EMPTY stdin is resolved too (a
        return                           # deliberate deletion, pinned) -- never read twice
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


def submit(root, edit: Edit, actor: str = "", session: str = "",
           role: str = "", ring_fresh: tuple | None = None,
           dry_run: bool = False) -> object:
    """Write the accumulated edit. **The only thing in this module that writes.**

    `dry_run` = THE preview judge (SM 130: the third preview/write drift): every
    refusal below runs, then it returns None just before the first write; the
    ring gate runs as its preview (no nonce spent, its refusal is the preview
    line `_preview_dry_run_gate` prints).

    Returns `node_writer`'s own result object, so a caller sees `UPDATED`,
    `UNCHANGED` or `REJECTED` and the reason — the same statuses every other
    writer path reports.
    """
    if edit.empty:
        raise EditError(f"nothing to submit for {edit.node_id}")

    # hypothesis:l4-write-api-root-resolution — an API caller's `root` is
    # resolved descend-only here, so a wrong root refuses before any write.
    root = _resolve_api_root(root)

    # conjunct 1: resolve `sub` BEFORE the outside-ref gate, on the API path
    # too; main already resolved it for its preview (idempotent).
    _resolve_sub(root, edit)
    if _stdin_refusal(edit):   # SM 117, for an API caller too
        raise EditError(_stdin_refusal(edit))
    _resolve_fm_row(root, edit)   # BUILD1, idempotent likewise
    _patch_the_node_itself(root, edit)   # goal:g4.18.1.6, idempotent: clears the patch it translates

    # A link_ref/payload_ref resolving outside the repo tree is refused before
    # any write; the SAME predicate links.py's schema report calls. It judges
    # the EFFECTIVE frontmatter: a value this edit SETS, else ABSENT when this
    # edit UNSETS the key, else what the node file already carries. Reading
    # only `set_fm` admitted a location-only move of an existing inside ref,
    # and falling back to the stale on-disk location over-refused an
    # `unset location` (hypothesis:write-py-outside-ref-gate-...).
    _on_disk: dict = {}
    if (_nf := node_writer.find_node_file(root, edit.node_id)):
        from graph_core.persistence import frontmatter as _fmr
        try:
            _on_disk = _fmr.load_node_file(_nf, body=False).frontmatter or {}
        except Exception:
            _on_disk = {}

    def _effective(key):
        if key in edit.set_fm:
            return edit.set_fm[key]
        if key in edit.unset_fm:
            return None
        return _on_disk.get(key)

    for _f in ("link_ref", "payload_ref"):
        if (_p := links.outside_repo_path(root, _effective(_f),
                                          _effective("location"))):
            raise EditError(
                f"cannot set {_f!r}: {_p} resolves outside the repo tree")

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
                                      or edit.sub_body
                                      or edit.replace_target == "body"),
                        signatures=getattr(edit, "signatures", []),
                        out_decision=_ring_out,
                        ring_fresh=ring_fresh, preview=dry_run)

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
    elif edit.sub_body:
        # sub touched the body with no note/thought riding along.
        body = edit.sub_body
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
        if _standalone_refusal(edit):
            raise EditError(_standalone_refusal(edit))
        body = apply_unified_diff(_read_body_text(root, edit.node_id),
                                  edit.body_patch_diff)

    # Everything that can refuse, refuses BEFORE anything is written: a
    # payload swap that lands next to a rejected node edit is a file whose
    # reason never made it into the graph, which is the exact split this verb
    # exists to close.
    if edit.patch_from == "-" and not edit.patch_diff:   # SM 139: refused BEFORE any write, dry and real
        raise EditError("patch - (stdin) is empty: no diff to apply -- nothing written")
    if edit.body_patch_from == "-" and not edit.body_patch_diff:   # SM 144: 139's sibling (an API caller sets the diff)
        raise EditError("body_patch - (stdin) is empty: no diff to apply -- nothing written")
    if edit.payload_from == "-":   # SM 140: main() reads stdin; `-` survives only an empty read
        raise EditError("payload - (stdin) is empty: no bytes to write -- nothing written")
    _writers = [bool(edit.payload_from), bool(edit.payload_bytes),
                bool(edit.patch_from or edit.patch_diff), edit.replace_target == "payload"]
    _verbs = edit.payload_verbs   # SM 145: repeated `sub payload` ops compose; any other pair drops one
    if sum(_writers) > 1 or len(set(_verbs)) > 1 or sum(v != "sub payload" for v in _verbs) > 1:
        raise EditError("one payload writer per submit: payload, payload_text, patch and "
                        "replace payload cannot share a line -- nothing written")
    touches_payload = any(_writers)
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
        if _standalone_refusal(edit):
            raise EditError(_standalone_refusal(edit))
        _current = _target_text(root, edit, edit.replace_target,
                                payload_ref, location)
        if edit.row_ref:   # goal:g4.18.5.1: the index picks the range
            edit.replace_range = _row_range(_current, edit.row_ref)
        if edit.replace_target == "body":
            _refusal = _thought_marker_refusal(_current, edit.replace_range, edit.replace_text)
            if _refusal:
                raise EditError(_refusal)
        # hypothesis:lm-replace-body-anchor-guards-against-mis-offset-
        # splices -- the body-only structural guard, before the splice and
        # before any write. A payload is arbitrary bytes and is never
        # structure-checked; `read body N:M` stays unguarded too.
        if edit.replace_target == "body" and not edit.replace_force:
            _refusal = _body_range_refusal(_current, edit.replace_range)
            if _refusal:
                raise EditError(
                    f"{_refusal} "
                    f"(hypothesis:lm-replace-body-anchor-guards-against-mis-"
                    f"offset-splices)")
        _spliced = _splice_range(_current, edit.replace_range,
                                 edit.replace_text)
        if edit.replace_target == "body":
            body = _spliced
        else:
            edit.payload_bytes = _spliced

    # hypothesis:every-write-py-path-is-schema-checked-not-only-the-set-verb
    # -- the schema gate for the LIBRARY path. main() runs the same predicate
    # (line ~3121) on the CLI, but submit() did not, so every engine caller
    # (rotate.py's list cells among them) wrote a value the schema refuses by
    # name: a `refuse:` annotation, a wrong type, a raw scalar into a
    # list-typed field, an out-of-regex value. The SAME one-line refusal, the
    # SAME row-and-rule naming, raised as an EditError before anything is
    # written -- so the API and the CLI cannot disagree about what a legal row
    # is. Only the caller's own `set_fm` is judged, exactly as on the CLI: the
    # provenance/ring cells submit() adds afterwards are its own bookkeeping.
    if edit.set_fm and ":" in edit.node_id:
        _refusal = _enforce_set_schema_gate(
            root, edit.node_id.split(":", 1)[0], edit.set_fm)
        if _refusal:
            raise EditError(_refusal)

    # A `location` set in this same edit wins over the one on disk: naming the
    # new base and moving the bytes is one intention, not two.
    if "location" in set_fm:
        location = set_fm["location"]

    # SM 142 + 143: every payload input resolves BEFORE the dry return -- the
    # destination exists, the source is a file and its bytes are read -- so
    # update_node is only ever followed by a payload write already known to
    # land. An EMPTY result (a patch deleting every line) is b"", never None.
    payload_data = None
    if payload_ref:
        _dest = locations.resolve_payload_path(Path(root), payload_ref, location)
        if not _dest.is_file():
            raise EditError(f"payload {_dest} does not exist -- `payload` replaces bytes, it never "
                            f"creates (a new file is `write.py create --payload`); nothing written")
        if edit.payload_from:
            if not Path(edit.payload_from).is_file():
                raise EditError(f"payload source {edit.payload_from} is not a file -- nothing written")
            try:
                payload_data = Path(edit.payload_from).read_bytes()
            except OSError as exc:   # SM 147: rc 2 + ERR, never a traceback
                raise EditError(f"payload source {edit.payload_from} cannot be read ({exc}) -- nothing written")
        else:
            payload_data = edit.payload_bytes.encode()
        if not os.access(_dest, os.R_OK):   # SM 148/149: replace_payload READS the dest first (same-bytes check)
            raise EditError(f"payload {_dest} is not readable -- nothing written")
        if not os.access(_dest, os.W_OK) and _dest.read_bytes() != payload_data:   # SM 146: replace_payload
            raise EditError(f"payload {_dest} is not writable -- nothing written")   # writes in place

    # PRIME RULING 2026-09-11 facts-region gate: a master-sensei BODY edit on
    # a `master_sensei_row`-governed node may change ONLY the `## facts`
    # section. Written here (post-composition) because the body bytes only
    # exist after the splice; `_enforce_written_by` admitted the writer on
    # the body-only path and this gate is the load-bearing confinement.
    _enforce_master_sensei_facts_body(root, edit.node_id, actor, body)

    # goal:g7.16.1.2.6 -- `set active` wakes that formation's parked nodes. The
    # carrier grep runs BEFORE the write and fails CLOSED (council C1 on bundle
    # 3, check_formation's stance): a grep that cannot look refuses the set,
    # nothing written -- never rc 0 with every carrier still parked.
    wake_goal, carriers = "", []
    if edit.node_id == "config:formations" and "active" in edit.set_fm:
        import rotation_record  # the shared carrier grep: write never imports the verifier
        from graph_core.persistence import frontmatter as _fmr
        cell = node_writer.find_node_file(root, "config:formations")
        # no cell -> no table -> no grep (the empty-goal path): residue 79
        table = (edit.set_fm["templates"] if "templates" in edit.set_fm else
                 (_fmr.load_node_file(cell, body=False).frontmatter.get("templates") if cell else None)) or {}
        wake_goal = str(table.get(edit.set_fm["active"]) or "")
        try:
            carriers = rotation_record.parked_carriers(root, wake_goal) if wake_goal else []
        except rotation_record.GrepError as exc:
            raise EditError(f"set active refused: the parked-carrier grep for parked:{wake_goal} "
                            f"failed ({exc}); nothing written -- the wake cannot be delivered")

    if dry_run:   # every refusal above has run; nothing is written
        return None
    res = node_writer.update_node(root, edit.node_id, set_fm=set_fm,
                                  unset_fm=edit.unset_fm, body=body,
                                  log_extra=_log_provenance(actor),
                                  canonicalize=edit.canonicalize)
    if payload_ref and res.status != node_writer.REJECTED:
        # hypothesis:l3-write-payload-unchanged-unlogged — a same-bytes re-log
        # is still a sanction. Hand the owning node's mint_id to
        # replace_payload so the payload-write log entry carries it, matching
        # write_guard's (mint_id, sha256) key even when the bytes did not
        # change.
        mint = _node_mint_id(root, edit.node_id)
        dest, changed = node_writer.replace_payload(
            root, payload_ref, None, location=location,
            data=payload_data,   # resolved above, before the dry return (SM 142/143)
            mint_id=mint,
            log_extra=_log_provenance(actor))
        res.payload_changed = changed
        res.payload_path = str(dest)
    # ... and, the set written, its `parked:<goal>` tag leaves every carrier found above.
    goal = wake_goal
    if res.status != node_writer.REJECTED:
        for nid, _f, tags in carriers:
            try:
                w = node_writer.update_node(root, nid, set_fm={
                    "tags": [t for t in tags if t != f"parked:{goal}"],
                    PROVENANCE_ACTOR: actor or _default_actor()}, log_extra=_log_provenance(actor))
            except OSError as exc:  # one carrier's failed write never aborts the rest
                w = node_writer.NodeWrite(status=node_writer.REJECTED, node_id=nid, reason=str(exc))
            print(f"unpark REJECTED {nid} (parked:{goal}): {w.reason}" if w.status == node_writer.REJECTED
                  else f"unparked {nid} (parked:{goal})", file=sys.stderr)
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


def _resolve_sub(root, edit: Edit) -> None:
    """Resolve every `sub` op, composing in order (conjunct 3)."""
    if edit.sub_resolved or not edit.sub_ops:
        return
    node_before = node_after = None
    payload_before = payload_after = None
    node_label = edit.node_id
    payload_label = ""
    total = 0
    for target, old, new, all_ in edit.sub_ops:
        if target == "payload":
            if payload_before is None:
                ref, loc = _payload_ref(root, edit)
                payload_before = payload_after = _read_payload_bytes(
                    root, ref, loc)
                payload_label = ref
            before, label = payload_after, payload_label
        else:
            if node_before is None:
                path = node_writer.find_node_file(root, edit.node_id)
                if path is None:
                    raise EditError(f"no node file for {edit.node_id}")
                node_before = node_after = path.read_text(encoding="utf-8")
            before, label = node_after, node_label
        n = before.count(old)
        if n == 0:
            raise EditError(f"sub: 0 occurrences of {old!r} in "
                            f"{label} -- nothing written")
        if not all_ and n != 1:
            raise EditError(f"sub: {n} occurrences of {old!r} in "
                            f"{label}; use sub! -- nothing written")
        after = before.replace(old, new, -1 if all_ else 1)
        total += n if all_ else 1
        if target == "payload":
            payload_after = after
        else:
            node_after = after
    if payload_after is not None:
        edit.payload_bytes = payload_after
    if node_after is not None:
        old_fm = frontmatter.read_frontmatter(node_before)
        new_fm = frontmatter.read_frontmatter(node_after)
        if not old_fm or new_fm is None or set(old_fm) != set(new_fm):
            raise EditError(f"sub would break frontmatter in {node_label} -- "
                            f"nothing written")
        if any(old_fm.get(k) != new_fm.get(k) for k in PROTECTED):
            raise EditError("sub cannot change id/mint_id/type/scaffold_hash "
                            "-- nothing written")
        changed = {k: v for k, v in new_fm.items()
                   if k not in PROTECTED and old_fm.get(k) != v}
        for k, v in changed.items():
            refusal = _refuse_marker_value(k, v)
            if refusal:
                raise EditError(refusal)
        edit.set_fm.update(changed)
        ob = frontmatter.split_frontmatter(node_before)[1]
        nb = frontmatter.split_frontmatter(node_after)[1]
        if nb != ob:
            edit.sub_body = nb
    edit.sub_count, edit.sub_resolved = total, True


# --------------------------------------------------------------------------
# The structural guard (hypothesis:lm-replace-body-anchor-guards-against-mis-
# offset-splices). `replace body N:M` is offset-free, but the RANGE is still
# chosen by hand: a range one line short of a section end splits a heading
# from its text and the write is silent. This guard catches exactly that
# class before `_splice_range` runs -- on the BODY only, because a payload is
# arbitrary bytes and a partial `read` must stay unguarded -- and always names
# `--force` plus the node id, so the refusal is an instruction, not a wall.
# --------------------------------------------------------------------------

_HEADING_RE = re.compile(r"^ {0,3}(#{1,6})(?:\s|$)")
_FENCE_RE = re.compile(r"^( {0,3})(`{3,}|~{3,})(.*)$")


def _is_heading(line: str) -> bool:
    """One strict CommonMark heading rule, shared by the whole guard."""
    return bool(_HEADING_RE.match(line))


def _heading_level(line: str) -> int:
    """The ATX heading level (1..6), or 0 for a non-heading line."""
    m = _HEADING_RE.match(line)
    return len(m.group(1)) if m else 0


def _fence_marker(line: str):
    """(char, length, info-string) of a CommonMark fence line, or None."""
    m = _FENCE_RE.match(line)
    return (m.group(2)[0], len(m.group(2)), m.group(3)) if m else None


def _guard_headings(lines: list[str]) -> list[bool]:
    """Per line: an ATX heading that is NOT inside a code fence.

    `# not a heading` inside ``` or ~~~ is code, and treating it as a
    heading truncates `_section_end`, admitting a replace-body range that
    cuts the fenced block in half (hypothesis:write-body-range-guard-is-
    fence-aware-and-clamped). Fences follow CommonMark: an opening run of
    three or more ``` or ~~~ (a backtick fence's info string may hold no
    backtick); it closes only on the SAME character, at least as long, with
    nothing but whitespace after it.
    """
    out = [False] * len(lines)
    fence = None
    for i, line in enumerate(lines):
        mark = _fence_marker(line)
        if fence is None:
            if mark and not (mark[0] == "`" and "`" in mark[2]):
                fence = mark[:2]
                continue
            out[i] = _is_heading(line)
        elif (mark and mark[0] == fence[0] and mark[1] >= fence[1]
              and not mark[2].strip()):
            fence = None
    return out


def _section_end(lines: list[str], idx: int) -> int:
    """The 0-based EXCLUSIVE end of the section headed by `lines[idx]`.

    The next line at the same-or-higher level OUTSIDE any code fence, or
    the end of the text. This is the guard's own rule for "where the
    heading's text stops", and the whole-section case is measured against
    it rather than guessed at.
    """
    head = _guard_headings(lines)
    level = _heading_level(lines[idx])
    j = idx + 1
    while j < len(lines):
        if head[j] and _heading_level(lines[j]) <= level:
            break
        j += 1
    return j


def _plain(line: str, heading: bool) -> bool:
    """A line that is neither blank nor a heading -- paragraph content."""
    return bool(line.strip()) and not heading


def _has_content(lines: list[str], a: int, b: int) -> bool:
    """Any non-blank line in the 0-based half-open `[a, b)`.

    Blank lines are not orphaned text, so a heading followed only by blanks
    may be a range's last line without refusing: the body always ends in a
    newline, and punishing that would be a false positive on the working
    case.
    """
    return any(ln.strip() for ln in lines[a:b])


def _body_range_refusal(text: str, rng: str) -> str | None:
    """The refusal text for a body range that splits structure, or None.

    Three shapes, each naming the offending line and the escape hatch:

    (a) the range STARTS strictly inside a paragraph;
    (b) the range ENDS strictly inside a paragraph;
    (c) the range STARTS on a heading but stops before the end of that
        heading's own section, orphaning non-blank text under it (only a
        BOUNDED upper bound can stop short -- `N:` runs to EOF and covers
        the section);
    (d) the range ENDS exactly on a heading -- `### A.1` -- whose own section
        still holds non-blank text: the heading is removed and its text
        survives, the same split from the other edge.

    The childless tail -- a section whose last line is a deeper heading with
    nothing under it -- matches none of the four and is ADMITTED, because
    that heading IS the correct end of the outer section (falsifier (c) of
    the hypothesis, measured on experiment:a00-29883877-7abb3b).
    """
    lo, hi = _parse_range(rng)
    lines = text.split("\n")
    n = len(lines)
    start = 0 if lo is None else lo - 1
    if hi is not None and hi > n:
        return (f"replace body {rng} ends past the end of the body at line "
                f"{n} -- the range overruns it. Cap the range at {n} or "
                f"pass --force")
    end = n if hi is None else hi
    if start >= n or end <= start:
        return None
    head = _guard_headings(lines)
    if start > 0 and _plain(lines[start], head[start]) \
            and _plain(lines[start - 1], head[start - 1]):
        return (f"replace body {rng} starts inside a paragraph at line "
                f"{start + 1} ({lines[start]!r}) -- it would cut the "
                f"paragraph in half. Widen the range to a blank line or a "
                f"heading, or pass --force")
    if end < n and _plain(lines[end - 1], head[end - 1]) \
            and _plain(lines[end], head[end]):
        return (f"replace body {rng} ends inside a paragraph at line {end} "
                f"({lines[end - 1]!r}) -- the rest of the paragraph would be "
                f"orphaned. Widen the range to a blank line or a heading, "
                f"or pass --force")
    if hi is not None and head[start]:
        sec = _section_end(lines, start)
        if end < sec and _has_content(lines, end, sec):
            return (f"replace body {rng} starts on the heading "
                    f"{lines[start]!r} but stops before the end of its "
                    f"section (line {sec}) -- that splits the heading from "
                    f"its text. Widen the range or pass --force")
    j = end - 1
    if head[j]:
        sec = _section_end(lines, j)
        if sec > j + 1 and _has_content(lines, j + 1, sec):
            return (f"replace body {rng} ends on the heading {lines[j]!r} "
                    f"-- the heading is removed while its text (line "
                    f"{j + 2}..{sec}) survives. Widen the range past its "
                    f"section or pass --force")
    return None


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

_NO_EOF_MARKER = "\\ No newline at end of file"


def _split_keepends(text: str) -> list[str]:
    """Split on a bare `\n` ONLY, keeping the newline on terminated lines.

    `str.splitlines(True)` also splits on `\r`, `\v`, `\f` and friends, which
    would corrupt a node whose bytes contain any of them. This is the one
    line-splitter `apply_unified_diff` and the diff renderer share, so the
    two halves agree on what a "line" is.
    """
    parts = text.split("\n")
    lines = [p + "\n" for p in parts[:-1]]
    if parts[-1]:
        lines.append(parts[-1])
    return lines


def _standard_unified_diff(before: str, after: str, *, fromfile: str,
                           tofile: str) -> str:
    """`difflib.unified_diff` rendered as a STANDARD unified diff.

    Both sides are compared keepends, so a missing EOF newline is a real line
    difference (exactly as GNU diff sees it), and every content line with no
    trailing newline is followed by the `\\ No newline at end of file` marker.
    The split("\n") representation instead models a missing EOF newline as a
    phantom empty trailing line, which GNU `patch` rejects (hypothesis:sub-
    dry-run-preview-is-the-bytes-update-node-lands).
    """
    out = []
    for line in difflib.unified_diff(
            _split_keepends(before), _split_keepends(after),
            fromfile=fromfile, tofile=tofile, lineterm="\n"):
        out.append(line)
        if not line.endswith("\n"):
            out.append("\n" + _NO_EOF_MARKER + "\n")
    return "".join(out)


def apply_unified_diff(original: str, diff: str) -> str:
    """Apply a unified diff to `original`, fail-closed, in memory.

    hypothesis:l3-write-partial-diffs-as-writes. Reads the grid's own diff
    vocabulary (what `git diff` / `difflib.unified_diff` emit): `---`/`+++`
    headers are optional, `@@` hunks carry body lines prefixed with space
    (context), `-` (removed) or `+` (added). A `\\ No newline at end of file`
    marker strips the trailing newline from the line before it, so a patch
    round-trips a file whose last line is unterminated -- the marker GNU
    `patch` emits and demands.

    **No partial application, ever.** Every context line and every removal is
    checked against the payload's current bytes; the first mismatch raises
    `EditError` and nothing is returned, so nothing is written. A hunk whose
    header is malformed, or body bytes that arrive outside any hunk, also
    refuse. The result is a single new string built entirely in memory.
    """
    orig = _split_keepends(original)
    diff_lines = diff.split("\n")
    if diff_lines and diff_lines[-1] == "":
        diff_lines = diff_lines[:-1]

    # --- Collect the hunks first, so a malformed diff refuses before any
    # state has been touched. Each body entry carries `has_nl`: the marker
    # line clears it on the entry it follows. ---
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
                if b == _NO_EOF_MARKER:
                    if not body:
                        raise EditError(
                            "no-newline marker with no preceding line")
                    action, content, _ = body[-1]
                    body[-1] = (action, content, False)
                    continue
                if not b:
                    body.append((" ", "", True))   # a context blank line
                    continue
                if b[0] not in "+- ":
                    raise EditError(f"bytes outside any hunk: {b!r}")
                body.append((b[0], b[1:], True))
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
        for action, content, has_nl in body:
            want = content + ("\n" if has_nl else "")
            if action == " ":
                if oi >= len(orig) or orig[oi] != want:
                    got = (repr(orig[oi]) if oi < len(orig) else "<EOF>")
                    raise EditError(
                        f"context mismatch at original line {oi + 1}: "
                        f"diff expects {want!r}, file has {got}")
                out.append(orig[oi])
                oi += 1
            elif action == "-":
                if oi >= len(orig) or orig[oi] != want:
                    got = (repr(orig[oi]) if oi < len(orig) else "<EOF>")
                    raise EditError(
                        f"removal mismatch at original line {oi + 1}: "
                        f"diff expects {want!r}, file has {got}")
                oi += 1
            else:                       # action == "+"
                out.append(want)
    while oi < len(orig):
        out.append(orig[oi])
        oi += 1
    return "".join(out)


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
            f"{edit.node_id} has no payload_ref: use `replace body N:M` (or "
            f"`row`) for the node file -- `payload` edits the file a build "
            f"node points at, and `patch` edits the node file itself "
            f"(council ruling on goal:g4.18.1.6)")
    loc = fm.get("location")
    return ref.strip(), loc.strip() if isinstance(loc, str) and loc.strip() else None


_CONTRACT_RE = re.compile(r"^<!--[ \t]*BUILD-CONTRACT:BEGIN\b.*?^<!--[ \t]*BUILD-CONTRACT:END[ \t]*-->",
                          re.DOTALL | re.MULTILINE)


def _patch_the_node_itself(root, edit: Edit) -> None:
    """goal:g4.18.1.6 (owner 09-30: "The node location just becomes the node
    itself."): a `patch` on a node with NO payload_ref applies to the node file
    and lands as the rows and body it changed -- through update_node and every
    gate after this call (ring, schema, THOUGHT carry, provenance). A build
    node keeps patching its payload. Identity rows, a BUILD-CONTRACT block and
    the THOUGHT markers refuse by name; so does another verb on the same line."""
    if not (edit.patch_from or edit.patch_diff):
        return
    path = node_writer.find_node_file(root, edit.node_id)
    if path is None or path.suffix != ".md":
        return
    from graph_core.persistence import frontmatter as _fmr
    old = _fmr.load_node_file(path)
    if old.frontmatter.get("payload_ref") or old.frontmatter.get(links.LINK_FIELD):
        return
    if edit.payload_verbs != ["patch"] or edit.set_fm or edit.unset_fm or edit.body_append or edit.thought \
            or edit.body_patch_from or edit.body_patch_diff or edit.replace_target or edit.sub_ops:
        raise EditError(f"{edit.node_id} has no payload_ref, so `patch` edits the node file itself "
                        f"and is standalone: no other verb on its line -- nothing written")
    if edit.patch_from == "-" and not edit.patch_diff:
        return   # SM 139 refuses it by name below
    try:   # SM 153: a bad source or a patch that breaks the frontmatter is an ERR, never a traceback
        diff = edit.patch_diff or Path(edit.patch_from).read_text(encoding="utf-8")
        applied = apply_unified_diff(path.read_text(encoding="utf-8"), diff)
        new = _fmr._parse_md(applied, ".md", True)
    except (OSError, UnicodeDecodeError, _fmr.FrontmatterError) as exc:
        raise EditError(f"patch on {edit.node_id} cannot apply: {exc} -- nothing written")
    ofm, nfm = old.frontmatter, new.frontmatter
    for k in sorted(set(ofm) | set(nfm)):   # SM 150: every row `set`/`unset` would judge, judged alike
        if ofm.get(k) != nfm.get(k) or (k in ofm) != (k in nfm):
            refusal = _row_refusal(k, nfm.get(k)) if k in nfm else (
                f"{k!r} may not be unset — see `set`." if k in PROTECTED else None)
            if refusal:
                raise EditError(f"patch: {refusal}")
    if _CONTRACT_RE.findall(old.body) != _CONTRACT_RE.findall(new.body):
        raise EditError("patch touches the BUILD-CONTRACT block, which is regenerated -- nothing written")
    def _stray(b):   # marker lines outside a well-formed block (_thought_marker_refusal's shape)
        return sum(bool(node_writer.THOUGHT_MARKER_LINE_RE.match(ln)) for ln in b.split("\n")) \
            - 2 * len(node_writer.thought_blocks(b))
    ob, nb = len(node_writer.thought_blocks(old.body)), len(node_writer.thought_blocks(new.body))
    if _stray(new.body) > _stray(old.body) or nb > max(1, ob) or nb < ob:   # SM 152: never a 2nd block
        raise EditError("patch would leave the THOUGHT malformed: rewrite it with the `thought` verb -- nothing written")
    canon = node_writer._serialize_node(node_writer.render_frontmatter(nfm), new.body)
    if canon != applied:   # council ruling on SM 154: one serializer, fail-closed, never a silent discard
        drift = [ln for ln in difflib.unified_diff(applied.split("\n"), canon.split("\n"), lineterm="", n=0)
                 if ln[:1] in "+-" and ln[:3] not in ("+++", "---")][:4]
        raise EditError(f"patch result is not in the canonical form, so it would not land as written "
                        f"(re-render: {drift}): run `write.py {edit.node_id} canonicalize` first, then "
                        f"re-cut the diff -- the canonical form drops frontmatter comments and "
                        f"non-significant quoting; nothing written")
    edit.set_fm.update({k: v for k, v in nfm.items() if ofm.get(k) != v})
    edit.unset_fm.extend(k for k in ofm if k not in nfm)
    if new.body != old.body:
        edit.sub_body = new.body   # the body writer update_node already takes (sub's slot)
    edit.patch_from, edit.patch_diff, edit.payload_verbs = "", "", []


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
    if edit.sub_body:
        # hypothesis:write-py-inline-replace-verb -- a `sub` that touched the
        # body is the base note/thought compose onto, so `sub a => b && note
        # why` is one body write, not two.
        body = edit.sub_body

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
        block = (f"{node_writer.THOUGHT_BEGIN}\n{edit.thought}\n"
                 f"{node_writer.THOUGHT_END}")
        body = node_writer.replace_thought(body, block)
    return body


def _landed_node_text(root, edit: Edit, actor: str = "",
                      session: str = "") -> str:
    """The bytes `update_node` would write; the conjunct-4 preview diff.

    Built through `node_writer.assemble_node`, the SAME ordering `update_node`
    uses, so the preview cannot drift from the landed bytes
    (hypothesis:sub-dry-run-preview-is-the-bytes-update-node-lands).
    """
    from graph_core.persistence import frontmatter as fm_reader
    path = node_writer.find_node_file(root, edit.node_id)
    if path is None:
        raise EditError(f"no node file for {edit.node_id}")
    nf = fm_reader.load_node_file(path)
    new_body = nf.body
    has_new_body = False
    if edit.body_append or edit.thought:
        new_body = _compose_body(root, edit)
        has_new_body = True
    elif edit.sub_body:
        new_body = edit.sub_body
        has_new_body = True
    set_fm = dict(edit.set_fm or {})
    set_fm[PROVENANCE_ACTOR] = actor or _default_actor()
    if session:
        set_fm[PROVENANCE_SESSION] = session
    fm, new_body, _ = node_writer.assemble_node(
        nf.frontmatter, new_body,
        old_body=nf.body if has_new_body else None,
        set_fm=set_fm, unset_fm=edit.unset_fm)
    return node_writer._serialize_node(node_writer.render_frontmatter(fm),
                                       new_body)


def _baseline_node_text(root, node_id: str) -> str:
    """The on-disk node's bytes, VERBATIM -- the `-` diff side: NO stamp, NO
    absorb, NO re-serialize, so the patch applies to the file that is actually
    there and a duplicate body frontmatter block the real write strips, a
    missing EOF newline, or a frontmatter `render_frontmatter` would rewrite
    all stay visible as the bytes they are (hypothesis:sub-dry-run-preview-is-
    the-bytes-update-node-lands).
    """
    path = node_writer.find_node_file(root, node_id)
    if path is None:
        raise EditError(f"no node file for {node_id}")
    return path.read_text(encoding="utf-8")


def create(root, node_type: str, slug: str, parents: list[str], *,
           set_fm: dict | None = None, payload: str | None = None,
           body: str | None = None,
           actor: str = "", session: str = "", role: str = "",
           bypass: bool = False, post_rows: dict | None = None):
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
                                 body=body,
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
    # `post_rows` (the answers route ONLY) is re-stamped HERE because
    # `node_writer._stamp_env_fields` OWNS `season` and `role` at mint and
    # overwrites whatever the file asked for, from the ENVIRONMENT; the post
    # row is the authority the claim names, so it lands last. Absent (the
    # argv route) this is a no-op and `create()` stays byte-identical.
    stamp_rows = dict(post_rows or {})
    if stamp_rows or actor or session:
        stamp = Edit(node_id=res.node_id)
        if actor:
            stamp.set_fm[PROVENANCE_ACTOR] = actor
        if session:
            stamp.set_fm[PROVENANCE_SESSION] = session
        stamp.set_fm.update(stamp_rows)
        node_writer.update_node(root, res.node_id, set_fm=stamp.set_fm,
                                log_extra=_log_provenance(actor))
    return res, created_file


def main(argv: list[str] | None = None) -> int:
    """`write.py <node-id> "set k v && link self && thought why"`
    or `write.py build:bin-x "read payload 10:20"` / `"patch -"` (diff on
    stdin, fail-closed; `body_patch -` for a node body).

    or `write.py create <type> <slug> --parent <id> [--payload PATH]
    [--body-file PATH]`.
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
    # hypothesis:lm-replace-body-standalone-restriction-is-documented-in-help
    # -- submit() already refuses this loudly (see the raise below); the gap
    # was discoverability, so the rule is rendered into `-h` BEFORE a caller
    # writes a script that will fail. Appended AFTER the verb table so every
    # verb line keeps its exact `name\tarity arg(s)\texample` shape that the
    # drift guard and the epilog tests inspect.
    epilog_lines.append("")
    epilog_lines.append("NOTES:")
    epilog_lines.append(
        "  replace body is standalone; it cannot share a script line with "
        "note, thought or body_patch (one body writer per submit). "
        "Compose them as separate write.py calls.")
    epilog_lines.append(
        "  a prose argument carries a literal verb-led && by escaping it "
        "as \\&&; an unescaped && before a verb still separates, and "
        "&&&& (a doubled pair) separates exactly as it always did.")
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
    ap.add_argument("--body-file", default=None, metavar="PATH",
                    help="with `create`: read this file's UTF-8 bytes as the "
                         "node body verbatim, instead of the type's "
                         "placeholder scaffold")
    ap.add_argument("--set", dest="sets", action="append", default=[],
                    help="with `create`: extra frontmatter, k=v, repeatable")
    ap.add_argument("--answers", default=None, metavar="PATH",
                    help="with `create`: mint the node from ONE JSON answers "
                         "file (type, slug, parents, every row, body) — an "
                         "alternative to --set/--body-file, not a new verb")
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
    ap.add_argument("--ring-fresh", default=None, metavar="TS|NONCE",
                    help="rung 2 freshness seam (kid D): pin the EXACT "
                         "'<ts>|<nonce>' this config write's `_fresh` field "
                         "carries, so an out-of-process signer computes the "
                         "SAME canonical bytes a `ring:`-declaring schema's "
                         "gate verifies. Absent -> the gate mints fresh "
                         "(unpredictable).")
    ap.add_argument("--ring-fields", action="store_true",
                    help="rung 2 signer's view (kid D): print the exact "
                         "config-write decision fields and canonical bytes the "
                         "`ring:`-declaring gate will verify for this edit "
                         "(+ `--ring-fresh`), then exit 0 -- never writes or "
                         "records a nonce.")
    args = ap.parse_args(argv)

    if args.node_id == "create":
        root = locations.find_project_root(Path(args.root).resolve())
        if root is None:
            print(f"ERR: not an agi project: {args.root}", file=sys.stderr)
            return 1
        answers: dict = {}
        post_rows: dict = {}
        if args.answers:
            answers, refusal = _read_answers_file(args.answers)
            if refusal:
                print(f"ERR: {refusal}", file=sys.stderr)
                return 2
        script = args.script or answers.get("type") or ""
        slug = args.slug or answers.get("slug") or ""
        parents = list(args.parents or answers.get("parents") or [])
        set_fm = {k: v for k, v in answers.items()
                  if k not in _ANSWERS_RESERVED}
        for k in sorted(set_fm):
            refusal = _refuse_authored_identity(k, "answers")
            if refusal:
                print(f"ERR: {refusal}", file=sys.stderr)
                return 2
        if not script or not slug:
            print("ERR: create needs a type and a slug: "
                  'write.py create <type> <slug> --parent <id>', file=sys.stderr)
            return 2
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
            refusal = (_refuse_authored_identity(k, "set")
                       or _refuse_marker_value(k, v))
            if refusal:
                print(f"ERR: {refusal}", file=sys.stderr)
                return 2
            set_fm[k] = v
        # claim 2: the answers route runs ONE row validator BEFORE the
        # dry-run short-circuit, so a bad row refuses on a dry run too.
        if answers:
            # claim 3: the calling post's row fills the rows the answers file
            # is SILENT on, BEFORE the validator — so a stamp goes through the
            # same row rules and can satisfy a REQUIRED row. A row the file
            # SETS wins; the stamp never overwrites an authored row.
            post_rows = {k: v for k, v in _post_stamp(root, args.actor).items()
                         if k not in set_fm}
            set_fm.update(post_rows)
            # THE PRECEDENCE, executed: an explicit `--set` and the file's own
            # row now outrank the post row, so the SURVIVING choice is what
            # create() re-stamps after `node_writer`'s environment stamp.
            post_rows.update({k: set_fm[k] for k in _STAMP_ROWS
                              if k in set_fm})
            refusal = _answers_row_refusal(root, script, f"{script}:{slug}",
                                           slug, parents, set_fm)
            if refusal:
                print(f"ERR: {refusal}", file=sys.stderr)
                return 2
        # hypothesis:l4-the-town-create-gate-refuses-what-the-loader-refuses-
        # and-every-vision-id-must-exist — the schema's field-level `refuse:`/
        # declared-`int` rules are a GATE the create path enforces GENERICALLY,
        # before the dry-run short-circuit (a dry run simulates the mint, so it
        # refuses what the real mint would refuse). A town `branches:` cell and
        # a non-int `season` both refuse BY NAME by exit 2 here — never a
        # traceback, never a node born only for a later reader to reject.
        refusal = _enforce_create_schema_gate(root, script, set_fm)
        if refusal:
            print(f"ERR: {refusal}", file=sys.stderr)
            return 2
        # The ceiling guard lives ABOVE the dry-run short-circuit: one guard,
        # one message, one exit code, on BOTH paths (a dry run simulates the
        # mint, so it refuses what the real mint refuses -- the same rule the
        # answers row validator above follows, and the hole `--dry-run` used
        # to open around it).
        # INHERITED FAIL-OPEN, stated here so a later reader sees it is policy
        # and not an oversight: an actor with no seat row (or a seat role off
        # the ladder) makes `_ceiling_refusal` return None, so an unseated
        # `--actor` -- or none at all -- still mints an elevated `role` here.
        # That is the SAME policy the `--role`/`AGI_ROLE` routes carry
        # (`_ceiling_refusal`); changing it would make `--answers` STRICTER
        # than `--role` on identical facts. A ladder decision, not this
        # call site's: named for the director, not fixed here.
        if post_rows.get("role"):
            refusal = _ceiling_refusal(
                str(post_rows["role"]), _resolve_seats_role(root, args.actor),
                args.actor or "-", "--answers")
            if refusal:
                print(f"ERR: {refusal}", file=sys.stderr)
                return 2
        if args.dry_run:
            print(f"create {script}:{slug}")
            print(f"  parents  {parents or '(none)'}")
            print(f"  payload  {args.payload or answers.get('payload') or ''}")
            if args.body_file is not None:
                print(f"  body-file {args.body_file}")
            elif answers.get("body") is not None:
                print("  body     (from --answers)")
            for k, v in set_fm.items():
                print(f"  set      {k} = {v!r}")
            return 0
        # hypothesis:lm-create-body-file-lands-real-prose-not-the-placeholder-
        # scaffold -- the verb layer owns IO. Read the body HERE, in `main()`,
        # so a missing/unreadable file is refused by name with exit 2 and NO
        # node is written; `body=None` (no flag) reaches `write_node`
        # unchanged, keeping the BODY_PROMPTS scaffold path byte-identical.
        # A `role` the answers file or an explicit `--set` names is re-stamped
        # LAST (below, in `create()`), AFTER `node_writer`'s environment stamp
        # -- which is exactly why the ceiling guard has to be applied to the
        # SURVIVING row HERE: an elevation that survives the precedence would
        # otherwise never be compared with the actor's seat at all.
        body = None
        if args.body_file is not None:
            try:
                body = Path(args.body_file).read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError) as exc:
                print(f"ERR: --body-file {args.body_file}: {exc}",
                      file=sys.stderr)
                return 2
        elif answers.get("body") is not None:
            body = answers["body"]
        res, made = create(root, script, slug, parents,
                           set_fm=set_fm,
                           payload=args.payload or answers.get("payload"),
                           body=body, actor=args.actor, session=args.session,
                           role=args.role, bypass=args.no_spawn_gate,
                           post_rows=post_rows)
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
        from types import SimpleNamespace  # noqa: PLC0415 -- residue 92: create commits too
        _note, _unc = _commit_write(root, res.node_id, SimpleNamespace(
            path=res.path, payload_changed=made is not None, payload_path=str(made or "")), args.actor)
        if _note:
            print(_note, file=sys.stderr)
        return EXIT_UNCOMMITTED if _unc else 0

    if not args.script:
        print("ERR: a script is required: "
              'write.py <node-id> "set k v && thought why"', file=sys.stderr)
        return 2
    # A second positional on an EDIT lands in `slug` (create's slot) and was
    # silently dropped: `write.py <id> 'row ...' 'thought ...'` wrote the row
    # and lost the thought (measured 09-29 on command:commands, f7a91e213 +
    # 3d1d03054). One script per call; verbs join with `&&`.
    if args.slug is not None:
        print(f"ERR: one script per call -- join verbs with ' && '; the extra "
              f"argument {args.slug[:60]!r} would be dropped", file=sys.stderr)
        return 2

    root = locations.find_project_root(Path(args.root).resolve())
    if root is None:
        print(f"ERR: not an agi project: {args.root}", file=sys.stderr)
        return 1

    if ":" not in (args.node_id or "") and not node_writer.find_node_file(root, args.node_id):
        # goal:g4.18.6.1: a mint id addresses its node (any shape: the Prime, 22:1xZ)
        import links  # noqa: PLC0415
        import rotation_record  # noqa: PLC0415
        try:
            hit = links.resolve_mint(root, args.node_id)
        except ValueError as exc:
            print(f"ERR: {exc}", file=sys.stderr)
            return 2
        except rotation_record.GrepError as exc:   # SM 102: never a traceback
            print(f"ERR: mint lookup could not look: {exc}", file=sys.stderr)
            return 2
        if hit is None:
            print(f"ERR: no node carries mint id {args.node_id}", file=sys.stderr)
            return 2
        args.node_id = hit[0]
    edit = Edit(node_id=args.node_id)
    try:
        for name, verb_args in parse_script(args.script):
            apply_verb(edit, name, verb_args)
    except EditError as exc:
        print(f"ERR: {exc}", file=sys.stderr)
        return 2

    if _stdin_refusal(edit):   # SM 117: before ANY verb reads stdin
        print(f"ERR: {_stdin_refusal(edit)}", file=sys.stderr)
        return 2
    # BUILD1: a nested frontmatter row becomes a `set_fm` entry HERE, before
    # the set schema gate, so it is judged exactly like a `set`.
    if edit.fm_rows:
        try:
            _resolve_fm_row(root, edit)
        except EditError as exc:
            print(f"ERR: {exc}", file=sys.stderr)
            return 2
    # SM 151 + 155: `patch -` reads its diff HERE (once: SM 132), and a patch on a
    # node with no payload_ref becomes its rows + body BEFORE the set gates and
    # --ring-fields read edit.set_fm (submit's own call stays idempotent)
    if edit.patch_from == "-":
        # a diff can contain the doubled ampersand, so it rides stdin, like `payload -`
        edit.patch_diff = sys.stdin.read()
    try:
        _patch_the_node_itself(root, edit)
    except EditError as exc:
        print(f"ERR: {exc}", file=sys.stderr)
        return 2

    # goal:g7.33.10 round B -- the SET half of the schema-checked-rows gate.
    # `edit.set_fm` is fully accumulated now (every `set` in the script has
    # landed), so one pass here judges every row before anything reaches
    # submit(). node_type is the node id's own prefix convention
    # (`goal:g7.2` -> `goal`), the same shortcut node_writer already uses.
    if edit.set_fm and ":" in args.node_id:
        node_type = args.node_id.split(":", 1)[0]
        refusal = (_enforce_set_schema_gate(root, node_type, edit.set_fm)
                   or _missing_link_refusal(root, edit.set_fm))
        if refusal:
            print(f"ERR: {refusal}", file=sys.stderr)
            return 2

    # hypothesis:write-py-inline-replace-verb -- resolve `sub`/`sub!` once,
    # here, so the `--dry-run` preview shows the real diff and a 0/2+ match
    # refusal prints ERR and writes nothing. submit() re-resolves idempotently
    # for an API caller.
    if edit.sub_ops:
        try:
            _resolve_sub(root, edit)
        except EditError as exc:
            print(f"ERR: {exc}", file=sys.stderr)
            return 2
    # SM N1 + 125: the preview refuses what submit refuses, judged in submit's
    # order -- AFTER the sub resolves, so its `sub_body` clause is seen
    if _standalone_refusal(edit):
        print(f"ERR: {_standalone_refusal(edit)}", file=sys.stderr)
        return 2

    # hypothesis:l4-...-the-write-itself, SIGNER'S VIEW (kid D): `--ring-fields`
    # prints the EXACT config-write decision bytes a `ring:`-declaring schema's
    # gate will verify for this edit (+ `--ring-fresh`), then exits 0 -- never
    # writes, never records a nonce. The signer parses the canonical hex line,
    # signs over it, and the corresponding real invocation admits (acceptance D).
    if args.ring_fields:
        from seatsig import rings as _ringslib  # noqa: PLC0415
        try:
            _fresh = _ringslib.parse_ring_fresh(args.ring_fresh)
        except ValueError as _ve:
            print(f"ERR: {_ve}", file=sys.stderr)
            return 2
        _t, _n = (_fresh if _fresh is not None else (None, None))
        fields = _config_write_fields(
            edit.node_id,
            edit.set_fm if edit.set_fm else None,
            edit.unset_fm if edit.unset_fm else None,
            ts=_t, nonce=_n)
        print(_ringslib.render_ring_fields(
            "config-write", fields,
            _ringslib.canonical_bytes("config-write", fields)))
        return 0

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
                or edit.body_patch_from or edit.body_patch_diff
                or edit.sub_body or edit.canonicalize):   # SM 163: a translated body-only node patch
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
        try:  # goal:g4.18.3 -- the SAME written_by gate submit applies, before any mint
            _enforce_written_by(root, edit.node_id.split(":", 1)[0], args.actor,
                                edit.node_id, args.role, allow_self_row=True)
        except EditError as exc:
            print(f"ERR: {exc}", file=sys.stderr)
            return 2
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
        _note, _unc = _commit_write(root, edit.node_id, res, args.actor)   # residue 92
        if _note:
            print(_note, file=sys.stderr)
        return EXIT_UNCOMMITTED if _unc else 0

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

    # SM 132: stdin is read ONCE, here, BEFORE the one judge -- a dry run judges
    # the same bytes the write lands (a `body_patch -` diff that does not apply
    # refuses in both)
    _stdin: set = set()   # SM 134: which sources came off stdin -- the preview labels them
    if edit.payload_from == "-":
        # The CLI layer reads stdin; the library never does. `payload -` is
        # for content that cannot ride in an argv chunk -- anything with `&&`
        # in it, or a whole file being piped in.
        _data = sys.stdin.read()
        _stdin.add("payload")
        if _data:   # SM 140: an EMPTY read keeps `-`, and submit refuses it by name, dry and real
            edit.payload_from, edit.payload_bytes = "", _data

    if edit.body_patch_from == "-":
        # Same stdin contract as `payload -` / `patch -`: the diff bytes ride
        # stdin because a diff can contain the doubled ampersand that would
        # split the `&&` script form. Read once, here, never in the library.
        _diff = sys.stdin.read()
        _stdin.add("body_patch")
        if _diff:   # SM 144: as 140 -- an EMPTY read keeps `-`, and submit refuses it by name
            edit.body_patch_from, edit.body_patch_diff = "", _diff

    if args.dry_run:
        print(f"{edit.node_id}:")
        for k, v in edit.set_fm.items():
            _mine = [ref for ref, _ in edit.fm_rows if ref.split(".", 1)[0] == k]
            if _mine:
                for ref in _mine:
                    print(f"  row    {ref} "
                          f"({'replace' if ref.split('.', 1)[1] in v else 'remove'})")
                continue
            print(f"  set    {k} = {v!r}")
        for k in edit.unset_fm:
            print(f"  unset  {k}")
        if edit.thought:
            print(f"  thought ({len(edit.thought)} chars)")
        if edit.body_append:
            print(f"  note    ({len(edit.body_append)} chars)")
        if edit.payload_from:
            print(f"  payload from {edit.payload_from}")
        if edit.payload_bytes or "payload" in _stdin:
            _src4 = "stdin" if "payload" in _stdin else "inline"
            print(f"  payload  ({len(edit.payload_bytes or '')} bytes, {_src4})")
        if edit.patch_diff:
            _src = "stdin" if edit.patch_from == "-" else edit.patch_from
            print(f"  patch   ({len(edit.patch_diff)} bytes of diff, {_src})")
        if edit.patch_from and not edit.patch_diff:
            print(f"  patch   from {edit.patch_from}")
        if edit.body_patch_diff or "body_patch" in _stdin:
            _src2 = "stdin" if "body_patch" in _stdin else edit.body_patch_from
            print(f"  body_patch ({len(edit.body_patch_diff)} bytes of diff, {_src2})")
        if edit.body_patch_from and not edit.body_patch_diff:
            print(f"  body_patch from {edit.body_patch_from}")
        if edit.replace_target:
            if edit.row_ref:   # residue 96: the preview resolves the row too
                try:
                    edit.replace_range = _row_range(
                        _target_text(root, edit, "body"), edit.row_ref)
                except EditError as exc:
                    print(f"ERR: {exc}", file=sys.stderr)
                    return 2
            if edit.row_ref:
                print(f"  row    {edit.row_ref} -> {edit.replace_range}")
            _src3 = "stdin" if edit.replace_from == "-" else edit.replace_from
            print(f"  replace {edit.replace_target} {edit.replace_range} "
                  f"({len(edit.replace_text)} chars, {_src3})")
        if edit.sub_resolved:
            _before = _baseline_node_text(root, edit.node_id)
            _after = _landed_node_text(root, edit, actor=args.actor,
                                       session=args.session)
            # A STANDARD unified diff: compared keepends so a missing EOF
            # newline is a real line difference, rendered with the `\ No
            # newline at end of file` marker GNU `patch` demands. The old
            # split("\n") render modelled a missing EOF newline as a phantom
            # empty trailing line and GNU patch rejected the printed diff
            # (hypothesis:sub-dry-run-preview-is-the-bytes-update-node-lands).
            _sdiff = _standard_unified_diff(
                _before, _after,
                fromfile=f"a/{edit.node_id}", tofile=f"b/{edit.node_id}")
            edit.sub_diff = _sdiff
            sys.stdout.write(_sdiff)
            if _sdiff and not _sdiff.endswith("\n"):
                sys.stdout.write("\n")
            print(f"  sub     {edit.sub_count} match(es) of "
                  f"{edit.sub_old!r} -> {edit.sub_new!r}")
        try:   # SM 130: the preview refuses by submit's OWN judgement, never a mirror
            submit(root, edit, actor=args.actor, session=args.session,
                   role=args.role, dry_run=True)
        except (EditError, FileNotFoundError) as exc:
            print(f"ERR: {exc}", file=sys.stderr)
            return 2
        return _preview_dry_run_gate(root, edit, args)

    try:
        edit.signatures = args.ring_sigs
        from seatsig import rings as _ringslib  # noqa: PLC0415
        try:
            _fresh = _ringslib.parse_ring_fresh(args.ring_fresh)
        except ValueError as _ve:
            print(f"ERR: {_ve}", file=sys.stderr)
            return 2
        res = submit(root, edit, actor=args.actor, session=args.session,
                     role=args.role, ring_fresh=_fresh)
    except (EditError, FileNotFoundError) as exc:
        print(f"ERR: {exc}", file=sys.stderr)
        return 2
    print(f"{res.status}: {edit.node_id}"
          + (f" — {res.reason}" if res.reason else ""))
    if res.status != node_writer.REJECTED and edit.sub_resolved:
        print(f"sub: replaced {edit.sub_count} occurrence(s)")
    if res.status != node_writer.REJECTED:
        # The seat's OWN last act (conjunct 1): --actor first, then the env.
        last_act.touch_env(root, args.actor)
    if res.payload_changed is not None:
        print(f"payload: {res.payload_path} "
              + ("replaced" if res.payload_changed else "unchanged"))
    if res.status == node_writer.UPDATED or res.payload_changed:   # goal:g4.18.5.2 (+ residue 91: payload-only)
        _note, _unc = _commit_write(root, edit.node_id, res, args.actor)
        if _note:
            print(_note, file=sys.stderr)
        if _unc:
            return EXIT_UNCOMMITTED
    return 1 if res.status == node_writer.REJECTED else 0


#: goal:g4.18.5.2.1 -- the node is written but NOT committed (a busy index
#: past the `values.core.write_commit_wait_s` budget): never exit 0 over it.
EXIT_UNCOMMITTED = 3


def _commit_wait_s(root) -> float:
    """`values.core.write_commit_wait_s` (goal:g4.18.5.2.1), default 30."""
    try:
        cfg = json.loads(locations.config_path(Path(root)).read_text(encoding="utf-8"))
        v = float(((cfg.get("values") or {}).get("core") or {})["write_commit_wait_s"])
        return v if v >= 0 else 30.0
    except (OSError, TypeError, ValueError, KeyError, AttributeError, json.JSONDecodeError):
        return 30.0


def _commit_message(root, node_id: str, actor: str = "") -> str:
    """goal:g4.18.5.2.2 -- a write's commit message, from the ONE cell
    `write.commit_message` (+ `write.commit_actor`) in the project's
    .agi/config.json, else the engine repo's own (a cloned engine carries it).
    No template literal here: a config without the cell names the node alone."""
    import json
    for cfg in (Path(root) / "config.json", Path(__file__).resolve().parents[3] / ".agi" / "config.json"):
        try:
            cell = json.loads(cfg.read_text(encoding="utf-8")).get("write") or {}
        except (OSError, ValueError, AttributeError):
            continue
        if cell.get("commit_message"):
            by = cell.get("commit_actor", "").format(actor=actor) if actor else ""
            return cell["commit_message"].format(node_id=node_id, actor=by)
    return node_id


def _commit_write(root, node_id: str, res, actor: str = "") -> tuple[str | None, bool]:
    """goal:g4.18.5.2 -- the CLI write, after the gate, is ONE commit of its
    own node (+ its payload) by exact path. In main() only: submit() is the
    library rotate.py and send.py call on shared files. `git commit -- <paths>`
    commits those paths alone: never -a, never a file another post staged. A
    held verify-suite.lock refuses the commit by name (the write stays on
    disk; the ONE sanctioned exit 0 over an uncommitted node). Not a git
    checkout = nothing to commit. Unpark carriers a formation switch writes
    are other nodes: they stay out.

    goal:g4.18.5.2.1: an `index.lock` refusal (concurrent writers) is
    retried with jittered backoff inside `values.core.write_commit_wait_s`;
    past it the write refuses by name. Returns `(note, uncommitted)` --
    `uncommitted` True = the caller exits EXIT_UNCOMMITTED. Every printed
    recovery line ADDS the paths first, so it works for a create (untracked)."""
    paths = [str(p if Path(p).is_absolute() else Path(root) / p)
             for p in (res.path, res.payload_changed and res.payload_path) if p]
    git = lambda *a: subprocess.run(["git", "-C", str(root), *a],  # noqa: E731
                                    capture_output=True, text=True)
    if not paths or git("rev-parse", "--is-inside-work-tree").returncode:
        return None, False
    msg = _commit_message(root, node_id, actor)
    recover = (f"git -C {root} add -- {' '.join(paths)} && "
               f"git -C {root} commit -q -m {shlex.quote(msg)} -- {' '.join(paths)}")
    import verification  # noqa: PLC0415 -- the ONE live-holder read (residue 93)
    holder = verification.suite_lock_holder(Path(root))
    if holder:
        return (f"commit refused: {Path(root) / 'sessions' / verification.SUITE_LOCK} is held "
                f"by live pid {holder} -- the write landed uncommitted; commit it by "
                f"exact path: {recover}"), False
    import random  # noqa: PLC0415
    deadline = time.monotonic() + _commit_wait_s(root)
    tries = 0
    while True:
        tries += 1
        add = git("add", "--", *paths)
        done = add if add.returncode else git("commit", "-q", "-m", msg, "--", *paths)
        if done.returncode == 0:
            return None, False
        busy = "index.lock" in (done.stderr or "") + (done.stdout or "")
        # the peer's commit won the race (hypothesis:a-write-refusal-names-the-index-truth):
        # the index is the truth, and it says these bytes are already in HEAD.
        # TRACKED or not "clean": `status --porcelain` is blind to an ignored
        # path, and an ignored uncommitted node is the exact rc-0-over-a-lost-
        # write the refusal exists to prevent.
        tracked = all(git("ls-files", "--error-unmatch", "--", p).returncode == 0
                      for p in paths)
        if (not busy and tracked
                and not git("status", "--porcelain", "--", *paths).stdout.strip()):
            return (f"commit skipped: {node_id} is clean at HEAD (a peer committed "
                    f"these bytes -- nothing to commit) -- exit 0"), False
        if not busy or time.monotonic() >= deadline:
            break
        time.sleep(min(2.0, 0.05 * 2 ** min(tries, 6)) * (0.5 + random.random()))
    # residue 90: never left STAGED in a shared index; residue 98: a reset
    # that fails too (index.lock held) is said loudly, never claimed as done
    reset = git("reset", "-q", "--", *paths)
    staged = git("diff", "--cached", "--quiet", "--", *paths).returncode != 0
    state = ("unstaged" if reset.returncode == 0 else
             f"STILL STAGED, reset failed rc {reset.returncode} -- run "
             f"git reset -q -- {' '.join(paths)}" if staged else
             f"reset failed rc {reset.returncode} -- the path is NOT staged, "
             f"so nothing of this write is left staged")
    return (f"commit failed after {tries} tr{'y' if tries == 1 else 'ies'} ({state}; "
            f"the write stays on disk UNCOMMITTED -- exit {EXIT_UNCOMMITTED}; recover: "
            f"{recover}): {(done.stderr or done.stdout).strip()[:300]}"), True

if __name__ == "__main__":
    raise SystemExit(main())
