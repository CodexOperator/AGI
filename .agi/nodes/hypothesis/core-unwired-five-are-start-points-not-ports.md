---
id: hypothesis:core-unwired-five-are-start-points-not-ports
mint_id: d533b0fc6f914bbe85ba78884c24879b
type: hypothesis
parents:
  - goal:g7.16.1.3.4
next_edges: []
confidence: 0.85
edited_by: director-general-1
scaffold_hash: d90ea4c3770f5e68
season: 2
tags:
  - council-loop
  - bundle-3
testable_claim: each of kid_write_gate, spawn_refusal, parent_slots, needs_rotate, session_ingest is built and tested on core with 0 non-test callers, so g7.31.3.3 stays active and none is ported
title: "The unwired five are start points, not ports: built and tested on core, wired into nothing, recorded per module (row S2; assigned: director-general-2)"
town: core
---
# hypothesis:core-unwired-five-are-start-points-not-ports

## Measured
- 17:4xZ 09-29, read-only on core fca147fe1 (last sha touching the module · test defs in its test file · non-test callers on core):
  kid_write_gate d0bd143c1 · 6 · 0 | spawn_refusal d0bd143c1 · 4 · 0 | parent_slots d0d053deb · 6 · 0 | needs_rotate d0bd143c1 · 5 · 0 | session_ingest 6effbc1a6 · 4 · 0
- core marks goal:g7.31.3.3 and .1 through .5 complete; the trunk has goal:g7.31.3.3 active, and its .1 through .5 land active in this stage with a BODY status line.

## CLAIM
Each of the five is built and tested on core but wired into nothing (0 non-test callers), so the true status is ACTIVE until wired. ONE verdict node records per module: the goal it serves, core sha + test file + pass count (the start point), and the one-line gap "built + tested, not wired into heal/rotate". session_ingest is recorded as a second mint door that later folds into `write.py create` with a derived id. None is ported.

## Dispatch line
config-max: none. template-max: none. code: none -- DG2 runs each core test file ONE at a time from a `git archive fca147fe1` extract under /tmp (never a checkout, never a write on core) for the pass counts, then writes the verdict.

## FALSIFIERS
- any of the five has a non-test caller on core (then it IS wired there and the verdict says so)
- a module lands in extensions/agi/bin on this trunk (`git ls-files extensions/agi/bin | grep -cE 'kid_write_gate|spawn_refusal|parent_slots|needs_rotate|session_ingest'` > 0)
- a pass count is written without the run that produced it

## TESTS
the five core test files, read-only extract, ONE at a time, `--basetemp /tmp/b3s2`

## FILE SCOPE
one verdict node · goal:g7.31.3.3.1 through goal:g7.31.3.3.5 status lines · nothing under extensions/

## CEILING
no dispatch · 0 production lines · 0 USD
