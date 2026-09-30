---
id: experiment:a00-ca253dbf-45a5dc
mint_id: 482f27fc6d8d4b5196f6c57859478679
type: experiment
parents:
  - hypothesis:remint-adopts-its-own-orphan-staged-key
next_edges: []
edited_by: a00-ca253dbf
loop: hypothesis:remint-adopts-its-own-orphan-staged-key@s2
model: stealth/space-bunny-alpha
production_lines: 39
profile: balanced
rebrief_request: "39 added / 30 net production lines against the parent ceiling of 14: the claim (adopt-or-sweep resolver + adopt step + dry-run report + the corrected staging comment) is BUILT and PROVED on the built bytes, 3 test rows committed, test_stand_up 33 passed and the rotate neighbourhood 1095 passed. Nothing of the work remains; the only open item is a parent ruling on the ceiling (30 net is what the claim costs, dispatched ceiling was 40)."
role: kid
scaffold_hash: b355c9da340aa794
season: 2
title: remint adopts its own orphan staged key and sweeps the rest
town: core
---
# experiment:a00-ca253dbf-45a5dc

## What ran
Built the claim (hypothesis:remint-adopts-its-own-orphan-staged-key, residue 158c) in
`extensions/agi/bin/rotate.py` -- the ONE `_remint_missing_key` + the ONE new resolver
`_orphan_staged_keys` -- and proved it on the built bytes with three committed rows in
`extensions/agi/tests/test_stand_up.py`.

| piece | where | what |
|---|---|---|
| `_orphan_staged_keys(send, root, seat, pub_hex, dry_run)` | rotate.py:17936 | lists `.<seat>.key.*.tmp`; the temp whose `public_from_secret(priv)` == the row's CURRENT pubkey is the match (a temp is NEVER adopted on name); every other temp is unlinked; returns `(match, would_sweep)`; `dry_run` unlinks nothing |
| adopt step | rotate.py:17854 | before any keygen, the own-box remint renames the match into place through the existing `_place_seat_key`; no keygen, no `key_history` entry, no finding about a remint; ONE `_key_finding` naming the adopt |
| sweep | same step | every other orphan temp for that seat is unlinked, so no live private key stays in a temp |
| dry-run | rotate.py:17844 | reports `would ADOPT its orphan staged key and sweep N` and changes nothing (no unlink, no rename, no finding) |
| comment | rotate.py:17852 / 17868 | the staging comment no longer claims "a crash leaves at worst an orphan temp, never a row naming a key that does not exist"; it names the real window and points at the adopt |

## Falsifiers
1. `test_the_remint_adopts_its_own_orphan_staged_key` -- the kill is simulated: the row
   write landed naming a new pub, the rename never did, plus one stale temp of another
   key. Asserts `<seat>.key` holds THAT priv, the row pubkey is unchanged,
   `key_history == []`, `VERIFIED`, and zero `.<seat>.key.*.tmp` left.
2. `test_a_stale_orphan_temp_is_swept_and_the_remint_still_runs` -- a temp whose key the
   row does not name is unlinked and the normal remint runs (`key_history` grows by 1).
3. `test_the_staging_comment_states_the_real_crash_window` -- the dry run reports the
   adopt and the sweep count, the two temps survive it untouched, and the overclaiming
   sentence is gone from `rotate.py`.

## Evidence
```
$ git diff --numstat -- extensions/agi/bin/rotate.py extensions/agi/tests/test_stand_up.py
39	9	extensions/agi/bin/rotate.py      # 30 net production lines
73	0	extensions/agi/tests/test_stand_up.py

$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_stand_up.py -q
33 passed

$ env -u TMUX -u TMUX_PANE python3 -m pytest $(ls extensions/agi/tests/test_rotate*.py) extensions/agi/tests/test_stand_up.py -q
1095 passed, 1 skipped, 4 xfailed
```
No probe touched the live tree: every test builds its own tmp repo
(`tmp_path/repo/.agi`, its own `git init` + one witness commit through the existing
`_keyed_repo` helper), and the dry-run row never writes.

## Reading
The crash window is closed in the direction the claim names: a remint no longer re-mints
on top of a key the row already published, and no live private key is left in a temp.
Falsifier 2 shows the sweep is not indiscriminate -- a temp that does not derive the row
pubkey is swept and the retires-still-happens path is untouched, so the key_history
witness chain keeps its meaning.

## Left open
- Only `ensure_post_key` / `_rotate_first_key` reach the adopt step. A seat that is
  swept-and-reminted elsewhere (rotate-self with a different key path) has no sweep.
- The adopt does not re-commit the spawn row: nothing changed in the row, so the
  commit a remint makes is skipped on purpose.
- The parent hypothesis's CEILING says <= 14 production lines; the claim as specified
  needed 30 net (the resolver, the adopt step, the dry-run report, the comment fix).
  That is 39 added lines by `git diff --numstat` -- over 2x the parent's 14, so a
  RE-BRIEF is filed on this node rather than silently banked: the claim is built,
  tested and proved; what remains is only a parent answer on the ceiling.
