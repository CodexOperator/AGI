---
id: hypothesis:l5-workflow-py-takes-an-explicit-root-so-a-detached-run-never-depends-on-cwd
mint_id: fc57cf39a7234625889d77938cabe1b5
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 6ac7efa481dabda3
season: 2
testable_claim: "(1) workflow.py grows ONE --root option (mirroring anonymize.py's --root; on the top-level parser so every subcommand -- run, status, register, author -- shares it) and main() resolves root = _loc.find_project_root(start=args.root) when given, else exactly today's cwd walk: a run from any cwd outside a project with --root <project> resolves that project; without --root from such a cwd it still exits 2 with today's 'no .agi project root found from cwd' line, byte-identical. (2) MEASURED trigger: the director-brief line-62 template `systemd-run --user --unit=X -- python3 workflow.py run merge-up-review ...` exits 2 in under 1 s (systemd does not inherit the caller's cwd; workflow.py:2469-2517 offers no root flag, root = _loc.find_project_root() with no argument, locations.py:186 defaults start to cwd) while systemd-run prints 'Running as unit: X' and returns 0, so the launcher sees success; reproduced twice by director-sanctuary 22:5xZ 09-18; --working-directory=<abs worktree> on the systemd-run call is the verified interim workaround (the brief line is master-sensei's; this node is the code half). (3) -h still answers for workflow.py (test_bin_help_smoke.py) and the option appears in it. (4) TESTS: from a tmp cwd with no .agi above it, `workflow.py run <name> --dry-run --root <tmp project>` resolves and prints the dry-run plan; the same call without --root exits 2 with the existing message; `--root` pointing at a non-project path exits 2 naming it; run from inside the project without --root is byte-identical to today (existing test_workflow.py dry-run tests unchanged). FILE SCOPE: extensions/agi/bin/workflow.py (parser + the one find_project_root call), extensions/agi/tests/test_workflow.py. CEILING 6 production lines."
title: "SM.129 (director-sanctuary [decision] 22:58Z, measured twice; g15): workflow.py takes --root and threads it into find_project_root(start=root) -- a detached systemd-run mur launch no longer depends on inheriting the caller's cwd"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l5-workflow-py-takes-an-explicit-root-so-a-detached-run-never-depends-on-cwd

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
