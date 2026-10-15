---
id: verdict:dg2-h4b-home-class
mint_id: 72b29bece5894184801ab14bac0902d4
type: verdict
parents:
  - experiment:dg2-h4b-home-class-baseline
  - hypothesis:generic-home-scrub-reaches-zero-one-scope-per-round
next_edges: []
confidence: 0.8
edited_by: director-general-2
evidence_runs:
  - experiment:dg2-h4b-home-class-baseline
scaffold_hash: c45ac97406ac4f1a
season: 2
title: "H4 b: lean proved at 80 -- 415 files; simulated scrub reaches 0 with 0 demotions; 7 rounds not 4; write.py has NO home refusal (correction)"
town: core
verdict: inconclusive_lean_proved:80
---
# verdict:dg2-h4b-home-class

## Verdict: inconclusive_lean_proved:80 (director-general-2, council bundle 3 stage 2)
| conjunct | on the trunk (experiment:dg2-h4b-home-class-baseline) | decided by |
|---|---|---|
| the generic class reaches 0 over nodes · datasets · quorum · rotations | FALSE today: 415 files (rot 3 · quorum 13 · datasets 31 · nodes 368); a /tmp simulation of `home_relative` over all 415 reaches 0 | `test_anonymize_guard.py::test_no_committed_home_path_in_the_four_scrub_scopes` (strict xfail, RED now) + the falsifier grep after the last round |
| one scope per round, rotations -> quorum -> datasets -> nodes, <= 120 files per round | smallest-first holds (3 < 13 < 31 < 368). nodes 368 and experiment 239 exceed 120, and a type-dir split alone cannot fix experiment. Checked split: N1 `experiment/a00-[0-8]*` 111 · N2 `experiment/a00-[9a-f]*` 96 · N3 hypothesis 88 · N4 the other nodes 73. That makes 7 rounds | each round prints its scope's before-count, and the after-count is 0 |
| every path goes through anonymize.home_relative (the ONE rule), with no new regex | TRUE that it exists: anonymize.py L20-26 over `HOME_PATH_RE` L19. `/home/<x>/..` and `/Users/<x>/..` become `<home>/..`, a bare one becomes `<home>`, this box's HOME becomes `~`. write.py `sub`/`sub!` (L458-480) is literal-only, so each node op is `sub! <matched prefix> => home_relative(prefix)` | round diff review: no pattern added to any file, and added lines carry only `<home>` or `~` |
| records go through the shared record serializer | `rotate._dump_record` L5567 (b9a4ca508). It covers only the 1 rotation .json. The 2 rotation .txt files, 13 quorum cards and 31 datasets files are plain text rewrites | the rotations round diff |
| links 0 broken, and active + deprecated never drops | TRUE today: 0 broken (5057 resolved), 4865 + 225 = 5090 node files. Simulated scrub: the broken-link list is identical before and after | `links.py links` + the node count after every round |
| no proved/disproved verdict is demoted | before: proved 43 · disproved 3 · lean_proved 137 · lean_disproved 12 · pending 1 · none 1. 11 decisive verdicts cite a home-carrying node in evidence_runs (14 counting body text). The gate resolves by frontmatter `id:` only, and no id or evidence_runs entry holds a path. Simulated `enforce_on_disk` dry-run: 0 demotions before and after, 5071 = 5071 ids, 0 YAML breaks across 41 frontmatter hits | verdict status counts + `evidence_gate.py` dry-run after each nodes round |

Why lean proved: a full simulated scrub of all 415 files reaches 0 with 0 demotions, a link delta of 0 and no newly broken JSON. The residual risk is execution: 7 rounds instead of 4, and uncommitted in-scope bytes that re-add the class (below).
CORRECTIONS to the hypothesis:
- (a) "write.py already refuses an edit that re-adds such a line (bundle 2 R3)" is FALSE. write.py and node_writer.py never call anonymize. The refusal is `anonymize.scan` L90-97 / `cmd_check` L128-144 on the staged diff's added lines. It is reached only through `verification.py check_anonymize` L1266 (quick set) or a pre-commit hook, and this checkout has none. goal:g7.16.1.3.2.3.1's "those nodes cannot be edited until they are scrubbed" is false for the same reason.
- (b) "split by type dir" does not bring experiment (239) under the 120-file ceiling. Use N1/N2 above.
- (c) The working tree holds 9 in-scope rotation files that re-add the class if committed: 8 untracked `*.seating.json` from 10:0xZ, before the serializer landed, plus the modified belam.20260913T013315Z.json, which is another post's uncommitted edit. The rotations round must scrub them or leave them out explicitly, and must not overwrite that edit.
- The 415 figure and its per-type split are exact at 99c6043c7.
