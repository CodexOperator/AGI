# QUICKSTART — agi, from zero on a new machine

> **Standing content.** Assumes **nothing** exists locally: no clone, no deps,
> no CLI, no auth. This does not change from session to session, which is
> exactly why it is not in `HANDOFF.md` — that file is replaced wholesale by
> each director and standing instructions would be destroyed by the first one
> to do it. Split out of `HANDOFF.md` on 2026-09-02.

**Where the rest of the knowledge lives:**

| Question | Read |
|---|---|
| What is agi, and why is it shaped this way? | `skills/agi/SKILL.md` |
| What is committed to, and what is being worked now? | `GOALS.md` (rendered from `.agi/nodes/goal/`) |
| What does the repo contain, and how do I run the loop? | `CLAUDE.md` |
| What does any given engine file do? | its build node — `.agi/nodes/build/*.md`, one per file |
| What is the CURRENT session doing, and what is next? | `HANDOFF.md` — one section, always current |
| What did an EARLIER session do? | `grid.py payload build:HANDOFF.md --version N` |

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
- **PROJECT_ROOT** — the **graph directory**, `<repo>/.agi/`: holds `config.json`, `nodes/`, `context/`, `sessions/`. Resolved by `bin/locations.py` walking up from cwd for the nearest enclosing `.agi/` that holds a config (`goal:g11`, `goal:g8.2`) — **nearest wins, no flag, no project name anywhere**. `$AGI_TREE_PROJECT_ROOT` (legacy `$AUTORESEARCH_TREE_PROJECT_ROOT`) still overrides. A pre-`goal:g11` project with a bare `agi-tree.config.json` at its repo root still resolves.
  - *Corrected 2026-09-02.* This entry still described the two-repo layout — a separate graph repo with `agi-tree.config.json` at its root — which `goal:g11` removed. Note the consequence: `PROJECT_ROOT` is `<repo>/.agi`, **not** `<repo>`, which is exactly the confusion that made `snapshot-goals.py` look for `<repo>/nodes/goal` and refuse (`goal:g11.1`).
- **Capillary DAG** — the chain shape above: many thin chains, not one thick trunk.

---


<!-- COMMANDS:BEGIN -->
<!-- This section is AUTO-GENERATED from `.geometry/commands.md`.
     Edit the node — never this table directly. -->

| Command | Does |
|---|---|
| `bash '<engine>/extensions/agi/driver.sh' --smoke --max-iters 1` | snapshot + render + metrics, no dispatch — verify the node count did not drop |
| `python3 -m pytest '<engine>/extensions/agi/tests/' -q` | the engine's own suite |
| `python3 '<engine>/extensions/agi/bin/snapshot-goals.py' --render --check` | GOALS.md and the goal nodes are byte-identical inverses |
| `python3 '<engine>/extensions/agi/bin/viewport.py' --verify` | goal:g9.7 — one render, two readers |
| `python3 '<engine>/extensions/agi/bin/grid.py' commit --all` | version every changed node and its payload |
| `python3 '<engine>/extensions/agi/bin/links.py' links` | goal:g13 — every node's link resolves; broken_links must be 0 |
| `python3 '<engine>/extensions/agi/bin/links.py' schema` | goal:s31 — which nodes violate their type's required list (dry) |
| `python3 '<engine>/extensions/agi/bin/spawn_budget.py' status` | goal:g4.8 — live agents against the tree-wide bound |
| `python3 '<engine>/extensions/agi/bin/provisioning.py' status` | goal:g1.11 — whether per-spawn keys are being issued |
| `python3 '<engine>/extensions/agi/bin/envfile.py' --check` | goal:g1.8 — required keys present, forbidden keys absent |
| `python3 '<engine>/extensions/agi/bin/crons.py' show` | the crontab the graph declares |
| `python3 '<engine>/extensions/agi/bin/viewport.py' --live` | the live graph, agents drawn as spiders where they are working |
| `python3 '<engine>/extensions/agi/bin/viewport.py' --emit llm` | goal:g9.7 — exactly what a kid is handed, from the same frame stream |
| `python3 '<engine>/extensions/agi/bin/viewport.py' --emit both` | human and llm views side by side, from ONE stream |
| `python3 '<engine>/extensions/agi/bin/write.py'` | goal:g13.1 — named node operations; a hand edit becomes an engine action |
<!-- COMMANDS:END -->

## Write guard hook (goal:g13.1, L2 wave 1.5)

Every sanctioned node write is logged to `.agi/sessions/write-log.jsonl`; `write_guard.py check` warns about any node changed outside `write.py` (the smoke path runs it, warn-only). To refuse such commits locally, install the hook once per clone:

```bash
mkdir -p .githooks && python3 extensions/agi/bin/write_guard.py hook > .githooks/pre-commit && chmod +x .githooks/pre-commit
git config core.hooksPath .githooks
```
