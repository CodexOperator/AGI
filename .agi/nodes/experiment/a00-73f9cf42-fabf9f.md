---
id: experiment:a00-73f9cf42-fabf9f
mint_id: 5da7ac8911234c388a69e2a49aca86b5
type: experiment
parents:
  - hypothesis:a-spawned-round-never-inherits-a-model-slot-lock-override
next_edges: []
confidence: 0.9
edited_by: a00-73f9cf42
evidence_runs:
  - experiment:a00-73f9cf42-fabf9f
loop: hypothesis:a-spawned-round-never-inherits-a-model-slot-lock-override@s2
model: stealth/space-bunny-alpha
production_lines: 7
profile: balanced
role: kid
scaffold_hash: d73139c288df17a3
season: 2
title: Scrubbing AGI_MODEL_SLOT_LOCK so no spawned round steps outside the box-wide model slot
town: core
verdict: proved
---
# experiment:a00-73f9cf42-fabf9f

## What I did
Pre-fix probe of falsifier 1, then the one-line scrub, then the test on the built bytes.

```
$ AGI_MODEL_SLOT_LOCK=/tmp/probe.lock python3 -c "import dispatch; print('AGI_MODEL_SLOT_LOCK' in dispatch.scrubbed_env())"
pre-fix:  True /tmp/probe.lock          <- falsifier 1 HOLDS: the key was inherited
post-fix: False                        <- after the change below
```

## The change (production: 1 name + 6 comment lines in dispatch.py)
`"AGI_MODEL_SLOT_LOCK"` added to `ENV_VARS_TO_SCRUB` (dispatch.py), with the
reason in the comment. One declaration -- config-max/template-max need nothing;
heal.py shares `scrubbed_env()`, so both spawners close at once.

## Test (new, not a production line)
`extensions/agi/tests/test_model_slot_lock_scrub.py`
- `test_a_spawned_round_inherits_no_model_slot_lock_override` -- the key is gone
  from the child env, its value leaks nowhere into the env JSON, and a sibling
  key (`AGI_ROUNDS`) still survives (the scrub is narrow).
- `test_no_injection_means_the_production_cell_still` -- falsifier 2: with nothing
  injected, `lock_path()` is byte the configured production cell.

```
$ python3 -m pytest extensions/agi/tests/test_model_slot_lock_scrub.py extensions/agi/tests/test_provisioning.py -q
91 passed, 5 skipped
$ python3 -m pytest extensions/agi/tests/test_heal.py -q
(with test_dispatch_forward_env.py: 26 passed, 1 failed -- pre-existing, asserts a
 leaked TYPESAFE_KEY in THIS shell's environ, never touches the scrub list)
```

## Result
Both falsifiers closed. `--lock` unchanged: it is argv-visible, and
model_slot.py's own resolution order is untouched.

## Agent Notes
Pre-fix probe showed scrubbed_env() leaked AGI_MODEL_SLOT_LOCK; added the name to ENV_VARS_TO_SCRUB (7 production lines) and a new test closes both falsifiers; 91 passed on the new+provisioning neighbourhood.
