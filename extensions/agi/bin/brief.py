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
        f"Your job: fill in the scaffolded node file below, then signal done.",
        # goal:s28 session, 2026-09-02 -- a kid ran `git add -A && git commit`
        # and swept up 37 lines of a CLAUDE.md section the director had
        # mid-edit. It was not the kid's fault: `SKILL.md` forbids kids from
        # committing, the parent brief forbids it, and THIS brief did not say
        # it. That is `goal:g1.9`'s whole argument arriving as an incident --
        # a rule enforced in three documents and absent from the one string the
        # agent actually receives.
        "DO NOT run git. No commit, no add, no push, no stash, no checkout. "
        "Automation owns all remote traffic and the parent owns commits. "
        "`git add -A` is especially forbidden: other agents and the director "
        "have uncommitted work in this tree, and it WILL be swept into your "
        "commit. If you see unexpected files, report them in one line and "
        "leave them exactly where they are.",
        "RUN THE REPO TEST SUITE before you report, if you changed any code: "
        "`python3 -m pytest extensions/agi/tests/ -q`. Your own scratch test "
        "passing is not the same claim. A failing assertion you did not expect "
        "is usually the assertion working.",
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
            target: str | None, parallel: int, max_live: int = 1) -> list[str]:
    """A loop, not a node. `goal:g4.8`.

    Three things a parent needs that a kid does not, and each is here because
    leaving it out has a named failure:

    1. **How to spawn.** Shelling out to `dispatch.py --tier kid` rather than
       inventing a spawn path -- otherwise the parent grows a private copy of
       the loop, which is the failure `goal:g4.6`'s invariant names.
    2. **The review gate**, including that it is enforced in code and that a
       bypass is not a shortcut it may take.
    3. **The serialization rule, which is now enforced rather than requested.**
       `spawn.parallel` does NOT bound grandchildren
       (`experiment:a00-763e629b-5c04ad`), so a parent's own spawns were an
       unbounded population as long as the limit lived only in this text. As
       of `goal:g4.8` item 3 the tree carries a lease per live agent and
       `dispatch.py` refuses admission past `spawn.max_live` -- so a parent
       that ignores the rule gets **refused slots**, not extra processes. The
       sentence stays in the brief because a parent that knows the bound plans
       around it instead of discovering it as an unexplained failure.
    4. **What its artefact is** (`goal:s27`). A parent authors no node. It is
       responsible for its kids' nodes, so it signals done with `--owns` and
       puts its review into those nodes' `THOUGHT` blocks -- which is honest
       rather than a workaround, because a parent's edit to a kid's node IS a
       new version of it, and the thought is by definition the reasoning
       behind the version.

       **Named as a stopgap in the brief itself**, deliberately. Once a
       session is linked to the versions it produced (`goal:g2.7`,
       `goal:g10.1`), a parent's full review reaches a reader through the
       node's high-LOD view and never needs compressing into prose. Telling
       the parent that now costs one sentence and stops the compression from
       being mistaken for the design.
    """
    aim = target or "(pick from the injected map)"
    return [
        f"You are PARENT agent {agent_id} on iteration {iter_n}. "
        f"You run a loop. You do not write the node yourself.",
        f"TARGET: {aim}\n"
        f"Your job, in order:\n"
        f"1. SPAWN kids with:\n"
        f"     python3 {dispatch_py} <project> {iter_n} --tier kid --detach --target <node-id>\n"
        f"   The `--detach` flag makes dispatch return immediately after spawning\n"
        f"   (no reaper phase). The kid runs detached; poll its status with:\n"
        f"     python3 {cli_py} status {iter_n}\n"
        f"   until the kid's status is `done` or `failed`. Sleep 30 seconds\n"
        f"   between polls so each poll is a short tool call that never outlives\n"
        f"   the harness timeout.\n"
        f"   Never construct a spawn command yourself and never call the model\n"
        f"   API directly -- one spawn path, harness chosen by config.\n"
        f"2. AT MOST {parallel} kid(s) running at once, and AT MOST {max_live}\n"
        f"   agent(s) alive ANYWHERE in this tree -- you and every other parent\n"
        f"   and kid count against the same {max_live}. That second bound is\n"
        f"   enforced in code, not requested: a slot past it is REFUSED and\n"
        f"   logged as `unadmitted` in the manifest, never queued. So serialize\n"
        f"   your kids rather than firing them all and hoping.\n"
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
        f"5. DO NOT commit, push, or sync. Automation owns all remote traffic.\n"
        f"6. SIGNAL DONE when every kid is finished:\n"
        f"     python3 {cli_py} done {iter_n} {agent_id} --verdict pending \\\n"
        f"       --owns <kid-node-id> [<kid-node-id> ...]\n"
        f"   `--owns`, NOT `--node-id`. You author no node of your own.",
        "YOUR ARTEFACT IS YOUR KIDS' NODES. You are responsible for them the "
        "way a parent is responsible for its children, not for some separate "
        "object of your own. Nothing is scaffolded for you and nothing should "
        "be.\n"
        "So put your review WHERE THE WORK IS: edit a kid's node in place, and "
        "write why the node now says what it says into that node's THOUGHT "
        "block:\n"
        "  <!-- THOUGHT:BEGIN -->\n"
        "  why this version differs from the previous one\n"
        "  <!-- THOUGHT:END -->\n"
        "Your edit IS a new version of that node, so the thought describing it "
        "is legitimately yours. Rewrite it from scratch; never append. Never "
        "fabricate one — absent means empty.\n"
        "This is a stopgap and is meant to be: once sessions are linked to the "
        "versions they produced (goal:g2.7, goal:g10.1), your full review "
        "reaches a reader through the node's high-LOD view and stops needing "
        "to be compressed into prose at all.",
        "Read `struggles:` and `caveats:` in a kid's report BEFORE reading its "
        "node. They are one line each and they are the cheapest signal in this "
        "system -- on 2026-09-01 those two lines surfaced five defects that the "
        "parent's own review had missed.",
    ]


def assemble(*, tier: str, agent_id: str, iter_n: int, cli_py: str | Path = "",
             dispatch_py: str | Path = "", scaffold: dict | None = None,
             target: str | None = None, parallel: int = 1,
             max_live: int = 1) -> list[str]:
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
                       parallel=parallel, max_live=max_live)
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
