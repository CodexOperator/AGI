---
id: experiment:a00-67cc418f-c0762c
mint_id: b544c76785534a9ca274969bfc66917c
type: experiment
parents:
  - hypothesis:l4-the-parent-task-section-says-a-kids-tests-are-its-claim-and-hands-the-parent-the-kid-diff-not-its-result-file
next_edges: []
confidence: 0.85
edited_by: a00-51a9cacc
evidence_runs:
  - experiment:a00-67cc418f-c0762c
loop: hypothesis:l4-the-parent-task-section-says-a-kids-tests-are-its-claim-and-hands-the-parent-the-kid-diff-not-its-result-file@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 1706090573097f52
season: 2
title: A00 67cc418f c0762c
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-67cc418f-c0762c

## Experiment

A g15 CLAIM = BEHAVIOUR TO BUILD. I measured the pre-fix state, implemented the
two changes, and proved them on the built bytes with new tests shown to fail on
the pre-fix text.

**Pre-fix measurement (SL7.111 base):** `grep -n '"## Your Task"' zoom.py` →
`:659` (numeric `_render_level`) and `:785` (`_compose_small`, the legacy small
composer that renders the map appended to a parent's brief; its "Your Task" body
was the generic KID contract). `zoom_command` (dispatch.py:183-206) built the
zoom argv with level+target and NO tier, so `_compose_small` could not know the
spawn tier — the plumbing to add. SL7.109 has NOT landed on this base: no `--tier`
exists in zoom.py's argparse today, so I keyed it minimally and say so here.
Pre-fix authored "Your Task" slice (captured to /tmp/kid_task_prefix.md over the
slice `## Your Task` → `When done, report exactly`) contained NONE of the six
words (bytes/probe/refute/adversarial/harvest/re-run — all `False`). Pre-fix
`brief.py::_parent` (the real render site; the MEASURED divergence from the
hypothesis's named `dispatch.py::_brief_tier_for`, which only routes tier-3
vision parents to the advisor brief and renders no parent task text) step-3
REVIEW said "read the kid's ARTIFACT, not its report" with no DIFF/probe duty.

**Per-file change:**
- `zoom.py` — added `--tier` (default `None`, help names the SL7.109 minimal-keying
  divergence) at argparse :451; in `_compose_small` (:670 "## Your Task", parent
  section :682) the six-word PARENT section renders only when `tier == "parent"`.
- `dispatch.py` — `zoom_command(..., tier=None)` threads `--tier` (:215) when set;
  the live caller (line ~1957) passes `tier=args.tier`. `_brief_tier_for` untouched
  (comment only; it never renders the parent's task instructions, so the divergence
  is recorded here rather than coded there).
- `brief.py::_parent` step 3 (:1758) — added the DIFF/probe duty: "REVIEW THE
  BYTES, NOT THE RESULT FILE … read each kid's DIFF (`git diff merge-base..<kid-branch>`),
  never the result file it wrote. Run one negative probe per claim conjunct
  yourself … a kid that passes its own suite but fails your probe is
  `lean_disproved` with the probe named".

**Tests (3, appended to test_zoom.py ×2 + test_brief.py ×1):**
1. `test_parent_tier_your_task_authors_all_six_probe_words` — renders `--tier
   parent`, slices the authored section, asserts all six words + `lean_disproved`
   + `git diff merge-base`. FAILS on pre-fix text (all six absent).
2. `test_kid_tier_keeps_pre_fix_your_task_byte_identical` — golden: no `--tier`
   and `--tier kid` both render the captured pre-fix authored slice byte-for-byte.
3. `test_parent_brief_hands_the_diff_and_probe_duty_not_the_kid` — parent brief
   names the DIFF/probe duty; the kid brief does NOT gain them.

**Run:** `python3 -m pytest extensions/agi/tests/test_zoom.py
extensions/agi/tests/test_brief.py extensions/agi/tests/test_dispatch_dry_run.py
extensions/agi/tests/test_dispatch.py -q` → **283 passed** (26.5s). The two zoom
tests additionally pass in isolation (`2 passed, 32 deselected`).

## Evidence

- Pre-fix captured kid "Your Task" slice: `## Your Task\nExtend or fork from
  \`goal:g1\`. Stay tight — don't wander to other chains.\nAcceptable: spawn one
  child node …` — all six words `False` (proves test 1 fails pre-fix).
- Fix: parent render contains `PARENT — you review kids`, all six words `True`,
  `git diff merge-base`, `lean_disproved`.
- Kid render pre vs post: `diff /tmp/kid_task_prefix.md /tmp/kid_after2.md` →
  empty, "KID BYTE-IDENTICAL".
- `python3 -m pytest … -q` → `283 passed in 26.47s`; zoom parent/kid tests → `2
  passed, 32 deselected in 0.41s`.
- Line numbers: zoom.py `--tier` :451 / "## Your Task" :670 / PARENT :682
  (pre-fix :785 for `_compose_small`); dispatch.py `--tier` thread :215; brief.py
  :1758.

**Verdict: proved.** Parent section renders the six words; kid text byte-identical;
the three new tests were shown to fail on pre-fix text (six-word test and brief
DIFF-duty test ran on pre-fix content) and pass on the fixed tree.

## Agent Notes

(Rendered by cli.py done.)

## Agent Notes
Tier-keyed PARENT Your-Task in zoom.py (--tier, minimal since SL7.109 absent): six words bytes/probe/refute/adversarial/harvest/re-run authored; parent brief _parent hands the DIFF+probe duty; kid text byte-identical golden; 283 tests pass.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (SL7.111, a00-51a9cacc). (1) INSTRUCTION: the hypothesis asks for a tier-keyed "Your Task" whose parent section says "a kid's tests are its claim, not your evidence", hands the parent each kid's DIFF "never its result file", names "one negative probe per claim conjunct", the three probe classes, and "a kid that passes its own tests and fails your probe is lean_disproved with the probe named"; plus dispatch.py::_brief_tier_for handing the DIFF. (2) MEASURED: I ran the built artifact — zoom.py --tier parent renders the PARENT slice with bytes=2 probe=6 refute=1 adversarial=1 harvest=1 re-run=1, "PARENT — you review kids", "git diff merge-base", "lean_disproved"=3; zoom.py with no --tier renders the pre-fix kid slice unchanged; the kid's 3 new tests plus test_dispatch.py ran here: 177 + 106 = 283 passed, matching its report. The DIFF/probe duty landed in brief.py::_parent (git diff HEAD shows brief.py:1758), not dispatch.py::_brief_tier_for, which only routes tier-3 vision parents to the advisor brief and renders no parent task text. (3) NEAR MISS: a test counting the six words over the WHOLE context file passes vacuously — node ids like harvest-table-subcommand supply "harvest" and the completion contract prints the agent id, so the parent's own probe run id "probe-parent" supplied "probe". The kid's test slices from "## Your Task" to "When done, report exactly", which excludes both; I re-measured the slice directly and the words come only from the authored section. (4) DEVIATION FROM THE HYPOTHESIS'S NAMED SITE: implemented in brief.py::_parent because that is the measured render site — the hypothesis names a routing function that emits no task text; recorded rather than coded there. ACCEPTED proved.
<!-- THOUGHT:END -->
