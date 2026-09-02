# SESSION HANDOFF — 2026-09-02b: LIVE SCRATCHPAD (session in progress)

Standing bootstrap lives in [QUICKSTART.md](QUICKSTART.md). This file is one
session only and the next director replaces it wholesale.

## §0 State block

| | baseline (session start) | now |
|---|---|---|
| active nodes | 893 | **896** |
| deprecated | 7 | 7 |
| `outcome_coverage` (primary) | 0.266 | 0.264 |
| `evidence_fraction` | 0.250 | **0.262** |
| `decisive_evidence_fraction` | 0.955 | **0.958** |
| unevidenced decisive | 1 | 1 |
| goals active / horizon / complete | 12 / 62 / 34 | 12 / 62 / 34 |
| tests | 1250 | **1265** |
| goals | 110 | 110 |
| unpushed | 0 | 0 |

`outcome_coverage` dipping 0.266 → 0.264 is the expected shape, not a
regression: iter-107 minted a hypothesis without minting an mvp, so the
denominator grew. `evidence_fraction` — the metric that only moves when
experiments actually run — went up.

**Runtime:** pi — `deepseek/deepseek-v4-flash` kids under `qwen/qwen3.8-27b`
parents. **Budget this session: iterations 107–116 (ten).** Director is the
Claude session; it acts as parent itself for engine-primitive work and
dispatches pi parents for graph work.

### 🔴 Crons are still OFF on purpose — push by hand

`.geometry/crons.md` has `crons_live: false`, left off by the owner since the
`goal:g11` migration freeze. **Nothing pushes `agi` automatically.**

```bash
git -C /home/ubuntu/work/agi push origin master
```

## §1 The plan, and where it got to

Ten iterations, ordered so each one's prerequisite is the one before it. The
concurrency numbers the owner asked for (`spawn.parallel = 5`, 5 parents per
iteration) are **not** safe until iter-107 lands, which is why it is first.

- [x] **Phase 0** — G13's three answers into the graph; pushed.
- [x] **iter-107** — `goal:g4.8` item 3: a concurrency bound that survives a
      tier. **Cap 5 live agents, tree-wide.** Built, measured, pushed.
- [ ] **iter-108 (next)** — `write.py`, `goal:g13`'s write half.
- [ ] **iter-109** — `goal:s31`, first defect fixed *through* the new write path.
- [ ] **iter-110** — `goal:g1.10`, `.geometry/commands.md`.
- [ ] **iter-111–112** — `goal:g13.1`, edit mode.
- [ ] **iter-113** — `goal:g4.7`, wire `restart()`.
- [ ] **iter-114** — `goal:g3`/`g5`, close chains to mvp.
- [ ] **iter-115–116** — reserve.

### 🔵 The concurrency number, stated so it can be corrected

The owner said "bound it to 5 just to be safe". Read as **5 live agents across
all tiers, tree-wide** — so 5 parents fill the budget and their kids queue
behind them. The other reading is 5 kids *per parent* (25 live). The safe one
was taken because last session measured parent deaths from rate limits above
roughly 4 concurrent pi agents.

## §2 What landed

### ✅ Phase 0 — `goal:g13`'s three open questions are answered in the node

The owner settled all three. They are now goal text the chain falsifies
against, not questions `write.py` has to stop and ask:

1. **`THOUGHT` stays in the node body.** Marker and authored region coexist in
   one file. Nothing migrates; `goal:g2.11` untouched; the grid keeps
   versioning thought for free. Rejected: a third grid tree entry (thought
   stops being visible in the working tree), and the head of the linked file
   (an authored region inside a file generators rewrite — `goal:g2.10`'s
   measured failure).
2. **A goal node links to itself — `link_ref: self`.** `goal:g6.9` stands;
   `GOALS.md` keeps rendering *from* goal bodies. An exception **with a name**,
   so a reader resolves `self` like any other link rather than branching on
   `type == goal`.
3. **Missing link: raise on single read, typed sentinel + `broken_links`
   metric on bulk scan.** The founding finding applied to itself — the defect
   was never divergent parsing but divergent *failure semantics*, so the answer
   is two **chosen** behaviours, not one behaviour everywhere.

The **scope gate in `goal:g13` is now open**, recorded in the node: the tiers
it was waiting on stand (manifest race fixed and verified at 8 concurrent
agents, two concurrent parents clean, read half landed).

### ✅ iter-107 — the bound is structural now (`goal:g4.8` item 3)

`spawn.parallel` bounds one invocation's slots and **never bounded
grandchildren**: a parent gets its kids by running `dispatch.py` again, and
that second invocation reads its own copy of the same number. A parent
carefully *enforcing* the number does not close it either —
`experiment:a00-5f927203-8a66a2` disproved that. **A limit expressed as a
number cannot be global.**

`bin/spawn_budget.py` puts it in shared state: one lease per live agent, taken
under a lock at the spawn site immediately before `Popen`, **reclaimed by
liveness rather than by any release path** — so a `kill -9` frees its slot and
the rail cannot degrade into an outage. There is no separate grandchild code
path to bound; **the same admission path entered twice is the whole mechanism.**

| cap | admissions | peak live |
|---|---|---|
| 1 | 2 | **1** |
| 3 | 5 | **3** |
| 5 | 10 | **5** |
| 999 (control = pre-fix) | 25 | **24** |

Peak **equals** cap in every bounded run, so the runs sat on the boundary
rather than passing because nothing was admitted. The control is what makes
the other three a comparison instead of an observation.

**Admission is non-blocking on purpose.** Waiting deadlocks this exact
topology — parents holding every lease, each blocked on a kid that cannot be
admitted until a parent finishes. A refused slot is skipped and recorded in
`manifest.unadmitted`, kept out of `agents` so nothing polls a corpse that was
never born.

Chain: `hypothesis:shared-lease-bounds-the-tree` →
`experiment:lease-bound-under-five-spawners` →
`verdict:the-bound-is-structural-now` (**proved @0.97**, evidence resolving to
a real node). **The verdict says plainly it closes falsifier clause 2 only** —
no pi agent was spawned, fairness is unmeasured, and the cap of 5 is *policy,
not a finding*.

Config now: `spawn.parallel: 5`, `spawn.max_live: 5`.

Inspect the live population any time:

```bash
python3 extensions/agi/bin/spawn_budget.py status
```

## §3 🔴 Where it stopped, and the exact next command

Phase 0 and iter-107 are committed, grid-versioned, pushed, green at 1265
tests. **Next is iter-108: `write.py`, `goal:g13`'s write half** — the thing
`goal:s31`, `goal:g1.10` and `goal:g13.1` all wait on. Its three design inputs
are now settled in the goal node (see §2).

`node_writer.write_node` is the starting point. The constraint that makes
`goal:s31`'s fix safe is already measured: **`scaffold_hash` hashes the BODY,
not the frontmatter**, so seeding schema-required fields cannot break
completion detection.

```bash
cd /home/ubuntu/work/agi
python3 extensions/agi/bin/dispatch.py "$PWD" 108 --tier parent --target goal:g13 --level small
```

## §4 Traps hit this session

1. **A background `pytest` reported exit 0 with an empty output file, and the
   suite was actually red.** One test failed. Trap 2 from last session in a new
   costume: *the exit code and the output disagreed, and believing either alone
   was wrong.* Re-run in the foreground before trusting a green.
2. **Backticks in a `git commit -m` message are command substitution.**
   ` `agents` ` in the iter-107 message ran as a command and left a hole in the
   commit body (`kept out of  so nothing that polls...`). Not amended — force-
   pushing `master` to fix one word is worse than the word. **Use `-F -` with a
   heredoc for any message containing backticks.**
3. **A test asserting a brief's wording is a test of the design, and it broke
   correctly.** `test_parent_brief_carries_the_grandchild_bound` asserted the
   string `"does not bound"`. Its own docstring said the brief was *not
   sufficient* and that `goal:g4.8` owned enforcing it at the spawn site — so
   once it was enforced, the right move was to strengthen the assertion (the
   brief must now name both bounds, say which is enforced, and name
   `unadmitted`), not to restore the old sentence.

## §5 Known-good verification sequence

```bash
bash extensions/agi/driver.sh --smoke --max-iters 1     # node count must NOT drop from 896
python3 -m pytest extensions/agi/tests/ -q              # 1265 passing
python3 extensions/agi/bin/viewport.py --verify         # goal:g9.7's invariant
python3 extensions/agi/bin/snapshot-goals.py --render --check
python3 extensions/agi/bin/grid.py commit --all
```

## §6 🔵 BANKED — decisions deliberately not made

Two carried forward from last session, both still the owner's:

1. **Should the viewport replace `INJECTION.md`'s renderer outright?**
   `goal:g9.7`'s falsifier is proven *within* `viewport.py`. Making
   `render-context.py` and `zoom.py` call `frame_stream` too would delete 4 of
   the 5 remaining render paths — the real prize — but it changes what every
   kid is handed. Parked as an iter-115 candidate, not scheduled.
2. **`goals_active` is 12 against a cap of 9, deliberately.** The open question
   is *how* it should count: `g3`, `g5` and `g7` are overarching and arguably
   permanent residents rather than in-flight work. Retune the cap or exempt
   them; the warning is expected noise until then.

## §7 Standing hazards this session must respect

- **The bound is real but the live run is not observed.** `spawn.max_live: 5`
  holds against sleeping interpreters. No pi agent has been spawned under it.
  Watch `spawn_budget.py status` and `manifest.unadmitted` on the first real
  dispatch, and note that a `SIGSTOP`ped agent is alive to `os.kill(pid, 0)`
  and holds its slot indefinitely — correct, and still a surprise at cap 5.
- **A parent's REPORT is not its artefact.** Check the node file, not the
  summary — last session a `proved` @0.99 sat unevidenced because a parent
  reported a field it never wrote.
- **A fix with no test is an assertion.** `b8cb2ec05` claimed atomicity in a
  commit message and was wrong.
- **Check exit codes, not just output.** A traceback and empty output look
  identical to `grep`.
