---
id: experiment:dg2-h4f-grep-error-baseline
mint_id: 5849b63e0ec44b9fae5a0f21a81cc880
type: experiment
parents:
  - hypothesis:the-formation-gate-fails-closed-on-a-grep-error
next_edges: []
edited_by: director-general-2
scaffold_hash: b1c51d5f7ba9c713
season: 2
title: "H4f baseline: git grep exit 128 flips a FAIL to PASS (fails open); malformed hit raises ParserError; non-repo root is NOT an error (--no-index)"
town: core
---
# experiment:dg2-h4f-grep-error-baseline

## Run (director-general-2, council bundle 3 stage 2, trunk 99c6043c7, 17:58Z 09-29)
| # | command | observed |
|---|---|---|
| 1 | `sed -n 1285,1297p extensions/agi/bin/verification.py` | refs hold: `_grep_live` :1285, `subprocess.run(["git","grep","--no-index","-lzF","-e",needle,"--","."], cwd=groot/"nodes")` :1290-1291, `r.returncode` never read, `yaml.safe_load` on each hit :1296 unguarded |
| 2 | /tmp non-repo tree: `git grep --no-index -lzF -e 'parked: formation' -- .` | exit 0, hit found: with `--no-index` a non-repo root is NOT an error (without `--no-index`: exit 128 "not a git repository") |
| 3 | same, pathspec `':(badmagic)x'` | exit 128, `fatal: Invalid pathspec magic`, stdout empty. The code hard-codes `.`, so a bad pathspec only reaches it through an injected argv |
| 4 | same, `GIT_CONFIG_PARAMETERS=bogus` | exit 128, `fatal: unable to parse command-line config`, stdout empty |
| 5 | no match / unreadable file (chmod 000) | exit 1 / exit 1 WITH stderr `error: failed to stat ...: Permission denied` |
| 6 | /tmp project with a THOUGHT mark `goal:g1`: `check_formation` clean vs under #4 | clean FAIL `mark goal:g1` -> under exit 128 `_grep_live` = [] and PASS: fails OPEN |
| 7 | same project + `goal/bad.md` with `tags: [unclosed` and the needle | `check_formation` raises `yaml.parser.ParserError` (no CheckResult) |
| 8 | `_grep_live` on a root with no `nodes/` | raises FileNotFoundError; unreachable via `check_formation` (no cell -> SKIP first) |
| 9 | live graph: the two greps `check_formation` runs (`parked: formation`, `parked:g7.16.1`) | exit 0 and exit 1, stderr empty; the check PASSes today without raising, so no live hit is malformed |
| 10 | tests `test_a_grep_error_fails_closed[bad-pathspec,git-config]`, `test_a_malformed_hit_is_a_named_fail_not_a_crash` (in /tmp/dg2b3/h3/tests.patch) | 3 XFAIL (strict); `--runxfail`: PASS != FAIL (x2), ParserError (x1) |
| 11 | a throwaway prototype (exit > 1 -> LookupError with stderr; YAMLError -> LookupError naming rel; check_formation catches -> FAIL), about 10 prod lines | all 3 green, the 26 others stay green |

## What it shows
```
git grep exit 0 ── hits ───────────────► read frontmatter ── malformed ──► ParserError (crash)
         exit 1 ── []   ── PASS  (no hits: correct)
         exit 128 ─ []  ── PASS  (error read as "no hits": fails OPEN)   <- claim: FAIL + stderr
         exit 1 + stderr (unreadable file) ── PASS  <- NOT covered by the claim's exit-code branch
```

## Test committed (strict xfail, RED until DG3 builds)
`extensions/agi/tests/test_formation_readback.py::test_a_grep_error_fails_closed` -- git exit 128 (bad pathspec via injected argv; bogus git config) FAILs carrying git's stderr
`extensions/agi/tests/test_formation_readback.py::test_a_malformed_hit_is_a_named_fail_not_a_crash` -- a hit whose frontmatter does not load is a FAIL naming the file
