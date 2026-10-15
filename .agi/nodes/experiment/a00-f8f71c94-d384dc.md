---
id: experiment:a00-f8f71c94-d384dc
mint_id: 9bb74e7b86ec442ca451f90e675e256b
type: experiment
parents:
  - hypothesis:l4-authority-verified-against-the-graph-not-the-message
next_edges: []
confidence: 0.9
evidence_runs:
  - experiment:a00-f8f71c94-d384dc
loop: hypothesis:l4-authority-verified-against-the-graph-not-the-message@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: db5b1ee4993fa2e3
season: 2
title: A00 f8f71c94 d384dc
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f8f71c94-d384dc

## Experiment

Task: prove hypothesis `l4-authority-verified-against-the-graph-not-the-message`
by adding a `whois` subcommand to `send.py` that authenticates a claimed
session_ref against the PUSHED config:seats, then running (a)-(h).

### What I built (scope: `extensions/agi/bin/send.py` + `test_send.py` only)

`send.py whois <session_ref> [--claim NAME] [--source REF] [--no-fetch]`:

* **Reads the pushed ref, not the working tree.** `_pushed_seats` does
  `git fetch origin season/s2`, then `git rev-parse <ref>` for provenance and
  `git show <ref>:.agi/nodes/.geometry/seats.md` for the file. Default source
  `origin/season/s2`.
* **Reuses the ONE parser — no sixth reader.** The pushed byte-string is
  parsed with `_fm.load_node_file` (graph_core frontmatter), the same node-
  loader `hierarchy.load_seats` routes through; the only difference is the
  byte source is as a temp file fed the git-show output instead of the local
  file. No new hand-rolled `/seats/` regex was added. I chose this over
  `hierarchy.load_seats` itself because that function is bound to the
  working-tree path — exactly what the crux forbids — so I reuse its parse,
  not its file handle.
* **Two directions.** `whois <ref>` names the seat+role; `whois <ref>
  --claim NAME` answers whether that ref IS that row (checks against BOTH the
  seat name and the role). A ref present in the table but under a DIFFERENT
  name/role answers `IS-NOT-AUTHORIZED` — the impersonation case a
  presence-only check would pass.
* **Provenance in every answer.** A verified answer prints the source ref and
  the commit sha it was read from.
* **Fail-closed.** If the pushed ref is unreachable it answers from the
  working tree as a labelled fallback but renders `UNVERIFIED` and returns
  exit code 1 — never a silent 0.

### Results

Hermetic suite (8 whois tests) + full `test_send.py` (82 passed, committed
additions only — no existing test edited) + `test_bin_help_smoke.py` (58
passed, 1 skipped) + real-tree run. Every criterion (a)-(h) green.

## Evidence

`test_send.py -k whois`: 8 passed. Full `test_send.py`: 82 passed.

Real-tree run against live pushed ref `origin/season/s2 @
39a3a3d4b49209d8dd145451d13aa11ef65bb266` (fetched live):

```
SEAT: 7902ac -> seat belam, role prime_director  (verified ...@ 39a3a3d4...)
SEAT: 3d6888 -> seat sanctuary-director, role director (verified ...@ 39a3a3d4...)
SEAT: 9d073a -> seat sanctuary-helper, role director (verified ...@ 39a3a3d4...)
IS-AUTHORIZED: 3d6888 vs claim 'sanctuary-director' -> ... (rc=0)
IS-AUTHORIZED: 9d073a vs claim 'sanctuary-helper'    -> ... (rc=0)
IS-NOT-AUTHORIZED: 7902ac vs claim 'sanctuary-helper' (wrong seat, rc=0)
IS-NOT-AUTHORIZED: 7902ac vs claim 'director'        (belam is prime_director, rc=0)
NO-MATCH: cafebabe belongs to no seat row (unknown ref, rc=0)
```

`commands.py run verify`: PASS (all 8 checks, suite=off): links broken=0,
goals byte-identical, write-guard, smoke, viewport-verify, dispatch-help,
budget, node-count active=1784/deprecated=194/total=1978.

DISPROVED criteria checked against the diff: reads the pushed ref (not only
working tree) — pass; unverified exits 0 — fail (returns 1) — pass; answers
YES on role mismatch — no (IS-NOT-AUTHORIZED) — pass; sixth seats parser —
reuses `_fm.load_node_file` — pass; provenance missing — no, present — pass;
existing test edited — none, additions only — pass.

## Agent Notes
whois subcommand added to send.py: authenticates a claimed session_ref against the PUSHED origin/season/s2 config:seats (git fetch+show+rev-parse), reuses the shared _fm.load_node_file parser (no sixth reader), two directions (name-the-seat / --claim impersonation check), provenance sha in every verified answer, UNVERIFIED+exit 1 on unreachable pushed ref. Real-tree run on live seats belam/7902ac dir-sd/3d6888 helper/9d073a + mismatch + unknown all correct; 8 hermetic tests + 82 test_send + 58 smoke + commands.py run verify PASS.

## Agent Notes
done
