# HANDOFF — agi

> **One session's state, and nothing else.** Bootstrap and install live in
> `QUICKSTART.md`; what the project is committed to lives in `GOALS.md`.
>
> **This file is REPLACED wholesale by each director**, not appended to —
> exactly one session section exists at a time. Prior sessions are in the grid,
> `grid.py payload build:HANDOFF.md --version N`, and in git, so nothing is
> lost by replacing and accumulating would charge every future cold session for
> superseded state. See `CLAUDE.md` for the rule.

---

# SESSION HANDOFF — 2026-09-02: LIVE SCRATCHPAD (session in progress)

> **🔴 This section is being written DURING the session, not after it.** The
> owner asked for it as a scratchpad so a fresh session can pick the work up
> cold at any point. Treat it as current state, not as a report — the last
> iteration listed may be half-done.
>
> **If you are a fresh session: read §0, then §3 "where it stopped".**

## 0. State

```
repo        /home/ubuntu/work/agi   ONE repo: source + .agi/ graph + refs/grid/*
runtime     pi, live.  parent qwen/qwen3.8-27b  |  kid deepseek/deepseek-v4-flash
crons       FROZEN — crons_live: false. Unchanged. Do not re-enable.
PUSHED      NO — several commits ahead. Push by hand when ready.

node_count  876      active 869   deprecated 7    goals 106
outcome_coverage ~0.28  evidence_fraction ~0.21   unevidenced_decisive 1
goals: active 10  horizon 61  retired 2  complete 33
tests       1215 pass    PUSHED: yes (crons frozen; pushed by hand)
```

## 1. The session's plan, and where each item stands

| # | Work | State |
|---|---|---|
| 0 | deepseek kid model + qwen parent; G13 board, G2.2, G4.8 recorded | ✅ `bd42d8c0b` |
| 1 | **G5 built** — `complete` scores, retired does not | ✅ `cdff3b60d` |
| 2 | **The goal sweep** — 41 active → 9 | ✅ `3c8435271` |
| 3 | First deepseek kid, g4.6 falsifier 4 re-measured | ✅ `383ed2107` |
| 4a | **The parent brief** (`goal:g1.9`) — `bin/brief.py` | ✅ this commit |
| 4b | **Live parent run** — qwen parent spawning deepseek kids | ✅ PROVEN |
| 5 | `goal:s23` + `goal:s25` + `goal:s26` — all three built | ✅ complete |
| 6 | **`goal:s27` decided and built** — a parent authors nothing | ✅ complete |
| 7 | `goal:s28` fixed by a kid; `goal:s29` build-parent rule | ✅ complete |
| 8 | `goal:s30` — handoff replaced each session; `QUICKSTART.md` split out | ✅ complete |

## 2. What landed, in one line each

- **`goal:g5` is built.** `SCORING_GOAL_STATUSES = {active, horizon, complete}`,
  `RETIRED_GOAL_STATUSES = {retired, phasing-out}`. `outcome_coverage`
  0.232 → 0.284. **`phasing-out` renamed to `retired`; the old spelling stays
  accepted permanently.**
- **Retirement cannot launder the ratio.** A hypothesis under a retired goal
  that never reached an mvp **stays in the denominator**. Without this, a sweep
  raises the metric for free. `retired_open_hypotheses` makes the spared set
  visible.
- **The sweep ran and the metric did not move** — 0.284 before and after. That
  is iteration 1's falsifier, measured live rather than in a fixture.
- **`bin/brief.py`** — one assembler, tier-parameterized, taxonomy derived from
  `evidence_gate.VERDICT_HELP`. `pi_adapter` now holds no brief text at all and
  a test asserts it stays that way.

## 3. ✅ 4b LANDED — the tiering works, end to end

`driver.sh --tier parent --target goal:g4.8`. **`driver.sh` did NOT forward
`--tier`** (found by checking, not assuming — the parent tier was unreachable
from the documented entry point and silently spawned a kid). Fixed; the flag is
now a one-line pass-through.

Verified from the persisted `agent.json.command`, not from assumption:

```
parent  a00-a54f694b  tier=parent  qwen/qwen3.8-27b            parent brief; NO kid text
  └─kid a00-8d238338  tier=kid     deepseek/deepseek-v4-flash  kid brief;    NO parent leak
```

The parent spawned that kid **itself**, via `dispatch.py --tier kid --target
goal:g4.8`, reviewed its node, accepted it, and flagged two real cosmetic
defects in it. That is `goal:g4.8` falsifier clauses 1 and 2, live. **Clauses
3 and 4 remain open** — one parent, one kid, so nothing exercised the
concurrency bound or the collision surface.

🔴 **The parent found a defect nobody had anticipated, in its `struggles:`
line:** dispatch scaffolds an authored node for EVERY tier, so a parent whose
brief says "you do not write the node yourself" must author a `hypothesis` to
pass `cli.py done`. It lands in `scoring_hypothesis_count`, so **running a
parent at all lowers `outcome_coverage`.** Filed as `goal:s27`, deliberately
undecided between three candidate artefacts.

**5 — three built and `complete`, one blocked on the owner:**

- ✅ **`goal:s23`** — `metrics.deprecated_node_ids` (one definition, beside
  `node_lifecycle_stats`) plus a `_LiveOnly` **view** in `render-context.py`.
  A view, not `Graph.remove_node`, because `g` is still read whole a few lines
  later for `by_type` and `find_chains`. `build:TODO.md` is out of the map;
  7 retired nodes load and do not render.
- ✅ **`goal:s25`** — `build_corpus` raises `CorpusRootError` on a directory
  containing a `nodes/` child. Narrow on purpose: a project root is the one
  confusion that has actually happened. A missing dir still returns empty.
- ✅ **`goal:s26`** — `warn_premature_complete` in `snapshot-goals.py`, run on
  every `--render`. A **warning**, never a failure: a hard error would make
  retiring a tree bottom-up unrepresentable.
- ✅ **`goal:s27`** — decided by the owner, and the answer was not on my menu:
  **a parent is not nodeless, it is responsible for its kids' nodes**, the way
  a real parent is responsible for its children. No scaffold at
  `tier == "parent"`; `cli.py done --owns <kid-node-id> ...`;
  `completion.owns_all_complete`; review prose into the kids' `THOUGHT` blocks.
  **Named a stopgap in the brief itself** — the destination is `goal:g2.7` /
  `goal:g10.1` session linking, where a review reaches a reader through the
  node's high-LOD view instead of being compressed into prose.

## 3b. `goal:s28` — FIXED by a kid, with two review findings worth keeping

**A parent that spawns a kid erases itself from `manifest.json`.**
`dispatch.py:329` writes the manifest wholesale, and a parent shelling out to
`dispatch.py --tier kid` is a second dispatch into the same iteration dir.
Measured after one parent + one kid: `agents in manifest: ['a00-f0fd9669/kid']`.

**Consequence:** `post_wire`'s parent-admission branch (`owns_all_complete`) is
correct and **never runs**, because `post_wire` iterates `manifest["agents"]`.
The parent's `owns` is written faithfully to its `agent.json` and read by
nothing — the same four-hop marshalling failure that dropped every pi verdict,
one tier up. `heal.py` cannot monitor a parent either.

**Fixed** in `dispatch.py`: the manifest is read before the new one is built,
`started_at` preserved, agents merged by `id` (update-in-place on re-dispatch),
corrupt manifest degrades to fresh with a warning, write via
`.manifest.json.tmp` + `rename`. Verdict demoted `proved` ->
`inconclusive_lean_proved:85`: verified by reading and by simulation, never by
a live parent-plus-two-kids run — and prediction 2 (that `owns_all_complete`
now actually executes) is the whole point and was never observed. **That live
run is the cheapest open item in the repo.**

🔴 **Two findings from the review, both mine rather than the kid's:**

1. **The kid broke a test and did not notice** — it ran its own scratch test,
   never `pytest extensions/agi/tests/`. The kid brief now requires the suite.
2. **The kid ran `git add -A` and committed 37 lines of a `CLAUDE.md` section
   the director had mid-edit** (`b8cb2ec05`). `SKILL.md` forbids kids
   committing, the parent brief forbids it, and `brief.py::_kid` did not say
   it — `goal:g1.9`'s argument arriving as a live incident four iterations
   after I built the assembler and left the prohibition out. Fixed, with tests.

## 3d. `goal:s30` — this file is replaced; standing content moved out

`QUICKSTART.md` now holds the bootstrap (safety rail, clone/deps/install, the
one-iteration diagram, glossary). It had to move: **replacement-by-default
turns any standing instruction left here into one with a deletion date.**
`README.md` and `SKILL.md` repointed.

`build:QUICKSTART.md` was created through `node_writer.write_node` with
`parents: [build:HANDOFF.md, goal:s30]` — the first node minted under
`goal:s29`, and the gate approved it on `parent_shapes=[build, goal]`.

## 3c. `goal:s29` — where a build node may come from

`parents: [mvp]` for a new file, `parents: [build, goal]` for a new version,
nothing else. **A goal alone never mints a build node.** Needed a new gate
primitive: `spawn.parent_shapes`, an OR across whole shapes, because
`allowed_parents` is a flat set and widening it to cover both shapes
necessarily permits their mixtures — including the lone goal being forbidden.
All six shapes asserted. **216 existing build nodes grandfathered**: the gate
is creation-time only and `level3.py` never calls it. **Residual: the level3
rescan was reasoned from grep, not run.**

**Three of those four are the same shape**, and it is worth naming: lifecycle
and scaffolding bookkeeping keeps leaking into the primary metric. `goal:g5`
(finished goals stopped scoring), `goal:s26` (premature `complete` scores), and
`goal:s27` (parent reports score as unconverted hypotheses) are one pattern
seen three times in one session.

## 4. 🔴 Traps from this session

- **A test can re-implement the thing it tests and pass 11/11.** The deepseek
  kid's `B2` was a hand-copy of `post_wire.py:319` rather than a call to it;
  delete that line and its test still passed. **Read the kid's artifact, not
  its report.** Found only because three line numbers in the report disagreed
  with the tree — small factual slips are signal.
- **A spec can contradict its own falsifier and nothing notices** while no data
  has the shape that would tell them apart. `goal:g5`'s sub-case 2 and its
  falsifier said opposite things about the same nodes for a day, and the
  reading that "looked right" would have armed a metric exploit in the very
  next iteration.
- **Retiring a goal can silently delete a live defect.** `goal:s10` carried two
  fixes; only one was moot. Its own closing line warned against exactly that.
  **Before retiring, check whether the goal carries anything still true.**
- **A proposed new state may already exist.** `legacy` was going to be minted;
  `deprecated` already means it and the renderer simply ignores it. Two
  definitions of one fact is `goal:s17` / `goal:g2.5` / `goal:g7.4` again.
- **`grid.py commit --all` says `N error(s) (missing mint_id)`** for
  hand-written nodes. It has read 0 all session. Read that line.
- **A flag the dispatcher accepts is not a flag the driver forwards.**
  `--tier` existed in `dispatch.py` since `goal:g4.6` and `driver.sh` dropped
  it silently, so `--tier parent` spawned a kid on the kid model. Check
  pass-through before trusting an entry point.
- **Read `struggles:` — twice this session it beat the review it came with.**
  The parent's line found `goal:s27`; the kid's line quality is why its
  overclaim in iter 3 got caught.

## 5. Known-good verification sequence

```bash
cd /home/ubuntu/work/agi
bash extensions/agi/driver.sh --smoke --max-iters 1              # count must not drop
python3 -m pytest extensions/agi/tests/ -q                       # 1189 pass
python3 extensions/agi/bin/snapshot-goals.py --render --check    # byte-identical, exit 0
python3 extensions/agi/bin/grid.py commit --all                  # 0 error(s)
python3 extensions/agi/bin/crons.py show                         # crons_live: False
```

---
