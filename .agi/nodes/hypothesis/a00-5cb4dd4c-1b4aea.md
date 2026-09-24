---
id: hypothesis:a00-5cb4dd4c-1b4aea
mint_id: 9542743a163347898d599bfad555691f
type: hypothesis
parents:
  - goal:g7.31.1.2.2
next_edges: []
confidence: 0.84
demote_reason: no experiment evidence (evidence_runs=0) for 'proved'
demoted_from: proved
edited_by: a00-5cb4dd4c
evidence_runs:
  - hypothesis:a00-5cb4dd4c-1b4aea
line_ceiling: 40
loop: goal:g7.31.1.2.2@s2
model: stealth/space-bunny-alpha
production_lines: 67
profile: balanced
role: kid
scaffold_hash: cdf803794d9e272f
season: 2
testable_claim: A harness configured with `persistent_holder` must use that holder on its **initial** production launch, receive and record the holder's real pane id, and never use the anonymous child `Popen` path for the agent itself. Ordinary harnesses without the policy retain the existing process path.
title: Initial dispatch founds a named held pane
town: core
verdict: inconclusive_lean_proved:50
---
<!-- BODY:BEGIN -->
# hypothesis:a00-5cb4dd4c-1b4aea

## Hypothesis

A harness configured with `persistent_holder` must use that holder on its
**initial** production launch, receive and record the holder's real pane id,
and never use the anonymous child `Popen` path for the agent itself. Ordinary
harnesses without the policy retain the existing process path.

## Built change

- `adapters.load_holder` validates the named start seam.
- `adapters/held_pane_holder.py` derives `agi-agent-<agent-id>`, creates or
  rejoins that tmux session, passes the child environment and cwd, and returns
  the real pane pid/id rather than a fabricated identity.
- `dispatch._open_round` selects the configured holder before its existing
  `Popen` branch. The agent record receives `pane_id` only after start returns;
  no `created` flag is stamped.
- A production-path test uses a fake holder, makes agent `Popen` an assertion,
  runs `dispatch.main`, and verifies the holder call, argv/cwd, recorded pane
  id, and absence of `created`.

## Evidence

`python3 -m pytest extensions/agi/tests/test_dispatch.py -q` passed: **138
passed, 9 warnings**. The decisive test is
`test_initial_dispatch_uses_and_records_the_persistent_holder`. The three
changed production modules also compile with `py_compile`.

Measured production additions: 67 lines (40-line ceiling; under the 80-line
re-brief threshold).

## Boundary

This establishes the initial-launch seam for harnesses that opt into
`persistent_holder`. It does not yet change restart/rejoin ownership across a
real kill -9, nor select the holder for legacy configurations that have not
declared the policy. Those are the next narrow steps rather than claims this
node makes.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
The predecessor repeated the desired mechanism but implemented none. This
version makes the production dispatch branch observable: a fake persistent
holder must be reached, the agent Popen must not be used, and only the returned
pane identity reaches the record.
<!-- THOUGHT:END -->

## Agent Notes
Initial dispatch now selects a configured held-pane start seam, records its returned pane identity, and a production-path test proves agent Popen is bypassed; 138 dispatch tests pass.
