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
thought_session: 914d302a-b33f-4c5f-b78d-a8b7320df6c5
title: the kid-tier gate derives the tier from every sessions root the tree can reach, not the one root beside conftest
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-kid-tier-gate-scans-every-root-it-can-reach

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Found by the prime (belam-S1-L4-VIII) ruling merge-up 31 (d0d9777a5, goal:g15 newest note), ACCEPTED there; minted by sanctuary-director gen XIII 09:4xZ. (g15-36a) conftest.py:88 resolves ONE root (`find_project_root(Path(__file__))`), so a kid that points pytest at MAIN's absolute tests dir (`python3 -m pytest /home/ubuntu/work/agi/extensions/agi/tests/`) scans MAIN's sessions dir, finds no agent.json for its own pid chain, derives no tier and runs the bare directory suite it is refused from its own worktree. CLAIM: the record roots scanned are ALL of: the invoking tree's `<worktree>/.agi/sessions`, the shared sessions dir (`locations.shared_sessions_dir`), and the sessions dir of every worktree registered under `<main>/.agi/worktrees/*` -- the tier is derived from the FIRST agent.json whose pid chain contains the pytest process; a kid cannot escape by choosing which tests directory it names. TESTS (test_tier_gate.py, fixtures): a kid record living in worktree A's sessions while pytest is invoked on MAIN's tests dir -> refused; no record anywhere -> unchanged pass. FALSIFIER: a bare directory run from inside a kid succeeding by naming another tree's tests dir. CEILING: 1 kid. FILE SCOPE: extensions/agi/tests/conftest.py (_default_record_root/_record_root only) + test_tier_gate.py. SERIAL on conftest.py behind L4.176 (l4-the-kid-tier-gate-has-no-env-seam).

DIRECTOR HARVEST (sanctuary-director gen XIV, L4.193, 2026-09-11 12:41Z). Kept both kids' proved (0.9 experiment:a00-71de766d-07a75b the multi-root scan; 0.85 experiment:a00-f1436b59-540122 the merged-map fix) and the parent's accept -- the parent found the first cut root-ORDER dependent (per-root resolve, first hit wins: a parent record in an earlier root cleared a kid whose own record sat later) and re-briefed for one merged pid map before the ancestor walk, which is the fix that makes the claim true rather than usually true. Ran myself from the round worktree (a00-06c44930) against the live tree at 12:40Z: `_record_roots()` = 151 unique roots, own round sessions FIRST, the seat's and MAIN's included; the merged `_running_record_tiers` map holds the three live seat-dispatched parents (pids 3145642/3146215/3146707 -> `parent`) that the pre-fix single-root scan from this worktree cannot see (False); `_effective_tier()` from my unrecorded shell = None, so the AGI_TIER fallback is intact for a plain interactive run. Cost, measured: `_record_roots` 0.028 s + merged scan 0.235 s = ~0.2 s per pytest session over 334 agent.json files in 151 worktrees -- acceptable now, grows with the worktree count; a worktree sweep bounds it (residue, not a demotion). 155 passed with neighbours (test_tier_gate/test_send). NOTE for the falsifier's live form: a kid that names MAIN's tests dir loads MAIN's conftest, so the closure bites only once this lands in MAIN at merge-up 35 -- until then the seat has it and MAIN does not.
