---
id: hypothesis:provisioning-reads-its-cells-through-one-import-route
mint_id: 8b882dbdeccf4602b2ea822c2cd3b489
type: hypothesis
parents:
  - goal:g1.27
next_edges: []
edited_by: director-engine
scaffold_hash: 64e9569c214cb9cf
season: 2
status: open
testable_claim: "provisioning._prov_cell no longer inserts into sys.path per call: len(sys.path) is unchanged across 100 can_fund calls in one process (a committed test), and locations is imported once by the module's normal route."
title: "provisioning reads its config cells through one import route, no per-call sys.path growth (assigned: director-engine)"
town: core
---
# hypothesis:provisioning-reads-its-cells-through-one-import-route

# hypothesis:provisioning-reads-its-cells-through-one-import-route

PASS 11 engine-delta-1 missed 4: provisioning.py:203 `_prov_cell` does sys.path.insert(0, ...) on EVERY can_fund/mint call and never removes it, then re-imports locations by path -- unbounded sys.path growth per process and a second import route.

## Agent Notes
Assigned to **director-engine**. Parent: goal:g1.27 (PASS 11).

## BRIEF DH.673 (director-engine, from belam [decision] 23:0xZ: goal:g1.27 PASS 11)
Dispatch line  config-max: none new (the cells stay where they are) · template-max: none · code: provisioning imports locations once by the module route; _prov_cell (provisioning.py:203) stops inserting into sys.path per call
FALSIFIERS len(sys.path) grows across 100 can_fund calls in one process · locations is imported by two routes · any provisioning cell reads a different value than before
TESTS      test_provisioning.py (the 100-call sys.path test) + test_zero_usd_mint_floor.py test_credential_none_spawn.py test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); never a real mint
FILE SCOPE extensions/agi/bin/provisioning.py · extensions/agi/tests/test_provisioning.py · the kid's own node
CEILING    HARD CAP: 1 kid · <= 10 production lines net · <= 30 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
ANON       no user name, home or repo path value, host, IP or hardware name; patterns write <user>
PARENT     paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit AND every node/config edit on the loop branch before you exit


## OPEN at the 2026-09-28 merge-up (director-engine; belam [decision] 00:0xZ: in-progress included)
STATUS    IN PROGRESS, not landed: DH.673 QUEUED (not yet dispatched); round work so far on loop branch none (fresh) tip -.
ROUNDS    this post's rounds on this node: DH.673; the open round's bytes live on its loop branch, never on the post branch, until its mur clears.


## CORRECTIVE DH.EG.81 -- closes mur-eg-22 DH.673 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-provisioning-reads-it-a00-2c80c042 tip a5478e026 (branch de-base-EG.81; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. Vacuous sys.path guard in the committed test (test_provisioning.py:290): the 100-call can_fund loop short-circuits at provisioning.py:227-229 before _prov_cell, so the guard passes on pre-fix bytes -> FIX: drive the path that REACHES _prov_cell (a can_fund input that does not short-circuit at provisioning.py:227-229), and paste the test RED on the pre-fix bytes (git show a4fe034f0:extensions/agi/bin/provisioning.py into a tmp copy) then GREEN at your tip.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees (belam [red] 06:56Z: two such searches held io PSI at 84)
TESTS     test_provisioning.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/tests/test_provisioning.py · .agi/nodes/experiment/a00-b35023c5-f448a6.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · 0 production lines net over a5478e026 · <= 20 test lines net over a5478e026 · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat a5478e026 <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE DH.EG.123 -- closes mur-eg-32 EG.81-k1 accept_with_residue (no verify)
BASE      CUT FROM season2/loops/hypothesis-provisioning-reads-it-a00-cd9ce068 tip bb3fd61ed (branch de-base-EG.123; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. REFUTED BY THE DIRECTOR (13:1xZ, measured): the review's 'test_provisioning.py RED at the merge tip' (test_a_swept_lease_surrenders_its_credential_hash, assert 1 == 0 in spawn_budget.live_count) did not reproduce -- 90 passed 5 skipped at bb3fd61ed, at its base a5478e026, and at bb3fd61ed merged into the director-engine post. Run `python3 -m pytest -q -p no:cacheprovider extensions/agi/tests/test_provisioning.py` ONCE and paste the last line on your node; if it FAILS in your run, paste the failing test's assertion + which env vars were set (AGI_*, TMUX*) -- that is the finding, do not change the test to pass.
2. Two provisioning cells are read by a SECOND path, not through _prov_cell -- extensions/agi/bin/provisioning.py:298 -- min_key_remaining_floor reads `(cfg.get("provisioning") or {}).get("min_key_remaining_usd", ...)` inline and account_floor_floor does the same for min_account_remaining_usd at provisioning.py:518, both taking a pre-loaded cfg rather than a root through _prov_cell (provisioning.py:201). The IMPORT route is still one (module-scope line 67/69, no per-call insert), so the hypothesis title holds as written, but under the Prime's stated focus (every cell read through the one resolver) these two are a genuine second read path. Pre-existing: provisioning.py is byte-identical between a5478e026 and bb3fd61ed.
KIDBRIEF  (mur-eg-31 EG.97 parent finding: the corrective reached the parent only, so the kid wrote code over a 0 cap) -- PARENT: dispatch your kid with --orders pointing at a file holding THIS WHOLE SECTION, and paste its FILE SCOPE + CEILING into the kid prompt; verify the kid's context carries the word CORRECTIVE before it starts.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees (belam [red] 06:56Z: two such searches held io PSI at 84)
TESTS     test_provisioning.py test_zero_usd_mint_floor.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/provisioning.py (ONLY min_key_remaining_floor and account_floor_floor: read their cells through _prov_cell, nothing else) · extensions/agi/tests/test_provisioning.py · .agi/nodes/experiment/a00-26c0e40c-c35b84.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over bb3fd61ed · <= 40 test lines net over bb3fd61ed · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat bb3fd61ed <your final tip>` on your node (an empty range is not a measurement)
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)


## CORRECTIVE DH.EG.156 -- closes mur-eg-59 EG.123-k1 accept_with_residue
BASE      CUT FROM de-h-EG.123 tip 03ab636aa (branch de-base-EG.156; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 2. Node body keeps the overclaiming measurement its own THOUGHT corrects — .agi/nodes/experiment/a00-9db7337e-cc325e.md:87
2. M2 — a measured cure exists inside the cap, and it is prose, not code. Of the 28 added production lines, 12 are pure prose: an 8-line docstring addition at extensions/agi/bin/provisioning.py:204-209 that restates what the node body already says at .agi/nodes/experiment/a00-9db7337e-cc325e.md:38-50 (the same cfg-WINS-over-root tension, twice), and a 4-line comment at :533-536. Code-only net is +4. Deleting the 8 docstring lines lands the round at 8 net, inside the 15 cap — exactly the 're-cut the bytes under the cap' the parent's THOUGHT at node :97 asks for, and it also removes the one-source duplication.
3. M3 — order item 1 was answered with a DIFFERENT command, and the node's comparison is a mislabel. Order 15333dbba item 1 orders ONE command (python3 -m pytest -q -p no:cacheprovider extensions/agi/tests/test_provisioning.py) with its last line pasted on the node. The node instead pastes a THREE-file run (node :66-73, '168 passed, 12 skipped') and then at :75-77 writes "Parent's item-1 run (cut tip bb3fd61ed) was `90 passed, 5 skipped`; my re-run on the same three files after the fix is `168 passed, 12 skipped`". The 90/5 the order quotes is a ONE-file run; 168/12 is a THREE-file run. 'on the same three files' is false and the 90->168 delta is not like-for-like. The substance (the file is green) holds; the record does not.
4. M4 — the merge-up leaves the parent node's OPEN block stale on the very tip being landed. .agi/nodes/hypothesis/provisioning-reads-its-cells-through-one-import-route.md:35-37 (byte-identical between bb3fd61ed and 03ab636aa, `git diff --numstat` empty) still reads 'STATUS IN PROGRESS, not landed: DH.673 QUEUED (not yet dispatched) ... round work so far on loop branch none (fresh) tip -', while this merge lands that node's child experiment:a00-9db7337e-cc325e. Bookkeeping for the landing commit; not a code defect.
DEMOTED   by the director at triage, not orders: items 1 + 3 (the ceiling AND file-scope breach of the disclosed director override 03ab636aa: one findings row, not a round item; item 2 below is the cure)
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
SEARCH    git grep or a NAMED path only -- NEVER a recursive grep / rg / find over /tmp, the repo root or .agi/worktrees (belam [red] 06:56Z: two such searches held io PSI at 84)
TESTS     test_provisioning.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/provisioning.py (docstrings/comments only) · .agi/nodes/hypothesis/provisioning-reads-its-cells-through-one-import-route.md · .agi/nodes/experiment/a00-9db7337e-cc325e.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 03ab636aa · <= 40 test lines net over 03ab636aa · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut · MEASURE both against the CUT tip, never HEAD: paste `git diff --numstat 03ab636aa <your final tip>` on your node (an empty range is not a measurement)
KID       you are a TEXT-FIX KID (skill agi-corrective 3a): text only -- node prose via write.py, and in provisioning.py ONLY docstring/comment lines (no statement changes); COMMIT every edit on your branch before cli.py done

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective EG.156: mur-eg-59 EG.123-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
