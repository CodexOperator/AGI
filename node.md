---
id: experiment:a00-19f90859-1a9507
mint_id: 7fda228a34454ab9bef975cf56bdf911
type: experiment
parents:
  - hypothesis:l4-the-stops-end-of-slot-scan-is-fence-run-aware-so-a-heading-inside-a-nested-fence-never-truncates-the-slot
next_edges: []
confidence: 0.9
edited_by: a00-0a257e10
evidence_runs:
  - experiment:a00-19f90859-1a9507
loop: hypothesis:l4-the-stops-end-of-slot-scan-is-fence-run-aware-so-a-heading-inside-a-nested-fence-never-truncates-the-slot@s2
model: ~deepseek/deepseek-v4-flash-latest
profile: balanced
role: kid
scaffold_hash: b458e1047a45f287
season: 2
title: A00 19f90859 1a9507
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-19f90859-1a9507

## Experiment

goal:g15.25 FIX-ONLY. Two sites in `extensions/agi/bin/rotate.py` paired
fences by naive `startswith("```")` (any >=3 backticks toggles), so under a
four-backtick outer fence a first inner three-backtick line toggled the scan
CLOSED and a `#`-leading line inside the inner block ended the slot.

**1. `_write_stops_section` ### sub-header scan (:11162)** — rebuilt the
end-of-slot loop to use the existing `_fence_run` helper: record `opener` run
on an opener, treat a line as a closer only when `run >= opener` (CommonMark),
so an inner shorter fence and a `#` line inside it stay content; the `#` test
now fires only when truly outside any fence.

**2. `_replace_fence_after` (:5141)** — opener found via `_fence_run >= 3`;
closer search pairs the run-length-aware closest (`run >= opener`) instead of
the first three-backtick line.

Reproduced the falsifier pre-fix: a card whose stops slot held
`step one / ```sh / # a shell comment / inner / ``` / step two` rendered under
a four-backtick outer fence got CORRUPTED on the second `_write_stops_section`
write — `# a shell comment` cut the slot and its tail (`inner \`\`\`\nstep two\n\`\`\`\`)
leaked after the clean replacement block. Post-fix the second write replaces
the whole block and leaves nothing behind.

## Evidence

Falsifier repro (pre-fix second write leaked the tail):
```
### 🔴 Where it stops
```
clean new cmd
```
# a shell comment
inner
```

step two
````
## Other
keep me
```

Post-fix second write is clean:
```
### 🔴 Where it stops
```
clean new cmd
```
## Other
keep me
```

Three new tests added to `extensions/agi/tests/test_rotate.py` (the ceiling's
three):
- `test_stops_nested_fence_round_trip_byte_identical` — two identical
  inner-fenced stops writes produce byte-identical cards.
- `test_stops_hash_line_inside_inner_fence_never_truncates` — the `#`-inside-
  inner-block case; no tail leaked, after-slot section survives.
- `test_replace_fence_after_pairs_outer_within_longer_fence` — 4-backtick
  outer with a 3-backtick inner opener pairs the outer closer.

Full suite clean: `pytest extensions/agi/tests/test_rotate.py -q` → 230 passed.

## Agent Notes
Fenced both stops-slot scans on _fence_run run-length; # inside inner 3-backtick block under 4-backtick fence no longer truncates; 3 new tests, full suite 230 pass

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Reviewed by parent a00-0a257e10 (SL7.48). Instruction (target node testable_claim): "both scans record the opener's backtick run length and treat a line as a closing fence only when its run is >= the opener's; a #-leading line inside any nested fence never ends the slot; ... one fence-run helper used at two sites, three tests". Machine, cited: rotate.py:11117-11130 now records opener = _fence_run and closes only on r >= opener, # test fires only outside a fence; rotate.py:5148-5160 _replace_fence_after opens on _fence_run>=3 and pairs the first run>=opener. _fence_run (:10975) is the one pre-existing helper used at both sites. Tests at test_rotate.py:2531/2553/2578 exercise the nested round trip, the #-inside-inner-fence case, and the four-backtick outer pairing. Ran the suite myself: 230 passed in 46.10s, including the three new tests. Near miss: a naive fix that special-cases only the #-line inside a fence (skip # when in_fence) would pass two of the three tests and still truncate on a four-backtick outer whose inner opener is shorter — the falsifier test_replace_fence_after_pairs_outer_within_longer_fence is what discriminates. Deviation: none — the claim named the helper, the sites and the test count; the kid hit all three exactly. Evidence self-cited (experiment names itself), which the gate permits for a run.
<!-- THOUGHT:END -->
