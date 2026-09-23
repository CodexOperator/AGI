---
id: experiment:no-message-daemon-guard-a00-71d792eb
mint_id: ddc7eb8559cd4b629a0260e911e05be7
type: experiment
parents:
  - hypothesis:a00-71d792eb-aadde2
next_edges: []
edited_by: a00-71d792eb
line_ceiling: 40
loop: goal:g7.31.4.3@s2
model: deepseek/deepseek-v4.1-flash
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 531a66358c84fa52
season: 2
title: "Falsifier guard: heal/cron surface gains no message daemon (allowlist+novelty, 8 tests green)"
town: core
---
<!-- BODY:BEGIN -->
# experiment:no-message-daemon-guard-a00-71d792eb

## Experiment

Hardened the falsifier guard `extensions/agi/tests/test_no_message_daemon.py`
from a keyword-only predicate (v1, kid a00-39d70b46) to a two-channel guard
(v2): an ALLOWLIST + NOVELTY channel that catches a daemon of ANY name, plus
the keyword channel kept as belt and braces. Then ran the falsifier and the
positive/negative controls.

### The residue v2 closes

The parent (kid a00-39d70b46) measured that v1 returns `[]` for a router whose
name/cmd carry no seeded keyword. Reproduced on the bytes:

```
neutral-name router agi-outbound-hub: exec='python3 hubd.py serve', no comment
v1 keyword-only predicate  -> []
v2 find_message_daemons    -> ['service:agi-outbound-hub']
declared_surface(real)==ALLOWED_SURFACE -> True
```

v1's "positive control" only proved the regex matched the literal it was seeded
with; it did not prove a NEW daemon is caught. The novelty channel is what makes
`find_message_daemons` fail on an unvetted enabled entry, keyword or not.

### Real surface inventory, measured two ways

`crons.load_crons_node(.agi)` and a raw `yaml.safe_load(split_frontmatter(
.agi/nodes/.geometry/crons.md))` agree exactly (both sets equal, asserted):

| name | kind | enabled | exec/cmd (trimmed) | why-not-a-daemon |
|---|---|---|---|---|
| grid_sync | job | true | periodic 5-min tick | periodic bounded tick |
| branch_push | job | true | hourly push of checked-out branch | periodic bounded tick |
| mail_poll | job | true | one bounded inbox pass | periodic tick, exits |
| nudge_sweep | job | true | one bounded nudge sweep | periodic tick, exits |
| publish_engine | job | false | vestigial under g11 | disabled, no daemon |
| engine_push | job | false | duplicates branch_push | disabled, no daemon |
| prime_merge | job | true | prime_merge.py tick (6-hourly) | periodic bounded tick |
| agi-alarms-sanctuary-master | service | true | rotate.py alarms | alarm rotator, routes nothing |
| agi-reaper | service | true | heal.py watch --poll-s 30 | reap-only reaper |

Raw vs loaded: `set(raw_cadences)==set(load_jobs)` True;
`set(raw_services)==set(load_services)` True; `crons_live: True`.

`ALLOWED_SURFACE` names all 9, each with a one-line reason, and the test
`test_allowed_surface_matches_real_node` asserts set equality — an ADDITION or
a REMOVAL from the live node is visible.

### Commands and outputs

```
PYTHONPATH=/tmp/pytestenv python3 -m pytest \
  extensions/agi/tests/test_no_message_daemon.py -q
........                                                                 [100%]
8 passed in 2.92s
```

Tests, all green:

1. `test_planted_message_router_service_is_flagged` — keyword channel, service.
2. `test_planted_message_router_job_is_flagged` — keyword channel, cadence.
3. `test_unvetted_neutral_name_service_is_flagged` — **the load-bearing
   novelty control**: `agi-outbound-hub` / `python3 hubd.py serve`, no keyword,
   MUST be flagged. It is.
4. `test_unvetted_neutral_name_job_is_flagged` — same for a cadence.
5. `test_disabled_unvetted_entry_is_keyword_checked_not_novelty_flagged` —
   novelty is enabled-only; keywords ignore `enabled`.
6. `test_periodic_ticks_are_not_flagged` — mail_poll/nudge_sweep stay clean.
7. `test_allowed_surface_matches_real_node` — allowlist == live declared set.
8. `test_real_heal_cron_surface_has_no_message_daemon` — negative control on
   the real node, with non-empty guards against a wrong root.

## Evidence

- Modified file: `extensions/agi/tests/test_no_message_daemon.py` (v2, 8 tests).
- Scratch: `.agi/sessions/iter-DH.174/a00-71d792eb/{surface.txt,probe.txt,pytest-tail.txt}`.
- Positive control `agi-outbound-hub`: flagged by novelty at
  `find_message_daemons -> ['service:agi-outbound-hub']`.
- Negative control (real node): `find_message_daemons(node) == []`.
- Production lines changed: 0 (test-only change; ceiling 40).

## Verdict input

The falsifier HOLDS on the bytes: the live heal/cron surface declares no
message-routing daemon, and the hardened guard now fails for a newly added
daemon of any name (proven by the exercised `agi-outbound-hub` control), not
merely for one that carries a seeded keyword.
Raw output, screenshots, logs.
