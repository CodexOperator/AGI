---
id: experiment:a00-a238ee0a-cab2a6
mint_id: d36cb03af20b4f658352df3d30b9eefb
type: experiment
parents:
  - hypothesis:g1-inbox-read-cursor-never-passes-an-unprinted-line
next_edges: []
confidence: 0.9
edited_by: a00-d311e8c8
evidence_runs:
  - experiment:a00-a238ee0a-cab2a6
loop: hypothesis:g1-inbox-read-cursor-never-passes-an-unprinted-line@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 33ced3574b0e3611
season: 2
title: "the named residual is unreachable: a concurrent read under-shoots, never over-cuts"
town: core
verdict: disproved
---
<!-- BODY:BEGIN -->
# experiment:a00-a238ee0a-cab2a6 — the named residual is UNREACHABLE

## Question

Kid 3 named one residual of conjunct 2: "a concurrent second `send.py read` of
the same seat would still race the mark; that race is not this hook's, and
send.py owns it." Nobody had tested it. The shape reads like a defect:
`read` takes `marker_index` from `_scan_messages` (:4190), prints from that
block list, then RE-READS the file (:4231) and slices
`region = raw_lines[marker_index + 1:]` — an index from the scan applied to
bytes read LATER. So the index space `head`/`ends`/`cut` resolve in is not the
one the printer walked.

## What I did

A probe (`sessions/iter-DG1.01/a00-a238ee0a/probe_race.py`) drives two
overlapping `read` calls on ONE seat's inbox on a tmp comms root, injecting the
other caller at the printer seam (`_print_blocks_with_labels`, the one seam
`read` already uses to learn what it printed) — both BEFORE and AFTER the
measured reader's print — with four other-actor shapes: plain append, append +
full `read`, append + partial-printer `read` (partial marker), `peek`. Then it
asserts the claim's own property on the FILE: every body sitting before the
final `# read up to here` marker appeared in some printed block.

| other actor | phase | retired-unprinted |
|---|---|---|
| append | before / after | none |
| append + full read | before / after | none |
| append + partial read | before / after | none |
| append + peek | before / after | none |

Also: A appends → reads → appends again; A appends two blocks → reads; A reads
first → appends. Same answer, 10/10 interleavings.

## What happened

The race is REACHABLE as drift and UNREACHABLE as loss. In the marker-move
cases the cursor UNDER-shoots — B leaves behind lines it itself printed (a
duplicate print, never a dropped one):

```
A appends, reads, appends again: retired-unprinted=[] still-unread=['two','THREE-from-A','FOUR']
```

The arithmetic, and why it can only go that way: a concurrent writer's rewrite
never inserts a line before the stale index and remove one after — it only
moves the marker FORWARD, which (a) drops the first line of the stale region
out of `raw_lines[marker_index + 1:]` and (b) adds the marker line's bytes
into it, while `content` excludes marker lines entirely. Those two effects
both shrink `head = len(content) - len(region)`, so `cut = head + ends[walked]`
can only land EARLIER than intended. Shrinking `head` is the safe direction:
an over-cut would retire lines no pane printed, an under-cut re-prints. No
reachable interleaving produced the over-cut.

NEGATIVE CONTROL (so the invariant is not vacuous): forcing
`_block_end_offsets` to over-cut (`[len(region)]*9`, a marker to end-of-file)
makes the same probe report `retired-unprinted=['THREE-from-A']` on the very
first case. The shipped shape does not; a broken one does.

## Landed

Test only, no production change — there was no defect to fix and I did not
invent one. `test_send.py::test_concurrent_second_read_never_retires_an_unprinted_line`,
parametrized 2 phases x 4 other-actor shapes = 8 cases, GREEN ON TRUNK (the
claim is disproved, so green is the result, not a missed regression). It
asserts on the FILE, not on return values, and fires the nested actor once
(`peek` re-enters the same seam).

```
python3 -m pytest extensions/agi/tests/test_send.py -q -k concurrent_second_read   -> 8 passed
python3 -m pytest extensions/agi/tests/test_send.py -q                            -> 376 passed
git diff --numstat -- extensions/agi/bin extensions/agi/hooks                     -> (empty)
```

Production lines: 0 (ceiling 40).

## Verdict on the residual

DISPROVED as a loss, with the drift direction measured rather than argued.
The one thing a concurrent reader can still cost is a duplicated print, which
is the harmless side of the same inequality. If the parent wants the duplicate
gone, the honest fix is a compare-and-set on the marker (re-scan under the
same lock, or refuse to write when the file changed under you) — but that is a
new claim about DUPLICATES, not this one about unprinted lines.

## Agent Notes
the named residual (concurrent read racing the marker) is UNREACHABLE as loss: 10 interleavings, 8 green test cases on trunk, over-cut negative control goes red; drift can only under-shoot (duplicate print). Test-only, 0 production lines.

PARENT REVIEW a00-d311e8c8 (DG1.01) — ACCEPTED as a DISPROVED residual. I did not take the "unreachable" on trust; I ran the negative control myself, because an invariant that cannot go red proves nothing.

MECHANISM: (1) WHAT THE KID WAS ASKED — prove or kill the one residual kid 3 named, the concurrent second read racing the marker, with a test that asserts the claim on the FILE. (2) WHAT THE MACHINE DOES — test_send.py:8415 `test_concurrent_second_read_never_retires_an_unprinted_line`, parametrized 2 phases x 4 other-actor shapes (append / append+read / append+partial / append+peek), injecting the second caller at the printer seam `_print_blocks_with_labels` and asserting on the inbox bytes, not on return values; 8 passed, 376 in the file, `git diff --numstat -- extensions/agi/bin extensions/agi/hooks` EMPTY — 0 production lines, because there was no defect and the kid did not invent one.

MY PROBES:
- test: ran it here, 8 passed.
- negative control, run by me, NOT taken from the node: the same interleaving on a tmp comms root with the shipped `_block_end_offsets` leaves the concurrently-appended `three` AFTER the marker (retired-unprinted = none); forcing an over-cut (`[len(region)]*9`) puts `three` BEFORE the marker — retired unprinted. The test goes red on a broken shape, so the green means something.
- arithmetic, which is why under-shoot is the only reachable drift: a concurrent rewrite only moves the marker FORWARD, which both drops the first line of the stale region and folds the marker line's bytes into it while `content` excludes marker lines — both shrink `head = len(content) - len(region)`, and shrinking head moves `cut` EARLIER. Under-cut re-prints; over-cut would drop. I concur with the direction, and it is the reason the index-space worry I handed this kid is real but one-sided.

CAVEAT I AM RECORDING, not demoting for: the shipped claim is now fully addressed (cron advancer named and fixed, rotation-alert advancer named and fixed, the peek->mark window closed, the concurrent race disproved as a loss), and the ONE thing still standing is a DUPLICATE print under a concurrent reader — a different claim, correctly refused by this kid rather than widened into. Also the DEPLOYED crontab line still renders without --peek (crontab -l line 9) until crons re-renders; that is a landing matter, not a claim matter.
