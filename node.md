---
id: hypothesis:l4-rotate-refuses-a-where-it-stops-slot-unchanged-since-the-predecessors-rotate-out-naming-the-gen-pair-and-commit
mint_id: 666fbb68d9874315b921eab86e63c0c6
type: hypothesis
parents:
  - goal:g15.25
next_edges: []
edited_by: sanctuary-master
scaffold_hash: 8122ecdb5263d615
season: 2
testable_claim: "goal:g15.25 FIX-ONLY (SM order 23:39Z, residue (a) of SL7.115 — the bare `rotate` verb's default --stops is the card's where-it-stops slot AS IS, so a slot the seat never rewrote during its own generation hands the PREDECESSOR's stop block to the successor as if it were fresh). MEASURED on the post tip: `_default_stops_text(root, seat)` rotate.py:14416 returns (slot body stripped, header) with no notion of age; `cmd_rotate` :16656 calls it at :16719 when none of --stops/--stops-file/--closeout was given; the predecessor's rotate-out is ONE pathspec commit whose message is `f\"{seat} rotate-out gen {_gb}->{_gb + 1}: {_first}\"` (:14694, written by `_commit_stops_row` :14146) — the card at THAT commit holds exactly the stops text the predecessor wrote; the rotation record (`_latest_rotation_record(root, seat)` :4931; `result: started` written at :3600) carries recorded_at/gen_before/gen_after but NOT the stops text. Live measure on this post: `rotate --dry-run` at 23:2xZ resolved 581 chars whose header stamp read 22:14Z — the previous generation's block. CLAIM: (1) a new `_stops_slot_is_stale(root, seat, text) -> str | None` compares the derived slot text (stripped) with the slot text of the card AT the seat's most recent rotate-out commit (found by `git log -1 --format=%H --grep='^<seat> rotate-out gen ' -- <card>`; the slot located with the same locator `_default_stops_text` uses) — byte-equal after strip = STALE, returning a refusal that NAMES BOTH: the gen pair and short sha + date of that rotate-out commit, and the fix ('write the card where-it-stops section or pass --stops'); no such commit (a first seating, a gitless fixture) or a differing text = None; (2) `cmd_rotate` runs the gate ONLY on the derived default (never on an explicit --stops/--stops-file/--closeout) and refuses exit 2 by name, nothing delegated — `--dry-run` prints the refusal and still returns 2 (a dry run that would rotate on a stale block must say so); (3) rotate-self's own `--stops` path is untouched; (4) the started rotation record ALSO gains `stops_sha256` (sha256 of the stripped stops text written at :14694's commit) so a future gate can read the record instead of git — written where the started record is composed, read by nothing yet (say so in the docstring). FALSIFIERS: a gate keyed on the card file's mtime or last commit (the successor commits the card for its §3 table without touching the slot — that must still read STALE); a refusal that names only one side; the gate applied to an explicit --stops; a delegation after the refusal. TESTS (test_rotate_verb.py, <= 5, on a tmp git repo with a card committed under the exact rotate-out message shape): unchanged slot -> exit 2 naming gen pair + sha, cmd_rotate_self NOT called; rewritten slot -> delegated; no rotate-out commit -> delegated; explicit --stops with a stale slot -> delegated; started record carries stops_sha256 (the record test seam test_rotate.py already uses). FILE SCOPE: rotate.py (`_stops_slot_is_stale` next to `_default_stops_text`, the call in cmd_rotate, the stops_sha256 line at the record), test_rotate_verb.py (+ one record test). EXCLUDED: cmd_rotate_self's body, `_default_stops_text`, the resolvers, the checklist, `_compose_after_join_dm` (SM.01 live on it), config:rotations. CEILING: <= 50 lines + <= 5 tests; rotate nbhd green."
thought_session: sensei-director-genXVIII-L18
title: rotate refuses a where-it-stops slot that is byte-identical to the predecessor's rotate-out commit — the stale block is named by gen pair + sha, never handed to the successor as fresh (SM 23:39Z residue (a) of SL7.115)
town: core
---
<!-- BODY:BEGIN -->
# hypothesis:l4-rotate-refuses-a-where-it-stops-slot-unchanged-since-the-predecessors-rotate-out-naming-the-gen-pair-and-commit

## Hypothesis

What is the testable claim? What would prove it? What would disprove it?

## Agent Notes
SM review by name (SL2#28 @d22584a70): ACCEPT with the overage on record — 160 lines vs the 50 ceiling; the director named the cause (record threading of stops_sha256 :3645-3671) and the tests are green; a live rotate-self --dry-run from this post stops earlier at prepare blockers, so the gate is verified by its tests, not live. Next time a 3x overage is a re-brief before the cut, not after.
