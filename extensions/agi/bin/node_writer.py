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
    for nf in sorted(nd.rglob("*.md")):
        try:
            text = nf.read_text(encoding="utf-8")
        except Exception:
            continue
        if not text.startswith("---"):
            continue
        parts = text.split("---", 2)
        if len(parts) < 3:
            continue
        try:
            import yaml
            fm = yaml.safe_load(parts[1]) or {}
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
        for nf in sorted(d.glob("*.md")):
            try:
                text = nf.read_text(encoding="utf-8")
                if not text.startswith("---"):
                    continue
                import yaml
                fm = yaml.safe_load(text.split("---", 2)[1]) or {}
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
                # valid YAML and round-trips exactly.
                out.append(f"{indent}  - {json.dumps(i)}")
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
    parts = text.split("---", 2)
    if len(parts) < 3:
        return True
    return parts[2].strip() in scaffold_body.strip()


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
                    data: bytes | None = None) -> tuple[Path, bool]:
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
        return dest, False
    mode = dest.stat().st_mode
    dest.write_bytes(new)
    os.chmod(dest, mode)
    _log_write(root, "replace_payload", str(ref), dest,
               text=new.decode("utf-8", errors="replace"),
               extra={"payload_ref": str(ref), "location": str(location)})
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
) -> NodeWrite:
    """Create one node file, gated. The only routine that does this.

    `parents` is a list of parent ids (a bare string is accepted for the
    common one-parent call). `extra_fm` is per-caller frontmatter — a
    verdict's `verdict:`/`confidence:`, say — merged over the four keys every
    node gets. `body` defaults to the type's `BODY_PROMPTS` entry.

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
    )
    if announce:
        spawn_gate.announce(gate)
    res.gate = gate
    if not gate.ok:
        res.status = REJECTED
        res.reason = gate.reason
        return res

    scaffold_body = f"\n# {node_id}\n\n" if heading else "\n"
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
    _stamp_env_fields(fm, current_season=current_season)
    spawn_gate.stamp(fm, gate)

    text = "\n".join(["---", *render_frontmatter(fm), "---", ""]) + scaffold_body

    node_file.parent.mkdir(parents=True, exist_ok=True)
    node_file.write_text(text, encoding="utf-8")
    _log_write(root, "write_node", node_id, node_file, text, extra={
        "parents": list(plist),
        "node_type": ntype,
    })
    # A new file invalidates `find_node_file`'s whole-corpus index. Dropping it
    # here is what makes caching safe at all: the only routine that adds a node
    # is the only routine that has to remember.
    _ID_INDEX.pop(str(root.resolve()), None)
    res.status = WRITTEN
    return res


def _stamp_env_fields(fm: dict, *, current_season: int | None = None) -> None:
    """Stamp season / loop / model / profile into a new node's frontmatter.

    Called from `write_node` at mint time only. `update_node` does NOT call
    this: existing nodes keep their stamps or their absence.

    - **season:** env AGI_SEASON > ladder current_season > 1
    - **loop:** env AGI_LOOP only; absent means absent
    - **model:** env AGI_MODEL only; absent means absent
    - **profile:** env AGI_PROFILE only; absent means absent

    A missing env var with no ladder fallback leaves the field absent — never
    fabricates a value (hypothesis:l2w2-writer-stamps).
    """
    import os as _os

    env_season = _os.environ.get("AGI_SEASON")
    if env_season is not None:
        try:
            fm["season"] = int(env_season)
            return  # successful parse — skip fallback chain
        except (ValueError, TypeError):
            pass  # bad value: fall through to ladder / default
    if current_season is not None:
        fm["season"] = current_season
    else:
        fm["season"] = 1

    loop = _os.environ.get("AGI_LOOP")
    if loop is not None:
        fm["loop"] = loop.strip()

    model = _os.environ.get("AGI_MODEL")
    if model is not None:
        fm["model"] = model.strip()

    profile = _os.environ.get("AGI_PROFILE")
    if profile is not None:
        fm["profile"] = profile.strip()


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


def update_node(
    root,
    node_id,
    *,
    set_fm=None,
    unset_fm=(),
    body=None,
    validate=True,
    announce=False,
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
    fm.update(set_fm or {})

    new_body = nf.body if body is None else _carry_thought(nf.body, body)

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

    text = "\n".join(["---", *render_frontmatter(fm), "---", ""]) + new_body
    tmp = path.with_suffix(path.suffix + ".tmp")
    try:
        tmp.write_text(text, encoding="utf-8")
        os.replace(tmp, path)
    except BaseException:
        tmp.unlink(missing_ok=True)
        raise

    _log_write(root, "update_node", node_id, path, text)
    res.status = UPDATED
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
def _log_write(root, operation: str, node_id: str, path: Path,
                text: str = "", *,
                extra: dict | None = None):
    """Append one JSON line to the write log under sessions/."""
    try:
        root_p = Path(root)
        log_path = root_p / WRITE_LOG
        log_path.parent.mkdir(parents=True, exist_ok=True)
        entry = {
            "ts": datetime.datetime.utcnow().isoformat() + "Z",
            "operation": operation,
            "node_id": node_id,
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
                extra: dict | None = None):
    """Public wrapper for _log_write. Same signature."""
    _log_write(root, operation, node_id, path, text, extra=extra)


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
    "testable_claim": ("testable claim", "claim"),
    "title": ("title",),
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
