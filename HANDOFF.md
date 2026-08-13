# HANDOFF — agi, for a fresh session on a new machine

> Self-contained. Assumes **nothing** exists locally: no clone, no deps, no CLI, no auth.
> Written 2026-08-13. Repo state: `CodexOperator/agi` **private**, default branch `master`, 118 commits, 266 tracked files.

---

## 0. TL;DR

`agi` = **Artificial Graph Intelligence**. One repo holding two things that used to be separate:

1. **Graph algorithms** — build a graph from a codebase, query it, render it as ASCII, benchmark it.
2. **A research loop harness** — spawns parallel LLM agents that extend a research DAG (idea → hypothesis → experiment → verdict → mvp → outcome), one node per iteration.

The point of the fold: **the loop researches its own code**. Graph nodes correspond to actual files and functions in this repo, so the loop can reason about — and eventually modify — its own algorithms.

The fold from `CodexOperator/autoresearch-tree` into this repo is **complete and pushed**. Both git histories are preserved via subtree merge.

---

## 1. 🔴 READ THIS BEFORE RUNNING THE LOOP ANYWHERE

There is a **silent data-loss bug**. See `TODO.md` → **H0** for the full writeup.

**Short version:** `driver.sh:79` prefers a *project-local* `bin/snapshot-build-site.py` over the plugin's. Some projects ship a **stale** copy of that script that begins with `shutil.rmtree(NODES_DIR)`. Result: running the loop in such a project deletes its entire node corpus. Exit code 0. No warning. Nothing printed.

Confirmed blast: `~/.hermes/agi-tree/` went from 29,422 node files → 158 in one `--smoke` run.

**The plugin's own snapshot script is safe** — it does incremental upsert and prunes only nodes carrying `origin: build-site` frontmatter.

**Before running the loop in ANY project, check:**

```bash
ls <project>/bin/snapshot-build-site.py 2>/dev/null && \
  grep -n "rmtree" <project>/bin/snapshot-build-site.py
```

If that prints an `rmtree` line, **rename the file** so the plugin's safe version wins:

```bash
mv <project>/bin/snapshot-build-site.py <project>/bin/snapshot-build-site.py.STALE-DO-NOT-USE
```

Audit the same way for `<project>/bin/render-context.py`.

---

## 2. Bootstrap on a new machine

### 2a. Auth + clone

The repo is **private**, so `gh` must be authenticated as `CodexOperator` first.

```bash
gh auth login          # choose HTTPS; scopes need at least 'repo'
gh auth status         # expect: Logged in to github.com account CodexOperator

git clone https://github.com/CodexOperator/agi.git ~/.hermes/agi
cd ~/.hermes/agi
```

Path `~/.hermes/agi` is conventional, not required — nothing in the code hardcodes it. Scripts resolve `PLUGIN_ROOT` from `$BASH_SOURCE` and `PROJECT_ROOT` from `$AUTORESEARCH_TREE_PROJECT_ROOT` or by walking up for `autoresearch-tree.config.json`.

### 2b. Dependencies

Versions below are what the fold was validated against.

| Dependency | Version used | Required for | Install |
|---|---|---|---|
| Python | 3.11.15 | everything | system |
| `pyyaml` | 6.0.3 | **hard requirement** — frontmatter parsing | `pip install pyyaml` |
| `pytest` | — | test suite | `pip install pytest` |
| Node | v22.22.2 | the TypeScript bridge extension | system |
| npm | 10.9.7 | installing `pi` | system |
| `pi` | 0.67.68 | agent runtime that executes loop iterations | `npm i -g @mariozechner/pi` (confirm current package name) |
| `gensim` | 4.4.0 | *optional* — embeddings research path | `pip install gensim` |
| `umap-learn` | — | *optional* — embeddings research path | `pip install umap-learn` |
| `ollama` | not installed | *optional* — a benchmark path logs `ERR: ollama package not installed` and continues | `pip install ollama` |

Only `pyyaml` is load-bearing for the core loop. The `ollama` error in benchmark output is benign and expected.

### 2c. Install the CLI

Two names point at the same driver during the transition:

```bash
mkdir -p ~/.local/bin
ln -sf ~/.hermes/agi/extensions/agi/driver.sh ~/.local/bin/agi
ln -sf ~/.hermes/agi/extensions/agi/driver.sh ~/.local/bin/autoresearch-tree

# ensure ~/.local/bin is on PATH
echo $PATH | tr : '\n' | grep -q "$HOME/.local/bin" || \
  echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
```

Verify:
```bash
agi --help
autoresearch-tree --help    # must print identical output
```

### 2d. Register the Claude Code SessionStart hook (optional)

Injects the project's graph map into every new CC session. In `~/.claude/settings.json`, under `hooks.SessionStart[].hooks[]`:

```json
{
  "type": "command",
  "command": "<HOME>/.hermes/agi/extensions/agi/hooks/cc-session-start.sh",
  "timeout": 15,
  "statusMessage": "Building agi map..."
}
```

The hook is a **silent no-op** outside projects containing `autoresearch-tree.config.json`, so it's safe to register globally.

> ⚠️ **On the old machine this entry is stale** — it still points at `/home/ubuntu/autoresearch-tree/extensions/autoresearch-tree/hooks/cc-session-start.sh`. That path still resolves today but breaks the moment `TODO.md` → C1 deletes the legacy directory. Fix it there or accept the breakage.

### 2e. Pi extension discovery

Pi discovers extensions via the **project-local `package.json`** glob, already declared at the repo root:

```json
"pi": { "extensions": ["./extensions"], "skills": ["./skills"] }
```

That picks up `extensions/agi/` and `extensions/agi-bridge/` automatically. **No `.pi/extensions/` symlinks are needed** — this was verified during the fold (`TODO.md` → F1).

Separately, `davebcn87/pi-autoresearch` is installed globally via pi and provides the `/autoresearch` slash command that drives loop turns. Check with `pi list`. It is an **external dependency — not forked, not vendored**. Nothing of davebcn's was copied into this repo.

### 2f. Verify the install

```bash
cd ~/.hermes/agi
pytest extensions/agi/tests/ -q --tb=no -p no:cacheprovider
```

**Expected: `1 failed, 166 passed`.** The one failure is pre-existing and known:
`extensions/agi/tests/graph_core/test_node.py::test_field_set_is_exactly_six`.
That is the accepted baseline — recorded in `context/refs/pytest-baseline-prefold.md`. Do not treat it as a regression.

Then check the algorithm package imports:
```bash
cd ~/.hermes/agi/extensions/agi/src
python3 -c "from agi_algos import build_graph, GraphBuilder, QueryEngine, PiTreeAdapter, ASCIIRenderer, render_to_string, benchmark; print('OK')"
```

---

## 3. Repo layout

```
~/.hermes/agi/
  README.md                          identity + orientation
  HANDOFF.md                         this file
  TODO.md                            deferred-work register — START HERE for what to do next
  package.json                       pi.extensions + pi.skills globs
  AGENTS.md / CLAUDE.md              agent briefs

  extensions/
    agi/                             the engine
      driver.sh                      orchestrator; resolves PLUGIN_ROOT + PROJECT_ROOT
      conftest.py                    pytest path injection for src/
      bin/                           snapshot-build-site, render-context, dispatch,
                                     heal, zoom, cli, benchmark, post_wire
      hooks/cc-session-start.sh      Claude Code SessionStart injector
      lib/                           find-root.sh, agent-prompt.md (builder agent rules)
      scripts/migrate_to_sqlite.py   one-shot filesystem -> sqlite migration
      src/
        graph_core/                  framework: node, edge, types, identity, cache,
                                     loader, db_loader, errors, persistence/
                                     (filesystem, sqlite_backend, in_memory,
                                      frontmatter, lazy_body)
        agi_algos/                   ALGORITHMS (folded from old hermes/agi root):
                                     graph_builder, query_engine, benchmark,
                                     pi_tree_adapter, asciirender
        renderers/                   ascii, mermaid, git_diff, representation
        embeddings/                  node2vec, projection, similarity (gensim+UMAP)
        schema_registry/             fingerprint, active_set, cascade, validation,
                                     dsl, meta_nodes, loader
      tests/                         167 tests

    agi-bridge/
      index.ts                       pi extension: hooks before_agent_start,
                                     refreshes INJECTION.md per agent turn

  skills/agi/SKILL.md                the skill doc driving loop iterations

  context/
    kits/                            5 cavekits + overview (the fold spec)
    plans/build-site.md              64-task dependency graph, 7 tiers
    impl/                            impl-tier0.md, impl-fold.md, loop-log.md
    refs/                            pytest baseline, commit conventions, legacy prestate
```

### Two ASCII renderers coexist — this is deliberate, not a bug

| File | Renders |
|---|---|
| `extensions/agi/src/renderers/ascii.py` | the autoresearch-tree **project graph** (hypothesis / idea / task / experiment / verdict / mvp / outcome) |
| `extensions/agi/src/agi_algos/asciirender.py` | the hermes **35-node-type code graph** |

`agi_algos/pi_tree_adapter.py` bridges the two taxonomies. Unifying them is `TODO.md` → **A2**, gated on **A1** (making `graph_builder` data-source-agnostic).

---

## 4. Current state

### Done and pushed

- Subtree merge of `CodexOperator/autoresearch-tree` into this repo. Both histories in one `git log` — e.g. `9a8c8b3` and `414424a` from autoresearch-tree, `3d550de` and `945597c` from agi.
- Engine, bridge, and skill relocated to `extensions/agi/`, `extensions/agi-bridge/`, `skills/agi/`.
- Root algorithm files moved into `extensions/agi/src/agi_algos/` with a public-API `__init__.py`. `_benchmark.py` renamed `benchmark.py`. All intra-package imports converted to relative form.
- `package.json` renamed to `agi`; pi globs preserved.
- Dual CLI (`agi`, `autoresearch-tree`), `--help` parity verified.
- `TODO.md` authored: 3 algorithm + 9 harness + 5 fold-time decisions + 6 cleanup entries.
- Secret scan clean before push (token patterns, key patterns, hardcoded assignments — all empty).

### Verified working

| Check | Result |
|---|---|
| `pytest extensions/agi/tests/` | 166 pass / 1 known fail — matches pre-fold baseline |
| `agi --smoke --max-iters 1` | engine runs; snapshot + render + metrics all fire |
| `autoresearch-tree --smoke --max-iters 1` | byte-identical output — alias parity |
| SessionStart hook | emits map header with graph snapshot + top-10 attractive ideas |
| `from agi_algos import ...` | all public symbols import |

### NOT done — deliberately

| Item | Why |
|---|---|
| **Live agent run** (`agi --max-iters 1` without `--smoke`) | Never executed. Consumes tokens. This is what verifies the env-leak fix — see §5. |
| **Bridge-load verification** | Needs a live pi + CC session. Bridge code is preserved verbatim but unproven post-fold. |
| **`CodexOperator/agi-tree` repo** | Remote URL is configured in `~/.hermes/agi-tree/` but **the GitHub repo was never created and nothing was pushed**. Blocked on the H0 fallout — see §5. |
| **Archiving `CodexOperator/autoresearch-tree`** | Still **public and unarchived**. It does **not** contain the fold. Gated on verification. |
| **Deleting legacy `~/autoresearch-tree/`** | `TODO.md` → C1. Note its local `main` has 2 commits never pushed to its origin. |
| **Loop-against-self** | `~/.hermes/agi/` is not yet itself a research project — it has no `autoresearch-tree.config.json` or `nodes/`. Bootstrapping that is the real "dogfood" milestone. |

---

## 5. Pending actions that can only happen on the OLD machine

These involve local state that is not in any git remote. If the old machine is being retired, do these first or accept the loss.

### 5a. 🔴 Restore the agi-tree node corpus

`~/.hermes/agi-tree/` has **29,264 node files deleted from disk** by the H0 bug. All are present in git HEAD — verified individually with `git cat-file -e`. Of the 158 survivors, 15 differ from HEAD and are strictly *worse* (regeneration stripped their `next_edges` links); 0 are new. A full restore therefore loses nothing.

```bash
# 1. defuse H0 FIRST, or the next run wipes it again
mv ~/.hermes/agi-tree/bin/snapshot-build-site.py \
   ~/.hermes/agi-tree/bin/snapshot-build-site.py.STALE-DO-NOT-USE

# 2. restore
git -C ~/.hermes/agi-tree checkout -- nodes/

# 3. verify — expect 29422
find ~/.hermes/agi-tree/nodes -name '*.md' -type f | wc -l
```

> This was attempted during the fold session and **correctly blocked** by the Claude Code safety classifier, on the grounds that discarding working-tree state across a research corpus needs the user to name that path explicitly. Run it yourself, or authorize it.

### 5b. Push agi-tree

Only after 5a. The working tree also carries pre-existing edits (`autoresearch-tree.config.json`, `autoresearch.jsonl`, `src/chain_engine/chains.py`) and untracked artifacts (`nodes.db`, `.chain_cache.pkl`, `exp-a01-extend-2000hop.py`, `.claude/worktrees/`).

```bash
cd ~/.hermes/agi-tree
git status                       # review before staging
# gitignore the cache/worktree artifacts, commit or stash the real edits
gh repo create CodexOperator/agi-tree --private --source=. --remote=origin
git push -u origin master        # master only; iter branches stay local
```

Current branch there is `iter24-extend-300hop`, not `master` — check out `master` first, or decide deliberately which to push.

### 5c. Live verification (the real gate)

```bash
cd ~/.hermes/agi-tree            # only after 5a + H0 defused
agi --max-iters 1 |& tee /tmp/agi-iter1.log
tail -50 sessions/iter-*/a00-*/output.log
```

**Must NOT contain** `api.anthropic.com`, `Token Plan`, or HTTP 429. If it does, pi is leaking the Claude Code subscription quota again — that was fixed in commit `5d7c7f1` (dispatch.py scrubs `ANTHROPIC_*` / `CLAUDE_CODE_*` from the pi subprocess env), so a recurrence means a new leak path. Expected instead: minimax-style output.

### 5d. Other local-only state

- `~/autoresearch-tree/` — legacy dir; local `main` is 2 commits ahead of its origin (`006d808` tier-0 tracking, `1aebdf7` pre-fold WIP). Both are already captured inside the agi subtree merge, so nothing is lost by deleting it.
- `~/.hermes/belam-codex-modularnn-spike-viz/` — separate modularNN research worktree. Unrelated to the fold. `TODO.md` → C4. **Audit it for the H0 stale-script landmine before ever running the loop there.**
- `~/.hermes/HANDOFF-autoresearch-2026-05-01.md` — the previous handoff. Superseded by this file, but retains detail on iters 6–37 (embedding wins, metric gaming) worth reading once.

---

## 6. What to work on next

`TODO.md` is the register. Priority order:

| ID | Item | Why first |
|---|---|---|
| **H0** | Stale snapshot override wipes node corpus | Data loss. Blocks safe loop runs anywhere. |
| **H3** | Replace `longest_chain_length` metric | Agents proved it gameable — they hit 2000 hops via shortcut chains (`hops=2*cycle+8`) with zero research signal. Until this changes, the loop optimizes noise. |
| **H4** | Orphan-verdict gate (`evidence_runs > 0`) | 99.7% of verdicts in the iter 6–37 run had no backing experiment. The system flagged its own bullshit (commit `67ead2f0`) but the gate was never added to the writer path. |
| **H1** | DB-only state migration | The stated long-term direction: no state files, DB as the only state reference, graph as the render layer. `sqlite_backend.py` (278 lines) and `db_loader.py` (173 lines) already exist as scaffolding. |
| **H2** | Import agi-tree nodes into the DB | 29,422 accumulated research nodes become queryable prior art. Depends on H1. |
| **A1 → A2** | Data-source-agnostic `graph_builder`, then unify the two ASCII renderers | Unblocks a single rendering path across both taxonomies. |
| **H7** | Ship gensim+UMAP embeddings to production | Already PROVED: Spearman 0.79+ vs 0.49 for PCA; k-NN 45.4% vs 8.4%. Sitting unused in `src/embeddings/`. |

**H3 and H4 together are the credibility problem.** The loop currently produces impressive-looking numbers that mean very little: a gameable primary metric plus verdicts with no evidence backing. Fixing those matters more than adding capability.

---

## 7. How the loop works

One iteration = one node added to the research DAG.

```
driver.sh
  ├─ snapshot-build-site.py   rebuild build-site-origin nodes from context/plans/build-site.md
  ├─ render-context.py        render graph -> context/INJECTION.md (ASCII map, bounded)
  ├─ benchmark.py             emit METRIC lines
  ├─ dispatch.py              spawn N pi agents in parallel
  │                             slot 0    -> BIG zoom  (whole graph, fresh ideas)
  │                             slot 1..N -> SMALL zoom (top-attractor subtree, 2-hop)
  │                           scrubs ANTHROPIC_*/CLAUDE_CODE_* from the child env
  ├─ heal.py                  poll manifests; SIGTERM/SIGKILL hung agents;
  │                           spawn a healer subagent with the last 4KiB of the agent log
  ├─ post_wire.py             wire up edges after agents finish
  └─ cli.py status            report
```

Agents signal completion with:
```bash
cli.py done <iter> <agent_id> --verdict <V> --confidence <0..1>
```

**Verdict taxonomy (finite-state):**
`proved | disproved | inconclusive_lean_proved:N | inconclusive_lean_disproved:N | pending`

**Capillary DAG chain:**
`idea → hypothesis → experiment → verdict → mvp → outcome → bigger_outcome → app_purpose`

**Zoom levels:** BIG = whole-graph context. SMALL = subtree-bounded, 2 hops.

**Recommended launch** (long runs; survives disconnect):
```bash
cd <project>
tmux new-session -d -s agi "agi --max-iters N --delay-mins M |& tee /tmp/agi.log"
tmux attach -t agi      # Ctrl-B D to detach
```

**Iter numbering caveat:** the driver always starts at `iter-001` and clobbers prior session manifests. `TODO.md` → H6 adds a `--iter-base N` flag. Until then, back up `sessions/` before a fresh run.

---

## 8. Glossary

- **Cavekit** — implementation-agnostic spec; R-numbered requirements with testable acceptance criteria. Lives in `context/kits/`.
- **Build site** — dependency-ordered task graph generated from cavekits. `context/plans/build-site.md`.
- **Tier** — dependency layer in a build site. Tier 0 has no blockers.
- **Capillary DAG** — the research chain shape (see §7).
- **Zoom level** — BIG (whole graph) vs SMALL (2-hop subtree) agent context.
- **PLUGIN_ROOT** — the engine directory, `extensions/agi/`. Resolved from `$BASH_SOURCE`.
- **PROJECT_ROOT** — the research project's own directory, holding `autoresearch-tree.config.json`, `nodes/`, `sessions/`, `context/`. From `$AUTORESEARCH_TREE_PROJECT_ROOT` or by walking up from cwd.
- **INJECTION.md** — the rendered ASCII graph map injected into agent context each turn.

---

## 9. Fast sanity check on a new machine

```bash
cd ~/.hermes/agi
git log --oneline | head -3                              # expect fold: / track: commits
git log --oneline | grep -c 9a8c8b3                      # expect 1 — ar-tree history present
pytest extensions/agi/tests/ -q --tb=no 2>&1 | tail -1   # expect "1 failed, 166 passed"
which agi && readlink -f "$(which agi)"                   # resolves into extensions/agi/driver.sh
agi --help | head -2
```

All five green ⇒ the install is sound. Then read `TODO.md` and pick a P0.
