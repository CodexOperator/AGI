# CC-native dispatch — loop iterations via Claude Code subagents

Alternative dispatch path: instead of `dispatch.py` spawning pi subprocesses,
a Claude Code session acts as **overseer** and spawns builder kids with the
Agent tool. Same graph, same node format, same chain workflow
(`lib/agent-prompt.md`) — different runtime.

General-purpose: works in any project with `autoresearch-tree.config.json`.
Project repos may carry their own customizations (goal docs, metric choice);
this file stays generic.

## When to use which runtime

| | pi harness (`driver.sh --max-iters N`) | CC-native dispatch |
|---|---|---|
| Billing | pi's own auth (`~/.pi/agent/auth.json`) | Claude Code subscription |
| Models | whatever pi is keyed for | any Claude model per kid |
| Supervision | heal.py timeouts, unattended | overseer reviews every node before commit |
| Best for | long unattended runs, cheap/OS models | supervised runs, model tiering, no pi auth for target provider |

`dispatch.py` scrubs `ANTHROPIC_*`/`CLAUDE_CODE_*` from pi child envs on
purpose (subscription quota-leak fix — HANDOFF §5c). CC-native dispatch is the
sanctioned way to spend Claude subscription tokens on the loop. Never bypass
the scrub instead.

## Iteration protocol (overseer)

One iteration = one node per kid, reviewed and committed by the overseer.

1. **Snapshot + render:** `bash <engine>/extensions/agi/driver.sh --smoke --max-iters 1`
   from inside the project. Records METRIC baseline, refreshes `context/INJECTION.md`.
   Verify node count did not drop (H0 paranoia).
2. **Pick zoom targets** from INJECTION.md, mirroring `dispatch.py`:
   - Slot 0 → BIG zoom: whole-graph context, fresh idea or top-level fork.
   - Slot 1..N → SMALL zoom: top attractor by descendant count, 2-hop subtree.
   N = `agent_dispatch.claude_max_parallel` from config.
3. **Spawn kids** (Agent tool, parallel, background). Each kid prompt must be
   self-contained: zoom scope, target parent node id, chain step to perform
   (agent-prompt.md steps A–E), node file format sample, verdict taxonomy,
   project paths (INJECTION.md, goals doc, spec). Explicit deltas from
   agent-prompt.md rules:
   - **Do NOT commit** (overrides rule 5) and do NOT call `cli.py done`
     (rule 6) — write the node file(s), report, stop. The overseer owns
     commit and record-keeping.
   - One node added or extended, nothing else (rule 2 unchanged).
4. **Review (the gate).** For each kid's node: parent link resolves, taxonomy
   valid, and — H4, enforced here because the cli gate is unbuilt —
   `proved`/`disproved` verdicts REQUIRE experiment evidence
   (`evidence_runs >= 1`); demote unevidenced verdicts to `pending` or
   `inconclusive_lean_*`. Reject orphans.
5. **Commit** accepted nodes in one commit:
   `iter-N cc-dispatch: <kid-a summary>; <kid-b summary>`.
6. **Re-render:** `--smoke` again; report METRIC deltas. Primary metric per
   project config — do not optimize raw chain length (H3: proven gameable).

## Model tiering

The tier map rides the zoom axis: overseer = strongest available model (goal
custody + review gate), BIG-zoom kid = mid tier (fresh ideas need judgment),
SMALL-zoom kids = cheapest capable tier (bounded 2-hop work). As zoom levels
generalize beyond BIG/SMALL, assign one tier per level; each level's output is
reviewed at the level above.

## Safety rails (inherited, non-negotiable)

- Never create project-local `bin/snapshot-build-site.py` or
  `bin/render-context.py` (TODO.md H0/H0b — stale overrides silently wipe
  `nodes/`).
- Engine improvements → engine repo; graph/domain output → project repo
  (agent-prompt rule 11).
- Kids that stall or wander out of zoom scope: kill, log, respawn narrower —
  the CC analogue of heal.py.
