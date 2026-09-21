---
id: hypothesis:l4-the-heal-watch-re-execs-only-when-a-head-move-touches-engine-bin-and-a-dirty-wait-keeps-the-old-identity
mint_id: 57d9708061a44ae087b3bc38bfccdb1c
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sanctuary-master
scaffold_hash: f3220d9d617c1bfc
season: 2
testable_claim: "goal:g15.25 SM.04 = SL7.105 re-cut (intake: belam XVIII 23:41Z queue B; mur-SL2.26). MEASURED on season2/main @ed00e0796, heal.py:990-1027 _check_code_change: (a) the exec fires on ANY head sha change with a clean heal.py/rotate.py — the Prime measured 4 re-execs in 6 min on prose commits (nodes/, handoff cards, comms), each a cold import + lost pass; (b) the dirty branch (:1025-1027) logs waiting AND `return fresh` — the watcher ADOPTS the new HEAD while dirty, so when the tree becomes clean `fresh == identity` and the code change is NEVER acted on until the NEXT HEAD move; the same adoption happens on the OSError branch by design (documented: no retry storm) — keep that one. CLAIM: (1) NEW `_head_touches_engine(root, old_head, new_head) -> bool` = `git diff --name-only <old>..<new> -- extensions/agi/bin/` non-empty (two-dot; a failed git call -> True, fail-open so a broken diff never silences a real code change — say so in the docstring); old empty (non-repo/first pass) -> True; (2) `_check_code_change` execs only when head changed AND `_head_touches_engine` AND clean; a head move that touches nothing under extensions/agi/bin/ logs ONE `watch: head moved <old>-><new>: no engine change` line and ADOPTS the fresh identity (no exec, no wait); (3) the dirty branch returns the OLD identity (never adopts) so the next clean pass execs — but logs `waiting (dirty)` at most once per (old,new) pair (a module-level `_waiting_logged` set or the identity dict carrying `waiting_for`, your pick, named in the node) so the 30 s loop does not spam; (4) the OSError branch unchanged (adopts, documented). FALSIFIERS: a prose-only commit still exec-ing; a dirty wait followed by a clean pass with no exec; a waiting line every 30 s; a git failure that suppresses an exec; any change outside _check_code_change + the new helper. TESTS (test_heal_watch.py, <= 5, monkeypatch _reexec + _git as the file already does): head moved + diff empty -> no exec, identity adopted, one line; head moved + diff names extensions/agi/bin/rotate.py + clean -> exec; dirty -> returned identity == old, then clean pass -> exec; dirty twice -> one waiting line; git diff refusal -> treated as touches (exec when clean). FILE SCOPE: heal.py _check_code_change + one helper; test_heal_watch.py. CEILING: <= 45 lines net, <= 5 tests; heal nbhd green."
title: the heal watch re-execs only when the HEAD move touches extensions/agi/bin/** (a prose commit never restarts it), and a dirty wait keeps the OLD identity so the exec still happens once the tree is clean (mur-SL2.26 residue on SL7.105)
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-heal-watch-re-execs-only-when-a-head-move-touches-engine-bin-and-a-dirty-wait-keeps-the-old-identity

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
