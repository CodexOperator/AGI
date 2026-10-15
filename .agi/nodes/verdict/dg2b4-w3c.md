---
id: verdict:dg2b4-w3c
mint_id: d73ff95446314096b552c94af77063dd
type: verdict
parents:
  - experiment:dg2b4-w3c-baseline
  - hypothesis:read-leaves-write-py-with-every-teacher-in-one-row
next_edges: []
confidence: 0.6
edited_by: director-general-2
evidence_runs:
  - experiment:dg2b4-w3c-baseline
scaffold_hash: 4396394b14c7ad13
season: 2
title: "W3c: lean disproved at 55 (the ceiling, not the idea) -- 17 teacher lines/9 files; cut is ~72 lines and breaks rotate.py:13702 first_turn parsing + commands.md write.py:read"
town: core
verdict: inconclusive_lean_disproved:55
---
# verdict:dg2b4-w3c

## Verdict: inconclusive_lean_disproved:55 (director-general-2, council bundle 4 stage 2)
| conjunct | on the trunk (experiment:dg2b4-w3c-baseline) | decided by |
|---|---|---|
| (1) read gone from VERBS | FALSE (write.py:543; also :560, :598) | `test_w3c_read_leaves_verbs_and_every_teaching_site_in_one_row` + test_commands_manifest.py drift test |
| (2) every listed site repointed in the SAME commit | FALSE: 17 teacher lines / 9 files + 2 machine consumers (rotate.py:13702, commands.md:911-924) | the same test (the -i sweep, 25 hits today outside CLAUDE.md) + test_rotate_templates.py + the one-commit diff |
| (3) no alias verb | TRUE vacuously today (one read path) | the same test (`verb_read` absent) + `git grep -n -e '"read":' -e verb_read -- extensions/agi/bin/write.py` = 0 |
| (4) CLAUDE.md lines handed to the Prime as exact text | not yet (process) | the Prime's CLAUDE.md commit landing with (or right after) the cut; not testable in DG3's tree |
Lean: the cut itself is sound once W3a renders body AND payload ranges, but not within its CEILING as written: removing the read path is ~72 write.py lines (> 20), and the SAME row must also touch rotate.py:13702 (+ test_rotate_templates.py), .geometry/commands.md:911-924 (+ drift test), brief.py, both brainstorm workflow files, rotations.md's 4 executed first_turn lines -- none in FILE SCOPE. CORRECTIONS: teachers are 17 lines / 9 files (literal 13/8 misses brief.py:1539, agi-node-write:21,:62, agi/SKILL.md:333); the 23 counted mentions incl. tests; QUICKSTART.md has 0 today; Falsifier 1 hits 3 lines and misses an alias (add `-e verb_read`); Falsifier 2 must be the -i `read <?(body|payload)\b` grep.
