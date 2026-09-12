---
id: hypothesis:l4-the-parent-task-section-says-a-kids-tests-are-its-claim-and-hands-the-parent-the-kid-diff-not-its-result-file
mint_id: 5252a009eed34dd7a5383e02f275d017
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: 57e895fb1494e84c
season: 2
testable_claim: "goal:g15 (Sensei ask — owner ask via the point 22:0xZ, draft .agi/sessions/sensei/drafts/parent-role-pass-L4.327-20260912T2157Z.md — line (3) CONSOLIDATE). MEASURED by the Sensei: the L4.327 parent's 'Your Task' was the generic KID contract (spawn one child, report fields, verdict grammar); the parent brief (dispatch.py:776 _brief_tier_for) says 'kid' 37 times and never 'bytes', 'probe', 'refute', 'adversarial', 'harvest', 're-run'; the parent read kidN-result.txt reports, never the kid DIFF. CLAIM: (1) ONE template, tier-keyed: the 'Your Task' slot (zoom.py:546/:659/:785 — keyed by SL7.109) carries a PARENT section when tier = parent: 'a kid's tests are its claim, not your evidence' · 'you are handed each kid's DIFF (git diff merge-base..kid-branch, bytes), never its result file' · 'one negative probe per claim conjunct, run by you, recorded as probes: (SL7.110's gate refuses without them)' · the three probe classes with one example each · 'a kid that passes its own tests and fails your probe is lean_disproved with the probe named'; (2) dispatch.py's parent brief (_brief_tier_for) hands the parent the DIFF path/command for each kid instead of kidN-result.txt, keeping the result file readable as secondary; (3) the kid template text is byte-identical to today (golden); (4) a rendered parent 'Your Task' contains each of the six words the Sensei counted at 0 (bytes, probe, refute, adversarial, harvest, re-run) at least once — assert it. FALSIFIERS: a parent task text without the six words; kid text changed; the parent still pointed at kidN-result.txt first. TESTS (append to test_zoom*.py + test_dispatch*.py, <= 4). FILE SCOPE: zoom.py (the parent section text only — SL7.109 keys the slot; if 109 has not landed on your base, key it minimally and say so), dispatch.py _brief_tier_for. EXCLUDED: cli.py (SL7.110), the spawn/lease/scaffold path (SL7.112). CEILING: <= 60 lines of prose/code + <= 4 tests."
thought_session: sensei-director-genXVII-L17
title: "one tier-keyed template: the parent's Your Task section says a kid's tests are its claim not the evidence, hands the parent each kid's DIFF instead of kidN-result.txt, and names the negative-probe duty and classes; the kid text stays byte-identical (owner heuristic line 3: CONSOLIDATE)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-the-parent-task-section-says-a-kids-tests-are-its-claim-and-hands-the-parent-the-kid-diff-not-its-result-file

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
