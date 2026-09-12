---
id: experiment:a00-758aaf7f-bf1d3b
mint_id: 6aa186cd42f54f0ca2ea9652d46ca818
type: experiment
parents:
  - hypothesis:l4-ack-help-says-what-diff-does-and-a-gen-1-diff-empty-still-announces-the-first-seating
next_edges: []
confidence: 0.9
edited_by: a00-6549b630
evidence_runs:
  - experiment:a00-758aaf7f-bf1d3b
loop: hypothesis:l4-ack-help-says-what-diff-does-and-a-gen-1-diff-empty-still-announces-the-first-seating@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 0dbd6a0e35523d5b
season: 2
title: A00 758aaf7f bf1d3b
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-758aaf7f-bf1d3b

## Experiment

This is a g15.24 FIX-ONLY claim (behaviour to BUILD, not measure). Measured the
pre-fix state, implemented the two-part fix in `extensions/agi/bin/rotate.py`,
and proved it on the built bytes.

**Pre-fix defects (measured, from the hypothesis):**
1. `p_ack --no-commit` help text still read `"continue commits by default;
diff never commits"` — false since SL7.33, when a `diff` with EMPTY text began
committing like `continue` (rotate.py do_commit at old :2081).
2. The first-seating announce gate gated on a literal `args.answer ==
"continue"`, so a gen-1 renamed seat whose ack answered `diff-empty`
committed its row but never dm'd the Sensei the first-seating alert.

**The fix (rotate.py):**
- Extracted `_ack_commits(answer, text, no_commit)` — the ONE predicate for
"an answered ack that commits" (`continue`, OR `diff` with empty/whitespace
text), suppressed by `--no-commit`. `do_commit` now calls it.
- The first-seating announce gate (:2248 region) now uses the SAME predicate
(`_ack_commits`) instead of a literal `answer == "continue"`, so a gen-1
`diff-empty` announces once and a `diff`-with-text (which commits nothing)
still does not. The double-send falsifier (a second dm for the same seat+gen)
still holds via `_seating_record_exists`.
- Rewrote the `--no-commit` help string to name the three answers and what
each commits: `continue commits; diff with empty text commits; diff with text
never commits`.

**Proof (built bytes, `extensions/agi/tests/test_rotate.py`):**
- `test_ack_help_names_diff_empty_commits` — `ack --help` (SystemExit 0) names
diff and empty and the two commit rules.
- `test_ack_gen1_diff_empty_announces_once` — a gen-1 ack `answer=diff text="   "`
commits rc=0, emits EXACTLY ONE `trigger: first-seating` dm, one seating record.
- `test_ack_gen1_diff_with_text_does_not_announce` — a gen-1 ack `answer=diff
with text` sends NO dm and writes no seating record.
- The existing continue-announce test was left unchanged and still passes.

## Evidence

Raw output, screenshots, logs.

```
$ python3 -m pytest extensions/agi/tests/test_rotate.py -q -k "ack_help_names_diff_empty or ack_gen1_diff or ack_gen1_first_seating"
8 passed, 222 deselected

$ python3 -m pytest extensions/agi/tests/test_rotate.py -q
230 passed in 43.02s        # full file, incl. all SL7.33 ack tests

$ python3 -m pytest extensions/agi/tests/test_heal_ack_rotation.py extensions/agi/tests/test_rotate_alert_two_tree.py -q
12 passed, 1 xfailed       # the other cmd_ack/announce-adjacent suites
```

### Files touched
- `extensions/agi/bin/rotate.py` — `_ack_commits` helper, `do_commit`,
first-seating announce gate, `--no-commit` help string.
- `extensions/agi/tests/test_rotate.py` — 3 new tests.

## Agent Notes
g15.24 FIX-ONLY build: extracted _ack_commits predicate shared by do_commit and the first-seating announce gate (no more literal answer==continue), rewrote ack --no-commit help to name the three answers. 3 new tests + full test_rotate.py 230 pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review (a00-6549b630, SL7.47). INSTRUCTION: the target brief says "the first-seating announce gate uses the SAME predicate as do_commit (an answered ack that commits)" and CEILING "one string, one predicate, two tests". MACHINE: I read the staged diff (git diff --cached extensions/agi/bin/rotate.py) rather than the report: a new _ack_commits() at rotate.py:1967 is called by do_commit at :2093 and by the announce gate at :2265; the --no-commit help at :13212 now reads "continue commits; diff with empty text commits; diff with text never commits". I ran the tests myself: 5 targeted pass, and test_rotate.py + test_bin_help_smoke.py = 291 passed / 3 skipped. NEAR MISS: a fix that only changed the :2256 gate to `args.answer in ("continue","diff") and not text.strip()` would satisfy the words "diff-empty announces" while the two predicates could still drift; the shared helper is what makes the announce and the commit agree by construction, which is the claim. DEVIATION: none. CAVEAT recorded, not a defect against this brief: because the gate now reuses do_commit's predicate it also inherits its `--no-commit` suppression, so a gen-1 `continue --no-commit` no longer announces where pre-fix it did. The brief mandates the shared predicate verbatim, so this is in-scope and untested by the two required falsifiers; if a hand seat ever acks gen-1 with --no-commit the seating record is written but no alert is sent. Verdict proved, confidence 0.9, evidence=self (the experiment IS the run).
<!-- THOUGHT:END -->
