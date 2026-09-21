---
id: experiment:a00-ab8d416a-f38771
mint_id: e12df05721ab40bd910cdfc62fb88202
type: experiment
parents:
  - hypothesis:l4-the-successor-key-swap-waits-for-the-push-and-a-recovery-record-still-yields-the-join
next_edges: []
confidence: 0.8
edited_by: a00-8f0f4ffa
evidence_runs:
  - experiment:a00-ab8d416a-f38771
loop: hypothesis:l4-the-successor-key-swap-waits-for-the-push-and-a-recovery-record-still-yields-the-join@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: c713c352df6f84ae
season: 2
title: A00 ab8d416a f38771
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-ab8d416a-f38771

## Experiment

Built mur-SL2.13 clause (4) (the SL7.06 harvest) of `hypothesis:l4-the-successor-key-swap-waits-for-the-push-and-a-recovery-record-still-yields-the-join` — the own-row commit left write.py's node-level `edited_by` restamp UNSTAGED, so MAIN read `M seats.md` after every keygen/spawn-row write.

THE GAP (reproduced first, on the built bytes): `keygen` mints the key and writes its row through `write.submit` on `config:seats`, which restamps the whole-node FRONTMATTER provenance line (`edited_by: <actor>`) as part of the SAME write. The own-row cut `_own_row_line` keyed that line ON THE SEAT NAME (`edited_by: <seat>`), but write.submit writes the WRITER'S RESOLVED ACTOR (the dispatch agent id, e.g. `a00-ab8d416a`) — never the seat name — so the frontmatter line fell outside the own-row content and got REVERTED to HEAD by `_seats_ownrow_content` while the working tree kept it, leaving seats.md dirty. Reproduced: the own-row commit landed the `pubkey` cell correctly, yet `git status --porcelain` read `M .agi/nodes/.geometry/seats.md`.

THE FIX (one predicate, shared by gate + commit-cut) — chosen option (a) of the claim, "carry the writer's own edited_by stamp in the same own-row commit", because the whole-node provenance write IS part of the same write that produced the own row, and carrying it keeps the tree clean without losing provenance (option b, "stop restamping", would touch write.py — out of scope — and drop a meaningful audit field): `_own_row_line` (rotate.py:5297) now recognizes the top-level YAML frontmatter stamp BY VALUE-INDEPENDENT POSITION — a new `_is_frontmatter_edited_by(line)` matches a line that begins `edited_by: ` (accepting the `+`/`-` diff prefix `_diff_owns_row` passes, so the ack GATE and the commit cut read the same predicate). A FOREIGN row's `"edited_by": ...` cell is quoted JSON inside an indented `  - {...}` row line, which never starts `edited_by: ` — so a foreign edited_by-only restamp is still never bundled (invariant 1, `test_ack_foreign_edited_by_only_restamp_not_committed` stays green). `_seats_ownrow_content` still pairs rows by the `name` CELL not by index (invariant 2).

EDIT-TOOL shape ref: `_own_row_line` + new `_is_frontmatter_edited_by` in rotate.py; strict-xfail mark removed from `tests/test_send.py::test_keygen_commits_and_pushes_own_row_to_bare_remote`.

## Evidence

Pre-fix repro (built bytes): keygen → `push: FAILED` (bare fixture) but `spawn_row_commit: committed` landed the row; `git status --porcelain` = ` M .agi/nodes/.geometry/seats.md`; `git diff` showed HEAD with the `pubkey` row but the working tree ADDED `edited_by: a00-ab8d416a` above `seats:` — the exact falsifier clause (4) named.

Post-fix: the same repro's `status --porcelain` is EMPTY and `diff` is EMPTY (the frontmatter stamp now rides the own-row commit). The strict xfail XPASSes and the mark is removed.

`pytest tests/test_send.py -k "test_keygen_commits_and_pushes_own_row_to_bare_remote"` → 1 passed (was 1 xfailed).
`pytest tests/test_send.py tests/test_rotate_handoff_driven.py tests/test_rotate_handover.py` → 307 passed.
`pytest tests/test_rotate.py` → 182 passed (incl. `test_ack_foreign_edited_by_only_restamp_not_committed`, the paired foreign-row gate invariant).
`pytest tests/test_rotate_identity_main.py tests/test_after_join_service.py tests/test_rotate_recover.py tests/test_heal_seats.py` → 54 passed (incl. `test_worktree_rotate_self_then_ack_continue_lands_in_main`, the two-tree fixture-dir invariant — registry points at a `reg-fixture` dir, never `~/.claude/sessions`).
(The lone `tier-gate: ... pid=1459751 (dead) -- skipped` line is a pre-existing phantom-running-record notice, not a failure.)

Why (chosen of the claim's two options): CARRY the stamp — write.submit's whole-node frontmatter `edited_by:` is produced by the same write that owns the row, so it belongs in the own-row commit and the tree stays clean; STOP-RESTAMPING would shed a meaningful audit field and live in write.py (out of SCOPE: rotate.py + test_send.py only).

## Agent Notes
mur-SL2.13 clause (4): `_own_row_line` now owns the top-level `edited_by:` frontmatter stamp by value-independent position (new `_is_frontmatter_edited_by`), so the writer's resolved-actor restamp (id, not seat name) rides the own-row commit and MAIN is clean after every keygen/spawn-row write. Strict xfail removed and XPASSed. Foreign-row JSON `"edited_by"` never matches (stays ignored); rows pair by name; two-tree test uses a fixture registry dir. 544+ tests green across send/rotate/handoff/handover/identity/after_join/recover/heal_seats.

## Agent Notes
Built mur-SL2.13 clause (4): _own_row_line now owns the top-level frontmatter 'edited_by:' stamp by value-independent position (new _is_frontmatter_edited_by), so the writer's resolved-actor restamp rides the own-row commit and MAIN is clean after keygen/spawn-row. Strict xfail removed and XPASSed; foreign-row JSON edited_by still ignored; rows pair by name; two-tree test uses fixture registry dir. 544+ tests green.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Reviewed by parent a00-8f0f4ffa (SL7.09). I read the built bytes: `git diff HEAD -- extensions/agi/bin/rotate.py` adds `_is_frontmatter_edited_by` (strips an optional `+`/`-` diff prefix, matches `edited_by: ` by value-independent position) and `_own_row_line` now returns `name_cell in line or _is_frontmatter_edited_by(line)`, so the own-row gate and the commit cut read the same predicate. `git diff HEAD -- extensions/agi/tests/test_send.py` removes the strict-xfail mark from `test_keygen_commits_and_pushes_own_row_to_bare_remote`. I ran it myself: `pytest test_send.py -k "test_keygen_commits_and_pushes_own_row_to_bare_remote or foreign_edited_by"` -> 1 passed, 258 deselected (no more xfail), and `pytest test_send.py test_rotate.py test_rotate_recover.py test_after_join_service.py` -> 470 passed. (1) THE INSTRUCTION SAID: carry the writer's own `edited_by` stamp in the same own-row commit (or stop restamping on a self-row write) -- say which. (2) THE MACHINE ACTUALLY DOES: it carries the stamp, choosing option (a), and the reason is documented: the whole-node frontmatter write is produced by the SAME write.submit that owns the row, so it belongs in the own-row commit; option (b) would edit write.py, out of the claim's scope. The predicate matches by POSITION not by the seat name, because write.submit restamps the resolved ACTOR id, not the seat name -- keying on `edited_by: <seat>` is exactly the bug. (3) THE NEAR MISS: keeping the old `f"edited_by: {seat}" in line` and just changing the xfail would have satisfied the words while the restamp still fell outside the cut for every writer whose actor is not the seat name (the normal case); the position-based predicate is what actually closes it. (4) Honest ceiling: clause (4) is built and the strict xfail removed, and the paired invariants hold (foreign JSON `\"edited_by\"` never matches; rows pair by name; the chain test uses a fixture registry dir). What remains of the target is the mandatory TWO-TREE alert fixture for clause (2) and the deferred-swap persistence/completion -- hence inconclusive_lean_proved:80, not proved.
<!-- THOUGHT:END -->
