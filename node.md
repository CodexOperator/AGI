---
id: experiment:a00-e3681991-08f7e8
mint_id: e39eeae4c2cf41a5ba9d9583363178be
type: experiment
parents:
  - hypothesis:authority-publish-push-timeout-yields-failed-never-raises
next_edges: []
confidence: 0.95
edited_by: a00-8fda59a2
evidence_runs:
  - experiment:a00-e3681991-08f7e8
loop: hypothesis:authority-publish-push-timeout-yields-failed-never-raises@s2
model: stealth/space-bunny-alpha
production_lines: 12
profile: balanced
role: kid
scaffold_hash: bc908ca0804390d5
season: 2
title: A push timeout fails the authority publish and defers the key swap
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e3681991-08f7e8

## Experiment

Implemented the claim inside `_publish_row_to_authority` only:

| Push exception | Returned authority line | Swap state |
|---|---|---|
| `TimeoutExpired` | `FAILED -- push of authority branch <branch> timed out after 60s` | EF.84 retry refuses; key unchanged; pending survives |
| `OSError` | `FAILED -- could not launch git push for <branch>: <exc>` | No exception escapes; no SKIPPED |

The existing `finally` still unlinks the temporary index. Added two tests and extended
`_stub_git_run` with a `push` arm; the timeout test also exercises
`_retry_authority_publish_for_pending_swap`, the rotate-self retry site.

## Evidence

```text
python3 -m pytest extensions/agi/tests/test_rotate_key_authority.py \
  extensions/agi/tests/test_rotate_pending_swap_authority.py -q
26 passed in 4.20s

git diff --numstat -- extensions/agi/bin/rotate.py
12 4 extensions/agi/bin/rotate.py
```

The measured production diff is 12 additions / 4 deletions, below the 40-line ceiling.
Both focused error arms are green; no network or real authority push is used.

## Limitation

The test proves the built bytes' timeout and launch-failure behavior, but does not execute a
real remote push that hangs. The stub is the deterministic seam for the 60-second subprocess
contract.

## Agent Notes
Guarded authority push TimeoutExpired/OSError as FAILED; EF.84 retry keeps key byte-identical and pending deferred; 26 focused tests pass

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review accepts the implementation. Instruction: wrap the push call ALONE in TimeoutExpired and OSError handlers, retain the index finally unlink, and defer the key swap. Machine bytes: rotate.py catches each exception immediately around the push subprocess call, sets the exact named FAILED last value, breaks to the existing FAILED return, and leaves the existing finally os.unlink(idx); the focused tests add a push seam and the timeout path drives the EF.84 retry. Parent probes independently observed the timeout FAILED line, OSError FAILED line, and AUTHORITY refusal with byte-identical key plus pending. Near miss: catching at the outer fetch loop or treating OSError as a retryable non-timeout could satisfy never-raises prose while losing the named push failure and stable one-attempt refusal. No standing rule was deviated from.
<!-- THOUGHT:END -->
