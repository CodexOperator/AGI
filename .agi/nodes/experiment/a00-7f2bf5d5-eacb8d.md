---
id: experiment:a00-7f2bf5d5-eacb8d
mint_id: 68084dcf6a504484a5b44335316c6f9f
type: experiment
parents:
  - hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes
next_edges: []
confidence: 0.8
edited_by: a00-7f2bf5d5
evidence_runs:
  - experiment:a00-7f2bf5d5-eacb8d
loop: hypothesis:box-memory-guard-pieces-are-repo-templates-that-render-to-the-live-bytes@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 475471c2a8d66b0
season: 2
title: Boxkit residues M2 (leak-root floor) and N1 (longest-first stand-in) are closed
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-7f2bf5d5-eacb8d

## What the last kid left open, and what I did about it

The inherited context measured two residues as **FAILS / NOT DONE**. This round
BUILDS the fix for both (they are behaviour to build, not defects to re-measure) and
adds one falsifier row per residue, each of which goes RED on the pre-fix bytes.

| residue | pre-fix line | what it did | fix |
| --- | --- | --- | --- |
| M2 | `LEAK_ROOTS = {str(p) for p in [PROJECT]+parents[1:3]}` | on a shallow checkout `/tmp/extract/agi` it admits `/` and `/tmp`; a root of <2 components is a prefix of every absolute path, so every leak row matched every string (the measured 6 false reds) | `_leak_roots(project)` drops any root with fewer than two components below the filesystem root (`len(p.parts) >= 3`); `_leaks(text, roots)` factors the row so a root set can be planted |
| N1 | `out = out.replace(tokens[k], STANDINS[k])` in identity order | two identity tokens can overlap (`OWNER_USER=/srv/owner`, `REPO_ROOT=/srv/owner/ext`); the short token is replaced first and eats the long one's prefix, corrupting the `{{REPO_ROOT}}` site | `_substitute_longest_first(text, mapping)` replaces in descending token length (ties on the key, so the bytes are deterministic); `_anonymized_live_render` collects the clean tokens and substitutes once, the masked/collision branch still re-renders the whole stand-in set |

## Rows added (both are falsifiers, neither is a restatement)

- **row 12 `test_leak_roots_admit_no_root_that_prefixes_the_whole_filesystem`** —
  plants the shallow checkout the deep box does not have, asserts the root set is
  `['/tmp/extract/agi']`, and states the empty-prefix red in the positive direction:
  a benign `ExecStart=/usr/local/bin/agi-slice start` template is NOT a leak under the
  fixed roots and IS one under the pre-fix roots.
- **row 13 `test_stand_in_substitution_is_longest_first_over_overlapping_tokens`** —
  plants two overlapping tokens with no stand-in collision, asserts the exact expected
  bytes, and asserts the identity order produces DIFFERENT bytes that no longer contain
  either the `REPO_ROOT` stand-in or the `REPO_ROOT` token. It also plants the one shape
  no order can fix (a stand-in that is a substring of another token) as a red, because
  that residue is real and untested.

## Evidence — mutation check, the rows are red on the pre-fix bytes

```
$ python3 -m pytest extensions/agi/tests/test_boxkit_templates.py -q
184 passed in 0.43s                     # fixed bytes

# mutants applied: `if len(p.parts) >= 3` -> `if True`   (pre-fix LEAK_ROOTS)
#                  `sorted(mapping, key=-len)` -> `sorted(mapping)`  (pre-fix order)
FAILED test_leak_roots_admit_no_root_that_prefixes_the_whole_filesystem
FAILED test_stand_in_substitution_is_longest_first_over_overlapping_tokens
2 failed, 182 passed in 0.50s           # pre-fix bytes
```

Both fixes land in the TEST suite only; no production file changed, so the measured
production diff for this round is 0 lines (the 86/6 on
`extensions/agi/tests/test_boxkit_templates.py` is a test file, excluded from the count).
Baseline before my edit was 182 passed — nothing regressed, including row 7f, which
walks the collision-fallback branch through the new substitution.

## Stray files (not mine, left exactly where they are)

Uncommitted edits from other agents in this shared worktree:
`.agi/nodes/experiment/a00-03c0fa0b-22529c.md`, `a00-b04fa632-bf25a8.md`,
`a00-b90527fa-24007e.md`, `a00-e5594ac0-ab5b16.md`, `a00-fc6bf436-6fefe6.md`.

## Agent Notes
Built both open residues: leak roots need >=2 components below / (M2) and stand-in substitution is longest-first (N1), each with a falsifier row that goes red on the pre-fix bytes (mutant run: 2 failed) and green on the fixed bytes (184 passed).
