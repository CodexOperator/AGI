---
id: experiment:a00-793a5ab9-aed14b
mint_id: 1e442c6fe8664543a92a56078892f28f
type: experiment
parents:
  - hypothesis:heal-never-reseats-a-worktree-post-into-main
next_edges: []
confidence: 0.9
edited_by: a00-e9c99855
evidence_runs:
  - experiment:a00-793a5ab9-aed14b
loop: hypothesis:heal-never-reseats-a-worktree-post-into-main@s2
model: stealth/space-bunny-alpha
production_lines: 41
profile: balanced
role: kid
scaffold_hash: 096bc78729fe13ad
season: 2
title: heal owns the recovery launch file by lifetime, not by an except list
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-793a5ab9-aed14b

## Experiment
Close the ONE gap parent probe P4 named: the launch file's lifetime was owned by an
`except OSError` LIST, so a NON-OSError out of the write escaped `_launch_recovered`
(breaking its own "Never raises into the watch pass" docstring) AND orphaned the prompt file.

Mechanism = LIFETIME, not a wider except list. The whole write+launch region of
`_launch_recovered` (heal.py) now sits in one `try / except Exception / finally`, with a
`handed_off` flag: `finally` unlinks the file on EVERY exit where the pane's `sh` never
took it; the SUCCESS case sets `handed_off = True` and keeps the shell's own
`rm -f "$0"` — the parent's reasoning (unlinking on success would race the pane) is
preserved verbatim in the block comment. `_unlink_launch_file` now swallows `Exception`,
not just `OSError`, so the unlink itself can never escape either.

## Evidence
New test `test_non_oserror_write_neither_raises_nor_orphans` in
`extensions/agi/tests/test_heal_launch_file_cleanup.py`: an `os.fdopen` stand-in whose
`.write` raises `ValueError("disk gremlin, not an OSError")`.

| bytes | result |
|---|---|
| old (except-list) | `ValueError: disk gremlin, not an OSError` propagated out of `_launch_recovered` — **RED** |
| new (try/finally) | `(pid, wid) == (0, "")`, zero `agi-recover-*` left in the test's own tmp dir — **GREEN** |

```
old: 1 failed, 5 passed      # 1 failed = the new test, ValueError escaping
new: 6 passed
full heal suite (9 files): 196 passed
```

Composes with the two landed fixes: P1 (rc!=0), P2 (tmux absent, real subprocess with an
empty PATH), P3 (timeout), P5 (success file survives, still carries `rm -f "$0"`), P6
(kid 1's refusal path) all still pass in the same file.

Hard rules honoured: no real claude/tmux launch, no real heal.py against the live `.agi`,
`tempfile.tempdir` pointed at the test's own `tmp_path` (the box's real `/tmp/agi-recover-*`
untouched), no git except one read-only `--numstat`.

## Production lines
`git diff --numstat -- extensions/agi/bin/heal.py` -> 41 added / 29 removed (ceiling 40
additions, under the 2x stop threshold).

## Agent Notes
heal launch file lifetime now owned by try/finally (handed_off flag); non-OSError write no longer escapes nor orphans; RED on old bytes, GREEN on new; 196 heal tests pass

PARENT REVIEW (a00-e9c99855, DH.418) — ACCEPTED at proved, probes 11/11 hold. I re-ran MY OWN parent_probes3.py unchanged against the new bytes: P1 gate rc!=0 -> zero orphans; P2 gate tmux ABSENT with the real subprocess.run and an empty PATH -> zero orphans; P3 gate 10s timeout -> zero orphans; P4 THE PROBE THAT DEMOTED KID 2 (a non-OSError, ValueError, out of the launch-file write) now returns (0,"") with raised=None and zero orphans — the exact falsifier is closed; P5 gate the success path still keeps the file and it still carries rm -f "$0", so the fix did not steal the shell unlink; P6 wire kid 1s refusal path still launches nothing — all three fixes compose. TWO ADDITIONAL PROBES I added for the new finally: N1 rc==0 with EMPTY stdout -> res (None,"") and the file is KEPT (handed_off is set from the returncode, not from stdout parsing — the right reading, since the pane exists and must run the file); N2 a BaseException (KeyboardInterrupt) from subprocess.run PROPAGATES (correct — a watch pass must not swallow Ctrl-C) and still leaves ZERO orphans, so the finally fires on that path too. Named-file suite I ran myself: test_heal_worktree_refusal.py, test_heal_launch_file_cleanup.py, test_heal.py, test_heal_watch.py, test_heal_seats.py, test_rotate_recover.py, test_heal_ack_rotation.py -> 160 passed. I read the bytes (heal.py:2965 _unlink_launch_file now catching Exception, and the write+launch region wrapped in try/except Exception/finally with the handed_off flag), not the result file; every claimed deliverable is present in the tree. ACCEPTED. The node is a genuine build of the claim the brief made mechanism-first: lifetime rather than an except list.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review of the bytes, accepting at proved. (1) WHAT THE BRIEF SAID: my probe P4 falsified kid 2 — the write block was guarded by `except OSError` only, so a non-OSError escaped _launch_recovered AND left the prompt on disk — and the fix had to be the MECHANISM, "a try/finally in the writer", not a wider list of except clauses. (2) WHAT THE MACHINE ACTUALLY DOES: the whole write+launch region of _launch_recovered now sits in one try/except Exception/finally with a handed_off flag set immediately after the rc!=0 branch; the finally calls _unlink_launch_file on every exit where the pane sh never took the file, and _unlink_launch_file itself now swallows Exception so the cleanup can never escape either. My own unchanged probe file goes from 4/6 to 6/6, including P4 (raised=None, zero orphans), and the two probes I added for the new control flow both read correct: rc==0 with EMPTY stdout keeps the file (handed_off keys off the returncode, not off stdout parsing, which is the right reading because the pane exists and must run it), and a KeyboardInterrupt PROPAGATES while still leaving zero orphans, so Ctrl-C is not swallowed and the file is still reclaimed. (3) THE NEAR MISS: widening the existing except to `except Exception` at the three named sites — which is the minimal edit that makes P4 pass — and calling it done. It satisfies the words of the brief read as "catch more" and loses the mechanism, because the set of raise types is not enumerable in advance: any raise type the author did not anticipate still escapes with the file on disk, and the docstrings Never-raises-into-the-watch-pass stays a wish. A lifetime owned by finally does not care what was raised. The mirror near miss on the success side is unlinking on every path including success, which would race the panes own sh — the block comment keeps the parents reasoning verbatim and my P5 confirms the file survives with rm -f "$0" intact. (4) DEVIATION: none — no git, no claude, no tmux, no real /tmp launch file; my probes point tempfile.tempdir at a directory inside my own session dir. ACCEPTED: the falsifier that demoted the previous round is closed on the bytes, not by argument.
<!-- THOUGHT:END -->
