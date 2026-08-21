# HANDOFF — agi, for a fresh session on a new machine

> Self-contained. Assumes **nothing** exists locally: no clone, no deps, no CLI, no auth.
> Updated 2026-08-18. `CodexOperator/agi` **private**, default branch `master`.
> Local paths note: `~/.hermes/agi` is now a **symlink → `~/work/agi`**. Either path works.

---

## 0. TL;DR

`agi` = **Artificial Graph Intelligence**. One repo holding:

1. **Graph algorithms** — build a graph from a codebase, query it, render it as ASCII, benchmark it.
2. **A loop harness** — spawns parallel LLM agents ("kids") that extend a DAG, one node per iteration, with a reviewing parent.

**The loop works on its own code.** Graph nodes correspond to real files and functions, so the loop can reason about — and eventually modify — its own algorithms.

### Where this is going — read `TODO.md` §"Long-term direction" (L0–L15)

The system is generalizing **from a research loop into a general-task loop**: game, app, web, SEO, ops. Each node stops being a research artifact and becomes a **long-lived thought** — extended, forked, deprecated over time.

**Design ethic governing all of it:** emitted tokens are an agent's motion; injected context is its sensation; context growth makes motion heavier. Every capability exists to keep agent bodies light. Sprint one node hard, rest, let the graph carry the marathon. Mundane operations — and the small errors they breed — are the system's job to absorb, never the agent's. Full statement in `skills/agi/SKILL.md` §"Why this machinery exists".

`TODO.md` L0 has a status table separating what is **built** from what is only **described**. Read it before planning — several capabilities exist as prose only.

**Goals live project-side.** `~/work/fantasia/GOALS.md` is the reference implementation — root goals `G1..G7` with `status: active | phasing-out | complete`, seed nodes referencing them by id, and a goal-attributable `metric_primary`. The engine stays domain-free. What is *not* built is engine support: attribution-based scoring, status enforcement, and goal nodes in `nodes/goal/`. See `TODO.md` L0a, L4, L5, L15.

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

**Audit `<project>/bin/render-context.py` the same way** — there is a second stale copy in the wild (`TODO.md` H0b) that uses a recursive chain walk and dies with `RecursionError` on any deep corpus. It doesn't destroy data, but it does break the render stage.

**General rule (`TODO.md` H0b):** treat *any* project-local `bin/*.py` as stale until proven otherwise. The override mechanism itself is the defect — `TODO.md` H0 action 2 proposes making it opt-in.

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

Path `~/.hermes/agi` is conventional, not required — nothing in the code hardcodes it. Scripts resolve `PLUGIN_ROOT` from `$BASH_SOURCE` and `PROJECT_ROOT` from `$AGI_TREE_PROJECT_ROOT` (legacy `$AUTORESEARCH_TREE_PROJECT_ROOT` still read) or by walking up for `agi-tree.config.json` (legacy `autoresearch-tree.config.json` still resolves).

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

The hook is a **silent no-op** outside projects containing `agi-tree.config.json`, so it's safe to register globally.

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

**Expected: `1 failed, 176 passed`.** The one failure is pre-existing and known:
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
                                     heal, zoom, cli, benchmark, post_wire,
                                     grid.py (per-node git versions + cron sync)
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

  skills/agi/
    SKILL.md                         the skill doc driving loop iterations
    CC-DISPATCH.md                   CC-native dispatch protocol (kids as CC
                                     subagents), design philosophy, escalation,
                                     model tiering, git grid usage

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

### Landed since the fold (2026-08-18)

| Work | Where |
|---|---|
| **CC-native dispatch** — Claude Code subagents as builder kids | `skills/agi/SKILL.md`. Validated on a live 6-iteration run. Substantially delivers `TODO.md` L12. |
| **Kid → parent escalation** — four triggers, one question per kid per iteration | `skills/agi/SKILL.md` §"Kid → parent questions" |
| **The git grid** — per-node versions in `refs/grid/*`, session drafts, cron sync | `extensions/agi/bin/grid.py`, `TODO.md` H10 |
| **Design philosophy** — motion / sensation / weight | `skills/agi/SKILL.md` §"Why this machinery exists", `extensions/agi/lib/agent-prompt.md` |
| **agi-tree corpus restored + pushed** | 29,422 nodes; `CodexOperator/agi-tree` exists with all branches pushed; working tree clean |

### NOT done — deliberately

| Item | Why |
|---|---|
| **Loop run against agi-tree** | 🔴 Blocked by **H0b** (stale project-local `render-context.py` → `RecursionError`) and **H0c** (`find_chains` hangs >300 s on the full corpus). Fix both before running. |
| **Live pi agent run** (`agi --max-iters 1` via pi, no `--smoke`) | Never executed. Would verify the env-leak scrub. The CC-dispatch path has been exercised live instead. |
| **Bridge-load verification** | Needs a live pi + CC session. Bridge code preserved verbatim but unproven post-fold. |
| **Archiving `CodexOperator/autoresearch-tree`** | Still **public and unarchived**. Does **not** contain the fold. `TODO.md` C2. |
| **Deleting legacy `~/autoresearch-tree/`** | `TODO.md` C1. |
| **Loop-against-self** | `~/work/agi/` is not itself a project yet — no `agi-tree.config.json` or `nodes/`. Bootstrapping that is the real dogfood milestone, and it interacts with L8 — read that first. |

---

## 5. Local-only state (not in any git remote)

Most of what used to live here is done. What remains:

- **`~/.hermes/agi-tree/`** — restored to 29,422 nodes, working tree clean, pushed to `CodexOperator/agi-tree` (branches `master`, `iter24-extend-300hop`, `claude/wonderful-lamport-51c9a9`). Its stale `bin/snapshot-build-site.py` is renamed `.STALE-DO-NOT-USE`. **Its `bin/render-context.py` is still stale — H0b.** Do not run the loop here yet.
- **`~/autoresearch-tree/`** — legacy directory, fully captured inside the agi subtree merge. Safe to delete (`TODO.md` C1).
- **`~/.hermes/belam-codex-modularnn-spike-viz/`** — separate modularNN worktree, unrelated. `TODO.md` C4. **Audit it for the H0/H0b stale-script landmine before ever running the loop there.**
- **`~/.claude/settings.json`** — the SessionStart hook entry still points at the legacy `~/autoresearch-tree/...` path. Works today; breaks the moment C1 runs.
- **`~/.hermes/HANDOFF-autoresearch-2026-05-01.md`** — superseded by this file. Retains iters 6–37 detail (embedding wins, metric gaming) worth one read.

### Live verification still owed

The pi dispatch path has never been run live post-fold. If you use it:

```bash
cd <project>
agi --max-iters 1 |& tee /tmp/agi-iter1.log
tail -50 sessions/iter-*/a00-*/output.log
```

**Must NOT contain** `api.anthropic.com`, `Token Plan`, or HTTP 429. If it does, pi is leaking the Claude Code subscription quota — fixed once in `5d7c7f1` (dispatch.py scrubs `ANTHROPIC_*`/`CLAUDE_CODE_*` from the pi child env), so a recurrence means a new leak path. CC-native dispatch (`skills/agi/SKILL.md`) is the *sanctioned* way to spend subscription tokens; never bypass the scrub instead.

---

## 6. What to work on next

`TODO.md` is the register. Two tracks: **unblock** (fix what's broken) and **direction** (build toward the general-task loop). Unblock first — the direction work runs on top of a loop that currently can't run on a real corpus.

### Track 1 — unblock (do these first)

| ID | Item | Why first |
|---|---|---|
| **H0b** | Stale project-local `render-context.py` (recursive → `RecursionError`) | One rename unblocks agi-tree. Then audit *every* project for any `bin/*.py` override. |
| **H0c** | `find_chains()` hangs >300 s on the full corpus | The loop cannot run on agi-tree until this is bounded. |
| **L7 bug** | `zoom.py:89-91` silently serves the whole graph when `graph_core` import fails | Subtree bounding never engages on big corpora — the opposite of the design intent. Small fix, immediate payoff. |
| **H3 + H4** | Gameable metric; unevidenced verdicts | Together these are the credibility problem: impressive numbers that mean little. H0c is H3's downstream damage — same defect, two ends. |

### Track 2 — direction (`TODO.md` L0–L15)

Recommended order, with the dependencies that force it:

1. **L0a — decide where goals live.** Everything scoring-related (L4, L5) blocks on this, and it's a 30-minute decision, not a build. Recommendation in the entry: project-side.
2. **L1 — the 5-step zoom axis**, starting with **level 3** (code nodes stitchable into a runnable directory). Level 3 is what makes the graph an executable artifact instead of a description of one. L3 (model tiering) and much of L2 block on this.
3. **L11 (remainder) — script away the copy-paste spawn step.** The rename is done; the one-command render-and-spawn is not. Directly serves the design ethic: every un-scripted step is motion spent on operations instead of work.
4. **L2 — IO maps.** These are what keep L1's decompose/rollup honest; contracts are what survive a zoom change.
5. **L12 — finish the CC runtime.** Mostly built; needs the pi-invocation flag and a hook-parity audit. **If the audit finds a gap, report it and plan rather than improvising.**
6. **L15 — make goals first-class nodes** in `nodes/goal/`, derived from `GOALS.md` the same way `build-site.md` already derives `task` nodes. This is what turns L4 scoring from a proxy into real attribution, and it *is* zoom level 1.

**Already done (2026-08-18):** L11 rename (`overseer` → `parent`), L13 for the skill, and L14 — `SKILL.md` and `CC-DISPATCH.md` merged into one 215-line CLI-first skill. L7's silent whole-graph fallback and H0b are fixed.

L8 (one repo vs two), L9 (forkability), L10 (peek/dashboard), L6 (recursive sub-loops) are P2 and can follow.

### Architecture questions — current answers

**Should `agi-tree` live inside `agi`?** *Optional, and there's a better shape.* No paradox — a repo holding a graph that describes itself is ordinary self-reference. But two real costs: **self-inflation** (graph storage inside the parsed tree means each iteration feeds the next build; needs an explicit parser exclusion shipped in the same commit) and **clone weight** (29,422 node files ride along for every consumer). Recommended instead: put the graph in a dedicated ref namespace `refs/tree/*`, exactly as `grid.py` already does with `refs/grid/*` — baked in, never checked out, fetched on demand. Full analysis in `TODO.md` L8.

**Should `agi` sit inside every project that uses it?** **No.** That's the H0/H0b failure mode generalized — stale project-local copies of engine scripts silently destroyed 29,264 files. Vendoring the *entire engine* per project makes every project a stale override waiting to happen. Engine installed once and referenced by version; each project owns only its own graph + config + goals doc. This is also the precondition for L9 (forkability).

**Is the goal system reflected in `agi-tree`?** No — because it doesn't exist in `agi` either. See `TODO.md` L0a. `agi-tree` is simply stale relative to the engine; its last substantive work is the 2000-hop chain extension that produced H3 and H0c.

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
- **PROJECT_ROOT** — the research project's own directory, holding `agi-tree.config.json`, `nodes/`, `sessions/`, `context/`. From `$AGI_TREE_PROJECT_ROOT` (legacy `$AUTORESEARCH_TREE_PROJECT_ROOT`) or by walking up from cwd.
- **INJECTION.md** — the rendered ASCII graph map injected into agent context each turn.

---

## 9. Fast sanity check on a new machine

```bash
cd ~/.hermes/agi
git log --oneline | head -3                              # expect fold: / track: commits
git log --oneline | grep -c 9a8c8b3                      # expect 1 — ar-tree history present
pytest extensions/agi/tests/ -q --tb=no 2>&1 | tail -1   # expect "1 failed, 176 passed"
which agi && readlink -f "$(which agi)"                   # resolves into extensions/agi/driver.sh
agi --help | head -2
```

All five green ⇒ the install is sound. Then read `TODO.md` and pick a P0.
