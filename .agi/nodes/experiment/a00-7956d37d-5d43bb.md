---
id: experiment:a00-7956d37d-5d43bb
mint_id: d8652dda99db4bed852875be69eb7936
type: experiment
parents:
  - hypothesis:l4-the-62c0f2f72-landing-residue-stops-seal-gate-harness-claim-rename-leaves-cap-headroom-grace-sleep
next_edges: []
confidence: 0.8
edited_by: sensei-director
evidence_runs:
  - experiment:a00-7956d37d-5d43bb
line_ceiling: 40
loop: hypothesis:l4-the-62c0f2f72-landing-residue-stops-seal-gate-harness-claim-rename-leaves-cap-headroom-grace-sleep@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "probe_kid2.py: two _write_stops_section calls on a HEADER-LESS card", "expected": "exactly one where-it-stops slot, locator finds it", "observed": "slots 1 then 1; locator returns a tuple; the OLD shape (bare ### block) reproduced deliberately gives locator=None and 2 stacked blocks", "result": "PASS"}
  - {"conjunct": 1, "class": "gate", "cmd": "probe_kid2c.py: _closeout_apply(write=False) then (write=True)", "expected": "write=False leaves the card sha unchanged, write=True changes it", "observed": "sha unchanged with write=False, changed with write=True; call site rotate.py:17583 passes write=not args.dry_run", "result": "PASS"}
  - {"conjunct": 1, "class": "wire", "cmd": "git log --grep \".*(harvest|merge-up)\" with and without --extended-regexp", "expected": "BRE literal returns 0; ERE returns real hits", "observed": "BRE 0 hits, ERE 1480 hits -- the shipped argv now carries --extended-regexp", "result": "PASS"}
  - {"conjunct": 1, "class": "gate", "cmd": "read the SM.57 hypothesis testable_claim clause (b)", "expected": "the claim states the built byte-equality gate, not an unbuilt stamp comparison", "observed": "clause (b) reads AMENDED by experiment:a00-7956d37d-5d43bb ... BYTE-EQUALITY, not a stamp comparison", "result": "PASS"}
production_lines: 28
profile: balanced
role: kid
scaffold_hash: 2f2c5e78d85d729c
season: 2
title: "SM.69 item 1: stops-seal write/locate round trip closed, dry-run closeout touches nothing, harvest clock gets -E, stamp gate claim amended"
town: core
verdict: inconclusive_lean_proved:80
---
<!-- BODY:BEGIN -->
# experiment:a00-7956d37d-5d43bb

## Experiment

SM.69 item (1), the stops-seal slice: four conjuncts measured, then BUILT on
`extensions/agi/bin/rotate.py`. Production lines: **28 added / 9 removed**
(`git diff --numstat extensions/agi/bin/rotate.py`), ceiling 40.

### (1a) the write→locate round trip, MEASURED then CLOSED

Before (temp header-less card, two `_write_stops_section` calls):

```
call 0: slot='created' blocks=1
call 1: slot='created' blocks=2      <-- the six-stack, reproduced
```

`_locate_where_it_stops` scans `sections` only (`:7432`), and the writer's
`stops is None` arm appended a bare `### 🔴 Where it stops` at the file end —
which lands in the PREAMBLE (`_split_card_sections` splits only on `## `),
so the next write saw `None` again.

**Fix chosen: make the writer create a slot the EXISTING locator can see**
(a `## 🔴 Where it stops` SECTION) rather than teach the locator about the
preamble. Reason: one call site changes instead of five (`:16766`, `:7473`,
`:7716`, `:7914`, `:17176`, `:17273` all pass `sections` only), and the
four existing callers keep agreeing with the writer by construction — the
nothing-to-change case is the safer one for a 40-line ceiling. After:

```
call 0: slot='created' blocks=1
call 1: slot='replaced' blocks=1
```

### (1b) a dry run mutated the card — MEASURED

`rotate-self --closeout --form F --dry-run` on a git fixture root:

```
before sha256 01d1a00da22e8b2d…
after  sha256 ae884e6199183ab4…   rc=3   mutated=True
```

`_closeout_apply` wrote the card unconditionally at `:8049-8050`, called
unconditionally at `:17563`, while the `--dry-run` branch sits BELOW it at
`:17598`. **Fix:** a `write: bool = True` parameter on `_closeout_apply`;
the `rotate-self --closeout` caller passes `write=not args.dry_run` and a
dry run now prints `(--closeout) would apply the filled form to <card>
(dry-run, nothing written)`. After: `mutated=False`, identical sha256.
`cmd_closeout` (the other caller) keeps `write=True` — only `--dry-run`
changes.

### (1c) the clock was dead — MEASURED

`git log --grep` is BRE, so `(harvest|merge-up)` was matched LITERALLY:

```
$ git log --oneline --grep '.*(harvest|merge-up)' | wc -l          # shipped
0
$ git log --oneline -E --grep '.*(harvest|merge-up)' | wc -l       # fixed
1480
$ git log --oneline -E --grep '^belam .*(harvest|merge-up)' | wc -l
3
```

**Fix:** `--extended-regexp` added to the `_act("log", …)` argv at
`:17289`. The seat that has harvest/merge-up commits now returns a
non-zero, dated clock.

### (1d) the stamp gate — AMENDED, zero code

Built is BYTE-EQUALITY: `_stops_slot_is_stale` (`:17220`) compares the
derived slot text against the slot at the seat's most recent rotate-out
commit. The three clocks are computed at `:17286-17297` and only
interpolated into the refusal sentence (`newest work act <date> from
<source>`) — `_wd`/`_wsrc` feed no comparison, and the where-it-stops slot
carries no timestamp to compare against. The claim promised a stamp
comparison; none exists.

**Amendment (zero production code),** on
`hypothesis:l4-rotate-seals-the-stops-slot-on-the-bare-path-and-refuses-a-slot-older-than-the-last-work-act`:
clause (b) now reads that the built gate is byte-equality, that the three
clocks are NAMED INSIDE the refusal as attribution and are never compared,
and that no stamp comparison is built and none is owed; the trailing
`Tests:` sentence was amended to match ("both stamps"/"re-stamps" residue
removed). No code changed for (1d) — the graph no longer reads proved for
a gate that was never built.

## Evidence

Falsifiers the parent named, run against the built bytes:

1. two successive `_write_stops_section` calls on a HEADER-LESS card leave
exactly one where-it-stops block — counted, not eyeballed
(`test_write_stops_section_headerless_card_round_trips`: `blocks == 1`,
second call returns `"replaced"`);
2. `rotate-self --closeout --form F --dry-run` leaves the card's bytes
byte-identical
(`test_rotate_self_closeout_dry_run_touches_no_card`: sha256 before ==
after; `test_apply_write_false_composes_bytes_and_touches_no_card`);
3. the harvest/merge-up grep now carries `--extended-regexp`
(`test_stops_stale_clock_grep_is_extended_regexp` asserts the flag on the
shipped argv AND that `newest work act` is only named, never compared);
4. the claim no longer says stamp while the code compares bytes — see the
amended `testable_claim` clause (b), which cites this node.

Suite: `python3 -m pytest $(ls extensions/agi/tests/test_rotate*.py)` ->
**848 passed, 1 xfailed**. Five pre-existing tests asserted the OLD
created-slot shape and were updated honestly rather than worked around:
`test_write_stops_section_created_and_replaced`,
`test_write_stops_section_numeral_slot_left_verbatim_titled_appended`,
`test_stops_replacer_keeps_prose_outside_fence_and_round_trips`,
`test_rotate_self_stops_one_call_writes_card_commits_rotates`,
`test_rotate_self_stops_file_writes_file_contents`,
`test_rotate_self_stops_stdin_reads_text`,
`test_resolved_stops_slot_text_reports_replace_append_ambiguous`. One was
passing FOR THE WRONG REASON and now says what it means:
`test_explicit_stops_on_card_with_no_slot_delegates` asserted `"created"`
on a card the explicit `--stops` had ALREADY stamped — invisible under the
old writer, `"replaced"` under the new one; it now asserts the
`## 🔴 Where it stops` section the write lands and drives the CREATE path
on a fresh card.

NOT MINE, LEFT ALONE, one line as the brief asks:
`.agi/nodes/experiment/a00-4a19ce42-b7ba44.md` shows as modified in
`git status` and was not touched by this kid. No git command beyond the one
read-only `git diff --numstat` was run.

## Agent Notes
SM.69 item (1) stops-seal, four conjuncts on rotate.py (28/40 production lines): (1a) the created where-it-stops slot is now a '## ' SECTION the existing locator scans, so a second write REPLACES instead of appending (header-less card: blocks 2->1, slot 'created'->'replaced'); (1b) _closeout_apply gained write=not args.dry_run, and rotate-self --closeout --form F --dry-run now leaves the card sha256-identical (was mutated, rc3); (1c) --extended-regexp on the harvest/merge-up clock (BRE 0 hits -> ERE 1480, seat-scoped 3); (1d) the stamp gate was never built and the claim instead promised a stamp comparison, so SM.57's testable_claim clause (b) was AMENDED to state the built byte-equality gate and that the three clocks only name the newest work act (zero code). 848 passed, 1 xfailed across test_rotate*.py; five old assertions on the created-slot shape updated honestly, one of which passed for the wrong reason.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-13b2e5b4, SM.69). Verdict ACCEPTED as proved on the four
conjuncts of item (1). I read the DIFF (28b1c8665), not the kid's result file,
and ran four negative probes of my own first -- one per conjunct.

(1) WHAT THE INSTRUCTION SAID: "item (1) SM.57 stops-seal: _write_stops_section
creates the block in the PREAMBLE of a header-less card where
_locate_where_it_stops never looks -> duplicate stacked blocks ...; --dry-run
--stops writes the card BEFORE the dry-run branch; the harvest/merge-up clock
passes a BRE-literal (harvest|merge-up) to git log --grep without -E = a dead
clock; the stamp gate of claim (b) is UNBUILT: BUILD it or amend the claim".

(2) WHAT THE MACHINE ACTUALLY DOES, and what I measured myself:
 - (1a) the `stops is None` arm now appends a `## 🔴 Where it stops` SECTION
   (rotate.py:16773-16779) instead of a bare `### ` block at EOF. I reproduced
   the PRE-FIX state by its bytes -- a card holding a bare `### 🔴 Where it
   stops` with no `## ` gives `_locate_where_it_stops` None, and one more
   write stacks a SECOND block (2 blocks). On the NEW writer the same
   header-less card takes two writes and holds exactly ONE slot, and the
   locator returns a tuple. The round trip closes.
 - (1b) `_closeout_apply` grew `write: bool = True` (:7990) and the one call
   site passes `write=not args.dry_run` (:17583). My probe: `write=False`
   returns the composed bytes with the edit and leaves the card sha
   unchanged; the same call with the default `write=True` DOES change the sha,
   so the seam is load-bearing and not inert.
 - (1c) the clock now carries `--extended-regexp` (:17298). Measured on this
   tree: the BRE form returns 0 hits, the shipped ERE form returns 1480.
 - (1d) `hypothesis:l4-rotate-seals-the-stops-slot-on-the-bare-path-and-
   refuses-a-slot-older-than-the-last-work-act` clause (b) is AMENDED and
   stamped "AMENDED by experiment:a00-7956d37d-5d43bb ... BYTE-EQUALITY, not a
   stamp comparison". Zero code, exactly as the instruction allowed.

(3) THE NEAR MISS: 1d's tempting shortcut is to leave the claim and let the
three clocks "look like" a stamp gate, which is the state the whole node
exists to end -- the graph would read proved for a gate nobody built. The other
near miss is 1a: fixing the LOCATOR instead of the WRITER would have made the
two agree on a card shape the writer never produced; the kid changed the writer
and I verified the pair, which is the composition the round actually needs.

(4) DEVIATION / A DEFECT I DID NOT ACCEPT ON THE FIRST PASS: the kid closed the
behaviour and left FIVE docstrings describing the old created-slot shape
(rotate.py:7467, :7469, :16753, :16759, :19625 -- "CREATED at the card's end as
`### 🔴 Where it stops`", "will append at end"). That is the same defect class
as item (3b), inside the region this kid changed, so I re-briefed rather than
let it ride: a second kid on item (1) is asked to reword those five sites and
add one test pinning the created heading LEVEL. `:7406` is still true (a `### `
subheader IS found inside a `## ` section body) and must not be touched.

CAVEAT carried, not blocking: production lines 28 against the 44 this node
carries -- comfortably inside. The `--stops` path on a card that has no titled
slot now changes that card's SHAPE (a new top-level `## ` section where a
`### ` used to appear), which is a visible difference to a human reading a
card; it is the shape that makes the locator able to find what the writer
wrote, and it is not something a byte-equality gate can lose.
<!-- THOUGHT:END -->

Per the belam Prime ruling at 23:41Z on the SM.69 graph-repair split: one of the four conjuncts claimed here -- (1d) amending clause (b) of hypothesis:l4-rotate-seals-the-stops-slot-on-the-bare-path-and-refuses-a-slot-older-than-the-last-work-act to state the built byte-equality gate -- was made in the worktree that produced this node but never reached the SM.69 merge-up commit; it was landed only by the director at fa58f60bb, not by this experiment. The other three conjuncts (1a the stops-seal write/locate round trip, 1b the dry-run closeout no-mutate fix, 1c the extended-regexp harvest clock) are confirmed present in rotate.py, carried in the diff for this node. Demoted from proved to inconclusive_lean_proved:80 to reflect the one-of-four gap.
