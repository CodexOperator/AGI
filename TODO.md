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
2. **Structural:** make the driver's project-override opt-in — require an explicit `"allow_local_script_overrides": true` in `agi-tree.config.json`, or version-stamp plugin scripts and refuse an override older than the plugin's.
3. **Defense in depth:** no snapshot path should ever `rmtree` the node corpus. Guard against deleting more than N% of existing nodes in one run absent an explicit `--force-rebuild` flag.
4. **Regression test:** seed a temp project with agent-origin nodes (no `origin` frontmatter), run the full driver, assert node count unchanged.

**Related:** handoff line 192 described this as *"seed hypothesis nodes get clobbered by snapshot each iter … Acceptable for now."* That framing badly understates it — it is total corpus deletion, not seed-node churn.

### H0b. Second stale project-local override: `render-context.py` — ✅ FIXED 2026-08-18
**Was:** with the node corpus intact, `~/.hermes/agi-tree/bin/render-context.py:162` raised `RecursionError` (~992 deep) inside `_longest_chain_length`. Same class as H0 — a stale project-local copy shadowing the plugin, predating commit `59d31e26` ("iterative `find_chains()` kills recursion limit"). Invisible while `nodes/` was wiped to 158; restoring the corpus surfaced it.

**Fix applied:** renamed to `bin/render-context.py.STALE-DO-NOT-USE`, so the plugin's iterative version wins. `~/.hermes/agi-tree/bin/` now contains only `autoresearch-tree.sh` plus the two `.STALE-DO-NOT-USE` files.

**Still open — the general rule.** Treat *any* project-local `bin/*.py` as stale until proven otherwise; the override mechanism itself is the defect (H0 action 2 proposes making it opt-in, and L9 proposes an engine-version pin plus a drift warning). Audit `~/.hermes/belam-codex-modularnn-spike-viz/.../modularNN/` before running the loop there. `~/work/fantasia/` is clean — it ships no `bin/` overrides.

**Note:** agi-tree is still blocked by **H0c** (`find_chains` hang), so this alone does not make the loop runnable there.

### H0c. `find_chains()` does not terminate in practical time on the full corpus — ✅ FIXED 2026-08-21

**Fixed.** `chain_engine` was **promoted into the engine** at `extensions/agi/src/chain_engine/` (this also settles H0d — plugin `src` is inserted at `sys.path[0]` while project `src` is only appended, so the promoted copy shadows agi-tree's). `chains.py` traversal rewritten: single mutable path + `on_path` cycle guard (no per-step path copy), iterative `_can_reach_terminal` (no `RecursionError` on deep chains), and three keyword bounds — `max_path_len=512`, `max_chains=10_000`, `deadline_s=20.0`. On any cap it returns partial chains plus `WARN: find_chains truncated (<reason>)` on stderr; it never raises and never hangs. The wall-clock budget is shared fairly across idea roots (`remaining / roots_left`), which on the real corpus is the difference between 0 and 28 chains. Also fixed a latent bug: `_get_chain_cache_file` memoized the cache path in a module global, so the first `graph_dir` in a process captured the path for every later one.

**Verified on the real 29,422-node corpus (cold cache, parent-reproduced):**
| | Before | After |
|---|---|---|
| Render stage | hang, killed at 300 s (exit 124), no output | **15.6 s cold / 2.0 s warm**, exit 0 |
| Output | none | 200-line ASCII, INJECTION.md written |
| Chains | none | 28 chains, longest 502 hops, deadline-truncated |

Tests: `extensions/agi/tests/test_chain_engine.py` (18) + `tests/chain_engine/` (21 ported from agi-tree, pass unmodified).

**Note:** the blowup is driven by the `spawns_edges` fallback (max fan-out 1001), not `next_edges` — `next_edges` alone traverses in ~0 s. So chain counts there are deadline-bound, not path-bound. Follow-up defect recorded as **H0e**.

<details><summary>original writeup</summary>

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

</details>

### H0e. A truncated `find_chains` result is cached and later served as complete — P1

**Found 2026-08-21 while verifying H0c.** When `find_chains` hits a bound it returns partial chains and warns — correct. But the partial result is then written to `.chain_cache.pkl` like any other result, and the cache is keyed only on node count + max mtime. Every subsequent run reads the truncated answer back and prints **no warning at all** (parent-reproduced: the warm run on the agi-tree corpus emits nothing). A partial answer becomes indistinguishable from a complete one for the rest of the corpus's life.

This matters because chain counts feed metrics and attractiveness ranking — a silently-truncated corpus quietly under-reports forever, which is the same class of defect as H3 (numbers that look authoritative and aren't).

**Action:** persist a `truncated` flag + the reason alongside the cached chains; re-emit the warning on every cache hit. Consider refusing to cache truncated results at all — cheaper and harder to get wrong.

### H0d. `chain_engine` is project-side only; its `graph_dir` fix is uncommitted — ✅ RESOLVED 2026-08-21

**Both halves closed.** The `graph_dir` parameter is committed in agi-tree (working tree verified clean), and the ownership question is settled the way H0d's option 1 proposed: `chain_engine` is now **engine code**, promoted to `extensions/agi/src/chain_engine/`. Confirmed by import test that the plugin copy shadows agi-tree's. agi-tree's copy was deliberately left in place and untouched — retiring it is a separate, deliberate step, not a side effect.

<details><summary>original writeup</summary>

#### H0d (original). `chain_engine` is project-side only; its `graph_dir` fix is uncommitted — P1
**Finding:** `chain_engine/` exists **only** in `~/.hermes/agi-tree/src/`, not in the plugin. The plugin's `bin/render-context.py:36-40` imports `find_chains` inside a `try/except ImportError` and falls back to `None`.

The plugin calls `find_chains(g, graph_dir=str(nodes_dir))`, but agi-tree's **committed** `chains.py` has no `graph_dir` parameter → `TypeError: find_chains() got an unexpected keyword argument 'graph_dir'`. The **uncommitted working copy** does have `graph_dir: str | None = None`. So that pending edit is load-bearing for the plugin's render path and will be lost if the working tree is ever discarded.

**Action:**
1. Commit `~/.hermes/agi-tree/src/chain_engine/chains.py` — it is a fix, not scratch work.
2. Decide ownership: either promote `chain_engine` into the plugin (`extensions/agi/src/chain_engine/`) so the engine is self-contained, or formalise it as a documented project-supplied interface with a version check. Current implicit-optional-import coupling is fragile.

</details>

### H1. DB-only state migration (drop `.md` state files) — P0
**Rationale:** Today the loop emits `nodes/{type}/*.md` files (frontmatter+markdown) and `sessions/iter-NNN/*.json` manifests. These are racey on concurrent writes, scattered across multiple dirs, and not queryable. `extensions/agi/src/graph_core/persistence/sqlite_backend.py` (278 lines) and `extensions/agi/src/graph_core/db_loader.py` (173 lines) already exist as scaffolding — promote them to the canonical persistence layer and drop the filesystem backend from the hot path.
**Evidence:** sqlite_backend.py + db_loader.py exist; cavekit-deferred-todo R2; user's stated long-term direction ("no more state files at all"); `extensions/agi/scripts/migrate_to_sqlite.py` exists as one-shot migration tool.
**Action:** Wire sqlite_backend into the snapshot/render/dispatch path. Add a `--state-backend sqlite|filesystem` flag during transition. Deprecate filesystem backend after one full iter cycle on sqlite.

### H2. Parse `~/.hermes/agi-tree/nodes/{type}/*.md` into the DB — P1
**Rationale:** agi-tree has 157 nodes accumulated across ~365 commits to iter 37. They're useful research artefacts that should populate the unified DB so the loop has prior-art context when re-running. Currently they live as filesystem-only frontmatter+markdown.
**Evidence:** `~/.hermes/agi-tree/nodes/{hypothesis,idea,task,experiment,verdict,mvp,outcome}/*.md`; cavekit-deferred-todo R2.
**Action:** Build a one-shot importer (`extensions/agi/scripts/import_agitree_nodes.py`) that reads each frontmatter file, validates against schema_registry, and writes via sqlite_backend. Idempotent — re-run safe.

### H3. Replace `longest_chain_length` primary metric — ✅ DONE 2026-08-21 (one config migration outstanding)

**Engine side done.** Metric computation moved out of the untestable `driver.sh` heredoc into `extensions/agi/bin/metrics.py`. All 7 original `METRIC` lines emit identical values (parent-verified against the deleted heredoc), plus:

- `evidence_fraction` — asserting verdicts (everything but `pending`) carrying `evidence_runs >= 1`. **This is the H3/H4 bridge:** it moves only when experiments actually run, and no amount of added hops shifts it. `pending` is excluded from the denominator on purpose, so honest uncertainty isn't penalised.
- `decisive_evidence_fraction`, `unevidenced_decisive_verdicts` (alarm counter — must be `0`), `evidence_weighted_depth` (= `avg_chain_depth × evidence_fraction`), `primary_metric` / `primary_value`.

`DEFAULT_METRIC_PRIMARY = "outcome_coverage"` is the fallback when config omits it — never chain length. `longest_chain_length` is listed in `GAMEABLE_METRICS`; naming it primary emits `METRIC_WARNING gameable_primary=…`. A test reproduces the actual attack: appending 30 hops moves `longest_chain_length` and leaves `evidence_fraction` flat.

**🔴 Outstanding — migrate `~/.hermes/agi-tree/autoresearch-tree.config.json`.** It still declares `"metric_primary": "longest_chain_length"`, `"metric_unit": "hops"`, **and `attractiveness_weights.length: 0.4` — the highest weight, which actively rewards the same gaming.** Should become `metric_primary: outcome_coverage`, `metric_unit: fraction`, `longest_chain_length` demoted to `secondary_metrics`, weights rebalanced off `length` — i.e. match `fantasia/autoresearch-tree.config.json`, which migrated already. Do this **before** any agi-tree run. Until then the engine warns every iteration.

<details><summary>original writeup</summary>

**Rationale:** Agents proved the metric is gameable via shortcut chains (`hops=2*cycle+8`); 2000 hops on 9 chains achieved with no real research signal. Composite metric (chain_depth × evidence_fraction) or evidence-fraction-only is harder to game.
**Evidence:** `~/.hermes/HANDOFF-autoresearch-2026-05-01.md` line 29; `~/.hermes/agi-tree/autoresearch-tree.config.json` declares the metric.
**Action:** Edit `agi-tree.config.json` schema (or wherever metric is declared); implement composite metric in `extensions/agi/bin/snapshot-build-site.py` (or wherever metrics are emitted); migrate all live projects' configs.

</details>

### H4. Orphan-verdict gate (require `evidence_runs > 0`) — ✅ DONE 2026-08-21

**The gate is out of the parent's head and into code** (which is what L4 asked for). `extensions/agi/bin/evidence_gate.py` is shared by **both** writer paths — `cli.py done` and `post_wire.py` (both its update-existing and create-verdict branches).

**Behaviour: demote, not hard-fail.** A non-zero exit would discard the expensive part (the experiment and write-up) to punish the cheap part (a wrong label). So `proved` → `inconclusive_lean_proved:50`, `disproved` → `inconclusive_lean_disproved:50`, exit 0, node kept, stamped `demoted_from` + `demote_reason` so every demotion is greppable and reversible. Hard-fail stays reserved for a malformed verdict (taxonomy violation → exit 2). Parent-verified matrix:

```
proved                ev=0 → inconclusive_lean_proved:50      DEMOTED
proved                ev=1 → proved                           pass
disproved             ev=0 → inconclusive_lean_disproved:50   DEMOTED
pending               ev=0 → pending                          pass
inconclusive_lean_*:N ev=0 → unchanged                        pass
```

`evidence_runs` is inferred from the target node's frontmatter when the flag is omitted, so a kid that ran a real experiment isn't demoted for forgetting a CLI flag. Escape hatch `--no-evidence-gate` exists for the H2 historical importer (157 agi-tree nodes whose evidence predates the field); it prints `EVIDENCE-GATE BYPASSED`, stamps `evidence_gate: bypassed`, and every such node is counted in `unevidenced_decisive_verdicts` so bypasses cannot hide. `SKILL.md` review step 4 updated — parent-link resolution and orphan rejection are still by hand.

<details><summary>original writeup</summary>

**Rationale:** 99.7% of verdicts in the agi-tree run were orphaned (created without backing experiment evidence). The loop self-aware-flagged it (commit `67ead2f0`) but the gate isn't in the writer path. Without this, `proved`/`disproved` verdicts are noise.
**Evidence:** `~/.hermes/HANDOFF-autoresearch-2026-05-01.md` line 26 (`67ead2f0`).
**Action:** In `extensions/agi/bin/cli.py done` command, reject verdict creation unless `evidence_runs >= 1`. Permit `pending` and `inconclusive_lean_*` without evidence.

</details>

### H4b. `driver.sh` calls `benchmark.py` with the wrong arguments — P2

**Found 2026-08-21 in passing.** `driver.sh` step 4 runs `benchmark.py "$PROJECT_ROOT"`, but that script's argparse expects a `chain_id`. The call is masked by `|| true`, so the pre-dispatch benchmark has been silently failing on every iteration rather than emitting attractiveness scores. Pre-existing, unrelated to H3/H4, deliberately not fixed in that pass.

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

### H9. Kid→parent question channel for the pi dispatch path — P2
**Rationale:** CC-dispatch kids can escalate judgment calls mid-task (SendMessage to main; four triggers + one-question budget — see `skills/agi/SKILL.md` §"Escalation — kid → parent"). The pi path has no equivalent: `dispatch.py` is fire-and-forget and `heal.py` only kills/replaces. Unattended weak-model runs are exactly where a wrong silent judgment call is most likely, so parity matters — but blocking a subprocess on a question conflicts with fire-and-forget, so the design is the work.
**Evidence:** CC-DISPATCH.md escalation section (commit `2ee9c5d`); first live CC run 2026-08-18 (fantasia): three kid judgment calls, all handled decide-and-document, protocol added kid-initiated stop/resume on top.
**Action (design open, pick one):**
1. *Poll-based:* agent writes `question.json` beside `agent.json`; `heal.py` (already polling every 30s) detects it, pauses the timeout clock, and either (a) surfaces it to the loop log for a human, or (b) dispatches a one-shot answerer agent (config `parent_model`) whose reply is written to `answer.json` for the kid to poll.
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

**Design ethic (governs every item here).** Emitted tokens are an agent's motion; injected context is its sensation; context growth makes motion heavier. Every capability exists to keep agent bodies light. Sprint one node hard, rest, let the graph carry the marathon. Mundane operations — and the small errors they breed — are the system's job to absorb, never the agent's. Full statement: `skills/agi/SKILL.md` §"Why this machinery exists".

**Applies to this doc too:** these entries get read by agents at spawn time. Keep them dense. An item that can't be acted on without opening three other files is badly written.

### L0. Status check — what actually exists today

Recorded 2026-08-18 so later readers don't re-litigate it.

| Capability | State |
|---|---|
| Zoom axis | **BIG/SMALL only.** `bin/zoom.py --level big\|small`. No numeric axis. |
| Model tiering | **Described, not built.** `SKILL.md §"The three tiers"`. Now specified as fully custom + three-tier (delegator/parent/kid) — see L3. |
| H4 evidence gate | **Built and enforced in code** (2026-08-21) — `bin/evidence_gate.py`, applied by both writer paths (`cli.py done`, `post_wire.py`). Demotes rather than hard-fails. See H4. |
| Goal nodes | **Built** (2026-08-21) — `bin/snapshot-goals.py` derives `nodes/goal/*.md` from `GOALS.md`. Linked by `parents: [goal:gN]`. See L15. |
| Goal-fulfillment scoring | **Still a proxy.** `evidence_fraction` (H3) answers *was the work real*; goal **attribution** — *did it count* — is L4 and is unbuilt. The goal nodes L4 needs now exist. |
| Chain finding | **Bounded** (2026-08-21) — `chain_engine` promoted into the engine; caps + deadline, degrades to partial output. See H0c. Caveat: truncated results are cached and re-served silently — H0e. |
| IO maps | **Do not exist.** |
| CC-native dispatch | **Largely built** — `skills/agi/SKILL.md`, validated on a live 6-iteration run. See L12. |
| Git grid | **Built** — `bin/grid.py`, refs namespace, cron sync (H10). |
| Per-agent condensed injection | **Built; the silent whole-graph fallback bug is fixed** (2026-08-18) — see L7. |

### L0a. The goal system EXISTS — it lives project-side, in `fantasia` — ✅ DECIDED

**Correction (2026-08-18).** An earlier draft of this entry claimed no goal system existed. Wrong — it was looked for in `agi` and `agi-tree` only. It lives in the **project** repo:

**`~/work/fantasia/GOALS.md`** — root goals with `status:` (`active` / `horizon` / `phasing-out` / `complete`). Seed nodes in `nodes/idea/` reference goals by id. Chains are scored on progress toward them via `metric_primary: outcome_coverage` (fraction of chains reaching a real outcome) in `fantasia/agi-tree.config.json` — note fantasia has **already moved off the gameable `longest_chain_length`**, which now sits in `secondary_metrics`.

**Updated 2026-08-21:** fantasia's goals are now `G1, G3..G7` — **G2 was removed.** G2 ("persistent ideation system with zoom levels") was engine work parked in a game repo: all seven of its capabilities are L1–L7 of this file. Its goal section, seed node, and full evidence chain were deleted from fantasia and the substance merged here — the measurements into L1, the contract-slice requirement into L2, the cheap-tier boundary into L3. **The G-numbering is deliberately left with a gap**; renumbering would break every node that references a goal by id. This is also the shape of the L8 rule in practice: a project holds goals about *its own domain*, and engine goals live in the engine's repo.

**Goal lifecycle, as practiced:** each long-term goal is a build tree. Retire by marking the section `status: phasing-out` and **deprecating — never deleting** its seed node; a phased-out goal's tree is marked `complete`, or is retired node by node as other nodes absorb its function. **Retired chains remain prior art.** That is the mechanism L5 formalizes.

**Decision: goals are project-side artifacts.** Confirmed by the user 2026-08-18, and already validated in production by fantasia. The engine stays domain-free — which is exactly what makes L9 (forkability) possible.

**What's actually missing is engine support:**
1. `outcome_coverage` is a *proxy* — it counts chains reaching an outcome, not their **attribution to a specific goal**. True goal-fulfillment scoring (L4) is still unbuilt.
2. Goal `status` transitions are a human convention in Markdown; nothing reads or enforces them (L5).
3. Nothing validates that a seed node's goal reference resolves to a real goal id — an orphaned reference fails silently.

**Cleanup — resolve the name collision.** `graph_builder.parse_goals()` (`extensions/agi/src/agi_algos/graph_builder.py:491`) parses a *different* `goals/` directory into `goal`-type nodes for the hermes 35-node-type **code** graph. Its call site (`:2579`) hardcodes `<hermes_dir>/belam-codex/goals`, **a path that no longer exists**, so it returns 0. It is dead code and unrelated to `GOALS.md`. Repoint it or delete it — two different things named "goal" in one codebase will mislead every future reader.

**`agi-tree` has no goals** and no `GOALS.md`. It predates the pattern; its last substantive work is the 2000-hop chain extension that produced H3 and H0c. If `agi-tree` is to keep being worked, it needs its own `GOALS.md` — otherwise its chains are unscoreable.


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

🔴 **That invariant is already falsified for the free-form implementation — measured, not suspected.** Evidence migrated here from fantasia's G2 chain (`hyp:zoom-roundtrip-claim-loss-r1` → `exp:zoom-roundtrip-recall-haiku-r1` → `verdict:zoom-loss-hits-contracts-not-prose-r1`, `inconclusive_lean_proved:80`, `evidence_runs: 6`), which was engine research living in a game repo; the chain was deleted there when its goal moved to this file.

**Protocol.** Two subjects, ground-truth claim lists and scoring rule locked before any decomposition ran. Each round trip used two *different* cheap (haiku) agents with no shared context: one decomposed a node into 3–6 children, a second — given only the children file — reconstructed a single node. 12 agents, 6 complete round trips, 111 claim-instances. Doubles as the L3 model-tiering demo: expensive orchestration, cheap zoom ops.

| category | recall |
|---|---|
| description (prose) | **0.792** |
| dependencies | 0.778 |
| invariant citations | 0.267 |
| file paths | 0.111 |
| structured frontmatter | **0.000** (0/24 — every field, every trial, both subjects, zero variance) |
| **overall** | **0.441** against a 0.90 bar |

**Three things to carry forward:**
1. **Loss is category-structured, not uniform.** Prose survives; node identity is destroyed outright. A round-tripped node cannot be identified as the node it came from.
2. **It is not a capacity problem.** The children were *longer* than the parents — the cheap agents were expanding, not compressing, and still lost 56% of claims. More context will not fix it.
3. **The mechanism is understood.** A parent-level universal ("*every* chain landing code must respect SPEC.md §V") reliably attaches to exactly one of six children, at which point the summarizer correctly reads it as that child's local detail and drops it. Neither agent misbehaves. The loss is a compounding artifact of the decompose/resummarize *shape*.

**Design consequence — zoom is not a view operation as prototyped; it is a lossy transform.** To make it behave like a view, the contract-bearing parts must not pass through the model at all. A child node = **(a)** mechanically inherited frontmatter plus a contract slice, attached by the harness, **(b)** model-authored prose. Only (b) ever round-trips through a summarizer. That splits cleanly across L2 (the contract slices) and L3 (what the cheap tier is allowed to touch).

**Held back from `proved`, and the limits matter:** the dependency leg came in at 0.778 — statistically indistinguishable from prose, so a named conjunct failed; its post-hoc rescue ("dependencies survived because the dependency list *was* the decomposition axis") is a new hypothesis, not a tested result. One model tier, one prompt shape, two thin subjects, single rater who also authored the ground truth. **Precision was never scored** — a reconstruction inventing plausible-but-false contracts would have scored identically, which for a contract layer is at least as dangerous as loss.

**The raw artifacts are kept** at `context/refs/zoom-roundtrip-ground-truth/` — claim lists, scoring rule, and all 6 children/reconstruction pairs. They were gitignored in fantasia (machine-local, at risk); they are tracked here because the follow-up A/B is only cheap if this exact baseline survives.

**Next node, when L1 is picked up:** *mechanically inherited contract slices restore round-trip fidelity without a smarter model.* Cheap and directly comparable — ground truth, scoring rule and baseline all exist. Pre-register: metadata recall 1.00 by construction, citations and paths ≥ 0.90, prose unchanged near 0.79. Pre-register the live falsifiers too: prose recall *drops* because the structural scaffold crowds out the summarizer, or citations die anyway because a summarizer discards inherited fields it did not author. Add a third dense subject whose dependency list is deliberately *not* the decomposition axis, and score precision this time.

Levels 4–5 aren't primarily for authoring — they're for **debugging** and for **recombining records into zoom-level-specific fine-tuning data** (train a small model to operate well at exactly one level; see L3).

Level 3's stitch-to-directory capability is the load-bearing one: it's what makes the graph an executable artifact rather than a description of one. Build it first; treat the other levels as projections around it.

### L2. Live IO maps — P1
Every node declares **required inputs** and **promised outputs**. Each entry carries:
- **how/why** it's needed or produced,
- a **performance note** (e.g. sluggish parsing risk),
- a **security note** (e.g. potential vulnerability).

IO maps **re-derive when neighbors change**, so decomposing a node never orphans its contracts. This is the mechanism that keeps L1's decompose/rollup honest — contracts are what survive a zoom change.

**L1's evidence promotes this from nice-to-have to load-bearing.** "Decomposing a node orphans its contracts" is no longer a worry with a hand-waved fix; it is an observed mechanism with a measured rate (invariant citations 0.267, file paths 0.111, frontmatter 0.000). The requirement that falls out: IO maps and invariant citations must be **explicitly inherited slices of the parent's contract set, attached to children mechanically by the harness, never restated by a decomposer.** At 0.00 frontmatter recall there is no prompt-tuning fix worth trying first — the field has to leave the model's hands entirely.

### L3. Model tiering — fully custom, three-tier — P1 (blocked on L1 for per-level assignment)

**Not a fixed ladder — a config the user sets and experiments with.** Specify the model for the parent and for the kids independently, and run different combinations to find what works for a given project and zoom level. Nothing hardcoded.

**Three tiers, not two:**

| Tier | Role | Runs as |
|---|---|---|
| **Delegator** | The main chat the user actually sees. Holds user intent, coordinates **several parent/kid groups** at once, reports progress back to the user. | The user's session |
| **Parent** | Owns one loop: picks zoom targets, spawns kids, reviews their nodes, enforces the evidence gate, commits the iteration. | **A subagent**, separate from the main flow |
| **Kid** | One node per iteration, bounded zoom scope. | Subagent spawned by a parent |

**Default: the parent is a subagent, not the main flow.** This keeps the user's own context light — parent work (reviewing every node, running the gate) is exactly the kind of motion that should not accumulate in the chat the user is reading.

**Exception, deliberately supported:** when the user's flow *is* the run — they want progress reported directly, or they're feeding run-specific instructions in as it goes — the overarching model acts as parent itself. Make this an explicit mode, not an accident.

**Why the delegator tier matters:** it's what lets several parent/kid groups run concurrently against different goals, coordinated in one place. That is the user-facing half of L6 (recursive sub-loops) — L6 supplies the scheduling and the shared iteration budget, L3 supplies who runs what.

Half-specified already in `SKILL.md §"The three tiers"` for the BIG/SMALL case. Once L1 lands, extend the config to one tier per zoom level, each level reviewed at the level above. Pairs with L1's per-level fine-tuning data — the long game is a level-specialized small model per tier.

**Tiering is not refuted by L1's zoom evidence — its price is now a number.** Prose recall of 0.792 from a haiku tier is precisely what a cheap tier is *for*. What that chain refutes is handing the cheap tier the **contract layer** (frontmatter 0.000, paths 0.111, citations 0.267). Tiering survives if the zoom operation is split in two: **the model authors prose, the harness moves structure.** Assign tiers per zoom level accordingly — no tier, however cheap, should ever be the thing that carries node identity across a decomposition.

### L4. Goal-fulfillment scoring — P0
Score chains by **contribution to goals**, never raw chain length (H3: hop count proven gameable; H0c: that gaming produced graph structure which broke the render path). Verdicts require experiment evidence (H4).

Move the H4 gate out of the parent's head and into `cli.py` so both dispatch paths enforce it. Depends on L0a's goal-location decision.

### L5. Goal rotation — P1

Swap or phase out goals without invalidating history. **The convention already exists and is practiced** — `fantasia/GOALS.md` defines it: mark the section `status: phasing-out`, **deprecate (never delete)** the seed node, mark a finished goal's tree `complete`, and let retired chains stand as prior art. A goal can also retire node by node as other nodes absorb its function.

What's missing is that **nothing reads or enforces any of it** — `status:` is a human-maintained Markdown field today. Build: parse goal status, stop accruing score to `phasing-out`/`complete` goals while keeping their chains attributable, and validate that every seed node's goal reference resolves to a real goal id (orphaned references currently fail silently).

Depends on L4 for the scoring side.

### L6. Recursive sub-loops for goal concurrency — P2

How many goals are worked at once is a knob. **`cc_dispatch.max_goals_active` already exists** — `fantasia/autoresearch-tree.config.json` sets it to `3`, alongside `iterations_per_run`, `kids_per_iter`, and `kid_model`. Nothing reads it yet.

*(Correction to an earlier draft of this entry: it claimed `cc_dispatch.*` would be an invented second namespace and should fold into `agent_dispatch.*`. Wrong — both exist and the split is deliberate: `agent_dispatch.*` configures the pi runtime, `cc_dispatch.*` the Claude Code runtime. One namespace per runtime is correct; keep them.)*

Mechanism: **agi loops spawn agi sub-loops** — one inner loop per goal/subtree, an outer loop scheduling across goals. Nesting is also how zoom granularity stays hierarchical: an inner loop owns one level.

**Budget invariant:** inner-loop completions count as iterations against a **single global iteration budget**, so the budget bounds total work regardless of nesting depth. Without this, recursion is unbounded.

The user-facing half of this is L3's delegator tier — the delegator is what coordinates several parent/kid groups across active goals.

### L7. Per-agent condensed graph injection — P1 (⚠️ bug ✅ FIXED 2026-08-18)
Every dispatched agent receives a condensed ASCII map showing **which part of the long-term thoughtgraph it occupies** and its task for this run. Built: `bin/zoom.py` → `sessions/iter-NNN/<agent>/context.md`, cached renderers.

Design intent — instant swarm awareness: *"this is a swarm action, do my part and move on"* / *"glad to be part of this, not on the hook for the whole thing."* Payoff already measured: embedding the map dropped kids from 11–13 tool calls to 5–7 (`SKILL.md §"Field notes"`).

**✅ Fixed: small zoom never actually bounded anything.** `zoom.py` added only the *project's* `src` to `sys.path`, never the plugin's — so on any project without its own `src/graph_core` (the normal case) the `graph_core` import always failed, and three separate `except` branches each returned the **entire INJECTION.md**. Every kid silently received the whole graph: the exact opposite of intent, and squarely against the design ethic.

Two changes:
1. `_add_graph_core_to_path()` inserts `PLUGIN_ROOT/src`, with the project's `src` taking precedence only when it actually contains `graph_core` — matching `driver.sh`'s documented override convention.
2. The three silent fallbacks now raise `ZoomUnavailable`, which `main()` reports on stderr and exits 1. `dispatch.py:128` runs zoom with `check=True`, so this surfaces as a real failure instead of a context bomb delivered to a kid. **Refusing to serve an unbounded context is the correct behavior** — falling back to the whole graph defeats the feature.

**Measured on `~/work/fantasia` (27-node graph), same target node:**

| | context.md |
|---|---|
| Before | **73 lines** (whole INJECTION.md + fallback header) |
| After | **22 lines** (bounded subtree, 2 hops) |

Tests: 176 passed, 1 pre-existing known fail (`test_field_set_is_exactly_six`) — no regression. On a 29k-node corpus the difference is far larger; this was silently inflating every kid's context on every run.

### L8. One repo or two — **keep them separate for now** — P2, decision deferred

Original proposal: fold `agi-tree` into `agi` via a `refs/tree/*` namespace, mirroring `grid.py`'s `refs/grid/*`.

**Open-source / paywall constraint changes the answer. Facts:**

1. **GitHub visibility is per-repository.** Not per-directory, per-branch, or per-ref. There is no way to make part of one repo public and part private. A `refs/tree/*` namespace would give **clone-weight control, not access control** — the moment the repo goes public, every ref in it goes public.
2. **Git history is permanent.** Folding `agi-tree` in means its full 29,422-node history rides along forever. At open-source time you'd be filtering or squashing history under pressure — precisely when mistakes are expensive.
3. **One wrong flag leaks everything.** With both in one repo, a single `git push --mirror` or `--all` to a public remote publishes the private graph. Separate repos make that failure impossible rather than merely unlikely.

**Decision: keep `agi` and `agi-tree` as separate repos while their intended visibility differs.** Revisit `refs/tree/*` only if both end up with the same visibility — at which point it becomes a clean optimization rather than a risk.

**This costs nothing.** The `fantasia` pattern (L9) already proves separate repos compose fine: the engine is a gitignored drop-in clone inside the project, and neither repo's history touches the other.

**If you want partial visibility later, the real options are:**
- **Two repos** — engine public, data/research private. (Current shape. Recommended.)
- **Submodule** — public repo references a private submodule; users without access simply can't fetch it. Adds friction for contributors.
- **Public mirror** — private repo of record, plus a curated public repo built from filtered history. Most control, most maintenance.

Paywall-then-open-source works cleanly with any of these: the engine is the thing with reuse value, and it's already the piece with no private data in it.

### L9. Forkability — let anyone grow their own tree — P2

**The project-layout question is already answered, and `fantasia` is the reference implementation.** Verified 2026-08-18:

```
~/work/fantasia/                     ← the project repo (CodexOperator/fantasia)
  GOALS.md                           long-term goals (G1, G3..G7) with status:
  agi-tree.config.json               metric_primary: outcome_coverage
  nodes/                             the graph (27 nodes)
  context/  sessions/                generated / gitignored
  SPEC.md  src/  test/               the game itself
  agi/                               ← GITIGNORED drop-in clone of CodexOperator/agi
```

`fantasia/.gitignore` carries exactly the right comment:
```
# agi research-loop engine (drop-in clone of CodexOperator/agi — never commit here)
agi/
```

**So: a project repo contains data and configuration, never engine code.** Concretely — `GOALS.md`, `agi-tree.config.json`, `nodes/`, project-specific node types / schema extensions, and the project's own source. The engine arrives as a gitignored clone (later: a versioned install). That is all the flexibility a project needs: new node types are *schema*, which is configuration, not code.

**This is why the engine must never be vendored** — H0/H0b proved that stale project-local *scripts* silently destroyed 29,264 files. A gitignored clone can be `git pull`ed; a committed copy diverges forever.

🔴 **Gap found: the clone is unpinned and silently stale.** `fantasia/agi` sits at `2923cef`, behind canonical `master`. Nothing declares which engine version the project expects, and nothing warns on drift. **Action:** record an engine version/commit in `agi-tree.config.json` and have `driver.sh` warn (not fail) when the running engine doesn't match. Cheap, and it closes the whole staleness class that H0/H0b belong to.

**Remaining forkability work:** an `agi init` that scaffolds a project (config, `nodes/`, `GOALS.md` template, grid refs) so the fantasia layout is reproducible without copying by hand.

**Recursive tree creation is the interesting case.** A tree per task domain: an OpenClaw/hermes agent keeps a tree for getting smarter and tracking memories, and that tree spawns child trees for specific personas it finds useful. Individual skills, plugins, and MCP servers can each own a tree.

Highest-value application: **AI "experts" that compound** — agents that get sharper the longer they're exposed to your workflow. That's why recursion matters here, not novelty.

### L10. Let the human peek — P2
Two capabilities:
1. **Ride along as a kid.** Load the kid experience and see the exact context injection a kid receives on arrival — the fastest way to judge whether briefs are genuinely self-contained.
2. **ASCII dashboard.** The graph rendered friendlier: nodes as rounded-off squares, plus a **live count of active agents and where each is working**, across all zoom levels at once.

### L11. Rename `overseer` → `parent` — ✅ DONE 2026-08-18 (scripting-away still open)

*(The original request said `supervisor`; that term appeared nowhere. The codebase term was `overseer` — 16 occurrences.)*

**Done:** all 16 renamed — `skills/agi/SKILL.md` (via the L14 merge), `TODO.md`, `extensions/agi/bin/grid.py`. `git grep overseer` now returns only these entries describing the rename itself. The config key `parent_model` replaces the proposed `overseer_model` in H9. `kid` already matched.

The rename isn't cosmetic — it sets the intended relationship (caring, responsible-for) over the supervisory one, and it lines up with L3's delegator/parent/kid tiers.

**Where this is tracked (decided 2026-08-21):** it stays a TODO entry for now — **no goal node yet.** The candidates were fantasia's G2 (cheap, but tracks engine work inside a game repo) or bootstrapping `agi` as its own project with its own `GOALS.md`. The latter is HANDOFF §4's "real dogfood milestone" and interacts with **L8** (one repo or two), so the where-do-engine-goals-live question is deferred until L8 is settled rather than answered by accident. The machinery to make it a goal node the moment that lands now exists (L15).

**Still open — cut the parent's machine-tending to near zero.** A parent should spend motion on the *kids*, never on the computer. Concretely: rendering a kid's map with `zoom.py` and then hand-pasting it into the spawn prompt should be **one command that renders and spawns**. `SKILL.md` now states the general rule — any repeated, mechanical step gets scripted away, and manual handles need a written reason — but the spawn command itself is not built.

### L12. Claude Code as a first-class runtime — P1 (largely done; finish it)
**Already built, don't rebuild:** `skills/agi/SKILL.md` defines CC-native dispatch — Claude Code subagents as builder kids, same graph/node format/chain workflow, parent owns review + commit, validated on a live 6-iteration run. Kid→parent escalation is specified (four triggers, one question per kid per iteration). Model tiering per kid. Healing analogue for API-error deaths.

**Remaining:**
- Anywhere the engine invokes `pi`, allow invoking a Claude Code instance instead — a runtime flag, not a parallel code path.
- Hook parity audit: confirm every pi hook has a CC equivalent. **If any gap turns up, report it and plan together rather than improvising.**
- Fold in L11's one-command spawn so the CC path stops feeling manual.

### L13. Drop the history, describe the present — ✅ MOSTLY DONE 2026-08-18

**Done:** `skills/agi/SKILL.md` was rewritten from scratch in the L14 merge — no `autoresearch-tree` repo references, no davebcn references, no fold narrative, no "Two repos, two purposes". It keeps exactly the history that changes present behavior: the stale-override lesson (as a safety rail), the metric-gaming lesson (as the reason not to optimize chain length), and the quota-scrub rationale.

**Still open:**
- `README.md` and `HANDOFF.md` still carry fold-era framing. HANDOFF is legitimately a migration document, so it can keep more; README should be rewritten to describe the present system.
- ✅ **Config key + env var renamed 2026-08-21** — canonical names are now `agi-tree.config.json` and `$AGI_TREE_PROJECT_ROOT`, matching the repo. Done with the compatibility window this entry asked for: every engine entry point resolves the canonical name first and falls back to the legacy one, and `driver.sh` / `cc-session-start.sh` / `agi-bridge` export **both** env spellings, so a project on an older engine clone still works. Covered by `test_find_project_root_accepts_canonical_and_legacy_config`. Removing the legacy fallback is a separate, later decision — see **L16**.

### L14. One skill, CLI-first — ✅ DONE 2026-08-18

**Merged** `SKILL.md` (318 lines) and `CC-DISPATCH.md` (194) into a single `skills/agi/SKILL.md` of **215 lines** — 58% smaller than the 512 it replaces. `CC-DISPATCH.md` deleted; all references across `TODO.md` and `HANDOFF.md` repointed to `SKILL.md` sections.

Landed in the same pass, as planned (all three touched the same two files):
- **L14** — one skill, opening with a CLI table where every loop capability is a named command.
- **L11** — `overseer` → `parent` throughout, plus the delegator/parent/kid tiers from L3.
- **L13** — stale `autoresearch-tree` / davebcn / fold references stripped.
- **Metric framing replaced** — the old skill actively taught "longest-chain-wins", the very metric H3 proved gameable. It now says never to optimize chain length, explains why (2000-hop shortcut chains, and the render breakage that followed), and points at goal-attributable metrics.

Also corrected: frontmatter `name: autoresearch-tree` → `name: agi`.

Preserved in full: the design ethic, the four escalation triggers, the DONE contract, verdict-taxonomy judgment guidance, grid usage, and the validated field notes.

The only remaining `autoresearch-tree` strings in the skill are the literal config filename, which is L13's scheduled breaking change.

### L15. Goals become first-class nodes in `nodes/goal/` — ✅ DONE 2026-08-21

**Built as recommended — the `build-site.md` → `task` pattern, reused verbatim.** `extensions/agi/bin/snapshot-goals.py` derives `nodes/goal/<gid>-<slug>.md` from `GOALS.md`, stamped `origin: goals-doc`, with H0-safe incremental upsert and origin-guarded prune. `GOALS.md` stays the human-authored source of truth. Wired into `driver.sh` as step 1a — **plugin-only, with no project-local override lookup**, because that override mechanism *is* the H0 data-loss defect and must not be extended to new scripts.

**Open question 1 settled — parent-pointing, and no new frontmatter field.** A node joins a goal by putting the goal id in its existing `parents:` list (`parents: [goal:g2]`). `render-context.py` already turns `parents` into `spawns` edges, so rendering and traversal came free. `snapshot-goals.py` only *reads* those pointers to compute each goal's `seeds:` list.

**Open question 2 dodged, deliberately.** Goal→idea is a `spawns` edge only; **no `next_edges` are emitted and chain shape is untouched.** The canonical-chain extension (`goal → idea → …`) that would ripple through `chain_engine` remains a separate, deliberate piece of work — exactly as this entry warned.

**Referential integrity** is live: a `goal:`-prefixed parent that resolves to no goal prints `INTEGRITY: <file> references unknown goal '<id>'`. Exit stays 0 by default (the loop must never break on it); `--strict` exits 1.

**Safety:** a missing/renamed `GOALS.md` is a no-op that prunes **nothing** — it must never be able to wipe the goal corpus. Status values are *not* enum-enforced: unknown values are preserved verbatim with a stderr warning. **Updated 2026-08-21:** `horizon` — fantasia's G3 — was adopted into the taxonomy rather than warned about, since "declared, not yet being worked" is exactly the queued state L5 rotation needs and `max_goals_active` (3) already implies. Taxonomy is now `active | horizon | phasing-out | complete`; pass-through coverage moved to a genuinely unknown value.

**Verified end-to-end on a fantasia copy** (not just unit tests): edges 12 → 19 (+7, one per goal→seed), `by type: … goal=7 …`, ASCII 33 → 40 lines. 12 tests in `extensions/agi/tests/test_snapshot_goals.py`. Project side: fantasia's 7 seed ideas now carry `parents: [goal:gN]`, mapping verified 1:1 against each seed's own body text.

**Two follow-ups noticed while building:**
- **G2's seed under-describes G2.** `idea:goal-zoom-level-granularity` covers the zoom axis, IO maps, model tiering and scoring, but not goal rotation (L5), recursive sub-loops (L6), or per-agent condensed injection (L7). Harmless today; the moment L4 scores by attribution, G2 will look under-served because its seed under-claims. Extend the seed *before* L4 lands.
- **`nodes/task/t-011-guild-hub-menu-lobby.md`** has `parents: []` and prose tying it to G3/G7. Left unlinked on purpose — attaching a `task` node directly to a goal is a chain-shape decision, not a data fix.

<details><summary>original writeup</summary>

**Goals are the baseline every chain grows from, so they belong in the graph — not only in prose.** Today `fantasia/GOALS.md` holds G1..G7 as Markdown, and `nodes/` has one directory per type (`idea`, `hypothesis`, `experiment`, `verdict`, `mvp`, `outcome`, `task`) — **no `goal/`**. Seed ideas reference goals by id in text, which nothing validates and nothing can traverse.

**Target:** `nodes/goal/<goal-id>.md`, same frontmatter convention as every other type, so goals get ids, edges, rendering, and traversal like anything else.

**Recommended mechanism — reuse the pattern that already exists.** `snapshot-build-site.py` parses `build-site.md` into `task` nodes stamped `origin: build-site`, and prunes only nodes carrying that stamp. Do exactly the same for goals: `GOALS.md` stays the human-authored source of truth, and snapshot derives `nodes/goal/*.md` stamped `origin: goals-doc`. This gets three things for free:
- the H0-safe incremental upsert and origin-guarded prune (agent-authored nodes are never touched),
- edit-in-Markdown ergonomics — you keep writing goals in prose,
- one direction of truth, so the doc and the nodes can't silently diverge.

**What becomes possible once goals are nodes:**
- **L4 scoring by attribution** — a chain's contribution is measured along real edges to a real goal node, instead of the `outcome_coverage` proxy.
- **L5 lifecycle enforcement** — `status: active | phasing-out | complete` becomes a node field the engine reads, rather than a human convention in Markdown.
- **Referential integrity** — a seed node pointing at a nonexistent goal id fails loudly instead of silently.
- **L1 zoom level 1** — the skill-tree view is literally "render the goal nodes and their descendants." Goals are what level 1 *is*.
- **Rendering** — goals appear in the ASCII map and the L10 dashboard as roots, so an agent can see what it's ultimately serving.

**Open questions to settle when building:**
- Do goal nodes carry `next_edges` into their seed ideas, or do seed ideas carry `parents: [goal:G1]`? Parent-pointing matches how the rest of the graph already works.
- Chain-validity rules currently expect chains to start at `idea`. Extending the canonical chain to `goal → idea → hypothesis → …` touches `chain_engine` and every chain-shape assumption — plan that deliberately rather than as a side effect.
- `agi-tree` has no goals at all; giving it a `GOALS.md` is a precondition for its chains ever being scoreable.

</details>

### L16. Close the `agi-tree.config.json` compatibility window — P2 (do not rush)

**Landed 2026-08-21:** the config marker is `agi-tree.config.json` and the env var is `$AGI_TREE_PROJECT_ROOT`, matching the repo name so setup reads as one thing rather than two. The legacy `autoresearch-tree.config.json` / `$AUTORESEARCH_TREE_PROJECT_ROOT` still resolve everywhere, and writers emit **both** env spellings.

**Why the fallback stays for now.** A project directory and the engine clone inside it version independently (see L9, and the unpinned-clone gap in L8). Dropping the legacy name would break exactly the projects whose engine clone is stale — the H0/H0b staleness class again, arriving through a different door.

**Close it only after all three hold:**
1. Engine version is pinned and checked (the L8 action: record the expected engine commit in the config, warn on drift). Without that, there is no way to know which projects would break.
2. Every live project has been migrated and its config renamed.
3. The engine has emitted a deprecation warning on legacy-name resolution for at least one full release cycle — **the warning does not exist yet; adding it is step one of this entry**, and it belongs in `lib/find-root.sh` plus the four Python entry points that resolve the config.

**Do not remove the fallback as a cleanup pass.** It is load-bearing until (1) exists.

### L17. Project config as the whole customization surface — P1

**The rename made the intended shape legible, and it should now be enforced.** A project owns `GOALS.md`, `agi-tree.config.json`, `nodes/`, and its own source. The engine arrives as a clone and is never edited per-project. Everything a project needs to differ — metrics, dispatch, timeouts, model tiering, schema extensions, node types — is *configuration*, written programmatically into its own `agi-tree.config.json`.

**This is the structural fix for H0.** The data-loss defect was project-local `bin/` scripts silently overriding engine scripts; the surviving override handles in `driver.sh` and `hooks/cc-session-start.sh` are still live. Config-as-only-surface is the principle that removes the *need* for script overrides, which is what makes deleting them safe rather than merely strict.

**Build order:**
- **Schema for the config.** There is none — every reader does `cfg.get(...)` with an inline default, so a typo'd key fails silently as a default value. A declared schema (with defaults in one place) is a precondition for anything writing configs programmatically.
- **A writer.** `agi-tree config set <key> <value>` / an init command that scaffolds a valid config for a new project. Today the only way to make one is by hand, which is precisely the mundane motion `SKILL.md` says to script away.
- **Then** make script overrides opt-in behind an explicit config key (the H0 structural action, TODO line ~63) — by then the escape hatch has a legitimate alternative.

### L18. The ideation stage — a project that is only a GOALS.md — P1

**Already works:** goal nodes derive from **every** goal regardless of status. `snapshot-goals.py` warns on an unrecognized status but never filters on one, so fantasia's `G3 — status: horizon` is a real node today (`nodes/goal/g3-…md`, `seeds: [idea:goal-agent-marketplace-pop]`). A `horizon` goal is a first-class part of the graph the moment it is written down — that is the point of the state.

**The gap is earlier than that: you cannot start a project from goals alone.** There is a stage before any skill tree exists — goals are being drafted by hand or through the skill workflow, and the graph should already be usable as an ideation surface. fantasia is *past* this stage; a new project has to get through it, and right now it can't.

**Reproduced on a bare project** (`GOALS.md` + `agi-tree.config.json`, nothing else):

| Step | Result |
|---|---|
| `snapshot-goals.py` | ✅ 2 goal nodes written |
| `render-context.py` | ✅ INJECTION.md, ASCII map, `by type: goal=2` |
| `metrics.py` | ✅ emits, `primary_value=0.0` |
| **`driver.sh --smoke`** | 🔴 **aborts** — `ERR: build site not found: context/plans/build-site.md` |

Every piece works. Only the driver refuses, and it refuses *before* render and metrics, so the project gets no map at all.

**Root cause is a one-line asymmetry between the two snapshot scripts.** `snapshot-goals.py:239` treats a missing `GOALS.md` as a safe no-op (`print(… skipping); return 0`) with a comment explaining why. `snapshot-build-site.py:141` treats a missing `build-site.md` as `sys.exit(1)`, and `driver.sh` runs under `set -euo pipefail`, so that one exit kills the iteration. A build site is a *later-stage* artifact; requiring one to render a graph inverts the order of work.

**Actions:**
1. **Make the build site optional.** Missing `build-site.md` → skip with a note, exactly as the goals path does. This alone unblocks the whole stage; it is the smallest possible change and the highest-value one here.
2. **`agi-tree init`.** Scaffold `agi-tree.config.json` (valid defaults, from L17's schema), `nodes/`, and a commented `GOALS.md` skeleton. Today the only way to start is to hand-write a config, which is precisely the mundane motion `SKILL.md` says to script away. This is L17's "a writer" seen from the other end — build them together.
3. **Name the stage in `SKILL.md`.** A project is usable at three depths: goals only (ideation), goals + seed ideas (chains starting), goals + build site (execution). Agents should know a goals-only project is a legitimate state and not a broken one.

**Why it's worth doing before more engine features:** it is the only thing standing between "I have an idea" and "the loop is running on it," and it is also how the engine gets tested against a project that isn't fantasia.

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
