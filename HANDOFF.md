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
cd ~/work/agi && python3 -m pytest extensions/agi/tests/ -q   # 723 passed, 1 skipped
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
