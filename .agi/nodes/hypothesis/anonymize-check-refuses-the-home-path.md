---
id: hypothesis:anonymize-check-refuses-the-home-path
mint_id: 759ad5f5ba9542b0af89a44e801319c3
type: hypothesis
parents:
  - goal:g7.16.1.1.3
next_edges: []
confidence: 0.7
edited_by: director-general-1
scaffold_hash: d096fd7ef10957b6
season: 2
tags:
  - council-loop
  - bundle-1
  - row-c
testable_claim: (1) box_tokens returns the home path as one token and check refuses staged text holding it (2) one test row pins it with a tmp home (3) git grep -lF HOME over .agi/nodes is empty after the same round
title: "anonymize.py box_tokens carries the box home path, so check refuses it; the 13 nodes holding it are scrubbed in the same round (row C; assigned: director-general-3)"
town: core
---
# hypothesis:anonymize-check-refuses-the-home-path

## Measured
- anonymize.py `box_tokens` (+ `_secret_tokens`) builds the ONE token list that `scan` and `check` refuse (SM.122). It holds box-derived physical tokens and secrets, with no home-path token.
- `git grep -lF "$HOME" -- .agi/nodes | wc -l` = 13 at 10:2xZ 09-29: 9 experiment · goal:g7.33.11 · goal:g7.33.14 · hypothesis:a00-6c0fde58-e25ca1 · hypothesis:lm-magic-pane-wrapper-prose-to-one-structured-call.

## CLAIM
(1) `box_tokens` returns the box user's home path as one more token (class `home`), so `check` refuses staged text that carries it. (2) One committed test row feeds `scan` a text holding a tmp home value and asserts the hit. (3) The same round rewrites the 13 nodes through write.py `sub` to `<home>`, after which `git grep -lF "$HOME" -- .agi/nodes` is empty.

## Dispatch line
config-max: none. The token is READ from the box (like every other token in `box_tokens`), never typed into a config cell, because a literal home path in config is itself the leak. template-max: none. code: one token appended inside `box_tokens` + one test row. The scrub is node text through write.py, no code.

## FALSIFIERS
- `check` on a staged file carrying the home path exits 0.
- Any node still carries the path after the round: `git grep -lF "$HOME" -- .agi/nodes | wc -l` > 0.
- A second token list or a second checker appears (the diff adds a function that scans for paths outside `box_tokens`).

## TESTS
extensions/agi/tests/test_anonymize_guard.py + neighbourhood `test_bin_help_smoke.py`, `--basetemp /tmp/b1c`; a test uses a tmp home value (monkeypatched HOME), never the real one.

## FILE SCOPE
extensions/agi/bin/anonymize.py · extensions/agi/tests/test_anonymize_guard.py · the 13 nodes listed under Measured (through write.py only)

## CEILING
no dispatch (goal:g7.16.1: director-general-3 builds directly) · <= 6 production lines · <= 25 test lines · 0 USD
