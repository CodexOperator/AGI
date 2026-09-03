# SESSION HANDOFF — 2026-09-03: LIVE SCRATCHPAD (loop L1, in progress — 02 done)

Standing bootstrap lives in [QUICKSTART.md](QUICKSTART.md). This file is one
session only and the next director replaces it wholesale.

**Loop-scoped numbering starts here.** This session is **loop L1**; its
iterations are `L1.01`…`L1.10`. The global `iter-NNN` series ended at 116.
Making that split real in `sessions/` and in commit subjects is L1.10's job —
until then the commit subject carries it by hand.

## §0 State block

| | baseline (post-116) | now |
|---|---|---|
| active nodes | 922 | **936** |
| deprecated | 7 | 7 |
| `outcome_coverage` (primary) | 0.300 | 0.275 ⬇ |
| `broken_links` | 0 | **0** |
| goals active / cap | 13 / 9 ⚠ | **13 / 15** ✅ |
| tests | 1335 | **1346** |
| unpushed | 0 | **0** |

**The primary is falling, and it is honest.** 14 hypotheses minted, no chain
closed. Same dynamic as iterations 107–111 last session: hypotheses lead, mvps
lag, coverage recovers when the chains close. **Do not "fix" it** by minting
mvps for work already done — that was tried and `[mvp].md` forbids it.

**OpenRouter, measured live:** `$20.00` total, **`$15.43` remaining**.
L1.02 + L1.03 cost **$0.14** for 12 kids. Per-key cap `$5.00`, so the balance
is three keys deep, not twenty. The owner's ruling stands: if it runs out,
stop the experiment where it got to and call it data.

🔵 **`spawn.parallel` is `8`.** Ramp so far: 5 → 2 → 1 (attribution) → 8.

**Runtime:** pi — `deepseek/deepseek-v4-flash` kids under `qwen/qwen3.8-27b`
parents. No pi agent dispatched yet this loop; L1.01 was engine-primitive work.

### 🔴 Crons are still OFF — push by hand

```bash
git -C /home/ubuntu/work/agi push origin master
```

## §1 The plan, and where it is

The owner granted director authority for a 10-iteration budget on 2026-09-03.
Concurrency ramps deliberately; **nothing ramps past a cap that has not
survived a live run.**

- [x] **L1.01** — config, the `write`/`links` rename, the workspace probe.
- [x] **L1.02** — first live agents on minted keys. **The mvp is not closed:**
      Part A was *disproved and then fixed*; Part B (provisioning-absent
      fallback) has still never been run live.
- [x] **L1.03** — the bound at 8 + `goal:g1.11` Part B. **The mvp is not
      closed:** cap 25 and clauses 2/3 are untouched.
- [ ] **L1.04** — viewport `--emit llm` reaches INJECTION parity. **NEXT.**
- [ ] **L1.05** — INJECTION.md retired, 4 render paths deleted. Cap 12.
- [ ] **L1.06** — `agi <verb>` router; `view` / `view-llm` / `write` declared.
- [ ] **L1.07** — `write.py create`; schema backfill rides along. Cap 16.
- [ ] **L1.08** — parent-spawns-kid live; per-agent grid scratchpad;
      **the removal guard** (`goal:g3` extended: deprecation cannot raise the
      primary). Cap 20. **The guard must land before L1.09.**
- [ ] **L1.09** — WIDE. Cavekit exit + legacy sweep. Cap 25.
- [ ] **L1.10** — webhook / direct model calls with session id → chat-to-node
      linking (`goal:g10.1`, `goal:g2.7`); engine-commit pinning; loop-scoped
      iteration numbering.

## §2 What landed in L1.01

### Config, on the owner's direction

`per_spawn_limit_usd` **0.25 → 5.00**. `max_goals_active` **9 → 15**.

The goals cap moved because the owner corrected what `active` *means*:
it is a **focus budget** — which long-term goals chain-building aims at — not
a census of what is in flight. `metrics.py`'s warning said the opposite and
would have been "fixed" by relabelling four real goals `horizon`, which is the
field losing information a second way. Reworded, not just re-capped. This
settles banked decision 3 from the previous session. Recorded on `goal:g5`.

### Keys mint into the `agi` workspace — a safety change, not tidiness

Probed against the live API **before** writing the code: `POST /keys` accepts
`workspace_id`, returns it on the created object, and a probe key landed in
the right workspace and was revoked. Both workspaces exist:

```
72750376-2d45-452e-8273-197fdaabae95  agi       ← keys mint here now
7e12bcd2-321e-51ec-b3f5-80efeb4fdaf0  default   ← the owner's own `agi` key
```

🔴 **Why this is safety.** `reap_orphans` matches the name prefix `agi-`, and
the owner's long-lived key is named `agi`. One character separated the reaper
from the key the project runs on. The reaper now also requires a key to be
**in the declared workspace**, so those two sets are disjoint by construction
rather than by string comparison — **two filters that fail differently**.
The owner's key is in `default` and is out of scope on both grounds.

`provisioning.workspace(cfg)` is a **sibling reader, not a third slot in
`settings()`** — that tuple has callers. Unset omits the field entirely rather
than sending null, so an unconfigured project is byte-identical to before.

### The latency question is closed

Mint is **0.760s** mean. The owner ruled it acceptable: inference already eats
1–3s, so a fraction of a second hides inside noise the run already has.
Recorded on `mvp:a-live-loop-on-minted-keys`.

### `edit.py` → `write.py`, and `write.py` → `links.py`

The owner's call, and the right one: a verb here either revises a node or
mints one, and both are **writes** — `create` would have read as an exception
to the module it lives in. The old `write.py` never wrote anything; it is
`link_ref` resolution and the `broken_links` count, so it is now `links.py`.
Two honest names beat one name doing two jobs.

Both renames used `git mv`; no build node exists for either file yet, so
`level3.py` will mint them under the new names at the next scan and there is
no `payload_ref` churn.

## §2b What landed in L1.02 — a disproof worth more than the feature

**pi does not read `OPENROUTER_API_KEY`.** Its `auth.json` uses the
`"!command"` indirection and points at `bin/env-get.sh`, which sourced `.env`
unconditionally. So `dispatch.py` minted a capped, expiring, per-agent
credential, injected it correctly — verified from `/proc/<pid>/environ`, not
from our own logs — and pi looked straight past it at the shared key.

```
iter-1002  both minted keys usage=0   shared key 4.433 -> 4.455 DURING the run
iter-1003  agi-iter1003-kid-a00 usage=0.0021   shared 4.4687 (pre-run, unchanged)
```

`goal:g1.11` was decorative end to end, and `env-get.sh` had **zero tests**.
**A stub that reads `$OPENROUTER_API_KEY` proves the injection happened; it
cannot prove the harness reads what was injected.** Recorded as `disproved`
in `experiment:per-spawn-keys-were-never-used`, not softened.

🔴 **Second defect, mine, from L1.01.** `GET /keys` is scoped to the *default*
workspace and does not say so. Keys minted into `agi` were invisible to
`list_keys`, so `status` said `engine_minted=0` with two keys live and
`reap_orphans` revoked nothing while truthfully reporting "0 orphaned" about
the wrong set. **The safety move made the backstop strictly worse for ~40
minutes** — old hazard: revoking too much; new one: revoking nothing, silently.

**What held:** injection, the provisioning-key scrub (0 occurrences in a kid),
revoke-on-reclaim live for the first time, and 0 outstanding keys afterwards.

## §2c What landed in L1.03 — the bound holds, and a warning about the ramp

**Part B ran.** With the provisioning key removed from `.env`: `available()`
False, dispatch exit 0, the minting line **absent** (skipped, not failed),
zero `OPENROUTER_*` vars in the kid's environ, zero minted keys, shared-key
usage moving. `goal:g1.11`'s falsifier is complete in both halves.

**The bound at 8**, sampled every 2s because a peak is invisible in an end
state:

```
PEAK leases=8  pi_procs=8   over 113 samples / ~226s
manifest 8 agents, 0 unadmitted · nodes 926 -> 935, exactly +9
8 distinct keys, 8 distinct bills, 0 outstanding afterwards
```

Peak **equals** cap — on the boundary, same signature as the synthetic 1/3/5.

### 🔴 Concurrency at one target buys duplicates, not coverage

**Six of eight kids wrote the same hypothesis.** Every slot was aimed with the
same `--target` and `--level`, so all eight got the same 2-hop subtree and
independently picked its most salient open thread. **`spawn.parallel` is a
throughput knob, not a coverage knob** — the marginal kid re-derives what the
previous kid is deriving *right now*, because none can see the others in
flight. This gets worse at 16 and 25.

**Implication for the ramp:** raising the cap without target diversity buys
duplicate tokens. Observe once more at 16 before deciding whether to fix it.

### 🔴 `goal:s31`'s "lift" fails ~33% and it hides the best node

4 of 12 kid nodes this session shipped a placeholder title and empty
`testable_claim` while the claim sat in the body two lines below. **Seed
works; lift does not.** Not cosmetic: `a05` carried the most valuable claim in
the batch — `goal:g4.8` clause 2, the never-observed one — under a title that
read like noise, and selecting by title is what every renderer and zoom does.

## §3 🔴 Where it stopped, and the exact next command

L1.03 is committed, grid-versioned and pushed. **Next is L1.04** — engine
work, no kids: bring `viewport.py --emit llm` up to `INJECTION.md` parity.

```bash
cd /home/ubuntu/work/agi
python3 extensions/agi/bin/viewport.py --emit llm | wc -l   # 45
wc -l .agi/context/INJECTION.md                             # 271
python3 extensions/agi/bin/commands.py run viewport-verify
```

The gap is not structure — it is the rules header, the stats block and the
command table that `render-context.py` adds and the viewport does not.
**L1.05 deletes four render paths once this lands**, so parity is the gate.

## §4 Traps hit this session

1. 🔴 **I wrote the same guard three times and the first two were vacuous.**
   The rename broke `links` and `schema` (declared as `write.py links`), and
   the existing test stayed green because it only checks the *file* exists —
   and a file by that name did. It was the wrong file.
   - **v1** shelled out to `script.py <sub> --help` and checked the exit code.
     argparse handles `--help` first and exits **0**, so the new `write.py`
     absorbed `links` as a positional and printed its own help. Passed on the
     bug.
   - **v2** read the script with `ast` but treated "declares no subcommands"
     as a skip. The new `write.py` declares none, so it skipped the one case
     it existed for. Passed on the bug.
   - **v3** treats that absence as the failure. Fails on the bug, passes clean.

   **The lesson is the method, not the bug: a guard is not a guard until it
   has failed once on purpose.** Reintroduce the defect and watch it go red.
   Both dead ends are recorded in the test's own docstring so the next reader
   does not re-propose v1.
2. **The declared command table caught the rename before any human did** —
   `goal:g1.10` earning its keep a second time. Prose copies stayed wrong and
   silent; the runnable one failed immediately.
3. **`commands.load()` needs the graph root (`.agi`), not the repo root.**
   Passing the repo root returns `0 commands` with no error — it looks like an
   empty table rather than a wrong argument.
4. 🔴 **A mock of the counterparty can only confirm what its author believed
   the counterparty does.** The whole of §2b. The seam — 30 lines of bash where
   the engine's credential meets the harness's auth — had no tests, while its
   docstring described a *different* hazard (cwd anchoring) in detail.
5. **`pgrep -af "cli.js"` does not find pi.** The process is named `pi`. I
   concluded "both kids have exited" while one had four minutes left to run,
   and nearly wrote that into a node.
6. **Piping a long background command through `tail` hides it until it ends.**
   Two runs produced no interim output at all. Redirect to a file instead.
7. **Usage figures lag slightly but attribution does not.** The shared key's
   number kept moving for a minute after a kid died; the *split* between keys
   was correct immediately. Compare keys against each other, not against wall
   clock.

## §5 Known-good verification sequence

```bash
python3 extensions/agi/bin/commands.py run smoke     # 922 active, must NOT drop
python3 extensions/agi/bin/commands.py run tests     # 1340 passing
python3 extensions/agi/bin/commands.py run goals-check
python3 extensions/agi/bin/commands.py run viewport-verify
python3 extensions/agi/bin/commands.py run links     # 927 resolved, 0 broken
python3 extensions/agi/bin/commands.py run grid-commit
```

## §6 🔵 BANKED — decisions deliberately not made

1. **Backfill the 115 schema-invalid nodes.** Unchanged, and now **scheduled**
   rather than banked: it rides along in L1.07 and widens in L1.09. The owner
   approved it explicitly.
2. ~~Viewport replaces `INJECTION.md`~~ — **SETTLED: yes.** L1.04 + L1.05.
   Measured gap: `--emit llm` is 45 lines against `INJECTION.md`'s 271, so it
   is *finish the emit, then delete four render paths*, not a swap.
3. ~~`goals_active` counting~~ — **SETTLED: it is a focus budget.** Cap 15.
4. ~~`goal:g1.11` batching granularity~~ — **SETTLED: per spawn** (prior run).

## §7 Standing hazards

- **The two live runs still have not happened.** The bound, the credentials
  and the reaper are proved against sleeping interpreters and fake adapters. A
  `SIGSTOP`ped agent is alive to `os.kill(pid, 0)` and holds its slot forever —
  correct, and still a surprise at cap 25.
- **$15.57 is the real ceiling**, not the `$5` per-key cap. Three keys at full
  cap is the balance. `spawn_budget` and the reaper know about per-key limits
  and **nothing knows about the account balance.**
- 🔴 **L1.09 has two ordering constraints that are load-bearing.**
  `snapshot-build-site.py` **deletes every `origin: build-site` node it does
  not re-derive** — so kits are removed *after* their 168 nodes are deprecated,
  never before (H0i). And a `payload_ref` is dropped *before* its file is
  deleted, or `broken_links` leaves 0.
- **`TODO.md` is already `status: deprecated`** — the 2026-09-02 timestamp is
  the retirement stamp, not an agent writing to it. Nothing uses it as a
  scratchpad. Mine it for unminted content in L1.09, then delete the file.
- **A parent's REPORT is not its artefact.** Check the node file.
- **A fix with no test is an assertion** — and per §4, a test that has never
  failed on purpose is closer to an assertion than it looks.
