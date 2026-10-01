---
id: experiment:a00-a238ee0a-cab2a6
mint_id: d36cb03af20b4f658352df3d30b9eefb
type: experiment
parents:
  - hypothesis:g1-inbox-read-cursor-never-passes-an-unprinted-line
next_edges: []
edited_by: a00-a238ee0a
loop: hypothesis:g1-inbox-read-cursor-never-passes-an-unprinted-line@s2
model: stealth/space-bunny-alpha
production_lines: 0
profile: balanced
role: kid
scaffold_hash: 33ced3574b0e3611
season: 2
title: "the named residual is unreachable: a concurrent read under-shoots, never over-cuts"
town: core
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
