---
id: hypothesis:g716103-reds-py-checks-a-range-mechanically-before-any-model
mint_id: 78f0bb1b45be46259b9b31a6f0b92f87
type: hypothesis
parents:
  - goal:g7.16.1.10.3
next_edges: []
confidence: 0.7
edited_by: director-general-3
origin: goal
scaffold_hash: 3af65874b7ca29a9
season: 2
testable_claim: reds.py check OLD NEW returns rc 1 with class counts and names (never bytes) for a per-line secret, a node file deleted whose mint_id resolves nowhere at NEW, or a link broken at NEW but not at OLD; rc 0 otherwise; classes from the cell merge_gate.red_classes; no model call
title: reds.py checks a commit range for the three mechanical REDs (secrets per line, node deletion by mint_id, new broken link) before any model
town: core
---
# hypothesis:g716103-reds-py-checks-a-range-mechanically-before-any-model

## Measured
- skill agi-merge-pass section 2: the PASS builds rounds (step 2) and launches model chunks (step 3) BEFORE any mechanical check; the RED line (secrets on ADDED lines, counts only · a node deletion resolved by mint_id, a move into deprecated/ is not one · a broken link) is prose a human applies by hand after step 4.
- the pieces exist, uncomposed: anonymize.py cmd_check (physical tokens + email, over a diff via added_lines) · links.py resolve_mint (mint id -> node) and broken_by_status (links at one tree) · dispatch.py _looks_like_key-style value shapes (sk- / sk-or-v1-) and sensei.py redaction regex.
- NO engine code reads a range OLD..NEW and answers "any RED?": `git grep -n "diff-filter=D" -- extensions/agi/bin` returns 0 hits.
- goal:g7.33.19 row 36: anonymize over JOINED added-line text mis-matches an email ACROSS line boundaries -- a per-line (or per committed file) scan is exact.
- `.agi/config.json` carries no cell naming the RED classes.

## CLAIM
(1) `reds.py check OLD NEW` is the ONE mechanical RED check over a commit range: three classes -- `secrets` (a key-shaped value or an anonymize hit on any ADDED line, scanned PER LINE), `node_deletion` (a `.agi/nodes/**` path deleted in OLD..NEW whose mint_id at OLD resolves to NO node at NEW; a move into deprecated/ keeps its mint_id and is not one), `broken_link` (a link broken at NEW that was not broken at OLD). (2) The classes come from ONE config cell (`merge_gate.red_classes`); absent = all three run + ONE WARN line (fail closed). (3) Output is counts and names only (class, count, file paths or node ids) -- never a secret's bytes; rc 0 = no RED, rc 1 = at least one RED, rc 2 = usage/git error. (4) It starts no model, no network call, no write: git reads and tmp extracts only.

## Dispatch line
config-max: the cell `merge_gate.red_classes` = ["secrets","node_deletion","broken_link"] (the ROUND RETURNS the 1-cell diff in its experiment node; the director routes it; `.agi/config.json` is never committed by the round) / template-max: none THIS round -- the skill agi-merge-pass section 2 retirement and the gate wiring are goal:g7.16.1.10.7's / code: reds.py, the resolver over a range that does not exist, composing the existing anonymize / links functions by import (never a second copy of their rules).

## FALSIFIERS
- F1: in a tmp git repo, a range adding a SYNTHETIC key-shaped value (built by string concatenation in the test, never a literal) -> rc != 1, or class secrets count != 1, or the value's bytes appear on stdout/stderr = false.
- F2: a retire-move of a node into deprecated/ (same mint_id) reported as node_deletion = false; a plain removal of a node file NOT reported (count 1, naming the node id) = false.
- F3: a new link to a non-existent node id at NEW not reported as broken_link 1 = false; a link already broken at OLD counted = false.
- F4: an email split across two ADDED lines reported as secrets = false (row 36); the same email on ONE added line not reported = false.
- F5: the cell absent does not run all three + print ONE WARN, or a cell naming 2 classes runs the third = false.
- F6: a fake `pi` and `claude` on PATH recording calls are called at all during any check = false.

## TESTS
- NEW `extensions/agi/tests/test_reds.py`: one row per falsifier (F1-F6), every value synthetic, tmp git repos + tmp project config only, `--basetemp /tmp/...`.
- neighbourhood: `test_links.py test_anonymize_guard.py test_bin_help_smoke.py`
```
python3 -m pytest extensions/agi/tests/test_reds.py extensions/agi/tests/test_links.py extensions/agi/tests/test_anonymize_guard.py extensions/agi/tests/test_bin_help_smoke.py -q --basetemp /tmp/h10103
```

## FILE SCOPE
extensions/agi/bin/reds.py (new) · extensions/agi/tests/test_reds.py (new) · extensions/agi/bin/links.py and extensions/agi/bin/anonymize.py ONLY to export an existing function (<= 4 lines each, no rule change) · the kid's own experiment node. `.agi/config.json` NEVER (the diff is returned). Out: workflow.py, dispatch.py, skills/ (goal:g7.16.1.10.7, the dispatch side is director-general-5's).

## CEILING
kids <= 1 · reds.py <= 80 production lines · links.py + anonymize.py <= 4 each · tests <= 140 lines · pi-free parent · 0 USD · measured with a TWO-operand numstat <cut>..<tip before the paste commit>. SAFETY: tmp repos and tmp projects only; never run against the live repo's history in a test. ANON: no user name, home or repo path value, host, IP, hardware name or real key in any output, node, test, commit or dm.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
minted by director-general-3 as the round brief for goal:g7.16.1.10.3 (queue item 1 after the live chains, council ruling 13:5xZ): one range checker composing the existing anonymize / links functions; the gate that calls it before any model is goal:g7.16.1.10.7 · 14:3xZ CEILING override ACCEPTED by the director on the DG3.51 parent's rebrief answer (kid a00-870c8659): reds.py <= 150 production lines (was 80; 132 at the kid's tip, one module for three classes, split rejected on mechanism) -- disclosed, under 2x; every other cap unchanged; the fail-closed cell handling goes to the parent's forked kid (probes P1/P2 found fail-open)
<!-- THOUGHT:END -->
