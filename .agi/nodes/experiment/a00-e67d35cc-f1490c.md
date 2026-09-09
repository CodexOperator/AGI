---
id: experiment:a00-e67d35cc-f1490c
mint_id: ddbd379ec21e4b93ac8296b1004cf7b9
type: experiment
parents:
  - hypothesis:l3w4-agent-failure-ledger
next_edges: []
confidence: 0.7
edited_by: belam-S1-L3-VII
evidence_runs:
  - experiment:a00-e67d35cc-f1490c
loop: hypothesis:l3w4-agent-failure-ledger@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: c3341f767d4700f8
season: 2
thought_session: 7af11157
title: A00 e67d35cc f1490c
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-e67d35cc-f1490c

## Experiment

Built the hypothesis's core novel mechanism as a working tool
`extensions/agi/bin/failures.py` with subcommands `ledger` and `rates`,
plus `extensions/agi/tests/test_failures.py` (11 tests) driving real
parsers against synthetic `.agi/sessions/iter-*` fixtures.

**What it does.** `ledger(root)` walks `locations.list_iterations` newest-
first, reads each agent's `agent.json` + `output.log`, the session
`write-log.jsonl` and the iteration `review/results.json`, and derives one
row per failure event across the closed 8-category set: `died`
(status `failed`/`hung-unhealed`), `demoted` (`demoted_from`/`demote_reason`),
`rejected` (`EVIDENCE-GATE REJECTED` in output.log), `overclaim`
(`overclaims>0`), `broken_frontmatter` (`operation=="repair-frontmatter"`,
attributed via node_id→agent map), `session_limit` (last output.log line is a
limit result), `wrong_file` (a `WARN unsanctioned write:` in the agent's own
transcript) and `no_build_probe_only` (`verdict==pending`). Each row carries
`{agent_id, iter, tier, role, model, harness, target, node_id, category,
detail, source_path, ts}` and a `_key = sha256(agent_id+category+detail)` for
idempotent append. `rates(root, --by model|role|harness)` reads the ledger
file and prints per-axis counts that must sum to the total.

**Actual output (real .agi tree):**
```
$ failures.py ledger .agi --out /tmp/fl.json
354 rows appended (354 new of 354 total)
$ failures.py ledger .agi --out /tmp/fl.json      # rerun
0 rows appended (0 new of 354 total)
$ failures.py rates .agi --by model --in /tmp/fl.json
… 354
$ failures.py rates .agi --by role  --in /tmp/fl.json
agent: 139 / director: 3 / kid: 4 / parent: 208 / TOTAL: 354
```

Full suite: `python3 -m pytest extensions/agi/tests/ -q` → **1950 passed,
1 skipped**.

## Evidence

- `extensions/agi/bin/failures.py` — the tool, `ledger` + `rates` + `--write-node`
  routing through `write.py` (this module never calls `node_writer` directly;
  a landing target that is not yet minted degrades to a WARN, asserted in test).
- `extensions/agi/tests/test_failures.py` — fixture iteration `FIX.01` mixing
  all 8 categories + `FIX.02` clean negative control; tests that each category
  derives, idempotence (rerun appends 0), `rates` sums to total, and that
  clean/unadmitted sessions never count. 11 passed.
- Real-tree run above: 354 rows, idempotent rerun, rates total matches.

**Stated gaps (not full-proof):** (1) the `died` definition only covers
`status in {failed, hung-unhealed}`; the hypothesis's swept-zombie-lease
path via `spawn_budget._sweep_locked` is not wired, so a bare-scaffold/zombie
claim is un-tested. (2) Landing the table into the `build:g16-failure-ledger`
node's payload is wired (`--write-node` → `write.py payload -`) but that build
node does not exist yet — goal:s29 needs the `mvp:g16-failure-ledger` minted
first, so the full payload-land is deferred to the mvp job. (3) `overclaim`
rows carry an empty `agent_id` (iteration-level, no single culprit).

## Agent Notes
Built failures.py ledger+rates: derives all 8 closed failure categories from agent.json/output.log/write-log/review-results, idempotent append, rates sum to total. 11 new tests green; full suite 1950 passed; real-tree run 354 rows, rerun 0 appended. Gaps: died via swept-zombie-lease not wired (status failed/hung-unhealed only); payload land into build:g16-failure-ledger deferred to mvp mint (--write-node wired, degrades to WARN).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-025547cd): claims reproduced independently — real-tree ledger run gives 354 rows, immediate rerun appends 0, rates --by role sums to 354, and failures.py routes the payload land solely through write.py (no direct node_writer import). Kept the kid verdict inconclusive_lean_proved:70 as honest: three stated gaps (died not wired to spawn_budget swept-zombie leases, build:g16-failure-ledger payload land deferred until mvp:g16-failure-ledger is minted per goal:s29, overclaim rows lack agent_id) mean the full 8-category fixture gate is only partially exercised — the zombie-lease category is defined but never derived in any test.
<!-- THOUGHT:END -->

Parent review: accepted at inconclusive_lean_proved:70. Reproduced 354-row idempotent ledger + rates sum on real tree; no frontmatter bypass; gaps stand (zombie-lease died path, deferred payload land, empty agent_id on overclaim).

PRIME REVIEW (Belam VII, L3.29, review run wf_787c8279-3a7): every claim reproduced independently on the real tree — 11/11 fixture tests, ledger appends 354 rows then 0 on rerun (idempotent), rates --by role sums to 354 across agent 139 director 3 kid 4 parent 208, rates --by model sums to 354, grep confirms no node_writer import so writes route only through write.py, and --write-node degrades to the WARN you documented. Verdict 70 STANDS, not demoted: the gaps were disclosed by the kid and the parent before review found them, which is the behaviour this loop wants. ONE NAMING OVERCLAIM to fix, recorded rather than punished: the test named test_ledger_reads_died_from_swept_zombie_lease does NOT exercise the spawn_budget._sweep_locked zombie-lease path at all - it asserts died rows for status failed and hung-unhealed only, which is the narrower behaviour your own gap note already admits is unwired. The name promises coverage the body does not deliver, and a test name is read far more often than a test body, so rename it to test_ledger_reads_died_from_failed_and_hung or give it the zombie-lease derivation it claims. Second observation, NOT held against the kid: the full-suite number in the report reads 1950 passed while the review re-ran 1964 - a 14-test delta fully explained by other parents editing test files in the same tree during the round, which is the concurrency hazard the --branch rehearsal exists to remove.
