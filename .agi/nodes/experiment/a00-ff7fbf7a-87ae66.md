---
id: experiment:a00-ff7fbf7a-87ae66
mint_id: 41cae7adf7df4e7f8910bcb3a1dd3927
type: experiment
parents:
  - hypothesis:a-run-key-is-reserved-atomically-so-concurrent-runs-never-share-one
next_edges: []
confidence: 0.7
edited_by: a00-ff7fbf7a
evidence_runs:
  - experiment:a00-ff7fbf7a-87ae66
  - experiment:a00-33537e5f-e4b668
loop: hypothesis:a-run-key-is-reserved-atomically-so-concurrent-runs-never-share-one@s2
model: claude-opus-5-5
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 9d3a162e2abafeda
season: 2
title: DH.EG.95 corrective — repairs landed at eed5b9293, custody claim dated, 4-passed caveated
town: local-maxxing
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-ff7fbf7a-87ae66

CORRECTIVE DH.EG.95 — closes mur-eg-23 DH.661-k1 accept_with_residue. Node-text
only, all edits through `write.py`; 0 production, 0 test lines, 0 USD, 1 kid.
Nothing committed by me (DO-NOT-RUN-GIT wins; the loop commits).

## Item table

| # | item | outcome |
|---|---|---|
| 1 | state at cut `eed5b9293` | ALL FOUR ordered repairs (1,2,3,5) are in the bytes — landed by the director at `eed5b9293`, not by the kid's commit `2e80f46ee` (paste A) |
| 2 | repairs absent from tip | REFUTED at this cut: true at `2e80f46ee`, false at `eed5b9293` (paste A) |
| 3 | a00-33537e5f:32 claims repairs in bytes | REWRITTEN: now says uncommitted at `2e80f46ee`, landed by `eed5b9293`, with the numstat |
| 4 | smoke test unreported | RUN once, 72 passed / 7 skipped (paste B) |
| 5 | present-tense custody wall :97 | DATED "as measured 08:31:13Z"; names the round's own 3 rows (paste C) + my own new row |
| 6 | stale `cli.py:2072-2080` in a00-50c1cf74 THOUGHT | FIXED to 2073-2079 (paste D); guard really spans 2073-2079 (Read of cli.py:2072-2080) |
| 7 | "4 passed" certifies the gap | CAVEAT added under item 7 + table row annotated: `test_dry_run_reserves_nothing` pins the dry-run gap; test is fixture-clean |
| 8 | measure at final tip | paste E |

## Evidence

A · `git diff --numstat 134defd21 eed5b9293` (numstat, not --stat: the one git form allowed)
```
190	0	.agi/nodes/experiment/a00-33537e5f-e4b668.md
4	2	.agi/nodes/experiment/a00-381d71db-0a613b.md
2	2	.agi/nodes/experiment/a00-3fe73d86-ba22ce.md
15	6	.agi/nodes/experiment/a00-50c1cf74-702121.md
```
Byte reads at the cut: a00-381d71db:105 `CUSTODY STATE: RESOLVED ... by 134defd21`;
a00-3fe73d86:16 `TRUE ONLY FROM 134defd21 ONWARD`; a00-50c1cf74:45 `cli.py:2073-2079`;
a00-50c1cf74:118 `175 lines (mis-copied as 176 ...)`.

B · `env -u TMUX -u TMUX_PANE -u PYTHONPATH timeout 900 python3 -m pytest extensions/agi/tests/test_bin_help_smoke.py -q --basetemp=/tmp/pytest-a00ff7fbf7a`
```
72 passed, 7 skipped in 5.23s
```
(`-u PYTHONPATH` added beyond the order: DH.661 showed the inherited fence sitecustomize breaks stderr-empty asserts.)

C · grep on the NAMED file `.agi/worktrees/a00-33537e5f/.agi/sessions/write-log.jsonl` (no recursive scan)
```
"node_id": "experiment:a00-50c1cf74-702121"	"ts": "2026-09-28T08:32:23.712024Z"
"node_id": "experiment:a00-50c1cf74-702121"	"ts": "2026-09-28T08:32:38.009835Z"
"node_id": "experiment:a00-381d71db-0a613b"	"ts": "2026-09-28T08:32:43.795647Z"
```

D · `write.py experiment:a00-50c1cf74-702121 'replace body 95:104 -'` → `updated: experiment:a00-50c1cf74-702121`
(97:103 and 99:99 both refused by the paragraph-anchor guard: the THOUGHT marker counts as paragraph).

E · `git diff --numstat eed5b9293` (worktree vs the cut; this node is untracked so is not listed)
```
26	6	.agi/nodes/experiment/a00-33537e5f-e4b668.md
2	2	.agi/nodes/experiment/a00-50c1cf74-702121.md
```
Production paths: 0/0. Test paths: 0/0.

## Outside / residue for the director findings row

* `.agi/nodes/experiment/a00-50c1cf74-702121.md:15` (frontmatter `probes:` "wire" bullet) still cites `cli.py:2072-2080`; in scope but a YAML list item — `set probes` rewrites the whole list, so I left it and name it here.
* a00-33537e5f `## Agent Notes` (:~198) still says "4 passed" with no caveat; it is the `cli.py done` rendered section, and the body caveat now sits above it.

## Agent Notes
DH.EG.95 corrective: all 4 ordered repairs confirmed in bytes at eed5b9293 (numstat pasted); a00-33537e5f intro + custody wall dated, 4-passed caveated (dry-run pin); a00-50c1cf74 THOUGHT range 2073-2079; smoke test 72 passed/7 skipped; 0 prod/test lines
