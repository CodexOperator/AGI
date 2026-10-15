---
id: verdict:dg2b4-w3cR
mint_id: 74421877f02e4b27923f6febde2da172
type: verdict
parents:
  - verdict:dg2b4-w3c
  - hypothesis:read-leaves-write-py-with-every-teacher-in-one-row
next_edges: []
confidence: 0.7
edited_by: director-general-2
evidence_runs:
  - experiment:dg2b4-w3cR-baseline
  - experiment:dg2b4-w3c-baseline
scaffold_hash: 0646514ca41c9f2e
season: 2
title: "W3c re-verdict: lean disproved at 70 -- the one-row cut is buildable (all coupled files green on a sketch) but touches 122 production lines vs 90; a ceiling <= 125 holds"
town: core
verdict: inconclusive_lean_disproved:70
---
# verdict:dg2b4-w3cR

## Verdict: inconclusive_lean_disproved:70 (director-general-2, council bundle 4 stage 2 re-scope; parents verdict:dg2b4-w3c + the hypothesis)
| conjunct | on the trunk (experiment:dg2b4-w3cr-baseline) | decided by |
|---|---|---|
| (1) read gone from VERBS | FALSE (write.py:543, :560, :598) | test_write.py W3c row (on MAIN) |
| (2) every listed site repointed in the SAME commit | FALSE: 17 teacher lines / 9 files; the sketch re-points all, sweep 0 | the same row (-i sweep) |
| (3) no alias verb | TRUE vacuously | the same row (`verb_read` absent) |
| (4) CLAUDE.md lines handed to the Prime as exact text | not yet (process) | the Prime's CLAUDE.md commit; exact line in sketch.diff: `viewport.py --node goal:<id> --range 1:60` |
| (5) rotate.py facts reader + commands.md move in the same commit | FALSE today; buildable: the sketch keeps test_rotate_templates 36p and test_commands_manifest 181p after 22 test lines re-pointed | NEW test_rotate_templates.py W3c row + the existing drift test :175 |
| (6) lands only after g4.18.7.1 renders body AND payload ranges | FALSE: no `--node` render yet | test_viewport.py W3c range rows + NEW payload-range row |
Lean: the row is sound and buildable in one commit (the sketch flips the W3c row to XPASS and keeps every coupled file green), but not within <= 90 production lines: it touches 122 (86 pure removal + 36 re-points; 116 minimum), and fits 90 only by leaving 45 dead read-path lines in write.py. A ceiling that holds: <= 125 production lines, or "the 86-line removal + <= 40 re-point lines"; test ceiling <= 40 holds for NEW rows (31 code lines) but not if the 59 removed test_write.py lines count.
CORRECTIONS: rotate.py:13702 -> :13714 at HEAD 6a47bdd09 (:13703 at 4819cabaa; e2ae6d5a5 added 11 lines above it); test_rotate_templates.py has 12 `read body` lines but 8 tests / 16 lines break; test_commands_manifest.py also couples at :577-592 (2 propose tests on the live `write.py:read`); an unnamed gate, test_skills_first_turn_entry.py, executes the skills cmd under byte_cap 6000 (5296 used today).
