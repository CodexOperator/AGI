---
id: experiment:a00-449411a8-a27f69
mint_id: db48e1191cfe4ce4a55e85c2532882f4
type: experiment
parents:
  - hypothesis:l4-rotate-seals-the-stops-slot-on-the-bare-path-and-refuses-a-slot-older-than-the-last-work-act
next_edges: []
confidence: 0.9
edited_by: a00-6919c88a
evidence_runs:
  - experiment:a00-449411a8-a27f69
line_ceiling: 40
loop: hypothesis:l4-rotate-seals-the-stops-slot-on-the-bare-path-and-refuses-a-slot-older-than-the-last-work-act@s2
model: ~deepseek/deepseek-v4-flash-latest
probes:
  - {"conjunct": 1, "class": "gate", "cmd": "parent probe P1-cured: cmd_rotate(--stops one line) on an EXISTING card with NO where-it-stops slot, keyed fixture, cmd_rotate_self stubbed; plus _write_stops_section on a copy of that card", "expected": "exit 0 and delegated (NOT refused), and _write_stops_section CREATES the slot carrying the line", "observed": "held: exit=0 delegated=True; _write_stops_section returns slot=created with the line present. On kid 1 bytes the SAME state was exit 2 delegated=False; on the merge-base tree 334549e84 it is exit 0 delegated=True -- the regression is cured", "result": "held"}
  - {"conjunct": 1, "class": "wire", "cmd": "parent probe P2-wire: _write_stops_section(card, seat, line) then _write_stops_section(card, seat, line, frac=0.42) -- the new pre-delegation write plus the delegate own write -- compared byte-for-byte against ONE _write_stops_section(..., frac=0.42), on both a card WITH a slot and a card with NO slot", "expected": "the double write is byte-identical to the single write, so the live bare rotate --stops flow ends with the same card as before the change", "observed": "held: byte-identical on both shapes; no double fence, no duplicated slot", "result": "held"}
  - {"conjunct": 1, "class": "wire", "cmd": "parent probe P3 (re-run on this kid bytes): _write_rotate_self_started(path, seal) then _write_rotation_record(seat=prime, result=success, path=SAME path)", "expected": "the on-disk OUTCOME record still carries stops_sha256", "observed": "held: result=success with stops_sha256 = sha256(run the suite)", "result": "held"}
  - {"conjunct": 1, "class": "gate", "cmd": "parent probe P2 (re-run): cmd_rotate() with slot bytes UNCHANGED since the rotate-out commit but the card re-committed after (newer mtime and newer last commit)", "expected": "exit 2, NOT delegated: byte comparison is the gate, not a mtime", "observed": "held: exit 2, delegated=False, refusal names the rotate-out sha+date, the newest work act date and the source the card last commit", "result": "held"}
  - {"conjunct": 1, "class": "gate", "cmd": "parent probe P5 (re-run): _prepare_checks check-4 with the card older than the seat last-act stamp, then saved with utime", "expected": "one-line exit before the walk; saved card not stale", "observed": "held: blocked=True, order_ok=True, saved_blocked=False", "result": "held"}
  - {"conjunct": 1, "class": "auth", "cmd": "parent probe P6 (re-run): cmd_rotate() with AGI_POST and AGI_SEAT unset and no --post", "expected": "non-zero, NOT delegated, refusal by name", "observed": "held: exit 3, delegated=False, no key holder identity", "result": "held"}
production_lines: 11
profile: balanced
role: kid
scaffold_hash: 22b34748b1e27c79
season: 2
title: A00 449411a8 a27f69
town: core
verdict: proved
---
<!-- BODY:BEGIN -->
# experiment:a00-449411a8-a27f69

## Experiment

Kid #2 on hypothesis:l4-rotate-seals-the-stops-slot-on-the-bare-path-and-refuses-a-slot-older-than-the-last-work-act.
Corrective round after the parent falsified kid #1's clause (b) pre-check.

**What I changed** — `extensions/agi/bin/rotate.py`, the `elif args.stops is not
None:` arm of `cmd_rotate` (19468-19479). DELETED the 7-line pre-check that
refused an existing own card whose where-it-stops slot was missing or ambiguous
BY NAME before delegating. KEPT `_ecard = _own_card_path(root, target)`,
`_write_stops_section(_ecard, target, args.stops)` and the `if _ewf is None:`
refusal that follows it. Added a 2-line comment naming why the pre-check is gone
(`_write_stops_section` itself CREATES a missing slot and returns `(None, ...)`
for an ambiguous one). Net `git diff --numstat HEAD -- extensions/agi/bin/rotate.py`
= `3  8` (3 added, 8 removed: net -5 lines), measured on my first test run.
Clauses (a), (b2), (c) untouched.

**Test-first, failure verified BEFORE the deletion** — new test (19)
`test_explicit_stops_on_card_with_no_slot_delegates` in
`extensions/agi/tests/test_rotate_verb.py`, beside (15)-(18), reusing
`_keyed_posts` / `_write_geo` / `_git_init` / `_parse`: a card that EXISTS
carrying `# card` + `lead only, no stops slot` and no where-it-stops section, an
explicit `--stops "fresh one line"`, `cmd_rotate_self` stubbed to capture.

On kid #1's committed bytes (HEAD = f8d1e099c) it FAILED exactly as the parent's
probe P1 predicted:

    assert 2 == 0
    E       assert 2 == 0
    Captured stderr call:
    rotate refused: card owns no where-it-stops slot (.../sessions/quorum/prime.md) (nothing delegated)

After the deletion it PASSES: exit 0, the stub is called, `ns.stops == "fresh one
line"`, and the write the delegation performs is exercised for real —
`_write_stops_section(copy, "prime", "fresh one line")` returns
`slot == "created"` with `"fresh one line"` in the returned body.

## Evidence

```
$ python3 -m pytest extensions/agi/tests/test_rotate_verb.py -q
20 passed, 3 warnings in 0.50s

$ python3 -m pytest extensions/agi/tests/test_rotate_prepare.py -q
52 passed, 10 warnings in 2.41s
```

Capability check — the AMBIGUOUS arm the pre-check claimed to guard is still
refused by NAME at the same exit code, by `_write_stops_section` itself, nothing
delegated (scratch probe `.agi/sessions/iter-SM.57/a00-449411a8/probe_ambiguous.py`,
a card with two `## 🔴 Where it stops` sections + `--stops`):

    rotate refused: ambiguous where-it-stops slot on the own card; refused (rotate-self --stops never guesses) (nothing delegated)
    AMBIGUOUS-CARD rc: 2

So no capability is lost and the missing-slot CREATE path is restored: the
delegated `cmd_rotate_self` still writes, commits (`_commit_stops_row`) and
pushes the slot for an explicit `--stops` (`_stops_has` at 17285), and
`_write_stops_section` already creates-or-refuses on its own.

<!-- THOUGHT:BEGIN — authored, not derived; carried across regenerating scans. The reasoning behind THIS version. -->
Kept proved by the parent (SM.57, a00-6919c88a). WHY THIS VERSION DIFFERS: it removes the seven-line pre-check that kid 1 added inside the elif args.stops is not None block, and removes nothing else. WHAT THE INSTRUCTION SAID: clause (b), an explicit --stops is not a bypass -- it rewrites the slot into the card. WHAT THE MACHINE DID: kid 1 s pre-check refused an existing card with no where-it-stops slot (measured exit 2, delegated=False), while the merge-base delegates the identical state (exit 0) because _write_stops_section CREATES a missing slot (rotate.py:16508 docstring and 16521-16531). The block was also redundant: cmd_rotate_self already writes, commits and pushes the slot for explicit --stops (_stops_has at rotate.py:17285, write at 17378, commit at 17383, push at 17384). THE NEAR MISS, and it was the parent s: the order that produced the pre-check (refuse when the slot is missing) satisfies the words of clause (b) and loses the mechanism, because the mechanism is that --stops puts a slot where there is none. The pre-check is unnecessary in any case -- _write_stops_section already returns (None, ambiguous ...) for the one case that must refuse, and the kept if _ewf is None branch catches it. The parent probe that falsified kid 1 (P1) and a new double-write idempotence wire probe both hold on these bytes.
<!-- THOUGHT:END -->

## Agent Notes
Deleted kid#1's redundant (b) pre-check in rotate.py cmd_rotate elif --stops arm (net -5 lines: 3 added/8 removed); test (19) test_explicit_stops_on_card_with_no_slot_delegates verified FAILING on kid#1 bytes (exit 2, 'card owns no where-it-stops slot') then PASSING (exit 0, stub called, _write_stops_section returns slot='created'); ambiguous card still refuses by name at exit 2 via _write_stops_section; test_rotate_verb.py 20 passed, test_rotate_prepare.py 52 passed.

PARENT REVIEW (SM.57, a00-6919c88a). Verdict KEPT proved. Read the bytes (git diff f8d1e099c..6875c2e9d: rotate.py 3 added / 8 removed, tests +30) and ran one negative probe per conjunct on THIS kid bytes. The single demanded correction landed exactly: the pre-check that refused a missing where-it-stops slot is gone, the _write_stops_section call and the if _ewf is None refusal are kept, so an AMBIGUOUS slot still refuses while a MISSING one is created. My falsifying probe P1 now reads exit 0 delegated=True and _write_stops_section returns slot=created. Two extra parent probes beyond the falsifier: (i) a double-write idempotence WIRE probe -- the new pre-delegation write followed by the delegate own write is byte-identical to the single write, on a card with a slot and on one without, so the live flow ends with the same card; (ii) P3 the outcome rewrite keeps the seal. Clauses (a) (b2) (c) re-probed and held. Remaining caveat carried from kid 1: --stops-file is not pre-written in cmd_rotate (it is still written and committed by the one rotate-self stops writer), and _git_maybe carries no timeout.
