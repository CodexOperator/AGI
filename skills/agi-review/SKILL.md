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
