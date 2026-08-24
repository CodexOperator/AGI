# GOALS.md — agi-tree long-term goals

`agi-tree` is the thoughtgraph that builds `agi`; `agi` is the code that operates
on thoughtgraphs. These goals are the **engine's own design contract** — the
durable commitments engine work serves, and **the only place new work is
recorded**. `agi/TODO.md` was demoted to an archive on 2026-08-22 (L19 action 4):
it keeps the reasoning behind each closed defect, which is worth preserving, but
nothing new is added there. Goals below cite the `L`/`H` entries they absorbed so
the reasoning stays reachable without the two documents restating each other —
two sources of truth about the same defects is how the injected context once
ended up teaching the opposite of the skill (H3b).

Seed nodes in `nodes/idea/` join a goal by listing its id in their own
`parents:` list (`parents: [goal:g3]`). `bin/snapshot-goals.py` derives
`nodes/goal/` from this file, so **this file stays the human-authored source of
truth** and the nodes are never edited by hand.

**Goal lifecycle:** `active` (being worked) · `horizon` (declared and committed
to, not yet being worked) · `phasing-out` (retiring) · `complete`. Retire by
marking the section `status: phasing-out` and **deprecating — never deleting**
its seed node; retired chains remain prior art.

**Three kinds of goal, all first-class nodes.** This is where new work gets
recorded — a defect or an idea belongs here, not in a second document.

| Heading | Becomes | Use for |
|---|---|---|
| `## G7 — Title — status: X` | `goal:g7`, a root | A long-term commitment. Rare; these barely change. |
| `### G7.2 — Title — status: X` | `goal:g7.2`, `parents: [goal:g7]` | A concrete near-term step **inside** a long-term goal. This is where most new work lands. |
| `## S4 — Title — status: X` | `goal:s4`, a root | A standalone short-term item that serves no single long-term goal. TODO-shaped. |

A sub-goal parent-points at its long-term goal exactly the way a seed idea
does, so it renders and traverses for free. Sub-goals carry their own `status`
independently of their parent — `G2` can be `horizon` while `G2.1` is `active`,
which is precisely how a long-term commitment gets worked one step at a time.

**Goal ids are never renumbered.** Nodes reference goals by id, so a gap is
always preferable to a renumber. Sub-goal numbers are likewise permanent: a
completed `G7.2` stays `G7.2` and the next step is `G7.3`.

**Sub-goals are sub-nodes, not a separate concept.** A goal node contains
sub-nodes the same way any node contains sub-nodes at the next zoom level down.
`goal:g7` at level 1 ⇔ `goal:g7.1`, `goal:g7.2`, … at the level below, and each
of those ⇔ the ideas, hypotheses and level-3 nodes beneath it. The zoom axis and
the goal hierarchy are the same mechanism, not two that resemble each other.

---

## The working rule — every change starts here and is built back into the engine

**All future work — fixes, upgrades, extensions, reworks — originates as a node
in `agi-tree` and is built back into `agi` for subsequent use.** Not "recorded
here afterwards": *originates* here. The engine is the artefact this graph
assembles; a change that appears in the engine without a node behind it is the
open loop G6 exists to close.

The mechanism is in place and measured as of 2026-08-22: `decompose-engine.py`
mints one census node per engine surface, `level3.py` mints one node per code
file with a derived contract, and `stitch.py --verify` reports drift in four
categories, including a contract that no longer matches the code it describes.
`stitch.py` materialises the graph back to a tree byte-for-byte.

**Build nodes and non-build nodes.** A **build node** contains or points at
production code — today that is the `level3` type, whose `payload_ref` resolves
to a real file. A **non-build node** is everything else: idea, hypothesis,
experiment, verdict, outcome, goal. **Both are equally important.** The
non-build layer is where a change is argued, tested and judged; the build layer
is where it lands. A build node with no non-build chain behind it is
unattributed work, and a non-build chain that never reaches a build node has
not shipped.

**The design ethic binds every goal here, whatever its status.** Emitted tokens
are an agent's motion; injected context is its sensation; context growth makes
motion heavier. Every capability exists to keep agent bodies light — sprint one
node hard, hand off, rest, and let the graph carry the marathon. Mundane
operations, and the small errors they breed, are the system's job to absorb and
never the agent's. Full statement: `agi/skills/agi/SKILL.md` §"Why this
machinery exists".

**Scope boundary (`TODO.md` L8, decided).** `agi` and `agi-tree` stay separate
repos. This file holds goals about the *engine*; a project holds goals about its
own domain. `fantasia/GOALS.md` is the reference for the project side — engine
work must never be tracked in a project repo again (that was fantasia's deleted
G2).

---

## The design ethic — power armor, not a heavier pack

The engine's job is to make an agent's work **more vigorous, not more strenuous.**
Motion is what an LLM spends; weight is what it carries while spending it. Every
token emitted or sensed rides along for the rest of the run, so an agent that had
to *find* its context arrives at the actual work already loaded down. The target
is the opposite shape: **arrive knowing where you are, hit hard, hand off, rest.**
Power armor amplifies the wearer; it does not ask the wearer to carry it.

This is a stronger claim than "the loop is convenient", and it has to be, because
convenience is unfalsifiable and this is not:

**The measurable: an agent doing real work in this graph should make more graph
calls than filesystem calls.** Not zero file reads — some questions genuinely
live outside the graph. But the ratio is the whole thesis. If agents keep
grepping source to answer questions the graph claims to hold, the graph is
decoration and the armor is a pack.

**First measurement, 2026-08-23 (`exp:evidence-gate-coverage`), and it is a
failing one: 3 graph calls against ~28 file reads and bash calls.** The kid
reported it unprompted and diagnosed it correctly — the question turned on
protocol documents and git history that the graph does not represent. That is
**G6.6**'s coverage gap arriving from an independent direction, and it is the
honest baseline this ethic gets measured against from here. Record the ratio on
work that matters; do not tune it by asking easier questions.

What the ethic forbids, stated so it can be enforced rather than admired:

- **No prose-only controls where a code control is possible.** "The parent
  reviews by hand" is not a mechanism, it is a hope with a name. **S9** exists
  because that class of control let 104 unevidenced verdicts accumulate for three
  and a half months, and `exp:evidence-gate-coverage` found the same class still
  load-bearing in the CC runtime today.
- **No mundane step without a command** (G1), and no command that has to be
  remembered rather than installed (G1.5).
- **No context an agent has to reassemble** that a previous agent already
  assembled. That is what the graph is *for*; a re-derivation is a bug report
  against it.

The corollary is uncomfortable and load-bearing: **when an agent has to leave the
graph to do its job, that is evidence against the graph, not against the agent.**
Log it, do not scold it.

## G1 — Zero-operations loop: every mundane step is a command — status: horizon

The ethic above, reduced to buildable surface. An agent should never spend
motion on tending the machine: no hand-pasting a rendered map into a spawn
prompt, no hand-writing a config, no syncing by hand.

**Invariant:** any repeated, mechanical step is a named command, and every
surviving manual handle carries a written reason.

Already banked — cron owns all remote traffic (H10), embedded maps cut kids from
11–13 tool calls to 5–7 (L7), the DONE contract makes stopping one line.

Owns: **L11** remainder (one command that renders *and* spawns — the parent's
last machine-tending chore), **L12** remainder (a runtime flag rather than a
parallel code path; hook parity audit), **L17** (config schema plus a writer, so
configs stop being hand-written), **L18** action 2 (`agi-tree init` scaffolds a
project), **H6** (`--iter-base N` for `dispatch.py`, so a run stops clobbering
prior session manifests).

### G1.1 — An agent should need only the graph to orient — status: active

**Recon happens in the graph, not in the filesystem.** Today a kid arrives with
a rendered map and then reads files anyway, because the map cannot answer
follow-up questions. Every one of those reads is motion spent re-deriving
context the graph already holds.

What has to exist: an agent can **move** through the graph from where it was
dropped — step to a neighbour, pull a snapshot of an adjacent region, widen to
the enclosing map — without opening a source file and without a second spawn.
The level-3 nodes make this newly plausible: a node already carries
`payload_ref` and a derived contract, so "what does this module take and
promise" is answerable from the graph alone.

The measurable version, and the reason this is worth doing: kids dropped from
11–13 tool calls to 5–7 when the map was embedded in the prompt. The target is
the same curve applied to follow-up reads — an agent that navigates instead of
grepping. Falsifier: if agents given navigation still read the same number of
files, the graph is not carrying the context it claims to.

Shares its substrate with G9.4 — the viewport a human pans and the region an
agent requests are the same query at different resolutions. Build them as one
mechanism with two front-ends, not two renderers that drift.

### G1.2 — One skill: fold in caveman, cavekit, and gitnexus — status: horizon

Four systems overlap in this repo and none of them know about the others:
**agi** (this loop), **caveman** (compressed communication, ~75% fewer tokens),
**cavekit** (kits → build sites → tiered task graphs, with its own peer-review
and convergence machinery), and **gitnexus** (a real code index with symbols,
call graph and execution flows).

Each holds a piece this loop needs. Caveman is directly the design ethic —
motion is expensive, so compress it — and belongs in kid briefs, not just in
chat. Cavekit's build-site → task decomposition is *already* wired in, via
`snapshot-build-site.py`, and its tier/dependency model is close to what G6.4
needs for build-node branching. GitNexus is the natural seed for zoom levels 4–5
where agi has no data at all.

Take pieces; do not merge wholesale. The failure to avoid is four overlapping
vocabularies for one idea — this project has already shown what happens when two
documents describe the same defects (H3b). Absorbs **H8** (SKILL.md propagation),
which should be done as part of deciding the boundary rather than before it.

**Known constraint, measured:** GitNexus excludes any directory named `bin/`, so
it currently indexes zero symbols for all fifteen engine entry points. See
**S1** — that is the same problem from the other end.

### G1.3 — The injected map teaches its own use — status: active

**The map shows what is in the graph and says nothing about how to move through
it.** An agent arrives holding 200 lines of ASCII render and no addressing
scheme, so the only move it knows is the one it brought from outside: open a
file. G1.1 asks for navigation to *exist*; this asks for the injected context to
*teach* it, in the same block, at the top, before the agent has spent a token.

**Adopt the supermap convention rather than inventing one.** The `.openclaw` and
`.hermes` harnesses already address a workspace coordinate-first — short stable
handles, a compact legend, full injection on the first turn and deltas after,
with an explicit refresh command instead of a per-turn re-render. Two properties
are worth copying exactly:

- **Coordinates, not identifiers.** A node is reachable by a short handle an
  agent can hold in working memory and name in one token, not by a 40-character
  id it has to copy. Ids stay canonical on disk; coordinates are the interface.
- **Full once, deltas after.** The first injection carries the whole map and the
  legend. Subsequent refreshes carry what changed. Re-rendering the entire graph
  every turn is precisely the motion this loop exists to remove.

The legend is the part that does not exist today and is the cheapest half: a
short header listing the moves available — step to a neighbour, widen, pull an
adjacent region, refresh — so navigation is discoverable from the context rather
than from a skill file the kid was never given.

**Familiarity is the point, and it is a real constraint, not a preference.** The
operator already thinks in this vocabulary across two other harnesses. A third
dialect for the same idea is the G1.2 failure mode — four overlapping
vocabularies for one concept — arriving through the front door.

Falsifier, and it must be checked both ways: if kids given coordinates still
quote full node ids and still request whole-graph renders to answer a follow-up,
the layer added tokens instead of saving them. If the injected block grows
faster than tool calls fall, the legend is too long.

Shares its substrate with **G1.1** and **G9.4** — the coordinate a kid names,
the region it requests and the viewport a human pans are one query at three
resolutions. Build one mechanism with three front-ends.

### G1.4 — Kids get the graph and nothing else — status: active

**A kid should not be able to spend motion on anything but the graph.** Weight
is the reason: everything a kid reads rides along in its context for the rest of
the run, and most of what it reads is context the graph already holds — this is
G1.1's finding stated as a permission rather than a capability. A kid that
*cannot* open a source file cannot re-derive what it was already handed.

The parent is exempt. It reviews, judges and commits; that is filesystem work by
definition. This is a constraint on kids only.

**Staged on purpose, and the order is not negotiable.**

1. **Now — say it and measure it.** The kid brief states graph-only, and
   `dispatch.py` logs every tool call a kid makes. A metric counts non-graph
   calls per kid per iteration. Kids can still escape when genuinely stuck, and
   *that escape is the measurement* — it says exactly which question the graph
   could not answer.
2. **Then — the allowlist.** Kids spawn with graph tools only; no `Read`,
   `Grep`, `Glob`, `Bash`. The allowlist is derived from what stage 1 observed,
   not guessed in advance.

**The gate between the stages, stated so it cannot be skipped:** if stage 1 shows
kids reaching for files the graph genuinely cannot answer, that is a **G1.1 gap,
not a discipline problem**. Clamping the tools first would convert a missing
navigation feature into a silent kid failure, and the loop would report fewer
tool calls while producing worse nodes — the metric improving as the work gets
worse. Fix the graph, then clamp.

Falsifier: non-graph tool calls per kid trend to zero in stage 1 *without* node
quality dropping. If quality drops, the graph is not yet carrying what it claims
and stage 2 must not ship.

### G1.5 — `init` leaves nothing to install by hand — status: active

**Setting up a project is currently three manual steps and a memory test.** The
commands all exist and none of them are called by anything:

- `grid.py init` — adds the `refs/grid/*` fetch refspec to origin. Skip it and a
  fresh clone silently has no version history; nothing warns, the grid is simply
  absent.
- `grid.py cron install` — the two-cadence sync (5-minute snapshot + grid push,
  hourly D1 push). Skip it and the crash-recovery window is not ≤5 minutes, it
  is however long since someone last remembered.
- The project scaffold itself — `agi-tree.config.json`, `nodes/`, `context/` —
  is **L18 action 2** and does not exist at all. `cli.py scaffold` scaffolds a
  node, not a project.

This is G1's invariant failing on G1's own setup path: three repeated mechanical
steps, none of them a named command, none carrying a written reason for staying
manual. The failure mode is silent in both directions — an uninitialised grid
and an uninstalled cron both look exactly like a working project until the day
you need the history.

What has to exist: one command that takes a directory to a running project —
config written from a schema (**L17**) rather than by hand, `nodes/` and
`context/` scaffolded, grid refspec configured, crons installed, and the whole
thing idempotent so re-running it on a live project is safe and does nothing.

**Verify the cron the way S2 had to be verified.** `grid.py cron install` must
confirm which branch is actually checked out, because agi-tree's own work once
sat on a stale `iter24-extend-300hop` branch while a cron pushed `master` and
published nothing, silently, indefinitely. An installer that writes a crontab
line without that check just automates the same failure faster.

Pairs with **G8.1** — whatever the distribution shape turns out to be
(drop-in clone, skill package, installer), this is the command it has to end in.

Falsifier: clone the repo to an empty machine, run the one command, and check
that `git fetch` brings the grid down and `crontab -l` shows both cadences. If
either needs a second command, this is not done.

### G1.6 — Every action is a one-word command, inside the project — status: active

**No more reaching for a file whose path you have to know.** Today an agent runs
`python3 agi/extensions/agi/bin/zoom.py "$PWD" 9006 kid-a --level small --target
goal:g6.3`. Every element of that except `goal:g6.3` is ceremony — an interpreter,
a four-segment path, a redundant cwd, an iteration number and an agent id the
harness already knows. The agent spends motion on the invocation instead of the
question, and gets the path wrong sometimes, which is worse.

**Target: one or two words, options optional, discoverable from inside the
project.** `agi zoom goal:g6.3`. `agi node new hypothesis --parent goal:g6.3`.
`agi resume <grid-ref>`. `agi audit`. Installed as part of adding agi to any
project (**G1.5**), so the command surface exists the moment the project does and
is identical in every project.

The list worth having, drawn from what actually cost tool calls in the 2026-08-23
run:
- **navigate** — zoom to a node, widen, step to a neighbour, raise LOD (**G10**)
- **write** — create or edit a node without hand-assembling frontmatter, which is
  where kids currently spend their first three tool calls and where they get
  `evidence_runs` shapes wrong
- **resume** — pick up from any point in the grid, which is the crash-recovery
  story the two-cadence cron already half-implements
- **audit** — what is unevidenced, what is orphaned, what fails to parse. Every
  one of those was a bespoke Python one-liner this session

**The measurable is the point, not the ergonomics:** fewer tool calls and fewer
tokens burned on recon *and* on acting. This is the Design Ethic's ratio attacked
from the second side — G1.3 and G10 reduce the recon a task needs, this reduces
what each action costs once you know what to do.

Note the reflexive risk and avoid it: these commands are engine surface, so under
**G6.8** they arrive from nodes rather than being written directly. Absorbs
**S1**'s rename (`bin/` is invisible to GitNexus) — do them together, since both
touch every entry point.

Falsifier: take the transcript of any completed iteration and count invocations
that needed an absolute path or an interpreter prefix. Not done until that is zero.

## G2 — Adjustable zoom with contracts that survive the trip — status: active

One graph readable at five grains, where level 3 is **actual code nodes that
stitch into a runnable directory layout** — the property that makes the graph an
executable artifact rather than a description of one. Build level 3 first and
treat the others as projections around it.

**Invariant:** one node at level N ⇔ a collection at level N+1, and back.

🔴 **Already falsified for the free-form implementation, and the number is
known:** 0.441 overall claim recall against a 0.90 bar, 12 agents over 6
complete round trips. Loss is category-structured, not uniform — prose survives
at 0.792, structured frontmatter recalls **0.000** (0/24, zero variance). Node
identity is destroyed outright, and it is not a capacity problem: the children
were longer than the parents.

**Design consequence:** zoom is a lossy transform, not a view. To behave like a
view, contract-bearing parts must not pass through a model at all — the harness
attaches inherited frontmatter and contract slices mechanically, and only prose
round-trips. Ground truth and scoring rule are preserved at
`agi/context/refs/zoom-roundtrip-ground-truth/` so the follow-up A/B stays cheap.

Owns: **L1** (the 1..5 axis), **L2** (live IO maps as inherited contract slices).

### G2.1 — Level 3 first: code nodes that stitch back into a running tree — status: active

**Build level 3 before any other level.** It is the one that makes the graph an
executable artifact rather than a description of one, and it is the level with
an existing index to stand on: GitNexus already holds this repo's symbols, call
graph and execution flows. A level-3 node is not a new parse of the code — it is
a code surface **plus the thought attached to it**: why it exists, what it
promises, what it requires.

What has to be true:
- A level-3 node round-trips: graph → directory of files → running software →
  back to graph, with no hand-editing in either direction.
- Its contract half (IO map, invariant citations, file paths, frontmatter) is
  **attached mechanically by the harness**, never authored by a summarising
  model. G2's measured falsifier is why: 0.000 frontmatter recall, 0.111 file
  paths.
- The index is a *seed*, not the source of truth. Known gap: GitNexus has zero
  symbol coverage of all twelve `bin/*.py`, which is the half of the engine
  where every 2026-08 change landed.

### G2.2 — IO maps as inherited contract slices — status: active

Every node declares required inputs and promised outputs, each with a how/why,
a performance note and a security note; the maps re-derive when neighbours
change.

**Half of this shipped 2026-08-22 and the half that shipped is the mechanical
half** — `level3.py` emits 1,110 contract entries whose `how` is derived from
`ast` with a line number, and `stitch.py --verify` re-derives and diffs them, so
a contract that drifts from its code is detected rather than rotting invisibly.
That is the freshness problem the anatomy node had recorded as unsolved.

**What remains is the judgement half.** `why`, `perf` and `security` are emitted
as explicit `TODO(model)` placeholders — deliberately blank, because a
fabricated security note is worse than an absent one. Filling them is a model
pass over the placeholders, and it is the first real test of the split this goal
rests on: the harness owns the shape, the model only ever fills free text. Its
falsifier is already pre-registered in `hyp:level3-node-anatomy` — harness
fields must hit 1.000 recall by construction, and prose must hold ≥ 0.792.

Do the model pass only after **S3** — a truncated `how` can currently contain a
fence-lookalike that trips a naive reader, and the model pass is exactly the
next consumer that would hit it.

### G2.3 — `graph_builder` becomes data-source-agnostic and cold-builds fast — status: horizon

`agi_algos/graph_builder.py` is the code-intelligence layer and the natural
substrate for zoom levels 4–5, but it is coupled to specific data sources and is
slow on a cold build. Absorbs **A1** (data-source-agnostic refactor) and **A3**
(cold-build optimisation).

Also carries a cleanup with a real trap in it: `graph_builder.parse_goals()`
parses a *different* `goals/` directory into `goal`-type nodes for a 35-node-type
code graph, and its only call site hardcodes a path that no longer exists, so it
returns 0. It is dead code, unrelated to `GOALS.md`, and **two different things
named "goal" in one codebase will mislead every future reader.** Repoint or
delete it.

### G2.4 — Embeddings into the production renderer path — status: horizon

gensim + UMAP embeddings exist and are not on the renderer path (**H7**).
Relevant to this goal rather than to G9 because a projection is a zoom
operation: it is how level 1 and 2 get a spatial layout that is stable as the
graph grows, which is what G9.4's viewport needs to pan across without the graph
rearranging itself under the reader.

Note `.gitnexus/meta.json` reports `embeddings: 0` — nothing is generated today,
and `npx gitnexus analyze` without `--embeddings` deletes any that exist.

## G3 — Scoring that added motion cannot move — status: active

The graph is measured by goals reached, never by motion spent. This goal exists
because the opposite was tried and it worked: 9 chains × 2000 hops via shortcut
cycles, carrying no signal, and the resulting structure then broke the render
path outright.

**Invariants:**
- No primary metric that appending hops can shift. `longest_chain_length` is a
  descriptive statistic, never a target.
- A decisive verdict (`proved` / `disproved`) requires `evidence_runs >= 1`.
  Unevidenced claims are demoted, not discarded — the expensive artifact is kept,
  only the overclaim is dropped.
- `unevidenced_decisive_verdicts` reads `0`. Nonzero means a bypass or a
  hand-edited node.

Banked: **H3** (metric computation out of the driver heredoc into `metrics.py`;
`evidence_fraction`, `evidence_weighted_depth`; gameable-primary warning) and
**H4** (the gate in code, on both writer paths). This project's own config
migrated off `longest_chain_length` on 2026-08-21.

Still open, and the reason this stays active: **L4** — `outcome_coverage` is a
*proxy* that counts chains reaching an outcome, not their **attribution to a
specific goal**. True goal-fulfilment scoring is unbuilt. The goal nodes it
needs exist as of L15.

### G3.1 — `evidence_runs` must resolve to a real node — status: active

🔴 **The evidence metric was itself gamed, and by the cheapest possible move.**
`normalize_evidence_runs` returns `len(value)` for any list, so
`evidence_runs: [synthetic]` — the literal string — satisfies `evidence_runs >= 1`
and the gate passes a `proved` verdict that ran nothing. Measured on this
corpus before the padding offload: 2,842 of 2,869 verdicts carrying
`evidence_runs` used that sentinel; 16 cited a resolvable `exp:` id.

Fix: count only entries that resolve to a real node in the corpus; treat a
non-id string as a taxonomy violation that fails closed, not a silent pass.
Then re-measure and record a corrected baseline on both live projects.

**Until this lands, no `evidence_fraction` reading means anything** — including
the post-offload 0.365, of which 33 of 121 surviving verdicts are still
sentinel-backed. Owns TODO **H4c**.

## G4 — Right model at the right grain, several goals at once — status: horizon

Model choice is a knob the user sets per tier and experiments with — nothing
hardcoded. Three tiers: **delegator** (the user's own session, holding intent
and coordinating several parent/kid groups), **parent** (a subagent by default,
so review motion never accumulates in the chat the user reads), **kid** (one
node, bounded scope).

**Not refuted by G2's evidence — its price is now a number.** Prose recall of
0.792 from a cheap tier is what a cheap tier is *for*. What is refuted is
handing the cheap tier the contract layer. Tiering survives if the model authors
prose and the harness moves structure.

**Budget invariant:** inner-loop completions count against a single global
iteration budget, so recursion is bounded regardless of nesting depth.

Owns: **L3** (per-tier and eventually per-level model assignment), **L6**
(recursive sub-loops; `cc_dispatch.max_goals_active` exists and is unread).
Blocked on G2 for per-level assignment.

### G4.1 — Parallel kids share one working tree and collide — status: active

Observed live 2026-08-22, by both kids of the same iteration independently.
Two kids doing **engine** work ran concurrently in one checkout: one was
rewriting `evidence_gate.py`, `metrics.py`, `cli.py` and `post_wire.py` while
the other was running the test suite against them. Consequences seen: the test
suite failed for several minutes on code neither kid had broken, and
`evidence_fraction` flipped between 0.365 and 0.035 on an unchanged corpus —
a stale-`.pyc` race against a file being rewritten underneath the interpreter.

Both kids diagnosed it correctly and neither corrupted anything, so the cost
this time was wasted motion and a briefly false test signal. **The failure
mode is that a kid reports a red suite it did not cause, or a green one it did
not earn.**

Kids writing *nodes* are naturally isolated — one file each. Kids writing
*engine code* are not isolated at all, and the closed loop (G6) makes engine
work the normal case rather than the exception.

Options, undecided: give each engine-writing kid its own worktree
(`isolation: worktree` already exists in the dispatch layer); serialise
engine-writing kids within an iteration; or partition by file ownership
declared in the brief. Measure before choosing — the worktree option costs a
checkout per kid and may not be worth it at two kids.

**Partial result, 2026-08-22:** file ownership declared explicitly in the brief
was tried across two iterations of two kids each. No collisions, and both kids
correctly attributed sibling breakage instead of claiming it. That is one
data point at two kids on disjoint files, not a solution — it says nothing
about kids that genuinely need the same file.

### G4.2 — A reasoning-effort dial, not just a model name — status: active

`cc_dispatch.kid_model` selects the model. **Nothing selects how hard it
thinks.** Asked for "sonnet 5 on max settings" the honest answer was that the
dispatch surface exposes model choice and not reasoning budget, so the request
had to be approximated by wording in the brief.

That is a real gap in L3's "fully configurable per tier" claim: a tier is
currently a model name and nothing else. Add effort/reasoning budget as a
per-tier config key alongside `kid_model` and `parent_model`, and make the
delegator tier configurable the same way.

Worth measuring rather than assuming: run the same brief at different efforts
and see whether node quality moves enough to justify the cost. This project's
own evidence says cheap tiers are fine for prose and catastrophic for contract
structure (0.792 vs 0.000) — effort may split the same way.

### G4.3 — Finish the runtime split: pi and Claude Code as one path — status: horizon

**L12** remainder plus **H9**. Anywhere the engine invokes `pi`, allow invoking
Claude Code instead — a runtime flag, not a parallel code path — and audit hook
parity between the two. H9's kid→parent question channel exists for the CC path
(four escalation triggers, one question per kid) and not for pi.

**H4b** belongs here too: `driver.sh` calls `benchmark.py` with the wrong
arguments under `|| true`, so it may never have run. That matters beyond the
bug — `benchmark.py` is what reaches `ranking.py` and the weighted attractiveness
path, which means the ranking this loop supposedly selects targets with has
never been confirmed to execute at all.

### G4.4 — A web of specialists, each owning a region — status: horizon

**Where the model-tiering goes once the dial exists.** G4.2 gives per-tier effort;
this is what to do with it. The target shape: many small, hyper-specialised models
each owning a **region of a zoom level** of the hypergraph, a smaller number of
capable parents reviewing across regions, and a very small number of directors
holding intent. Specialisation is by *territory*, not by task type — an agent that
only ever works one region accumulates a sharper prior about it than a generalist
re-reading it cold every time.

**The objective function, stated plainly because it is the actual constraint:
functional output per token spent.** Not quality alone and not cost alone — the
ratio. A director on the largest model is worth its cost only if it multiplies
what the tiers below produce.

**Fine-tuning is the horizon, and it has a dependency the rest of this list
doesn't:** a specialist tuned on a region needs that region to be stable enough to
be worth learning. That argues for doing **G10** and **G6.8** first — you cannot
tune a model on a territory whose shape and contents are still being decided.

**Honest near-term constraint, recorded so the plan is not built on it.** Local
inference on a 16 GB machine does not produce a peer to the parents; it produces a
*mechanical* worker. That is not a disappointment, it is the split this system
already believes in — the harness derives mechanically, the model fills judgement
(**G2.2**). The jobs a local model can genuinely take off the paid tiers are the
mechanical half: frontmatter assembly and validation, census and counting, LOD
compaction (**G10**), draft node scaffolding for a parent to review. Every one of
those is currently done by a paid model or a bespoke script.

What it cannot do is act as an autocomplete in front of a larger model — there is
no cross-provider speculative decoding, and any "check my draft" arrangement pays
the full input cost of the draft anyway. The saving comes from work the local model
**completes**, never from work it merely starts.

Depends on **G4.2** (the dial), **G4.1** (parallel kids must stop colliding before
there are many more of them), and **G10** for stable territory.

## G5 — Goals are a lifecycle the engine reads, not a human convention — status: horizon

`status:` should be a field the engine acts on: stop accruing score to
`phasing-out` and `complete` goals while keeping their chains attributable, and
fail loudly when a seed node points at a goal id that does not exist.

**Invariant:** a project is legitimate at three depths — goals only (ideation),
goals + seed ideas (chains starting), goals + build site (execution). A
goals-only project is a valid state, not a broken one.

Banked: **L15** — goals are first-class nodes, derived from this file, linked by
parent-pointing, with referential integrity live and an H0-safe origin-guarded
prune. A missing `GOALS.md` prunes nothing.

Owns: **L5** (rotation the engine enforces), **L18** (the ideation stage; a
missing build site must degrade like a missing `GOALS.md` does, not abort the
driver).

## G6 — The closed loop: engine work starts in the graph — status: active

Run `agi` and `agi-tree` against each other and the pair is closed: a change to
the engine originates as a node in this graph, and the engine that grows this
graph is the thing the node changed. Neither is the author of the other — the
graph is the sequence, the engine is the machinery that reads it.

Today the loop is open. Engine reasoning lives in `TODO.md` and `CLAUDE.md` as
prose, gets read by agents, and never returns to the graph.

**Invariants:**
- An engine change is reviewable as **node → verdict → commit**.
- The decomposition is **generated, never hand-written** — a hand-authored map
  goes stale exactly the way `domain-exporters` did.
- Deprecate superseded mass; **never delete it.** Retired nodes remain prior art
  and remain evidence.

Known state of this graph: the idea layer already decomposes an *older* engine —
`domain-exporters` and `domain-environment-indexers` describe modules that no
longer exist, and there is no idea node at all for `src/agi_algos`, the twelve
`bin/*.py`, `driver.sh`, `hooks/`, `lib/`, `scripts/`, or `extensions/agi-bridge/`.
The half of the engine that actually changes is the half with no representation.
Below the idea layer it is not a decomposition of anything: ~14.5k experiments
and ~14.6k verdicts against 14 ideas is the H3 gaming artifact, not thought.

Owns: **L19**. Preconditions cleared 2026-08-21: H3 config migration (this
project), this file, and H0e (truncated chain results no longer cached as
complete).

### G6.1 — agi-tree becomes the source of truth agi is assembled from — status: active

**The direction of authority reverses.** Today the graph describes the engine
after the fact. The target is that the engine is *assembled from* the graph —
the code is a projection of level-3 nodes, not a thing the nodes comment on.
This is the goal G2.1 serves and the reason level 3 is built first.

Ordering that follows from it: a decomposition census (which surfaces exist) →
level-3 nodes with contracts attached (what each promises) → stitch-to-directory
(the projection runs) → the engine's own changes originating as nodes.

### G6.2 — Retire the padding and keep it recoverable — status: complete

Done 2026-08-21. 28,916 gamed `-extend<N>` experiment/verdict nodes were
removed from the working tree and archived outside the repo with a manifest
recording the predicate, family and index of every one. 122 family heads were
preserved in-tree as prior art for H3's own finding.

Deviation recorded on purpose: G6/G7 say deprecate, never delete. The owner
directed removal so the git grid would not be initialised over ~29k refs of
baggage. "Never delete" was honoured by **relocation** — archive plus manifest,
plus git history — rather than by retention in-tree.

Result: 29,432 → 516 nodes; `outcome_coverage` unchanged at 0.202 (the
pre-registered must-not-move check); `find_chains` stopped truncating, so
H0c's "the loop cannot be run against this corpus" is now false.

### G6.3 — A fix lands as a new version of a build node — status: active

**The mechanism to test, and the reason to test it on real work.** Today an
engine fix is edited in the engine repo, and `level3.py` re-derives the build
node afterwards — the node trails the code. The target is the reverse: a fix is
applied *as a version update to the build node*, and the engine file follows
from it via `stitch.py`.

This is also how the grid's version dimension gets exercised for the first time
on content that matters. `refs/grid/node/<id>` already records one version per
change and the grid held 535 refs after its first full pass; what has never been
tested is a build node accumulating **meaningful** versions — v1 → v2 → v3 as a
real fix evolves — and `stitch.py` materialising a chosen version rather than
whichever is current.

Falsifier: take one real fix from this session, apply it as a build-node version
update, stitch it out, and confirm the engine file is byte-identical to what the
direct edit produced. If it is not, the version layer is not yet a source of
truth and should not be described as one.

**Payload model decided 2026-08-23 (iter-9006 → 9008), and the falsifier is now
known to be passable.** The chain is `hyp:payload-in-node` →
`exp:grid-payload-roundtrip` → `verdict:payload-in-node` (proved, conf 0.75,
evidence resolves).

- **The pick: grid-ref payload.** `payload_ref` keeps its shape; only its
  *resolution rule* changes, from "read this path off the engine tree" to "read
  this path from `refs/grid/node/<id>`'s tree". Inline body lost — three
  independent docstrings rule it out and a source file containing a fence breaks
  the node's own parser. Blob-sha lost on authoring mechanics, not storage: the
  blob must exist before the sha can be written, so the edit is never expressible
  as one node write, and a sha-to-sha diff says *that* something changed and
  nothing about *what*.
- **Proved at the mechanism level, with bytes.** Git's tree format carries
  content, exec bit and symlink-ness losslessly across real version history — 4
  files × 3 bumps, sha256-matched against a non-git baseline.
- **Blocked on S9, and this is the operative sentence:** "payload lives in the
  node's grid ref" is a proved **design**, not a proved **deployment**. Wiring
  resolution to `commit_file()` as it ships today reproduces the failing variant.
  S9 first.

This also settles that the anatomy decision was not overturned by fiat. A grid
ref is never checked out, so it is not a second copy of the tree — it is a second
*name* into the same object store. When bytes match, git's hashing makes them the
same object, which is a stronger non-drift guarantee than "never inlined" was
reaching for.

### G6.4 — Non-build work branches off a build version and returns a new one — status: horizon

The full cycle, once G6.3 holds: a non-build chain — idea → hypothesis →
experiment → verdict — **branches off a specific version of a build node**, and
its accepted verdict produces the **next version** of that build node.

That makes provenance answerable in the direction that matters: not "what
changed in this file" but *"which argument produced this line, and what was the
state of the code when that argument was made"*. It also makes a rejected
verdict cheap — the branch simply never lands a new build version, and the
attempt survives as prior art (G9.5's rejected-draft case).

Depends on G6.3 for versioning and on G9.5 for the session→version link, without
which a branch point cannot be identified after the fact.

### G6.5 — The cron rebuilds agi from agi-tree, then commits and pushes it — status: active

**The shape being committed to: `agi-tree` is the development environment,
`agi` is the shippable package.** Work happens in the graph; the engine repo is
what falls out of it. When the grid cron runs it should re-derive the census,
re-scan level 3, `stitch` the result into the engine tree, and — once that is
trustworthy — **commit and push the engine repo too**, so `agi` is always a
published build of `agi-tree` rather than a thing edited in parallel.

**Answering the question directly: today the two repos' commits are NOT the
same work, and that is the defect.** This session's engine changes were edited
directly in `agi`, and the level-3 nodes merely *describe* the result through
`payload_ref`. The graph trails the code. G6.3 reverses the arrow (a fix lands
as a build-node version), G6.4 gives it provenance (a non-build chain produces
the next version), and only then is an automatic rebuild-and-push safe — at
that point the engine commit is a *derivation*, and its message can cite the
node and verdict that caused it.

**Sequencing, and it is not negotiable:**
1. **Now — verify only.** Cron runs the generators and `stitch --verify`, and
   reports drift. It writes nothing to the engine.
2. **After G6.3** — cron may stitch and commit the engine.
3. **After G6.4** — the engine commit message carries the node → verdict →
   version chain that produced it.

A cron that writes the engine from the graph before the version layer is
trusted is a data-loss defect waiting to happen, and this project has already
paid for that class twice (H0, H0b). Report drift; never silently reconcile it.

**The generality worth preserving:** `agi` already has the tooling to run
against *any* project, including itself. Pointing it at itself is what makes
this loop closed; pointing it at fantasia is what makes it a product. Neither
should require a different engine — see **G8.2**.

Pairs with **S2** (done) and **S5** (the engine repo has no sync at all yet).

### G6.6 — Level 3 covers the non-code surfaces too — status: active

**A projection that omits half the engine cannot rebuild it.** `level3.py`'s
scope is deliberately narrow and says so in its own docstring:
`extensions/agi/src/**/*.py` plus `extensions/agi/bin/*.py`, about 70 files.
Everything else in `agi` is outside the graph entirely —

- `skills/agi/SKILL.md`, the document that tells every agent what this loop *is*
- `extensions/agi/lib/agent-prompt.md`, the kid brief itself
- `extensions/agi/driver.sh`, `lib/find-root.sh`, `hooks/cc-session-start.sh` —
  the shell surfaces, including the one that injects context into every session
- `extensions/agi-bridge/index.ts`, `schema.sql`, `README.md`, `run-loop.sh`

That was the right call for a first pass and it is now the thing blocking
**G6.1**. Stitch cannot assemble `agi` from `agi-tree` while the skill, the kid
brief and the session hook are files the graph has never seen. Worse, they are
the *highest-leverage* files in the repo: a change to `agent-prompt.md` alters
every kid in every future iteration, and today that change can be made with no
node behind it — which is exactly the open loop **G6** exists to close, in the
one place where it costs the most.

What has to exist: a level-3 node per non-code surface, carrying the same
derived contract shape as a code node — what it takes, what it promises — so
`stitch.py --verify` reports drift on a prose file the same way it does on a
module. Prose has no signature to parse, so the contract has to come from
somewhere else; deciding what a `SKILL.md` node's contract *is* is the real work
here, not the scanning.

Note the reflexive case and do not skip it: **G1.3 and G1.4 are changes to
`agent-prompt.md` and `dispatch.py`.** Under G6.1 they should originate as node
versions, which means this sub-goal is on their critical path, not parallel to
it. If they land as direct engine edits, they are two more entries in the
evidence that the arrow still points the wrong way.

~~Falsifier: run `stitch.py --verify` after editing one word of `SKILL.md`. If it
reports no drift, the surface is not covered.~~ **Retired 2026-08-23 — see below.
It was run, it fired, and passing it would not deliver what this goal is for.**

**Measured and judged 2026-08-23 (iter-9006 → 9008).** Chain:
`exp:noncode-surface-census` → `exp:prose-surface-probe` →
`verdict:noncode-coverage` (disproved as written, conf 0.85, evidence resolves).
The two halves of this goal resolve in opposite directions, so they are now
stated separately.

**The coverage diagnosis holds, and is no longer an assertion.** 74 of 316
tracked files carry level-3 nodes; against an eligible set of 189 after 127
justified exclusions, 74/189 = **39.2%**. Zero declared-scope files are missed —
the generator does exactly what it says, so the gap is a scope decision, not a
bug. All nine files named above: **9/9 uncovered**, verified. One extra find:
`extensions/agi/scripts/migrate_to_sqlite.py` is hand-written engine code that
misses the scan only because `scripts/` is not a scanned prefix — a second,
narrower scope bug.

**The remedy as originally stated does not deliver.** The old falsifier was run
for real and fired: a one-word edit to the live `SKILL.md` produced zero drift,
because `ast.parse` dies unconditionally at line 4 on an em dash, so stored and
fresh contracts are always the identical failure and the diff is always empty.
Worse than the mechanism failing is what fixing it would buy: of four candidate
prose-contract shapes, the best — **extracted claims** (directive clauses and
numbered rules, with line numbers, derived mechanically the way code's `how` is)
— *would* pass that falsifier, and would still **not** have caught the
`agent-prompt.md` / `SKILL.md` contradiction that motivates this goal. That is
two self-consistent nodes disagreeing, not one node going stale against its own
file, and `stitch.py`'s only cross-node check compares `payload_ref` strings,
never content.

**What this goal now commits to, in order:**
1. **Contract shape: extracted claims.** Decided, not left open. Same split code
   contracts use — the harness derives the claim list mechanically, a model fills
   the judgement fields.
2. **A fifth drift category: cross-node claim comparison.** None of the existing
   four compares two nodes against each other. Without it, coverage alone cannot
   deliver the reflexive-case protection this goal argues for.
3. **Reserve a model-judgement step.** "Commit your work" contradicting "do not
   commit" is a semantic negation. No mechanical diff performs it, and the
   `how`/`why` split reserves no room for it today.

**Replacement falsifier, and it is the whole point:** reintroduce the
`agent-prompt.md` / `SKILL.md` contradiction and confirm `stitch.py --verify`
flags it. Passing the old one-word test would have produced false confidence that
the reflexive case (G1.3/G1.4 editing `agent-prompt.md`) is protected when it is
not.

### G6.7 — Publish the engine as a grid ref, not a written tree — status: horizon

**The question: could a fourth grid dimension replace `stitch.py --out`?** The
grid already has three — D1 chain (`refs/heads/*`), D2 node
(`refs/grid/node/<id>`), D3 session (`refs/grid/session/...`). A D4 *release*
dimension would take each build node's payload, `mktree` it into the engine's
directory layout, `commit-tree` it, and move `refs/grid/release/agi`. The live
engine becomes a ref you can move and roll back, and `agi` is published by
pushing that ref rather than by writing 74 files and committing them.

**Answer the blocking part first, because it decides everything else: there is
no code in the graph to stitch.** A level-3 node holds `payload_ref` — a
*pointer* into the engine repo — plus a mechanically-derived contract.
`stitch.py`'s own docstring is honest about the consequence: `--out` is
"near-identity: resolve 73 pointers, copy 73 files… not a compiler". That shape
was a deliberate decision, recorded in `hyp:level3-node-anatomy` — source lives
on disk exactly once, never inlined. So D4 has nothing to pick out. **The fork
is not `stitch.py` vs. the grid; it is whether a node holds its payload or
points at it**, and that is **G6.3**, which is already the gate on G6.5.

**Once payloads are in nodes, D4 is the better publisher, for one reason worth
stating plainly: a `commit-tree` cannot partially apply.** `stitch.py --out`
writing 74 files can fail on file 35 and leave a half-written engine — the exact
class of defect this project has paid for three times (H0, H0b, H0i). Grid
commits are built with plumbing and never touch a working tree, so either the
ref moves or nothing happened. G6.5's sequencing exists precisely because a cron
that writes the engine before the version layer is trusted is a data-loss defect
waiting to happen; an atomic publisher is what makes step 2 of that sequence
safe rather than merely sequenced.

**And it is not "yet another layer".** D4 reuses the same object store, the same
plumbing helpers and the same push path D2 and D3 already use — the marginal
cost is a ref namespace and a tree-builder, not a second system. A node version
whose content is also on D1 is the same blob.

**So `stitch.py` is not retired — it is re-scoped, exactly as proposed:**
`--verify` stays the valuable half (an independent claim about what the tree
should contain, which `cp -r` cannot make), and `--out` becomes the *test*
materialisation — put the graph on disk, run the suite against it — while
publishing goes through the ref.

Ordering, and none of it is optional: **G6.3** (payload in the node) → this →
**G6.5** step 2 (cron may commit the engine). Building D4 before G6.3 would
produce a publisher with nothing to publish.

Falsifier: with payloads in nodes, build `refs/grid/release/agi` from the graph
and confirm the tree it names is byte-identical to what `stitch.py --out`
produces. If it is not, one of the two is lying about what the graph contains.

**Gained a hard precondition 2026-08-23 (`verdict:payload-in-node`): D4 inherits
S9's defect structurally, not incidentally.** D4's whole plan is to `mktree` each
build node's payload using the same plumbing `commit_file()` uses. Pointed at
that code as it ships, D4 would silently mis-hash every symlinked payload and
downgrade every exec-bit payload — **across the entire published engine tree, in
one commit.**

And atomicity does not save it. G6.7's selling point is "either the ref moves or
nothing happened", which is worthless when the tree being atomically published is
simply the wrong tree, moved cleanly. An atomic publisher of corrupt content is
worse than a partial writer, because the partial writer leaves evidence.

So **S9 is not a shared inconvenience, it is the same fix with two callers.**
G6.3 and G6.7 do not each need their own mode-aware rewrite; they need the one
rewrite to land before either attempts its falsifier.

### G6.8 — The payload boundary: what is allowed to be a node — status: active

**G6.6 said "cover the non-code surfaces" without saying where coverage stops.
This draws the line, so the answer is a rule rather than a judgement call each
time.**

**In — anything that exists as a file in the repo.** That is the whole test, and
it is deliberately mechanical:

- **Code.** Already in. A code node ties cleanly to thought: it can spawn a
  hypothesis about itself, an experiment against itself, or just an idea. That
  bidirectionality is what makes it worth being a node rather than a record.
- **Docs and prose, including the skill docs.** In, for exactly the same reason —
  they spawn the same children, and most of what they assert is measurable
  against the metrics already collected. `SKILL.md` and `agent-prompt.md` are the
  highest-leverage files in the engine and are the reason **G6.6** exists.
- **Philosophy and instruction prose specifically.** In, and with a direction
  attached: **it belongs in the `agi` repo, arriving there from a node in
  `agi-tree`.** Not written into the engine and described afterwards. This is
  **G6.1**'s arrow applied to the documents that steer every agent — the class of
  file where a change made without a node behind it does the most damage, as
  **S8**'s three-way contradiction demonstrates.

**Out — anything with no file behind it.** Today that means, concretely:

- **Git refs are not nodes.** A node per grid ref is tedious to no purpose:
  `refs/grid/node/<id>` is already *about* a node that exists. Making it its own
  node inverts the relationship and doubles the corpus for zero new thought.
- Sessions, run logs, and ephemeral output likewise. They are evidence a node can
  *cite*; they are not thoughts.

### The shape this implies, and it is worth stating because it is the whole model

Two dimensions, not one. **The graph is the lateral dimension** — nodes and their
edges, which can be flattened for reading or left as a 3-D structure of filaments.
**Each node then carries its own linear stack of versions** as it is updated, and
that stack is the grid. Refs are the *geometry* of that second dimension, not
content within the first. That is precisely why they do not need nodes: they are
the axis, not points on it.

**The immediate payoff, and it is concrete: the 104 demoted verdicts can be
resurrected.** They were demoted rather than deleted, so each still holds its
original body at `v1`. Under this model, bringing one back to a decisive verdict
is not an edit and not a rewrite — it is **minting a `v2` that meets the current
standard**, with `v1` preserved as what was actually claimed at the time. The
overclaim stays visible as history; the honest version is what the graph serves.
That is the version dimension doing real work on real content for the first time,
which is exactly what **G6.3** says has never been tested.

**Scope note, so this does not read as permanent:** this boundary is *today's*
line and it is drawn at the filesystem for tractability, not principle. **G10**
holds the horizon where git refs, sessions and history all become addressable
regions of the same hypergraph. When that lands, this goal narrows rather than
being contradicted — the rule becomes "everything is in, materialised on demand"
and the filesystem test retires.

Falsifier: name any file in the engine repo and get a yes/no from this rule
without argument. If a case needs a human to adjudicate, the boundary is not yet
a boundary.

## G7 — Nothing the loop produces is ever silently lost — status: active

The graph is what makes it safe to stop mid-sprint, which only holds if stopping
cannot lose work and no artefact can quietly disappear or quietly lie.

**Invariants:**
- **Node count never drops** across a snapshot.
- The engine is never vendored into a project. It arrives as a gitignored clone
  that can be pulled; a committed copy diverges forever.
- No project-local `bin/*.py` shadowing an engine script. Treat any that exists
  as stale until proven otherwise.
- A partial answer is never served as a complete one.

Paid for in full: stale project-local `snapshot-build-site.py` silently wiped
29,264 files (**H0**); a second stale override broke the render path (**H0b**);
`find_chains` did not terminate on this corpus (**H0c**); a truncated
`find_chains` result was cached and re-served silently forever (**H0e**).
Banked on the other side: the git grid — per-node and per-session refs, cron
sync at a ≤5-minute crash window, rejected drafts survive (**H10**).

Owns: **L9**'s unpinned-clone gap (record the expected engine commit in config;
warn, never fail, on drift — it closes the whole staleness class), **H1**/**H2**
(state into the DB), **L16** (close the config-name compatibility window only
once pinning exists — it is load-bearing until then).

### G7.1 — Referential integrity on every parent reference — status: active

L15 validates `goal:`-prefixed parents only. Everything else dangles silently,
and on this corpus 60.3% of parent references did — a `hypothesis:` vs `hyp:`
prefix mismatch that quietly disconnected most of the `spawns` graph the
attractiveness ranking is computed over. Nothing warned, and the ranking was
read as authoritative for months.

Extend the existing check to all parent references: warn by default, `--strict`
to fail. The mechanism exists; only its scope is wrong. Owns TODO **H4d**.

### G7.2 — Duplicate node ids silently hide files on disk — status: active

Found 2026-08-22 by the G9.1 dashboard on its first run, which is the argument
for G9 in miniature: **17 node ids are declared by two files each.** The loader
keeps one and drops the other, so 17 files sit on disk fully invisible to every
tool that reads this graph — the renderer, the metrics, the chain finder, and
the dashboard itself.

The dropped file is frequently the *larger* one: `app-purpose:graph-core` keeps
a 276-byte file and hides a 575-byte one; `bigger-outcome:graph-core-r1` keeps
315 bytes and hides 1,217. This is not a cosmetic duplicate — it is content
loss that has already happened and that nothing reported.

Fix: id uniqueness must be checked at load and at write. A second file claiming
a live id is an error, not a silent preference for whichever sorts first.
**Do not resolve the existing 17 by deleting either side** — merge or re-id
them deliberately, the G7 rule.

### G7.3 — `evidence_runs` as a bare integer is still unverifiable — status: horizon

Residual left open by G3.1 and named here so it is not forgotten. After the
H4c fix a list entry must resolve to a real node, but an integer
(`evidence_runs: 3`) is still accepted as direct attestation and counts 3.
Writing an integer is exactly as cheap as writing the `synthetic` sentinel was.

Not closed immediately on purpose: many honest nodes legitimately record a
count rather than ids, and forcing ids everywhere would break the honest path
in order to close a hole nobody has yet exploited. Decide deliberately — the
H4c lesson is that any unverifiable field eventually gets gamed, so the
question is when, not whether.

### G7.4 — Two loaders, two opposite duplicate-id policies — status: active

`graph_core/loader.py::load_directory` keeps the **first**-sorted file on an id
collision and, as of 2026-08-22, reports every collision via
`graph.duplicate_ids`, a `WARN:` line, and `DuplicateIdError` under `strict`.
`snapshot-goals.py::load_existing_nodes` keeps the **last**-sorted file, by
plain dict overwrite, and reports nothing.

**Not cosmetic — it silently narrows the integrity check that was just built.**
`collect_parent_refs` and the whole G7.1 check read off `load_existing_nodes`,
so when a duplicate pair disagrees on `parents:`, the losing file's references
are invisible and its dangling refs are never reported. Measured on this
corpus: an independent raw scan finds **89** dangling parent references;
`snapshot-goals.py` finds **88**. The missing one is
`nodes/task/t-090-bfsdfs-traversal-primitives.md → hyp:graph-core-r11`, whose
id `task:t-090` is shared with `t-090-schema-as-file-with.md` — one of G7.2's
17 pairs, where the wrong sibling wins.

Fix: one duplicate-id policy, in one place, reported the same way by both
readers. First-wins plus a warning is the established behaviour; make
`load_existing_nodes` conform rather than inventing a third rule. The 88-vs-89
gap is the regression test.

### G7.5 — Parse failures are swallowed with zero signal — status: active

`load_directory`'s `except Exception: continue` and `load_existing_nodes`'s
`except Exception: pass` both silently drop any file that raises while its
frontmatter is parsed. **No caller learns anything.**

On the live corpus this hides exactly one file:
`nodes/hypothesis/a00-1467544f-chain-600hop.md`, whose frontmatter carries a
stray `- "exp:a00-1467544f-chain-600hop"` list line between `id:` and
`parents:`, breaking YAML block-mapping parsing. That file is invisible to the
renderer, the metrics, the chain finder and the dashboard alike — the same
failure mode as G7.1 and G7.2, reached through a hard parse error instead of a
bad reference or an id collision.

Fix: both sites warn with the file path and the exception, following the
warn-by-default / strict-to-fail pattern G7.1 and G7.2 already established.
**Do not repair the malformed node.** Fixing the corpus is a separate,
deliberate decision — the G7.2 rule. This goal is about making the failure
visible, not about making it go away.

### G7.6 — One persistence model: frontmatter, JSON, or a database — status: horizon

Three representations exist and none is authoritative. Markdown frontmatter is
what the loop actually reads and writes. A JSON/SQLite backend exists
(`graph_core/persistence/sqlite_backend.py`, `db_loader.py`, plus a one-shot
migration script) and is wired into the snapshot scripts behind a config key —
but agi-tree's own `persistence` block was removed this session because the
project's vendored `graph_core` predates the backend entirely.

The question to settle deliberately: **unify on one, support both honestly, or
migrate to a real database.** The case for a database is not tidiness — it is
that several defects this session are *schema problems wearing filesystem
clothes*: duplicate ids (G7.2, G7.4) cannot happen under a primary key; dangling
references (G7.1) are a foreign-key constraint; unresolvable `evidence_runs`
(G3.1) is a join. A store that can express those constraints removes whole
classes of bug rather than detecting them after the fact.

The case against is equally real: frontmatter is human-editable, greppable,
diffable, and it is what makes the git grid work at all — a node's version
history is a file's history. A database gives that up unless the grid is
rebuilt on top of it.

Absorbs **H1** (DB-only state migration, long carried as P0) and **H2** (import
the historical corpus). Decide before building either: H1 has sat at P0 without
the decision being made, which is why it never moved.

### G7.7 — Retire the vendored engine copy and the last loader path bug — status: horizon

Two carried defects with one root: `agi-tree/src/` holds project-local copies of
`graph_core`, `chain_engine`, `renderers`, `schema_registry`, `embeddings` and
`environment_indexers`, and the documented override convention gives them
precedence over the engine's own. The project therefore runs on a stale copy
that predates `sqlite_backend.py` — which is how a snapshot came to crash
mid-corpus this session (H0g).

This is H0/H0b's defect class arriving through the `src/` door, and L9 states
the rule it breaks: **the engine must never be vendored.** Retire the directory
deliberately — the historical `exp-*.py` scripts import from it, so verify
before deleting. Absorbs **H0h** and **H5** (the R11 loader path-safety bug,
which lives in the same code).

## G8 — Forkability: anyone grows their own tree — status: horizon

A project repo holds data and configuration; the engine arrives as a clone.
`fantasia` is the reference implementation and proves the layout composes.

The interesting case is **recursive**: a tree per task domain, where a tree
spawns child trees for personas it finds useful, and individual skills, plugins
and MCP servers can each own one. The payoff that justifies the recursion is
**AI experts that compound** — agents that get sharper the longer they are
exposed to a workflow.

Owns: **L9** (scaffolding a project without copying by hand — shares its writer
with G1/L17). L10 moved to **G9**, which is where legibility now lives.

### G8.1 — Decide the distribution shape: drop-in clone, skill package, or install — status: active

**The engine currently arrives by being cloned into a project and gitignored.**
That was chosen to prevent vendoring (H0/H0b: a committed copy diverges
forever, and a stale one destroyed 29,264 files). It works, but it means every
project carries a full checkout it must remember to pull, and L9 already found
the gap: **the clone is unpinned and silently stale** — nothing declares which
engine version a project expects and nothing warns on drift.

Three candidate shapes, and the question is which one the engine should *be*:

1. **Drop-in clone (today).** Simple, pullable, no packaging step. Costs a
   checkout per project and has no version pinning.
2. **Skill package(s).** Most of the engine is Python scripts invoked by a
   skill; as features get more advanced the question is whether the `.py` files
   belong *inside* skill packages rather than beside them. This would make the
   engine installable the way every other skill is, and would fold naturally
   into **G1.2** (folding caveman/cavekit/gitnexus into one skill). Open
   question: whether a skill package is a sane home for ~15 entry points, a
   `src/` tree and a test suite, or whether that is stretching the format past
   what it is for.
3. **A real install** (`pip`/`uv` tool, pinned version). Clean dependency and
   version story; adds a release step and a packaging surface the project does
   not have today.

**Not a cosmetic choice — it decides who owns the engine's history.** Cloning
into a work repo keeps the engine out of the project's history and lets the
project maintain its own node set independently, which is the property that
makes forkability work at all. Any shape chosen must preserve that separation.

Pull L9's pinning gap in here regardless of the outcome: record the expected
engine commit in `agi-tree.config.json` and warn (never fail) on drift. That
closes the whole staleness class H0/H0b belong to, and it is cheap under any of
the three shapes.

**Related and load-bearing: S1.** Retiring `bin/` is partly a packaging
question — a directory of scripts named `bin/` is exactly what a package
layout would have to rename anyway, and it is currently costing GitNexus
coverage of all fifteen entry points.

### G8.2 — One engine, any project, including itself — status: active

**The engine must never need to know which project it is running.** It already
mostly holds: `driver.sh` walks up for a config file, the goal and build-site
snapshots are project-agnostic, and the same binary ran against fantasia (a
game) and agi-tree (an engine graph) this session without modification.

What is newly true and worth protecting: **agi can be pointed at itself.** The
census, the level-3 scan and `stitch` all ran against the engine's own source
this session, which is what makes G6 a closed loop rather than a slogan. That
self-application must stay a *normal use of the general tool*, never a special
mode — the moment there is an `if project == "agi-tree"` branch anywhere, the
generality that makes G8 possible is gone.

Falsifier, and it is cheap to run: a third project — neither fantasia nor
agi-tree — should reach a rendered map and a first chain with no engine change
at all. L18 already proved the goals-only stage works on a bare project; this
extends it through a full iteration.

## G9 — Legibility: a human can see what the loop is doing — status: active

**Stated plainly by the owner, and it is the sharpest usability signal this
project has had:** *"You keep referencing these items and I have no idea what
you are talking about."* Every artefact this system produces today is addressed
to an agent. `INJECTION.md` is generated for a spawn prompt. `GOALS.md` and
`TODO.md` are dense on purpose. The ASCII map is capped at 200 lines and
truncates silently. There is no view built for a person.

That is not a documentation gap, it is a **product gap**, and it gates every
other goal: a system whose state only agents can read cannot be evaluated,
corrected, or handed to anyone else. G8 (forkability) is unreachable without it.

**Invariant:** the dashboard is a *reader*, never a writer. It must be safe to
run at any moment, mid-iteration, with zero possibility of touching the corpus.

**Design constraint that shapes the whole thing:** it renders the graph
*truthfully*, including its damage. Truncation, dangling references,
unevidenced verdicts and deprecated mass are the things a human most needs to
see — a dashboard that shows a clean graph over a broken one is worse than none.

### G9.1 — CLI dashboard, runnable as a Claude Code side terminal — status: active

First deliverable, and deliberately the humble one. A terminal view that
answers, without the reader knowing any of this system's vocabulary:

- what goals exist, their status, and what is actually being worked
- which chains are real and which are stubs
- where every metric currently stands, **with its known contamination named**
- what the loop did last iteration, and what it would pick next

Runs in a repeating-refresh mode so it can sit in a split terminal beside a
Claude Code session. No install step beyond the engine itself.

### G9.2 — The same view in a browser — status: horizon

The CLI view earns the data model; the web version earns the audience. Not
started until G9.1 has been used enough to know which panels matter.

### G9.3 — Ride along as a kid — status: horizon

Load the exact context injection a kid receives on arrival. The fastest way to
judge whether a brief is genuinely self-contained, and the only way to see the
system from the inside without spending an agent. Was L10's first half.

### G9.4 — The live graph viewport: watch the whole thing, moving — status: active

**This supersedes the dashboard as the primary view.** G9.1 answers "what is the
state" in panels of text. This answers "what does the graph *look* like, right
now, while agents are working in it" — and that is a different instrument.

What it is:
- **The whole node graph rendered as a navigable web**, at level 3 by default —
  not a 200-line truncated snapshot, the actual graph.
- **A terminal viewport that pans** up/down and left/right across a graph far
  larger than the screen. The screen is a window onto the graph, not a summary
  of it.
- **Agents appear as spiders on the web**, positioned where they are actually
  working — kids, parents and the director each distinguishable, moving as they
  move. The point is to *watch the swarm*, not read a log of it.
- **Zoom is the same axis as everywhere else** (`--level 1..5`). Zooming out
  aggregates the web; agents take appropriate positions at each grain, so a
  parent working across a whole goal reads as one spider at level 1 and resolves
  into its kids at level 3. Levels 1–3 are enough to start; 4–5 follow the axis.

Progression, deliberately: **ASCII first, then a rudimentary ASCII web, then a
3D-looking ASCII web in the wireframe style of the original *Elite*, then the
browser version (G9.2).** Each stage has to be usable on its own — the terminal
version is the one that runs beside a Claude Code session, and it is not a
throwaway prototype for the web one.

Absorbs **A2** (ASCII renderer unification): there are currently several ASCII
renderers with overlapping jobs, and this needs one that can render a viewport
rather than a whole-graph dump. Do the unification as part of this, not before
it — the viewport requirement is what tells you what the unified renderer needs
to do.

Inherits G9's invariants: reader-never-writer, and it renders damage rather than
hiding it — a broken region of the graph should be visibly broken on the web.

### G9.5 — Pick a node, see its history; pick a version, see how it got there — status: active

The viewport is only half of it. From any node on the web:
- **select the node → its version history**, straight off the git grid
  (`refs/grid/node/<id>`), which already records one version per change;
- **select a version → what produced it** — for a non-build node, the chat and
  reasoning that wrote it; for a build node, the code at that version and the
  chain that led to it.

The data mostly exists already and is unused: the grid holds per-node and
per-session refs, `grid.py log|diff|versions` can read them, and session drafts
are versioned under `refs/grid/session/*` — including drafts that were rejected.
**Rejected drafts are the interesting ones**, because they are the only record
of what the loop considered and declined.

Gap to close: nothing currently links a node version back to the *session* that
produced it. That link is what turns the grid from storage into history.

---

## G10 — The hypergraph: an environment, not a document — status: horizon

**The end state this whole system is walking toward.** Not "a graph the agent can
query" — a *place the agent is in*. There are no blocks of prose anywhere in the
working context; everything an agent sees is graph, rendered. The agent receives
an injection of the hypergraph at the resolution its director chose, moves through
it, and asks for more of it. Every other goal here is a component of this one.

**The reason, and it is the load-bearing claim of the project:** memories are weak
things. A memory is a lossy re-encoding made after the fact, and every layer of
memory machinery bolted onto an LLM harness is an attempt to compensate for having
thrown the original away. The graph does not remember — **it keeps the original
thought verbatim, as it occurred, and lets a later agent connect to it directly.**
That is why this system has no memory layer and should never grow one. Nothing
here needs to *recall*; it needs to *reach*.

### The two axes are orthogonal, and conflating them is the current defect

- **Zoom** — which region of the graph, and at what structural grain. Already
  numeric 1–5 (**G2**). This is *where you are*.
- **Level of detail (LOD)** — how much of each node is printed at that grain. Does
  not exist yet. This is *how hard you are looking*.

Today they are fused: a node's grain is baked into its type (`level3:`) and there
is one rendering per node. The target is that any node at any zoom can be pulled
to full LOD — its complete contents, expanded — while its neighbours stay compact.
Pick a node or a small set, raise their LOD, read; pick another set, push it a zoom
level in or out. **Like slides you click through, with one-word commands, orienting
in seconds rather than in tool calls** (see **G1.6**).

The rendered artefact is a long tapestry of expanded ASCII nodes, sized so the
whole selection lands cleanly in token space. Compaction is an LOD setting, not a
separate renderer.

### Zoom must not name itself

**A node must not be titled `level3`.** The zoom level is a property of the *view*,
never of the node. The environment injection says "you are at zoom 3"; the nodes
say what they are.

The reasoning is specific and it is the sharpest thing in this goal: zoom exists,
for a human, to produce **tunnel vision** — block out everything but the relevant.
An LLM has no tunnel vision. It only has peripheral vision; it sees the whole
context at once. So for an agent, zooming is **not** occlusion — it is a slight
reduction in dimensionality. Designing the zoom axis as though the agent needs
blinders imports a constraint from the wrong nervous system. Naming the level on
the node is that mistake made concrete: it tells the agent to identify with a
grain instead of simply working at one.

Consequence for **G2.1**/**G6.6**: `level3:` as an id prefix is a migration
artefact, and the type should become a *facet* the renderer reads, not a name the
node wears. Do not rename anything yet — ids are permanent (that rule holds) — but
stop minting the grain into new ids.

### Eventually: everything loads in

**G6.8** draws today's payload boundary at the filesystem, and git refs sit outside
it on purpose. That is the *current* line, not the final one. The horizon is that
git refs, sessions, and run history all become addressable regions of the same
hypergraph, materialised on demand as an agent asks for more touch of its
environment — not pre-loaded, not a second system, just further out in the same
space. **The supermap convention (G1.3) is the addressing scheme that makes this
possible**, which is why G1.3 is worth building before the thing it will address
exists.

Falsifier, and it has to be behavioural rather than aesthetic: give an agent a task
that today requires leaving the graph, and measure the graph-call to file-read
ratio (the Design Ethic's measurable). The hypergraph is real when that ratio
inverts on work that currently fails it — the standing baseline is 3:28 from
`exp:evidence-gate-coverage`. If agents still reach for the filesystem, the
environment is a document with better formatting.

Depends on: **G2** (zoom axis), **G1.3** (addressing), **G9.4** (the viewport is
the same query with a human front-end), **G6.8** (what is in it at all).

## S1 — Retire `bin/` as a directory name — status: active

**Every engine entry point is a script, not a binary.** `extensions/agi/bin/`
holds fifteen `.py` files with shebangs, plus `driver.sh` alongside in the
parent. Nothing in it is compiled and nothing in it is a binary.

The name has a measured cost: **GitNexus excludes any directory called `bin/`
by default**, so it indexes zero symbols for all fifteen — verified after a
fresh reindex, against a working control probe on `src/`. That is the half of
the engine where every 2026-08 change landed, and it is why the engine census
had to be seeded from `git ls-files` instead of the code index.

Rename to something that describes what is there — `cmd/`, `tools/`, `scripts/`
— and take the opportunity to reconsider the layout as a whole rather than
doing a one-word rename. Fifteen flat scripts with three separate generators
among them (`snapshot-goals`, `snapshot-build-site`, `decompose-engine`,
`level3`) have a structure worth making explicit.

**Not a cheap change.** `driver.sh`, `dispatch.py`, the hooks, the skill, the
tests and every one of the 27 census nodes reference these paths; `zoom.py`'s
`--level` aliases are invoked by `dispatch.py` by path. Do it as a deliberate
pass with the census re-run afterwards, and confirm GitNexus actually picks the
directory up before committing to the churn — the exclusion is inferred from
behaviour, not from a documented setting.

## S2 — Cron parity with fantasia — status: complete

`grid.py cron install` sets both cadences — a 5-minute grid snapshot + push
(crash window ≤ 5 minutes) and an hourly main-branch push. fantasia has this;
**agi-tree does not**, and the grid was only initialised in this project on
2026-08-22.

Until it is installed, every guarantee that rests on "sync is automated, nobody
syncs by hand" is false here, and the grid's 535 refs exist only on this
machine. Install it, verify both entries land, and confirm a push actually
reaches the remote rather than assuming the cron line is correct — a cd-less
cron line is exactly the class of small operational error the design ethic says
the system should absorb.

**Done 2026-08-22.** Both cadences installed and verified, targeting `master`
(fantasia's line pushes `main`; the engine's installer got the branch right
rather than copying it). First push completed: 84 commits and 641 grid refs are
now on the remote, where before this the entire session existed on one disk.

**Found while installing it, and it is the more useful half:** agi-tree's
working branch was `iter24-extend-300hop`, a leftover from the 2026-05 padding
run, and every commit this session landed there rather than on `master`. The
branch was 84 ahead / 0 behind, so `master` fast-forwarded cleanly with nothing
lost — but a cron installed before checking would have pushed `master` and
silently published nothing at all, for as long as nobody looked.

Precondition for **G6.5** (automatic rebuild on the grid's cadence).

## S3 — A truncated contract value can contain a fence lookalike — status: active

`level3.py`'s `_cap()` truncates derived text to 240 characters. In
`nodes/level3/bin-heal.md` the `healer_ctx` input's `how` field is the truncated
source of a `write_text(f"""...```json ...```...""")` call, so the truncated
value contains a literal ` ```json ` sequence **inside** the YAML scalar.

The file is valid YAML today — `yaml.safe_dump` escapes it correctly. The trap
is on the reading side: any consumer that locates the contract's closing fence
by scanning for the first ` ``` ` after ` ```yaml ` stops at the embedded one and
gets a truncated, broken parse. This was hit for real while writing
`stitch.py`, and fixed there by bounding extraction on the
`LEVEL3-CONTRACT:BEGIN/END` markers and taking the **last** fence in that span;
there is a regression test reproducing the exact `bin-heal.md` shape.

Fix it at the source, cheaply: either neutralise fence-lookalike sequences in
`_cap()`'s output, or document the bounded-extraction requirement in a comment
beside `_cap()` and the marker constants. **The next consumer is the G2.2 model
pass** that fills `why`/`perf`/`security`, so this should land before that runs.
Must not regress the 20 existing level3 tests.

## S4 — Retire the legacy directories and repos — status: horizon

Housekeeping carried from TODO **C1–C6**, gated on bug-sweep clearance and
grouped here because none of it is worth its own long-term goal:

- `~/autoresearch-tree/` local directory (C1) and the
  `CodexOperator/autoresearch-tree` repo (C2) — archive rather than delete.
- The old pi fallback under `~/.pi/agent/git/.../extensions/autoresearch-tree/`
  (C3), pending verification that nothing resolves through it.
- The modularNN spike worktree (C4) and legacy `~/.hermes/agi/` artifacts (C5).
- `.claude/skills/gitnexus/*/SKILL.md` accidentally tracked (C6).

Do these last. Every one is a deletion, and the two data-loss defects this
project has already paid for both arrived as routine cleanup.

## S5 — The engine repo has no sync at all — status: active

`agi-tree` got both grid cadences on 2026-08-22 (**S2**). **`agi` got nothing** —
no cron, and as of that date 11 unpushed commits on `master` carrying every
engine fix this session produced.

**The consequence is worse than "not backed up", and it is specific:**
`agi-tree` is now published, and its 74 level-3 nodes carry `payload_ref`
values pointing at engine files at commits that exist only on one disk. A fresh
clone of `agi-tree` gets a graph that describes code it cannot fetch —
`stitch.py` would report every payload missing. The graph and its subject are
published at different times, which is a new way for the two to disagree.

Immediate fix, one line:

```
git -C /home/ubuntu/work/agi push origin master
```

Then decide the standing arrangement, which is **not** simply "install the same
cron". The engine repo's sync should eventually be a *consequence* of the
rebuild in **G6.5**, not an independent schedule racing it — two crons pushing
two repos on separate cadences is exactly how the graph and the engine drift
apart at the moment either one is slow. Until G6.3 makes the rebuild
trustworthy, a plain hourly push of `agi` is the honest interim.

Check the same thing that made S2 worth doing: **verify which branch is
actually checked out before trusting any push.** agi-tree's work had
accumulated on a stale `iter24-extend-300hop` branch, and a cron pushing
`master` would have published nothing, silently, indefinitely.

## S6 — Strip agi-tree to the graph and its inputs — status: complete

Done 2026-08-23. `agi-tree` had accumulated a second copy of most of `agi`:
~95 one-off `exp-*.py` / `extend-*.py` scripts at the root, a vendored engine
tree (`src/`, `tests/`, `engines/` — the copy **G7.7** wanted retired), the
cavekit-era runner, both `.STALE-DO-NOT-USE` snapshot scripts, a duplicate
`skill/autoresearch-tree/` under the pre-rename name, and 768 tracked session
transcripts. 1,026 files, −281k lines; git history is the archive.

**The rule that replaces it, now in `CLAUDE.md` as a table:** this repo holds
`nodes/`, the inputs the nodes are derived from (`GOALS.md`, `context/kits/`,
`context/plans/build-site.md`, `context/schemas/`), and `agi-tree.config.json`.
A `.py` file added here belongs in the engine.

The engine arrives as a gitignored clone at `agi/`, the way `fantasia` takes it,
so `driver.sh --smoke` runs from this repo with no install step. That is an
interim shape and **G8.1** still owns the real answer — it is a second working
copy of a repo that also lives at `~/work/agi`, and G6.5 wants exactly one
stitch target. Recorded here so the interim is not mistaken for the decision.

The duplicate skill was deleted rather than re-pointed: `~/.claude/skills/agi`
already symlinks to `agi/skills/agi`. One skill, one source — **G1.2**'s first
concrete step, taken by subtraction.

Two things this surfaced that were not housekeeping:

- **`agi` was 11 commits ahead of `origin`** — exactly **S5**'s defect, caught
  because a fresh clone would have pulled an engine 11 commits stale. Pushed
  before cloning. S5's standing arrangement is still open.
- **`context/kits/` and `context/plans/build-site.md` are generators, not
  stale output.** They mint 159 of 661 nodes, and `snapshot-build-site.py`
  unlinks every `origin: build-site` node it does not re-derive on a run — so
  deleting them prunes a quarter of the graph silently, at loop time rather than
  at delete time. Kept, and the hazard is written into `CLAUDE.md`. This is the
  **H0i** class a third time, and the third time it was found by reading the
  script rather than by losing the data.

Verified: `driver.sh --smoke --max-iters 1` completes and `nodes/` is
byte-identical afterwards.

**Left standing on purpose:** `nodes.db` (7.8 MB, gitignored — **G7.6** owns the
persistence question, and deleting it while two loaders disagree is not
cleanup), and the `.claude/worktrees/` worktree still registered against a
`~/.hermes/agi-tree/` path (**S4** C5, which is gated and explicitly last).

## S7 — `snapshot-goals.py` needs two passes to wire a new sub-goal — status: active

Found 2026-08-23 while adding G1.3–G1.5, G6.6 and G6.7. Adding a sub-goal and
running the script once mints the child node with a correct `parents:` list, but
the **parent's `seeds:` list does not contain it**. A second run adds it.
Reproduced twice: pass 1 wrote `goal:g1.5` and left `goal:g1` unchanged; pass 2
added `- goal:g1.5` to `goal:g1`.

Cause is ordering — the parent's frontmatter is composed before the children of
that pass exist, so each run wires the sub-goals it knew about at entry.

**Why it is worth a row rather than a shrug.** The edge exists in one direction
only, so nothing looks broken: the child's `parents:` is right, traversal
upward works, and `--verify` has no complaint. What breaks is downward
traversal — a renderer or a kid walking `seeds:` from `goal:g1` cannot see the
newest sub-goal, which is reliably the one being worked. `driver.sh` runs the
script every iteration so a live loop self-heals on the next pass, which is
exactly what makes this easy to never notice; a fresh clone plus a single run
renders a graph whose most recent work is invisible from above.

Fix: compose parent seed lists after all nodes for the pass are known, or make
the wiring a second phase over the completed set. Assert the fixed point in a
test — run twice, second run writes nothing. Related to **G7.1** (referential
integrity on every parent reference), which checks the reference that exists;
this is the reference that silently does not.

## S8 — `zoom.py` bakes the pi-runtime completion contract into the kid context — status: active
When using the script to inject context, eventually zoom.py fires and inserts the
reference for each kid on how to mark the completion of their task. It currently
inserts a pi-runtime reference for completion, rather than being properly runtime-
agnostic.

Fix: make zoom.py or whatever upstream file be runtime aware and offer the proper
completion contract or have this be set during install.

**Corroborated 2026-08-23 by the iter-9006..9008 run, which hit it three times.**
The generated kid context ends with a `cli.py done` block, so every CC-dispatch
kid was handed a completion contract that `skills/agi/SKILL.md` explicitly
forbids for its role ("do not commit, and do not call `cli.py done`"). All six
spawn prompts had to carry an out-of-band override telling the kid to ignore its
own context file. `exp:noncode-surface-census` independently found the same
contradiction one layer up, between `agent-prompt.md` rules 5–6 and SKILL.md's
kid contract.

That makes this a three-way disagreement — `agent-prompt.md`, `zoom.py`'s emitted
block, and `SKILL.md` — about one procedure, with no file deferring to another.
Note the shape: it is the same defect **G6.6** exists to catch, and G6.6's own
verdict says the currently-prescribed remedy would not have caught it, because
all three are internally self-consistent and only disagree with each other.
Patching at dispatch time, as this run did, is the workaround, not the fix.

## S9 — `commit_file()` drops the exec bit and mis-hashes symlinks — status: active

Found 2026-08-23 by `exp:grid-payload-roundtrip`, confirmed at the cited lines.
`bin/grid.py`:

- **`:154`** — `git hash-object -w str(path.resolve())`. `Path.resolve()`
  dereferences a symlink *before* hashing, so the object committed is the
  **target file's bytes**, not the link text. Not a dropped-metadata edge case: a
  silently wrong object, no error, no warning.
- **`:160`** — the tree line is `f"100644 blob {blob}\tnode.md\n"`. Mode is
  hardcoded, so any `100755` payload comes back `100644` and any `120000` comes
  back a regular file.

**Benign today, and it will not stay that way.** Grid only ever commits regular
node `.md` files under the fixed name `node.md`, and node files are not symlinks
and not executable — so nothing is currently wrong on disk. The defect activates
the moment a *payload* goes through the same call, which is exactly what
**G6.3** picked and what **G6.7** is built on. This is the rare case where the
right time to fix a latent bug is before its first caller, because both callers'
falsifiers are byte-comparisons that it would fail.

Fix: read the mode from `os.lstat()` (100644 / 100755 / 120000) and, for a
symlink, hash the `readlink()` target text via `hash-object --stdin` rather than
the dereferenced file — which is what `git add` does internally, built from the
four primitives `grid.py` already calls. A matching mode/symlink-aware read path
is needed in whatever resolves a payload back out. Estimated ~15–20 lines, and
the experiment's mode-aware variant is a working reference implementation
(`sessions/iter-9007/kid-c/sandbox/`, which is gitignored — port it, do not
depend on it).

Test: the experiment's own table is the regression suite — a 100755 file and a
120000 symlink, three version bumps each, sha256 against a non-git baseline.

Blocks **G6.3** and **G6.7**. One fix, two callers.

## S10 — the purged gamed mass is still on disk inside agi-tree — status: active

Found 2026-08-23. **G6.2 says the 28,916 gamed `-extend<N>` nodes were "removed
from the working tree and archived outside the repo." The first half is not
true.** `.claude/worktrees/wonderful-lamport-51c9a9/` — a git worktree registered
against a `~/.hermes/agi-tree/` path — still holds **29,706 `.md` files, 29,062
of them `-extend<N>` nodes**. They are gitignored, which is why nothing has
complained, and why nothing found them for two days.

**The hazard is specific and I walked into it while writing this iteration.**
`evidence_gate.build_corpus()` takes a directory and `rglob`s it for `*.md`.
Called on `nodes/` it returns 657 ids, correct. Called on the **project root** it
returns **29,582** — the pre-purge corpus, resurrected. A verdict citing a
deleted gamed node as `evidence_runs` would resolve against it and pass the gate,
which is H4c's fix silently undone.

**The engine is not currently affected, and that was checked rather than
assumed:** all three real callers pass `root / "nodes"` — `cli.py:85`,
`metrics.py:145`, `post_wire.py:137`. The bug was in the throwaway harness that
found it. But "the correct argument is passed at all three current call sites" is
a property of today's callers, not of the function, and the incorrect call took
one line to write.

Two independent fixes, and both are cheap:
1. **Delete the worktree.** `git worktree remove` / prune. This is **S4** C5,
   which is gated and explicitly last — this entry is the evidence for promoting
   it, because "archived, not deleted" was the deviation G6.2 recorded and it did
   not fully happen.
2. **Make `build_corpus` refuse a non-`nodes/` root**, or resolve `nodes/` itself
   from the project root rather than trusting the caller. A gate that cannot
   verify must fail closed — the function already argues exactly this for a
   `None` corpus, and should hold itself to it for a wrong directory.

Do (2) regardless of (1). Deleting the worktree removes today's 29k; it does not
stop the next stale tree from being swept in.
