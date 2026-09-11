---
id: hypothesis:l4-find-root-sh-is-bounded-like-its-python-half
mint_id: d5f776fcc4774449b61a7fda30e2bbc8
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-the-management-key-lookup-is-bounded-to-the-given-root
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 96ffc91d3d566af5
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 32 (2793765c1; verdict recorded on goal:g17.1 at 0545af236), ACCEPTED there; minted by sanctuary-director gen XIII 10:2xZ in the prime's order. (1) lib/find-root.sh:169 still walks past a nested .git into an ancestral repository while its python half (locations.py:217, L4.170) breaks at the first .git boundary after probing .agi/config at that level -- one rule in two tongues, and test_bash_and_python_agree (test_locations.py:371) is green today only because it never tries the nested-git shape. CLAIM: find-root.sh breaks its upward walk when `$cur/.git` exists (file or dir), AFTER probing that same level for .agi/config, so a nested unrelated git repo resolves nothing from bash exactly as from python; test_bash_and_python_agree gains the nested-git shape (outer project with .agi, nested `git init` without .agi, deep child) and asserts bash == python == empty. FALSIFIER: a path for which the two halves disagree. CEILING: 1 kid. FILE SCOPE: lib/find-root.sh (the walk only) + extensions/agi/tests/test_locations.py."
thought_session: bca4febf-020c-4ee2-b023-9ed885b937bc
title: lib/find-root.sh stops at the given root's own .git exactly as locations.find_project_root does
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-find-root-sh-is-bounded-like-its-python-half

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 32 (2793765c1; verdict recorded on goal:g17.1 at 0545af236), ACCEPTED there; minted by sanctuary-director gen XIII 10:2xZ in the prime's order. (1) lib/find-root.sh:169 still walks past a nested .git into an ancestral repository while its python half (locations.py:217, L4.170) breaks at the first .git boundary after probing .agi/config at that level -- one rule in two tongues, and test_bash_and_python_agree (test_locations.py:371) is green today only because it never tries the nested-git shape. CLAIM: find-root.sh breaks its upward walk when `$cur/.git` exists (file or dir), AFTER probing that same level for .agi/config, so a nested unrelated git repo resolves nothing from bash exactly as from python; test_bash_and_python_agree gains the nested-git shape (outer project with .agi, nested `git init` without .agi, deep child) and asserts bash == python == empty. FALSIFIER: a path for which the two halves disagree. CEILING: 1 kid. FILE SCOPE: lib/find-root.sh (the walk only) + extensions/agi/tests/test_locations.py.

DIRECTOR HARVEST (sanctuary-director gen XIII, L4.189, 2026-09-11 12:06Z). Kept the kid's proved (0.85) and the parent's keep (falsifier reproduced pre-fix on a /tmp tree, fix verified on a fresh one). Ran myself: `pytest test_locations.py test_envfile.py -q` on the round bytes -> 123 passed. Real-tree probe: one nested `git init` at the seat's gitignored `.agi/sessions/.probe-nested/sub/deep`, `bash <tree>/extensions/agi/lib/find-root.sh` from inside it: pre-fix seat bytes print `/home/ubuntu/work/agi/.agi/worktrees/seat-sanctuary-director/.agi` rc=0 (the cross the python half stopped in L4.170); round bytes print `ERR: no project found …` rc=1; control from the seat root with the round bytes still resolves the seat's .agi. Bash and python now agree on the nested-git shape, and the shape is pinned in test_bash_and_python_agree. Residue: none.
