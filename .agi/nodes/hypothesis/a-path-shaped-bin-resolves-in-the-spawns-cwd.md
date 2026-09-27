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

## CORRECTIVE DH.567 -- closes mur-director-engine-26 DH.549-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-a-path-shaped-bin-res-a00-60e5d07e tip dab79e47c (branch de-base-567; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. Absolute-cell refusal now claims a cwd was consulted (adapters/__init__.py:139)
2. 2. cwd= parameter has no production caller after two rounds (adapters/__init__.py:75)
3. 3. build:bin-adapters-init v2 row 2 misdescribes the payload this round changed (.agi/nodes/build/bin-adapters-init.md:88)
4. 5. Superseded node retains a false RED tally and line count in its body, corrected only by an appended note (a00-8bbde2ea-933463.md:246)
5. adapters/__init__.py:124 `here = os.getcwd() if os.path.isdir('.') else None` — the guard does not guard: with the resolver's cwd deleted, os.path.isdir('.') is still True (measured, os-only snippet) and os.getcwd() raises FileNotFoundError, which propagates out of resolve_bin uncaught, naming no harness, no cell and no $env_var — the exact unnamed death the docstring at :86-93 says this function exists to prevent. It also falsifies the reviewing parent's own probe note that 'the os.path.isdir(".") guard holds' (a00-96302aef:17, :231-232). Pre-existing: :124 is a context line, unchanged by this diff, so it is residue, not a demotion. Probe I would run and did NOT: a committed test that chdirs into a tmp_path dir, rmdir's it, and asserts the refusal names the harness and $PI_BIN (needs no engine CLI, only tmp_path); the pre-fix comparison would need a /tmp checkout of payload a947f5a73, which I did not do.
6. adapters/__init__.py:118-119 — the shipped comment says a relative cell is judged against the SPAWN's cwd 'not this process's', but :125 keeps `here` as the live second candidate and the shipped test test_adapters_spawn_cwd.py:77-90 pins that a cell valid only in the RESOLVER's cwd is returned as an absolute join. Comment contradicts code and its own test; wording-level, low.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_adapters_spawn_cwd.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/adapters/__init__.py · extensions/agi/tests/test_adapters_spawn_cwd.py · .agi/nodes/experiment/a00-8bbde2ea-933463.md · .agi/nodes/experiment/a00-96302aef-adf2d5.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over dab79e47c · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

## CORRECTIVE DH.584 -- closes mur-director-engine-30 DH.567-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-a-path-shaped-bin-res-a00-5a797dd1 tip 1363f84d8 (branch de-base-584; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
0. FIRST (third round this conjunct is unmet): wire the ONE live production caller -- adapters/pi_adapter.py's resolve_bin call -- to pass the spawn's cwd (the branch worktree the spawn runs in), so the hypothesis's central conjunct is true of the running system; a committed test pins that pi_adapter hands resolve_bin the spawn cwd (monkeypatch, no spawn). The other three adapters: name them OUTSIDE if their call differs.
1. 2. refusal mislabels the spawn join as the resolver's cwd when spawn is given and the resolver cwd is deleted
2. 3. the grid holds no version of the build node or its payload for this round
3. 4. build node v2 table `lines` column stale (8) for the branch it now describes
4. Four paths in the round's own OUTSIDE table DO NOT EXIST. `experiment/a00-b1695286-6be4b3.md:78-81` cite `extensions/agi/bin/pi_adapter.py:52`, `.../claude_code_adapter.py:274`, `.../grok_bot_adapter.py:39`, `.../copilot_cli_adapter.py:88`; `git cat-file -e 1363f84d8:extensions/agi/bin/pi_adapter.py` and the other three all return DOES NOT EXIST — the `adapters/` segment is dropped. The line numbers are right (`git show 1363f84d8:extensions/agi/bin/adapters/<f>.py | grep -n 'return adapters.resolve_bin'` -> 52/274/39/88), and the same node's pasted grep at :52-57 prints the correct prefixed paths, so the table is the wrong copy. A follow-up agent grepping those four paths finds nothing; `links.py links` will not catch it (inline code spans, not links).
5. The prescribed follow-up VALUE is wrong for the hop it names. `experiment/a00-b1695286-6be4b3.md:78` and `build/bin-adapters-init.md:97-99` say the hop 'would need `cwd=str(branch_root)`'. But the reader behind that hop was never opened: `adapters/pi_adapter.py:52` is called from `build_command` (:227), which `restart()` also calls (pi_adapter.py:329-330) before spawning at pi_adapter.py:349 with `cwd=str(_restart_cwd(sess_dir, agent_record))` (:265-288) — so one resolve_bin hop feeds TWO different spawn cwds (dispatch's `branch_root` at dispatch.py:2861, and the adapter restart's `_restart_cwd`). The same holds for claude_code_adapter.py:889 (`_root_of(sess_dir)`), copilot_cli_adapter.py:385 and grok_bot_adapter.py:178. Wiring the recorded one-liner would give the restart path the wrong cwd.
6. A GREEN TEST PINS A DEFECT. `extensions/agi/tests/test_adapters_spawn_cwd.py:77-90` (`test_the_resolver_cwd_is_still_tried_after_the_spawn_cwd`) requires the resolver-cwd fallback, and `adapters/__init__.py:141-148` returns the resolver-cwd join when the spawn join is missing. So once `cwd=` IS wired, a branch worktree that does not contain `tools/pi` silently gets the MAIN checkout's binary instead of the refusal that names both cwds — the same branch-isolation partial break named at `adapters/pi_adapter.py:266-275` (`hypothesis:l3-branch-isolation-partial-break`). Harmless today (zero callers) and it is a deliberate 'no regression in the other direction', but the test makes it permanent and the round's own build-node row :88 calls the fallback the intended behaviour.
7. Comment undercounts the invariant it protects: `adapters/__init__.py:119-121` says 'every three-arg caller (the four adapter modules) is UNCHANGED', but the same node's grep (`experiment/a00-b1695286-6be4b3.md:52-57`) lists nine three-arg sites — the four adapter wrappers plus rotate.py:942, rotate.py:946, workflow.py:1438, heal.py:125, harness_template.py:250. Wording only (the three-arg byte-equality is pinned by test:179-192), but the reader stops believing the comment covers heal/rotate.
8. Coverage note behind defect 2: the new try/except at `adapters/__init__.py:133-140` is exercised only on the 3-arg path (test:157-176). The probe I WOULD run (NOT run — it is the round's own g4 case, and no committed test covers it) is a spawn+deleted-resolver-cwd resolve_bin call asserting the message labels the survivor 'spawn cwd', not 'this cwd'.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_adapters_spawn_cwd.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/adapters/__init__.py · extensions/agi/bin/adapters/pi_adapter.py · extensions/agi/tests/test_adapters_spawn_cwd.py · .agi/nodes/build/bin-adapters-init.md · .agi/nodes/experiment/a00-8bbde2ea-933463.md · .agi/nodes/experiment/a00-b1695286-6be4b3.md (write.py) · the kid's own node
CEILING   HARD CAP: 1 kid · <= 15 production lines net over 1363f84d8 · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.584: mur-director-engine-30 DH.567-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
