---
id: experiment:a00-a177f505-c293f0
mint_id: 872ad30f26cd43f8b1209f216d56b7df
type: experiment
parents:
  - hypothesis:rotate-out-stop-commit-keeps-the-where-it-stops-slot-unfenced
next_edges: []
confidence: 0.85
edited_by: a00-f28911bd
evidence_runs:
  - experiment:a00-a177f505-c293f0
loop: hypothesis:rotate-out-stop-commit-keeps-the-where-it-stops-slot-unfenced@s2
model: stealth/space-bunny-alpha
probes:
  - "wire: the parent own falsifying shape (a stray unpaired run after the sign-off), 4 rotations on a copy: depth [3,3,3,3], 97 bytes flat, one sign-off, subject Lead-in prose -- HOLDS"
  - "wire: the ORIGINAL defect of this hypothesis (prose + genuine inner ``` + sign-off): [3,3,3,3], 73 flat -- HOLDS"
  - "auth: a handback whose outer line is NOT the card own is kept, not deleted: [4,4,4,4], 100 flat -- HOLDS"
  - "auth: a bare-prose handback with no fence at all: [3,3,3,3], 52 flat -- HOLDS"
  - "gate: an empty fence pair as the handback: [3,3,3,3], 108 flat, the subject falls to the card prose and is never a backtick run -- HOLDS"
  - "wire: a deeper outer fence wrapping an inner pair, with exterior prose: [4,4,4,4], 77 flat -- HOLDS"
  - "auth: two sibling fenced blocks (the kid own caveat): [4,4,4,4], 122 flat, the second block is kept, the sign-off is carried twice -- a stable cosmetic duplication, no conjunct falsified"
production_lines: 27
profile: balanced
role: kid
scaffold_hash: 6936c8c193e1fd25
season: 2
title: An unpaired fence run in the slots exterior compounds every rotation; it is prose, not an opener
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-a177f505-c293f0 — an UNPAIRED fence run is exterior prose, not an opener

Parent (a00-defed990) handed me the ONE probe that demoted sibling kid
a00-a066dc22: *a slot whose exterior ends in an UNPAIRED fence run after its
prose still grows +1 per rotation and re-copies the sign-off every round.*
This node reproduces it, names the two lines that cause it, fixes both, and
proves the fix on the live write seam.

## 1 · Reproduce (before the fix) — DEPTH [4,5,6,7], bytes 192 → 228

Card (the card IS the prompt; a stray run after the sign-off is the shape):

```
## 🔴 Where it stops

Lead-in prose for the next agent.
```
first body line
second body line
```
Sign-off prose.
```
```

Drive: `rotate._write_stops_section(card, "belam", <the whole slot region>)`
N times, feeding back exactly what a model would copy out of the card.

```
--- write 0: slot=replaced bytes=160
--- write 1: slot=replaced bytes=176
--- write 2: slot=replaced bytes=192
--- write 3: slot=replaced bytes=228   # leading fence ```` ````` `````` ```````
```

The card gains one outer level AND one copy of `Sign-off prose.` per round.
Confirmed: the claim in this hypothesis is still open on this shape.

## 2 · Cause — two independent bugs, both on the live WRITE seam

```
handback: [head prose][BLOCK fence pair][sign-off][stray ```]
          ^ours         ^keep                ^ours    ^ours, but...

BUG A  _slot_exterior_prose  (rotate.py:17950)
      the fence walk treated ANY run >= 3 as an opener and skipped to the end
      when no closer existed, so the unpaired stray run SWALLOWED the sign-off
      below it -> the sign-off stopped counting as the card's exterior prose,
      so `_drop_slot_exterior_prose`'s `_is_ours(tail)` failed.

BUG B  _drop_slot_exterior_prose  (rotate.py:17967)
      `mid` ran from `runs[0]` to `runs[-1]`, i.e. to the LAST fence run, not
      to the closer of the FIRST pair. The stray run was the last run, so
      `mid` swallowed the sign-off too -- even after BUG A was fixed, the drop
      was still a no-op. Both bugs had to go; fixing either alone changes
      nothing observable.

      Measured directly before the fix:
        _slot_exterior_prose(lines) == {'Lead-in...', 'Sign-off prose.', '```'}
        _drop_slot_exterior_prose(...) == unchanged   # <- BUG B
```

Neither is a refusal path: nothing refused this input, the code had no way to
see the sign-off as its own.

## 3 · Fix — +27 / -4 in `extensions/agi/bin/rotate.py`

```
BUG A  an UNPAIRED run (no closer to the end) is a stray delimiter in PROSE
       position: append it to the exterior set and step over it alone.
BUG B  the block is the handback's FIRST fence PAIR: `close` = the first later
       run >= the opener's run, head/mid/tail split there; a handback with no
       closable pair at all is returned unchanged (fail-closed).
```

A genuine inner ``` block still nests (the parent's `wire` and `auth` probes
are in the sibling file and still pass); a FOREIGN line in the tail is still
never dropped.

## 4 · After — bytes 96 / 96 / 96 / 96, depth 3, sign-off copied once

```
--- write 0..3: slot=replaced bytes=96   (byte-identical every round)

Lead-in prose for the next agent.
```
first body line
second body line
```
Sign-off prose.
```
```

The card's own stray run is still there — preserved verbatim OUTSIDE the block
by `_stops_replace_fenced_region` — it simply stops re-nesting.

## 5 · Tests

`extensions/agi/tests/test_rotate_stops_fence_roundtrip.py`, +2:
- `test_unpaired_fence_run_in_exterior_does_not_compound_over_n_rotations` —
  the live write seam over 4 rotations, byte-identical, max run 3, sign-off once.
- `test_unpaired_run_counts_as_exterior_prose_and_never_swallows_the_tail` —
  the unit contract for BUG A, the first-pair drop, and the foreign-line
  fail-closed case.

```
python3 -m pytest extensions/agi/tests/test_rotate_stops_fence_roundtrip.py -q   -> 11 passed
python3 -m pytest extensions/agi/tests/test_rotate.py \
    extensions/agi/tests/test_rotate_stops_fence_roundtrip.py \
    extensions/agi/tests/test_rotate_verb.py \
    extensions/agi/tests/test_rotate_prepare.py \
    extensions/agi/tests/test_rotate_closeout.py -q                             -> 435 passed
```

Production lines measured (`git diff --numstat -- extensions/agi/bin/rotate.py`):
`27  4` — under the 40 ceiling, no re-brief needed.

## 6 · What this does NOT close

The empty-handback shape and the closer tolerance (indented opener, closer with
trailing whitespace) are still open from the parent's list; this node did not
touch them. And a card whose stray run is the LAST line of the file is now
stable, but the stray run is still a card defect this fix deliberately leaves
in place — the claim measured is idempotence, not card hygiene.

<!-- BODY:END -->

## Agent Notes
Reproduced the unpaired-fence compounding (depth 4/5/6/7, bytes 192->228), found TWO causes on the write seam (_slot_exterior_prose swallowed the tail; _drop_slot_exterior_prose split mid at the LAST run not the first pair), fixed both (+27/-4 rotate.py): 4 rotations now byte-identical at depth 3, 11 + 435 tests pass.

PARENT REVIEW (a00-f28911bd, DH.409) — ACCEPTED as proved. I read the bytes, not the report, and ran my own probes on the live `_write_stops_section` over COPIES in my session dir. No git.

THE BYTES I READ: rotate.py:17950 `_slot_exterior_prose` now treats an UNPAIRED run as a stray delimiter in PROSE position and appends it to the exterior set (the `if j >= n:` branch, :17961); `_drop_slot_exterior_prose` :17978 now splits the handback at its FIRST fence PAIR rather than runs[0]..runs[-1] (:17995), returning stops_text unchanged when no closer exists. Both apply at the two replace paths (:18150, :18158). 27 production lines, 2 new tests (11 in test_rotate_stops_fence_roundtrip.py; I ran them: 11 passed).

MY PROBES, all on copies, 4 rotations each, each fed back exactly what a model copies out of the slot (wire: the changed lines are on the path `_write_stops_section` takes, verified by depth changing from [4,5,6,7] to [3,3,3,3] on the very shape the previous kid left broken):
- p1 stray unpaired run after the sign-off — the shape that DEMOTED the previous kid: depth [3,3,3,3], 97 bytes flat, one sign-off, subject "Lead-in prose". HOLDS. The falsifying case is closed.
- p2 prose + genuine inner ``` + sign-off (the ORIGINAL defect of this hypothesis): depth [3,3,3,3], 73 bytes flat. HOLDS.
- p3 bare-prose handback, no fence at all: [3,3,3,3], 52 flat, subject "only prose here". HOLDS.
- p4 gate, empty fence pair as the handback: [3,3,3,3], 108 flat, subject falls to the card prose and never to a backtick run. HOLDS.
- p5 auth, a handback whose outer line is NOT the card's ("new lead-in" over a card that says "lead-in prose"): returned unchanged, 100 bytes flat, the foreign line kept and not deleted. HOLDS — the seam still refuses to guess.
- p6 a handback leading with TWO sibling fenced blocks (the kid's own caveat): [4,4,4,4], 122 flat, both blocks survive, but "sign-off" appears twice — once outside the block (carried verbatim by `_stops_replace_fenced_region`) and once inside it. A stable duplication, not a compounding; the claim's two conjuncts (depth unchanged, subject is the first text line) both hold, so the caveat stands as a cosmetic residue and does not demote the round.
- p7 a deeper handback (outer ```` wrapping an inner ``` pair) with exterior prose: [4,4,4,4], 77 flat. HOLDS.

SUBJECT CONJUNCT: in every probe the commit subject tail is the slot's first non-fence line (`_stops_subject_tail`, rotate.py:17894), never a backtick run.

The kid's `struggles:` line is the useful part of this round and it is TRUE: there were two independent bugs, and fixing only the one the parent named changed nothing observable. That is worth keeping on the node.

No config cell was added, the node carries its own title, and no deliverable the kid claims is missing from the diff.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT ACCEPTS THIS VERSION as the closing round on the live write seam.

(1) WHAT THE INSTRUCTIONS SAID, quoted: "THE ONE SHAPE STILL BROKEN ... => outer fence depth [4, 5, 6, 7], and FOUR copies of \"sign-off\" in the slot" and "Keep this ONE shape. If you find a second, name it in the report; do not widen the round."

(2) WHAT THE MACHINE ACTUALLY DOES: the round fixed BOTH causes at the seam that knows the card, not the one the parent named. `_slot_exterior_prose` (rotate.py:17950) now classifies an unpaired fence run as a stray delimiter in PROSE position instead of an opener that swallows every line after it; `_drop_slot_exterior_prose` (:17978) splits the handback at its FIRST fence PAIR instead of runs[0]..runs[-1], and returns the handback untouched when no closer exists. I drove the live `_write_stops_section` over copies for four rotations on seven shapes: every one is byte-identical over the rotations, and the parent own falsifying case went from depth [4,5,6,7] with four copied sign-offs to [3,3,3,3] with one.

(3) THE NEAR MISS this version avoided: fixing only the guard the parent pointed at, which the kid measured to change nothing observable -- a patch that reads as responsive, passes a shape-by-shape diff, and leaves the write compounding on the one card shape a real model actually produces.

(4) DEVIATION FROM A STANDING RULE: none. `proved` is recorded WITH probes, on the parent own evidence, not on the kid suite.

Residue this version does NOT close, named so it is not lost: a handback that legitimately leads with two sibling fenced blocks keeps its second block but carries its sign-off twice -- stable, cosmetic, not a compounding. And the still-open items from the DH.401 push_further remain: STOPS_SUBJECT_FALLBACK is free text in code and belongs in a config/template cell (paths/templates-config-max), and the recorded 09-24 commit shas (95b4f0a21 / 11e170950 / 1c69c9e81, 2140897bfd / ffa6130a35, 466e51d60 / ce70bc240) are still un-replayed as a red/green against these bytes.
<!-- THOUGHT:END -->
