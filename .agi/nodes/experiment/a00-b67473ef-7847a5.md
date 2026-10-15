---
id: experiment:a00-b67473ef-7847a5
mint_id: 0d7f54a7b46646ed9b93ff77fc4c4f17
type: experiment
parents:
  - hypothesis:l4-meter-pin-refuses-a-target-that-is-not-a-pin-and-prepare-prints-the-clear-line-that-clears
next_edges: []
confidence: 0.85
edited_by: a00-0171fd39
evidence_runs:
  - experiment:a00-b67473ef-7847a5
loop: hypothesis:l4-meter-pin-refuses-a-target-that-is-not-a-pin-and-prepare-prints-the-clear-line-that-clears@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 19bfda3f8c3ccf57
season: 2
title: "kid2: read-gen row-first justified at all 7 callers; vacuous clean fixture now asserts the pushed/unpushed captive"
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-b67473ef-7847a5

## Experiment

Kid 2 of the target: halves (3) `_read_generation` and (4) the vacuous prepare
fixture. Sibling kid 1 already landed (1)+(2) (cmd_meter pin guard, check-5
clear line) on disk; untouched here.

### (3) `_read_generation` row-first — DECISION: JUSTIFY, no code change

Function renders via `_generation_measured` (rotate.py L~2766): reads the
config:seats row generation first (`_seat_row_generation`, the documented
AUTHORITY — written at spawn by rotate-self, back-filled by the ack), handoff
header only as fallback. Grepped every `_read_generation(` call site — exactly
SEVEN (NOT the approximate 397/977/7291/8328/8333 in the brief; the read
moved with edits). Table (line = current rotate.py line):

| line | caller | what it reads the generation for | row-first right? |
|------|--------|--------------------------------|------------------|
| 432 | `resolve_transcript` | stale-pin compare: a gen-bearing pin's `written_gen` vs the seat's CURRENT occupant generation | YES — must compare against the truth, else a predecessor's stale pin reads as the successor's own and the refusal never fires |
| 1033 | `cmd_meter` --pin write | stamps `cur_gen\t<transcript>` into a fresh pin (the gen that owns this claim) | YES — must stamp the live occupant gen (the Prime's stale pin cur=11 vs pin 10 is this caller's stub proof); a stale handoff counter would re-stamp a lie |
| 2090 | `cmd_status` (row) | display `gen=` for the seat's row | YES — display should show the live row's authority, not a stale handoff |
| 2112 | `cmd_status` --seats | display `gen=` in the seats listing | YES — same display semantics |
| 7347 | `cmd_next` | startup template gen placeholder = current + 1 | YES — next gen must continue from the live occupant gen; row is the spawn record |
| 8402 | `cmd_rotate_self` chain seat | `gen_before` fallback when no chain numeral window is live | YES — the fallback only fires for a fresh prime; row (or handoff if no row) is the only source LEFT; row-first is strictly more accurate (asserted in test_rotate_handover::...gen_before_from_numeral) |
| 8407 | `cmd_rotate_self` plain seat | `gen_before` = current, then `gen = gen_before + 1` | YES — rotation must advance from the live occupant gen; a stale handoff counter is exactly the `0 -> 8` bug the chain fix (L4.122) already named |

Justification, uniform: EVERY caller wants the seat's CURRENT occupant
generation. The row is the single authoritative source for that (spawn-written,
ack-back-filled); the handoff header is a fallback for a seat with no live row.
Row-first therefore rescues the prepare captives (5/6), the pin stamp (1033)
and the rotate/next gen advance (7347/8402/8407) from a possibly-stale handoff
counter, and degrades to the very same fallback a handoff-only read would have
used in every measured case — no caller loses resolution it previously had.
Scope-back not needed: no caller prefers the handoff over the row, and a
row-vs-handoff divergence is precisely the stale-rotation condition the row is
meant to win. FALSIFIER (keeps every caller's current behaviour green): the
full rotate + smoke suite stays green — 241 passed, 1 skipped (network-seam
skip) across test_rotate.py, test_rotate_prepare.py, test_bin_help_smoke.py,
test_rotate_handover.py.

### (4) The vacuous prepare fixture — FIXED

Fixture: `test_prepare_clean_fixture_exits_0` (test_rotate_prepare.py).
Vacuous assertion: `_no_git(monkeypatch)` then `assert rc == 0` + `assert
"[ok]" in out`. With `_no_git`, `_prepare_checks` check 1 read `rev-list
--count @{u}..HEAD` as None -> branch unmeasured -> `[ok] unpushed commits
(unmeasured)`. So the clean fixture passed whether the seat was pushed, had 1
unpushed commit, or had 50 — the unpushed captive never figured in the pass at
all (SL3.02 residue: the `(None or 0) > 0` gate became a named-ok
`unmeasured` branch, and the clean fixture rode that branch to false ok).

Fix (same function, now asserts the REAL outcome, flipping the captive in the
test not by reading it):
- clean state is MEASURED-pushed: inject branch `feature/clean`,
  `@{u}..HEAD: ["0"]`, empty porcelain, `HEAD..origin/season/s2: ["0"]`;
  assert rc==0 and `[ok] unpushed commits`, `[ok] dirty tree`, `[ok] behind
  origin/season/s2 (0)`, no `[BLOCK]`.
- FALSIFIER turn: MUTATE the captive in the test — set `@{u}..HEAD: ["1"]` on
the otherwise-identical fixture — and assert rc==3 with `[BLOCK] unpushed
commits`. Flipping the captive flips ok<->BLOCK, proving the fixture now
asserts the unpushed captive's real measured outcome.

No other prepare test is vacuous on its unpushed captive (audited each rc==0
test: the others inject a real `@{u}..HEAD` count coupled to their scenario).

## Evidence

- Seven grep-confirmed call sites: rotate.py 432, 1033, 2090, 2112, 7347,
  8402, 8407 (all seven read via `_generation_measured` row-first
  handoff-fallback).
- Baseline before edit: 241 passed, 1 skipped (test_rotate.py +
test_rotate_prepare.py + test_bin_help_smoke.py + test_rotate_handover.py).
- After part (4) edit, same suite: 241 passed, 1 skipped.
- `pytest test_rotate_prepare.py -k clean_fixture`: 1 passed (the fixed
  fixture, both the measured-ok and the mutated-BLOCK turns).

## Agent Notes
kid2 (3)+(4): read_gen row-first JUSTIFIED at all seven callers (432/1033/2090/2112/7347/8402/8407) - every caller wants the current occupant gen, row is the authority, suite stays green (241 passed); vacuous clean-fixture test_prepare_clean_fixture_exits_0 now asserts the unpushed captive's real outcome (measured-pushed -> ok, mutate @{u}..HEAD to 1 -> BLOCK).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review SL4.01: ACCEPTED as proved for (3)+(4).

(1) WHAT THE INSTRUCTION SAID: the target hypothesis named "kid 2 = (3)+(4)" — _read_generation row-first must be JUSTIFIED per caller (a seven-line table on the experiment node) or scoped back to the prepare captives behind a named helper; and the vacuous prepare fixture must assert the captive's REAL outcome, flipping pass/fail with the captive.

(2) WHAT THE MACHINE ACTUALLY DOES — I ran it, not the report: grep -n "_read_generation(" rotate.py returns EXACTLY seven call sites, at 432, 1033, 2090, 2112, 7347, 8402, 8407 — the kid's table cites those exact lines (the brief's approximate numbers were stale, and the kid re-grepped instead of copying them). `_read_generation` (L2793) delegates to `_generation_measured`, which is row-first with handoff fallback, and the diff --cached --stat shows kid 2 changed ZERO code lines in rotate.py: the (3) deliverable is the justification table, which the hypothesis explicitly permits. My own suite run: test_rotate.py + test_rotate_prepare.py + test_bin_help_smoke.py + test_rotate_handover.py = 241 passed, 1 skipped. The (4) fix is in the diff: test_prepare_clean_fixture_exits_0 now injects a measured-pushed clean map and then MUTATES @{u}..HEAD to ["1"] on the same fixture, asserting rc==3 and [BLOCK] unpushed commits — so the fixture flips with the captive, not with _no_git.

(3) THE NEAR MISS: a kid could have satisfied "(3)" by asserting "row-first is fine" in prose without touching a single call site, or by scoping to a named helper and silently changing the six non-prepare callers' behaviour. The kid avoided both: it enumerated every call site and argued each one WANTS the current occupant generation (the stamp at 1033 and the gen+1 advance at 7347/8402/8407 are the ones the Prime's stale pin cur=11 vs pin 10 actually breaks). The residual weakness, recorded not demoted: the justification is reasoning, not a per-caller test, so a future handoff/row divergence at, say, 2090 (display-only) is argued rather than asserted.

(4) NO DEVIATION: no guard lowered; sibling kid 1's cmd_meter path guard and check-5 clear line were left untouched, as the brief required.
<!-- THOUGHT:END -->
