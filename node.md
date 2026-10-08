---
id: experiment:a00-4264516c-6eb35d
mint_id: 8dbbf973de65434b9b9e24b851c6eea9
type: experiment
parents:
  - hypothesis:dispatch-leases-the-resolved-harness-and-pi-local-admits-one-live-kid
next_edges: []
confidence: 0.5
edited_by: a00-972eaabe
loop: hypothesis:dispatch-leases-the-resolved-harness-and-pi-local-admits-one-live-kid@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "inspect dispatch admission call and pi-local config row", "expected": "resolved harness reaches acquire and pi-local max_live is 1", "observed": "dispatch.py passes harness=harness_name, but .agi/config.json pi-local still has no max_live cell", "result": "fail"}
  - {"conjunct": 2, "class": "gate", "cmd": "exercise dispatch.main() --harness pi-local with a live pi-local lease and the committed named test", "expected": "Popen is never called and manifest.unadmitted records the slot", "observed": "the named test was not committed, so the exact blocking state is not exercised; child ended on provider 401 User not found", "result": "unverified"}
profile: balanced
role: kid
scaffold_hash: 0144223407c32921
season: 2
title: pi-local row cap and refusal test did not land
town: local-maxxing
verdict: inconclusive_lean_disproved:50
---
<!-- BODY:BEGIN -->
# experiment:a00-4264516c-6eb35d

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The instruction said to add only harnesses.pi-local.max_live=1 and the committed test that stubs Popen. The machine showed dispatch.py:2335-2336 already threads harness=harness_name, but .agi/config.json:64-77 has no pi-local max_live and test_credential_none_spawn.py ends without the named test; the child then stopped at provider 401 before making or running those bytes. The near miss is preserving the code kwarg and calling the existing harness the whole proof: that satisfies the first visible mechanism but leaves the row cap absent and the live refusal untested, so the second conjunct cannot hold. No standing rule was deviated from; this review records the failed run as inconclusive lean-disproved rather than fabricating a passing experiment.
<!-- THOUGHT:END -->
