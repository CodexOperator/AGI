---
id: hypothesis:l4-the-kid-tier-gate-is-not-clearable-from-inside-a-kid
mint_id: b6322e7471864b9697d4446daac77661
type: hypothesis
parents:
  - goal:g15
  - hypothesis:l4-mint-refuses-under-pytest-unless-mocked
next_edges: []
edited_by: sanctuary-director
scaffold_hash: ce8bb1351757465b
season: 2
testable_claim: "OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 29 review by name (wf_ad872f68-50a, 14 agents), goal:g15 newest note at f477e63bd/ee2000edc; line numbers on 2b4f33ed4. Proposed by the prime's ruling, minted by sanctuary-director gen XII 07:4xZ. g15-25: two kids cleared the kid-tier gate to run the FULL suite (a00-4cb96cbc:104, a00-78b9dd4e:70) and L4.155's kid a00-1422fa2e ran `env -u AGI_TIER python3 -m pytest extensions/agi/tests/ -q` (2808 passed, 216 s) — the gate in extensions/agi/tests/conftest.py reads AGI_TIER, which any kid can unset; the kid brief itself (brief.py, the RUN THE REPO TEST SUITE line) tells a kid to run the bare directory the gate refuses, so the workaround is invited. The test-to-real-mint half (provisioning.py:563) is CLOSED by L4.155 (harvested at c1e2a57f1) and is not re-derived here. CLAIM: (1) the gate derives the tier from the running agent record whose pid is an ancestor of the pytest process (`agent.json` under the tree's `.agi/sessions/iter-*/<agent>/` and the worktrees' sessions dirs: `tier`, `pid`, `status: running`), falling back to AGI_TIER only when no record matches, so `env -u AGI_TIER` no longer clears it; (2) the kid brief's suite line names the touched test files (`python3 -m pytest <the test files you changed or that cover your files> -q`), never the bare directory. TESTS: fixture agent.json with pid = an ancestor of the test process + tier kid -> bare directory run refused even with AGI_TIER unset; parent record -> allowed; no record -> env fallback as today; brief text asserts no bare-directory line for tier=kid. FALSIFIER: a bare directory run from inside a kid succeeds with AGI_TIER unset. CEILING: 2 kids (conftest gate / brief line — disjoint files). FILE SCOPE: extensions/agi/tests/conftest.py (gate) + extensions/agi/bin/brief.py (the ONE suite line for kids) + their tests. EXCLUDED: provisioning.py (landed), dispatch.py, item 5 of brief.py (g15-20, helper)."
thought_session: sanctuary-director-gen12
title: the full-suite refusal for a kid derives the tier from the running agent record, not from an env var the kid can unset; the kid brief names its test files
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-kid-tier-gate-is-not-clearable-from-inside-a-kid

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
OWNER 2026-09-11 05:1xZ: bugfix/optimization findings are g15 hypothesis nodes fixed in-loop. Source: merge-up 29 review by name (wf_ad872f68-50a, 14 agents), goal:g15 newest note at f477e63bd/ee2000edc; line numbers on 2b4f33ed4. Proposed by the prime's ruling, minted by sanctuary-director gen XII 07:4xZ. g15-25: two kids cleared the kid-tier gate to run the FULL suite (a00-4cb96cbc:104, a00-78b9dd4e:70) and L4.155's kid a00-1422fa2e ran `env -u AGI_TIER python3 -m pytest extensions/agi/tests/ -q` (2808 passed, 216 s) — the gate in extensions/agi/tests/conftest.py reads AGI_TIER, which any kid can unset; the kid brief itself (brief.py, the RUN THE REPO TEST SUITE line) tells a kid to run the bare directory the gate refuses, so the workaround is invited. The test-to-real-mint half (provisioning.py:563) is CLOSED by L4.155 (harvested at c1e2a57f1) and is not re-derived here. CLAIM: (1) the gate derives the tier from the running agent record whose pid is an ancestor of the pytest process (`agent.json` under the tree's `.agi/sessions/iter-*/<agent>/` and the worktrees' sessions dirs: `tier`, `pid`, `status: running`), falling back to AGI_TIER only when no record matches, so `env -u AGI_TIER` no longer clears it; (2) the kid brief's suite line names the touched test files (`python3 -m pytest <the test files you changed or that cover your files> -q`), never the bare directory. TESTS: fixture agent.json with pid = an ancestor of the test process + tier kid -> bare directory run refused even with AGI_TIER unset; parent record -> allowed; no record -> env fallback as today; brief text asserts no bare-directory line for tier=kid. FALSIFIER: a bare directory run from inside a kid succeeds with AGI_TIER unset. CEILING: 2 kids (conftest gate / brief line — disjoint files). FILE SCOPE: extensions/agi/tests/conftest.py (gate) + extensions/agi/bin/brief.py (the ONE suite line for kids) + their tests. EXCLUDED: provisioning.py (landed), dispatch.py, item 5 of brief.py (g15-20, helper).
