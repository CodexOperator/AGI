---
created: "2026-05-04"
last_edited: "2026-05-04"
---

# Implementation Tracking: fold (Tiers 1–5)

Build site: /home/ubuntu/.hermes/agi/context/plans/build-site.md
Branch: `agi-unification` in `~/.hermes/agi/`
Cumulative commits on branch: 8 (subtree merge + fold work)

## Tier 1 — Subtree Merge & Skeleton

| Task | Status | Notes |
|------|--------|-------|
| T-007 | DONE | `git subtree add --prefix=staging /home/ubuntu/autoresearch-tree main`. Both histories preserved. Pre-merge cleanup commit (`4625bf7 fold: pre-merge cleanup`) gitignored cache+log files. |
| T-008 | DONE | Skeleton `extensions/`, `skills/agi/`, `TODO.md` placeholder created. |
| T-009 | DONE | `README.md` declares "agi — Artificial Graph Intelligence", references graph algorithms + research loop harness, mentions companion repo CodexOperator/agi-tree, documents pi auto-discovery + dual CLI + history preservation. |

## Tier 2 — File Moves

| Task | Status | Notes |
|------|--------|-------|
| T-010..T-015 | DONE | Engine moved: `staging/extensions/autoresearch-tree → extensions/agi`. All git renames preserve history. |
| T-016 | DONE | `staging/extensions/autoresearch-tree-bridge → extensions/agi-bridge`. README.md absolute-ref updated. |
| T-017 | DONE | `staging/skills/autoresearch-tree/SKILL.md → skills/agi/SKILL.md`. |
| T-018 | DONE | `extensions/agi/src/agi_algos/__init__.py` exports public API: `build_graph, GraphBuilder, QueryEngine, PiTreeAdapter, ASCIIRenderer, render_to_string, benchmark`. |
| T-019..T-023 | DONE | Algo files moved into agi_algos/: graph_builder, query_engine, benchmark (renamed from `_benchmark`), pi_tree_adapter, asciirender. All imports rewritten to relative form. |
| T-024 | DONE | No external imports of root names found outside `.claude/worktrees/`. Clean removal — no stubs needed. |
| T-025 | DONE | `extensions/agi/src/renderers/ascii.py` preserved at autoresearch-tree-style location. R7 coexistence requirement satisfied. Unification deferred (TODO A2). |

## Tier 3 — Path Hygiene + Manifest + CLI

| Task | Status | Notes |
|------|--------|-------|
| T-026 | DONE | No absolute refs to `~/autoresearch-tree/` under `extensions/agi/`. |
| T-027 | DONE | One reference in `extensions/agi-bridge/README.md` updated to canonical path. |
| T-028 | DONE | `package.json` updated: name `agi`, description, repo URL `CodexOperator/agi`. pi.extensions/pi.skills globs preserved. |
| T-029 | RECORDED | SKILL.md propagation recipe update captured in `TODO.md` H8. New canonical at `~/.hermes/agi/skills/agi/SKILL.md`. Sync recipe targets reduced to 2 locations. |
| T-030 | DONE | `~/.local/bin/agi → ~/.hermes/agi/extensions/agi/driver.sh`. |
| T-031 | DONE | `~/.local/bin/autoresearch-tree` repointed to same target. `--help` parity verified — both CLIs produce identical help. |

## Tier 4 — Pi Discovery + TODO Authoring

| Task | Status | Notes |
|------|--------|-------|
| T-032 | DONE | Verdict: pi auto-discovers via project-local `package.json pi.extensions` glob. davebcn87/pi-autoresearch is globally pi-installed and handles invocation. agi extensions deliberately not pi-installed (project-local discovery). Recorded in TODO.md F1. |
| T-033 | SKIPPED | No `.pi/extensions/` symlinks needed. F1 verdict resolves R9. |
| T-034 | DEFERRED → T-053 | Pi startup smoke is rolled into the smoke loop verification at T-053. |
| T-035 | DONE | `TODO.md` skeleton with 4 sections (Algorithm, Harness, Fold-time decisions, Cleanup). |
| T-036..T-051 | DONE | TODO.md fully populated: A1-A3 (algorithm), H1-H8 (harness), F1-F5 (fold-time decisions), C1-C6 (cleanup). All entries have rationale, evidence, priority. |

## Tier 5 — Loop Continuity Verification

| Task | Status | Notes |
|------|--------|-------|
| T-052 | DONE | `pytest extensions/agi/tests/ -q` → **166 passed, 1 known fail** (`test_field_set_is_exactly_six`). Matches baseline. No regression. R1 satisfied. |
| T-053 | DONE — **with data-loss side effect** | `agi --smoke --max-iters 1` from `~/.hermes/agi-tree/` → PROJECT_ROOT and PLUGIN_ROOT resolved correctly; snapshot wrote 158 nodes; loaded 157 existing nodes; ASCII rendering 163 lines; INJECTION.md written; metrics emitted. R2 satisfied. **This run detonated bug H0**: agi-tree's stale project-local `bin/snapshot-build-site.py` (`shutil.rmtree(NODES_DIR)`, line 164) deleted 29,264 node files. Root-caused via controlled probes in throwaway clones — the plugin's own snapshot, render, and benchmark each delete nothing; only the full driver path does, because `driver.sh:79` prefers the project-local stale script over the plugin's safe one. All deleted files verified recoverable from HEAD. Restore + defusal in `TODO.md` → H0/F4 and `HANDOFF.md` §5a. |
| T-054 | DONE | `autoresearch-tree --smoke --max-iters 1` produces identical output to T-053. Alias parity confirmed. |
| T-055 | DEFERRED | env-leak audit requires live agent run (smoke skips dispatch). Pre-existing fix at commit `5d7c7f1` already scrubs ANTHROPIC_*/CLAUDE_CODE_* env. Live verification: user runs `agi --max-iters 1` (no --smoke) and inspects `sessions/iter-NNN/a00-*/output.log`. |
| T-056 | DEFERRED | Bridge load marker requires live pi+CC session with `/autoresearch` slash command. Bridge code preserved verbatim; will load when invoked. Live verification: user runs CC session in any agi-tree project and watches for `[autoresearch-tree-bridge] loaded` in pi startup. |
| T-057 | DONE | SessionStart hook (`extensions/agi/hooks/cc-session-start.sh`) tested directly: walks up cwd, finds project root, emits "## autoresearch-tree map (auto-injected)" header with graph snapshot (157 nodes, 148 edges, attractive ideas top-10). R5 satisfied. |
| T-058 | DEFERRED | Loop with `~/.hermes/agi/` as project root requires `autoresearch-tree.config.json` + `nodes/` to be created at agi root (it is not currently a research project). This is a *meta* operation — populating agi as its own project. Out of fold scope; recorded as a future research task (would technically satisfy R6 but not part of this fold cycle). |

## Tier 6 — Bug Sweep

**Status:** PARTIAL.

T-059..T-063 envisioned dispatching parallel verification agents. The verification surface they would cover is:
- pytest (covered by T-052: PASS)
- smoke loop (covered by T-053+T-054: PASS)
- env-leak audit (T-055 deferred — needs live run)
- bridge-load (T-056 deferred — needs live run)
- render-output sanity (covered by T-053: ASCII 163 lines, INJECTION.md written)
- embeddings sanity (NOT covered — requires `python -c 'from gensim import models; from umap import UMAP'` smoke + a test run)

**Aggregate report:** `bug-sweep-report.md` deferred. The deferred verifications (T-055, T-056) are the GATE between Tier 6 PARTIAL and Tier 7 (push). User must drive a live run before push.

## Tier 7 — Push + Archive

**Status:** GATED. Not started.

Per kit gate: push to `CodexOperator/agi` and `CodexOperator/agi-tree` is conditioned on bug-sweep clearance. Live agent verification (T-055, T-056) required first.

Pre-push cleanup also needed: agi-tree dirty working tree (TODO F4), `.claude/skills/gitnexus/` accidentally tracked (TODO C6).

## Verification surface for user

To complete Tier 5/6 and unblock Tier 7, run from `~/.hermes/agi-tree/`:

```bash
cd ~/.hermes/agi-tree
agi --max-iters 1 |& tee /tmp/agi-iter1.log

# Then check:
ls sessions/iter-001/a00-*/
tail -50 sessions/iter-001/a00-*/output.log

# Should NOT contain: "Token Plan", "anthropic 429", "api.anthropic.com"
# Should show: minimax-style output (this verifies env-leak fix)
```

For T-056, separate test:
```bash
cd ~/.hermes/agi-tree
pi --print "test" 2>&1 | grep -i "bridge\|extension"
# expect: "[autoresearch-tree-bridge] loaded" or similar
```

## Risks identified during fold

1. **agi-tree dirty working tree** (TODO F4) — must resolve before T-067 push.
2. **`.claude/skills/gitnexus/` accidentally tracked** (TODO C6) — clean before T-066 push.
3. **gensim/umap dependencies** (TODO H7) — embeddings sanity check needs them installed; smoke run logged "ERR: ollama package not installed" (irrelevant for current path).
4. **`master` vs `main` branch naming** (TODO F2) — kits referenced "main"; agi default is `master`. Operations target `master`.
