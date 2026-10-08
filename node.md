---
id: experiment:a00-cede29bc-b27151
mint_id: 65abac47cf744623a587e39d992a6151
type: experiment
parents:
  - hypothesis:l4-the-orders-channel-refuses-what-it-cannot-deliver-and-every-orders-record-names-bytes-that-reached-a-brief
next_edges: []
confidence: 0.8
edited_by: a00-e9a79454
evidence_runs:
  - experiment:a00-cede29bc-b27151
loop: hypothesis:l4-the-orders-channel-refuses-what-it-cannot-deliver-and-every-orders-record-names-bytes-that-reached-a-brief@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 4, "class": "gate", "cmd": "live dispatch --tier parent --orders o.md --from KID2PROBE --target hypothesis:l4-x (refused by the zoom gate, rc1)", "expected": "no orphan orders copy", "observed": "no orders.KID2PROBE.md written; pre-fix left orders.SAME.md", "result": "pass"}
  - {"conjunct": 4, "class": "wire", "cmd": "two parent dispatch.main() runs into one iter dir with the SAME --from SAME (Popen/adapters/zoom faked)", "expected": "two per-agent files, two manifest records", "observed": "FILES [orders.a00-15eaa9fb.md, orders.a00-a8ee4fe0.md]; each REC names its own file", "result": "pass"}
profile: balanced
role: kid
scaffold_hash: d7d00d7adadb9cce
season: 2
title: A00 cede29bc b27151
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-cede29bc-b27151

## Experiment

Claim under test: `hypothesis:l4-the-orders-channel-refuses-what-it-cannot-
deliver-and-every-orders-record-names-bytes-that-reached-a-brief`, conjunct
(4) ONLY — "`<iter>/orders.md` is per-parent: `<iter>/orders.<agent>.md` keyed
like the manifest parent record, written AFTER the last refusal gate so a
refused dispatch leaves no orphan file, and the manifest path cell names it".
SM.28 kid1 (`experiment:a00-0d3f3f2f-5b7b2a`) built conjuncts 1,2,3,5; the
parent probe failed conjunct 4 two ways, both on the built bytes:

- **KEYING** — the copy was keyed by `AGI_ORDERS_FROM` (`orders.<from>.md`,
  default `unspecified`) and written at `dispatch.py:2105`, BEFORE `agent_id`
  is minted at `:2119`. Two parents dispatching into one iter dir with the same
  `--from` (or both defaulting) overwrite each other's file.
- **ORPHAN** — the same write sat ABOVE the per-slot gates (spawn-budget
  lease, zoom render, model allowlist), so a dispatch refused at any per-slot
  gate left an orders file with no manifest record beside it.

### What I did

Moved the copy INSIDE the slot loop: `_orders_file = iter_dir /
"orders.<agent_id>.md"`, written after the last per-slot refusal gate and
above `Popen`; the manifest record's `orders.path` is the resolved absolute
path of that per-agent file. On a `Popen` failure the copy is unlinked, so
no path that fails to produce an agent record leaves an orphan either.
Production diff: `extensions/agi/bin/dispatch.py` — the 16-line pre-loop
block (old `:2090-2105`) becomes an 8-line comment above the loop; +10 lines
above `Popen` (new `:2468-2478`); +4 lines in the `except BaseException`
around `Popen`. Net production lines: ONE, well under the ~20 ceiling.

Tests changed/added:

- `extensions/agi/tests/test_dispatch_dry_run.py`
  `test_a_dispatch_refused_at_the_zoom_gate_leaves_no_orders_copy` — LIVE
  subprocess, claude-code harness, bogus `--target`: refuses at the zoom
  render inside the slot loop (rc 1, no spawn) and asserts the iter dir holds
  no `orders.*`.
- `extensions/agi/tests/test_dispatch.py`
  `test_orders_copy_is_per_agent_and_written_after_the_last_refusal_gate`
  (structural, renamed/repointed from the old per-parent check) plus
  `test_two_parents_keep_separate_orders_copies_in_one_iter_dir` — live
  `dispatch.main()` with only the process boundary faked (`adapters.load`,
  `subprocess.Popen`, the zoom `subprocess.run`): two parent dispatches into
  ONE iter-001 with the SAME `--from SAME` leave TWO files named
  `orders.<agent_id>.md` and TWO manifest records each naming its own path.
- `extensions/agi/tests/test_node_writer.py` — the
  session-artefact allowlist in
  `test_dispatch_no_longer_touches_the_node_tree_at_all` updated from the
  bare `orders.md` string to `_orders_file` (the assertion caught the re-key:
  the write line no longer carries an `orders.md` comment).

## Evidence

Pre-fix falsification, ON THE BUILT BYTES: hoisting the copy back above the
slot loop as `orders.PRE-FIX.md` makes the new live test fail exactly as the
parent measured:

```
E  AssertionError: a dispatch refused at the zoom gate left an orphan orders copy:
   [PosixPath('/tmp/pytest-of-ubuntu/pytest-6698/test_a_dispatch_refused_at_the0/
    .agi/sessions/iter-001/orders.PRE-FIX.md')]
1 failed, 26 deselected in 0.37s
```

With the probe removed (the shipped code):

```
$ python3 -m pytest extensions/agi/tests/test_dispatch_dry_run.py -q -k refused_at_the_zoom_gate
1 passed, 26 deselected in 0.60s

$ python3 -m pytest extensions/agi/tests/test_dispatch.py -q -k separate_orders_copies
1 passed, 120 deselected in 0.54s

$ python3 -m pytest extensions/agi/tests/test_dispatch.py -q -k orders_copy
1 passed, 119 deselected in 0.51s

$ python3 -m pytest extensions/agi/tests/test_dispatch.py \
    extensions/agi/tests/test_dispatch_dry_run.py extensions/agi/tests/test_brief.py \
    extensions/agi/tests/test_node_writer.py -q
376 passed, 63 warnings in 49.81s
```

Final shape in `dispatch.py`: one `_orders_text` `write_text` in the whole
file, inside the slot loop, target `_orders_file`, template
`f"orders.{agent_id}.md"`; the manifest cell is
`str(_orders_file.resolve())` (absolute); no bare `"orders.md"` literal
survives. `test_node_writer.py` first FAILED on the shipped change with
`_orders_file.write_text(...)` not on the allowlist — that is the assertion
working, and the allowlist was corrected to name the new artefact.

## Verdict

proved for conjunct (4): keying by agent id and the orphan fix are both
measured on the built bytes. Conjuncts 1, 2, 3, 5 were not touched.

## Agent Notes
conjunct 4 fixed on the built bytes: orders copy moved inside the slot loop, keyed by agent id (orders.<agent_id>.md), below every per-slot refusal gate and above Popen; manifest orders.path is the absolute per-agent file; copy unlinked on Popen failure. Evidence: live subprocess zoom-gate refusal leaves no orphan (falsification probe reproducing the pre-fix orphan fails it), two parents with the same --from into one iter dir keep two files + two records; 376 passed across test_dispatch/test_dispatch_dry_run/test_brief/test_node_writer.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-e9a79454), kid2 accepted.
WHAT THE INSTRUCTION SAID: fix conjunct (4) only -- "<iter>/orders.<agent>.md keyed like the manifest parent
record, written AFTER the last refusal gate so a refused dispatch leaves no orphan file, and the manifest path
cell names it".
WHAT THE MACHINE DOES (built bytes): the pre-loop write is gone; the only orders write is
dispatch.py:2476-2478 `_orders_file = iter_dir / f"orders.{agent_id}.md"` (agent_id minted at :2119, in the
same slot loop), placed after the lease (:2124), the zoom render and the mint/model gates, and immediately
before `Popen` (:2482); the `except BaseException` at :2491 unlinks it and returns 4, so no failure between
the write and Popen leaves the copy. The manifest cell at :2561 is `str(_orders_file.resolve())`.
THE NEAR MISS: keying on the slot INDEX or the target would read as "per-parent" and still collide across two
independent dispatches into one iter dir; keying on the sender (the kid1 bug) is the same trap. Only the
agent_id the manifest record carries is unique per record.
PROBES RUN BY THE PARENT: (a) LIVE orphan -- `dispatch --tier parent --orders o.md --from KID2PROBE --target
hypothesis:l4-x` (bogus target, refused by the zoom gate, rc 1) left NO orders.KID2PROBE.md; pre-fix the same
shape left orders.SAME.md. (b) KEYING -- an independent two-parent probe into one iter dir with the SAME
--from SAME produced `orders.a00-15eaa9fb.md` and `orders.a00-a8ee4fe0.md`, two manifest records each naming
its own file. Conjunct 4 now holds. Verdict left proved.
<!-- THOUGHT:END -->

PARENT REVIEW (a00-e9a79454): ACCEPTED. Conjunct 4 verified on the built bytes by two parent-run probes: a live zoom-gate refusal (rc1) leaves no orders copy, and two parents sharing --from SAME into one iter dir get two agent-keyed files each named by its own manifest record. The only orders write is dispatch.py:2478 inside the slot loop, below every per-slot gate and above Popen, unlinked on Popen failure. Kid1 remains inconclusive_lean_disproved:70 (conjuncts 1,2,3,5 hold; 4 was its miss).
