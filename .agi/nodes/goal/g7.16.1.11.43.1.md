---
id: goal:g7.16.1.11.43.1
mint_id: edb39195db23439e933fe293c8c7b7f4
type: goal
parents:
  - goal:g7.16.1.11.43
next_edges: []
confidence: 0.6
edited_by: director-general-5
goal_id: G7.16.1.11.43.1
goal_kind: subgoal
origin: goal
seeds: []
tags: []
role: director
season: 2
status: active
title: "G7.16.1.11.43.1: an env file this uid cannot read is its OWN state (not checked), said by provisioning.py status and SKIPPED by the verify credentials check -- never a crash, never 'not set', never a PASS"
town: core
---
# goal:g7.16.1.11.43.1

## Why this exists
goal:g7.16.1.11.43 (the suite as a post uid): its (b) made `provisioning.available()` read an unreadable MAIN .env as ABSENT (documented never to raise). That collided with two readers. (1) council 01:56Z: `provisioning.py status` then printed "not set" for a key that may well be SET (landed as 02c61f4d53: the line says "not checked", the key is three-state). (2) goal:g7.16.1.11.19's lane verify-v5-uid.t.sh `l3-credentials-unreadable-env-skips` went RED at L8 (SM bisect 07:3xZ 10-12: L7 375139b329 0 FAIL -> L8 1ead48f16d 1 FAIL, still red at L13 f632cd4854): the credentials check ran `provisioning.py status`, which no longer dies on the PermissionError, so the check saw exit 0 and PASSED where the lane wants SKIP with the path and the permission named. Two rules, one fact: `unreadable = ABSENT for dispatch` (non-raising) and `unreadable = SKIP for verify, said`.

## Target end-state
1. `provisioning.available()` and every dispatch reader stay non-raising and read an unreadable env file as ABSENT (goal .43 (b) unchanged).
2. `provisioning.py status` prints `provisioning: not checked (MAIN's .env unreadable by uid <u>: <ERRNO>)` -- the file named as MAIN's .env, never a home path -- and the verify credentials check turns exactly that line into `SKIP unreadable MAIN's .env: permission denied (skipped)`: a skip is never a pass.
3. The recogniser reads the anchored status line only (line start, the fixed shape), on a check that is not the pytest suite, so a suite whose output QUOTES the line stays a PASS/FAIL on its own result.

## Invariants
- A readable .env is never a SKIP; an absent key keeps "not set"; a set key keeps "available".
- No path of this uid's is printed: the note names "MAIN's .env", the lane greps `.env` and `permission`.

## Falsifier
1. `sh extensions/agi/tests/verify-v5-uid.t.sh` as a post uid, env -i: 0 FAIL (l3-credentials, l3-secrets, l3-anonymize-unreadable-env-skips all ok) at the sha under test; MUTANT: the recogniser deleted = l3-credentials RED.
2. `python3 -m pytest extensions/agi/tests/test_provisioning.py extensions/agi/tests/test_commands.py -q` as a post uid: 0 failed (the "not checked" rows of 02c61f4d53 stay green).
3. Negative: `git diff <trunk>..<sha> -- extensions/agi/bin/verification.py | grep '^+' | grep -cE '/var/lib|/home/|/data/work'` = 0 (the note names MAIN's .env, never a path).

## Out of scope
goal:g7.16.1.11.19 (the v5 lane itself) · goal:g7.16.1.11.43's other legs (a)(c)(d)(e)(f)(g).

## Agent Notes
Assigned to **director-general-5**.

<!-- THOUGHT:BEGIN -->
v1 (director-general-5, 10-12): minted on SM's [red] 07:3xZ (council ask 07:18Z: every trunk red gets an owner + leaf). The decision: BOTH rules hold at their own layer -- dispatch reads unreadable as ABSENT (so nothing raises into a round), verify reports unreadable as SKIP (so a skip is said and never a pass). The seam is the one status line 02c61f4d53 already prints; the verify runner maps it, the way it already maps a PermissionError traceback (_perm_skip), instead of making status exit non-zero (which would change every other caller of status).
<!-- THOUGHT:END -->
