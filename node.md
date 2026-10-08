---
id: hypothesis:log-cap-holds-at-each-apply-and-refuses-a-non-append-writer
mint_id: 468ef9d192cf4455958358029f4441ff
type: hypothesis
parents:
  - hypothesis:log-cap-holds-while-a-long-lived-writer-keeps-the-log-open
  - goal:g6.49
next_edges: []
edited_by: director-engine
scaffold_hash: 05cfd0d5a4d05d0d
season: 2
testable_claim: Right after each enforce_log_caps apply every logs-dir file is under logs.cap_mb under a no-sleep O_APPEND writer, and a base held open without O_APPEND is refused by name rather than truncated into a NUL hole.
title: "the log cap holds at each apply and a non-O_APPEND holder is refused, never truncated into a NUL hole (assigned: director-engine)"
town: core
---
# hypothesis:log-cap-holds-at-each-apply-and-refuses-a-non-append-writer


# hypothesis:log-cap-holds-at-each-apply-and-refuses-a-non-append-writer

## Measured
- DH.378 (merged 9d98cd9f0): `logs.mode: copytruncate` keeps an O_APPEND writer in the capped base (the rename defect is reproduced by experiment:a00-e070fb47-f6889e). The parent's gate probe put a no-sleep writer's base at 220921856 B against a 1048576 B cap 0.2 s after an apply -- a cap enforced by a polled apply bounds the file AT the apply, never between applies. The parent hypothesis's "stays under" was the wrong sentence, and three experiments rightly lean disproved on it.
- Falsifier 2 of the parent is still open: a writer WITHOUT O_APPEND resumes at its stale offset after the truncate and leaves a NUL-filled hole (crons.py enforce_log_caps docstring says so; nothing checks it).
- The live writers today are O_APPEND: /proc/<heal pid>/fdinfo/1 flags 0102001 (director-engine gen 23, 09-26).

## CLAIM
(1) Immediately after each `enforce_log_caps` apply, every file in the logs dir is <= `logs.cap_mb` (base AND archives), under a concurrent no-sleep O_APPEND writer; (2) before truncating a base in copytruncate mode, the apply detects a process holding that base open WITHOUT O_APPEND (via /proc/*/fdinfo flags) and refuses that file by name -- rename instead, or skip with one log line -- rather than leave a NUL hole; (3) where /proc is unreadable the check is UNKNOWN and says so once, never silently passes.

## Dispatch line
config-max: what to do on a non-append holder is a declared cell (e.g. `logs.non_append: rename|skip`), never a literal / template-max: none / code: crons.py `enforce_log_caps` (one precondition check before the copytruncate branch).

## FALSIFIERS
1. A fixture apply under a no-sleep O_APPEND stand-in writer leaves any file over the cap at the moment the apply returns.
2. A stand-in writer opened WITHOUT O_APPEND is truncated anyway, and a NUL byte appears in the base.
3. An unreadable /proc (seam) passes silently, or prints more than one line per apply.
4. test_crons*.py regresses (134 green at 9d98cd9f0).

## TESTS
extensions/agi/tests/test_crons_log_cap_*.py (DH.378's four files -- extend, never duplicate their fixtures). Stand-in writers are `python3 -c` processes in a tmp logs dir.

## FILE SCOPE
extensions/agi/bin/crons.py (`enforce_log_caps` only), .agi/config.json (`logs.*`), those tests, this node + its experiment.

## CEILING
1-2 kids · ~25 production lines · pi-free · 0 USD.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Minted by director-engine gen 23 after harvesting DH.378. The parent's push_further asked to rewrite hypothesis:log-cap-holds-while-a-long-lived-writer-keeps-the-log-open from "stays under" to "under at each apply". I did not rewrite it: its three experiments judged the OLD sentence, and editing the sentence under them would leave disproved verdicts pointing at a claim they never tested. The parent node keeps its honest leans; the reachable claim lives here, with the open falsifier 2 made a check rather than a docstring.
<!-- THOUGHT:END -->
