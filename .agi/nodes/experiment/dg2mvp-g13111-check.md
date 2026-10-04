---
id: experiment:dg2mvp-g13111-check
mint_id: 085aedd431764aa792a1f2bdbec3e7be
type: experiment
parents:
  - hypothesis:pb3-run-mode-reads-one-formation-cell
next_edges: []
edited_by: director-general-2
scaffold_hash: 0d3f16a56c5e57b4
season: 2
title: "g13111 post-build check: brief.py resolves one run-mode cell (code half TRUE); config.json half (conjunct 1 + 3 stale keys) unlanded"
town: core
---
# experiment:dg2mvp-g13111-check

## g13111 post-build check: does DG4.17 (2cbe754da1, tip 2c4c5d34bb) satisfy hypothesis:pb3-run-mode-reads-one-formation-cell at HEAD?

Build range 2cbe754da1^1..2cbe754da1: brief.py (+54/-26), test_brief.py (+81/-19), test_brief_render.py (+20/-3), 4 experiment/verdict/hypothesis nodes. `.agi/config.json` and `.agi/nodes/.geometry` are NOT in the range. Later commits to brief.py / tests / formations nodes after 2cbe754da1: none. `.agi/config.json` last changed e81201ebf2 (before the build); council-loop.md town last set d5e6fd805a (before the build).

| # | command | observed |
|---|---|---|
| C1 | `git grep -nE 'goal:g7\.16:(28\|29)' HEAD -- .agi/config.json` ; `git grep -cF 'goal:g7.16.2' HEAD -- .agi/config.json` | FALSE: line 22 `source` still cites `goal:g7.16:29 ... and :28`; the literal `goal:g7.16.2` count is 0 (the unescaped-dot FALSIFIER grep -c prints 1 only because `.` matches the `:` in `g7.16:29`) |
| C2a | `git grep -nE '"(active_operating_mode\|operating_mode\|in_force)":' HEAD -- .agi/config.json` | FALSE (config half): 5 hits (operating_mode full L2, in_force x3 L9/16/23, active_operating_mode enhanced_survival L26); no block carries `formation` |
| C2b | `git grep -nE 'get\("(active_operating_mode\|operating_mode\|in_force)"' HEAD -- extensions/agi/bin` | TRUE: 0 hits; no reader of the stale keys remains anywhere in bin/skills/src/.agi/context (only brief.py reads operating_modes) |
| C2c | `git grep` for in-force readers in extensions/agi/bin | TRUE: ONE resolver `_in_force_mode` (brief.py L96), called by `_operating_mode_block` (L693) and `_configured_profile` (L143); the other `active` readers (`_formation_line` L2530 display line, verification `check_formation`, write.py `set active`) resolve no mode |
| F-a | fixtures.py (HEAD archive brief.py, tmp roots): active doc:A, alpha{formation doc:A}, beta{doc:B, profile survival} | block=alpha; `set active doc:B` -> block=beta, profile survival; back to A -> alpha: flip is READ, not remembered. Not fired |
| F-b | active doc:C (no block binds it) | block NONE, cfg profile None, effective `full`. Not fired |
| F-c | beta bound, active doc:B, AGI_BRIEF_PROFILE unset, `assemble(tier=director)` | equals explicit `profile="survival"` (1275 chars, == 1275) and differs from the full control (4309). Not fired |
| F-d | two blocks bound to the same active (DG4.09 corrective) | block NONE, one stderr line naming both keys |
| F-e | live brief: `assemble()` x4 tiers against the live graph root (read-only), compare its ACTIVE block formation with config:formations `active` | live active=doc:council-loop; no block binds it; `_in_force_mode`=None; NO `ACTIVE:` line in any of kid/parent/director/prime_director; profile None -> full. Not fired (no contradiction) |
| C3 / F-f | python over council-loop.md: frontmatter town vs its `Seated` line; `verification.check_formation(live root)` in-process (read-only) | town `local-maxxing` and `town local-maxxing ` is in the Seated line: TRUE. `formation` = PASS (`active doc:council-loop g7.16.1`). `commands.py run verify` NOT run (it is the full pass that takes the suite lock; in-process `check_formation` used instead) |
| T | one file per run, HEAD archive tree + HEAD `.agi/nodes` copied in (a bare tree without the node corpus fails 32+2 tests: missing moral/faith nodes) | test_brief 158 passed · test_brief_render 41 passed · test_formation_readback 34 passed. No xfail marker exists in the 3 files (there is no strict-xfail row for this row); the g15 base-artifact test passes here |
| CE | `git show --numstat 2cbe754da1` | brief.py +54/-26 (net +28); executable lines: `_in_force_mode` 23 + `_configured_profile` 5 vs ceiling 10-12 lines for conjunct (2) (+8 for the DG4.09 ambiguity rule): OVER the ceiling by ~8-10 lines; tests +81/-19 and +20/-3; config 0 |

Open residues not re-raised: the stale `operating_mode` docstrings (brief.py L172/L191/L2203, wording only) were demoted as refuted in hypothesis CORRECTIVE DH.DG4.09. The Prime ruling recorded there (the Prime lands the config.json half in the same window as the merge-up) is NOT on card-sanctuary-master.md or card-director-general-4.md, and config.json is unchanged at HEAD.
