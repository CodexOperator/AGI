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
- **PROJECT_ROOT** — the graph repo: holds `agi-tree.config.json`, `nodes/`, `context/`, `sessions/`. From `$AGI_TREE_PROJECT_ROOT` (legacy `$AUTORESEARCH_TREE_PROJECT_ROOT`) or by walking up from cwd.
- **Capillary DAG** — the chain shape above: many thin chains, not one thick trunk.

---

# SESSION HANDOFF — 2026-08-29: the publish path is closed, end to end

> **Read this section first if you are the next session.** Everything above is
> the install/orientation guide and is still broadly correct. This section is
> the current state and the work queue.

## 0. State as of commit `65b2a6dd3` (engine `11a8e62`)

```
node_count            792          goal_count             85
active_node_count     787          deprecated_node_count  5
evidence_fraction     0.206        primary (outcome_cov)  0.255
unevidenced_decisive  0            shadow_decisive        0
thought_coverage      0.015        nodes_with_thought     12
hours_since_publish   0.34         publish_blocked_reason (empty)
unpushed_graph        0            unpushed_engine        0
engine tests          861 passed, 1 skipped
```

Graph clean, engine clean, **both remotes current**. `--render --check`
round-trips byte-identical across 85 goals.

## 1. What shipped — four iterations, 2026-08-28/29

The previous handoff's whole queue above S7 is done. **S19, G7.10 and S20 are
all closed**; do not re-open them looking for work.

**S19 — `how` quotes the payload instead of re-rendering the AST.** `_render(source, node)`
returns `ast.get_source_segment`, the literal slice of the payload's own bytes,
joined onto one line. Source bytes are interpreter-independent by construction.
`3.12 → 3.11 → 3.12` against the live corpus now leaves `nodes/` byte-identical
at every step; before, it moved a hunk every time. The node's own blast-radius
estimate was wrong in both halves and is corrected in place: 363 entries
(12.9%) across 55 of 186 build nodes changed value, not "exactly 1 node".
`ast.arguments` deliberately keeps `ast.unparse` — `get_source_segment` returns
`None` for all 1,241 signatures — licensed by measurement and guarded by
`test_no_engine_signature_contains_an_fstring`.

**G7.10 — all four parts, goal closed.** Part 3: a `graph-dirty` refusal parks
the publishable tree on `cron/pending-<graph-sha>` in the engine, **local, never
pushed**, via a `git worktree` outside both repos. Part 4: `level3.py` derives
into a throwaway worktree of the graph and `nodes/` is not written until gate 2
passes. Head-to-head on identical clones with 6 genuinely-moved contracts —
**old path: 6 junk nodes, 6 grid versions burned; new path: 0 and 0.**

**S20 — the alarm reaches the remote.** `hours_since_successful_publish` stopped
at the local commit, so an engine remote 3 days and 25 commits behind moved no
number and was found by looking at GitHub. `metrics.py` now emits
`unpushed_{graph,engine}_commits` from `git rev-list --count @{upstream}..HEAD`
— a **gap**, not an event, because a timestamp can read fresh while work is
stranded. `-1` with a reason token (`no-upstream`, `detached-head`,
`not-a-repo`, `missing`) for every blind spot; `0` never means "could not tell".
No network I/O — the only two occurrences of "fetch" in `metrics.py` are the
comments explaining why one is not called.

**The `export PATH=/usr/bin:$PATH` workaround is no longer load-bearing.** S19
removed the interpreter dependency, so 3.11 and 3.12 now derive identical
contracts. Still worth doing to match the cron exactly, but a session that
forgets it no longer dirties the graph.

## 2. 🔴 The one live trap: a derivation change takes two publishes

**`publish-engine.sh` runs `level3.py` from the ENGINE at step 1, then installs
the new engine at step 3.** So a change to *derivation logic itself* cannot
converge in a single publish.

Publishing S19 re-derived all 55 affected nodes with the **pre-change** renderer,
then shipped the **post-change** renderer over the top — leaving the graph dirty
with a clean revert of the commit that had just landed. It looks alarming and it
is not: one more re-derivation with the now-published engine converges it to
zero.

```bash
python3 /home/ubuntu/work/agi/extensions/agi/bin/level3.py \
  --project . --engine-root /home/ubuntu/work/agi --from-grid
```

Benign and self-correcting, but it arms gate 0 in the window, so **expect it and
do not go hunting for a bug.** Only matters when you change `level3.py`'s own
derivation; every other payload publishes in one pass. Not fixed, not yet
written up as a goal.

## 3. S7 — open, but currently repaired

Seed wiring lived in the `GOALS.md -> nodes` direction. **G6.9 reversed the
arrow and `driver.sh` now runs only `--render`, so S7's "a second run adds it"
became "no run ever adds it."** A sub-goal added after 2026-08-25 gets a correct
`parents:` and its parent is never told.

**The detector currently reports 0 missing edges** — the five that were missing
were repaired by hand, and S20 was minted with `parents: []`, which sidesteps
it entirely. So there is no live damage today; the defect is that nothing
prevents recurrence. The fix has to be re-homed into the render direction, and
S7's original ask — assert the fixed point in a test — still stands.

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

**Judgement call, not a ranking handed down.** Nothing on this list is currently
armed to lose data.

1. **S7** — §3. Cheap to detect, and it silently hides exactly the work that is
   current: the newest sub-goals are the ones that go missing from above. Zero
   damage right now, which makes this the calm moment to close it.

2. **G7.9** — `level3.py` should not prune quietly, and is misnamed
   (`view.py`/`main.py`). *The user has said they have more pieces of this in
   mind — **ask before starting**.* Its overlap with the old G7.10 part 4 is now
   resolved from that side: a refused publish no longer mutates first.

3. **G1.7** — the demotion path is four fields (`verdict`, `status`,
   `demoted_from`, `demote_reason`) and `evidence_gate` owns one. Reproduced
   live: a correctly-gated demotion left `status: proved` contradicting the
   demoted `verdict:` underneath. `shadow_decisive_verdicts` is 0 and is the
   regression alarm — it caught this once already, so leave it in.

4. **`grid.py commit` can drop a payload entry, silently.** Named during G7.10
   part 4 and deliberately left: it takes no `--engine-root`, so it resolves
   payloads against its own on-disk location and, finding nothing, records a
   version with the `payload` tree entry **missing**. Latent — `<project>/payloads/`
   wins resolution first, so it never fires in production — but
   `stitch.py --from-grid --grid-version N` materialises history out of exactly
   those refs, so the corruption would surface much later and far from its
   cause. Make it refuse loudly rather than write a truncated version.

5. **S21** — the graph can add a file to the engine but can never remove one.
   Filed 2026-08-29, not built. The publish path is one-directional for
   existence: nothing lets the graph say "this payload is retired, stop
   materialising it". **Deprecating a build node does NOT remove its engine
   file** — `stitch.py` reads `nodes/deprecated/build/` precisely so it keeps
   materialising those payloads, and that is correct. All four obvious routes
   fail differently; the node lists each with the code that decides it. **Do
   this before S18**, which ends in retiring files and cannot finish without it.

6. **S18** — absorb cavekit references before cavekit retires. The hazard is
   *ordering*: deleting `context/kits/` prunes 159 `origin: build-site` nodes
   (H0i). Gated on S21.

7. **G4.5** — generalize `blocked_by` -> `depends_on`. 89 populated nodes, 0
   cycles, max depth 15. Must stay out of every metric traversal or it becomes
   a fresh gaming surface.

Also named and deliberately unfixed: **gate 2 now certifies the tree as
*derived*, not as *published***, so a `payloads/` edit landing mid-run ships
bytes one derivation ahead of their contract. Strictly better than what it
replaced — the old ordering turned the same race into a refusal *plus* junk
nodes — and the next `:37` converges it.

**Do not "improve" `thought_coverage`.** Still the design at 11/791: absent
means empty, and fabricating reasoning after the fact is forbidden because a
made-up thought reads as evidence. Recovering real reasoning from stored
sessions is **G10.1**'s job.

## 5. Traps hit — do not re-learn these

- **A derivation change takes two publishes.** §2. The only one of these that
  will make you think you broke something.
- **`publish-engine.sh` no longer re-derives before it refuses** — that was
  G7.10 part 4 and it is fixed. If `git status` shows node files you did not
  touch after a *refused* publish, that is a regression, not the old normal.
- **A `@v2` node is the publish head, not the v1 node.** `grid.py commit --all`
  writes an edited payload to *every* node sharing that `payload_ref`, so both
  refs stay in sync — but **verify before publishing**, because the head is what
  ships: `grid.py payload 'build:<name>@v2' --out /tmp/x && diff`. The five
  `@v2` nodes are deprecated and still resolve as chain head.
- **A `how:` field embeds a line number**, so adding a comment block near the
  top of an engine file re-derives every contract entry below it. Expect a
  large, boring diff and one extra commit; it is not drift.
- **`level3.py` run from `payloads/` makes `payloads/` the engine root** and
  correctly refuses with "discover_files returned zero files". Use
  `--engine-root /home/ubuntu/work/agi --project /home/ubuntu/work/agi-tree`
  to exercise an unpublished change against the real graph.
- **`stitch.py` already imports `level3.py`,** so level3 borrowing the contract
  reader back was an import cycle and died with `RecursionError`. Ownership
  decides direction: level3.py owns the contract shape, stitch aliases it.
- **Inserting one sub-goal renumbers every goal after it.** `order` is unique
  and positional (`int`, duplicates are a hard error). Appending at the end
  costs nothing — S20 took order 83 after S19's 82 and renumbered zero nodes.
- **A test asserting a hole will fail when you close it.** Read each failure
  before fixing it — several were documentation of a defect, not regressions.
- **Whitespace normalisation is not `\s+`.** In `f"a:\n  b"` the `\n` is two
  source characters and the spaces after it are *content*. Collapsing `\s+`
  silently rewrites indentation inside string literals, in an engine whose main
  output is YAML and markdown. Collapse only runs that *contain* a real line
  break, and assert the quoted fragment is a verbatim substring of the payload
  rather than that it merely looks right.

## 6. How to write into this file

`HANDOFF.md` is `build:HANDOFF.md`, `build_kind: prose`. **Edit the payload.**
The `BUILD-CONTRACT` block and the derived prose around it are regenerated on
every scan; only a `THOUGHT` region would survive there (G2.10).

```bash
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
bash agi/extensions/agi/driver.sh --smoke --max-iters 1        # count must not drop
cd payloads && python3 -m pytest extensions/agi/tests/ -q      # 861 passed, 1 skipped
python3 agi/extensions/agi/bin/snapshot-goals.py --render --check
bash agi/extensions/agi/bin/publish-engine.sh --dry-run        # every gate, no writes
```
