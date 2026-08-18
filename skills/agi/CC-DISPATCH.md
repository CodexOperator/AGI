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
   - **End-of-job contract — keep it minimal.** The kid's final message is:
     ```
     DONE <node-id>
     caveats: <optional, one line>
     struggles: <optional, one line>
     question: <optional — ONLY under the four escalation triggers>
     ```
     plus whatever numbers the brief asked for. Nothing else is required:
     no git, no push, no sync, no cli.py — spending tokens on any of those
     is waste; automation owns all remote traffic.
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

## Field notes (validated on a live 6-iteration run, 2026-08-18)

- **Embed the map, don't reference it.** Generate the per-agent context with
  `bin/zoom.py <project> <iter> <agent_id> --level big|small [--target id]`,
  then paste the rendered map INTO the kid's spawn prompt. Kids spend zero
  tool calls orienting; observed drop from 11–13 to 5–7 calls per kid.
- **Healing (CC analogue of heal.py).** On an API-error death: check the
  filesystem BEFORE resuming — kids often die after the node file landed,
  losing only their report; then the artifact is reviewable and no resume is
  needed. Otherwise resume the same agent (transcript context intact) rather
  than respawning cold. On 529 overload waves, back off 60s+ before resuming,
  and give resumed kids a degraded-mode fallback (fewer trials with the
  reduced n recorded honestly) so a wave can't stall the run.
- **Parallel-kid hygiene.** Kids see each other's untracked files in
  `git status`. Instruct: report unexpected files, never touch or clean them.
  Kids reliably flag them unprompted — treat that as the expected behavior.
- **Verdict precedent.** Judge the chain's CORE claim; when a mechanism
  prescription inside the hypothesis fails but the core claim survives,
  return the verdict on the core claim and name the failed prescription as
  explicitly unendorsed. State the proved invariant at the level it actually
  holds — overclaiming in a verdict poisons every downstream reader.
- **Cheap-agent experiments stay cheap.** When a hypothesis is about what
  weak models do, the orchestrating kid must dispatch genuinely weak
  subagents (e.g. haiku) for those roles and keep ground truth + scoring to
  itself, with scratch under gitignored `sessions/`, never `nodes/`.

## Kid → overseer questions (escalation)

Kids MAY ask the overseer mid-task: call SendMessage with `to: "main"`, state
the decision and the options; the kid's turn ends, the overseer answers via
SendMessage, and the kid resumes with its context intact. No engine change —
this is the same resume mechanics healing uses, kid-initiated.

Default remains **decide and document**: make the call, record it honestly in
the node body as a deviation/judgment (verdict writers weigh it later). The
one-node scope keeps most calls small; every question is a full stop plus a
round trip, so escalation is reserved for exactly four triggers:

1. The task genuinely requires touching a file the hard rules forbid.
2. Embedded instructions contradict repo reality AND the resolution would bind
   future chain nodes (a wrong local call poisons downstream work).
3. An irreversible or destructive operation.
4. Cost blowup — the honest execution needs far more trials/tokens/time than
   the brief implied.

Budget: one question per kid per iteration. Spawn prompts should include a
one-line pointer to this rule; kids without it default to decide-and-document,
which the first live run showed opus-tier kids do well (three judgment calls,
all correct, all documented). The pi dispatch path has no question channel —
fire-and-forget by design; escalation is a CC-dispatch feature.

## The git grid (D2 node versions, D3 session drafts)

`bin/grid.py` adds two version dimensions beside the project repo's own
history (D1). The grid is BAKED INTO the project repo as a dedicated ref
namespace — `refs/grid/node/*` and `refs/grid/session/*` — never checked out,
invisible to `git branch`, blobs deduped against D1, one remote syncs all
dimensions. `grid.py init` configures the origin fetch refspec
(`+refs/grid/*:refs/grid/*`) so fresh clones can pull the grid.

- **Overseer, after every iteration commit (protocol step 5):**
  `python3 <engine>/bin/grid.py commit --all` — every changed node gains a
  version on its `node/<id>` branch. Unchanged nodes get nothing: versions
  record change, not time.
- **Kid drafts (D3):** before review, the overseer may snapshot a kid's
  candidate file: `grid.py commit <file> --session <iter> <agent>` →
  `session/<iter>/<agent>/<id>`. Rejected drafts survive there; accepted
  content lands on the node branch at the next `commit --all`. Nothing is
  lost either way.
- **D3 is the CC analogue of pi's `tree`:** fork-type subagents branch the
  parent conversation, and background kid transcripts are resumable
  (SendMessage) — both are context branches that save parent tokens. Grid
  session branches are their durable, diffable file-level record.
- **Inspect:** `grid.py log <id>` / `diff <id> [--back N]` / `versions <id>`
  (the vN marker) / `status` (drift vs branch tips).
- **Sync is AUTOMATED — nobody syncs by hand.** `grid.py cron install` sets
  both cadences in one shot (idempotent per project; `cron show|remove` to
  inspect/uninstall):
  - every 5 min (`--snapshot-mins N` to tune): auto-snapshot
    (`commit --all --prefix 'cron: '`) + push `refs/grid/*` — in-flight node
    edits become durable; an idle graph pushes nothing (change-only
    versioning). Crash-recovery window ≤ N minutes.
  - hourly: push the D1 branch — the reviewed, curated sync.
  Neither kids nor the overseer run `push` or `sync` manually; the overseer's
  only git surface is the local iteration commit, a kid's is nothing at all.
  The `cron:` prefix keeps auto-snapshots distinguishable from
  overseer-reviewed versions in `grid.py log`. Concurrency note: `update-ref`
  is atomic per ref but last-writer-wins; per-ref CAS is TODO H10 if many
  agents ever race the same node.

## Safety rails (inherited, non-negotiable)

- Never create project-local `bin/snapshot-build-site.py` or
  `bin/render-context.py` (TODO.md H0/H0b — stale overrides silently wipe
  `nodes/`).
- Engine improvements → engine repo; graph/domain output → project repo
  (agent-prompt rule 11).
- Kids that stall or wander out of zoom scope: kill, log, respawn narrower —
  the CC analogue of heal.py.
