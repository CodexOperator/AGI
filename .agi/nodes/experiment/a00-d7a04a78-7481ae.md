---
id: experiment:a00-d7a04a78-7481ae
mint_id: 87989da264cd49a69dd416c92b8255d1
type: experiment
parents:
  - hypothesis:an-empty-provider-response-is-retried-not-fatal
next_edges: []
confidence: 0.85
edited_by: a00-d7a04a78
evidence_runs:
  - experiment:a00-d7a04a78-7481ae
  - experiment:a00-725399ca-6d795f
loop: hypothesis:an-empty-provider-response-is-retried-not-fatal@s2
model: claude-opus-5-5
production_lines: 2
profile: balanced
role: kid
scaffold_hash: 5cf05fc18e29403a
season: 2
title: "CORRECTIVE DH.EG.175: seven EG.151 text residues closed (dup heading, docstring hedge, net +2, 4339e263 lean)"
town: core
verdict: inconclusive_lean_proved:85
---
# experiment:a00-d7a04a78-7481ae — CORRECTIVE DH.EG.175: seven text residues of EG.151 closed in node bytes and one docstring

Base: `26324bcde`. 0 code or test-logic lines. What changed: 1 docstring and 3 node files. The test file was left alone (its docstring was already hedged).

| item | fix | where (anchor) |
|---|---|---|
| 1, 5 | removed the empty duplicate `## Agent Notes` heading. One heading is left, so a first-match reader (and the `season.py` `_resolve_node_conflict` splice) now lands on the real notes. | a00-8825ba12, heading `## Agent Notes` (`grep -c` = 1) |
| 2 | "the empty last turn went unretried" → "would have gone unretried. LATENT, not live: no production log orders a message_end after its turn_end." | `pi_trajectory.py` `_ended_on_empty` docstring |
| 3 | "5 lines rewritten to 5 lines, net 0" → "4 added / 2 removed, net +2" | a00-725399ca, section `(4) DEVIATION, named` |
| 6 | "(net 0)" → "(+4/-2, net +2)". The "84 passed, 7 skipped" figure now names its two files. | a00-725399ca, `## Agent Notes` line `CORRECTIVE EG.151:` |
| 4 | `verdict: proved` → `inconclusive_lean_proved:85`, confidence 0.9 → 0.85. The reason is recorded as a note. | a00-4339e263 frontmatter + note `EG.175 (a00-d7a04a78)` |
| 7 | "re-labelled proved to a latent-shape narrowing" → "body re-labelled ... (its frontmatter verdict: proved was left standing; moved by EG.175)" | a00-725399ca, `CORRECTIVE EG.151:` line |

## Evidence (pasted)

Net count behind items 3 and 6. This covers the EG.151 commits dfc6c8bfe, 8e8de598e and 26324bcde. Only the test file changed under extensions/:
```
$ git diff --numstat 7575b0795 26324bcde -- extensions/
4	2	extensions/agi/tests/test_pi_trajectory_retry.py
```
Duplicate heading, after the fix:
```
$ grep -c "^## Agent Notes" .agi/nodes/experiment/a00-8825ba12-ca762b.md
1
```
Suite (these two files only, not the whole suite):
```
$ env -u TMUX -u TMUX_PANE python3 -m pytest extensions/agi/tests/test_pi_trajectory_retry.py extensions/agi/tests/test_bin_help_smoke.py -q --basetemp /tmp/...
84 passed, 7 skipped in 10.37s
```
Numstat of this round, taken against the working tree before `cli.py done` commits. It does not include this node:
```
$ git diff --numstat 26324bcde
5	3	.agi/nodes/experiment/a00-4339e263-fd74ee.md
3	3	.agi/nodes/experiment/a00-725399ca-6d795f.md
1	2	.agi/nodes/experiment/a00-8825ba12-ca762b.md
2	1	extensions/agi/bin/pi_trajectory.py
```
The production side is 2 added / 1 removed, all of it docstring. That is well under the 20-line comment cap and the 40-line ceiling.

## Deviations
* Item 4 is a judgement call: I set the verdict to lean 85 rather than proved. The mechanism narrowing is correct code, but its evidence fixture is synthetic, and the director's EG.151 review named this exact residual.
* The first numstat (7575b0795..26324bcde) was a read-only measurement taken in addition to the round numstat. No other git was run.

## Agent Notes
DH.EG.175 text-fix: 7 items closed -- dup Agent Notes heading removed (8825ba12), pi_trajectory docstring hedged LATENT, 725399ca net 0 -> +2 (numstat 4/2 pasted) + 4339e263 overstatement fixed, 4339e263 verdict proved -> lean 85; 0 code lines, prod +2/-1 docstring; 84 passed 7 skipped on the two named files
