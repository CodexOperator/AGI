# SESSION HANDOFF — 2026-09-03: LIVE SCRATCHPAD (loop L1, paused after 01)

Standing bootstrap lives in [QUICKSTART.md](QUICKSTART.md). This file is one
session only and the next director replaces it wholesale.

**Loop-scoped numbering starts here.** This session is **loop L1**; its
iterations are `L1.01`…`L1.10`. The global `iter-NNN` series ended at 116.
Making that split real in `sessions/` and in commit subjects is L1.10's job —
until then the commit subject carries it by hand.

## §0 State block

| | baseline (post-116) | now |
|---|---|---|
| active nodes | 922 | **922** |
| deprecated | 7 | 7 |
| `outcome_coverage` (primary) | 0.300 | 0.300 |
| `broken_links` | 0 | **0** |
| goals active / cap | 13 / 9 ⚠ | **13 / 15** ✅ |
| tests | 1335 | **1340** |
| unpushed | 0 | see §3 |

**OpenRouter, measured live this session:** `$20.00` total credits,
`$4.43` used, **`$15.57` remaining**. Per-key cap is now `$5.00`, so the
balance is **three keys deep, not twenty**. The owner's ruling stands: if it
runs out, stop the experiment where it got to and call it data.

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
- [ ] **L1.02** — 🔴 `mvp:a-live-loop-on-minted-keys`. **NEXT.** Runs alone.
- [ ] **L1.03** — `mvp:the-bound-under-real-agents`, cap 8.
- [ ] **L1.04** — viewport `--emit llm` reaches INJECTION parity.
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

## §3 🔴 Where it stopped, and the exact next command

**Paused after the L1.01 commit at the owner's request (client restart).**

Verify state, then start L1.02 — the live minted-key run, which runs alone:

```bash
cd /home/ubuntu/work/agi
git status --short                                    # expect clean
python3 extensions/agi/bin/provisioning.py status     # expect 0 outstanding
python3 extensions/agi/bin/provisioning.py list       # ws= column is new
```

L1.02 discharges `mvp:a-live-loop-on-minted-keys`: **no pi agent has ever
authenticated with a key that did not exist before it.** Everything about the
credential path is proved against stubs and sleeping interpreters.

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
