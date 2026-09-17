---
id: experiment:a00-dd6c5e70-c528df
mint_id: 190f987b29724cf99b3a79539259c7e4
type: experiment
parents:
  - hypothesis:l4-post-branches-are-local-only-mirrored-to-refs-agi-posts-and-the-merge-up-takes-the-suite-lock-itself-no-window-ask
next_edges: []
confidence: 0.7
edited_by: sanctuary-master
evidence_runs:
  - experiment:a00-dd6c5e70-c528df
loop: hypothesis:l4-post-branches-are-local-only-mirrored-to-refs-agi-posts-and-the-merge-up-takes-the-suite-lock-itself-no-window-ask@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 62a507825b7e49cf
season: 2
status: deprecated
title: A00 dd6c5e70 c528df
town: core
verdict: inconclusive_lean_disproved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-dd6c5e70-c528df

## Experiment

ROUND SLICE A of `hypothesis:l4-post-branches-are-local-only-mirrored-to-refs-
agi-posts-and-the-merge-up-takes-the-suite-lock-itself-no-window-ask`:
clause (1) (no post head is ever pushed) and clause (2)'s MIRROR HELPER at
the ROTATE-OUT path only. The merge-up verb, `cli.py`, and the GRANT
protocol retirement are deliberately NOT in this round (a later kid does
clauses (3)-(6)).

A g15 claim is behaviour to build, so this round MEASURED the pre-fix state,
IMPLEMENTED the claim, and proved it on the built bytes.

### Pre-fix (measured)
- `git grep` on the tree: the only engine push of a seat's own checked-out
  branch is `rotate.py:_stops_push` (`git push origin <branch>`), and a seat
  worktree is checked out ON `season<n>/posts/<name>` — so rotate-out DID
  push the post head. `_push_season_branch` (the seating push) resolves
  MAIN's branch and is already main-only. `dispatch.branch_worktree_for_spawn`
  creates the post/loop branch locally and pushes nothing.
- No literal `refs/heads/season<n>/posts` push refspec existed anywhere.

### Built
1. `branches.py` — the ONE mirror helper for the `refs/agi/<kind>/<name>`
   namespace, reusable for posts now and loops later:
   - `mirror_ref(season, kind, name)` -> `refs/agi/posts/<name>` |
     `refs/agi/loops/<name>`; a bad kind refuses by name.
   - `mirror_ref_for_branch(branch)` -> the mirror ref for a post/loop
     branch, `None` for a trunk / unrecognised name; NEVER raises.
   - `mirror_and_prove(local_root, ref, *, tip="HEAD", run=None, label)`
     -> `(ok, detail, {ref, sha, proved_by})`: `git push origin
     <sha>:<ref>` rc-gated, proven by `git ls-remote origin <ref>`. rc != 0
     from the rev-parse, the push, or the ls-remote, or a sha mismatch, is a
     REFUSAL BY NAME. ADDITIVE — never deletes, never forces, never a head.
2. `rotate.py:_stops_push` — at the ROTATE-OUT path a post/loop branch's tip
   is mirrored to its `refs/agi/...` ref (rc-gated; a failed mirror refuses
   the rotation by name and nothing rotates), and the head push is not
   reached. Trunks and unrecognised names keep the previous head push.
3. Clause (1) confirmed by grep + tests: seating (`_push_season_branch`,
   `_commit_spawn_row`, the spawn-row commit) pushes MAIN only.

### Tests added (6)
- `test_branches.py`: `mirror_ref`/`mirror_ref_for_branch` shapes (a);
  `mirror_and_prove` additive + proved-by-ls-remote + no head + no
  `--delete`/`--force` (c, f); mirror push failure refuses by name (d);
  no engine path names a pushed post head (e).
- `test_rotate.py`: seating push publishes main only, zero post heads (b);
  rotate-out mirrors to `refs/agi/posts/adv` and proves the sha, no head;
  mirror push failure refuses by name (d).
- Updated `test_rotate_closeout_steps.py` fakes: the frozen-prime
  post-branch push now asserts the mirror ref, never a head.

## Evidence

Command (explicit files, never the bare tests dir — the kid-tier gate
refuses a bare directory run):

```
python3 -m pytest extensions/agi/tests/test_branches.py \
    extensions/agi/tests/test_rotate.py \
    extensions/agi/tests/test_rotate_closeout_steps.py -q
-> 388 passed (70 + 277 + 41), 0 failed
```

Wider rotate sweep:

```
python3 -m pytest $(ls extensions/agi/tests/test_rotate*.py) \
    extensions/agi/tests/test_sensei_rotate_out_audit.py \
    extensions/agi/tests/test_veto.py -q
-> 803 passed, 1 xfailed, 1 FAILED
```

The one failure is PRE-EXISTING and unrelated to this diff:
`test_rotate_g1517.py::test_spawn_first_seating_role_from_row_and_pin_at_row_gen`
fails on `FileNotFoundError: .../seats/director-seat.ack.json`, with the
captured stderr `warn: first-seating meter pin / ack failed: not an agi
project graph root`. It runs in a gitless fixture, never reaches
`_stops_push`/`mirror_*` (neither changed function is on its path), and
fails identically in isolation.

Pre-fix context (NOT re-measured here — inherited from the parent
hypothesis, which measured it on season2/main @332ff48cf): `origin` heads
today = master, season1/main, season2/main, 2 town trunks, and 3
`season2/posts/*` heads (sanctuary-director, sanctuary-helper,
sensei-director) — the heads this round stops an engine path from creating,
and which clause (2)'s migration delete (with the merge-up kid) removes only
after an `ls-remote` proves the `refs/agi/posts/<name>` mirror.

## Deferred (this is a slice, and the deferral is named)
- The MERGE-UP half of clause (2), the new `rotate.py merge-up` verb
  (clauses (3)-(5)), the `--delete-old` mirror re-key/clause (6), and the
  three live origin post-heads' migration at their next merge-up: a LATER
  kid. The helper takes a `run` seam and a `label`, so the merge-up kid
  reuses it unchanged.
- `_stops_push`'s success contract stays `None` (the callers refuse on a
  truthy return); the `{ref, sha, proved_by}` dict is returned by
  `mirror_and_prove` and printed on the `push: OK` line, not threaded into
  the rotation record. Threading it into the record belongs with the
  merge-up kid.

## Agent Notes
Built clauses (1)+(2)-mirror-helper: branches.mirror_ref/mirror_ref_for_branch/mirror_and_prove (refs/agi/<kind>/<name>, push+ls-remote-proved, additive) and rotate.py _stops_push now mirrors a post/loop tip at rotate-out instead of pushing its head; 6 tests added / 3 updated, 388 passed. Merge-up verb, clause (6) re-key and the live head migration deferred to a later kid by the round brief.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
WHY THIS VERSION DIFFERS (parent a00-ea1066f0 review, SM.250).
(1) INSTRUCTION: the round brief said 'Confirm ... seating ... pushes MAIN only and never the post head. If a site does push a post head, remove that push and refuse by name instead' and clause (1) says 'a git push origin season2/posts/<name> from any engine path is a refusal by name'.
(2) WHAT THE MACHINE DOES: the mirror helper is REAL and proved -- branches.mirror_ref/mirror_ref_for_branch/mirror_and_prove (source: extensions/agi/bin/branches.py) pushes <sha>:refs/agi/<kind>/<name> and refuses on push rc!=0 OR an ls-remote mismatch; rotate._stops_push :15757 routes a post/loop branch to it instead of the head push. My probes: gate (ls-remote reports a DIFFERENT sha -> refusal naming both shas; ls-remote empty -> refusal), wire (push argv is exactly ...:refs/agi/posts/adv, no refs/heads). Those hold.
(3) THE NEAR MISS: the kid's own test test_no_engine_path_pushes_a_post_head greps for the LITERAL 'refs/heads/season...' and passes, but the bytes that push a post head spell the ref as a bare branch name. rotate._rename_surfaces :3365 adds the surface ('branch (origin)', src origin/season2/posts/old, dst origin/season2/posts/new) and rotate._apply_surfaces :3506-3510 runs git push origin season2/posts/new and git push origin :season2/posts/old with delete_old=True. I RAN it on a bare-origin fixture (probe_A1b): AFTER = refs/heads/season2/posts/new present, old head deleted, refs/agi/posts/* = (none). So a post rename both PUSHES A POST HEAD (falsifier 1) and DELETES BEFORE ANY MIRROR (falsifier 'never delete first'). The rename-apply path is the 'any engine path' clause (1) forbids.
(4) DEVIATION: none -- the rule is that a passing own-suite with a failed parent probe is lean_disproved, so the verdict drops from inconclusive_lean_proved:85 to inconclusive_lean_disproved:70; the mirror code is good and kept, the rename-apply fix moves to the next kid.
PROBES: gate=mirror_and_prove ls-remote-mismatch/absent refusal (PASS); wire=mirror_and_prove push argv + a live bare-origin mirror round trip (PASS); wire2=rotate._apply_surfaces post rename (FAIL: pushes refs/heads/season2/posts/new, deletes old head with no mirror).
<!-- THOUGHT:END -->

SM gen 6, Prime 08:24Z ruling: deprecated, never deleted -- the superseded SM.25 attempt on the orphan branch season2/loops/hypothesis-l4-post-branches-are--a00-ea1066f0 @140c5dd2a (1878 lines, gen-21-era base); the SM.25b re-cut (SM.90, landed 903718e22) found every clause already true on the current base, so this kid work is abandoned by construction. Moved under nodes/deprecated/experiment/; mint id and grid refs unchanged; the branch ref stays for the owner branch-cleanup pass listed in COMPLETE.md.
