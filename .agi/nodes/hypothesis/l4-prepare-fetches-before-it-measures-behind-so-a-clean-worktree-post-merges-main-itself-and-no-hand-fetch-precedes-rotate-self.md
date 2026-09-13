---
id: hypothesis:l4-prepare-fetches-before-it-measures-behind-so-a-clean-worktree-post-merges-main-itself-and-no-hand-fetch-precedes-rotate-self
mint_id: d6ead146b658488ba4fa83198e4e11ba
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 1edfa79b66c33c5c
season: 2
testable_claim: "goal:g15.25 SM.08 (intake: master-sensei 01:14Z, one line: worktree posts pay one call before every rotate-self — git fetch + merge origin/season2/main — because rotate-self reads the template from the worktree, F14). MEASURED on season2/main @7973e3f2a: _prepare_checks rotate.py:12757 check 3 counts behind with `rev-list --count HEAD..origin/<sb>` (:12879) against the LOCAL remote-tracking ref BEFORE any fetch; the perform branch (:12889-12902) fetches (`_git_maybe fetch origin <sb>`) and merges ONLY when that stale count is already > 0 — a worktree whose local origin/<sb> has not moved since its last fetch reads behind = 0, performs nothing, and the successor wakes on a stale template with stale {facts}; hence the hand fetch+merge before every rotate-self (the F14 line, rotations.md:186). CLAIM: (1) in _prepare_checks when perform is true, ONE `fetch origin <sb>` runs BEFORE the behind count (move the existing :12898 fetch above :12879; never a second fetch in the perform branch); a failed fetch (network, 403) does not block: the check reports `behind origin/<sb> (unmeasured: fetch failed <rc>)` and the rotation continues exactly as today with the stale ref — say so in the docstring; (2) with perform false (`prepare` without --perform, `--dry-run`) NO fetch runs (fetch is a network write, rotate.py:9600-9603 — the allowlist stays as is); (3) the clean-tree + zero-conflict merge then performs as today (P1-a same-ref rule kept: the merge uses the ref the fetch refreshed); dirty or conflicting stays a BLOCK by name; (4) the bare rotate verb inherits it through cmd_rotate_self (no change there — measure and say the line where perform defaults ON, :14799 region); (5) F14 in config:rotations becomes a template line for master-sensei: the hand merge sentence is retired once this lands (the round does NOT write config:rotations; name the sentence). FALSIFIERS: a fetch on a dry-run or on plain prepare; two fetches in one prepare; a fetch failure that blocks the rotation; a behind count taken before the fetch; any change to the conflict/dirty gates. TESTS (test_rotate_prepare.py, <= 4, on the existing fixture with a monkeypatched _git_maybe recording argv order): perform=True -> argv order is fetch THEN rev-list THEN merge, and a fixture where the local ref is stale-behind-zero but the fetched ref is ahead -> merge performed; perform=False -> no fetch argv; fetch rc!=0 -> unmeasured line, no block; conflict -> BLOCK unchanged. FILE SCOPE: rotate.py _prepare_checks only; test_rotate_prepare.py. CEILING: <= 20 lines net, <= 4 tests."
title: the prepare gate fetches origin/<sb> BEFORE it counts behind, so a clean worktree post fast-forwards itself to main inside rotate-self (and the bare rotate verb) and the hand fetch+merge every worktree rotation pays today (F14; sanctuary-helper 8→9 call 178) is gone
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-prepare-fetches-before-it-measures-behind-so-a-clean-worktree-post-merges-main-itself-and-no-hand-fetch-precedes-rotate-self

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
