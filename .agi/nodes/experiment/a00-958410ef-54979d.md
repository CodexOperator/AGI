---
id: experiment:a00-958410ef-54979d
mint_id: 7ea0ada1c97e4f4391e27ad11bd8179c
type: experiment
parents:
  - hypothesis:l4-an-empty-or-blank-explicit-kinds-is-refused-and-every-branch-spelling-is-in-its-own-ref-candidates
next_edges: []
confidence: 0.95
edited_by: a00-276f7aff
evidence_runs:
  - experiment:a00-958410ef-54979d
loop: hypothesis:l4-an-empty-or-blank-explicit-kinds-is-refused-and-every-branch-spelling-is-in-its-own-ref-candidates@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 1e0a33b94944dc75
season: 2
title: A00 958410ef 54979d
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-958410ef-54979d

## Experiment

Target: branches.py `ref_candidates` docstring claim "The as-written input
always appears in the result (it is one of the three spellings for every
input kind)" (mur-47). Measured pre-fix, two inputs were absent from their
own lists: `master` and the town one-season alias `town/<t>@s<N>`.

Pre-fix probe (defect confirmed):
    'master'     -> ['season1/main', 'season/s1']            # master ABSENT
    'town/core@s2' -> ['season2/core/season1/main', 'town/core/season/s1']  # town/core@s2 ABSENT

Implemented the FIRST option (make the docstring true — add the missing
reverse rows to `_canonical_to_old`), not merely the second (narrow the
docstring). Region: extensions/agi/bin/branches.py `ref_candidates` +
`_canonical_to_old`, and extensions/agi/tests/test_branches.py. cli.py and
test_cli.py were NOT touched (owned by KID A).

`_canonical_to_old` now returns `list[str]` (was `str | None`) so a canonical
may carry MORE than one old spelling:
  (a) season<n>/main -> [season/s<n>]; when n==1 ALSO append "master"
      (master is the pre-rename spelling of the core season-1 main only;
      is_legal_branch("master") is True).
  (b) season<n>/<t>/season<k>/main -> [town/<t>/season/s<k>]; when k==1 ALSO
      append "town/<t>@s<n>" (town/<t>@s<N> canonicalises to
      season<n>/<t>/season1/main). A town main with town_season != 1 has no
      town@ reverse, correctly.
ref_candidates flattens inter + legacy lists, canonical first, deduped.
Post/loop/season main lists unchanged byte-for-byte.

## Evidence

Post-fix probe (past verbatim):
    $ python3 -c "import sys;sys.path.insert(0,'bin');import branches;[print(repr(b), branches.ref_candidates(b)) for b in ['post/x@s2','seat/x@s2','season2/posts/x','town/core@s2','master','season1/main','season2/main','season/s2','town/core/season/s1','loop/y-a00@s2']]" 2>/dev/null
    'post/x@s2'          ['season2/posts/x', 'post/x@s2', 'seat/x@s2']
    'seat/x@s2'          ['season2/posts/x', 'post/x@s2', 'seat/x@s2']
    'season2/posts/x'    ['season2/posts/x', 'post/x@s2', 'seat/x@s2']
    'town/core@s2'       ['season2/core/season1/main', 'town/core/season/s1', 'town/core@s2']
    'master'             ['season1/main', 'season/s1', 'master']
    'season1/main'       ['season1/main', 'season/s1', 'master']
    'season2/main'       ['season2/main', 'season/s2']
    'season/s2'          ['season2/main', 'season/s2']
    'town/core/season/s1'['season2/core/season1/main', 'town/core/season/s1', 'town/core@s2']
    'loop/y-a00@s2'      ['season2/loops/y-a00', 'loop/y-a00@s2']

Every input kind is now in its own list; post/loop/season lists byte-identical
to the pre-fix measured ground truth.

Tests: extensions/agi/tests/test_branches.py (new parametrized
test_ref_candidates_every_input_kind_in_own_list over town/<t>@s<N>,
town/<t>/season/s<k>, master, season1/main, season/s2, loop/...@s2,
post/...@s2, seat/...@s2 — every one asserts the as-written input IS in its
own list; plus test_ref_candidates_master_is_legal_branch, the town@
reverse-derives-back check, the master-only-for-season1 check, and updated
town trunk / _canonical_to_old list asserts).

Run: `python3 -m pytest extensions/agi/tests/test_branches.py extensions/agi/tests/test_cli.py -q`
    -> 85 passed (test_branches.py + test_cli.py).
Cross-check of downstream ref_candidates consumers:
    `python3 -m pytest extensions/agi/tests/test_dispatch.py extensions/agi/tests/test_send.py extensions/agi/tests/test_rotate_autopsy.py extensions/agi/tests/test_verification.py extensions/agi/tests/test_heal.py -q`
    -> 469 passed. No --apply / --delete-old / git run.

Note: dispatch.py:293 `_town_at_legacy` was a workaround for the grammar NOT
deriving `town/<t>@s<N>` back; that row now exists in the grammar, so the
workaround is redundant-but-harmless (deduped away by _dedupe_ordered). Left
untouched (outside region); a future round may retire it.

## Agent Notes
Made ref_candidates docstring TRUE: added reverse rows to _canonical_to_old so master (for season1/main only) and the town one-season alias town/<t>@s<N> (for town_season==1) each appear in their own candidate list. _canonical_to_old returns list[str] now; ref_candidates flattens+dedupes, canonical first. post/loop/season main lists byte-identical to before. 85 pass (test_branches+test_cli), 469 pass downstream (dispatch/send/rotate_autopsy/verification/heal).

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
REVIEW (parent a00-276f7aff, L4.331): (1) THE INSTRUCTION: Prime mur-47 verbatim -- "ref_candidates docstring overclaims (branches.py:118: town/<t>@s<N> and master absent from their own lists)"; the brief said PREFER THE FIRST OPTION, make the docstring TRUE by adding the missing reverse rows. (2) WHAT THE MACHINE NOW DOES: branches.py:146 _canonical_to_old now returns list[str]; :158-164 appends "master" only when the season number is 1; :168-171 appends town/<t>@s<n> only when the town season is 1; ref_candidates:138-143 flattens inter+legacy, canonical first, deduped. The parent RECOMPUTED the probe rather than reading the node: master -> [season1/main, season/s1, master], town/core@s2 -> [season2/core/season1/main, town/core/season/s1, town/core@s2], town/web-app-suite@s2 -> [... , town/web-app-suite@2 spelling present], and post/loop/season lists byte-identical to the pre-fix ground truth the parent measured before any kid ran; 115 passed across test_branches.py + test_cli.py + test_branch_reshuffle.py. (3) THE NEAR MISS: appending "master" for EVERY season<n>/main (drop the n==1 guard) -- the words "master is in its own list" would still hold for the one probe the kid pasted, while inventing a spelling that no ref of season2/main ever bears, i.e. a list that claims reachability it does not have. Same shape for town/<t>@s<n> without the k==1 guard: town/<t>@s<N> canonicalises to season<N>/<t>/season1/main, so only a town_season==1 main can carry it. The two guards are the mechanism. (4) DEVIATION, with the property of this case: the brief scoped branches.py to ref_candidates + _canonical_to_old, and the kid widened the LATTER return type from str|None to list[str]. That is licensed here because ref_candidates is its only caller (grep over the whole tree finds calls only in branches.py:136-137 and the tests; dispatch.py:376 names it in prose only), and because a canonical that bears two old spellings cannot be expressed by a str|None return at all -- the alternative, a second parallel helper, would leave the grammar-level claim false and duplicate the alias table. RESIDUE handed up, not fixed (outside region): dispatch.py _town_at_legacy is now redundant-but-harmless, and its :376 comment still describes the old single-form derivation.
<!-- THOUGHT:END -->
