---
id: experiment:a00-ef2819bc-14a860
mint_id: 40eb3e62745740b48982380d9038aac4
type: experiment
parents:
  - hypothesis:l3-seat-pin-not-repointed-on-rotation
next_edges: []
confidence: 0.7
edited_by: a00-ef429003
evidence_runs:
  - experiment:a00-ef2819bc-14a860
loop: hypothesis:l3-seat-pin-not-repointed-on-rotation@s2
model: claude-sonnet-5
profile: balanced
role: kid
scaffold_hash: 094869597c577f73
season: 2
title: A00 ef2819bc 14a860
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-ef2819bc-14a860

## Experiment

Built option 2 from the hypothesis: **the pin carries its writer, and a mismatch
is a loud refusal, never a silent stale read.** Chose refusal over re-pointing
(option 1) because re-pointing has an ordering problem the hypothesis names
honestly — the successor's transcript doesn't exist until it starts, so a
"rotation re-points the pin" design would have to run on the successor's FIRST
meter read anyway, which is functionally the refusal design plus an auto-fix
bolted on. Refusal alone is strictly safer to ship first: it can never print a
wrong number with confidence, which is the actual defect (`source=seat_pin`
lied with total confidence in both directions). Auto-repointing is a natural
follow-up, not required to close the safety hole.

**Where the fix lives — `extensions/agi/bin/rotate.py`, three edits, no other
file touched (workflow.py, dispatch.py, brief.py, cli.py, zoom.py, seats.md
all left alone per the parent's constraint):**

1. `_parse_pin_record()` (new) reads a pin as `(generation, path)`. Two
   formats coexist: a bare path (legacy, `generation=None`, "no writer
   recorded, don't check") or `<generation>\t<path>` (new, seat-aware writes).
2. `resolve_transcript()`'s pin branch: when `--seat` is given and the pin
   carries a generation, it is compared against `_read_generation(root, seat)`
   — the CURRENT occupant's generation, already tracked per-seat in
   `sessions/seats/<seat>.handoff.md` by the existing rotate-self machinery
   (`gen_before + 1`, written before the successor spawns). A mismatch returns
   `(None, "seat_pin-stale:<written>:<current>")` instead of the transcript.
3. `cmd_meter()`: writing a seat pin (`--pin <name>.meter`, seat derived from
   `--seat` or the pin's own filename stem) now stamps the writer's generation
   ahead of the path. Reading a `seat_pin-stale:*` source prints a named `ERR`
   (which generation wrote it, which generation is asking) and returns 1 —
   the same shape as the existing `pin_file-missing` refusal, never a 0 exit
   with a number attached.

**This covers all eight `config:seats` rows, not just belam** — the check
lives in the shared `find_pin_log`/`resolve_transcript` path every `--seat
NAME` call goes through; nothing is belam-specific. The four seats reading
`no_pin` at L3.37 gain nothing new until they get a real pin (no pin, nothing
to compare), but the moment any seat's pin is written through this `--pin`
path, it is protected the same way belam now is.

**What it does NOT fix:** the belam.meter pin live on this box right now
predates this change and is a legacy bare-path pin with no generation stamped
in it, so it is NOT retroactively protected — there is nothing to compare
against. Protection starts the next time a generation calls `rotate.py meter
--pin <sessions>/<seat>.meter` to claim the seat. Confirmed live below.

## Evidence

**Red first** — reverted only the three-line generation-comparison block
(kept everything else, including the new test) and re-ran the new test:

    $ python3 -m pytest extensions/agi/tests/test_rotate.py -q -k seat_pin_refuses
    F
    AssertionError:
    assert 0 == 1
    1 failed, 55 deselected in 0.16s

Restored the fix, same test:

    $ python3 -m pytest extensions/agi/tests/test_rotate.py -q -k "seat_pin"
    ... 3 passed, 53 deselected

New tests added to `extensions/agi/tests/test_rotate.py`:
- `test_seat_pin_refuses_predecessors_generation` — pins seat `belam` as
  generation 1, advances the seat's handoff to generation 2 (rotation, pin
  never re-pointed — the exact defect measured live by Belam XI), asserts
  `rotate.py meter --seat belam` now exits 1 with an `ERR` naming both
  generations, never a silent number.
- `test_seat_pin_same_generation_reads_clean` — the matching case must NOT
  regress into a refusal.

Full engine suite, unchanged behaviour everywhere else:

    $ python3 -m pytest extensions/agi/tests/ -q
    2096 passed, 1 skipped in 122.55s

Live read from this session, unaffected because the live pin predates
generation-stamping (see "What it does NOT fix" above):

    $ python3 extensions/agi/bin/rotate.py meter --seat belam
    0.2147	214669/1000000 tokens	source=seat_pin	threshold=0.35

    $ cat .agi/sessions/belam.meter
    /home/ubuntu/.claude/projects/-home-ubuntu-work-agi/e6b3481a-a49f-4247-9397-24050b9fa958.jsonl

No `sessions/seats/belam.handoff.md` exists yet on this box, confirming the
seat has not been rotated through `rotate-self` since generation tracking was
introduced — there is no live case to demonstrate the refusal against outside
the test suite. `git diff --stat` at close: `extensions/agi/bin/rotate.py`,
`extensions/agi/tests/test_rotate.py` changed; no files added or deleted.

## Agent Notes
seat pin now stamps its writer's generation and a cross-generation --seat read is a loud ERR refusal (not a silent stale number), proved red-first; covers all eight config:seats rows via the shared resolve_transcript path, but the live belam.meter pin predates the stamp so it is not retroactively protected

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review, L3.41. Kept the kid verdict at inconclusive_lean_proved:70 rather than lifting it: the refusal path is genuinely proved (rotate.py:283 _parse_pin_record, :366 seat_pin-stale, :769 the ERR branch; test_seat_pin_refuses_predecessors_generation asserts exit 1 with BOTH generations named, and the same-generation test guards against over-refusing — 3 passed on re-run by the parent), but the claim the hypothesis actually asks about is that a meter read through a seat can NEVER be another generation as, and the live belam.meter pin is a legacy bare-path record with no writer stamped, so it is still unprotected today. The node says this plainly instead of hiding it, which is why it stays a lean and not a demote. Option 2 over option 1 is the right call and the reasoning given (re-pointing collapses into the successor claiming on first read, i.e. the same design plus an auto-fix) is sound. Unverifiable from here: the kid asserts it touched only rotate.py and its test, but the shared worktree diff also carries workflow.py from a concurrent parent, so authorship of that file is not attributable either way.
<!-- THOUGHT:END -->

ACCEPTED at 70, not demoted and not lifted. Diff and tests independently re-run by the parent. Residual gap the successor generation must close: the live pin predates generation-stamping, so belam is protected only from the next --pin write onward.
