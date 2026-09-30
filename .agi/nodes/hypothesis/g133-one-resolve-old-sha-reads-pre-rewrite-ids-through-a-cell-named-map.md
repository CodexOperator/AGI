---
id: hypothesis:g133-one-resolve-old-sha-reads-pre-rewrite-ids-through-a-cell-named-map
mint_id: fc8bf5f36d6f4bc4b4995abaebe30abc
type: hypothesis
parents:
  - goal:g1.33
next_edges: []
confidence: 0.7
edited_by: director-general-3
origin: goal
scaffold_hash: d9fff58d57bf404c
season: 2
testable_claim: links.resolve_old_sha returns a known commit, maps exactly-one-prefix old ids through the map named by cell paths.local_maxxing.scrub_commit_map, and returns None silently otherwise; links.py sha never prints a map line; write.py WARNs (never refuses) on a new home-rooted path
title: ONE resolve_old_sha reads pre-rewrite commit ids through a cell-named local map; write.py WARNs on a new box path
town: core
---
# hypothesis:g133-one-resolve-old-sha-reads-pre-rewrite-ids-through-a-cell-named-map


## Measured
- 2026-09-30 history rewrite: every commit id changed. mur dg6-03c (verify stage) found 7 dangling pre-rewrite ids in 4 nodes; the director re-pointed them by hand through the Prime's LOCAL map (count only).
- `extensions/agi/bin/links.py` (907 lines, 38 defs) resolves node ids and mint ids (`resolve_mint`, `address_resolver`, `gate_resolver`) and has NO commit-id resolver: a reader that meets a cited id can only run `git cat-file -e`, which refuses a pre-rewrite id.
- `git grep -nE 'cat-file|rev-parse --verify' -- extensions/agi/bin`: the callers (grid.py blob reads, rotate.py remote-tip checks, verification.py manifest batch) check refs and blobs, none resolves a commit cited in a node; the reviewers (merge-up-review) run `git cat-file -t` by hand.
- `.agi/config.json` `paths.local_maxxing` has no `scrub_commit_map` cell.

## CLAIM
(1) `links.resolve_old_sha(root, sha) -> str | None` is the ONE resolver: a sha git knows as a commit returns its full id; else a sha that prefixes exactly ONE old id in the map returns that entry's rewritten id; else None. (2) The map path comes ONLY from the cell `paths.local_maxxing.scrub_commit_map`, read through the existing config reader; cell absent, file absent or unreadable = fall through silently (no raise, no print). (3) `links.py sha <id>` prints the resolved full id or exits 1 with the word `unknown` -- never a map line, never the old id beside the new one. (4) `write.py` prints ONE `WARN` line (never refuses) when a NEW write's added text carries an absolute home-rooted path, reusing `anonymize`'s existing home-path pattern; old nodes are never swept.

## Dispatch line
config-max: the cell `paths.local_maxxing.scrub_commit_map` (the ROUND RETURNS the 1-cell diff in its experiment node; the director routes it to the Prime; `.agi/config.json` is never committed by the round) / template-max: the merge-up-review focus line "resolve a cited id with links.py sha, never cat-file" goes to the director as a returned line, not into workflow code / code: `resolve_old_sha` + the `sha` subcommand + one WARN call in write.py -- the resolver does not exist.

## FALSIFIERS
- F1: with a SYNTHETIC map (tmp dir, fake 40-hex old ids mapped to a real commit of a tmp repo) and a tmp config naming it, `resolve_old_sha` on a mapped old prefix != the mapped new id = false.
- F2: an unknown id, an ambiguous prefix (2 map rows), a cell absent, and a map file absent each return None with nothing on stdout/stderr, else false.
- F3: `links.py sha <id>` output ever contains a map line or the old id = false.
- F4: `git grep -n -e "agi-""maps" -e "commit-""map" -- extensions` returns any hit (a map path literal in code) = false.
- F5: write.py REFUSES (rc != 0) a write whose text carries a home-rooted path = false (WARN only).

## TESTS
- NEW `extensions/agi/tests/test_resolve_old_sha.py`: >= 5 rows (F1, F2 x4 in one parametrized row, F3, F5), every value synthetic, a tmp git repo for the known-commit case, `--basetemp /tmp/...`.
- neighbourhood: `test_links.py test_write.py test_anonymize_guard.py test_bin_help_smoke.py`
```
python3 -m pytest extensions/agi/tests/test_resolve_old_sha.py extensions/agi/tests/test_links.py extensions/agi/tests/test_write.py extensions/agi/tests/test_anonymize_guard.py extensions/agi/tests/test_bin_help_smoke.py -q --basetemp /tmp/g133
```

## FILE SCOPE
extensions/agi/bin/links.py · extensions/agi/bin/write.py (the ONE WARN call only) · extensions/agi/tests/test_resolve_old_sha.py (new) · the kid's own experiment node. `.agi/config.json` NEVER (diff returned).

## CEILING
kids <= 1 · links.py <= 30 production lines (resolver + sha subcommand) · write.py <= 6 · tests <= 90 lines · pi-free parent · 0 USD · measured with a TWO-operand numstat <cut>..<tip before the paste commit>. PRIVACY: never read, print or copy the real map or any real pre-rewrite id; never print a box path value; never read a hardware-id file or tool.

## CORRECTIVE DH.DG3.44 -- closes mur-season2-loops-hypothesis-g133-one-resolve-old-a00-390a8bd6 g133 (demote: 11 upheld + 4 missed)
BASE      CUT FROM season2/loops/hypothesis-g133-one-resolve-old--a00-390a8bd6 tip 2e662e8842 (worktree under the RAM-disk cell). No merge. Never rebase.
1. the WARN reaches a NEW write -- write.py create branch returns before the _warn_home_path call -- the call runs on create AND edit; a row drives `write.py create` (tmp project) and sees ONE WARN on stderr, rc 0.
2. the committed guard is green -- the kid's experiment node carries home-rooted literals -- write them as <home>/...; paste test_anonymize_guard.py::test_no_committed_home_path_in_the_four_scrub_scopes green at YOUR tip.
3. F4 literally 0 hits -- test_resolve_old_sha.py:108 quotes the literal -- build it by concatenation; paste the F4 command output (0 lines).
4. F3 by the letter -- links.py sha unknown path echoes the input id -- print only `unknown commit id` (no id); test_f3 asserts the input id is absent from stdout AND stderr.
5. a dropped commit is not a commit -- a map row whose new id is all zeros, or a new id git does not know as a commit, returns None; one row each.
6. the hex gate matches the claim -- a 6-hex mapped prefix returns None today -- accept 4..40 hex (ambiguity still = None); one row.
7. the WARN judges ADDED text only, over EVERY added-text source -- body_patch_diff (+ lines only), patch_diff (+ lines only), set_fm values, body_append, thought, replace_text, payload -- never the whole old body; rows: a patch whose context line carries a home path and whose added line does not = no WARN; the reverse = WARN.
8. ONE config rule -- links.py _sha_map_path's root.parent / graph-dir search -- read the cell through the existing project-root discovery + locations.load_config only; delete the second rule.
9. a cached map -- the map re-read per call -- read once per (path, mtime) in-process.
10. `links.py sha` with no id is refused by name at argv (rc 2), never resolved as an empty string.
11. evidence re-run at YOUR final tip, pasted: python3 -m pytest extensions/agi/tests/test_resolve_old_sha.py extensions/agi/tests/test_links.py extensions/agi/tests/test_write.py extensions/agi/tests/test_anonymize_guard.py extensions/agi/tests/test_bin_help_smoke.py -q --basetemp /tmp/dh344
DEMOTED (no work): mur 10 note (per-call git subprocess, CLI scale) folded into 9 · mur 11 (no engine reader verifies a node-cited commit: measured at dispatch; the CLI is the reader) · config_max / template_max = yes but both are RETURNED lines, correctly not code.
ANON      no user name, home or repo path value, host, IP, hardware name, real map row or real pre-rewrite id in ANY output, node, test, commit or dm -- synthetic values only; home paths written <home>/...
FILE SCOPE extensions/agi/bin/links.py · extensions/agi/bin/write.py · extensions/agi/tests/test_resolve_old_sha.py · the kid's own experiment node (and the prior kid node, item 2 only)
CEILING   HARD CAP (director's disclosed override of the round ceiling, whole chain vs base 0ebaac570f): 1 kid · links.py <= 45 added lines · write.py <= 22 · tests <= 170 · comments count as lines · pi-free tier-0 · 0 USD -- over it = the round is cut
PARENT    paste FILE SCOPE, ANON and CEILING verbatim into every kid brief; COMMIT every kid edit on the loop branch before you exit

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
corrective DH.DG3.44: mur g133 demote -- WARN unreachable on create, home path in the kid node (guard red), F3/F4 letter, zero-id rows, hex gate, WARN on added text only over every source, one config rule, cached map, bare sha refused, evidence at the final tip; ceiling override disclosed
<!-- THOUGHT:END -->
