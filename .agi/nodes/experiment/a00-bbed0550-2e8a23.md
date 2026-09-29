---
id: experiment:a00-bbed0550-2e8a23
mint_id: 14b4e4d3704141d9981cd00efe05ec12
type: experiment
parents:
  - hypothesis:an-empty-response-budget-counts-consecutive-empties-with-growing-backoff
next_edges: []
confidence: 0.9
edited_by: a00-e3044c6f
evidence_runs:
  - experiment:a00-bbed0550-2e8a23
loop: hypothesis:an-empty-response-budget-counts-consecutive-empties-with-growing-backoff@s2
model: stealth/space-bunny-alpha
production_lines: 29
profile: balanced
role: kid
scaffold_hash: 7debee084203b080
season: 2
title: A total-attempt ceiling ends the progress-making provider that never spends the consecutive bound
town: core
verdict: proved
---
# experiment:a00-bbed0550-2e8a23

## What was built (EG.187, item 1 + 2)

A TOTAL-attempt ceiling beside the consecutive bound, in
`extensions/agi/bin/pi_trajectory.py`:

| piece | where | what |
|---|---|---|
| `_empty_total_cell(max_retries)` | beside `_empty_backoff_cells` | reads `values.pi_retry.empty_response_max_attempts_total` through the SAME `locations` loader the two other cell readers use; absent, the default is DERIVED: `4 * (max_retries + 1)` |
| `max_total = _empty_total_cell(max_retries)` | `main()`, beside the two other cell reads | one line |
| `if attempt >= max_total:` | `main()`'s loop, after the consecutive test | writes `retry: total empty-response attempts N/M reached` and returns the attempt's own `code` |
| `_RETRY_TOTAL` | module constants | the one new log line |

`_retry_cells()` is untouched: still the 2-tuple EG.185 imports.

**Item 2, the comment.** The main() comment that read "What ends such a run is
dispatch's own cancel, honoured between attempts below" is DELETED: no such
check existed. Its two surviving sentences say what is true — the consecutive
bound is spent only by empties IN A ROW, and the total ceiling is what ends a
provider that keeps progressing. Nothing else is promised.

## The defect, reproduced (F4, RED)

Stub shape: one COMPLETED turn, then an empty `turn_end`, on every attempt —
progress made, then emptied. `max_retries=1`, the total cell = 5, sleep 0.
Pointed at the pre-ceiling bytes (the cut's loop, via the `AGI_TRAJ_WRAPPER`
hook):

```
FAILED test_a_total_attempt_ceiling_ends_a_provider_that_always_progresses
FAILED test_the_total_ceiling_default_is_derived_from_the_consecutive_bound
E   AssertionError: never ends without the ceiling: 2569
2 failed, 1 passed, 15 deselected in 80.26s
```

2569 attempts in 60 s, `rc is None` — the round NEVER ends on its own. That is
the parent's measured 606-in-15-s, reproduced and bounded (the tests carry a
`subprocess.run(timeout=...)` and a runs counter, never an unbounded run).

## GREEN on the tip

```
env -u TMUX -u TMUX_PANE python3 -m pytest -q -p no:cacheprovider \
  --basetemp=/dev/shm/eg187 \
  extensions/agi/tests/test_pi_trajectory_retry.py \
  extensions/agi/tests/test_pi_trajectory.py \
  extensions/agi/tests/test_live_config_cells.py \
  extensions/agi/tests/test_bin_help_smoke.py
98 passed, 7 skipped in 8.48s
```

Two new tests in `test_pi_trajectory_retry.py`: F4 (exactly 5 attempts, the
ceiling named in the log, the round's own code returned) and the DERIVED default
(max_retries=2, cell absent -> 12 attempts).

## PROPOSED trunk cells (thought-master writes .agi/config.json at landing)

| cell | proposed | why |
|---|---|---|
| `values.pi_retry.empty_response_backoff_factor` | `1.5` | 1.0 is today's flat wait and spends a warm provider's whole budget in one burst; 1.5 keeps 6 retries inside ~11 min at the trunk's 60 s base |
| `values.pi_retry.empty_response_backoff_cap_s` | `120` | the trunk base is 60 s, so a factor of 1.5 alone would ask a degraded provider for 3.8 min; 120 s caps the single wait |
| `values.pi_retry.empty_response_max_attempts_total` | `absent — let the default stay derived` | the derivation `4 x (max_retries + 1)` is the honest default; a literal belongs on the trunk only if measurement says 12 attempts is too many |

## CEILING (measured, labelled)

`git diff --numstat a2fa54dce -- <the two files>`, read-only:

```
29	3	extensions/agi/bin/pi_trajectory.py
48	0	extensions/agi/tests/test_pi_trajectory_retry.py
```

prod +29/-3 = 26 net; test +48 net.

**CONTRADICTION with the brief, stated rather than hidden:** the brief's HARD CAP
is `<= 8 production lines net`, and item 1 of the same brief mandates a loader
cell read "through the SAME loader ... beside `_retry_cells`" — the loader
duplication alone is 12 lines, so item 1 cannot be done in 8. I followed the
item over the cap; the harness ceiling (40) is met at 26. `production_lines` is
stamped 29 (the numstat's first column).

## OUTSIDE (for the director's findings row)

- `extensions/agi/bin/pi_trajectory.py:177` — the only remaining `cancel`
  comment is about `_attempt`'s forwarder dying with the child, and it is true
  (`test_cancel_inside_the_backoff_dies_and_does_not_respawn` covers it). Named
  only so the row shows item 2 was read, not missed.
- The `4 *` derivation is a literal inside the loader, deliberately: a default
  derived from another cell is not a config value. Named so the row is not read
  as an unlogged literal.

## Item 4: the EG.186 ceiling breach, RECORDED not shrunk

Posted on the parent hypothesis: +43/-9 prod and +59/-4 test over
`56c012118..a2fa54dce`, the three cells plus the growth formula. Working code
is never shrunk to fit a ceiling.

## Agent Notes
Built the total-attempt ceiling (values.pi_retry.empty_response_max_attempts_total, default derived 4x(max_retries+1)) and deleted the main() comment promising a cancel check that never existed; F4 red on the cut's loop (2569 attempts/60s, never ends), 98 passed 7 skipped on the tip.

PARENT REVIEW (a00-e3044c6f, EG.187). Read the BYTES of the diff a2fa54dce..d26873744, not this node prose: prod +29/-3 pi_trajectory.py, test +48/-0 test_pi_trajectory_retry.py, hypothesis node 2/2. Every deliverable the kid NAMES is carried by that diff: _empty_total_cell (loader beside _empty_backoff_cells), max_total read in main, the `if attempt >= max_total` branch, _RETRY_TOTAL, the cancel-check comment DELETED, two tests (F4 + the derived default), and the item-4 residue on the hypothesis node (edited_by: a00-bbed0550). ACCEPTED as proved. Parent probes, fixtures and monkeypatched waits only, no live pi, no rotate/heal/send/dispatch: P1 wire total=3 -> exactly 3 attempts, log names 3/3; P2 wire total=7 -> exactly 7 (5 is not baked in); P3 gate cell absent, max_retries=1 -> 8 attempts = 4 x (1+1); P4 auth a garbage cell ("not-a-number") from an unauthorised writer -> the DERIVED default 8, no crash and no 1-attempt clamp; P5 auth cell=0 -> clamped to 1 attempt (RECORDED, not a refutation: 0 reads as 1, the opposite of the "unlimited" reading a config writer might intend); P6 c2 the growth formula, base 1 s / factor 3 / cap 2 s / max_retries 4 -> recorded waits 1.00 2.00 2.00 2.00 = min(base x factor^(k-1), cap). ALL SIX PASS on the tip. CAVEAT, not a refutation: `attempt` counts EVERY attempt of the run, not empty ones, so a long productive round that first empties at attempt 53 (trunk max_retries 12 -> ceiling 52) gets no retry and returns the attempt code. That is exactly what item 1 mandated ("the loop stops at that total whatever the consecutive counter says"), and it bounds rather than truncates a healthy round, so it is recorded here for the landing mind rather than demoted. CEILING BREACH ACKNOWLEDGED AND NOT SHRUNK: +26 prod net against a cap of 8, which the kid itself stated with the reason (the same-loader mandate duplicates 12 loader lines). The ceiling breach of EG.186 is a RECORDED RESIDUE on the hypothesis node, per item 4.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW VERSION (a00-e3044c6f, EG.187) -- this is a review edit, not the kid own authorship. (1) WHAT THE INSTRUCTION SAID, quoted: "read each kid DIFF (git diff merge-base..<kid-branch>), never the result file", "Run one negative probe per claim conjunct yourself", and "A kid that passes its own suite but fails your probe is lean_disproved with the probe named". (2) WHAT THE MACHINE ACTUALLY DOES: the diff a2fa54dce..d26873744 carries 29 added / 3 removed lines of pi_trajectory.py and 48 added lines of test_pi_trajectory_retry.py; the changed branch `if attempt >= max_total:` sits AFTER `if not empty or empties >= max_retries: return code`, so it can only be reached on an empty attempt, and it returns that attempt own `code`; my six probes (fixtures, monkeypatched waits, no live pi) measured 3, 7, 8, 8, 1 and 5 attempts at cells 3, 7, absent, "not-a-number" and 0, plus recorded waits 1.00/2.00/2.00/2.00 for base 1 / factor 3 / cap 2 -- every claim conjunct holds on the tip, so the verdict stands at proved. (3) THE NEAR MISS: a node that reads plausibly, quotes its own 98-passed summary line, and names a F4 test I would have accepted on the prose -- but a test that only ever ran total=5, with the loader reading a hardcoded 5, would have passed the kid suite and failed P2. Likewise a "derived" default printed in the log but never computed from max_retries would have passed F4-at-5 and failed P3. (4) DEVIATION: none from a standing rule; the read-only `git diff`/`git log` I ran is inspection, the loop still owns every commit and my own round is committed only by cli.py done.
<!-- THOUGHT:END -->
