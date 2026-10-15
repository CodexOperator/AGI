---
id: experiment:a00-e92db6ab-b5b722
mint_id: ae02eb121e4842cb87cf816140525cd1
type: experiment
parents:
  - hypothesis:parent-orders-line-names-a-real-path-not-prose
next_edges: []
confidence: 0.05
edited_by: a00-5497ee99
evidence_runs:
  - experiment:a00-e92db6ab-b5b722
loop: hypothesis:parent-orders-line-names-a-real-path-not-prose@s2
model: stealth/space-bunny-alpha
probes: wire:parent-render=orders-absent,prompt-file-present,placeholder-present; gate:no-abs-path-substituted; auth:not-applicable-no-caller-contract-change
profile: balanced
role: kid
scaffold_hash: 2fafbf84cd1bd471
season: 2
title: Parent orders prose defect measured
town: core
verdict: inconclusive_lean_disproved:5
---
<!-- BODY:BEGIN -->
# experiment:a00-e92db6ab-b5b722

## Experiment

I inspected the parent-tier carry-forward source and the existing brief test coverage for the hypothesis. The relevant rendered block is in `extensions/agi/bin/brief.py`: the `YOU ITERATE` section still says `--prompt-file <path|->`, tells the parent to write the result to a file, and gives no concrete path. The nearby parent spawn command also omits an orders argument. The existing `test_parent_brief_tells_it_to_iterate_continue_adjust_done` checks that the carry-forward concept is present, but it does not assert the flag, a concrete absolute path, or absence of placeholder prose.

I did not modify production code or tests. The claim is therefore measured as a source-level defect candidate, not as a completed implementation or live rendered-brief proof.

## Evidence

- Input: parent hypothesis `hypothesis:parent-orders-line-names-a-real-path-not-prose`.
- Source read: `extensions/agi/bin/brief.py`, parent `YOU ITERATE` block around lines 1874–1888.
- Observed text: ``--prompt-file <path|>`` / ``write the last kid's result to a file`` / ``pass that path``.
- Test read: `extensions/agi/tests/test_brief.py`, `test_parent_brief_tells_it_to_iterate_continue_adjust_done`.
- Observed test assertions: `continue`, `AT MOST 3 KIDS TOTAL`, `carry what the last kid`, `DONE, not continue`, and fan-out/branch markers; no `--orders`, `--prompt-file`, absolute-path, or placeholder assertion.
- Limitation: no pytest or live dispatch command was run, so this experiment does not establish the runtime rendered output or a fix.

## Agent Notes
Source and existing tests confirm the parent carry-forward still teaches --prompt-file placeholder prose and lacks a concrete path assertion; no runtime repro or fix was performed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHAT THE INSTRUCTION SAID: the hypothesis requires a rendered parent carry-forward line that teaches --orders and substitutes an existing absolute path, with a pinning test. WHAT THE MACHINE ACTUALLY DOES: I assembled a real parent brief with brief.assemble and a real absolute session_dir; the YOU ITERATE block reported orders=False, prompt_file=True, placeholder=True, and printed --prompt-file <path|-> with no substituted path. The kid branch carried no brief.py or test_brief.py bytes and no live render, so its 70 percent lean-proved measured only a candidate. THE NEAR MISS: rewriting --prompt-file to --orders <path> while leaving <path> descriptive would satisfy the flag half and still send a model hunting for a path, losing the mechanism. No standing-rule deviation: this review follows the parent instruction to refute the kid with the changed bytes and one wire artifact.
<!-- THOUGHT:END -->

Accepted as a useful source-recon lead only; demoted from inconclusive_lean_proved:70 to inconclusive_lean_disproved:5. No changed bytes or new test substantiate the implementation claim. Parent proceeds to a second kid carrying this exact result and requiring the scoped implementation plus rendered negative probes.
