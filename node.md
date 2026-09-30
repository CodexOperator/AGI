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
