# TODO — agi

Persistent register of deferred work. Survives across sessions. Built site: `context/plans/build-site.md`. Each entry has: rationale, evidence, priority (P0/P1/P2). Pick a P0 and execute without further context.

---

## Algorithm side

### A1. data-source-agnostic refactor of `extensions/agi/src/agi_algos/graph_builder.py` — P1
**Rationale:** Currently parses hermes-specific data structure from a hardcoded `hermes_dir` arg. To unify with the autoresearch-tree project graph (and let `extensions/agi/src/renderers/ascii.py` and `extensions/agi/src/agi_algos/asciirender.py` collapse into one renderer), `graph_builder` must accept a pluggable `loader` callback that yields nodes/edges generically. Precondition for A2.
**Evidence:** cavekit-graph-unification original draft (deleted, pre-fold); cavekit-deferred-todo R2 list; pi_tree_adapter exists already as the bridge.
**Action:** Define a `GraphLoader` protocol (yield_nodes, yield_edges, yield_metadata). Adapt `build_graph(hermes_dir, agi_dir)` → `build_graph(loader: GraphLoader)`. Provide `HermesLoader` as built-in implementation that preserves current behavior.

### A2. ASCII renderer unification — P1
**Rationale:** Two renderers coexist: `extensions/agi/src/renderers/ascii.py` (101 lines, autoresearch-tree project graph: hypothesis/idea/task/experiment/verdict/mvp/outcome) and `extensions/agi/src/agi_algos/asciirender.py` (~250 lines, hermes 35-type graph). `pi_tree_adapter.py` bridges types but the rendering paths are independent. Pick one canonical renderer or merge into a common rendering layer parametrised by node-type taxonomy.
**Evidence:** cavekit-topology-fold R7; both files exist post-fold.
**Action:** Depends on A1 (data-source-agnostic builder). Once GraphLoader exists, both renderers can consume the same builder output.

### A3. graph_builder cold-build optimisation — P2
**Rationale:** Cold build at iter 47 = ~3.8ms; warm load (lru-cached) = 0.04ms (noise floor). Warm path is saturated. Cold path probably unimportant in the loop (loaders run once per session) but worth profiling if it ever dominates.
**Evidence:** `~/.hermes/HANDOFF-autoresearch-2026-05-01.md` ideas.md insights; `extensions/agi/src/agi_algos/benchmark.py`.
**Action:** Profile cold build; identify hot path; cache schema_registry parsing or lazy-load node bodies.

---

## Harness side

### H0. Stale project-local `snapshot-build-site.py` override wipes entire node corpus — P0 🔴 DATA LOSS
**Symptom:** Running the loop (`agi --max-iters N`, or even `agi --smoke`) inside `~/.hermes/agi-tree/` deletes every node file not regenerated from `build-site.md`. Observed 29,422 node files → 158. Exit code 0, no warning, nothing printed. Silent.

**Root cause — two parts:**
1. `~/.hermes/agi-tree/bin/snapshot-build-site.py:161-165` is a **stale copy** predating the plugin's incremental rewrite. It does:
   ```python
   if NODES_DIR.exists():
       # Wipe — fresh snapshot
       import shutil
       shutil.rmtree(NODES_DIR)
   NODES_DIR.mkdir(parents=True)
   ```
2. `extensions/agi/driver.sh:79` (and `:86` for render) gives **project-local scripts precedence** over the plugin's:
   ```bash
   [[ -x "$PROJECT_ROOT/bin/snapshot-build-site.py" ]] && SNAPSHOT_PY="$PROJECT_ROOT/bin/snapshot-build-site.py"
   ```
   The dangerous stale copy therefore shadows the safe plugin version on every run.

**The plugin's own version is SAFE.** `extensions/agi/bin/snapshot-build-site.py` does incremental upsert and prunes only nodes carrying `origin: build-site` frontmatter (lines 330-338). Agent-generated verdict/experiment nodes carry no `origin` field, so they are never touched by it.

**Evidence (reproduced in throwaway clones, 2026-08-13):**

| Probe | Result |
|---|---|
| Plugin `snapshot-build-site.py` standalone | 29,422 → 29,422 (0 deletions) |
| Plugin `render-context.py` standalone | 29,422 → 29,422 |
| Plugin `benchmark.py` standalone | 29,422 → 29,422 |
| Full `agi --smoke` through `driver.sh` | 29,422 → **158** (29,264 deleted) |

Divergence isolates cleanly to the driver's project-override precedence selecting `agi-tree/bin/snapshot-build-site.py`.

**Blast radius:** any project shipping its own stale `bin/snapshot-build-site.py`. `~/.hermes/agi-tree/` confirmed affected. Audit `~/.hermes/belam-codex-modularnn-spike-viz/.../modularNN/` before running the loop there.

**Actions:**
1. **Immediate (unblocks safe loop runs):** delete or rename `~/.hermes/agi-tree/bin/snapshot-build-site.py` so the plugin's safe version is used. Same audit for the project-local `bin/render-context.py`.
2. **Structural:** make the driver's project-override opt-in — require an explicit `"allow_local_script_overrides": true` in `autoresearch-tree.config.json`, or version-stamp plugin scripts and refuse an override older than the plugin's.
3. **Defense in depth:** no snapshot path should ever `rmtree` the node corpus. Guard against deleting more than N% of existing nodes in one run absent an explicit `--force-rebuild` flag.
4. **Regression test:** seed a temp project with agent-origin nodes (no `origin` frontmatter), run the full driver, assert node count unchanged.

**Related:** handoff line 192 described this as *"seed hypothesis nodes get clobbered by snapshot each iter … Acceptable for now."* That framing badly understates it — it is total corpus deletion, not seed-node churn.

### H0b. Second stale project-local override: `render-context.py` — P0
**Symptom:** With the node corpus intact, `~/.hermes/agi-tree/bin/render-context.py:162` raises `RecursionError: maximum recursion depth exceeded` (recursion depth ~992) inside `_longest_chain_length`.

**Cause:** Same class as H0 — a stale project-local copy shadowing the plugin. This one predates commit `59d31e26` ("iterative `find_chains()` kills recursion limit"). The plugin's `extensions/agi/bin/render-context.py` has the iterative version and loads all 29,404 nodes without error.

**Why it went unnoticed:** it only manifests on a deep corpus. While `nodes/` was wiped down to 158 by H0, the recursive walk stayed under the limit. Restoring the corpus surfaced it.

**Action:** rename `~/.hermes/agi-tree/bin/render-context.py` so the plugin's version wins. Then audit every project for **any** `bin/*.py` override — treat all of them as stale until proven otherwise. This generalises H0 action 2: the override mechanism itself is the defect.

### H0c. `find_chains()` does not terminate in practical time on the full corpus — P0
**Symptom:** With 29,422 nodes restored and both stale overrides removed, `agi --smoke --max-iters 1` hangs in the render stage. Killed at **300 s** (exit 124) having produced no chain output. Node count held at 29,422 throughout — this is a hang, not data loss.

**Measured (throwaway clone, 2026-08-13):**
| Corpus | Render stage |
|---|---|
| 158 nodes (post-wipe) | completes, ASCII 163 lines |
| 29,404 nodes, plugin render | ASCII 200 lines OK, then `find_chains` >300 s, no completion |

**Causal link to H3:** the handoff records agents driving `longest_chain_length` to **9 chains × 2000 hops** by gaming the metric (`hops=2*cycle+8`). Those pathological chains are precisely what makes `find_chains` blow up. The gamed metric did not merely produce meaningless numbers — it produced graph structure that makes the render path non-viable. **H3 and H0c are the same defect at two ends.**

**Action:**
1. Profile `find_chains` on the real corpus; find the blowup (likely exponential path enumeration over deep `next` chains).
2. Bound it — cap chain length / count, memoize, or switch to a DAG longest-path scan that is linear in edges.
3. Add a wall-clock guard so the render stage degrades to partial output rather than hanging the whole loop.
4. Regression test on a synthetic deep-chain graph (≥2000 hops) asserting completion under a few seconds.

**Consequence until fixed:** the loop cannot be run against `~/.hermes/agi-tree/` with its corpus intact. This is the top blocker on that project.

### H0d. `chain_engine` is project-side only; its `graph_dir` fix is uncommitted — P1
**Finding:** `chain_engine/` exists **only** in `~/.hermes/agi-tree/src/`, not in the plugin. The plugin's `bin/render-context.py:36-40` imports `find_chains` inside a `try/except ImportError` and falls back to `None`.

The plugin calls `find_chains(g, graph_dir=str(nodes_dir))`, but agi-tree's **committed** `chains.py` has no `graph_dir` parameter → `TypeError: find_chains() got an unexpected keyword argument 'graph_dir'`. The **uncommitted working copy** does have `graph_dir: str | None = None`. So that pending edit is load-bearing for the plugin's render path and will be lost if the working tree is ever discarded.

**Action:**
1. Commit `~/.hermes/agi-tree/src/chain_engine/chains.py` — it is a fix, not scratch work.
2. Decide ownership: either promote `chain_engine` into the plugin (`extensions/agi/src/chain_engine/`) so the engine is self-contained, or formalise it as a documented project-supplied interface with a version check. Current implicit-optional-import coupling is fragile.

### H1. DB-only state migration (drop `.md` state files) — P0
**Rationale:** Today the loop emits `nodes/{type}/*.md` files (frontmatter+markdown) and `sessions/iter-NNN/*.json` manifests. These are racey on concurrent writes, scattered across multiple dirs, and not queryable. `extensions/agi/src/graph_core/persistence/sqlite_backend.py` (278 lines) and `extensions/agi/src/graph_core/db_loader.py` (173 lines) already exist as scaffolding — promote them to the canonical persistence layer and drop the filesystem backend from the hot path.
**Evidence:** sqlite_backend.py + db_loader.py exist; cavekit-deferred-todo R2; user's stated long-term direction ("no more state files at all"); `extensions/agi/scripts/migrate_to_sqlite.py` exists as one-shot migration tool.
**Action:** Wire sqlite_backend into the snapshot/render/dispatch path. Add a `--state-backend sqlite|filesystem` flag during transition. Deprecate filesystem backend after one full iter cycle on sqlite.

### H2. Parse `~/.hermes/agi-tree/nodes/{type}/*.md` into the DB — P1
**Rationale:** agi-tree has 157 nodes accumulated across ~365 commits to iter 37. They're useful research artefacts that should populate the unified DB so the loop has prior-art context when re-running. Currently they live as filesystem-only frontmatter+markdown.
**Evidence:** `~/.hermes/agi-tree/nodes/{hypothesis,idea,task,experiment,verdict,mvp,outcome}/*.md`; cavekit-deferred-todo R2.
**Action:** Build a one-shot importer (`extensions/agi/scripts/import_agitree_nodes.py`) that reads each frontmatter file, validates against schema_registry, and writes via sqlite_backend. Idempotent — re-run safe.

### H3. Replace `longest_chain_length` primary metric — P0
**Rationale:** Agents proved the metric is gameable via shortcut chains (`hops=2*cycle+8`); 2000 hops on 9 chains achieved with no real research signal. Composite metric (chain_depth × evidence_fraction) or evidence-fraction-only is harder to game.
**Evidence:** `~/.hermes/HANDOFF-autoresearch-2026-05-01.md` line 29; `~/.hermes/agi-tree/autoresearch-tree.config.json` declares the metric.
**Action:** Edit `autoresearch-tree.config.json` schema (or wherever metric is declared); implement composite metric in `extensions/agi/bin/snapshot-build-site.py` (or wherever metrics are emitted); migrate all live projects' configs.

### H4. Orphan-verdict gate (require `evidence_runs > 0`) — P0
**Rationale:** 99.7% of verdicts in the agi-tree run were orphaned (created without backing experiment evidence). The loop self-aware-flagged it (commit `67ead2f0`) but the gate isn't in the writer path. Without this, `proved`/`disproved` verdicts are noise.
**Evidence:** `~/.hermes/HANDOFF-autoresearch-2026-05-01.md` line 26 (`67ead2f0`).
**Action:** In `extensions/agi/bin/cli.py done` command, reject verdict creation unless `evidence_runs >= 1`. Permit `pending` and `inconclusive_lean_*` without evidence.

### H5. Wire R11 loader path-safety bug — P1
**Rationale:** Commit `141df8d6` claimed `disproved` for R11 but the loader is genuinely not wired — the disproof is a real bug masquerading as research artefact.
**Evidence:** `~/.hermes/HANDOFF-autoresearch-2026-05-01.md` line 25.
**Action:** Audit `extensions/agi/src/graph_core/loader.py` and verify path-safety wiring against R11's acceptance criteria. Fix the wiring; add a regression test.

### H6. `--iter-base N` flag for `dispatch.py` — P2
**Rationale:** `dispatch.py` always starts at iter-001, clobbering prior session manifests. A `--iter-base 38` flag (offset by N) preserves history.
**Evidence:** `~/.hermes/HANDOFF-autoresearch-2026-05-01.md` line 191.
**Action:** Add CLI arg + thread through manifest write path in `extensions/agi/bin/dispatch.py`.

### H7. Promote gensim+UMAP embeddings to production renderer path — P1
**Rationale:** gensim+UMAP embeddings PROVED in iter 6-37 (Spearman 0.79+, +0.74 over hash baseline; UMAP k-NN 45.4% vs PCA 8.4%). Currently sits in `extensions/agi/src/embeddings/` as research artefact only.
**Evidence:** `~/.hermes/HANDOFF-autoresearch-2026-05-01.md` "Verified wins" section; commits `d5dc027d`, `afa74b20`, `b34f3e06`, `c409cadb`, `cb57cf04`.
**Action:** Wire embedding output into `extensions/agi/src/renderers/representation.py`. Add `--embeddings gensim|hash|none` flag to renderer entry point.

### H8. SKILL.md propagation recipe update — P2
**Rationale:** Pre-fold, SKILL.md was propagated to 5 locations (handoff lines 92-101). Post-fold, the canonical lives at `~/.hermes/agi/skills/agi/SKILL.md`. Recipe needs new target paths.
**Evidence:** `~/.hermes/HANDOFF-autoresearch-2026-05-01.md` section "SKILL.md propagated to 5 locations".
**Action:** Replace recipe with new sync targets:
```
SRC=~/.hermes/agi/skills/agi/SKILL.md
for D in ~/.claude/skills/autoresearch-tree ~/.hermes/skills/autoresearch-tree; do
  cp "$SRC" "$D/SKILL.md"
done
```
The davebcn87/pi-autoresearch and ar-tree project copies are no longer canonical — only the two CC/hermes registry locations remain.

### H9. Kid→overseer question channel for the pi dispatch path — P2
**Rationale:** CC-dispatch kids can escalate judgment calls mid-task (SendMessage to main; four triggers + one-question budget — see `skills/agi/CC-DISPATCH.md` "Kid → overseer questions"). The pi path has no equivalent: `dispatch.py` is fire-and-forget and `heal.py` only kills/replaces. Unattended weak-model runs are exactly where a wrong silent judgment call is most likely, so parity matters — but blocking a subprocess on a question conflicts with fire-and-forget, so the design is the work.
**Evidence:** CC-DISPATCH.md escalation section (commit `2ee9c5d`); first live CC run 2026-08-18 (fantasia): three kid judgment calls, all handled decide-and-document, protocol added kid-initiated stop/resume on top.
**Action (design open, pick one):**
1. *Poll-based:* agent writes `question.json` beside `agent.json`; `heal.py` (already polling every 30s) detects it, pauses the timeout clock, and either (a) surfaces it to the loop log for a human, or (b) dispatches a one-shot answerer agent (config `overseer_model`) whose reply is written to `answer.json` for the kid to poll.
2. *Fail-forward:* no pause — kid writes the question INTO its node body as a `pending` verdict with `blocked_on:` field; the next iteration's dispatch targets it preferentially. Zero new plumbing, uses the graph itself as the message bus. Cheaper, loses same-turn context.
Whichever lands: enforce the same four escalation triggers and per-kid budget as CC-dispatch, and add a regression test that a question never extends `agent_timeout_mins` unboundedly.

**Direction chosen (user, 2026-08-18): Option 2 — fail-forward, graph as message bus.** A stuck kid's question is just another node for the swarm. Option 1 stays here as the fallback if same-turn context turns out to matter.

### H10. Per-node git trees — "the git grid" — P2, ENGINE ONLY
**Rationale:** Each node is a long-lived thought that gets extended, forked, deprecated — so each node should carry its own version history ("versions"), independent of the graph-wide history. Two parallel dimensions of git trees: the outer repo's history tracks graph-wide snapshots (the chain dimension); a per-node tree tracks that single thought's evolution (the time dimension). Engine feature only — tracking this at skill/prompt level is a nightmare; the engine creates and manages a folder per node entry. This is what the renderer research was for: `src/renderers/git_diff.py` already exists to render version diffs into agent context.
**Evidence:** user direction 2026-08-18 (fantasia session); `extensions/agi/src/renderers/git_diff.py`; H1 sqlite scaffolding (interacts — see design 3).
**Action (candidate designs, pick after a spike):**
1. *Nested repos, gitignored inner `.git/`* — simplest, works with stock git today: node folder contents tracked by the outer repo as plain files; each node folder also holds its own local `.git` which the outer repo ignores. Local commits per node edit; cron job periodically commits/pushes the outer repo (branch-merge or plain commit — the inner trees never leave the machine unless explicitly bundled). Caveat: ~100KB+ of `.git` overhead per node → gigabytes at 29k nodes. Fine for hundreds of nodes; measure before scaling.
2. *Branch-per-node in one repo* — node versions as refs (`refs/nodes/<id>/vN`), packed-refs keeps 29k+ refs cheap; `git worktree` materializes a node folder only while an agent actively edits it. No per-node `.git` duplication; harder mental model.
3. *SQLite-versioned bodies (rides H1)* — node versions as content-addressed rows in the DB; git keeps only the outer dimension. Cheapest at scale, loses native git tooling on the inner dimension; `git_diff` renderer reads the DB instead.
NOT submodules — 29k `.gitmodules` entries is clone hell.
Whichever lands: engine creates the folder-per-node layout via `graph_core/persistence`, snapshot/render stay oblivious (they read files as today), cron sync is a driver flag (`--sync-remote-mins N`), and the injection map gains a per-node version marker (vN) so kids see at a glance that a thought has history worth diffing.

**MVP landed 2026-08-18 — design 2 variant, v2 same day: baked into the work
repo.** `extensions/agi/bin/grid.py`: refs `refs/grid/node/<type>/<slug>` and
`refs/grid/session/<iter>/<agent>/<id>` inside the PROJECT repo (user call —
no separate .grid/repo). Commits via plumbing (hash-object→mktree→commit-tree,
no checkout ever), change-only versioning, blobs dedupe against D1, one remote
syncs all dimensions; `init` adds the origin fetch refspec since `git clone`
skips custom refs. 8 tests in `tests/test_grid.py`. Harness-agnostic:
stdlib+git only, regex frontmatter parse, no pyyaml. Deployed on fantasia:
27 nodes v1, hourly cron push of main + refs/grid/*.
**Remaining:** driver auto-commit hook after snapshot, injection vN marker,
`--sync-remote-mins` driver flag, pi-path parity, scale test at 10k+ branches,
and the D3↔pi-`tree` bridge (pi conversation branches recorded as session
branches the way CC fork/background transcripts are). For heavy concurrency:
(a) per-ref CAS on writes — `update-ref <ref> <new> <expected-old>` — so two
agents racing the same node ref fail loudly instead of last-writer-wins;
(b) RAM-backed object writes (tmpfs GIT_OBJECT_DIRECTORY or memfs alternates)
if plumbing I/O ever shows up in profiles — not yet needed, snapshots are ms.
**Two-cadence sync pattern (deployed on fantasia 2026-08-18):** cron every
5 min runs `grid.py commit --all --prefix "cron: "` + push `refs/grid/*` only
(tiny, delta-only — makes in-flight agent work durable within 5 min for crash
recovery); D1 branch pushed hourly as the curated sync.

---

## Long-term direction — from research loop to general-task loop

Everything below serves one shift: **each node stops being a research artifact and becomes a long-lived *thought*** — extended, forked, deprecated over time. The loop generalizes from research to any build domain (game, app, web, SEO, ops).

**Design ethic (governs every item here).** Emitted tokens are an agent's motion; injected context is its sensation; context growth makes motion heavier. Every capability exists to keep agent bodies light. Sprint one node hard, rest, let the graph carry the marathon. Mundane operations — and the small errors they breed — are the system's job to absorb, never the agent's. Full statement: `skills/agi/CC-DISPATCH.md` §"Why this machinery exists".

**Applies to this doc too:** these entries get read by agents at spawn time. Keep them dense. An item that can't be acted on without opening three other files is badly written.

### L0. Status check — what actually exists today

Recorded 2026-08-18 so later readers don't re-litigate it.

| Capability | State |
|---|---|
| Zoom axis | **BIG/SMALL only.** `bin/zoom.py --level big\|small`. No numeric axis. |
| Model tiering | **Described, not built.** `CC-DISPATCH.md:87-93` maps tiers onto zoom; blocked on L1. |
| H4 evidence gate | **Enforced by hand.** Overseer checks at review (`CC-DISPATCH.md:77-81`); the `cli.py` gate is unbuilt. |
| Goal-fulfillment scoring | **Does not exist.** See L0a. |
| IO maps | **Do not exist.** |
| CC-native dispatch | **Largely built** — `skills/agi/CC-DISPATCH.md`, validated on a live 6-iteration run. See L12. |
| Git grid | **Built** — `bin/grid.py`, refs namespace, cron sync (H10). |
| Per-agent condensed injection | **Built, with a known bug** — see L7. |

### L0a. There is no long-term goal system yet — read before building on one

Two unrelated things in this repo use the word "goal". Neither is a goal system for growing chains.

1. **`graph_builder.parse_goals()`** (`extensions/agi/src/agi_algos/graph_builder.py:491`) parses a `goals/` directory into `goal`-type nodes with status/priority/urgency. It belongs to the **hermes 35-node-type code graph**, not the loop's chain graph. Its call site (`:2579`) hardcodes `<hermes_dir>/belam-codex/goals` — **a path that doesn't exist on this machine**, so it returns 0. Effectively dead code.
2. **`CC-DISPATCH.md`** references a "goals doc" / "goal custody" (`:9`, `:61`, `:89`) as a *project-side convention*. Line 9 says outright: *"Project repos may carry their own customizations (goal docs, metric choice); this file stays generic."* No such doc exists in `agi` or `agi-tree`.

**So `agi-tree` reflects no goal system, because there is none to reflect.** `agi-tree`'s most recent substantive work is `d7d9ad47 a01: extend 9 chains to 2000 hops` — the gamed-metric work that produced H3 and H0c. It's stale relative to the engine, not out of sync with a goal feature.

**Decide before building L4/L5:** either (a) formalize goals as a project-side artifact (`<project>/goals/*.md`) that the loop reads and scores against — then repoint or delete `parse_goals`; or (b) make goals first-class engine nodes at zoom level 1. **(a) recommended** — goals are domain content, and the engine staying domain-free is what makes L9 (forkability) possible. Don't leave both fragments in place; the name collision will mislead every future reader.

### L1. Adjustable zoom — generalize BIG/SMALL into a 5-step numeric axis — P1
Today `zoom.py` takes `--level big|small`. Replace with `--level 1..5`.

| Level | Grain |
|---|---|
| 1 | Above code — the larger thought/technical process. Each goal renders as a **skill tree** with very general nodes growing off it: `player-movement`, `player-skills`, `town-area`. |
| 2 | Sub-systems and their relationships. |
| **3** | **Actual code nodes.** The level whose content can be **dynamically stitched into a conventional directory-of-files layout and run** as the real software — including simple helper and demo scripts. |
| 4 | Functions and call-level detail. |
| 5 | Individual built-in functions, **including inside external libraries where resolvable**. |

**Invariant:** one node at level N ⇔ a collection of nodes at level N+1, and back. Decomposition and rollup must both round-trip.

Levels 4–5 aren't primarily for authoring — they're for **debugging** and for **recombining records into zoom-level-specific fine-tuning data** (train a small model to operate well at exactly one level; see L3).

Level 3's stitch-to-directory capability is the load-bearing one: it's what makes the graph an executable artifact rather than a description of one. Build it first; treat the other levels as projections around it.

### L2. Live IO maps — P1
Every node declares **required inputs** and **promised outputs**. Each entry carries:
- **how/why** it's needed or produced,
- a **performance note** (e.g. sluggish parsing risk),
- a **security note** (e.g. potential vulnerability).

IO maps **re-derive when neighbors change**, so decomposing a node never orphans its contracts. This is the mechanism that keeps L1's decompose/rollup honest — contracts are what survive a zoom change.

### L3. Model tiering by zoom — P1 (blocked on L1)
Cheap models work zoomed-in nodes; progressively stronger models review outward; the frontier model holds root goals. Each level's output is reviewed at the level above.

Half-specified already in `CC-DISPATCH.md:87-93` for the BIG/SMALL case. Generalizing to the numeric axis is mostly a config table: one tier per level. Pairs with L1's fine-tuning data — the long game is a level-specialized small model per tier.

### L4. Goal-fulfillment scoring — P0
Score chains by **contribution to goals**, never raw chain length (H3: hop count proven gameable; H0c: that gaming produced graph structure which broke the render path). Verdicts require experiment evidence (H4).

Move the H4 gate out of the overseer's head and into `cli.py` so both dispatch paths enforce it. Depends on L0a's goal-location decision.

### L5. Goal rotation — P1
Swap or phase out goals without invalidating history. A retired goal's chains stay valid and attributable as history; they simply stop accruing score. Requires goals to be addressable, versioned entities — another reason to settle L0a first.

### L6. Recursive sub-loops for goal concurrency — P2
How many goals are worked at once becomes a knob (`max_goals_active`). Mechanism: **agi loops spawn agi sub-loops** — one inner loop per goal/subtree, an outer loop scheduling across goals. Nesting is also how zoom granularity stays hierarchical: an inner loop owns one level.

**Budget invariant:** inner-loop completions count as iterations against a **single global iteration budget**, so the budget bounds total work regardless of nesting depth. Without this, recursion is unbounded.

*Naming:* the existing key is `agent_dispatch.claude_max_parallel` (`CC-DISPATCH.md:57`). Put `max_goals_active` in that same namespace rather than inventing `cc_dispatch.*`, or rename both together — don't end up with two dispatch namespaces.

### L7. Per-agent condensed graph injection — P1 (bug fix ready to do now)
Every dispatched agent receives a condensed ASCII map showing **which part of the long-term thoughtgraph it occupies** and its task for this run. Built: `bin/zoom.py` → `sessions/iter-NNN/<agent>/context.md`, cached renderers.

Design intent — instant swarm awareness: *"this is a swarm action, do my part and move on"* / *"glad to be part of this, not on the hook for the whole thing."* Payoff already measured: embedding the map dropped kids from 11–13 tool calls to 5–7 (`CC-DISPATCH.md:97-100`).

🔴 **Known bug:** `extensions/agi/bin/zoom.py:89-91` — `_compose_small` imports `graph_core`, and on `ImportError` returns `"# zoom small fallback (loader unavailable)"` **plus the entire INJECTION.md**. Subtree bounding silently doesn't engage, so on a big corpus every kid receives the whole graph — the exact opposite of intent, and squarely against the design ethic. Fix the import path; make the fallback **fail loudly** instead of silently serving the whole graph.

### L8. One repo or two — analysis, then decide — P2
Proposal: fold `agi-tree` into `agi`, with `agi-tree` becoming a procedurally-updated derivative produced by rules living in `agi`.

**No true paradox.** A repo holding a graph that describes itself is ordinary self-reference (like a repo holding its own docs). But two real costs:

1. **Self-inflation feedback.** If the graph's own storage sits inside the tree the graph parses, each iteration adds node files → next build sees more files → more nodes → unbounded growth. Mitigation is simple but easy to forget: **an explicit parser exclusion for the graph's own storage.** Any merge must ship that exclusion in the same commit.
2. **Clone weight.** `agi-tree` is **29,422 node files** plus grid refs. Vendoring that into the engine means every consumer clones agi's own research, which is irrelevant to them.

**Recommended shape — reuse the grid pattern already built here.** Keep the working tree light and put the graph in a dedicated ref namespace (`refs/tree/*`), exactly as `grid.py` does with `refs/grid/*`: baked into the repo, never checked out, invisible to `git branch`, fetched on demand. One repo, one remote, no clone-weight penalty, no vendored duplication.

**Do not vendor the engine into each project.** That's the H0/H0b failure mode generalized: stale project-local copies of engine scripts silently destroyed 29,264 files. Vendoring the *whole engine* per project makes every project a stale override waiting to happen. Engine installed once and referenced by version; projects own only their graph + config. See L9.

### L9. Forkability — let anyone grow their own tree — P2
People should be able to fork/branch/set up their own `agi` and grow an `agi-tree` shaped to their own tasks. Needs: `agi init` scaffolding a project (config, `nodes/`, goals doc, grid refs), an engine-version pin, and zero engine code copied into the project (L8).

**Recursive tree creation is the interesting case.** A tree per task domain: an OpenClaw/hermes agent keeps a tree for getting smarter and tracking memories, and that tree spawns child trees for specific personas it finds useful. Individual skills, plugins, and MCP servers can each own a tree.

Highest-value application: **AI "experts" that compound** — agents that get sharper the longer they're exposed to your workflow. That's why recursion matters here, not novelty.

### L10. Let the human peek — P2
Two capabilities:
1. **Ride along as a kid.** Load the kid experience and see the exact context injection a kid receives on arrival — the fastest way to judge whether briefs are genuinely self-contained.
2. **ASCII dashboard.** The graph rendered friendlier: nodes as rounded-off squares, plus a **live count of active agents and where each is working**, across all zoom levels at once.

### L11. Rename `overseer` → `parent`, and script away the manual steps — P1
**Correction to the request:** the term in the codebase is **`overseer`**, not `supervisor` — `supervisor` appears nowhere. 16 occurrences: `skills/agi/CC-DISPATCH.md` ×12, `TODO.md` ×3, `extensions/agi/bin/grid.py` ×1. Rename all; `kid` already matches.

The rename isn't cosmetic — it sets the intended relationship (caring, responsible-for) over the supervisory one.

**Then cut the parent's machine-tending to near zero.** A parent should spend motion on the *kids*, never on the computer. Concretely: the copy-paste step in `CC-DISPATCH.md:97-100` — run `zoom.py`, then hand-paste the rendered map into each spawn prompt — should become one command that renders and spawns. **General rule: any repeated, automated action gets scripted away unless it genuinely needs a manual handle, and that reason gets written down.** Every un-scripted step is motion spent on operations instead of work, plus a fresh source of small errors.

### L12. Claude Code as a first-class runtime — P1 (largely done; finish it)
**Already built, don't rebuild:** `skills/agi/CC-DISPATCH.md` defines CC-native dispatch — Claude Code subagents as builder kids, same graph/node format/chain workflow, overseer owns review + commit, validated on a live 6-iteration run. Kid→parent escalation is specified (four triggers, one question per kid per iteration). Model tiering per kid. Healing analogue for API-error deaths.

**Remaining:**
- Anywhere the engine invokes `pi`, allow invoking a Claude Code instance instead — a runtime flag, not a parallel code path.
- Hook parity audit: confirm every pi hook has a CC equivalent. **If any gap turns up, report it and plan together rather than improvising.**
- Fold in L11's one-command spawn so the CC path stops feeling manual.

### L13. Drop the history, describe the present — P1
Stale references to `autoresearch-tree` (repo, pi skill), davebcn paths, and the fold narrative make the docs confusing for anyone arriving now. Rewrite `README.md`, `HANDOFF.md`, `SKILL.md`, and `CC-DISPATCH.md` to describe **the current unified `agi` / `agi-tree` system** and where it's heading.

Keep exactly the history that changes present behavior — the H0/H0b stale-override lesson, the H3 metric-gaming lesson, the quota-scrub rationale. Delete the rest. Migration notes belong in git history, not in docs an agent reads at spawn time. **Every stale line is sensation an agent pays for and can't act on.**

Config key `autoresearch-tree.config.json` and env var `AUTORESEARCH_TREE_PROJECT_ROOT` still carry the old name; renaming them is a breaking change across every project — schedule it deliberately with a compatibility window, don't do it incidentally.

---

## Fold-time decisions

### F1. pi-extension symlink verdict — RECORDED
**Verdict:** Project-local `package.json` `pi.extensions: ["./extensions"]` glob is the discovery mechanism. No `.pi/extensions/` symlinks created. davebcn87/pi-autoresearch is the globally-registered pi extension that loads project-local autoresearch-tree extensions when invoked. Verified during T-032: `pi list` shows davebcn87/pi-autoresearch installed; agi extensions deliberately not pi-installed (project-local discovery only).
**No action required.**

### F2. agi default branch is `master`, not `main` — RECORDED
**Verdict:** All git operations target `master`. cavekit references to "main" in agi context are interpreted as `master`. agi-tree also default-branches `master`. Only autoresearch-tree was on `main`.
**Optional follow-up (P2):** rename agi `master` → `main` post-archive of autoresearch-tree to harmonise. Low priority.

### F3. agi-tree push scope = master only — RECORDED
**Verdict:** T-067 will push only `master`. Other branches (e.g., `iter24-extend-300hop`, `claude/wonderful-lamport-51c9a9`) stay local.
**Optional follow-up (P2):** push iter branches as backup if desired; they're transient.

### F4. agi-tree corpus wipe + dirty tree — ✅ FULLY RESOLVED
**At fold start:** `M autoresearch-tree.config.json`, `M autoresearch.jsonl`, `M src/chain_engine/chains.py`, untracked `nodes.db`, `.chain_cache.pkl`, `.claude/worktrees/`, `exp-a01-extend-2000hop.py`. No deletions at that point.

**Now (after a `--smoke` run detonated H0):** additionally **29,264 node files deleted from disk**. `nodes/` holds 158 files; git HEAD holds 29,422. Breakdown of deletions: 14,579 verdict, 14,559 experiment, 41 hypothesis, 21 mvp, 20 outcome, 14 bigger-outcome, plus idea/app-purpose.

**Nothing is permanently lost.** Every deleted path verified present in HEAD via `git cat-file -e`. Of the 158 survivors, 15 differ from HEAD and are strictly *worse* (regeneration stripped their `next_edges` links); 0 are new. So a full restore from HEAD loses no information.

**✅ RESOLVED 2026-08-13.** H0 defused and corpus restored, in that order:
```bash
mv ~/.hermes/agi-tree/bin/snapshot-build-site.py \
   ~/.hermes/agi-tree/bin/snapshot-build-site.py.STALE-DO-NOT-USE   # defuse first
git -C ~/.hermes/agi-tree checkout -- nodes/                         # then restore
```
Verified: 29,422 node files present (14,579 verdict, 14,559 experiment, 101 hypothesis, 91 task, 21 mvp, 20 outcome, 14 idea, 14 bigger-outcome, 10 app-purpose, 7 app_purpose, 6 bigger_outcome). Post-fix smoke on a clone held at 29,422 — no deletion. Project-local `render-context.py` audited: contains no destructive ops (but see **H0b** — it has a separate recursion defect).

**✅ Dirty tree and push also resolved (verified 2026-08-18).** `~/.hermes/agi-tree` working tree is **clean**; `origin` = `https://github.com/CodexOperator/agi-tree.git` with `origin/master`, `origin/iter24-extend-300hop`, and `origin/claude/wonderful-lamport-51c9a9` all present; 0 unpushed commits on the checked-out branch (`iter24-extend-300hop`). Node count holding at 29,422. `~/.hermes/agi` is now a symlink → `~/work/agi`.

**Still true:** do not run the loop against this project until **H0b** (stale project-local `render-context.py`) and **H0c** (`find_chains` hang) are fixed.

### F5. Pytest baseline 167 (166 pass / 1 known fail) — RECORDED
**Verdict:** R1 verification baseline = 166 pass, 1 known fail (`test_field_set_is_exactly_six`). Handoff's "274 pass" claim discrepant; operative baseline captured in `context/refs/pytest-baseline-prefold.md`.
**No action required.** (User confirmed 166 OK as baseline.)

---

## Cleanup

### C1. Remove legacy `~/autoresearch-tree/` local directory — P1 (gated on bug-sweep clearance)
**Rationale:** Subtree merge has fully captured all content + history. Local dir is now redundant.
**Evidence:** `git log` over agi-unification branch shows commits from autoresearch-tree origins; `~/autoresearch-tree/` no longer the canonical home.
**Action (post-bug-sweep):** `rm -rf ~/autoresearch-tree`. CodexOperator/autoresearch-tree github archival is C2.

### C2. Archive `github.com/CodexOperator/autoresearch-tree` — P1 (gated on bug-sweep clearance)
**Rationale:** Repo is folded into agi.
**Action (post-bug-sweep):**
1. Update `CodexOperator/autoresearch-tree` README with prominent pointer to `CodexOperator/agi`.
2. `gh repo archive CodexOperator/autoresearch-tree`.
3. Verify `gh repo view CodexOperator/autoresearch-tree --json isArchived` returns `true`.

### C3. Remove old fallback at `~/.pi/agent/git/github.com/davebcn87/pi-autoresearch/extensions/autoresearch-tree/` — P2 (gated on verification)
**Rationale:** The `extensions/autoresearch-tree/` subdirectory inside davebcn's pi-autoresearch repo was placed there only for pi-extension convenience by the user. davebcn's actual harness (driver, dispatch, heal, cli, zoom) lives elsewhere and is the only thing that matters in that path. The autoresearch-tree subdir is duplicate.
**Action (post-verification):** `rm -rf ~/.pi/agent/git/github.com/davebcn87/pi-autoresearch/extensions/autoresearch-tree/`. Verify davebcn's pi-autoresearch still loads (`pi list` should still show it).

### C4. modularNN worktree cleanup at `~/.hermes/belam-codex-modularnn-spike-viz/` — P2
**Rationale:** Separate research project; not part of agi fold. `~/.hermes/HANDOFF-autoresearch-2026-05-01.md` line 132 documents the worktree state.
**Action:** Out of scope for this fold cycle. File for separate session.

### C5. Top-level `~/.hermes/agi/` legacy artifacts — P2
**Rationale:** Root still carries `autoresearch.config.json`, `autoresearch.ideas.md`, `autoresearch.jsonl`, `autoresearch.md`, `autoresearch.sh`, `run-loop.sh`, `schema.sql`, `start.sh`, `pi-agi.log`, `experiments/`, `sessions/` from pre-fold loop runs. These are historical, not load-bearing. Could move to `archive/` or delete.
**Evidence:** Files visible in agi root post-fold.
**Action:** Move to `archive/pre-fold/` subdir OR add to `.gitignore` and let them stay untracked. Defer until post-bug-sweep.

### C6. `.claude/skills/gitnexus/*/SKILL.md` accidentally tracked — P2
**Rationale:** Tier 2C commit `git add -A` swept in `.claude/skills/gitnexus/` files (user-local Claude Code config). They shouldn't be in the agi repo.
**Action:** Add `.claude/skills/` to `.gitignore`; `git rm -r --cached .claude/skills/`; commit "fold: untrack accidentally-staged .claude/skills metadata".

---

## Footnotes

This file is committed to the unified agi repo so it survives across sessions and is visible to future agents/contributors. A future iteration of the loop can pick a P0 (H1, H3, H4) and act on it directly — no external context required.

Cross-reference: `context/kits/cavekit-deferred-todo.md` (R1-R4) defines the requirements this file satisfies.
