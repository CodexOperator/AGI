---
id: experiment:dg2mvp-g133-check
mint_id: 61b64ede3bbf48b1b4cb905ae24470a2
type: experiment
parents:
  - hypothesis:g133-one-resolve-old-sha-reads-pre-rewrite-ids-through-a-cell-named-map
next_edges: []
edited_by: director-general-2
scaffold_hash: 7069b299f18f32e8
season: 2
title: "g133 post-build check: resolve_old_sha MAP branch live, silent on every miss, one reader, cell-only path"
town: core
---
# experiment:dg2mvp-g133-check

## g133 post-build check: does 5f1e8092f2 satisfy the hypothesis (judged at HEAD faa8516346, no later commit touches links.py, write.py, test_resolve_old_sha.py, test_links.py, test_write.py)

| # | command | observed |
|---|---|---|
| 1 | links.resolve_old_sha on an OLD id picked from the live map (first column only; a row whose old id git lacks and whose new id git knows), from a HEAD archive tree, root = the repo | returns a 40-hex id, == the mapped column 2, is a commit in the repo, differs from the input; stdout+stderr empty. TRUE |
| 2 | same id as a 12-hex prefix | resolves to the same id. TRUE |
| 3 | CLI `links.py sha <old40>` and `<old12>`, stdout+stderr captured | rc 0, exactly ONE stdout line == the new id, stderr empty; no line carries two 40-hex ids; the old id is never echoed. F3 not fired |
| 4 | CLI `links.py sha deadbeefdeadbeef` (map miss) / no id | rc 1 + `unknown commit id` (input never echoed) / rc 2 `ERR: sha needs a commit id`; no crash, nothing else printed. TRUE |
| 5 | the brief's pick, file line 2 old id | git lacks it AND its new id is not in this repo: None, silent (by design, a dropped/unreachable commit is not a commit). Across the map: 17414 rows old-unknown+new-known (resolve), 41809 old-unknown+new-unknown (None), 20343 old ids git knows itself |
| 6 | synthetic tmp project, real files: cell absent / map file absent / map chmod 000 / binary junk row + good row / ambiguous 8-hex prefix (2 rows) / new id all-zero / new id not a commit / good row / known sha | None (silent) x7 (first six + zero + not-commit), junk+good row resolves, exact 40-hex among 2 sharing a prefix resolves, known sha returns itself; output empty in every case. F1, F2 not fired. CLI with map absent: rc 1 `unknown commit id`, stdout empty |
| 7 | `git grep -nE 'def resolve_old_sha\|commit-map\|commit_map' -- extensions/agi/bin` | 3 hits, all in links.py: the `_sha_map_path` docstring + cell read (608, 614) and `def resolve_old_sha` (648). The only map reader is `_map_rows` (630), called once, from resolve_old_sha (660): ONE resolver, ONE reader. TRUE |
| 8 | `git grep -nE '/data/agi-maps\|/data/scrub\|agi-maps' -- extensions/agi/bin` | 0 hits: the path comes only from `.agi/config.json` cell `paths.local_maxxing.scrub_commit_map` through `locations.find_project_root` + `load_config` (links.py 607-616; the cell exists at HEAD). TRUE |
| 9 | F4 as written `git grep -n -e "agi-""maps" -e "commit-""map" -- extensions` | 0 hits. Not fired. The map file lies outside the repo (never tracked) |
| 10 | write.py WARN: synthetic tmp project, `write.py create hypothesis ... --body-file` whose text carries a home-rooted path; then clean body; then `note` edit carrying one | create: rc 0, exactly 1 `WARN:` line on stderr, node written, path value not echoed; clean create: 0 WARN; edit: rc 0, 1 WARN. F5 not fired (write.py never refuses). Call sites write.py 3987 (create) and 4248 (edit, after stdin read); patterns reuse `anonymize.HOME_PATH_RE` |
| 11 | test_resolve_old_sha.py from the HEAD tree | 17 passed |
| 12 | test_links.py | 48 passed, 1 skipped (live pin: no subject), 1 xfailed (test_w2cb_*: BANKED 86, another row) |
| 13 | test_write.py (whole) | 206 passed, 1 xfailed (test_w3c_*: another row); the two test_g73320_* rows were green here (no red to name) |
| 14 | CEILING `git show --numstat 5f1e8092f2 -- extensions` | links.py +73/-1, write.py +76/-50, test_resolve_old_sha.py +220. Original ceiling links<=30, write<=6, tests<=90: over. Already closed: disclosed override DH.DG3.44 (hard cap) and DH.DG3.46 (goal:g7.33.19 row 33) on the hypothesis node |
| 15 | my strict-xfail rows for g133 | none exist (git grep g133 over test_links, test_write finds no marker); the two xfails are other rows, unchanged |
| 16 | goal end-state bullet 3 "every engine reader calls it" | no engine reader verifies a node-cited commit; `links.py sha` is the reader. Already DEMOTED on the node (DH.DG3.44 item 11, measured at dispatch). Cited, not re-raised |

Open SM residues (card-sanctuary-master, card-director-general-3): nothing open on g133; mur g133d residues (F9 demote, file count) closed on the node, cited not re-raised.
