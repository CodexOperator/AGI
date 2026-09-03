# SESSION HANDOFF — 2026-09-03: loop L1 STOPPED AFTER 07 (of 10)

Standing bootstrap lives in [QUICKSTART.md](QUICKSTART.md). This file is one
session only and the next director replaces it wholesale.

**Loop-scoped numbering.** This session is **loop L1**; iterations `L1.01`…`L1.07`
ran. The global `iter-NNN` series ended at 116. Making the split real in
`sessions/` and in commit subjects was L1.10's job and **did not happen** —
commit subjects carry it by hand for now.

## §0 State block

| | start (post-116) | now |
|---|---|---|
| active nodes | 922 | **940** |
| deprecated | 7 | **8** |
| `outcome_coverage` (primary) | 0.300 | **0.271** ⬇ |
| `evidence_fraction` | 0.328 | 0.317 |
| `mvp_count` | 39 | 39 |
| `broken_links` | 0 | **0** |
| schema-invalid nodes | 118 | **62** |
| goals active / cap | 13 / 9 ⚠ | **13 / 15** ✅ |
| tests | 1335 | **1371** |
| unpushed | 0 | **0** |

**The primary fell 0.300 → 0.271 and that is honest.** 18 nodes were added,
mostly hypotheses and experiments, and **no chain closed** — `mvp_count` is
unchanged at 39. Hypotheses lead, mvps lag. **Do not "fix" it** by minting
mvps for work already done; `[mvp].md` is explicit that an mvp points forward,
and the corpus proved it (`source_files` 0/26).

**OpenRouter:** `$20.00` total, **`$15.43` remaining**. This loop spent
**$0.14** for 12 live kids. Per-key cap `$5.00`, so the balance is three keys
deep, not twenty. Nothing knows about the account balance — not `spawn_budget`,
not the reaper.

🔵 **`spawn.parallel` is `8`.** Ramp this loop: 5 → 2 → 1 (attribution) → 8.

### 🔴 Crons are still OFF — push by hand

```bash
git -C /home/ubuntu/work/agi push origin master
```

## §1 The plan, and where it stopped

- [x] **L1.01** — config ($5/key, goals cap 15), `edit`→`write`, `write`→`links`,
      keys mint into the `agi` workspace.
- [x] **L1.02** — first live agents on minted keys. **Part A disproved, then fixed.**
- [x] **L1.03** — the bound at 8 + `goal:g1.11` Part B. Cap 25 still untouched.
- [x] **L1.04** — the briefing extracted; `INJECTION.md` byte-identical.
- [x] **L1.05** — `render-context.py` retired. **One render path, not four.**
- [x] **L1.06** — `agi <verb>` router; `view` / `view-llm` / `view-both` / `write`.
- [x] **L1.07** — `write create`; schema backfill 118 → 62; **a serializer bug
      of mine that reached a push**.
- [ ] **L1.08** — 🔴 **the removal guard. NEXT, and it gates L1.09.**
- [ ] **L1.09** — the wide run: cavekit exit + legacy sweep. See §6.
- [ ] **L1.10** — webhook / session-id → chat-to-node linking (`goal:g10.1`,
      `goal:g2.7`); engine-commit pinning; loop-scoped iteration numbering.

## §2 What landed

**L1.01 — the workspace is a safety change, not tidiness.** Keys mint into
workspace `72750376-…` (`agi`); the owner's own long-lived key named `agi`
sits in `default`. `reap_orphans` matched the prefix `agi-`, so **one character
separated the reaper from the key the project runs on**. It now requires the
workspace too — two filters that fail differently. `active` is a **focus
budget**, not an in-flight census (owner's ruling); `metrics.py` said the
opposite and now says so correctly.

**L1.02 — per-spawn keys were decorative, end to end.** pi does not read
`OPENROUTER_API_KEY`; its `auth.json` shells out to `env-get.sh`, which read
`.env` unconditionally. Minted keys sat at `usage=0` while spend landed on the
shared key. `env-get.sh` had **zero tests**. *A stub that reads
`$OPENROUTER_API_KEY` proves the injection happened; it cannot prove the
harness reads what was injected.* Fixed — attribution is now proved by a bill.

**L1.03 — the bound holds at 8.** Peak leases 8, peak pi procs 8, over 113
samples. All 8 nodes written, none lost (`goal:s28`'s hazard did not fire).
`goal:g1.11`'s falsifier is now complete in both halves.

**L1.04 — the briefing was the whole viewport gap.** Nine sections, now in
`bin/briefing.py`. `INJECTION.md` came out **byte-identical**, which is what
proved it a move rather than a rewrite.

**L1.05 — `render-context.py` retired**, node deprecated and moved, payload
deleted (recoverable v5–v13, *not* v1). Two invariants came off silently with
it; both restored — see §4.

**L1.06 — `agi <verb>` works and the router has no verb list.** Any bare first
word is delegated to `commands.py`, so adding `agi <anything>` is a node edit.

**L1.07 — `write create`** mints a node and the file behind it, through the
spawn gate. **Schema backfill 118 → 62**; the remaining 62 (`testable_claim`×51,
`scale`×7, `next_edges`×3, `confidence`×1) are exactly the set that needs
`goal:g1.9`. Nothing was invented.

## §3 🔴 Where it stopped, and the exact next command

Everything is committed, grid-versioned and pushed. Working tree clean.

**L1.08 is the removal guard, and it is a gate, not a nicety.** Deprecating
the 168 `origin: build-site` nodes removes **52 unclosed hypothesis chains**
from `outcome_coverage`'s denominator, which raises the primary for free.
`goal:g3` says *added motion* cannot move scoring; nothing yet says the same
about *removal*. The owner approved **guard first, then retire**.

```bash
cd /home/ubuntu/work/agi
python3 extensions/agi/bin/commands.py run smoke     # 940 active, must NOT drop
python3 extensions/agi/bin/commands.py run tests     # 1371
python3 extensions/agi/bin/provisioning.py status    # expect 0 outstanding
python3 extensions/agi/bin/spawn_budget.py status    # expect 0/25 live
```

## §4 Traps hit this session

1. 🔴 **Four times, a check ran, passed, and was not measuring the thing that
   broke.** The command-subcommand guard (three attempts: `--help` exits 0
   regardless; then `ast` but skipping the one case it existed for);
   `viewport._verify` matching "any line with a backtick" once the briefing
   filled the output with backticks; and the two below. **The only defence
   that worked: reintroduce the defect and watch it go red.** Do that every
   time; a guard that has never failed on purpose is not a guard.
2. 🔴 **I pushed a commit that broke `agi <verb>`.** One `write.py` edit on
   `command:commands` wrote its nested `commands:` mapping back as a Python
   dict repr in a string, because `render_frontmatter` fell through to
   `str(v)` for any type it did not name. Latent for months — no node had a
   nested mapping until `[command]` existed. **It escaped because I ran the
   suite, then made the edit, then committed in one shell command.** Running
   tests before your last edit is indistinguishable from not running them.
3. 🔴 **A rewrite carries visible behaviour across and drops invariants
   implemented elsewhere.** Retiring `render-context.py` took `_LiveOnly`
   with it, so the injected map started showing deprecated nodes
   (`goal:s23`). `grep -c` on the map said `0` — **luck**, the node sat
   outside depth 3. Anchoring the viewport at its parent showed it at once.
4. 🔴 **`broken_links` had never met a retired payload.** Deprecating a build
   node and deleting its file — the documented end state — drove the metric
   permanently to 1, and `[build]` *requires* `payload_ref` so the gate
   correctly refuses to remove it. Damage now means a broken link on a **live**
   node; retired payloads are counted and printed, never silently excluded.
5. **`briefing.py` was written against one graph representation and used with
   another.** `load_directory` answers `edges_from`; `zoom._load_wired_graph`
   builds no edges and hangs `children` on nodes. Result: `edges: 0` on a graph
   with 869, and **every idea reporting 0 descendants** — the attractor list
   came out all zeros in alphabetical order and looked plausible.
6. **`pgrep -af "cli.js"` does not find pi.** The process is named `pi`. I
   concluded "both kids exited" while one had four minutes left.
7. **Piping a long background command through `tail` hides it until it ends.**
   Redirect to a file instead.

## §5 Known-good verification sequence

```bash
python3 extensions/agi/bin/commands.py run smoke     # 940 active, must NOT drop
python3 extensions/agi/bin/commands.py run tests     # 1371 passing
python3 extensions/agi/bin/commands.py run goals-check
python3 extensions/agi/bin/commands.py run viewport-verify
python3 extensions/agi/bin/commands.py run links     # 943 resolved, 0 broken
python3 extensions/agi/bin/commands.py run grid-commit
```

`agi <verb>` also works now: `agi smoke`, `agi links`, `agi view`,
`agi view-llm`, `agi write <id> "<script>"`, `agi write create <type> <slug>`.

## §6 🔵 Owner direction for L1.09 — recorded 2026-09-03, not yet acted on

### Concurrency goes ACROSS targets, not at one

L1.03 measured the failure: at cap 8 aimed with one `--target`, **six of eight
kids wrote substantially the same hypothesis**. The owner's intent was never
one target — it is **several chains built simultaneously**, whole sections of
graph at a time: parallel `experiment → mvp → build` chains.

**That is why `goal:g4.1` (worktree-per-kid) matters** and is the real
prerequisite: without isolation, concurrent agents touching the same node or
the same file break each other's work.

**When same-target concurrency IS right:** when a goal is genuinely open-ended
and the point is to explore different options. **The owner's read of this
tree: the vast majority of goals do not need that.** They are clear-cut
feature goals where the direction is already obvious and the chain just needs
standard validation — straight through to a node edit, or verdict → mvp → new
node. A handful may benefit from exploratory fan-out; most will not.

### The build sites: mine them before retiring them

**The corpus, measured:**

| type | n | note |
|---|---|---|
| task | 91 | |
| hypothesis | 61 | **52 never reach a verdict** — only 9 do |
| idea | 8 | the `Domain: …` roots — **these are the top attractors** |
| goal | 5 | already real goals, see below |
| build / experiment / mvp | 1 each | |

The 5 build-site **goals** already exist as goals:

```
S18  horizon   Absorb cavekit references before cavekit retires   <- the owner's ask, already a goal
S21  horizon   The graph can add a file but can never remove one
G7.8 horizon   A generator mints parent ids it never checks exist
S6   complete  Strip agi-tree to the graph and its inputs
G11.1 complete Nine Python files still declare their own ancestor walk
```

**The owner's instructions, in order:**

1. **Go through the build sites and see which carry descriptions that belong
   in a goal.** Move those into goals rather than losing them.
2. **Before deprecating anything that describes a stale shape, confirm an
   equivalent goal already exists and is being built.** `goal:s18` is that
   goal for the cavekit half and is currently `horizon`.
3. **Then walk the hypothesis chains those sites spawned and spend iterations
   closing them** — *unless another part of the graph already contains every
   piece that chain was trying to establish*, in which case say so and close
   it that way. **52 open chains** is the number.

### Deprecate vs retire — the mechanics, since the owner asked

The owner had these possibly reversed. Correct, from `CLAUDE.md`:

- **`retired` is a GOAL status** (`active | horizon | retired | complete`). A
  retired goal's *closed* chains leave the score but stay in the graph and
  stay attributable. Retiring cannot inflate `outcome_coverage`, because only
  a closed chain can leave the denominator (`goal:g5`).
- **`deprecated` is a NODE status**, and the node **moves to
  `.agi/nodes/deprecated/<type>/`**. Never `git rm` — a node's grid ref
  outlives its file, so deleting decouples the ref instead of shrinking it.
- **The owner's actual want is satisfied by deprecation.** As of L1.05 the
  injected map **hides deprecated nodes and their subtrees**
  (`frame_stream(hide_deprecated=True)`), so an agent cannot pick one as a live
  chain head. The human viewport still shows them on purpose, as damage.

### 🔴 The ordering constraint that is load-bearing

`snapshot-build-site.py` **deletes every `origin: build-site` node it does not
re-derive on that run.** So the kits are removed *after* their nodes are
deprecated, **never before** (H0i). And a `payload_ref` is dropped before its
file is deleted, or `broken_links` leaves 0.

**Deprecating the 8 `Domain: …` ideas would gut the attractor list** —
`idea:domain-graph-core` alone has 68 descendants and heads the list every
agent is handed. Decide what replaces it before removing it.

## §7 Standing hazards

- **Cap 25 has never run.** The bound is proved at 8. `goal:g4.8` clause 2 (a
  parent demoting an unevidenced verdict unaided) and clause 3 (delegator
  spend sub-linear) are **never observed** — clause 2 is what distinguishes a
  parent tier from a spawn fan-out.
- **No parent-spawns-kid run has ever happened live.** `brief.py` gives a
  parent the spawn primitive and `spawn_budget` bounds grandchildren; neither
  has met a real parent.
- **$15.43 is the real ceiling**, not the $5 per-key cap. Nothing in the
  engine knows the account balance.
- **A parent's REPORT is not its artefact.** Check the node file.
- **A fix with no test is an assertion — and a test that has never failed on
  purpose is closer to an assertion than it looks.** See §4.1.
