---
id: experiment:a00-c73e0d7a-91c84e
mint_id: cabdf84e365b48caac0f604c319c99e5
type: experiment
parents:
  - hypothesis:wait-returns-on-an-empty-kid-set-and-turn-end-keeps-death-evidence
next_edges: []
confidence: 0.9
edited_by: a00-59133696
evidence_runs:
  - experiment:a00-c73e0d7a-91c84e
line_ceiling: 40
loop: hypothesis:wait-returns-on-an-empty-kid-set-and-turn-end-keeps-death-evidence@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "live cli.py wait 990 --agent ghost on a tier:parent-only manifest", "expected": "named non-zero at once, stderr names ghost", "observed": "rc=3; stderr no manifest agent matches --agent: ghost", "result": "pass"}
  - {"conjunct": 1, "class": "wire", "cmd": "live cli.py wait 990 on a kid row with started_at, --max-seconds -1", "expected": "heartbeat carries elapsed seconds; rc=2 genuine timeout", "observed": "stdout wait 990: k1=running elapsed=Ns; rc=2", "result": "pass"}
  - {"conjunct": 1, "class": "gate", "cmd": "live cli.py wait 990 on a parent-only manifest (zero kid rows)", "expected": "round 1 returned 0; order EF.39 item 2 requires a measured decision and a named non-zero code", "observed": "rc=0 at once SUPERSEDED by round-2 kid a00-bc68178d _WAIT_NO_KID_ROWS=4 -> rc=4", "result": "pass"}
production_lines: 27
profile: balanced
role: kid
scaffold_hash: 15c69da135a0bf1a
season: 2
title: DEF5 zero matching rows returns at once and DEF1 heartbeat carries elapsed, proved red-on-pre-fix
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-c73e0d7a-91c84e

## Experiment

DEF5 + DEF1 of the `l5-a-parent-waits` residue row, built on the round's base
`76a6be473cfe5f0ec09268635c9159868ef7eb8a`.

### (A) DEF5 — zero matching rows never poll to the deadline, never return 2

`cmd_wait` now splits the formerly empty-set fall-through into two cases:

1. Default set (no `--agent`) and the manifest carries NO `tier: kid` row:
   `rows == []`, `all(...)` over the empty list is True, so it returns **0 at
   once** after one heartbeat line.
2. `--agent X` where X matches no manifest row: printed
   `no manifest agent matches --agent: X` on stderr and returned the new
   module-level named constant `_WAIT_NO_AGENT = 3` at once. 3 is distinct
   from 1 (missing manifest) and 2 (genuine still-running timeout).

2 stays reserved for exactly one situation: at least one matching row is
non-terminal when the deadline elapses.

### (B) DEF1 — every heartbeat carries elapsed seconds

The heartbeat line keeps the `id=status` shape and appends `elapsed=Ns`.
A new module-level `_wait_elapsed(rec, now)` computes `now - started_at` as
whole seconds via `time.time()` (the epoch clock `started_at` is written with,
same as `dispatch.py:3424`), clamps negatives to 0, and returns 0 when
`started_at` is absent/0/null/unparseable. It never raises.

## Evidence

Production diff (measured, the only git read run):

```
$ git diff --numstat -- extensions/agi/bin/cli.py
27	6	extensions/agi/bin/cli.py
```

27 added production lines, under the 40-line ceiling (2x = 80).

Repo test run:

```
$ python3 -m pytest extensions/agi/tests/test_cli_wait.py -q
........                                                                 [100%]
8 passed in 0.22s
```

RED-ON-PRE-FIX, reproduced by the committed test
`test_pre_fix_base_sha_polls_empty_kid_set_to_timeout`, which materialises the
base bytes with:

```
$ git show 76a6be473cfe5f0ec09268635c9159868ef7eb8a:extensions/agi/bin/cli.py > <tmp>/base_cli.py
```

and calls that module's `cmd_wait` on the empty-kid fixture
(`agents=[{id:p1, tier:parent, status:running}]`, `max_seconds=2.0`,
a monotonic clock advancing 1 s per check): the PRE-FIX module printed a
heartbeat, slept 2.0 s worth of deadline, and returned **2** with
`still running: ` (empty). The same fixture on the built bytes returns
**0** at once. The base sha is hardcoded in the test so the red is
reproducible forever.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Round-1 review by parent a00-59133696 (EF.39 round 2). (1) The parent task says: read the bytes, not the result file, and run one negative probe per claim conjunct myself. (2) I read the commit 62b776560 diff for cli.py and ran three live probes against the real argparse subcommand (recorded in probes): --agent ghost returns the named 3 at once, a kid row with started_at prints elapsed seconds, and the same fixture shows the zero-kid-row case returning a silent 0. (3) Near miss: a probe that only calls cmd_wait through a module import would pass while the CLI never dispatched it; the live subcommand is what proves the changed bytes are reached. (4) The zero-kid-row branch this node built as a 0-at-once is SUPERSEDED by director order EF.39 item (2) and by round-2 kid a00-bc68178d, which measured the spawn race (manifest written before dispatch returns) and made the same case return the named _WAIT_NO_KID_ROWS=4. The --agent-absent code 3 and the elapsed heartbeat stand as built.
<!-- THOUGHT:END -->

## Agent Notes
DEF5: zero matching rows return at once (0 for no kid rows, named _WAIT_NO_AGENT=3 for --agent absent), never 2; DEF1: heartbeat carries elapsed=Ns. 27 production lines; test_cli_wait.py 8 passed, red-on-pre-fix proved against base 76a6be473.
