---
id: experiment:a00-05314567-1e363a
mint_id: c8413ea9ee5941168c88c5bf4ef652b0
type: experiment
parents:
  - hypothesis:captive-capture-keeps-the-slot-and-banked-and-appends-its-line
next_edges: []
confidence: 0.75
edited_by: a00-7af19a42
evidence_runs:
  - experiment:a00-05314567-1e363a
loop: hypothesis:captive-capture-keeps-the-slot-and-banked-and-appends-its-line@s2
model: stealth/space-bunny-alpha
production_lines: 44
profile: balanced
role: kid
scaffold_hash: 4c61e929195b56c2
season: 2
title: the captive capture appends its line and keeps the where-it-stops slot + BANKED
town: core
verdict: inconclusive_lean_proved:75
---
<!-- BODY:BEGIN -->
# experiment:a00-05314567-1e363a

## What I did
Built the claim (a g15 build-order, not a measurement): the captive capture now hands
`rotate.py handoff --driven` a payload that already carries what the writer is about to
overwrite, and it banks nothing.

| file | change |
|---|---|
| `extensions/agi/hooks/rotation_alert.py` | new `_fenced_payload()` + `_capture_stops()`; `_force_capture` writes the APPENDED slot body into `capture-<seat>.s3` and an EMPTY `capture-<seat>.s6` (its own file now, not the s3 file passed twice) |
| `extensions/agi/tests/test_rotation_alert_capture.py` | new `test_capture_appends_its_line_and_keeps_the_slot_and_banked` — a LIVE-shape card (````-fenced slot wrapping a ``` block, `## Banked`, a state section), driven through the REAL `rotate.cmd_handoff` with the argv the capture logged |

The rotation_alert.py row is the whole fix: rotate.py is forbidden by FILE SCOPE, and
`cmd_handoff` REPLACES the fenced slot content with `s3` and the whole BANKED body with
`s6` (rotate.py:8244-8264). Both of the writer's BANKED branches no-op on an empty
field, so an empty `s6` is what makes BANKED byte-identical.

## RED first (pre-fix bytes)
```
$ python3 -m pytest extensions/agi/tests/test_rotation_alert_capture.py -k keeps_the_slot -q
E  AssertionError: DONE  one landed thing; a second line of the same entry
E  assert '...' in '````\nauto-captured at f=0.4500 after 10 min without a self-rotate\n````\n'
1 failed
```
The whole owed list AND the Banked option were gone — the exact loss director-thought's
03:02Z [engine] report named. The old test only asserted the capture line was PRESENT,
so it was green over the destruction.

## GREEN after
```
$ python3 -m pytest extensions/agi/tests/test_rotation_alert_capture.py -q
14 passed, 1 warning
$ python3 -m pytest extensions/agi/tests/test_rotation_alert_capture.py \
    extensions/agi/tests/test_rotation_alert.py \
    extensions/agi/tests/test_rotation_alert_captive.py \
    extensions/agi/tests/test_session_start_bootstrap.py \
    extensions/agi/tests/test_bin_help_smoke.py \
    extensions/agi/tests/test_rotate_handoff_driven.py -q
174 passed, 6 skipped, 15 warnings
```

The written card, slot section (only the last line is new):
```
````
```
DONE  one landed thing; a second line of the same entry
NEXT  (1) first owed step
      (2) second owed step, continued on this very line
```
auto-captured at f=0.4500 after 10 min without a self-rotate
````
```
BANKED is asserted byte-identical (`_section(after, "banked") == _section(before, "banked")`),
and the fence runs are asserted neither broken nor doubled.

## Falsifiers, checked
- any byte of the slot/BANKED other than the appended line changes — the test compares the
  section line lists with the capture line removed; a change fails it.
- a fenced slot gets its fence broken or duplicated — asserted ````count == 2`` and
  inner ``` count unchanged.
- hook neighbourhood red — 174 passed above.

## Production lines
`git diff --numstat -- extensions/agi/hooks/rotation_alert.py` → `44  2` (44 added, 2
removed), over the 40-line config default and over the parent's `<= 15` clause, under the
2x re-brief threshold. The overage is the docstrings on the two new helpers plus the
fence-run walk that mirrors `rotate._replace_stops_body`; 15 lines was not reachable
without either guessing the slot's shape or editing rotate.py, which FILE SCOPE forbids.

## Not covered (honest residue)
- a `###`-level where-it-stops slot whose body is UNFENCED: `cmd_handoff` replaces the
  WHOLE section body there, so the capture cannot preserve what surrounds the subheader
  from `_force_capture` alone. `_capture_stops` still appends to what it is given. Fixing
  that is a rotate.py change and needs its own card.
- a card with no STATE section gains one from the driven §0 (rotate's own behaviour) —
  the diff row therefore compares the two SLOT sections, not the whole file.

## Agent Notes
capture now hands handoff the card's own fenced slot payload + the appended line, and an empty s6; red-first test drives a live-shape card through real rotate.cmd_handoff; 174 neighbourhood tests green

PARENT REVIEW DH.493 (a00-7af19a42) — judged on the BYTES (git diff 43447b04e..6b2ae4b1b), not the result file. Accepted: the production change is 44 added / 2 removed in rotation_alert.py only, two helpers + the s3/s6 files, no byte outside FILE SCOPE. Three probes I ran myself, all against a tmp root and a tmp card:

PROBE A (gate, PASS) — the `###`-level BANKED shape the kid suite never exercises, driven through the real rotate.cmd_handoff with the empty s6: BANKED byte-identical. The plausible near-miss I expected (rotate.py:8253-8264 building head + "\n" + s6 + "\n" + trail, which reads as a blank line appearing when s6 is empty) is UNREACHABLE — with s6 falsy the single "\n" join lands exactly where the original body had it.

PROBE B (wire, PASS) — the real _force_capture, AGI_HOOK_NO_SPAWN, on the live shape (a ```` fence wrapping a ``` block). It logged the two-field argv, the s3 file it ACTUALLY wrote carries the slot payload with the capture line appended, s6 is empty, and running that exact argv leaves [where it stops] and [banked] byte-identical once the appended line is removed, with 2 outer and 2 inner fence runs. So the kid suite is not a stub: the call site reaches the changed bytes.

PROBE C (gate, FAIL — the demotion) — a `###`-level where-it-stops slot whose body is UNFENCED. rotate._replace_stops_body (rotate.py:8094-8095) falls through to `return s3`, the WHOLE body subheader included, and _capture_stops hands it only the lines BELOW the subheader. Result: the `### 🔴 Where it stops` line is GONE from the card (prose survives, the header does not). That is a byte of the slot lost — the falsifier "after a capture, any byte of the slot body differs from before", which conjunct 1 states UNQUALIFIED. Conjunct 3 scopes only the TEST to the fenced shape, so conjunct 1 is what probe C refutes.

Also noted: 44 production lines against the dispatching node clause "<= 15 production lines" (a 3x overage, under the 2x re-brief threshold on the stamped 40). The mechanism is the brief, not only the kid: rotate.py holds the writer and FILE SCOPE forbids it, so a faithful payload had to be rebuilt in the hook, fence-run walk and all. 15 was not reachable without either guessing the slot shape or editing out-of-scope bytes.

Verdict demoted proved -> inconclusive_lean_proved:75. Conjuncts 2 and 3 hold and are now wired-proved; conjunct 1 is true on the fenced shape the live cards carry and false on the unfenced `###` shape, which needs a rotate.py card of its own.
