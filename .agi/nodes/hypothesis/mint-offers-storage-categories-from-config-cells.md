---
id: hypothesis:mint-offers-storage-categories-from-config-cells
mint_id: 4bd1d330335142aebd7a5b34e6e38457
type: hypothesis
parents:
  - goal:g4.18.1.3
next_edges: []
confidence: 0.8
edited_by: director-engine
scaffold_hash: 4a56d56600042137
season: 2
tags:
  - engine
  - write
  - locations
  - g4.18.1
testable_claim: "(1) storage categories are config cells (2) one locations.py resolver numbers them and maps a pick + tail to (location, payload_ref), a custom path flagged (3) one CLI prints the list; one new cell = one new option, no code edit (assigned: director-engine)"
title: "the mint flow offers storage categories as a numbered list read from config cells, plus a flagged custom path (goal:g4.18.1.3; assigned: director-engine)"
town: core
---
# hypothesis:mint-offers-storage-categories-from-config-cells

## Measured
- A payload's base is already a NAME, never a path: `locations.payload_base` (extensions/agi/bin/locations.py:445) resolves `source_root` · `graph_root` · `repo_root` · any key under the config's `locations:` block; an unknown name is a hard error ([build].md "location" section). `write.py create --payload` stamps `location: source_root` (write.py ~2904).
- NO storage-CATEGORY list exists: the directory a post files a new payload under (engine code, tests, skills, .geometry config, schemas, context templates) is typed by hand into `--payload`; nothing offers the options, so a post can only guess the prefix.

## CLAIM
(1) the storage categories are CONFIG cells (one table, e.g. `mint.storage_categories.<key> = {location, prefix, label}`), seeded with the categories the owner names (engine code, tests, skills, .geometry config, schemas, context templates) (2) ONE resolver in locations.py returns them as a numbered list in cell order, and turns a pick (number or key) plus an optional path tail into `(location, payload_ref)`; a path outside every category is accepted and returned flagged `custom` (3) a one-line CLI prints the numbered list (the pane-side picker the draft flow of goal:g4.18.1.2 will call); adding one cell in a temp config adds one option with no code edit.

## Dispatch line
config-max: the category table IS the change -- a config cell, seeded by the kid via write.py/config edit in the round. template-max: none (the flow text rides goal:g4.18.1.2). code: the resolver + its CLI only, because no reader of such a table exists.

## FALSIFIERS
- a temp config with one extra category cell does not print one extra option (exit 0).
- `grep -nE '"(extensions|skills|\.agi)/' ` over the new resolver code finds a storage-path literal.
- a pick outside the list, or a custom path, raises instead of returning the flagged custom row.
- the resolver returns a location name `payload_base` refuses.

## TESTS
extensions/agi/tests/test_storage_categories.py (new; temp config only, tmp_path, never the live config written). Neighbourhood: test_locations*.py test_write*.py test_bin_help_smoke.py. Every pytest under `timeout 600`, --basetemp under /tmp.

## FILE SCOPE
extensions/agi/bin/locations.py (the new resolver + CLI only) · .agi/config.json (the one new cell block) · extensions/agi/tests/test_storage_categories.py. NOT write.py (goal:g4.18.1.1 is under review there; the wiring into the mint flow rides goal:g4.18.1.2).

## CEILING
1 kid · <= 40 production lines · pi-free tier-0 · 0 USD. No test spawns pytest; kids never launch real claude.

## CORRECTIVE DH.519 -- closes mur-director-engine-18 DH.510-k1 + k2 (accept_with_residue, verify died before returning)
BASE      CUT FROM season2/loops/hypothesis-mint-offers-storage-c-a00-a77d4234 tip 0c3d7766a. No merge. Never rebase.
1. locations.py:541-543 -- a non-dict storage category cell is skipped with `continue` and vanishes from the numbering -> refuse it BY NAME (a BAD row naming the cell, or a ValueError naming it), plus one test with a mistyped cell (DH.510 order 4, still NOT_MET).
2. locations.py:502 -- known_payload_locations admits every str KEY under locations: without checking its value, while payload_base:479-491 accepts only a non-empty str value -> admit only the names payload_base accepts; one test: a cell naming such a location is refused by name.
3. locations.py:1084-1088 -- main does not catch the ValueError raised at 583-588, so --storage-pick with a bad-location cell prints a traceback -> print the same ERR: line the other branches use and exit non-zero; one test through main.
4. experiment:a00-4bf392d4-1e7c8c is stale: verdict inconclusive_lean_disproved:45, probe-C (:18) and Still-open bullet 1 (:117-119) call the --storage-pick fall-through open, but 9f5816bdb fixed it -> RE-RUN the probe at the base, paste the output, set the verdict and bullets to what it shows (write.py only; never the thought verb over its THOUGHT).
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_storage_categories.py test_locations.py test_bin_help_smoke.py once (timeout 600, --basetemp under /tmp)
FILE SCOPE extensions/agi/bin/locations.py (storage functions + their CLI branch only) · extensions/agi/tests/test_storage_categories.py · experiment:a00-4bf392d4-1e7c8c (write.py) · the kid's own node. NOT .agi/config.json.
CEILING   HARD CAP: 1 kid · net <= 15 production lines · <= 60 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit

## CORRECTIVE DH.553 -- closes mur-director-engine-23 DH.510-k4 demote + DH.519-k1 accept_with_residue
BASE      CUT FROM season2/loops/hypothesis-mint-offers-storage-c-a00-01725b8e tip 36f928c7d (branch de-base-553; the zero-USD fix is on it or cherry-picked). No merge. Never rebase.
For EACH item: fix it in the bytes, OR -- when the item is already true, refuted by the bytes, or UNVERIFIED -- run the one command that settles it and PASTE its output on your node (never type a number). A node-text item is fixed with write.py on that node.
1. 1. non-dict storage-category cell vanishes silently (locations.py:543)
2. 2. known_payload_locations over-accepts names payload_base refuses (locations.py:501)
3. 3. CLI traceback instead of ERR: for a bad-location cell (locations.py:1085)
4. 4. the round's own deliverable is unlandable by the loop's commit gate; director hand-landed the byte (cli.py:2113)
5. 5. ceiling breach: 4 kids vs 1, locations.py +82/-18 (net 64) vs <= 40
6. 6. k4 edited a file its brief named as out of scope (locations.py:484)
7. 8. k4's mistyped-block test never exercises storage_categories: None (test_storage_categories.py:307)
8. MECHANISM, and the true severity of finding 2 — the round INTRODUCED a crash on the one case it claims to survive. main:1083 newly passes `root` into storage_categories (base 3d470e290:1022 passed none), so locations.py:555-557 now calls storage_category_target -> payload_base, which raises for any name known_payload_locations:502-503 admitted but payload_base:479-480 refuses. Probed at 0c3d7766 with locations:{docset:''}: `locations.py <root> --storage-categories` dies with an uncaught KeyError traceback. This directly falsifies the round's central deliverable ('the picker survives a mistyped config block'), and the round's own totality test (test_storage_categories.py:303-316) cannot see it because it only mistypes the storage_categories BLOCK, never a `locations:` value.
9. A GREEN TEST THAT REQUIRES A DEFECT, and a merge hazard: test_a_mistyped_block_is_an_empty_table_not_a_crash (test_storage_categories.py:303-316) asserts `storage_categories(cfg) == []`, which canonises exactly the silence the round set out to remove — locations.py:536-539 justifies the empty table 'so the config can be read and the typo seen', but an empty table PRINTS NOTHING, so the typo is never seen. The corrective the parent ordered (DH.519 order 1: a BAD row naming the cell) would make this committed test FAIL. A test that blocks its own round's ordered fix is a defect of higher order than either finding it hides.
10. EXIT CODE: the round added the BAD LOCATION stamp (locations.py:1093-1094) and then returns 0 at :1095, so `locations.py --storage-categories` on a config with a broken cell prints the diagnosis and exits GREEN. The one place a pane can learn the table is broken is the one place the shell reports success; every other error branch in main prints ERR: and returns 1 (cf. :1068-1070, :1076-1080).
11. TEST COUPLED TO THE LIVE CHECKOUT, not a fixture: test_live_seeded_cells_all_point_at_a_directory_that_exists (test_storage_categories.py:253-261, added in this merge) reads the real REPO config via find_project_root and asserts all six live targets exist on disk; :61 and :71 do the same. It only READS (no tmux/systemd/crontab/process, so not a forbidden touch), but the suite's green now moves when the live tree's directories are renamed or a fresh clone is partial — the opposite of the file's own 'Every test here builds its own temp project under tmp_path' (:5-6). This, not the docstring, is the part of finding 7 with teeth.
12. PROVENANCE/VERDICT DRIFT, unreported: the committed node .agi/nodes/experiment/a00-8c4aa1c8-73a5ad.md:26 reads `verdict: inconclusive_lean_disproved:45` while its own done-commit 48ee19286's subject records `verdict=inconclusive_lean_proved:65`. The graph and the loop log disagree on what the loop concluded about the same round; the same node is the one the parent wrote probe-C/probe-D and a 4-paragraph review into, so a reader of the graph sees a 45 and a 65 for one round. (edited_by: a00-a77d4234 is NOT a defect — it is the loop session id, identical on all four nodes at :9 in each.)
13. REDUNDANT DISK WORK, minor: main:1083 computes `rows = storage_categories(cfg, root)` and, when a pick is given, discards it — resolve_storage_category recomputes the whole table at locations.py:575, so every row's is_dir() syscall runs twice per invocation, and on a config broken per finding 2 the crash fires at :1083 before the picker's own by-name ValueError can ever be printed.
14. known_payload_locations:509 re-copies payload_base:480's value predicate instead of sharing it (one source per rule)
15. the round's new node has no refs/grid version (mint f8aaa5f2... unversioned while the hypothesis 4bd1d33... has one)
16. the ordered re-measure left a contradicted bullet standing: payload_base's duplicate known list was removed before the base
17. CEILING breach: locations.py net 20 (+24/-4) against net <= 15
18. SECOND, LARGER BREACH OF THE SAME HARD CAP, missed by the first reviewer: the corrective also caps `<= 60 test lines` and extensions/agi/tests/test_storage_categories.py is +65/-0 (git diff --numstat 0c3d7766a 36f928c7d) = 65 > 60, with the same 'a byte over it = the round is cut' clause. The node audits the production-line ceiling twice (:44, :74-79, :130-141) and never counts the test lines it was also granted 60 of.
19. .agi/nodes/experiment/a00-8b031ae3-9e4790.md:136-137 says 'Five of the 20 lines are a comment block'. It is eight (locations.py:503-506, :549-552). The one number that softens the ceiling overage is misstated in the node the verdict rests on.
20. .agi/nodes/experiment/a00-4bf392d4-1e7c8c.md:18 rewrote `production_lines: 25` → `24` while the body keeps 25 at :110 ('Net 25 production lines against the 40 ceiling') and the Agent Notes keep 25 at :141. The round corrected one copy of a measure and left two.
21. .agi/nodes/experiment/a00-4bf392d4-1e7c8c.md:15-17 replaced four probes with two, dropping probe A — the wire claim the node's own TITLE (:25) still rests on. It is still covered by committed tests (test_storage_categories.py:230 test_the_cli_marks_a_row_whose_target_is_missing, :253 test_live_seeded_cells_all_point_at_a_directory_that_exists, both in the 27 that passed), so this is residue, not a hole in the verdict.
22. Checked and NOT defects, stated so the next reviewer does not re-open them: no deletion under .agi/nodes (the diff is 2 modified + 2 added; no renames) so nothing is demoted by removal; no committed test touches a real tmux pane, systemd unit, crontab or process (the test file has no subprocess/tmux/systemd reference and writes only under tmp_path; REPO/.agi/config.json is READ at :61,70); the verdict move on a00-4bf392d4 is not a hand-fixed gate — corrective item 4 ORDERED 'RE-RUN the probe at the base, paste the output, set the verdict and bullets to what it shows', the re-run output is pasted at :117-131 and the kid's node carries it; and the BAD row really does print with the existing `BAD LOCATION` marker (locations.py:1111-1114 reads only n/key/location/prefix/label/target_exists/location_ok, all of which :553-558 supplies), so the node's :48 claim about the printer holds by reading the reader, not only by the parent's P3 probe.
OUTSIDE   an item whose fix needs a file outside FILE SCOPE: name it on your node (file:line + one sentence) for the director's findings row -- never touch that file.
ANON      no user name, home or repo path value, host or IP; patterns write <user>
TESTS     test_storage_categories.py + test_bin_help_smoke.py once (timeout 900, --basetemp under /tmp, env -u TMUX -u TMUX_PANE); tmp repos only; never a live pane, seat, worktree or real mint
FILE SCOPE extensions/agi/bin/locations.py · extensions/agi/tests/test_storage_categories.py · .agi/nodes/experiment/a00-4bf392d4-1e7c8c.md · .agi/nodes/experiment/a00-8b031ae3-9e4790.md · .agi/nodes/experiment/a00-8c4aa1c8-73a5ad.md (write.py) · the kid's own node
CEILING   HARD CAP: 2 kids (split the numbered items between them, no overlap) · <= 25 production lines net over 36f928c7d · <= 40 test lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut
PARENT    paste FILE SCOPE and CEILING verbatim into the kid brief; COMMIT every kid edit AND every node edit on the loop branch before you exit (g7.33.19 row 13)

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.553: mur-director-engine-23 DH.510-k4 + DH.519-k1 residues batched into one corrective (orders above, generated from the verdict files).
<!-- THOUGHT:END -->
