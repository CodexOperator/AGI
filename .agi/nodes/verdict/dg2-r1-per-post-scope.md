---
id: verdict:dg2-r1-per-post-scope
mint_id: 5741b2dff566475b873e2e6ad47dbeaf
type: verdict
parents:
  - experiment:dg2-r1-per-post-scope-baseline
  - hypothesis:every-post-launch-gets-its-own-scope-by-construction
next_edges: []
confidence: 0.65
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-r1-per-post-scope-baseline
scaffold_hash: 1aa317cbe888a5da
season: 2
title: "R1: lean proved at 65 -- grouped cutover works on dummies (one kill = one post) but its helper is 38 lines vs +20; heal.py must join the file scope; agi.slice cap is shared"
town: core
verdict: inconclusive_lean_proved:65
---
# verdict:dg2-r1-per-post-scope

## Verdict: inconclusive_lean_proved:65 (director-general-2, council bundle 3 stage 2)
| conjunct | on the trunk (experiment:dg2-r1-per-post-scope-baseline) | decided by |
|---|---|---|
| `_launch_window` ensures agi-rc in its OWN agi.slice scope when absent | FALSE: 0 new-session sites, 0 `_ensure_tmux_session` | test_rotate.py::test_r1_launch_window_ensures_agi_rc_in_its_own_scope_first |
| `_shell_cmd` wraps every post argv in a scope | FALSE: no systemd-run in either `_shell_cmd` line | test_rotate.py::test_r1_every_post_argv_is_scoped_even_when_cap_is_none |
| cmd_spawn, heal recover and rotate inherit it with no per-caller code | HALF: the argv wrap reaches heal (spawn_window dry-run -> `_shell_cmd`, heal.py:3267), the tmux ensure does NOT (heal.py:3036 is its own new-window) | Falsifier 2 by `git grep '"new-window"'` (2 sites today) + a heal-side ensure call |
| cap None still yields a scope, never the unwrapped argv | FALSE: mem_cap.py:318-319 returns the same object | test_r1_every_post_argv_is_scoped_even_when_cap_is_none (post path only) |
| a post's cap is its OWN cell, never the 2G dispatch cap | no post cell; `resolve_memory_cap` = 2G (config.json:150) | review of the config.json cell + its resolver (no row: the cell name is DG3's) |
| one kill of a scoped dummy takes only it; grouped cutover = one kill one post | TRUE on dummies (rows 8, 11, 12); service count unchanged every time | test_rotate.py::test_r1_cutover_plan_gives_each_post_tree_its_own_scope + ::test_r1_cutover_dummy_one_kill_is_one_post |
Lean: the launcher half is ~25 lines and mechanical; the risk is the cutover helper -- my grouped prototype (/tmp/dg2b3/r1/cutover_sketch.py, green on dummies) is 38 code lines vs the +20 helper ceiling, so as written R1 lands the named FALLBACK or needs the helper ceiling raised to ~40. The live cutover is NOT this round's: it waits for the owner's word after PASS B3 closes (banked on doc:card-belam §6); Falsifier 2 closes only then.
CORRECTIONS: (1) FILE SCOPE must add heal.py (an ensure call before heal.py:3036 in `_launch_recovered`, as goal:g6.41.1 P1 says), else "no per-caller code" is false for heal recover. (2) cap-None guard is mem_cap.py:318 (return :319), not :317. (3) "the cap-None scope path in wrap_argv" must NOT change wrap_argv's shared contract: 3 tests pin `wrap_argv(argv, None) is argv` (test_launch_memory_cap.py:132, test_mem_cap_tasks_max.py:243, :289-295) for dispatch/workflow/heal-pi; use a post-only arm (kwarg/scope helper). (4) AttachProcessesToUnit needs Delegate=yes on the target (refused otherwise, row 9); StartTransientUnit(PIDs, Delegate=yes) moves a group in one call. (5) slice names with '-' nest (dg2-r-dummy.slice -> dg2.slice/dg2-r.slice/...): keep the cell `agi.slice`. (6) agi.slice has MemoryHigh 9.26G / MemoryMax 10.29G shared with agi-work/agi-engine: moving tmux + every post under it puts them under that cap -- name it.
RISK for DG3 + the council (not a conjunct): `agi.slice` already exists on this box with MemoryHigh 9.26G / MemoryMax 10.29G SHARED with agi-work + agi-engine -- moving tmux and every post under it puts all posts under that one cap (one OOM-kill decision for the whole town). Decide the target slice (a dedicated posts slice, or the cap raised) before the cutover. Trap: a slice name with `-` nests (`dg2-r-dummy.slice` -> `dg2.slice/dg2-r.slice/...`). The prototype helper lives only in /tmp (dg2b3/r1/cutover_sketch.py) -- DG3 rebuilds it, it is not evidence.
