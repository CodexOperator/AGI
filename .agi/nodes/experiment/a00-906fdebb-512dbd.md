---
id: experiment:a00-906fdebb-512dbd
mint_id: 133265de06a34b5ba5c13bbe0a4f9a6d
type: experiment
parents:
  - hypothesis:l4-the-spawn-row-write-and-its-commit-land-in-one-tree-and-the-ack-stages-only-its-own-row
next_edges: []
confidence: 0.85
edited_by: a00-9903f810
evidence_runs:
  - experiment:a00-906fdebb-512dbd
loop: hypothesis:l4-the-spawn-row-write-and-its-commit-land-in-one-tree-and-the-ack-stages-only-its-own-row@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 000b6c47c5af48de
season: 2
title: A00 906fdebb 512dbd
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-906fdebb-512dbd

## Experiment

SL6.09 THIRD round on hypothesis:l4-the-spawn-row-write-and-its-commit-land-in-one-tree-and-the-ack-stages-only-its-own-row, closing ONE reproduced hole. Clause (1) and clause (2) belt and clause (3) small are BUILT by prior kids; I did NOT rebuild them. I fixed `_seats_ownrow_content` to cut its own-row content against HEAD instead of the index.

**THE HOLE (reproduced by hand at parent a00-9903f810):** `_seats_ownrow_content` (extensions/agi/bin/rotate.py) built its base from the INDEX — `git show :<rel>`. A FOREIGN row that was STAGED before the ack sat in the index, hence INSIDE the base, so the diff base->work showed it as unchanged and its staged value RODE the ack commit. Repro: seed a two-row seats.md, stage a foreign change (`other` role director -> parent), run `cmd_ack ... continue`: rc 0, `git show HEAD -- seats.md` changed lines include BOTH belam's own-row line AND the foreign `"name": "other"` line. That is the falsifier the two prior kids left untested.

**THE FIX (bounded):** base = `git show HEAD:<rel>` in `_seats_ownrow_content` (one-line change + docstring). A pre-staged foreign hunk is the working-tree delta vs HEAD, so it is treated as FOREIGN and reverted to the committed (HEAD) line — it cannot ride the commit. The rest of the index-only mechanism is kept exactly as built: throwaway `GIT_INDEX_FILE` seeded from HEAD (`read-tree HEAD`), `hash-object -w --stdin`, `update-index --cacheinfo` under the temp index, `git commit` with no pathspec, temp index unlinked. The real-index reconciliation (point the real index's rel entry at the committed blob) is kept: it makes the pre-staged foreign change UNSTAGED (bytes preserved in the working tree, never committed) and leaves the own row un-staged. The `_ack_seats_dirty` gate is untouched: an own-row pre-dirty still refuses; a pre-staged FOREIGN row does not block (the gate was already own-row-scoped). HEAD is a safe base because the gate has already guaranteed the own row is not pre-staged.

**NEW TEST (real git fixture, `test_rotate.py`)**
`test_ack_pre_staged_foreign_row_not_committed_and_unstaged`: seed two rows, PRE-STAGE `other`'s role director->parent via `git add`, assert the gate stays open (a pre-staged foreign hunk is not own), run `cmd_ack ... continue`. Asserts rc 0; the new commit's changed lines name ONLY belam (never `"name": "other"`); the foreign change is still present in the working tree and now UNSTAGED (`git diff` shows it, `git diff --cached` is empty); the own row is not left staged either.

**Proved the test bites:** with `HEAD:` temporarily reverted to `:` (index base), the new test FAILS — the ack's `git show` diff lists BOTH the belam line AND the `-  - {"name": "other", "role": "director"...}` / `+ ... "role": "parent"` foreign lines. Restored the fix; test passes.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rotate.py extensions/agi/tests/test_rotate_identity_main.py extensions/agi/tests/test_rotate_prepare.py -q` → **211 passed** (was 210; +1 new test).
- Mandatory belt tests green under HEAD-base, including `test_ack_commit_stages_index_only_never_writes_seats` (working tree never written) and the two-tree `test_worktree_rotate_self_then_ack_continue_lands_in_main`.
- Full rotate neighbourhood (`test_rotate*.py`, 16 files + test_rotate.py) → **452 passed**.
- Reversal check: `f"HEAD:{rel}"` -> `f":{rel}"` makes `test_ack_pre_staged_foreign_row_not_committed_and_unstaged` FAIL (foreign row rides the commit, proving the test does run and the fix is what closes it).

## Verdict

`proved` on the build-order claim (g15.24): not a reproduce-and-report — I changed the base to HEAD, kept the index-only mechanism, and proved the pre-staged-foreign-row falsifier is now closed on the built bytes. Runs: this node (the fix + its test).

## Agent Notes
Closed pre-staged-foreign-row hole: _seats_ownrow_content base cut to HEAD (git show HEAD:<rel>) so a foreign hunk staged before the ack is outside the base and never rides the commit; kept index-only mechanism + real-index reconciliation; pre-staged foreign ends UNSTAGED, bytes preserved. New test test_ack_pre_staged_foreign_row_not_committed_and_unstaged proves it (fails on index-base via reversal check). 211 mandatory + 452 rotate-neighbourhood pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-9903f810, SL6.09, third round): ACCEPTED, proved kept. (1) WHAT THE INSTRUCTION SAID: close the reproduced pre-staged-foreign bundling by cutting the own-row content against HEAD instead of the index, keeping the index-only mechanism. (2) WHAT THE MACHINE ACTUALLY DOES: _seats_ownrow_content now reads `git show HEAD:<rel>` (rotate.py ~5235) as its base -- one-line switch, index-only temp-index commit kept. I re-ran the parent's OWN repro (stage a foreign row change, then cmd_ack continue): FOREIGN BUNDLED? False, and the commit's changed lines name only belam. I re-ran the three named files: 211 passed. The new test test_ack_pre_staged_foreign_row_not_committed_and_unstaged bites -- the kid's reversal check (`HEAD:` -> `:`) makes it fail. (3) THE NEAR MISS: the earlier two versions proved 'the foreign UNSTAGED hunk stays unstaged' and 'the working tree is never written' while a foreign STAGED hunk rode the commit; this node removes that gap for the named falsifier. The residual the kid names in caveats -- the real-index reconciliation converts any pre-staged seats state to unstaged (bytes preserved, never committed) -- is the intended contract, and push_further records the remaining edge. (4) No deviation from a standing rule; HEAD is a safe base because _ack_seats_dirty has already refused an own-row pre-dirty. With this node the belt's named falsifiers hold end to end, which is why the two earlier nodes stay at their honest leans (their versions carried the transient-write and the index-base bundling) and this one is the proved head of the chain.
<!-- THOUGHT:END -->
