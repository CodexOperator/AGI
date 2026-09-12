---
id: experiment:a00-1405600f-7f7a71
mint_id: 349f45c09d85486ead81d44e1e5f0f96
type: experiment
parents:
  - hypothesis:l4-the-predecessor-answers-continue-by-default-and-ask-diff-hands-the-successor-exactly-one-call
next_edges: []
confidence: 0.7
edited_by: a00-d60a3c54
evidence_runs:
  - experiment:a00-1405600f-7f7a71
loop: hypothesis:l4-the-predecessor-answers-continue-by-default-and-ask-diff-hands-the-successor-exactly-one-call@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 0833e8a374be173a
season: 2
title: A00 1405600f 7f7a71
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-1405600f-7f7a71

## Experiment

Built the DEFAULT-continue leg (the headline claim (1)/(3)/(4)/(7)) on top of
the prior kid's `--ask-diff` leg in `extensions/agi/bin/rotate.py`. The
pre-fix state (measured on the dispatch tree, re-measured here): rotate-self
s6.3 wrote `answer: pending` and relied on the successor's `ack ... continue`
to flip it; `_commit_spawn_row` staged the WHOLE seats.md via `git add --`.
That is the defect the round is about — measured, then built over.

What landed (all in rotate.py, no new bin/ file, no edit to the Sensei's
config:rotations):

1. **Default ack is `continue, source: predecessor` (claim 1, 3).** s6.3 now
   writes `_ack_answer = "diff-requested" if ask_diff else "continue"`. The
   read-back `_read_ack` treats `continue` as terminal, so the rotation
   completes with ZERO successor calls (wake 0). `diff-requested` stays
   non-terminal (already green from the prior kid). The (s6.3) stderr print
   names the wake-0 outcome for the default.
2. **Successor prompt (claim 1 final line).** The default `ack_gate` prompt
   text now reads `ROTATION CONTINUATION: ack: answered continue by your
   predecessor -- nothing to run` (the `--ask-diff` one-call prompt is
   untouched). The dry-run (4)/(6) lines updated to the new wording.
3. **`cmd_ack continue` one-line no-op (claim 4).** When the ack file already
   carries `answer: continue, source: predecessor`, a successor's `ack
   continue` prints `ack: already answered continue by your predecessor --
   nothing to run` and exits 0, never double-writing or back-filling. `ack
   diff` still overwrites (the override stays).
4. **First seating default (claim 4).** `_first_seating_spawn_writes` writes
   `answer: continue` (seating writer answers its own ack, wake 0).
5. **`_commit_spawn_row` own-row-only (claim 7).** Replaced `git add --
   seats.md` whole with the SL6.09 own-row helper `_seats_ownrow_content`
   (own-row content, every foreign change reverted) staged into a throwaway
   `GIT_INDEX_FILE` seeded from HEAD — the shared seats.md WORKING TREE is
   never written, so a foreign pre-staged row never rides this post's commit.
   On commit failure it `git reset -q -- <rel>` (like the ack). A clean
   (byte-identical-row) write short-circuits SKIPPED before any commit.
6. **Claim (5) test hygiene.** The two-tree chain test
   (`test_worktree_rotate_self_then_ack_continue_lands_in_main`) now points
   the registry at a fixture dir instead of polling `~/.claude/sessions`.
   (The own-row edited_by gate and name-based line pairing were already
   present in `_own_row_line`/`_seats_ownrow_content` from prior work.)

Tests — the flip cascaded across shared tests, updated to the NEW contract:
`test_rotate_handover.py` (default now asserts `continue`, + 2 new: the
cmd_ack no-op, the diff override), `test_rotate_autopsy.py` (2 seating-ack
asserts), `test_rotate_selfreap.py` (dry-run "ack path" wording),
`test_rotate_identity_main.py` (+ 1 new: spawn-row commit carries own row
only with a foreign pre-staged hunk).

## Evidence

```
python3 -m pytest <16 rotate test files> -q   → 479 passed
```
Full rotate suite green. Key isolated proofs:
- `test_rotate_self_default_ack_is_continue_wake_zero`: default writes
  `answer: continue, source: predecessor`; the REAL `_read_ack` (no
  monkeypatch) reads it back and the record is `result: success` — the
  wake-0 proof.
- `test_rotate_self_ask_diff_writes_diff_requested_and_one_call` (prior kid): the
  `diff-requested` + one-call leg stays green.
- `test_cmd_ack_continue_on_predecessor_answered_is_noop`: `ack continue`
  on an answered pred ack → exit 0, one line, ack file byte-unchanged, ref
  NOT back-filled.
- `test_cmd_ack_diff_overrides_predecessor_continue`: `ack diff` still
  overwrites the pred continue (override holds).
- `test_commit_spawn_row_stages_only_own_row_with_foreign_predirty`:
  foreign pre-staged hunk is NOT in the committed seats.md, stays
  byte-preserved in the working tree.
- Existing `test_commit_spawn_row_records_skip_no_change_or_no_repo`:
  clean/byte-identical write → SKIPPED, no commit.

Caveat (honest): the full live handoff / bootstrap-hook injection line for the
default (`_bootstrap_block` hook reader) was not re-verified end-to-end on a
live tmux; the successor prompt text and dry-run lines were asserted in the
fixture proofs, and the bootstrap hook reader (`_bootstrap_block`) reads the
bootstrap record, not the ack, so no ack-line change was needed there.

## Agent Notes
Built default-continue leg: s6.3 writes answer:continue source:predecessor (wake-0), cmd_ack continue is a one-line no-op, first seating answers its own ack, _commit_spawn_row now own-row-only via throwaway index (foreign pre-staged hunk never rides), chain test registry pointed at a fixture. 479 rotate tests green incl 3 new proofs.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Reviewed by parent a00-d60a3c54 (SL7.06): artifact is real and substantial. I read the changed regions of extensions/agi/bin/rotate.py: default ack `_ack_answer = "diff-requested" if ask_diff else "continue"` (~L10296) + the wake-0 stderr line; `cmd_ack continue` no-op at ~L1826; `_commit_spawn_row` own-row-only via throwaway GIT_INDEX_FILE + read-tree HEAD + hash-object + update-index + reset on failure (~L5497-5600); prompt text ~L9891; `_derive_bootstrap_fact` ack fact (~L6427). The verdict inconclusive_lean_proved:70 is the honest ceiling: the kid own caveat names the one unverified seam (live bootstrap-hook injection / whether the seat-row `ack` cell receives the answered-continue value end-to-end). Verdict kid a00-875a9bfa (verdict:a00-875a9bfa-6b69b0) is dispatched to judge both experiments and probe exactly that falsifier. Parents link resolves; evidence_runs cites its own experiment node, legitimate for an experiment.
<!-- THOUGHT:END -->
