#!/usr/bin/env python3
"""node_writer.py — THE routine that creates a node file (GOALS.md S17).

Every path that mints a new node calls `write_node()`. There is exactly one
of these, and it is gated.

Why this file exists
--------------------
`spawn_gate.py` landed on `cli.py scaffold`, `cli.py done`'s fallback verdict
and `post_wire.py`'s verdict creation — three of the writers — and
`verdict:spawn-gate-lands-on-writer-path` recorded the miss: `bin/dispatch.py`
carried a **duplicated copy of the whole scaffold routine**, with its own
`NODE_TYPES` tuple, its own body-prompt dict and its own `write_text()`. So a
pi-runtime run (`driver.sh --max-iters N`) wrote nodes past the gate entirely,
and its private tuple still minted the hyphenated `bigger-outcome` /
`app-purpose` spellings that `[shape].md` declares non-canonical.

The duplication is the defect, not the missing call. Wiring the gate into
dispatch.py's copy would have made two gated routines that drift apart at the
next edit — the same one-fact-three-definitions shape S17 names. So the copy
is deleted and every writer points here, **by the same method**: an ordinary
`import node_writer` off `bin/` on `sys.path`, which is already how `cli.py`
and `post_wire.py` reach `evidence_gate` and `spawn_gate`.

Callers, all four:

  bin/cli.py       cmd_scaffold           — the agent-facing scaffold
  bin/cli.py       cmd_done (fallback)    — verdict node when none exists
  bin/post_wire.py cmd_wire (fallback)    — verdict node when none exists
  bin/dispatch.py  _scaffold_node_for_agent — pi runtime, previously ungated

What is deliberately NOT routed here
------------------------------------
The three **generators** — `snapshot-goals.py`, `snapshot-build-site.py`,
`level3.py`. They do not *spawn*: they re-derive a whole node population from
an input file on every run, own their own frontmatter keys, and carry a
`preserve=` merge this routine has no notion of. They also share one
`write_frontmatter` between them already (`level3.py` imports
snapshot-goals'), so they are not a duplication problem. Gating them is
undecided on purpose: a generator that trips the gate is a generator bug, and
failing the loop over it is worse than reporting it (H0i is what happens when
a generator run goes wrong).

Type spelling
-------------
Underscore is canonical (`context/schemas/[shape].md ::
canonical_type_spelling`). Hyphens are accepted as *input* aliases, because
scripts and habits pass them, and are never written. This is the single
generator for both facts; before this file there were two tuples and only one
of them had been fixed.
"""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import spawn_gate  # noqa: E402
from frontmatter import split_frontmatter  # noqa: E402

# goal:s14 — a node gets its permanent id from whatever writes the file, not
# from a backfill run afterwards. The ENGINE's graph_core, never a project's
# vendored src/ (which predates `mint_permanent_id` entirely).
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from graph_core.identity import mint_permanent_id  # noqa: E402


# goal:s17 -- underscore is canonical (`context/schemas/[shape].md`).
#
# `goal` and `level3` are deliberately absent. Both are *derived*:
# `snapshot-goals.py` regenerates `nodes/goal/` from GOALS.md and deletes every
# `origin: goals-doc` node it does not re-derive, and `level3.py` regenerates
# the census. A hand-scaffolded node of either type is a stray the next loop
# run silently removes -- offering the option would be offering a trap.
CANONICAL_NODE_TYPES = (
    "idea", "hypothesis", "task", "experiment", "verdict", "mvp", "outcome",
    "bigger_outcome", "overview", "vision",
)
# `app_purpose` was renamed to `vision` on 2026-08-27 (the old name described
# one kind of project; the node is about what the whole graph is for). Kept as
# an alias, not deleted: the reader accepts both spellings so a caller written
# against the old name keeps working, which is the same sequence S11 requires
# for `level3` and the reason the hyphen aliases below are still here.
TYPE_ALIASES = {"bigger-outcome": "bigger_outcome",
                "app-purpose": "vision",
                "app_purpose": "vision"}
#: What an argparse `choices=` should accept: canonical + aliases.
NODE_TYPES = CANONICAL_NODE_TYPES + tuple(TYPE_ALIASES)

#: The body a fresh node opens with, per type. One dict, not two: dispatch.py
#: shipped a terser variant of this whose keys were the hyphenated spellings,
#: so the two generators could not even agree on what a node of a given type
#: should say.
BODY_PROMPTS = {
    "idea": "## Idea\n\nWhat is the concept? `scale:` big (new chain) or small (extension)?\n\n",
    "task": "## Task\n\nWhich cavekit requirement (`cavekit_req`)? What are the acceptance criteria?\n\n",
    "hypothesis": "## Hypothesis\n\nWhat is the testable claim? What would prove it? What would disprove it?\n\n",
    "experiment": "## Experiment\n\nWhat did you do? What happened? Include command/inputs and actual outputs.\n\n## Evidence\n\nRaw output, screenshots, logs.\n\n",
    "verdict": "## Verdict\n\nproved | disproved | inconclusive_lean_proved:N | inconclusive_lean_disproved:N\n\n## Evidence\n\nWhat evidence supports this verdict?\n\n## Confidence\n\n0.0 – 1.0\n\n",
    "mvp": "## MVP\n\nWhat does this script/module do? Show the code or describe the implementation.\n\n## Inputs\n\nWhat does it take?\n\n## Outputs\n\nWhat does it produce?\n\n",
    "outcome": "## Outcome\n\nInput shape (what enters):\n\nOutput shape (what exits):\n\nBehavior (what it does):\n\nEdge cases:\n\n## i/o doc\n\n```\ninputs:\noutputs:\n```\n\n",
    "bigger_outcome": "## Bigger Outcome\n\nWhat module or purpose does this outcome serve?\n\nHow do the child outcomes compose into this?\n\n",
    "overview": "## Overview\n\nWhich bigger outcomes does this read together (>=3)?\n\nWhat do they say jointly that none says alone?\n\n",
    "vision": "## Vision\n\nWhat is the whole graph for?\n\nWhich overviews assemble into this (>=2)?\n\nWhat goals does it propose for the next season (`proposes_goals:`)?\n\n",
}

#: Frontmatter keys that lead, in this order. Everything else follows sorted,
#: so two writers producing the same node produce the same bytes.
LEADING_KEYS = ("id", "mint_id", "type", "parents", "next_edges")

#: One-line HTML comment the scaffold writes right after the closing `---`,
#: marking where the body starts (hypothesis:l3-done-broken-frontmatter).
#: `cli.py done`'s repair path uses it as the one reliable boundary between a
#: mangled frontmatter block and the kid's body: without it there is no safe
#: way to tell the two apart, so a broken `---` block becomes unrecoverable
#: rather than repairable. `graph_core` treats everything after the closing
#: `---` as body, so the comment is inert to every reader that parses the
#: frontmatter.
BODY_BEGIN = "<!-- BODY:BEGIN -->"

WRITE_LOG = "sessions/write-log.jsonl"

WRITTEN = "written"
SKIPPED = "skipped"
REJECTED = "rejected"
#: `update_node` only. A node that already existed and now differs.
UPDATED = "updated"
#: `update_node` only. The node was read, the write was legal, and nothing
#: about it would change. Distinct from SKIPPED, which means refused.
UNCHANGED = "unchanged"

#: `on_exists` policies.
SKIP = "skip"                       # a file that exists is never touched
REUSE_SCAFFOLD = "reuse-scaffold"   # overwrite only an untouched scaffold


def canonical_node_type(node_type) -> str:
    """Resolve an input spelling to the canonical one.

    Alias table first (it is the documented input surface), then the general
    `-` -> `_` rule so a type nobody aliased still lands canonical.
    """
    if not isinstance(node_type, str):
        return ""
    t = node_type.strip()
    return TYPE_ALIASES.get(t, spawn_gate.canonical_type(t))


def node_dir(root, node_type) -> Path:
    """Where a node of this type lives: `<root>/nodes/<canonical_type>/`."""
    return Path(root) / "nodes" / canonical_node_type(node_type)


#: `find_node_file`'s whole-corpus index, keyed by resolved root. Built once,
#: dropped whenever `write_node` adds a file, so it can never go stale within a
#: process.
_ID_INDEX: dict = {}


def _build_id_index(root: Path) -> dict:
    """id -> path, over the whole node tree. The last-resort lookup."""
    index: dict = {}
    nd = Path(root) / "nodes"
    if not nd.is_dir():
        return index
    from graph_core.persistence import frontmatter as fm_reader
    for nf in sorted(nd.rglob("*.md")):
        try:
            fm = fm_reader.load_node_file(nf, body=False).frontmatter
        except Exception:
            continue
        if isinstance(fm, dict):
            nid = fm.get("id")
            if isinstance(nid, str) and nid.strip():
                index.setdefault(nid.strip(), nf)
    return index


def find_node_file(root, node_id) -> Path | None:
    """id -> the file that holds it. The one lookup, mirroring the one write.

    `cli.py` and `post_wire.py` each carried their own version of this and
    they did not agree, which is the read-side of the defect S17 names.
    Measured over the 781-node corpus on 2026-08-26:

      post_wire's copy could not resolve 417 ids -- 53% of the graph, 270 of
      which cli.py's copy resolved fine. That is not cosmetic: post_wire's
      "no file found" branch *creates a verdict node*, so every unresolved id
      minted a duplicate instead of updating the node it meant to update. 56
      of the 270 were verdicts, which is the type post_wire exists to wire.

      cli.py's copy missed 147, all of them ids on an abbreviated prefix --
      `exp:` and `hyp:` for nodes under `nodes/experiment/` and
      `nodes/hypothesis/`. Neither copy had a fallback that did not assume the
      id prefix names the directory.

    Three steps, cheapest first, so the common case still costs one `stat`:

    1. `nodes/<canonical-type>/<slug>.md`, then the raw prefix as written.
    2. a frontmatter scan of those same two directories -- catches a
       descriptive filename like `t-001-thing.md`.
    3. a frontmatter index over the whole tree -- catches an id whose prefix
       is not its directory at all. Built once per root and dropped by
       `write_node`, so it cannot go stale under its own writer.
    """
    if not isinstance(node_id, str) or ":" not in node_id:
        return None
    root = Path(root)
    prefix, slug = node_id.split(":", 1)
    # Live directories first, then the retired sibling `nodes/deprecated/<type>/`
    # (goal:g2.10). Order is load-bearing: both loops below take the first hit,
    # so a live node must win over a retired namesake. Retired nodes are still
    # resolvable because they are still real — a deprecation moves an address,
    # it does not remove the node, and an edge pointing at one must keep
    # resolving or the retirement silently becomes a broken link.
    dirs = []
    names = (canonical_node_type(prefix), prefix.strip())
    for parent in (root / "nodes", root / "nodes" / "deprecated"):
        for name in names:
            d = parent / name
            if d not in dirs:
                dirs.append(d)

    for d in dirs:
        f = d / f"{slug}.md"
        if f.exists():
            return f

    for d in dirs:
        if not d.is_dir():
            continue
        from graph_core.persistence import frontmatter as fm_reader
        for nf in sorted(d.glob("*.md")):
            try:
                fm = fm_reader.load_node_file(nf, body=False).frontmatter
            except Exception:
                continue
            if isinstance(fm, dict) and fm.get("id") == node_id:
                return nf

    key = str(root.resolve())
    if key not in _ID_INDEX:
        _ID_INDEX[key] = _build_id_index(root)
    return _ID_INDEX[key].get(node_id)


def _needs_quoting(sval: str) -> bool:
    """True when a scalar would not survive the cheap frontmatter parsers.

    Every writer path here splits on `---` and hands the middle to
    `yaml.safe_load`, so the value has to be real YAML. `verdict:x` is fine —
    a colon with no space after it is part of a plain scalar, which is why
    every node id in the corpus is written bare and why quoting them here
    would be a gratuitous reformat. `no node: ['x']` is not fine, and that is
    a real `spawn_check_reason` this routine can emit.

    Negative numbers (`-1`, `-42`, `-0.5`) are valid YAML plain scalars and
    do NOT need quoting, even though they start with `-`. Verified 2026-09-04
    (iter-1068): `_needs_quoting("-1")` returned True, causing `tier: "-1"`
    instead of `tier: -1`, a lossy round-trip for negative ints that broke
    schema validation ([task].md declares `tier: {type: int}`).
    """
    if not sval:
        return False
    if ": " in sval or sval.endswith(":") or " #" in sval:
        return True
    # A `---` run ANYWHERE (e.g. `the --- and --- again`) would split the
    # frontmatter short for a reader that still splits on the substring, and
    # must never present as a bare `---` line to the line-anchored shared
    # reader (hypothesis:l4-one-line-anchored-frontmatter-reader-...).
    # Quoting keeps the value a valid YAML scalar on one line and turns what
    # would be a silent truncation into a detectable parse failure. `---`
    # itself is a document marker and so MUST be quoted too.
    if "---" in sval:
        return True
    # Negative number (`-N` or `-N.N`): valid YAML plain scalar, no quoting.
    # Bare `-` or `- ` would be a block sequence indicator.
    if sval[0] == "-" and len(sval) > 1 and (sval[1].isdigit() or sval[1] == "."):
        return False
    return sval[0] in "\"'[{&*!|>%@`#-?:,"


def _scalar(v) -> str:
    """One frontmatter scalar, quoted if it needs to be."""
    if isinstance(v, bool):
        return str(v).lower()
    sval = str(v).replace("\n", " ").strip()
    if _needs_quoting(sval):
        esc = sval.replace("\\", "\\\\").replace('"', '\\"')
        sval = f'"{esc}"'
    return sval


# YAML 1.1 treats these three code points as line breaks. Inside the
# JSON-in-YAML double-quoted string that a list-of-dict entry renders to,
# json.dumps(..., ensure_ascii=False) emits U+0085 (NEL), U+2028 (LINE
# SEPARATOR) and U+2029 (PARAGRAPH SEPARATOR) LITERALLY, and PyYAML folds
# NEL to a space on the next read — one code point lost through a serializer
# that is lossless for every other non-ASCII character. JSON does not require
# these to be escaped (they are valid inside a JSON string), but `\u0085`,
# `\u2028`, `\u2029` are equally valid JSON escapes, stay inside the one
# scalar, and read back to the same code points. Escape only these three;
# every other non-ASCII code point stays literal.
_YAML_LINEBREAK_ESCAPES = {chr(0x85): "\\u0085", chr(0x2028): "\\u2028", chr(0x2029): "\\u2029"}


def _escape_yaml_linebreaks(jtext: str) -> str:
    """Post-process a json.dumps output so no YAML line-break code point is
    emitted literally inside the scalar."""
    for cp, esc in _YAML_LINEBREAK_ESCAPES.items():
        jtext = jtext.replace(cp, esc)
    return jtext


def _render_value(key: str, v, indent: str = "") -> list[str]:
    """One `key: value` entry, recursing into lists and **mappings**.

    🔴 **A mapping used to fall through to `str(v)`, and that destroyed the
    node the whole command system reads** (2026-09-03, L1.07). `command:commands`
    carries a nested `commands:` mapping; one `write.py ... 'thought ...'` on it
    round-tripped the frontmatter through this function and wrote back a
    **Python dict repr in a quoted string**:

        commands: "{'smoke': {'argv': ['bash', ...

    `commands.load` then raised `'str' object has no attribute 'items'` and
    every `agi <verb>` stopped working. It was committed and pushed, because
    the test suite had been run *before* that edit and the edit was in the
    same shell command as the commit.

    The bug is old and was merely never reachable: nothing had written a node
    with a nested mapping through this path until `[command]` existed. The
    lesson is not "be careful with structural nodes" — it is that a serializer
    silently lossy on a type it does not recognise will eventually meet that
    type, and `str(v)` is the branch that makes losing data look like working.
    """
    if isinstance(v, dict):
        if not v:
            return [f"{indent}{key}: {{}}"]
        out = [f"{indent}{key}:"]
        for k2 in v:
            out.extend(_render_value(str(k2), v[k2], indent + "  "))
        return out
    if isinstance(v, (list, tuple)):
        if not v:
            return [f"{indent}{key}: []"]
        out = [f"{indent}{key}:"]
        for i in v:
            if isinstance(i, (dict, list, tuple)):
                # A list of containers has no single-line spelling here, and
                # inventing one would be another silent lossy branch. JSON is
                # valid YAML and round-trips exactly — but YAML 1.1 reads
                # U+0085/U+2028/U+2029 as line breaks, so they are escaped
                # explicitly inside the JSON rather than emitted literally.
                out.append(f"{indent}  - {_escape_yaml_linebreaks(json.dumps(i, ensure_ascii=False))}")
            else:
                out.append(f"{indent}  -" if i is None
                           else f"{indent}  - {i}")
        return out
    if v is None:
        return [f"{indent}{key}:"]
    return [f"{indent}{key}: {_scalar(v)}"]


def render_frontmatter(fm: dict) -> list[str]:
    """`fm` -> the lines between the `---` markers. Deterministic."""
    ordered = [k for k in LEADING_KEYS if k in fm]
    ordered += sorted(k for k in fm if k not in LEADING_KEYS)
    lines = []
    for k in ordered:
        lines.extend(_render_value(k, fm[k]))
    return lines


@dataclass
class NodeWrite:
    """What `write_node` did, and enough detail for a caller to report it."""

    status: str = WRITTEN
    node_id: str = ""
    node_type: str = ""
    slug: str = ""
    parents: list = field(default_factory=list)
    path: Path | None = None
    gate: "spawn_gate.SpawnResult | None" = None
    reason: str = ""
    #: goal:s31 -- schema-required fields this write could not supply. Empty
    #: is the healthy value; a non-empty list is a node that is valid-shaped
    #: but incomplete, and the caller is told rather than left to find out.
    missing_required: list = field(default_factory=list)
    #: goal:g13.1 -- what the `payload` verb did to the bytes behind this
    #: node, if anything. `None` = the edit did not touch them, `False` =
    #: identical bytes, `True` = replaced. A caller reports it; nothing
    #: branches on it.
    payload_changed: bool | None = None
    payload_path: str = ""

    @property
    def written(self) -> bool:
        return self.status == WRITTEN

    @property
    def rejected(self) -> bool:
        return self.status == REJECTED

    def as_info(self) -> dict:
        """The shape `dispatch.py` puts in `agent.json` and the pi prompt."""
        return {
            "node_type": self.node_type,
            "node_id": self.node_id,
            "parent": self.parents[0] if self.parents else "",
            "parents": list(self.parents),
            "slug": self.slug,
            "path": str(self.path) if self.path else "",
        }


def scaffold_hash(body: str) -> str:
    """Identity of a scaffold's body: what `completion.is_complete` compares against.

    Stamped into the node's frontmatter as `scaffold_hash:` by `write_node`, at
    write time. The stripped form, because the file's body region carries one
    leading blank line (a byproduct of how `write_node` joins its lines) that
    the scaffold body string itself does not.

    Capturing the hash when the file is written — rather than recomputing the
    placeholder at check time — is what makes the test drift-safe: if
    `BODY_PROMPTS` changes later, an untouched scaffold still hashes to the
    stamp and still reads incomplete (mvp:unified-spawn-path clause 5, the
    weak joint the MVP's own THOUGHT names).
    """
    return hashlib.sha256(body.strip().encode("utf-8")).hexdigest()[:16]


def _is_untouched_scaffold(text: str, scaffold_body: str) -> bool:
    """Has nobody filled this scaffold in yet?

    dispatch.py's rule, fixed. It compared the existing body against the type's
    *prompt* — but the body it writes is the `# <node-id>` heading followed by
    the prompt, so the comparison never matched and the re-scaffold branch was
    dead: dispatch always preserved, even a scaffold it had written itself
    seconds earlier. Comparing against the whole body this call would write is
    what the branch was for. A malformed file with no closing marker is also
    fair game — there is nothing in it to lose.
    """
    sp = split_frontmatter(text)
    if sp is None:
        return True
    return sp[1].strip() in scaffold_body.strip()


def ensure_payload(root, ref: str, location: str | None = None) -> Path | None:
    """Create the source file a node will point at, if it is not there yet.

    Returns the path if this call created it, else None. **Never overwrites**:
    an existing file is linked, not replaced.

    It lives here rather than in `write.py` on purpose. `write.py` holds a
    mechanically-checked invariant that it performs **no file write at all**
    (`test_write_py_contains_no_file_write` parses it rather than grepping),
    and that guard is what keeps the verb layer a front end instead of a
    second way to change a node. Creating a payload is a legitimate write, so
    it belongs in the module that already owns writing the files behind nodes
    — weakening the guard to make room for it would have traded a strong
    mechanical property for a comment (L1.07).
    """
    import locations as _loc

    src = _loc.resolve_payload_path(Path(root), ref, location)
    if src.exists() or src.is_symlink():
        return None
    src.parent.mkdir(parents=True, exist_ok=True)
    src.write_text("")
    _log_write(root, "ensure_payload", ref, src,
               text="",
               extra={"sha256": hashlib.sha256(b"").hexdigest(),
                       "payload_ref": ref, "location": str(location)})
    return src


def replace_payload(root, ref: str, source=None, *, location: str | None = None,
                    data: bytes | None = None,
                    mint_id: str = "",
                    log_extra: dict | None = None) -> tuple[Path, bool]:
    """Replace the bytes of an existing payload from `source`. Never creates.

    The other half of `ensure_payload`, and here for the same reason: a payload
    write is a real file write, and `write.py` holds a mechanically-checked
    invariant that it performs none (`test_edit_py_contains_no_file_write`).
    Editing the file behind a build node was the last node operation with no
    named command — `goal:g13.1`'s whole complaint — so it lands in the module
    that already owns writing the files behind nodes rather than weakening the
    guard that keeps the verb layer a front end.

    Returns `(path, changed)`. Refuses rather than guesses:

    - a `source` that does not exist, because a typo must not empty a payload;
    - a destination that does not exist, because replacing nothing is creating,
      and creation is `ensure_payload`'s job with its own never-overwrite rule.

    **The destination's mode is preserved**, so replacing the bytes of an
    executable does not silently disarm it — the grid reads the real mode from
    `os.lstat()` and a dropped exec bit is `goal:s9` all over again.
    """
    import locations as _loc

    if (source is None) == (data is None):
        raise ValueError("replace_payload takes exactly one of source, data")
    if source is not None:
        src = Path(source)
        if not src.is_file():
            raise FileNotFoundError(f"payload source {src} does not exist")
        data = src.read_bytes()

    dest = _loc.resolve_payload_path(Path(root), ref, location)
    if not dest.is_file():
        raise FileNotFoundError(
            f"payload {dest} does not exist — `payload` replaces bytes, it "
            f"never creates. A new file is `write.py create --payload`.")

    new = data
    if dest.read_bytes() == new:
        # hypothesis:l3-write-payload-unchanged-unlogged — a same-bytes
        # re-log IS a sanction. An explicit payload verb on bytes that
        # already match must record the (mint_id, sha256) write_guard keys on,
        # or the guard's own hint (`write.py <id> payload <path>`) can never
        # clear the state it reports: L3.27 measured 5 WARNs after 5
        # successful re-logs because this branch logged nothing. Keep
        # `changed=False` (the 'unchanged' message stays) but log the
        # attempted payload write all the same.
        _log_extra = dict(log_extra) if log_extra else {}
        _log_write(root, "replace_payload", str(ref), dest,
                   mint_id=mint_id,
                   text=new.decode("utf-8", errors="replace"),
                   extra={**{"payload_ref": str(ref), "location": str(location),
                          "changed": False}, **_log_extra})
        return dest, False
    mode = dest.stat().st_mode
    dest.write_bytes(new)
    os.chmod(dest, mode)
    _log_extra = dict(log_extra) if log_extra else {}
    _log_write(root, "replace_payload", str(ref), dest,
               mint_id=mint_id,
               text=new.decode("utf-8", errors="replace"),
               extra={**{"payload_ref": str(ref), "location": str(location)},
                      **_log_extra})
    return dest, True


def write_node(
    root,
    node_type,
    slug,
    parents=None,
    *,
    extra_fm=None,
    body=None,
    heading=True,
    bypass=False,
    rules=None,
    type_index=None,
    fm_for_gate=None,
    on_exists=SKIP,
    announce=True,
    stamp=None,
    log_extra=None,
) -> NodeWrite:
    """Create one node file, gated. The only routine that does this.

    `parents` is a list of parent ids (a bare string is accepted for the
    common one-parent call). `extra_fm` is per-caller frontmatter — a
    verdict's `verdict:`/`confidence:`, say — merged over the four keys every
    node gets. `body` defaults to the type's `BODY_PROMPTS` entry.

    `stamp` is the resolved identity of the agent the node is FOR — the
    role/model/loop/profile/season a dispatch-spawned agent will actually
    run under (hypothesis:l3-scaffold-stamps-spawner-env). When present it
    wins over os.environ for the mint stamps; the env is the fallback for a
    caller with no spawn record (a hand scaffold). Absent stays absent —
    never fabricate.


    The spawn check runs **before anything is written**, so a rejection leaves
    no node behind — the same convention `cli.py done` uses for an
    `evidence_runs` taxonomy violation. `rules`/`type_index` are accepted
    pre-loaded for callers that write several nodes in one pass
    (`post_wire.py`); omit them and they are loaded per call.

    Returns a `NodeWrite`; never raises for a rejection.
    """
    root = Path(root)
    ntype = canonical_node_type(node_type)
    if isinstance(parents, str):
        parents = [parents]
    plist = [p.strip() for p in (parents or []) if isinstance(p, str) and p.strip()]
    node_id = f"{ntype}:{slug}"
    res = NodeWrite(node_id=node_id, node_type=ntype, slug=str(slug),
                    parents=list(plist))

    current_season = None
    if rules is None or type_index is None:
        loaded_rules, loaded_index, current_season = spawn_gate.gate_for_root(root)
        rules = rules if rules is not None else loaded_rules
        type_index = type_index if type_index is not None else loaded_index
        if announce:
            spawn_gate.announce_schema_errors(rules)

    gate_fm = fm_for_gate if fm_for_gate is not None else (extra_fm or {})
    gate = spawn_gate.check_spawn(
        ntype, plist, rules=rules, type_index=type_index,
        fm=gate_fm,
        node_id=node_id, bypass=bypass,
        season_parents=gate_fm.get("season_parents"),
        current_season=current_season,
        nodes_dir=str(Path(root) / "nodes"),
    )
    if announce:
        spawn_gate.announce(gate)
    res.gate = gate
    if not gate.ok:
        res.status = REJECTED
        res.reason = gate.reason
        return res

    scaffold_body = f"\n# {node_id}\n\n" if heading else "\n"
    if body is None:
        # hypothesis:l3-done-broken-frontmatter -- anchor the body start with
        # the marker, right after the closing `---`. A kid's write tool that
        # later mangles the frontmatter leaves this line intact; `cli.py done`
        # repairs the broken `---` block up to that boundary, never past it.
        scaffold_body = BODY_BEGIN + scaffold_body
    scaffold_body += BODY_PROMPTS.get(ntype, "") if body is None else body
    node_file = node_dir(root, ntype) / f"{slug}.md"
    res.path = node_file

    if node_file.exists():
        if on_exists == SKIP or not _is_untouched_scaffold(
            node_file.read_text(encoding="utf-8"), scaffold_body
        ):
            res.status = SKIPPED
            res.reason = f"{node_file} already exists"
            return res

    fm = {
        "id": node_id,
        "mint_id": mint_permanent_id(),
        "type": ntype,
        "parents": list(plist),
        "next_edges": [],
        # mvp:unified-spawn-path clause 5 — the finish signal is "body differs
        # from the scaffold placeholder", and the placeholder's identity is
        # captured here, at write time, not re-derived at check time.
        "scaffold_hash": scaffold_hash(scaffold_body),
    }
    fm.update(extra_fm or {})
    # goal:s31 -- fill what the schema requires and this routine can derive,
    # BEFORE the file is written, so a scaffold is born valid rather than
    # waiting for a parent to notice. Safe because `scaffold_hash` hashes the
    # BODY: seeding frontmatter cannot move it, so completion detection is
    # untouched. Anything still missing is named on stderr -- the goal's third
    # candidate shape, which fixes nothing by itself but converts a silent
    # defect into a visible one.
    still_missing = seed_required(root, ntype, fm, slug)
    if still_missing and announce:
        print(f"SCHEMA-WARNING {node_id} scaffolded without "
              f"{', '.join(sorted(still_missing))} — required by "
              f"[{ntype}].md and not derivable at scaffold time (goal:s31)",
              file=sys.stderr)
    res.missing_required = list(still_missing)
    # hypothesis:l2w2-writer-stamps — season, loop, model, profile stamped
    # at mint time from environment, falling back to the ladder node's
    # current_season for season only. loop, model, profile are stamped only
    # when their env vars are present (never fabricated). Updates do NOT
    # stamp — `update_node` is deliberately separate.
    _stamp_env_fields(fm, current_season=current_season, stamp=stamp)
    spawn_gate.stamp(fm, gate)
    # hypothesis:l4-towns-each-app-is-a-vision-with-its-own-council -- a node
    # is born into a town, derived from its parents' nearest vision, default
    # core. Mint-only (updates never re-stamp); read from the shared helper so
    # the deriving rule lives exactly once. A failure must never block a mint:
    # town is a derived convenience, and the graph stops being a town graph
    # the moment a write dies for lack of one.
    try:
        fm.setdefault("town", spawn_gate.nearest_vision_town(
            str(Path(root) / "nodes"), plist))
    except Exception:
        pass

    text = _serialize_node(render_frontmatter(fm), scaffold_body)

    node_file.parent.mkdir(parents=True, exist_ok=True)
    node_file.write_text(text, encoding="utf-8")
    _log_extra = dict(log_extra) if log_extra else {}
    _log_write(root, "write_node", node_id, node_file, text,
               mint_id=fm.get("mint_id", ""),
               extra={
                   "parents": list(plist),
                   "node_type": ntype,
                   **_log_extra,
               })
    # A new file invalidates `find_node_file`'s whole-corpus index. Dropping it
    # here is what makes caching safe at all: the only routine that adds a node
    # is the only routine that has to remember.
    _ID_INDEX.pop(str(root.resolve()), None)
    res.status = WRITTEN
    return res


def _stamp_env_fields(fm: dict, *, current_season: int | None = None,
                      stamp: dict | None = None) -> None:
    """Stamp season / loop / model / profile / role into a new node's fm.

    Called from `write_node` at mint time only. `update_node` does NOT call
    this: existing nodes keep their stamps or their absence.

    - **season:** `stamp['season']` > env AGI_SEASON > ladder current_season
      > 1
    - **loop:** `stamp['loop']` if set else env AGI_LOOP; absent means absent
    - **model:** `stamp['model']` if set else env AGI_MODEL; absent = absent
    - **profile:** `stamp['profile']` if set else env AGI_PROFILE; absent =
      absent
    - **role:** `stamp['role']` if set else env AGI_ROLE; absent = absent

    `stamp` is the resolved identity of the agent a scaffold is FOR, handed
    in by the spawner at write time (hypothesis:l3-scaffold-stamps-
    spawner-env). A dispatch-spawned scaffold used to be stamped from the
    DISPATCHER's os.environ, so a kid born under a parent inherited the
    PARENT's role/model/loop. The spawner now resolves the child's row and
    passes it here; the env is the fallback for a caller with no record (a
    hand scaffold).

    A missing value with no fallback leaves the field absent — never
    fabricates a value (hypothesis:l2w2-writer-stamps).

    A deliberate non-`return` in the season branch: the old implementation
    returned after a successful AGI_SEASON parse, so in the real dispatch
    environment -- where dispatch.py sets AGI_SEASON and AGI_LOOP together --
    the loop/model/profile/role stamps never landed (measured: the
    `test_minted_node_stamps_loop_model_profile_from_env` test failed under an
    AGI_SEASON=1 shell). dispatch exports all five before it spawns, so
    stamping one must not skip the rest.
    """
    import os as _os

    def _pick(key: str, env: str):
        if stamp and stamp.get(key):
            return stamp[key]
        return _os.environ.get(env)

    env_season = _pick("season", "AGI_SEASON")
    if env_season is not None:
        try:
            fm["season"] = int(env_season)
        except (ValueError, TypeError):
            # Bad value: fall through to ladder / default.
            fm["season"] = current_season if current_season is not None else 1
    else:
        fm["season"] = current_season if current_season is not None else 1

    loop = _pick("loop", "AGI_LOOP")
    if loop is not None:
        fm["loop"] = loop.strip()

    model = _pick("model", "AGI_MODEL")
    if model is not None:
        fm["model"] = model.strip()

    profile = _pick("profile", "AGI_PROFILE")
    if profile is not None:
        fm["profile"] = profile.strip()

    # hypothesis:l3w0-ladder-roles-table — dispatch exports AGI_ROLE for
    # every spawn so a minted node records which role made it.
    role = _pick("role", "AGI_ROLE")
    if role is not None:
        fm["role"] = role.strip()


# ---------------------------------------------------------------------------
# goal:g13 — the write half. `write_node` creates; this EDITS IN PLACE.
#
# Until now nothing gated could change an existing node, so every fix, retag
# and field addition was a hand edit: no schema check, no `THOUGHT` guarantee,
# no record that a write happened at all. `goal:g13.1` names that exactly --
# a hand edit is "a completely stray and untraceable commit". This is the
# routine those edits are supposed to go through.
#
# Three properties, and the first is the one everything else depends on:
#
#   1. THE AUTHORED REGION SURVIVES. `THOUGHT` is authored, durable, and lives
#      in the body (the owner's answer, 2026-09-02). A writer that rewrote the
#      body would destroy it -- which is `goal:g2.10`, the defect that left
#      8,034 fields reading TODO(model) because a generator rewrote the whole
#      body on every run. Body is untouched unless a caller passes a new one,
#      and even then the thought is carried across.
#   2. Frontmatter is MERGED, never replaced. A caller sets the keys it owns.
#   3. An update that changes nothing reports UNCHANGED and does not write, so
#      `grid.py commit --all` does not mint a version recording no change.
# ---------------------------------------------------------------------------

#: The authored region, matched exactly as `snapshot-goals.py` and `metrics.py`
#: match it. One spelling, three readers -- a fourth regex here would be the
#: hand-maintained second copy this project keeps paying for (`goal:s17`).
_THOUGHT_RE = re.compile(
    r"<!--\s*THOUGHT:BEGIN.*?<!--\s*THOUGHT:END\s*-->", re.DOTALL)


def extract_thought(body: str) -> str | None:
    """The authored region of a body, or None. **Absent means empty.**

    Never fabricate one after the fact -- a made-up thought reads as evidence
    (`goal:g2.11`).
    """
    match = _THOUGHT_RE.search(body or "")
    return match.group(0) if match else None


def _carry_thought(old_body: str, new_body: str) -> str:
    """Put the old body's authored region into a new body that lacks one.

    Only ever ADDS. A new body that carries its own thought keeps it -- the
    writer is the author of the version and is entitled to say why it differs.
    """
    thought = extract_thought(old_body)
    if thought is None or extract_thought(new_body) is not None:
        return new_body
    return new_body.rstrip("\n") + "\n\n" + thought + "\n"


def _absorb_leading_frontmatter(fm: dict, body: str) -> tuple[dict, str, list[str]]:
    """Merge a duplicate `---` frontmatter block that opens the body.

    A kid that kept the scaffold's frontmatter in its body (L2.01,
    hypothesis:l2-done-doubled-frontmatter) leaves a second `---` YAML block
    at the top of the body. Serializing the file back with that block present
    produces a node with TWO frontmatter blocks -- which is exactly how
    `experiment:a00-e65beccc-ac5309` arrived.

    When the body (after optional leading newlines) opens with `---` and
    contains a parseable YAML mapping block, that block is merged INTO `fm`
    (**later keys winning** -- the body block is physically later in the
    file), stripped from the body, and the absorbed key names are returned.
    A body with no leading block, an unclosed block, or an unparseable
    non-mapping block is returned untouched, so kid-authored content that
    merely resembles frontmatter is never mangled.
    """
    stripped = body.lstrip("\n")
    lead = body[: len(body) - len(stripped)]
    if not stripped.startswith("---\n"):
        return fm, body, []
    lines = stripped.split("\n")
    close_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            close_idx = i
            break
    if close_idx is None or close_idx == 1:
        return fm, body, []
    yaml_block = "\n".join(lines[1:close_idx])
    try:
        import yaml
        dup = yaml.safe_load(yaml_block)
    except yaml.YAMLError:
        return fm, body, []
    if not isinstance(dup, dict):
        return fm, body, []
    absorbed = [k for k in dup if dup[k] != fm.get(k)]
    merged = dict(fm)
    merged.update(dup)  # later (body) keys win over the real frontmatter
    remaining = "\n".join(lines[close_idx + 1:])
    return merged, lead + remaining.lstrip("\n"), absorbed


def _serialize_node(fm_lines: list[str], body: str) -> str:
    """Serialize a node file to the ONE canonical shape.

    hypothesis:l4-one-serializer-ends-every-node-file-with-one-newline. The
    frontmatter reader (`load_node_file`) strips the trailing newline when it
    splits the body, so `text = frontmatter + nf.body` silently drops the
    EOF newline of a file that ended `...content\n` -- a 1-byte whitespace
    dirt that showed up after every rotate-self spawn-row write and refused
    the ack's prepare gate (`_prepare_dirty_paths`) and `_ack_seats_dirty` on
    a delta they read as dirty (the diff's no-newline-at-EOF marker).

    ONE serializer, both write sites (update_node and repair_mint). The body's
    trailing newlines are normalised to EXACTLY one -- never zero, never two
    -- so a frontmatter-only (`set_fm`) edit reproduces the body
    byte-identically including its EOF newline, and no writer can drop it.
    Nothing but trailing newlines is touched: a body that legitimately ends
    with two newlines is collapsed to one by the single-EOF rule, and
    interior blank lines are preserved.
    """
    text = "\n".join(["---", *fm_lines, "---", ""]) + body
    return text.rstrip("\n") + "\n"


def update_node(
    root,
    node_id,
    *,
    set_fm=None,
    unset_fm=(),
    body=None,
    validate=True,
    announce=False,
    log_extra=None,
) -> NodeWrite:
    """Edit one existing node in place, gated. The only routine that does this.

    `set_fm` is merged over the node's frontmatter; `unset_fm` names keys to
    drop. `body` replaces the body and is the one case where the authored
    `THOUGHT` region could be lost -- so it is carried across automatically
    unless the new body brings its own.

    Returns a `NodeWrite` whose status is `UPDATED`, `UNCHANGED` or `REJECTED`.
    Never raises for a rejection, matching `write_node`.
    """
    from graph_core.persistence import frontmatter as fm_reader

    root = Path(root)
    res = NodeWrite(node_id=str(node_id))
    path = find_node_file(root, node_id)
    if path is None:
        res.status = REJECTED
        res.reason = f"no node file for {node_id}"
        return res
    res.path = path

    try:
        nf = fm_reader.load_node_file(path)
    except Exception as exc:
        # The read half's own failure class, surfaced rather than swallowed.
        # A node that will not parse must not be silently rewritten from a
        # partial read -- that turns an unreadable node into a wrong one.
        res.status = REJECTED
        res.reason = f"{node_id} could not be parsed: {exc}"
        return res

    fm = dict(nf.frontmatter)
    res.node_type = canonical_node_type(fm.get("type") or path.parent.name)
    res.slug = path.stem
    res.parents = list(fm.get("parents") or [])

    for key in unset_fm:
        fm.pop(key, None)

    new_body = nf.body if body is None else _carry_thought(nf.body, body)

    # hypothesis:l2-done-doubled-frontmatter — a kid that kept the scaffold's
    # frontmatter in its body (L2.01: experiment:a00-e65beccc-ac5309) leaves a
    # duplicate `---` block at the top of the body. Once this writer
    # serializes the file back it would read as TWO frontmatter blocks. Absorb
    # the duplicate into the real frontmatter (later keys winning) and strip it
    # from the body, ONE writer -- the shared `cli.py done`/`post_wire` path.
    fm, new_body, _absorbed = _absorb_leading_frontmatter(fm, new_body)
    if _absorbed:
        print(
            f"warn: absorbed duplicate frontmatter from body of {node_id} "
            f"(merged {len(_absorbed)} key(s), first {_absorbed[0]!r}); "
            f"duplicate removed (l2-done-doubled-frontmatter)",
            file=sys.stderr)

    # The verdict/confidence delta wins over anything the duplicate carried,
    # so it is applied AFTER the absorb -- never clobbered by a body block.
    fm.update(set_fm or {})

    if fm == nf.frontmatter and new_body == nf.body:
        res.status = UNCHANGED
        res.reason = "nothing to change"
        return res

    if validate:
        # Judge the DELTA, not the state. An update is rejected for fields it
        # BREAKS, never for fields that were already missing when it arrived.
        #
        # Rejecting on state was the first version and it would have been a
        # live regression the moment real writers routed through here: 115
        # nodes in this corpus are already schema-invalid (`goal:s31`), so
        # `cli.py done` recording a verdict on one of them would have been
        # refused for a defect it did not cause and could not fix. A gate that
        # punishes the wrong write teaches callers to pass `validate=False`,
        # which is how a gate stops existing.
        before = set(missing_required(root, res.node_type, nf.frontmatter, node_id))
        after = missing_required(root, res.node_type, fm, node_id)
        broke = [k for k in after if k not in before]
        if broke:
            res.status = REJECTED
            res.reason = (f"{res.node_type} requires {', '.join(sorted(broke))}; "
                          f"an update may not REMOVE a required field")
            return res

    text = _serialize_node(render_frontmatter(fm), new_body)
    tmp = path.with_suffix(path.suffix + ".tmp")
    try:
        tmp.write_text(text, encoding="utf-8")
        os.replace(tmp, path)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise

    _log_extra = dict(log_extra) if log_extra else {}
    _log_write(root, "update_node", node_id, path, text,
               mint_id=fm.get("mint_id", ""),
               extra=_log_extra or None)
    res.status = UPDATED
    return res


def repair_mint(root, node_id, *, announce=True) -> NodeWrite:
    """Mint a first `mint_id` for a node written outside node_writer.

    hypothesis:l3-node-without-mint-id — a kid that writes its own node file
    with its own file tool (not through this module) leaves a node with no
    `mint_id` and no `scaffold_hash`, and `grid.py commit --all` refuses to
    version it on every grid_sync tick. No verb can adopt it either: `write.py`
    refuses `set mint_id` by design (goal:g2.5: identity is assigned once,
    never by a verb). This is that adoption — the one sanctioned path from
    "argument" to writing a node someone else left behind with no identity.

    Mints through the SAME identity source as every mint
    (`mint_permanent_id`) and stamps `scaffold_hash` of the *placeholder*
    body, so the adopted node reads complete under `completion.is_complete`
    exactly like a node `write_node` produced (real content differs from the
    placeholder -> complete). Logs the final bytes to the write-guard.

    Refuses when a non-empty `mint_id` already exists — a mint id is assigned
    once and never changed (goal:g2.5).

    Returns a `NodeWrite` with status `UPDATED` (adopted), `SKIPPED` (already
    carries a `mint_id` — the refusal), or `REJECTED` (could not find or
    parse the node). Never raises for a refusal.
    """
    from graph_core.persistence import frontmatter as fm_reader

    root = Path(root)
    res = NodeWrite(node_id=str(node_id))
    path = find_node_file(root, node_id)
    if path is None:
        res.status = REJECTED
        res.reason = f"no node file for {node_id}"
        return res
    res.path = path
    try:
        nf = fm_reader.load_node_file(path)
    except Exception as exc:
        res.status = REJECTED
        res.reason = f"{node_id} could not be parsed: {exc}"
        return res
    fm = dict(nf.frontmatter)
    res.node_type = canonical_node_type(fm.get("type") or path.parent.name)
    res.slug = path.stem
    res.parents = list(fm.get("parents") or [])
    existing = fm.get("mint_id")
    if isinstance(existing, str) and existing.strip():
        res.status = SKIPPED
        res.reason = (f"{node_id} already carries mint_id {existing.strip()}; "
                      "a mint id is assigned once and never changed "
                      "(goal:g2.5) -- refusing")
        return res
    mint = mint_permanent_id()
    fm["mint_id"] = mint
    # Stamp as complete, not as an untouched scaffold: this node already holds
    # real content (the reason it is being adopted at all), so the stamp is
    # the *placeholder* hash -- completion reads "body differs from stamp" ->
    # complete, drift-safe against a future BODY_PROMPTS change.
    ph = f"\n# {node_id}\n\n" + BODY_PROMPTS.get(res.node_type, "")
    fm["scaffold_hash"] = scaffold_hash(ph)
    text = _serialize_node(render_frontmatter(fm), nf.body)
    tmp = path.with_suffix(path.suffix + ".tmp")
    try:
        tmp.write_text(text, encoding="utf-8")
        os.replace(tmp, path)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise
    _log_write(root, "repair_mint", node_id, path, text, mint_id=mint)
    res.status = UPDATED
    if announce:
        print(f"adopted {node_id}: minted {mint} "
              f"(was missing on a node written outside node_writer)",
              file=sys.stderr)
    return res


# ---------------------------------------------------------------------------
# goal:s31 -- a scaffolded node ships schema-invalid.
#
# `[hypothesis].md` declares `required: [id, type, mint_id, title,
# testable_claim]`. `write_node` seeded neither `title` nor `testable_claim`,
# and the kid that holds the content is CORRECTLY forbidden from touching
# frontmatter. So the field was required, the writer did not supply it, and the
# one agent who could was told not to: **the node could not become valid by
# anyone doing their job as briefed.** Every hypothesis this loop ever
# scaffolded was born violating its own schema, silently.
#
# The goal names the trap in the obvious fix: do NOT solve this by telling kids
# to write frontmatter. That re-opens the `scaffold_hash` hazard and trades a
# silent invalid node for a silently broken completion check.
#
# What is safe, and is what this does: **`scaffold_hash` hashes the BODY**, so
# seeding frontmatter cannot affect completion detection at all. Two of the
# goal's three candidate shapes, together:
#
#   1. Seed at scaffold time what can be DERIVED (`title` from the slug -- a
#      real, human-readable value, never a placeholder; the `[experiment]`
#      schema already warns that declaring a field nothing writes invites
#      someone to write `TODO(model)` into it).
#   2. Validate `required` at write time and say what is still missing, so a
#      field nothing can derive becomes a visible defect rather than a silent
#      one.
#
# And the whole thing reads the schema through `schema_registry`, not through a
# hand-kept list -- the goal's own objection to patching this was that it would
# add "one more caller that agrees with the schema by convention".
# ---------------------------------------------------------------------------

#: Fields this module knows how to derive without a model. Everything else
#: required-but-absent is reported, never invented.
def _node_project_root(path: Path) -> Path | None:
    """The project root hosting a node file, derived from its own path.

    A node file lives under `<root>/nodes/<type>/...` (legacy layout) or
    `<root>/.agi/nodes/<type>/...`; the parent of the `nodes` component is the
    project root the node belongs to. Returning it lets the write log travel
    with the file rather than follow whatever `root` a caller happened to pass
    (l2w15-write-guard test-pollution fix). None when `path` has no `nodes`
    component (a payload file, or any non-node path).
    """
    try:
        parts = path.parts
        for i, part in enumerate(parts):
            if part == "nodes" and i >= 1 and i + 2 < len(parts):
                return Path(*parts[:i])
    except BaseException:
        pass
    return None


def _log_write(root, operation: str, node_id: str, path: Path,
                text: str = "", *,
                mint_id: str = "",
                extra: dict | None = None):
    """Append one JSON line to the write log under sessions/.

    Every line carries `mint_id` (SETTLED, l2w15-write-guard): the durable
    identifier the grid refs and write_guard key on, read from the node's
    frontmatter at write time. A payload write logs under its build node's
    mint_id. Absent is fine (a payload created before its node exists, or a
    legacy writer that does not pass one) — write_guard then falls back to
    sha256-only matching, which covers bytes written before a node existed.

    The log location follows the *written node*, not the caller's `root`
    (l2w15-write-guard test-pollution fix): the project hosting a node file
    is the parent of the `nodes/` component of `path`, so a write is recorded
    in that project's own sessions/ dir. A caller whose module-global root
    defaults to the real repo (snapshot_goals/level3 reusing this writer)
    cannot then leak a test-fixture node into the box's real write-log.
    Payload writes (no `nodes` component) keep the passed `root` **only when
    the file really belongs to that project** — a payload always does (it is
    resolved off `root`), but a bare fixture path in another tree (e.g. a test
    writing `tmp/n.md` under pytest) is a foreign write with no project here,
    and is **not logged anywhere** rather than leaked into the box's real
    `.agi/sessions/write-log.jsonl`.
    """
    try:
        root_p = Path(root)
        derived = _node_project_root(path)
        if derived is not None:
            root_p = derived.resolve()
        else:
            root_p = root_p.resolve()
            proj = root_p.parent if root_p.name == ".agi" else root_p
            p = path.resolve()
            inside = (str(p) == str(root_p) or str(p).startswith(str(root_p) + os.sep)
                      or str(p) == str(proj) or str(p).startswith(str(proj) + os.sep))
            if not inside:
                # Not this project's file (no node-tree component, and not
                # under root/project): it has no home in this log. Skip rather
                # than leak a foreign write into a real project's log.
                return
        log_path = root_p / WRITE_LOG
        log_path.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "ts": datetime.datetime.utcnow().isoformat() + "Z",
            "operation": operation,
            "node_id": node_id,
            "mint_id": mint_id,
            "path": _log_relpath(path, root_p),
            "sha256": hashlib.sha256(
                text.encode("utf-8")).hexdigest() if text else "",
        }
        if extra:
            entry.update(extra)
        with open(log_path, "a") as f:
            f.write(json.dumps(entry, sort_keys=True) + "\n")
    except BaseException:
        pass  # best-effort logging, never breaks a write


def log_write(root, operation: str, node_id: str, path: Path,
                text: str = "", *,
                mint_id: str = "",
                extra: dict | None = None):
    """Public wrapper for _log_write. Same signature."""
    _log_write(root, operation, node_id, path, text, mint_id=mint_id,
               extra=extra)


def _log_relpath(path: Path, root: Path) -> str:
    """Relative path from root, or absolute if not under root."""
    try:
        r = root.resolve()
        p = path.resolve()
        return str(p.relative_to(r))
    except (ValueError, OSError):
        return str(path)


def _derive_title(slug: str):
    """A human-readable title from a slug. A real value, not a placeholder.

    `title` is what every human-facing renderer keys on -- `snapshot-goals.py`,
    `dashboard.py`, the injected map. A corpus of untitled nodes renders as a
    wall of opaque ids, which is `goal:g9`'s complaint arriving from a
    direction G9 never looked.
    """
    words = str(slug).replace("_", "-").split("-")
    words = [w for w in words if w]
    if not words:
        return str(slug)
    return " ".join([words[0].capitalize(), *words[1:]])


def required_fields(root, node_type) -> list[str]:
    """The type's `validation.required` list, read from the schema registry.

    Through the registry rather than a local table, because `goal:s31`'s whole
    objection to a local patch is that it would be one more caller agreeing
    with the schema by convention instead of reading it.
    """
    try:
        from schema_registry import load_schemas_from_dir, parse_rules
    except Exception:
        return []
    try:
        reg = load_schemas_from_dir(Path(root) / "context" / "schemas")
        schema = reg.get(canonical_node_type(node_type))
        if schema is None:
            return []
        return list(parse_rules(schema.frontmatter).get("required") or [])
    except Exception:
        return []


def missing_required(root, node_type, fm, node_id="") -> list[str]:
    """Which required fields this frontmatter is actually missing.

    Delegates to `schema_registry.validate` rather than testing truthiness,
    because the registry's rule is `None` or an empty STRING -- and an empty
    LIST is present and legal. A first version here used `not fm.get(k)` and
    reported 86 goal nodes as invalid for carrying `seeds: []`, which is
    exactly what a goal with no seeds is supposed to carry.

    That mistake is `goal:s31`'s own thesis turned on its author: the objection
    to patching this locally was that a local patch "agrees with the schema by
    convention" instead of reading it, and a hand-rolled emptiness test is that
    disagreement in miniature.
    """
    required = required_fields(root, node_type)
    if not required:
        return []
    try:
        from schema_registry import validate
        errors = validate(str(node_id or fm.get("id") or ""),
                          canonical_node_type(node_type), fm,
                          {"required": required})
        return [e.field for e in errors]
    except Exception:
        return [k for k in required
                if fm.get(k) is None
                or (isinstance(fm.get(k), str) and not fm[k].strip())]


def seed_required(root, node_type, fm, slug) -> list[str]:
    """Fill what can be derived; return what is still missing.

    Mutates `fm` in place. Only ever ADDS a field that is absent or empty --
    a value already present is never overwritten, because a caller that
    supplied one knows more than a derivation does.
    """
    for name in list(missing_required(root, node_type, fm)):
        if name == "title":
            fm["title"] = _derive_title(slug)
    return missing_required(root, node_type, fm)





#: Headings a body may use to state a schema-required field, lowercased.
#: `testable_claim` is the one `[hypothesis].md` requires and no scaffold can
#: derive -- the kid holds that content and writes it into the body, which is
#: exactly where a kid is supposed to write.
_BODY_SECTIONS = {
    "testable_claim": ("testable claim", "claim", "hypothesis", "the claim"),
    "title": ("title",),
}


#: The scaffold's own question prompts. A kid who answers replaces these with
#: real prose; lifting an untouched prompt would INVENT a claim the kid never
#: made -- exactly the failure `*_invents_nothing*` guards against. A section
#: whose text is one of these is treated as absent.
_PLACEHOLDER_PARAS = {
    # the one our own scaffold ships to every hypothesis kid
    "testable_claim": "What is the testable claim? What would prove it? "
                      "What would disprove it?",
}


def _section_text(body: str, headings: tuple[str, ...]) -> str | None:
    """The first paragraph under any of `headings`, or None.

    Markdown-heading driven rather than regex-over-the-whole-body, because a
    body is prose and the heading is the only structural promise a brief
    actually makes to a kid.
    """
    lines = (body or "").splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if not stripped.startswith("#"):
            continue
        title = stripped.lstrip("#").strip().lower().rstrip(":")
        if title not in headings:
            continue
        para: list[str] = []
        for follow in lines[i + 1:]:
            if follow.strip().startswith("#"):
                break
            if not follow.strip():
                if para:
                    break
                continue
            para.append(follow.strip())
        if para:
            return " ".join(para)
    return None


def derive_required_from_body(root, node_id, announce=False) -> NodeWrite:
    """Fill schema-required fields from the body a kid just wrote (`goal:s31`).

    The completion half of the fix. A scaffold is born with everything this
    engine can derive from a slug; **the rest is content only the kid has**,
    and the kid writes it into the body because a kid writing frontmatter is
    the trade `goal:s31` explicitly forbids -- it would swap a silent invalid
    node for a silently broken completion check.

    So the kid writes prose under the heading its brief asked for, and this
    lifts it into the field the schema requires, through `update_node` and
    therefore through the gate. Nothing is invented: a field with no matching
    section stays missing and stays reported.
    """
    root = Path(root)
    path = find_node_file(root, node_id)
    if path is None:
        res = NodeWrite(node_id=str(node_id), status=REJECTED,
                        reason=f"no node file for {node_id}")
        return res

    from graph_core.persistence import frontmatter as fm_reader
    try:
        nf = fm_reader.load_node_file(path)
    except Exception as exc:
        return NodeWrite(node_id=str(node_id), status=REJECTED, path=path,
                         reason=f"{node_id} could not be parsed: {exc}")

    ntype = canonical_node_type(nf.frontmatter.get("type") or path.parent.name)
    set_fm = {}
    for name in missing_required(root, ntype, nf.frontmatter, node_id):
        text = _section_text(nf.body, _BODY_SECTIONS.get(name, ()))
        if text:
            # An untouched scaffold leaves its question prompt in place; that is
            # a non-answer, not a claim. Skip it so the field stays reported.
            if _PLACEHOLDER_PARAS.get(name) == text.strip():
                text = None
        if text:
            set_fm[name] = text
        elif name == "title":
            # The same derivation a new scaffold gets, applied to a node that
            # predates it. Still a real value from the node's own address, not
            # a placeholder -- and `title` is the field every human-facing
            # renderer keys on, so an absent one degrades the human view and
            # the agent view together (`goal:g9.7`).
            set_fm["title"] = _derive_title(path.stem)
    if not set_fm:
        return NodeWrite(node_id=str(node_id), status=UNCHANGED, path=path,
                         node_type=ntype, reason="nothing derivable from the body")
    return update_node(root, node_id, set_fm=set_fm, announce=announce)
