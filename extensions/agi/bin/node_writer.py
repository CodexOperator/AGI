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
    "bigger_outcome", "app_purpose",
)
TYPE_ALIASES = {"bigger-outcome": "bigger_outcome", "app-purpose": "app_purpose"}
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
    "app_purpose": "## App Purpose\n\nWhat is the top-level mission this chain serves?\n\n",
}

#: Frontmatter keys that lead, in this order. Everything else follows sorted,
#: so two writers producing the same node produce the same bytes.
LEADING_KEYS = ("id", "mint_id", "type", "parents", "next_edges")

WRITTEN = "written"
SKIPPED = "skipped"
REJECTED = "rejected"

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


def _needs_quoting(sval: str) -> bool:
    """True when a scalar would not survive the cheap frontmatter parsers.

    Every writer path here splits on `---` and hands the middle to
    `yaml.safe_load`, so the value has to be real YAML. `verdict:x` is fine —
    a colon with no space after it is part of a plain scalar, which is why
    every node id in the corpus is written bare and why quoting them here
    would be a gratuitous reformat. `no node: ['x']` is not fine, and that is
    a real `spawn_check_reason` this routine can emit.
    """
    if not sval:
        return False
    if ": " in sval or sval.endswith(":") or " #" in sval:
        return True
    return sval[0] in "\"'[{&*!|>%@`#-?:,"


def render_frontmatter(fm: dict) -> list[str]:
    """`fm` -> the lines between the `---` markers. Deterministic."""
    ordered = [k for k in LEADING_KEYS if k in fm]
    ordered += sorted(k for k in fm if k not in LEADING_KEYS)
    lines = []
    for k in ordered:
        v = fm[k]
        if isinstance(v, (list, tuple)):
            if not v:
                lines.append(f"{k}: []")
            else:
                lines.append(f"{k}:")
                lines.extend("  -" if i is None else f"  - {i}" for i in v)
        elif isinstance(v, bool):
            lines.append(f"{k}: {str(v).lower()}")
        elif v is None:
            lines.append(f"{k}:")
        else:
            sval = str(v).replace("\n", " ").strip()
            if _needs_quoting(sval):
                esc = sval.replace("\\", "\\\\").replace('"', '\\"')
                sval = f'"{esc}"'
            lines.append(f"{k}: {sval}")
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

    if rules is None or type_index is None:
        loaded_rules, loaded_index = spawn_gate.gate_for_root(root)
        rules = rules if rules is not None else loaded_rules
        type_index = type_index if type_index is not None else loaded_index
        if announce:
            spawn_gate.announce_schema_errors(rules)

    gate = spawn_gate.check_spawn(
        ntype, plist, rules=rules, type_index=type_index,
        fm=fm_for_gate if fm_for_gate is not None else (extra_fm or {}),
        node_id=node_id, bypass=bypass,
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
    }
    fm.update(extra_fm or {})
    spawn_gate.stamp(fm, gate)

    text = "\n".join(["---", *render_frontmatter(fm), "---", ""]) + scaffold_body

    node_file.parent.mkdir(parents=True, exist_ok=True)
    node_file.write_text(text, encoding="utf-8")
    res.status = WRITTEN
    return res
