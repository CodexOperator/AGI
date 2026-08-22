# GOALS.md — agi-tree long-term goals

`agi-tree` is the thoughtgraph that builds `agi`; `agi` is the code that operates
on thoughtgraphs. These goals are the **engine's own design contract** — the
durable commitments engine work serves. They are not a task list: concrete
defects and work items live in `agi/TODO.md`, and each goal below names the
entries it owns so the two never restate each other (`TODO.md` L19 action 4).

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
project). Queued rather than active: the handles are named but untouched.

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

### G2.2 — IO maps as inherited contract slices — status: horizon

Every node declares required inputs and promised outputs, each with a how/why,
a performance note and a security note; the maps re-derive when neighbours
change. Blocked on G2.1 — an IO map needs a code-level node to hang off.

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
