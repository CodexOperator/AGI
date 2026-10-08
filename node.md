---
id: experiment:a00-05237869-730b66
mint_id: 1caa69c426bc4f32a33d5099b4792221
type: experiment
parents:
  - hypothesis:l4-prepare-measures-and-merges-the-same-ref-guard-first-and-check-5-prefers-the-rows-transcript
confidence: 0.85
edited_by: a00-4f25c9b5
evidence_runs:
  - experiment:a00-05237869-730b66
scaffold_hash: 35782e4df5e2e652
title: A00 05237869 730b66
verdict: proved
---
# experiment:a00-05237869-730b66

## Experiment

Piece P1-a + P2-a of `hypothesis:l4-prepare-measures-and-merges-the-same-ref-guard-first-and-check-5-prefers-the-rows-transcript` (g15.14 build order, fix-only #3). Scope: rotate.py perform/merge region + test_rotate_prepare.py. Other pieces (P1-b/c/d, P2-b) untouched.

**Pre-fix state measured:** in the `--perform` block of `_prepare_checks`, the conflict-free gate and the merge acted on DIFFERENT refs — `_merge_applies_clean(root, sb)` measured `merge-tree` against the LOCAL `origin/<sb>`, then `_perform_season_merge` re-`fetch`ed and merged whatever the REFRESHED `origin/<sb>` had become. A remote that advanced between the measure and the re-fetch turned a measured-clean merge into a different, conflicting merge with NO abort path; a conflict left git's conflict markers half-applied and nothing cleaned them up.

**Change 1 — measure and merge the SAME ref (P1-a).** In `_prepare_checks`' perform branch I added `_git_maybe(root, "fetch", "origin", _sb)` BEFORE the gate, so the gate measures the freshly-fetched `origin/<sb>`; and I REMOVED the internal `fetch` from `_perform_season_merge`, which now merges that same ref with no re-fetch. Re-fetching inside the merge was the whole divergence — a fetch could pull a NEWER ref than the one measured clean. With the fetch hoisted before measure and absent from the merge, measure and merge act on one frozen sha and cannot diverge.

**Change 2 — abort, never a half-merge (P1-a).** `_perform_season_merge` now runs `git merge --abort` whenever the merge's rc is non-zero (a refused merge or a conflict), so the working tree is never left mid-merge; it still returns None (never a false `merged <sha>`). The caller's refused-branch message is now `— merge attempted, refused by git (aborted)`; exit 3, block. The merge-tree-detected-conflict branch (gate == False) already BLOCKS naming the paths, unchanged.

**P2-a — real-fixture test, no gate monkeypatched.** Added a `_real_repo` helper that builds a live two-branch git repo (a `season/s2` branch ahead of a `seat/x` checked-out branch, real `refs/remotes/origin/*`, upstreams configured) and three tests that run the REAL merge-tree gate, REAL merge and REAL abort:

1. `test_prepare_perform_merge_same_ref_clean_real_fixture` — clean merge flows through `cmd_prepare --perform`, prints `[ok] behind origin/season/s2 (1) — merged <sha>`, exit 0; asserts HEAD actually moved past the season commit and the season file landed.
2. `test_prepare_perform_conflict_blocks_real_fixture` — a branch that conflicts on `f.txt`; the real gate BLOCKS naming `f.txt`, exit 3, no merge; asserts no MERGING state, no conflict markers, HEAD unmoved.
3. `test_prepare_perform_season_merge_aborts_live_conflict` — drives the real `_perform_season_merge` at the actual `git merge` conflict; asserts it returns None and the half-merge is aborted (no MERGING state, clean diff, HEAD = seat work).

Because all three assert on what the LIVE repo actually shows (HEAD advanced / conflict named / tree left clean), a gate patched out fails them — there is no monkeypatch of `_merge_applies_clean`, `_merge_conflict_paths` or `_perform_season_merge` anywhere in these tests.

## Evidence

Commands run (from the worktree root):

```
python3 -m pytest extensions/agi/tests/test_rotate_prepare.py -q
  -> 24 passed (21 prior + 3 new real-fixture tests)
python3 -m pytest extensions/agi/tests/test_rotate.py test_rotate_selfreap.py test_rotate_startup.py test_rotate_handover.py test_rotate_recover.py test_rotate_autopsy.py test_rotate_g1517.py -q
  -> 288 passed
```

Clean-merge test's fixed expected output: line `[ok] behind origin/season/s2 (1) — merged <sha>`; the sha is the season-work commit of the fixture repo (per-run, not a stable literal). The merge that performed was `git merge --no-edit origin/season/s2` on ref `origin/season/s2` = the freshly-fetched ref the gate had just measured — the same ref, per the claim.

**Falsifier checked:** "a prepare --perform where the local ref is clean but the refreshed ref conflicts leaves a half-merge or merges anyway" — the divergence is structurally closed (fetch hoisted before the gate, no re-fetch in the merge, abort on any non-zero merge rc). The half-merge-anyway case is covered by the abort test (real conflict → `merge --abort`, tree clean). Directly covering the stale-local-vs-refreshed-remote divergence in a unit test would need a file:// remote that mutates between two fetches; the local-fixture layout rebuilds the ref freshly each time, so that specific race is covered by construction, not by an assertion — the code reads fetch-once → measure → merge-same-<no-fetch> and the merge has no path to a newer ref.

## Experiment notes

g15.14 fix-only #3, P1-a + P2-a only. The core defect was measure-vs-merge ref divergence: the gate measured the local `origin/<sb>`, the merge re-fetched and merged a newer ref, with no abort path. Fix: one fetch hoisted before the gate, the merge's internal fetch deleted so measure and merge act on one sha, and an abort on any non-zero merge rc (never a half-merge). P2-a adds a real two-branch git fixture with nothing about the gate/merge monkeypatched, so a patched-out gate fails it. Two tool fights: the first edit call was malformed (a nested `edits` array) and only one of the two edits landed — the fetch line had to be re-applied; and `git branch --set-upstream-to` rejects a ref made by `update-ref` ("starting point 'origin/seat/x' is not a branch"), so the upstream was configured via `git config branch.seat/x.*` instead.

## Agent Notes
P1-a: fetch hoisted before the merge-tree gate, _perform_season_merge's internal fetch deleted so measure+merge act on one sha, and merge --abort on any non-zero rc (never a half-merge). P2-a: 3 real two-branch git-fixture tests with the gate/merge un-monkeypatched (clean merge, conflict BLOCK naming f.txt, live abort). 24 prepare + 288 rotate-neighbour tests green.

PARENT REVIEW a00-4f25c9b5 (SL5.06, kid 1/3), accepted. Evidence re-run by the parent, not taken on report: pytest test_rotate_prepare.py 24 passed; rotate neighbours (test_rotate, selfreap, startup, handover, recover, autopsy, g1517) 288 passed. P1-a verified on the built bytes: fetch is hoisted before _merge_applies_clean and _perform_season_merge no longer re-fetches (rotate.py:8035 fetch, :7838 merge), so measure and merge act on one frozen origin/<sb>; git merge --abort on any non-zero rc at rotate.py:7857. P2-a verified: the three _real_repo tests monkeypatch _merge_applies_clean/_merge_conflict_paths/_perform_season_merge NOWHERE; the conflict test fails if the gate is patched True (it would print "refused by git (aborted)" instead of "merge conflicts: f.txt"), so the real gate IS exercised. RESIDUE (not blocking): (1) the post-gate refused branch names no conflict paths — capture them before merge --abort if a conflict-race must name files; (2) the race itself (remote advances between the single fetch and the merge) is closed by construction, not asserted. NOTE: the changed line reads "refused by git (aborted)" — a superset of the old asserted substring, so the existing test still pins it. Both pieces are build-order items and the code implements them.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review version (a00-4f25c9b5, SL5.06): the kid node is accepted as written for P1-a+P2-a; this version differs only in adding the parent review note and the two named residues. Mechanism check against the instruction: the claim says "measure and merge the SAME ref ... on ANY conflict abort and BLOCK naming the paths; never leave a half-merge". What the machine now does (rotate.py:8035): _git_maybe fetch origin <sb> runs BEFORE _merge_applies_clean, and _perform_season_merge (7838) merges origin/<sb> with no internal fetch and aborts on non-zero rc (7857) — so the measured ref and the merged ref are one frozen value. Near miss that satisfies the words and loses the mechanism: fetching inside _perform_season_merge but ALSO calling merge-tree against a sha resolved before it — that still measures one ref and merges another, which is exactly the defect; the kid avoided it by hoisting the fetch and deleting the inner one. Deviation from a standing rule: none — the parent used write.py (sanctioned writer) rather than editing the node file, and ran the tests itself before accepting.
<!-- THOUGHT:END -->
