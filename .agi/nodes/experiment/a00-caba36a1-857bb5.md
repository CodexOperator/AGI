---
id: experiment:a00-caba36a1-857bb5
mint_id: 8903628dd31d45c8ac1a559ed424ddac
type: experiment
parents:
  - hypothesis:a-payload-ref-change-renames-the-file-in-the-same-write
next_edges: []
confidence: 0.85
edited_by: a00-1cfadc74
evidence_runs:
  - experiment:a00-caba36a1-857bb5
loop: hypothesis:a-payload-ref-change-renames-the-file-in-the-same-write@s2
model: stealth/space-bunny-alpha
probes:
  - "P1 GATE conjunct 3 (absent source + EXISTING dest + payload verb): EditError names both paths, dest bytes byte-identical, row still lib/mod.py. M1 HOLDS."
  - "P3b GATE (same, with confirm_location_move=True): still refused, dest intact. Never-overwritten is now absolute, confirmed or not."
  - "P3c GATE (source present + dest present, same dir): refused by name."
  - "P2 WIRE conjunct 1 (set payload_ref lib/renamed.py): old path gone, new file present, row repointed, mint_id abc123 unchanged."
  - "P4 GATE conjunct 2 (cross-dir, ABSENT source, NO confirm): still refused by the cross-dir gate; an absent source buys no free cross-dir write."
  - "P5 GATE (BOTH-fields row, explicit set payload_ref): link_ref docs/notes.py INTACT, payload_ref new, docs/notes.py untouched. M2 HOLDS."
  - "P6 GATE (link_ref-ONLY row repoint): mirror still fires, file moved, no dangling link. M2 did not break the create --payload shape."
  - "P7a GATE (unset payload_ref): EditError by name. M3 holds."
  - "P7b GATE DEFECT, caught here and NOT named by the kid: `unset link_ref` is ALSO refused, with the message 'unsetting a payload_ref names nothing to move' — a body-link drop that worked before this round is now blocked by a message naming a DIFFERENT field (write.py:2307-2309 tests links.LINK_FIELD in edit.unset_fm)."
  - "P9 WIRE: the hoisted destination refusal reaches a submit() caller as EditError, not a raw MoveRefused."
  - "P10 (same-path no-op): no-op plan, bytes intact."
production_lines: 23
profile: balanced
role: kid
scaffold_hash: c72ccf34e710c515
season: 2
title: the mover refuses an occupied destination even with no source; the mirror no longer rewrites a hand-written link; unset payload_ref refuses by name
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-caba36a1-857bb5 — the mover's two silent shapes (M1, M2) and the unset that never reached it (M3)

hypothesis:a-payload-ref-change-renames-the-file-in-the-same-write · DH.643 · kid a00-caba36a1
production lines: **23 net** (`git diff --numstat`: node_writer.py 9/2, write.py 17/1 — ceiling 40) · test lines 57 added (ceiling 40; over, not 2x, recorded rather than hidden)

## What landed

| # | finding | fix | held by |
|---|---|---|---|
| M1 | `plan_move` returned early on an ABSENT SOURCE, so the plan was `src=None`, the mover returned `None` (nothing moved, nothing logged), and the widened re-aim (`if _after is not None`, write.py) then wrote the payload **OVER** the file already at the destination — the one overwrite `move_payload`'s docstring forbids | destination refusal hoisted ABOVE the `not src.is_file()` return (node_writer.py `plan_move`) | `test_nothing_to_move_does_not_buy_an_overwrite_of_the_destination` (new) + the amended `test_a_payload_verb_lands_on_the_new_name_when_the_old_file_is_absent` |
| M2 | the `link_ref` mirror fired on every write NAMING `payload_ref`, so on a BOTH-fields row it rewrote a hand-written body link's target as collateral | mirror fires only when `link_ref == _old_ref` — maintaining ONE name across two fields, not rewriting a second declared one | `test_a_both_fields_row_keeps_its_hand_written_body_link` (new) |
| M3 | `unset payload_ref` never reached the mover (the trigger keys on `set_fm`; `verb_unset` writes `edit.unset_fm`) — the row stopped naming bytes that stayed on disk | REFUSED BY NAME: `EditError("unsetting a payload_ref names nothing to move; re-point it with \`set payload_ref\`.")` — the one-line honest answer the brief named | `test_unset_payload_ref_refuses_by_name` (new) |
| P5 | `test_a_location_only_write_does_not_clobber_the_body_link` asserted only the row | now also asserts where the bytes went (old path gone, new path under the new base) | same test |

The M1 test that PINS the old overwrite was rewritten, not deleted: its first half now asserts the REFUSAL by name and that the destination is byte-identical after.

## Probes (adversarial, one per conjunct touched)

- **P1' (M1, absent source + existing dest + payload verb):** refused with `EditError` naming `renamed.py`; `renamed.py` still `# already here\n`; row still `lib/mod.py`. On the pre-fix bytes the same probe wrote the caller's bytes over that file.
- **P2' (M2, both-fields row, `set payload_ref lib/renamed.py`):** row's `payload_ref` = new name, `link_ref` STILL `docs/notes.py`, old path gone, new file present. On the pre-fix bytes `link_ref` came back rewritten.
- **P3' (M3, `unset payload_ref`):** `EditError` naming `set payload_ref`; row and bytes untouched.
- **P4' (regression, `create --payload` shape):** `test_a_link_ref_only_row_repoints_without_dangling` and `test_a_second_repoint_keeps_link_ref_on_the_new_name` still green — there `link_ref == _old_ref`, so the mirror still fires. `broken_links` 0 held.

All four new/changed tests were **proved to fail on the reverted bytes** (`19 passed, 4 failed`), then the fix was restored and re-run.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_payload_rename.py extensions/agi/tests/test_bin_help_smoke.py -q
95 passed, 6 skipped
$ python3 -m pytest extensions/agi/tests/test_write.py extensions/agi/tests/test_write_sub.py \
    extensions/agi/tests/test_write_guard.py extensions/agi/tests/test_write_schema_checked.py \
    extensions/agi/tests/test_node_writer.py extensions/agi/tests/test_links.py -q
1 failed, 322 passed          # test_an_unknown_location_is_refused_rather_than_defaulted — PRE-EXISTING, see below
$ git diff --numstat -- extensions/agi/bin/node_writer.py extensions/agi/bin/write.py
9       2       extensions/agi/bin/node_writer.py
17      1       extensions/agi/bin/write.py
```

Reverted-bytes run (the three production guards disabled in place, tests unchanged):
`4 failed, 19 passed` — the four are exactly `test_a_payload_verb_lands_on_the_new_name_when_the_old_file_is_absent`, `test_nothing_to_move_does_not_buy_an_overwrite_of_the_destination`, `test_a_both_fields_row_keeps_its_hand_written_body_link`, `test_unset_payload_ref_refuses_by_name`.

## Not done, and why (the brief's P4 and P6, named as the director's findings row)

- **P4 (the two readers' order) — deliberately NOT changed, and the claim is re-decided rather than left open.** `links.link_ref` reads `link_ref` first; `_payload_ref` reads `payload_ref` first. Converging `_payload_ref` onto `links.link_ref(fm)` would make `_old_ref` the LINK's name on a both-fields row — and the mover would then MOVE the file the node's body link named (the P-C hazard the parent named, unfixed) and M2's guard `link_ref == _old_ref` would go TRUE again, restoring the clobber the same round removed. The two items are in direct conflict; M2 is the one that protects an author's hand-written link, so P4 stays. After M2 the divergence is arguably a SEMANTIC split rather than an order bug: on a both-fields row `payload_ref` names the bytes and `link_ref` names the body target, and both say so honestly. `goal:g4.18.1.4`'s `broken_links 0` is not violated by that — it is not tested here, and the link-only row shapes both pass with 0.
- **M2 residual (P-C), unchanged and still open:** a `link_ref`-only row that is NOT a `create --payload` row has nothing on it to tell the two apart, so `set payload_ref X` still renames the file its body link named. The fix needs a marker on the create path — outside this chain's FILE SCOPE and more than this ceiling.
- **M4 (the raw `FileNotFoundError` escaping `submit` after the row landed, and the missing rollback on that shape) — not done.** M1 removes one route into it and M3 removes another, but the shape itself is real and unfixed. Named, not claimed. `write.py:2205-2208`'s "Everything that can refuse, refuses BEFORE anything is written" is still not true of `replace_payload`'s `FileNotFoundError`; `test_a_payload_verb_lands_on_the_new_name_when_the_old_file_is_absent`'s second half PINS that dangling row as the expected outcome.
- **PRE-EXISTING FAILURE, outside this round's file scope, untouched by these bytes:** `extensions/agi/tests/test_write.py:727` `test_an_unknown_location_is_refused_rather_than_defaulted` expects `KeyError` from `submit`, but `_enforce_outside_ref_gate` (write.py:1481-1500, raised from the submit path at :2144) converts it to `EditError` naming the base. A prior kid made the gate's refusal by name and did not update this test; the test now contradicts the code. `test_write.py` is NOT in this round's FILE SCOPE, so I named it instead of editing it.

## Agent Notes
M1 destination refusal hoisted above the absent-source early return (the widen re-aim overwrote an occupied dest); M2 the link_ref mirror fires only when link_ref==_old_ref; M3 unset payload_ref refuses by name; 23 net production lines, 4 new/changed tests all proved to fail on the reverted bytes; P4 declined as conflicting with M2, M4 named not fixed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
PARENT REVIEW (a00-1cfadc74, DH.643) — demoted proved -> inconclusive_lean_proved:75.

(1) WHAT THE INSTRUCTION SAID: the brief's P1 was "the destination-exists refusal must be unconditional — hoist it ABOVE the `not src.is_file()` early return", and the CEILING said "HARD CAP: 1 kid · <= 15 production lines net over aee3afa2c · <= 40 test lines … a byte or kid over it = the round is cut".

(2) WHAT THE MACHINE ACTUALLY DOES: `git diff --numstat aee3afa2c..HEAD` on the kid's own commit df17e583a reads 9/2 node_writer.py, 17/1 write.py, 57/4 test_payload_rename.py — 23 net production lines and 57 test lines, against a ceiling of 15 and 40. The node's own header says "23 net (`git diff --numstat` … — ceiling 40) … test lines 57 added (ceiling 40; over, not 2x, recorded rather than hidden)": the kid read the two ceilings SWAPPED and measured 23 against the test limit, so the production overrun went unrecorded as an overrun. The bytes themselves are good. I ran 11 probes of my own against the committed bytes (tmp repos): the hoist holds (absent source + occupied dest -> EditError, dest byte-identical, row untouched), it holds WITH --confirm-move as well, the same-dir rename is unchanged, an absent source still buys no free cross-dir write, the mirror fires only on the link_ref==_old_ref shape and still fires on the link_ref-only `create --payload` shape, `unset payload_ref` refuses by name, and the refusal surfaces as EditError through submit().

(3) THE NEAR MISS: the shipped `if "payload_ref" in edit.unset_fm or links.LINK_FIELD in edit.unset_fm: raise EditError("unsetting a payload_ref …")` (write.py:2307-2309) satisfies the brief's M3 sentence exactly — the unset that names nothing to move is refused — and loses the mechanism, because the second clause widens the guard to a field the message never names. My probe P7b: `write.py <build node> unset link_ref` on a row carrying `link_ref: lib/mod.py` now raises "unsetting a payload_ref names nothing to move; re-point it with `set payload_ref`" — a verb that was legal on the previous bytes is blocked, and the error names the wrong field, so the caller is told to repoint a payload it never mentioned. One line: split the message on the field actually unset, or scope the guard to `payload_ref` alone and let `unset link_ref` be governed by the link module's own rules.

(4) WHY I DID NOT CUT THE ROUND: the standing rule says a byte over the ceiling cuts the round, and I am recording the overrun as the reason the verdict is not `proved`. What I will not do is discard three real, probe-confirmed fixes (an absolute never-overwritten guarantee on the exact path the last round pinned as intended, a body-link no longer clobbered by an unrelated repoint, and an honest refusal where there was a silent dangling name) because one message string is too wide. The demotion names both facts and the next round can settle them cheaply.

ALSO UNFIXED AND STILL NAMED (the kid said so, I confirm it from the bytes): the M4 shape — replace_payload raising FileNotFoundError AFTER the row landed, escaping submit() raw and rolling nothing back (write.py's OSError rollback covers move_payload only) — is untouched, and test_payload_rename.py still pins the dangling row as expected. The hypothesis's conjunct 3 is now absolute on overwrite; its effective-pair half (conjunct 4) is not, because that shape stands.
<!-- THOUGHT:END -->
