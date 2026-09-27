---
id: hypothesis:a-payload-ref-change-renames-the-file-in-the-same-write
mint_id: 0b764207c4494a45a5d167b539c75524
type: hypothesis
parents:
  - goal:g4.18.1.4
next_edges: []
confidence: 0.8
edited_by: a00-3d52306e
scaffold_hash: 8b25e9228029f4e9
season: 2
tags:
  - engine
  - write
  - node_writer
  - g4.18.1
testable_claim: "(1) a same-directory payload_ref change renames the file and the row in one write, mint_id unchanged (2) a cross-directory or cross-location change is refused unless explicitly confirmed (3) the row always resolves to an existing file and an existing destination is never overwritten (assigned: director-engine)"
title: "a payload_ref change renames the file in the same write; a directory move needs an explicit confirm (goal:g4.18.1.4; assigned: director-engine)"
town: core
---
# hypothesis:a-payload-ref-change-renames-the-file-in-the-same-write

## Measured
- A build node names its file by `payload_ref` + `location` (a base NAME, locations.payload_base, locations.py:445). A write that sets `location` in the same edit wins over disk (write.py ~2218-2221), but NOTHING moves the file: `grep -nE 'git mv|shutil.move|rename\('` over write.py + node_writer.py = 0 hits (`os.replace` only for atomic temp writes, node_writer.py:1127, :1203). So `set payload_ref=<new>` rewrites the row and leaves the file at the old name: the row dangles until a hand `git mv`.

## CLAIM
(1) a node write that changes `payload_ref` to a new NAME in the same directory renames the file and updates the row in ONE write (mint_id unchanged, the grid history of the node continuous) (2) a change that moves the file to another DIRECTORY or another `location` is REFUSED, naming both paths, unless the write carries an explicit confirm (one named flag/verb arg); with it, the move happens, WHETHER OR NOT the old file is in this checkout -- the gate is about the ROW, which outlives the checkout (3) a declared ref that names a file THIS CHECKOUT DOES NOT HOLD is still repointed, because a row may name bytes that were never created, are deleted, or live in another worktree, and refusing that would make the field unwritable on a partial clone; nothing is invented for it and no move is logged; WHERE THE BYTES ARE IN THIS CHECKOUT, the write that moves them leaves the row resolving to an existing file, the old path gone, and an existing file at the destination refused (never overwritten).

> Narrowed 2026-09-27 (DH.579, experiment:a00-3d52306e-031125). The prior text said "after ANY such write the row resolves to an existing file", which `test_payload_rename.py:140` (`test_a_declared_ref_with_no_file_here_is_not_a_refusal`) asserts the NEGATION of. A test that contradicts its own claim is a defect; the claim moved, not the test. Conjunct 2's shape is now the STRICT one: an absent source must NOT short-circuit the consent gate (it does today -- see the falsifiers below), because the row, unlike the bytes, does not disappear with the worktree.

## Dispatch line
config-max: none (bases are already config names). template-max: none. code: the rename path in the writer, because no mover exists.

- a same-dir rename on a temp build node leaves the old file or a dangling row, or changes mint_id.
- a cross-directory or cross-`location` change without `--confirm-move` moves any byte **or repoints the row** -- the ROW is what the gate protects, so an absent source must not buy a free cross-directory write. **OPEN, measured BROKEN by experiment:a00-6cb920d2-f30271 probe P5**: `plan_move` returns `_MovePlan(None, dest)` at node_writer.py:565, BEFORE the cross-directory refusal at :570, so an absent old file short-circuits the consent gate entirely. The one-line fix is ORDER: evaluate the cross-directory/cross-`location` refusal first, then treat a non-file source as nothing-to-move. Not fixed here (code slots closed; production-line budget of this chain is closed at the bytes on disk).
- a rename onto an existing file overwrites it, confirmed or not.
- a declared ref with no file here is REFUSED (the shape P4 regressed into and P4's fix re-closed): the row must still repoint. **Closed** by `test_a_declared_ref_with_no_file_here_is_not_a_refusal`.
- `unset payload_ref` (and any other verb that reaches the row's path WITHOUT going through `set_fm["payload_ref"]`/`set_fm["location"]`) leaves the bytes at the old path while the row stops naming them -- the mover's trigger at write.py:2257 is `"payload_ref" in set_fm or "location" in set_fm`, and `verb_unset` (write.py:288-293) only appends to `unset_fm`. **UNTRACKED, unmeasured, still open.** The ledger of paths-into-the-mover is: `set` yes; `sub` YES (a non-protected frontmatter value resolved by `_resolve_sub` lands in `edit.set_fm`, write.py:2418) and therefore covered by both the mover and the gate; `body_patch` NO (it writes `edit.sub_body` / `body_patch_diff` only and never reaches `set_fm`); `unset` NO.
- the two readers of the same field disagree: `links.link_ref` (links.py:124-142) resolves `link_ref:` FIRST and falls back to `payload_ref:`, while `write._payload_ref` (write.py:2783) does the OPPOSITE (`fm.get("payload_ref") or fm.get(links.LINK_FIELD)`). A node carrying BOTH fields is therefore renamed after one file and linked as another. **UNTRACKED defect, one-line fix: `_payload_ref` reads `link_ref` FIRST, so both readers share one order.** (`goal:g4.18.1.4:40` requires `broken_links` 0, so an order disagreement is a broken link, not a style point.)
- **`set payload_ref X` in the SAME write as a `payload` verb LOSES the new bytes.** MEASURED BROKEN here (DH.579, probe P-A): `submit()` takes the old pair at write.py:2169 and never re-reads `payload_ref` from `set_fm`; the rename happens at :2271-2276 and `replace_payload` runs AFTER it at :2278-2290, still aimed at the OLD ref. So `set payload_ref lib/renamed.py` + `payload <file>` renames the file, writes the row, and then raises `FileNotFoundError: payload .../lib/mod.py does not exist` out of `submit()` with the new bytes written NOWHERE. Observed residual: row `lib/renamed.py`, file `lib/renamed.py` holding the OLD bytes, the caller's payload lost. This is the sharpest remaining violation of "naming a file is ONE intention": the mover and the payload writer are two intentions wearing one command. The fix is to resolve the payload target from the EFFECTIVE pair (`set_fm` over disk), the same `_effective` shape submit already uses for the outside-ref gate at :2085-2096, so both land on the new path.
- `set location` in the same write as a payload verb, by contrast, is **CORRECT and needs no falsifier**: the rebinding at :2237 happens before both the plan and `replace_payload`, and the mover refuses the cross-base move without `--confirm-move`. Recorded so a later run does not re-open it. (The rebinding IS after the patch bytes are read for `sub payload` -- write.py:2380 -- so the diff is taken against the OLD base's bytes and written into the moved file; the result is consistent, which is why it is a note and not a defect.)

## TESTS
extensions/agi/tests/test_payload_rename.py (new; temp graph under tmp_path only). Neighbourhood: test_write*.py test_node_writer*.py test_links*.py. Every pytest under `timeout 600`, --basetemp under /tmp.

## FILE SCOPE
extensions/agi/bin/node_writer.py (a mover beside replace_payload) · extensions/agi/bin/write.py (ONLY the update path that calls it, ~2215-2250 -- never main()/create/answers: goal:g4.18.1.1 is under review there) · extensions/agi/tests/test_payload_rename.py.

## CEILING
1-2 kids · <= 45 production lines · pi-free tier-0 · 0 USD. No test spawns pytest; kids never launch real claude.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
DH.579 (a00-3d52306e) — the chain prose disagreed with the chain bytes, and prose is what a merge-pass reads. Three corrections, each measured against the bytes in this checkout rather than against a report. (1) CLAIM conjunct 3 narrowed: the old text said the row ALWAYS resolves to an existing file, and test_payload_rename.py:140 asserts the negation of exactly that for a declared ref this checkout does not hold. A test that contradicts its own claim is a defect, and the honest resolution is to narrow the claim, not to weaken the test — a row may name bytes that were never created, are deleted, or live in another worktree, and refusing that would make the field unwritable on a partial clone. Conjunct 2 is now the STRICT shape, because the gate protects the ROW and the row outlives the checkout. (2) FALSIFIERS gained the open cases a reader could not previously see: P5 (an absent source short-circuits the consent gate at node_writer.py:565, before the refusal at :570), unset payload_ref (outside the trigger, untested), the link_ref/payload_ref ORDER disagreement between links.link_ref and write._payload_ref (a one-line fix; broken_links 0 is a command-table requirement), and a NEW measurement of my own: set payload_ref X in the same write as a payload verb LOSES the caller's bytes, because the mover renames first (write.py:2271) while replace_payload still aims at the OLD ref read at :2169 — the write raises FileNotFoundError with the row written, the file moved, and the new bytes nowhere. (3) The set location + payload shape is correct, and is recorded as a NOTE so a later run does not re-open it as a bug. No test covers the new shapes, so these falsifiers are NAMED, not closed.
<!-- THOUGHT:END -->
