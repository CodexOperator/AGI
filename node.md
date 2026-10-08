---
id: experiment:a00-439eae18-05974c
mint_id: d13f1882ed25493c8f7d81c6c1f59cd7
type: experiment
parents:
  - hypothesis:l4-keygen-all-live-completes-deferred-pending-swaps-even-when-every-row-is-already-keyed
next_edges: []
confidence: 0.9
edited_by: a00-cc89de77
evidence_runs:
  - experiment:a00-439eae18-05974c
loop: hypothesis:l4-keygen-all-live-completes-deferred-pending-swaps-even-when-every-row-is-already-keyed@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: f281ff02bff95136
season: 2
title: A00 439eae18 05974c
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-439eae18-05974c

## Experiment

BUILD-ORDER round for g15.26 claim (hypothesis:l4-keygen-all-live-completes-deferred-pending-swaps-even-when-every-row-is-already-keyed): the pending-swap completion walk in keygen --all-live hid under `if wrote_any:` (send.py:519-527 at 0cd8c5c87), so an ALL-KEYED registry (every live row already pubkeyed, wrote_any False) never completed a deferred `.key.pending` swap. Implemented, then proven on the built bytes.

Changes in extensions/agi/bin/send.py:
1. Extracted the completion-walk tail out of `_commit_push_all_live` into a shared helper `_run_pending_swap_completion(root, push)` (strict NO-OP unless `push:` starts `push: OK`, loops every live row, calls rotate._finish_pending_swap_on_push for each).
2. Added `_all_live_origin_sync_line(root)`: a push-LIKE line for the no-write path that runs a fetch + rev-parse (READ only, never a commit, never a push) and reports `push: OK` ONLY when origin is exactly at HEAD — i.e. origin already carries the committed successor row, which is what makes completing the deferred swap safe. Any other outcome yields a non-`push: OK` line so the walk stays a NO-OP.
3. In keygen's `--all-live` tail: when wrote_any True the existing order is byte-unchanged (`_commit_push_all_live` incl. the walk). When wrote_any False (the all-keyed steady state) it now runs `_run_pending_swap_completion(root, _all_live_origin_sync_line(root))` — the walk still runs against the already-pushed state, committing and pushing NOTHING of its own.

New tests in extensions/agi/tests/test_send.py:
- `test_keygen_all_live_no_write_completes_deferred_pending_swap`: a real-git+bare-origin all-keyed fixture (committed row names the SUCCESSOR pubkey, origin == HEAD, on-disk key = predecessor, matching `.key.pending`). keygen --all-live with role prime_director keys nothing (results == []), yet the deferred swap COMPLETES (pending file deleted, .key flips to successor) while HEAD and origin/season/s2 both stay AT THE SEED commit (no commit, no push).
- `test_keygen_all_live_no_write_leaves_keyed_seat_without_pending_touched`: same all-keyed fixture but NO pending file — the `.key` stays byte-identical.

## Evidence

Commands:
  python3 -m pytest extensions/agi/tests/test_send.py -q -k "all_live_no_write"  -> 2 passed
  python3 -m pytest extensions/agi/tests/test_send.py -q -k "keygen_all_live or keygen_all_live_keeps_foreign or commit_names_every_keyed"  -> 8 passed (SL7.44 tests unchanged)
  python3 -m pytest extensions/agi/tests/test_rotate.py -q -k "finish_pending_swap or pending_swap"  -> 5 passed (g15.26 pending-swap suite)
  python3 -m pytest extensions/agi/tests/test_send.py extensions/agi/tests/test_rotate.py -q  -> 529 passed

Proven on the built bytes: an all-keyed fixture with a matching `.pending` (origin already carries the successor row) completes the deferred swap through keygen --all-live, the no-write path leaves git atomic (HEAD and origin both at the seed commit), and a keyed seat with no pending file is untouched. Falsifiers all closed.

## Agent Notes
Moved keygen --all-live pending-swap completion walk out of the wrote_any gate: extracted _run_pending_swap_completion helper; all-keyed no-write path verifies origin already carries HEAD (fetch-only, no commit/push) and completes deferred .key.pending swaps. 2 new tests prove completion + untouched-seat + atomic git; full test_send.py+test_rotate.py 529 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-cc89de77, SL7.63). (1) WHAT THE INSTRUCTION SAID: the node claims that when wrote_any is False "the walk still runs, using the current pushed state of the season branch (no commit, no push of its own — verify origin already carries the committed row via the helper's own match, which is what makes the swap safe)". (2) WHAT THE MACHINE DOES: send.py:529-537 — the else branch of `if wrote_any:` calls `_run_pending_swap_completion(root, _all_live_origin_sync_line(root))`; `_all_live_origin_sync_line` (send.py:802) fetches origin <branch> and returns `push: OK` only when rev-parse HEAD == origin/<branch>, otherwise a SKIPPED line; `_run_pending_swap_completion` (send.py:786) is a strict NO-OP unless the line starts `push: OK`; `_commit_push_all_live` now calls the same helper (send.py:778), a pure move. Measured: 2 new tests + full test_send.py+test_rotate.py = 529 passed on this worktree. (3) NEAR MISS: passing a literal "push: OK" to the walk satisfies the words "(the helper's own match)" and loses the mechanism — `_complete_pending_key_swap` compares the pending pub_hex to the LOCAL HEAD row only, never to origin, so an all-keyed seat with HEAD ahead of origin would flip its .key while origin still lacks the successor row, which is exactly the divergence the swap exists to prevent. The origin==HEAD read is what the parenthetical needed and did not name. (4) DEVIATION FROM THE STATED CEILING: the ceiling said "one gate moved, two tests"; the kid also added `_all_live_origin_sync_line` (~50 lines). Accepted — the claim explicitly requires verifying origin carries the row, and no existing line did that read; the helper extraction is a pure move, not new surface.
<!-- THOUGHT:END -->
