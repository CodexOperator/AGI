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

**Goals live project-side, as nodes.** ⚠️ *This paragraph said the opposite until 2026-08-27 — it claimed goal nodes in `nodes/goal/` were **not** built. They are, and they are the source of truth.*

`nodes/goal/*.md` is authoritative and **`GOALS.md` is rendered from it** by `snapshot-goals.py --render`, which `driver.sh` runs on every smoke pass. **Edit the node, never `GOALS.md`** — a hand-edit there survives until the next `--smoke` and then vanishes with no warning. `--render --check` exits 0 only on a byte-identical round trip.

The lifecycle is **four** states, not three: `active` (being worked) | `horizon` (declared and committed to, not yet being worked) | `phasing-out` (retiring) | `complete`. `horizon` is what makes goal rotation expressible without lying about which goals are in flight. Unknown values are preserved verbatim with a warning, never dropped.

Ids are `G<n>` (long-term), `G<n>.<m>` (subgoal, exactly one goal parent) and `S<n>` (short-term / bugfix), discriminated on `goal_kind`. **Ids are never renumbered — a gap beats a renumber.** Retire by marking `phasing-out` and deprecating the seed node; never delete.

Still not built: attribution-based scoring and status enforcement. (`TODO.md` is an archive as of 2026-08-22 — its L-entries are absorbed into goals and nothing new is added there.)

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

---

# SESSION HANDOFF — 2026-08-27: graph standardization pass

> **Read this section first if you are the next session.** Everything above is
> the 2026-08-18 install/orientation guide and is still broadly correct; a few
> details in it are stale (the pytest baseline is now **723 passed, 1 skipped**,
> not 176, and `TODO.md` is an archive — `GOALS.md` is the only place new work
> is recorded). This section is the current state and the work queue.

## 0. State as of commit `4f06e3a4f`

```
node_count            786          goal_count             80
evidence_fraction     0.206        primary (outcome_cov)  0.255
dangling references   0            unevidenced_decisive   0
duplicate ids         0            shadow_decisive        0
engine tests          723 passed, 1 skipped
```

Graph and engine are both clean and in sync. `publish-engine.sh` reports
"engine already matches the graph". Verified stable across 3 consecutive runs.

## 1. What changed this session

**Renames, all atomic, all verified with node counts at each step.**

| was | now | n |
|---|---|---|
| `level3` (type, dir, id prefix, `origin`, contract marker) | `build` + `build_kind: code\|prose` | 190 |
| `app_purpose` | `vision` | 17 |
| `hypothesis:` / `experiment:` id prefixes | `hyp:` / `exp:` | 37 |
| `nodes/app-purpose/`, `nodes/bigger-outcome/` | merged into underscore dirs | 19 files |
| — | new type `overview` | 0 nodes yet |

**Integrity repairs.** 21 hidden parent edges recovered from legacy keys
(`parent_hypothesis`, `parent_idea`, `parent`) that no gate read; 8 dangling
`next_edges` (2 repaired, 6 dropped); `spawns` folded into `next_edges`;
`evidence_runs: 0` normalized to `[]` on 65 nodes; 3 nodes had no `type:`.

**Spawn DSL.** `min_parents_by_type` added (per-kind parent floors),
`max_parents_ceiling` 2 -> 4, `edge_fields` classifying edges as lineage /
scheduling / provenance / proposal.

**Convergence tier.** `outcome -> bigger_outcome -> overview -> vision`, floors
2v+2o -> 3bo -> 2ov. `vision --proposes_goals--> goal` closes the loop across
**seasons** and is declared non-traversable, so the type graph stays acyclic.

## 2. 🔴 Start here: G2.10 — a build node cannot hold a thought

**The most important finding of the session, and the one that gates several
others.** `bin/level3.py` regenerates a build node's *entire body* on every
run. Probed both directions on 2026-08-27:

- prose added to a build node body -> **wiped** by the next scan
- a filled-in `why: TODO(model)` -> **wiped** by the next scan

The corpus reads exactly as that predicts:

```
why/perf/security fields across 190 build nodes:  8,034
still reading TODO(model):                        8,034
ever filled:                                          0
```

`[build].md` states a permission ("a model may fill why/perf/security") that
the code revokes on the next run. Frontmatter *is* preserved (`write_frontmatter`
merges with `preserve=`); the body is not. **The fix is to give the body the
same treatment: regenerate the mechanical `how`, carry over `why`/`perf`/
`security` and any prose outside the markers.**

Falsifier: fill one `why:` on one build node, run `driver.sh --smoke`, read it
back.

**This is coupled to G6.8**, whose whole argument for admitting build nodes is
that they hold thought bidirectionally — half of which is currently false. Read
G2.10 and G6.8 together; both carry the cross-reference.

**It also reverses the `@v2` cleanup.** The five `origin: build-version` nodes
(`build:bin-grid@v2` + 4) look like the redundancy CLAUDE.md forbids. They are
not: they hold 7k–13k characters of reasoning each and survive *only* because
`level3.py` does not own their origin. Their payloads are byte-identical to the
engine, so collapsing loses no bytes — and ~47,000 characters of prose, with
nowhere to put it. **Sequence: fix G2.10, migrate the five bodies into their v1
nodes, then retire the convention.**

## 3. Next most valuable, in order

1. **G2.10** — above. Unblocks the `@v2` collapse and makes build nodes real.
2. **G7.3** — `evidence_runs` as a bare integer. 77 of 112 values are bare ints
   against a schema declaring a list. 65 zeros were normalized to `[]`; **the
   12 remaining `1`s are listed by id in the goal node.** The severe one is
   `verdict:zoom-encoded-node-ids` — `proved`, decisive only because
   `normalize_evidence_runs` returns an unchecked int. Fixing it is a payload
   change to `bin/evidence_gate.py`, not a node edit.
3. **G7.9** — `level3.py` should not prune quietly, and should be renamed
   (`view.py`/`main.py` — it is the code-level view you load into). *You said
   you have more pieces of this update in mind.* Also carries: a refused
   `publish-engine.sh` is not a no-op — it mutated the graph at step 1 before
   refusing at step 3, creating 184 junk nodes during the rename.
4. **G1.7** — the demotion path is four fields (`verdict`, `status`,
   `demoted_from`, `demote_reason`) and `evidence_gate` owns one. Reproduced
   live: a correctly-gated demotion rewrote `verdict:` and left the legacy
   `status: proved` contradicting it underneath. Caught only because
   `metrics.py` emits `shadow_decisive_verdicts`, which went 0 -> 1.
5. **S18** — absorb cavekit references before cavekit retires. 91 of 94
   `cavekit_req` values resolve fine; the hazard is *ordering* — deleting
   `context/kits/` prunes 159 `origin: build-site` nodes (H0i).
6. **G4.5** — generalize `blocked_by` -> `depends_on` beyond `task`. Already
   89 populated nodes, 0 cycles, max depth 15. Must stay out of every metric
   traversal or it becomes a fresh gaming surface.

## 4. Traps this session actually hit — do not re-learn these

- **`publish-engine.sh`, not `stitch.py --publish`.** The latter writes the
  bytes and never commits, leaving the engine dirty — which is exactly what the
  next `--publish` refuses on. Recovery: `git -C <engine> checkout .` (the bytes
  are in the grid), then `publish-engine.sh`. CLAUDE.md documented the wrong one
  until 2026-08-27.
- **Gate 1 refuses on *any* uncommitted change under `nodes/` or `GOALS.md`.**
  A single node whose stored contract differs from what `level3.py` re-derives
  makes the graph permanently dirty, and the cron then refuses **silently, every
  hour**. It had done so **40 consecutive times, with 0 successful publishes
  ever**, since it was installed 2026-08-25. If the publish cron seems idle, run
  `level3.py` and check `git status` before anything else.
- **Hand edits to `origin: build-site` nodes are reverted on the next smoke
  run.** Observed: a dangling `blocked_by` was removed by hand and was back
  after `driver.sh --smoke`. Fix those in `context/plans/build-site.md`.
- **A bare type name in a schema is invisible to an id-rename pass.**
  `[experiment].md` still listed `level3` in `allowed_parents` after the rename,
  because it has no `:` in it. **Run the spawn gate over the whole corpus as the
  last step of any type rename.**
- **Contract derivation still reads the engine tree.** A payload edited only
  in the graph has a stale contract until published and rescanned. During a *rename* this is a bootstrap problem: the engine's own
  `stitch.py` could not publish the change that teaches it to read
  `nodes/build/`. Published once with the payload copy to break the cycle.

## 5. How to write into this file

`HANDOFF.md` is `build:HANDOFF.md`, `build_kind: prose`. **Edit the payload,
never the node body** — the body is regenerated on every scan (G2.10), the
payload is the real file and is durable:

```bash
python3 agi/extensions/agi/bin/grid.py checkout --all   # payloads/HANDOFF.md
$EDITOR payloads/HANDOFF.md
python3 agi/extensions/agi/bin/grid.py commit --all     # the payload's real home
bash agi/extensions/agi/bin/publish-engine.sh           # re-derives, publishes, commits engine
git add -A && git commit                                 # NOW the node contract has changed
```

**The order matters and is not the obvious one.** `payloads/` is **gitignored** —
the committed home of those bytes is the node's grid ref, not the working tree.
So `git add -A` finds *nothing* right after a payload-only edit, and a commit
attempted there silently does nothing ("nothing to commit, working tree clean")
while you believe your reasoning was recorded. The node file only changes once
`publish-engine.sh` re-derives its contract block from the published payload.
**Commit last, and put the reasoning for the payload edit in that commit** —
otherwise it exists solely as a grid version with no message in git history.
Walked into on 2026-08-27, twice.

## 6. Known-good verification sequence

```bash
bash agi/extensions/agi/driver.sh --smoke --max-iters 1   # node_count must not drop
cd payloads && python3 -m pytest extensions/agi/tests/ -q # 723 passed, 1 skipped
python3 agi/extensions/agi/bin/snapshot-goals.py --render --check   # byte-identical
bash agi/extensions/agi/bin/publish-engine.sh            # "already matches" when clean
```

Spawn-gate state over the whole corpus: **712 approved, 72 rejected, 1
unverified**. Of the 72, 70 are pre-existing `min_parents` violations (down from
91) and 36 overlap the three deliberately PRESCRIPTIVE schemas
(`[bigger_outcome].md`, `[overview].md`, `[vision].md`) which state what *should*
be and which the corpus is expected to fail until written up to. The 1
unverified is `doc:goals-preamble` — there is still no `[doc].md`.
