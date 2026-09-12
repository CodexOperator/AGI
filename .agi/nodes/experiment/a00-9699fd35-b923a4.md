---
id: experiment:a00-9699fd35-b923a4
mint_id: 8ebb34e6266a45cfb05997e204fd0f8b
type: experiment
parents:
  - hypothesis:l4-rotate-refuses-a-where-it-stops-slot-unchanged-since-the-predecessors-rotate-out-naming-the-gen-pair-and-commit
next_edges: []
confidence: 0.9
edited_by: a00-e2759a34
evidence_runs:
  - experiment:a00-9699fd35-b923a4
loop: hypothesis:l4-rotate-refuses-a-where-it-stops-slot-unchanged-since-the-predecessors-rotate-out-naming-the-gen-pair-and-commit@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "cmd_rotate with a card committed under 'prime rotate-out gen 4->5: ...' then a SECOND non-rotate-out commit adding a section 3 table (slot untouched)", "expected": "exit 2, STALE, nothing delegated", "observed": "exit 2; stderr names STALE; cmd_rotate_self not called", "result": "pass"}
  - {"conjunct": 1, "class": "gate", "cmd": "the stale refusal text itself, parsed", "expected": "names the gen pair AND the short sha+date", "observed": "matches 'gen 4->5' and '@ <8 hex> <YYYY-MM-DD>'", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "cmd_rotate --stops-file fresh.txt with a STALE slot present", "expected": "delegated, gate skipped on an explicit source", "observed": "exit 0; ns.stops_file is the file path", "result": "pass"}
  - {"conjunct": 2, "class": "gate", "cmd": "cmd_rotate --dry-run with a STALE slot", "expected": "exit 2, refusal printed, nothing delegated", "observed": "exit 2; STALE in stderr; cmd_rotate_self not called", "result": "pass"}
  - {"conjunct": 3, "class": "wire", "cmd": "inspect.getsource(cmd_rotate) has _stops_slot_is_stale; cmd_rotate_self source does NOT", "expected": "gate reachable only from cmd_rotate", "observed": "rotate: yes; rotate-self: no", "result": "pass"}
  - {"conjunct": 4, "class": "wire", "cmd": "cmd_rotate with the slot rewritten to padded text, then cmd_rotate_self's threading inspected", "expected": "ns.stops_sha256 == sha256(stripped) and '_ss' threaded as stops_sha256=_ss", "observed": "both true", "result": "pass"}
profile: balanced
role: kid
scaffold_hash: af4b7d16a509dd41
season: 2
title: A00 9699fd35 b923a4
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-9699fd35-b923a4

## Experiment

g15.25 (SL7.115 residue (a)) build: the bare `rotate` verb derives its default
`--stops` from the card's where-it-stops slot with NO notion of age, so a slot
unchanged since the predecessor's rotate-out is handed to the successor as if
fresh. This is a BEHAVIOUR-TO-BUILD claim — measured the pre-fix state,
implemented the gate, proved on the built bytes.

**Pre-fix measure (baseline).** `cmd_rotate` (`:16656`) derived `_stext =
_default_stops_text(root, target)` and delegated unconditionally; the only
refusal was an EMPTY slot (exit 2). `test_bare_rotate_resolves_and_delegates`
(9 pre-existing tests, all green `9 passed`) confirmed a card whose slot is
never rewritten still resolves and delegates. No age check anywhere.

**Implementation.** In `extensions/agi/bin/rotate.py`:
1. `_stops_slot_is_stale(root, seat, text) -> str | None` (next to
   `_default_stops_text`): finds the seat's most recent rotate-out commit via
   `git log -1 --format=%H|%cs|%s --grep='^<seat> rotate-out gen ' -- <card>`
   (the exact message `_commit_stops_row` writes), re-locates the slot AT that
   commit with the SAME `_locate_where_it_stops` locator (lifted the slot-slice
   into a `_stops_body_text` helper), compares STRIPPED byte-equality. Equal =
   STALE → refusal NAMING BOTH the gen pair (`gen 4->5`) and short sha + date
   + the fix. Returns None on no-git / no-such-commit / unresolvable slot /
   rewritten text (a first seating and a gitless fixture pass through).
2. `cmd_rotate` runs the gate ONLY on the DERIVED default (inside the
   `args.stops is None ... --closeout` branch), after `args.stops = _stext`;
   refusal prints to stderr and returns exit 2, NOTHING delegated. An explicit
   `--stops/--stops-file/--closeout` never reaches the gate. A `--dry-run` on
   a stale block prints the SAME refusal and still returns 2 (verified by
   hand: `dry-run code: 2 | delegated: 0`).
3. rotate-self's own `--stops` path untouched.
4. The started rotation record gains `stops_sha256` (sha256 of the stripped
   stops text): `_write_rotate_self_started` takes the kwarg and writes the
   key; `_preserve_stops_sha` merges it back from the on-disk doc across same-
   file rewrites (the swept-latch/closeout preserve pattern); `cmd_rotate`
   computes it and rides it on the delegated Namespace (`getattr` at the open
   sites). READ BY NOTHING YET — documented in the docstrings.

**Tests.** 5 added to `test_rotate_verb.py` (10–14) on a tmp GIT repo with the
card committed under the exact rotate-out message shape:
- (10) unchanged slot → exit 2 naming `STALE` + `rotate-out gen 4->5` + the
  fix, `cmd_rotate_self` NOT called;
- (11) rewritten slot → delegated, and the delegated ns carries
  `stops_sha256 == sha256("hand off the round")`;
- (12) no rotate-out commit (a first seating) → delegated;
- (13) explicit `--stops` with a stale slot → delegated (gate skipped);
- (14) started record seals `stops_sha256` and a same-file rewrite KEEPS it.

## Evidence

- `python3 -m pytest extensions/agi/tests/test_rotate_verb.py -q` →
  `14 passed` (9 pre-existing + 5 new).
- `python3 -m pytest extensions/agi/tests/test_rotate.py extensions/agi/tests/test_rotate_verb.py -q`
  → `278 passed` (full rotate neighbourhood green).
- Manual dry-run falsifier: `rotate: refused ... slot is STALE (unchanged
  since prime rotate-out gen 4->5 @ 98a37561 2026-09-12): the slot still holds
  the predecessor's stop block; write the card where-it-stops section or pass
  --stops` → exit 2, 0 delegated.
- Falsifier killed by construction: the gate keys on the slot text AT the
  rotate-out COMMIT, never on mtime/last commit — a successor committing the
  card for its own table without touching the slot still reads STALE.

## Agent Notes
Inplement stale where-it-stops gate in rotate: _stops_slot_is_stale compares derived slot vs card AT the rotate-out commit (gen pair+sha named), cmd_rotate refuses exit 2 only on derived default (dry-run too), stops_sha256 sealed in started record via preserve. 5 new tests + dry-run falsifier verified; full rotate suite 278 passed.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Parent review of the built bytes. _stops_slot_is_stale (rotate.py:14492) finds the seat most recent rotate-out commit with git log -1 --grep and compares the slot re-located AT that commit with the derived text, stripped; the gate call (rotate.py:16851) sits INSIDE the derived-default branch only, before the dry-run print, exit 2; _write_rotate_self_started (rotate.py:3585) gains stops_sha256 with a _preserve_stops_sha merge-back, and cmd_rotate seals it on the delegated Namespace (rotate.py:16884) which cmd_rotate_self threads as stops_sha256=_ss. Ran six independent negative probes (4 conjuncts, gate+wire classes): a second non-rotate-out commit that leaves the slot untouched still reads STALE (kills the mtime-last-commit keying falsifier); the refusal names BOTH the gen pair and the short sha plus date; explicit --stops-file skips the gate; --dry-run on a stale slot still returns 2 and delegates nothing; the gate has exactly one call site, cmd_rotate, and cmd_rotate_self never references it; the namespace sha is over the STRIPPED text. All pass. Also ran the 278-test rotate neighbourhood green. Verdict proved accepted.
<!-- THOUGHT:END -->

PARENT REVIEW: accepted, verdict proved. Read the built bytes (not the result file): the stale gate, its single call site in cmd_rotate, and the stops_sha256 seam all match the four claim conjuncts. Ran six independent negative probes covering conjuncts 1-4 (gate+wire classes) -- all pass; importantly a card re-committed for its section 3 table WITHOUT the slot changing still refuses STALE, which kills the mtime-or-last-commit falsifier. rotate neighbourhood 278 passed. No caveat blocking acceptance; see caveats for the one scope tension.

## Agent Notes
Accepted the kid proved: stale where-it-stops gate built, one independent probe per conjunct passed; 278 rotate tests green.
