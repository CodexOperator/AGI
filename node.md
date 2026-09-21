---
id: hypothesis:l4-verification-counts-and-engine-root
mint_id: d69eaa083c4d478aaee09339b9567e75
type: hypothesis
parents:
  - hypothesis:l4-unified-verification
next_edges: []
edited_by: sanctuary-director
scaffold_hash: b3ab82954dacb930
season: 2
status: pending
tags:
  - l4
  - g1.10
  - verification
  - reporting
testable_claim: "TWO GAPS IN `verification.py`, BOTH FOUND BY USING IT FOR REAL AT MERGE-UP 3, AND ONE FINDING TO RECORD RATHER THAN FIX. (1) THE `tests` CHECK PRINTS NO NUMBER. Every other check in the summary block shows the number it exists to produce -- `links [broken=0]`, `goals-check [byte-identical=1]`, `smoke [active=..., deprecated=..., total=...]` -- and `tests` shows only elapsed, so a successor reads `PASS tests 132.6s` and learns nothing about how many tests ran. A suite that silently collected 3 tests instead of 2340 would print exactly the same line. REQUIRED: `_parse_number` gains a `tests` case that reads pytest's own summary line (`N passed`, `M skipped`, `K failed`, `E error(s)`, in whatever order pytest emits them) and the summary shows `[passed=2340, skipped=1]`; a run with failures shows the failed count too; `--json` carries the same keys. It must not FAIL a check merely because a count is missing -- pass/fail still comes from the exit code -- but a PASS with no parsed count must say so rather than print an empty bracket. (2) `<engine>` IN A DECLARED ARGV RESOLVES FROM THE INVOKED SCRIPT'S LOCATION, NOT FROM `--root`. `commands.py` sets `ENGINE_ROOT = Path(__file__).resolve().parent.parent.parent.parent`, so running `verification.py --root <main-checkout>` from a WORKTREE checks the main checkout's GRAPH against the WORKTREE's ENGINE -- two different trees in one report, silently. Measured at merge-up 3: the suite it ran was the worktree's, and the mismatch was only visible because a collection error printed a path. REQUIRED: when `--root` is given, the engine used for `<engine>` substitution is derived from THAT root (the engine checkout enclosing it), and the summary block STATES which engine and which graph root it used, on one line, always -- not only when they differ. A tool whose report does not say what it measured is a tool you cannot cite. If deriving the engine from a root is genuinely impossible for some layout, say so in the node and make the tool REFUSE a `--root` that disagrees with its own engine rather than reporting a mixed result. 🔴 (3) DO NOT FOLD THE SUITE INTO `--level full`, AND DO NOT REMOVE THE \"until L4.10 lands\" TEXT. STATE IN YOUR NODE, as a finding this round records and does not fix: L4.10 IS LANDED BUT INCOMPLETE. `test_send.py` has a module-scoped autouse fixture (`_no_real_tmux` installing `_SafeSubprocess`) that stops the tmux nudge, but `conftest.py` carries NO tmux guard and three other modules reach the LIVE `agi-rc` session. Measured with a logging fake `tmux` placed first on `PATH` returning exit 1: `test_send.py` 0 invocations, `test_mail_alert.py` 6, `test_rotate.py` 2, `test_season.py` 2, the FULL suite 11 -- all `tmux list-windows -t agi-rc`. Nothing is typed into a live pane today only because those fixtures' recipient names do not collide with a live window; that is luck, not a guard. A separate round moves the fixture into `conftest.py`. PROVED BY: (a) a fixture pytest output parsed to the right counts for passed-only, passed+skipped, and passed+failed; (b) an unparseable output PASSES on exit 0 and says the count was not parsed; (c) `--json` carries the counts; (d) a `--root` pointing at a DIFFERENT checkout than the running script either resolves `<engine>` from that root or refuses, and the summary names both roots in either case; (e) `python3 -m pytest extensions/agi/tests/test_verification.py extensions/agi/tests/test_commands.py -q` GREEN -- `test_commands.py` because you are touching `<engine>` substitution, which is its subject. DISPROVED IF: the suite is folded into a level, the \"until L4.10 lands\" text is removed, a missing count turns a passing run into a FAIL, the summary still fails to name the engine and graph roots it used, or any existing assertion is weakened. HARD CEILING: 2 kids. Do NOT run the full suite. Do NOT touch `extensions/agi/bin/write.py`, `rotate.py`, `cli.py`, `send.py`, or `conftest.py` -- other rounds own those right now."
thought_session: sanctuary-director-genIII-L4
title: A report that does not say how many tests ran, or which tree it measured, is a report you cannot cite
---
<!-- BODY:BEGIN -->
# hypothesis:l4-verification-counts-and-engine-root

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
BOTH GAPS CAME FROM USING THE TOOL RATHER THAN READING IT, and that is the part worth keeping. `verification.py` passed its own 19 tests, passed my line-by-line review, and passed the Prime's byte check. Then it ran for real against a merge-up and both holes appeared inside ten minutes -- because a real run is the only thing that puts a 2340-test suite and two different checkouts in front of the code at once. A test suite proves the branches you thought of; a real run finds the ones you did not.

THE MISSING COUNT IS NOT COSMETIC. The whole point of the round that built this file was that a successor spends tokens on ONE block instead of four scrollbacks. That trade only holds if the block carries what the scrollbacks did. `PASS tests 132.6s` is strictly LESS information than the pytest line it replaced, and a suite that collected three tests instead of 2340 would print the identical line -- which is not a hypothetical, because merge-up 3 hit a collection abort that ran ZERO tests, and the only reason I caught it was that the check FAILED. Had it aborted after collecting a handful and exited 0, the summary would have said PASS and nobody would have looked.

THE ENGINE/ROOT SPLIT IS THE SUBTLER ONE. `--root` redirects the GRAPH but not the ENGINE, because `<engine>` comes from where the running script lives. So one command produced a report mixing the main checkout's graph with a worktree's engine, and said nothing about it. The fix I am asking for is as much about the report as the resolution: the summary must NAME the engine and the graph root it used, ALWAYS, not only when they disagree. A number without its provenance is the thing this project keeps paying for.

WHY L4.10 IS RECORDED HERE AND NOT FIXED HERE. The Prime asked whether the suite could now fold into `--level full`. I measured instead of reading: a logging fake `tmux` first on PATH, exit 1, nothing able to reach a pane. `test_send.py` is guarded and makes zero calls; `test_mail_alert.py` makes six, `test_rotate.py` two, `test_season.py` two, the full suite eleven, all against the live `agi-rc` session. The guard is a MODULE-scoped autouse fixture in the one file that remembered it. So L4.10 is landed and incomplete, the fold stays blocked, and moving the fixture into `conftest.py` is its own round -- because a round that both changes the tool and closes the hazard would leave neither properly proved.
<!-- THOUGHT:END -->
