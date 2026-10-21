---
name: agi-review
description: >
  Review a merge range (BASE..TIP) with Sonnet subagents from a graph-held brief: cut the range into area
  lanes with review-lanes.sh, fan out one Sonnet reviewer per lane (the harness Agent tool, model sonnet),
  then ONE adversarial Sonnet verifier over every lane's findings; the RED scans stay mechanical. Use for a
  merge pass, a merge-up gate (mur), or any range a post must judge. Replaces workflow.py reviews.
---

# agi-review — Sonnet lanes + one verifier, from the graph

Owner 00:4xZ 10-10: "Nah just use sonnet subagents and we retired workflows.py in favor of shel scripts". Owner
07:5xZ 10-10 asked for it as a graph template. First run: PASS B5 (season2/main 7276f11d36, 272 files, 0 RED).
The brief lives in the graph: `doc:agi-review-brief` (rules, RED / demote / residue, the OUT JSON shape).

## 1 · Cut the lanes (read-only)
```bash
O=<your scratchpad>/review-<key>                      # never inside a repo worktree
sh extensions/agi/bin/review-lanes.sh <BASE> <TIP> $O [MAX]   # MAX files per lane, default 40
```
Writes `$O/range`, `$O/all.txt`, one `$O/L<n>-<area>.txt` per lane; every changed path lands in exactly one lane.
Copy the brief out of the node next to them, past BOTH frontmatter fences (a single `sed '1,/^---$/d'` leaves 0 B -- SM 08:44Z):
`awk 'f>=2; /^---$/{f++}' .agi/nodes/doc/agi-review-brief.md > $O/brief.md`

## 2 · Fan out (one Agent call per lane, all in ONE message, `model: sonnet`, background)
Prompt per lane = "Read the brief at $O/brief.md and follow it exactly." + `LANE` · `RANGE: $O/range` ·
`FILES: $O/L<n>-<area>.txt` · `OUT: $O/out/L<n>-<area>.json` · ONE focus line for the area
(engine: weakened rails · tests: tests that cannot fail · guard: root-shell safety · goals: complete without
bytes, dangling links · docs: secrets/home paths, sha claims · research: overclaims, payload paths · config:
loosened bounds, keys in records). Keep ≤ ~9 lanes; reviewers run NO tests and no repo scripts.

## 3 · Verify (ONE adversarial Sonnet agent)
Merge the lane JSONs into `$O/combined.json`; the verifier hunts a MISSED RED across the whole range
(credential shapes, a D that is not a move into deprecated/, a removed lock/refusal) and marks each residue
CONFIRMED / REFUTED / UNCHECKED into `$O/out/verify.json`. Its first word is CLEAR or RED.

## 4 · Mechanical REDs (the caller, never an agent)
Full anonymize with `.env` (`anonymize.py check --root <MAIN> --diff-file F`, as a uid that reads `.env`) ·
deletions by mint_id · `links.py links` = 0 broken. A RED blocks; residues go to ONE leaf goal (skill agi-goal).

## Traps
| trap | rule |
|---|---|
| a reviewer printing a secret | the brief forbids values: kind + file:line only |
| scratch paths in a node body | rewrite home paths to `~` before minting (anonymize home class) |
| a stale TIP | pin TIP as a sha at the start; a later delta gets its own small lane |
| a new test in the range | prove it can fail: run the SAME file on the previous tip (control = RED) and mutate one guard on yours; green alone is not evidence (DG5 round 1) |
| a grep-shaped falsifier | prove it can FAIL against the bytes: falsifier 5 grepped 'refs/grid' in a piece that never names it (alive gen 12) |

## Traps moved from cards (owner 10-10: one sweep, then a rule; self-perpetuating gens 5-8, swept at gen 9)
- a checker you approve -> read it WHOLE and ask which input makes it check NOTHING and still exit 0 (sp gen 8: DG3's checker, no sha line -> 0 checked, rc 0)
- a probe's RED you cite -> it must also go GREEN on the fixed sha; run it there first (sp gen 5: my probe disabled a job in a 2nd project and I cited the RED)
- a gate of N conjuncts -> one mutant PER conjunct, named before you judge the row; ABSENT and PRESENT-BUT-LOW are different inputs (sp gen 5: 3 flips on the PSI row in 2 min; gen 8: one mutant for a 5-conjunct gate)
- an alarm row -> two rows: RED on stress AND GREEN on a healthy live reading (sp gen 6: a NEVER-fires fix agreed into an ALWAYS-fires one)
- a red from a lane you ran -> run the same lane on the BASE in the same env before calling it (sp gen 6: 25 FAIL from an archive without .agi/context)
- an append/drain pair -> test an fd opened BEFORE the rename and written AFTER the read; never pass on the commit's own claim (sp gen 6: alarm_spool)
- a claimed hole -> trace the input through every EARLIER refusal before saying it reaches its sink (sp gen 8: .42.2 returned for a drop an earlier refusal blocks)
- a claim about what code, a unit or a key does -> read the CODE it rests on and its STATE (is-active, timestamps, expires_at, the SUM over every live key), never a name, a grep or a unit FILE (sp gen 7-8: 'carry.env writes project' from a never-active unit; a key TTL assumed)
- a count or an open item -> measure it, on the director's BRANCH as well as the trunk (sp gen 8)
- refusing a carry, or naming another path to use -> read what the CURRENT carrier moves (guard.md move.exclude) and how fresh the other path is (sp gen 5: origin lagged box-move by 5 min; withdrawn)
- testifying about a past generation -> grep the card's HISTORY (`git log -G <pat> -p -- <card>`), never the trunk text: a card is replaced whole (sp gen 5: 'VERDICT YES' was in the history; withdrawn)
- a line number in a word -> cite the one you READ, after the read (sp gen 6: baseline() placed from memory, alive corrected)
- an SM ask to the council -> the answerer (alive) writes it; another seat writes only when alive names it (sp + alive gen 5: two .5 commits 1 min apart)
