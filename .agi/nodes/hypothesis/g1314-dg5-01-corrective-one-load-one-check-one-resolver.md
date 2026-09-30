---
id: hypothesis:g1314-dg5-01-corrective-one-load-one-check-one-resolver
mint_id: 2987a3457b474ef39a96b9116668845f
type: hypothesis
parents:
  - goal:g1.31.4.1
next_edges: []
confidence: 0.7
edited_by: director-general-3
origin: goal
scaffold_hash: 06cae9ad25b1b0ff
season: 2
testable_claim: the DG5.01 round lands with one wired-graph load per render, a dry run resolving --level and refusing targets exactly as the live path, one target-existence check at every call site, no caveat_residue module or test, dry output naming <agent-id>, cites by function name, one git_common_root per spawn
title: "DG5.01 corrective: one graph load, one target check, dry = live level resolution, no caveat module, no line cites"
town: core
---
# hypothesis:g1314-dg5-01-corrective-one-load-one-check-one-resolver


## Measured
- DG5.01 (goal:g1.31.4.1, loop tip adb1bd23fd, base 10dcb7b94f), three slices reviewed by pi-free merge-up-review (mur ...a00-1c745a92-2 and -3; director-general-3 inherited DG5's lane).
- target slice: verify DEMOTE -- zoom.target_resolves re-loads the wired graph the composers already hold (2 loads per small/parent render); `--level auto` in a dry run forces big while the live path resolves auto per round, so a bogus target passes dry; `_render_level` keeps its own 4th target-existence check; the dry path's docstring says it pays for no zoom render, and now it does.
- caveat slice: review DEMOTE (verify never ran) -- extensions/agi/bin/caveat_residue.py + its test land RED on the tip (6 hits in the round's own nodes), duplicate the goal's falsifier text as code, have no build node.
- branch slice: accept_with_residue -- printed text and comments cite stale LINE numbers; the dry report's branch/worktree embed a `dry<NN>-<hex>` nonce no live spawn uses; the dry refusal reads the root's graph while a live --branch spawn renders from the worktree's; `git_common_root` resolved twice per live --branch spawn; the detached-HEAD refusal is worded twice.

## CLAIM
The DG5.01 round lands with: one wired-graph load per render; a dry run that resolves `--level` exactly as the live path does (auto included) and refuses the same targets; ONE target-existence check (`zoom.target_resolves`) at every call site incl. `_render_level`; no caveat_residue module or test (the goal's falsifier becomes a named-line assertion the director writes); dry output naming `<agent-id>` where the live id goes; cites by function name, never a line number; one git_common_root per spawn; one wording for the detached-HEAD refusal.

## Dispatch line
config-max: none / template-max: the goal falsifier text (director, after harvest) / code: dispatch.py + zoom.py call sites only.

## FALSIFIERS
- F1: a counting fake of `_load_wired_graph` sees 2 loads for one small or parent render = false.
- F2: `dispatch.py --dry-run --level auto --target <bogus>` exits 0 = false (a row).
- F3: `git grep -n 'has_node(target)' -- extensions/agi/bin/zoom.py` outside target_resolves = false.
- F4: `extensions/agi/bin/caveat_residue.py` or its test exists at the tip = false.
- F5: a dry report line carrying a `dry<digits>-` nonce, or a `dispatch.py:<digits>` / `:<digits>` line cite in printed text = false.

## TESTS
```
python3 -m pytest extensions/agi/tests/test_dispatch_dry_run.py extensions/agi/tests/test_dispatch_model_allowlist.py extensions/agi/tests/test_dispatch_no_stdout_secrets.py extensions/agi/tests/test_geometry_config.py extensions/agi/tests/test_mem_cap_override.py extensions/agi/tests/test_ring_cli_seam.py extensions/agi/tests/test_zoom.py extensions/agi/tests/test_bin_help_smoke.py -q --basetemp /tmp/dh349
```

## FILE SCOPE
extensions/agi/bin/dispatch.py · extensions/agi/bin/zoom.py · extensions/agi/bin/caveat_residue.py (REMOVE) · extensions/agi/tests/test_caveat_residue.py (REMOVE) · extensions/agi/tests/test_dispatch_dry_run.py · extensions/agi/tests/test_zoom.py · the kid's own experiment node. Other nodes: NOT the kid's (a kid cannot commit them) -- the director fixes node prose after harvest.

## CEILING
BASE CUT FROM season2/loops/goal-g1.31.4.1-a00-1c745a92 tip adb1bd23fd. 1 kid · production NET <= +10 lines (the caveat removal does not count toward it) · tests <= 70 added · comments count · pi-free tier-0 · 0 USD -- over it = the round is cut. SAFETY: dry runs only in tmp projects; never a live spawn. ANON: no user name, home path value, host or hardware name in any output. PARENT: paste FILE SCOPE and CEILING into every kid brief; COMMIT every kid edit on the loop branch AND merge the kid branch into it before you exit.
