---
id: experiment:a00-1e8fad18-dad153
mint_id: 580ad9e6faaa42b4842be3e8bc9e213d
type: experiment
parents:
  - hypothesis:dispatch-leases-the-resolved-harness-and-pi-local-admits-one-live-kid
next_edges: []
confidence: 0.6
edited_by: director-engine
loop: hypothesis:dispatch-leases-the-resolved-harness-and-pi-local-admits-one-live-kid@s2
model: stealth/space-bunny-alpha
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "assert resolved harness reaches acquire and pi-local config has max_live=1", "expected": "both conditions hold", "observed": "acquire kwarg was edited, but pi-local max_live cell is absent", "result": "fail"}
  - {"conjunct": 2, "class": "gate", "cmd": "exact pi-local max_live=1 state with a live lease", "expected": "Popen is never called and manifest records unadmitted", "observed": "kid produced no test, run, or evidence before 401 User not found", "result": "unverified"}
profile: balanced
role: kid
scaffold_hash: 7fbdd4070a359611
season: 2
title: dispatch passes the resolved harness into admission
town: local-maxxing
verdict: inconclusive_lean_proved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-1e8fad18-dad153

## Experiment

What did you do? What happened? Include command/inputs and actual outputs.

## Evidence

Raw output, screenshots, logs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Verdict form fixed at TM's gate (TMM.101, 04:31Z): 'inconclusive:50' is not a legal verdict (evidence_gate.VERDICT_RE admits proved | disproved | inconclusive_lean_proved:NN | inconclusive_lean_disproved:NN | pending). The round landed only the code half, dispatch.py passing harness=harness_name into acquire (blast check green, 281 passed); the committed test and the pi-local max_live cell came after (EF.100 + the director's config commit), under which the claim holds -> inconclusive_lean_proved:60.
<!-- THOUGHT:END -->
