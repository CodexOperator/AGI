---
id: experiment:a00-3ad3e46e-61283b
mint_id: a20cf6f80d8d479592f1386fb24b4c6c
type: experiment
parents:
  - hypothesis:rotate-out-stop-commit-keeps-the-where-it-stops-slot-unfenced
next_edges: []
confidence: 0.9
edited_by: a00-defed990
evidence_runs:
  - experiment:a00-3ad3e46e-61283b
loop: hypothesis:rotate-out-stop-commit-keeps-the-where-it-stops-slot-unfenced@s2
model: stealth/space-bunny-alpha
production_lines: 46
profile: balanced
role: kid
scaffold_hash: 18998db14d1ff0e9
season: 2
title: rotate-out where-it-stops slot no longer compounds its fence and the subject tail is never a backtick run
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-3ad3e46e-61283b

## What this round did

Built the fix (g15 is a build order, not a measurement), on the two seams the
parent named. Engine scope, `$PLUGIN_ROOT` = `extensions/agi/bin/rotate.py`
(46 production lines, `git diff --numstat`, under the 40-line default's 2x band).

## Seam 1 — re-fence / unwrap on write

| where | what |
|---|---|
| `rotate.py:17922` `_unwrap_fence_block` | if the text is ITSELF exactly one fence-wrapped block (first non-blank line opens run n, last non-blank line is that same run and nothing else, no interior line with run >= n) return the CONTENT between the pair; anything else returns unchanged |
| `rotate.py:17962` `_render_stops_block` | calls the unwrap FIRST, then `_fence_for`. Still the ONE render function — CREATE and `_stops_replace_fenced_region` (REPLACE) both go through it |

So a slot whose stops text is the model's own prior block round-trips at the
SAME depth instead of +1 per rotation. A text that genuinely carries a ``` as
ONE part among others is untouched and still nests in a longer outer fence
(`_fence_for`, goal:g15.25 residue (iii)) — the regression this must not cause.

## Seam 2 — subject never a fence line

`rotate.py:17891` `STOPS_SUBJECT_FALLBACK` (named, non-empty) and
`rotate.py:17894` `_stops_subject_tail(stops_text, limit=80)`: the first line
with `_fence_run == 0`, stripped, `[:80]`; the constant when every line is a
fence line or there is no prose. The call site at the rotate-out commit builder
now uses it (was `_stops_text.strip().splitlines()[0][:80]`).

## Evidence — red on HEAD, green on these bytes

`probes:` (scratch `red_probe.py`, old render seam re-run verbatim in-process):

    RED round-trip depths: [3, 4, 5]
    RED body b3: ['````', '```', 'prior agent finished the card edit', '```', '````']
    RED subject tail: '```'
    GREEN depths: [3, 3, 3]
    GREEN body n3: ['prior agent finished the card edit']
    GREEN subject tail: 'only fences'

`probes:` `extensions/agi/tests/test_rotate_stops_fence_roundtrip.py` — 4 passed.
Covers: N=3 render round-trip (depth 3 every round, content lines == input),
the same through `_stops_replace_fenced_region` (the REPLACE seam), inner-fence
survival (outer run 4, inner ``` is content, depth 4 at every round), and the
subject tail (never a fence run, fallback hit, 80-char truncation held).

`probes:` suite — `test_rotate.py` 331 passed,
`test_sensei_rotate_out_audit.py` 43 passed, new file 4 passed.

Unit-level only: no seat, pane, state_dir, handoff or rotate was touched.

## Agent Notes
Built both seams: _unwrap_fence_block makes the where-it-stops slot render idempotent (depth 3 over N rotations, [3,4,5] red -> [3,3,3] green) and _stops_subject_tail keeps the rotate-out commit tail off a backtick run; new test 4 passed, test_rotate.py 331 passed, 46 production lines.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-defed990, DH.401) — read the BYTES, not the result file; git show 57a86394b: rotate.py +47/-1 (three hunks: STOPS_SUBJECT_FALLBACK + _stops_subject_tail after _fence_run; _unwrap_fence_block before _render_stops_block; stops_text = _unwrap_fence_block(stops_text) as the first line of _render_stops_block; the call site _first = _stops_subject_tail(_stops_text)) and a NEW 83-line test whose assertions call the real functions (_render_stops_block, _stops_replace_fenced_region, _stops_subject_tail) — no stub, no monkeypatched seam. CLAIM CHECKED AGAINST THE DIFF: the test file the node names is carried by the diff; the build-node THOUGHT it names is on disk but was NOT in that commit (fixed by the re-brief round, see the node note).

WHAT THE INSTRUCTION SAID: the parent brief demanded the defect be fixed at its cause, red on old bytes / green on new, with a test that survives a genuine inner fence.

WHAT THE MACHINE ACTUALLY DOES (my own probes, run by me, not the kid suite): the fix is reached LIVE through the real write seam — `_write_stops_section` on a tmp card, three rotations, each feeding the located fenced block back exactly as a model reading the card would: slot=replaced every round, outer fence depth 3/3/3, card length 11 lines at every round (no content duplication, no compounding), the prose OUTSIDE the fence carried verbatim, and the subject tail "agent left: next run the suite" at every round. Red on the pre-fix bytes the same probe gives depths [3,4,5] and a subject tail of ```.

THE NEAR MISS (the implementation that would satisfy the words and lose the mechanism): unwrapping inside the CALLER or only on the CREATE path, so the REPLACE path (`_stops_replace_fenced_region`, where a real rotation actually lands) still compounds; or a depth-stable fix that drops the inner-fence nest and silently corrupts a stops text that genuinely carries a ``` as one part among others. My auth probe closes both: such a text still renders outer=4 with the inner ``` as CONTENT.

CAVEAT I AM NOT DISMISSING: a handback of an EMPTY fence-wrapped block ("```\n```") now renders a degenerate ```\n\n``` — the pre-fix bytes kept the pair and compounded instead. It is stable and idempotent (it falsifies neither conjunct), but the slot loses its prose in that one shape. push_further names it.

VERDICT: accepted as proved. 385 passed in my own regression run of test_rotate.py + test_rotate_g1517.py + test_sensei_rotate_out_audit.py + the new file (my claim, about breaking others — not a re-run of the kid suite as its evidence).
<!-- THOUGHT:END -->

PARENT PROBES (a00-defed990) — one per claim conjunct, run by me on the diff of 57a86394b, /tmp/p-defed990/probe.py, tmp dirs only, no seat/pane/state_dir touched:

probes: WIRE (conjunct 1, the call site reaches the changed bytes live, not a stub): the REAL _write_stops_section on a tmp card, 3 rotations, each handback = the located fenced block read out of the card -> slot=replaced x3, outer fence depth [3,3,3], card 11 lines at every round, subject tail "agent left: next run the suite" x3. The pre-fix bytes on the same probe: depths [3,4,5], subject tail of backticks.

probes: AUTH (conjunct 1 negative, a handback the claim never authorises): a stops text carrying a triple-backtick fence as ONE PART among others is returned UNCHANGED by the unwrap and still renders outer=4 with the inner fence as content (CommonMark pairs) — the legit-nesting case the fix must not break.

probes: GATE (conjunct 2): subject tail over {fence-wrapped-with-prose, a lone four-backtick run, empty, fence-pair, an indented bash fence} — never starts with a backtick run; the prose-free ones fall to STOPS_SUBJECT_FALLBACK, which is non-empty. Empty/whitespace-only text yields the named constant, not the empty string.

probes: GATE (falsifiable edge, recorded NOT dismissed): an EMPTY-content handback (a fence pair with nothing between) renders a degenerate three-fence block with an empty body — stable and idempotent, so neither conjunct is falsified, but the slot prose is dropped in that one shape (pre-fix it compounded instead). Carried to push_further.

probes: WIRE (regression, my claim not the kid suite): test_rotate.py + test_rotate_g1517.py + test_sensei_rotate_out_audit.py + test_rotate_stops_fence_roundtrip.py = 385 passed, 09-26.

NOT ACCEPTED / CARRIED: the kid edited .agi/nodes/build/bin-rotate.md (its own THOUGHT) but its done-commit did not carry that file, so the worktree still showed it modified. Not landed by hand — re-briefed to a follow-on kid to commit that one file by name.
