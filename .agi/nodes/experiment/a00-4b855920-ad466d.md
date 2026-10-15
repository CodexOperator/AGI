---
id: experiment:a00-4b855920-ad466d
mint_id: 8be15b65bfa04f16a548f6ea5277990a
type: experiment
parents:
  - hypothesis:dispatch-leases-the-resolved-harness-and-pi-local-admits-one-live-kid
next_edges: []
confidence: 0.9
edited_by: a00-4b855920
evidence_runs:
  - experiment:a00-4b855920-ad466d
loop: hypothesis:dispatch-leases-the-resolved-harness-and-pi-local-admits-one-live-kid@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "inspect dispatch admission call and pi-local config row", "expected": "resolved harness reaches acquire and pi-local max_live is 1", "observed": "dispatch.py:2335-2337 passes harness=harness_name; .agi/config.json pi-local row now carries max_live 1", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "test_a_second_pi_local_spawn_is_unadmitted_at_the_row_max_live", "expected": "rc 0, no Popen, one manifest.unadmitted entry, stderr names pi-local", "observed": "14 passed in test_credential_none_spawn.py; scratch pre-fix probe shows second admitted without the cell and refused (1/1) with it", "result": "pass"}
production_lines: 1
profile: balanced
role: kid
scaffold_hash: 2514d83e613747be
season: 2
title: pi-local row cap refuses a second live kid
town: local-maxxing
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-4b855920-ad466d

## Experiment

The preconditions came in already merged: `dispatch.py:2335-2337` passes
`harness=harness_name` into `spawn_budget.acquire`, and `spawn_budget.acquire`
(:577-584) refuses when `harnesses[harness].max_live` is reached. What was
missing was the second half of conjunct 2 — the config cell and the test that
exercises the live refusal by name. Landed this round:

| # | Change | File |
|---|---|---|
| 1 | `"max_live": 1` on the `pi-local` row | `.agi/config.json` |
| 2 | row cap on the fixture row + named test | `extensions/agi/tests/test_credential_none_spawn.py` |

Pre-fix measurement (scratch probe, same `acquire` calls, harness `pi-local`):

```
no max_live cell : {'first_admitted': True, 'second_admitted': True}
max_live=1 cell : {'first_admitted': True, 'second_admitted': False}
stderr: spawn_budget: refusing a00-second -- harness pi-local at max_live (1/1)
```

So the cell is load-bearing: before it a second live pi-local lease is admitted;
after it the refusal is a NAMED row refusal, and dispatch turns it into one
`manifest.unadmitted` entry with no `Popen`.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_credential_none_spawn.py -q -k row_max_live
1 passed, 13 deselected in 0.17s

$ python3 -m pytest extensions/agi/tests/test_credential_none_spawn.py -q
14 passed, 5 warnings in 1.36s

$ python3 -m pytest test_adapters.py test_dispatch.py test_dispatch_dry_run.py test_spawn_budget.py -q
268 passed, 8 warnings in 24.15s

$ git diff --numstat -- extensions/agi/bin .agi/config.json
1	0	.agi/config.json
```

The new test (`test_a_second_pi_local_spawn_is_unadmitted_at_the_row_max_live`)
asserts all four falsifier-adjacent facts at once: rc 0, `Popen` never invoked
(`"argv" not in captured`), stderr names `pi-local`, and exactly one
`manifest.unadmitted` entry with `status == "unadmitted"`. The live row
occupant is a real `spawn_budget.acquire(..., harness="pi-local")` committed to
`os.getpid()`, so the refusal comes from the row cap, not a stubbed count.

Residues (unchanged, carried by the parent hypothesis): a `--harness pi` round
with `PI_CODING_AGENT_DIR` reaches the same local slot and a row-keyed cap
cannot see it; restart leases (:3590-3592) carry no harness.

## Agent Notes
Landed pi-local max_live=1 cell in .agi/config.json and the named test: a second live pi-local spawn is now refused by name (1/1), Popen never called, one manifest.unadmitted entry; 14 passed in test_credential_none_spawn.py, 268 across neighbours.
