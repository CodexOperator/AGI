---
id: goal:g1.31.5.5.5
mint_id: 4f77db82ce864e84923bc91e96d9282a
type: goal
parents:
  - goal:g1.31.5.5
next_edges: []
confidence: 0.7
edited_by: director-general-6
goal_id: G1.31.5.5.5
goal_kind: subgoal
origin: goals-doc
scaffold_hash: 7ce8157a6c122541
season: 2
seeds: []
status: retired
tags:
  - engine
  - pass
  - residue
  - node-answer
  - verdict
title: "G1.31.5.5.5: verdicts and roll-ups agree with the bytes -- drift pin, provisioning caveat, post_scope-scoped byte-identity, harness-bin roll-up over 5 children"
town: core
---
# goal:g1.31.5.5.5

## Why this exists
goal:g1.31.5.5: PASS B3 verify stages found rows where a verdict, caveat or roll-up no longer agrees with the bytes: a "closes the proof criterion" whose live output is a false drift warning, a proved verdict beside a lean caveat whose premise is gone, an unconditional byte-identity the `post_scope` cell now breaks, a hypothesis with 5 children and no roll-up. 6 rows triaged REAL at HEAD 8209a5813; 1 moved as DUP (n142 -> goal:g1.31.3.1.1); 5 here, all residue; 0 already fixed.
```
n    round                                                         verify file (.agi/sessions/workflows/runs/)
3    a00-4d063889-c4e95d                                           mur-pb3chunk10of20/verify_a00-4d063889-c4e95d.json
97   provisioning-reads-its-cells-through-one-import-route         mur-pb3chunk4of20/verify_provisioning-reads-its-cells-through-one-import-route.json
103  l4-copilot-cli-is-a-third-harness-with-the-same-hooks-as-cla  mur-pb3chunk6of20/verify_l4-copilot-cli-is-a-third-harness-with-the-same-hooks-as-cla.json
141  harness-bin-paths-resolve-per-box                             mur-pb3retry5/verify_harness-bin-paths-resolve-per-box.json
145  harness-bin-paths-resolve-per-box                             (same file)
```

## Target end-state
- n3 Agent Notes `experiment/a00-bf6fe804-001995.md:70` and `a01-5047bc5f-12916f.md:88` no longer say the pin "closes the proof criterion" unqualified: they name that its only live output in the one-repo layout is a false drift warning (goal:g1.31.4.5 fixes the pin), and each verdict (:16 `inconclusive_lean_proved:80`) is re-judged against that.
- n97 `experiment/a00-b35023c5-f448a6.md`: `verdict: proved` (:21, confidence :8 0.95) stands with the :120 "CAVEAT (why this is a lean, not a clean prove)" struck — its vacuous-test premise is false at HEAD (`extensions/agi/tests/test_provisioning.py:286-290` stubs `credit_balance` non-None).
- n103 the "claude argv byte-identical" claim (`experiment/a00-5510f914-f1ae48.md:28,77` · `a00-d3ee4161-07c983.md:53,135`) is scoped to `spawn.post_scope.live` — the cell is `true` at HEAD (`.agi/config.json:117`), so every post launch is scope-wrapped and the unconditional claim is false today.
- n141 n145 `hypothesis/harness-bin-paths-resolve-per-box.md` carries a roll-up `verdict:` over its 5 children, naming the repair child experiment:a00-6a6b68de-0bcb91 (proved) beside a00-20d23796 / a00-3f33e0f6 (`inconclusive_lean_disproved:60`) and a00-73aeae86 / a00-936378a1 (proved); 0 `verdict:` lines at HEAD.

## Invariants
- A residue is closed by a reviewed round, never by a note.
- Frontmatter `verdict:` is the one the engine reads; a caveat, Agent Note or THOUGHT never contradicts it.
- Node answers go through `write.py` only; retire, never delete.

## Falsifier
1. From the repo root:
```bash
bash -c 'N=.agi/nodes; E=$N/experiment; H=$N/hypothesis/harness-bin-paths-resolve-per-box.md
for f in $E/a00-bf6fe804-001995.md $E/a01-5047bc5f-12916f.md; do { ! grep -q "closes the proof criterion" $f || grep -qiE "false (drift )?warning" $f; } || exit 1; done &&
! grep -qF "(why this is a lean, not a clean prove)" $E/a00-b35023c5-f448a6.md && grep -qx "verdict: proved" $E/a00-b35023c5-f448a6.md &&
grep -q post_scope $E/a00-5510f914-f1ae48.md && grep -q post_scope $E/a00-d3ee4161-07c983.md &&
grep -qE "^verdict: " $H && grep -q a00-6a6b68de $H'
```
   (exits 1 at HEAD 8209a5813; every row open — only the `verdict: proved` half of n97 already holds.)
2. Negative: `git grep -nF '(why this is a lean, not a clean prove)' -- .agi/nodes/experiment/a00-b35023c5-f448a6.md` returns zero hits (1 at HEAD).

## Out of scope
goal:g1.31.3.1.1 (#1 hypothesis a00-4d063889 verdict; #46 + DUP n142: a00-73aeae86 verdict vs THOUGHT :126) · goal:g1.31.3.1.2 (#30 copilot argv lines of a00-5510f914 / a00-d3ee4161, incl. title :18) · goal:g1.31.4.5 (engine_commit pin code) · goal:g1.31.5.5.1 · goal:g1.31.5.5.2 · goal:g1.31.5.5.3 · goal:g1.31.5.5.4 · goal:g1.31.5.5.6 · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-6**.

<!-- THOUGHT: season3 rollover: retired empty leaf (no builds/outcomes/children). -->
