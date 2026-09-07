---
id: experiment:a00-2b79aea7-29861b
mint_id: bbc08bee8b544fab86ac81bb7f8f5271
type: experiment
parents:
  - hypothesis:l3w3-advisor-brief
next_edges: []
confidence: 0.7
edited_by: ubuntu
evidence_runs:
  - experiment:a00-2b79aea7-29861b
loop: hypothesis:l3w3-advisor-brief@s2
model: ~z-ai/glm-flash-latest
profile: balanced
role: parent
scaffold_hash: beb2e1cf8b3b9205
season: 2
title: A00 2b79aea7 29861b
verdict: proved
---
# experiment:a00-2b79aea7-29861b

## Experiment

Built the L3.13 addendum deliverable (hypothesis:l3w3-advisor-brief, addendum
after L3.12): the advisor DUTIES block in `brief.assemble(tier=advisor)` now
carries real, runnable commands instead of the `dispatch.py <project> <iter>`
placeholder.

What I did, in order:

1. **`extensions/agi/bin/brief.py`**
   - New `_resolve_perpetual_goals(project_root)` reads every `goal_kind:
     perpetual` goal node (g1, g15, g16) and returns `(id, title)`, so the
     brief lists the real perpetual goals with titles instead of a hardcoded
     list.
   - New `_WAVE3_GATE` constant, owner-verbatim: "one short-term subgoal
     under the perpetual goal closed with a judged outcome and no human hand
     on a node".
   - Rewrote `_advisor(...)`: resolves the dispatch path (from the spawn site
     or defaulting to `extensions/agi/bin/dispatch.py`), derives sibling
     `send.py`/`rotate.py`/`season.py` paths, substitutes the resolved project
     root and iteration id into the spawn primitive, names the advisor's own
     `agent_id` (and `session_dir` when the pi harness supplies it) on the
     room read, pins which director to spawn when `--goal goal:<id>` is set,
     and otherwise says the assignment arrives from the prime in
     `tier3-quorum` and to READ THE ROOM FIRST. Duties 1-4 and the
     "DO NOT run git" line are kept; the head's Michael line and the vision
     body are untouched.
   - `assemble(...)` gained `goal` and `session_dir` params; the advisor
     branch resolves `goal = explicit or os.environ["AGI_ADVISOR_GOAL"]`.

2. **`extensions/agi/bin/dispatch.py`** (`--goal flag only`)
   - Added `--goal goal:<id>` argument and `apply_advisor_goal_env()`, which
     seeds/clears `AGI_ADVISOR_GOAL`. Wiring is via env (not a new keyword on
     every harness adapter) because `claude_code_adapter.py` belongs to
     another kid this round and I was told not to touch it.

3. **`extensions/agi/bin/adapters/pi_adapter.py`** — forwards `session_dir`
   into `brief.assemble` (cc_adapter untouched).

4. **`extensions/agi/tests/test_brief.py`** — red-first tests, all now green:
   real runnable dispatch/send/rotate commands, perpetual goals listed with
   titles, `--goal goal:g15` pins the director with its title, wave-3 gate
   verbatim, and the six duties + git line kept.

5. **`extensions/agi/tests/test_dispatch.py`** — `--goal` flag accepted by the
   argparser and `apply_advisor_goal_env` seeds/clears the env.

## Evidence

Verify commands (each with actual output):

```
$ unset AGI_ADVISOR_GOAL
$ python3 -m pytest extensions/agi/tests/test_brief.py extensions/agi/tests/test_dispatch.py -q
........................................................................ [ 66%]
....................................                                     [100%]
108 passed in 2.90s
```

L3.13 red-first advisor tests (within the 108): duties spell runnable
`extensions/agi/bin/dispatch.py` / `send.py` commands; the resolved iter id is
in the spawn command; `AGI_ADVISOR_GOAL=goal:g15` yields `--target goal:g15`
and "G15: Bugfix and optimization"; the wave-3 gate sentence renders verbatim.

Assembled DUTIES block, pinned (`AGI_ADVISOR_GOAL=goal:g15`, iter L3.13):

```
YOUR DUTIES
1. Sit the quorum: stay a standing member of the room tier3-quorum — ...
     python3 extensions/agi/bin/send.py send --room tier3-quorum <text>
     python3 extensions/agi/bin/send.py read --room tier3-quorum --me a00-2b79aea7
2. The prime is inbox-only; ... `extensions/agi/bin/send.py audience prime --reason <why> [--morals]`; ... Belam.
3. Perpetual-goal assignment — you are PINNED to goal:g15 — G15: Bugfix and optimization.
     python3 extensions/agi/bin/dispatch.py /home/ubuntu/work/agi/.agi L3.13 --tier director --role director --ladder-tier 1 --target goal:g15 --detach
     python3 extensions/agi/bin/rotate.py loop --role director
   Review each director's rounds ... with `extensions/agi/bin/season.py judge` ...
   WAVE-3 GATE: one short-term subgoal under the perpetual goal closed with a judged outcome and no human hand on a node.
4. NEVER edit vision prose. ...
```

Unpinned variant names goal:g15 / goal:g16 with titles and says "READ THE ROOM
FIRST — `...send.py read --room tier3-quorum --me <id>`".

L3.12 routing tests still pass unchanged (`test_brief_tier_routes_tier3_vision_parent_to_advisor` and siblings, green in the 108).

Full suite (`python3 extensions/agi/bin/commands.py run tests`):
**1801 passed, 1 skipped, 4 failed** — the four failures are ALL in
`extensions/agi/tests/test_claude_code_adapter.py` (tools_by_role, director
tier model, advisor tier-3 tools). `claude_code_adapter.py` is the file the
L3.13 addendum says another kid edits this round; I did not touch it, and none
of my changes feed it. Nothing else failed.

No git ran. No commit. Unexpected files: `claude_code_adapter.py` /
`test_claude_code_adapter.py` carry another kid's in-flight, uncommitted edits
(4 red tests there) — left exactly where they are.

## Agent Notes
Advisor DUTIES block built: real runnable dispatch/send/rotate commands, perpetual goals listed w/ titles, --goal pins director, wave-3 gate verbatim; brief+dispatch+pi tests green (108). Full suite 4 fails all in cc_adapter (another kid's file, untouched).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
L3.13 kid (a00-2b79aea7) implemented the addendum after L3.12: advisor DUTIES block now carries real runnable commands with resolved project root, iter id and agent id; perpetual goals g1/g15/g16 read from the graph with titles; --goal goal:<id> pins the spawned director (via AGI_ADVISOR_GOAL env, deliberately not cc_adapter keywords); wave-3 gate verbatim; duties 1-4 + no-git line kept; head Michael line and vision body untouched. Parent verified independently: test_brief+test_dispatch 108 green, git diff touches only brief.py/dispatch.py/pi_adapter.py, claude_code_adapter.py (another kid in-flight, 4 red tests there) untouched. Verdict proved confirmed; caveat noted that ultracode-env half of the original claim still lives in the in-flight cc_adapter work.
<!-- THOUGHT:END -->

Parent review (a00-7bf85a4d, L3.13): ACCEPTED as proved. Checked report struggles/caveats, read node + artifact, ran the verify commands myself, confirmed diff scope. No demotion.
