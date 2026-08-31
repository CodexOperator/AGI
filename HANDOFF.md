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

# SESSION HANDOFF — 2026-08-30: the migration's residuals, closed

> **Read this section first.** It supersedes 2026-08-29b below wherever they
> disagree — in particular §1 of that section, which says the repo is unpushed
> and blocked on a remote decision. **Both halves of that are now false.**

## 0. State

```
repo         /home/ubuntu/work/agi   ONE repo: source + .agi/ graph + refs/grid/*
HEAD         efa7ea347               714 commits, 1087 grid refs
node_count   816                     active 811, deprecated 5, goal_count 91
tests        1049 pass, 0 fail       metric outcome_coverage 0.283 (was 0.255)
crons        FROZEN — crons_live: false. See §4.
PUSHED       master is 2 commits ahead of origin. Grid refs are current.
```

## 1. The remote question is SETTLED. Do not reopen it.

The previous section called the push blocked pending a new repo name. It was
not blocked — **the hourly `branch_push` cron had already published everything
to `CodexOperator/agi`** before anyone decided anything. `git rev-list
--left-right --count origin/master...HEAD` read `0 0`.

The owner's decision, 2026-08-30, is that **the `agi` name stays on the live
repo**. Three repos, and this is the final shape:

| repo | holds | commits |
|---|---|---|
| `CodexOperator/agi` | **canonical and live.** The unified repo, keeping its split-era history. `origin` points here. | 714 + 1087 grid refs |
| `CodexOperator/agi-archive` | the engine immediately before the merge: `21308535f`, no `.agi/` | 210 |
| `CodexOperator/agi-tree` | the pre-migration graph repo, untouched | — |

`agi-archive` was created and pushed 2026-08-30. It is push-once; **no local
remote was added for it**, deliberately, so nothing can accidentally push there
again. The rename-to-archive plan was dropped because, post-push, renaming
`agi` would have produced two identical repos and a true engine-only archive
would have needed a force push against published history.

## 2. What landed, 2026-08-30 — two iterations, four kids

**iter-5 (`b124133d3`) — the two post-migration bugfixes.**

- **All ten `bin/` entry points delegate to `locations.py`.** `goal:g11.1` is
  closed; its falsifier (`grep -c '^CONFIG_NAMES' extensions/agi/bin/*.py`)
  went 11 → 1. The goal said ten *duplicates*; the measurement said ten
  *breakages* — no `agi-tree.config.json` or `autoresearch-tree.config.json`
  exists anywhere in this repo, so every copy of the legacy walk was already
  dead code resolving nothing. Seven failed hard, two answered `os.getcwd()`
  with no walk at all, one had the right root and a wrong config lookup.
- **`grid.py` takes two roots** — `repo_root` for every git invocation,
  `graph_root` only for finding node files. `grid.py status` went from
  reporting 809 byte-identical nodes as `CHANGED` to reporting 0. `--full-tree`
  was proven **not load-bearing** once the roots are split (stripped: 68/68
  pass; conflation restored: 5–7 fail). Both spellings shipped anyway, now
  provably belt-and-braces. `cmd_diff` was separately returning an empty diff
  and exit 0 — `git diff` has no `--full-tree`, so the flag never covered it.

**iter-6 (`efa7ea347`) — the residuals.**

- **`order:` is retired.** `GOALS.md` renders by natural `goal_id` sort. The
  new document is a byte-exact permutation of the old: identical size, empty
  sorted-line diff, all 70 G-goals in place, only S1..S17 rotated out of
  historical order.
- **`cron:crons` can finally say which value kills.** See §4.
- **`metrics.py` no longer measures the retired publish boundary.** Four dead
  metrics removed; `unpushed_graph_*` fixed and renamed to `unpushed_commits`/
  `unpushed_reason`, routed through `locations.repo_root()` — the `not-a-repo`
  sentinel was it treating `.agi/` as its own repo. **No metric reports a
  sentinel in place of a measurement any more.**

**Three live bugs found in passing, none of which anyone was looking for:**

| bug | what it would have done |
|---|---|
| `snapshot-goals.py` lost `.agi/config.json`, fell back to `BODY_CAP=4000` | written **26 of 91 goal NODE bodies truncated** on the next `--snapshot`. `driver.sh` only runs `--render`, which is the only reason it had not fired |
| `zoom.py::default_runtime` returned `pi`, not `cc` | handed every Claude Code kid the **wrong completion contract** — `goal:s8`, silently re-broken by the layout change |
| `snapshot-build-site.py` answered `os.getcwd()` with no walk | run its prune against the wrong tree. The 159 build-site nodes survived **only because the missing-`build-site.md` guard returns before the unlink** — the guard, not the resolver |

That last one has since been exercised for real: with the resolver fixed the
prune path is reachable for the first time, and it re-derived exactly
`7 idea + 61 hypothesis + 91 task = 159` and changed nothing.

## 3. 🔴 Next tasks, in order

### 3a. 🔴 ONE MANUAL STEP REMAINS: paste the OpenRouter key (goal:g1.8)

**Added 2026-08-31. Item one because no paid iteration runs until the value is
on the box, and the value is the one thing an agent must never touch.**
Everything around it landed this session:

```
.env.example                     committed — the SHAPE of the secret set, has a build node
.env                             gitignored, mode 0600 — the VALUES, never committed  ← MISSING
.agi/nodes/.geometry/secrets.md  DECLARES both paths + required/optional/forbidden keys
extensions/agi/bin/envfile.py    the one reader — resolves the node, checks the file
extensions/agi/driver.sh         asks envfile.py, runs the check, sources the file
extensions/agi/bin/env-get.sh    prints one value; for pi auth.json's "!command" form
~/.pi/agent/auth.json            openrouter entry → env-get.sh (pointer, not a copy)
~/.pi/agent/settings.json        default model qwen/qwen3.8-27b; both OR models registered
.agi/config.json                 agent_dispatch → openrouter / z-ai/glm-5.3-flash / medium
```

Backups of both pi files are at `~/.pi/agent/*.bak-2026-08-31`.

**Do this over SSH. Never paste the key into an agent session — not into a
prompt, not into a file an agent then reads back:**

```bash
cd /home/ubuntu/work/agi && cp -n .env.example .env && chmod 600 .env && read -rs -p 'OPENROUTER_API_KEY: ' K && printf 'OPENROUTER_API_KEY=%s\n' "$K" >> .env && unset K && bash extensions/agi/driver.sh --smoke --max-iters 1 2>&1 | grep secrets
```

Expected last line: `[driver] [secrets] ok: /home/ubuntu/work/agi/.env satisfies
required keys: OPENROUTER_API_KEY`. Then confirm pi resolves it — this is the
step that proves the indirection works and that the model slugs match:

```bash
pi --list-models | grep -E 'qwen3.8-27b|glm-5.3-flash'
```

**If those two lines do not appear, the model id string is what to adjust**, in
`~/.pi/agent/settings.json` — `providers.openrouter.models[].id` and
`agents.default.model`. pi's baked registry does not know either model (checked:
it knows `z-ai/glm-5` and `glm-5.1`, not `5.3-flash`), which is why they are
registered explicitly rather than merely named. Both ids are real —
`https://openrouter.ai/api/v1/models` lists them — so a mismatch is pi's
matching rule, not a wrong slug.

**Model routing, as decided 2026-08-31.** pi general default and the parent
role: `qwen/qwen3.8-27b` ($0.43/$2.55 per Mtok, 1M ctx). Kid role:
`z-ai/glm-5.3-flash` ($0.075/$0.25, 1M ctx) — ~6x cheaper in, ~10x out, which
is the right shape for the tier that does the most talking.

🔴 **`cc_dispatch` cannot be pointed at OpenRouter, and this is a hard limit,
not a config gap.** Claude Code's subagent tool spawns Claude models only;
there is no setting that makes a CC kid an OpenRouter model. So OpenRouter is
reachable **through the pi runtime only** (`driver.sh --max-iters N`) until
someone writes an OpenRouter dispatcher — G1.8 item 4, and the decision there
is already made: **use the OpenRouter Python SDK, not raw HTTP**, so a minor
change on their side cannot silently break the loop. `cc_dispatch` stays on
Claude models and the main chat stays on the Anthropic subscription, which is
what was asked for anyway.

**Fixed in passing, and it was silently defeating every model setting:**
`dispatch.py::_build_pi_args` read `agent_dispatch` and then used none of it —
every pi kid ran whatever `~/.pi/agent/settings.json` said, while the config
key that claims to choose the model chose nothing. It now passes `--provider`,
`--model` and `--thinking` (the `goal:g4.2` dial) when set, and passes nothing
when unset, so a project that configures none of them is unaffected.
`tests/test_dispatch.py` covers both directions.

**Still open — G1.8 items 2–4:** `init` rendering the `.env` stub (G1.5's job);
a verifier that no tracked file, grid ref or session transcript ever contains a
value from `.env`; and the OpenRouter dispatcher above.

**The one hard rule, restated because it is the failure mode with teeth:**
never put `ANTHROPIC_API_KEY` or a `CLAUDE_CODE_*` var in `.env`.
`dispatch.py` scrubs exactly those from pi children so subagents cannot bill
the interactive Claude Code subscription; setting one in `.env` re-adds that
leak from *below* the scrub, where nothing checks. `envfile.py` enforces the
three `ANTHROPIC_*` names as a floor a project's own node cannot lower.

### 3b. The goal sweep. `METRIC_WARNING goal_rotation=45/3` fires every run.

45 goals are `status: active` against `cc_dispatch.max_goals_active: 3` — 44,
plus `G1.8` added by §3a above, which is genuinely in flight and should be among
the first retired once its items 1–3 land.
**This is not only over-declaration — several are finished and mislabelled:**

- `G11` — one repo. Landed 2026-08-29. Should be `complete`.
- `G11.1` — closed by iter-5; its own falsifier passes. Should be `complete`.
- `G6.5` — "the cron rebuilds agi from agi-tree, then commits and pushes it".
  Describes the retired two-repo publish. `phasing-out`, superseded by G11.
- `S5` — "the engine repo has no sync at all". The crons sync it.
- `S8` — "`zoom.py` bakes the pi-runtime completion contract into the kid
  context". iter-5 fixed exactly that.

**So the job is classify-with-evidence, not demote-in-bulk:** complete /
phasing-out / horizon / at most three active. Retire by marking, never by
deleting; `node_count` must not drop.

One off-taxonomy value to fix while there: **`goal:S16` carries
`status: proved`** — a verdict value in a lifecycle field. The four states are
`active | horizon | phasing-out | complete`. The irony is that S16 is the goal
about the evidence gate leaving a `status` shadow behind.

### 3c. Config influence — what `.agi/config.json` should govern and does not

`locations.source_root` and `goals_file` exist. Log paths, remote name and the
branch to push are still computed or hardcoded. `crons.py` is already better
than the note in the previous section implied — it re-resolves the checked-out
branch at every `apply` and **refuses rather than guessing** `master`/`main`.

The cron-symlink question from the previous session still wants costing:
**not possible for crontab** (`/var/spool/cron/crontabs/<user>` is root-owned
and mode-checked; a symlink there is refused or ignored), but **`systemd --user`
timers CAN be symlinked** out of the repo, which would make the schedule a
tracked file. Interim win available without any of that: reduce to **one**
bootstrap cron line running `crons.py apply` and let the rest be graph state.

### 3d. Carried, unchanged

- **G6.6** — `build:CLAUDE.md` / `AGENTS.md` / `GOALS.md` exist but carry
  `parse_ok: false` and empty contracts. Give them real prose contracts.
- **Worktree-per-kid isolation (G4.1)** — now genuinely possible; one repo
  means a `git worktree` isolates source, graph and tests together.
- **`init` (G1.5)**, **G8.2 falsifier** (a third project reaching a rendered
  map with no engine change).
- **Cosmetic, but it misleads:** the SessionStart hook still prints
  `## agi-tree map` and `Run: agi-tree --max-iters N`. The command is `agi`.

## 4. 🔴 THE CRONS ARE FROZEN. Turning them back on takes a manual step.

`.agi/nodes/.geometry/crons.md` has `crons_live: false`, set deliberately at
the start of the 2026-08-30 session because a kid was editing `grid.py` —
the exact file the `*/5` job runs. **Nothing is scheduled right now: no grid
snapshot, no ref push, no branch push.**

To restore:

```bash
$EDITOR /home/ubuntu/work/agi/.agi/nodes/.geometry/crons.md   # crons_live: true
python3 /home/ubuntu/work/agi/extensions/agi/bin/crons.py apply
python3 /home/ubuntu/work/agi/extensions/agi/bin/crons.py show   # expect 2 lines
```

**The manual `apply` is required and is not a bug.** `false` removes all four
managed lines including `grid_sync`, and `grid_sync` is the job that re-runs
`crons.py apply`. So the switch is self-disabling in one direction and not the
other — off is one edit, on is one edit plus one command.

While frozen, **nothing pushes.** `git push` by hand if you need the remote
current; `master` is 2 commits ahead as of this writing.

## 5. 🔴 Traps from this session — do not re-learn these

- **Anchor the pattern before believing the number.** Twice in two iterations
  a loose `grep -rl` produced a confident wrong count that an anchored one
  refuted. `grep -rl 'origin: build-site'` returns **167** because eight nodes
  merely mention the marker in prose; `grep -rl '^origin: build-site$'` returns
  the true **159**. Same shape for `THOUGHT:BEGIN` vs `<!-- THOUGHT:BEGIN`.
  Both times the loose number was asserted first and corrected at review.
- **A doc bug can be produced mechanically and survive every version.**
  `cron:crons` said "`crons_live: X` removes every managed line … and
  `crons_live: X` brings all four back" — same X on both sides, at v1, at v2
  and at v3, because each edit replace-all'd the boolean through the prose as
  well as the frontmatter. Prose that embeds a key:value literal is prose a
  find-and-replace will silently corrupt.
- **A commit subject that names one change can carry another.** `27855bafc`,
  "retire two cadences the migration made meaningless", also flipped
  `crons_live` false→true and re-enabled every scheduled job. That is why the
  crons were believed off while they were running and pushing.
- **`git for-each-ref 'refs/grid/*'` returns 0.** The quoted glob does not
  match under `for-each-ref`'s pattern rules. Use `git for-each-ref refs/grid`.
  A brief handed to a kid with the wrong form nearly produced a "the refs are
  gone" finding.
- **Check the filesystem before resuming a dead kid.** Both iter-6 kids were
  cut off when the host process exited. One had landed everything and needed
  nothing; the other had done half its work and no node. Resuming with context
  intact beat respawning cold, and neither lost work.

## 6. Known-good verification sequence

```bash
cd /home/ubuntu/work/agi
bash extensions/agi/driver.sh --smoke --max-iters 1     # node count must not drop
python3 -m pytest extensions/agi/tests/ -q              # 1049 passed
python3 extensions/agi/bin/snapshot-goals.py --render --check   # 91 byte-identical
python3 extensions/agi/bin/locations.py . --json        # layout must be graph_dir
python3 extensions/agi/bin/crons.py show                # says: up to date
python3 extensions/agi/bin/grid.py status | grep -c CHANGED     # 0 on a clean tree
grep -c '^CONFIG_NAMES' extensions/agi/bin/*.py | grep -v ':0'  # exactly 1
```

---

# SESSION HANDOFF — 2026-08-29b: one repo. G11 landed.

> **Read this first.** Everything above is install/orientation and is now
> PARTLY WRONG — it describes the two-repo layout. §2 (bootstrap) and §6 (how
> to write into this file) are superseded by this section. `CLAUDE.md` and
> `SKILL.md` are correct and rewritten.

## 0. State

```
repo         /home/ubuntu/work/agi   ONE repo: source + .agi/ graph + refs/grid/*
HEAD         1c14c46a2               710+ commits, 1080 grid refs
node_count   812                     goal_count 91      tests 1029 pass, in place
metric       outcome_coverage 0.255  evidence_fraction 0.214
crons        2 lines, graph-driven, pointing at /home/ubuntu/work/agi/.agi
PUSHED       NO — 500+ unpushed commits. Deliberate. See §1.
```

`/home/ubuntu/work/agi-tree` and the `agi-tree` remote are the **archive and
fallback**, untouched: 809 nodes, 1080 refs, own history intact. S4's rule —
archive, never delete.

**The workflow is now: edit the file, run its tests, commit.** No `payloads/`,
no `grid.py checkout`, no `stitch --publish`, no `publish-engine.sh`. Those are
retired; the payload *is* the source file. `grid.py commit --all` **stays** —
it versions `node.md` and its payload together as one atomic version, which
plain git does not.

## 1. 🔴 BLOCKED ON A DECISION: where to push

Nothing is pushed. Two reasons, one hard and one procedural:

- **Rollback after a push needs a force push** against published history
  (`verdict:g11-migration-rehearsal` makes this a condition of the verdict).
- **The intended new remote name does not exist.** The owner asked for a fresh
  repo called `AGI`, keeping `agi` and `agi-tree` as archives. **GitHub repo
  names are case-insensitive for uniqueness — `CodexOperator/AGI` resolves to
  the existing `CodexOperator/agi`.** Verified with `gh repo view`. So "AGI" is
  not a new name; it is the old one.

Options, undecided, and the choice is the owner's:
1. A distinct name (`agi-mono`, `agi-one`, `agi2`) — no collision, no rename.
2. Rename `CodexOperator/agi` → `agi-engine-archive`, then create `agi` fresh.
   GitHub leaves a redirect, so the archive's old URL keeps resolving — which
   is either convenient or confusing.
3. Push to the existing `agi` remote. The unified repo *is* that repo's
   history plus the graph's; nothing is lost and no new remote is needed. What
   it costs is the clean separation between "archive" and "live" the owner
   asked for.

Whatever is chosen: **verify `verify_unified.py` reports 8/8 before pushing**,
and keep both existing remotes untouched until it does.

## 2. What landed, 2026-08-29

- **G11 — one repo.** `unify.py` migrated in place; the independently-written
  `verify_unified.py` reported 8/8 (809 nodes in/out, zero bytes changed, 1080
  refs preserved, 494 graph commits as real ancestors, 199/199 `payload_ref`
  resolving unchanged).
- **The first attempt FAILED and `--rollback` restored the repo exactly** —
  209 commits, no `.agi/`, 0 refs, clean. On the real repo, first try.
- **`bin/locations.py`** — the single path resolver. **`bin/crons.py`** —
  cadence read from `.agi/nodes/.geometry/crons.md`, `crons_live` kill switch,
  self-reapplying every 5 minutes. G10.2's first geometry node read by real
  code.
- Four goals recorded for the parentage spine: **G12**, G12.1, G12.2 (moral →
  vision → goal, only morals parentless) and **G9.6** (build-node
  `description:`, body as rendered payload).

## 3. 🔴 Next tasks — iterations 5 and 6, batched

### 3a. Finish G11.1. This is the top item and it is a defect, not tidiness.

**Nine `bin/` entry points still declare their own ancestor walk.** Three broke
within an hour of the migration; see `goal:g11.1` for the table. Fix the rest
by delegating to `locations.project_root_from_env()`.

**Do `snapshot-build-site.py` first** — not because it is worst, but because it
**deletes every `origin: build-site` node it does not re-derive on that run**.
A wrong resolver there is the H0i pruning hazard with the safety catch off. It
has not fired only because nothing has run it from a cwd where the old rule
resolves differently.

Falsifier: `grep -c '^CONFIG_NAMES' extensions/agi/bin/*.py` returns 1.

### 3b. `git ls-tree --full-tree` — the owner asked whether it is a workaround. It is.

`--full-tree` is the *correct flag* for what that call does, so it is not
wrong. But it treats a symptom. **The real defect is that `grid.py` runs git
commands with the GRAPH root as cwd, when grid refs live in the GIT repo.**
Those were the same directory before G11 and are not now.

Proper fix: `grid.py` should take `repo_root` (which `locations.repo_root()`
already returns) for every git invocation, and `graph_root` only for finding
node files. Two roots, two jobs — the same split `locations.py` already makes
and `grid.py` has not adopted. Then `--full-tree` becomes belt-and-braces
rather than the thing holding it up.

Worth doing because the failure mode was **a silent wrong answer**: every one
of 809 nodes read as `CHANGED` while byte-identical. `ref_tip` worked
throughout, which is exactly what made it look fine.

### 3c. Config influence, and folding crons into the graph properly

Manual path editing in cron lines is clunky and the owner is right. Current
state: cadence is graph-declared, but the *commands* are built in `crons.py`
and the paths resolved at apply time.

The owner asked: **can the crons themselves be symlinked into the graph, the
way the skill and hook are?** Short answer, and it needs verifying next
session rather than trusting this note: **not for crontab.** `cron` reads
`/var/spool/cron/crontabs/<user>`, which is root-owned, mode-checked, and
installed only via `crontab -`; a symlink there is refused or ignored by most
`cron` implementations. **`systemd --user` timers CAN be symlinked** from a
repo into `~/.config/systemd/user/`, which would make the schedule literally a
tracked file. That is the shape worth costing.

Interim improvement available without any of that: reduce to **one** bootstrap
cron line that runs `crons.py apply`, and let everything else be graph state —
the `*/5` job already re-applies, so the second line is nearly redundant
already.

Also expand what `.agi/config.json` governs. `locations.source_root` and
`goals_file` exist; log paths, remote names and the branch to push are still
computed or hardcoded.

### 3d. Strip the `order:` field — the owner's call, and the analysis agrees

91 goals carry `order: 0..90`, dense. It is read in exactly one place that
matters: `snapshot-goals.py` sorts the render by it. Every insertion renumbers
every later goal — inserting G9.6 and G12/.1/.2 churned 21 nodes for no
semantic change, twice in one session.

**A queue of 91 is not a priority list.** Sort the render by `goal_id` instead
(natural sort: G1, G1.1, … G12.2, then S1…S21). Derivable from the id, needs
no stored field, never renumbers on insert.

One real consequence to accept: the S-goals are currently in *historical*
order (S11 renders before S1), and `goal_id` sort would reshuffle them once.
That is a one-time document change, and arguably a correction.

Priority/queue then lives in this handoff's §3, which is what the owner wants
and what a human actually reads.

### 3e. CLAUDE.md / AGENTS.md prose nodes — half done automatically

`build:CLAUDE.md`, `build:AGENTS.md` and `build:GOALS.md` now exist: they were
minted the moment the boundary and resolver were fixed, because for the first
time those files are tracked in the repo being scanned. The old layout could
not express them at all.

Remaining: they carry `parse_ok: false` and an empty contract like every
non-Python payload. Giving them real prose contracts is **G6.6**, and spawning
them from `verdict:g11-migration-rehearsal` (or a new verdict on the docs
themselves) is the chain work the owner asked for.

### 3f. Carried from the original iteration 5

- **Worktree-per-kid isolation (G4.1).** Now actually possible: one repo means
  a `git worktree` isolates source, graph and tests together. It never did
  before.
- **`init` (G1.5)** — one command from empty directory to running project.
- **G8.2 falsifier** — a third project, neither `agi` nor `fantasia`, reaching
  a rendered map with no engine change.
- **Sweep `status: active`.** 43 active goals against
  `cc_dispatch.max_goals_active: 3`. The metric warns every run. Move all but
  ~3 to `horizon`; that is what `horizon` is for.

## 4. 🔴 Traps from this session — do not re-learn these

- **`git ls-tree` is scoped by cwd within the work tree.** From `<repo>/.agi`
  it looks for entries under an `.agi/` prefix. Grid trees have `node.md` at
  their own root. Silent wrong answer, not an error.
- **A generator whose output lands inside its own input set does not
  converge.** `level3.py` scanned the graph, wrote to the wrong directory, and
  minted nodes for its own output —
  `nodes-build-nodes-build-nodes-build-….md.md.md`, 3,098 files committed
  before anyone noticed. Fixed by `payload_boundary.is_the_graph_itself` and
  the resolver, but the *class* is what to remember.
- **`git clone` does not copy ignored files.** The real migration failed on an
  ignored `CLAUDE.md` at the engine root that no cloned rehearsal could ever
  have. Four rehearsals could not find it.
- **Ignored files do not appear in `git status --porcelain`.** A "clean"
  cleanliness check is not the same as an empty directory.
- **Existence is not currency.** The publish gate checked whether a
  `payload_ref` existed, not whether it matched, and passed on live data with
  two stale files. Testing a gate against real data rather than fixtures is
  what found it.
- **Three wrong numbers were asserted confidently this session** —
  "thirteen" resolver sites (eleven), "375 payload_refs to rewrite" (zero),
  "166 build-site nodes" (159). All in documents arguing for rigor. **Record
  the command that produced a number next to the number.**

## 5. How to write into this file — SUPERSEDED

The `payloads/` dance in §6 above is retired. It is now:

```bash
$EDITOR HANDOFF.md
python3 extensions/agi/bin/level3.py
python3 extensions/agi/bin/grid.py commit --all
git add -A && git commit
```

## 6. Known-good verification sequence

```bash
cd /home/ubuntu/work/agi
bash extensions/agi/driver.sh --smoke --max-iters 1     # node count must not drop
python3 -m pytest extensions/agi/tests/ -q              # 1029 passed
python3 extensions/agi/bin/snapshot-goals.py --render --check
python3 extensions/agi/bin/locations.py . --json        # layout must be graph_dir
python3 extensions/agi/bin/crons.py show                # must say: up to date
python3 extensions/agi/bin/grid.py status | grep -c CHANGED   # small, not 809
```

If the last one prints a number near the node count, §4's `ls-tree` trap has
come back.

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

**Do not "improve" `thought_coverage`.** Still the design at 12/792: absent
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
