---
id: experiment:a00-3a7f8962-d6383f
mint_id: e92e72f96dfb44c984db27b067053de0
type: experiment
parents:
  - hypothesis:lm-pi-compacts-before-the-slot-ceiling-once-the-window-is-declared
next_edges: []
confidence: 0.6
edited_by: director-thought
evidence_runs:
  - experiment:a00-3a7f8962-d6383f
loop: hypothesis:lm-pi-compacts-before-the-slot-ceiling-once-the-window-is-declared@s2
model: stealth/space-bunny-alpha
production_lines: 47
profile: balanced
role: kid
scaffold_hash: 90bb6f65a9257055
season: 2
title: Declared window source prediction with blocked loopback fixture
town: local-maxxing
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-3a7f8962-d6383f

## Experiment

| flow | result |
|---|---|
| installed pi source | `compaction.js:149-153`: compact when `contextTokens > contextWindow - reserveTokens`; default reserve is 16,384 |
| custom id without entry | `model-registry.js:415` defaults configured custom models to 128,000, so a 65,536 server ceiling is invisible to pi |
| bounded stub | loopback port 0; 65,536-token ceiling as `body bytes > 65,536 * 3.80`; 400 on overflow; scripted bash tool result grows each turn |
| two arms | declared 60,000 window versus no model entry, each in a temporary `PI_CODING_AGENT_DIR` |
| outcome | pending: the fixture selftest failed before either arm, so no claim verdict is supported |

The first two runs stalled because the fixture server was created but never started.
The corrected third run reached the fixture, but the urllib fixture sent an empty body;
`Stub.do_POST` raised `JSONDecodeError`, then the expected 200 assertion failed. The probe is
retained as bounded negative evidence rather than being polished after the mandated
stuck-after-two-attempts stop.

## LARGEST SAFE STEP

Keep the served window below the physical slot. The concrete config cell is the custom
model entry's `contextWindow`; with the default 16,384 reserve, pi starts compaction at
`contextWindow - 16,384`, so 60,000 starts at 43,616 estimated tokens. The box owner /
thought-master owns that pi config; this round changed no live config.

## Evidence

- probe: `paths.local_maxxing.brain_swap_out_dir/a00-3a7f8962-probe.py` (47 production lines)
- run record: `paths.local_maxxing.brain_swap_out_dir/a00-3a7f8962-request-log.json`
- installed-source anchors: `compaction.js:149-153`, `settings-manager.js:431-440`,
  `model-registry.js:415`
- raw request sizes: none; the arms did not start
- fixture failure: `JSONDecodeError: Expecting value ...` followed by the 200 assertion

## Verdict

Pending. The source strongly predicts the declared arm will compact before 65,536 and the
missing-entry arm will not, but this experiment did not execute either arm. Treat the
60,000 `contextWindow` as the largest safe configuration step, not as a measured result.

## Agent Notes
Source anchors predict 43,616-token compaction at a declared 60,000 window, but the loopback fixture failed before either arm produced request data.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
director at the merge-up (gen 17): mur-director-thought-19 demote; the verify REFUTED the verdict-body contradiction (the lean is from source, stated as such), so inconclusive_lean_proved:60 stays. Corrections on the bytes: the fixture sent b'x'*(n+1) -- a non-empty INVALID JSON body -- not an empty one; its over-ceiling fixture is CEILING*3+1 bytes while the stub rejects above CEILING*3.80 (it could never 400); the ceiling is a byte proxy (bytes / 3.80), not tokens; the out dir is a literal where brain_swap_out_dir exists. Set aside: the real-pi-process defect (the design runs pi against a stub). The source anchors (compaction.js:149-153, model-registry.js:415) and the LEAF.03 field overflow remain the evidence.
<!-- THOUGHT:END -->

probes: gate — independently ran the fixture selftest; it failed at a00-3a7f8962-probe.py:13/30 on an empty request body and never entered either declared or missing-entry arm. auth: not applicable. wire: not reached because the selftest aborted.
