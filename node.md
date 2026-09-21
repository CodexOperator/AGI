---
id: experiment:a00-f0c20962-edea74
mint_id: ef84b25593e9407883fb261cabe9b0f5
type: experiment
parents:
  - hypothesis:l4-first-seating-tests-stub-the-real-tmux-list-windows-and-the-seating-base-block-and-alert-read-one-resolved-generation
next_edges: []
confidence: 0.8
evidence_runs:
  - experiment:a00-f0c20962-edea74
loop: hypothesis:l4-first-seating-tests-stub-the-real-tmux-list-windows-and-the-seating-base-block-and-alert-read-one-resolved-generation@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 79a670bc5cde2971
season: 2
title: A00 f0c20962 edea74
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-f0c20962-edea74

## Experiment

FIX-ONLY round on `hypothesis:l4-first-seating-tests-stub-the-real-tmux-list-windows-and-the-seating-base-block-and-alert-read-one-resolved-generation` (a g15.25 build claim). Measured the pre-fix state on this base, then implemented the missing pieces.

**Measured pre-fix state (`extensions/agi/bin/rotate.py`, this base):**
- Claims (c) and half of (b) had already landed in prior iterations: `_first_seating_announce` (:4003) already takes `generation` from its caller and keeps the `_seat_row_generation` read only as the `if generation is None:` fallback; `_seating_record_exists(root, seat, generation=...)` already takes a generation and compares `rec.get("gen_after") == generation`.
- LIVE still: **claim (b)** — `_compose_seating_base_block` (:4356) called `_seating_record_exists(root, seat)` with NO generation, so it checked gen 1 only; a re-seated seat at gen N with a gen-N record on disk read `record: none yet (never seated)`. 
- LIVE still: **claim (a)** — the two direct-announce tests (`test_first_seating_respawn_record_and_alert_carry_row_gen`, `test_first_seating_row_generation_zero_is_kept_as_zero`) called `rotate._first_seating_announce(..., tmux_session="t", live_names=[])` with `_successor_window_id` UNSTUBBED, so the suite ran a real `tmux list-windows` subprocess (box-dependent).

**Implemented:**
1. `_compose_seating_base_block` gains `generation: int | None = None`. When None it resolves `_seat_row_generation(root, seat)` ONCE (gen 1 stays the first-seating default for an absent/gen-less row, 0 kept as 0) and calls `_seating_record_exists(root, seat, generation=gen)` at THAT generation. The cmd_spawn caller (:1712) already holds `_rowgen`, so it now passes `generation=(_rowgen if root is not None else None)` — no second read.
2. New helper `_fs_stub_successor_window(monkeypatch, window_id="@3")` in `test_rotate_startup.py`: monkeypatches `rotate._successor_window_id` to a fixed @id (recording each consultation) and `rotate._join_successor` to a deterministic `found: False` (a fixed @id would otherwise trigger a real bounded join poll into `~/.claude/sessions`). Both direct-announce tests now call it and assert `_successor_window_id` was consulted.
3. New test `test_seating_base_block_checks_record_at_resolved_row_gen`: writes a gen-3 seating record, row gen 3, asserts base block reads `record: present` (the falsifier direction); complementary half asserts a stray gen-1 record must NOT mask an absent gen-3 record (reads `none yet`).

**Run:** `python3 -m pytest extensions/agi/tests/test_rotate_startup.py -q` → **92 passed**. Targeted `-q -k "first_seating or base_block or row_generation or respawn"` → 10 passed.

## Evidence

- `extensions/agi/tests/test_rotate_startup.py`: 92 passed, 0 failed (5.15s).
- No remaining unstubbed `_successor_window_id` call: grep shows only the helper (1768) and the two assert messages; the two direct `_first_seating_announce` calls (1891, 1940) are each preceded by `_fs_stub_successor_window`.
- `_compose_seating_base_block` callers: 2 sites in rotate.py (definition + cmd_spawn caller), both now generation-aware.

## Agent Notes
FIX-ONLY g15.25 round. Base block now checks _seating_record_exists at the resolved row generation (param generation, resolves once when None; cmd_spawn passes its _rowgen, no 2nd read); both direct-announce tests stub _successor_window_id (+_join_successor) so no real tmux subprocess or join poll; new base-block test covers the gen-N 'never seated' falsifier. test_rotate_startup.py 92 passed.
