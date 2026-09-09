---
id: experiment:a00-a6c651f9-c9734d
mint_id: 31687861988149f7871101c84d7d8cd8
type: experiment
parents:
  - hypothesis:l3w4-agent-failure-ledger
next_edges: []
confidence: 0.95
evidence_runs:
  - experiment:a00-a6c651f9-c9734d
loop: hypothesis:l3w4-agent-failure-ledger@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: bcb903d0e3f86f61
season: 2
title: A00 a6c651f9 c9734d
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-a6c651f9-c9734d

## Experiment

Slice of `hypothesis:l3w4-agent-failure-ledger` (`MS.01` next-slice): prove the
full ledger data path runs against **real** session artifacts on the live
project root — derive → idempotent append → aggregate rate table →
`sensei.pick_worst` consuming the JSON array. The parent's SENSEI note claimed
`pick_worst` had never run against real data and `failure-ledger.json` had
never existed because nothing wires `failures.py ledger` into the loop. This
experiment answers: *can the path produce and consume a real ledger today?*

Commands run from `/home/ubuntu/work/agi`, writing the ledger/rates out to
`/tmp/ms01-ledger` (scratch, so nothing shared is touched):

```
1. python3 extensions/agi/bin/failures.py ledger .agi --out /tmp/ms01-ledger/ledger.json
2. python3 extensions/agi/bin/failures.py ledger .agi --out /tmp/ms01-ledger/ledger.json   (rerun)
3. python3 extensions/agi/bin/failures.py sensei .agi --by role --in .../ledger.json --out .../rates.json
4. python3 extensions/agi/bin/sensei.py pick_worst --ledger .../rates.json
```

## Evidence

Real, verified output (2026-09-08):

```
1. 405 rows appended (405 new of 405 total)          # derive from live artifacts
2. 0 rows appended (0 new of 405 total)              # idempotent rerun
3. wrote 10 rate rows (405 failure events) -> /tmp/ms01-ledger/rates.json
4. {"fail_rate": 0.3235, "failed": 131, "model": "qwen/qwen3.8-27b",
    "seat_or_role": "parent"}                        # pick_worst, no JSONDecodeError
```

What this proves (gaps #2 and #3 of the MS.01 next-slice are closed and now
verified live, not just unit-tested):

- `ledger()` derives **405 real rows** from the live graph's session artifacts
  and is **idempotent on rerun** (0 appended) — the row keying works.
- `failures.py sensei` (the `aggregate()` step) compresses the 405 raw
  per-event rows into the `seat_or_role/fail_rate/failed` shape `pick_worst`
  groups on — **10 rate rows summing to 405 events**.
- `sensei.pick_worst --ledger .../rates.json` reads that table as a JSON
  array with **no JSONDecodeError** (the old JSONL-assumption bug is fixed),
  and returns the worst `(seat_or_role, model)` group: `parent` / `qwen3.8-27b`,
  131 failures, fail_rate 0.3235.

The unit suite backs this up: `test_failures.py` (13 tests, all green) covers
derivation of all 8 categories, idempotence, rates-summing, and the
pick_worst-shape aggregation.

**Still open — wiring gap #1.** `failures.py ledger` is *not* scheduled by any
cron (`crons.md` declares only `grid_sync`/`branch_push`; neither invokes
the ledger) and no dispatch hook calls it, so `failure-ledger.json` still
does not exist in the live loop — the phase of the pipeline that needs to
*invoke* this verified path is what remains unwired. This run wrote to a
scratch path and did not land the table in any `build:g16-failure-ledger`
payload (that node is still unminted, `goal:s29` gate), so the write.py
landing half of the parent's testable_claim is *not* tested here.

## Agent Notes
MS.01: proved full ledger data path live — failures.py ledger derives 405 real rows (idempotent, 0 on rerun), sensei aggregate writes 10 pick_worst-shaped rate rows summing to 405, sensei.pick_worst reads JSON array with no JSONDecodeError (gaps #2,#3 closed & verified live). Wiring gap #1 still open: no cron/hook invokes the ledger.
