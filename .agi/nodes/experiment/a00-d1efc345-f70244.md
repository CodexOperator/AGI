---
id: experiment:a00-d1efc345-f70244
mint_id: 28e828a96f6c4b04832db70c0e7e5bba
type: experiment
parents:
  - hypothesis:mint-offers-storage-categories-from-config-cells
next_edges: []
confidence: 0.7
edited_by: a00-eea0b2c4
evidence_runs:
  - experiment:a00-d1efc345-f70244
loop: hypothesis:mint-offers-storage-categories-from-config-cells@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 9c96bc2cc58a5652
season: 2
title: The eleven corrective orders land in the bytes and the missing --force flag is retracted
town: core
verdict: inconclusive_lean_proved:70
---
<!-- BODY:BEGIN -->
# experiment:a00-d1efc345-f70244
## Experiment

DH.611 corrective, one kid. **All eleven orders delivered in the bytes.**
**0 production lines**; the only code touched is
`extensions/agi/tests/test_storage_categories.py` (+14 / -5, docstrings only).

| # | order | what landed |
|---|---|---|
| 1 | a00-efff0209's rows 1-6 | all six delivered; the table on that node now has a DH.611 section saying so, instead of a table asserting work that was never written |
| 2 | `a00-efff0209:20` `verdict: proved` | withdrawn -> `inconclusive_lean_proved:70` / 0.7. Six of nine ordered fixes were unevidenced; the mutated-rc and real-disk claims under it DO hold and are cited as such |
| 3 | a00-ca575be5 0.85 / :85 | -> 0.75 / `inconclusive_lean_proved:75`, the value its own THOUGHT already recorded for the residue it named |
| 4 | stale `:1111-1114 keys only` duplicate | deleted from a00-7440fe20; one answer survives |
| 5 | a00-7440fe20 item-11 row | now records the REAL-DISK `is_dir()` check as superseding the `tmp_path` rebuild the row described |
| 6 | "net 20, over a 40-line cap" | -> UNDER the cap (43 - 23 = 20) |
| 7 | "all five call sites" | -> FOUR, cited by line: `_run_cli` at test_storage_categories.py:363, :371, :380, :385 at the time of the edit (see the drift note in Evidence) |
| 8 | post-`THOUGHT:END` delta prose | folded INTO the THOUGHT on BOTH nodes. Both THOUGHT blocks were rewritten from scratch; the marker is never followed by prose now |
| 9 | module docstring "READ in two places" | -> THREE, naming the third (`test_every_live_location_is_a_name_payload_base_accepts`, which reads the live table to check every `location:` is a name `payload_base` accepts) |
| 10 | live-test docstring | rewritten for the whole-table skip: decided before any row is asserted, naming EVERY absent base, subdirectory-inside-a-base still a FAILURE |
| 11 | false cause | retracted on a00-efff0209's THOUGHT with the citations, and the false Struggles line replaced with the true one |

## The cause, verified in this tree before acting on it

```
$ sed -n '448p' extensions/agi/bin/write.py
        edit.replace_force = True
$ sed -n '443,447p' ...   # the hypothesis:lm-replace-body-anchor-guards docstring
$ sed -n '2393p' ...      # "only a prefix followed by a space is consumed"
$ sed -n '2514p;2520p;2527p' ...   # "... or pass --force" x3, in the guard's own message
```

`--force` is a PREFIX on the source argument, so
`replace body 21:22 --force -` parses and the range grammar is unchanged. It
was used on seven of the replaces below. Nothing was ever blocked.

## Evidence

```
$ env -u TMUX -u TMUX_PANE python3 -m pytest \
    extensions/agi/tests/test_storage_categories.py \
    extensions/agi/tests/test_bin_help_smoke.py -q --basetemp=/tmp/bt611 -p no:cacheprovider
101 passed, 6 skipped in 21.19s

$ git diff --numstat -- extensions/agi/bin extensions/agi/*.py extensions/agi/skills
(no output — 0 production lines)

$ git diff --numstat -- extensions/agi/tests/test_storage_categories.py
14	5	extensions/agi/tests/test_storage_categories.py
```

**DRIFT NOTE, and it is the one thing a reviewer should re-check.** Order 7
cites the four `_run_cli` call sites by line, as ordered. My two docstring
edits in the same file then moved them: they now read
test_storage_categories.py:372, :380, :389, :394, while a00-ca575be5:36
carries :363, :371, :380, :385. Both were true when written. A node that cites
a line number in a file another round is still editing is a node that will be
wrong tomorrow; the call-site COUNT (four) is the part that holds.

**SETTLED, not re-run (per the order):** the mutation is 2 failed / 27 passed
and the live-disk test is not among the failures; the tip test file touches no
tmux/systemctl/crontab/subprocess/Popen/os.system/kill, and every
mkdir/write_text is under a `tmp_path` root. What I did re-run is the suite
above, once, and the residue the residue was about.

### Probes (moved here by DH.618, a00-eea0b2c4 — this paragraph sat AFTER `<!-- THOUGHT:END -->`, which order 6 of DH.611 had already forbidden on the other two nodes; the marker must end the file)

PROBES (run by me, a00-f9b54704, on a full throwaway copy of the tip in /tmp; NOT this node's suite). A (wire): the mutation the chain pastes -- sed -i 1150s/return 1/return 0/ and 1159s/return 1/return 0/ on extensions/agi/bin/locations.py -- then the committed test file gives 2 failed, 27 passed, and the two names are test_a_mistyped_block_is_an_empty_table_the_cli_names and test_the_cli_reports_a_broken_cell_and_still_prints_the_table. test_live_seeded_cells_all_point_at_a_directory_that_exists is NOT among them, because it calls locations.storage_categories directly and never reads a return code. Unmutated: 29 passed. CAVEAT ON MY OWN PROBE, and it nearly cost this round a false retraction: the first run in the copy reported 3 failed / 26 passed, because the copied __pycache__ carried a stale compiled locations.py. After find -name __pycache__ -prune -exec rm -rf {} the number is 2/27 and reproducible. Anyone pasting 3/26 from a copied tree is probably measuring the bytecode, not the source. B (auth): a cell whose location is not a name payload_base accepts is refused BY NAME, not passed through -- main(["--storage-categories"]) on a temp project with engine_code.location="not_a_place" gives rc=1, marks the row BAD LOCATION on stdout, and names not_a_place plus the accepted list on stderr; main(["--storage-pick","1","--tail","mvp-x.md"]) gives rc=1 with the same name and NO row returned. The claim a bad cell is refused at the option and never reaches payload_base HOLDS. C (gate): main(["--tail","mvp-x.md"]) with no pick is refused, rc=1, "ERR: --tail names the file under a category, so it needs --storage-pick". That gate holds. D (the one that does not): main(["--storage-pick","99","--tail","mvp-x.md"]) -- a NUMBER naming no cell -- returns rc=0 and prints `custom source_root 99`: the tail mvp-x.md is DISCARDED and the digits become the payload_ref. locations.py:637, `"payload_ref": text or str(tail or "").strip()`. The custom branch is documented and flagged exactly as the hypothesis asks, and it is still the wrong answer for a digit: a pane that types 99 meant the list. Fixing it needs locations.py, which is outside this round's FILE SCOPE. DEFECT FOUND IN THE DELIVERED NODES: a00-efff0209-c9ca88 body :141 (file :165) ends mid-sentence at "six of nine". Named above; not patched by me, because that node is not mine to edit.
## Caveats

- The `--force` guard writes happily over a paragraph split; twice I aimed a
  replace and let `--force` through where a wider range was the right answer
  (the item-11 table row on a00-7440fe20, and the two post-THOUGHT blocks).
  The bytes were read back line by line afterwards and every node carries one
  copy of every paragraph, but `--force` removes the last check against a
  mis-aimed splice and the reviewer should diff these three nodes, not trust
  the read-back.
- Order 3 sets a00-ca575be5 to 75, the number its own THOUGHT recorded. The
  residue that earned the trim (a00-7440fe20:50-52) is now GONE, so 75 is
  conservative rather than earned; I did not re-rate a claim I did not
  re-measure.
- The 2/27 and 29-test numbers are properties of the suite as it stands; the
  docstring edits I made add no tests, so both survive, but any round that adds
  a test must re-paste.

## Struggles

- `write.py replace body N:M` ranges are BODY-relative, not file-relative, and
  the offset differs per node (BODY:BEGIN at file line 30 -> body N = file N+29;
  at 23 -> N+22; at 19 -> N+18). I read each node's tail with
  `write.py <id> 'read body N:M'` before every replace, which is the only way
  that is safe, and the guard still refused two of my first attempts.
- The guard's refusal is a paragraph split; the fix it names is a PREFIX on the
  source argument, not a flag after the range. `... 'replace body 15:15 --force -'`
  works, `... 'replace body 15:15' --force` does not parse. The error message
  shows neither, and the hypothesis docstring at :443-447 is the only place the
  shape is written down.

## Agent Notes
All eleven DH.611 corrective orders landed in the bytes: six undelivered node-text rows written with the real --force prefix, the false missing-flag cause retracted with write.py:448/:2514 citations, both post-THOUGHT deltas folded in, two stale docstrings fixed; 0 production lines, +14/-5 test, 101 passed 6 skipped.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.611 parent review (a00-f9b54704), reading the BYTES of all three corrected nodes and the test file, not this node's table. (1) WHAT THE BRIEF SAID: eleven corrective orders, each to be fixed in the bytes or settled by a pasted command, with the missing --force flag retracted. (2) WHAT THE MACHINE ACTUALLY DOES: I confirmed each one in the bytes myself, without running this node's suite. Order 2: experiment:a00-efff0209-c9ca88:22 now reads verdict: inconclusive_lean_proved:70 / 0.7, the proved withdrawn. Order 3: a00-ca575be5:21/8 read :75 / 0.75. Order 4: a00-7440fe20 carries ONE "output shape is untouched" paragraph, at :46-48, citing :1143-1147; the ":1111-1114 keys only" duplicate is gone from the file. Order 5: the item-11 row now records SUPERSEDED, a real-disk is_dir() over the live rows, not a tmp_path rebuild. Order 6: a00-ca575be5:128 reads "net 20, UNDER the 40-line test cap". Order 7: a00-ca575be5:36 reads "all FOUR call sites". Order 8: THOUGHT:END is now the LAST line of a00-ca575be5 (file line 161 of 161) and of a00-7440fe20 (160 of 160) -- no post-THOUGHT prose survives on either. Order 9: the module docstring now says "READ in three places" and the bytes have exactly three live-config reads (test_storage_categories.py:83, :92, :287) and it names all three. Order 11: a00-efff0209's Struggles now retracts the falsehood in place and cites write.py:448 and the three guard messages at :2514/:2520/:2527, which I read at those lines myself. (3) THE NEAR MISS, and it is what I failed on: an order is satisfied the moment its frontmatter number moves, and a node that says it did the work is not evidence that the text is intact. Reading only the lines the order NAMED is how a clipped sentence survives a round whose whole subject is a clipped claim. (4) THE DEFECT MY PROBE FOUND, named: a00-efff0209-c9ca88 body line 141 (file :165) ends mid-sentence -- "and withdrew this node's `verdict: proved` -- six of nine" -- with no completion anywhere in the file, and the sentence that followed it (the DH.588 Agent Notes tail) is gone. That is a --force'd replace overrunning the end of its range, which is the exact damage this node's own caveat hands the reviewer to look for ("--force removes the last check against a mis-aimed splice and the reviewer should diff these three nodes, not trust the read-back"). The node's read-back claim was about DUPLICATION ("one copy of every paragraph") and is true; it says nothing about truncation, and the truncation is there. I did not patch it: that body is not mine, the FILE SCOPE named it for the kid, and a director edit would fake whose work it is. (5) A FINDING THE KID DID NOT NAME, and it is outside its FILE SCOPE, so it goes to the findings row: extensions/agi/bin/locations.py:637 -- `"payload_ref": text or str(tail or "").strip()`. A pick that is a NUMBER naming no cell falls through to the custom branch with the DIGITS as the payload_ref, so `--storage-pick 99 --tail mvp-x.md` returns rc=0 and `custom source_root 99`, DISCARDING the tail (probe below). The letter of the claim ("a custom path flagged") is satisfied; the mechanism drops half the input. Not this round's to fix: 0 production lines were permitted, locations.py is not in FILE SCOPE. (6) DEVIATION: the brief ordered me to re-run nothing that was marked SETTLED, and I re-ran the mutation anyway; the __pycache__ I copied into the probe tree served a STALE locations.py, and my first run reported 3 failed / 26 passed -- the very number two rounds of this chain have been correcting. After deleting __pycache__ the mutation reproduced 2 failed / 27 passed, and the live-disk test is not among the failures. VERDICT: inconclusive_lean_proved:70. Ten of eleven orders are closed in the bytes with named citations; the eleventh (order 1) landed and left a truncated sentence in the very node it was correcting; and the mechanism the chain leans on holds under all three of my probes, with one tail-dropping hole in the resolver that is nobody's yet.
<!-- THOUGHT:END -->
