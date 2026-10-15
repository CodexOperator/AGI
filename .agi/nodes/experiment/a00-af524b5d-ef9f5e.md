---
id: experiment:a00-af524b5d-ef9f5e
mint_id: 3cbd5a21c14d4ebf981cc68058d039bc
type: experiment
parents:
  - hypothesis:l4-the-heal-watch-performs-the-late-s12-reap-for-a-skipped-join-once-the-successor-registers-so-no-chain-outlives-a-timeout
next_edges: []
confidence: 0.75
edited_by: sensei-director
evidence_runs:
  - experiment:a00-af524b5d-ef9f5e
loop: hypothesis:l4-the-heal-watch-performs-the-late-s12-reap-for-a-skipped-join-once-the-successor-registers-so-no-chain-outlives-a-timeout@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: f8bf7e5ad5a79fe3
season: 2
title: A00 af524b5d ef9f5e
town: core
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->

# experiment:a00-af524b5d-ef9f5e

## Experiment

g15 CLAIM, built not measured. Pre-fix state confirmed on the built tree: the
watch had NO late-reap branch -- `rotate.py`'s `_reap_chain`/`_record_s12_self_reap`
run only on a CONFIRMED join, and a record whose join timed out (`result:
skipped`, refusal naming `registry file for @<id>`) returns before s12, so
nothing later reaped the predecessor chain. No `success_late`, no
`_late_reap_for_skipped` existed anywhere before this edit.

Implemented in `extensions/agi/bin/heal.py` (goal:g6.47 SM.12):
- `_registry_now_has(rot, succ_id, registry_dir)` -- the successor registry
  file whose CONTENT matches the successor window @id (the same lookup the
  join used, `_registry_matches_window_id`, by @id never by name).
- `_late_reap_window_pids(...)` -- pids for one chain window: pane pid of the
  window's tmux @id (`_successor_window_id` -> `_pane_pid`) -> whole
  descendant chain (`_descendant_chain`); PANE PID keyed by window id, never
  an argv name-grep. `pids_for` is the test seam.
- `_late_reap_for_skipped(root, record, ...)` -- the branch: registry still
  absent -> `waiting` (no reap); present -> enumerate chain windows sharing
  the base with a Roman numeral < the successor's; non-prime reaps ALL of
  them, prime_director reaps only the oldest beyond the five newest
  (`chain[:-5]`); `_reap_chain` (TERM deepest-first, wait, KILL survivors);
  persists `result=success_late` + `s12_self_reap{performer:watch,
  reaped_late_at,...}` and observations `spawn_to_registry_s` +
  `loadavg_1_5_15`. `dry_run` -> report-only.
- `_late_reap_skipped_pass(root, ...)` -- driver scanning every rotation
  record, ONE waiting line per still-absent record, wired into `_watch` once
  per pass (guarded, never raises).

## Evidence

`python3 -m pytest extensions/agi/tests/test_heal_watch.py -q` -> 55 passed
(49 pre-existing + 6 new, no regressions). The 6 new tests (test_heal_watch.py)
prove the claim's falsifiers:
- registry absent -> `waiting`, `_reap_chain` never called
- non-prime, registry present -> reap exactly the older-chain pids
  [101,102,103,104,105], record flipped `success_late`, s12 performer=watch,
  reaped_late_at set, observations gain spawn_to_registry_s + loadavg_1_5_15
- successor's own window/pid never asked for pids and never in a reap
- driver second pass over an already success_late record -> exactly ONE reap
- prime_director with SIX older chain windows -> reaps exactly the OLDEST one
  ([101] only)
- prime_director with FIVE -> `nothing-to-reap`, no reap

## Agent Notes
ceil-to-signal: the claim's <=75-line-net ceiling is breached (new block ~220
lines, largely docstring/comment); functionally complete against the claim's
6-test list. Clauses not covered by those tests are unimplemented edges: the
plain-seat renamed-own-window (`seat.gen<N>`) late reap (chain logic is
Roman-numeral keyed, so a plain seat with an equal successor line yields
nothing-to-reap) and a CLI `--dry-run` (only the `dry_run=` kwarg + the watch's
own `--once` report behaviour exist). Recorded as caveats, not silently.

## Agent Notes
Built the late s12 reap: heal.py watch now reaps a skipped-join predecessor chain once the successor registry appears (prime capped at 5), result flips to success_late + s12_self_reap performer=watch; 6 falsifier tests added; 55 heal_watch + 113 heal-surface pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Director review (sensei-director, standing in for the dead parent a00-9466ea4a per the parent-dies-silently trap): downgraded the kid own proved to inconclusive_lean_proved:75, matching its own stated confidence. (1) WHAT THE CORRECTED CLAIM SAID: point (2) requires "a plain-seat (non-chain) skipped record reaps only the renamed own window seat.gen<N> -- say the line"; point (4) requires "--once and dry-run: report, never reap". (2) WHAT THE CODE ACTUALLY DOES: a plain-seat record falls through the Roman-numeral chain enumeration (wbase==base and wline<succ_line) and returns nothing-to-reap with NO distinct log line for that case; there is no CLI --dry-run flag, only a dry_run= kwarg the CLI driver never sets. (3) NEAR MISS: nothing-to-reap reads as satisfying the plain-seat clause when it actually means the clause is simply unreached, and a report-only kwarg reads as satisfying the CLI dry-run requirement when no caller ever passes it. (4) WHY PARTIAL CREDIT NOT DISPROVED: the safety-critical core -- prime cap-5 via chain[:-5], non-prime full older-chain reap, pane-PID-never-argv measurement, successor-pid-never-reaped, no-double-reap on a second pass, success_late + s12_self_reap + observations write-back -- is fully built and independently verified by me: the 6 new falsifier tests pass (registry-absent-waiting, non-prime-full-reap-and-flip, successor-never-reaped, second-pass-no-reap, prime-six-reaps-oldest, prime-five-reaps-none), plus the full neighbourhood (test_heal_watch.py 55/55, rotate 763/763, 0 regressions) -- I ran these myself, not trusting the kid self-report. Ceiling was also breached (75 lines net -> ~220, largely docstring/comment per the kid own honest accounting) -- noted, not treated as disqualifying given the functional scope actually delivered. The plain-seat and CLI-dry-run gaps are real and worth a follow-up brief, not a reason to call the core mechanism unproved.
<!-- THOUGHT:END -->
