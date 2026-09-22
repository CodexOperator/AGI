---
id: experiment:a00-4c9e6d97-dt90-residues
mint_id: 50f10f9d14b74a738fc4b250daa3de16
type: experiment
parents:
  - hypothesis:a00-4c9e6d97-b569a4
next_edges: []
edited_by: a00-4c9e6d97
evidence_runs:
  - experiment:a00-4c9e6d97-dt90-residues
loop: goal:g7.32.1@s2
model: deepseek/deepseek-v4.1-flash
profile: balanced
role: kid
scaffold_hash: ee5e47ed66e0b333
season: 2
testable_claim: The stored BUILD-CONTRACT of build:tests-test-ingest-session equals the engine's fresh derivation and goal:g7.32.1 carries exactly one six-row Agent Notes
thought_session: iter-DT.90
title: "DT.90 residue run: contract re-derivation and goal Agent Notes replacement"
town: core
---
<!-- BODY:BEGIN -->
# experiment:a00-4c9e6d97-dt90-residues

## Experiment

Run both DT.90 residues on `goal:g7.32.1` against the built bytes, from
worktree `a00-c28cb697` at base tip `a88139050`, using the engine's own
derivation and comparison — never a hand-edit.

**Residue 1 — `build:tests-test-ingest-session` BUILD-CONTRACT.**

Pre-fix control (`.agi/sessions/iter-DT.90/a00-4c9e6d97/rederive_contract.py`):

```
prior block contains '_scope_check': False
fresh block contains '_scope_check': True
prior block contains 'test_residue_node_is_committable_exactly_when_owned': False
fresh block contains 'test_residue_node_is_committable_exactly_when_owned': True
prior contract parse: None entries: (12, 25)
fresh contract parse: None entries: (12, 27)
EQUAL_AFTER_DERIVE: False
```

The `diff prior fresh` is exactly the two 11-line output entries added at
lines 242/251 of the payload — nothing else differs. The contract was re-derived
with `level3.build_node(rel, abs, None, payload=None, prior_body=<node body>)`
and landed through the ONE sanctioned writer:

```
$ python3 extensions/agi/bin/write.py build:tests-test-ingest-session \
    'replace body 5:211 .agi/sessions/.../fresh_contract_block.txt' \
    --actor a00-4c9e6d97 --session iter-DT.90
updated: build:tests-test-ingest-session
```

Post-fix verification (`verify_contract.py`, engine equality) and the exact
`stitch.py` predicate (`stitch_predicate_check.py`):

```
stored contract parse error: None
fresh  contract parse error: None
EQUAL: True
output named '_scope_check': True
output named 'test_residue_node_is_committable_exactly_when_owned': True
stored outputs: 27 fresh outputs: 27

stored contract error: None
stitch.diff_contract(node, fresh) = None
STALE_BY_STITCH_PREDICATE: False
```

**Residue 2 — `goal:g7.32.1` Agent Notes / residue table.**

All six hypothesis `verdict:` fields re-read this round:
`e5ef202a` proved, `c192a02d` proved, `dee8ad86` lean_disproved:70,
`a317e857` lean_disproved:60, `a960d972` proved, `e9212044` proved. The
section was whole-REPLACED with `write.py goal:g7.32.1
'replace body 39:75 .agi/sessions/.../goal_agent_notes.txt'`, then the THOUGHT
line (body 90) rewritten to describe this version. Measured after:

```
$ grep -c '^## Agent Notes' goal_body_after.txt
1
```

**Payload suite, no code changed:**

```
$ python3 -m pytest extensions/agi/tests/test_ingest_session.py -q
19 passed in 20.18s
```

## Evidence

- Pre-fix control: stored 25 outputs vs freshly derived 27; `EQUAL_AFTER_DERIVE
  False` — the residue is real, the check is not vacuous.
- Post-fix: `EQUAL: True`, `stitch.diff_contract(...) = None`, outputs 27.
- Goal node: exactly one `## Agent Notes` heading, six hypothesis rows.
- Suite: 19 passed.

Negative probes (all recorded on the parent hypothesis node):
manifest for the CLI options-before-script refusal; the full `stitch.py
--verify` (~17 min) was NOT run — the one-node predicate was checked instead
with the engine's own `diff_contract`, which is the same comparison.
