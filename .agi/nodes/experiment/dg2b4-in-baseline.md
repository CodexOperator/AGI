---
id: experiment:dg2b4-in-baseline
mint_id: 563d90736fd3436f86b72a482cb59ad1
type: experiment
parents:
  - hypothesis:core-write-hunks-each-get-a-named-disposition
next_edges: []
edited_by: director-general-2
scaffold_hash: 8e13fd469add81cf
season: 2
title: "12/12 core write.py hunks named (+123/-17 from 8e4b4c286): 9 row-by-NAME (a4b077aba) -> W1a g4.18.5.1; 3 profile_sync -> rejected, bundle 5"
town: core
---
# experiment:dg2b4-in-baseline

## Run (director-general-2, council bundle 4 stage 2, trunk 9af4232ef, 20:34Z 09-29)
Core tip `origin/core/season2/main` = fca147fe1; `git merge-base HEAD origin/core/season2/main` = 8e4b4c286 (as the hypothesis says). write.py is byte-identical at 85246da86 and 9af4232ef. Read-only on core: git diff / show / ls-tree; `git apply --check` ran on an archived copy of trunk's write.py under /tmp only.

| # | command | observed |
|---|---|---|
| 1 | `git diff --stat 8e4b4c286 origin/core/season2/main -- extensions/agi/bin/write.py` | +123/-17, one file |
| 2 | `git diff 8e4b4c286 origin/core/season2/main -- extensions/agi/bin/write.py \| grep -c '^@@'` | 12 hunks |
| 3 | `git log --oneline 8e4b4c286..origin/core/season2/main -- extensions/agi/bin/write.py` + `git show --stat <c>` | a4b077aba (g7.33.10 row replace-by-NAME) = +108/-17 = hunks 2-7, 10-12 exactly; 5461f2fc1 (+10) and 9e78692f3 (+12/-7) = profile_sync, hunks 1, 8, 9 (+15/-0 net); 15c0ef0ad / b53722312 are sync merges |
| 4 | `git grep -c -e replace_row_name -e _resolve_body_row_range -e profile_sync HEAD -- extensions/agi/bin/write.py` | 0: no hunk is already on trunk (trunk's 3 `g7.33.10` mentions, :1804 :2048 :3350, are round B's SET half, a different change) |
| 5 | `git ls-tree HEAD extensions/agi/bin/profile_sync.py` / same on 8e4b4c286 / on core | absent / absent / present: hunk 1's import alone would ImportError on trunk |
| 6 | `git apply --check -v core_write.diff` on trunk write.py (archived copy) | hunks 1-8 and 10-12 apply at offsets +6..+30; ONLY hunk 9 fails, its context now holds trunk's unpark tail (write.py:2385-2396, the rotation_record carriers) |
| 7 | leaf existence: `git grep -l '^id: goal:<id>$' HEAD -- .agi/nodes/goal` for every disposition target | goal:g4.18.5.1 and goal:g7.16.1.4 (whose Out of scope names profile_sync) both exist; the 12 bundle-4 row leaves all exist |
| 8 | disposition sources: `write.py goal:g4.18.5.1 'read body 1:40'`, `write.py goal:g7.16.1.4 'read body 1:40'` | g4.18.5.1 Why: "Core's replace-by-NAME (goal:g7.16.1.4.3) is input"; g7.16.1.4 Out of scope: "... core's edits to EXISTING files (write.py +125 after W-input, ...) + profile_sync" |

### The 12 hunks (core line numbers at fca147fe1; full table with evidence: hunks.tsv)
| # | core lines | +/- | what it changes | disposition | row |
|---|---|---|---|---|---|
| 1 | 69 | +1/-0 | `import profile_sync` (g7.31.5.1) | rejected: bundle 5 (g7.16.1.4 Out of scope names profile_sync; module absent on trunk) | none |
| 2 | 156-160 | +5/-0 | `Edit.replace_row_name` field | absorbed -> goal:g4.18.5.1 | W1a |
| 3 | 427 | +1/-1 | verb_replace docstring `<START:END\|NAME>` | absorbed -> goal:g4.18.5.1 | W1a |
| 4 | 435-446 | +12/-5 | docstring: NAME = one table row by first cell, body-only, refuse missing/ambiguous | absorbed -> goal:g4.18.5.1 | W1a |
| 5 | 466-480 | +15/-2 | verb_replace parses bare NAME; payload + empty refused; range deferred to submit | absorbed -> goal:g4.18.5.1 | W1a |
| 6 | 627-628 | +2/-1 | VERB_EXAMPLES comment admits `replace body NAME path` | absorbed -> goal:g4.18.5.1 | W1a |
| 7 | 2322-2339 | +14/-1 | submit resolves NAME -> N:N on the CURRENT body; a named row skips the structural guard | absorbed -> goal:g4.18.5.1 | W1a |
| 8 | 2384-2390 | +7/-0 | comment: projection ordered after the payload write (residue 4) | rejected: bundle 5 (profile_sync) | none |
| 9 | 2406-2412 | +7/-0 | `profile_sync.sync_node` after update_node + payload; Refused -> EditError | rejected: bundle 5 (profile_sync; also the one hunk that no longer applies) | none; bundle-5 port lands after W1b g4.18.5.2 + W3 B3 g4.18.7.2 |
| 10 | 2642-2679 | +38/-0 | `_TABLE_ROW_FIRST_CELL_RE` + `_resolve_body_row_range` | absorbed -> goal:g4.18.5.1: semantics become the table-row kind of node_writer's ONE row index; the write.py def is NOT ported (leaf Falsifier 2: one def) | W1a |
| 11 | 3189-3192 | +4/-0 | `-h` epilog line for `replace body NAME` | absorbed -> goal:g4.18.5.1 | W1a |
| 12 | 3576-3593 | +17/-7 | `--dry-run` preview: resolve NAME, guard numeric ranges only, print NAME | absorbed -> goal:g4.18.5.1 | W1a |

## What it shows
```
core write.py  8e4b4c286 .. fca147fe1   +123/-17, 12 hunks
 ├─ a4b077aba  g7.33.10 row-by-NAME  9 hunks (2-7,10-12) +108/-17 ──> absorbed: W1a goal:g4.18.5.1
 │     semantics kept: NAME resolved at submit on the CURRENT body; 0 or >1 hits refuse by name;
 │     body-only; a named row is atomic (no N:M guard); --dry-run previews it
 │     shape NOT kept: the write.py resolver -> one row index in node_writer (tables are one row kind)
 │     test input: core's test_write_body_row_by_name.py (156 lines, 8 tests)
 └─ 5461f2fc1 + 9e78692f3  g7.31.5.1 profile_sync  3 hunks (1,8,9) +15/-0 ──> rejected: bundle 5
       reason: g7.16.1.4 Out of scope names profile_sync; profile_sync.py absent on trunk;
       hunk 9 already conflicts with trunk's unpark tail; its port must sit inside W1b's gate->write->commit
W-G, W1b, W1 B2, W2a-e, W3a, W3 B3, W3c: consume no hunk (0 each)
```
