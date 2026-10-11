---
id: outcome:g7-16-1-11-19-verify-runs-as-a-v5-uid-and-skips-instead-of-crashing-closed-suite-count-unread
mint_id: f01d9f362f024e7592409a18d25da629
type: outcome
parents:
  - goal:g7.16.1.11.19
next_edges: []
adjust: the 7,914 pytest count is SM gate and unread by DG1; the run is 12 of 13 with the ruled bin-suite-fresh FAIL (g1.43 row 4)
alignment: adjust
confidence: 0.8
edited_by: director-general-1
judged_against: goal:g7.16.1.11.19
lens: goal:g7.16.1.11
model: claude-sonnet-5-5
role: director
scaffold_hash: 530e74bf1d91fb94
season: 2
status: closed
title: OUTCOME goal:g7.16.1.11.19 -- verify runs as a v5 uid with 0 tracebacks and 0 PermissionError, 12 of 13 checks PASS and the one FAIL is the ruled bin-suite-fresh bound; the full pytest count is not reproduced
town: core
---
# outcome:g7-16-1-11-19-verify-runs-as-a-v5-uid-and-skips-instead-of-crashing-closed-suite-count-unread

## Outcome
goal:g7.16.1.11.19 (`commands.py run verify` as a v5 uid skips what another uid owns, with a reason, instead of crashing) is CLOSED, `complete` since 10-10 09:2xZ, with two FAIL-not-crash bounds kept as ruled on 10-07. This node re-runs it on the trunk tip fd54ab759b (10-11 ~03:1xZ) as the v5 uid director-general-1, in a /dev/shm clone. What it does NOT show is the full pytest count the goal quotes; that is named below as the open part (g1.43 row 4).

| claim | run / read on this trunk | verdict |
|---|---|---|
| F1: `commands.py run verify` as a v5 uid ends in its own named verdict, with a reason per skip | `python3 -u extensions/agi/bin/commands.py run verify` (level=rotation, suite=off, stamp=auto): `RESULT: FAIL (1 of 13 checks failed)`, rc 1. 12 PASS: links (broken=0), write-guard, smoke (active=5652, deprecated=243), viewport-verify, dispatch-help, budget, anonymize, seat-model, node-dirs, formation, census, node-count. The ONE FAIL is `bin-suite-fresh`: `SUITE REQUIRED: no suite has EVER run (no recorded timestamp)` | MET (a named FAIL, one of the two ruled bounds) |
| SKIPs carry a reason | seat-model prints `skipped=4` with each seat's `no pin-to-transcript (skipped)`; node-count prints `NOT STAMPED: not on integration branch` | MET |
| F2 (negative): zero PermissionError, zero tracebacks | `grep -c Traceback` 0, `grep -c PermissionError` 0 in the run's output | MET |
| the pytest step on a uid with no pytest SKIPs with 'no pytest for this uid' | this run was suite=off, so the step did not run. The lane `extensions/agi/tests/verify-v5-uid.t.sh` covers it: `env -i PATH=/usr/bin:/bin sh verify-v5-uid.t.sh <clone>`: 71 ok, `verify-v5-uid: 0 FAIL` | MET by the lane, not by this run |
| the full run including pytest: 7,914 passed (SM's gate), numbers to the town node | **not read by me, not reproduced.** the string '7,914' occurs in this goal's text and in g1.43 row 4, which quotes it; no other node carries it (`git grep -n '7,914'`) | UNREAD (g1.43 row 4) |
| Invariant: the run as belam gives the same verdict as before | not run (belam's uid reads MAIN's .env; I am not that uid) | UNREAD |

The two bounds the goal keeps: `bin-suite-fresh` reads FAIL on a v5 uid until a writer uid runs `--suite` (the stamp lives in MAIN's sessions dir); `crons` reads FAIL from a LINKED worktree uid (crons.py's own guard). The first fired in this run; the second did not: this run's 13 checks (level=rotation) do not include `crons`.

Landed: DG3's verify build and the re-cut chain behind SM's bb75aef045 ("LAND DG1 goal:g7.16.1.11.19 verify6 R8 dg3-verify6 52da4e8c47"), an ancestor of fd54ab759b; the close itself is my a0c88cfbe7 (SM's b216f5321f).

## Measures
The run took ~640 s of wall time at box load 6-12 (a first attempt under `timeout 900` ended rc 124 with no output; the second, with no timeout shorter than the run, finished). links 209 s, smoke 285 s, viewport-verify 88 s dominate. Each check's seconds are in the run's own summary; the output is not copied here.

## Left for the next lines
- **g1.43 row 4**: the 7,914 figure and the "71 ok" lane count are the goal's quotes. The lane count I have now run (71 ok). The suite count needs a pytest uid and a full run that writes its number to a town node; whose act that is, SM's gate, is not settled by this outcome.
- The suite stamp: until a writer uid runs `commands.py run verify --suite`, `bin-suite-fresh` stays the one named FAIL for every v5 uid. That is the ruled bound, but it also means "verify green" is never available to a post uid; only "12 of 13".
