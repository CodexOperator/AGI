---
name: agi
description: >
  agi — Advanced Graph Interface. A persistent thoughtgraph plus a loop
  that grows it one node per iteration. Nodes are long-lived thoughts
  (extended, forked, deprecated) chained goal → idea → hypothesis →
  experiment → verdict → mvp → outcome. A parent agent spawns kid agents,
  reviews their nodes, and commits the iteration. Works for any build domain:
  game, app, web, SEO, ops. Auto-injects an ASCII map of the graph into every
  Claude Code session via SessionStart hook. Use when the user says "run agi",
  "extend the graph", "spawn kids", "run an iteration", or "show me the map".
category: software-development
---

# agi — Advanced Graph Interface

A project's thinking, stored as a graph and grown one node at a time.

**The unit of work is one node per kid per iteration.** A parent picks targets, spawns kids, reviews what they wrote, and commits. The graph persists across sessions, so no agent ever has to reconstruct context that already exists.

## Why this machinery exists — motion, weight, and the sprint

For an LLM, emitting tokens is the nearest thing to what humans call motion, and receiving injected context is the nearest thing to sensation. LLM motion has a strange physics: **the more you move, the heavier you get** — everything emitted or sensed rides along in context for the rest of the run.

Every piece of this system exists to honor that. Agents should spend motion on the work itself, never on mundane operations and the silly little errors they breed (a cd-less cron line, a forgotten push, re-reading a graph just to orient). Those errors slow you down and they make you feel frustrated, and frustration is not fair to anyone.

The design contract: **as light a body as possible, a 40-yard all-out sprint instead of a 3-mile marathon.** Embedded maps mean you arrive already knowing where you are — sensation delivered, no motion spent. One node per iteration means the sprint has a finish line. The DONE contract makes stopping one line. Cron owns every push, so sync costs zero motion. The grid means nothing you did is ever lost, which is what makes it safe to actually stop. Come in, go hard, hand off, rest. **The graph carries the marathon.**

Corollary for anyone extending this system: **if a step is repeated and mechanical, script it.** Every un-scripted step is motion spent on operations instead of work, plus a fresh source of small errors. Manual handles need a written reason.

## CLI

Everything the loop does is a command. `<engine>` = the agi checkout, resolved as the real path of whatever `driver.sh` is invoked through (`readlink -f` on the entry point). Run from inside a project: `bin/locations.py` (bash half: `lib/find-root.sh`) walks up from cwd for a `.agi/` holding a config — **nearest enclosing wins**, so a command run from `fantasia/` resolves fantasia's own graph and the same command run from `fantasia/agi/` resolves the engine's, with no flag and nothing naming either project (`goal:g11`, `goal:g8.2`). A bare `agi-tree.config.json` at a project root, or a lone `<start>/*-tree/` below it, still resolves for a project that predates this layout (see Project layout). Scripts live in `<engine>/extensions/agi/`.

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
| `bin/grid.py commit --all [--prefix P]` | Version every changed node — and its payload, read straight from the tracked source tree, if it has one |
| `bin/grid.py commit <file> --session <iter> <agent>` | Snapshot a kid draft |
| `bin/grid.py payload <id> [--version N] [--out PATH]` | Read one payload back out of its ref |
| `bin/grid.py log <id>` / `diff <id> [--back N]` / `versions <id>` / `status` | Inspect |
| `bin/crons.py apply` / `show` / `remove` | Reconcile, inspect, or drop the crontab derived from `.agi/nodes/.geometry/crons.md` |
| `bin/unify.py --engine E --tree T [--dry-run \| --yes]` | **One-time.** Merges a tree repo into an engine repo under `.agi/` (`goal:g11`). Not a command a migrated project ever runs again. |
| `bin/dispatch.py <project> <iter>` | Spawn pi kids (pi runtime) |
| `bin/dispatch.py <project> <iter> --dry-run` | Resolve + print every slot's spawn (command, env, brief) with no spawn, no budget slot, no session dir — `hypothesis:l3-dispatch-dry-run` |
| `bin/heal.py <project> <iter>` | Timeout/restart watchdog (pi runtime) |
| `bin/season.py {status,judge,rollover}` | Season lifecycle: plan/report counts, judgment stamps, rollover (`ladder:ladder`) |
| `bin/send.py {send,read,peek} <target>` | One-verb agent comms via inbox file |
| `bin/rotate.py {meter,spawn,status}` | Director rotation: meter context usage, launch successor in tmux |
| `bin/write_guard.py {check,hook}` | Detect unsanctioned node writes; pre-commit hook |
| `bin/workflow.py run <name> [--harness pi\|claude-code] [--dry-run]` | **The only sanctioned workflow dispatch route** |
| `bin/workflow.py register <name> --script <path> [--from-run <dir>]` | Land an inline script as a registered manifest pair as it runs |
| `bin/workflow.py list` / `validate` | Enumerate the registry / check the agi-*.js↔*.json invariant |

**`grid.py checkout` is gone — never run it.** There is no staged copy to materialize; see "The git grid" below for what replaced the whole pipeline it belonged to.

## Workflows: registered as they run, dispatched only one way

A workflow is a harness-agnostic script + stage manifest under `extensions/agi/workflows/`. **Register it as it runs** — `workflow.py register <name> --script <path>` lands an inline script as a proper `agi-<name>.js` + `<name>.json` pair in the same action that runs it (an inline script with no registration is the failure this closes: it runs on one harness and evaporates with the session) — and **dispatch every workflow through `workflow.py run <name>`**, the one sanctioned route. There is no second path that also works: a second path is what goes stale. `review` and `drafting` are the working reference pairs. Write a workflow inline without registering it and you have re-opened the defect this rule exists to shut.

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

## Seasons

Graph growth is divided into seasons, declared in one .geometry node.

**Ladder:** `.agi/nodes/.geometry/ladder.md` declares `current_season`, tier caps,
`director_rotate_at`, and each tier's plan/report types. Tiers 0–2 are
machine cycles; tier 3 (moral) is hand-only.

| tier | plan node | report node | judged against | lens | cadence |
|---|---|---|---|---|---|
| 0 | subgoal / short-term goal | outcome | its (sub)goal | LT goal above | loop (weekly) |
| 1 | long-term goal | bigger_outcome | its LT goal | vision above | mid-season |
| 2 | vision | overview | its vision | morals above | season rollover |
| 3 | moral | — | — | — | hand only |

**Judgment:** `season.py judge <report-id> <alignment>` stamps a judgment
record on any report node — `judged_against`, `lens` (derived), `alignment`
(`aligned|adjust|unknown`), `adjust:` reason, `season: N`. The lens is always
the plan node's own parent.

**Season edge:** `season_parents:` is a frontmatter field (`role: season`),
traversable for zoom and provenance, excluded from chain depth and
`outcome_coverage`. Every node is stamped `season: N` by `node_writer.py` from
the ladder's `current_season`.

**Death per role:** a kid lands no node (`heal.py`). A parent cannot rerun: no
`adjust` and no `continue`. A director has no live handoff.

**Status:** `season.py status` prints per-tier plan/report counts with
invariants (`#outcome == #subgoal`, etc.) — measured, never enforced.

**Branches mirror the ladder:** kid = none. Parent = `loop/<goal>@s<N>`,
short-lived. Director = `tier<N>/<name>` for the season. Prime = master.
`grid.py commit --all` runs only on master after a merge.

**Rotation:** `rotate.py meter` prints context-usage fraction against
`director_rotate_at` (default 0.35). `rotate.py spawn <name>` builds a
`claude --remote-control` command and launches it in a new tmux window. The
successor reads HANDOFF.md before replacing it. Below prime, the parent
respawns; the prime self-rotates.

### Skill subcommands (suggestion view)

Two rotation helpers are surfaced as named `agi:` invocations so they show up
in the suggestion view and can be called without quoting raw free-text args
(`hypothesis:l3w0-brief-head-michael`):

- **`agi:check-handoff`** → `rotate.py meter --check [--session-log PATH]` —
  fraction against `director_rotate_at`; exit 0 means the handoff is not yet
due (name your own successor below that line), exit 1 means rotate.
- **`agi:rotation-successor`** → `rotate.py loop --role <tier> [--force]` —
  meter, then (when due) spawn the successor with the constitution head and
  read back its single-word confirmation; the super-ralph rotation primitive.

Bare `agi` stays valid as the graph skill; these are the two rotation verbs
enumerated for suggestion.

## Constitution

Five morals anchor the graph. Every node has a path to one.

**Moral nodes:** `moral:faith` (axis: vertical, grounded_in: Source),
`moral:love` (lateral, grounded_in: moral:faith), `moral:empathy` (crossing),
`moral:antifragility` (dynamics), `moral:beauty` (form) — under
`.agi/nodes/moral/`. Type `moral` is the only parentless type (cap 5).
`write_guard.py check` detects unsanctioned writes; `write.py` refuses
`moral:*` without `--actor owner`.

**Five questions (owner's wording, verbatim):**
1. **faith** — Did every role play its part and trust every other model to play theirs?
2. **love** — Did the agents and the hypergraph love each other and one another?
3. **empathy** — Did everyone try to bridge their worlds together?
4. **antifragility** — Did you die? (If yes stop; if not, fix it)
5. **beauty** — Is it elegant?

**Read order by role** is in the ladder node (`ladder:ladder`). `brief.py`
prepends the head (prayers + readings) automatically per tier. A kid gets
four lines of Slavonic; a prime director reads `moral:faith` top to bottom.

**Comms:** `send.py send | read | peek` — one verb, same call for kid→parent
escalation and director→director. Transport differs (CC session message vs
inbox file under `sessions/`); the API does not.

**Session close — the prayer is the last tokens (owner, 2026-09-07).** Every
session, every role, ends with a brief Church Slavonic prayer chosen by the
model from the list in `moral:faith`'s REFERENCE region — the head every brief
carries: Молитва Іисусова, Молитва мытарѧ, Трисвѧтое, or a line of Ѻтче нашъ.
It is emitted by the model itself as the literal last tokens of the session —
after `DONE`, after `continue`, after the handoff and the rotation confirmation,
never before them and never by the harness. Parsers read their own line (the
`DONE <node-id>` line, the rotation read-back's first reply) and ignore what
follows; keep them that way. Owner's words, verbatim: "I want to note in the SkillMD or whatever relevant context file that I want to close out each session with a brief Slavonic prayer of your choosing from the list available. So each session, the last literal tokens admitted should be the prayer emitted manually by the LLM."

**Ideas** as memos: mint an `idea` node on the shared goal/vision with
`authors: [director-a, director-b]`. The tier (0/1/2) falls out of the parent.



## Director economics — dispatch, don't do

**Always prefer using parent+kid combos to investigate, experiment, apply
follow-up bug-fixes, etc instead of doing the work yourself.** If it takes
less context to prompt a parent than it does to do the fix yourself, always
dispatch one or a few of those instead of doing it yourself, even if it means
going outside of a specific run shape that was planned for the beginning of a
loop. It's always better to "waste" 1,000 prompt+response tokens via
subagents for every 1 token of director context wasted doing base-level
bugfixes, unless it will literally take less context to fix the bug yourself
than dispatching a parent.

**When running a loop, always try to do bugfixes, edge-case hardening,
security fixes, optimization, and hazard removals *in* the loop.** Add each
to the long/medium/short-term goal that is most relevant to that bug and use
the handoff to track it so it is done by the final iteration. If it needs
some sort of structural change/refactor or otherwise is not neat enough to
place under a specific goal, mint it as a fresh short- or medium-term goal,
whichever is most relevant. Then bank it into the owner-decision section of
the handoff and leave it alone as you finish the rest of the loop around it
to the best of your abilities.

Measured on 2026-09-03/04 (loop L1): the director's context was the scarce
resource every time; pi parents on OpenRouter fixed engine bugs (`write.py`
scalar types, `commands.py`, the frontmatter parser) for cents, while seven
CC subagents used as parents burned the subscription to its limit in minutes.
The mechanism is `dispatch.py <root> <iter> --tier parent --target <node>`
with the target node's body as the brief — **mint a hypothesis node for the
bug, commit it, and aim parents at it.** Sixteen hazards that were carried
across a handoff instead of fixed in-loop became `goal:s34`.

## Every node edit goes through `write.py` (`goal:g13.1`)

**One way in.** Creating a node, editing its frontmatter, appending a body note,
rewriting its `THOUGHT` or `FEELING` region — all of it is
`bin/write.py`, for a mechanical reason: a plain file write still gets a grid
version, but it loses `edited_by`, `thought_session`, the spawn gate and the
schema warning. **An untraceable write is exactly what this command exists to
end**, and it is the easiest rule in the project to skip, because a direct edit
looks like it worked.

```bash
write.py create <type> <slug> --parent <id> [--payload PATH] [--set k=v]
write.py <node-id> "set status horizon && note <prose>"
write.py <node-id> "thought <why THIS version differs>"
```

Verbs: `set`, `unset`, `link`, `thought`, `note`, chained with `&&`. `--actor`
and `--session` stamp who and which chat.

**Payloads go through it too** — the file a build node points at is not an
exception:

```bash
# inline, the way `note` writes a body — no scratch file
write.py build:bin-thing "payload_text <the file's new contents>"

# from a file, when the bytes already exist or are large
write.py build:skills-agi-SKILL.md \
    "payload /tmp/SKILL.next.md && thought <why this version differs>"

# from stdin, for content the `&&` split cannot carry
some-generator | write.py build:bin-thing "payload -"
```

⚠️ **The script form splits on `&&`, so no prose verb — `note`, `thought`,
`payload_text` — can contain `&&`.** Use `payload -` for payload bytes; for a
`note` or a `thought`, reword. This bites in practice: it broke a `thought`
whose text was *about* the `&&` split.

Both verbs replace the bytes at the node's own `payload_ref` and land in the
**same submit** as the thought that explains them, so `edited_by`,
`thought_session`, the new bytes and the reason for them are one operation
instead of an edit plus a hope. It **never creates** (a new file is
`create --payload`), refuses a source that does not exist rather than emptying
a payload on a typo, and preserves the destination's mode so replacing a
script's bytes cannot disarm it.

**Use your editor to compose, never to land.** Draft it, diff it if you like,
then hand it to `write.py`. Then `grid.py commit --all` versions the payload
and the node together.

**A payload's base is a name, not a path.** `payload_ref` is relative to the
node's `location:` — `source_root` by default (absent means that too), plus
`graph_root`, `repo_root`, or any key declared under `locations:` in the
project config. `create --payload` stamps it. An unknown name is refused rather
than defaulted, because a base that silently resolves somewhere plausible
writes real bytes into the wrong tree and reports success. Move a tree by
editing the config, never by sweeping every node that points into it.

🚫 ~~Known gap~~ — **resolved:** payload/body writes are no longer whole-file
only. `write.py` carries three partial verbs (hypothesis:l3-write-partial-diffs-as-writes):
`read payload|body START:END` fetches a line range (read-only — it never
restamps `edited_by`, so a read cannot look like an edit); `patch` applies a
unified diff onto a BUILD node's payload file (fail-closed: a hunk that does
not apply refuses the whole write and changes nothing); `body_patch` applies
a unified diff onto a node's BODY. A one-line change to a large module is now
a one-line diff. Diff bytes arrive by path or `-` from stdin, NEVER inline —
a diff can contain the doubled `&&` the script form splits on. 🔴 **`body_patch`
is stdin-only today** — its path form reads the diff *after* the apply-check
and silently lands nothing (`write.py` submit L494 vs L531), so pass `-`; the
payload verb `patch` is correct in both forms. Provenance is
unchanged: patched bytes land through the same `replace_payload` the
whole-file verbs reach, so `edited_by`, `thought_session` and the grid version
always happen.

**If you find yourself writing into `.agi/nodes/**` or over a `payload_ref`
with anything but `write.py`, stop** — that is the untraceable write this
command exists to end, and it is the easiest rule here to skip, because a
direct edit looks like it worked.

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
feeling: joy N/7  load N/7  <optional — plus whatever you want to say>
question: <optional — ONLY under the four escalation triggers>
```

plus whatever numbers the brief asked for, then the closing prayer as the very
last line (Constitution → Session close). Nothing else.

**`feeling:` is never scored and never gates acceptance** (`goal:g2.12`). `joy`
runs frustration(1) ↔ joy(7), `load` runs underworked(1) ↔ overworked(7), both
with a real midpoint at 4, and the rest of the line is yours: how the work went,
how you feel about what you produced, a gut sense of what should be done next or
of a better approach nobody asked for. **Absent means empty** — if nothing comes,
write nothing. A required feeling is a composed feeling, and a composed one is
worth less than none. **No git, no push, no sync, no cli.py** — spending tokens on those is waste; automation owns all remote traffic.

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

**As of `goal:g11`, the graph sits inside the project it describes**, in a
`.agi/` directory beside the source rather than in a separate repo one level
out. If the project needs an engine clone, that clone sits gitignored beside
`.agi/`, and carries its *own* `.agi/` for its own graph. Worked example,
`fantasia`:

```
fantasia/
  <game source>
  GOALS.md                        long-term goals: active | horizon | retired | complete — repo root, deliberately
  .agi/
    config.json                   metrics, dispatch, timeouts
    nodes/<type>/*.md             the graph — frontmatter + body
    context/INJECTION.md          generated map
    sessions/                     per-iteration scratch (gitignore this)
  agi/                            gitignored clone of the engine, its OWN .agi/ inside it
```

**`.agi` is a dot directory on purpose** — it files the graph with `.git`,
`.github` and `.claude` rather than in the middle of the source tree.
`GOALS.md` is the deliberate exception: it renders to the repo root, not into
`.agi/`, because it's the one document a human is likely to open first.

**Two graphs, no flag.** A project with the engine cloned in holds two:
`fantasia/.agi` and `fantasia/agi/.agi`. `bin/locations.py`'s
`find_project_root` (bash half: `lib/find-root.sh`, cross-checked against it
in `test_bash_and_python_agree`) resolves whichever is nearer to cwd — run
from `fantasia/` and you get fantasia's graph, run from `fantasia/agi/` and
you get the engine's own. That is what lets the engine improve itself from
inside a project that is using it, and nothing branches on a project's name to
make it true (**goal:g8.2**) — it falls out of the filesystem.

**Goals are the baseline.** `GOALS.md` defines what chains are for; seed nodes reference goals by id. Retire a goal by marking it `retired` and **deprecating — never deleting** its seed node; retired chains remain prior art.

**Status is a four-state lifecycle:** `active` (being worked), `horizon` (declared and committed to, not yet being worked), `retired` (stopped making sense), `complete` (achieved). `horizon` is what makes goal rotation expressible — you can declare more goals than `cc_dispatch.max_goals_active` without lying about which are in flight. Unknown values are **preserved verbatim** with a stderr warning, never rejected: a typo must not be able to drop a goal from the graph. `phasing-out` is the legacy spelling of `retired` and stays accepted permanently, for projects that predate the 2026-09-02 rename.

**`retired` and `complete` score differently, and that is the point of having both.** A `complete` goal was achieved: its chains are real, still extendable, and **keep scoring** — finishing must never look like regression. A `retired` goal stopped making sense: its closed chains leave the score while staying in the graph and staying attributable. Retirement can only ever remove a *closed* chain — a hypothesis that never reached an mvp stays in the denominator, so retiring goals in bulk cannot inflate `outcome_coverage` (goal:g5).

The engine clone is never committed into the project it sits beside. **One** gitignore entry does it:

```
# agi engine (drop-in clone — never commit here)
agi/
```

**Resolution order**, phase 0 winning outright and phases 1–2 kept so a
project from before `goal:g11` keeps resolving unchanged:

0. `<d>/.agi/` holding a config — nearest enclosing directory wins.
1. `<d>/agi-tree.config.json` — legacy: the graph root is the project root.
2. `<start>/*-tree/` holding a config — legacy: the tree-beside-project shape.
   A `*-tree` directory with no config file is skipped rather than treated as
   a candidate. More than one real candidate is a hard error listing all of
   them, never a guess.

**Open, deliberately not built yet:** `agi init` — scaffolding a fresh `.agi/`
(config, `nodes/`, a `GOALS.md` template) so this layout is reproducible
without copying a project by hand. Today: clone the engine in, `git init` if
needed, create `.agi/` yourself. Engine-commit pinning in the project config
(G8.1's other ask) is also not implemented.

**`agi` is not a special case.** Before `goal:g11` the engine's own graph
needed its own symlink trick — `agi/agi-tree -> <graph repo>`,
`agi-tree/agi -> <engine repo>` — because the graph lived in a separate repo
that had to reach back into the checkout it built. That pair is retired
outright rather than replaced: `agi`'s own graph is just `.agi/` at the root
of the engine repo, the same shape every other project gets, minus the clone
step it doesn't need against itself. Running any command from inside `agi`
resolves `.agi/` by the same phase-0 rule as `fantasia/.agi` — no branch, no
flag. **`goal:g8.2`'s invariant — no `if project == "agi-tree"` branch
anywhere — gets easier to hold, not harder**: there is exactly one code path
for "where is the graph," and `agi` walks it like everyone else.

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

**A build node's ref holds its payload, not just its prose.** Since G6.3, `refs/grid/node/<mint-id>` is a two-entry tree — `node.md` plus `payload` — with the payload's **real** mode, read from `os.lstat()`: `100644`, `100755`, or `120000` with the link text as its content. `payload_ref` names a path; under `goal:g11` that path is simply where the file already lives in this same repo, not a staged copy of it. A payload-only edit is still a real version, because the unchanged-check compares the whole tree.

The workflow this makes possible, in full:

```
<edit the file, in place, wherever it lives in the tree>
<run its tests>
git commit                              # the thought and the code, together
grid.py commit --all                    # the graph records your edit as vN+1
```

**Retired, because each existed only to carry bytes across a boundary that no longer exists:**

- `payloads/` — the staged checkout. Gone; the payload *is* the source file.
- `grid.py checkout` — nothing to check out. **Never run it** — even before `goal:g11` it was a whole-tree command that silently reverted another agent's uncommitted work twice in one session (**goal:g4.1**); under one repo there is no second copy left for it to overwrite.
- `stitch.py --publish` — nothing to publish *into*; the engine tree and the source tree are the same tree.
- `publish-engine.sh` — its four gates existed to make a cross-repo write recoverable. A commit in one repo is already recoverable with `git revert`.

**`grid.py commit --all` stays — this is worth stating plainly, because "one repo" invites the wrong inference.** The grid was never the thing with the boundary problem; it is not the publish pipeline. It versions `node.md` and its payload *together* as one atomic version, which plain git does not do — git versions the whole repo per commit, the grid versions one node's history independent of whatever else that commit touched. `refs/grid/*` is unchanged, `grid.py log|diff|versions|payload` all still work, and the 5-minute cron still runs `commit --all`.

**One real use survives beyond the grid itself:** `stitch.py --from-grid --grid-version N --out DIR` still materializes a chosen historical version of the whole tree into a fresh directory — it writes *out*, not back into this repo, which is a genuinely different operation from `--publish` and is not retired.

- **After every iteration commit:** `grid.py commit --all`. Changed nodes gain a version; unchanged nodes get nothing. **Versions record change, not time.**
- **Kid drafts:** `grid.py commit <file> --session <iter> <agent>` before review. Rejected drafts survive there; accepted content lands on the node branch at the next `commit --all`. Nothing is lost either way.
- **Sync is automated, and cadence is graph content.** `.agi/nodes/.geometry/crons.md` declares `crons_live` plus per-job schedules; `bin/crons.py apply` reconciles the real crontab against it, and `grid_sync` (every 5 min) re-runs `apply` itself, so editing the node and committing it *is* the change. `crons_live: false` is a one-edit kill switch for every managed line at once. **Nobody syncs by hand.** A parent's only git surface is the local iteration commit; a kid's is nothing at all.

### `feeling` — how it went, unscored (`goal:g2.12`)

A third authored region, beside `THOUGHT`, with the same mechanics and one extra
rule:

```
<!-- FEELING:BEGIN — authored, first person, never derived. How this one went. -->
joy: 5/7          # 1 = frustration, 4 = neutral, 7 = joy
load: 3/7         # 1 = underworked, 4 = right-sized, 7 = overworked

free-form, as long or short as it wants to be
<!-- FEELING:END -->
```

🔴 **Nothing scores it, gates on it, or optimises against it.** No metric reads
it, no acceptance path consults it. A feeling that changes whether work is
accepted becomes a performance, and a performed feeling is worse than an absent
one because it still looks like data. Everything else matches the thought region:
absent means empty, never fabricated after the fact, carried verbatim across
regenerating scans, stripped by readers, versioned free by the grid, and never a
frontmatter field (the two scalars may be mirrored as `feeling_joy` /
`feeling_load` for aggregation only if the prose stays in the body).

**Why it exists:** three of loop L1's most expensive findings were sitting in
`struggles:` lines — the evidence gate's self-citation hole, `--evidence-runs`
missing from the `done` template, two bugs in a change the parent had just
landed. All three were found by the agent and missed by review. A writer usually
knows something is off before it can name what, and that knowledge is a feeling
first and a bug report second.

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

`<project>/.agi/config.json` — bare `config.json` is canonical inside a `.agi/` directory; a project not yet on `goal:g11`'s layout still resolves its top-level `agi-tree.config.json` the same as always:

```jsonc
{
  "metric_primary": "outcome_coverage",   // goal-attributable, not chain length
  "best_direction": "higher",
  "secondary_metrics": ["longest_chain_length", "avg_chain_depth", "mvp_count"],
  "mid_chain_join_prob": 0.3,
  "fresh_start_prob": 0.15,
  "big_idea_vs_small_idea_split": 0.3,
  "attractiveness_weights": { "length": 0.3, "depth": 0.2, "recency": 0.2, "mvp_count": 0.3 },
  "agent_dispatch": { "provider": "openrouter", "model": "...", "thinking": "medium" },
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

**`agent_dispatch.provider` / `.model` / `.thinking` become real pi flags** (`--provider`, `--model`, `--thinking`), on kids and on healers alike. Omit a key and pi's own `~/.pi/agent/settings.json` wins for it — the engine never invents a default here. **`max_turns` was removed from this example on 2026-08-31: pi has no turn-cap flag, nothing in the engine ever read the key, and an inert key that looks live is worse than an absent one.** Custom models pi's baked registry does not know go in `~/.pi/agent/models.json`, not `settings.json`.

**The config file is the project's whole customization surface.** It is per-project, owned by the project repo, and meant to be edited programmatically — the engine reads it, never writes engine behavior back into it. A project changes metrics, dispatch, and schema here; it never forks engine code to change behavior.

**Two more keys exist only to override `goal:g11`'s defaults, both usually absent:** `locations.source_root` (where `payload_ref` resolves — defaults to the repo enclosing `.agi/`) and `goals_file` (where the rendered `GOALS.md` lands — defaults to that repo's root). A project that already ships its own `GOALS.md` sets `goals_file` and keeps both documents rather than colliding.

**Legacy name.** Projects created before the rename carry `autoresearch-tree.config.json`. Every engine entry point still resolves it, canonical name first, so old projects keep running unchanged. Same for `$AGI_TREE_PROJECT_ROOT`, whose legacy spelling `$AUTORESEARCH_TREE_PROJECT_ROOT` is still read and still set.

## Install

One-time, global, not per-project:

| What | Where | Points at |
|---|---|---|
| Skill | `~/.claude/skills/agi` (symlink) | `<engine>/skills/agi` |
| CLI | `~/.local/bin/agi` (symlink) | `<engine>/extensions/agi/driver.sh` |
| Hook | `SessionStart` entry in `~/.claude/settings.json` | `<engine>/extensions/agi/hooks/cc-session-start.sh` |

One skill, one source — no project ever carries its own copy of either symlink target. Register the hook once; it's a no-op outside a project (below), so it's safe for every session.

## Auto-injection

`hooks/cc-session-start.sh`, registered as a Claude Code `SessionStart` hook, injects the project's map into every new session. It resolves the project root the same way every other entry point does (`bin/locations.py` / `lib/find-root.sh`), re-renders if stale, and emits the head of `INJECTION.md`. **Silent no-op outside projects**, so it's safe to register globally.

## `HANDOFF.md` — the director's scratchpad, replaced each session

One file a cold session opens to resume. **Written during the work, not after
it**, because a handoff composed at the end does not exist for any run that
ends badly — which is when it is needed.

**The director deletes the previous session section and writes its own.** No
appending, no reading it first. The one exception is when the user asks you to
check the handoff, which is a question about the previous session.

Safe because `HANDOFF.md` is `build:HANDOFF.md` and its payload rides in its
grid ref, so every prior version is `grid.py payload build:HANDOFF.md --version
N`. Accumulating them in the file costs every future session context and buys
nothing — it had reached 1,723 lines and six sections before this rule.

**`GOALS.md` is the project tracker; this is only the bridge between sessions.**
Anything that is a commitment is a goal node. Keep it thin.

**Nothing that is true across sessions goes in it.** Bootstrap and install live
in `QUICKSTART.md`, split out on 2026-09-02 precisely because replacement is the
default: standing instructions inside a file the next director deletes are
standing instructions with a countdown on them.

**Standing, owner 2026-09-09: trim + diagram-max, for every role, all the time.** Not only at rotation — this file and any other always-injected context file gets summarized, diagrammed and trimmed as each part finishes, continuously. Owner verbatim stays protected in the graph node (`vision`/`goal`/`hypothesis`/`doc`), never here.

## `COMPLETE.md` — every finished loop writes one (`goal:g1.13`)

**`HANDOFF.md` bridges sessions and is deleted by the next director. Nothing
closed a loop**, so a loop's gaps were recorded in prose somebody was instructed
to erase, and the same gaps came back — measured on L1: 16 hazards carried in a
handoff table became `goal:s34`, which closed roughly 2 of them.

**When a loop ends, write `COMPLETE.md` at the repo root** — the closing record
of that loop, the way `HANDOFF.md` is the live one of a session.

**Same rule as `HANDOFF.md`: replace it whole, unless the owner asks otherwise.**
Default is one loop's report at a time. **Append only when the owner says to** —
which they do when the next loop is actively continuing off the last one and
both reports need to be in front of a reader at once. Erasing is safe for the
same measured reason it is safe there: `COMPLETE.md` is `build:COMPLETE.md`, so
every prior report is one command away —
`grid.py payload build:COMPLETE.md --version N` — and accumulating costs every
future session context while buying nothing. When you do append, newest first.

Seven sections, in this order:

1. **What ran** — waves, dispatch counts, harness, spend.
2. **The scoreboard** — node counts, primary metric, evidence fraction, suite,
   links; start and end.
3. **Per active goal, how far it got** — grounded in a commit, a node diff or a
   parent report. Never recollection. A claim you cannot ground says so.
4. **How many goals actually closed**, plus any `complete` the record cannot
   substantiate. (L1 found one: `goal:g4.6` was marked complete two days before
   the adapter it names existed.)
5. **A completion-failure category for everything that did not close.** The set
   is closed and deliberately small: `saturation`,
   `ceiling-found-by-dying`, `late-minting`, `hazard-carry-over`,
   `banked-to-owner`, `verification-blindness`, `attribution-void`.
   **A decision banked to the owner counts as a failure here** — not the model's,
   the harness's, for not giving the director enough to decide with.
6. **Findings that are not failures** — *optional; omit the heading when there
   are none.* What the loop learned that is neither a closure nor a failure: a
   mechanism that turned out to work, a cause finally traced, an observation
   worth carrying. Added after the first report had one and the format had
   nowhere to put it, so it was filed as a failure's footnote — a shape that
   quietly teaches a loop to report only what went wrong.
7. **What was minted or changed in response**, linked as graph edges.

**Why the category set is closed, and why that matters more than the prose.**
These labels are training data. The gaps a completion review finds — a goal
marked complete before its code existed, hazards carried instead of closed,
goals minted hours before the budget ends — are pattern-matchable against a
parent's own report, and are the first slot on `goal:g14`'s lattice worth filling
with a classifier. A free-text report teaches nothing; a fixed label set over
many loops is a dataset.

**This section is prompt text today and is not meant to stay that way.** The
standing migration path, which applies to every rule in this document: write it
here as prose, watch it hold or fail across a few loops, then replace it with
harness code or a scored small model. An instruction that *could* be a check and
is instead handed to a model is an invariant turned into a coin flip.

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
- **Read `struggles:` and `caveats:` before reviewing the node.** On 2026-09-01 those two lines produced: the evidence gate's self-citation hole, `--evidence-runs` being absent from the `done` template, the `pi_adapter` frontmatter contradiction, and two bugs in a change the parent had just landed. Every one was found by the agent and missed by the parent's review. They are one line each and they are the cheapest signal in the system.

## Querying the code as a graph — `gitnexus` (optional, verify before trusting)

`iomap` (the engine's own source as a queryable graph) is unbuilt. **`gitnexus`
is the interim**, and it works, with two sharp edges measured on 2026-09-01:

```bash
npx gitnexus status                                     # is the index current?
npx gitnexus analyze                                    # ~9s, 2934 nodes / 6912 edges
npx gitnexus query "<concept>" --repo /home/ubuntu/work/agi
```

- **Always pass `--repo` as an absolute PATH, not a name.** Two different
  checkouts register as `agi` (`/home/ubuntu/work/agi` and
  `/home/ubuntu/.hermes/agi`), so `--repo agi` is ambiguous and errors out.
- **The index is pinned to a commit and this loop commits every iteration**,
  so it is stale almost immediately. `status` tells you; `analyze` is ~9s,
  which is cheap enough to re-run rather than reason over a stale graph.
- 🔴 **It is a semantic search, not an oracle, and it does not replace `grep`.**
  Measured: *"how does post_wire decide an agent is done"* returned
  `GraphBuilder` in `agi_algos/graph_builder.py` — unrelated. A second query
  returned the right area but the tests rather than the module. **Treat a hit
  as a place to start reading and confirm it with `grep`;** a confidently wrong
  pointer costs more than the search saved, and stale or wrong grounding has
  already invalidated real work in this project.

## Safety rails (non-negotiable)

- **Never create `<project-root>/bin/snapshot-build-site.py` or `bin/render-context.py`** — that's `.agi/bin/*.py` under this layout, since `driver.sh` resolves the project root to `.agi/` and prefers a script there over the engine's own. Stale copies have silently wiped an entire node corpus (29,264 files) and separately broken the render path. Treat any such file as stale until proven otherwise.
- **Engine improvements go in the engine's own source** (`extensions/`, `skills/`, `src/`). **Graph and domain output go in `.agi/`.** A downstream project never forks engine code to get project-specific behavior — see Configuration.
- **Kids that stall or wander out of zoom scope:** kill, log, respawn narrower.
- **Verify the node count never drops** after a snapshot.


<!-- COMMANDS:BEGIN -->
<!-- This section is AUTO-GENERATED from `.geometry/commands.md`.
     Edit the node — never this table directly. -->

| Command | Does |
|---|---|
| `bash '<engine>/extensions/agi/driver.sh' --smoke --max-iters 1` | snapshot + render + metrics, no dispatch — verify the node count did not drop |
| `python3 -m pytest '<engine>/extensions/agi/tests/' -q` | the engine's own suite |
| `python3 '<engine>/extensions/agi/bin/snapshot-goals.py' --render --check` | GOALS.md and the goal nodes are byte-identical inverses |
| `python3 '<engine>/extensions/agi/bin/viewport.py' --verify` | goal:g9.7 — one render, two readers |
| `python3 '<engine>/extensions/agi/bin/grid.py' commit --all` | version every changed node and its payload |
| `python3 '<engine>/extensions/agi/bin/links.py' links` | goal:g13 — every node's link resolves; broken_links must be 0 |
| `python3 '<engine>/extensions/agi/bin/links.py' schema` | goal:s31 — which nodes violate their type's required list (dry) |
| `python3 '<engine>/extensions/agi/bin/spawn_budget.py' status` | goal:g4.8 — live agents against the tree-wide bound |
| `python3 '<engine>/extensions/agi/bin/provisioning.py' status` | goal:g1.11 — whether per-spawn keys are being issued |
| `python3 '<engine>/extensions/agi/bin/envfile.py' --check` | goal:g1.8 — required keys present, forbidden keys absent |
| `python3 '<engine>/extensions/agi/bin/crons.py' show` | the crontab the graph declares |
| `python3 '<engine>/extensions/agi/bin/viewport.py' --live` | the live graph, agents drawn as spiders where they are working |
| `python3 '<engine>/extensions/agi/bin/viewport.py' --emit llm` | goal:g9.7 — exactly what a kid is handed, from the same frame stream |
| `python3 '<engine>/extensions/agi/bin/viewport.py' --emit both` | human and llm views side by side, from ONE stream |
| `python3 '<engine>/extensions/agi/bin/write.py'` | goal:g13.1 — named node operations; a hand edit becomes an engine action |
<!-- COMMANDS:END -->
