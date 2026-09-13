---
id: hypothesis:l4-dispatch-performs-the-stale-base-sync-itself-when-the-merge-is-clean-instead-of-returning-the-merge-as-text
mint_id: f9c984b015ff47e0b24f7dd9e5845b42
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sanctuary-master
scaffold_hash: ba224c8c0e483b0c
season: 2
testable_claim: "goal:g15.25 SM.10 (intake: master-sensei 01:28Z line 1, measured on 59e3272b0: sensei-director 18 dispatched 01:22Z on a worktree cut 01:16Z, REFUSED stale-base behind=4 twice, then 3 hand fetch/merge/push calls; gen 17 paid 4 inline F14/stale-base calls). MEASURED on season2/main @8c9d3e1e0: dispatch.py _stale_base_spawn :280-372 fetches, counts behind and lists the engine files in `git diff --name-only HEAD...<integration>`; at :1904-1911 a `behind` status without --allow-stale-base prints _stale_base_record (whose `cmd` :403 is the literal text `git merge origin/<sb>`), releases the lease and returns 3 — the caller is handed an action list, never the action. rotate.py already owns the measured-clean merge primitive: _merge_applies_clean :12570 (read-only `git merge-tree --write-tree`) and _perform_season_merge :12605 (aborts on conflict). CLAIM: (1) NEW dispatch flag `--sync` (default ON; `--no-sync` restores today) — when _stale_base_spawn reports behind AND the spawner tree is clean (`git status --porcelain` empty, whitespace-only excluded as rotate does) AND the merge applies clean (reuse rotate._merge_applies_clean / _perform_season_merge by import, never a copy), dispatch performs `git merge --no-edit origin/<sb>` in the spawner tree, re-measures _stale_base_spawn, prints ONE line `synced: <old7>-><new7> behind 0 (N files)` and CONTINUES the dispatch; (2) the push after the merge is NOT performed by dispatch (a network write on the caller branch — name it in the synced line as the one remaining call: `push: git push` — or the auto-push SL7.113 already covers it at rotate-out: say which); (3) a dirty tree or a conflicting merge -> today exit 3 with the record, whose `cmd` now names WHY the sync was not performed (dirty paths / conflict paths) beside the merge text; (4) --allow-stale-base unchanged; --dry-run performs no merge and prints `would sync`; (5) the stale-base record gains `synced: true|false` + `sync_reason`. FALSIFIERS: a merge performed on a dirty tree; a merge that ran without the clean measure; a conflict left in the tree (abort path proven); a dry-run that merged; a second fetch (the one in _stale_base_spawn is the fetch). TESTS (test_dispatch.py, <= 5, fixture repo with an origin branch ahead): clean + mergeable -> merge performed, dispatch continues, one synced line; dirty -> exit 3, record names the dirty path; conflict -> exit 3, tree clean after (abort); --no-sync -> today; --dry-run -> would sync, no merge. FILE SCOPE: dispatch.py (the :1904 branch + one helper importing rotate primitives), test_dispatch.py. CEILING: <= 50 lines net, <= 5 tests."
title: "dispatch performs the stale-base sync itself — fetch, measured-clean merge of origin/<sb>, push — when the spawner tree is clean and the merge applies without conflict, instead of exit 3 with the merge command as text (master-sensei 01:3xZ: sensei-director 18 refused twice then 3 hand calls; gen 17 paid 4; 5 calls → 0)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-dispatch-performs-the-stale-base-sync-itself-when-the-merge-is-clean-instead-of-returning-the-merge-as-text

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
