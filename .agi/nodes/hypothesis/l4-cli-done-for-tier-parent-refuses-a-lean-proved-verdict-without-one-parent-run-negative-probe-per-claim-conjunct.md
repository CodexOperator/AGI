---
id: hypothesis:l4-cli-done-for-tier-parent-refuses-a-lean-proved-verdict-without-one-parent-run-negative-probe-per-claim-conjunct
mint_id: b13d1ca7f1994838a24b861c08f186aa
type: hypothesis
parents:
  - goal:g15
next_edges: []
edited_by: sensei-director
scaffold_hash: 7c5958aeb4869e25
season: 2
testable_claim: "goal:g15 (Sensei ask — owner ask via the point 22:0xZ, draft .agi/sessions/sensei/drafts/parent-role-pass-L4.327-20260912T2157Z.md — line (2) AUTOMATE). MEASURED by the Sensei: the L4.327 parent (a00-6b41b0ad) re-ran the KIDS' tests (423 passed 'on the disk bytes, not on the reports') and still passed a defect — a kid's tests are its claim, not evidence; spawn.json.brief 11,113 bytes: 'kid' x37, 'probe'/'refut'/'adversar'/'harvest'/'re-run' 0x. cli.py done (cli.py:555 cmd_done; :655 rec['status'] = 'done') accepts any verdict from a parent. CLAIM: (1) cli.py done for tier parent REFUSES by name a verdict >= inconclusive_lean_proved:50 (and proved) unless the round record carries probes: — a list with at least ONE parent-run negative probe PER CLAIM CONJUNCT (conjuncts = the numbered CLAIM items of the target hypothesis, counted by the same parser zoom uses for SL7.109's conjunct list), each probe = {conjunct, class, cmd, expected, observed, result}; probes: is recorded like evidence_runs (same record, same commit); (2) the refusal names the missing conjunct numbers; a verdict < 50 or disproved needs no probe; (3) probe CLASSES per claim type live as template lines in the parent section (SL7.111 writes the prose; this round defines the schema keys and the gate): auth -> a no-identity call must refuse; gate -> the other leg must refuse; wire -> the path exercised through the CLI, not the function; (4) --dry-run prints the gate's decision without writing. FALSIFIERS: a parent verdict >= 50 accepted with probes: absent; a probe count below the conjunct count accepted; a kid-tier done changed. TESTS (append to test_cli*.py, <= 5): refusal names conjuncts; accepted with one probe per conjunct; < 50 needs none; kid unchanged; dry-run. FILE SCOPE: cli.py cmd_done + a probes schema note in the experiment schema (.agi/context/schemas/[experiment].md — additive key); the cli tests. EXCLUDED: zoom.py (SL7.109), dispatch.py (SL7.112), template prose (SL7.111). CEILING: <= 80 lines + <= 5 tests; test_cli* green."
thought_session: sensei-director-genXVII-L17
title: "cli.py done for tier parent refuses a verdict >= inconclusive_lean_proved:50 unless the round records one parent-run negative probe per claim conjunct (probes: like evidence_runs; classes auth/gate/wire); the refusal names the missing conjuncts (owner heuristic line 2: AUTOMATE)"
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-cli-done-for-tier-parent-refuses-a-lean-proved-verdict-without-one-parent-run-negative-probe-per-claim-conjunct

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?
