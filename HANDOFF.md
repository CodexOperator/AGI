# HANDOFF — agi, for a fresh session on a new machine

> Two halves, and only one of them persists.
>
> **The bootstrap (§1-§3) is standing content.** Assumes **nothing** exists
> locally: no clone, no deps, no CLI, no auth.
>
> **The SESSION HANDOFF below is replaced wholesale by each director**, not
> appended to. Exactly one session section exists at a time. Prior ones live in
> the grid — `grid.py payload build:HANDOFF.md --version N` — and in git, so
> nothing is lost by replacing and accumulating would cost every future session
> context for no gain. Trimmed 2026-09-02 from 1,723 lines and six sections.

**Where the knowledge actually lives, so this file does not restate it:**

| Question | Read |
|---|---|
| What is agi, and why is it shaped this way? | `skills/agi/SKILL.md` |
| What is committed to, and what is being worked on now? | `GOALS.md` (rendered from `nodes/goal/`) |
| What does the repo contain, and how do I run the loop? | `<tree>/CLAUDE.md` |
| What does any given engine file do? | its build node — `nodes/build/*.md`, one per file |
| What happened THIS session, and what is next? | the **SESSION HANDOFF** section below — there is exactly one, and it is current |
| What happened in an EARLIER session? | `grid.py payload build:HANDOFF.md --version N`. Prior sessions are not kept in this file. |

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

node_count  874      active 867   deprecated 7    goals 105
outcome_coverage ~0.28  evidence_fraction ~0.21   unevidenced_decisive 1
goals: active 10  horizon 61  retired 2  complete 32
tests       1215 pass
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
