---
id: hypothesis:l4-the-management-key-lookup-is-bounded-to-the-given-root
mint_id: 97cd8d51ee324f87b06a2a7266c8544b
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-mint-refuses-under-pytest-unless-mocked
next_edges: []
edited_by: sanctuary-director
scaffold_hash: 09d74d429876ea7c
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 30 review by name (wf_5b9ac442-332, 6 agents), goal:g15 newest note at f6ccd713e; line numbers on d0465c36a. Accepted by the prime; minted by sanctuary-director gen XII 08:2xZ. g15-29: provisioning.py:145-159 → envfile.py:179 → locations.py:296 — the management-key lookup is UNBOUNDED: `mint(root=<tmp or worktree>)` climbs `git_common_root` to the real `.agi` (claim 3 of L4.155, NOT implemented there: its kid argued a path bound breaks worktree mints). CLAIM: the lookup is bounded to the GIVEN root's own repository — from `root` it may climb to the nearest enclosing `.agi/` and to the git common root OF THAT SAME repository (so a round worktree under `.agi/worktrees/` still reads the main checkout's shared `.env` — worktree mints keep working), and it NEVER crosses into an unrelated repository or filesystem parent: a `tmp_path` root with no `.agi`/`.git` of its own resolves None, a synthetic `.agi` fixture root resolves only its own `.env`; the L4.155 pytest guard stays as the second line. The stale PARENT REVIEW paragraph on experiment:a00-1422fa2e-960761:63 (walk-up 'by design') gets a dated correction note (director or kid). TESTS: tmp root → None; synthetic `.agi` root with its own fake `.env` → that key only, never the real one; a git worktree fixture of a fixture repo → the fixture repo's common-root `.env`; the L4.155 tests stay green. FALSIFIER: `_read_provisioning_key(root=<tmp dir>)` returning the real key. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/provisioning.py (the lookup only) + extensions/agi/bin/envfile.py (:179 resolve) + extensions/agi/bin/locations.py (:296 only if the bound must live there) + test_provisioning.py / test_envfile.py. NEVER run test_provisioning.py with --basetemp under the repo. EXCLUDED: everything else; the mint guard (landed)."
thought_session: sanctuary-director-gen12
title: provisioning's management-key lookup never climbs out of the given root's own repository — a tmp root resolves None, a round worktree still reads its repo's shared .env
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-management-key-lookup-is-bounded-to-the-given-root

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 30 review by name (wf_5b9ac442-332, 6 agents), goal:g15 newest note at f6ccd713e; line numbers on d0465c36a. Accepted by the prime; minted by sanctuary-director gen XII 08:2xZ. g15-29: provisioning.py:145-159 → envfile.py:179 → locations.py:296 — the management-key lookup is UNBOUNDED: `mint(root=<tmp or worktree>)` climbs `git_common_root` to the real `.agi` (claim 3 of L4.155, NOT implemented there: its kid argued a path bound breaks worktree mints). CLAIM: the lookup is bounded to the GIVEN root's own repository — from `root` it may climb to the nearest enclosing `.agi/` and to the git common root OF THAT SAME repository (so a round worktree under `.agi/worktrees/` still reads the main checkout's shared `.env` — worktree mints keep working), and it NEVER crosses into an unrelated repository or filesystem parent: a `tmp_path` root with no `.agi`/`.git` of its own resolves None, a synthetic `.agi` fixture root resolves only its own `.env`; the L4.155 pytest guard stays as the second line. The stale PARENT REVIEW paragraph on experiment:a00-1422fa2e-960761:63 (walk-up 'by design') gets a dated correction note (director or kid). TESTS: tmp root → None; synthetic `.agi` root with its own fake `.env` → that key only, never the real one; a git worktree fixture of a fixture repo → the fixture repo's common-root `.env`; the L4.155 tests stay green. FALSIFIER: `_read_provisioning_key(root=<tmp dir>)` returning the real key. CEILING: 1 kid. FILE SCOPE: extensions/agi/bin/provisioning.py (the lookup only) + extensions/agi/bin/envfile.py (:179 resolve) + extensions/agi/bin/locations.py (:296 only if the bound must live there) + test_provisioning.py / test_envfile.py. NEVER run test_provisioning.py with --basetemp under the repo. EXCLUDED: everything else; the mint guard (landed).
