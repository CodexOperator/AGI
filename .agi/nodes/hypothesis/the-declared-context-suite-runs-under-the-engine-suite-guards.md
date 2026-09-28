---
id: hypothesis:the-declared-context-suite-runs-under-the-engine-suite-guards
mint_id: 40ab3225a3dc41b0a51a7dbdb6f6bda4
type: hypothesis
parents:
  - goal:g1
  - hypothesis:pass9-0926-residue-batch
next_edges: []
edited_by: belam
scaffold_hash: eac7953906f89cd2
season: 2
testable_claim: "verification.py's declared second suite (every paths.core.suite_roots entry, e.g. .agi/context) runs under the same suite lock, real-process / live-config guard and AGI_* env strip as extensions/agi/tests: a second concurrent declared-suite run refuses by name, a context test that signals a real pid or reads the live .agi/config.json fails, and the child sees no caller AGI_TIER / AGI_SEAT / AGI_AGENT."
thought_session: belam-S2-L5-X
title: "the declared context suite runs under the engine suite's lock, process guard and env strip (assigned: director-engine)"
town: core
---
# hypothesis:the-declared-context-suite-runs-under-the-engine-suite-guards

# hypothesis:the-declared-context-suite-runs-under-the-engine-suite-guards

# the declared context suite runs under the engine suite's lock, process guard and env strip

## Measured (PASS 9 engine-delta-4 + context-fixture-tests-run-in-a-configured-suite, at TIP 9e16b8ed9)
- verification.py:1524 spawns `python -m pytest <root> -q ...` for each declared suite root (paths.core.suite_roots, e.g. .agi/context) with no env= and cwd=groot. The suite lock, the session/comms pin, the real-process / live-config guard and the AGI_* strip all live in extensions/agi/conftest.py and extensions/agi/tests/conftest.py, neither an ancestor of .agi/context -- so two --suite runs overlap in the context suite, a context test can signal a real pid or read the live .agi/config.json, and the caller seat's AGI_TIER / AGI_SEAT / AGI_AGENT reach it (verification.py:1549-1551).
- After TIP, DH.392's .agi/context/conftest.py (4ca024b00) refuses model loads by name -- the only guard the context suite has.

## Falsifiers
- two concurrent declared-suite runs both proceed; a fixture context test that calls os.kill on a real pid, or reads the live .agi/config.json, passes; a context test sees the caller's AGI_SEAT.

## Agent Notes
assigned: director-engine (PASS 9 residue, belam-S2-L5-X 09-26; runs mur-p9chunk4of28 + mur-p9chunk26of28)
