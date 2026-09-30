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

## CORRECTIVE DH.DG3.54 -- closes mur-season2-loops-hypothesis-g716103-reds-py-check-a00-da20f44e h10103-reds + h10103-tests (both accept_with_residue; verify upheld)
BASE      CUT FROM season2/loops/hypothesis-g716103-reds-py-check-a00-da20f44e tip 2f375f5154 (worktree under the RAM-disk cell). No merge. Never rebase.
1. node_deletion fails CLOSED -- reds.py _node_deletions, the except that sets alive True -- a resolver that raises makes the check rc 2 naming the class, never a silent survive; AND a node survives only when the node carrying its mint at NEW did NOT already exist at OLD under another id (a mint reused by a different, pre-existing node is a deletion); one row each.
2. extract only the graph -- reds.py _extract -- git archive with the .agi pathspec only (the config and nodes the check reads); paste one timed live check (rc and seconds only) before and after.
3. errors never echo raw git stderr -- reds.py _git -- the rc-2 line names the git verb and its exit code only (no stderr bytes, no path); a row asserts no absolute path reaches stderr on a bad rev.
4. a malformed config is rc 2 -- reds.py main, _classes runs outside the rc-2 guard -- a config.json that does not parse gives rc 2 with one line naming the cell file class, never a traceback; a row.
5. rc 2 is pinned -- test_reds.py -- rows: a bad rev and a malformed config each return rc 2.
6. broken_link counts BOTH halves -- reds.py _broken_links reads only the live half of links.broken_by_status -- live and retired broken links, NEW minus OLD; a row with a link broken on a deprecated node at NEW only.
7. a bare key-shaped value is a RED -- reds.py _secrets matches only name = value pairs -- every added-line token with the key shape the engine already names (dispatch value shape) is a hit, whether or not a name precedes it; a row (value built by concatenation, never a literal).
8. the gate passes its own bytes -- test_reds.py commit-identity arguments use an address the landed anonymize.email_allow cell admits (example.com), never .invalid; paste reds.py check <cut>..<your tip> on this repo read-only: RED none for secrets on test_reds.py.
9. one source in the test -- test_reds.py re-declares CLASSES -- import reds.CLASSES.
10. no blank stdout line -- reds.py main prints an empty line when a RED exists -- print the RED none line only when none.
11. evidence that can exist -- the chain's experiment nodes: the transcripts pairing RED with rc 0 (a00-22944b9e-eadf7b, a00-a2ea1ace-6b1e76) and the false cite of the fail-open line as the class-cell line (a00-870c8659-37df21, a00-f76f6632-37b944) are corrected with write.py in place (name the function, not a line), and the stale VERDICT STATE line in a00-870c8659-37df21 is removed.
12. evidence at YOUR final tip, pasted, + a labelled numstat 2f375f5154..<tip before the paste commit>: python3 -m pytest extensions/agi/tests/test_reds.py extensions/agi/tests/test_links.py extensions/agi/tests/test_anonymize_guard.py extensions/agi/tests/test_bin_help_smoke.py -q --basetemp /tmp/dh354
ANON      no user name, home or repo path value, host, IP, email address, key-shaped value or hardware name in ANY output, node, test, commit or dm -- patterns write <user>
FILE SCOPE extensions/agi/bin/reds.py · extensions/agi/tests/test_reds.py · the four chain experiment nodes named in item 11 (write.py only) · the kid's own experiment node. NEVER the hypothesis node, .agi/config.json, links.py, anonymize.py, dispatch.py.
CEILING   HARD CAP: 1 kid · reds.py NET <= +30 production lines · test_reds.py NET <= +40 lines · pi-free tier-0 · 0 USD -- a byte or kid over it = the round is cut; ask BEFORE, never after
PARENT    paste FILE SCOPE, ANON and CEILING verbatim into every kid brief; COMMIT every kid edit AND merge the kid branch into the loop branch before you exit

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DG3.51 forked kid: the build round proved five of six conjuncts on its own bytes, and the parent probe refuted the sixth (fail closed) — a present-but-empty or all-unknown merge_gate.red_classes filtered to the EMPTY SET, and an empty set reads as "run nothing": the gate that must hard-stop a round disabled itself on a typo. Fixed in _classes (14 production lines) with a test row that plants a key line AND a deleted node and asserts rc 1, all three classes and exactly ONE WARN. Lesson carried into the docstring: fail-closed is a property of the CALLER default, not of the filter.
<!-- THOUGHT:END -->
