---
id: experiment:dg2mvp-g13141-check
mint_id: 0ab5d15953dd419095663af9960c5eb9
type: experiment
parents:
  - hypothesis:g1314-dg5-01-corrective-one-load-one-check-one-resolver
next_edges: []
edited_by: director-general-2
scaffold_hash: cebcebd77562bfec
season: 2
title: "g13141 post-build check: DG5.01 corrective lands one load, one target check, dry == live target refusal (goal:g1.31.4.1 as re-scoped)"
town: core
---
# experiment:dg2mvp-g13141-check

## g13141 post-build check: goal:g1.31.4.1 (landed 88ddd2ca08, tip e22a38df4c), judged at HEAD

Scope: goal:g1.31.4.1 as re-scoped (falsifier 2 in its THOUGHT). The dropped conjunct "a --branch dry run reads the graph a live --branch spawn renders from" is ROUTED to goal:g1.31.4.1.1 (horizon) and is NOT judged here. No later commit touches dispatch.py / zoom.py after 88ddd2ca08 (git log 88ddd2ca08..HEAD on both: empty).
Method: HEAD archive tree in /tmp/dg2mvp/g13141/tree (base tree 8ea76d2488 in /tmp/dg2mvp/g13141/base); probes in-process with call-counting wrappers on the module globals; dry runs only, no spawn.

| # | command / test | observed |
|---|---|---|
| 1 | counting wrappers on zoom._load_wired_graph and zoom.target_resolves, zoom.main in-process (probe1.py), small kid / small parent / numeric 2 / numeric 1 | load=1 check=1 for every render with a target (small kid, small parent, L2); load=1 check=0 for L1 with no target. Bogus target: rc 1, still load=1 check=1, one ERR line, 0 tracebacks |
| 2 | same wrappers around dispatch.main --dry-run (probe1.py) | small: load=1 check=1 rc 0; auto+target: 1/1; big: 0/0; small bogus: 1/1 rc 1; small parent: 1/1. One load and one check per dry dispatch |
| 3 | git grep has_node zoom.py dispatch.py (F3) | zoom.py:658 (inside target_resolves) only; dispatch.py has_node hits are parent-id scoring, not the target check |
| 4 | dry vs live matrix (probe2.py): tier x level{small,auto,big} x target{x, vision:alive, bogus}; live side = resolve_auto_level -> zoom_command -> run zoom.py (up to, never past, the spawn), auto drawn both ways | kid: 9/9 agree (auto: dry refuses iff ANY draw refuses = by design, hypothesis F2). parent: small 3/3 agree; auto+big draw and big refuse live with "--tier parent has no shape at --level big" (zoom.py main, pre-existing, a tier/level refusal, not a target one) and dry exits 0 |
| 5 | dry --level auto --target bogus (F2) | rc 1, "ERR: no context for target 'bogus:zzz' at level small: ..." on stderr; fixture project: same for small and small+parent tier |
| 6 | --branch --dry-run from INSIDE a linked worktree (probe in /tmp repo M + worktree W, trunk-only node, worktree-only node) | from W: --branch wt-only rc 0 and mainonly rc 1, same verdicts without --branch; from M: the mirror. Printed `branch: season2/loops/<slug>-<id> base=<W's branch> worktree=<M>/.agi/worktrees/<id>` (git_common_root of W = M); no worktree created (worktree list unchanged) |
| 7 | zoom.py CLI, ZoomUnavailable sites: small kid bogus, small parent bogus, L2 bogus, empty graph dir | rc 1 each, one `ERR:` block on stderr, 0 tracebacks; dry on the empty-graph dir: rc 1 + the dispatch refusal line. (Malformed config.json is a JSONDecodeError traceback, pre-existing, not a ZoomUnavailable) |
| 8 | git_common_root counter around dry runs | dry --branch = 2 calls, plain dry = 1 (provisioning key read, pre-existing); the branch line adds exactly ONE (branch_worktree_link). Live helper branch_worktree_for_spawn = 2 at base AND at HEAD (1 direct + 1 via guard_cell in ram_worktrees_dir, g7.16.1.5.4 code) |
| 9 | F4 git ls-tree HEAD caveat_residue.py test_caveat_residue.py; git grep caveat_residue | 0 files, 0 hits (F4 not fired) |
| 10 | F5 git grep dry[0-9]+- and \.py:[0-9]+ on dispatch.py zoom.py; dry stdout with --branch and plain | 0 hits in source, 0 nonce and 0 line cites in printed output; one live-grammar id `a<NN>-<hex8>` (test_dry_agent_id_uses_the_live_id_grammar) |
| 11 | DETACHED_HEAD_REFUSAL: git grep | one constant (dispatch.py:1392), used by the live ERR and the dry `base=NONE (...)` line. Dry on a detached HEAD exits 0 with the refusal text printed; live exits 1 (branch-slice residue "worded twice" is closed; the rc difference was never a conjunct) |
| 12 | CEILING git show --numstat 88ddd2ca08 (merge; first-parent diff vs trunk 8ea76d2488) | dispatch.py +112/-20 (net +92), zoom.py +50/-14 (net +36), test_dispatch_dry_run +229/-4, test_zoom +44, 5 small tests +5 each. Round chain adb1bd23fd..e22a38df4c (caveat -62/-72 excluded): dispatch +67/-36 = +31, zoom +13/-6 = +7 -> production NET +38 vs ceiling +10 (OVER); tests added 94+44 = 138 vs 70 (OVER). DH.DG3.56 slice b8fb98359e..e22a38df4c: dispatch +15/-17 = -2 (<= 0 OK), tests +33-3 +15-26 = net +19 (<= +20 OK). The chain overshoot is recorded in the hypothesis node itself ("the chain was +40 vs +10") |
| 13 | strict-xfail rows of mine for this row (git grep xfail in test_dispatch_dry_run/test_zoom/test_dispatch; git log --all -S xfail on both files) | none exist and none ever landed: nothing to un-mark or compare |
| 14 | pytest from the HEAD tree, one file per run, flock | test_dispatch_dry_run 36 passed 1 failed (test_claude_advisor_dry_run_resolves_model_effort_and_env: BriefError "advisor brief needs a vision node"); test_zoom 43 passed; test_dispatch 139 passed; model_allowlist 7; no_stdout_secrets 8; geometry_config 18; mem_cap_override 8; ring_cli_seam 11, all green |
| 15 | same advisor test on the BASE tree 8ea76d2488 | same test, same BriefError: red at base = INHERITED (DH.DG3.56 item 6 already names it) |

Pinning tests in the suite (green): test_each_render_path_loads_once_and_checks_once, test_render_level_refuses_through_target_resolves (zoom); test_auto_level_refuses_a_bad_target_a_live_round_would_refuse, test_resolve_auto_level_is_the_one_resolver_both_paths_call, test_split_cell_resolves_through_the_one_helper, test_branch_dry_run_checks_the_dispatchers_own_checkout, test_dry_agent_id_uses_the_live_id_grammar, test_dry_run_names_branch, test_dry_run_refuses_unknown_target (dry_run).
Goal falsifier 1 (pytest -k "dry_run_names_branch or dry_run_refuses_unknown_target" >= 2 tests): both collected and passed inside the file's 36 green.
