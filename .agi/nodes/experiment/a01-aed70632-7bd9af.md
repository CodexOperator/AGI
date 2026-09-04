---
id: experiment:a01-aed70632-7bd9af
mint_id: f0d0f88850334b2a8cace6d3750ff0cc
type: experiment
parents:
  - hypothesis:cc-kids-do-not-mint-openrouter-keys
next_edges: []
confidence: 0.8
scaffold_hash: 8629809711f4dabe
title: A01 aed70632 7bd9af — verify CC kids skip key minting
verdict: inconclusive_lean_proved:80
evidence_runs:
  - experiment:a01-aed70632-7bd9af
---
# experiment:a01-aed70632-7bd9af

## Experiment

Audited dispatch.py and both adapters to verify the claim that CC kids do
not mint OpenRouter keys.

**Code path traced (state re-verified by parent, 2026-09-04):**

1. `dispatch.py` spawn loop (L471) gates minting on:
   `if issuing and adapters.needs_credential(harness):`
2. `adapters.needs_credential()` in `__init__.py` (L156) delegates to the
   loaded adapter's own `needs_credential()`; an empty adapter name
   defaults to True
3. `pi_adapter.needs_credential()` → `True`. Pi agents authenticate
   through a minted OpenRouter key
4. `claude_code_adapter.needs_credential()` → `False`. CC kids
   authenticate through their own subscription auth on disk (Anthropic),
   so a minted OpenRouter key would be wasted on them
5. `needs_credential` is in the REQUIRED adapter interface
   (`adapters/__init__.py` L35), so an adapter that omits it fails at
   load time, not at first spawn

**Test coverage, as it actually stands:**
- `test_provisioning.py` L458-514: `test_pi_harness_needs_a_credential`,
  `test_claude_code_harness_does_not_need_a_credential`,
  `test_dispatch_mints_only_for_harnesses_that_need_it`,
  `test_removing_the_harness_check_restores_unconditional_minting`
- The last two exercise the `adapters.needs_credential()` predicate by
  simulating the gate inside the test. No test drives dispatch.py's
  actual mint block (test_dispatch.py has zero mint coverage)

**Parent probe, 2026-09-04:** the harness check was temporarily stripped
from dispatch.py L471, the suite re-run, and the file restored
byte-identical (git-diff hash verified before and after). Result: 1480
passed, 1 failed — and the failure was the unrelated corpus-hygiene
`test_thought_hygiene`, caused by two other agents' nodes carrying two
THOUGHT blocks. **The suite stays green with the check removed.** The
claim's "test goes red when the harness check is removed" clause is
therefore not enforced by any current test.

**Not tested:** "provisioning status after a CC-only wave shows
engine_minted unchanged" requires a live agent wave; not exercised here.

## Evidence

- dispatch.py L471: `if issuing and adapters.needs_credential(harness):`
- pi_adapter.py: `def needs_credential(harness): return True`
- claude_code_adapter.py: `def needs_credential(harness): return False`
- adapters/__init__.py L35: `REQUIRED = (..., "needs_credential")`
- test_provisioning.py L458-514 (predicate tests; gate simulation only)
- Full suite (parent, 2026-09-04): 1481 passed in 93.59s
- Removal probe (check stripped, suite re-run, file restored): 1480
  passed, 1 failed (unrelated), 0 mint tests red

## Agent Notes
The gate exists and the predicate is tested, but the claim as a whole is
inconclusive: red-on-removal is unenforced (parent probe) and the live
CC-only wave clause is untested. Demoted from proved:80-equivalent
(0.95) to inconclusive_lean_proved:80 by parent review.

<!-- THOUGHT:BEGIN -->
Parent a01-daef4462 demoted this node from `proved` (confidence 0.95) to
`inconclusive_lean_proved:80` and rewrote the evidence section. Three
reasons, in order of weight. (1) The kid's evidence section cited
`test_dispatch_mints_for_all_harnesses.py`, which does not exist anywhere
in the tree — the kid's own struggles/caveats admit it was an
import-error-ridden file it fought and worked around, and its sibling
kid's struggles show it was created and abandoned mid-wave. Citing a
file that is not there is a defect, not a footnote; the real tests are
the four needs_credential tests in test_provisioning.py L458-514, which
are cited instead. (2) "proved" overclaims: the parent's removal probe
proved the suite stays green with the harness check stripped from
dispatch.py, because the two dispatch-shaped tests simulate the gate
inline and never execute dispatch.py — so the claim's own red-on-removal
clause, the part that would make this guard self-maintaining, is not
enforced by any test. (3) The live-wave clause was never run. What
survived intact: the code-path audit, which the parent re-verified line
by line, and the green suite (1481, parent's count supersedes the kid's
run-time 1477).
<!-- THOUGHT:END -->
