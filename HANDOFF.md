# HANDOFF — agi, for a fresh session on a new machine

> Self-contained bootstrap. Assumes **nothing** exists locally: no clone, no deps,
> no CLI, no auth. Everything that is *not* bootstrap has been removed from this
> file — the graph says it, and saying it twice is how the two copies drift.
> Trimmed 2026-08-27 (was 397 lines of mostly-2026-08-18 state).

**Where the knowledge actually lives, so this file does not restate it:**

| Question | Read |
|---|---|
| What is agi, and why is it shaped this way? | `skills/agi/SKILL.md` |
| What is committed to, and what is being worked on now? | `GOALS.md` (rendered from `nodes/goal/`) |
| What does the repo contain, and how do I run the loop? | `<tree>/CLAUDE.md` |
| What does any given engine file do? | its build node — `nodes/build/*.md`, one per file |
| What happened in the last session, and what is next? | the **SESSION HANDOFF** section at the bottom of this file |

---

## 1. 🔴 READ THIS BEFORE RUNNING THE LOOP IN ANY PROJECT

**This is a live, unfixed defect — not history.** `driver.sh` still prefers a
*project-local* script over the engine's own:

```
driver.sh:91   [[ -x "$PROJECT_ROOT/bin/snapshot-build-site.py" ]] && SNAPSHOT_PY=...
driver.sh:99   [[ -x "$PROJECT_ROOT/bin/render-context.py"      ]] && RENDER_PY=...
```

Some projects ship a **stale** `snapshot-build-site.py` beginning with
`shutil.rmtree(NODES_DIR)`. Running the loop there deletes the entire node
corpus. **Exit code 0, no warning, nothing printed.** Confirmed blast: one
project went from 29,422 node files to 158 in a single `--smoke` run.

The engine's own script is safe — incremental upsert, and it prunes only nodes
carrying `origin: build-site`.

**Audit before the first run in any project:**

```bash
ls <project>/bin/*.py 2>/dev/null && grep -n "rmtree" <project>/bin/*.py
```

Anything that prints, rename it so the engine's version wins:

```bash
mv <project>/bin/snapshot-build-site.py <project>/bin/snapshot-build-site.py.STALE-DO-NOT-USE
```

**General rule: treat any project-local `bin/*.py` as stale until proven
otherwise.** The override mechanism is itself the defect; making it opt-in is
still open. `agi-tree` deleted its `bin/` entirely for this reason (goal S1).

---

## 2. Bootstrap on a new machine

### 2a. Clone

`CodexOperator/agi` is **private**, default branch `master`. Authenticate with
`gh auth login` or an SSH key, then:

```bash
git clone git@github.com:CodexOperator/agi.git ~/work/agi
```

### 2b. Dependencies

```bash
python3 -m pip install --user pyyaml pytest
```

Optional, only for specific paths: `gensim` + `umap-learn` (embeddings),
`ollama` (local models — the driver prints a harmless `ERR:` line without it).

### 2c. Install the CLI, skill and hook

One-time, global, symlinks only — no project ever carries its own copy:

```bash
ln -s ~/work/agi/extensions/agi/driver.sh   ~/.local/bin/agi
ln -s ~/work/agi/skills/agi                 ~/.claude/skills/agi
```

Ensure `~/.local/bin` is on `PATH`. For Claude Code, register
`extensions/agi/hooks/cc-session-start.sh` as a `SessionStart` hook in
`~/.claude/settings.json` — it is a silent no-op outside a project, so it is
safe to register globally.

### 2d. Verify

```bash
cd ~/work/agi && python3 -m pytest extensions/agi/tests/ -q   # 861 passed, 1 skipped
which agi && readlink -f "$(which agi)"                        # -> extensions/agi/driver.sh
agi --help | head -2
```

---

## 3. The loop, one iteration

```
driver.sh
  ├─ snapshot-goals.py        GOALS.md <- nodes/goal/   (the nodes are the source)
  ├─ snapshot-build-site.py   rebuild origin:build-site nodes from context/plans/build-site.md
  ├─ render-context.py        graph -> context/INJECTION.md (bounded ASCII map)
  ├─ metrics.py               emit METRIC lines   (benchmark.py also exists; see G-goals)
  ├─ dispatch.py              spawn N pi kids; scrubs ANTHROPIC_*/CLAUDE_CODE_* from child env
  ├─ heal.py                  poll manifests, kill hung kids, respawn with the tail of their log
  ├─ post_wire.py             wire edges after kids finish
  └─ cli.py status            report
```

`--smoke` stops after metrics: snapshot + render + metrics, no dispatch, no spend.

**The chain, goal to convergence** — nine types, and the last two are new as of
2026-08-27:

```
goal -> idea -> hypothesis -> experiment -> verdict -> mvp -> outcome
        -> bigger_outcome -> overview -> vision
```

`vision --proposes_goals--> goal` closes the loop **across seasons** and is
declared non-traversable, so the type graph stays acyclic.

Everything else about running it — verdict taxonomy, zoom, the evidence gate,
model tiering, tmux for long runs, the `iter-001` clobber caveat — is in
`skills/agi/SKILL.md` and is deliberately not repeated here.

---

## 4. Glossary (only terms not defined in SKILL.md)

- **PLUGIN_ROOT** — the engine directory, `extensions/agi/`. Resolved from `$BASH_SOURCE`.
- **PROJECT_ROOT** — the graph repo: holds `agi-tree.config.json`, `nodes/`, `context/`, `sessions/`. From `$AGI_TREE_PROJECT_ROOT` (legacy `$AUTORESEARCH_TREE_PROJECT_ROOT`) or by walking up from cwd.
- **Capillary DAG** — the chain shape above: many thin chains, not one thick trunk.

---

# ITER-9 SWEEP — worked 2026-09-01. Status per item.

> Opened as a deferred list mid-session, then worked. Each item records what
> was found, not just what was decided.

1. ✅ **`post_wire._read_frontmatter` — FIXED.** Both branches were unsafe and
   the quiet one was worse. *Two markers + bad YAML* raised uncaught, and
   `post_wire` is in the loop's critical path, so one malformed node lost the
   **whole iteration's wiring**. *No closing marker* returned `{}` + the entire
   file, which `cmd_wire` then WROTE BACK — verified: the node was re-headered
   with a **freshly minted `mint_id`** and its real one demoted into the body,
   inventing an identity and orphaning a grid ref. Now one catchable
   `MalformedNode` class covering unclosed / unparseable / non-mapping, and
   both call sites **skip with a report and never write**. A file with no
   frontmatter at all is still legitimate and still returns `({}, text)` — that
   distinction is the fix.
2. ✅ **Healer contract — FIXED** (`4d00b7927`). `heal.py` told healers to
   commit; one obeyed and produced `7b57b5955`. Contract now matches the kid's.
   `-p` added for consistency. **Still open and worth knowing:** that commit
   stands, authored as the repo owner, and its justification is self-refuting —
   it claims pi hangs without `-p`, while five kids succeeded without it that
   day and the healer that wrote the claim ran without it. **The real cause of
   `a00-df2af9f7`'s hang is still unknown.**
3. ✅ **Evidence-gate self-citation — FIXED.** `evidence_runs: [<my own id>]`
   resolved and bought a decisive verdict — `goal:g7.3`'s hole one substitution
   later. Now: an `experiment` may cite itself (it IS the run); every other type
   may not. `self_id=None` preserves historical behaviour exactly, so no
   existing node is retroactively demoted.
4. ✅ **262 orphaned grid refs — DIAGNOSED, not ongoing.** Two historical
   scars: **185** are `type: level3`, from the level3→build rename that changed
   mint ids rather than only addresses (exactly what `goal:g2.5` exists to
   prevent, and it predates mint-id stability); **76** are chain nodes whose
   ids are gone from the corpus, named `exp:…-r1-extend3` /
   `verdict:…-r1-extend1` — the 2000-hop shortcut-cycle era that was cleaned
   up. 1 was re-minted. **Nothing is producing new orphans.** Reattaching them
   is a migration, not a sweep item.
5. ✅ **`evidence_fraction` was never the problem — the interface was.**
   `--evidence-runs` was absent from the `done` template, so a kid could not
   supply evidence without discovering an undocumented flag. Measured after the
   fix: both verdicts written since carry `evidence_runs: 1`; the one written
   before carries 0. The metric was correct throughout.
6. ⏸ **15 duplicate basenames** across type directories, one repeated 7 times.
   Basename-keyed tooling is silently wrong (a kid hit it as 37 phantom
   disagreements). Left alone: renaming node files changes addresses, and the
   right fix is for readers to key on relative path or mint id — `goal:g13`'s
   territory, not a rename pass.
7. ✅ **`benchmark.py` import-time `sys.exit(1)` — FIXED.** An unguarded
   `except ImportError: sys.exit(1)` at module scope killed any process that
   merely imported it; it took out a kid's first run mid-experiment. `ollama`
   is now required at call time via `require_ollama()`, not at import.
8. ⏳ **The goal sweep: 49 -> 40 active. NOT DONE — the cap is 3.**
   Nine reclassified on mechanical falsifiers (G11, G11.1, G4.6, G3.1, S5, S8,
   S17, S22 complete; G6.5 phasing-out), each with a rewritten `THOUGHT`.
   Forty remain and most are genuinely open; the next pass is judgement, not
   greps. One list item was a **phantom carried across three handoffs** —
   "goal:S16 still carries `status: proved`" is a fenced code block
   *illustrating* the bug S16 describes, found by an unanchored grep.

9. 🔴 **`outcome_coverage` penalises finishing — fix before the next sweep.**
   `metrics.py:483` `SCORING_GOAL_STATUSES = {"active", "horizon"}` excludes
   `complete` and `phasing-out` alike, so today's sweep dropped the primary
   metric **0.27 -> 0.232** with no work undone and no node removed. A metric
   that falls when you finish teaches you not to finish, and this project has
   sat at 49 active against a cap of 3 for three sessions.

   **The fix is a semantics split, not a constant change** — specified on
   `goal:g5`, which owns "status is a field the engine acts on" and whose own
   text is the defect:
   - **`complete`** = achieved. Chains are valid and still extendable, so the
     evidence **stays in the metric**. Success must not read as regression.
   - **retired** (`phasing-out`) = folded into another goal, achieved
     incidentally, or no longer worth pursuing. Results leave the score.
   - A chain that **concluded "retire this goal"** is excluded — it produced
     evidence for *stopping*, which is a decision about the graph, not a
     contribution to it. Counting it would reward abandonment.
   - A goal **retired before any chain closed** is ignored in BOTH terms of
     the ratio, rather than counting as an unconverted hypothesis.

   Naming is the only real gap: `phasing-out` already means retired
   (`CLAUDE.md` documents retirement that way). Renaming costs a `status`
   regex plus a corpus pass — do it with the change, not before.

10. ⚠️ **`npx gitnexus analyze` writes 102 lines into `CLAUDE.md`.** It
    appends a `<!-- gitnexus:start -->` block of **MUST** directives telling
    agents to call GitNexus **MCP** tools — which pi kids have no client for —
    and to query "instead of grepping", which `skills/agi/SKILL.md`
    deliberately does not claim after a measured query returned an unrelated
    symbol. Reverted before the 2026-09-01 push. **Re-check `git status` after
    every `analyze`**; it edits the one document every agent reads first.

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

node_count  866      active 859   deprecated 8    goals 102
outcome_coverage 0.284   evidence_fraction 0.211   unevidenced_decisive 1
goals: active 9  horizon 65  retired 2  complete 27
tests       1189 pass
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
| 5 | `goal:s23` + `goal:s25` + `goal:s26` (+ `goal:s27`) | ⬜ NEXT |

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

**5 — four goals, all `horizon`, all specified with falsifiers:**

- **`goal:s23`** — a deprecated node still reaches injected context. Measured:
  `build:TODO.md` is deprecated, moved to `.agi/nodes/deprecated/`, and still
  sits at `INJECTION.md:85`. **Fix the render/chain-selection path, not the
  loader** — four readers depend on deprecated nodes still loading.
- **`goal:s25`** — `evidence_gate.build_corpus` rglobs whatever directory it is
  handed. Split out of `goal:s10` when that retired.
- **`goal:s26`** — an overarching goal must not be `complete` while its
  subgoals are live. Warning in `snapshot-goals.py`, not a hard failure.
- **`goal:s27`** — the parent-scaffold defect above. Needs an owner decision
  on what a parent's session artefact is before it can be built.

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

# SESSION HANDOFF — 2026-09-01: the spawn silo, named and half-closed

> **Read this section first.** It supersedes 2026-08-31 below wherever they
> disagree — in particular that section's §3a, which frames the work as "build
> the CC dispatcher". That frame is now recorded as **drift**; see §2.

## 0. State

```
repo         /home/ubuntu/work/agi   ONE repo: source + .agi/ graph + refs/grid/*
node_count   838                     goal_count 95, active 47
tests        1121 pass, 0 fail       outcome_coverage 0.27, evidence_fraction 0.212
runtime      pi, live, primary       CC: config only, and now deliberately deferred
crons        FROZEN — crons_live: false. Unchanged. Do not re-enable.
PUSHED       NO — several commits ahead. Push by hand when ready.
```

**Operating mode, unchanged and deliberate: one pi kid at a time.**
`agent_dispatch.claude_max_parallel: 1`. Aim every run —
`driver.sh --max-iters 1 --target <node-id>` — because an unaimed single-slot
run is the *least* steerable shape available (§4).

## 1. The defect that matters: every pi kid's verdict was being dropped

**Live for the entire life of the pi runtime. Fixed 2026-09-01.**

`dispatch.py` writes the manifest **once**, at spawn. `cli.py done` writes the
kid's results to `<agent>/agent.json`. `heal.py` bridges them by syncing
exactly **one** field — `status` — under a comment reading "so post_wire sees
current state". `post_wire` read the manifest. So `verdict`, `confidence`,
`evidence_runs` and `notes` went to a file nothing read, and every node kept
the scaffold's `pending`.

It hid because **the dropped value equalled the default.** Every pi verdict
anyone had ever observed — including all three of 2026-08-31's verification
runs — was `pending`. The first kid to return anything else exposed it in one
run.

**The quiet part is worse than the lost field.** `post_wire` applies the
evidence gate to the verdict it reads there, so the gate has been running
against `None` and finding nothing to demote. `unevidenced_decisive_verdicts:
0` and `evidence_fraction` never said anything about pi discipline — only that
no pi verdict ever arrived. `post_wire`'s own docstring had claimed since it
was written that it "reads all agent.json records". The loop never did.

Fixed by `post_wire._merged_agent`: manifest for dispatch-time context,
`agent.json` overlaid and winning. Also makes `--no-heal` runs wire correctly,
which they previously did not.

**`mvp:unified-spawn-path` proposes making this structurally impossible** —
the kid writes `verdict`/`confidence`/`evidence_runs` into its own node
frontmatter and `post_wire` reads the node, deleting the four-hop marshalling
path entirely.

## 2. 🔴 The frame was wrong: `goal:g4.3` was masking the real shortfall

The owner's call, and the analysis agrees. `goal:g4.3` says "anywhere the
engine invokes `pi`, allow invoking Claude Code instead". That is the frame the
CC adaptation had **when it was a stop-gap at the start of the project**: two
named runtimes reaching parity. Under it, "unify" reads as "make the second one
work like the first", which is why the CC half stayed configuration with
nothing behind it while the pi half grew.

Observed, not theorised: kids aimed at `goal:g4.3` produced CC-framed nodes,
**correctly**, because that is what the goal asks for. `hypothesis:pi-parent-
tier-mode2` had to be seeded by hand to get pi work out of the same goal.

- **`goal:g4.6` — one spawn path, N harnesses declared in config as adapters.**
  `active`. Filed under g4, not beside g4.3: g4 already says model choice is a
  per-tier knob with nothing hardcoded, and a spawn path that cannot name a
  tier is exactly why that knob was never connected to anything.
- **`goal:g4.7` — healing belongs to every harness, and inside the dispatch
  loop.** `horizon`, waiting on g4.6 to define completion.
- **`goal:g4.3` keeps its own live items** (H4b `closed_chains.txt`, hook
  parity, H9's question channel) and carries a superseded-in-intent banner. Not
  rewritten — that text steered real work and a reader needs to see the frame
  that produced those nodes.

**`mvp:unified-spawn-path` is the design to build from.** Two-function adapter
interface (`build_command`, `child_env`), the config shape, an explicit
out-of-scope list, four falsifiers. **Read it before writing any of this.**

### 2a. Completion must become a graph event

The owner's addition, and the piece most likely to be discarded as an
implementation detail. It is not one. Today "done" is `cli.py done` writing
`agent.json` while `heal.py` polls a pid — the pi process model wearing a
general name. A CC kid has no pid. A kid that wrote its node and then died
looks identical to one that never started (a 2026-08-31 field note, handled by
hand ever since).

**The finish signal should be the scaffolded node acquiring real content.**
Observable by any harness, and identical from the spawned agent's own point of
view: *write your node*. `cli.py done` demotes from the definition of done to
one way to announce it. This is also a prerequisite for `goal:g1.9`'s
assembled brief, which cannot describe finishing without naming a runtime
until it lands.

## 3. `mvp` is now a design type, not a code type

`[mvp].md` revised. The corpus said so before anyone decided it: `source_files`
**0/26**, `tests_pass` **0/26**, `commit_hash` **0/26** — the three fields that
would make an MVP a code artifact have never been filled in by any author. The
old schema read that as a backlog; it reads better as a measurement. An `mvp`
now states the minimum a subsequent `build` must satisfy, plus the falsifier.
It removes a real overlap too: `build` nodes already carry code mechanically,
and the hand-maintained second copy is the one that drifts.

## 4. `dispatch.py` can now be aimed

`--target ID [--level L]`, passed through from `driver.sh`. Before this, a
single-slot run was unsteerable: `_pick_targets` short-circuits at `n <= 1` to
`("big", None, "explore_new")`, so the one kid always scaffolded a parentless
`idea` and explored wherever scoring pointed. `_explicit_targets` bypasses
scoring; `small` is the default level because `zoom_command` omits `--target`
for big zoom and would silently discard the aim.

Not fixed, and it still bounds what aiming buys: **`closed_chains.txt` has
never been written**, so unaimed selection still draws from the full set.

## 5. 🔴 Next tasks, in order

1. **Finish `goal:g4.6`: the completion half.** The **spawn** half LANDED
   2026-09-01 (`2857a7f64`) — `bin/adapters/` with `pi_adapter` and a
   `claude_code_adapter` stub, `harnesses`/`spawn` in config, tier selecting
   the model, and falsifiers 1–3 passing as tests. Verified live: a kid spawned
   with `harness=pi tier=kid` and a command built entirely by the adapter.
   **Falsifier 4 is the one still open** — completion as a graph event.
   `hypothesis:a00-9bae6ee8-52d7f5` is aimed at exactly it and names the work:
   one shared `is_complete(root, node_id)`, `post_wire` reading verdict data
   from the node's own frontmatter with `agent.json` only as fallback, and no
   harness-keyed branch in the completion path. Its named risk is the MVP's own
   weak joint: if "scaffold filled with real content" needs harness-specific
   knowledge, the seam is wrong — the scaffold-hash variant is the fallback.
2. **The parent tier spawns, but has no brief. Deliberately left manual.**
   `dispatch.py --tier parent` works and correctly selects
   `harnesses.pi.models.parent` (`qwen/qwen3.8-27b`) — but the brief it hands
   that process is **the kid brief**, because `_build_pi_args`' successor
   builds one prompt shape and `zoom.py`'s contract knows tiers not at all. So
   a parent spawned today is a kid on a better model, which is worse than
   useless: it would write one node and stop, while looking like it ran a loop.

   **Not built on purpose, for a reason worth keeping.** A parent brief is
   `goal:g1.9`'s object — *"a parent should name the target and the tier, and
   nothing else"* — and writing one by hand now would create exactly the
   hand-maintained copy of a contract that g1.9 exists to delete. It also
   depends on clause 5 above: a parent brief has to tell a parent how it knows
   its kids finished, and that answer is changing.

   **Until then, the delegator is the parent**, by hand, which is how every
   iteration in this session ran and it worked. What a parent brief will need
   when it is written: the target and tier only; how to spawn (shell out to
   `dispatch.py --tier kid --target <id>`); the review gate; and the
   serialization rule — **`spawn.parallel` does not bound grandchildren**
   (`experiment:a00-763e629b-5c04ad`), so a parent's own spawns need the limit
   applied again, and making that a property of the brief alone means a parent
   that ignores its brief can still collide.

3. **Decide what a design MVP's child is.** `_node_type_for` maps
   `mvp -> outcome` and the documented chain agrees — both assuming `mvp` held
   built code. It no longer does (§3), so **the chain has no step meaning
   "implement this design"**, and a kid aimed at a design MVP is scaffolded an
   `outcome` it cannot honestly write. The first kid aimed at one hit this
   immediately and adapted by writing a falsifier baseline instead. `task` is
   the likely answer; the change touches every chain, so it was recorded rather
   than made in the same pass as the redefinition. **Do not fix it by quietly
   widening `outcome`.**
4. **Graph the code (`iomap`, unbuilt).** The owner wants the engine's own
   source queryable as a graph. **Interim: gitnexus**, which is installed and
   works on standard code — worth wiring into the `agi` skill so kids can use
   it instead of grepping. Not started; no node yet beyond this paragraph.
5. **`goal:g4.7`** once completion is a graph event — half of it dissolves
   then.
6. **The goal sweep, still 47 active against a cap of 3.** Two more were added
   this session, both genuinely in flight. Same job as ever: classify with
   evidence. `goal:S16` still carries `status: proved`, a verdict value in a
   lifecycle field.
7. Carried unchanged from 2026-08-31 §3: `goal:g1.9` (assembled brief — now
   partly blocked on 2a), `goal:g1.4` stage 2, `goal:g1.8` items 2–3,
   `goal:g6.6`, `goal:g1.5` init, the `goal:g8.2` falsifier, and the
   SessionStart hook still printing `agi-tree`.

## 6. 🔴 Traps from this session

- **A green suite says nothing about the runtime, again.** 1097 tests passed
  over a `post_wire` that had never once read a kid's verdict. It took a kid
  returning a non-default value to surface it. **Run the loop.**
- **A defect hides perfectly when its wrong answer equals the default.** The
  verdict drop was undetectable for as long as every verdict was `pending`.
  When a field's failure mode is indistinguishable from its common value, the
  test has to supply an uncommon one.
- **Delegating to a shared function can trade churn for corruption.** Making
  `post_wire` use `write_frontmatter` exposed that it has no dict branch, so
  nested mappings became Python reprs in string scalars — and `crons.py` reads
  one of those to build the real crontab. Round-tripping all 833 nodes before
  trusting the change is what caught it (**0 data-lossy, 787 byte-identical**).
- **An explicit warning in the brief is not a fix.** The contract already said
  "N is an INTEGER PERCENT... not a 0..1 fraction — that is what
  `--confidence` takes", and a kid still passed 65 to `--confidence`. Two
  scales on one command line is the defect; the prose was never the problem.
  Now shown as one filled example with both numbers pointed at.
- **Hand-written nodes skip `mint_id`.** `grid.py commit --all` says
  `N error(s) (missing mint_id)` and does not version them. Read that line.
- **`test_zoom.py` drives zoom as a subprocess**, so a test asserting on an
  internal helper has to load the module — it is not importable by default.
- **Three test assertions were substring checks against raw file bytes**, so
  they asserted *serialization* where they meant to assert *the gate*, and
  broke on a quoting change alone. Rewritten to parse frontmatter.

## 7. Known-good verification sequence

```bash
cd /home/ubuntu/work/agi
bash extensions/agi/driver.sh --smoke --max-iters 1     # node count must not drop; secrets ok
python3 -m pytest extensions/agi/tests/ -q              # 1121 passed
python3 extensions/agi/bin/snapshot-goals.py --render --check   # 95, byte-identical, exit 0
python3 extensions/agi/bin/grid.py status               # 0 changed on a clean tree
python3 extensions/agi/bin/crons.py show                # crons_live: False, none installed
bash extensions/agi/driver.sh --max-iters 1 --target <node-id>  # LIVE, aimed, costs cents
```

After the last line: `git log --oneline -1` must still be **your** commit, and
the kid's node must carry the verdict the kid reported — not `pending` by
default. That second check is new, and it is the one that would have caught §1.

---

# SESSION HANDOFF — 2026-08-31: paid keys in, pi runtime audited live

> **Read this section first.** It supersedes 2026-08-30 below wherever they
> disagree — in particular that section's §3a, which is the *previous* state of
> the credential work and is now finished. The pi runtime was run end to end
> three times this session; every claim below about it was watched, not
> reasoned about.

## 0. State

```
repo         /home/ubuntu/work/agi   ONE repo: source + .agi/ graph + refs/grid/*
HEAD         (see git log)           720 commits, 1102 grid refs
node_count   832                     active 827, deprecated 5, goal_count 93
tests        1098 pass, 0 fail       outcome_coverage 0.275
provider     OpenRouter, LIVE        .env set, pi resolves it, both models ping OK
runtime      pi: verified live 3x    CC: config only, no dispatcher — see §3a
crons        FROZEN — deliberately, not pending. See §0a before touching them.
PUSHED       master + refs/grid/* pushed by hand 2026-08-31. Remote is current.
```

## 0a. Operating mode: manual, deliberately. Do not re-enable the crons.

**The owner's sequencing, 2026-08-31 — this is a decision, not an oversight:**

1. **Finish automated worktree branching first** (`goal:g4.1`). Not because
   the loop is unstable — three live runs were clean — but because the one
   failure it produced was a shared-worktree collision, and turning a schedule
   on is the wrong moment to find the next one.
2. **Then ramp live slowly: one parent, spawning two kids at a time.** Not the
   full `iterations_per_run`, not unattended.
3. **Crons stay `crons_live: false` until both.** The grid is run by hand —
   `grid.py commit --all` after a commit — with periodic manual pushes. That
   is working; `grid status` reports 832 clean and remote refs match local.

Pushing is manual too. `master` and `refs/grid/*` were pushed by hand on
2026-08-31 and are current; nothing pushes on a timer.

**`goal:g4.1` now carries the open question this depends on**, recorded rather
than answered at the owner's direction: *what a worktree means once the tiers
are nested* — whose tree it is, where review happens when kids wrote in
separate trees, what an iteration commit becomes across N branches, and whether
the grid makes the merge smaller or just hides it. `isolation: worktree`
already exists in the dispatch layer, so the mechanism is not what is missing;
the shape is. **Flagged for a dedicated small-context brainstorm** — a
half-chosen answer gets built into both runtimes at once through `goal:g4.3`
and is expensive to reverse.

## 0b. `agi-tree` is ARCHIVED and read-only. Everything goes in `~/work/agi`.

**`~/work/agi-tree` is prior art. It is finished, complete, and closed.** Three
guards, applied 2026-08-31, innermost last:

| | guard | effect |
|---|---|---|
| 1 | `agi-tree.config.json` → `.RETIRED` (`bb9d29be8`) | no agi tooling resolves it as a project |
| 2 | `CodexOperator/agi-tree` archived on GitHub | remote is read-only; every push gets `403 … archived so it is read-only` |
| 3 | `.git/hooks/pre-commit` refusing, in that working copy | a local commit is refused rather than becoming a dead end |

Guard 3 exists *because of* guard 2: with a read-only remote, a local commit
would **succeed** and then sit in that working copy forever, unpushable, with
nothing telling you until you tried. A refusal beats a silent dead end. Both
were tested — push returned 403, commit was refused, and the test commits were
discarded (`HEAD` is still `bb9d29be8`).

**The archive is complete and was verified ref-by-ref**, not assumed: all 3
branches and all 1080 grid refs exist on the remote at the same sha, with zero
local-only refs. `master` was 5 ahead and `iter24-extend-300hop` 9 ahead before
this; both were pushed. *(Those 9 were not unique work — every one is reachable
from `master`; the remote branch pointer was simply stale. Worth knowing before
anyone goes looking for lost commits on the branch `CLAUDE.md` warns about.)*

Why guard 1 mattered in the first place: the config made the resolver treat it
as a *live* legacy project, and its `source_root` resolved through the
`agi -> ~/work/agi` symlink to the **live engine**. A loop run from there would
have rewritten that repo's `GOALS.md` from its 809 stale goal nodes and minted
build nodes from live engine source into the retired graph. Nothing warns — the
resolver was behaving correctly for what the marker file claimed.

```
locations.py  from agi-tree        -> ERR: no agi project found        (was: a live project)
locations.py  from agi             -> /home/ubuntu/work/agi/.agi        (unaffected)
locations.py  agi-tree/agi         -> /home/ubuntu/work/agi/.agi        (symlink still fine)
```

**To reverse any of it:** unarchive in GitHub settings, `git mv` the config
back, `rm .git/hooks/pre-commit`. None of it deletes anything.

## 0c. `find-root.sh` hung on relative paths — fixed, found by accident

Running `find-root.sh .` from a non-project directory **spun at 100% CPU
forever**: the upward walk did `d="$(dirname "$d")"` on the raw argument, and
`dirname .` is `.`, so `d` stopped changing while the loop waited for it to
reach `/`. No output, no error, no timeout. `dirname nope` is also `.`, so a
nonexistent relative path did it too.

It survived because **every live caller passes `$PWD`** — triggering it needs a
relative argument *and* no project above the cwd. `driver.sh` was never at
risk. The Python half was never affected: it does `Path(start).resolve()`
first, and this now does the same, including for paths that do not exist.
Second effect fixed with it: a relative start used to return a *relative* root
(`./.agi`), which callers hand to other processes.

`test_bash_and_python_agree` only ever passed absolute paths. Ten new cases in
`test_locations.py` cover relative, nonexistent and symlinked starts; the
timeout is the assertion, so a regression hangs rather than passes.

## 1. Provider keys — DONE. Do not redo this.

`.env` exists, mode 0600, and `driver.sh --smoke` prints
`[secrets] ok: … satisfies required keys: OPENROUTER_API_KEY`. The chain, end
to end:

```
.env  →  bin/envfile.py  →  driver.sh (sources it) ──→ dispatch.py → pi → kid
      ↘  bin/env-get.sh  →  ~/.pi/agent/auth.json  ──↗   (same one value)
```

`.agi/nodes/.geometry/secrets.md` declares where `.env` is and which keys it
must hold; `bin/envfile.py` is the only reader. **Shape is graph content
(`.env.example`, committed, has a build node); value is not, ever.**

**Models. `~/.pi/agent/models.json`, not `settings.json`** — pi reads custom
models from the former only, which cost an hour to find. Both are registered
there because pi's baked registry does not know either:

| tier | model | $/Mtok in / out |
|---|---|---|
| pi default + parent | `qwen/qwen3.8-27b` | 0.43 / 2.55 |
| kid (`agent_dispatch.model`) | `z-ai/glm-5.3-flash` | 0.075 / 0.25 |

Verify in one line: `pi --list-models | grep -E 'qwen3.8-27b|glm-5.3-flash'`.
Backups: `~/.pi/agent/{settings,auth}.json.bak-2026-08-31`.

## 2. The pi runtime works, and was silently broken in five places

Three live `--max-iters 1` runs. The path is sound — dispatch → 2 kids → nodes
written → `heal.py` closes them out → `post_wire` adds the edge → status. Every
defect below was found by *running* it; none was visible by reading.

1. **pi kids were handed the CC contract.** `zoom.py::default_runtime()`
   answers `"cc"` for any project carrying a `cc_dispatch` block, and a project
   may carry both — so pi kids read *"Do not call cli.py"* in the one runtime
   where `cli.py done` is how the manifest closes. Both kids reported the
   contradiction and correctly ignored their own context. `dispatch.py` now
   passes `--runtime pi` explicitly (`goal:s8`).
2. 🔴 **A kid ran `git commit -A`** and swept a second kid's half-written node
   *and* a human's uncommitted engine edits into one commit labelled with its
   own node id — **`d34048aa1`, left in place deliberately**: it is true
   evidence for `goal:g4.1` and rewriting it would erase that. Nothing was
   lost; the history says something untrue. Cause: the pi contract said how to
   signal done and nothing about git, so committing read as part of finishing.
   Both contracts now forbid git outright.
3. **Every healer ever spawned died at birth.** `heal.py` passed
   `--max-turns 8`; pi has no such flag, printed `Unknown option`, and **exited
   0**, so the loop recorded a healer as launched that never read its context.
4. **Healers billed the Claude Code subscription.** That `Popen` had no `env=`,
   so it inherited the `ANTHROPIC_*` vars `dispatch.py` scrubs. The scrub
   existed; the healer sat outside it. One shared definition now.
5. **A parentless idea produced a bare `--parent`**, which argparse rejects.

Also fixed: `agent_dispatch.provider/model/thinking` are now *real* pi flags —
`_build_pi_args` used to read the config and use none of it, so every kid ran
whatever `settings.json` said. `agent_dispatch.max_turns` was dropped from
config and SKILL.md: pi has no turn cap and nothing read the key. And
`VERDICT_HELP` now says `N` is an integer percent — a kid wrote
`inconclusive_lean_proved:0.6`, was rejected, and fell back to `pending`,
losing the lean it had formed.

### 2a. 🔴 `struggles:` is the instrument. Read it every run.

**Four of the five defects above came out of a kid's `struggles:` line** —
unprompted, accurate, one line each. Nothing else in this system reports
harness bugs, because nothing else is *inside* the harness while it runs.

**To be clear about where the field comes from: kids did not invent it.** It is
specified in `SKILL.md`'s DONE contract and emitted by `zoom.py::
completion_contract()`. But it was in the **CC** branch only, and the moment
fixing §2.1 gave pi kids their own contract they stopped emitting it and
reported in free prose instead — run 3's verdict-taxonomy defect survived as a
loose "Note:" and could as easily have been dropped. **Both contracts now carry
the report block**; they differ only in how a kid *signals* completion
(`cli.py done` for pi), never in what it *reports*. `test_zoom.py` asserts
both. The old test asserted the pi contract had no report block at all, which
encoded the gap as a requirement — rewritten.

The wording now distinguishes the two lines, because they do different jobs:
`caveats` is what the kid knows is weak about **its node**; `struggles` is what
fought it — a tool, a flag, a contradiction. The second finds engine bugs,
because a kid describing what obstructed it is describing the harness. It also
now says **report a struggle even when you worked around it**, which is exactly
what run 3's kid did and nearly did not say.

## 3. 🔴 Next tasks, in order

### 3a. The CC dispatcher — specified, not built (`goal:g4.3`)

**`cc_dispatch` is configuration with nothing behind it.** `kid_model` and
`parent_model` are read by no code. The spec now lives in `goal:g4.3` and has
four parts, of which the first two are the owner's explicit requirement:

1. **Spawn kids directly** — N kids, one node each, the shape `dispatch.py`
   already produces for pi. Cheap mode, must work first.
2. **Spawn parents, which then spawn their own kids** — a parent owns one
   loop: picks targets, spawns kids, reviews, enforces the evidence gate,
   reports. Tier is assigned at spawn; kids never become parents.
3. **A model per tier, independently** — `parent_model` for parents,
   `kid_model` for kids, in *both* modes. Neither may silently inherit the
   other's; tiering the model is the point of having tiers.
4. **Provider-agnostic via the OpenRouter Python SDK, not raw HTTP** — so a
   minor change on their side cannot silently break the loop.

**The invariant that must not break: a runtime flag, not a parallel code
path.** Target selection, spawn gate, evidence gate, `post_wire` and the node
format stay shared. If the CC dispatcher grows its own copy of any of them,
this goal has failed even if the dispatcher runs.

Until it exists, **OpenRouter is reachable through the pi runtime only** —
Claude Code's subagent tool spawns Claude models and nothing else.

### 3b. `closed_chains.txt` has never been written (`goal:g4.3`, H4b)

`driver.sh`'s `benchmark.py` call is **removed** — it passed a directory where
a chain id belongs and never got that far anyway: the module exits at import
without `ollama`, under `|| true`. One `ERR` line per run, for however long.
The consequence is live: `dispatch.py` reads `closed_chains.txt` to stop
re-picking a finished chain, and nothing has ever written it, so target
selection has drawn from the full set every iteration. Re-enabling wants a
per-chain loop, a config gate, and the dependency present.

**The old diagnosis was half wrong and is corrected in the goal:**
`benchmark.py` does not import `ranking.py`. The attractiveness path was never
implicated; `dispatch.py::_pick_targets` does its own scoring and does run.

### 3c. Stop hand-typing spawn prompts (`goal:g1.9`, new)

**Before running hierarchical loops at any volume, read this one.** `SKILL.md`
still tells a parent to hand-assemble a self-contained brief per kid, naming
six ingredients: zoom scope, target parent id, chain step, node file format,
verdict taxonomy, project paths. **The engine already knows all six at spawn
time.** The parent is retyping harness state into a string, once per kid, once
per iteration — in the tier where tokens cost most, since a parent's context
carries every brief it wrote for the rest of the run.

It is also a correctness problem, which is why it is above the goal sweep: a
hand-assembled brief is a hand-maintained copy of a contract enforced
elsewhere, so it drifts silently. **Both §2.1 and the `:0.6` verdict bug are
instances of exactly that**, found in one session.

The falsifier is the half that matters: change the verdict taxonomy in
`evidence_gate.py`, spawn again, and **the brief must change with it in the
same commit with nothing edited by hand.** The convenience half will look done
long before that holds.

Neighbours it must not be merged into: `goal:g1.6` (cost of *invoking* a
command), `goal:g1.1` (how little an agent needs to orient), `goal:g1.4` (what
it may *touch*). `goal:g4.3`'s dispatcher is the first consumer — if it grows
its own brief assembler, that goal's "runtime flag, not a parallel code path"
invariant is already broken.

### 3d. The kid tool allowlist now has live evidence (`goal:g1.4` stage 2)

§2.2's rogue commit is stage 2's case, recorded on the goal. Worth restating
precisely: the failure was **not** a badly written node, it was a **raw write
to a path the graph does not own** — a kid's shell being the widest such path.
Words are stage 1 and both contracts now forbid git in words, but a wording fix
depends on every future kid reading and obeying; an allowlist makes the call
unavailable.

**The stage gate still stands and this does not license skipping it.** No kid
this session reached for a file the graph could not answer, so stage 1's
measurement is still what derives the allowlist. Clamp after measuring, not
before.

### 3e. The goal sweep — now 46 active against a cap of 3

Unchanged from 2026-08-30 §3b and two worse: `goal:g1.8` and `goal:g1.9` were
both added this session and both are genuinely in flight, which is the honest
use of `active` and still makes the number less useful. Same job: classify with
evidence into complete / phasing-out / horizon / at most three active.
`goal:S16` still carries `status: proved`, a verdict value in a lifecycle
field.

**Do this before running loops at volume, not after.** The sweep is what makes
`INJECTION.md` say something to a kid picking a target; with 46 goals claiming
to be in flight, target selection is choosing from noise — and `closed_chains
.txt` (§3b) never having been written means it is choosing from *all* of it.

### 3f. `goal:g1.8` items 2–4

`init` rendering the `.env` stub (G1.5's job); a verifier that no tracked file,
grid ref or session transcript ever contains a value from `.env`; and item 4,
which is 3a above.

### 3g. Carried, unchanged

Everything in 2026-08-30 §3c: **G6.6** prose contracts, worktree-per-kid
isolation (**G4.1** — now with live evidence, see §2.2), **`init` (G1.5)**,
the **G8.2** falsifier, and the SessionStart hook still printing `agi-tree`.

## 4. 🔴 Traps from this session

- **A green test suite says nothing about the runtime.** 1081 tests passed
  over a `heal.py` that could not spawn a healer, a `dispatch.py` that ignored
  its own model config, and a `zoom.py` that handed kids the wrong contract.
  All four surfaced within two live runs. **Run the loop.**
- **Kids are the best defect reporters you have.** Four of the five bugs above
  were in kid `struggles:` lines, unprompted and accurate. Read them.
- **`|| true` is where bugs go to live.** Two of the five were invisible
  because a non-zero exit was swallowed — and pi's own `Unknown option` path
  exits **0**, so even `set -e` would not have caught the healer.
- **Check which file a tool reads before writing to it.** Registering models in
  `~/.pi/agent/settings.json` looked correct, changed nothing, and reported no
  error; pi reads `models.json`.
- **The verification runs left six kid nodes in the graph.** They are real
  loop output and are kept — `node_count` never drops. Runs 1 and 2's four are
  in `d34048aa1` (see §2.2); run 3's two are reviewed and committed normally.

## 5. Known-good verification sequence

```bash
cd /home/ubuntu/work/agi
bash extensions/agi/driver.sh --smoke --max-iters 1     # node count must not drop; secrets must say ok
python3 -m pytest extensions/agi/tests/ -q              # 1098 passed
python3 extensions/agi/bin/snapshot-goals.py --render --check
python3 extensions/agi/bin/envfile.py --check           # exit 0
pi --list-models | grep -E 'qwen3.8-27b|glm-5.3-flash'  # 2 lines
bash extensions/agi/driver.sh --max-iters 1             # LIVE, ~90s, ~2 nodes, costs cents
```

The last line is the one that matters and the one that was missing. After it:
`git log --oneline -1` must still be **your** commit — a kid that committed is
a regression of §2.2.

---

# SESSION HANDOFF — 2026-08-30: the migration's residuals, closed

> **Read this section first.** It supersedes 2026-08-29b below wherever they
> disagree — in particular §1 of that section, which says the repo is unpushed
> and blocked on a remote decision. **Both halves of that are now false.**

## 0. State

```
repo         /home/ubuntu/work/agi   ONE repo: source + .agi/ graph + refs/grid/*
HEAD         efa7ea347               714 commits, 1087 grid refs
node_count   816                     active 811, deprecated 5, goal_count 91
tests        1049 pass, 0 fail       metric outcome_coverage 0.283 (was 0.255)
crons        FROZEN — crons_live: false. See §4.
PUSHED       master is 2 commits ahead of origin. Grid refs are current.
```

## 1. The remote question is SETTLED. Do not reopen it.

The previous section called the push blocked pending a new repo name. It was
not blocked — **the hourly `branch_push` cron had already published everything
to `CodexOperator/agi`** before anyone decided anything. `git rev-list
--left-right --count origin/master...HEAD` read `0 0`.

The owner's decision, 2026-08-30, is that **the `agi` name stays on the live
repo**. Three repos, and this is the final shape:

| repo | holds | commits |
|---|---|---|
| `CodexOperator/agi` | **canonical and live.** The unified repo, keeping its split-era history. `origin` points here. | 714 + 1087 grid refs |
| `CodexOperator/agi-archive` | the engine immediately before the merge: `21308535f`, no `.agi/` | 210 |
| `CodexOperator/agi-tree` | the pre-migration graph repo, untouched | — |

`agi-archive` was created and pushed 2026-08-30. It is push-once; **no local
remote was added for it**, deliberately, so nothing can accidentally push there
again. The rename-to-archive plan was dropped because, post-push, renaming
`agi` would have produced two identical repos and a true engine-only archive
would have needed a force push against published history.

## 2. What landed, 2026-08-30 — two iterations, four kids

**iter-5 (`b124133d3`) — the two post-migration bugfixes.**

- **All ten `bin/` entry points delegate to `locations.py`.** `goal:g11.1` is
  closed; its falsifier (`grep -c '^CONFIG_NAMES' extensions/agi/bin/*.py`)
  went 11 → 1. The goal said ten *duplicates*; the measurement said ten
  *breakages* — no `agi-tree.config.json` or `autoresearch-tree.config.json`
  exists anywhere in this repo, so every copy of the legacy walk was already
  dead code resolving nothing. Seven failed hard, two answered `os.getcwd()`
  with no walk at all, one had the right root and a wrong config lookup.
- **`grid.py` takes two roots** — `repo_root` for every git invocation,
  `graph_root` only for finding node files. `grid.py status` went from
  reporting 809 byte-identical nodes as `CHANGED` to reporting 0. `--full-tree`
  was proven **not load-bearing** once the roots are split (stripped: 68/68
  pass; conflation restored: 5–7 fail). Both spellings shipped anyway, now
  provably belt-and-braces. `cmd_diff` was separately returning an empty diff
  and exit 0 — `git diff` has no `--full-tree`, so the flag never covered it.

**iter-6 (`efa7ea347`) — the residuals.**

- **`order:` is retired.** `GOALS.md` renders by natural `goal_id` sort. The
  new document is a byte-exact permutation of the old: identical size, empty
  sorted-line diff, all 70 G-goals in place, only S1..S17 rotated out of
  historical order.
- **`cron:crons` can finally say which value kills.** See §4.
- **`metrics.py` no longer measures the retired publish boundary.** Four dead
  metrics removed; `unpushed_graph_*` fixed and renamed to `unpushed_commits`/
  `unpushed_reason`, routed through `locations.repo_root()` — the `not-a-repo`
  sentinel was it treating `.agi/` as its own repo. **No metric reports a
  sentinel in place of a measurement any more.**

**Three live bugs found in passing, none of which anyone was looking for:**

| bug | what it would have done |
|---|---|
| `snapshot-goals.py` lost `.agi/config.json`, fell back to `BODY_CAP=4000` | written **26 of 91 goal NODE bodies truncated** on the next `--snapshot`. `driver.sh` only runs `--render`, which is the only reason it had not fired |
| `zoom.py::default_runtime` returned `pi`, not `cc` | handed every Claude Code kid the **wrong completion contract** — `goal:s8`, silently re-broken by the layout change |
| `snapshot-build-site.py` answered `os.getcwd()` with no walk | run its prune against the wrong tree. The 159 build-site nodes survived **only because the missing-`build-site.md` guard returns before the unlink** — the guard, not the resolver |

That last one has since been exercised for real: with the resolver fixed the
prune path is reachable for the first time, and it re-derived exactly
`7 idea + 61 hypothesis + 91 task = 159` and changed nothing.

## 3. 🔴 Next tasks, in order

### 3a. 🔴 ONE MANUAL STEP REMAINS: paste the OpenRouter key (goal:g1.8)

**Added 2026-08-31. Item one because no paid iteration runs until the value is
on the box, and the value is the one thing an agent must never touch.**
Everything around it landed this session:

```
.env.example                     committed — the SHAPE of the secret set, has a build node
.env                             gitignored, mode 0600 — the VALUES, never committed  ← MISSING
.agi/nodes/.geometry/secrets.md  DECLARES both paths + required/optional/forbidden keys
extensions/agi/bin/envfile.py    the one reader — resolves the node, checks the file
extensions/agi/driver.sh         asks envfile.py, runs the check, sources the file
extensions/agi/bin/env-get.sh    prints one value; for pi auth.json's "!command" form
~/.pi/agent/auth.json            openrouter entry → env-get.sh (pointer, not a copy)
~/.pi/agent/settings.json        default model qwen/qwen3.8-27b; both OR models registered
.agi/config.json                 agent_dispatch → openrouter / z-ai/glm-5.3-flash / medium
```

Backups of both pi files are at `~/.pi/agent/*.bak-2026-08-31`.

**Do this over SSH. Never paste the key into an agent session — not into a
prompt, not into a file an agent then reads back:**

```bash
cd /home/ubuntu/work/agi && cp -n .env.example .env && chmod 600 .env && read -rs -p 'OPENROUTER_API_KEY: ' K && printf 'OPENROUTER_API_KEY=%s\n' "$K" >> .env && unset K && bash extensions/agi/driver.sh --smoke --max-iters 1 2>&1 | grep secrets
```

Expected last line: `[driver] [secrets] ok: /home/ubuntu/work/agi/.env satisfies
required keys: OPENROUTER_API_KEY`. Then confirm pi resolves it — this is the
step that proves the indirection works and that the model slugs match:

```bash
pi --list-models | grep -E 'qwen3.8-27b|glm-5.3-flash'
```

**If those two lines do not appear, the model id string is what to adjust**, in
`~/.pi/agent/settings.json` — `providers.openrouter.models[].id` and
`agents.default.model`. pi's baked registry does not know either model (checked:
it knows `z-ai/glm-5` and `glm-5.1`, not `5.3-flash`), which is why they are
registered explicitly rather than merely named. Both ids are real —
`https://openrouter.ai/api/v1/models` lists them — so a mismatch is pi's
matching rule, not a wrong slug.

**Model routing, as decided 2026-08-31.** pi general default and the parent
role: `qwen/qwen3.8-27b` ($0.43/$2.55 per Mtok, 1M ctx). Kid role:
`z-ai/glm-5.3-flash` ($0.075/$0.25, 1M ctx) — ~6x cheaper in, ~10x out, which
is the right shape for the tier that does the most talking.

🔴 **`cc_dispatch` cannot be pointed at OpenRouter, and this is a hard limit,
not a config gap.** Claude Code's subagent tool spawns Claude models only;
there is no setting that makes a CC kid an OpenRouter model. So OpenRouter is
reachable **through the pi runtime only** (`driver.sh --max-iters N`) until
someone writes an OpenRouter dispatcher — G1.8 item 4, and the decision there
is already made: **use the OpenRouter Python SDK, not raw HTTP**, so a minor
change on their side cannot silently break the loop. `cc_dispatch` stays on
Claude models and the main chat stays on the Anthropic subscription, which is
what was asked for anyway.

**Fixed in passing, and it was silently defeating every model setting:**
`dispatch.py::_build_pi_args` read `agent_dispatch` and then used none of it —
every pi kid ran whatever `~/.pi/agent/settings.json` said, while the config
key that claims to choose the model chose nothing. It now passes `--provider`,
`--model` and `--thinking` (the `goal:g4.2` dial) when set, and passes nothing
when unset, so a project that configures none of them is unaffected.
`tests/test_dispatch.py` covers both directions.

**Still open — G1.8 items 2–4:** `init` rendering the `.env` stub (G1.5's job);
a verifier that no tracked file, grid ref or session transcript ever contains a
value from `.env`; and the OpenRouter dispatcher above.

**The one hard rule, restated because it is the failure mode with teeth:**
never put `ANTHROPIC_API_KEY` or a `CLAUDE_CODE_*` var in `.env`.
`dispatch.py` scrubs exactly those from pi children so subagents cannot bill
the interactive Claude Code subscription; setting one in `.env` re-adds that
leak from *below* the scrub, where nothing checks. `envfile.py` enforces the
three `ANTHROPIC_*` names as a floor a project's own node cannot lower.

### 3b. The goal sweep. `METRIC_WARNING goal_rotation=45/3` fires every run.

45 goals are `status: active` against `cc_dispatch.max_goals_active: 3` — 44,
plus `G1.8` added by §3a above, which is genuinely in flight and should be among
the first retired once its items 1–3 land.
**This is not only over-declaration — several are finished and mislabelled:**

- `G11` — one repo. Landed 2026-08-29. Should be `complete`.
- `G11.1` — closed by iter-5; its own falsifier passes. Should be `complete`.
- `G6.5` — "the cron rebuilds agi from agi-tree, then commits and pushes it".
  Describes the retired two-repo publish. `phasing-out`, superseded by G11.
- `S5` — "the engine repo has no sync at all". The crons sync it.
- `S8` — "`zoom.py` bakes the pi-runtime completion contract into the kid
  context". iter-5 fixed exactly that.

**So the job is classify-with-evidence, not demote-in-bulk:** complete /
phasing-out / horizon / at most three active. Retire by marking, never by
deleting; `node_count` must not drop.

One off-taxonomy value to fix while there: **`goal:S16` carries
`status: proved`** — a verdict value in a lifecycle field. The four states are
`active | horizon | phasing-out | complete`. The irony is that S16 is the goal
about the evidence gate leaving a `status` shadow behind.

### 3c. Config influence — what `.agi/config.json` should govern and does not

`locations.source_root` and `goals_file` exist. Log paths, remote name and the
branch to push are still computed or hardcoded. `crons.py` is already better
than the note in the previous section implied — it re-resolves the checked-out
branch at every `apply` and **refuses rather than guessing** `master`/`main`.

The cron-symlink question from the previous session still wants costing:
**not possible for crontab** (`/var/spool/cron/crontabs/<user>` is root-owned
and mode-checked; a symlink there is refused or ignored), but **`systemd --user`
timers CAN be symlinked** out of the repo, which would make the schedule a
tracked file. Interim win available without any of that: reduce to **one**
bootstrap cron line running `crons.py apply` and let the rest be graph state.

### 3d. Carried, unchanged

- **G6.6** — `build:CLAUDE.md` / `AGENTS.md` / `GOALS.md` exist but carry
  `parse_ok: false` and empty contracts. Give them real prose contracts.
- **Worktree-per-kid isolation (G4.1)** — now genuinely possible; one repo
  means a `git worktree` isolates source, graph and tests together.
- **`init` (G1.5)**, **G8.2 falsifier** (a third project reaching a rendered
  map with no engine change).
- **Cosmetic, but it misleads:** the SessionStart hook still prints
  `## agi-tree map` and `Run: agi-tree --max-iters N`. The command is `agi`.

## 4. 🔴 THE CRONS ARE FROZEN. Turning them back on takes a manual step.

`.agi/nodes/.geometry/crons.md` has `crons_live: false`, set deliberately at
the start of the 2026-08-30 session because a kid was editing `grid.py` —
the exact file the `*/5` job runs. **Nothing is scheduled right now: no grid
snapshot, no ref push, no branch push.**

To restore:

```bash
$EDITOR /home/ubuntu/work/agi/.agi/nodes/.geometry/crons.md   # crons_live: true
python3 /home/ubuntu/work/agi/extensions/agi/bin/crons.py apply
python3 /home/ubuntu/work/agi/extensions/agi/bin/crons.py show   # expect 2 lines
```

**The manual `apply` is required and is not a bug.** `false` removes all four
managed lines including `grid_sync`, and `grid_sync` is the job that re-runs
`crons.py apply`. So the switch is self-disabling in one direction and not the
other — off is one edit, on is one edit plus one command.

While frozen, **nothing pushes.** `git push` by hand if you need the remote
current; `master` is 2 commits ahead as of this writing.

## 5. 🔴 Traps from this session — do not re-learn these

- **Anchor the pattern before believing the number.** Twice in two iterations
  a loose `grep -rl` produced a confident wrong count that an anchored one
  refuted. `grep -rl 'origin: build-site'` returns **167** because eight nodes
  merely mention the marker in prose; `grep -rl '^origin: build-site$'` returns
  the true **159**. Same shape for `THOUGHT:BEGIN` vs `<!-- THOUGHT:BEGIN`.
  Both times the loose number was asserted first and corrected at review.
- **A doc bug can be produced mechanically and survive every version.**
  `cron:crons` said "`crons_live: X` removes every managed line … and
  `crons_live: X` brings all four back" — same X on both sides, at v1, at v2
  and at v3, because each edit replace-all'd the boolean through the prose as
  well as the frontmatter. Prose that embeds a key:value literal is prose a
  find-and-replace will silently corrupt.
- **A commit subject that names one change can carry another.** `27855bafc`,
  "retire two cadences the migration made meaningless", also flipped
  `crons_live` false→true and re-enabled every scheduled job. That is why the
  crons were believed off while they were running and pushing.
- **`git for-each-ref 'refs/grid/*'` returns 0.** The quoted glob does not
  match under `for-each-ref`'s pattern rules. Use `git for-each-ref refs/grid`.
  A brief handed to a kid with the wrong form nearly produced a "the refs are
  gone" finding.
- **Check the filesystem before resuming a dead kid.** Both iter-6 kids were
  cut off when the host process exited. One had landed everything and needed
  nothing; the other had done half its work and no node. Resuming with context
  intact beat respawning cold, and neither lost work.

## 6. Known-good verification sequence

```bash
cd /home/ubuntu/work/agi
bash extensions/agi/driver.sh --smoke --max-iters 1     # node count must not drop
python3 -m pytest extensions/agi/tests/ -q              # 1049 passed
python3 extensions/agi/bin/snapshot-goals.py --render --check   # 91 byte-identical
python3 extensions/agi/bin/locations.py . --json        # layout must be graph_dir
python3 extensions/agi/bin/crons.py show                # says: up to date
python3 extensions/agi/bin/grid.py status | grep -c CHANGED     # 0 on a clean tree
grep -c '^CONFIG_NAMES' extensions/agi/bin/*.py | grep -v ':0'  # exactly 1
```

---

# SESSION HANDOFF — 2026-08-29b: one repo. G11 landed.

> **Read this first.** Everything above is install/orientation and is now
> PARTLY WRONG — it describes the two-repo layout. §2 (bootstrap) and §6 (how
> to write into this file) are superseded by this section. `CLAUDE.md` and
> `SKILL.md` are correct and rewritten.

## 0. State

```
repo         /home/ubuntu/work/agi   ONE repo: source + .agi/ graph + refs/grid/*
HEAD         1c14c46a2               710+ commits, 1080 grid refs
node_count   812                     goal_count 91      tests 1029 pass, in place
metric       outcome_coverage 0.255  evidence_fraction 0.214
crons        2 lines, graph-driven, pointing at /home/ubuntu/work/agi/.agi
PUSHED       NO — 500+ unpushed commits. Deliberate. See §1.
```

`/home/ubuntu/work/agi-tree` and the `agi-tree` remote are the **archive and
fallback**, untouched: 809 nodes, 1080 refs, own history intact. S4's rule —
archive, never delete.

**The workflow is now: edit the file, run its tests, commit.** No `payloads/`,
no `grid.py checkout`, no `stitch --publish`, no `publish-engine.sh`. Those are
retired; the payload *is* the source file. `grid.py commit --all` **stays** —
it versions `node.md` and its payload together as one atomic version, which
plain git does not.

## 1. 🔴 BLOCKED ON A DECISION: where to push

Nothing is pushed. Two reasons, one hard and one procedural:

- **Rollback after a push needs a force push** against published history
  (`verdict:g11-migration-rehearsal` makes this a condition of the verdict).
- **The intended new remote name does not exist.** The owner asked for a fresh
  repo called `AGI`, keeping `agi` and `agi-tree` as archives. **GitHub repo
  names are case-insensitive for uniqueness — `CodexOperator/AGI` resolves to
  the existing `CodexOperator/agi`.** Verified with `gh repo view`. So "AGI" is
  not a new name; it is the old one.

Options, undecided, and the choice is the owner's:
1. A distinct name (`agi-mono`, `agi-one`, `agi2`) — no collision, no rename.
2. Rename `CodexOperator/agi` → `agi-engine-archive`, then create `agi` fresh.
   GitHub leaves a redirect, so the archive's old URL keeps resolving — which
   is either convenient or confusing.
3. Push to the existing `agi` remote. The unified repo *is* that repo's
   history plus the graph's; nothing is lost and no new remote is needed. What
   it costs is the clean separation between "archive" and "live" the owner
   asked for.

Whatever is chosen: **verify `verify_unified.py` reports 8/8 before pushing**,
and keep both existing remotes untouched until it does.

## 2. What landed, 2026-08-29

- **G11 — one repo.** `unify.py` migrated in place; the independently-written
  `verify_unified.py` reported 8/8 (809 nodes in/out, zero bytes changed, 1080
  refs preserved, 494 graph commits as real ancestors, 199/199 `payload_ref`
  resolving unchanged).
- **The first attempt FAILED and `--rollback` restored the repo exactly** —
  209 commits, no `.agi/`, 0 refs, clean. On the real repo, first try.
- **`bin/locations.py`** — the single path resolver. **`bin/crons.py`** —
  cadence read from `.agi/nodes/.geometry/crons.md`, `crons_live` kill switch,
  self-reapplying every 5 minutes. G10.2's first geometry node read by real
  code.
- Four goals recorded for the parentage spine: **G12**, G12.1, G12.2 (moral →
  vision → goal, only morals parentless) and **G9.6** (build-node
  `description:`, body as rendered payload).

## 3. 🔴 Next tasks — iterations 5 and 6, batched

### 3a. Finish G11.1. This is the top item and it is a defect, not tidiness.

**Nine `bin/` entry points still declare their own ancestor walk.** Three broke
within an hour of the migration; see `goal:g11.1` for the table. Fix the rest
by delegating to `locations.project_root_from_env()`.

**Do `snapshot-build-site.py` first** — not because it is worst, but because it
**deletes every `origin: build-site` node it does not re-derive on that run**.
A wrong resolver there is the H0i pruning hazard with the safety catch off. It
has not fired only because nothing has run it from a cwd where the old rule
resolves differently.

Falsifier: `grep -c '^CONFIG_NAMES' extensions/agi/bin/*.py` returns 1.

### 3b. `git ls-tree --full-tree` — the owner asked whether it is a workaround. It is.

`--full-tree` is the *correct flag* for what that call does, so it is not
wrong. But it treats a symptom. **The real defect is that `grid.py` runs git
commands with the GRAPH root as cwd, when grid refs live in the GIT repo.**
Those were the same directory before G11 and are not now.

Proper fix: `grid.py` should take `repo_root` (which `locations.repo_root()`
already returns) for every git invocation, and `graph_root` only for finding
node files. Two roots, two jobs — the same split `locations.py` already makes
and `grid.py` has not adopted. Then `--full-tree` becomes belt-and-braces
rather than the thing holding it up.

Worth doing because the failure mode was **a silent wrong answer**: every one
of 809 nodes read as `CHANGED` while byte-identical. `ref_tip` worked
throughout, which is exactly what made it look fine.

### 3c. Config influence, and folding crons into the graph properly

Manual path editing in cron lines is clunky and the owner is right. Current
state: cadence is graph-declared, but the *commands* are built in `crons.py`
and the paths resolved at apply time.

The owner asked: **can the crons themselves be symlinked into the graph, the
way the skill and hook are?** Short answer, and it needs verifying next
session rather than trusting this note: **not for crontab.** `cron` reads
`/var/spool/cron/crontabs/<user>`, which is root-owned, mode-checked, and
installed only via `crontab -`; a symlink there is refused or ignored by most
`cron` implementations. **`systemd --user` timers CAN be symlinked** from a
repo into `~/.config/systemd/user/`, which would make the schedule literally a
tracked file. That is the shape worth costing.

Interim improvement available without any of that: reduce to **one** bootstrap
cron line that runs `crons.py apply`, and let everything else be graph state —
the `*/5` job already re-applies, so the second line is nearly redundant
already.

Also expand what `.agi/config.json` governs. `locations.source_root` and
`goals_file` exist; log paths, remote names and the branch to push are still
computed or hardcoded.

### 3d. Strip the `order:` field — the owner's call, and the analysis agrees

91 goals carry `order: 0..90`, dense. It is read in exactly one place that
matters: `snapshot-goals.py` sorts the render by it. Every insertion renumbers
every later goal — inserting G9.6 and G12/.1/.2 churned 21 nodes for no
semantic change, twice in one session.

**A queue of 91 is not a priority list.** Sort the render by `goal_id` instead
(natural sort: G1, G1.1, … G12.2, then S1…S21). Derivable from the id, needs
no stored field, never renumbers on insert.

One real consequence to accept: the S-goals are currently in *historical*
order (S11 renders before S1), and `goal_id` sort would reshuffle them once.
That is a one-time document change, and arguably a correction.

Priority/queue then lives in this handoff's §3, which is what the owner wants
and what a human actually reads.

### 3e. CLAUDE.md / AGENTS.md prose nodes — half done automatically

`build:CLAUDE.md`, `build:AGENTS.md` and `build:GOALS.md` now exist: they were
minted the moment the boundary and resolver were fixed, because for the first
time those files are tracked in the repo being scanned. The old layout could
not express them at all.

Remaining: they carry `parse_ok: false` and an empty contract like every
non-Python payload. Giving them real prose contracts is **G6.6**, and spawning
them from `verdict:g11-migration-rehearsal` (or a new verdict on the docs
themselves) is the chain work the owner asked for.

### 3f. Carried from the original iteration 5

- **Worktree-per-kid isolation (G4.1).** Now actually possible: one repo means
  a `git worktree` isolates source, graph and tests together. It never did
  before.
- **`init` (G1.5)** — one command from empty directory to running project.
- **G8.2 falsifier** — a third project, neither `agi` nor `fantasia`, reaching
  a rendered map with no engine change.
- **Sweep `status: active`.** 43 active goals against
  `cc_dispatch.max_goals_active: 3`. The metric warns every run. Move all but
  ~3 to `horizon`; that is what `horizon` is for.

## 4. 🔴 Traps from this session — do not re-learn these

- **`git ls-tree` is scoped by cwd within the work tree.** From `<repo>/.agi`
  it looks for entries under an `.agi/` prefix. Grid trees have `node.md` at
  their own root. Silent wrong answer, not an error.
- **A generator whose output lands inside its own input set does not
  converge.** `level3.py` scanned the graph, wrote to the wrong directory, and
  minted nodes for its own output —
  `nodes-build-nodes-build-nodes-build-….md.md.md`, 3,098 files committed
  before anyone noticed. Fixed by `payload_boundary.is_the_graph_itself` and
  the resolver, but the *class* is what to remember.
- **`git clone` does not copy ignored files.** The real migration failed on an
  ignored `CLAUDE.md` at the engine root that no cloned rehearsal could ever
  have. Four rehearsals could not find it.
- **Ignored files do not appear in `git status --porcelain`.** A "clean"
  cleanliness check is not the same as an empty directory.
- **Existence is not currency.** The publish gate checked whether a
  `payload_ref` existed, not whether it matched, and passed on live data with
  two stale files. Testing a gate against real data rather than fixtures is
  what found it.
- **Three wrong numbers were asserted confidently this session** —
  "thirteen" resolver sites (eleven), "375 payload_refs to rewrite" (zero),
  "166 build-site nodes" (159). All in documents arguing for rigor. **Record
  the command that produced a number next to the number.**

## 5. How to write into this file — SUPERSEDED

The `payloads/` dance in §6 above is retired. It is now:

```bash
$EDITOR HANDOFF.md
python3 extensions/agi/bin/level3.py
python3 extensions/agi/bin/grid.py commit --all
git add -A && git commit
```

## 6. Known-good verification sequence

```bash
cd /home/ubuntu/work/agi
bash extensions/agi/driver.sh --smoke --max-iters 1     # node count must not drop
python3 -m pytest extensions/agi/tests/ -q              # 1029 passed
python3 extensions/agi/bin/snapshot-goals.py --render --check
python3 extensions/agi/bin/locations.py . --json        # layout must be graph_dir
python3 extensions/agi/bin/crons.py show                # must say: up to date
python3 extensions/agi/bin/grid.py status | grep -c CHANGED   # small, not 809
```

If the last one prints a number near the node count, §4's `ls-tree` trap has
come back.

---

# SESSION HANDOFF — 2026-08-29: the publish path is closed, end to end

> **Read this section first if you are the next session.** Everything above is
> the install/orientation guide and is still broadly correct. This section is
> the current state and the work queue.

## 0. State as of commit `65b2a6dd3` (engine `11a8e62`)

```
node_count            792          goal_count             85
active_node_count     787          deprecated_node_count  5
evidence_fraction     0.206        primary (outcome_cov)  0.255
unevidenced_decisive  0            shadow_decisive        0
thought_coverage      0.015        nodes_with_thought     12
hours_since_publish   0.34         publish_blocked_reason (empty)
unpushed_graph        0            unpushed_engine        0
engine tests          861 passed, 1 skipped
```

Graph clean, engine clean, **both remotes current**. `--render --check`
round-trips byte-identical across 85 goals.

## 1. What shipped — four iterations, 2026-08-28/29

The previous handoff's whole queue above S7 is done. **S19, G7.10 and S20 are
all closed**; do not re-open them looking for work.

**S19 — `how` quotes the payload instead of re-rendering the AST.** `_render(source, node)`
returns `ast.get_source_segment`, the literal slice of the payload's own bytes,
joined onto one line. Source bytes are interpreter-independent by construction.
`3.12 → 3.11 → 3.12` against the live corpus now leaves `nodes/` byte-identical
at every step; before, it moved a hunk every time. The node's own blast-radius
estimate was wrong in both halves and is corrected in place: 363 entries
(12.9%) across 55 of 186 build nodes changed value, not "exactly 1 node".
`ast.arguments` deliberately keeps `ast.unparse` — `get_source_segment` returns
`None` for all 1,241 signatures — licensed by measurement and guarded by
`test_no_engine_signature_contains_an_fstring`.

**G7.10 — all four parts, goal closed.** Part 3: a `graph-dirty` refusal parks
the publishable tree on `cron/pending-<graph-sha>` in the engine, **local, never
pushed**, via a `git worktree` outside both repos. Part 4: `level3.py` derives
into a throwaway worktree of the graph and `nodes/` is not written until gate 2
passes. Head-to-head on identical clones with 6 genuinely-moved contracts —
**old path: 6 junk nodes, 6 grid versions burned; new path: 0 and 0.**

**S20 — the alarm reaches the remote.** `hours_since_successful_publish` stopped
at the local commit, so an engine remote 3 days and 25 commits behind moved no
number and was found by looking at GitHub. `metrics.py` now emits
`unpushed_{graph,engine}_commits` from `git rev-list --count @{upstream}..HEAD`
— a **gap**, not an event, because a timestamp can read fresh while work is
stranded. `-1` with a reason token (`no-upstream`, `detached-head`,
`not-a-repo`, `missing`) for every blind spot; `0` never means "could not tell".
No network I/O — the only two occurrences of "fetch" in `metrics.py` are the
comments explaining why one is not called.

**The `export PATH=/usr/bin:$PATH` workaround is no longer load-bearing.** S19
removed the interpreter dependency, so 3.11 and 3.12 now derive identical
contracts. Still worth doing to match the cron exactly, but a session that
forgets it no longer dirties the graph.

## 2. 🔴 The one live trap: a derivation change takes two publishes

**`publish-engine.sh` runs `level3.py` from the ENGINE at step 1, then installs
the new engine at step 3.** So a change to *derivation logic itself* cannot
converge in a single publish.

Publishing S19 re-derived all 55 affected nodes with the **pre-change** renderer,
then shipped the **post-change** renderer over the top — leaving the graph dirty
with a clean revert of the commit that had just landed. It looks alarming and it
is not: one more re-derivation with the now-published engine converges it to
zero.

```bash
python3 /home/ubuntu/work/agi/extensions/agi/bin/level3.py \
  --project . --engine-root /home/ubuntu/work/agi --from-grid
```

Benign and self-correcting, but it arms gate 0 in the window, so **expect it and
do not go hunting for a bug.** Only matters when you change `level3.py`'s own
derivation; every other payload publishes in one pass. Not fixed, not yet
written up as a goal.

## 3. S7 — open, but currently repaired

Seed wiring lived in the `GOALS.md -> nodes` direction. **G6.9 reversed the
arrow and `driver.sh` now runs only `--render`, so S7's "a second run adds it"
became "no run ever adds it."** A sub-goal added after 2026-08-25 gets a correct
`parents:` and its parent is never told.

**The detector currently reports 0 missing edges** — the five that were missing
were repaired by hand, and S20 was minted with `parents: []`, which sidesteps
it entirely. So there is no live damage today; the defect is that nothing
prevents recurrence. The fix has to be re-homed into the render direction, and
S7's original ask — assert the fixed point in a test — still stands.

Check it in one line:

```bash
python3 - <<'EOF'
import pathlib, yaml
n={}
for p in pathlib.Path("nodes").rglob("*.md"):
    t=p.read_text()
    if t.startswith("---"):
        try: fm=yaml.safe_load(t.split("---",2)[1]) or {}
        except Exception: continue
        if fm.get("id"): n[fm["id"]]=fm
print([(a,b) for b,fm in n.items() for a in (fm.get("parents") or [])
       if a in n and b not in (n[a].get("seeds") or [])
       and a.startswith("goal:") and b.startswith("goal:")])
EOF
```

## 4. Next most valuable, in order

**Judgement call, not a ranking handed down.** Nothing on this list is currently
armed to lose data.

1. **S7** — §3. Cheap to detect, and it silently hides exactly the work that is
   current: the newest sub-goals are the ones that go missing from above. Zero
   damage right now, which makes this the calm moment to close it.

2. **G7.9** — `level3.py` should not prune quietly, and is misnamed
   (`view.py`/`main.py`). *The user has said they have more pieces of this in
   mind — **ask before starting**.* Its overlap with the old G7.10 part 4 is now
   resolved from that side: a refused publish no longer mutates first.

3. **G1.7** — the demotion path is four fields (`verdict`, `status`,
   `demoted_from`, `demote_reason`) and `evidence_gate` owns one. Reproduced
   live: a correctly-gated demotion left `status: proved` contradicting the
   demoted `verdict:` underneath. `shadow_decisive_verdicts` is 0 and is the
   regression alarm — it caught this once already, so leave it in.

4. **`grid.py commit` can drop a payload entry, silently.** Named during G7.10
   part 4 and deliberately left: it takes no `--engine-root`, so it resolves
   payloads against its own on-disk location and, finding nothing, records a
   version with the `payload` tree entry **missing**. Latent — `<project>/payloads/`
   wins resolution first, so it never fires in production — but
   `stitch.py --from-grid --grid-version N` materialises history out of exactly
   those refs, so the corruption would surface much later and far from its
   cause. Make it refuse loudly rather than write a truncated version.

5. **S21** — the graph can add a file to the engine but can never remove one.
   Filed 2026-08-29, not built. The publish path is one-directional for
   existence: nothing lets the graph say "this payload is retired, stop
   materialising it". **Deprecating a build node does NOT remove its engine
   file** — `stitch.py` reads `nodes/deprecated/build/` precisely so it keeps
   materialising those payloads, and that is correct. All four obvious routes
   fail differently; the node lists each with the code that decides it. **Do
   this before S18**, which ends in retiring files and cannot finish without it.

6. **S18** — absorb cavekit references before cavekit retires. The hazard is
   *ordering*: deleting `context/kits/` prunes 159 `origin: build-site` nodes
   (H0i). Gated on S21.

7. **G4.5** — generalize `blocked_by` -> `depends_on`. 89 populated nodes, 0
   cycles, max depth 15. Must stay out of every metric traversal or it becomes
   a fresh gaming surface.

Also named and deliberately unfixed: **gate 2 now certifies the tree as
*derived*, not as *published***, so a `payloads/` edit landing mid-run ships
bytes one derivation ahead of their contract. Strictly better than what it
replaced — the old ordering turned the same race into a refusal *plus* junk
nodes — and the next `:37` converges it.

**Do not "improve" `thought_coverage`.** Still the design at 12/792: absent
means empty, and fabricating reasoning after the fact is forbidden because a
made-up thought reads as evidence. Recovering real reasoning from stored
sessions is **G10.1**'s job.

## 5. Traps hit — do not re-learn these

- **A derivation change takes two publishes.** §2. The only one of these that
  will make you think you broke something.
- **`publish-engine.sh` no longer re-derives before it refuses** — that was
  G7.10 part 4 and it is fixed. If `git status` shows node files you did not
  touch after a *refused* publish, that is a regression, not the old normal.
- **A `@v2` node is the publish head, not the v1 node.** `grid.py commit --all`
  writes an edited payload to *every* node sharing that `payload_ref`, so both
  refs stay in sync — but **verify before publishing**, because the head is what
  ships: `grid.py payload 'build:<name>@v2' --out /tmp/x && diff`. The five
  `@v2` nodes are deprecated and still resolve as chain head.
- **A `how:` field embeds a line number**, so adding a comment block near the
  top of an engine file re-derives every contract entry below it. Expect a
  large, boring diff and one extra commit; it is not drift.
- **`level3.py` run from `payloads/` makes `payloads/` the engine root** and
  correctly refuses with "discover_files returned zero files". Use
  `--engine-root /home/ubuntu/work/agi --project /home/ubuntu/work/agi-tree`
  to exercise an unpublished change against the real graph.
- **`stitch.py` already imports `level3.py`,** so level3 borrowing the contract
  reader back was an import cycle and died with `RecursionError`. Ownership
  decides direction: level3.py owns the contract shape, stitch aliases it.
- **Inserting one sub-goal renumbers every goal after it.** `order` is unique
  and positional (`int`, duplicates are a hard error). Appending at the end
  costs nothing — S20 took order 83 after S19's 82 and renumbered zero nodes.
- **A test asserting a hole will fail when you close it.** Read each failure
  before fixing it — several were documentation of a defect, not regressions.
- **Whitespace normalisation is not `\s+`.** In `f"a:\n  b"` the `\n` is two
  source characters and the spaces after it are *content*. Collapsing `\s+`
  silently rewrites indentation inside string literals, in an engine whose main
  output is YAML and markdown. Collapse only runs that *contain* a real line
  break, and assert the quoted fragment is a verbatim substring of the payload
  rather than that it merely looks right.

## 6. How to write into this file — 🔴 SUPERSEDED BY `goal:g11`, DO NOT RUN

> **Retracted in the 2026-08-29b section above, which holds the current recipe.**
> Kept as written because it is what this session did, not what to do now. The
> block below calls **`grid.py checkout --all`, which is a NEVER-RUN command**
> — there is no staged copy left for it to materialise, and it silently
> reverted uncommitted work twice in one session (`goal:g4.1`).
> `publish-engine.sh` is retired for the same reason: nothing to publish into.

`HANDOFF.md` is `build:HANDOFF.md`, `build_kind: prose`. **Edit the payload.**
The `BUILD-CONTRACT` block and the derived prose around it are regenerated on
every scan; only a `THOUGHT` region would survive there (G2.10).

```bash
python3 agi/extensions/agi/bin/grid.py checkout --all   # payloads/HANDOFF.md
$EDITOR payloads/HANDOFF.md
python3 agi/extensions/agi/bin/grid.py commit --all
bash agi/extensions/agi/bin/publish-engine.sh
git add -A && git commit                                 # LAST
```

**The order matters and is not the obvious one.** `payloads/` is gitignored, so
`git add -A` finds *nothing* right after a payload-only edit, and a commit
attempted there silently does nothing while you believe your reasoning was
recorded. The node file only changes once `publish-engine.sh` re-derives its
contract from the published payload.

## 7. Known-good verification sequence

```bash
bash agi/extensions/agi/driver.sh --smoke --max-iters 1        # count must not drop
cd payloads && python3 -m pytest extensions/agi/tests/ -q      # 861 passed, 1 skipped
python3 agi/extensions/agi/bin/snapshot-goals.py --render --check
bash agi/extensions/agi/bin/publish-engine.sh --dry-run        # every gate, no writes
```
