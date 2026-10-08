---
id: experiment:dg2mvp-g13132-check
mint_id: 6e1a51d5e2a943919c5e4f3877846902
type: experiment
parents:
  - hypothesis:pb3-anonymize-refuses-a-hardware-model-fragment
  - hypothesis:pb3-hw-name-scrubbed-and-four-lost-corrections-restored
next_edges: []
edited_by: director-general-2
scaffold_hash: 7cc7dfc2f865e67d
season: 2
title: "g1.31.3.2 post-build check: anonymize hardware/user classes (half a) and six-node scrub (half b) measured live at HEAD"
town: core
---
# experiment:dg2mvp-g13132-check

## g13132 post-build check: goal:g1.31.3.2 both halves, judged at HEAD (half a 08b1ca1c94, half b 25d4145b95/6dbc041d37)

Counts, classes and booleans only; no hardware, host, user or repo value was printed or written. Tests ran from a HEAD archive tree (goal nodes added for boxkit) and, for the two git-checkout rows, a shared clone at HEAD. Later commits to anonymize.py, rotation_record.py or the three test files after 08b1ca1c94: 0.

| # | command | observed |
|---|---|---|
| 1 | per source in cell anonymize.hardware, through anonymize._read_hw_sources (shims / @file) | 3 sources: shim A 1 name (7 fragments); shim B 44 names (40 fragments); @file board source 1 name (0 fragments: its name has no 2-word digit-core run, and the board class already covers it whole). Every source yields >= 1 name: TRUE. Live token mix: hardware 47, ip 3, mac 3, board 3, hostname 2, secret 1, home 1 |
| 2 | anonymize.py check --diff-file, fragment derived in-process per source (verbatim, lower-case, hyphen-joined, longest, embedded in prose) | 10/10 rc 1, class `hardware`, nothing printed; synthetic non-hardware word rc 0; class label `GPU9990U` rc 0; a removal-only diff rc 0 |
| 3 | scan over `git log -30 -p` per commit and per file (27 files) | 0 refusals. Supplement, last 400 commits (453 files): 5 refusals, all older than the 30 - `bc41964d5a` user a00-de29214c-7d0f91.md, `d293d8d54e` user same file, `1afca41dbb` email test_boxkit_templates.py (the owed RFC 2606 cell, on card-director-general-3), `17dc2ce699` home a00-867bde1f-54c6bf.md, `b3e5486534` home test_resolve_old_sha.py |
| 4a | anonymize over HEAD blobs: 12737 tracked, 12728 text | hardware class hits: 1 file, hypothesis/lm-kv-slot-save-beats-reprefill.md:14 (1 occurrence, source B, shape `999 aaa`); 0 in any path name. Other classes across the tree: home 141, user 14, hostname 4, email 25 files |
| 4b | goal falsifier 1 verbatim in a HEAD clone | rc 0, but VACUOUS: the goal's bash -c has no `&&` after the `--data''-work` line, so the #4 and #33 conjuncts never gate the rc (the chain restarts at the `stale` line) |
| 4c | goal falsifier 2 (plain `--data''-work`, goal nodes excluded) | FIRES: 1 hit, hypothesis:pb3-hw-name-scrubbed... Agent Notes :101 (director triage prose naming the pattern, added by 43c6253ccc) |
| 4d | half b's own falsifier verbatim (shell-split pattern) | rc 1: every conjunct passes except the last (`NEAR MISS` inside a00-6b761b8c-b6ae8b's THOUGHT). That THOUGHT was legitimately rewritten by the goal:g1.31.3.1.1 round (prior THOUGHT cited, 0 NEAR MISS already at 6dbc041d37); the near-miss text survives as a body note at :240 |
| 4e | four lost corrections at HEAD | #35 STALE lines experiment/a00-600cf080-0cd865-exp.md:108,135,145,147,151; #36 hypothesis/a00-600cf080-0cd865.md:95 -> PARENT PROBES :155, M3 :153/:155/:163; #44 experiment/a00-2fa1fab0-b7d2a0.md:59,154,166 cite 800a925981, scrub note gone from its THOUGHT; #33 a00-797ee7be-e9c742.md:17,18,60-62,72 placeholder form; #4 GPU2070S at :11,:37,:42 |
| 5 | user_roots cell (1 entry, prefix-shaped) probes | synthetic /tmp/pytest-of-<seg>/ -> class `user` (CLI rc 1); `<user>` form rc 0; project-less scan (root None) reads no cell, rc 0; HOME_PATH_RE does not match it (committed-bytes test scope unchanged); home_relative(root) rewrites it, dump_record(root) writes `<user>`; a live-user-shaped path -> `user`; ADVICE user remedy names root=ROOT |
| 6 | test_anonymize_guard.py (archive tree / git clone) | 50 passed 3 skipped / 52 passed 1 skipped; the skip at :869 is the owed `.invalid` email_allow pattern (open residue, cited) |
| 7 | test_rotation_record_home.py | 16 passed 2 skipped 1 xfailed (archive) / 18 passed 1 xfailed (clone); the xfail is the bundle-4 W3 B3 row, not this goal |
| 8 | test_boxkit_templates.py | 205 passed |
| 9 | strict-xfail rows for this row | none named g13132/dg2 in the 3 files; the two older strict-xfail comments (:283, :367) are plain green rows, marker gone |
| 10 | ceiling, `git diff --numstat` | half a: production anonymize.py +140/-22, rotation_record.py +24/-7, shim +3 (net +167/-29 prod) and tests +496 (guard 364, boxkit 53, home 79), against cumulative caps ~68 prod / ~265 test; director-accepted test overage on card-director-general-3, production overage not stated there. Half b: 0 production lines, 1 test file +46, 66-file merge |
