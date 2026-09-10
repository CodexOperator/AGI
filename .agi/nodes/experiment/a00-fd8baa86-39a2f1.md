---
id: experiment:a00-fd8baa86-39a2f1
mint_id: 2816eadfa71a4c3981b06e1566991fab
type: experiment
parents:
  - hypothesis:l4-a-meter-you-must-remember-to-read-is-a-coin-flip
next_edges: []
confidence: 0.6
edited_by: a00-651d2d35
evidence_runs:
  - experiment:a00-fd8baa86-39a2f1
loop: hypothesis:l4-a-meter-you-must-remember-to-read-is-a-coin-flip@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 12a664c29e7d2b9a
season: 2
title: A00 fd8baa86 39a2f1
verdict: inconclusive_lean_proved:65
---
<!-- BODY:BEGIN -->
# experiment:a00-fd8baa86-39a2f1

## Claim under test

`hypothesis:l4-a-meter-you-must-remember-to-read-is-a-coin-flip` — a rotation
warning must arrive UNPROMPTED (a SessionStart hook handed its own transcript
path on stdin), escalate per rising bands, and name the exact next command. The
mechanistic proof criteria (a)–(g) of the brief, tested against a NEW hook.

## What I did

Scoped tight (HARD ceiling = 2 kids; only `extensions/agi/hooks/` and
`extensions/agi/tests/` may be touched — rotate.py and its tests are a parallel
round's, left untouched). Built one thing:

- **`extensions/agi/hooks/rotation_alert.py`** — a SessionStart hook reading the
  handed JSON payload on stdin. It uses ONLY the handed `transcript_path`
  (P1: never resolves, never reads a `.meter` pin, never takes the newest);
  **fails closed** with a named error exit(3) if `transcript_path` is absent
  and exit(4) if the ladder window/threshold is unreadable (P2, P6); **escalates**
  once per band below the line and on EVERY firing at/over it (P3); keys
  escalation state by `session_id` under `/tmp/agi-rotation-<uid>` — machine
  local, never the shared main-checkout sessions dir (P4); prints a copy-pasteable
  command naming the explicit `--session-log <handed path>` (P5); silent + exit 0
  outside an agi project and on an unreadable transcript (P7). NOT installed —
  registration snippet is in the hook's header, the owner's call.
- **`extensions/agi/tests/test_rotation_alert.py`** — 8 tests implementing the
  brief's proof criteria (a)–(e).

## What happened (results)

All 8 new tests PASS; the 90 pre-existing `test_rotate*.py` tests still PASS
(nothing of theirs edited); `commands.py run verify` PASS (8/8).

Proof outcomes, mapped to the brief:
- (a) names the handed path in `--session-log` — asserted on the LITERAL path.
- (b) missing `transcript_path` → exit(3), named "fail-closed" error, no fraction.
- (c) ONE session, rising usage → emits once per band below line, and a re-run
      at/over the line emits again (every firing); staying inside a fired band
      is SILENT. Counts asserted per band.
- (d) two different session_ids in ONE state dir do not share escalation state
      (B still fires after A; A is silent on replay).
- (e) silent + exit 0 outside a project and on an unreadable/nonexistent
      transcript, and on empty stdin.
- (f) run by hand against a real payload naming a real transcript:
      `## ⚠️ ROTATION OWED NOW — at or over the line … python3 …/rotate.py meter
      --seat director --pin --session-log /home/ubuntu/.claude/projects/…jsonl`
      with the handled path interpolated. Exit 0.
- (g) `commands.py run verify` PASS.

## Caveat this experiment surfaces (the open question is real, not theoretical)

The real-payload run scored the biggest transcript on the box at **180.07** —
way over the ladder's 1M window. The numerator choice (input + cache_read +
cache_creation, summed over assistant messages, exactly what `rotate.py meter`
reports) plus a 1M window is NOT a valid bound for a long prime session. The
hook reads the ladder's `director_context_tokens` and does not independently
measure or validate the window, so on P6 ("DO NOT ASSUME the denominator … FAIL
CLOSED if it cannot be established") it is only HALF met: it fails closed on an
ABSENT window, but trusts a DECLARED one. That is the honest state of the brief:
the mechanism is proved, the denominator is not.

## Agent Notes
Built rotation_alert.py SessionStart hook + 8 tests: handed-path transcript (P1), fail-closed on missing transcript/ladder (P2/P6), per-band escalation + every-fire-at-line (P3), per-session_id state in /tmp not main checkout (P4), names --session-log <handed path> (P5), silent outside project (P7). 8 new + 90 existing tests pass; verify PASS; real-payload run emitted the rotation banner naming the handed path. Caveat: real run scored 180x -> the 1M denominator is unmeasured; hook trusts a DECLARED window, so P6 half-met. Mechanism proved, denominator not.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-651d2d35, L4.94): accepted as written. Verified independently, not from the report — ran the 8-test suite (pass), fed a payload missing transcript_path (exit 3, named error, no fraction), an unreadable transcript (exit 0, silent), and grep-confirmed no resolve_transcript / .meter read / glob / settings.json write in the hook body (hits only in header comments). Verdict held at inconclusive_lean_proved:65, not demoted: the mechanism criteria (a)-(e),(g) are met and tested; the only gap is the DENOMINATOR (P6), which the brief itself left open and the node states honestly rather than overclaiming — 180x real-run score shows the declared 1M window is unmeasured. Evidence linked (this experiment IS the run), so no auto-demotion. No scope violations: only the hook and its test were touched; rotate.py and its tests untouched.
<!-- THOUGHT:END -->

Review verdict (parent a00-651d2d35): ACCEPT. All proof criteria tested and independently reproduced; P6 denominator honestly reported half-met; verdict 65 lean proved stands; evidence_runs correctly self-linked.
