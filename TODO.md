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

### F4. agi-tree working tree — DIRTY + 29,264 NODES MISSING FROM DISK — 🔴 BLOCKING
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

**Remaining working-tree state:** 5 modified, 5 untracked, 1 deleted (the intentional rename above). The 5 modified include `src/chain_engine/chains.py`, which is a **load-bearing fix** — see **H0d**.

**Still to do — resolve dirty tree and push:** commit the legitimate edits (especially `chains.py`), gitignore the cache artifacts (`nodes.db`, `.chain_cache.pkl`, `.claude/worktrees/`), create `CodexOperator/agi-tree` on GitHub, push `master`. Note the checked-out branch is `iter24-extend-300hop`, not `master`.

**Do not run the loop against this project yet** — blocked by **H0b** and **H0c**.

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
