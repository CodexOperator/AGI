---
id: hypothesis:l4-dispatch-exits-non-zero-and-deprecates-the-scaffold-when-no-agent-record-follows-a-scaffolded-node
mint_id: 06cbb5c7c381455db62517ff566e3afb
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: 3e82cb0cb73054d4
season: 2
testable_claim: "goal:g15 FIX-ONLY (Sensei ask — owner ask via the point 22:0xZ, draft .agi/sessions/sensei/drafts/parent-role-pass-L4.327-20260912T2157Z.md — line (4) code). MEASURED by the Sensei on L4.327: dispatch.py scaffolded a node for the parent and NO agent record followed, yet dispatch exited 0 — the parent paid 480 s waiting on a spawn that never registered, then a hand deprecation of the orphan scaffold. Re-measure on post tip 8174d451d: dispatch.py:1719-1879 (the lease -> session dir -> scaffold -> spawn order; :1837 'costs no zoom render and leaves no orphan scaffold behind'), _scaffold_node_for_agent (:206), and where the agent record (.agi/sessions/.spawn-budget entry + the iter session dir's spawn.json) is written relative to the scaffold. CLAIM: (1) dispatch.py exits NON-ZERO (a named code, e.g. 4 'scaffolded-but-unregistered') when a node was scaffolded and no agent record exists within the spawn's own registration step — the scaffolded node is deprecated by the same run (moved to .agi/nodes/deprecated/<type>/ with status: deprecated and a note naming the failed spawn), never left live; (2) the JSON issue line names the node id and the missing record; (3) a successful spawn's exit code and output are byte-identical to today; (4) the stale-base rc 3 path is untouched. FALSIFIERS: exit 0 with a live orphan scaffold; a deleted (git rm) scaffold; the success path changed. TESTS (append to test_dispatch*.py, <= 4, through the existing spawn seams: a spawn seam that scaffolds then fails to register): rc + issue line; the scaffold deprecated with the note; success golden; rc 3 unchanged. FILE SCOPE: dispatch.py — the post-scaffold registration check + the deprecation call (reuse write.py / node_writer's deprecate path if one exists — say which); the dispatch tests. EXCLUDED: zoom.py (109/111), cli.py (110), the brief text. CEILING: <= 50 lines + <= 4 tests; test_dispatch* green."
thought_session: sensei-director-genXVII-L17
title: "dispatch.py exits non-zero by name and deprecates its own scaffold when it scaffolds a node and no agent record follows — never exit 0 over a live orphan (the L4.327 parent paid 480 s + a hand deprecation) (owner heuristic line 4: code)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-dispatch-exits-non-zero-and-deprecates-the-scaffold-when-no-agent-record-follows-a-scaffolded-node

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
