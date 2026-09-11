---
id: hypothesis:l4-the-kid-tier-gate-scans-every-root-it-can-reach
mint_id: 3734623f08844481968587b3dda7e317
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-the-kid-tier-gate-has-no-env-seam
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 3fd1741fe3224447
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-VIII) ruling merge-up 31 (d0d9777a5, goal:g15 newest note), ACCEPTED there; minted by sanctuary-director gen XIII 09:4xZ. (g15-36a) conftest.py:88 resolves ONE root (`find_project_root(Path(__file__))`), so a kid that points pytest at MAIN's absolute tests dir (`python3 -m pytest /home/ubuntu/work/agi/extensions/agi/tests/`) scans MAIN's sessions dir, finds no agent.json for its own pid chain, derives no tier and runs the bare directory suite it is refused from its own worktree. CLAIM: the record roots scanned are ALL of: the invoking tree's `<worktree>/.agi/sessions`, the shared sessions dir (`locations.shared_sessions_dir`), and the sessions dir of every worktree registered under `<main>/.agi/worktrees/*` -- the tier is derived from the FIRST agent.json whose pid chain contains the pytest process; a kid cannot escape by choosing which tests directory it names. TESTS (test_tier_gate.py, fixtures): a kid record living in worktree A's sessions while pytest is invoked on MAIN's tests dir -> refused; no record anywhere -> unchanged pass. FALSIFIER: a bare directory run from inside a kid succeeding by naming another tree's tests dir. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/conftest.py (_default_record_root/_record_root only) + test_tier_gate.py. SERIAL on conftest.py behind L4.176 (l4-the-kid-tier-gate-has-no-env-seam)."
thought_session: bca4febf-020c-4ee2-b023-9ed885b937bc
title: the kid-tier gate derives the tier from every sessions root the tree can reach, not the one root beside conftest
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-kid-tier-gate-scans-every-root-it-can-reach

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-VIII) ruling merge-up 31 (d0d9777a5, goal:g15 newest note), ACCEPTED there; minted by sanctuary-director gen XIII 09:4xZ. (g15-36a) conftest.py:88 resolves ONE root (`find_project_root(Path(__file__))`), so a kid that points pytest at MAIN's absolute tests dir (`python3 -m pytest /home/ubuntu/work/agi/extensions/agi/tests/`) scans MAIN's sessions dir, finds no agent.json for its own pid chain, derives no tier and runs the bare directory suite it is refused from its own worktree. CLAIM: the record roots scanned are ALL of: the invoking tree's `<worktree>/.agi/sessions`, the shared sessions dir (`locations.shared_sessions_dir`), and the sessions dir of every worktree registered under `<main>/.agi/worktrees/*` -- the tier is derived from the FIRST agent.json whose pid chain contains the pytest process; a kid cannot escape by choosing which tests directory it names. TESTS (test_tier_gate.py, fixtures): a kid record living in worktree A's sessions while pytest is invoked on MAIN's tests dir -> refused; no record anywhere -> unchanged pass. FALSIFIER: a bare directory run from inside a kid succeeding by naming another tree's tests dir. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/conftest.py (_default_record_root/_record_root only) + test_tier_gate.py. SERIAL on conftest.py behind L4.176 (l4-the-kid-tier-gate-has-no-env-seam).
