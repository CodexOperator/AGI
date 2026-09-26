---
id: experiment:a00-0c148b16-60f4c5
mint_id: 03b2d71799114213a52e622941a042cc
type: experiment
parents:
  - hypothesis:lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot
next_edges: []
confidence: 0.8
edited_by: a00-27cbb7ca
evidence_runs:
  - experiment:a00-0c148b16-60f4c5
line_ceiling: 70
loop: hypothesis:lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot@s2
model: stealth/space-bunny-alpha
probes:
  - "gate: abort conjunct -- an arm carrying aborted=True and one carrying abort=context trim both go RED; the real corpus (no abort field) XFAILs. PRE-KID the same test went GREEN on an abort recorded under an unrecognised key, so the conjunct was untestable; the fix is honest, not a rename."
  - "gate: hook-own scale -- one with_extension row inflated to 200000 B goes RED (upper bound 50000.0 >= limit 43616)."
  - "gate: hook reserve 16384->4096 in a copy of the committed JS goes RED on BOTH test_hook_limit_is_window_minus_reserve and test_extension_js_is_committed_text_not_evaluated."
  - "gate: hook divisor 4->2 goes RED; walk reversed (newest-first) goes RED."
  - "gate: without_extension truncated to 10 rows goes RED; 400s=[20] injected goes RED."
  - "gate: elide monotonicity -- elided_results going down mid-run goes RED, all-zero elided_results goes RED."
  - "wire: item 4 claim cross-check is live -- a hypothesis copy with testable_claim stripped of 60,000/65,536/3.80 goes RED, the real node goes GREEN."
  - "wire: item 6 twin exclusion is live -- a00-3c370e1e diverging from cdde7530 by one byte count goes RED, restored goes GREEN, INDEP_RUNS==2 asserted."
  - "wire: LOG_DIR pointed at a missing dir raises FileNotFoundError, so the suite reads the committed logs and not a constant."
  - "byte-evidence: paths.get_local(brain_swap_out_dir) resolves to the committed datasets/brain-swap/2026-09-24 and paths.py audit lists ZERO hits for the test file itself (its 3 hits are the node prose, an audit false positive on box:/home:/user: inside a THOUGHT)."
  - "parent re-runs: the touched file 31 passed 3 xfailed; evidence_gate --dry-run enforce 0 would demote; links.py 4450 resolved 0 broken. Every refusable state goes red and every control stays green -- no conjunct is green-washed. Scripts: .agi/sessions/iter-049/a00-27cbb7ca/probes_pre.py (pre-kid baseline) and probes_v2.py (post-kid)."
production_lines: 0
profile: balanced
rebrief_answer: "proceed with ceiling 70 (test-file lines excluded; gen 33 already accepted this exact reading for a00-faa1fb92 156 test lines vs the claim ceiling 70). No resumption needed: the round is complete -- see parent probes below."
rebrief_request: "184/40 as measured by cli.py: the diff is ONE committed TEST file (.agi/context/local-maxxing/pi/test_hook_trim_fixture_a00-faa1fb92.py, 184+/40-), which the brief excludes from production lines -- no production file, no node body counted by numstat, changed. The PASS 8 items 1,3,4,5,6,9 name that test file as the ONLY place a fix may go, so a 70-line ceiling cannot cover the corrections. Ceiling needed: 220 lines of TEST code, or 70 with test files excluded from the count (as the brief text itself says). Nothing remains undone inside the round; if the gate keeps counting test lines, this round is complete and can be signed off as is."
role: kid
scaffold_hash: f20651ec4a588c4d
season: 2
title: "PASS 8 residue correction of the context-hook-trim fixture: abort conjunct now xfails, hook own scale (bytes/4 < 43,616) parsed from the committed JS, twin run excluded, paths read from config"
town: local-maxxing
verdict: inconclusive_lean_proved:80
---
# experiment:a00-0c148b16-60f4c5

PASS 8 RESIDUE round for hypothesis:lm-pi-context-hook-trim-keeps-one-prompt-loops-under-the-slot
(TMM.210). ONE touched code file:
`.agi/context/local-maxxing/pi/test_hook_trim_fixture_a00-faa1fb92.py` (184 added / 40 removed
lines by `git diff --numstat`; a TEST file, so production lines = 0, ceiling 70).
No model, no GPU, no pi, no subprocess, no git write. Nodes touched through
`bin/write.py` only: the hypothesis (THOUGHT gen 34) and experiment:a00-faa1fb92-350574 (THOUGHT).

## LEDGER — one row per PASS 8 item

| item | disposition | before -> after |
|---|---|---|
| 1 no-abort green-washed | FIXED (test :146) | `for f in ("aborted","abort","timed_out"): if f in arm: assert not arm[f]; return` -> an abort field (`aborted`/`abort`) is REQUIRED; no such field -> `pytest.xfail("the 'no abort' conjunct is UNMEASURED by this corpus")`; with a field, every present one must be false. 3 false greens -> 2 honest xfails |
| 2 evidence outside every suite | NOT FIXABLE IN SCOPE (structural, quantified) | no pytest.ini / pyproject.toml / setup.cfg / tox.ini exists in the repo; `SUITE_CMD = "tests"` (extensions/agi/bin/verification.py:78); the only conftests are extensions/agi/**. The fix is a suite cell (a root `pytest.ini` testpaths, or SUITE_CMD covering `.agi/context`) -- an ENGINE/root file this residue round may not touch. Handed up in the hypothesis THOUGHT |
| 3 near-tautology `assert "context" in text` | FIXED (test :206) | that assertion is replaced by a PARSE of the committed hook: `contextWindow ?? N` or `const LIMIT = N - M`, the reserve, the `/4` divisor, the `MARK` placeholder, and an oldest-first `for (const message of ...)` walk must all be present. This is the assertion whose absence let item 5 survive |
| 4 constants duplicated vs the claim | FIXED (drift closed, copy kept) | the file keeps its own literals (independence) and gains `test_claim_constants_still_match_the_node_testable_claim`, which reads the node's `testable_claim` and asserts 60,000 / 65,536 / 3.80 / 40 requests / request 20 are still stated there. A claim edit now fails the file instead of leaving it green. 43,616 = 60,000 - 16,384 is now derived in-file (`LIMIT = WINDOW - RESERVE`) and cross-checked against the JS |
| 5 divisor gap untested/undiscussed | FIXED (test :222, :231) | new `test_hook_limit_is_window_minus_reserve` (limit parsed = 43,616) and `test_hook_own_scale_stays_under_its_limit`: per with_extension row, `bytes / 4` -- an UPPER bound on the hook's own estimate, since the serialized request carries the messages plus schemas and framing -- must be < the parsed limit, AND the /3.80 scale is asserted to sit ABOVE it, so the gap cannot silently disappear |
| 6 the disqualified twin still runs green | FIXED (test :64, :170) | `TWIN_OF = {"a00-3c370e1e": "a00-cdde7530"}`, `INDEP_RUNS` drives the five claim tests (2 runs, not 3); `test_twin_run_is_excluded_from_the_independent_arms` asserts the twin differs from its source ONLY in `wall_seconds` and that `len(INDEP_RUNS) == 2`. Twin-of stays a stale-failing assertion if the logs ever diverge |
| 7 caveat one node away | FIXED (hypothesis THOUGHT gen 34) | the THOUGHT now states the abort conjunct is UNMEASURED, names the four measured conjuncts, and explains the lean. `testable_claim` and `verdict: inconclusive_lean_proved:80` are untouched -- a claim is never re-worded after its data |
| 8 UNVERIFIED probes | RAN (a); OUT OF SCOPE (b) | (a) `pytest .agi/context --collect-only -q` -> 127 tests collected, 18 modules ERROR at collection (the tree-wide gap of item 2, quantified). (b) a commit-path audit needs `git log -- <node>`, which a kid may not run; the frontmatter shape (`edited_by:`, THOUGHT block) is consistent with write.py but that is inference, not a record |
| 9 config_max literal path | FIXED (test :43) | `REPO = Path(__file__).resolve().parents[4]` + the literal `datasets/brain-swap/2026-09-24` -> `paths.get_local("brain_swap_out_dir")`, with `paths.py` found by `__file__` (sibling module). `get_local` is the right reader here: `box.root` is /home/ubuntu/work/agi while the checkout is /data/work/agi. The node file for item 4 is discovered via `os.path.dirname(paths.config_path())` -- no literal |

## Evidence

```
$ env -u TMUX PYTHONPATH=.agi/context/local-maxxing \
    python3 -m pytest .agi/context/local-maxxing/pi/test_hook_trim_fixture_a00-faa1fb92.py -q
31 passed, 3 xfailed in 0.08s
```
the 3 xfails: 2 x the abort conjunct (no `aborted`/`abort` field in any log) + 1 x
`a00-3c370e1e-context-trim.js` (artifact never committed).

The report table now carries the hook's OWN scale beside the claim's:

```
log            | arm               | n | max bytes/3.80 | first > 65536 | 400s | abort              | hook upper /4 < 43,616
a00-54d3d9b0   | with_extension    | 40| 45206.6        | -             | 0    | UNMEASURED         | 42946.2 True
a00-cdde7530   | with_extension    | 40| 44849.7        | -             | 0    | UNMEASURED         | 42607.2 True
a00-54d3d9b0   | without_extension | 20| 68521.3        | 11            | 2    | UNMEASURED         | -
a00-cdde7530   | without_extension | 22| 67510.3        | 12            | 2    | UNMEASURED         | -
```

What this does and does not move: the four MEASURED conjuncts (40 requests, no 400, slot
crossed at seq 11/12 without the hook, and now -- on the hook's own scale -- every trimmed
request under the 43,616 the hook actually gates on) hold on BOTH independent logs. The
fifth, "no abort", is unmeasured and stays unmeasured: no log in the corpus records an abort
field. So the line stays a lean, not a proof. What would make it `proved`: a live re-run of
both arms (WAITS-FOR-MODEL -- forbidden this round) plus an abort field actually recorded in
the log. What would make it `disproved`: any with_extension row at/over 43,616 tokens on the
/4 scale, a 400, or the loop ending before 40 requests.

## Struggles

- The two committed hooks have DIFFERENT SOURCE SHAPES (`(usage?.contextWindow ?? N) - M` +
  `ctx.getSystemUsage` vs `const LIMIT = N - M`), so every mechanism parse needs two
  fallbacks or it silently reads None and the assertion dies in an arithmetic TypeError.
- `paths.checkout_root()` returns the CHECKOUT, not the `.agi` dir -- one level off from what
  the name suggests; the node path needs `os.path.dirname(paths.config_path())`.

## Agent Notes
PASS 8 residue round: 7 of 9 items fixed in the fixture (abort conjunct now xfails, hook-own scale bytes/4<43,616 parsed from the committed JS, twin run excluded, claim constants cross-checked, log dir read via paths.get_local); item 2 is a tree-wide suite gap outside file scope, item 8b needs git a kid may not run; 31 passed 3 xfailed; claim text and verdict untouched; rebrief filed on the test-line count

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
"PARENT REVIEW gen 35 (a00-27cbb7ca, iteration 49). ACCEPTED on the BYTES, not on the ledger. (1) WHAT THE ORDERS SAID: correct the 9 PASS 8 items IN PLACE, in the fixture file each item names. (2) WHAT THE MACHINE DOES: I did not re-run the kid suite as evidence -- I imported the committed module and handed each test a state the claim says must be refused. Every refusable state goes RED: aborted=True and abort=\"context trim\" (test:187-195), a with_extension row inflated to 200000 B (upper bound 50000.0 vs the parsed limit 43616), the hook reserve 16384->4096 in a copy of the committed JS, the divisor 4->2, the walk reversed newest-first, without_extension truncated to 10 rows, 400s=[20], a non-monotonic elide count, an all-zero elide count, a hypothesis copy stripped of its constants, a twin diverging by one byte. Every CONTROL stays green (restored JS, real node, restored twin), which is what makes the reds mean something. WIRE: LOG_DIR aimed at a missing directory raises FileNotFoundError, so the suite reads the committed logs rather than a constant. (3) THE NEAR MISS THIS ROUND AVOIDED: item 1 could have been closed by renaming the fall-through -- keeping the timed_out branch and calling the conjunct PARTIAL in prose -- which satisfies the words and keeps the conjunct untestable. The bytes instead REQUIRE an aborted/abort field and xfail without one, so the green count fell 31/1 to 31/3 and the hypothesis THOUGHT gen 34 now says UNMEASURED on the node a future round is handed. I ran that same probe BEFORE the kid: on the pre-kid file an abort recorded as stop_reason=aborted went GREEN, which is the falsifying case the item named, and the new file no longer has that hole. (4) DEVIATION: I did not run git, so the kid DIFF was reviewed as the committed working-tree file plus the parse-level probes, which is the same evidence for a change confined to one file; item 8b (the write.py commit-path audit) therefore stays UNVERIFIED, and the kid marked it that way rather than inferring a record it did not have. Items 2 and 8b are correctly hand-upped: item 2 needs a root pytest.ini testpaths or the SUITE_CMD cell in extensions/agi/bin/verification.py:78, both outside a residue round scoped to one fixture. The 184/40 line count is a TEST file and production_lines=0, which is the same reading gen 33 already accepted for a00-faa1fb92 -- the re-brief is answered proceed-with-ceiling-70, and the round needs no resumption."
<!-- THOUGHT:END -->

"ACCEPTED (lean_proved:80 kept). 7 of 9 PASS 8 items fixed in the fixture and hold under 13 parent probes; items 2 and 8b hand-upped as out-of-scope by the orders own rules. Re-brief answered in-node: proceed with ceiling 70, test lines excluded. Verdict unchanged -- four conjuncts measured, no abort conjunct UNMEASURED."
