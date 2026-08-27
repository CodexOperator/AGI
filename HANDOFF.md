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

# SESSION HANDOFF — 2026-08-27 (evening): thought, and evidence that resolves

> **Read this section first if you are the next session.** Everything above is
> the install/orientation guide and is still broadly correct. This section is
> the current state and the work queue.

## 0. State as of commit `d559a1a90` (engine `3fe6cba`)

```
node_count            789          goal_count             83
evidence_fraction     0.206        primary (outcome_cov)  0.255
unevidenced_decisive  0            shadow_decisive        0
thought_coverage      0.003        nodes_with_thought     2
engine tests          755 passed, 1 skipped
```

Graph clean, engine clean, `publish-engine.sh --dry-run` reports all gates
passed. `--render --check` round-trips byte-identical.

## 1. 🔴 PRIORITY — the interpreter flap, and the silent cron behind it

**The user has named this and §4.1 as the two things to fix next, ahead of
everything else. Do not start further feature work until both are done.**
Owned by **S19** (the flap) and **G7.10** (the silence that let it hide).

### The workaround you need immediately

**`python3` on an interactive shell here is 3.11 (a hermes venv early on
`PATH`). The `:37` publish cron uses `/usr/bin/python3`, which is 3.12.**
`ast.unparse` renders f-strings differently across the two (PEP 701), so
`level3.py` derives a different contract depending on who ran it, and the graph
flaps dirty between them — burning a real grid version each way on a file
nobody edited.

```bash
export PATH=/usr/bin:$PATH      # do this first, every session
```

Written up as **S19**, with the durable fix specified (derive `how` from
`ast.get_source_segment` — source bytes are interpreter-independent by
construction) and deliberately not done, because it rewrites a large share of
2,692 contract entries and wants its own commit and its own before/after count.
Blast radius today is exactly 1 node, so the flap itself is annoying rather
than dangerous. **What is dangerous is that nothing told anyone.**

### The real defect: the cron can fail forever and say nothing — G7.10

Gate 1 of `publish-engine.sh` refuses when the graph is dirty. That gate is
correct. Everything around it is not:

- It refused **40 consecutive times, with 0 successful publishes ever**, from
  install on 2026-08-25 until someone checked by hand on 2026-08-27.
- The refusal goes to a log nobody reads. No metric moves, `--smoke` says
  nothing, `INJECTION.md` says nothing.
- **A refusal is not a no-op.** It mutates the graph at step 1 before refusing
  at step 3 — a refused run left 184 junk nodes behind during the last rename.
- S19 made it *intermittent* rather than permanent, which is worse: it looks
  healthy half the time, which is exactly when nobody investigates.

**G7.10 has the full design.** Build order, and the reasoning is in the goal
node, not repeated here:

1. **An alarm that moves a number** — `hours_since_successful_publish` from
   `metrics.py`. This idiom has already caught one defect that would otherwise
   have shipped (`shadow_decisive_verdicts`, 0 -> 1). A failure that does not
   move a metric is one this project cannot see.
2. **Non-zero exit + a durable marker the `SessionStart` hook surfaces**, so
   the next agent to open any session is told rather than having to suspect it.
3. **Branch and continue** — publish to `cron/pending-<graph-sha>` instead of
   stopping, so the bytes always land and a human fast-forwards later. This is
   the recommended default: it preserves both invariants at once.
4. **Make the refusal atomic** — today step 1 writes and step 3 refuses.

Worth saying in the failure message itself, because it is the reasonable fear
and it is wrong: **payload bytes are never lost when a publish stalls.**
`grid.py commit --all` runs on its own ungated 5-minute cadence. Only the
engine publish is blocked.

## 2. What changed this session

**G2.10 fixed — a build node can hold a thought.** `write_frontmatter` gained
`preserve_body=`; the body now has two named regions, `BUILD-CONTRACT`
(derived, rewritten every scan) and `THOUGHT` (authored, carried across).
`why`/`perf`/`security` carry over too, keyed on entry `name` rather than on
`how` — `how` embeds a line number, so keying on it would drop a rationale the
first time anything above the call site moved. Falsifier run on the live
corpus, twice: both survived.

**G2.11 minted and closed — the general form.** `body` is state, `thought` is
delta.
Declared in all 14 active schemas, `CLAUDE.md` and `SKILL.md`. Absent means
empty, so it churned 0 of 788 nodes. Readers strip it, so it never reaches
`GOALS.md` or injected context.

`thought_coverage` sits at 2/789 and **that is the design, not a residual**:
absent means empty, and fabricating reasoning for 786 nodes after the fact is
explicitly forbidden because a made-up thought reads as evidence. Recovering
real reasoning from stored sessions is **G10.1**'s job. Do not "improve" this
number.

**G7.3 closed — a bare integer is no longer evidence.** Only a reference that
resolves to a real node counts. All 12 live instances handled without
inventing a citation; see the goal node for why 11 were correctly left alone
and why the 12th was *not* demoted.

**S14's residual closed.** The two `write_frontmatter` copies had already
drifted: `snapshot-build-site.py`'s was missing both null round-trip fixes, so
a `None` list entry and a YAML-null scalar each came back as the string
`"None"` — silent corruption in the writer touching all 159 build-site nodes
every iteration. Collapsed to one definition.

**S7 amended — it is worse than recorded.** See §3.

## 3. S7 is now unfixable-by-rerun

Seed wiring lived in the `GOALS.md -> nodes` direction. **G6.9 reversed the
arrow and `driver.sh` now runs only `--render`, so S7's "a second run adds it"
became "no run ever adds it."** A sub-goal added after 2026-08-25 gets a
correct `parents:` and its parent is *never* told.

Five edges were missing, and every one was a recently-added sub-goal — three of
them the previous handoff's own next items (`g1.7`, `g4.5`, `g7.9`). The newest
work is reliably the work invisible from above. **Data repaired by hand; the
defect is open.** The fix has to be re-homed into the render direction, and
S7's original ask still stands: assert the fixed point in a test.

Check it in one line:

```bash
python3 - <<'EOF'
import pathlib, yaml
n={}
for p in pathlib.Path("nodes").rglob("*.md"):
    t=p.read_text()
    if t.startswith("---"):
        try: fm=yaml.safe_load(t.split("---",2)[1]) or {}
        except Exception: continue
        if fm.get("id"): n[fm["id"]]=fm
print([(a,b) for b,fm in n.items() for a in (fm.get("parents") or [])
       if a in n and b not in (n[a].get("seeds") or [])
       and a.startswith("goal:") and b.startswith("goal:")])
EOF
```

## 4. Next most valuable, in order

**The first two are set by the user, 2026-08-27, and are not to be reordered:
`@v2` first, then the §1 pair. Everything after that is the usual judgement
call.**

1. **G2.10's open half — the `@v2` collapse.** The five `origin: build-version`
   nodes hold ~47,000 characters of reasoning that now *has* somewhere to go.
   Sequence: migrate each body into its v1 node's `THOUGHT` region, verify,
   then retire the convention. **Retiring deletes 5 nodes and drops the node
   count, so get explicit sign-off before removing anything** — the migration
   itself needs none. Also note `SKILL.md`, `grid.py`, `stitch.py`,
   `find-root.sh` and `identity.py` all resolve `@v2` as head on publish, so
   **check which ref a payload edit actually landed in before trusting it**;
   two nodes share each of those `payload_ref`s.

2. **S19 + G7.10 — the interpreter flap and the silent cron. See §1.** Do
   G7.10's alarm first even if S19 takes longer: the alarm is what makes every
   *future* stall visible, and it is a `metrics.py` addition, not a redesign.
   S19's fix is one function (`_unparse_safe` -> `ast.get_source_segment`), but
   it rewrites a large share of 2,692 contract entries, so it wants its own
   commit with a before/after count and a two-interpreter diff as its
   falsifier.

3. **S7** — §3. Cheap to detect, and it silently hides exactly the work that is
   current. The fix has to be re-homed into the render direction now that the
   arrow is reversed; S7's original ask (assert the fixed point in a test)
   still stands.

4. **G7.9** — `level3.py` should not prune quietly, and is misnamed
   (`view.py`/`main.py`). *The user has said they have more pieces of this in
   mind — ask before starting.* Note its overlap with G7.10 item 4: a refused
   `publish-engine.sh` mutating the graph before refusing is the same
   non-atomicity defect seen from the other side.

5. **G1.7** — the demotion path is four fields (`verdict`, `status`,
   `demoted_from`, `demote_reason`) and `evidence_gate` owns one. Reproduced
   live: a correctly-gated demotion left `status: proved` contradicting the
   demoted `verdict:` underneath. `shadow_decisive_verdicts` is currently 0 and
   is the regression alarm — it caught this once already, so leave it in.

6. **S18** — absorb cavekit references before cavekit retires. The hazard is
   *ordering*: deleting `context/kits/` prunes 159 `origin: build-site` nodes
   (H0i).

7. **G4.5** — generalize `blocked_by` -> `depends_on`. 89 populated nodes, 0
   cycles, max depth 15. Must stay out of every metric traversal or it becomes
   a fresh gaming surface.

## 5. Traps hit this session — do not re-learn these

- **The interpreter, twice.** §1.
- **`level3.py` run from `payloads/` makes `payloads/` the engine root** and
  correctly refuses with "discover_files returned zero files". Use
  `--engine-root /home/ubuntu/work/agi --project /home/ubuntu/work/agi-tree`
  to exercise an unpublished change against the real graph.
- **`stitch.py` already imports `level3.py`,** so level3 borrowing the contract
  reader back was an import cycle and died with `RecursionError`. Ownership
  decides direction: level3.py owns the contract shape, stitch aliases it.
- **Inserting one sub-goal renumbers every goal after it.** `order` is unique
  and positional (`int`, duplicates are a hard error), so G2.11 at order 19
  meant bumping 61 nodes. Mechanical and safe, but budget for the diff.
- **A test asserting a hole will fail when you close it.** 10 did. Six asserted
  `evidence_runs: 3` counted; one asserted `metrics.py` and `dashboard.py`
  *disagreed* and called the gap "the contamination the dashboard exists to
  name". Read each failure before fixing it — they were documentation of the
  defect, not regressions.
- **Widening a CLI flag can turn a soft demotion into a hard rejection.**
  `--evidence-runs` taking ids made `--evidence-runs 0` arrive as `["0"]`,
  which the taxonomy check treated like the `synthetic` sentinel: exit 2,
  nothing written, work discarded. Rejection is for claims that are actively
  false.

## 6. How to write into this file

`HANDOFF.md` is `build:HANDOFF.md`, `build_kind: prose`. **Edit the payload.**
The `BUILD-CONTRACT` block and the derived prose around it are regenerated on
every scan; only a `THOUGHT` region would survive there now (G2.10).

```bash
export PATH=/usr/bin:$PATH                              # 1. match the cron
python3 agi/extensions/agi/bin/grid.py checkout --all   # payloads/HANDOFF.md
$EDITOR payloads/HANDOFF.md
python3 agi/extensions/agi/bin/grid.py commit --all
bash agi/extensions/agi/bin/publish-engine.sh
git add -A && git commit                                 # LAST
```

**The order matters and is not the obvious one.** `payloads/` is gitignored, so
`git add -A` finds *nothing* right after a payload-only edit, and a commit
attempted there silently does nothing while you believe your reasoning was
recorded. The node file only changes once `publish-engine.sh` re-derives its
contract from the published payload.

## 7. Known-good verification sequence

```bash
export PATH=/usr/bin:$PATH
bash agi/extensions/agi/driver.sh --smoke --max-iters 1        # count must not drop
cd payloads && python3 -m pytest extensions/agi/tests/ -q      # 755 passed, 1 skipped
python3 agi/extensions/agi/bin/snapshot-goals.py --render --check
bash agi/extensions/agi/bin/publish-engine.sh --dry-run        # every gate, no writes
```
