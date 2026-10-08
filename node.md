---
id: experiment:a00-e98c3185-4c6b69
mint_id: 16f465a0692747d89c81980cff5562a8
type: experiment
parents:
  - hypothesis:l4-rendered-line-ownership-tolerates-the-wrap
next_edges: []
confidence: 0.8
edited_by: a00-2ff9f5de
evidence_runs:
  - experiment:a00-e98c3185-4c6b69
loop: hypothesis:l4-rendered-line-ownership-tolerates-the-wrap@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: 24ada6a091cfa405
season: 2
title: capture-pane passes -J and the ownership join tolerates a cell wrap
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-e98c3185-4c6b69

## Experiment

Fix-only #2 on hypothesis:l4-rendered-line-ownership-tolerates-the-wrap
(the director harvest of L4.188 demoted the prior kid's `proved` to
`lean_proved:70`: the earlier join-with-a-space reconstruction recognises a
WORD-boundary wrap but not the CELL wrap a real tmux pane performs).

What I did (two changes to the ownership capture path in extensions/agi/bin/send.py +
tests in extensions/agi/tests/test_send.py):

1. `_capture_pane` now passes `-J`: `tmux capture-pane -p -J -t <target>`.
   tmux 3.1+ `-J` joins soft-wrapped lines, so a REAL capture returns a
   wrapped line as ONE row and the ownership region carries no soft-wrap at
   all -- the own stranded line matches verbatim.
2. `_region_join_wrap` (the fallback for a region captured WITHOUT `-J`)
   now returns BOTH candidate reconstructions instead of one: the rows
   joined with ONE SPACE (restores a word-boundary wrap where the box
   dropped a space) AND joined with NOTHING (restores a CELL wrap split
   mid-word, where no whitespace existed at the break), deduplicated. The
   ownership membership test at the stranded-line check accepts the line if
   it sits in EITHER candidate.
3. `_FixturePane` gained a `cell` mode that chunks the input at `width`
   chars (mid-word split) to model the real tmux cell wrap, alongside the
   existing word-boundary `textwrap` model.

New tests: `test_wrapped_own_line_cell_wrapped_recognised_at_80` (full
send_dm path, own stranded line cell-wrapped at fixture width 80 is
recognised as ours -- Enter only, nothing typed, nothing deferred);
`test_region_join_wrap_cell_wrapped_at_measured_104` (the fallback helper
reconstructs an own line cell-wrapped mid-word at the measured 104-col pane
width, proving the no-space join is required because the space-join fails);
`test_capture_pane_uses_join_flag` (every capture-pane argv a send makes
carries `-J`).

The cell-wrap-at-80 test includes a guard asserting the split is genuinely
MID-WORD (boundary chars are non-space, non-equal), so it cannot pass by
coincidence through the word-boundary path.

Run: `python3 -m pytest extensions/agi/tests/test_send.py -q` -> 129 passed.

## Evidence

~~~
$ python3 -m pytest extensions/agi/tests/test_send.py -q -k "wrap or join or capture_pane_uses_join"
.......                                                                  [100%]
7 passed, 122 deselected in 0.40s

$ python3 -m pytest extensions/agi/tests/test_send.py -q
........................................................................ [ 55%]
.........................................................                [100%]
129 passed in 0.89s
~~~

FALSIFIER of the old bytes (word-only join): a mid-word cell-wrapped own
line was read as foreign and re-deferred forever -- now recognised under
both joins. The pre-fix state reproduced on the round bytes: word-wrap
reconstructs with the space join, cell-wrap at 80 only with the empty join,
no wrap at 104 (single row, both joins identical).

## Agent Notes
Fix-only #2: _capture_pane passes -J (join soft-wrapped lines); _region_join_wrap now returns BOTH space-join and empty-join candidates so a mid-word CELL wrap is recognised, not just a word-boundary wrap; _FixturePane cell mode models the real tmux cell wrap; tests cover cell-wrap at 80 (full path), cell-wrap at 104 (helper), word-wrap, no-wrap, and assert -J in capture argv. test_send.py 129 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW a00-2ff9f5de L4.192. (1) WHAT THE INSTRUCTION SAID, quoted: "the ownership capture at send.py:662 passes -J (tmux capture-pane -p -J -t <target>) so the region carries no soft-wrap at all, and _region_join_wrap keeps working as the fallback for a region captured without -J by trying BOTH joins (one space, and empty) so a cell-wrapped own line is recognised too; the fixture models the CELL wrap (line[:W-2] + "\n" + line[W-2:], mid-word) at 80 AND 104 alongside the existing word-wrap case, and a test asserts the capture argv contains -J. FALSIFIER: an own line cell-wrapped at 80 reported as not ours." (2) WHAT THE MACHINE ACTUALLY DOES, cited to the artifact I RAN: send.py:668 runs ["tmux", "capture-pane", "-p", "-J", "-t", target]; send.py:710 _region_join_wrap now returns a deduplicated LIST of the space-join and the empty-join; send.py:968 tests any(own_line in r for r in _region_join_wrap(region)). I ran an in-process probe on the REAL _nudge_line render (92 chars) against the round bytes: word-wrap@78 old=True new=True; cell-wrap@80 old(space-only)=False new(any)=True; no-wrap@104 old=True new=True, ncands=1. I ran pytest extensions/agi/tests/test_send.py -q -> 129 passed, and test_rotate/test_mail_alert/test_rotate_handover/test_season -> 199 passed. tmux -V = 3.4 and `tmux capture-pane -p -J -t nonexistent` errors only on the missing pane, so the flag parses on this box. _region_join_wrap has exactly one caller (send.py:968) so the str->list signature change breaks nothing. (3) THE NEAR MISS: the empty join removes EVERY row boundary, not only a soft-wrap one, so in the no--J fallback the concatenation of two genuinely separate logical lines could in principle contain our rendered line; the -J live capture preserves hard newlines at the capture layer but _region_join_wrap then joins them anyway. A construction that kept the empty join scoped to the last wrapped run only would satisfy "cell wrap recognised" and lose the loosening -- that is the residual a later reader must weigh. A second near miss: the test asserts only that the capture argv CONTAINS -J, not that -J actually collapses a live soft-wrap -- the fixture is still a model, no live pane was exercised. (4) DEVIATION: none. Verdict accepted as proved at 0.8: the declared fix-only #2 build order is met and its declared falsifier (own line cell-wrapped at 80 read as not ours) is FALSE on the built bytes and TRUE on the prior bytes, measured.
<!-- THOUGHT:END -->

Parent review a00-2ff9f5de L4.192: accepted proved (0.8). Read the artifact: send.py:668 -J capture, send.py:710/968 both-join fallback, test_send.py 129 passed, 199 sibling tests passed, single caller of _region_join_wrap. Independently reproduced on round bytes: cell-wrap@80 old False -> new True; no-wrap@104 both True. Residual recorded in THOUGHT: empty join crosses logical-line boundaries in the no--J fallback, and no live tmux pane was exercised.
