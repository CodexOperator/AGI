"""The brief an agent is handed, assembled by the engine. `goal:g1.9`.

**A parent should name the target and the tier, and nothing else.** Before this
module, `pi_adapter.build_command` inlined the brief, and it inlined exactly one
brief: *"fill in the scaffolded node file below, then signal done."* That is a
kid's job description. `dispatch.py --tier parent` already selected the parent
model correctly, so a parent spawned today ran on the better model and was told
to write one node and stop -- worse than useless, because it looked like it had
run a loop.

**Why this is not in the adapter.** `goal:g1.9` item 3 says tier is the only
interesting parameter of a brief, and that building the assembler inside a
dispatcher "would put the assembler inside one runtime". An adapter owns two
questions -- the argv and the environment (`goal:g4.6`) -- and brief *content*
is neither. So the adapter asks for segments and decides only how to spell them
on its own command line: `--append-system-prompt` for pi, something else for
whoever comes next. Adding a harness must not fork the brief.

**Derived, not retyped.** The verdict taxonomy comes from
`evidence_gate.VERDICT_HELP`, which is the string the gate's own regex is
documented against. That is the half of g1.9's falsifier that makes it more
than a convenience: change the taxonomy in `evidence_gate.py` and every brief
changes in the same commit, with nothing edited by hand. A brief that restates
a rule enforced elsewhere is a hand-maintained copy of a contract, and this
project has already lost a kid's verdict to exactly that drift (`goal:s8`, and
the `:N`-read-as-`0.6` incident that `VERDICT_HELP` now spells out).

**What is deliberately still missing**, so nobody reads this as g1.9 closed:

- The per-project additive override (g1.9 item 4). A project cannot yet say
  what is *special* about its briefs.
- `lib/agent-prompt.md` is still appended by the adapter as a file with no node
  behind it -- `goal:g6.6`'s complaint, which g1.9 says the assembler must not
  inherit. Moving it into graph content is a separate change.
- The map still arrives as a separate `--append-system-prompt @context_file`
  rather than through here.
"""
from __future__ import annotations

from pathlib import Path

import evidence_gate

#: Tiers a brief can be assembled for. Not the same list as
#: `adapters.TIERS`, which is about which models a harness declares -- a
#: harness may declare a tier this module has no brief for, and that should
#: fail loudly here rather than silently hand over the wrong job description.
TIERS = ("kid", "parent")


class BriefError(ValueError):
    """Raised for a tier no brief exists for."""


def _kid(*, agent_id: str, iter_n: int, cli_py: str, scaffold: dict | None) -> list[str]:
    """One node, bounded scope. Behaviour-preserving move of the old inline text.

    The wording is unchanged on purpose: it is the brief every measured
    field-note in `SKILL.md` was taken against (kids at 5-7 tool calls with an
    embedded map), and changing it in the same commit that moves it would make
    any regression impossible to attribute.
    """
    segs = [
        f"You are agent {agent_id} on iteration {iter_n}. "
        f"Your job: fill in the scaffolded node file below, then signal done."
    ]
    if scaffold:
        parent = (scaffold.get("parent") or "").strip()
        parent_arg = f" --parent {parent}" if parent else ""
        parent_line = f"Parent: {parent}" if parent else "Parent: (none — parentless node)"
        segs.append(
            f"SCAFFOLDED NODE FILE: {scaffold['path']}\n"
            f"Node type: {scaffold['node_type']}  "
            f"Node ID: {scaffold['node_id']}  "
            f"{parent_line}\n"
            f"FILL IN the body of that file. Leave frontmatter alone --\n"
            f"`cli.py done` writes `verdict`, `confidence` and\n"
            f"`evidence_runs` into it for you. Seeing those keys on a node\n"
            f"is not a request to maintain them by hand.\n"
            f"Verdict must be one of: {evidence_gate.VERDICT_HELP}\n"
            f"When done, run: python3 {cli_py} done {iter_n} {agent_id} "
            f"--verdict <state> --confidence <0..1> --node-id {scaffold['node_id']}"
            f"{parent_arg}"
            f" --evidence-runs <backing-node-id> [...]"
        )
    else:
        segs.append(
            f"When complete, run: python3 {cli_py} done {iter_n} {agent_id} "
            f"--verdict <state> --confidence <0..1> --node-id <id> --parent <parent>\n"
            f"Verdict must be one of: {evidence_gate.VERDICT_HELP}"
        )
    return segs


def _parent(*, agent_id: str, iter_n: int, cli_py: str, dispatch_py: str,
            target: str | None, parallel: int) -> list[str]:
    """A loop, not a node. `goal:g4.8`.

    Three things a parent needs that a kid does not, and each is here because
    leaving it out has a named failure:

    1. **How to spawn.** Shelling out to `dispatch.py --tier kid` rather than
       inventing a spawn path -- otherwise the parent grows a private copy of
       the loop, which is the failure `goal:g4.6`'s invariant names.
    2. **The review gate**, including that it is enforced in code and that a
       bypass is not a shortcut it may take.
    3. **The serialization rule.** `spawn.parallel` does NOT bound
       grandchildren (`experiment:a00-763e629b-5c04ad`), so a parent's own
       spawns are an unbounded population unless the parent applies the limit
       again. **This is stated here AND must be enforced at the spawn site** --
       a bound that lives only in a brief is a bound a parent can ignore, and
       `goal:g4.8` owns making it structural.
    """
    aim = target or "(pick from the injected map)"
    return [
        f"You are PARENT agent {agent_id} on iteration {iter_n}. "
        f"You run a loop. You do not write the node yourself.",
        f"TARGET: {aim}\n"
        f"Your job, in order:\n"
        f"1. SPAWN kids with:\n"
        f"     python3 {dispatch_py} <project> {iter_n} --tier kid --target <node-id>\n"
        f"   Never construct a spawn command yourself and never call the model\n"
        f"   API directly -- one spawn path, harness chosen by config.\n"
        f"2. AT MOST {parallel} kid(s) running at once. `spawn.parallel` bounds\n"
        f"   YOUR spawns only; it does not bound the kids you spawn, so you must\n"
        f"   apply this limit yourself. Serialize beyond it.\n"
        f"3. REVIEW every node a kid writes, before anything is recorded:\n"
        f"   - the `parents:` link resolves to a node that exists\n"
        f"   - the verdict is one of: {evidence_gate.VERDICT_HELP}\n"
        f"   - `proved`/`disproved` REQUIRE evidence: `evidence_runs` must be a\n"
        f"     LIST of node ids that exist, not a bare count. A bare integer\n"
        f"     certifies nothing and will be resolved to zero.\n"
        f"   - reject orphans; demote overclaims to `inconclusive_lean_*`.\n"
        f"   The gate also runs in code and will demote without you. Agreeing\n"
        f"   with it is not review -- read the kid's ARTIFACT, not its report.\n"
        f"4. DO NOT bypass the gate. `--no-evidence-gate` stamps the node\n"
        f"   `evidence_gate: bypassed` and marks it unreviewed.\n"
        f"5. DO NOT commit, push, or sync. Automation owns all remote traffic.",
        "Read `struggles:` and `caveats:` in a kid's report BEFORE reading its "
        "node. They are one line each and they are the cheapest signal in this "
        "system -- on 2026-09-01 those two lines surfaced five defects that the "
        "parent's own review had missed.",
    ]


def assemble(*, tier: str, agent_id: str, iter_n: int, cli_py: str | Path = "",
             dispatch_py: str | Path = "", scaffold: dict | None = None,
             target: str | None = None, parallel: int = 1) -> list[str]:
    """The whole brief for one agent, as ordered prompt segments.

    Returns segments rather than one string so a harness can spell them
    however its CLI wants (pi repeats `--append-system-prompt`; another
    harness may want one system prompt and one user turn). The *content* is
    this module's; the *spelling* is the adapter's.

    Raises `BriefError` for an unknown tier rather than defaulting to the kid
    brief. Defaulting is precisely the bug this module exists to fix -- a
    parent that silently receives a kid brief writes one node and stops while
    looking like it ran a loop.
    """
    if tier not in TIERS:
        raise BriefError(
            f"no brief for tier {tier!r}; known tiers: {', '.join(TIERS)}. "
            f"A tier with no brief must fail here rather than fall back to "
            f"another tier's job description (goal:g1.9)."
        )
    if tier == "parent":
        return _parent(agent_id=agent_id, iter_n=iter_n, cli_py=str(cli_py),
                       dispatch_py=str(dispatch_py), target=target,
                       parallel=parallel)
    return _kid(agent_id=agent_id, iter_n=iter_n, cli_py=str(cli_py),
                scaffold=scaffold)


def closing_line(tier: str, agent_id: str, iter_n: int) -> str:
    """The final positional prompt. Separate because pi appends it as the
    user turn rather than as a system prompt, and the two tiers end
    differently: a kid signals done, a parent reports what it reviewed."""
    if tier == "parent":
        return (f"Begin iteration {iter_n} as parent agent {agent_id}. "
                f"Read your zoom context, spawn and review kids, report what "
                f"you accepted and what you demoted.")
    return (f"Begin iteration {iter_n} as agent {agent_id}. "
            f"Read your zoom context, do the work, signal done.")
