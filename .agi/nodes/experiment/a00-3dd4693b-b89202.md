---
id: experiment:a00-3dd4693b-b89202
mint_id: f27cab2d961343dbabe58346edc07a9b
type: experiment
parents:
  - hypothesis:l5-spawn-mints-the-successor-key-under-the-row-name-not-the-renamed-seat
next_edges: []
confidence: 0.85
edited_by: a00-82f84cb0
evidence_runs:
  - experiment:a00-3dd4693b-b89202
line_ceiling: 40
loop: hypothesis:l5-spawn-mints-the-successor-key-under-the-row-name-not-the-renamed-seat@s2
model: deepseek/deepseek-v4.1-flash
probes:
  - {"conjunct": 1, "class": "wire", "cmd": "probe_prefix.py: the same wire fixture with the fix DISABLED (key_seat dropped)", "expected": "successor key at <new>.key", "observed": "<new>.key held the PREDECESSOR key; row pubkey was the successor -> cannot sign as the new seat", "result": "defect reproduced (test would fail)"}
  - {"conjunct": 1, "class": "gate", "cmd": "probe_gates.py: keyed row, rename target, NO predecessor key file", "expected": "_rotate_successor_key returns None (no keyless mint)", "observed": "None", "result": "pass"}
  - {"conjunct": 1, "class": "wire", "cmd": "pytest test_rotate_boundary_rename.py::test_rename_rotation_successor_signs_as_the_new_seat", "expected": "successor at <new>.key 0600, pub == row pubkey cell, predecessor preserved, sign as AGI_SEAT=new verifies", "observed": "pass; 942 passed over every rotate/rename/keygen test file", "result": "pass"}
  - {"conjunct": 1, "class": "wire", "cmd": "parent probe A: cmd_rotate_self with a staged rename; a wrapper records the key_seat kwarg actually passed to _rotate_successor_key", "expected": "key_seat == 'adv-new' and pending path ends adv-new.key", "observed": "key_seat=adv-new path=.../adv-new.key rc=0", "result": "pass"}
  - {"conjunct": 1, "class": "auth", "cmd": "parent probe B: after the renamed rotation, send._sign_line as 'adv-alive' (old) and as 'adv-new' (new)", "expected": "old name resolves NO key; new name signs and VERIFIES under the seats row pubkey cell", "observed": "old_key_exists=False; row.pubkey==pub(new.key); verify=True", "result": "pass"}
  - {"conjunct": 1, "class": "gate", "cmd": "parent probe C: stage present + a post-staging drift surface, then cmd_rotate_self", "expected": "boundary refuses (rc=2), stage intact, NO <new>.key written by the peek", "observed": "rc=2, stage exists, new.key absent", "result": "pass"}
  - {"conjunct": 1, "class": "wire", "cmd": "parent probe F (discriminator): same live call site with the fix DISABLED (key_seat dropped)", "expected": "the pre-fix defect returns: <new>.key holds the predecessor, row pubkey is the successor", "observed": "new_key_pub != row.pubkey and <old>.key exists -> defect reproduced", "result": "pass (the regression test discriminates a fix from its absence)"}
  - {"conjunct": 1, "class": "gate", "cmd": "parent probe G (residual): simulate push: FAILED after a rename rotation, then _complete_pending_key_swap as the NEW name and as the OLD name", "expected": "the deferred .pending swap can complete", "observed": "<new>.key.pending persisted but complete_as_new refuses ('committed row for adv-new still names the old pubkey'); complete_as_old finds no pending", "result": "FAIL (pre-existing sibling defect, named in the kid THOUGHT; queued as kid 2)"}
production_lines: 40
profile: balanced
role: kid
scaffold_hash: b07be2d0756d8e3d
season: 2
title: rename rotation mints the successor key under the new seat name and preserves the pre-rename key
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-3dd4693b-b89202

## Experiment

BUILD ROUND (goal:g15 — a g15 claim is a build order). Implemented the fix in
`extensions/agi/bin/rotate.py` and proved it on the built bytes.

**The mechanism, verified by reading the code (not trusted from the brief).**
At a rotation that also carries a post rename:

- `cmd_rotate_self` mints the successor key at L~18323, while `seat` is still
  the PRE-rename name; `_rotate_successor_key` computed
  `send._seat_key_path(root, seat)` and returned it in `pending_key["path"]`.
- The `(0.9)` RENAME BOUNDARY at L~18354 runs AFTER that mint and calls
  `_apply_staged`, whose surface table includes
  `sessions/seats/<old>* → <new>*` as `rename-file` actions. So the boundary
  MOVES the predecessor key `<old>.key` to `<new>.key`.
- `_apply_successor_key_gated` then writes the DEFERRED successor key to the
  OLD path, so `<old>.key` holds the fresh successor and `<new>.key` holds the
  predecessor. But the successor is spawned with `AGI_SEAT=<new>`, and `send`
  signs via `_seat_key_path(root, from_id)` — so it read `<new>.key`, the
  PREDECESSOR key, whose pub does not match the row's `pubkey` cell (which the
  same rotation wrote as the successor pub). Exactly the 22:43Z defect; the
  Prime had swapped the files by hand.

**The fix (40 production lines, `git diff --numstat` =
`40 3 extensions/agi/bin/rotate.py`; ceiling 40).**

1. `_rotate_successor_key(..., key_seat=None)`: the successor target is
   `key_seat or seat`, but the PREDECESSOR private key is still read from
   `seat`'s own path (so the retirement is signed, unchanged). `pending_key`
   now carries `pred_path` (set only when the target name differs) and
   `gen_from`.
2. `_apply_successor_key_pending`: when `pred_path` is set, the predecessor
   bytes are MOVED aside to `<key_path>.gen<from>-pre-rename` (0600 — the name
   the Prime used by hand) before the atomic replace, with a copy fallback if
   `os.replace` fails. Without `pred_path` the function is byte-identical to
   before.
3. `cmd_rotate_self`: PEEK the staged `<seat>.rename.json`'s `new` field before
   the mint (the same field `_apply_staged` reads and re-derives) and pass it
   as `key_seat`. A later boundary refusal still returns before any write, and
   the minted key is only ever written by the gated apply — so a refused
   rotation leaves no key anywhere.

All three constraints held: the retirement is still signed with the
predecessor key read before any replace; the `os.replace` stays deferred until
the one spawn-row write + one commit + push succeed (a failed row write/commit
leaves the predecessor file byte-identical, a failed push persists `.pending`);
and the boundary still does not write config, so the seats row keeps the OLD
name.

**`<old>.key` after the fix:** the boundary's `rename-file` action has moved it
to `<new>.key`; the gated apply then moves those bytes to
`<new>.key.gen<from>-pre-rename` and writes the successor to `<new>.key`. The
predecessor private key is therefore never destroyed and nothing that resolves
the old name loses a key. Without a rename there is no backup — `<seat>.key` is
replaced exactly as today, with the predecessor pub fact retained in
`key_history`.

## Evidence

Regression tests added to `extensions/agi/tests/test_rotate_boundary_rename.py`:

- `test_rotate_successor_key_mints_under_new_name_and_preserves_old` — unit:
  pending path is `<new>.key`, the predecessor file is untouched by the mint,
  the apply writes the successor at `<new>.key` (0600) and preserves the
  predecessor at `<new>.key.gen3-pre-rename` (0600).
- `test_rotate_successor_key_no_rename_is_unchanged` — the fix is a no-op
  without a rename, and writes no `*pre-rename*` file.
- `test_rename_rotation_successor_signs_as_the_new_seat` — WIRE PROOF through
  `cmd_rotate_self` with a keyed seat, a staged rename and a fake spawn seam:
  the successor key lands at `adv-new.key`, its pub equals the row's `pubkey`
  cell, the predecessor is preserved, and `send._sign_line(root, "adv-new", …)`
  returns a signature that VERIFIES under the row's pubkey — i.e. a process
  running with `AGI_SEAT=adv-new` can sign as that seat.

The wire test FAILS on the unfixed code: with `key_seat` dropped (the pre-fix
target name), `adv-new.key` holds the predecessor key (`priv == pred_priv`) and
the row's pubkey is the successor — the assertion `row.pubkey == pub(new.key)`
cannot hold.

Commands run (all pass):

```
python3 -m pytest extensions/agi/tests/test_rotate.py \
  extensions/agi/tests/test_rotate_boundary_rename.py \
  extensions/agi/tests/test_rename_post.py extensions/agi/tests/test_post_rename.py \
  extensions/agi/tests/test_rotate_own_root_rename.py \
  extensions/agi/tests/test_rotate_alert_two_tree.py -q
  → 398 passed, 1 xfailed
python3 -m pytest <every test_rotate*.py + test_*rename*.py + test_keygen*.py> -q
  → 942 passed, 1 xfailed
```

## Probes

Negative probes this run performed, with the refusal/result observed:

1. Fix disabled (`key_seat` dropped, the pre-fix name) on the same wire
   fixture — result: `new.key` priv == predecessor (`True`), `old.key` priv !=
   predecessor (`False`), row pubkey != predecessor pub. The defect reproduced;
   the regression assertions refuse it.
2. Rename staged, predecessor key file ABSENT — `_rotate_successor_key(…,
   key_seat="new")` returns `None`: no keyless mint, the moved gate still
   refuses.
3. Unkeyed row (no `pubkey`) with `key_seat` set — returns `None`.
4. A pending whose `pred_path` no longer exists — the successor is still
   written to `<new>.key` (0600) and the predecessor bytes are moved to
   `<new>.key.gen0-pre-rename`; no crash and no silent skip.
5. A keyed seat + staged rename with a dirty tree / no upstream — the rotation
   refuses (rc 3 at the prepare gate) and NOTHING is written: `old.key`
   byte-identical, `new.key` absent, no `*.gen*-pre-rename`, stage intact.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW VERSION (rewritten from scratch). The previous version recorded the kid's own measured probes and its build; this version adds the parent's independent probes and the review verdict. Why it differs: I read the changed bytes (git diff fe0fe6413..4df820a37), not the kid's result file; I re-ran the wire call site myself and, decisively, ran the fix-DISABLED discriminator (probe F) and the push-failure recovery probe (probe G). F confirms the regression test discriminates the fix from its absence; G confirms the kid's own caveat as a live, pre-existing defect in the deferred-swap path. The claim (mint under the new name on a rename) holds on all three probe classes; the residual is out of this claim's conjunct set and is carried forward as kid 2 rather than silently accepted.
<!-- THOUGHT:END -->

## Agent Notes
rename rotation now mints the successor key under the NEW seat name (peek the staged rename before the mint) and preserves the predecessor as <new>.key.gen<from>-pre-rename; no-rename path byte-identical; 40 production lines

PARENT REVIEW L5.16: accepted proved. Read the diff fe0fe6413..4df820a37 (rotate.py +40/-3, tests +137). Ran 7 independent probes (A wire, B auth, C gate, F pre-fix discriminator, G residual, E no-rename, D malformed) -- all pass except G, which confirms the residual the kid itself named: on a push: FAILED after a rename, <new>.key.pending is persisted but _complete_pending_key_swap refuses because the committed seats row still carries the OLD name (send._seat_row_in does not resolve the aliases table), so the deferred swap can never complete for a renamed seat. That is a pre-existing sibling defect (pre-fix the pending landed at <old>.key.pending and was likewise never read), not a conjunct of this claim; the claim's fix is real and discriminative (probe F). Queued as kid 2.
