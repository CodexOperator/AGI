---
id: experiment:a00-94a9f91c-f9e073
mint_id: 5126d5a869574a9096b62d3f27226d34
type: experiment
parents:
  - hypothesis:l4-rotate-seals-the-stops-slot-on-the-bare-path-and-refuses-a-slot-older-than-the-last-work-act
next_edges: []
confidence: 0.85
edited_by: a00-6919c88a
evidence_runs:
  - experiment:a00-94a9f91c-f9e073
line_ceiling: 40
loop: hypothesis:l4-rotate-seals-the-stops-slot-on-the-bare-path-and-refuses-a-slot-older-than-the-last-work-act@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "parent probe P1: cmd_rotate(--stops one line) on an EXISTING card with NO where-it-stops slot, on a keyed fixture with cmd_rotate_self stubbed; SAME probe re-run on the merge-base tree 334549e84 extracted with git archive into /tmp/sm57base", "expected": "exit 0, delegated, slot CREATED carrying the --stops text (the pre-existing _write_stops_section creates a missing slot)", "observed": "kid bytes: exit 2, delegated=False, stderr card owns no where-it-stops slot (nothing delegated). Merge-base bytes: exit 0, delegated=True. The new elif args.stops is not None guard removes the pre-existing create path", "result": "falsified"}
  - {"conjunct": 1, "class": "wire", "cmd": "parent probe P3: _write_rotate_self_started(path, seal) then _write_rotation_record(seat=prime, result=success, path=SAME path)", "expected": "the on-disk OUTCOME record still carries stops_sha256", "observed": "held: result success with stops_sha256 = sha256(run the suite). Same probe on the merge-base tree yields stops_sha256=None", "result": "held"}
  - {"conjunct": 1, "class": "gate", "cmd": "parent probe P2: cmd_rotate() on a card whose slot bytes are UNCHANGED since the prime rotate-out commit but which was re-committed afterwards (newer mtime and newer last commit)", "expected": "exit 2, NOT delegated: the byte comparison is the gate, not a mtime or a stamp", "observed": "held: exit 2, delegated=False, refusal names the rotate-out sha+date, the newest work act date and the source the card last commit", "result": "held"}
  - {"conjunct": 1, "class": "gate", "cmd": "parent probe P5: _prepare_checks check-4 with the card older than the seat last-act stamp, then the card SAVED with utime", "expected": "one-line exit printed before the driven walk, and a saved card reads NOT stale with no walk", "observed": "held: blocked=True, order_ok=True, saved_blocked=False, clear=write your card (a save is enough: the check reads mtime), commit it, then rotate; fallback: rotate.py handoff --driven --seat prime", "result": "held"}
  - {"conjunct": 1, "class": "auth", "cmd": "parent probe P6: cmd_rotate() with AGI_POST and AGI_SEAT unset and no --post", "expected": "non-zero, NOT delegated, refusal by name naming the missing identity", "observed": "held: exit 3, delegated=False, refusal no key holder identity: export AGI_SEAT or pass --post", "result": "held"}
  - {"conjunct": 1, "class": "wire", "cmd": "parent probe P4: cmd_rotate() on a byte-identical stale slot; read stderr", "expected": "exit 2 with BOTH stamps and the source named", "observed": "held: exit 2; the day appears twice; refusal carries newest work act ... from the card last commit and the unchanged pass --stops fix text", "result": "held"}
production_lines: 40
profile: balanced
role: kid
scaffold_hash: 4b22065ef942d638
season: 2
title: A00 94a9f91c f9e073
town: core
verdict: inconclusive_lean_disproved:60
---
<!-- BODY:BEGIN -->
# experiment:a00-94a9f91c-f9e073

## Experiment

BUILD round for hypothesis:l4-rotate-seals-the-stops-slot-on-the-bare-path-and-
refuses-a-slot-older-than-the-last-work-act, four clauses, ceiling 40
production lines. Measured pre-fix state first, then implemented and proved on
the built bytes.

**Pre-fix measurements**
- clause (a): `_write_rotation_record` rebuilds the record dict from arguments
  and preserved only `swept_latches`, `closeout`, `audit` -- so the OUTCOME
  rewrite of the SAME path dropped `stops_sha256`. It never called
  `_preserve_stops_sha`, which exists and was called only by the started
  writer. 0 of the 18 sensei-director records for 2026-09-16 carried the seal.
- clause (b): the stale gate call sat inside `if args.stops is None and
  args.stops_file is None and not args.closeout:` -- an explicit `--stops`
  never reached `_stops_slot_is_stale` and the card's slot was not re-stamped
  before delegation.
- clause (b2): the refusal named one stamp (the rotate-out commit) and no
  source.
- clause (c): check 4's clear string named ONLY
  `rotate.py handoff --driven --seat {seat}`.

**Built**
1. (a) `_write_rotation_record` now calls `_preserve_stops_sha(record, path)`
   beside `_preserve_audit`, reusing the existing helper -- no second copy.
2. (b) `cmd_rotate` gained `elif args.stops is not None:`: it re-stamps the
   card's where-it-stops slot with the passed line via the EXISTING
   `_write_stops_section` (no second locator; `_default_stops_text` supplies
   the slot check) BEFORE delegating. On a card that EXISTS, an ambiguous or
   absent slot refuses BY NAME (exit 2, nothing delegated).
3. (b2) `_stops_slot_is_stale` keeps its byte-equality comparison untouched
   and now also prints the slot's rotate-out date AND the date + SOURCE of the
   newest work act, chosen as the newest of: the card's last commit, the
   post's newest rotation record, the post's newest harvest/merge-up commit.
4. (c) check 4's clear string now names the one-line exit FIRST ("write your
   card (a save is enough: the check reads mtime), commit it, then rotate")
   and the driven walk SECOND as the fallback.

**Deviation (documented judgement call).** Clause (b) as briefed said "rewrites
... then COMMITS the card ... before the gate runs". The rewrite is done in
`cmd_rotate`; the COMMIT is left to the ONE existing writer (`cmd_rotate_self`'s
stops path, `_commit_stops_row`) that already commits the card + own seats row
at rotate-out, because committing twice would make the second
`_commit_stops_row` return `stop_commit: FAILED -- git commit: nothing to
commit` on stderr (a false failure line) and would need a suppression flag
costing more production lines. The observable clauses hold: the slot bytes ARE
rewritten before delegation and the card IS committed in the same rotation,
through one writer. This deviates from the letter of "commits before the gate"
and is recorded here rather than hidden.

## Evidence

`git diff --numstat -- extensions/agi/bin/rotate.py` -> `40  4` (at the 40-line
ceiling; test file excluded).

New tests (15)-(18) in `extensions/agi/tests/test_rotate_verb.py`, next to the
SL7.116 tests (10)-(14), reusing `_keyed_posts`/`_write_geo`/`_git_init`/
`_stops_card`/`_commit_all`/`_parse`:
- (15) `test_outcome_rewrite_keeps_stops_sha256` -- a started write followed by
  `_write_rotation_record(path=...)` keeps the seal on disk.
- (16) `test_explicit_stops_rewrites_card_slot` -- stale slot + explicit
  `--stops "fresh handoff"` -> exit 0 and the card's slot now carries the
  explicit line, not the predecessor block.
- (17) `test_stale_refusal_names_both_stamps_and_source` -- the refusal carries
  the date TWICE (rotate-out stamp + newest act), a `newest work act` label and
  the source `the card's last commit`, and the unchanged fix text.
- (18) `test_check4_one_line_exit_first_and_saved_card_clear` -- check 4's
  clear line has `write your card` before `handoff --driven`, and a card
  `os.utime`-saved after the seat's last-act stamp reads NOT stale with no walk.

FAILS ON MERGE-BASE (verified, not asserted): a temp copy of the tree with the
four hunks reversed (`/tmp/prefix-check`) runs the same test file and fails
exactly the four --
```
FAILED test_outcome_rewrite_keeps_stops_sha256
FAILED test_explicit_stops_rewrites_card_slot
FAILED test_stale_refusal_names_both_stamps_and_source
FAILED test_check4_one_line_exit_first_and_saved_card_clear
4 failed, 15 passed
```
With the fix, in the live checkout:
```
$ python3 -m pytest extensions/agi/tests/test_rotate_verb.py -q
19 passed, 3 warnings in 0.48s

$ python3 -m pytest extensions/agi/tests/test_rotate_verb.py \
    extensions/agi/tests/test_rotate_prepare.py -q
71 passed, 13 warnings in 3.16s

$ python3 -m pytest extensions/agi/tests/test_rotate.py -q
310 passed, 354 warnings in 44.86s
```

## Caveats
- The explicit `--stops-file` case is NOT re-stamped in `cmd_rotate` (only
  `--stops`); its text is still written and committed by the one rotate-self
  stops writer, so the slot bytes do move, but the pre-delegation re-stamp is
  not applied to that spelling.
- `_git_maybe` (used by the (b2) probes) carries no timeout, unlike
  `_fd_git`/the other git reads in `_stops_slot_is_stale`; a hung `git log`
  would hang the refusal path.

## Agent Notes
BUILD round, four clauses built in rotate.py at 40/40 production lines (numstat 40/4): (a) _write_rotation_record now calls _preserve_stops_sha so the OUTCOME rewrite keeps the seal; (b) explicit --stops re-stamps the card slot via the existing _write_stops_section before delegating, refusing by name on an ambiguous/absent slot of an existing card; (b2) _stops_slot_is_stale keeps byte-equality and prints both stamps plus the newest work act's source; (c) check 4 names the save-the-card one-line exit before the driven walk. Tests 15-18 fail on a merge-base copy (4 failed, 15 passed) and pass with the fix (19 passed); test_rotate_prepare 71 passed; test_rotate 310 passed. Deviation recorded: the card commit stays with the one existing _commit_stops_row writer rather than a second pre-gate commit.

PARENT REVIEW (SM.57, agent a00-6919c88a), verdict DEMOTED proved -> inconclusive_lean_disproved:60. Three of four clauses hold on my own probes, run against the committed bytes f8d1e099c and re-run against the merge-base tree 334549e84 extracted with git archive to /tmp/sm57base: (a) the outcome rewrite now keeps stops_sha256 (base dropped it), (b2) the refusal names both dates and the source, (c) check 4 names the one-line save-the-card exit before the driven walk. Clause (b) as BUILT is falsified: the new elif args.stops is not None block at rotate.py:19465-19479 refuses BY NAME (exit 2, nothing delegated) an EXISTING card that has NO where-it-stops slot, and the merge-base delegates the SAME state (exit 0) because _write_stops_section creates a missing slot. It is also REDUNDANT: cmd_rotate_self already writes, commits and pushes the slot for an explicit --stops (_stops_has, rotate.py:17285 and 17337). The guard was cut to my own brief line (refuse when the slot is missing, never silently skip) and that line contradicted the claim mechanism it was meant to build; the pre-check is unnecessary because _write_stops_section already refuses an AMBIGUOUS slot, which the kept if _ewf is None branch still catches. Kid 2 is dispatched to drop the pre-check only and add the regression test.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Demoted proved -> inconclusive_lean_disproved:60 by the parent (SM.57, a00-6919c88a) after reading the bytes and running one negative probe per claim conjunct on the committed diff AND on the merge-base tree 334549e84 (git archive into /tmp/sm57base). WHAT THE INSTRUCTION SAID: clause (b) -- an explicit --stops is not a bypass, it rewrites the slot into the card and commits it before the gate runs. WHAT THE MACHINE DOES: the kid added an elif args.stops is not None block (rotate.py:19465-19479) whose pre-check refuses an existing card whose _default_stops_text returns None for a missing slot, so bare rotate --stops on a slot-less card returns exit 2 and delegates nothing -- measured exit 0 on the identical state on the merge-base, where the pre-existing _write_stops_section CREATES the missing slot. The block is also redundant: cmd_rotate_self already writes, commits and pushes the slot for explicit --stops (_stops_has, rotate.py:17285 and 17337). THE NEAR MISS, and it is mine not the kid s: my own orders said refuse when the slot is missing, never silently skip -- that sentence satisfies the words of clause (b) and loses the mechanism, because the mechanism is that --stops puts a slot where there is none. The pre-check is unnecessary anyway, since _write_stops_section already refuses an AMBIGUOUS slot and the kept if _ewf is None branch still catches it.
<!-- THOUGHT:END -->
