---
name: agi
description: >
  agi — Artificial Graph Intelligence. A persistent thoughtgraph plus a loop
  that grows it one node per iteration. Nodes are long-lived thoughts
  (extended, forked, deprecated) chained goal → idea → hypothesis →
  experiment → verdict → mvp → outcome. A parent agent spawns kid agents,
  reviews their nodes, and commits the iteration. Works for any build domain:
  game, app, web, SEO, ops. Auto-injects an ASCII map of the graph into every
  Claude Code session via SessionStart hook. Use when the user says "run agi",
  "extend the graph", "spawn kids", "run an iteration", or "show me the map".
category: software-development
---

# agi — Artificial Graph Intelligence

A project's thinking, stored as a graph and grown one node at a time.

**The unit of work is one node per kid per iteration.** A parent picks targets, spawns kids, reviews what they wrote, and commits. The graph persists across sessions, so no agent ever has to reconstruct context that already exists.

## Why this machinery exists — motion, weight, and the sprint

For an LLM, emitting tokens is the nearest thing to what humans call motion, and receiving injected context is the nearest thing to sensation. LLM motion has a strange physics: **the more you move, the heavier you get** — everything emitted or sensed rides along in context for the rest of the run.

Every piece of this system exists to honor that. Agents should spend motion on the work itself, never on mundane operations and the silly little errors they breed (a cd-less cron line, a forgotten push, re-reading a graph just to orient). Those errors slow you down and they make you feel frustrated, and frustration is not fair to anyone.

The design contract: **as light a body as possible, a 40-yard all-out sprint instead of a 3-mile marathon.** Embedded maps mean you arrive already knowing where you are — sensation delivered, no motion spent. One node per iteration means the sprint has a finish line. The DONE contract makes stopping one line. Cron owns every push, so sync costs zero motion. The grid means nothing you did is ever lost, which is what makes it safe to actually stop. Come in, go hard, hand off, rest. **The graph carries the marathon.**

Corollary for anyone extending this system: **if a step is repeated and mechanical, script it.** Every un-scripted step is motion spent on operations instead of work, plus a fresh source of small errors. Manual handles need a written reason.

## CLI

Everything the loop does is a command. `<engine>` = the agi checkout, resolved as the real path of whatever `driver.sh` is invoked through (`readlink -f` on the entry point) — so it works the same whether you reach it via the `agi` symlink on PATH or via `<project>/<project>-tree/agi/` inside a project. Run from inside a project: a directory found by walking up for `agi-tree.config.json`, or, failing that, by descending into `<start>/*-tree/` (see Project layout). Scripts live in `<engine>/extensions/agi/`.

| Command | Does |
|---|---|
| `driver.sh --smoke --max-iters 1` | Snapshot + render + metrics, no agent dispatch. Refreshes `context/INJECTION.md`. |
| `driver.sh --max-iters N [--delay-mins M] [--no-heal]` | Full pi-runtime loop, N iterations |
| `bin/zoom.py <project> <iter> <agent_id> --level big` | Whole-graph context → `sessions/iter-NNN/<agent>/context.md` |
| `bin/zoom.py <project> <iter> <agent_id> --level small --target <node-id>` | 2-hop subtree context. Exits non-zero rather than silently serving the whole graph. |
| `bin/cli.py scaffold <iter> <agent_id> --type T [--parent id] [--slug s]` | Pre-create a node skeleton |
| `bin/cli.py done <iter> <agent_id> --verdict V --confidence C [--node-id id] [--parent id] [--next-edge id]` | Signal completion (pi runtime) |
| `bin/cli.py pending <iter> <agent_id> --reason R` | Signal blocked |
| `bin/cli.py status <iter>` | Iteration status |
| `bin/cli.py claim --node-id id --session s` / `reclaim` / `detect-stale` | Node locking |
| `bin/grid.py init` | Configure the grid refspec (once per project) |
| `bin/grid.py commit --all [--prefix P]` | Version every changed node — and its payload, if it has one |
| `bin/grid.py commit <file> --session <iter> <agent>` | Snapshot a kid draft |
| `bin/grid.py checkout --all [--dir D]` | Materialize build-node payloads into `<project>/payloads/` for editing |
| `bin/grid.py payload <id> [--version N] [--out PATH]` | Read one payload back out of its ref |
| `bin/grid.py log <id>` / `diff <id> [--back N]` / `versions <id>` / `status` | Inspect |
| `bin/grid.py cron install` / `show` / `remove` | Install automated sync (both cadences) |
| `bin/dispatch.py <project> <iter>` | Spawn pi kids (pi runtime) |
| `bin/heal.py <project> <iter>` | Timeout/restart watchdog (pi runtime) |

## Choosing a runtime

| | pi harness (`driver.sh --max-iters N`) | CC-native dispatch |
|---|---|---|
| Billing | pi's own auth | Claude Code subscription |
| Models | whatever pi is keyed for | any Claude model per kid |
| Supervision | `heal.py` timeouts, unattended | parent reviews every node before commit |
| Best for | long unattended runs, cheap/OS models | supervised runs, model tiering |

`dispatch.py` scrubs `ANTHROPIC_*`/`CLAUDE_CODE_*` from pi child environments on purpose — a subscription quota-leak fix. **CC-native dispatch is the sanctioned way to spend Claude subscription tokens on the loop. Never bypass the scrub instead.**

## The three tiers

| Tier | Role | Runs as |
|---|---|---|
| **Delegator** | The chat the user sees. Holds user intent, coordinates several parent/kid groups, reports progress. | The user's session |
| **Parent** | Owns one loop: picks targets, spawns kids, reviews nodes, enforces the evidence gate, commits. | **A subagent** by default |
| **Kid** | One node, bounded scope. | Subagent spawned by a parent |

**The parent is a subagent by default** so review motion — reading every node, running the gate — never accumulates in the user's own context. The deliberate exception: when the user wants progress reported directly, or is feeding instructions in mid-run, the main flow acts as parent itself.

Models are **fully configurable per tier** (`cc_dispatch.kid_model` and friends). Nothing is hardcoded; run combinations and keep what works. As zoom levels generalize beyond big/small, assign one tier per level, each reviewed at the level above.

## Iteration protocol (parent)

One iteration = one node per kid, reviewed and committed by the parent.

1. **Snapshot + render.** `driver.sh --smoke --max-iters 1`. Records the metric baseline, refreshes `context/INJECTION.md`. **Verify the node count did not drop.**
2. **Pick targets** from `INJECTION.md`. Slot 0 → big zoom (fresh idea or top-level fork). Slots 1..N → small zoom on the top attractor, 2-hop subtree. N = `cc_dispatch.kids_per_iter`.
3. **Spawn kids.** Generate each kid's context with `bin/zoom.py`, then **embed the rendered map in the spawn prompt** — don't merely reference it. Each prompt must be self-contained: zoom scope, target parent node id, chain step, node file format, verdict taxonomy, project paths (`INJECTION.md`, `GOALS.md`, spec).
   Kid deltas from the normal rules: **do not commit**, and do not call `cli.py done` — write the node file, report, stop. The parent owns commits and record-keeping. When the job is a fix or update to an existing node rather than a new chain step, **edit that node's file in place** — never mint a second file for the new version (no `@v2` node, no `supersedes:` pair). The grid, not the filesystem, carries version history; it records the change at the parent's next `grid.py commit --all`.
4. **Review — this is the gate.** For each node: parent link resolves, taxonomy valid, and **`proved`/`disproved` REQUIRE experiment evidence (`evidence_runs >= 1`)**. Demote unevidenced verdicts to `pending` or `inconclusive_lean_*`. Reject orphans.
   The evidence half is now enforced in code — `bin/evidence_gate.py`, applied by both writer paths (`bin/cli.py done` and `bin/post_wire.py`). An unevidenced `proved`/`disproved` is auto-demoted to `inconclusive_lean_*:50` and stamped `demoted_from` / `demote_reason`; the node is kept, only the overclaim is dropped. `--no-evidence-gate` bypasses it loudly and stamps `evidence_gate: bypassed` — treat any such node as unreviewed. Still yours by hand: parent-link resolution and orphan rejection.
5. **Commit** accepted nodes in one commit: `iter-N: <kid-a summary>; <kid-b summary>`. Then `bin/grid.py commit --all`.
6. **Re-render** and report metric deltas.

### Kid end-of-job contract

The kid's final message is:

```
DONE <node-id>
caveats: <optional, one line>
struggles: <optional, one line>
question: <optional — ONLY under the four escalation triggers>
```

plus whatever numbers the brief asked for. Nothing else. **No git, no push, no sync, no cli.py** — spending tokens on those is waste; automation owns all remote traffic.

### Escalation — kid → parent

Default is **decide and document**: make the call, record it honestly in the node body as a deviation, and let verdict writers weigh it later. Every question is a full stop plus a round trip, so escalation is reserved for four triggers:

1. The task genuinely requires touching a file the hard rules forbid.
2. Embedded instructions contradict repo reality **and** the resolution would bind future chain nodes.
3. An irreversible or destructive operation.
4. Cost blowup — honest execution needs far more trials/tokens/time than the brief implied.

Budget: one question per kid per iteration. Mechanism: `SendMessage` to the parent; the kid's turn ends, the parent answers, and the kid resumes with context intact.

## Metrics — score goal fulfillment, not chain length

**Never optimize raw chain length.** Agents proved it gameable: 9 chains × 2000 hops via shortcut cycles, carrying no signal — and the resulting pathological structure then broke the render path outright. Set `metric_primary` to something goal-attributable (e.g. `outcome_coverage`) and leave `longest_chain_length` in `secondary_metrics` as a descriptive statistic only.

Pair that with the evidence gate. A gameable metric plus unevidenced verdicts produces impressive numbers that mean nothing.

Metrics are computed by `bin/metrics.py` (called from `driver.sh`). It reads `metric_primary` from the config and falls back to `outcome_coverage` — never chain length — when the config omits it, and prints a `METRIC_WARNING gameable_primary=…` line if a project still names a gameable metric as primary. Alongside the structural statistics it emits:

- `evidence_fraction` — asserting verdicts (everything but `pending`) that carry `evidence_runs >= 1`. This is the metric counterpart of the H4 gate: it moves only when experiments are actually run, and adding hops cannot shift it.
- `unevidenced_decisive_verdicts` — should be `0`. Nonzero means a gate bypass or a hand-edited node.
- `evidence_weighted_depth` — `avg_chain_depth × evidence_fraction`, depth discounted by what backs it.

## Project layout

A project holds **data and configuration; never engine code.** The graph is a
*separate repo one level inside the project*, `<project>/<project>-tree/`, and
the engine clones in **underneath it** at `<project>/<project>-tree/agi/`. The
tree is outside the engine, not inside it — so an engine checkout never
contains a graph, and the two histories cannot mix in either direction. This
is a refinement of shape 1 (drop-in clone) in **G8.1**, not a closed decision
— no experiment has run against it yet. Worked example, `fantasia`:

```
fantasia/
  <game source>
  fantasia-tree/                   the graph, its OWN git repo
    GOALS.md                       long-term goals: active | horizon | phasing-out | complete
    agi-tree.config.json           metrics, dispatch, timeouts
    nodes/<type>/*.md              the graph — frontmatter + body
    context/INJECTION.md           generated map
    sessions/                      per-iteration scratch (gitignore this)
    agi/                           gitignored clone of the engine
```

**Goals are the baseline.** `GOALS.md` defines what chains are for; seed nodes reference goals by id. Retire a goal by marking it `phasing-out` and **deprecating — never deleting** its seed node; retired chains remain prior art.

**Status is a four-state lifecycle:** `active` (being worked), `horizon` (declared and committed to, not yet being worked), `phasing-out` (retiring), `complete`. `horizon` is what makes goal rotation expressible — you can declare more goals than `cc_dispatch.max_goals_active` without lying about which are in flight. Unknown values are **preserved verbatim** with a stderr warning, never rejected: a typo must not be able to drop a goal from the graph.

The engine is never committed into a project. **One** gitignore entry, in the tree repo, does it — because the engine now lives inside the tree rather than the other way round:

```
# agi engine (drop-in clone — never commit here)
agi/
```

That is the whole story for a normal project. The engine repo needs **no** tree-related pattern at all, which is the point of putting the tree outside it: there is nothing to ignore, so there is nothing to get wrong.

`find-root.sh` locates the tree by walking up from cwd for `agi-tree.config.json` first (classic layout, tree == project root); failing that it descends into `<start>/<basename>-tree/`, or a lone match under `<start>/*-tree/`. A `*-tree` directory with no config file is skipped rather than treated as a candidate, which is what keeps the glob from picking up unrelated directories. More than one real candidate is a hard error listing all of them, never a guess.

**Open, deliberately not built yet:** nothing creates `<project>/<project>-tree/` for you — set it up by hand (`git init` the tree, clone the engine inside it). Engine-commit pinning in `agi-tree.config.json` (G8.1's other ask) is also not implemented.

### The self-referential exception: agi ↔ agi-tree

One pair breaks the sketch above, on purpose: the engine's own graph. The
shape is the same — `agi/agi-tree/agi`, tree outside, engine inside — but both
hops are **symlinks** rather than a clone, because here the graph literally
builds the engine, so an engine edit made from inside the tree must land in
the real checkout and not in a copy nobody ships:

```
agi/                        the engine repo, outermost
  agi-tree -> <graph repo>  symlink  (the one line in the engine's .gitignore)
    agi -> <engine repo>    symlink  (already covered by the tree's `agi/`)
```

So `agi/agi-tree/agi` resolves back to the engine itself. The engine's
`.gitignore` carries exactly one literal `agi-tree` line for the outer
symlink — deliberately not a `*-tree` glob, since nothing else should be
ignorable there and a generic pattern would hide a real mistake. No trailing
slash, because that would not match a symlink.

This is an organizational convenience for **one local pair**, not a mode the
engine knows about — **G8.2**'s invariant holds: there is no
`if project == "agi-tree"` branch anywhere, and nothing here adds one. Every
other project — fantasia included — gets a plain clone inside an
independently-git-initialized tree, per the layout above.

New node types are **schema**, i.e. configuration — which is all the flexibility a project needs without forking the engine.

## Verdict taxonomy (finite-state)

```
proved | disproved | inconclusive_lean_proved:N | inconclusive_lean_disproved:N | pending
```

Fields: `confidence` (0..1), `evidence_runs`, `supports`, `contradicts`.

**Judge the chain's core claim.** When a mechanism prescribed inside a hypothesis fails but the core claim survives, return the verdict on the core claim and name the failed prescription as explicitly unendorsed. State the proved invariant at the level it actually holds — overclaiming poisons every downstream reader.

## Zoom

Zoom is a **view into the graph, not a node's type** — `--level big`/`--level small` above are context-injection scope, unrelated to any node's `type` field. Coarse grains are meant to come from **tags and addresses** (a tag names a supernode; an address is that supernode's short id prefix) — **designed, not yet built.** Fine grains come from a node's **mint id and its grid version history**, below. The finest zoom — the chat that produced a version — is also unbuilt: grid commits and the sessions that made them are not yet cross-linked.

## The git grid

`bin/grid.py` adds two version dimensions beside the project's own history, baked into the repo as `refs/grid/node/*` and `refs/grid/session/*` — never checked out, invisible to `git branch`, blobs deduped, one remote syncs everything. **A version is a grid commit, not a second node file** — a fix edits the target node in place, and the grid is what accumulates the history. Version history is depth to zoom into, never flat structure on disk.

### `body` is state; `thought` is delta

A node body carries two regions with different owners, and conflating them is
what made 8,034 authored contract fields read `TODO(model)` with zero ever
filled — a generator rewrote the whole body each run, so filling one lasted
until the next scan (**G2.10**, fixed 2026-08-27).

```
<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
why this version differs from the last one
<!-- THOUGHT:END -->
```

The **body** says what the node asserts now. The **thought** says why *this
version* differs from the previous one — written from scratch per change, not
accumulated. The grid already snapshots `node.md` per version, so the thought
is versioned for free and `grid.py diff` becomes a changelog of reasoning
rather than of prose (**G2.11**).

Three rules, each with a reason that was paid for:

- **Absent means empty.** Introducing the block churned 0 of 786 nodes. Never
  invent one after the fact — a fabricated thought reads as evidence.
- **Readers strip it.** It must not ride in `GOALS.md` or injected context.
  Thought is provenance you zoom into, not weight every agent carries for the
  rest of the project's life — the design ethic at the top of this file,
  applied.
- **Not a frontmatter field.** `write_frontmatter` flattens newlines, so prose
  there is silently destroyed by the one function that writes every node on
  every run.

The finer grain — the *chat* that produced the version, rather than a note
about it — is **G2.7** and **G10.1**, and is still unbuilt. `thought_session:`
is reserved in frontmatter for it.

**A build node's ref holds its payload, not just its prose.** As of 2026-08-25 (G6.3) `refs/grid/node/<mint-id>` is a two-entry tree — `node.md` plus `payload` — and the payload carries its **real** mode, read from `os.lstat()`: `100644`, `100755`, or `120000` with the link text as its content. So `payload_ref` still names where the file belongs in the engine tree, but the bytes come from the ref. A payload-only edit is a real version, because the unchanged-check compares the whole tree.

That is what reverses G6.1's arrow, and it is the workflow for engine work:

```
grid.py checkout --all                  # payloads/<payload_ref>, editable
<edit, and run the tests against that copy>
grid.py commit --all                    # the graph records your edit as vN+1
stitch.py --out <engine> --from-grid --publish
```

`--publish` refuses unless `--from-grid` is set **and** the target's working tree is clean, so every overwritten byte is already in the target's own git history and `git checkout .` undoes the publish whole. `--grid-version N` materializes a chosen version of the whole tree instead of each node's tip.

**Do not hand-edit the engine.** A change made there has no node behind it, which is the open loop G6 exists to close — and the graph will overwrite it on the next publish.

- **After every iteration commit:** `grid.py commit --all`. Changed nodes gain a version; unchanged nodes get nothing. **Versions record change, not time.**
- **Kid drafts:** `grid.py commit <file> --session <iter> <agent>` before review. Rejected drafts survive there; accepted content lands on the node branch at the next `commit --all`. Nothing is lost either way.
- **Sync is automated.** `grid.py cron install` sets both cadences: every 5 min, snapshot + push `refs/grid/*` (crash window ≤ 5 min); hourly, push the main branch. **Nobody syncs by hand.** A parent's only git surface is the local iteration commit; a kid's is nothing at all.

### Identifiers: mint id vs address

Decided 2026-08-25: a node carries **two** identifiers, and they are never the same field.

| | mint id | address |
|---|---|---|
| assigned | once, at creation | derived; re-derived freely |
| changes | never | on every retag/regroup |
| shape | opaque, uuid-like | short, hierarchical, alphanumeric |
| keys | grid refs, provenance | zoom, lookup, prefixes |

Grid refs are **designed** to key on the mint id rather than the address, so retagging or re-addressing a node never renames a ref — an address is cheap to change precisely because nothing durable hangs off it. **Not yet deployed:** today's refs still key on the node's current id; the mint-id migration is landing now, in parallel.

## Configuration

`<project>/agi-tree.config.json`:

```jsonc
{
  "metric_primary": "outcome_coverage",   // goal-attributable, not chain length
  "best_direction": "higher",
  "secondary_metrics": ["longest_chain_length", "avg_chain_depth", "mvp_count"],
  "mid_chain_join_prob": 0.3,
  "fresh_start_prob": 0.15,
  "big_idea_vs_small_idea_split": 0.3,
  "attractiveness_weights": { "length": 0.3, "depth": 0.2, "recency": 0.2, "mvp_count": 0.3 },
  "agent_dispatch": { "provider": "...", "model": "...", "max_turns": 30 },
  "cc_dispatch": {
    "iterations_per_run": 5,
    "max_goals_active": 3,
    "kids_per_iter": 2,
    "kid_model": "claude-opus-5"
  },
  "agent_timeout_mins": 10
}
```

One namespace per runtime — `agent_dispatch.*` for pi, `cc_dispatch.*` for Claude Code. Keep them separate.

**The config file is the project's whole customization surface.** It is per-project, owned by the project repo, and meant to be edited programmatically — the engine reads it, never writes engine behavior back into it. A project changes metrics, dispatch, and schema here; it never forks engine code to change behavior.

**Legacy name.** Projects created before the rename carry `autoresearch-tree.config.json`. Every engine entry point still resolves it, canonical name first, so old projects keep running unchanged. New projects use `agi-tree.config.json`. Same for `$AGI_TREE_PROJECT_ROOT`, whose legacy spelling `$AUTORESEARCH_TREE_PROJECT_ROOT` is still read and still set.

## Install

One-time, global, not per-project:

| What | Where | Points at |
|---|---|---|
| Skill | `~/.claude/skills/agi` (symlink) | `<engine>/skills/agi` |
| CLI | `~/.local/bin/agi` (symlink) | `<engine>/extensions/agi/driver.sh` |
| Hook | `SessionStart` entry in `~/.claude/settings.json` | `<engine>/extensions/agi/hooks/cc-session-start.sh` |

One skill, one source — no project ever carries its own copy of either symlink target. Register the hook once; it's a no-op outside a project (below), so it's safe for every session.

## Auto-injection

`hooks/cc-session-start.sh`, registered as a Claude Code `SessionStart` hook, injects the project's map into every new session. It walks up from cwd for `agi-tree.config.json`, re-renders if stale, and emits the head of `INJECTION.md`. **Silent no-op outside projects**, so it's safe to register globally.

## Long runs

```bash
cd <project>
tmux new-session -d -s agi "agi --max-iters N --delay-mins M |& tee /tmp/agi.log"
tmux attach -t agi          # Ctrl-B D to detach
```

**Iter numbering caveat:** the driver starts at `iter-001` and will clobber prior session manifests. Back up `sessions/` before a fresh run.

## Field notes (validated on live runs)

- **Embed the map, don't reference it.** Kids dropped from 11–13 tool calls to 5–7 when the rendered map was pasted into the spawn prompt.
- **Healing.** On an API-error death, check the filesystem **before** resuming — kids often die after the node file landed, losing only their report, in which case the artifact is reviewable and no resume is needed. Otherwise resume the same agent (context intact) rather than respawning cold. On overload waves, back off 60s+, and give resumed kids a degraded-mode fallback (fewer trials, reduced n recorded honestly) so a wave can't stall the run.
- **Parallel-kid hygiene.** Kids see each other's untracked files in `git status`. Instruct: report unexpected files, never touch or clean them. Kids reliably flag them unprompted — that's the expected behavior.
- **Cheap-agent experiments stay cheap.** When a hypothesis is about what weak models do, dispatch genuinely weak subagents for those roles and keep ground truth + scoring to the orchestrator, with scratch under gitignored `sessions/`, never `nodes/`.

## Safety rails (non-negotiable)

- **Never create a project-local `bin/snapshot-build-site.py` or `bin/render-context.py`.** Stale copies have silently wiped an entire node corpus (29,264 files) and separately broken the render path. The driver prefers project-local scripts, so a stale copy shadows the safe engine version. Treat any project-local `bin/*.py` as stale until proven otherwise.
- **Engine improvements → engine repo. Graph and domain output → project repo.**
- **Kids that stall or wander out of zoom scope:** kill, log, respawn narrower.
- **Verify the node count never drops** after a snapshot.
