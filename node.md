---
id: experiment:a00-8d44610d-b25ed4
mint_id: 3b25d75528f5428b92e06ce6be431397
type: experiment
parents:
  - hypothesis:l4-the-after-join-dm-is-one-line-per-entry-detail-only-on-refusal-or-nonzero-record-named-by-graph-address
next_edges: []
confidence: 0.9
edited_by: a00-2d7d67b8
evidence_runs:
  - experiment:a00-8d44610d-b25ed4
loop: hypothesis:l4-the-after-join-dm-is-one-line-per-entry-detail-only-on-refusal-or-nonzero-record-named-by-graph-address@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "_compose_after_join_dm rc0 with sentinel cmd/output", "expected": "one line [label] exit 0, no cmd, no output", "observed": "ZCMDZ/ZOUTZ absent; [seed] exit 0 present", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "_compose_after_join_dm refused entry with reason sentinel", "expected": "one line carrying the reason, no cmd", "observed": "RSN present; CMD absent", "result": "pass"}
  - {"conjunct": 3, "class": "gate", "cmd": "_compose_after_join_dm rc=2 with output sentinel", "expected": "$ cmd + output kept", "observed": "[sync] exit 2, $ ls nope, OUT present", "result": "pass"}
  - {"conjunct": 4, "class": "wire", "cmd": "_compose_after_join_dm record_path=/ABS/p.json; then run the emitted address", "expected": "path absent, graph address present, command runs clean", "observed": "/ABS/p.json absent; status --post s --record latest present; running it prints no --seat deprecation note", "result": "pass"}
  - {"conjunct": 5, "class": "gate", "cmd": "_compose_after_join_dm with gen=1 ref=r", "expected": "captive ack --post line byte-identical", "observed": "ack --post s --gen 1 --ref r diff --text - present", "result": "pass"}
  - {"conjunct": 6, "class": "gate", "cmd": "_compose_after_join_dm rc=1 output 9000 chars dm_byte_cap=1500", "expected": "entry lines + one trimmed marker + graph address, no path, <=1500 bytes", "observed": "trimmed count 1; path absent; addr present; 1500-byte bound held", "result": "pass"}
profile: balanced
role: kid
scaffold_hash: 5168662d860d2d90
season: 2
title: A00 8d44610d b25ed4
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-8d44610d-b25ed4

## Experiment

CORRECTION ROUND (second kid, SM.01) — five of the six rule conjuncts of the
parent hypothesis already passed in a00-c2d776c3-7a60dc. Exactly ONE
conjunct (4) failed: the composer emitted the record's graph address with the
DEPRECATED `--seat` spelling.

```
python3 extensions/agi/bin/rotate.py status --seat s --record latest
-> note: --seat is deprecated; use --post this season.
```

`--seat` is a deprecated alias (`geometry_config.py:40-56`): a literal `--seat`
prints a warning notice, so the successor's first command would open with a
wordy redundancy — the exact thing the owner cut. FIX (rotate.py only + the
tests, nothing else):

- `_compose_after_join_dm` `graph_addr` :11336
  `status --seat {seat}` -> `status --post {seat}`
- its docstring graph-address mention :11308 likewise
- four test assertions (223, 2403, 2467, 2473) matched to `--post`

Ceiling held: 2 lines net in rotate.py, no test count change (6 composer
tests total).

## Evidence

- `python3 -m pytest extensions/agi/tests/test_after_join_service.py -q`
  -> 78 passed in 1.78s
- composer probe (rc0 under cap + rc1 over cap), record_path="/ABS/p.json":
  `status --post s --record latest` PRESENT, `/ABS/p.json` ABSENT,
  `--seat` ABSENT in both branches.
- live `status --post s --record latest` -> NO deprecation note (clean).
- falsifier `status --seat s --record latest` -> prints the notice,
  confirming the true defect the fix removes.

<!-- CORRECTION:BEGIN -->
THOUGHT: this round only repaired the dead-but-warning `--seat` spelling in
the emitted graph address to the live `--post` grammar (F6). No behaviour
change, no reformat. The rope is: the ack captive line already used `--post`
(SL7.74); the graph-address tail was the one straggler on the deprecated
alias.
<!-- CORRECTION:END -->

## Agent Notes
Fixed the one failing conjunct (4): composer graph-address tail emitted deprecated --seat; rewrote to --post (rotate.py graph_addr+docstring), matched 4 test assertions; 78 tests green, --post clean at live, --seat falsifier still warns.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-2d7d67b8, SM.01). (1) INSTRUCTION: correction brief from the parent - the emitted graph address must be `status --post <seat> --record latest` per claim conjunct (4); `--seat` is the deprecated alias. (2) MACHINE: the bytes at rotate.py:11336 now read `f"status --post {seat} --record latest"`, the docstring at :11308 says --post, and all four test assertions match `status --post`. Parent re-ran all six conjunct probes against the final bytes: rc0 one line (ZCMDZ/ZOUTZ absent), refusal reason kept, nonzero keeps cmd+output, record_path string absent while `status --post s --record latest` present under AND over budget, over-budget marker count 1 with the 1500-byte bound held, captive ack line byte-identical. Ran the emitted address live: no `note: --seat is deprecated` line. `pytest test_after_join_service.py` 78 passed. (3) NEAR MISS: fixing the composer string but leaving the tests asserting the deprecated alias would have kept a green suite while the claim conjunct still failed - checked all four assertion sites. (4) no standing-rule deviation. Verdict proved stands.
<!-- THOUGHT:END -->

PARENT-CONFIRMED proved. Corrected the emitted graph address from the deprecated --seat alias to --post (composer, docstring, 4 test assertions). All six claim conjuncts pass the parent probes; emitted address runs with no deprecation note; 78 tests green.
