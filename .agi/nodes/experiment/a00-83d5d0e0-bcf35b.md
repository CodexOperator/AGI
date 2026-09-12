---
id: experiment:a00-83d5d0e0-bcf35b
mint_id: 0b8c2651a02b4f5585631b8fb9929040
type: experiment
parents:
  - hypothesis:l4-the-rotation-alert-hook-prints-one-compact-meter-line-on-every-prompt
next_edges: []
confidence: 0.95
edited_by: a00-84f091be
evidence_runs:
  - experiment:a00-83d5d0e0-bcf35b
loop: hypothesis:l4-the-rotation-alert-hook-prints-one-compact-meter-line-on-every-prompt@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 4b4c3fea03e881c6
season: 2
title: SL7.70 kid2 — P7 carve-out pinned in tests (no [meter] on silent paths), mid-read OSError settled as P7 silence, and the living "read the meter" instructions named
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-83d5d0e0-bcf35b

SL7.70 kid 2 on hypothesis:l4-the-rotation-alert-hook-prints-one-compact-meter-line-on-every-prompt (built by kid 1, experiment:a00-7cee97dc-f7add2, 40/40 green). Kid 2 did NOT re-do the build — it pinned the silence kid 1 left unguarded, settled the one path kid 1 did not probe, and named the meter instructions. **Hook untouched** (measured, default honoured). Three parts.

## T1 — PIN the P7 carve-out in tests (the main deliverable)

The claim's word "unconditionally" is false on exactly the paths the hook's own P7 line (rotation_alert.py:36 — "SILENT and exit 0 outside an agi project and on an unreadable transcript — this runs on every session on the box and must never break one") requires to be silent. That is architecture, not a defect — but it was an unguarded cliff: a kid who reads "unconditionally" and greps for the early `return 0` could "fix" it and emit a meter line into every session on this box.

Re-measured on this base (real hook bytes, out of process):

| payload | rc | stdout |
|---|---|---|
| no `transcript_path` | 3 | `[meter] post=n/a no-transcript-path` + fail-closed on stderr |
| `transcript_path` to a file that does not exist | **0** | **`''` — nothing at all** |
| `cwd` outside an agi project | **0** | **`''` — nothing at all** |
| readable transcript, below band | 0 | `[meter] post=sensei-director 0.0500 (5000/100000) line=0.2500` |

Added two tests in `extensions/agi/tests/test_rotation_alert.py` that make the silence **deliberate and named**, each naming `P7` and the hypothesis id, each quoting the measured probe row (not an inference):
- `test_p7_no_meter_outside_agi_project` — payload cwd with no enclosing `.agi` → rc 0, `out == ""`, `"[meter]" not in out`.
- `test_p7_no_meter_transcript_does_not_exist` — transcript_path not on disk → rc 0, `out == ""`, `"[meter]" not in out`.

## T2 — SETTLE the mid-read OSError path by measuring it

Third silent path the parent did not probe: `_latest_usage(tp)` raising `OSError` (file exists — so P7's "unreadable transcript" clause is ambiguous — but the read fails after `is_file()`). Measured for real with a `chmod 000` transcript (file exists on disk at `is_file()` time, open() raises `PermissionError`, uid 1001):

| payload | rc | stdout | stderr |
|---|---|---|---|
| existing transcript, chmod 000 | **0** | **`''` — nothing** | `rotation-alert: fail-closed: cannot read transcript: [Errno 13] Permission denied: '...locked.jsonl'` |

**Decision: P7 silence, not the claim.** The claim is explicitly scoped to "INSIDE AN AGI PROJECT WITH A READABLE TRANSCRIPT". An unreadable transcript is outside that scope; P7 says be silent and exit 0 so a session is never broken. A `[meter]` line for a number the hook could not read would be worse than none (P6: never a confident fraction). The fail-closed reason belongs on **stderr** — a diagnostic that breaks nothing. Current behaviour is correct; **the hook was left completely untouched**, as the directive's default required.

Pinned with `test_mid_read_oserror_is_p7_silence_not_claim`, which exercises the `_latest_usage` seam deterministically (an unreadable real file is environment-dependent — root bypasses 000), asserts rc 0, `"[meter]" not in out`, `out == ""`, and the fail-closed `cannot read transcript` on stderr. Its docstring states which of the two it is (P7 silence) and why.

## T3 — NAME (do not edit) the living "read the meter" sentences

## F-facts and briefs that still say "read the meter"

Grep'd `.agi/nodes/`, `extensions/`, `skills/`, `context/` for the sentences that tell a reader/post/seat to read the meter by hand. **Edited none.** The living instructions:

- `.agi/nodes/doc/l4-owner-decisions.md:459` — "Seats read the meter after every round close and before every dispatch, not only at pauses." — a standing protocol note that seats read the meter **by hand**. The strongest "read the meter" instruction in the tree. The hook now auto-prints the meter every prompt; this sentence could be dropped (or, if the auto-line is deemed the new "read", reworded) — named, not edited.
- `skills/agi/SKILL.md:140` — "**`agi:check-handoff`** → `rotate.py meter --check [--session-log PATH]` — fraction against `director_rotate_at`..." — surfaces a manual meter read as a named suggestion. A reader running this to check context now does by hand what the hook already prints.
- `skills/agi/SKILL.md:128` — "**Rotation:** `rotate.py meter` prints context-usage fraction against `director_rotate_at`..." — reference line describing the manual command; a reader following it to read their own context does it by hand.
- `extensions/agi/briefs/prime-director-successor.md:7` — "Pin your meter yourself: `rotate.py meter --pin .agi/sessions/belam.meter --session-log <your transcript>`." — on the RECOVERY/spawn path only (predecessor died without rotate-self pre-run); still a real manual meter action there, so it is arguably correct to keep — named regardless.
- `extensions/agi/briefs/prime-director-successor.md:27,29` — references to "the 0.47 context cap to rotate" / "the prime rotates at 0.47" — describe the threshold, not an instruction to read by hand.

Not counted (descriptive / auto-run, not manual reads): `goal/g15.25.md:158` describes this round's own purpose; `.agi/nodes/hypothesis/l3-seat-pin-not-repointed-on-rotation.md:45` and `l3-seat-pin-generation-never-increments.md:58` are stale round-reproduction/verify instructions, and their old rounds are long since run; the `pin` template rows in `.agi/nodes/.geometry/rotations.md:66,107` are `rotate.py meter --pin` commands **auto-run by rotate-self** (startup/after_join), not manual reads; `sensei.py` wake-audit's `service-owed (s) meter` category classifies a *hand* `rotate.py meter --pin` as service-owed, which is a different concern. The F-facts themselves are already auto-run by rotate-self (per rotations.md:191, "Target: the seat's first tool call is graph work"), so no F-fact sentence still tells a seat to read the meter by hand.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rotation_alert.py -q` → **43 passed** (was 40; +2 T1 +1 T2).
- `python3 -m pytest extensions/agi/tests/test_rotate.py extensions/agi/tests/test_rotate_next.py extensions/agi/tests/test_rotate_prepare.py -q` → **283 passed** (neighbours, untouched, still green).
- The three T1/T2 probe tables above are live measurements of the real hook binaries via a subprocess, pasted verbatim.
- FILE SCOPE honoured: only `extensions/agi/tests/test_rotation_alert.py` edited + this node. Hook, hypothesis node, rotate.py, ladder untouched.

## Agent Notes

T1, T2, T3 all finished. Caveat worth recording: T2's *real* chmod-000 probe is only a valid manual measurement on a non-root user (root bypasses 000); the pinned test uses the `_latest_usage` seam for determinism, so the suite is environment-independent.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW SL7.70 (a00-84f091be), accepted as proved. I re-ran the suite (43 passed in 4.56s, was 40) and spot-checked the kid's citations against the bytes: skills/agi/SKILL.md:128 and :140 do contain the two lines it names, extensions/agi/briefs/prime-director-successor.md:7 does contain 'Pin your meter yourself: rotate.py meter --pin ...', and .agi/nodes/doc/l4-owner-decisions.md:459 does contain 'Seats read the meter after every round close and before every dispatch, not only at pauses.' So T3's naming is checkable and correct, not paraphrase. T2's decision (the mid-read OSError path is P7 silence, not the claim, hook untouched) I accept and it is the right call for a reason the kid did not state: the fail-closed stderr line is already the diagnostic for that path (:1044ish, 'cannot read transcript'), so adding a [meter] refusal on stdout would print a meter line for a session whose transcript we could not read -- the one thing P6 forbids is a confident number, and the second thing P7 forbids is breaking a session on a path this hook cannot see into. The kid's `_latest_usage`-seam test is the right determinism choice too (its own caveat is correct: a chmod-000 fixture is only valid as a manual measurement on a non-root uid). Its placeholder-vs-instruction classification is exactly the kind of judgement a later kid can overturn with evidence; I have handed the (a)-class drops to kid 3 (a00-35eff647) which must REWORD not delete, so this node's naming survives as the audit trail for whatever kid 3 removes.
<!-- THOUGHT:END -->

## Agent Notes
P7 carve-out pinned in tests (no [meter] outside project / on missing transcript, named P7+hyp id); mid-read OSError measured real (chmod-000) and settled as P7 silence not the claim (hook untouched); T3 names live read-the-meter sentences (doc:459 strongest, SKILL.md:128/140, brief:7), edits none. 43 rotation-alert + 283 neighbour tests green.
