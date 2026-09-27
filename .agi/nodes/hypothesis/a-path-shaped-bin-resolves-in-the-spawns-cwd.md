---
id: hypothesis:a-path-shaped-bin-resolves-in-the-spawns-cwd
mint_id: 2e0438c0a7ab49118881856d04ba904f
type: hypothesis
parents:
  - goal:g1.26
next_edges: []
edited_by: director-engine
scaffold_hash: a689b82fb32c9e9f
season: 2
testable_claim: a relative bin valid in the spawn cwd resolves; an invalid one refuses by name; the build node is versioned with the payload
title: "A path-shaped bin is judged in the spawn cwd, not the resolver cwd (assigned: director-engine)"
town: core
---
# hypothesis:a-path-shaped-bin-resolves-in-the-spawns-cwd

# hypothesis: A path-shaped bin is judged in the spawn cwd, not the resolver cwd (assigned: director-engine)

## Why this exists
**Parent `goal:g1`** (PASS residues; g15 -> g20 -> g1). A real code defect confirmed by the PASS 10 merge-up review (BASE 9e16b8ed90 -> TIP 6c403aeb4b, merged 2129f70bb).

## Measured
adapters/__init__.py:117 judges a path-shaped bin with os.path.exists in the RESOLVER process cwd while Popen runs in another cwd -> over-refusal of a valid relative bin, untested; build:bin-adapters-init not re-versioned with its payload (PASS 10 c5)

## Testable claim
a relative bin valid in the spawn cwd resolves; an invalid one refuses by name; the build node is versioned with the payload

## CORRECTIVE DH.549 -- closes mur-director-engine-23 DH.516-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-a-path-shaped-bin-res-a00-42e99d0a tip 7cabf1f8f (branch de-base-549; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. Machine verdict contradicts the parent's own demotion in the same node (.agi/nodes/experiment/a00-8bbde2ea-933463.md:22)
2. 2. New parameter has no production caller (extensions/agi/bin/adapters/pi_adapter.py:52) -- dead code in production
3. 3. Undisclosed behaviour change for three-arg callers (.agi/nodes/experiment/.../__init__.py:125) -- a relative cell that exists in the resolver's cwd is now returned ABSOLUTE
4. RED TRANSCRIPT UNDERCOUNTS, AND THE MISSING TEST IS THE ONE THAT PROVES THE 3-ARG CHANGE. The node's evidence block (a00-8bbde2ea-933463.md:94) claims `5 failed, 1 passed in 0.18s`. I extracted the committed test at 7cabf1f8f and the pre-fix payload at a947f5a73 into a /tmp sandbox (no repo mutation, env -u TMUX -u TMUX_PANE) and re-ran: 6 failed, 1 passed. The sixth is test_omitting_cwd_preserves_todays_behaviour (test_adapters_spawn_cwd.py:139), which fails RED precisely because the three-arg path's answer MOVED. So the block that is used to argue 'the new keyword is the only thing that moves it' (node:95-97) in fact contains the counter-evidence, and the reported tally is wrong.
5. A GREEN TEST WHOSE NAME ASSERTS THE OPPOSITE OF ITS BODY. test_adapters_spawn_cwd.py:139-150 is named `test_omitting_cwd_preserves_todays_behaviour`; its docstring at :142-143 says the answer 'now resolves to the concrete path Popen will actually exec' and it asserts `== str(resolver_cwd / 'tools' / 'pi')`, an ABSOLUTE path the pre-fix code never returned. A regression guard whose name promises preservation while pinning a behaviour change is the green-test-requires-a-defect shape, and it is the only place the change is stated accurately -- the code comment at __init__.py:118-120 and the node body both assert the opposite.
6. MACHINE-FIELD LINE BUDGET DOES NOT REPRODUCE. production_lines: 11 (a00-8bbde2ea-933463.md:14, repeated at :132, :142 '11 added / 7 removed lines (3 comment lines, 1 signature line, 7 body lines)' and in the Agent Notes :155, and in the build node v2 table whose rows sum to 11). `git diff --numstat a947f5a73 7cabf1f8f -- extensions/agi/bin/adapters/__init__.py` is 14 added / 7 removed: the signature costs 2 lines, not 1, and the body costs 9, not 7. A number the node says it read from numstat, cited three times, is off by three.
7. THE UNNAMED-REFUSAL SHAPE STILL EXISTS FOR EVERY LIVE CALLER (residue of the refuted defect 4, stated correctly). With no cwd=, `tried` has length 1, so the clause at __init__.py:128-129 is skipped and a relative cell that exists nowhere yields `cannot resolve binary 'tools/pi': does not exist; set $PI_BIN to override` -- no cwd named. Measured. That is precisely the shape hypothesis:a-path-shaped-bin-resolves-in-the-spawns-cwd is about, and it is what rotate.py:942/946, workflow.py:1438, heal.py:125 and harness_template.py:250 still get. It is only untouched because of defect 2; it is not fixed for anyone.
8. BUILD-CONTRACT NOT REGENERATED, AND IT NEVER COVERED THE CHANGED FUNCTION (low, pre-existing). .agi/nodes/build/bin-adapters-init.md:22-71 keeps the level3-generated block whose `outputs` list only AdapterError (line 38), load (42), resolve (82), parallelism (141) -- `resolve_bin` is absent and the line numbers are 30+ lines stale. The round added 7 net lines to the payload without a rescan, so the canonical record of the file does not describe the function the round changed. Pre-existing drift (the block was already stale at a947f5a73), correctly not hand-edited, but it means the v2 table is currently the only accurate description of the file's public API.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_adapters_spawn_cwd.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/adapters/__init__.py · extensions/agi/tests/test_adapters_spawn_cwd.py · .agi/nodes/build/bin-adapters-init.md · .agi/nodes/experiment/a00-8bbde2ea-933463.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 7cabf1f8f · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.549: mur-director-engine-23 DH.516-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
