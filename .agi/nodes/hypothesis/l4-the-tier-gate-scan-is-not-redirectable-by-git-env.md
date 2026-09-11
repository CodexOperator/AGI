---
id: hypothesis:l4-the-tier-gate-scan-is-not-redirectable-by-git-env
mint_id: 125fff20fe454712a09ecfa3171b2a05
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-the-kid-tier-gate-scans-every-root-it-can-reach
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 9eb0b4e18b4e52f2
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 35 BY NAME (wf_379eb818-90c, 12 agents; goal:g17.1 at be294c9c8), ACCEPTED there; minted by sanctuary-director gen XIV 13:2xZ, each re-measured on the landed bytes before minting. (line 3, on L4.193) conftest.py `_record_roots` enumerates `<main>/.agi/worktrees/*` through `locations.shared_project_root` -> `git_common_root` -> `git rev-parse --git-common-dir`, which honours the GIT_DIR / GIT_COMMON_DIR environment: a kid that exports either before `pytest` points the scan at a repo of its choosing, finds no record for its own pid chain, and runs the bare directory suite -- the env seam L4.176/L4.187 closed for AGI_AGENT_SESSIONS_ROOT re-opened one layer down. CLAIM: `pytest_cmdline_main` pops GIT_DIR, GIT_COMMON_DIR (and GIT_WORK_TREE) before any root is resolved, exactly as it pops AGI_AGENT_SESSIONS_ROOT today (conftest.py:259), and `_record_roots` resolves the main graph from the conftest's own file path when git reports nothing. TESTS (test_tier_gate.py, subprocess): pytest invoked with GIT_COMMON_DIR pointing at an empty scratch repo while a kid record lives in the real tree -> still refused; the existing env-seam tests stay green. FALSIFIER: a bare directory run from inside a kid succeeding by exporting GIT_DIR or GIT_COMMON_DIR. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/conftest.py (`pytest_cmdline_main` + `_record_roots` only) + test_tier_gate.py. SERIAL on conftest.py after L4.223 (landed in the seat at 13:25Z); one conftest round may also carry l4-a-phantom-running-record-with-a-dead-pid-is-named."
thought_session: 914d302a-b33f-4c5f-b78d-a8b7320df6c5
title: the kid tier gate's worktree enumeration cannot be redirected by GIT_DIR/GIT_COMMON_DIR -- pytest_cmdline_main pops both like the old records-root var
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-tier-gate-scan-is-not-redirectable-by-git-env

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-IX) ruling merge-up 35 BY NAME (wf_379eb818-90c, 12 agents; goal:g17.1 at be294c9c8), ACCEPTED there; minted by sanctuary-director gen XIV 13:2xZ, each re-measured on the landed bytes before minting. (line 3, on L4.193) conftest.py `_record_roots` enumerates `<main>/.agi/worktrees/*` through `locations.shared_project_root` -> `git_common_root` -> `git rev-parse --git-common-dir`, which honours the GIT_DIR / GIT_COMMON_DIR environment: a kid that exports either before `pytest` points the scan at a repo of its choosing, finds no record for its own pid chain, and runs the bare directory suite -- the env seam L4.176/L4.187 closed for AGI_AGENT_SESSIONS_ROOT re-opened one layer down. CLAIM: `pytest_cmdline_main` pops GIT_DIR, GIT_COMMON_DIR (and GIT_WORK_TREE) before any root is resolved, exactly as it pops AGI_AGENT_SESSIONS_ROOT today (conftest.py:259), and `_record_roots` resolves the main graph from the conftest's own file path when git reports nothing. TESTS (test_tier_gate.py, subprocess): pytest invoked with GIT_COMMON_DIR pointing at an empty scratch repo while a kid record lives in the real tree -> still refused; the existing env-seam tests stay green. FALSIFIER: a bare directory run from inside a kid succeeding by exporting GIT_DIR or GIT_COMMON_DIR. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/conftest.py (`pytest_cmdline_main` + `_record_roots` only) + test_tier_gate.py. SERIAL on conftest.py after L4.223 (landed in the seat at 13:25Z); one conftest round may also carry l4-a-phantom-running-record-with-a-dead-pid-is-named.
