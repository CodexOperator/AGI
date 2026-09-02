# SESSION HANDOFF — 2026-09-02b: LIVE SCRATCHPAD (session in progress)

Standing bootstrap lives in [QUICKSTART.md](QUICKSTART.md). This file is one
session only and the next director replaces it wholesale.

## §0 State block

| | baseline (session start) | now |
|---|---|---|
| active nodes | 893 | **903** |
| deprecated | 7 | 7 |
| `outcome_coverage` (primary) | 0.266 | 0.260 |
| `evidence_fraction` | 0.250 | **0.286** |
| `decisive_evidence_fraction` | 0.955 | **0.964** |
| unevidenced decisive | 1 | 1 |
| goals active / horizon / complete | 12 / 62 / 34 | **13** / 62 / 34 |
| tests | 1250 | **1295** |
| goals | 110 | **111** |
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

Ten iterations, ordered so each one's prerequisite is the one before it.
iter-107 came first because the concurrency numbers the owner asked for were
not safe without it. `goal:g1.11` was minted mid-session at the owner's
direction and displaced `write.py` from the front of the queue.

- [x] **Phase 0** — G13's three answers into the graph; pushed.
- [x] **iter-107** — `goal:g4.8` item 3: a concurrency bound that survives a
      tier. Built, measured, pushed. **Cap now 25 tree-wide** (owner's call).
- [x] **iter-108** — `goal:g1.11`, per-spawn credentials. Built, measured
      against the live API, verified end to end. Key is IN and working.
- [x] **iter-109** — `write.py` + `node_writer.update_node`, `goal:g13`'s
      write half. Plus **iter-109b**, a self-correction (see §4).
- [ ] **iter-110 (next)** — `goal:s31`, first defect fixed *through* the new
      write path.
- [ ] **iter-111** — `goal:g1.10`, `.geometry/commands.md`.
- [ ] **iter-112–113** — `goal:g13.1`, edit mode.
- [ ] **iter-114** — `goal:g4.7`, wire `restart()`.
- [ ] **iter-115** — `goal:g3`/`g5`, close chains to mvp.
- [ ] **iter-116** — reserve.

### The concurrency number, settled

Built at 5, then raised: **`spawn.max_live: 25` tree-wide**, `spawn.parallel:
5`. The owner's intended shape is **5 parents + 10 kids**, with 25 as the
ceiling nothing may cross. 5 was rejected once the arithmetic was concrete —
5 parents at cap 5 leaves zero budget for kids, so five parents would have run
and produced nothing.

**The cap is policy, not a finding.** What is measured is that whatever number
is declared is the number that holds. 25 concurrent pi agents is well past the
~4 where rate-limit deaths were measured last session, which is the reason
`goal:g1.11` moved to the front of the queue.

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

Config now: `spawn.parallel: 5`, `spawn.max_live: 25`.

Inspect the live population any time:

```bash
python3 extensions/agi/bin/spawn_budget.py status
```

### ✅ iter-108 — `goal:g1.11`, one minted key per spawn

Every agent inherited one long-lived `OPENROUTER_API_KEY` and that key was the
whole balance. Now a spawn gets a key that did not exist before it and does not
outlive it, with **three independent limits because a cleanup step is not a
safety property**: a credit cap ($0.25), a TTL (60 min), and revocation when
the lease is reclaimed. A director killed mid-loop leaks keys that expire on
their own.

The credential hangs on `spawn_budget`'s lease — already per-agent, already
reclaimed by liveness — so **reclaiming the slot and revoking the key are one
event**. Only the hash is stored; the secret goes to the child env and nowhere
else.

**Measured against the live API:** mint 0.760s mean / 0.859s max (10 serial);
**10 concurrent mints in 0.919s wall**; 20 concurrent revokes in 2.781s; 30/30
ok, 0 leaked. That settled the banked granularity question — **per spawn**,
because batching is a cost optimisation and the cost is 0.06% of the 20-minute
timeout it gates, and per-slot cannot answer "which agent" since a slot
outlives the agents in it.

**Live end-to-end** (stub harness, `--tier parent` so nothing entered the
graph): key minted as `agi-iter908-parent-a00-245fe1f5`, injected as
`OPENROUTER_API_KEY`, **provisioning key absent from the child's environment
read out of the process itself**, hash on the lease, auto-revoked when the
agent died, no `sk-or-` string anywhere on disk.

```bash
python3 extensions/agi/bin/provisioning.py status
python3 extensions/agi/bin/provisioning.py reap        # dry run; --yes to act
```

### ✅ iter-109 — `goal:g13`'s write half

`goal:g13` names five operations. **Edit-in-place had no routine**, so every
fix and retag in this project's history was a hand edit — `goal:g13.1`'s
"completely stray and untraceable commit". `node_writer.update_node` is that
routine, and it **cannot destroy the authored `THOUGHT` region** —
`goal:g2.10` made impossible rather than discouraged. Tested by replacing
bodies outright.

`bin/write.py` is the link layer: `link_ref` generalises `payload_ref`, `self`
means the body is its own data, a single read of a missing link **raises**, a
bulk scan returns a **typed sentinel** and counts it in `broken_links`.

```
links: 905 resolved, 0 broken
  declared 0 · payload_ref 220 · defaulted 685
```

🔵 **`declared: 0` — the corpus is NOT migrated.** The resolver distinguishes a
declared `self` from a defaulted one exactly so that stays checkable. A node
body is still a payload, not a marker; this built the mechanism a marker would
need.

## §3 🔴 Where it stopped, and the exact next command

Phase 0 and iterations 107, 108, 109, 109b are committed, grid-versioned,
pushed, green at 1295 tests.

**Next is iter-110: `goal:s31`** — a scaffolded node ships schema-invalid.
`[hypothesis].md` requires `title` + `testable_claim`; `node_writer` seeds
neither; the kid is *correctly* forbidden from touching frontmatter. **The node
cannot become valid by anyone doing their job as briefed.** It is now fixable
*through* `update_node` rather than by hand, which makes it the write half's
first real consumer.

The constraint that makes the fix safe is already measured: **`scaffold_hash`
hashes the BODY, not the frontmatter**, so seeding schema-required fields
cannot break completion detection.

```bash
cd /home/ubuntu/work/agi
python3 -m pytest extensions/agi/tests/ -q          # 1295 green
python3 extensions/agi/bin/write.py links           # 905 resolved, 0 broken
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
3. 🔴 **A `grep` proved the wrong thing, and I published the wrong claim
   before checking it.** The iter-109 experiment node said *"there is no
   `type == goal` branch in `write.py` — `grep` confirms the string does not
   appear"*. Running it returns **1**: the phrase is in the module docstring,
   stating the invariant it was meant to verify. **The invariant held; the
   evidence did not.** Same class as trap 1 — the tool answered a different
   question and the answer looked like the one wanted. Replaced with an `ast`
   test that excludes string constants. Corrected in iter-109b rather than
   quietly repaired, because a wrong evidence line silently fixed is the exact
   shape the evidence gate exists to prevent.
4. **A test asserting a brief's wording is a test of the design, and it broke
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

**New this session, and the first thing to settle when the owner returns:**

0. **`goal:g1.11`'s batching granularity.** One minted key per spawn, per
   `ceil(max_live / 3)` batch, or one per slot minted at loop start? All three
   were named by the owner and none chosen. **Leading candidate: per slot** —
   `spawn_budget` already owns a bounded set of slots, so a lease and a key
   become the same object at two layers and there is one admission path
   granting both. Not decided here, because mint latency and failure rate
   against the real API are unmeasured and a guess baked into a goal is the
   `goal:s17` shape. Recorded in the goal node too.

**Two carried forward from last session, both still the owner's:**

1. **Should the viewport replace `INJECTION.md`'s renderer outright?**
   `goal:g9.7`'s falsifier is proven *within* `viewport.py`. Making
   `render-context.py` and `zoom.py` call `frame_stream` too would delete 4 of
   the 5 remaining render paths — the real prize — but it changes what every
   kid is handed. Parked as an iter-115 candidate, not scheduled.
2. **`goals_active` is 13 against a cap of 9, deliberately** — `g1.11` makes
   thirteen. The open question
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
