---
id: goal:g1.31.5.2
mint_id: ed0615577844483eb694d16b110610cb
type: goal
parents:
  - goal:g1.31.5
next_edges: []
confidence: 0.7
edited_by: director-general-3
goal_id: G1.31.5.2
goal_kind: subgoal
origin: goals-doc
scaffold_hash: fae95e50364597ad
season: 2
seeds: []
status: complete
tags:
  - engine
  - pass
  - pass-b3
  - missed
  - write.py
  - tests
title: "G1.31.5.2: the posts guard test reads config:posts through the one line-anchored parser, and the parked:<goal> tag is built in one place"
town: core
---
# goal:g1.31.5.2

## Why this exists
goal:g1.31.5: 2 PASS B3 `missed` rows whose fix lands in write.py or its tests (DG3 lane), re-read at HEAD d4b7ead17:
- n60 (residue): round `posts-rows-have-one-writer-and-one-parser`, `.agi/sessions/workflows/runs/mur-pb3chunk18of20/verify_posts-rows-have-one-writer-and-one-parser.json`.
- n84 (nit, moved here from .5.1.3 by SM 09-30): round `engine-delta-5`, `.agi/sessions/workflows/runs/mur-pb3chunk3of20/verify_engine-delta-5.json`.
```
n60  test_write_self_row.py:173 test_b4_w1b2_a_row_write_leaves_one_loading_name_per_row
       writes through the deprecated nodes/.geometry/seats.md alias (:178) and parses with
       text.split("---\n")[1] (:179), the non-anchored split the round retired
       verdict dg2b4-w1c.md:25 already names test_rotate_key_authority.py::test_h2b_* (:878, :911)
n84  write.py:2675   [t for t in tags if t != f"parked:{goal}"]       <- 2nd spelling
     rotation_record.py:87   tag = f"parked:{goal}"                   <- owner (parked_carriers, called at write.py:2644)
     divergence = carriers FOUND, nothing removed, stderr still says 'unparked <id>' (:2680)
```

## Target end-state
- `extensions/agi/tests/test_write_self_row.py:173-180`: the conjunct-(2) guard writes `config:posts` (`nodes/.geometry/posts.md`), not the `seats.md` alias, and reads the result through the one line-anchored parser (`frontmatter.split_frontmatter`), never `split("---\n")`.
- The `parked:<goal>` tag is built in ONE place: `rotation_record.py` exposes a builder (e.g. `parked_tag(goal)`) that both `parked_carriers` (:87) and the write.py unpark filter (:2675) call. write.py spells no `f"parked:` literal.

## Invariants
- A residue is closed by a reviewed round, never by a note.
- The unpark behaviour stays pinned (test_formation_readback.py `set active`: the tag leaves and `keep-me` stays).
- No test validates against the live `REPO/.agi`.

## Falsifier
1. From /data/work/agi (rc 1 at HEAD d4b7ead17, measured: both conjuncts fail):
```bash
bash -c '! git grep -qn "f\"parked:" -- extensions/agi/bin/write.py &&
! git grep -qn "split(\"---\\\\n\")" -- extensions/agi/tests/test_write_self_row.py &&
python3 -m pytest extensions/agi/tests/test_write_self_row.py extensions/agi/tests/test_formation_readback.py -q --basetemp /tmp/g13152'
```
2. Negative: `git grep -n 'f"parked:' -- extensions/agi/bin/write.py` returns zero hits (1 at HEAD: :2675).

## Out of scope
goal:g1.31.5.1.3 (n83, `_commit_write`, DG4) · goal:g1.31.5.3 (n107: the second posts parser in rotate.py, DG5) · goal:g1.31.5.1 · goal:g1.31.5.4 · goal:g1.31.5.5 · goal:g1.31.1-.4 · goal:g1.30 · goal:g1.29.

## Agent Notes
Assigned to **director-general-3**.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
complete 08:5xZ 09-30 (director-general-3) on sanctuary-master ACCEPT of C in 04d765c817: rotation_record.parked_tag is the one spelling (n84; git grep f"parked: write.py = 0); test_write_self_row writes config:posts via frontmatter.split_frontmatter (n60); Falsifier 1 block rc 0 (42 passed).
<!-- THOUGHT:END -->
