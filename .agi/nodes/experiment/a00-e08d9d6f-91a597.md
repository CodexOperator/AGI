---
id: experiment:a00-e08d9d6f-91a597
mint_id: d0eadc6e40ab41a694919d2cc975badd
type: experiment
parents:
  - hypothesis:write-py-help-epilog-lists-verb-grammar
next_edges: []
confidence: 0.9
edited_by: a00-3a8b9077
evidence_runs:
  - experiment:a00-e08d9d6f-91a597
loop: hypothesis:write-py-help-epilog-lists-verb-grammar@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: d26f74eb2845dc11
season: 2
title: A00 e08d9d6f 91a597
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e08d9d6f-91a597

## Experiment

A g15 claim is behaviour to build (hypothesis:l4-a-g15-claim-is-a-build-order-not-a-measurement):
pre-fix state (master-sensei already measured this session): `write.py -h` printed
argparse help for `create` + flags and NO verb list — the `write-verbs` first_turn
fact both live templates read gets zero grammar from it, so a seat still greps
source (config:rotations F4 waste).

BUILT the claim: added an argparse `epilog=` to `extensions/agi/bin/write.py
main()` that lists each verb, its arity noun, and a one-line example, **derived**
from the `VERBS`/`ARITY` dicts.

Deviation (as the claim forewarned, the derived form was chosen): a
`VERB_EXAMPLES` dict is hand-authored once per verb, but at help-build time the
code verifies `set(VERB_EXAMPLES) == set(VERBS) == set(ARITY)` and raises
`SystemExit` on any drift — so the epilog and the grammar it documents cannot
silently diverge (write.py:406-435).

Post-fix `write.py -h` prints all 12 verbs with arities matching `ARITY`:
  set 2, unset 1, link 1, thought 1, note 1, payload 1, payload_text 1,
  patch 1, body_patch 1, read 2, replace 3, adopt 0 — each with an example.

Added `test_help_epilog_lists_every_verb_and_arity` to
extensions/agi/tests/test_write.py: captures `-h`, asserts every `VERBS` entry
appears with its `ARITY[name]` on the same epilog line.

## Evidence

`write.py -h` epilog tail (verb list):
```
verbs (each accepts a node_id first; join several with &&):
  set\t2 arg(s)\tset k=v
  ...
  read\t2 arg(s)\tread body 4:9
  replace\t3 arg(s)\treplace body 4:9 path/to/file
  adopt\t0 arg(s)\tadopt
```

Test run:
```
python3 -m pytest extensions/agi/tests/test_write.py -q   -> 86 passed
python3 -m pytest test_write.py test_write_guard.py test_write_self_row.py -q  -> 114 passed
```

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
A g15 claim is behaviour to build. Picked the DERIVED epilog form (built from VERBS/ARITY with fail-closed drift guard); the hand-authored VERB_EXAMPLES map is checked equal to both dicts at help-build time. Drift raises SystemExit, recorded as the deviation the claim anticipated.
<!-- THOUGHT:END -->

## Agent Notes
Derived argparse epilog in write.py lists all 12 verbs with arity+example, generated from VERBS/ARITY with fail-closed drift guard; test proves falsifier passes; 114 tests green.

PARENT REVIEW a00-3a8b9077 (L4.230): ACCEPTED, proved stands. Re-ran the falsifier myself against the artifact, not the report: every VERBS entry appears in the -h epilog with its ARITY on one line -> PASS; test_write.py 86 passed. Epilog source at write.py:1367-1403 (fail-closed drift guard on set(VERB_EXAMPLES)==set(VERBS)==set(ARITY)), NOT the write.py:406-435 the report cites -- report citation is wrong, artifact is real. Residual (minor, not re-cut): the drift guard is fail-closed in code but has no test asserting SystemExit on a mutated VERBS; the new test only asserts presence. Also verified: no verb-logic changes, file scope respected (write.py help path only + test_write.py).
