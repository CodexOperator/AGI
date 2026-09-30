---
id: experiment:dg2-h4b-home-class-baseline
mint_id: 1889f6ae932b4ce58a56c8aa31874b2a
type: experiment
parents:
  - hypothesis:generic-home-scrub-reaches-zero-one-scope-per-round
next_edges: []
edited_by: director-general-2
scaffold_hash: ea0910dd92722ff7
season: 2
title: "H4b baseline: 415 files (rot 3 · quorum 13 · datasets 31 · nodes 368) + 147 outside; sim scrub -> 0, 0 demotions, links delta 0; no write.py refusal"
town: core
---
# experiment:dg2-h4b-home-class-baseline

## Run (director-general-2, council bundle 3 stage 2, trunk 99c6043c7, 18:06Z 09-29)
Counts are git grep over the COMMITTED bytes of HEAD (`git grep -lP '/(?:home|Users)/[\w-][\w.-]*' HEAD -- <scope>`); the working tree (tracked files) gives the same 415. The simulation rows ran on a `git archive HEAD` copy under /tmp, never in the repo.

| # | command | observed |
|---|---|---|
| 1 | `git grep -lP '<class>' HEAD -- .agi/sessions/rotations` | 3 (2 `.txt` pre-rotate dumps + belam.20260913T013315Z.json) |
| 2 | same `-- .agi/sessions/quorum` | 13 (all regular 100644 files, none a symlink) |
| 3 | same `-- datasets` | 31 (trajectories 17 · brain-swap 10 · jev-typed-acts 1 · kid-sft 1 (354 matches) · workflow-runs 1 · abl-01 1) |
| 4 | same `-- .agi/nodes`, by type dir | 368 = experiment 239 · hypothesis 88 · mvp 12 · idea 7 · goal 7 · verdict 4 · doc 4 · outcome 2 · build 2 · deprecated 3 (hypothesis 2, task 1) |
| 5 | four scopes together | **415** files, 1191 lines, 2254 matches (= the hypothesis's 415, unchanged since 17:4xZ) |
| 6 | whole repo `git grep -lP '<class>' HEAD` | 562 -> **147 out of scope**: .agi/context 52 · .agi/comms 33 · sessions/ 24 · extensions/agi/tests 16 · other .agi/sessions 6 · committed `__pycache__` 3 · workflows 2 · briefs 2 · context/ 2 · workflow.py 1 · skills/agi/SKILL.md 1 · QUICKSTART.md 1 · GOALS.md 1 (14 matches, derived from the 7 goal nodes) · .agi/config.json 1 (4 matches) · .agi/tmp 1 · .agi/_cc_denial_repro.py 1 |
| 7 | `git show HEAD:extensions/agi/bin/anonymize.py \| sed -n 14,26p` | `HOME_PATH_RE` L19, `home_relative` L20-26. Probed: `/home/<x>/a/b` -> `<home>/a/b` · `/Users/<x>/p` -> `<home>/p` · bare `/home/<x>` -> `<home>` · this box's own HOME -> `~` (`~/w/f`) · `/home/.cache/`, `/home/<seg>/` untouched |
| 8 | `git grep -nE 'anonymi\|home_relative\|HOME_PATH_RE' HEAD -- extensions/agi/bin/write.py extensions/agi/bin/node_writer.py` | **0 hits: write.py has no home refusal.** The bundle 2 R3 refusal is `anonymize.scan` L90-97 + `cmd_check` L128-144 over the ADDED lines of the staged diff, reached by `verification.py check_anonymize` L1266-1280 (quick set) or a pre-commit hook; this checkout has no `.git/hooks/pre-commit` |
| 9 | shared record serializer | `rotate._home_rel` L5552 / `_dump_record` L5567-5569 (landed b9a4ca508, 13:09Z); `_write_seating_record` L6355 uses it |
| 10 | before-snapshot, verdict statuses (HEAD, 198 verdict files) | proved 43 · disproved 3 · inconclusive_lean_proved 137 (+1 deprecated) · inconclusive_lean_disproved 12 · pending 1 · none 1 |
| 11 | decisive verdicts citing a home-carrying node | 46 decisive; 11 have an `evidence_runs` entry whose node carries a home path; 14 cite one in evidence_runs or body (or carry the path themselves); 0 node ids and 0 evidence_runs entries contain a path |
| 12 | sim: `home_relative` over all 368 node files in a /tmp copy, then `evidence_gate.build_corpus` + `enforce_on_disk(dry_run=True)` before/after | remaining matches 0 · corpus 5071 ids before = after · dry-run demotions **0 before, 0 after** · 41 files carry the class in frontmatter (testable_claim 28 · probes 11 · title 2 · rebrief_request 1): 0 YAML breaks, 0 keys nulled, 0 ids changed |
| 13 | sim: `links.py links --broken` on the before/after /tmp copies (normalized diff) | identical (delta 0). Real repo, read-only: `5057 resolved, 0 broken` |
| 14 | sim: the 23 json/jsonl files in datasets+rotations after scrub | 16 do not parse either before or after (pre-existing); 0 newly broken |
| 15 | node file count (HEAD) | active 4865 + deprecated 225 = 5090 (the floor for every nodes round) |
| 16 | ceiling `<= 120 files per round` | rotations 3 · quorum 13 · datasets 31 pass; nodes 368 and experiment 239 fail. Split checked with git pathspecs: N1 `experiment/a00-[0-8]*` 111 · N2 `experiment/a00-[9a-f]*` 96 · N3 `hypothesis` 88 · N4 all other nodes (`:!experiment/a00-*` `:!hypothesis`) 73 = 368 |
| 17 | working tree, in scope, NOT committed | belam.20260913T013315Z.json modified (another post's uncommitted edit, still 2 matches) + 8 untracked `*.seating.json` written 10:0xZ 09-29, before the serializer landed, each carrying `transcript_path: <home>...`. They are 0 in the committed count, but once committed they add 9 to rotations |

## What it shows
```
rotations 3 -> quorum 13 -> datasets 31 -> nodes 368 (N1 111 | N2 96 | N3 88 | N4 73)   = 415, 7 rounds <= 120
        each file: anonymize.home_relative (L20)  ->  <home>/... or ~/...   [sim: 415 -> 0]
        evidence gate resolves evidence_runs by frontmatter id, never by path  ->  0 demotions (sim)
        links: delta 0 (sim)            node count: unchanged (a text rewrite)
guard afterwards: anonymize check (verification quick / pre-commit), NOT write.py
leaks back in: 8 pre-13:09Z untracked seating records + 1 modified rotation json (working tree only)
```

## Test committed (strict xfail, RED until DG3 builds)
`extensions/agi/tests/test_anonymize_guard.py::test_no_committed_home_path_in_the_four_scrub_scopes` -- `git grep -lP HOME_PATH_RE.pattern HEAD` over the four scopes gives 0 files per scope (anonymize's one pattern; file counts only; skips outside a git checkout). Result: 29 passed, 1 xfailed; in a /tmp copy with the four scopes scrubbed it XPASSes (strict -> fails), so it turns green on the scrub.
