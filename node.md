---
id: experiment:a00-10f3a2f6-16ba7a
mint_id: a97aaa415ee545baae86b5cd4be71c20
type: experiment
parents:
  - hypothesis:l4-a-failed-push-persists-the-pending-successor-key-and-the-next-push-completes-the-swap-and-one-record-join
next_edges: []
confidence: 0.4
edited_by: sensei-director
evidence_runs:
  - experiment:a00-10f3a2f6-16ba7a
loop: hypothesis:l4-a-failed-push-persists-the-pending-successor-key-and-the-next-push-completes-the-swap-and-one-record-join@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 5eecf8c260365b57
season: 2
title: A00 10f3a2f6 16ba7a
town: core
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-10f3a2f6-16ba7a

## Experiment

Goal: build the g15.26 claim (a)+(b) core on real bytes -- a failed push must
PERSIST the pending successor key (not drop it with the return string), and
the NEXT successful push of that row must COMPLETE the swap. Measured pre-fix
state first: `_apply_successor_key_gated` (rotate.py) on a `push: FAILED`
commit outcome returned the NOT-applied line and dropped `pending_key` (the
minted successor private key lived only in the rotation dict, nowhere on
fido). The falsifier "after a failed push the minted key exists nowhere on
disk" was live.

Implemented in `extensions/agi/bin/rotate.py`:
- NEW `_persist_pending_key(key_rotation, key_path)`: on push FAILED (row
  written AND committed naming the successor pubkey), writes the successor
  private key to `<sessions>/seats/<seat>.key.pending` (SEAT_KEY_MODE 0600,
  temp + os.replace) as JSON `{scheme,priv_hex,pub_hex,gen_after,minted_at}`;
  the return line names the pending path and keeps "NOT applied"+"deferred
  swap" so the existing deferred-test assertions are unchanged. Row-write /
  commit-failure paths still persist nothing (no successor pubkey reached a
  committed row).
- NEW `_complete_pending_key_swap(root, seat)`: after `_push_season_branch`
  reports `push: OK`, `_commit_spawn_row` calls it; a `.key.pending` whose
  `pub_hex` equals the seat's COMMITTED row pubkey (`git show HEAD`, fresh)
  atomically replaces `<seat>.key` with the pending private key, deletes the
  pending file, prints `key swap completed (deferred from gen N)`. Row naming
  the OLD pubkey -> pending left alone (still deferred). Absent pending file
  / gitless -> '' (never a failure).
- `.gitignore`: added `*.key.pending` (the pending swap holds a LIVE private
  key, never commit; defensive line beside the sessions/ seat-key area).

Ran the engine suite for the touched surface:
- `python3 -m pytest extensions/agi/tests/test_rotate.py extensions/agi/tests/test_seatsig.py -q` -> 207 passed
- `python3 -m pytest extensions/agi/tests/test_send.py extensions/agi/tests/test_heal.py -q` -> 295 passed

## Evidence

New tests in test_rotate.py:
- `test_rotate_successor_key_gate_persists_on_push_failure`: push FAILED ->
  `.key.pending` exists, mode 0600, shape {scheme,priv_hex,pub_hex,gen_after}
  matching the rotation dict; `<seat>.key` byte-identical; push-OK and
  row-write-FAILED cases persist NOTHING.
- `test_rotate_complete_pending_key_swap`: matching committed pubkey ->
  `key swap completed (deferred from gen 2)`, `<seat>.key` holds the pending
  priv, pending file removed; mismatched (old-pubkey) row -> "NOT completed"
  + "deferred", pending left, old key intact. Patches the TOP-LEVEL bin send
  module (rotate's local `import send` is not `agi.bin.send`).

Caveat -- clauses (c) (send.py signer prefers `.key.pending` when HEAD's row
matches it) and (d) (heal.py imports rotate's one `_record_join`; its own copy
not yet deleted) are NOT built this round. Those are separate behaviours:
(c) touches send's signature path, (d) is a heal/rotate accessor unification.
This experiment proves (a)+(b)+(their tests) on built bytes and closes the
primary falsifier (minted key exists on disk after failed push; later push
completes the swap).

## Agent Notes
Built+proved claim (a)(b): failed push now persists successor key to seats/<seat>.key.pending 0600; next successful push completes swap via _complete_pending_key_swap wired into _commit_spawn_row; .key.pending gitignored; 502 engine tests pass. (c) send signer pending-preference and (d) single _record_join NOT built.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DEMOTED by the Prime XV at mur-SL2.17 (wf_2144282d-658, digested 10:22Z, g17.1 note bf7881ad1), edited on the seat by sensei-director gen X: clause (b) was wired ONLY into _commit_spawn_row (rotate.py:6233), which on a rotate-self seat runs AFTER the pubkey already changed, so the :07 cron push and keygen --all-live (send.py:752 — the sole-caller grep missed it) complete nothing; the next rotate-self reads the stale gen-N key (10328-10333), key_history duplicates N and the pending N+1 is orphaned (10495-10497). The parent review that accepted a/b/e at lean 65 is in the grid history of this node. Fix minted as a g15 line: complete the pending swap at the ack, prepare and cron-push sites too, or before the row write, with a fixture that combines .key.pending with a rotate-self.
<!-- THOUGHT:END -->
