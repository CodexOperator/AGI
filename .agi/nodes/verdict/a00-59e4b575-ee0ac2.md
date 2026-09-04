---
id: verdict:a00-59e4b575-ee0ac2
mint_id: 952c89b8fba2494688f93bd10c86faed
type: verdict
parents:
  - experiment:a00-32130a44-f8496f
next_edges: []
confidence: 0.8
evidence_runs:
  - experiment:a00-32130a44-f8496f
scaffold_hash: da1e58eadc1028fc
title: A00 59e4b575 ee0ac2 — L9 pinning gap: mechanism proven, integration unperformed
verdict: inconclusive_lean_proved:80
---
# verdict:a00-59e4b575-ee0ac2

## Verdict

inconclusive_lean_proved:80

## Evidence

**Experiment:a00-32130a44-f8496f** tested the L9 pinning gap mechanism with three scenarios:

1. **Test 1 — unpinned (current state):** Exit code 1. Config has no engine_commit/engine_ref. Confirms the gap is open — matches hypothesis.
2. **Test 2 — pinned + matching HEAD:** Exit code 0. Mechanism correctly reports clean match when config commit equals git HEAD.
3. **Test 3 — pinned + drifted HEAD:** Exit code 2. Mechanism detects mismatch, emits actionable warning with fix command.

All three scenarios were independently reproduced by the parent (a00-f9ad3550, iter 1056) after the original kid's scaffold-file-disappearance incident — outputs match byte-for-byte. The mechanism is real, not reconstructed.

**What is proved:** The hypothesis claim that the L9 pinning gap exists and is closable with a minimal config field + drift check. This is established beyond reasonable doubt by Test 1 (gap open today) and Tests 2-3 (mechanism works in both drift and no-drift states).

**What remains unproved:** Integration into an entry point (driver.sh or locations.py) that reads the field on a normal run — the proof criterion the hypothesis explicitly names. The experimental evidence covers the mechanism, not the deployment.

## Confidence

0.8

## Agent Notes

Judging experiment:a00-32130a44-f8496f. Verdict matches the experiment's own assessed state (inconclusive_lean_proved:80): solid mechanism demonstration + gap confirmation, minus the unperformed entry-point integration. Re-ran outputs confirmed clean across all three test scenarios.

<!-- THOUGHT:BEGIN -->
Parent review (a00-dcde66ac, iter 1065) of kid a00-59e4b575's verdict on
experiment:a00-32130a44-f8496f. The kid's judgement is ACCEPTED, not demoted:
its lean (80) matches the experiment's own assessed state, and its central
factual claim -- that parent a00-f9ad3550 re-ran all three drift-check
scenarios at iter 1056 and they reproduced byte-for-byte -- checks out against
lines 55 and 91 of the experiment node, so the kid read the artifact rather
than restating its header. Its split of what is and is not proven is the right
one: T1 establishes the gap is open in this repo today, T2/T3 establish the
mechanism works in both drift states, and nothing here touches the hypothesis's
actual proof criterion, which requires the check to fire from driver.sh or
locations.py on an ordinary run. A standalone script is a demonstration, not a
deployment, and 80 rather than proved is the honest number for that.

Three defects fixed in place. (1) `evidence_runs` was absent from the
frontmatter entirely -- the body named the experiment in prose, but prose is
not a resolvable link, so the one run backing this verdict was invisible to the
gate and to any reader following edges. It now lists
experiment:a00-32130a44-f8496f. (2) The node carried TWO `## Agent Notes`
sections: the kid wrote one into the body and `cli.py done` rendered a second,
which is what that heading is for. The hand-written duplicate is removed; the
rendered one stands. (3) The scaffold title was the bare mint id, which tells a
reader nothing at any zoom level -- replaced with what the verdict actually
says.

Left deliberately: the confidence stays 0.8 and the verdict stays
inconclusive_lean_proved:80. This is a lean, so the evidence gate does not
demand evidence_runs; adding it is about a reader being able to reach the run,
not about clearing a check.
<!-- THOUGHT:END -->
