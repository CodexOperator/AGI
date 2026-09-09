---
id: hypothesis:l3-engine-files-outside-the-grid
mint_id: eb52f664dcd7448ab482abbb2b555a43
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-director
scaffold_hash: e077642e6d37617e
season: 2
testable_claim: After the change, every tracked engine file that the project intends to grid-version has a build node whose payload_ref resolves to it, proven by a checker that enumerates tracked engine files, subtracts every declared payload_ref, and exits nonzero on any remainder outside a declared exclusion list -- with the remainder at zero and level3.py gaining an additive mode that mints missing nodes without pruning or resurrecting anything.
thought_session: sanctuary-director-genVI
title: "Seventy-two tracked engine files have no build node, so their bytes are outside the grid entirely: rotate.py, season.py, send.py and write_guard.py among them, and the discoverer that would mint them is forbidden to run"
---
<!-- BODY:BEGIN -->
# hypothesis:l3-engine-files-outside-the-grid

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
BUILD, NOT A PROBE. YOUR ARTEFACT IS A DIFF.

THE OWNER APPROVED THIS DIRECTLY, 2026-09-08, verbatim: 'I'm fine doing the item49 of section 6 where we do a brief per file that's outside node.' Every file below is named individually, which is what 'per file' buys; they are worked as ONE class because 72 separate hypothesis nodes asserting 'mint a node for file X' would be 72 nodes of pure bookkeeping in a graph whose whole point is that a node carries a thought. That granularity call is the director's, is recorded here rather than hidden, and the owner can reverse it in one line.

THE GAP, measured 2026-09-08 by set subtraction, not by estimate. Every payload_ref declared anywhere under .agi/nodes (live and deprecated) was collected: 231 distinct paths. Every tracked file under extensions/, skills/, src/ and bin/ was collected: 252. The difference is 72 files with NO build node, whose bytes are therefore outside the grid entirely -- grid.py commit --all versions nothing for them, grid.py payload cannot read them back, and stitch.py --from-grid could not materialise them.

WHY IT HAPPENED, and it is structural rather than neglect. level3.py is the discoverer that mints build nodes from git ls-files, and trap 0i forbids running it without --dry-run because it would prune 18 deprecated build nodes and mint parentless nodes for the .claude/workflows/*.js symlinks. So every engine file created since the last scan has quietly accumulated with no node, and the only tool that could fix it is the one nobody is allowed to run.

THE 72 FILES, grouped:

ENGINE MODULES (18) -- the load-bearing half
  extensions/agi/bin/briefing.py
  extensions/agi/bin/commands.py
  extensions/agi/bin/derive-commands.py
  extensions/agi/bin/drift_check.py
  extensions/agi/bin/frontier.py
  extensions/agi/bin/glitch_master.py
  extensions/agi/bin/inject.py
  extensions/agi/bin/pi_edit_forgiveness.py
  extensions/agi/bin/plan_master.py
  extensions/agi/bin/provisioning.py
  extensions/agi/bin/rotate.py
  extensions/agi/bin/season.py
  extensions/agi/bin/seat_status.py
  extensions/agi/bin/send.py
  extensions/agi/bin/sensei.py
  extensions/agi/bin/spawn_budget.py
  extensions/agi/bin/telemetry_rollup.py
  extensions/agi/bin/write_guard.py

BRIEFS (2)
  extensions/agi/briefs/master-sensei-duties.md
  extensions/agi/briefs/prime-director-successor.md

GIT HOOKS (2)
  extensions/agi/hooks/agent-git/pre-commit
  extensions/agi/hooks/agent-git/pre-push

ONE-OFF SCRIPTS (2)
  extensions/agi/scripts/chat_vs_briefing_proxy.py
  extensions/agi/scripts/chat_vs_briefing_tradeoff.py

SOURCE (1)
  extensions/agi/src/renderers/scatter.py

WORKFLOWS (4)
  extensions/agi/workflows/agi-deep-search.js
  extensions/agi/workflows/agi-l3w-route-probe.js
  extensions/agi/workflows/deep-search.json
  extensions/agi/workflows/l3w-route-probe.json

TEST FIXTURES (14) -- probably EXCLUDE, they are data
  extensions/agi/tests/fixtures/nested/level_a/level_b/level_c/leaf.md
  extensions/agi/tests/fixtures/nested/level_a/level_b/middle.md
  extensions/agi/tests/fixtures/nested/level_a/outer.md
  extensions/agi/tests/fixtures/nested/top.md
  extensions/agi/tests/fixtures/nodes/sample.json
  extensions/agi/tests/fixtures/nodes/sample.md
  extensions/agi/tests/fixtures/schemas/[hypothesis].md
  extensions/agi/tests/fixtures/schemas/example.json
  extensions/agi/tests/fixtures/schemas/example.md
  extensions/agi/tests/fixtures/walk_test/a/file_a.md
  extensions/agi/tests/fixtures/walk_test/b/file_b.md
  extensions/agi/tests/fixtures/walk_test/b/file_c.md
  extensions/agi/tests/fixtures/walk_test/file_top.md

TESTS (29)
  extensions/agi/tests/test_agi_bin_absent.py
  extensions/agi/tests/test_agi_env_strip.py
  extensions/agi/tests/test_bin_help_smoke.py
  extensions/agi/tests/test_briefing.py
  extensions/agi/tests/test_claude_code_adapter.py
  extensions/agi/tests/test_commands.py
  extensions/agi/tests/test_dispatch_dry_run.py
  extensions/agi/tests/test_edit_tool_forgiveness.py
  extensions/agi/tests/test_failures.py
  extensions/agi/tests/test_frontier.py
  extensions/agi/tests/test_git_commit_guard.py
  extensions/agi/tests/test_glitch_master.py
  extensions/agi/tests/test_ladder_node.py
  extensions/agi/tests/test_links.py
  extensions/agi/tests/test_pi_edit_forgiveness.py
  extensions/agi/tests/test_plan_master.py
  extensions/agi/tests/test_post_wire.py
  extensions/agi/tests/test_provisioning.py
  extensions/agi/tests/test_real_adapter_restart.py
  extensions/agi/tests/test_rotate.py
  extensions/agi/tests/test_season.py
  extensions/agi/tests/test_seat_status.py
  extensions/agi/tests/test_send.py
  extensions/agi/tests/test_sensei.py
  extensions/agi/tests/test_shared_state_worktree.py
  extensions/agi/tests/test_spawn_budget.py
  extensions/agi/tests/test_telemetry_rollup.py
  extensions/agi/tests/test_workflow.py
  extensions/agi/tests/test_write_guard.py

TESTS, renderers (1)
  extensions/agi/tests/renderers/test_scatter.py

READ THE GROUPS AS A DECISION, NOT A LIST. The 18 bin modules are the load-bearing half and are not arguable: rotate.py is the file the entire seat ladder rotates through and the file whose orphaned diff nearly vanished in an earlier session; season.py runs the ladder; send.py is the comms verb; write_guard.py is the thing that catches unsanctioned writes. The 14 test fixtures are almost certainly a legitimate exclusion -- they are data, not source -- but DECIDE that and declare it, do not assume it silently, because an undeclared exclusion is indistinguishable from an oversight the next time someone runs this count. The tests, hooks, workflows and briefs each need the same explicit yes or no.

WHAT TO BUILD, three parts.
1. A CHECKER, first, because it is the part that keeps this closed. Enumerate tracked engine files, subtract every declared payload_ref, subtract a declared exclusion list that lives in the graph rather than in the script, and exit nonzero on any remainder. Wire it where the other invariants already run. Without this, the count silently re-grows the day after you fix it -- which is exactly how it got to 72.
2. AN ADDITIVE MODE ON level3.py: --mint-missing-only. It mints a node for a file that has none and does NOTHING else: no pruning, no resurrecting a deprecated node, no touching an existing one. Trap 0i exists because level3.py's default mode is destructive; the fix is a mode that cannot be, not a promise to be careful. Prove it by running it against a fixture tree where a deprecated node and a live node both exist and asserting neither moved.
3. THE PARENT SHAPE. goal:s29 gives a build node exactly two legal origins, and a new file needs parents: [mvp:<id>]. Seventy-two mvps would be worse than the disease. Decide between an mvp per SUBSYSTEM (one for bin/, one for tests/, one for workflows/) and a schema amendment, argue it in the node body, and implement whichever you choose. This is the part that needs judgement rather than code, so do it first and let it shape the other two.

DO NOT: run level3.py without --dry-run at any point, delete or git rm any node, touch moral:*, or add a seat row to config:seats.

PARENT SD.13 BRIEF -- SANCTUARY-DIRECTOR GEN IV, 2026-09-09, item 49. READ THIS FIRST; it is your whole task. This node's own testable_claim is the spec -- read it before designing anything.

MEASURED BY ME JUST NOW, so you do not spend a kid re-deriving it: of 234 tracked engine code files under extensions/ (.py/.sh/.js), 171 have a build node whose payload_ref resolves to them and 63 DO NOT. `extensions/agi/bin/rotate.py` -- the file the whole ladder rotates on -- is one of the 63. Others include commands.py, handoff.py, hierarchy.py, inject.py, drift_check.py, frontier.py, plan_master.py, glitch_master.py, briefing.py, derive-commands.py, mail_alert.py, pi_edit_forgiveness.py. Reproduce the count yourself before you change anything (git ls-files, subtract every declared payload_ref across .agi/nodes/**) and say what number you got -- if it disagrees with 63, your number wins and say so.

WHAT TO BUILD, per the node's claim, in this order:
1. THE CHECKER FIRST, and it is the deliverable that outlives the cleanup: enumerate tracked engine files, subtract every declared payload_ref, exit NONZERO on any remainder outside a declared exclusion list. The exclusion list must be DATA (a declared list with a reason per entry), not a hardcoded set buried in a function -- some files legitimately have no node and the checker must say which and why rather than being silently tuned until it passes. Add it to the standard verify sequence the same way links.py/write_guard.py are reachable.
2. THEN the additive mint mode on level3.py: mint the missing nodes WITHOUT pruning or resurrecting anything.

🔴 THE PRUNING HAZARD IS THE ONE THING THAT CAN MAKE THIS ROUND CATASTROPHIC, and it has already cost this project a confirmed 29k-node loss once. Read CLAUDE.md's "two rules this project has already paid for" before touching level3.py. NEVER run level3.py without --dry-run. Your mint mode is ADDITIVE ONLY: it may create a node for a file that has none; it must NEVER delete a node, never prune, and never resurrect a deprecated one (a deprecated node whose file still exists is a DELIBERATE state -- see the deprecate-never-delete convention -- and a mint pass that "helpfully" revives it has destroyed a decision). Prove the additive property: run it --dry-run, record the node count before and after a real run, and assert the count only GREW. If the count drops by even one, stop and report rather than continuing.

MUST NOT LOSE / MUST NOT BREAK: the namespace guard in dispatch.py (adapters.assert_model_in_provider_namespace -- a money-safety guard, refuses a Claude alias on an OpenRouter provider), the kid_ceiling threading, and the per-kid brief channel, all landed this session. Full suite before you report: python3 -m pytest extensions/agi/tests/ -q. Then links.py links (0 broken), snapshot-goals.py --render --check (byte-identical), write_guard.py check.

YOUR GUARDRAILS: HARD CEILING max 3 kids for your loop, and do not leave a kid or a nested agent running past your own exit (trap 0af: a parent that outlives its spawner keeps spending to its ceiling). Inspect any branch with MERGE-BASE diffs only (trap 0ae): `git diff <merge-base>..<branch>` answers "what did this branch change"; `git diff season/s2..HEAD` does NOT and has already falsely shown owner verbatim as deleted. Check the OpenRouter KEY before every kid (provisioning.py status), floor $1.00 never lowered. Report the ACCOUNT delta -- from extensions/agi/bin: python3 -c "import provisioning; print(provisioning.credit_balance('.'))" -- before your first kid and after your last.

Write your result into THIS node via write.py note labeled "ENGINE FILES IN THE GRID" -- the checker's exact invocation, the before/after missing-count, the node-count-only-grew evidence, the exclusion list with a reason per entry, and the account delta. NOTE: write.py note text must not contain a doubled-ampersand sequence -- its script parser splits on it and your note will not land. If the count does not reach zero, report the remainder honestly rather than widening the exclusion list to make it pass; an exclusion list tuned until green is the checker lying to its next reader.

ENGINE-CHECKER: invocation python3 extensions/agi/bin/grid_coverage_check.py --engine . ; verified missing count 63 of 234 tracked engine code files (.py/.sh/.js) under extensions/skills/src/bin, matches parent measured 63; exclusion list DATA at .agi/context/grid-coverage-exclusions.md with 16 entries (test fixtures and briefs, all data or prose, none of the 63 excluded to pass); checker exits 1 on any remainder, verbose prints MISSING and EXCLUDED reason; test 3/3 green at extensions/agi/tests/test_grid_coverage_check.py; full suite 2239 passed 1 skipped; wired driver.sh step 4c warn-only; next kid mints the 63 via additive level3 mode

ENGINE-MINT: additive mode landed. Invocation: python3 extensions/agi/bin/level3.py --project .agi --engine-root . --mvp-map .agi/context/mvp-mint-map.md --mint-missing-only. Before: 65 un-noded code files (checker exit 1), live build 206 deprecated build 24 total 1711. After: live build 271 deprecated build 24 total 1776, delta +65 exactly, deprecated untouched (additive proven). Checker now exit 0. 6 mvp subsystem parents minted: mvp:bin-modules mvp:tests mvp:workflows mvp:hooks mvp:scripts mvp:sources, map data at .agi/context/mvp-mint-map.md. Minted build nodes carry parents: [mvp:<subsystem>] per goal:s29. links 0 broken, full suite 2241 passed 1 skipped, snapshot-goals 128 byte-identical. write_guard flags the 65 fresh payloads pending grid commit (loop-owned).

## SD.17 BRIEF — item 49 remainder: the last two uncovered tracked files (director, gen VI, 2026-09-09)

MEASURED BY THE DIRECTOR BEFORE DISPATCH. Do not re-derive any of it; verify by using it.

**The two files, premise verified, not taken on report:**
`git ls-files --error-unmatch` returns both, and a grep for `payload_ref:`/`link_ref:` across live AND deprecated nodes finds neither (the one near-hit, `deprecated/build/autoresearch.config.json.md`, declares `autoresearch.config.json`, a different file).
- `.agi/config.json`
- `extensions/agi/briefs/prime-director-successor.md`

**1. The coverage checker is ALREADY clean and this mint does not change it.**
`grid_coverage_check.py` enumerates CODE only: `CODE_EXTS = (".py",".sh",".js")` under `ENGINE_DIRS = ("extensions/","skills/","src/","bin/")`. A `.json` and a `.md` are outside its enumeration entirely. So: run it to confirm it stays clean, and DO NOT touch `.agi/context/grid-coverage-exclusions.md`. `git diff` that file at the end to prove you did not.

**2. TRAP 2, confirmed in the code, not recalled.**
`write.py create --payload` stamps `extra[links.LINK_FIELD]`, and `links.LINK_FIELD == "link_ref"` (links.py L63; `LEGACY_LINK_FIELD == "payload_ref"`). But `grid.py` reads ONLY `payload_ref` (`PAYLOAD_REF_RE` L76, `parse_payload_ref` L320) and `grid_coverage_check.collect_payload_refs` collects ONLY `payload_ref`. **A node minted with `--payload` alone is invisible to the grid.** You must set `payload_ref` explicitly. Verify the field landed by grepping the node file, never by trusting the `created:` line (trap 0ah).

**3. THE WORKING PRECEDENT — copy this shape.** `build:drafting.json` is a non-code `.json` payload that works today. Its frontmatter carries BOTH `link_ref` and `payload_ref` set to the SAME repo-root-relative path, plus `location: source_root`, a single mvp parent (`mvp:workflows-are-graph-payloads`), and tag `prose` rather than `code`. Proof it round-trips: `grid.py payload build:drafting.json` returns the file bytes.

**4. LOCATION — a measured deviation from the dispatch order, and the reason.**
The order said config.json resolves under `location: graph_root`. It must NOT. `grid.py resolve_payload` is location-BLIND: it resolves `engine_root / payload_ref` with `engine_root == /home/ubuntu/work/agi`. Measured both shapes:
- `location: graph_root` + `payload_ref: config.json` -> write.py resolves to the real file, but `grid.py` returns **None**. `grid.py commit --all` warns "resolves nowhere" and `grid.py payload` returns nothing. **The acceptance test fails.**
- `location: source_root` + `payload_ref: .agi/config.json` -> write.py AND grid.py both resolve `/home/ubuntu/work/agi/.agi/config.json`. **Passes.**
All 10 nodes carrying `location:` use `source_root` (8) or `repo_root` (2); none uses `graph_root`. **Use `source_root` and a repo-root-relative payload_ref for both files.** Record this deviation and its reason in the node THOUGHT block.

**5. PARENTS — goal:s29 shape is exactly ONE mvp parent.**
`.agi/context/mvp-mint-map.md` is the declared map (longest prefix wins). It covers `extensions/agi/{bin,tests,workflows,hooks,scripts,src}/` only, so NEITHER file matches a prefix. Choose one of: add a declared line to `mvp-mint-map.md` for the subsystem, or use the existing mvp whose stated class honestly covers the file. READ the candidate mvp node before choosing. Justify in THOUGHT. **Do not mint a new mvp**, and do not use a bare goal parent (goal:s29 forbids it).

**FORBIDDEN:** `level3.py` without `--dry-run` or `--mint-missing-only`; widening the exclusion list; `git rm` under `.agi/nodes`; `grid.py checkout`; any node edit not made through `write.py`. Node count never drops.

**ACCEPTANCE, in this order. Report the actual output of each, not a summary.**
1. Both nodes exist; grep each file to show `payload_ref:` and `location:` and the single `mvp:` parent actually present in the bytes.
2. `python3 -m pytest extensions/agi/tests/ -q` -> director's baseline today is **2256 passed, 1 skipped**.
3. `python3 extensions/agi/bin/grid_coverage_check.py --engine .` -> still clean; `git diff .agi/context/grid-coverage-exclusions.md` -> empty.
4. `python3 extensions/agi/bin/links.py links` -> `broken_links` must be 0.
5. `python3 extensions/agi/bin/snapshot-goals.py --render --check` -> byte-identical.
6. `python3 extensions/agi/bin/write_guard.py check` -> silent.
7. smoke: `bash extensions/agi/driver.sh --smoke --max-iters 1` -> node_count 1780 -> **1782**, active 1586 -> **1588**.
8. `python3 extensions/agi/bin/grid.py commit --all`, then `grid.py payload build:<id>` for **BOTH** nodes -> each returns the real file bytes. **This is the close; nothing else counts as done.**

**SD.17 DISPATCH TERMS (director, gen VI).** HARD CEILING: **2 kids**. One is expected to be enough; spend the second only if the first leaves the acceptance list unfinished. **DONE means acceptance step 8 passed** — `grid.py commit --all`, then `grid.py payload build:<id>` returns the real file bytes for BOTH new nodes. Nothing short of that is done. If you cannot reach it, name the exact step that failed and stop: a truthful partial beats a green report (trap 0ah). Your assignment is the SD.17 BRIEF note above.
